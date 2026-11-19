"""Shared plumbing for the keyless data-integration modules.

Everything here is stdlib-only. Mirrors the conventions of
hedge_desk/data/open_market_feeds.py: injectable transports, fail-closed
ValueError semantics, no live network in tests (transports are overridable).
"""

from __future__ import annotations

import json
import os
import random
import ssl
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Mapping, Tuple


Transport = Callable[[str], Tuple[int, bytes]]
RequestTransport = Callable[[urllib.request.Request], Tuple[int, bytes]]
Clock = Callable[[], float]
Sleeper = Callable[[float], None]


@dataclass(frozen=True)
class FeedResult:
    """Small result dataclass shared by all integration modules."""

    provider_id: str
    dataset: str
    rows: Tuple[Mapping[str, object], ...]
    fetched_at: str = field(default="")

    @property
    def row_count(self) -> int:
        return len(self.rows)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _system_ssl_context() -> ssl.SSLContext:
    try:
        import certifi

        return ssl.create_default_context(cafile=certifi.where())
    except Exception:  # pragma: no cover
        return ssl.create_default_context()


def _urlopen(request: urllib.request.Request, timeout: int) -> Tuple[int, bytes]:
    try:
        with urllib.request.urlopen(
            request, timeout=timeout, context=_system_ssl_context()
        ) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()
    except Exception as exc:
        return 0, str(exc).encode("utf-8")


# 429 (rate limited) is deliberately NOT retried: the provider has told us to
# stop, so the call fails closed with its status and the caller reports it
# (CarpeDATA invariant 4: respect every provider's limits). Only transport
# errors (0) and transient 5xx are retried.
RETRYABLE_STATUSES = frozenset({0, 500, 502, 503, 504})


def with_retries(
    transport: Transport,
    attempts: int = 3,
    base_delay: float = 0.5,
    max_delay: float = 8.0,
    sleeper: Sleeper = time.sleep,
    rng: Callable[[], float] = random.random,
) -> Transport:
    """Wrap a GET transport with bounded exponential backoff and full jitter.

    Retries only transport errors (status 0) and 5xx (never 429), the transient
    classes in Google SRE "Handling Overload" and the AWS Architecture Blog
    "Exponential Backoff and Jitter" (full-jitter variant). GET is
    idempotent, so a retry cannot double-act. The last response is returned
    unchanged, so callers keep their fail-closed status handling.
    """
    if attempts < 1:
        raise ValueError("attempts must be >= 1")

    def wrapped(url: str) -> Tuple[int, bytes]:
        status, body = transport(url)
        for attempt in range(1, attempts):
            if status not in RETRYABLE_STATUSES:
                break
            sleeper(rng() * min(max_delay, base_delay * (2 ** (attempt - 1))))
            status, body = transport(url)
        return status, body

    return wrapped


def make_get_transport(
    headers: Mapping[str, str],
    timeout: int = 15,
) -> Transport:
    """Build a GET Transport with fixed headers (the repo pattern's injectable default)."""

    def transport(url: str) -> Tuple[int, bytes]:
        req = urllib.request.Request(url, headers=dict(headers))
        return _urlopen(req, timeout)

    # Single attempt, exactly as established. Callers own their retry policy
    # (_fetch_json/_fetch_bytes already retry; the SEC probe must not retry).
    # Wrapping here stacked retries (up to 9 calls) — reverted per CarpeDATA.
    return transport


_DEFAULT_UA = os.environ.get(
    "MARKET_DATA_USER_AGENT",
    "hedge-desk/1.0 research https://github.com/mega-byte2600/hedge-desk",
).strip()

_default_transport = make_get_transport(
    {"Accept": "application/json", "User-Agent": _DEFAULT_UA}
)

_NASDAQ_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)

_nasdaq_transport = make_get_transport(
    {"Accept": "application/json", "User-Agent": _NASDAQ_UA}
)


