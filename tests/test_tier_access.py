import os
import tempfile
import unittest
from datetime import datetime, timezone

from hedge_desk.membership import MembershipStore, Clock
from hedge_desk.tier_access import (
    DataTier,
    can_access_real_data,
    data_tier_for,
    is_investor,
)


class TierAccessPolicyTests(unittest.TestCase):
    def test_guest_is_synthetic_only(self):
        self.assertEqual(data_tier_for("GUEST"), DataTier.SYNTHETIC)
        self.assertFalse(can_access_real_data("GUEST"))
        self.assertFalse(is_investor("GUEST"))

    def test_member_has_real_data_but_not_investor(self):
        self.assertEqual(data_tier_for("MEMBER"), DataTier.REAL)
        self.assertTrue(can_access_real_data("MEMBER"))
        self.assertFalse(is_investor("MEMBER"))

    def test_lp_has_full_service_and_is_investor(self):
        self.assertEqual(data_tier_for("LP"), DataTier.FULL)
        self.assertTrue(can_access_real_data("LP"))
        self.assertTrue(is_investor("LP"))

    def test_gp_has_full_service(self):
        self.assertEqual(data_tier_for("GP"), DataTier.FULL)
        self.assertTrue(can_access_real_data("GP"))

    def test_unknown_or_missing_role_fails_closed_to_synthetic(self):
        self.assertEqual(data_tier_for(None), DataTier.SYNTHETIC)
        self.assertEqual(data_tier_for(""), DataTier.SYNTHETIC)
        self.assertEqual(data_tier_for("HACKER"), DataTier.SYNTHETIC)
        self.assertFalse(can_access_real_data(None))


class TierAccessEndpointTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.db = os.path.join(self.tmp, "tier.db")
        self.store = MembershipStore(self.db, clock=Clock(), secret="test-secret")
        from hedge_desk.auth_app import make_auth_app

        class _S:
            def __init__(self):
                self.sent = []

            def __call__(self, to, subj, body):
                self.sent.append(body)

        self.sender = _S()
        self.dispatch = make_auth_app(self.store, sender=self.sender, gp_email="gp@x.com")

    def tearDown(self):
        self.store.close()

    def _guest_session(self):
        # sign in as a guest (open test-drive)
        import io, json
        from hedge_desk.auth_app import SESSION_COOKIE
        from http.cookies import SimpleCookie

        email = "guest@example.com"
        body = json.dumps({"email": email}).encode()
        env = {"PATH_INFO": "/api/auth/request", "REQUEST_METHOD": "POST",
               "CONTENT_LENGTH": str(len(body)), "wsgi.input": io.BytesIO(body)}
        cap = {}
        def start(s, h): cap["status"] = s
        self.dispatch(env, start)
        code = self.sender.sent[-1].split("code is:\n\n")[1].split("\n")[0]
        body = json.dumps({"email": email, "code": code}).encode()
        env = {"PATH_INFO": "/api/auth/verify", "REQUEST_METHOD": "POST",
               "CONTENT_LENGTH": str(len(body)), "wsgi.input": io.BytesIO(body)}
        hdrs = {}
        def start2(s, h): cap["status"] = s; hdrs["set-cookie"] = dict(h).get("Set-Cookie", "")
        self.dispatch(env, start2)
        sc = SimpleCookie(); sc.load(hdrs["set-cookie"])
        return sc[SESSION_COOKIE].value

    def test_tier_endpoint_guest_is_synthetic(self):
        import io, json
        cookie = self._guest_session()
        env = {"PATH_INFO": "/api/tier", "REQUEST_METHOD": "GET",
               "HTTP_COOKIE": "emporion_session=" + cookie}
        cap = {}
        def start(s, h): cap["status"] = s
        out = b"".join(self.dispatch(env, start))
        payload = json.loads(out)
        self.assertEqual(payload["tier"], "synthetic")
        self.assertFalse(payload["real_data"])

    def test_guest_denied_real_data(self):
        import json
        cookie = self._guest_session()
        env = {"PATH_INFO": "/api/data/real", "REQUEST_METHOD": "GET",
               "HTTP_COOKIE": "emporion_session=" + cookie}
        cap = {}
        def start(s, h): cap["status"] = s
        out = b"".join(self.dispatch(env, start))
        self.assertEqual(cap["status"], "403 Forbidden")
        payload = json.loads(out)
        self.assertEqual(payload["error"], "real_data_requires_member")

    def test_unauthenticated_tier_is_synthetic(self):
        import json
        env = {"PATH_INFO": "/api/tier", "REQUEST_METHOD": "GET"}
        cap = {}
        def start(s, h): cap["status"] = s
        out = b"".join(self.dispatch(env, start))
        payload = json.loads(out)
        self.assertEqual(payload["tier"], "synthetic")


if __name__ == "__main__":
    unittest.main()
