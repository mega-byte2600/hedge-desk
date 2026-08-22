from dataclasses import replace
from datetime import datetime, timezone
from decimal import Decimal
import unittest

from hedge_desk.demo import build_reference_plan
from hedge_desk.domain import Account, AccountType, ProductType, TradeCandidate


NOW = datetime(2026, 8, 22, tzinfo=timezone.utc)


class DomainModelTests(unittest.TestCase):
    def test_account_rejects_nonfinite_money_and_nonboolean_approvals(self) -> None:
        with self.assertRaisesRegex(ValueError, "finite"):
            Account("paper", AccountType.INDIVIDUAL, Decimal("Infinity"), Decimal("1"))
        with self.assertRaisesRegex(ValueError, "boolean"):
            Account(
                "paper", AccountType.INDIVIDUAL, Decimal("1"), Decimal("1"),
                options_approved=1,
            )

    def test_candidate_rejects_nonfinite_values_and_boolean_quantity(self) -> None:
        values = dict(
            candidate_id="candidate", symbol="TEST", product_type=ProductType.EQUITY,
            quantity=1, entry_price=Decimal("1"), max_loss=Decimal("1"),
            expected_win=Decimal("1"), win_probability=Decimal("0.5"),
            quote_timestamp=NOW, average_daily_dollar_volume=Decimal("100"),
            thesis="Synthetic.", invalidation="Synthetic invalidation.",
        )
        with self.assertRaisesRegex(ValueError, "finite"):
            TradeCandidate(**dict(values, win_probability=Decimal("NaN")))
        with self.assertRaisesRegex(ValueError, "positive integer"):
            TradeCandidate(**dict(values, quantity=True))

    def test_decision_rejects_tampered_ror_hash_and_reasons(self) -> None:
        decision = build_reference_plan().risk_decision
        with self.assertRaisesRegex(ValueError, "finite"):
            replace(decision, risk_of_ruin_after=Decimal("Infinity"))
        with self.assertRaisesRegex(ValueError, "artifact hash"):
            replace(decision, risk_input_sha256="z" * 64)
        with self.assertRaisesRegex(ValueError, "unique and sorted"):
            replace(decision, reason_codes=("Z", "A", "A"))


if __name__ == "__main__":
    unittest.main()
