"""Build the Emporion interactive Plotly dashboard from the REAL overnight report.

Reads artifacts/am-report-latest.json (real Yahoo/Cboe/FRED/EDGAR data) and emits
a self-contained HTML with Plotly interactive charts. plotly.js is loaded once
from CDN in the <head>. No synthetic data, no fabricated numbers. BLOCKED or
missing sections render as honest state panels, never as invented values.
"""
from typing import Optional
import html
import json
import sys
from pathlib import Path

# Allow `python3 scripts/build_plotly_dashboard.py` from the repo root: the
# script directory (not the root) lands on sys.path in that mode.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from hedge_desk.candidates import CIK_TO_SYMBOL
from hedge_desk.desk_call import build_desk_call
from hedge_desk.premium_score import atm_benchmark_from_report

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts" / "am-report-latest.json"
OUT = ROOT / "artifacts" / "am-demo.html"

# Plotly is vendored in web/vendor (served at /vendor/ by hedge_desk.server).
# Load order: served path -> repo-relative path (file:// opens of artifacts/)
# -> versioned CDN, so charts render offline and behind CDN-blocking CSPs.
PLOTLY_VERSION = "2.35.2"
PLOTLY_LOADER = (
    f'<script src="/vendor/plotly-{PLOTLY_VERSION}.min.js"></script>'
    "<script>window.Plotly||document.write('<script src=\"../web/vendor/plotly-"
    f"{PLOTLY_VERSION}.min.js\"><\\/script>')</script>"
    "<script>window.Plotly||document.write('<script src=\"https://cdn.plot.ly/plotly-"
    f"{PLOTLY_VERSION}.min.js\"><\\/script>')</script>"
)

BG = "#121215"
FG = "#f4f1e8"
MUTED = "#a39e93"


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


def chart(fig: go.Figure, div_id: str, source: str = "") -> str:
    """Keep descriptive chart headings outside Plotly's toolbar/axis canvas.

    The visible heading occupies normal document flow, never shares a drawing
    layer with the floating modebar, axes, annotations or legends. Retain the
    complete original title as text and keep every real-data trace unchanged.
    """
    heading = str(fig.layout.title.text or "") if fig.layout.title else ""
    fig.update_layout(title=None, autosize=True)
    fig.update_xaxes(automargin=True)
    fig.update_yaxes(automargin=True)
    # Legends for multi-series visuals need their own real estate. A wrapped
    # seven-symbol legend cannot share the plotting rectangle on a 390px phone.
    # Do not change series, values, axis semantics or visibility.
    if len(fig.data) > 1 and fig.layout.showlegend is not False:
        margin = dict(fig.layout.margin.to_plotly_json()) if fig.layout.margin else {}
        margin.update(l=max(54, margin.get("l", 0)),
                      r=max(20, margin.get("r", 0)),
                      t=max(26, margin.get("t", 0)), b=max(118, margin.get("b", 0)))
        fig.update_layout(legend=dict(orientation="h", x=0, xanchor="left", y=-0.25,
                                      yanchor="top"), margin=margin,
                          height=max(430, fig.layout.height or 0))
    html = fig.to_html(
        full_html=False, include_plotlyjs=False, div_id=div_id,
        config={"responsive": True, "displaylogo": False},
    )
    label = f"<h4 class='chart-caption'>{esc(heading)}</h4>" if heading else ""
    return label + html + (src_note(source) if source else "")


def muted(msg: str) -> str:
    return f"<p class='muted'>{esc(msg)}</p>"


def src_note(source: str) -> str:
    """One-line provenance caption every dashboard visual must carry.

    The user requires every chart/table to state where its data came from,
    so a reader can trace any number back to its origin. Empty source
    renders nothing (the caller, not this helper, decides what is sourced).
    """
    if not source:
        return ""
    return f"<p class='src-note'>source: {esc(source)}</p>"


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

def human_time(value) -> str:
    """'2026-11-18T04:55:20.57+00:00' -> 'Nov 18, 2026 04:55 UTC' (raw on parse failure)."""
    from datetime import datetime, timezone

    try:
        ts = datetime.fromisoformat(str(value).replace("Z", "+00:00")).astimezone(timezone.utc)
    except (TypeError, ValueError):
        return "" if value is None else str(value)
    return ts.strftime("%b %d, %Y %H:%M UTC")


def freshness_strip(r: dict) -> str:
    f = r.get("data_freshness", {}) or {}
    return (
        f"<p class='ts'>REAL overnight report &middot; generated "
        f"<time datetime='{esc(r.get('generated_at'))}'>{esc(human_time(r.get('generated_at')))}</time> &middot; "
        f"{esc(r.get('candidate_count'))} candidates &middot; {esc(r.get('mode'))} &middot; "
        f"eod {esc(r.get('eod_batch_status'))} &middot; "
        f"trading day {esc(f.get('expected_trading_day'))} "
        f"({'current' if f.get('is_current') else 'STALE'})</p>"
    )


def desk_call_block(r: dict) -> str:
    """Three-line decision header (hedge_desk.desk_call): action, shortlist, exits."""
    call = build_desk_call(r)
    spy = (r.get("chain_income") or {}).get("SPY") or {}
    banner = ("" if "premium_universe" in spy or not spy else
              "<p class='dc-banner'>This nightly predates the banded premium universe: the "
              "structures below are the near-the-money return-on-risk set, so none can meet the "
              "10-30 delta band. The next nightly run adds 10-30 delta candidates.</p>")
    def _risk(s):
        pct = s.get("max_loss_pct_demo_equity")
        if pct is None:
            return "—"
        return f"{pct}%" + (" ⚠ over 2%" if float(pct) > 2 else "")
    rows = "".join(
        f"<tr class='{'' if s.get('eligible') else 'dc-inelig'}'><td>{esc(s['contract_id'])}</td><td>{esc(s['days_to_expiration'])}d</td>"
        f"<td>${esc(s['net_credit'])}</td><td>${esc(s['maximum_loss'])}</td>"
        f"<td><b>{esc(s.get('premium_score') if s.get('premium_score') is not None else '—')}</b></td>"
        f"<td>{'✓ eligible' if s.get('eligible') else '✗ ' + esc(', '.join(s.get('eligibility_reasons') or []) or 'not scored')}</td>"
        f"<td>{esc(s.get('probability_of_profit') or '—')}</td><td>{esc(s.get('risk_neutral_ev') or '—')}</td>"
        f"<td>{esc(s['invalidation_underlying_through'])}</td>"
        f"<td>${esc(s.get('collateral_per_contract'))} / {esc(_risk(s))} / {esc(s.get('example_max_contracts_2pct_demo_equity'))}</td>"
        f"<td>+${esc(s['take_profit_at_credit_captured'])} / −${esc(s['stop_at_loss'])}</td></tr>"
        for s in call["shortlist"])
    ctx = call["context"]
    cls = "dc-go" if call["action"] == "PAPER_CANDIDATE" else "dc-no"
    return (
        f"<section class='deskcall {cls}' aria-labelledby='dc-h'>"
        f"<h2 id='dc-h'>Desk call · {esc(call['as_of'])}: {esc(call['action'].replace('_', ' '))}</h2>"
        f"{banner}<p class='dc-head'>{esc(call['headline'])} VIX {esc(ctx['vix_close'])} "
        f"({esc(ctx['vix_regime'])}). Reasons: {esc('; '.join(call['reason_codes']) or 'none')}.</p>"
        "<div class='dc-wrap'><table><caption>Top 3 SPY credit verticals, ranked by "
        f"{esc(call['ranked_by'])}. Exits: take profit at 50% of credit, close by 21 DTE, stop at 50% of max loss.</caption>"
        "<thead><tr><th scope='col'>Structure</th><th scope='col'>DTE</th><th scope='col'>Credit</th>"
        "<th scope='col'>Max loss</th><th scope='col'>Premium score</th><th scope='col'>GP bands</th>"
        "<th scope='col'>P(profit) (ref, delayed)</th><th scope='col'>RN EV (ref)</th>"
        "<th scope='col'>Invalidation</th><th scope='col'>Collateral / risk per contract (% of DEMO equity) / max contracts under 2% rule</th><th scope='col'>Exit +/−</th></tr></thead>"
        f"<tbody>{rows}</tbody></table></div>"
        "<p class='dc-foot'>Paper only. Probabilities are risk-neutral, not forecasts. "
        "<span data-hook='dc-prob-delayed-reference'>P(profit) and RN EV are reference only: "
        "computed from delayed option data, not probability claims.</span> "
        "Nothing is trade-authorized; a human approves every paper entry.</p>"
        f"<p class='dc-foot' id='dc-age' data-generated='{esc(r.get('generated_at'))}'>Report generated "
        f"{esc(human_time(r.get('generated_at')))}.</p>"
        "<script>(function(){var e=document.getElementById('dc-age');if(!e)return;var g=Date.parse(e.dataset.generated);"
        "if(isNaN(g))return;var h=Math.round((Date.now()-g)/36e5);e.textContent+=' Age: '+h+'h'+(h>24?' — STALE (over 24h)':'');"
        "if(h>24){e.style.color='#e0a43a';e.style.fontWeight='700';}})();</script></section>")


