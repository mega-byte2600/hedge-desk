"""Fail-closed provenance and point-in-time validation."""

from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256
from typing import Tuple


@dataclass(frozen=True)
class DataArtifact:
    artifact_id: str
    payload_kind: str
    source_id: str
    license_id: str
    source_as_of: datetime
    received_at: datetime
    payload_sha256: str
    synthetic: bool
    redistribution_allowed: bool


@dataclass(frozen=True)
class DataGateResult:
    admissible: bool
    reason_codes: Tuple[str, ...]


def sha256_text(payload: str) -> str:
    return sha256(payload.encode("utf-8")).hexdigest()


def validate_data_artifact(
    artifact: DataArtifact,
    decision_cutoff: datetime,
    maximum_age_seconds: int,
) -> DataGateResult:
    """Validate provenance without interpreting or estimating market values."""
    reasons = []
    timestamps = (artifact.source_as_of, artifact.received_at, decision_cutoff)
    if any(timestamp.tzinfo is None for timestamp in timestamps):
        reasons.append("TIMESTAMP_NOT_TIMEZONE_AWARE")
    if not artifact.artifact_id or not artifact.payload_kind or not artifact.source_id:
        reasons.append("PROVENANCE_MISSING")
    if not artifact.license_id:
        reasons.append("LICENSE_MISSING")
    if len(artifact.payload_sha256) != 64:
        reasons.append("PAYLOAD_HASH_INVALID")
    else:
        try:
            int(artifact.payload_sha256, 16)
        except ValueError:
            reasons.append("PAYLOAD_HASH_INVALID")

    if not reasons or "TIMESTAMP_NOT_TIMEZONE_AWARE" not in reasons:
        if artifact.received_at < artifact.source_as_of:
            reasons.append("RECEIVED_BEFORE_SOURCE")
        if artifact.received_at > decision_cutoff:
            reasons.append("POINT_IN_TIME_VIOLATION")
        age = (decision_cutoff - artifact.received_at).total_seconds()
        if age > maximum_age_seconds:
            reasons.append("DATA_STALE")
    reason_codes = tuple(sorted(set(reasons)))
    return DataGateResult(not reason_codes, reason_codes)
