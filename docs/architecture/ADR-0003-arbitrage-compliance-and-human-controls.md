# ADR-0003: Arbitrage Research, Compliance Control, and Human Decision Plane

- Status: Accepted for implementation planning
- Date: 2026-08-21
- Scope: Paper research and paper trading only

## Decision

Add two specialized roles to the orchestration while keeping control authority
outside the agent swarm:

1. **Arbitrage Research Agent** - discovers and explains possible identity or
   relative-value dislocations.
2. **Compliance Agent** - gathers regulatory/licensing evidence and proposes
   classifications to a deterministic Compliance Policy Engine.

Neither role can authorize a trade. Alpha-agent votes cannot override risk,
compliance, or the human decision point.

## Arbitrage taxonomy

The Arbitrage Research Agent must label every idea as exactly one of:

- `IDENTITY_ARBITRAGE`: a contractual payoff identity appears violated before
  all implementation costs;
- `RELATIVE_VALUE`: convergence is a statistical hypothesis;
- `EVENT_SPECULATION`: outcome or direction is uncertain.

Earnings up/call and earnings down/put is `EVENT_SPECULATION`, not arbitrage.
Pairs, calendar spreads, merger spreads, and most index-event strategies are
`RELATIVE_VALUE`. Put-call parity and European index boxes may begin as
`IDENTITY_ARBITRAGE`, but only deterministic executable-side calculations can
promote them to a net-edge candidate.

## Arbitrage MVP

Add a paper-only **European Index Box/Parity Observer** after the first common
control contracts are implemented. European-style cash-settled index options are
cleaner for this test than American-style physical equity options because they
avoid early exercise and physical delivery.

Result vocabulary:

- `THEORETICAL_DISLOCATION`
- `NET_EDGE_CANDIDATE`
- `NOT_EXECUTABLE`
- `INSUFFICIENT_DATA`
- `NO_TRADE`

The deterministic calculator uses synchronized executable bid/ask sides for all
legs, official contract multiplier/settlement, fees, financing/day count,
slippage, depth, and a partial-fill reserve. Midpoint-only economics are
prohibited. Paper observation cannot prove simultaneous execution and is never
called risk-free, sure, or guaranteed.

Agents never calculate parity, terminal payoff, financing, net edge, hedge ratio,
margin, portfolio exposure, or RoR.

## Off-exchange inference boundary

The research system may ingest FINRA TRF prints, delayed FINRA ATS/non-ATS
transparency, licensed TAQ, and SEC Form ATS-N venue descriptions. It may produce
an `institutional_like_off_exchange_flow` STAT model output under the evidence
standard in `DATA_SOURCE_ARCHITECTURE.md`.

It may not identify a hedge fund, trader, subscriber, hidden order, or intent.
Confidential CAT data and live hidden ATS order books are not public. Observed
off-exchange volume is distinct from model-inferred institutional flow and agent
interpretation.

## Compliance architecture

The Compliance Agent is an evidence assistant, not the binding control. It may:

- retrieve official rules and source terms;
- classify instruments, communications, data rights, and regulatory questions;
- propose reason codes and escalation;
- prepare an auditable explanation.

An independently versioned deterministic Compliance Policy Engine issues the
binding `PASS`, `REVIEW`, or `BLOCK`. Missing, stale, conflicting, or uncertain
evidence fails closed. Only an approved policy release can alter a control;
agents cannot activate rule updates.

Required gates:

1. **Ingest:** allowlisted source/license, provenance, timestamps, content hash,
   rate limits, privacy, MNPI quarantine, and redistribution rights.
2. **Research:** primary-source claims, point-in-time evidence, fact/model/agent
   labels, and no restricted or nonpublic information.
3. **Strategy:** paper-only allowlist, defined maximum loss, no manipulation,
   no naked short options, short equity, 0DTE, or physical-delivery futures in
   the initial MVP.
4. **Account/rule:** hypothetical approval tier, current OCC disclosure,
   effective broker/intraday-margin regime, buying power, contract limits, and
   jurisdiction.
5. **Risk/compliance:** immutable risk artifact plus compliance policy decision;
   either control can block.
6. **Human:** named review of the exact immutable candidate; approval cannot
   override a block.
7. **Publication:** prominent paper/hypothetical label, full assumptions and
   costs, losers and limitations, no sure/easy/guaranteed claims.
8. **Audit:** append-only evidence, model/code/data/policy versions, raw agent
   output, reason codes, human token, and tamper-evident hashes.

Calling software open source, research, paper, or not advice is not a safe harbor.
Securities/commodities counsel must review before monetization, individualized
signals, account connection, public recommendations, pooled capital, or live
trading.

## Human control plane

The human decision packet must show separate panels for:

- `OBSERVED_STATISTIC`;
- `STAT_MODEL_OUTPUT` with confidence interval/calibration;
- `BIG_MODEL_OUTPUT` integrating validated research inputs;
- `AGENT_INTERPRETATION` and independent skeptic case;
- `RISK_POLICY_DECISION`;
- `COMPLIANCE_POLICY_DECISION`;
- maximum loss, costs, liquidity, timing, and unresolved evidence;
- `HUMAN_CONTEXT` and final `HUMAN_DECISION`.

The decision choices are `APPROVE_PAPER`, `REJECT`, and
`REQUEST_MORE_EVIDENCE`. Approval is bound to the candidate hash, policy/model
versions, paper account, authorized size, and expiry time. Any material change
invalidates it.

## Corporate motto boundary

**Making money overnight - the dream: making money while you sleep.**

The system searches, validates, calculates, red-teams, and prepares decisions
while the user sleeps. The motto is aspirational. It cannot appear as a
performance guarantee, substitute for evidence, or reason to override a control.

## Release tests

- Agent-calculated or relabeled statistics/model/risk/compliance values: block.
- Missing source license, provenance, or point-in-time evidence: block.
- `p >= 0.005` confirmatory claim or missing 95% CI: label exploratory; block
  policy use.
- Named-actor claim from dark/off-exchange inference: block publication.
- Sure/easy/guaranteed/proven-profit promotion: block publication.
- Missing current options disclosure/approval or undefined loss: block.
- Missing or stale risk/compliance decision: block.
- Human token missing, expired, or bound to another hash: block.
- Human attempts to override risk/compliance block: block and audit.
- Any production broker endpoint/dependency in the MVP: fail CI.
