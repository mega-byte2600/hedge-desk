"""Minimal append-only, tamper-evident audit chain for paper evaluation."""

import json
from dataclasses import dataclass, replace
from datetime import datetime
from hashlib import sha256
from typing import Any, Dict, Optional, Tuple

from hedge_desk.replay import reference_pending_replay


AUDIT_VERSION = "audit-chain-1.0.0"
GENESIS_HASH = "0" * 64


@dataclass(frozen=True)
class AuditEvent:
    sequence: int
    run_id: str
    stage: str
    occurred_at: datetime
    artifact_id: str
    component_version: str
    reason_codes: Tuple[str, ...]
    previous_hash: str
    event_hash: str


def _event_hash(
    sequence: int,
    run_id: str,
    stage: str,
    occurred_at: datetime,
    artifact_id: str,
    component_version: str,
    reason_codes: Tuple[str, ...],
    previous_hash: str,
) -> str:
    payload = json.dumps(
        {
            "artifact_id": artifact_id,
            "component_version": component_version,
            "occurred_at": occurred_at.isoformat(),
            "previous_hash": previous_hash,
            "reason_codes": list(reason_codes),
            "run_id": run_id,
            "sequence": sequence,
            "stage": stage,
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    return sha256(payload.encode("utf-8")).hexdigest()


def append_audit_event(
    chain: Tuple[AuditEvent, ...],
    run_id: str,
    stage: str,
    occurred_at: datetime,
    artifact_id: str,
    reason_codes: Tuple[str, ...] = (),
) -> Tuple[AuditEvent, ...]:
    if occurred_at.tzinfo is None:
        raise ValueError("audit timestamp must be timezone-aware")
    if not run_id or not stage or not artifact_id:
        raise ValueError("audit identity, stage, and artifact are required")
    previous_hash = chain[-1].event_hash if chain else GENESIS_HASH
    sequence = len(chain) + 1
    ordered_reasons = tuple(sorted(set(reason_codes)))
    event_hash = _event_hash(
        sequence,
        run_id,
        stage,
        occurred_at,
        artifact_id,
        AUDIT_VERSION,
        ordered_reasons,
        previous_hash,
    )
    return chain + (
        AuditEvent(
            sequence,
            run_id,
            stage,
            occurred_at,
            artifact_id,
            AUDIT_VERSION,
            ordered_reasons,
            previous_hash,
            event_hash,
        ),
    )


def verify_audit_chain(chain: Tuple[AuditEvent, ...]) -> Tuple[str, ...]:
    reasons = []
    expected_previous = GENESIS_HASH
    run_ids = {event.run_id for event in chain}
    if len(run_ids) > 1:
        reasons.append("AUDIT_RUN_ID_MISMATCH")
    for expected_sequence, event in enumerate(chain, start=1):
        if event.sequence != expected_sequence:
            reasons.append("AUDIT_SEQUENCE_INVALID")
        if event.previous_hash != expected_previous:
            reasons.append("AUDIT_PREVIOUS_HASH_INVALID")
        expected_hash = _event_hash(
            event.sequence,
            event.run_id,
            event.stage,
            event.occurred_at,
            event.artifact_id,
            event.component_version,
            event.reason_codes,
            event.previous_hash,
        )
        if event.event_hash != expected_hash:
            reasons.append("AUDIT_EVENT_HASH_INVALID")
        expected_previous = event.event_hash
    return tuple(sorted(set(reasons)))


def build_reference_audit() -> Tuple[AuditEvent, ...]:
    chain: Tuple[AuditEvent, ...] = ()
    for event in reference_pending_replay():
        chain = append_audit_event(
            chain,
            "reference-overnight-run",
            event.kind.value,
            event.received_time,
            event.artifact_id,
        )
    return chain


def build_audit_evaluation() -> Dict[str, Any]:
    chain = build_reference_audit()
    reasons = verify_audit_chain(chain)
    return {
        "version": AUDIT_VERSION,
        "valid": not reasons,
        "reason_codes": list(reasons),
        "event_count": len(chain),
        "head_hash": chain[-1].event_hash if chain else GENESIS_HASH,
    }
