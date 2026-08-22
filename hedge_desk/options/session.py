"""Deterministic exchange-session evidence gate for option decisions."""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Tuple


@dataclass(frozen=True)
class MarketSessionEvidence:
    venue: str
    regular_open: datetime
    regular_close: datetime
    received_at: datetime
    calendar_artifact_sha256: str


@dataclass(frozen=True)
class MarketSessionGate:
    admissible: bool
    reason_codes: Tuple[str, ...]
    latest_entry_time: datetime


def _valid_hash(value: str) -> bool:
    try:
        return len(value) == 64 and int(value, 16) >= 0
    except ValueError:
        return False


def evaluate_market_session(
    evidence: MarketSessionEvidence,
    decision_time: datetime,
    minimum_seconds_before_close: int,
) -> MarketSessionGate:
    """Use supplied exchange-calendar evidence; never infer holidays or hours."""
    if minimum_seconds_before_close < 0:
        raise ValueError("minimum seconds before close cannot be negative")
    timestamps = (
        evidence.regular_open,
        evidence.regular_close,
        evidence.received_at,
        decision_time,
    )
    reasons = []
    aware = all(value.tzinfo is not None for value in timestamps)
    if not aware:
        reasons.append("MARKET_SESSION_TIMESTAMP_NOT_TIMEZONE_AWARE")
    if not evidence.venue:
        reasons.append("MARKET_VENUE_MISSING")
    if not _valid_hash(evidence.calendar_artifact_sha256):
        reasons.append("MARKET_CALENDAR_HASH_INVALID")
    if aware:
        if evidence.regular_close <= evidence.regular_open:
            reasons.append("MARKET_SESSION_INTERVAL_INVALID")
        if evidence.received_at > decision_time:
            reasons.append("MARKET_CALENDAR_NOT_POINT_IN_TIME")
    latest_entry = evidence.regular_close - timedelta(
        seconds=minimum_seconds_before_close
    )
    if aware and evidence.regular_close > evidence.regular_open:
        if decision_time < evidence.regular_open:
            reasons.append("MARKET_NOT_OPEN")
        if decision_time > latest_entry:
            reasons.append("MARKET_ENTRY_WINDOW_CLOSED")
    reason_codes = tuple(sorted(set(reasons)))
    return MarketSessionGate(not reason_codes, reason_codes, latest_entry)
