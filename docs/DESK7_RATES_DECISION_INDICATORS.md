# Desk 7 — Core Indicators for the Fed Rate Decision (Consolidated)

**Status:** Consolidated deliverable, Fri 2026-11-13. Replaces the 30-line v1.0 framework (`desk7-rates-decision-indicators.md`, retained as raw material, not overwritten). Numbers from the 2026-11-13 snapshot pulls (~08:35–08:45 PT) unless noted. Labels: FACT = primary source + as-of; INFERENCE = stated logic from FACTs; UNVERIFIED = looked, could not confirm.

**Grounding:** CFA evidence discipline (diligence, reasonable basis, documented record, verdict as thesis / evidence / what would change it) per the `cfa-financial-analysis` skill; broker discipline (reasonable basis, mandate fit, fair-and-balanced presentation including disconfirming evidence) per the repo's derived Series 7 domain notes (`docs/design/DOMAIN_COVERAGE_AND_ENGINEERING_DECISIONS.md`, `docs/compliance/FINRA_ENGINEERING_MAP.md`). No LEM manual text was available to cite — the manual is cataloged as a reference identity only, encrypted and copyrighted, with no readable copy in the workspace. No rule numbers, quotes, or licensed text are reproduced. No license is claimed; this is decision support, not a recommendation.

## 1. The decision

The FOMC meets Dec 8–9 with the target range at 3.75–4.00% after a 10–2 October hold in which Cook and Hammack dissented for an immediate hike. The call is a 25bp hike on Dec 9: core PCE, the variable the 2% target is defined on, runs 3.12% y/y; the labor market shows no deterioration on any kept read; growth runs above trend; and Kalshi prices a hike at $1.00 combined ($0.88 for 25bp, $0.12 for more, pulled 12:00 PT). The distilled tally is 5 HIKE / 1 CUT / 4 NEUTRAL across the 10 core indicators below. Confidence is high on direction — indicators and markets agree — and lower on size: the 50bp tail repriced from $0.05 this morning to $0.12, and no indicator rule distinguishes 25bp from 50bp. November CPI lands Dec 10 (date single-basis), after the decision, so it cannot change December. (INFERENCE from the FACTs below; the decision belongs to the Committee.)

## 2. Core indicators

| Indicator | Why the Fed watches it | Trigger rule | Today's read | Broker POV |
|---|---|---|---|---|
| Core PCE price index (PCEPILFE, BEA) | The 2% target is defined on this series; nothing outranks it. | HIKE if y/y > 2.5% or m/m > +0.25%; CUT if y/y < 2.2%. | y/y +3.121%, m/m +0.317% (130.902, Sep 2026; FRED). HIKE. | Anchor the discount rate to the higher regime. Do not re-anchor on a soft CPI print — the decision variable is PCE, and the next PCE print (Nov 25, date provisional) is the re-anchor date. |
| Breakeven expectations (T5YIE / T10YIE, FRED) | Expectations feed wage and price setting; anchored expectations give the Fed room. | HIKE if > 2.75%; CUT if < 1.75%; NEUTRAL 2.0–2.5%. | 2.31% / 2.24% (Nov 12). NEUTRAL. | Anchored market expectations mean no credibility crisis in the bond market: room for 25bp, not a forced 50bp. The tripwire is a break above 2.75%. |
| Michigan expectations (MICH, U-M) | Household expectations feed wage demands directly and respond to prices households see. | HIKE if yr-ahead > 3.5%; CUT if < 2.5%. | 4.3% yr-ahead, Nov prelim (Oct 4.7%), rel. Nov 6. HIKE. | Do not average this with breakevens: 4.3% against 2.24% is a credibility gap the Fed reads as pressure to act. The fall from 4.7% narrows the gap; the level still fires the trigger. |
| Payrolls, 3-mo avg (PAYEMS, BLS) | The direct count of job creation; the employment half of the mandate. | HIKE if 3-mo avg > +150k; CUT if < +50k. | 3-mo avg +137k; Oct +165k (Oct 2026; FRED). NEUTRAL. | Apply the rule as written: NEUTRAL. The single +165k print does not override the average — one print is noise, the average is the signal, and cherry-picking the strong print fails the reasonable-basis standard. |
| Initial claims, 4-wk avg (ICSA, DOL) | The fastest labor signal; claims rise before payrolls fall. | CUT if 4-wk avg > 300k; NEUTRAL < 250k. | 200k w/e Nov 7; 4-wk avg 195,250 (FRED). NEUTRAL. | No action on this read. Check it every Thursday: it turns first, and a 4-week average above 300k flips the labor read to CUT before payrolls confirm. |
| Job openings (JTSJOL, BLS) | Openings measure labor demand; the openings-to-unemployed ratio is the tightness gauge the Fed has cited. | HIKE if 3-mo change positive; CUT if −500k over 3 months. | 7,523k, Sep 2026 (Jul 7,335k, Aug 7,190k; FRED). HIKE. | Demand has not rolled over: this rules out the "labor is cracking" case for a hold. It corroborates payrolls — filled jobs plus unfilled demand — rather than replacing them. |
| Real GDP (GDPC1, BEA) | Growth above trend with inflation above target means the economy can absorb tighter policy. | HIKE if > 2.5% annualized; CUT if < 1.0%. | Q3 +3.37% annualized (Q2 +2.22%; FRED). HIKE. | Above-trend growth removes the "restraint is biting" objection to a hike. Growth is the backdrop, not the trigger — the prints that can move the call before Dec 9 are PCE, claims, and the minutes (§4). |
| Housing starts (HOUST, Census) | The most rate-sensitive sector; the first place transmission shows up. | CUT if −5% over 3 months; HIKE if rising through high rates. | 1,221k; −10.8% Jul→Sep (Sep 2026; FRED). CUT. | Report it, don't bury it: this is the evidence a hold argument would cite, and it is why the call is 25bp, not 50bp. A view that omits its strongest counter-evidence fails the fair-and-balanced standard. |
| High-yield OAS (BAMLH0A0HYM2, ICE BofA via FRED) | The price of credit risk; widening spreads mean conditions tightening on their own. | CUT if > 5.00%; NEUTRAL < 4.00%. | 3.20% (Nov 12). NEUTRAL. | No stress: the market is neither doing the Fed's tightening work nor forcing an easing response. No defensive action on credit; the watch is a break above 5.00%. |
| FOMC vote & guidance (federalreserve.gov) | The Committee speaking for itself outranks any data print. | HIKE if dissents favor tightening or statement language turns hawkish; CUT if the reverse. | Oct 28: held 3.75–4.00%, 10–2, Cook + Hammack dissenting for +25bp; statement: "Inflation remains elevated." 7 hawkish / 0 dovish named statements this week (INFERENCE, single-basis press reports). HIKE. | Weight the vote above any single print: two dissents for an immediate hike plus that sentence is the Committee stating its lean. The Nov 18 minutes are the check on whether 10–2 understates division. |

