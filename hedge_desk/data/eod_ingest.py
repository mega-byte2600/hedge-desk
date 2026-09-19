"""Real end-of-day equities ingestion from Yahoo Finance's public chart API.

This is the first increment of the true-MVP re-scope (docs/MVP_RESCOPE_2026.md):
an EOD batch pull that is NOT synthetic. It fetches daily closes for a
watchlist at end of day (or any point after a trading day), validates the raw
payload is non-empty, point-in-time-consistent, and dollar/value-parseable, then
hashes it into a ``DataArtifact`` and a deterministic ``BatchManifest`` using the
existing immutable data contracts.

Source and licensing posture (matches docs/architecture/DATA_SOURCE_ARCHITECTURE.md
Tier-0 free/open stack):
- Public non-authenticated quote endpoint returning delayed daily OHLCV. This is
  discovery-grade reference data for research, not a licensed execution feed.
- Only normalized low-frequency fields (date, open, high, low, close, volume)
  are retained as artifacts. No redistribution claim is made; ``redistribution_allowed``
  is False.
- Fail closed: a missing, empty, or malformed payload for any symbol produces a
  QUARANTINE/REJECT row in the batch and never an invented quote.

This module places NO order and computes NO probability or Risk of Ruin. It
validates provenance (the provenance gate's job) and then stops at the immutable
artifact boundary. It does not estimate market value or make a trade decision.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
import urllib.error
import urllib.request
from typing import Callable, Dict, Sequence, Tuple

from hedge_desk.data.batch import (
    BatchManifest,
    SourceBatchResult,
    SourceBatchStatus,
    build_batch_manifest,
)
from hedge_desk.data.contracts import DataArtifact

EOD_INGEST_VERSION = "hedge-desk-eod-ingest-1.0.0"
EOD_SOURCE_ID = "yahoo-public-chart-v8"
YAHOO_CHART_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range={range_param}&interval=1d"
DEFAULT_YAHOO_RANGE = "5d"   # lightweight daily batch
FEATURE_YAHOO_RANGE = "3mo"  # enough history for 1/5/21-day + realized-vol features

# Transport injection for deterministic tests.
Transport = Callable[[str], Tuple[int, bytes]]


@dataclass(frozen=True)
class EodDay:
    date: str  # ISO date of the trading day
    close: str  # decimal string close
    open: str
    high: str
    low: str
    volume: int


@dataclass(frozen=True)
class EodSymbolResult:
    symbol: str
    status: SourceBatchStatus
    reason_codes: Tuple[str, ...]
    days: Tuple[EodDay, ...]
    artifact_sha256: str
    source_as_of: datetime
    received_at: datetime


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


def _canonical_payload(symbol: str, days: Sequence[EodDay]) -> str:
    """Deterministic, sorted JSON text used as the artifact content hash."""
    rows = sorted(
        (
            {
                "date": day.date,
                "open": day.open,
                "high": day.high,
                "low": day.low,
                "close": day.close,
                "volume": day.volume,
            }
            for day in days
        ),
        key=lambda row: row["date"],
    )
    body = {
        "schema_version": f"{EOD_INGEST_VERSION}",
        "source_id": EOD_SOURCE_ID,
        "symbol": symbol,
        "days": rows,
    }
    return json.dumps(body, sort_keys=True, separators=(",", ":"))


def _decimal_ok(value: str) -> bool:
    if not isinstance(value, str) or not value:
        return False
    try:
        parsed = float(value)
        return parsed == parsed  # NaN check
    except ValueError:
        return False


def _parse_chart_payload(symbol: str, raw: bytes) -> Tuple[Tuple[EodDay, ...], str]:
    """Parse Yahoo v8 chart JSON into EodDay rows plus a reason code on failure."""
    try:
        data = json.loads(raw.decode("utf-8"))
        result = data["chart"]["result"][0]
        timestamps = result.get("timestamp") or []
        quote = result["indicators"]["quote"][0]
    except (KeyError, IndexError, TypeError, ValueError, UnicodeDecodeError):
        return (), "PAYLOAD_MALFORMED"
    meta = result.get("meta") or {}
    symbol_from_meta = meta.get("symbol", "")
    if symbol_from_meta and symbol_from_meta.upper() != symbol.upper():
        return (), "SYMBOL_MISMATCH"
    if not isinstance(timestamps, list) or not timestamps:
        return (), "EMPTY_PAYLOAD"
    closes = quote.get("close") or []
    opens = quote.get("open") or []
    highs = quote.get("high") or []
    lows = quote.get("low") or []
    volumes = quote.get("volume") or []
    if not (len(closes) == len(timestamps) == len(opens) == len(highs) == len(lows) == len(volumes)):
        return (), "SERIES_LENGTH_MISMATCH"
    rows = []
    for ts, close, open_, high, low, volume in zip(
        timestamps, closes, opens, highs, lows, volumes
    ):
        if close is None or open_ is None or high is None or low is None:
            return (), "SERIES_HAS_NULL_PRICE"
        day_date = datetime.fromtimestamp(int(ts), tz=timezone.utc).date().isoformat()
        vals = {
            "date": day_date,
            "open": str(float(open_)),
            "high": str(float(high)),
            "low": str(float(low)),
            "close": str(float(close)),
        }
        if not all(_decimal_ok(v) for v in (vals["open"], vals["high"], vals["low"], vals["close"])):
            return (), "NON_NUMERIC_PRICE"
        if not isinstance(volume, (int, float)) or volume < 0:
            return (), "INVALID_VOLUME"
        rows.append(
            EodDay(day_date, vals["close"], vals["open"], vals["high"], vals["low"], int(volume))
        )
    if not rows:
        return (), "NO_VALID_DAYS"
    return tuple(rows), ""


def ingest_eod(
    symbols: Sequence[str],
    decision_cutoff: datetime,
    transport: Transport = _default_transport,
    prior_manifest_sha256: str = "0" * 64,
    range_param: str = DEFAULT_YAHOO_RANGE,
) -> Dict[str, object]:
    """Pull EOD daily bars for a watchlist and return a validated batch result.

    Returns a plain dict (schema-versioned) so callers are not coupled to a
    parsed dataclass. Each symbol's row carries its own PASS/QUARANTINE/REJECT
    status; the aggregate ``BatchManifest`` decides READY/INCOMPLETE/etc.
    ``range_param`` controls the Yahoo window (default 5d; use FEATURE_YAHOO_RANGE
    for a feature plane that needs 1/5/21-day history).
    """
    if not symbols:
        raise ValueError("eod watchlist cannot be empty")
    if decision_cutoff.tzinfo is None:
        raise ValueError("eod decision cutoff must be timezone-aware")
    if not isinstance(prior_manifest_sha256, str) or len(prior_manifest_sha256) != 64:
        raise ValueError("eod prior manifest hash invalid")

    results: list[EodSymbolResult] = []
    in_epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    for symbol in symbols:
        url = YAHOO_CHART_URL.format(symbol=symbol, range_param=range_param)
        status, raw = transport(url)
        received_at = datetime.now(timezone.utc)
        if status != 200 or not raw:
            results.append(
                EodSymbolResult(
                    symbol,
                    SourceBatchStatus.QUARANTINE,
                    ("TRANSPORT_FAILED",) if status not in (404,) else ("SYMBOL_UNKNOWN",),
                    (),
                    "0" * 64,
                    datetime(1970, 1, 1, tzinfo=timezone.utc),
                    received_at,
                )
            )
            continue
        days, reason = _parse_chart_payload(symbol, raw)
        if not days:
            results.append(
                EodSymbolResult(
                    symbol, SourceBatchStatus.REJECT, (reason,), (), "0" * 64,
                    datetime(1970, 1, 1, tzinfo=timezone.utc), received_at,
                )
            )
            continue
        payload_text = _canonical_payload(symbol, days)
        artifact_hash = sha256(payload_text.encode("utf-8")).hexdigest()
        # Point-in-time: last day's date must not be after the decision cutoff.
        last_day = max(days, key=lambda d: d.date)
        if last_day.date > decision_cutoff.date().isoformat():
            results.append(
                EodSymbolResult(
                    symbol, SourceBatchStatus.REJECT, ("FUTURE_DAY",), (), "0" * 64,
                    datetime(1970, 1, 1, tzinfo=timezone.utc), received_at,
                )
            )
            continue
        results.append(
            EodSymbolResult(
                symbol, SourceBatchStatus.PASS, (), days, artifact_hash,
                # Real source as-of: the last trading day's date, NOT the moment
                # we asked. Stamping decision_cutoff here would make the freshness
                # gate trivially pass and misrepresent the data's actual age.
                datetime.fromisoformat(last_day.date + "T00:00:00+00:00"),
                received_at,
            )
        )

    ordered = tuple(sorted(results, key=lambda item: item.symbol))
    source_results = tuple(
        SourceBatchResult(item.symbol, item.status, item.artifact_sha256, item.reason_codes)
        for item in ordered
    )
    manifest = build_batch_manifest(
        f"eod-{decision_cutoff.isoformat()}",
        tuple(sorted(symbols)),
        source_results,
        sha256(EOD_INGEST_VERSION.encode("utf-8")).hexdigest(),
        prior_manifest_sha256,
    )
    artifacts = {
        str(item.symbol): DataArtifact(
            artifact_id=f"eod-{item.symbol}",
            payload_kind="equity_daily",
            source_id=EOD_SOURCE_ID,
            license_id="yahoo-public-reference",
            source_as_of=item.source_as_of,
            received_at=item.received_at,
            payload_sha256=item.artifact_sha256,
            synthetic=False,
            redistribution_allowed=False,
        )
        for item in ordered
    }
    return {
        "schema_version": EOD_INGEST_VERSION,
        "mode": "REAL_EOD_BATCH",
        "decision_cutoff": decision_cutoff.isoformat(),
        "batch_manifest_sha256": manifest.manifest_sha256,
        "batch_status": manifest.status.value,
        "manifest_reason_codes": list(manifest.reason_codes),
        "source_results": [
            {
                "symbol": item.symbol,
                "status": item.status.value,
                "reason_codes": list(item.reason_codes),
                "artifact_sha256": item.artifact_sha256,
                "days_count": len(item.days),
                "last_day_close": item.days[-1].close if item.days else None,
                "last_day": item.days[-1].date if item.days else None,
                "days": [
                    {
                        "date": d.date, "close": d.close, "open": d.open,
                        "high": d.high, "low": d.low, "volume": d.volume,
                    }
                    for d in item.days
                ],
            }
            for item in ordered
        ],
        "artifacts": {
            symbol: {
                "artifact_id": artifact.artifact_id,
                "payload_kind": artifact.payload_kind,
                "source_id": artifact.source_id,
                "license_id": artifact.license_id,
                "synthetic": artifact.synthetic,
                "redistribution_allowed": artifact.redistribution_allowed,
                "payload_sha256": artifact.payload_sha256,
            }
            for symbol, artifact in artifacts.items()
        },
        "in_epoch": int(in_epoch.timestamp()),
    }


__all__ = [
    "EOD_INGEST_VERSION",
    "EOD_SOURCE_ID",
    "EodDay",
    "EodSymbolResult",
    "ingest_eod",
]