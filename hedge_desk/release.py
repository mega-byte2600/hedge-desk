"""Deterministic paper-to-live readiness gate; no agent or human override."""

import json
from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
from typing import Any, Dict, Mapping, Tuple


RELEASE_GATE_VERSION = "live-release-gate-1.0.0"
REQUIRED_RELEASE_EVIDENCE = (
    "BROKER_ORDER_ADAPTER_CERTIFIED",
    "EXTERNAL_AUDIT_DURABILITY_VERIFIED",
    "KILL_SWITCH_AND_DR_TESTED",
    "LICENSED_POINT_IN_TIME_DATA_VERIFIED",
    "MODEL_VV_APPROVED",
    "REGULATORY_COUNSEL_SIGNOFF",
    "ROR_CONVENTIONAL_VV_APPROVED",
)


class ReleaseStatus(str, Enum):
    BLOCKED = "LIVE_RELEASE_BLOCKED"
    READY_FOR_SEPARATE_AUTHORIZATION = "READY_FOR_SEPARATE_LIVE_AUTHORIZATION"


@dataclass(frozen=True)
class ReleaseEvidence:
    requirement_id: str
    satisfied: bool
    evidence_sha256: str


@dataclass(frozen=True)
class ReleaseReadiness:
    gate_version: str
    current_environment: str
    target_environment: str
    status: ReleaseStatus
    reason_codes: Tuple[str, ...]
    evidence: Tuple[ReleaseEvidence, ...]
    human_override_allowed: bool
    live_transition_authorized: bool
    artifact_sha256: str


def _is_hash(value: str) -> bool:
    try:
        return len(value) == 64 and int(value, 16) > 0
    except ValueError:
        return False


def evaluate_live_release_readiness(
    evidence: Tuple[ReleaseEvidence, ...],
) -> ReleaseReadiness:
    if len({item.requirement_id for item in evidence}) != len(evidence):
        raise ValueError("release evidence identities must be unique")
    by_id = {item.requirement_id: item for item in evidence}
    unknown = sorted(set(by_id) - set(REQUIRED_RELEASE_EVIDENCE))
    if unknown:
        raise ValueError("unknown release evidence: " + ",".join(unknown))
    reasons = []
    for requirement_id in REQUIRED_RELEASE_EVIDENCE:
        item = by_id.get(requirement_id)
        if item is None:
            reasons.append("RELEASE_EVIDENCE_MISSING:" + requirement_id)
        elif item.satisfied and not _is_hash(item.evidence_sha256):
            reasons.append("RELEASE_EVIDENCE_HASH_INVALID:" + requirement_id)
        elif not item.satisfied:
            reasons.append("RELEASE_REQUIREMENT_UNSATISFIED:" + requirement_id)
    reason_codes = tuple(sorted(reasons))
    status = (
        ReleaseStatus.BLOCKED
        if reason_codes
        else ReleaseStatus.READY_FOR_SEPARATE_AUTHORIZATION
    )
    ordered = tuple(sorted(evidence, key=lambda item: item.requirement_id))
    payload = {
        "current_environment": "paper",
        "evidence": [
            {
                "evidence_sha256": item.evidence_sha256,
                "requirement_id": item.requirement_id,
                "satisfied": item.satisfied,
            }
            for item in ordered
        ],
        "gate_version": RELEASE_GATE_VERSION,
        "human_override_allowed": False,
        "live_transition_authorized": False,
        "reason_codes": list(reason_codes),
        "status": status.value,
        "target_environment": "live",
    }
    artifact_hash = sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return ReleaseReadiness(
        RELEASE_GATE_VERSION,
        "paper",
        "live",
        status,
        reason_codes,
        ordered,
        False,
        False,
        artifact_hash,
    )


def build_reference_release_readiness() -> ReleaseReadiness:
    return evaluate_live_release_readiness(
        tuple(
            ReleaseEvidence(requirement_id, False, "0" * 64)
            for requirement_id in REQUIRED_RELEASE_EVIDENCE
        )
    )


def validate_serialized_release_readiness(
    value: Mapping[str, Any],
) -> Tuple[str, ...]:
    try:
        evidence = tuple(
            ReleaseEvidence(
                str(item["requirement_id"]),
                item["satisfied"] is True,
                str(item["evidence_sha256"]),
            )
            for item in value["evidence"]
        )
        rebuilt = evaluate_live_release_readiness(evidence)
        expected: Dict[str, Any] = {
            "gate_version": rebuilt.gate_version,
            "current_environment": rebuilt.current_environment,
            "target_environment": rebuilt.target_environment,
            "status": rebuilt.status.value,
            "reason_codes": list(rebuilt.reason_codes),
            "evidence": [
                {
                    "requirement_id": item.requirement_id,
                    "satisfied": item.satisfied,
                    "evidence_sha256": item.evidence_sha256,
                }
                for item in rebuilt.evidence
            ],
            "human_override_allowed": rebuilt.human_override_allowed,
            "live_transition_authorized": rebuilt.live_transition_authorized,
            "artifact_sha256": rebuilt.artifact_sha256,
        }
    except (KeyError, TypeError, ValueError):
        return ("LIVE_RELEASE_SCHEMA_INVALID",)
    return () if dict(value) == expected else ("LIVE_RELEASE_ARTIFACT_INVALID",)
