# Version 1 switch-over

This is a runbook for Austin's later order. None of these deployment steps was run during the build. Approval of the build and permission to switch the live app are separate from building it. Do not submit an extraction during the switch-over checks.

## Prepare the approved commit

The build commit contains a draft; its root instruction remains Version 0. After Austin approves the draft, put that approved text at `SEC_Deal_Ledger_Extraction_Instruction.md`, complete the documentation updates in DRAFTING_SPEC section 10, and commit and push on `version-1`. Record the full approved commit ID here or in the deployment record. Do not deploy the earlier build commit as Version 1.

Create a separate deployment worktree at that exact commit, from the development clone. Substitute the reviewed commit ID for the placeholder:

```bash
cd ~/work/Projects/sec-auction
git worktree add --detach ~/work/Projects/ledger-live APPROVED_COMMIT
git -C ~/work/Projects/ledger-live rev-parse HEAD
```

Check that the root instruction matches the approved draft byte for byte and says Version 1. The deployment folder stays detached at this commit. Subsequent development happens in `sec-auction`, never in a running deployment folder. If `ledger-live` already exists, inspect it and select a new deployment path rather than deleting or repurposing it.

Check disk space on both `/` and `~/work`; use `~/work/tmp` for scratch files. Confirm the existing unit files and drop-ins, the current live path, backup destination and external credential location without printing credentials. In the archived implementation, the accounts table stores account metadata; provider credentials live under `~/.config/sec-extraction/users` unless `COCKPIT_TOKEN_ROOT` overrides it. Retain the same Unix user and credential location. Neither the state-copy script nor this build copies or displays that external store.

## Close submissions and drain the old worker

First stop the cockpit server, so no new jobs can be submitted:

```bash
systemctl --user stop ledger-cockpit.service
```

Leave the old worker running until every queued or active job has finished. Inspect the old database through a read-only SQLite connection and print only job IDs, kinds, states and runner PIDs:

```bash
python3 - <<'PY'
import pathlib, sqlite3
p = pathlib.Path.home() / 'work/Projects/sec-extraction/_dev/cockpit/state/workspace.sqlite3'
with sqlite3.connect(p.as_uri() + '?mode=ro', uri=True) as db:
    for row in db.execute("SELECT id, kind, state, pid FROM jobs WHERE state NOT IN ('completed','failed','cancelled') ORDER BY created_at"):
        print(row)
PY
```

If a job stalls, stop the switch-over and resolve that job deliberately; do not discard it or assume stopping the worker stops its runner. Confirm all runner PIDs from the database and any extraction runner processes using the old repository have exited. Inspect process command lines and working directories without dumping their environments. The worker uses `KillMode=process`, and runners have their own sessions, so runners can outlive it.

When the queue is drained and all runners have exited, stop the worker and backup timer. If the backup service is currently running, let it finish before continuing:

```bash
systemctl --user stop ledger-worker.service ledger-backup.timer
systemctl --user is-active ledger-backup.service
```

## Back up and build fresh state

Take a final backup with the old app's backup command after the drain. Use a new dated destination under `~/backups/ledger-cockpit/` to avoid pruning earlier backups. Also archive the complete old state as a dated tarball in `~/backups/`, with restrictive permissions. Verify the archive can be listed and the database backup passes `PRAGMA integrity_check`. Record paths, timestamps and file hashes, never credentials. Keep the old state and checkout unchanged for rollback.

For example, with a unique deployment timestamp supplied by the operator:

```bash
umask 077
python3 ~/work/Projects/sec-extraction/_dev/tools/cockpit/backup.py create \
  --repo-root ~/work/Projects/sec-extraction \
  --dest ~/backups/ledger-cockpit/version-1-TIMESTAMP
tar -czf ~/backups/ledger-state-before-version-1-TIMESTAMP.tgz \
  -C ~/work/Projects/sec-extraction/_dev/cockpit state
tar -tzf ~/backups/ledger-state-before-version-1-TIMESTAMP.tgz >/dev/null
```

Build the new state with the deployment script's two positional paths:

```bash
python3 ~/work/Projects/ledger-live/_dev/tools/cockpit/fresh_state.py \
  ~/work/Projects/sec-extraction/_dev/cockpit/state \
  ~/work/Projects/ledger-live/_dev/cockpit/state
```

The destination `ledger-live/_dev/cockpit/state` must be absent. The script is read-only toward its source. It retains accounts, the four added deals and their filings; the nine repository catalog deals are already present with no workbook version. It omits instructions, default settings, jobs, activity, comments, runs, working copies and their review history. It refuses an existing destination.

