"""
re_math.py — Financial primitives with Excel-compatible semantics.

All functions replicate Excel behavior (float64 arithmetic) so engine outputs
can be asserted against cached workbook values:
- PMT/IPMT/PPMT/PV: Excel sign conventions (outflows negative).
- NPV: Excel semantics — first value discounted one full period.
- IRR: Newton-Raphson with bisection fallback (mirrors Excel's iterative solver).
- XIRR: actual/365 day count, Newton + bisection.
- MIRR: Excel semantics (finance rate discounts negatives, reinvest rate
  compounds positives).
- payback_risk_sheet: exact replication of the Risk-sheet fractional payback.
"""
from __future__ import annotations

import math
from datetime import date
from typing import Callable, List, Optional, Sequence, Tuple


# ── Time value ──────────────────────────────────────────────────────

def pmt(rate: float, nper: int, pv: float, fv: float = 0.0, when: int = 0) -> float:
    """Excel PMT. Returns negative when pv > 0 (cash outflow)."""
    if rate == 0:
        return -(pv + fv) / nper
    return -(pv * (1 + rate) ** nper + fv) * rate / ((1 + rate) ** nper - 1) / (1 + rate * when)


def ipmt(rate: float, per: int, nper: int, pv: float, fv: float = 0.0, when: int = 0) -> float:
    """Excel IPMT — interest portion of payment `per` (1-indexed)."""
    if per < 1 or per > nper:
        raise ValueError("per out of range")
    payment = pmt(rate, nper, pv, fv, when)
    if when == 1 and per == 1:
        return 0.0
    # Balance before payment `per`
    bal = pv * (1 + rate) ** (per - 1) + payment * (((1 + rate) ** (per - 1) - 1) / rate) * (1 + rate * when)
    return -bal * rate


def ppmt(rate: float, per: int, nper: int, pv: float, fv: float = 0.0, when: int = 0) -> float:
    """Excel PPMT — principal portion of payment `per` (1-indexed)."""
    return pmt(rate, nper, pv, fv, when) - ipmt(rate, per, nper, pv, fv, when)


def pv(rate: float, nper: int, pmt_: float, fv: float = 0.0, when: int = 0) -> float:
    """Excel PV."""
    if rate == 0:
        return -(pmt_ * nper + fv)
    return -(pmt_ * (1 + rate * when) * ((1 + rate) ** nper - 1) / rate + fv) / (1 + rate) ** nper


def npv_excel(rate: float, values: Sequence[float]) -> float:
    """Excel NPV: values[0] is discounted one full period (t=1)."""
    return sum(v / (1 + rate) ** (i + 1) for i, v in enumerate(values))


# ── Rate of return ──────────────────────────────────────────────────

def _npv_at(rate: float, cf: Sequence[float]) -> float:
    import math
    base = 1.0 + rate
    if base <= 1e-300:
        # Limit as rate -> -1+: dominated by the last cash flow's sign.
        last = next((c for c in reversed(cf) if c != 0), 0.0)
        return math.copysign(math.inf, last) if last != 0 else math.inf
    total = 0.0
    try:
        for i, c in enumerate(cf):
            if c:
                total += c / base ** i
    except (OverflowError, ZeroDivisionError):
        return math.copysign(math.inf, total) if total != 0 else math.inf
    return total


def irr(values: Sequence[float], guess: float = 0.1) -> Optional[float]:
    """Excel-compatible IRR: Newton-Raphson, bisection fallback. None if no root."""
    cf = [float(v) for v in values]
    if not any(v > 0 for v in cf) or not any(v < 0 for v in cf):
        return None

    # Newton-Raphson
    rate = guess
    for _ in range(100):
        if rate <= -0.9999999:
            rate = -0.9999999
        try:
            f = _npv_at(rate, cf)
            df = sum(-i * c / (1 + rate) ** (i + 1) for i, c in enumerate(cf) if c)
        except (OverflowError, ZeroDivisionError):
            break
        if not math.isfinite(f) or not math.isfinite(df) or abs(df) < 1e-14:
            break
        step = f / df
        rate -= step
        if rate <= -1:
            rate = -0.9999999
        if abs(step) < 1e-12:
            return rate
    else:
        pass

    # Bisection fallback on a wide bracket
    lo, hi = -0.9999999, 1e10
    f_lo, f_hi = _npv_at(lo, cf), _npv_at(hi, cf)
    if f_lo * f_hi > 0:
        # Try to find a bracket by scanning
        return _irr_scan(cf)
    for _ in range(500):
        mid = (lo + hi) / 2
        f_mid = _npv_at(mid, cf)
        if abs(f_mid) < 1e-9:
            return mid
        if f_lo * f_mid <= 0:
            hi, f_hi = mid, f_mid
        else:
            lo, f_lo = mid, f_mid
    return (lo + hi) / 2


def _irr_scan(cf: Sequence[float]) -> Optional[float]:
    """Scan for a sign change when the wide bracket fails."""
    prev_r, prev_f = -0.9999999, _npv_at(-0.9999999, cf)
    r = -0.9
    while r < 1e6:
        f = _npv_at(r, cf)
        if prev_f * f < 0:
            lo, hi = (prev_r, r) if prev_r < r else (r, prev_r)
            f_lo = _npv_at(lo, cf)
            for _ in range(300):
                mid = (lo + hi) / 2
                f_mid = _npv_at(mid, cf)
                if abs(f_mid) < 1e-9:
                    return mid
                if f_lo * f_mid <= 0:
                    hi = mid
                else:
                    lo, f_lo = mid, f_mid
            return (lo + hi) / 2
        prev_r, prev_f = r, f
        r = r * 1.5 + 0.1 if r < 10 else r * 2
    return None


