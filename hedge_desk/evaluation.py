"""Common labeled evaluation records for all Hedge Desk MVPs."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Mapping, Tuple


class EvaluationLayer(str, Enum):
    OBSERVED = "OBSERVED"
    STAT = "STAT"
    BIG = "BIG"
    DETERMINISTIC_RISK = "DETERMINISTIC_RISK"
    HUMAN = "HUMAN"


class EvaluationStatus(str, Enum):
    PASS = "PASS"
    BLOCKED = "BLOCKED"
    NOT_REQUIRED = "NOT_REQUIRED"
    NOT_IMPLEMENTED = "NOT_IMPLEMENTED"
    PENDING = "PENDING"


class Disposition(str, Enum):
    HUMAN_REVIEW = "HUMAN_REVIEW"
    NO_TRADE = "NO_TRADE"


@dataclass(frozen=True)
class LayerEvaluation:
    layer: EvaluationLayer
    status: EvaluationStatus
    reason_codes: Tuple[str, ...]
    metrics: Mapping[str, str]
    artifact_refs: Tuple[str, ...] = ()


@dataclass(frozen=True)
class ProjectEvaluation:
    project_id: str
    evaluated_at: datetime
    disposition: Disposition
    layers: Tuple[LayerEvaluation, ...]

    def __post_init__(self) -> None:
        expected = tuple(EvaluationLayer)
        actual = tuple(evaluation.layer for evaluation in self.layers)
        if actual != expected:
            raise ValueError("evaluation layers must be complete and ordered")
