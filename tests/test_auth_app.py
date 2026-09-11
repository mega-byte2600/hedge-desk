import json
import os
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from http.cookies import SimpleCookie

from hedge_desk.auth_app import make_auth_app, SESSION_COOKIE
from hedge_desk.membership import Clock, MembershipStore, MAX_LP_MEMBERS


class FakeClock(Clock):
    def __init__(self):
        self._t = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

    def now(self):
        return self._t

    def advance(self, delta):
        self._t += delta


def _capture():
    c = {}

    def start(status, headers):
        c["status"] = status
        c["headers"] = headers

    return c, start


class CaptureSender:
    def __init__(self):
        self.sent = []

    def __call__(self, to, subject, body):
        self.sent.append({"to": to, "subject": subject, "body": body})


def _post(dispatch, path, payload, cookie=None):
    body = json.dumps(payload).encode("utf-8")
    environ = {
        "PATH_INFO": path,
        "REQUEST_METHOD": "POST",
        "CONTENT_LENGTH": str(len(body)),
        "wsgi.input": __import__("io").BytesIO(body),
    }
    if cookie:
        environ["HTTP_COOKIE"] = f"{SESSION_COOKIE}={cookie}"
    cap, start = _capture()
    out = b"".join(dispatch(environ, start))
    return cap["status"], json.loads(out), cap["headers"]


def _get(dispatch, path, cookie=None):
    environ = {"PATH_INFO": path, "REQUEST_METHOD": "GET"}
    if cookie:
        # cookie is a bare token; the server expects the named cookie header
        environ["HTTP_COOKIE"] = f"{SESSION_COOKIE}={cookie}"
    cap, start = _capture()
    out = b"".join(dispatch(environ, start))
    return cap["status"], json.loads(out), cap["headers"]


def _extract_cookie(headers):
    for k, v in headers:
        if k.lower() == "set-cookie" and SESSION_COOKIE in v:
            c = SimpleCookie()
            c.load(v)
            return c[SESSION_COOKIE].value
    return None


def _full_signin(dispatch, sender, email, clock=None):
    """Perform a full OTP sign-in and return the session cookie."""
    status, body, _ = _post(dispatch, "/api/auth/request", {"email": email})
    assert status.startswith("202"), body
    # The sender captured the OTP code (dev console fallback prints it).
    code = sender.sent[-1]["body"].split("code is:\n\n")[1].split("\n")[0].strip()
    status, body, headers = _post(dispatch, "/api/auth/verify", {"email": email, "code": code})
    assert status == "200 OK", body
    cookie = _extract_cookie(headers)
    assert cookie, "expected session cookie"
    return cookie


class AuthAppTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.db = os.path.join(self.tmp, "auth.db")
        self.clock = FakeClock()
        self.store = MembershipStore(self.db, clock=self.clock, secret="test-secret")
        self.sender = CaptureSender()
        self.gp = "gp@hedge-desk.com"
        self.dispatch = make_auth_app(
            self.store, sender=self.sender, gp_email=self.gp
        )

    def tearDown(self):
        self.store.close()

    def test_request_otp_sends_email_and_creates_guest(self):
        status, body, _ = _post(self.dispatch, "/api/auth/request", {"email": "new@example.com"})
        self.assertEqual(status, "202 Accepted")
        self.assertEqual(self.sender.sent[0]["to"], "new@example.com")
        self.assertIn("sign-in code", self.sender.sent[0]["subject"])
        member = self.store.get_member("new@example.com")
        self.assertIsNotNone(member)
        self.assertEqual(member["role"], "GUEST")

    def test_verify_with_correct_code_creates_session(self):
        status, _, _ = _post(self.dispatch, "/api/auth/request", {"email": "g@example.com"})
        code = self.sender.sent[-1]["body"].split("code is:\n\n")[1].split("\n")[0]
        status, body, headers = _post(
            self.dispatch, "/api/auth/verify", {"email": "g@example.com", "code": code}
        )
        self.assertEqual(status, "200 OK")
        self.assertEqual(body["role"], "GUEST")
        self.assertIsNotNone(_extract_cookie(headers))

    def test_verify_wrong_code_denied(self):
        _post(self.dispatch, "/api/auth/request", {"email": "w@example.com"})
        status, body, _ = _post(
            self.dispatch, "/api/auth/verify", {"email": "w@example.com", "code": "wrong"}
        )
        self.assertEqual(status, "401 Unauthorized")

    def test_me_reports_authenticated_role(self):
        cookie = _full_signin(self.dispatch, self.sender, "me@example.com")
        status, body, _ = _get(self.dispatch, "/api/auth/me", cookie=cookie)
        self.assertEqual(status, "200 OK")
        self.assertTrue(body["authenticated"])
        self.assertEqual(body["email"], "me@example.com")
        self.assertEqual(body["role"], "GUEST")
        self.assertTrue(body["access"])

    def test_me_unauthenticated(self):
        status, body, _ = _get(self.dispatch, "/api/auth/me")
        self.assertEqual(status, "200 OK")
        self.assertFalse(body["authenticated"])

    def test_guest_expires_after_31_days(self):
        cookie = _full_signin(self.dispatch, self.sender, "exp@example.com")
        self.clock.advance(timedelta(days=31, seconds=1))
        status, body, _ = _get(self.dispatch, "/api/auth/me", cookie=cookie)
        self.assertFalse(body["access"])
        self.assertEqual(body["reason"], "guest_expired")

    def test_logout_revokes_session(self):
        cookie = _full_signin(self.dispatch, self.sender, "lo@example.com")
        _post(self.dispatch, "/api/auth/logout", {}, cookie=cookie)
        status, body, _ = _get(self.dispatch, "/api/auth/me", cookie=cookie)
        self.assertFalse(body["authenticated"])

    def test_invite_only_gp(self):
        status, body, _ = _post(self.dispatch, "/api/auth/invite", {"email": "lp@example.com"})
        self.assertEqual(status, "403 Forbidden")

        cookie = _full_signin(self.dispatch, self.sender, self.gp)
        status, body, _ = _post(
            self.dispatch, "/api/auth/invite", {"email": "lp@example.com"}, cookie=cookie
        )
        self.assertEqual(status, "201 Created")
        self.assertTrue(body["token"])
        member = self.store.get_member("lp@example.com")
        self.assertEqual(member["role"], "LP")

    def test_cap_reports_lp_count(self):
        # promote LPs then check cap endpoint as GP
        for i in range(5):
            self.store.promote_to_lp(f"lp{i}@example.com")
        cookie = _full_signin(self.dispatch, self.sender, self.gp)
        status, body, _ = _get(self.dispatch, "/api/auth/cap", cookie=cookie)
        self.assertEqual(status, "200 OK")
        self.assertEqual(body["lp_count"], 5)
        self.assertEqual(body["max_lp"], MAX_LP_MEMBERS)

    def test_gp_sees_member_roster_and_cap(self):
        self.store.promote_to_lp("lp1@example.com")
        self.store.set_subscribed("sub@example.com")
        cookie = _full_signin(self.dispatch, self.sender, self.gp)
        status, body, _ = _get(self.dispatch, "/api/auth/members", cookie=cookie)
        self.assertEqual(status, "200 OK")
        self.assertEqual(body["lp_count"], 1)
        self.assertEqual(body["max_lp"], MAX_LP_MEMBERS)
        self.assertIn("counts", body)
        self.assertGreaterEqual(body["total"], 3)  # gp + lp + member
        roles = {m["email"]: m["role"] for m in body["members"]}
        self.assertEqual(roles.get("lp1@example.com"), "LP")
        self.assertEqual(roles.get("sub@example.com"), "MEMBER")

    def test_member_roster_denied_for_non_gp(self):
        cookie = _full_signin(self.dispatch, self.sender, "notgp@example.com")
        status, body, _ = _get(self.dispatch, "/api/auth/members", cookie=cookie)
        self.assertEqual(status, "403 Forbidden")

    def test_member_roster_denied_when_unauthenticated(self):
        status, body, _ = _get(self.dispatch, "/api/auth/members")
        self.assertEqual(status, "403 Forbidden")

    # ---- the GP identity (GP_EMAIL) ----------------------------------------
    # The GP is configured by environment, not by a stored invite, so the
    # member row is created as a GUEST on first sign-in. The console gates its
    # GP panel on the role reported here, so every surface must agree.

    def test_gp_signs_in_as_gp_not_guest(self):
        cookie = _full_signin(self.dispatch, self.sender, self.gp)
        status, body, _ = _get(self.dispatch, "/api/auth/me", cookie=cookie)
        self.assertEqual(status, "200 OK")
        self.assertEqual(body["role"], "GP")
        self.assertTrue(body["access"])

    def test_verify_reports_gp_role_for_the_gp(self):
        _post(self.dispatch, "/api/auth/request", {"email": self.gp})
        code = self.sender.sent[-1]["body"].split("code is:\n\n")[1].split("\n")[0].strip()
        status, body, _ = _post(
            self.dispatch, "/api/auth/verify", {"email": self.gp, "code": code}
        )
        self.assertEqual(status, "200 OK")
        self.assertEqual(body["role"], "GP")

    def test_gp_gets_full_tier_and_real_data(self):
        cookie = _full_signin(self.dispatch, self.sender, self.gp)
        status, body, _ = _get(self.dispatch, "/api/tier", cookie=cookie)
        self.assertEqual(body["tier"], "full")
        self.assertTrue(body["real_data"])
        self.assertTrue(body["investor"])
        status, body, _ = _get(self.dispatch, "/api/data/real", cookie=cookie)
        self.assertEqual(status, "200 OK")

    def test_gp_identity_is_recorded_in_the_store(self):
        self.assertEqual(self.store.get_member(self.gp)["role"], "GP")
        cookie = _full_signin(self.dispatch, self.sender, self.gp)
        status, body, _ = _get(self.dispatch, "/api/auth/members", cookie=cookie)
        roles = {m["email"]: m["role"] for m in body["members"]}
        self.assertEqual(roles.get(self.gp), "GP")

    def test_gp_role_resolved_even_when_the_stored_row_lags(self):
        """A stale GUEST row must not hide the operator's console."""
        self.store._conn.execute(
            "UPDATE members SET role=? WHERE email=?", ("GUEST", self.gp)
        )
        self.store._conn.commit()
        self.assertEqual(self.store.get_member(self.gp)["role"], "GUEST")
        cookie = _full_signin(self.dispatch, self.sender, self.gp)
        status, body, _ = _get(self.dispatch, "/api/auth/me", cookie=cookie)
        self.assertEqual(body["role"], "GP")

    def test_non_gp_member_is_never_promoted_to_gp(self):
        email = "someone@example.com"
        cookie = _full_signin(self.dispatch, self.sender, email)
        status, body, _ = _get(self.dispatch, "/api/auth/me", cookie=cookie)
        self.assertEqual(body["role"], "GUEST")
        self.assertEqual(self.store.get_member(email)["role"], "GUEST")
        status, body, _ = _get(self.dispatch, "/api/tier", cookie=cookie)
        self.assertEqual(body["tier"], "synthetic")
        self.assertFalse(body["real_data"])

    def test_subscribe_upgrades_to_member(self):
        cookie = _full_signin(self.dispatch, self.sender, "sub@example.com")
        status, body, _ = _post(
            self.dispatch, "/api/auth/subscribe", {"email": "sub@example.com"}, cookie=cookie
        )
        self.assertEqual(status, "200 OK")
        self.assertEqual(body["role"], "MEMBER")
        member = self.store.get_member("sub@example.com")
        self.assertEqual(member["role"], "MEMBER")
        self.assertTrue(member["subscribed"])

    def test_subscribe_requires_auth_as_that_email(self):
        _full_signin(self.dispatch, self.sender, "a@example.com")
        # another user tries to subscribe a@example.com -> denied
        status, body, _ = _post(self.dispatch, "/api/auth/subscribe", {"email": "a@example.com"})
        self.assertEqual(status, "403 Forbidden")


