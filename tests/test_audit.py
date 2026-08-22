from dataclasses import replace
import unittest

from hedge_desk.audit import build_reference_audit, verify_audit_chain


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


if __name__ == "__main__":
    unittest.main()
