"""Versioned paper-only Back Office compliance decision.

This narrow software gate is not a representation that every FINRA, SEC, state,
broker, tax, or registration obligation has been resolved for live trading.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Tuple

from hedge_desk.compliance.account_gate import account_gate
from hedge_desk.domain import Account, ProductType, TradeCandidate
from .portfolio import PositionExposure, PortfolioPolicy, evaluate_portfolio_gate


BACK_OFFICE_POLICY_VERSION = "paper-options-1.0.0"
APPROVED_BACK_OFFICE_POLICY_VERSIONS = frozenset({BACK_OFFICE_POLICY_VERSION})


class BackOfficeStatus(str, Enum):
    PASS = "pass"
    BLOCK = "block"


@dataclass(frozen=True)
class BackOfficeDecision:
    candidate_id: str
    account_id: str
    status: BackOfficeStatus
    reason_codes: Tuple[str, ...]
    policy_version: str
    portfolio_snapshot_sha256: str
    evaluated_at: datetime
    environment: str = "paper"


def evaluate_paper_compliance(
    account: Account,
    candidate: TradeCandidate,
    evaluated_at: datetime,
    positions: Tuple[PositionExposure, ...] = (),
    portfolio_policy: PortfolioPolicy = PortfolioPolicy(),
) -> BackOfficeDecision:
    """Evaluate the deliberately narrow paper-only product/account policy."""
    if evaluated_at.tzinfo is None:
        raise ValueError("Back Office timestamp must be timezone-aware")
    reasons = account_gate(account, candidate)
    portfolio = evaluate_portfolio_gate(
        account, candidate, positions, portfolio_policy
    )
    reasons.extend(portfolio.reason_codes)
    if candidate.product_type is not ProductType.DEFINED_RISK_OPTION:
        reasons.append("PREMIUM_MVP_DEFINED_RISK_OPTIONS_ONLY")
    reason_codes = tuple(sorted(set(reasons)))
    return BackOfficeDecision(
        candidate_id=candidate.candidate_id,
        account_id=account.account_id,
        status=BackOfficeStatus.BLOCK if reason_codes else BackOfficeStatus.PASS,
        reason_codes=reason_codes,
        policy_version=BACK_OFFICE_POLICY_VERSION,
        portfolio_snapshot_sha256=portfolio.snapshot_sha256,
        evaluated_at=evaluated_at,
    )
