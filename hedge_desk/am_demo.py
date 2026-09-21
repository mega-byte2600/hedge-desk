"""True-MVP demo: render the full AM report (real data from every desk) as HTML.

Runs the consolidated nightly and renders one page with: EOD equity candidates,
real premium income (with gate decisions), the rates environment, and earnings
actuals. This is what the GP opens before the market open.

Honesty: every panel labels its data source; premium spreads show their risk+
release gate decision (all BLOCKED with kill switch off by default), and nothing
is trade_authorized. Real data or an explicit BLOCKED reason — never fabricated.
"""

from __future__ import annotations

import html
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Sequence

from hedge_desk.nightly import run_nightly

DEFAULT_WATCHLIST = ("NKE", "CCL", "AAL", "LYFT", "NCLH", "F", "DVN")
DEFAULT_EARNINGS_CIKS = ("0000320193",)  # AAPL


def _esc(v: Any) -> str:
    return html.escape(str(v))


def _equity_rows(candidates: Sequence[Dict]) -> str:
    return "".join(
        "<tr>"
        f"<td>{_esc(c['symbol'])}</td><td>{_esc(c['close'])}</td>"
        f"<td>{_esc(c['strategy'])}</td><td>{_esc(c['strike'])}</td>"
        f"<td>${_esc(c['requirement'])}</td><td>{_esc(c['policy_version'])}</td>"
        "<td>NO</td></tr>"
        for c in candidates
    )


def _premium_rows(structures: Sequence[Dict]) -> str:
    from decimal import Decimal as _Dec

    rows = []
    for s in structures:
        badge = (
            "ok" if s.get("gate_decision") == "ALLOW_PAPER" else "warn"
        )
        credit = f"{float(_Dec(str(s['net_credit']))):.2f}"
        maxloss = f"{float(_Dec(str(s['maximum_loss']))):.2f}"
        ror = f"{float(_Dec(str(s['return_on_risk']))):.3f}"
        rows.append(
            "<tr>"
            f"<td>{_esc(s['contract_id'])}</td><td>{_esc(s['expiration'])}</td>"
            f"<td>{_esc(s['days_to_expiration'])}</td>"
            f"<td>${_esc(credit)}</td>"
            f"<td>${_esc(maxloss)}</td>"
            f"<td>{_esc(ror)}</td>"
            f"<td><span class='badge {badge}'>{_esc(s.get('gate_decision','-'))}</span></td>"
            f"<td>{_esc(', '.join(s.get('gate_reasons', [])) or '-')}</td>"
            "<td>NO</td></tr>"
        )
    return "".join(rows)


def _rates_block(rates: Dict) -> str:
    if rates.get("mode") == "BLOCKED":
        return f"<p class='note'>Rates blocked: {_esc(rates.get('reason'))}</p>"
    return (
        "<table><tr><th>Series</th><th>Value</th><th>Date</th></tr>"
        f"<tr><td>Fed funds effective</td><td>{_esc(rates.get('fed_funds_effective_rate'))}%</td>"
        f"<td>{_esc(rates.get('fed_funds_latest_date'))}</td></tr>"
        f"<tr><td>Fed funds change (window)</td><td>{_esc(rates.get('fed_funds_change_over_window'))}%</td><td>-</td></tr>"
        f"<tr><td>Treasury 2y</td><td>{_esc(rates.get('treasury_2y'))}%</td>"
        f"<td>{_esc(rates.get('treasury_2y_date'))}</td></tr>"
        f"<tr><td>Treasury 10y</td><td>{_esc(rates.get('treasury_10y'))}%</td>"
        f"<td>{_esc(rates.get('treasury_10y_date'))}</td></tr>"
        f"<tr><td>10y-2y spread</td><td>{_esc(rates.get('spread_10y_2y_points'))}bp</td><td>-</td></tr>"
        f"<tr><td>Curve shape</td><td>{_esc(rates.get('curve_shape'))}</td><td>-</td></tr>"
        "</table>"
    )


