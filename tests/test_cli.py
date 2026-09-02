import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from hashlib import sha256

from hedge_desk.overnight import build_morning_report
from hedge_desk.demo import json_value
from hedge_desk.audit import build_reference_audit
from hedge_desk.audit_store import initialize_audit_journal
from hedge_desk.scheduler import ScheduledRunRequest, execute_scheduled_run
from datetime import datetime, timezone


class CliTests(unittest.TestCase):
    def test_cli_shows_yellow_sheet_rationale_for_candidate(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "hedge_desk.cli", "--yellow-sheet-rationale"],
            check=True, capture_output=True, text=True,
        )
        output = json.loads(result.stdout)
        self.assertEqual(output["disposition"], "HOLD")
        self.assertEqual(output["reason_codes"], [])
        self.assertTrue(output["yellow_sheet_id"])
        self.assertTrue(output["why"])

    def test_committed_directional_fixture_is_content_bound_and_insufficient(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "hedge_desk.cli",
             "--evaluate-directional-outcomes",
             str(Path(__file__).resolve().parents[1] / "examples" /
                 "directional-outcomes.synthetic.json")],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)
        self.assertEqual(output["label"], "STAT")
        self.assertEqual(output["evaluation"]["inference_status"], "INSUFFICIENT_SAMPLE")
        self.assertFalse(output["evaluation"]["trade_authorized"])

    def test_directional_inference_cli_rejects_hash_mismatch_and_duplicate_ids(self) -> None:
        base = {
            "schema_version": "directional-outcomes-1.1.0",
            "dataset_sha256": "a" * 64,
            "source_id": "source",
            "model_id": "model",
            "model_version": "1",
            "observations": [
                {"observation_id": "duplicate", "outcome": True},
                {"observation_id": "duplicate", "outcome": False},
            ],
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "outcomes.json"
            path.write_text(json.dumps(base), encoding="utf-8")
            duplicate = subprocess.run(
                [sys.executable, "-m", "hedge_desk.cli",
                 "--evaluate-directional-outcomes", str(path)],
                capture_output=True, text=True, check=False,
            )
            base["observations"][1]["observation_id"] = "unique"
            path.write_text(json.dumps(base), encoding="utf-8")
            mismatch = subprocess.run(
                [sys.executable, "-m", "hedge_desk.cli",
                 "--evaluate-directional-outcomes", str(path)],
                capture_output=True, text=True, check=False,
            )
        self.assertNotEqual(duplicate.returncode, 0)
        self.assertIn("must be unique", duplicate.stderr)
        self.assertNotEqual(mismatch.returncode, 0)
        self.assertIn("hash mismatch", mismatch.stderr)

    def test_directional_inference_cli_is_strict_and_never_authorizes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "outcomes.json"
            observations = [
                {"observation_id": f"obs-{index}", "outcome": index < 70}
                for index in range(100)
            ]
            dataset_hash = sha256(json.dumps(
                observations, sort_keys=True, separators=(",", ":")
            ).encode()).hexdigest()
            path.write_text(json.dumps({
                "schema_version": "directional-outcomes-1.1.0",
                "dataset_sha256": dataset_hash,
                "source_id": "licensed-point-in-time-fixture",
                "model_id": "stat-directional-fixture",
                "model_version": "1.0.0",
                "observations": observations,
            }), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, "-m", "hedge_desk.cli",
                 "--evaluate-directional-outcomes", str(path)],
                capture_output=True, text=True, check=False,
            )
            path.write_text(json.dumps({
                "schema_version": "directional-outcomes-1.1.0",
                "dataset_sha256": "a" * 64,
                "source_id": "licensed-point-in-time-fixture",
                "model_id": "stat-directional-fixture",
                "model_version": "1.0.0",
                "observations": [
                    {"observation_id": f"obs-{index}", "outcome": True}
                    for index in range(100)
                ],
                "agent_override": True,
            }), encoding="utf-8")
            rejected = subprocess.run(
                [sys.executable, "-m", "hedge_desk.cli",
                 "--evaluate-directional-outcomes", str(path)],
                capture_output=True, text=True, check=False,
            )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        output = json.loads(completed.stdout)
        self.assertEqual(output["label"], "STAT")
        self.assertEqual(output["dataset_sha256"], dataset_hash)
        self.assertEqual(output["evaluation"]["alpha"], "0.005")
        self.assertEqual(output["evaluation"]["confidence_level"], "0.95")
        self.assertTrue(output["evaluation"]["statistically_significant"])
        self.assertFalse(output["evaluation"]["trade_authorized"])
        self.assertNotEqual(rejected.returncode, 0)
        self.assertIn("schema is invalid", rejected.stderr)

    def test_control_summary_cli_requires_and_validates_report(self) -> None:
        report = build_morning_report(datetime(2026, 8, 21, 12, 0, tzinfo=timezone.utc))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "report.json"
            path.write_text(json.dumps(report), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, "-m", "hedge_desk.cli", "--control-summary",
                 "--report-input", str(path)],
                capture_output=True, text=True, check=False,
            )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        summary = json.loads(completed.stdout)
        self.assertEqual(summary["real_money_pnl"], "0")
        self.assertEqual(summary["real_trades_executed"], 0)
        self.assertEqual(summary["war_game_scenarios"], 73)
        self.assertFalse(summary["live_transition_authorized"])
        self.assertEqual(summary["paper_back_office_reconciliation"], "pass")
        self.assertFalse(summary["paper_reconciliation_live_release_eligible"])
        self.assertTrue(summary["premium_new_entry_evaluation_allowed"])
        self.assertTrue(summary["premium_monitoring_allowed"])

    def test_run_health_cli_verifies_fresh_paper_artifacts(self) -> None:
        now = datetime(2026, 8, 22, 9, 0, tzinfo=timezone.utc)
        commit = "a" * 40
        report = build_morning_report(now, commit)
        receipt = json_value(execute_scheduled_run(
            ScheduledRunRequest("cli-health", now), (), lambda _: report
        )[-1])
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "morning-report.json").write_text(json.dumps(report), encoding="utf-8")
            (root / "run-receipt.json").write_text(json.dumps(receipt), encoding="utf-8")
            initialize_audit_journal(root / "audit-journal.jsonl", build_reference_audit())
            result = subprocess.run(
                [
                    sys.executable, "-m", "hedge_desk.cli", "--verify-run-health",
                    str(root), "--health-evaluated-at", "2026-08-22T09:15:00Z",
                    "--maximum-run-age-seconds", "900",
                ],
                check=True, capture_output=True, text=True,
                env={**os.environ, "HEDGE_DESK_CODE_COMMIT": commit},
            )
        output = json.loads(result.stdout)
        self.assertEqual(output["status"], "HEALTHY_PAPER")
        self.assertFalse(output["live_authorized"])

    def test_audit_journal_cli_creates_once_and_verifies(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "audit.jsonl"
            created = subprocess.run(
                [sys.executable, "-m", "hedge_desk.cli", "--audit-journal", str(path)],
                check=True, capture_output=True, text=True,
            )
            self.assertEqual(json.loads(created.stdout)["status"], "INITIALIZED")
            verified = subprocess.run(
                [sys.executable, "-m", "hedge_desk.cli", "--verify-audit-journal", str(path)],
                check=True, capture_output=True, text=True,
            )
            self.assertTrue(json.loads(verified.stdout)["valid"])
            duplicate = subprocess.run(
                [sys.executable, "-m", "hedge_desk.cli", "--audit-journal", str(path)],
                capture_output=True, text=True,
            )
            self.assertNotEqual(duplicate.returncode, 0)

    def test_data_stack_cli_reports_readiness_without_vendor_payload(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data-stack.json"
            path.write_text(json.dumps({
                "schema_version": "hedge-desk-data-stack-1.1.0",
                "monthly_budget": "100",
                "subscriptions": [{
                    "source_id": "permissioned-options-feed",
                    "monthly_cost": "80",
                    "entitlement_id": "internal-research-license",
                    "historical_nbbo_quotes": True,
                    "expired_option_contracts": True,
                    "option_chain_snapshots": True,
                    "corporate_actions": True,
                    "point_in_time_timestamps": True,
                    "trades": True,
                    "open_interest": True,
                    "historical_years": 8,
                    "real_time_nbbo": False,
                    "commercial_use_allowed": False,
                    "redistribution_allowed": False,
                }],
            }), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "-m", "hedge_desk.cli", "--validate-data-stack", str(path)],
                check=True, capture_output=True, text=True,
            )
        output = json.loads(result.stdout)
        self.assertTrue(output["ready_for_internal_options_research"])
        self.assertFalse(output["ready_for_live_production_data"])
        self.assertEqual(output["live_production_reason_codes"], [
            "COMMERCIAL_USE_PERMISSION_ABSENT", "REAL_TIME_NBBO_ABSENT"
        ])
        self.assertFalse(output["raw_payload_commit_allowed"])
        self.assertNotIn("vendor_payload", result.stdout)

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
                        }, {
                            "contract_id": "TEST260918P00090000",
                            "underlying": "TEST", "option_type": "put",
                            "strike": "90", "expiration": "2026-09-18",
                            "bid": "0.75", "ask": "0.80", "bid_size": 25,
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
            session = root / "market-session.json"
            session.write_text(json.dumps({
                "schema_version": "hedge-desk-market-session-1.0.0",
                "venue": "OPRA",
                "regular_open": "2026-08-21T11:00:00Z",
                "regular_close": "2026-08-21T13:00:00Z",
                "received_at": "2026-08-21T10:00:00Z",
                "calendar_artifact_sha256": "b" * 64,
            }), encoding="utf-8")
            result = subprocess.run([
                sys.executable, "-m", "hedge_desk.cli",
                "--validate-data-envelope", str(envelope),
                "--payload", str(payload), "--validate-option-snapshot",
                "--scan-vertical-spreads",
                "--market-session-evidence", str(session),
                "--decision-cutoff", "2026-08-21T12:00:00Z",
            ], check=True, capture_output=True, text=True)
            output = json.loads(result.stdout)
            self.assertEqual(output["option_snapshot"]["contract_count"], 2)
            self.assertEqual(output["option_snapshot"]["symbol"], "TEST")
            self.assertEqual(
                output["vertical_spread_scan"]["disposition"],
                "CANDIDATES_FOR_CONTROL_PIPELINE",
            )
            self.assertEqual(len(output["control_handoffs"]), 1)
            self.assertFalse(output["control_handoffs"][0]["trade_authorized"])
            self.assertEqual(output["handoff_reason_codes"], [])
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
        self.assertEqual(len(receipt["receipt_sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
