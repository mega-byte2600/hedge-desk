"""Restricted Supabase persistence for the latest public market-context snapshot.

Only public provider observations are stored. Writes use a server-only Supabase
secret/service key; this module never returns credentials or upstream error text.
"""
from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from urllib.request import Request, urlopen


TABLE = "market_context_snapshots"


def _credentials(env=None):
    source = os.environ if env is None else env
    url = str(source.get("SUPABASE_URL", "")).strip().rstrip("/")
    key = (
        str(source.get("SUPABASE_SECRET_KEY", "")).strip()
        or str(source.get("SUPABASE_SERVICE_ROLE_KEY", "")).strip()
    )
    if not url or not key:
        return None
    return url, key


def _send(request, timeout=5):
    with urlopen(request, timeout=timeout) as response:
        return response.status


def persist_latest_market_context(snapshot, *, env=None, transport=None):
    """Upsert the public latest snapshot; report an explicit safe storage status."""
    credentials = _credentials(env)
    if credentials is None:
        return {"status": "UNCONFIGURED", "reason_code": "SERVER_STORAGE_CREDENTIALS_MISSING"}

    url, key = credentials
    generated_at = str(snapshot.get("generated_at") or datetime.now(timezone.utc).isoformat())
    row = {
        "snapshot_key": "latest",
        "schema_version": str(snapshot.get("schema_version", "")),
        "generated_at": generated_at,
        "status": str(snapshot.get("status", "BLOCKED")),
        "live_sources": int(snapshot.get("live_sources", 0)),
        "blocked_sources": int(snapshot.get("blocked_sources", 0)),
        "unconfigured_sources": int(snapshot.get("unconfigured_sources", 0)),
        "payload": snapshot,
    }
    request = Request(
        url + "/rest/v1/" + TABLE + "?on_conflict=snapshot_key",
        data=json.dumps(row, separators=(",", ":")).encode("utf-8"),
        method="POST",
        headers={
            "apikey": key,
            "Authorization": "Bearer " + key,
            "Content-Type": "application/json",
            "Prefer": "resolution=merge-duplicates,return=minimal",
        },
    )
    try:
        status = (transport or _send)(request)
    except Exception:
        return {"status": "FAILED", "reason_code": "STORAGE_WRITE_FAILED"}
    if 200 <= int(status) < 300:
        return {"status": "PERSISTED", "generated_at": generated_at}
    return {"status": "FAILED", "reason_code": "STORAGE_WRITE_REJECTED", "http_status": int(status)}


def load_latest_market_context(*, env=None, transport=None):
    """Read the last persisted snapshot using server credentials, if configured."""
    credentials = _credentials(env)
    if credentials is None:
        return None
    url, key = credentials
    request = Request(
        url + "/rest/v1/" + TABLE + "?snapshot_key=eq.latest&select=payload&limit=1",
        headers={
            "apikey": key,
            "Authorization": "Bearer " + key,
            "Accept": "application/json",
        },
    )
    try:
        result = (transport or _send_json)(request)
    except Exception:
        return None
    if isinstance(result, list) and result and isinstance(result[0], dict):
        payload = result[0].get("payload")
        if isinstance(payload, dict):
            return payload
    return None


def _send_json(request, timeout=5):
    with urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


__all__ = ["persist_latest_market_context", "load_latest_market_context"]
