from datetime import datetime, timedelta, timezone
from decimal import Decimal
import unittest

from hedge_desk.backoffice import (
    BackOfficeStatus,
    evaluate_compliance_policy,
    evaluate_drawdown_circuit_breaker,
    evaluate_paper_compliance,
)
from hedge_desk.domain import Account, AccountType, ProductType, TradeCandidate


NOW = datetime(2026, 8, 21, 12, 0, tzinfo=timezone.utc)


def candidate(product: ProductType) -> TradeCandidate:
    return TradeCandidate(
        "candidate-1", "TEST", product, 1, Decimal("1"), Decimal("100"),
        Decimal("25"), Decimal("0.9"), NOW, Decimal("10000000"),
        "Synthetic paper thesis.", "Synthetic invalidation.",
    )


class BackOfficeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.account = Account(
            "paper-1", AccountType.INDIVIDUAL, Decimal("100000"),
            Decimal("50000"), options_approved=True,
            options_disclosure_version="synthetic-odd-v1",
            options_disclosure_acknowledged_at=NOW - timedelta(days=1),
            broker_options_policy_version="synthetic-broker-policy-v1",
        )

    def test_defined_risk_option_with_approval_passes_paper_policy(self) -> None:
        result = evaluate_paper_compliance(
            self.account, candidate(ProductType.DEFINED_RISK_OPTION), NOW
        )
        self.assertIs(result.status, BackOfficeStatus.PASS)
        self.assertEqual(result.environment, "paper")
        self.assertEqual(len(result.policy_decision.artifact_sha256), 64)
        self.assertEqual(
            result.policy_decision.options_disclosure_version,
            "synthetic-odd-v1",
        )
        self.assertEqual(
            result.policy_decision.broker_options_policy_version,
            "synthetic-broker-policy-v1",
        )

    def test_compliance_policy_is_independent_and_live_fails_closed(self) -> None:
        result = evaluate_compliance_policy(
            self.account,
            candidate(ProductType.DEFINED_RISK_OPTION),
            NOW,
            environment="live",
        )
        self.assertIs(result.status, BackOfficeStatus.BLOCK)
        self.assertEqual(result.reason_codes, ("PAPER_ONLY_VIOLATION",))
        self.assertEqual(len(result.artifact_sha256), 64)

    def test_front_office_equity_proposal_cannot_enter_premium_workflow(self) -> None:
        result = evaluate_paper_compliance(
            self.account, candidate(ProductType.EQUITY), NOW
        )
        self.assertIs(result.status, BackOfficeStatus.BLOCK)
        self.assertIn("PREMIUM_MVP_DEFINED_RISK_OPTIONS_ONLY", result.reason_codes)

    def test_missing_options_approval_blocks(self) -> None:
        account = Account(
            "paper-2", AccountType.INDIVIDUAL, Decimal("100000"),
            Decimal("50000"), options_approved=False,
        )
        result = evaluate_paper_compliance(
            account, candidate(ProductType.DEFINED_RISK_OPTION), NOW
        )
        self.assertIn("OPTIONS_APPROVAL_REQUIRED", result.reason_codes)

    def test_portfolio_drawdown_freeze_blocks_front_office_candidate(self) -> None:
        circuit_breaker = evaluate_drawdown_circuit_breaker(
            Decimal("5000.01"), Decimal("5000"), "a" * 64
        )
        result = evaluate_paper_compliance(
            self.account,
            candidate(ProductType.DEFINED_RISK_OPTION),
            NOW,
            circuit_breaker=circuit_breaker,
        )
        self.assertIs(result.status, BackOfficeStatus.BLOCK)
        self.assertIn("PORTFOLIO_DRAWDOWN_CIRCUIT_BREAKER", result.reason_codes)
        self.assertEqual(result.circuit_breaker_sha256, circuit_breaker.artifact_sha256)


if __name__ == "__main__":
    unittest.main()
