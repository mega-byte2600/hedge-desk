"""Tier-based data access policy.

Maps a membership role to a data entitlement level:

* GUEST  -> synthetic only (the public "test drive" — never real market or
            personal data).
* MEMBER -> real market data + their own broker-linked data (read-only first).
* LP     -> investor; real market data + broker + full desk service.
* GP     -> operator; everything.

This is a pure policy layer: it decides WHAT a role may see, not HOW data is
fetched. Endpoints call ``data_tier_for(role)`` and serve the corresponding
payload. It is fail-closed: unknown roles get the most restrictive tier.
"""

from __future__ import annotations

from enum import Enum
from typing import Optional


class DataTier(str, Enum):
    SYNTHETIC = "synthetic"          # guest test-drive
    REAL = "real"                    # member / subscriber
    FULL = "full"                    # LP investor / GP operator


# Roles are additive tiers: LP sees everything MEMBER does, GP sees everything LP does.
_TIER_BY_ROLE = {
    "GUEST": DataTier.SYNTHETIC,
    "MEMBER": DataTier.REAL,
    "LP": DataTier.FULL,
    "GP": DataTier.FULL,
}


def data_tier_for(role: Optional[str]) -> DataTier:
    """Return the data tier a role may access. Fail closed to SYNTHETIC."""
    if not role:
        return DataTier.SYNTHETIC
    return _TIER_BY_ROLE.get(role.upper(), DataTier.SYNTHETIC)


def can_access_real_data(role: Optional[str]) -> bool:
    """Whether the role may see real (non-synthetic) market data."""
    return data_tier_for(role) in (DataTier.REAL, DataTier.FULL)


def is_investor(role: Optional[str]) -> bool:
    """Whether the role is a capital-committed investor (LP/GP)."""
    return data_tier_for(role) == DataTier.FULL


__all__ = [
    "DataTier",
    "data_tier_for",
    "can_access_real_data",
    "is_investor",
]
