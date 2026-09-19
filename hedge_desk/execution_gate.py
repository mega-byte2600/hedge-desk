"""Risk-gated auto-execution decision harness for real premium structures.

Increment 12 of the true-MVP re-scope: the GP's chosen mode is "risk-gated auto"
— the engine MAY place an order automatically, but only behind the deterministic
risk gate plus a kill switch, with the existing paper-to-live release gate on top.
This module plugs a REAL premium structure (from the Cboe chain path) into that
decision WITHOUT placing an order.

Honesty and safety:
- It NEVER sends an order. It returns a DECISION (ALLOW_PAPER / BLOCKED) that the
  released adapter would act on only after the live release gate is satisfied.
- RoR is CONSUMED from a caller-supplied validated value, never calculated here
  (the desk rule: agents never calculate authoritative RoR).
- A kill switch is required ON for any ALLOW. Default OFF -> BLOCKED.
- trade_authorized is only ever set inside the same harness that also checks the
  kill switch and release readiness; nothing here fabricates release evidence.

This is the "set up the infra and validate it works" step. Wiring the actual
Schwab HTTP order call is a separate, explicitly-gated slice requiring the GP's
credentials and a real-money review — NOT fabricated here.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from typing import Dict, Optional, Tuple

from hedge_desk.domain import Account, AccountType, TradeCandidate, ProductType
from hedge_desk.risk.ruin import RiskPolicy, risk_gate
from hedge_desk.release import (
    REQUIRED_RELEASE_EVIDENCE,
    ReleaseEvidence,
    evaluate_live_release_readiness,
)

EXEC_GATE_VERSION = "hedge-desk-execution-gate-1.0.0"


@dataclass(frozen=True)
class KillSwitch:
    armed: bool
    source: str = "manual"


@dataclass(frozen=True)
class ExecutionDecision:
    decision: str  # "BLOCKED" | "ALLOW_PAPER"
    reason_codes: Tuple[str, ...]
    risk_gate_reasons: Tuple[str, ...]
    kill_switch_armed: bool
    release_ready: bool
    trade_authorized: bool
    decision_sha256: str
    evaluated_at: datetime


def _hash_of(payload: str) -> str:
    import hashlib

    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def evaluate_execution(
    *,
    candidate: TradeCandidate,
    account: Account,
    evaluated_at: datetime,
    validated_risk_of_ruin_after: Optional[Decimal] = None,
    risk_policy: RiskPolicy = RiskPolicy(),
    kill_switch: KillSwitch = KillSwitch(armed=False),
    release_evidence: Optional[Tuple[ReleaseEvidence, ...]] = None,
) -> ExecutionDecision:
    """Run the full pre-order decision without placing any order.

    Honesty requirement (desk rule, AGENTS.md): agents must never substitute an
    authoritative Risk-of-Ruin value. Therefore ``validated_risk_of_ruin_after``
    must be the immutable result of a separately versioned deterministic validator.
    If it is NOT supplied, the decision is BLOCKED with ``RISK_INPUT_ABSENT`` and
    the risk gate is never evaluated against a fabricated number. The caller is
    a validated-input boundary, not a free-form injector.
    """
    if evaluated_at.tzinfo is None:
        raise ValueError("execution evaluated_at must be timezone-aware")

    reasons: list[str] = []

    # 1. Kill switch: must be armed for ANY allow.
    if not kill_switch.armed:
        reasons.append("KILL_SWITCH_OFF")

    # 2. Deterministic risk gate — ONLY if a validated RoR artifact is supplied.
    #    Absent a validated input, we fail closed with a reason code rather than
    #    inject a placeholder (no fabricated risk numbers).
    risk_reasons: tuple = ()
    if validated_risk_of_ruin_after is None:
        reasons.append("RISK_INPUT_ABSENT")
    else:
        risk_reasons = tuple(
            risk_gate(account, candidate, evaluated_at, risk_policy, validated_risk_of_ruin_after)
        )
        if risk_reasons:
            reasons.append("RISK_GATE_BLOCKED")

    # 3. Paper-to-live release readiness. If no evidence supplied, use the
    #    reference (all-false) gate -> BLOCKED. This never fabricates evidence.
    evidence = release_evidence or tuple(
        ReleaseEvidence(r, False, "0" * 64) for r in REQUIRED_RELEASE_EVIDENCE
    )
    release = evaluate_live_release_readiness(evidence)
    release_ready = release.status.value == "READY_FOR_SEPARATE_LIVE_AUTHORIZATION"
    if not release_ready:
        reasons.append("LIVE_RELEASE_NOT_READY")

    decision = "BLOCKED"
    trade_authorized = False
    if not reasons:
        decision = "ALLOW_PAPER"
        # Even on allow, this is a PAPER order decision; the release gate for live
        # is separately enforced and the harness never sends an order.
        trade_authorized = False

    reason_codes = tuple(sorted(set(reasons)))
    payload = {
        "decision": decision,
        "candidate_id": candidate.candidate_id,
        "symbol": candidate.symbol,
        "max_loss": str(candidate.max_loss),
        "risk_gate_reasons": list(risk_reasons),
        "release_reason_codes": list(release.reason_codes),
        "kill_switch_armed": kill_switch.armed,
    }
    decision_hash = _hash_of(
        str(sorted(payload.items()))
        + "|" + decision + "|" + str(trade_authorized)
    )
    return ExecutionDecision(
        decision,
        reason_codes,
        risk_reasons,
        kill_switch.armed,
        release_ready,
        trade_authorized,
        decision_hash,
        evaluated_at,
    )


def build_candidate_from_structure(
    structure: Dict[str, object],
    quantity: int = 1,
    quote_timestamp: Optional[datetime] = None,
    average_daily_dollar_volume: Optional[Decimal] = None,
) -> TradeCandidate:
    """Map one real premium structure into the domain TradeCandidate the risk
    gate reads. The structure carries net_credit and maximum_loss as strings.

    ``average_daily_dollar_volume`` must be a REAL market/liquidity figure supplied
    by the caller. It is intentionally NOT defaulted to a synthetic value: a desk
    that hardcodes liquidity passes every liquidity gate and cannot be trusted.
    Raising here forces the caller to admit it lacks a real ADV rather than
    silently swallowing a made-up number.
    """
    uri = str(structure.get("contract_id", "unknown"))
    symbol = str(structure.get("underlying", uri.split("--")[0][:6]))
    adv = average_daily_dollar_volume
    if adv is None:
        raise ValueError(
            "average_daily_dollar_volume is required (real liquidity); refusing to "
            "invent an ADV for risk evaluation"
        )
    if not isinstance(adv, Decimal) or not adv.is_finite() or adv <= 0:
        raise ValueError("average_daily_dollar_volume must be a positive finite Decimal")
    qtime = quote_timestamp or datetime.now(timezone.utc)
    return TradeCandidate(
        candidate_id=uri,
        symbol=symbol,
        product_type=ProductType.DEFINED_RISK_OPTION,
        quantity=quantity,
        entry_price=Decimal(str(structure.get("net_credit_per_share", "0"))),
        max_loss=Decimal(str(structure.get("maximum_loss", "0"))),
        expected_win=Decimal(str(structure.get("net_credit", "0"))),
        win_probability=Decimal("0"),  # not estimated by this harness
        quote_timestamp=qtime,
        average_daily_dollar_volume=adv,
        thesis="Real defined-risk premium structure from Cboe chain intake.",
        invalidation="Reject if risk or release gate blocks, or kill switch is off.",
    )


__all__ = [
    "EXEC_GATE_VERSION",
    "KillSwitch",
    "ExecutionDecision",
    "evaluate_execution",
    "build_candidate_from_structure",
]