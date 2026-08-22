"""Delayed aggregate FINRA OTC transparency evidence; never a live dark-order feed."""

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import Tuple


@dataclass(frozen=True)
class OtcWeeklyObservation:
    observation_id: str
    symbol: str
    tier: str
    week_start: date
    total_share_quantity: int
    total_trade_count: int
    published_at: datetime
    received_at: datetime
    declared_publication_delay_days: int
    source_artifact_sha256: str


@dataclass(frozen=True)
class OtcTransparencyEvaluation:
    admissible: bool
    reason_codes: Tuple[str, ...]
    average_shares_per_trade: Decimal
    delayed_aggregate_evidence: bool = True
    live_hidden_order_visibility: bool = False
    directional_signal_authorized: bool = False
    trade_authorized: bool = False


def _valid_hash(value: str) -> bool:
    try:
        return len(value) == 64 and int(value, 16) >= 0
    except ValueError:
        return False


def evaluate_otc_weekly_observation(
    observation: OtcWeeklyObservation,
    decision_time: datetime,
) -> OtcTransparencyEvaluation:
    if decision_time.tzinfo is None:
        raise ValueError("OTC decision time must be timezone-aware")
    reasons = []
    if not observation.observation_id or not observation.symbol:
        reasons.append("OTC_OBSERVATION_IDENTITY_MISSING")
    if observation.tier not in {"T1", "T2", "OTCE"}:
        reasons.append("OTC_TIER_INVALID")
    minimum_delay = 14 if observation.tier == "T1" else 28
    if observation.declared_publication_delay_days < minimum_delay:
        reasons.append("OTC_PUBLICATION_DELAY_UNDERSTATED")
    if observation.total_share_quantity < 0 or observation.total_trade_count <= 0:
        reasons.append("OTC_AGGREGATE_INPUT_INVALID")
    if observation.published_at.tzinfo is None or observation.received_at.tzinfo is None:
        reasons.append("OTC_TIMESTAMP_NOT_TIMEZONE_AWARE")
    else:
        period_end = datetime.combine(
            observation.week_start + timedelta(days=7),
            datetime.min.time(),
            tzinfo=observation.published_at.tzinfo,
        )
        if observation.published_at < period_end:
            reasons.append("OTC_PUBLICATION_PRECEDES_PERIOD_END")
        if observation.received_at < observation.published_at:
            reasons.append("OTC_RECEIVED_BEFORE_PUBLICATION")
        if observation.received_at > decision_time:
            reasons.append("OTC_POINT_IN_TIME_VIOLATION")
    if not _valid_hash(observation.source_artifact_sha256):
        reasons.append("OTC_SOURCE_HASH_INVALID")
    average = (
        Decimal(observation.total_share_quantity) / Decimal(observation.total_trade_count)
        if observation.total_trade_count > 0 else Decimal("0")
    )
    reason_codes = tuple(sorted(set(reasons)))
    return OtcTransparencyEvaluation(not reason_codes, reason_codes, average)
