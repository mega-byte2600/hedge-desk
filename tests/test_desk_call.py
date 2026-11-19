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


def test_ranks_by_ev_then_pop_and_prints_exits():
    call = build_desk_call(_report([_s("x", "-9.0", "0.8"), _s("y", "-2.0", "0.6"),
                                    _s("z", "-2.0", "0.7"), _s("w", "-20", "0.9")]))
    assert [s["contract_id"] for s in call["shortlist"]] == ["z", "y", "x"]
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
