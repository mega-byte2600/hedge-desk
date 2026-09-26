# Multi-Asset Trade Desk API Matrix

Purpose: define the minimum data plane a serious multi-asset research desk needs. Prefer authoritative issuers/exchanges/regulators for primary facts; use commercial aggregators for speed, normalized schemas, intraday breadth, and redundancy. Provider credentials stay server-side. Raw licensed payloads are never committed.

## Desk coverage

| Desk need | Primary source | Secondary / convenience source | Required fields |
|---|---|---|---|
| U.S. macro | FRED | Finnhub / Nasdaq Data Link datasets | releases, revisions, observation dates, vintages, rates, inflation, labor, growth |
| Money markets / policy | New York Fed Markets Data | FRED | SOFR, EFFR, OBFR, repo rates/volumes, publication date |
| Treasury / sovereign context | U.S. Treasury Fiscal Data | FRED / Nasdaq Data Link | auctions, debt/fiscal series, Treasury reference datasets |
| Equities prices | Schwab when connected | Yahoo -> Stooq existing failover; Polygon/Tiingo optional | bid/ask when entitled, last, OHLCV, timestamp, venue/source |
| Company fundamentals | SEC EDGAR | Tiingo / Polygon / Alpha Vantage | 10-K/10-Q/8-K, XBRL facts, filing time, period, accession |
| Corporate events | SEC EDGAR + exchange/broker data | Finnhub / Polygon / Tiingo | earnings, dividends, splits, filings, ex/pay/record dates |
| Listed options | Cboe + Schwab | Polygon; CME for CME-listed derivatives | chain, bid/ask, trades, OI, IV/Greeks when licensed, underlying timestamp |
| Futures / futures options | CME Group | Nasdaq Data Link datasets | top of book, trades, settlement, OI, contract metadata, expiries, IV/Greeks where licensed |
| Energy commodities | EIA + CME | FRED / Nasdaq Data Link | WTI/gas prices, inventories, production, storage, refinery/utilization context |
| Futures positioning | CFTC COT | Nasdaq Data Link mirrors if licensed | long/short/spreading, OI, trader category, report/as-of dates |
| FX | CME / Schwab where available | Polygon / Twelve Data / Alpha Vantage | spot/futures prices, bid/ask, timestamps, volume where applicable |
| Crypto research | CME regulated derivatives where relevant | Polygon / Alpha Vantage | spot/futures basis, volume, OI, timestamp, venue |
| News / catalyst research | issuer/SEC/Fed/Treasury releases first | Finnhub / Tiingo / licensed news vendor | headline, source, published_at, symbols/entities, canonical URL |
| Account / broker state | Schwab Trader API | none | balances, positions, transactions, read-only order state; no execution expansion without separate review |

## What each trader actually needs

### Equities
- consolidated or broker-quality quote context, OHLCV, corporate actions, earnings calendar, filings and point-in-time fundamentals;
- symbol/reference-data normalization (ticker changes, CUSIP/CIK where licensed/available);
- pre/post-market timestamps when the provider supports them;
- historical data deep enough for factor, event, and drawdown work.

### Options
- full chains by expiration and strike;
- bid/ask, last/trades, volume, open interest, underlying price and timestamp;
- IV and Greeks from an entitled source or internally computed from validated inputs;
- corporate-action adjustments and expired-contract history for honest backtests;
- exchange calendar and contract specifications.

### Rates / bonds
- SOFR, EFFR, OBFR and repo context from the New York Fed;
- Treasury issuance/auction/fiscal data plus market yields from an entitled market source;
- futures prices/settlements/OI for Treasury and SOFR complexes from CME when licensed;
- economic releases and revisions from FRED.

### Commodities
- futures curve, settlement, volume, OI and options from the relevant exchange;
- EIA inventories, production, storage and energy balances;
- CFTC positioning for producer/merchant, swap dealer, managed money and other reportable categories where available;
- calendar/spread structure and contract specs.

### Macro / cross-asset
- point-in-time economic observations and release dates;
- central-bank/reference-rate data;
- event calendar for CPI, payrolls, FOMC, GDP, Treasury auctions and major earnings;
- cross-asset closes/returns and volatility proxies with consistent timestamps.

## Source hierarchy

1. Official regulator / government / central bank: SEC, CFTC, EIA, Treasury, Federal Reserve / FRED, New York Fed.
2. Exchange: Cboe, CME and other venues for their own instruments.
3. Broker: Schwab for entitled account and market-data views.
4. Commercial normalizer: Polygon, Tiingo, Finnhub, Nasdaq Data Link, Alpha Vantage, Twelve Data.
5. Public fallback: Stooq and the existing Yahoo public chart route for research continuity only.

A lower tier must not silently overwrite a higher-tier observation. Every artifact retains `source_id`, `source_as_of`, `received_at`, license metadata, freshness state, and payload hash.

## Key-management contract

Expected environment variables for optional/keyed adapters:

- `FRED_API_KEY`
- `EIA_API_KEY`
- `SCHWAB_CLIENT_ID` plus the existing Schwab OAuth secret/token mechanism
- `CME_API_KEY` when CME API access is licensed
- `POLYGON_API_KEY`
- `TIINGO_API_KEY`
- `FINNHUB_API_KEY`
- `ALPHA_VANTAGE_API_KEY`
- `NASDAQ_DATA_LINK_API_KEY`

Keys are deployment secrets, never source code, logs, issue bodies, artifacts, browser JavaScript, iOS bundles, or GitHub commits.

## Implementation order

1. Keep FRED, SEC, Cboe, Yahoo/Stooq, VIX/WTI and Schwab seams intact.
2. Add NY Fed reference-rate adapter for SOFR/EFFR/OBFR/repo.
3. Add CFTC COT adapter for futures positioning.
4. Add EIA v2 adapter for energy inventories/production/storage.
5. Add Treasury Fiscal Data adapter for Treasury/fiscal datasets.
6. Add a licensed CME adapter when credentials/entitlements exist.
7. Add one normalized commercial redundancy layer (Polygon or Tiingo first), then event/news calendar coverage (Finnhub/Tiingo).
8. Only add more vendors when they close a measured coverage or reliability gap.
