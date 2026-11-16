# Desk 5 Short Sale Research — handoff

## What changed

- Reassigned the Desk 5 product label and purpose to Short Sale Research while
  retaining the legacy project ID for report and mobile-client compatibility.
- Added an evidence-completeness gate that requires SEC filing evidence,
  corroborating sources, dated reported short-interest evidence, thesis and
  counter-thesis, catalyst timing, valuation and liquidity context, invalidation
  conditions, and conflict review.
- Added point-in-time checks, explicit unknown borrow status, and an evidence
  requirement before broker-confirmed borrow can be represented.
- Desk 5 no longer receives generic ETF seed candidates or a default quote
  universe. Its live-data response identifies the missing approved watchlist.
- Added the CFA / FINRA Series 7 and Series 4 / Regulation SHO reference map and
  research-only limits in ADR-0007.
- Added the 48-hour Desk 5 research automation in ChatGPT Automations. It
  researches the approved watchlist, reports direct sources and timestamps, and
  does not authorize trades. It returns no company candidates if the approved
  watchlist is absent from the task context; it will not invent a universe.

## Verification

- 78 focused Python tests passed across short research, project registry,
  overnight report, web contract/server, iOS product surface, public web
  contracts, copy quality, and no-synthetic-production checks.
- Browser-module syntax parse passed with Node; changed Python modules compiled.
- `git diff --check` passed.
- The full repository unittest discovery did not complete in this environment;
  its run stalled during the oil-desk transport test. No full-suite pass is
  claimed.

## Reviewer checks

- Review the short research completeness criteria and confirm these are the
  desired minimum inputs before review status.
- Confirm Desk 5 watchlist wiring and live SEC filing enrichment before marking
  the desk as a working foundation or publishing actual candidates.
- Confirm any future broker borrow fields are source-bound, time-stamped, and
  never used as locate or order authorization.
- The feature branch includes earlier sign-in removal and SEC client-identity
  commits already present in its base history. Those earlier changes were not
  re-audited as part of this Desk 5 verification.
