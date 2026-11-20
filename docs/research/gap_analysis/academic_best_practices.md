# AI/ML and LLM Agents in Investing: Best-Practice Baseline (for Emporion / hedge-desk)

Compiled 2026-11-19. Research input only; this does not authorize trades and makes no performance claim.
It covers academic, institutional, regulatory and practitioner sources, including work from 2024 to 2026.

**Evidence tiers**
- **A:** peer-reviewed, NBER, or top journal.
- **B:** arXiv/SSRN preprint, or a white paper from an institution or regulator.
- **C:** practitioner talk, book, blog or podcast.
- **D:** community discussion (Reddit, YouTube). D-tier sources show what people practice and think. They are never evidence of performance.

**Method and honesty notes**
- I checked every paper title, author list and venue below on arXiv, SSRN, NBER, RePEc, the journal page or the publisher page.
- When a summary depends only on an abstract or a secondary page, the entry says so.
- **Reddit:** Reddit itself was blocked from this environment, and so was a Reddit mirror. I could not read any thread, so D-tier Reddit items are thread titles that appeared in search results.
- **YouTube:** `site:youtube.com` searches returned no YouTube URLs. Talks are cited from their host pages (CFA Institute, podcast pages) instead.
- **Withdrawn paper:** Kim, Muhn & Nikolaev's GPT financial-statement paper was **withdrawn** on arXiv (v3, 20 Feb 2025). Treat its results as unverified (see §2).

---

## 1. ML in asset pricing: the academic core (mostly tier A)

