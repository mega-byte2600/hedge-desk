"""Deterministic reference cases for the Paper Outcome Ledger."""
import json
from datetime import date
from decimal import Decimal

from hedge_desk.premium_ledger import (BASIS, due_outcomes, new_entries, read_ledger, settle,
                                       summarize, update_ledger)


def _cand(cid, score, eligible=True, credit="120.00", max_loss="380.00", exp="2026-12-24"):
    return {"contract_id": cid, "underlying": "SPY", "expiration": exp, "days_to_expiration": 36,
            "net_credit": credit, "maximum_loss": max_loss, "spread_width": "5",
            "premium": {"premium_score": score, "eligible": eligible, "components": {},
                        "inputs": {"short_leg_abs_delta": 0.2}}}


PUT = "SPY261224P00700000--SPY261224P00695000"   # short 700 put, long 695 put
CALL = "SPY261224C00760000--SPY261224C00765000"  # short 760 call, long 765 call


def _entry(cid):
    return new_entries([_cand(cid, 70.0)], [], date(2026, 11, 18), {"vix": "24.6"})[0]


def test_put_spread_reference_cases():
    e = _entry(PUT)
    # Expires above the short strike: keep the full net credit, no closing commission.
    win = settle(e, Decimal("720"))
    assert win["pnl_usd"] == "120.00" and win["expired_worthless"] is True
    assert win["return_on_collateral"] == "0.2400"          # 120 / (120 + 380)
    # Expires between strikes at 698: intrinsic 2.00 -> cost 200 + closing 1.30.
    mid = settle(e, Decimal("698"))
    assert mid["pnl_usd"] == "-81.30"
    # Expires far below: loss capped at width 5 -> cost 500 + 1.30 = max loss + commission.
    loss = settle(e, Decimal("600"))
    assert loss["pnl_usd"] == "-381.30"
    assert loss["basis"] == BASIS and loss["trade_authorized"] is False


def test_call_spread_reference_case():
    e = _entry(CALL)
    assert settle(e, Decimal("750"))["pnl_usd"] == "120.00"
    assert settle(e, Decimal("762.50"))["pnl_usd"] == "-131.30"   # 120 - 250 - 1.30


def test_entries_only_for_eligible_and_never_duplicated():
    rows = new_entries([_cand(PUT, 70.0), _cand(CALL, 90.0, eligible=False)], [], date(2026, 11, 18), {})
    assert [r["contract_id"] for r in rows] == [PUT]
    again = new_entries([_cand(PUT, 72.0)], rows, date(2026, 11, 19), {})
    assert again == []


def test_missing_expiry_close_stays_open_never_guessed():
    rows = [_entry(PUT)]
    assert due_outcomes(rows, {}, date(2026, 12, 30)) == []                    # no close on record
    assert due_outcomes(rows, {"2026-12-24": "710"}, date(2026, 12, 23)) == []  # not expired yet
    out = due_outcomes(rows, {"2026-12-24": "710"}, date(2026, 12, 24))
    assert len(out) == 1 and out[0]["pnl_usd"] == "120.00"


def test_update_is_append_only_and_summary_bands(tmp_path):
    led = tmp_path / "ledger.jsonl"
    s1 = update_ledger(led, [_cand(PUT, 75.0), _cand(CALL, 50.0)], {}, date(2026, 11, 18), {"vix": "24.6"})
    assert s1["entries"] == 2 and s1["open"] == 2 and s1["entries_added_tonight"] == 2
    first_lines = led.read_text().splitlines()
    s2 = update_ledger(led, [], {"2026-12-24": "720"}, date(2026, 12, 24))
    assert led.read_text().splitlines()[:2] == first_lines            # never rewritten
    assert s2["settled"] == 2 and s2["outcomes_settled_tonight"] == 2
    assert s2["by_score_band"]["score >= 70"]["n"] == 1 and s2["by_score_band"]["< 55"]["n"] == 1
    assert s2["overall"]["win_rate"] == "1.000" and s2["trade_authorized"] is False
    assert all(json.loads(x)["trade_authorized"] is False for x in led.read_text().splitlines())
    assert summarize(read_ledger(led)) ["entries"] == 2


