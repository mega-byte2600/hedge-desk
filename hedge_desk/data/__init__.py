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
from .manifest import (
    DATASET_MANIFEST_SCHEMA_VERSION,
    DatasetManifest,
    DatasetValidationStatus,
    build_dataset_manifest,
    dataset_manifest_sha256,
    parse_dataset_manifest,
)
from .news import NewsBatchGate, NewsObservation, NewsTransport, evaluate_news_batch
from .pwb_news import (
    PWB_DAILY_NEWS_DATASET,
    PwbDailyNewsResult,
    PwbSymbolNewsFeature,
    evaluate_pwb_daily_news,
    load_pwb_daily_news,
)

__all__ = [
    "DataArtifact", "DataGateResult", "validate_data_artifact",
    "BatchManifest", "BatchStatus", "SourceBatchResult", "SourceBatchStatus",
    "build_batch_manifest",
    "validate_serialized_batch_manifest",
    "DATA_ENVELOPE_SCHEMA_VERSION", "LocalIntakeResult",
    "validate_local_observation",
    "DATA_STACK_SCHEMA_VERSION", "DataReadinessResult", "DataSubscription",
    "evaluate_options_data_stack", "parse_data_stack_manifest",
    "DATASET_MANIFEST_SCHEMA_VERSION", "DatasetManifest",
    "DatasetValidationStatus", "build_dataset_manifest",
    "dataset_manifest_sha256", "parse_dataset_manifest",
    "NewsBatchGate", "NewsObservation", "NewsTransport", "evaluate_news_batch",
    "PWB_DAILY_NEWS_DATASET", "PwbDailyNewsResult", "PwbSymbolNewsFeature",
    "evaluate_pwb_daily_news", "load_pwb_daily_news",
]
