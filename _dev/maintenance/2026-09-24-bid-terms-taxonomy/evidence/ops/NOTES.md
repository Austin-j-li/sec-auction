# OPS: deploy readiness (spec §7.11)

25 September 2026. Package OPS of the v1.14 upgrade. The code is in the OPS sandbox, `/home/uctpiaj/work/tmp/v114-scratch/pkg/ops`. Nothing is deployed or installed. No systemd unit was changed, no service was contacted, and nothing in the live checkout was edited except this file.

## What OPS changed (paths relative to the checkout root)

| File | Change |
|---|---|
| `_dev/tools/cockpit/deploy/ledger-cockpit.service` | New. A byte-identical reference copy of `~/.config/systemd/user/ledger-cockpit.service` (SHA-256 `c302ca0b…`). |
| `_dev/tools/cockpit/deploy/ledger-cockpit.service.d/20-public-origin.conf` | New. A reference copy of the drop-in (`3a8c6f60…`). It holds only the public origin URL. |
| `_dev/tools/cockpit/deploy/ledger-worker.service` | New. A reference copy (`fdca9d70…`). |
| `_dev/tools/cockpit/deploy/PROPOSED-tmpdir.md` | New. The `TMPDIR` proposal for window step 6a: exact lines, install commands, checks, rollback. Not applied. |
| `_dev/tools/cockpit/backup.py` | The manifest records `checker_version` (parsed from the repository root's `_dev/tools/check_lean.py`) and `dist_index_sha256` (of `_dev/tools/cockpit/dist/index.html`) beside `git_head`. Each is `null` when its file is missing. |
| `_dev/tools/cockpit/workspace.py` | Optional B21. An edited working copy's check is cached per deal, keyed by revision, revision time, base SHA-256, the filing's mtime and size, and `check_lean.CHECKER_VERSION`. Only the latest entry per deal is kept. |
| `_dev/tools/cockpit/worker.py` | Optional B20. A job whose params name no instruction fails `instruction_missing` ("The job names no instruction version.") and no longer runs on the repository's instruction. `instruction_version()` and `INSTRUCTION` stay, to label jobs from before phase 4. |
| `_dev/tools/cockpit/frontend/src/api.js` | Optional B12. When a write is refused with 403 `write authorization failed`, the frontend fetches `/api/session` again. If the user is unchanged and the token is new, it stores the new token on the shared session object and retries once. Any other 403, a different user, an unchanged token or a second refusal is raised as before. |
| `_dev/tools/README.md` | Four lines: the worker unit's reference copy and the instruction rule (line 53); the manifest's new fields (77); the check cache (181); the reference copies, the proposal and the token retry (185). None of these are the S6 deploy or release lines (19, 118, 158; 49, 120). |
| Tests | `test_cockpit_backup.py` (+1), `test_cockpit_workspace.py` (+1), `test_cockpit_phase4.py` (+1), `frontend/src/api.test.js` (+2). |

There are no database changes and no new dependencies.

## Tests (sandbox root, `TMPDIR=/home/uctpiaj/work/tmp/v114-scratch/tmp/ops`)

| Command | Result |
|---|---|
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s _dev/tools -p 'test_*.py'` | 202 pass (baseline 199; +3) |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider _dev/tools/cockpit/acceptance/test_http.py` | 14 pass |
| `(cd _dev/tools/cockpit/frontend && npx vitest run)` | 55 pass (baseline 53; +2) |
| `npx vite build --outDir $TMPDIR/dist-check --emptyOutDir` | builds; `dist/` untouched |

Each new Python test was also run against the unchanged file and failed there.

## What the §12 deploy checklist needs from OPS

**Before the window**
- The deploy patch carries four new files under `_dev/tools/cockpit/deploy/`, one of them in a new subfolder, `ledger-cockpit.service.d/`. `git apply` creates both; check the patch lists them.
- Confirm that the installed units have not drifted from the reference copies:
  `diff ~/.config/systemd/user/ledger-cockpit.service <worktree>/_dev/tools/cockpit/deploy/ledger-cockpit.service`, and the same for `ledger-cockpit.service.d/20-public-origin.conf` and `ledger-worker.service`. Each must print nothing. If one does, copy the installed file again before making the patch.

**In the window**
- Step 3: the backup is made by the old `backup.py`, so its manifest has no `checker_version` or `dist_index_sha256`. To keep the same record for the pre-deploy code, add to step 4:
  `sha256sum _dev/tools/check_lean.py _dev/tools/cockpit/dist/index.html > ~/work/archive/v114-deploy/pre-v114-code.txt`.
  Keep this file apart from `pre-v114-hashes.txt`: both of these files change in the deploy, so step 10's `sha256sum -c` would fail on them.
- Step 6a, only with Austin's approval: follow `_dev/tools/cockpit/deploy/PROPOSED-tmpdir.md`. It adds two drop-ins (`30-tmpdir.conf`), creates `~/work/tmp` if needed and runs `systemctl --user daemon-reload`. The restarts in steps 7 and 9 apply them. The file also gives the check after step 9 and the rollback.
- Step 10, additions:
  - Call `/api/deals` a second time. The first call is still cold (about 20 s): the check cache is in memory and starts empty at each restart. The second call should skip the recheck of every edited deal.
  - Optional: run `python3 _dev/tools/cockpit/backup.py create` after step 9. Check that the new manifest has `"checker_version": "1.7"` and a `dist_index_sha256` equal to `sha256sum _dev/tools/cockpit/dist/index.html`. The backup is written to `~/backups/ledger-cockpit/` on the root disk; all five backups there now total 17 MB.
- Step 11 is still needed for this deploy. Tabs opened before it run the old frontend, which does not retry, and the new API needs the new frontend anyway. After this deploy, a later restart that changes only Python code no longer breaks writes from open tabs: the first refused write fetches the new token and retries.
- If 6a is installed: at the gate 3a commit, copy the two installed `30-tmpdir.conf` drop-ins into `_dev/tools/cockpit/deploy/` (under `ledger-cockpit.service.d/` and a new `ledger-worker.service.d/`), so the reference copies match what is installed.

**Rollback**
- Code: restoring `_dev/tools` from the step 5 tarball removes every OPS change, including the reference copies. OPS changes no data, so no data rollback is needed for it.
- The manifest works across versions both ways. `verify` and `restore` read only `database`, `files` and `state`, so the old `backup.py` can restore a backup made by the new one, and the new one can restore old backups.
- `TMPDIR`: see "Rollback" in `PROPOSED-tmpdir.md`. Keep `ledger-cockpit.service.d/`, which holds `20-public-origin.conf`.

## Observations

- Root disk at 20:45 UTC on 25 September: `/` was 82% full, with 1.7 GB free (8.8 GB total); `/home/uctpiaj/work` was 14% full, with 324 GB free. The audit measured `/` at 97% earlier the same day.
- The nightly backups also land on the root disk (`~/backups/ledger-cockpit/`, 17 MB for five backups). This is not a `TMPDIR` matter, and the spec makes no change to it.
- `ledger-backup.service` and `ledger-backup.timer` in `deploy/` match the installed files byte for byte.
- No unit file carries a secret: `COCKPIT_PUBLIC_ORIGIN` is the public URL. Nothing was replaced with a placeholder.
- The `'v1.13.2'` fallback label in `frontend/src/runs.js` is kept: it labels only jobs from before phase 4 (audit B20, "keep them for old rows").

## Notes for merging

The OPS edits are small, separate hunks in files that other packages also edit:
- `workspace.py`: `Workspace.__init__` gains one line (`self._checks`), and the `else:` branch of `_payload` that rechecks a working copy is changed (about lines 322–336). S2 edits `_payload`'s choices below it.
- `worker.py`: only the `else:` branch after the frozen-instruction check in `start()` (about line 259). S2's checker metadata is in `finish()`.
- `api.js`: `post` becomes `send` plus an async `post`. No exported name changes.
- `test_cockpit_workspace.py`: one test after `test_read_only_get_and_immutable_export`, and `import check_lean`.
- `test_cockpit_phase4.py`: one test after `test_an_altered_stored_instruction_fails_the_run`.
