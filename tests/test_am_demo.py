"""Deterministic tests for the AM demo render helpers (no network)."""

import unittest

from hedge_desk.am_demo import _csp_block, _csp_top_pick


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
        self.assertIn("<strong>1.28%</strong>", html)
        self.assertNotIn(">0.0128</td>", html)
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


    def test_csp_ranks_fits_by_return_on_capital(self):
        # Best return-on-capital first, not alphabetical.
        csp = {
            "F": {"mode": "CASH_SECURED_PUT", "candidate": {
                "strike": "12", "dte": 34, "net_credit_per_share": "0.10",
                "collateral_required": "1200.00", "return_on_capital": "0.0083"},
                "fits_gp_rules": True, "eval_reasons": []},
            "NKE": {"mode": "CASH_SECURED_PUT", "candidate": {
                "strike": "32", "dte": 34, "net_credit_per_share": "0.41",
                "collateral_required": "3200.00", "return_on_capital": "0.0128"},
                "fits_gp_rules": True, "eval_reasons": []},
            "AAL": {"mode": "CASH_SECURED_PUT", "candidate": {
                "strike": "11.5", "dte": 34, "net_credit_per_share": "0.16",
                "collateral_required": "1150.00", "return_on_capital": "0.0139"},
                "fits_gp_rules": True, "eval_reasons": []},
        }
        html = _csp_block(csp)
        # AAL (1.39%) must appear before NKE (1.28%) before F (0.83%)
        self.assertLess(html.index("<td>AAL</td>"),
                        html.index("<td>NKE</td>"))
        self.assertLess(html.index("<td>NKE</td>"),
                        html.index("<td>F</td>"))
        # top pick is the highest RoC
        top = _csp_top_pick(csp)
        self.assertIn("<strong>Top fit: AAL</strong>", top)
        self.assertIn("1.39%", top)


if __name__ == "__main__":
    unittest.main()