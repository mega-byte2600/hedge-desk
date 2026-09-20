"""Cash-secured-put scanner for the GP's premium wheel (roadmap Tier 2).

The GP's actual product (standing): sell cash-secured puts ~10% OTM, 30-45 DTE,
capital required under ~$5k, return on capital deployed ~1-2% per trade. This
module scans a REAL Cboe chain and reports which puts fit that wheel.

It uses real bid/ask, real strikes, real expirations. Collateral = short-strike
(a cash-secured put holds the strike); return_on_capital = net_credit /
collateral; the GP rules are applied from evaluate_premium. Survivability is
INDETERMINATE until a real account balance is wired — never fabricated. No order,
no probability, trade_authorized stays False.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Callable, Dict, Sequence, Tuple

from hedge_desk.cboe_chain import (
    build_snapshot_from_cboe,
    _default_transport,
    CBOE_URL,
)
from hedge_desk.position_sizing import evaluate_premium
from hedge_desk.options import OptionType
from hedge_desk.options.requirements import cash_secured_put_collateral

CSP_VERSION = "hedge-desk-cash-secured-put-1.0.0"

# ~10% OTM put target (the GP's wheel), tight band for "options basics".
OTM_DELTA_FRACTION = Decimal("0.10")


def _put_10pct_otm(symbol: str, raw: bytes, now) -> Dict[str, object]:
    """Find the ~10% OTM cash-secured put on the 30-45 DTE cycle.

    Returns one candidate (best-fit strike) or an empty dict if none fits.
    """
    snap = build_snapshot_from_cboe(raw, symbol, now)
    mid = (snap.underlying_quote.bid + snap.underlying_quote.ask) / 2
    today = now.date()
    # 30-45 DTE window (matching the wheel), pick closest to target.
    puts = [
        q for q in snap.option_quotes
        if q.option_type is OptionType.PUT
        and (q.expiration - today).days >= 30
        and (q.expiration - today).days <= 45
    ]
    if not puts:
        return {"found": False, "reason": "no_put_in_30_45_dte"}
    # candidate: ~10% OTM put (strike ~ 0.90 * mid), with real executable bid/ask.
    target_strike = mid * (Decimal("1") - OTM_DELTA_FRACTION)
    best = min(puts, key=lambda q: abs(q.strike - target_strike))
    credit = best.ask  # we SELL -> collect the bid-side? We sell at the bid.
    # Selling a put: we receive the BID. But executable realism = use bid.
    net_credit = best.bid
    collateral = cash_secured_put_collateral(best.strike, net_credit, 1).requirement
    return {
        "found": True,
        "contract_id": best.contract_id,
        "strike": str(best.strike),
        "expiration": best.expiration.isoformat(),
        "dte": (best.expiration - today).days,
        "underlying_mid": str(mid),
        "net_credit_per_share": str(net_credit),
        # QUANT finding: use the same credit-offset collateral as evaluate_premium
        # (strike - credit)*100, so both paths report the same return-on-capital for
        # the same put (was gross strike*100 in the scan, ~1.3bps off, could flip a
        # near-boundary candidate).
        "collateral_required": str(collateral.quantize(Decimal("0.01"))),
        # Return on capital deployed = credit_per_contract / collateral_in_dollars
        # (net_credit*100 / (strike-credit)*100 = net_credit/(strike-credit)).
        "return_on_capital": str(
            (net_credit * Decimal("100") / collateral).quantize(Decimal("0.0001"))
        ),
        "max_loss": str(collateral.quantize(Decimal("0.01"))),
    }


def scan_cash_secured_put(
    symbol: str,
    now,
    transport: Callable = _default_transport,
    account_equity: str | None = None,
) -> Dict[str, object]:
    """Scan one symbol's real chain for the GP-fit cash-secured put."""
    if not symbol or not str(symbol).strip():
        raise ValueError("symbol required")
    status, raw = transport(CBOE_URL.format(symbol=str(symbol).upper().strip()))
    if status != 200 or not raw:
        return {"mode": "BLOCKED", "symbol": symbol, "reason": f"cboe_fetch_{status}"}
    try:
        cand = _put_10pct_otm(symbol, raw, now)
    except ValueError as exc:
        return {"mode": "NO_CANDIDATE", "symbol": symbol, "reason": str(exc)}
    if not cand.get("found"):
        return {"mode": "NO_CANDIDATE", "symbol": symbol, "reason": cand.get("reason")}
    out = {"mode": "CASH_SECURED_PUT", "symbol": symbol, "candidate": cand,
           "data_source": "cboe-delayed-public-http-200", "trade_authorized": False}
    # Equity-free rule checks (never raise on missing equity): capital < $5k,
    # DTE in 30-45, return-on-capital in the 0.5%-2% band. Survivability needs a
    # real account balance -> INDETERMINATE until one is wired.
    from decimal import Decimal as _D
    reasons = []
    cap = _D(cand["collateral_required"])
    roc = _D(cand["return_on_capital"])
    if cap > _D("5000"):
        reasons.append("CAPITAL_OVER_5K")
    if not _D("30") <= cand["dte"] <= _D("45"):
        reasons.append("DTE_OUTSIDE_30_45")
    if not _D("0.005") <= roc <= _D("0.02"):
        reasons.append("RETURN_NOT_IN_GP_BAND")
    if account_equity:
        try:
            v = evaluate_premium(
                str(cand["net_credit_per_share"]), str(cand["max_loss"]),
                str(cand["strike"]), account_equity, int(cand["dte"]),
            )
            reasons = v["reasons"]
        except ValueError as exc:
            reasons = [str(exc)]
        out["survivability"] = "PASS" if not reasons else "FAIL"
    else:
        out["survivability"] = "INDETERMINATE"
    out["fits_gp_rules"] = not reasons
    out["eval_reasons"] = reasons
    return out


__all__ = ["CSP_VERSION", "scan_cash_secured_put"]