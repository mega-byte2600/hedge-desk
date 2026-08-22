import unittest

from hedge_desk.demo import json_value
from hedge_desk.release import (
    REQUIRED_RELEASE_EVIDENCE,
    ReleaseEvidence,
    ReleaseStatus,
    build_reference_release_readiness,
    evaluate_live_release_readiness,
    validate_serialized_release_readiness,
)


class ReleaseReadinessTests(unittest.TestCase):
    def test_current_reference_is_blocked_and_not_human_overridable(self) -> None:
        result = build_reference_release_readiness()
        self.assertIs(result.status, ReleaseStatus.BLOCKED)
        self.assertFalse(result.human_override_allowed)
        self.assertFalse(result.live_transition_authorized)
        self.assertEqual(len(result.reason_codes), len(REQUIRED_RELEASE_EVIDENCE))
        self.assertEqual(validate_serialized_release_readiness(json_value(result)), ())
        self.assertIn(
            "RELEASE_REQUIREMENT_UNSATISFIED:REGULATORY_TRACEABILITY_VERIFIED",
            result.reason_codes,
        )
        self.assertIn(
            "RELEASE_REQUIREMENT_UNSATISFIED:BACK_OFFICE_RECONCILIATION_CERTIFIED",
            result.reason_codes,
        )
        self.assertEqual(result.gate_version, "live-release-gate-1.2.0")

    def test_all_hashed_evidence_only_reaches_separate_authorization(self) -> None:
        evidence = tuple(
            ReleaseEvidence(requirement_id, True, "a" * 64)
            for requirement_id in REQUIRED_RELEASE_EVIDENCE
        )
        result = evaluate_live_release_readiness(evidence)
        self.assertIs(result.status, ReleaseStatus.READY_FOR_SEPARATE_AUTHORIZATION)
        self.assertFalse(result.live_transition_authorized)
        self.assertFalse(result.human_override_allowed)
        zero_evidence = tuple(
            ReleaseEvidence(requirement_id, True, "0" * 64)
            for requirement_id in REQUIRED_RELEASE_EVIDENCE
        )
        zero_result = evaluate_live_release_readiness(zero_evidence)
        self.assertIs(zero_result.status, ReleaseStatus.BLOCKED)
        self.assertTrue(
            all("HASH_INVALID" in reason for reason in zero_result.reason_codes)
        )

    def test_missing_invalid_and_tampered_evidence_fails_closed(self) -> None:
        result = evaluate_live_release_readiness((
            ReleaseEvidence(REQUIRED_RELEASE_EVIDENCE[0], True, "bad"),
        ))
        self.assertIs(result.status, ReleaseStatus.BLOCKED)
        self.assertTrue(any("HASH_INVALID" in item for item in result.reason_codes))
        serialized = json_value(build_reference_release_readiness())
        serialized["live_transition_authorized"] = True
        self.assertIn(
            "LIVE_RELEASE_ARTIFACT_INVALID",
            validate_serialized_release_readiness(serialized),
        )

    def test_nonboolean_satisfaction_and_bad_identity_are_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "boolean"):
            evaluate_live_release_readiness((
                ReleaseEvidence(REQUIRED_RELEASE_EVIDENCE[0], 1, "a" * 64),
            ))
        with self.assertRaisesRegex(ValueError, "nonempty strings"):
            evaluate_live_release_readiness((ReleaseEvidence("", False, "0" * 64),))


if __name__ == "__main__":
    unittest.main()
