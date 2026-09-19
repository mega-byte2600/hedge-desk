"""Real rates/bond desk on FRED daily data (free, official).

Pulls the Federal Reserve's own daily series (FRED CSV) and reports the actual
rate environment: the fed-funds effective rate, a benchmark treasury yield, the
nominal curve's short-vs-long shape, and the observed change in the fed funds rate
across the lookback window. All arithmetic is the already-tested closed-form in
``hedge_desk.rates_futures`` (curve_slope / curve_shape).

Honesty boundary:
- These are OBSERVATIONS of official FRED data, not a forecast and not advice.
- A change in the fed funds rate is reported as a measured fact from the series.
  This rhythm is context for the overnight desk; it is not a directional trade.
- No order is placed; this desk makes no trade_authorized decision.

Source: https://fred.stlouisfed.org/graph/fredgraph.csv?id=<SERIES>&cosd=..&coed=..
License: FRED data is free for many uses; this is reference use of official
series and retains no redistributed payload.
"""

from __future__ import annotations

import datetime as _dt
import urllib.error
import urllib.request
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Callable, Dict, Tuple

from hedge_desk.rates_futures import curve_shape, curve_slope

FRED_CSV_URL = (
    "https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}"
    "&cosd={start}&coed={end}"
)
Transport = Callable[[str], Tuple[int, bytes]]

# Official FRED series ids.
FED_FUNDS = "DFF"          # effective federal funds rate, %
TEN_YEAR = "DGS10"         # 10-year treasury constant maturity, %
TWO_YEAR = "DGS2"          # 2-year treasury constant maturity, %


def _default_transport(url: str) -> Tuple[int, bytes]:
    req = urllib.request.Request(url, headers={"User-Agent": "hedge-desk/1.0"})
    try:
        # FRED normally answers in <2s; a short timeout makes a down/slow FRED
        # fail fast so the after-close batch is bounded, not stalled for minutes.
        with urllib.request.urlopen(req, timeout=8) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()
    except Exception as exc:
        return 0, str(exc).encode("utf-8")


def _num(value: str) -> Decimal | None:
    value = value.strip()
    if value == "":
        return None
    try:
        parsed = Decimal(value)
        return parsed if parsed.is_finite() else None
    except (InvalidOperation, ValueError):
        return None


def _parse_fred_csv(raw: bytes) -> Tuple[Tuple[str, Decimal], ...]:
    """Parse a FRED CSV (two columns: observation_date, <series>)."""
    rows = []
    for line in raw.decode("utf-8").strip().splitlines():
        if line.startswith("observation_date"):
            continue
        if not line.strip():
            continue
        parts = line.split(",")
        if len(parts) < 2:
            continue
        value = _num(parts[1])
        if value is None:
            continue
        rows.append((parts[0], value))
    return tuple(rows)


def _fetch_series(series, start, end, transport) -> Tuple[str, Decimal]:
    url = FRED_CSV_URL.format(series=series, start=start.isoformat(), end=end.isoformat())
    status, raw = transport(url)
    if status != 200 or not raw:
        raise ValueError(f"fred fetch failed for {series} (status {status})")
    rows = _parse_fred_csv(raw)
    if not rows:
        raise ValueError(f"fred series {series} has no observations")
    return rows[-1]


def _lookback_dates(days: int) -> Tuple[_dt.date, _dt.date]:
    end = _dt.date.today()
    start = end - _dt.timedelta(days=days)
    return start, end


def rates_environment(
    lookback_days: int = 60,
    transport: Transport = _default_transport,
    as_of: _dt.date | None = None,
) -> Dict[str, object]:
    """Fetch the real rate environment and report the measured curve + fed change."""
    if lookback_days < 1 or type(lookback_days) is not int:
        raise ValueError("lookback_days must be a positive integer")
    end = as_of or _dt.date.today()
    start = end - _dt.timedelta(days=lookback_days)

    # Fetch the fed funds series ONCE for the whole window; the earliest
    # observation is the prior-period baseline for the change, and the latest is
    # the current effective rate. Single fetch, fail closed on non-200 so a
    # transport error can never fabricate a "0.00 change" in a published report.
    ff_url = FRED_CSV_URL.format(
        series=FED_FUNDS, start=start.isoformat(), end=end.isoformat()
    )
    ff_status, ff_raw = transport(ff_url)
    if ff_status != 200 or not ff_raw:
        raise ValueError(f"fred fetch failed for {FED_FUNDS} (status {ff_status})")
    ff_series = _parse_fred_csv(ff_raw)
    if not ff_series:
        raise ValueError(f"fred series {FED_FUNDS} has no observations")
    ff_date, ff = ff_series[-1]
    ff_earliest = ff_series[0][1]

    y2_date, y2 = _fetch_series(TWO_YEAR, start, end, transport)
    y10_date, y10 = _fetch_series(TEN_YEAR, start, end, transport)

    # 2y vs 10y slope (tenors in years) -> curve shape.
    slope = curve_slope(((2, y2), (10, y10)))
    shape = curve_shape(slope)

    return {
        "schema_version": "hedge-desk-rates-desk-1.0.0",
        "mode": "REAL_FRED_RATES",
        "as_of": end.isoformat(),
        "fed_funds_effective_rate": str(ff),
        "fed_funds_latest_date": ff_date,
        "fed_funds_change_over_window": str(ff - ff_earliest),
        "treasury_2y": str(y2),
        "treasury_2y_date": y2_date,
        "treasury_10y": str(y10),
        "treasury_10y_date": y10_date,
        "spread_10y_2y_points": str((y10 - y2) * 100),
        "curve_slope": str(slope),
        "curve_shape": shape,
        "lookback_days": lookback_days,
        "data_source": "fred-public-csv-http-200",
        "trade_authorized": False,
        "note": (
            "Observations of official FRED daily series. Fed funds/src curve "
            "change is a measured fact, not a forecast and not advice. No order "
            "placed."
        ),
    }


__all__ = ["rates_environment", "FED_FUNDS", "TEN_YEAR", "TWO_YEAR"]