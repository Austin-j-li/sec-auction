# Build spec: Version 1 of the instruction, its tools and the app

27 September 2026. This is the entry point for building Version 1 on the VM. It says where the work happens, what it produces, what it must not touch and where it stops. The content of the instruction and its tools is specified in [DRAFTING_SPEC.md](DRAFTING_SPEC.md); the decisions behind it are in [DECISIONS.md](DECISIONS.md). Any agent or team of agents may do the build; nothing here depends on a particular model. Where a step needs a research judgement, those two files are the authority, not the builder's own view.

Read in this order: this file, DRAFTING_SPEC.md, DECISIONS.md (the decision table and the records, including the evening rulings), then the sources each part names.

## 1. What is being built

The project turns the Background section of an SEC merger filing into an Excel deal ledger for research on takeover auctions (Austin Li and Alex Gorbenko). An extraction model (Claude Opus 5.5 at medium effort) reads the instruction and one filing and writes the ledger; a mechanical checker (`_dev/tools/check_lean.py`) and an analysis tool (`_dev/tools/derive_analysis.py`) consume it. A web app, the cockpit, lets Austin and Alex run extractions on their own subscriptions, review and edit ledgers, and publish instruction versions.

The build has three parts:

- **A. The instruction and its tools:** the Version 1 draft, the checker and analysis changes, and their tests (DRAFTING_SPEC.md).
- **B. The app on Version 1:** the cockpit code, taken from the VM archive and wired to the new tools, with a fresh starting state and a switch-over runbook.
- **C. The workbook check:** a list of places where the draft's outcomes differ from Alex's hand coding, for Austin to rule on.

Austin approves the result before anything goes live.

## 2. The machine and what not to touch

The build runs on the Condenser VM (`ssh condenser-vm`, user `uctpiaj`; home directories live under `~/work`, and `~/Projects` links to `~/work/Projects`).

The live app runs there and must keep running unchanged until the switch-over Austin orders:

- `ledger-cockpit.service` and `ledger-worker.service` (systemd user units in `~/.config/systemd/user/`) run from `~/work/Projects/sec-extraction`, now on branch `vm-live-2026-09-26`. The site is public at lines.dealextract.org through cloudflared. `ledger-backup.timer` backs up the app's state nightly to `~/backups/ledger-cockpit/`.
- The server loads some modules lazily and the worker starts the runner and checker as new processes for every job. So any file change in that folder takes effect on the next request or job, with no restart.

Therefore:

- **In `~/work/Projects/sec-extraction`, change nothing.** No edits, no `git checkout`, `switch`, `stash`, `pull`, `merge`, `reset` or `clean`, and no writes to `_dev/cockpit/state/`. Reading is fine. Open its SQLite database only with `mode=ro` and copy it with SQLite's online backup API; the live database is in WAL mode and changing, so `immutable=1` is only for a finished offline copy.
- **Leave the services, the unit files and the timer alone.** Don't stop, restart or edit them. Don't change `~/backups/`.
- **Leave `~/work/Projects/sec-extraction-v114`** (archived on branch `vm-v114-2026-09-26`), other project folders, and other agent processes running on the VM alone.
- **Watch disk space.** About 1.4 GB was free on 27 September. Keep build artifacts and test state small, and delete scratch copies when done.

The laptop checkout is retired; development continues on the VM from this build on.

## 3. Setting up

- Clone the repository into a new folder and work on a new branch:
  - `git clone git@gitlab-sec:austin.junyu.li/sec-auctions.git ~/work/Projects/sec-auction`
  - `git -C ~/work/Projects/sec-auction switch -c version-1 origin/local-recovery-2026-09-27`
  - `git -C ~/work/Projects/sec-auction push -u origin version-1`

  Run every later git command inside the new clone.

  The `gitlab-sec` host alias and its deploy key are already set up on the VM.
- `version-1` starts from the laptop's work: the Version 0 instruction, the Version 0 tools, the decision log, these specs and the reconciliation reports. It descends from `extraction-v2`'s last commit (`679d4fc`), so `extraction-v2` can later move forward to it without a merge.
- The app code is not on this branch; the Version 0 reset removed it. It comes from `origin/vm-live-2026-09-26` in part B.
- Python packages for the tools are installed under `PYTHONUSERBASE=~/work/.local`, as the services use them. The frontend uses Node and vitest; install its dependencies inside the new clone only.

## 4. Part A: the instruction and its tools

