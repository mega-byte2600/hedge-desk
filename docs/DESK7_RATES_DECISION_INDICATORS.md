# Desk 7 (Bonds & Rates) — Rates-Decision Indicator Framework

**Question:** Which core/key indicators inform whether the Fed raises or cuts rates, and what do they read right now?

**Role:** This framework is written from the desk's standing lens — the value investor in the Benjamin Graham tradition, working with the CFA analyst's evidence discipline and the Series 7 broker's recommendation discipline. Rates enter this framework in exactly one primary way: as the discount rate in intrinsic-value estimation. Everything else — the curve, the spreads, the Fed's own words — is context for that one input and for the margin of safety the desk requires before anything is attractive.

**Status:** Framework v1.0, built Fri 2026-11-13. Extends the existing Desk 7 part file (levels + slope + funding from `hedge_desk.rates_desk`); it does not replace it. The live snapshot that pairs with this framework is `2026-11-13-desk7-rates-snapshot.md`. The interactive dashboard prototype is `desk7-rates-dashboard.html`.

**Grounding rule:** Series 7 and CFA concepts below are stated in original wording from public knowledge of the exam and curriculum domains (Federal Reserve tools and policy mechanics, economic indicators, yield-curve theories, bond pricing, monetary transmission, inflation expectations, term premium, the neutral rate). No licensed manual or curriculum text is reproduced. Public sources are named: federalreserve.gov, fred.stlouisfed.org, bls.gov, bea.gov, cme.com, finra.org, cfainstitute.org. Where a claim rests on a source, the source and as-of date are given. Where a claim cannot be verified, it is labeled UNVERIFIED.

**Evidence labels (every material claim carries one):** FACT (verifiable from a primary source right now, with source + as-of), INFERENCE (follows from stated facts by stated logic), SPECULATION (a scenario without grounding — labeled, never the basis of a conclusion), UNVERIFIED (looked and could not confirm, or have not looked). A reasoning chain is only as strong as its weakest label. No synthetic data ever; a missing value reads "data unavailable," never an estimate.

---

## 1. The decision this framework serves

The desk is a value desk. Its question about rates is not "which way will rates go next?" but "what discount rate should intrinsic-value estimates carry, and how wide a margin of safety does the current rate environment demand?" (INFERENCE — follows from the desk's stated value-investing lens and the repo's method stack, which names Graham/Buffett/Burry/Shiller as the valuation layer.)

Three consequences follow, and they organize everything below:

