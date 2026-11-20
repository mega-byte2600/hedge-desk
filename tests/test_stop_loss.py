"""Enforced stop-loss (ADR-0008): deterministic rules, runner auto-close, C5 gates.

Reference plan economics (hedge_desk.demo): net credit 118.70, max loss 381.30,
1 contract x 100, close commission 0.65 x 2 legs = 1.30.
"""

import json
import tempfile
import unittest
from dataclasses import replace
from datetime import timedelta
from decimal import Decimal
from pathlib import Path

from hedge_desk.compliance.account_gate import account_gate
from hedge_desk.demo import FIXTURE_AS_OF, build_reference_option_snapshot, build_reference_plan
from hedge_desk.domain import Account, AccountType, ProductType, TradeCandidate
from hedge_desk.paper import (
    advance_paper_lifecycle,
    approve_paper_trade,
    create_paper_trade_plan,
    write_plan_file,
)
from hedge_desk.paper.runner import STATUS_CLOSED, STATUS_OPEN, _load_state
from hedge_desk.paper.settler import settle_paper_outcomes
from hedge_desk.risk.ruin import RiskPolicy, risk_gate
from hedge_desk.risk.stop_loss import (
    BASIS_DEFINED_RISK,
    BASIS_STOP_DEFINED,
    EQUITY_UNCONFIGURED,
    GAP_RISK_NOT_GUARANTEED,
    StopLossPolicy,
    defined_risk_stop_rule,
    stop_defined_rule,
    stop_triggered,
)

OPEN_TICK = FIXTURE_AS_OF + timedelta(seconds=60)
DECIDED_AT = FIXTURE_AS_OF + timedelta(minutes=1)
MARK_TICK = FIXTURE_AS_OF + timedelta(minutes=5)


# --- pure rules ------------------------------------------------------------------

class StopRuleTests(unittest.TestCase):
    def test_defined_risk_stop_is_half_of_max_loss_without_equity(self):
        rule = defined_risk_stop_rule(Decimal("381.30"), None)
        self.assertEqual(rule.trigger_loss, Decimal("190.65"))
        self.assertEqual(rule.basis, BASIS_DEFINED_RISK)
        self.assertIn(EQUITY_UNCONFIGURED, rule.flags)

    def test_defined_risk_stop_is_capped_at_two_percent_of_equity(self):
        # 2% of 5,000 = 100 < 190.65
        rule = defined_risk_stop_rule(Decimal("381.30"), Decimal("5000"))
        self.assertEqual(rule.trigger_loss, Decimal("100.00"))
        self.assertEqual(rule.flags, ())

    def test_large_equity_keeps_policy_fraction(self):
        rule = defined_risk_stop_rule(Decimal("381.30"), Decimal("100000"))
        self.assertEqual(rule.trigger_loss, Decimal("190.65"))

    def test_trigger_is_inclusive(self):
        rule = defined_risk_stop_rule(Decimal("200"), None)  # trigger 100.00
        self.assertTrue(stop_triggered(Decimal("-100.00"), rule))
        self.assertFalse(stop_triggered(Decimal("-99.99"), rule))
        self.assertFalse(stop_triggered(Decimal("50"), rule))

    def test_policy_fraction_bounds(self):
        with self.assertRaises(ValueError):
            StopLossPolicy(stop_fraction_of_max_loss=Decimal("0"))
        with self.assertRaises(ValueError):
            StopLossPolicy(stop_fraction_of_max_loss=Decimal("1.01"))

    def test_undefined_risk_requires_stop_and_equity(self):
        rule, reasons = stop_defined_rule(None, None)
        self.assertIsNone(rule)
        self.assertEqual(reasons, ("EQUITY_REQUIRED_FOR_STOP_DEFINED_RISK", "STOP_LOSS_REQUIRED"))

    def test_undefined_risk_stop_must_fit_two_percent(self):
        rule, reasons = stop_defined_rule(Decimal("201"), Decimal("10000"))
        self.assertIsNone(rule)
        self.assertEqual(reasons, ("STOP_LOSS_EXCEEDS_2PCT_EQUITY",))

    def test_undefined_risk_valid_stop_carries_gap_risk_flag(self):
        rule, reasons = stop_defined_rule(Decimal("200"), Decimal("10000"))
        self.assertEqual(reasons, ())
        self.assertEqual(rule.basis, BASIS_STOP_DEFINED)
        self.assertEqual(rule.trigger_loss, Decimal("200.00"))
        self.assertIn(GAP_RISK_NOT_GUARANTEED, rule.flags)


