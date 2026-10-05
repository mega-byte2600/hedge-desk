import json
import unittest
from unittest.mock import patch

from hedge_desk.market_context_storage import (
    load_latest_market_context,
    persist_latest_market_context,
)


class MarketContextStorageTests(unittest.TestCase):
    def setUp(self):
        self.snapshot = {
            "schema_version": "hedge-desk-market-context-1.0.0",
            "status": "LIVE",
            "live_sources": 2,
            "blocked_sources": 0,
            "unconfigured_sources": 1,
            "generated_at": "2026-10-05T12:00:00+00:00",
            "trade_authorized": False,
            "sources": {},
        }

    def test_storage_is_explicitly_unconfigured_without_server_key(self):
        result = persist_latest_market_context(self.snapshot, env={})
        self.assertEqual(result["status"], "UNCONFIGURED")
        self.assertEqual(
            result["reason_code"], "SERVER_STORAGE_CREDENTIALS_MISSING"
        )

    def test_persist_uses_server_key_and_upserts_only_latest_public_snapshot(self):
        captured = {}

        def transport(request):
            captured["url"] = request.full_url
            captured["method"] = request.get_method()
            captured["headers"] = request.headers
            captured["body"] = json.loads(request.data)
            return 204

        result = persist_latest_market_context(
            self.snapshot,
            env={
                "SUPABASE_URL": "https://project.supabase.co",
                "SUPABASE_SECRET_KEY": "test-secret",
            },
            transport=transport,
        )

        self.assertEqual(result["status"], "PERSISTED")
        self.assertEqual(captured["method"], "POST")
        self.assertIn("on_conflict=snapshot_key", captured["url"])
        self.assertEqual(captured["headers"]["Prefer"], "resolution=merge-duplicates,return=minimal")
        self.assertEqual(captured["body"]["snapshot_key"], "latest")
        self.assertFalse(captured["body"]["payload"]["trade_authorized"])
        self.assertNotIn("test-secret", json.dumps(result))

    def test_load_accepts_only_a_single_object_payload(self):
        payload = {"status": "DEGRADED", "trade_authorized": False}

        def transport(request):
            self.assertEqual(request.get_method(), "GET")
            return [{"payload": payload}]

        result = load_latest_market_context(
            env={
                "SUPABASE_URL": "https://project.supabase.co",
                "SUPABASE_SERVICE_ROLE_KEY": "test-secret",
            },
            transport=transport,
        )

        self.assertEqual(result, payload)


if __name__ == "__main__":
    unittest.main()