Before starting the app, verify the fresh database has the same accounts and four added-deal rows and matching filing hashes, no old instruction/default setting, and no old work or jobs. Do not print account contents. Preserve the archived eight edited working copies: their judgments must be carried into Version 1 reviews by hand after Austin authorizes extractions.

Build the frontend in the deployment folder:

```bash
cd ~/work/Projects/ledger-live/_dev/tools/cockpit/frontend
npm ci
npm run test
npm run build
```

## Point services at the approved deployment

Keep existing unit files and unrelated drop-ins. Add a dedicated `40-version-1-deploy.conf` under each of `ledger-cockpit.service.d`, `ledger-worker.service.d` and `ledger-backup.service.d` in `~/.config/systemd/user/`. For the cockpit:

```ini
[Service]
WorkingDirectory=%h/work/Projects/ledger-live
ExecStart=
ExecStart=/usr/bin/python3 %h/work/Projects/ledger-live/_dev/tools/cockpit/server.py --port 8778
Environment=TMPDIR=%h/work/tmp
```

For the worker, use the same WorkingDirectory and TMPDIR, clear ExecStart, and set `ExecStart=/usr/bin/python3 %h/work/Projects/ledger-live/_dev/tools/cockpit/worker.py`. For the backup service, use the same WorkingDirectory, clear ExecStart, and set `ExecStart=/usr/bin/python3 %h/work/Projects/ledger-live/_dev/tools/cockpit/backup.py create`. Preserve its existing backup destination and timer schedule. The backup service needs no TMPDIR override.

This implements the archived `deploy/PROPOSED-tmpdir.md` fix for the cockpit and worker as part of the authorized switch-over. Create `~/work/tmp` first. Keep a copy of the installed drop-ins in the deployment record. If a file with that name already exists, inspect it instead of overwriting it blindly.

```bash
mkdir -p ~/work/tmp
systemctl --user daemon-reload
systemctl --user start ledger-worker.service ledger-cockpit.service ledger-backup.timer
systemctl --user status ledger-cockpit.service ledger-worker.service ledger-backup.timer
```

Verify the effective WorkingDirectory and ExecStart of all three services, and TMPDIR for cockpit and worker. Do not dump complete process environments. Confirm only the approved deployment supplies their Python code and frontend.

## Check the live site without submitting a run

Under Austin's and Alex's existing sign-ins, check that the deal list contains thirteen deals and that a deal with no version opens with its filing. Check the instruction pages and Add Deal's seed search and lookup; an EDGAR lookup is allowed during the ordered deployment but is not an extraction. Confirm accounts appear connected without reconnecting or revealing tokens.

Fresh state seeds the repository instruction as the first published version and default. At an approved deployment that is Version 1. Austin checks the text/hash, publication and default under his account. If it is already published and default, record that verification; do not create a duplicate publication just to change attribution. If Version 0 appears, stop: the deployed commit is wrong. Do not patch the live instruction file in place. If an explicitly approved alternative workflow requires manual publication, Austin publishes the approved Version 1 text and sets it as default under his account.

The empty catalog cannot demonstrate ledger editing until a version exists. Use the isolated, hand-made Version 1 fixture checks from the build for editing, saving, the Review checker line and Q/R links; keep that fixture out of the real thirteen-deal state. On the real site, inspect the run form only, and stop before submission. Do not leave a queued extraction as a test: the worker can start it within seconds. Record live ledger editing and the real model path as untested until Austin authorizes a real extraction.

## Roll back

Close submissions again by stopping the new cockpit. Let any authorized new jobs and their runner processes finish, then stop the new worker and backup timer. Preserve the new deployment's state for diagnosis. Remove only the three `40-version-1-deploy.conf` files created by this switch-over, run `systemctl --user daemon-reload`, and start the old worker, cockpit and backup timer. The original units point back to the old checkout and untouched state. Verify their effective paths and the old site's operation. Any separately installed TMPDIR drop-in should be removed only if it was part of this deployment and is being rolled back. Keep unrelated public-origin drop-ins.

## One week after a clean switch-over

After Austin confirms a week of clean operation, verify the archive branches and `~/backups/vm-checkouts-2026-09-27.tgz` are recoverable, the old state backup is intact, and no service, runner, worktree or agent uses either old folder. Then remove `~/work/Projects/sec-extraction`, `~/work/Projects/sec-extraction-v114` and any archived `dist.old` under those retired folders. Use Git worktree removal for a registered worktree. Keep the deployment worktree, development clone, backups and other projects. This cleanup is a later authorized action, not part of this build.
