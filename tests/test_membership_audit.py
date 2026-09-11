import json
import os
import tempfile
import unittest
from urllib.parse import parse_qs, urlparse

from hedge_desk.membership import Clock, MembershipStore
from hedge_desk.membership_audit import (
    GENESIS,
    MembershipAuditLog,
    SupabaseMembershipAuditLog,
    entry_hash,
    verify_chain,
)


class AuditLogTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.log = MembershipAuditLog(os.path.join(self.tmp, "audit.db"))

    def tearDown(self):
        self.log.close()

    def test_first_entry_links_to_genesis(self):
        e = self.log.record("guest_signup", "a@example.com")
        self.assertEqual(e["seq"], 1)
        self.assertEqual(e["prev_hash"], GENESIS)

    def test_chain_links_consecutively(self):
        a = self.log.record("guest_signup", "a@example.com")
        b = self.log.record("subscribed", "a@example.com")
        self.assertEqual(b["prev_hash"], a["entry_hash"])
        self.assertEqual(b["seq"], 2)

    def test_chain_verifies_clean(self):
        self.log.record("guest_signup", "a@example.com")
        self.log.record("lp_invited", "lp@example.com", actor="gp@example.com")
        self.assertEqual(self.log.verify(), [])

    def test_tampering_with_a_field_breaks_the_chain(self):
        self.log.record("guest_signup", "a@example.com")
        self.log.record("subscribed", "a@example.com")
        # Tamper directly in the DB: change the event of entry 1.
        self.log._conn.execute(
            "UPDATE membership_events SET event='hacked' WHERE seq=1"
        )
        self.log._conn.commit()
        reasons = self.log.verify()
        self.assertTrue(reasons, "tampering must be detected")
        self.assertTrue(any("ENTRY_HASH_MISMATCH" in r for r in reasons))

    def test_deleting_an_entry_breaks_the_chain(self):
        self.log.record("e1", "a@example.com")
        self.log.record("e2", "a@example.com")
        self.log.record("e3", "a@example.com")
        self.log._conn.execute("DELETE FROM membership_events WHERE seq=2")
        self.log._conn.commit()
        reasons = self.log.verify()
        self.assertTrue(reasons, "a removed entry must be detected")

    def test_email_is_lowercased(self):
        e = self.log.record("guest_signup", "MiXeD@Example.COM")
        self.assertEqual(e["email"], "mixed@example.com")

    def test_entries_are_append_only_ordered(self):
        for i in range(5):
            self.log.record("evt", f"u{i}@example.com")
        entries = self.log.entries()
        self.assertEqual([e["seq"] for e in entries], [1, 2, 3, 4, 5])

    def test_verify_chain_helper_detects_hash_mismatch(self):
        e = self.log.record("evt", "a@example.com")
        bad = dict(e)
        bad["event"] = "changed"
        self.assertTrue(verify_chain([bad]))


class FakeSupabase:
    def __init__(self):
        self.rows = []

    def __call__(self, method, url, headers, body):
        parsed = urlparse(url)
        q = parse_qs(parsed.query)
        if method == "GET":
            order_desc = any("seq.desc" in v for v in q.get("order", []))
            rows = sorted(self.rows, key=lambda r: r["seq"], reverse=order_desc)
            limit = 1 if any("limit=1" in v for v in q.get("limit", [])) else len(rows)
            out = rows[:limit]
            return 200, json.dumps(out).encode()
        if method == "POST":
            self.rows.append(json.loads(body))
            return 201, b"[]"
        return 404, b""


class SupabaseAuditTests(unittest.TestCase):
    def setUp(self):
        self.backend = FakeSupabase()
        self.log = SupabaseMembershipAuditLog(
            "https://p.supabase.co", "svc", transport=self.backend
        )

    def test_record_and_verify(self):
        self.log.record("guest_signup", "a@example.com")
        self.log.record("lp_invited", "lp@example.com", actor="gp@x.com")
        self.assertEqual(self.log.verify(), [])
        entries = self.log.entries()
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[1]["prev_hash"], entries[0]["entry_hash"])

    def test_requires_credentials(self):
        with self.assertRaises(ValueError):
            SupabaseMembershipAuditLog("", "", transport=self.backend)


class FakeClock(Clock):
    def now(self):
        from datetime import datetime, timezone

        return datetime(2026, 1, 1, tzinfo=timezone.utc)


class AuditEndpointTests(unittest.TestCase):
    def setUp(self):
        from hedge_desk.auth_app import make_auth_app
        from tests.test_auth_app import CaptureSender

        self.tmp = tempfile.mkdtemp()
        self.store = MembershipStore(os.path.join(self.tmp, "m.db"), clock=Clock(), secret="s")
        self.audit = MembershipAuditLog(os.path.join(self.tmp, "a.db"))
        self.sender = CaptureSender()
        self.gp = "gp@x.com"
        self.dispatch = make_auth_app(
            self.store, sender=self.sender, gp_email=self.gp, audit=self.audit
        )

    def tearDown(self):
        self.store.close()
        self.audit.close()

    def _post(self, path, payload, cookie=None):
        import io

        body = json.dumps(payload).encode()
        env = {
            "PATH_INFO": path, "REQUEST_METHOD": "POST",
            "CONTENT_LENGTH": str(len(body)), "wsgi.input": io.BytesIO(body),
        }
        if cookie:
            env["HTTP_COOKIE"] = "emporion_session=" + cookie
        cap = {}

        def start(s, h):
            cap["status"] = s
            cap["headers"] = dict(h)

        out = b"".join(self.dispatch(env, start))
        return cap, json.loads(out)

    def _get(self, path, cookie=None):
        env = {"PATH_INFO": path, "REQUEST_METHOD": "GET"}
        if cookie:
            env["HTTP_COOKIE"] = "emporion_session=" + cookie
        cap = {}

        def start(s, h):
            cap["status"] = s
            cap["headers"] = dict(h)

        out = b"".join(self.dispatch(env, start))
        return cap, json.loads(out)

    def _signin(self, email):
        from http.cookies import SimpleCookie

        self._post("/api/auth/request", {"email": email})
        code = self.sender.sent[-1]["body"].split("code is:\n\n")[1].split("\n")[0]
        cap, body = self._post("/api/auth/verify", {"email": email, "code": code})
        sc = SimpleCookie()
        sc.load(cap["headers"]["Set-Cookie"])
        return sc["emporion_session"].value

    def test_invite_and_subscribe_are_audited(self):
        cookie = self._signin(self.gp)
        self._post("/api/auth/invite", {"email": "lp@example.com"}, cookie=cookie)
        events = [e["event"] for e in self.audit.entries()]
        self.assertIn("lp_invited", events)

    def test_audit_endpoint_gp_only(self):
        cap, _ = self._get("/api/auth/audit")
        self.assertEqual(cap["status"], "403 Forbidden")
        cookie = self._signin(self.gp)
        cap, body = self._get("/api/auth/audit", cookie=cookie)
        self.assertEqual(cap["status"], "200 OK")
        self.assertTrue(body["valid"])
        self.assertIsInstance(body["entries"], list)

    def test_audit_chain_valid_after_real_actions(self):
        cookie = self._signin(self.gp)
        self._post("/api/auth/invite", {"email": "lp@example.com"}, cookie=cookie)
        self.assertEqual(self.audit.verify(), [])


if __name__ == "__main__":
    unittest.main()
