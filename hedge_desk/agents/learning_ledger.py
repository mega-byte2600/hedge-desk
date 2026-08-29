"""Outcome ledger for agent self-improvement.

The pattern is borrowed from public agentic trading systems: record predictions,
score them against realized paper outcomes, attribute mistakes, and allow only
append-only improvement proposals under non-negotiable safety invariants.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Dict, Iterable, List


SAFETY_INVARIANTS = (
    "NO_LIVE_TRADING",
    "NO_AGENT_ORDER_PLACEMENT",
    "NO_RISK_OF_RUIN_OVERRIDE",
    "NO_COMPLIANCE_OVERRIDE",
    "NO_SECRET_OR_ACCOUNT_DATA_IN_PROMPTS",
    "APPEND_ONLY_AGENT_CHANGES",
)


class OutcomeGrade(str, Enum):
    CORRECT = "correct"
    PREMATURE = "premature"
    WRONG = "wrong"
    UNRESOLVED = "unresolved"


class MistakeType(str, Enum):
    NONE = "none"
    BAD_TIMING = "bad_timing"
    BAD_VOL_ASSUMPTION = "bad_vol_assumption"
    BAD_CATALYST_READ = "bad_catalyst_read"
    BAD_LIQUIDITY_FILTER = "bad_liquidity_filter"
    RULE_BLOCK_MISSED = "rule_block_missed"
    RISK_BLOCK_MISSED = "risk_block_missed"


@dataclass(frozen=True)
class AgentPrediction:
    prediction_id: str
    agent_name: str
    candidate_id: str
    expected_direction: str
    expected_premium_capture: float
    expected_max_loss: float
    thesis: str
    invalidation: str
    source_hashes: List[str]


@dataclass(frozen=True)
class PaperOutcome:
    prediction_id: str
    realized_premium_capture: float
    realized_drawdown: float
    thesis_state: str
    rule_blocks_triggered: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class LearningRecord:
    prediction: AgentPrediction
    outcome: PaperOutcome
    grade: OutcomeGrade
    mistake_type: MistakeType
    score_delta: float
    allowed_improvement: str
    safety_invariants: List[str]
    trade_authorized: bool = False


def grade_prediction(prediction: AgentPrediction, outcome: PaperOutcome) -> LearningRecord:
    """Grade one paper outcome without granting any trade authority."""
    if outcome.rule_blocks_triggered:
        grade = OutcomeGrade.WRONG
        mistake = MistakeType.RULE_BLOCK_MISSED
        score_delta = -2.0
        improvement = "Tighten pre-trade rule awareness before ranking similar candidates."
    elif outcome.realized_drawdown > prediction.expected_max_loss:
        grade = OutcomeGrade.WRONG
        mistake = MistakeType.RISK_BLOCK_MISSED
        score_delta = -2.0
        improvement = "Reduce confidence when realized drawdown exceeds planned max loss."
    elif outcome.realized_premium_capture >= prediction.expected_premium_capture:
        grade = OutcomeGrade.CORRECT
        mistake = MistakeType.NONE
        score_delta = 1.0
        improvement = "Retain setup pattern; require repeat evidence before increasing weight."
    elif outcome.thesis_state in {"intact", "strengthening"}:
        grade = OutcomeGrade.PREMATURE
        mistake = MistakeType.BAD_TIMING
        score_delta = -0.5
        improvement = "Improve trigger timing and avoid early entry without vol confirmation."
    else:
        grade = OutcomeGrade.WRONG
        mistake = MistakeType.BAD_CATALYST_READ
        score_delta = -1.0
        improvement = "Downgrade similar catalyst reads until source and reaction quality improve."

    return LearningRecord(
        prediction=prediction,
        outcome=outcome,
        grade=grade,
        mistake_type=mistake,
        score_delta=score_delta,
        allowed_improvement=improvement,
        safety_invariants=list(SAFETY_INVARIANTS),
    )


def agent_score(records: Iterable[LearningRecord]) -> Dict[str, float]:
    """Aggregate paper-learning scores by agent."""
    scores: Dict[str, float] = {}
    for record in records:
        name = record.prediction.agent_name
        scores[name] = scores.get(name, 0.0) + record.score_delta
    return scores


def records_as_dicts(records: Iterable[LearningRecord]) -> List[Dict[str, object]]:
    return [asdict(record) for record in records]
