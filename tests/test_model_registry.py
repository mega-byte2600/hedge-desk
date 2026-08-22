from dataclasses import replace
from datetime import datetime, timezone
import unittest

from hedge_desk.models import ModelArtifact, ModelTeam, validate_open_model_artifact


HASH = "a" * 64


def open_artifact(team: ModelTeam = ModelTeam.QUANT) -> ModelArtifact:
    return ModelArtifact(
        artifact_id="model-1",
        team=team,
        model_id="reference-open-model",
        model_version="1.0.0",
        source_repository="https://huggingface.co/example/reference-open-model",
        license_spdx="Apache-2.0",
        weights_sha256=HASH,
        code_commit="deadbeef",
        training_cutoff=datetime(2026, 1, 1, tzinfo=timezone.utc),
        evaluation_dataset_sha256="b" * 64,
        evaluation_report_sha256="c" * 64,
    )


class ModelRegistryTests(unittest.TestCase):
    def test_quant_and_ai_open_artifacts_pass_same_gate(self) -> None:
        self.assertEqual(validate_open_model_artifact(open_artifact()), ())
        self.assertEqual(validate_open_model_artifact(open_artifact(ModelTeam.AI)), ())

    def test_proprietary_runtime_or_unapproved_license_fails_closed(self) -> None:
        artifact = replace(
            open_artifact(),
            license_spdx="unknown",
            proprietary_runtime_required=True,
        )
        self.assertEqual(
            validate_open_model_artifact(artifact),
            ("OPEN_LICENSE_REQUIRED", "PROPRIETARY_RUNTIME_REQUIRED"),
        )

    def test_missing_reproducibility_hash_fails_closed(self) -> None:
        artifact = replace(open_artifact(), weights_sha256="")
        self.assertIn("REPRODUCIBILITY_HASH_INVALID", validate_open_model_artifact(artifact))


if __name__ == "__main__":
    unittest.main()
