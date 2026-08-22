"""Content-addressed quantitative inputs for the conventional risk engine."""

import json
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from hashlib import sha256


@dataclass(frozen=True)
class ValidatedRiskInputs:
    candidate_id: str
    maximum_loss: Decimal
    expected_win: Decimal
    win_probability: Decimal
    as_of: datetime
    source_artifact_sha256: str
    portfolio_snapshot_sha256: str
    risk_of_ruin_before: Decimal
    risk_of_ruin_after: Decimal
    risk_model_id: str
    risk_model_version: str
    validator_id: str
    validator_version: str
    environment: str
    artifact_sha256: str


def _valid_hash(value: str) -> bool:
    try:
        return len(value) == 64 and int(value, 16) >= 0
    except ValueError:
        return False


def _payload(
    candidate_id: str,
    maximum_loss: Decimal,
    expected_win: Decimal,
    win_probability: Decimal,
    as_of: datetime,
    source_artifact_sha256: str,
    portfolio_snapshot_sha256: str,
    risk_of_ruin_before: Decimal,
    risk_of_ruin_after: Decimal,
    risk_model_id: str,
    risk_model_version: str,
    validator_id: str,
    validator_version: str,
    environment: str,
) -> dict:
    return {
        "as_of": as_of.isoformat(),
        "candidate_id": candidate_id,
        "environment": environment,
        "expected_win": str(expected_win),
        "maximum_loss": str(maximum_loss),
        "source_artifact_sha256": source_artifact_sha256,
        "portfolio_snapshot_sha256": portfolio_snapshot_sha256,
        "risk_of_ruin_before": str(risk_of_ruin_before),
        "risk_of_ruin_after": str(risk_of_ruin_after),
        "risk_model_id": risk_model_id,
        "risk_model_version": risk_model_version,
        "validator_id": validator_id,
        "validator_version": validator_version,
        "win_probability": str(win_probability),
    }


def build_validated_risk_inputs(
    candidate_id: str,
    maximum_loss: Decimal,
    expected_win: Decimal,
    win_probability: Decimal,
    as_of: datetime,
    source_artifact_sha256: str,
    portfolio_snapshot_sha256: str,
    risk_of_ruin_before: Decimal,
    risk_of_ruin_after: Decimal,
    risk_model_id: str,
    risk_model_version: str,
    validator_id: str,
    validator_version: str,
    environment: str = "paper",
) -> ValidatedRiskInputs:
    if (
        not candidate_id
        or not validator_id
        or not validator_version
        or not risk_model_id
        or not risk_model_version
    ):
        raise ValueError("risk input and validator identities are required")
    if as_of.tzinfo is None:
        raise ValueError("risk input timestamp must be timezone-aware")
    if maximum_loss < 0 or expected_win < 0:
        raise ValueError("risk payoff inputs cannot be negative")
    if not Decimal("0") <= win_probability <= Decimal("1"):
        raise ValueError("risk probability must be between zero and one")
    if not _valid_hash(source_artifact_sha256) or not _valid_hash(
        portfolio_snapshot_sha256
    ):
        raise ValueError("validated source and portfolio snapshot hashes are required")
    if not (
        Decimal("0") <= risk_of_ruin_before <= Decimal("1")
        and Decimal("0") <= risk_of_ruin_after <= Decimal("1")
    ):
        raise ValueError("portfolio risk of ruin values must be between zero and one")
    if environment != "paper":
        raise ValueError("only paper risk inputs are accepted")
    payload = _payload(
        candidate_id, maximum_loss, expected_win, win_probability, as_of,
        source_artifact_sha256, portfolio_snapshot_sha256, risk_of_ruin_before,
        risk_of_ruin_after, risk_model_id, risk_model_version,
        validator_id, validator_version, environment,
    )
    artifact_hash = sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return ValidatedRiskInputs(
        candidate_id, maximum_loss, expected_win, win_probability, as_of,
        source_artifact_sha256, portfolio_snapshot_sha256, risk_of_ruin_before,
        risk_of_ruin_after, risk_model_id, risk_model_version,
        validator_id, validator_version, environment,
        artifact_hash,
    )


def validate_risk_inputs(inputs: ValidatedRiskInputs) -> None:
    rebuilt = build_validated_risk_inputs(
        inputs.candidate_id,
        inputs.maximum_loss,
        inputs.expected_win,
        inputs.win_probability,
        inputs.as_of,
        inputs.source_artifact_sha256,
        inputs.portfolio_snapshot_sha256,
        inputs.risk_of_ruin_before,
        inputs.risk_of_ruin_after,
        inputs.risk_model_id,
        inputs.risk_model_version,
        inputs.validator_id,
        inputs.validator_version,
        inputs.environment,
    )
    if rebuilt.artifact_sha256 != inputs.artifact_sha256:
        raise ValueError("risk input artifact integrity check failed")