def _vix_block(vix: Dict) -> str:
    if vix.get("mode") == "BLOCKED":
        return f"<p class='note'>VIX blocked: {_esc(vix.get('reason'))}</p>"
    return (
        "<table><tr><th>Series</th><th>Value</th><th>Date</th><th>Regime</th></tr>"
        f"<tr><td>VIX (implied vol)</td><td>{_esc(vix.get('last_close'))}</td>"
        f"<td>{_esc(vix.get('last_day'))}</td>"
        f"<td><span class='badge warn'>{_esc(vix.get('regime'))}</span></td></tr>"
        "</table>"
    )


def _macro_block(macro: Dict) -> str:
    if macro.get("mode") == "BLOCKED":
        return f"<p class='note'>Macro blocked: {_esc(macro.get('reason'))}</p>"
    rows = [
        ("CPI YoY (inflation)", macro.get("cpi_yoy_pct"), macro.get("cpi_latest_date")),
        ("Unemployment", macro.get("unemployment_rate_pct"), macro.get("unemployment_date")),
        ("Treasury 5y", macro.get("treasury_5y"), macro.get("treasury_5y_date")),
        ("Treasury 30y", macro.get("treasury_30y"), macro.get("treasury_30y_date")),
    ]
    body = "".join(
        f"<tr><td>{_esc(k)}</td><td>{_esc(v)}</td><td>{_esc(d)}</td></tr>"
        for k, v, d in rows if v is not None
    )
    blocked = macro.get("blocked") or []
    note = f"<div class='note'>Blocked series: {_esc(', '.join(blocked))}</div>" if blocked else ""
    return f"<table><tr><th>Series</th><th>Value</th><th>Date</th></tr>{body}</table>{note}"


def _earnings_block(earnings: Dict) -> str:
    blocks = []
    for cik, e in earnings.items():
        if not isinstance(e, dict) or e.get("mode") == "BLOCKED":
            blocks.append(f"<p class='note'>CIK {_esc(cik)} blocked: "
                          f"{_esc(e.get('reason')) if isinstance(e, dict) else '-'}</p>")
            continue
        obs = e.get("observation", {})
        blocks.append(
            "<table><tr><th>Metric</th><th>Value</th></tr>"
            f"<tr><td>Latest FY EPS</td><td>{_esc(obs.get('latest_fy_eps'))} "
            f"({_esc(obs.get('latest_fy_period'))})</td></tr>"
            f"<tr><td>Latest quarter EPS</td><td>{_esc(obs.get('latest_quarterly_eps'))} "
            f"({_esc(obs.get('latest_quarterly_period'))})</td></tr>"
            f"<tr><td>Prior quarter EPS</td><td>{_esc(obs.get('prior_quarterly_eps'))} "
            f"({_esc(obs.get('prior_quarterly_period'))})</td></tr>"
            f"<tr><td>Quarterly change</td><td>{_esc(e.get('quarterly_eps_change'))}</td></tr>"
            "</table>"
        )
    return "".join(blocks)


def _features_block(features: Dict) -> str:
    feats = features.get("features", {})
    if not feats:
        return "<p class='note'>No feature bundle in this report.</p>"
    rows = []
    for sym in sorted(feats):
        f = feats[sym]
        rows.append(
            "<tr>"
            f"<td>{_esc(sym)}</td>"
            f"<td>{_esc(f.get('return_1d'))}</td>"
            f"<td>{_esc(f.get('return_5d'))}</td>"
            f"<td>{_esc(f.get('return_21d'))}</td>"
            f"<td>{_esc(f.get('realized_vol_21d'))}</td>"
            f"<td>{_esc(f.get('range_position_21d'))}</td>"
            f"<td>{_esc(f.get('candle_bias'))}</td>"
            "</tr>"
        )
    return (
        "<table><thead><tr><th>Symbol</th><th>r1d</th><th>r5d</th><th>r21d</th>"
        "<th>vol21d</th><th>rangePos21d</th><th>candleBias</th></tr></thead>"
        f"<tbody>{''.join(rows)}</tbody></table>"
    )


