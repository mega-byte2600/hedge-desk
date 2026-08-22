"""Fail-closed human authorization and paper-only lifecycle."""

from dataclasses import dataclass, replace
from datetime import datetime
from decimal import Decimal
from enum import Enum
from hashlib import sha256
from typing import Optional, Tuple

from hedge_desk.domain import Decision, DecisionStatus
from hedge_desk.options import VerticalSpreadCalculation


class MachineRiskStatus(str, Enum):
    PASS = "pass"
    REJECT = "reject"


class HumanAuthorizationStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass(frozen=True)
class HumanAuthorization:
    status: HumanAuthorizationStatus
    human_id: Optional[str] = None
    decided_at: Optional[datetime] = None
    plan_hash: Optional[str] = None


@dataclass(frozen=True)
class PaperTradePlan:
    plan_id: str
    spread: VerticalSpreadCalculation
    risk_decision: Decision
    machine_risk_status: MachineRiskStatus
    reason_codes: Tuple[str, ...]
    authorization: HumanAuthorization
    created_at: datetime
    approval_expires_at: datetime
    execution_quote_max_age_seconds: int
    plan_hash: str


@dataclass(frozen=True)
class PaperOpen:
    plan_id: str
    plan_hash: str
    opened_at: datetime
    entry_credit: Decimal
    quantity: int
    environment: str = "paper"


@dataclass(frozen=True)
class PaperClose:
    plan_id: str
    plan_hash: str
    closed_at: datetime
    exit_debit: Decimal
    exit_commission: Decimal
    realized_pnl: Decimal
    environment: str = "paper"


def _calculate_plan_hash(
    plan_id: str,
    spread: VerticalSpreadCalculation,
    risk_decision: Decision,
    created_at: datetime,
    approval_expires_at: datetime,
    execution_quote_max_age_seconds: int,
) -> str:
    payload = "|".join(
        (
            plan_id,
            spread.spread_id,
            spread.model_id,
            spread.model_version,
            spread.calculated_at.isoformat(),
            ",".join(spread.input_contract_ids),
            ",".join(timestamp.isoformat() for timestamp in spread.quote_timestamps),
            str(spread.quantity),
            str(spread.contract_multiplier),
            str(spread.width_per_share),
            str(spread.short_sale_price_per_share),
            str(spread.long_purchase_price_per_share),
            str(spread.gross_credit),
            str(spread.total_commission),
            str(spread.net_credit),
            str(spread.maximum_loss),
            str(spread.break_even),
            str(spread.return_on_risk),
            risk_decision.candidate_id,
            risk_decision.account_id,
            risk_decision.status.value,
            ",".join(risk_decision.reason_codes),
            str(risk_decision.risk_of_ruin_before),
            str(risk_decision.risk_of_ruin_after),
            risk_decision.evaluated_at.isoformat(),
            created_at.isoformat(),
            approval_expires_at.isoformat(),
            str(execution_quote_max_age_seconds),
        )
    )
    return sha256(payload.encode("utf-8")).hexdigest()


def _assert_plan_integrity(plan: PaperTradePlan) -> None:
    expected = _calculate_plan_hash(
        plan.plan_id,
        plan.spread,
        plan.risk_decision,
        plan.created_at,
        plan.approval_expires_at,
        plan.execution_quote_max_age_seconds,
    )
    if expected != plan.plan_hash:
        raise PermissionError("paper-trade plan integrity check failed")


