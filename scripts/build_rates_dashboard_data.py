#!/usr/bin/env python3
"""Build the Desk 7 rates-dashboard data file: web/rates-dashboard-data.json.

The dashboard page (web/rates-dashboard.html) fetches this JSON and renders
from it; no data is baked into the page. This generator is the only writer.

Sources (no synthetic data anywhere; a failed series quarantines, never
invents):
  * FRED levels via the keyed helper ONLY, invoked exactly as
    PYTHONPATH=/opt/muse/skills/custom-connector-setup/bin python3
    ~/workspace/custom-connectors/custom.legacy-fred/bin/fred_observations.py
    <SERIES> --limit=N
    Yahoo is not a substitute for FRED here. The helper returns newest-first
    observations with values as strings and "." for missing.
  * Kalshi via direct GET to the trade API, series KXFEDDECISION. Price
    fields carry the _dollars suffix (last_price_dollars, yes_bid_dollars,
    yes_ask_dollars, previous_price_dollars, volume_24h_fp); the bare
    last_price / yes_bid keys return null and must NOT be read as no market.
    The FRONT meeting is the event_ticker group with the nearest future
    close_time — never hardcoded.
  * Meeting calendar + FedWatch note + Michigan marker from the checked-in
    manual file scripts/rates-dashboard-calendar.json (seeded from verified
    reads; the daily worker refreshes it when the cycle turns). The Michigan
    marker stays manual because FRED MICH lags the U-M release; the generator
    carries the latest FRED MICH observation separately as michigan_fred for
    cross-check, never as a silent substitute.

Recompute rules (everything derived from levels, never carried forward):
  * m/m % = round((curr - prev) / prev * 100, 3), consecutive months only.
    The Oct-2025 BLS collection gap (CPIAUCSL jumps Sep 2025 -> Nov 2025)
    renders as a gap, never interpolated.
  * Payroll changes are level diffs, consecutive months only; pay_avg3 is
    the trailing mean of 3 consecutive monthly changes, rounded to 1 decimal.
  * icsa_avg4 is the trailing mean of 4 weekly claims, int(round()).
  * Curve snapshots are the latest close plus the nearest common-date close
    on or before latest-30/60/90 days, actual dates labeled.

Quarantine and core-failure rule:
  * One failed NON-CORE series quarantines: the file still builds, the
    affected key is empty/omitted, and an entry {series, reason} is added to
    `unavailable`. The page shows "data unavailable" for that chart only.
  * CORE inputs are the DGS10 base (base_10y) and the Kalshi front meeting.
    If either fails, this script exits nonzero and writes NOTHING, so the
    daily job keeps the last good JSON. The calendar file is also required:
    a missing or corrupt calendar file exits nonzero.

Skip-if-unchanged: if the payload (excluding generated_at) matches the
existing file, the file is left untouched and the run exits 0. --force
overrides. Writes are atomic (tmp file + replace).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SCHEMA_VERSION = "rates-dashboard-1"

FRED_HELPER = os.environ.get(
    "FRED_HELPER",
    str(Path.home() / "workspace" / "custom-connectors" / "custom.legacy-fred"
        / "bin" / "fred_observations.py"),
)
FRED_PYTHONPATH = os.environ.get(
    "FRED_PYTHONPATH", "/opt/muse/skills/custom-connector-setup/bin"
)
FRED_TIMEOUT_SECONDS = 60

KALSHI_URL = (
    "https://api.elections.kalshi.com/trade-api/v2/markets"
    "?series_ticker=KXFEDDECISION&limit=200"
)
KALSHI_TIMEOUT_SECONDS = 30

# series -> --limit for the FRED helper. Curve/history series need ~70 daily
# observations to cover the 90-day snapshot window; monthly series need 14
# to cover a year of m/m points; MICH is a cross-check only (limit 3).
SERIES_LIMITS = {
    "DTB3": 70,
    "DGS2": 70,
    "DGS5": 70,
    "DGS10": 70,
    "DGS30": 70,
    "T10Y2Y": 70,
    "T10Y3M": 70,
    "BAMLC0A0CM": 70,
    "BAMLH0A0HYM2": 70,
    "CPIAUCSL": 14,
    "CPILFESL": 14,
    "PCEPILFE": 14,
    "PPIFIS": 14,
    "T5YIE": 70,
    "T10YIE": 70,
    "MICH": 3,
    "PAYEMS": 14,
    "UNRATE": 14,
    "ICSA": 30,
    "JTSJOL": 14,
}

TENOR_SERIES = ["DTB3", "DGS2", "DGS5", "DGS10", "DGS30"]
TENOR_LABELS = ["3M", "2Y", "5Y", "10Y", "30Y"]
TENOR_LABEL = dict(zip(TENOR_SERIES, TENOR_LABELS))

INFL_SERIES = ["CPIAUCSL", "CPILFESL", "PCEPILFE", "PPIFIS"]
BE_SERIES = ["T5YIE", "T10YIE"]
SLOPE_SERIES = ["T10Y2Y", "T10Y3M"]
SPREAD_SERIES = {"IG": "BAMLC0A0CM", "HY": "BAMLH0A0HYM2"}

# Kalshi outcome order matches the shipped dashboard (Hike 25bps is the
# highlighted bar, index 1). Labels are keyed by ticker suffix, NOT by the
# API subtitle (the H0 subtitle reads "Fed maintains rate"; the dashboard
# label is "Hike 0bps").
KALSHI_OUTCOMES = [
    ("H26", "Hike >25bps"),
    ("H25", "Hike 25bps"),
    ("H0", "Hike 0bps"),
    ("C26", "Cut >25bps"),
    ("C25", "Cut 25bps"),
]

_MONTHS = {
    "JAN": 1, "FEB": 2, "MAR": 3, "APR": 4, "MAY": 5, "JUN": 6,
    "JUL": 7, "AUG": 8, "SEP": 9, "OCT": 10, "NOV": 11, "DEC": 12,
}
_MONTH_ABBR = {v: k for k, v in _MONTHS.items()}
_MEETING_RE = re.compile(r"(\d{2})(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)$")


class CoreDataError(RuntimeError):
    """A core input failed: the run must exit nonzero and write nothing."""


def parse_fred_observations(stdout: str, series: str) -> list[tuple[str, float]]:
    """Parse keyed-helper output into ascending [(date, value)] pairs.

    The helper returns newest-first JSON: {"SERIES": [{"date": ..., "value":
    "..."}]}. Values are strings; "." is the missing marker and is skipped.
    Duplicate dates collapse, the last non-missing value winning. A
    non-numeric, non-"." value is a corrupt payload and raises.
    """
    try:
        data = json.loads(stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"FRED helper returned unparseable JSON for {series}: {exc}") from exc
    rows = data.get(series)
    if not isinstance(rows, list):
        raise RuntimeError(f"FRED helper returned no observations list for {series}")
    by_date: dict[str, float] = {}
    for row in rows:
        raw = row.get("value")
        if raw == "." or raw is None:
            continue
        try:
            value = float(raw)
        except (TypeError, ValueError) as exc:
            raise RuntimeError(
                f"FRED helper returned non-numeric value {raw!r} for {series}"
            ) from exc
        by_date[str(row["date"])] = value
    if not by_date:
        raise RuntimeError(f"FRED helper returned no usable observations for {series}")
    return [(d, by_date[d]) for d in sorted(by_date)]


def fetch_fred_series(series: str, limit: int) -> list[tuple[str, float]]:
    """Fetch one FRED series through the keyed helper. Raises on failure."""
    env = dict(os.environ)
    env["PYTHONPATH"] = FRED_PYTHONPATH
    try:
        # NOTE: the helper honors ONLY the --limit=N form (with "="); a
        # space-separated --limit N is silently ignored and the number is
        # treated as a series id, yielding just 1 observation per series.
        proc = subprocess.run(
            [sys.executable, FRED_HELPER, series, f"--limit={limit}"],
            capture_output=True,
            text=True,
            timeout=FRED_TIMEOUT_SECONDS,
            env=env,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"FRED helper timed out for {series} after {FRED_TIMEOUT_SECONDS}s") from exc
    if proc.returncode != 0:
        tail = (proc.stderr or "").strip().splitlines()[-1:] or [""]
        raise RuntimeError(f"FRED helper failed for {series} (exit {proc.returncode}): {tail[0]}")
    return parse_fred_observations(proc.stdout, series)


def fetch_kalshi_markets() -> list[dict]:
    """GET the KXFEDDECISION markets from the Kalshi trade API."""
    req = urllib.request.Request(
        KALSHI_URL, headers={"User-Agent": "hedge-desk-rates-dashboard/1.0"}
    )
    try:
        with urllib.request.urlopen(req, timeout=KALSHI_TIMEOUT_SECONDS) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as exc:  # network, timeout, JSON: all core failures
        raise RuntimeError(f"Kalshi API request failed: {exc}") from exc
    markets = data.get("markets")
    if not isinstance(markets, list) or not markets:
        raise RuntimeError("Kalshi API returned no markets for KXFEDDECISION")
    return markets


def meeting_label_from_event_ticker(event_ticker: str) -> str:
    """'KXFEDDECISION-26DEC' -> 'Dec-2026'. Falls back to the raw ticker."""
    match = _MEETING_RE.search(event_ticker)
    if not match:
        return event_ticker
    year = 2000 + int(match.group(1))
    month = _MONTHS[match.group(2)]
    return f"{_MONTH_ABBR[month].title()}-{year}"


def _kalshi_number(market: dict, field: str) -> float:
    """Parse one Kalshi _dollars/_fp field. Null or missing is a failure;
    0.0 is a legitimate value (e.g. a 0.00 bid) and must not fail."""
    raw = market.get(field)
    if raw is None:
        raise CoreDataError(
            f"Kalshi market {market.get('ticker')} missing {field}"
        )
    try:
        return float(raw)
    except (TypeError, ValueError) as exc:
        raise CoreDataError(
            f"Kalshi market {market.get('ticker')} has non-numeric {field}: {raw!r}"
        ) from exc


def select_front_meeting(
    markets: list[dict], now: datetime
) -> dict:
    """Pick the front FOMC meeting: the event_ticker group with the nearest
    future close_time. Returns {event_ticker, meeting_label, outcomes}.

    All five outcomes must be present with all five numeric fields parsed
    from the _dollars/_fp keys; anything less is a core failure.
    """
    groups: dict[str, list[dict]] = {}
    closes: dict[str, datetime] = {}
    for market in markets:
        event = market.get("event_ticker")
        close_raw = market.get("close_time")
        if not event or not close_raw:
            continue
        try:
            close = datetime.fromisoformat(str(close_raw).replace("Z", "+00:00"))
        except ValueError:
            continue
        if close <= now:
            continue
        groups.setdefault(event, []).append(market)
        if event not in closes or close < closes[event]:
            closes[event] = close
    if not groups:
        raise CoreDataError("Kalshi returned no future KXFEDDECISION meetings")
    front = min(groups, key=lambda e: (closes[e], e))
    by_suffix = {}
    for market in groups[front]:
        suffix = str(market.get("ticker", "")).rsplit("-", 1)[-1]
        by_suffix[suffix] = market
    outcomes = []
    for suffix, label in KALSHI_OUTCOMES:
        market = by_suffix.get(suffix)
        if market is None:
            raise CoreDataError(f"Kalshi front meeting {front} missing outcome {suffix}")
        outcomes.append({
            "label": label,
            "price": _kalshi_number(market, "last_price_dollars"),
            "bid": _kalshi_number(market, "yes_bid_dollars"),
            "ask": _kalshi_number(market, "yes_ask_dollars"),
            "prev": _kalshi_number(market, "previous_price_dollars"),
            "vol24h": _kalshi_number(market, "volume_24h_fp"),
        })
    return {
        "event_ticker": front,
        "meeting_label": meeting_label_from_event_ticker(front),
        "outcomes": outcomes,
    }


def _is_consecutive_month(prev: str, curr: str) -> bool:
    """True only if curr is exactly one calendar month after prev."""
    py, pm = int(prev[:4]), int(prev[5:7])
    cy, cm = int(curr[:4]), int(curr[5:7])
    return (cy, cm) == (py + (pm == 12), pm % 12 + 1)


def monthly_pct_changes(obs: list[tuple[str, float]]) -> list[list]:
    """Consecutive-month m/m % changes, rounded to 3 decimals. Gaps (e.g.
    the Oct-2025 BLS collection gap) produce no point, never an
    interpolated one."""
    out = []
    for (prev_date, prev_val), (curr_date, curr_val) in zip(obs, obs[1:]):
        if not _is_consecutive_month(prev_date, curr_date):
            continue
        if prev_val == 0:
            continue
        out.append([curr_date, round((curr_val - prev_val) / prev_val * 100, 3)])
    return out


def level_changes(obs: list[tuple[str, float]]) -> list[list]:
    """Consecutive-month level diffs (payrolls)."""
    out = []
    for (prev_date, prev_val), (curr_date, curr_val) in zip(obs, obs[1:]):
        if not _is_consecutive_month(prev_date, curr_date):
            continue
        out.append([curr_date, curr_val - prev_val])
    return out


def trailing_avg_consecutive(
    changes: list[list], window: int, ndigits: int
) -> list[list]:
    """Trailing mean over `window` changes, requiring the window's dates to
    be consecutive months. Used for pay_avg3 (window 3, 1 decimal)."""
    out = []
    for i in range(window - 1, len(changes)):
        window_dates = [c[0] for c in changes[i - window + 1 : i + 1]]
        if all(
            _is_consecutive_month(a, b)
            for a, b in zip(window_dates, window_dates[1:])
        ):
            mean = sum(c[1] for c in changes[i - window + 1 : i + 1]) / window
            out.append([changes[i][0], round(mean, ndigits)])
    return out


def trailing_avg(changes: list[list], window: int) -> list[list]:
    """Trailing mean over `window` points, int(round()). Used for icsa_avg4."""
    out = []
    for i in range(window - 1, len(changes)):
        mean = sum(c[1] for c in changes[i - window + 1 : i + 1]) / window
        out.append([changes[i][0], int(round(mean))])
    return out


def curve_snapshots(
    hist: dict[str, list[tuple[str, float]]]
) -> list[dict]:
    """Latest + ~30/60/90-day-ago closes from dates present in ALL five
    tenor series. For each target, the nearest common date on or before
    latest-offset; a target with no common date on or before it is skipped.
    Actual dates are labeled."""
    common = None
    by_tenor: dict[str, dict[str, float]] = {}
    for series in TENOR_SERIES:
        obs = hist.get(series)
        if not obs:
            return []
        by_tenor[series] = dict(obs)
        dates = set(by_tenor[series])
        common = dates if common is None else common & dates
    if not common:
        return []
    latest = max(common)
    latest_d = date.fromisoformat(latest)
    snapshots = []
    for offset, label in (
        (0, "Latest"),
        (30, "~30d ago"),
        (60, "~60d ago"),
        (90, "~90d ago"),
    ):
        target = latest_d - timedelta(days=offset)
        candidates = [d for d in common if date.fromisoformat(d) <= target]
        if not candidates:
            continue
        chosen = max(candidates)
        snapshots.append({
            "label": f"{label} ({chosen})",
            "date": chosen,
            "y": [by_tenor[s][chosen] for s in TENOR_SERIES],
        })
    return snapshots


def load_calendar(path: Path) -> dict:
    """Load the checked-in manual calendar file. Missing/corrupt is fatal:
    the dashboard cannot be built complete without it."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CoreDataError(f"calendar file {path} unreadable: {exc}") from exc
    for key in ("calendar", "fedwatch_note", "meeting_label", "michigan"):
        if key not in data:
            raise CoreDataError(f"calendar file {path} missing required key {key!r}")
    return data


