"""Fail-closed human authorization and paper-only lifecycle."""

from dataclasses import dataclass, replace
from datetime import datetime
from decimal import Decimal
from enum import Enum
from hashlib import sha256
from typing import Optional, Tuple

from hedge_desk.backoffice import BackOfficeDecision, BackOfficeStatus
from hedge_desk.backoffice.compliance import APPROVED_BACK_OFFICE_POLICY_VERSIONS
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
    compliance_decision: BackOfficeDecision
    machine_risk_status: MachineRiskStatus
    reason_codes: Tuple[str, ...]
    authorization: HumanAuthorization
    created_at: datetime
    approval_expires_at: datetime
    execution_quote_max_age_seconds: int
    control_artifact_max_age_seconds: int
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


@dataclass(frozen=True)
class PaperFillCheck:
    ready: bool
    reason_codes: Tuple[str, ...]
    available_combo_size: int
    current_net_credit: Decimal
    checked_at: datetime


@dataclass(frozen=True)
class PaperLifecycleCheck:
    action: str
    reason_codes: Tuple[str, ...]
    checked_at: datetime


def evaluate_paper_lifecycle(
    checked_at: datetime,
    planned_exit_reached: bool,
    expiration_reached: bool,
    short_leg_in_the_money: bool,
    ex_dividend_before_expiration: bool,
    assignment_notice_received: bool,
    contract_adjustment_pending: bool,
    settlement_terms_confirmed: bool,
) -> PaperLifecycleCheck:
    """Select a fail-closed operational action; never estimate market risk or RoR."""
    if checked_at.tzinfo is None:
        raise ValueError("lifecycle timestamp must be timezone-aware")
    blocking = []
    if contract_adjustment_pending:
        blocking.append("CONTRACT_ADJUSTMENT_PENDING")
    if not settlement_terms_confirmed:
        blocking.append("SETTLEMENT_TERMS_UNCONFIRMED")
    if blocking:
        return PaperLifecycleCheck("BLOCK_AND_ESCALATE", tuple(sorted(blocking)), checked_at)
    if assignment_notice_received:
        return PaperLifecycleCheck(
            "ASSIGNMENT_RECONCILIATION_REQUIRED",
            ("ASSIGNMENT_NOTICE_RECEIVED",), checked_at,
        )
    if expiration_reached:
        return PaperLifecycleCheck(
            "EXPIRATION_RECONCILIATION_REQUIRED", ("EXPIRATION_REACHED",), checked_at
        )
    if short_leg_in_the_money and ex_dividend_before_expiration:
        return PaperLifecycleCheck(
            "CLOSE_REVIEW_REQUIRED", ("EARLY_ASSIGNMENT_RISK",), checked_at
        )
    if planned_exit_reached:
        return PaperLifecycleCheck(
            "CLOSE_REVIEW_REQUIRED", ("PLANNED_EXIT_REACHED",), checked_at
        )
    return PaperLifecycleCheck("MONITOR", (), checked_at)


def _calculate_plan_hash(
    plan_id: str,
    spread: VerticalSpreadCalculation,
    risk_decision: Decision,
    compliance_decision: BackOfficeDecision,
    created_at: datetime,
    approval_expires_at: datetime,
    execution_quote_max_age_seconds: int,
    control_artifact_max_age_seconds: int,
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
            risk_decision.risk_model_id,
            risk_decision.risk_model_version,
            compliance_decision.candidate_id,
            compliance_decision.account_id,
            compliance_decision.status.value,
            ",".join(compliance_decision.reason_codes),
            compliance_decision.policy_version,
            compliance_decision.portfolio_snapshot_sha256,
            compliance_decision.circuit_breaker_sha256,
            compliance_decision.evaluated_at.isoformat(),
            compliance_decision.environment,
            created_at.isoformat(),
            approval_expires_at.isoformat(),
            str(execution_quote_max_age_seconds),
            str(control_artifact_max_age_seconds),
        )
    )
    return sha256(payload.encode("utf-8")).hexdigest()


def _assert_plan_integrity(plan: PaperTradePlan) -> None:
    expected = _calculate_plan_hash(
        plan.plan_id,
        plan.spread,
        plan.risk_decision,
        plan.compliance_decision,
        plan.created_at,
        plan.approval_expires_at,
        plan.execution_quote_max_age_seconds,
        plan.control_artifact_max_age_seconds,
    )
    if expected != plan.plan_hash:
        raise PermissionError("paper-trade plan integrity check failed")


