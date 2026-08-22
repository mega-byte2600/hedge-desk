from dataclasses import replace
from datetime import datetime, timedelta, timezone
import unittest

from hedge_desk.data.contracts import DataArtifact, sha256_text, validate_data_artifact


NOW = datetime(2026, 8, 21, 12, 0, tzinfo=timezone.utc)


def artifact() -> DataArtifact:
    return DataArtifact(
        "artifact-1", "option_chain", "vendor", "license-1", NOW, NOW,
        sha256_text("payload"), False, False,
    )


class DataContractTests(unittest.TestCase):
    def test_boolean_age_or_entitlement_and_zero_hash_are_rejected(self) -> None:
        value = artifact()
        with self.assertRaisesRegex(ValueError, "nonnegative integer"):
            validate_data_artifact(value, NOW, True)
        with self.assertRaisesRegex(ValueError, "boolean"):
            validate_data_artifact(replace(value, synthetic=1), NOW, 120)
        blocked = validate_data_artifact(
            replace(value, payload_sha256="0" * 64), NOW, 120
        )
        self.assertIn("PAYLOAD_HASH_INVALID", blocked.reason_codes)

    def test_complete_point_in_time_artifact_passes(self) -> None:
        self.assertTrue(validate_data_artifact(artifact(), NOW, 0).admissible)

    def test_missing_license_and_bad_hash_fail_closed(self) -> None:
        result = validate_data_artifact(
            replace(artifact(), license_id="", payload_sha256="bad"), NOW, 0
        )
        self.assertEqual(result.reason_codes, ("LICENSE_MISSING", "PAYLOAD_HASH_INVALID"))

    def test_data_received_after_cutoff_is_point_in_time_violation(self) -> None:
        future = replace(artifact(), received_at=NOW + timedelta(microseconds=1))
        self.assertIn(
            "POINT_IN_TIME_VIOLATION", validate_data_artifact(future, NOW, 0).reason_codes
        )

    def test_freshness_boundary_is_exact(self) -> None:
        old = replace(artifact(), source_as_of=NOW - timedelta(seconds=11), received_at=NOW - timedelta(seconds=11))
        self.assertTrue(validate_data_artifact(old, NOW, 11).admissible)
        self.assertIn("DATA_STALE", validate_data_artifact(old, NOW, 10).reason_codes)


if __name__ == "__main__":
    unittest.main()
