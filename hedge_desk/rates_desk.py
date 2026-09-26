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
import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
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


def _cache_dir() -> Path | None:
    """Root dir for the FRED observation cache. None disables caching."""
    raw = os.environ.get("HEDGE_DESK_CACHE_DIR", "").strip()
    if raw.lower() in ("0", "false", "no", "off"):
        return None
    return Path(raw) if raw else Path("artifacts/.cache")


def fred_series_rows(
    series: str,
    start: _dt.date,
    end: _dt.date,
    transport: Transport,
    cache_dir: Path | None = None,
    retries: int = 1,
) -> Tuple[Tuple[str, Decimal], ...]:
    """Fetch one FRED daily series, caching the observation window on disk.

    FRED daily series move slowly; the after-close batch re-runs (idempotent)
    and the dashboard rebuild should not re-hit FRED every time. The cache is
    keyed by (series, start, end) so different lookback windows never collide.
    A cache hit returns the stored observations; a miss fetches, parses, and
    stores them atomically (tmp + rename). Transient transport failures are
    retried ``retries`` times with a short backoff; a persistent failure
    raises ValueError (fail closed) — a stale or missing cache is never
    silently served as fresh data.
    """
    cdir = _cache_dir() if cache_dir is None else cache_dir
    cache_file = (
        cdir / "fred" / series / f"{start.isoformat()}_{end.isoformat()}.json"
        if cdir is not None
        else None
    )
    if cache_file is not None and cache_file.is_file():
        try:
            payload = json.loads(cache_file.read_text(encoding="utf-8"))
            if (
                payload.get("series") == series
                and payload.get("start") == start.isoformat()
                and payload.get("end") == end.isoformat()
            ):
                return tuple(
                    (d, Decimal(v)) for d, v in payload.get("rows", [])
                )
        except (ValueError, KeyError, TypeError, ArithmeticError):
            pass  # corrupt cache entry -> fall through to a fresh fetch
    url = FRED_CSV_URL.format(series=series, start=start.isoformat(), end=end.isoformat())
    last_status: int | None = None
    rows: Tuple[Tuple[str, Decimal], ...] = ()
    for attempt in range(retries + 1):
        try:
            status, raw = transport(url)
        except Exception:
            status, raw = 0, b""
        last_status = status
        if status == 200 and raw:
            rows = _parse_fred_csv(raw)
            if rows:
                break
            raise ValueError(f"fred series {series} has no observations")
        if attempt < retries:
            import time as _time
            _time.sleep(0.5 * (attempt + 1))
    if not rows:
        raise ValueError(f"fred fetch failed for {series} (status {last_status})")
    if cache_file is not None:
        try:
            cache_file.parent.mkdir(parents=True, exist_ok=True)
            tmp = cache_file.with_suffix(".tmp")
            tmp.write_text(
                json.dumps(
                    {
                        "series": series,
                        "start": start.isoformat(),
                        "end": end.isoformat(),
                        "rows": [[d, str(v)] for d, v in rows],
                    }
                ),
                encoding="utf-8",
            )
            os.replace(tmp, cache_file)
        except OSError:
            pass  # cache write failure must never fail the batch
    return rows


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

    y2_rows = fred_series_rows(TWO_YEAR, start, end, transport)
    y10_rows = fred_series_rows(TEN_YEAR, start, end, transport)
    y2_date, y2 = y2_rows[-1]
    y10_date, y10 = y10_rows[-1]

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
        # Full observation windows for the dashboard's trend charts.
        "treasury_2y_history": [[d, str(v)] for d, v in y2_rows],
        "treasury_10y_history": [[d, str(v)] for d, v in y10_rows],
        "data_source": "fred-public-csv-http-200",
        "trade_authorized": False,
        "note": (
            "Observations of official FRED daily series. Fed funds/src curve "
            "change is a measured fact, not a forecast and not advice. No order "
            "placed."
        ),
    }


__all__ = ["rates_environment", "FED_FUNDS", "TEN_YEAR", "TWO_YEAR"]