def build_payload(
    series: dict[str, list[tuple[str, float]] | None],
    kalshi: dict,
    calendar: dict,
    generated_at: str,
    unavailable: list[dict],
) -> dict:
    """Assemble the dashboard payload. `series` maps series id to ascending
    observations or None (quarantined). `unavailable` already carries the
    fetch failures; derivation gaps are appended here."""
    dgs10 = series.get("DGS10")
    if not dgs10:
        raise CoreDataError("DGS10 base missing: core input failed")
    if not kalshi or not kalshi.get("outcomes"):
        raise CoreDataError("Kalshi front meeting missing: core input failed")

    def pairs(series_id: str) -> list[list] | None:
        obs = series.get(series_id)
        if not obs:
            return None
        return [[d, v] for d, v in obs]

    as_of = max(
        obs[-1][0] for obs in series.values() if obs
    )

    # Curve history: only tenors that pulled. Snapshots need all five.
    curve_hist = {}
    for series_id in TENOR_SERIES:
        p = pairs(series_id)
        if p is not None:
            curve_hist[TENOR_LABEL[series_id]] = p
    hist = {s: series[s] for s in TENOR_SERIES if series.get(s)}
    snapshots = curve_snapshots(hist) if len(hist) == len(TENOR_SERIES) else []
    if not snapshots and len(hist) == len(TENOR_SERIES):
        unavailable.append({
            "series": "snapshots",
            "reason": "no common observation date across the five tenor series",
        })

    base_10y_date, base_10y = dgs10[-1]

    infl = {}
    for series_id in INFL_SERIES:
        obs = series.get(series_id)
        if obs:
            infl[series_id] = monthly_pct_changes(obs)

    be = {}
    for series_id in BE_SERIES:
        p = pairs(series_id)
        if p is not None:
            be[series_id] = p

    pay_obs = series.get("PAYEMS")
    pay_chg = level_changes(pay_obs) if pay_obs else []
    pay_avg3 = trailing_avg_consecutive(pay_chg, 3, 1) if pay_chg else []

    unrate = pairs("UNRATE") or []
    icsa = pairs("ICSA") or []
    icsa_avg4 = trailing_avg(icsa, 4) if icsa else []
    jolts = pairs("JTSJOL") or []

    slopes = {}
    for series_id in SLOPE_SERIES:
        p = pairs(series_id)
        if p is not None:
            slopes[series_id] = p

    spreads = {}
    for label, series_id in SPREAD_SERIES.items():
        p = pairs(series_id)
        if p is not None:
            spreads[label] = p

    mich = series.get("MICH")
    michigan_fred = None
    if mich:
        michigan_fred = {"value": mich[-1][1], "date": mich[-1][0]}

    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": generated_at,
        "as_of": as_of,
        "source": "FRED (keyed helper), Kalshi trade API (KXFEDDECISION), "
                  "federalreserve.gov + U-M Surveys of Consumers via "
                  "scripts/rates-dashboard-calendar.json",
        "tenor_labels": list(TENOR_LABELS),
        "snapshots": snapshots,
        "curve_hist": curve_hist,
        "base_10y": base_10y,
        "base_10y_date": base_10y_date,
        "kalshi": kalshi["outcomes"],
        "kalshi_meeting_label": kalshi["meeting_label"],
        "kalshi_event_ticker": kalshi["event_ticker"],
        "infl": infl,
        "be": be,
        "pay_chg": pay_chg,
        "pay_avg3": pay_avg3,
        "unrate": unrate,
        "icsa": icsa,
        "icsa_avg4": icsa_avg4,
        "jolts": jolts,
        "slopes": slopes,
        "spreads": spreads,
        "michigan": calendar["michigan"],
        "michigan_fred": michigan_fred,
        "manual": {
            "calendar": calendar["calendar"],
            "fedwatch_note": calendar["fedwatch_note"],
            "meeting_label": calendar["meeting_label"],
            "source": calendar.get("source", ""),
            "read_date": calendar.get("read_date", ""),
        },
        "unavailable": unavailable,
    }


