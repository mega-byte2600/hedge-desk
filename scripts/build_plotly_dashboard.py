"""Build the Emporion interactive Plotly dashboard from the REAL overnight report.

Reads artifacts/am-report-latest.json (real Yahoo/Cboe/FRED/EDGAR data) and emits
a self-contained HTML with Plotly interactive charts. plotly.js is loaded once
from CDN in the <head>. No synthetic data, no fabricated numbers.
"""
import json
from pathlib import Path

import plotly.graph_objects as go

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts" / "am-report-latest.json"
OUT = ROOT / "artifacts" / "am-demo.html"

PLOTLY_JS = "https://cdn.plot.ly/plotly-2.35.2.min.js"


def csp_scan_chart(csp: dict) -> str:
    rows = [(s, v) for s, v in (csp or {}).items() if v.get("mode") == "CASH_SECURED_PUT"]
    if not rows:
        return "<p class='muted'>no cash-secured-put candidates</p>"
    symbols = [s for s, _ in rows]
    roc = [float(v["candidate"]["return_on_capital"]) for _, v in rows]
    fits = [bool(v.get("fits_gp_rules")) for _, v in rows]
    cols = ["#27ae60" if f else "#e74c3c" for f in fits]
    fig = go.Figure(go.Bar(x=symbols, y=roc, marker_color=cols, customdata=fits,
                           hovertemplate="%{x}<br>RoC %{y:.2%}<br>fits=%{customdata}<extra></extra>"))
    fig.add_hline(y=0.005, line_dash="dash", line_color="#f39c12")
    fig.add_hline(y=0.02, line_dash="dash", line_color="#f39c12")
    fig.update_layout(margin=dict(l=10, r=10, t=40, b=10), height=340,
                      title="Cash-Secured Put Wheel — return on collateral (real Cboe)",
                      yaxis_tickformat=".1%", yaxis_title="return on collateral",
                      xaxis_title="symbol", xaxis_tickangle=-30,
                      font=dict(color="#e8eef7"), paper_bgcolor="#0f1828", plot_bgcolor="#0f1828")
    return fig.to_html(full_html=False, include_plotlyjs=False, div_id="ch_csp")


def candidates_chart(cands: list) -> str:
    sym = [c["symbol"] for c in cands]
    req = [float(c["requirement"]) for c in cands]
    strat = [c["strategy"] for c in cands]
    color = {"CASH_SECURED_PUT": "#3498db", "COVERED_CALL": "#e67e22", "CREDIT_SPREAD": "#9b59b6"}
    fig = go.Figure(go.Bar(x=sym, y=req, marker_color=[color.get(s, "#777") for s in strat],
                           customdata=strat, hovertemplate="%{x}<br>%{customdata}<br>collateral %{y:$,.0f}<extra></extra>"))
    fig.update_layout(margin=dict(l=10, r=10, t=40, b=10), height=340,
                      title=f"Equity Candidates — collateral by symbol ({len(cands)})",
                      yaxis_title="collateral ($)", xaxis_title="symbol", xaxis_tickangle=-30,
                      font=dict(color="#e8eef7"), paper_bgcolor="#0f1828", plot_bgcolor="#0f1828")
    return fig.to_html(full_html=False, include_plotlyjs=False, div_id="ch_cands")


def premium_yield_chart(csp: dict) -> str:
    """Options premium economics: return-on-capital vs premium-yield (net_credit/strike).

    Real Cboe data from the CSP scan. Two metrics per PREMIUM_WHEEL_ECONOMICS.md:
    return_on_capital = net_credit/collateral (small, on full capital deployed);
    premium_yield = net_credit/strike (what 'sell premium' intuitively means).
    """
    rows = [(s, v) for s, v in (csp or {}).items() if v.get("mode") == "CASH_SECURED_PUT"]
    if not rows:
        return "<p class='muted'>no cash-secured-put candidates</p>"
    symbols = [s for s, _ in rows]
    roc = [float(v["candidate"]["return_on_capital"]) for _, v in rows]
    py = []
    for _, v in rows:
        c = v["candidate"]
        credit = float(c["net_credit_per_share"])
        strike = float(c["strike"])
        py.append(credit / strike if strike else 0.0)
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