## 3. Market pricing vs indicators

Kalshi, direct API pull Nov 13, 12:00 PT (Dec-2026 meeting, `KXFEDDECISION`): 25bp hike $0.88 (bid/ask 0.87/0.88, prev 0.86), more than 25bp $0.12 (0.11/0.12, prev 0.11), hold $0.03, cuts $0.01 each; the five lasts sum to $1.05 (5-cent over-round). Total hike $1.00. CME FedWatch could not be read directly (embedded app, no public text API); secondhand reads Nov 10–13 converge at 87–91% for 25bp and 9–15% for 50bp. This morning Kalshi's tail ($0.05) sat below the FedWatch range; it has since repriced to $0.12, inside it — the two markets now agree on direction and tail. The remaining disagreement is between the markets and the indicators: the indicator set votes direction (hike), not size, and no rule in it distinguishes 25bp from 50bp. The tail repriced intraday, after this morning's PPI release (+0.3% m/m reported, y/y +6.5%, BLS USDL 26-1687); no kept indicator printed new data in that window, so the size repricing is market-driven, not data-driven. (INFERENCE from the sequence.)

## 4. What would change the call

- October core PCE (Nov 25; date single-basis, provisional): m/m at or below +0.15% with a downward revision to September — the target variable softening.
- Initial claims 4-week average above 300k — the fast labor signal turning before payrolls confirm.
- November 18 minutes, or a named speaker arguing for a hold, showing the Committee more worried about overtightening than the 10–2 vote suggested — guidance shifting against the hike.

## 5. Graham lens

The 10-year yield (FRED DGS10) rose 4.86% (Nov 6) → 4.98% (Nov 10). At assumed perpetual growth g = 3.00%, the Gordon multiple 1 ÷ (r − g) falls 53.76x → 50.51x, −6.06% — arithmetic, not opinion.
That is a multiple change: Mr. Market repricing the same earnings stream at a higher discount rate. Earnings power did not change on any data in this session's pulls.
Duration ≈ 8 puts the same +12bp move at about −0.96% on a 10-year position (approximation; ignores convexity).
The margin of safety is thinner at the same prices: any intrinsic-value estimate carried at the old 4.86% anchor overstates value by ~6% on this sensitivity. Re-anchor to 4.98%.
Earnings-yield vs bond-yield spread: UNVERIFIED. Bond side verified (4.98%); earnings side unverified from any primary source this session (Shiller download failed; no S&P Dow Jones figure). No live spread is asserted.
The defensive read: the bond side pays ~5% on a contractual claim, so equity risk must be compensated from price — a wider required discount, not a chase for yield.

## 6. What was cut

Cut 19 of the 30 v1.0 lines as duplicative or triggerless: DFF, target range, IORB, ON RRP, balance sheet, headline CPI, core CPI, PPI, core PPI, median CPI, unemployment rate, unit labor costs, industrial production, retail sales, CFNAI, permits, 2s10s, 10s3m, IG spread. Market pricing was not cut — it moved to §3.
