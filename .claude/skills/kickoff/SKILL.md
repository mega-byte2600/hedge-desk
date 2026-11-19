---
name: kickoff
description: Use proactively before writing code for any new feature, integration, or multi-file change. Turns a feature idea or bug report into a researched spec and step-by-step implementation plan before any code is written. Use at the start of any non-trivial feature, refactor, or integration.
argument-hint: "[feature or problem in plain words]"
effort: high
---

# /kickoff — Spec & plan before code

> **Repo rules win.** `CLAUDE.md` (and any `SOUL.md` / `AGENTS.md` it imports) overrides anything in this workflow, including its "Workflow overrides" section.

Request: **$ARGUMENTS**

Act like a staff engineer opening a design doc. Do NOT write production code in this workflow.

## 1. Understand
- Read `CLAUDE.md` and, if the request touches data, the data registry (see `CLAUDE.md` → Data sources).
- Explore the codebase for the areas involved (use the Explore subagent for broad searches). Note existing patterns to reuse — never invent a second way of doing something the repo already does.
- If the request is ambiguous in a way that changes the design, ask up to 3 sharp questions with your recommended answer for each, then wait. Otherwise state assumptions and continue.

## 2. Spec — write `docs/specs/<yyyy-mm-dd>-<slug>.md`
- **Problem & goal** (2–3 lines), **non-goals**
- **User-facing behavior** incl. loading, empty, error, and stale-data states
- **Data contracts**: inputs/outputs, schemas, which data sources are touched, freshness needs
- **Failure modes**: what happens when each dependency is slow, down, rate-limited, or returns bad data
- **Security**: authn/authz, input validation, secrets handling (env-var names only)
- **Performance budget**: latency / bundle / query targets
- **Acceptance criteria**: a numbered, testable checklist

## 3. Plan — append to the same file
- Ordered tasks, each small enough for one commit, each naming files to touch and the test that proves it.
- Mark tasks that can run in parallel.
- Call out risky or irreversible steps (migrations, provider swaps) and the rollback for each.

## 4. Hand-off
Reply with: the spec path, a 5-line summary, open questions, and the exact next command:
`/build docs/specs/<file>.md`
