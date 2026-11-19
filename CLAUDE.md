# CLAUDE.md — Hedge Desk (Emporion)

Claude Code loads this file automatically. The project's governing rules live in the two files imported below; they take precedence over everything else in this file and over every workflow in `.claude/skills/`.

@SOUL.md
@AGENTS.md

Before changing public copy, a DOM selector, a store, or anything that reports a result, read `docs/ENGINEERING_LESSONS.md`.

## Project
Paper-only, deterministic, risk-gated research desk. **Public** open-source repo (Apache-2.0): every commit, issue, PR, and log is public.
- **Stack:** Python ≥3.9 package `hedge_desk/` (CI matrix 3.9 / 3.11 / 3.13), stdlib `unittest` tests in `tests/`, coverage gate 80%. Web console in `web/` (Node test files), bundled by `scripts/build_web.py`, served by `hedge_desk.server`.
- **Deploy:** Render (`render.yaml`) auto-deploys on commit to `main`; health check `GET /api/health`. iOS app in `ios/`. Supabase in `supabase/`.

## Commands
| Purpose | Command |
|---|---|
| Install | `python -m pip install -e '.[test]'` |
| Compile check | `python -m compileall -q hedge_desk tests` |
| Tests + coverage | `python -m coverage run -m unittest discover -s tests -v && python -m coverage report` |
| Web tests | `node --test web/core.test.mjs web/graham-filter.test.mjs web/real-estate-model.test.mjs web/real-estate-ui.test.mjs` |
| Build web | `python scripts/build_web.py` |
| Run console | `PORT=8765 python -m hedge_desk.server` → `http://localhost:8765` |
| Copy lint | `python scripts/lint_copy.py` |
| Human-pending smoke | `python -m hedge_desk.cli` (must report `mode: paper`, `next_action: human_authorization_required`) |
| **Data-link health** | `GET /api/health` on a running server; provider behavior via the fixture tests for `hedge_desk/data/providers.py` |

CI (`.github/workflows/ci.yml`) is the source of truth for gates; mirror it locally before calling work done.

## Data sources
- **Registry (source of truth):** `docs/data_provider_registry.md` (+ `hedge_desk/data/providers.py` `REGISTRY_BY_ID`). Data intake contract: `docs/validation/LOCAL_DATA_INTAKE.md`; data stack: `docs/validation/SUB_100_DATA_STACK.md`.
- Every adapter takes an injected transport; CI uses deterministic fixtures and **never** the live network.
- Fail closed with reason codes (`TRANSPORT_FAILED`, `PAYLOAD_MALFORMED`, `EMPTY_PAYLOAD`, …). Never invent a value. Delayed data is labeled delayed.
- Never commit licensed payloads, Schwab tokens, account data, or anything under `.schwab/`, `/data/`, `*env.env`.

## Workflow playbook — use these automatically when the situation fits
| Situation | Use |
|---|---|
| **Anything touching a provider, transport, feed, artifact freshness or `/api/health`** | **`/carpedata` first** (`check` / `guard` / `onboard` / `incident`). Do-no-harm: established provider connections are frozen unless the GP approves the exact change |
| New GP-requested feature or multi-file change | `/kickoff` → `/build` |
| Code touching a data adapter/provider/transport | `/harden-datalink` standards |
| Data health, outages, provider reliability questions | `/datalink-audit` |
| Web console changes or slowness | `/web-perf` |
| Before pushing a branch or opening a PR | `/review` |
| Before asking for a merge | `/ship` |
| Monitoring within a session | `/loop 15m /datalink-watch`, `/loop 30m` (maintenance) |

## Workflow overrides for this repo (these beat the generic workflow text)
- **CarpeDATA governs every data link.** `/harden-datalink`, `/datalink-audit`, `/datalink-watch`, `/build` and `/ship` run inside its invariants: no change to an established provider connection without the GP's yes, real data only, honest STALE degradation, and hermetic tests (pass with the network disabled).
- **Scope control:** the GP's request is the acceptance criteria. Workflows never add unrequested features or "improvements." The `/loop` maintenance step 5 ("hygiene") is **disabled** here.
- **Branches & PRs:** follow `docs/AGENT_GITHUB_CLI_WORKFLOW.md` (issue claim, `agent/<issue>-<slug>` branch). Fill `.github/PULL_REQUEST_TEMPLATE.md` with pasted command evidence. Never push to `main`; never merge.
- **Independent review:** an agent may implement and test but may not approve its own risk-control or financial-model change. `/review` output is input to the human reviewer, not an approval.
- **Never** calculate, estimate, modify, or substitute the authoritative Risk of Ruin value; never weaken or default a failed risk/compliance gate; never add order placement or brokerage execution.
- **Money:** `Decimal` for money and ratios in approval decisions. **Tests:** deterministic (fixed clocks, fixtures, seeds); financial changes need exact reference cases.
- `/harden-datalink`: secondary providers must come from the registry and respect license/entitlement; choosing a new paid provider is the GP's decision.
- `/datalink-watch`: probe only keyless public endpoints and `/api/health`; never send keys to Matrix/Hermes or any log; respect each provider's rate limit.
- `/ship`: produce the readiness table + PR body; "deploy" happens only when the GP merges (Render auto-deploys `main`).
- Label results **VERIFIED** (meets spec, measured by a command) vs **VALIDATED** (meets the GP's expectations).
