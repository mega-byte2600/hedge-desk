# Quant/AI Model Lab — Deep Literature Sweep
**Date:** 2026-09-25 · **Scope:** deeper than the daily pass; arXiv q-fin, SSRN-adjacent, Hugging Face datasets
**Question:** Which external research should the quant lab adopt, test, or watch to strengthen the desks' edge?
**Lens:** value investor — mispricings, intrinsic-value gaps, margin of safety. **Bar:** outperform the best Wall Street analyst.
**Method:** RESEARCH ONLY — no code changes, no GitHub operations. Each candidate scored with the repo's own `hedge_desk.research_intelligence.assess_source` (100-point scale; ≥80 INTEGRATE, ≥65 TEST, ≥45 WATCH, else ARCHIVE). Claims labeled FACT / INFERENCE / UNVERIFIED per the CFA evidence standard.

## Verdict up front
- **1 INTEGRATE:** HF Data Library (score 80) — the only candidate with a verified open license, DOI, and documented pipeline.
- **2 TEST:** Gormsen & Lazarus "Equity Duration and Interest Rates" (68); "Propose, Don't Judge" anytime-valid referee (66).
- **11 WATCH, 1 ARCHIVE.** No candidate was rejected on license grounds.

## Score table

| # | Candidate | Topic | Score | Disposition | URL |
|---|-----------|-------|-------|-------------|-----|
| 1 | HF Data Library: 1-min bars, 1391 US equities, CC BY 4.0 | dataset | 80 | **INTEGRATE** | https://github.com/elkassabgi/hfdatalibrary/blob/HEAD/huggingface_README.md |
| 2 | Gormsen & Lazarus: Equity Duration and Interest Rates (Apr 2025) | macro→equity (rates) | 68 | **TEST** | https://www.gsb.stanford.edu/sites/default/files/2025-05/StockBondDurationMain.pdf |
| 3 | Propose, Don't Judge: Anytime-Valid Referee for LLM factor mining (2609.27051) | methodology | 66 | **TEST** | https://arxiv.org/abs/2609.27051 |
| 4 | Arbitrage-Aware Multi-Step Forecasting of IV Surfaces (2608.22478) | vol forecasting | 63 | WATCH | https://arxiv.org/abs/2608.22478v1 |
| 5 | Realised Volatility Forecasting via Financial Word Embedding (2108.00480) | vol forecasting | 62 | WATCH | https://arxiv.org/abs/2108.00480v4 |
| 6 | Dividend Growth: forecasting from dividend futures, state-space (FMA) | dividend forecasting | 62 | WATCH | https://www.fmaconferences.org/Taipei/Papers/206.pdf |
| 7 | Universal Diffusion Models for IVS (2609.22893) | vol forecasting | 60 | WATCH | https://arxiv.org/abs/2609.22893v1 |
| 8 | Forecasting IV surface with generative diffusion models (2511.07571) | vol forecasting | 60 | WATCH | https://arxiv.org/abs/2511.07571v1 |
| 9 | Memory, Roughness, and Information Persistence in Volatility (2605.24285) | vol forecasting | 60 | WATCH | http://arxiv.org/abs/2605.24285v1 |
| 10 | Energy prices → US stock market volatility (J. Energy Markets) | macro→equity (oil) | 56 | WATCH | https://www.risk.net/node/7962838 |
| 11 | Predicting Stock Price Direction on Earnings Days, multi-modal DL (2605.25894) | earnings drift | 54 | WATCH | http://arxiv.org/abs/2605.25894v1 |
| 12 | Controllable Generation of IVS with VAEs (2509.01743) | vol forecasting | 51 | WATCH | https://arxiv.org/abs/2509.01743v1 |
| 13 | Macroeconomic Shocks and Cross-sectional Stock Returns (MFA 2026) | macro→equity | 51 | WATCH | https://www.conftool.pro/mfa2026/index.php/Fieldhouse-1028-Macroeconomic_Shocks_and_Cross-sectional_Stock_Returns.pdf?page=downloadPaper&filename=Fieldhouse-1028-Macroeconomic_Shocks_and_Cross-sectional_Stock_Returns.pdf&form_id=1028 |
| 14 | Koijen & Levy: AI explains 17% of earnings-day moves (live test) | earnings drift | 48 | WATCH | http://phys.org/news/2026-07-ai-day-stock.html |
| 15 | Learning Market Making with Closing Auctions (2601.17247) | microstructure | 42 | ARCHIVE | https://arxiv.org/abs/2601.17247v1 |

## Candidate notes (evidence-labeled)

**1. HF Data Library — INTEGRATE (80).** FACT: 1,391 US equities/ETFs, 1.6B+ 1-minute bars, Dec 2002–present, daily updates, nine-step documented cleaning pipeline, CC BY 4.0, Zenodo DOI 10.5281/zenodo.19501605, academic maintainer (Univ. of Central Arkansas). INFERENCE: this directly fills the desk's persistent gap in free intraday data for microstructure and realized-vol work. UNVERIFIED: actual download throughput / API reliability under our pipeline (free registration required; data hosted off-HF at hfdatalibrary.com). Disposition rationale: only candidate with verified open license + provenance + maintenance cadence. Next step: implementation review — pull a 5-ticker sample, validate bar alignment vs Yahoo EOD, then wire into the vol estimators.

**2. Gormsen & Lazarus, "Equity Duration and Interest Rates" — TEST (68).** FACT: Stanford GSB working paper, Apr 2025; decomposes trend real-rate changes into expected-growth, uncertainty, and pure-discounting components; reports pure discounting explains >80% of cross-country valuation variation since 1990, but only ~35% of the US rate decline was pure discounting. INFERENCE: this is the disciplined version of the rates→equity channel the macro desk now tracks — it prevents over-attributing equity moves to headline yield moves. UNVERIFIED: replication on our watchlist (needs FRED + price panel; both available). Disposition rationale: highest-signal macro paper found; test = replicate the decomposition on SPY/QQQ + watchlist before citing it in research.

