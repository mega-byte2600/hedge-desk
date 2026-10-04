"""Research-literature adapters for the Open Quant / AI Model Lab (keyless).

Sources (verified live 2026-10-04):
  - arXiv API: https://export.arxiv.org/api/query?search_query=...&max_results=N
    Atom XML. Slow in practice; this module's default transport uses a 45s
    timeout and passes start=0 explicitly.
  - Semantic Scholar: https://api.semanticscholar.org/graph/v1/paper/search
    Keyless but aggressively rate-limited (429 observed on 2026-10-04 even at
    low volume). 429 fails closed (ValueError, "data unavailable") — callers
    must back off, never retry blindly.

Both return rows of {title, abstract, year, url, authors, source}. Abstracts
are short strings when the provider omits them. Fail closed on transport
errors, non-200 status, or malformed payloads — never partial/invented rows.
"""

from __future__ import annotations

import urllib.parse
import xml.etree.ElementTree as ET
from typing import Callable, Sequence

from .feed_base import (
    FeedResult,
    Transport,
    _decode_json,
    _default_transport,
    _fetch_bytes,
    _fetch_json,
    _positive_limit,
    make_get_transport,
    utc_now_iso,
)

ARXIV_API_URL = "https://export.arxiv.org/api/query"
SEMANTIC_SCHOLAR_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

_arxiv_transport = make_get_transport(
    {
        "Accept": "application/atom+xml",
        "User-Agent": (
            "hedge-desk/1.0 research https://github.com/mega-byte2600/hedge-desk"
        ),
    },
    timeout=45,
)

_s2_transport = make_get_transport(
    {
        "Accept": "application/json",
        "User-Agent": (
            "hedge-desk/1.0 research https://github.com/mega-byte2600/hedge-desk"
        ),
    },
    timeout=20,
)

_S2_FIELDS = ("title", "abstract", "year", "authors", "url")

ATOM_NS = "http://www.w3.org/2005/Atom"


def _arxiv_text(entry: ET.Element, tag: str) -> str:
    child = entry.find(f"{{{ATOM_NS}}}{tag}")
    return (child.text or "").strip() if child is not None else ""


def _parse_arxiv_feed(raw: bytes, provider: str) -> tuple:
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        raise ValueError(f"{provider} returned malformed Atom XML") from exc
    if root.tag != f"{{{ATOM_NS}}}feed":
        raise ValueError(f"{provider} payload is not an Atom feed")
    rows = []
    for entry in root.findall(f"{{{ATOM_NS}}}entry"):
        paper_id = _arxiv_text(entry, "id")
        if not paper_id:
            raise ValueError(f"{provider} entry has no id")
        authors = []
        for author in entry.findall(f"{{{ATOM_NS}}}author"):
            name = author.find(f"{{{ATOM_NS}}}name")
            if name is not None and (name.text or "").strip():
                authors.append(name.text.strip())
        abs_link = ""
        for link in entry.findall(f"{{{ATOM_NS}}}link"):
            if link.attrib.get("rel") == "alternate":
                abs_link = link.attrib.get("href", "")
                break
        rows.append(
            {
                "title": _arxiv_text(entry, "title"),
                "abstract": _arxiv_text(entry, "summary"),
                "year": _arxiv_text(entry, "published")[:4],
                "url": abs_link or paper_id,
                "authors": authors,
                "source": "arxiv",
                "arxiv_id": paper_id.rsplit("/", 1)[-1],
            }
        )
    return tuple(rows)


def arxiv_search(
    search_query: str,
    max_results: int = 10,
    start: int = 0,
    transport: Transport = _arxiv_transport,
    now: Callable[[], str] = utc_now_iso,
) -> FeedResult:
    """Search arXiv via the export API. search_query uses arXiv syntax
    (e.g. 'all:option pricing' or 'ti:volatility forecasting')."""
    query = str(search_query).strip()
    if not query:
        raise ValueError("arxiv search_query is required")
    max_results = _positive_limit(max_results, 500)
    if type(start) is not int or start < 0:
        raise ValueError("arxiv start must be a non-negative integer")
    params = urllib.parse.urlencode(
        {
            "search_query": query,
            "start": str(start),
            "max_results": str(max_results),
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
    )
    raw = _fetch_bytes(f"{ARXIV_API_URL}?{params}", "arxiv", transport)
    rows = _parse_arxiv_feed(raw, "arxiv")
    return FeedResult(
        provider_id="arxiv", dataset="paper-search", rows=rows, fetched_at=now()
    )


def semantic_scholar_search(
    query: str,
    limit: int = 10,
    fields: Sequence[str] = _S2_FIELDS,
    transport: Transport = _s2_transport,
    now: Callable[[], str] = utc_now_iso,
) -> FeedResult:
    """Search Semantic Scholar's paper graph (keyless; rate-limited).

    A 429 (or the "Too Many Requests" message body) fails closed with
    "data unavailable" — callers must back off, never retry blindly.
    """
    text = str(query).strip()
    if not text:
        raise ValueError("semantic-scholar query is required")
    limit = _positive_limit(limit, 100)
    wanted = tuple(str(f).strip() for f in fields if str(f).strip())
    if not wanted:
        raise ValueError("semantic-scholar needs at least one field")
    params = urllib.parse.urlencode(
        {"query": text, "limit": str(limit), "fields": ",".join(wanted)}
    )
    try:
        payload = _fetch_json(f"{SEMANTIC_SCHOLAR_URL}?{params}", "semantic-scholar", transport)
    except ValueError as exc:
        if "429" in str(exc) or "Too Many Requests" in str(exc):
            raise ValueError(
                "semantic-scholar rate limited — data unavailable, back off and retry later"
            ) from exc
        raise
    if not isinstance(payload, dict) or not isinstance(payload.get("data"), list):
        raise ValueError("semantic-scholar payload has no data rows")
    rows = []
    for paper in payload["data"]:
        if not isinstance(paper, dict):
            raise ValueError("semantic-scholar paper is not an object")
        authors = paper.get("authors")
        rows.append(
            {
                "title": paper.get("title") or "",
                "abstract": paper.get("abstract") or "",
                "year": paper.get("year"),
                "url": paper.get("url") or "",
                "authors": [
                    a.get("name", "") for a in authors
                ]
                if isinstance(authors, list)
                else [],
                "source": "semantic-scholar",
            }
        )
    return FeedResult(
        provider_id="semantic-scholar",
        dataset="paper-search",
        rows=tuple(rows),
        fetched_at=now(),
    )


__all__ = [
    "ARXIV_API_URL",
    "SEMANTIC_SCHOLAR_URL",
    "arxiv_search",
    "semantic_scholar_search",
]
