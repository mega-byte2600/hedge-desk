"""Deterministic tests for the cash-secured-put scanner (no network)."""

import json
import unittest

from hedge_desk.csp_scan import scan_cash_secured_put


def _chain(payload):
    return lambda url: (200, json.dumps(payload).encode("utf-8"))


def _option(contract, bid, ask, oi=500, vol=200):
    return {
        "option": contract, "bid": bid, "ask": ask, "bid_size": 25, "ask_size": 30,
        "open_interest": oi, "volume": vol,
    }


def _spy_put_chain():
    return {
        "data": {
            "symbol": "SPY", "current_price": "100.00", "bid": "100.00", "ask": "100.00",
            "options": [
                # 30-45 DTE put at ~90 (10% OTM), real executable bid
                _option("SPY261023P00090000", 1.19, 1.25),
                _option("SPY261023P00095000", 2.00, 2.10),
                # a call shouldn't match the put filter
                _option("SPY261023C00110000", 3.00, 3.20),
            ],
        }
    }


class CspScanTests(unittest.TestCase):
    def test_finds_10pct_otm_put(self):
        from datetime import datetime, timezone
        r = scan_cash_secured_put("SPY", datetime(2026, 9, 19, tzinfo=timezone.utc),
                                  transport=_chain(_spy_put_chain()))
        self.assertEqual(r["mode"], "CASH_SECURED_PUT")
        c = r["candidate"]
        self.assertEqual(c["strike"], "90")
        self.assertEqual(c["net_credit_per_share"], "1.19")
        self.assertIn("CAPITAL_OVER_5K", r["eval_reasons"])
        self.assertEqual(r["survivability"], "INDETERMINATE")
        self.assertFalse(r["trade_authorized"])

    def test_empty_chain_no_candidate(self):
        from datetime import datetime, timezone
        r = scan_cash_secured_put("SPY", datetime(2026, 9, 19, tzinfo=timezone.utc),
                                  transport=_chain({"data": {"symbol": "SPY", "current_price": "100", "options": []}}))
        self.assertEqual(r["mode"], "NO_CANDIDATE")

    def test_blocked_on_transport_error(self):
        from datetime import datetime, timezone
        r = scan_cash_secured_put("SPY", datetime(2026, 9, 19, tzinfo=timezone.utc),
                                  transport=lambda url: (500, b""))
        self.assertEqual(r["mode"], "BLOCKED")


if __name__ == "__main__":
    unittest.main()