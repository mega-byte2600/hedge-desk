# Hedge Desk MVP

> **Corporate motto:** Making money overnight - the dream: making money while
> you sleep.

This is an aspirational product motto, not a promise of investment performance.
The MVP automates overnight research and prepares human-pending, defined-risk
paper-trade proposals. It does not autonomously authorize or execute trades.

This repository implements the first deterministic, paper-only vertical slice
from the Hedge Desk specification.

Original repository code and documentation are open source under
[Apache License 2.0](LICENSE). Market data, model weights, publications, and
other third-party inputs retain their own licenses and are not relicensed here.

See [current implementation status](docs/architecture/STATUS.md) for the tested
MVP matrix, war-game coverage, and known production blockers.
See the [sub-$100 data stack](docs/validation/SUB_100_DATA_STACK.md) and
[local data intake contract](docs/validation/LOCAL_DATA_INTAKE.md) before
supplying licensed snapshots.
The [news evidence boundary](docs/validation/NEWS_EVIDENCE.md) includes a
licensed, point-in-time adapter for Papers With Backtest `All-Daily-News` that
emits hashed symbol-sentiment features without retaining vendor text.
The [High-Flyer and DeepSeek research inventory](docs/research/high_flyer/README.md)
provides Astra with a validated official-source catalog, license boundaries,
desk mappings, and a bounded local-model evaluation handoff.

## Build culture: the 80/20 hacker rule

- **80% working code:** fail fast, build, measure, learn, and ship small tested
  vertical slices.
- **20% ADR:** record only decisions needed to reproduce, review, or safely
  change the software.
- A feature is not real until it has deterministic tests and a runnable path.

## MVP series

1. **Overnight Premium Desk:** defined-risk premium-selling research with a
   planned pre-expiration close. It monitors continuously but admits at most
   one new-entry evaluation per calendar month and enforces a minimum 21-day
   interval on the `America/New_York` market calendar; cadence admission never
   authorizes a trade.
2. **Earnings Event Paper Desk:** earnings/guidance surprise and market-response
   research with a defined-risk directional leg, independently calculated hedge,
   and explicit `NO_TRADE` outcome.
3. **European Index Box/Parity Observer:** paper-only search for theoretical
   identity dislocations using deterministic executable-side economics.
4. **Dividend Opportunity Desk:** rank sustainable dividend opportunities from
   point-in-time ten-year histories, then compare owning shares, a defined-risk
   option expression, and `NO_TRADE`. Long calls do not receive dividends, so
   the system must never equate buying a call with earning the cash payout.
5. **Open Quant/AI Model Lab:** independent Quant and AI research teams using
   versioned open code, open-weight models where applicable, explicit licenses,
   immutable hashes, frozen training cutoffs, and reproducible evaluations.
   Purged walk-forward train/validation/test windows and embargoes are enforced
   by executable split gates, not model-authored metadata.
   Neither team can create authoritative RoR, clear compliance, or authorize a
   trade.
6. **Weather/War/Logistics Futures Event Desk:** compare validated physical
   event surprise with what the curve already prices, basis, roll, liquidity,
   margin, and transaction costs. Physical delivery and live trading are
   disabled.

Together these MVPs build toward a coordinated 24/7 research orchestration. Each
MVP shares the same deterministic calculation, independent risk, audit, and
human-authorization controls.

Specialized research agents include an Arbitrage Research Agent and an
off-exchange-flow research path. An independent Compliance Agent assists a
deterministic Compliance Policy Engine. Human judgment remains a distinct,
explicit decision point and cannot override risk or compliance blocks.

The system evaluates every trade candidate through independent gates:

1. source provenance, entitlement, point-in-time, and schema validation;
2. account/product eligibility and deterministic compliance policy;
3. portfolio exposure and conventional economic-risk controls;
4. exact-plan human authorization for paper execution.

No future live transition can pass unless an independently hashed Back Office
reconciliation certification is present. Front Office, risk, compliance, human
authorization, and Back Office must all refer to the same immutable plan.

Passing every gate produces a paper-trade decision record. It never submits an
order to a broker.

## Run

### Web console (Emporion)

The console is a single-page app served by `hedge_desk.server`, which also owns the
JSON API. Do **not** serve `web/` with a plain static server: the membership, tier
and report routes live in the server, and the page will load without them.

```bash
python scripts/build_web.py                 # bundle web/ -> dist/
bash scripts/demo.sh                        # serve on :8765 (PORT=… to change)
# or: PORT=8765 python -m hedge_desk.server
```

Open `http://localhost:8765`. Sign-in codes print to the terminal (dev mail
fallback) until `SMTP_*` is configured.

Deployed: <https://hedge-desk.onrender.com> (Render free tier; it sleeps when idle).

#### What is in it

- **Eight tabs** — Overview, Candidates, Research desks, Scenario lab, Yellow
  Sheets, Research resources, Multi-agent desk, About.
