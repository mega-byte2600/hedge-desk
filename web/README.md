# Emporion web console

Dependency-free, responsive operator website over the repository's existing
paper research engine. Includes six research-desk views, declared scenario records,
release requirements, provenance, JSON/Markdown downloads and browser-local
Yellow Sheets. There are no trade authorization or order submission endpoints.

## Run locally

From the repository root:

```sh
python scripts/build_web.py
python -m http.server 8080 --directory web --bind 127.0.0.1
```

Open http://localhost:8080. The export runs the existing report publication
validator before atomically writing `web/report.json`. To use a finalized report:

```sh
python scripts/build_web.py --report /path/to/morning-report.json
```

The website displays the exported snapshot, not a running Python service.
Reload fetches that snapshot again; rerun the export and republish to update it.
All shipped data is synthetic and explicitly labeled. Frozen evaluation dates
remain visible. RoR is displayed only as a recorded engine output, with its
unvalidated model version; the web layer never calculates or changes it.

Yellow Sheets are browser-local research notes, not authoritative audit records
or human authorizations. Export notes before clearing browser storage or moving
to another device. They are never sent to a server.

## Brand

Public presentation uses the Emporion Institutional Seal with the approved
**Markets · Intelligence · Discipline** brand line and **A Bolton Investment Group (BIG) Project** attribution.

## Verify

```sh
node --check web/app.js
node --test web/core.test.mjs
python -m unittest discover -s tests
```

The static directory can be served by standard static hosting, including GitHub
Pages. No JavaScript dependencies, paid APIs, database or always-on server are
required. Google Fonts is optional; system fonts render if it is unavailable.
Sites deployment identity is in `.openai/hosting.json`.