# --- runner: enforced auto-close ----------------------------------------------------

def _approved_plan(plan_id):
    base = build_reference_plan()
    plan = create_paper_trade_plan(
        plan_id, base.spread, base.risk_decision, base.compliance_decision,
        base.created_at, base.approval_expires_at,
        event_calendar_gate=base.event_calendar_gate,
    )
    return approve_paper_trade(plan, "captain", DECIDED_AT)


def _monitor_lifecycle(plan):
    return {
        "short_leg_in_the_money": False,
        "ex_dividend_before_expiration": False,
        "assignment_notice_received": False,
        "contract_adjustment_pending": False,
        "settlement_terms_confirmed": True,
    }


def _marks(short_ask, long_bid, at=MARK_TICK):
    snapshot = build_reference_option_snapshot()

    def provider(plan):
        short = replace(snapshot.option_quotes[0], bid=short_ask - Decimal("0.10"),
                        ask=short_ask, quoted_at=at)
        long = replace(snapshot.option_quotes[1], bid=long_bid,
                       ask=long_bid + Decimal("0.10"), quoted_at=at)
        return short, long

    return provider


class RunnerStopLossTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.plans = root / "plans"
        self.plans.mkdir()
        self.state = root / "state.json"
        self.plan = _approved_plan("plan-stop")
        write_plan_file(self.plan, self.plans / "plan-stop.json")
        advance_paper_lifecycle(
            self.plans, self.state,
            lambda p: (p.spread.quantity, p.spread.net_credit), OPEN_TICK,
        )
        self.assertEqual(_load_state(self.state)["plans"]["plan-stop"]["status"], STATUS_OPEN)

    def _tick(self, marks, equity=None):
        return advance_paper_lifecycle(
            self.plans, self.state, None, MARK_TICK, _monitor_lifecycle,
            marks_provider=marks, account_equity=equity,
        )

    def test_stop_triggers_auto_close_in_paper(self):
        # debit (3.60 - 0.40) x 100 = 320; P&L = 118.70 - 320 - 1.30 = -202.60 <= -190.65
        report = self._tick(_marks(Decimal("3.60"), Decimal("0.40")))
        self.assertEqual(len(report["stopped_out"]), 1)
        hit = report["stopped_out"][0]
        self.assertEqual(hit["reason_codes"], ["STOP_LOSS_ENFORCED"])
        self.assertEqual(hit["realized_pnl"], "-202.60")
        self.assertEqual(hit["trigger_loss"], "190.65")
        entry = _load_state(self.state)["plans"]["plan-stop"]
        self.assertEqual(entry["status"], STATUS_CLOSED)
        self.assertEqual(entry["close_decision"]["actor"], "STOP_LOSS_ENFORCER")
        self.assertIsNone(entry["close_decision"]["human_id"])
        artifact = json.loads((self.state.parent / "closes" / "plan-stop.json").read_text())
        self.assertEqual(artifact["environment"], "paper")

    def test_two_percent_equity_cap_tightens_the_stop(self):
        # equity 5,000 -> stop 100. Debit 2.60-0.40 = 220; P&L = -102.60 -> triggers.
        report = self._tick(_marks(Decimal("2.60"), Decimal("0.40")), equity=Decimal("5000"))
        self.assertEqual(report["stopped_out"][0]["trigger_loss"], "100.00")

    def test_same_loss_without_cap_does_not_trigger(self):
        report = self._tick(_marks(Decimal("2.60"), Decimal("0.40")))  # -102.60 > -190.65
        self.assertEqual(report["stopped_out"], [])
        self.assertEqual(_load_state(self.state)["plans"]["plan-stop"]["status"], STATUS_OPEN)

    def test_profitable_mark_keeps_position_open(self):
        report = self._tick(_marks(Decimal("0.50"), Decimal("0.10")))
        self.assertEqual(report["stopped_out"], [])
        self.assertEqual(report["stop_unmonitored"], [])

    def test_missing_marks_are_reported_not_silent(self):
        report = self._tick(None)
        self.assertEqual(report["stop_unmonitored"][0]["reason_codes"], ["STOP_MARKS_PROVIDER_ABSENT"])
        self.assertEqual(_load_state(self.state)["plans"]["plan-stop"]["status"], STATUS_OPEN)

    def test_failing_marks_provider_is_reported(self):
        def boom(plan):
            raise RuntimeError("feed down")

        report = self._tick(boom)
        self.assertEqual(report["stop_unmonitored"][0]["reason_codes"], ["STOP_MARK_UNAVAILABLE"])

    def test_stale_marks_never_trigger_a_close(self):
        stale = _marks(Decimal("3.60"), Decimal("0.40"), at=MARK_TICK - timedelta(minutes=10))
        report = self._tick(stale)
        self.assertEqual(report["stopped_out"], [])
        self.assertEqual(report["stop_unmonitored"][0]["reason_codes"], ["STOP_MARK_REJECTED"])
        self.assertEqual(_load_state(self.state)["plans"]["plan-stop"]["status"], STATUS_OPEN)

    def test_settler_logs_stop_close_with_truthful_provenance(self):
        self._tick(_marks(Decimal("3.60"), Decimal("0.40")))
        log = self.state.parent / "paper_log.jsonl"
        settle_paper_outcomes(self.state.parent, log, now=MARK_TICK + timedelta(minutes=1))
        lines = [json.loads(x) for x in log.read_text().splitlines() if x.strip()]
        text = json.dumps(lines)
        self.assertIn("enforced-stop-loss-paper-close", text)
        self.assertIn("STOP_LOSS_ENFORCER", text)


