# Emporion (hedge-desk) capability inventory, for a gap analysis against a Wall Street trading desk

- Audit date: 2026-11-19. Read-only audit of this repository. Nothing was edited, committed, or fetched from the network.
- Status legend: **PRODUCTION-REAL** = runs against real external data on a deployed or scheduled path. **PAPER-REAL** = real logic with real inputs, paper-only, no money moves. **SYNTHETIC-ONLY** = exercised only on repository fixtures or war games. **STUB** = scaffold, contract, or fail-closed seam with no working source. **ABSENT** = no code found.
- **VERIFIED (measured here):** a copy of the repo was run in a temporary directory with HTTP(S) proxies pointed at a dead port. `python3 -m pytest tests` gave **1325 passed, 51 subtests passed** in 36 s (Python 3.13). `coverage report` gave **TOTAL branch coverage 80%** (13,662 statements). `tests/` has 160 files and 1,324 `def test` functions.
- Doc-reported figures I did not re-measure are marked "(doc)".
- **Stale docs:** `docs/architecture/STATUS.md` (2026-08-22) and the README "Safety boundary" both still say "no broker adapter, no live market-data adapter". The code now has a read-only Schwab adapter (`hedge_desk/brokers/schwab_readonly.py`), a Schwab market-data adapter (`brokers/schwab_market_data.py`) and many live keyless feeds. Treat STATUS.md as historical.

## 1. Desks / strategies

| Capability | Status | Evidence path | Notes |
|---|---|---|---|
| Desk 1 Overnight Premium: EOD watchlist intake | PRODUCTION-REAL (local cron) | `hedge_desk/data/eod_ingest.py` `ingest_eod`; `nightly.py` `run_nightly`, `_watchlist` | Daily bars come from Yahoo's public chart API. The watchlist comes from the `EOD_WATCHLIST` env var or a default. `artifacts/am-report-latest.json` (generated 2026-11-19) has mode `REAL_EOD_NIGHTLY`, 7 symbols, 21 candidates, freshness `is_current: true`. |
| Desk 1: real option chain to spreads | PAPER-REAL | `cboe_chain.py` `build_snapshot_from_cboe`, `real_chain_income`; `options/scanner.py` `scan_vertical_credit_spreads`; `options/spreads.py` | Uses the Cboe *delayed* public chain. The latest report has SPY with 749 pairs and 747 admissible. Economics use the executable side (bid/ask) with a $0.65/contract commission. |
| Desk 1: cash-secured-put wheel scan | PAPER-REAL | `csp_scan.py` `scan_cash_secured_put`; `position_sizing.py` `evaluate_premium` | Rules: ~10% OTM, 30-45 DTE, collateral < $5k, 0.5-2% return on collateral. `docs/TECH_ROADMAP.md` Tier 2 records that no liquid name met 1-2% at 10% OTM. The basis of "2%" is still open with the GP (`docs/PREMIUM_WHEEL_ECONOMICS.md`). |
| Desk 1: premium score ranking | PAPER-REAL | `premium_score.py` `score_structure`, `rank_chain_income`; `docs/REVIEW_ROUNDS.md` | Weighted sum: vol edge (IV vs 21d realized vol) 30%, time value 25%, DTE window 25%, delta placement 20%. Uses floats, not Decimal. Research ranking only. Per REVIEW_ROUNDS, the ranking objective is "open until the GP states the desk's purpose". |
| Desk 1: monthly cadence, events, session, exit gates | PAPER-REAL / SYNTHETIC | `options/cadence.py`, `options/events.py`, `options/session.py`, `options/exit_policy.py` | Cadence: one entry per month, minimum 21 days apart. Also covers point-in-time corporate-event windows, exchange-session evidence, and buy-to-close monitoring. The CI intake path feeds them synthetic evidence. |
| Desk 2 Earnings Event | PAPER-REAL (actuals) / SYNTHETIC (surprise) | `earnings_desk.py` `earnings_desk`; `earnings.py` `evaluate_earnings_surprise`, `evaluate_earnings_universe`; `earnings_experiment.py` | Reported EPS comes from SEC XBRL (live in the AM report for CIK 0000320193). A surprise is computed only if a consensus is supplied, and there is no consensus/estimates feed. STATUS.md disposition is `NO_TRADE`. |
| Desk 3 Box/Parity (arbitrage) observer | SYNTHETIC-ONLY | `arbitrage.py` `evaluate_arbitrage_package`; `wargames.py` `ArbitrageWarGame`; ADR-0003 | Executable-edge math including fees, a slippage reserve and financing. No live European index option quotes or financing curve. |
| Desk 4 Dividend Opportunity | SYNTHETIC-ONLY (ranker); STUB (live) | `dividends.py` `evaluate_dividend_universe`, CAPE overlay; `data/nasdaq_calendars.py` | Ten-year point-in-time payout ranking runs on fixtures. A Nasdaq dividends/splits calendar adapter exists, but there is no survivorship-safe 10-year history source. |
| Desk 5 Short Sale Research | PAPER-REAL (leads) / STUB (FINRA) | `short_research.py` `review_short_research`; `short_research_board.py`; `sec_filings_service.py`; `short_interest_service.py`; `burry_sensitivity.py`; ADR-0007 | Live SEC submissions give filing and 8-K leads. FINRA short interest **fails closed until `FINRA_CLIENT_ID/SECRET` are set**. Includes a depreciation sensitivity on user inputs and an evidence-completeness gate. No borrow/locate data, no thesis generation (`DESK_COVERAGE_AUDIT_2026-11-16.md`). |
| Desk 6 Weather/War/Logistics Futures | PRODUCTION-REAL (event context) / SYNTHETIC (economics) | `futures_events.py` `evaluate_futures_event`; `data/event_wire.py` (GDELT); `open_market_feeds.py` `nasa_eonet_events`, `usgs_earthquakes`; `public_signal_feeds.py` `nws_active_alerts`; `cot_desk.py` | Event feeds are live in the AM report. Curve, basis, roll and margin economics are synthetic. **No CME curves, settlements or contract specs** (audit doc). |
| Desk 7 Bonds & Rates | PRODUCTION-REAL (FRED) / static snapshot | `rates_desk.py` `rates_environment`; `macro_desk.py`; `rates_futures.py` (bond price, duration, basis, carry, curve slope); `web/desk7-indicators.json`; `docs/DESK7_RATES_DECISION_INDICATORS.md` | FRED CSV and NY Fed reference rates are live. The ten-indicator board is a dated JSON snapshot (2026-11-13) with a stale warning. No yield-curve model, OAS or credit pricing. |
| Supporting context: VIX regime, WTI, macro | PRODUCTION-REAL | `vix_regime.py`, `oil_desk.py`, `macro_desk.py` | Yahoo `^VIX` and `CL=F` delayed closes. Regime bands are conventional labels. |
| War games / scenario lab | SYNTHETIC-ONLY | `wargames.py` (1,401 lines; Premium, Earnings, Arbitrage, Dividend, Execution, Lifecycle, Futures, Compliance, Audit, Scheduler attack classes); `portfolio_stress.py` | STATUS.md (doc): 72 war games plus 5 combined capital-path stresses, 45 of them `NO_TRADE` controls. |

