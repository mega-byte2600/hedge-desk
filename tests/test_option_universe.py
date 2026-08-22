from dataclasses import replace
from datetime import datetime, timezone
import unittest

from hedge_desk.demo import (
    build_reference_market_session_gate,
    build_reference_option_snapshot,
)
from hedge_desk.options import evaluate_option_universe


NOW = datetime(2026, 7, 28, 20, 0, tzinfo=timezone.utc)


def renamed(snapshot, symbol, source_hash):
    underlying = replace(snapshot.underlying_quote, symbol=symbol)
    quotes = tuple(replace(item, underlying=symbol) for item in snapshot.option_quotes)
    return replace(
        snapshot, underlying_quote=underlying, option_quotes=quotes,
        source_artifact_sha256=source_hash,
    )


class OptionUniverseTests(unittest.TestCase):
    def test_underlyings_rank_by_executable_defined_risk_not_probability(self) -> None:
        base = build_reference_option_snapshot()
        stronger_quotes = tuple(
            replace(
                item,
                bid=item.bid + (1 if index == 0 else 0),
                ask=item.ask + (1 if index == 0 else 0),
            )
            for index, item in enumerate(base.option_quotes)
        )
        stronger = renamed(replace(base, option_quotes=stronger_quotes), "STRONG", "c" * 64)
        weaker = renamed(base, "WEAK", "d" * 64)
        result = evaluate_option_universe(
            (weaker, stronger), NOW, build_reference_market_session_gate()
        )
        self.assertEqual(result.candidates[0].symbol, "STRONG")
        self.assertFalse(result.probability_inferred)
        self.assertTrue(all(not item.trade_authorized for item in result.candidates))

    def test_order_is_stable_and_blocked_session_returns_no_trade(self) -> None:
        base = build_reference_option_snapshot()
        one = renamed(base, "ONE", "c" * 64)
        two = renamed(base, "TWO", "d" * 64)
        gate = build_reference_market_session_gate()
        self.assertEqual(
            evaluate_option_universe((one, two), NOW, gate),
            evaluate_option_universe((two, one), NOW, gate),
        )
        blocked = replace(gate, admissible=False, reason_codes=("MARKET_NOT_OPEN",))
        result = evaluate_option_universe((one,), NOW, blocked)
        self.assertEqual(result.disposition, "NO_TRADE")
        self.assertIn("MARKET_NOT_OPEN", result.rejected_underlyings[0][1])


if __name__ == "__main__":
    unittest.main()
