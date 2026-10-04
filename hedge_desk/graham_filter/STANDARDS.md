# Graham Filter — Standards: Graham-sourced proposals, NOT user-approved

Every number in `Standards` is a judgment call, not a fact. On 2026-10-04 the
user delegated the first real pass on these values to Toby with one hard
rule: **no invented numbers** — every value must be anchored in Benjamin
Graham's published criteria (The Intelligent Investor / Security Analysis),
with chapter-level provenance. Where Graham states a principle but no number,
the value is marked **INTERPRETED** and the reasoning is shown; an
interpretation is never presented as Graham's own words.

**None of the values below are user-approved.** They live in
`PROPOSED_STANDARDS` (label `"PROPOSED — Toby, pending user approval"`) with
per-field provenance in `PROVENANCE`. The engine refuses to run without an
explicit `Standards` instance — there is no production default. The UI must
badge these as proposed, exactly as it badged the prototype.

## Provenance table

| # | Field | Value | Source | Interpreted? | Reasoning (one line) | What would change it |
|---|-------|-------|--------|--------------|----------------------|----------------------|
| 1 | `margin_strong` | 33.0 | Intelligent Investor, Ch. 15 — net-net rule: buy at ≤ 2/3 of net current asset value (a one-third discount), Graham's canonical "decisive" margin of safety | Yes | Graham never rated put-strike cushions; 33% maps his only hard numerical margin-of-safety rule onto total cushion % | User defines their own cushion bands, or picks a different Graham anchor |
| 2 | `margin_adequate` | 20.0 | Intelligent Investor, Ch. 20 (margin-of-safety principle); no direct Graham number for an "adequate" band | Yes | Between the net-net anchor (33) and the thin floor (10): absorbs a one-fifth adverse move — passing but not decisive | User defines their own bands |
| 3 | `margin_thin` | 10.0 | Intelligent Investor, Ch. 1 (investment requires safety of principal) and Ch. 20; no direct Graham number for a "thin" band | Yes | Double-digit minimum: absorbs a 10% adverse move before capital impairment; below this there is no safety of principal at all | User defines their own floor |
| 4 | `manic_vix` | 30.0 | Intelligent Investor, Ch. 8 (Mr. Market: manic-depressive markets). The VIX did not exist in Graham's lifetime (created 1993); 30 is the market-convention fear threshold (~1.5× the ~19–20 long-run average) | Yes | Ch. 8 gives the principle but no number; 30 operationalizes "manic" with the standard practitioner fear line | User picks a different fear threshold or gauge |
| 5 | `complacent_vix` | 14.0 | Intelligent Investor, Ch. 8 (Mr. Market); VIX below ~14 sits in the index's historical low zone — the practitioner read of complacency | Yes | Mirror of `manic_vix`: Ch. 8's complacent pole, quantified at the VIX's historical low zone | User picks a different complacency line |
| 6 | `manic_margin_bump` | 5.0 | Intelligent Investor, Ch. 20 — the margin of safety must be larger when the future is less certain | Yes | 5 points = half the thin floor: a material, not prohibitive, extra cushion when Mr. Market is manic | User judgment on how much extra cushion fear markets must pay |
| 7 | `default_hurdle` | 12.0 | Intelligent Investor, Ch. 11 — valuation formula Value = EPS × (8.5 + 2g): 8.5 is Graham's no-growth P/E → 1/8.5 = 11.8% required earnings yield for a no-growth business | Yes | A cash-secured put is a no-growth income operation; Graham's no-growth baseline demands ~12% yield (rounded). Consistent with Ch. 5's bond thinking | User sets their own definition of "adequate return" |
| 8 | `per_symbol_hurdles` | {} (empty) | No Graham source exists — Graham never set per-ticker return hurdles | Yes | Deliberately empty: every symbol falls back to `default_hurdle` uniformly. Inventing per-ticker bars would be invention | User assigns per-name hurdles |

**Nothing was left UNSET**: all eight fields have values, and all eight are
marked interpreted — there is no Graham-published number for any of these
exact thresholds (he never rated put cushions, never saw the VIX, never set
per-ticker hurdles). The anchors above are the closest published Graham
criteria for each.

## Honest behavioral consequence

Graham's margins were **large**. Under these bands, a typical 30-DTE
cash-secured put (a few % price cushion + ~1–3% premium) rates **NONE** →
**SPECULATION**, because a 3–6% cushion is, in Graham's terms, no margin of
safety at all. The desk will therefore show mostly SPECULATION / NEEDS-YOU
until the user sets their own (tighter) bands for short-dated premium. That
is the honest Graham answer, not a bug — but the user should know the filter
is strict by design at these values.

## Structural decisions also needing approval

- **Verdict precedence** (engine.py docstring): the ordering data-unavailable →
  own-it-no → margin-none → own-it-unset → inadequate-return → investment.
  Reordering changes what the desk shows; do not reorder silently.
- **Inadequate return = NEEDS-YOU, not SPECULATION.** Deliberate: a below-hurdle
  return is a judgment call for the human, not evidence of speculation.
- **Margin NONE = SPECULATION.** Complete absence of safety is speculation per
  Graham Ch. 1, even with own-it = Yes.
- **VIX is context only.** It moves the margin bar; it never overrides a test
  and never generates a signal.
- **Annualization uses 365/DTE simple scaling** (no compounding). If the desk
  wants effective-annual or continuous compounding, that is a methodology change.

## How to approve

Replace `PROPOSED_STANDARDS` usage with a real instance, e.g.:

```python
from engine import Standards
USER_STANDARDS = Standards(
    margin_strong=..., margin_adequate=..., margin_thin=...,
    manic_vix=..., complacent_vix=..., manic_margin_bump=...,
    default_hurdle=..., per_symbol_hurdles={...},
    label="user-approved 2026-10-__",
)
```

Then pass `standards_approved=True` with that label in `contract.to_dict` /
`to_batch` so the UI stops badging the standards as unapproved.
