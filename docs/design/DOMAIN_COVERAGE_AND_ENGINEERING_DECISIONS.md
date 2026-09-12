# Domain coverage and engineering decisions

Derived from the licensing domain outlines (Series 7 General Securities Representative;
Series 3 National Commodity Futures) studied against this codebase. Sources cited are the
**public** rule numbers and the published exam-domain structure; no licensed study text is
reproduced here, and no licensed material is committed to this repository.

Purpose: let the domain decide the design. Where a domain is heavy, the engineering is
heavy; where a domain is an edge case, the code should say so rather than pretend.

## 1. What the domain weighting tells us

Series 7 breaks into four job functions, and the weights are decisive:

| Job function | Weight | What it implies for this product |
|---|---|---|
| F1 Open accounts; evaluate financial profile and objectives | 9% | Suitability capture must exist before research output means anything |
| **F2 Provide information, make suitable recommendations, maintain records** | **73%** | **This is the product's spine: recommendation support + records** |
| F3 Obtain/verify instructions; process, complete, confirm transactions | 11% | Order handling is *not* the centre of gravity — consistent with paper-only today |
| F4 Seek business; communications with the public | 7% | Marketing claim discipline is a regulated surface, not a nicety |

Decision taken: Emporion stays weighted to F2. Candidate intake → desk research → scenario
stress → Yellow Sheet (with explicit invalidation) → deterministic survival gate → human
review is a **recommendation-support and records** pipeline. That is a deliberate match to
where the regulation actually spends its weight, and it is why the product is not built
around order entry.

## 2. Option valuation and premium selling — the biggest gap

The domain covers basic options including the role of the clearing corporation, **option
valuation**, and basic option strategies. The engine today has:

    options/spreads.py      executable-side economics for defined-risk vertical credit spreads
    options/scanner.py      deterministic vertical-spread enumeration
    options/exit_policy.py  executable paper exit monitoring
    options/universe.py     contract universe, cadence, session, events

That is the *structure* of premium selling — executable prices, defined risk, exits
monitored. What is missing is the **valuation layer** the domain treats as basic:

- intrinsic vs extrinsic value; moneyness
- breakeven, max profit, max loss per structure
- **collateral and margin requirement per strategy** (cash-secured put collateral;
  Reg T initial and maintenance margin for spreads)
- early assignment and pin risk
- theta/vega sensitivities in plain, deterministic terms

Engineering decision: implement these as **pure, deterministic, unit-tested functions**
over `Decimal`, matching the existing `spreads.py` style. No model license needed, no
prediction — valuation and requirement arithmetic is the basic-concept layer, and it is the
difference between "a spread" and "a premium sale the desk can defend".

## 3. Bonds, rates, and futures — the two thin desks

- **Bonds & Rates** is architecture-only. The domain's debt material is dense: money market
  instruments, bond **yields**, ratings, corporate bond types, priority in dissolution,
  convertibles, taxation, municipals, and the **price-yield relationship**. For a rates desk
  the load-bearing primitives are: price↔yield, duration and convexity, credit spread,
  curve shape, and liquidity stress.
- **Futures Event** (Series 3 domain): futures **basis**, intra- and inter-market **spreads**,
  processing spreads, hedging vs speculation, interest-rate futures, stock-index and
  single-stock futures, order types and processing, clearing, margin regulation, settlement
  and delivery.

Engineering decision: add deterministic **basis** and **spread** primitives plus a
**price-yield/duration** primitive. These are closed-form, testable, and they are what makes
the two thin desks publishable rather than decorative. Do not invent a signal where the
domain says the primitive is arithmetic.

## 4. Records, supervision, and public communication

| Domain area | Existing control | Engineering decision |
|---|---|---|
| Maintain appropriate records (F2) | append-only hash-chained membership audit | Extend the trail from membership events to **research and approval events**: who cleared a gate, who reviewed, when, with what inputs |
| Supervisory review and principal approval | GP console issues LP invites | Record **approvals as first-class audited actions**, not just state changes |
| Communications with the public (Unit 19; FINRA Rule 2210) | `tests/test_public_claims.py` claim guard | Keep claim discipline executable; add review/approval provenance for anything product-specific |
| Risk disclosures (Unit 14) | paper-only notices | Make disclosures a **surface**, not a footnote, and version them |
| Senior exploitation rules | none | Out of scope for this build; noted as a required control before real money |
| Complaint resolution (Unit 18) | none | Out of scope for this build; a retail product needs a complaint path |

## 5. Queued engineering actions

1. **Option valuation primitives** — intrinsic/extrinsic, breakeven, max profit/loss,
   assignment/pin risk. Pure functions, Decimal, tested.
2. **Collateral and margin model per strategy** — cash-secured put, covered call, credit
   spread; Reg T initial/maintenance as data, not magic numbers.
3. **Basis and spread primitives** for the futures desk; **price-yield and duration** for
   the rates desk.
4. **Audit coverage** — research and approval events join the hash chain.
5. **Disclosures surface** — versioned, visible, and part of the shipped surface (the claim
   guard already covers the language).

Each of these is deterministic and testable; none requires predicting the market, and none
crosses the paper-only boundary.
