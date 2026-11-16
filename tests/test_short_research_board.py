import json
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

from hedge_desk.short_research_board import build_short_research_board
from hedge_desk.sec_filings_service import _extract_filings


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
            with patch("hedge_desk.sec_filings_service.get_sec_filings", return_value={"status":"CACHED","source":"SEC EDGAR submissions","symbols":{"ABC":{"status":"CIK_UNMAPPED","filings":[]}}}), patch("hedge_desk.short_interest_service.get_short_interest", return_value={"status":"UNCONFIGURED","source":"FINRA Consolidated Short Interest","interpretation":"snapshot only","symbols":{"ABC":{"status":"UNCONFIGURED"}}}):
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
        self.assertEqual(row["sec_filing_status"], "CIK_UNMAPPED")
        self.assertEqual(row["sec_filings"], [])
        self.assertEqual(row["borrow_status"], "BROKER_CONFIRMATION_REQUIRED")
        self.assertEqual(row["short_interest_status"], "UNCONFIGURED")
        self.assertFalse(row["trade_authorized"])

    def test_failed_eod_source_does_not_publish_price_context(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "report.json"
            report.write_text(json.dumps({
                "watchlist": ["ABC"],
                "series": {"as_of": "2026-01-22", "symbols": {"ABC": [["2026-01-22", "10"]]}},
                "eod_source_results": [{"symbol": "ABC", "status": "BLOCKED"}],
            }), encoding="utf-8")
            with patch("hedge_desk.sec_filings_service.get_sec_filings", return_value={"status":"CACHED","source":"SEC EDGAR submissions","symbols":{"ABC":{"status":"CIK_UNMAPPED","filings":[]}}}), patch("hedge_desk.short_interest_service.get_short_interest", return_value={"status":"UNCONFIGURED","source":"FINRA Consolidated Short Interest","interpretation":"snapshot only","symbols":{"ABC":{"status":"UNCONFIGURED"}}}):
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
            with patch("hedge_desk.sec_filings_service.get_sec_filings", return_value={"status":"REFRESHING","source":"SEC EDGAR submissions","symbols":{symbol:{"status":"LOADING","filings":[]} for symbol in ["NKE","CCL","AAL","LYFT","NCLH","F","DVN"]}}), patch("hedge_desk.short_interest_service.get_short_interest", return_value={"status":"UNCONFIGURED","source":"FINRA Consolidated Short Interest","interpretation":"snapshot only","symbols":{symbol:{"status":"UNCONFIGURED"} for symbol in ["NKE","CCL","AAL","LYFT","NCLH","F","DVN"]}}):
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
        self.assertTrue(all(x["sec_filing_status"] in {"LOADING", "BLOCKED", "LIVE", "LIVE_NO_RECENT_FORMS"} for x in board["symbols"]))
        self.assertFalse(board["trade_authorized"])

    def test_burry_sensitivity_api_is_post_only_and_decimal_backed(self):
        from io import BytesIO
        from hedge_desk import server
        captured = {}
        def start_response(status, headers):
            captured["status"] = status
        inputs = {"asset_cost_millions":"17000", "reported_life_years":"6", "scenario_life_years":"3", "service_fraction_pct":"100", "tax_rate_pct":"0", "reported_net_income_millions":"88100", "diluted_shares_millions":"6240", "share_price":"480"}
        body = json.dumps(inputs).encode()
        result = b"".join(server.application({"PATH_INFO":"/api/burry-sensitivity", "REQUEST_METHOD":"POST", "CONTENT_LENGTH":str(len(body)), "wsgi.input":BytesIO(body)}, start_response))
        self.assertEqual(captured["status"], "200 OK")
        self.assertEqual(json.loads(result)["additional_annual_depreciation_millions"], "2833.33")

    def test_sec_filings_are_read_from_submissions_and_link_to_primary_document(self):
        payload = {
            "name": "Microsoft Corporation",
            "filings": {"recent": {
                "form": ["10-K", "4"],
                "filingDate": ["2026-07-30", "2026-08-01"],
                "reportDate": ["2026-06-30", ""],
                "accessionNumber": ["0000789019-26-000123", "0000789019-26-000124"],
                "primaryDocument": ["msft-20260630.htm", "x.xml"],
                "items": ["2.02, 5.02", ""],
            }},
        }
        result = _extract_filings("MSFT", payload)
        self.assertEqual(result["status"], "LIVE")
        self.assertEqual(result["company_name"], "Microsoft Corporation")
        self.assertEqual(result["filings"][0]["form"], "10-K")
        self.assertEqual(result["filings"][0]["filing_date"], "2026-07-30")
        self.assertEqual(result["filings"][0]["items"], "2.02, 5.02")
        self.assertEqual(result["filings"][0]["catalyst_evidence"], "DATED_REGULATORY_FILING")
        self.assertEqual(result["filings"][0]["url"], "https://www.sec.gov/Archives/edgar/data/789019/000078901926000123/msft-20260630.htm")

    def test_eight_k_item_is_preserved_as_a_dated_lead_not_a_thesis(self):
        payload = {"name": "Microsoft Corporation", "filings": {"recent": {
            "form": ["8-K"], "filingDate": ["2026-11-13"],
            "reportDate": ["2026-11-12"],
            "accessionNumber": ["0000789019-26-000999"],
            "primaryDocument": ["msft-20261113.htm"],
            "items": ["2.02, 7.01"],
        }}}
        result = _extract_filings("MSFT", payload)
        filing = result["filings"][0]
        self.assertEqual(filing["items"], "2.02, 7.01")
        self.assertEqual(filing["catalyst_evidence"], "SEC_FILING_EVENT_LEAD")


if __name__ == "__main__":
    unittest.main()
