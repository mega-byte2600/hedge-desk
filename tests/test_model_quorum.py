from datetime import datetime, timezone
from dataclasses import replace
import unittest

from hedge_desk.models import (
    ModelArtifact,
    ModelTeam,
    ResearchLabel,
    ResearchVote,
    evaluate_research_quorum,
)


NOW = datetime(2026, 8, 21, tzinfo=timezone.utc)


def artifact(team: ModelTeam) -> ModelArtifact:
    return ModelArtifact(
        f"{team.value.lower()}-model-v1", team, "open-research-model", "1.0.0",
        "https://huggingface.co/example/open-research-model", "Apache-2.0",
        "a" * 64, "deadbeef", datetime(2026, 1, 1, tzinfo=timezone.utc),
        "b" * 64, "c" * 64,
    )


def vote(team: ModelTeam, label: ResearchLabel) -> ResearchVote:
    return ResearchVote(
        "candidate-1", team, f"{team.value.lower()}-model-v1", label, NOW, "d" * 64
    )


class ModelQuorumTests(unittest.TestCase):
    def test_agreement_is_research_only_and_has_no_control_authority(self) -> None:
        result = evaluate_research_quorum(
            (vote(ModelTeam.QUANT, ResearchLabel.POSITIVE),
             vote(ModelTeam.AI, ResearchLabel.POSITIVE)),
            (artifact(ModelTeam.QUANT), artifact(ModelTeam.AI)),
        )
        self.assertEqual(result.disposition, "RESEARCH_HYPOTHESIS_ONLY")
        self.assertFalse(result.authoritative_risk_input)
        self.assertEqual(result.compliance_status, "NOT_EVALUATED")
        self.assertEqual(result.human_authorization_status, "NOT_EVALUATED")

    def test_disagreement_or_abstention_is_no_trade(self) -> None:
        disagreement = evaluate_research_quorum(
            (vote(ModelTeam.QUANT, ResearchLabel.POSITIVE),
             vote(ModelTeam.AI, ResearchLabel.NEGATIVE)),
            (artifact(ModelTeam.QUANT), artifact(ModelTeam.AI)),
        )
        self.assertEqual(disagreement.disposition, "NO_TRADE")
        self.assertIn("RESEARCH_TEAMS_DISAGREE", disagreement.reason_codes)

    def test_model_binding_and_open_artifact_fail_closed(self) -> None:
        bad_vote = replace(
            vote(ModelTeam.AI, ResearchLabel.POSITIVE), model_artifact_id="wrong"
        )
        bad_artifact = replace(artifact(ModelTeam.AI), license_spdx="proprietary")
        result = evaluate_research_quorum(
            (vote(ModelTeam.QUANT, ResearchLabel.POSITIVE), bad_vote),
            (artifact(ModelTeam.QUANT), bad_artifact),
        )
        self.assertEqual(result.disposition, "NO_TRADE")
        self.assertIn("MODEL_ARTIFACT_BINDING_INVALID", result.reason_codes)
        self.assertIn("OPEN_LICENSE_REQUIRED", result.reason_codes)


if __name__ == "__main__":
    unittest.main()
