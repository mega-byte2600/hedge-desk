"""Minimal append-only, tamper-evident audit chain for paper evaluation."""

import json
from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256
from typing import Any, Dict, Mapping, Tuple

from hedge_desk.demo import build_reference_plan
from hedge_desk.replay import reference_pending_replay


AUDIT_VERSION = "audit-chain-1.1.0"
GENESIS_HASH = "0" * 64


@dataclass(frozen=True)
class AuditEvent:
    sequence: int
    run_id: str
    stage: str
    occurred_at: datetime
    artifact_id: str
    candidate_id: str
    input_sha256: str
    output_sha256: str
    component_version: str
    policy_version: str
    reason_codes: Tuple[str, ...]
    previous_hash: str
    event_hash: str


def _event_hash(
    sequence: int,
    run_id: str,
    stage: str,
    occurred_at: datetime,
    artifact_id: str,
    candidate_id: str,
    input_sha256: str,
    output_sha256: str,
    component_version: str,
    policy_version: str,
    reason_codes: Tuple[str, ...],
    previous_hash: str,
) -> str:
    payload = json.dumps(
        {
            "artifact_id": artifact_id,
            "candidate_id": candidate_id,
            "input_sha256": input_sha256,
            "output_sha256": output_sha256,
            "component_version": component_version,
            "policy_version": policy_version,
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
    candidate_id: str,
    input_sha256: str,
    output_sha256: str,
    component_version: str,
    policy_version: str,
    reason_codes: Tuple[str, ...] = (),
) -> Tuple[AuditEvent, ...]:
    if occurred_at.tzinfo is None:
        raise ValueError("audit timestamp must be timezone-aware")
    if (
        not run_id
        or not stage
        or not artifact_id
        or not candidate_id
        or not component_version
        or not policy_version
    ):
        raise ValueError("audit identity, stage, and artifact are required")
    existing_reasons = verify_audit_chain(chain)
    if existing_reasons:
        raise ValueError("cannot append to invalid audit chain")
    if chain and run_id != chain[-1].run_id:
        raise ValueError("audit run identity cannot change")
    if chain and occurred_at < chain[-1].occurred_at:
        raise ValueError("audit event time cannot move backward")
    expected_input = chain[-1].output_sha256 if chain else GENESIS_HASH
    if input_sha256 != expected_input:
        raise ValueError("audit input must equal prior output")
    if any(not isinstance(reason, str) or not reason for reason in reason_codes):
        raise ValueError("audit reason codes must be nonempty strings")
    for label, value in (("input", input_sha256), ("output", output_sha256)):
        try:
            parsed = int(value, 16)
            valid_hash = (
                isinstance(value, str)
                and len(value) == 64
                and (parsed > 0 or (label == "input" and not chain and parsed == 0))
            )
        except (TypeError, ValueError):
            valid_hash = False
        if not valid_hash:
            raise ValueError("audit input and output hashes must be valid")
    previous_hash = chain[-1].event_hash if chain else GENESIS_HASH
    sequence = len(chain) + 1
    ordered_reasons = tuple(sorted(set(reason_codes)))
    event_hash = _event_hash(
        sequence,
        run_id,
        stage,
        occurred_at,
        artifact_id,
        candidate_id,
        input_sha256,
        output_sha256,
        component_version,
        policy_version,
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
            candidate_id,
            input_sha256,
            output_sha256,
            component_version,
            policy_version,
            ordered_reasons,
            previous_hash,
            event_hash,
        ),
    )


