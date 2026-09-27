"""Deterministic tests for the CFTC COT adapter (no network)."""

import json
import unittest

from hedge_desk.cot_desk import CotReport, cot_summary, fetch_cot

_COT_JSON = json.dumps(
    [
        {
            "commodity_name": "GOLD",
            "market_and_exchange_names": "GOLD - COMMODITY EXCHANGE INC",
            "report_date_as_yyyy_mm_dd": "2026-09-22T00:00:00.000",
            "open_interest_all": "412800",
            "noncomm_positions_long_all": "300000",
            "noncomm_positions_short_all": "74147",
            "noncomm_postions_spread_all": "50000",
            "comm_positions_long_all": "80000",
            "comm_positions_short_all": "250000",
        }
    ]
)


def _ok_transport(url):
    assert "publicreporting.cftc.gov" in url
    return 200, _COT_JSON.encode()


def _fail_transport(url):
    return 500, b""


class CotDeskTest(unittest.TestCase):
    def test_fetch_parses_positioning(self):
        reports = fetch_cot(commodity="GOLD", transport=_ok_transport)
        self.assertEqual(len(reports), 1)
        r = reports[0]
        self.assertEqual(r.commodity_name, "GOLD")
        self.assertEqual(r.report_date, "2026-09-22")
        self.assertEqual(r.open_interest, 412800)
        self.assertEqual(r.noncomm_net, 300000 - 74147)
        self.assertEqual(r.comm_net, 80000 - 250000)

    def test_net_pct_oi(self):
        r = CotReport(
            commodity_name="G",
            market_name="M",
            report_date="2026-09-22",
            open_interest=1000,
            noncomm_long=600,
            noncomm_short=100,
            noncomm_spread=0,
            comm_long=100,
            comm_short=600,
            noncomm_net=500,
            comm_net=-500,
        )
        self.assertEqual(r.noncomm_net_pct_oi(), 50.0)

    def test_summary_real(self):
        s = cot_summary("GOLD", transport=_ok_transport)
        self.assertEqual(s["mode"], "REAL_CFTC_COT")
        self.assertEqual(s["noncomm_net"], 225853)
        self.assertAlmostEqual(s["noncomm_net_pct_oi"], 54.71, places=1)

    def test_summary_blocked_on_failure(self):
        s = cot_summary("GOLD", transport=_fail_transport)
        self.assertEqual(s["mode"], "BLOCKED")
        self.assertIn("reason", s)

    def test_summary_blocked_on_empty(self):
        s = cot_summary("GOLD", transport=lambda u: (200, b"[]"))
        self.assertEqual(s["mode"], "BLOCKED")


if __name__ == "__main__":
    unittest.main()
