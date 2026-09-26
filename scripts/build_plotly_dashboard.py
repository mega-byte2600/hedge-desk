"""Build the Emporion interactive Plotly dashboard from the REAL overnight report.

Reads artifacts/am-report-latest.json (real Yahoo/Cboe/FRED/EDGAR data) and emits
a self-contained HTML with Plotly interactive charts. plotly.js is loaded once
from CDN in the <head>. No synthetic data, no fabricated numbers. BLOCKED or
missing sections render as honest state panels, never as invented values.
"""
import html
import json
from pathlib import Path

import plotly.graph_objects as go

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts" / "am-report-latest.json"
OUT = ROOT / "artifacts" / "am-demo.html"

PLOTLY_JS = "https://cdn.plot.ly/plotly-2.35.2.min.js"

BG = "#0f1828"
FG = "#e8eef7"
MUTED = "#93a5c4"


def esc(value) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def base_layout(title: str, height: int = 340) -> dict:
    return dict(
        margin=dict(l=10, r=10, t=44, b=10),
        height=height,
        title=dict(text=title, font=dict(size=14)),
        font=dict(color=FG),
        paper_bgcolor=BG,
        plot_bgcolor=BG,
    )


def chart(fig: go.Figure, div_id: str) -> str:
    return fig.to_html(full_html=False, include_plotlyjs=False, div_id=div_id)


def muted(msg: str) -> str:
    return f"<p class='muted'>{esc(msg)}</p>"


