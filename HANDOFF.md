# HANDOFF — Desk 7 Plotly indicator dashboard

Branch: `toby/desk7-plotly` (base: main `277666b`).
Order: user, 2026-11-14 ~10:34 PT — the Desk 7 table was rejected as "a list of
indicators"; the order is an interactive, intuitive indicators dashboard that
visualizes and helps understand possible rate cuts or hikes. "Plotly!"

## What changed (3 files + this handoff)

- `web/desk7-indicators.json` — schema `desk7-indicators-2`. Each of the 9
  numeric indicators gains a `gauge` object encoding its trigger rule as
  numbers (value(s), tripwires, window, short label, unit); FOMC keeps
  `gauge: null` (qualitative vote). `market_pricing.kalshi_markets` added
  (4 entries from the same Nov 13 12:00 PT pull). No new numbers: every gauge
  value and tripwire comes from the consolidated doc's stated rules; the two
  cut markets are combined as "Any cut" ($0.02) and never individually named.
- `web/app.js` — three Plotly charts on #desk7, progressive enhancement over
  the unchanged table (table renders first; charts fail closed with a note):
  vote-balance bar (5 HIKE / 4 NEUTRAL / 1 CUT), 9-row trigger gauges in real
  units with dashed tripwires, zone tints, and diamond markers (click a marker
  → scrolls to the indicator's table row and highlights it 1.8s), and the
  Kalshi pricing bars. Plotly is the already-vendored
  `vendor/plotly-2.35.2.min.js`, loaded by dynamic import (workbench GAP-3
  pattern). Colors: HIKE brass #dcb96f, NEUTRAL #a39e93, CUT workbench blue
  #4a90d9; live green #35c26e is NOT used (reserved for live-data semantics).
  Table rows carry `id="desk7-row-${i}"` for the click target.
- `tests/test_desk7_indicators.py` — 6 tests → 9. New: gauge encoding
  recomputes every stated vote from value + tripwires (9 gauges, FOMC null,
  values/tripwires inside windows); Kalshi markets sum to the $1.05
  over-round with total hike $1.00; chart wiring + theme-safety asserts
  (chart div ids, vendor Plotly import, plotly_click, fail copy, vote colors,
  no #35c26e in the Desk 7 chart block).

## What was verified

- ESM syntax via `.mjs` copy (`node --check`) — the plain check passes
  silently on ESM errors (see ENGINEERING_LESSONS.md rule 2 addendum).
- `pytest tests/test_desk7_indicators.py`: 9 passed. `lint_copy.py`: passed.
  `test_dashboard_build.py`: exactly the one pre-existing failure
  (`test_titles_are_outside_plotly_canvas`), identical on clean main.
- `build_web.py` scratch build in /tmp: dist/ carries
  `desk7-indicators.json` (schema v2, 10 indicators, 4 Kalshi markets) and
  `vendor/plotly-2.35.2.min.js`, versioned app.js.
- Playwright (loopback preview server, branch web/ + live /api proxy):
  desktop 1280px and phone 390px — all 3 charts render, 10 gauge points,
  gauge click verified end-to-end (row highlight + scroll into view),
  0 page errors, no horizontal scroll on phone. Screenshots read by the
  builder across 4 QA rounds; the last round fixed the phone "1 CUT" label
  (outside placement) and the breakevens combined label.
- Data unchanged: same labeled Nov 13 snapshot. The refresh question (manual
  update vs research-job refresh) is still an open user decision; no pipeline
  was built. This is NOT the rejected Nov 13 rates dashboard: no yield-curve
  re-presentation, no framework, no refresh pipeline.

## Reviewer must check before merge

1. Render #desk7 at phone width; confirm all three charts legible, no overlap.
2. Confirm each gauge tripwire matches the trigger rule in the table row
   (the recomputation test pins votes, not the rule text itself).
3. Confirm the table below the charts still carries the same data (the
   fail-closed path: block vendor/plotly-2.35.2.min.js and confirm the note
   + table, no blank panels).
4. Confirm no live green appears anywhere on #desk7.
