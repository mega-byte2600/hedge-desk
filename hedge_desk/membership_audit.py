"""Append-only, tamper-evident audit log for membership events.

Why this exists: a fund's membership record is a compliance artifact. Who was
invited, when a role changed, and when a broker was linked must be replayable
and provably unaltered. This mirrors the desk's existing hash-chained audit
philosophy (see ``hedge_desk/audit.py``) for the membership surface.

Design:
- Each entry stores the hash of the previous entry plus a canonical encoding of
  its own fields, so altering or removing any entry breaks the chain.
- Append-only: there is no update or delete operation.
- Two backends with identical semantics: SQLite (dev) and Supabase (production,
  survives redeploys), chosen by ``default_audit_log()``.
- stdlib only; transport injectable for tests.
"""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from hedge_desk.sqlite_thread import new_lock, open_connection, thread_safe

GENESIS = "0" * 64

_SCHEMA = """
CREATE TABLE IF NOT EXISTS membership_events (
    seq        INTEGER PRIMARY KEY AUTOINCREMENT,
    event      TEXT NOT NULL,
    email      TEXT NOT NULL,
    actor      TEXT NOT NULL,
    detail     TEXT NOT NULL,
    created_at TEXT NOT NULL,
    prev_hash  TEXT NOT NULL,
    entry_hash TEXT NOT NULL
);
"""


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def entry_hash(seq, event, email, actor, detail, created_at, prev_hash) -> str:
    """Canonical hash for one audit entry (defines what 'unaltered' means)."""
    payload = json.dumps(
        {
            "seq": seq,
            "event": event,
            "email": email,
            "actor": actor,
            "detail": detail,
            "created_at": created_at,
            "prev_hash": prev_hash,
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def verify_chain(entries: list[dict]) -> list[str]:
    """Return reason codes for any broken link; empty means intact."""
    reasons = []
    prev = GENESIS
    for i, e in enumerate(entries):
        if e.get("prev_hash") != prev:
            reasons.append(f"PREV_HASH_MISMATCH@{i}")
        expected = entry_hash(
            e.get("seq"), e.get("event"), e.get("email"), e.get("actor"),
            e.get("detail"), e.get("created_at"), e.get("prev_hash"),
        )
        if e.get("entry_hash") != expected:
            reasons.append(f"ENTRY_HASH_MISMATCH@{i}")
        prev = e.get("entry_hash")
    return reasons


@thread_safe
class MembershipAuditLog:
    """SQLite-backed append-only audit log."""

    def __init__(self, db_path: Path | str) -> None:
        self.db_path = str(db_path)
        # Served from a thread pool: one connection shared under one lock.
        self._lock = new_lock()
        self._conn = open_connection(self.db_path)
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.executescript(_SCHEMA)
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()

    def record(self, event: str, email: str, actor: str = "", detail: str = "") -> dict:
        row = self._conn.execute(
            "SELECT seq, entry_hash FROM membership_events ORDER BY seq DESC LIMIT 1"
        ).fetchone()
        seq = (row[0] + 1) if row else 1
        prev = row[1] if row else GENESIS
        created = _utcnow()
        digest = entry_hash(seq, event, email.lower(), actor, detail, created, prev)
        self._conn.execute(
            "INSERT INTO membership_events "
            "(seq, event, email, actor, detail, created_at, prev_hash, entry_hash) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (seq, event, email.lower(), actor, detail, created, prev, digest),
        )
        self._conn.commit()
        return {"seq": seq, "event": event, "email": email.lower(), "actor": actor,
                "detail": detail, "created_at": created, "prev_hash": prev,
                "entry_hash": digest}

    def entries(self, limit: int = 500) -> list[dict]:
        rows = self._conn.execute(
            "SELECT seq, event, email, actor, detail, created_at, prev_hash, entry_hash "
            "FROM membership_events ORDER BY seq ASC LIMIT ?",
            (limit,),
        ).fetchall()
        return [
            {"seq": r[0], "event": r[1], "email": r[2], "actor": r[3], "detail": r[4],
             "created_at": r[5], "prev_hash": r[6], "entry_hash": r[7]}
            for r in rows
        ]

    def verify(self) -> list[str]:
        return verify_chain(self.entries())


class SupabaseMembershipAuditLog:
    """Supabase-backed append-only audit log (same semantics)."""

    def __init__(self, url: str, service_key: str, transport=None) -> None:
        if not url or not service_key:
            raise ValueError("SupabaseMembershipAuditLog requires url and service_key")
        self.url = url.rstrip("/")
        self.service_key = service_key
        if transport is None:

            def _default_transport(method, url_, headers, body):  # PostgREST transport
                import urllib.error
                import urllib.request

                req = urllib.request.Request(url_, data=body, headers=headers, method=method)
                try:
                    with urllib.request.urlopen(req, timeout=20) as resp:
                        return resp.status, resp.read()
                except urllib.error.HTTPError as exc:
                    return exc.code, exc.read()

            transport = _default_transport

        self._transport = transport

    def _call(self, method, query="", body=None, prefer=""):
        url = f"{self.url}/rest/v1/membership_events"
        if query:
            url += "?" + query
        headers = {
            "apikey": self.service_key,
            "Authorization": f"Bearer {self.service_key}",
            "Content-Type": "application/json",
        }
        if prefer:
            headers["Prefer"] = prefer
        data = json.dumps(body).encode("utf-8") if body is not None else None
        status, raw = self._transport(method, url, headers, data)
        if status >= 400:
            raise RuntimeError(f"supabase membership_events {method} failed: {status}")
        if not raw:
            return []
        try:
            return json.loads(raw)
        except Exception:
            return []

    def close(self) -> None:
        return None

    def record(self, event: str, email: str, actor: str = "", detail: str = "") -> dict:
        rows = self._call("GET", "select=seq,entry_hash&order=seq.desc&limit=1")
        last = rows[0] if rows else None
        seq = (int(last["seq"]) + 1) if last else 1
        prev = last["entry_hash"] if last else GENESIS
        created = _utcnow()
        digest = entry_hash(seq, event, email.lower(), actor, detail, created, prev)
        self._call(
            "POST",
            body={"seq": seq, "event": event, "email": email.lower(), "actor": actor,
                  "detail": detail, "created_at": created, "prev_hash": prev,
                  "entry_hash": digest},
        )
        return {"seq": seq, "event": event, "email": email.lower(), "actor": actor,
                "detail": detail, "created_at": created, "prev_hash": prev,
                "entry_hash": digest}

    def entries(self, limit: int = 500) -> list[dict]:
        rows = self._call(
            "GET", f"select=*&order=seq.asc&limit={int(limit)}"
        )
        return rows or []

    def verify(self) -> list[str]:
        return verify_chain(self.entries())


def default_audit_log():
    """Supabase when configured (persists through redeploys), else SQLite."""
    url = (os.environ.get("SUPABASE_URL") or "").strip().rstrip("/")
    key = (
        os.environ.get("SUPABASE_SERVICE_KEY") or os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or ""
    ).strip()
    if url and key:
        return SupabaseMembershipAuditLog(url, key)
    db = os.environ.get("AUDIT_DB") or str(
        Path(__file__).resolve().parents[1] / "data" / "membership-audit.db"
    )
    Path(db).parent.mkdir(parents=True, exist_ok=True)
    return MembershipAuditLog(db)


__all__ = [
    "MembershipAuditLog",
    "SupabaseMembershipAuditLog",
    "default_audit_log",
    "verify_chain",
    "entry_hash",
    "GENESIS",
]