class SocialLoginEndpointTests(unittest.TestCase):
    def setUp(self):
        import base64, hashlib, hmac, json, time

        self._b64 = lambda o: base64.urlsafe_b64encode(json.dumps(o).encode()).rstrip(b"=").decode()
        self._hmac = hmac
        self._sha = hashlib
        self._time = time

        self.tmp = tempfile.mkdtemp()
        self.store = MembershipStore(
            os.path.join(self.tmp, "s.db"), clock=FakeClock(), secret="test-secret"
        )
        from hedge_desk.auth_app import make_auth_app
        from hedge_desk.supabase_auth import SupabaseJwtVerifier

        self.SECRET = "jwt-secret"
        self.verifier = SupabaseJwtVerifier(self.SECRET)
        self.dispatch = make_auth_app(
            self.store,
            sender=CaptureSender(),
            gp_email="gp@x.com",
            jwt_verifier=self.verifier,
        )

    def tearDown(self):
        self.store.close()

    def _token(self, email="social@example.com"):
        import base64

        header = {"alg": "HS256", "typ": "JWT"}
        payload = {"email": email, "aud": "authenticated", "exp": int(self._time.time()) + 3600}
        signing = f"{self._b64(header)}.{self._b64(payload)}".encode()
        sig = base64.urlsafe_b64encode(
            self._hmac.new(self.SECRET.encode(), signing, self._sha.sha256).digest()
        ).rstrip(b"=").decode()
        return f"{self._b64(header)}.{self._b64(payload)}.{sig}"

    def test_social_login_valid_token_issues_session(self):
        status, body, headers = _post(
            self.dispatch, "/api/auth/social", {"access_token": self._token("new@example.com")}
        )
        self.assertEqual(status, "200 OK")
        self.assertEqual(body["role"], "GUEST")
        self.assertEqual(body["email"], "new@example.com")
        self.assertIsNotNone(_extract_cookie(headers))
        # membership record created
        self.assertIsNotNone(self.store.get_member("new@example.com"))

    def test_social_login_rejects_bad_token(self):
        status, body, _ = _post(self.dispatch, "/api/auth/social", {"access_token": "garbage"})
        self.assertEqual(status, "401 Unauthorized")
        self.assertEqual(body["error"], "invalid_token")

    def test_social_login_missing_token(self):
        status, body, _ = _post(self.dispatch, "/api/auth/social", {})
        self.assertEqual(status, "400 Bad Request")

    def test_social_login_not_configured_returns_503(self):
        from hedge_desk.auth_app import make_auth_app
        from tests.test_auth_app import CaptureSender as CS

        disp = make_auth_app(self.store, sender=CS(), gp_email="gp@x.com", jwt_verifier=None)
        status, body, _ = _post(disp, "/api/auth/social", {"access_token": self._token()})
        self.assertEqual(status, "503 Service Unavailable")
        self.assertEqual(body["error"], "social_login_not_configured")

    def test_social_login_preserves_existing_lp_role(self):
        self.store.promote_to_lp("lp@example.com")
        status, body, _ = _post(
            self.dispatch, "/api/auth/social", {"access_token": self._token("lp@example.com")}
        )
        self.assertEqual(status, "200 OK")
        self.assertEqual(body["role"], "LP")

    def test_providers_endpoint_reports_config(self):
        status, body, _ = _get(self.dispatch, "/api/auth/providers")
        self.assertEqual(status, "200 OK")
        self.assertIn("enabled", body)
        self.assertIn("providers", body)


