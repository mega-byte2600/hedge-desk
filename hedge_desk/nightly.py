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

NIGHTLY_VERSION = "hedge-desk-nightly-1.0.0"
DEFAULT_WATCHLIST = ("SPY", "QQQ", "AAPL", "MSFT", "NVDA", "TSLA")


def _watchlist() -> Sequence[str]:
    raw = os.environ.get("EOD_WATCHLIST", "")
    if raw.strip():
        return tuple(s.strip().upper() for s in raw.split(",") if s.strip())
    return DEFAULT_WATCHLIST


def run_nightly(
    watchlist: Sequence[str] | None = None,
    artifacts_dir: Path | str = "artifacts",
    transport=None,
) -> Dict[str, object]:
    """Run the EOD batch + premium candidates and write the AM report."""
    symbols = tuple(watchlist) if watchlist else _watchlist()
    if not symbols:
        raise ValueError("nightly watchlist cannot be empty")
    cutoff = datetime.now(timezone.utc)
    eod = ingest_eod(symbols, cutoff, transport=transport) if transport else ingest_eod(symbols, cutoff)
    candidates = build_premium_candidates(eod)

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
        "note": (
            "Collateral/margin requirements from real EOD closes. No option "
            "prices, probability, or Risk of Ruin fabricated. No order placed; "
            "no trade authorized. Premium income requires a real option chain."
        ),
    }
    # Content-address the report body (without the hash field itself).
    body = {k: v for k, v in report.items() if k != "report_sha256"}
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
    report["report_path"] = str(final_path)
    return report


__all__ = ["NIGHTLY_VERSION", "DEFAULT_WATCHLIST", "run_nightly"]