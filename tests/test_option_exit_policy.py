from dataclasses import replace
from datetime import timedelta
from decimal import Decimal
import unittest

from hedge_desk.demo import FIXTURE_AS_OF, build_reference_option_snapshot, build_reference_plan
from hedge_desk.options import PremiumExitPolicy, evaluate_premium_exit


class PremiumExitPolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.spread = build_reference_plan().spread
        snapshot = build_reference_option_snapshot()
        self.short = snapshot.option_quotes[0]
        self.long = snapshot.option_quotes[1]
        self.now = FIXTURE_AS_OF + timedelta(days=1)

    def quotes(self, short_bid="0.80", short_ask="0.90", long_bid="0.40", long_ask="0.50"):
        return (
            replace(
                self.short,
                bid=Decimal(short_bid),
                ask=Decimal(short_ask),
                quoted_at=self.now,
            ),
            replace(
                self.long,
                bid=Decimal(long_bid),
                ask=Decimal(long_ask),
                quoted_at=self.now,
            ),
        )

    def test_executable_profit_capture_requires_close_review_not_trade(self) -> None:
        short, long = self.quotes()
        result = evaluate_premium_exit(
            self.spread, short, long, self.now, Decimal("0.65")
        )
        self.assertEqual(result.executable_close_debit, Decimal("50.00"))
        self.assertEqual(result.marked_pnl, Decimal("67.40"))
        self.assertEqual(result.action, "CLOSE_REVIEW_REQUIRED")
        self.assertIn("PROFIT_CAPTURE_TARGET_REACHED", result.reason_codes)
        self.assertFalse(result.trade_authorized)
        self.assertEqual(len(result.artifact_sha256), 64)

    def test_loss_threshold_event_and_exit_window_all_escalate(self) -> None:
        short, long = self.quotes("4.40", "4.50", "0.40", "0.50")
        result = evaluate_premium_exit(
            self.spread,
            short,
            long,
            self.now,
            Decimal("0.65"),
            event_escalation_required=True,
        )
        self.assertIn("EVENT_ESCALATION_REQUIRED", result.reason_codes)
        self.assertIn("LOSS_REVIEW_THRESHOLD_REACHED", result.reason_codes)
        near_exit = self.spread.expiration_date - timedelta(days=7)
        short, long = (
            replace(short, quoted_at=self.now.replace(
                year=near_exit.year, month=near_exit.month, day=near_exit.day
            )),
            replace(long, quoted_at=self.now.replace(
                year=near_exit.year, month=near_exit.month, day=near_exit.day
            )),
        )
        result = evaluate_premium_exit(
            self.spread, short, long, short.quoted_at, Decimal("0.65")
        )
        self.assertIn("PLANNED_EXIT_WINDOW_REACHED", result.reason_codes)

    def test_unreached_threshold_monitors_and_timing_fails_closed(self) -> None:
        short, long = self.quotes("1.20", "1.30", "0.60", "0.70")
        result = evaluate_premium_exit(
            self.spread, short, long, self.now, Decimal("0.65")
        )
        self.assertEqual(result.action, "MONITOR")
        self.assertEqual(result.reason_codes, ())
        with self.assertRaisesRegex(ValueError, "stale"):
            evaluate_premium_exit(
                self.spread,
                replace(short, quoted_at=self.now - timedelta(seconds=121)),
                replace(long, quoted_at=self.now - timedelta(seconds=121)),
                self.now,
                Decimal("0.65"),
            )

    def test_policy_and_contract_tampering_fail_closed(self) -> None:
        with self.assertRaises(ValueError):
            PremiumExitPolicy(profit_capture_fraction=Decimal("NaN"))
        short, long = self.quotes()
        with self.assertRaisesRegex(ValueError, "opened contracts"):
            evaluate_premium_exit(
                self.spread,
                replace(short, contract_id="OTHER"),
                long,
                self.now,
                Decimal("0.65"),
            )
        with self.assertRaisesRegex(ValueError, "source does not match"):
            evaluate_premium_exit(
                self.spread,
                replace(short, source_id="SUBSTITUTED-SOURCE"),
                replace(long, source_id="SUBSTITUTED-SOURCE"),
                self.now,
                Decimal("0.65"),
            )


if __name__ == "__main__":
    unittest.main()
