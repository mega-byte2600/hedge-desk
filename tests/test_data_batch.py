import unittest

from hedge_desk.data import (
    BatchStatus,
    SourceBatchResult,
    SourceBatchStatus,
    build_batch_manifest,
    validate_serialized_batch_manifest,
)
from hedge_desk.demo import json_value


HASH_A = "a" * 64
HASH_B = "b" * 64


class DataBatchTests(unittest.TestCase):
    def test_complete_batch_is_ready_and_order_deterministic(self) -> None:
        a = SourceBatchResult("a", SourceBatchStatus.PASS, HASH_A)
        b = SourceBatchResult("b", SourceBatchStatus.PASS, HASH_B)
        forward = build_batch_manifest("batch", ("a", "b"), (a, b), HASH_A)
        reverse = build_batch_manifest("batch", ("b", "a"), (b, a), HASH_A)
        self.assertIs(forward.status, BatchStatus.READY_FOR_RESEARCH)
        self.assertEqual(forward.manifest_sha256, reverse.manifest_sha256)

    def test_missing_required_source_is_incomplete(self) -> None:
        result = SourceBatchResult("a", SourceBatchStatus.PASS, HASH_A)
        manifest = build_batch_manifest("batch", ("a", "b"), (result,), HASH_A)
        self.assertIs(manifest.status, BatchStatus.INCOMPLETE)
        self.assertIn("REQUIRED_SOURCE_MISSING:b", manifest.reason_codes)

    def test_quarantined_and_rejected_sources_fail_closed(self) -> None:
        quarantine = SourceBatchResult("a", SourceBatchStatus.QUARANTINE, HASH_A)
        rejected = SourceBatchResult("a", SourceBatchStatus.REJECT, HASH_A)
        self.assertIs(
            build_batch_manifest("q", ("a",), (quarantine,), HASH_A).status,
            BatchStatus.QUARANTINED,
        )
        self.assertIs(
            build_batch_manifest("r", ("a",), (rejected,), HASH_A).status,
            BatchStatus.REJECTED,
        )

    def test_invalid_artifact_hash_rejects_batch(self) -> None:
        result = SourceBatchResult("a", SourceBatchStatus.PASS, "bad")
        manifest = build_batch_manifest("batch", ("a",), (result,), HASH_A)
        self.assertIs(manifest.status, BatchStatus.REJECTED)
        self.assertIn("SOURCE_ARTIFACT_HASH_INVALID", manifest.reason_codes)

    def test_unexpected_source_pass_reasons_and_zero_policy_reject(self) -> None:
        unexpected = SourceBatchResult("extra", SourceBatchStatus.PASS, HASH_B)
        claimed_pass = SourceBatchResult(
            "a", SourceBatchStatus.PASS, HASH_A, ("STALE",)
        )
        manifest = build_batch_manifest(
            "batch", ("a",), (claimed_pass, unexpected), HASH_A
        )
        self.assertIs(manifest.status, BatchStatus.REJECTED)
        self.assertIn("SOURCE_PASS_HAS_REASONS", manifest.reason_codes)
        self.assertIn("UNEXPECTED_SOURCE:extra", manifest.reason_codes)
        with self.assertRaisesRegex(ValueError, "hashes"):
            build_batch_manifest("batch", ("a",), (claimed_pass,), "0" * 64)

    def test_serialized_manifest_is_independently_rebuilt(self) -> None:
        result = SourceBatchResult("a", SourceBatchStatus.PASS, HASH_A)
        manifest = json_value(
            build_batch_manifest("batch", ("a",), (result,), HASH_B)
        )
        self.assertEqual(validate_serialized_batch_manifest(manifest), ())
        manifest["source_results"][0]["artifact_sha256"] = "f" * 64
        self.assertIn(
            "BATCH_MANIFEST_HASH_MISMATCH",
            validate_serialized_batch_manifest(manifest),
        )


if __name__ == "__main__":
    unittest.main()
