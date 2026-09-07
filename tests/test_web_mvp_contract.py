import hashlib
import json
import unittest
from pathlib import Path

from hedge_desk.candidates import build_candidate_feed
from hedge_desk.server import application


GOLDEN_CANDIDATE_FEED_BLOB_SHA = "5a81ad4ee99822a1c7370e78a8eb34d01d7ac3d3"


class WebMvpContractTests(unittest.TestCase):
    def _call(self, path):
        captured = {}

        def start_response(status, headers):
            captured["status"] = status
            captured["headers"] = dict(headers)

        body = b"".join(application({"PATH_INFO": path}, start_response))
        return captured["status"], captured["headers"], body

    def _golden_path(self):
        return Path(__file__).parent / "golden" / "candidate_feed.json"

    def _golden_payload(self):
        return json.loads(self._golden_path().read_text())

    def test_golden_master_fixture_is_content_locked(self):
        raw = self._golden_path().read_bytes()
        git_blob = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
        self.assertEqual(
            git_blob,
            GOLDEN_CANDIDATE_FEED_BLOB_SHA,
            "Golden Master drift detected. Treat baseline changes as an explicit regression-baseline update.",
        )

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
        self.assertEqual(payload["display_name"], "mbolton")
        self.assertEqual(payload["linkedin_url"], "https://www.linkedin.com/in/bolton-2600/")

    def test_candidate_feed_matches_golden_master(self):
        self.assertEqual(build_candidate_feed(), self._golden_payload())

    def test_black_box_candidate_api_matches_golden_master(self):
        status, headers, body = self._call("/api/candidates")
        self.assertEqual(status, "200 OK")
        self.assertEqual(headers["Content-Type"], "application/json")
        self.assertEqual(json.loads(body), self._golden_payload())

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
