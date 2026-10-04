"""GDELT 2.1 DOC API adapter for the Futures Event desk (keyless).

Endpoint (verified live 2026-10-04 — and it rate-limited the probe call
itself, confirming aggressive limiting):
  https://api.gdeltproject.org/api/v2/doc/doc?query=...&mode=artlist&maxrecords=N&format=json

GDELT returns a plain-text "Please limit requests to one every 5 seconds"
notice on HTTP 200 instead of JSON when it throttles. This module:
  - paces calls: minimum 6 seconds between requests (injectable clock/sleeper
    so tests stay deterministic);
  - fails closed on the rate-limit notice or any transport/parse error with
    an explicit "data unavailable" ValueError — never partial or invented rows.

Feeds: Futures Event desk (catalyst news, domain/language/sourcecountry
enrichment per article).
"""

from __future__ import annotations

import time as _time
import urllib.parse
from typing import Callable

from .feed_base import (
    Clock,
    FeedResult,
    Sleeper,
    Transport,
    _default_transport,
    _decode_json,
    _fetch_bytes,
    _positive_limit,
    utc_now_iso,
)

GDELT_DOC_URL = "https://api.gdeltproject.org/api/v2/doc/doc"
GDELT_MIN_PACING_SECONDS = 6.0
_RATE_LIMIT_MARKER = "Please limit requests to one every 5 seconds"


class GdeltPacer:
    """Enforces the >=6s gap GDELT requires between DOC API calls."""

    def __init__(
        self,
        min_gap: float = GDELT_MIN_PACING_SECONDS,
        clock: Clock = _time.monotonic,
        sleeper: Sleeper = _time.sleep,
    ) -> None:
        if min_gap < 0:
            raise ValueError("GDELT pacing gap must be non-negative")
        self._min_gap = min_gap
        self._clock = clock
        self._sleeper = sleeper
        self._last_call = 0.0
        self._calls_made = 0

    def wait(self) -> None:
        now = self._clock()
        if self._calls_made:
            elapsed = now - self._last_call
            if elapsed < self._min_gap:
                self._sleeper(self._min_gap - elapsed)
        self._last_call = self._clock()
        self._calls_made += 1


_default_pacer = GdeltPacer()


def gdelt_artlist(
    query: str,
    maxrecords: int = 25,
    transport: Transport = _default_transport,
    pacer: GdeltPacer | None = None,
    now: Callable[[], str] = utc_now_iso,
) -> FeedResult:
    """Fetch GDELT 2.1 artlist articles for a DOC query.

    DOC 2.1 query syntax applies (e.g. 'FEDERAL RESERVE' with quotes,
    theme:ECON, sourcelang:english). Rate-limit responses fail closed as
    "data unavailable".
    """
    text = str(query).strip()
    if not text:
        raise ValueError("gdelt query is required")
    maxrecords = _positive_limit(maxrecords, 250)
    (pacer or _default_pacer).wait()
    params = urllib.parse.urlencode(
        {
            "query": text,
            "mode": "artlist",
            "maxrecords": str(maxrecords),
            "format": "json",
        }
    )
    # GDELT answers throttled calls with plain text on HTTP 200, so inspect
    # the raw body for the rate-limit marker before JSON decoding.
    try:
        raw = _fetch_bytes(f"{GDELT_DOC_URL}?{params}", "gdelt", transport)
    except ValueError as exc:
        if _RATE_LIMIT_MARKER in str(exc):
            raise ValueError(
                "gdelt rate limited — data unavailable, wait and retry later"
            ) from exc
        raise
    body_text = raw.decode("utf-8", errors="replace")
    if _RATE_LIMIT_MARKER in body_text:
        raise ValueError("gdelt rate limited — data unavailable, wait and retry later")
    payload = _decode_json(raw, "gdelt")
    if not isinstance(payload, dict):
        raise ValueError("gdelt payload is not an object")
    articles = payload.get("articles")
    if not isinstance(articles, list):
        raise ValueError("gdelt payload has no articles list")
    rows = []
    for article in articles:
        if not isinstance(article, dict):
            raise ValueError("gdelt article is not an object")
        rows.append(
            {
                "title": str(article.get("title") or ""),
                "url": str(article.get("url") or ""),
                "url_mobile": str(article.get("url_mobile") or ""),
                "seendate": str(article.get("seendate") or ""),
                "socialimage": str(article.get("socialimage") or ""),
                "domain": str(article.get("domain") or ""),
                "language": str(article.get("language") or ""),
                "sourcecountry": str(article.get("sourcecountry") or ""),
            }
        )
    return FeedResult(
        provider_id="gdelt", dataset="doc-artlist", rows=tuple(rows), fetched_at=now()
    )


__all__ = [
    "GDELT_DOC_URL",
    "GDELT_MIN_PACING_SECONDS",
    "GdeltPacer",
    "gdelt_artlist",
]
