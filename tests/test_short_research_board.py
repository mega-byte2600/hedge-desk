import json
import tempfile
import unittest
from pathlib import Path

from hedge_desk.short_research_board import build_short_research_board


class ShortResearchBoardTests(unittest.TestCase):
    def test_uses_real_watchlist_closes_and_does_not_invent_short_cases(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "report.json"
            prices = [[f"2026-01-{day:02d}", str(100 + day)] for day in range(1, 23)]
            report.write_text(json.dumps({
                "generated_at": "2026-01-23T00:00:00+00:00",
                "watchlist": ["ABC"],
                "series": {"as_of": "2026-01-22", "symbols": {"ABC": prices}},
                "eod_source_results": [{"symbol": "ABC", "status": "PASS"}],
            }), encoding="utf-8")
            board = build_short_research_board(report)

        self.assertEqual(board["status"], "LIVE")
        self.assertEqual(len(board["symbols"]), 1)
        row = board["symbols"][0]
        self.assertEqual(row["symbol"], "ABC")
        self.assertEqual(row["last_close"], 122.0)
        self.assertAlmostEqual(row["return_5_sessions_pct"], (122 / 117 - 1) * 100)
        self.assertAlmostEqual(row["return_20_sessions_pct"], (122 / 102 - 1) * 100)
        self.assertEqual(row["case_status"], "NO_SHORT_THESIS")
        self.assertEqual(row["price_context"], "BOTH_LOOKBACKS_POSITIVE")
        self.assertEqual(row["sec_filing_status"], "NOT_RESEARCHED")
        self.assertEqual(row["borrow_status"], "NOT_CHECKED")
        self.assertFalse(row["trade_authorized"])

    def test_failed_eod_source_does_not_publish_price_context(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "report.json"
            report.write_text(json.dumps({
                "watchlist": ["ABC"],
                "series": {"as_of": "2026-01-22", "symbols": {"ABC": [["2026-01-22", "10"]]}},
                "eod_source_results": [{"symbol": "ABC", "status": "BLOCKED"}],
            }), encoding="utf-8")
            row = build_short_research_board(report)["symbols"][0]
        self.assertEqual(row["status"], "PRICE_DATA_UNAVAILABLE")
        self.assertEqual(row["price_context"], "INSUFFICIENT_DATA")
        self.assertIsNone(row["last_close"])
        self.assertIsNone(row["return_5_sessions_pct"])

    def test_missing_report_fails_closed(self):
        board = build_short_research_board(Path("/definitely/missing/report.json"))
        self.assertEqual(board["status"], "DATA_UNAVAILABLE")
        self.assertEqual(board["symbols"], [])
        self.assertFalse(board["trade_authorized"])

    def test_api_serves_the_watchlist_research_board(self):
        from hedge_desk import server

        captured = {}
        def start_response(status, headers):
            captured["status"] = status
            captured["headers"] = dict(headers)
        server._api_cache.pop("short-research-board", None)
        try:
            payload = b"".join(server.application(
                {"PATH_INFO": "/api/short-research", "REQUEST_METHOD": "GET"},
                start_response,
            ))
        finally:
            server._api_cache.pop("short-research-board", None)
        board = json.loads(payload)
        self.assertEqual(captured["status"], "200 OK")
        self.assertEqual(captured["headers"]["Cache-Control"], "no-store")
        self.assertEqual(board["schema_version"], "hedge-desk-short-research-board-1.0.0")
        self.assertEqual(len(board["symbols"]), 7)
        self.assertEqual(board["as_of"], "2026-11-13")
        weak = [x["symbol"] for x in board["symbols"] if x["price_context"] == "BOTH_LOOKBACKS_NEGATIVE"]
        self.assertEqual(weak, ["LYFT", "F"])
        self.assertTrue(all(x["case_status"] == "NO_SHORT_THESIS" for x in board["symbols"]))
        self.assertTrue(all(x["sec_filing_status"] == "NOT_RESEARCHED" for x in board["symbols"]))
        self.assertFalse(board["trade_authorized"])


if __name__ == "__main__":
    unittest.main()
