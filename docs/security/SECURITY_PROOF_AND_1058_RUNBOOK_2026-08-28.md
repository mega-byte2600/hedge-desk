# Security Proof and 10:58 Runbook - 2026-08-28

## Current Proof

- Local deterministic tests pass: `24/24`.
- Demo generation succeeds and writes the HTML, desk packets, and local SQLite paper ledger.
- Local source scan found no real Schwab client secret, OAuth token, GitHub token, AWS key, private key, or OpenAI key in committable files.
- The only local scan hits are code field names and placeholder strings:
  - `access_token` in the Schwab read-only adapter
  - `client_secret` placeholder in `config/schwab.example.json`
- Real Schwab config stays in `config/schwab.local.json`, which is excluded by `.gitignore`.

## GitHub Facts Verified

- Repository: `mega-byte2600/hedge-desk`
- Default branch: `main`
- Current `main` commit observed: `17ae1e484175d8c3a0f747f59b80d42e468a2cfd`
- GitHub branch list reports `main` as `protected: false`.
- Active ruleset exists and blocks branch deletion and non-fast-forward rewrites.
- That ruleset does not yet prove required pull requests, required reviews, required checks, or signed commits.
- GitHub remote already has CI and CodeQL workflow files.
- GitHub remote did not show `SECURITY.md` before this runbook was prepared.

## Schwab Credential Boundary

Never commit, paste, screenshot, or upload:

- `config/schwab.local.json`
- Schwab client secret
- OAuth authorization code
- access token
- refresh token
- brokerage account numbers
- SQLite account snapshots
- paid/licensed market-data payloads

Allowed in GitHub:

- fake placeholders
- source code
- tests
- paper-only reports
- fixture data
- architecture/security docs

## Manual GitHub Lockdown

In GitHub repository settings:

1. Protect branch `main`.
2. Require pull requests before merging.
3. Require at least one approval.
4. Dismiss stale approvals after new commits.
5. Require status checks to pass before merging.
6. Require branches to be up to date before merging.
7. Require conversation resolution.
8. Require signed commits if available.
9. Do not allow bypassing if available.
10. Keep force pushes disabled.
11. Keep branch deletion disabled.
12. Enable dependency graph, Dependabot alerts, Dependabot security updates, CodeQL/code scanning, secret scanning, and push protection.
13. Set Actions workflow permissions to read-only.
14. Disable GitHub Actions ability to create or approve pull requests.

## Tomorrow Morning Startup

From `/Users/cebu/Documents/BIG`:

```bash
python3 -m unittest discover -s tests -v
python3 -m hedge_desk.demo
python3 -m hedge_desk.server
```

Then open:

- `http://127.0.0.1:8765/demo`
- `http://127.0.0.1:8765/schwab/setup`

Paper-only rule:

- Schwab can be connected for auth/status and later read-only market/account data.
- Order placement remains disabled.
- Any endpoint that attempts broker orders must return blocked/forbidden until a separate live-release gate exists.
