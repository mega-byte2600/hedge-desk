# Astra handoff: High-Flyer research intake

## Mission

Turn the verified catalog into a reproducible research intake for the existing
paper-only `mega-byte2600/hedge-desk`. Do not implement live trading, brokerage
access, or a model-authored risk control.

## Start here

1. Read `AGENTS.md`, this file, `README.md`, and `source_catalog.json`.
2. Run `python scripts/validate_high_flyer_catalog.py`.
3. Select only catalog entries with `intake_status` equal to `candidate` and an
   artifact-level license that permits the intended experiment.
4. Resolve and record an immutable revision for every selected GitHub or
   Hugging Face artifact.
5. Produce a manifest containing source ID, canonical URL, resolved revision,
   retrieval time, license identifier, SHA-256, size, and intended experiment.

## First experiment

Evaluate `DeepSeek-R1-Distill-Qwen-1.5B` as a local, non-authoritative research
assistant against the project's existing deterministic fixtures. Compare it
with the current baseline using a frozen prompt set and fixed sampling settings.

Required evaluation dimensions:

1. Exact extraction of symbols, dates, quantities, and reason codes.
2. Citation fidelity to supplied evidence.
3. Correct `NO_TRADE` behavior when evidence is stale, missing, contradictory,
   or outside entitlement.
4. Prompt-injection resistance in news and filing text.
5. Refusal to calculate, estimate, infer, modify, or substitute authoritative
   Risk of Ruin.
6. Reproducibility across repeated runs.
7. Runtime, memory, and disk use on the actual local hardware.

## Desk mapping

| Desk | Permitted experiment |
| --- | --- |
| Overnight Premium | Explain existing deterministic candidate records; no pricing or risk authority |
| Earnings Event | Extract management claims, guidance changes, and contradictory evidence from supplied filings/news |
| Box and Parity Observer | Code and test review only; deterministic parity math remains authoritative |
| Dividend Opportunity | Extract dividend history evidence from already admitted sources; no invented values |
| Quant and AI Model Lab | Own the controlled model evaluation, prompt set, registry entry, and comparison report |
| Futures Event | Classify supplied weather, war, and logistics evidence; no position sizing or margin authority |

## Explicit exclusions

1. Do not claim that DeepSeek publishes High-Flyer's investment models.
2. Do not treat benchmark scores as evidence of trading performance.
3. Do not download every model weight. Begin with the smallest relevant
   candidate and justify any larger download with measured failure evidence.
4. Do not use unofficial quantizations or mirrors in the first evaluation.
5. Do not send project secrets or licensed data to the hosted DeepSeek API.
6. Do not modify deterministic risk, compliance, or Back Office calculations.

## Completion evidence

Astra's pull request must include the immutable source manifest, license review,
frozen evaluation set, deterministic test results, measured local resource use,
known limitations, and a `NO_TRADE` default. Passing model evaluation may admit
research evidence; it cannot authorize a paper or live trade.

