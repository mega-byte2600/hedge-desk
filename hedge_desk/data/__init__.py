"""Validated, immutable data contracts for paper research."""

from .contracts import DataArtifact, DataGateResult, validate_data_artifact
from .batch import (
    BatchManifest,
    BatchStatus,
    SourceBatchResult,
    SourceBatchStatus,
    build_batch_manifest,
    validate_serialized_batch_manifest,
)
from .intake import (
    DATA_ENVELOPE_SCHEMA_VERSION,
    LocalIntakeResult,
    validate_local_observation,
)

__all__ = [
    "DataArtifact", "DataGateResult", "validate_data_artifact",
    "BatchManifest", "BatchStatus", "SourceBatchResult", "SourceBatchStatus",
    "build_batch_manifest",
    "validate_serialized_batch_manifest",
    "DATA_ENVELOPE_SCHEMA_VERSION", "LocalIntakeResult",
    "validate_local_observation",
]