def _human_status(mode: str) -> str:
    """Map internal mode codes to user-facing status labels.

    Never leak internal enum names (REAL_*, BLOCKED, READY_*) to readers.
    """
    mode = str(mode or "?").upper()
    if mode.startswith("REAL_") or mode in ("CASH_SECURED_PUT", "PASS"):
        return "Live"
    if mode == "BLOCKED":
        return "Unavailable"
    if mode == "READY_FOR_RESEARCH":
        return "Ready"
    if mode in ("?", "UNKNOWN"):
        return "Unknown"
    # Fallback: title-case the code without underscores, never raw.
    return mode.replace("_", " ").title()


def _human_detail(detail: str) -> str:
    """Map internal reason/note strings to user-facing explanations."""
    detail = str(detail or "").strip()
    if not detail:
        return ""
    low = detail.lower()
    # Never show raw fetch errors or status codes to readers.
    if "fetch failed" in low or "status 0" in low or "status 403" in low:
        return "Couldn't reach the source just now."
    if "upstream" in low or "auth failure" in low:
        return "Couldn't reach the source just now."
    if low.startswith("fred"):
        return "Couldn't reach the source just now."
    return detail


def source_health(r: dict) -> str:
    """Per-source status table: what the batch actually closed on."""
    rows = []
    rows.append(("Daily prices (Yahoo)", _human_status(r.get("eod_batch_status", "?")),
                 _human_detail(str((r.get("data_freshness", {}) or {}).get("note", "")))))
    for sym, ch in (r.get("chain_income", {}) or {}).items():
        mode = ch.get("mode", "?")
        if mode == "BLOCKED":
            detail = _human_detail(ch.get("reason", ""))
        else:
            n = len(ch.get('gated_income_structures', []) or [])
            detail = f"{n} structures" if n else ""
        rows.append((f"Options data (Cboe {sym})", _human_status(mode), detail))
    for label, key in (("Rates (FRED)", "rates_environment"), ("Market volatility (VIX)", "vix_regime"),
                       ("Economy (FRED)", "macro_environment"), ("Oil WTI (Yahoo)", "oil_market")):
        d = r.get(key, {}) or {}
        rows.append((label, _human_status(d.get("mode", "?")),
                     _human_detail(str(d.get("reason", d.get("note", ""))))))
    csp = r.get("cash_secured_put_scan", {}) or {}
    real_csp = sum(1 for v in csp.values() if isinstance(v, dict) and v.get("mode") == "CASH_SECURED_PUT")
    rows.append(("Cash-secured puts (Cboe)", f"{real_csp}/{len(csp)} live" if real_csp else "Unavailable", ""))
    ea = r.get("earnings_actuals", {}) or {}
    real_ea = sum(1 for v in ea.values() if isinstance(v, dict) and v.get("mode") == "REAL_EDGAR_EARNINGS")
    rows.append(("Earnings (SEC)", f"{real_ea}/{len(ea)} live" if real_ea else "Unavailable", ""))
    trs = "".join(
        f"<tr><td>{esc(a)}</td><td class='{'ok' if b == 'Live' or b == 'Ready' else 'warn'}'>{esc(b)}</td>"
        f"<td class='muted'>{esc(c)}</td></tr>"
        for a, b, c in rows
    )
    return (f"<table class='health'><thead><tr><th>source</th><th>status</th><th>detail</th></tr></thead>"
            f"<tbody>{trs}</tbody></table>")


# ---------------------------------------------------------------- macro

