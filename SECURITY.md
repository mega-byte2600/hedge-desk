# Security Policy

## Reporting Security Issues

Do not open public issues containing secrets, account data, broker tokens, or
exploit details. Use private contact with the repository owner.

## Scope

In scope:
- credential exposure
- broker/API token handling
- order-placement boundary bypass
- account-data leakage
- source/licensed-data leakage
- risk/compliance gate bypass

Out of scope:
- requests to enable live trading
- requests for account-specific financial advice

## Current Safety Position

- The MVP is paper-only.
- Schwab integration is read-only scaffolded.
- Agent order placement is blocked.
- Delayed data is marked as delayed.
- Local secrets must stay out of GitHub.