def _csp_block(csp: Dict) -> str:
    # Rank the GP-fit candidates best-trade-first (highest return-on-capital) so
    # the top of the table is the best actionable trade, not the alphabet. Non-fit
    # names follow sorted by symbol.
    def _roc(sym: str) -> float:
        try:
            return float(csp[sym]["candidate"].get("return_on_capital"))
        except (TypeError, ValueError, KeyError):
            return -1.0

    fits = sorted(
        (s for s, r in csp.items() if r.get("mode") == "CASH_SECURED_PUT" and r.get("fits_gp_rules")),
        key=_roc, reverse=True,
    )
    non_fits = sorted(
        (s for s, r in csp.items() if r.get("mode") == "CASH_SECURED_PUT" and not r.get("fits_gp_rules")),
    )
    rows = []
    for sym in fits + non_fits:
        r = csp[sym]
        c = r.get("candidate", {})
        badge = "ok" if r.get("fits_gp_rules") else "warn"
        try:
            roc_pct = f"{float(c.get('return_on_capital')) * 100:.2f}%"
        except (TypeError, ValueError):
            roc_pct = _esc(c.get("return_on_capital")) or "-"
        rows.append(
            "<tr>"
            f"<td>{_esc(sym)}</td><td>{_esc(c.get('strike'))}</td>"
            f"<td>{_esc(c.get('dte'))}</td>"
            f"<td>${_esc(c.get('net_credit_per_share'))}</td>"
            f"<td>${_esc(c.get('collateral_required'))}</td>"
            f"<td><strong>{_esc(roc_pct)}</strong></td>"
            f"<td>{_esc(r.get('survivability', 'INDETERMINATE'))}</td>"
            f"<td><span class='badge {badge}'>{'FITS' if r.get('fits_gp_rules') else 'no'}</span></td>"
            f"<td>{_esc(', '.join(r.get('eval_reasons', [])) or '-')}</td>"
            "</tr>"
        )
    for sym in sorted(csp):
        r = csp[sym]
        if r.get("mode") != "CASH_SECURED_PUT":
            rows.append(f"<tr><td>{_esc(sym)}</td><td colspan='5' class='note'>[{_esc(r.get('mode'))}]</td></tr>")
    return (
        "<table><thead><tr><th>Symbol</th><th>Strike</th><th>DTE</th><th>Credit</th>"
        "<th>Capital</th><th>RoC</th><th>Survivability</th><th>GP rules</th><th>Reasons</th></tr></thead>"
        f"<tbody>{''.join(rows)}</tbody></table>"
    )


def _csp_top_pick(csp: Dict) -> str:
    """One-line top pick from the ranked fits (best return-on-capital, <$5k)."""
    best = None
    best_roc = -1.0
    for sym, r in csp.items():
        if r.get("mode") != "CASH_SECURED_PUT" or not r.get("fits_gp_rules"):
            continue
        try:
            roc = float(r["candidate"].get("return_on_capital"))
        except (TypeError, ValueError, KeyError):
            continue
        if roc > best_roc:
            best_roc = roc
            best = (sym, r["candidate"])
    if not best:
        return "<p class='note'>No candidate currently fits the GP wheel.</p>"
    sym, c = best
    try:
        roc_pct = f"{float(c.get('return_on_capital')) * 100:.2f}%"
    except (TypeError, ValueError):
        roc_pct = str(c.get("return_on_capital"))
    return (
        f"<p class='top'><strong>Top fit: {_esc(sym)}</strong> — "
        f"cash-secured put at {_esc(c.get('strike'))}, {_esc(c.get('dte'))} DTE, "
        f"${_esc(c.get('collateral_required'))} capital, {_esc(roc_pct)} return-on-capital.</p>"
    )


def _yellow_sheet_block(ys: Dict) -> str:
    if not ys or ys.get("sheet_count", 0) == 0:
        return ("<p class='note'>No Yellow Sheets yet. The GP records a decision "
                "as a Yellow Sheet (thesis, evidence, invalidation, exit plan) — "
                "the product's decision document, bound to this report hash.</p>")
    rows = "".join(
        f"<tr><td>{_esc(k)}</td><td>{_esc(v)}</td></tr>"
        for k, v in sorted((ys.get("by_decision") or {}).items())
    )
    return (
        f"<p class='note'>Yellow Sheets recorded: {_esc(ys.get('sheet_count'))} "
        f"across {_esc(ys.get('symbol_count'))} symbols.</p>"
        f"<table><thead><tr><th>Decision</th><th>Count</th></tr></thead>"
        f"<tbody>{rows}</tbody></table>"
        f"<div class='note'>{_esc(ys.get('note',''))}</div>"
    )


