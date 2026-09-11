import os
import tempfile
import threading
import unittest
from datetime import datetime, timedelta, timezone

from hedge_desk.membership import (
    MAX_LP_MEMBERS,
    OTP_TTL_SECONDS,
    ROLE_GP,
    ROLE_GUEST,
    ROLE_LP,
    ROLE_MEMBER,
    SESSION_TTL_SECONDS,
    Clock,
    MembershipStore,
)


class FakeClock(Clock):
    def __init__(self, start: datetime):
        self._t = start

    def now(self) -> datetime:
        return self._t

    def advance(self, delta):
        self._t = self._t + delta


T0 = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)


class MembershipStoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.db = os.path.join(self.tmp, "members.db")
        self.clock = FakeClock(T0)
        self.store = MembershipStore(
            self.db, clock=self.clock, secret="test-secret"
        )

    def tearDown(self):
        self.store.close()

    # ---- guest tier --------------------------------------------------------

    def test_guest_gets_31_day_access(self):
        self.store.upsert_guest("person@example.com")
        decision = self.store.access_for("person@example.com")
        self.assertTrue(decision.allowed)
        self.assertEqual(decision.role, ROLE_GUEST)

        member = self.store.get_member("person@example.com")
        expires = datetime.fromisoformat(member["guest_expires_at"])
        self.assertEqual(
            expires, T0 + timedelta(days=31), "guest access should be 31 days"
        )

    def test_guest_access_expires_after_31_days(self):
        self.store.upsert_guest("person@example.com")
        self.clock.advance(timedelta(days=31, seconds=1))
        decision = self.store.access_for("person@example.com")
        self.assertFalse(decision.allowed, "expired guest must be denied")
        self.assertEqual(decision.reason, "guest_expired")

    def test_unknown_email_is_denied_fail_closed(self):
        decision = self.store.access_for("nobody@example.com")
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.reason, "not_a_member")

    def test_email_is_normalized_to_lowercase(self):
        self.store.upsert_guest("Person@Example.COM")
        decision = self.store.access_for("person@example.com")
        self.assertTrue(decision.allowed)

    # ---- subscription member tier ------------------------------------------

    def test_member_subscription_does_not_expire(self):
        self.store.upsert_guest("sub@example.com")
        self.store.set_subscribed("sub@example.com")
        # even far in the future a member keeps access
        self.clock.advance(timedelta(days=400))
        decision = self.store.access_for("sub@example.com")
        self.assertTrue(decision.allowed)
        self.assertEqual(decision.role, ROLE_MEMBER)

    def test_subscription_clears_guest_expiry(self):
        self.store.upsert_guest("sub@example.com")
        self.store.set_subscribed("sub@example.com")
        member = self.store.get_member("sub@example.com")
        self.assertIsNone(member["guest_expires_at"])
        self.assertTrue(member["subscribed"])

    def test_subscribe_does_not_downgrade_lp(self):
        self.store.promote_to_lp("lp@example.com")
        member = self.store.set_subscribed("lp@example.com")
        self.assertEqual(member["role"], ROLE_LP, "an LP must not be downgraded to MEMBER")
        self.assertTrue(member["investor"])

    def test_subscribe_creates_row_when_missing(self):
        member = self.store.set_subscribed("fresh@example.com")
        self.assertEqual(member["role"], ROLE_MEMBER)
        self.assertTrue(member["subscribed"])

    # ---- LP tier + cap -----------------------------------------------------

    def test_lp_promotion_clears_guest_expiry(self):
        self.store.upsert_guest("lp@example.com")
        self.store.promote_to_lp("lp@example.com")
        member = self.store.get_member("lp@example.com")
        self.assertIsNone(member["guest_expires_at"])
        self.assertEqual(member["role"], ROLE_LP)
        self.assertTrue(member["investor"], "LP is an LLC investor, not a payer")
        decision = self.store.access_for("lp@example.com")
        self.assertTrue(decision.allowed)
        self.assertEqual(decision.role, ROLE_LP)

    def test_lp_is_investor_not_subscriber(self):
        # LP is never the paid 'subscribed' tier; investor flag distinguishes them.
        self.store.promote_to_lp("investor@example.com")
        member = self.store.get_member("investor@example.com")
        self.assertTrue(member["investor"])
        self.assertFalse(member["subscribed"], "LP is not a paid subscriber")
        self.assertEqual(member["role"], ROLE_LP)

    def test_set_lp_fee_schedule(self):
        self.store.promote_to_lp("fee@example.com")
        self.store.set_lp_fee("fee@example.com", "management", "0.015")
        member = self.store.get_member("fee@example.com")
        self.assertEqual(member["fee_type"], "management")
        self.assertEqual(member["fee_rate"], "0.015")

    def test_issue_lp_invite_marks_investor(self):
        invite = self.store.issue_lp_invite("newlp@example.com")
        self.assertTrue(invite["token"])
        member = self.store.get_member("newlp@example.com")
        self.assertEqual(member["role"], ROLE_LP)
        self.assertTrue(member["investor"])

    def test_lp_cap_is_enforced(self):
        for i in range(MAX_LP_MEMBERS):
            self.store.promote_to_lp(f"lp{i}@example.com")
        self.assertEqual(self.store.lp_count(), MAX_LP_MEMBERS)
        with self.assertRaises(ValueError):
            self.store.issue_lp_invite("overflow@example.com")
        self.assertEqual(self.store.lp_count(), MAX_LP_MEMBERS)

    def test_issue_lp_invite_creates_or_updates_and_respects_cap(self):
        invite = self.store.issue_lp_invite("newlp@example.com")
        self.assertTrue(invite["token"])
        member = self.store.get_member("newlp@example.com")
        self.assertEqual(member["role"], ROLE_LP)
        self.assertEqual(member["invite_token"], invite["token"])
        expires = datetime.fromisoformat(invite["expires_at"])
        self.assertEqual(expires, T0 + timedelta(days=14))

    # ---- OTP ---------------------------------------------------------------

    def test_otp_verify_success_and_single_use(self):
        code = self.store.issue_otp("otp@example.com")
        self.assertTrue(self.store.verify_otp("otp@example.com", code))
        self.assertFalse(
            self.store.verify_otp("otp@example.com", code),
            "OTP must be single-use",
        )

    def test_otp_wrong_code_denied(self):
        code = self.store.issue_otp("otp@example.com")
        self.assertFalse(self.store.verify_otp("otp@example.com", code + "x"))

    def test_otp_expires(self):
        code = self.store.issue_otp("otp@example.com")
        self.clock.advance(timedelta(seconds=OTP_TTL_SECONDS + 1))
        self.assertFalse(self.store.verify_otp("otp@example.com", code))

    # ---- sessions ----------------------------------------------------------

    def test_session_create_lookup_and_expiry(self):
        self.store.upsert_guest("session@example.com")
        token = self.store.create_session("session@example.com")
        self.assertEqual(
            self.store.lookup_session(token), "session@example.com"
        )
        self.clock.advance(timedelta(days=46))
        self.assertIsNone(self.store.lookup_session(token))

    def test_session_lookup_wrong_token_denied(self):
        self.store.upsert_guest("session@example.com")
        token = self.store.create_session("session@example.com")
        self.assertIsNone(self.store.lookup_session(token + "x"))
        self.store.delete_session(token)
        self.assertIsNone(self.store.lookup_session(token))


