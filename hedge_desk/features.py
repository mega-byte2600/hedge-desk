"""Deterministic feature plane over the real overnight batch (roadmap Tier 1).

Computes a small, spec'd, re-derivable feature set per symbol from the daily OHLCV
series so the overnight desk has numeric context without live data:

- return_1d / return_5d / return_21d: log returns over the window (Decimal).
- realized_vol_21d: std-dev of daily log returns over the trailing window, as a
  ratio (not a percentage, to avoid unit confusion), only when enough bars exist.
- range_position: where the latest close sits in its 21-day high/low range (0..1);
  None when the range is flat (open an explicit flag, never a fabricated value).
- candle_bias: sign of (close-open) on the latest bar (+1/-1/None if flat).

Honesty and determinism (matches AGENTS.md and the desk's discipline):
- Pure functions over the EodDay series; no network, no randomness, no market
  forecast, no probability, no RoR. A fixed input series yields a byte-identical
  feature bundle (content-addressed), so a later reader can reproduce it.
- Every feature is documented with its formula. Windows shorter than required
  return None + an explicit code, never a guessed number.
- No order, no trade_authorized, no probability.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from hashlib import sha256
import json
from math import sqrt
from typing import Dict, Sequence, Tuple

from hedge_desk.data.eod_ingest import EodDay

FEATURES_VERSION = "hedge-desk-features-1.0.0"


@dataclass(frozen=True)
class SymbolFeatures:
    symbol: str
    as_of: str
    return_1d: str | None
    return_5d: str | None
    return_21d: str | None
    realized_vol_21d: str | None
    range_position_21d: str | None
    candle_bias: int | None
    source_days: int
    reason_codes: Tuple[str, ...]
    feature_sha256: str


def _log_return(prev: Decimal, cur: Decimal) -> Decimal | None:
    if prev <= 0 or cur <= 0:
        return None
    from decimal import getcontext
    ctx = getcontext()
    p = ctx.prec
    ctx.prec = 20
    try:
        from math import log
        r = Decimal(log(float(cur) / float(prev)))
    finally:
        ctx.prec = p
    return r.quantize(Decimal("0.00000001"), rounding=ROUND_HALF_UP)


def _ret(closes: Sequence[Decimal], lag: int) -> Decimal | None:
    if len(closes) <= lag:
        return None
    return _log_return(closes[-1 - lag], closes[-1])


def _close_series(days: Sequence[EodDay]) -> Tuple[Decimal, ...]:
    return tuple(Decimal(d.close) for d in sorted(days, key=lambda x: x.date))


def build_symbol_features(symbol: str, days: Sequence[EodDay]) -> SymbolFeatures:
    """Compute the spec'd feature set for one symbol from its EOD day series."""
    ordered = tuple(sorted(days, key=lambda d: d.date))
    closes = _close_series(ordered)
    reasons: list[str] = []

    r1 = _ret(closes, 1)
    r5 = _ret(closes, 5)
    r21 = _ret(closes, 21)
    if r21 is None:
        reasons.append("NEED_22_BARS_FOR_21D")

    # Realized vol of daily log returns over trailing 21 days.
    rv = None
    if len(closes) >= 22:
        rets = [
            _log_return(closes[i], closes[i + 1])
            for i in range(len(closes) - 1)
            if i >= len(closes) - 21
        ]
        finite = [x for x in rets if x is not None]
        if len(finite) >= 20:
            mean = sum(finite, Decimal("0")) / len(finite)
            var = sum((x - mean) ** 2 for x in finite) / (len(finite) - 1)
            rv = Decimal(sqrt(float(max(var, Decimal("0"))))).quantize(
                Decimal("0.00000001"), rounding=ROUND_HALF_UP
            )
        else:
            reasons.append("INSUFFICIENT_RETURNS_FOR_REALIZED_VOL")

    # Range position: where the latest close sits in the trailing 21-bar
    # high/low range (0..1). Spec'd as a window of the last 21 bars.
    rp = None
    recent = ordered[-21:]
    if recent:
        highs = [Decimal(d.high) for d in recent]
        lows = [Decimal(d.low) for d in recent]
        hi, lo = max(highs), min(lows)
        if hi > lo:
            latest = Decimal(ordered[-1].close)
            rp = ((latest - lo) / (hi - lo)).quantize(
                Decimal("0.0001"), rounding=ROUND_HALF_UP
            )

    # Candle bias on latest bar.
    cb = None
    if ordered:
        last = ordered[-1]
        c, o = Decimal(last.close), Decimal(last.open)
        if c > o:
            cb = 1
        elif c < o:
            cb = -1

    feature_sha = sha256(
        json.dumps(
            {
                "symbol": symbol,
                "return_1d": str(r1),
                "return_5d": str(r5),
                "return_21d": str(r21),
                "realized_vol_21d": str(rv),
                "range_position_21d": str(rp),
                "candle_bias": cb,
                "source_days": len(ordered),
            },
            sort_keys=True, separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()

    return SymbolFeatures(
        symbol,
        ordered[-1].date if ordered else "",
        str(r1) if r1 is not None else None,
        str(r5) if r5 is not None else None,
        str(r21) if r21 is not None else None,
        str(rv) if rv is not None else None,
        str(rp) if rp is not None else None,
        cb,
        len(ordered),
        tuple(sorted(set(reasons))),
        feature_sha,
    )


def build_feature_bundle_from_days(
    days_by_symbol: Dict[str, Sequence[EodDay]],
) -> Dict[str, object]:
    """Compute the feature bundle for a {symbol: [EodDay,...]} map."""
    features = {}
    for symbol, days in sorted(days_by_symbol.items()):
        features[symbol] = build_symbol_features(symbol, days)
    return {
        "schema_version": FEATURES_VERSION,
        "mode": "DETERMINISTIC_FEATURES",
        "symbols": sorted(features),
        "features": {
            sym: {
                "as_of": f.as_of,
                "return_1d": f.return_1d,
                "return_5d": f.return_5d,
                "return_21d": f.return_21d,
                "realized_vol_21d": f.realized_vol_21d,
                "range_position_21d": f.range_position_21d,
                "candle_bias": f.candle_bias,
                "source_days": f.source_days,
                "reason_codes": list(f.reason_codes),
                "feature_sha256": f.feature_sha256,
            }
            for sym, f in features.items()
        },
        "note": (
            "Deterministic technical context from the real overnight batch. "
            "No probability, no RoR, no forecast, no order."
        ),
    }


__all__ = [
    "FEATURES_VERSION",
    "SymbolFeatures",
    "build_symbol_features",
    "build_feature_bundle_from_days",
]