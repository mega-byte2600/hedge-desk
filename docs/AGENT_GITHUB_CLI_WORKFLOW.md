# Agent GitHub CLI Workflow

GitHub issues, branches, pull requests, reviews, and comments are the durable
communication channel for coding agents. Chat may coordinate work, but decisions
and verification evidence belong in GitHub.

## Human setup

Install and authenticate GitHub CLI, then create the private repository:

```bash
gh auth login
gh repo create hedge-desk --private --source=. --remote=origin --push
```

Change `--private` only after an explicit decision to publish the project.

## Start an agent task

```bash
gh issue create --template agent-task.yml
gh issue develop ISSUE_NUMBER --checkout
```

If `gh issue develop` is unavailable, use:

```bash
git switch -c agent/ISSUE_NUMBER-short-description
```

Each branch addresses one bounded issue. Agents read `AGENTS.md` before making
changes and post a short claim comment before editing:

```bash
gh issue comment ISSUE_NUMBER --body "Claimed by AGENT_NAME. Scope: SHORT_SCOPE."
```

## Report progress and blockers

```bash
gh issue comment ISSUE_NUMBER --body-file progress.md
```

Comments should contain facts that another agent can act on: files inspected,
decisions made, checks run, exact failures, and remaining work. Do not publish
credentials, private market data, account identifiers, or proprietary datasets.

## Submit work

```bash
python3 -m unittest discover -s tests -v
git status --short
git add -- PATCHED_FILES
git commit -m "type: concise change (#ISSUE_NUMBER)"
git push -u origin HEAD
gh pr create --fill --body-file pull-request.md
```

An agent must not merge its own risk-control or financial-model change. Such a
pull request requires locked reference cases and independent human or separately
authorized reviewer approval.

## Review and handoff

```bash
gh pr view PR_NUMBER --comments
gh pr checks PR_NUMBER --watch
gh pr review PR_NUMBER --comment --body-file review.md
```

Only an authorized human records final approval for risk-control changes and any
future execution capability. A GitHub approval does not itself constitute trade
authorization; trade authorization must be stored in the application's audit
contract for the specific proposed trade.

