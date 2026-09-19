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

from hedge_desk.data.eod_ingest import ingest_eod
from hedge_desk.premium_candidates import build_premium_candidates
from hedge_desk.cboe_chain import real_chain_income
from hedge_desk.rates_desk import rates_environment
from hedge_desk.earnings_desk import earnings_desk
from hedge_desk.execution_gate import (
    KillSwitch,
    build_candidate_from_structure,
    evaluate_execution,
)
from hedge_desk.domain import Account, AccountType
from decimal import Decimal

NIGHTLY_VERSION = "hedge-desk-nightly-2.0.0"
DEFAULT_WATCHLIST = ("SPY", "QQQ", "AAPL", "MSFT", "NVDA", "TSLA")


def _watchlist() -> Sequence[str]:
    raw = os.environ.get("EOD_WATCHLIST", "")
    if raw.strip():
        return tuple(s.strip().upper() for s in raw.split(",") if s.strip())
    return DEFAULT_WATCHLIST


def _annotate_chain_with_gates(
    chain: Dict[str, object],
    account_equity: str = "100000",
    kill_switch_armed: bool = False,
) -> Dict[str, object]:
    """Annotate each presented premium structure with its risk+release gate decision."""
    from datetime import datetime as _dt

    acct = Account(
        "demo-account", AccountType.INDIVIDUAL,
        Decimal(account_equity), Decimal(account_equity) / Decimal("2"),
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
    out["gate_account_equity"] = account_equity
    out["gate_risk_input_advanced"] = False
    out["gate_note"] = (
        "No validated Risk-of-Ruin artifact and no real account/liquidity are "
        "wired yet, so gate decisions are INDETERMINATE (missing inputs), never a "
        "fabricated approval. No order is placed and nothing is trade_authorized."
    )
    out["gate_kill_switch_armed"] = kill_switch_armed
    return out
    out = dict(chain)
    out["gated_income_structures"] = gated
    out["gate_account_equity"] = account_equity
    out["gate_kill_switch_armed"] = kill_switch_armed
    return out


def run_nightly(
    watchlist: Sequence[str] | None = None,
    artifacts_dir: Path | str = "artifacts",
    transport=None,
    chain_symbols: Sequence[str] = ("SPY",),
    chain_transport=None,
    rates_transport=None,
    earnings_ciks: Sequence[str] = (),
    earnings_transport=None,
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
    eod = ingest_eod(symbols, cutoff, transport=transport) if transport else ingest_eod(symbols, cutoff)
    candidates = build_premium_candidates(eod)

    chain_results = {}
    for cs in chain_symbols:
        cs = str(cs).upper()
        try:
            chain = (
                real_chain_income(cs, cutoff, transport=chain_transport)
                if chain_transport
                else real_chain_income(cs, cutoff)
            )
            chain_results[cs] = _annotate_chain_with_gates(chain)
        except ValueError as exc:
            chain_results[cs] = {"mode": "BLOCKED", "reason": str(exc)}

    # Real macro: rates environment (FRED).
    try:
        rates = (
            rates_environment(transport=rates_transport)
            if rates_transport
            else rates_environment()
        )
    except ValueError as exc:
        rates = {"mode": "BLOCKED", "reason": str(exc)}

    # Real earnings actuals (SEC EDGAR) per supplied CIK.
    earnings_results = {}
    for cik in earnings_ciks:
        try:
            earnings_results[cik] = (
                earnings_desk(cik, transport=earnings_transport)
                if earnings_transport
                else earnings_desk(cik)
            )
        except ValueError as exc:
            earnings_results[cik] = {"mode": "BLOCKED", "reason": str(exc)}

    report = {
        "schema_version": NIGHTLY_VERSION,
        "mode": "REAL_EOD_NIGHTLY",
        "generated_at": cutoff.isoformat(),
        "watchlist": list(symbols),
        "eod_batch_status": eod["batch_status"],
        "eod_manifest_sha256": eod["batch_manifest_sha256"],
        "candidate_count": candidates["candidate_count"],
        "symbol_count": candidates["symbol_count"],
        "candidates": candidates["candidates"],
        "eod_source_results": eod["source_results"],
        "chain_income": chain_results,
        "rates_environment": rates,
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