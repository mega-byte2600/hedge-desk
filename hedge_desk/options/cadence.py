"""Deterministic monthly new-entry cadence with continuous monitoring."""

import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from hashlib import sha256
from typing import Optional, Tuple
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


CADENCE_GATE_VERSION = "monthly-premium-cadence-1.0.0"


@dataclass(frozen=True)
class PremiumCadenceGate:
    evaluated_at: datetime
    last_new_entry_at: Optional[datetime]
    minimum_days_between_entries: int
    cadence_timezone: str
    new_entry_evaluation_allowed: bool
    monitoring_allowed: bool
    reason_codes: Tuple[str, ...]
    artifact_sha256: str
    trade_authorized: bool = False


def evaluate_premium_cadence(
    evaluated_at: datetime,
    last_new_entry_at: Optional[datetime],
    minimum_days_between_entries: int = 21,
    cadence_timezone: str = "America/New_York",
) -> PremiumCadenceGate:
    """Permit monthly research intake without authorizing an order."""
    if evaluated_at.tzinfo is None:
        raise ValueError("cadence evaluation timestamp must be timezone-aware")
    if type(minimum_days_between_entries) is not int or minimum_days_between_entries <= 0:
        raise ValueError("cadence minimum days must be a positive integer")
    if last_new_entry_at is not None and last_new_entry_at.tzinfo is None:
        raise ValueError("last entry timestamp must be timezone-aware")
    try:
        market_timezone = ZoneInfo(cadence_timezone)
    except (TypeError, ZoneInfoNotFoundError) as exc:
        raise ValueError("cadence timezone invalid") from exc
    evaluated_market_time = evaluated_at.astimezone(market_timezone)
    last_market_time = (
        last_new_entry_at.astimezone(market_timezone)
        if last_new_entry_at is not None else None
    )
    reasons = []
    if last_new_entry_at is not None:
        if last_new_entry_at > evaluated_at:
            reasons.append("LAST_ENTRY_FROM_FUTURE")
        if (
            last_market_time is not None
            and last_market_time.year == evaluated_market_time.year
            and last_market_time.month == evaluated_market_time.month
        ):
            reasons.append("MONTHLY_NEW_ENTRY_ALREADY_EVALUATED")
        if evaluated_at - last_new_entry_at < timedelta(
            days=minimum_days_between_entries
        ):
            reasons.append("MINIMUM_ENTRY_INTERVAL_NOT_REACHED")
    reason_codes = tuple(sorted(set(reasons)))
    allowed = not reason_codes
    payload = {
        "evaluated_at": evaluated_at.isoformat(),
        "last_new_entry_at": (
            last_new_entry_at.isoformat() if last_new_entry_at else None
        ),
        "minimum_days_between_entries": minimum_days_between_entries,
        "cadence_timezone": cadence_timezone,
        "monitoring_allowed": True,
        "new_entry_evaluation_allowed": allowed,
        "reason_codes": list(reason_codes),
        "trade_authorized": False,
        "version": CADENCE_GATE_VERSION,
    }
    artifact_sha256 = sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return PremiumCadenceGate(
        evaluated_at, last_new_entry_at, minimum_days_between_entries,
        cadence_timezone,
        allowed, True, reason_codes, artifact_sha256, False,
    )
