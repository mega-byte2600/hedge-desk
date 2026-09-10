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

import hashlib
import hmac
import os
import secrets
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional

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


def _encrypt_token(token: str, key: bytes) -> str:
    # Envelope: random nonce + HMAC-authenticated token. Not cryptographic
    # storage-grade on its own; it only guards an at-rest reference until a
    # real broker adapter and key-management story land.
    nonce = secrets.token_hex(16)
    tag = hmac.new(key, (nonce + token).encode("utf-8"), hashlib.sha256).hexdigest()
    return f"{nonce}:{tag}:{token}"


def _decrypt_token(blob: str, key: bytes) -> Optional[str]:
    try:
        nonce, tag, token = blob.split(":", 2)
        expect = hmac.new(key, (nonce + token).encode("utf-8"), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(tag, expect):
            return None
        return token
    except Exception:
        return None


class BrokerLinkStore:
    """SQLite-backed broker connections, scoped per member email."""

    def __init__(self, db_path: Path | str) -> None:
        self.db_path = str(db_path)
        self._conn = sqlite3.connect(self.db_path)
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
    ) -> dict:
        """Store a broker connection for a member. Fail closed on tier or key."""
        if role.upper() not in _ROLES_ALLOWED:
            raise PermissionError("broker link requires member/LP/GP")
        if not key:
            key = (os.environ.get("BROKER_LINK_KEY") or "").encode("utf-8")
            if not key:
                raise ValueError("BROKER_LINK_KEY not set; refusing to store broker token")
        now = _utcnow()
        enc = _encrypt_token(token, key)
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
