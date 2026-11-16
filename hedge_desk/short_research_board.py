"""Build Desk 5's sourced short-research queue from approved watchlist data."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Dict, List, Optional


SCHEMA_VERSION = "hedge-desk-short-research-board-1.0.0"


def _pct(current: Decimal, prior: Decimal) -> Optional[Decimal]:
    if prior == 0:
        return None
    return ((current / prior) - Decimal("1")) * Decimal("100")


def build_short_research_board(report_path: Path) -> Dict[str, Any]:
    """Read the last real nightly snapshot; never synthesize candidate cases."""
    try:
        report = json.loads(Path(report_path).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return {
            "schema_version": SCHEMA_VERSION,
            "status": "DATA_UNAVAILABLE",
            "reason": "latest validated nightly report unavailable",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "as_of": None,
            "symbols": [],
            "trade_authorized": False,
        }

    source_rows = {str(row.get("symbol", "")).upper(): row
                   for row in report.get("eod_source_results", [])
                   if isinstance(row, dict)}
    series = report.get("series", {}).get("symbols", {})
    from hedge_desk.sec_filings_service import get_sec_filings
    sec_snapshot = get_sec_filings(report.get("watchlist", []))
    from hedge_desk.short_interest_service import get_short_interest
    short_snapshot = get_short_interest(report.get("watchlist", []))
    rows: List[Dict[str, Any]] = []
    for raw_symbol in report.get("watchlist", []):
        symbol = str(raw_symbol).strip().upper()
        source = source_rows.get(symbol, {})
        points = series.get(symbol, []) if isinstance(series, dict) else []
        valid: List[tuple[str, Decimal]] = []
        for point in points if isinstance(points, list) else []:
            try:
                session, close = point
                amount = Decimal(str(close))
                if amount.is_finite() and amount > 0:
                    valid.append((str(session), amount))
            except (TypeError, ValueError, InvalidOperation):
                continue
        last = valid[-1] if valid else None
        latest = last[1] if last else None
        ret5 = _pct(latest, valid[-6][1]) if latest is not None and len(valid) >= 6 else None
        ret20 = _pct(latest, valid[-21][1]) if latest is not None and len(valid) >= 21 else None
        source_ok = source.get("status") == "PASS" and last is not None
        if not source_ok or ret5 is None or ret20 is None:
            price_context = "INSUFFICIENT_DATA"
        elif ret5 < 0 and ret20 < 0:
            price_context = "BOTH_LOOKBACKS_NEGATIVE"
        elif ret5 < 0 or ret20 < 0:
            price_context = "MIXED_LOOKBACKS"
        else:
            price_context = "BOTH_LOOKBACKS_POSITIVE"
        issuer_filings = sec_snapshot["symbols"].get(symbol, {}).get("filings", [])
        issuer_short = short_snapshot["symbols"].get(symbol, {"status": "LOADING"})
        rows.append({
            "symbol": symbol,
            "status": "PRICE_CONTEXT_AVAILABLE" if source_ok else "PRICE_DATA_UNAVAILABLE",
            "last_close": float(latest) if source_ok else None,
            "price_as_of": last[0] if source_ok else None,
            "return_5_sessions_pct": float(ret5) if source_ok and ret5 is not None else None,
            "return_20_sessions_pct": float(ret20) if source_ok and ret20 is not None else None,
            "price_context": price_context,
            "eod_source_status": source.get("status", "MISSING"),
            "sec_filing_status": sec_snapshot["symbols"].get(symbol, {}).get("status", "LOADING"),
            "sec_filings": issuer_filings,
            "sec_company_name": sec_snapshot["symbols"].get(symbol, {}).get("company_name", ""),
            "catalyst_status": (
                "SEC_8K_EVENT_LEADS_AVAILABLE"
                if any(filing.get("form") == "8-K" for filing in issuer_filings)
                else "DATED_FILINGS_ONLY"
                if issuer_filings
                else "NO_DATED_SEC_FILING_LEAD"
            ),
            "short_interest": issuer_short,
            "short_interest_status": issuer_short.get("status", "LOADING"),
            "borrow_status": "BROKER_CONFIRMATION_REQUIRED",
            "case_status": "NO_SHORT_THESIS",
            "trade_authorized": False,
        })

    as_of = report.get("series", {}).get("as_of")
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "LIVE" if rows and any(r["status"] == "PRICE_CONTEXT_AVAILABLE" for r in rows) else "DATA_UNAVAILABLE",
        "generated_at": report.get("generated_at"),
        "as_of": as_of,
        "watchlist_source": "latest validated nightly report",
        "sec_feed_status": sec_snapshot["status"],
        "sec_feed_source": sec_snapshot["source"],
        "short_interest_feed_status": short_snapshot["status"],
        "short_interest_feed_source": short_snapshot["source"],
        "short_interest_interpretation": short_snapshot["interpretation"],
        "symbols": rows,
        "interpretation": "Price behavior is descriptive context. SEC filings and FINRA short-interest snapshots are evidence leads, not a completed short thesis or borrow confirmation. No trade is authorized.",
        "trade_authorized": False,
    }
