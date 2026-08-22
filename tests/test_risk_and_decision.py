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
from hedge_desk.risk import build_validated_risk_inputs


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


def risk_inputs(
    trade: TradeCandidate,
    risk_of_ruin_after: Decimal = Decimal("0"),
):
    return build_validated_risk_inputs(
        trade.candidate_id,
        trade.max_loss,
        trade.expected_win,
        trade.win_probability,
        trade.quote_timestamp,
        "a" * 64,
        "b" * 64,
        Decimal("0"),
        risk_of_ruin_after,
        "finite-capital-ruin-approximation",
        "0.1.0-unvalidated",
        "classic-vv-test-validator",
        "1.0.0",
    )


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
        decision = evaluate_candidate(self.account, trade, NOW, risk_inputs=risk_inputs(trade))
        self.assertEqual(decision.status, DecisionStatus.BLOCKED)
        self.assertIn("STALE_QUOTE", decision.reason_codes)

    def test_excessive_trade_loss_blocks_decision(self) -> None:
        trade = make_candidate(max_loss=Decimal("2000"))
        decision = evaluate_candidate(self.account, trade, NOW, risk_inputs=risk_inputs(trade))
        self.assertIn("SINGLE_TRADE_LOSS_LIMIT", decision.reason_codes)

    def test_valid_candidate_is_approved_for_paper_only(self) -> None:
        trade = make_candidate()
        decision = evaluate_candidate(
            self.account,
            trade,
            NOW,
            RiskPolicy(maximum_risk_of_ruin=Decimal("0.04")),
            risk_inputs(trade),
        )
        self.assertEqual(decision.status, DecisionStatus.RISK_PASS)
        self.assertEqual(decision.reason_codes, ())
        self.assertEqual(decision.risk_source_artifact_sha256, "a" * 64)

    def test_decision_consumes_exact_validated_ror_without_recalculation(self) -> None:
        trade = make_candidate()
        supplied = Decimal("0.0123456789")
        decision = evaluate_candidate(
            self.account, trade, NOW, risk_inputs=risk_inputs(trade, supplied)
        )
        self.assertEqual(decision.risk_of_ruin_after, supplied)

    def test_validated_ror_above_policy_limit_blocks(self) -> None:
        trade = make_candidate()
        decision = evaluate_candidate(
            self.account,
            trade,
            NOW,
            RiskPolicy(maximum_risk_of_ruin=Decimal("0.04")),
            risk_inputs(trade, Decimal("0.0400000001")),
        )
        self.assertEqual(decision.status, DecisionStatus.BLOCKED)
        self.assertIn("RISK_OF_RUIN_LIMIT", decision.reason_codes)

    def test_decision_is_deterministic(self) -> None:
        trade = make_candidate()
        first = evaluate_candidate(self.account, trade, NOW, risk_inputs=risk_inputs(trade))
        second = evaluate_candidate(self.account, trade, NOW, risk_inputs=risk_inputs(trade))
        self.assertEqual(first, second)

    def test_missing_or_mismatched_risk_input_artifact_fails_closed(self) -> None:
        trade = make_candidate()
        with self.assertRaisesRegex(ValueError, "validated quantitative"):
            evaluate_candidate(self.account, trade, NOW)
        changed = make_candidate(win_probability=Decimal("0.61"))
        with self.assertRaisesRegex(ValueError, "differ"):
            evaluate_candidate(
                self.account, changed, NOW, risk_inputs=risk_inputs(trade)
            )

    def test_unapproved_model_or_validator_identity_fails_closed(self) -> None:
        trade = make_candidate()
        with self.assertRaisesRegex(ValueError, "risk model is not permitted"):
            evaluate_candidate(
                self.account,
                trade,
                NOW,
                RiskPolicy(required_risk_model_version="approved-v2"),
                risk_inputs(trade),
            )
        with self.assertRaisesRegex(ValueError, "risk validator is not permitted"):
            evaluate_candidate(
                self.account,
                trade,
                NOW,
                RiskPolicy(permitted_validator_ids=("independent-vv-prod",)),
                risk_inputs(trade),
            )

    def test_malformed_risk_policy_cannot_be_constructed(self) -> None:
        invalid_cases = (
            {"maximum_risk_of_ruin": Decimal("NaN")},
            {"maximum_risk_of_ruin": Decimal("1.01")},
            {"maximum_quote_age_seconds": -1},
            {"maximum_single_trade_loss_fraction": Decimal("0")},
            {"required_risk_model_id": ""},
            {"permitted_validator_ids": ()},
            {"permitted_validator_ids": ("same", "same")},
        )
        for values in invalid_cases:
            with self.subTest(values=values), self.assertRaises(ValueError):
                RiskPolicy(**values)


if __name__ == "__main__":
    unittest.main()