1. **The discount rate is the transmission belt.** A higher long rate lowers the present value of every future cash flow mechanically, through arithmetic, not through opinion. The Gordon-style sensitivity in §5 shows the size of that effect with live numbers. When the 10-year yield moves, intrinsic values move — even when the businesses themselves have not changed at all.
2. **Margin of safety is the decision variable.** A rate rise does not make the desk "bearish." It lowers intrinsic value, which means the same market price now carries a thinner margin of safety, which means a wider discount is required before anything is attractive. Rate moves change the required discount; they are never momentum signals and never a reason to chase yield.
3. **Mr. Market moves multiples; businesses move earnings power.** A rate-driven multiple change is market mood repricing the same earnings stream. It is not a change in the earnings power of the business. Every snapshot must separate the two explicitly and say which one moved. (Graham's Mr. Market concept, stated in original words.)

The Fed's decision matters to the desk because the policy rate anchors the front end of the curve, the front end anchors the whole curve through expectations and term premium, and the curve anchors the discount rate. The indicators below are the evidence chain from the Fed's mandate to the desk's discount rate.

---

## 2. Indicator framework, group by group

Each indicator carries: what it measures, why the Fed watches it, source + FRED series ID, release cadence, and the rise/cut read rule. Read rules are trigger rules, not predictions: they state what direction of reading argues for a hike versus a cut, so that any run can score the tally transparently. Thresholds are stated as triggers, not forecasts.

### Group 1 — Policy stance: where policy is right now

**DFF — Effective federal funds rate.** What it measures: the volume-weighted median rate on overnight loans of reserves between banks, computed daily by the New York Fed. Why the Fed watches it: it is the rate policy is actually steering; the target range is the instruction, DFF is the result. Source: FRED `DFF` (Board of Governors / NY Fed). Cadence: daily, one-day lag. Read rule: DFF persistently at the top of the target range argues the stance is tight relative to intent (no hike signal by itself); DFF persistently below the range argues implementation is loose. Scored NEUTRAL unless DFF sits outside the range, which is an implementation event, not a policy signal.

**DFEDTARL / DFEDTARU — Target range, lower and upper bound.** What they measure: the FOMC's announced target range for the federal funds rate. Why the Fed watches it: it is the policy decision itself. Source: FRED `DFEDTARL`, `DFEDTARU`. Cadence: daily; changes only on FOMC decision days. Read rule: the range is the stance, not a signal — scored NEUTRAL in every tally. Its level matters for the discount-rate floor, not for the hike/cut direction.

**IORB — Interest on reserve balances.** What it measures: the rate the Fed pays banks on reserves held at the Fed. (The older series `IOER` was discontinued in 2021; `IORB` is the live series. Any framework citing IOER as current is stale.) Why the Fed watches it: it is the primary tool that steers overnight rates — banks will not lend reserves below what the Fed pays them, so IORB sets a floor under money-market rates. Source: FRED `IORB`. Cadence: daily. Read rule: IORB at its normal position (10bp below the top of the range) is NEUTRAL; a change in IORB outside a meeting is an implementation event.

**RRPONTSYD — Overnight reverse repo facility usage.** What it measures: how much cash counterparties park at the Fed overnight in exchange for Treasury collateral. Why the Fed watches it: heavy usage means cash is abundant relative to the supply of short-term government paper; near-zero usage means the facility has drained and reserves are the binding margin. Source: FRED `RRPONTSYD` (billions of dollars). Cadence: daily. Read rule: usage near zero is NEUTRAL (the facility is no longer absorbing liquidity); a rapid rebuild argues liquidity is ample (no tightening signal); a spike during stress argues funding dislocation (a cut-side risk, scored only with corroborating funding spreads).

**WALCL — Federal Reserve balance sheet (total assets).** What it measures: the size of the Fed's securities holdings — the stock of past asset purchases minus runoff. Why the Fed watches it: the balance sheet is the second policy tool alongside the rate; runoff (quantitative tightening) withdraws reserves, purchases add them. Source: FRED `WALCL` (millions of dollars, weekly). Cadence: weekly (Wednesday, H.4.1). Read rule: a flat balance sheet is NEUTRAL; sustained runoff argues the stance is tightening on the quantity margin (hike-side context, not a rate signal by itself); renewed growth argues easing on the quantity margin (cut-side context).

### Group 2 — Inflation: the mandate's price-stability half

The Fed's stated goal is 2% inflation measured by the 12-month change in the personal consumption expenditures price index (FACT — federalreserve.gov, monetary policy framework). Every inflation indicator below is read against that 2% anchor. The monthly pace consistent with 2% annualized is about 0.17% per month (2 ÷ 12 = 0.167, simple division, stated as arithmetic not a forecast).

**CPIAUCSL — Consumer Price Index, all items.** What it measures: the average change in prices paid by urban consumers for a fixed basket. Why the Fed watches it: it is the most widely followed inflation gauge, it moves expectations, and persistent upside surprises force the Committee to defend the target. Source: FRED `CPIAUCSL` (BLS, seasonally adjusted). Cadence: monthly, mid-month. Read rule: headline m/m above +0.25% (a 3% annualized pace) argues HIKE; m/m below +0.10% argues CUT; between is NEUTRAL. The 12-month rate above 3% argues HIKE; below 2.5% argues CUT.

**CPILFESL — Core CPI (all items less food and energy).** What it measures: the CPI basket excluding the two most volatile components, to reveal the underlying trend. Why the Fed watches it: food and energy prices swing on supply shocks the Fed cannot control; the core trend is the better guide to where inflation is heading. Source: FRED `CPILFESL` (BLS, seasonally adjusted). Cadence: monthly. Read rule: same thresholds as headline CPI. Three consecutive core prints at or above +0.3% m/m is a HIKE trigger (a 3.7% annualized core pace).

**PCEPILFE — Core PCE price index.** What it measures: the Fed's target variable — the price index for personal consumption expenditures excluding food and energy, computed by the BEA with a broader basket and different weights than the CPI (notably a larger housing-services treatment difference and chain weighting). Why the Fed watches it: it is the variable the 2% target is defined on. Nothing else in this group outranks it. Source: FRED `PCEPILFE` (BEA). Cadence: monthly, late month. Read rule: 12-month core PCE above 2.5% argues HIKE; below 2.2% argues CUT; m/m above +0.25% argues HIKE. A core PCE print is the single highest-weight inflation input in the tally.

**PPIFIS / PPIACO — Producer Price Index, final demand / all commodities.** What they measure: prices received by domestic producers — the pipeline that feeds consumer prices with a lag. Why the Fed watches them: producer-price pressure today is consumer-price pressure tomorrow; a hot PPI warns the pipeline is still full. Source: FRED `PPIFIS` (BLS, final demand, seasonally adjusted) and `PPIACO` (all commodities, not seasonally adjusted). Cadence: monthly. Read rule: final-demand m/m above +0.3% argues HIKE; the 12-month rate above 4% argues HIKE. The core PPI variant (final demand less foods, energy, and trade services, from the BLS release text) above +0.3% m/m argues HIKE.

**CPIMEDSL — Median CPI.** What it measures: the median price change across CPI components — the middle of the distribution, so a few extreme movers cannot dominate it. Why the Fed watches it: it answers "is inflation broad or narrow?" Broad inflation (a high median) is harder to dismiss as transitory than a headline driven by one sector. Source: FRED `CPIMEDSL` (Federal Reserve Bank of Cleveland, via BLS data). Cadence: monthly. Read rule: median m/m above +0.25% argues HIKE (broad-based pressure); below +0.15% argues CUT.

**T5YIE / T10YIE — Breakeven inflation expectations (5-year / 10-year).** What they measure: the difference between nominal Treasury yields and inflation-protected (TIPS) yields of the same maturity — the market's priced-in average inflation rate over that horizon, plus an inflation risk premium and a liquidity difference. Why the Fed watches them: expectations are self-fulfilling — if the market expects inflation, wage and price setting follows. Anchored expectations near 2% give the Fed room; drifting expectations force action. Source: FRED `T5YIE`, `T10YIE`. Cadence: daily. Read rule: breakevens inside 2.0–2.5% are NEUTRAL (anchored); above 2.75% argues HIKE (de-anchoring); below 1.75% argues CUT. Read against the survey measure below — a market/survey disagreement is itself information (see §6 cross-checks).

**MICH — University of Michigan inflation expectations.** What it measures: the median inflation rate households expect over the next 12 months, from the Surveys of Consumers. Why the Fed watches it: household expectations feed wage demands and spending behavior directly, and they respond to the prices households actually see (food, fuel) rather than to bond-market arithmetic. Source: FRED `MICH` (University of Michigan). Cadence: monthly (preliminary mid-month, final late month). Read rule: year-ahead expectations above 3.5% argue HIKE (unanchored household expectations); 2.5–3.5% NEUTRAL; below 2.5% CUT. Direction matters secondarily: a falling print from a high level softens but does not erase a HIKE read until the level clears the threshold.

### Group 3 — Labor: the mandate's employment half

The Fed's other mandate half is maximum employment. Strong labor readings remove the employment-side case for easing and give the Committee room to tighten against inflation; weakening labor readings force the trade-off into the open.

**PAYEMS — Total nonfarm payroll employment.** What it measures: the net change in jobs on employer payrolls. Why the Fed watches it: it is the most direct count of job creation. Source: FRED `PAYEMS` (BLS, thousands, seasonally adjusted). Cadence: monthly, first Friday. Read rule: a 3-month average gain above +150k argues HIKE (no labor case for easing); below +50k argues CUT; between is NEUTRAL. Single-month prints are noisy — the rule uses the 3-month average, and a single negative print never scores alone.

**UNRATE — Unemployment rate.** What it measures: the share of the labor force without a job and actively seeking one. Why the Fed watches it: it is the headline slack gauge. Source: FRED `UNRATE` (BLS). Cadence: monthly, with payrolls. Read rule: a rise of more than 0.3 percentage points over three months argues CUT (deterioration); a stable rate below 4.5% is NEUTRAL; a rate below 4.0% with rising wages argues HIKE (overheating context).

**ICSA — Initial claims for unemployment insurance.** What it measures: new filings for jobless benefits — the fastest labor signal in the set, weekly. Why the Fed watches it: claims rise before payrolls fall; a sustained rise is the earliest warning of layoffs. Source: FRED `ICSA` (Department of Labor, weekly, seasonally adjusted). Cadence: weekly, Thursday. Read rule: a 4-week average below 250k is NEUTRAL (no deterioration); above 300k argues CUT; above 350k is a strong CUT trigger.

**JTSJOL — Job openings (JOLTS).** What it measures: unfilled positions on the last business day of the month. Why the Fed watches it: openings measure labor demand directly; the openings-to-unemployed ratio is the tightness gauge the Fed has cited in its own communications. Source: FRED `JTSJOL` (BLS, thousands). Cadence: monthly, with a one-month lag. Read rule: openings rising on a 3-month trend argues HIKE (demand strong, no easing case); openings falling more than 500k over three months argues CUT.

**ULCNFB — Unit labor costs, nonfarm business.** What it measures: what employers pay per unit of output — compensation growth minus productivity growth. Why the Fed watches it: it is the wage-price transmission channel. If pay rises faster than output per hour, firms either absorb the margin hit or pass it into prices; sustained unit-cost growth is the mechanism by which a hot labor market becomes persistent inflation. Source: FRED `ULCNFB` (BLS, quarterly index). Cadence: quarterly. Read rule: annualized growth above 2% argues HIKE (cost-push pressure); below 0% argues CUT (cost pressure easing); between is NEUTRAL.

### Group 4 — Growth and activity: the backdrop the Fed reads policy against

**GDPC1 — Real GDP.** What it measures: inflation-adjusted output of the whole economy. Why the Fed watches it: growth above trend with inflation above target argues the economy can absorb tighter policy; growth below trend argues restraint is already biting. Source: FRED `GDPC1` (BEA, billions of chained 2017 dollars, quarterly). Cadence: quarterly (advance, second, third estimates). Read rule: annualized growth above 2.5% argues HIKE (above-trend demand); below 1.0% argues CUT; between is NEUTRAL. Annualized growth is computed as (this quarter ÷ last quarter)^4 − 1, stated with the two levels named.

**INDPRO — Industrial production.** What it measures: output of factories, mines, and utilities. Why the Fed watches it: it is the monthly growth proxy — the goods-producing economy's pulse between GDP prints. Source: FRED `INDPRO` (Federal Reserve Board). Cadence: monthly. Read rule: m/m above +0.3% argues HIKE; below −0.3% argues CUT; between is NEUTRAL.

**RSXFS — Retail sales excluding food services.** What it measures: consumer spending on goods. Why the Fed watches it: consumption is roughly two-thirds of GDP; resilient spending argues demand is not yet restrained. Source: FRED `RSXFS` (Census Bureau, millions of dollars). Cadence: monthly. Read rule: m/m above +0.3% argues HIKE; below −0.3% argues CUT; between is NEUTRAL.

**CFNAI — Chicago Fed National Activity Index.** What it measures: a weighted average of 85 monthly indicators, standardized so zero means trend growth. Why the Fed watches it: it compresses the whole activity picture into one number with known recession/inflation thresholds published by the Chicago Fed. Source: FRED `CFNAI`. Cadence: monthly. Read rule: above +0.70 (sustained) argues HIKE (above-trend expansion with inflation risk); below −0.70 argues CUT (recession risk); between is NEUTRAL. These are the Chicago Fed's own published thresholds, stated as triggers.

**HOUST / PERMIT — Housing starts / building permits.** What they measure: new residential construction begun (starts) and authorized (permits) — the most rate-sensitive sector in the economy, and therefore the first place policy transmission shows up. Why the Fed watches them: housing is the transmission channel made visible. If starts are falling, higher rates are already restraining the most exposed sector; if starts are rising through high rates, transmission is weak. Source: FRED `HOUST`, `PERMIT` (Census Bureau, thousands of units, seasonally adjusted annual rate). Cadence: monthly. Read rule: starts falling more than 5% over three months argues CUT (transmission working, restraint biting); starts rising through the rate level argues HIKE (transmission weak). Permits lead starts — the same rule applies one step earlier.

### Group 5 — Curve and credit: what the bond market itself says

**DGS2 / DGS10 / DGS30 — Treasury par yields, 2/10/30 years.** What they measure: the market's required return for lending to the U.S. government at each maturity. Why the Fed watches them: the long end is the discount rate for the whole economy; the front end is the market's forecast of the policy path. Source: FRED `DGS2`, `DGS10`, `DGS30` (daily, market yield on Treasury securities at constant maturity). Cadence: daily. Read rule (levels): a 2-year yield rising faster than the 10-year (flattening) argues the market is pricing more near-term tightening — scored through the slope rules below, not separately. The 10-year level itself is the desk's discount-rate anchor (§5), not a hike/cut vote.

**T10Y2Y / T10Y3M — Curve slopes.** What they measure: the 10-year minus 2-year spread and the 10-year minus 3-month spread — the slope of the yield curve. Why the Fed watches them: the slope encodes the market's growth and policy expectations. An inverted curve (short rates above long rates) has historically preceded recessions, because it means the market expects the Fed to cut in the future. Source: FRED `T10Y2Y`, `T10Y3M` (percentage points). Cadence: daily. Read rule: either slope below zero (inverted) argues CUT (the market expects easing ahead); a positive slope is NEUTRAL; a slope steepening by more than 50bp in a month argues the easing cycle is being priced (CUT-side context). Curve theories in brief, in original words: the expectations view says long yields are the average of expected future short rates; the liquidity-preference view adds a premium for holding longer bonds; the preferred-habitat view says different buyers dominate different maturities, so supply and demand at each tenor matter. All three agree that slope carries information about the expected policy path — they disagree about how much of the long yield is forecast and how much is premium. That disagreement is why the slope is scored NEUTRAL when positive rather than read as a hike vote.

**BAMLC0A0CM / BAMLH0A0HYM2 — Investment-grade / high-yield option-adjusted spreads.** What they measure: the extra yield corporate bonds pay over Treasuries, adjusted for embedded options — the market's price of credit risk. Why the Fed watches them: widening spreads mean financial conditions are tightening on their own (the market doing the Fed's work) and can signal stress that forces an easing response; tight spreads mean easy conditions that argue against urgency to cut. Source: FRED `BAMLC0A0CM` (ICE BofA US Corporate Master OAS), `BAMLH0A0HYM2` (ICE BofA US High Yield OAS), percentage points. Cadence: daily. Read rule: IG OAS above 1.50% or HY OAS above 5.00% argues CUT (stress, tightening conditions); IG below 1.00% and HY below 4.00% is NEUTRAL (no stress, no easing case); between is NEUTRAL with a watch flag.