def xirr(cashflows: Sequence[float], dates: Sequence[date], guess: float = 0.1) -> Optional[float]:
    """Excel XIRR: actual/365 day count. cashflows[i] pairs with dates[i]."""
    if len(cashflows) != len(dates) or not cashflows:
        return None
    cf = [float(v) for v in cashflows]
    if not any(v > 0 for v in cf) or not any(v < 0 for v in cf):
        return None
    d0 = dates[0]
    t = [(d - d0).days / 365.0 for d in dates]

    def f(r: float) -> float:
        return sum(c / (1 + r) ** ti for c, ti in zip(cf, t))

    def df(r: float) -> float:
        return sum(-ti * c / (1 + r) ** (ti + 1) for c, ti in zip(cf, t))

    rate = guess
    for _ in range(100):
        fv, dv = f(rate), df(rate)
        if abs(dv) < 1e-14:
            break
        step = fv / dv
        rate -= step
        if rate <= -1:
            rate = -0.9999999
        if abs(step) < 1e-12:
            return rate

    lo, hi = -0.9999999, 1e10
    f_lo, f_hi = f(lo), f(hi)
    if f_lo * f_hi > 0:
        return None
    for _ in range(500):
        mid = (lo + hi) / 2
        f_mid = f(mid)
        if abs(f_mid) < 1e-9:
            return mid
        if f_lo * f_mid <= 0:
            hi, f_hi = mid, f_mid
        else:
            lo, f_lo = mid, f_mid
    return (lo + hi) / 2


def mirr(values: Sequence[float], finance_rate: float, reinvest_rate: float) -> Optional[float]:
    """Excel MIRR. Returns None when undefined (no sign change)."""
    cf = [float(v) for v in values]
    n = len(cf) - 1
    if n <= 0:
        return None
    neg = sum(v / (1 + finance_rate) ** i for i, v in enumerate(cf) if v < 0)
    pos = sum(v * (1 + reinvest_rate) ** (n - i) for i, v in enumerate(cf) if v > 0)
    if neg == 0 or pos == 0:
        return None
    return (pos / -neg) ** (1 / n) - 1


# ── Payback / elasticity / sensitivity / inverse solving ────────────

def payback_risk_sheet(year_flows: Sequence[float], year_numbers: Sequence[float]) -> Optional[float]:
    """
    Exact replication of the Risk-sheet fractional payback:
      E18 = IF(E17>0, 0, IF(G17=0, 0, E13+E16/G17))
    i.e. for each year n with cumulative_n <= 0 and cumulative_{n+1} != 0:
      frac_n = year_n + flow_n / cumulative_{n+1}
    Payback = MAX over years (None if never positive).
    year_flows[0] is time-0 (negative equity); year_numbers[0] = 0.
    """
    cumul: List[float] = []
    run = 0.0
    for v in year_flows:
        run += v
        cumul.append(run)
    fracs: List[float] = []
    for n in range(len(year_flows) - 1):
        if cumul[n] > 0:
            fracs.append(0.0)
        elif cumul[n + 1] == 0:
            fracs.append(0.0)
        else:
            fracs.append(year_numbers[n] + year_flows[n] / cumul[n + 1])
    if not any(c > 0 for c in cumul):
        return None
    return max(fracs) if fracs else None


def elasticity(base_value: float, varied_value: float, input_change: float) -> Optional[float]:
    """% change in output per unit input change: (V1-V0)/V0 / input_change."""
    if base_value == 0 or input_change == 0:
        return None
    return ((varied_value - base_value) / base_value) / input_change


def one_way_table(
    base_inputs,
    vary: Callable,
    levels: Sequence[float],
    run: Callable,
    metric: Callable,
) -> List[Tuple[float, Optional[float]]]:
    """One-way sensitivity: for each level, apply vary(inputs, level), run, extract metric."""
    import copy
    rows = []
    for lv in levels:
        inp = copy.deepcopy(base_inputs)
        vary(inp, lv)
        try:
            out = run(inp)
            rows.append((lv, metric(out)))
        except Exception:
            rows.append((lv, None))
    return rows


def two_way_table(
    base_inputs,
    vary_row: Callable,
    row_levels: Sequence[float],
    vary_col: Callable,
    col_levels: Sequence[float],
    run: Callable,
    metric: Callable,
) -> List[List[Optional[float]]]:
    """Two-way sensitivity grid."""
    import copy
    grid = []
    for rl in row_levels:
        row = []
        for cl in col_levels:
            inp = copy.deepcopy(base_inputs)
            vary_row(inp, rl)
            vary_col(inp, cl)
            try:
                row.append(metric(run(inp)))
            except Exception:
                row.append(None)
        grid.append(row)
    return grid


def solve_bisection(
    f: Callable[[float], float],
    lo: float,
    hi: float,
    target: float = 0.0,
    tol: float = 1e-9,
    max_iter: int = 200,
) -> Optional[float]:
    """Find x in [lo, hi] with f(x) = target. None if no sign change."""
    f_lo, f_hi = f(lo) - target, f(hi) - target
    if f_lo * f_hi > 0:
        return None
    for _ in range(max_iter):
        mid = (lo + hi) / 2
        f_mid = f(mid) - target
        if abs(f_mid) < tol or (hi - lo) < tol:
            return mid
        if f_lo * f_mid <= 0:
            hi, f_hi = mid, f_mid
        else:
            lo, f_lo = mid, f_mid
    return (lo + hi) / 2
