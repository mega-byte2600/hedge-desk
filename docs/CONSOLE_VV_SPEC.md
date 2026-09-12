# Emporion console — V&V specification

Two different words, never used interchangeably:

- **VERIFIED** — the artifact meets its **specification**. Objective, repeatable,
  measured by a command. A test passing is verification.
- **VALIDATED** — the artifact meets the **GP's expectations for function and use**.
  Judged against stated expectations and the published demo runbook. Only the GP can
  finally accept this; the harness reports evidence for it.

Every claim in a status report must name which of the two it is.

## How specs are set

1. **Hard spec** — the repo already fixes the value (a constant, a contract, a rule in
   `AGENTS.md`). Quote the source. No latitude.
2. **Derived spec** — no hard value exists, so one is derived from what this web app
   actually is: a single-page research console on Render's free tier, opened by a
   demo audience on a laptop or phone. The derived target and the **tolerable range**
   are both stated, with the reasoning, so the range can be argued rather than
   assumed.

Runner: `node scripts/vv_console.mjs <url> [--engine=chromium|webkit]`. Exit code 0
means every check met its spec. Measured values are printed beside each target.

---

## A. Hard specs (values fixed by the codebase)

| # | Spec | Source | Pass condition |
|---|------|--------|----------------|
| H1 | Guest test drive lasts 31 days | `GUEST_ACCESS_DAYS = 31`, membership.py | `/api/tier` reports `guest_days_left` in 30–31 on a new guest |
| H2 | LP seats capped at 99 | `MAX_LP_MEMBERS = 99`, membership_base.py | cap reported as 99; enforced server-side |
| H3 | Paper only, no live orders | `AGENTS.md`; `live_orders_enabled: false` | `/api/health` returns `mode: paper` and `live_orders_enabled: false` |
| H4 | Real data is member/LP/GP only | tier_access.py | guest `/api/data/real` → 403; member → 200 |
| H5 | Unknown `/api/*` is a JSON 404 | server.py dispatch | status 404, `content-type: application/json`, body has `error` |
| H6 | OTP request limit 5 per address / 15 min | `SlidingWindowLimiter(5, 900)` | 6th request in the window → 429 |
| H7 | OTP request limit 20 per IP / 15 min | `SlidingWindowLimiter(20, 900)` | 21st request from one IP → 429 |
| H8 | Session cookie is HttpOnly + SameSite + Path | auth_app.py | Set-Cookie contains all three; `Secure` over TLS; `Cache-Control: no-store` |
| H9 | A sign-in never lowers a role | membership.py / supabase_membership.py | LP/MEMBER/GP survive `upsert_guest` |
| H10 | Yellow Sheet lifecycle fields persist | web/yellow-sheet.js | all 9 fields stored after submit |
| H11 | Zero uncaught JS errors on any route | a console must not error | 0 `pageerror` events across the walk |
| H12 | No tracked secrets or credentials | GP directive; SECURITY.md | no key material, tokens, or `.env` in tracked files |

## B. Derived specs (no hard value in the repo — target and tolerable range)

The console is a static SPA whose data comes from one engine call, served from
Render's free tier, demoed live. Ranges are set from that context, not from generic
web advice.

| # | Spec | Target | Tolerable | Why this range |
|---|------|--------|-----------|----------------|
| D1 | Route renders its content (warm, local) | ≤ 2.0 s | ≤ 4.0 s | one `/api/report` round trip plus DOM build; beyond 4 s a viewer assumes it broke |
| D2 | Main thread never blocks | 0 blocks | block ≤ 1.0 s, never twice | a freeze has shipped twice here; any block is a defect, but a single sub-second hitch is invisible on a laptop |
| D3 | Warm API latency, local | ≤ 300 ms | ≤ 1.5 s | engine work is cached 15 s; 1.5 s is where a click feels unresponsive |
| D4 | Live cold start (Render free sleeps) | ≤ 45 s | ≤ 75 s | free-tier wake-up is outside our control; past ~75 s a demo audience will have lost confidence |
| D5 | Live warm page load | ≤ 3.0 s | ≤ 6.0 s | cross-region round trip plus free-tier CPU |
| D6 | One slow cache build must not block another endpoint | ≤ 300 ms | ≤ 500 ms | measured directly; a shared lock across a 5 s network probe was a real defect |
| D7 | Rate-limiter key map stays bounded | ≤ `max_keys` | 10 000 keys | caller-controlled keys on a 512 MB instance |
| D8 | A desk is openable from the Research desks tab | ≥ 1 wired surface | all 6 evaluated desks | the tab lists desks; if none opens, its purpose is unmet |
| D9 | Every actionable control has a defined outcome | 0 dead controls | 0 dead controls | "all links, tabs, and clicks work" is a GP expectation; no latitude assigned |

## C. GP expectations — the VALIDATION criteria

Recorded as stated. These are judged, not measured, though the harness gathers the
evidence.

| # | Expectation (as stated) | Evidence the harness produces |
|---|-------------------------|-------------------------------|
| V1 | "it cant be gettin stuck no way no how" | D2 + full route walk + control sweep: zero blocks, zero freezes |
| V2 | "all links, tabs, and clicks work?" | D9 sweep: every control yields a defined outcome |
| V3 | "imperative that this is fixed tonight so i can check out site and prep for demo" | the published runbook's 9 steps, executed against the **deployed** URL |
| V4 | "sw architect … elegant and not redundant nor inefficient" | architecture review + the open-debt list in the PR trail |
| V5 | "never expose secrets, phi, or pii" | H12 scan + the known published-email item flagged for the GP's decision |
| V6 | "production level code this aint a hobby" | CI green on every change; guard tests that fail on the pre-fix commit |

## D. Definition of done for any change

A change is done only when all four hold, and the PR says so explicitly:

1. **VERIFIED** — the spec it changes is met, measured by a command, and a test that
   fails on the pre-fix commit pins it.
2. **VALIDATED (evidence)** — the expectation it serves is exercised end to end on the
   deployed URL, not only locally.
3. **No regression** — the full suite and the full V&V runner are green.
4. **Known gaps stated plainly** — anything still unmet is named, with what it needs.

## E. Standing limitation

Automated validation cannot accept the product. V3 in particular stays *partially*
validated while the deployed service lacks `SMTP_*` and `GP_EMAIL`: sign-in codes
reach only the Render log and the operator's console needs the GP address. Those two
values are the difference between "the demo works if you read the server log" and
"the demo works as published". See `docs/DEMO_RUNBOOK.md` §5.