def payload_unchanged(path: Path, payload: dict) -> bool:
    """True if the existing file matches the new payload on every key
    except generated_at. Missing or corrupt existing file -> False."""
    try:
        existing = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    existing = {k: v for k, v in existing.items() if k != "generated_at"}
    new = {k: v for k, v in payload.items() if k != "generated_at"}
    return existing == new


def _write_atomic(path: Path, payload: dict) -> None:
    # No sort_keys: insertion order is meaningful (tenor order, inflation
    # series order) and the page iterates the JSON's key order for traces.
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--out",
        default=str(ROOT / "web" / "rates-dashboard-data.json"),
        help="Output JSON path (default: web/rates-dashboard-data.json)",
    )
    parser.add_argument(
        "--calendar",
        default=str(ROOT / "scripts" / "rates-dashboard-calendar.json"),
        help="Manual calendar file (default: scripts/rates-dashboard-calendar.json)",
    )
    parser.add_argument("--force", action="store_true", help="Rewrite even if unchanged")
    args = parser.parse_args(argv)

    try:
        calendar = load_calendar(Path(args.calendar))
    except CoreDataError as exc:
        print(f"rates-dashboard-data: refusing to build: {exc}", file=sys.stderr)
        return 2

    series: dict[str, list[tuple[str, float]] | None] = {}
    unavailable: list[dict] = []
    for series_id, limit in SERIES_LIMITS.items():
        try:
            series[series_id] = fetch_fred_series(series_id, limit)
        except Exception as exc:
            print(f"rates-dashboard-data: quarantined {series_id}: {exc}", file=sys.stderr)
            series[series_id] = None
            unavailable.append({"series": series_id, "reason": str(exc)})

    try:
        markets = fetch_kalshi_markets()
        kalshi = select_front_meeting(markets, datetime.now(timezone.utc))
    except Exception as exc:
        print(f"rates-dashboard-data: core input failed (Kalshi): {exc}", file=sys.stderr)
        return 2

    generated_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    try:
        payload = build_payload(series, kalshi, calendar, generated_at, unavailable)
    except CoreDataError as exc:
        print(f"rates-dashboard-data: core input failed: {exc}", file=sys.stderr)
        return 2

    out = Path(args.out)
    if not args.force and payload_unchanged(out, payload):
        print(f"rates-dashboard-data: unchanged, kept {out}")
        return 0
    _write_atomic(out, payload)
    print(
        f"rates-dashboard-data: wrote {out} (as_of {payload['as_of']}, "
        f"{len(unavailable)} unavailable)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