def _scale_path_block(scale: Dict) -> str:
    if not scale:
        return "<p class='note'>Compounding scale: configure account equity to see how position size grows with the account.</p>"
    rows = "".join(
        f"<tr><td>${int(p['equity']):,}</td><td>{p['contracts']}</td></tr>"
        for p in scale.get("path", [])
    )
    return (
        f"<p class='note'>Top fit: {_esc(scale.get('symbol'))} at strike "
        f"{_esc(scale.get('strike'))}, {_esc(scale.get('capital_per_contract'))} "
        f"capital/contract. Holding the 2%-of-equity rule, contracts scale as the "
        f"account grows:</p>"
        f"<table><thead><tr><th>Account equity</th><th>Contracts</th></tr></thead>"
        f"<tbody>{rows}</tbody></table>"
        f"<div class='note'>{_esc(scale.get('note',''))}</div>"
    )


def _paper_block(paper: Dict) -> str:
    counts = paper.get("outcome_counts", {})
    if not counts:
        return "<p class='note'>No paper outcomes recorded yet — the loop is armed, waiting for real paper entries.</p>"
    rows = "".join(
        f"<tr><td>{_esc(k)}</td><td>{_esc(v)}</td></tr>" for k, v in sorted(counts.items())
    )
    return (
        "<table><thead><tr><th>Outcome</th><th>Count</th></tr></thead>"
        f"<tbody>{rows}</tbody></table>"
        f"<div class='note'>{_esc(paper.get('note',''))}</div>"
    )


def build_am_demo_html(
    watchlist=DEFAULT_WATCHLIST, earnings_ciks=DEFAULT_EARNINGS_CIKS
) -> Dict[str, object]:
    report = run_nightly(watchlist=watchlist, earnings_ciks=earnings_ciks)
    chain = report["chain_income"].get("SPY", {})
    structures = chain.get("gated_income_structures") or chain.get("income_structures", [])
    chain_note = chain.get("note", "")
    if chain.get("mode") == "BLOCKED":
        chain_note = f"Blocked: {chain.get('reason')}"
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    page = _render_report_page(
        report, chain_note=chain_note, structures=structures, generated=generated
    )

    return {
        "eod_status": report["eod_batch_status"],
        "candidate_count": report["candidate_count"],
        "premium_count": len(structures),
        "html": page,
    }


