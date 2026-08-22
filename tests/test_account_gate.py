from datetime import datetime, timedelta, timezone
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
    def test_defined_risk_option_requires_odd_and_broker_policy_evidence(self) -> None:
        incomplete = Account(
            "paper-incomplete", AccountType.INDIVIDUAL, Decimal("10000"),
            Decimal("10000"), options_approved=True,
        )
        reasons = account_gate(
            incomplete, candidate(ProductType.DEFINED_RISK_OPTION)
        )
        self.assertIn("OPTIONS_DISCLOSURE_ACKNOWLEDGEMENT_REQUIRED", reasons)
        self.assertIn("BROKER_OPTIONS_POLICY_REQUIRED", reasons)
        complete = Account(
            "paper-complete", AccountType.INDIVIDUAL, Decimal("10000"),
            Decimal("10000"), options_approved=True,
            options_disclosure_version="synthetic-odd-v1",
            options_disclosure_acknowledged_at=NOW - timedelta(days=1),
            broker_options_policy_version="synthetic-broker-policy-v1",
        )
        self.assertEqual(
            account_gate(complete, candidate(ProductType.DEFINED_RISK_OPTION)), []
        )

    def test_post_candidate_odd_acknowledgement_fails_point_in_time(self) -> None:
        account = Account(
            "paper-late", AccountType.INDIVIDUAL, Decimal("10000"),
            Decimal("10000"), options_approved=True,
            options_disclosure_version="synthetic-odd-v1",
            options_disclosure_acknowledged_at=NOW + timedelta(microseconds=1),
            broker_options_policy_version="synthetic-broker-policy-v1",
        )
        self.assertIn(
            "OPTIONS_DISCLOSURE_ACKNOWLEDGED_AFTER_CANDIDATE",
            account_gate(account, candidate(ProductType.DEFINED_RISK_OPTION)),
        )

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
