"""Pre-market morning briefing — ready before the 9:00am EST open.

A Wall-Street-style morning briefing built from the real overnight report
(am-report-latest.json): what the desk is watching, the candidates ready for the
open, the macro backdrop, and the risk context. Generated pre-open (8am) so the
GP opens the desk at 9am with a fresh briefing, not Friday's close re-stamped.

Real data only. No fabricated numbers, no probability/RoR claims, no trade
authorization. Research output, not a signal.
"""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts" / "am-report-latest.json"
OUT = ROOT / "artifacts" / "morning-briefing.md"


def _fmt(v, nd=2):
    try:
        return f"{float(v):,.{nd}f}"
    except (TypeError, ValueError):
        return str(v)


def build() -> str:
    if not REPORT.exists():
        raise SystemExit("no report; run the nightly batch first")
    r = json.loads(REPORT.read_text())
    now = datetime.now(timezone.utc)
    lines = []
    lines.append("# Emporion — Morning Briefing")
    lines.append(f"Prepared {now.strftime('%A %Y-%m-%d %H:%M UTC')} · ready for the 9:00am EST open")
    lines.append("")
    lines.append(f"**Mode:** {r.get('mode')} · **EOD batch:** {r.get('eod_batch_status')} · "
                 f"**Report:** {r.get('generated_at')}")
    lines.append("")

    # 1. The candidates ready for the open
    cands = r.get("candidates", [])
    lines.append("## What's on the desk for the open")
    lines.append(f"{len(cands)} real candidates across {r.get('symbol_count', 0)} symbols "
                 f"({', '.join(r.get('watchlist', []))}).")
    lines.append("")
    lines.append("| Symbol | Strategy | Collateral |")
    lines.append("|---|---|---|")
    for c in cands[:12]:
        lines.append(f"| {c['symbol']} | {c['strategy']} | ${_fmt(c['requirement'])} |")
    lines.append("")

    # 2. Cash-secured put wheel (the GP's product)
    csp = r.get("cash_secured_put_scan", {})
    fits = [(s, v) for s, v in csp.items() if v.get("mode") == "CASH_SECURED_PUT"]
    if fits:
        lines.append("## Cash-secured put wheel (real Cboe)")
        lines.append("| Symbol | Strike | DTE | Return on collateral | Fits GP rules |")
        lines.append("|---|---|---|---|---|")
        for s, v in fits:
            c = v["candidate"]
            lines.append(f"| {s} | {c['strike']} | {c['dte']} | {_fmt(float(c['return_on_capital'])*100,1)}% | "
                         f"{'yes' if v.get('fits_gp_rules') else 'no'} |")
        lines.append("")

    # 3. Macro backdrop
    lines.append("## Macro backdrop (real)")
    vix = r.get("vix_regime", {})
    if vix.get("mode") == "REAL_VIX":
        lines.append(f"- VIX: {_fmt(vix.get('last_close'))} ({vix.get('regime')})")
    rates = r.get("rates_environment", {})
    if rates.get("mode") == "REAL_FRED_RATES":
        lines.append(f"- Fed funds: {rates.get('fed_funds_effective_rate')}%")
    oil = r.get("oil_market", {})
    if oil.get("mode") == "REAL_YAHOO_WTI":
        lines.append(f"- WTI oil: ${_fmt(oil.get('last_close'))}")
    macro = r.get("macro_environment", {})
    if macro.get("mode") == "REAL_FRED_MACRO" and macro.get("cpi_yoy_pct"):
        lines.append(f"- CPI YoY: {macro['cpi_yoy_pct']}%")
    elif macro.get("mode") == "BLOCKED":
        lines.append(f"- Macro: BLOCKED ({macro.get('reason', 'pending FRED refetch')})")
    lines.append("")

    # 4. Risk context
    lines.append("## Risk context")
    lines.append(f"- Account equity configured: {r.get('account_equity_configured')}")
    wf = r.get("wheel_fit", {})
    if wf.get("max_position_collateral"):
        lines.append(f"- 2%-of-equity max position collateral: ${_fmt(wf['max_position_collateral'])}")
    lines.append(f"- Live orders: {r.get('live_orders_enabled', False)} (paper-only)")
    lines.append("")
    lines.append("---")
    lines.append("Research output, not a trade signal. No probability or Risk-of-Ruin claims. "
                 "No order placed; every candidate trade_authorized=False.")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    OUT.write_text(build())
    print(f"wrote {OUT}")