def history_trend_chart() -> str:
    """Real multi-day trend from the dated nightly reports (am-report-*.json).

    Shows how candidates, the wheel's average return-on-collateral, and VIX
    moved across the last N closes — real history, not a single snapshot.
    """
    import glob
    dates, cands, roc, vix = [], [], [], []
    for f in sorted(glob.glob(str(ROOT / "artifacts" / "am-report-*.json"))):
        if "latest" in f:
            continue
        try:
            r = json.loads(Path(f).read_text())
        except (OSError, ValueError):
            continue
        d = Path(f).name.replace("am-report-", "").replace(".json", "")
        csp = r.get("cash_secured_put_scan", {})
        rocs = [float(v["candidate"]["return_on_capital"])
                for v in csp.values() if v.get("mode") == "CASH_SECURED_PUT"]
        dates.append(d)
        cands.append(len(r.get("candidates", [])))
        roc.append(round(sum(rocs) / len(rocs), 4) if rocs else None)
        vix.append(r.get("vix_regime", {}).get("last_close"))
    if len(dates) < 2:
        return "<p class='muted'>need 2+ dated reports for a trend</p>"
    # Separate scales vertically rather than overlaying three y-axes. The
    # previous mobile layout placed VIX and RoC tick labels atop each other.
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.10,
                        subplot_titles=("Candidates", "Average return on collateral", "VIX"))
    fig.add_trace(go.Scatter(x=dates, y=cands, name="candidates", mode="lines+markers",
                             line=dict(color="#c6a15b"),
                             hovertemplate="%{x}<br>%{y} candidates<extra></extra>"), row=1, col=1)
    fig.add_trace(go.Scatter(x=dates, y=roc, name="avg return on collateral", mode="lines+markers",
                             line=dict(color="#dcb96f"),
                             hovertemplate="%{x}<br>avg RoC %{y:.2%}<extra></extra>"), row=2, col=1)
    fig.add_trace(go.Scatter(x=dates, y=vix, name="VIX", mode="lines+markers",
                             line=dict(color="#8a6d3b"),
                             hovertemplate="%{x}<br>VIX %{y:.1f}<extra></extra>"), row=3, col=1)
    fig.update_layout(margin=dict(l=62, r=20, t=86, b=52), height=560,
                      title="Multi-Day Trend — real nightly history",
                      showlegend=False,
                      font=dict(color="#f4f1e8"), paper_bgcolor="#121215", plot_bgcolor="#121215")
    fig.update_yaxes(gridcolor="#232329", tickformat=".0f", row=1, col=1)
    fig.update_yaxes(gridcolor="#232329", tickformat=".1%", row=2, col=1)
    fig.update_yaxes(gridcolor="#232329", tickformat=".1f", row=3, col=1)
    fig.update_xaxes(title_text="date", row=3, col=1)
    return chart(fig, "ch_trend", source="Dated real overnight reports, nightly batch")


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
    if rates.get("mode") == "REAL_FRED_RATES":
        cells.append(("Fed funds %", str(rates.get("fed_funds_effective_rate", "-")), "FRED"))
        if rates.get("treasury_10y_yield"):
            cells.append(("10Y Treasury %", str(rates["treasury_10y_yield"]), "FRED"))
        if rates.get("spread_10y_2y_points"):
            cells.append(("10Y-2Y bp", str(rates["spread_10y_2y_points"]), "FRED"))
    if oil.get("mode") == "REAL_YAHOO_WTI" and oil.get("last_close") is not None:
        try:
            cells.append(("WTI oil $", f"{float(oil['last_close']):.1f}", "Yahoo"))
        except (TypeError, ValueError):
            pass
    if macro.get("mode") == "REAL_FRED_MACRO":
        if macro.get("cpi_yoy_pct"):
            cells.append(("CPI YoY %", str(macro["cpi_yoy_pct"]), "FRED"))
        # Report key is unemployment_rate_pct (not the older unemployment_rate).
        if macro.get("unemployment_rate_pct"):
            cells.append(("Unemployment %", str(macro["unemployment_rate_pct"]), "FRED"))
        if macro.get("treasury_5y"):
            cells.append(("5Y Treasury %", str(macro["treasury_5y"]), "FRED"))
        if macro.get("treasury_30y"):
            cells.append(("30Y Treasury %", str(macro["treasury_30y"]), "FRED"))
    elif macro.get("mode") == "BLOCKED":
        # Withheld rather than fabricated: show a short marker, not the full
        # reason string (which lives in the report JSON for audit).
        cells.append(("Macro (FRED)", "withheld — refetch pending", "FRED"))
    blocks = "".join(
        f'<div class="metric"><div class="ml">{esc(l)} <span class="src">{esc(s)}</span></div>'
        f'<div class="mv">{esc(v)}</div></div>'
        for l, v, s in cells
    )
    return f'<div class="macropanel">{blocks or "<p class=muted>no real macro</p>"}</div>'


# ------------------------------------------------------- live public data
# Carpe-data panels: raw open-market feeds rendered directly from the batch's
# market_context block. Every metric carries its source; nothing is invented.

def _mc_sources(r: dict) -> dict:
    return ((r.get("market_context", {}) or {}).get("sources", {}) or {})


def nasdaq_quotes_panel(r: dict) -> str:
    src = _mc_sources(r).get("nasdaq-quotes", {}) or {}
    obs = src.get("observations") or []
    if src.get("status") != "LIVE" or not obs:
        return "<p class='muted'>Nasdaq quotes unavailable in this batch</p>" + src_note("Nasdaq public quote API")
    cells = []
    for o in obs:
        sym = esc(o.get("symbol", "?"))
        price = esc(o.get("lastSalePrice", "-"))
        chg = esc(o.get("percentageChange", ""))
        ts = esc(o.get("lastTradeTimestamp", ""))
        rt = "live" if o.get("isRealTime") else "delayed"
        cells.append(
            f'<div class="metric"><div class="ml">{sym} <span class="src">Nasdaq · {rt}</span></div>'
            f'<div class="mv">{price}</div><div class="muted">{chg} · {ts}</div></div>'
        )
    return f'<div class="macropanel">{"".join(cells)}</div>' + src_note("Nasdaq public quote API (no key)")


def fx_panel(r: dict) -> str:
    src = _mc_sources(r).get("ecb-fx", {}) or {}
    obs = src.get("observations") or []
    if src.get("status") != "LIVE" or not obs:
        return "<p class='muted'>ECB reference rates unavailable in this batch</p>" + src_note("ECB euro reference rates")
    cells = []
    for o in obs:
        cells.append(
            f'<div class="metric"><div class="ml">EUR/{esc(o.get("currency", "?"))} '
            f'<span class="src">ECB</span></div>'
            f'<div class="mv">{esc(o.get("rate", "-"))}</div>'
            f'<div class="muted">{esc(o.get("date", ""))}</div></div>'
        )
    return f'<div class="macropanel">{"".join(cells)}</div>' + src_note("ECB euro foreign exchange reference rates (daily)")


def world_bank_gdp_panel(r: dict) -> str:
    """World Bank GDP (current US$) trend — global macro context (keyless)."""
    src = _mc_sources(r).get("world-bank", {}) or {}
    obs = src.get("observations") or []
    if src.get("status") != "LIVE" or not obs:
        return "<p class='muted'>World Bank indicator unavailable in this batch</p>" + src_note("World Bank Open Data API (NY.GDP.MKTP.CD)")
    # observations: {indicator: {id,value}, country:{...}, date, value, ...}
    points = []
    country = "US"
    for o in obs:
        try:
            points.append((str(o.get("date", "")), _fnum(o.get("value"))))
        except (TypeError, ValueError):
            continue
        if o.get("countryiso3code"):
            country = str(o.get("countryiso3code"))
    points = [(d, v) for d, v in points if v > 0]
    if len(points) < 2:
        return "<p class='muted'>World Bank GDP series too short to chart</p>" + src_note("World Bank Open Data API")
    points.sort()
    years = [d for d, _ in points]
    gdp = [v / 1e12 for _, v in points]
    fig = go.Figure(go.Bar(
        x=years, y=gdp,
        marker_color="#c6a15b",
        hovertemplate="%{x}<br>GDP $%{y:.2f} trillion<extra></extra>"))
    fig.update_layout(**base_layout(f"World Bank GDP — {country} (current US$)", 320))
    fig.update_layout(yaxis_title="USD trillions", xaxis_title="year")
    return chart(fig, "ch_world_gdp", source="World Bank Open Data API (NY.GDP.MKTP.CD), keyless")


def treasury_auctions_panel(r: dict) -> str:
    """Latest U.S. Treasury auctions (fiscaldata API) — debt issuance context."""
    src = _mc_sources(r).get("treasury-fiscaldata", {}) or {}
    obs = src.get("observations") or []
    if src.get("status") != "LIVE" or not obs:
        return "<p class='muted'>Treasury fiscal data unavailable in this batch</p>" + src_note("U.S. Treasury Fiscal Data API")
    trs = "".join(
        f"<tr><td>{esc(o.get('security_type', o.get('auction_date', '?')))}</td>"
        f"<td>{esc(o.get('auction_date', '-'))}</td>"
        f"<td>{esc(o.get('high_investment_rate', '-'))}%</td>"
        f"<td class='muted'>{esc(o.get('maturity_date', '-'))}</td></tr>"
        for o in obs[:6]
    )
    return (f"<table class='health'><thead><tr><th>security</th><th>auction</th>"
            f"<th>high rate</th><th>maturity</th></tr></thead><tbody>{trs}</tbody></table>"
            + src_note("U.S. Treasury Fiscal Data API (rates_of_exchange/auctions), keyless"))


