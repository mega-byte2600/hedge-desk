"""Desk call: the three-line decision header for the morning output.

Reviewers found that the AM report never states the decision. This module
derives one, deterministically, from fields the nightly report already
carries. It adds no model and changes no gate:

* ACTION is NO_TRADE unless data is current AND a structure's risk-gate
  decision is APPROVED. The gate is consumed, never re-evaluated (AGENTS.md:
  agents may not substitute or weaken the Risk-of-Ruin gate).
* SHORTLIST is at most three structures ranked by the premium-selling score
  (hedge_desk.premium_score) when present, else by return on risk.
* INVALIDATION is the structure's break-even; EXITS are the released
  PremiumExitPolicy defaults (50% profit capture, 50%-of-max-loss stop).
* RISK is max loss as a share of the DEMO equity the gate already uses; it is
  descriptive, not a sizing instruction.
"""
from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Any, Dict, List, Optional

from hedge_desk.options.exit_policy import PremiumExitPolicy

SCHEMA_VERSION = "hedge-desk-desk-call-1.0.0"
SHORTLIST_SIZE = 3


def _dec(value: Any) -> Optional[Decimal]:
    try:
        d = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        return None
    return d if d.is_finite() else None


def _rank_key(s: Dict[str, Any]):
    """Premium score (hedge_desk.premium_score, GP brief 2026-11-19) when the
    nightly carries it; otherwise the scanner's return-on-risk order."""
    p = s.get("premium") or {}
    prem = p.get("premium_score")
    ror = _dec(s.get("return_on_risk")) or Decimal("0")
    if prem is not None:
        # Eligible (inside the GP's delta/DTE bands with a positive vol edge)
        # always outrank ineligible structures.
        return (0, not p.get("eligible", True), -Decimal(str(prem)), -ror, s.get("contract_id", ""))
    return (1, True, Decimal("0"), -ror, s.get("contract_id", ""))


def build_desk_call(report: Dict[str, Any], symbol: str = "SPY") -> Dict[str, Any]:
    reasons: List[str] = []
    fresh = report.get("data_freshness") or {}
    if not fresh.get("is_current"):
        reasons.append("DATA_NOT_CURRENT")
    if report.get("eod_batch_status") != "READY_FOR_RESEARCH":
        reasons.append("EOD_BATCH_NOT_READY")
    chain = (report.get("chain_income") or {}).get(symbol) or {}
    structures = chain.get("gated_income_structures") or chain.get("income_structures") or []
    equity = _dec(chain.get("gate_demo_account_equity"))
    approved = [s for s in structures if s.get("gate_decision") == "APPROVED"]
    if not structures:
        reasons.append("NO_ADMISSIBLE_STRUCTURES")
    elif not approved:
        gate_reasons = sorted({r for s in structures for r in s.get("gate_reasons", [])})
        reasons.append("RISK_GATE_NOT_APPROVED:" + ",".join(gate_reasons or ["UNSPECIFIED"]))
    pool = approved if approved else structures
    shortlist = []
    policy = PremiumExitPolicy()
    from hedge_desk.premium_score import unique_by_short_leg
    for s in unique_by_short_leg(sorted(pool, key=_rank_key))[:SHORTLIST_SIZE]:
        credit = _dec(s.get("net_credit")) or Decimal("0")
        max_loss = _dec(s.get("maximum_loss")) or Decimal("0")
        shortlist.append({
            "contract_id": s.get("contract_id"),
            "expiration": s.get("expiration"),
            "days_to_expiration": s.get("days_to_expiration"),
            "net_credit": str(credit),
            "maximum_loss": str(max_loss),
            "probability_of_profit": s.get("probability_of_profit"),
            "risk_neutral_ev": s.get("risk_neutral_ev"),
            "invalidation_underlying_through": s.get("break_even"),
            "take_profit_at_credit_captured": str(
                (credit * policy.profit_capture_fraction).quantize(Decimal("0.01"))),
            "stop_at_loss": str((max_loss * policy.maximum_loss_fraction).quantize(Decimal("0.01"))),
            "max_loss_pct_demo_equity": (
                str((max_loss / equity * 100).quantize(Decimal("0.01"))) if equity else None),
            # SOUL rule 7 (2%-of-equity max loss) applied to the DEMO equity the
            # gate already uses: an example, never an order or the GP's balance.
            "collateral_per_contract": str((credit + max_loss).quantize(Decimal("0.01"))),
            "example_max_contracts_2pct_demo_equity": (
                int((equity * Decimal("0.02")) // max_loss) if equity and max_loss > 0 else None),
            "eligible": (s.get("premium") or {}).get("eligible"),
            "eligibility_reasons": (s.get("premium") or {}).get("eligibility_reasons") or [],
            "gate_decision": s.get("gate_decision", "NOT_EVALUATED"),
            "premium_score": (s.get("premium") or {}).get("premium_score"),
            "premium_components": (s.get("premium") or {}).get("components"),
            "time_exit_dte": ((s.get("premium") or {}).get("management") or {}).get("time_exit_dte"),
        })
    action = "PAPER_CANDIDATE" if approved and not reasons else "NO_TRADE"
    vix = report.get("vix_regime") or {}
    vix_close = _dec(vix.get("last_close"))
    ranked_by = ("eligible first (16-30 delta, 21-60 DTE, positive vol edge), then premium score: "
                 "vol edge 30%, return on collateral 25%, 30-45 DTE window 25%, 16-30 delta 20%"
                 if shortlist and shortlist[0].get("premium_score") is not None
                 else "return on risk (premium score absent in this nightly; next run adds it)")
    if action == "NO_TRADE":
        headline = ("No trade today. " + ("Risk gate has not approved any structure; "
                    "the shortlist is research only." if structures else "Nothing admissible."))
    else:
        headline = f"Paper candidate: {shortlist[0]['contract_id']} (human approval required)."
    return {
        "schema_version": SCHEMA_VERSION,
        "as_of": fresh.get("as_of"),
        "action": action,
        "headline": headline,
        "reason_codes": reasons,
        "context": {
            "vix_regime": vix.get("regime"),
            "vix_close": str(vix_close.quantize(Decimal("0.01"))) if vix_close is not None else None,
            "data_current": bool(fresh.get("is_current")),
        },
        "ranked_by": ranked_by,
        "shortlist": shortlist,
        "exit_policy_version": "premium-exit-monitor-1.0.0",
        "trade_authorized": False,
    }


__all__ = ["build_desk_call", "SCHEMA_VERSION"]
