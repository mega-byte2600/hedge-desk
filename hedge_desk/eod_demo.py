"""First true-MVP demo: real EOD batch -> premium-desk AM candidate page.

Runs the real EOD ingest for a watchlist, builds the premium-desk candidate
economics, and renders a clean, self-contained HTML page. This is the "first
demo" of the re-scope: real data, overnight-style batch, AM candidate list.

Honesty: the page labels every number as collateral/margin requirement computed
from real EOD closes, states that no option prices/probability/RoR are
fabricated, and that no order is placed. It is a research candidate list, not a
promise of income.
"""

from __future__ import annotations

import html
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict

from hedge_desk.data.eod_ingest import ingest_eod
from hedge_desk.premium_candidates import build_premium_candidates

DEFAULT_WATCHLIST = ("SPY", "QQQ", "AAPL", "MSFT", "NVDA", "TSLA")


def _render_row(c: Dict[str, object]) -> str:
    return (
        "<tr>"
        f"<td>{html.escape(str(c['symbol']))}</td>"
        f"<td>{html.escape(str(c['close']))}</td>"
        f"<td>{html.escape(str(c['strategy']))}</td>"
        f"<td>{html.escape(str(c['strike']))}</td>"
        f"<td>${html.escape(str(c['requirement']))}</td>"
        f"<td>{html.escape(str(c['policy_version']))}</td>"
        "<td>NO</td>"
        "</tr>"
    )


def build_demo_html(watchlist=DEFAULT_WATCHLIST) -> Dict[str, object]:
    cutoff = datetime.now(timezone.utc)
    eod = ingest_eod(watchlist, cutoff)
    candidates = build_premium_candidates(eod)
    rows = "".join(_render_row(c) for c in candidates["candidates"])
    eod_status = eod["batch_status"]
    eod_rows = "".join(
        f"<tr><td>{html.escape(str(s['symbol']))}</td>"
        f"<td>{html.escape(str(s['status']))}</td>"
        f"<td>{html.escape(str(s['last_day']))}</td>"
        f"<td>{html.escape(str(s['last_day_close']))}</td></tr>"
        for s in eod["source_results"]
    )
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    page = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Emporion — Overnight Premium Desk (real EOD)</title>
<style>
  body {{ font-family: -apple-system, Segoe UI, Roboto, sans-serif; margin: 0;
         background: #0d1117; color: #e6edf3; }}
  header {{ padding: 24px 32px; border-bottom: 1px solid #21262d; }}
  h1 {{ margin: 0 0 4px; font-size: 22px; }}
  .sub {{ color: #8b949e; font-size: 13px; }}
  main {{ padding: 24px 32px; max-width: 1000px; }}
  h2 {{ font-size: 16px; margin: 28px 0 10px; color: #58a6ff; }}
  table {{ border-collapse: collapse; width: 100%; font-size: 13px; }}
  th, td {{ text-align: left; padding: 8px 10px; border-bottom: 1px solid #21262d; }}
  th {{ color: #8b949e; font-weight: 600; }}
  .badge {{ display: inline-block; padding: 2px 10px; border-radius: 12px;
            font-size: 12px; font-weight: 600; }}
  .ok {{ background: #1f6feb22; color: #58a6ff; }}
  .warn {{ background: #9e6a0322; color: #d29922; }}
  .note {{ color: #8b949e; font-size: 12px; margin-top: 20px; line-height: 1.5; }}
  .pill {{ background: #21262d; color: #e6edf3; padding: 2px 8px; border-radius: 6px;
           font-size: 12px; margin-right: 6px; }}
</style></head><body>
<header>
  <h1>Emporion — Overnight Premium Desk</h1>
  <div class="sub">Real end-of-day batch &middot; generated {generated}</div>
</header>
<main>
  <h2>EOD batch intake <span class="badge {'ok' if eod_status=='READY_FOR_RESEARCH' else 'warn'}">{html.escape(eod_status)}</span></h2>
  <table><thead><tr><th>Symbol</th><th>Status</th><th>Last day</th><th>Close</th></tr></thead>
  <tbody>{eod_rows}</tbody></table>

  <h2>Premium-desk candidates (defined-risk, collateral/margin requirement)</h2>
  <table><thead><tr><th>Symbol</th><th>Close</th><th>Strategy</th><th>Strike</th>
  <th>Capital required</th><th>Policy</th><th>Trade authorized</th></tr></thead>
  <tbody>{rows}</tbody></table>

  <div class="note">
    <span class="pill">REAL EOD</span><span class="pill">NO FABRICATED PRICES</span>
    <span class="pill">NO PROBABILITY / RoR</span><span class="pill">NO ORDER</span><br><br>
    Capital required is the collateral/margin for each defined-risk structure,
    computed from real end-of-day closes via the versioned margin policy. Premium
    income is only knowable from a real option chain (BYO-data path) and is not
    shown here. This is a research candidate list, not a promise of income and not
    an order. Every candidate is trade_authorized = NO.
  </div>
</main></body></html>
"""
    return {
        "eod_status": eod_status,
        "candidate_count": candidates["candidate_count"],
        "symbol_count": candidates["symbol_count"],
        "html": page,
    }


def main() -> None:
    out = Path("artifacts/eod-demo.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    result = build_demo_html()
    out.write_text(result["html"], encoding="utf-8")
    print(f"wrote {out} ({result['candidate_count']} candidates, "
          f"{result['symbol_count']} symbols, EOD {result['eod_status']})")


if __name__ == "__main__":
    main()