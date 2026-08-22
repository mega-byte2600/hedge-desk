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
from .entitlements import (
    DATA_STACK_SCHEMA_VERSION,
    DataReadinessResult,
    DataSubscription,
    evaluate_options_data_stack,
    parse_data_stack_manifest,
)
from .news import NewsBatchGate, NewsObservation, NewsTransport, evaluate_news_batch

__all__ = [
    "DataArtifact", "DataGateResult", "validate_data_artifact",
    "BatchManifest", "BatchStatus", "SourceBatchResult", "SourceBatchStatus",
    "build_batch_manifest",
    "validate_serialized_batch_manifest",
    "DATA_ENVELOPE_SCHEMA_VERSION", "LocalIntakeResult",
    "validate_local_observation",
    "DATA_STACK_SCHEMA_VERSION", "DataReadinessResult", "DataSubscription",
    "evaluate_options_data_stack", "parse_data_stack_manifest",
    "NewsBatchGate", "NewsObservation", "NewsTransport", "evaluate_news_batch",
]
