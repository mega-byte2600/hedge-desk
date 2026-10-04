import os
import tempfile
import unittest
from unittest.mock import patch

from hedge_desk.broker_link import BrokerLinkStore, BrokerAdapter, build_broker_gate
from hedge_desk.membership import MembershipStore, Clock


class BrokerLinkStoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.db = os.path.join(self.tmp, "broker.db")
        self.store = BrokerLinkStore(self.db)
        self.key = b"test-broker-key"

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
        creds = self.store.credentials("member@example.com", key=self.key)
        self.assertEqual(creds["status"], "ok")
        self.assertEqual(creds["access_token"], "secret-token")

    def test_refresh_and_account_metadata_roundtrip_encrypted(self):
        self.store.link(
            "m@example.com", "MEMBER", "schwab", "secret-access-token-value-2600",
            account_label="Main", key=self.key,
            refresh_token="secret-refresh-token-value-2600",
            expires_at="2026-10-04T00:00:00+00:00", account_hash="HASH", account_number="1234",
        )
        creds = self.store.credentials("m@example.com", key=self.key)
        self.assertEqual(creds["refresh_token"], "secret-refresh-token-value-2600")
        self.assertEqual(creds["account_hash"], "HASH")
        raw = self.store._conn.execute(
            "SELECT token_enc FROM broker_links WHERE email=?", ("m@example.com",)
        ).fetchone()[0]
        self.assertNotIn("secret-access-token-value-2600", raw)
        self.assertNotIn("secret-refresh-token-value-2600", raw)
        self.assertNotIn("access_token", raw)
        self.assertTrue(raw.startswith("fernet:"))

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
        self.key = b"k"

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