### Group 6 — Market pricing of the next decision

**CME FedWatch (fed funds futures).** What it measures: the probabilities of each target-range outcome at each FOMC meeting, derived from 30-day federal funds futures prices by CME's published method (the implied rate change divided into 25bp steps, chained across meetings). Why the Fed watches it: it is the market's consolidated forecast, and the Committee reads it as the expectations backdrop — though the Fed has repeatedly said it is not bound by it. Source: cme.com (CME FedWatch Tool). Cadence: live during futures trading. Read rule: a hike probability above 50% for the next meeting argues HIKE; a cut probability above 50% argues CUT; otherwise NEUTRAL. Access note: the tool is an embedded application with no public text API; when it cannot be read directly, the figure is reported from independent secondhand reads with that limit stated, and Kalshi (below) is the primary basis.

**Kalshi KXFEDDECISION.** What it measures: event-contract prices for each FOMC outcome (hike 25bp, hike more than 25bp, hold, cut 25bp, cut more than 25bp) — a prediction market's priced probabilities. Why it matters here: it is directly readable via a public API, it is a second basis independent of futures, and its prices update continuously. Source: `api.elections.kalshi.com/trade-api/v2/markets?series_ticker=KXFEDDECISION` (direct GET, no key). Cadence: live. Read rule: same 50% rule as FedWatch. Cross-check rule: Kalshi and FedWatch must be reported side by side; agreement within ~5 points corroborates; a wider gap is reported as a disagreement with both figures named, not averaged away.

