import json
import unittest
from pathlib import Path

from hedge_desk.candidates import build_candidate_feed
from hedge_desk.server import application


class WebMvpContractTests(unittest.TestCase):
    def _call(self, path):
        captured = {}

        def start_response(status, headers):
            captured["status"] = status
            captured["headers"] = dict(headers)

        body = b"".join(application({"PATH_INFO": path}, start_response))
        return captured["status"], captured["headers"], body

    def test_health_contract_is_paper_only(self):
        status, headers, body = self._call("/api/health")
        payload = json.loads(body)
        self.assertEqual(status, "200 OK")
        self.assertEqual(headers["Content-Type"], "application/json")
        self.assertEqual(payload["service"], "hedge-desk-web")
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["mode"], "paper")
        self.assertIs(payload["live_orders_enabled"], False)
        self.assertIn("supabase", payload)
        self.assertEqual(set(payload["supabase"]), {"configured", "reachable"})

    def test_about_contract(self):
        status, _, body = self._call("/api/about")
        payload = json.loads(body)
        self.assertEqual(status, "200 OK")
        self.assertEqual(payload["display_name"], "Bolton")
        self.assertEqual(payload["linkedin_url"], "https://www.linkedin.com/in/bolton-2600/")

    def test_candidate_feed_matches_golden_master(self):
        golden = json.loads((Path(__file__).parent / "golden" / "candidate_feed.json").read_text())
        self.assertEqual(build_candidate_feed(), golden)

    def test_candidate_contract_has_six_desks_and_tickers(self):
        payload = build_candidate_feed()
        desks = {row["desk_id"] for row in payload["candidates"]}
        symbols = {row["symbol"] for row in payload["candidates"]}
        self.assertEqual(len(desks), 6)
        self.assertTrue({"SPY", "QQQ", "AAPL", "NVDA", "SPX", "XSP", "KO", "JNJ", "CL", "NG", "ZW"}.issubset(symbols))
        self.assertTrue(all(row["trade_authorized"] is False for row in payload["candidates"]))
        self.assertEqual(payload["candidate_definition"], "SEED_UNIVERSE_NOT_METHOD_QUALIFIED")


if __name__ == "__main__":
    unittest.main()
