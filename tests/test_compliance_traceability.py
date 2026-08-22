from dataclasses import replace
import unittest

from hedge_desk.compliance.traceability import (
    REFERENCE_REQUIREMENTS,
    traceability_sha256,
    validate_traceability_registry,
)


class ComplianceTraceabilityTests(unittest.TestCase):
    def test_reference_registry_is_authoritative_hashed_and_not_live_approved(self) -> None:
        self.assertEqual(validate_traceability_registry(), ())
        self.assertEqual(len(traceability_sha256()), 64)
        self.assertTrue(all(not item.counsel_approved_for_live for item in REFERENCE_REQUIREMENTS))

    def test_non_authoritative_source_or_missing_test_fails_closed(self) -> None:
        attacked = (
            replace(
                REFERENCE_REQUIREMENTS[0],
                source_url="https://example.com/summary",
                test_module="",
            ),
        )
        reasons = validate_traceability_registry(attacked)
        self.assertIn("REGULATORY_SOURCE_NOT_AUTHORITATIVE", reasons)
        self.assertIn("REGULATORY_TEST_REFERENCE_INVALID", reasons)


if __name__ == "__main__":
    unittest.main()
