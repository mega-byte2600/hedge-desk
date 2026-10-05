## Consolidate Options Guide into Workbench

The standalone Options Guide page is removed. The Workbench now has top-level
**Workbench | Guide** tabs; the Guide tab embeds the existing visual guide plus
a download link. Less is more: one fewer page, same content.

### Changes
- `web/options-workbench-ui.js`: top-level tabs + `guidePanel()` (iframe + download)
- `web/app.js`: guide route removed (title, function, dispatch)
- `web/index.html`: Guide nav entry removed
- `web/styles.css`: `.wb-toptabs`, `.wb-download`
- `tests/test_public_web_surface.py`: dispatch assertion updated

### Verification
- [ ] CI green on branch
- [ ] Workbench tabs switch; guide iframe renders; download works (phone width)
- [ ] No Guide nav entry; `#guide` falls back cleanly
- [ ] Render deploy confirmed after merge

Guide content (`docs/guides/selling-options-premium-visual-guide.html`) untouched.
