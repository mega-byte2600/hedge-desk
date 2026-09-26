"""Deterministic tests for the paper lifecycle runner (Move #2)."""

import json
import subprocess
import sys
import tempfile
import unittest
from dataclasses import replace
from datetime import timedelta
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
    list_pending_escalations,
    parse_option_quote,
    write_plan_file,
)
from hedge_desk.paper.runner import (
    STATUS_CLOSED,
    STATUS_OPEN,
    STATUS_PENDING_OPEN,
    _load_state,
)

TICK_NOW = FIXTURE_AS_OF + timedelta(seconds=60)
DECIDED_AT = FIXTURE_AS_OF + timedelta(minutes=1)
CLOSED_AT = FIXTURE_AS_OF + timedelta(minutes=2)


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


def _monitor_lifecycle(plan):
    """Neutral lifecycle inputs: nothing adverse, settlement terms confirmed."""
    return {
        "short_leg_in_the_money": False,
        "ex_dividend_before_expiration": False,
        "assignment_notice_received": False,
        "contract_adjustment_pending": False,
        "settlement_terms_confirmed": True,
    }


class PaperRunnerTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.plans_dir = Path(self.directory.name) / "plans"
        self.plans_dir.mkdir()
        self.state_path = Path(self.directory.name) / "state.json"

    def _write_plan(self, plan_id):
        plan = _approved_plan(plan_id)
        write_plan_file(plan, self.plans_dir / f"{plan_id}.json")
        return plan

    def test_tick_opens_when_fill_ready(self) -> None:
        plan = self._write_plan("plan-open-ready")
        report = advance_paper_lifecycle(
            self.plans_dir, self.state_path, _ready_quotes, TICK_NOW
        )
        self.assertEqual(len(report["opened"]), 1)
        self.assertEqual(report["opened"][0]["plan_id"], plan.plan_id)
        self.assertEqual(report["opened"][0]["plan_hash"], plan.plan_hash)
        self.assertEqual(report["still_pending"], [])
        state = _load_state(self.state_path)
        entry = state["plans"][plan.plan_id]
        self.assertEqual(entry["status"], STATUS_OPEN)
        self.assertEqual(entry["open"]["plan_hash"], plan.plan_hash)
        self.assertEqual(entry["open"]["opened_at"], TICK_NOW.isoformat())

    def test_pending_plan_is_not_considered(self) -> None:
        plan = build_reference_plan()
        write_plan_file(plan, self.plans_dir / f"{plan.plan_id}.json")
        report = advance_paper_lifecycle(
            self.plans_dir, self.state_path, _ready_quotes, TICK_NOW
        )
        self.assertEqual(report["opened"], [])
        self.assertNotIn(plan.plan_id, _load_state(self.state_path)["plans"])

    def test_stale_quotes_stay_pending_with_stale_quote(self) -> None:
        plan = self._write_plan("plan-stale")
        stale_now = FIXTURE_AS_OF + timedelta(seconds=121)
        report = advance_paper_lifecycle(
            self.plans_dir, self.state_path, _ready_quotes, stale_now
        )
        self.assertEqual(report["opened"], [])
        self.assertEqual(len(report["still_pending"]), 1)
        self.assertIn("STALE_QUOTE", report["still_pending"][0]["reason_codes"])
        entry = _load_state(self.state_path)["plans"][plan.plan_id]
        self.assertEqual(entry["status"], STATUS_PENDING_OPEN)

    def test_default_quotes_provider_stays_pending_fail_closed(self) -> None:
        plan = self._write_plan("plan-no-provider")
        report = advance_paper_lifecycle(self.plans_dir, self.state_path, now=TICK_NOW)
        self.assertEqual(report["opened"], [])
        codes = report["still_pending"][0]["reason_codes"]
        self.assertIn("QUOTE_UNAVAILABLE", codes)
        self.assertIn("INSUFFICIENT_COMBO_SIZE", codes)
        self.assertEqual(
            _load_state(self.state_path)["plans"][plan.plan_id]["status"],
            STATUS_PENDING_OPEN,
        )

    def test_insufficient_size_and_worse_credit_stay_pending(self) -> None:
        plan = self._write_plan("plan-bad-fill")

        def thin(plan):
            return (0, plan.spread.net_credit)

        report = advance_paper_lifecycle(self.plans_dir, self.state_path, thin, TICK_NOW)
        codes = report["still_pending"][0]["reason_codes"]
        self.assertIn("INSUFFICIENT_COMBO_SIZE", codes)

        def worse(plan):
            return (plan.spread.quantity, plan.spread.net_credit - Decimal("0.01"))

        report = advance_paper_lifecycle(self.plans_dir, self.state_path, worse, TICK_NOW)
        codes = report["still_pending"][0]["reason_codes"]
        self.assertIn("APPROVED_CREDIT_NOT_AVAILABLE", codes)

    def test_expired_approval_stays_pending_fail_closed(self) -> None:
        plan = self._write_plan("plan-expired")
        late = plan.approval_expires_at + timedelta(seconds=1)
        report = advance_paper_lifecycle(
            self.plans_dir, self.state_path, _ready_quotes, late
        )
        self.assertEqual(report["opened"], [])
        self.assertEqual(
            report["still_pending"][0]["reason_codes"], ["APPROVAL_EXPIRED"]
        )
        self.assertEqual(
            _load_state(self.state_path)["plans"][plan.plan_id]["status"],
            STATUS_PENDING_OPEN,
        )

    def test_lifecycle_monitor_stays_open(self) -> None:
        plan = self._write_plan("plan-monitor")
        advance_paper_lifecycle(self.plans_dir, self.state_path, _ready_quotes, TICK_NOW)
        later = TICK_NOW + timedelta(seconds=120)
        report = advance_paper_lifecycle(
            self.plans_dir,
            self.state_path,
            _ready_quotes,
            later,
            lifecycle_provider=_monitor_lifecycle,
        )
        self.assertEqual(report["opened"], [])
        self.assertEqual(len(report["monitoring"]), 1)
        self.assertEqual(report["monitoring"][0]["plan_id"], plan.plan_id)
        self.assertEqual(report["escalated"], [])
        self.assertEqual(
            _load_state(self.state_path)["plans"][plan.plan_id]["status"],
            STATUS_OPEN,
        )

    def test_default_lifecycle_provider_fails_closed_on_unconfirmed_terms(self) -> None:
        self._write_plan("plan-default-lifecycle")
        advance_paper_lifecycle(self.plans_dir, self.state_path, _ready_quotes, TICK_NOW)
        report = advance_paper_lifecycle(
            self.plans_dir,
            self.state_path,
            _ready_quotes,
            TICK_NOW + timedelta(seconds=120),
        )
        self.assertEqual(report["monitoring"], [])
        self.assertEqual(len(report["escalated"]), 1)
        self.assertEqual(report["escalated"][0]["action"], "BLOCK_AND_ESCALATE")
        self.assertIn(
            "SETTLEMENT_TERMS_UNCONFIRMED",
            report["escalated"][0]["reason_codes"],
        )

    def test_close_review_required_escalates_and_never_auto_closes(self) -> None:
        plan = self._write_plan("plan-close-review")
        advance_paper_lifecycle(self.plans_dir, self.state_path, _ready_quotes, TICK_NOW)

        def early_assignment(plan):
            return {
                "short_leg_in_the_money": True,
                "ex_dividend_before_expiration": True,
                "assignment_notice_received": False,
                "contract_adjustment_pending": False,
                "settlement_terms_confirmed": True,
            }

        report = advance_paper_lifecycle(
            self.plans_dir,
            self.state_path,
            _ready_quotes,
            TICK_NOW + timedelta(seconds=120),
            lifecycle_provider=early_assignment,
        )
        self.assertEqual(len(report["escalated"]), 1)
        escalated = report["escalated"][0]
        self.assertEqual(escalated["action"], "CLOSE_REVIEW_REQUIRED")
        self.assertIn("EARLY_ASSIGNMENT_RISK", escalated["reason_codes"])
        entry = _load_state(self.state_path)["plans"][plan.plan_id]
        self.assertEqual(entry["status"], STATUS_OPEN)
        self.assertIsNone(entry["close"])
        self.assertEqual(len(entry["escalations"]), 1)
        self.assertEqual(entry["escalations"][0]["status"], "PENDING_HUMAN")
        closes_dir = self.state_path.parent / "closes"
        self.assertFalse((closes_dir / f"{plan.plan_id}.json").exists())

    def test_block_and_escalate_escalates_and_never_auto_closes(self) -> None:
        plan = self._write_plan("plan-block")
        advance_paper_lifecycle(self.plans_dir, self.state_path, _ready_quotes, TICK_NOW)

        def contract_terms(plan):
            return {
                "short_leg_in_the_money": False,
                "ex_dividend_before_expiration": False,
                "assignment_notice_received": False,
                "contract_adjustment_pending": True,
                "settlement_terms_confirmed": False,
            }

        report = advance_paper_lifecycle(
            self.plans_dir,
            self.state_path,
            _ready_quotes,
            TICK_NOW + timedelta(seconds=120),
            lifecycle_provider=contract_terms,
        )
        self.assertEqual(len(report["escalated"]), 1)
        escalated = report["escalated"][0]
        self.assertEqual(escalated["action"], "BLOCK_AND_ESCALATE")
        self.assertIn("CONTRACT_ADJUSTMENT_PENDING", escalated["reason_codes"])
        entry = _load_state(self.state_path)["plans"][plan.plan_id]
        self.assertEqual(entry["status"], STATUS_OPEN)
        self.assertIsNone(entry["close"])

    def test_escalation_manifest_is_written_for_humans(self) -> None:
        self.test_close_review_required_escalates_and_never_auto_closes()
        manifest_path = self.state_path.parent / "escalations.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(manifest["environment"], "paper")
        self.assertIn("plan-close-review", manifest["escalations"])
        pending = list_pending_escalations(self.state_path)
        self.assertEqual(len(pending["pending_escalations"]), 1)
        self.assertEqual(pending["pending_escalations"][0]["plan_id"], "plan-close-review")

    def test_assignment_reconciliation_escalates(self) -> None:
        plan = self._write_plan("plan-assignment")
        advance_paper_lifecycle(self.plans_dir, self.state_path, _ready_quotes, TICK_NOW)

        def assigned(plan):
            return {
                "short_leg_in_the_money": False,
                "ex_dividend_before_expiration": False,
                "assignment_notice_received": True,
                "contract_adjustment_pending": False,
                "settlement_terms_confirmed": True,
            }

        report = advance_paper_lifecycle(
            self.plans_dir,
            self.state_path,
            _ready_quotes,
            TICK_NOW + timedelta(seconds=120),
            lifecycle_provider=assigned,
        )
        self.assertEqual(report["escalated"][0]["action"], "ASSIGNMENT_RECONCILIATION_REQUIRED")
        self.assertEqual(
            _load_state(self.state_path)["plans"][plan.plan_id]["status"],
            STATUS_OPEN,
        )


class PaperCloseTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.plans_dir = Path(self.directory.name) / "plans"
        self.plans_dir.mkdir()
        self.state_path = Path(self.directory.name) / "state.json"

    def _open_plan(self, plan_id="plan-close"):
        plan = _approved_plan(plan_id)
        write_plan_file(plan, self.plans_dir / f"{plan_id}.json")
        advance_paper_lifecycle(self.plans_dir, self.state_path, _ready_quotes, TICK_NOW)
        return plan

    def _exit_quotes(self, closed_at):
        snapshot = build_reference_option_snapshot()
        short = replace(
            snapshot.option_quotes[0],
            bid=Decimal("0.40"), ask=Decimal("0.50"), quoted_at=closed_at,
        )
        long = replace(
            snapshot.option_quotes[1],
            bid=Decimal("0.10"), ask=Decimal("0.20"), quoted_at=closed_at,
        )
        return short, long

    def test_human_close_happy_path_records_reason_codes(self) -> None:
        plan = self._open_plan()
        short, long = self._exit_quotes(CLOSED_AT)
        result = close_paper_position(
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
        self.assertEqual(result["status"], "closed")
        self.assertEqual(result["human_id"], "captain")
        self.assertEqual(result["reason_codes"], ["PROFIT_TARGET_REACHED"])
        self.assertEqual(result["exit_debit"], "40.00")
        self.assertEqual(result["exit_commission"], "1.30")
        self.assertEqual(result["realized_pnl"], "77.40")
        self.assertEqual(result["environment"], "paper")
        entry = _load_state(self.state_path)["plans"][plan.plan_id]
        self.assertEqual(entry["status"], STATUS_CLOSED)
        self.assertEqual(entry["close_decision"]["human_id"], "captain")
        self.assertEqual(entry["close_decision"]["reason_codes"], ["PROFIT_TARGET_REACHED"])
        artifact_path = Path(result["close_artifact"])
        self.assertTrue(artifact_path.exists())
        artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
        self.assertEqual(artifact["environment"], "paper")
        self.assertEqual(artifact["close"]["realized_pnl"], "77.40")
        self.assertEqual(artifact["decision"]["reason_codes"], ["PROFIT_TARGET_REACHED"])

    def test_close_of_non_open_plan_is_refused(self) -> None:
        plan = self._write_plan_pending("plan-never-opened")
        # A tick runs (stays pending: no quotes provider) so the plan has a
        # PENDING_OPEN lifecycle entry; the human close still refuses.
        advance_paper_lifecycle(self.plans_dir, self.state_path, now=TICK_NOW)
        short, long = self._exit_quotes(CLOSED_AT)
        with self.assertRaisesRegex(PermissionError, "only an OPEN"):
            close_paper_position(
                self.plans_dir, self.state_path, plan.plan_id,
                "captain", CLOSED_AT, ("NO_THESIS",), short, long, Decimal("0.65"),
            )

    def _write_plan_pending(self, plan_id):
        plan = _approved_plan(plan_id)
        write_plan_file(plan, self.plans_dir / f"{plan_id}.json")
        return plan

    def test_close_of_unknown_plan_is_refused(self) -> None:
        short, long = self._exit_quotes(CLOSED_AT)
        with self.assertRaisesRegex(ValueError, "no paper plan file"):
            close_paper_position(
                self.plans_dir, self.state_path, "no-such-plan",
                "captain", CLOSED_AT, ("NO_THESIS",), short, long, Decimal("0.65"),
            )

    def test_double_close_is_refused(self) -> None:
        plan = self._open_plan()
        short, long = self._exit_quotes(CLOSED_AT)
        close_paper_position(
            self.plans_dir, self.state_path, plan.plan_id,
            "captain", CLOSED_AT, ("PROFIT_TARGET_REACHED",), short, long, Decimal("0.65"),
        )
        later = CLOSED_AT + timedelta(minutes=5)
        short2, long2 = self._exit_quotes(later)
        with self.assertRaisesRegex(PermissionError, "only an OPEN"):
            close_paper_position(
                self.plans_dir, self.state_path, plan.plan_id,
                "captain", later, ("AGAIN",), short2, long2, Decimal("0.65"),
            )

    def test_close_requires_human_identity_timestamp_and_reason_codes(self) -> None:
        plan = self._open_plan()
        short, long = self._exit_quotes(CLOSED_AT)
        with self.assertRaisesRegex(ValueError, "human identity"):
            close_paper_position(
                self.plans_dir, self.state_path, plan.plan_id,
                "  ", CLOSED_AT, ("NO_THESIS",), short, long, Decimal("0.65"),
            )
        naive = CLOSED_AT.replace(tzinfo=None)
        with self.assertRaisesRegex(ValueError, "timezone-aware"):
            close_paper_position(
                self.plans_dir, self.state_path, plan.plan_id,
                "captain", naive, ("NO_THESIS",), short, long, Decimal("0.65"),
            )
        with self.assertRaisesRegex(ValueError, "reason code"):
            close_paper_position(
                self.plans_dir, self.state_path, plan.plan_id,
                "captain", CLOSED_AT, (), short, long, Decimal("0.65"),
            )

    def test_double_open_is_refused_second_tick_does_not_reopen(self) -> None:
        plan = self._open_plan()
        later = TICK_NOW + timedelta(seconds=120)
        report = advance_paper_lifecycle(
            self.plans_dir,
            self.state_path,
            _ready_quotes,
            later,
            lifecycle_provider=_monitor_lifecycle,
        )
        self.assertEqual(report["opened"], [])
        self.assertEqual(len(report["monitoring"]), 1)
        entry = _load_state(self.state_path)["plans"][plan.plan_id]
        self.assertEqual(entry["open"]["opened_at"], TICK_NOW.isoformat())

    def test_state_refuses_non_paper_environment(self) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
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
        with self.assertRaisesRegex(ValueError, "non-paper"):
            _load_state(self.state_path)

    def test_parse_option_quote_round_trip(self) -> None:
        snapshot = build_reference_option_snapshot()
        quote = snapshot.option_quotes[0]
        payload = {
            "contract_id": quote.contract_id,
            "underlying": quote.underlying,
            "option_type": quote.option_type.value,
            "strike": str(quote.strike),
            "expiration": quote.expiration.isoformat(),
            "bid": str(quote.bid),
            "ask": str(quote.ask),
            "bid_size": quote.bid_size,
            "ask_size": quote.ask_size,
            "quoted_at": quote.quoted_at.isoformat(),
            "source_id": quote.source_id,
            "open_interest": quote.open_interest,
            "volume": quote.volume,
        }
        self.assertEqual(parse_option_quote(payload), quote)


class PaperRunnerCliTests(unittest.TestCase):
    def _run_cli(self, *argv):
        return subprocess.run(
            [sys.executable, "-m", "hedge_desk.cli", *argv],
            capture_output=True, text=True, check=False,
        )

    def test_cli_tick_is_noop_on_missing_plans_dir(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            state = Path(directory) / "paper" / "state.json"
            result = self._run_cli(
                "--paper-tick",
                "--plans-dir", str(Path(directory) / "paper" / "plans"),
                "--state", str(state),
                "--now", TICK_NOW.isoformat(),
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["opened"], [])
        self.assertEqual(report["still_pending"], [])
        self.assertEqual(report["monitoring"], [])
        self.assertEqual(report["escalated"], [])
        self.assertEqual(report["environment"], "paper")
        self.assertFalse(state.exists())

    def test_cli_tick_is_noop_on_empty_plans_dir(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            plans_dir = Path(directory) / "plans"
            plans_dir.mkdir()
            state = Path(directory) / "state.json"
            result = self._run_cli(
                "--paper-tick",
                "--plans-dir", str(plans_dir),
                "--state", str(state),
                "--now", TICK_NOW.isoformat(),
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["opened"], [])
        self.assertFalse(state.exists())

    def test_cli_tick_requires_plans_dir_and_state(self) -> None:
        result = self._run_cli("--paper-tick")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--plans-dir", result.stderr)

    def test_cli_tick_requires_tz_aware_now(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = self._run_cli(
                "--paper-tick",
                "--plans-dir", directory,
                "--state", str(Path(directory) / "state.json"),
                "--now", "2026-07-28T20:01:00",
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("timezone-aware", result.stderr)

    def test_cli_close_happy_path_and_escalations_listing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            plans_dir = directory / "plans"
            plans_dir.mkdir()
            state = directory / "state.json"
            plan = _approved_plan("plan-cli-close")
            write_plan_file(plan, plans_dir / "plan-cli-close.json")
            tick = self._run_cli(
                "--paper-tick",
                "--plans-dir", str(plans_dir),
                "--state", str(state),
                "--now", TICK_NOW.isoformat(),
            )
            self.assertEqual(tick.returncode, 0, tick.stderr)
            # Bare CI tick ships no quotes provider: stays pending, no opens.
            self.assertEqual(json.loads(tick.stdout)["opened"], [])

            snapshot = build_reference_option_snapshot()
            quotes = {
                "short": {
                    "contract_id": snapshot.option_quotes[0].contract_id,
                    "underlying": snapshot.option_quotes[0].underlying,
                    "option_type": snapshot.option_quotes[0].option_type.value,
                    "strike": str(snapshot.option_quotes[0].strike),
                    "expiration": snapshot.option_quotes[0].expiration.isoformat(),
                    "bid": "0.40",
                    "ask": "0.50",
                    "bid_size": snapshot.option_quotes[0].bid_size,
                    "ask_size": snapshot.option_quotes[0].ask_size,
                    "quoted_at": CLOSED_AT.isoformat(),
                    "source_id": snapshot.option_quotes[0].source_id,
                    "open_interest": snapshot.option_quotes[0].open_interest,
                    "volume": snapshot.option_quotes[0].volume,
                },
                "long": {
                    "contract_id": snapshot.option_quotes[1].contract_id,
                    "underlying": snapshot.option_quotes[1].underlying,
                    "option_type": snapshot.option_quotes[1].option_type.value,
                    "strike": str(snapshot.option_quotes[1].strike),
                    "expiration": snapshot.option_quotes[1].expiration.isoformat(),
                    "bid": "0.10",
                    "ask": "0.20",
                    "bid_size": snapshot.option_quotes[1].bid_size,
                    "ask_size": snapshot.option_quotes[1].ask_size,
                    "quoted_at": CLOSED_AT.isoformat(),
                    "source_id": snapshot.option_quotes[1].source_id,
                    "open_interest": snapshot.option_quotes[1].open_interest,
                    "volume": snapshot.option_quotes[1].volume,
                },
            }
            quotes_file = directory / "quotes.json"
            quotes_file.write_text(json.dumps(quotes), encoding="utf-8")
            # Close is refused while still pending — open it first through a
            # library tick with an injected provider, then close via CLI.
            def _ready(plan):
                return (plan.spread.quantity, plan.spread.net_credit)

            from hedge_desk.paper.runner import advance_paper_lifecycle as _tick

            _tick(plans_dir, state, _ready, TICK_NOW)
            close = self._run_cli(
                "--paper-close", plan.plan_id,
                "--plans-dir", str(plans_dir),
                "--state", str(state),
                "--human-id", "captain",
                "--decided-at", CLOSED_AT.isoformat(),
                "--reason-codes", "PROFIT_TARGET_REACHED,MANUAL_REVIEW",
                "--quotes-json", str(quotes_file),
                "--exit-commission-per-contract", "0.65",
            )
            self.assertEqual(close.returncode, 0, close.stderr)
            closed = json.loads(close.stdout)
            self.assertEqual(closed["status"], "closed")
            self.assertEqual(closed["reason_codes"], ["PROFIT_TARGET_REACHED", "MANUAL_REVIEW"])
            self.assertEqual(closed["realized_pnl"], "77.40")
            self.assertTrue(Path(closed["close_artifact"]).exists())

    def test_cli_close_requires_quotes_and_reason_codes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = self._run_cli(
                "--paper-close", "plan-x",
                "--plans-dir", directory,
                "--state", str(Path(directory) / "state.json"),
                "--human-id", "captain",
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--quotes-json", result.stderr)

    def test_cli_escalations_lists_pending_human_escalations(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            plans_dir = directory / "plans"
            plans_dir.mkdir()
            state = directory / "state.json"
            plan = _approved_plan("plan-cli-escalate")
            write_plan_file(plan, plans_dir / "plan-cli-escalate.json")
            result = self._run_cli(
                "--paper-escalations",
                "--state", str(state),
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        pending = json.loads(result.stdout)["pending_escalations"]
        self.assertEqual(pending, [])


if __name__ == "__main__":
    unittest.main()
