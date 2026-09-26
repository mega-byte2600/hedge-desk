# Competitive analysis: learning from High-Flyer (inference-bounded)

Date: 2026-09-23. Scope: what the hedge desk can learn from High-Flyer/DeepSeek's
public posture, using only the repo's verified intake package
(`docs/research/high_flyer/`, verified 2026-09-07). Every claim below is tagged
FACT (from the intake package) or INFERENCE (my read — challenge it).

## What High-Flyer actually gives away — FACT

- High-Flyer's public site describes ML, neural networks, NLP, and the
  Fire-Flyer platform, but publishes **no** trading signals, portfolio data,
  security-level returns, features, labels, execution logic, or risk engine.
  Those assets are unavailable, not reconstructible from press. (README)
- The usable public surface is: DeepSeek model weights/papers/code (R1, V3,
  Coder, Math, GRPO), the Fire-Flyer AI-HPC co-design paper, HAI Platform,
  ffrecord, smallpond (DuckDB batch research), Prover datasets. 24 of 34
  cataloged sources are intake candidates. (source_catalog.json)
- The intake's explicit controls: pin every artifact to an immutable revision;
  re-read licenses at the pinned revision; never treat benchmark scores as
  trading performance; begin with the smallest relevant candidate and justify
  anything larger with measured failure. (README, ASTRA_HANDOFF.md)

## Learnings — INFERENCE

**1. Their moat is what they don't publish.**
The tradable stack — features, labels, portfolio construction, execution —
is entirely absent from the public record. INFERENCE: for a paper desk, the
analog moat is not a model, it's proprietary research process plus
deterministic risk controls. The repo already encodes this (RoR is never
agent-computed; gates fail closed). Protect the process, not the prose.

**2. Infrastructure efficiency is the visible edge.**
The Fire-Flyer paper's thesis is cost-effective software-hardware co-design;
DeepSeek-V3's headline was frontier capability at a fraction of training cost
(MLA, multi-token prediction, DeepEP/DeepGEMM). INFERENCE: the durable lesson
is research throughput per dollar. For this desk that means cheap, fast,
reproducible pipelines (smallpond-style DuckDB batch research, ffrecord-style
reproducible records) over expensive complexity. Measure cost per research
answer; prefer the smallest sufficient tool.

**3. Evaluation discipline beats model worship.**
The ASTRA handoff's first experiment doesn't chase the biggest model — it
evaluates a 1.5B distill against deterministic fixtures on exact extraction,
citation fidelity, NO_TRADE behavior on stale/contradictory evidence,
prompt-injection resistance, and reproducibility. INFERENCE: the Quant Lab's
compounding asset is the eval harness, not any single model. Frozen prompt
sets, fixed seeds, failure-mode tests — that's the machinery that turns
experiments into knowledge.

**4. Open-source the tooling, keep the judgment private.**
DeepSeek's strategy: publish models and methods, keep the trading stack
private. INFERENCE: this repo is intended public — that's fine. The edge lives
in accumulated paper-outcome learning (append-only per AGENTS.md), prompt
craft, and eval sets, not in any single committed file.

**5. Bounded model authority.**
The desk mapping in ASTRA_HANDOFF.md is the template: models may *explain*
deterministic records (Premium/IV), *extract* claims from filings (Earnings),
*review* code (Parity) — they never price, size, or override deterministic
math. INFERENCE: every desk should write down its model's authority boundary
in one sentence. If you can't state the boundary, the model has too much.

## What this changes for the six desks — INFERENCE

| Desk | Learning applied |
| --- | --- |
| Overnight Premium/IV | Models explain existing candidate records only; no pricing or risk authority |
| Earnings Event | Treat claim/guidance extraction as a bounded, testable NLP task with fixtures |
| Dividend Opportunity | Evidence extraction from admitted sources; no invented values |
| Quant/AI Model Lab | Own the eval harness; frozen sets, fixed seeds, NO_TRADE tests |
| Futures Event | Classify supplied evidence; no position sizing or margin authority |
| Box/Parity Observer | Deterministic parity math stays authoritative; models do code review only |

## Honest limits of this analysis

- None of the above is High-Flyer's actual trading edge; it is inference from
  their public research posture plus this repo's intake rules. Their real alpha
  is unobservable by design.
- "bracket22" was not found in the repo (no branch, no file, no doc mention
  beyond an unrelated pgrep idiom). If it's a strategy, branch, or external
  reference, point me at it and I'll run the same treatment.
- Do not let this analysis drift into reconstructing their signals from press
  coverage — the intake package explicitly forbids it, and so do I.
