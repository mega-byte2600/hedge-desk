"""Deterministic completeness and lineage gate for an ingestion batch."""

import json
from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
from typing import Any, Mapping, Tuple


class SourceBatchStatus(str, Enum):
    PASS = "PASS"
    QUARANTINE = "QUARANTINE"
    REJECT = "REJECT"


class BatchStatus(str, Enum):
    READY_FOR_RESEARCH = "READY_FOR_RESEARCH"
    INCOMPLETE = "INCOMPLETE"
    QUARANTINED = "QUARANTINED"
    REJECTED = "REJECTED"


@dataclass(frozen=True)
class SourceBatchResult:
    source_id: str
    status: SourceBatchStatus
    artifact_sha256: str
    reason_codes: Tuple[str, ...] = ()


@dataclass(frozen=True)
class BatchManifest:
    batch_id: str
    status: BatchStatus
    required_sources: Tuple[str, ...]
    source_results: Tuple[SourceBatchResult, ...]
    source_policy_sha256: str
    prior_manifest_sha256: str
    reason_codes: Tuple[str, ...]
    manifest_sha256: str


def _is_hash(value: str, allow_zero: bool = False) -> bool:
    try:
        parsed = int(value, 16)
        return (
            isinstance(value, str)
            and len(value) == 64
            and (parsed > 0 or (allow_zero and parsed == 0))
        )
    except (TypeError, ValueError):
        return False


def build_batch_manifest(
    batch_id: str,
    required_sources: Tuple[str, ...],
    source_results: Tuple[SourceBatchResult, ...],
    source_policy_sha256: str,
    prior_manifest_sha256: str = "0" * 64,
) -> BatchManifest:
    if not batch_id or not required_sources:
        raise ValueError("batch identity and required sources are required")
    if (
        any(not isinstance(item, str) or not item for item in required_sources)
        or len(set(required_sources)) != len(required_sources)
    ):
        raise ValueError("required sources must be unique and nonempty")
    result_ids = [result.source_id for result in source_results]
    if (
        any(not isinstance(item, str) or not item for item in result_ids)
        or len(set(result_ids)) != len(source_results)
    ):
        raise ValueError("source batch results must be unique and nonempty")
    if not _is_hash(source_policy_sha256) or not _is_hash(
        prior_manifest_sha256, allow_zero=True
    ):
        raise ValueError("batch policy and prior manifest hashes must be valid")

    by_source = {result.source_id: result for result in source_results}
    missing = sorted(set(required_sources) - set(by_source))
    unexpected = sorted(set(by_source) - set(required_sources))
    reasons = []
    if missing:
        reasons.extend(f"REQUIRED_SOURCE_MISSING:{source}" for source in missing)
    if unexpected:
        reasons.extend(f"UNEXPECTED_SOURCE:{source}" for source in unexpected)
    invalid_hash = any(
        not _is_hash(result.artifact_sha256) for result in source_results
    )
    pass_with_reasons = any(
        result.status is SourceBatchStatus.PASS and result.reason_codes
        for result in source_results
    )
    noncanonical_reasons = any(
        result.reason_codes != tuple(sorted(set(result.reason_codes)))
        for result in source_results
    )
    if invalid_hash:
        status = BatchStatus.REJECTED
        reasons.append("SOURCE_ARTIFACT_HASH_INVALID")
    elif pass_with_reasons or noncanonical_reasons or unexpected:
        status = BatchStatus.REJECTED
        if pass_with_reasons:
            reasons.append("SOURCE_PASS_HAS_REASONS")
        if noncanonical_reasons:
            reasons.append("SOURCE_REASON_CODES_NONCANONICAL")
    elif any(result.status is SourceBatchStatus.REJECT for result in source_results):
        status = BatchStatus.REJECTED
        reasons.append("SOURCE_REJECTED")
    elif any(result.status is SourceBatchStatus.QUARANTINE for result in source_results):
        status = BatchStatus.QUARANTINED
        reasons.append("SOURCE_QUARANTINED")
    elif missing:
        status = BatchStatus.INCOMPLETE
    else:
        status = BatchStatus.READY_FOR_RESEARCH

    ordered_results = tuple(sorted(source_results, key=lambda item: item.source_id))
    ordered_reasons = tuple(sorted(set(reasons)))
    payload = {
        "batch_id": batch_id,
        "prior_manifest_sha256": prior_manifest_sha256,
        "reason_codes": list(ordered_reasons),
        "required_sources": sorted(required_sources),
        "source_policy_sha256": source_policy_sha256,
        "source_results": [
            {
                "artifact_sha256": result.artifact_sha256,
                "reason_codes": sorted(result.reason_codes),
                "source_id": result.source_id,
                "status": result.status.value,
            }
            for result in ordered_results
        ],
        "status": status.value,
    }
    manifest_hash = sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return BatchManifest(
        batch_id,
        status,
        tuple(sorted(required_sources)),
        ordered_results,
        source_policy_sha256,
        prior_manifest_sha256,
        ordered_reasons,
        manifest_hash,
    )


def validate_serialized_batch_manifest(value: Mapping[str, Any]) -> Tuple[str, ...]:
    """Rebuild a serialized batch so a claimed READY flag is never trusted."""
    expected_fields = {
        "batch_id", "status", "required_sources", "source_results",
        "source_policy_sha256", "prior_manifest_sha256", "reason_codes",
        "manifest_sha256",
    }
    if set(value) != expected_fields:
        return ("BATCH_SCHEMA_INVALID",)
    try:
        required = tuple(str(item) for item in value["required_sources"])
        source_results = tuple(
            SourceBatchResult(
                str(item["source_id"]),
                SourceBatchStatus(str(item["status"])),
                str(item["artifact_sha256"]),
                tuple(str(reason) for reason in item["reason_codes"]),
            )
            for item in value["source_results"]
        )
        rebuilt = build_batch_manifest(
            str(value["batch_id"]),
            required,
            source_results,
            str(value["source_policy_sha256"]),
            str(value["prior_manifest_sha256"]),
        )
    except (KeyError, TypeError, ValueError):
        return ("BATCH_SCHEMA_INVALID",)
    reasons = []
    if value["status"] != rebuilt.status.value:
        reasons.append("BATCH_STATUS_MISMATCH")
    if tuple(value["required_sources"]) != rebuilt.required_sources:
        reasons.append("BATCH_REQUIRED_SOURCES_NONCANONICAL")
    if tuple(value["reason_codes"]) != rebuilt.reason_codes:
        reasons.append("BATCH_REASON_CODES_MISMATCH")
    if value["manifest_sha256"] != rebuilt.manifest_sha256:
        reasons.append("BATCH_MANIFEST_HASH_MISMATCH")
    serialized_results = tuple(
        (
            item["source_id"], item["status"], item["artifact_sha256"],
            tuple(item["reason_codes"]),
        )
        for item in value["source_results"]
    )
    rebuilt_results = tuple(
        (
            item.source_id, item.status.value, item.artifact_sha256,
            item.reason_codes,
        )
        for item in rebuilt.source_results
    )
    if serialized_results != rebuilt_results:
        reasons.append("BATCH_SOURCE_RESULTS_NONCANONICAL")
    return tuple(sorted(set(reasons)))
