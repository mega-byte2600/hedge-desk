"""Verify Supabase Auth JWTs for social-login sign-in.

Supabase Auth (GoTrue) handles identity: Google/GitHub/Microsoft/Apple OAuth
returns a signed JWT. This module verifies that JWT server-side so the desk can
trust the resulting email, then map it to a membership role/tier.

Design:
- HS256 verification with the Supabase JWT secret (Supabase's default for
  projects using the shared JWT secret). RS256/JWKS is a follow-up.
- stdlib only (hmac/hashlib/base64) — no new dependency.
- Fail closed: any malformed token, bad signature, expired exp, or wrong
  audience returns None. Never partial-trust a token.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import time
import urllib.error
import urllib.request
from typing import Callable, Optional


def _b64url_decode(segment: str) -> bytes:
    padding = "=" * (-len(segment) % 4)
    return base64.urlsafe_b64decode(segment + padding)


def _sign(message: bytes, secret: bytes) -> str:
    return base64.urlsafe_b64encode(
        hmac.new(secret, message, hashlib.sha256).digest()
    ).rstrip(b"=").decode("ascii")


class SupabaseJwtVerifier:
    """Verify a Supabase-issued JWT and return its claims (or None)."""

    def __init__(
        self,
        jwt_secret: str,
        *,
        audience: str = "authenticated",
        clock: Optional[Callable[[], int]] = None,
    ) -> None:
        if not jwt_secret:
            raise ValueError("SupabaseJwtVerifier requires the project JWT secret")
        self._secret = jwt_secret.encode("utf-8")
        self.audience = audience
        self._now = clock or (lambda: int(time.time()))

    def verify(self, token: str) -> Optional[dict]:
        """Return verified claims, or None if the token is not trustworthy."""
        if not token or token.count(".") != 2:
            return None
        try:
            header_b64, payload_b64, signature = token.split(".")
            header = json.loads(_b64url_decode(header_b64))
            if header.get("alg") != "HS256":
                return None
            expected = _sign(f"{header_b64}.{payload_b64}".encode("ascii"), self._secret)
            if not hmac.compare_digest(expected, signature):
                return None
            claims = json.loads(_b64url_decode(payload_b64))
        except Exception:
            return None
        # expiry
        exp = claims.get("exp")
        if exp is None or int(exp) <= int(self._now()):
            return None
        # audience (Supabase uses 'authenticated' for signed-in users)
        aud = claims.get("aud")
        if self.audience and aud and aud != self.audience:
            return None
        # require an email to map to a membership record
        if not claims.get("email"):
            return None
        return claims

    def email_from(self, token: str) -> Optional[str]:
        claims = self.verify(token)
        if not claims:
            return None
        return str(claims["email"]).strip().lower()


class SupabaseRemoteVerifier:
    """Validate a Supabase access token through the project's Auth API."""

    def __init__(
        self,
        url: str,
        publishable_key: str,
        *,
        transport=None,
    ) -> None:
        self.url = url.rstrip("/")
        self.publishable_key = publishable_key
        self._transport = transport or self._default_transport

    @staticmethod
    def _default_transport(request: urllib.request.Request):
        try:
            with urllib.request.urlopen(request, timeout=8) as response:
                return response.status, response.read()
        except urllib.error.HTTPError as exc:
            return exc.code, exc.read()
        except Exception:
            return 0, b""

    def email_from(self, token: str) -> Optional[str]:
        if not token or not self.url or not self.publishable_key:
            return None
        request = urllib.request.Request(
            self.url + "/auth/v1/user",
            headers={
                "apikey": self.publishable_key,
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
            },
        )
        status, raw = self._transport(request)
        if status != 200 or not raw:
            return None
        try:
            payload = json.loads(raw.decode("utf-8"))
        except Exception:
            return None
        email = str(payload.get("email", "")).strip().lower()
        return email or None


def verifier_from_env(env: Optional[dict] = None):
    """Build the strongest available Supabase verifier from environment."""
    source = env if env is not None else os.environ
    secret = str(source.get("SUPABASE_JWT_SECRET", "")).strip()
    if secret:
        return SupabaseJwtVerifier(secret)
    url = str(source.get("SUPABASE_URL", "")).strip()
    key = (
        str(source.get("SUPABASE_PUBLISHABLE_KEY", "")).strip()
        or str(source.get("SUPABASE_ANON_KEY", "")).strip()
    )
    if url and key:
        return SupabaseRemoteVerifier(url, key)
    return None


__all__ = ["SupabaseJwtVerifier", "SupabaseRemoteVerifier", "verifier_from_env"]
