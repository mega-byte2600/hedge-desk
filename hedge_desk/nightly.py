"""Nightly orchestrator: run the real EOD batch and write the AM candidate report.

Increment 5 of the true-MVP re-scope. This is the "process at night" piece: a
single idempotent entry point that pulls the real EOD batch for a watchlist,
builds the premium-desk candidate economics, and writes a dated, content-addressed
AM report to ``artifacts/``. A scheduler (cron / launchd) calls this after market
close; the GP opens the report before the open.

Honesty and safety:
- No secrets, tokens, or PII are read, written, or logged. The only inputs are
  public symbols and configured server-side market-data credentials.
- No order is placed and no trade is authorized (every candidate is
  trade_authorized=False).
- The report is content-addressed (sha256) so a later reader can verify it was
  not tampered with, and it is written atomically (temp file + rename).
- Fail closed: a transport or parse failure for a symbol/source is surfaced in
  the report; the run never substitutes fabricated market data.
"""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Sequence

from hedge_desk.data.eod_ingest import EodDay, FEATURE_YAHOO_RANGE, ingest_eod
from hedge_desk.features import build_feature_bundle_from_days
from hedge_desk.csp_scan import scan_cash_secured_put
from hedge_desk.paper_log import summarize as summarize_paper_log
from hedge_desk.yellow_sheet import summarize_yellow_sheets
from hedge_desk.premium_candidates import build_premium_candidates
from hedge_desk.cboe_chain import real_chain_income
from hedge_desk.rates_desk import rates_environment
from hedge_desk.vix_regime import vix_regime, apply_vix_regime_filter
from hedge_desk.macro_desk import macro_environment
from hedge_desk.market_context import build_market_context
from hedge_desk.freshness import freshness_summary
from hedge_desk.data_quality import quality_report
from hedge_desk.account import read_account_equity
from hedge_desk.position_sizing import wheel_fit_for_equity, scale_position_to_equity
from hedge_desk.oil_desk import oil_market
from hedge_desk.earnings_desk import earnings_desk
from hedge_desk.execution_gate import (
    KillSwitch,
    build_candidate_from_structure,
    evaluate_execution,
)
from hedge_desk.domain import Account, AccountType
from decimal import Decimal

NIGHTLY_VERSION = "hedge-desk-nightly-2.2.0"
DEFAULT_WATCHLIST = ("NKE", "CCL", "AAL", "LYFT", "NCLH", "F", "DVN")


def _watchlist() -> Sequence[str]:
    raw = os.environ.get("EOD_WATCHLIST", "")
    if raw.strip():
        return tuple(s.strip().upper() for s in raw.split(",") if s.strip())
    return DEFAULT_WATCHLIST


def _annotate_chain_with_gates(
    chain: Dict[str, object],
    demo_account_equity: str = "100000",
    kill_switch_armed: bool = False,
) -> Dict[str, object]:
    """Annotate each presented premium structure with its risk+release gate decision."""
    from datetime import datetime as _dt

    acct = Account(
        "demo-account", AccountType.INDIVIDUAL,
        Decimal(demo_account_equity), Decimal(demo_account_equity) / Decimal("2"),
        options_approved=True,
    )
    structures = chain.get("income_structures", [])
    gated = []
    now = _dt.now(timezone.utc)
    for s in structures:
        gate_reasons = []
        try:
            cand = build_candidate_from_structure(s, quote_timestamp=now)
        except (ValueError, TypeError):
            gate_reasons.append("MISSING_REAL_RISK_INPUT")
            gated.append(
                {**s, "gate_decision": "INDETERMINATE",
                 "gate_reasons": gate_reasons,
                 "kill_switch_armed": kill_switch_armed}
            )
            continue
        decision = evaluate_execution(
            candidate=cand,
            account=acct,
            evaluated_at=now,
            validated_risk_of_ruin_after=None,
            kill_switch=KillSwitch(armed=kill_switch_armed),
        )
        gated.append({**s, "gate_decision": decision.decision,
                      "gate_reasons": list(decision.reason_codes),
                      "kill_switch_armed": decision.kill_switch_armed})
    out = dict(chain)
    out["gated_income_structures"] = gated
    out["gate_demo_account_equity"] = demo_account_equity
    out["gate_risk_input_advanced"] = False
    out["gate_note"] = (
        "No validated Risk-of-Ruin artifact and no real account/liquidity are "
        "wired yet, so gate decisions are INDETERMINATE (missing inputs), never a "
        "fabricated approval. gate_demo_account_equity is a DEMO default, NOT the "
        "GP's real balance. No order is placed and nothing is trade_authorized."
    )
    out["gate_kill_switch_armed"] = kill_switch_armed
    return out


