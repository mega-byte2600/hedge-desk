import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from hashlib import sha256

from hedge_desk.overnight import build_morning_report
from datetime import datetime, timezone


class CliTests(unittest.TestCase):
    def test_option_snapshot_cli_reports_structure_not_quote_payload(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payload = root / "options.json"
            payload.write_text(
                json.dumps(
                    {
                        "schema_version": "hedge-desk-option-snapshot-1.0.0",
                        "underlying_quote": {
                            "symbol": "TEST", "bid": "99.99", "ask": "100.01",
                            "quoted_at": "2026-08-21T12:00:00Z",
                        },
                        "option_quotes": [{
                            "contract_id": "TEST260918P00095000",
                            "underlying": "TEST", "option_type": "put",
                            "strike": "95", "expiration": "2026-09-18",
                            "bid": "2.00", "ask": "2.10", "bid_size": 25,
                            "ask_size": 30, "quoted_at": "2026-08-21T12:00:00Z",
                            "open_interest": 1000, "volume": 500,
                        }],
                    }
                ),
                encoding="utf-8",
            )
            envelope = root / "options.envelope.json"
            envelope.write_text(json.dumps({
                "schema_version": "hedge-desk-observation-1.0.0",
                "artifact_id": "options-1", "payload_kind": "option_chain",
                "source_id": "local-entitled-source", "license_id": "entitlement-1",
                "source_as_of": "2026-08-21T12:00:00Z",
                "received_at": "2026-08-21T12:00:00Z",
                "payload_sha256": sha256(payload.read_bytes()).hexdigest(),
                "synthetic": False, "redistribution_allowed": False,
            }), encoding="utf-8")
            result = subprocess.run([
                sys.executable, "-m", "hedge_desk.cli",
                "--validate-data-envelope", str(envelope),
                "--payload", str(payload), "--validate-option-snapshot",
                "--scan-vertical-spreads",
                "--decision-cutoff", "2026-08-21T12:00:00Z",
            ], check=True, capture_output=True, text=True)
            output = json.loads(result.stdout)
            self.assertEqual(output["option_snapshot"]["contract_count"], 1)
            self.assertEqual(output["option_snapshot"]["symbol"], "TEST")
            self.assertEqual(
                output["vertical_spread_scan"]["disposition"], "NO_TRADE"
            )
            self.assertNotIn('"bid": "2.00"', result.stdout)

    def test_local_data_intake_cli_validates_without_copying_payload(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payload = root / "snapshot.json"
            payload.write_bytes(b'{"symbol":"TEST"}\n')
            envelope = root / "snapshot.envelope.json"
            envelope.write_text(
                json.dumps(
                    {
                        "schema_version": "hedge-desk-observation-1.0.0",
                        "artifact_id": "snapshot-1",
                        "payload_kind": "option_chain",
                        "source_id": "local-entitled-source",
                        "license_id": "entitlement-1",
                        "source_as_of": "2026-08-21T12:00:00+00:00",
                        "received_at": "2026-08-21T12:00:00+00:00",
                        "payload_sha256": sha256(payload.read_bytes()).hexdigest(),
                        "synthetic": False,
                        "redistribution_allowed": False,
                    }
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "hedge_desk.cli",
                    "--validate-data-envelope",
                    str(envelope),
                    "--payload",
                    str(payload),
                    "--decision-cutoff",
                    "2026-08-21T12:00:00Z",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            output = json.loads(result.stdout)
            self.assertTrue(output["gate"]["admissible"])
            self.assertEqual(output["payload_path"], str(payload.resolve()))
            self.assertEqual(sorted(root.iterdir()), [envelope, payload])

    def test_markdown_is_rendered_from_exact_json_report_hash(self) -> None:
        report = build_morning_report(
            datetime(2026, 8, 21, 12, 0, tzinfo=timezone.utc)
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "morning.json"
            path.write_text(json.dumps(report), encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "hedge_desk.cli",
                    "--morning-markdown",
                    "--report-input",
                    str(path),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
        self.assertIn(report["report_sha256"], result.stdout)

    def test_scheduler_receipt_is_bound_to_exact_report_hash(self) -> None:
        report = build_morning_report(
            datetime(2026, 8, 21, 12, 0, tzinfo=timezone.utc)
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "morning.json"
            path.write_text(json.dumps(report), encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable, "-m", "hedge_desk.cli",
                    "--scheduled-receipt", "--idempotency-key", "test-run",
                    "--report-input", str(path),
                ],
                check=True, capture_output=True, text=True,
            )
        receipt = json.loads(result.stdout)
        self.assertEqual(receipt["status"], "COMPLETE")
        self.assertEqual(receipt["report_sha256"], report["report_sha256"])


if __name__ == "__main__":
    unittest.main()