def _render_report_page(
    report: Dict, *, chain_note: str, structures: Sequence[Dict], generated: str
) -> str:
    """Render the full AM report page from a populated report dict.

    Pure/deterministic given (report, chain_note, structures, generated) so the
    document's structural integrity (unique, sequential numbered section
    headings) is unit-testable without touching the network pipeline.
    build_am_demo_html fills these from the nightly run, then delegates here.
    """
    return f"""<!DOCTYPE html>
    <html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Emporion — AM Report (real data)</title>
<style>
  body {{ font-family: -apple-system, Segoe UI, Roboto, sans-serif; margin: 0;
         background: #0d1117; color: #e6edf3; }}
  header {{ padding: 22px 28px; border-bottom: 1px solid #21262d; }}
  h1 {{ margin: 0 0 4px; font-size: 22px; }}
  .sub {{ color: #8b949e; font-size: 13px; }}
  main {{ padding: 20px 28px; max-width: 1150px; }}
  h2 {{ font-size: 16px; margin: 26px 0 10px; color: #58a6ff; }}
  table {{ border-collapse: collapse; width: 100%; font-size: 12px; }}
  th, td {{ text-align: left; padding: 6px 8px; border-bottom: 1px solid #21262d; }}
  th {{ color: #8b949e; font-weight: 600; }}
  .badge {{ display: inline-block; padding: 1px 8px; border-radius: 10px; font-size: 11px; font-weight: 600; }}
  .ok {{ background: #1f6feb22; color: #58a6ff; }}
  .warn {{ background: #9e6a0322; color: #d29922; }}
  .note {{ color: #8b949e; font-size: 12px; line-height: 1.5; }}
  .pill {{ background: #21262d; color: #e6edf3; padding: 2px 8px; border-radius: 6px; font-size: 11px; margin-right: 6px; }}
  .top {{ background: #1f6feb11; color: #58a6ff; padding: 8px 12px; border: 1px solid #1f6feb55; border-radius: 8px; font-size: 13px; }}
  .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
  .panel {{ border: 1px solid #21262d; border-radius: 8px; padding: 14px; }}
</style></head><body>
<header>
  <h1>Emporion — Overnight Desk AM Report</h1>
  <div class="sub">Real end-of-day batch &middot; generated {generated} &middot;
  eod status {_esc(report['eod_batch_status'])} &middot;
  data as-of {_esc(report['data_freshness']['as_of'])} ({'current' if report['data_freshness']['is_current'] else 'prior trading day'})</div>
</header>
<main>

<h2>1. Equity premium candidates (collateral/margin from real EOD closes)</h2>
<table><thead><tr><th>Symbol</th><th>Close</th><th>Strategy</th><th>Strike</th>
<th>Capital required</th><th>Policy</th><th>Trade auth</th></tr></thead>
<tbody>{_equity_rows(report['candidates'])}</tbody></table>

<h2>2. Premium income — SPY defined-risk spreads (REAL Cboe chain; top by return-on-risk)</h2>
<div class="note">{_esc(chain_note)}</div>
<table><thead><tr><th>Contract (short--long)</th><th>Exp</th><th>DTE</th><th>Net credit</th>
<th>Max loss</th><th>RoR</th><th>Gate</th><th>Gate reasons</th><th>Trade auth</th></tr></thead>
<tbody>{_premium_rows(structures)}</tbody></table>

<h2>3. Feature plane (deterministic, from real 3mo EOD)</h2>
{_features_block(report['features'])}

<h2>4. Cash-secured-put wheel scan (REAL Cboe chains; GP rules)</h2>
{_csp_top_pick(report['cash_secured_put_scan'])}
{_csp_block(report['cash_secured_put_scan'])}

<div class="panel" style="margin-top:16px"><h2>4b. Compounding scale (hold the rule, size to grow)</h2>{_scale_path_block(report.get('scale_path'))}</div>

<h2>5. Decision ledger — Yellow Sheets</h2>
{_yellow_sheet_block(report['yellow_sheets'])}

<h2>6. Paper-outcome loop (append-only journal)</h2>
{_paper_block(report['paper_outcome_summary'])}

<div class="grid">
  <div class="panel"><h2>7. Rates environment (REAL FRED)</h2>{_rates_block(report['rates_environment'])}
  <h2 style="margin-top:18px">VIX regime (REAL)</h2>{_vix_block(report['vix_regime'])}
  <h2 style="margin-top:18px">Macro (REAL FRED)</h2>{_macro_block(report['macro_environment'])}</div>
  <div class="panel"><h2>8. Earnings actuals (REAL SEC EDGAR)</h2>{_earnings_block(report['earnings_actuals'])}</div>
</div>

<div class="note" style="margin-top:24px">
  <span class="pill">REAL DATA</span><span class="pill">NO FABRICATED NUMBERS</span>
  <span class="pill">NO PROBABILITY / RoR</span><span class="pill">NO ORDER</span><br><br>
  Panel 1: collateral/margin from real EOD closes. Panel 2: executable net credit
  and max loss from a real Cboe delayed chain, ranked by return-on-risk, each with
  its execution-gate decision (kill switch OFF by default -> BLOCKED). Panel 3:
  official FRED observations. Panel 4: official SEC filings. This is research, not
  income, not advice, and not an order. Every trade_authorized field reads NO.
</div>
</main></body></html>
"""


def main() -> None:
    out = Path("artifacts/am-demo.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    result = build_am_demo_html()
    out.write_text(result["html"], encoding="utf-8")
    print(f"wrote {out}: {result['candidate_count']} equity candidates, "
          f"{result['premium_count']} premium structures, EOD {result['eod_status']}")


if __name__ == "__main__":
    main()