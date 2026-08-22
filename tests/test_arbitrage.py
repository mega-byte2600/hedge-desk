from dataclasses import replace
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
import unittest

from hedge_desk.arbitrage import (
    ArbitrageLeg,
    ArbitragePackage,
    LegSide,
    evaluate_arbitrage_package,
    evaluate_arbitrage_universe,
)


NOW = datetime(2026, 8, 21, 20, 0, tzinfo=timezone.utc)
SETTLEMENT = date(2026, 9, 18)


def legs():
    return (
        ArbitrageLeg("buy-a", LegSide.BUY, Decimal("1.9"), Decimal("2.0"), 5, NOW, SETTLEMENT, "a" * 64),
        ArbitrageLeg("sell-b", LegSide.SELL, Decimal("1.5"), Decimal("1.6"), 5, NOW, SETTLEMENT, "b" * 64),
    )


class ArbitrageTests(unittest.TestCase):
    def test_nonfinite_edge_input_cannot_rank(self) -> None:
        with self.assertRaisesRegex(ValueError, "finite"):
            evaluate_arbitrage_package(
                legs(), 1, 100, Decimal("Infinity"),
                Decimal("1"), Decimal("1"), Decimal("1"), Decimal("1"),
            )

    def package(self, package_id, terminal_value):
        return ArbitragePackage(
            package_id, legs(), 1, 100, Decimal(terminal_value), Decimal("5"),
            Decimal("5"), Decimal("5"), Decimal("20"),
        )

    def test_universe_ranks_executable_net_edge_without_authorizing(self) -> None:
        lower = self.package("LOWER", "100")
        higher = self.package("HIGHER", "120")
        evaluation = evaluate_arbitrage_universe((lower, higher))
        self.assertEqual(evaluation.disposition, "RANKED_RESEARCH_ONLY")
        self.assertEqual(evaluation.candidates[0].package_id, "HIGHER")
        self.assertEqual(evaluation.candidates[0].net_edge, Decimal("55.0"))
        self.assertFalse(evaluation.trade_authorized)
        self.assertTrue(all(not item.trade_authorized for item in evaluation.candidates))

    def test_universe_is_order_stable_and_can_return_no_trade(self) -> None:
        one = self.package("ONE", "100")
        two = self.package("TWO", "110")
        self.assertEqual(
            evaluate_arbitrage_universe((one, two)),
            evaluate_arbitrage_universe((two, one)),
        )
        blocked = evaluate_arbitrage_universe((self.package("BLOCKED", "70"),))
        self.assertEqual(blocked.disposition, "NO_TRADE")
        self.assertIn("EDGE_BELOW_SAFETY_BUFFER", blocked.rejected_packages[0][1])

    def test_executable_net_edge_survives_all_reserves_but_is_research_only(self) -> None:
        result = evaluate_arbitrage_package(
            legs(), 1, 100, Decimal("100"), Decimal("5"), Decimal("5"),
            Decimal("5"), Decimal("20"),
        )
        self.assertEqual(result.executable_entry_cashflow, Decimal("-50.0"))
        self.assertEqual(result.net_edge, Decimal("35.0"))
        self.assertEqual(result.disposition, "NET_EDGE_RESEARCH_CANDIDATE")
        self.assertFalse(result.trade_authorized)

    def test_costs_can_erase_apparent_identity_edge(self) -> None:
        result = evaluate_arbitrage_package(
            legs(), 1, 100, Decimal("70"), Decimal("5"), Decimal("5"),
            Decimal("5"), Decimal("20"),
        )
        self.assertEqual(result.disposition, "NO_TRADE")
        self.assertIn("EDGE_BELOW_SAFETY_BUFFER", result.reason_codes)

    def test_stale_leg_depth_and_settlement_mismatch_fail_closed(self) -> None:
        bad = (
            legs()[0],
            replace(
                legs()[1], quoted_at=NOW - timedelta(seconds=2), displayed_size=0,
                settlement_date=date(2026, 9, 19),
            ),
        )
        result = evaluate_arbitrage_package(
            bad, 1, 100, Decimal("100"), Decimal("5"), Decimal("5"),
            Decimal("5"), Decimal("20"),
        )
        self.assertIn("QUOTES_NOT_SYNCHRONIZED", result.reason_codes)
        self.assertIn("INSUFFICIENT_DEPTH", result.reason_codes)
        self.assertIn("SETTLEMENT_MISMATCH", result.reason_codes)


if __name__ == "__main__":
    unittest.main()
