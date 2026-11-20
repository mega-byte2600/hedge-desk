from hedge_desk.desk_call import build_desk_call


def _report(structs, current=True, batch="READY_FOR_RESEARCH"):
    return {"data_freshness": {"is_current": current, "as_of": "2026-11-17"},
            "eod_batch_status": batch,
            "vix_regime": {"regime": "ELEVATED", "last_close": "25.459999084472656"},
            "chain_income": {"SPY": {"gate_demo_account_equity": 100000,
                                     "gated_income_structures": structs}}}


def _s(cid, ev=None, pop=None, ror="0.5", decision="INDETERMINATE"):
    d = {"contract_id": cid, "net_credit": "100.00", "maximum_loss": "400.00",
         "break_even": "700", "return_on_risk": ror, "gate_decision": decision,
         "gate_reasons": ["MISSING_REAL_RISK_INPUT"], "expiration": "2026-12-24",
         "days_to_expiration": 36}
    if ev is not None:
        d.update(risk_neutral_ev=ev, probability_of_profit=pop)
    return d


def test_indeterminate_gate_is_always_no_trade():
    call = build_desk_call(_report([_s("a"), _s("b")]))
    assert call["action"] == "NO_TRADE" and call["trade_authorized"] is False
    assert any(r.startswith("RISK_GATE_NOT_APPROVED:MISSING_REAL_RISK_INPUT") for r in call["reason_codes"])
    assert call["context"]["vix_close"] == "25.46"


def test_ranks_by_return_on_risk_and_prints_exits():
    call = build_desk_call(_report([_s("x", "-9.0", "0.8", ror="0.9"), _s("y", "-2.0", "0.6", ror="0.3"),
                                    _s("z", "-2.0", "0.7", ror="0.5"), _s("w", "-20", "0.9", ror="0.1")]))
    assert [s["contract_id"] for s in call["shortlist"]] == ["x", "z", "y"]
    assert "risk_neutral_ev" not in call["shortlist"][0]  # SOUL rule 4: never in the payload
    top = call["shortlist"][0]
    assert top["take_profit_at_credit_captured"] == "50.00"
    assert top["stop_at_loss"] == "200.00"
    assert top["max_loss_pct_demo_equity"] == "0.40"
    assert top["invalidation_underlying_through"] == "700"


def test_approved_and_current_yields_paper_candidate_only():
    call = build_desk_call(_report([_s("ok", "-1", "0.7", decision="APPROVED")]))
    assert call["action"] == "PAPER_CANDIDATE" and call["trade_authorized"] is False
    stale = build_desk_call(_report([_s("ok", decision="APPROVED")], current=False))
    assert stale["action"] == "NO_TRADE" and "DATA_NOT_CURRENT" in stale["reason_codes"]


def test_premium_score_ranks_when_present():
    a = _s("a", ror="0.9"); a["premium"] = {"premium_score": 40.0, "components": {}, "management": {"time_exit_dte": 21}}
    b = _s("b", ror="0.2"); b["premium"] = {"premium_score": 82.5, "components": {}, "management": {"time_exit_dte": 21}}
    call = build_desk_call(_report([a, b]))
    assert [s["contract_id"] for s in call["shortlist"]] == ["b", "a"]
    assert call["shortlist"][0]["premium_score"] == 82.5 and "premium score" in call["ranked_by"]


def test_shortlist_dedupes_short_leg_ranks_eligible_first_and_sizes_under_2pct():
    def prem(score, eligible):
        return {"premium_score": score, "eligible": eligible, "components": {},
                "eligibility_reasons": [] if eligible else ["DELTA_OUT_OF_BAND"], "management": {"time_exit_dte": 21}}
    atm1 = _s("SPY261224C00740000--SPY261224C00747000"); atm1["premium"] = prem(90.0, False)
    atm2 = _s("SPY261224C00740000--SPY261224C00748000"); atm2["premium"] = prem(89.0, False)
    good = _s("SPY261224P00700000--SPY261224P00695000"); good["premium"] = prem(60.0, True)
    call = build_desk_call(_report([atm1, atm2, good]))
    ids = [s["contract_id"] for s in call["shortlist"]]
    assert ids[0].startswith("SPY261224P00700000")          # eligible beats higher-scored ineligible
    assert len([i for i in ids if i.startswith("SPY261224C00740000")]) == 1  # one row per short leg
    top = call["shortlist"][0]
    assert top["collateral_per_contract"] == "500.00"       # credit 100 + max loss 400
    assert top["example_max_contracts_2pct_demo_equity"] == 5  # 2% of 100k / 400


def test_no_probability_fields_survive_into_the_delayed_data_payload():
    """SOUL rule 4: delayed Cboe data must not carry probability/EV claims."""
    call = build_desk_call(_report([_s("a", "-1.0", "0.8")]))
    for row in call["shortlist"]:
        assert "probability_of_profit" not in row and "risk_neutral_ev" not in row
