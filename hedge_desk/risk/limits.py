"""Immutable desk-wide risk limits (single source of truth).

SOUL.md order 7: the 2%-of-equity max-loss rule is immutable. Every module that
enforces a per-trade loss limit imports this constant, so the limit cannot
drift between the risk gate and position sizing (ADR-0008, decision C2).
"""

from decimal import Decimal

SOUL_MAX_LOSS_FRACTION_EQUITY = Decimal("0.02")
