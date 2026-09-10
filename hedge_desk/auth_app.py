"""HTTP auth + membership endpoints for the Emporion desk.

WSGI-level handlers that connect the membership store and email transport to
HTTP requests. Kept separate from the main server module so the auth surface
is testable in isolation and the report-serving server stays uncluttered.

Endpoints:
  POST /api/auth/request  {email}          -> issue OTP, send email, 202
  POST /api/auth/verify   {email, code}    -> create session cookie, 200
  POST /api/auth/logout   (session cookie) -> revoke session, 200
  GET  /api/auth/me       (session cookie) -> current role/status, 200
  GET  /api/auth/cap      (session cookie, GP) -> LP count + cap, 200
  POST /api/auth/invite   {email} (GP)     -> issue LP invite, 201
  POST /api/auth/subscribe {email}         -> self-serve member, 200

The guest "test drive" tier is the open default: anyone with a verified email
gets GUEST access that expires after 31 days. That consent-collected email
becomes the GP's opt-in marketing list.
"""

from __future__ import annotations

import json
import os
from http.cookies import SimpleCookie
from typing import Callable, Optional
from urllib.parse import parse_qs
from pathlib import Path

from hedge_desk.membership import (
    MAX_LP_MEMBERS,
    MembershipStore,
)
from hedge_desk.email_transport import build_sender

SESSION_COOKIE = "emporion_session"
# Where the SQLite DB lives. In production this should point at a path on a
# persistent volume; on Render free the instance disk is ephemeral, so
# configure MEMBERSHIP_DB to a persistent store (Supabase/Turso/DB) or accept
# reset-on-redeploy for the guest tier only.
MEMBERSHIP_DB = os.getenv("MEMBERSHIP_DB", str(Path(__file__).resolve().parents[1] / "data" / "membership.db"))
MEMBERSHIP_SECRET = os.getenv("MEMBERSHIP_SECRET", "dev-secret-change-me")
ACCESS_DAYS = int(os.getenv("GUEST_ACCESS_DAYS", "31"))


def _read_json(environ) -> dict:
    try:
        length = int(environ.get("CONTENT_LENGTH") or "0")
        body = environ["wsgi.input"].read(min(length, 1_000_000)).decode("utf-8")
        payload = json.loads(body or "{}")
        if not isinstance(payload, dict):
            raise ValueError("expected object")
        return payload
    except Exception:
        return {}


def _cookie_from(environ) -> str:
    raw = environ.get("HTTP_COOKIE", "")
    if not raw:
        return ""
    cookie = SimpleCookie()
    try:
        cookie.load(raw)
    except Exception:
        return ""
    morsel = cookie.get(SESSION_COOKIE)
    return morsel.value if morsel else ""


def _json_response(start_response, payload, status="200 OK"):
    body = json.dumps(payload).encode("utf-8")
    start_response(
        status,
        [
            ("Content-Type", "application/json"),
            ("Content-Length", str(len(body))),
            ("Cache-Control", "no-store"),
        ],
    )
    return [body]


def _set_session_cookie(start_response, token):
    start_response(
        "200 OK",
        [
            ("Content-Type", "application/json"),
            ("Set-Cookie", f"{SESSION_COOKIE}={token}; HttpOnly; Path=/; SameSite=Lax"),
        ],
    )