| Work | Tier | What it found (paraphrased) | Actionable practice |
|---|---|---|---|
| Gu, Kelly & Xiu, "Empirical Asset Pricing via Machine Learning," *RFS* 33(5), 2020 ([RePEc](https://econpapers.repec.org/RePEc:oup:rfinst:v:33:y:2020:i:5:p:2223-2273.); [NBER w25398](https://nber.org/papers/w25398)) | A | Trees and neural nets did best. Their gains came from nonlinear interactions between predictors. Every method ranked momentum, liquidity and volatility variants as the main predictors. In some cases ML forecasts roughly doubled the performance of regression-based strategies. | Compare ML against a strong linear baseline. Report variable importance. Expect the gains to come from interactions, not from new exotic signals. |
| Kelly, Malamud & Zhou, "The Virtue of Complexity in Return Prediction," *JF* 79(1), 2024 ([SFI](https://www.sfi.ch/en/publications/the-virtue-of-complexity-in-return-prediction); [RePEc](https://econpapers.repec.org/RePEc:bla:jfinan:v:79:y:2024:i:1:p:459-503)) | A | Theory and US market evidence show that models with more parameters than observations can capture more return predictability than small models. | Complexity is not banned by default, but it must be paired with shrinkage/regularization and honest out-of-sample tests. This is in tension with the Arnott/Harvey "prefer simplicity" position (below), and both views should be on record. |
| Chen, Pelger & Zhu, "Deep Learning in Asset Pricing," *Management Science* 70(2), 2024 ([RePEc](https://econpapers.repec.org/RePEc:inm:ormnsc:v:70:y:2024:i:2:p:714-750); [SSRN](https://papers.ssrn.com/abstract=3350138)) | A | Uses no-arbitrage as the loss function, with adversarially chosen test assets and hidden macro states. Out of sample, it beat benchmarks on Sharpe ratio, explained variation and pricing errors. | Build economic constraints (no-arbitrage) into the objective instead of fitting pure forecasts. |
| Kelly & Xiu, "Financial Machine Learning," *Foundations and Trends in Finance* 13(3–4) ([now publishers](https://nowpublishers.com/article/Details/FIN-064); [NBER w31502](https://www.nber.org/system/files/working_papers/w31502/w31502.pdf)) | A | A survey of ML methods for return prediction, factor models and text. | Use it as the reference syllabus for any model choice. |
| Harvey, Liu & Zhu, "…and the Cross-Section of Expected Returns," *RFS* 29(1), 2016 ([RePEc](https://econpapers.repec.org/RePEc:oup:rfinst:v:29:y:2016:i:1:p:5-68.); [NBER w20592](https://nber.org/papers/w20592)) | A | With hundreds of factors already tested, a new factor should clear a t-ratio above 3.0, not 2.0. Most claimed findings in the field are likely false. | Raise the significance bar to t>3, or apply a multiple-testing correction, for every new signal. |
| Harvey & Liu, "Backtesting," *JPM* 2015 ([Duke PDF](https://people.duke.edu/~charvey/Research/Published_Papers/P120_Backtesting.PDF)) | A | Proposes "haircutting" backtested Sharpe ratios to account for multiple testing. | Never show a raw backtest Sharpe ratio without a haircut. |
| Bailey & López de Prado, "The Deflated Sharpe Ratio," *JPM* 40(5), 2014 ([SSRN](https://papers.ssrn.com/abstract=2460551)) | A | The DSR corrects a Sharpe ratio for selection bias from multiple testing and for non-normal returns. | Log the number of trials. Report DSR next to SR. |
| Bailey, Borwein, López de Prado & Zhu, "The Probability of Backtest Overfitting," *J. Computational Finance* ([Risk.net](https://www.risk.net/journal-of-computational-finance/2471206/the-probability-of-backtest-overfitting); [SSRN](https://papers.ssrn.com/abstract=2326253)) | A | Estimates the probability that a backtest is overfit, using combinatorially symmetric cross-validation (CSCV). Standard hold-out tests are unreliable for this. | Compute PBO before promoting any parameterized rule. |
| Arnott, Harvey & Markowitz, "A Backtesting Protocol in the Era of Machine Learning," *J. Financial Data Science* 1(1), 2019 ([Duke](https://scholars.duke.edu/publication/1518184); [SSRN](https://papers.ssrn.com/abstract=3275654)) | A | A 7-part checklist covering motivation, multiple testing, data, cross-validation, model dynamics, complexity and research culture. Key points: start from an economic hypothesis, ask who is on the other side of the trade, track every trial, don't tune a model on its live results, prefer simplicity, and judge researchers on their process ([Alpha Architect summary](https://alphaarchitect.com/protocol-to-prevent-quants-gone-wild/), C). | Adopt the 7 categories as the desk's research checklist. |
| López de Prado, "The 10 Reasons Most Machine Learning Funds Fail," *JPM* 2018 ([GARP PDF](https://www.garp.org/hubfs/Whitepapers/a1Z1W0000054x6lUAA.pdf)) | A | Pairs each pitfall with a fix: meta-strategy teams; feature importance instead of backtest-driven research; triple-barrier labels; meta-labeling (separate side from size); uniqueness weighting; purging and embargo in CV; combinatorial purged CV instead of a single walk-forward path; deflated Sharpe ratio and synthetic-data backtests. | These are the core techniques of *Advances in Financial Machine Learning* (Wiley, 2018). Implement purge/embargo first. |
| Wiecki, Campbell, Lent & Stauth, "All that Glitters Is Not Gold" (Quantopian, 2016) ([EconBiz](https://www.econbiz.de/Record/all-that-glitters-is-not-gold-comparing-backtest-and-out-of-sample-performance-on-a-large-cohort-of-trading-algorithms/10012903535)) | B | Across 888 algorithms, backtest Sharpe barely predicted out-of-sample Sharpe (R² < 0.025). Volatility and drawdown predicted better. More backtesting meant a bigger gap ([HedgeFundAlpha summary](https://hedgefundalpha.com/strategies/comparing-backtest-sample-performance-large-cohort-trading-algorithms/), C). | Count backtest iterations per idea. Weight risk metrics above backtest return. |

## 2. LLMs and text in finance (A/B)

**Return prediction from text**
- **Lopez-Lira & Tang, "Can ChatGPT Forecast Stock Price Movements? Return Predictability and Large Language Models"** ([arXiv 2304.07619](https://arxiv.org/abs/2304.07619), v6 Oct 2025; B).
  - GPT-4 headline scores predicted the post-news drift, most strongly for small stocks and negative news.
  - Forecasting ability rose with model size.
  - Strategy returns fell as LLM adoption spread, which the authors read as markets becoming more efficient. Practice: expect any LLM signal to decay.
- **Kim, Muhn & Nikolaev, "Financial Statement Analysis with Large Language Models"** (Chicago Booth; [arXiv 2407.17866](https://arxiv.org/abs/2407.17866v3); B, withdrawn).
  - Earlier versions claimed GPT-4 beat analysts at predicting the direction of earnings from anonymized statements.
  - v3 (20 Feb 2025) is **withdrawn**. A co-author identified inconsistencies in the data and analyses.
  - Do not cite it as evidence. It is also a reminder to check the version and retraction status of every source.
- **Wu et al., "BloombergGPT: A Large Language Model for Finance"** ([arXiv 2303.17564](https://arxiv.org/abs/2303.17564v1); B). A domain-specific LLM trained on a mixed financial and general corpus. Useful as background for "domain model vs. general model" decisions.
- **Islam et al., "FinanceBench"** ([arXiv 2311.11944](https://arxiv.org/abs/2311.11944v1); B).
  - GPT-4-Turbo with retrieval answered incorrectly or refused on 81% of a 150-question sample of financial questions about public filings.
  - Every model tested hallucinated.
  - Practice: ground every claim in a cited filing and verify numbers deterministically.

**Look-ahead bias in LLM backtests (key risk for any desk using LLMs on history)**
- **Glasserman & Lin, "Assessing Look-Ahead Bias in Stock Return Predictions Generated By GPT Sentiment Analysis"** ([arXiv 2309.17322](https://arxiv.org/abs/2309.17322); B).
  - Two separate biases: look-ahead (the model may know what happened after the news) and "distraction" (what it knows about the company skews its sentiment score).
  - Removing company identifiers improved in-sample results, especially for large firms.
  - Out of sample, look-ahead bias goes away but distraction can remain. Practice: anonymize entities.
- **Sarkar & Vafa, "Lookahead Bias in Pretrained Language Models"** (ICML 2025 DataWorld workshop; [ICML](https://icml.cc/virtual/2025/48685); B).
  - Provide direct tests for lookahead bias and found it in earnings-call risk prediction.
  - Prompting the model to ignore the future works poorly. Models trained only on text from before the test period are the fix.
- **He, Lv, Manela & Wu, "Chronologically Consistent Large Language Models"** (ChronoBERT/ChronoGPT; [arXiv 2502.21206](https://arxiv.org/abs/2502.21206v3); B).
  - Models trained only on text available at each date. In their news-to-returns test, lookahead bias was modest.
  - They caution that the size of the bias depends on the model and the application.
- **Practice:** for any LLM-derived historical signal, record the model's training cutoff. Treat results inside the training window as contaminated unless anonymized or produced by a point-in-time model.

**LLM trading agents and benchmarks (2024–2026)**

These are agent designs and benchmarks, mostly preprints (B).

| Work | Finding relevant to robustness |
|---|---|
| Xiao, Sun, Luo & Wang, "TradingAgents: Multi-Agents LLM Financial Trading Framework" ([arXiv 2412.20138](https://arxiv.org/abs/2412.20138)) | Role-based design: analysts, bull/bear researchers, traders, and a risk-management team. The abstract claims better return, Sharpe and drawdown than baselines, but over a short window. Useful as an architecture pattern, not as performance evidence. |
| FinMem ([arXiv 2311.13743](https://arxiv.org/abs/2311.13743v2)); FinCon ([arXiv 2407.06567](https://arxiv.org/html/2407.06567v2)); FinAgent, KDD 2024 ([arXiv 2402.18485](https://arxiv.org/abs/2402.18485v2)) | Agent designs built on layered memory, a manager–analyst hierarchy with verbal reinforcement, and multimodal tools. Their evaluations are short and cover few symbols. |
| Li et al., "INVESTORBENCH," ACL 2025 ([ACL Anthology](https://aclanthology.org/2025.acl-long.126)) | A benchmark for agent financial decision tasks. |
| Li, Kim, Cucuringu & Ma, "Can LLM-based Financial Investing Strategies Outperform the Market in Long Run?" (FINSABER; [arXiv 2505.07078](https://arxiv.org/abs/2505.07078?context=cs), KDD 2026 D&B) | Tested over about 20 years and 100+ symbols, previously reported LLM advantages shrank substantially. LLM strategies were too cautious in bull markets and took heavy losses in bear markets. The authors call for regime-aware risk controls rather than more framework complexity. |
| Chen et al., "StockBench" ([arXiv 2510.02209](https://arxiv.org/abs/2510.02209v1)) | Most LLM agents failed to beat buy-and-hold over multi-month windows. Scoring well on static finance knowledge tests did not translate into trading skill. |
| Qian et al. (incl. Lopez-Lira), "When Agents Trade" / Agent Market Arena ([arXiv 2510.11695](https://arxiv.org/abs/2510.11695)) | In live tests, the agent framework shaped behavior more than the choice of underlying LLM. |
| Yu, Li & You, "LiveTradeBench" ([arXiv 2511.03628](https://arxiv.org/abs/2511.03628?context=cs)) | 50-day live test of 21 LLMs. LMArena rank did not predict trading results, and static benchmarks missed real-world skill. |
| Yu et al., "Can AI Make Money in Crypto? Measuring the Gap from Backtests to Real Markets" ([arXiv 2609.34510](https://arxiv.org/pdf/2609.34510), Sep 2026) | Ran 32 methods through backtest, then paper trading, then live trading. 23 of 24 ML methods were profitable in backtest, but only 2 of 8 tested ML methods stayed profitable in paper trading. No deployed method beat buy-and-hold live. Paper trading tracked live results better than backtests did. |

**Takeaway**
- No peer-reviewed evidence (yet) shows that autonomous LLM trading agents reliably beat passive benchmarks after realistic evaluation.
- The best-supported LLM uses are text-to-signal features, research productivity, and summarization grounded in sources, all with deterministic checks.

## 3. Institutional and academic voices: what each stands for

| Voice | Tier | Actionable practice (sourced) |
|---|---|---|
| **Andrew Lo (MIT)** | C | LLMs can already give financial advice, but quality, ethics and fiduciary duty are unresolved. He expects finance-specific modules to be needed and adjusts tone to temper extreme investor sentiment ([MIT Sloan](https://mitsloan.mit.edu:443/ideas-made-to-matter/can-generative-ai-provide-trusted-financial-advice); Lo & Ross, "Can ChatGPT Plan Your Retirement?: Generative AI and Financial Advice," *Harvard Data Science Review*, per [Harvard GSAS](https://gsas.harvard.edu/news/can-chatgpt-plan-your-retirement)). Practice: keep a human fiduciary-style reviewer between LLM output and any decision. |
| **Bryan Kelly (Yale / AQR)** | A/C | Supports complex, well-regularized ML for return prediction (papers above). Talk: "The Virtue of Complexity in Financial Machine Learning," Swedish House of Finance podcast ([Player.fm](https://el.player.fm/series/swedish-house-of-finance-podcast/ai-machine-learning-in-finance-the-virtue-of-complexity-in-financial-machine-learning)). |
| **Campbell Harvey (Duke)** | A | Multiple-testing discipline: t>3, haircut Sharpe ratios, the backtesting protocol (above). |
| **Marcos López de Prado (Cornell / ADIA)** | A/C | Purged/embargoed CV, CPCV, meta-labeling, DSR/PBO (above). He also argues for causal inference beyond correlational factor models. Source: CFA Institute video, "Conversations with Frank Fabozzi featuring Marcos López de Prado," 18 Mar 2025 ([CFA Institute](https://rpc.cfainstitute.org/research/multimedia/2025/conversations-with-frank-fabozzi-featuring-marcos-lopez-de-prado)). |
| **Robert Shiller (Yale)** | A | CAPE/valuation ratios as a guide to long-horizon returns, not to timing: Campbell & Shiller, "Valuation Ratios and the Long-Run Stock Market Outlook: An Update" ([NBER w8221](https://www.nber.org/papers/w8221)). Under AGENTS.md, any Shiller-layer method must cite this exact source and must not be turned into a formula from an agent's interpretation. |
| **Aswath Damodaran (NYU Stern)** | C | AI is strongest at mechanical, rule-based work. Human valuation has an edge in "narrative plus numbers" and judgment. A "Damodaran Bot" was built by Vasant Dhar ([Musings on Markets, 28 Aug 2024](https://aswathdamodaran.substack.com/p/beat-your-bot-building-your-moat)). Practice: automate the mechanical parts of valuation and keep humans on the story and the assumptions. |
| **John Hull (Toronto)** | B | Cao, Chen, Hull & Poulos, "Deep Hedging of Derivatives Using Reinforcement Learning" ([arXiv 2103.16409](https://arxiv.org/abs/2103.16409v1)). Practice: test any ML for options hedging or pricing against classical Greeks-based benchmarks. |
| **Emanuel Derman (Columbia) & Paul Wilmott** | C | "The Financial Modelers' Manifesto" (Jan 2009): models are not the world; don't trade realism for elegance; state assumptions and known gaps; don't give users false confidence ([emanuelderman.com](https://emanuelderman.com/the-financial-modelers-manifesto/)). Practice: every model output carries its assumptions and limitations. |
| **Giuseppe Paleologo** | C | *The Elements of Quantitative Investing* (Wiley, 2025) ([Wiley-VCH](https://www.wiley-vch.de/en/areas-interest/finance-economics-law/the-elements-of-quantitative-investing-978-1-394-26545-9)). The book exists, but I did not review its content. It is listed as reading for factor-risk practice. |
| **Ernest Chan** | C | Medina & Chan, *Generative AI for Trading and Asset Management* (Wiley, 2025) ([Wiley-VCH](https://www.wiley-vch.de/en/areas-interest/finance-economics-law/generative-ai-for-trading-and-asset-management-978-1-394-26697-5)). The book exists, but I did not review its content. Separately, Chan has spoken on optimizing strategies without overfitting ([Quantopian archive](https://quantopian-archive.netlify.app/forum/threads/optimizing-trading-strategies-without-overfitting-by-dr-ernest-chan)). |
| **CFA Institute Research Foundation** | B | *AI in Asset Management: Tools, Applications, and Frontiers* (ed. Simonian, Nov 2025): AI should augment human judgment; validate models; keep humans in oversight; manage model risk ([CFA RPC](https://rpc.cfainstitute.org/research/foundation/2025/ai-in-asset-management-book)). Also the 2023 *Handbook of AI and Big Data Applications in Investments* ([CFA RPC](https://rpc.cfainstitute.org/research/foundation/2023/ai-and-big-data-in-investments-handbook)). |
| **Man Group** | B | "What AI Can (and Can't Yet) Do for Alpha": an internal workflow (AlphaGPT) generates and codes ideas. It warns of p-hacking, hallucination and implementation drift. Every decision is logged, a committee reviews ideas, and AI-generated strategies must pass the same bar as human ones ([Man Group](https://www.man.com/insights/what-ai-can-do-for-alpha)). This is the closest institutional analogue to Emporion's gated design. |

## 4. Regulators and standard setters (B)

- **IOSCO.**
  - Consultation report on AI in capital markets, 12 Mar 2025, covering risks to investor protection, market integrity and financial stability ([Regulation Tomorrow](https://www.regulationtomorrow.com/2025/03/iosco-consults-on-ai-in-capital-markets/); [IOSCO PDF](https://iosco.org/library/pubdocs/pdf/IOSCOPD788.pdf)).
  - Final *Supervisory Toolkit for AI use in Capital Markets*, 25 May 2026. Its scope covers ML, generative AI and **agentic AI**. Focus areas: governance and risk management, third-party risk, disclosure, and recordkeeping/reporting ([Regulation Tomorrow](https://www.regulationtomorrow.com/2026/05/iosco-final-report-supervisory-toolkit-for-ai-use-in-capital-markets/)).
- **FSB, "The Financial Stability Implications of AI," 14 Nov 2024.** Flags four vulnerabilities: dependence on a few third-party providers, correlated market behavior, cyber risk, and model risk/data quality/governance. Also warns about AI-enabled fraud and disinformation ([FSB](https://www.fsb.org/2024/11/fsb-assesses-the-financial-stability-implications-of-artificial-intelligence/)).
- **BIS.**
  - *Annual Economic Report 2024*, ch. III, "Artificial intelligence and the economy: implications for central banks" ([BIS](https://www.bis.org/publ/arpdf/ar2024e3.htm)).
  - Working Paper 1194, "Intelligent financial system: how AI is transforming finance" ([BIS](https://bis.org/publ/work1194.htm)).
- **FINRA Regulatory Notice 24-09 (27 Jun 2024).**
  - Rules are technology-neutral. Supervision (Rule 3110) should cover model risk, data integrity, and reliability/accuracy.
  - Rule 2210 content standards apply whether a person or AI wrote the communication.
  - Named risks: accuracy, privacy, bias, IP, and exploitation by threat actors ([FINRA](https://www.finra.org/rules-guidance/notices/24-09)).
- **SEC.**
  - First "AI-washing" cases (18 Mar 2024): Delphia and Global Predictions were fined $400k in total for overstating their use of AI ([SEC 2024-36](https://www.sec.gov/newsroom/press-releases/2024-36)).
  - The 2023 predictive-data-analytics conflicts proposal was **withdrawn** on 12 Jun 2025 ([Ropes & Gray](https://www.ropesgray.com/en/insights/alerts/2025/06/sec-clears-unfinished-rulemakings-from-regulatory-agenda)).
  - Practice: every public "AI" claim must be literally true.
- **ESMA public statement on AI and investment services (30 May 2024).** MiFID II organisational and conduct duties, including acting in the client's best interest, apply when firms use AI ([ESMA](https://esma.europa.eu/press-news/esma-news/esma-provides-guidance-firms-using-artificial-intelligence-investment-services)).
- **EU AI Act.**
  - The Annex III high-risk financial uses are creditworthiness/credit scoring and life/health insurance pricing ([William Fry](https://www.williamfry.com/knowledge/high-risk-ai-in-financial-services/)).
  - I found no source placing research or trading decision support in Annex III.
  - Classification guidance was still a draft as of May 2026 ([DLA Piper](https://www.dlapiper.com/en/insights/publications/2026/06/eu-commission-draft-guidelines-on-classification-of-high-risk-ai-systems-key-points)).
  - Low direct relevance to a US paper-only desk. This is not legal advice.

## 5. Practitioner channels (C) and community (D)

**C: podcasts, talks, blogs (existence verified on host pages)**
- **Chat With Traders × Quantopian, "Q1: Delaney Mackenzie – You Don't Know How Wrong You Are"** (21 Nov 2016) ([Metacast](https://metacast.app/podcast/chat-with-traders/BWeUo6jw/q1-delaney-mackenzie-you-don-t-know-how-wrong-you-are/IquOqwAL)). Covers overfitting, multiple-comparison bias, survivorship bias, and data-cleaning bias (vendor-cleaned history hides the bad prints a live feed will contain).
- **Other Chat With Traders episodes:** Q3 Jonathan Larkin on alpha factors ([Metacast](https://metacast.app/podcast/chat-with-traders/BWeUo6jw/q3-jonathan-larkin-seeking-alpha-try-more-alpha-factors/cgTbpL6E)); Morgan Slade on ML strategy development ([Metacast](https://metacast.app/podcast/chat-with-traders/BWeUo6jw/131-morgan-slade-strategy-development-powered-by-machine-learning/sxbhBMNP)). Titles verified; content not reviewed.
- **Flirting with Models (Corey Hoffstein):** John Alberg, "The Man in the Machine (Learning)" S1E7 ([Captivate](https://player.captivate.fm/episode/f3b74b23-4e4c-420c-8670-93a5d22ee4ee)); Ben Wellington (Two Sigma), "Complex Feature Engineering" S7E32 (listing on [Castfox](https://www.castfox.net/podcast/flirting-with-models-333980/episode/ben-wellington-complex-feature-engineering-at-two-sigma-s7e32-3213073)). Titles only.
- **Quantopian Lecture Series, "Dangers of Overfitting,"** a notebook preserved by QuantRocket ([QuantRocket](https://www.quantrocket.com/codeload/quant-finance-lectures/quant_finance_lectures/Lecture19-Dangers-of-Overfitting.ipynb.html)). The Quantopian forum post "9 mistakes quants make that cause backtests to lie" is also archived ([archive](https://quantopian-archive.netlify.app/forum/threads/9-mistakes-quants-make-that-cause-backtests-to-lie)).
- **Wheel/CSP risk (practitioner):**
  - Schwab (6 May 2025): assignment can come after fundamentals have deteriorated, premium may not offset a large drop, and secured cash has an opportunity cost ([Schwab](https://www.schwab.com/learn/story/three-things-to-know-about-wheel-strategy)).
  - Early Retirement Now, "The Wheel Strategy Doesn't Work" (Sep 2024): long bear markets hurt it; net delta rises as prices fall; reporting only realized premium hides losses on assigned stock; it relies on stock-picking skill ([ERN](https://earlyretirementnow.com/2024/09/17/the-wheel-strategy-doesnt-work-options-series-part-12/)).
  - Practice for the GP's wheel: show the unrealized P&L on assigned stock alongside premium income, and stress-test long bear regimes.

**D: Reddit/YouTube (signal of practice only; threads could not be opened from this environment)**
- **Thread titles seen in search:**
  - r/quant, "Research paper from Quantopian showing most of…" (Apr 2025), which discusses the 888-algorithm study ([reddit](https://www.reddit.com/r/quant/comments/1k05dp4/)).
  - r/options, "The Wheel (aka Triple Income) Strategy Explained" (Dec 2018) ([reddit](https://www.reddit.com/r/options/comments/a36k4j/the_wheel_aka_triple_income_strategy_explained/)).
- **Reddit-originated experiment reported in the press:** a $100 GPT-4o micro-cap experiment with one month of results ([Benzinga](https://www.benzinga.com/markets/equities/25/08/46783783/redditors-100-chatgpt-day-trading-experiment-trounces-two-benchmark-indexes-with-24-returns-here)). It is n=1 with a short horizon. Typical of community "AI beats market" claims and **not evidence**.
- **Recurring themes:** this is a summary of the C sources above plus the D titles. It is not quantified.
  - Overfitting and too many backtest iterations.
  - Survivorship bias and delisted stocks.
  - Look-ahead bias, now including LLM training-data leakage.
  - Transaction costs, slippage, and a paper-vs-live gap ([Alpaca forum thread](https://forum.alpaca.markets/t/slippage-paper-trading-vs-real-trading/2801); [QuantConnect forum](https://www.quantconnect.com/forum/discussion/3532/running-an-algorithm-live/)).
  - Short "AI beat the market" anecdotes.
  - For options: assignment, bag-holding after assignment, and concentration in volatile names.
- **YouTube:** no YouTube URL could be verified through search. Use the CFA Institute video (§3) and the podcasts above instead. Gap reported, not filled.

---

## 6. Synthesis: best-practice baseline for an AI trading desk

**Columns**
- **Tier:** the strongest evidence tier behind the practice.
- **Emporion status to check:** what a reviewer should look for in this repository. These are pointers only; this document does not verify Emporion's compliance.

### Data
| # | Practice | Tier | Sources | Emporion status to check |
|---|---|---|---|---|
| 1 | Use point-in-time data with explicit as-of stamps, and label stale or delayed data. | A | [Arnott et al.](https://alphaarchitect.com/protocol-to-prevent-quants-gone-wild/); [FSB](https://www.fsb.org/2024/11/fsb-assesses-the-financial-stability-implications-of-artificial-intelligence/) | `hedge_desk/freshness.py`, `data_quality.py`; STALE paths in `/api/health` |
| 2 | Use survivorship-free universes that include delisted names. | C | [Chat With Traders Q1](https://metacast.app/podcast/chat-with-traders/BWeUo6jw/q1-delaney-mackenzie-you-don-t-know-how-wrong-you-are/IquOqwAL) | Watchlist-to-candidates history: are removed or delisted symbols kept for backtests? |
| 3 | Don't cherry-pick, clean or winsorize data arbitrarily. Log every transform. | A | [Arnott et al.](https://alphaarchitect.com/protocol-to-prevent-quants-gone-wild/) | `data_quality.py` reason codes; fixture provenance |
| 4 | Record provider provenance, and fail closed on malformed or empty payloads. | B | [FINRA 24-09](https://www.finra.org/rules-guidance/notices/24-09); [IOSCO 2026](https://www.regulationtomorrow.com/2026/05/iosco-final-report-supervisory-toolkit-for-ai-use-in-capital-markets/) | `hedge_desk/data/providers.py` reason codes; `docs/data_provider_registry.md` |
| 5 | Track LLM training cutoffs. Treat LLM signals inside the training window as contaminated, or anonymize entities and use point-in-time models. | B | [Glasserman & Lin](https://arxiv.org/abs/2309.17322); [Sarkar & Vafa](https://icml.cc/virtual/2025/48685); [He et al.](https://arxiv.org/abs/2502.21206v3) | Does the Muse/news pipeline (`data/pwb_news.py`, `research_intelligence.py`) log model ID and cutoff, and anonymize entities? |

### Research
| # | Practice | Tier | Sources | Emporion status to check |
|---|---|---|---|---|
| 6 | Start from an economic hypothesis and name who is on the other side of the trade. | A | [Arnott et al.](https://alphaarchitect.com/protocol-to-prevent-quants-gone-wild/) | Yellow Sheet template: is there a "why it should work" field? (`yellow_sheet.py`) |
| 7 | Compare against a strong linear or passive baseline, including buy-and-hold. | A/B | [Gu et al.](https://nber.org/papers/w25398); [StockBench](https://arxiv.org/abs/2510.02209v1); [FINSABER](https://arxiv.org/abs/2505.07078?context=cs) | `evaluation.py`, `stat_evaluation.py`: is a baseline mandatory? |
| 8 | Use feature importance, not repeated backtests, as the research loop. | A | [López de Prado 10 reasons](https://www.garp.org/hubfs/Whitepapers/a1Z1W0000054x6lUAA.pdf) | `features.py` |
| 9 | Treat LLM output as a hypothesis or feature, and ground it in cited filings. | B | [FinanceBench](https://arxiv.org/abs/2311.11944v1); [Man Group](https://www.man.com/insights/what-ai-can-do-for-alpha) | Muse citations; `sec_filings_service.py`; `research_audit.py` |
| 10 | Check retraction and version status for every cited paper. | B | [Kim et al. withdrawn](https://arxiv.org/abs/2407.17866v3) | `docs/research/` citation hygiene |

### Validation
| # | Practice | Tier | Sources | Emporion status to check |
|---|---|---|---|---|
| 11 | Use purged and embargoed time-series CV, never shuffled K-fold. | A | [López de Prado](https://www.garp.org/hubfs/Whitepapers/a1Z1W0000054x6lUAA.pdf) | `hedge_desk/models/splits.py` has `evaluate_purged_walk_forward_split` with an embargo check. Confirm it gates real runs, not only the synthetic gate. |
| 12 | Log every trial and report the trial count. | A | [Bailey & López de Prado DSR](https://papers.ssrn.com/abstract=2460551); [Wiecki et al.](https://hedgefundalpha.com/strategies/comparing-backtest-sample-performance-large-cohort-trading-algorithms/) | `models/training_run.py`: is there a trial counter? |
| 13 | Report a deflated or haircut Sharpe ratio, never a raw one. | A | [DSR](https://papers.ssrn.com/abstract=2460551); [Harvey & Liu](https://people.duke.edu/~charvey/Research/Published_Papers/P120_Backtesting.PDF) | No DSR or haircut was found by a quick grep. Gap to confirm. |
| 14 | Set a multiple-testing bar: t>3 or an FDR control. | A | [Harvey, Liu & Zhu](https://nber.org/papers/w20592) | `stat_inference.py` (has Wilson intervals and an exact binomial tail; no multiple-testing correction seen) |
| 15 | Estimate PBO (via CSCV) before promotion. | A | [Bailey et al.](https://papers.ssrn.com/abstract=2326253) | Not seen. Gap to confirm. |
| 16 | Test across regimes: long windows, bull and bear markets, and wide universes. | B | [FINSABER](https://arxiv.org/abs/2505.07078?context=cs); [ERN](https://earlyretirementnow.com/2024/09/17/the-wheel-strategy-doesnt-work-options-series-part-12/) | `wargames.py`, `portfolio_stress.py`, `vix_regime.py` |
| 17 | Treat paper trading as a required stage between backtest and any live use, and measure the gap explicitly. | B | [Yu et al. 2026](https://arxiv.org/pdf/2609.34510) | `hedge_desk/paper/` (runner, settler, review); `paper_log.py` |
| 18 | Don't re-tune a model on its own live or paper results. | A | [Arnott et al.](https://alphaarchitect.com/protocol-to-prevent-quants-gone-wild/) | `agents/learning_ledger.py` must stay append-only and not auto-feed parameters |
| 19 | Use deterministic reference cases for every financial calculation. | C | [Derman & Wilmott](https://emanuelderman.com/the-financial-modelers-manifesto/) | `tests/` exact Decimal cases (required by AGENTS.md) |

### Portfolio and risk
| # | Practice | Tier | Sources | Emporion status to check |
|---|---|---|---|---|
| 20 | Keep sizing and risk limits in deterministic, non-agentic code. LLM agents must not set them. | B | [FINSABER](https://arxiv.org/abs/2505.07078?context=cs) (regime-aware risk controls); [Man Group](https://www.man.com/insights/what-ai-can-do-for-alpha) | `position_sizing.py`; 2%-of-equity rule; `risk/ruin.py` is consumed, never computed by agents |
| 21 | Weight risk metrics (volatility, drawdown) above backtest return when choosing what to promote. | B | [Wiecki et al.](https://hedgefundalpha.com/strategies/comparing-backtest-sample-performance-large-cohort-trading-algorithms/) | `premium_score.py`, `SCORING_RUBRIC.md` |
| 22 | For CSPs and the wheel, show assigned-stock unrealized P&L, opportunity cost of secured cash, and the downside at assignment. Display return on collateral, not on risk. | C | [Schwab](https://www.schwab.com/learn/story/three-things-to-know-about-wheel-strategy); [ERN](https://earlyretirementnow.com/2024/09/17/the-wheel-strategy-doesnt-work-options-series-part-12/) | `csp_scan.py`, `docs/PREMIUM_WHEEL_ECONOMICS.md` |
| 23 | Use valuation (CAPE) as long-horizon context only, tied to an exact source. | A | [Campbell & Shiller](https://www.nber.org/papers/w8221) | Shiller layer cites w8221 (or the original), with no agent-derived formula |

### Execution (paper-only here)
| # | Practice | Tier | Sources | Emporion status to check |
|---|---|---|---|---|
| 24 | Model costs, slippage and bid/ask in every evaluation. Live execution cost can far exceed paper: one study measured live price difference at nearly 6× the paper figure (about 1.86‰ vs 0.31‰). | B/D | [Yu et al. 2026](https://arxiv.org/pdf/2609.34510); [Alpaca forum](https://forum.alpaca.markets/t/slippage-paper-trading-vs-real-trading/2801) | `paper/settler.py`: are fills at mid or at a conservative bid/ask? |
| 25 | Keep a hard execution boundary with no order placement. Candidates stay `trade_authorized=False`. | B | [FINRA 24-09](https://www.finra.org/rules-guidance/notices/24-09); [ESMA](https://esma.europa.eu/press-news/esma-news/esma-provides-guidance-firms-using-artificial-intelligence-investment-services) | `execution_gate.py`; `brokers/` contain no order endpoints |

### Monitoring
| # | Practice | Tier | Sources | Emporion status to check |
|---|---|---|---|---|
| 26 | Monitor signal decay. LLM-based edges erode as adoption spreads. | B | [Lopez-Lira & Tang](https://arxiv.org/abs/2304.07619) | `stat_evaluation.py` calibration over time; `operational_health.py` |
| 27 | Track concentration on one model vendor and plan a fallback. | B | [FSB](https://www.fsb.org/2024/11/fsb-assesses-the-financial-stability-implications-of-artificial-intelligence/); [IOSCO 2026](https://www.regulationtomorrow.com/2026/05/iosco-final-report-supervisory-toolkit-for-ai-use-in-capital-markets/) | Is the LLM provider pinned and versioned, and does the desk degrade honestly if it is unavailable? |
| 28 | Keep data-feed health and freshness alerts in place. | B | [FSB](https://www.fsb.org/2024/11/fsb-assesses-the-financial-stability-implications-of-artificial-intelligence/) | `/api/health`; `/datalink-watch` |

### Governance and human oversight
| # | Practice | Tier | Sources | Emporion status to check |
|---|---|---|---|---|
| 29 | Hold AI-generated ideas to the same bar as human ones. Use committee review and log every decision. | B | [Man Group](https://www.man.com/insights/what-ai-can-do-for-alpha) | Yellow Sheet independent review; `audit.py`, `audit_store.py` |
| 30 | Require independent validation. No agent approves its own risk-control change. | B | [CFA RF 2025](https://rpc.cfainstitute.org/research/foundation/2025/ai-in-asset-management-book); [FINRA 24-09](https://www.finra.org/rules-guidance/notices/24-09) | PR template and `/review` flow per AGENTS.md |
| 31 | Keep recordkeeping that can reproduce each decision: inputs, model versions, prompts, reason codes. | B | [IOSCO 2026](https://www.regulationtomorrow.com/2026/05/iosco-final-report-supervisory-toolkit-for-ai-use-in-capital-markets/) | `replay.py`; reason codes in decisions |
| 32 | Make no AI-washing or performance claims, and keep public copy literally true. | B | [SEC 2024-36](https://www.sec.gov/newsroom/press-releases/2024-36) | `scripts/lint_copy.py`; `docs/EMPORION_MARKETING_CLAIM_AUDIT.md` |
| 33 | State assumptions and limits with every model output. | C | [Derman & Wilmott](https://emanuelderman.com/the-financial-modelers-manifesto/) | Console disclaimers; `ENGINEERING_LESSONS.md` locked copy |
| 34 | Keep humans on judgment (narrative, assumptions) and automate the mechanical parts. | C | [Damodaran](https://aswathdamodaran.substack.com/p/beat-your-bot-building-your-moat); [Lo](https://mitsloan.mit.edu:443/ideas-made-to-matter/can-generative-ai-provide-trusted-financial-advice) | The GP decides; lane separation in SOUL.md |

### Agent design
| # | Practice | Tier | Sources | Emporion status to check |
|---|---|---|---|---|
| 35 | Prefer role-separated agents (analyst, bull/bear, risk), but put a deterministic risk gate after them. Debate does not replace limits. | B | [TradingAgents](https://arxiv.org/abs/2412.20138); [AMA](https://arxiv.org/abs/2510.11695) | Hermes profiles (RESEARCH/QUANT/RISK...) and the order in which deterministic gates run |
| 36 | Judge agents on live or forward data, not static QA scores or leaderboard rank. | B | [LiveTradeBench](https://arxiv.org/abs/2511.03628?context=cs); [StockBench](https://arxiv.org/abs/2510.02209v1) | Paper-log forward evaluation per agent lane |
| 37 | Version the agent framework and the model separately; the framework drives behavior more than the model does. | B | [AMA](https://arxiv.org/abs/2510.11695) | Are prompt and framework versions recorded in `learning_ledger.py` and the artifacts? |
| 38 | Grounding: every numeric claim an agent makes is recomputed or looked up deterministically, and is never trusted as free text. | B | [FinanceBench](https://arxiv.org/abs/2311.11944v1) | `research_audit.py`; Muse claims vs. data store |
| 39 | Treat agent memory and learning as append-only, outcome-labeled and audited, never self-modifying risk inputs. | B | [FinMem](https://arxiv.org/abs/2311.13743v2); [Man Group](https://www.man.com/insights/what-ai-can-do-for-alpha) | `agents/learning_ledger.py` |

### Red flags and anti-patterns
1. Reporting a backtest Sharpe ratio without the trial count, a DSR or a haircut ([DSR](https://papers.ssrn.com/abstract=2460551)).
2. Shuffled K-fold or a single walk-forward path on overlapping labels ([López de Prado](https://www.garp.org/hubfs/Whitepapers/a1Z1W0000054x6lUAA.pdf)).
3. LLM sentiment or "reasoning" backtested inside the model's training window ([Sarkar & Vafa](https://icml.cc/virtual/2025/48685)).
4. Prompting an LLM to "ignore the future" as a fix for lookahead bias ([Sarkar & Vafa](https://icml.cc/virtual/2025/48685)).
5. Short-window agent demos and n=1 Reddit experiments presented as evidence ([FINSABER](https://arxiv.org/abs/2505.07078?context=cs); [Benzinga](https://www.benzinga.com/markets/equities/25/08/46783783/redditors-100-chatgpt-day-trading-experiment-trounces-two-benchmark-indexes-with-24-returns-here)).
6. Citing withdrawn or unreplicated papers ([Kim et al.](https://arxiv.org/abs/2407.17866v3)).
7. Letting an LLM set position size, limits or risk-of-ruin inputs. This violates the separation in SOUL.md and AGENTS.md.
8. Re-tuning a model on its own live results ([Arnott et al.](https://alphaarchitect.com/protocol-to-prevent-quants-gone-wild/)).
9. Ignoring costs and slippage, or filling paper trades at mid ([Yu et al. 2026](https://arxiv.org/pdf/2609.34510)).
10. Wheel P&L that counts only realized premium and hides losses on assigned stock ([ERN](https://earlyretirementnow.com/2024/09/17/the-wheel-strategy-doesnt-work-options-series-part-12/)).
11. Public "AI-powered" claims the system cannot back up ([SEC 2024-36](https://www.sec.gov/newsroom/press-releases/2024-36)).
12. Using leaderboard rank or static finance-QA scores to choose the trading model ([LiveTradeBench](https://arxiv.org/abs/2511.03628?context=cs)).
13. Single-vendor LLM dependence with no degradation path ([FSB](https://www.fsb.org/2024/11/fsb-assesses-the-financial-stability-implications-of-artificial-intelligence/)).
14. Survivorship-biased universes and vendor-cleaned history used as if it were a live feed ([Chat With Traders Q1](https://metacast.app/podcast/chat-with-traders/BWeUo6jw/q1-delaney-mackenzie-you-don-t-know-how-wrong-you-are/IquOqwAL)).

**V&V label for this document**
- **VERIFIED (partial):** every source title, author and venue was checked against a primary page via WebSearch/WebFetch. Content summaries come from abstracts or host pages, as noted.
- **Not VALIDATED:** the GP has not reviewed this document.
- **Known gaps:**
  - Reddit thread bodies and YouTube URLs could not be read.
  - The Paleologo and Chan/Medina book contents were not reviewed.
  - The Emporion status column consists of pointers, not an audit.
