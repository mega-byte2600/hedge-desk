# HANDOFF — Desk 7 indicator dashboard

Branch: `toby/desk7-indicator-dashboard`, based on origin/main `6fa909b`.
Author: Toby. Reviewer: Sol / user's other model. Toby never merges.

## Order

User order, Sat 2026-11-14 (main chat): "just implement indicator dashboard on
desk 7." This supersedes the Nov 13 teardown order FOR THIS DELIVERABLE ONLY:
the Nov 13 rejection was a rates/yield dashboard re-presenting data the
dashboards page already shows, plus a 30-indicator framework and a refresh
pipeline. This build is the 10 consolidated core indicators from
`desk7-core-indicators.md` (the doc the user accepted Nov 13), presented as
Desk 7's own surface. No framework, no refresh pipeline, no Plotly chart wall.

## What changed

- `web/desk7-indicators.json` (new): the 10 indicators, the Dec 9 call, the
  5/1/4 tally, Kalshi market pricing, what-would-change-it, Graham lens, and
  grounding note. Values copied verbatim from the Nov 13 consolidated doc
  (snapshot pulls ~8:35-8:45am PT, Kalshi 12:00pm PT). Labeled as a snapshot;
  the view links to the daily brief for the newer read.
- `web/app.js`: new `#desk7` route (`desk7()` + `hydrateDesk7()`), following
  the real-estate lazy-route pattern. Fetch fails closed to a literal
  "data unavailable" panel; schema version and 10-indicator count validated
  before render. The Bonds & Rates card in the Desks view carries an
  "Indicator dashboard" link. NO second card: the live report already carries
  bonds-rates-desk as a project (7 projects), so the link rides the existing
  card. A test pins this (no `desk7Card` helper may exist).
- `web/index.html`: sidebar link "Desk 7 · Rates" after "7 - Research Desks".
- `scripts/build_web.py`: `desk7-indicators.json` added to CONSOLE_ASSETS so
  the file ships in dist/ (the build does not fail on an unlisted fetch-only
  asset; it silently drops it — this entry prevents that).
- `tests/test_desk7_indicators.py` (new): JSON schema + tally recount
  (5/1/4) + call + route/nav/asset wiring + fail-closed copy + no execution
  boundaries + the two guards below.
- `web/app.js` (also): `gates()` and the disposition tag tolerate a project
  with no `layers`/`disposition`. REASON: the live /api/report payload omits
  both keys for every project (verified on two fresh pulls), so the Desks
  view threw in `gates()` and never rendered on production. Pre-existing,
  independent of this branch; the dashboard link rides the Desks view, so
  the guards ship here. Two lines, no behavior change when the keys exist.
- `web/professional.js` (also): the VISIBLE Bonds & Rates card (this module
  hides app.js's cards and substitutes its own markup) now navigates to
  `#desk7` instead of `#resources`. REASON: Desk 7 has a research surface
  now; sending its card to the resources page would strand the dashboard.
  One line + comments. No user-facing copy changed anywhere on this branch.

## What was verified

- ESM syntax via the Lesson 2 `.mjs`-copy check (`node --check` on the copy).
- pytest: 4 new tests pass; 53-test web subset green
  (desk7, real-estate lazy route, copy quality, public web surface, page
  guards, disclosures). The single `test_dashboard_build.py` mobile-chart
  failure is pre-existing and identical on clean main.
- `scripts/lint_copy.py`: passed.
- `scripts/build_web.py` in a /tmp scratch copy: dist/ carries
  desk7-indicators.json and the versioned app.js entrypoint.
- Real-browser render check: Playwright chromium-headless-shell against a
  local preview serving this branch's web/ plus the live /api/report
  payload. Zero page errors. #desk7 renders 10 indicator rows, call, tally,
  and all 5 sections at desktop (1280px) and phone (390px) widths; the
  table stacks into labeled rows on phone, no horizontal scroll needed, no
  overlap. Clicking the visible Bonds & Rates card on #desks lands on
  #desk7 with all 10 rows. The managed browser could not reach the local
  preview (loopback refused); Playwright is the established local path.
  Screenshots were read by the author, not just asserted.

## Reviewer must check before merge

1. Render `#desk7` at phone width: the table stacks into labeled rows;
   confirm nothing overlaps or clips. (Author verified at 390px.)
2. Confirm the visible Bonds & Rates card on #desks lands on #desk7.
   (Author verified the click-through.) Note the hidden app.js grid holds
   8 cards (7 projects + the desk-architecture placeholder); the visible
   substitute shows 7. That duplication predates this branch.
3. Confirm the snapshot labeling reads honestly (Nov 13 data, not live).
4. Staleness is an OPEN user decision, not part of this branch: the JSON is
   a snapshot. Refreshing it (manual update vs. research-job refresh) needs
   its own order — do not add a pipeline in review.