def imf_gdp_panel(r: dict) -> str:
    """IMF real GDP growth (%) — global macro context (keyless)."""
    src = _mc_sources(r).get("imf", {}) or {}
    obs = src.get("observations") or []
    if src.get("status") != "LIVE" or not obs:
        return "<p class='muted'>IMF indicator unavailable in this batch</p>" + src_note("IMF DataMapper API (NGDP_RPCH)")
    points = []
    for o in obs:
        try:
            points.append((str(o.get("date", "")), _fnum(o.get("value"))))
        except (TypeError, ValueError):
            continue
    points = [(d, v) for d, v in points if v is not None]
    if len(points) < 2:
        return "<p class='muted'>IMF GDP series too short to chart</p>" + src_note("IMF DataMapper API")
    points.sort()
    years = [d for d, _ in points]
    growth = [v for _, v in points]
    fig = go.Figure(go.Bar(
        x=years, y=growth,
        marker_color="#7fd1a0",
        hovertemplate="%{x}<br>real GDP growth %{y:.1f}%<extra></extra>"))
    fig.update_layout(**base_layout("IMF real GDP growth — USA (annual %)", 320))
    fig.update_layout(yaxis_title="%", xaxis_title="year")
    return chart(fig, "ch_imf_gdp", source="IMF DataMapper API (NGDP_RPCH), keyless")


def bank_of_canada_panel(r: dict) -> str:
    """Bank of Canada official USD/CAD reference rate (keyless)."""
    src = _mc_sources(r).get("bank-of-canada", {}) or {}
    obs = src.get("observations") or []
    if src.get("status") != "LIVE" or not obs:
        return "<p class='muted'>Bank of Canada FX unavailable in this batch</p>" + src_note("Bank of Canada Valet API")
    points = []
    for o in obs:
        try:
            points.append((str(o.get("date", "")), _fnum(o.get("value"))))
        except (TypeError, ValueError):
            continue
    points = [(d, v) for d, v in points if v > 0]
    if len(points) < 2:
        return "<p class='muted'>Bank of Canada FX series too short to chart</p>" + src_note("Bank of Canada Valet API")
    points.sort()
    dates = [d for d, _ in points]
    rates = [v for _, v in points]
    fig = go.Figure(go.Scatter(
        x=dates, y=rates, mode="lines+markers",
        line=dict(color="#dcb96f"),
        hovertemplate="%{x}<br>USD/CAD %{y:.4f}<extra></extra>"))
    fig.update_layout(**base_layout("Bank of Canada — USD/CAD reference rate", 320))
    fig.update_layout(yaxis_title="USD/CAD", xaxis_title="date")
    return chart(fig, "ch_boc_fx", source="Bank of Canada Valet API (FXUSDCAD), keyless")


def frankfurter_panel(r: dict) -> str:
    """Frankfurter USD-base FX reference rates (keyless, ECB data)."""
    src = _mc_sources(r).get("frankfurter", {}) or {}
    obs = src.get("observations") or []
    if src.get("status") != "LIVE" or not obs:
        return "<p class='muted'>Frankfurter FX unavailable in this batch</p>" + src_note("Frankfurter FX API (ECB data)")
    cells = []
    for o in obs:
        cells.append(
            f'<div class="metric"><div class="ml">USD/{esc(o.get("quote", "?"))} '
            f'<span class="src">Frankfurter</span></div>'
            f'<div class="mv">{esc(o.get("rate", "-"))}</div>'
            f'<div class="muted">{esc(o.get("date", ""))}</div></div>'
        )
    return f'<div class="macropanel">{"".join(cells)}</div>' + src_note("Frankfurter FX API (ECB reference data), keyless")


def treasury_curve_chart(r: dict) -> str:
    src = _mc_sources(r).get("treasury-rates", {}) or {}
    obs = src.get("observations") or []
    if src.get("status") != "LIVE" or not obs:
        return "<p class='muted'>Treasury curve unavailable in this batch</p>"
    latest_date = max(str(o.get("date", "")) for o in obs)
    order = ["DGS1MO", "DGS3MO", "DGS6MO", "DGS1", "DGS2", "DGS3", "DGS5", "DGS7", "DGS10", "DGS20", "DGS30"]
    labels = {"DGS1MO": "1M", "DGS3MO": "3M", "DGS6MO": "6M", "DGS1": "1Y", "DGS2": "2Y", "DGS3": "3Y",
              "DGS5": "5Y", "DGS7": "7Y", "DGS10": "10Y", "DGS20": "20Y", "DGS30": "30Y"}
    xs, ys = [], []
    for tenor in order:
        match = [o for o in obs if o.get("tenor") == tenor and str(o.get("date")) == latest_date]
        if not match:
            continue
        try:
            xs.append(labels.get(tenor, tenor))
            ys.append(float(match[0]["value"]))
        except (TypeError, ValueError):
            continue
    if len(xs) < 2:
        return "<p class='muted'>Treasury curve unavailable in this batch</p>"
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines+markers", line=dict(color="#c6a15b"),
                             hovertemplate="%{x}: %{y:.2f}%<extra></extra>"))
    fig.update_layout(margin=dict(l=10, r=10, t=40, b=10), height=300,
                      title=f"U.S. Treasury par yield curve — {latest_date}",
                      yaxis=dict(title="yield %", gridcolor="#232329"),
                      xaxis=dict(title="tenor"),
                      font=dict(color="#f4f1e8"), paper_bgcolor="#121215", plot_bgcolor="#121215")
    return chart(fig, "ch_treasury_curve",
                 "FRED DGS constant-maturity series (official U.S. Treasury par yields)")


