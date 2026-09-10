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


if __name__ == "__main__":
    unittest.main()
