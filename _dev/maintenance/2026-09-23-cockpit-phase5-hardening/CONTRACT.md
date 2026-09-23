# Phase 5 (hardening) build contract

Implements the rest of [the app spec](../../COCKPIT_APP_SPEC.md): backups and a restore rehearsal (§4, §13.3), hiding deals (§13.5; hiding versions was built in phase 2) and the documentation of §11, including the optional export-to-repository script. Phases 1–4 rules stay (identity, CSRF, design, worker, versions, instructions).

Claude-only build (Austin, 23 September: "build phase 5, use subagents"): Opus 5.5 leads, writes this contract and the docs, and integrates; Opus 5.5 subagents build backups, deal hiding and the export script in parallel. Do not read `ref/`, `_dev/reviews/` or `_dev/side-notes/`. Building and testing make no model calls.

Done when (spec §12): a restore from backup reproduces the working copies and comments. Every existing suite stays green.

## A. Backups and restore (`_dev/tools/cockpit/backup.py`, new)

Standard library only. The state directory is `<repo>/_dev/cockpit/state/` (the server and `Data(repo_root)` derive it from the repository root).

- **`backup.py create [--repo-root R] [--dest D] [--keep-days 14]`**. Default destination `~/backups/ledger-cockpit/`, created with mode 0700.
  - Writes `<dest>/<YYYYMMDD-HHMMSS>Z/` atomically: build it under `<dest>/.partial-<stamp>/`, then rename.
  - `workspace.sqlite3` is copied with the SQLite online backup API (`sqlite3.Connection.backup`), never by copying the file. Run `PRAGMA integrity_check` on the copy and fail if it is not `ok`.
  - The store is copied as files: `filings/`, `instructions/`, `versions/`, `jobs/`. Leave out `lookups/` (EDGAR search caches, rebuilt on demand), `worker.lock`, and any SQLite `-wal`/`-shm` files.
  - Credentials are never backed up. They live in `~/.config/sec-extraction/users/`, outside the state directory. After a restore, users reconnect.
  - `manifest.json` records:
    - `created_at`, the source state path and the git HEAD;
    - each file's relative path, bytes and SHA-256;
    - the database's SHA-256 and its row counts per table;
    - a `summary` of working copies and comments (see below).
  - Pruning:
    - Remove finished backups older than `--keep-days`, judged by the stamp in the directory name.
    - Always keep the newest backup.
    - Never touch anything in the destination that isn't a backup directory made by this script, and remove stale `.partial-*` directories.
  - Exit non-zero with a one-line error on any failure, and print the backup path on success.
- **`backup.py restore <backup-dir> --state <dir> [--replace]`**.
  - Verify every hash in the manifest first, and restore nothing if one mismatches.
  - Restore into an empty or new directory.
  - With `--replace` on a non-empty target, move the existing directory aside to `<dir>.before-restore-<stamp>` rather than deleting it.
  - Refuse when the target is the live state directory while `ledger-cockpit` or `ledger-worker` is active (`systemctl --user is-active`).
  - The restored directory gets an empty `lookups/`.
- **`backup.py rehearse [--repo-root R] [--dest D]`**. This is the phase's acceptance check.
  1. Create a backup of the live state, restore it into a temporary repository root, and compare the two states through the same `Data`/`Workspace` code the server uses.
  2. The temporary root has the restored `_dev/cockpit/state/` and symlinks to the real checkout's other inputs: `catalog.json`, `raw_filing/`, `extraction/`, the instruction file, `ref/seed.csv` if needed, and so on. Read only what the data layer itself opens.
  3. Compare, per deal (catalog and added):
     - the working copy: the current revision number and base, and the working workbook's sheet contents as the API returns them;
     - its revision history;
     - every thread and comment, with edit history and resolved state;
     - versions, including the hidden flag;
     - added deals and hidden deals;
     - instructions, with their texts and the default.
  4. Print a JSON report `{backup, deals: n, working_copies_equal, comments_equal, differences: [...]}`. Exit 0 only when there are no differences.
  5. Delete the temporary root afterwards and keep the backup.
- **Summary used in the manifest and the rehearsal:** for each slug, the working revision and its content SHA-256 (a canonical JSON of the working sheets), plus thread and comment counts and a SHA-256 over the canonical comment rows.
- **Nightly job** (unit files in `_dev/tools/cockpit/deploy/`):
  - `ledger-backup.service` is a oneshot: `WorkingDirectory=%h/work/Projects/sec-extraction`, runs `python3 _dev/tools/cockpit/backup.py create`, with the same `Environment=` lines as the worker unit.
  - `ledger-backup.timer` uses `OnCalendar=*-*-* 03:30:00 UTC` and `Persistent=true`.
  - The lead installs both into `~/.config/systemd/user/`.
