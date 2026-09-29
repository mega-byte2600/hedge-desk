"""Deterministic tests for the data-quality monitor (no network).

The monitor scans a nightly AM report and flags DOWN/STALE/MISSING sources
loudly, so a failed source can never slide by silently again.
"""

import unittest
from datetime import date

from hedge_desk.data_quality import (
    SEV_DOWN,
    SEV_MISSING,
    SEV_OK,
    SEV_STALE,
    quality_report,
)


def _base_report():
    return {
        "macro_environment": {
            "mode": "REAL_FRED_MACRO",
            "as_of": "2026-09-25",
        },
        "rates_environment": {
            "mode": "REAL_FRED_RATES",
            "as_of": "2026-09-25",
        },
        "data_freshness": {
            "as_of": "2026-09-25",
            "expected_trading_day": "2026-09-25",
            "is_current": True,
        },
        "eod_batch_status": "READY_FOR_RESEARCH",
        "oil_market": {"mode": "REAL_WTI"},
        "earnings_actuals": {"mode": "REAL_SEC"},
        "chain_income": {"mode": "REAL_CBOE"},
    }


class QualityReportTests(unittest.TestCase):
    def test_all_ok(self):
        q = quality_report(_base_report(), as_of=date(2026, 9, 26))
        self.assertEqual(q["overall"], SEV_OK)
        self.assertEqual(q["alert_count"], 0)
        self.assertEqual(q["summary"], "All data sources OK.")

    def test_fred_blocked_is_down_and_loud(self):
        r = _base_report()
        r["macro_environment"] = {
            "mode": "BLOCKED",
            "blocked": ["CPIAUCSL", "UNRATE"],
            "reason": "all_fred_series_blocked",
        }
        q = quality_report(r, as_of=date(2026, 9, 26))
        self.assertEqual(q["overall"], SEV_DOWN)
        loud = {a["source"]: a for a in q["loud_alerts"]}
        self.assertIn("Macro/FRED", loud)
        self.assertEqual(loud["Macro/FRED"]["severity"], SEV_DOWN)
        self.assertIn("CPIAUCSL", loud["Macro/FRED"]["message"])
        # The alert tells the user what to do.
        self.assertIn("FRED_API_KEY", loud["Macro/FRED"]["detail"])

    def test_missing_section(self):
        r = _base_report()
        del r["oil_market"]
        q = quality_report(r, as_of=date(2026, 9, 26))
        loud = {a["source"]: a for a in q["loud_alerts"]}
        self.assertEqual(loud["Oil/WTI"]["severity"], SEV_MISSING)

    def test_stale_eod(self):
        r = _base_report()
        r["data_freshness"] = {
            "as_of": "2026-09-24",
            "expected_trading_day": "2026-09-25",
            "is_current": False,
        }
        q = quality_report(r, as_of=date(2026, 9, 26))
        loud = {a["source"]: a for a in q["loud_alerts"]}
        self.assertEqual(loud["EOD"]["severity"], SEV_STALE)
        self.assertIn("2026-09-24", loud["EOD"]["message"])

    def test_worst_severity_wins(self):
        r = _base_report()
        r["macro_environment"] = {"mode": "BLOCKED", "blocked": [], "reason": "x"}
        del r["oil_market"]
        q = quality_report(r, as_of=date(2026, 9, 26))
        # MISSING (3) outranks DOWN (2).
        self.assertEqual(q["overall"], SEV_MISSING)


if __name__ == "__main__":
    unittest.main()
