"""Executable-side economics for defined-risk vertical credit spreads."""

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from decimal import Decimal
from enum import Enum
from typing import Tuple


CONTRACT_MULTIPLIER = 100
SPREAD_MODEL_ID = "vertical-credit-spread-executable-side"
SPREAD_MODEL_VERSION = "1.0.0"


class OptionType(str, Enum):
    CALL = "call"
    PUT = "put"


@dataclass(frozen=True)
class OptionQuote:
    contract_id: str
    underlying: str
    option_type: OptionType
    strike: Decimal
    expiration: date
    bid: Decimal
    ask: Decimal
    bid_size: int
    ask_size: int
    quoted_at: datetime
    source_id: str

    def __post_init__(self) -> None:
        if not self.contract_id or not self.underlying or not self.source_id:
            raise ValueError("quote identity and source are required")
        if self.quoted_at.tzinfo is None:
            raise ValueError("quote timestamp must be timezone-aware")
        if self.strike <= 0 or self.bid < 0 or self.ask <= 0:
            raise ValueError("strike and quote values must be valid")
        if self.ask < self.bid:
            raise ValueError("crossed option quote is prohibited")
        if self.bid_size <= 0 or self.ask_size <= 0:
            raise ValueError("executable quote sizes must be positive")


@dataclass(frozen=True)
class VerticalCreditSpread:
    spread_id: str
    short_leg: OptionQuote
    long_leg: OptionQuote
    quantity: int
    commission_per_contract: Decimal
    quote_tolerance_seconds: int = 2
    planned_exit_days_before_expiration: int = 7

    def __post_init__(self) -> None:
        if not self.spread_id or self.quantity <= 0:
            raise ValueError("spread identity and positive quantity are required")
        if self.commission_per_contract < 0:
            raise ValueError("commission cannot be negative")
        if self.quote_tolerance_seconds < 0:
            raise ValueError("quote tolerance cannot be negative")
        if self.planned_exit_days_before_expiration <= 0:
            raise ValueError("planned exit offset must be positive")


@dataclass(frozen=True)
class VerticalSpreadCalculation:
    spread_id: str
    model_id: str
    model_version: str
    calculated_at: datetime
    input_contract_ids: Tuple[str, str]
    quote_timestamps: Tuple[datetime, datetime]
    expiration_date: date
    days_to_expiration: int
    planned_exit_days_before_expiration: int
    planned_exit_date: date
    quantity: int
    contract_multiplier: int
    width_per_share: Decimal
    short_sale_price_per_share: Decimal
    long_purchase_price_per_share: Decimal
    gross_credit: Decimal
    total_commission: Decimal
    net_credit: Decimal
    maximum_loss: Decimal
    break_even: Decimal
    return_on_risk: Decimal


def calculate_vertical_credit_spread(
    spread: VerticalCreditSpread,
    calculated_at: datetime,
) -> VerticalSpreadCalculation:
    """Calculate a credit spread using only executable bid/ask sides.

    The short leg is sold at its bid and the long leg is bought at its ask.
    No midpoint, probability, Greek, or agent-generated estimate is used.
    """
    if calculated_at.tzinfo is None:
        raise ValueError("calculation timestamp must be timezone-aware")

    short = spread.short_leg
    long = spread.long_leg
    if short.underlying != long.underlying:
        raise ValueError("spread legs must share an underlying")
    if short.option_type is not long.option_type:
        raise ValueError("spread legs must share an option type")
    if short.expiration != long.expiration:
        raise ValueError("spread legs must share an expiration")
    if short.source_id != long.source_id:
        raise ValueError("spread legs must share a validated quote source")

    timestamp_gap = abs((short.quoted_at - long.quoted_at).total_seconds())
    if timestamp_gap > spread.quote_tolerance_seconds:
        raise ValueError("spread leg quotes are not timestamp-compatible")
    if calculated_at < short.quoted_at or calculated_at < long.quoted_at:
        raise ValueError("calculation cannot precede quote availability")
    days_to_expiration = (short.expiration - calculated_at.date()).days
    if days_to_expiration <= spread.planned_exit_days_before_expiration:
        raise ValueError("candidate has reached its planned pre-expiration exit window")
    planned_exit_date = short.expiration - timedelta(
        days=spread.planned_exit_days_before_expiration
    )
    if spread.quantity > min(short.bid_size, long.ask_size):
        raise ValueError("spread quantity exceeds executable displayed size")

    if short.option_type is OptionType.PUT:
        if short.strike <= long.strike:
            raise ValueError("put credit spread requires short strike above long")
        width = short.strike - long.strike
    else:
        if short.strike >= long.strike:
            raise ValueError("call credit spread requires short strike below long")
        width = long.strike - short.strike

    credit_per_share = short.bid - long.ask
    if credit_per_share <= 0:
        raise ValueError("spread does not provide executable positive credit")

    multiplier = Decimal(CONTRACT_MULTIPLIER)
    quantity = Decimal(spread.quantity)
    gross_credit = credit_per_share * multiplier * quantity
    total_commission = (
        spread.commission_per_contract * Decimal(2) * quantity
    )
    net_credit = gross_credit - total_commission
    maximum_loss = width * multiplier * quantity - net_credit
    if net_credit <= 0 or maximum_loss <= 0:
        raise ValueError("spread economics must have positive credit and max loss")

    net_credit_per_share = net_credit / (multiplier * quantity)
    break_even = (
        short.strike - net_credit_per_share
        if short.option_type is OptionType.PUT
        else short.strike + net_credit_per_share
    )

    return VerticalSpreadCalculation(
        spread_id=spread.spread_id,
        model_id=SPREAD_MODEL_ID,
        model_version=SPREAD_MODEL_VERSION,
        calculated_at=calculated_at,
        input_contract_ids=(short.contract_id, long.contract_id),
        quote_timestamps=(short.quoted_at, long.quoted_at),
        expiration_date=short.expiration,
        days_to_expiration=days_to_expiration,
        planned_exit_days_before_expiration=spread.planned_exit_days_before_expiration,
        planned_exit_date=planned_exit_date,
        quantity=spread.quantity,
        contract_multiplier=CONTRACT_MULTIPLIER,
        width_per_share=width,
        short_sale_price_per_share=short.bid,
        long_purchase_price_per_share=long.ask,
        gross_credit=gross_credit,
        total_commission=total_commission,
        net_credit=net_credit,
        maximum_loss=maximum_loss,
        break_even=break_even,
        return_on_risk=net_credit / maximum_loss,
    )
