from datetime import datetime, timezone
from decimal import Decimal
import unittest

from hedge_desk.compliance.account_gate import account_gate
from hedge_desk.domain import Account, AccountType, ProductType, TradeCandidate


NOW = datetime(2026, 7, 28, 13, 0, tzinfo=timezone.utc)


def candidate(product: ProductType) -> TradeCandidate:
    return TradeCandidate(
        candidate_id="candidate-1",
        symbol="TEST",
        product_type=product,
        quantity=1,
        entry_price=Decimal("100"),
        max_loss=Decimal("50"),
        expected_win=Decimal("100"),
        win_probability=Decimal("0.6"),
        quote_timestamp=NOW,
        average_daily_dollar_volume=Decimal("5000000"),
        thesis="Reference thesis.",
        invalidation="Reference invalidation.",
    )


class AccountGateTests(unittest.TestCase):
    def test_undefined_risk_options_are_always_blocked(self) -> None:
        account = Account(
            "paper-1",
            AccountType.INDIVIDUAL,
            Decimal("10000"),
            Decimal("10000"),
            options_approved=True,
        )
        self.assertIn(
            "UNDEFINED_RISK_OPTION_PROHIBITED",
            account_gate(account, candidate(ProductType.UNDEFINED_RISK_OPTION)),
        )

    def test_futures_are_conservatively_blocked_in_ira_mvp(self) -> None:
        account = Account(
            "paper-ira",
            AccountType.ROTH_IRA,
            Decimal("10000"),
            Decimal("10000"),
            futures_approved=True,
        )
        self.assertIn(
            "FUTURES_BLOCKED_IN_IRA_MVP",
            account_gate(account, candidate(ProductType.FUTURE)),
        )


if __name__ == "__main__":
    unittest.main()

