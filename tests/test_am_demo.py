"""Deterministic tests for the AM demo render helpers (no network)."""

import unittest

from hedge_desk.am_demo import _csp_block


class AmDemoRenderTests(unittest.TestCase):
    def test_csp_block_renders_roc_as_percent_not_fraction(self):
        # return_on_capital is a decimal fraction (0.0128); the GP-facing page
        # must read 1.28%, not a misread 0.0128%.
        csp = {
            "NKE": {
                "mode": "CASH_SECURED_PUT",
                "candidate": {
                    "strike": "32", "dte": 34, "net_credit_per_share": "0.41",
                    "collateral_required": "3200.00", "return_on_capital": "0.0128",
                },
                "fits_gp_rules": True,
                "eval_reasons": [],
            }
        }
        html = _csp_block(csp)
        self.assertIn("<td>1.28%</td>", html)
        self.assertNotIn("<td>0.0128</td>", html)
        self.assertIn("badge ok'>FITS", html)

    def test_csp_block_escapes_missing_roc(self):
        csp = {
            "NKE": {
                "mode": "CASH_SECURED_PUT",
                "candidate": {"strike": "32", "dte": 34, "return_on_capital": None},
                "fits_gp_rules": False,
                "eval_reasons": ["RETURN_NOT_IN_GP_BAND"],
            }
        }
        html = _csp_block(csp)
        self.assertIn("badge warn'>no", html)
        self.assertIn("RETURN_NOT_IN_GP_BAND", html)


if __name__ == "__main__":
    unittest.main()