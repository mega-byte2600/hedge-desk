# Graham Filter — Standards Needing User Approval

Every number in `Standards` is a judgment call, not a fact. **None of the
values below are user-approved.** They are the first prototype's placeholders,
kept in `PROTOTYPE_STANDARDS` (explicitly labeled `"PROTOTYPE — UNAPPROVED"`).
The engine refuses to run without an explicit `Standards` instance — there is
no production default, because any default would be an invented hurdle.

## Threshold inventory

| # | Field | Meaning | Prototype value | What approval decides |
|---|-------|---------|-----------------|----------------------|
| 1 | `margin_strong` | Total margin % at/above which a candidate is rated STRONG | 5.0 | How much cushion counts as a decisive margin of safety |
| 2 | `margin_adequate` | Total margin % at/above which a candidate is rated ADEQUATE | 2.0 | The minimum cushion for a passing margin |
| 3 | `margin_thin` | Total margin % at/above which a candidate is rated THIN (else NONE → SPECULATION) | 0.5 | The line between "thin but real" and "no safety at all" |
| 4 | `manic_vix` | VIX above this = MANIC regime | 30.0 | What counts as fear-driven markets |
| 5 | `complacent_vix` | VIX below this = COMPLACENT regime | 14.0 | What counts as complacent markets |
| 6 | `manic_margin_bump` | Extra margin % demanded when MANIC | 2.0 | How much more cushion fear markets must offer |
| 7 | `default_hurdle` | Annualized return % required when no per-symbol hurdle exists | 15.0 | The bar for "adequate return" on an unlisted symbol |
| 8 | `per_symbol_hurdles` | Per-ticker annualized hurdles | SPY 15, QQQ 15, AAPL 20, TSLA 25, NVDA 22, MSFT 18 | Whether different names deserve different bars, and what they are |

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

Replace `PROTOTYPE_STANDARDS` usage with a real instance, e.g.:

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