def create_paper_trade_plan(
    plan_id: str,
    spread: VerticalSpreadCalculation,
    risk_decision: Decision,
    created_at: datetime,
    approval_expires_at: datetime,
    execution_quote_max_age_seconds: int = 120,
) -> PaperTradePlan:
    if not plan_id:
        raise ValueError("plan identity is required")
    if created_at.tzinfo is None or approval_expires_at.tzinfo is None:
        raise ValueError("plan timestamps must be timezone-aware")
    if approval_expires_at <= created_at:
        raise ValueError("approval expiry must follow plan creation")
    if execution_quote_max_age_seconds <= 0:
        raise ValueError("execution quote age limit must be positive")

    machine_status = (
        MachineRiskStatus.PASS
        if risk_decision.status is DecisionStatus.APPROVED_FOR_PAPER
        else MachineRiskStatus.REJECT
    )
    plan_hash = _calculate_plan_hash(
        plan_id,
        spread,
        risk_decision,
        created_at,
        approval_expires_at,
        execution_quote_max_age_seconds,
    )
    return PaperTradePlan(
        plan_id=plan_id,
        spread=spread,
        risk_decision=risk_decision,
        machine_risk_status=machine_status,
        reason_codes=risk_decision.reason_codes,
        authorization=HumanAuthorization(HumanAuthorizationStatus.PENDING),
        created_at=created_at,
        approval_expires_at=approval_expires_at,
        execution_quote_max_age_seconds=execution_quote_max_age_seconds,
        plan_hash=plan_hash,
    )


def approve_paper_trade(
    plan: PaperTradePlan,
    human_id: str,
    decided_at: datetime,
) -> PaperTradePlan:
    _assert_plan_integrity(plan)
    if not human_id.strip():
        raise ValueError("human identity is required")
    if decided_at.tzinfo is None:
        raise ValueError("authorization timestamp must be timezone-aware")
    if plan.machine_risk_status is not MachineRiskStatus.PASS:
        raise PermissionError("human cannot override a machine risk rejection")
    if decided_at > plan.approval_expires_at:
        raise PermissionError("paper-trade approval window has expired")
    if plan.authorization.status is not HumanAuthorizationStatus.PENDING:
        raise PermissionError("plan has already received a human decision")

    return replace(
        plan,
        authorization=HumanAuthorization(
            status=HumanAuthorizationStatus.APPROVED,
            human_id=human_id,
            decided_at=decided_at,
            plan_hash=plan.plan_hash,
        ),
    )


def execute_paper_open(plan: PaperTradePlan, opened_at: datetime) -> PaperOpen:
    _assert_plan_integrity(plan)
    if opened_at.tzinfo is None:
        raise ValueError("paper-open timestamp must be timezone-aware")
    if plan.authorization.status is not HumanAuthorizationStatus.APPROVED:
        raise PermissionError("paper execution requires human authorization")
    if plan.authorization.plan_hash != plan.plan_hash:
        raise PermissionError("authorization is not bound to this plan")
    if opened_at > plan.approval_expires_at:
        raise PermissionError("paper execution approval has expired")
    quote_age = (opened_at - max(plan.spread.quote_timestamps)).total_seconds()
    if quote_age < 0:
        raise PermissionError("paper execution cannot precede its quotes")
    if quote_age > plan.execution_quote_max_age_seconds:
        raise PermissionError("paper execution quotes are stale")
    return PaperOpen(
        plan_id=plan.plan_id,
        plan_hash=plan.plan_hash,
        opened_at=opened_at,
        entry_credit=plan.spread.net_credit,
        quantity=plan.spread.quantity,
    )


def close_paper_trade(
    opened: PaperOpen,
    exit_debit_per_share: Decimal,
    exit_commission_per_contract: Decimal,
    closed_at: datetime,
) -> PaperClose:
    if closed_at.tzinfo is None:
        raise ValueError("paper-close timestamp must be timezone-aware")
    if closed_at <= opened.opened_at:
        raise ValueError("paper close must follow paper open")
    if exit_debit_per_share < 0 or exit_commission_per_contract < 0:
        raise ValueError("exit debit and commission cannot be negative")

    quantity = Decimal(opened.quantity)
    exit_debit = exit_debit_per_share * Decimal(100) * quantity
    exit_commission = exit_commission_per_contract * Decimal(2) * quantity
    return PaperClose(
        plan_id=opened.plan_id,
        plan_hash=opened.plan_hash,
        closed_at=closed_at,
        exit_debit=exit_debit,
        exit_commission=exit_commission,
        realized_pnl=opened.entry_credit - exit_debit - exit_commission,
    )
