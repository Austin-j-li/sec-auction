# Phase 5 (hardening): build record

Contract: [CONTRACT.md](CONTRACT.md). Built on 23 September 2026 (Austin: "build phase 5, use subagents to expedite and manage context better"). Opus 5.5 led: it wrote the contract, the docs and the migration fix, reviewed and integrated the work, and deployed. Three Opus 5.5 subagents built the rest in parallel, each owning its own files: backups (A), hiding deals (B) and the export script (C). No model was called in building or testing.

## What was built

- **Backups (A)**, `cockpit/backup.py`:
  - `create` makes an online SQLite backup, integrity-checked and stored in rollback-journal mode, plus the file store (`filings/`, `instructions/`, `versions/`, `jobs/`), into `~/backups/ledger-cockpit/<stamp>Z/` (0700).
  - Each backup has a `manifest.json` of hashes, table row counts and a per-deal summary (working copy, comments).
  - Backups are written atomically and pruned after 14 days, always keeping the newest.
  - `restore` checks hashes first, refuses the live state while the services run, and with `--replace` moves the old directory aside.
  - `rehearse` backs up, restores into a temporary root and compares both through the data layer and table by table.
  - Nightly job: `cockpit/deploy/ledger-backup.{service,timer}` at 03:30 UTC.
  - Credentials are not backed up.
- **Hiding deals (B)**:
  - `hidden_deals` table and `POST /api/deals/<slug>/visibility` (`hide`/`unhide`).
  - It returns 409 when the deal is already in that state, when a run on the deal is queued or going, and on extract of a hidden deal ("unhide the deal first").
  - Activity `hide_deal`/`unhide_deal`, and `hidden`/`hidden_by`/`hidden_at` on the deal list and deal payloads.
  - UI: a ⋯ menu in the deal toolbar with **Hide deal…** and a confirm dialog; the banner "Hidden by … · Unhide"; **Show hidden (n)** under the deal list; "Deal hidden/unhidden" in the activity feed.
- **Export to repository (C)**, `cockpit/export_repo.py`:
  - `instruction <name|id>` exports published versions only, after a hash check.
  - `deal <slug> --version <id>|working` writes the Excel download's exact bytes. For added deals it also writes the filing and its `MANIFEST.csv` row.
  - Refusals: a draft instruction, a hash mismatch, and any path `catalog.json` names as an immutable original.
  - Dry run by default; `--write` writes atomically. It never commits.
- **Migration race (lead)**:
  - The cause: two connections migrating a fresh database at once could both try `ALTER TABLE … ADD COLUMN`, and the second failed with "duplicate column name". Subagent B saw this once in `test_instructions` when the browser suites ran concurrently.
  - The fix: `workspace.add_column` tolerates exactly that error, and `runs` and `trace` use it for their three added columns.
  - Test: `MigrationTests` in `test_cockpit_workspace.py`.
- **Docs (lead, spec §11)**:
  - AGENTS.md: the app exists; app versions reach the repository only through `export_repo.py` on Austin's request; the generality rule stays as guidance.
  - Cockpit README: hiding deals, backups, and corrected lines about versions and roles.
  - Tools README: backups and restore, the systemd socket recovery, the export script, and `test_instructions` in the suite list.
  - HANDOFF.

## Decisions made in the build

- The rehearsal compares the backup with its restored copy, not with the live state (which may change meanwhile). The summary in the manifest is also checked against the restored state.
- Catalog workbooks are copied into the rehearsal's temporary root rather than symlinked, because the workspace refuses paths that resolve outside the root.
- Deal hiding lives in the deal toolbar's new ⋯ menu; there was no overflow menu before.
- A deal export of a catalog deal is refused, so today only added deals (such as Medivation) can be exported. Changing the catalog stays a separate, requested edit.

## Verification (23 September, 18:00 UTC)

- **Staged build.** All suites were run at the same moment, which exercises the migration race:

  | Suite | Result |
  |---|---|
  | Python `pytest _dev/tools` | 207 passed (8 backup, 7 export, 1 hide-deal, 1 migration new) |
  | `test_http.py` | 13 passed |
  | vitest | 52 passed |
  | `test_browser` | passed (46) |
  | `test_resize` | passed |
  | `test_responsive` | passed |
  | `test_deals` | passed (25; 8 new hide checks) |
  | `test_instructions` | passed (24) |

- **Deployment.**
  1. The live state was backed up first (`~/backups/ledger-cockpit/20260923-175122Z`), plus a copy of the database in the session scratchpad.
  2. `dist/` was swapped.
  3. Both services were restarted, and the timer was installed, enabled and run once (`20260923-180000Z`).
  4. `test_runs` and `test_trace` then passed on the deployed `dist/`.
  5. Live: `/api/session`, `/api/deals` (10 deals, each with `hidden`), `/deal/medivation` and `/instructions` return 200. The next backup is 24 September 03:30 UTC.
- **Deployment incident.** `systemctl --user` could not connect: the user manager's private socket file had been replaced at 17:44, most likely by the subagent's `systemd-analyze` check of the new units. The manager was re-executed over D-Bus, after which the services, including `cloudflared`, stayed active. The recovery command is in the tools README.
- **Acceptance (spec §12):**
  - `backup.py rehearse` on the live state gave `{"deals": 10, "working_copies_equal": true, "comments_equal": true, "differences": []}` (backup `20260923-180006Z`).
  - The live database holds no saved revisions or comments yet, so the live rehearsal exercises the machinery on empty history.
  - Reproducing saved edits, comment replies, edits and resolutions, a hidden version, an added deal, a hidden deal and a draft instruction is shown on the fixture in `test_cockpit_backup.py`.
  - Rerun `rehearse` once real edits and comments exist.

## Not yet done

- Acceptance runs from earlier phases (real model runs needing Austin's go-ahead): Alex's first run (phase 2), a seed deal and a pasted-link deal extracted end to end (phase 3), and the draft/published and per-engine runs (phase 4).
- Confirm on 24 September that the nightly backup ran (03:30 UTC) and that the ChatGPT login refresh renewed a login.