def verify_audit_chain(chain: Tuple[AuditEvent, ...]) -> Tuple[str, ...]:
    reasons = []
    expected_previous = GENESIS_HASH
    expected_input = GENESIS_HASH
    prior_time = None
    run_ids = {event.run_id for event in chain}
    if len(run_ids) > 1:
        reasons.append("AUDIT_RUN_ID_MISMATCH")
    for expected_sequence, event in enumerate(chain, start=1):
        if event.sequence != expected_sequence:
            reasons.append("AUDIT_SEQUENCE_INVALID")
        if event.previous_hash != expected_previous:
            reasons.append("AUDIT_PREVIOUS_HASH_INVALID")
        if event.input_sha256 != expected_input:
            reasons.append("AUDIT_INPUT_LINEAGE_INVALID")
        for label, value, allow_zero in (
            ("INPUT", event.input_sha256, expected_sequence == 1),
            ("OUTPUT", event.output_sha256, False),
            ("PREVIOUS", event.previous_hash, expected_sequence == 1),
            ("EVENT", event.event_hash, False),
        ):
            try:
                parsed = int(value, 16)
                valid_hash = (
                    isinstance(value, str)
                    and len(value) == 64
                    and (parsed > 0 or (allow_zero and parsed == 0))
                )
            except (TypeError, ValueError):
                valid_hash = False
            if not valid_hash:
                reasons.append(f"AUDIT_{label}_HASH_INVALID")
        if event.occurred_at.tzinfo is None:
            reasons.append("AUDIT_TIMESTAMP_NOT_TIMEZONE_AWARE")
        elif prior_time is not None and event.occurred_at < prior_time:
            reasons.append("AUDIT_TIME_ORDER_INVALID")
        if event.reason_codes != tuple(sorted(set(event.reason_codes))):
            reasons.append("AUDIT_REASON_CODES_NONCANONICAL")
        if (
            not event.run_id
            or not event.stage
            or not event.artifact_id
            or not event.candidate_id
            or not event.component_version
            or not event.policy_version
        ):
            reasons.append("AUDIT_METADATA_INCOMPLETE")
        expected_hash = _event_hash(
            event.sequence,
            event.run_id,
            event.stage,
            event.occurred_at,
            event.artifact_id,
            event.candidate_id,
            event.input_sha256,
            event.output_sha256,
            event.component_version,
            event.policy_version,
            event.reason_codes,
            event.previous_hash,
        )
        if event.event_hash != expected_hash:
            reasons.append("AUDIT_EVENT_HASH_INVALID")
        expected_previous = event.event_hash
        expected_input = event.output_sha256
        prior_time = event.occurred_at if event.occurred_at.tzinfo is not None else prior_time
    return tuple(sorted(set(reasons)))


def build_reference_audit() -> Tuple[AuditEvent, ...]:
    chain: Tuple[AuditEvent, ...] = ()
    plan = build_reference_plan()
    component_versions = (
        "source-fixture-1.0.0",
        "intake-1.0.0",
        "data-contract-1.0.0",
        "vertical-credit-spread-1.0.0",
        plan.risk_decision.risk_model_version,
        plan.compliance_decision.policy_decision.policy_version,
        "human-authorization-1.0.0",
    )
    policy_versions = (
        "paper-source-policy-1.0.0",
        "paper-source-policy-1.0.0",
        "paper-source-policy-1.0.0",
        "paper-options-1.0.0",
        "paper-risk-1.0.0",
        plan.compliance_decision.policy_decision.policy_version,
        "paper-human-checkpoint-1.0.0",
    )
    prior_output = GENESIS_HASH
    for event, component_version, policy_version in zip(
        reference_pending_replay(), component_versions, policy_versions
    ):
        if event.kind.value == "CANDIDATE_CREATED":
            from hedge_desk.yellow_sheet import append_yellow_sheet_audit_event

            chain = append_yellow_sheet_audit_event(
                chain, plan.yellow_sheet, "reference-overnight-run"
            )
            prior_output = plan.yellow_sheet.artifact_sha256
        try:
            output_hash = (
                event.artifact_id
                if len(event.artifact_id) == 64 and int(event.artifact_id, 16) >= 0
                else sha256(event.artifact_id.encode("utf-8")).hexdigest()
            )
        except ValueError:
            output_hash = sha256(event.artifact_id.encode("utf-8")).hexdigest()
        chain = append_audit_event(
            chain,
            "reference-overnight-run",
            event.kind.value,
            event.received_time,
            event.artifact_id,
            plan.risk_decision.candidate_id,
            prior_output,
            output_hash,
            component_version,
            policy_version,
        )
        prior_output = output_hash
    return chain


