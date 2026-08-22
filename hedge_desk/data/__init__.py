"""Validated, immutable data contracts for paper research."""

from .contracts import DataArtifact, DataGateResult, validate_data_artifact
from .batch import (
    BatchManifest,
    BatchStatus,
    SourceBatchResult,
    SourceBatchStatus,
    build_batch_manifest,
)

__all__ = [
    "DataArtifact", "DataGateResult", "validate_data_artifact",
    "BatchManifest", "BatchStatus", "SourceBatchResult", "SourceBatchStatus",
    "build_batch_manifest",
]
