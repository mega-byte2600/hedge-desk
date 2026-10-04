import json
import unittest
from urllib.parse import parse_qs, urlparse

from hedge_desk.brokers.schwab_oauth import (
    SchwabOAuth,
    SchwabOAuthConfig,
)
from hedge_desk.broker_link import BrokerLinkStore, SupabaseBrokerLinkStore


CFG = SchwabOAuthConfig(
    client_id="cid",
    client_secret="csecret",
    redirect_uri="https://hedge-desk.onrender.com/api/broker/callback",
)


def transport_ok(payload=None, status=200, capture=None):
    def t(method, url, headers, body):
        if capture is not None:
            capture.append({"method": method, "url": url, "headers": headers, "body": body})
        return status, json.dumps(payload if payload is not None else {}).encode()

    return t


class SchwabOAuthTests(unittest.TestCase):
    def test_authorize_url_uses_approved_app_product_and_state_without_guessing_scope(self):
        oauth = SchwabOAuth(CFG, transport=transport_ok())
        url = oauth.authorize_url("STATE123")
        parsed = urlparse(url)
        q = parse_qs(parsed.query)
        self.assertEqual(parsed.netloc, "api.schwabapi.com")
        self.assertEqual(q["client_id"][0], "cid")
        self.assertEqual(q["response_type"][0], "code")
        self.assertNotIn("scope", q)
        self.assertEqual(q["state"][0], "STATE123")

    def test_not_configured_raises_on_authorize(self):
        oauth = SchwabOAuth(SchwabOAuthConfig("", "", ""), transport=transport_ok())
        with self.assertRaises(ValueError):
            oauth.authorize_url("s")

    def test_exchange_code_success(self):
        capture = []
        oauth = SchwabOAuth(
            CFG,
            transport=transport_ok(
                {"access_token": "AT", "refresh_token": "RT", "expires_in": 1800, "token_type": "Bearer", "scope": "api"},
                capture=capture,
            ),
        )
        result = oauth.exchange_code("AUTHCODE")
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["access_token"], "AT")
        self.assertEqual(result["scope"], "api")
        # credentials go in the Authorization header, never the body
        self.assertIn("Authorization", capture[0]["headers"])
        self.assertNotIn(b"csecret", capture[0]["body"] or b"")

    def test_exchange_code_http_error_fails_closed(self):
        oauth = SchwabOAuth(CFG, transport=transport_ok({"error": "bad"}, status=400))
        self.assertEqual(oauth.exchange_code("x")["status"], "error")

    def test_exchange_code_missing_token_fails_closed(self):
        oauth = SchwabOAuth(CFG, transport=transport_ok({"nope": True}))
        self.assertEqual(oauth.exchange_code("x")["error"], "no_access_token")

    def test_exchange_rejects_malformed_schema_and_expiry(self):
        for payload, error in (([], "unexpected_response_schema"), ({"access_token": "AT"}, "invalid_expiry")):
            with self.subTest(payload=payload):
                oauth = SchwabOAuth(CFG, transport=transport_ok(payload))
                self.assertEqual(oauth.exchange_code("x")["error"], error)

    def test_refresh_access_token_posts_refresh_grant(self):
        capture = []
        oauth = SchwabOAuth(
            CFG,
            transport=transport_ok(
                {"access_token": "AT2", "refresh_token": "RT2", "expires_in": 1800, "scope": "api"},
                capture=capture,
            ),
        )
        result = oauth.refresh_access_token("RT1")
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["access_token"], "AT2")
        self.assertIn(b"grant_type=refresh_token", capture[0]["body"])
        self.assertIn(b"refresh_token=RT1", capture[0]["body"])
        self.assertNotIn("RT1", capture[0]["url"])

    def test_refresh_reauthentication_and_transport_fail_closed(self):
        expired = SchwabOAuth(CFG, transport=transport_ok({"error": "invalid_grant"}, status=401))
        self.assertEqual(expired.refresh_access_token("RT")["error"], "reauthentication_required")

        def transport_failure(*_args):
            raise RuntimeError("sensitive token content must not escape")

        failed = SchwabOAuth(CFG, transport=transport_failure)
        result = failed.refresh_access_token("RT")
        self.assertEqual(result["error"], "transport_failure")
        self.assertNotIn("sensitive", str(result))

    def test_exchange_code_requires_code(self):
        oauth = SchwabOAuth(CFG, transport=transport_ok())
        self.assertEqual(oauth.exchange_code("")["error"], "missing_code")

    def test_env_config(self):
        cfg = SchwabOAuthConfig.from_environment(
            {
                "SCHWAB_CLIENT_ID": "a",
                "SCHWAB_CLIENT_SECRET": "b",
                "SCHWAB_REDIRECT_URI": "https://example.com/oauth/callback",
            }
        )
        self.assertTrue(cfg.configured)
        self.assertFalse(SchwabOAuthConfig.from_environment({}).configured)

    def test_insecure_redirect_or_endpoint_disables_oauth(self):
        for cfg in (
            SchwabOAuthConfig("cid", "secret", "http://example.com/callback"),
            SchwabOAuthConfig("cid", "secret", "https://example.com/callback", token_url="http://example.com/token"),
            SchwabOAuthConfig("cid", "secret", "https://example.com/callback", token_url="https://evil.example/v1/oauth/token"),
        ):
            with self.subTest(cfg=cfg):
                self.assertFalse(cfg.configured)

    def test_module_has_no_order_paths(self):
        from pathlib import Path

        text = (
            Path(__file__).resolve().parents[1] / "hedge_desk" / "brokers" / "schwab_oauth.py"
        ).read_text(encoding="utf-8").lower()
        for forbidden in ("submit_order", "place_order", "placeorder", "cancel_order", "replace_order"):
            self.assertNotIn(forbidden, text)


