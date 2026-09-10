"""Read-only Schwab brokerage adapter.

Implements the broker-link `BrokerAdapter` interface against Schwab's Trader
API, READ-ONLY. It exposes account balances and positions only.

Hard constraints:
- No order placement. There is no submit/cancel/replace code path here, and a
  test asserts the module contains no mutating HTTP verbs against the broker.
- Tokens are passed in by the caller (resolved from the encrypted broker-link
  record); this module never persists credentials.
- Every result is explicitly tagged ``read_only`` so a caller can never mistake
  it for an executable action.
- Fail closed: any HTTP/parse error yields a structured error dict, never
  invented data.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Callable, Optional

SCHWAB_API_BASE = "https://api.schwabapi.com"

# transport(method, url, headers) -> (status:int, body:bytes)
Transport = Callable[[str, str, dict], "tuple[int, bytes]"]


def _default_transport(method, url, headers):
    req = urllib.request.Request(url, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()


class SchwabReadOnlyBroker:
    """Schwab Trader API, read-only: balances + positions."""

    name = "schwab"

    def __init__(self, transport: Optional[Transport] = None, base_url: str = SCHWAB_API_BASE):
        self._transport = transport or _default_transport
        self.base_url = base_url.rstrip("/")

    def _get(self, path: str, token: str) -> dict:
        if not token:
            return {"status": "error", "error": "missing_token", "read_only": True}
        url = self.base_url + path
        headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
        try:
            status, raw = self._transport("GET", url, headers)
        except Exception as exc:  # network / transport failure -> fail closed
            return {"status": "error", "error": f"transport:{exc}", "read_only": True}
        if status >= 400:
            return {"status": "error", "http_status": status, "read_only": True}
        try:
            return {"status": "ok", "read_only": True, "data": json.loads(raw or b"{}")}
        except Exception:
            return {"status": "error", "error": "bad_json", "read_only": True}

    def account_numbers(self, token: str) -> dict:
        """List the account numbers the token can read (read-only)."""
        result = self._get("/trader/v1/accounts/accountNumbers", token)
        if result["status"] != "ok":
            return result
        numbers = [a.get("accountNumber") for a in result["data"]]
        return {"status": "ok", "read_only": True, "account_numbers": numbers}

    def positions(self, token: str, account_number: str = "") -> dict:
        """Read positions for an account (read-only)."""
        if not account_number:
            return {"status": "error", "error": "missing_account_number", "read_only": True}
        result = self._get(
            f"/trader/v1/accounts/{account_number}?fields=positions", token
        )
        if result["status"] != "ok":
            return result
        return {"status": "ok", "read_only": True, "positions": result["data"]}

    def balances(self, token: str, account_number: str = "") -> dict:
        """Read balances for an account (read-only)."""
        if not account_number:
            return {"status": "error", "error": "missing_account_number", "read_only": True}
        result = self._get(
            f"/trader/v1/accounts/{account_number}?fields=positions", token
        )
        if result["status"] != "ok":
            return result
        return {"status": "ok", "read_only": True, "balances": result["data"]}


__all__ = ["SchwabReadOnlyBroker", "SCHWAB_API_BASE"]
