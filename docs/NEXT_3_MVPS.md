# Next 3 MVPs

## Purpose

Organize the open-source roadmap so the public GitHub repo shows what is being built without exposing credentials, accounts, licensed data, or live-trading capability.

## MVP 1: Risk, Compliance, Data Foundation

Status: runnable local demo.

Includes:
- local backend
- delayed market tape
- risk-of-ruin gate
- account/compliance gate
- policy plane
- source contracts
- audit chain
- Schwab read-only boundary
- no agent order placement

## MVP 2: Dividend Premium/Capture Paper Desk

Goal:
- identify dividend-related paper candidates using ex-date timing, dividend amount/yield, price-gap risk, account fit, and optional premium overlay.

Controls:
- ex-dividend source validation
- dividend amount/yield timestamp
- account tax fit
- price-drop risk
- DTE/premium/extrinsic value when options are used
- risk-of-ruin under 4%
- paper only

## MVP 3: Earnings Event Paper Desk

Goal:
- identify earnings-event premium candidates using event timing, expected move, IV rank, DTE, defined-risk setup, account fit, and source boundary.

Controls:
- earnings calendar source validation
- expected move / IV source boundary
- DTE event-risk gate
- defined-risk options only
- risk-of-ruin under 4%
- paper only

## Public Repo Rule

GitHub shows architecture, code, tests, fixtures, and status. GitHub must not contain broker credentials, account data, OAuth tokens, paid/licensed market data, or live order-routing capability.