def market_context_health(r: dict) -> str:
    """Status table for the open public-data plane (market_context block)."""
    sources = _mc_sources(r)
    if not sources:
        return "<p class='muted'>no market-context block in this report</p>"
    pretty = {
        "fred": "Macro/rates (FRED)", "nyfed-markets": "Reference rates (NY Fed)",
        "treasury-fiscaldata": "Auctions (Treasury)", "treasury-rates": "Yield curve (Treasury via FRED)",
        "fdic": "Bank failures (FDIC)", "world-bank": "Indicators (World Bank)",
        "bls": "Labor/prices (BLS)", "ecb-fx": "FX reference (ECB)",
        "cftc-cot": "Positioning (CFTC)", "eia-open-data": "Energy (EIA)",
        "finra": "Fixed income (FINRA)", "nasdaq-quotes": "Quotes (Nasdaq)",
        "nasdaq-earnings": "Earnings calendar (Nasdaq)",
    }
    trs = []
    for key, label in pretty.items():
        s = sources.get(key, {}) or {}
        status = s.get("status", "?")
        if status == "LIVE":
            cell, detail = "ok", f'{s.get("observation_count", 0)} obs'
        elif status == "UNCONFIGURED":
            cell, detail = "warn", "needs API key"
        else:
            cell, detail = "warn", _human_detail(str(s.get("detail", s.get("reason_code", ""))))
        trs.append(f"<tr><td>{esc(label)}</td><td class='{cell}'>{esc(status.title())}</td>"
                   f"<td class='muted'>{esc(detail)}</td></tr>")
    return (f"<table class='health'><thead><tr><th>source</th><th>status</th><th>detail</th></tr></thead>"
            f"<tbody>{''.join(trs)}</tbody></table>"
            + src_note("Batch market-context block: each source fetched live, fail-closed"))


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
    fig.add_trace(go.Bar(x=symbols, y=roc, name="return on capital", marker_color="#c6a15b",
                         hovertemplate="%{x}<br>RoC %{y:.2%}<extra></extra>"))
    fig.add_trace(go.Bar(x=symbols, y=py, name="premium yield (credit/strike)", marker_color="#dcb96f",
                         hovertemplate="%{x}<br>premium yield %{y:.2%}<extra></extra>"))
    fig.update_layout(barmode="group", margin=dict(l=10, r=10, t=40, b=10), height=340,
                      title="Options Premium — return on capital vs premium yield (real Cboe)",
                      yaxis_tickformat=".1%", yaxis_title="per 30-45d", xaxis_title="symbol",
                      xaxis_tickangle=-30, legend=dict(orientation="h", y=1.12),
                      font=dict(color="#f4f1e8"), paper_bgcolor="#121215", plot_bgcolor="#121215")
    return chart(fig, "ch_premium", source="Cboe delayed option chains, nightly premium scan")


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
    fig.update_layout(**base_layout("Equity performance — rebased to 100 (Yahoo daily closes)", 360))
    fig.update_layout(yaxis_title="index (start = 100)", xaxis_title="date",
                      legend=dict(orientation="h", y=-0.25))
    return chart(fig, "ch_prices", source="Yahoo Finance daily closes, nightly batch")


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
    return chart(fig, "ch_heatmap", source="computed from Yahoo Finance daily closes, nightly batch")


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
    return chart(fig, "ch_csp", source="nightly cash-secured-put scan (Yahoo daily + Cboe delayed chains)") + table


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
        def _roc(s):
            c, m = _fnum(s.get("net_credit")), _fnum(s.get("maximum_loss"))
            return c / (c + m) if c + m > 0 else 0.0
        top = sorted(structs, key=lambda s: -_roc(s))[:10]
        trs = "".join(
            f"<tr><td>{esc(s.get('expiration'))}</td><td>{esc(s.get('days_to_expiration'))}</td>"
            f"<td>${esc(s.get('spread_width'))}</td><td>${esc(s.get('net_credit'))}</td>"
            f"<td>${esc(s.get('maximum_loss'))}</td>"
            f"<td>{_roc(s):.1%}</td>"
            f"<td class='{'ok' if s.get('gate_decision') == 'APPROVED' else 'warn'}'>"
            f"{esc(s.get('gate_decision'))}</td></tr>"
            for s in top
        )
        parts.append(
            f"<h4>{esc(sym)} vertical credit spreads — top 10 by return on collateral "
            f"(real Cboe delayed chain, underlying ${esc(ch.get('underlying_bid'))} / ${esc(ch.get('underlying_ask'))})</h4>"
            f"<table class='health'><thead><tr><th>expiry</th><th>DTE</th><th>width</th>"
            f"<th>credit</th><th>max loss</th><th>return on collateral</th><th>gate</th></tr></thead>"
            f"<tbody>{trs or '<tr><td colspan=7 class=muted>no admissible structures</td></tr>'}</tbody></table>"
            f"<p class='muted'>{esc(ch.get('gate_note', ''))}</p>")
    return "".join(parts) + src_note("Cboe delayed option chains, nightly batch")


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
    color = {"CASH_SECURED_PUT": "#c6a15b", "COVERED_CALL": "#dcb96f", "CREDIT_SPREAD": "#8a6d3b"}
    fig = go.Figure(go.Bar(x=sym, y=req, marker_color=[color.get(s, "#777") for s in strat],
                           customdata=strat,
                           hovertemplate="%{x}<br>%{customdata}<br>collateral %{y:$,.0f}<extra></extra>"))
    fig.update_layout(**base_layout(f"Equity Candidates — collateral by symbol ({len(cands)})", 340))
    fig.update_layout(yaxis_title="collateral ($)", xaxis_title="symbol", xaxis_tickangle=-30)
    return chart(fig, "ch_cands", source="nightly candidate batch (Yahoo Finance)")


# ---------------------------------------------------------------- rates / vix / oil

def rates_chart(rates: dict, series: dict) -> str:
    rates = rates or {}
    series = series or {}
    t10 = series.get("treasury_10y") or []
    t2 = series.get("treasury_2y") or []
    if not t10 and not t2:
        return muted("no treasury series in this report (rebuild the overnight report to include them)")
    fig = go.Figure()
    for label, pts, col in (("10Y", t10, "#c6a15b"), ("2Y", t2, "#f39c12")):
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
    return chart(fig, "ch_rates", source="FRED public series, nightly batch")


def vix_chart(series: dict, vix: dict) -> str:
    xs, ys = _xy((series or {}).get("vix"))
    if not xs:
        return muted("no VIX series in this report")
    regime = (vix or {}).get("regime", "?")
    fig = go.Figure(go.Scatter(x=xs, y=ys,
                               mode="lines", name="VIX", line=dict(color="#e74c3c"),
                               hovertemplate="VIX %{x}<br>%{y:.2f}<extra></extra>"))
    fig.update_layout(**base_layout(f"VIX 3-month trend (Yahoo, {regime.lower()})", 320))
    fig.update_layout(yaxis_title="VIX", xaxis_title="date")
    return chart(fig, "ch_vix", source="Yahoo Finance (^VIX), nightly batch")


def wti_chart(series: dict, oil: dict) -> str:
    xs, ys = _xy((series or {}).get("wti"))
    if not xs:
        return muted("no WTI series in this report")
    fig = go.Figure(go.Scatter(x=xs, y=ys,
                               mode="lines+markers", name="WTI", line=dict(color="#27ae60"),
                               hovertemplate="WTI %{x}<br>$%{y:.2f}<extra></extra>"))
    fig.update_layout(**base_layout("WTI front-month trend (Yahoo CL=F)", 320))
    fig.update_layout(yaxis_title="$", xaxis_title="date")
    return chart(fig, "ch_wti", source="Yahoo Finance WTI (CL=F), nightly batch")


# ---------------------------------------------------------------- earnings / paper

def earnings_table(earnings_actuals: dict) -> str:
    ea = earnings_actuals or {}
    real = [(k, v) for k, v in ea.items() if isinstance(v, dict) and v.get("mode") == "REAL_EDGAR_EARNINGS"]
    if not real:
        return muted("no reported earnings in this report")
    trs = ""
    for cik, v in real:
        obs = v.get("observation", {}) or {}
        latest = obs.get('latest_quarterly_eps', '')
        period = obs.get('latest_quarterly_period', '')
        prior = obs.get('prior_quarterly_eps', '')
        change = v.get('quarterly_eps_change', '')
        trs += (f"<tr><td>{esc(cik)}</td><td>{esc(latest)}</td>"
                f"<td>{esc(period)}</td>"
                f"<td>{esc(prior)}</td>"
                f"<td>{esc(change)}</td></tr>")
    return (f"<table class='health'><thead><tr><th>CIK</th><th>Latest EPS</th><th>Period</th>"
            f"<th>Prior EPS</th><th>Change</th></tr></thead><tbody>{trs}</tbody></table>"
            f"<p class='muted'>source: SEC filings</p>")


