from datetime import datetime, timedelta, timezone
from decimal import Decimal
import unittest

from hedge_desk.core.decision import evaluate_candidate
from hedge_desk.domain import (
    Account,
    AccountType,
    DecisionStatus,
    ProductType,
    TradeCandidate,
)
from hedge_desk.risk.ruin import RiskPolicy, estimate_risk_of_ruin


NOW = datetime(2026, 7, 28, 13, 0, tzinfo=timezone.utc)


def make_candidate(**overrides: object) -> TradeCandidate:
    values = {
        "candidate_id": "candidate-1",
        "symbol": "TEST",
        "product_type": ProductType.EQUITY,
        "quantity": 1,
        "entry_price": Decimal("100"),
        "max_loss": Decimal("100"),
        "expected_win": Decimal("200"),
        "win_probability": Decimal("0.6"),
        "quote_timestamp": NOW - timedelta(minutes=1),
        "average_daily_dollar_volume": Decimal("5000000"),
        "thesis": "Reference positive-expectancy thesis.",
        "invalidation": "Reference invalidation.",
    }
    values.update(overrides)
    return TradeCandidate(**values)  # type: ignore[arg-type]


class RiskAndDecisionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.account = Account(
            "paper-1",
            AccountType.INDIVIDUAL,
            Decimal("100000"),
            Decimal("50000"),
        )

    def test_non_positive_expectancy_is_certain_ruin(self) -> None:
        result = estimate_risk_of_ruin(
            Decimal("100000"),
            Decimal("1000"),
            Decimal("0.4"),
            Decimal("500"),
        )
        self.assertEqual(result, Decimal("1"))

    def test_stale_quote_blocks_decision(self) -> None:
        trade = make_candidate(quote_timestamp=NOW - timedelta(hours=1))
        decision = evaluate_candidate(self.account, trade, NOW)
        self.assertEqual(decision.status, DecisionStatus.BLOCKED)
        self.assertIn("STALE_QUOTE", decision.reason_codes)

    def test_excessive_trade_loss_blocks_decision(self) -> None:
        trade = make_candidate(max_loss=Decimal("2000"))
        decision = evaluate_candidate(self.account, trade, NOW)
        self.assertIn("SINGLE_TRADE_LOSS_LIMIT", decision.reason_codes)

    def test_valid_candidate_is_approved_for_paper_only(self) -> None:
        decision = evaluate_candidate(
            self.account,
            make_candidate(),
            NOW,
            RiskPolicy(maximum_risk_of_ruin=Decimal("0.04")),
        )
        self.assertEqual(decision.status, DecisionStatus.APPROVED_FOR_PAPER)
        self.assertEqual(decision.reason_codes, ())

    def test_decision_is_deterministic(self) -> None:
        trade = make_candidate()
        first = evaluate_candidate(self.account, trade, NOW)
        second = evaluate_candidate(self.account, trade, NOW)
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()

