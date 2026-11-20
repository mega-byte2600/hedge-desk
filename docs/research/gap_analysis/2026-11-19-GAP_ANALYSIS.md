# Emporion gap analysis: trade-desk scale, Wall Street and AI-quant benchmarks

- **Date:** 2026-11-19. **Requested by:** the GP.
- **Status:** research input for GP decision. **VERIFIED** where marked (measured by a command). **Not VALIDATED** until the GP reviews it.
- **Boundary:** this document proposes; it authorizes nothing. SOUL.md and AGENTS.md govern. Paper-only stays in force. No agent calculates Risk of Ruin. Licensed exam material is not reproduced; the knowledge baseline cites public outlines only.

## Supporting evidence (same folder)
| File | What it is |
|---|---|
| [`inventory.md`](inventory.md) | Capability inventory with a file path for every claim. Full suite run offline: **1,325 passed, 80% branch coverage (VERIFIED)** |
| [`benchmark.md`](benchmark.md) | Institutional desk reference architecture, 2026 regulatory changes, AI-quant firms (High-Flyer, Man, Two Sigma, Bridgewater…), OSS agent frameworks, failure modes, 12-dimension scorecard |
| [`academic_best_practices.md`](academic_best_practices.md) | Peer-reviewed and preprint research, top-program academics, regulators, practitioner/community channels; 39 practices with evidence tiers; 14 red flags |
| [`knowledge_baseline.md`](knowledge_baseline.md) | FINRA SIE/7/4/9-10/24/57/63/65/66 and CFA I–III from public outlines; suitability profile schema; agent curriculum |
| [`tools.md`](tools.md) | Connectors, plugins, skills: have, installed-but-unconnected, available, missing |

---

## 1. Bottom line

