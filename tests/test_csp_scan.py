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
        # Return on capital deployed = credit/strike (1.19/90 ~ 1.32%), not
        # credit/(strike*100) which would report ~0.013%.
        self.assertEqual(c["return_on_capital"], "0.0134")
        self.assertEqual(r["fits_gp_rules"], False)
        self.assertIn("CAPITAL_OVER_5K", r["eval_reasons"])
        self.assertNotIn("RETURN_NOT_IN_GP_BAND", r["eval_reasons"])
        self.assertEqual(r["survivability"], "INDETERMINATE")
        self.assertFalse(r["trade_authorized"])

    def test_sub5k_put_in_gp_band_fits_rules(self):
        from datetime import datetime, timezone
        # 32 strike put, bid 0.41 -> return on capital 1.28% (in 0.5-2% band),
        # collateral $3,200 (under $5k) -> fits_gp_rules must be True.
        payload = {
            "data": {
                "symbol": "NKE", "current_price": "36.00", "bid": "36.00", "ask": "36.10",
                "options": [
                    _option("NKE261023P00032000", 0.41, 0.45),
                ],
            }
        }
        r = scan_cash_secured_put("NKE", datetime(2026, 9, 19, tzinfo=timezone.utc),
                                  transport=_chain(payload))
        self.assertEqual(r["mode"], "CASH_SECURED_PUT")
        c = r["candidate"]
        self.assertEqual(c["strike"], "32")
        self.assertEqual(c["collateral_required"], "3159.00")
        self.assertEqual(c["return_on_capital"], "0.0130")
        self.assertTrue(r["fits_gp_rules"])
        self.assertEqual(r["eval_reasons"], [])

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