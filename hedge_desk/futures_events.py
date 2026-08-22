"""Deterministic weather/war/logistics futures-event research economics."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Tuple


class PhysicalEventType(str, Enum):
    EXTREME_WEATHER = "EXTREME_WEATHER"
    WAR_GEOPOLITICAL = "WAR_GEOPOLITICAL"
    SHIPPING_DISRUPTION = "SHIPPING_DISRUPTION"


@dataclass(frozen=True)
class FuturesContractSnapshot:
    contract_id: str
    average_daily_volume: int
    initial_margin: Decimal
    physically_deliverable: bool
    last_trade_date_known: bool
    source_artifact_sha256: str


@dataclass(frozen=True)
class FuturesEventInputs:
    event_id: str
    event_type: PhysicalEventType
    observed_at: datetime
    received_at: datetime
    modeled_gross_impact_per_contract: Decimal
    curve_priced_impact_per_contract: Decimal
    basis_reserve_per_contract: Decimal
    roll_cost_per_contract: Decimal
    transaction_cost_per_contract: Decimal
    source_artifact_sha256: str
    impact_model_artifact_sha256: str


@dataclass(frozen=True)
class FuturesEventEvaluation:
    admissible: bool
    disposition: str
    reason_codes: Tuple[str, ...]
    residual_edge_per_contract: Decimal
    trade_authorized: bool = False
    environment: str = "paper"


def _valid_hash(value: str) -> bool:
    try:
        return len(value) == 64 and int(value, 16) >= 0
    except ValueError:
        return False


def evaluate_futures_event(
    contract: FuturesContractSnapshot,
    event: FuturesEventInputs,
    decision_time: datetime,
    minimum_edge_buffer: Decimal,
    minimum_daily_volume: int = 1000,
) -> FuturesEventEvaluation:
    if decision_time.tzinfo is None:
        raise ValueError("decision timestamp must be timezone-aware")
    if minimum_edge_buffer < 0:
        raise ValueError("minimum edge buffer cannot be negative")
    reasons = []
    if event.observed_at.tzinfo is None or event.received_at.tzinfo is None:
        reasons.append("EVENT_TIMESTAMP_NOT_TIMEZONE_AWARE")
    else:
        if event.received_at < event.observed_at:
            reasons.append("EVENT_RECEIVED_BEFORE_OBSERVED")
        if decision_time < event.received_at:
            reasons.append("EVENT_NOT_POINT_IN_TIME")
    if not contract.contract_id or not event.event_id:
        reasons.append("FUTURES_EVENT_IDENTITY_MISSING")
    if contract.average_daily_volume < minimum_daily_volume:
        reasons.append("FUTURES_LIQUIDITY_INSUFFICIENT")
    if contract.initial_margin <= 0:
        reasons.append("FUTURES_MARGIN_INVALID")
    if contract.physically_deliverable:
        reasons.append("PHYSICAL_DELIVERY_DISABLED")
    if not contract.last_trade_date_known:
        reasons.append("LAST_TRADE_DATE_UNKNOWN")
    hashes = (
        contract.source_artifact_sha256,
        event.source_artifact_sha256,
        event.impact_model_artifact_sha256,
    )
    if not all(_valid_hash(value) for value in hashes):
        reasons.append("FUTURES_EVENT_SOURCE_HASH_INVALID")
    reserves = (
        event.basis_reserve_per_contract,
        event.roll_cost_per_contract,
        event.transaction_cost_per_contract,
    )
    if any(value < 0 for value in reserves):
        reasons.append("FUTURES_COST_INPUT_INVALID")
    residual = (
        event.modeled_gross_impact_per_contract
        - event.curve_priced_impact_per_contract
        - event.basis_reserve_per_contract
        - event.roll_cost_per_contract
        - event.transaction_cost_per_contract
    )
    if residual < minimum_edge_buffer:
        reasons.append("EVENT_EDGE_BELOW_SAFETY_BUFFER")
    reason_codes = tuple(sorted(set(reasons)))
    return FuturesEventEvaluation(
        not reason_codes,
        "EVENT_RESEARCH_CANDIDATE" if not reason_codes else "NO_TRADE",
        reason_codes,
        residual,
    )
