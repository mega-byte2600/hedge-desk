import os
import tempfile
import unittest

from hedge_desk.membership import Clock, MembershipStore
from hedge_desk.rate_limit import AuthRateLimits, SlidingWindowLimiter


class FakeMonotonic:
    def __init__(self):
        self.t = 1000.0

    def __call__(self):
        return self.t

    def advance(self, seconds):
        self.t += seconds


class SlidingWindowLimiterTests(unittest.TestCase):
    def setUp(self):
        self.clock = FakeMonotonic()
        self.limiter = SlidingWindowLimiter(3, 60, clock=self.clock)

    def test_allows_up_to_limit_then_denies(self):
        self.assertTrue(self.limiter.allow("k"))
        self.assertTrue(self.limiter.allow("k"))
        self.assertTrue(self.limiter.allow("k"))
        self.assertFalse(self.limiter.allow("k"), "fourth attempt must be denied")

    def test_window_slides(self):
        for _ in range(3):
            self.limiter.allow("k")
        self.assertFalse(self.limiter.allow("k"))
        self.clock.advance(61)
        self.assertTrue(self.limiter.allow("k"), "limit should reset after the window")

    def test_keys_are_independent(self):
        for _ in range(3):
            self.limiter.allow("a")
        self.assertFalse(self.limiter.allow("a"))
        self.assertTrue(self.limiter.allow("b"))

    def test_remaining_and_reset(self):
        self.limiter.allow("k")
        self.assertEqual(self.limiter.remaining("k"), 2)
        self.limiter.reset("k")
        self.assertEqual(self.limiter.remaining("k"), 3)

    def test_invalid_limit_rejected(self):
        with self.assertRaises(ValueError):
            SlidingWindowLimiter(0, 60)


class AuthRateLimitsTests(unittest.TestCase):
    def setUp(self):
        self.clock = FakeMonotonic()
        self.limits = AuthRateLimits(clock=self.clock)

    def test_request_limited_per_email(self):
        for _ in range(5):
            self.assertTrue(self.limits.allow_request("a@example.com", "1.1.1.1"))
        self.assertFalse(self.limits.allow_request("a@example.com", "1.1.1.1"))

    def test_request_limited_per_ip(self):
        # 20 different addresses from one IP trips the IP limit
        for i in range(20):
            self.assertTrue(self.limits.allow_request(f"u{i}@example.com", "9.9.9.9"))
        self.assertFalse(self.limits.allow_request("other@example.com", "9.9.9.9"))

    def test_verify_limited_per_email(self):
        for _ in range(10):
            self.assertTrue(self.limits.allow_verify("a@example.com"))
        self.assertFalse(self.limits.allow_verify("a@example.com"))


class AuthEndpointRateLimitTests(unittest.TestCase):
    def setUp(self):
        import io, json

        from hedge_desk.auth_app import make_auth_app

        self.tmp = tempfile.mkdtemp()
        self.store = MembershipStore(os.path.join(self.tmp, "r.db"), clock=Clock(), secret="s")
        self.sent = []

        def sender(to, subj, body):
            self.sent.append(body)

        self.limits = AuthRateLimits(clock=FakeMonotonic())
        self.dispatch = make_auth_app(
            self.store, sender=sender, gp_email="gp@x.com", rate_limits=self.limits
        )

    def tearDown(self):
        self.store.close()

    def _post(self, path, payload, ip="1.2.3.4"):
        import io, json

        body = json.dumps(payload).encode()
        env = {
            "PATH_INFO": path,
            "REQUEST_METHOD": "POST",
            "CONTENT_LENGTH": str(len(body)),
            "wsgi.input": io.BytesIO(body),
            "HTTP_X_FORWARDED_FOR": ip,
        }
        cap = {}

        def start(s, h):
            cap["status"] = s

        out = b"".join(self.dispatch(env, start))
        return cap["status"], json.loads(out)

    def test_otp_request_is_rate_limited(self):
        email = "bomb@example.com"
        for _ in range(5):
            status, _ = self._post("/api/auth/request", {"email": email})
            self.assertEqual(status, "202 Accepted")
        status, body = self._post("/api/auth/request", {"email": email})
        self.assertEqual(status, "429 Too Many Requests")
        self.assertEqual(body["error"], "rate_limited")

    def test_otp_verify_is_rate_limited(self):
        email = "guess@example.com"
        self._post("/api/auth/request", {"email": email})
        for _ in range(10):
            status, _ = self._post("/api/auth/verify", {"email": email, "code": "wrong"})
            self.assertEqual(status, "401 Unauthorized")
        status, body = self._post("/api/auth/verify", {"email": email, "code": "wrong"})
        self.assertEqual(status, "429 Too Many Requests")

    def test_other_addresses_unaffected_by_one_address_limit(self):
        # Burning out one address must not block a different address on a
        # different client.
        for _ in range(6):
            self._post("/api/auth/request", {"email": "a@example.com"}, ip="10.0.0.1")
        status, _ = self._post("/api/auth/request", {"email": "b@example.com"}, ip="10.0.0.2")
        self.assertEqual(status, "202 Accepted")


