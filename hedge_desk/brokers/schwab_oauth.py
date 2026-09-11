"""Schwab OAuth (read-only) for linking a member's brokerage account.

Implements the authorization-code flow against Schwab's Trader API so a
MEMBER/LP can link their own account. Scopes are read-only; no order scope is
requested and no order endpoint is called anywhere in this module.

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
from typing import Callable, Optional

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
        return bool(self.client_id and self.client_secret and self.redirect_uri)


class SchwabOAuth:
    """Read-only Schwab OAuth: build the authorize URL, exchange the code."""

    name = "schwab"

    def __init__(self, config: SchwabOAuthConfig, transport: Optional[Transport] = None):
        self.config = config
        self._transport = transport or _default_transport

    def new_state(self) -> str:
        """Generate a CSRF state value; the caller must store and verify it."""
        return secrets.token_urlsafe(24)

    def authorize_url(self, state: str) -> str:
        """Build the provider authorize URL (read-only scope)."""
        if not self.config.configured:
            raise ValueError("Schwab OAuth is not configured")
        params = {
            "client_id": self.config.client_id,
            "redirect_uri": self.config.redirect_uri,
            "response_type": "code",
            "scope": "readonly",
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
        except Exception as exc:
            return {"status": "error", "error": f"transport:{exc}"}
        if status >= 400:
            return {"status": "error", "http_status": status}
        try:
            data = json.loads(raw or b"{}")
        except Exception:
            return {"status": "error", "error": "bad_json"}
        access = data.get("access_token")
        if not access:
            return {"status": "error", "error": "no_access_token"}
        return {
            "status": "ok",
            "access_token": access,
            "refresh_token": data.get("refresh_token", ""),
            "expires_in": data.get("expires_in"),
            "token_type": data.get("token_type", "Bearer"),
            "scope": data.get("scope", "readonly"),
        }


__all__ = ["SchwabOAuth", "SchwabOAuthConfig", "DEFAULT_AUTHORIZE_URL", "DEFAULT_TOKEN_URL"]
