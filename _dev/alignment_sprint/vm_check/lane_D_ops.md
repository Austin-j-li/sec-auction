# Lane D: getting the VM and the laptop back onto one line

27 September 2026. Read-only plan. Sources: VM tree snapshot and `git status` (99 entries), the `sec-extraction-v114` worktree status (78 entries), recovery tree `ae03c85`, laptop `HEAD` 70be7f0, and the cockpit database copy in the VM snapshot. The checker comparisons below were run locally on the 34 cockpit export workbooks (no model runs).

## What the evidence shows (short)

1. **v0's ledger header is the same as v1.14.1's** (the 29 columns match exactly). So the v0 checker does **not** reject v1.14 or v1.14.1 ledgers. It checks them under v0 rules. For v1.14.1 run workbooks that is correct: on all five 26 Sep runs, checker 1.8 and the v0 checker gave the same error and warning counts. For the two 24 Sep v1.14-draft runs it silently gives the wrong result (Mac-Gray: 1 error under v1.14 rules, 12 under v0). v1.13.2 ledgers (22 columns) get a `schema.columns` error and then 26–110 follow-on errors, not a clean refusal.
2. **All 13 working copies and all 9 catalog bases are v1.13.2.** The cockpit has 12 run versions: 5 under v1.14.1, 2 under the v1.14 draft (`f9595d74`), and 5 under v1.13.2 (the four added deals and PetSmart).
3. **The VM's current tools can already check v0 runs correctly.** Checker 1.8 treats an instruction hash it doesn't know as v1.14.1, and v1.14.1 rules are v0 rules. Publishing v0 in the app is enough for v0 extractions, with no code deploy. Only the labels would be off ("checker 1.8, v1.14.1 rules").
4. **The laptop branch deletes what the app runs on:** the cockpit source, `_dev/cockpit/catalog.json`, `extraction/*.xlsx` (the nine catalog bases), `_dev/reviews/2026-09-22-opus55-reextraction` (the bases' receipts) and `deploy/ledger-backup.{service,timer}`. Checking the laptop branch out in the live folder would delete the running app and every working copy's base.
5. **`ae03c85` is not the VM state.** It was partly rebuilt from transcripts. 80 files differ from the VM tree. `check_lean.py` is identical. `compare_alex.py` (163 changed lines), `cockpit/data.py` (72), `run_model.py`, `server.py`, `worker.py` and `runs.py` all differ, and `provenance.py`, `bulk.js`, `choices.js`, `downloads.js` and the service units exist only on the VM. Treat the VM tree as the true record and ae03c85's cockpit files as superseded.
6. **The four added deals' filings** (Medivation, Zep, Pepco Holdings, Imprivata) exist only in the VM's `_dev/cockpit/state/filings/`. The laptop's `raw_filing/MANIFEST.csv` doesn't list them.
7. **The VM repository's own instruction file is still v1.13.2** (`513c8e3e`). v1.14.1 lives only in the app's instruction store.

## Order of operations

Each step gives: what to do, where, who authorizes it, and the risk.

1. **Renew the SSH certificate.**
   Where: laptop to VM. Who: Austin (only he can). Risk: none.

2. **Take a fresh backup before any git command.** Run `backup.py` (or tar `_dev/cockpit/state/` and `~/backups/ledger-cockpit/`) and copy the archive to the laptop.
   Where: VM. Who: Austin says go. Risk: low. It reads state and doesn't stop the services.

3. **Gate 0: commit the live checkout's dirty tree on a new branch, without touching any files.**
   Where: VM, `~/work/Projects/sec-extraction`. Who: Austin (gate 0).
   Steps:
   - `git switch -c vm-live-2026-09-26`
   - `git add` with explicit paths
   - `git commit`
   - `git push -u origin vm-live-2026-09-26`

   Leave out `_dev/tools/cockpit/dist.old/` and `lesson/` (Austin called `lesson/` stale). Decide on the root `HANDOFF.md`; committing it is harmless.
   Before committing:
   - Run `git status --ignored` and confirm `.claude/`, `_dev/cockpit/state/` and `_dev/runs/` are ignored. `.claude/` is absent from the status output, but check it; don't assume.
   - Grep the staged files for tokens.

   Risk: low. These commands only write inside `.git`. **Never use `stash`, `checkout <branch>`, `pull`, `merge`, `reset` or `clean` in this folder.** `stash` looks harmless, but it removes the deployed code from the working tree while the services run.

4. **Do the same in the `sec-extraction-v114` worktree.** Commit its 78 entries on branch `vm-v114-2026-09-26` and push.
   Where: VM. Who: Austin. Risk: low. That worktree serves nothing.

5. **Record how the recovery commit compares to the VM.** Fetch the branch, run `git diff --stat ae03c85 origin/vm-live-2026-09-26`, and note the result in `_dev/STATUS.md`. Don't merge `vm-live` into `local-recovery`: that gives about 100 modify/delete conflicts on cockpit files the v0 branch deliberately removed. `vm-live` becomes the cockpit's branch. `extraction-v2` stays at 679d4fc until Austin picks one canonical line. No force-push is needed anywhere.
   Where: laptop. Who: agent, as a normal session commit. Risk: none.

6. **Withdraw the obsolete handoff gates.**
   - `export_repo.py instruction v1.14.1 --write` is now harmful. It would overwrite the v0 file and, for deals, write to `extraction/`.
   - Gate 12 (move the nine `extraction/` workbooks) must not run on the VM while the catalog points at them.
   - "Rebase working copies onto v1.14.1 runs" is replaced by the data decision below.
   - The questionnaire stays unsent; a new one needs Austin's authorization.

   Record these in STATUS. Where: laptop docs. Who: Austin approves. Risk: none.

7. **Publish v0 in the app, only if Austin wants v0 re-extractions before Version 1.** Create a draft from v1.14.1 in the Instructions page and paste the laptop's v0 text exactly, so the SHA-256 is `cbb1f35c…96ce`. Then publish it and make it the default. No code deploy is needed (see finding 3).
   Where: cockpit UI. Who: Austin. Risk: low. Labels read "v1.14.1 rules".

8. **Draft Version 1 on the laptop, per DRAFTING_SPEC.** Do the §6 tool changes on a branch off `local-recovery`, built on the laptop's v0 tools. The drafter lists the cockpit adapter items (see "Drafting work" below) in `CHANGE_MAP.md` as follow-ups on the VM side; it doesn't implement them.
   Where: laptop. Who: Austin gives the go-ahead. Risk: none to the VM.

9. **Build the Version 1 deploy in a separate VM worktree.** Run `git worktree add ~/work/Projects/sec-extraction-v1 vm-live-2026-09-26`, copy in the laptop's Version 1 `_dev/tools/*.py` (including `fetch_filing.py`), and write the cockpit adapter. Then run the cockpit tests, the HTTP and vitest suites, and `pytest`, point the adapter at a copy of `state/`, then commit and push.
   Where: VM. Who: Austin authorizes the build. Risk: none to the live services while the work stays in the other folder.

10. **Deploy deliberately.** Stop both `ledger-cockpit` and `ledger-worker`, because they share modules. Take a backup. Then either:
    - point `WorkingDirectory` at the new worktree with a drop-in and run `daemon-reload`, or
    - switch the live folder to the deploy branch.

    In the same restart, add the TMPDIR drop-in, rebuild `dist/`, and delete `dist.old/`. Start both services, then smoke-test one deal page, one edit, Add Deal and one check.
    Where: VM. Who: Austin orders it. Risk: medium, but rollback is easy: point back at the old folder.

11. **Apply the chosen cockpit-data option** (below), publish Version 1 as the default, and hide or retire the old versions.
    Where: cockpit. Who: Austin. Risk: depends on the option.

12. **Close the session.** Commit and push on both machines, and update STATUS's "Operational" section.
    Who: agent. Risk: none.

**Why no file in the live folder may change except at step 10.** The server imports `cockpit.workspace`, `runs`, `deals` and `instructions` lazily inside methods (`data.py:648–656`). The worker also starts `run_model.py` and `check_lean.py` as new processes for every job. So any file edit in the live folder takes effect on the next request or job, with no restart. A half-copied tool set would mix versions inside the running app.

## Breakage table: laptop v0 tools dropped into the VM's live folder

| Call site on VM | Uses | Laptop v0 | Effect |
|---|---|---|---|
| `cockpit/data.py:770` `Cockpit.check` | `LeanChecker(path, filing, rules=…)` | no `rules` argument | TypeError on **every deal page** (Review, Records, Overview check) |
| `cockpit/workspace.py:349` saved-revision check | `LeanChecker(..., rules=)` | missing | Same as above, for every working copy with revisions |
| `cockpit/workspace.py:626` `rules_for` | `rules_for_instruction` | removed | AttributeError on page load and on every edit (`_apply`) |
| `cockpit/workspace.py:379` | `choice_lists(schema)` | removed | Editor value lists fail (STATUS listed this) |
| `cockpit/workspace.py:372, 592` | `ledger_schema(path, rules)` | removed | Version list and "base columns" fail |
| `cockpit/workspace.py:694` `_coerce` | `SCHEMA_V114`, `STOCK_RANGE_RE` | `SCHEMA_V114` removed | Editing Stock % fails |
| `cockpit/data.py:927` `report_schema` | `ledger_schema` | removed | Schema label for fatal checks fails |
| `cockpit/worker.py:316–318` finish | `rules_for_instruction`, then `--rules` | both removed | **Every run fails at the check step after the paid extraction**, whatever its instruction (STATUS listed only `--rules`) |
| `cockpit/deals.py:240`, `provenance.py:76` | `fetch_filing.index_link` | removed | **Add Deal and the provenance download fail** (STATUS missed this) |
| `cockpit/verify_catalog.py:140` | `LeanChecker(base, filing)` | same signature | Runs, but v1.13.2 bases now fail `schema.columns` |
| `cockpit/backup.py:271` | reads `CHECKER_VERSION` with a regex | `"v0"` | Fine |
| `cockpit/worker.py:272` prepare | `run_model --model` always passed | Sol default changed | Fine: the cockpit always names the model. Only manual CLI use without `--model` changes, from Astra to Sol (STATUS listed this) |
| `run_model --revise-from` | schema detector | refuses non-v0 | Cockpit doesn't use it. Fine |
| `derive_analysis` manifest and `rounds.csv` columns | none in the cockpit | changed | Offline only. Old packets' outputs no longer reproduce. **No cockpit effect** |
| `compare_alex`, `diff_workbooks`, `effort_sweep` | `RULES_29_COLUMN`, `schema_for_header`, `TERM_COLUMNS_V114` | removed | Only the VM copies break, and they are replaced together with the tools |
| `migrate_review.py` | `choice_lists`, `rules_for_instruction` | the file is deleted on the laptop | Triage of old working copies against new runs is gone |
| Instructions pages, comments, activity, accounts, login | no checker | none | Fine |
| Checking out the laptop branch (not just the tools) | catalog, `extraction/`, cockpit source | deleted | **The whole app is gone** |

What STATUS got wrong or left out:
- "Rejects any non-v0 ledger" holds only for v1.13.2. v1.14 is mis-checked silently.
- The `rules_for_instruction` and `LeanChecker(rules=)` failures are wider than `--rules`.
- The `fetch_filing.index_link` removal breaks Add Deal and the provenance download.
- The derive changes don't touch the app.
- The deletions make a branch switch fatal.
- The v114 worktree's own uncommitted work.
- The VM can already run v0 without a deploy.

## Options for the cockpit's existing data

What exists:
- Instructions: v1.13.2 (published), v1.14.1 (published, default), and two drafts.
- 9 catalog deals on v1.13.2 bases, plus 4 added deals.
- 13 working copies. 8 have revisions: Providence & Worcester 16, Mac-Gray 8, Kraton 4, Meredith 4, Penford 2, PetSmart 2, sTec 1, Synacor 1.
- 12 run versions.

**A. Keep the old checker available for legacy versions, read-only.** A rules switch keyed on the instruction, kept beside the new rules. This is exactly a "fallback for older schemas", which AGENTS.md forbids. Moderate work, and it keeps the complexity v0 removed. Not recommended.

**B. Migrate the working copies to Version 1.** Rebase each of the 8 edited copies onto a Version 1 run and carry over the review edits. This needs `migrate_review.py` (deleted on the laptop) or hand work per deal, plus new extractions on Austin's command. Most work. It is also the only option that carries the reviewers' edits forward into live Version 1 working copies.

**C. Freeze and archive, then start Version 1 fresh (recommended: least work and within the rules).**
- Until the Version 1 deploy, leave the VM stack exactly as deployed. It already handles all three old schemas, so nothing breaks in the meantime.
- At step 10, archive the old `state/` as a tarball (together with the 34 exports already on the laptop in the S1 snapshot), and start Version 1 with a new catalog whose deals have no base until their Version 1 extraction.
- Old versions are retired, not re-checked.

**The tension, stated honestly:**
- The 8 hand-edited working copies stop being editable. Their revisions survive only in the archive and the exports.
- Per the "preserve reader rulings" rule, whatever those edits decided must be carried over as evidence (for example into the Version 1 review), not lost.
- If Austin wants those edits live in Version 1, that is option B for those deals only, and it needs a `migrate_review` rebuilt for Version 1: new tool work, not a fallback.
- A middle path is also allowed: keep the frozen old app running read-only at another port or folder for reference, using its own old checker. That is an archive, not a fallback in the new code, but it is a second service to maintain.

## Drafting work (DRAFTING_SPEC §6 and §8)

- **Where:** the laptop. The decisions, evidence and v0 tools are there, and the VM is unreachable. The drafter also shouldn't work where the live app runs.
- **Which tool base:** the laptop's v0 tools, and there is no real choice. §6's "Version" row forbids the old-schema branches that the VM's deployed tools carry. The v0 checker is checker 1.8 with those branches removed, and it produced the same counts on every v1.14.1 workbook.
- **What the drafter should add to `CHANGE_MAP.md` as VM follow-ups for the same deploy:**
  - the cockpit calls `LeanChecker(path, filing)` with no `rules` argument and drops `rules_for_instruction`;
  - editor value lists come from a schema-free `choice_lists()`. Adding it to the checker as a current-schema helper is not a fallback, and it is the smallest adapter; Austin should decide whether the checker exports it;
  - the Questions view and flag parsing accept `R` ids beside `Q` ids;
  - Initiation lists gain `mixed`;
  - `fetch_filing.index_link` is restored, or `deals.py` and `provenance.py` are changed to match.
- **Deliverables §8, items 1–5:** all on the laptop branch. They reach the VM only through step 9.
