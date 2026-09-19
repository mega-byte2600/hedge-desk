"""Deterministic tests for the real-EOD candidate feed (no network)."""

import json
import tempfile
import unittest
from pathlib import Path

from hedge_desk.candidates import build_real_eod_candidate_feed


def _write_report(tmp, candidates=None):
    report = {
        "schema_version": "hedge-desk-nightly-1.0.0",
        "mode": "REAL_EOD_NIGHTLY",
        "candidates": candidates
        or [
            {
                "symbol": "AAPL",
                "strategy": "CASH_SECURED_PUT",
                "strike": "302.52",
                "requirement": "30252.00",
                "trade_authorized": False,
            }
        ],
    }
    path = Path(tmp) / "am-report-latest.json"
    path.write_text(json.dumps(report), encoding="utf-8")
    return str(path)


class RealEodFeedTests(unittest.TestCase):
    def test_missing_report_fails_closed(self):
        feed = build_real_eod_candidate_feed("/nonexistent/am-report-latest.json")
        self.assertEqual(feed["mode"], "REAL_EOD")
        self.assertEqual(feed["candidate_definition"], "NIGHTLY_REPORT_MISSING")
        self.assertEqual(feed["candidates"], [])

    def test_unreadable_report_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "am-report-latest.json"
            path.write_text("not json", encoding="utf-8")
            feed = build_real_eod_candidate_feed(str(path))
            self.assertEqual(feed["candidate_definition"], "NIGHTLY_REPORT_UNREADABLE")
            self.assertEqual(feed["candidates"], [])

    def test_maps_candidates_into_shared_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            feed = build_real_eod_candidate_feed(_write_report(tmp))
            self.assertEqual(feed["mode"], "REAL_EOD")
            self.assertEqual(feed["candidate_definition"], "REAL_EOD_PREMIUM_CANDIDATES")
            self.assertEqual(len(feed["candidates"]), 1)
            c = feed["candidates"][0]
            self.assertEqual(c["desk_id"], "overnight-premium-desk")
            self.assertEqual(c["symbol"], "AAPL")
            self.assertEqual(c["instrument_type"], "EQUITY_OPTIONS")
            self.assertIn("CASH_SECURED_PUT", c["method"])
            self.assertFalse(c["trade_authorized"])

    def test_never_authorizes(self):
        with tempfile.TemporaryDirectory() as tmp:
            feed = build_real_eod_candidate_feed(_write_report(tmp))
            self.assertTrue(all(not c["trade_authorized"] for c in feed["candidates"]))


if __name__ == "__main__":
    unittest.main()