def test_dashboard_ledger_panel_renders_bands_and_empty_state():
    import importlib.util
    from pathlib import Path
    spec = importlib.util.spec_from_file_location(
        "bpd", Path(__file__).resolve().parents[1] / "scripts" / "build_plotly_dashboard.py")
    bpd = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bpd)
    assert "Paper track record starts" in bpd.premium_ledger_panel(None)
    rows = [_entry(PUT), settle(_entry(PUT), Decimal("720"))]
    html = bpd.premium_ledger_panel(summarize(rows))
    assert "score &gt;= 70" in html or "score >= 70" in html
    assert "1.000" in html and "$120.00" in html


def test_ledger_rebuilds_from_committed_reports_when_jsonl_is_lost(tmp_path):
    """Durability: tonight's rows ride in the dated report the batch always commits."""
    from hedge_desk.premium_ledger import rebuild_from_reports
    led = tmp_path / "ledger.jsonl"
    r1 = update_ledger(led, [_cand(PUT, 75.0)], {}, date(2026, 11, 18))
    r2 = update_ledger(led, [_cand(PUT, 75.0)], {"2026-12-24": "720"}, date(2026, 12, 24))
    (tmp_path / "am-report-2026-11-18.json").write_text(json.dumps({"premium_ledger": r1}))
    (tmp_path / "am-report-2026-12-24.json").write_text(json.dumps({"premium_ledger": r2}))
    rebuilt = rebuild_from_reports(sorted(tmp_path.glob("am-report-*.json")))
    assert rebuilt == read_ledger(led)
    assert summarize(rebuilt)["settled"] == 1


def _sheet(vault, strike, dte=36, when="2026-11-18T21:00:00+00:00", strategy="CREDIT_SPREAD"):
    from datetime import datetime
    from hedge_desk.yellow_sheet import record_yellow_sheet
    return record_yellow_sheet(vault, symbol="SPY", strategy=strategy, strike=strike, dte=dte,
                               thesis="Sell the 700/695 put spread at 20 delta.",
                               invalidation="SPY closes below 700 before expiry.",
                               decision="PAPER_OPEN", recorded_at=datetime.fromisoformat(when))


def test_yellow_sheets_link_to_ledger_outcomes_read_only(tmp_path):
    from hedge_desk.premium_ledger import link_yellow_sheets
    from hedge_desk.yellow_sheet import read_yellow_sheets
    vault, led = tmp_path / "ys.jsonl", tmp_path / "ledger.jsonl"
    _sheet(vault, "700")                                  # matches PUT short strike 700, exp 12-24 (36d)
    _sheet(vault, "760")                                  # matches CALL short strike 760
    _sheet(vault, "650")                                  # no ledger entry
    _sheet(vault, "33", strategy="CASH_SECURED_PUT")      # not a spread: ignored
    before = vault.read_text()
    update_ledger(led, [_cand(PUT, 75.0), _cand(CALL, 60.0)], {}, date(2026, 11, 18))
    update_ledger(led, [], {"2026-12-24": "720"}, date(2026, 12, 24))
    out = link_yellow_sheets(read_yellow_sheets(vault), read_ledger(led))
    assert vault.read_text() == before                   # vault untouched, hashes still verify
    by_strike = {r["strike"]: r for r in out["rows"]}
    assert set(by_strike) == {"700", "760", "650"}
    assert by_strike["700"]["link"] == "LINKED" and by_strike["700"]["status"] == "SETTLED"
    assert by_strike["700"]["pnl_usd"] == "120.00" and by_strike["700"]["thesis_held"] is True
    assert by_strike["760"]["thesis_held"] is True       # 720 close: call spread expires worthless
    assert by_strike["650"]["link"] == "NO_LEDGER_MATCH"
    assert out["linked"] == 2 and out["settled"] == 2 and out["thesis_held"] == 2
    assert out["trade_authorized"] is False


def test_yellow_sheet_link_respects_date_and_dte_windows(tmp_path):
    from hedge_desk.premium_ledger import link_yellow_sheets
    from hedge_desk.yellow_sheet import read_yellow_sheets
    vault, led = tmp_path / "ys.jsonl", tmp_path / "ledger.jsonl"
    _sheet(vault, "700", when="2026-11-30T21:00:00+00:00")   # 12 days after entry: outside window
    _sheet(vault, "700", dte=90)                              # wrong expiry for the DTE
    update_ledger(led, [_cand(PUT, 75.0)], {}, date(2026, 11, 18))
    out = link_yellow_sheets(read_yellow_sheets(vault), read_ledger(led))
    assert [r["link"] for r in out["rows"]] == ["NO_LEDGER_MATCH", "NO_LEDGER_MATCH"]