def make_auth_app(
    store: MembershipStore,
    sender: Optional[Callable[[str, str, str], None]] = None,
    gp_email: Optional[str] = None,
):
    """Build a WSGI auth dispatch for the given store + email sender.

    gp_email is the GP's address; only it may issue LP invites.
    """
    send = sender or build_sender()

    def dispatch(environ, start_response):
        path = environ.get("PATH_INFO", "")
        method = environ.get("REQUEST_METHOD", "GET")
        session_token = _cookie_from(environ)
        email = store.lookup_session(session_token) if session_token else None

        # ---- request OTP ---------------------------------------------------
        if path == "/api/auth/request" and method == "POST":
            data = _read_json(environ)
            email_addr = str(data.get("email", "")).strip().lower()
            if "@" not in email_addr or "." not in email_addr:
                return _json_response(start_response, {"error": "invalid_email"}, "400 Bad Request")
            # Any verified email can start as a GUEST (open test drive). LP/MEMBER
            # status is preserved if the account already has it.
            store.upsert_guest(email_addr)
            code = store.issue_otp(email_addr, purpose="signin")
            try:
                send(
                    email_addr,
                    "Your Emporion desk sign-in code",
                    f"Your one-time sign-in code is:\n\n{code}\n\n"
                    f"It expires in 10 minutes. If you didn't request this, ignore it.\n",
                )
            except Exception as exc:  # email is not an access control; don't fail signup
                return _json_response(
                    start_response,
                    {"error": "mail_unavailable", "detail": str(exc)},
                    "503 Service Unavailable",
                )
            return _json_response(
                start_response, {"status": "otp_sent", "email": email_addr}, "202 Accepted"
            )

        # ---- verify OTP ----------------------------------------------------
        if path == "/api/auth/verify" and method == "POST":
            data = _read_json(environ)
            email_addr = str(data.get("email", "")).strip().lower()
            code = str(data.get("code", "")).strip()
            if not store.verify_otp(email_addr, code, purpose="signin"):
                return _json_response(start_response, {"error": "invalid_code"}, "401 Unauthorized")
            decision = store.access_for(email_addr)
            if not decision.allowed:
                return _json_response(start_response, {"error": decision.reason}, "403 Forbidden")
            token = store.create_session(email_addr)
            _set_session_cookie(start_response, token)
            return [json.dumps({"status": "ok", "role": decision.role}).encode("utf-8")]

        # ---- logout --------------------------------------------------------
        if path == "/api/auth/logout" and method == "POST":
            if session_token:
                store.delete_session(session_token)
            return _json_response(start_response, {"status": "logged_out"})

        # ---- me ------------------------------------------------------------
        if path == "/api/auth/me" and method == "GET":
            if not email:
                return _json_response(start_response, {"authenticated": False})
            decision = store.access_for(email)
            return _json_response(
                start_response,
                {
                    "authenticated": True,
                    "email": email,
                    "role": decision.role,
                    "access": decision.allowed,
                    "reason": decision.reason,
                },
            )

        # ---- cap (GP only) -------------------------------------------------
        if path == "/api/auth/cap" and method == "GET":
            if not email or email.lower() != (gp_email or "").lower():
                return _json_response(start_response, {"error": "unauthorized"}, "403 Forbidden")
            return _json_response(
                start_response,
                {"lp_count": store.lp_count(), "max_lp": MAX_LP_MEMBERS},
            )

        # ---- invite LP (GP only) -------------------------------------------
        if path == "/api/auth/invite" and method == "POST":
            if not email or email.lower() != (gp_email or "").lower():
                return _json_response(start_response, {"error": "unauthorized"}, "403 Forbidden")
            data = _read_json(environ)
            invite_email = str(data.get("email", "")).strip().lower()
            try:
                invite = store.issue_lp_invite(invite_email)
            except ValueError as exc:
                return _json_response(start_response, {"error": str(exc)}, "409 Conflict")
            return _json_response(start_response, {"status": "invited", **invite}, "201 Created")

        # ---- subscribe (self-serve, non-invite) -----------------------------
        if path == "/api/auth/subscribe" and method == "POST":
            data = _read_json(environ)
            email_addr = str(data.get("email", "")).strip().lower()
            if not email or email.lower() != email_addr:
                # require the requester to be authenticated as that email
                return _json_response(start_response, {"error": "unauthorized"}, "403 Forbidden")
            store.set_subscribed(email_addr)
            return _json_response(start_response, {"status": "subscribed", "role": "MEMBER"})

        return _json_response(start_response, {"error": "not_found"}, "404 Not Found")

    return dispatch


def default_membership_store() -> MembershipStore:
    Path(MEMBERSHIP_DB).parent.mkdir(parents=True, exist_ok=True)
    return MembershipStore(MEMBERSHIP_DB, secret=MEMBERSHIP_SECRET)


__all__ = [
    "SESSION_COOKIE",
    "MEMBERSHIP_DB",
    "make_auth_app",
    "default_membership_store",
]