## 2. Market data & providers

| Capability | Status | Evidence path | Notes |
|---|---|---|---|
| Provider registry and fail-closed contract | PRODUCTION-REAL | `data/providers.py` `REGISTRY_BY_ID`, `missing_auth_env`; `docs/data_provider_registry.md` | Reason codes include `TRANSPORT_FAILED`, `PAYLOAD_MALFORMED`, `CONFIG_MISSING_KEY` and `BOT_WALL`. Transports are injected, so tests run without network. |
| Equities EOD (Yahoo chart) | PRODUCTION-REAL, delayed EOD | `data/eod_ingest.py` | Keyless public endpoint with no license or SLA. `freshness.py` labels today versus the prior close. |
| Equities quotes (Schwab primary, Yahoo failover) | PAPER-REAL when token present | `schwab_core_data.py`; `brokers/schwab_market_data.py` (quotes, option_chain, price_history, movers, instruments, market_hours) | Needs Schwab OAuth (`brokers/schwab_oauth.py`, `schwab_tokens.py`). Live status depends on the token. `/api/health` reports `schwab_core`. |
| Stooq / Alpha Vantage / Tiingo / Twelve Data EOD | STUB | `providers.py` | Stooq returns `BOT_WALL`. The other three return `CONFIG_MISSING_KEY` until a key is set. |
| Finnhub quotes | STUB until key | `finnhub_desk.py` | Needs `FINNHUB_API_KEY`. |
| Options chains | PAPER-REAL, **delayed** | `cboe_chain.py` (Cboe delayed JSON); `options_seed.py` (exchange IV/delta/gamma/theta/vega); `open_market_feeds.py` `nasdaq_option_chain`; Schwab `option_chain` | Delayed reference data with no OPRA entitlement. `DATA_SOURCE_ARCHITECTURE.md` says Cboe delayed pages are "human reference only where automated extraction is prohibited". That is a licensing tension for automated use. |
| Real-time NBBO / OPRA | ABSENT | CI asserts `live_production_reason_codes == ["COMMERCIAL_USE_PERMISSION_ABSENT","REAL_TIME_NBBO_ABSENT"]` (`.github/workflows/ci.yml`); `data/entitlements.py` | The planned paid source is ThetaData at $80/mo (`docs/validation/SUB_100_DATA_STACK.md`). Not purchased or wired. |
| Historical option chains (backtest grade) | ABSENT | `DATA_SOURCE_ARCHITECTURE.md` Tier 1 (OptionMetrics/CRSP not licensed) | STATUS.md lists this as production blocker #1. |
| Corporate actions | STUB / partial | `data/nasdaq_calendars.py` (dividends, splits); `options/events.py` (gate fed with supplied events) | No survivorship-safe security master, delisting returns or option contract-adjustment feed (STATUS.md blocker #2). |
| Fundamentals | PRODUCTION-REAL (limited) | `providers.py` `sec-edgar-companyfacts`; `open_market_feeds.py` `sec_companyfacts`, `sec_submissions`; `data/sec_fts.py` | Raw XBRL facts only. No standardized fundamentals (Compustat-like) and no estimates/IBES. |
| News | STUB / licensed BYO | `data/news.py` (point-in-time gate); `data/pwb_news.py` (licensed local file, hashed features); `event_wire.py` (GDELT leads) | No real-time licensed newswire. GDELT is labeled a lead, not confirmation. |
| Macro / rates | PRODUCTION-REAL | `open_market_feeds.py` (Treasury auctions and yield curve, NY Fed reference rates, BLS, ECB FX, IMF, OECD, Eurostat, World Bank, FDIC, BoC FX, Frankfurter FX); `institutional_feeds.py` (BIS); `rates_desk.py`/`macro_desk.py` (FRED CSV) | The latest AM report `market_context` shows 22 LIVE, 0 blocked, 4 UNCONFIGURED (BEA, USDA-NASS, EIA, FINRA, all key-gated). |
| Futures / commodities | PARTIAL | `cot_desk.py`/`cftc_cot` (positioning, LIVE); `oil_desk.py` (Yahoo `CL=F` front month); `eia_v2` (key-gated) | No CME curve, settlement or open-interest data. |
| FX / crypto | PRODUCTION-REAL (reference) | ECB, BoC, Frankfurter; `coinbase_exchange_rates`, `coinbase_product_trades` | Reference rates only. No desk trades them. |
| Data lineage / BYO intake | PAPER-REAL | `data/contracts.py` `validate_data_artifact`; `data/batch.py` `build_batch_manifest`; `data/intake.py`; `data/manifest.py` | Content-addressed; licensed payloads stay outside Git. |
| Data-quality monitor | PRODUCTION-REAL | `data_quality.py` `quality_report`; `freshness.py` | Alerts are embedded in the AM report (latest: overall `OK`). |

## 3. Analytics & models

| Capability | Status | Evidence path | Notes |
|---|---|---|---|
| BSM pricing, N(d2) win probability, IV inversion | PAPER-REAL | `risk/win_probability.py` (`MODEL_VERSION = "2.0.0"`, `implied_volatility` by bisection, Merton dividend yield); `tests/test_win_probability.py` (Hull Ex. 15.6 / 17.1 reference cases) | Labeled risk-neutral, not a forecast. Promoted by a GP decision on 2026-11-19 (`REVIEW_ROUNDS.md`). |
| Spread probability of profit / risk-neutral EV | PAPER-REAL | `cboe_chain.py` `spread_probabilities` | Computed on **delayed** Cboe IV. Information column only. This may sit in tension with SOUL order #4 ("No probability ... claims on delayed data"); a reviewer should decide. |
| Greeks | PAPER-REAL (vendor-supplied) | `options_seed.py` (exchange delta/gamma/theta/vega with null if missing); `premium_score.py` `short_leg_delta` | No internal Greeks engine or portfolio Greek aggregation. |
| Vol surface / skew model | ABSENT | Search for surface/skew/smile found nothing beyond per-leg IV use in `cboe_chain.py` | No surface fit, term structure or skew metrics. |
| Binomial / ML option pricing scaffolding | STUB | `quantdesk/ml_options.py` (`black_scholes_price`, `binomial_price`, `curate_option_chain`) | Data-curation baselines. No trained model. |
| Option valuation primitives, collateral/margin | PAPER-REAL | `options/valuation.py`; `options/requirements.py` (CSP, covered call, credit spread margin) | Decimal throughout. Broker-specific margin is not modeled beyond a versioned policy. |
| Bond / futures arithmetic | PAPER-REAL | `rates_futures.py` (`bond_price_from_yield`, `macaulay_duration`, `futures_basis`, `annualised_carry`) | Closed-form only. No convexity or key-rate DV01. |
| Feature plane | PRODUCTION-REAL | `features.py` (returns 1/5/21d, realized vol 21d, range position) | Hashed deterministically per batch. |
| Statistical inference / calibration | SYNTHETIC-ONLY | `stat_inference.py` (exact binomial); `stat_evaluation.py` (calibration); CI step asserts `INSUFFICIENT_SAMPLE` | No real outcome sample exists: the paper log has 0 entries. |
| Backtest / replay | STUB | `replay.py` (look-ahead gate, `reference_replay`) | No historical backtest engine and no historical data to run one. STATUS.md blocker #4. |
| Walk-forward splits / model governance | STUB | `models/splits.py` (purged walk-forward), `models/training_run.py`, `models/registry.py`, `models/quorum.py` | Governance gates exist. The only builders are `build_synthetic_*`. |
| Monte Carlo | ABSENT | No `random`/MC code in `hedge_desk/` (only `feed_base.py` jitter) | — |
| Stress testing | SYNTHETIC-ONLY | `portfolio_stress.py` `build_portfolio_stress_report` (hard-coded `StrategyShock` dollar P&L per desk), `build_stress_circuit_breaker` | Fixed scenario table. Not shocking real positions or Greeks. `live_desk_data.py` `build_real_scenarios` applies %-moves to live SPY/QQQ/IWM quotes for display. |
| Strategic allocation / CAPE overlay | PAPER-REAL (supplied inputs) | `strategic_allocation.py` | Inputs are user-supplied. |

## 4. Risk management

| Capability | Status | Evidence path | Notes |
|---|---|---|---|
| 2%-of-equity max-loss rule | PAPER-REAL | `position_sizing.py` `MAX_LOSS_FRACTION_EQUITY = 0.02`, `scale_position_to_equity`, `wheel_fit_for_equity` | Survivability stays **INDETERMINATE** until `ACCOUNT_EQUITY` is supplied (`account.py`). Latest report: `account_equity_configured: false`. |
| Per-trade loss limit in the risk gate | PAPER-REAL | `risk/ruin.py` `RiskPolicy.maximum_single_trade_loss_fraction = 0.01` | **Inconsistent thresholds:** the risk gate defaults to 1% while position_sizing uses 2% and the portfolio symbol limit is 2%. A reviewer should reconcile them. |
| Portfolio exposure limits | PAPER-REAL | `backoffice/portfolio.py` `PortfolioPolicy` (aggregate 5%, symbol 2%, max 10 positions), `evaluate_portfolio_gate` | Max-loss based only. No Greek, sector, factor, beta or correlation limits. |
| Drawdown circuit breaker | PAPER-REAL | `backoffice/portfolio.py` `evaluate_drawdown_circuit_breaker` | Inputs are supplied drawdowns. There is no live P&L feed. |
| Risk of Ruin component | STUB (unvalidated) | `risk/ruin.py` `RISK_MODEL_VERSION = "0.1.0-unvalidated"`, `estimate_risk_of_ruin`; `risk/inputs.py` `ValidatedRiskInputs`; `tests/test_architecture_boundaries.py` | AST tests confine the RoR calculation and validated-input construction. `risk_gate` only *consumes* RoR. Permitted validators are `classic-vv-fixture-validator` and `classic-vv-test-validator`. Release evidence `ROR_CONVENTIONAL_VV_APPROVED` is false. |
| Pre-trade risk checks | PAPER-REAL | `risk/ruin.py` `risk_gate` (`MAX_LOSS_UNDEFINED`, `STALE_QUOTE` > 900 s, `INSUFFICIENT_LIQUIDITY` < $1M ADV, `QUOTE_FROM_FUTURE`, `RISK_OF_RUIN_LIMIT`); `core/decision.py` `evaluate_candidate` | Deterministic, with reason codes. |
| Kill switch | STUB (decision-only) | `execution_gate.py` `KillSwitch(armed=False)`, `evaluate_execution` | Defaults to BLOCKED. It is a dataclass flag passed to a harness that never sends orders. There is no operator UI, persistence or DR test (release item `KILL_SWITCH_AND_DR_TESTED` is false). |
| Paper-to-live release gate | PAPER-REAL (always blocked) | `release.py` (9 required evidence items incl. `BROKER_ORDER_ADAPTER_CERTIFIED`, `REGULATORY_COUNSEL_SIGNOFF`) | Status is `LIVE_RELEASE_BLOCKED`. It cannot be overridden by an agent or a human. |
| Real-time intraday risk monitoring / VaR | ABSENT | — | No intraday positions, VaR, ES or margin-call simulation. |

## 5. Compliance & suitability

| Capability | Status | Evidence path | Notes |
|---|---|---|---|
| Deterministic compliance policy engine | PAPER-REAL | `backoffice/compliance.py` `evaluate_compliance_policy`, `COMPLIANCE_POLICY_VERSION = "paper-securities-1.0.0"` | Hash-bound artifacts. Live counsel flags are all false (STATUS.md). |
| Options/futures approval and disclosure gate | PAPER-REAL | `compliance/account_gate.py` `account_gate` | Blocks undefined-risk options. Checks `options_approved`, a timestamped disclosure acknowledgement, the broker policy version, and blocks futures in IRAs. This is a boolean approval, not FINRA options **levels** 1-5. |
| Regulatory traceability registry | PAPER-REAL | `compliance/traceability.py` (`regulatory-traceability-1.0.0`) | Maps FINRA/SEC/CFTC/OCC requirements to a hash. |
| Reg BI / suitability | ABSENT (by design) | `docs/compliance/FINRA_ENGINEERING_MAP.md` | Product positioned as research, "does not recommend". There is no suitability profile or check. |
| Public-claims guard (Rule 2210 direction) | PRODUCTION-REAL (CI) | `tests/test_public_claims.py`, `tests/test_public_web_surface.py`, `scripts/lint_copy.py`, `web/disclosures.json` | Prohibited-claim scanning runs in CI. |
| Audit journal / recordkeeping | PAPER-REAL | `audit.py` (hash chain), `audit_store.py` (fsync JSONL), `research_audit.py`, `membership_audit.py` | Not WORM storage, no retention schedule, no regulator export (17a-4 gap per FINRA map). STATUS.md blocker #5. |
| Reason codes on every decision | PAPER-REAL | `risk/ruin.py`, `compliance/account_gate.py`, `execution_gate.py`, `paper/workflow.py` | Consistent sorted reason-code tuples. |
| Registration / supervision (3110) | ABSENT | FINRA map | The map states no registered persons. Supervisory roster was tied to retired membership features (`server.py` returns 410). |

## 6. Order lifecycle / execution

| Capability | Status | Evidence path | Notes |
|---|---|---|---|
| Paper trade plan, human approval bound to plan hash | PAPER-REAL | `paper/workflow.py` `create_paper_trade_plan`, `approve_paper_trade`, `execute_paper_open/close`; CI "Verify authorized paper lifecycle" | The CI fixture closes with `realized_pnl == "77.40"` on **synthetic** data. |
| Review queue | STUB (in-memory) | `paper/review.py` `PaperReviewQueue` | Not persisted. |
| Paper lifecycle runner | PAPER-REAL | `paper/runner.py` `advance_paper_lifecycle`; `paper/settler.py` `settle_paper_outcomes` | Handles stale/worse/partial fills, assignment, expiration and ex-dividend escalations (`EARLY_ASSIGNMENT_RISK`, `CONTRACT_ADJUSTMENT_PENDING`, …). |
| Fill simulation | PAPER-REAL (simple) | `paper/workflow.py` `PaperFillCheck` (combo size, current net credit, staleness) | Fills at the quoted executable side or cancels. No queue position, partial-fill model or latency. |
| Slippage / cost model | PARTIAL | `cboe_chain.py` commission 0.65/contract; `arbitrage.py` `slippage_reserve`; CLI `--exit-commission-per-contract` | Bid/ask crossing plus a flat commission. No market-impact or exchange fee schedule. |
| Order types (limit/stop/OCO), OMS/EMS, routing, FIX | ABSENT | CI step "Assert no production broker adapter exists" greps for `submit_order|placeOrder` | Structures are CSP, covered call and verticals only. |
| Broker adapters | PAPER-REAL (read-only) | `brokers/schwab_readonly.py` (balances/positions GET only); `tests/test_schwab_readonly.py::test_module_contains_no_order_paths`; `broker_link.py` | AGENTS.md forbids exposing balances or positions to the browser/public API. |
| Hard execution boundary | PAPER-REAL (enforced) | `tests/test_architecture_boundaries.py::test_paper_runtime_has_no_broker_or_network_client_dependency`; CI broker grep; `/api/health` `live_orders_enabled: False` | **Governance conflict:** `docs/MVP_RESCOPE_2026.md` and `TECH_ROADMAP.md` Tier 5 record a GP choice of "risk-gated AUTO execution" via Schwab. SOUL/AGENTS keep paper-only, and the code matches SOUL. |

## 7. Back office

| Capability | Status | Evidence path | Notes |
|---|---|---|---|
| Reconciliation | PAPER-REAL (hash inputs) | `backoffice/reconciliation.py` `evaluate_paper_reconciliation` (`paper-back-office-reconciliation-1.1.0`) | Compares supplied position hashes, cash and exception counts. No broker statement ingestion. A passing paper result is explicitly ineligible as live evidence. |
| P&L | PAPER-REAL (per paper close) | `paper/workflow.py` `PaperClose.realized_pnl`; `paper_log.py` (outcome tally) | Latest report: 0 paper outcomes, 0 Yellow Sheets. No mark-to-market, daily P&L attribution or performance reporting. |
| Ledgers / books | PARTIAL | `paper_log.py`, `yellow_sheet.py`, `audit_store.py` (append-only JSONL) | No general ledger, tax lots, cost basis, fees ledger or NAV. |
| Settlement / clearing | STUB | `paper/workflow.py` (`SETTLEMENT_TERMS_UNCONFIRMED`, assignment reconciliation required) | Lifecycle flags only. No T+1, cash sweeps, corporate-action processing or OCC exercise files. |

## 8. Agents / multi-agent orchestration

| Capability | Status | Evidence path | Notes |
|---|---|---|---|
| Six Hermes profiles: orchestrator, quant, engineer, research, risk, data | EXTERNAL (spec only in repo) | `docs/architecture/MULTI_AGENT_DESK.md` | Models listed: deepseek-v4-pro, glm-5.3, gpt-6-astra-flex, claude-haiku-4.5, gemini-3.8-flash, qwen3.8-flash. Profiles live outside the repo (no Hermes code in `hedge_desk/`). |
| Muse research lane | EXTERNAL (contract only) | `MUSE.md`; `scripts/validate_muse_findings.py` | Post-close research agent. Its findings are validated by a script. |
| Learning ledger | STUB (not wired) | `agents/learning_ledger.py` (`grade_prediction`, `agent_score`) | Referenced only by `tests/test_agent_learning_ledger.py`. |
| Research quorum | SYNTHETIC-ONLY | `models/quorum.py` `evaluate_research_quorum` | Used only in `wargames.py`. |
| Agent gating | PAPER-REAL (enforced) | `tests/test_architecture_boundaries.py` (agents cannot import the RoR calculator or build validated risk inputs; stat inference cannot become authority) | Strong static boundary. |
| Hermes/Matrix messaging | EXTERNAL | AGENTS.md "Hermes / Matrix" | No bridge code in repo. |
| Research job contract | STUB | `jobs.py` `ResearchJob`; `research_intelligence.py` `assess_source` | Contract only. No queue worker. |

## 9. Platform & ops

| Capability | Status | Evidence path | Notes |
|---|---|---|---|
| CI gates | PRODUCTION-REAL | `.github/workflows/ci.yml` | Py 3.9/3.11/3.13 matrix; ruff; compileall; node web tests; SHA-pinned actions check; coverage ≥80% (79% on 3.9); CLI smoke assertions; golden-master API; black-box server; load test p95 < 400 ms at 25/50/100 concurrency; path-traversal test. |
| Security scans | PRODUCTION-REAL | `codeql.yml` (weekly, Wed 09:17 UTC + push/PR), `secret-pattern-scan.yml`, `supply_chain.py` | — |
| Scheduled jobs | PRODUCTION-REAL | `overnight-paper-evaluation.yml` every 15 min (**synthetic** war games + morning report); `data-scout.yml` every 6 h; `options-seed.yml` Mon 15:30 UTC (real Cboe SPY seed, committed); `supabase-keepalive.yml` 3×/day | GitHub cron is best-effort (README). |
| Real nightly batch | PRODUCTION-REAL (single developer Mac) | `deploy/com.emporion.nightly.plist` (launchd 13:30 host-local), `deploy/com.emporion.preopen.plist` (05:00), `scripts/run_nightly_batch.sh` | Runs on one workstation via launchd, not on server infra. Single point of failure. |
| Deploy | PRODUCTION-REAL | `render.yaml` (free plan, auto-deploy on commit, health `/api/health`) | Free tier sleeps when idle. |
| Health / observability | PARTIAL | `server.py` `/api/health` (static `status: ok`, `mode: paper`, `schwab_core`, deploy SHA); `operational_health.py`; `data_quality.py` | Health is hard-coded "ok" and does not reflect data freshness. No metrics, alerting or paging stack. |
| Web console | PRODUCTION-REAL | `web/` (8 tabs), `scripts/build_web.py`, `scripts/vv_console.mjs` | Membership/sign-in routes retired (410). |
| iOS | PAPER-REAL (build-only CI) | `ios/TradeDesk`, `ios/HedgeDeskObjC`; `iphone.yml` (unsigned simulator build) | Not distributed. |
| Supabase | PARTIAL | `supabase/migrations/*market_context_snapshots*.sql`, `supabase/schema.sql` | Stores market-context snapshots. The Postgres control plane in `EMPORION_TARGET_ARCHITECTURE_CODEX.md` §8 is target state. |
| Tests / coverage | VERIFIED | (measured) 1325 passed; 80% branch | — |

## 10. Investor profile / suitability inputs

| Capability | Status | Evidence path | Notes |
|---|---|---|---|
| Account record | PAPER-REAL (minimal) | `domain/models.py` `Account` (account_type: individual/IRA/Roth/trust; equity; cash; approval flags; disclosure ack) | No investor-profile fields. |
| Risk tolerance, objectives, time horizon, liquidity needs, net worth | ABSENT | Search for `risk_tolerance`, `investment_objective`, `time_horizon`, `suitability` etc. found nothing in `hedge_desk/`, `web/` or `ios/` | — |
| Account equity input | PAPER-REAL | `account.py` `read_account_equity` (`ACCOUNT_EQUITY` env or gitignored file) | Not configured in the latest report. |
| Watchlist-only research input boundary | PAPER-REAL | AGENTS.md "Research input boundary"; `nightly.py` `_watchlist`; `short_research_board.py` (uses report watchlist) | The watchlist is the only user input. Positions and holdings are deliberately excluded. |
| Accredited / qualified-purchaser verification | ABSENT | FINRA map ("no verification is implemented") | — |
| Tier/entitlement mapping | STUB (retired) | `tier_access.py`, `membership.py` | Membership surfaces are retired. |

## Top 10 strengths

1. **Static safety boundaries enforced by tests.** AST tests stop agents computing RoR or building validated risk inputs, and keep broker/network clients out of the paper runtime (`tests/test_architecture_boundaries.py`). CI also greps for order APIs.
2. **Fail-closed data plane with reason codes.** Transports are injected and CI is hermetic (`data/providers.py`, `data/feed_base.py`). The measured suite passes with the network disabled.
3. **Broad keyless official macro and rates coverage.** 22 sources were LIVE in the 2026-11-19 report (`market_context.py`, `open_market_feeds.py`).
4. **Content-addressed lineage everywhere.** Covers batch manifests, AM report hashes, decision hashes and the audit hash chain (`data/batch.py`, `audit.py`, `execution_gate.py`).
5. **Executable-side option economics in Decimal,** with liquidity, open-interest and staleness gates (`options/spreads.py`, `options/scanner.py`, `risk/ruin.py`).
6. **Textbook-referenced BSM N(d2) and IV inversion** with exact reference cases, honestly labeled risk-neutral (`risk/win_probability.py`).
7. **Layered gates:** data, compliance, portfolio, risk, human approval bound to the plan hash, and a non-overridable release gate (`core/decision.py`, `paper/workflow.py`, `release.py`).
8. **Paper lifecycle depth:** assignment, expiration, ex-dividend, stale/partial fills and plan-bound closes (`paper/runner.py`, `paper/settler.py`).
9. **Strong CI/CD hygiene:** 3-version matrix, SHA-pinned actions, CodeQL, secret scan, golden master, load and traversal tests (`.github/workflows/ci.yml`).
10. **Honest disclosure culture.** Real versus synthetic is labeled, a claims-lint runs in CI, and limitations are self-reported (`DESK_COVERAGE_AUDIT_2026-11-16.md`, `test_public_claims.py`, `ENGINEERING_LESSONS.md`).

## Top 15 observed gaps (things a professional desk has that this repo lacks or only stubs)

1. **No real-time or licensed options data.** There is no OPRA/NBBO feed. Chains are Cboe *delayed* with possible automated-use license limits. CI asserts `REAL_TIME_NBBO_ABSENT` (`ci.yml`; `DATA_SOURCE_ARCHITECTURE.md`).
2. **No historical options or survivorship-safe equity data, so no real backtest.** `replay.py` and `models/splits.py` run on synthetic data only (STATUS.md blockers #1, #2, #4).
3. **RoR model unvalidated.** `0.1.0-unvalidated`, the validator allowlist holds only fixture/test IDs, and `ROR_CONVENTIONAL_VV_APPROVED` is false (`risk/ruin.py`, `release.py`).
4. **No OMS/EMS.** There are no order types, routing, FIX, order state machine or execution algos. Only paper plan open/close exists (`paper/workflow.py`; CI broker grep).
5. **No vol surface, portfolio Greeks or Greek-based limits.** IV is per leg and Greeks come from the vendor (`cboe_chain.py`, `options_seed.py`). Portfolio limits use max-loss only (`backoffice/portfolio.py`).
6. **No VaR/ES, Monte Carlo, or position-based stress.** Stress uses hard-coded dollar shocks per desk (`portfolio_stress.py`).
7. **Kill switch is a dataclass flag.** There is no operator control, persistence or DR test (`execution_gate.py`; release item `KILL_SWITCH_AND_DR_TESTED`).
8. **Back office is hash-comparison only.** There is no broker statement ingestion, mark-to-market P&L, tax lots, NAV, settlement or corporate-action processing (`backoffice/reconciliation.py`).
9. **No WORM books and records or retention.** The JSONL journal is a local file (`audit_store.py`; FINRA map 17a-4 row; STATUS.md blocker #5).
10. **No investor profile or suitability.** There are no risk tolerance, objectives or horizon fields. Options approval is a boolean, not leveled (`domain/models.py`, `compliance/account_gate.py`).
11. **Desks 3, 4 and 6 run on synthetic economics.** Desk 2 has no consensus/estimates feed, and Desk 5's short interest is key-gated with no borrow/locate data (`arbitrage.py`, `dividends.py`, `futures_events.py`, `short_interest_service.py`).
12. **No futures market data (CME curves, settlements, specs)** and no news wire. Event data are leads only (`DESK_COVERAGE_AUDIT_2026-11-16.md`).
13. **Real nightly runs on one workstation's launchd.** `/api/health` is a static "ok" that does not reflect data health, and there is no metrics or alerting stack (`deploy/*.plist`, `server.py`).
14. **No measured track record.** The paper outcome log and Yellow Sheets have 0 entries, so stat inference returns `INSUFFICIENT_SAMPLE` (`artifacts/am-report-latest.json`, `ci.yml`).
15. **Governance and threshold inconsistencies:**
    - The re-scope records a GP choice of Schwab "risk-gated AUTO execution", which conflicts with SOUL/AGENTS paper-only (`MVP_RESCOPE_2026.md`).
    - Per-trade loss limits disagree: 1% in `RiskPolicy` versus 2% in `position_sizing.py`.
    - Probabilities are shown on delayed data (`cboe_chain.py` `spread_probabilities`) versus SOUL order #4.
    - STATUS.md and README are stale on the existence of broker and data adapters.
