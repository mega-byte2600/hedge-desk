"""Point-in-time earnings surprise calculation with no directional trade claim."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional, Tuple


@dataclass(frozen=True)
class EarningsConsensus:
    symbol: str
    fiscal_period: str
    eps_consensus: Decimal
    revenue_consensus: Decimal
    analyst_count: int
    as_of: datetime
    source_artifact_sha256: str


@dataclass(frozen=True)
class EarningsRelease:
    symbol: str
    fiscal_period: str
    eps_actual: Decimal
    revenue_actual: Decimal
    published_at: datetime
    received_at: datetime
    source_artifact_sha256: str


@dataclass(frozen=True)
class EarningsSurpriseResult:
    admissible: bool
    reason_codes: Tuple[str, ...]
    eps_surprise_fraction: Optional[Decimal]
    revenue_surprise_fraction: Optional[Decimal]
    surprise_alignment: str
    directional_trade_authorized: bool = False


@dataclass(frozen=True)
class EarningsEventInput:
    event_id: str
    consensus: EarningsConsensus
    release: EarningsRelease


@dataclass(frozen=True)
class RankedEarningsEvent:
    rank: int
    event_id: str
    symbol: str
    fiscal_period: str
    eps_surprise_fraction: Decimal
    revenue_surprise_fraction: Decimal
    surprise_alignment: str
    combined_absolute_surprise: Decimal
    directional_trade_authorized: bool = False


@dataclass(frozen=True)
class EarningsUniverseEvaluation:
    disposition: str
    candidates: Tuple[RankedEarningsEvent, ...]
    rejected_events: Tuple[Tuple[str, Tuple[str, ...]], ...]
    directional_trade_authorized: bool = False


def _valid_hash(value: str) -> bool:
    try:
        return isinstance(value, str) and len(value) == 64 and int(value, 16) > 0
    except ValueError:
        return False


def evaluate_earnings_surprise(
    consensus: EarningsConsensus,
    release: EarningsRelease,
    decision_time: datetime,
    minimum_analyst_count: int = 3,
) -> EarningsSurpriseResult:
    if decision_time.tzinfo is None:
        raise ValueError("decision timestamp must be timezone-aware")
    if type(minimum_analyst_count) is not int or minimum_analyst_count <= 0:
        raise ValueError("minimum analyst count must be a positive integer")
    numeric_values = (
        consensus.eps_consensus,
        consensus.revenue_consensus,
        release.eps_actual,
        release.revenue_actual,
    )
    if any(
        not isinstance(value, Decimal) or not value.is_finite()
        for value in numeric_values
    ):
        raise ValueError("earnings numeric inputs must be finite Decimals")
    reasons = []
    if consensus.as_of.tzinfo is None or release.published_at.tzinfo is None or release.received_at.tzinfo is None:
        reasons.append("EARNINGS_TIMESTAMP_NOT_TIMEZONE_AWARE")
    else:
        if consensus.as_of >= release.published_at:
            reasons.append("CONSENSUS_NOT_POINT_IN_TIME")
        if release.received_at < release.published_at:
            reasons.append("RELEASE_RECEIVED_BEFORE_PUBLICATION")
        if decision_time < release.received_at:
            reasons.append("DECISION_PRECEDES_RELEASE_RECEIPT")
    if consensus.symbol != release.symbol or consensus.fiscal_period != release.fiscal_period:
        reasons.append("EARNINGS_IDENTITY_MISMATCH")
    if consensus.analyst_count < minimum_analyst_count:
        reasons.append("CONSENSUS_BREADTH_INSUFFICIENT")
    if consensus.eps_consensus == 0 or consensus.revenue_consensus == 0:
        reasons.append("CONSENSUS_DENOMINATOR_ZERO")
    if not _valid_hash(consensus.source_artifact_sha256) or not _valid_hash(
        release.source_artifact_sha256
    ):
        reasons.append("EARNINGS_SOURCE_HASH_INVALID")
    reason_codes = tuple(sorted(set(reasons)))
    if reason_codes:
        return EarningsSurpriseResult(False, reason_codes, None, None, "UNAVAILABLE")
    eps = (release.eps_actual - consensus.eps_consensus) / abs(consensus.eps_consensus)
    revenue = (
        (release.revenue_actual - consensus.revenue_consensus)
        / abs(consensus.revenue_consensus)
    )
    if eps > 0 and revenue > 0:
        alignment = "BOTH_POSITIVE"
    elif eps < 0 and revenue < 0:
        alignment = "BOTH_NEGATIVE"
    else:
        alignment = "MIXED"
    return EarningsSurpriseResult(True, (), eps, revenue, alignment)


def evaluate_earnings_universe(
    events: Tuple[EarningsEventInput, ...],
    decision_time: datetime,
) -> EarningsUniverseEvaluation:
    if not events:
        raise ValueError("earnings event universe cannot be empty")
    event_ids = [event.event_id for event in events]
    if any(not event_id for event_id in event_ids) or len(event_ids) != len(set(event_ids)):
        raise ValueError("earnings event identities must be unique and nonempty")
    admitted = []
    rejected = []
    for event in sorted(events, key=lambda item: item.event_id):
        result = evaluate_earnings_surprise(
            event.consensus, event.release, decision_time
        )
        reasons = list(result.reason_codes)
        if result.admissible and result.surprise_alignment == "MIXED":
            reasons.append("SURPRISE_NOT_ALIGNED")
        reason_codes = tuple(sorted(set(reasons)))
        if reason_codes:
            rejected.append((event.event_id, reason_codes))
            continue
        assert result.eps_surprise_fraction is not None
        assert result.revenue_surprise_fraction is not None
        admitted.append((event, result))
    ordered = sorted(
        admitted,
        key=lambda item: (
            -(
                abs(item[1].eps_surprise_fraction)
                + abs(item[1].revenue_surprise_fraction)
            ),
            item[0].event_id,
        ),
    )
    candidates = tuple(
        RankedEarningsEvent(
            rank,
            event.event_id,
            event.consensus.symbol,
            event.consensus.fiscal_period,
            result.eps_surprise_fraction,
            result.revenue_surprise_fraction,
            result.surprise_alignment,
            abs(result.eps_surprise_fraction)
            + abs(result.revenue_surprise_fraction),
        )
        for rank, (event, result) in enumerate(ordered, start=1)
    )
    return EarningsUniverseEvaluation(
        "ALIGNED_RESEARCH_EVENTS" if candidates else "NO_TRADE",
        candidates,
        tuple(rejected),
        False,
    )