def build_audit_evaluation() -> Dict[str, Any]:
    chain = build_reference_audit()
    reasons = verify_audit_chain(chain)
    return {
        "version": AUDIT_VERSION,
        "valid": not reasons,
        "reason_codes": list(reasons),
        "event_count": len(chain),
        "complete_lineage": not reasons and all(
            event.candidate_id
            and event.input_sha256
            and event.output_sha256
            and event.component_version
            and event.policy_version
            for event in chain
        ),
        "head_hash": chain[-1].event_hash if chain else GENESIS_HASH,
        "events": [
            {
                "sequence": event.sequence,
                "run_id": event.run_id,
                "stage": event.stage,
                "occurred_at": event.occurred_at.isoformat(),
                "artifact_id": event.artifact_id,
                "candidate_id": event.candidate_id,
                "input_sha256": event.input_sha256,
                "output_sha256": event.output_sha256,
                "component_version": event.component_version,
                "policy_version": event.policy_version,
                "reason_codes": list(event.reason_codes),
                "previous_hash": event.previous_hash,
                "event_hash": event.event_hash,
            }
            for event in chain
        ],
    }


def validate_audit_evaluation(value: Mapping[str, Any]) -> Tuple[str, ...]:
    """Reconstruct and independently verify a serialized audit evaluation."""
    reasons = []
    raw_events = value.get("events")
    if not isinstance(raw_events, list):
        return ("AUDIT_EVENTS_MISSING",)
    expected_fields = {
        "sequence", "run_id", "stage", "occurred_at", "artifact_id",
        "candidate_id", "input_sha256", "output_sha256", "component_version",
        "policy_version", "reason_codes", "previous_hash", "event_hash",
    }
    events = []
    try:
        for raw in raw_events:
            if not isinstance(raw, dict) or set(raw) != expected_fields:
                raise ValueError("event schema")
            if not isinstance(raw["reason_codes"], list):
                raise ValueError("reason schema")
            events.append(
                AuditEvent(
                    int(raw["sequence"]),
                    str(raw["run_id"]),
                    str(raw["stage"]),
                    datetime.fromisoformat(str(raw["occurred_at"])),
                    str(raw["artifact_id"]),
                    str(raw["candidate_id"]),
                    str(raw["input_sha256"]),
                    str(raw["output_sha256"]),
                    str(raw["component_version"]),
                    str(raw["policy_version"]),
                    tuple(str(item) for item in raw["reason_codes"]),
                    str(raw["previous_hash"]),
                    str(raw["event_hash"]),
                )
            )
    except (TypeError, ValueError):
        return ("AUDIT_EVENT_SCHEMA_INVALID",)
    chain = tuple(events)
    reasons.extend(verify_audit_chain(chain))
    if value.get("version") != AUDIT_VERSION:
        reasons.append("AUDIT_VERSION_INVALID")
    if value.get("event_count") != len(chain):
        reasons.append("AUDIT_EVENT_COUNT_INVALID")
    expected_head = chain[-1].event_hash if chain else GENESIS_HASH
    if value.get("head_hash") != expected_head:
        reasons.append("AUDIT_HEAD_HASH_INVALID")
    if value.get("valid") is not (not reasons):
        reasons.append("AUDIT_VALIDITY_FLAG_INVALID")
    complete = not reasons and all(
        event.candidate_id
        and event.input_sha256
        and event.output_sha256
        and event.component_version
        and event.policy_version
        for event in chain
    )
    if value.get("complete_lineage") is not complete:
        reasons.append("AUDIT_COMPLETENESS_FLAG_INVALID")
    return tuple(sorted(set(reasons)))
