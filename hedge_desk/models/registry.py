"""Reproducibility and license gates for Quant/AI research artifacts."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Tuple


class ModelTeam(str, Enum):
    QUANT = "QUANT"
    AI = "AI"


OPEN_LICENSES = frozenset(
    {"Apache-2.0", "MIT", "BSD-2-Clause", "BSD-3-Clause", "MPL-2.0"}
)


@dataclass(frozen=True)
class ModelArtifact:
    artifact_id: str
    team: ModelTeam
    model_id: str
    model_version: str
    source_repository: str
    license_spdx: str
    weights_sha256: str
    code_commit: str
    training_cutoff: datetime
    evaluation_dataset_sha256: str
    evaluation_report_sha256: str
    proprietary_runtime_required: bool = False


def _valid_sha256(value: str) -> bool:
    if len(value) != 64:
        return False
    try:
        int(value, 16)
    except ValueError:
        return False
    return True


def validate_open_model_artifact(artifact: ModelArtifact) -> Tuple[str, ...]:
    """Return stable blockers for a model that is not reproducibly open."""
    reasons = []
    if not artifact.artifact_id or not artifact.model_id or not artifact.model_version:
        reasons.append("MODEL_IDENTITY_MISSING")
    if not artifact.source_repository.startswith("https://"):
        reasons.append("PUBLIC_SOURCE_REPOSITORY_REQUIRED")
    if artifact.license_spdx not in OPEN_LICENSES:
        reasons.append("OPEN_LICENSE_REQUIRED")
    if artifact.proprietary_runtime_required:
        reasons.append("PROPRIETARY_RUNTIME_REQUIRED")
    if artifact.training_cutoff.tzinfo is None:
        reasons.append("TRAINING_CUTOFF_NOT_TIMEZONE_AWARE")
    hashes = (
        artifact.weights_sha256,
        artifact.evaluation_dataset_sha256,
        artifact.evaluation_report_sha256,
    )
    if not all(_valid_sha256(value) for value in hashes):
        reasons.append("REPRODUCIBILITY_HASH_INVALID")
    if not artifact.code_commit:
        reasons.append("CODE_COMMIT_REQUIRED")
    return tuple(sorted(set(reasons)))
