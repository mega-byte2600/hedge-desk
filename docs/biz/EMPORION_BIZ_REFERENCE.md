# Emporion — business reference

Generated for demo prep. Refresh with `bash scripts/biz_prep.sh`.
Everything marked **[SHIPPED]** is in `main` and verified; **[2.0]** is positioning
prep only and deliberately out of scope for this build.

---

## 1. The pitch, in the GP's words

> "If you were an institutional trade-desk manager and started an app that let retail
> investors have what is usually behind doors in back office, etc — Emporion allows you
> to have a compass to navigate the seas of the market and make it to shore. That means
> in manual mode you can use our multilayered AI to have your watchlist 'activated' like
> that of a professional money manager's portfolio."

One-line form: **Emporion is a compass for the retail investor — it turns a watchlist
into a researched, risk-checked decision instead of a pile of tickers.**

## 2. The two modes, named in domain terms

| | **Manual mode** | **Full-service mode** |
|---|---|---|
| Who holds the decision | The client | The client, with automation executing |
| What Emporion does | Activates the watchlist: qualifies candidates, gathers and challenges evidence, runs the scenario set, writes the thesis and its invalidation, clears the survival gate | The same suite, end to end, without a human step in the loop |
| User's choice | Take the candidates the desks surface, **or configure your own desks** on the same research layer | Choose notification cadence; stop valves ("kill switch") remain the user's |
| Price | Lower | Higher |
| Status | **[SHIPPED]** as research + decision support; execution stays manual | **[2.0]** — automated execution is not in this build |

### Vocabulary, tied to sources

| Concept | Term | Basis |
|---|---|---|
| Investor who may hold the higher-risk unregistered offering | **accredited investor** | SEC Regulation D, Rule 501 |
| Investor in a private fund such as the LLC | **qualified purchaser** | Investment Company Act Sec. 2(a)(51) |
| End-to-end automated trading | **automated / algorithmic trading** | standard regulatory vocabulary |
| The user-held stop valve | **kill switch** | SEC Rule 15c3-5 (Market Access Rule); FINRA names kill switches for highly automated firms |

**Kill switch, stated honestly.** Rule 15c3-5 obliges a broker-dealer *with market
access* to maintain risk-management controls and supervisory procedures, and FINRA
describes kill switches as part of that duty for highly automated firms. Emporion is not
a broker-dealer: this is a product control built in the spirit of the rule, **not** a
compliance claim. Making it a real compliance posture is for securities counsel,
alongside the fund structure.

## 3. The tier model (revenue shape)

    GUEST    free, open, 31-day test drive, synthetic research only, converts to MEMBER
    MEMBER   self-serve subscription  <-- THE REVENUE PATH: real data + own broker (read-only)
    LP       investor in the LLC, invited by the GP, never a paid tier, capped at 99

GP issues every LP invite. LPs are investors, not customers; subscribers are the revenue.

## 4. What is shipped and can be demoed today

- **[SHIPPED]** Eight tabs: Overview, Candidates, Research desks, Scenario lab, Yellow
  Sheets, Research resources, Multi-agent desk, About.
- **[SHIPPED]** Email-OTP sign-in, rate-limited (5 codes/address/15 min, 20/IP),
  `HttpOnly` sessions, first-party consent list.
- **[SHIPPED]** Three tiers enforced server-side, not just displayed.
- **[SHIPPED]** GP console: LP seats against the 99 cap, member counts, invite-an-LP.
- **[SHIPPED]** Multi-agent desk: six SOUL specialists with distinct model families,
  mandates and hard boundaries.
- **[SHIPPED]** Scenario lab: recorded war games and stress cases, searchable, each
  opening its exact engine record.
- **[SHIPPED]** Yellow Sheets with the full lifecycle: thesis, evidence, what would
  invalidate it, planned exit, trade status, why-exit, post-trade review.
- **[SHIPPED]** Read-only broker link scaffold (tier-gated; reports "not configured"
  cleanly until `SCHWAB_*` is set; the desk never places orders).
- **[SHIPPED]** Deterministic risk gate with reason codes; no agent may override it.
- **[SHIPPED]** Tamper-evident, hash-chained membership audit trail.
- **[SHIPPED]** Social sign-in via Supabase Auth, wired and verified end to end against a
  locally minted token; off in production for lack of `SUPABASE_*` config.

## 5. Copy gap — what the site does not yet say

The site states the **input** half of the promise but not the output half.

| The site currently says | What is missing |
|---|---|
| "Bring your watchlist. Research it your way." | what the system **does** with the watchlist — it activates it |
| "Your choice. Your data. Your money." | that this is the machinery normally behind a desk's closed doors |
| "Research it your way" | the two modes, named, and what each gives you |
| Candidates tab: "UNIVERSE, NOT PICKS", "Method-qualified picks: 0" | that the desks surface candidates the client acts on |
| "does not generate a live order" (repeated) | the positive trust feature: the user-held kill switch / stop valves |
| Member tier row: "manual or automated service" | a real explanation of manual vs full-service |
| LP row: "investor in the LLC" | accredited investor / qualified purchaser |
| small notes about the risk gate | the deterministic gate + reason codes as the differentiator |
| nothing anywhere | the tamper-evident audit chain |
| nothing anywhere | the six-agent desk as **the mechanism** that activates a watchlist |

The single biggest gap: there is **no navigational sentence** on the surface. The closest
is the Risk-of-Ruin line, which is about survival, not navigation. A visitor learns what
Emporion refuses to do before they learn what it does for them.

## 6. Roadmap fence — build 2.0, prep only

**[2.0], explicitly not in this build:**

- Automated execution end to end, with a user-held kill switch and configurable
  notification cadence.
- User-configurable desks on top of the research layer.
- Real market-data adapters (licensed feeds) replacing synthetic fixtures.
- Durable membership via Supabase, social providers enabled in production.
- Securities counsel sign-off before any live LP capital or order execution.

Nothing in section 6 is claimed by the current build, and the site must not imply it.

## 7. Demo path

    bash scripts/biz_prep.sh              # build, start the server, print this pack

    http://127.0.0.1:8765                 # full functionality, incl. sign-in + GP console

Demo order that shows the most: the eight tabs, then sign in (the code prints to the
terminal), then the GP console, then Research desks → open a desk → engine detail →
Write Yellow Sheet, then Yellow Sheets → save with the closeout fields.

**The public URL is not yet the same experience:** `SMTP_*` and `GP_EMAIL` are unset on
Render, so sign-in codes reach only the service log and the operator console depends on
that address. That is the `render login` item.
