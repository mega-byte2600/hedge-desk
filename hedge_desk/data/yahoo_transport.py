"""Hardened Yahoo Finance transport: crumb handling, backoff, pacing, UA rotation.

Root cause it addresses (verified 2026-10-04 from this VM):
Yahoo's query1/query2 endpoints intermittently return HTTP 401 from datacenter
IPs (bot mitigation). The v7 options endpoint requires a crumb, and the crumb
endpoint itself 401s under the same mitigation. Retrying the identical request
never recovers — the correct response is: refresh the crumb once, back off,
then FAIL OVER to the next source instead of stalling the desk.

The repo's only Yahoo module (hedge_desk/data/eod_ingest.py) uses the v8 chart
API (lenient, no crumb needed) and has NO crumb handling and NO options
fetcher at all — the premium desk's options pulls were ad-hoc with no retry,
no crumb, and no failover. That is why the 10-01 premarket and 10-03 daily runs
lost the entire Premium IV desk instead of degrading gracefully.

All network goes through an injectable transport so tests never touch the net.
"""

from __future__ import annotations

import http.cookiejar
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Tuple

# Small pool of current browser UAs. Rotated per SESSION, not per request —
# per-request rotation looks more bot-like, not less.
USER_AGENTS = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
]

CRUMB_URL = "https://query1.finance.yahoo.com/v1/test/getcrumb"
COOKIE_URL = "https://fc.yahoo.com"

MIN_INTERVAL_S = 1.0          # minimum gap between Yahoo requests
BACKOFF_S = (1.0, 2.0, 4.0)   # exponential backoff on transport failures


class YahooBlocked(Exception):
    """Yahoo is not serving this run: crumb blocked or persistent 401."""


# transport(url, headers) -> (http_status, body_bytes); status 0 = transport error
Transport = Callable[[str, Dict[str, str]], Tuple[int, bytes]]
Sleeper = Callable[[float], None]


def _urllib_transport_factory() -> Transport:
    """Default transport: cookie jar + redirect following, like a browser."""
    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))

    def transport(url: str, headers: Dict[str, str]) -> Tuple[int, bytes]:
        req = urllib.request.Request(url, headers=headers)
        try:
            with opener.open(req, timeout=30) as resp:
                return resp.status, resp.read()
        except urllib.error.HTTPError as exc:
            try:
                return exc.code, exc.read()
            except Exception:
                return exc.code, b""
        except Exception:
            return 0, b""

    return transport


@dataclass
class YahooSession:
    """One Yahoo session: one UA, one cookie jar, one cached crumb.

    Pass transport=/sleeper= in tests; defaults do real network.
    Every significant event is appended to attempts_log for the audit trail.
    """

    transport: Transport = field(default_factory=_urllib_transport_factory)
    sleeper: Sleeper = field(default=time.sleep)
    user_agent: str = ""
    _crumb: str = ""
    _crumb_blocked: bool = False
    _last_req: float = 0.0
    attempts_log: List[Dict[str, str]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.user_agent:
            import random
            self.user_agent = random.choice(USER_AGENTS)

    def _log(self, event: str, detail: str = "") -> None:
        self.attempts_log.append({"event": event, "detail": detail})

    def _headers(self) -> Dict[str, str]:
        return {"User-Agent": self.user_agent, "Accept": "application/json"}

    def _pace(self) -> None:
        elapsed = time.monotonic() - self._last_req
        if elapsed < MIN_INTERVAL_S:
            self.sleeper(MIN_INTERVAL_S - elapsed)
        self._last_req = time.monotonic()

    def _with_backoff(self, url: str) -> Tuple[int, bytes]:
        """GET with exponential backoff on transport-level failures only."""
        last: Tuple[int, bytes] = (0, b"")
        for i, wait in enumerate(BACKOFF_S):
            self._pace()
            status, body = self.transport(url, self._headers())
            if status != 0:
                return status, body
            last = (status, body)
            self._log("transport_error_retry", f"attempt {i + 1}/{len(BACKOFF_S)}")
            self.sleeper(wait)
        return last

    def get_crumb(self, force: bool = False) -> str:
        """Fetch (and cache) a Yahoo crumb. Raises YahooBlocked when the crumb
        endpoint itself is mitigated — do NOT hammer it, fail over instead."""
        if self._crumb and not force:
            return self._crumb
        if self._crumb_blocked and not force:
            raise YahooBlocked("crumb endpoint previously 401 (cached)")
        # Best-effort cookie seeding; fc.yahoo.com may 404 — that is fine.
        try:
            self.transport(COOKIE_URL, self._headers())
        except Exception:
            pass
        status, body = self._with_backoff(CRUMB_URL)
        if status == 401:
            self._crumb_blocked = True
            self._log("crumb_blocked", "getcrumb returned 401")
            raise YahooBlocked("getcrumb returned 401 — IP mitigated")
        if status != 200 or not body:
            self._log("crumb_failed", f"HTTP {status}")
            raise YahooBlocked(f"getcrumb returned HTTP {status}")
        self._crumb = body.decode("utf-8", errors="replace").strip()
        if not self._crumb or len(self._crumb) > 64:
            raise YahooBlocked("getcrumb returned unusable body")
        self._crumb_blocked = False
        self._log("crumb_acquired", f"len={len(self._crumb)}")
        return self._crumb

    def get(self, url: str) -> bytes:
        """GET a Yahoo API URL with crumb. On 401: refresh the crumb ONCE and
        retry; a second 401 means mitigation — raise so the caller fails over
        instead of stalling."""
        crumb = self.get_crumb()
        sep = "&" if "?" in url else "?"
        status, body = self._with_backoff(
            f"{url}{sep}crumb={urllib.parse.quote(crumb)}"
        )
        if status == 401:
            self._log("stale_crumb_401", "refreshing crumb once")
            crumb = self.get_crumb(force=True)  # may raise YahooBlocked
            status, body = self._with_backoff(
                f"{url}{sep}crumb={urllib.parse.quote(crumb)}"
            )
            if status == 401:
                self._log("crumb_refresh_failed", "second 401 — mitigated")
                raise YahooBlocked("401 persisted after crumb refresh")
        if status != 200:
            raise YahooBlocked(f"Yahoo returned HTTP {status}")
        return body
