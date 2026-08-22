from dataclasses import replace
from datetime import datetime, timedelta, timezone
import unittest

from hedge_desk.models import (
    ModelArtifact, ModelTeam, TrainingRunManifest, validate_training_run,
)


CUTOFF = datetime(2026, 1, 1, tzinfo=timezone.utc)


def artifact():
    return ModelArtifact(
        "ai-model-v1", ModelTeam.AI, "open-model", "1.0.0",
        "https://huggingface.co/example/open-model", "Apache-2.0", "a" * 64,
        "deadbeef", CUTOFF, "d" * 64, "e" * 64,
    )


def run():
    return TrainingRunManifest(
        "run-1", ModelTeam.AI, "ai-model-v1", "deadbeef", "f" * 64,
        "b" * 64, "c" * 64, "d" * 64, "e" * 64, CUTOFF,
        CUTOFF + timedelta(days=1), CUTOFF + timedelta(days=2), 2600,
        "point-in-time-purged-walk-forward", True,
    )


class TrainingRunTests(unittest.TestCase):
    def test_reproducible_open_run_is_research_only(self) -> None:
        result = validate_training_run(run(), artifact())
        self.assertTrue(result.admissible)
        self.assertFalse(result.authoritative_risk_input)
        self.assertFalse(result.trade_authorized)

    def test_split_collision_and_lookahead_fail_closed(self) -> None:
        attacked = replace(
            run(), validation_dataset_sha256="b" * 64,
            data_cutoff=CUTOFF + timedelta(days=3),
        )
        result = validate_training_run(attacked, artifact())
        self.assertIn("TRAINING_SPLIT_HASH_COLLISION", result.reason_codes)
        self.assertIn("TRAINING_DATA_LOOKAHEAD", result.reason_codes)

    def test_binding_or_authority_attack_fails_closed(self) -> None:
        attacked = replace(run(), code_commit="other", research_only=False)
        result = validate_training_run(attacked, artifact())
        self.assertIn("TRAINING_CODE_COMMIT_MISMATCH", result.reason_codes)
        self.assertIn("TRAINING_RUN_CONTROL_AUTHORITY_FORBIDDEN", result.reason_codes)


if __name__ == "__main__":
    unittest.main()
