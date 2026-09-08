# Emporion Product Positioning and Measurement

## Product origin

Emporion is the current implementation of a personal investment-research system that has been developed iteratively since 1998. The product should communicate that history as continuity of research practice, not as a claim of investment performance.

## Product thesis

Emporion is open investment research and decision infrastructure.

The user brings the watchlist, data, rules, models, and implementation choices. Emporion provides a structured research system around those inputs: candidate intake, specialized research desks, scenario analysis, Yellow Sheets, deterministic controls, and human review.

Core promise:

**Bring your watchlist. Research it your way.**

Ownership principle:

**Your choice. Your data. Your money.**

Brand statement:

**Your money should work as hard for you as you do for it.**

Point of difference:

**Risk of Ruin is not an afterthought. It is an independent constraint on every decision.**

North Star principle:

**Survive first. Compound second.**

That portfolio-survival discipline, including the explicit Risk of Ruin framing, was strengthened through input from Dr. Cooper.

The product must not imply guaranteed returns or that Emporion itself executes trades for users by default.

## User-controlled implementation modes

Emporion supports a continuum rather than one mandatory operating mode.

1. Research only. Import or connect a watchlist, inspect candidates, research through one or more desks, run scenarios, and document the thesis in a Yellow Sheet.
2. Decision ready. Produce structured candidate packets with thesis, evidence, invalidation criteria, sizing inputs, risk state, and a proposed execution plan for human review.
3. User-implemented automation. Because the system is open, a technically capable user may connect their own data, brokerage, execution logic, and controls and automate as much of their own workflow as they choose.

The repository's default product boundary remains paper/research oriented and does not silently enable live orders.

## Market problem

The problem is not lack of financial information. Users already have screeners, charts, research feeds, filings, calendars, news, and brokerage tools. The problem is fragmentation and inconsistent decision discipline.

Emporion's value is to move a user's own market ideas through a repeatable lifecycle:

**Watchlist → Candidate → Research → Scenario → Yellow Sheet → Risk of Ruin gate → Human decision → Outcome → Review → Learning**

The seven desks are capabilities inside this system, not seven unrelated products.

## Product architecture

Public architecture: seven research desks.

Current evaluated engine: six workflows.

Bonds & Rates is the seventh architecture desk and macro anchor until its evaluated engine path is connected.

Cross-cutting rails remain separate from desks: source provenance, deterministic risk, deterministic compliance, auditability, and human authorization.

## Web and iOS product contract

Web and iOS must mirror product semantics, not pixel layout.

Shared contract:

- EMPORION identity and Markets · Intelligence · Discipline brand
- seven-desk architecture and six-evaluated-workflow state until that state changes
- candidate identity and desk identity
- scenario terminology
- Yellow Sheet lifecycle
- explicit Risk of Ruin / portfolio-survival gate
- source/provenance terminology
- paper/research default boundary
- production website and repository links

Web emphasis: exploration, comparison, deep research, resources, larger data surfaces.

iOS emphasis: what changed, what needs attention, quick evidence review, Yellow Sheet capture, and decision status.

## North Star and KPI framework

Product North Star principle: **Survive first. Compound second.**

Operating North Star metric: **Weekly Researched Watchlist Decisions**.

A qualified event is a user-originated watchlist symbol or candidate that is reviewed with research/evidence, passes through the independent portfolio-survival risk state, and results in a documented Yellow Sheet decision, no-decision, or updated thesis.

Supporting KPIs:

- Watchlist connection or import rate
- Percent of imported symbols researched
- Time from watchlist import to first candidate review
- Percent of researched candidates with a Yellow Sheet
- Percent of Yellow Sheets with evidence
- Percent of Yellow Sheets with explicit invalidation criteria
- Percent of decision-ready candidates with completed Risk of Ruin review
- Cross-desk coverage per watchlist
- Weekly active researchers
- Week 1, Week 4, and Week 12 researcher retention
- Post-decision review completion rate
- Source/evidence open rate
- Export, fork, and contribution rate
- Crash-free sessions and published-snapshot refresh success

NPS should be triggered only after meaningful repeat use, not on install. Suggested eligibility: at least three research sessions, at least one completed Yellow Sheet, and at least seven days since first use.

NPS question: "How likely are you to recommend Emporion to another serious investor or market researcher?"

Always pair the score with an open-text reason.

## Analytics event contract

Web and iOS should use the same event vocabulary:

- session_started
- watchlist_connected
- watchlist_symbol_imported
- candidate_viewed
- desk_opened
- source_opened
- scenario_reviewed
- yellow_sheet_started
- yellow_sheet_completed
- invalidation_added
- risk_of_ruin_reviewed
- decision_recorded
- post_trade_review_completed
- resource_opened
- share_used
- nps_requested
- nps_submitted

Recommended properties: platform, app_version, desk_id, candidate_id, instrument_type, workflow_stage, source_type, research_state, and days_since_first_use.

Do not place thesis text, position details, account data, brokerage credentials, or other sensitive research content into generic marketing analytics.

## Marketing hierarchy

Emporion should compete on disciplined decision process, not claim to win the information-volume race.

Positioning hierarchy:

- Survival first: Risk of Ruin is an independent gate, not a footnote to conviction.
- Open: inspect, modify, extend, and self-host.
- Bring your own: watchlist, data, models, rules, broker integration.
- Structured: candidates, research desks, scenarios, Yellow Sheets, deterministic gates.
- Configurable: research only, human-in-the-loop, or user-built automation.
- User owned: their strategy, their data, their capital, their implementation.

Public language should distinguish what the shipped default does from what users may build with the open source system. Avoid guaranteed-performance language, autonomous-trading claims about the default deployment, investment-advice claims, or claims that user customization eliminates legal, broker, or regulatory obligations.
