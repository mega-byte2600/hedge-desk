import unittest
from datetime import datetime, timedelta, timezone

from hedge_desk.brokers.schwab_tokens import (
    SchwabTokenError,
    SchwabTokenManager,
    SchwabTokenState,
)


NOW = datetime(2026, 1, 1, tzinfo=timezone.utc)


def token_state(*, expires_at=NOW + timedelta(hours=1), issued_at=NOW - timedelta(days=1)):
    return SchwabTokenState("access-secret", "refresh-secret", expires_at, issued_at, "readonly", NOW)


class SchwabTokenManagerTests(unittest.TestCase):
    def test_unexpired_access_token_is_returned_without_refresh(self):
        def unexpected(_token):
            raise AssertionError("valid access token must not refresh")

        manager = SchwabTokenManager(
            refresh=unexpected,
            persist=lambda _state: self.fail("valid token must not persist"),
            refresh_token_max_age=timedelta(days=7),
        )
        self.assertEqual(manager.access_token(token_state(), NOW), "access-secret")
        self.assertNotIn("access-secret", repr(token_state()))
        self.assertNotIn("refresh-secret", repr(token_state()))

    def test_forced_refresh_refreshes_an_unexpired_token_and_persists_first(self):
        calls = []
        persisted = []
        manager = SchwabTokenManager(
            refresh=lambda token: calls.append(token) or {
                "status": "ok", "access_token": "new-access", "refresh_token": "new-refresh",
                "expires_in": 1800, "scope": "api",
            },
            persist=lambda current: persisted.append(current),
            refresh_token_max_age=timedelta(days=7),
        )
        result = manager.access_token(
            token_state(expires_at=NOW + timedelta(minutes=10)), NOW, force_refresh=True
        )
        self.assertEqual(result, "new-access")
        self.assertEqual(calls, ["refresh-secret"])
        self.assertEqual(persisted[0].refresh_token, "new-refresh")

    def test_refresh_is_persisted_before_token_is_returned(self):
        events = []
        refreshed = {
            "status": "ok",
            "access_token": "new-access",
            "refresh_token": "new-refresh",
            "expires_in": 1800,
            "scope": "readonly",
        }

        def persist(state):
            self.assertEqual(state.access_token, "new-access")
            events.append("persist")

        manager = SchwabTokenManager(
            refresh=lambda token: (events.append(("refresh", token)) or refreshed),
            persist=persist,
            refresh_token_max_age=timedelta(days=7),
        )
        result = manager.access_token(token_state(expires_at=NOW), NOW)
        self.assertEqual(result, "new-access")
        self.assertEqual(events, [("refresh", "refresh-secret"), "persist"])

    def test_unverified_refresh_lifetime_fails_closed(self):
        manager = SchwabTokenManager(
            refresh=lambda _token: self.fail("must not refresh"),
            persist=lambda _state: self.fail("must not persist"),
            refresh_token_max_age=None,
        )
        with self.assertRaisesRegex(SchwabTokenError, "refresh_lifetime_unverified"):
            manager.access_token(token_state(expires_at=NOW), NOW)

    def test_expired_refresh_token_requires_reauthentication(self):
        manager = SchwabTokenManager(
            refresh=lambda _token: self.fail("must not refresh an expired token"),
            persist=lambda _state: self.fail("must not persist"),
            refresh_token_max_age=timedelta(days=7),
        )
        with self.assertRaisesRegex(SchwabTokenError, "reauthentication_required"):
            manager.access_token(token_state(expires_at=NOW, issued_at=NOW - timedelta(days=7)), NOW)

    def test_refresh_failure_and_persistence_failure_do_not_return_access(self):
        manager = SchwabTokenManager(
            refresh=lambda _token: {"status": "error", "error": "reauthentication_required"},
            persist=lambda _state: None,
            refresh_token_max_age=timedelta(days=7),
        )
        with self.assertRaisesRegex(SchwabTokenError, "reauthentication_required"):
            manager.access_token(token_state(expires_at=NOW), NOW)

        manager = SchwabTokenManager(
            refresh=lambda _token: {"status": "ok", "access_token": "new", "expires_in": 600},
            persist=lambda _state: (_ for _ in ()).throw(OSError("storage unavailable")),
            refresh_token_max_age=timedelta(days=7),
        )
        with self.assertRaisesRegex(SchwabTokenError, "token_persistence_failed"):
            manager.access_token(token_state(expires_at=NOW), NOW)


if __name__ == "__main__":
    unittest.main()
