"""Deterministic tests for the earnings/macro desk feeds and nightly-outcomes endpoint.

All feeds read the nightly AM report and fail closed: a missing or unreadable
report yields an explicit empty feed (or 503 for the outcomes endpoint), never
fabricated candidates. trade_authorized is always False.
"""

import json
import tempfile
import unittest
from pathlib import Path

from hedge_desk.candidates import (
    build_earnings_candidate_feed,
    build_macro_candidate_feed,
)
from hedge_desk.server import build_nightly_outcomes_payload


def _write_report(tmp, **sections):
    report = {"schema_version": "hedge-desk-nightly-1.0.0", "mode": "REAL_EOD_NIGHTLY"}
    report.update(sections)
    path = Path(tmp) / "am-report-latest.json"
    path.write_text(json.dumps(report), encoding="utf-8")
    return str(path)


def _earnings_entry(**overrides):
    entry = {
        "mode": "REAL_EDGAR_EARNINGS",
        "cik": "0000320193",
        "data_source": "sec-edgar-xbrl-http-200",
        "observation": {
            "latest_fy_eps": 7.49,
            "latest_fy_period": "2025-09-27",
            "latest_quarterly_eps": 2.03,
            "latest_quarterly_period": "2026-06-27",
            "prior_quarterly_eps": 2.02,
            "prior_quarterly_period": "2026-03-28",
        },
        "trade_authorized": False,
    }
    entry.update(overrides)
    return entry