Follow DRAFTING_SPEC.md in full: its inputs and their authority (section 2), boundaries (3), reconciliations (4), writing standard (5), tool changes (6), round map and regression anchors (7), deliverables (8) and checks (9).

The writing standard in its section 5 is written for the extraction model, Claude Opus 5.5, and applies whoever drafts. The sources are listed at the end of that file.

## 5. Part B: the app on Version 1

### B1. Bring the app code in

Copy the app from `origin/vm-live-2026-09-26` into `version-1`:

- `_dev/tools/cockpit/`, without `dist.old/` or caches;
- `_dev/cockpit/catalog.json` and `_dev/cockpit/README.md`;
- the deploy unit copies in `_dev/tools/cockpit/deploy/`, including the backup service and timer;
- the app's tests (`_dev/tools/test_cockpit_*.py` and the acceptance suites);
- any other module the app imports that `version-1` lacks.

The VM archive is the true record of the app. Where the laptop's recovery commit (`ae03c85`) holds a reconstructed version of an app file, take the archive's file.

The tools themselves (`check_lean.py`, `derive_analysis.py`, `run_model.py`, `fetch_filing.py` and the rest) stay as they are on `version-1` with the part A changes. The app adapts to the tools, not the reverse.

### B2. Wire the app to the Version 1 tools

Make the smallest changes that let the app work with the Version 1 checker and ledger. Carry no code path for older instruction versions or ledger formats: no rules selector keyed on the instruction, and no branches for v1.13.2 or v1.14 (AGENTS.md, "Version 0").

The known call sites come from the breakage table in [`vm_check/lane_D_ops.md`](vm_check/lane_D_ops.md). Confirm each against the code, and fix any others the tests reveal.

- **Checking:**
  - The checker is called without a `rules` argument (`data.py`, `workspace.py`), and `rules_for_instruction` and `ledger_schema` are no longer used (`workspace.py`, `data.py`).
  - The worker's check step after a run calls the Version 1 checker without `--rules` (`worker.py`).
- **Editing:**
  - The editor's value lists come from a `choice_lists()` that `check_lean.py` exports for the current format only.
  - The Stock % field's validation uses the current checker's patterns.
- **Review items:** R ids work wherever Q ids do: the Questions view, flag links, and `workspace.py`'s id validation, renaming and reference checks (its `QID` and `QREF` patterns). Otherwise any save of a workbook that contains R1 fails. Test saving, renaming and deleting an R item (DRAFTING_SPEC section 6).
- **Initiation:** lists gain `mixed`.
- **Filing links:** Add Deal and the provenance download get their filing index link through `fetch_filing.index_link`. Either restore that function in `fetch_filing.py` or change `deals.py` and `provenance.py` to match.
- **Labels:** version and checker labels in the interface name the Version 1 checker.
- **Not rebuilt:** the migration tool for old working copies (`migrate_review.py`). Old working copies are archived, not migrated (B3).

List every adapter change in `CHANGE_MAP.md` under a heading of its own.

### B3. A fresh starting state

The app restarts on a fresh state (DECISIONS.md, evening ruling 7). Write a script (for example `_dev/tools/cockpit/fresh_state.py`) that builds a new state directory from an old one. The script reads the old state and never modifies it.

The new state keeps:

- the `accounts` table, so that Austin's and Alex's sign-ins carry over without reconnecting;
- the thirteen deals: the nine catalog deals, and the four added in the app (Medivation, Zep, Pepco Holdings, Imprivata) with their `added_deals` rows and their filings from `state/filings/`;
- no instruction and no `default_instruction` setting. When its instruction table is empty, the app imports the repository's instruction file as the first published version and the default (`instructions.py`, `_seed`). At the switch-over the deploy folder is at the approved commit, whose instruction file is Version 1, so Version 1 becomes the default with no extra step. In testing before approval it imports Version 0, which is fine.

The new state leaves out:

- old instruction versions, run versions and working copies, with their revisions and row marks;
- comments and threads;
- jobs and activity.

These stay in the archived old state. The eight edited working copies hold Austin's review judgments; they are carried into the Version 1 review by hand, not by the app.

The nine catalog deals have no base version until their Version 1 extraction; `extraction/` is empty on `version-1`. Give catalog deals the same no-version state that app-added deals already have before their first run (`workspace.py`, `item` and `pending_payload`, which today read the `added` row that catalog deals lack; take their filing details from the catalog). The first successful run becomes the deal's base and ends the pending state. Update `catalog.json` and the app wherever else they assume a base workbook, and test the whole path for a catalog deal with the test suites' stub runner.

