# Hedge Desk Agent Rules

- Keep the system paper-only until a separately reviewed release explicitly
  introduces read-only brokerage access.
- Never bypass, weaken, or silently default a failed risk or compliance gate.
- Use `Decimal` for money and portfolio ratios used in approval decisions.
- Every decision must retain reason codes and enough inputs to reproduce it.
- Tests must be deterministic: fixed clocks, fixtures, and random seeds.
- Financial-model changes require reference cases and independent review.
- An agent may implement and test a change but may not approve its own
  risk-control change for release.

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
