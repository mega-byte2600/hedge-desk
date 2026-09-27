"""Multi-asset market-data provider registry.

This module is intentionally transport-light: it defines the authoritative source
catalog, capability coverage, environment-key requirements, and licensing posture
used by higher-level adapters. It does not fetch secrets or market payloads.
"""

from dataclasses import dataclass
from typing import Dict, FrozenSet, Optional, Tuple


@dataclass(frozen=True)
class ProviderSpec:
    provider_id: str
    display_name: str
    asset_classes: FrozenSet[str]
    capabilities: FrozenSet[str]
    authority: str
    auth_env_var: Optional[str]
    public_without_key: bool
    redistribution_default: bool
    commercial_use_default: bool
    notes: str


_PROVIDERS: Tuple[ProviderSpec, ...] = (
    ProviderSpec(
        "fred",
        "Federal Reserve Economic Data (FRED)",
        frozenset({"macro", "rates", "commodities"}),
        frozenset({"economic_series", "release_history", "macro_regimes"}),
        "official",
        "FRED_API_KEY",
        True,
        False,
        True,
        "Official St. Louis Fed macro series; API key enables the JSON route.",
    ),
    ProviderSpec(
        "sec-edgar",
        "SEC EDGAR",
        frozenset({"equities", "credit"}),
        frozenset({"filings", "company_facts", "xbrl", "corporate_events"}),
        "official",
        None,
        True,
        False,
        True,
        "Official submissions and XBRL company-facts APIs; identify the client per SEC policy.",
    ),
    ProviderSpec(
        "nyfed-markets",
        "Federal Reserve Bank of New York Markets Data",
        frozenset({"rates", "credit", "macro"}),
        frozenset({"sofr", "effr", "obfr", "repo", "reference_rates"}),
        "official",
        None,
        True,
        False,
        True,
        "Official administered reference rates and money-market data.",
    ),
    ProviderSpec(
        "treasury-fiscaldata",
        "U.S. Treasury Fiscal Data",
        frozenset({"rates", "credit", "macro"}),
        frozenset({"treasury_data", "debt", "auctions", "fiscal_series"}),
        "official",
        None,
        True,
        False,
        True,
        "Official Treasury fiscal datasets; use Treasury terms for downstream redistribution.",
    ),
    ProviderSpec(
        "eia-open-data",
        "U.S. Energy Information Administration Open Data",
        frozenset({"commodities", "macro"}),
        frozenset({"oil", "gas", "power", "inventories", "production", "energy_prices"}),
        "official",
        "EIA_API_KEY",
        False,
        False,
        True,
        "Official EIA API v2 for petroleum, natural gas, electricity, inventories, and production.",
    ),
    ProviderSpec(
        "cftc-cot",
        "CFTC Commitments of Traders",
        frozenset({"futures", "commodities", "rates", "fx"}),
        frozenset({"positioning", "open_interest", "cot"}),
        "official",
        None,
        True,
        False,
        True,
        "Official CFTC positioning data for futures markets; useful for crowding and regime context.",
    ),
    ProviderSpec(
        "finra",
        "FINRA Public Data",
        frozenset({"credit", "rates", "fixed_income"}),
        frozenset({"corporate_bond_breadth", "treasury_aggregates", "market_sentiment", "agency_tba"}),
        "official",
        "FINRA_CLIENT_ID",
        False,
        False,
        True,
        "Free FINRA Public Credential OAuth; FINRA_CLIENT_SECRET is also required server-side.",
    ),
    ProviderSpec(
        "cboe",
        "Cboe",
        frozenset({"equities", "options", "volatility"}),
        frozenset({"option_chains", "vix", "delayed_quotes", "market_statistics"}),
        "exchange",
        None,
        True,
        False,
        False,
        "Existing delayed-chain/VIX source; exchange licensing controls production and redistribution.",
    ),
    ProviderSpec(
        "cme",
        "CME Group Market Data APIs",
        frozenset({"futures", "options", "rates", "commodities", "fx", "crypto"}),
        frozenset({"real_time_top_of_book", "trades", "market_statistics", "greeks", "implied_volatility", "reference_data"}),
        "exchange",
        "CME_API_KEY",
        False,
        False,
        False,
        "Authoritative futures/options source. Production use requires appropriate CME licensing/entitlements.",
    ),
    ProviderSpec(
        "schwab",
        "Charles Schwab Trader API",
        frozenset({"equities", "options", "etfs", "account"}),
        frozenset({"quotes", "option_chains", "account_positions", "transactions", "orders_readonly"}),
        "broker",
        "SCHWAB_CLIENT_ID",
        False,
        False,
        False,
        "Broker/account seam. Keep credentials server-side and preserve read-only boundaries unless separately reviewed.",
    ),
    ProviderSpec(
        "nasdaq-data-link",
        "Nasdaq Data Link",
        frozenset({"equities", "futures", "options", "macro", "alternative"}),
        frozenset({"historical_datasets", "tables", "streaming", "reference_data"}),
        "commercial",
        "NASDAQ_DATA_LINK_API_KEY",
        False,
        False,
        False,
        "Optional commercial/alternative-data adapter; dataset-specific licenses govern use.",
    ),
    ProviderSpec(
        "polygon",
        "Polygon.io",
        frozenset({"equities", "options", "fx", "crypto"}),
        frozenset({"quotes", "trades", "aggregates", "option_chains", "corporate_actions", "reference_data"}),
        "commercial",
        "POLYGON_API_KEY",
        False,
        False,
        False,
        "Optional consolidated market-data adapter; entitlement and redistribution depend on plan/exchange agreements.",
    ),
    ProviderSpec(
        "tiingo",
        "Tiingo",
        frozenset({"equities", "news", "fx", "crypto"}),
        frozenset({"eod", "fundamentals", "news", "corporate_actions"}),
        "commercial",
        "TIINGO_API_KEY",
        False,
        False,
        False,
        "Optional lower-cost research adapter and secondary EOD/fundamentals source.",
    ),
    ProviderSpec(
        "alpha-vantage",
        "Alpha Vantage",
        frozenset({"equities", "options", "fx", "crypto", "macro", "commodities"}),
        frozenset({"eod", "intraday", "fundamentals", "economic_indicators", "news_sentiment"}),
        "commercial",
        "ALPHA_VANTAGE_API_KEY",
        False,
        False,
        False,
        "Optional research fallback. Rate limits and plan rights must be respected.",
    ),
    ProviderSpec(
        "finnhub",
        "Finnhub",
        frozenset({"equities", "news", "fx", "crypto"}),
        frozenset({"quotes", "fundamentals", "earnings_calendar", "economic_calendar", "news"}),
        "commercial",
        "FINNHUB_API_KEY",
        False,
        False,
        False,
        "Optional event/calendar/news adapter; useful for catalyst desks.",
    ),
    ProviderSpec(
        "stooq",
        "Stooq",
        frozenset({"equities", "indices", "fx", "commodities"}),
        frozenset({"eod"}),
        "public",
        None,
        True,
        False,
        False,
        "Existing no-key EOD fallback. Treat as secondary and preserve source attribution.",
    ),
)


_PROVIDER_INDEX: Dict[str, ProviderSpec] = {item.provider_id: item for item in _PROVIDERS}


def all_providers() -> Tuple[ProviderSpec, ...]:
    return _PROVIDERS


def provider(provider_id: str) -> ProviderSpec:
    try:
        return _PROVIDER_INDEX[provider_id]
    except KeyError as exc:
        raise KeyError(f"unknown provider: {provider_id}") from exc


def providers_for_capability(capability: str) -> Tuple[ProviderSpec, ...]:
    return tuple(item for item in _PROVIDERS if capability in item.capabilities)


def providers_for_asset_class(asset_class: str) -> Tuple[ProviderSpec, ...]:
    return tuple(item for item in _PROVIDERS if asset_class in item.asset_classes)


def missing_auth_env(provider_id: str, environment: Dict[str, str]) -> Optional[str]:
    spec = provider(provider_id)
    if spec.public_without_key or not spec.auth_env_var:
        return None
    return None if environment.get(spec.auth_env_var) else spec.auth_env_var