class LimiterHardeningTests(unittest.TestCase):
    """Bounded memory, atomic accounting, IP checked first."""

    def test_key_map_stays_bounded(self):
        # Keys are caller-controlled (an attacker picks the email address) and a
        # key was never removed once created, so one client could grow the map
        # without limit on a 512MB instance.
        clock = FakeMonotonic()
        limiter = SlidingWindowLimiter(5, 60, clock=clock, max_keys=50)
        for i in range(500):
            limiter.allow(f"victim{i}@example.com")
        self.assertLessEqual(
            len(limiter._events), 60, "the key map must not grow without bound"
        )

    def test_live_keys_are_never_evicted_inside_their_window(self):
        clock = FakeMonotonic()
        limiter = SlidingWindowLimiter(2, 600, clock=clock, max_keys=10)
        for i in range(5):
            limiter.allow(f"live{i}@example.com")
        # A live window must still be enforced: evicting active keys to make room
        # would let a caller reset its own limit by flooding new addresses.
        self.assertTrue(limiter.allow("live0@example.com"))
        self.assertFalse(limiter.allow("live0@example.com"))

    def test_exhausted_budget_fails_closed_for_new_keys(self):
        clock = FakeMonotonic()
        limiter = SlidingWindowLimiter(5, 600, clock=clock, max_keys=3)
        for i in range(3):
            self.assertTrue(limiter.allow(f"a{i}@example.com"))
        self.assertFalse(limiter.allow("a-brand-new@example.com"))
        self.assertLessEqual(len(limiter._events), 3)

    def test_expired_keys_are_reclaimed_once_the_window_passes(self):
        clock = FakeMonotonic()
        limiter = SlidingWindowLimiter(5, 60, clock=clock, max_keys=3)
        for i in range(3):
            limiter.allow(f"a{i}@example.com")
        self.assertFalse(limiter.allow("blocked@example.com"))
        clock.advance(61)     # every window has elapsed
        self.assertTrue(limiter.allow("fresh@example.com"))
        self.assertLessEqual(len(limiter._events), 3)

    def test_ip_limit_is_checked_before_the_address_budget_is_spent(self):
        # The per-address limiter used to run first, so traffic the IP limit was
        # about to refuse still consumed (and minted) per-address entries.
        clock = FakeMonotonic()
        limits = AuthRateLimits(clock=clock)
        for i in range(25):   # past the per-IP limit of 20
            limits.allow_request(f"fresh{i}@example.com", "203.0.113.9")
        self.assertEqual(
            limits.request_per_email.remaining("fresh24@example.com"),
            limits.request_per_email.limit,
            "a request refused by the IP limiter must not spend the address budget",
        )

    def test_concurrent_allows_cannot_exceed_the_limit(self):
        import threading

        limiter = SlidingWindowLimiter(50, 60)
        granted = []
        lock = threading.Lock()

        def hammer():
            for _ in range(50):
                if limiter.allow("shared-key"):
                    with lock:
                        granted.append(1)

        threads = [threading.Thread(target=hammer) for _ in range(6)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        self.assertLessEqual(len(granted), 50, "check-then-act must be atomic")


if __name__ == "__main__":
    unittest.main()
