# Emporion Multi-Agent Research Desk

## The problem this records

The research organization is not a single model or a single persona. Different
tasks have different evidence requirements, different failure modes, and
different personalities that SHOULD disagree. A small desk does not need six
agreeable copies of one model; it needs specialized, independently-governed
agents that can be routed, challenged, and audited.

This document records the concrete, reproducible configuration of the Emporion
agent team as isolated Hermes profiles. It is a spec for how the desk is stood
up, not a promise that any agent authorizes a trade.

## Governing principle

**Survival before conviction.** The desk is paper-only. No agent, model, or
agentic workflow authorizes a trade, and no agent is authoritative for Risk of
Ruin. Risk is an independent function that is not rewarded for agreeing with
anyone else.

## The team

Six profiles, each an isolated Hermes instance with its own persistent identity
(`SOUL.md`), session store, memory, and state. They share one inference
credential (the Nous Portal OAuth) but are otherwise independent islands.

| Profile       | Role                              | Backing model            | Independence / mandate                                        |
|---------------|-----------------------------------|--------------------------|---------------------------------------------------------------|
| `orchestrator`| Coordinator (router / synthesizer)| `deepseek/deepseek-v4-pro`   | Routes by mandate, synthesizes, escalates disagreement. Never overrides a specialist by fiat. |
| `quant`       | Quantitative research            | `z-ai/glm-5.3`              | Data before narrative. Falsification, backtesting, statistical rigor. Never fabricates data. |
| `engineer`    | Software / systems               | `openai/gpt-6-astra-flex`   | Inspect before modifying. Simple, testable, reliable systems. |
| `research`    | Deep financial / economic research| `anthropic/claude-haiku-4.5`| Traces claims to evidence. Distinguishes fact / inference / speculation. |
| `risk`        | Independent challenge            | `google/gemini-3.8-flash`   | Independent risk function, NOT rewarded for agreeing. Tail risk, model risk, survivability. |
| `data`        | Data acquisition / stewardship   | `qwen/qwen3.8-flash`        | Provenance, quality, lineage, reproducibility. Filesystem-first. |

Model choice is deliberate: six distinct model families (`deepseek`, `glm`,
`gpt`, `claude`, `gemini`, `qwen`) give genuine cognitive diversity so the desk
does not produce six identical answers.

## Why independent profiles, not subagents

- **Isolated state.** Each profile owns its own `state.db`, `sessions/`,
  `memories/`, and `skills/`. A session or identity in one profile is invisible
  to every other.
- **Persistent identity.** `SOUL.md` is the identity slot; when present it
  replaces the default agent identity in the system prompt, so each profile
  carries its role, ownership, prohibitions, and behavior contract in its
  system prompt.
- **Real diversity.** Different models + different mandates = independent
  verification and explicit handoffs instead of a consensus echo chamber.
- **Auditable.** Handoffs are explicit; disagreement is surfaced, not averaged
  into mush.

## Command model

- List: `hermes profile list`
- Launch: `hermes -p <profile> chat` (wrappers at `~/.local/bin/<profile>`)
- One-shot: `hermes -p <profile> chat -q "<question>"`
- Set model: `hermes -p <profile> config set model.default <model>`
- Tools per role: `hermes -p <profile> tools disable <toolset>`

## SOUL contract (each agent's identity file)

Each `SOUL.md` is self-contained and states, in this order:

1. Framework operating discipline (finish the job, verify with tools, never
   fabricate output, plain claims).
2. `# IDENTITY: <ROLE>` — why the agent exists.
3. What it **owns**.
4. What it does **NOT own** (boundaries that prevent overlap).
5. How it behaves (role principle + explicit handoffs).
6. `## Model` — its backing model and provider.

## Reproducing the setup

The pattern (inspect → create profiles → pick diverse models → stage and apply
role SOULs → verify identity and isolation) is captured in the
`hedge-desk-multiagent-setup` Hermes skill. Reproducing it requires an existing
authenticated inference provider; profiles inherit credentials read-only from
the global auth store, so no per-profile secrets are stored.

## Guardrails that survive the multi-agent structure

- The desk remains paper-only. Agents may research, draft, and propose, but
  never authorize or execute.
- Agents never bypass, weaken, or silently default a failed risk or compliance
  gate.
- RoR is produced only by a separately versioned deterministic component;
  agents consume its immutable result and never recompute, estimate, or
  override it.
- `RISK` is the independent challenge function. It is not rewarded for
  agreement, and it escalates material risk concerns even when doing so slows
  the desk.
