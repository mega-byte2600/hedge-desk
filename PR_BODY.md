# Desk 5 SEC/Burry research and Desk 6 Carpe DATA coverage

## What changed

- Connect Desk 5 to the official SEC EDGAR submissions API for the approved watchlist and link the most recent relevant primary filings.
- Add an exact-input, `Decimal` based one-cohort depreciation sensitivity grounded in a specific SEC filing, with transparent tax/EPS/constant-multiple assumptions and no invented Burry score.
- Keep the 48-hour Desk 5 research workflow anchored to Burry's official publication; treat Reddit as an unverified lead source.
- Connect paced GDELT headlines to Desk 6 Carpe DATA as uncorroborated conflict/shipping leads, alongside official event and commodity feeds.
- Show Desk 6's missing contract curves, basis, roll, costs, and specs as explicit gates; no futures candidate is ranked without them.
- Correct mobile desk copy/routes and remove stale generic status claims. Flag Desk 7's dated snapshot as stale when older than two days.
- Add seven-desk coverage audit and regression coverage; package the new stylesheet.

## Validation

Targeted SEC, depreciation, market-context, GDELT, public-signal, Desk 7, public-surface, copy-quality, iPhone-preview, and page-guard checks pass. JavaScript syntax, Python compilation, and whitespace checks pass. Full legacy test discovery remains blocked by the missing `plotly` dependency in `tests/test_dashboard_build.py`.

## Review focus

See `HANDOFF.md` for independent review details, particularly SEC contact/production feed status, financial-sensitivity math, GDELT corroboration labels, narrow-screen review, and Desk 6 futures readiness gates.
