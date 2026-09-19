"""Deterministic tests for the real SEC EDGAR earnings desk (no network)."""

import json
import unittest

from hedge_desk.earnings_desk import earnings_desk, parse_eps_concept


def _concept(cik):
    return json.dumps(
        {
            "cik": cik,
            "units": {
                "USD/shares": [
                    {"end": "2025-09-27", "val": 7.49, "form": "10-K", "fy": 2025, "fp": "FY"},
                    {"end": "2026-03-28", "val": 2.02, "form": "10-Q", "fy": 2026, "fp": "Q2"},
                    # Restated prior quarter (same end date, newer filing -> authoritative).
                    {"end": "2026-03-28", "val": 2.05, "form": "10-Q/A", "fy": 2026, "fp": "Q2"},
                    {"end": "2026-06-27", "val": 2.03, "form": "10-Q", "fy": 2026, "fp": "Q3"},
                ]
            },
        }
    ).encode("utf-8")


class _FakeTransport:
    def __init__(self, cik):
        self.cik = cik

    def __call__(self, url):
        return 200, _concept(self.cik)


class EarningsDeskTests(unittest.TestCase):
    def test_latest_fy_and_quarters(self):
        r = earnings_desk("0000320193", transport=_FakeTransport("0000320193"))
        obs = r["observation"]
        self.assertEqual(r["mode"], "REAL_EDGAR_EARNINGS")
        self.assertEqual(obs["latest_fy_eps"], "7.49")
        # Latest quarter unaffected by a prior-period restatement.
        self.assertEqual(obs["latest_quarterly_eps"], "2.03")
        self.assertEqual(obs["latest_quarterly_period"], "2026-06-27")

    def test_restated_prior_period_is_authoritative(self):
        r = earnings_desk("0000320193", transport=_FakeTransport("0000320193"))
        obs = r["observation"]
        # Prior is the distinct earlier period, using the restated (later) value 2.05.
        self.assertEqual(obs["prior_quarterly_period"], "2026-03-28")
        self.assertEqual(obs["prior_quarterly_eps"], "2.05")
        # Change = latest (2.03) - prior restated (2.05).
        self.assertEqual(r["quarterly_eps_change"], "-0.02")

    def test_never_authorizes_or_computes_surprise(self):
        r = earnings_desk("0000320193", transport=_FakeTransport("0000320193"))
        self.assertFalse(r["trade_authorized"])
        self.assertFalse(r["surprise_computed"])
        self.assertEqual(r["data_source"], "sec-edgar-xbrl-http-200")

    def test_parse_rejects_malformed(self):
        with self.assertRaises(ValueError):
            parse_eps_concept(b"not json")


if __name__ == "__main__":
    unittest.main()