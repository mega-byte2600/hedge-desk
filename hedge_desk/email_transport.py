"""Email transport for membership OTPs.

Keeps the membership layer independent of any specific email provider. The
server reads SMTP settings from the environment; if none are configured, the
transport falls back to a no-op console sender (dev mode) so the flow remains
testable and the site never crashes because mail is unset.
"""

from __future__ import annotations

import smtplib
from email.message import EmailMessage
from email.utils import formataddr, formatdate
from typing import Callable

SenderFn = Callable[[str, str, str], None]


def _console_send(to: str, subject: str, body: str) -> None:
    # Dev fallback: print the OTP so the flow is usable without SMTP config.
    print(f"[membership-mail] TO={to} SUBJECT={subject}\n{body}", flush=True)


class SmtpSender:
    """Sends membership email through SMTP configured via environment.

    Environment variables (set on the Render service or local .env):
      SMTP_HOST, SMTP_PORT (default 587), SMTP_USER, SMTP_PASSWORD,
      SMTP_FROM (sender address, e.g. desk@hedge-desk.com),
      SMTP_FROM_NAME (optional display name), SMTP_STARTTLS (default true).
    """

    def __init__(self, env=None) -> None:
        import os as _os

        source = env if env is not None else _os.environ
        self.host = str(source.get("SMTP_HOST", "")).strip()
        self.port = int(source.get("SMTP_PORT", "587"))
        self.user = str(source.get("SMTP_USER", "")).strip()
        self.password = str(source.get("SMTP_PASSWORD", "")).strip()
        self.from_addr = str(source.get("SMTP_FROM", "")).strip()
        self.from_name = str(source.get("SMTP_FROM_NAME", "")).strip() or "Emporion Desk"
        self.starttls = str(source.get("SMTP_STARTTLS", "true")).lower() in ("1", "true", "yes")

    @property
    def configured(self) -> bool:
        return bool(self.host and self.user and self.password and self.from_addr)

    def send(self, to: str, subject: str, body: str) -> None:
        if not self.configured:
            _console_send(to, subject, body)
            return
        msg = EmailMessage()
        msg["From"] = formataddr((self.from_name, self.from_addr))
        msg["To"] = to
        msg["Subject"] = subject
        msg["Date"] = formatdate(localtime=True)
        msg.set_content(body)
        with smtplib.SMTP(self.host, self.port, timeout=15) as client:
            if self.starttls:
                client.starttls()
            client.login(self.user, self.password)
            client.send_message(msg)


def build_sender(env: Optional[dict] = None) -> SenderFn:
    return SmtpSender(env).send
