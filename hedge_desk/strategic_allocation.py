"""Deterministic diversified-allocation and valuation concentration controls."""

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from hashlib import sha256
import json
from typing import Tuple


ALLOCATION_POLICY_VERSION = "diversification-cape-policy-1.0.0"


class AssetClass(str, Enum):
    US_EQUITY = "US_EQUITY"
    INTERNATIONAL_EQUITY = "INTERNATIONAL_EQUITY"
    FIXED_INCOME = "FIXED_INCOME"
    REAL_ASSET = "REAL_ASSET"
    CASH = "CASH"


@dataclass(frozen=True)
class AllocationWeight:
    asset_class: AssetClass
    weight: Decimal


@dataclass(frozen=True)
class StrategicAllocationPolicy:
    minimum_distinct_asset_classes: int = 4
    maximum_single_asset_class_weight: Decimal = Decimal("0.40")
    high_cape_threshold: Decimal = Decimal("30")
    high_cape_us_equity_maximum: Decimal = Decimal("0.30")


@dataclass(frozen=True)
class StrategicAllocationGate:
    admissible: bool
    reason_codes: Tuple[str, ...]
    us_equity_weight: Decimal
    largest_asset_class_weight: Decimal
    cape_ratio: Decimal
    policy_version: str = ALLOCATION_POLICY_VERSION
    risk_of_ruin_calculated: bool = False
    trade_authorized: bool = False
    artifact_sha256: str = ""


def evaluate_strategic_allocation(
    weights: Tuple[AllocationWeight, ...],
    cape_ratio: Decimal,
    policy: StrategicAllocationPolicy = StrategicAllocationPolicy(),
) -> StrategicAllocationGate:
    if not weights:
        raise ValueError("strategic allocation cannot be empty")
    classes = [item.asset_class for item in weights]
    if len(classes) != len(set(classes)):
        raise ValueError("strategic allocation asset classes must be unique")
    if (
        policy.minimum_distinct_asset_classes <= 0
        or not Decimal("0") < policy.maximum_single_asset_class_weight <= Decimal("1")
        or policy.high_cape_threshold <= 0
        or not Decimal("0") <= policy.high_cape_us_equity_maximum <= Decimal("1")
    ):
        raise ValueError("strategic allocation policy invalid")
    reasons = []
    if any(item.weight < 0 or item.weight > 1 for item in weights):
        reasons.append("ALLOCATION_WEIGHT_INVALID")
    total = sum((item.weight for item in weights), Decimal("0"))
    if total != Decimal("1"):
        reasons.append("ALLOCATION_WEIGHTS_DO_NOT_SUM_TO_ONE")
    positive = sum(item.weight > 0 for item in weights)
    if positive < policy.minimum_distinct_asset_classes:
        reasons.append("ALLOCATION_DIVERSIFICATION_INSUFFICIENT")
    largest = max(item.weight for item in weights)
    if largest > policy.maximum_single_asset_class_weight:
        reasons.append("ASSET_CLASS_CONCENTRATION_LIMIT")
    if cape_ratio <= 0:
        reasons.append("PORTFOLIO_CAPE_INVALID")
    us_equity = next(
        (item.weight for item in weights if item.asset_class is AssetClass.US_EQUITY),
        Decimal("0"),
    )
    if (
        cape_ratio >= policy.high_cape_threshold
        and us_equity > policy.high_cape_us_equity_maximum
    ):
        reasons.append("HIGH_CAPE_US_EQUITY_CONCENTRATION")
    reason_codes = tuple(sorted(set(reasons)))
    payload = {
        "cape_ratio": str(cape_ratio),
        "policy": {
            "high_cape_threshold": str(policy.high_cape_threshold),
            "high_cape_us_equity_maximum": str(policy.high_cape_us_equity_maximum),
            "maximum_single_asset_class_weight": str(policy.maximum_single_asset_class_weight),
            "minimum_distinct_asset_classes": policy.minimum_distinct_asset_classes,
            "version": ALLOCATION_POLICY_VERSION,
        },
        "reason_codes": list(reason_codes),
        "weights": [
            {"asset_class": item.asset_class.value, "weight": str(item.weight)}
            for item in sorted(weights, key=lambda value: value.asset_class.value)
        ],
    }
    artifact_hash = sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return StrategicAllocationGate(
        not reason_codes, reason_codes, us_equity, largest, cape_ratio,
        ALLOCATION_POLICY_VERSION, False, False, artifact_hash,
    )
