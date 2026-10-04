"""Broker-link scaffold for the Emporion desk.

Lets a MEMBER or LP connect their own broker account so the desk can act on
the Emporion "compass" signal. This is deliberately READ-ONLY first: the
connection stores broker metadata and, once an adapter is wired, can read
positions/balances. Order placement is gated separately behind the
deterministic risk engine and is NOT enabled here.

Security posture:
- Schwab access/refresh tokens and account hashes are stored only inside an
  AES-GCM encrypted bundle. The encryption key comes from the environment
  (BROKER_LINK_KEY) and must contain at least 32 bytes; without it the store
  refuses to persist tokens.
- Fail closed: any missing/invalid state yields no connection and no access.
- Tiered: only MEMBER / LP / GP may link a broker; GUEST and unauthenticated
  callers are denied.

Real adapter hooks: a concrete broker (e.g. Schwab) adapter implements
``BrokerAdapter`` and is injected. Until one is wired, calls return
``not_connected`` / ``not_implemented`` rather than inventing data.
"""

from __future__ import annotations

import hashlib
import base64
import binascii
import hmac
import json
import os
import secrets
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional

from cryptography.fernet import Fernet, InvalidToken
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from hedge_desk.sqlite_thread import new_lock, open_connection, thread_safe
from hedge_desk.tier_access import can_access_real_data

BROKER_TABLE = """
CREATE TABLE IF NOT EXISTS broker_links (
    email         TEXT PRIMARY KEY,
    broker        TEXT NOT NULL,             -- e.g. 'schwab'
    account_label TEXT,
    token_enc     TEXT,                      -- AES-GCM encrypted token/metadata bundle
    created_at    TEXT NOT NULL,
    updated_at    TEXT NOT NULL
);
"""

# Role check: only real-data tiers (MEMBER/LP/GP) may link a broker.
_ROLES_ALLOWED = ("MEMBER", "LP", "GP")


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def _resolved_key(key: Optional[bytes]) -> bytes:
    if key is not None:
        if not key:
            raise ValueError("BROKER_LINK_KEY must contain at least 32 bytes")
        return key
    value = (os.environ.get("BROKER_LINK_KEY") or "").encode("utf-8")
    if not value:
        raise ValueError("BROKER_LINK_KEY not set; refusing to store broker token")
    return value


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


_TOKEN_AAD = b"hedge-desk:broker-link:v1"


def _token_key(key: bytes) -> bytes:
    if not isinstance(key, bytes) or len(key) < 32:
        raise ValueError("BROKER_LINK_KEY must contain at least 32 bytes")
    return hashlib.sha256(b"hedge-desk:broker-link:key:v1\0" + key).digest()


def _aad(context: str) -> bytes:
    return _TOKEN_AAD + b":" + context.strip().lower().encode("utf-8")


def _encrypt_token(token: str, key: bytes, context: str = "") -> str:
    """Encrypt token material using AES-256-GCM with a fresh random nonce."""
    if not isinstance(token, str) or not token:
        raise ValueError("broker token material is required")
    nonce = secrets.token_bytes(12)
    ciphertext = AESGCM(_token_key(key)).encrypt(nonce, token.encode("utf-8"), _aad(context))
    payload = base64.urlsafe_b64encode(nonce + ciphertext).decode("ascii").rstrip("=")
    return f"v1.{payload}"


def _decrypt_token(blob: str, key: bytes, context: str = "") -> Optional[str]:
    try:
        if not isinstance(blob, str):
            return None
        if blob.startswith("fernet:"):
            derived = base64.urlsafe_b64encode(hashlib.sha256(key).digest())
            return Fernet(derived).decrypt(blob.split(":", 1)[1].encode("ascii")).decode("utf-8")
        if not blob.startswith("v1."):
            # Verify and migrate the old HMAC envelope. Its token content was
            # plaintext, so callers re-encrypt it before returning any token.
            nonce, tag, token = blob.split(":", 2)
            expected = hmac.new(key, (nonce + token).encode("utf-8"), hashlib.sha256).hexdigest()
            return token if hmac.compare_digest(tag, expected) else None
        encoded = blob[3:]
        combined = base64.urlsafe_b64decode(encoded + "=" * (-len(encoded) % 4))
        if len(combined) < 12 + 16:
            return None
        plaintext = AESGCM(_token_key(key)).decrypt(combined[:12], combined[12:], _aad(context))
        return plaintext.decode("utf-8")
    except (InvalidTag, InvalidToken, ValueError, UnicodeDecodeError, binascii.Error):
        return None


