"""Paper trade outcome log (roadmap Tier 4 - feedback plane).

The honest heartbeat of a high-flyer-like desk: every paper decision records an
outcome, and outcomes feed re-evaluation so the signal improves on measured
results. Without this, nothing in the desk ever learns.

Honesty and safety:
- Append-only JSONL, content-addressed per entry. No in-place edits.
- Only OBSERVED outcomes are recorded: entered / expired_worthless / stopped /
  assigned / closed. No inferred probability, no fabricated P&L.
- Absent a real account and real fills, entry states are PAPER; a closed/entered
  outcome can only be recorded when the user supplies the actual market outcome.
- Never estimates Risk of Ruin. trade_authorized is not a thing here — this is
  the recording layer AFTER a paper decision, not an order.
"""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping, Sequence, Tuple

PAPER_LOG_VERSION = "hedge-desk-paper-outcome-log-1.0.0"

ALLOWED_OUTCOMES = frozenset({
    "NEVER_ENTERED",      # paper candidate selected but not entered
    "ENTERED_PAPER",      # paper entry recorded (needs real fills to be LIVE)
    "EXPIRED_WORTHLESS",  # collected the full premium, no assignment
    "ASSIGNED",           # put assigned -> now own the underlying at strike
    "STOPPED",            # stopped out / closed at a loss or managed
    "CLOSED_GAIN",        # closed profitably before expiration
    "CLOSED_LOSS",        # closed at a loss before expiration
    "UNKNOWN",            # outcome not yet settled
})


def _hash_entry(entry: Mapping[str, object]) -> str:
    # content-address excludes the entry's own hash + sequence to keep it stable
    body = {k: v for k, v in entry.items() if k not in ("entry_sha256", "seq")}
    return hashlib.sha256(
        json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _validate_entry(
    *,
    candidate_id: str,
    symbol: str,
    strategy: str,
    outcome: str,
    entered_at: datetime | None,
    exit_price: str | None = None,
    premium_received: str | None = None,
) -> Tuple[str, ...]:
    reasons = []
    if not candidate_id or not symbol:
        reasons.append("CANDIDATE_IDENTITY_MISSING")
    if strategy not in ("CASH_SECURED_PUT", "COVERED_CALL", "CREDIT_SPREAD"):
        reasons.append("UNKNOWN_STRATEGY")
    if outcome not in ALLOWED_OUTCOMES:
        reasons.append("UNKNOWN_OUTCOME")
    if entered_at is not None and entered_at.tzinfo is None:
        reasons.append("ENTRY_TIME_NOT_UTC")
    return tuple(sorted(set(reasons)))


def append_outcome(
    log_path: Path | str,
    *,
    candidate_id: str,
    symbol: str,
    strategy: str,
    outcome: str,
    entered_at: datetime | None = None,
    exit_price: str | None = None,
    premium_received: str | None = None,
    recorded_at: datetime | None = None,
) -> dict:
    """Append one observed paper outcome to the journal (append-only, hashed)."""
    reasons = _validate_entry(
        candidate_id=candidate_id, symbol=symbol, strategy=strategy, outcome=outcome,
        entered_at=entered_at, exit_price=exit_price, premium_received=premium_received,
    )
    if reasons:
        raise ValueError("paper outcome invalid: " + ",".join(reasons))
    path = Path(log_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    recorded_at = recorded_at or datetime.now(timezone.utc)
    # sequence = existing line count + 1 (append-only; entries never rewritten)
    if path.exists():
        with path.open(encoding="utf-8") as fh:
            seq = sum(1 for _ in fh) + 1
    else:
        seq = 1
    entry = {
        "schema_version": PAPER_LOG_VERSION,
        "seq": seq,
        "candidate_id": candidate_id,
        "symbol": symbol,
        "strategy": strategy,
        "outcome": outcome,
        "entered_at": entered_at.isoformat() if entered_at else None,
        "exit_price": exit_price,
        "premium_received": premium_received,
        "recorded_at": recorded_at.isoformat(),
        "trade_authorized": False,
    }
    entry["entry_sha256"] = _hash_entry(entry)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, sort_keys=True) + "\n")
        fh.flush()
        os.fsync(fh.fileno())  # durability: don't lose an observed outcome
    return dict(entry)


def read_log(log_path: Path | str) -> Sequence[dict]:
    """Read and verify every entry; raise on tamper/corruption."""
    path = Path(log_path)
    if not path.is_file():
        return []
    entries = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        entry = json.loads(line)
        expected = _hash_entry(entry)
        if entry.get("entry_sha256") != expected:
            raise ValueError("paper log entry tampered at seq " + str(entry.get("seq")))
        entries.append(entry)
    return tuple(entries)


def summarize(log_path: Path | str) -> dict:
    """Tally observed outcomes by category (validated learning, not performance)."""
    entries = read_log(log_path)
    counts: dict[str, int] = {}
    symbols: set[str] = set()
    for e in entries:
        oc = str(e.get("outcome", "UNKNOWN"))
        counts[oc] = counts.get(oc, 0) + 1
        symbols.add(str(e.get("symbol", "")))
    return {
        "schema_version": PAPER_LOG_VERSION,
        "mode": "PAPER_OUTCOME_SUMMARY",
        "entry_count": len(entries),
        "symbol_count": len(symbols),
        "outcome_counts": counts,
        "note": "Observed outcomes tally; NOT performance. No P&L claimed.",
    }


__all__ = ["PAPER_LOG_VERSION", "append_outcome", "read_log", "summarize",
           "ALLOWED_OUTCOMES"]