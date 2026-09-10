import base64
import hashlib
import hmac
import json
import time
import unittest

from hedge_desk.supabase_auth import SupabaseJwtVerifier, verifier_from_env


def _b64(obj) -> str:
    return base64.urlsafe_b64encode(json.dumps(obj).encode()).rstrip(b"=").decode()


def make_token(secret: str, *, email="user@example.com", exp_delta=3600, aud="authenticated", alg="HS256"):
    header = {"alg": alg, "typ": "JWT"}
    payload = {"email": email, "aud": aud, "exp": int(time.time()) + exp_delta, "sub": "abc"}
    signing_input = f"{_b64(header)}.{_b64(payload)}".encode()
    sig = base64.urlsafe_b64encode(
        hmac.new(secret.encode(), signing_input, hashlib.sha256).digest()
    ).rstrip(b"=").decode()
    return f"{_b64(header)}.{_b64(payload)}.{sig}"


class SupabaseJwtTests(unittest.TestCase):
    SECRET = "super-secret-jwt"

    def setUp(self):
        self.verifier = SupabaseJwtVerifier(self.SECRET)

    def test_valid_token_verifies_and_yields_email(self):
        token = make_token(self.SECRET, email="a@b.com")
        claims = self.verifier.verify(token)
        self.assertIsNotNone(claims)
        self.assertEqual(claims["email"], "a@b.com")
        self.assertEqual(self.verifier.email_from(token), "a@b.com")

    def test_wrong_secret_rejected(self):
        token = make_token("other-secret")
        self.assertIsNone(self.verifier.verify(token))

    def test_tampered_payload_rejected(self):
        token = make_token(self.SECRET)
        header, payload, sig = token.split(".")
        forged = _b64({"email": "attacker@evil.com", "aud": "authenticated", "exp": int(time.time()) + 3600})
        tamp = f"{header}.{forged}.{sig}"
        self.assertIsNone(self.verifier.verify(tamp))

    def test_expired_token_rejected(self):
        token = make_token(self.SECRET, exp_delta=-10)
        self.assertIsNone(self.verifier.verify(token))

    def test_wrong_audience_rejected(self):
        token = make_token(self.SECRET, aud="anon")
        self.assertIsNone(self.verifier.verify(token))

    def test_none_alg_rejected(self):
        token = make_token(self.SECRET, alg="none")
        self.assertIsNone(self.verifier.verify(token))

    def test_malformed_token_rejected(self):
        for bad in ("", "a.b", "not-a-token", "a.b.c.d"):
            self.assertIsNone(self.verifier.verify(bad))

    def test_missing_email_rejected(self):
        header = _b64({"alg": "HS256"})
        payload = _b64({"aud": "authenticated", "exp": int(time.time()) + 3600})
        signing_input = f"{header}.{payload}".encode()
        sig = base64.urlsafe_b64encode(
            hmac.new(self.SECRET.encode(), signing_input, hashlib.sha256).digest()
        ).rstrip(b"=").decode()
        self.assertIsNone(self.verifier.verify(f"{header}.{payload}.{sig}"))

    def test_verifier_from_env(self):
        self.assertIsNone(verifier_from_env({}))
        v = verifier_from_env({"SUPABASE_JWT_SECRET": self.SECRET})
        self.assertIsNotNone(v)

    def test_requires_secret(self):
        with self.assertRaises(ValueError):
            SupabaseJwtVerifier("")


if __name__ == "__main__":
    unittest.main()
