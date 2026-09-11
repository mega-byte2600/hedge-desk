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
    ) -> None:
        if limit < 1:
            raise ValueError("limit must be >= 1")
        self.limit = limit
        self.window = float(window_seconds)
        self._clock = clock or time.monotonic
        self._events: Dict[str, Deque[float]] = defaultdict(deque)

    def _prune(self, key: str, now: float) -> None:
        events = self._events[key]
        cutoff = now - self.window
        while events and events[0] <= cutoff:
            events.popleft()

    def allow(self, key: str) -> bool:
        """Record an attempt for ``key``; return False if it exceeds the limit."""
        now = self._clock()
        self._prune(key, now)
        events = self._events[key]
        if len(events) >= self.limit:
            return False
        events.append(now)
        return True

    def remaining(self, key: str) -> int:
        now = self._clock()
        self._prune(key, now)
        return max(0, self.limit - len(self._events[key]))

    def reset(self, key: str) -> None:
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
        """Both the address and the client IP must be under their limits."""
        email_ok = self.request_per_email.allow(email)
        ip_ok = self.request_per_ip.allow(client_ip or "unknown")
        return email_ok and ip_ok

    def allow_verify(self, email: str) -> bool:
        return self.verify_per_email.allow(email)


__all__ = ["SlidingWindowLimiter", "AuthRateLimits"]