def _token_bundle(
    access_token: str,
    *,
    refresh_token: str = "",
    access_expires_at: str = "",
    refresh_token_issued_at: str = "",
    scope: str = "",
    selected_account_hash: str = "",
    available_account_hashes: str = "",
    updated_at: str = "",
) -> str:
    values = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "access_expires_at": access_expires_at,
        "refresh_token_issued_at": refresh_token_issued_at,
        "scope": scope,
        "selected_account_hash": selected_account_hash,
        "available_account_hashes": available_account_hashes,
        "updated_at": updated_at,
    }
    if any(not isinstance(value, str) for value in values.values()):
        raise ValueError("broker token metadata must be text")
    if not access_token:
        raise ValueError("access token is required")
    return json.dumps(values, sort_keys=True, separators=(",", ":"))


def _decode_token_bundle(blob: str, key: bytes, context: str = "") -> tuple[dict, bool]:
    plaintext = _decrypt_token(blob, key, context)
    if plaintext is None:
        raise ValueError("stored broker token is unreadable; reauthentication required")
    try:
        payload = json.loads(plaintext)
    except (TypeError, ValueError, UnicodeDecodeError):
        payload = {
            "access_token": plaintext,
            "refresh_token": "",
            "access_expires_at": "",
            "refresh_token_issued_at": "",
            "scope": "",
            "selected_account_hash": "",
            "available_account_hashes": "",
            "updated_at": "",
        }
        legacy = True
    else:
        legacy = not blob.startswith("v1.")
    if isinstance(payload, dict) and set(payload) == {"access_token", "refresh_token", "expires_at", "account_hash", "account_number"}:
        account_hash = payload["account_hash"]
        payload = {
            "access_token": payload["access_token"], "refresh_token": payload["refresh_token"],
            "access_expires_at": payload["expires_at"], "refresh_token_issued_at": "",
            "scope": "api", "selected_account_hash": account_hash,
            "available_account_hashes": json.dumps([account_hash] if account_hash else []), "updated_at": "",
        }
        legacy = True
    # Missing refresh issuance evidence requires renewed consent; do not invent an age.
    # Migrate earlier encrypted bundle revisions without dropping existing
    # credentials. Missing account metadata stays unselected and therefore
    # cannot be used for an account-specific API call.
    if isinstance(payload, dict):
        old_required = {
            "access_token", "refresh_token", "access_expires_at",
            "refresh_token_issued_at", "scope", "selected_account_hash",
        }
        if set(payload) == old_required:
            payload = {**payload, "available_account_hashes": "[]", "updated_at": ""}
            legacy = True
        elif set(payload) == old_required | {"available_account_hashes"}:
            payload = {**payload, "updated_at": ""}
            legacy = True
    required = {
        "access_token", "refresh_token", "access_expires_at",
        "refresh_token_issued_at", "scope", "selected_account_hash",
        "available_account_hashes",
        "updated_at",
    }
    if not isinstance(payload, dict) or set(payload) != required:
        raise ValueError("stored broker token is unreadable; reauthentication required")
    if any(not isinstance(value, str) for value in payload.values()) or not payload["access_token"]:
        raise ValueError("stored broker token is unreadable; reauthentication required")
    return payload, legacy


