from datetime import datetime, timedelta, timezone
from decimal import Decimal
import unittest

from hedge_desk.earnings_experiment import (
    assign_earnings_experiment,
    score_earnings_experiment,
)


RELEASE = datetime(2026, 8, 22, 20, 0, tzinfo=timezone.utc)


class EarningsExperimentTests(unittest.TestCase):
    def test_assignment_is_pre_release_deterministic_and_research_only(self) -> None:
        args = ("earnings-v1", "event-1", RELEASE - timedelta(days=1), RELEASE, "a" * 64)
        first = assign_earnings_experiment(*args)
        second = assign_earnings_experiment(*args)
        self.assertEqual(first, second)
        self.assertFalse(first.trade_authorized)

    def test_post_release_score_uses_only_locked_arm_and_costs(self) -> None:
        plan = assign_earnings_experiment(
            "earnings-v1", "event-1", RELEASE - timedelta(days=1), RELEASE, "a" * 64
        )
        result = score_earnings_experiment(
            plan, Decimal("100"), Decimal("7.50"), RELEASE + timedelta(minutes=5)
        )
        self.assertEqual(result.assigned_arm, plan.assigned_arm)
        self.assertEqual(result.net_pnl, Decimal("92.50"))
        self.assertTrue(result.hypothetical)
        self.assertFalse(result.trade_authorized)

    def test_late_assignment_or_early_scoring_fails(self) -> None:
        with self.assertRaisesRegex(ValueError, "must precede"):
            assign_earnings_experiment(
                "earnings-v1", "event-1", RELEASE, RELEASE, "a" * 64
            )
        plan = assign_earnings_experiment(
            "earnings-v1", "event-1", RELEASE - timedelta(days=1), RELEASE, "a" * 64
        )
        with self.assertRaisesRegex(ValueError, "must follow"):
            score_earnings_experiment(plan, Decimal("1"), Decimal("0"), RELEASE)


if __name__ == "__main__":
    unittest.main()