### Group 7 — Fed communication: the Committee speaking for itself

**FOMC meeting calendar.** The Committee holds eight scheduled meetings a year; four (March, June, September, December) carry the Summary of Economic Projections. Source: federalreserve.gov/monetarypolicy/fomccalendars.htm. The next meeting date, the decision time (2:00 p.m. ET on the second day), and whether an SEP follows are verified on that page each run — never carried from memory.

**Summary of Economic Projections (SEP) / dot plot.** What it measures: each participant's anonymous projection of the policy rate, growth, unemployment, and inflation. Why it matters: it is the Committee's own published path — the median dot is the closest thing to an official forecast. Source: federalreserve.gov (released with the statement at SEP meetings). Read rule: a median dot above the current range for year-end argues HIKE context; the SEP vintage must always be named (a September dot plot is stale after a December meeting).

**FOMC minutes.** Released three weeks after the decision (FACT — federalreserve.gov calendar page). The minutes reveal the distribution of views behind the vote, including dissents and the conditions members named for changing stance. Read rule: minutes showing a majority open to tightening argue HIKE context; minutes showing concern about overtightening argue CUT context. Minutes are context, never a vote in the tally by themselves — they score through the communication line only with named quotes.

**Scheduled Fed speakers.** Each run lists the week's scheduled remarks (Chair, Vice Chairs, Governors, regional presidents), with voter status where known. A speaker's stated position is reported as that speaker's view, never as the Committee's. Read rule: net hawkish guidance across the week's speakers (more officials favoring tightening than easing, by count of named statements) argues HIKE; net dovish argues CUT; mixed is NEUTRAL. This line is an INFERENCE — it aggregates judgments — and is labeled as such in every snapshot.

---

## 3. One-page rise/cut dashboard table

The trigger rules from §2, compressed. Each run scores every line HIKE / CUT / NEUTRAL by the rule stated, counts transparently, and reports the count with the line items — never a bare total.

