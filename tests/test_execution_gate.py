"""Deterministic tests for the risk-gated auto-execution decision harness."""

import unittest
from datetime import datetime, timezone
from decimal import Decimal

from hedge_desk.domain import Account, AccountType, TradeCandidate, ProductType
from hedge_desk.execution_gate import (
    KillSwitch,
    build_candidate_from_structure,
    evaluate_execution,
)
from hedge_desk.release import REQUIRED_RELEASE_EVIDENCE, ReleaseEvidence


def _candidate():
    return TradeCandidate(
        candidate_id="SPY261023C00764000--SPY261023C00768000",
        symbol="SPY",
        product_type=ProductType.DEFINED_RISK_OPTION,
        quantity=1,
        entry_price=Decimal("2.247"),
        max_loss=Decimal("175.30"),
        expected_win=Decimal("224.70"),
        win_probability=Decimal("0"),
        quote_timestamp=datetime(2026, 9, 19, 15, 0, tzinfo=timezone.utc),
        average_daily_dollar_volume=Decimal("100000000"),
        thesis="Real defined-risk premium structure.",
        invalidation="Reject if gate blocks.",
    )


def _account():
    return Account(
        "acct-1", AccountType.INDIVIDUAL, Decimal("100000"), Decimal("50000"),
        options_approved=True,
    )


class ExecutionGateTests(unittest.TestCase):
    def test_kill_switch_off_blocks(self):
        d = evaluate_execution(
            candidate=_candidate(),
            account=_account(),
            evaluated_at=datetime(2026, 9, 19, 15, 30, tzinfo=timezone.utc),
            validated_risk_of_ruin_after=Decimal("0.01"),
            kill_switch=KillSwitch(armed=False),
        )
        self.assertEqual(d.decision, "BLOCKED")
        self.assertIn("KILL_SWITCH_OFF", d.reason_codes)
        self.assertFalse(d.trade_authorized)

    def test_kill_switch_on_still_blocks_without_release(self):
        d = evaluate_execution(
            candidate=_candidate(),
            account=_account(),
            evaluated_at=datetime(2026, 9, 19, 15, 30, tzinfo=timezone.utc),
            validated_risk_of_ruin_after=Decimal("0.01"),
            kill_switch=KillSwitch(armed=True),
        )
        self.assertEqual(d.decision, "BLOCKED")
        self.assertIn("LIVE_RELEASE_NOT_READY", d.reason_codes)
        self.assertFalse(d.release_ready)
        self.assertFalse(d.trade_authorized)

    def test_stale_quote_blocks_risk_gate(self):
        # Quote 2h old exceeds 900s max age.
        d = evaluate_execution(
            candidate=_candidate(),
            account=_account(),
            evaluated_at=datetime(2026, 9, 19, 17, 0, tzinfo=timezone.utc),
            validated_risk_of_ruin_after=Decimal("0.01"),
            kill_switch=KillSwitch(armed=True),
        )
        self.assertEqual(d.decision, "BLOCKED")
        self.assertIn("RISK_GATE_BLOCKED", d.reason_codes)
        self.assertIn("STALE_QUOTE", d.risk_gate_reasons)

    def test_never_authorizes_without_all_false_evidence(self):
        # Even with kill switch on and fresh quote, missing release evidence blocks.
        d = evaluate_execution(
            candidate=_candidate(),
            account=_account(),
            evaluated_at=datetime(2026, 9, 19, 15, 30, tzinfo=timezone.utc),
            validated_risk_of_ruin_after=Decimal("0.01"),
            kill_switch=KillSwitch(armed=True),
            release_evidence=tuple(
                ReleaseEvidence(r, False, "0" * 64) for r in REQUIRED_RELEASE_EVIDENCE
            ),
        )
        self.assertEqual(d.decision, "BLOCKED")
        self.assertFalse(d.trade_authorized)

    def test_absent_ror_blocks_with_risk_input_absent(self):
        # The desk rule: an agent must never substitute authoritative RoR. Without
        # a validated RoR artifact the gate must fail closed, not fabricate 0.01.
        d = evaluate_execution(
            candidate=_candidate(),
            account=_account(),
            evaluated_at=datetime(2026, 9, 19, 15, 30, tzinfo=timezone.utc),
            validated_risk_of_ruin_after=None,
            kill_switch=KillSwitch(armed=True),
        )
        self.assertEqual(d.decision, "BLOCKED")
        self.assertIn("RISK_INPUT_ABSENT", d.reason_codes)
        self.assertFalse(d.trade_authorized)

    def test_build_candidate_from_structure_requires_real_adv(self):
        structure = {
            "contract_id": "SPY261023C00764000--SPY261023C00768000",
            "underlying": "SPY",
            "net_credit_per_share": "2.247",
            "net_credit": "224.70",
            "maximum_loss": "175.30",
        }
        # Refuses to invent an ADV (honesty: no fabricated liquidity).
        with self.assertRaises(ValueError):
            build_candidate_from_structure(structure)
        cand = build_candidate_from_structure(
            structure, average_daily_dollar_volume=Decimal("5000000000")
        )
        self.assertEqual(cand.symbol, "SPY")
        self.assertEqual(cand.entry_price, Decimal("2.247"))
        self.assertEqual(cand.max_loss, Decimal("175.30"))
        self.assertEqual(cand.average_daily_dollar_volume, Decimal("5000000000"))
        self.assertEqual(cand.product_type, ProductType.DEFINED_RISK_OPTION)


if __name__ == "__main__":
    unittest.main()