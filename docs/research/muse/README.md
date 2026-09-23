# Muse research intake

Landing point for research findings contributed by **Muse** (an external meta-agent
app) around market close.

## Purpose

Muse performs research at/after market close and contributes findings. This directory
is the durable, structured intake so those findings are:

1. **Attributed** — each entry names Muse as author, the date, and the market session
   it was produced for.
2. **Sourced** — every claim cites the public source (URL / ticker / release). No
   fabricated numbers. The repo's standing rule applies: public commits must cite
   sources and never present research as performance.
3. **Treated as research input, not trusted desk output** — findings here are
   candidate context. They become desk input only after review against the repo's
   V&V: never a probability/RoR claim on delayed data, never a trade authorization.
4. **Gated like all data** — a finding conflicts with nothing in AGENTS.md so long as
   it stays sourced and non-fabricated; anything that would relax a risk gate or the
   paper-only boundary does not come in through this path.

## Layout

- `YYYY-MM-DD.md` — one file per finding batch (the market-close session's findings).
- Each file front-loads: date, market session, Muse author tag, then findings as a
  list of sourced observations.

## Review before use

A finding is not a decision. Before any candidate here feeds the AM report or a Yellow
Sheet, it must pass the repo's independent review (peer-review profiles, per the desk's
standing MEASURE rule) and be recorded as data with its source, exactly as every other
real-data surface is. Research ≠ income ≠ order.