| # | Indicator | HIKE trigger | CUT trigger | Otherwise |
|---|---|---|---|---|
| 1 | DFF | — | — | NEUTRAL unless outside range |
| 2 | Target range (DFEDTARL/U) | — | — | NEUTRAL (stance, not signal) |
| 3 | IORB | — | — | NEUTRAL at normal position |
| 4 | ON RRP (RRPONTSYD) | — | Spike + funding stress | NEUTRAL near zero |
| 5 | Balance sheet (WALCL) | Sustained runoff (context) | Sustained growth (context) | NEUTRAL flat |
| 6 | Headline CPI (CPIAUCSL) | m/m > +0.25% or y/y > 3% | m/m < +0.10% or y/y < 2.5% | NEUTRAL |
| 7 | Core CPI (CPILFESL) | m/m > +0.25% (3 straight ≥ +0.3% = strong) | m/m < +0.10% | NEUTRAL |
| 8 | Core PCE (PCEPILFE) | y/y > 2.5% or m/m > +0.25% | y/y < 2.2% | NEUTRAL |
| 9 | PPI final demand (PPIFIS) | m/m > +0.3% or y/y > 4% | m/m < 0% | NEUTRAL |
| 10 | Core PPI (BLS release) | m/m > +0.3% | m/m < 0% | NEUTRAL |
| 11 | Median CPI (CPIMEDSL) | m/m > +0.25% | m/m < +0.15% | NEUTRAL |
| 12 | Breakevens (T5YIE/T10YIE) | > 2.75% | < 1.75% | NEUTRAL 2.0–2.5% |
| 13 | Michigan expectations (MICH) | > 3.5% | < 2.5% | NEUTRAL |
| 14 | Payrolls 3-mo avg (PAYEMS) | > +150k | < +50k | NEUTRAL |
| 15 | Unemployment (UNRATE) | < 4.0% + rising wages | +0.3pp over 3 months | NEUTRAL |
| 16 | Initial claims 4-wk avg (ICSA) | — | > 300k | NEUTRAL < 250k |
| 17 | Openings trend (JTSJOL) | Rising 3-mo trend | −500k over 3 months | NEUTRAL |
| 18 | Unit labor costs (ULCNFB) | > 2% annualized | < 0% annualized | NEUTRAL |
| 19 | Real GDP (GDPC1) | > 2.5% annualized | < 1.0% annualized | NEUTRAL |
| 20 | Industrial production (INDPRO) | m/m > +0.3% | m/m < −0.3% | NEUTRAL |
| 21 | Retail sales (RSXFS) | m/m > +0.3% | m/m < −0.3% | NEUTRAL |
| 22 | CFNAI | > +0.70 sustained | < −0.70 | NEUTRAL |
| 23 | Housing starts (HOUST) | Rising through high rates | −5% over 3 months | NEUTRAL |
| 24 | Permits (PERMIT) | Rising trend | Falling trend | NEUTRAL |
| 25 | 2s10s (T10Y2Y) | — | < 0 (inverted) | NEUTRAL positive |
| 26 | 10s3m (T10Y3M) | — | < 0 (inverted) | NEUTRAL positive |
| 27 | IG spread (BAMLC0A0CM) | — | > 1.50% | NEUTRAL < 1.00% |
| 28 | HY spread (BAMLH0A0HYM2) | — | > 5.00% | NEUTRAL < 4.00% |
| 29 | Market pricing (Kalshi/FedWatch) | Hike prob > 50% | Cut prob > 50% | NEUTRAL |
| 30 | Fed communication | Net hawkish (named statements) | Net dovish (named statements) | NEUTRAL mixed |

Scoring notes: the inflation block (lines 6–11) carries the most weight in the narrative because price stability is the half of the mandate currently furthest from target — but the tally itself is unweighted and transparent, one vote per line, so the reader can re-weight. The communication line (30) is an INFERENCE by construction. A line whose data failed to pull is scored UNVERIFIED, excluded from the count, and named in the snapshot's UNVERIFIED register — never silently dropped, never guessed.

---

## 4. The practitioner POV: data needed before acting

The user asked what a CFA charterholder and a licensed Series 7 broker would each require in hand before acting — and the answer must serve the value-investing decision, not sit beside it. Both checklists below end at the same place: the discount rate, the margin of safety, and the documentation that lets a decision be audited later. Rule and standard concepts are summarized in original words from the public concepts; no licensed text is reproduced.

### 4a. CFA charterholder POV — the investment decision process

The charterholder's discipline, in the concepts of the CFA Institute Code of Ethics and Standards of Professional Conduct, is diligence with a reasonable basis: thorough, independent research, documented, with the reasoning preserved so the decision can be reviewed. Applied to this desk, the checklist before forming or acting on a rates view is:

1. **The discount curve, tenor by tenor.** A view needs the whole curve, not one yield: the 3-month bill (policy anchor), the 2-year (policy-path forecast), the 5- and 10-year (discount-rate anchors), the 30-year (term premium and long expectations). Each tenor feeds a different part of the valuation — the front end feeds near-term cash flows, the long end feeds the terminal value. Indicators: DTB3, DGS2, DGS5, DGS10, DGS30 (FRED, daily). Without the curve, there is no discount rate; without the discount rate, there is no intrinsic value.
2. **Inflation expectations, real vs nominal.** A nominal discount rate built on a stale inflation assumption misstates real value. The checklist requires both the market's expectation (breakevens) and the household survey (Michigan), because they measure different populations and their disagreement is itself a risk input. Indicators: T5YIE, T10YIE, MICH (FRED). The Fisher relationship — nominal rate ≈ real rate + expected inflation — is the arithmetic that ties them together, stated here as the concept, not as a pricing formula.
3. **Risk premia.** The equity risk premium and the credit risk premium are the compensation for bearing risk above the risk-free rate. If credit spreads are tight, the market is charging little for risk — which means the margin of safety must come from price, not from spread. Indicators: BAMLC0A0CM, BAMLH0A0HYM2 (FRED, daily), plus the earnings-yield comparison in §5.
4. **The earnings/valuation linkage for the watchlist.** Rates matter to the watchlist only through earnings power and multiples. The checklist requires, for the names the desk follows, the separation the Graham lens demands: what changed — the multiple (Mr. Market, rate-driven) or the earnings power (the business)? That separation needs the earnings data the earnings desk carries; Desk 7 supplies the rate half (the discount rate and its change) and names the multiple effect with the Gordon arithmetic in §5.
5. **Scenario and stress inputs.** A single-point rate view is not a reasonable basis. The checklist requires at least three rate scenarios (current curve, +50bp parallel shift, −50bp parallel shift) run through the discount-rate sensitivity, with the margin-of-safety consequence of each stated. Scenarios are labeled HYPOTHETICAL projections from real base data, per the desk's hard data rule — never presented as forecasts.
6. **The documentation standard.** Thesis, evidence, what would change the view — written before acting, in that order, with every number sourced and as-of dated. This is the record-retention concept: a decision that cannot be reconstructed from its record was not a disciplined decision. Every Desk 7 snapshot follows this format (see §6).

### 4b. Series 7 licensed broker POV — the recommendation standard

