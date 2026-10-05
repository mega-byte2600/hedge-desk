import json
import unittest
from unittest.mock import patch

from hedge_desk.server import _api_cache, application


class MarketContextApiTests(unittest.TestCase):
    def request(self, path):
        captured = {}

        def start_response(status, headers):
            captured["status"] = status
            captured["headers"] = dict(headers)

        body = b"".join(
            application({"PATH_INFO": path, "REQUEST_METHOD": "GET"}, start_response)
        )
        return captured["status"], json.loads(body)

    def test_public_context_route_is_paper_only(self):
        expected = {
            "schema_version": "hedge-desk-market-context-1.0.0",
            "status": "DEGRADED",
            "live_sources": 1,
            "blocked_sources": 1,
            "unconfigured_sources": 0,
            "sources": {"fred": {"provider_id": "fred", "status": "LIVE"}},
            "storage": {"status": "PERSISTED"},
            "trade_authorized": False,
        }
        _api_cache.pop("market-context", None)
        try:
            with patch(
                "hedge_desk.server.build_market_context_payload",
                return_value=expected,
            ) as build:
                status, payload = self.request("/api/market-context")
                self.assertEqual(status, "200 OK")
                self.assertEqual(payload, expected)
                self.assertFalse(payload["trade_authorized"])
                build.assert_called_once()
        finally:
            _api_cache.pop("market-context", None)

    def test_failed_context_returns_a_safe_blocked_status(self):
        _api_cache.pop("market-context", None)
        try:
            with patch(
                "hedge_desk.server.build_market_context_payload",
                side_effect=RuntimeError("upstream failed"),
            ):
                status, payload = self.request("/api/market-context")
            self.assertEqual(status, "503 Service Unavailable")
            self.assertEqual(payload["status"], "BLOCKED")
            self.assertEqual(payload["reason_code"], "MARKET_CONTEXT_UNAVAILABLE")
            self.assertFalse(payload["trade_authorized"])
        finally:
            _api_cache.pop("market-context", None)


if __name__ == "__main__":
    unittest.main()