def _sec_user_agent() -> str:
    contact = os.environ.get("SEC_CONTACT_EMAIL", "").strip()
    user_agent = os.environ.get("SEC_USER_AGENT", "").strip()
    if user_agent:
        return user_agent
    if contact:
        return f"hedge-desk/1.0 {contact}"
    # SEC fair-access guidance asks scripted clients to identify both the
    # application and a contact. A browser UA or a project URL alone can be
    # rejected by EDGAR's automated-access gate.
    return "Emporion Hedge Desk/1.0 michael.bolton.ph@dartmouth.edu"


def _sec_transport(url: str) -> Tuple[int, bytes]:
    """Fetch SEC data with a declared, environment-overridable client identity."""
    transport = make_get_transport(
        {
            "Accept": "application/json",
            "User-Agent": _sec_user_agent(),
        }
    )
    return transport(url)


def _decode_json(raw: bytes, provider: str) -> Any:
    try:
        return json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as exc:
        raise ValueError(f"{provider} returned malformed JSON") from exc


def _is_transient_status(status: int) -> bool:
    return status == 0 or status == 429 or 500 <= status < 600


def _fetch_json(
    url: str,
    provider: str,
    transport: Transport,
    retries: int = 2,
) -> Any:
    last_status, last_raw = 0, b""
    for attempt in range(retries + 1):
        try:
            status, raw = transport(url)
        except Exception as exc:
            status, raw = 0, str(exc).encode("utf-8")
        if status == 200 and raw:
            return _decode_json(raw, provider)
        last_status, last_raw = status, raw
        if not _is_transient_status(status) or attempt == retries:
            break
        import time as _time

        _time.sleep(1.0 * (attempt + 1))
    body = last_raw[:200].decode("utf-8", errors="replace") if last_raw else ""
    raise ValueError(f"{provider} fetch failed (status {last_status}) body={body}")


def _fetch_bytes(
    url: str,
    provider: str,
    transport: Transport,
    retries: int = 2,
) -> bytes:
    last_status, last_raw = 0, b""
    for attempt in range(retries + 1):
        try:
            status, raw = transport(url)
        except Exception as exc:
            status, raw = 0, str(exc).encode("utf-8")
        if status == 200 and raw:
            return raw
        last_status, last_raw = status, raw
        if not _is_transient_status(status) or attempt == retries:
            break
        import time as _time

        _time.sleep(1.0 * (attempt + 1))
    body = last_raw[:200].decode("utf-8", errors="replace") if last_raw else ""
    raise ValueError(f"{provider} fetch failed (status {last_status}) body={body}")


def _positive_limit(limit: int, maximum: int = 1000) -> int:
    if type(limit) is not int or limit < 1 or limit > maximum:
        raise ValueError(f"limit must be an integer from 1 to {maximum}")
    return limit


def _rows_from_list(payload: object, provider: str) -> Tuple[Mapping[str, object], ...]:
    if not isinstance(payload, list):
        raise ValueError(f"{provider} payload is not a row list")
    rows = []
    for row in payload:
        if not isinstance(row, dict):
            raise ValueError(f"{provider} row is not an object")
        rows.append(row)
    return tuple(rows)


def _normalize_iso_date(value: object) -> str | None:
    """Convert MM/DD/YYYY to ISO date; None when absent or unparsable."""
    text = str(value).strip()
    if not text:
        return None
    from datetime import datetime as _dt

    for fmt in ("%m/%d/%Y", "%Y-%m-%d"):
        try:
            return _dt.strptime(text, fmt).date().isoformat()
        except ValueError:
            continue
    return None


__all__ = [
    "Clock",
    "FeedResult",
    "RequestTransport",
    "Sleeper",
    "Transport",
    "_default_transport",
    "_decode_json",
    "_fetch_bytes",
    "_fetch_json",
    "_is_transient_status",
    "_nasdaq_transport",
    "_normalize_iso_date",
    "_positive_limit",
    "_rows_from_list",
    "_sec_transport",
    "make_get_transport",
    "utc_now_iso",
]
