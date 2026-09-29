"""Tests for the Plotly dashboard builder: required panels, escaping, BLOCKED paths."""

import json
import tempfile
import unittest
from pathlib import Path

import scripts.build_plotly_dashboard as dash


def _report(**overrides):
    base = {
        "schema_version": "hedge-desk-nightly-1.0.0",
        "mode": "REAL_EOD_NIGHTLY",
        "generated_at": "2026-09-26T14:35:09+00:00",
        "candidate_count": 1,
        "eod_batch_status": "READY_FOR_RESEARCH",
        "data_freshness": {"expected_trading_day": "2026-09-25", "is_current": True, "note": "ok"},
        "candidates": [{"symbol": "AAL", "requirement": "1200.00", "strategy": "CASH_SECURED_PUT"}],
        "cash_secured_put_scan": {
            "AAL": {
                "mode": "CASH_SECURED_PUT",
                "fits_gp_rules": True,
                "fit_reasons": ["ROC_ABOVE_MIN"],
                "candidate": {"return_on_capital": "0.012"},
            }
        },
        "chain_income": {"SPY": {"mode": "BLOCKED", "reason": "option snapshot exceeds pair-count safety limit",
                                 "gated_income_structures": []}},
        "features": {"features": {"AAL": {"return_1d": "0.01", "return_5d": "0.02",
                                          "return_21d": "0.03", "realized_vol_21d": "0.02",
                                          "range_position_21d": "0.5"}}},
        "rates_environment": {"mode": "REAL_FRED_RATES"},
        "vix_regime": {"mode": "REAL_VIX"},
        "macro_environment": {"mode": "BLOCKED", "reason": "x"},
        "oil_market": {"mode": "REAL_YAHOO_WTI"},
        "earnings_actuals": {},
        "market_context": {
            "status": "LIVE",
            "sources": {
                "nasdaq-quotes": {
                    "provider_id": "nasdaq", "status": "LIVE", "observation_count": 2,
                    "observations": [
                        {"symbol": "SPY", "lastSalePrice": "$765.05", "percentageChange": "-0.07%",
                         "lastTradeTimestamp": "Sep 28, 2026 4:53 PM ET", "isRealTime": True},
                        {"symbol": "AAPL", "lastSalePrice": "$338.36", "percentageChange": "+0.10%",
                         "lastTradeTimestamp": "Sep 28, 2026 4:53 PM ET", "isRealTime": True},
                    ],
                },
                "ecb-fx": {
                    "provider_id": "ecb-fx", "status": "LIVE", "observation_count": 1,
                    "observations": [{"currency": "USD", "rate": "1.1723", "date": "2026-09-28", "base": "EUR"}],
                },
                "treasury-rates": {
                    "provider_id": "fred", "status": "LIVE", "observation_count": 3,
                    "observations": [
                        {"tenor": "DGS2", "date": "2026-09-25", "value": "4.10"},
                        {"tenor": "DGS10", "date": "2026-09-25", "value": "5.17"},
                        {"tenor": "DGS30", "date": "2026-09-25", "value": "5.52"},
                    ],
                },
                "fred": {"provider_id": "fred", "status": "LIVE", "observation_count": 5},
                "cftc-cot": {"provider_id": "cftc-cot", "status": "BLOCKED", "reason_code": "UPSTREAM_OR_PARSE_FAILURE",
                             "detail": "cftc-cot fetch failed (status 0)"},
            },
        },
        "paper_outcome_summary": {"entry_count": 3, "outcome_counts": {"WIN": 2}},
        "yellow_sheets": {"sheet_count": 1, "by_decision": {"HOLD": 1}},
        "series": {},
    }
    base.update(overrides)
    return base


class DashboardBuildTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self._old_report, self._old_out = dash.REPORT, dash.OUT
        dash.REPORT = Path(self.tmp.name) / "report.json"
        dash.OUT = Path(self.tmp.name) / "dash.html"

    def tearDown(self):
        dash.REPORT, dash.OUT = self._old_report, self._old_out
        self.tmp.cleanup()

    def _build(self, **overrides):
        dash.REPORT.write_text(json.dumps(_report(**overrides)))
        dash.build()
        return dash.OUT.read_text()

    def test_builds_required_panels(self):
        html = self._build()
        for div in ("ch_csp", "ch_cands", "ch_heatmap"):
            self.assertIn(div, html)
        self.assertIn("Source health", html)

    def test_blocked_chain_renders_honest_panel(self):
        html = self._build()
        self.assertIn("pair-count safety limit", html)
        self.assertNotIn("Traceback", html)

    def test_missing_series_renders_honest_note(self):
        html = self._build()
        self.assertIn("rebuild the overnight report", html)

    def test_macro_panel_renders_cells_not_none(self):
        # Regression: a truncated macro_panel once rendered the literal
        # string "None" in the Macro backdrop card.
        html = self._build(
            vix_regime={"mode": "REAL_VIX", "last_close": "14.9", "regime": "LOW"},
            oil_market={"mode": "REAL_YAHOO_WTI", "last_close": "64.5"},
            macro_environment={"mode": "BLOCKED", "reason": "withheld"},
        )
        self.assertNotIn("Macro backdrop</h3>None", html)
        self.assertIn("VIX (LOW)", html)
        self.assertIn("withheld — refetch pending", html)

    def test_earnings_eps_chart_draws_real_quarters(self):
        html = self._build(
            earnings_actuals={
                "0000320193": {
                    "mode": "REAL_EDGAR_EARNINGS",
                    "observation": {
                        "latest_quarterly_eps": 2.03,
                        "latest_quarterly_period": "2026-06-27",
                        "prior_quarterly_eps": 2.02,
                        "prior_quarterly_period": "2026-03-28",
                    },
                }
            }
        )
        self.assertIn("ch_earnings_eps", html)
        self.assertIn("AAPL", html)

    def test_earnings_eps_chart_empty_state_is_honest(self):
        html = self._build(earnings_actuals={})
        self.assertIn("no real quarterly EPS observations", html)

    def test_carpe_data_panels_render_live_feeds(self):
        html = self._build()
        # Nasdaq watchlist quotes
        self.assertIn("$765.05", html)
        self.assertIn("Nasdaq", html)
        # Treasury curve chart (Plotly) with honest FRED attribution
        self.assertIn("ch_treasury_curve", html)
        self.assertIn("FRED DGS", html)
        # ECB FX panel
        self.assertIn("EUR/USD", html)
        self.assertIn("1.1723", html)
        # Public data plane health table shows live + blocked honestly
        self.assertIn("Quotes (Nasdaq)", html)
        self.assertIn("Blocked", html)

    def test_carpe_data_panels_degrade_honestly_without_market_context(self):
        html = self._build(market_context={})
        self.assertIn("unavailable in this batch", html)
        self.assertNotIn("$765.05", html)

    def test_global_markets_panels_render_live_world_bank_and_treasury(self):
        # World Bank GDP + Treasury auctions are keyless global feeds surfaced
        # on the dashboard. When LIVE they draw real charts/tables; the fixtures
        # are captured from the live API, never invented.
        html = self._build(market_context={
            "status": "LIVE",
            "sources": {
                "world-bank": {
                    "provider_id": "world-bank", "status": "LIVE", "observation_count": 5,
                    "observations": [
                        {"countryiso3code": "USA", "date": "2021", "value": 23725645000000},
                        {"countryiso3code": "USA", "date": "2022", "value": 26054614000000},
                    ],
                },
                "treasury-fiscaldata": {
                    "provider_id": "treasury-fiscaldata", "status": "LIVE",
                    "observation_count": 2,
                    "observations": [
                        {"security_type": "Treasury Note", "auction_date": "2026-09-28",
                         "high_investment_rate": "4.100", "maturity_date": "2028-09-30"},
                        {"security_type": "Treasury Bill", "auction_date": "2026-09-27",
                         "high_investment_rate": "4.550", "maturity_date": "2026-12-24"},
                    ],
                },
            },
        })
        self.assertIn("ch_world_gdp", html)
        self.assertIn("World Bank GDP", html)
        self.assertIn("Treasury auctions", html)
        self.assertIn("Treasury Note", html)
        self.assertIn("4.100", html)

    def test_global_markets_panels_degrade_when_sources_missing(self):
        html = self._build(market_context={"status": "LIVE", "sources": {}})
        self.assertIn("World Bank indicator unavailable", html)
        self.assertIn("Treasury fiscal data unavailable", html)

    def test_every_rendered_visual_states_its_source(self):
        # The user requires every dashboard visual to be annotated with its
        # data source so any number can be traced back to its origin.
        html = self._build(
            earnings_actuals={
                "0000320193": {
                    "mode": "REAL_EDGAR_EARNINGS",
                    "observation": {
                        "latest_quarterly_eps": 2.03,
                        "latest_quarterly_period": "2026-06-27",
                        "prior_quarterly_eps": 2.02,
                        "prior_quarterly_period": "2026-03-28",
                    },
                }
            },
            series={
                "symbols": {"AAL": [["2026-09-01", 10.0], ["2026-09-02", 11.0]]},
                "vix": [["2026-09-01", 14.0], ["2026-09-02", 15.0]],
                "wti": [["2026-09-01", 64.0], ["2026-09-02", 65.0]],
                "treasury_10y": [["2026-09-01", 4.5], ["2026-09-02", 4.6]],
            },
        )
        import re

        # Every Plotly div id that rendered must be followed by a source note.
        for div_id in set(re.findall(r'id="(ch_[a-z_]+)"', html)):
            i = html.find(f'id="{div_id}"')
            following = html[i:i + 200000]
            j = following.find("class='src-note'")
            self.assertGreater(
                j, 0, f"chart {div_id} renders without a source annotation")
        self.assertGreaterEqual(html.count("class='src-note'"), 8)
        for src in ("Yahoo Finance", "Cboe", "SEC EDGAR",
                    "FRED", "paper-outcomes.jsonl"):
            self.assertIn(src, html)

    def test_html_escapes_untrusted_text(self):
        html = self._build(chain_income={
            "SPY": {"mode": "BLOCKED", "reason": "<script>alert(1)</script>",
                    "gated_income_structures": []}})
        self.assertNotIn("<script>alert(1)</script>", html)
        self.assertIn("&lt;script&gt;", html)

    def test_missing_report_exits(self):
        with self.assertRaises(SystemExit):
            dash.build()

    def test_malformed_entries_do_not_crash_build(self):
        # Junk numerics / missing keys in mode-matching sections must be
        # skipped, never abort the nightly build under set -e.
        html = self._build(
            cash_secured_put_scan={
                "AAL": {"mode": "CASH_SECURED_PUT", "candidate": {}},
                "ZZZ": {"mode": "CASH_SECURED_PUT",
                        "candidate": {"return_on_capital": "not-a-number"}},
                "OK": {"mode": "CASH_SECURED_PUT", "fits_gp_rules": True,
                       "candidate": {"return_on_capital": "0.012"}},
            },
            candidates=[
                {"symbol": "AAL"},  # missing requirement
                {"requirement": "abc", "strategy": "CASH_SECURED_PUT"},  # no symbol, junk number
                {"symbol": "MSFT", "requirement": "2500.00", "strategy": "CASH_SECURED_PUT"},
            ],
            chain_income={"SPY": {
                "mode": "REAL_CBOE_CHAIN_INCOME",
                "underlying_bid": "772.0", "underlying_ask": "772.04",
                "gated_income_structures": [
                    {"expiration": "2026-10-30", "return_on_risk": "junk",
                     "gate_decision": "INDETERMINATE"},
                    {"expiration": "2026-10-30", "return_on_risk": "0.05",
                     "gate_decision": "INDETERMINATE"},
                ]}},
            series={"treasury_10y": [["2026-09-25", "junk"], ["2026-09-24", "5.18"]],
                    "vix": [["2026-09-25", None]],
                    "wti": [["2026-09-25", "nan"]]},
        )
        self.assertNotIn("Traceback", html)
        self.assertIn("ch_csp", html)
        self.assertIn("ch_cands", html)
        # The one valid CSP row and the one valid candidate still render.
        self.assertIn("OK", html)
        self.assertIn("MSFT", html)


if __name__ == "__main__":
    unittest.main()
