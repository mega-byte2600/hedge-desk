"""Chronological replay gate preventing look-ahead and control bypass."""

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, Tuple

from hedge_desk.demo import FIXTURE_AS_OF


class ReplayEventKind(str, Enum):
    SOURCE_PUBLISHED = "SOURCE_PUBLISHED"
    SYSTEM_RECEIVED = "SYSTEM_RECEIVED"
    VALIDATION_COMPLETE = "VALIDATION_COMPLETE"
    CANDIDATE_CREATED = "CANDIDATE_CREATED"
    RISK_COMPLETE = "RISK_COMPLETE"
    COMPLIANCE_COMPLETE = "COMPLIANCE_COMPLETE"
    HUMAN_APPROVED = "HUMAN_APPROVED"
    PAPER_FILL = "PAPER_FILL"
    EXIT = "EXIT"


REQUIRED_ORDER = tuple(ReplayEventKind)


@dataclass(frozen=True)
class ReplayEvent:
    kind: ReplayEventKind
    event_time: datetime
    received_time: datetime
    artifact_id: str


@dataclass(frozen=True)
class ReplayValidation:
    valid: bool
    reason_codes: Tuple[str, ...]


def validate_replay(events: Tuple[ReplayEvent, ...]) -> ReplayValidation:
    """Require a complete, ordered, timezone-aware paper decision timeline."""
    reasons = []
    kinds = tuple(event.kind for event in events)
    if kinds != REQUIRED_ORDER:
        reasons.append("REPLAY_STAGE_ORDER_INVALID")
    if len(set(kinds)) != len(kinds):
        reasons.append("DUPLICATE_REPLAY_STAGE")
    if any(
        event.event_time.tzinfo is None or event.received_time.tzinfo is None
        for event in events
    ):
        reasons.append("REPLAY_TIMESTAMP_NOT_TIMEZONE_AWARE")
    else:
        if any(event.received_time < event.event_time for event in events):
            reasons.append("RECEIVED_BEFORE_EVENT")
        if any(
            later.received_time < earlier.received_time
            for earlier, later in zip(events, events[1:])
        ):
            reasons.append("REPLAY_RECEIVE_ORDER_INVALID")
    if any(not event.artifact_id for event in events):
        reasons.append("REPLAY_ARTIFACT_MISSING")
    reason_codes = tuple(sorted(set(reasons)))
    return ReplayValidation(not reason_codes, reason_codes)


def reference_replay() -> Tuple[ReplayEvent, ...]:
    offsets = (0, 1, 2, 3, 4, 5, 6, 7, 3600)
    return tuple(
        ReplayEvent(
            kind,
            FIXTURE_AS_OF + timedelta(seconds=offset),
            FIXTURE_AS_OF + timedelta(seconds=offset),
            f"reference-{kind.value.lower()}",
        )
        for kind, offset in zip(REQUIRED_ORDER, offsets)
    )


def build_replay_evaluation() -> Dict[str, Any]:
    validation = validate_replay(reference_replay())
    return {
        "environment": "paper",
        "valid": validation.valid,
        "reason_codes": list(validation.reason_codes),
        "events": [
            {
                "kind": event.kind.value,
                "event_time": event.event_time.isoformat(),
                "received_time": event.received_time.isoformat(),
                "artifact_id": event.artifact_id,
            }
            for event in reference_replay()
        ],
    }
