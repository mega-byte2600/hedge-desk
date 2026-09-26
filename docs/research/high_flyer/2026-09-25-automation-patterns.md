# High-Flyer Automation Patterns — Implementable at Our Scale

**Date:** 2026-09-25 · **Method:** public material only (papers, technical reports, reputable reporting) + read-only inspection of `~/workspace/github/hedge-desk` · **Lens:** value investor (mispricings, margin of safety) · **Lane:** research only, no code changes, no GitHub operations

**Evidence labels:** every claim below is tagged **FACT** (sourced, checkable), **INFERENCE** (my read — challenge it), or **UNVERIFIED** (could not confirm). Nothing here is High-Flyer's actual trading edge; their signals, features, labels, portfolio construction, and execution logic are unpublished by design (intake README, verified 2026-09-07). What transfers is the *machinery*: how they organize research, evaluation, and control at machine scale.

**Baseline facts about High-Flyer (FACT):**
- High-Flyer's own account: began automated quantitative trading with machine learning in 2008; first deep-learning-generated trade on **October 21, 2016**; built the Fire-Flyer computing platform; asset-management operation works with **>10 petabytes of data** and serves **>10,000** high-net-worth and institutional clients (reported via AP, 2026). Accumulated **10,000 Nvidia A100 GPUs by 2022** (AP).
- Fire-Flyer AI-HPC paper (arXiv 2408.14158): Fire-Flyer 2 with 10,000 PCIe A100 GPUs achieves ~80% of DGX-A100 performance at ~60% of cost and 40% less energy. Software co-design: **HFReduce** (custom allreduce), **HaiScale** (parallel-strategy framework overlapping compute/communication), **3FS** (distributed filesystem), and the **HAI Platform** software stack, which "addresses a variety of system faults, from network congestion to hardware failures, thereby ensuring high stability and robustness."
- DeepSeek-V3 technical report: 671B MoE (37B active/token), trained on 14.8T tokens for **2.788M H800 GPU-hours (~$5.576M at $2/hr)**; evaluated on **30+ benchmarks**; the run reported **no irrecoverable loss spikes and no rollbacks**.
- Intake package rules (repo `docs/research/high_flyer/README.md`, verified 2026-09-07): pin every artifact to an immutable revision; re-read licenses at the pinned revision; never treat benchmark scores as trading performance; begin with the smallest relevant candidate and justify anything larger with measured failure. Priority-2 material for the desk: **smallpond** (DuckDB-oriented batch research) and **HAI Platform + ffrecord** ("reproducible jobs, datasets, checkpoint and record concepts").

---

## Pattern 1 — Content-addressed, reproducible research records (ffrecord concept)

**What it is (FACT):** The intake catalogs HAI Platform + ffrecord as "reproducible jobs, datasets, checkpoint and record concepts" (README). The Fire-Flyer paper documents the HAI Platform as the software layer that absorbs faults and keeps the system stable and reproducible at 10k-GPU scale. The desk's intake rule #3 requires storing "metadata, revision IDs, hashes, test results, and permitted derived facts" for every artifact.

**Why it matters (INFERENCE):** High-Flyer-scale automation treats the *reproducible record* — not the script, not the model — as the unit of work. Every research output pins its inputs (data revision, code revision, seed, prompt set) so any result can be replayed and audited. At our scale this is nearly free: hash the inputs, write a manifest. It is also the precondition for every other pattern below — you cannot evaluate, gate, or learn from what you cannot reproduce.

**Repo mapping (verified by inspection):**
- EXISTS (partial): `nightly.py` writes content-addressed AM reports to `artifacts/`; `artifacts.py` builds/verifies bundle manifests (`build_artifact_bundle_manifest`); `compliance/traceability.py` keeps a sha256 registry; the automation audit (2026-09-25) confirms the nightly pipeline is fail-closed and hashed.
- MISSING: the Muse research batches (`~/workspace/hedge-desk-research/*.md`) carry **no input manifest** — no pinned data revision, code commit, or prompt-set version. There is no ffrecord-style "record" as a first-class schema covering research runs.

## Pattern 2 — Frozen evaluation harnesses with failure-mode fixtures

**What it is (FACT):** DeepSeek-V3 was evaluated on 30+ benchmarks with results published in the technical report; the ASTRA handoff in this repo defines a first experiment: evaluate a 1.5B distill against **deterministic fixtures** on 7 dimensions — exact extraction of symbols/dates/quantities/reason codes, citation fidelity, correct `NO_TRADE` on stale/missing/contradictory evidence, prompt-injection resistance, refusal to touch Risk of Ruin, reproducibility, and measured resource use — using a **frozen prompt set and fixed sampling settings**.

