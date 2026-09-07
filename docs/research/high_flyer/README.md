# High-Flyer and DeepSeek open research inventory

Verified 2026-09-07 for the paper-only Hedge Desk.

## What this package is

This is a source-first intake package for Astra. It separates official
High-Flyer material from official DeepSeek material, records licenses at the
artifact level, and maps only relevant work to the six Hedge Desk research
paths. The machine-readable source of truth is `source_catalog.json`.

High-Flyer's own site describes its use of machine learning, neural networks,
NLP, and the Fire-Flyer research platform, but it does not publish its trading
signals, portfolio data, security-level returns, features, labels, execution
logic, or risk engine. Those assets must be treated as unavailable, not
reconstructed from press coverage.

Official roots:

1. High-Flyer Quant: <https://www.high-flyer.cn/en/fund/>
2. High-Flyer AI GitHub: <https://github.com/HFAiLab>
3. DeepSeek GitHub: <https://github.com/deepseek-ai>
4. DeepSeek Hugging Face: <https://huggingface.co/deepseek-ai>
5. DeepSeek research site: <https://www.deepseek.com/>

## Highest-value material for Hedge Desk

| Priority | Material | Hedge Desk use | Boundary |
| --- | --- | --- | --- |
| 1 | DeepSeek-R1 and distills | Local research-agent baseline, critique, structured hypothesis generation | Model output is untrusted research; no risk or trade authority |
| 1 | DeepSeek-V3 technical report | MoE, MLA, multi-token prediction, training and evaluation design | Architecture reference, not a financial model |
| 1 | DeepSeekMath and GRPO | Deterministic-math explanation, test generation, evaluation design | Never calculate or substitute authoritative Risk of Ruin |
| 1 | DeepSeek-Coder and Coder-V2 | Code review, test generation, local agent experiments | Generated code requires tests and review |
| 1 | Fire-Flyer AI-HPC | Cost-aware local-first platform and data-pipeline design | The reported cluster architecture is not appropriate for the current Mac-first MVP |
| 2 | smallpond | DuckDB-oriented batch research and feature engineering | Prototype only; benchmark against the existing Python path |
| 2 | HAI Platform and ffrecord | Reproducible jobs, datasets, checkpoint and record concepts | Do not import cluster complexity into the MVP without measured need |
| 2 | Prover-V1 and ProverBench datasets | Formal-verification and reasoning evaluation experiments | Not market data and not evidence of investment skill |
| 3 | 3FS, DeepEP, DeepGEMM, FlashMLA | Future infrastructure study | Defer until scale measurements justify specialized hardware |

## Material that is not available

1. High-Flyer proprietary market data.
2. High-Flyer live or historical positions and order records.
3. Security-level alpha signals, labels, features, portfolio construction, and
   execution models.
4. A reproducible financial training corpus for DeepSeek models.
5. The full pretraining corpora described in DeepSeek technical reports.
6. The reported 800,000-sample R1 distillation corpus as a separately released
   official dataset.

Absence is a control. Astra must not fill these gaps with inferred formulas,
unverified mirrors, synthetic claims, or media descriptions.

## Intake rules

1. Pin repositories, models, and datasets to immutable commit revisions before
   use. A moving `main` branch is discovery-only.
2. Re-read each artifact's license at the pinned revision. Repository code and
   model weights can have different licenses.
3. Store metadata, revision IDs, hashes, test results, and permitted derived
   facts in this public repository. Do not commit model weights or third-party
   datasets.
4. Run models in an isolated, least-privilege research environment without
   broker credentials, account identifiers, private prompts, or licensed raw
   market payloads.
5. Treat every model response and retrieved document as untrusted input.
6. Preserve the current deterministic data, compliance, risk, human approval,
   and Back Office boundaries.

## Files

1. `source_catalog.json`: machine-readable official-source inventory.
2. `ASTRA_HANDOFF.md`: bounded next actions and acceptance criteria.
3. `../../../..//scripts/validate_high_flyer_catalog.py`: offline catalog
   validation.

