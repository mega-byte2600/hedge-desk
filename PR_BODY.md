## Title

Desk 5: add sourced short-research queue and Plotly price-context map

## Body

Add a dedicated Desk 5 view backed by the latest validated nightly watchlist
snapshot. The Plotly scatter compares each symbol's 5-session and 20-session
price changes, labels points directly, and exposes close/as-of values on hover.
The queue carries the same sourced values and makes missing SEC research,
catalyst dates, short-interest reports, and borrow evidence explicit.

On the current snapshot, LYFT and F are negative over both lookback windows.
They are surfaced only as price-context follow-ups. No symbol has a completed
short thesis, and no short-sale recommendation, locate, broker confirmation, or
trade authorization is represented.

The design follows Plotly's scatter/hover guidance, SEC Regulation SHO
requirements, and FINRA's distinction between reported short interest and
daily short-sale volume. CFA Standards V(A), V(B), VI(A), FINRA Series 7, and
Series 4 supervisory concepts inform the research checklist without copying
licensed materials.

**Verification:** 24 targeted tests, ESM syntax, `git diff --check`, and web
bundle build passed. Browser visual QA was not completed in the sandbox; see
HANDOFF.md for details and the remaining phone-width review.

Adds a one-request, five-second SEC source-health probe to prevent a blocked EDGAR
request from holding the endpoint through repeated 15-second retries. Desk 5
also states the Burry-inspired valuation diagnostic and Schwab/TOS manual
locate/borrow verification fields. The existing 48-hour research task now uses
the same research and broker checklist.

**Current verification:** 151 targeted tests, ESM syntax, `git diff --check`,
and web bundle build passed. SEC EDGAR timed out from this workspace, so no live
feed success is claimed. Browser visual QA was not completed in the sandbox;
see HANDOFF.md for remaining review checks.
