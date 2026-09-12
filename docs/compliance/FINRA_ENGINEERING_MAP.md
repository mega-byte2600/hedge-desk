# FINRA / SEC engineering map

**Status of my credentials, stated plainly: I hold none.** I am not a registered
representative, I have not sat the SIE, Series 7, or Series 4, and no exam score exists
to report. Those exams require a human candidate with a CRD record — fingerprinting, a
Form U4 filed by a sponsoring member firm, and a proctored test session with photo ID.
Claiming a pass would be a fabrication, and holding out as registered without
registration is a securities-law problem rather than a paperwork one.

What follows is the honest, useful version: the published rule content studied and turned
into engineering requirements for this product. **This is a requirements map, not legal
advice.** Anything that depends on registration, supervision, or a broker-dealer
relationship needs securities counsel; it cannot be satisfied by software alone.

## The exams, and what each implies for software

| Exam | What it qualifies a human to do | Why it matters to this product |
|---|---|---|
| **SIE** — Securities Industry Essentials | The baseline knowledge exam, no sponsorship needed to sit it | Sets the vocabulary: products, trading, regulatory framework |
| **Series 7** — General Securities Representative | Sell all securities products except commodities/futures | What a person would need to be doing anything *for a client* that resembles a recommendation |
| **Series 4** — Registered Options Principal | Supervise options activity as a principal | Principal approval and supervisory review — the pattern behind any "independent review before action" control |

The Series 4 pattern is the one this product most resembles internally: a **principal must
review and approve** before certain activity proceeds. Emporion already encodes that shape
(the deterministic risk gate plus human review cannot be overridden by an agent or a
narrative). It is a design pattern, not a licence.

## Rules that bear on what this codebase does

| Rule | What it requires | Where Emporion stands | Engineering action |
|---|---|---|---|
| **SEC Rule 15c3-5** — Market Access Rule | A broker-dealer *with market access* must maintain risk-management controls and supervisory procedures; FINRA describes **kill switches** as part of that for highly automated firms | No market access, so the rule does not apply to us. The **user-held kill switch** is a product control built in the spirit of it. Execution is not implemented | Keep the kill-switch concept as a 2.0 feature; never describe it as compliance |
| **FINRA Rule 2210** — Communications with the Public | Retail communications must be fair, balanced, not misleading; principal approval and recordkeeping for many categories | Public copy is deliberately capability-framed; claim discipline is documented in `docs/EMPORION_MARKETING_CLAIM_AUDIT.md` | **Implemented as a test**: `tests/test_public_claims.py` scans the built surface for prohibited/unsupportable claim patterns and run CI fails on a regression |
| **FINRA Rule 3110** — Supervision | Designate and record supervisors; retain the record at least 3 years, first 2 easily accessible | The GP console is the supervisory surface (roster, seats, invites); the tamper-evident audit trail records membership events | Extend the audit trail to cover every supervisory action, and record who holds the supervisor role and when it changed |
| **SEC Rule 17a-4** — Books and Records | Preserve electronic records in a non-rewriteable, non-erasable format, indexed and accessible to regulators (amended 2022 for electronic records) | The membership audit log is append-only and hash-chained, which is the right *shape*; it is not WORM storage, has no retention schedule, and only covers membership events | 2.0: retention policy, WORM/immutable storage, export for a regulator, and coverage of every record class the business actually relies on |
| **SEC Regulation D, Rule 501** — Accredited Investor | Defines who may hold unregistered offerings | Tier model names it; no verification is implemented | If LPs are ever onboarded through software, verification is a control that must exist before capital moves |
| **Investment Company Act Sec. 2(a)(51)** — Qualified Purchaser | $5M+ in investments; the test for private-fund investors | Named in the positioning only | Counsel question: which test the LLC relies on, and what evidence is retained |
| **Regulation Best Interest / suitability** | If a recommendation is made, the standard attaches to a broker-dealer or investment adviser | Emporion is research and decision support; it does not recommend and places no orders | If the product ever nudges toward a specific action for a client, this becomes live and needs counsel first |

## The two things software cannot do for us

1. **Registration.** No amount of code makes a person a registered representative or a firm
   a member. That path is a CRD record, a sponsoring firm, exams, and ongoing CE.
2. **Compliance claims.** Rule 15c3-5 obligations attach to a broker-dealer with market
   access. We may build the control; we may not describe it as compliance. The public
   surface must never imply registered status, examination passes, or regulatory approval.

## How this knowledge is applied to development

Written down so it is applied rather than admired:

- **Supervisory actions are recorded, not just performed.** Any GP action that changes a
  member's status appends to the audit trail with actor and reason (Rule 3110 shape).
- **Every public claim is testable.** Prohibited-pattern scanning runs in CI, so a claim
  that drifts into "guaranteed", "insured", "SEC-approved", or "registered" fails a run
  rather than reaching a visitor (Rule 2210 direction).
- **Controls fail closed.** The risk gate, the tier gate, and the read-only broker boundary
  deny by default; an unknown role gets the most restrictive tier.
- **The kill switch stays the user's.** Automation is bounded by a control the client holds.
- **Nothing is claimed as live that is not exercised.** Every "verified" statement names
  the command that measured it; see `docs/CONSOLE_VV_SPEC.md`.
