# Deploy from a Claude cloud session

Austin requested this route on 4 October 2026. Deployment stays in the cloud task that prepares the release.
Use the existing protected ARC connection to Condenser. A separate “Work locally” task is optional.

## Access and authority

- Project: `sec-auction`, repository `Austin-j-li/sec-auction`, base branch `extraction-v2`.
- Website: https://lines.dealextract.org, with Cloudflare Access.
- Cloud command: `/usr/local/bin/arc`. Its protected credential targets `arc.dealextract.org`.
- VM account: `uctpiaj` on `econ-phd-04`.
- Source checkout: `/home/uctpiaj/work/Projects/sec-auction`.
- Live checkout: `/home/uctpiaj/work/Projects/ledger-live`.
- Services: `ledger-cockpit.service`, `ledger-worker.service`, `ledger-backup.timer`.
- State: `/home/uctpiaj/work/Projects/ledger-live/_dev/cockpit/state`.
- Database: `workspace.sqlite3` inside that state folder; use Python's `sqlite3` module with `mode=ro` for inspection.
- Backups: `/home/uctpiaj/backups/ledger-live`.

A request to deploy or publish authorizes the release steps in that task. Do not request a second approval for the same release.
A request to prepare code alone does not authorize a release. Austin still merges pull requests.
Use a full commit ID for the release. Do not infer the target from whichever branch the VM currently uses.
The extraction instruction, paid extraction runs, and research decisions retain their separate rules.

No Cloudflare API token is needed for an ordinary app release. The existing tunnel serves the VM application.
Do not change DNS, Access policy, tunnel credentials, provider accounts, or public exposure as part of an ordinary release.
Never put the ARC credential in a prompt, repository, or plain variable.

## First use in a cloud task

Read this guide and the project rules. Use the installed client:

```bash
arc health
arc exec condenser 'hostname; id -un; git -C /home/uctpiaj/work/Projects/ledger-live rev-parse HEAD; git -C /home/uctpiaj/work/Projects/ledger-live status --porcelain; systemctl --user is-active ledger-cockpit.service ledger-worker.service ledger-backup.timer'
```

An existing cloud session with `arc` can use this route immediately.
If the client or protected credential is absent, use a fresh session in the `sec-auction` environment.
Do not ask Austin to switch to “Work locally” merely because old repository text says cloud sessions cannot reach the VM.
Report the exact access error if the protected connection fails. Never print a credential to diagnose it.

## Prepare the release

1. Finish the source change on the task branch.
2. Use the real app or CLI with relevant inputs to verify the change.
3. For frontend changes, build the frontend and commit the resulting `dist/` files.
4. Do not write or run tests or test suites.
5. Push the branch and open a pull request into `extraction-v2`.
6. Use the commit Austin selected, or the merged commit for the requested release.
7. Compare the target with the live commit before the outage.
8. Review dependency, instruction, and database changes in that difference.
9. For a database change, prepare a migration and recovery plan before the outage.
10. Keep cloud edits out of the live folder until the release is ready.

Use ARC for VM commands. For a multiline script, send a local file through standard input:

```bash
arc exec condenser 'bash -se' --stdin-file release.sh --timeout 3600 --detach
arc status JOB_ID
```

Save the returned job ID immediately. Reconnect with `arc status` after a browser or client interruption.
An ARC job survives a disconnected client, but not necessarily a bridge restart. Inspect the live state before any retry.
Do not submit a second release when the first command's outcome is unknown.

## Apply the release

These steps update the existing Version 1 app. Do not repeat the historical fresh-state switch-over or delete earlier data.

