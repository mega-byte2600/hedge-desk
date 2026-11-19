"""Desk call: the three-line decision header for the morning output.

Reviewers found that the AM report never states the decision. This module
derives one, deterministically, from fields the nightly report already
carries. It adds no model and changes no gate:

* ACTION is NO_TRADE unless data is current AND a structure's risk-gate
  decision is APPROVED. The gate is consumed, never re-evaluated (AGENTS.md:
  agents may not substitute or weaken the Risk-of-Ruin gate).
* SHORTLIST is at most three structures, ranked by risk-neutral EV and then
  probability of profit when the nightly carries them (cboe_chain), else by
  return on risk with an explicit flag.
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
    ev = _dec(s.get("risk_neutral_ev"))
    pop = _dec(s.get("probability_of_profit")) or Decimal("0")
    ror = _dec(s.get("return_on_risk")) or Decimal("0")
    if ev is not None:
        return (0, -ev, -pop, s.get("contract_id", ""))
    return (1, -ror, Decimal("0"), s.get("contract_id", ""))


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
    for s in sorted(pool, key=_rank_key)[:SHORTLIST_SIZE]:
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
            "gate_decision": s.get("gate_decision", "NOT_EVALUATED"),
        })
    action = "PAPER_CANDIDATE" if approved and not reasons else "NO_TRADE"
    vix = report.get("vix_regime") or {}
    vix_close = _dec(vix.get("last_close"))
    ranked_by = ("risk-neutral EV, then probability of profit"
                 if shortlist and shortlist[0]["risk_neutral_ev"] is not None
                 else "return on risk (EV fields absent in this nightly; next run adds them)")
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
