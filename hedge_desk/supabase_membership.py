"""Supabase-backed membership store.

Implements the same public interface as ``hedge_desk.membership.MembershipStore``
(members, OTPs, sessions, invites, access decisions) but persists to Supabase
Postgres over PostgREST instead of a local SQLite file. Use this on Render free
(or any ephemeral-disk host) so members, sessions, and broker links survive
redeploys.

Design:
- stdlib only (urllib) — no new dependencies.
- The HTTP transport is injectable, so the store is deterministically testable
  without a live Supabase project.
- Security semantics are shared with the SQLite store via ``membership_base``
  (same token hashing, OTP comparison, expiry, and fail-closed access rules).
"""

from __future__ import annotations

import json
import secrets
import urllib.error
import urllib.request
from datetime import datetime, timedelta
from typing import Callable, Optional

from hedge_desk.membership_base import (
    GUEST_ACCESS_DAYS,
    MAX_LP_MEMBERS,
    OTP_TTL_SECONDS,
    ROLE_GUEST,
    ROLE_GP,
    ROLE_LP,
    ROLE_MEMBER,
    SESSION_TTL_SECONDS,
    AccessDecision,
    access_decision_for,
    hash_secret,
    utc_iso,
)

# transport(method, url, headers, body_bytes) -> (status:int, body:bytes)
Transport = Callable[[str, str, dict, Optional[bytes]], "tuple[int, bytes]"]


def _default_transport(method, url, headers, body):
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()


class Clock:
    def now(self) -> datetime:
        from datetime import timezone

        return datetime.now(timezone.utc)


