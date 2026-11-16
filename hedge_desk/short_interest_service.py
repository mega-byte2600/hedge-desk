"""Read-only, cached FINRA consolidated short-interest snapshots for Desk 5."""
from __future__ import annotations

import os
from threading import Lock, Thread
from time import monotonic
from typing import Dict, Iterable

from hedge_desk.data.institutional_feeds import finra_equity
from hedge_desk.data.open_market_feeds import _finra_oauth_token, _default_request_transport

SOURCE = "FINRA Consolidated Short Interest"
SOURCE_URL = "https://developer.finra.org/docs"
_lock = Lock()
_snapshot: Dict[str, dict] = {}
_built_at = 0.0
_refreshing = False
_cache_seconds = 12 * 60 * 60


def _unconfigured(symbols: tuple[str, ...]) -> dict:
    return {
        "status": "UNCONFIGURED",
        "source": SOURCE,
        "source_url": SOURCE_URL,
        "reason": "Add a FINRA Public API credential to the server environment to load consolidated short interest.",
        "symbols": {symbol: {"status": "UNCONFIGURED"} for symbol in symbols},
        "interpretation": "FINRA short interest is a twice-monthly position snapshot; it is not daily short-sale volume, locate availability, or borrow cost.",
    }


def _refresh(symbols: tuple[str, ...]) -> None:
    global _snapshot, _built_at, _refreshing
    fresh: Dict[str, dict] = {}
    try:
        token = _finra_oauth_token(_default_request_transport)
        for symbol in symbols:
            try:
                result = finra_equity(
                    "consolidated_short_interest",
                    limit=3,
                    access_token=token,
                    symbol_code=symbol,
                )
                candidates = [row for row in result.rows if str(row.get("symbolCode", "")).upper() == symbol]
                candidates.sort(key=lambda row: str(row.get("settlementDate", "")), reverse=True)
                if not candidates:
                    fresh[symbol] = {"status": "NO_MATCHING_REPORT"}
                    continue
                row = candidates[0]
                fresh[symbol] = {
                    "status": "LIVE",
                    "settlement_date": row.get("settlementDate"),
                    "issue_name": row.get("issueName"),
                    "current_short_position": row.get("currentShortPositionQuantity"),
                    "previous_short_position": row.get("previousShortPositionQuantity"),
                    "change_percent": row.get("changePercent"),
                    "average_daily_volume": row.get("averageDailyVolumeQuantity"),
                    "days_to_cover": row.get("daysToCoverQuantity"),
                    "market_class": row.get("marketClassCode"),
                    "revision_flag": row.get("revisionFlag"),
                    "source": SOURCE,
                    "source_url": SOURCE_URL,
                }
            except Exception:
                fresh[symbol] = {"status": "BLOCKED"}
    except Exception:
        fresh = {symbol: {"status": "BLOCKED"} for symbol in symbols}
    finally:
        with _lock:
            if fresh:
                _snapshot = {**_snapshot, **fresh}
                _built_at = monotonic()
            _refreshing = False
    # ``overall`` is recomputed from the shared symbol snapshot on read.


def get_short_interest(symbols: Iterable[str]) -> dict:
    """Return last-known data immediately and refresh stale watchlist rows in background."""
    global _refreshing
    requested = tuple(dict.fromkeys(str(item).strip().upper() for item in symbols if str(item).strip()))
    if not (os.environ.get("FINRA_CLIENT_ID", "").strip() and os.environ.get("FINRA_CLIENT_SECRET", "").strip()):
        return _unconfigured(requested)
    with _lock:
        missing = any(symbol not in _snapshot for symbol in requested)
        stale = monotonic() - _built_at >= _cache_seconds
        start = (missing or stale) and not _refreshing
        if start:
            _refreshing = True
            Thread(target=_refresh, args=(requested,), name="finra-short-interest-refresh", daemon=True).start()
        rows = {symbol: _snapshot.get(symbol, {"status": "LOADING"}) for symbol in requested}
    statuses = {row.get("status") for row in rows.values()}
    if start:
        status = "REFRESHING"
    elif "LIVE" in statuses:
        status = "LIVE"
    elif "LOADING" in statuses:
        status = "LOADING"
    elif statuses == {"NO_MATCHING_REPORT"}:
        status = "NO_MATCHING_REPORT"
    elif "NO_MATCHING_REPORT" in statuses:
        status = "PARTIAL"
    else:
        status = "BLOCKED"
    return {
        "status": status,
        "source": SOURCE,
        "source_url": SOURCE_URL,
        "symbols": rows,
        "interpretation": "FINRA short interest is a twice-monthly position snapshot; it is not daily short-sale volume, locate availability, or borrow cost.",
    }


__all__ = ["get_short_interest", "SOURCE", "SOURCE_URL"]
