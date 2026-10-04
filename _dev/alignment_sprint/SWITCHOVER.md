# Version 1 switch-over

This file records the original fresh-state cutover. For subsequent cloud deployments, use [CLOUD_DEPLOYMENT.md](../CLOUD_DEPLOYMENT.md).
Do not repeat the state reset for a routine release. Austin's current no-tests rule overrides historical test commands below.

## Deployment record, 28 September 2026

Run on Austin's order ("hard switch and get rid of the old version").
- Deployed commit `4dd04c19c004e1e9b32a578e988a954702e52986` at `~/work/Projects/ledger-live` (detached worktree of `sec-auction`); root instruction SHA-256 `05d8668d…05de4`; committed `dist/` matched a fresh build of its source.
- Old app drained (no outstanding jobs or runners), then stopped. Final backup `~/backups/ledger-cockpit/version-1-20260928-123713/` (integrity ok) and state archive `~/backups/ledger-state-before-version-1-20260928-123713.tgz` (SHA-256 `ca3cc60b…fd82db`). The archive holds the eight edited working copies to carry into Version 1 reviews by hand.
- Fresh state: 3 accounts, 4 added deals, 4 filings; no old instructions, jobs or work. The app shows 13 deals; Version 1 is the only instruction and the default, seeded as "System".
- Drop-ins `40-version-1-deploy.conf` installed for the cockpit, worker and backup units. Cloudflare Access: team domain `https://divine-flower-e89f.cloudflareaccess.com`, AUD `8050c359…51f049` (both read from the site's Access redirect), plus `COCKPIT_REQUIRE_ACCESS=1`.
- Checks: a forged email header and an unsigned loopback request both get `unknown`, `can_edit` false; Austin's browser session via Access gets `austin`, `can_edit` true. Alex's sign-in not yet observed.
- On Austin's order the old version was then deleted without the one-week wait: `~/work/Projects/sec-extraction`, `sec-extraction-v114`, `sec-extraction-archive` and the old nightlies in `~/backups/ledger-cockpit/`. Their Git history stays on GitLab (`vm-live-2026-09-26`, `vm-v114-2026-09-26`). **Rollback below is no longer possible.** `~/backups/vm-checkouts-2026-09-27.tgz` is kept for now as the only copy of the untracked `lesson/` notes.


## Redeployment, 29 September 2026

On Austin's order ("make sol 6.1 selectable in the cockpit webapp"): no queued or active jobs; the deployment worktree moved from `4dd04c1` to `9f0750e` (GPT-6.1-Sol engine, rebuilt `dist/`, docs); `ledger-cockpit` and `ledger-worker` restarted, backup timer untouched. The served page loads the new bundle and the deployed `ENGINES` lists `sol61`.


This is a runbook for Austin's later order. None of these deployment steps was run during the build. Approval of the build and permission to switch the live app are separate from building it. Do not submit an extraction during the switch-over checks.

## Prepare the approved commit

The build commit contains a draft; its root instruction remains Version 0. After Austin approves the draft, put that approved text at `SEC_Deal_Ledger_Extraction_Instruction.md`, complete the documentation updates in DRAFTING_SPEC section 10, and commit and push on `version-1`. Record the full approved commit ID here or in the deployment record. Do not deploy the earlier build commit as Version 1.

The server serves the committed `_dev/tools/cockpit/dist/`; nothing is built at the switch-over. As part of approval, check once, in the development clone at the approved commit, that the committed build matches its source:

```bash
mkdir -p ~/work/tmp
cd ~/work/Projects/sec-auction
git rev-parse HEAD
git status --porcelain -- _dev/tools/cockpit
cd _dev/tools/cockpit/frontend
npm ci
npm run test
npx vite build --outDir ~/work/tmp/ledger-dist-check --emptyOutDir
diff -r ../dist ~/work/tmp/ledger-dist-check && echo "dist matches its source"
rm -rf ~/work/tmp/ledger-dist-check
```

`git rev-parse HEAD` must print the approved commit ID and `git status` nothing. If `diff` reports a difference, do not approve that commit: rebuild and commit `dist/`, and check the new commit before it is approved. Record the result with the commit ID. `node_modules/` stays in the development clone, ignored by Git.

Create a separate deployment worktree at that exact commit, from the development clone. Substitute the reviewed commit ID for the placeholder:

```bash
cd ~/work/Projects/sec-auction
git worktree add --detach ~/work/Projects/ledger-live APPROVED_COMMIT
git -C ~/work/Projects/ledger-live rev-parse HEAD
```

Check that the root instruction matches the approved draft byte for byte and says Version 1. The deployment folder stays detached at this commit. Subsequent development happens in `sec-auction`, never in a running deployment folder. If `ledger-live` already exists, inspect it and select a new deployment path rather than deleting or repurposing it.

Check disk space on both `/` and `~/work`; use `~/work/tmp` for scratch files. Confirm the existing unit files and drop-ins, the current live path, backup destination and external credential location without printing credentials. In the archived implementation, the accounts table stores account metadata; provider credentials live under `~/.config/sec-extraction/users` unless `COCKPIT_TOKEN_ROOT` overrides it. Retain the same Unix user and credential location. Neither the state-copy script nor this build copies or displays that external store.

### Check the frontend before the outage

The build was checked at approval. The only frontend step now is to confirm the deployment folder's committed build is untouched:

```bash
git -C ~/work/Projects/ledger-live status --porcelain -- _dev/tools/cockpit/dist
```

It must print nothing; otherwise stop.

### Prepare the Cloudflare Access settings

On the public site the new server takes a reader's identity only from the signed token Cloudflare Access sends in `Cf-Access-Jwt-Assertion` (`_dev/tools/cockpit/access.py`). It verifies the RS256 signature against the team's published keys, the issuer, the audience tag and the expiry. It ignores the `Cf-Access-Authenticated-User-Email` header, which any local process could forge. Two values from the Cloudflare Zero Trust dashboard are needed; neither is a secret:

- `COCKPIT_ACCESS_TEAM_DOMAIN`: the team domain, `https://<team>.cloudflareaccess.com`;
- `COCKPIT_ACCESS_AUD`: the Application Audience (AUD) tag of the Access application that protects `lines.dealextract.org`.

They go in the cockpit's deployment drop-in below. Without them, or if the key set cannot be fetched, nobody is signed in: the site stays readable through Access and no one can edit, run or publish. The server logs a warning at start when the public origin is set but these values are not. Check that the service's Python has the verification library: `/usr/bin/python3 -c "import jwcrypto"` (the VM's `python3-jwcrypto` package).

## Close submissions and drain the old worker

First stop the cockpit server, so no new jobs can be submitted:

```bash
systemctl --user stop ledger-cockpit.service
```

Leave the old worker running until every queued or active job has finished. Inspect the old database through a read-only SQLite connection and print only job IDs, kinds, states and runner PIDs. The query lists every job not in one of the worker's four final states (`completed`, `failed`, `timed_out`, `cancelled`), so an unexpected state shows up rather than hiding:

```bash
python3 - <<'PY'
import pathlib, sqlite3
p = pathlib.Path.home() / 'work/Projects/sec-extraction/_dev/cockpit/state/workspace.sqlite3'
with sqlite3.connect(p.as_uri() + '?mode=ro', uri=True) as db:
    for row in db.execute("SELECT id, kind, state, pid FROM jobs WHERE state NOT IN ('completed','failed','timed_out','cancelled') ORDER BY created_at"):
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

The destination `ledger-live/_dev/cockpit/state` must be absent. The script changes nothing in its source. With the old services stopped, no program has the old database open, and the script copies it byte for byte and checks it did not change meanwhile; SQLite never opens it, so no `-wal` or `-shm` file appears beside it. (If a program still had it open, the script would read it through a read-only SQLite connection instead.) It retains accounts, the four added deals and their filings; the nine repository catalog deals are already present with no workbook version. It omits instructions, default settings, jobs, activity, comments, runs, working copies and their review history, and hidden-deal marks: a deal hidden in the old app appears again and can be hidden again. It refuses an existing destination.

Before starting the app, verify the fresh database has the same accounts and four added-deal rows and matching filing hashes, no old instruction/default setting, and no old work or jobs. Do not print account contents. Preserve the archived eight edited working copies: their judgments must be carried into Version 1 reviews by hand after Austin authorizes extractions.

## Point services at the approved deployment

Keep existing unit files and unrelated drop-ins, including the cockpit's `20-public-origin.conf`. Add a dedicated `40-version-1-deploy.conf` under each of `ledger-cockpit.service.d`, `ledger-worker.service.d` and `ledger-backup.service.d` in `~/.config/systemd/user/`. Reference copies are in the deployment folder under `_dev/tools/cockpit/deploy/`. The cockpit's sets the working directory, the server, `TMPDIR` and the two Access values:

```ini
[Service]
WorkingDirectory=%h/work/Projects/ledger-live
ExecStart=
ExecStart=/usr/bin/python3 %h/work/Projects/ledger-live/_dev/tools/cockpit/server.py --port 8778
Environment=TMPDIR=%h/work/tmp
Environment=COCKPIT_ACCESS_TEAM_DOMAIN=
Environment=COCKPIT_ACCESS_AUD=
```

The worker's uses the same WorkingDirectory and TMPDIR, clears ExecStart, and sets `ExecStart=/usr/bin/python3 %h/work/Projects/ledger-live/_dev/tools/cockpit/worker.py`. The backup service's uses the same WorkingDirectory, clears ExecStart, and sets `ExecStart=/usr/bin/python3 %h/work/Projects/ledger-live/_dev/tools/cockpit/backup.py create`; it needs no TMPDIR override. Keep the timer schedule.

The new backup job writes to `~/backups/ledger-live/` (the default of the new `backup.py`) and prunes only there. The old app's nightlies stay in `~/backups/ledger-cockpit/`, which the new job never touches; they remain for rollback until Austin decides to delete them.

This implements the archived `deploy/PROPOSED-tmpdir.md` fix for the cockpit and worker as part of the authorized switch-over. Install the drop-ins without overwriting an existing file (`cp -n`; if one exists, inspect it instead), then fill in the two Access values in the installed cockpit drop-in, substituting the values prepared above for the placeholders. Keep a copy of the installed drop-ins in the deployment record.

```bash
mkdir -p ~/work/tmp
D=~/.config/systemd/user
for unit in ledger-cockpit ledger-worker ledger-backup; do
  mkdir -p $D/$unit.service.d
  cp -n ~/work/Projects/ledger-live/_dev/tools/cockpit/deploy/$unit.service.d/40-version-1-deploy.conf $D/$unit.service.d/
done
sed -i -e 's|^Environment=COCKPIT_ACCESS_TEAM_DOMAIN=$|Environment=COCKPIT_ACCESS_TEAM_DOMAIN=TEAM_DOMAIN|' \
       -e 's|^Environment=COCKPIT_ACCESS_AUD=$|Environment=COCKPIT_ACCESS_AUD=AUD_TAG|' $D/ledger-cockpit.service.d/40-version-1-deploy.conf
grep '^Environment=COCKPIT_ACCESS' $D/ledger-cockpit.service.d/40-version-1-deploy.conf
systemctl --user daemon-reload
systemctl --user start ledger-worker.service ledger-cockpit.service ledger-backup.timer
systemctl --user status ledger-cockpit.service ledger-worker.service ledger-backup.timer
```

Verify the effective WorkingDirectory and ExecStart of all three services, TMPDIR for cockpit and worker, and the two Access values for the cockpit (`systemctl --user show -p Environment ledger-cockpit`). Do not dump complete process environments. Confirm only the approved deployment supplies their Python code and frontend. The cockpit's log (`journalctl --user -u ledger-cockpit -n 50`) should show neither the start-up warning about missing Access settings nor a failed key-set fetch.

## Check the live site without submitting a run

Under Austin's and Alex's existing sign-ins, check that each is shown as signed in and may edit (the session at `/api/session` names them with `can_edit` true), that the deal list contains thirteen deals and that a deal with no version opens with its filing. From the VM, check that a forged email header gets no identity:

```bash
curl -s -H 'Host: lines.dealextract.org' -H 'Cf-Access-Authenticated-User-Email: junyu.li.24@ucl.ac.uk' http://127.0.0.1:8778/api/session
```

It must answer `"user":"unknown","can_edit":false`. Check the instruction pages and Add Deal's seed search and lookup; an EDGAR lookup is allowed during the ordered deployment but is not an extraction. Confirm accounts appear connected without reconnecting or revealing tokens. Deals hidden in the old app are shown again (fresh state carries no hidden marks); hide them again if wanted.

Fresh state seeds the repository instruction as the first published version and default. At an approved deployment that is Version 1. Austin checks the text/hash, publication and default under his account. If it is already published and default, record that verification; do not create a duplicate publication just to change attribution.

Open for Austin's decision: the seeded version is attributed to "System" (`instructions.py`, `_seed`), while BUILD_SPEC B5 says Austin publishes Version 1 under his account. This build leaves the seeding as it is until he chooses.

If Version 0 appears, stop: the deployed commit is wrong. Do not patch the live instruction file in place, and do not submit anything. Recover as follows. Stop the new cockpit, worker and backup timer. Delete the new state folder `~/work/Projects/ledger-live/_dev/cockpit/state`; it holds only copies, and the old state is untouched. Move the deployment worktree to the approved commit (`git -C ~/work/Projects/ledger-live checkout --detach APPROVED_COMMIT`) and repeat the checks under "Prepare the approved commit". Then rebuild the fresh state with `fresh_state.py` as above, verify it, and start the three units again. If an explicitly approved alternative workflow requires manual publication, Austin publishes the approved Version 1 text and sets it as default under his account.

The empty catalog cannot demonstrate ledger editing until a version exists. Use the isolated, hand-made Version 1 fixture checks from the build for editing, saving, the Review checker line and Q/R links; keep that fixture out of the real thirteen-deal state. On the real site, inspect the run form only, and stop before submission. Do not leave a queued extraction as a test: the worker can start it within seconds. Record live ledger editing and the real model path as untested until Austin authorizes a real extraction.

## Export to the repository after the switch

The state now lives in the deployment folder, which must never receive exported files. For a commit Austin requests, run the deployment's own export script, which reads that state by default, and write into the development clone with `--out-root`. Check the dry run first, then repeat with `--write`:

```bash
python3 -B ~/work/Projects/ledger-live/_dev/tools/cockpit/export_repo.py \
  --out-root ~/work/Projects/sec-auction deal SLUG --version VERSION_ID
python3 -B ~/work/Projects/ledger-live/_dev/tools/cockpit/export_repo.py \
  --out-root ~/work/Projects/sec-auction deal SLUG --version VERSION_ID --write
```

The same applies to `instruction NAME`. The script refuses `--write` without `--out-root`; always name the development clone there, never the deployment folder. Commit in `sec-auction` only when Austin asks.

## Roll back

Close submissions again by stopping the new cockpit. Let any authorized new jobs and their runner processes finish, then stop the new worker and backup timer. Preserve the new deployment's state for diagnosis. Remove only the three `40-version-1-deploy.conf` files created by this switch-over, run `systemctl --user daemon-reload`, and start the old worker, cockpit and backup timer. The original units point back to the old checkout and untouched state, and the old nightlies resume in `~/backups/ledger-cockpit/`. Verify their effective paths and the old site's operation. The old app reads the plain email header again (the security fix is part of Version 1 only). Any separately installed TMPDIR drop-in should be removed only if it was part of this deployment and is being rolled back. Keep unrelated public-origin drop-ins.

## One week after a clean switch-over

After Austin confirms a week of clean operation, verify the archive branches and `~/backups/vm-checkouts-2026-09-27.tgz` are recoverable, the old state backup is intact, and no service, runner, worktree or agent uses either old folder. Then remove `~/work/Projects/sec-extraction`, `~/work/Projects/sec-extraction-v114` and any archived `dist.old` under those retired folders. Use Git worktree removal for a registered worktree. Keep the deployment worktree, development clone, backups and other projects. The old app's nightlies in `~/backups/ledger-cockpit/` are no longer pruned by anything; keep or delete them as Austin decides. This cleanup is a later authorized action, not part of this build.