def create_paper_trade_plan(
    plan_id: str,
    spread: VerticalSpreadCalculation,
    risk_decision: Decision,
    compliance_decision: BackOfficeDecision,
    created_at: datetime,
    approval_expires_at: datetime,
    execution_quote_max_age_seconds: int = 120,
    control_artifact_max_age_seconds: int = 120,
) -> PaperTradePlan:
    if not plan_id:
        raise ValueError("plan identity is required")
    if created_at.tzinfo is None or approval_expires_at.tzinfo is None:
        raise ValueError("plan timestamps must be timezone-aware")
    if approval_expires_at <= created_at:
        raise ValueError("approval expiry must follow plan creation")
    if execution_quote_max_age_seconds <= 0:
        raise ValueError("execution quote age limit must be positive")
    if control_artifact_max_age_seconds <= 0:
        raise ValueError("control artifact age limit must be positive")
    if compliance_decision.environment != "paper":
        raise ValueError("only paper Back Office decisions are accepted")
    if compliance_decision.candidate_id != risk_decision.candidate_id:
        raise ValueError("risk and compliance candidate identities must match")
    if compliance_decision.account_id != risk_decision.account_id:
        raise ValueError("risk and compliance account identities must match")
    if compliance_decision.policy_version not in APPROVED_BACK_OFFICE_POLICY_VERSIONS:
        raise ValueError("Back Office policy version is not approved")
    for label, evaluated_at in (
        ("risk", risk_decision.evaluated_at),
        ("compliance", compliance_decision.evaluated_at),
    ):
        age = (created_at - evaluated_at).total_seconds()
        if age < 0:
            raise ValueError(f"{label} control cannot be from the future")
        if age > control_artifact_max_age_seconds:
            raise ValueError(f"{label} control artifact is stale")

    machine_status = (
        MachineRiskStatus.PASS
        if risk_decision.status is DecisionStatus.RISK_PASS
        else MachineRiskStatus.REJECT
    )
    plan_hash = _calculate_plan_hash(
        plan_id,
        spread,
        risk_decision,
        compliance_decision,
        created_at,
        approval_expires_at,
        execution_quote_max_age_seconds,
        control_artifact_max_age_seconds,
    )
    return PaperTradePlan(
        plan_id=plan_id,
        spread=spread,
        risk_decision=risk_decision,
        compliance_decision=compliance_decision,
        machine_risk_status=machine_status,
        reason_codes=tuple(
            sorted(set(risk_decision.reason_codes + compliance_decision.reason_codes))
        ),
        authorization=HumanAuthorization(HumanAuthorizationStatus.PENDING),
        created_at=created_at,
        approval_expires_at=approval_expires_at,
        execution_quote_max_age_seconds=execution_quote_max_age_seconds,
        control_artifact_max_age_seconds=control_artifact_max_age_seconds,
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
    if plan.compliance_decision.status is not BackOfficeStatus.PASS:
        raise PermissionError("human cannot override a Back Office compliance block")
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
    if plan.compliance_decision.status is not BackOfficeStatus.PASS:
        raise PermissionError("paper execution requires Back Office compliance pass")
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


def evaluate_paper_fill(
    plan: PaperTradePlan,
    available_combo_size: int,
    current_net_credit: Decimal,
    checked_at: datetime,
    contract_adjustment_pending: bool = False,
) -> PaperFillCheck:
    """Fail closed when current executable terms differ from the approved plan."""
    _assert_plan_integrity(plan)
    if checked_at.tzinfo is None:
        raise ValueError("fill-check timestamp must be timezone-aware")
    reasons = []
    if plan.authorization.status is not HumanAuthorizationStatus.APPROVED:
        reasons.append("HUMAN_AUTHORIZATION_REQUIRED")
    if plan.machine_risk_status is not MachineRiskStatus.PASS:
        reasons.append("RISK_PASS_REQUIRED")
    if plan.compliance_decision.status is not BackOfficeStatus.PASS:
        reasons.append("BACK_OFFICE_PASS_REQUIRED")
    if available_combo_size < plan.spread.quantity:
        reasons.append("INSUFFICIENT_COMBO_SIZE")
    if current_net_credit < plan.spread.net_credit:
        reasons.append("APPROVED_CREDIT_NOT_AVAILABLE")
    if contract_adjustment_pending:
        reasons.append("CONTRACT_ADJUSTMENT_PENDING")
    quote_age = (checked_at - max(plan.spread.quote_timestamps)).total_seconds()
    if quote_age < 0:
        reasons.append("CHECK_PRECEDES_QUOTE")
    elif quote_age > plan.execution_quote_max_age_seconds:
        reasons.append("STALE_QUOTE")
    reason_codes = tuple(sorted(set(reasons)))
    return PaperFillCheck(
        not reason_codes,
        reason_codes,
        available_combo_size,
        current_net_credit,
        checked_at,
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
