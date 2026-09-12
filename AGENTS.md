# Hedge Desk Agent Rules

## 80/20 delivery rule

- Target 80% working, tested code and 20% durable decision records.
- Fail fast, build, measure, learn, and ship the smallest useful vertical slice.
- Do not count commentary, plans, or generated prose as implementation.
- No merge is complete until CI passes unit, failure-path, and runnable smoke
  tests. Financial calculations require exact deterministic reference cases.
- CI/CD and model/data validation gates fail closed; agents cannot waive them.

- Keep the system paper-only until a separately reviewed release explicitly
  introduces read-only brokerage access.
- Never bypass, weaken, or silently default a failed risk or compliance gate.
- Use `Decimal` for money and portfolio ratios used in approval decisions.
- Every decision must retain reason codes and enough inputs to reproduce it.
- Tests must be deterministic: fixed clocks, fixtures, and random seeds.
- Financial-model changes require reference cases and independent review.
- An agent may implement and test a change but may not approve its own
  risk-control change for release.
- Agents and agentic workflows must never calculate, estimate, infer, modify, or
  substitute the authoritative Risk of Ruin value. RoR is produced only by a
  separately versioned deterministic software component developed and validated
  through conventional software V&V. Agents may consume its immutable result.
- Agent-proposed inputs are not validated risk inputs. The deterministic risk
  engine accepts only data that has passed its non-agentic schema, provenance,
  freshness, and validation controls.
- Portfolio-risk methodology must cite its primary research basis and validated
  reference cases. Work attributed to David P. Swensen or Robert J. Shiller must
  be tied to an exact source and must not be converted into a formula by an
  agent's interpretation alone.

## Reference material and licensed content

Agents are permitted, and expected, to study reference material — licensing exam
manuals, vendor documentation, rulebooks, textbooks — and to let it inform design and
engineering decisions. A rule, a domain outline, or a concept is knowledge; applying it
is the job.

The constraint is on redistribution, not on learning:

- Do **not** commit licensed or restricted material to this repository, in whole or in
  part. This project is public open source, so everything committed is published.
- Do **not** reproduce passages from licensed material in commits, PRs, issues, comments,
  or documentation. Cite public sources instead — rule numbers, statute sections, and
  published exam-domain structures.
- Derived notes in an agent's own words **are** permitted and belong in `docs/`, with the
  public sources named.
- The same rule covers brokerage credentials, account data, licensed market-data
  payloads, and third-party study material purchased under a personal licence.

## Engineering lessons

Read `docs/ENGINEERING_LESSONS.md` before changing public copy, a DOM selector, a store, or
anything that reports a result. It records the failure classes this project has actually hit
and the rule that prevents each. Two of them have already cost real time more than once:

- **Locked public copy is not safe from a DOM edit.** Positioned copy conveys claims (Risk of
  Ruin, disclaimers, method descriptions). A bare class selector can match more than one
  block and silently rewrite the wrong one, and that has happened repeatedly.
- **A check that passes for the wrong reason is worse than no check.** A count is not
  evidence until you know what it counted. An assertion is a hypothesis, not proof.

## Method Stack

- Series 7 / FINRA / SEC: compliance and product-rule layer.
- Graham / Buffett / Burry / Shiller: valuation and mispricing layer.
- Hull / ML options papers: derivatives pricing, volatility, bid/ask, and premium research layer.
- Trader Vic: timing and market-structure layer.
- Risk of Ruin: portfolio survival layer.

## Hermes / Matrix

- Hermes is the self-hosted Matrix messenger interface for coordinating agents.
- Matrix/Hermes can receive sanitized project status and task instructions.
- Matrix/Hermes must not receive Schwab secrets, OAuth tokens, API keys, account identifiers, or licensed/private payloads.
- Agent learning is append-only and paper-outcome based.
- Do not commit ChatGPT chat history, raw prompts, private project instructions, copied conversation transcripts, or Matrix room transcripts to GitHub.

## GitHub CLI collaboration

- Use GitHub issues as the durable task queue and pull requests as the unit of
  review. Follow `docs/AGENT_GITHUB_CLI_WORKFLOW.md`.
- Before editing, claim the issue with a `gh issue comment` and work on a
  dedicated branch. Do not let multiple agents edit the same critical path.
- Put test evidence, limitations, and handoff context in the pull request.
- Never place secrets, brokerage credentials, account data, licensed datasets,
  or material non-public information in issues, comments, commits, or logs.
- Agents may comment on and review each other's work, but risk-control and
  financial-model changes require independent authorized approval before merge.
- This project is intended to be public open source. Treat every issue, pull
  request, commit, artifact, and log as public; never upload restricted source
  material unless its license permits public redistribution.
