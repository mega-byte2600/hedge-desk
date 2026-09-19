"""Deterministic tests for premium-desk candidate economics from real EOD."""

import unittest
from decimal import Decimal

from hedge_desk.premium_candidates import (
    PREMIUM_CANDIDATE_VERSION,
    build_premium_candidates,
)


def _eod_result(symbol="AAPL", close="100.00"):
    return {
        "schema_version": "hedge-desk-eod-ingest-1.0.0",
        "source_results": [
            {
                "symbol": symbol,
                "status": "PASS",
                "last_day_close": close,
                "last_day": "2026-09-18",
                "reason_codes": [],
            }
        ],
    }


class PremiumCandidateTests(unittest.TestCase):
    def test_three_structures_per_symbol(self):
        result = build_premium_candidates(_eod_result())
        self.assertEqual(result["schema_version"], PREMIUM_CANDIDATE_VERSION)
        self.assertEqual(result["symbol_count"], 1)
        self.assertEqual(result["candidate_count"], 3)
        strategies = {c["strategy"] for c in result["candidates"]}
        self.assertEqual(
            strategies,
            {"CASH_SECURED_PUT", "COVERED_CALL", "CREDIT_SPREAD"},
        )

    def test_cash_secured_put_strike_and_collateral(self):
        result = build_premium_candidates(_eod_result(close="100.00"))
        put = next(c for c in result["candidates"] if c["strategy"] == "CASH_SECURED_PUT")
        # 10% below 100 = 90.00; collateral = strike x 100 = 9000.00
        self.assertEqual(put["strike"], "90.00")
        self.assertEqual(Decimal(put["requirement"]), Decimal("9000.00"))
        self.assertIn("COLLATERAL_CASH_SECURED", put["reason_codes"])
        self.assertFalse(put["trade_authorized"])

    def test_covered_call_requirement_is_shares(self):
        result = build_premium_candidates(_eod_result(close="100.00"))
        call = next(c for c in result["candidates"] if c["strategy"] == "COVERED_CALL")
        # 100 shares x 100.00 = 10000.00
        self.assertEqual(Decimal(call["requirement"]), Decimal("10000.00"))
        self.assertIn("SHARES_ARE_COLLATERAL", call["reason_codes"])

    def test_credit_spread_margin_is_width(self):
        result = build_premium_candidates(_eod_result(close="100.00"))
        spread = next(c for c in result["candidates"] if c["strategy"] == "CREDIT_SPREAD")
        # $5 wide x 100 = 500.00 at zero credit
        self.assertEqual(Decimal(spread["requirement"]), Decimal("500.00"))
        self.assertIn("DEFINED_RISK", spread["reason_codes"])

    def test_rejected_symbols_are_skipped(self):
        result = build_premium_candidates(
            {
                "source_results": [
                    {"symbol": "BAD", "status": "REJECT", "reason_codes": ["X"]},
                    {"symbol": "OK", "status": "PASS", "last_day_close": "50.00"},
                ]
            }
        )
        self.assertEqual(result["symbol_count"], 1)
        self.assertEqual({c["symbol"] for c in result["candidates"]}, {"OK"})

    def test_no_trade_authorized_anywhere(self):
        result = build_premium_candidates(_eod_result())
        self.assertTrue(all(not c["trade_authorized"] for c in result["candidates"]))


if __name__ == "__main__":
    unittest.main()