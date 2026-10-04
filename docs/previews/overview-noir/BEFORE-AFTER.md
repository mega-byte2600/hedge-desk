# Overview revamp — before / after

Prototype location: `~/workspace/hedge-desk/overview-revamp/`

- `overview-revamp.js` — drop-in render function (plain script, no deps)
- `overview-revamp.css` — all styles, phone-first, light/dark via `[data-theme]`
- `preview.html` — self-contained demo (CSS inlined, JS loaded, inline fixture)

## Before (current repo page)

The overview route renders two stacked layers:

1. `app.js overview()` — page head ("Research overview"), a "Where things live"
   notice, four stat tiles, a desk-evaluation table, a scenario-lab panel, and
   an "Operating boundary" panel.
2. `professional.js overviewBlock()` — injected on top: a status tape plus five
   word-heavy marketing sections (PROBLEM / PROMISE / OWNERSHIP, the "WHAT
   EMPORION DOES" process line, "COORDINATED RESEARCH SYSTEM", the Risk-of-Ruin
   explainer, the operating continuum, and a desk name list). `installStyle()`
   also hard-codes a light-only palette (`#fff`, `#101820`) and hides
   app.js's own overview stats/table with `display:none`.

Static copy: **~472 words** (403 in `overviewBlock`, 69 in `overview()`).
Framing: promotes the platform/membership wrapper (PROBLEM/PROMISE/OWNERSHIP
marketing arc); live numbers are present but buried under the prose.

## After (this prototype)

Four visual blocks, **~142 words of static copy** (~70% reduction):

| Block | Content |
|---|---|
| (a) Hero strip | `DESKS LIVE 5/6`, `DATA AS OF <ts> · Yahoo Finance · 3h ago`, `CANDIDATES 24`, `DAILY BRIEF <date> + headline` — freshness dots (green <6h, amber <24h, red older) |
| (b) Desk grid | One tight card per evaluated desk: name, one-line method, Live/Batch/No-data status dot, per-desk `as of` |
| (c) Pipeline strip | 5-step visual stepper: Candidate intake → Research desks → Scenario analysis → Risk gate → Human review. No paragraphs |
| (d) Boundary footer | Three short lines: paper-only / not investment advice / RoR as independent gate |

No membership pitches, no LP/investor content, no "test drive" language anywhere
(verified by render test). Page promotes the desk's capabilities and live data.

## Design decisions

- **Same data inputs as `overview()`**: `render(data, report, brief?)` consumes
  `data.summary`, `data.candidate_feed`, `data.registry` (method fallback),
  `report.projects`, and an optional brief `{date, headline}` from
  `research-brief.json`. Desk names reuse the exact `names` map from app.js.
- **No hard-coded palette**: all colors resolve through `--ov-*` tokens with
  light defaults; `[data-theme="dark"]` overrides live on `<html>` or `<body>`.
  Host tokens `--ink/--muted/--line` are reused where they fit (labels, hairlines).
- **Phone-first**: base layout is single-column; 4-up hero and 3-col desk grid
  arrive via `min-width` breakpoints. Stepper scrolls horizontally on narrow screens.
- **Freshness is computed, not asserted**: `data_as_of` is rendered as absolute
  time + relative age + dot, so a stale snapshot reads stale instead of looking live.
- **Escaping**: all dynamic text passes through `esc()`; dates via the same
  `toLocaleString(medium, short)` shape as app.js.
- **RoR positioning**: one line, no new claims — "Risk of Ruin is an independent
  gate — research conviction never overrides it." (matches the repo's "agents never
  calculate/infer RoR" rule by saying nothing about the value).

## Integration notes (for the repo integrator)

1. **app.js**: replace the body of `overview()` with
   `return HedgeDeskOverview.render(data, report, window.__brief || null);`
   and load `overview-revamp.js` as a classic script before app.js (or convert
   the IIFE to an ES module export). Pass the brief from the existing
   `hydrateBrief` fetch: it already loads `research-brief.json` — cache its
   `{date, headline}` and re-render, or render the brief stat lazily.
2. **professional.js**: delete `overviewBlock()` entirely, and remove its
   inclusion in `renderContext()` (`statusStrip() + overviewBlock() + …`).
   Delete or scope the `body[data-route='overview'] #main>.notice,…{display:none}`
   rule in `installStyle()` — it hides app.js's overview sections, which no
   longer exist in this design. Keep `statusStrip()`, `applyBrand()`,
   `desksBlock()`, `wireDeskRows()` untouched.
3. **CSS**: add `overview-revamp.css` to the page (link or bundle). It is
   self-contained under the `.ov` scope and does not touch existing selectors.
4. **Dark mode**: the host needs a theme toggle that sets
   `data-theme="dark"` on `<html>`/`<body>` for the dark tokens to apply;
   light remains the default with no host changes.
5. **What to delete**: the PROBLEM/PROMISE/OWNERSHIP grid, coordinated-research
   section, RoR explainer section, continuum, and the old desk-list in
   `overviewBlock()` — all superseded. The old `overview()` stats/table/panels
   are superseded by the hero/desk-grid.
6. **Bonds & Rates** ("coming soon", 7th desk) is intentionally not a card —
   it has no evaluated research yet; add a card when it reports data.

## Validation

- `node --check overview-revamp.js` — PASS
- CSS brace balance (48/48) — PASS
- Node render smoke test on a 6-desk / 24-candidate fixture — PASS:
  6 desk cards, 4 hero stats, 5 pipeline steps, correct live counts,
  no membership/LP/test-drive language, all dynamic text escaped.
- `preview.html` — open in a browser; "PREVIEW DATA — NOT LIVE" badge fixed
  top-right; "Toggle dark" button exercises the `[data-theme]` hook.
