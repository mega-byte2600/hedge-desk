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


@dataclass(frozen=True)
class FuturesEventCandidate:
    contract: FuturesContractSnapshot
    event: FuturesEventInputs


@dataclass(frozen=True)
class RankedFuturesEvent:
    rank: int
    event_id: str
    contract_id: str
    event_type: PhysicalEventType
    residual_edge_per_contract: Decimal
    trade_authorized: bool = False


@dataclass(frozen=True)
class FuturesUniverseEvaluation:
    disposition: str
    candidates: Tuple[RankedFuturesEvent, ...]
    rejected_events: Tuple[Tuple[str, Tuple[str, ...]], ...]
    trade_authorized: bool = False


def _valid_hash(value: str) -> bool:
    try:
        return isinstance(value, str) and len(value) == 64 and int(value, 16) > 0
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
    decimal_values = (
        contract.initial_margin,
        event.modeled_gross_impact_per_contract,
        event.curve_priced_impact_per_contract,
        event.basis_reserve_per_contract,
        event.roll_cost_per_contract,
        event.transaction_cost_per_contract,
        minimum_edge_buffer,
    )
    if any(
        not isinstance(value, Decimal) or not value.is_finite()
        for value in decimal_values
    ):
        raise ValueError("futures numeric inputs must be finite Decimals")
    if type(minimum_daily_volume) is not int or minimum_daily_volume < 0:
        raise ValueError("minimum futures volume must be a nonnegative integer")
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


def evaluate_futures_universe(
    candidates: Tuple[FuturesEventCandidate, ...],
    decision_time: datetime,
    minimum_edge_buffer: Decimal,
    minimum_daily_volume: int = 1000,
) -> FuturesUniverseEvaluation:
    if not candidates:
        raise ValueError("futures event universe cannot be empty")
    identities = [item.event.event_id for item in candidates]
    if any(not item for item in identities) or len(identities) != len(set(identities)):
        raise ValueError("futures event identities must be unique and nonempty")
    admitted = []
    rejected = []
    for item in sorted(candidates, key=lambda value: value.event.event_id):
        result = evaluate_futures_event(
            item.contract,
            item.event,
            decision_time,
            minimum_edge_buffer,
            minimum_daily_volume,
        )
        if result.reason_codes:
            rejected.append((item.event.event_id, result.reason_codes))
        else:
            admitted.append((item, result))
    ordered = sorted(
        admitted,
        key=lambda value: (-value[1].residual_edge_per_contract, value[0].event.event_id),
    )
    ranked = tuple(
        RankedFuturesEvent(
            rank,
            item.event.event_id,
            item.contract.contract_id,
            item.event.event_type,
            result.residual_edge_per_contract,
        )
        for rank, (item, result) in enumerate(ordered, start=1)
    )
    return FuturesUniverseEvaluation(
        "EVENT_RESEARCH_CANDIDATES" if ranked else "NO_TRADE",
        ranked,
        tuple(rejected),
    )
