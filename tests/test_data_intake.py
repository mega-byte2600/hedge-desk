from datetime import datetime, timedelta, timezone
from hashlib import sha256
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from hedge_desk.data import validate_local_observation


NOW = datetime(2026, 8, 21, 12, 0, tzinfo=timezone.utc)


class LocalDataIntakeTests(unittest.TestCase):
    def _files(self, root: Path):
        payload = root / "vendor-payload.json"
        payload.write_bytes(b'{"bid":"1.00","ask":"1.05"}\n')
        envelope = root / "vendor-payload.envelope.json"
        envelope.write_text(
            json.dumps(
                {
                    "schema_version": "hedge-desk-observation-1.0.0",
                    "artifact_id": "vendor-option-snapshot-1",
                    "payload_kind": "option_chain",
                    "source_id": "licensed-vendor-account",
                    "license_id": "private-entitlement-1",
                    "source_as_of": NOW.isoformat(),
                    "received_at": NOW.isoformat(),
                    "payload_sha256": sha256(payload.read_bytes()).hexdigest(),
                    "synthetic": False,
                    "redistribution_allowed": False,
                },
                sort_keys=True,
            ),
            encoding="utf-8",
        )
        return envelope, payload

    def test_valid_local_payload_is_hashed_but_not_copied(self) -> None:
        with TemporaryDirectory() as temporary:
            envelope, payload = self._files(Path(temporary))
            result = validate_local_observation(envelope, payload, NOW, 0)
            self.assertTrue(result.gate.admissible)
            self.assertFalse(result.artifact.redistribution_allowed)
            self.assertEqual(result.payload_size_bytes, len(payload.read_bytes()))
            self.assertEqual(result.payload_path, str(payload.resolve()))

    def test_payload_tamper_is_rejected_before_artifact_creation(self) -> None:
        with TemporaryDirectory() as temporary:
            envelope, payload = self._files(Path(temporary))
            payload.write_bytes(b"changed")
            with self.assertRaisesRegex(ValueError, "does not match"):
                validate_local_observation(envelope, payload, NOW, 0)

    def test_unknown_fields_and_naive_timestamps_fail_closed(self) -> None:
        with TemporaryDirectory() as temporary:
            envelope, payload = self._files(Path(temporary))
            value = json.loads(envelope.read_text())
            value["agent_probability"] = "0.99"
            envelope.write_text(json.dumps(value))
            with self.assertRaisesRegex(ValueError, "fields unknown"):
                validate_local_observation(envelope, payload, NOW, 0)
            value.pop("agent_probability")
            value["received_at"] = "2026-08-21T12:00:00"
            envelope.write_text(json.dumps(value))
            with self.assertRaisesRegex(ValueError, "include a timezone"):
                validate_local_observation(envelope, payload, NOW, 0)

    def test_point_in_time_and_freshness_rules_are_preserved(self) -> None:
        with TemporaryDirectory() as temporary:
            envelope, payload = self._files(Path(temporary))
            future = validate_local_observation(
                envelope, payload, NOW - timedelta(microseconds=1), 0
            )
            self.assertIn("POINT_IN_TIME_VIOLATION", future.gate.reason_codes)
            stale = validate_local_observation(
                envelope, payload, NOW + timedelta(seconds=11), 10
            )
            self.assertIn("DATA_STALE", stale.gate.reason_codes)


if __name__ == "__main__":
    unittest.main()
