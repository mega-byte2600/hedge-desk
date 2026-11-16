# HANDOFF — Desk 5 Short Research candidate board

Branch: `toby/desk5-short-research` (base: `d93bd49`).

## What changed

- `hedge_desk/short_research_board.py` builds an API payload from the latest
  nightly report's configured watchlist and real EOD close series. It calculates
  5-session and 20-session returns and emits a descriptive price-context bucket.
  It never invents a short thesis, catalyst, SEC filing status, short interest,
  borrow status, or trade authorization.
- `hedge_desk/server.py` exposes `/api/short-research` with `no-store` caching.
- `hedge_desk/web_app.py` now probes EDGAR with the declared SEC user agent, a
  single bounded 5-second request, and no retry. A probe outage no longer falls
  back to another slow SEC request. The actual SEC request from this workspace
  timed out; live connectivity remains unverified here.
- `web/index.html` and `web/app.js` add a dedicated Desk 5 navigation route, a
  Plotly return-context scatter with direct symbol labels and source-dated hover
  details, a mobile-friendly queue, explicit missing-evidence fields, and
  broker-readiness controls.
- `tests/test_short_research_board.py` covers exact calculations, failed/missing
  source behavior, API response semantics, and the current report's two
  negative/negative price-context rows.
- Desk 5 documents an explicitly labeled Burry-inspired valuation diagnostic,
  without an invented Burry formula, plus Schwab/TOS manual availability,
  locate, fee, quantity, and timestamp checks. The 48-hour task now includes
  this research lens and broker checklist.

## Current report read

The latest checked-in report contains seven watchlist symbols with EOD closes
through 2026-11-13. LYFT and F are negative in both return windows. The board
calls them price-context follow-ups only. All seven remain `NO_SHORT_THESIS`;
SEC case research, dated catalysts, reported short interest, and broker borrow
evidence are not in the short research files. None is represented as
broker-ready.

## Research basis

- [Plotly scatter reference](https://plotly.com/javascript/reference/scatter/)
  and [hover formatting](https://plotly.com/javascript/hover-text-and-formatting/)
  support the directly labeled, responsive chart and explain-on-hover pattern.
- [SEC Regulation SHO overview](https://www.sec.gov/investor/pubs/regsho.htm)
  describes Rule 201 and locate requirements. A public chart cannot establish a
  broker locate.
- [FINRA short-interest explainer](https://syndication.finra.org/content/short-interest-what-it-what-it-not)
  distinguishes periodic short-interest position snapshots from daily
  short-sale volume.
- CFA Institute Standards V(A), V(B), VI(A), FINRA Series 7 short-sale concepts,
  and Series 4 supervisory concepts are research lenses only. No licensed exam
  material is reproduced.

## Verification

- 151 targeted Python tests passed across Desk 5, SEC/open-market integrations,
  data-source health, Desk 7 Plotly, and the live web-data plane.
- Browser ESM syntax check, `git diff --check`, and `scripts/build_web.py`
  passed.
- Direct SEC API request timed out after 4 seconds from this workspace. The
  source-health probe is now bounded, but a live EDGAR `LIVE` response has not
  been achieved or claimed.
- Visual browser QA could not be completed: Playwright's bundled Chromium was
  absent and the available system Chromium could not launch in this sandbox.
  Phone-width rendering and Plotly blocked-load fallback remain reviewer checks.
- The repository's full suite is not claimed in this turn.

## Reviewer checks before merge

1. Match the plotted returns against the real closes in the latest report.
2. Keep price weakness a review cue, never a recommendation or ranking.
3. Block Plotly and verify the table and evidence gaps remain readable on desktop
   and phone.
4. Populate catalysts, filings, short interest, or borrow only from timestamped
   sources; execution and broker locate stay outside this paper-only app.
