# ADR-0005: Open Quant/AI Model Lab as MVP 5

Status: Accepted for architecture; implementation foundation only

## Decision

Create two independent research teams behind a shared reproducibility gate:

- **Quant Team:** deterministic features, statistical tests, confidence
  intervals, calibration, walk-forward evaluation, costs, and baselines.
- **AI Team:** hypothesis generation, evidence synthesis, counter-theses, and
  critique using versioned open models where suitable.

The teams may challenge each other but cannot vote through deterministic risk,
compliance, or human authorization. AI output cannot be relabeled as an observed
statistic. Neither team may calculate or modify authoritative RoR.

## End-to-end open requirement

Every promoted model needs a public source repository, approved SPDX license,
weights hash, exact code commit, frozen training cutoff, evaluation-dataset hash,
and evaluation-report hash. A proprietary runtime dependency blocks the
end-to-end-open claim. Licensed market observations remain separate: model
openness does not grant redistribution rights to training or evaluation data.

Hugging Face may host model code, weights, cards, and evaluations, but hosting
alone does not prove an open license, reproducibility, financial validity, or
freedom from data leakage.

## Evaluation boundary

Promotion requires chronological walk-forward tests, purging/embargo around the
holding horizon, a locked test window, declared baselines including `NO_TRADE`,
all-in costs, tail-risk metrics, calibration for probabilistic outputs, stable
artifact hashes, and independent conventional V&V for financial calculations.
