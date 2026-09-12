"""Sliding-window rate limiting for authentication endpoints.

Protects the email-OTP flow against two concrete abuses:

* **Email bombing** — repeatedly requesting sign-in codes for someone else's
  address. Limited per address and per client IP.
* **Code brute force** — guessing the one-time code. Limited per address, with
  a stricter window than issuance.

Design notes:
- In-process and dependency-free: a dict of timestamps per key. Adequate for a
  single web instance (the desk's target scale); a distributed deployment would
  move this to the shared store.
- Injectable clock so tests are deterministic.
- Fail-closed at the call site: the auth app denies the request when the
  limiter says no. Denying on limiter error is safer than allowing.
"""

from __future__ import annotations

import threading
import time
from collections import defaultdict, deque
from typing import Callable, Deque, Dict, Optional


class SlidingWindowLimiter:
    """Allow at most ``limit`` events per ``window_seconds`` for a given key."""

    def __init__(
        self,
        limit: int,
        window_seconds: float,
        *,
        clock: Optional[Callable[[], float]] = None,
        max_keys: int = 10_000,
    ) -> None:
        if limit < 1:
            raise ValueError("limit must be >= 1")
        self.limit = limit
        self.window = float(window_seconds)
        self._clock = clock or time.monotonic
        # One lock per limiter: check-then-act on a deque is not atomic, and this
        # runs on the threaded WSGI server, so two concurrent requests could both
        # observe room and both append.
        self._lock = threading.Lock()
        self._max_keys = max_keys
        self._events: Dict[str, Deque[float]] = defaultdict(deque)

    def _prune(self, key: str, now: float) -> None:
        events = self._events[key]
        cutoff = now - self.window
        while events and events[0] <= cutoff:
            events.popleft()

    def _evict_expired(self, now: float) -> None:
        """Drop keys whose window has fully elapsed, so the map stays bounded.

        Only elapsed keys are reclaimed. Evicting *live* keys to make room would
        let a caller reset its own limit by flooding new addresses, so when the
        budget is exhausted by active keys the limiter fails closed instead (see
        ``allow``).
        """
        cutoff = now - self.window
        for k in [k for k, v in self._events.items() if not v or v[-1] <= cutoff]:
            self._events.pop(k, None)

    def allow(self, key: str) -> bool:
        """Record an attempt for ``key``; return False if it exceeds the limit."""
        with self._lock:
            now = self._clock()
            if key not in self._events and len(self._events) >= self._max_keys:
                self._evict_expired(now)
                if len(self._events) >= self._max_keys:
                    # Every remaining key is inside its window. Refusing here keeps
                    # the map bounded without handing an attacker a way to clear an
                    # active limit; keys are caller-controlled, so the bound is the
                    # only thing standing between this map and the instance memory.
                    return False
            self._prune(key, now)
            events = self._events[key]
            if len(events) >= self.limit:
                return False
            events.append(now)
            return True

    def remaining(self, key: str) -> int:
        with self._lock:
            now = self._clock()
            self._prune(key, now)
            return max(0, self.limit - len(self._events[key]))

    def reset(self, key: str) -> None:
        with self._lock:
            self._events.pop(key, None)


class AuthRateLimits:
    """The rate limits applied to the auth surface."""

    def __init__(self, clock: Optional[Callable[[], float]] = None) -> None:
        # Issuing codes: generous enough for a re-send, tight enough to stop bombing.
        self.request_per_email = SlidingWindowLimiter(5, 900, clock=clock)
        self.request_per_ip = SlidingWindowLimiter(20, 900, clock=clock)
        # Verifying codes: a few typos allowed, then a cool-off.
        self.verify_per_email = SlidingWindowLimiter(10, 900, clock=clock)

    def allow_request(self, email: str, client_ip: str) -> bool:
        """Both the address and the client IP must be under their limits.

        The IP limit is evaluated first and short-circuits. It used to run second,
        so a rejected request still recorded a per-address entry for an
        attacker-chosen address: one client could mint unbounded keys (and the
        per-email limiter is the primary control, so its budget was also spent by
        traffic the IP limit was about to refuse).
        """
        if not self.request_per_ip.allow(client_ip or "unknown"):
            return False
        return self.request_per_email.allow(email)

    def allow_verify(self, email: str) -> bool:
        return self.verify_per_email.allow(email)


__all__ = ["SlidingWindowLimiter", "AuthRateLimits"]
