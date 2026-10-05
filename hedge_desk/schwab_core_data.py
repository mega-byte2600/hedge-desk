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
CORROBORATIVE_SOURCE_NAME = "Yahoo Finance corroborative"
DEFAULT_DELTA_BPS = 50.0


def _delta_threshold_bps() -> float:
    try:
        value = float(os.getenv("EMPORION_MARKET_DATA_DELTA_BPS", str(DEFAULT_DELTA_BPS)))
    except (TypeError, ValueError):
        return DEFAULT_DELTA_BPS
    return value if value > 0 else DEFAULT_DELTA_BPS


def _delta_bps(primary: dict, secondary: dict) -> float | None:
    p = _as_number(primary.get("last"))
    s = _as_number(secondary.get("last"))
    if p in (None, 0) or s is None:
        return None
    return abs(s - p) / abs(p) * 10000.0


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
    """Use Schwab where it has quote coverage; corroborate overlapping quotes.

    Schwab is primary only for the market-data capability it actually supplies.
    Yahoo is secondary/corroborative for overlapping quotes, but is promoted for
    a datum when the observed price delta breaches the configured tolerance.
    If Schwab has no datum, Yahoo becomes primary for that datum.
    """
    from hedge_desk.live_desk_data import _fetch_yahoo

    normalized = [str(s).strip().upper() for s in symbols if str(s).strip()]
    schwab = {}
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
                    parsed = _parse_quote(symbol, payload.get(symbol))
                    if parsed:
                        schwab[symbol] = parsed
    except Exception as exc:
        schwab_error = str(exc) or exc.__class__.__name__

    threshold = _delta_threshold_bps()
    for symbol in normalized:
        primary = schwab.get(symbol)
        secondary = _fetch_yahoo(symbol, timeout=timeout)

        if primary is None:
            if secondary is not None:
                secondary["source"] = FALLBACK_SOURCE_NAME
                secondary["source_role"] = "primary_no_schwab_coverage"
                data[symbol] = secondary
            else:
                reason = "quote unavailable from Schwab and secondary source"
                if schwab_error:
                    reason += f" ({schwab_error})"
                unavailable.append({"symbol": symbol, "reason": reason})
            continue

        primary["source_role"] = "primary"
        primary["primary_source"] = SOURCE_NAME

        if secondary is None:
            data[symbol] = primary
            continue

        delta = _delta_bps(primary, secondary)
        if delta is not None:
            primary["corroborated_by"] = CORROBORATIVE_SOURCE_NAME
            primary["corroboration_delta_bps"] = round(delta, 2)
            primary["delta_threshold_bps"] = threshold

        if delta is not None and delta > threshold:
            secondary["source"] = CORROBORATIVE_SOURCE_NAME
            secondary["source_role"] = "primary_on_delta"
            secondary["displaced_primary_source"] = SOURCE_NAME
            secondary["corroboration_delta_bps"] = round(delta, 2)
            secondary["delta_threshold_bps"] = threshold
            data[symbol] = secondary
        else:
            data[symbol] = primary

    return data, unavailable


__all__ = ["fetch_market_snapshot", "status", "SOURCE_NAME", "FALLBACK_SOURCE_NAME", "CORROBORATIVE_SOURCE_NAME"]
