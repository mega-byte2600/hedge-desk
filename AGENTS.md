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
