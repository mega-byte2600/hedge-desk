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
        "bls",
        "U.S. Bureau of Labor Statistics",
        frozenset({"macro", "labor", "inflation"}),
        frozenset({"cpi", "employment", "unemployment", "economic_series"}),
        "official",
        None,
        True,
        False,
        True,
        "Official BLS public time-series API for labor and inflation context.",
    ),
    ProviderSpec(
        "bea",
        "U.S. Bureau of Economic Analysis",
        frozenset({"macro", "growth", "trade"}),
        frozenset({"gdp", "nipa", "regional", "international_trade", "economic_series"}),
        "official",
        "BEA_API_KEY",
        False,
        False,
        True,
        "Official BEA Data API. Free key stays server-side; NIPA provides GDP and national-accounts context.",
    ),
    ProviderSpec(
        "nws",
        "National Weather Service API",
        frozenset({"weather", "commodities", "logistics"}),
        frozenset({"alerts", "forecasts", "observations", "hazards"}),
        "official",
        None,
        True,
        False,
        True,
        "Official api.weather.gov open data. Use a declared User-Agent and respect rate limits.",
    ),
    ProviderSpec(
        "usda-nass",
        "USDA NASS Quick Stats",
        frozenset({"agriculture", "commodities", "macro"}),
        frozenset({"crop_progress", "crop_condition", "production", "agricultural_statistics"}),
        "official",
        "USDA_NASS_API_KEY",
        False,
        False,
        True,
        "Official USDA NASS Quick Stats API. Free key stays server-side; use narrow queries rather than bulk extraction.",
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
        frozenset({"equities", "credit", "rates", "fixed_income"}),
        frozenset({
            "corporate_bond_breadth", "treasury_aggregates", "market_sentiment",
            "agency_tba", "short_interest", "short_sale_volume",
        }),
        "official",
        "FINRA_CLIENT_ID",
        False,
        False,
        True,
        "FINRA Query API credential required; plan terms and fees govern production access. FINRA_CLIENT_SECRET is also required server-side.",
    ),
    ProviderSpec(
        "ecb-fx",
        "European Central Bank Euro Reference Rates",
        frozenset({"fx", "macro"}),
        frozenset({"reference_rates", "fx_reference"}),
        "official",
        None,
        True,
        False,
        True,
        "Official ECB euro foreign-exchange reference rates.",
    ),
    ProviderSpec(
        "fdic",
        "Federal Deposit Insurance Corporation",
        frozenset({"banks", "credit", "macro"}),
        frozenset({"bank_failures", "banking_stress"}),
        "official",
        None,
        True,
        False,
        True,
        "Official FDIC public bank-failure data.",
    ),
    ProviderSpec(
        "world-bank",
        "World Bank Indicators API",
        frozenset({"macro", "global"}),
        frozenset({"global_indicators", "country_macro"}),
        "official",
        None,
        True,
        False,
        True,
        "World Bank public indicators API for global macro context.",
    ),
    ProviderSpec(
        "imf",
        "International Monetary Fund DataMapper",
        frozenset({"macro", "global", "growth"}),
        frozenset({"real_gdp_growth", "country_macro", "forecasts"}),
        "official",
        None,
        True,
        False,
        True,
        "Official IMF DataMapper annual macro series; public keyless research data.",
    ),
    ProviderSpec(
        "oecd",
        "OECD Composite Leading Indicators",
        frozenset({"macro", "global", "business_cycle"}),
        frozenset({"leading_indicators", "business_cycle", "country_macro"}),
        "official",
        None,
        True,
        False,
        True,
        "Official OECD SDMX public API; queries are restricted to bounded series and periods.",
    ),
    ProviderSpec(
        "eurostat",
        "Eurostat Quarterly National Accounts",
        frozenset({"macro", "global", "growth"}),
        frozenset({"gdp", "national_accounts", "country_macro"}),
        "official",
        None,
        True,
        False,
        True,
        "Official Eurostat Statistics API; compact JSON-stat query for quarterly aggregate GDP.",
    ),
    ProviderSpec(
        "usgs",
        "USGS Earthquake Hazards Program",
        frozenset({"natural_events", "commodities", "logistics", "country_risk"}),
        frozenset({"earthquakes", "hazards", "event_context"}),
        "official",
        None,
        True,
        False,
        True,
        "Official FDSN Earthquake Catalog GeoJSON API; recent, magnitude-filtered, bounded queries.",
    ),
    ProviderSpec(
        "nasa-eonet",
        "NASA Earth Observatory Natural Event Tracker",
        frozenset({"natural_events", "commodities", "logistics", "weather"}),
        frozenset({"natural_events", "hazards", "event_context"}),
        "official",
        None,
        True,
        False,
        True,
        "Official NASA EONET v3 API; recent open-event queries are bounded by age and count.",
    ),
    ProviderSpec(
        "bis",
        "Bank for International Settlements Statistics",
        frozenset({"macro", "global", "credit", "rates"}),
        frozenset({"global_liquidity", "cross_border_credit", "international_banking", "credit_to_gdp"}),
        "official",
        None,
        True,
        False,
        True,
        "Official BIS SDMX statistics for global liquidity, international banking, credit, and financial-system context.",
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
        "coinbase-exchange",
        "Coinbase Exchange Public Market Data",
        frozenset({"crypto"}),
        frozenset({"spot_market_data", "trades", "market_microstructure"}),
        "exchange",
        None,
        True,
        False,
        False,
        "Public read-only Exchange REST market data; no account or order endpoints are used.",
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
        "No-key EOD fallback. 2026-09-28: BLOCKED — /q/l/ 404s and /q/d/l/ serves a "
        "JS bot challenge from this network. Treat as secondary when available.",
    ),
    ProviderSpec(
        "nasdaq",
        "Nasdaq public market-data API",
        frozenset({"equities", "options"}),
        frozenset({"quotes", "option_chains", "earnings_calendar"}),
        "exchange",
        None,
        True,
        False,
        False,
        "No-key public API (browser UA required). Rate-sensitive: batch callers must cache; fail closed on 429.",
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


def provider_console_rows() -> list[dict]:
    """Surface the provider catalog on the desk console (Controls & evidence).

    Honest status derivation, no network at build time:
    - PASS       : official/public, no key required.
    - PENDING    : key-gated or a public source currently blocked from this host.
    - REVIEW     : exchange / broker / commercial seams requiring entitlement review.
    """
    official_public = {
        "fred", "sec-edgar", "nyfed-markets", "treasury-fiscaldata", "bls",
        "nws", "cftc-cot", "ecb-fx", "fdic", "world-bank", "imf", "oecd",
        "eurostat", "usgs", "nasa-eonet", "bis", "cboe",
        "coinbase-exchange", "nasdaq",
    }
    keyed_or_blocked = {"bea", "usda-nass", "eia-open-data", "finra", "stooq"}
    review = {
        "cme", "schwab", "nasdaq-data-link", "polygon", "tiingo",
        "alpha-vantage", "finnhub",
    }

    def _status(provider_id: str) -> str:
        if provider_id in official_public:
            return "PASS"
        if provider_id in keyed_or_blocked:
            return "PENDING"
        if provider_id in review:
            return "REVIEW_REQUIRED"
        return "PENDING"

    rows = []
    for spec in all_providers():
        # The public-claims gate bans "fdic"/"insured" in shipped copy (implied
        # insurance the product cannot offer). FDIC stays in the internal
        # catalog for research; it is simply not surfaced on the public page.
        if spec.provider_id == "fdic":
            continue
        rows.append(
            {
                "source_id": spec.provider_id,
                "display_name": spec.display_name,
                "dataset": ", ".join(sorted(spec.capabilities)),
                "status": _status(spec.provider_id),
                "mode": "FREE_OPEN_PUBLIC_DATA_ONLY"
                if spec.authority in ("official", "public", "exchange")
                else "REVIEW_REQUIRED",
                "feeds": sorted(spec.asset_classes),
                "authority": spec.authority,
                "key_env": spec.auth_env_var,
                "public_without_key": spec.public_without_key,
                "controls": [
                    "fail-closed parsing",
                    "no fabricated values",
                    "server-side key only",
                    "no trade authorization",
                    "no RoR / probability",
                ],
                "notes": spec.notes,
            }
        )
    return rows
