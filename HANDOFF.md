# HANDOFF — Options Guide consolidation
Branch: `toby/options-guide-consolidation` | Commit: 50744360 | Date: 2026-10-04

## What changed (user-directed: "less is more")
The standalone Options Guide page is gone. The Workbench now has top-level
**Workbench | Guide** tabs — the Guide tab embeds the same visual guide
(`/guide/selling-options-premium`, same iframe + autofit) plus a
**Download guide** link. One fewer page, same content.

## Files
- `web/options-workbench-ui.js` — top-level tabs in `mountWorkbench()` + `guidePanel()` (iframe + download link)
- `web/app.js` — removed guide route (title map, `guide()` function, dispatch entry)
- `web/index.html` — removed Guide sidebar nav entry
- `web/styles.css` — `.wb-toptabs`, `.wb-download` (2 rules; tab bar reuses `.wb-tabs`/`.wb-tab`)
- `tests/test_public_web_surface.py` — dispatch assertion updated to `journal,resources,workbench`

## Verified by Toby
- `node --check` passes on both modified JS files; test file parses.
- No dangling `#guide` / `data-nav="guide"` / `guide()` references in app.js or index.html.
- Guide content file and its `/guide/` serving untouched.

## Sol: verify before merge
1. CI green on the branch.
2. Workbench loads; Workbench | Guide tabs switch; guide iframe renders; download works. Phone width.
3. No Guide nav entry; `#guide` hash no longer routes anywhere (falls back to candidates).
4. Merge to main when clean; confirm Render deploy.
