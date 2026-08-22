from dataclasses import replace
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
import unittest

from hedge_desk.options import (
    OptionQuote,
    OptionType,
    UnderlyingQuote,
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
        open_interest=1000,
        volume=500,
    )


class OptionSpreadTests(unittest.TestCase):
    def test_nonfinite_quote_or_spread_policy_is_rejected(self) -> None:
        spread = VerticalCreditSpread(
            "spread-1",
            self.short,
            self.long,
            UnderlyingQuote(
                "TEST", Decimal("99.99"), Decimal("100.01"), NOW, "fixture"
            ),
            1,
            Decimal("0.65"),
        )
        with self.assertRaisesRegex(ValueError, "finite"):
            replace(spread.short_leg, ask=Decimal("Infinity"))
        with self.assertRaisesRegex(ValueError, "finite"):
            replace(spread, commission_per_contract=Decimal("NaN"))

    def setUp(self) -> None:
        self.short = quote("short", "95", "2.00", "2.10")
        self.long = quote("long", "90", "0.75", "0.80")

    def calculate(self, **overrides: object):
        values = {
            "spread_id": "spread-1",
            "short_leg": self.short,
            "long_leg": self.long,
            "underlying_quote": UnderlyingQuote(
                "TEST", Decimal("99.99"), Decimal("100.01"), NOW, "fixture"
            ),
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
        self.assertEqual(result.underlying_bid, Decimal("99.99"))
        self.assertEqual(result.underlying_ask, Decimal("100.01"))
        self.assertEqual(result.planned_exit_days_before_expiration, 7)
        self.assertEqual(result.planned_exit_date, date(2026, 8, 14))
        self.assertEqual(result.minimum_leg_open_interest, 1000)
        self.assertEqual(result.minimum_leg_volume, 500)
        self.assertEqual(result.return_on_risk, Decimal("118.70") / Decimal("381.30"))

    def test_misaligned_quote_timestamps_fail_closed(self) -> None:
        stale_long = replace(self.long, quoted_at=NOW - timedelta(seconds=3))
        with self.assertRaisesRegex(ValueError, "timestamp-compatible"):
            self.calculate(long_leg=stale_long)

    def test_stale_or_wrong_underlying_snapshot_fails_closed(self) -> None:
        stale = UnderlyingQuote(
            "TEST", Decimal("99"), Decimal("100"),
            NOW - timedelta(seconds=3), "fixture",
        )
        with self.assertRaisesRegex(ValueError, "timestamp-compatible"):
            self.calculate(underlying_quote=stale)
        wrong = UnderlyingQuote(
            "OTHER", Decimal("99"), Decimal("100"), NOW, "fixture"
        )
        with self.assertRaisesRegex(ValueError, "symbol must match"):
            self.calculate(underlying_quote=wrong)

    def test_quantity_above_displayed_size_fails_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "displayed size"):
            self.calculate(quantity=11)

    def test_thin_or_wide_option_market_fails_closed(self) -> None:
        thin = replace(self.long, open_interest=99)
        with self.assertRaisesRegex(ValueError, "open interest"):
            self.calculate(long_leg=thin)
        inactive = replace(self.long, volume=9)
        with self.assertRaisesRegex(ValueError, "volume"):
            self.calculate(long_leg=inactive)
        wide = replace(self.long, bid=Decimal("0.50"), ask=Decimal("0.80"))
        with self.assertRaisesRegex(ValueError, "bid-ask spread"):
            self.calculate(long_leg=wide)

    def test_invalid_put_strike_orientation_fails_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "short strike above"):
            self.calculate(short_leg=self.long, long_leg=self.short)

    def test_non_positive_executable_credit_fails_closed(self) -> None:
        expensive_hedge = replace(
            self.long, bid=Decimal("1.90"), ask=Decimal("2.00")
        )
        with self.assertRaisesRegex(ValueError, "positive credit"):
            self.calculate(long_leg=expensive_hedge)

    def test_new_candidate_at_planned_exit_window_fails_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "planned pre-expiration exit"):
            calculate_vertical_credit_spread(
                VerticalCreditSpread(
                    "spread-1",
                    self.short,
                    self.long,
                    UnderlyingQuote(
                        "TEST", Decimal("99.99"), Decimal("100.01"), NOW, "fixture"
                    ),
                    1,
                    Decimal("0.65"),
                    planned_exit_days_before_expiration=24,
                ),
                NOW,
            )


if __name__ == "__main__":
    unittest.main()