Tokens in the `accounts` table are secrets. The state directory is ignored by git (`_dev/**/state/`) and must stay out of every commit and report.

### B4. Test the app

- Run every test suite the app has: the Python unit tests, the HTTP acceptance tests, vitest, and the browser suites where they can run headless on the VM.
- Then run the app from the new clone on a spare localhost port (not 8778), against a fresh state built from a copy of the live state. Take the copy with SQLite's online backup API from a `mode=ro` connection, plus the `filings/` folder.
- Check by hand:
  - the deal list;
  - a deal with no version;
  - editing and saving a hand-made Version 1 ledger;
  - the checker line on the Review tab;
  - the Questions view with R ids;
  - the instruction pages;
  - the Add Deal lookup.
- Start no extraction job. Test the run path only with the test suites' stubs. Where a check would need a real extraction, stop before submitting the job and report it as untested. A queued job is not a safe stopping point: the worker starts queued jobs by itself within seconds. The same holds for the switch-over smoke test.
- Stop the test server and delete the scratch state when done.

### B5. The switch-over runbook

Write `_dev/alignment_sprint/SWITCHOVER.md` for Austin. Nobody runs it before his order. It covers:

- **A separate deploy folder.** The services should run from a deploy worktree checked out at the approved commit, for example `~/work/Projects/ledger-live`, not from the development clone. Development then never changes the running app.
- **Before:**
  - stop the cockpit server so no new jobs are submitted;
  - let queued and running extractions finish under the old worker, and confirm their runner processes have exited (runners run in their own sessions and outlive a worker stop, `KillMode=process`);
  - then stop the worker and the backup timer, and take a backup;
  - archive the old state as a tarball in `~/backups/`;
  - build the fresh state into the deploy worktree with the B3 script;
  - build the frontend.
- **Services:**
  - point the units at the deploy worktree with drop-ins;
  - add the TMPDIR fix proposed in `_dev/tools/cockpit/deploy/PROPOSED-tmpdir.md` (on the archive branch);
  - reload systemd and start the services and the timer.
- **Smoke test:** the checks of B4, against the live site.
- **In the app:** Austin publishes Version 1 and makes it the default, under his account.
- **Rollback:** remove the drop-ins and restart, which returns the services to the old folder and its untouched state.
- **A week after a clean switch-over:**
  - delete `~/work/Projects/sec-extraction`, `~/work/Projects/sec-extraction-v114` and `dist.old`;
  - they remain on the archive branches and in `~/backups/vm-checkouts-2026-09-27.tgz`.

## 6. Part C: the workbook check

Produce `WORKBOOK_CHECK.md` as DRAFTING_SPEC section 8 item 6 describes. Alex's workbook is `ref/deal_details_Alex_2026.xlsx`, one row per event, with bid type, dates, ranges and drop codes. The check reports; it changes no rule.

## 7. Rules that hold throughout

- **No extraction runs.** No model reads a filing to produce a ledger, in the app or outside it; extractions run only on Austin's command. Engineering help from any model is fine.
- **General rules only.** Every rule in the instruction is general; no rule names or fits one deal (AGENTS.md).
- **No secrets in git.** No tokens, credentials or state directories in any commit. Scan what you stage.
- **Never force-push, rewrite pushed history or push to `extraction-v2`.** Commit and push `version-1` at the end of each working session so that nothing is lost if the VM becomes unreachable.
- **Write reports in plain language.** Austin reads them. State results and failures as they are, with test counts and any step not done.

## 8. What finished looks like

On `version-1`, committed and pushed:

- the draft instruction, `CHANGE_MAP.md`, `ROUND_MAP.md`, the check report and `WORKBOOK_CHECK.md` (DRAFTING_SPEC section 8);
- the tool changes and their tests, all passing;
- the app code and its adapter, its tests passing, the fresh-state script and `SWITCHOVER.md`;
- `_dev/alignment_sprint/BUILD_REPORT.md`:
  - what was built;
  - the test results with counts;
  - what could not be done or checked, and why;
  - every item waiting for Austin: the flagged items in the change map, the round-map cells that could go another way, and the workbook-check disagreements.

Then stop. Publishing Version 1, the switch-over, moving `extraction-v2`, updating STATUS, AGENTS and README (DRAFTING_SPEC section 10) and any extraction all wait for Austin.
