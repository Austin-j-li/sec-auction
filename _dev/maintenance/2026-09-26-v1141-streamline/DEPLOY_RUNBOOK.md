# v1.14.1 deploy runbook

26 September 2026. Prepared under `PIPELINE_UPGRADE_SPEC.md` WP1 and WP7. **Both deploys are GATEs. Nothing here has been run; the live services still run the 26 September 12:02 UTC build (Astra-high default, checker 1.6).**

> **Status, 26 September, about 20:45 UTC.** Austin ordered B, and it was done at 19:41 UTC: patch applied, tests green (336 unit, 20 HTTP, 77 vitest), frontend rebuilt, both services restarted. Receipt: [`deployment-v1141.json`](deployment-v1141.json). Live now: checker 1.8, derive_analysis 0.3 and the Opus 5.5 medium default. A was not run separately. Step 11 is open: `dist.old` is kept until Austin accepts; the backup and tarball named in the receipt stay for at least 14 days. The unit-file changes are not installed.

`$LIVE` is `/home/uctpiaj/work/Projects/sec-extraction`. Run everything from `$LIVE`.

There are two ways to ship:

- **A. WP1 alone** (engine back to Opus 5.5 medium). The code is already in `$LIVE`'s working tree; only the restart and the frontend swap are left.
- **B. WP7, the full v1.14.1 code** (checker 1.8, rules selector, analysis, migration, runner and cockpit changes, WP1 included). Deploy once, after WP1–WP6; do not deploy the v1.14 code without the v1.14.1 changes (spec §5).

If B is ordered, A is not needed separately.

## Common checks (both)

1. **Nothing is running.** Read-only:

   ```bash
   python3 -c "import sqlite3; c=sqlite3.connect('file:$HOME/work/Projects/sec-extraction/_dev/cockpit/state/workspace.sqlite3?mode=ro', uri=True); print(c.execute(\"SELECT kind, state, COUNT(*) FROM jobs WHERE state IN ('queued','preparing','running','checking','importing','waiting_for_code','completing','waiting_for_approval') GROUP BY kind, state\").fetchall())"
   ```

   It must print `[]`, and `pgrep -af run_model.py` must print nothing. Austin confirms open cockpit tabs are saved. Nobody contacts Alex.

2. **Backup:** `python3 _dev/tools/cockpit/backup.py create`; note the path.

## A. WP1 alone

The WP1 frontend is built into `_dev/maintenance/2026-09-26-v1141-streamline/wp1-main-dist/` (from `$LIVE`'s source, 26 September), not into the live `dist/`, because the server reads `dist/` from disk and a build there would change the live page before the restart.

1. Common checks.
2. Focused tests (in a copy, as on 26 September, or in `$LIVE`): `test_cockpit_runs`, `test_cockpit_deals`, `test_cockpit_phase4`, `test_run_model`, `runs.test.js`. They passed on 26 September (201 unit, 14 HTTP, 53 vitest on a copy of `$LIVE`).
3. Restart: `systemctl --user restart ledger-cockpit ledger-worker`.
4. Swap in the frontend, keeping the old assets for open tabs:

   ```bash
   cp -n _dev/maintenance/2026-09-26-v1141-streamline/wp1-main-dist/assets/* _dev/tools/cockpit/dist/assets/
   cp _dev/maintenance/2026-09-26-v1141-streamline/wp1-main-dist/index.html _dev/tools/cockpit/dist/index.html
   ```

5. Confirm the extraction dialog shows "Opus 5.5 · medium" without starting a run.
6. Write a receipt (`deployment-wp1.json` in this folder: time, active jobs before restart, service PIDs and start times, `dist/index.html` SHA-256), as the Astra deploy did.

## B. WP7, the full code

The patch is `../2026-09-24-bid-terms-taxonomy/release/deploy-tools-v1141.patch` (SHA-256 `7256570979f1ce8c57e9ee04e531700dabd5758fd203278493357e333f9e15ba`, 62 files, `_dev/tools/` only, no `dist/`). It was generated on 26 September from the v114 tree against `$LIVE`, and checked three ways:

- `git apply --check` passes in `$LIVE`.
- Applied to a copy of `$LIVE`, it makes `_dev/tools/` identical to the v114 tree (except `node_modules`, `__pycache__`, `dist`, caches).
- On that copy: 336 unit tests pass (1 skipped), 20 HTTP, 77 vitest.

Before applying it, confirm nothing in `$LIVE/_dev/tools/` changed since (the patch was made against the tree as it stood at 19:25 UTC). If anything did, regenerate the patch.

1. Common checks.
2. **Rollback copy:** `tar czf ~/work/archive/v1141-deploy/pre-v1141-tools.tgz --exclude=node_modules --exclude=dist _dev/tools`.
3. **Apply:** `git apply _dev/maintenance/2026-09-24-bid-terms-taxonomy/release/deploy-tools-v1141.patch`.
4. **Tests:** the three suites of spec §6 from `$LIVE`.
5. **Build to a side folder**, so the live `dist/` is untouched until the swap: `cd _dev/tools/cockpit/frontend && npx vite build --outDir ../dist.new --emptyOutDir`.
6. **Restart the server:** `systemctl --user restart ledger-cockpit.service`; the journal must show `ledger cockpit -> http://127.0.0.1:8778` and no traceback.
7. **Swap `dist/`, keeping the old assets:** `cp -n _dev/tools/cockpit/dist/assets/* _dev/tools/cockpit/dist.new/assets/ && mv _dev/tools/cockpit/dist _dev/tools/cockpit/dist.old && mv _dev/tools/cockpit/dist.new _dev/tools/cockpit/dist`.
8. **Restart the worker:** `systemctl --user restart ledger-worker.service`; the journal must show "cockpit worker started".
9. **Verify:** the extraction dialog shows "Opus 5.5 · medium" (start nothing), and one read-only workbook view shows "Live check: checker 1.8" with the rules named.
10. **Receipt:** `deployment-v1141.json` in this folder. Then apply the deploy-time doc lines in `../2026-09-24-bid-terms-taxonomy/release/PROPOSED_DOC_LINES.md` ("checker 1.8, deployed on <date>").
11. After acceptance, remove `dist.old`. Keep the backup and the tarball for at least 14 days.

The unit files in the patch (`cockpit/deploy/`) are reference copies. Installing changed units (`TMPDIR`, V114_SPEC §7.11) is a separate approval (V114_SPEC §12 step 6a).

**Rollback:** `mv dist dist.bad && mv dist.old dist`; restore `_dev/tools` from the tarball; restart `ledger-cockpit`, then `ledger-worker`. Versions imported under checker 1.8 keep their 1.8 receipts.

After B, the gate 12 patch (`release-gate12.patch`) applies (checked on the patched copy); it does not apply to `$LIVE` before B.
