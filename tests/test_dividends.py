from dataclasses import replace
from datetime import datetime, timedelta, timezone
from decimal import Decimal
import unittest

from hedge_desk.dividends import (
    AnnualPayoutObservation,
    DividendCompanyHistory,
    evaluate_dividend_history,
    evaluate_dividend_universe,
)


NOW = datetime(2026, 8, 21, tzinfo=timezone.utc)


def history():
    return tuple(
        AnnualPayoutObservation(
            2016 + index,
            Decimal("1") + Decimal(index) / Decimal("10"),
            Decimal("4"), Decimal("50"), Decimal("100"), Decimal("25"),
            Decimal("10000"), NOW - timedelta(days=365 * (10 - index)),
            format(index + 1, "x") * 64,
        )
        for index in range(10)
    )


class DividendTests(unittest.TestCase):
    def test_universe_ranks_yield_per_payout_but_never_authorizes(self) -> None:
        base = history()
        efficient = tuple(
            replace(item, dividends_per_share=item.dividends_per_share * Decimal("1.2"),
                    earnings_per_share=Decimal("8"))
            for item in base
        )
        evaluation = evaluate_dividend_universe((
            DividendCompanyHistory("BASE", base),
            DividendCompanyHistory("EFFICIENT", efficient),
        ), NOW)
        self.assertEqual(evaluation.disposition, "RANKED_RESEARCH_ONLY")
        self.assertEqual(evaluation.candidates[0].symbol, "EFFICIENT")
        self.assertEqual(evaluation.candidates[0].rank, 1)
        self.assertEqual(
            evaluation.candidates[0].long_call_cash_dividend_entitlement,
            Decimal("0"),
        )
        self.assertFalse(evaluation.trade_authorized)

    def test_universe_rejects_yield_trap_and_can_return_no_trade(self) -> None:
        risky = tuple(
            replace(item, earnings_per_share=Decimal("1")) for item in history()
        )
        evaluation = evaluate_dividend_universe((
            DividendCompanyHistory("TRAP", risky),
        ), NOW)
        self.assertEqual(evaluation.disposition, "NO_TRADE")
        self.assertEqual(evaluation.candidates, ())
        self.assertIn(
            "AVERAGE_PAYOUT_RATIO_ABOVE_POLICY",
            evaluation.rejected_symbols[0][1],
        )

    def test_universe_order_is_deterministic_and_symbols_unique(self) -> None:
        one = DividendCompanyHistory("AAA", history())
        two = DividendCompanyHistory("BBB", history())
        forward = evaluate_dividend_universe((one, two), NOW)
        reverse = evaluate_dividend_universe((two, one), NOW)
        self.assertEqual(forward, reverse)
        with self.assertRaisesRegex(ValueError, "symbols must be unique"):
            evaluate_dividend_universe((one, one), NOW)

    def test_ten_year_metrics_are_exact_and_call_gets_no_dividend(self) -> None:
        result = evaluate_dividend_history(history(), NOW)
        self.assertTrue(result.admissible)
        self.assertEqual(result.ten_year_average_dividend_yield, Decimal("0.029"))
        self.assertEqual(result.ten_year_average_payout_ratio, Decimal("0.3625"))
        self.assertEqual(result.ten_year_average_net_shareholder_yield, Decimal("0.0365"))
        self.assertEqual(result.dividend_cut_count, 0)
        self.assertEqual(result.long_call_cash_dividend_entitlement, Decimal("0"))
        self.assertFalse(result.trade_authorized)

    def test_short_history_or_lookahead_fails_closed(self) -> None:
        self.assertIn(
            "TEN_YEAR_HISTORY_REQUIRED",
            evaluate_dividend_history(history()[:-1], NOW).reason_codes,
        )
        future = (replace(history()[0], available_at=NOW + timedelta(seconds=1)),) + history()[1:]
        self.assertIn(
            "PAYOUT_LOOKAHEAD_VIOLATION",
            evaluate_dividend_history(future, NOW).reason_codes,
        )

    def test_nonpositive_earnings_is_explicit_not_imputed(self) -> None:
        invalid = (replace(history()[0], earnings_per_share=Decimal("-1")),) + history()[1:]
        result = evaluate_dividend_history(invalid, NOW)
        self.assertFalse(result.admissible)
        self.assertIn("PAYOUT_COVERAGE_UNAVAILABLE", result.reason_codes)
        self.assertIsNone(result.ten_year_average_payout_ratio)


if __name__ == "__main__":
    unittest.main()
