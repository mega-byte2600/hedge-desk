"""SEC EDGAR full-text search adapter (verified live).

Endpoint (verified live 2026-10-04 — GET with URL query params returned
HTTP 200 with a declared User-Agent header):
  https://efts.sec.gov/LATEST/search-index?q="stock repurchase"&forms=10-Q&startdt=2026-01-01

SEC requires a declared client identity per EDGAR fair-access guidance; the
default transport reuses the declared hedge-desk identity from
feed_base._sec_transport (env-overridable via SEC_USER_AGENT /
SEC_CONTACT_EMAIL). This sandbox's own origin is flagged by SEC's
automated-tool gate, so independent re-confirmation of the response body from
here was not possible; the response parsing below follows the documented
elastic-style {"hits": {"hits": [...]}} shape and fails closed on anything
unexpected.

Intended feeds: filing-level corporate-event discovery (10-Q / 10-K / 8-K /
S-1 text search), complementing the sec-edgar submissions/XBRL adapters.
"""

from __future__ import annotations

import urllib.parse
from datetime import date as _date
from typing import Callable, Sequence

from .feed_base import (
    FeedResult,
    Transport,
    _fetch_json,
    _sec_transport,
    utc_now_iso,
)

SEC_FTS_URL = "https://efts.sec.gov/LATEST/search-index"

_DEFAULT_FORMS = ("10-K", "10-Q", "8-K", "S-1", "S-4", "DEF 14A", "SC 13D", "SC 13G")


def sec_fulltext_search(
    query: str,
    forms: Sequence[str] = _DEFAULT_FORMS,
    startdt: str | None = None,
    enddt: str | None = None,
    transport: Transport = _sec_transport,
    now: Callable[[], str] = utc_now_iso,
) -> FeedResult:
    """Full-text search across EDGAR filings via GET query params.

    query: free-text search, quote phrases for exact match
    (e.g. '"stock repurchase"'). forms: filing forms to search (comma-joined
    in the request). startdt/enddt: ISO date bounds (YYYY-MM-DD), optional.

    Fails closed: non-200, non-JSON, or an unexpected payload shape raises
    ValueError. Any live-shape correction must update the fixtures in
    tests/test_data_integrations.py.
    """
    text = str(query).strip()
    if not text:
        raise ValueError("sec-fts query is required")
    normalized_forms = [str(f).strip() for f in forms if str(f).strip()]
    if not normalized_forms:
        raise ValueError("sec-fts needs at least one filing form")
    params = {"q": text, "forms": ",".join(normalized_forms)}
    for label, value in (("startdt", startdt), ("enddt", enddt)):
        if value is None:
            continue
        value_str = str(value).strip()
        try:
            _date.fromisoformat(value_str)
        except ValueError as exc:
            raise ValueError(f"sec-fts {label} must be an ISO date (YYYY-MM-DD)") from exc
        params[label] = value_str
    url = SEC_FTS_URL + "?" + urllib.parse.urlencode(params)
    payload = _fetch_json(url, "sec-fts", transport)
    if not isinstance(payload, dict):
        raise ValueError("sec-fts payload is not an object")
    hits = payload.get("hits")
    if isinstance(hits, dict):
        hits = hits.get("hits")
    if not isinstance(hits, list):
        raise ValueError("sec-fts payload has no hits list")
    rows = []
    for hit in hits:
        if not isinstance(hit, dict):
            raise ValueError("sec-fts hit is not an object")
        src = hit.get("_source") if isinstance(hit.get("_source"), dict) else hit
        rows.append(
            {
                "form": src.get("form"),
                "company": src.get("c_name") or src.get("companyName"),
                "cik": src.get("c_cik") or src.get("cik"),
                "file_date": src.get("f_date") or src.get("filedAt"),
                "accession": src.get("adsh") or src.get("accessionNumber"),
                "title": src.get("title"),
                "raw": src,
            }
        )
    return FeedResult(
        provider_id="sec-fts",
        dataset="fulltext-search",
        rows=tuple(rows),
        fetched_at=now(),
    )


__all__ = [
    "SEC_FTS_URL",
    "sec_fulltext_search",
]