The broker's discipline, in the concepts of FINRA rules, is that a recommendation must have a reasonable basis, must fit the customer, and must be communicated fairly. The desk is not a brokerage and makes no recommendations to customers — but the discipline maps directly onto the desk's own gates, because the desk's "customer" is its own mandate. The mapping:

1. **The client-profile analog: the mandate, constraints, and risk tolerance.** Before any action, the broker must know the customer — objectives, time horizon, risk tolerance, constraints. For this desk, the mandate is stated in the repo's own rules (FACT — `hedge-desk/AGENTS.md`, read 2026-11-13): paper-only until a separately reviewed release says otherwise; gates fail closed and agents cannot waive them; every decision retains reason codes and enough inputs to reproduce it; the authoritative Risk of Ruin is an immutable upstream input that agents never calculate, estimate, infer, modify, or substitute; research input is the watchlist only — no brokerage balances, positions, or account data; Emporion is the compass, not the broker — no order placement, no execution workflows. The user-stated scope adds: covered premium only, always behind human approval, compliance, Back Office, and Risk of Ruin gates (user statement 2026-10-03, recorded in desk memory). Any rates view that implies action outside those constraints fails the profile check before it reaches the data.
2. **Product and market data.** A recommendation needs the security's own facts — for rates work, the market facts: yields at each tenor, spreads, curve shape, and where relevant the features that change a bond's behavior (call provisions, credit quality). Indicators: the full Group 5 set (DGS2/5/10/30, T10Y2Y, T10Y3M, BAMLC0A0CM, BAMLH0A0HYM2). A view formed without the curve shape is a view formed without the product data.
3. **The economic backdrop that justifies the rationale.** The rationale for any rates view must rest on the mandate's own evidence — inflation, labor, growth — not on a single print. Indicators: Groups 2, 3, and 4 in full. A rationale citing one hot CPI print while ignoring three soft payrolls prints fails the fair-and-balanced concept: the communication must present the balance of the evidence, including what argues the other way.
4. **The documentation and disclosure standard.** The broker's communications concept requires fair, balanced, non-misleading presentation with the basis stated. For the desk, that means: every snapshot names its sources and as-of dates, states what is UNVERIFIED, shows the disconfirming evidence (the CUT lines in a HIKE tally, and vice versa), and labels every scenario HYPOTHETICAL. A snapshot that reports only the evidence for its own conclusion fails this standard.

Both checklists converge on the same working rule: **no view without the curve, no action without the mandate check, no conclusion without the disconfirming evidence.** The practitioner sections are not compliance decoration — they are the reason the tally in §3 is transparent and the snapshot in the paired file shows its work.

---

## 5. The Graham lens: rates as the discount rate

### 5a. Intrinsic-value math — the discount rate moves value mechanically

Graham's central analytical idea, in original words: a security has an intrinsic value — what the business is worth based on its earnings power — and the market price is a separate thing, set by Mr. Market's mood on any given day. The investor's job is to estimate the first, observe the second, and act only when the gap (the margin of safety) is wide enough.

Rates enter intrinsic value through the discount rate: future cash flows are worth less today when the rate used to discount them is higher. The Gordon-style formula below is the simplest version of that arithmetic — a perpetuity growing at a constant rate — used here as a sensitivity demonstration, not as a valuation of any real security:

    Multiple = 1 ÷ (r − g)

where r is the discount rate and g is the assumed perpetual growth rate. Both inputs are stated; g = 3.00% is an ASSUMPTION for illustration, labeled as such; r is the live 10-year Treasury yield from FRED, the desk's discount-rate anchor.

**Worked math with live numbers (recomputed this session, FRED DGS10):**

The 10-year yield moved from 4.86% (Nov 6) to 4.98% (Nov 10) — a rise of 0.12 percentage points (4.98 − 4.86 = +0.12, arithmetic).

- Case A (Nov 6): 1 ÷ (0.0486 − 0.0300) = 1 ÷ 0.0186 = **53.76x**
- Case B (Nov 10): 1 ÷ (0.0498 − 0.0300) = 1 ÷ 0.0198 = **50.51x**
- Change: (50.51 − 53.76) ÷ 53.76 = **−6.06%**

A 12-basis-point rise in the discount rate mechanically lowers the Gordon-implied multiple by about 6%, with no change in earnings power, no change in growth, and no change in the business. In dollar terms for a hypothetical $1-per-share earner growing at the assumed 3%: $53.76 → $50.51, a $3.25 decline in intrinsic value from the rate move alone. (HYPOTHETICAL illustration — the $1 earner and the 3% growth rate are assumptions; the yields are FACT.)

The longer window tells the other half of the story, and honesty requires both: from Oct 5 (10-year 5.31%) to Nov 10 (4.98%), the discount rate FELL 0.33 points, and the same arithmetic gives 1 ÷ (0.0531 − 0.0300) = 43.29x → 50.51x, a **+16.67%** rise in the implied multiple. Over five weeks, rates raised intrinsic value; over the last three sessions, rates lowered it. The business did not change on either window — Mr. Market's discount rate did. That is the separation the snapshot must make every time.

**Limits of this arithmetic (stated, not buried):** the Gordon form assumes perpetual constant growth, a single discount rate for all years, and r > g. Real businesses do not grow at one rate forever, and the 10-year yield is a proxy for the discount rate, not the discount rate itself (the full curve and a risk premium belong in a real estimate). The formula is used here to size the sensitivity, not to value a security. A sensitivity that moves 6% on 12bp is the point — it shows why Desk 7's discount-rate input deserves the evidence discipline of §4.

### 5b. Duration approximation — what a yield move does to a bond position

The same discounting logic prices bonds directly. The duration approximation states the price change from a yield change as:

    ΔP/P ≈ −D × Δy

where D is modified duration (about 8 for a 10-year Treasury note — an APPROXIMATION, stated) and Δy is the yield change. With the measured Nov 6 → Nov 10 move (Δy = +0.12pp):

    −8 × 0.0012 = −0.0096 = **−0.96%** (about −1.0% on a 10-year position)

