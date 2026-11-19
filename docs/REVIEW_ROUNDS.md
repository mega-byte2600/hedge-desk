# Independent review rounds

Each round: an independent reviewer (a separate agent that does not see the
fixer's reasoning) scores six dimensions from 1 to 10. Everything below 9
is fixed against primary sources and saved as a tagged version
(`review-rN`). The loop stops when every score is 9 or higher. Risk-control
and model changes are implemented and tested here but **not self-approved**
(AGENTS.md); each one is listed for independent review.

## Score history

| Round | Version | Code quality | API & data health | UI/UX | Insight | Rigor | Actionability |
|---|---|---|---|---|---|---|---|
| 1 (baseline, pre-fix) | `review-r1` | 6 | 6 | 5 | 7 | 6 | 5 |

## Round 1 — fixes shipped in `review-r1`

**Tests:** 1,313 passed and 51 subtests passed, 0 failed (baseline: 4 failed).

**Code quality (6)**
- CI ran `unittest discover`, which never collects pytest-style tests, so
  four failures got through. CI now runs `coverage run -m pytest`.
- Fixed the tests that depended on the calendar:
  - The options-seed refresh takes an injected clock (`now=`).
  - The short-board API test asserts against the committed artifact instead
    of literals.
- Restored the broker-scope disclosure in the console footer.
- Added a `[tool.ruff]` config and a CI lint step (gating set: E9, F, B).
  Cleared all 77 findings, including F821 (`Optional` undefined in
  `email_transport.py`) and B023 (a loop variable captured in a lambda).

**API & data health (6)**
- `feed_base.with_retries`: bounded exponential backoff with full jitter,
  only on transport errors, 429 and 5xx (per Google SRE *Handling Overload*
  and AWS *Exponential Backoff and Jitter*). Wired into the Cboe, EOD and
  `make_get_transport` fetchers.
- `/api/report` no longer returns a bare 503 when a real report was built in
  the last 72 hours. It serves that report labelled `freshness.status=STALE`
  with its age and the live error, and `trade_authorized=false`. It still
  fails closed if there is none. Nothing synthetic is served.
- `/api/options-seed` now carries `freshness` (age, `is_stale`) against
  the weekly refresh SLA.
- EOD prices are quantized to 4 dp at ingest
  (`12.920000076293945` → `12.92`).

**UI/UX (5)**
- `am-demo.html` loads the vendored Plotly first (served path, then the
  repo-relative path, then the CDN). It now renders 14 of 14 charts offline.
- Logo fallback for file opens; times shown in readable form; mobile has no
  horizontal scroll at 390 px (was 481 px).
- The console stamp shows STALE, with the age and the reason, when the
  fallback is used. Fixed the doubled "Data unavailable: data unavailable"
  message.

**Rigor (6)** (model changes, pending independent review)
- `win_probability`:
  - Documented that |Δput| = N(−d1) **overstates** a short put's win
    probability compared with the risk-neutral N(−d2) (Hull, eq. 15.21),
    by about 2.6 points for a 30-day 5%-OTM put at 28% IV.
  - The exact `risk_neutral_win_probability` is added alongside the released
    value; the gate value is unchanged.
  - The A&S CDF is replaced by `erf`.
  - Reference case added: Hull's Example 15.6.
- The Cboe spread scan now reports the probability of profit,
  P(max loss) and risk-neutral EV for each leg using its own exchange IV. It
  ranks by EV, then probability of profit, instead of return on risk, which
  favoured near-the-money coin flips.

**Actionability (5) / Insight (7)**
- `hedge_desk/desk_call.py` and the am-demo header:
  - A **Desk call** states the action. It is `NO_TRADE` unless the data is
    current and the existing risk gate says APPROVED; the gate is consumed,
    not re-evaluated.
  - It gives a top-3 shortlist with invalidation (break-even), released exit
    rules (50% profit capture, 50% max-loss stop) and max loss as a share of
    demo equity, plus VIX context.

**Needs independent (human) review before release:** promoting N(d2) to the
gate value, and the EV-first ranking.
