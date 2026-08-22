from dataclasses import replace
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
import unittest

from hedge_desk.options import (
    OptionQuote,
    OptionType,
    VerticalCreditSpread,
    calculate_vertical_credit_spread,
)


NOW = datetime(2026, 7, 28, 20, 0, tzinfo=timezone.utc)


def quote(contract_id: str, strike: str, bid: str, ask: str) -> OptionQuote:
    return OptionQuote(
        contract_id=contract_id,
        underlying="TEST",
        option_type=OptionType.PUT,
        strike=Decimal(strike),
        expiration=date(2026, 8, 21),
        bid=Decimal(bid),
        ask=Decimal(ask),
        bid_size=10,
        ask_size=10,
        quoted_at=NOW,
        source_id="fixture",
    )


class OptionSpreadTests(unittest.TestCase):
    def setUp(self) -> None:
        self.short = quote("short", "95", "2.00", "2.10")
        self.long = quote("long", "90", "0.75", "0.80")

    def calculate(self, **overrides: object):
        values = {
            "spread_id": "spread-1",
            "short_leg": self.short,
            "long_leg": self.long,
            "quantity": 1,
            "commission_per_contract": Decimal("0.65"),
        }
        values.update(overrides)
        return calculate_vertical_credit_spread(
            VerticalCreditSpread(**values), NOW  # type: ignore[arg-type]
        )

    def test_reference_economics_use_executable_sides(self) -> None:
        result = self.calculate()
        self.assertEqual(result.gross_credit, Decimal("120.00"))
        self.assertEqual(result.net_credit, Decimal("118.70"))
        self.assertEqual(result.maximum_loss, Decimal("381.30"))
        self.assertEqual(result.break_even, Decimal("93.813"))
        self.assertEqual(result.days_to_expiration, 24)
        self.assertEqual(result.expiration_date, date(2026, 8, 21))
        self.assertEqual(result.planned_exit_days_before_expiration, 7)
        self.assertEqual(result.planned_exit_date, date(2026, 8, 14))
        self.assertEqual(result.return_on_risk, Decimal("118.70") / Decimal("381.30"))

    def test_misaligned_quote_timestamps_fail_closed(self) -> None:
        stale_long = replace(self.long, quoted_at=NOW - timedelta(seconds=3))
        with self.assertRaisesRegex(ValueError, "timestamp-compatible"):
            self.calculate(long_leg=stale_long)

    def test_quantity_above_displayed_size_fails_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "displayed size"):
            self.calculate(quantity=11)

    def test_invalid_put_strike_orientation_fails_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "short strike above"):
            self.calculate(short_leg=self.long, long_leg=self.short)

    def test_non_positive_executable_credit_fails_closed(self) -> None:
        expensive_hedge = replace(self.long, ask=Decimal("2.00"))
        with self.assertRaisesRegex(ValueError, "positive credit"):
            self.calculate(long_leg=expensive_hedge)

    def test_new_candidate_at_planned_exit_window_fails_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "planned pre-expiration exit"):
            calculate_vertical_credit_spread(
                VerticalCreditSpread(
                    "spread-1",
                    self.short,
                    self.long,
                    1,
                    Decimal("0.65"),
                    planned_exit_days_before_expiration=24,
                ),
                NOW,
            )


if __name__ == "__main__":
    unittest.main()
