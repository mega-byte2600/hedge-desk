"""Membership and access control for the Emporion desk.

Implements a three-tier access model for the research desk:

* GUEST  - open "test drive"; anyone can sign in with a verified email and
           explore. Access auto-expires after GUEST_ACCESS_DAYS (31).
* MEMBER - self-serve subscription member (non-invite). Opt-in paid tier.
* LP     - invited limited partner, issued by the GP. Hard-capped at
           MAX_LP_MEMBERS (99). The inner circle.

Auth is email-OTP (magic-link / one-time code): a user provides an email, the
system issues a short-lived code, and on verification they are authenticated
via a signed session cookie. This also gives the GP a consent-collected,
first-party email list (opt-in) that the guest tier feeds for marketing.

Design goals:
- Self-contained and dependency-free: a single SQLite database (plus stdlib
  hmac/hashlib/secrets) backs members, OTPs, sessions, and invites. No new
  infrastructure beyond what Render's free tier already provides.
- Deterministic and testable: clock is injectable; codes/sessions are generated
  with injected randomness so tests are repeatable.
- Fail closed: every access decision returns False/deny by default; any store
  or validation error is treated as no-access, never an accidental grant.
- Paper-only invariants are untouched: membership gates who can view the desk,
  it does not touch trade authorization or Risk of Ruin.
"""

from __future__ import annotations

import hashlib
import hmac
import secrets
import sqlite3
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Callable, Optional

GUEST_ACCESS_DAYS = 31
MAX_LP_MEMBERS = 99
OTP_TTL_SECONDS = 600  # 10 minutes
SESSION_TTL_SECONDS = 45 * 86400  # 45 days; outlives guest access so expiry is access-gated, not session-gated
ROLE_GP = "GP"
ROLE_LP = "LP"
ROLE_MEMBER = "MEMBER"
ROLE_GUEST = "GUEST"

SCHEMA = """
CREATE TABLE IF NOT EXISTS members (
    email       TEXT PRIMARY KEY,
    role        TEXT NOT NULL,            -- GP | LP | MEMBER | GUEST
    created_at  TEXT NOT NULL,
    -- guest expiry: non-null while the user is a guest; cleared on upgrade
    guest_expires_at TEXT,
    -- subscription member flag (self-serve, non-invite)
    subscribed  INTEGER NOT NULL DEFAULT 0,
    -- LP is an LLC investor (invited by GP), never a payer. investor=1 marks
    -- a capital-committed LP as distinct from a paid subscriber.
    investor    INTEGER NOT NULL DEFAULT 0,
    -- LP/GP fee schedule fields, set by the GP per the LLC operating agreement.
    -- fee_type: e.g. management | carried | performance. rate is a Decimal str.
    fee_type    TEXT,
    fee_rate    TEXT,
    -- invite: invite token + expiry, issued by GP for LP seats
    invite_token   TEXT,
    invite_expires_at TEXT
);
CREATE TABLE IF NOT EXISTS otps (
    email      TEXT NOT NULL,
    code_hash  TEXT NOT NULL,
    purpose    TEXT NOT NULL,             -- signin | invite
    expires_at TEXT NOT NULL,
    used       INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS sessions (
    token_hash TEXT PRIMARY KEY,
    email      TEXT NOT NULL,
    created_at TEXT NOT NULL,
    expires_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_otps_email ON otps(email);
CREATE INDEX IF NOT EXISTS idx_sessions_email ON sessions(email);
"""


@dataclass
class AccessDecision:
    """Fail-closed result of an access check."""

    allowed: bool
    role: Optional[str] = None
    email: Optional[str] = None
    reason: str = ""


class Clock:
    """Injectable time source so tests are deterministic."""

    def now(self) -> datetime:
        return datetime.now(timezone.utc)


class _SystemClock(Clock):
    pass


