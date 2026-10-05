"""Serve stale market context immediately while refreshing public APIs in background.

The provider fan-out can exceed a web request timeout. This process-local
coordinator returns the latest persisted/in-memory snapshot and refreshes at
most once at a time; provider work never blocks the main console boot path.
"""
from __future__ import annotations

from datetime import datetime, timezone
from threading import Lock, Thread
from time import monotonic
import os

from hedge_desk.market_context import build_market_context
from hedge_desk.market_context_storage import (
    load_latest_market_context,
    persist_latest_market_context,
)


_REFRESH_SECONDS = max(
    60.0, float(os.getenv("EMPORION_MARKET_CONTEXT_CACHE_SECONDS", "900"))
)
_lock = Lock()
_snapshot = None
_built_at = 0.0
_refreshing = False
_store_checked = False


def _empty_status():
    return {
        "schema_version": "hedge-desk-market-context-1.0.0",
        "status": "LOADING",
        "live_sources": 0,
        "blocked_sources": 0,
        "unconfigured_sources": 0,
        "sources": {},
        "generated_at": None,
        "storage": {"status": "LOADING"},
        "trade_authorized": False,
    }


def _refresh():
    global _snapshot, _built_at, _refreshing, _store_checked
    try:
        with _lock:
            should_load_store = not _store_checked
            _store_checked = True
        if should_load_store:
            stored = load_latest_market_context()
            if isinstance(stored, dict):
                with _lock:
                    if _snapshot is None:
                        _snapshot = stored
                        _built_at = monotonic()

        fresh = build_market_context()
        fresh["generated_at"] = datetime.now(timezone.utc).isoformat()
        fresh["trade_authorized"] = False
        fresh["storage"] = persist_latest_market_context(fresh)
        with _lock:
            _snapshot = fresh
            _built_at = monotonic()
    except Exception:
        # Never replace a last-good snapshot with an exception or synthetic data.
        with _lock:
            if _snapshot is None:
                _snapshot = {
                    **_empty_status(),
                    "status": "BLOCKED",
                    "reason_code": "MARKET_CONTEXT_REFRESH_FAILED",
                    "storage": {"status": "UNAVAILABLE"},
                }
                _built_at = monotonic()
    finally:
        with _lock:
            _refreshing = False


def get_market_context_snapshot():
    """Return current snapshot quickly and queue a refresh when absent or stale."""
    global _refreshing
    with _lock:
        current = _snapshot
        stale = current is None or monotonic() - _built_at >= _REFRESH_SECONDS
        start = stale and not _refreshing
        if start:
            _refreshing = True
    if start:
        Thread(target=_refresh, name="market-context-refresh", daemon=True).start()
    if current is None:
        return _empty_status()
    return current


__all__ = ["get_market_context_snapshot"]
