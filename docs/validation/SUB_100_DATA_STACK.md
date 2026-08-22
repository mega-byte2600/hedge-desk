# Sub-$100 monthly research data stack

Verified 2026-08-22. Prices and entitlements can change; re-check vendor terms
before purchase or automated use.

## Recommended paid source: ThetaData Options Standard — $80/month

For the premium-selling MVP, the binding need is historical executable quote
evidence, not modeled Greeks alone. [ThetaData's official retail pricing](https://www.thetadata.net/subscribe)
lists Options Standard at $80/month with eight years of data, option-chain
snapshots, tick-level data, and every NBBO quote reported by OPRA. That is the
best verified fit under the Captain's $100 total cap.

Use it for personal/internal research only under the purchased entitlement.
Keep raw payloads, credentials, and tokens outside GitHub. Feed permissioned
snapshots through `--validate-data-envelope --validate-option-snapshot
--scan-vertical-spreads`; commit only schemas, hashes, synthetic fixtures, and
derived artifacts that the license permits.

## Alternatives, not additions

- [Massive Options Developer](https://massive.com/pricing?product=options) is
  $79/month and advertises four years of history, trades, snapshots, open
  interest, IV, and Greeks. Its official page reserves “Quotes” for the
  $199/month Advanced tier, so it is not the optimal primary source for
  executable bid/ask replay under this budget.
- [Tradier](https://docs.tradier.com/docs/market-data) supplies real-time
  consolidated equity/options data to brokerage account holders and delayed
  data in sandbox. Use it later for broker-authoritative current account and
  paper integration, not as the historical OptionMetrics/OPRA-quality research
  substitute. The repository has no broker adapter and the live-release gate
  remains blocked.

Do not buy multiple option feeds inside the first $100 budget. Validate one
feed's completeness, timestamps, corporate actions, expired contracts, and
actual entitlement terms before adding redundancy.

## Free official complements

- [SEC EDGAR APIs](https://www.sec.gov/file/api-overview): filing and issuer
  facts. Preserve accession/publication/acceptance timestamps; never treat a
  later filing revision as point-in-time knowledge.
- [FRED and ALFRED APIs](https://fred.stlouisfed.org/docs/api/fred/overview.html):
  macro series and vintages. ALFRED is preferable when revisions matter. API
  keys and the [FRED terms](https://fred.stlouisfed.org/docs/api/terms_of_use.html)
  remain outside the repository.
- [NOAA Climate Data Online API](https://www.ncei.noaa.gov/cdo-web/webservices/v2):
  weather/climate observations for event research; its official documentation
  states token and rate limits.
- [CFTC Commitments of Traders](https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm):
  weekly futures positioning with historical files. The CFTC notes the usual
  report covers Tuesday positions and is released Friday, so publication time
  must be preserved to avoid look-ahead.

These sources do not replace survivorship-clean CRSP histories, point-in-time
IBES estimate vintages, or institutional OptionMetrics data. At this budget,
the system must label those gaps and return `NO_TRADE` when a required artifact
is absent.

The executable `evaluate_options_data_stack` entitlement gate separately emits
internal-research and live-production-data readiness. Internal research requires
the budget, a permission record, at least five declared historical years,
point-in-time timestamps, historical NBBO, trades, open interest, expired
contracts, chain snapshots, and corporate actions. Live-production-data
readiness additionally requires real-time NBBO and explicit commercial-use
permission. It never authorizes raw vendor payloads to be committed.

Agents can run the same gate with:

```bash
python3 -m hedge_desk.cli --validate-data-stack /absolute/path/data-stack.json
```

The strict manifest schema is `hedge-desk-data-stack-1.1.0`; money values must
be decimal strings, unknown fields fail, and a non-ready result exits nonzero.
Start from `examples/data-stack.synthetic.json`, but replace every synthetic
claim only after checking the purchased entitlement. The example is capability
shape, not proof that a named vendor license grants those rights.
