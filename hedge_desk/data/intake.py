"""Local bring-your-own-data intake without copying payloads into the repo."""

import json
from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict, Tuple

from .contracts import DataArtifact, DataGateResult, validate_data_artifact


DATA_ENVELOPE_SCHEMA_VERSION = "hedge-desk-observation-1.0.0"
_REQUIRED_FIELDS = frozenset(
    {
        "schema_version",
        "artifact_id",
        "payload_kind",
        "source_id",
        "license_id",
        "source_as_of",
        "received_at",
        "payload_sha256",
        "synthetic",
        "redistribution_allowed",
    }
)


@dataclass(frozen=True)
class LocalIntakeResult:
    artifact: DataArtifact
    gate: DataGateResult
    payload_path: str
    payload_size_bytes: int


def _aware_datetime(value: Any, field_name: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be an ISO-8601 string")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{field_name} must be valid ISO-8601") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{field_name} must include a timezone")
    return parsed


def _load_envelope(path: Path) -> Dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError("data envelope must be readable UTF-8 JSON") from exc
    if not isinstance(value, dict):
        raise ValueError("data envelope must be a JSON object")
    missing = sorted(_REQUIRED_FIELDS - set(value))
    unknown = sorted(set(value) - _REQUIRED_FIELDS)
    if missing:
        raise ValueError("data envelope fields missing: " + ",".join(missing))
    if unknown:
        raise ValueError("data envelope fields unknown: " + ",".join(unknown))
    if value["schema_version"] != DATA_ENVELOPE_SCHEMA_VERSION:
        raise ValueError("data envelope schema version is not supported")
    for field in (
        "artifact_id",
        "payload_kind",
        "source_id",
        "license_id",
        "source_as_of",
        "received_at",
        "payload_sha256",
    ):
        if not isinstance(value[field], str):
            raise ValueError(f"{field} must be a string")
    for field in ("synthetic", "redistribution_allowed"):
        if not isinstance(value[field], bool):
            raise ValueError(f"{field} must be boolean")
    return value


def validate_local_observation(
    envelope_path: Path,
    payload_path: Path,
    decision_cutoff: datetime,
    maximum_age_seconds: int,
) -> LocalIntakeResult:
    """Hash a local payload and validate its declared point-in-time envelope."""
    if decision_cutoff.tzinfo is None:
        raise ValueError("decision cutoff must be timezone-aware")
    if type(maximum_age_seconds) is not int or maximum_age_seconds < 0:
        raise ValueError("maximum age must be a nonnegative integer")
    envelope = _load_envelope(envelope_path)
    try:
        payload = payload_path.read_bytes()
    except OSError as exc:
        raise ValueError("payload must be a readable file") from exc
    observed_hash = sha256(payload).hexdigest()
    if envelope["payload_sha256"] != observed_hash:
        raise ValueError("payload content does not match envelope SHA-256")
    artifact = DataArtifact(
        artifact_id=envelope["artifact_id"],
        payload_kind=envelope["payload_kind"],
        source_id=envelope["source_id"],
        license_id=envelope["license_id"],
        source_as_of=_aware_datetime(envelope["source_as_of"], "source_as_of"),
        received_at=_aware_datetime(envelope["received_at"], "received_at"),
        payload_sha256=observed_hash,
        synthetic=envelope["synthetic"],
        redistribution_allowed=envelope["redistribution_allowed"],
    )
    return LocalIntakeResult(
        artifact,
        validate_data_artifact(artifact, decision_cutoff, maximum_age_seconds),
        str(payload_path.resolve()),
        len(payload),
    )
