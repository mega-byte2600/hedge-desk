Title: Desk 7 indicator dashboard (10 consolidated core indicators)

Body:

Desk 7 gets its own surface: the 10 consolidated core indicators behind the
Fed rate decision, each with its trigger rule, today's read, vote, and broker
view, plus the Dec 9 call, the 5/1/4 tally, Kalshi market pricing,
what-would-change-it, the Graham lens, and the grounding note.

This is the consolidated indicator research from Nov 13, presented on Desk 7.
It is not the torn-down rates dashboard: no yield-curve re-presentation, no
30-indicator framework, no refresh pipeline. Data is the labeled Nov 13
snapshot; the view links to the daily brief for the newer read. Refresh is a
separate decision, not part of this change.

Changes:
- web/desk7-indicators.json (new): snapshot data, verbatim from the
  consolidated doc.
- web/app.js: #desk7 route with fail-closed fetch; dashboard link on the
  existing Bonds & Rates desk card (no second card).
- web/index.html: sidebar link.
- scripts/build_web.py: JSON added to CONSOLE_ASSETS.
- tests/test_desk7_indicators.py (new): schema, tally recount, wiring,
  fail-closed copy, both guards below.
- web/app.js: gates()/disposition guards so the Desks view renders when the
  live payload omits layers/disposition (it currently omits both: the view
  threw and never rendered on production).
- web/professional.js: the visible Bonds & Rates card now opens #desk7
  instead of #resources.

Verified: ESM syntax via .mjs-copy check; web subset green (6 new tests);
lint_copy passed; build_web scratch build ships the JSON. One pre-existing
test_dashboard_build mobile-chart failure, identical on clean main.
Playwright render check at desktop + phone widths, zero page errors,
click-through from the Desks view verified. See HANDOFF.md.

Reviewer checks: phone-width render of the indicator table; exactly 7 desk
cards; snapshot labeling honest. Paper-only; no execution boundaries touched.
