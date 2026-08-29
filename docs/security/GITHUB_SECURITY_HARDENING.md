# GitHub Security Hardening Plan

## Goal

Keep the repository open enough to show the work, but locked down enough that
outsiders cannot use the public setup to cause damage, steal secrets, or sneak
unsafe trading behavior into the codebase.

## Immediate Repository Controls

- Keep the repository public, but treat `main` as protected.
- Require pull requests before merging to `main`.
- Require at least one review for every pull request.
- Require status checks to pass before merge.
- Require branches to be up to date before merge when practical.
- Block force pushes to `main`.
- Block branch deletion for protected branches.
- Restrict who can push directly to `main`.
- Enable secret scanning and push protection if available.
- Enable Dependabot alerts and security updates if dependencies are added.
- Enable code scanning once workflows are active.

## Files That Must Never Be Committed

- `config/schwab.local.json`
- `.env`
- `.env.*`
- broker tokens
- OAuth refresh tokens
- account numbers
- brokerage statements
- SQLite files containing account snapshots
- raw source payloads containing licensed data

## Open Source Boundary

Allowed in GitHub:
- architecture
- docs
- source code
- fixtures with fake/deterministic data
- tests
- security policy
- contribution rules
- paper-only demos

Blocked from GitHub:
- real Schwab credentials
- live account data
- paid/licensed market data
- personal account identifiers
- live order-routing capability

## Pull Request Gate

Every PR must answer:

- Does this add or alter trading behavior?
- Could this enable live orders?
- Does this touch Schwab, broker, auth, account, or token logic?
- Does this include new dependencies?
- Does this change risk-of-ruin, options timing, account gates, or policy logic?
- Are tests included?
- Are sources cited when market/regulatory claims are made?

## Manual GitHub Settings To Apply

In GitHub repository settings:

1. Settings -> Branches -> Add branch protection rule.
2. Branch name pattern: `main`.
3. Enable: require a pull request before merging.
4. Enable: require approvals.
5. Enable: require status checks to pass before merging.
6. Enable: require conversation resolution before merging.
7. Disable force pushes.
8. Disable deletions.
9. Settings -> Code security and analysis.
10. Enable secret scanning, push protection, Dependabot alerts, and code scanning where available.

## Sources

- GitHub branch protection rules: https://docs.github.com/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
- GitHub secret scanning: https://docs.github.com/code-security/secret-scanning/about-secret-scanning
- GitHub Dependabot alerts: https://docs.github.com/code-security/dependabot/dependabot-alerts/about-dependabot-alerts
- GitHub code scanning: https://docs.github.com/code-security/code-scanning/introduction-to-code-scanning/about-code-scanning
