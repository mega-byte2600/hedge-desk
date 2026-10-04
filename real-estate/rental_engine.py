"""
rental_engine.py — Exact Python port of Rental_Property_Investment_BOLT.xlsx.

Replicates every formula from Model_Mthly / Model_Annual /
Sensitivity_Analysis_Mthly / Sensitivity_Analysis_Annual, verified against
cached Excel values (fixtures/rental_cached.json).

Verified semantics (do not "simplify"):
- Fixed ANNUAL expenses (Property Tax, Insurance, Advertising, Other_1):
  full annual amount in the start month and each anniversary month
  (start+12k, k=0..10); 0 in all other months; 0 after 10 step-ups.
- Fixed MONTHLY expenses (Utilities, Other_2): charged EVERY month from
  start; annual step-up factor (1+rate)^k with k=min((m-start)//12, 10)
  (freezes after 10 steps — carry-forward behavior).
- % of income (Mgmt fee, Repairs): every month from start.
- Other_3: % of income ONLY in anniversary months (start+12k, k=0..10).
- Rent: month 1 = base; increase hits when m>1 and m % interval_months == 1.
- Appreciation terminal: monthly increment X compounds annually at the
  appreciation rate (steps at months 13, 25, ...); Y accumulates X net of
  sale costs.  Y_1 = (cost + X_1)*(1-sale); Y_m = Y_{m-1} + X_m*(1-sale).
- Cap-rate terminal: NEXT 12 months' NOI / cap_rate, net of sale costs
  (forward-looking; months beyond 132 contribute 0).
- Cap-gains tax may be NEGATIVE (tax benefit on a loss) — never floored.
- Model rows with terminal/returns run months 1..120 (row 124); the base
  monthly series runs 1..132 for the forward NOI window.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional

from re_math import irr as _irr, mirr as _mirr, xirr as _xirr
from re_math import pmt as _pmt, ipmt as _ipmt


_INTERVAL_MONTHS = {
    "6-Mthly": 6, "Annually": 12, "2-Yrs": 24,
    "3-Yrs": 36, "4-Yrs": 48, "5-Yrs": 60,
}

N_MODEL_MONTHS = 132   # base series (rent/NOI/debt) — Model_Mthly rows 5..136
N_RETURN_MONTHS = 120  # terminal/returns — rows 5..124


def add_months(d: date, n: int) -> date:
    """Excel EDATE."""
    m = d.month - 1 + n
    y = d.year + m // 12
    m = m % 12 + 1
    import calendar
    return date(y, m, min(d.day, calendar.monthrange(y, m)[1]))


@dataclass
class ExpenseInput:
    """One operating expense row from the Input sheet."""
    amount: float            # base amount (annual $ or monthly $ or fraction of income)
    start_month: Optional[int]  # None/blank -> expense is 0
    annual_increase: float   # e.g. 0.035
    kind: str                # 'annual_fixed' | 'monthly_fixed' | 'pct_income' | 'pct_income_anniv'


@dataclass
class RentalInputs:
    purchase_price: float = 20_000_000
    additional_capex: float = 500_000
    purchase_costs: float = 200_000
    purchase_date: date = date(2009, 12, 15)
    loan_amount: float = 9_500_000
    interest_rate_annual: float = 0.055
    amortization_months: int = 360
    monthly_rent: float = 160_000
    rent_increase_interval: str = "2-Yrs"
    rent_increase_pct: float = 0.17
    vacancy_pct: float = 0.05
    improvement_ratio: float = 0.6
    depreciation_years: int = 39
    cap_rate: float = 0.08
    appreciation_rate: float = 0.05
    cost_of_sale_pct: float = 0.04
    terminal_value_option: int = 2  # 1=appreciation, 2=cap rate
    income_tax_pct: float = 0.30
    cap_gains_tax_pct: float = 0.20
    finance_rate_monthly: float = 0.0125
    reinvestment_rate_monthly: float = 0.015
    hold_months: int = 120
    select_month: int = 36  # BA4 — XIRR evaluation month
    expenses: list = field(default_factory=lambda: [
        ExpenseInput(47000,  2, 0.035,  'annual_fixed'),    # Property Tax
        ExpenseInput(12000,  6, 0.0275, 'annual_fixed'),    # Insurance
        ExpenseInput(450,    4, 0.0325, 'monthly_fixed'),   # Utilities
        ExpenseInput(11500,  7, 0.0567, 'annual_fixed'),    # Advertising
        ExpenseInput(4500,   5, 0.04,   'annual_fixed'),     # Other_1
        ExpenseInput(550,    1, 0.025,  'monthly_fixed'),    # Other_2
        ExpenseInput(0.009,  4, 0.0,    'pct_income'),       # Mgmt fee
        ExpenseInput(0.011,  1, 0.0,    'pct_income'),       # Repairs
        ExpenseInput(0.0128, 2, 0.0,    'pct_income_anniv'), # Other_3
    ])

    @property
    def total_initial_cost(self) -> float:
        return self.purchase_price + self.additional_capex + self.purchase_costs  # C6

    @property
    def down_payment(self) -> float:  # C9
        if self.loan_amount > 0:
            return self.total_initial_cost - self.loan_amount
        return self.total_initial_cost

    @property
    def leveraged(self) -> bool:
        return self.loan_amount * self.interest_rate_annual * self.amortization_months > 0

    @property
    def improvement_value(self) -> float:  # C23
        return self.total_initial_cost * self.improvement_ratio

    @property
    def annual_depreciation(self) -> float:  # C25
        if not self.improvement_value or not self.depreciation_years:
            return 0.0
        return self.improvement_value / self.depreciation_years

    def validate(self) -> List[str]:
        errs = []
        if self.purchase_price <= 0: errs.append("Purchase Price must be > 0")
        if self.total_initial_cost <= 0: errs.append("Total Initial Cost must be > 0")
        if self.down_payment <= 0: errs.append("Down Payment must be > 0")
        if self.leveraged and self.interest_rate_annual <= 0: errs.append("Interest Rate required when leveraged")
        if self.leveraged and self.amortization_months <= 0: errs.append("Amortization required when leveraged")
        if self.monthly_rent <= 0: errs.append("Monthly Rent must be > 0")
        if self.cap_rate <= 0: errs.append("Cap Rate must be > 0")
        return errs


@dataclass
class MonthRow:
    m: int
    gross_rent: float = 0.0
    vacancy_loss: float = 0.0
    gross_income: float = 0.0
    expenses: float = 0.0
    noi: float = 0.0
    mortgage_interest: float = 0.0
    mortgage_principal: float = 0.0
    debt_service: float = 0.0
    mortgage_balance: float = 0.0
    # terminal block (months 1..120)
    appr_increment: float = 0.0      # X
    term_appreciation: float = 0.0   # Y
    term_caprate: float = 0.0        # Z
    term_value: float = 0.0          # AA
    depreciation: float = 0.0        # AC
    taxable_income: float = 0.0      # AD
    income_tax: float = 0.0           # AE
    capital_gain: float = 0.0        # AF
    cap_gains_tax: float = 0.0       # AG
    term_after_tax: float = 0.0      # AH
    cfbt: float = 0.0                # AQ
    term_cfbt: float = 0.0           # AR
    irr_m_bt: Optional[float] = None    # AS
    irr_a_bt: Optional[float] = None    # AT
    mirr_m_bt: Optional[float] = None   # AU
    mirr_a_bt: Optional[float] = None   # AV
    cfat: Optional[float] = None     # AX (None beyond select month)


def _expense_for(exp: ExpenseInput, m: int, gross_income: float) -> float:
    if exp.start_month is None or m < exp.start_month:
        return 0.0
    s = exp.start_month
    if exp.kind == 'annual_fixed':
        k, rem = divmod(m - s, 12)
        if rem == 0 and k <= 10:
            return exp.amount * (1 + exp.annual_increase) ** k
        return 0.0
    if exp.kind == 'monthly_fixed':
        k = min((m - s) // 12, 10)
        return exp.amount * (1 + exp.annual_increase) ** k
    if exp.kind == 'pct_income':
        return gross_income * exp.amount
    if exp.kind == 'pct_income_anniv':
        k, rem = divmod(m - s, 12)
        if rem == 0 and k <= 10:
            return gross_income * exp.amount
        return 0.0
    return 0.0


def project(inputs: RentalInputs) -> List[MonthRow]:
    """Full monthly projection. Base series 1..132; terminal/returns 1..120."""
    errs = inputs.validate()
    if errs:
        raise ValueError(f"Input errors: {errs}")
    interval = _INTERVAL_MONTHS.get(inputs.rent_increase_interval, 24)
    r_m = inputs.interest_rate_annual / 12.0
    nper = inputs.amortization_months
    payment = -_pmt(r_m, nper, inputs.loan_amount) if inputs.leveraged else 0.0
    monthly_depr = inputs.annual_depreciation / 12.0
    sale_net = 1.0 - inputs.cost_of_sale_pct

    rows: List[MonthRow] = []
    balance = inputs.loan_amount
    acc_depr = 0.0
    rent = inputs.monthly_rent
    x = inputs.total_initial_cost * inputs.appreciation_rate / 12.0  # X_1 seed
    y = 0.0  # Y built below

    for m in range(1, N_MODEL_MONTHS + 1):
        # Rent (C): increase when m>1 and m % interval == 1
        if m > 1 and m % interval == 1:
            rent = rent * (1 + inputs.rent_increase_pct)
        vacancy = rent * inputs.vacancy_pct                      # D
        gi = rent - vacancy                                       # E
        exp_total = sum(_expense_for(e, m, gi) for e in inputs.expenses)  # P
        noi = gi - exp_total                                      # Q

        # Debt service
        if inputs.leveraged and m <= nper:
            interest = -_ipmt(r_m, m, nper, inputs.loan_amount)   # S (positive)
            principal = payment - interest                        # T
            ds = payment                                          # U
            balance = max(balance - principal, 0.0)               # V
        else:
            interest = principal = ds = 0.0
            balance = 0.0 if inputs.leveraged else 0.0

        row = MonthRow(m=m, gross_rent=rent, vacancy_loss=vacancy,
                       gross_income=gi, expenses=exp_total, noi=noi,
                       mortgage_interest=interest, mortgage_principal=principal,
                       debt_service=ds, mortgage_balance=balance)
        rows.append(row)

    # Terminal block, months 1..120
    noi_list = [r.noi for r in rows]
    for i in range(N_RETURN_MONTHS):
        r = rows[i]
        m = r.m
        # X: annual compounding step at months 13, 25, ...
        if m > 1 and (m - 1) % 12 == 0:
            x = x * (1 + inputs.appreciation_rate)
        r.appr_increment = x
        if m == 1:
            y = (inputs.total_initial_cost + x) * sale_net        # Y5 seed
        else:
            y = y + x * sale_net
        r.term_appreciation = y
        # Z: forward 12-month NOI / cap rate
        fwd = sum(noi_list[m:m + 12])  # months m+1..m+12 (0 beyond 132)
        r.term_caprate = (fwd / inputs.cap_rate) * sale_net if inputs.cap_rate > 0 else 0.0
        r.term_value = r.term_appreciation if inputs.terminal_value_option == 1 else r.term_caprate  # AA

        r.depreciation = monthly_depr                             # AC
        acc_depr += monthly_depr
        r.taxable_income = r.noi - r.mortgage_interest - monthly_depr  # AD
        r.income_tax = r.taxable_income * inputs.income_tax_pct   # AE
        adj_basis = inputs.total_initial_cost - acc_depr
        r.capital_gain = r.term_value - adj_basis if r.term_value != 0 else 0.0  # AF
        r.cap_gains_tax = r.capital_gain * inputs.cap_gains_tax_pct  # AG (may be negative)
        r.term_after_tax = r.term_value - r.cap_gains_tax         # AH

        r.cfbt = r.noi - r.debt_service                          # AQ
        r.term_cfbt = r.cfbt + r.term_value - r.mortgage_balance  # AR

    # Growing-range IRR/MIRR (AS..AV), months 1..120
    cfbt0 = [-inputs.down_payment]
    for i in range(N_RETURN_MONTHS):
        r = rows[i]
        stream = cfbt0 + [rr.cfbt for rr in rows[:i]] + [r.term_cfbt]
        if inputs.down_payment > 0:
            r.irr_m_bt = _irr(stream)
            r.irr_a_bt = (1 + r.irr_m_bt) ** 12 - 1 if r.irr_m_bt is not None else None
            r.mirr_m_bt = _mirr(stream, inputs.finance_rate_monthly, inputs.reinvestment_rate_monthly)
            r.mirr_a_bt = (1 + r.mirr_m_bt) ** 12 - 1 if r.mirr_m_bt is not None else None

    # CFAT stream with terminal at select_month (AX), XIRR (AY), BA6/BA8
    sel = min(inputs.select_month, N_RETURN_MONTHS)
    cfat_stream: List[Optional[float]] = [-inputs.down_payment]
    for i in range(N_RETURN_MONTHS):
        r = rows[i]
        base = r.noi - r.debt_service - r.income_tax
        if r.m < sel:
            r.cfat = base
            cfat_stream.append(base)
        elif r.m == sel:
            r.cfat = base + r.term_after_tax - r.mortgage_balance
            cfat_stream.append(r.cfat)
        else:
            r.cfat = None  # Excel "" — ignored by IRR
    return rows


def xirr_at_select(inputs: RentalInputs, rows: List[MonthRow]) -> Optional[float]:
    """AY at select month: XIRR of CFAT stream with actual dates."""
    sel = min(inputs.select_month, N_RETURN_MONTHS)
    cfs, dts = [], []
    cfs.append(-inputs.down_payment); dts.append(inputs.purchase_date)
    for r in rows[:sel]:
        if r.cfat is None:
            break
        cfs.append(r.cfat); dts.append(add_months(inputs.purchase_date, r.m))
    if inputs.down_payment <= 0:
        return None
    return _xirr(cfs, dts)


def irr_ba6(inputs: RentalInputs, rows: List[MonthRow]) -> Optional[float]:
    """BA6: IRR($AX$4:$AX$124) — text cells ignored."""
    if inputs.down_payment <= 0:
        return None
    stream = [-inputs.down_payment] + [r.cfat for r in rows[:N_RETURN_MONTHS] if r.cfat is not None]
    return _irr(stream)


def annual_rollup(inputs: RentalInputs, rows: List[MonthRow]) -> dict:
    """Model_Annual: years 0..11 (year y = months (y-1)*12+1 .. y*12)."""
    years = {}
    for y in range(0, 12):
        if y == 0:
            years[y] = {"cfbt0": -inputs.down_payment}
            continue
        ms = rows[(y - 1) * 12: y * 12]
        if not ms:
            break
        s = lambda f: sum(getattr(x, f) for x in ms)
        d = {
            "gross_rent": s("gross_rent"), "vacancy": s("vacancy_loss"),
            "gross_income": s("gross_income"), "expenses": s("expenses"),
            "noi": s("noi"), "interest": s("mortgage_interest"),
            "principal": s("mortgage_principal"),
            "debt_service": s("debt_service"),
            "balance": ms[-1].mortgage_balance,
            "depreciation": s("depreciation"),
            "taxable": s("taxable_income"), "income_tax": s("income_tax"),
            "term_value": ms[-1].term_value if y <= 10 else 0.0,
            "term_after_tax": ms[-1].term_after_tax if y <= 10 else 0.0,
            "cap_gain": ms[-1].capital_gain if y <= 10 else 0.0,
        }
        d["cfbt"] = d["noi"] - d["debt_service"]                    # C60
        d["term_cfbt"] = d["cfbt"] + d["term_value"] - d["balance"]  # C61
        d["cfat"] = d["cfbt"] - d["income_tax"]                     # C68
        d["term_cfat"] = d["cfat"] + d["term_after_tax"] - d["balance"]  # C69
        # Ratios (C55/C56/C57)
        d["cash_on_cash"] = (d["noi"] - d["debt_service"]) / inputs.down_payment if inputs.down_payment > 0 else None
        d["noi_return"] = d["noi"] / inputs.total_initial_cost if inputs.total_initial_cost > 0 else None
        d["dcr"] = d["noi"] / d["debt_service"] if inputs.leveraged and d["debt_service"] > 0 else None
        years[y] = d
    # Growing-range annual IRR/MIRR (C63/C65/C71/C73)
    if inputs.down_payment > 0:
        for y in range(1, 12):
            if y not in years:
                continue
            s_bt = [-inputs.down_payment] + [years[k]["cfbt"] for k in range(1, y)] + [years[y]["term_cfbt"]]
            s_at = [-inputs.down_payment] + [years[k]["cfat"] for k in range(1, y)] + [years[y]["term_cfat"]]
            years[y]["irr_bt"] = _irr(s_bt)
            years[y]["irr_at"] = _irr(s_at)
            fr, rr = inputs.finance_rate_monthly * 12, inputs.reinvestment_rate_monthly * 12
            years[y]["mirr_bt"] = _mirr(s_bt, fr, rr)
            years[y]["mirr_at"] = _mirr(s_at, fr * (1 - inputs.income_tax_pct), rr * (1 - inputs.income_tax_pct))
    return years


def sensitivity_cap_rate(inputs: RentalInputs, rows: List[MonthRow],
                         cap_rates: List[float]) -> dict:
    """Sensitivity_Analysis_Mthly cap-rate block (monthly, months 1..120)."""
    base_noi = [r.noi for r in rows]
    base_cfbt = [r.cfbt for r in rows]
    base_bal = [r.mortgage_balance for r in rows]
    sale_net = 1.0 - inputs.cost_of_sale_pct
    out = {}
    for cr in cap_rates:
        col = {"cap_rate": cr, "term_cfbt": [], "irr_m": [], "irr_a": []}
        valid = inputs.cap_rate > 0.0075 and cr > 0
        for i in range(N_RETURN_MONTHS):
            fwd = sum(base_noi[i + 1:i + 13])
            tcfbt = base_cfbt[i] + (fwd / cr) * sale_net - base_bal[i] if valid and cr > 0 else 0.0
            col["term_cfbt"].append(tcfbt)
            stream = [-inputs.down_payment] + base_cfbt[:i] + [tcfbt]
            im = _irr(stream) if (valid and inputs.down_payment > 0) else None
            col["irr_m"].append(im)
            col["irr_a"].append((1 + im) ** 12 - 1 if im is not None else None)
        out[cr] = col
    return out


def sensitivity_interest_rate(inputs: RentalInputs, rows: List[MonthRow],
                              rates: List[float]) -> dict:
    """Sensitivity_Analysis_Mthly interest-rate block (monthly, months 1..120)."""
    base_noi = [r.noi for r in rows]
    base_term = [r.term_value for r in rows]
    nper = inputs.amortization_months
    out = {}
    for rt in rates:
        r_m = rt / 12.0
        pay = -_pmt(r_m, nper, inputs.loan_amount) if inputs.leveraged else 0.0
        col = {"rate": rt, "cfbt": [], "balance": [], "term_cfbt": [], "irr_m": [], "irr_a": []}
        bal = inputs.loan_amount
        for i in range(N_RETURN_MONTHS):
            m = i + 1
            if inputs.leveraged and m <= nper:
                interest = -_ipmt(r_m, m, nper, inputs.loan_amount)
                ds = pay
                bal = max(bal - (pay - interest), 0.0)
            else:
                interest, ds = 0.0, 0.0
                bal = 0.0
            cfbt = base_noi[i] - ds
            tcfbt = cfbt + base_term[i] - bal
            col["cfbt"].append(cfbt); col["balance"].append(bal); col["term_cfbt"].append(tcfbt)
            stream = [-inputs.down_payment] + col["cfbt"][:i] + [tcfbt]
            im = _irr(stream) if (inputs.leveraged and inputs.down_payment > 0) else None
            col["irr_m"].append(im)
            col["irr_a"].append((1 + im) ** 12 - 1 if im is not None else None)
        out[rt] = col
    return out
