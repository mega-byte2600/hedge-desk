"""Nonblocking, read-only SEC submissions feed for the approved Desk 5 watchlist."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from threading import Lock, Thread
from time import monotonic
from typing import Dict, Iterable

from hedge_desk.data.open_market_feeds import sec_submissions

# SEC CIKs are identifiers, not a substitute universe. Only requested watchlist
# symbols are queried. Extend this map only from an authoritative SEC mapping.
CIK_BY_TICKER = {
    "NKE": "0000320187", "CCL": "0000815097", "AAL": "0000006201",
    "LYFT": "0001759509", "NCLH": "0001513761", "F": "0000037996",
    "DVN": "0001090012", "MSFT": "0000789019", "NVDA": "0001045810",
    "GOOGL": "0001652044", "GOOG": "0001652044", "AMZN": "0001018724",
    "META": "0001326801", "ORCL": "0001341439",
}

_lock = Lock()
_snapshot: Dict[str, dict] = {}
_built_at = 0.0
_refreshing = False
_CACHE_SECONDS = 3600.0


def _extract_filings(symbol: str, payload: dict) -> dict:
    recent = payload.get("filings", {}).get("recent", {})
    columns = ("form", "filingDate", "reportDate", "accessionNumber", "primaryDocument")
    if not all(isinstance(recent.get(key), list) for key in columns):
        raise ValueError("SEC submissions recent-filings fields are malformed")
    item_rows = recent.get("items", [])
    if not isinstance(item_rows, list):
        item_rows = []
    rows = []
    for index, values in enumerate(zip(*(recent[key] for key in columns))):
        form, filing_date, report_date, accession, document = values
        if form not in {"10-K", "10-Q", "8-K", "20-F", "6-K"}:
            continue
        if not all(isinstance(value, str) and value for value in (filing_date, accession, document)):
            continue
        cik = CIK_BY_TICKER[symbol].lstrip("0")
        accession_path = accession.replace("-", "")
        rows.append({
            "form": form,
            "filing_date": filing_date,
            "report_date": report_date if isinstance(report_date, str) else "",
            "items": item_rows[index] if index < len(item_rows) and isinstance(item_rows[index], str) else "",
            "catalyst_evidence": "SEC_FILING_EVENT_LEAD" if form == "8-K" else "DATED_REGULATORY_FILING",
            "url": f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_path}/{document}",
        })
        if len(rows) == 5:
            break
    return {"status": "LIVE", "company_name": payload.get("name", ""), "filings": rows}


def _refresh(symbols: tuple[str, ...]) -> None:
    global _snapshot, _built_at, _refreshing
    try:
        def load_symbol(symbol: str) -> tuple[str, dict]:
            if symbol not in CIK_BY_TICKER:
                return symbol, {"status": "CIK_UNMAPPED", "filings": []}
            try:
                payload = sec_submissions(CIK_BY_TICKER[symbol], retries=0)
                record = _extract_filings(symbol, payload)
                if not record["filings"]:
                    record = {"status": "LIVE_NO_RECENT_FORMS", "company_name": payload.get("name", ""), "filings": []}
                return symbol, record
            except Exception:
                return symbol, {"status": "BLOCKED", "filings": []}

        # SEC fair-access guidance allows up to 10 requests per second. Four
        # workers keep the approved watchlist refresh comfortably below that
        # ceiling while avoiding a long serial spinner for every user.
        with ThreadPoolExecutor(max_workers=min(4, max(1, len(symbols)))) as pool:
            fresh = dict(pool.map(load_symbol, symbols))
        with _lock:
            _snapshot = {**_snapshot, **fresh}
            _built_at = monotonic()
    finally:
        with _lock:
            _refreshing = False


def get_sec_filings(symbols: Iterable[str]) -> dict:
    """Return last-known filings immediately, refreshing stale symbols in background."""
    global _refreshing
    requested = tuple(dict.fromkeys(str(item).strip().upper() for item in symbols if str(item).strip()))
    with _lock:
        missing = any(symbol not in _snapshot for symbol in requested)
        stale = monotonic() - _built_at >= _CACHE_SECONDS
        start = (missing or stale) and not _refreshing
        if start:
            _refreshing = True
            Thread(target=_refresh, args=(requested,), name="sec-watchlist-refresh", daemon=True).start()
        result = {
            symbol: _snapshot.get(symbol, {"status": "LOADING", "filings": []})
            for symbol in requested
        }
    return {"status": "REFRESHING" if start else "CACHED", "symbols": result, "source": "SEC EDGAR submissions"}


__all__ = ["CIK_BY_TICKER", "get_sec_filings", "_extract_filings"]
