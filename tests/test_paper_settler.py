"""Deterministic tests for the read-only paper outcome settler (Move #3)."""

import json
import subprocess
import sys
import tempfile
import unittest
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

from hedge_desk.demo import (
    FIXTURE_AS_OF,
    build_reference_option_snapshot,
    build_reference_plan,
)
from hedge_desk.paper import (
    advance_paper_lifecycle,
    approve_paper_trade,
    close_paper_position,
    create_paper_trade_plan,
    settle_paper_outcomes,
    write_plan_file,
)
from hedge_desk.paper_log import read_log

TICK_NOW = FIXTURE_AS_OF + timedelta(seconds=60)
DECIDED_AT = FIXTURE_AS_OF + timedelta(minutes=1)
CLOSED_AT = FIXTURE_AS_OF + timedelta(minutes=2)
# The reference fixture expires 2026-08-21; this is past expiration.
PAST_EXPIRATION = datetime(2026, 8, 22, 12, 0, tzinfo=timezone.utc)


def _approved_plan(plan_id):
    base = build_reference_plan()
    plan = create_paper_trade_plan(
        plan_id,
        base.spread,
        base.risk_decision,
        base.compliance_decision,
        base.created_at,
        base.approval_expires_at,
        event_calendar_gate=base.event_calendar_gate,
    )
    return approve_paper_trade(plan, "captain", DECIDED_AT)


def _ready_quotes(plan):
    return (plan.spread.quantity, plan.spread.net_credit)


def _exit_quotes(closed_at, short_bid, short_ask, long_bid, long_ask):
    snapshot = build_reference_option_snapshot()
    short = replace(
        snapshot.option_quotes[0],
        bid=Decimal(short_bid), ask=Decimal(short_ask), quoted_at=closed_at,
    )
    long = replace(
        snapshot.option_quotes[1],
        bid=Decimal(long_bid), ask=Decimal(long_ask), quoted_at=closed_at,
    )
    return short, long


def _provider_otm(plan):
    return {"underlying_close": Decimal("100.00"), "short_intrinsic": Decimal("0")}


def _provider_itm(plan):
    return {"underlying_close": Decimal("85.00"), "short_intrinsic": Decimal("10.00")}


def _provider_none(plan):
    return {"underlying_close": None, "short_intrinsic": None}


class PaperSettlerTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.state_dir = Path(self.directory.name)
        self.plans_dir = self.state_dir / "plans"
        self.plans_dir.mkdir()
        self.state_path = self.state_dir / "state.json"
        self.log_path = self.state_dir / "paper-outcomes.jsonl"

    def _write_plan(self, plan_id):
        plan = _approved_plan(plan_id)
        write_plan_file(plan, self.plans_dir / f"{plan_id}.json")
        return plan

    def _open_plan(self, plan_id):
        plan = self._write_plan(plan_id)
        advance_paper_lifecycle(self.plans_dir, self.state_path, _ready_quotes, TICK_NOW)
        return plan

    def _close_plan(self, plan_id, short_quotes, long_quotes):
        plan = self._open_plan(plan_id)
        short, long = _exit_quotes(CLOSED_AT, *short_quotes, *long_quotes)
        close_paper_position(
            self.plans_dir,
            self.state_path,
            plan.plan_id,
            "captain",
            CLOSED_AT,
            ("PROFIT_TARGET_REACHED",),
            short,
            long,
            Decimal("0.65"),
        )
        return plan

    def _log_lines(self):
        if not self.log_path.exists():
            return []
        return [line for line in self.log_path.read_text(encoding="utf-8").splitlines() if line.strip()]

    def test_closed_gain_recorded_once_with_provenance(self):
        plan = self._close_plan("plan-gain", ("0.40", "0.50"), ("0.10", "0.20"))
        report = settle_paper_outcomes(
            self.state_dir, self.log_path, _provider_none, PAST_EXPIRATION
        )
        self.assertEqual(len(report["settled"]), 1)
        settled = report["settled"][0]
        self.assertEqual(settled["plan_id"], plan.plan_id)
        self.assertEqual(settled["outcome"], "CLOSED_GAIN")
        self.assertIn("REALIZED_PNL_GAIN", settled["reason_codes"])
        self.assertEqual(report["unknown"], [])
        self.assertEqual(report["skipped"], [])

        entries = read_log(self.log_path)
        self.assertEqual(len(entries), 1)
        entry = entries[0]
        self.assertEqual(entry["candidate_id"], plan.plan_id)
        self.assertEqual(entry["symbol"], "TEST")
        self.assertEqual(entry["strategy"], "CREDIT_SPREAD")
        self.assertEqual(entry["outcome"], "CLOSED_GAIN")
        self.assertFalse(entry["trade_authorized"])
        provenance = entry["provenance"]
        self.assertEqual(provenance["plan_id"], plan.plan_id)
        self.assertEqual(provenance["plan_hash"], plan.plan_hash)
        self.assertEqual(provenance["human_id"], "captain")
        self.assertEqual(provenance["decided_at"], CLOSED_AT.isoformat())
        self.assertEqual(provenance["reason_codes"], ["PROFIT_TARGET_REACHED"])
        artifact = json.loads(
            (self.state_dir / "closes" / f"{plan.plan_id}.json").read_text(encoding="utf-8")
        )
        self.assertEqual(provenance["close_sha256"], artifact["close"]["close_sha256"])

    def test_rerun_is_idempotent(self):
        self._close_plan("plan-gain-twice", ("0.40", "0.50"), ("0.10", "0.20"))
        first = settle_paper_outcomes(
            self.state_dir, self.log_path, _provider_none, PAST_EXPIRATION
        )
        self.assertEqual(len(first["settled"]), 1)
        second = settle_paper_outcomes(
            self.state_dir, self.log_path, _provider_none, PAST_EXPIRATION
        )
        self.assertEqual(second["settled"], [])
        self.assertEqual(second["unknown"], [])
        self.assertEqual(len(second["skipped"]), 1)
        self.assertEqual(second["skipped"][0]["reason_codes"], ["ALREADY_SETTLED"])
        self.assertEqual(second["skipped"][0]["outcome"], "CLOSED_GAIN")
        self.assertEqual(len(self._log_lines()), 1)

    def test_closed_loss_recorded(self):
        plan = self._close_plan("plan-loss", ("1.90", "2.00"), ("0.40", "0.50"))
        report = settle_paper_outcomes(
            self.state_dir, self.log_path, _provider_none, PAST_EXPIRATION
        )
        self.assertEqual(len(report["settled"]), 1)
        self.assertEqual(report["settled"][0]["outcome"], "CLOSED_LOSS")
        self.assertIn("REALIZED_PNL_LOSS", report["settled"][0]["reason_codes"])
        entries = read_log(self.log_path)
        self.assertEqual(entries[0]["outcome"], "CLOSED_LOSS")
        self.assertEqual(entries[0]["candidate_id"], plan.plan_id)

    def test_zero_pnl_close_maps_to_stopped(self):
        # Hand-written close artifact: realized P&L of exactly zero settles to
        # STOPPED with the ZERO_PNL_CLOSE reason code.
        plan = self._write_plan("plan-zero")
        state = {
            "schema_version": "paper-runner-state-1.0.0",
            "environment": "paper",
            "plans": {
                plan.plan_id: {
                    "status": "CLOSED",
                    "plan_hash": plan.plan_hash,
                    "open": {
                        "plan_id": plan.plan_id,
                        "plan_hash": plan.plan_hash,
                        "spread_id": plan.spread.spread_id,
                        "opened_at": TICK_NOW.isoformat(),
                        "entry_credit": str(plan.spread.net_credit),
                        "quantity": plan.spread.quantity,
                        "environment": "paper",
                    },
                    "close": None,
                    "escalations": [],
                }
            },
        }
        self.state_path.write_text(json.dumps(state), encoding="utf-8")
        closes = self.state_dir / "closes"
        closes.mkdir()
        artifact = {
            "schema_version": "paper-runner-state-1.0.0",
            "environment": "paper",
            "decision": {
                "human_id": "captain",
                "decided_at": CLOSED_AT.isoformat(),
                "reason_codes": ["FLAT_CLOSE"],
            },
            "close": {
                "plan_id": plan.plan_id,
                "plan_hash": plan.plan_hash,
                "closed_at": CLOSED_AT.isoformat(),
                "exit_debit": "1.00",
                "exit_commission": "0.00",
                "realized_pnl": "0.00",
                "exit_evaluation_sha256": "deadbeef",
                "close_sha256": "cafef00d",
                "environment": "paper",
            },
        }
        (closes / f"{plan.plan_id}.json").write_text(
            json.dumps(artifact), encoding="utf-8"
        )
        report = settle_paper_outcomes(
            self.state_dir, self.log_path, _provider_none, PAST_EXPIRATION
        )
        self.assertEqual(len(report["settled"]), 1)
        self.assertEqual(report["settled"][0]["outcome"], "STOPPED")
        self.assertIn("ZERO_PNL_CLOSE", report["settled"][0]["reason_codes"])
        self.assertEqual(read_log(self.log_path)[0]["outcome"], "STOPPED")

    def test_open_past_expiration_otm_expires_worthless(self):
        plan = self._open_plan("plan-otm")
        report = settle_paper_outcomes(
            self.state_dir, self.log_path, _provider_otm, PAST_EXPIRATION
        )
        self.assertEqual(len(report["settled"]), 1)
        settled = report["settled"][0]
        self.assertEqual(settled["outcome"], "EXPIRED_WORTHLESS")
        self.assertIn("SHORT_LEG_EXPIRED_OTM", settled["reason_codes"])
        entries = read_log(self.log_path)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["outcome"], "EXPIRED_WORTHLESS")
        self.assertEqual(entries[0]["provenance"]["short_intrinsic"], "0")
        self.assertEqual(entries[0]["provenance"]["underlying_close"], "100.00")
        self.assertEqual(entries[0]["premium_received"], str(plan.spread.net_credit))

    def test_open_past_expiration_itm_assigned(self):
        self._open_plan("plan-itm")
        report = settle_paper_outcomes(
            self.state_dir, self.log_path, _provider_itm, PAST_EXPIRATION
        )
        self.assertEqual(len(report["settled"]), 1)
        self.assertEqual(report["settled"][0]["outcome"], "ASSIGNED")
        self.assertIn("SHORT_LEG_EXPIRED_ITM", report["settled"][0]["reason_codes"])
        self.assertEqual(read_log(self.log_path)[0]["outcome"], "ASSIGNED")

    def test_open_past_expiration_no_data_unknown(self):
        self._open_plan("plan-unknown")
        report = settle_paper_outcomes(
            self.state_dir, self.log_path, _provider_none, PAST_EXPIRATION
        )
        self.assertEqual(report["settled"], [])
        self.assertEqual(len(report["unknown"]), 1)
        self.assertEqual(report["unknown"][0]["outcome"], "UNKNOWN")
        self.assertIn("MARKET_DATA_UNAVAILABLE", report["unknown"][0]["reason_codes"])
        self.assertEqual(read_log(self.log_path)[0]["outcome"], "UNKNOWN")
        # A later run with real data may still settle the true outcome.
        second = settle_paper_outcomes(
            self.state_dir, self.log_path, _provider_otm, PAST_EXPIRATION
        )
        self.assertEqual(len(second["settled"]), 1)
        self.assertEqual(second["settled"][0]["outcome"], "EXPIRED_WORTHLESS")

    def test_default_provider_records_unknown_fail_closed(self):
        self._open_plan("plan-default-provider")
        report = settle_paper_outcomes(
            self.state_dir, self.log_path, None, PAST_EXPIRATION
        )
        self.assertEqual(len(report["unknown"]), 1)
        self.assertEqual(report["unknown"][0]["outcome"], "UNKNOWN")

    def test_provider_exception_records_unknown(self):
        def bad_provider(plan):
            raise RuntimeError("feed down")

        self._open_plan("plan-bad-provider")
        report = settle_paper_outcomes(
            self.state_dir, self.log_path, bad_provider, PAST_EXPIRATION
        )
        self.assertEqual(len(report["unknown"]), 1)
        self.assertIn(
            "MARKET_DATA_PROVIDER_FAILED", report["unknown"][0]["reason_codes"]
        )

    def test_negative_intrinsic_is_not_guessed(self):
        def bad_data(plan):
            return {"underlying_close": Decimal("90"), "short_intrinsic": Decimal("-1")}

        self._open_plan("plan-negative-intrinsic")
        report = settle_paper_outcomes(
            self.state_dir, self.log_path, bad_data, PAST_EXPIRATION
        )
        self.assertEqual(report["unknown"][0]["outcome"], "UNKNOWN")
        self.assertIn("NEGATIVE_SHORT_INTRINSIC", report["unknown"][0]["reason_codes"])

    def test_open_before_expiration_is_skipped(self):
        self._open_plan("plan-early")
        report = settle_paper_outcomes(
            self.state_dir, self.log_path, _provider_otm, TICK_NOW
        )
        self.assertEqual(report["settled"], [])
        self.assertEqual(report["unknown"], [])
        self.assertEqual(len(report["skipped"]), 1)
        self.assertEqual(report["skipped"][0]["reason_codes"], ["NOT_AT_EXPIRATION"])
        self.assertEqual(self._log_lines(), [])

    def test_pending_plan_is_skipped(self):
        self._write_plan("plan-pending")
        advance_paper_lifecycle(self.plans_dir, self.state_path, None, TICK_NOW)
        report = settle_paper_outcomes(
            self.state_dir, self.log_path, _provider_otm, PAST_EXPIRATION
        )
        self.assertEqual(report["settled"], [])
        self.assertEqual(len(report["skipped"]), 1)
        self.assertEqual(
            report["skipped"][0]["reason_codes"], ["PLAN_NOT_OPEN_OR_CLOSED"]
        )

    def test_closed_plan_missing_artifact_is_skipped(self):
        plan = self._write_plan("plan-no-artifact")
        # Force a CLOSED state entry with no close artifact on disk.
        raw = {
            "schema_version": "paper-runner-state-1.0.0",
            "environment": "paper",
            "plans": {
                plan.plan_id: {
                    "status": "CLOSED",
                    "plan_hash": plan.plan_hash,
                    "open": None,
                    "close": None,
                    "escalations": [],
                }
            },
        }
        self.state_path.write_text(json.dumps(raw), encoding="utf-8")
        report = settle_paper_outcomes(
            self.state_dir, self.log_path, _provider_none, PAST_EXPIRATION
        )
        self.assertEqual(len(report["skipped"]), 1)
        self.assertEqual(
            report["skipped"][0]["reason_codes"], ["CLOSE_ARTIFACT_MISSING"]
        )
        self.assertEqual(self._log_lines(), [])

    def test_non_paper_state_is_refused(self):
        self.state_path.write_text(
            json.dumps(
                {
                    "schema_version": "paper-runner-state-1.0.0",
                    "environment": "live",
                    "plans": {},
                }
            ),
            encoding="utf-8",
        )
        with self.assertRaises(ValueError):
            settle_paper_outcomes(
                self.state_dir, self.log_path, _provider_none, PAST_EXPIRATION
            )

    def test_missing_state_file_is_refused(self):
        with self.assertRaises(ValueError):
            settle_paper_outcomes(
                self.state_dir, self.log_path, _provider_none, PAST_EXPIRATION
            )

    def test_naive_now_is_refused(self):
        self._open_plan("plan-naive")
        with self.assertRaises(ValueError):
            settle_paper_outcomes(
                self.state_dir, self.log_path, _provider_otm, PAST_EXPIRATION.replace(tzinfo=None)
            )


