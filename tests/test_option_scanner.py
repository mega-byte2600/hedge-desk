from dataclasses import replace
from datetime import date, datetime, timezone
from decimal import Decimal
import unittest

from hedge_desk.options import (
    OptionQuote,
    OptionSnapshot,
    OptionType,
    SpreadScanPolicy,
    UnderlyingQuote,
    scan_vertical_credit_spreads,
)


NOW = datetime(2026, 8, 21, 12, 0, tzinfo=timezone.utc)
EXPIRY = date(2026, 9, 18)


def quote(contract_id, strike, bid, ask):
    return OptionQuote(
        contract_id, "TEST", OptionType.PUT, Decimal(strike), EXPIRY,
        Decimal(bid), Decimal(ask), 25, 25, NOW, "licensed-source", 1000, 500,
    )


def snapshot(quotes):
    return OptionSnapshot(
        "hedge-desk-option-snapshot-1.0.0",
        "licensed-source",
        UnderlyingQuote(
            "TEST", Decimal("99.99"), Decimal("100.01"), NOW, "licensed-source"
        ),
        tuple(quotes),
    )


class OptionScannerTests(unittest.TestCase):
    def test_nonfinite_or_boolean_scan_policy_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "finite"):
            SpreadScanPolicy(commission_per_contract=Decimal("Infinity"))
        with self.assertRaisesRegex(ValueError, "integers"):
            SpreadScanPolicy(quantity=True)

    def test_executable_put_vertical_reaches_control_pipeline(self) -> None:
        result = scan_vertical_credit_spreads(snapshot((
            quote("P95", "95", "2.00", "2.10"),
            quote("P90", "90", "0.75", "0.80"),
        )), NOW)
        self.assertEqual(result.disposition, "CANDIDATES_FOR_CONTROL_PIPELINE")
        self.assertEqual(result.pair_count, 1)
        self.assertEqual(result.admissible_count, 1)
        calculation = result.evaluations[0].calculation
        self.assertIsNotNone(calculation)
        self.assertEqual(calculation.net_credit, Decimal("118.70"))

    def test_input_order_does_not_change_scan_result(self) -> None:
        quotes = (
            quote("P95", "95", "2.00", "2.10"),
            quote("P90", "90", "0.75", "0.80"),
            quote("P85", "85", "0.20", "0.25"),
        )
        forward = scan_vertical_credit_spreads(snapshot(quotes), NOW)
        reverse = scan_vertical_credit_spreads(snapshot(tuple(reversed(quotes))), NOW)
        self.assertEqual(forward, reverse)
        self.assertEqual(forward.pair_count, 3)

    def test_thin_market_yields_no_trade_with_reason(self) -> None:
        thin = replace(quote("P95", "95", "2.00", "2.10"), volume=9)
        result = scan_vertical_credit_spreads(snapshot((
            thin, quote("P90", "90", "0.75", "0.80")
        )), NOW)
        self.assertEqual(result.disposition, "NO_TRADE")
        self.assertEqual(result.admissible_count, 0)
        self.assertEqual(result.evaluations[0].reason_code, "VOLUME_BELOW_POLICY")

    def test_safety_limits_fail_before_quadratic_scan(self) -> None:
        policy = SpreadScanPolicy(maximum_contract_count=1)
        with self.assertRaisesRegex(ValueError, "contract-count safety limit"):
            scan_vertical_credit_spreads(snapshot((
                quote("P95", "95", "2.00", "2.10"),
                quote("P90", "90", "0.75", "0.80"),
            )), NOW, policy)


if __name__ == "__main__":
    unittest.main()
