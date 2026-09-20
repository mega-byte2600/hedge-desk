"""Deterministic tests for the FRED macro desk (no network)."""

import unittest
from datetime import date

from hedge_desk.macro_desk import macro_environment


class _FakeTransport:
    def __init__(self, data):
        self.data = data  # series_id -> csv text

    def __call__(self, url):
        series = url.split("id=")[1].split("&")[0]
        csv = self.data.get(series, "observation_date,VALUE\n")
        return 200, csv.encode("utf-8")


class MacroDeskTests(unittest.TestCase):
    def test_reports_inflation_unemployment_and_curve(self):
        data = {
            "CPIAUCSL": "observation_date,CPIAUCSL\n"
                        "2025-08-01,320.0\n2026-08-01,334.131\n",
            "UNRATE": "observation_date,UNRATE\n2026-08-01,4.1\n",
            "DGS5": "observation_date,DGS5\n2026-09-17,4.78\n",
            "DGS30": "observation_date,DGS30\n2026-09-17,5.29\n",
        }
        r = macro_environment(transport=_FakeTransport(data), as_of=date(2026, 9, 17))
        self.assertEqual(r["mode"], "REAL_FRED_MACRO")
        # (334.131 - 320.0) / 320.0 = 4.416%
        self.assertAlmostEqual(float(r["cpi_yoy_pct"]), 4.416, places=2)
        self.assertEqual(r["unemployment_rate_pct"], "4.1")
        self.assertEqual(r["treasury_5y"], "4.78")
        self.assertEqual(r["treasury_30y"], "5.29")
        self.assertFalse(r["trade_authorized"])
        self.assertEqual(r["blocked"], [])

    def test_all_blocked_flips_mode_to_blocked(self):
        # DATA peer-review: if every series is blocked, the desk must not claim
        # REAL_FRED_MACRO — it reports mode BLOCKED.
        r = macro_environment(transport=_FakeTransport({}), as_of=date(2026, 9, 17))
        self.assertEqual(r["mode"], "BLOCKED")
        self.assertIn("all_fred_series_blocked", r.get("reason", ""))

    def test_missing_series_is_blocked_not_fabricated(self):
        data = {
            "CPIAUCSL": "observation_date,CPIAUCSL\n2026-08-01,334.131\n",
            "UNRATE": "observation_date,UNRATE\n2026-08-01,4.1\n",
        }
        r = macro_environment(transport=_FakeTransport(data), as_of=date(2026, 9, 17))
        # CPI present but no 12-month prior -> YoY blocked; 5y/30y absent -> blocked
        self.assertIn("CPIAUCSL_YOY", r["blocked"])
        self.assertIn("DGS5", r["blocked"])
        self.assertIn("DGS30", r["blocked"])
        self.assertNotIn("cpi_yoy_pct", r)
        self.assertNotIn("treasury_5y", r)
        # the ones that succeeded are still reported
        self.assertEqual(r["unemployment_rate_pct"], "4.1")


if __name__ == "__main__":
    unittest.main()