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
2. a versioned, content-addressed Yellow Sheet explaining **WHY** the exact
   candidate and plan are proposed;
3. account/product eligibility and deterministic compliance policy;
4. portfolio exposure and conventional economic-risk controls;
5. exact-plan human authorization for paper execution.

The mandatory lifecycle is:

`Interest → Hypothesis → Investigation → Evidence → Yellow Sheet → Proposed Trade → Deterministic Risk/RoR → Compliance → Human Authorization → Execution`

**NO YELLOW SHEET = NO TRADE.** Missing, incomplete, stale, invalidated, or
hash-mismatched sheets produce an explicit `NO_TRADE` disposition. A human
cannot override that outcome. Each plan holds exactly one active sheet version;
revisions identify the immediately prior version and require a new artifact
hash. AI may research, synthesize, and challenge the sheet, but cannot turn it
into an execution-authorizing decision. Risk/RoR, compliance, audit, and human
authorization remain separate deterministic boundaries.

No future live transition can pass unless an independently hashed Back Office
reconciliation certification is present. Front Office, risk, compliance, human
authorization, and Back Office must all refer to the same immutable plan.

Passing every gate produces a paper-trade decision record. It never submits an
order to a broker.

## Run

```bash
python -m hedge_desk.cli
python -m hedge_desk.cli --approve --human-id captain
python -m hedge_desk.cli --yellow-sheet-rationale
python -m hedge_desk.cli --projects
python -m hedge_desk.cli --overnight-report
python -m hedge_desk.cli --war-games
python -m hedge_desk.cli --morning-markdown
python -m hedge_desk.cli --control-summary --report-input morning-report.json
python -m hedge_desk.cli --validate-data-stack examples/data-stack.synthetic.json
python -m hedge_desk.cli --validate-option-universe-manifest examples/option-universe.synthetic.json
python -m unittest discover -s tests -v
python -m coverage run -m unittest discover -s tests -v && python -m coverage report
```

The default command stops at `human_authorization_required`. The second command
simulates a named human approval and paper-only open/close against a frozen
synthetic fixture; it does not connect to a broker or market-data vendor.
`--yellow-sheet-rationale` prints the candidate, exact plan hash, active sheet
identity/version, gate result, and plain-English WHY without granting authority.

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

## Self-hosted Hermes, Schwab read-only, and iOS

Hermes runs independently as a local supervised service. Verify it with
`hermes doctor` and `hermes gateway status`; Hedge Desk sends no brokerage
credentials or account payloads to Hermes.

The dependency-free backend serves the Objective-C MVP at `127.0.0.1:8765`.
Its Schwab boundary supports OAuth readiness, authorization callback/token
storage, and GET-only account-number retrieval. It defines no order operation,
rejects every POST with HTTP 405, stores tokens only at an ignored local path
with mode `0600`, and returns `orders_blocked: true` throughout.

Configure credentials locally, never in Git:

```bash
export SCHWAB_CLIENT_ID='configured-in-your-Schwab-developer-app'
export SCHWAB_CLIENT_SECRET='configured-locally'
export SCHWAB_REDIRECT_URI='http://127.0.0.1:8765/api/schwab/callback'
./scripts/start_ios_backend.sh
open http://127.0.0.1:8765/api/schwab/authorize
```

The Schwab developer app must use the exact same callback URL. A physical
iPhone cannot reach the Mac through `127.0.0.1`; set
`HEDGE_DESK_API_BASE_URL` in Xcode to a trusted HTTPS backend or the Mac's
trusted-LAN address for development. The Release default is intentionally
nonfunctional until replaced with the operator's HTTPS host.

The buildable project is at `ios/HedgeDeskObjC.xcodeproj` and includes an
original app icon, privacy manifest, configurable API URL, and explicit backend
error states. TestFlight/App Store upload still requires the account owner to
select their Apple Developer team, register the final bundle identifier, supply
the production HTTPS backend and required listing URLs, and authorize submission.

## Safety boundary

- No broker adapter exists.
- Undefined-loss, stale-price, and insufficient-liquidity candidates are
  blocked.
- Risk estimates are model outputs requiring independent validation; they are
  not guarantees of future loss or portfolio survival.
