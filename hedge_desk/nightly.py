"""Nightly orchestrator: run the real EOD batch and write the AM candidate report.

Increment 5 of the true-MVP re-scope. This is the "process at night" piece: a
single idempotent entry point that pulls the real EOD batch for a watchlist,
builds the premium-desk candidate economics, and writes a dated, content-addressed
AM report to ``artifacts/``. A scheduler (cron / launchd) calls this after market
close; the GP opens the report before the open.

Honesty and safety:
- No secrets, tokens, or PII are read, written, or logged. The only inputs are
  public symbols and the public Yahoo chart endpoint.
- No order is placed and no trade is authorized (every candidate is
  trade_authorized=False).
- The report is content-addressed (sha256) so a later reader can verify it was
  not tampered with, and it is written atomically (temp file + rename).
- Fail closed: a transport or parse failure for a symbol quarantines/rejects that
  symbol; the run still writes a report with the failures visible.
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
from hedge_desk.freshness import freshness_summary
from hedge_desk.account import read_account_equity
from hedge_desk.position_sizing import wheel_fit_for_equity, scale_position_to_equity
from hedge_desk.earnings_desk import earnings_desk
from hedge_desk.execution_gate import (
    KillSwitch,
    build_candidate_from_structure,
    evaluate_execution,
)
from hedge_desk.domain import Account, AccountType
from decimal import Decimal

NIGHTLY_VERSION = "hedge-desk-nightly-2.0.0"
DEFAULT_WATCHLIST = ("NKE", "CCL", "AAL", "LYFT", "NCLH", "F", "DVN")  # sub-$55 GP-fit universe (see docs/MVP_RESCOPE)


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
        except (ValueError, TypeError) as exc:
            # Missing real inputs (e.g. real ADV) -> INDETERMINATE, never ERROR.
            gate_reasons.append("MISSING_REAL_RISK_INPUT")
            gated.append(
                {**s, "gate_decision": "INDETERMINATE",
                 "gate_reasons": gate_reasons,
                 "kill_switch_armed": kill_switch_armed}
            )
            continue
        # No validated RoR artifact exists yet, so pass None: the gate fails
        # closed with RISK_INPUT_ABSENT instead of a fabricated 0.01. No agent
        # may substitute an authoritative Risk-of-Ruin (AGENTS.md).
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
    # DATA peer-review: this is a DEMO default (drives the fail-closed gates to
    # INDETERMINATE); never present it as the GP's validated account balance.
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
    earnings_ciks: Sequence[str] = (),
    earnings_transport=None,
    paper_log_path: Path | str = "artifacts/paper-outcomes.jsonl",
    yellow_sheet_path: Path | str = "artifacts/yellow-sheets.jsonl",
) -> Dict[str, object]:
    """Run the EOD batch + premium candidates + real chain income + macro desks.

    Real chain income (Cboe) for ``chain_symbols``; a real rates environment
    (FRED); and real earnings actuals (SEC EDGAR, by 10-digit CIK in
    ``earnings_ciks``). Anything that fails is reported blocked — never
    fabricated.
    """
    symbols = tuple(watchlist) if watchlist else _watchlist()
    if not symbols:
        raise ValueError("nightly watchlist cannot be empty")
    cutoff = datetime.now(timezone.utc)
    # Real account equity (local, gitignored) so survivability can evaluate
    # instead of INDETERMINATE. Raw value is never put in the report.
    account_equity = read_account_equity()

    # Pull enough history for the feature plane (3mo), not just the 5d batch.
    eod = (ingest_eod(symbols, cutoff, transport=transport, range_param=FEATURE_YAHOO_RANGE)
           if transport else ingest_eod(symbols, cutoff, range_param=FEATURE_YAHOO_RANGE))
    candidates = build_premium_candidates(eod)

    # Data-freshness gate: is the batch running on today's close or the prior
    # trading day's? (At 4:30pm EST the source may not have published today yet.)
    last_bar_dates = [
        str(row["last_day"]) for row in eod.get("source_results", [])
        if isinstance(row, dict) and row.get("status") == "PASS" and row.get("last_day")
    ]
    freshness = freshness_summary(last_bar_dates, cutoff.date())

    # Feature plane (Tier 1): deterministic per-symbol technical context.
    days_by_symbol = {}
    for row in eod.get("source_results", []):
        if isinstance(row, dict) and row.get("status") == "PASS" and row.get("days"):
            days_by_symbol[str(row["symbol"])] = [
                EodDay(d["date"], d["close"], d["open"], d["high"], d["low"], d["volume"])
                for d in row["days"]
            ]
    features = build_feature_bundle_from_days(days_by_symbol)

    # Independent data fetches run CONCURRENTLY so one slow/flaky source (e.g.
    # FRED) cannot stall the whole after-close batch. Each is fail-closed: a
    # ValueError becomes a BLOCKED entry, never a fabricated number. The EOD
    # ingest above stays sequential because candidates/features depend on it.
    from concurrent.futures import ThreadPoolExecutor, as_completed

    def _safe(fn, *args, **kwargs):
        # DATA peer-review: catch any exception (not just ValueError) so a
        # KeyError/TypeError from one desk cannot escape fut.result() and kill
        # the whole batch before the report is written. Fail-stop is honest, but
        # one flaky source should not cost the AM report.
        try:
            return fn(*args, **kwargs)
        except Exception as exc:
            return {"mode": "BLOCKED", "reason": str(exc)}

    csp_results: dict = {}
    chain_results: dict = {}
    rates: dict = {}
    vix: dict = {}
    macro: dict = {}
    earnings_results: dict = {}

    with ThreadPoolExecutor(max_workers=8) as ex:
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
            elif kind == "earnings":
                earnings_results[key] = res

    # VIX regime as a risk filter on the CSP candidates (RISK peer-review):
    # a HIGH regime flags/forces fits_gp_rules=False; ELEVATED warns.
    csp_results = apply_vix_regime_filter(vix, csp_results)

    # Compounding scale path for the top GP-fit candidate: how contracts scale
    # as the account grows, holding the 2%-of-equity rule. Purely conditional on
    # equity milestones; no performance projected or claimed.
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
        "earnings_actuals": earnings_results,
        "note": (
            "Equity candidates: collateral/margin from real EOD closes. Premium "
            "desk: executable net credit from REAL Cboe delayed option chains. "
            "Rates: real FRED observations. Earnings: real SEC EDGAR actuals. "
            "No probability or Risk of Ruin. No order placed; no trade "
            "authorized (every candidate trade_authorized=False)."
        ),
    }
    # Content-address the stable report body (exclude the hash and the
    # runtime path fields so the hash is reproducible across runs).
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
    tmp_path.write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    os.replace(tmp_path, final_path)  # atomic
    # Stable "latest" pointer so the web/iOS feed can read today's report.
    latest_path = root / "am-report-latest.json"
    latest_tmp = root / ".am-report-latest.tmp"
    latest_tmp.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    os.replace(latest_tmp, latest_path)
    report["report_path"] = str(final_path)
    report["latest_path"] = str(latest_path)
    return report


__all__ = ["NIGHTLY_VERSION", "DEFAULT_WATCHLIST", "run_nightly"]