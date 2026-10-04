"""Unit tests for re_math primitives (Excel-compatible financial functions)."""
import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from re_math import (
    pmt, ipmt, ppmt, npv_excel, irr, xirr, mirr,
    payback_risk_sheet, elasticity, solve_bisection,
    one_way_table, two_way_table,
)

PASS = 0
FAIL = 0


def ok(name, cond):
    global PASS, FAIL
    if cond:
        PASS += 1
    else:
        FAIL += 1
        print("FAIL:", name)


def test_pmt():
    ok("pmt magnitude", abs(abs(pmt(0.05 / 12, 360, 100000)) - 536.82) < 0.01)
    ok("pmt sign (Excel: outflow negative)", pmt(0.05 / 12, 360, 100000) < 0)
    im, pr = 0.05 / 12, 1
    ok("ipmt+ppmt==pmt",
       abs(ipmt(im, pr, 360, 100000) + ppmt(im, pr, 360, 100000)
           - pmt(0.05 / 12, 360, 100000)) < 1e-9)


def test_npv_irr():
    ok("npv", abs(npv_excel(0.1, [100, 100]) - 173.55) < 0.01)
    r = irr([-100, 110])
    ok("irr basic", r is not None and abs(r - 0.1) < 1e-9)
    ok("irr no sign change (+)", irr([100, 100]) is None)
    ok("irr no sign change (-)", irr([-100, -50]) is None)


def test_xirr():
    d0 = date(2023, 1, 1)  # non-leap year -> exactly 365 days
    xr = xirr([-1000, 1100], [d0, date(2024, 1, 1)])
    ok("xirr 1yr 10%", xr is not None and abs(xr - 0.1) < 1e-6)
    # leap-year day count: 2024-01-01 -> 2025-01-01 is 366 days
    xr2 = xirr([-1000, 1100], [date(2024, 1, 1), date(2025, 1, 1)])
    ok("xirr leap-year day count", xr2 is not None and abs(xr2 - 0.09971) < 1e-4)


def test_mirr():
    m = mirr([-1000, 300, 300, 300, 300], 0.1, 0.12)
    ok("mirr defined", m is not None)
    ok("mirr no sign change", mirr([100, 200], 0.1, 0.12) is None)


def test_payback_elasticity():
    # payback_risk_sheet replicates the workbook Risk-sheet formula
    # (ground truth = parity test vs cached U19)
    pb = payback_risk_sheet([-100, 40, 40, 40], [1, 2, 3, 4])
    ok("payback defined", pb is not None)
    ok("elasticity", abs(elasticity(100, 110, 0.05) - 2.0) < 1e-9)


def test_solve_and_tables():
    s = solve_bisection(lambda r: npv_excel(r, [-100, 110]), 0.0, 0.5, 0.0)
    ok("solve_bisection", s is not None and abs(s - 0.1) < 1e-6)
    t1 = one_way_table({"x": 0}, lambda d, lv: d.update(x=lv), [1, 2, 3],
                       lambda d: {"y": d["x"] * 2}, lambda o: o["y"])
    ok("one_way_table", t1 == [(1, 2), (2, 4), (3, 6)])
    t2 = two_way_table({"x": 0, "y": 0},
                       lambda d, lv: d.update(x=lv), [1, 2],
                       lambda d, lv: d.update(y=lv), [10, 20],
                       lambda d: {"z": d["x"] + d["y"]}, lambda o: o["z"])
    ok("two_way_table", t2 == [[11, 21], [12, 22]])


def main():
    test_pmt()
    test_npv_irr()
    test_xirr()
    test_mirr()
    test_payback_elasticity()
    test_solve_and_tables()
    print(f"re_math unit tests: {PASS} passed, {FAIL} failed")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
