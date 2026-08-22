"""Leakage-resistant, content-addressed model evaluation split controls."""

import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from typing import Tuple


SPLIT_GATE_VERSION = "purged-walk-forward-split-1.0.0"


@dataclass(frozen=True)
class EvaluationWindow:
    split_id: str
    started_at: datetime
    ended_at: datetime
    observation_count: int
    dataset_sha256: str


@dataclass(frozen=True)
class EvaluationSplitGate:
    admissible: bool
    reason_codes: Tuple[str, ...]
    artifact_sha256: str
    authoritative_risk_input: bool = False
    trade_authorized: bool = False


def _valid_hash(value: str) -> bool:
    try:
        return len(value) == 64 and int(value, 16) > 0
    except (TypeError, ValueError):
        return False


def evaluate_purged_walk_forward_split(
    train: EvaluationWindow,
    validation: EvaluationWindow,
    test: EvaluationWindow,
    embargo: timedelta,
    evaluated_at: datetime,
    minimum_observations_per_split: int = 100,
) -> EvaluationSplitGate:
    if evaluated_at.tzinfo is None:
        raise ValueError("split evaluation timestamp must be timezone-aware")
    if embargo < timedelta(0):
        raise ValueError("split embargo cannot be negative")
    if type(minimum_observations_per_split) is not int or minimum_observations_per_split <= 0:
        raise ValueError("minimum split observations must be a positive integer")
    windows = (train, validation, test)
    reasons = []
    if tuple(item.split_id for item in windows) != ("train", "validation", "test"):
        reasons.append("MODEL_SPLIT_IDENTITIES_INVALID")
    if any(item.started_at.tzinfo is None or item.ended_at.tzinfo is None for item in windows):
        reasons.append("MODEL_SPLIT_TIMESTAMP_INVALID")
    else:
        if any(item.ended_at <= item.started_at for item in windows):
            reasons.append("MODEL_SPLIT_INTERVAL_INVALID")
        if train.ended_at + embargo > validation.started_at:
            reasons.append("TRAIN_VALIDATION_PURGE_VIOLATION")
        if validation.ended_at + embargo > test.started_at:
            reasons.append("VALIDATION_TEST_PURGE_VIOLATION")
        if test.ended_at > evaluated_at:
            reasons.append("MODEL_SPLIT_POINT_IN_TIME_VIOLATION")
    if any(
        type(item.observation_count) is not int
        or item.observation_count < minimum_observations_per_split
        for item in windows
    ):
        reasons.append("MODEL_SPLIT_SAMPLE_INSUFFICIENT")
    hashes = tuple(item.dataset_sha256 for item in windows)
    if not all(_valid_hash(value) for value in hashes):
        reasons.append("MODEL_SPLIT_HASH_INVALID")
    elif len(set(hashes)) != 3:
        reasons.append("MODEL_SPLIT_HASH_COLLISION")
    reason_codes = tuple(sorted(set(reasons)))
    payload = {
        "embargo_seconds": int(embargo.total_seconds()),
        "evaluated_at": evaluated_at.isoformat(),
        "minimum_observations_per_split": minimum_observations_per_split,
        "reason_codes": list(reason_codes),
        "version": SPLIT_GATE_VERSION,
        "windows": [
            {
                "dataset_sha256": item.dataset_sha256,
                "ended_at": item.ended_at.isoformat(),
                "observation_count": item.observation_count,
                "split_id": item.split_id,
                "started_at": item.started_at.isoformat(),
            }
            for item in windows
        ],
    }
    artifact_sha256 = sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return EvaluationSplitGate(
        not reason_codes, reason_codes, artifact_sha256, False, False
    )


def build_synthetic_split_gate(evaluated_at: datetime) -> EvaluationSplitGate:
    """Build the frozen research split used by the overnight model-lab demo."""
    utc = timezone.utc
    windows = (
        EvaluationWindow(
            "train", datetime(2020, 1, 1, tzinfo=utc),
            datetime(2023, 12, 31, tzinfo=utc), 1000, "a" * 64,
        ),
        EvaluationWindow(
            "validation", datetime(2024, 1, 8, tzinfo=utc),
            datetime(2024, 12, 31, tzinfo=utc), 250, "b" * 64,
        ),
        EvaluationWindow(
            "test", datetime(2025, 1, 8, tzinfo=utc),
            datetime(2025, 12, 31, tzinfo=utc), 250, "c" * 64,
        ),
    )
    return evaluate_purged_walk_forward_split(
        *windows, timedelta(days=7), evaluated_at
    )
