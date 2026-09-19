# Technology Roadmap: overnight-batch, end-to-end automated trading
# (the "High-Flyer-like" loop, at hedge-desk scale)

Goal, in the GP's words: **batch-overnight data processing (not real-time) that
supports end-to-end automated trading** — a systematic closed loop like a
quant-shop's research-to-execution pipeline, sized for a small desk and a Mac.

## Principle: High-Flyer-like is METHOD, not HPC

Your own research inventory (`docs/research/high_flyer/README.md`) is explicit:
High-Flyer does NOT publish trading signals, features, labels, positions,
execution logic, or its risk engine — those are unavailable and must not be
reconstructed. What it DOES open-source is the infrastructure that made the
loop work at low cost: batch research tooling (smallpond/DuckDB), a
reproducible job/data platform (HAI, ffrecord), and cost-efficient training
compute (Fire-Flyer). DeepSeek's affordability is the proof of the method:
**systematic, batch, cost-aware, closed-loop** — not raw HPC.

So "high-flyer like" for us = adopt their DISCIPLINE at our scale:
- overnight batch, not real-time (you explicitly want this);
- features computed on batch, re-derived reproducibly;
- a measured, self-improving loop (validated learning);
- survival-first (Risk of Ruin) and paper-to-live gating;
- cheap footprint (small desk, budget-conscious).

Governed by SOUL: paper-first, deterministic risk, real-data-only, small-desk
systems, never fabricate, V&V everything. Governed by Lean Startup (Ries):
Build-Measure-Learn tiers, each with a measurable exit gate.

## The target shape (six planes, from data to execution)

1. DATA PLANE  — overnight batch ingestion, provenance-bound, reproducible.
2. FEATURE PLANE — compute signals off each batch (returns, vol, IV rank,
   event proximity, spread economics).
3. SIGNAL/LEARNING PLANE — turn features into an evaluated candidate policy;
   honest (no fabricated RoR; deterministic risk consumes validated inputs).
4. DECISION/GATE PLANE — risk + compliance + kill-switch + release gate.
5. EXECUTION PLANE — the release-gated Schwab adapter (risk-gated auto).
6. FEEDBACK PLANE — record outcomes, re-evaluate walk-forward, improve the
   signal. This is the "learn from ALL sessions" close of the loop.

The six planes form a pipeline: 1 → 2 → 3 → 4 → 5, and 6 reads outcomes back into 1 and 3.

## Roadmap tiers (each a Build-Measure-Learn cycle; exit = measured gate)

### Tier 0 — DONE (verified 2026-09-19, 702+ tests green)
- Data plane: real EOD (Yahoo), real option chains (Cboe), real rates (FRED),
  real earnings (SEC EDGAR). Provenance + content-addressed AM report.
- Nightly orchestrator consolidates 4 desks into one AM report; demo page renders it.
- Position filter encodes the GP's real rules (return on capital deployed ~2%,
  <$5k capital, 30-45 DTE, survivability).
- Execution scaffolding: OAuth connector + read-only probe (RISK-audited, safe);
  Schwab approval in progress.

### Tier 1 — BATCH FEATURE PLANE (next; the top of the actual "high-flyer-like" step)
GOAL: one deterministic feature bundle per symbol per night, re-derivable from
   the persisted artifact. Mirror smallpond's idea (batch feature engineering)
   without importing DuckDB complexity unless it beats the Python path by a
   measured margin.
BUILD: a features module computing, from the existing real artifacts:
   - returns (1/5/21/63-day), realized vol, close-vs-SMA bands;
   - for the premium desk: IV context, 10-yr dividend/cape context is separate;
   - event proximity (earnings date from EDGAR calendar, ex-div).
MEASURE: a feature artifact hashes deterministically for a fixed batch; a
   spec file states each feature's formula + tolerable range; 100% reproducible
   re-run.
LEARN: which features actually separate "survivable premium candidate" from
   not, judged on the paper-outcome log (must come from Tier 4, not invented).

### Tier 2 — SIGNAL EVALUATION (honest candidate policy)
GOAL: rank candidates by a combination of the features + rule-gated risk, with
   NO fabricated probability/RoR. Everything downstream consumes validated
   deterministic risk inputs only.
BUILD: a walk-forward evaluation scaffold (existing purged-split machinery in
   `hedge_desk/models/`) over the feature bundle; a ranking that surfaces the
   cash-secured seller case first (fix the current return_on_risk basis).

### Tier 3 — DECISION + GATE (largely exists; harden)
Risk gate (fail closed), compliance policy, kill switch, release gate (9
evidence items). Build the validated-input boundary so agents can never inject
an authoritative RoR (the frame the desk audit already exposed in nightly.py).

### Tier 4 — PAPER OUTCOME LOOP (the true "learn from ALL sessions")
GOAL: every paper candidate records an outcome (entered/stopped/expired/
   assigned, money realized). Outcomes feed the walk-forward re-evaluation so
   the signal improves on measured results — the feedback plane.
This is the honest heartbeat of a high-flyer-like desk: you cannot improve what
you do not measure, and you never claim performance you have not produced
paper-first.

### Tier 5 — RELEASE-GATED EXECUTION (end-to-end automation)
The Schwab adapter behind the release gate: read-only now; then risk-gated
auto placement only when the 9 evidence items are real (incl. kill-switch DR,
regulated counsel). A test contract runs through the gate against the real
account before any real money.

## Honest boundaries (do not cross; SOUL + the research inventory)
- Do NOT import High-Flyer HPC/cluster design into the MVP. The docs defer
  3FS/DeepEP/DeepGEMM/FlashMLA until scale measurements justify them.
- Do NOT reconstruct High-Flyer's trading signals/features/execution from
  press or speculation. Their method is the closed loop; their pass is ours.
- No fabricated RoR, no invented account/liquidity, no real orders until the
  release gate passes. trade_authorized stays False until then.

## Verified status
- VERIFIED (measured): Tiers 0 implemented, 702 tests green, live real-data
  pipeline + demo + audited connector.
- VALIDATED: matches the GP's goal (batch overnight -> end-to-end automation)
  and the SOUL/Lean discipline (BML tiers + honest gates).
- NOT YET: Tiers 1-5 are the roadmap; nothing there is claimed as built.