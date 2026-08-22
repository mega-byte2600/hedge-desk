"""Point-in-time corporate-event gate for option holding windows."""

import json
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from hashlib import sha256
from typing import Tuple

from .spreads import OptionType, VerticalSpreadCalculation


class CorporateEventType(str, Enum):
    EARNINGS = "EARNINGS"
    EX_DIVIDEND = "EX_DIVIDEND"


@dataclass(frozen=True)
class ScheduledCorporateEvent:
    event_id: str
    symbol: str
    event_type: CorporateEventType
    event_date: date
    published_at: datetime
    source_artifact_sha256: str


@dataclass(frozen=True)
class EventCalendarGate:
    admissible: bool
    reason_codes: Tuple[str, ...]
    calendar_sha256: str
    complete_through: date


def _valid_hash(value: str) -> bool:
    try:
        return len(value) == 64 and int(value, 16) >= 0
    except ValueError:
        return False


def evaluate_event_calendar(
    symbol: str,
    calendar_as_of: datetime,
    complete_through: date,
    events: Tuple[ScheduledCorporateEvent, ...],
    spread: VerticalSpreadCalculation,
    short_option_type: OptionType,
    short_strike: Decimal,
) -> EventCalendarGate:
    if not symbol or calendar_as_of.tzinfo is None:
        raise ValueError("calendar identity and timezone-aware as-of are required")
    if len({event.event_id for event in events}) != len(events):
        raise ValueError("corporate event identities must be unique")
    reasons = []
    if complete_through < spread.expiration_date:
        reasons.append("EVENT_CALENDAR_INCOMPLETE_THROUGH_EXPIRATION")
    for event in events:
        if not event.event_id or event.symbol != symbol:
            reasons.append("EVENT_IDENTITY_MISMATCH")
        if event.published_at.tzinfo is None:
            reasons.append("EVENT_TIMESTAMP_NOT_TIMEZONE_AWARE")
        elif event.published_at > calendar_as_of:
            reasons.append("EVENT_NOT_POINT_IN_TIME")
        if not _valid_hash(event.source_artifact_sha256):
            reasons.append("EVENT_SOURCE_HASH_INVALID")
        inside_holding_window = (
            calendar_as_of.date() <= event.event_date <= spread.planned_exit_date
        )
        if event.event_type is CorporateEventType.EARNINGS and inside_holding_window:
            reasons.append("EARNINGS_INSIDE_PLANNED_HOLDING_WINDOW")
        short_call_in_the_money = (
            short_option_type is OptionType.CALL and spread.underlying_ask > short_strike
        )
        if (
            event.event_type is CorporateEventType.EX_DIVIDEND
            and inside_holding_window
            and short_call_in_the_money
        ):
            reasons.append("EX_DIVIDEND_EARLY_ASSIGNMENT_RISK")
    payload = {
        "calendar_as_of": calendar_as_of.isoformat(),
        "complete_through": complete_through.isoformat(),
        "events": [
            {
                "event_date": event.event_date.isoformat(),
                "event_id": event.event_id,
                "event_type": event.event_type.value,
                "published_at": event.published_at.isoformat(),
                "source_artifact_sha256": event.source_artifact_sha256,
                "symbol": event.symbol,
            }
            for event in sorted(events, key=lambda item: item.event_id)
        ],
        "spread_id": spread.spread_id,
        "symbol": symbol,
    }
    calendar_hash = sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    reason_codes = tuple(sorted(set(reasons)))
    return EventCalendarGate(not reason_codes, reason_codes, calendar_hash, complete_through)