**3. "Propose, Don't Judge" (2609.27051) — TEST (66).** FACT: submitted 22 Sep 2026; frozen betting-based referee scores factors only on post-submission outcomes; reports 5–11× fewer false admissions vs leaky referees; 10-year CSI 500 walk-forward; admitted true factors wait ~500 trading days. INFERENCE: maps directly onto the desk's doctrine (deterministic evaluation over model output) and the automation audit's human-gate design — the referee is the machine analogue of the frozen judgment layer. UNVERIFIED: no code released; CSI 500 results may not transfer to US single-name options. Disposition rationale: test = prototype the referee inside the existing evaluation framework on a synthetic planted-truth world first.

**4–6. IV-surface diffusion cluster — WATCH (63/60/60).** Three 2025–26 preprints (2608.22478 latent diffusion with 30-step SPX trajectories; 2511.07571 DDPM with SNR-weighted arbitrage penalty; 2609.22893 universal cross-stock diffusion) all push the same frontier: generative, arbitrage-aware IV-surface dynamics. FACT: all three are preprints with no released code found in their abstracts. INFERENCE: the field is converging on diffusion + arbitrage penalties as the standard approach; worth tracking for the premium desk's scenario engine, but nothing here is adoptable today. The desk's standing rule holds: deterministic parity math outranks any of these models' outputs.

**7. Financial word embedding + HAR (2108.00480) — WATCH (62).** FACT: v6 (Apr 2026), SSRN-linked; financial word embedding from 15 years of news improves HAR realized-vol forecasts statistically and economically. INFERENCE: the "news → vol" channel is real but the lift is incremental over HAR; needs a news corpus we don't currently license. Watch for an open-weights embedding release.

**8. Memory/roughness/persistence (2605.24285) — WATCH (60).** FACT: 115 S&P 500 names, 2001–2026; persistence features (GPH/local-Whittle) give moderate but significant OOS gains over HAR/HAR-X, strongest at long horizons and in stress. INFERENCE: cheapest vol-forecast upgrade on this list — computable from price data we already pull. Promote to TEST if the desk's HAR baseline is built.

**9. Dividend futures state-space (FMA) — WATCH (62).** FACT: forecasts 1-year-ahead dividend growth from dividend-futures-implied equity yields; beats Binsbergen-Koijen and historical-average benchmarks OOS, strongest in stress periods. INFERENCE: directly relevant to the dividend desk's mispricing hunt. UNVERIFIED: relies on proprietary OTC dividend-derivative data we don't have; testability depends on a free dividend-futures proxy.

**10. Energy prices → US equity vol (J. Energy Markets) — WATCH (56).** FACT: peer-reviewed; monthly 1986–2023; crude shows asymmetric long-run supply-driven effects on stock returns; gas/electricity mitigate oil shocks. INFERENCE: supports the oil-impact channel the R&D pipeline now tracks, but monthly frequency limits trading-desk use. Paywalled — abstract-level only.

**11. Earnings-day direction, multi-modal DL (2605.25894) — WATCH (54).** FACT: arXiv abs page verified 2026-09-25; FinBERT sentiment + fundamentals + technicals; Transformer beats LSTM on macro F1; sentiment ablation positive. INFERENCE: direction-prediction on EA days is a crowded, decay-prone signal class (cf. Lopez-Lira & Tang decay curve). Watch, don't chase.

**12. Koijen & Levy live AI test — WATCH (48).** FACT: per phys.org (Jul 2026), Chicago Booth authors ran a live (non-simulated) test on ~2,000 late-2025 earnings announcements; best AI models explained ~17% of same-day moves vs ~5% for earnings surprise alone. INFERENCE: the methodological lesson (live test kills lookahead bias) matters more than the 17% number. UNVERIFIED: scored from press coverage; underlying working paper not verified from a primary source. Do not cite the 17% figure until the paper itself is read.

**13. MFA 2026 macro shocks paper — WATCH (51).** FACT: conference paper (Sep 2025); local projections; monetary/credit/oil/fiscal shocks explain 5–50% of residual cross-sectional return variance over 4-year horizons. INFERENCE: useful causal framing for the macro desk, but conference-stage and author-unverified. Watch for the journal version.

**14. Controllable VAE IVS generation (2509.01743) — WATCH (51).** FACT: Delft/ING authors; disentangled shape features + latent-space arbitrage repair. INFERENCE: most directly useful for wargame scenario design (controllable stress surfaces), not forecasting. Niche; watch.

**15. Closing-auction market making (2601.17247) — ARCHIVE (42).** Deep Q-learning market maker anticipating the closing auction. Desk doesn't make markets; no transferable edge for a paper research system. Archived, not rejected on quality.

## Methodology note: purged walk-forward
The sweep found **no new peer-reviewed candidate** on purged walk-forward / CPCV beyond the established López de Prado framework (AFML ch. 7, 12–13; PBO). FACT: the desk already implements purged walk-forward per its evaluation module. INFERENCE: methodology effort is better spent on the anytime-valid referee (#3) than on re-deriving CPCV. Practitioner references (CPCV explainer repos) were reviewed but add nothing citable beyond the book.

## What would change these verdicts
- Any WATCH paper releasing code + data → re-score (reproducibility is the binding constraint on 11 of 15).
- HF Data Library sample pull failing bar-alignment vs Yahoo EOD → downgrade to WATCH.
- Gormsen–Lazarus replication failing on the watchlist panel → ARCHIVE.
- Koijen–Levy working paper verified from primary source → re-score as PEER_REVIEWED-adjacent.
