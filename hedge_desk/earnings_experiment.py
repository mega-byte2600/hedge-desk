"""Pre-release locked experiment assignment for earnings strategy evaluation."""

import json
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from hashlib import sha256


EXPERIMENT_POLICY_VERSION = "earnings-four-arm-1.0.0"


class EarningsExperimentArm(str, Enum):
    EQUITY = "EQUITY"
    DEFINED_RISK_OPTION = "DEFINED_RISK_OPTION"
    HEDGED_EQUITY = "HEDGED_EQUITY"
    NO_TRADE = "NO_TRADE"


@dataclass(frozen=True)
class EarningsExperimentPlan:
    experiment_id: str
    candidate_id: str
    assigned_arm: EarningsExperimentArm
    assigned_at: datetime
    scheduled_release_at: datetime
    assignment_salt_sha256: str
    policy_version: str
    plan_sha256: str
    trade_authorized: bool = False


@dataclass(frozen=True)
class EarningsExperimentOutcome:
    plan_sha256: str
    assigned_arm: EarningsExperimentArm
    gross_pnl: Decimal
    costs: Decimal
    net_pnl: Decimal
    observed_at: datetime
    hypothetical: bool = True
    trade_authorized: bool = False


def _valid_hash(value: str) -> bool:
    try:
        return len(value) == 64 and int(value, 16) >= 0
    except ValueError:
        return False


def assign_earnings_experiment(
    experiment_id: str,
    candidate_id: str,
    assigned_at: datetime,
    scheduled_release_at: datetime,
    assignment_salt_sha256: str,
) -> EarningsExperimentPlan:
    if not experiment_id or not candidate_id:
        raise ValueError("experiment and candidate identities are required")
    if assigned_at.tzinfo is None or scheduled_release_at.tzinfo is None:
        raise ValueError("experiment timestamps must be timezone-aware")
    if assigned_at >= scheduled_release_at:
        raise ValueError("experiment assignment must precede scheduled release")
    if not _valid_hash(assignment_salt_sha256):
        raise ValueError("experiment assignment salt hash invalid")
    identity = "|".join((
        EXPERIMENT_POLICY_VERSION, experiment_id, candidate_id,
        assignment_salt_sha256,
    ))
    digest = sha256(identity.encode()).hexdigest()
    arms = tuple(EarningsExperimentArm)
    assigned_arm = arms[int(digest, 16) % len(arms)]
    payload = {
        "assigned_arm": assigned_arm.value,
        "assigned_at": assigned_at.isoformat(),
        "assignment_salt_sha256": assignment_salt_sha256,
        "candidate_id": candidate_id,
        "experiment_id": experiment_id,
        "policy_version": EXPERIMENT_POLICY_VERSION,
        "scheduled_release_at": scheduled_release_at.isoformat(),
        "trade_authorized": False,
    }
    plan_hash = sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return EarningsExperimentPlan(
        experiment_id, candidate_id, assigned_arm, assigned_at,
        scheduled_release_at, assignment_salt_sha256,
        EXPERIMENT_POLICY_VERSION, plan_hash, False,
    )


def validate_earnings_experiment_plan(
    plan: EarningsExperimentPlan,
) -> tuple[str, ...]:
    reasons = []
    if plan.policy_version != EXPERIMENT_POLICY_VERSION:
        reasons.append("EARNINGS_EXPERIMENT_POLICY_INVALID")
    if plan.trade_authorized:
        reasons.append("EARNINGS_EXPERIMENT_AUTHORITY_FORBIDDEN")
    try:
        rebuilt = assign_earnings_experiment(
            plan.experiment_id,
            plan.candidate_id,
            plan.assigned_at,
            plan.scheduled_release_at,
            plan.assignment_salt_sha256,
        )
    except ValueError:
        reasons.append("EARNINGS_EXPERIMENT_PLAN_INVALID")
    else:
        if plan.assigned_arm is not rebuilt.assigned_arm:
            reasons.append("EARNINGS_EXPERIMENT_ARM_TAMPER")
        if plan.plan_sha256 != rebuilt.plan_sha256:
            reasons.append("EARNINGS_EXPERIMENT_HASH_MISMATCH")
    return tuple(sorted(set(reasons)))


def score_earnings_experiment(
    plan: EarningsExperimentPlan,
    gross_pnl: Decimal,
    costs: Decimal,
    observed_at: datetime,
) -> EarningsExperimentOutcome:
    reasons = validate_earnings_experiment_plan(plan)
    if reasons:
        raise ValueError("earnings experiment plan invalid:" + ",".join(reasons))
    if observed_at.tzinfo is None:
        raise ValueError("experiment outcome timestamp must be timezone-aware")
    if observed_at <= plan.scheduled_release_at:
        raise ValueError("experiment outcome must follow scheduled release")
    if costs < 0:
        raise ValueError("experiment costs cannot be negative")
    return EarningsExperimentOutcome(
        plan.plan_sha256,
        plan.assigned_arm,
        gross_pnl,
        costs,
        gross_pnl - costs,
        observed_at,
        True,
        False,
    )
