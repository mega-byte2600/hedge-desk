# Validation Source Catalog

This catalog records locally supplied reference inputs without redistributing
their copyrighted PDF contents. A SHA-256 digest identifies the exact local
artifact used during requirements analysis and V&V preparation.

None of these sources is allowed to generate an authoritative Risk of Ruin
value through an agent. Any quantitative requirement derived from a source must
be stated explicitly, implemented in deterministic software, tested against
locked cases, and independently validated.

## Intake batch 2026-08-21

| Local artifact | SHA-256 | Pages | Preliminary role | Public-repository treatment |
|---|---|---:|---|---|
| `ML_Options_Pricing_JSER.pdf` | `a777a6800635059d2bb7e76ad9e017c4b0af58c04f1835e880a4cb5db51fb30f` | 7 | ML option-pricing research candidate; model evaluation context, not a risk-gate authority | Metadata/citation only until author, publication, and license are confirmed |
| `OptionPricing_DeepLearning_Stanford.pdf` | `83482c3ea04df5581ea9cf97dbdff59374e097e5d488c9438eca4f1454e4e688` | 8 | Stanford CS230 paper, *Option Pricing with Deep Learning*, Alexander Ke and Andrew Yang; benchmark/methodology candidate | Metadata/citation only until redistribution license is confirmed |
| `2020_Series_7_2E_LEM_REV4.pdf` | `97b6aaf0faa8636ab91ee06748c34048674c2fdcde956dd8131f49a5eebfeba9` | 616 | Kaplan Series 7 License Exam Manual, 2nd ed.; compliance/product terminology | Do not commit; encrypted against copying and apparently copyrighted |
| `shiller2003.pdf` | `712e88c9ddc0c2822125298d7c79d1b3e3e07da5c1c27cea41b5ad8f90f40100` | 186 | Robert J. Shiller, *The New Financial Order: Risk in the 21st Century*; conceptual/systemic risk and risk-sharing requirements research | Do not commit full book; retain bibliographic citation and permitted derived requirements only |
| `Derivatives_Fall_2015-3.pdf` | `88e428e1b590b5d15d993fb0a4da867197e905162d8ae376c8d9493433e8bd7b` | 11 | SNHU College of Business derivatives course material; educational cross-check | Metadata/citation only until title, author, and license are confirmed |
| `Hull J.C.-Options, Futures and Other Derivatives_9th edition.pdf` | `7feca358324f69bfdc5dcb18f8a2299e05311964e5c38ea45637be5dd5370445` | 892 | John C. Hull, *Options, Futures, and Other Derivatives*, 9th ed.; deterministic derivatives formulas, assumptions, and numerical reference-case design | Do not commit full book; cite exact edition/section and add independently constructed redistributable fixtures |
| `S7.LEM_2ndEdition.pdf` | `cccb9852f59582a3002a7e7c13d80fe908a40bf947d5e307239d5922cda27e25` | 616 | Second local copy/variant of Kaplan Series 7 License Exam Manual, 2nd ed. | Do not commit; resolve duplication and retain one local reference identity |
| `Victor_Sperandeo_-_Trader_Vic_-_Methods_of__a_Wall_Street_Master.pdf` | `0f3c097528741b57c6ec7d1aabc70bf4d5869b998d2b170496bd218e3fa1ee78` | 147 | Victor Sperandeo with T. Sullivan Brown, *Trader Vic: Methods of a Wall Street Master*; practitioner heuristics and hypothesis-generation context | Do not commit full book; heuristics require independent formalization and empirical validation |

## Preliminary methodological disposition

- **Deterministic reference candidates:** Hull, once exact chapters, equations,
  conventions, examples, and edition-specific errata are mapped.
- **Portfolio-risk requirements research:** Shiller can inform risk categories,
  risk sharing, and long-horizon framing, but does not by itself specify the
  portfolio risk engine or RoR formula.
- **Experimental model benchmarks:** the Stanford and JSER ML option-pricing
  papers may inform an evaluation harness. ML outputs cannot replace validated
  deterministic risk controls.
- **Compliance education:** Series 7 material can help identify terminology and
  candidate rules, but current authoritative regulations and primary regulatory
  sources must control implementation.
- **Practitioner hypotheses:** Sperandeo can supply hypotheses for testing, not
  authoritative calculations or policy thresholds.

No David P. Swensen primary source was included in this intake batch. Swensen
methodology must not be attributed or implemented until an exact source is
provided or independently obtained and cited.

## Required next-pass metadata

Before a source becomes a V&V dependency, capture:

1. complete bibliographic citation and stable source identifier;
2. redistribution/license status;
3. exact pages, equations, tables, or propositions used;
4. documented interpretation and applicability limits;
5. deterministic reference inputs, expected outputs, units, and tolerances;
6. errata and edition/revision status;
7. independent validator and approval evidence.

## Intake batch 2026-08-21 - MIT 15.401 Finance Theory I

The title pages and embedded metadata identify this batch as Andrew W. Lo's
MIT Sloan 15.401 Finance Theory I lecture materials from 2008. Licensing and
the authoritative MIT OpenCourseWare source URLs must be confirmed before any
PDF is redistributed.

| Local artifact | SHA-256 | Pages | Preliminary role | Public-repository treatment |
|---|---|---:|---|---|
| `Equities_MIT.pdf` | `9eb7e4c30ff8a42220d947554d0021fad446fea9c270fd2cca00f82039bba106` | 24 | Lecture 7, Equities; candidate cross-check for equity valuation/return assumptions and deterministic reference-case design | Metadata/citation only pending exact source URL and license confirmation |
| `Fixed.Income_MIT.pdf` | `2a6d65689c33c1d67dbea5fe3eaf8925eea97cd6ea9842092fe6aa1077a384ef` | 66 | Lectures 4-6, Fixed-Income Securities; candidate cross-check for discounting, term structure, duration/convexity, and rate-risk requirements | Metadata/citation only pending exact source URL and license confirmation |
| `Forward.Future.Contracts_MIT.pdf` | `af516e9151c77b9b6dbb1f437736d100591e58220b8847846436e66e3b821d0b` | 33 | Lectures 8-9, Forward and Futures Contracts; deterministic pricing, carry, hedge, and exposure test-case candidate | Metadata/citation only pending exact source URL and license confirmation |
| `Options_MIT.pdf` | `0305d83f1fe3fb006921e0e58fe10992e0392d7df5a0080a9cd6502f3cf60cfb` | 31 | Lectures 10-11, Options; deterministic payoff/pricing/hedging reference-case candidate and cross-check against Hull | Metadata/citation only pending exact source URL and license confirmation |
| `Options.MIT.pdf` | `0305d83f1fe3fb006921e0e58fe10992e0392d7df5a0080a9cd6502f3cf60cfb` | 31 | Exact byte-for-byte duplicate of `Options_MIT.pdf`; no separate evidentiary value | Do not retain as a second V&V dependency |

### Disposition

- Treat these materials as secondary instructional cross-checks until each
  requirement is traced to the exact slide and corroborated by a primary or
  otherwise authoritative source.
- Construct independent, redistributable numerical fixtures rather than copying
  slide content into the repository.
- Do not use the lecture material to define or calculate authoritative RoR.
- When formulas are adopted, record compounding, day-count, settlement, dividend,
  carry, exercise-style, and market-friction conventions explicitly.
- Resolve the two options filenames to the single SHA-256 identity above.
