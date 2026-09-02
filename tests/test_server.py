import json
import threading
import unittest
import urllib.error
import urllib.request

from hedge_desk.server import build_server


class ServerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.server, _ = build_server("127.0.0.1", 0)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base = "http://127.0.0.1:" + str(self.server.server_port)

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)

    def get(self, path):
        with urllib.request.urlopen(self.base + path) as response:
            return response.status, json.loads(response.read())

    def test_status_is_paper_only_and_yellow_sheet_gated(self) -> None:
        status, payload = self.get("/api/status")
        self.assertEqual(status, 200)
        self.assertEqual(payload["mode"], "PAPER_ONLY")
        self.assertTrue(payload["orders_blocked"])
        self.assertTrue(payload["yellow_sheet_required"])

    def test_research_endpoints_are_explicit_no_trade(self) -> None:
        for path in ("/api/dividends", "/api/earnings"):
            _, payload = self.get(path)
            self.assertEqual(payload["disposition"], "NO_TRADE")

    def test_every_post_is_rejected(self) -> None:
        request = urllib.request.Request(
            self.base + "/api/schwab/orders", data=b"{}", method="POST"
        )
        with self.assertRaises(urllib.error.HTTPError) as caught:
            urllib.request.urlopen(request)
        self.assertEqual(caught.exception.code, 405)
        payload = json.loads(caught.exception.read())
        self.assertTrue(payload["orders_blocked"])


if __name__ == "__main__":
    unittest.main()
