"""Broker-link scaffold for the Emporion desk.

Lets a MEMBER or LP connect their own broker account so the desk can act on
the Emporion "compass" signal. This is deliberately READ-ONLY first: the
connection stores broker metadata and, once an adapter is wired, can read
positions/balances. Order placement is gated separately behind the
deterministic risk engine and is NOT enabled here.

Security posture:
- Broker credentials are never stored. A connection holds an encrypted
  reference (encrypted access token) plus non-secret metadata (broker name,
  account label). The encryption key comes from the environment
  (BROKER_LINK_KEY); if it is absent the store refuses to persist tokens.
- Fail closed: any missing/invalid state yields no connection and no access.
- Tiered: only MEMBER / LP / GP may link a broker; GUEST and unauthenticated
  callers are denied.

Real adapter hooks: a concrete broker (e.g. Schwab) adapter implements
``BrokerAdapter`` and is injected. Until one is wired, calls return
``not_connected`` / ``not_implemented`` rather than inventing data.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import secrets
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional

from cryptography.fernet import Fernet, InvalidToken

from hedge_desk.sqlite_thread import new_lock, open_connection, thread_safe
from hedge_desk.tier_access import can_access_real_data

BROKER_TABLE = """
CREATE TABLE IF NOT EXISTS broker_links (
    email         TEXT PRIMARY KEY,
    broker        TEXT NOT NULL,             -- e.g. 'schwab'
    account_label TEXT,
    token_enc     TEXT,                      -- encrypted token blob (never raw)
    created_at    TEXT NOT NULL,
    updated_at    TEXT NOT NULL
);
"""

# Role check: only real-data tiers (MEMBER/LP/GP) may link a broker.
_ROLES_ALLOWED = ("MEMBER", "LP", "GP")


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def _default_http_transport(method, url, headers, body):
    """Default PostgREST transport (stdlib urllib)."""
    import urllib.error
    import urllib.request

    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()


def _fernet(key: bytes) -> Fernet:
    """Derive a stable Fernet key from the server-side BROKER_LINK_KEY."""
    if not key:
        raise ValueError("broker encryption key is required")
    derived = hashlib.sha256(key).digest()
    return Fernet(base64.urlsafe_b64encode(derived))


def _encrypt_token(token: str, key: bytes) -> str:
    """Authenticated encryption for broker credential bundles."""
    encrypted = _fernet(key).encrypt(token.encode("utf-8")).decode("ascii")
    return "fernet:" + encrypted


def _decrypt_token(blob: str, key: bytes) -> Optional[str]:
    """Decrypt current Fernet blobs; accept legacy HMAC envelopes for migration."""
    try:
        if blob.startswith("fernet:"):
            return _fernet(key).decrypt(blob.split(":", 1)[1].encode("ascii")).decode("utf-8")
        # Legacy format from the read-only scaffold. Read it only so an existing
        # connection can be re-saved under Fernet on its next successful refresh.
        nonce, tag, token = blob.split(":", 2)
        expect = hmac.new(key, (nonce + token).encode("utf-8"), hashlib.sha256).hexdigest()
        return token if hmac.compare_digest(tag, expect) else None
    except (InvalidToken, ValueError, UnicodeDecodeError):
        return None


def _bundle_json(
    access_token: str,
    refresh_token: str = "",
    expires_at: str = "",
    account_hash: str = "",
    account_number: str = "",
) -> str:
    return json.dumps(
        {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_at": expires_at,
            "account_hash": account_hash,
            "account_number": account_number,
        },
        separators=(",", ":"),
        sort_keys=True,
    )


def _parse_bundle(raw: str) -> dict:
    try:
        data = json.loads(raw)
        if isinstance(data, dict) and data.get("access_token"):
            return data
    except Exception:
        pass
    # Backward compatibility for a pre-bundle stored access token.
    return {"access_token": raw, "refresh_token": "", "expires_at": "", "account_hash": "", "account_number": ""}


@thread_safe
class BrokerLinkStore:
    """SQLite-backed broker connections, scoped per member email."""

    def __init__(self, db_path: Path | str) -> None:
        self.db_path = str(db_path)
        # Served from a thread pool: one connection shared under one lock.
        self._lock = new_lock()
        self._conn = open_connection(self.db_path)
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.executescript(BROKER_TABLE)
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()

    def link(
        self,
        email: str,
        role: str,
        broker: str,
        token: str,
        account_label: str = "",
        key: Optional[bytes] = None,
        refresh_token: str = "",
        expires_at: str = "",
        account_hash: str = "",
        account_number: str = "",
    ) -> dict:
        """Store a broker connection for a member. Fail closed on tier or key."""
        if role.upper() not in _ROLES_ALLOWED:
            raise PermissionError("broker link requires member/LP/GP")
        if not key:
            key = (os.environ.get("BROKER_LINK_KEY") or "").encode("utf-8")
            if not key:
                raise ValueError("BROKER_LINK_KEY not set; refusing to store broker token")
        now = _utcnow()
        enc = _encrypt_token(_bundle_json(token, refresh_token, expires_at, account_hash, account_number), key)
        self._conn.execute(
            "INSERT INTO broker_links (email, broker, account_label, token_enc, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?) "
            "ON CONFLICT(email) DO UPDATE SET broker=excluded.broker, "
            "account_label=excluded.account_label, token_enc=excluded.token_enc, "
            "updated_at=excluded.updated_at",
            (email.lower(), broker, account_label, enc, now, now),
        )
        self._conn.commit()
        return {
            "email": email.lower(),
            "broker": broker,
            "account_label": account_label,
            "linked": True,
        }

    def connection(self, email: str) -> dict:
        """Return a connection descriptor (never the raw token)."""
        row = self._conn.execute(
            "SELECT broker, account_label, updated_at FROM broker_links WHERE email=?",
            (email.lower(),),
        ).fetchone()
        if not row:
            return {"linked": False}
        return {
            "linked": True,
            "broker": row[0],
            "account_label": row[1],
            "updated_at": row[2],
        }

    def credentials(self, email: str, key: Optional[bytes] = None) -> dict:
        """Return decrypted broker credentials for server-side adapter use only."""
        if not key:
            key = (os.environ.get("BROKER_LINK_KEY") or "").encode("utf-8")
        if not key:
            return {"status": "error", "error": "broker_key_missing"}
        row = self._conn.execute(
            "SELECT broker, account_label, token_enc FROM broker_links WHERE email=?",
            (email.lower(),),
        ).fetchone()
        if not row or not row[2]:
            return {"status": "error", "error": "no_broker_linked"}
        raw = _decrypt_token(row[2], key)
        if not raw:
            return {"status": "error", "error": "credential_decrypt_failed"}
        bundle = _parse_bundle(raw)
        bundle.update({"status": "ok", "broker": row[0], "account_label": row[1]})
        return bundle

    def unlink(self, email: str) -> None:
        self._conn.execute("DELETE FROM broker_links WHERE email=?", (email.lower(),))
        self._conn.commit()


@dataclass
class BrokerAdapter:
    """Interface a concrete broker adapter implements.

    Until a real adapter is injected, read/execute calls fail closed with
    ``not_implemented`` — the desk never invents broker data or executions.
    """

    name: str = "none"

    def positions(self, token: str) -> dict:
        return {"status": "not_implemented", "broker": self.name}

    def balances(self, token: str) -> dict:
        return {"status": "not_implemented", "broker": self.name}


class SupabaseBrokerLinkStore:
    """Broker connections persisted to Supabase so they survive redeploys.

    Same interface as ``BrokerLinkStore`` (link/connection/unlink) but backed
    by PostgREST over stdlib urllib. The transport is injectable for tests.
    """

    def __init__(self, url: str, service_key: str, transport=None) -> None:
        if not url or not service_key:
            raise ValueError("SupabaseBrokerLinkStore requires url and service_key")
        self.url = url.rstrip("/")
        self.service_key = service_key
        self._transport = transport or _default_http_transport

    def _headers(self, prefer: str = "") -> dict:
        headers = {
            "apikey": self.service_key,
            "Authorization": f"Bearer {self.service_key}",
            "Content-Type": "application/json",
        }
        if prefer:
            headers["Prefer"] = prefer
        return headers

    def _call(self, method, query="", body=None, prefer=""):
        url = f"{self.url}/rest/v1/broker_links"
        if query:
            url += "?" + query
        import json as _json
        import urllib.request as _ur

        data = _json.dumps(body).encode("utf-8") if body is not None else None
        status, raw = self._transport(method, url, self._headers(prefer), data)
        if status >= 400:
            raise RuntimeError(f"supabase broker_links {method} failed: {status}")
        if not raw:
            return []
        try:
            return _json.loads(raw)
        except Exception:
            return []

    def close(self) -> None:
        return None

    def link(
        self, email, role, broker, token, account_label="", key=None,
        refresh_token="", expires_at="", account_hash="", account_number=""
    ) -> dict:
        if str(role).upper() not in _ROLES_ALLOWED:
            raise PermissionError("broker link requires member/LP/GP")
        if not key:
            key = (os.environ.get("BROKER_LINK_KEY") or "").encode("utf-8")
            if not key:
                raise ValueError("BROKER_LINK_KEY not set; refusing to store broker token")
        now = _utcnow()
        enc = _encrypt_token(_bundle_json(token, refresh_token, expires_at, account_hash, account_number), key)
        self._call(
            "POST",
            body={
                "email": email.lower(),
                "broker": broker,
                "account_label": account_label,
                "token_enc": enc,
                "created_at": now,
                "updated_at": now,
            },
            prefer="resolution=merge-duplicates",
        )
        return {"email": email.lower(), "broker": broker, "account_label": account_label, "linked": True}

    def connection(self, email: str) -> dict:
        rows = self._call("GET", f"email=eq.{email.lower()}&select=broker,account_label,updated_at")
        if not rows:
            return {"linked": False}
        r = rows[0]
        return {
            "linked": True,
            "broker": r.get("broker"),
            "account_label": r.get("account_label"),
            "updated_at": r.get("updated_at"),
        }

    def credentials(self, email: str, key: Optional[bytes] = None) -> dict:
        if not key:
            key = (os.environ.get("BROKER_LINK_KEY") or "").encode("utf-8")
        if not key:
            return {"status": "error", "error": "broker_key_missing"}
        rows = self._call(
            "GET",
            f"email=eq.{email.lower()}&select=broker,account_label,token_enc",
        )
        if not rows or not rows[0].get("token_enc"):
            return {"status": "error", "error": "no_broker_linked"}
        raw = _decrypt_token(rows[0]["token_enc"], key)
        if not raw:
            return {"status": "error", "error": "credential_decrypt_failed"}
        bundle = _parse_bundle(raw)
        bundle.update({
            "status": "ok",
            "broker": rows[0].get("broker"),
            "account_label": rows[0].get("account_label"),
        })
        return bundle

    def unlink(self, email: str) -> None:
        self._call("DELETE", f"email=eq.{email.lower()}")


def default_broker_store():
    """Choose the broker-link store backend from the environment.

    Supabase when SUPABASE_URL + SUPABASE_SERVICE_KEY are set (persists through
    redeploys), else local SQLite (dev).
    """
    url = (os.environ.get("SUPABASE_URL") or "").strip().rstrip("/")
    key = (
        os.environ.get("SUPABASE_SERVICE_KEY") or os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or ""
    ).strip()
    if url and key:
        return SupabaseBrokerLinkStore(url, key)
    db = os.environ.get("BROKER_DB") or str(Path(__file__).resolve().parents[1] / "data" / "broker.db")
    Path(db).parent.mkdir(parents=True, exist_ok=True)
    return BrokerLinkStore(db)


def build_broker_gate(store: BrokerLinkStore, adapter: Optional[BrokerAdapter] = None) -> Callable:
    """Build a broker-gate callable: (email, role) -> {connection, tier, adapter}.

    The returned callable lets a member/LP inspect their linked broker and the
    (read-only) adapter result. Order placement is intentionally absent.
    """
    adapter = adapter or BrokerAdapter()

    def gate(email: str, role: str) -> dict:
        if not can_access_real_data(role):
            return {
                "allowed": False,
                "tier": "synthetic",
                "error": "broker_link_requires_member",
            }
        conn = store.connection(email)
        if not conn["linked"]:
            return {"allowed": False, "error": "no_broker_linked", "tier": "member"}
        return {
            "allowed": True,
            "tier": "real",
            "broker": conn["broker"],
            "account_label": conn["account_label"],
            "read_only": True,
            "positions": adapter.positions(""),  # token resolved by real adapter
        }

    return gate


__all__ = [
    "BrokerLinkStore",
    "BrokerAdapter",
    "build_broker_gate",
]
