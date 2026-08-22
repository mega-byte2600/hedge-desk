# ADR-0002: Earnings Event Paper Desk MVP

- Status: Accepted for implementation planning
- Date: 2026-08-21
- Scope: Paper research and paper trading only

## Decision

Add an **Earnings Event Paper Desk** as the second MVP in the broader agentic
financial-research orchestration. It studies short-horizon reactions around U.S.
equity earnings releases and creates, at most, human-pending paper proposals.

The MVP does not promise "two sure picks" per day. It may produce zero, one, or
more candidates. A forced daily quota is prohibited because it converts absence
of edge into mandatory risk-taking.

## Trade architecture

Each event enters a deterministic trade-expression tournament. It may produce
one alpha expression and, where required, one separately justified hedge:

1. **Straight equity:** long or short common equity with a deterministic holding
   window and borrow/locate constraint where applicable.
2. **Market/sector-neutral equity:** long or short the issuer against a
   deterministic beta/factor hedge.
3. **Defined-risk options:** a bullish or bearish vertical only when the net
   payoff after implied move, volatility crush, spread, slippage, assignment,
   and liquidity is superior under the locked policy.
4. **No trade:** mandatory when no expression clears evidence and risk gates.
5. **Portfolio hedge leg:** a separately sized sector/index hedge designed to
   reduce measured beta, factor, volatility, or gap exposure. It is not assumed
   to make money independently and must not be mislabeled as a second alpha pick.

A bullish surprise does not mechanically imply buying a call, and a bearish
surprise does not mechanically imply buying a put. The options market may have
priced a larger move; implied volatility can collapse after the release; guidance,
quality of earnings, positioning, liquidity, and the initial price response can
reverse the apparent direction.

### Documented institutional research basis

