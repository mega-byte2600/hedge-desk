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


def _put(contract_strike: int, oi: int, vol: int = 50):
    return _opt(f"SPY261023P{contract_strike * 1000:08d}", 1.0, 1.2, oi=oi, vol=vol)


def _call(contract_strike: int, oi: int, vol: int = 50):
    return _opt(f"SPY261023C{contract_strike * 1000:08d}", 1.0, 1.2, oi=oi, vol=vol)


class CboePrefilterTests(unittest.TestCase):
    """Regression: the real SPY chain hit the 20k pair-count safety limit.

    Thousands of illiquid/ITM quotes reached the O(n^2) pair enumeration even
    though the scanner's own rules could never admit them into a spread. The
    snapshot pre-filter must drop those quotes before pairing.
    """

    def test_liquidity_prefilter_prevents_pair_count_explosion(self):
        now = datetime(2026, 9, 19, 12, 0, tzinfo=timezone.utc)
        # 182 within-band OTM quotes; only 20 meet the liquidity minimums.
        # 182*181 = 32,942 ordered pairs > maximum_pair_count (20000).
        opts = ([_put(s, oi=5) for s in range(669, 760)]
                + [_call(s, oi=5) for s in range(761, 852)])
        for s in range(750, 760):
            opts.append(_put(s, oi=500))
        for s in range(761, 771):
            opts.append(_call(s, oi=500))
        payload = _cboe_payload(options=opts)
        unfiltered = build_snapshot_from_cboe(payload, "SPY", now)
        self.assertGreater(len(unfiltered.option_quotes), 140)
        filtered = build_snapshot_from_cboe(
            payload, "SPY", now, min_open_interest=100, min_volume=10)
        self.assertEqual(len(filtered.option_quotes), 20)
        # The filtered snapshot's pair count stays under the safety limit.
        n = len(filtered.option_quotes)
        self.assertLessEqual(n * (n - 1), 20000)

    def test_itm_prefilter_drops_itm_keeps_atm(self):
        now = datetime(2026, 9, 19, 12, 0, tzinfo=timezone.utc)
        payload = _cboe_payload(options=[
            _put(770, oi=500),   # ITM put -> dropped
            _put(760, oi=500),   # ATM put -> kept
            _put(750, oi=500),   # OTM put -> kept
            _call(750, oi=500),  # ITM call -> dropped
            _call(760, oi=500),  # ATM call -> kept
            _call(770, oi=500),  # OTM call -> kept
        ])
        snap = build_snapshot_from_cboe(
            payload, "SPY", now, min_open_interest=100, min_volume=10)
        kept = {q.contract_id for q in snap.option_quotes}
        self.assertEqual(len(kept), 4)
        self.assertIn("SPY261023P00760000", kept)
        self.assertIn("SPY261023C00760000", kept)
        self.assertNotIn("SPY261023P00770000", kept)
        self.assertNotIn("SPY261023C00750000", kept)

    def test_real_chain_income_unblocked_by_prefilter(self):
        from hedge_desk.options.scanner import SpreadScanPolicy
        now = datetime(2026, 9, 19, 12, 0, tzinfo=timezone.utc)
        policy = SpreadScanPolicy()
        opts = ([_put(s, oi=5) for s in range(669, 760)]
                + [_call(s, oi=5) for s in range(761, 852)])
        for s in range(750, 760):
            opts.append(_put(s, oi=500))
        for s in range(761, 771):
            opts.append(_call(s, oi=500))
        payload = _cboe_payload(options=opts)

        def transport(url):
            return 200, payload

        result = real_chain_income("SPY", now, transport=transport)
        self.assertEqual(result["mode"], "REAL_CBOE_CHAIN_INCOME")
        self.assertLessEqual(result["pair_count"], policy.maximum_pair_count)


if __name__ == "__main__":
    unittest.main()