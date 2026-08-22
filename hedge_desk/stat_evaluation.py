"""Deterministic calibration metrics with explicit inference sufficiency gates."""

from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Dict, Optional, Tuple


STAT_EVALUATOR_VERSION = "calibration-evaluator-1.0.0"


@dataclass(frozen=True)
class ForecastObservation:
    observation_id: str
    predicted_probability: Decimal
    outcome: bool

    def __post_init__(self) -> None:
        if not self.observation_id:
            raise ValueError("forecast observation identity is required")
        if (
            not isinstance(self.predicted_probability, Decimal)
            or not self.predicted_probability.is_finite()
        ):
            raise ValueError("predicted probability must be a finite Decimal")
        if not Decimal("0") <= self.predicted_probability <= Decimal("1"):
            raise ValueError("predicted probability must be between zero and one")
        if type(self.outcome) is not bool:
            raise ValueError("forecast outcome must be boolean")


@dataclass(frozen=True)
class InferencePolicy:
    alpha: Decimal = Decimal("0.005")
    confidence_level: Decimal = Decimal("0.95")
    minimum_sample_size: int = 100

    def __post_init__(self) -> None:
        if any(
            not isinstance(value, Decimal) or not value.is_finite()
            for value in (self.alpha, self.confidence_level)
        ):
            raise ValueError("inference policy probabilities must be finite Decimals")
        if not Decimal("0") < self.alpha < Decimal("1"):
            raise ValueError("significance alpha must be between zero and one")
        if not Decimal("0") < self.confidence_level < Decimal("1"):
            raise ValueError("confidence level must be between zero and one")
        if type(self.minimum_sample_size) is not int or self.minimum_sample_size <= 0:
            raise ValueError("minimum sample size must be a positive integer")


@dataclass(frozen=True)
class CalibrationEvaluation:
    evaluator_version: str
    sample_size: int
    brier_score: Decimal
    mean_predicted_probability: Decimal
    observed_event_rate: Decimal
    alpha: Decimal
    confidence_level: Decimal
    confidence_interval_alpha: Decimal
    inference_status: str
    p_value: Optional[Decimal]
    confidence_interval: Optional[Tuple[Decimal, Decimal]]


def evaluate_calibration(
    observations: Tuple[ForecastObservation, ...],
    policy: InferencePolicy = InferencePolicy(),
) -> CalibrationEvaluation:
    if not observations:
        raise ValueError("calibration requires observations")
    if len({item.observation_id for item in observations}) != len(observations):
        raise ValueError("forecast observation identities must be unique")
    count = Decimal(len(observations))
    probabilities = tuple(item.predicted_probability for item in observations)
    outcomes = tuple(Decimal(1 if item.outcome else 0) for item in observations)
    brier = sum(
        ((probability - outcome) ** 2 for probability, outcome in zip(probabilities, outcomes)),
        Decimal("0"),
    ) / count
    sufficient = len(observations) >= policy.minimum_sample_size
    # Inferential statistics require a separately validated method and adequate
    # sample. This evaluator deliberately emits no invented p-value or interval.
    return CalibrationEvaluation(
        STAT_EVALUATOR_VERSION,
        len(observations),
        brier,
        sum(probabilities, Decimal("0")) / count,
        sum(outcomes, Decimal("0")) / count,
        policy.alpha,
        policy.confidence_level,
        Decimal("1") - policy.confidence_level,
        "METHOD_VALIDATION_REQUIRED" if sufficient else "INSUFFICIENT_SAMPLE",
        None,
        None,
    )


REFERENCE_FORECASTS: Tuple[ForecastObservation, ...] = (
    ForecastObservation("f1", Decimal("0.8"), True),
    ForecastObservation("f2", Decimal("0.7"), True),
    ForecastObservation("f3", Decimal("0.6"), False),
    ForecastObservation("f4", Decimal("0.4"), False),
    ForecastObservation("f5", Decimal("0.3"), False),
    ForecastObservation("f6", Decimal("0.2"), True),
)


def build_stat_evaluation() -> Dict[str, Any]:
    evaluation = evaluate_calibration(REFERENCE_FORECASTS)
    return {
        "label": "STAT",
        "evaluator_version": evaluation.evaluator_version,
        "sample_size": evaluation.sample_size,
        "brier_score": str(evaluation.brier_score),
        "mean_predicted_probability": str(evaluation.mean_predicted_probability),
        "observed_event_rate": str(evaluation.observed_event_rate),
        "alpha": str(evaluation.alpha),
        "confidence_level": str(evaluation.confidence_level),
        "confidence_interval_alpha": str(evaluation.confidence_interval_alpha),
        "alpha_semantics": "hypothesis_test_significance_threshold",
        "confidence_level_semantics": "separate_interval_coverage_target",
        "inference_status": evaluation.inference_status,
        "p_value": None,
        "confidence_interval": None,
        "source": "synthetic_fixture",
    }
