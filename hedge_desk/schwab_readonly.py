"""Secret-safe Schwab OAuth boundary with no trading or order capability."""

import base64
import json
import os
import secrets
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping, Optional


AUTHORIZE_URL = "https://api.schwabapi.com/v1/oauth/authorize"
TOKEN_URL = "https://api.schwabapi.com/v1/oauth/token"
TRADER_API_URL = "https://api.schwabapi.com/trader/v1"


@dataclass(frozen=True)
class SchwabConfig:
    client_id: str
    client_secret: str
    redirect_uri: str
    token_path: Path

    @classmethod
    def from_environment(cls) -> "SchwabConfig":
        return cls(
            os.environ.get("SCHWAB_CLIENT_ID", "").strip(),
            os.environ.get("SCHWAB_CLIENT_SECRET", "").strip(),
            os.environ.get("SCHWAB_REDIRECT_URI", "http://127.0.0.1:8765/api/schwab/callback").strip(),
            Path(os.environ.get("SCHWAB_TOKEN_PATH", "config/schwab.tokens.local.json")),
        )


class SchwabReadOnlyClient:
    """OAuth and GET-only account client; deliberately exposes no order method."""

    def __init__(self, config: SchwabConfig) -> None:
        self.config = config
        self._pending_states = set()

    def readiness(self) -> Mapping[str, object]:
        return {
            "client_id_configured": bool(self.config.client_id),
            "client_secret_configured": bool(self.config.client_secret),
            "redirect_uri_configured": bool(self.config.redirect_uri),
            "ready_for_authorization_url": bool(
                self.config.client_id and self.config.client_secret and self.config.redirect_uri
            ),
            "token_present": self.config.token_path.is_file(),
            "access_mode": "READ_ONLY",
            "orders_blocked": True,
        }

    def authorization_url(self) -> str:
        if not self.readiness()["ready_for_authorization_url"]:
            raise ValueError("Schwab OAuth configuration is incomplete")
        state = secrets.token_urlsafe(32)
        self._pending_states.add(state)
        query = urllib.parse.urlencode({
            "client_id": self.config.client_id,
            "redirect_uri": self.config.redirect_uri,
            "state": state,
        })
        return AUTHORIZE_URL + "?" + query

    def exchange_callback(self, code: str, state: str) -> Mapping[str, object]:
        if not code or state not in self._pending_states:
            raise PermissionError("Schwab OAuth callback state is invalid")
        self._pending_states.remove(state)
        credentials = base64.b64encode(
            f"{self.config.client_id}:{self.config.client_secret}".encode("utf-8")
        ).decode("ascii")
        body = urllib.parse.urlencode({
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.config.redirect_uri,
        }).encode("ascii")
        request = urllib.request.Request(
            TOKEN_URL, data=body, method="POST",
            headers={
                "Authorization": "Basic " + credentials,
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
            },
        )
        with urllib.request.urlopen(request, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
        if not isinstance(payload, dict) or not payload.get("access_token"):
            raise ValueError("Schwab token response is invalid")
        stored = dict(payload)
        stored["received_at"] = datetime.now(timezone.utc).isoformat()
        self.config.token_path.parent.mkdir(parents=True, exist_ok=True)
        descriptor = os.open(
            self.config.token_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600
        )
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(stored, stream, sort_keys=True, separators=(",", ":"))
        return {"connected": True, "access_mode": "READ_ONLY", "orders_blocked": True}

    def account_numbers(self) -> object:
        token = self._access_token()
        request = urllib.request.Request(
            TRADER_API_URL + "/accounts/accountNumbers",
            method="GET",
            headers={"Authorization": "Bearer " + token, "Accept": "application/json"},
        )
        with urllib.request.urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))

    def _access_token(self) -> str:
        try:
            payload = json.loads(self.config.token_path.read_text(encoding="utf-8"))
            token = payload["access_token"]
        except (OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
            raise PermissionError("Schwab read-only token is unavailable") from exc
        if not isinstance(token, str) or not token:
            raise PermissionError("Schwab read-only token is unavailable")
        return token
