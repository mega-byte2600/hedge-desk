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

from datetime import datetime, timezone
from typing import Callable, Dict

from hedge_desk.data.eod_ingest import ingest_eod

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


def vix_regime(
    now: datetime | None = None,
    transport: Callable | None = None,
) -> Dict[str, object]:
    """Read the real ^VIX close and label the regime.

    Reuses the validated EOD chart parser (ingest_eod) so the transport, point-in-time
    and parse gates are the same ones the daily batch trusts. ``transport`` is
    injectable for deterministic offline tests.
    """
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ValueError("vix cutoff must be timezone-aware")
    try:
        if transport is not None:
            batch = ingest_eod((VIX_SYMBOL,), now, transport=transport, range_param="5d")
        else:
            batch = ingest_eod((VIX_SYMBOL,), now, range_param="5d")
    except ValueError as exc:
        return {"mode": "BLOCKED", "reason": str(exc)}
    row = batch["source_results"][0]
    if row["status"] != "PASS" or row.get("last_day_close") is None:
        return {
            "mode": "BLOCKED",
            "reason": ",".join(row.get("reason_codes", [])) or row["status"],
        }
    try:
        close = float(row["last_day_close"])
    except (TypeError, ValueError):
        return {"mode": "BLOCKED", "reason": "NON_NUMERIC_VIX"}
    return {
        "schema_version": VIX_VERSION,
        "mode": "REAL_VIX",
        "symbol": VIX_SYMBOL,
        "last_close": str(close),
        "last_day": row.get("last_day"),
        "regime": _regime(close),
        "data_source": "yahoo-public-chart-http-200",
        "note": (
            "Real delayed VIX close. Regime is a descriptive band (LOW/NORMAL/"
            "ELEVATED/HIGH), context for when to sell premium, not a signal and "
            "not advice. No order placed."
        ),
    }


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