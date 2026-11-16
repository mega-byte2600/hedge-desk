## Summary

Make Desk 5 the Short Sale Research Desk. The desk is dedicated to developing
source-backed, point-in-time short-sale research cases from the approved
watchlist, challenging the bear thesis with counter-evidence, and exposing
missing research and short-side constraints.

The feature does not generate trade authorization. Short candidates remain
research-only until independently reviewed; broker-specific locate, borrow,
order marking, delivery, and Regulation SHO execution controls remain outside
the desk's authority.

## Controls

- Require SEC filing evidence, independent corroboration, a dated short-interest
  report, catalyst/timing, counter-thesis, valuation and liquidity context,
  invalidation conditions, and conflict disclosure before independent review.
- Reject future-dated source evidence and unsupported claims of broker-confirmed
  borrow.
- Keep short-sale volume distinct from short-interest positions.
- Do not substitute ETFs or other sample symbols for the user's approved
  watchlist.

## Verification

- Focused tests: 78 passed.
- Node browser-module syntax check: passed.
- Python compile check: passed.
- `git diff --check`: passed.
- Full repository test discovery did not complete; see HANDOFF.md.

## References

See `docs/architecture/ADR-0007-desk5-short-sale-research.md` for the CFA
Institute, FINRA Series 7 / Series 4, SEC Regulation SHO, and FINRA short-interest
references.