def _open_token_bundle(blob: str, key: bytes, context: str = "") -> dict:
    return _decode_token_bundle(blob, key, context)[0]


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
        *,
        refresh_token: str = "",
        access_expires_at: str = "",
        refresh_token_issued_at: str = "",
        scope: str = "",
        selected_account_hash: str = "",
        available_account_hashes: str = "",
    ) -> dict:
        """Store a broker connection for a member. Fail closed on tier or key."""
        if role.upper() not in _ROLES_ALLOWED:
            raise PermissionError("broker link requires member/LP/GP")
        key = _resolved_key(key)
        now = _utcnow()
        bundle = _token_bundle(
            token,
            refresh_token=refresh_token,
            access_expires_at=access_expires_at,
            refresh_token_issued_at=refresh_token_issued_at,
            scope=scope,
            selected_account_hash=selected_account_hash,
            available_account_hashes=available_account_hashes,
            updated_at=now,
        )
        enc = _encrypt_token(bundle, key, email.lower())
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

    def token_state(self, email: str, key: Optional[bytes] = None) -> dict:
        """Read decrypted credentials for trusted server-side adapter use only."""
        key = _resolved_key(key)
        row = self._conn.execute(
            "SELECT broker, token_enc FROM broker_links WHERE email=?", (email.lower(),)
        ).fetchone()
        if not row:
            raise LookupError("no broker link")
        if row[0] != "schwab":
            raise ValueError("broker link is not Schwab")
        payload, legacy = _decode_token_bundle(row[1], key, email.lower())
        if legacy:
            upgraded = _encrypt_token(_token_bundle(**payload), key, email.lower())
            self._conn.execute(
                "UPDATE broker_links SET token_enc=?, updated_at=? WHERE email=?",
                (upgraded, _utcnow(), email.lower()),
            )
            self._conn.commit()
        return payload

    def persist_schwab_tokens(self, email: str, state, key: Optional[bytes] = None) -> None:
        """Persist a refreshed Schwab token bundle before protected API calls."""
        key = _resolved_key(key)
        row = self._conn.execute(
            "SELECT broker, token_enc FROM broker_links WHERE email=?", (email.lower(),)
        ).fetchone()
        if not row:
            raise LookupError("no broker link")
        if row[0] != "schwab":
            raise ValueError("broker link is not Schwab")
        existing = _open_token_bundle(row[1], key, email.lower())
        bundle = _token_bundle(
            state.access_token,
            refresh_token=state.refresh_token,
            access_expires_at=state.access_expires_at.isoformat(),
            refresh_token_issued_at=state.refresh_issued_at.isoformat(),
            scope=state.scope,
            selected_account_hash=state.selected_account_hash,
            available_account_hashes=existing.get("available_account_hashes", ""),
            updated_at=state.updated_at.isoformat(),
        )
        self._conn.execute(
            "UPDATE broker_links SET token_enc=?, updated_at=? WHERE email=?",
            (_encrypt_token(bundle, key, email.lower()), _utcnow(), email.lower()),
        )
        self._conn.commit()

    def select_schwab_account(self, email: str, account_hash: str, key: Optional[bytes] = None) -> None:
        """Persist a selected encrypted account hash without exposing it to clients."""
        if not account_hash:
            raise ValueError("account hash is required")
        key = _resolved_key(key)
        row = self._conn.execute(
            "SELECT broker, token_enc FROM broker_links WHERE email=?", (email.lower(),)
        ).fetchone()
        if not row:
            raise LookupError("no broker link")
        if row[0] != "schwab":
            raise ValueError("broker link is not Schwab")
        bundle = _open_token_bundle(row[1], key, email.lower())
        try:
            available = json.loads(bundle.get("available_account_hashes", "[]"))
        except (TypeError, ValueError):
            available = []
        if account_hash not in available:
            raise PermissionError("account hash is not linked to this Schwab grant")
        bundle["selected_account_hash"] = account_hash
        bundle["updated_at"] = _utcnow()
        encrypted = _encrypt_token(json.dumps(bundle, sort_keys=True, separators=(",", ":")), key, email.lower())
        self._conn.execute(
            "UPDATE broker_links SET token_enc=?, updated_at=? WHERE email=?",
            (encrypted, _utcnow(), email.lower()),
        )
        self._conn.commit()

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

    def positions(self, token: str, account_hash: str = "") -> dict:
        return {"status": "not_implemented", "broker": self.name}

    def balances(self, token: str, account_hash: str = "") -> dict:
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
        self,
        email,
        role,
        broker,
        token,
        account_label="",
        key=None,
        *,
        refresh_token="",
        access_expires_at="",
        refresh_token_issued_at="",
        scope="",
        selected_account_hash="",
        available_account_hashes="",
    ) -> dict:
        if str(role).upper() not in _ROLES_ALLOWED:
            raise PermissionError("broker link requires member/LP/GP")
        key = _resolved_key(key)
        now = _utcnow()
        bundle = _token_bundle(
            token,
            refresh_token=refresh_token,
            access_expires_at=access_expires_at,
            refresh_token_issued_at=refresh_token_issued_at,
            scope=scope,
            selected_account_hash=selected_account_hash,
            available_account_hashes=available_account_hashes,
            updated_at=now,
        )
        enc = _encrypt_token(bundle, key, email.lower())
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

    def token_state(self, email: str, key: Optional[bytes] = None) -> dict:
        """Read decrypted credentials for trusted server-side adapter use only."""
        key = _resolved_key(key)
        rows = self._call(
            "GET", f"email=eq.{email.lower()}&select=broker,token_enc"
        )
        if not rows:
            raise LookupError("no broker link")
        row = rows[0]
        if row.get("broker") != "schwab":
            raise ValueError("broker link is not Schwab")
        payload, legacy = _decode_token_bundle(row.get("token_enc"), key, email.lower())
        if legacy:
            upgraded = _encrypt_token(_token_bundle(**payload), key, email.lower())
            self._call(
                "PATCH",
                f"email=eq.{email.lower()}",
                body={"token_enc": upgraded, "updated_at": _utcnow()},
            )
        return payload

    def persist_schwab_tokens(self, email: str, state, key: Optional[bytes] = None) -> None:
        """Persist a refreshed Schwab token bundle before protected API calls."""
        key = _resolved_key(key)
        rows = self._call("GET", f"email=eq.{email.lower()}&select=broker,token_enc")
        if not rows:
            raise LookupError("no broker link")
        if rows[0].get("broker") != "schwab":
            raise ValueError("broker link is not Schwab")
        existing = _open_token_bundle(rows[0].get("token_enc"), key, email.lower())
        bundle = _token_bundle(
            state.access_token,
            refresh_token=state.refresh_token,
            access_expires_at=state.access_expires_at.isoformat(),
            refresh_token_issued_at=state.refresh_issued_at.isoformat(),
            scope=state.scope,
            selected_account_hash=state.selected_account_hash,
            available_account_hashes=existing.get("available_account_hashes", ""),
            updated_at=state.updated_at.isoformat(),
        )
        self._call(
            "PATCH",
            f"email=eq.{email.lower()}",
            body={"token_enc": _encrypt_token(bundle, key, email.lower()), "updated_at": _utcnow()},
        )

    def select_schwab_account(self, email: str, account_hash: str, key: Optional[bytes] = None) -> None:
        if not account_hash:
            raise ValueError("account hash is required")
        key = _resolved_key(key)
        rows = self._call("GET", f"email=eq.{email.lower()}&select=broker,token_enc")
        if not rows:
            raise LookupError("no broker link")
        row = rows[0]
        if row.get("broker") != "schwab":
            raise ValueError("broker link is not Schwab")
        bundle = _open_token_bundle(row.get("token_enc"), key, email.lower())
        try:
            available = json.loads(bundle.get("available_account_hashes", "[]"))
        except (TypeError, ValueError):
            available = []
        if account_hash not in available:
            raise PermissionError("account hash is not linked to this Schwab grant")
        bundle["selected_account_hash"] = account_hash
        bundle["updated_at"] = _utcnow()
        encrypted = _encrypt_token(json.dumps(bundle, sort_keys=True, separators=(",", ":")), key, email.lower())
        self._call(
            "PATCH", f"email=eq.{email.lower()}",
            body={"token_enc": encrypted, "updated_at": _utcnow()},
        )

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
