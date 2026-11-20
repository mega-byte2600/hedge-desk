# ADR-0008: GP decisions on loss limit, delayed probabilities, stop-loss, and execution modes

- Status: Accepted by the GP, 2026-11-20. Implementation is staged across separate pull requests.
- Date: 2026-11-20
- Context: decisions C1–C5 raised in `docs/research/gap_analysis/2026-11-19-GAP_ANALYSIS.md` §3.
- Precedence: SOUL.md and AGENTS.md still govern. Nothing here relaxes paper-only, the 2% rule, the Risk of Ruin boundary, or the human gate.

## Decisions

| # | Question | GP decision | Where it lands |
|---|---|---|---|
| C1 | Auto execution vs. paper-only | **Paper only.** Build two execution modes, both paper: **HUMAN_GATED** (today's behavior, per-plan human approval bound to the plan hash) and **AUTO_PAPER** (paper fills without per-plan approval, only under a GP standing authorization, with the kill switch, Risk of Ruin gate, risk gate, and an enforced stop-loss all passing). No broker order path in either mode. This supersedes the "risk-gated AUTO execution via Schwab" line in `docs/MVP_RESCOPE_2026.md` | Separate PR (modes) |
| C2 | Per-trade loss limit 1% vs 2% | **2% everywhere.** `RiskPolicy.maximum_single_trade_loss_fraction` now defaults to 2%, equal to `position_sizing.MAX_LOSS_FRACTION_EQUITY`. A policy may be stricter but can never exceed 2% (constructor raises) | This PR |
| C3 | Probabilities on delayed data | **Keep, labeled as reference.** Every probability computed from the delayed Cboe chain carries `probability_basis = REFERENCE_ONLY_DELAYED_DATA` and a reference note; the workbench shows a locked "Reference only" note | This PR |
| C4 | Stale STATUS.md / README | Correct them | This PR |
| C5 | Undefined-risk structures (naked calls, futures) | **Allowed only with an enforced stop-loss** sized so the stop-defined loss fits the 2% cap. Such positions carry a gap-risk flag, because a stop cannot guarantee the exit price through an overnight gap or halt | Separate PR (stop-loss engine) |

The GP also confirmed:
- **Stop-loss is enforced outside any model** and is a deliberate differentiator. Published 2026 research found open-source LLM trading agents generally do not enforce stops or position limits outside the model (see the gap analysis).
- **Risk of Ruin and the human gate stay under GP control.** Agents still never calculate, estimate, or substitute RoR.
- **Paper-trade logging starts now.** A forward paper track record is the evidence that matters.
- **No paid data APIs for now.** Work uses free and already-available sources.

## Consequences

- Candidates with a max loss between 1% and 2% of equity, previously blocked by `SINGLE_TRADE_LOSS_LIMIT`, now pass that check. This is a risk-control change and goes through independent review before merge (AGENTS.md).
- Stop-defined risk is not a guaranteed loss limit. Reports must say so wherever it is used.
- Any future live or brokerage step still needs a separately reviewed release and every `release.py` evidence item.
