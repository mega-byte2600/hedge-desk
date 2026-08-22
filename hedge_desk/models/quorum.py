"""Independent Quant/AI research quorum with no control-plane authority."""

from dataclasses import dataclass
from datetime import datetime, timezone
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


def build_synthetic_reference_quorum(observed_at: datetime) -> ResearchQuorumResult:
    """Build a frozen open-artifact governance fixture, not a market prediction."""
    if observed_at.tzinfo is None:
        raise ValueError("reference observation must be timezone-aware")
    cutoff = datetime(2026, 1, 1, tzinfo=timezone.utc)
    artifacts = tuple(
        ModelArtifact(
            f"{team.value.lower()}-synthetic-model-v1",
            team,
            "open-synthetic-research-model",
            "1.0.0",
            "https://huggingface.co/example/open-synthetic-research-model",
            "Apache-2.0",
            "a" * 64,
            "deadbeef",
            cutoff,
            "b" * 64,
            "c" * 64,
        )
        for team in (ModelTeam.QUANT, ModelTeam.AI)
    )
    votes = tuple(
        ResearchVote(
            "synthetic-research-candidate",
            team,
            f"{team.value.lower()}-synthetic-model-v1",
            ResearchLabel.POSITIVE,
            observed_at,
            "d" * 64,
        )
        for team in (ModelTeam.QUANT, ModelTeam.AI)
    )
    return evaluate_research_quorum(votes, artifacts)  # type: ignore[arg-type]
