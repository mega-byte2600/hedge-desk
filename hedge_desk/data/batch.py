"""Deterministic completeness and lineage gate for an ingestion batch."""

import json
from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
from typing import Tuple


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


def _is_hash(value: str) -> bool:
    try:
        return len(value) == 64 and int(value, 16) >= 0
    except ValueError:
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
    if len(set(required_sources)) != len(required_sources):
        raise ValueError("required sources must be unique")
    if len({result.source_id for result in source_results}) != len(source_results):
        raise ValueError("source batch results must be unique")
    if not _is_hash(source_policy_sha256) or not _is_hash(prior_manifest_sha256):
        raise ValueError("batch policy and prior manifest hashes must be valid")

    by_source = {result.source_id: result for result in source_results}
    missing = sorted(set(required_sources) - set(by_source))
    reasons = []
    if missing:
        reasons.extend(f"REQUIRED_SOURCE_MISSING:{source}" for source in missing)
    if any(result.status is SourceBatchStatus.REJECT for result in source_results):
        status = BatchStatus.REJECTED
        reasons.append("SOURCE_REJECTED")
    elif any(result.status is SourceBatchStatus.QUARANTINE for result in source_results):
        status = BatchStatus.QUARANTINED
        reasons.append("SOURCE_QUARANTINED")
    elif missing:
        status = BatchStatus.INCOMPLETE
    elif any(not _is_hash(result.artifact_sha256) for result in source_results):
        status = BatchStatus.REJECTED
        reasons.append("SOURCE_ARTIFACT_HASH_INVALID")
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