For the 2-year (D ≈ 1.9, Δy = +0.22pp from 4.51% to 4.73%): −1.9 × 0.0022 = **−0.42%**. The long end carries roughly twice the price sensitivity of the front end for the measured moves — which is why the curve's shape, not just its level, belongs in every snapshot.

Limits: the approximation is linear — it ignores convexity, which makes the true loss slightly smaller for a rise and the true gain slightly larger for a fall. It assumes a parallel shift; the Nov 6 → Nov 10 shift was not parallel (the front end rose more), so the 10-year figure is the 10-year figure only. Duration itself drifts as yields move. The approximation sizes the effect; it does not price the bond.

### 5c. The stock-vs-bond comparison (Graham's comparison) — live status UNVERIFIED

Graham's comparison, in original words: compare what stocks earn (the earnings yield — earnings divided by price) with what bonds pay (the bond yield). When the earnings yield comfortably exceeds the bond yield, stocks offer compensation for their extra risk; when it does not, the bond is doing the stock's job with a contractual claim instead of a residual one. The formula:

    Earnings yield = E ÷ P = 1 ÷ (P/E).  Spread = earnings yield − 10-year yield.

**Live comparison: UNVERIFIED.** The bond side verifies (10-year 4.98%, FRED DGS10, Nov 10 — FACT). The earnings side did not verify from any enumerated primary source this session: the Shiller dataset download from Yale failed (connection, no file returned); no S&P Dow Jones public page returned a usable figure; no Yahoo meta provided an index earnings yield. Per the fail-closed rule, the live comparison is UNVERIFIED and no live spread is asserted.

**Reference points (labeled, not the verified comparison):** FactSet's published Earnings Insight (Nov 9, 2026) reported a forward 12-month P/E of 17.7 for the S&P 500 on Nov 5, based on a closing price of 7,353.73 and a forward 12-month EPS estimate of $415.82 — recomputed: 7,353.73 ÷ 415.82 = 17.69x, and the implied forward earnings yield is 415.82 ÷ 7,353.73 = 5.65%. A second vendor basis (DollarLiquidity, Nov 12) reported a forward P/E of 18.34x, implying 5.45%. On the trailing basis, aggregators conflict (23.2x–25.75x, implying 3.9%–4.3%) with no primary source. These are vendor-reported figures with named provenance, not verified FACTs under this framework's standard, and the forward/trailing basis difference (about 1.5 points of yield) is itself the warning against quoting any single earnings-yield number without its basis.

**Labeled worked example (HYPOTHETICAL — assumed inputs, real formula):** if the earnings yield were 5.00% and the 10-year yield were the verified 4.98%, the spread would be 5.00 − 4.98 = +0.02 points — essentially no compensation for equity risk on this crude comparison, which is the condition under which Graham's defensive investor demands a wider margin of safety from price alone. Change the assumed earnings yield to 4.00% and the spread is −0.98 points — bonds paying more than stocks earn. The example shows the mechanics; it asserts nothing about today's earnings yield.

### 5d. Margin of safety as the decision variable

The action read in every snapshot is framed through margin of safety, never through momentum:

- A rise in the discount rate lowers intrinsic value (shown in §5a). The same market price now sits closer to (or above) intrinsic value. The margin of safety has narrowed. The required discount widens. Nothing about the business changed.
- A fall in the discount rate raises intrinsic value. The margin of safety widens at the same price. That is not a buy signal — it is a wider cushion, and the desk's other gates (human approval, compliance, Back Office, Risk of Ruin) still govern any action.
- Tight credit spreads (§2, Group 5) mean the market is charging little for risk. The margin of safety must then come from the price paid, not from the spread earned. "Chasing yield" — accepting a thinner margin because the spread looks attractive — is the exact error the defensive discipline exists to prevent, and it appears nowhere in this framework as a recommendation.

### 5e. Mr. Market, stated plainly

When the snapshot reports that the multiple compressed 6% on a 12bp rate rise, it must also report whether earnings power changed. If earnings power did not change, the move is Mr. Market repricing the same stream — mood, not substance. The defensive investor's response to mood is patience, not reaction. The snapshot's "multiple vs earnings power" section exists for exactly this separation, and a snapshot that cannot make the separation says so.

### 5f. The defensive allocation context (Graham's 25–75 discipline)

Graham's defensive-investor concept, in original words: hold a balance between stocks and bonds, never all of one, with the stock share bounded (the classic statement bounds it between one-quarter and three-quarters) and rebalanced when the balance drifts. The concept is context for this framework, not an allocation recommendation: when the discount rate is high and the earnings-yield spread is thin, the bond side of that balance is doing more of the work, and the discipline argues for patience on the stock side rather than stretching for return. No allocation change is proposed or authorized by this framework — the desk's gates govern all action, and this document is decision support only.

---

## 6. How Desk 7 uses this framework each run

1. **Pull first, in FRED-first order.** Run the keyed FRED helper for every series in §2 (daily series: limit 3; monthly/quarterly: limit 3, plus limit 14 once a month for trend context). Pull Kalshi KXFEDDECISION by direct GET. Check the Fed calendar page for the next meeting and SEP vintage. Check CME FedWatch; if inaccessible, record the limit and use Kalshi as primary with secondhand FedWatch reads labeled as such.
2. **Recompute, don't carry.** Every percent change is recomputed from the two values named in the snapshot. Every slope is recomputed from the two yields named. Every basis is labeled (same series, same horizon, same convention) before any comparison. A number carried from a prior run without re-verification is labeled as carried, never presented as fresh.
3. **Score the tally by the §3 rules.** One vote per line, HIKE/CUT/NEUTRAL, with the rule that fired named. UNVERIFIED lines are excluded from the count and named in the register. The tally arithmetic is shown explicitly (counts, which lines, which rules).
4. **Run the three cross-checks.** (a) Kalshi vs FedWatch — agreement or disagreement, both figures named. (b) Breakevens vs Michigan — market vs household expectations, gap in points named. (c) Payrolls trend vs claims trend — agreement or disagreement. Report agreements AND disagreements honestly; a disagreement is a finding, not an embarrassment.
5. **Write the verdict as thesis / evidence / what would change it.** Thresholds as triggers, not forecasts. The "what would change it" section names the specific prints and dates that would flip the read (next CPI, next PCE, next claims run, next Fed speaker slate).
6. **Frame the action read through margin of safety.** Multiple change vs earnings-power change, stated separately. What is NOT yet knowable, stated plainly. Paper-only framing, never a trade authorization, never a substitute for the desk's gates, never a Risk of Ruin input.
7. **Fail closed.** Any series that fails to pull is UNVERIFIED with the reason. Any comparison whose basis cannot be reconciled is not made. The snapshot is published with its gaps visible, not held for completeness and not smoothed over.

