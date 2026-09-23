# Phase 1 (trace): build record, 23 September 2026

Contract: [CONTRACT.md](CONTRACT.md). Claude-only build at Austin's direction: Opus 5.5 wrote the contract, the backend and the tests, and integrated and deployed; an Opus 5.5 subagent wrote the frontend; Fable 5.1 gave one second-opinion review of the backend before deployment.

## What changed

- Backend: new `_dev/tools/cockpit/trace.py` (threads, comments, edit history, activity, per-user seen markers, legacy-note migration); `workspace.py` records one activity row per save in the same transaction and exposes `record_label`; `server.py` adds `GET/POST /api/deal/<slug>/comments`, `GET /api/deal/<slug>/activity`, `POST /api/deal/<slug>/seen`, `GET /api/activity`, the `/activity` page route, and `field_authors`, `thread_counts`, `seen` and `unseen` in existing payloads.
- Frontend: `Comments.jsx`, `WhatsNew.jsx`, `Activity.jsx`, `trace.js` (+ tests); comments in every editor and in Review; the note textareas replaced by comments; initials and thread marks in lists; last-changed-by on field labels; the overview digest line. The version dropdown labels were shortened to "Working copy · editable" and "… · original, read only" so they fit.
- Acceptance: `test_trace.mjs` (two users through the Access header), `serve_fixture.py --two-users`; `test_browser.mjs` and `test_resize.mjs` updated for the removed note fields.

## Fable review (applied)

No material defect. Applied: the first-run note migration now runs in its own `BEGIN IMMEDIATE` transaction and closes its connection on failure; a save's activity row uses the revision's timestamp; out-of-range `before`/`activity_id` values return 400. The suggested extra `test_http.py` cases were not added: `test_cockpit_trace.py` already covers bad CSRF, unknown-user writes and GET-only misuse through the real server.

## Verification

- Python: `cd _dev/tools && python3 -m pytest -q` — 148 passed, 57 subtests (includes 8 new trace tests).
- Frontend: 12 vitest tests; `npm run build`.
- Browser (synthetic fixture, private Chrome): `test_browser.mjs` 46 passed; `test_resize.mjs` and `test_responsive.mjs` passed with no browser errors; `test_trace.mjs` 13 passed (Alex edits and comments, Austin's overview and What's new show it with the `AG` row mark, Austin replies, Mark as read clears and Mark unread restores, Alex's digest shows Austin's reply, the Activity page lists it, an unknown reader gets read-only comments, no console errors).
- Deployment: `ledger-cockpit.service` restarted from the working tree. On loopback, `/activity` serves the page; `/api/deals` returns `unseen` for all nine deals; comments, field authors and seen are empty; GET requests did not create `_dev/cockpit/state/`. The public route redirects to Cloudflare Access (302), as before. No authenticated public session was exercised.