class StoreThreadSafetyTests(unittest.TestCase):
    """The web console serves requests from a thread pool.

    A sqlite3 connection is bound to its creating thread unless opened with
    check_same_thread=False, so a store built while handling one request used to
    raise ProgrammingError (HTTP 500) the moment another thread touched it.
    """

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.store = MembershipStore(
            os.path.join(self.tmp, "threads.db"), clock=FakeClock(T0), secret="test-secret"
        )

    def tearDown(self):
        self.store.close()

    def test_store_is_usable_from_another_thread(self):
        errors = []

        def work():
            try:
                self.store.upsert_guest("other-thread@example.com")
                self.store.get_member("other-thread@example.com")
            except Exception as exc:  # pragma: no cover - failure path
                errors.append(exc)

        thread = threading.Thread(target=work)
        thread.start()
        thread.join()
        self.assertEqual(errors, [])

    def test_concurrent_sign_ins_do_not_raise(self):
        errors = []

        def work(index):
            try:
                email = f"concurrent{index}@example.com"
                self.store.upsert_guest(email)
                token = self.store.create_session(email)
                self.store.lookup_session(token)
                self.store.access_for(email)
            except Exception as exc:  # pragma: no cover - failure path
                errors.append(exc)

        threads = [threading.Thread(target=work, args=(i,)) for i in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        self.assertEqual(errors, [])
        self.assertIsNotNone(self.store.get_member("concurrent7@example.com"))


if __name__ == "__main__":
    unittest.main()