class PaperSettlerCliTests(unittest.TestCase):
    def _run_cli(self, *argv):
        return subprocess.run(
            [sys.executable, "-m", "hedge_desk.cli", *argv],
            capture_output=True, text=True, check=False,
        )

    def test_cli_paper_settle_prints_report(self):
        with tempfile.TemporaryDirectory() as directory:
            state_dir = Path(directory)
            plans_dir = state_dir / "plans"
            plans_dir.mkdir()
            plan = _approved_plan("plan-cli-settle")
            write_plan_file(plan, plans_dir / "plan-cli-settle.json")
            advance_paper_lifecycle(
                plans_dir, state_dir / "state.json", _ready_quotes, TICK_NOW
            )
            log_path = state_dir / "paper-outcomes.jsonl"
            result = self._run_cli(
                "--paper-settle",
                "--state", str(state_dir / "state.json"),
                "--paper-log", str(log_path),
                "--now", PAST_EXPIRATION.isoformat(),
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            # No market-data provider is wired on the CLI: the OPEN plan is past
            # expiration but unverifiable, so it settles UNKNOWN (never guessed).
            self.assertEqual(len(report["unknown"]), 1)
            self.assertEqual(report["unknown"][0]["outcome"], "UNKNOWN")
            self.assertEqual(report["environment"], "paper")
            entries = read_log(log_path)
            self.assertEqual(len(entries), 1)
            self.assertEqual(entries[0]["outcome"], "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