**Why it matters (INFERENCE):** The compounding asset is the eval harness, not any model. Frozen sets + fixed seeds + failure-mode tests turn experiments into durable knowledge: a model (or prompt, or agent) is admitted to the research pipeline only by passing the harness, and regressions are caught mechanically. This is how you let models touch research at scale without authority creep.

**Repo mapping (verified by inspection):**
- EXISTS (partial): `evaluation.py` (layers, statuses, dispositions incl. `HUMAN_REVIEW`/`NO_TRADE` per audit), `stat_evaluation.py`, `wargames.py` (20+ war-game classes including `ModelGovernanceWarGame`, `AuditAttackWarGame`, `SchedulerAttackWarGame`), `research_intelligence.assess_source` (deterministic 100-point source scorer).
- MISSING: no frozen prompt sets checked into the repo; no per-desk eval fixture suite wired into CI; the Astra experiment's acceptance criteria exist but the experiment has no recorded results.

## Pattern 3 — Deterministic gates, fail-closed, checked synchronously on every decision

**What it is (FACT):** `execution_gate.py`: `KillSwitch` class, default `armed=False` → `BLOCKED`; "a kill switch is required ON for any ALLOW." `release.py`: "Deterministic paper-to-live readiness gate; **no agent or human override**"; `ReleaseReadiness` carries evidence sha256 hashes, `human_override_allowed`, and `live_transition_authorized` fields. Industry baseline: a kill switch cancels all open orders and halts new order generation, authority sits with a designated supervisor/risk officer, and firms test it regularly (expert review, foulegold/media). SEC Rule 15c3-5 requires broker-imposed pre-trade controls under the firm's direct and exclusive control; MiFID II RTS 6 mandates real-time monitoring by staff with intervention authority.

**Why it matters (INFERENCE):** Machine-scale automation runs on gates that are (a) deterministic, (b) evaluated on every decision, (c) fail closed, and (d) leave evidence. The human never sits in the per-decision path; the human owns gate *design*, *arming*, and *attestation*. This is the precise shape of "limited human intervention."

**Repo mapping (verified by inspection):**
- EXISTS: `evaluate_execution`, `KillSwitch`, `evaluate_live_release_readiness`, plan hashing + fill checks in `paper/workflow.py`.
- MISSING (automation audit 2026-09-25): `approve_paper_trade` has **zero production callers**; the kill switch defaults OFF and nothing in production arms it. A control you cannot observe firing is not a control (cf. the dead-control audit lesson). NOTE: a coordinator subagent is currently implementing the approval-surface wiring on branch `automation-track` — per parent-agent transcript, **unverified by this research**.

## Pattern 4 — Kill-switch design: automatic trips + manual trips, human-only resume, exercised with evidence

**What it is (FACT):** Documented industry design (mhughesdev/trading_bot spec COMP-002): a global `trading_enabled` flag checked **synchronously at the start of every risk-gate evaluation**; **automatic trips** (max daily loss, position/broker reconciliation divergence, market-data staleness, broker disconnection, event-bus down); **manual trips** (UI button, REST endpoint); **resume requires explicit human action**; the kill switch blocks new orders but does *not* force-close positions — squaring is a separate, deliberate, tested action.

**Why it matters (INFERENCE):** The kill switch is the cheapest catastrophic-risk control in the building, and its value is entirely in the details: synchronous check (no path around it), auto-trips (machines detect faster), human-only resume (no auto-recovery into a broken state), and regular drills with recorded evidence. For a paper desk the "positions" are paper plans and the "orders" are research-to-proposal flow — the design transfers directly.

**Repo mapping (verified by inspection):**
- EXISTS (partial): `KillSwitch` dataclass, checked in `evaluate_execution`.
- MISSING: no automatic trip conditions anywhere in the codebase; no drill/exercise records; no resume ceremony; kill switch not wired to the paper lifecycle or the 15-minute runner.

## Pattern 5 — Human-in-the-loop split: humans own validation, deployment, and attestation — never the per-signal path

