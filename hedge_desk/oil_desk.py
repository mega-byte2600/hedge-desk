"""WTI front-month oil desk on Yahoo Finance public chart data (free).

Pulls the front-month WTI crude futures contract (``CL=F``) daily closes from
Yahoo Finance's public chart endpoint and reports the observed last close, the
as-of date, and the measured net change across the lookback window.

Honesty boundary:
- These are OBSERVATIONS of public Yahoo Finance chart data, not a forecast
  and not advice.
- A change in the front-month price is a reported measured fact. It is
  context for the nightly macro read; it is not a directional trade signal.
- No order is placed; this desk makes no trade_authorized decision.
- Paper research context only: observations feed the AM report's macro
  section, never an execution path.

Source: https://query1.finance.yahoo.com/v8/finance/chart/CL=F?range=..&interval=1d
(the same public ``yahoo-public-chart-v8`` endpoint as the EOD ingest).
"""

from __future__ import annotations

import datetime as _dt
import json
import urllib.error
import urllib.request
from decimal import Decimal, InvalidOperation
from typing import Callable, Dict, Tuple

from hedge_desk.data.eod_ingest import EOD_SOURCE_ID, YAHOO_CHART_URL

OIL_DESK_SCHEMA_VERSION = "hedge-desk-oil-desk-1.0.0"
WTI_SYMBOL = "CL=F"
Transport = Callable[[str], Tuple[int, bytes]]


def _default_transport(url: str) -> Tuple[int, bytes]:
    req = urllib.request.Request(
        url, headers={"Accept": "application/json", "User-Agent": "hedge-desk/1.0"}
    )
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()
    except Exception as exc:
        return 0, str(exc).encode("utf-8")


def _range_for_lookback(lookback_days: int) -> str:
    """Pick the smallest Yahoo range that covers the lookback window."""
    if lookback_days <= 5:
        return "5d"
    if lookback_days <= 30:
        return "1mo"
    if lookback_days <= 90:
        return "3mo"
    return "6mo"


def _parse_wti_closes(raw: bytes) -> Tuple[Tuple[str, Decimal], ...]:
    """Parse a Yahoo v8 chart payload into (ISO date, close) pairs.

    Raises ValueError (fail closed) on any malformed, empty, or non-numeric
    payload — never an invented price.
    """
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as exc:
        raise ValueError(
            f"yahoo chart payload is not JSON for {WTI_SYMBOL}"
        ) from exc
    try:
        result = payload["chart"]["result"][0]
    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError(
            f"yahoo chart payload has no result for {WTI_SYMBOL}"
        ) from exc
    meta = result.get("meta") or {}
    if meta.get("symbol") and str(meta["symbol"]).upper() != WTI_SYMBOL:
        raise ValueError(f"yahoo chart symbol mismatch for {WTI_SYMBOL}")
    timestamps = result.get("timestamp") or []
    indicators = result.get("indicators") or {}
    quotes = indicators.get("quote") or []
    first_quote = quotes[0] if quotes else {}
    closes = first_quote.get("close") or []
    if not isinstance(timestamps, list) or not timestamps:
        raise ValueError(f"yahoo chart payload is empty for {WTI_SYMBOL}")
    if len(closes) != len(timestamps):
        raise ValueError(f"yahoo chart series length mismatch for {WTI_SYMBOL}")
    rows = []
    for ts, close in zip(timestamps, closes):
        if close is None:
            raise ValueError(f"yahoo chart has a null close for {WTI_SYMBOL}")
        try:
            price = Decimal(str(close))
        except (InvalidOperation, ValueError) as exc:
            raise ValueError(
                f"yahoo chart close is not numeric for {WTI_SYMBOL}"
            ) from exc
        if not price.is_finite():
            raise ValueError(f"yahoo chart close is not finite for {WTI_SYMBOL}")
        day = _dt.datetime.fromtimestamp(int(ts), tz=_dt.timezone.utc).date()
        rows.append((day.isoformat(), price))
    if not rows:
        raise ValueError(f"yahoo chart payload has no closes for {WTI_SYMBOL}")
    return tuple(rows)


def oil_market(
    transport: Transport | None = None,
    lookback_days: int = 5,
) -> Dict[str, object]:
    """Fetch front-month WTI (CL=F) daily closes and report the observed market.

    Returns the last close (Decimal), the first close of the lookback window,
    and the measured net change across the window — observations only.
    """
    if type(lookback_days) is not int or lookback_days < 1:
        raise ValueError("lookback_days must be a positive integer")
    fetch = transport or _default_transport
    url = YAHOO_CHART_URL.format(
        symbol=WTI_SYMBOL, range_param=_range_for_lookback(lookback_days)
    )
    status, raw = fetch(url)
    if status != 200 or not raw:
        raise ValueError(f"yahoo chart fetch failed for {WTI_SYMBOL} (status {status})")
    rows = _parse_wti_closes(raw)
    # The window is the last lookback_days+1 closes, so the net change spans
    # the lookback horizon; when fewer closes exist, use what is there.
    window = rows[-(lookback_days + 1):] if len(rows) > lookback_days + 1 else rows
    first_date, first_close = window[0]
    last_date, last_close = window[-1]
    return {
        "schema_version": OIL_DESK_SCHEMA_VERSION,
        "mode": "REAL_YAHOO_WTI",
        "symbol": WTI_SYMBOL,
        "as_of": last_date,
        "last_close": str(last_close),
        "window_first_date": first_date,
        "window_first_close": str(first_close),
        "net_change_over_window": str(last_close - first_close),
        "observation_count": len(window),
        "lookback_days": lookback_days,
        "data_source": EOD_SOURCE_ID,
        "trade_authorized": False,
        "note": (
            "Front-month WTI crude (CL=F) daily closes observed from public "
            "Yahoo Finance chart data. Net change is a measured fact over the "
            "lookback window, not a forecast and not advice. No order placed; "
            "no trade authorized."
        ),
    }


__all__ = ["OIL_DESK_SCHEMA_VERSION", "WTI_SYMBOL", "oil_market"]
