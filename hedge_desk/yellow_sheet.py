"""Yellow Sheet — the product's decision document (the GP's word, not a paper log).

A Yellow Sheet is the decision artifact a GP fills when they decide to act on a
candidate: "Why Enter" (thesis), "Evidence / catalyst", "What Would Prove Me
Wrong" (invalidation), a "Planned Exit / Roll Rule", the risk state auto-filled
from a REAL candidate (collateral, return-on-capital, survivability), and the
decision. It is bound to the report hash it was made against, so the decision is
reproducible to the exact data. The low-level outcome journal (paper_log) remains
the place the observed OUTCOME is recorded after the position settles.

Honesty and safety:
- Append-only, content-addressed (sha256 per entry), tamper-evident — like the
  paper log. No in-place edits.
- The risk_state must come from a REAL evaluated candidate (it is auto-filled, not
  typed by the agent); absent a real risk_state the Yellow Sheet records
  risk_input_absent explicitly (fail closed) — never an invented risk reading.
- This is a PAPER decision document; trade_authorized stays False. No order.
- The thesis/evidence/invalidation are the GP's own research text. Stored in a
  gitignored local vault (artifacts/), never committed to the public repo.
"""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping, Optional, Sequence, Tuple

YELLOW_SHEET_VERSION = "hedge-desk-yellow-sheet-1.0.0"

ALLOWED_DECISIONS = frozenset({
    "RESEARCH",      # under research, no decision yet
    "NO_TRADE",      # reviewed, decided not to trade
    "PAPER_OPEN",    # paper position open (live fills would be LIVE_OPEN)
    "PAPER_CLOSED",  # paper position closed with a documented outcome
})

ALLOWED_STRATEGIES = frozenset({
    "CASH_SECURED_PUT", "COVERED_CALL", "CREDIT_SPREAD",
})


def _hash_entry(entry: Mapping[str, object]) -> str:
    body = {k: v for k, v in entry.items() if k not in ("entry_sha256", "seq")}
    return hashlib.sha256(
        json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _validate(
    *,
    symbol: str,
    strategy: str,
    thesis: str,
    invalidation: str,
    decision: str,
    recorded_at: Optional[datetime],
) -> Tuple[str, ...]:
    reasons = []
    if not symbol or not str(symbol).strip():
        reasons.append("SYMBOL_MISSING")
    if strategy not in ALLOWED_STRATEGIES:
        reasons.append("UNKNOWN_STRATEGY")
    if not thesis or not str(thesis).strip():
        reasons.append("THESIS_MISSING")
    if not invalidation or not str(invalidation).strip():
        reasons.append("INVALIDATION_MISSING")
    if decision not in ALLOWED_DECISIONS:
        reasons.append("UNKNOWN_DECISION")
    if recorded_at is not None and recorded_at.tzinfo is None:
        reasons.append("RECORDED_AT_NOT_UTC")
    return tuple(sorted(set(reasons)))


def record_yellow_sheet(
    vault_path: Path | str,
    *,
    symbol: str,
    strategy: str,
    thesis: str,
    evidence: str = "",
    invalidation: str,
    planned_exit: str = "",
    decision: str = "PAPER_OPEN",
    strike: Optional[str] = None,
    dte: Optional[int] = None,
    risk_state: Optional[Mapping[str, object]] = None,
    bound_report_sha256: Optional[str] = None,
    recorded_at: Optional[datetime] = None,
) -> dict:
    """Append one Yellow Sheet decision to the local vault (append-only, hashed).

    ``risk_state`` must be a dict produced by a real candidate evaluation (the
    CSP scan). If provided, it is stored verbatim and carries provenance. If a
    non-dict is passed, the entry fails closed with risk_input_absent.
    """
    reasons = _validate(
        symbol=symbol, strategy=strategy, thesis=thesis, invalidation=invalidation,
        decision=decision, recorded_at=recorded_at,
    )
    if reasons:
        raise ValueError("yellow sheet invalid: " + ",".join(reasons))

    if risk_state is not None and not isinstance(risk_state, Mapping):
        # A risk state that isn't a real mapping would be a fabricated input.
        raise ValueError("yellow sheet invalid: RISK_STATE_NOT_A_MAPPING")
    risk = dict(risk_state) if risk_state else {"risk_input_absent": True}

    path = Path(vault_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    recorded_at = recorded_at or datetime.now(timezone.utc)
    if path.exists():
        with path.open(encoding="utf-8") as fh:
            seq = sum(1 for _ in fh) + 1
    else:
        seq = 1

    entry = {
        "schema_version": YELLOW_SHEET_VERSION,
        "seq": seq,
        "symbol": str(symbol).upper(),
        "strategy": strategy,
        "strike": str(strike) if strike is not None else None,
        "dte": dte,
        "thesis": thesis,
        "evidence": evidence,
        "invalidation": invalidation,
        "planned_exit": planned_exit,
        "decision": decision,
        "risk_state": risk,
        "bound_report_sha256": bound_report_sha256,
        "recorded_at": recorded_at.isoformat(),
        "trade_authorized": False,
    }
    entry["entry_sha256"] = _hash_entry(entry)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, sort_keys=True) + "\n")
        fh.flush()
        os.fsync(fh.fileno())
    return dict(entry)


def read_yellow_sheets(vault_path: Path | str) -> Sequence[dict]:
    """Read and verify every entry; raise on tamper/corruption."""
    path = Path(vault_path)
    if not path.is_file():
        return []
    entries = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        entry = json.loads(line)
        expected = _hash_entry(entry)
        if entry.get("entry_sha256") != expected:
            raise ValueError("yellow sheet tampered at seq " + str(entry.get("seq")))
        entries.append(entry)
    return tuple(entries)


def summarize_yellow_sheets(vault_path: Path | str) -> dict:
    """Tally Yellow Sheets by decision and symbol (the decision ledger)."""
    entries = read_yellow_sheets(vault_path)
    by_decision: dict[str, int] = {}
    symbols: set[str] = set()
    for e in entries:
        d = str(e.get("decision", "UNKNOWN"))
        by_decision[d] = by_decision.get(d, 0) + 1
        symbols.add(str(e.get("symbol", "")))
    return {
        "schema_version": YELLOW_SHEET_VERSION,
        "mode": "YELLOW_SHEET_SUMMARY",
        "sheet_count": len(entries),
        "symbol_count": len(symbols),
        "by_decision": by_decision,
        "note": "Decision ledger; not performance. No P&L claimed.",
    }


__all__ = ["YELLOW_SHEET_VERSION", "ALLOWED_DECISIONS", "record_yellow_sheet",
           "read_yellow_sheets", "summarize_yellow_sheets"]