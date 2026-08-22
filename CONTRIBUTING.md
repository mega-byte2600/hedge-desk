# Contributing to Hedge Desk

Hedge Desk accepts human- and agent-authored contributions through GitHub. The
same evidence and control boundaries apply regardless of who wrote the patch.

## CLI-first workflow

```bash
gh issue create --template agent-task.yml
git switch -c agent/<issue-number>-<short-name>
python -m pip install -e '.[test]'
python -m coverage run -m unittest discover -s tests -v
python -m coverage report
gh pr create --fill
gh pr checks --watch
```

Each increment should be small, runnable, deterministic, and linked to a
bounded issue. Use the pull-request template and include the exact verification
commands and results. A green workflow is evidence, not permission to merge or
trade.

## Protected boundaries

- Agents, LLMs, orchestration code, and model training code must not generate,
  modify, validate, or override authoritative Risk of Ruin inputs or results.
- Do not add a live broker/order adapter, credentials, customer data, MNPI, or
  licensed raw market-data payloads.
- Keep STAT outputs distinct from BIG agent/model proposals and from HUMAN
  decisions.
- Compliance, deterministic risk, Back Office reconciliation, and release
  `BLOCK` results are not human- or agent-overridable.
- Material risk, model, data, compliance, or licensing changes require an ADR
  and independent review.

## Definition of done

- deterministic happy-path and failure-path tests;
- at least the repository-wide 80% branch-coverage floor;
- Python 3.9, 3.11, and 3.13 CI green;
- no secrets or redistributability violations;
- paper/live and hypothetical/real results labeled truthfully;
- exact source, data, code, policy, and artifact hashes retained where the
  relevant contract requires them.
