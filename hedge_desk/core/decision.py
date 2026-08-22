"""Combine independent eligibility and economic-risk gates."""

from datetime import datetime
from decimal import Decimal

from hedge_desk.compliance.account_gate import account_gate
from hedge_desk.domain import Account, Decision, DecisionStatus, TradeCandidate
from hedge_desk.risk.ruin import RiskPolicy, estimate_risk_of_ruin, risk_gate


def evaluate_candidate(
    account: Account,
    candidate: TradeCandidate,
    evaluated_at: datetime,
    policy: RiskPolicy = RiskPolicy(),
) -> Decision:
    """Create a deterministic paper-only decision with auditable reasons."""
    reasons = account_gate(account, candidate)
    reasons.extend(risk_gate(account, candidate, evaluated_at, policy))
    reason_codes = tuple(sorted(set(reasons)))

    ruin_after = estimate_risk_of_ruin(
        account.equity,
        candidate.max_loss,
        candidate.win_probability,
        candidate.expected_win,
    )
    return Decision(
        candidate_id=candidate.candidate_id,
        account_id=account.account_id,
        status=(
            DecisionStatus.BLOCKED
            if reason_codes
            else DecisionStatus.RISK_PASS
        ),
        reason_codes=reason_codes,
        risk_of_ruin_before=Decimal("0"),
        risk_of_ruin_after=ruin_after,
        evaluated_at=evaluated_at,
    )
