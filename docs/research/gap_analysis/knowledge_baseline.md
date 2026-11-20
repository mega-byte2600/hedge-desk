# Knowledge baseline for desk agents: FINRA, NFA, NASAA and CFA (public sources only)

**Status:** research input. It is not legal advice, not exam prep material, and not a credential.
No agent on this desk holds any registration (see `hedge-desk/docs/compliance/FINRA_ENGINEERING_MAP.md`).
**Compiled:** 2026-11-19, from official public pages: finra.org, nasaa.org, nfa.futures.org, cfainstitute.org,
and the public rule texts (eCFR, FINRA rulebook). Everything is in our own words. No licensed manual,
prep-provider text or CFA curriculum text was used or reproduced.
**Verification legend:** every count, duration, passing score and weight below was read from the official page
cited next to it on the date above. Anything we could not confirm says **unverified**.
Labels: this document is **VERIFIED** only in the sense that the figures match their cited pages. Whether it meets
the GP's needs (**VALIDATED**) has not been assessed.

## 0. Recent changes worth knowing (2025–2026)

- **FINRA retake waits shorten on 2027-01-19:** 30 → 15 days after a 1st or 2nd failure, 180 → 60 days after a 3rd (Regulatory Notice 26-18, summarised on each exam page, e.g. [Series 7](https://www.finra.org/registration-exams-ce/qualification-exams/series7)).
- **Fewer unscored pretest items** on the SIE, Series 7 and Series 79 from 2025-10-27 ([FINRA weekly, 2025-10-08](https://www.finra.org/compliance-tools/weekly-archive/10082025)). The current per-exam unscored count is **unverified**.
- **Possible Series 7 rewrite:** FINRA opened a job-analysis survey on 2026-09-14 to guide updates ([FINRA weekly, 2026-09-02](https://www.finra.org/compliance-tools/weekly-archive/09022026)). No new outline yet.
- **NASAA on 2027-01-04:** remote testing ends; the wait after a 3rd failure falls from 180 to 60 days, while the 1st/2nd stay at 30 ([NASAA exam FAQs](https://www.nasaa.org/exams/exam-faqs/)).
- **NASAA advertising:** model rules on adviser advertising were amended in May 2026; the exams will reflect them in early 2027, date not yet given ([NASAA Series 63 page](https://www.nasaa.org/exams/study-guides/series-63-exam-content-outline/)).
- **CFA 2027 curriculum**, announced 2026-05-26, applies from the February 2027 exams ([press release](https://www.cfainstitute.org/about/press-room/2026/cfa-institute-announces-updates-to-cfa-program-curriculum)). Level I Ethics weight goes down, Quant goes up, and four topics are renamed (§14). It adds data science, AI and LLM content and aligns Ethics to the Standards of Practice Handbook, 12th edition ([curriculum update 2027](https://www.cfainstitute.org/sites/default/files/curriculum-update-2027.pdf)). Every level requires one Practical Skills Module (PSM).
- **Series 9/10 is still active** as two parts, with no retirement or restructuring notice ([Series 9/10 page](https://www.finra.org/registration-exams-ce/qualification-exams/series9-10)).

## 1. SIE — Securities Industry Essentials (FINRA)

**Purpose / who needs it:** the entry-level knowledge exam. No firm sponsorship is needed to sit it. It is a corequisite for the Series 7, 57, 79, 82, 86/87, 99 and other representative exams.
**Format** ([SIE page](https://www.finra.org/registration-exams-ce/qualification-exams/securities-industry-essentials-exam-sie)): 75 multiple-choice questions, 1 h 45 min, passing score 70. The scored/unscored split is **unverified** after the Oct 2025 change.

| Section | Weight | Items |
|---|---|---|
| 1 Knowledge of Capital Markets | 16% | 12 |
| 2 Understanding Products and Their Risks | 44% | 33 |
| 3 Understanding Trading, Customer Accounts and Prohibited Activities | 31% | 23 |
| 4 Overview of the Regulatory Framework | 9% | 7 |

**Key concepts an agent must know**
- **Who regulates what.** The SEC, the SROs (FINRA, MSRB, the exchanges), state administrators, the Fed (credit under Reg T), the CFTC/NFA for futures, and FinCEN for anti-money-laundering (AML).
- **The core statutes.** The Securities Act of 1933 covers new issues (registration and prospectus delivery). The Exchange Act of 1934 covers secondary markets, broker-dealers and SROs. The Investment Company Act of 1940 covers funds. The Investment Advisers Act of 1940 covers advisers.
- **Products and their risks.** Equity, debt, municipal securities, packaged products (mutual funds, ETFs, UITs, variable annuities), options and DPPs. Main risk types: market, credit, interest-rate, liquidity, inflation and reinvestment.
- **Options basics.** Calls, puts, long and short positions, intrinsic and time value, and exercise and assignment. The Options Disclosure Document (ODD) must be delivered before an options account is approved.
- **Account types and registration.** Individual, joint (JTWROS/TIC), custodial (UTMA/UGMA), trust, entity, retirement, and cash versus margin accounts.
- **Prohibited practices.** Churning, unauthorized trading, front-running ([FINRA 5270](https://www.finra.org/rules-guidance/rulebooks/finra-rules/5270)), market manipulation, insider trading (Exchange Act 10b-5), guarantees against loss, sharing in customer accounts, and improper borrowing or lending ([FINRA 3240](https://www.finra.org/rules-guidance/rulebooks/finra-rules/3240)).
- **Settlement and trading mechanics.** Regular-way equity trades settle T+1 (SEC amendment to Rule 15c6-1, effective 2024-05-28). Order types: market, limit, stop and stop-limit.
- **AML and CIP.** Customer identification programs ([31 CFR 1023.220](https://www.ecfr.gov/current/title-31/section-1023.220)), beneficial-ownership due diligence ([31 CFR 1010.230](https://www.ecfr.gov/current/title-31/section-1010.230)), suspicious activity reports, and currency transaction reports for cash over $10k.

**How it maps to the desk:** the vocabulary and ontology layer for every agent, including Muse. It sets the shared glossary used for instrument and product types and for risk labels in candidate records.

## 2. Series 7 — General Securities Representative (FINRA)

**Purpose:** qualifies a person, sponsored by a member firm, to solicit, recommend and execute trades in most securities, including options and munis. It does not cover commodities or futures.
**Format** ([Series 7 page](https://www.finra.org/registration-exams-ce/qualification-exams/series7)): 125 multiple-choice items, 3 h 45 min, passing score 72. The SIE is a corequisite.

| Function | Items | Weight |
|---|---|---|
| F1 Seeks business from customers and potential customers | 9 | 7.2% |
| F2 Opens accounts after evaluating financial profiles and objectives | 11 | 8.8% |
| F3 Provides information, makes recommendations, transfers assets, maintains records | 91 | 72.8% |
| F4 Obtains and verifies instructions; processes and confirms transactions | 14 | 11.2% |

**Key concepts an agent must know**
- **Regulation Best Interest** ([17 CFR 240.15l-1](https://www.ecfr.gov/current/title-17/section-240.15l-1)) has four component obligations: disclosure, care, conflict-of-interest and compliance. Form CRS goes to retail investors.
- **Suitability ([FINRA 2111](https://www.finra.org/rules-guidance/rulebooks/finra-rules/2111)).** It still governs non-Reg-BI recommendations (Supplementary Material .08 excludes recommendations covered by Reg BI). Its three prongs are reasonable-basis, customer-specific and quantitative.
- **Know your customer ([FINRA 2090](https://www.finra.org/rules-guidance/rulebooks/finra-rules/2090)) and account records ([FINRA 4512](https://www.finra.org/rules-guidance/rulebooks/finra-rules/4512)).** These include a trusted contact person. Financial-exploitation holds come under [FINRA 2165](https://www.finra.org/rules-guidance/rulebooks/finra-rules/2165).
- **Options ([FINRA 2360](https://www.finra.org/rules-guidance/rulebooks/finra-rules/2360)):** required profile items, principal approval, the ODD, a signed options agreement within 15 days, special risk disclosure and minimum-equity procedures before uncovered writing, and position and exercise limits.
- **Option strategy math.** Breakevens, maximum gain and maximum loss for covered calls, cash-secured puts, spreads, straddles and collars. Tax treatment at a high level.
- **Margin.** Reg T initial requirement ([12 CFR 220](https://www.ecfr.gov/current/title-12/part-220)), commonly 50% for equities. FINRA maintenance and pattern-day-trader rules ([FINRA 4210](https://www.finra.org/rules-guidance/rulebooks/finra-rules/4210)), including the $25k PDT minimum equity.
- **Short sales under Reg SHO** ([17 CFR 242.200–204](https://www.ecfr.gov/current/title-17/part-242)): locate (Rule 203(b)), close-out of fails (204) and the short-sale price-test circuit breaker (201).
- **Communications ([FINRA 2210](https://www.finra.org/rules-guidance/rulebooks/finra-rules/2210)).** The three classes are correspondence, retail and institutional. Content must be fair and balanced. Projections are prohibited except in narrow cases. Many retail communications need principal pre-approval.
- **Packaged products.** Mutual fund share classes, breakpoints and rights of accumulation; variable annuity rules ([FINRA 2330](https://www.finra.org/rules-guidance/rulebooks/finra-rules/2330)).
- **Fixed income.** Yield measures, duration intuition, munis (MSRB rules) and the yield curve.
- **Fair prices and best execution.** Markups ([FINRA 2121](https://www.finra.org/rules-guidance/rulebooks/finra-rules/2121)) and best execution ([FINRA 5310](https://www.finra.org/rules-guidance/rulebooks/finra-rules/5310)).
- **Confirmations and records.** Trade confirmations (Exchange Act Rule 10b-10) and books and records (Rules 17a-3 and 17a-4).

**How it maps to the desk:** the **suitability/profile engine** and **options approval levels** (§19) come from 2111, 2360 and Reg BI care. **Margin checks** come from Reg T and 4210, and **short-sale gating** from Reg SHO. The **communications linter** extends `tests/test_public_claims.py` under 2210. Wheel breakeven, maximum loss and return-on-collateral math belongs to the deterministic Quant lane, never an LLM.

## 3. Series 4 — Registered Options Principal (FINRA)

**Purpose:** supervises a firm's options business, including approving options accounts, reviewing options trading and approving options communications.
**Format** ([Series 4 page](https://www.finra.org/registration-exams-ce/qualification-exams/series4)): 125 items, 3 h 15 min, passing score 72. The SIE and Series 7 are corequisites.

| Function | Items | Weight |
|---|---|---|
| F1 Supervise opening of new options accounts | 21 | 16.8% |
| F2 Supervise options account activities | 25 | 20.0% |
| F3 Supervise general options trading | 30 | 24.0% |
| F4 Supervise options communications | 9 | 7.2% |
| F5 Implement practices / regulatory requirements | 12 | 9.6% |
| F6 Supervise associated persons / personnel | 28 | 22.4% |

**Key concepts an agent must know**
- **Account approval under 2360(b)(16):** a qualified principal approves or disapproves in writing; background and financial data go to the customer for verification within 15 days of approval, and the signed options agreement is also due within 15 days.
- **Uncovered writing** needs written suitability criteria, a minimum net-equity standard set by the firm (the rule sets no dollar figure), and a special risk statement delivered before the first uncovered short sale.
- **Options suitability (2360(b)(19)).** The firm needs a reasonable basis to believe the customer understands the risk and can bear the loss.
- **Supervision (2360(b)(20)).** Written supervisory procedures under [FINRA 3110](https://www.finra.org/rules-guidance/rulebooks/finra-rules/3110), 3120 and 3130. Head-office review of each account for suitability, trading size and frequency, concentration, P&L and Reg T compliance.
- **Options records (2360(b)(17)).** A central complaint log, and customer background data kept at both the branch and the supervisory office.
- **Position and exercise limits; large options position reporting.** Conventional equity options have a default limit of 25,000 contracts, with higher tiers for qualifying underlyings (2360(b)(3)).
- **Options communications.** Retail options communications must not be shown to a customer before they receive the ODD, unless an exception applies. Options worksheets and projections are covered by 2220/2210.
- **Exchange rules.** Exercise cut-offs, early assignment, adjustments for corporate actions, and OCC's role as issuer and guarantor.

**How it maps to the desk:** the **principal-approval pattern** the Engineering Map already names (row "Series 4"); this section adds the concrete pieces. Encode an **options approval level** field on the profile, a **principal gate** only a human can clear, an **exception log** for every override request, and deterministic **activity surveillance** (turnover, concentration, drawdown).

## 4. Series 9/10 — General Securities Sales Supervisor (FINRA)

**Current status:** active. It is still delivered as two parts, Series 9 (options) and Series 10 (general). The page carries no retirement notice ([Series 9/10 page](https://www.finra.org/registration-exams-ce/qualification-exams/series9-10)). The SIE and Series 7 are corequisites.

| Exam | Items | Time | Pass |
|---|---|---|---|
| Series 9 | 55 | 1 h 30 min | 70 |
| Series 10 | 145 | 4 h | 70 |

**Content (items):** Series 10 covers supervising associated persons (28), opening and maintaining customer accounts (49), sales practices and general trading (52), and communications with the public (16). Series 9 covers options accounts (18), options sales practices and trading (19), options communications (5), and associated persons (13).

**Key concepts:** branch-level supervision under 3110; review of correspondence and retail communications under 2210; and red flags in trading such as excessive trading, concentration and unsuitable options strategies. Under 2360, this registration can also approve options accounts.
**Desk mapping:** the **Supervisor** role's daily review queue. Every flagged candidate and every exception needs a recorded reviewer and a timestamp.

## 5. Series 24 — General Securities Principal (FINRA)

**Format** ([Series 24 page](https://www.finra.org/registration-exams-ce/qualification-exams/series24)): 150 items, 3 h 45 min, passing score 70. The SIE plus a representative exam (Series 7, 57, 79, 82 or 86/87) or the Series 16 is a corequisite.

| Function | Items | Weight |
|---|---|---|
| F1 Registration of broker-dealer and personnel management | 9 | 6.0% |
| F2 General broker-dealer activities | 45 | 30.0% |
| F3 Retail and institutional customer-related activities | 32 | 21.3% |
| F4 Trading and market-making activities | 32 | 21.3% |
| F5 Investment banking and research | 32 | 21.3% |

**Key concepts**
- **Supervision.** The supervisory system and written supervisory procedures ([3110](https://www.finra.org/rules-guidance/rulebooks/finra-rules/3110)), annual testing and the CEO certification ([3120](https://www.finra.org/rules-guidance/rulebooks/finra-rules/3120) and [3130](https://www.finra.org/rules-guidance/rulebooks/finra-rules/3130)).
- **Registration and continuing education.** Form U4/U5 and the CE requirement ([FINRA 1240](https://www.finra.org/rules-guidance/rulebooks/finra-rules/1240)).
- **Market access controls ([17 CFR 240.15c3-5](https://www.ecfr.gov/current/title-17/section-240.15c3-5)).** Pre-trade credit and capital thresholds, erroneous-order checks and regulatory checks, all under the firm's direct and exclusive control.
- **Net capital and customer protection.** Net capital (Rule 15c3-1) and the customer protection reserve (Rule 15c3-3), at a conceptual level.
- **Books and records.** Rule 17a-4 retention periods, including the 2022 amendments on electronic records ([17 CFR 240.17a-4](https://www.ecfr.gov/current/title-17/section-240.17a-4)).
- **Research and banking.** Research analyst conflicts ([FINRA 2241](https://www.finra.org/rules-guidance/rulebooks/finra-rules/2241)), Regulation AC, and the conduct of offerings.
- **Trading.** Trade reporting, OATS→CAT, best execution and regular reviews of execution quality (5310), and manipulation surveillance.
- **Business continuity and outsourcing.** Business continuity planning ([FINRA 4370](https://www.finra.org/rules-guidance/rulebooks/finra-rules/4370)) and vendor oversight.

**Desk mapping:** the **Supervisor/Principal** role and the **ORCHESTRATOR**'s governance controls. That covers written policies kept as code (AGENTS.md, SOUL.md), the hash-chained audit trail, and the kill switch (a 15c3-5 *analogue*, never described as compliance).

## 6. Series 57 — Securities Trader (FINRA)

**Format** ([Series 57 page](https://www.finra.org/registration-exams-ce/qualification-exams/series57)): 50 items, 1 h 45 min, passing score 70. The SIE is a corequisite.

| Function | Items | Weight |
|---|---|---|
| F1 Trading activities | 41 | 82% |
| F2 Books and records, trade reporting, clearance and settlement | 9 | 18% |

**Key concepts**
- **Order handling.** Limit-order display and protection (Reg NMS Rules 610/611), and customer limit-order protection ([FINRA 5320](https://www.finra.org/rules-guidance/rulebooks/finra-rules/5320)).
- **Best execution and fair prices** (5310 and 2121).
- **Short sales.** Reg SHO locate and close-out requirements, and marking orders long, short or short-exempt.
- **Halts and limits.** Trading halts, LULD bands and market-wide circuit breakers.
- **Trade reporting** to TRF/ORF/ADF and CAT reporting, both conceptually.
- **Prohibited practices.** Manipulative practices (wash trades, marking the close, spoofing) and front-running (5270).

**Desk mapping:** the **Trader/Execution** lane is research-only, with no order placement (CLAUDE.md, AGENTS.md). It uses this knowledge to *describe* execution quality for the GP (spread, size, price versus NBBO) and to flag illiquid option chains, such as a wide bid/ask spread or low open interest, in the Cboe adapter's validation.

## 7. Futures exams (NFA, administered by FINRA): Series 3, 30, 34

| Exam | Who needs it | Format |
|---|---|---|
| **Series 3** (National Commodity Futures) | Associated persons (APs) of an FCM, IB, CPO or CTA, and others joining NFA ([NFA proficiency](https://www.nfa.futures.org/registration-membership/how-to-register/proficiency-requirements.html)) | 120 questions in two parts, 2 h 30 min, 70% on each part ([FINRA Series 3 page](https://www.finra.org/registration-exams-ce/qualification-exams/series3)). Content-area weights are **unverified** (FINRA points to NFA's study outline). |
| **Series 30** (NFA Branch Manager) | Branch office managers of NFA members | 50 questions, 1 h, 70% ([Series 30 page](https://www.finra.org/registration-exams-ce/qualification-exams/series30)) |
| **Series 34** (Retail Off-Exchange Forex) | Firms and APs doing off-exchange retail forex. Series 3 or 32 must come first | 40 questions, 60 min, 70% ([Series 34 page](https://www.finra.org/registration-exams-ce/qualification-exams/series34)) |

**Key concepts:** futures margin is a performance bond, not Reg T credit, and positions are marked to market daily; hedging versus speculation and basis; CFTC/NFA customer segregation and the risk disclosure statement; position limits and large-trader reporting; retail forex leverage limits.

**Desk mapping:** relevant only if the GP ever asks for futures research. Today futures and forex are **out of scope**, and the strategy gate below denies them by default.

## 8. Series 63 — Uniform Securities Agent State Law (NASAA)

**Purpose:** state ("blue-sky") registration for agents of broker-dealers. Most states require it on top of the FINRA exams ([NASAA FAQs](https://www.nasaa.org/exams/exam-faqs/)).
**Format** ([FINRA Series 63 page](https://www.finra.org/registration-exams-ce/qualification-exams/series63)): 60 scored plus 5 unscored questions, 75 min, passing score 43 of 60.
**Outline**, effective 2023-06-12 ([NASAA Series 63 outline](https://www.nasaa.org/wp-content/uploads/2023/02/Series-63-Outline-June-2023.pdf)):

| Section | Weight | Items |
|---|---|---|
| I Regulation of investment advisers | 5% | 3 |
| II Regulation of IA representatives | 5% | 3 |
| III Regulation of broker-dealers | 12% | 7 |
| IV Regulation of agents of broker-dealers | 13% | 8 |
| V Regulation of securities and issuers | 9% | 5 |
| VI Remedies and administrative provisions | 11% | 7 |
| VII Communication with customers and prospects | 20% | 12 |
| VIII Ethical practices and obligations | 25% | 15 |

**Key concepts:**
- **Uniform Securities Act**, 1956 or 2002 version depending on the state: definitions (person, agent, broker-dealer, security), registration by coordination, qualification or notice filing, and exempt securities and transactions.
- **State administrator powers** (stop orders, subpoenas, denial, suspension, revocation), plus civil liability and rescission.
- **NASAA unethical-practices statements** for broker-dealers and agents, e.g. unsuitable recommendations, unauthorized trading, misleading advertising, sharing in client accounts.
- **Cybersecurity and data protection** expectations.

**Desk mapping:** the **Compliance** lane's state-law overlay. The comms linter treats NASAA unethical-practice categories as additional prohibited patterns.

## 9. Series 65 — Uniform Investment Adviser Law (NASAA)

**Purpose:** qualifies investment adviser representatives (IARs), people who give advice for compensation. No sponsorship is needed.
**Format** ([FINRA Series 65 page](https://www.finra.org/registration-exams-ce/qualification-exams/series65)): 130 scored plus 10 unscored questions, 180 min, passing score 92 of 130. NASAA stresses that this pass mark is a raw count, not a percentage ([NASAA FAQs](https://www.nasaa.org/exams/exam-faqs/)).
**Outline**, effective 2023-06-12 ([NASAA Series 65 outline](https://www.nasaa.org/wp-content/uploads/2023/02/Series-65-Outline-June-2023.pdf)):

| Section | Weight | Items |
|---|---|---|
| I Economic factors and business information | 15% | 20 |
| II Investment vehicle characteristics | 25% | 32 |
| III Client investment recommendations and strategies | 30% | 39 |
| IV Laws, regulations and guidelines, including prohibition on unethical business practices | 30% | 39 |

**Key concepts:**
- **Advisers Act fiduciary duty** under Section 206 (antifraud): duties of care and loyalty, with full and fair disclosure of conflicts.
- **The Marketing Rule** ([17 CFR 275.206(4)-1](https://www.ecfr.gov/current/title-17/section-275.206(4)-1)): testimonials, endorsements and hypothetical performance.
- **Custody** (206(4)-2), **books and records** (204-2), and **Form ADV** Parts 1 and 2 (the brochure).
- **Federal-covered versus state-registered advisers**, and the exclusions from the adviser definition.
- **Portfolio theory and returns:** MPT, beta, Sharpe ratio, standard deviation, CAPM, efficient markets; time-weighted versus dollar-weighted returns.
- **Tax, retirement and profiling:** account and plan taxation (IRAs, 401(k), ERISA prudence), client profiling and asset allocation.

**Desk mapping:** the **Research/Quant** methodology layer (portfolio statistics) and the **Compliance** layer (no hypothetical performance shown as real, in line with SOUL.md rule 2). Hypothetical-performance restrictions are the strongest public-rule basis for the desk's "never claim performance" rule.

## 10. Series 66 — Uniform Combined State Law (NASAA)

**Purpose:** a combined state-law exam for agents and IARs. Paired with the Series 7, it stands in for the 63 and 65.
**Format** ([FINRA Series 66 page](https://www.finra.org/registration-exams-ce/qualification-exams/series66)): 100 scored plus 10 unscored questions, 150 min, passing score 73 of 100. The SIE and Series 7 are corequisites.
**Outline**, effective 2023-06-12 ([NASAA Series 66 outline](https://www.nasaa.org/wp-content/uploads/2023/02/Series-66-Outline-June-2023.pdf)):

| Section | Weight | Items |
|---|---|---|
| Economic factors and business information | 8% | 8 |
| Investment vehicle characteristics | 17% | 17 |
| Client/customer investment recommendations and strategies | 30% | 30 |
| Laws, regulations, guidelines and unethical practices | 45% | 45 |

**Key concepts:** the union of §8 and §9, weighted toward law and ethics. Main topics: dual registrants, and where broker-dealer duties and adviser duties overlap and where they part.
**Desk mapping:** same as §8 and §9. Its practical use is the **standard-of-care switch**: the record must say whether a (hypothetical) recommendation would fall under Reg BI or under the Advisers Act fiduciary duty.

## 11. Series 86/87 — Research Analyst (FINRA)

**Format** ([Series 86/87 page](https://www.finra.org/registration-exams-ce/qualification-exams/series86-87)): the SIE is a corequisite.
- **Series 86:** 85 items, 4 h 30 min, passing score 73. Candidates who have passed CFA Levels I and II, or the CMT equivalent, may request an exemption.
- **Series 87:** 50 items, 1 h 45 min, passing score 74.

| Part | Function | Items | Weight |
|---|---|---|---|
| 86 | F1 Information and data collection | 18 | 21.2% |
| 86 | F2 Analysis, modeling and valuation | 28 | 32.9% |
| 86 | F3 Valuation and forecasting | 39 | 45.9% |
| 87 | F4 Preparation of research reports | 36 | 72.0% |
| 87 | F5 Dissemination of information | 14 | 28.0% |

**Key concepts:**
- **Data and valuation:** sourcing and validating SEC filings (10-K/10-Q/8-K), financial-statement analysis, DCF, multiples, sum-of-parts, and sector and macro inputs.
- **Research disclosures ([FINRA 2241](https://www.finra.org/rules-guidance/rulebooks/finra-rules/2241)):** ratings definitions and distribution, price-target basis and risks, and conflicts (ownership, compensation, banking).
- **Regulation AC** analyst certification ([17 CFR 242.500–505](https://www.ecfr.gov/current/title-17/part-242)).
- **Information barriers:** quiet periods and Reg FD ([17 CFR 243](https://www.ecfr.gov/current/title-17/part-243)) on selective disclosure.

**Desk mapping:** the **Research (Muse)** lane. Every claim is sourced; every price target or valuation states its reasonable basis and key risks; conflicts are disclosed; research is labeled input, not a recommendation (SOUL.md rule 3).

## 12. Series 16 — Supervisory Analyst (brief)

**Format** ([Series 16 page](https://www.finra.org/registration-exams-ce/qualification-exams/series16)): two parts of 50 items each. Part 1 is 1 h 30 min with passing score 72. Part 2 is 2 h with passing score 74. There is no corequisite.

**Content:** Part 1 covers approving research communications for compliance (34 items) and liaison between research and other parties (16). Part 2 covers accuracy, consistency and sourcing of data and calculations (16) and the reasonable basis for ratings and price targets (34).

**Desk mapping:** the **independent reviewer** of Muse output. This is the public-rule basis for SOUL.md's peer-review rule: research gets approved by someone other than its author.

## 13. CFA Program: format and recent changes

Every level now needs one **Practical Skills Module (PSM)** before the exam result is released. A module cannot be reused at a second level ([Level I page](https://www.cfainstitute.org/programs/cfa-program/candidate-resources/level-i-exam); for Level III this has applied since February 2025, per the [Level III page](https://www.cfainstitute.org/programs/cfa-program/candidate-resources/level-iii-exam)).
- Named PSMs include Python Programming Fundamentals; Python, Data Science & AI; Analyst Skills; Equity Analysis; and Macro Insights for Investing.
- A Due Diligence PSM for Level III was announced for later in 2026 ([press release](https://www.cfainstitute.org/about/press-room/2026/cfa-institute-announces-updates-to-cfa-program-curriculum)).

## 14. CFA Level I

**Format:** 180 multiple-choice questions in two sessions of 90 questions, each about 135 min ([Level I page](https://www.cfainstitute.org/programs/cfa-program/candidate-resources/level-i-exam)). The passing score is not published (**unverified / not disclosed**).

| Topic (2026 name → 2027 name) | 2026 | 2027 |
|---|---|---|
| Ethical and Professional Standards | 15–20% | 10–15% |
| Quantitative Methods | 6–9% | 11–14% |
| Economics | 6–9% | 6–9% |
| Financial Statement Analysis | 11–14% | 11–14% |
| Corporate Issuers → Corporate Finance | 6–9% | 6–9% |
| Equity Investments → Equities | 11–14% | 11–14% |
| Fixed Income | 11–14% | 11–14% |
| Derivatives → Derivatives and Risk Management | 5–8% | 6–9% |
| Alternative Investments | 7–10% | 6–9% |
| Portfolio Management → Portfolio Construction | 8–12% | 8–12% |

**What 2027 adds:** simulation methods (historical simulation, bootstrapping, Monte Carlo), more portfolio optimization, a reading on financial data science and AI/LLMs, CAPM and multi-factor approaches to the cost of equity, scenario-weighted forecasting, and modules on writing equity research reports ([curriculum update 2027](https://www.cfainstitute.org/sites/default/files/curriculum-update-2027.pdf)).

## 15. CFA Level II

**Format:** 22 item sets of 4 questions each (88 questions). 4 h 24 min in two sessions. 20 sets are scored and 2 are unscored trial sets ([Level II page](https://www.cfainstitute.org/programs/cfa-program/candidate-resources/level-ii-exam)).
**Weights:** the page lists one table and does not label it by year. It uses the 2027 topic names.

| Topic | Weight |
|---|---|
| Quantitative Methods | 5–10% |
| Economics | 5–10% |
| Financial Statement Analysis | 10–15% |
| Corporate Finance | 5–10% |
| Equities | 10–15% |
| Fixed Income | 10–15% |
| Derivatives and Risk Management | 5–10% |
| Alternative Investments | 5–10% |
| Portfolio Construction | 10–15% |
| Ethical and Professional Standards | 10–15% |

Whether the 2026 and 2027 Level II weights differ is **unverified**. The year-specific PDFs were not read.

## 16. CFA Level III and the pathways

**Format:** 11 item sets and 11 essay (constructed-response) sets, each worth 12 points. 20 sets are scored. 4 h 24 min in two sessions ([Level III page](https://www.cfainstitute.org/programs/cfa-program/candidate-resources/level-iii-exam)).

| Core / pathway | Weight |
|---|---|
| Asset Allocation | 15–20% |
| Portfolio Construction | 15–20% |
| Performance Measurement | 5–10% |
| Derivatives and Risk Management | 10–15% |
| Ethical and Professional Standards | 10–15% |
| Chosen pathway | 30–35% |

All three pathways are current, with outlines published for 2026 and 2027: **Portfolio Management** (index and active equity, fixed-income strategies, trade execution, case study); **Private Wealth** (business models, ultra-high-net-worth clients, goals-based planning, risk mitigation, wealth transfer); **Private Markets** (private equity, private debt, special situations, real estate, infrastructure).

**Desk mapping:**
- Level I/II quant, fixed income and derivatives feed **Quant** (pricing, Greeks, duration). FSA and equities feed **Research**.
- Level III asset allocation, performance measurement and derivatives/risk management feed **Risk**. Paper results are never presented as real returns (SOUL.md). Risk of Ruin stays with its separately versioned component; CFA material informs review of it and never lets an agent compute RoR.
- Trade execution (PM pathway) feeds the execution-quality descriptions in §6.

## 17. CFA Institute Code of Ethics and Standards of Professional Conduct (own-words summary)

The current Code took effect 2024-01-01. The governing interpretation is the **Standards of Practice Handbook, 12th edition (2024)**; the 11th edition is superseded ([CFA Code & Standards](https://www.cfainstitute.org/standards/professionals/code-ethics-standards)).

**Code (summary in our words).** Act with integrity and competence. Put clients' interests and the integrity of the profession ahead of your own. Use reasonable care and independent judgment. Practise professionally and encourage others to. Support capital-market integrity. Keep building your competence.

**Standards (structure as published, with our gloss):**
- **I Professionalism:** (A) know and obey the law, following the stricter rule where law and Standards differ; (B) independence and objectivity, refusing gifts that could compromise judgment; (C) no misrepresentation, including plagiarism; (D) no dishonest conduct; (E) competence, added in the 2024 revision.
- **II Integrity of capital markets:** (A) do not act on, or cause others to act on, material nonpublic information; (B) no price or volume manipulation.
- **III Duties to clients:** (A) loyalty, prudence and care; (B) fair treatment when disseminating information and allocating trades; (C) suitability, meaning understand the client and keep an investment policy statement current; (D) fair and complete performance presentation; (E) confidentiality.
- **IV Duties to employers:** (A) loyalty; (B) disclose and get consent for outside compensation; (C) supervisors make reasonable efforts to prevent and detect violations.
- **V Investment analysis, recommendations and actions:** (A) diligence and a reasonable basis; (B) communicate process, risks and limitations, and separate fact from opinion; (C) keep records that support the analysis.
- **VI Conflicts of interest:** (A) disclose conflicts; (B) client and employer transactions come before personal ones; (C) disclose referral fees.
- **VII Members and candidates:** (A) conduct in the program; (B) proper reference to the designation.

**Desk mapping:** V(B) becomes a required schema field, with each Muse claim typed `fact|estimate|opinion` and every fact carrying a source. V(A) and V(C) become provenance plus reason codes (AGENTS.md). III(D) becomes the linter rule against misleading performance. II(A) means the desk takes in no non-public data. IV(C) is the Supervisor's duty.

## 18. Overlap with `hedge-desk/docs/compliance/FINRA_ENGINEERING_MAP.md`

The Engineering Map already covers the SIE, Series 7 and Series 4 at a high level, plus rules 15c3-5, 2210, 3110, 17a-4, Reg D 501, ICA 2(a)(51) and Reg BI. This baseline **extends** it with official formats and weights; with Rules 2111, 2360 (paragraph citations), 4512, 4210/Reg T, Reg SHO, 5310, 2241, Reg AC, CIP/CDD, the Advisers Act Marketing Rule and NASAA state law; and by turning the Series 4 principal-approval pattern into concrete fields (§19).

It **does not change** the Map's two conclusions: software cannot register a person, and a control must never be described as compliance. One item to reconcile: the Map treats Reg BI as dormant. §19 keeps it dormant too. The profile schema is a *design-ready* model, and every strategy decision remains `trade_authorized=False`.

## 19. Suitability / investor profile model (design schema, not implemented)

**Basis:** FINRA 2111(a) profile factors; FINRA 4512(a) account-record items; SEA Rule 17a-3(a)(17) income, net-worth and objectives records (exact field list **unverified** here); the Reg BI care obligation (reasonable basis, customer-specific, series of recommendations); FINRA 2360(b)(16)/(19) options profile items, principal approval, the ODD and uncovered-writing rules.

**Scope today.** The GP is the only user. AGENTS.md says the desk takes in only a watchlist, never brokerage account data. So this profile is a **self-declared GP policy profile**: hand-entered configuration that is versioned and reviewed. It is never pulled from a broker. Decimal is used for money and ratios.

```yaml
InvestorProfile:            # versioned; every change appended to audit trail (3110/17a-4 shape)
  profile_id: str
  version: int
  effective_at: datetime    # fixed clock in tests
  # --- 2111(a) factors ---
  age_band: enum [UNDER_30, 30_44, 45_59, 60_74, 75_PLUS]   # band, not DOB (no PII)
  tax_status: enum [TAXABLE, TAX_DEFERRED, TAX_EXEMPT]
  investment_objective: enum [CAPITAL_PRESERVATION, INCOME, GROWTH_AND_INCOME, GROWTH, SPECULATION]
  risk_tolerance: enum [CONSERVATIVE, MODERATE, AGGRESSIVE, SPECULATIVE]
  time_horizon: enum [LT_1Y, Y1_3, Y3_10, GT_10Y]
  liquidity_needs: enum [HIGH, MEDIUM, LOW]
  financial_situation:
    annual_income_band: enum [LT_50K, 50_100K, 100_250K, 250K_1M, GT_1M]
    net_worth_ex_residence: Decimal     # 2360(b)(16) excludes family residence
    liquid_net_worth: Decimal
    dependents: int                      # 2360(b)(16) item
  other_investments_summary: str        # free text, no account identifiers
  investment_experience:                # 2360(b)(16): options, stock, bond, other
    stocks:  {years: int, level: enum [NONE, LIMITED, GOOD, EXTENSIVE]}
    bonds:   {years: int, level: ...}
    options: {years: int, level: ...}
    futures: {years: int, level: ...}
  additional_disclosed_info: str        # 2111(a) catch-all
  # --- 4512 analogues (non-PII) ---
  trusted_contact_on_file: bool          # 4512(a)(1)(F); contact details NOT stored here
  responsible_reviewer: str              # role id of supervising principal
  # --- account capabilities (self-declared, mirrors broker approvals) ---
  account_type: enum [CASH, MARGIN, IRA_CASH, IRA_LIMITED_MARGIN]
  options_level: enum [L0_NONE, L1_COVERED, L2_LONG_AND_SECURED, L3_SPREADS, L4_UNCOVERED_EQUITY, L5_UNCOVERED_INDEX_AND_CALLS]
  options_level_source: str              # e.g. "broker approval letter dated …" (no account number)
  odd_acknowledged_at: datetime|null     # 2360(b)(16) ODD delivery analogue
  uncovered_risk_statement_ack_at: datetime|null  # 2360 special statement
  short_selling_enabled: bool
  futures_enabled: bool                  # default false; out of scope
  # --- desk-wide immutable limits ---
  max_loss_pct_equity: Decimal = 0.02    # SOUL.md rule 7, immutable
  principal_approval:
    approved_by: str                     # human only; agent ids rejected
    approved_at: datetime
    reason_codes: [str]
```

**Generic options levels** (our mapping; firms differ): L1 covered calls and protective puts; L2 adds long calls/puts and cash-secured puts; L3 adds defined-risk spreads, condors, butterflies; L4 uncovered equity puts; L5 uncovered calls and uncovered index options. Public examples of variation: [TradeStation](https://help.tradestation.com/10_00/eng/tradestationhelp/elanalysis/row/option_approval_level_row_.htm) uses Levels 0–5, with naked equity puts at 4 and naked calls/index puts at 5; [Fidelity](https://www.fidelity.com/options-trading/faqs) uses 3 tiers and allows cash-covered puts at Tier 1. So the profile stores the firm's own level as well as our normalized enum.

**Strategy gate.** Every condition must pass; any failure DENIES with reason codes. A pass yields a `RESEARCH_ELIGIBLE` label, never an order, and `trade_authorized=False` always.

| Strategy | Min level | Account | Profile conditions (all) | Extra checks |
|---|---|---|---|---|
| Covered call | L1 | any | objective ≠ CAPITAL_PRESERVATION, or covered-call-for-income explicitly allowed | Shares are held (self-declared). Flag early-assignment and dividend risk |
| Cash-secured put (the GP's wheel) | L2* | CASH ok | objective ∈ {INCOME, GROWTH_AND_INCOME, GROWTH}; liquidity ≠ HIGH | Collateral = strike × 100 × contracts (Decimal). Maximum loss at expiry, (strike − premium) × 100, must fit the 2% rule *at the position-sizing layer*. Show return on collateral. DTE 30–45 and ~10% OTM per SOUL.md rule 8. Not allowed on delayed-only data, so no probability claims |
| Long call/put | L2 | any | risk_tolerance ≥ MODERATE; options experience ≥ LIMITED | Premium at risk ≤ 2% of equity |
| Debit/credit vertical, iron condor | L3 | MARGIN (or a firm cash-spread rule) | risk ≥ MODERATE; options experience ≥ GOOD | Defined maximum loss = width − credit, which must be ≤ 2% of equity. Check bid/ask width |
| Uncovered put (naked) | L4 | MARGIN | risk ≥ AGGRESSIVE; options experience ≥ GOOD; `uncovered_risk_statement_ack_at` set; firm minimum equity met | Margin estimate is labeled *estimate*. Gap-risk flag |
| Uncovered call / naked index | L5 | MARGIN | risk = SPECULATIVE; experience EXTENSIVE; statement acknowledged | **Default DENY.** Unlimited loss cannot fit a fixed 2% cap without a stop, so the desk denies it unless the GP explicitly changes policy, and that change goes through human review |
| Short stock | n/a | MARGIN; `short_selling_enabled` | risk ≥ AGGRESSIVE | Reg SHO locate is the broker's job (flag only). Hard-to-borrow and borrow-fee flags. Unlimited-loss handling as above |
| Futures / forex | n/a | futures account | `futures_enabled` | **Out of scope: DENY** (§7) |

\* Some firms put cash-secured puts at their lowest level (Fidelity Tier 1). The gate uses whichever level the GP declares, mapped to our enum.

Reason codes, in the existing desk style:
`LEVEL_INSUFFICIENT`, `ACCOUNT_TYPE_MISMATCH`, `OBJECTIVE_MISMATCH`, `RISK_TOLERANCE_LOW`,
`EXPERIENCE_LOW`, `ODD_NOT_ACKNOWLEDGED`, `UNCOVERED_STATEMENT_MISSING`, `MAX_LOSS_EXCEEDS_2PCT`,
`UNDEFINED_RISK_DENIED`, `DATA_DELAYED_NO_PROBABILITY`, `OUT_OF_SCOPE_FUTURES`, `PROFILE_STALE`.

A profile older than a review interval set by the GP gives `PROFILE_STALE`. The interval is unspecified until the GP sets it.

**Ownership:** RISK owns the gate as deterministic code with reference cases. COMPLIANCE reviews the mapping. The gate is a risk control, so per AGENTS.md the agent that implements it may not approve it.

## 20. Agent curriculum

| Desk role | Core exam knowledge | Rules it must encode / respect | CFA material |
|---|---|---|---|
| **Research (Muse)** | SIE; Series 86/87; Series 16 (as reviewee) | 2241, Reg AC, Reg FD, 2210 (fair and balanced), MNPI ban | L1/L2 FSA, Equities, Economics; Standards V(A), V(B), II(A) |
| **Quant** | Series 7 options math; Series 65 portfolio statistics | Decimal money, deterministic reference cases; no probability claims on delayed data | L1/L2 Quant, Fixed Income, Derivatives; L3 Performance Measurement |
| **Risk** | Series 4 (2360 account and uncovered rules); Series 7 margin and Reg SHO | 2111 / Reg BI care (profile gate), Reg T / 4210, 2% rule; consumes RoR only | L3 Derivatives and Risk Management, Asset Allocation; III(C) |
| **Compliance** | Series 24; Series 63/65/66; Series 9/10 communications | 2210, NASAA unethical practices, Marketing Rule (no hypothetical performance), CIP/CDD/AML concepts, 17a-4 | Standards I, III(D), VI |
| **Trader / Execution (descriptive only)** | Series 57; Series 7 F4 | 5310, 5320, Reg NMS, LULD/halts; **no order placement** | L3 PM pathway: trade execution |
| **Back office / Data** | SIE; Series 57 F2; Series 24 records | 17a-3/17a-4 shape, audit trail, T+1, data provenance and freshness (CarpeDATA) | Standard V(C) record retention |
| **Supervisor / Principal (human GP; agents only prepare queues)** | Series 24, 4, 9/10, 16 | 3110/3120 review and exception log; principal approval of options-level changes and public copy; independent review | Standards IV(C), I(B) |
| **Futures (dormant)** | Series 3/30/34 | CFTC/NFA disclosures | none |

**Reminder:** this knowledge base never lets an agent claim to hold a licence, give a recommendation, or authorize a trade.
