"""ML option-pricing data curation and deterministic baselines.

This module turns the two ML-options paper ideas into executable MVP scaffolding:

- Stanford CS230 option pricing: model contract terms and financial state, use
  20-day realized volatility or a price sequence, and prefer bid/ask labels over
  a single theoretical price when market microstructure matters.
- DeepOption-style distillation: generate balanced synthetic labels from
  conventional pricing methods before any neural model is trusted with real
  option data.

The output is research-only. It cannot authorize trades or override risk gates.
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from statistics import mean, pstdev
from typing import Dict, Iterable, List, Sequence


SECONDS_PER_TRADING_YEAR = 252


@dataclass(frozen=True)
class OptionQuote:
    symbol: str
    option_type: str
    underlying_price: float
    strike: float
    dte: int
    risk_free_rate: float
    dividend_yield: float
    bid: float
    ask: float
    volume: int
    open_interest: int
    underlying_closes_20d: Sequence[float]


@dataclass(frozen=True)
class CuratedOptionRow:
    symbol: str
    option_type: str
    moneyness: float
    log_moneyness: float
    years_to_expiry: float
    risk_free_rate: float
    dividend_yield: float
    realized_volatility_20d: float
    normalized_mid_price: float
    normalized_bid: float
    normalized_ask: float
    relative_spread: float
    volume: int
    open_interest: int
    liquidity_pass: bool
    labels: Dict[str, float]
    source: str
    trade_authorized: bool = False


def normal_cdf(value: float) -> float:
    """Standard normal cumulative distribution function."""
    return 0.5 * (1.0 + math.erf(value / math.sqrt(2.0)))


def realized_volatility_20d(closes: Sequence[float]) -> float:
    """Annualized close-to-close realized volatility from a 20-day sequence."""
    if len(closes) < 2:
        raise ValueError("at least two closes are required")
    returns: List[float] = []
    for prior, current in zip(closes, closes[1:]):
        if prior <= 0 or current <= 0:
            raise ValueError("closes must be positive")
        returns.append(math.log(current / prior))
    return pstdev(returns) * math.sqrt(SECONDS_PER_TRADING_YEAR)


def black_scholes_price(
    option_type: str,
    spot: float,
    strike: float,
    years_to_expiry: float,
    risk_free_rate: float,
    dividend_yield: float,
    volatility: float,
) -> float:
    """Price a European option with continuous dividend yield."""
    if spot <= 0 or strike <= 0 or years_to_expiry <= 0 or volatility <= 0:
        raise ValueError("spot, strike, expiry, and volatility must be positive")
    sqrt_t = math.sqrt(years_to_expiry)
    d1 = (math.log(spot / strike) + (risk_free_rate - dividend_yield + 0.5 * volatility**2) * years_to_expiry) / (
        volatility * sqrt_t
    )
    d2 = d1 - volatility * sqrt_t
    discounted_spot = spot * math.exp(-dividend_yield * years_to_expiry)
    discounted_strike = strike * math.exp(-risk_free_rate * years_to_expiry)
    if option_type.lower() == "call":
        return discounted_spot * normal_cdf(d1) - discounted_strike * normal_cdf(d2)
    if option_type.lower() == "put":
        return discounted_strike * normal_cdf(-d2) - discounted_spot * normal_cdf(-d1)
    raise ValueError("option_type must be call or put")


def binomial_price(
    option_type: str,
    spot: float,
    strike: float,
    years_to_expiry: float,
    risk_free_rate: float,
    dividend_yield: float,
    volatility: float,
    steps: int = 50,
) -> float:
    """Cox-Ross-Rubinstein European option baseline."""
    if steps <= 0:
        raise ValueError("steps must be positive")
    dt = years_to_expiry / steps
    up = math.exp(volatility * math.sqrt(dt))
    down = 1.0 / up
    growth = math.exp((risk_free_rate - dividend_yield) * dt)
    probability = (growth - down) / (up - down)
    if not 0 <= probability <= 1:
        raise ValueError("invalid risk-neutral probability")

    values: List[float] = []
    for index in range(steps + 1):
        terminal_spot = spot * (up ** (steps - index)) * (down**index)
        if option_type.lower() == "call":
            values.append(max(terminal_spot - strike, 0.0))
        elif option_type.lower() == "put":
            values.append(max(strike - terminal_spot, 0.0))
        else:
            raise ValueError("option_type must be call or put")

    discount = math.exp(-risk_free_rate * dt)
    for _step in range(steps):
        values = [discount * (probability * values[i] + (1.0 - probability) * values[i + 1]) for i in range(len(values) - 1)]
    return values[0]


def curate_option_quote(quote: OptionQuote) -> CuratedOptionRow:
    """Build the model-ready row consumed by QuantDesk experiments."""
    if quote.bid < 0 or quote.ask <= 0 or quote.ask < quote.bid:
        raise ValueError("invalid bid/ask")
    if quote.strike <= 0 or quote.underlying_price <= 0 or quote.dte <= 0:
        raise ValueError("invalid option economics")

    years = quote.dte / 365.0
    realized_vol = realized_volatility_20d(quote.underlying_closes_20d)
    mid = (quote.bid + quote.ask) / 2.0
    relative_spread = (quote.ask - quote.bid) / mid if mid else float("inf")
    liquidity_pass = quote.volume >= 10 and quote.open_interest >= 100 and relative_spread <= 0.25

    bs = black_scholes_price(
        quote.option_type,
        quote.underlying_price,
        quote.strike,
        years,
        quote.risk_free_rate,
        quote.dividend_yield,
        realized_vol,
    )
    bi = binomial_price(
        quote.option_type,
        quote.underlying_price,
        quote.strike,
        years,
        quote.risk_free_rate,
        quote.dividend_yield,
        realized_vol,
    )
    return CuratedOptionRow(
        symbol=quote.symbol.upper(),
        option_type=quote.option_type.lower(),
        moneyness=quote.underlying_price / quote.strike,
        log_moneyness=math.log(quote.underlying_price / quote.strike),
        years_to_expiry=years,
        risk_free_rate=quote.risk_free_rate,
        dividend_yield=quote.dividend_yield,
        realized_volatility_20d=realized_vol,
        normalized_mid_price=mid / quote.strike,
        normalized_bid=quote.bid / quote.strike,
        normalized_ask=quote.ask / quote.strike,
        relative_spread=relative_spread,
        volume=quote.volume,
        open_interest=quote.open_interest,
        liquidity_pass=liquidity_pass,
        labels={
            "market_bid": quote.bid,
            "market_ask": quote.ask,
            "market_mid": mid,
            "black_scholes": bs,
            "binomial": bi,
            "distilled_mean": mean([bs, bi]),
        },
        source="quantdesk_ml_options_curation_v0",
    )


def curate_option_chain(quotes: Iterable[OptionQuote]) -> List[Dict[str, object]]:
    """Return JSON-ready rows for downstream model experiments."""
    return [asdict(curate_option_quote(quote)) for quote in quotes]