class SupabaseMembershipStore:
    """Membership store persisted to Supabase (PostgREST)."""

    def __init__(
        self,
        url: str,
        service_key: str,
        *,
        secret: Optional[str] = None,
        clock: Optional[Clock] = None,
        transport: Optional[Transport] = None,
    ) -> None:
        if not url or not service_key:
            raise ValueError("SupabaseMembershipStore requires url and service_key")
        self.url = url.rstrip("/")
        self.service_key = service_key
        self._secret = (secret or "dev-secret-change-me").encode("utf-8")
        self.clock = clock or Clock()
        self._transport = transport or _default_transport

    # ---- low-level REST ----------------------------------------------------

    def _headers(self, prefer: str = "") -> dict:
        headers = {
            "apikey": self.service_key,
            "Authorization": f"Bearer {self.service_key}",
            "Content-Type": "application/json",
        }
        if prefer:
            headers["Prefer"] = prefer
        return headers

    def _call(self, method, table, query="", body=None, prefer=""):
        url = f"{self.url}/rest/v1/{table}"
        if query:
            url += "?" + query
        data = json.dumps(body).encode("utf-8") if body is not None else None
        status, raw = self._transport(method, url, self._headers(prefer), data)
        if status >= 400:
            raise RuntimeError(f"supabase {method} {table} failed: {status} {raw[:200]!r}")
        if not raw:
            return []
        try:
            return json.loads(raw)
        except Exception:
            return []

    def _hash(self, value: str) -> str:
        return hash_secret(self._secret, value)

    def _now(self) -> datetime:
        return self.clock.now()

    def close(self) -> None:
        return None

    # ---- members -----------------------------------------------------------

    def get_member(self, email: str) -> Optional[dict]:
        rows = self._call(
            "GET", "members", f"email=eq.{email.lower()}&select=*"
        )
        if not rows:
            return None
        r = rows[0]
        return {
            "email": r["email"],
            "role": r["role"],
            "created_at": r.get("created_at"),
            "guest_expires_at": r.get("guest_expires_at"),
            "subscribed": bool(r.get("subscribed")),
            "investor": bool(r.get("investor")),
            "fee_type": r.get("fee_type"),
            "fee_rate": r.get("fee_rate"),
            "invite_token": r.get("invite_token"),
            "invite_expires_at": r.get("invite_expires_at"),
        }

    def upsert_guest(self, email: str) -> dict:
        """Create (or refresh the expiry of) a guest member.

        Must never downgrade an existing role. The SQLite store's
        ``ON CONFLICT(email) DO UPDATE SET guest_expires_at`` touches only the
        expiry column, but PostgREST's ``resolution=merge-duplicates`` writes every
        column present in the payload. Sending ``role=GUEST`` therefore reset an
        existing LP or MEMBER to GUEST on every sign-in: it stripped investor
        rights, dropped the member out of ``lp_count()`` (so the 99-seat cap became
        unenforceable, because ``promote_to_lp``/``issue_lp_invite`` check a count
        that had just read 0), and rewrote ``created_at`` so the roster reordered.
        Mirrored here as: insert a new row, otherwise patch the expiry only.
        """
        email = email.lower()
        now = self._now()
        expires = now + timedelta(days=GUEST_ACCESS_DAYS)
        if self.get_member(email) is None:
            self._call(
                "POST",
                "members",
                body={
                    "email": email,
                    "role": ROLE_GUEST,
                    "created_at": utc_iso(now),
                    "guest_expires_at": utc_iso(expires),
                    "subscribed": False,
                    "investor": False,
                },
            )
        else:
            # Same single-column update the SQLite store performs. No role,
            # subscribed, investor or created_at in the payload.
            self._call(
                "PATCH",
                "members",
                f"email=eq.{email}",
                body={"guest_expires_at": utc_iso(expires)},
            )
        member = self.get_member(email)
        assert member is not None
        return member

    def ensure_gp(self, email: str) -> Optional[dict]:
        """Record (or upgrade) the configured GP identity.

        Mirrors MembershipStore.ensure_gp: the GP is configured by GP_EMAIL,
        not by a stored invite, so the row is written here. Without it the GP
        signs in as GUEST and the console's GP surfaces never render.

        The row is inserted through an explicit GET/POST/PATCH split rather than a
        merge-duplicates upsert: ``members.created_at`` is NOT NULL with no default,
        so an upsert payload that omitted it failed with a 400 on every new row and
        the operator's row was never created at all.
        """
        email = (email or "").strip().lower()
        if not email:
            return None
        existing = self.get_member(email)
        if existing is None:
            self._call(
                "POST",
                "members",
                body={
                    "email": email,
                    "role": ROLE_GP,
                    "created_at": utc_iso(self._now()),
                    "guest_expires_at": None,
                },
            )
        elif existing.get("role") != ROLE_GP:
            self._call(
                "PATCH",
                "members",
                f"email=eq.{email}",
                body={"role": ROLE_GP, "guest_expires_at": None},
            )
        return self.get_member(email)

    def set_subscribed(self, email: str) -> dict:
        """Upgrade a GUEST to self-serve subscription; never downgrade LP/GP."""
        email = email.lower()
        existing = self.get_member(email)
        if existing is None:
            self._call(
                "POST",
                "members",
                body={
                    "email": email,
                    "role": ROLE_MEMBER,
                    "created_at": utc_iso(self._now()),
                    "subscribed": True,
                    "investor": False,
                },
                prefer="resolution=merge-duplicates",
            )
        elif existing["role"] == ROLE_GUEST:
            self._call(
                "PATCH",
                "members",
                f"email=eq.{email}&role=eq.{ROLE_GUEST}",
                body={"role": ROLE_MEMBER, "subscribed": True, "guest_expires_at": None},
            )
        member = self.get_member(email)
        assert member is not None
        return member

    def promote_to_lp(self, email: str) -> dict:
        if self.lp_count() >= MAX_LP_MEMBERS:
            raise ValueError(f"LP cap of {MAX_LP_MEMBERS} reached")
        email = email.lower()
        now = self._now()
        self._call(
            "POST",
            "members",
            body={
                "email": email,
                "role": ROLE_LP,
                "created_at": utc_iso(now),
                "investor": True,
                "subscribed": False,
            },
            prefer="resolution=merge-duplicates",
        )
        self._call(
            "PATCH",
            "members",
            f"email=eq.{email}",
            body={
                "role": ROLE_LP,
                "investor": True,
                "guest_expires_at": None,
                "invite_token": None,
                "invite_expires_at": None,
            },
        )
        member = self.get_member(email)
        assert member is not None
        return member

    def set_lp_fee(self, email: str, fee_type: str, fee_rate: str) -> dict:
        self._call(
            "PATCH",
            "members",
            f"email=eq.{email.lower()}&role=eq.{ROLE_LP}",
            body={"fee_type": fee_type, "fee_rate": fee_rate},
        )
        member = self.get_member(email)
        assert member is not None
        return member

    def lp_count(self) -> int:
        rows = self._call("GET", "members", f"role=eq.{ROLE_LP}&select=email")
        return len(rows)

    def all_members(self) -> list[dict]:
        rows = self._call("GET", "members", "select=*&order=created_at")
        return [
            {
                "email": r["email"],
                "role": r["role"],
                "created_at": r.get("created_at"),
                "subscribed": bool(r.get("subscribed")),
                "investor": bool(r.get("investor")),
                "fee_type": r.get("fee_type"),
                "fee_rate": r.get("fee_rate"),
            }
            for r in rows
        ]

    # ---- invites -----------------------------------------------------------

    def issue_lp_invite(self, email: str, ttl_days: int = 14) -> dict:
        if self.lp_count() >= MAX_LP_MEMBERS:
            raise ValueError(f"LP cap of {MAX_LP_MEMBERS} reached")
        email = email.lower()
        token = secrets.token_urlsafe(32)
        now = self._now()
        expires = now + timedelta(days=ttl_days)
        self._call(
            "POST",
            "members",
            body={
                "email": email,
                "role": ROLE_LP,
                "created_at": utc_iso(now),
                "investor": True,
                "subscribed": False,
                "invite_token": token,
                "invite_expires_at": utc_iso(expires),
            },
            prefer="resolution=merge-duplicates",
        )
        self._call(
            "PATCH",
            "members",
            f"email=eq.{email}",
            body={
                "role": ROLE_LP,
                "investor": True,
                "invite_token": token,
                "invite_expires_at": utc_iso(expires),
            },
        )
        return {"email": email, "token": token, "expires_at": utc_iso(expires)}

    # ---- OTP ---------------------------------------------------------------

    def issue_otp(self, email: str, purpose: str = "signin") -> str:
        email = email.lower()
        code = secrets.token_urlsafe(12)
        now = self._now()
        self._call(
            "POST",
            "otps",
            body={
                "email": email,
                "code_hash": self._hash(code),
                "purpose": purpose,
                "expires_at": utc_iso(now + timedelta(seconds=OTP_TTL_SECONDS)),
                "used": False,
                "created_at": utc_iso(now),
            },
        )
        return code

    def verify_otp(self, email: str, code: str, purpose: str = "signin") -> bool:
        email = email.lower()
        rows = self._call(
            "GET",
            "otps",
            f"email=eq.{email}&purpose=eq.{purpose}&used=eq.false&select=id,code_hash,expires_at",
        )
        now = self._now()
        for r in rows:
            try:
                if datetime.fromisoformat(r["expires_at"]) < now:
                    continue
            except Exception:
                continue
            if hmac_compare(r["code_hash"], self._hash(code)):
                self._call("PATCH", "otps", f"id=eq.{r['id']}", body={"used": True})
                return True
        return False

    # ---- sessions ----------------------------------------------------------

    def create_session(self, email: str) -> str:
        email = email.lower()
        token = secrets.token_urlsafe(32)
        now = self._now()
        self._call(
            "POST",
            "sessions",
            body={
                "token_hash": self._hash(token),
                "email": email,
                "created_at": utc_iso(now),
                "expires_at": utc_iso(now + timedelta(seconds=SESSION_TTL_SECONDS)),
            },
        )
        return token

    def lookup_session(self, token: str) -> Optional[str]:
        rows = self._call(
            "GET", "sessions", f"token_hash=eq.{self._hash(token)}&select=email,expires_at"
        )
        if not rows:
            return None
        try:
            if datetime.fromisoformat(rows[0]["expires_at"]) < self._now():
                return None
        except Exception:
            return None
        return rows[0]["email"]

    def delete_session(self, token: str) -> None:
        self._call("DELETE", "sessions", f"token_hash=eq.{self._hash(token)}")

    # ---- access decision ---------------------------------------------------

    def access_for(self, email: str) -> AccessDecision:
        return access_decision_for(self.get_member(email), self._now())


def hmac_compare(a: str, b: str) -> bool:
    import hmac as _hmac

    return _hmac.compare_digest(a, b)


__all__ = ["SupabaseMembershipStore", "Clock"]
