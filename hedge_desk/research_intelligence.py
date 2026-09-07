"""Deterministic scoring for external research intelligence.

This module ranks papers, repositories, datasets, APIs, and research commentary
for further review. It never authorizes trading, treats visibility as permission,
or auto-adopts third-party code. An ``INTEGRATE`` decision means eligible for
implementation review only.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Tuple


class SourceType(str, Enum):
    OFFICIAL = "official"
    PEER_REVIEWED = "peer_reviewed"
    PREPRINT = "preprint"
    REPOSITORY = "repository"
    DATASET = "dataset"
    API = "api"
    INDUSTRY_BLOG = "industry_blog"


class ResearchDecision(str, Enum):
    WATCH = "watch"
    TEST = "test"
    INTEGRATE = "integrate"
    REJECT = "reject"
    ARCHIVE = "archive"


@dataclass(frozen=True)
class ResearchSource:
    name: str
    url: str
    source_type: SourceType
    use_cases: Tuple[str, ...]
    signal_value: int
    data_value: int
    implementation_value: int
    risk_value: int
    credibility: int
    reproducible: bool
    license_status: str = "REVIEW_REQUIRED"


@dataclass(frozen=True)
class ResearchAssessment:
    score: int
    decision: ResearchDecision
    reasons: Tuple[str, ...]


def _bounded(value: int) -> int:
    if not 0 <= value <= 5:
        raise ValueError("research intelligence scores must be between 0 and 5")
    return value


def assess_source(source: ResearchSource) -> ResearchAssessment:
    """Score one source on a 100-point scale and assign a review disposition."""
    values = (
        _bounded(source.signal_value),
        _bounded(source.data_value),
        _bounded(source.implementation_value),
        _bounded(source.risk_value),
        _bounded(source.credibility),
    )
    reasons: list[str] = []

    if source.license_status in {"BLOCKED", "PROHIBITED"}:
        return ResearchAssessment(0, ResearchDecision.REJECT, ("LICENSE_BLOCK",))

    # Credibility and reproducibility receive extra weight because Emporion is a
    # research system, not a feed of interesting links.
    score = round(
        values[0] * 3.0
        + values[1] * 3.0
        + values[2] * 3.0
        + values[3] * 3.0
        + values[4] * 5.0
        + (15 if source.reproducible else 0)
    )
    score = min(score, 100)

    if source.credibility <= 1:
        reasons.append("LOW_CREDIBILITY")
        decision = ResearchDecision.REJECT
    elif score >= 80:
        reasons.append("HIGH_VALUE_REVIEW_CANDIDATE")
        decision = ResearchDecision.INTEGRATE
    elif score >= 65:
        reasons.append("TEST_BEFORE_ADOPTION")
        decision = ResearchDecision.TEST
    elif score >= 45:
        reasons.append("MONITOR_FOR_EVIDENCE")
        decision = ResearchDecision.WATCH
    else:
        reasons.append("INSUFFICIENT_CURRENT_VALUE")
        decision = ResearchDecision.ARCHIVE

    if not source.reproducible:
        reasons.append("REPRODUCIBILITY_NOT_ESTABLISHED")
    if source.license_status == "REVIEW_REQUIRED":
        reasons.append("LICENSE_REVIEW_REQUIRED")

    return ResearchAssessment(score, decision, tuple(reasons))
