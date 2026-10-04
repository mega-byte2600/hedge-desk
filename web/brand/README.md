# Emporion brand assets

## THEME DIRECTIVE — NOIR ONLY
The approved theme is Noir Institutional: near-black backgrounds, muted
brass as the single accent, warm-white typography, green ONLY for
live-data semantics. Fraunces headlines/wordmark, Inter body, IBM Plex
Mono numerals. A navy/cream shell is NOT approved — restyle to noir.

## Official logo (current)
`emporion-logo-hermes.jpg` — 1260x1260 JPEG, delivered 2026-10-04.
Golden bust of Hermes wearing a winged helmet in profile, compass rose
behind (N/E/S/W), EMPORION wordmark with a compass star as the O.
Note: the JPEG has a white background.

## Transparent version (no white background)
`emporion-logo-hermes-transparent.png` — 1260x1260 PNG with alpha channel.
White background and drop shadow removed (edge flood-fill with
saturation-aware masking, feathered edges). Verified clean on dark and
white. USE THIS EVERYWHERE — marketing and web. For web, downscale
as needed (the 1260px master is ~2.2 MB; a 512px copy is plenty for UI).

## Website integration (for Sol)
1. In `web/index.html`, swap the 2 references from
   `./brand/emporion-logo-hermes.jpg?v=20261004` (one `src`, one `href`)
   to `./brand/emporion-logo-hermes-transparent.png`.
2. REQUIRED: add `"brand/emporion-logo-hermes-transparent.png"` to
   `CONSOLE_ASSETS` in `scripts/build_web.py`. Without it the Python 3.11
   white-box gate fails and main goes red (same trap as `f868c8dd`).
3. QA at 390px: noir theme throughout, single logo in the sidebar,
   no white box, no legacy seal.

## Build verifier notes
`scripts/build_web.py` (patched `6dddbd2a`): the asset extractor strips
`?v=` cache-busters, and the disk check resolves `web/brand/` and
`web/vendor/` via relative paths. Unknown assets still fail the gate.

## Site emblem
`web/emporion-institutional-seal.svg` — "Hermes compass emblem" (SVG):
gold Hermes profile in a winged helmet over a compass rose.
Currently used in the site nav and overview brand bar.

## Superseded
The `toby/seal-redraw` branch iterations (empty-helm concepts, no face) —
rejected and replaced. Do not use for new work.