class FakeSupabase:
    def __init__(self):
        self.rows = {}

    def __call__(self, method, url, headers, body):
        parsed = urlparse(url)
        q = parse_qs(parsed.query)
        if method == "GET":
            email = (q.get("email") or ["eq."])[0][3:]
            row = self.rows.get(email)
            if not row:
                return 200, b"[]"
            fields = (q.get("select") or ["broker,account_label,updated_at"])[0].split(",")
            return 200, json.dumps([{k: row[k] for k in fields if k in row}]).encode()
        if method == "POST":
            row = json.loads(body)
            self.rows[row["email"]] = row
            return 201, b"[]"
        if method == "PATCH":
            email = (q.get("email") or ["eq."])[0][3:]
            if email in self.rows:
                self.rows[email].update(json.loads(body))
            return 204, b""
        if method == "DELETE":
            email = (q.get("email") or ["eq."])[0][3:]
            self.rows.pop(email, None)
            return 204, b""
        return 404, b""


class SupabaseBrokerStoreTests(unittest.TestCase):
    def setUp(self):
        self.backend = FakeSupabase()
        self.store = SupabaseBrokerLinkStore("https://p.supabase.co", "svc", transport=self.backend)
        self.key = b"k" * 32

    def test_link_and_connection(self):
        self.store.link(
            "m@x.com", "MEMBER", "schwab", "tok", account_label="Main", key=self.key,
            refresh_token="refresh", access_expires_at="2026-01-01T00:30:00+00:00",
            refresh_token_issued_at="2026-01-01T00:00:00+00:00", scope="readonly",
            selected_account_hash="hash-secret",
        )
        conn = self.store.connection("m@x.com")
        self.assertTrue(conn["linked"])
        self.assertEqual(conn["broker"], "schwab")
        self.assertEqual(conn["account_label"], "Main")
        self.assertNotIn("token", conn)
        self.assertEqual(self.store.token_state("m@x.com", self.key)["selected_account_hash"], "hash-secret")

    def test_refreshed_token_is_persisted_encrypted_before_return(self):
        from datetime import datetime, timezone
        from hedge_desk.brokers.schwab_tokens import SchwabTokenState

        self.store.link(
            "m@x.com", "MEMBER", "schwab", "old-access", key=self.key,
            refresh_token="old-refresh", access_expires_at="2026-01-01T00:30:00+00:00",
            refresh_token_issued_at="2026-01-01T00:00:00+00:00", scope="readonly",
        )
        state = SchwabTokenState(
            "new-access", "new-refresh", datetime(2026, 1, 1, 1, tzinfo=timezone.utc),
            datetime(2026, 1, 1, tzinfo=timezone.utc), "readonly",
            datetime(2026, 1, 1, tzinfo=timezone.utc), "hash-secret",
        )
        self.store.persist_schwab_tokens("m@x.com", state, self.key)
        stored = self.backend.rows["m@x.com"]["token_enc"]
        self.assertNotIn("new-access", stored)
        self.assertEqual(self.store.token_state("m@x.com", self.key)["access_token"], "new-access")
        self.assertEqual(self.store.token_state("m@x.com", self.key)["selected_account_hash"], "hash-secret")

    def test_guest_cannot_link(self):
        with self.assertRaises(PermissionError):
            self.store.link("g@x.com", "GUEST", "schwab", "t", key=self.key)

    def test_unlink(self):
        self.store.link("m@x.com", "MEMBER", "schwab", "t", key=self.key)
        self.store.unlink("m@x.com")
        self.assertFalse(self.store.connection("m@x.com")["linked"])

    def test_requires_key(self):
        import os
        from unittest.mock import patch

        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                self.store.link("m@x.com", "MEMBER", "schwab", "t", key=None)

    def test_requires_credentials(self):
        with self.assertRaises(ValueError):
            SupabaseBrokerLinkStore("", "", transport=self.backend)


class DefaultBrokerStoreSelectionTests(unittest.TestCase):
    def test_supabase_when_configured(self):
        import os
        from unittest.mock import patch
        from hedge_desk.broker_link import default_broker_store

        with patch.dict(os.environ, {"SUPABASE_URL": "https://p.supabase.co", "SUPABASE_SERVICE_KEY": "k"}, clear=False):
            self.assertIsInstance(default_broker_store(), SupabaseBrokerLinkStore)

    def test_sqlite_fallback(self):
        import os, tempfile
        from unittest.mock import patch
        from hedge_desk.broker_link import default_broker_store

        tmp = tempfile.mkdtemp()
        env = {k: v for k, v in os.environ.items()
               if k not in ("SUPABASE_URL", "SUPABASE_SERVICE_KEY", "SUPABASE_SERVICE_ROLE_KEY")}
        env["BROKER_DB"] = os.path.join(tmp, "b.db")
        with patch.dict(os.environ, env, clear=True):
            self.assertIsInstance(default_broker_store(), BrokerLinkStore)


if __name__ == "__main__":
    unittest.main()