1. Run the release in one remote shell with `set -euo pipefail`.
2. Hold a VM lock for the whole release: `exec 9>/home/uctpiaj/work/sec-auction-deploy.lock; flock -n 9`.
3. Record the current commit, service states, and target commit outside the live checkout.
4. Fetch the target from GitHub without changing the development checkout's branch or files.
5. Verify the target object and the full commit ID on the VM.
6. Check that the live checkout has no tracked or untracked source changes.
7. Check available disk space for the backup and release.
8. Prepare dependencies before the outage, with the repository's version pins.
9. Inspect the job queue and runner processes before you stop services.
10. If a job is active, postpone the release until it completes.
11. Stop `ledger-cockpit.service` to prevent new submissions.
12. Recheck the queue and runner processes after the server stops.
13. If a job appeared, restore the server and postpone the release.
14. Stop `ledger-worker.service` and `ledger-backup.timer` only after the queue is empty.
15. Wait for an active `ledger-backup.service` to finish.
16. Create a backup with the current release's `backup.py create` command.
17. Give that release a unique destination below `/home/uctpiaj/backups/ledger-live/releases/`.
18. Record the backup path and inspect its manifest and database integrity result.
19. Move the live checkout to the full target ID with `git checkout --detach`.
20. Preserve the ignored state directory and external provider credentials.
21. Start the cockpit and inspect its responses before you start the worker.
22. Start the worker and restore the backup timer to its earlier state.
23. Verify the website through the browser and the release commit through the VM.
24. Record the target, previous commit, backup, commands, and observed results.

For the queue, open the SQLite database in read-only mode. Query jobs outside the four final states:
`completed`, `failed`, `timed_out`, and `cancelled`.
Print only job IDs, states, and process IDs. A missing database or failed query blocks the release.
Check runner processes too; the worker can leave a runner alive after it stops.

Use `backup.py create --repo-root /home/uctpiaj/work/Projects/ledger-live --dest RELEASE_BACKUP_PATH` for the backup.
The command prints the completed backup directory. It also checks SQLite integrity during the copy.
A unique destination keeps older backups outside this command's retention pass.

Never use `git clean`, forced checkout, state reset, or credential replacement for a routine release.
Do not overwrite unit files or their Access settings. An ordinary code release needs no service reconfiguration.

## Failure and recovery

Keep a release record on the VM so a fresh cloud task can recover it.
Restore the earlier service state if preparation fails before the code changes.
If startup fails after the code changes, keep the worker stopped while you inspect the error.
Return to the recorded previous commit only when it can read the current database.
For a migration, follow the approved recovery plan; never restore a database over new user work without authorization.
Verify service state and browser behavior after recovery. Report the failed release and the actual live commit.

## Verify the result

- Read the deployed commit from `ledger-live`.
- Inspect the cockpit, worker, and backup timer states.
- Read `http://127.0.0.1:8778/api/session` through ARC.
- An unsigned request must report `user: unknown` and `can_edit: false`.
- An unsigned request to `http://127.0.0.1:8778/api/deals` must return 401.
- Open https://lines.dealextract.org through the browser.
- Check the requested behavior with real app inputs in the authenticated session.
- A Cloudflare login page proves only that the access gate responds.
- A successful HTTP response alone does not prove that the requested feature works.
- Do not launch an extraction merely to verify a deployment.

## Setup verification, 4 October 2026

The selected desktop project has the `sec-auction` environment and `Austin-j-li/sec-auction` repository.
Its protected credential list includes `arc.dealextract.org`.
The VM services were active at inspection, with live commit `9f0750e`.
No release was requested as part of this connection setup.

A fresh Claude cloud session verified the route at 15:38–15:41 Europe/London on 4 October 2026.
Environment: `env_01SohAnkv8aZfd2kKUSq2mjV` (`sec-auction`).
Session: `session_01GBXD3zfth8eu3vFfo6xdc4`.
It reached Condenser through `arc`, read this guide, and confirmed the live checkout and Git metadata were writable by `uctpiaj`.
The checkout was clean. All three services were active. The unfinished-job count was zero.
The unsigned session response reported `user: unknown` and `can_edit: false`.
The project coordinator saved the route to memory and sent it to existing threads.
This verifies cloud access and the release workflow instructions. No deployment or recovery operation ran during setup.
