"""
test_parity.py — Deterministic workbook-parity suite.

Compares engine outputs against cached Excel values
(fixtures/rental_cached.json, fixtures/analysis_cached.json)
extracted via openpyxl data_only=True.

Money tolerance: $0.01 absolute. Rates: 1e-9.
Every mismatch is reported; the suite fails on any mismatch.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rental_engine import (
    RentalInputs, project, xirr_at_select, irr_ba6, annual_rollup,
    sensitivity_cap_rate, sensitivity_interest_rate, _expense_for,
    N_RETURN_MONTHS,
)
from analysis_engine import AnalysisInputs, AnalysisModel, r100

FIX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fixtures")
rental_fx = json.load(open(os.path.join(FIX, "rental_cached.json")))
analysis_fx = json.load(open(os.path.join(FIX, "analysis_cached.json")))

PASS = 0
FAIL = 0
FAILURES = []


def check(name, got, want, tol=0.01):
    global PASS, FAIL
    if want is None or isinstance(want, str):
        return  # blank/text cell — engine None matches implicitly
    if got is None:
        FAIL += 1
        FAILURES.append(f"{name}: engine None, want {want}")
        return
    if abs(got - want) <= tol:
        PASS += 1
    else:
        FAIL += 1
        FAILURES.append(f"{name}: got {got!r} want {want!r} diff {got - want!r}")


def check_rate(name, got, want):
    check(name, got, want, tol=1e-9)


# ── Rental: Model_Mthly cell-by-cell ──────────────────────────────
def test_rental_monthly():
    m = rental_fx["Model_Mthly"]
    inp = RentalInputs()
    rows = project(inp)
    exp_cols = ["G", "H", "I", "J", "K", "L", "M", "N", "O"]
    for i, r in enumerate(rows):
        row = i + 5  # Excel row
        mo = r.m
        check(f"C{row} rent", r.gross_rent, m.get(f"C{row}"))
        check(f"D{row} vacancy", r.vacancy_loss, m.get(f"D{row}"))
        check(f"E{row} gross income", r.gross_income, m.get(f"E{row}"))
        for ci, col in enumerate(exp_cols):
            check(f"{col}{row} expense", _expense_for(inp.expenses[ci], mo, r.gross_income),
                  m.get(f"{col}{row}"))
        check(f"P{row} total exp", r.expenses, m.get(f"P{row}"))
        check(f"Q{row} NOI", r.noi, m.get(f"Q{row}"))
        check(f"S{row} interest", r.mortgage_interest, m.get(f"S{row}"))
        check(f"T{row} principal", r.mortgage_principal, m.get(f"T{row}"))
        check(f"U{row} payment", r.debt_service, m.get(f"U{row}"))
        check(f"V{row} balance", r.mortgage_balance, m.get(f"V{row}"))
        if mo <= N_RETURN_MONTHS:
            check(f"X{row} appr incr", r.appr_increment, m.get(f"X{row}"))
            check(f"Y{row} term appr", r.term_appreciation, m.get(f"Y{row}"))
            check(f"Z{row} term cap", r.term_caprate, m.get(f"Z{row}"))
            check(f"AA{row} term val", r.term_value, m.get(f"AA{row}"))
            check(f"AC{row} depr", r.depreciation, m.get(f"AC{row}"))
            check(f"AD{row} taxable", r.taxable_income, m.get(f"AD{row}"))
            check(f"AE{row} tax", r.income_tax, m.get(f"AE{row}"))
            check(f"AF{row} capgain", r.capital_gain, m.get(f"AF{row}"))
            check(f"AG{row} cgtax", r.cap_gains_tax, m.get(f"AG{row}"))
            check(f"AH{row} term AT", r.term_after_tax, m.get(f"AH{row}"))
            check(f"AQ{row} CFBT", r.cfbt, m.get(f"AQ{row}"))
            check(f"AR{row} term CFBT", r.term_cfbt, m.get(f"AR{row}"))
            check_rate(f"AS{row} IRRm", r.irr_m_bt, m.get(f"AS{row}"))
            check_rate(f"AT{row} IRRa", r.irr_a_bt, m.get(f"AT{row}"))
            check_rate(f"AU{row} MIRRm", r.mirr_m_bt, m.get(f"AU{row}"))
            check_rate(f"AV{row} MIRRa", r.mirr_a_bt, m.get(f"AV{row}"))
    # XIRR block (tolerance 1e-8: day-count fractions + Newton iteration noise;
    # economically zero — ~$0.00 on any derived figure)
    check(f"AX40 cfat", rows[35].cfat, m.get("AX40"))
    check("AY40 XIRR", xirr_at_select(inp, rows), m.get("AY40"), tol=1e-8)
    check_rate("BA6 IRR", irr_ba6(inp, rows), m.get("BA6"))
    ba8 = (1 + irr_ba6(inp, rows)) ** 12 - 1 if irr_ba6(inp, rows) else None
    check_rate("BA8 IRR ann", ba8, m.get("BA8"))


# ── Rental: Model_Annual ──────────────────────────────────────────
def test_rental_annual():
    a = rental_fx["Model_Annual"]
    inp = RentalInputs()
    rows = project(inp)
    yrs = annual_rollup(inp, rows)
    col = {y: open_col(y) for y in range(0, 12)}
    for y in range(1, 12):
        c = col[y]
        d = yrs.get(y)
        if d is None:
            continue
        check(f"{c}6 rent", d["gross_rent"], a.get(f"{c}6"))
        check(f"{c}23 NOI", d["noi"], a.get(f"{c}23"))
        check(f"{c}28 DS", d["debt_service"], a.get(f"{c}28"))
        check(f"{c}30 bal", d["balance"], a.get(f"{c}30"))
        check(f"{c}55 CoC", d["cash_on_cash"], a.get(f"{c}55"), tol=1e-9)
        check(f"{c}56 NOI ret", d["noi_return"], a.get(f"{c}56"), tol=1e-9)
        check(f"{c}60 CFBT", d["cfbt"], a.get(f"{c}60"))
        check(f"{c}61 term CFBT", d["term_cfbt"], a.get(f"{c}61"))
        check_rate(f"{c}63 IRR", d.get("irr_bt"), a.get(f"{c}63"))
        check_rate(f"{c}65 MIRR", d.get("mirr_bt"), a.get(f"{c}65"))
        check(f"{c}68 CFAT", d["cfat"], a.get(f"{c}68"))
        check(f"{c}69 term CFAT", d["term_cfat"], a.get(f"{c}69"))
        check_rate(f"{c}71 IRR AT", d.get("irr_at"), a.get(f"{c}71"))
        check_rate(f"{c}73 MIRR AT", d.get("mirr_at"), a.get(f"{c}73"))


def open_col(y):
    # B=year 0, C=year 1, ... M=year 11
    return chr(ord("B") + y)


# ── Rental: Sensitivity sheets (spot + structural) ─────────────────
def test_rental_sensitivity():
    sm = rental_fx["Sensitivity_Analysis_Mthly"]
    inp = RentalInputs()
    rows = project(inp)
    base_cr = inp.cap_rate
    cr_levels = [base_cr - 0.0075, base_cr - 0.005, base_cr - 0.0025, base_cr,
                 base_cr + 0.0025, base_cr + 0.005, base_cr + 0.0075]
    cols = ["E", "F", "G", "H", "I", "J", "K"]
    res = sensitivity_cap_rate(inp, rows, cr_levels)
    for ci, cr in zip(cols, cr_levels):
        col = res[cr]
        for mi in [0, 119]:  # month 1 and month 120
            row = mi + 5
            check(f"{ci}{row} scen term CFBT", col["term_cfbt"][mi], sm.get(f"{ci}{row}"))
    # IRR columns M..S map to E..K cap scenarios
    irr_cols = ["M", "N", "O", "P", "Q", "R", "S"]
    ann_cols = ["U", "V", "W", "X", "Y", "Z", "AA"]
    for cc, ac, cr in zip(irr_cols, ann_cols, cr_levels):
        col = res[cr]
        for mi in [0, 119]:
            row = mi + 5
            check_rate(f"{cc}{row} scen IRRm", col["irr_m"][mi], sm.get(f"{cc}{row}"))
            check_rate(f"{ac}{row} scen IRRa", col["irr_a"][mi], sm.get(f"{ac}{row}"))

    base_rt = inp.interest_rate_annual
    rt_levels = [base_rt - 0.0075, base_rt - 0.005, base_rt - 0.0025, base_rt,
                 base_rt + 0.0025, base_rt + 0.005, base_rt + 0.0075]
    rcols = ["AC", "AF", "AI", "AL", "AO", "AR", "AU"]
    ircols = ["AY", "AZ", "BA", "BB", "BC", "BD", "BE"]
    arcols = ["BG", "BH", "BI", "BJ", "BK", "BL", "BM"]
    res2 = sensitivity_interest_rate(inp, rows, rt_levels)
    for rc, ic, ac, rt in zip(rcols, ircols, arcols, rt_levels):
        col = res2[rt]
        bcol = rc[0] + chr(ord(rc[1]) + 1)  # AD, AG, AJ, ...
        for mi in [0, 119]:
            row = mi + 5
            check(f"{rc}{row} rate CFBT", col["cfbt"][mi], sm.get(f"{rc}{row}"))
            check(f"{bcol}{row} rate bal", col["balance"][mi], sm.get(f"{bcol}{row}"))
            check_rate(f"{ic}{row} rate IRRm", col["irr_m"][mi], sm.get(f"{ic}{row}"))
            check_rate(f"{ac}{row} rate IRRa", col["irr_a"][mi], sm.get(f"{ac}{row}"))


# ── Analysis: full sheet parity ────────────────────────────────────
def test_analysis():
    fx = analysis_fx
    mm = AnalysisModel(AnalysisInputs())
    rows = mm.enrich()
    s = mm.sale()
    d = mm.dcf()
    ra = mm.ratios()
    rk = mm.risk()

    def g(sh, c):
        return fx[sh].get(c)

    # Pro forma year 1..6 (spot all years for NOI)
    for y in range(1, 7):
        check(f"NOI y{y}", rows[y - 1].noi, g("Operating", f"{chr(ord('C') + (y-1)*2)}27"))
    check("Expenses N31", rows[0].noi, g("Expenses", "N31"))
    check("BTCF C30", rows[0].btcf, g("BTCF", "C30"))
    check("ATCF C43", rows[0].atcf, g("ATCF", "C43"))
    # Mortgage
    check("K12 pmt", mm.mortgage_payment_monthly(), g("Mortgage", "K12"))
    for y in range(1, 7):
        col = chr(ord("D") + (y - 1))
        check(f"bal y{y}", rows[y - 1].balance, g("Mortgage", f"{col}24"))
    # Sale / DCF
    for name, got, cell in [
        ("F27 cumul depr", s["cumul_depr"], "F27"), ("K13 gain", s["gain"], "K13"),
        ("K19 tax", s["tax_total"], "K19"), ("K28 BTER", s["bter"], "K28"),
        ("K30 ATER", s["ater"], "K30"),
    ]:
        check(f"Sale {name}", got, g("Sale", cell))
    check("DCF G14 equity", d["initial_equity"], g("DCF", "G14"))
    check_rate("DCF W22 IRR BT", d["irr_before_tax"], g("DCF", "W22"))
    check_rate("DCF W30 IRR AT", d["irr_after_tax"], g("DCF", "W30"))
    # Ratios
    for name, got, cell, wb in [
        ("J10 GRM", ra["grm"], "J10", "Ratio1"), ("J13 GIM", ra["gim"], "J13", "Ratio1"),
        ("J16 NIM", ra["nim"], "J16", "Ratio1"), ("J9 op ratio", ra["operating_ratio"], "J9", "Ratio2"),
        ("J12 breakeven", ra["breakeven_ratio"], "J12", "Ratio2"), ("J15 DCR", ra["dcr"], "J15", "Ratio2"),
        ("J18 LTV", ra["ltv"], "J18", "Ratio2"), ("J23 cap", ra["cap_rate"], "J23", "Ratio2"),
        ("J29 bt div", ra["bt_equity_div"], "J29", "Ratio2"), ("J32 at div", ra["at_equity_div"], "J32", "Ratio2"),
    ]:
        check(f"{wb} {name}", got, g(wb, cell), tol=1e-9)
    # Risk
    check_rate("Risk U19 payback", rk["payback"], g("Risk", "U19"))
    check("Risk K22 NPV", rk["base_npv"], g("Risk", "K22"))
    check("Risk G85 NPV NOI+", rk["npv_noi_up"], g("Risk", "G85"))
    check_rate("Risk K28 elast wb", rk["elast_noi_wb"], g("Risk", "K28"))
    check("Risk G92 NPV sale+", rk["npv_sale_up"], g("Risk", "G92"))
    check_rate("Risk K32 elast wb", rk["elast_sale_wb"], g("Risk", "K32"))


def main():
    import time
    t0 = time.time()
    test_rental_monthly()
    print(f"rental monthly done: {PASS} pass {FAIL} fail")
    test_rental_annual()
    print(f"+ annual: {PASS} pass {FAIL} fail")
    test_rental_sensitivity()
    print(f"+ sensitivity: {PASS} pass {FAIL} fail")
    test_analysis()
    print(f"+ analysis: {PASS} pass {FAIL} fail")
    print(f"\nTOTAL: {PASS} passed, {FAIL} failed in {time.time()-t0:.1f}s")
    if FAILURES:
        print("\nWORST MISMATCHES (first 20):")
        for f in FAILURES[:20]:
            print("  " + f)
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
