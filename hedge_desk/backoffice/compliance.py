"""Versioned paper-only Back Office compliance decision.

This narrow software gate is not a representation that every FINRA, SEC, state,
broker, tax, or registration obligation has been resolved for live trading.
"""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from hashlib import sha256
from typing import Tuple

from hedge_desk.compliance.account_gate import account_gate
from hedge_desk.domain import Account, ProductType, TradeCandidate
from .portfolio import (
    CircuitBreakerResult,
    PositionExposure,
    PortfolioPolicy,
    evaluate_drawdown_circuit_breaker,
    evaluate_portfolio_gate,
)


BACK_OFFICE_POLICY_VERSION = "paper-options-1.0.0"
APPROVED_BACK_OFFICE_POLICY_VERSIONS = frozenset({BACK_OFFICE_POLICY_VERSION})
COMPLIANCE_POLICY_VERSION = "paper-securities-1.0.0"


class BackOfficeStatus(str, Enum):
    PASS = "pass"
    BLOCK = "block"


@dataclass(frozen=True)
class CompliancePolicyDecision:
    """Independent policy artifact; it contains no portfolio-risk calculation."""

    candidate_id: str
    account_id: str
    status: BackOfficeStatus
    reason_codes: Tuple[str, ...]
    policy_version: str
    evaluated_at: datetime
    environment: str
    options_disclosure_version: str
    options_disclosure_acknowledged_at: str
    broker_options_policy_version: str
    artifact_sha256: str


@dataclass(frozen=True)
class BackOfficeDecision:
    candidate_id: str
    account_id: str
    status: BackOfficeStatus
    reason_codes: Tuple[str, ...]
    policy_version: str
    portfolio_snapshot_sha256: str
    circuit_breaker_sha256: str
    policy_decision: CompliancePolicyDecision
    evaluated_at: datetime
    environment: str = "paper"


def _compliance_artifact_hash(
    candidate_id: str,
    account_id: str,
    status: BackOfficeStatus,
    reason_codes: Tuple[str, ...],
    policy_version: str,
    evaluated_at: datetime,
    environment: str,
    options_disclosure_version: str,
    options_disclosure_acknowledged_at: str,
    broker_options_policy_version: str,
) -> str:
    payload = "|".join(
        (
            candidate_id,
            account_id,
            status.value,
            ",".join(reason_codes),
            policy_version,
            evaluated_at.isoformat(),
            environment,
            options_disclosure_version,
            options_disclosure_acknowledged_at,
            broker_options_policy_version,
        )
    )
    return sha256(payload.encode("utf-8")).hexdigest()


def validate_compliance_policy_artifact(
    decision: CompliancePolicyDecision,
) -> Tuple[str, ...]:
    reasons = []
    if decision.policy_version != COMPLIANCE_POLICY_VERSION:
        reasons.append("COMPLIANCE_POLICY_VERSION_UNAPPROVED")
    if decision.evaluated_at.tzinfo is None:
        reasons.append("COMPLIANCE_TIMESTAMP_INVALID")
    if decision.reason_codes != tuple(sorted(set(decision.reason_codes))):
        reasons.append("COMPLIANCE_REASON_CODES_NONCANONICAL")
    expected_status = (
        BackOfficeStatus.BLOCK if decision.reason_codes else BackOfficeStatus.PASS
    )
    if decision.status is not expected_status:
        reasons.append("COMPLIANCE_STATUS_INCONSISTENT")
    expected_hash = _compliance_artifact_hash(
        decision.candidate_id,
        decision.account_id,
        decision.status,
        decision.reason_codes,
        decision.policy_version,
        decision.evaluated_at,
        decision.environment,
        decision.options_disclosure_version,
        decision.options_disclosure_acknowledged_at,
        decision.broker_options_policy_version,
    )
    if decision.artifact_sha256 != expected_hash:
        reasons.append("COMPLIANCE_ARTIFACT_HASH_MISMATCH")
    return tuple(sorted(reasons))


def evaluate_compliance_policy(
    account: Account,
    candidate: TradeCandidate,
    evaluated_at: datetime,
    environment: str = "paper",
) -> CompliancePolicyDecision:
    """Apply the immutable MVP policy separately from risk and portfolio gates."""
    if evaluated_at.tzinfo is None:
        raise ValueError("compliance timestamp must be timezone-aware")
    reasons = account_gate(account, candidate)
    if environment != "paper":
        reasons.append("PAPER_ONLY_VIOLATION")
    if candidate.product_type is not ProductType.DEFINED_RISK_OPTION:
        reasons.append("PREMIUM_MVP_DEFINED_RISK_OPTIONS_ONLY")
    reason_codes = tuple(sorted(set(reasons)))
    status = BackOfficeStatus.BLOCK if reason_codes else BackOfficeStatus.PASS
    artifact_sha256 = _compliance_artifact_hash(
        candidate.candidate_id,
        account.account_id,
        status,
        reason_codes,
        COMPLIANCE_POLICY_VERSION,
        evaluated_at,
        environment,
        account.options_disclosure_version or "",
        (
            account.options_disclosure_acknowledged_at.isoformat()
            if account.options_disclosure_acknowledged_at is not None
            else ""
        ),
        account.broker_options_policy_version or "",
    )
    return CompliancePolicyDecision(
        candidate.candidate_id,
        account.account_id,
        status,
        reason_codes,
        COMPLIANCE_POLICY_VERSION,
        evaluated_at,
        environment,
        account.options_disclosure_version or "",
        (
            account.options_disclosure_acknowledged_at.isoformat()
            if account.options_disclosure_acknowledged_at is not None
            else ""
        ),
        account.broker_options_policy_version or "",
        artifact_sha256,
    )


def evaluate_paper_compliance(
    account: Account,
    candidate: TradeCandidate,
    evaluated_at: datetime,
    positions: Tuple[PositionExposure, ...] = (),
    portfolio_policy: PortfolioPolicy = PortfolioPolicy(),
    circuit_breaker: CircuitBreakerResult = evaluate_drawdown_circuit_breaker(
        current_drawdown=Decimal("0"),
        maximum_drawdown=Decimal("1"),
        source_report_sha256="0" * 64,
    ),
) -> BackOfficeDecision:
    """Evaluate the deliberately narrow paper-only product/account policy."""
    if evaluated_at.tzinfo is None:
        raise ValueError("Back Office timestamp must be timezone-aware")
    compliance = evaluate_compliance_policy(account, candidate, evaluated_at)
    reasons = list(compliance.reason_codes)
    portfolio = evaluate_portfolio_gate(
        account, candidate, positions, portfolio_policy
    )
    reasons.extend(portfolio.reason_codes)
    reasons.extend(circuit_breaker.reason_codes)
    reason_codes = tuple(sorted(set(reasons)))
    return BackOfficeDecision(
        candidate_id=candidate.candidate_id,
        account_id=account.account_id,
        status=BackOfficeStatus.BLOCK if reason_codes else BackOfficeStatus.PASS,
        reason_codes=reason_codes,
        policy_version=BACK_OFFICE_POLICY_VERSION,
        portfolio_snapshot_sha256=portfolio.snapshot_sha256,
        circuit_breaker_sha256=circuit_breaker.artifact_sha256,
        policy_decision=compliance,
        evaluated_at=evaluated_at,
    )
