"""Combine independent eligibility and economic-risk gates."""

from datetime import datetime
from typing import Optional

from hedge_desk.compliance.account_gate import account_gate
from hedge_desk.domain import Account, Decision, DecisionStatus, TradeCandidate
from hedge_desk.risk.ruin import (
    RiskPolicy,
    risk_gate,
)
from hedge_desk.risk.inputs import ValidatedRiskInputs, validate_risk_inputs


def evaluate_candidate(
    account: Account,
    candidate: TradeCandidate,
    evaluated_at: datetime,
    policy: RiskPolicy = RiskPolicy(),
    risk_inputs: Optional[ValidatedRiskInputs] = None,
) -> Decision:
    """Create a deterministic paper-only decision with auditable reasons."""
    if risk_inputs is None:
        raise ValueError("validated quantitative risk inputs are required")
    validate_risk_inputs(risk_inputs)
    if risk_inputs.candidate_id != candidate.candidate_id:
        raise ValueError("risk inputs are bound to another candidate")
    if (
        risk_inputs.maximum_loss != candidate.max_loss
        or risk_inputs.expected_win != candidate.expected_win
        or risk_inputs.win_probability != candidate.win_probability
    ):
        raise ValueError("candidate economics differ from validated risk inputs")
    if risk_inputs.as_of > evaluated_at:
        raise ValueError("risk inputs cannot be from the future")
    if (
        risk_inputs.risk_model_id != policy.required_risk_model_id
        or risk_inputs.risk_model_version != policy.required_risk_model_version
    ):
        raise ValueError("risk model is not permitted by policy")
    if risk_inputs.validator_id not in policy.permitted_validator_ids:
        raise ValueError("risk validator is not permitted by policy")
    reasons = account_gate(account, candidate)
    reasons.extend(
        risk_gate(
            account,
            candidate,
            evaluated_at,
            policy,
            risk_inputs.risk_of_ruin_after,
        )
    )
    reason_codes = tuple(sorted(set(reasons)))

    return Decision(
        candidate_id=candidate.candidate_id,
        account_id=account.account_id,
        status=(
            DecisionStatus.BLOCKED
            if reason_codes
            else DecisionStatus.RISK_PASS
        ),
        reason_codes=reason_codes,
        risk_of_ruin_before=risk_inputs.risk_of_ruin_before,
        risk_of_ruin_after=risk_inputs.risk_of_ruin_after,
        evaluated_at=evaluated_at,
        risk_model_id=risk_inputs.risk_model_id,
        risk_model_version=risk_inputs.risk_model_version,
        risk_input_sha256=risk_inputs.artifact_sha256,
        risk_source_artifact_sha256=risk_inputs.source_artifact_sha256,
        portfolio_snapshot_sha256=risk_inputs.portfolio_snapshot_sha256,
    )
