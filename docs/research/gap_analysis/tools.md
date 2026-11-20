# Tools, integrations, skills — have vs. missing (as of 2026-11-19)

Source: this Claude session's connector list (`ListConnectors`), enabled plugins (`ListPlugins`), skills, and a connector-directory search. "Connected" means usable from Claude sessions on this account. None of these are wired into the hedge-desk runtime unless noted.

## Connected and usable now
| Integration | What it gives the desk | Fit / limits |
|---|---|---|
| **FMP** (Financial Modeling Prep) | Quotes, history, fundamentals, statements, analyst estimates, calendars, SEC filings index, insider trades, Senate trades, COT, commodities, forex, crypto, DCF, news | Research-grade; good for Desk 2 (earnings), Desk 4 (dividends), Desk 5 (short research). Licensing for redistribution must be checked before anything is committed |
| **Twelve Data** | Prices, 60+ technical indicators, fundamentals, dividends, earnings, ETF/fund data, SEC/insider/institutional | **No options, no indices, no bonds** (per its own server notes). Cannot replace an options chain |
| **Supabase** | Postgres, auth, storage, edge functions | Already in repo (`supabase/`). Candidate home for an audit/ledger store and an investor-profile table |
| **Google Drive / Notion** | Document storage, notes, knowledge base | Good for the GP's licensed study notes (kept private, never committed) |
| **Arca (FDA/PubMed)** | Biomedical regulatory data | Niche: biotech catalyst research (PDUFA dates, CRLs) for Desk 2 / Desk 5 |
| **Claude Docs / Artifacts** | Shareable reports, dashboards | Morning packet / GP brief publishing |
| **Claude in Chrome** | Drive any website as the user | Fallback for sites with no API; must respect site terms |

## Installed but not connected
| Integration | Status | Value |
|---|---|---|
| **Alpha Vantage MCP** | `connect_incomplete` | Options (historical + realtime on premium), fundamentals, news sentiment, economic indicators. Already a key-gated adapter in `hedge_desk/data/providers.py`. **Action: finish connecting (GP)** |

## Plugins and skills available
| Plugin / skill | Use for the desk |
|---|---|
| **equity-research** (earnings, earnings-preview, initiate, thesis, catalysts, sector, screen, model-update, morning-note) | Directly maps to Desk 2 (earnings), Desk 5 (short thesis), morning packet. Strongest ready-made research workflow set available |
| **engineering** (architecture/ADR, code-review, debug, deploy-checklist, incident-response, testing-strategy, system-design, tech-debt) | ADRs for the gap roadmap, incident runbooks |
| **claude-security** | Repo-wide vulnerability scan + verified patches. Recommended before any brokerage-adjacent release |
| **feature-dev**, **superpowers** (TDD, systematic debugging, plans, subagent-driven development) | Build discipline for the roadmap |
| **Databricks** (ML training, MLflow evaluation, model serving, vector search, pipelines) | Only if the desk outgrows Supabase/files. A real path for model registry + MLflow-style model risk records, but adds cost |
| **dataviz**, **frontend-design** | Console / dashboard quality (UI/UX scored 6 in review round 2) |
| **Repo skills** (`.claude/skills`: kickoff, build, review, datalink-audit, harden-datalink, web-perf, ship, datalink-watch; **carpedata**) | Governed build/data workflows; `/loop` for monitoring |
| **Dynamic workflows** (Claude Code `use a workflow` / `/deep-research`) | Parallel research swarms, codebase-wide audits, cross-checked findings |
| **Scheduled tasks** (cloud) | 24/7 runs without a laptop: nightly research, data-health watch, morning packet |

## Not connected but available in the connector directory (GP decision; cost/licensing)
| Integration | What it would close | Boundary note |
|---|---|---|
| **Interactive Brokers (IBKR)** | Real account, positions, price snapshots/history, order instructions | **Execution-capable.** SOUL/AGENTS keep Emporion paper-only; read-only market data would need a separately reviewed release |
| **Questrade** | Portfolio, real-time data, option/order instructions | Same boundary as IBKR (and Canada-focused) |
| **Clear Street** | Stocks + options research, instrument data, balances/positions | Same boundary for account endpoints |
| **Schwab Advisor Services** | RIA custodial data | For advisors only; not a fit for the GP's retail Schwab account. Schwab market data already exists in repo (`hedge_desk/brokers/schwab_market_data.py`, market-data-only) |
| **LSEG / LSEG AI** | Institutional pricing, curves, option valuation, RFQ | Enterprise licence; overkill at current scale |
| **FactSet AI-Ready Data** | Institutional fundamentals, estimates consensus, prices | Enterprise licence |
| **Morningstar** | Fund/equity research, ratings, holdings | Useful for Desk 4 (dividends) and ETF context |
| **Bigdata.com** | Cited news, filings, transcripts, sentiment | Fills the news/transcript gap with citations |
| **TEXT TO QUANT** | Plain-English backtests with "honesty flags" | Third-party backtester; use only as a cross-check, never as the authoritative engine |
| **D&B Risk Analytics** | Counterparty/company credit risk | Low priority |

## Still missing (no connector found in this session's search)
- **OPRA-grade real-time options NBBO and full chains with greeks** (e.g., Cboe DataShop, Databento, Polygon/Massive, ORATS, Tradier). The repo uses delayed Cboe chain pages (`hedge_desk/cboe_chain.py`); `ready_for_live_production_data` is false with `REAL_TIME_NBBO_ABSENT`
- **Corporate actions / reference data** service (splits, special dividends, option contract adjustments)
- **Short interest / borrow / locate data** (FINRA short interest is snapshot-only and `UNCONFIGURED`)
- **Earnings call transcripts** (Bigdata.com could fill this)
- **FRED / Treasury / SEC EDGAR** do not need connectors: the repo already uses them keylessly
