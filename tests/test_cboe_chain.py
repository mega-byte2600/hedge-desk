"""Deterministic parser tests for the real Cboe chain adapter (no network)."""

import json
import unittest
from datetime import datetime, timezone

from hedge_desk.cboe_chain import (
    _parse_symbol,
    build_snapshot_from_cboe,
    real_chain_income,
)
from hedge_desk.options import OptionType


def _cboe_payload(symbol="SPY", price="100.00", options=()):
    # SPY-style strikes are ~760; a price of 760 keeps them in the 12% band.
    actual_price = price
    if price == "100.00":
        actual_price = "760.00"
    return json.dumps(
        {
            "data": {
                "symbol": symbol,
                "current_price": actual_price,
                "bid": actual_price,
                "ask": actual_price,
                "options": list(options),
            }
        }
    ).encode("utf-8")


def _opt(contract, bid, ask, oi=500, vol=200, bsize=25, asize=30):
    return {
        "option": contract,
        "bid": bid,
        "ask": ask,
        "bid_size": bsize,
        "ask_size": asize,
        "open_interest": oi,
        "volume": vol,
    }


class CboeParseTests(unittest.TestCase):
    def test_parse_symbol_call(self):
        result = _parse_symbol("SPY261023C00764000")
        self.assertIsNotNone(result)
        under, expiry, ot, strike = result
        self.assertEqual(under, "SPY")
        self.assertEqual(expiry.isoformat(), "2026-10-23")
        self.assertEqual(ot, OptionType.CALL)
        self.assertEqual(strike, 764)

    def test_parse_symbol_put(self):
        result = _parse_symbol("QQQ261023P00450000")
        self.assertIsNotNone(result)
        under, expiry, ot, strike = result
        self.assertEqual(under, "QQQ")
        self.assertEqual(ot, OptionType.PUT)
        self.assertEqual(strike, 450)

    def test_build_snapshot_filters_unexecutable(self):
        now = datetime(2026, 9, 19, 12, 0, tzinfo=timezone.utc)
        payload = _cboe_payload(
            options=[
                _opt("SPY261023C00760000", 2.0, 2.2),  # valid OTM call
                _opt("SPY261023C00750000", 0.0, 1.0),  # bid 0 -> excluded
                _opt("SPY261023C00770000", 3.0, 2.5),  # crossed -> excluded
            ]
        )
        snap = build_snapshot_from_cboe(payload, "SPY", now)
        self.assertEqual(snap.underlying_quote.symbol, "SPY")
        self.assertEqual(len(snap.option_quotes), 1)
        self.assertEqual(snap.option_quotes[0].contract_id, "SPY261023C00760000")

    def test_parse_symbol_rejects_garbage(self):
        self.assertIsNone(_parse_symbol("NOTANOPTION"))
        self.assertIsNone(_parse_symbol(""))


if __name__ == "__main__":
    unittest.main()