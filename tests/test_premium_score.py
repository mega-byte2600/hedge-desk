import math

from hedge_desk.premium_score import (annualized_rv, parse_occ, rank_chain_income,
                                      score_structure, short_leg_delta)


def _s(cid, dte, credit, max_loss, iv, ror="0.5"):
    return {"contract_id": cid, "days_to_expiration": dte, "net_credit": str(credit),
            "maximum_loss": str(max_loss), "short_leg_iv": str(iv), "return_on_risk": ror}


def test_occ_and_delta():
    assert parse_occ("SPY261224P00680000") == {"type": "P", "strike": 680.0}
    d = short_leg_delta(737.5, 680, 36 / 365, 0.22, False)
    assert 0.05 < d < 0.2
    assert abs(annualized_rv(0.01) - 0.01 * math.sqrt(252)) < 1e-12


def test_sweet_spot_beats_near_money_coin_flip():
    spot = 737.5
    sweet = _s("SPY261224P00700000--SPY261224P00695000", 36, 120, 380, 0.24)   # ~20-25 delta
    coin = _s("SPY261224C00740000--SPY261224C00747000", 36, 341.7, 358.3, 0.16)  # ~ATM
    weekly = _s("SPY261127P00700000--SPY261127P00695000", 8, 60, 440, 0.24)
    s1, s2, s3 = (score_structure(x, spot, 0.15) for x in (sweet, coin, weekly))
    assert s1["components"]["strike_placement"] == 1.0
    assert s2["components"]["strike_placement"] < 0.5
    assert s3["components"]["entry_window"] == 0.0
    assert s1["premium_score"] > s3["premium_score"]
    assert s1["management"]["time_exit_dte"] == 21 and s1["management"]["days_until_time_exit"] == 15


def test_missing_rv_is_flagged_not_invented_and_ranking_is_by_score():
    chain = {"underlying_bid": "737", "underlying_ask": "738",
             "income_structures": [_s("SPY261224C00740000--SPY261224C00747000", 36, 341.7, 358.3, 0.16, "0.95"),
                                   _s("SPY261224P00700000--SPY261224P00695000", 36, 120, 380, 0.24, "0.31")]}
    ranked = rank_chain_income(chain, None)
    assert "RV_UNAVAILABLE" in ranked["income_structures"][0]["premium"]["flags"]
    assert ranked["income_structures"][0]["premium"]["components"]["vol_edge"] == 0.0
    assert ranked["ranking"]["dividend_yield"] == 0.0  # no symbol -> no assumed yield
    assert ranked["income_structures"][0]["contract_id"].startswith("SPY261224P00700000")
    assert ranked["ranking"]["by"] == "premium_score"
    scores = [r["premium"]["premium_score"] for r in ranked["income_structures"]]
    assert scores == sorted(scores, reverse=True)


def test_merton_delta_matches_win_probability_model():
    from hedge_desk.risk.win_probability import _bs_put_delta
    d = short_leg_delta(737.5, 700, 36 / 365, 0.22, False, rate=0.038, dividend_yield=0.012)
    assert abs(d - abs(_bs_put_delta(737.5, 700, 36 / 365, 0.038, 0.22, 0.012))) < 1e-12
    assert d != short_leg_delta(737.5, 700, 36 / 365, 0.22, False)


def test_spy_gets_its_dividend_assumption_and_annualized_ror():
    chain = {"symbol": "SPY", "underlying_bid": "737", "underlying_ask": "738",
             "income_structures": [_s("SPY261224P00700000--SPY261224P00695000", 36, 120, 380, 0.24)]}
    r = rank_chain_income(chain, 0.15, rate=0.038)
    p = r["income_structures"][0]["premium"]
    assert r["ranking"]["dividend_yield"] == 0.012 and p["inputs"]["rate"] == 0.038
    assert abs(p["inputs"]["annualized_return_on_risk"] - p["inputs"]["monthly_return_on_risk"] * 365 / 30) < 1e-3


def test_trader_panel_renders_ranked_components_and_empty_state():
    import importlib.util
    from pathlib import Path
    spec = importlib.util.spec_from_file_location(
        "bpd", Path(__file__).resolve().parents[1] / "scripts" / "build_plotly_dashboard.py")
    bpd = importlib.util.module_from_spec(spec); spec.loader.exec_module(bpd)
    assert "next nightly run" in bpd.premium_candidates_panel({})
    chain = {"symbol": "SPY", "underlying_bid": "737", "underlying_ask": "738",
             "income_structures": [_s("SPY261224P00700000--SPY261224P00695000", 36, 120, 380, 0.24)]}
    html = bpd.premium_candidates_panel({"SPY": rank_chain_income(chain, 0.15, rate=0.038)})
    assert "premium-candidates" in html and "Return on collateral" in html and "16-30 delta" in html


def test_out_of_band_or_no_edge_can_never_rank_first():
    """GP brief as hard constraints (review r5): a 40-delta coin flip or a
    negative-VRP structure must rank below any eligible candidate."""
    coin = _s("SPY261224C00740000--SPY261224C00747000", 36, 341.7, 358.3, 0.18)   # ~ATM, high RoC
    good = _s("SPY261224P00690000--SPY261224P00685000", 36, 60, 440, 0.26)       # ~20 delta put
    chain = {"symbol": "SPY", "underlying_bid": "737", "underlying_ask": "738", "income_structures": [coin, good]}
    hi_rv = rank_chain_income(chain, 0.30, rate=0.038)          # IV < RV: nobody has an edge
    assert all(not r["premium"]["eligible"] for r in hi_rv["income_structures"])
    lo_rv = rank_chain_income(chain, 0.12, rate=0.038)          # IV > RV: edge exists
    top = lo_rv["income_structures"][0]
    assert top["contract_id"].startswith("SPY261224P00690000") and top["premium"]["eligible"]
    coin_p = next(r for r in lo_rv["income_structures"] if r["contract_id"].startswith("SPY261224C"))["premium"]
    assert "DELTA_OUT_OF_BAND" in coin_p["eligibility_reasons"]


def test_time_value_is_return_on_collateral():
    p = score_structure(_s("SPY261224P00700000--SPY261224P00695000", 30, 100, 400, 0.24), 737.5, 0.15)
    assert p["inputs"]["collateral_usd"] == 500 and p["inputs"]["return_on_collateral"] == 0.2
    assert abs(p["components"]["time_value"] - 0.2 / 0.30) < 1e-3
