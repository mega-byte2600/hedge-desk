"""
analysis_engine.py — Exact Python port of Real_Estate_Investment_Analysis_BOLT.xlsx.

Sheets: INTRO, Expenses, Operating, Mortgage, BTCF, ATCF, Sale, Ratio1,
Ratio2, DCF, Risk.

Conventions replicated:
- Money rounded to nearest $100 via ROUND(x/1000,1)*1000 (Excel ROUND =
  half away from zero) at the same cells as the workbook.
- Year columns: years 1..10; all formulas guarded by holding period
  (years beyond hold → 0).
- Mortgage: PMT for payment; year-end balance = PV of remaining payments.
- Depreciation: 27.5-yr straight line with IRS mid-month convention
  (11.5 months in first and sale years).

Bug fixes vs the workbook (flagged, never silent):
- ATCF!Q30:Q35 / Risk!S59:S64 `>77` typo → corrected to `>7`
  (latent at default 6-yr hold; visible at 8+ yr holds).
- Risk NOI sensitivity: workbook leaks the varied sale price into the NOI
  elasticity via V46. Fixed: NOI sensitivity uses the BASE after-tax
  reversion. Set compat_excel_bugs=True to replicate the contamination.
- Risk!V41 hardcoded 5% selling cost → parameterized from Sale inputs
  (selling_cost / selling_price ratio). Identical at defaults.

Dead sections stay dead: DCF has no NPV (lives on Risk); Ratio1 inputs
H22/H25/H28 and Ratio2 H26 are user inputs.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal, ROUND_HALF_UP
from typing import List, Optional

from re_math import irr as _irr, npv_excel as _npv, pmt as _pmt, pv as _pv
from re_math import payback_risk_sheet as _payback, elasticity as _elasticity


def _round1(x: float) -> float:
    """Excel ROUND(x,1) — half away from zero."""
    return float(Decimal(str(x)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def r100(x: float) -> float:
    """Workbook money rounding: ROUND(x/1000,1)*1000 (nearest $100)."""
    return _round1(x / 1000.0) * 1000.0


@dataclass
class AnalysisInputs:
    # INTRO
    holding_years: int = 6
    units: List[float] = field(default_factory=lambda: [50.0, 150.0, 80.0])
    monthly_rents: List[float] = field(default_factory=lambda: [858.0, 704.0, 528.0])
    nonres_sqft: float = 0.0
    nonres_rent_sf: float = 0.0
    rent_growth: List[float] = field(default_factory=lambda: [0.025, 0.05, 0.05, 0.035, 0.035, 0.035, 0.0, 0.0, 0.0, 0.0])
    vacancy_rates: List[float] = field(default_factory=lambda: [0.075, 0.04, 0.04, 0.06, 0.06, 0.06, 0.0, 0.0, 0.0, 0.0])
    other_income_pct: float = 0.047
    # Expenses
    opex_increase: float = 0.035
    mgmt_fee_pct: float = 0.05
    base_expenses: List[float] = field(default_factory=lambda: [197100.0, 105300.0, 35500.0, 21000.0, 32000.0, 181900.0])
    base_property_tax: float = 300000.0
    tax_schedule: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    # Mortgage
    mortgage_amount: float = 8_000_000
    mortgage_term_years: int = 20
    mortgage_rate: float = 0.08
    mortgage_amort_per_year: int = 12
    # ATCF
    marginal_tax_rate: float = 0.40
    depreciable_basis: float = 9_300_000
    recovery_years: float = 27.5
    # Sale
    purchase_price: float = 11_444_500
    transaction_costs: float = 150_000
    selling_price: float = 17_800_000
    selling_costs: float = 890_000
    cap_gains_tax_rate: float = 0.20
    recapture_tax_rate: float = 0.25
    # Ratio1 inputs
    grm_input: float = 5.0
    gim_input: float = 5.0
    nim_input: float = 9.0
    # Ratio2 input
    cap_rate_input: float = 0.10
    # Risk inputs
    discount_rate: float = 0.10
    noi_variation: float = 0.10
    sale_variation: float = 0.10


@dataclass
class YearRow:
    y: int
    pgr: float = 0.0
    vacancy: float = 0.0
    collectable: float = 0.0
    other_income: float = 0.0
    egi: float = 0.0
    mgmt_fee: float = 0.0
    expenses6: List[float] = field(default_factory=list)
    property_tax: float = 0.0
    total_expenses: float = 0.0
    noi: float = 0.0
    debt_service: float = 0.0
    interest: float = 0.0
    principal: float = 0.0
    balance: float = 0.0
    depreciation: float = 0.0
    taxable_income: float = 0.0
    income_tax: float = 0.0
    btcf: float = 0.0
    atcf: float = 0.0


class AnalysisModel:
    def __init__(self, inputs: AnalysisInputs):
        self.i = inputs
        self._proforma: Optional[List[YearRow]] = None

    # ── Pro forma (single implementation; workbook quadruplicates it) ──
    def proforma(self) -> List[YearRow]:
        if self._proforma is not None:
            return self._proforma
        i = self.i
        base_rent = (i.nonres_sqft * i.nonres_rent_sf
                     + sum(u * r * 12 for u, r in zip(i.units, i.monthly_rents)))
        base_pgr = r100(base_rent)  # INTRO!O13
        rows: List[YearRow] = []
        prev_pgr, prev_exp6, prev_tax = 0.0, [0.0] * 6, 0.0
        for y in range(1, 11):
            r = YearRow(y=y)
            if y <= i.holding_years:
                g = i.rent_growth[y - 1] if y - 1 < len(i.rent_growth) else 0.0
                r.pgr = r100(base_pgr * (1 + g)) if y == 1 else r100(prev_pgr * (1 + g))
                v = i.vacancy_rates[y - 1] if y - 1 < len(i.vacancy_rates) else 0.0
                r.vacancy = r100(r.pgr * v)
                r.collectable = r.pgr - r.vacancy
                r.other_income = r100(r.collectable * i.other_income_pct)
                r.egi = r.collectable + r.other_income
                r.mgmt_fee = r100(r.egi * i.mgmt_fee_pct)
                if y == 1:
                    r.expenses6 = [r100(b * (1 + i.opex_increase)) for b in i.base_expenses]
                    r.property_tax = r100(i.base_property_tax * (1 + (i.tax_schedule[0] if i.tax_schedule else 0.0)))
                else:
                    r.expenses6 = [r100(p * (1 + i.opex_increase)) for p in prev_exp6]
                    ts = i.tax_schedule[y - 1] if y - 1 < len(i.tax_schedule) else 0.0
                    r.property_tax = r100(prev_tax * (1 + ts))
                r.total_expenses = r.mgmt_fee + sum(r.expenses6) + r.property_tax
                r.noi = r.egi - r.total_expenses
                prev_pgr, prev_exp6, prev_tax = r.pgr, list(r.expenses6), r.property_tax
            rows.append(r)
        self._proforma = rows
        return rows

    # ── Mortgage ──
    def mortgage_payment_monthly(self) -> float:
        i = self.i
        return _pmt(i.mortgage_rate / i.mortgage_amort_per_year,
                    i.mortgage_term_years * i.mortgage_amort_per_year,
                    -i.mortgage_amount)

    def mortgage_annual_ds(self) -> float:
        return self.mortgage_payment_monthly() * self.i.mortgage_amort_per_year  # K13

    def mortgage_balance(self, year: int) -> float:
        """Year-end balance = PV of remaining payments (Mortgage!D24:M24)."""
        i = self.i
        n = i.mortgage_term_years * i.mortgage_amort_per_year
        r = i.mortgage_rate / i.mortgage_amort_per_year
        pmt = self.mortgage_payment_monthly()
        remaining = n - year * i.mortgage_amort_per_year
        if remaining <= 0:
            return 0.0
        return _pv(r, remaining, -pmt)

    def mortgage_schedule(self) -> List[dict]:
        i = self.i
        ads_r = r100(self.mortgage_annual_ds())  # L15 rounded
        out = []
        prev_bal = i.mortgage_amount
        for y in range(1, 11):
            if y <= i.holding_years:
                bal = self.mortgage_balance(y)
                principal = prev_bal - bal
                interest = self.mortgage_annual_ds() - principal
                ds = self.mortgage_annual_ds()
            else:
                bal = principal = interest = ds = 0.0
            out.append({"ds": ds, "ds_rounded": ads_r if y <= i.holding_years else 0.0,
                        "principal": principal, "interest": interest, "balance": bal})
            prev_bal = bal
        return out

    # ── Operating / BTCF / ATCF ──
    def enrich(self) -> List[YearRow]:
        """Attach debt, tax, BTCF, ATCF to each pro-forma year."""
        i = self.i
        rows = self.proforma()
        sched = self.mortgage_schedule()
        depr_full = r100(i.depreciable_basis / i.recovery_years)      # N9
        depr_mid = r100(depr_full * 11.5 / 12.0)                       # R9
        for r, s in zip(rows, sched):
            if r.y <= i.holding_years:
                r.debt_service = s["ds_rounded"]                       # BTCF!C28
                r.interest = r100(s["interest"])
                r.principal = s["principal"]
                r.balance = s["balance"]
                r.btcf = r.noi - r.debt_service
                if r.y == 1 or r.y == i.holding_years:
                    r.depreciation = depr_mid
                else:
                    r.depreciation = depr_full
                r.taxable_income = r.noi - r.interest - r.depreciation
                r.income_tax = r100(r.taxable_income * i.marginal_tax_rate)
                r.atcf = r.btcf - r.income_tax
        return rows

    # ── Sale ──
    def sale(self) -> dict:
        i = self.i
        rows = self.enrich()
        basis_initial = i.purchase_price + i.transaction_costs          # F26
        cumul_depr = sum(r.depreciation for r in rows)                  # F27
        adj_basis = basis_initial - cumul_depr                          # F28
        adj_basis_sale = adj_basis + i.selling_costs                    # F30
        gain = i.selling_price - adj_basis_sale                         # K13
        recapture = min(cumul_depr, gain) if gain > 0 else 0.0          # K14
        lt_gain = gain - recapture                                      # K15
        tax_recapture = r100(recapture * i.recapture_tax_rate)          # K17
        tax_gain = r100(lt_gain * i.cap_gains_tax_rate)                 # K18
        tax_total = tax_recapture + tax_gain                            # K19
        net_proceeds = i.selling_price - i.selling_costs                # K26
        bal = self.mortgage_balance(i.holding_years)                    # F18
        bal_r = r100(bal)                                               # K27
        bter = net_proceeds - bal_r                                     # K28
        ater = bter - tax_total                                         # K30
        return {"basis_initial": basis_initial, "cumul_depr": cumul_depr,
                "adj_basis": adj_basis, "adj_basis_sale": adj_basis_sale,
                "gain": gain, "recapture": recapture, "lt_gain": lt_gain,
                "tax_recapture": tax_recapture, "tax_gain": tax_gain,
                "tax_total": tax_total, "net_proceeds": net_proceeds,
                "mortgage_balance": bal, "bter": bter, "ater": ater}

    def initial_equity(self) -> float:  # DCF!G14
        i = self.i
        return (i.purchase_price + i.transaction_costs) - i.mortgage_amount

    # ── DCF ──
    def dcf(self) -> dict:
        i = self.i
        rows = self.enrich()
        s = self.sale()
        eq = self.initial_equity()
        bt_stream = [-eq]
        at_stream = [-eq]
        for r in rows:
            bt_stream.append(r.btcf + (s["bter"] if r.y == i.holding_years else 0.0))
            at_stream.append(r.atcf + (s["ater"] if r.y == i.holding_years else 0.0))
        return {"initial_equity": eq,
                "bt_stream": bt_stream, "at_stream": at_stream,
                "irr_before_tax": _irr(bt_stream),
                "irr_after_tax": _irr(at_stream)}

    # ── Ratios ──
    def ratios(self) -> dict:
        i = self.i
        rows = self.enrich()
        y1 = rows[0]
        ads_r = r100(self.mortgage_annual_ds())
        return {
            "grm": i.purchase_price / y1.pgr if y1.pgr else None,                    # J10
            "gim": i.purchase_price / y1.egi if y1.egi else None,                    # J13
            "nim": i.purchase_price / y1.noi if y1.noi else None,                    # J16
            "grm_value": y1.pgr * i.grm_input,                                       # J22
            "gim_value": y1.egi * i.gim_input,                                       # J25
            "nim_value": y1.noi * i.nim_input,                                       # J28
            "operating_ratio": y1.total_expenses / y1.egi if y1.egi else None,       # J9
            "breakeven_ratio": (y1.total_expenses + ads_r) / y1.egi if y1.egi else None,  # J12
            "dcr": y1.noi / ads_r if ads_r else None,                                # J15
            "ltv": i.mortgage_amount / i.purchase_price if i.purchase_price else None,  # J18
            "cap_rate": y1.noi / i.purchase_price if i.purchase_price else None,    # J23
            "cap_value": y1.noi / i.cap_rate_input if i.cap_rate_input else None,    # J26
            "bt_equity_div": y1.btcf / self.initial_equity(),                        # J29
            "at_equity_div": y1.atcf / self.initial_equity(),                        # J32
        }

    # ── Risk ──
    def risk(self, compat_excel_bugs: bool = False) -> dict:
        i = self.i
        rows = self.enrich()
        s = self.sale()
        eq = self.initial_equity()
        hold = i.holding_years

        # Payback block (ATCF + ATER at hold year)
        year_flows = [-eq]
        for r in rows:
            year_flows.append(r.atcf + (s["ater"] if r.y == hold else 0.0))
        payback = _payback(year_flows, list(range(0, 11)))

        # Base NPV (Excel NPV: time-0 excluded)
        base_npv = _npv(i.discount_rate, year_flows[1:])

        # NOI sensitivity — workbook uses BASE after-tax reversion here
        # (O82 = $V$10 at default hold=6; the $V$46 refs in other columns are
        # dead unless hold != 6, in which case they leak the varied sale
        # price in — the contamination this fix removes).
        var = i.noi_variation
        varied_flows = [-eq]
        for r in rows:
            if r.y <= hold:
                noi_v = r.noi * (1 + var)
                btcf_v = noi_v - r.debt_service
                tax_v = r100((noi_v - r.interest - r.depreciation) * i.marginal_tax_rate)
                atcf_v = btcf_v - tax_v
            else:
                atcf_v = 0.0
            ater_v = s["ater"]  # FIXED: base reversion, always
            if compat_excel_bugs and hold != 6:
                ater_v = self._compat_varied_ater()  # V46 leak (hold!=6 only)
            varied_flows.append(atcf_v + (ater_v if r.y == hold else 0.0))
        npv_noi_up = _npv(i.discount_rate, varied_flows[1:])
        d_noi = npv_noi_up - base_npv
        # Workbook "elasticity" (K28) = fractional change in equity value for
        # the stated variation (NOT normalized by the variation itself).
        elast_noi_wb = d_noi / base_npv if base_npv else None
        elast_noi = _elasticity(base_npv, npv_noi_up, var)  # true normalized

        # Sale-price sensitivity — workbook keeps BASE taxes (V45=$V$9);
        # only price and selling costs vary.
        sv = i.sale_variation
        sp_v = i.selling_price * (1 + sv)
        sc_ratio = i.selling_costs / i.selling_price if i.selling_price else 0.05
        sc_v = sp_v * sc_ratio  # FIXED: parameterized (workbook hardcodes 5%)
        if compat_excel_bugs:
            sc_v = sp_v * 0.05
        ater_v2 = (sp_v - sc_v) - r100(s["mortgage_balance"]) - s["tax_total"]
        sale_flows = [-eq]
        for r in rows:
            sale_flows.append(r.atcf + (ater_v2 if r.y == hold else 0.0))
        npv_sale_up = _npv(i.discount_rate, sale_flows[1:])
        d_sale = npv_sale_up - base_npv
        elast_sale_wb = d_sale / base_npv if base_npv else None
        elast_sale = _elasticity(base_npv, npv_sale_up, sv)

        return {"payback": payback, "base_npv": base_npv,
                "npv_noi_up": npv_noi_up, "d_noi": d_noi,
                "elast_noi_wb": elast_noi_wb, "elast_noi": elast_noi,
                "downside_noi": base_npv - d_noi, "upside_noi": base_npv + d_noi,
                "npv_sale_up": npv_sale_up, "d_sale": d_sale,
                "elast_sale_wb": elast_sale_wb, "elast_sale": elast_sale,
                "downside_sale": base_npv - d_sale, "upside_sale": base_npv + d_sale}

    def _compat_varied_ater(self) -> float:
        """Replicate the workbook's contaminated V46 (for parity only)."""
        i = self.i
        sv = i.sale_variation
        sp_v = i.selling_price * (1 + sv)
        sc_v = sp_v * 0.05
        net_v = sp_v - sc_v
        bter_v = net_v - r100(self.sale()["mortgage_balance"])
        s = self.sale()
        gain_v = sp_v - s["adj_basis_sale"]
        recapture_v = min(s["cumul_depr"], gain_v) if gain_v > 0 else 0.0
        lt_v = gain_v - recapture_v
        tax_v = r100(recapture_v * i.recapture_tax_rate) + r100(lt_v * i.cap_gains_tax_rate)
        return bter_v - tax_v

    # ── Inverse solving: max purchase price at target IRR ──
    def solve_price_for_irr(self, target_irr: float, after_tax: bool = True,
                            lo: float = 1.0, hi: float = 100_000_000) -> Optional[float]:
        """Bisection: purchase price giving target IRR (all else equal)."""
        from re_math import solve_bisection
        import copy

        def irr_at_price(p: float) -> float:
            inp = copy.deepcopy(self.i)
            inp.purchase_price = p
            m = AnalysisModel(inp)
            d = m.dcf()
            v = d["irr_after_tax"] if after_tax else d["irr_before_tax"]
            return v if v is not None else float("nan")

        return solve_bisection(irr_at_price, lo, hi, target_irr)