1. **Emporion is strongest exactly where published AI-trading projects are weakest.** A 2026 review of seven open-source agent-trading codebases found none enforced stop-losses or position limits outside the LLM ([SoK, arXiv 2609.19705](https://arxiv.org/abs/2609.19705)). Emporion enforces deterministic, fail-closed gates in code, binds human approval to a plan hash, and uses AST tests to stop agents computing Risk of Ruin (`tests/test_architecture_boundaries.py`).
2. **It is a research-and-paper desk, not yet a trade desk.** The gaps that separate it from a professional desk are, in order: licensed options data, a real backtest with overfitting controls, a measured paper track record, an investor-profile and suitability engine, portfolio-level risk (Greeks, VaR/ES), reliable operations, and in-repo agent orchestration. Execution is deliberately absent.
3. **The evidence does not support autonomous LLM alpha.** Contamination-free and live benchmarks from 2025–2026 (FINSABER, StockBench, Agent Market Arena, LiveTradeBench) find most LLM agents fail to beat buy-and-hold. The firms that report success (Man Group's AlphaGPT, Two Sigma) use agents to widen research and keep humans and hard gates in charge. The right target for Emporion is **agent-accelerated research inside deterministic gates**, measured on forward paper results.
4. **"End-to-end trading by suitability" is achievable as a staged path**, ending at human-approved paper trades now and, only after a separately authorized release, read-only and then gated live execution. Section 6 lays it out.

## 2. Scorecard (0–5, benchmark dimensions)

Scale from `benchmark.md` §D: 0 absent · 1 ad hoc · 2 documented · 3 credible OSS standard · 4 audited/enforced · 5 top-firm practice. Scored on verified code evidence; a control with no production caller scores at most 2. Execution, clearing and suitability are scored as design readiness.

| # | Dimension | Score | Why (evidence) | What 5 looks like |
|---|---|---|---|---|
| 1 | Data quality, latency, provenance | **3** | Fail-closed registry with reason codes, content-addressed lineage, 22 live keyless macro/rates feeds, honest delay labels. But options are Cboe *delayed* with an automated-use licence tension, no OPRA/NBBO, no point-in-time security master | OPRA/NBBO with validation, PIT security master and corporate actions, cross-source corroboration |
| 2 | Pre-trade risk controls, kill switch | **3** | `risk_gate` reason codes (stale quote, liquidity, undefined max loss), portfolio and drawdown gates, 2% sizing. Kill switch is a dataclass flag with no operator control or drill; **1% vs 2% per-trade limit conflict** | 15c3-5-grade documented limits, change control, drilled quick-disable |
| 3 | Execution capability (paper fidelity) | **2** | Deep paper lifecycle (assignment, expiry, ex-div, stale fills) but fills at the quote, flat commission, no impact/latency model, no backtest↔paper parity | Same strategy code in backtest/paper/live with a cost model and TCA |
| 4 | Compliance and suitability design | **2** | Deterministic policy engine, claims lint in CI, disclosure gate, traceability hash. **No investor profile, no suitability check, options approval is a yes/no flag, not levels**; journal is not WORM | Reg BI/2111/2360 workflow, leveled approvals, 3110 supervision, 17a-4 records |
| 5 | Model governance | **2** | Registry, quorum, purged splits exist but are exercised only by synthetic war games. RoR model `0.1.0-unvalidated`. No-self-approval rule is written and enforced by review | Model inventory, independent validation, outcome monitoring |
| 6 | Backtesting and evaluation rigor | **1** | No historical backtest engine or historical chains. **No deflated Sharpe, no PBO, no trial log, no multiple-testing bar (VERIFIED by grep)**. Paper log has 0 outcomes | Purged CV, trial counts, DSR/PBO, post-cutoff and regime-split evaluation, forward test vs buy-and-hold |
| 7 | Agent orchestration | **1** | Six Hermes profiles and Muse are specs outside the repo; learning ledger not wired; quorum only in war games | Role lanes with typed handoffs, debate, deterministic gate after, human approval |
| 8 | Observability, reproducibility | **3** | Hash-chained audit, decision hashes, reason codes everywhere. `/api/health` is a static "ok"; no metrics or alerting; no WORM | Replay of any decision; immutable records; real-time alerts |
| 9 | Security | **3** | Secret scan, CodeQL, SHA-pinned actions, Claude Code deny rules on secrets. No prompt-injection / Unicode defenses for news or LLM inputs; no written incident-response plan | Reg S-P-style incident program, adversarial-news defenses, sandboxed model code |
| 10 | Human oversight, separation of duties | **4** | Human approval bound to plan hash; non-overridable release gate; agents may not approve their own risk changes; CI gates fail closed | Plus drilled overrides and a standing review committee |
| 11 | Research breadth | **3** | SEC XBRL and filings, FRED/Treasury/NY Fed/BLS/BIS, Cboe chains, GDELT leads, COT. No estimates/consensus, licensed news, transcripts, futures curves, borrow data | Multi-asset licensed and alternative data, firm-wide RAG over vetted research |
| 12 | Scalability, cost, reliability | **2** | Real nightly runs on one Mac via launchd; Render free tier sleeps; GitHub cron best-effort | Redundant scheduled infrastructure with monitoring |

**Total 29 / 60.** Credible-OSS level (3) on data, risk gates, observability, security and research. Above it on human oversight (4). Below it on backtest rigor and agent orchestration (1). Top-firm practice would be about 55–60.

## 3. Governance conflicts to resolve first (GP decisions)

These were found by the inventory and should be settled before building further.

| # | Conflict | Evidence | Options |
|---|---|---|---|
| C1 | **Auto execution vs. paper-only.** The re-scope records a GP choice of Schwab "risk-gated AUTO execution"; SOUL/AGENTS keep paper-only, and the code follows SOUL | `docs/MVP_RESCOPE_2026.md`, `docs/TECH_ROADMAP.md` Tier 5 vs SOUL.md, AGENTS.md | (a) Keep paper-only and mark the re-scope superseded; (b) authorize a *separately reviewed* read-only release first, live later via `release.py` evidence |
| C2 | **Per-trade loss limit 1% vs 2%** | `risk/ruin.py` `RiskPolicy.maximum_single_trade_loss_fraction = 0.01` vs `position_sizing.py` `MAX_LOSS_FRACTION_EQUITY = 0.02` | SOUL order 7 fixes 2% as the immutable maximum; 1% is stricter. Decide whether the gate should be 1% (stricter than the cap) or 2%. This is a risk-control change: needs independent review |
| C3 | **Probabilities on delayed data** | `cboe_chain.py` `spread_probabilities` shows PoP/EV from delayed IV; SOUL order 4 forbids probability claims on delayed data | Hide the column when data is delayed, or relabel it "reference only, delayed" and get explicit GP sign-off |
| C5 | **Default-deny strategies in the suitability design** | `knowledge_baseline.md` §19 proposes DENY for naked calls/naked index and futures, because unlimited loss cannot fit the immutable 2% cap without a stop | Confirm default-deny, or define the stop/size rule that would make them fit 2% |
| C4 | Stale docs | `docs/architecture/STATUS.md` and README still say no broker or market-data adapter exists | Update in a docs-only PR |

## 4. Gap register (prioritized)

Priority: **P0** safety, governance or reliability, cheap; **P1** needed to be a credible desk; **P2** scale and breadth. "Closes with" lists tools we already have first.

| ID | Gap | Pri | Closes with (have → need) | Owner lane | Effort |
|---|---|---|---|---|---|
| G1 | Resolve C1–C5 | P0 | GP decision; docs PR | GP | S |
| G2 | `/api/health` is static "ok"; no freshness-aware health or alerting | P0 | Repo `carpedata` + `/datalink-watch` skills; `data_quality.py`, `freshness.py` already compute it | DATA / ENGINEER | S |
| G3 | Real nightly batch runs on one Mac (single point of failure) | P0 | Cloud scheduled tasks or GitHub Actions with secrets; keep launchd as backup | ENGINEER | M |
| G4 | Kill switch is a flag: no persisted operator control, no drill | P0 | Persisted switch + console control + quarterly drill record (`release.py` item `KILL_SWITCH_AND_DR_TESTED`) | RISK / ENGINEER | M |
| G5 | **No investor profile / suitability / options levels** | P0 | New deterministic `suitability` module from `knowledge_baseline.md` §schema (FINRA 2111 profile factors, 4512 account info, 2360 levels); Supabase table; gate strategies by level. Research-only use: it filters what the desk *shows* the GP, it does not recommend | COMPLIANCE / RISK | M |
| G6 | No licensed or real-time options data; no historical chains | P1 | **Have:** Schwab market data (token), FMP, Twelve Data (no options). **Need:** finish Alpha Vantage connection (installed, incomplete) or the planned ThetaData ($80/mo, `SUB_100_DATA_STACK.md`); historical chains for backtests | DATA (GP buys) | M |
| G7 | **No real backtest and no overfitting controls** | P1 | Backtest engine with bid/ask costs reusing the paper fill code (parity); trial log; deflated Sharpe and PBO; t>3 / FDR bar; mandatory buy-and-hold baseline; wire `models/splits.py` purged walk-forward to real runs | QUANT | L |
| G8 | **No track record (0 paper outcomes, 0 Yellow Sheets)** | P1 | Start the forward paper log now; it is the only evidence that counts per the 2025–26 benchmarks | GP / RESEARCH | S (start), ongoing |
| G9 | No vol surface, portfolio Greeks, Greek limits, VaR/ES, position-based stress | P1 | Surface fit from chains; aggregate Greeks; Greek and concentration limits in `PortfolioPolicy`; historical-sim VaR/ES on paper book (deterministic, reference cases) | QUANT / RISK (independent review) | L |
| G10 | Records not WORM; no retention | P1 | Supabase storage or object storage with object lock; retention policy; export | ENGINEER / COMPLIANCE | M |
| G11 | Agent orchestration not in repo | P2 | Typed role lanes (analysts → bull/bear → risk check → GP), each step recorded with model/version/prompt hash; deterministic recomputation of every numeric claim; wire `learning_ledger.py` append-only; Claude Code dynamic workflows for research fan-out | ORCHESTRATOR | L |
| G12 | LLM/news safety: prompt injection, Unicode tricks, look-ahead | P2 | Unicode normalization, source provenance and cross-source corroboration, model training-cutoff log, evaluate LLM signals only after cutoff | SENTRY / DATA | M |
| G13 | Missing research data: estimates/consensus, transcripts, licensed news, borrow/locate, CME curves | P2 | **Have:** FMP (estimates, calendars, insider), equity-research plugin. **Need:** FINRA short-interest keys (configured by GP), Bigdata.com or similar for transcripts/news, a futures-curve source for Desk 6 | DATA | M |
| G14 | Back office: no mark-to-market P&L, tax lots, NAV, statement ingestion | P2 | Daily MTM of the paper book; lot ledger; reconcile against Schwab statements (read-only, not exposed to browser) | BACK OFFICE | M |
| G15 | Knowledge not encoded | P2 | Turn `knowledge_baseline.md` into (a) rule-referenced tests for compliance gates, (b) per-agent curriculum prompts with public citations | COMPLIANCE / ORCHESTRATOR | M |
| G16 | Execution (OMS/EMS, broker orders) | Gated | **Only after C1 is decided and `release.py` evidence exists.** Design to 15c3-5-style pre-trade checks and RN 15-09 algo SDLC. Broker connectors that can trade (IBKR, Questrade, Clear Street) exist in the directory but are out of bounds today | GP authorization required | XL |

## 5. Where Emporion stands vs. the field

| | Top firms (Man, Two Sigma, Bridgewater) | Credible OSS (TradingAgents, FinRL-X, RD-Agent, Nautilus) | Emporion today |
|---|---|---|---|
| AI role | Agents widen research; humans approve; hard limits outside the model | Agent graphs often decide trades; limits frequently inside the LLM | Agents research; deterministic gates and the GP decide |
| Data | Licensed real-time, PIT, alt data | Free/EOD, some PIT fixes added in 2026 | Free official + delayed options, honest labels |
| Validation | Independent validation, outcome monitoring | Walk-forward, rarely DSR/PBO | Gates and reference cases; **no real backtest yet** |
| Execution | OMS/EMS, TCA, best-ex | Paper/live via Alpaca etc. | Paper only, by design |
| Evidence of edge | Proprietary; reported signals in production | Self-reported, often short windows | None yet (0 paper outcomes) |

## 6. Staged path to "end-to-end by suitability"

Each stage has an exit test. Nothing advances without the GP.

| Stage | What runs | Exit test |
|---|---|---|
| **S0 Fix foundations** (P0) | C1–C5 decided; freshness-aware health; nightly off the single Mac; drilled kill switch | Health turns red when data is stale; two weeks of on-time nightly runs |
| **S1 Suitability-gated research** | Investor profile + options level filter which desks and structures are shown; agents research the watchlist; every claim recomputed | Every candidate carries `suitability_check` reason codes; zero strategies shown above the GP's level |
| **S2 Evidence engine** | Licensed chains; backtest with costs + purged walk-forward + DSR/PBO + buy-and-hold baseline; trial log | A strategy is "research-promotable" only with DSR above threshold, PBO below threshold, and a beaten baseline after costs |
| **S3 Forward paper track record** | Daily human-approved paper trades from promoted strategies; MTM P&L; Greeks and VaR on the paper book | 6+ months / adequate sample of paper outcomes; stat inference leaves `INSUFFICIENT_SAMPLE` |
| **S4 Read-only brokerage** (separately authorized) | Schwab read-only positions reconciled server-side; not exposed to the browser | Reconciliation clean for N weeks; security review (`claude-security`) passed |
| **S5 Gated execution** (separately authorized; may never happen) | OMS with 15c3-5-style checks, kill switch, per-order GP approval | All `release.py` evidence items true, including counsel sign-off and validated RoR |

## 7. Recommended next three moves

1. **GP decides C1–C3 and C5** (one sitting). Everything else depends on C1.
2. **Build G5 (suitability profile and options levels) and G2 (honest health)** as two small PRs. Both are deterministic, testable, and inside the paper boundary.
3. **Start G8 today** (forward paper log) and **buy the options data for G6/G7**, because a track record and a real backtest are what every benchmark says matters.

## Sources
Every external claim above is cited inline or in the supporting files, which carry the full source lists with evidence tiers.
