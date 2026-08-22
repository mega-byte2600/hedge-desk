"""Chronological replay gate preventing look-ahead and control bypass."""

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, Mapping, Tuple

from hedge_desk.demo import (
    FIXTURE_AS_OF,
    FIXTURE_OPTION_PAYLOAD_SHA256,
    build_reference_plan,
)


class ReplayEventKind(str, Enum):
    SOURCE_PUBLISHED = "SOURCE_PUBLISHED"
    SYSTEM_RECEIVED = "SYSTEM_RECEIVED"
    VALIDATION_COMPLETE = "VALIDATION_COMPLETE"
    CANDIDATE_CREATED = "CANDIDATE_CREATED"
    RISK_COMPLETE = "RISK_COMPLETE"
    COMPLIANCE_COMPLETE = "COMPLIANCE_COMPLETE"
    HUMAN_PENDING = "HUMAN_PENDING"
    HUMAN_APPROVED = "HUMAN_APPROVED"
    PAPER_FILL = "PAPER_FILL"
    EXIT = "EXIT"


PENDING_ORDER = (
    ReplayEventKind.SOURCE_PUBLISHED,
    ReplayEventKind.SYSTEM_RECEIVED,
    ReplayEventKind.VALIDATION_COMPLETE,
    ReplayEventKind.CANDIDATE_CREATED,
    ReplayEventKind.RISK_COMPLETE,
    ReplayEventKind.COMPLIANCE_COMPLETE,
    ReplayEventKind.HUMAN_PENDING,
)
EXECUTED_ORDER = PENDING_ORDER[:-1] + (
    ReplayEventKind.HUMAN_APPROVED,
    ReplayEventKind.PAPER_FILL,
    ReplayEventKind.EXIT,
)


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
    if kinds not in (PENDING_ORDER, EXECUTED_ORDER):
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
        for kind, offset in zip(EXECUTED_ORDER, offsets)
    )


def reference_pending_replay() -> Tuple[ReplayEvent, ...]:
    plan = build_reference_plan()
    artifact_ids = (
        "synthetic-option-chain-v1",
        "synthetic-option-chain-v1",
        FIXTURE_OPTION_PAYLOAD_SHA256,
        plan.spread.spread_id,
        plan.risk_decision.risk_input_sha256,
        plan.compliance_decision.circuit_breaker_sha256,
        plan.plan_hash,
    )
    return tuple(
        ReplayEvent(
            kind,
            FIXTURE_AS_OF + timedelta(seconds=offset),
            FIXTURE_AS_OF + timedelta(seconds=offset),
            artifact_id,
        )
        for kind, offset, artifact_id in zip(
            PENDING_ORDER, range(len(PENDING_ORDER)), artifact_ids
        )
    )


def build_replay_evaluation() -> Dict[str, Any]:
    events = reference_pending_replay()
    validation = validate_replay(events)
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
            for event in events
        ],
    }


def validate_replay_evaluation(value: Mapping[str, Any]) -> Tuple[str, ...]:
    """Rebuild serialized replay events instead of trusting their valid flag."""
    if value.get("environment") != "paper":
        return ("REPLAY_ENVIRONMENT_INVALID",)
    raw_events = value.get("events")
    if not isinstance(raw_events, list):
        return ("REPLAY_EVENTS_MISSING",)
    expected_fields = {"kind", "event_time", "received_time", "artifact_id"}
    events = []
    try:
        for raw in raw_events:
            if not isinstance(raw, dict) or set(raw) != expected_fields:
                raise ValueError("event schema")
            events.append(
                ReplayEvent(
                    ReplayEventKind(str(raw["kind"])),
                    datetime.fromisoformat(str(raw["event_time"])),
                    datetime.fromisoformat(str(raw["received_time"])),
                    str(raw["artifact_id"]),
                )
            )
    except (TypeError, ValueError):
        return ("REPLAY_EVENT_SCHEMA_INVALID",)
    validation = validate_replay(tuple(events))
    reasons = list(validation.reason_codes)
    if tuple(value.get("reason_codes", ())) != validation.reason_codes:
        reasons.append("REPLAY_REASON_CODES_MISMATCH")
    if value.get("valid") is not validation.valid:
        reasons.append("REPLAY_VALIDITY_FLAG_INVALID")
    return tuple(sorted(set(reasons)))
