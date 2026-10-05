"""Schwab OAuth for linking a member's brokerage account.

Implements Schwab's documented authorization-code flow. Production OAuth
authorization is tied to the approved App/API product; the authorization URL
does not request a ``scope`` query parameter and token responses report
``scope=api``. Live order use remains independently disabled by default.

Config comes from the environment (server-side only):
  SCHWAB_CLIENT_ID, SCHWAB_CLIENT_SECRET, SCHWAB_REDIRECT_URI
  SCHWAB_AUTHORIZE_URL (default  https://api.schwabapi.com/v1/oauth/authorize)
  SCHWAB_TOKEN_URL     (default  https://api.schwabapi.com/v1/oauth/token)

Security posture:
- client_secret is never logged or returned.
- state is generated per attempt and must round-trip; callers verify it.
- The HTTP transport is injectable for deterministic tests.
- Fail closed: any error yields a structured error, never a fabricated token.
"""

from __future__ import annotations

import base64
import json
import os
import secrets
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any, Callable, Optional

DEFAULT_AUTHORIZE_URL = "https://api.schwabapi.com/v1/oauth/authorize"
DEFAULT_TOKEN_URL = "https://api.schwabapi.com/v1/oauth/token"

# transport(method, url, headers, body) -> (status:int, body:bytes)
Transport = Callable[[str, str, dict, Optional[bytes]], "tuple[int, bytes]"]


def _default_transport(method, url, headers, body):
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()


@dataclass
class SchwabOAuthConfig:
    client_id: str
    client_secret: str
    redirect_uri: str
    authorize_url: str = DEFAULT_AUTHORIZE_URL
    token_url: str = DEFAULT_TOKEN_URL

    @classmethod
    def from_environment(cls, env: Optional[dict] = None) -> "SchwabOAuthConfig":
        source = env if env is not None else os.environ
        return cls(
            client_id=str(source.get("SCHWAB_CLIENT_ID", "")).strip(),
            client_secret=str(source.get("SCHWAB_CLIENT_SECRET", "")).strip(),
            redirect_uri=str(source.get("SCHWAB_REDIRECT_URI", "")).strip(),
            authorize_url=str(source.get("SCHWAB_AUTHORIZE_URL", DEFAULT_AUTHORIZE_URL)).strip(),
            token_url=str(source.get("SCHWAB_TOKEN_URL", DEFAULT_TOKEN_URL)).strip(),
        )

    @property
    def configured(self) -> bool:
        if not (self.client_id and self.client_secret and self.redirect_uri):
            return False
        redirect = urllib.parse.urlparse(self.redirect_uri)
        authorize = urllib.parse.urlparse(self.authorize_url)
        token = urllib.parse.urlparse(self.token_url)
        return (
            redirect.scheme == "https"
            and bool(redirect.hostname)
            and not redirect.fragment
            and authorize.scheme == "https"
            and authorize.hostname == "api.schwabapi.com"
            and authorize.path == "/v1/oauth/authorize"
            and not authorize.fragment
            and token.scheme == "https"
            and token.hostname == "api.schwabapi.com"
            and token.path == "/v1/oauth/token"
            and not token.fragment
        )


class SchwabOAuth:
    """Schwab OAuth: build the documented authorize URL and exchange tokens."""

    name = "schwab"

    def __init__(self, config: SchwabOAuthConfig, transport: Optional[Transport] = None):
        self.config = config
        self._transport = transport or _default_transport

    def new_state(self) -> str:
        """Generate a CSRF state value; the caller must store and verify it."""
        return secrets.token_urlsafe(24)

    def authorize_url(self, state: str) -> str:
        """Build Schwab's documented authorization URL."""
        if not self.config.configured:
            raise ValueError("Schwab OAuth is not configured")
        if not state or not state.strip():
            raise ValueError("OAuth state is required")
        params = {
            "client_id": self.config.client_id,
            "redirect_uri": self.config.redirect_uri,
            "response_type": "code",
            "state": state,
        }
        return f"{self.config.authorize_url}?{urllib.parse.urlencode(params)}"

    def exchange_code(self, code: str) -> dict:
        """Exchange an authorization code for tokens. Returns a dict; never logs secrets."""
        if not self.config.configured:
            return {"status": "error", "error": "schwab_oauth_not_configured"}
        if not code:
            return {"status": "error", "error": "missing_code"}
        body = urllib.parse.urlencode(
            {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": self.config.redirect_uri,
            }
        ).encode("utf-8")
        basic = base64.b64encode(
            f"{self.config.client_id}:{self.config.client_secret}".encode("utf-8")
        ).decode("ascii")
        headers = {
            "Authorization": f"Basic {basic}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        try:
            status, raw = self._transport("POST", self.config.token_url, headers, body)
        except Exception:
            return {"status": "error", "error": "transport_failure"}
        if status >= 400:
            return {"status": "error", "http_status": status}
        return self._parse_token_response(raw)

    def refresh_access_token(self, refresh_token: str) -> dict:
        """Refresh an access token; caller must persist the result before API use."""
        if not self.config.configured:
            return {"status": "error", "error": "schwab_oauth_not_configured"}
        if not refresh_token:
            return {"status": "error", "error": "missing_refresh_token"}
        body = urllib.parse.urlencode(
            {"grant_type": "refresh_token", "refresh_token": refresh_token}
        ).encode("utf-8")
        basic = base64.b64encode(
            f"{self.config.client_id}:{self.config.client_secret}".encode("utf-8")
        ).decode("ascii")
        headers = {
            "Authorization": f"Basic {basic}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        try:
            status, raw = self._transport("POST", self.config.token_url, headers, body)
        except Exception:
            return {"status": "error", "error": "transport_failure"}
        if status in (400, 401):
            return {"status": "error", "error": "reauthentication_required", "http_status": status}
        if status == 429:
            return {"status": "error", "error": "throttled", "http_status": status}
        if status >= 400:
            return {"status": "error", "http_status": status}
        return self._parse_token_response(raw)

    @staticmethod
    def _parse_token_response(raw: bytes) -> dict:
        try:
            data: Any = json.loads(raw or b"{}")
        except (TypeError, ValueError, UnicodeDecodeError):
            return {"status": "error", "error": "bad_json"}
        if not isinstance(data, dict):
            return {"status": "error", "error": "unexpected_response_schema"}
        access = data.get("access_token")
        expires_in = data.get("expires_in")
        if not isinstance(access, str) or not access:
            return {"status": "error", "error": "no_access_token"}
        if isinstance(expires_in, bool) or not isinstance(expires_in, (int, float)) or expires_in <= 0:
            return {"status": "error", "error": "invalid_expiry"}
        refresh = data.get("refresh_token", "")
        scope = data.get("scope", "api")
        token_type = data.get("token_type", "Bearer")
        if not isinstance(refresh, str) or not isinstance(scope, str) or not isinstance(token_type, str):
            return {"status": "error", "error": "unexpected_response_schema"}
        return {
            "status": "ok",
            "access_token": access,
            "refresh_token": refresh,
            "expires_in": expires_in,
            "token_type": token_type,
            "scope": scope,
        }


__all__ = [
    "SchwabOAuth",
    "SchwabOAuthConfig",
    "DEFAULT_AUTHORIZE_URL",
    "DEFAULT_TOKEN_URL",
]