class BrokerEndpointTests(unittest.TestCase):
    def setUp(self):
        import tempfile

        from hedge_desk.auth_app import make_auth_app
        from hedge_desk.broker_link import BrokerLinkStore, BrokerAdapter
        from hedge_desk.brokers.schwab_oauth import SchwabOAuth, SchwabOAuthConfig

        self.tmp = tempfile.mkdtemp()
        self.store = MembershipStore(
            os.path.join(self.tmp, "b.db"), clock=FakeClock(), secret="test-secret"
        )
        self.broker_store = BrokerLinkStore(os.path.join(self.tmp, "bl.db"))
        self.key = b"broker-key"
        os.environ["BROKER_LINK_KEY"] = "broker-key"

        self.sender = CaptureSender()
        cfg = SchwabOAuthConfig("cid", "csecret", "https://site/api/broker/callback")
        tokens = {"access_token": "AT", "refresh_token": "RT", "expires_in": 1800, "scope": "readonly"}
        self.oauth = SchwabOAuth(cfg, transport=lambda m, u, h, b: (200, json.dumps(tokens).encode()))
        self.adapter = BrokerAdapter("schwab")

        self.dispatch = make_auth_app(
            self.store,
            sender=self.sender,
            gp_email="gp@x.com",
            broker_store=self.broker_store,
            broker_oauth=self.oauth,
            broker_adapter=self.adapter,
        )

    def tearDown(self):
        self.store.close()
        self.broker_store.close()
        os.environ.pop("BROKER_LINK_KEY", None)

    def sender_for_member(self):
        return self.sender

    def test_guest_denied_broker_authorize(self):
        cookie = _full_signin(self.dispatch, self.sender_for_member(), "guest@example.com")
        status, body, _ = _get(self.dispatch, "/api/broker/authorize", cookie=cookie)
        self.assertEqual(status, "403 Forbidden")
        self.assertEqual(body["error"], "broker_requires_member")

    def test_member_gets_authorize_url_with_state(self):
        cookie = _full_signin(self.dispatch, self.sender_for_member(), "m@example.com")
        self.store.set_subscribed("m@example.com")
        status, body, _ = _get(self.dispatch, "/api/broker/authorize", cookie=cookie)
        self.assertEqual(status, "200 OK")
        self.assertIn("authorize_url", body)
        self.assertIn("state=", body["authorize_url"])
        self.assertIn("scope=readonly", body["authorize_url"])

    def test_link_requires_valid_state(self):
        cookie = _full_signin(self.dispatch, self.sender_for_member(), "m@example.com")
        self.store.set_subscribed("m@example.com")
        status, body, _ = _post(
            self.dispatch, "/api/broker/link", {"code": "C", "state": "bogus"}, cookie=cookie
        )
        self.assertEqual(status, "400 Bad Request")
        self.assertEqual(body["error"], "invalid_state")

    def test_link_with_valid_state_stores_connection_read_only(self):
        cookie = _full_signin(self.dispatch, self.sender_for_member(), "m@example.com")
        self.store.set_subscribed("m@example.com")
        # get a real state from the authorize endpoint
        _, auth_body, _ = _get(self.dispatch, "/api/broker/authorize", cookie=cookie)
        state = auth_body["authorize_url"].split("state=")[1].split("&")[0]
        status, body, _ = _post(
            self.dispatch, "/api/broker/link", {"code": "C", "state": state, "account_label": "Main"}, cookie=cookie
        )
        self.assertEqual(status, "200 OK")
        self.assertTrue(body["read_only"])
        conn = self.broker_store.connection("m@example.com")
        self.assertTrue(conn["linked"])
        self.assertEqual(conn["broker"], "schwab")

    def test_status_reports_configured_and_linked(self):
        cookie = _full_signin(self.dispatch, self.sender_for_member(), "m@example.com")
        self.store.set_subscribed("m@example.com")
        status, body, _ = _get(self.dispatch, "/api/broker/status", cookie=cookie)
        self.assertEqual(status, "200 OK")
        self.assertTrue(body["configured"])
        self.assertFalse(body["linked"])

    def test_positions_requires_link(self):
        cookie = _full_signin(self.dispatch, self.sender_for_member(), "m@example.com")
        self.store.set_subscribed("m@example.com")
        status, body, _ = _get(self.dispatch, "/api/broker/positions", cookie=cookie)
        self.assertEqual(status, "409 Conflict")
        self.assertEqual(body["error"], "no_broker_linked")

    def test_unlink(self):
        cookie = _full_signin(self.dispatch, self.sender_for_member(), "m@example.com")
        self.store.set_subscribed("m@example.com")
        _, auth_body, _ = _get(self.dispatch, "/api/broker/authorize", cookie=cookie)
        state = auth_body["authorize_url"].split("state=")[1].split("&")[0]
        _post(self.dispatch, "/api/broker/link", {"code": "C", "state": state}, cookie=cookie)
        _post(self.dispatch, "/api/broker/unlink", {}, cookie=cookie)
        self.assertFalse(self.broker_store.connection("m@example.com")["linked"])

    def test_broker_requires_auth(self):
        status, body, _ = _get(self.dispatch, "/api/broker/status")
        self.assertEqual(status, "403 Forbidden")


if __name__ == "__main__":
    unittest.main()
