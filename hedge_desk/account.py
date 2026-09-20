"""Real account-equity input for the survivability gate (privacy-safe).

The desk's survivability reading is INDETERMINATE until a real account balance is
wired. This module reads the GP's account equity from a LOCAL, gitignored source
(env var ACCOUNT_EQUITY or data/account_equity.txt) so the survivability gate can
evaluate PASS/FAIL instead of INDETERMINATE.

Privacy and honesty:
- The equity value is NEVER committed, logged, or shown raw in any report. It is
  read at runtime and only its derived readings (capital utilization %, survivability
  PASS/FAIL) are surfaced.
- Absent a real value, this returns None and the gate stays INDETERMINATE (fail
  closed) — never a fabricated balance.
- This is the GP's own account input, not a broker connection and not an order.
"""

from __future__ import annotations

import os
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Optional

ACCOUNT_EQUITY_ENV = "ACCOUNT_EQUITY"
ACCOUNT_EQUITY_FILE = Path("data/account_equity.txt")


def read_account_equity(
    env: Optional[str] = None,
    path: Optional[Path] = None,
) -> Optional[Decimal]:
    """Return the real account equity as a Decimal, or None if not provided.

    Reads from the env var first, then the gitignored file. A missing, empty, or
    non-numeric value returns None (the gate stays INDETERMINATE) — never a
    fabricated balance. ``env``/``path`` are injectable for deterministic tests.
    """
    raw = env if env is not None else os.environ.get(ACCOUNT_EQUITY_ENV, "")
    if not raw or not str(raw).strip():
        p = path if path is not None else ACCOUNT_EQUITY_FILE
        try:
            raw = p.read_text(encoding="utf-8").strip()
        except (OSError, UnicodeError):
            raw = ""
    if not raw:
        return None
    try:
        value = Decimal(str(raw).strip())
    except (InvalidOperation, ValueError):
        return None
    if not value.is_finite() or value <= 0:
        return None
    return value


__all__ = ["ACCOUNT_EQUITY_ENV", "ACCOUNT_EQUITY_FILE", "read_account_equity"]