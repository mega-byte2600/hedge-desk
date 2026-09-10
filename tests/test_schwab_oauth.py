import json
import unittest
from urllib.parse import parse_qs, urlparse

from hedge_desk.brokers.schwab_oauth import SchwabOAuth, SchwabOAuthConfig
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
        return status, json.dumps(payload or {}).encode()

    return t


class SchwabOAuthTests(unittest.TestCase):
    def test_authorize_url_contains_readonly_scope_and_state(self):
        oauth = SchwabOAuth(CFG, transport=transport_ok())
        url = oauth.authorize_url("STATE123")
        parsed = urlparse(url)
        q = parse_qs(parsed.query)
        self.assertEqual(parsed.netloc, "api.schwabapi.com")
        self.assertEqual(q["client_id"][0], "cid")
        self.assertEqual(q["response_type"][0], "code")
        self.assertEqual(q["scope"][0], "readonly")
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
                {"access_token": "AT", "refresh_token": "RT", "expires_in": 1800, "token_type": "Bearer", "scope": "readonly"},
                capture=capture,
            ),
        )
        result = oauth.exchange_code("AUTHCODE")
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["access_token"], "AT")
        self.assertEqual(result["scope"], "readonly")
        # credentials go in the Authorization header, never the body
        self.assertIn("Authorization", capture[0]["headers"])
        self.assertNotIn(b"csecret", capture[0]["body"] or b"")

    def test_exchange_code_http_error_fails_closed(self):
        oauth = SchwabOAuth(CFG, transport=transport_ok({"error": "bad"}, status=400))
        self.assertEqual(oauth.exchange_code("x")["status"], "error")

    def test_exchange_code_missing_token_fails_closed(self):
        oauth = SchwabOAuth(CFG, transport=transport_ok({"nope": True}))
        self.assertEqual(oauth.exchange_code("x")["error"], "no_access_token")

    def test_exchange_code_requires_code(self):
        oauth = SchwabOAuth(CFG, transport=transport_ok())
        self.assertEqual(oauth.exchange_code("")["error"], "missing_code")

    def test_env_config(self):
        cfg = SchwabOAuthConfig.from_environment(
            {"SCHWAB_CLIENT_ID": "a", "SCHWAB_CLIENT_SECRET": "b", "SCHWAB_REDIRECT_URI": "c"}
        )
        self.assertTrue(cfg.configured)
        self.assertFalse(SchwabOAuthConfig.from_environment({}).configured)

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
            return 200, json.dumps([{k: row[k] for k in ("broker", "account_label", "updated_at")}]).encode()
        if method == "POST":
            row = json.loads(body)
            self.rows[row["email"]] = row
            return 201, b"[]"
        if method == "DELETE":
            email = (q.get("email") or ["eq."])[0][3:]
            self.rows.pop(email, None)
            return 204, b""
        return 404, b""


class SupabaseBrokerStoreTests(unittest.TestCase):
    def setUp(self):
        self.backend = FakeSupabase()
        self.store = SupabaseBrokerLinkStore("https://p.supabase.co", "svc", transport=self.backend)
        self.key = b"k"

    def test_link_and_connection(self):
        self.store.link("m@x.com", "MEMBER", "schwab", "tok", account_label="Main", key=self.key)
        conn = self.store.connection("m@x.com")
        self.assertTrue(conn["linked"])
        self.assertEqual(conn["broker"], "schwab")
        self.assertEqual(conn["account_label"], "Main")
        self.assertNotIn("token", conn)

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
