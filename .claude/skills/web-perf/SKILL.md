---
name: web-perf
description: Use when changing dashboard or web UI code, or when pages feel slow. Measures and optimizes web performance, accessibility, and SEO basics — Core Web Vitals, bundle size, rendering strategy, caching, images, and API latency — with before/after numbers.
argument-hint: "[optional: route/page or area to focus on]"
effort: high
---

# /web-perf — Measure, fix, prove

> **Repo rules win.** `CLAUDE.md` (and any `SOUL.md` / `AGENTS.md` it imports) overrides anything in this workflow, including its "Workflow overrides" section.

Focus: **$ARGUMENTS** (empty = the most important user-facing pages).

Rule: **no optimization without a before and after measurement.**

## 1. Baseline
- Production build using the build command in `CLAUDE.md`; record bundle sizes per route (use the framework's analyzer if available).
- If a URL or local server is available, run Lighthouse (`npx lighthouse <url> --only-categories=performance,accessibility,best-practices,seo --output=json --quiet`) for mobile. Record LCP, INP/TBT, CLS, TTFB, and scores.
- Time the slowest API routes and DB queries behind those pages.

## 2. Find the biggest wins (rank by user impact ÷ effort)
- **Rendering:** right strategy per route (static / ISR / SSR / streaming); avoid client-side waterfalls; fetch data in parallel on the server.
- **JavaScript:** remove/replace heavy deps, code-split below-the-fold and rarely used components, tree-shake, avoid shipping server-only code.
- **Images/fonts:** modern formats, explicit sizes (CLS), lazy-load below the fold, preload the LCP image, `font-display: swap`, subset fonts.
- **Data:** cache API responses (HTTP cache headers, CDN, server cache) aligned with freshness SLAs in the data registry (see `CLAUDE.md` → Data sources); paginate; add missing indexes; kill N+1s.
- **Real-time data (odds, prices, scores):** prefer WebSocket/SSE or efficient polling with ETags; throttle UI updates; virtualize long tables.
- **Accessibility:** labels, contrast, keyboard nav, focus states, semantic HTML.

## 3. Fix
Apply the top items one at a time, each its own commit (`perf:` / `fix(a11y):`), re-measuring after each. Revert anything that doesn't move the number.

## 4. Report
Before/after table (bundle KB, LCP, INP/TBT, CLS, Lighthouse scores, API p95), what changed, and the next 3 opportunities not yet done.
