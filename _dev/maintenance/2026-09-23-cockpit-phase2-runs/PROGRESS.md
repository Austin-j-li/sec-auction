# Phase 2 (accounts and runs): build record, 23 September 2026

Contract: [CONTRACT.md](CONTRACT.md). Claude-only build at Austin's direction: Opus 5.5 wrote the contract, the backend, the worker and the tests, then integrated and deployed. An Opus 5.5 subagent wrote the frontend, and Fable 5.1 gave one second-opinion review of the backend.

## What changed

- **Runner** (`_dev/tools/sandbox/run_model.py`):
  - SIGTERM cancels a run. The provider's process group gets SIGTERM, then SIGKILL after 20 s, and the outcome is `cancelled`.
  - The stream's `rate_limit_event`s are recorded as `plan_usage`.
  - A rejected limit that leaves no valid workbook fails as `usage_limit`, with `usage_limit_resets_at`.
- **Accounts and jobs** (`_dev/tools/cockpit/runs.py`):
  - Tables: `jobs`, `accounts`, `plan_usage` and `versions`.
  - Claude connection: connect, code, cancel, token paste and disconnect. Tokens go in `~/.config/sec-extraction/users/<user>/claude-oauth-token`, with the directory at 0700 and the file at 0600. They are never returned or logged.
  - Extraction start and cancel, with caps of 4 runs in total and 2 per user.
  - Hiding and unhiding imported versions.
- **Worker** (`_dev/tools/cockpit/worker.py`, `ledger-worker.service`):
  - Sign-in: it drives `claude setup-token` in a PTY and passes the link and code through the jobs table.
  - Runs: it prepares and launches `run_model.py` with the starting user's token file only, then runs `check_lean.py` outside the sandbox.
  - Import: it saves the workbook and receipts as an immutable version under `_dev/cockpit/state/versions/<deal>/<id>/`.
  - Records: it logs `extraction` or `extraction_failed` activity, the extraction activity with its `version_id`, and each job's `cancelled_by`. A failed run's receipts are kept in `state/jobs/<id>/`.
  - Restarts: after a restart, orphaned runs are finished or failed.
- **Workspace and server:**
  - Imported versions are merged into each deal.
  - Rebase and restore edits: a `rebase` activity row carries its revision.
  - `GET /api/deal/<slug>/compare`: two versions, rows matched by key, with `same_instruction`.
  - `is_base` on each version.
  - New routes:
    - `GET /api/account` and `POST /api/account/claude`;
    - `GET` and `POST /api/deal/<slug>/jobs`;
    - `POST /api/deal/<slug>/versions`;
    - the `/settings` page.
  - `/api/deals` gains `active_jobs`.
- **Frontend:**
  - Settings page: Claude account, sign-in link and code, token paste fallback, and plan usage.
  - Extract dialog: Opus 5.5 with a chosen effort and time limit.
  - Runs tab: live status, cancel, open version, and show hidden.
  - Version dropdown: originals are grouped and the base is marked, with "Use as working-copy base…", Hide and Unhide.
  - Changes tab: From/To compare.
  - The overview shows a running line, and What's new and Activity show runs.
- **Acceptance:**
  - `test_runs.mjs`, with `serve_fixture.py --runs`. The real worker loop drives the fake runner and fake `claude`, so no model is called.
  - `test_cockpit_runs.py` has 10 tests.
  - The runner tests cover cancellation and usage limits.

Deviation (also in the contract): tokens are protected by file permissions, not encrypted at rest, because the key would sit on the same VM.

## Verification

- **Python:** `python3 -m pytest -q _dev/tools` gives 160 passed and 57 subtests (162 after the review fixes).
- **Frontend:** 28 vitest tests pass, and `npm run build` succeeds.
- **Browser** (synthetic fixture, private Chrome):
  - `test_browser.mjs`, `test_resize.mjs` and `test_responsive.mjs` pass.
  - `test_trace.mjs`: 14 checks pass.
  - `test_runs.mjs`: 11 checks pass. Austin connects through the sign-in link and code, and his token never appears in any response. Alex stays unconnected and is sent to Settings. Austin's run completes and is imported. Open version switches the dropdown, and Hide and Unhide work. Rebasing makes the new run the working base, with the changed bidder. The compare view shows the difference between the original and the run. Alex's feed shows the extraction linked to its version, and the rebase with its revision. No browser errors.