def _fnum(value, default=0.0) -> float:
    """float() that returns *default* instead of raising on junk input."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _xy(pts):
    """Parse [[x, y-ish], ...] into (xs, ys), skipping points with junk y."""
    xs, ys = [], []
    for p in pts or []:
        try:
            y = float(p[1])
        except (TypeError, ValueError, IndexError):
            continue
        xs.append(p[0])
        ys.append(y)
    return xs, ys


# ---------------------------------------------------------------- freshness

def freshness_strip(r: dict) -> str:
    f = r.get("data_freshness", {}) or {}
    return (
        f"<p class='ts'>REAL overnight report &middot; generated {esc(r.get('generated_at'))} &middot; "
        f"{esc(r.get('candidate_count'))} candidates &middot; {esc(r.get('mode'))} &middot; "
        f"eod {esc(r.get('eod_batch_status'))} &middot; "
        f"trading day {esc(f.get('expected_trading_day'))} "
        f"({'current' if f.get('is_current') else 'STALE'}) &middot; "
        f"paper-only &middot; every candidate trade_authorized=False</p>"
    )


def source_health(r: dict) -> str:
    """Per-source status table: what the batch actually closed on."""
    rows = []
    rows.append(("EOD batch (Yahoo)", str(r.get("eod_batch_status", "?")),
                 str((r.get("data_freshness", {}) or {}).get("note", ""))))
    for sym, ch in (r.get("chain_income", {}) or {}).items():
        mode = ch.get("mode", "?")
        detail = ch.get("reason", "") if mode == "BLOCKED" else f"{len(ch.get('gated_income_structures', []) or [])} gated structures"
        rows.append((f"Premium chain (Cboe {sym})", mode, detail))
    for label, key in (("Rates (FRED)", "rates_environment"), ("VIX regime (Yahoo)", "vix_regime"),
                       ("Macro (FRED)", "macro_environment"), ("Oil WTI (Yahoo)", "oil_market")):
        d = r.get(key, {}) or {}
        rows.append((label, str(d.get("mode", "?")), str(d.get("reason", d.get("note", "")))))
    csp = r.get("cash_secured_put_scan", {}) or {}
    real_csp = sum(1 for v in csp.values() if isinstance(v, dict) and v.get("mode") == "CASH_SECURED_PUT")
    rows.append(("CSP scan (Cboe)", f"{real_csp}/{len(csp)} real", ""))
    ea = r.get("earnings_actuals", {}) or {}
    real_ea = sum(1 for v in ea.values() if isinstance(v, dict) and v.get("mode") == "REAL_EDGAR_EARNINGS")
    rows.append(("Earnings (SEC EDGAR)", f"{real_ea}/{len(ea)} real", ""))
    trs = "".join(
        f"<tr><td>{esc(a)}</td><td class='{'ok' if 'REAL' in b or 'PASS' in b else 'warn'}'>{esc(b)}</td>"
        f"<td class='muted'>{esc(c)}</td></tr>"
        for a, b, c in rows
    )
    return (f"<table class='health'><thead><tr><th>source</th><th>status</th><th>detail</th></tr></thead>"
            f"<tbody>{trs}</tbody></table>")


# ---------------------------------------------------------------- macro

def macro_panel(vix: dict, rates: dict, oil: dict, macro: dict) -> str:
    cells = []  # (label, value, source)
    vix = vix or {}
    rates = rates or {}
    oil = oil or {}
    macro = macro or {}
    if vix.get("mode") == "REAL_VIX" and vix.get("last_close") is not None:
        try:
            cells.append((f"VIX ({vix.get('regime', '?')})", f"{float(vix['last_close']):.1f}", "Yahoo"))
        except (TypeError, ValueError):
            pass


def premium_yield_chart(csp: dict) -> str:
    """Options premium economics: return-on-capital vs premium-yield (net_credit/strike).

    Real Cboe data from the CSP scan. Two metrics per PREMIUM_WHEEL_ECONOMICS.md:
    return_on_capital = net_credit/collateral (small, on full capital deployed);
    premium_yield = net_credit/strike (what 'sell premium' intuitively means).
    """
    rows = []
    for s, v in (csp or {}).items():
        if not isinstance(v, dict) or v.get("mode") != "CASH_SECURED_PUT":
            continue
        c = v.get("candidate")
        if not isinstance(c, dict):
            continue
        try:
            roc_v = float(c["return_on_capital"])
            credit = float(c["net_credit_per_share"])
            strike = float(c["strike"])
        except (TypeError, ValueError, KeyError):
            continue
        rows.append((s, roc_v, credit / strike if strike else 0.0))
    if not rows:
        return "<p class='muted'>no cash-secured-put candidates</p>"
    symbols = [s for s, _, _ in rows]
    roc = [r for _, r, _ in rows]
    py = [y for _, _, y in rows]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=symbols, y=roc, name="return on capital", marker_color="#3498db",
                         hovertemplate="%{x}<br>RoC %{y:.2%}<extra></extra>"))
    fig.add_trace(go.Bar(x=symbols, y=py, name="premium yield (credit/strike)", marker_color="#e67e22",
                         hovertemplate="%{x}<br>premium yield %{y:.2%}<extra></extra>"))
    fig.update_layout(barmode="group", margin=dict(l=10, r=10, t=40, b=10), height=340,
                      title="Options Premium — return on capital vs premium yield (real Cboe)",
                      yaxis_tickformat=".1%", yaxis_title="per 30-45d", xaxis_title="symbol",
                      xaxis_tickangle=-30, legend=dict(orientation="h", y=1.12),
                      font=dict(color="#e8eef7"), paper_bgcolor="#0f1828", plot_bgcolor="#0f1828")
    return fig.to_html(full_html=False, include_plotlyjs=False, div_id="ch_premium")


# ---------------------------------------------------------------- price trends

def price_chart(series: dict) -> str:
    syms = (series or {}).get("symbols", {}) or {}
    syms = {s: pts for s, pts in syms.items() if pts and len(pts) > 1}
    if not syms:
        return muted("no symbol price series in this report (rebuild the overnight report to include them)")
    fig = go.Figure()
    for sym in sorted(syms):
        pts = syms[sym]
        try:
            closes = [float(p[1]) for p in pts]
        except (TypeError, ValueError, IndexError):
            continue
        if not closes or closes[0] == 0:
            continue
        base = closes[0]
        fig.add_trace(go.Scatter(
            x=[p[0] for p in pts], y=[c / base * 100 for c in closes],
            mode="lines", name=sym,
            hovertemplate=f"{sym}<br>%{{x}}<br>index %{{y:.1f}}<br>${{customdata:,.2f}}<extra></extra>",
            customdata=closes,
        ))
    if not fig.data:
        return muted("symbol price series not parseable in this report")
    fig.update_layout(**base_layout("Equity performance — rebased to 100 (real Yahoo EOD)", 360))
    fig.update_layout(yaxis_title="index (start = 100)", xaxis_title="date",
                      legend=dict(orientation="h", y=-0.25))
    return chart(fig, "ch_prices")


def feature_heatmap(features: dict) -> str:
    feats = (features or {}).get("features", {}) or {}
    cols = ["return_1d", "return_5d", "return_21d", "realized_vol_21d", "range_position_21d"]
    rows = []
    for sym in sorted(feats):
        f = feats[sym]
        try:
            rows.append([sym] + [float(f[c]) for c in cols])
        except (TypeError, ValueError, KeyError):
            continue
    if not rows:
        return muted("no feature bundle in this report")
    # z-score per column for color; annotations carry the raw values.
    import math
    z = []
    for j in range(len(cols)):
        vals = [r[j + 1] for r in rows]
        mu = sum(vals) / len(vals)
        sd = math.sqrt(sum((v - mu) ** 2 for v in vals) / len(vals)) or 1.0
        z.append([(v - mu) / sd for v in vals])
    zmat = [[z[j][i] for j in range(len(cols))] for i in range(len(rows))]
    annot = [[f"{r[j + 1]:.3f}" for j in range(len(cols))] for r in rows]
    fig = go.Figure(go.Heatmap(
        z=zmat, x=cols, y=[r[0] for r in rows], text=annot, texttemplate="%{text}",
        colorscale="RdYlGn", zmin=-2, zmax=2,
        hovertemplate="%{y} · %{x}<br>value %{text}<extra></extra>",
    ))
    fig.update_layout(**base_layout("Feature bundle — per-symbol z-scored heatmap (raw values annotated)", 360))
    return chart(fig, "ch_heatmap")


# ---------------------------------------------------------------- premium desks

def csp_scan_chart(csp: dict) -> str:
    rows = []
    for s, v in (csp or {}).items():
        if not isinstance(v, dict) or v.get("mode") != "CASH_SECURED_PUT":
            continue
        try:
            roc = float((v.get("candidate") or {}).get("return_on_capital"))
        except (TypeError, ValueError):
            continue
        rows.append((s, v, roc))
    if not rows:
        return muted("no cash-secured-put candidates")
    symbols = [s for s, _, _ in rows]
    roc = [r for _, _, r in rows]
    fits = [bool(v.get("fits_gp_rules")) for _, v, _ in rows]
    reasons = ["; ".join(v.get("fit_reasons", []) or v.get("reason_codes", []) or []) for _, v, _ in rows]
    cols = ["#27ae60" if f else "#e74c3c" for f in fits]
    fig = go.Figure(go.Bar(
        x=symbols, y=roc, marker_color=cols, customdata=list(zip(fits, reasons)),
        hovertemplate="%{x}<br>RoC %{y:.2%}<br>fits=%{customdata[0]}<br>%{customdata[1]}<extra></extra>"))
    fig.add_hline(y=0.005, line_dash="dash", line_color="#f39c12")
    fig.add_hline(y=0.02, line_dash="dash", line_color="#f39c12")
    fig.update_layout(**base_layout("Cash-Secured Put Wheel — return on collateral (real Cboe)", 340))
    fig.update_layout(yaxis_tickformat=".1%", yaxis_title="return on collateral",
                      xaxis_title="symbol", xaxis_tickangle=-30)
    tbl = "".join(
        f"<tr><td>{esc(s)}</td><td class='{'ok' if f else 'warn'}'>{esc('FIT' if f else 'NO FIT')}</td>"
        f"<td class='muted'>{esc(rn)}</td></tr>"
        for s, f, rn in zip(symbols, fits, reasons)
    )
    table = (f"<table class='health'><thead><tr><th>symbol</th><th>fit</th><th>reasons</th></tr></thead>"
             f"<tbody>{tbl}</tbody></table>")
    return chart(fig, "ch_csp") + table


def chain_panel(chain_income: dict) -> str:
    chain_income = chain_income or {}
    if not chain_income:
        return muted("no chain-income section in this report")
    parts = []
    for sym, ch in chain_income.items():
        mode = ch.get("mode", "?")
        if mode != "REAL_CBOE_CHAIN_INCOME":
            parts.append(
                f"<div class='blocked'><b>{esc(sym)}</b> — {esc(mode)}"
                f"<br><span class='muted'>{esc(ch.get('reason', 'no reason given'))}</span></div>")
            continue
        structs = [s for s in (ch.get("gated_income_structures", []) or []) if isinstance(s, dict)]
        top = sorted(structs, key=lambda s: -_fnum(s.get("return_on_risk")))[:10]
        trs = "".join(
            f"<tr><td>{esc(s.get('expiration'))}</td><td>{esc(s.get('days_to_expiration'))}</td>"
            f"<td>${esc(s.get('spread_width'))}</td><td>${esc(s.get('net_credit'))}</td>"
            f"<td>${esc(s.get('maximum_loss'))}</td>"
            f"<td>{_fnum(s.get('return_on_risk')):.1%}</td>"
            f"<td class='{'ok' if s.get('gate_decision') == 'APPROVED' else 'warn'}'>"
            f"{esc(s.get('gate_decision'))}</td></tr>"
            for s in top
        )
        parts.append(
            f"<h4>{esc(sym)} vertical credit spreads — top 10 by return on risk "
            f"(real Cboe delayed chain, underlying ${esc(ch.get('underlying_bid'))} / ${esc(ch.get('underlying_ask'))})</h4>"
            f"<table class='health'><thead><tr><th>expiry</th><th>DTE</th><th>width</th>"
            f"<th>credit</th><th>max loss</th><th>RoR</th><th>gate</th></tr></thead>"
            f"<tbody>{trs or '<tr><td colspan=7 class=muted>no admissible structures</td></tr>'}</tbody></table>"
            f"<p class='muted'>{esc(ch.get('gate_note', ''))}</p>")
    return "".join(parts)


def candidates_chart(cands: list) -> str:
    rows = []
    for c in cands or []:
        if not isinstance(c, dict):
            continue
        sym = c.get("symbol")
        if sym is None:
            continue
        try:
            req = float(c.get("requirement"))
        except (TypeError, ValueError):
            continue
        rows.append((sym, req, c.get("strategy")))
    if not rows:
        return muted("no candidates")
    sym = [r[0] for r in rows]
    req = [r[1] for r in rows]
    strat = [r[2] for r in rows]
    color = {"CASH_SECURED_PUT": "#3498db", "COVERED_CALL": "#e67e22", "CREDIT_SPREAD": "#9b59b6"}
    fig = go.Figure(go.Bar(x=sym, y=req, marker_color=[color.get(s, "#777") for s in strat],
                           customdata=strat,
                           hovertemplate="%{x}<br>%{customdata}<br>collateral %{y:$,.0f}<extra></extra>"))
    fig.update_layout(**base_layout(f"Equity Candidates — collateral by symbol ({len(cands)})", 340))
    fig.update_layout(yaxis_title="collateral ($)", xaxis_title="symbol", xaxis_tickangle=-30)
    return chart(fig, "ch_cands")


# ---------------------------------------------------------------- rates / vix / oil

def rates_chart(rates: dict, series: dict) -> str:
    rates = rates or {}
    series = series or {}
    t10 = series.get("treasury_10y") or []
    t2 = series.get("treasury_2y") or []
    if not t10 and not t2:
        return muted("no treasury series in this report (rebuild the overnight report to include them)")
    fig = go.Figure()
    for label, pts, col in (("10Y", t10, "#6ea8ff"), ("2Y", t2, "#f39c12")):
        xs, ys = _xy(pts)
        if not xs:
            continue
        fig.add_trace(go.Scatter(x=xs, y=ys,
                                 mode="lines", name=f"{label} Treasury",
                                 line=dict(color=col),
                                 hovertemplate=f"{label} %{{x}}<br>%{{y:.2f}}%<extra></extra>"))
    shape = rates.get("curve_shape", "?") if rates.get("mode") == "REAL_FRED_RATES" else "?"
    fig.update_layout(**base_layout(f"Treasury yields — 10Y vs 2Y (FRED, curve {shape})", 340))
    fig.update_layout(yaxis_title="yield %", xaxis_title="date")
    return chart(fig, "ch_rates")


def vix_chart(series: dict, vix: dict) -> str:
    xs, ys = _xy((series or {}).get("vix"))
    if not xs:
        return muted("no VIX series in this report")
    regime = (vix or {}).get("regime", "?")
    fig = go.Figure(go.Scatter(x=xs, y=ys,
                               mode="lines", name="VIX", line=dict(color="#e74c3c"),
                               hovertemplate="VIX %{x}<br>%{y:.2f}<extra></extra>"))
    fig.update_layout(**base_layout(f"VIX 3-month trend (Yahoo, regime {regime})", 320))
    fig.update_layout(yaxis_title="VIX", xaxis_title="date")
    return chart(fig, "ch_vix")


def wti_chart(series: dict, oil: dict) -> str:
    xs, ys = _xy((series or {}).get("wti"))
    if not xs:
        return muted("no WTI series in this report")
    fig = go.Figure(go.Scatter(x=xs, y=ys,
                               mode="lines+markers", name="WTI", line=dict(color="#27ae60"),
                               hovertemplate="WTI %{x}<br>$%{y:.2f}<extra></extra>"))
    fig.update_layout(**base_layout("WTI front-month trend (Yahoo CL=F)", 320))
    fig.update_layout(yaxis_title="$", xaxis_title="date")
    return chart(fig, "ch_wti")


# ---------------------------------------------------------------- earnings / paper

def earnings_table(earnings_actuals: dict) -> str:
    ea = earnings_actuals or {}
    real = [(k, v) for k, v in ea.items() if isinstance(v, dict) and v.get("mode") == "REAL_EDGAR_EARNINGS"]
    if not real:
        return muted("no real EDGAR earnings actuals in this report")
    trs = ""
    for cik, v in real:
        obs = v.get("observation", {}) or {}
        trs += (f"<tr><td>{esc(cik)}</td><td>{esc(obs.get('form', ''))}</td>"
                f"<td>{esc(obs.get('filed', obs.get('period', '')))}</td>"
                f"<td>{esc(v.get('quarterly_eps_change'))}</td>"
                f"<td>{esc(v.get('surprise_computed'))}</td></tr>")
    return (f"<table class='health'><thead><tr><th>CIK</th><th>form</th><th>filed</th>"
            f"<th>quarterly EPS Δ</th><th>surprise</th></tr></thead><tbody>{trs}</tbody></table>"
            f"<p class='muted'>source: SEC EDGAR companyfacts</p>")


def paper_panels(paper: dict, yellow: dict) -> str:
    paper = paper or {}
    yellow = yellow or {}
    oc = paper.get("outcome_counts", {}) or {}
    bd = yellow.get("by_decision", {}) or {}
    return (
        f"<div class='macropanel'>"
        f"<div class='metric'><div class='ml'>paper log entries</div><div class='mv'>{esc(paper.get('entry_count', 0))}</div></div>"
        f"<div class='metric'><div class='ml'>yellow sheets</div><div class='mv'>{esc(yellow.get('sheet_count', 0))}</div></div>"
        f"</div>"
        f"<p class='muted'>paper outcomes: {esc(json.dumps(oc))}<br>"
        f"yellow-sheet decisions: {esc(json.dumps(bd))}<br>{esc(paper.get('note', ''))}</p>"
    )


# ---------------------------------------------------------------- build

def card(title: str, body: str, wide: bool = False) -> str:
    cls = "card wide" if wide else "card"
    return f"<div class='{cls}'><h3>{esc(title)}</h3>{body}</div>"


def build() -> None:
    if not REPORT.exists():
        raise SystemExit(f"no report at {REPORT}")
    r = json.loads(REPORT.read_text())
    series = r.get("series", {}) or {}
    body = "\n".join([
        card("Source health — what the batch actually closed on", source_health(r), wide=True),
        card("Macro backdrop", macro_panel(r.get("vix_regime", {}), r.get("rates_environment", {}),
                                           r.get("oil_market", {}), r.get("macro_environment", {}))),
        card("Paper trail", paper_panels(r.get("paper_outcome_summary", {}), r.get("yellow_sheets", {}))),
        card("Equity performance", price_chart(series), wide=True),
        card("Feature heatmap", feature_heatmap(r.get("features", {})), wide=True),
        card("Cash-secured puts", csp_scan_chart(r.get("cash_secured_put_scan")), wide=True),
        card("Options premium", premium_yield_chart(r.get("cash_secured_put_scan")), wide=True),
        card("Equity candidates", candidates_chart(r.get("candidates", [])), wide=True),
        card("Premium chain income", chain_panel(r.get("chain_income", {})), wide=True),
        card("Rates", rates_chart(r.get("rates_environment", {}), series)),
        card("Volatility", vix_chart(series, r.get("vix_regime", {}))),
        card("WTI oil", wti_chart(series, r.get("oil_market", {}))),
        card("Earnings actuals", earnings_table(r.get("earnings_actuals", {})), wide=True),
    ])
    html_doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Emporion — Overnight Desk</title>
<script src="{PLOTLY_JS}"></script>
<style>
body{{margin:0;font-family:-apple-system,'Segoe UI',Roboto,sans-serif;background:#0b1220;color:{FG}}}
header{{padding:18px 28px;background:#111a2c;border-bottom:1px solid #1e2b47;display:flex;align-items:center;gap:12px}}
header h1{{margin:0;font-size:20px}} header .tag{{color:#6ea8ff;font-size:12px}}
.gbtn{{margin-left:auto;color:#e8eef7;text-decoration:none;background:#1a2a4a;border:1px solid #2a3f6a;padding:8px 14px;border-radius:8px;font-size:13px;white-space:nowrap}}
.gbtn:hover{{background:#24406e}}
.ts{{padding:10px 28px;color:#93a5c4;font-size:12px}}
.ts{{padding:10px 28px;color:{MUTED};font-size:12px}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:18px;padding:0 28px 28px}}
.card{{background:{BG};border:1px solid #1e2b47;border-radius:10px;padding:10px;overflow:hidden}}
.card.wide{{grid-column:1/-1}}
.card h3{{margin:6px 4px 10px;font-size:15px;color:{FG}}}
.card h4{{margin:10px 4px;font-size:13px}}
.macropanel{{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;padding:8px}}
.metric{{background:#111c30;border:1px solid #1e2b47;border-radius:8px;padding:14px}}
.ml{{color:{MUTED};font-size:12px}} .ml .src{{color:#6ea8ff;font-size:10px}}
.mv{{font-size:26px;font-weight:600;margin-top:4px}}
.muted{{color:{MUTED};font-size:12px}}
table.health{{width:100%;border-collapse:collapse;font-size:12px;margin:6px 0}}
table.health th,table.health td{{text-align:left;padding:6px 8px;border-bottom:1px solid #1e2b47}}
table.health th{{color:{MUTED};font-weight:600}}
td.ok{{color:#27ae60}} td.warn{{color:#f39c12}}
.blocked{{background:#2a1a12;border:1px solid #7a4a1f;border-radius:8px;padding:12px;margin:8px 0;font-size:13px}}
@media(max-width:900px){{.grid{{grid-template-columns:1fr}}.grid{{padding:0 12px 12px}}header{{padding:14px 12px}}.ts{{padding:8px 12px}}}}
</style></head><body>
<header><span style="font-size:26px">⚓</span><div><h1>Emporion Overnight Desk</h1>
<div class="tag">compass · real data · paper-only</div></div>
<a class="gbtn" href="/guide/selling-options-premium">📘 Selling Options Premium — visual guide</a></header>
{freshness_strip(r)}
<div class="grid">
{body}
</div>
</body></html>"""
    OUT.write_text(html_doc)
    print(f"wrote {OUT} ({len(html_doc)} bytes)")


if __name__ == "__main__":
    build()
