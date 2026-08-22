from dataclasses import replace
from datetime import datetime, timedelta, timezone
from decimal import Decimal
import unittest

from hedge_desk.earnings import (
    EarningsConsensus,
    EarningsEventInput,
    EarningsRelease,
    evaluate_earnings_surprise,
    evaluate_earnings_universe,
)


NOW = datetime(2026, 8, 21, 20, 0, tzinfo=timezone.utc)


class EarningsTests(unittest.TestCase):
    def test_nonfinite_consensus_or_actual_cannot_rank(self) -> None:
        with self.assertRaisesRegex(ValueError, "finite"):
            evaluate_earnings_surprise(
                replace(self.consensus, eps_consensus=Decimal("Infinity")),
                self.release,
                NOW,
            )

    def setUp(self) -> None:
        self.consensus = EarningsConsensus(
            "TEST", "2026Q2", Decimal("1.00"), Decimal("1000"), 8,
            NOW - timedelta(hours=2), "a" * 64,
        )
        self.release = EarningsRelease(
            "TEST", "2026Q2", Decimal("1.10"), Decimal("1020"),
            NOW - timedelta(minutes=2), NOW - timedelta(minutes=1), "b" * 64,
        )

    def test_aligned_surprise_is_exact_but_never_authorizes_direction(self) -> None:
        result = evaluate_earnings_surprise(self.consensus, self.release, NOW)
        self.assertTrue(result.admissible)
        self.assertEqual(result.eps_surprise_fraction, Decimal("0.10"))
        self.assertEqual(result.revenue_surprise_fraction, Decimal("0.02"))
        self.assertEqual(result.surprise_alignment, "BOTH_POSITIVE")
        self.assertFalse(result.directional_trade_authorized)

    def test_universe_ranks_aligned_surprises_without_directional_trade(self) -> None:
        stronger = EarningsEventInput(
            "stronger",
            replace(self.consensus, symbol="STRONG"),
            replace(
                self.release, symbol="STRONG", eps_actual=Decimal("1.20"),
                revenue_actual=Decimal("1050"),
            ),
        )
        weaker = EarningsEventInput("weaker", self.consensus, self.release)
        evaluation = evaluate_earnings_universe((weaker, stronger), NOW)
        self.assertEqual(evaluation.candidates[0].event_id, "stronger")
        self.assertEqual(evaluation.candidates[0].surprise_alignment, "BOTH_POSITIVE")
        self.assertFalse(evaluation.directional_trade_authorized)
        self.assertTrue(
            all(not item.directional_trade_authorized for item in evaluation.candidates)
        )

    def test_mixed_or_invalid_universe_events_are_rejected_not_forced(self) -> None:
        mixed = EarningsEventInput(
            "mixed", self.consensus,
            replace(self.release, revenue_actual=Decimal("990")),
        )
        evaluation = evaluate_earnings_universe((mixed,), NOW)
        self.assertEqual(evaluation.disposition, "NO_TRADE")
        self.assertIn("SURPRISE_NOT_ALIGNED", evaluation.rejected_events[0][1])

    def test_mixed_surprise_is_not_forced_into_call_or_put(self) -> None:
        release = replace(self.release, revenue_actual=Decimal("990"))
        result = evaluate_earnings_surprise(self.consensus, release, NOW)
        self.assertEqual(result.surprise_alignment, "MIXED")
        self.assertFalse(result.directional_trade_authorized)

    def test_lookahead_and_weak_consensus_fail_closed(self) -> None:
        consensus = replace(self.consensus, as_of=NOW, analyst_count=1)
        result = evaluate_earnings_surprise(consensus, self.release, NOW)
        self.assertFalse(result.admissible)
        self.assertIn("CONSENSUS_NOT_POINT_IN_TIME", result.reason_codes)
        self.assertIn("CONSENSUS_BREADTH_INSUFFICIENT", result.reason_codes)


if __name__ == "__main__":
    unittest.main()
