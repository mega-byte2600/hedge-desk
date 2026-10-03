"""Regression: production surfaces must never serve synthetic data.

User directive (2026-09-30, enforced 2026-10-03): no synthetic data anywhere
in production. Live timestamped data or the latest real batch only. Missing
data renders as ``data unavailable`` plus reason.
"""

import json
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent

SYNTHETIC_MARKERS = [
    "synthetic",
    "Synthetic",
    "SYNTHETIC",
    "fixture",
    "Fixture",
    "FIXTURE",
    "paper_hypothetical",
    "reference_project",
]


def _fake_quotes(symbols, timeout=8):
    quotes = {}
    for i, s in enumerate(symbols):
        quotes[s] = {
            "symbol": s, "name": s, "last": 100.0 + i,
            "prev_close": 99.0 + i, "change_pct": 1.0,
            "source": "Yahoo Finance",
        }
    return quotes, []


class TestNoSyntheticPayload(unittest.TestCase):
    def _payload(self):
        from hedge_desk import server
        with patch("hedge_desk.live_desk_data.fetch_market_snapshot", _fake_quotes):
            return server.build_live_console_payload()

    def test_report_is_not_synthetic_type(self):
        payload = self._payload()
        report = payload["report"]
        self.assertNotIn("paper_hypothetical", report["report_type"])
        self.assertNotIn("synthetic", report["report_type"].lower())
        self.assertFalse(report.get("synthetic_data", True))

    def test_no_synthetic_markers_in_payload_json(self):
        payload = self._payload()
        text = json.dumps(payload)
        for marker in SYNTHETIC_MARKERS:
            # "synthetic_data": false is the explicit opt-out flag, allowed.
            cleaned = text.replace('"synthetic_data": false', '')
            self.assertNotIn(marker, cleaned, f"synthetic marker in payload: {marker}")

    def test_projects_have_real_data_or_explicit_unavailable(self):
        payload = self._payload()
        for project in payload["report"]["projects"]:
            status = project["data_status"]
            self.assertIn(status, ("live", "batch", "data_unavailable"))
            if status == "data_unavailable":
                self.assertTrue(project["reason"], "unavailable desk must state a reason")
            else:
                self.assertTrue(project["live_data"], "live desk must carry real quotes")
                for symbol, quote in project["live_data"].items():
                    self.assertIn("source", quote)
                    self.assertIn("last", quote)

    def test_scenarios_labeled_hypothetical_from_real_base(self):
        payload = self._payload()
        scenarios = payload["report"]["scenarios"]
        self.assertTrue(scenarios, "scenario lab must have real-base scenarios")
        for scenario in scenarios:
            self.assertIn("hypothetical projection from real base data", scenario["label"])
            self.assertIn("base_price", scenario)
            self.assertIn("projected_price", scenario)
            self.assertNotIn("fixture", json.dumps(scenario).lower())

    def test_fail_closed_when_no_live_data(self):
        from hedge_desk import server
        from hedge_desk.live_desk_data import build_live_console_report
        with patch("hedge_desk.live_desk_data.fetch_market_snapshot", lambda s, timeout=8: ({}, [])):
            with self.assertRaises(RuntimeError):
                build_live_console_report("test-commit")


class TestNoSyntheticFrontend(unittest.TestCase):
    def test_no_report_json_fallback(self):
        app_js = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        self.assertNotIn("fetch('./report.json'", app_js)
        self.assertNotIn('fetch("./report.json"', app_js)

    def test_no_synthetic_copy(self):
        app_js = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        self.assertNotIn("synthetic research fixtures", app_js)
        self.assertNotIn("Synthetic inputs only", app_js)
        self.assertNotIn("SYNTHETIC RESEARCH", app_js)

    def test_build_web_writes_fail_closed_stub(self):
        import scripts.build_web as build_web
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            stub = build_web.export_report({}, Path(td))
            self.assertEqual(stub["status"], "data_unavailable")
            self.assertFalse(stub["synthetic_data"])
            on_disk = json.loads((Path(td) / "report.json").read_text(encoding="utf-8"))
            self.assertEqual(on_disk["status"], "data_unavailable")


if __name__ == "__main__":
    unittest.main()