- **Tests** (`_dev/tools/test_cockpit_backup.py`) run against a fixture repository with a real workspace: saved edits, comments, a hidden version, an added deal and a draft instruction.
  - create → restore → rehearse is equal;
  - a backup taken while a writer holds the DB open is consistent;
  - a tampered file fails restore and leaves the target untouched;
  - pruning keeps 14 days and the newest, and ignores foreign directories and removes stale partials;
  - `--replace` moves the old directory aside;
  - restore is refused on the live path when services are "active" (use a fake `systemctl` on `PATH`);
  - a changed comment after the backup makes the rehearsal comparison report a difference (test the comparison function directly).

## B. Hide deals

- Storage: `CREATE TABLE IF NOT EXISTS hidden_deals (slug TEXT PRIMARY KEY, hidden_by TEXT NOT NULL, hidden_at TEXT NOT NULL)`, created where the other tables are. A row means the deal is hidden; unhiding deletes the row.
- API: `POST /api/deals/<slug>/visibility` with `{"action": "hide" | "unhide"}` (CSRF, known users, the same patterns as the version hide route).
  - Unknown slug → 404.
  - Hiding an already hidden deal, or unhiding one that is shown → 409.
  - Hiding a deal with a queued or running job (extraction or fetch) → 409 "a run on this deal is still going".
  - Activity kinds `hide_deal` / `unhide_deal` on that slug: "Hid the deal" / "Unhid the deal".
- The deal list API gives each deal `hidden: bool` (plus `hidden_by` and `hidden_at`). The page hides hidden deals from the deal list by default for both users. A "Show hidden (n)" toggle at the foot of the list shows them, dimmed and marked "Hidden", with **Unhide**.
- A hidden deal still opens by URL, with a banner "Hidden by Alex on 23 Sep · Unhide". Its data, versions, comments and working copy are untouched. Nothing is ever deleted.
- **Hide deal** is in the deal's header overflow menu or wherever version Hide lives, with a confirm dialog: "Hide <deal> for both of you? It stays in the store and can be shown again."
- What's new, the digest and the Activity page still show hidden deals' activity. The deal list's unread badges show only for visible deals.
- Extract and Add-and-extract on a hidden deal → 409 "unhide the deal first". Hiding does not affect adding a new deal with the same filing (the slug is already taken, as now).
- Tests:
  - Python: hide/unhide, the 409s, activity, list flag, persistence;
  - `test_http.py`: route, CSRF;
  - vitest for any new pure helper;
  - browser: extend `test_deals.mjs` (or a new small suite) for hiding a deal, the toggle, the banner and unhiding.

## C. Export to repository (`_dev/tools/cockpit/export_repo.py`, new, admin-only script, not a button)

For a commit Austin requests. The script never commits and never calls a model or the network.

- **`export_repo.py instruction <name-or-id> [--write]`**. Only published versions can be exported. It writes the stored text into `SEC_Deal_Ledger_Extraction_Instruction.md` and first checks that the stored text's SHA-256 matches its content address.
- **`export_repo.py deal <slug> --version <id>|working [--write]`**:
  - It writes the version's workbook (or the working copy exported as Excel, through the same export code as the server's download) to `extraction/<slug>.xlsx`.
  - For a deal added in the cockpit, it also writes the filing to `raw_filing/<file>` and adds or updates its `raw_filing/MANIFEST.csv` row in that file's existing format.
  - It refuses to overwrite a path that `catalog.json` references as an immutable original. It says so, and says that the catalog must be changed by a separate, requested edit.
- Both default to a dry run that prints each target path, its current SHA-256 (or "new") and its new SHA-256. `--write` writes atomically and prints the same lines.
- Tests (`_dev/tools/test_cockpit_export.py`), on a fixture repository:
  - a dry run changes nothing;
  - write for a published instruction;
  - a draft is refused;
  - a hash mismatch is refused;
  - a deal export of an added deal writes the workbook, filing and manifest row;
  - a catalog-referenced target is refused.

## D. Documentation (§11, lead)

- **AGENTS.md** and **HANDOFF.md** say:
  - extractions may be started in the app by Austin or Alex, and instructions versioned there, with either able to change the default;
  - the rule that instruction changes must be general stays as guidance;
  - repository changes still go through `export_repo.py` on Austin's request.
- **Cockpit README:** accounts, adding deals, running, versions (hide), deals (hide), comments, what's new, instructions, backups.
- **Tools README:** per-user credentials, engines, the worker, backups (create, restore, rehearse, timer), and the export script.

## Deployment (lead)

Before deploying:
1. Take an online backup of the live DB with the new script, plus an extra copy in the scratchpad.

Deploy:
2. Rebuild `dist/`.
3. Restart both services.
4. Install and enable the timer, and run `ledger-backup.service` once.
5. Run `backup.py rehearse` on the live state. That is the acceptance evidence.

Record everything in PROGRESS.md.
