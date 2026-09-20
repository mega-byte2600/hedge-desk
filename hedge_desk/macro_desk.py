"""Real macro desk: inflation, unemployment, and the fuller yield curve (FRED).

The premium desk's macro context beyond the 2y/10y rates desk: year-over-year CPI
inflation, the unemployment rate, and the 5y/30y points of the official Treasury
curve. All from FRED's free, official, no-auth CSV endpoint — the same proven
transport the rates desk already uses (UA hedge-desk/1.0, HTTP 200 verified).

Honesty and safety:
- Real official observations only. A series that fails to fetch is reported in
  ``blocked`` and its field is omitted — never a fabricated number.
- If EVERY series is blocked, the desk reports mode BLOCKED (not a partial
  "REAL" claim) so a fully-degraded macro panel is never presented as live.
- CPI YoY is computed from the index series (latest vs 12 months prior), a measured
  fact, not a forecast and not advice.
- No order, no probability, no Risk of Ruin.
"""

from __future__ import annotations

import datetime as _dt
from decimal import Decimal
from typing import Callable, Dict, Sequence, Tuple

from hedge_desk.rates_desk import FRED_CSV_URL, _default_transport, _parse_fred_csv

MACRO_VERSION = "hedge-desk-macro-desk-1.0.0"

# Official FRED series ids.
CPI = "CPIAUCSL"      # CPI, all urban consumers, index (monthly)
UNEMPLOYMENT = "UNRATE"  # civilian unemployment rate, % (monthly)
TREASURY_5Y = "DGS5"  # 5-year treasury constant maturity, % (daily)
TREASURY_30Y = "DGS30"  # 30-year treasury constant maturity, % (daily)

# CPI YoY needs ~13 months of index history.
CPI_LOOKBACK_DAYS = 400


def _fetch(series: str, start: _dt.date, end: _dt.date, transport) -> Sequence[Tuple[str, Decimal]] | None:
    """Fetch one FRED series with a small retry for transient network blips.

    Returns the full (date, value) rows so callers can slice locally (e.g. the
    CPI YoY baseline) without a second network fetch. A persistent failure
    returns None (blocked), never a fabricated number. The retry sleeps only
    BETWEEN attempts, not after the final one.
    """
    url = FRED_CSV_URL.format(series=series, start=start.isoformat(), end=end.isoformat())
    for attempt in range(2):
        status, raw = transport(url)
        if status == 200 and raw:
            rows = _parse_fred_csv(raw)
            if rows:
                return rows
        if attempt < 1:  # sleep only between attempts, not after the last
            import time as _time
            _time.sleep(0.5 * (attempt + 1))
    return None


def macro_environment(
    transport: Callable = _default_transport,
    as_of: _dt.date | None = None,
) -> Dict[str, object]:
    """Fetch real inflation, unemployment, and the fuller curve from FRED."""
    end = as_of or _dt.date.today()
    start = end - _dt.timedelta(days=CPI_LOOKBACK_DAYS)

    blocked: list[str] = []
    out: Dict[str, object] = {
        "schema_version": MACRO_VERSION,
        "mode": "REAL_FRED_MACRO",
        "as_of": end.isoformat(),
        "data_source": "fred-public-csv-http-200",
        "trade_authorized": False,
        "blocked": blocked,
    }

    # CPI YoY: latest index vs 12 months prior, from ONE fetch (no re-fetch).
    cpi_rows = _fetch(CPI, start, end, transport)
    if cpi_rows is None:
        blocked.append(CPI)
    else:
        cpi_date, cpi_value = cpi_rows[-1]
        target = _dt.date.fromisoformat(cpi_date) - _dt.timedelta(days=365)
        prior = None
        for d, v in cpi_rows:
            if _dt.date.fromisoformat(d) <= target:
                prior = v
        if prior is not None and prior != 0:
            out["cpi_yoy_pct"] = str(((cpi_value - prior) / prior) * 100)
            out["cpi_latest_date"] = cpi_date
            out["cpi_index"] = str(cpi_value)
        else:
            blocked.append(CPI + "_YOY")

    unemp = _fetch(UNEMPLOYMENT, start, end, transport)
    if unemp is None:
        blocked.append(UNEMPLOYMENT)
    else:
        out["unemployment_rate_pct"] = str(unemp[-1][1])
        out["unemployment_date"] = unemp[-1][0]

    for series, key in ((TREASURY_5Y, "treasury_5y"), (TREASURY_30Y, "treasury_30y")):
        row = _fetch(series, start, end, transport)
        if row is None:
            blocked.append(series)
        else:
            out[key] = str(row[-1][1])
            out[key + "_date"] = row[-1][0]

    # If every series is blocked, this is not a live macro reading — say so.
    if not any(k.startswith(("cpi_", "unemployment_", "treasury_")) for k in out):
        out["mode"] = "BLOCKED"
        out["reason"] = "all_fred_series_blocked"

    out["note"] = (
        "Official FRED observations (CPI YoY, unemployment, 5y/30y curve). "
        "Measured facts, not a forecast and not advice. No order placed."
    )
    return out


__all__ = ["MACRO_VERSION", "macro_environment", "CPI", "UNEMPLOYMENT",
           "TREASURY_5Y", "TREASURY_30Y"]