- **Deployment:**
  - `ledger-cockpit.service` was restarted, and `ledger-worker.service` was enabled and started.
  - On loopback:
    - `/settings` serves the new build;
    - `/api/account` answers;
    - `/api/deals` reports `active_jobs: 0` for all nine deals;
    - an unauthenticated write to `/api/account/claude` is refused with 403.
  - The public route still redirects to Cloudflare Access (302).
  - No live working state or token existed before deployment, and none was created.

## Fable review

Fable 5.1 found no problems with the token handling, identity checks, catalog immutability or the runner. It found four material defects in the worker, all fixed and covered by two new tests (`test_cockpit_runs.py` now has 12):

1. An error while finishing one job stopped the whole worker, which then crash-looped on restart. Each job step now runs guarded: an unexpected error fails that job as `worker_error` and keeps its receipts. Recovery is guarded too.
2. A crash between saving a version and marking the job complete made the retry collide with the existing version. Now the version row and the job's completion are written in one transaction, and a retry replaces the row.
3. After a reboot, a reused process ID could make a dead run look alive forever. A run now counts as alive only if the process is `run_model.py` for that job's run directory.
4. Two worker processes could start the same run. A job is now claimed atomically before preparation, and the worker holds a lock file, so a second instance exits.

Minor points also applied:
- Disconnect is refused while the user's runs are active.
- Recovery clears any pasted sign-in code.
- The unit file `~/.config/systemd/user/ledger-worker.service` sits outside the repository by design.

## Live sign-in failure (fixed)

Austin's first live connect attempt failed with "did not return a token". A probe of the real `claude setup-token` with a deliberately invalid code showed:
- Claude answers a rejected code with `OAuth error: Request failed with status code 400` and `Press Enter to retry`.
- The code-plus-Enter write is received correctly.
- The stored link was intact.

So the likely cause was a rejected code: it had expired or was incompletely copied. The worker now stops as soon as Claude refuses a code and shows Claude's message. It logs a redacted tail of the output, with the code and any token replaced. It also strips the `ESC ( B` terminal sequence.

After the fixes: `pytest` gives 162 passed; `test_runs.mjs` passes 11 checks; both services were restarted.

## Live sign-in failure, second cause (fixed 15:20 UTC)

Austin's retry at 15:12 also failed. This time the log showed Claude printing only the masked code (92 asterisks) and nothing after it, so the code was never submitted. Claude's input treats a multi-character write as a paste, and an Enter inside that same write is swallowed. The earlier probe's conclusion that "the code-plus-Enter write is received correctly" was wrong for a real-length code. A probe with a fake 92-character code confirmed it: code and Enter written together gave no response; the code followed by a separate Enter got Claude's `400` reply. The worker now writes the code, waits 0.5 s, then sends Enter on its own. The fake `claude` in `test_cockpit_runs.py` now reads raw chunks and submits only on a lone Enter; the sign-in test fails against the old worker and passes with the fix. `pytest` gives 162 passed; both services were restarted.

## Run badge in the deal header (15:36 UTC)

Austin reopened PetSmart during the first real run and could not see it: a deal opens on Ledger, and the only sign was the "Runs 1" count, which reads like the other tab counts. The header now shows a pulsing "Extracting · 7 min 55 s" badge (or "Extraction queued" / "N extractions running") on every tab while the deal has an active run; clicking it opens the Runs tab. `activeRunLabel` in `runs.js` has a vitest case (29 pass). All five browser suites passed against the staged build, which was swapped in without a restart; the badge was checked on the live PetSmart page during the real run.

## Not yet done

> **Status, 26 September 2026:** Austin has since made real runs on his own plan (the latest, the five v1.14.1 retest runs, `../../reviews/2026-09-26-v1141-retest/README.md`). Alex's own run was still outstanding when last recorded; the [development handoff](../../HANDOFF.md) tracks what remains.

- **One real run by each user on their own plan** (spec acceptance). Each user connects in Settings, then extracts one deal at Opus 5.5 medium. It needs Austin's go-ahead: building the app does not authorise a real model run.
- **Is the long-lived token refreshable or revocable?** Claude reports the token as valid for one year. The app shows the expiry date, and Reconnect replaces the token.