# --- C5 gates ---------------------------------------------------------------------

def _account(equity="10000"):
    return Account(
        "paper-1", AccountType.INDIVIDUAL, Decimal(equity), Decimal(equity),
        options_approved=True, futures_approved=True,
        options_disclosure_version="odd-2024",
        options_disclosure_acknowledged_at=FIXTURE_AS_OF - timedelta(days=1),
        broker_options_policy_version="broker-2026",
    )


def _candidate(product, stop=None, max_loss="0"):
    return TradeCandidate(
        "c-1", "TEST", product, 1, Decimal("100"), Decimal(max_loss), Decimal("50"),
        Decimal("0.5"), FIXTURE_AS_OF, Decimal("5000000"), "thesis", "invalidation",
        stop_loss_amount=None if stop is None else Decimal(stop),
    )


class C5GateTests(unittest.TestCase):
    def test_naked_option_without_stop_stays_prohibited(self):
        reasons = account_gate(_account(), _candidate(ProductType.UNDEFINED_RISK_OPTION))
        self.assertIn("UNDEFINED_RISK_OPTION_PROHIBITED", reasons)
        self.assertIn("STOP_LOSS_REQUIRED", reasons)

    def test_naked_option_with_stop_within_two_percent_passes_account_gate(self):
        reasons = account_gate(_account(), _candidate(ProductType.UNDEFINED_RISK_OPTION, stop="200"))
        self.assertEqual(reasons, [])

    def test_naked_option_with_stop_over_two_percent_is_blocked(self):
        reasons = account_gate(_account(), _candidate(ProductType.UNDEFINED_RISK_OPTION, stop="201"))
        self.assertIn("STOP_LOSS_EXCEEDS_2PCT_EQUITY", reasons)
        self.assertIn("UNDEFINED_RISK_OPTION_PROHIBITED", reasons)

    def test_future_requires_stop(self):
        self.assertIn("STOP_LOSS_REQUIRED", account_gate(_account(), _candidate(ProductType.FUTURE)))
        self.assertEqual(account_gate(_account(), _candidate(ProductType.FUTURE, stop="150")), [])

    def test_risk_gate_measures_undefined_risk_at_the_stop(self):
        policy = RiskPolicy()
        ok = risk_gate(_account(), _candidate(ProductType.FUTURE, stop="200"), FIXTURE_AS_OF, policy, Decimal("0"))
        self.assertNotIn("MAX_LOSS_UNDEFINED", ok)
        self.assertNotIn("SINGLE_TRADE_LOSS_LIMIT", ok)
        over = risk_gate(_account(), _candidate(ProductType.FUTURE, stop="250"), FIXTURE_AS_OF, policy, Decimal("0"))
        self.assertIn("SINGLE_TRADE_LOSS_LIMIT", over)
        missing = risk_gate(_account(), _candidate(ProductType.FUTURE), FIXTURE_AS_OF, policy, Decimal("0"))
        self.assertIn("STOP_LOSS_REQUIRED", missing)
        self.assertIn("MAX_LOSS_UNDEFINED", missing)

    def test_invalid_stop_amount_rejected_at_construction(self):
        with self.assertRaises(ValueError):
            _candidate(ProductType.FUTURE, stop="-5")


if __name__ == "__main__":
    unittest.main()