Public evidence supports testing event-driven and post-earnings effects, not
copying an undocumented proprietary hedge-fund rule. NBER research documents an
[earnings announcement premium](https://www.nber.org/papers/w13090) and research
on [investor inattention and delayed earnings response](https://www.nber.org/papers/w11683).
Separate research shows that transaction costs materially reduce implementable
post-earnings-announcement-drift returns. These are hypotheses for point-in-time
replication, not proof that a current trade will work.

Delayed public holdings disclosures cannot reconstruct a hedge fund's event-time
signal, hedge, entry, exit, derivative exposure, or intraperiod trading. The desk
will reproduce documented public methods and compare them under current data and
costs; it will not claim to copy proprietary hedge-fund trades.

## Earnings Whispers boundary

[Earnings Whispers](https://www.earningswhispers.com/) may be evaluated as a
licensed expectations source. Its site describes earnings expectations,
sentiment, option tools, and post-earnings analytics. Its
[Terms of Service](https://www.earningswhispers.com/usage) state that service
information is for personal, non-commercial use and restrict reproduction,
distribution, and organizational sharing without prior written consent. The
terms also describe whisper numbers as frequently rumor-like and disclaim
accuracy, completeness, and timeliness.

Therefore:

- no crawler, scraper, credential automation, cache, redistribution, or public
  fixture may use Earnings Whispers content under the currently reviewed terms;
- an `earnings_whispers` source adapter remains disabled until written commercial
  permission, API/data-feed rights, retention rules, and redistribution limits
  are documented and approved;
- site content and credentials never enter GitHub issues, commits, logs, prompts,
  or agent memory;
- an individual user's subscription does not automatically authorize company,
  agent, swarm, or commercial-system use;
- the MVP must run with independent sources and synthetic fixtures.

## Permitted source design

The point-in-time evidence layer distinguishes:

- company earnings releases, SEC 8-K/10-Q filings, and investor-relations pages;
- confirmed release timestamp and before-open/after-close status;
- licensed consensus estimates and estimate timestamps;
- licensed option-chain quotes, implied move, volatility surface, volume, open
  interest, and underlying trades/quotes;
- company guidance, comparable-period actuals, restatements, and revisions;
- sector/index prices and hedge instruments;
- optional licensed whisper/sentiment source with explicit provenance.

Missing expectations data cannot be inferred by an agent and labeled as
consensus or whisper data.

## Event states

```text
SCHEDULED
  -> PRE_RELEASE_SNAPSHOT_LOCKED
  -> RELEASE_OBSERVED
  -> PRIMARY_SOURCE_VERIFIED
  -> DETERMINISTIC_SURPRISE_CALCULATED
  -> MARKET_RESPONSE_WINDOW_COMPLETE
  -> CANDIDATE | NO_TRADE
  -> DETERMINISTIC_RISK_PASS | REDUCE | REJECT
  -> HUMAN_PENDING
  -> PAPER_APPROVED | REJECTED
  -> CLOSED
```

Every transition is timestamped and fail-closed. Late, corrected, conflicting,
or unverified releases remain blocked.

## Deterministic calculation boundary

Versioned conventional software calculates and V&V validates:

- EPS/revenue/KPI surprise versus timestamped expectations;
- guidance delta on like-for-like definitions and periods;
- underlying gap, abnormal return, market/sector-relative return, volume, and
  post-release confirmation window;
- option bid/ask, implied move, realized move, volatility change, Greeks,
  payoff, break-even, maximum loss, transaction costs, and slippage;
- historical base rates using point-in-time membership and no revision leakage;
- alpha-leg scenario P&L and hedge-leg beta/factor exposure reduction;
- portfolio concentration, gap/stress loss, capital-at-risk, permitted size,
  and the authoritative RoR artifact.

Agents may retrieve, classify, compare, red-team, and explain these artifacts.
They may not generate authoritative earnings values, surprises, probabilities,
prices, Greeks, implied moves, hedge ratios, sizes, portfolio risk, or RoR.

## Candidate policy

A candidate requires all of the following:

- primary-source result verified and timestamped;
- validated expectations snapshot predating the release;
- material surprise or guidance change under a prespecified rule;
- post-release price/volume confirmation under a prespecified window;
- option liquidity and maximum-loss limits;
- deterministic expected net payoff favorable relative to implied move and costs;
- no unresolved earnings-definition, corporate-action, or data-quality conflict;
- independent deterministic risk result and pending human authorization.

Otherwise the correct output is `NO_TRADE`.

## Backtest and V&V design

The evaluation set is event-based, not a random row split. It must preserve
release timestamps, estimate vintages, option quotes, delisted issuers, earnings
calendar revisions, corporate actions, and sector/index state.

Required comparisons:

- calls after positive headline EPS surprise;
- puts after negative headline EPS surprise;
- surprise plus guidance;
- surprise/guidance plus price-volume confirmation;
- equity versus defined-risk options expression;
- straight equity versus beta/sector-neutral equity;
- unhedged versus deterministic sector/index hedge;
- no-trade threshold variants fixed before final out-of-sample evaluation.

Report hit rate, average/median net return, tail loss, drawdown, expected shortfall,
turnover, fill sensitivity, implied-volatility crush, event-time latency, and
performance by market/volatility regime. Do not optimize or select models on the
locked test period.

## MVP demonstration

Use synthetic and legally redistributable frozen fixtures for two historical-like
events:

- one verified positive surprise/guidance case;
- one verified negative surprise/guidance case.

For each, the demo shows evidence ingestion, deterministic calculation,
candidate/no-trade decision, independent risk, human-pending state, paper
authorization, monitoring, and deterministic close. At least one adversarial
fixture must show that the headline direction was wrong or that IV crush made the
obvious call/put unattractive.

## Success gate

The MVP succeeds when the architecture is reproducible, licensed, fail-closed,
and capable of falsifying the simple directional rule. It is not successful
merely because two hand-picked examples make money.

Forward paper trading begins only after locked out-of-sample evaluation. Live or
automatic execution remains deferred.