class EarningsFeedTests(unittest.TestCase):
    def test_missing_report_fails_closed(self):
        feed = build_earnings_candidate_feed("/nonexistent/am-report-latest.json")
        self.assertEqual(feed["candidate_definition"], "NIGHTLY_REPORT_MISSING")
        self.assertEqual(feed["candidates"], [])

    def test_unreadable_report_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "am-report-latest.json"
            path.write_text("not json", encoding="utf-8")
            feed = build_earnings_candidate_feed(str(path))
            self.assertEqual(feed["candidate_definition"], "NIGHTLY_REPORT_UNREADABLE")
            self.assertEqual(feed["candidates"], [])

    def test_maps_real_edgar_entry(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_report(
                tmp, earnings_actuals={"0000320193": _earnings_entry()}
            )
            feed = build_earnings_candidate_feed(path)
            self.assertEqual(feed["candidate_definition"], "REAL_EDGAR_EARNINGS_ACTUALS")
            self.assertEqual(len(feed["candidates"]), 1)
            c = feed["candidates"][0]
            self.assertEqual(c["desk_id"], "earnings-event-desk")
            self.assertEqual(c["symbol"], "AAPL")
            self.assertEqual(c["cik"], "0000320193")
            self.assertEqual(c["stage"], "REAL_EDGAR_EARNINGS")
            self.assertIn("2.03", c["method"])
            self.assertFalse(c["trade_authorized"])

    def test_skips_blocked_entries(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_report(
                tmp,
                earnings_actuals={
                    "0000320193": _earnings_entry(),
                    "0000789019": {"mode": "BLOCKED", "reason": "edgar_timeout"},
                },
            )
            feed = build_earnings_candidate_feed(path)
            self.assertEqual(len(feed["candidates"]), 1)

    def test_unknown_cik_falls_back_to_cik(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_report(
                tmp, earnings_actuals={"0009999999": _earnings_entry()}
            )
            feed = build_earnings_candidate_feed(path)
            self.assertEqual(feed["candidates"][0]["symbol"], "0009999999")


class MacroFeedTests(unittest.TestCase):
    def _macro_section(self, **overrides):
        section = {
            "mode": "REAL_FRED_MACRO",
            "data_source": "fred-public-csv-http-200",
            "unemployment_rate_pct": "4.20",
            "unemployment_date": "2026-08-01",
            "treasury_5y": "4.78",
            "treasury_5y_date": "2026-09-17",
            "treasury_30y": "5.29",
            "treasury_30y_date": "2026-09-17",
        }
        section.update(overrides)
        return section

    def test_missing_report_fails_closed(self):
        feed = build_macro_candidate_feed("/nonexistent/am-report-latest.json")
        self.assertEqual(feed["candidate_definition"], "NIGHTLY_REPORT_MISSING")
        self.assertEqual(feed["candidates"], [])

    def test_maps_real_fred_observations(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_report(tmp, macro_environment=self._macro_section())
            feed = build_macro_candidate_feed(path)
            self.assertEqual(feed["candidate_definition"], "REAL_FRED_MACRO_OBSERVATIONS")
            symbols = [c["symbol"] for c in feed["candidates"]]
            self.assertEqual(symbols, ["UNRATE", "DGS5", "DGS30"])
            for c in feed["candidates"]:
                self.assertEqual(c["desk_id"], "macro-rates-desk")
                self.assertEqual(c["instrument_type"], "MACRO_SERIES")
                self.assertFalse(c["trade_authorized"])
            self.assertIn("4.20%", feed["candidates"][0]["method"])

    def test_blocked_macro_yields_empty_feed_with_reason(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_report(tmp, macro_environment={"mode": "BLOCKED"})
            feed = build_macro_candidate_feed(path)
            self.assertEqual(feed["candidate_definition"], "FRED_SECTIONS_BLOCKED")
            self.assertEqual(feed["candidates"], [])
            self.assertIn("reason", feed)


class NightlyOutcomesTests(unittest.TestCase):
    def test_missing_report_raises(self):
        with self.assertRaises(FileNotFoundError):
            build_nightly_outcomes_payload("/nonexistent/am-report-latest.json")

    def test_unreadable_report_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "am-report-latest.json"
            path.write_text("not json", encoding="utf-8")
            with self.assertRaises(ValueError):
                build_nightly_outcomes_payload(str(path))

    def test_passes_through_real_sections_verbatim(self):
        outcomes = {"mode": "PAPER_OUTCOME_SUMMARY", "entry_count": 0}
        sheets = {"mode": "YELLOW_SHEET_SUMMARY", "sheet_count": 0}
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_report(
                tmp,
                paper_outcome_summary=outcomes,
                yellow_sheets=sheets,
                report_sha256="abc",
            )
            payload = build_nightly_outcomes_payload(path)
            self.assertEqual(payload["paper_outcome_summary"], outcomes)
            self.assertEqual(payload["yellow_sheets"], sheets)
            self.assertEqual(payload["report_sha256"], "abc")
            self.assertFalse(payload["trade_authorized"])

    def test_empty_report_is_honest_not_synthetic(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_report(tmp)
            payload = build_nightly_outcomes_payload(path)
            self.assertEqual(
                payload["paper_outcome_summary"]["status"], "NO_OUTCOMES_RECORDED"
            )
            self.assertEqual(
                payload["yellow_sheets"]["status"], "NO_SHEETS_RECORDED"
            )

    def test_outcomes_route_serves_503_when_report_missing(self):
        from unittest import mock

        from hedge_desk import server as _server

        _server._api_cache.pop("nightly-outcomes", None)

        def _boom(report_path="artifacts/am-report-latest.json"):
            raise FileNotFoundError("nightly report not found: nope")

        statuses = []
        with mock.patch.object(
            _server, "build_nightly_outcomes_payload", _boom
        ):
            body = b"".join(
                _server._dispatch(
                    {"PATH_INFO": "/api/nightly-outcomes", "REQUEST_METHOD": "GET"},
                    lambda s, h: statuses.append(s),
                )
            )
        payload = json.loads(body)
        self.assertTrue(statuses[0].startswith("503"))
        self.assertEqual(payload["status"], "NIGHTLY_REPORT_UNAVAILABLE")
        self.assertFalse(payload["trade_authorized"])


if __name__ == "__main__":
    unittest.main()
