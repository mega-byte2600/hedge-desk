"""Shared membership primitives used by every store backend.

Keeps constants, hashing, and the access-decision dataclass in one place so the
SQLite store and the Supabase store cannot drift apart in their security
semantics (token hashing, OTP comparison, expiry handling).
"""

from __future__ import annotations

import hashlib
import hmac
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

GUEST_ACCESS_DAYS = 31
MAX_LP_MEMBERS = 99
OTP_TTL_SECONDS = 600  # 10 minutes
SESSION_TTL_SECONDS = 45 * 86400  # 45 days (outlives guest access)
ROLE_GP = "GP"
ROLE_LP = "LP"
ROLE_MEMBER = "MEMBER"
ROLE_GUEST = "GUEST"


@dataclass
class AccessDecision:
    """Fail-closed result of an access check."""

    allowed: bool
    role: Optional[str] = None
    email: Optional[str] = None
    reason: str = ""


def utc_iso(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat()


def hash_secret(secret: bytes, value: str) -> str:
    """HMAC-SHA256 hex digest used for OTP codes and session tokens."""
    return hmac.new(secret, value.encode("utf-8"), hashlib.sha256).hexdigest()


def access_decision_for(member: Optional[dict], now: datetime) -> AccessDecision:
    """Apply the shared, fail-closed access rules to a member record."""
    if not member:
        return AccessDecision(False, reason="not_a_member")
    role = member["role"]
    if role == ROLE_GUEST:
        expires = member.get("guest_expires_at")
        if not expires:
            return AccessDecision(False, role=role, reason="guest_not_activated")
        if datetime.fromisoformat(expires) < now:
            return AccessDecision(False, role=role, reason="guest_expired")
        return AccessDecision(True, role=role, reason="guest_active")
    if role in (ROLE_LP, ROLE_MEMBER, ROLE_GP):
        return AccessDecision(True, role=role, reason=f"{role.lower()}_active")
    return AccessDecision(False, role=role, reason="unknown_role")


__all__ = [
    "GUEST_ACCESS_DAYS",
    "MAX_LP_MEMBERS",
    "OTP_TTL_SECONDS",
    "SESSION_TTL_SECONDS",
    "ROLE_GP",
    "ROLE_LP",
    "ROLE_MEMBER",
    "ROLE_GUEST",
    "AccessDecision",
    "utc_iso",
    "hash_secret",
    "access_decision_for",
]
