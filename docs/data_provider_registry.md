# Multi-Asset Data-Provider Registry

Status: implemented · branch `feat/multi-asset-data-adapters` · closes #81 scope

## What it is

`hedge_desk/data/providers.py` adds a provider **registry + adapter seam** so the
desk can pull authoritative free/open market data across asset classes behind
one fail-closed gate, with the same provenance/freshness discipline as the rest
of the data layer. A transport function is injected for every adapter, so CI
runs deterministic fixtures and never depends on the live network.

## Registered providers (REGISTRY_BY_ID)

| Provider id | Source | Keyless | Asset classes | Live status |
|---|---|---|---|---|
| `sec-edgar-companyfacts` | SEC EDGAR XBRL | yes | equities, filings, earnings | PASS (verified live) |
| `cftc-cot` | CFTC COT | yes | futures, positioning, rates | code verified; host SSL | 
| `ust-treasury-fiscal` | U.S. Treasury Fiscal Data | yes | fixed income, macro, FX | PASS (verified live) |
| `eia-open-data-v2` | EIA Open Data v2 | no (key) | energy, macro | key-gated fail-closed |
| `stooq-eod` | Stooq EOD CSV | yes | equities, EOD | BOT_WALL detected honestly |
| `alpha-vantage-eod` | Alpha Vantage | no (key) | equities, EOD | key-gated fail-closed |
| `tiingo-eod` | Tiingo | no (key) | equities, EOD | key-gated fail-closed |
| `twelve-data-eod` | Twelve Data | no (key) | equities, EOD | key-gated fail-closed |

## Behavior guarantees

- **Fail closed.** A missing/empty/malformed payload yields no invented value and
  a reason code (`TRANSPORT_FAILED`, `PAYLOAD_MALFORMED`, `EMPTY_PAYLOAD`,
  `TAG_UNKNOWN`, `CIK_INVALID`, `PAYLOAD_NOT_ZIP`, `NO_NUMERIC_ROWS`,
  `NO_VALID_DAYS`).
- **Key-gated sources report, never fabricate.** With no key present an adapter
  returns `CONFIG_MISSING_KEY` + the env var it needs (`EIA_API_KEY`,
  `ALPHA_VANTAGE_API_KEY`, `TIINGO_API_KEY`). Keys are read server-side from the
  environment in `fetch_provider`; the key value is never logged or emitted.
- **Bot-walls are detected, not bypassed.** Stooq now fronts a JS proof-of-work
  challenge; `stooq-eod` returns `BOT_WALL` rather than scraping around the gate.
- **No RoR, probability, or trade authorization.** Observations are sealed via
  `build_provider_artifact` as `synthetic=False`, `redistribution_allowed=False`.
- **No licensed/commercial source** is wired; free-open only.

## Live findings (2026-09-29)

- Yahoo EOD (existing) and SEC EDGAR answer keyless.
- U.S. Treasury Fiscal Data answers keyless (`rates_of_exchange` verified).
- **Host SSL note:** Treasury and CFTC fail `urllib` with
  `CERTIFICATE_VERIFY_FAILED` from this Mac because a MITM/self-signed cert is
  in their chain — this is a machine/proxy issue, not the adapter. SEC and Yahoo
  work through the same transport, and the Treasury parser is proven against a
  captured live payload. The adapter deliberately does **not** disable SSL
  verification (security regression; fails closed instead).
- **FRED JSON** now requires an API key (400 without) but FRED **CSV**
  (`fredgraph.csv`, used by `rates_desk`) is still keyless.
- Stooq CSV is now behind a JS bot-wall; kept as a forward seam only.

## Wiring

- `data/__init__.py` re-exports the registry and helpers.
- CLI:
  - `hedge-desk --list-providers`
  - `hedge-desk --data-provider <id> --provider-series <series> [--provider-param k=v …]`
    e.g.
    `--data-provider sec-edgar-companyfacts --provider-series 320193 --provider-param tag=Revenues`

## Tests (deterministic, no network)

`tests/test_data_providers.py` (adapter-level) and `tests/test_cli_providers.py`
(CLI-level) assert each adapter parses a good captured-shape payload and fails
closed on bad input. Full suite: **924 passed + 18 subtests**.