def earnings_eps_chart(earnings_actuals: dict) -> str:
    """Quarterly EPS: latest vs prior quarter per CIK (real SEC EDGAR actuals).

    Grouped bars, one group per filer. Only entries with mode
    REAL_EDGAR_EARNINGS and parseable quarterly EPS are drawn; anything else
    yields the honest empty state, never an invented bar.
    """
    ea = earnings_actuals or {}
    rows = []  # (label, latest_eps, latest_period, prior_eps, prior_period)
    for cik, v in ea.items():
        if not isinstance(v, dict) or v.get("mode") != "REAL_EDGAR_EARNINGS":
            continue
        obs = v.get("observation") or {}
        try:
            latest = float(obs["latest_quarterly_eps"])
            prior = float(obs["prior_quarterly_eps"])
        except (TypeError, ValueError, KeyError):
            continue
        label = CIK_TO_SYMBOL.get(str(cik), str(cik))
        rows.append((label,
                     latest, str(obs.get("latest_quarterly_period", "")),
                     prior, str(obs.get("prior_quarterly_period", ""))))
    if not rows:
        return muted("no real quarterly EPS observations in this report")
    labels = [r[0] for r in rows]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=labels, y=[r[1] for r in rows], name="latest quarter",
        marker_color="#c6a15b",
        customdata=[r[2] for r in rows],
        hovertemplate="%{x} %{customdata}<br>EPS $%{y:.2f}<extra></extra>"))
    fig.add_trace(go.Bar(
        x=labels, y=[r[3] for r in rows], name="prior quarter",
        marker_color="#5a6b8c",
        customdata=[r[4] for r in rows],
        hovertemplate="%{x} %{customdata}<br>EPS $%{y:.2f}<extra></extra>"))
    fig.update_layout(**base_layout("Quarterly EPS — latest vs prior (SEC EDGAR actuals)", 340))
    fig.update_layout(barmode="group", yaxis_title="EPS $", xaxis_title="filer",
                      legend=dict(orientation="h", y=1.12))
    return chart(fig, "ch_earnings_eps", source="SEC EDGAR companyfacts, nightly batch")


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
        + src_note("paper-outcomes.jsonl + yellow-sheets.jsonl, nightly batch")
    )


# ---------------------------------------------------------------- build

