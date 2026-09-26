"""Build the Emporion interactive Plotly dashboard from the REAL overnight report.

Reads artifacts/am-report-latest.json (real Yahoo/Cboe/FRED/EDGAR data) and emits
a self-contained HTML with Plotly interactive charts. No synthetic data, no
fabricated numbers — charts render only what the real report contains.
"""
import json
from pathlib import Path

import plotly.graph_objects as go

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts" / "am-report-latest.json"
OUT = ROOT / "artifacts" / "am-demo.html"


def csp_scan_chart(csp: dict) -> go.Figure:
    rows = [(s, v) for s, v in (csp or {}).items() if v.get("mode") == "CASH_SECURED_PUT"]
    if not rows:
        return go.Figure()
    symbols = [s for s, _ in rows]
    roc = [float(v["candidate"]["return_on_capital"]) for _, v in rows]
    fits = [v.get("fits_gp_rules", False) for _, v in rows]
    cols = ["#2ecc71" if f else "#e74c3c" for f in fits]
    fig = go.Figure(go.Bar(x=symbols, y=roc, marker_color=cols,
                           customdata=fits, hovertemplate="%{x}<br>RoC %{y:.2%}<br>fits=%{customdata}<extra></extra>",
                           name="return on collateral"))
    fig.add_hline(y=0.005, line_dash="dash", line_color="#888", annotation_text="0.5% band floor")
    fig.add_hline(y=0.02, line_dash="dash", line_color="#888", annotation_text="2% band ceiling")
    fig.update_layout(title="Cash-Secured Put Wheel — Return on Collateral (real Cboe)",
                      yaxis_tickformat=".1%", yaxis_title="return on collateral",
                      xaxis_title="symbol", template="plotly_dark",
                      annotations=[dict(x=1, y=1.05, xref="paper", yref="paper",
                                        text="green=fits GP rules · red=outside 0.5–2% band", showarrow=False)])
    return fig


def candidates_chart(cands: list) -> go.Figure:
    sym = [c["symbol"] for c in cands]
    req = [float(c["requirement"]) for c in cands]
    strat = [c["strategy"] for c in cands]
    color = {"CASH_SECURED_PUT": "#3498db", "COVERED_CALL": "#e67e22", "CREDIT_SPREAD": "#9b59b6"}
    fig = go.Figure(go.Bar(x=sym, y=req, marker_color=[color[s] for s in strat],
                           customdata=strat, hovertemplate="%{x}<br>%{customdata}<br>collateral %{y:$,.0f}<extra></extra>"))
    fig.update_layout(title=f"Equity Candidates — collateral by symbol ({len(cands)} real)",
                      yaxis_title="collateral ($)", template="plotly_dark", showlegend=False)
    return fig


def macro_row(vix: dict, rates: dict, oil: dict, macro: dict) -> go.Figure:
    cells, labels = [], []
    if vix.get("mode") == "REAL_VIX":
        labels += ["VIX", "VIX regime"]; cells += [f"{float(vix['last_close']):.1f}", vix["regime"]]
    if rates.get("mode") == "REAL_FRED_RATES":
        labels += ["Fed funds %", "10Y %"]; cells += [f"{rates.get('fed_funds_effective_rate')}", f"{rates.get('treasury_10y_yield')}"]
    if oil.get("mode") == "REAL_YAHOO_WTI":
        labels += ["WTI oil $"]; cells += [f"{float(oil['last_close']):.1f}"]
    if macro.get("mode") == "REAL_FRED_MACRO":
        labels += ["CPI YoY %"]; cells += [f"{macro.get('cpi_yoy_pct')}"]
    fig = go.Figure(go.Indicator(mode="number", value=1,
                                 number={"valueformat":"", "suffix":""}))
    txt = "<br>".join(f"<b>{l}</b>: {v}" for l, v in zip(labels, cells))
    fig.add_annotation(text=txt, x=0.5, y=0.5, showarrow=False, xref="paper", yref="paper",
                       font={"size": 22})
    fig.update_layout(title="Real Macro Backdrop", template="plotly_dark",
                      xaxis={"visible": False}, yaxis={"visible": False})
    return fig


def build() -> None:
    if not REPORT.exists():
        raise SystemExit(f"no report at {REPORT}")
    r = json.loads(REPORT.read_text())
    figs = {
        "csp": csp_scan_chart(r.get("cash_secured_put_scan")),
        "cands": candidates_chart(r["candidates"]),
        "macro": macro_row(r.get("vix_regime", {}), r.get("rates_environment", {}),
                           r.get("oil_market", {}), r.get("macro_environment", {})),
    }
    gen = (f"<p class='ts'>REAL overnight report · generated {r['generated_at']} · "
           f"{len(r['candidates'])} candidates · {r['mode']} · live_orders {r.get('live_orders_enabled', False)}</p>")
    divs = "".join(f'<div class="grid">{f.to_html(full_html=False, include_plotlyjs=("cdn" if i == 0 else False), div_id=f"ch{i}")}</div>'
                   for i, f in enumerate(figs.values()))
    html = f"""<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Emporion — Overnight Desk</title>
<style>
body{{margin:0;font-family:-apple-system,Segoe UI,Roboto,sans-serif;background:#0b1220;color:#e8eef7}}
header{{padding:20px 28px;background:#111a2c;border-bottom:1px solid #1e2b47}}
header h1{{margin:0;font-size:22px}} header .tag{{color:#6ea8ff;font-size:13px}}
.ts{{padding:10px 28px;color:#93a5c4;font-size:12px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(420px,1fr));gap:18px;padding:0 28px 28px}}
.grid>div{{background:#0f1828;border:1px solid #1e2b47;border-radius:10px;overflow:hidden}}
</style></head><body>
<header><h1>⚓ Emporion Overnight Desk</h1><div class="tag">compass · real data · paper-only · plotting what the batch actually closed on</div></header>
{gen}{divs}
</body></html>"""
    OUT.write_text(html)
    print(f"wrote {OUT} ({len(html)} bytes)")


if __name__ == "__main__":
    build()