**What it is (FACT):** Expert review of algorithmic-trading oversight: oversight operates **before deployment** (validation), **in parallel** (monitoring), and **after** (post-trade review) — "the microsecond path from signal to order contains no human." What oversight slows is the *deployment of new strategies*, deliberately. MiFID II RTS 6 requires real-time monitoring by staff with intervention authority. The Bracket22 analysis (repo research, 2026-09-25): specialist-agent isolation with a human judgment layer; the human keeps kill/keep calls. Repo AGENTS.md: "an agent may implement and test a change but may not approve its own risk-control change."

**Why it matters (INFERENCE):** This is the org chart for "fully automated with limited human intervention": machines run the entire deterministic loop; humans appear at exactly four checkpoints — plan approval, kill-switch arming/resume, release-gate attestation, and method adoption (INTEGRATE decisions). Everything else is automation surface. The audit's graded touchpoint table is already this split.

**Repo mapping (verified by inspection):**
- EXISTS (partial): `HumanAuthorization`/`HumanAuthorizationStatus` in `paper/workflow.py` (human confirms, cannot override machine blocks); `EvaluationLayer.HUMAN` with `HUMAN_REVIEW`/`NO_TRADE` dispositions; `assess_source` INTEGRATE = "eligible for implementation review only."
- MISSING: the approval surface has no production caller (Pattern 3); release-gate evidence (counsel signoff, external audit, RoR V&V, DR test) requires real-world human actions not yet performed.

## Pattern 6 — Throughput-per-dollar as the operating metric

**What it is (FACT):** Fire-Flyer: 80% of DGX-A100 performance at 60% of cost, 40% less energy — cost-effectiveness as the headline result, not a footnote. DeepSeek-V3: the training bill itemized to the GPU-hour ($5.576M). Liang Wenfeng: research funded by an "adequate R&D budget"; "we have the computing power and a team of engineers, so we have half the leverage." Intake rule: begin with the smallest relevant candidate; justify anything larger with measured failure.

**Why it matters (INFERENCE):** At our scale the "HPC" is the agent fleet plus API spend, and the disciplined question is the same: **cost per verified finding**. A desk that measures research throughput per dollar will outrun one that buys bigger models. The smallest-sufficient-tool rule is the cultural version of this metric.

**Repo mapping (verified by inspection):**
- MISSING: no cost/throughput instrumentation on research runs — batch outputs record no token/API cost, no findings-per-run metric, no per-desk cost accounting.
- EXISTS (adjacent): `metrics.py`, `operational_health.py` (`PaperRunHealth`) — health, not cost.

## Pattern 7 — Append-only outcome learning + adversarial self-review

**What it is (FACT):** Repo AGENTS.md: "Agent learning is append-only and paper-outcome based." `paper_log.py` records outcomes append-only. The desk runs a weekly adversarial review (Sentry) over its own research output — per parent-agent transcript, **unverified by this research**.

**Why it matters (INFERENCE):** High-Flyer's published advantage is research velocity disciplined by evaluation; the desk's analog is the outcome feedback loop: every paper outcome recorded → re-evaluation → method improvement, with an adversary (red team) hunting the pipeline's own blind spots. A learning loop that only records wins is marketing; the value is in recorded, re-playable failures.

**Repo mapping (verified by inspection):**
- EXISTS (partial): append-only `paper_log.py`; `stat_evaluation.py`; research batches; wargames.
- MISSING: `paper_log` stalls waiting for user-supplied outcomes (automation audit) — the feedback plane has no read-only market-data settler; read-only settler is reportedly in-flight on `automation-track` (unverified by this research).

---

## Honest limits

- None of the above is High-Flyer's trading edge; it is their *public research posture* plus industry control design, mapped onto this repo. Their alpha is unobservable by design.
- "Smallest sufficient tool" cuts against model maximalism: several patterns here are pure software engineering (hashing, fixtures, flags), not AI.
- Items marked "in-flight" come from the parent agent's transcript, not from my inspection — verify before treating them as done.

## Suggested implementation order (INFERENCE)

1. **Pattern 1 (records)** — cheapest, unlocks everything else; every batch run emits a manifest.
2. **Pattern 2 (eval fixtures)** — the Astra acceptance criteria already define it; check in frozen sets, wire to CI.
3. **Pattern 4 (kill-switch trips + drills)** — a control you can't observe firing isn't a control; add auto-trips and exercised-with-evidence drills.
4. **Pattern 6 (cost instrumentation)** — measure cost per verified finding before scaling the fleet.
5. Patterns 3 & 5 are substantially in-flight (approval surface); Pattern 7's settler is in-flight — verify, don't duplicate.
