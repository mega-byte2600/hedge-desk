"""Fail-closed Schwab access-token lifecycle primitives.

The manager deliberately requires a verified refresh-token age limit and an
atomic persistence callback. It will not refresh a token using guessed policy
or make an API call before the refreshed state has been persisted.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Callable, Optional


class SchwabTokenError(RuntimeError):
    """Token lifecycle failure with a stable, non-secret reason code."""

    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


@dataclass(frozen=True)
class SchwabTokenState:
    access_token: str = field(repr=False)
    refresh_token: str = field(repr=False)
    access_expires_at: datetime
    refresh_issued_at: datetime
    scope: str
    updated_at: datetime
    selected_account_hash: str = field(default="", repr=False)

    def __post_init__(self) -> None:
        if not self.access_token or not self.refresh_token:
            raise ValueError("both Schwab tokens are required")
        for value in (self.access_expires_at, self.refresh_issued_at, self.updated_at):
            if value.tzinfo is None or value.utcoffset() is None:
                raise ValueError("token timestamps must be timezone-aware")
        if not self.scope:
            raise ValueError("token scope metadata is required")


Refresh = Callable[[str], dict]
Persist = Callable[[SchwabTokenState], None]


class SchwabTokenManager:
    def __init__(
        self,
        *,
        refresh: Refresh,
        persist: Persist,
        refresh_token_max_age: Optional[timedelta],
        refresh_before: timedelta = timedelta(minutes=2),
    ) -> None:
        if refresh_before < timedelta(0):
            raise ValueError("refresh_before cannot be negative")
        if refresh_token_max_age is not None and refresh_token_max_age <= timedelta(0):
            raise ValueError("refresh token maximum age must be positive")
        self._refresh = refresh
        self._persist = persist
        self._refresh_token_max_age = refresh_token_max_age
        self._refresh_before = refresh_before

    def access_token(
        self,
        state: SchwabTokenState,
        now: Optional[datetime] = None,
        *,
        force_refresh: bool = False,
    ) -> str:
        """Return a usable access token, persisting refreshed state first."""
        instant = now or datetime.now(timezone.utc)
        if instant.tzinfo is None or instant.utcoffset() is None:
            raise ValueError("now must be timezone-aware")
        if not force_refresh and state.access_expires_at > instant + self._refresh_before:
            return state.access_token

        if self._refresh_token_max_age is None:
            raise SchwabTokenError("refresh_lifetime_unverified")
        age = instant - state.refresh_issued_at
        if age < timedelta(0) or age >= self._refresh_token_max_age:
            raise SchwabTokenError("reauthentication_required")

        result = self._refresh(state.refresh_token)
        if not isinstance(result, dict) or result.get("status") != "ok":
            code = result.get("error") if isinstance(result, dict) else None
            if code == "reauthentication_required":
                raise SchwabTokenError("reauthentication_required")
            raise SchwabTokenError("refresh_failed")

        access = result.get("access_token")
        expires_in = result.get("expires_in")
        if (
            not isinstance(access, str)
            or not access
            or isinstance(expires_in, bool)
            or not isinstance(expires_in, (int, float))
            or expires_in <= 0
        ):
            raise SchwabTokenError("unexpected_refresh_response")
        rotated_refresh = result.get("refresh_token") or state.refresh_token
        if not isinstance(rotated_refresh, str) or not rotated_refresh:
            raise SchwabTokenError("unexpected_refresh_response")
        rotated = rotated_refresh != state.refresh_token
        scope = result.get("scope") or state.scope
        if not isinstance(scope, str) or not scope:
            raise SchwabTokenError("unexpected_refresh_response")
        new_state = SchwabTokenState(
            access_token=access,
            refresh_token=rotated_refresh,
            access_expires_at=instant + timedelta(seconds=float(expires_in)),
            refresh_issued_at=instant if rotated else state.refresh_issued_at,
            scope=scope,
            updated_at=instant,
            selected_account_hash=state.selected_account_hash,
        )
        try:
            self._persist(new_state)
        except Exception as exc:
            raise SchwabTokenError("token_persistence_failed") from exc
        return new_state.access_token


__all__ = ["SchwabTokenError", "SchwabTokenState", "SchwabTokenManager"]
