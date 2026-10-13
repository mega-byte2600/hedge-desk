# FRED measurement and integration audit — 2026-10-05

## Diagnosis

At main a158ff8, the source-status probe fetched CPIAUCSL over 60 days,
selected only the last row, and wrapped it in a `latest` dictionary.
`_observation_count` counts any nonempty dictionary as one. The displayed
“1 data points” therefore measured that wrapper, not series breadth or the
number of observations fetched. LIVE required only a nonempty result: it did
not measure observation age, release-calendar timeliness, completeness, or a
fresh network request.

The live market-context endpoint separately fetches daily DFF over 14 days,
counts its rows, and displays at most five. Rates/macro desks use additional
FRED series and lookback windows. A CPI availability probe cannot certify
those consumers. The dashboard also rewrote last night's Rates (FRED) result
when CPI succeeded, falsely implying that the historical failure was fixed.
That override is removed.

CPIAUCSL is monthly. On the official series page inspected October 5, its
latest observation is August 2026, updated September 11, with the next release
October 14. An observation date is the period date, not the release timestamp.
The old October 5 60-day start excludes August 1; it can return no rows even
when the source is working. The probe now uses 120 days, counts returned usable
observations, and identifies its dataset, window, latest period date, and age.
Freshness and coverage are explicitly NOT_ASSESSED. No arbitrary daily-data
age threshold is applied to monthly CPI.

## Integration changes and bounds

- Cache entries previously had no expiry; same-window calls could reuse data
  indefinitely and legacy/corrupt caches could return empty or invalid rows.
  Entries now require a retrieval timestamp younger than one hour and validated,
  nonempty observations. Legacy, expired, future-dated, and corrupt entries are
  refetched. An upstream failure does not serve an expired entry.
- Cache keys remain series/start/end. Unique temporary files prevent simultaneous
  writers from sharing a temporary path; replacement remains atomic. The TTL is
  an application cache policy, not evidence that the observation is current.
- CSV/JSON observations validate calendar dates, discard missing/nonfinite values,
  sort chronologically, reject conflicting duplicates, and filter to the requested
  window. JSON advertised counts larger than the returned page fail closed;
  automatic pagination is not implemented. Malformed CSV headers/rows fail closed.
- Keyed transport exceptions are suppressed because their text may contain the
  request URL. Cache payloads contain observations and timestamps, never API keys.
- Route order remains configured JSON API, machine-local skill CLI when available,
  then public CSV when no key/CLI result exists. No new secrets are provisioned.
  A failed configured JSON request does not automatically fall back to CSV.
- Dashboard probe details explicitly separate availability from freshness/coverage
  and warn that probes may use cache. The surrounding API cache still applies.
  Legacy desk `data_source` labels remain route-agnostic and should not be read as
  proof of a fresh CSV request. Exact route/cache-hit provenance and release-calendar
  freshness assessment remain follow-up work; this patch does not authorize risk use.

Window validation also exposed a pre-existing CPI request gap: the macro desk's
400-day range could exclude the prior-year monthly period while the latest
release lagged the as-of date. The existing fixture supplied that excluded row,
hiding the gap. The range is now 450 days and the fixture verifies the request
includes its August prior-year baseline; YoY arithmetic is unchanged.

## PR #156 boundary

Inspected open PR #156 at f017477306475dc63fdea0743ed0c7e626baade1.
Its BLS registered-v2/keyless-v1 fallback matches official BLS documentation;
its list/object result handling covers the published shapes. It caches keyless
requests for 23 hours; this is process-local, so restarts/multiple workers can
still consume the shared upstream quota. Returning one BLS row is deliberate
latest-only coverage, not complete historical coverage. It does not assess
release timeliness. SEC contact-identity gating follows the official declared
user-agent example. SEC context is limited to four mapped watchlist issuers
and five recent filings each; LIVE can coexist with partial issuer failures.
No claim of complete filings coverage follows from its status.

This FRED branch does not alter PR #156's BLS/SEC implementation or tests.
Both branches touch web_app.py in separate sections; verify the combined result
before merge. No Render settings, trading, financial models, or risk controls change.

## Deployment acceptance

After CI and review, deploy through the project's authorized release flow, then
remeasure `/api/data-sources`, `/api/market-context`, and the dashboard from the
production host. Record the deployed commit and measurement time. Confirm actual
CPI count/window/latest date, separate DFF counts, and BLS/SEC statuses/reasons.
Exercise expiry through deterministic tests rather than modifying production data.
Source availability from this developer environment is not production verification.

## Primary sources

- https://fred.stlouisfed.org/docs/api/fred/series_observations.html — observation
  fields, window parameters, count/limit/offset; missing observations use `.`.
- https://fred.stlouisfed.org/series/CPIAUCSL — monthly frequency, period versus
  update/release dates, revisions, attribution.
- https://www.bls.gov/developers/api_FAQs.htm — registered/unregistered API limits.
- https://www.bls.gov/developers/api_signature.htm — official v1 signatures.
- https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data —
  declared user-agent identity, fair access and submissions API guidance.