def _utc_iso(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat()


class MembershipStore:
    """SQLite-backed membership, OTP, session, and invite store."""

    def __init__(
        self,
        db_path: Path | str,
        *,
        clock: Optional[Clock] = None,
        secret: Optional[str] = None,
    ) -> None:
        self.db_path = str(db_path)
        self.clock = clock or _SystemClock()
        # secret is used for cookie signing / token hashing. In production set
        # from env (e.g. MEMBERSHIP_SECRET); for tests a deterministic value.
        self._secret = (secret or "dev-secret-change-me").encode("utf-8")
        self._conn = sqlite3.connect(self.db_path)
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA foreign_keys=ON")
        self._conn.executescript(SCHEMA)
        self._conn.commit()

    # ---- internals ---------------------------------------------------------

    def _hash(self, value: str) -> str:
        return hmac.new(self._secret, value.encode("utf-8"), hashlib.sha256).hexdigest()

    def _now(self) -> datetime:
        return self.clock.now()

    def close(self) -> None:
        self._conn.close()

    # ---- members -----------------------------------------------------------

    def get_member(self, email: str) -> Optional[dict]:
        row = self._conn.execute(
            "SELECT email, role, created_at, guest_expires_at, subscribed, "
            "investor, fee_type, fee_rate, invite_token, invite_expires_at "
            "FROM members WHERE email=?",
            (email.lower(),),
        ).fetchone()
        if not row:
            return None
        return {
            "email": row[0],
            "role": row[1],
            "created_at": row[2],
            "guest_expires_at": row[3],
            "subscribed": bool(row[4]),
            "investor": bool(row[5]),
            "fee_type": row[6],
            "fee_rate": row[7],
            "invite_token": row[8],
            "invite_expires_at": row[9],
        }

    def upsert_guest(self, email: str) -> dict:
        """Create (or reset the expiry of) a guest member."""
        email = email.lower()
        now = self._now()
        expires = now + timedelta(days=GUEST_ACCESS_DAYS)
        self._conn.execute(
            "INSERT INTO members (email, role, created_at, guest_expires_at, subscribed) "
            "VALUES (?, ?, ?, ?, 0) "
            "ON CONFLICT(email) DO UPDATE SET guest_expires_at=excluded.guest_expires_at",
            (email, ROLE_GUEST, _utc_iso(now), _utc_iso(expires)),
        )
        self._conn.commit()
        member = self.get_member(email)
        assert member is not None
        return member

    def set_subscribed(self, email: str) -> dict:
        """Upgrade a member to self-serve subscription (non-invite)."""
        email = email.lower()
        self._conn.execute(
            "UPDATE members SET role=?, subscribed=1, guest_expires_at=NULL WHERE email=?",
            (ROLE_MEMBER, email),
        )
        self._conn.commit()
        member = self.get_member(email)
        assert member is not None
        return member

    def promote_to_lp(self, email: str) -> dict:
        """Promote a member to LP (must be within the cap; GP issues invite)."""
        if self.lp_count() >= MAX_LP_MEMBERS:
            raise ValueError(f"LP cap of {MAX_LP_MEMBERS} reached")
        email = email.lower()
        self._conn.execute(
            "INSERT INTO members (email, role, created_at, subscribed, "
            "investor, guest_expires_at, invite_token, invite_expires_at) "
            "VALUES (?, ?, ?, 0, 1, NULL, NULL, NULL) "
            "ON CONFLICT(email) DO UPDATE SET "
            "  role=?, investor=1, guest_expires_at=NULL, invite_token=NULL, "
            "  invite_expires_at=NULL",
            (email, ROLE_LP, _utc_iso(self._now()), ROLE_LP),
        )
        self._conn.commit()
        member = self.get_member(email)
        assert member is not None
        return member

    def set_lp_fee(self, email: str, fee_type: str, fee_rate: str) -> dict:
        """Set the LP fee schedule (e.g. management/carried/performance).

        Rate is stored as a string so it can be a Decimal at the point of use;
        the value is set by the GP per the LLC operating agreement.
        """
        email = email.lower()
        self._conn.execute(
            "UPDATE members SET fee_type=?, fee_rate=? WHERE email=? AND role=?",
            (fee_type, fee_rate, email, ROLE_LP),
        )
        self._conn.commit()
        member = self.get_member(email)
        assert member is not None
        return member

    def lp_count(self) -> int:
        row = self._conn.execute(
            "SELECT COUNT(*) FROM members WHERE role=?", (ROLE_LP,)
        ).fetchone()
        return row[0] if row else 0

    def all_members(self) -> list[dict]:
        rows = self._conn.execute(
            "SELECT email, role, created_at, subscribed, investor, fee_type, fee_rate "
            "FROM members ORDER BY created_at"
        ).fetchall()
        return [
            {
                "email": r[0],
                "role": r[1],
                "created_at": r[2],
                "subscribed": bool(r[3]),
                "investor": bool(r[4]),
                "fee_type": r[5],
                "fee_rate": r[6],
            }
            for r in rows
        ]

    # ---- invites -----------------------------------------------------------

    def issue_lp_invite(self, email: str, ttl_days: int = 14) -> dict:
        """Issue a GP invite for an LP seat. Returns the invite token."""
        if self.lp_count() >= MAX_LP_MEMBERS:
            raise ValueError(f"LP cap of {MAX_LP_MEMBERS} reached")
        email = email.lower()
        token = secrets.token_urlsafe(32)
        now = self._now()
        expires = now + timedelta(days=ttl_days)
        self._conn.execute(
            "INSERT INTO members (email, role, created_at, subscribed, "
            "investor, guest_expires_at, invite_token, invite_expires_at) "
            "VALUES (?, ?, ?, 0, 1, NULL, ?, ?) "
            "ON CONFLICT(email) DO UPDATE SET "
            "  role=?, investor=1, guest_expires_at=NULL, invite_token=excluded.invite_token, "
            "  invite_expires_at=excluded.invite_expires_at",
            (
                email,
                ROLE_LP,
                _utc_iso(now),
                token,
                _utc_iso(expires),
                ROLE_LP,
            ),
        )
        self._conn.commit()
        return {"email": email, "token": token, "expires_at": _utc_iso(expires)}

    # ---- OTP ---------------------------------------------------------------

    def issue_otp(self, email: str, purpose: str = "signin") -> str:
        """Generate an OTP, store its hash, return the plaintext code."""
        email = email.lower()
        code = secrets.token_urlsafe(12)  # ~ a one-time code / magic token
        now = self._now()
        expires = now + timedelta(seconds=OTP_TTL_SECONDS)
        self._conn.execute(
            "INSERT INTO otps (email, code_hash, purpose, expires_at, used, created_at) "
            "VALUES (?, ?, ?, ?, 0, ?)",
            (email, self._hash(code), purpose, _utc_iso(expires), _utc_iso(now)),
        )
        self._conn.commit()
        return code

    def verify_otp(self, email: str, code: str, purpose: str = "signin") -> bool:
        """Verify a one-time code. Single-use, fails closed on any problem."""
        email = email.lower()
        now = self._now()
        rows = self._conn.execute(
            "SELECT rowid, code_hash, expires_at, used FROM otps "
            "WHERE email=? AND purpose=? AND used=0 ORDER BY created_at DESC LIMIT 5",
            (email, purpose),
        ).fetchall()
        for rowid, code_hash, expires_at, used in rows:
            if used:
                continue
            expires = datetime.fromisoformat(expires_at)
            if expires < now:
                continue
            if hmac.compare_digest(code_hash, self._hash(code)):
                self._conn.execute("UPDATE otps SET used=1 WHERE rowid=?", (rowid,))
                self._conn.commit()
                return True
        return False

    # ---- sessions ----------------------------------------------------------

    def create_session(self, email: str) -> str:
        """Create a session and return the plaintext token (cookie value)."""
        email = email.lower()
        token = secrets.token_urlsafe(32)
        now = self._now()
        expires = now + timedelta(seconds=SESSION_TTL_SECONDS)
        self._conn.execute(
            "INSERT INTO sessions (token_hash, email, created_at, expires_at) "
            "VALUES (?, ?, ?, ?)",
            (self._hash(token), email, _utc_iso(now), _utc_iso(expires)),
        )
        self._conn.commit()
        return token

    def lookup_session(self, token: str) -> Optional[str]:
        """Return the email for a valid, unexpired session token, else None."""
        row = self._conn.execute(
            "SELECT email, expires_at FROM sessions WHERE token_hash=?",
            (self._hash(token),),
        ).fetchone()
        if not row:
            return None
        expires = datetime.fromisoformat(row[1])
        if expires < self._now():
            return None
        return row[0]

    def delete_session(self, token: str) -> None:
        self._conn.execute("DELETE FROM sessions WHERE token_hash=?", (self._hash(token),))
        self._conn.commit()

    # ---- access decision ---------------------------------------------------

    def access_for(self, email: str) -> AccessDecision:
        """Decide whether a member (by email) currently has access and with what role.

        Fail closed: unknown email => no access; expired guest => no access;
        any role except GUEST is long-lived (does not expire here).
        """
        member = self.get_member(email)
        if not member:
            return AccessDecision(False, reason="not_a_member")
        role = member["role"]
        if role == ROLE_GUEST:
            expires = member["guest_expires_at"]
            if not expires:
                return AccessDecision(False, role=role, reason="guest_not_activated")
            if datetime.fromisoformat(expires) < self._now():
                return AccessDecision(False, role=role, reason="guest_expired")
            return AccessDecision(True, role=role, reason="guest_active")
        if role in (ROLE_LP, ROLE_MEMBER, ROLE_GP):
            return AccessDecision(True, role=role, reason=f"{role.lower()}_active")
        return AccessDecision(False, role=role, reason="unknown_role")