def premium_candidates_panel(chain_income: dict, csp_scan: Optional[dict] = None,
                             atm_benchmark: Optional[float] = None) -> str:
    """Trader view (GP brief): premium-selling candidates, Wall-Street style.

    Structures are re-scored at render time from the report's own real inputs
    (IV, RV, rate, DTE, credit) with the current premium model, so the page
    reflects the model even between nightly runs. Eligible structures (10-30
    delta, 21-60 DTE, positive vol edge) always rank first; one row per short
    leg; every row shows why it is or is not eligible. The GP's wheel (cash-
    secured puts) is shown alongside with return on collateral."""
    from hedge_desk.premium_score import rank_chain_income, rank_key, unique_by_short_leg
    rows = []
    for sym, chain in (chain_income or {}).items():
        chain = chain or {}
        rk = chain.get("ranking") or {}
        if rk.get("by") == "premium_score":
            chain = rank_chain_income(chain, rk.get("realized_vol_21d_annual"), rk.get("rate") or 0.0,
                                      rk.get("dividend_yield"), atm_benchmark)
        for s in ((chain.get("gated_income_structures") or chain.get("income_structures") or [])
                  + list(chain.get("premium_universe") or [])):
            if (s.get("premium") or {}).get("premium_score") is not None:
                rows.append(s)
    if not rows:
        blocked = [(sym, (ch or {}).get("reason")) for sym, ch in (chain_income or {}).items()
                   if (ch or {}).get("mode") == "BLOCKED"]
        if blocked:
            # Honest data health (CarpeDATA): say WHY there are no candidates.
            return ("<div class='blocked'><b>No premium candidates tonight: option chain unavailable.</b> "
                    + "; ".join(f"{esc(sym)}: {esc(reason or 'no reason given')}" for sym, reason in blocked)
                    + ". Nothing is scored or ranked from missing data; the last good report is not "
                    "re-used for candidates.</div>")
        return muted("Premium scores appear after the next nightly run (this report predates the "
                     "premium-selling score).")
    top = unique_by_short_leg(sorted(rows, key=rank_key))[:10]
    n_eligible = sum(1 for s in top if s["premium"].get("eligible"))
    labels = [f"{'✓ ' if s['premium'].get('eligible') else '✗ '}{s.get('contract_id', '')[:18]}… "
              f"{s.get('days_to_expiration')}d" for s in top][::-1]
    names = {"vol_edge": "Vol edge (30%)", "time_value": "Return on collateral (25%)",
             "entry_window": "30-45 DTE window (25%)", "strike_placement": "10-30 delta (20%)"}
    colors = {"vol_edge": "#c9a227", "time_value": "#8a6d3b", "entry_window": "#5b8db8", "strike_placement": "#7fa37a"}
    fig = go.Figure()
    for k, label in names.items():
        w = top[0]["premium"]["weights"][k]
        fig.add_bar(y=labels, x=[round(100 * w * s["premium"]["components"][k], 1) for s in top][::-1],
                    name=label, orientation="h", marker_color=colors[k])
    fig.update_layout(**base_layout("Premium score by component (0-100); ✓ eligible, ✗ outside GP bands", height=440),
                      barmode="stack")
    reason_text = {"DELTA_OUT_OF_BAND": "delta outside 10-30", "NO_VOL_EDGE": "IV ≤ realized vol (no edge)",
                   "DTE_OUT_OF_WINDOW": "DTE outside 21-60"}

    def _row(s):
        p = s["premium"]
        i = p["inputs"]
        why = "; ".join(reason_text.get(r, r) for r in p.get("eligibility_reasons") or []) or "eligible"
        vrp = i.get("variance_risk_premium")
        return (f"<tr><td>{'✓' if p.get('eligible') else '✗'}</td><td>{esc(s.get('contract_id'))}</td>"
                f"<td>{esc(p['premium_score'])}</td><td>{esc(s.get('days_to_expiration'))}</td>"
                f"<td>{esc(i.get('short_leg_abs_delta'))}</td>"
                f"<td>{esc('—' if vrp is None else f'{round(100 * vrp)}%')}</td>"
                f"<td>{esc(round(100 * i.get('return_on_collateral_30d', 0), 1))}%</td>"
                f"<td>${esc(p['management']['take_profit_at_credit_captured'])} / "
                f"{esc(p['management']['days_until_time_exit'])}d</td><td>{esc(why)}</td></tr>")
    table = ("<div class='dc-wrap'><table><caption>"
             f"{n_eligible} of {len(top)} shortlisted structures meet the GP bands. Ineligible rows are shown "
             "for context and always rank below eligible ones. Return on collateral for spreads is on the "
             "spread width, so it runs far above the cash-secured wheel's 1-2% per trade.</caption><thead><tr>"
             "<th scope='col'>OK</th><th scope='col'>Structure</th><th scope='col'>Score</th>"
             "<th scope='col'>DTE</th><th scope='col'>|Δ| short</th><th scope='col'>Vol edge (IV vs RV)</th>"
             "<th scope='col'>Return on collateral / 30d</th><th scope='col'>Take profit / days to 21-DTE exit</th>"
             f"<th scope='col'>Why / warnings</th></tr></thead><tbody>{''.join(_row(s) for s in top)}</tbody></table></div>")
    wheel = ""
    csp_rows = []
    demo_equity = None
    for ch in (chain_income or {}).values():
        try:
            demo_equity = float((ch or {}).get("gate_demo_account_equity"))
            break
        except (TypeError, ValueError):
            continue
    for sym, res in sorted((csp_scan or {}).items()):
        c = (res or {}).get("candidate") or {}
        if not c.get("found"):
            continue
        try:
            otm = 100 * (1 - float(c["strike"]) / float(c["underlying_mid"]))
        except (KeyError, TypeError, ValueError, ZeroDivisionError):
            otm = None
        reasons = list(res.get("eval_reasons") or [])
        roc = float(c.get("return_on_capital") or 0)
        if roc < 0.01 and "RETURN_BELOW_GP_BAND" not in reasons:
            reasons.append("RETURN_BELOW_GP_BAND")
        fits = bool(res.get("fits_gp_rules")) and not reasons
        try:
            max_c = int((demo_equity * 0.02) // float(c.get("max_loss") or 0)) if demo_equity else None
        except (TypeError, ValueError, ZeroDivisionError):
            max_c = None
        csp_rows.append(
            f"<tr><td>{'✓' if fits else '✗'}</td><td>{esc(sym)}</td>"
            f"<td>{esc(c.get('contract_id'))}</td><td>{esc(c.get('dte'))}</td>"
            f"<td>{esc('—' if otm is None else f'{otm:.1f}%')}</td>"
            f"<td>{esc(round(100 * float(c.get('return_on_capital') or 0), 2))}%</td>"
            f"<td>${esc(c.get('collateral_required'))}</td>"
            f"<td>{esc('—' if max_c is None else max_c)}</td>"
            f"<td>{esc(', '.join(reasons) or 'fits GP wheel')}</td></tr>")
    if csp_rows:
        wheel = ("<h4 class='chart-caption'>GP wheel — cash-secured puts (target ~30-45 DTE, ~10% OTM, "
                 "1-2% return on collateral)</h4><div class='dc-wrap'><table><thead><tr>"
                 "<th scope='col'>Fits</th><th scope='col'>Symbol</th><th scope='col'>Contract</th>"
                 "<th scope='col'>DTE</th><th scope='col'>OTM</th><th scope='col'>Return on collateral</th>"
                 "<th scope='col'>Collateral</th><th scope='col'>Max contracts (2% rule, DEMO equity)</th>"
                 "<th scope='col'>Reasons</th></tr></thead>"
                 f"<tbody>{''.join(csp_rows)}</tbody></table></div>")
    return (chart(fig, "premium-candidates",
                  source="Cboe delayed chain + Yahoo EOD realized vol; hedge_desk.premium_score")
            + table + wheel)

def yellow_sheet_outcomes_table(ys: Optional[dict]) -> str:
    """Each GP Yellow Sheet next to the paper outcome of the trade it describes."""
    rows = [r for r in (ys or {}).get("rows") or []]
    if not rows:
        return muted("No credit-spread Yellow Sheets to connect yet. Record one with "
                     "scripts/record_yellow_sheet.py; it links to its ledger trade automatically.")
    def _out(r):
        if r.get("link") != "LINKED":
            return esc(r.get("link", "").replace("_", " ").lower())
        if r.get("status") == "OPEN":
            return "open"
        return (f"{'✓ thesis held' if r.get('thesis_held') else '✗ thesis failed'} · ${esc(r.get('pnl_usd'))}"
                f" · RoC {esc(r.get('return_on_collateral'))}")
    trs = "".join(
        f"<tr><td>#{esc(r.get('yellow_sheet_seq'))}</td><td>{esc(r.get('symbol'))} {esc(r.get('strike'))}</td>"
        f"<td>{esc(r.get('decision'))}</td><td>{esc((r.get('thesis') or '')[:90])}</td><td>{_out(r)}</td></tr>"
        for r in rows)
    return ("<h4 class='chart-caption'>Yellow Sheets → paper outcome</h4><div class='dc-wrap'><table><thead><tr>"
            "<th scope='col'>Sheet</th><th scope='col'>Structure</th><th scope='col'>Decision</th>"
            "<th scope='col'>Thesis</th><th scope='col'>Outcome</th></tr></thead>"
            f"<tbody>{trs}</tbody></table></div>")


def premium_ledger_panel(summary: Optional[dict], yellow_sheets: Optional[dict] = None) -> str:
    """Paper track record of the premium score (hedge_desk.premium_ledger):
    hold-to-expiry outcomes by score band — the evidence for the weights."""
    if not summary or summary.get("status") == "LEDGER_UNAVAILABLE" or "entries" not in summary:
        return muted("Paper track record starts with the first nightly that records eligible candidates; "
                     "outcomes settle on each expiration's real close.")
    rows = "".join(
        f"<tr><td>{esc(name)}</td><td>{esc(st['n'])}</td><td>{esc(st['win_rate'] or '—')}</td>"
        f"<td>{esc(('$' + st['avg_pnl_usd']) if st['avg_pnl_usd'] else '—')}</td>"
        f"<td>{esc(st['avg_return_on_collateral'] or '—')}</td></tr>"
        for name, st in [("All settled", summary["overall"])] + list(summary["by_score_band"].items()))
    return (f"<p class='muted'>{esc(summary['entries'])} recorded · {esc(summary['open'])} open · "
            f"{esc(summary['settled'])} settled.</p>"
            "<div class='dc-wrap'><table><thead><tr><th scope='col'>Score band</th><th scope='col'>Settled</th>"
            "<th scope='col'>Win rate</th><th scope='col'>Avg P&amp;L</th><th scope='col'>Avg return on collateral</th>"
            f"</tr></thead><tbody>{rows}</tbody></table></div><p class='muted'>{esc(summary['note'])}</p>"
            + yellow_sheet_outcomes_table(yellow_sheets)
            + src_note("artifacts/premium-ledger.jsonl (append-only); settled on Yahoo EOD expiry closes"))


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
        card("Live public data — watchlist quotes", nasdaq_quotes_panel(r), wide=True),
        card("Live public data — Treasury curve", treasury_curve_chart(r), wide=True),
        card("Live public data — FX reference", fx_panel(r)),
        card("Global markets — World Bank GDP", world_bank_gdp_panel(r)),
        card("Global markets — Treasury auctions", treasury_auctions_panel(r)),
        card("Global markets — IMF GDP growth", imf_gdp_panel(r)),
        card("Global markets — Bank of Canada FX", bank_of_canada_panel(r)),
        card("Global markets — Frankfurter FX", frankfurter_panel(r)),
        card("Public data plane — source status", market_context_health(r)),
        card("Macro backdrop", macro_panel(r.get("vix_regime", {}), r.get("rates_environment", {}),
                                           r.get("oil_market", {}), r.get("macro_environment", {}))),
        card("Paper trail", paper_panels(r.get("paper_outcome_summary", {}), r.get("yellow_sheets", {}))),
        card("Equity performance", price_chart(series), wide=True),
        card("Multi-day trend", history_trend_chart(), wide=True),
        card("Feature heatmap", feature_heatmap(r.get("features", {})), wide=True),
        card("Cash-secured puts", csp_scan_chart(r.get("cash_secured_put_scan")), wide=True),
        card("Options premium", premium_yield_chart(r.get("cash_secured_put_scan")), wide=True),
        card("Equity candidates", candidates_chart(r.get("candidates", [])), wide=True),
        card("Premium-selling candidates", premium_candidates_panel(r.get("chain_income", {}), r.get("cash_secured_put_scan"),
                                                                        atm_benchmark_from_report(r, "SPY")), wide=True),
        card("Premium score — paper track record", premium_ledger_panel(r.get("premium_ledger"), r.get("yellow_sheet_outcomes")), wide=True),
        card("Premium chain income", chain_panel(r.get("chain_income", {})), wide=True),
        card("Rates", rates_chart(r.get("rates_environment", {}), series)),
        card("Volatility", vix_chart(series, r.get("vix_regime", {}))),
        card("WTI oil", wti_chart(series, r.get("oil_market", {}))),
        card("Earnings actuals", earnings_table(r.get("earnings_actuals", {})), wide=True),
        card("Earnings — quarterly EPS", earnings_eps_chart(r.get("earnings_actuals", {})), wide=True),
    ])
    html_doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#0a0a0c">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<title>Emporion — Overnight Desk</title>
{PLOTLY_LOADER}
<style>
body{{margin:0;font-family:'Inter',-apple-system,'Segoe UI',sans-serif;background:#0a0a0c;color:{FG}}}
header{{padding:16px 28px;background:#0a0a0c;border-bottom:1px solid #232329;display:flex;flex-wrap:wrap;align-items:center;gap:14px}}
.brand-logo{{width:46px;height:46px;object-fit:contain;display:block;filter:drop-shadow(0 2px 8px rgba(198,161,91,.22))}}
header h1{{margin:0;font-family:'Fraunces',Georgia,serif;font-size:20px;letter-spacing:.02em;font-weight:600}} header .tag{{color:#c6a15b;font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:.14em;text-transform:uppercase}}
.gbtn{{margin-left:auto;color:#f4f1e8;text-decoration:none;background:#121215;border:1px solid #8a6d3b;padding:8px 14px;border-radius:6px;font-size:13px;white-space:nowrap}}
.gbtn:hover{{background:#17130d}}
.ts{{padding:10px 28px;color:#a39e93;font-size:12px}}
.ts{{padding:10px 28px;color:{MUTED};font-size:12px}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:18px;padding:0 28px 28px}}
.card{{background:{BG};border:1px solid #232329;border-radius:10px;padding:10px;overflow:hidden}}
.card.wide{{grid-column:1/-1}}
.card h3{{margin:6px 4px 10px;font-size:15px;color:{FG}}}
.card h4{{margin:10px 4px;font-size:13px}}
/* Chart names have their own accessible, wrapping line above the graphics. */
.chart-caption{{font-size:13px;line-height:1.45;margin:12px 6px 6px;color:#f4f1e8;font-weight:500;overflow-wrap:anywhere}}
.card .js-plotly-plot{{width:100%;max-width:100%;min-width:0}}
.card .plot-container{{max-width:100%}}
.card, .grid{{min-width:0}}
.card svg{{overflow:visible}}
.macropanel{{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;padding:8px}}
.metric{{background:#121215;border:1px solid #232329;border-radius:8px;padding:14px}}
.ml{{color:{MUTED};font-size:12px}} .ml .src{{color:#c6a15b;font-size:10px}}
.mv{{font-size:26px;font-weight:600;margin-top:4px}}
.muted{{color:{MUTED};font-size:12px}}
.src-note{{color:{MUTED};font-size:11px;margin:6px 2px 0;font-style:italic}}
table.health{{width:100%;border-collapse:collapse;font-size:12px;margin:6px 0}}
table.health th,table.health td{{text-align:left;padding:6px 8px;border-bottom:1px solid #232329}}
table.health th{{color:{MUTED};font-weight:600}}
td.ok{{color:#27ae60}} td.warn{{color:#f39c12}}
.blocked{{background:#2a1a12;border:1px solid #7a4a1f;border-radius:8px;padding:12px;margin:8px 0;font-size:13px}}
@media(max-width:900px){{.grid{{grid-template-columns:1fr}}.grid{{padding:0 12px 12px}}header{{padding:14px 12px}}.gbtn{{margin-left:0;white-space:normal}}.ts{{padding:8px 12px}}}}
/* Plotly's floating controls must not cover chart labels on a phone. */
.js-plotly-plot .plotly .modebar-container{{top:44px!important}}
@media(max-width:640px){{
 .js-plotly-plot .plotly .modebar-container{{display:none!important}}
 .js-plotly-plot .gtitle{{display:none!important}}
 .chart-caption{{font-size:13px;line-height:1.5}}
 .card{{padding:10px 8px}}
 .grid{{gap:12px}}
 .js-plotly-plot .legend{{max-width:100%}}
 .card{{min-width:0}}
 .js-plotly-plot{{max-width:100%}}
}}
.deskcall{{overflow-wrap:anywhere;min-width:0;max-width:100%;box-sizing:border-box;margin:16px 28px;padding:14px 18px;border:1px solid #232329;border-left:4px solid #8a6d3b;border-radius:8px;background:#121215}}.deskcall h2{{margin:0 0 6px;font-size:18px}}.dc-head{{margin:0 0 10px;color:#f4f1e8}}.dc-wrap{{overflow-x:auto}}.deskcall table{{border-collapse:collapse;width:100%;font-size:13px}}.deskcall caption{{text-align:left;color:#a39e93;font-size:12px;padding-bottom:6px}}.deskcall th,.deskcall td{{padding:6px 8px;border-bottom:1px solid #232329;text-align:left;white-space:nowrap}}.dc-foot{{margin:8px 0 0;font-size:12px;color:#a39e93}}.dc-inelig td{{color:#8b867c}}.dc-banner{{margin:0 0 8px;padding:6px 10px;border-left:3px solid #e0a43a;background:#1a1712;font-size:13px}}.dc-no{{border-left-color:#a39e93}}@media(max-width:900px){{.deskcall{{margin:12px}}}}
</style></head><body>
<header><img class="brand-logo" src="/brand/emporion-logo-hermes-transparent.png?v=20261004-power" alt="Emporion" onerror="this.onerror=null;this.src='../web/brand/emporion-logo-hermes-transparent.png'"><div><h1>Emporion Overnight Desk</h1>
<div class="tag">Markets · Intelligence · Discipline</div></div>
<a class="gbtn" href="/guide/selling-options-premium">📘 Selling Options Premium — visual guide</a></header>
{desk_call_block(r)}
{freshness_strip(r)}
<div class="grid">
{body}
</div>
</body></html>"""
    OUT.write_text(html_doc)
    print(f"wrote {OUT} ({len(html_doc)} bytes)")


if __name__ == "__main__":
    build()
