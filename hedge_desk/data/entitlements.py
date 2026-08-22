"""Deterministic data-entitlement readiness checks; no vendor payload access."""

from dataclasses import dataclass
from decimal import Decimal
from typing import Tuple


@dataclass(frozen=True)
class DataSubscription:
    source_id: str
    monthly_cost: Decimal
    entitlement_id: str
    historical_nbbo_quotes: bool
    expired_option_contracts: bool
    option_chain_snapshots: bool
    corporate_actions: bool
    redistribution_allowed: bool


@dataclass(frozen=True)
class DataReadinessResult:
    ready_for_internal_options_research: bool
    total_monthly_cost: Decimal
    reason_codes: Tuple[str, ...]
    raw_payload_commit_allowed: bool = False


def evaluate_options_data_stack(
    subscriptions: Tuple[DataSubscription, ...],
    monthly_budget: Decimal,
) -> DataReadinessResult:
    """Require executable historical evidence within budget and fail closed."""
    if monthly_budget < 0:
        raise ValueError("monthly budget cannot be negative")
    if not subscriptions:
        return DataReadinessResult(False, Decimal("0"), ("DATA_SOURCE_ABSENT",))
    identities = [item.source_id for item in subscriptions]
    if any(not item for item in identities) or len(identities) != len(set(identities)):
        raise ValueError("subscription source identities must be unique and nonempty")
    reasons = []
    total = sum((item.monthly_cost for item in subscriptions), Decimal("0"))
    if any(item.monthly_cost < 0 for item in subscriptions):
        reasons.append("SUBSCRIPTION_COST_INVALID")
    if total > monthly_budget:
        reasons.append("MONTHLY_DATA_BUDGET_EXCEEDED")
    if any(not item.entitlement_id for item in subscriptions):
        reasons.append("DATA_ENTITLEMENT_UNVERIFIED")
    required_capabilities = {
        "HISTORICAL_NBBO_QUOTES_ABSENT": any(
            item.historical_nbbo_quotes for item in subscriptions
        ),
        "EXPIRED_OPTION_CONTRACTS_ABSENT": any(
            item.expired_option_contracts for item in subscriptions
        ),
        "OPTION_CHAIN_SNAPSHOTS_ABSENT": any(
            item.option_chain_snapshots for item in subscriptions
        ),
        "CORPORATE_ACTIONS_ABSENT": any(
            item.corporate_actions for item in subscriptions
        ),
    }
    reasons.extend(
        reason for reason, present in required_capabilities.items() if not present
    )
    reason_codes = tuple(sorted(set(reasons)))
    return DataReadinessResult(not reason_codes, total, reason_codes, False)
