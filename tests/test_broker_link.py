import os
import hashlib
import hmac
import tempfile
import unittest
from unittest.mock import patch

from hedge_desk.broker_link import (
    BrokerLinkStore,
    BrokerAdapter,
    _decrypt_token,
    _encrypt_token,
    build_broker_gate,
)
from hedge_desk.membership import MembershipStore, Clock


class BrokerLinkStoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.db = os.path.join(self.tmp, "broker.db")
        self.store = BrokerLinkStore(self.db)
        self.key = b"t" * 32

    def tearDown(self):
        self.store.close()

    def test_link_and_connection_roundtrip(self):
        result = self.store.link(
            "member@example.com", "MEMBER", "schwab", "secret-token",
            account_label="My Schwab", key=self.key,
        )
        self.assertTrue(result["linked"])
        conn = self.store.connection("member@example.com")
        self.assertTrue(conn["linked"])
        self.assertEqual(conn["broker"], "schwab")
        self.assertEqual(conn["account_label"], "My Schwab")
        # raw token must never be returned by connection()
        self.assertNotIn("token", conn)
        creds = self.store.token_state("member@example.com", self.key)
        self.assertEqual(creds["access_token"], "secret-token")

    def test_existing_fernet_bundle_migrates_without_losing_tokens(self):
        import base64, json
        from cryptography.fernet import Fernet
        payload = {"access_token": "old-access", "refresh_token": "old-refresh", "expires_at": "2026-10-04T00:00:00+00:00", "account_hash": "HASH", "account_number": "1234"}
        cipher = Fernet(base64.urlsafe_b64encode(hashlib.sha256(self.key).digest()))
        blob = "fernet:" + cipher.encrypt(json.dumps(payload).encode()).decode()
        self.store._conn.execute("INSERT INTO broker_links VALUES (?, ?, ?, ?, ?, ?)", ("m@example.com", "schwab", "Main", blob, "now", "now"))
        self.store._conn.commit()
        state = self.store.token_state("m@example.com", self.key)
        self.assertEqual(state["refresh_token"], "old-refresh")
        self.assertEqual(state["selected_account_hash"], "HASH")
        self.assertEqual(state["refresh_token_issued_at"], "")
        raw = self.store._conn.execute("SELECT token_enc FROM broker_links WHERE email=?", ("m@example.com",)).fetchone()[0]
        self.assertTrue(raw.startswith("v1."))
        self.assertNotIn("old-refresh", raw)

    def test_tokens_and_sensitive_metadata_are_authenticated_encrypted(self):
        self.store.link(
            "member@example.com", "MEMBER", "schwab", "access-secret",
            account_label="My Schwab", key=self.key, refresh_token="refresh-secret",
            access_expires_at="2026-01-01T00:30:00+00:00",
            refresh_token_issued_at="2026-01-01T00:00:00+00:00",
            scope="readonly", selected_account_hash="account-hash-secret",
        )
        encrypted = self.store._conn.execute(
            "SELECT token_enc FROM broker_links WHERE email=?", ("member@example.com",)
        ).fetchone()[0]
        self.assertNotIn("access-secret", encrypted)
        self.assertNotIn("refresh-secret", encrypted)
        self.assertNotIn("account-hash-secret", encrypted)
        self.assertEqual(self.store.token_state("member@example.com", self.key)["refresh_token"], "refresh-secret")
        self.assertEqual(self.store.token_state("member@example.com", self.key)["selected_account_hash"], "account-hash-secret")
        self.assertNotIn("access-secret", str(self.store.connection("member@example.com")))

    def test_ciphertext_tamper_and_wrong_key_fail_closed(self):
        blob = _encrypt_token("secret", self.key)
        self.assertEqual(_decrypt_token(blob, self.key), "secret")
        changed = blob[:4] + ("A" if blob[4] != "A" else "B") + blob[5:]
        self.assertIsNone(_decrypt_token(changed, self.key))
        self.assertIsNone(_decrypt_token(blob, b"w" * 32))
        contextual_blob = _encrypt_token("scoped", self.key, "member@example.com")
        self.assertEqual(_decrypt_token(contextual_blob, self.key, "member@example.com"), "scoped")
        self.assertIsNone(_decrypt_token(contextual_blob, self.key, "other@example.com"))
        with self.assertRaisesRegex(ValueError, "32 bytes"):
            _encrypt_token("secret", b"short")

    def test_legacy_token_is_reencrypted_before_being_returned(self):
        legacy = "legacy-access-token"
        nonce = "old-nonce"
        tag = hmac.new(self.key, (nonce + legacy).encode(), hashlib.sha256).hexdigest()
        blob = f"{nonce}:{tag}:{legacy}"
        self.store._conn.execute(
            "INSERT INTO broker_links (email, broker, account_label, token_enc, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            ("member@example.com", "schwab", "Old", blob, "now", "now"),
        )
        self.store._conn.commit()
        state = self.store.token_state("member@example.com", self.key)
        stored = self.store._conn.execute(
            "SELECT token_enc FROM broker_links WHERE email=?", ("member@example.com",)
        ).fetchone()[0]
        self.assertEqual(state["access_token"], legacy)
        self.assertTrue(stored.startswith("v1."))
        self.assertNotIn(legacy, stored)

    def test_guest_cannot_link_broker(self):
        with self.assertRaises(PermissionError):
            self.store.link("guest@example.com", "GUEST", "schwab", "t", key=self.key)

    def test_unknown_role_cannot_link(self):
        with self.assertRaises(PermissionError):
            self.store.link("x@example.com", "HACKER", "schwab", "t", key=self.key)

    def test_refuses_to_store_token_without_key(self):
        # In production, BROKER_LINK_KEY must be set; otherwise fail closed.
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                self.store.link("member@example.com", "MEMBER", "schwab", "t", key=None)

    def test_unlink_removes_connection(self):
        self.store.link("m@example.com", "MEMBER", "schwab", "t", key=self.key)
        self.assertTrue(self.store.connection("m@example.com")["linked"])
        self.store.unlink("m@example.com")
        self.assertFalse(self.store.connection("m@example.com")["linked"])

    def test_no_connection_is_fail_closed(self):
        conn = self.store.connection("nobody@example.com")
        self.assertFalse(conn["linked"])


class BrokerGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.store = BrokerLinkStore(os.path.join(self.tmp, "g.db"))
        self.gate = build_broker_gate(self.store, BrokerAdapter("schwab"))
        self.key = b"k" * 32

    def tearDown(self):
        self.store.close()

    def test_guest_denied_broker_access(self):
        result = self.gate("guest@example.com", "GUEST")
        self.assertFalse(result["allowed"])
        self.assertEqual(result["error"], "broker_link_requires_member")

    def test_member_without_link_gets_no_broker(self):
        result = self.gate("member@example.com", "MEMBER")
        self.assertFalse(result["allowed"])
        self.assertEqual(result["error"], "no_broker_linked")

    def test_linked_member_gets_read_only_broker(self):
        self.store.link("member@example.com", "MEMBER", "schwab", "t", key=self.key)
        result = self.gate("member@example.com", "MEMBER")
        self.assertTrue(result["allowed"])
        self.assertTrue(result["read_only"])
        self.assertEqual(result["broker"], "schwab")
        self.assertEqual(result["positions"]["status"], "not_implemented")


if __name__ == "__main__":
    unittest.main()
