# HANDOFF — Desk 5 Short Research candidate board

Branch: `toby/desk5-short-research` (based on `d93bd49`).

## What changed

- `hedge_desk/short_research_board.py` builds an API payload from the validated
  nightly report's watchlist, EOD source results, and actual close series. It
  computes 5-session and 20-session price changes and classifies only the
  descriptive direction of those two windows. It does not infer a short thesis,
  catalyst, SEC status, short interest, borrow, or trade authorization.
- `hedge_desk/server.py` serves the payload at `/api/short-research` with
  `no-store` caching.
- `web/index.html` and `web/app.js` add a dedicated Desk 5 nav page with a
  responsive Plotly return-context scatter, direct labels and hover details,
  a mobile-friendly research queue, clear missing-evidence fields, and broker
  readiness gates.
- `tests/test_short_research_board.py` pins exact arithmetic, fail-closed source
  behavior, missing-report behavior, API response semantics, and the current
  seven-symbol snapshot's two negative/negative price-context names.

## Current data read

The checked-in nightly report has seven watchlist names, with real EOD closes
through 2026-11-13. LYFT and F are negative over both the 5-session and
20-session windows. They are only price-context follow-ups: all seven rows say
`NO_SHORT_THESIS`; SEC filing research, dated catalyst research, reported short
interest, and broker borrow evidence are not present in the short-case files.
No short candidate is represented as broker-ready.

## Research / compliance basis

- Plotly's official JavaScript reference and hover-formatting documentation
  support directly labeled scatter points, date/number formatting, and
  responsive chart layout.
- SEC Regulation SHO materials distinguish Rule 201's price-test circuit
  breaker from broker/dealer locate controls; locating shares is not established
  by a public chart.
- FINRA explains that short-interest position reports are periodic snapshots
  and are not the same data as daily short-sale volume.
- CFA Institute Standards V(A), V(B), VI(A), FINRA Series 7, and Series 4
  supervisory concepts remain interpretive reference lenses only. No licensed
  exam-manual material is included.

## Verification

- 25 targeted tests passed across Desk 5 board/research, Desk 7 Plotly contract,
  and the live web-data plane.
- ESM parser check passed using a `.mjs` copy of `web/app.js`.
- `scripts/build_web.py` passed; `git diff --check` passed.
- A browser visual pass was not run in this turn. Recheck phone-width layout and
  Plotly fallback before merge. Full-suite completion is not claimed.

## Reviewer checks

1. Confirm the plotted returns match the latest report's real close series.
2. Confirm negative/negative price context remains a review cue, never a
   recommendation or ranking.
3. Block Plotly and verify the visible table and missing-evidence statuses still
   work on desktop and phone.
4. Confirm SEC filings, event dates, reported short interest and borrow fields
   become populated only from timestamped source evidence; broker locate,
   order marking and execution remain outside this paper-only app.
