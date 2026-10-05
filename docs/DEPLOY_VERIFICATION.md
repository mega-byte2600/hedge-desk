# Deploy Verification Standard

**Origin:** 2026-10-04 About incidents (#146/#149/#150/#151). Sol set this bar
after calling "live" and "demo-ready" while browsers were still serving stale
cached JS (304 Not Modified on unchanged `?v=` strings).

**Rule (Lesson 9, made concrete):** merged is not deployed, deployed is not
correct, and correct-on-the-server is not correct-in-the-browser. No status
claim stronger than what was actually measured.

## The 4-point bar — all four, every deploy

1. **PR merged.** The fix commit is on `main` (not just approved, not just
   green — merged).
2. **Render on the exact SHA.** Production serves the merge commit's SHA,
   verified via the GitHub API (`/repos/.../commits?per_page=1`), not via
   "deploy succeeded" logs.
3. **Browser fetches fresh assets.** Production serves the NEW asset URLs.
   Verify with a real browser hard-reload: open DevTools network, confirm
   the changed JS/CSS return 200 (not 304), and that the `?v=` query strings
   differ from the previous deploy. A 304 on a changed file means the
   cache-bust failed and the browser is running stale code.
4. **Rendered page verified.** Load the affected route in a real browser and
   confirm the fix visually: the exact invariant the PR claimed (e.g., one
   logo, content present). `node --check` and static previews are not
   verification.

**Status vocabulary (use exactly these, no stronger):**
- "Merged" = point 1 only.
- "Deployed" = points 1+2.
- "Live" = points 1+2+3.
- "Demo-ready" = all four. Nothing else earns the word.

## Recommended hardening: content-hash cache-busting (proposed, not yet adopted)

**The defect:** `?v=` strings in `web/index.html` are hand-maintained
(`?v=20261004-sitewide`). Every deploy requires a human to remember to bump
them. Forgetting = browsers serve stale JS indefinitely while every
server-side check stays green. This is what happened on 2026-10-04.

**The poka-yoke:** version strings must be derived from file content, never
hand-written. Convention: `?v=` = first 12 chars of the file's SHA-256.
A CI test (`tests/test_asset_cache_bust.py`, proposed) asserts the invariant
for every versioned asset in `index.html`. Changing a JS file without
updating its hash fails the build — the manual step becomes unskippable.

**Adoption note:** PR #151 used manual date strings (`?v=20261005-about-recovery`).
Migrating to content-hash requires a one-time `index.html` update. Coordinate
with Sol; do not change the convention unilaterally while #151 is open.