- **Three access tiers, published openly.** GUEST is the open 31-day test drive on
  synthetic research only. MEMBER is the self-serve subscription: real market data
  and connecting your own broker **read-only**. LP is an investor in the LLC —
  invited by the GP, never a paid tier, capped at 99 seats. The About tab states all
  three; the server enforces them (`/api/tier`), and the guest lane is never walled.
- **Email-OTP sign-in** with rate limiting (5 codes per address / 15 min, 20 per IP),
  a first-party consent list, and `HttpOnly` session cookies. Social login via
  Supabase Auth appears only when `SUPABASE_URL` + an anon key are configured.
- **GP console** — appears for the `GP_EMAIL` address: LP seats used against the cap,
  member counts, and issue-an-LP-invite. Enforced server-side, not just hidden in UI.
- **Broker linking (read-only)** — tier-gated Schwab OAuth scaffold. It reports
  "not configured" cleanly until `SCHWAB_*` is set, and the desk never places orders.
- **Multi-agent desk** — the six SOUL specialists, their models, mandates and
  boundaries, plus a results timeline. Commit history is shown only when the
  timeline loads; it is never fabricated.
- **Yellow Sheets / Trade Log** — thesis, evidence, invalidation, then the closeout
  lifecycle (planned exit, trade status, why exit, post-trade review), stored in the
  browser with the report hash they were written against.
- **Scenario lab** — the recorded war games and stress cases, searchable and
  filterable, each opening its exact engine record.
- **Research resources** — primary-source-first institutional links, every external
  link `rel="noopener"`.

The console displays validated synthetic report snapshots, desk controls, scenario
evidence and browser-local research notes. See
[web console instructions](web/README.md) for exports.

#### Verify and validate before demoing

```bash
bash scripts/demo.sh > /tmp/demo.log 2>&1 &        # server, codes -> /tmp/demo.log

node scripts/vv_console.mjs  http://127.0.0.1:8765            # full V&V matrix
node scripts/vv_console.mjs  http://127.0.0.1:8765 --engine=webkit
node scripts/smoke_console.mjs http://127.0.0.1:8765          # routes + data-loss + RoR + desks
node scripts/smoke_auth.mjs  http://127.0.0.1:8765 /tmp/demo.log   # sign-in lifecycle
```

V&V follows `docs/CONSOLE_VV_SPEC.md`: **VERIFIED** means the artifact meets its
specification (measured by the commands above plus `python -m unittest discover -s
tests` and `node --test web/`); **VALIDATED** means it meets the GP's expectations
for function and use. Browser tooling is optional — the scripts print `SKIP` and
exit 0 when Playwright is absent.

```bash
python -m hedge_desk.cli
python -m hedge_desk.cli --approve --human-id captain
python -m hedge_desk.cli --projects
python -m hedge_desk.cli --overnight-report
python -m hedge_desk.cli --war-games
python -m hedge_desk.cli --morning-markdown
python -m hedge_desk.cli --control-summary --report-input morning-report.json
python -m hedge_desk.cli --validate-data-stack examples/data-stack.synthetic.json
python -m hedge_desk.cli --validate-option-universe-manifest examples/option-universe.synthetic.json
python -m hedge_desk.cli --pwb-news-summary --pwb-source-timezone UTC --max-age-seconds 172800
python -m unittest discover -s tests -v
python -m coverage run -m unittest discover -s tests -v && python -m coverage report
```

The default command stops at `human_authorization_required`. The second command
simulates a named human approval and paper-only open/close against a frozen
synthetic fixture; it does not connect to a broker or market-data vendor.

The overnight report evaluates every registered MVP through separately labeled
`OBSERVED`, `STAT`, `BIG`, `DETERMINISTIC_RISK`,
`DETERMINISTIC_COMPLIANCE`, and `HUMAN` layers. Until real
licensed adapters exist, it truthfully runs synthetic fixtures and returns
`NO_TRADE` for architecture-only projects. GitHub Actions runs this paper-only
evaluation every 15 minutes, 24/7, and retains its JSON report for 30 days.
GitHub scheduling is best-effort; delayed runs do not constitute a production
uptime guarantee.

The two strict data commands exercise the entitlement/capability gate and the
cross-underlying local option intake. Local vendor payloads remain outside the
repository; only validated, content-addressed derived output is emitted. Neither
command estimates win probability, calculates Risk of Ruin, or authorizes a
trade.

`--control-summary` refuses unpublishable or tampered reports, then emits only
the validated operator headlines: paper versus real results, scenario/control
counts, combined synthetic stress result, and live-release status.

CI enforces at least 80% branch coverage over the complete `hedge_desk`
package. The measured baseline includes CLI code even though subprocess-driven
CLI tests are not attributed to the parent coverage process.

## Safety boundary

- No broker adapter exists.
- Undefined-loss, stale-price, and insufficient-liquidity candidates are
  blocked.
- Risk estimates are model outputs requiring independent validation; they are
  not guarantees of future loss or portfolio survival.
