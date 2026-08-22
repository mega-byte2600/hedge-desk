from datetime import datetime, timezone
from decimal import Decimal
import unittest

from hedge_desk.backoffice import (
    PortfolioPolicy,
    PositionExposure,
    evaluate_drawdown_circuit_breaker,
    evaluate_portfolio_gate,
)
from hedge_desk.domain import Account, AccountType, ProductType, TradeCandidate


NOW = datetime(2026, 8, 21, 12, 0, tzinfo=timezone.utc)
ACCOUNT = Account(
    "paper-1", AccountType.INDIVIDUAL, Decimal("100000"), Decimal("50000"), True
)
CANDIDATE = TradeCandidate(
    "candidate-1", "TEST", ProductType.DEFINED_RISK_OPTION, 1, Decimal("100"),
    Decimal("1000"), Decimal("200"), Decimal("0.9"), NOW,
    Decimal("10000000"), "Synthetic thesis.", "Synthetic invalidation.",
)


class PortfolioGateTests(unittest.TestCase):
    def test_empty_portfolio_snapshot_is_explicit_and_reproducible(self) -> None:
        first = evaluate_portfolio_gate(ACCOUNT, CANDIDATE, ())
        second = evaluate_portfolio_gate(ACCOUNT, CANDIDATE, ())
        self.assertEqual(first, second)
        self.assertEqual(len(first.snapshot_sha256), 64)
        self.assertEqual(first.reason_codes, ())

    def test_aggregate_loss_and_symbol_concentration_block(self) -> None:
        positions = (
            PositionExposure("p1", "TEST", Decimal("1500")),
            PositionExposure("p2", "OTHER", Decimal("3000")),
        )
        result = evaluate_portfolio_gate(ACCOUNT, CANDIDATE, positions)
        self.assertIn("PORTFOLIO_AGGREGATE_LOSS_LIMIT", result.reason_codes)
        self.assertIn("SYMBOL_CONCENTRATION_LIMIT", result.reason_codes)

    def test_exact_fraction_boundaries_pass_and_one_cent_over_blocks(self) -> None:
        exact = (PositionExposure("p1", "OTHER", Decimal("4000")),)
        self.assertNotIn(
            "PORTFOLIO_AGGREGATE_LOSS_LIMIT",
            evaluate_portfolio_gate(ACCOUNT, CANDIDATE, exact).reason_codes,
        )
        over = (PositionExposure("p1", "OTHER", Decimal("4000.01")),)
        self.assertIn(
            "PORTFOLIO_AGGREGATE_LOSS_LIMIT",
            evaluate_portfolio_gate(ACCOUNT, CANDIDATE, over).reason_codes,
        )

    def test_position_order_does_not_change_snapshot_hash(self) -> None:
        one = PositionExposure("p1", "AAA", Decimal("100"))
        two = PositionExposure("p2", "BBB", Decimal("200"))
        forward = evaluate_portfolio_gate(ACCOUNT, CANDIDATE, (one, two))
        reverse = evaluate_portfolio_gate(ACCOUNT, CANDIDATE, (two, one))
        self.assertEqual(forward.snapshot_sha256, reverse.snapshot_sha256)

    def test_drawdown_circuit_breaker_exact_boundary_and_breach(self) -> None:
        source_hash = "a" * 64
        exact = evaluate_drawdown_circuit_breaker(
            Decimal("5000"), Decimal("5000"), source_hash
        )
        self.assertFalse(exact.new_risk_frozen)
        breached = evaluate_drawdown_circuit_breaker(
            Decimal("5000.01"), Decimal("5000"), source_hash
        )
        self.assertTrue(breached.new_risk_frozen)
        self.assertEqual(
            breached.reason_codes, ("PORTFOLIO_DRAWDOWN_CIRCUIT_BREAKER",)
        )
        self.assertEqual(len(breached.artifact_sha256), 64)


if __name__ == "__main__":
    unittest.main()