def run_nightly(
    watchlist: Sequence[str] | None = None,
    artifacts_dir: Path | str = "artifacts",
    transport=None,
    chain_symbols: Sequence[str] = ("SPY",),
    chain_transport=None,
    csp_transport=None,
    rates_transport=None,
    vix_transport=None,
    macro_transport=None,
    oil_transport=None,
    earnings_ciks: Sequence[str] = (),
    earnings_transport=None,
    paper_log_path: Path | str = "artifacts/paper-outcomes.jsonl",
    yellow_sheet_path: Path | str = "artifacts/yellow-sheets.jsonl",
) -> Dict[str, object]:
    """Run EOD candidates plus real option, macro and authoritative API context.

    Independent providers fail closed. A failed provider is represented as
    BLOCKED/UNCONFIGURED in the report and never replaced by invented values.
    """
    symbols = tuple(watchlist) if watchlist else _watchlist()
    if not symbols:
        raise ValueError("nightly watchlist cannot be empty")
    cutoff = datetime.now(timezone.utc)
    account_equity = read_account_equity()

    eod = (ingest_eod(symbols, cutoff, transport=transport, range_param=FEATURE_YAHOO_RANGE)
    if transport else ingest_eod(symbols, cutoff, range_param=FEATURE_YAHOO_RANGE))
    candidates = build_premium_candidates(eod)

    last_bar_dates = [
        str(row["last_day"]) for row in eod.get("source_results", [])
        if isinstance(row, dict) and row.get("status") == "PASS" and row.get("last_day")
    ]
    freshness = freshness_summary(last_bar_dates, cutoff.date())

    days_by_symbol = {}
    for row in eod.get("source_results", []):
        if isinstance(row, dict) and row.get("status") == "PASS" and row.get("days"):
            days_by_symbol[str(row["symbol"])] = [
                EodDay(d["date"], d["close"], d["open"], d["high"], d["low"], d["volume"])
                for d in row["days"]
            ]
    features = build_feature_bundle_from_days(days_by_symbol)

    from concurrent.futures import ThreadPoolExecutor, as_completed

    def _safe(fn, *args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as exc:
            return {"mode": "BLOCKED", "reason": str(exc)}

    csp_results: dict = {}
    chain_results: dict = {}
    rates: dict = {}
    vix: dict = {}
    macro: dict = {}
    oil: dict = {}
    earnings_results: dict = {}
    market_context: dict = {}

    with ThreadPoolExecutor(max_workers=9) as ex:
        futures = {}
        for cs in symbols:
            if csp_transport:
                futures[ex.submit(_safe, scan_cash_secured_put, cs, cutoff,
                                  csp_transport, account_equity)] = ("csp", cs)
            else:
                futures[ex.submit(_safe, scan_cash_secured_put, cs, cutoff,
                                  account_equity=account_equity)] = ("csp", cs)
        for cs in chain_symbols:
            cs = str(cs).upper()
            if chain_transport:
                futures[ex.submit(_safe, real_chain_income, cs, cutoff,
                                  chain_transport)] = ("chain", cs)
            else:
                futures[ex.submit(_safe, real_chain_income, cs, cutoff)] = ("chain", cs)
        if rates_transport:
            futures[ex.submit(_safe, rates_environment, transport=rates_transport)] = ("rates", None)
        else:
            futures[ex.submit(_safe, rates_environment)] = ("rates", None)
        if vix_transport:
            futures[ex.submit(_safe, vix_regime, cutoff, vix_transport)] = ("vix", None)
        else:
            futures[ex.submit(_safe, vix_regime, cutoff)] = ("vix", None)
        if macro_transport:
            futures[ex.submit(_safe, macro_environment, macro_transport)] = ("macro", None)
        else:
            futures[ex.submit(_safe, macro_environment)] = ("macro", None)
        if oil_transport:
            futures[ex.submit(_safe, oil_market, transport=oil_transport)] = ("oil", None)
        else:
            futures[ex.submit(_safe, oil_market)] = ("oil", None)
        futures[ex.submit(_safe, build_market_context)] = ("market_context", None)
        for cik in earnings_ciks:
            if earnings_transport:
                futures[ex.submit(_safe, earnings_desk, cik, earnings_transport)] = ("earnings", cik)
            else:
                futures[ex.submit(_safe, earnings_desk, cik)] = ("earnings", cik)

        for fut in as_completed(futures):
            kind, key = futures[fut]
            res = fut.result()
            if kind == "csp":
                csp_results[key] = res
            elif kind == "chain":
                chain_results[key] = _annotate_chain_with_gates(res)
            elif kind == "rates":
                rates = res
            elif kind == "vix":
                vix = res
            elif kind == "macro":
                macro = res
            elif kind == "oil":
                oil = res
            elif kind == "earnings":
                earnings_results[key] = res
            elif kind == "market_context":
                market_context = res

    csp_results = apply_vix_regime_filter(vix, csp_results)

    scale_path = None
    top_fit = None
    best_roc = -1.0
    for sym, r in csp_results.items():
        if r.get("mode") == "CASH_SECURED_PUT" and r.get("fits_gp_rules"):
            c = r.get("candidate", {})
            try:
                roc = float(c.get("return_on_capital"))
            except (TypeError, ValueError):
                roc = -1.0
            if roc > best_roc:
                best_roc = roc
                top_fit = (sym, c)
    if top_fit is not None:
        sym, c = top_fit
        capital = c.get("collateral_required") or c.get("max_loss")
        scale_path = {
            "symbol": sym,
            "strike": c.get("strike"),
            "capital_per_contract": capital,
            "path": [
                {"equity": str(eq), "contracts": scale_position_to_equity(
                    capital, capital, str(eq))["max_contracts"]}
                for eq in (100000, 250000, 500000, 1000000)
            ],
            "note": ("Conditional on real account equity; holds the 2%-of-equity "
                     "max-loss rule. Sizing design, not a performance projection."),
        }

    def _downsample(points, limit=63):
        if len(points) <= limit:
            return list(points)
        step = len(points) / limit
        idxs = sorted({min(int(i * step), len(points) - 1) for i in range(limit)})
        return [points[i] for i in idxs]

    series = {
        "as_of": cutoff.date().isoformat(),
        "symbols": {
            sym: _downsample([[d.date, str(d.close)] for d in days])
            for sym, days in sorted(days_by_symbol.items())
            if days
        },
        "vix": (vix.get("history") if isinstance(vix, dict) else None),
        "treasury_10y": (rates.get("treasury_10y_history") if isinstance(rates, dict) else None),
        "treasury_2y": (rates.get("treasury_2y_history") if isinstance(rates, dict) else None),
        "wti": (oil.get("window_closes") if isinstance(oil, dict) else None),
    }

    report = {
        "schema_version": NIGHTLY_VERSION,
        "mode": "REAL_EOD_NIGHTLY",
        "generated_at": cutoff.isoformat(),
        "watchlist": list(symbols),
        "eod_batch_status": eod["batch_status"],
        "eod_manifest_sha256": eod["batch_manifest_sha256"],
        "data_freshness": freshness,
        "candidate_count": candidates["candidate_count"],
        "symbol_count": candidates["symbol_count"],
        "candidates": candidates["candidates"],
        "series": series,
        "eod_source_results": eod["source_results"],
        "chain_income": chain_results,
        "features": features,
        "cash_secured_put_scan": csp_results,
        "account_equity_configured": account_equity is not None,
        "scale_path": scale_path,
        "wheel_fit": (
            wheel_fit_for_equity(str(account_equity))
            if account_equity is not None
            else {"max_position_collateral": None,
                  "explanation": "Account equity not configured; survivability is INDETERMINATE."}
        ),
        "paper_outcome_summary": summarize_paper_log(paper_log_path),
        "yellow_sheets": summarize_yellow_sheets(yellow_sheet_path),
        "rates_environment": rates,
        "vix_regime": vix,
        "macro_environment": macro,
        "oil_market": oil,
        "earnings_actuals": earnings_results,
        "market_context": market_context,
        "note": (
            "Equity candidates use real EOD closes; options use real delayed Cboe "
            "chains. Nasdaq's public API supplies real-time watchlist quotes and the "
            "earnings calendar. WTI market price context remains sourced from the "
            "existing oil desk, while EIA supplies official energy fundamentals "
            "when its key is configured. Rates/macro retain FRED with "
            "authoritative cross-checks from the New York Fed and the U.S. Treasury "
            "par yield curve via FRED DGS. ECB supplies euro reference FX. "
            "CFTC supplies futures positioning and FINRA supplies public fixed-income "
            "breadth when credentials are configured. Yahoo Finance and SEC EDGAR "
            "are currently unreachable from this network and are reported BLOCKED, "
            "never backfilled. No provider failure is replaced "
            "with fabricated data. No order placed; trade_authorized=False."
        ),
    }
    report["data_quality"] = quality_report(report)
    body = {
        k: v
        for k, v in report.items()
        if k not in ("report_sha256", "report_path", "latest_path")
    }
    report["report_sha256"] = hashlib.sha256(
        json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()

    root = Path(artifacts_dir)
    root.mkdir(parents=True, exist_ok=True)
    date_stamp = cutoff.date().isoformat()
    final_path = root / f"am-report-{date_stamp}.json"
    tmp_path = root / f".am-report-{date_stamp}.tmp"
    tmp_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp_path, final_path)
    latest_path = root / "am-report-latest.json"
    latest_tmp = root / ".am-report-latest.tmp"
    latest_tmp.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    os.replace(latest_tmp, latest_path)
    report["report_path"] = str(final_path)
    report["latest_path"] = str(latest_path)
    return report


__all__ = ["NIGHTLY_VERSION", "DEFAULT_WATCHLIST", "run_nightly"]
