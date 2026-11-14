# PR BODY (ready to paste)

## Title

Desk 7: interactive Plotly indicator dashboard (vote balance, trigger gauges, Kalshi)

## Body

User order 2026-11-14: the Desk 7 table alone was rejected as "a list of
indicators". This replaces the list-only presentation with an interactive
Plotly dashboard that visualizes where each indicator sits against its
hike/cut trigger.

**Charts (progressive enhancement over the unchanged table):**

- Vote balance — the 5 HIKE / 1 CUT / 4 NEUTRAL tally as a stacked bar;
  hover a segment for the indicators behind it.
- Trigger gauges — one row per numeric indicator, in its own real units,
  with dashed tripwires from the trigger rule, tinted HIKE/CUT zones, and a
  diamond marker for today's read. Click a marker to jump to that
  indicator's table row. FOMC has no numeric trigger and is footnoted.
- Kalshi pricing — the four Dec-meeting outcomes as bars ($0.88 / $0.12 /
  $0.03 / $0.02 combined cuts).

**Data:** the same labeled Nov 13 snapshot — no new numbers. The JSON schema
bumps to `desk7-indicators-2`: each numeric indicator carries a `gauge`
object encoding its trigger rule as numbers, and the Kalshi markets are
carried as data. A test recomputes every stated vote from the gauge numbers,
so a chart can never show a marker on the wrong side of its tripwire.

**Theme:** brass HIKE / muted NEUTRAL / workbench-blue CUT. Live green is
reserved for live-data semantics and is not used here. Plotly is the
already-vendored bundle, loaded by dynamic import; if it fails, the table
below carries the same data.

**Verification:** 9/9 Desk 7 tests (ESM syntax gate, lint, scratch build),
Playwright desktop + phone with the click-to-row path exercised and 0 page
errors. The one `test_dashboard_build.py` failure is pre-existing on clean
main. See HANDOFF.md on the branch for the full evidence and reviewer
checklist.

**Not in scope:** data refresh (still an open user decision; no pipeline),
the rejected Nov 13 rates dashboard (no yield-curve re-presentation, no
framework).