def macro_panel(vix: dict, rates: dict, oil: dict, macro: dict) -> str:
    cells = []  # (label, value, source)
    if vix.get("mode") == "REAL_VIX":
        cells.append((f"VIX ({vix.get('regime', '?')})", f"{float(vix['last_close']):.1f}", "Yahoo"))
    if rates.get("mode") == "REAL_FRED_RATES":
        cells.append(("Fed funds %", str(rates.get("fed_funds_effective_rate", "-")), "FRED"))
        if rates.get("treasury_10y_yield"):
            cells.append(("10Y Treasury %", str(rates["treasury_10y_yield"]), "FRED"))
    if oil.get("mode") == "REAL_YAHOO_WTI":
        cells.append(("WTI oil $", f"{float(oil['last_close']):.1f}", "Yahoo"))
    if macro.get("mode") == "REAL_FRED_MACRO":
        if macro.get("cpi_yoy_pct"):
            cells.append(("CPI YoY %", str(macro["cpi_yoy_pct"]), "FRED"))
        if macro.get("unemployment_rate"):
            cells.append(("Unemployment %", str(macro["unemployment_rate"]), "FRED"))
    blocks = "".join(
        f'<div class="metric"><div class="ml">{l} <span class="src">{s}</span></div>'
        f'<div class="mv">{v}</div></div>'
        for l, v, s in cells
    )
    return f'<div class="macropanel">{blocks or "<p class=muted>no real macro</p>"}</div>'


def build() -> None:
    if not REPORT.exists():
        raise SystemExit(f"no report at {REPORT}")
    r = json.loads(REPORT.read_text())
    csp = csp_scan_chart(r.get("cash_secured_put_scan"))
    cands = candidates_chart(r["candidates"])
    premium = premium_yield_chart(r.get("cash_secured_put_scan"))
    macro = macro_panel(r.get("vix_regime", {}), r.get("rates_environment", {}),
                        r.get("oil_market", {}), r.get("macro_environment", {}))
    html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Emporion — Overnight Desk</title>
<script src="{PLOTLY_JS}"></script>
<style>
body{{margin:0;font-family:-apple-system,'Segoe UI',Roboto,sans-serif;background:#0b1220;color:#e8eef7}}
header{{padding:18px 28px;background:#111a2c;border-bottom:1px solid #1e2b47;display:flex;align-items:center;gap:12px}}
header h1{{margin:0;font-size:20px}} header .tag{{color:#6ea8ff;font-size:12px}}
.gbtn{{margin-left:auto;color:#e8eef7;text-decoration:none;background:#1a2a4a;border:1px solid #2a3f6a;padding:8px 14px;border-radius:8px;font-size:13px;white-space:nowrap}}
.gbtn:hover{{background:#24406e}}
.ts{{padding:10px 28px;color:#93a5c4;font-size:12px}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:18px;padding:0 28px 28px}}
.card{{background:#0f1828;border:1px solid #1e2b47;border-radius:10px;padding:10px;overflow:hidden}}
.card.wide{{grid-column:1/-1}}
.macropanel{{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;padding:8px}}
.metric{{background:#111c30;border:1px solid #1e2b47;border-radius:8px;padding:14px}}
.ml{{color:#93a5c4;font-size:12px}} .ml .src{{color:#6ea8ff;font-size:10px}}
.mv{{font-size:26px;font-weight:600;margin-top:4px}}
.muted{{color:#93a5c4}}
@media(max-width:900px){{.grid{{grid-template-columns:1fr}}}}
</style></head><body>
<header><span style="font-size:26px">⚓</span><div><h1>Emporion Overnight Desk</h1>
<div class="tag">compass · real data · paper-only · what the batch actually closed on</div></div>
<a class="gbtn" href="/guide/selling-options-premium">📘 Selling Options Premium — visual guide</a></header>
<p class="ts">REAL overnight report · generated {r['generated_at']} ·
{len(r['candidates'])} candidates · {r['mode']} · live_orders {str(r.get('live_orders_enabled', False))}</p>
<div class="grid">
<div class="card">{macro}</div>
<div class="card wide">{cands}</div>
<div class="card wide">{premium}</div>
<div class="card wide">{csp}</div>
</div>
</body></html>"""
    OUT.write_text(html)
    print(f"wrote {OUT} ({len(html)} bytes)")


if __name__ == "__main__":
    build()