---

## 7. Dashboard determination — what an amazing Desk 7 Plotly dashboard looks like

The dashboard exists to answer the decision questions in this framework at a glance, with the evidence one hover away. Data flow: the same free pulls (FRED helper, Kalshi API, Fed calendar) straight into the visuals — no hand-typed numbers, no backend, a single self-contained HTML file, Plotly via CDN. Any panel whose data failed to pull reads "data unavailable" with the reason. No order buttons, no buy/sell signals, no trade authorization, no Risk of Ruin content. The dashboard informs the premium/multiple/margin-of-safety decisions; it does not execute or recommend trades.

**Panel 1 — The yield curve, now vs then.** Decision question: *What discount rate does the curve imply today, and how has it moved?* Content: the curve (3M, 2Y, 5Y, 10Y, 30Y) at the latest close plus snapshots ~30/60/90 days earlier, and a curve-history chart with a range slider. Interactions: hover shows yield + source + as-of date per point; tenor toggles; range selection on the history chart. Why it leads: the curve IS the discount rate — everything else in the framework hangs off it.

**Panel 2 — Fed decision pricing.** Decision question: *What does the market price for the next FOMC decision, and how much do two independent markets agree?* Content: Kalshi outcome bars for the Dec 8–9 meeting (hike 25bp / hike >25bp / hold / cut 25bp / cut >25bp), the FedWatch secondhand range shown as a labeled annotation (not a bar — it is not a direct pull), and the meeting calendar (decision date/time, SEP status, minutes date). Interactions: hover shows price, bid/ask, volume, as-of time. Why it matters: it is the market's consolidated forecast, and the Kalshi/FedWatch gap is the disagreement gauge.

**Panel 3 — Inflation vs the 2% target.** Decision question: *Is inflation returning to target, and is the pressure broad or narrow?* Content: monthly percent changes for headline CPI, core CPI, core PCE, and PPI final demand against the 0.17%/month pace consistent with 2% annualized; breakeven expectations (5Y/10Y) against the 2% line; the Michigan survey level as a labeled marker. Interactions: hover shows value + source + observation date; series toggles. The missing October 2025 CPI observation (BLS collection gap) is shown as a gap, never interpolated.

**Panel 4 — Labor: demand, slack, and the fast signal.** Decision question: *Is the labor market giving the Fed room to tighten, or forcing the trade-off?* Content: payrolls monthly change (3-month average highlighted), unemployment rate, weekly initial claims (4-week average), JOLTS openings. Interactions: hover with source + as-of; the payrolls chart shows the 3-month average the read rule uses, not just the noisy monthly print.

**Panel 5 — Curve slope + credit spreads.** Decision question: *Is the bond market pricing recession or stress that would force easing?* Content: 2s10s and 10s3m slopes with the zero (inversion) line marked; IG and HY option-adjusted spreads with the stress thresholds marked. Interactions: hover, range slider, threshold annotations. Why it matters: slope and spreads are the market's own recession/stress vote, independent of the data prints.

**Panel 6 — The Graham lens.** Decision question: *What does the rate environment do to intrinsic value and the required margin of safety?* Content: (a) the earnings-yield vs bond-yield comparison — which reads "data unavailable" when the earnings-yield input fails the primary-source standard, with the formula and the reason shown; (b) the discount-rate sensitivity curve: the Gordon-implied multiple as a function of the discount rate, computed live from the real 10-year base, with a scenario slider for the discount rate — labeled HYPOTHETICAL projection from real base data, with the assumed growth rate stated and adjustable. Interactions: the slider moves the rate and shows the implied multiple and the percent change from the base case, with the assumption labels always visible. Why it closes the dashboard: it turns every other panel's data into the one decision variable the desk actually uses — the margin of safety.

**What was considered and rejected:** a TradingView-style embed (external dependency, no control over data provenance); a real-time ticking display (the desk's data is daily/monthly — a ticking display would imply precision the data does not carry); a single "hawkish/dovish" gauge (it would hide the tally the framework exists to make transparent). The dashboard shows the evidence and the arithmetic, not a verdict dial.

---

## Sources

- Federal Reserve: federalreserve.gov — FOMC statements, meeting calendars, Summary of Economic Projections, monetary policy framework. FRED (Federal Reserve Bank of St. Louis): fred.stlouisfed.org — all series cited by ID.
- Bureau of Labor Statistics: bls.gov — CPI, PPI, employment, JOLTS, unit labor costs releases.
- Bureau of Economic Analysis: bea.gov — PCE price index, GDP releases.
- CME Group: cme.com — FedWatch Tool methodology and probabilities.
- Kalshi: api.elections.kalshi.com — KXFEDDECISION event contracts.
- FINRA: finra.org — Rule 2111 (suitability), Rule 2210 (communications), Rule 2090/4512 (know-your-customer / account records) — public rule concepts, summarized in original words.
- CFA Institute: cfainstitute.org — Code of Ethics and Standards of Professional Conduct concepts (diligence and reasonable basis, record retention, fair dealing, suitability) — summarized in original words.
- Graham concepts (intrinsic value, margin of safety, Mr. Market, defensive-investor discipline, stock-vs-bond comparison) are stated in original words from the public concepts; no licensed text is reproduced.
- Repo rules: `hedge-desk/AGENTS.md` (mandate, constraints, gates) — read 2026-11-13.
