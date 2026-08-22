"""Independent Quant/AI research quorum with no control-plane authority."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Tuple

from .registry import ModelArtifact, ModelTeam, validate_open_model_artifact


class ResearchLabel(str, Enum):
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"
    ABSTAIN = "ABSTAIN"


@dataclass(frozen=True)
class ResearchVote:
    candidate_id: str
    team: ModelTeam
    model_artifact_id: str
    label: ResearchLabel
    observed_at: datetime
    evidence_sha256: str


@dataclass(frozen=True)
class ResearchQuorumResult:
    candidate_id: str
    disposition: str
    label: ResearchLabel
    reason_codes: Tuple[str, ...]
    model_artifact_ids: Tuple[str, str]
    authoritative_risk_input: bool = False
    compliance_status: str = "NOT_EVALUATED"
    human_authorization_status: str = "NOT_EVALUATED"


def evaluate_research_quorum(
    votes: Tuple[ResearchVote, ResearchVote],
    artifacts: Tuple[ModelArtifact, ModelArtifact],
) -> ResearchQuorumResult:
    """Require two reproducible independent teams; output remains research only."""
    if len(votes) != 2 or len(artifacts) != 2:
        raise ValueError("exactly two independent research teams are required")
    if {vote.team for vote in votes} != {ModelTeam.QUANT, ModelTeam.AI}:
        raise ValueError("one QUANT and one AI vote are required")
    if len({vote.candidate_id for vote in votes}) != 1:
        raise ValueError("research votes must address the same candidate")
    if any(vote.observed_at.tzinfo is None for vote in votes):
        raise ValueError("research vote timestamps must be timezone-aware")
    by_team = {artifact.team: artifact for artifact in artifacts}
    if set(by_team) != {ModelTeam.QUANT, ModelTeam.AI}:
        raise ValueError("one QUANT and one AI artifact are required")
    reasons = []
    for vote in votes:
        artifact = by_team[vote.team]
        reasons.extend(validate_open_model_artifact(artifact))
        if vote.model_artifact_id != artifact.artifact_id:
            reasons.append("MODEL_ARTIFACT_BINDING_INVALID")
        try:
            valid_evidence = len(vote.evidence_sha256) == 64 and int(vote.evidence_sha256, 16) >= 0
        except ValueError:
            valid_evidence = False
        if not valid_evidence:
            reasons.append("RESEARCH_EVIDENCE_HASH_INVALID")
        if vote.observed_at <= artifact.training_cutoff:
            reasons.append("OBSERVATION_NOT_AFTER_TRAINING_CUTOFF")

    labels = {vote.label for vote in votes}
    if ResearchLabel.ABSTAIN in labels:
        reasons.append("RESEARCH_TEAM_ABSTAINED")
    elif len(labels) != 1:
        reasons.append("RESEARCH_TEAMS_DISAGREE")
    reason_codes = tuple(sorted(set(reasons)))
    agreed_label = votes[0].label if not reason_codes else ResearchLabel.ABSTAIN
    return ResearchQuorumResult(
        votes[0].candidate_id,
        "RESEARCH_HYPOTHESIS_ONLY" if not reason_codes else "NO_TRADE",
        agreed_label,
        reason_codes,
        tuple(sorted(artifact.artifact_id for artifact in artifacts)),
    )
