from decimal import Decimal
import unittest

from hedge_desk.strategic_allocation import (
    AllocationWeight, AssetClass, evaluate_strategic_allocation,
)


def diversified(us_equity="0.25"):
    return (
        AllocationWeight(AssetClass.US_EQUITY, Decimal(us_equity)),
        AllocationWeight(AssetClass.INTERNATIONAL_EQUITY, Decimal("0.20")),
        AllocationWeight(AssetClass.FIXED_INCOME, Decimal("0.25")),
        AllocationWeight(AssetClass.REAL_ASSET, Decimal("0.20")),
        AllocationWeight(AssetClass.CASH, Decimal("1") - Decimal(us_equity) - Decimal("0.65")),
    )


class StrategicAllocationTests(unittest.TestCase):
    def test_diversified_high_cape_allocation_passes_without_ror_or_trade(self) -> None:
        result = evaluate_strategic_allocation(diversified(), Decimal("35"))
        self.assertTrue(result.admissible)
        self.assertFalse(result.risk_of_ruin_calculated)
        self.assertFalse(result.trade_authorized)
        self.assertEqual(len(result.artifact_sha256), 64)

    def test_input_order_does_not_change_allocation_artifact(self) -> None:
        weights = diversified()
        self.assertEqual(
            evaluate_strategic_allocation(weights, Decimal("35")).artifact_sha256,
            evaluate_strategic_allocation(tuple(reversed(weights)), Decimal("35")).artifact_sha256,
        )

    def test_high_cape_concentration_and_poor_diversification_block(self) -> None:
        weights = (
            AllocationWeight(AssetClass.US_EQUITY, Decimal("0.70")),
            AllocationWeight(AssetClass.FIXED_INCOME, Decimal("0.30")),
        )
        result = evaluate_strategic_allocation(weights, Decimal("35"))
        self.assertIn("HIGH_CAPE_US_EQUITY_CONCENTRATION", result.reason_codes)
        self.assertIn("ASSET_CLASS_CONCENTRATION_LIMIT", result.reason_codes)
        self.assertIn("ALLOCATION_DIVERSIFICATION_INSUFFICIENT", result.reason_codes)

    def test_weights_must_sum_exactly_to_one(self) -> None:
        result = evaluate_strategic_allocation(
            (AllocationWeight(AssetClass.CASH, Decimal("0.99")),), Decimal("20")
        )
        self.assertIn("ALLOCATION_WEIGHTS_DO_NOT_SUM_TO_ONE", result.reason_codes)


if __name__ == "__main__":
    unittest.main()
