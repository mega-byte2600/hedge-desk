"""Real VIX regime reading for the premium desk (data is king).

The cash-secured-put wheel's timing input: how expensive is premium right now?
VIX is the market's implied-volatility gauge. We read the REAL ^VIX close from the
same public Yahoo chart endpoint the EOD batch uses (verified reachable, HTTP 200)
and label a regime from conventional bands. It is context for when to sell premium,
never a directional call and never a forecast.

Honesty and safety:
- Real delayed close only; a transport/parse failure returns mode BLOCKED, never a
  fabricated VIX.
- The regime label is a descriptive band, not a signal and not advice.
- No order, no probability, no Risk of Ruin.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Callable, Dict, List, Tuple

from hedge_desk.data.eod_ingest import YAHOO_CHART_URL, _default_transport

VIX_VERSION = "hedge-desk-vix-regime-1.0.0"
VIX_SYMBOL = "^VIX"

# Conventional VIX bands (descriptive, not a signal).
def _regime(close: float) -> str:
    if close < 15:
        return "LOW"          # complacent; premium is cheap
    if close < 20:
        return "NORMAL"
    if close < 30:
        return "ELEVATED"     # richer premiums, more risk
    return "HIGH"             # fear; premium expensive but risky


def _parse_vix_chart(raw: bytes) -> Tuple[List[Tuple[str, Decimal]], int]:
    """Parse a Yahoo chart payload into (date, close) points.

    Days with null/non-numeric/non-positive closes are DROPPED and counted,
    not fatal: a single bad print (e.g. a holiday-shortened session months
    ago) must not block today's regime read. A malformed payload or zero
    valid closes raises ValueError (fail closed).
    """
    try:
        payload = json.loads(raw.decode("utf-8"))
        result = payload["chart"]["result"][0]
        timestamps = result["timestamp"]
        closes = (result["indicators"]["quote"][0].get("close") or [])
    except (KeyError, IndexError, TypeError, ValueError, UnicodeDecodeError) as exc:
        raise ValueError(f"vix chart payload malformed: {exc}")
    try:
        n_ts, n_cl = len(timestamps), len(closes)
    except TypeError as exc:
        raise ValueError(f"vix chart series not sequences: {exc}")
    if n_ts != n_cl:
        raise ValueError(
            f"vix chart series length mismatch: {n_ts} timestamps vs {n_cl} closes"
        )
    points: List[Tuple[str, Decimal]] = []
    dropped = 0
    for ts, close in zip(timestamps, closes):
        try:
            dec = Decimal(str(close))
        except (InvalidOperation, ValueError, TypeError):
            dropped += 1
            continue
        if not dec.is_finite() or dec <= 0:
            dropped += 1
            continue
        try:
            day = datetime.fromtimestamp(int(ts), tz=timezone.utc).date().isoformat()
        except (OverflowError, OSError, ValueError, TypeError):
            raise ValueError(f"vix chart has corrupt timestamp: {ts!r}")
        points.append((day, dec))
    if not points:
        raise ValueError("vix chart has no valid closes")
    return points, dropped


def vix_regime(
    now: datetime | None = None,
    transport: Callable | None = None,
) -> Dict[str, object]:
    """Read the real ^VIX close and label the regime.

    Fetches the 3mo Yahoo chart directly and parses it null-tolerantly (see
    _parse_vix_chart): the EOD batch's strict parser would reject the whole
    series over one stale null print. ``transport`` is injectable for
    deterministic offline tests.
    """
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ValueError("vix cutoff must be timezone-aware")
    t = transport or _default_transport
    try:
        status, raw = t(YAHOO_CHART_URL.format(symbol=VIX_SYMBOL, range_param="3mo"))
    except Exception as exc:
        return {"mode": "BLOCKED", "reason": f"vix transport failed: {exc}"}
    if status != 200 or not raw:
        return {"mode": "BLOCKED", "reason": f"yahoo vix fetch failed (status {status})"}
    try:
        points, dropped = _parse_vix_chart(raw)
    except ValueError as exc:
        return {"mode": "BLOCKED", "reason": str(exc)}
    last_day, close = points[-1]
    if last_day > now.date().isoformat():
        return {"mode": "BLOCKED", "reason": f"vix chart last day {last_day} is in the future"}
    out: Dict[str, object] = {
        "schema_version": VIX_VERSION,
        "mode": "REAL_VIX",
        "symbol": VIX_SYMBOL,
        # Full 3mo close history for the dashboard's trend chart (small).
        "history": [[d, str(c)] for d, c in points],
        "last_close": str(close),
        "last_day": last_day,
        "regime": _regime(float(close)),
        "data_source": "yahoo-public-chart-http-200",
        "note": (
            "Real delayed VIX close. Regime is a descriptive band (LOW/NORMAL/"
            "ELEVATED/HIGH), context for when to sell premium, not a signal and "
            "not advice. No order placed."
        ),
    }
    if dropped:
        out["dropped_null_days"] = dropped
    return out


def apply_vix_regime_filter(vix: Dict[str, object], csp_results: Dict[str, object]) -> Dict[str, object]:
    """Apply the VIX regime as a risk filter on the cash-secured-put candidates.

    RISK peer-review finding: the regime was context only, so a HIGH-VIX (fear)
    environment still recommended selling puts with no vol-regime flag. Now a HIGH
    regime adds VIX_HIGH_REGIME to each candidate's eval_reasons and forces
    fits_gp_rules=False (fail-closed on the risk filter); ELEVATED adds a warning
    but keeps the candidate. LOW/NORMAL and BLOCKED (no regime) leave candidates
    unchanged. Returns a new dict; never mutates the input.
    """
    regime = vix.get("regime") if vix.get("mode") == "REAL_VIX" else None
    if regime not in ("HIGH", "ELEVATED"):
        return dict(csp_results)
    out = {}
    for sym, r in csp_results.items():
        r = dict(r)
        if r.get("mode") == "CASH_SECURED_PUT":
            reasons = list(r.get("eval_reasons", []))
            if regime == "HIGH":
                if "VIX_HIGH_REGIME" not in reasons:
                    reasons.append("VIX_HIGH_REGIME")
                r["fits_gp_rules"] = False
            elif regime == "ELEVATED" and "VIX_ELEVATED_REGIME" not in reasons:
                reasons.append("VIX_ELEVATED_REGIME")
            r["eval_reasons"] = reasons
        out[sym] = r
    return out


__all__ = ["VIX_VERSION", "VIX_SYMBOL", "vix_regime", "apply_vix_regime_filter"]