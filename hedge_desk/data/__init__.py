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
from .eod_ingest import (
    EOD_INGEST_VERSION,
    EOD_SOURCE_ID,
    STOOQ_SOURCE_ID,
    EodDay,
    EodSymbolResult,
    ingest_eod,
)
from .providers import (
    ProviderSpec,
    all_providers,
    missing_auth_env,
    provider,
    providers_for_asset_class,
    providers_for_capability,
)
from .open_market_feeds import (
    CFTC_COT_DATASETS,
    FINRA_FIXED_INCOME_DATASETS,
    NASDAQ_ETF_SYMBOLS,
    NYFED_REFERENCE_RATES,
    TREASURY_DGS_TENORS,
    OpenFeedResult,
    bls_latest_series,
    cftc_cot,
    ecb_exchange_rates,
    eia_v2,
    fdic_failures,
    finra_fixed_income,
    nasdaq_earnings_calendar,
    nasdaq_option_chain,
    nasdaq_quote,
    nyfed_reference_rates,
    sec_companyfacts,
    sec_submissions,
    treasury_latest_auctions,
    treasury_yield_curve,
    world_bank_indicator,
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
    "EOD_INGEST_VERSION", "EOD_SOURCE_ID", "STOOQ_SOURCE_ID", "EodDay", "EodSymbolResult",
    "ingest_eod",
    "ProviderSpec", "all_providers", "missing_auth_env", "provider",
    "providers_for_asset_class", "providers_for_capability",
    "CFTC_COT_DATASETS", "FINRA_FIXED_INCOME_DATASETS", "NASDAQ_ETF_SYMBOLS",
    "NYFED_REFERENCE_RATES", "TREASURY_DGS_TENORS",
    "OpenFeedResult", "bls_latest_series", "cftc_cot", "ecb_exchange_rates",
    "eia_v2", "fdic_failures", "finra_fixed_income",
    "nasdaq_earnings_calendar", "nasdaq_option_chain", "nasdaq_quote",
    "nyfed_reference_rates", "sec_companyfacts", "sec_submissions",
    "treasury_latest_auctions", "treasury_yield_curve", "world_bank_indicator",
]
