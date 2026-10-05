"""Primary Schwab market-data provider for Emporion production desk surfaces.

Schwab is the preferred production quote source. Yahoo Finance is retained only
as a per-symbol failover so the desk can degrade gracefully without inventing data.
No live-order capability is exposed here.
"""

from __future__ import annotations

import os
from datetime import datetime, timedelta

from hedge_desk.broker_link import default_broker_store
from hedge_desk.brokers.schwab_market_data import SchwabMarketDataBroker
from hedge_desk.brokers.schwab_oauth import SchwabOAuth, SchwabOAuthConfig
from hedge_desk.brokers.schwab_tokens import SchwabTokenManager, SchwabTokenState


SOURCE_NAME = "Schwab Trader API / Market Data"
FALLBACK_SOURCE_NAME = "Yahoo Finance fallback"


def _data_email() -> str:
    return (os.getenv("SCHWAB_DATA_EMAIL") or os.getenv("GP_EMAIL") or "").strip().lower()


def _state_from_payload(payload: dict) -> SchwabTokenState:
    return SchwabTokenState(
        access_token=payload["access_token"],
        refresh_token=payload["refresh_token"],
        access_expires_at=datetime.fromisoformat(payload["access_expires_at"]),
        refresh_issued_at=datetime.fromisoformat(payload["refresh_token_issued_at"]),
        scope=payload["scope"],
        updated_at=datetime.fromisoformat(payload["updated_at"]),
        selected_account_hash=payload.get("selected_account_hash", ""),
    )


def _access_token() -> str:
    email = _data_email()
    if not email:
        raise RuntimeError("schwab_data_identity_not_configured")

    cfg = SchwabOAuthConfig.from_environment()
    if not cfg.configured:
        raise RuntimeError("schwab_oauth_not_configured")

    store = default_broker_store()
    payload = store.token_state(email)
    state = _state_from_payload(payload)
    manager = SchwabTokenManager(
        refresh=SchwabOAuth(cfg).refresh_access_token,
        persist=lambda refreshed: store.persist_schwab_tokens(email, refreshed),
        refresh_token_max_age=timedelta(days=7),
    )
    return manager.access_token(state)


def status() -> dict:
    """Return non-secret deployment readiness for diagnostics/health only."""
    email = _data_email()
    try:
        cfg = SchwabOAuthConfig.from_environment()
        configured = bool(cfg.configured)
    except Exception:
        configured = False

    linked = False
    if email:
        try:
            linked = bool(default_broker_store().connection(email).get("linked"))
        except Exception:
            linked = False

    return {
        "provider": "schwab",
        "oauth_configured": configured,
        "data_identity_configured": bool(email),
        "linked": linked,
        "ready": bool(configured and email and linked),
    }


def _as_number(value):
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return None


def _parse_quote(symbol: str, item: dict) -> dict | None:
    if not isinstance(item, dict):
        return None
    quote = item.get("quote") if isinstance(item.get("quote"), dict) else item
    reference = item.get("reference") if isinstance(item.get("reference"), dict) else {}

    last = (
        _as_number(quote.get("lastPrice"))
        or _as_number(quote.get("mark"))
        or _as_number(quote.get("closePrice"))
    )
    prev = (
        _as_number(quote.get("closePrice"))
        or _as_number(quote.get("previousClose"))
    )
    if last is None:
        return None

    pct = _as_number(quote.get("netPercentChange"))
    if pct is None and prev not in (None, 0):
        pct = (last - prev) / prev * 100.0

    return {
        "symbol": symbol,
        "name": reference.get("description") or symbol,
        "last": round(last, 2),
        "prev_close": round(prev, 2) if prev is not None else round(last, 2),
        "change_pct": round(pct or 0.0, 2),
        "source": SOURCE_NAME,
    }


def fetch_market_snapshot(symbols, timeout=8):
    """Fetch Schwab first; use Yahoo only for symbols Schwab cannot return."""
    # Local import avoids coupling the fallback into the broker package.
    from hedge_desk.live_desk_data import _fetch_yahoo

    normalized = [str(s).strip().upper() for s in symbols if str(s).strip()]
    data = {}
    unavailable = []
    schwab_error = ""

    try:
        token = _access_token()
        result = SchwabMarketDataBroker().quotes(token, normalized)
        if result.get("status") != "ok":
            schwab_error = result.get("error") or f"http_{result.get('http_status', 'unknown')}"
        else:
            payload = result.get("data")
            if isinstance(payload, dict):
                for symbol in normalized:
                    item = payload.get(symbol)
                    parsed = _parse_quote(symbol, item)
                    if parsed:
                        data[symbol] = parsed
    except Exception as exc:
        schwab_error = str(exc) or exc.__class__.__name__

    for symbol in normalized:
        if symbol in data:
            continue
        fallback = _fetch_yahoo(symbol, timeout=timeout)
        if fallback is not None:
            fallback["source"] = FALLBACK_SOURCE_NAME
            data[symbol] = fallback
        else:
            reason = "quote unavailable from Schwab and Yahoo fallback"
            if schwab_error:
                reason += f" ({schwab_error})"
            unavailable.append({"symbol": symbol, "reason": reason})

    return data, unavailable


__all__ = ["fetch_market_snapshot", "status", "SOURCE_NAME", "FALLBACK_SOURCE_NAME"]
