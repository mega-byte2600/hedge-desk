"""Reproducible, open Quant/AI training-run governance."""

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Tuple

from .registry import ModelArtifact, ModelTeam, validate_open_model_artifact


TRAINING_RUN_SCHEMA_VERSION = "open-training-run-1.0.0"


@dataclass(frozen=True)
class TrainingRunManifest:
    run_id: str
    team: ModelTeam
    model_artifact_id: str
    code_commit: str
    environment_lock_sha256: str
    training_dataset_sha256: str
    validation_dataset_sha256: str
    test_dataset_sha256: str
    evaluation_report_sha256: str
    data_cutoff: datetime
    started_at: datetime
    completed_at: datetime
    random_seed: int
    split_method: str
    research_only: bool = True


@dataclass(frozen=True)
class TrainingRunGate:
    admissible: bool
    reason_codes: Tuple[str, ...]
    authoritative_risk_input: bool = False
    trade_authorized: bool = False


def _valid_hash(value: str) -> bool:
    try:
        return len(value) == 64 and int(value, 16) >= 0
    except ValueError:
        return False


def validate_training_run(
    run: TrainingRunManifest,
    artifact: ModelArtifact,
) -> TrainingRunGate:
    reasons = list(validate_open_model_artifact(artifact))
    if not run.run_id or not run.split_method:
        reasons.append("TRAINING_RUN_IDENTITY_MISSING")
    if run.random_seed < 0:
        reasons.append("TRAINING_SEED_INVALID")
    hashes = (
        run.environment_lock_sha256,
        run.training_dataset_sha256,
        run.validation_dataset_sha256,
        run.test_dataset_sha256,
        run.evaluation_report_sha256,
    )
    if not all(_valid_hash(value) for value in hashes):
        reasons.append("TRAINING_REPRODUCIBILITY_HASH_INVALID")
    if len(set(hashes[1:4])) != 3:
        reasons.append("TRAINING_SPLIT_HASH_COLLISION")
    timestamps = (run.data_cutoff, run.started_at, run.completed_at)
    if any(value.tzinfo is None for value in timestamps):
        reasons.append("TRAINING_TIMESTAMP_NOT_TIMEZONE_AWARE")
    else:
        if run.completed_at < run.started_at:
            reasons.append("TRAINING_INTERVAL_INVALID")
        if run.data_cutoff > run.started_at:
            reasons.append("TRAINING_DATA_LOOKAHEAD")
    if not run.research_only:
        reasons.append("TRAINING_RUN_CONTROL_AUTHORITY_FORBIDDEN")
    if run.team is not artifact.team or run.model_artifact_id != artifact.artifact_id:
        reasons.append("TRAINING_MODEL_BINDING_INVALID")
    if run.code_commit != artifact.code_commit:
        reasons.append("TRAINING_CODE_COMMIT_MISMATCH")
    if run.data_cutoff != artifact.training_cutoff:
        reasons.append("TRAINING_CUTOFF_MISMATCH")
    if run.test_dataset_sha256 != artifact.evaluation_dataset_sha256:
        reasons.append("TRAINING_TEST_DATASET_MISMATCH")
    if run.evaluation_report_sha256 != artifact.evaluation_report_sha256:
        reasons.append("TRAINING_EVALUATION_REPORT_MISMATCH")
    reason_codes = tuple(sorted(set(reasons)))
    return TrainingRunGate(not reason_codes, reason_codes, False, False)


def build_synthetic_training_gate(team: ModelTeam) -> TrainingRunGate:
    cutoff = datetime(2026, 1, 1, tzinfo=timezone.utc)
    artifact = ModelArtifact(
        f"{team.value.lower()}-synthetic-model-v1", team,
        "open-synthetic-research-model", "1.0.0",
        "https://huggingface.co/example/open-synthetic-research-model",
        "Apache-2.0", "a" * 64, "deadbeef", cutoff, "d" * 64, "e" * 64,
    )
    run = TrainingRunManifest(
        f"{team.value.lower()}-synthetic-run-v1", team, artifact.artifact_id,
        artifact.code_commit, "f" * 64, "b" * 64, "c" * 64, "d" * 64,
        "e" * 64, cutoff, cutoff + timedelta(days=1),
        cutoff + timedelta(days=2), 2600,
        "point-in-time-purged-walk-forward", True,
    )
    return validate_training_run(run, artifact)
