import unittest
from datetime import datetime, timedelta, timezone
from urllib.parse import parse_qs, urlparse

from hedge_desk.membership_base import (
    MAX_LP_MEMBERS,
    ROLE_LP,
    ROLE_MEMBER,
)
from hedge_desk.supabase_membership import SupabaseMembershipStore


class FakeClock:
    def __init__(self):
        self._t = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

    def now(self):
        return self._t

    def advance(self, delta):
        self._t += delta


class FakeSupabase:
    """Minimal in-memory PostgREST emulator: eq filters, upsert, patch, delete."""

    def __init__(self):
        self.tables = {"members": {}, "otps": {}, "sessions": {}}
        self._otp_seq = 0

    def _filter_rows(self, table, query):
        params = parse_qs(query)
        rows = list(self.tables[table].values())
        for key, val in params.items():
            if key in ("select", "order"):
                continue
            if val and val[0].startswith("eq."):
                want = val[0][3:]
                if want == "false":
                    rows = [r for r in rows if r.get(key) is False]
                elif want == "true":
                    rows = [r for r in rows if r.get(key) is True]
                else:
                    rows = [r for r in rows if str(r.get(key)) == want]
        return rows

    def __call__(self, method, url, headers, body):
        parsed = urlparse(url)
        table = parsed.path.rsplit("/", 1)[-1]
        query = parsed.query
        payload = None
        if body:
            import json

            payload = json.loads(body)

        if method == "GET":
            rows = self._filter_rows(table, query)
            import json

            return 200, json.dumps(rows).encode()

        if method == "POST":
            row = dict(payload)
            if table == "members":
                key = row["email"]
                self.tables["members"][key] = row
            elif table == "sessions":
                self.tables["sessions"][row["token_hash"]] = row
            elif table == "otps":
                self._otp_seq += 1
                row["id"] = self._otp_seq
                self.tables["otps"][str(self._otp_seq)] = row
            return 201, b"[]"

        if method == "PATCH":
            rows = self._filter_rows(table, query)
            for r in rows:
                r.update(payload)
            import json

            return 200, json.dumps(rows).encode()

        if method == "DELETE":
            rows = self._filter_rows(table, query)
            for r in rows:
                for k, v in list(self.tables[table].items()):
                    if v is r:
                        del self.tables[table][k]
            return 204, b""

        return 404, b""


class SupabaseMembershipTests(unittest.TestCase):
    def setUp(self):
        self.backend = FakeSupabase()
        self.clock = FakeClock()
        self.store = SupabaseMembershipStore(
            "https://proj.supabase.co",
            "service-key",
            secret="test-secret",
            clock=self.clock,
            transport=self.backend,
        )

    def test_guest_upsert_and_access(self):
        self.store.upsert_guest("g@example.com")
        decision = self.store.access_for("g@example.com")
        self.assertTrue(decision.allowed)
        self.assertEqual(decision.role, "GUEST")

    def test_guest_expires(self):
        self.store.upsert_guest("g@example.com")
        self.clock.advance(timedelta(days=31, seconds=1))
        self.assertFalse(self.store.access_for("g@example.com").allowed)

    def test_subscribe_upgrades_to_member(self):
        self.store.upsert_guest("s@example.com")
        self.store.set_subscribed("s@example.com")
        m = self.store.get_member("s@example.com")
        self.assertEqual(m["role"], ROLE_MEMBER)
        self.assertTrue(m["subscribed"])
        self.assertIsNone(m["guest_expires_at"])

    def test_promote_to_lp_marks_investor(self):
        self.store.promote_to_lp("lp@example.com")
        m = self.store.get_member("lp@example.com")
        self.assertEqual(m["role"], ROLE_LP)
        self.assertTrue(m["investor"])
        self.assertFalse(m["subscribed"])

    def test_lp_fee_schedule(self):
        self.store.promote_to_lp("fee@example.com")
        self.store.set_lp_fee("fee@example.com", "carried", "0.20")
        m = self.store.get_member("fee@example.com")
        self.assertEqual(m["fee_type"], "carried")
        self.assertEqual(m["fee_rate"], "0.20")

    def test_lp_cap_enforced(self):
        for i in range(MAX_LP_MEMBERS):
            self.store.promote_to_lp(f"lp{i}@x.com")
        with self.assertRaises(ValueError):
            self.store.issue_lp_invite("overflow@x.com")

    def test_otp_roundtrip_single_use(self):
        code = self.store.issue_otp("o@example.com")
        self.assertTrue(self.store.verify_otp("o@example.com", code))
        self.assertFalse(self.store.verify_otp("o@example.com", code))

    def test_otp_wrong_code_denied(self):
        code = self.store.issue_otp("o@example.com")
        self.assertFalse(self.store.verify_otp("o@example.com", code + "x"))

    def test_session_roundtrip(self):
        self.store.upsert_guest("se@example.com")
        token = self.store.create_session("se@example.com")
        self.assertEqual(self.store.lookup_session(token), "se@example.com")
        self.store.delete_session(token)
        self.assertIsNone(self.store.lookup_session(token))

    def test_requires_credentials(self):
        with self.assertRaises(ValueError):
            SupabaseMembershipStore("", "", secret="x", transport=self.backend)


class StoreSelectionTests(unittest.TestCase):
    def test_selects_supabase_when_configured(self):
        import os, tempfile
        from unittest.mock import patch
        from hedge_desk.auth_app import default_membership_store
        from hedge_desk.supabase_membership import SupabaseMembershipStore

        env = {"SUPABASE_URL": "https://proj.supabase.co", "SUPABASE_SERVICE_KEY": "svc"}
        with patch.dict(os.environ, env, clear=False):
            store = default_membership_store()
        self.assertIsInstance(store, SupabaseMembershipStore)

    def test_falls_back_to_sqlite_without_supabase_env(self):
        import os, tempfile
        from unittest.mock import patch
        from hedge_desk.auth_app import default_membership_store
        from hedge_desk.membership import MembershipStore

        tmp = tempfile.mkdtemp()
        env = {"MEMBERSHIP_DB": os.path.join(tmp, "m.db")}
        cleaned = {k: v for k, v in os.environ.items()
                   if k not in ("SUPABASE_URL", "SUPABASE_SERVICE_KEY", "SUPABASE_SERVICE_ROLE_KEY")}
        cleaned.update(env)
        with patch.dict(os.environ, cleaned, clear=True):
            store = default_membership_store()
        self.assertIsInstance(store, MembershipStore)
        store.close()


if __name__ == "__main__":
    unittest.main()
