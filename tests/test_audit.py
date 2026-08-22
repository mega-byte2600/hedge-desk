from dataclasses import replace
import unittest

from hedge_desk.audit import (
    append_audit_event,
    build_audit_evaluation,
    build_reference_audit,
    validate_audit_evaluation,
    verify_audit_chain,
)


class AuditChainTests(unittest.TestCase):
    def test_reference_chain_is_complete_and_valid(self) -> None:
        chain = build_reference_audit()
        self.assertEqual(len(chain), 7)
        self.assertEqual(verify_audit_chain(chain), ())
        self.assertTrue(all(event.candidate_id for event in chain))
        self.assertEqual(chain[0].input_sha256, "0" * 64)
        self.assertTrue(
            all(
                later.input_sha256 == earlier.output_sha256
                for earlier, later in zip(chain, chain[1:])
            )
        )

    def test_mutated_event_is_detected(self) -> None:
        chain = list(build_reference_audit())
        chain[3] = replace(chain[3], artifact_id="tampered")
        self.assertIn("AUDIT_EVENT_HASH_INVALID", verify_audit_chain(tuple(chain)))
        chain = list(build_reference_audit())
        chain[2] = replace(chain[2], output_sha256="0" * 64)
        self.assertIn("AUDIT_OUTPUT_HASH_INVALID", verify_audit_chain(tuple(chain)))

    def test_deleted_event_breaks_sequence_and_link(self) -> None:
        chain = build_reference_audit()
        damaged = chain[:3] + chain[4:]
        reasons = verify_audit_chain(damaged)
        self.assertIn("AUDIT_SEQUENCE_INVALID", reasons)
        self.assertIn("AUDIT_PREVIOUS_HASH_INVALID", reasons)
        self.assertIn("AUDIT_INPUT_LINEAGE_INVALID", reasons)

    def test_changed_policy_or_input_lineage_is_detected(self) -> None:
        chain = list(build_reference_audit())
        chain[4] = replace(chain[4], policy_version="agent-policy")
        self.assertIn("AUDIT_EVENT_HASH_INVALID", verify_audit_chain(tuple(chain)))
        chain = list(build_reference_audit())
        chain[4] = replace(chain[4], input_sha256="f" * 64)
        self.assertIn("AUDIT_INPUT_LINEAGE_INVALID", verify_audit_chain(tuple(chain)))

    def test_append_rejects_wrong_lineage_run_time_and_corrupt_chain(self) -> None:
        chain = build_reference_audit()
        last = chain[-1]
        common = (
            last.occurred_at,
            "artifact-next",
            last.candidate_id,
            last.output_sha256,
            "f" * 64,
            "component-1",
            "policy-1",
        )
        with self.assertRaisesRegex(ValueError, "run identity"):
            append_audit_event(chain, "other-run", "NEXT", *common)
        with self.assertRaisesRegex(ValueError, "prior output"):
            append_audit_event(
                chain, last.run_id, "NEXT", last.occurred_at,
                "artifact-next", last.candidate_id, "e" * 64, "f" * 64,
                "component-1", "policy-1",
            )
        corrupt = chain[:-1] + (replace(last, event_hash="e" * 64),)
        with self.assertRaisesRegex(ValueError, "invalid audit chain"):
            append_audit_event(corrupt, last.run_id, "NEXT", *common)

    def test_serialized_evaluation_is_independently_verified(self) -> None:
        evaluation = build_audit_evaluation()
        self.assertEqual(validate_audit_evaluation(evaluation), ())
        evaluation["events"][3]["artifact_id"] = "tampered"
        self.assertIn(
            "AUDIT_EVENT_HASH_INVALID", validate_audit_evaluation(evaluation)
        )


if __name__ == "__main__":
    unittest.main()
