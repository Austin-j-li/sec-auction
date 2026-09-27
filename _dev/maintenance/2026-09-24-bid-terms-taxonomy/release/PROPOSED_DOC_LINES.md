# Proposed deploy and release documentation lines (package S6)

25 September 2026, about 23:00 UTC. V114_SPEC §7.12, §12 (window step 9a) and §13 (gates 3a, 8, 9 and 12). Proposed text only: nothing here has been applied. Each part is applied by Austin's order at its step.

**How to read an entry.** Each entry names the file and the line as it stands now, quotes the current text exactly (the whole line, or the passage of the line to replace), and gives the replacement. Line numbers are those of the live files on 25 September at about 23:00 UTC, before any edit below; several entries insert lines, so apply them from the bottom of each file up, or find each passage by its text. Placeholders in angle brackets are values known only at that step: `<date>` (for example "26 September 2026"), `<time>` (UTC), `<sha>` (a full SHA-256), `<id>` (a 12-character cockpit id), `<person>` (Austin or Alex), `<n>`, `<packet>`, `<engine>`, `<effort>`, `<backup>` (the path `backup.py create` printed at window step 3). Where a choice is still open, the alternatives are written `<A | B>`.

**Retargeted to v1.14.1 on 26 September** ([PIPELINE_UPGRADE_SPEC](../../2026-09-26-v1141-streamline/PIPELINE_UPGRADE_SPEC.md) WP7). The instruction to be released is v1.14.1 (SHA-256 `8bdb7c205512c9bcf55ffa7623fba0a8bb4aabaed23c99845fa88b4a80cc8a79`), not v1.14 (`c2d47a47…ab27`), which was trialled and will not be the default. The code to deploy is the v1.14 build updated for v1.14.1, with checker 1.8, carried by `deploy-tools-v1141.patch`. The 25 September `deploy-tools.patch` is superseded and no longer applies. Checker 1.8 checks a 29-column ledger under the v1.14.1 rules by default and under the v1.14 rules with `--rules v1.14`, and the cockpit picks the rules from the instruction's SHA-256. The replacement texts below were retargeted to match. The "Current" quotations and line numbers are still those of 25 September, except D7, D13 and R5, whose text had changed and was re-quoted on 26 September. The WP1 and WP8 documentation edits are still changing these files, and the root `README.md` and `_dev/HANDOFF.md` lines have already shifted. Before applying an entry, find its passage by text and confirm that it still reads as quoted. Figures for checker 1.7 (the pilots' 1 / 18 and 0 / 16, and its SHA-256) are replaced by placeholders to be taken at the deploy.

> **Status, 26 September, about 20:45 UTC.** Part 1's deploy happened at 19:41 UTC (`deploy-tools-v1141.patch`; [receipt](../../2026-09-26-v1141-streamline/deployment-v1141.json)). Its entries were not applied from this file one by one: the current-state docs are being brought up to date directly, so an entry's quoted "Current" text may no longer be there. At gate 9, publishing and the default are done (v1.14.1, id `08caed447f7d`, SHA-256 `8a93df3cc6d989386958e9cb2d74ab34ebc0f07d281e8cc398605a388e066c98`, not the `8bdb7c20…` in the entries), but the export to `SEC_Deal_Ledger_Extraction_Instruction.md` is not; gates 8 (the questionnaire) and 12 are not done. Use `<sha>` = `8a93df3c…` and `<id>` = `08caed447f7d` where an entry needs them.

**Entries marked "(additional)"** are lines the audit (systemic-audit/D §1) did not list, mostly "now" lines written on 25 September that say "not deployed" and so go stale at the deploy or the release. The others are audit D's rows, with its line numbers updated to the live files.

**Inside `_dev/tools/` nothing here is needed.** The deploy-class lines of `_dev/tools/README.md` are already written in the worktree (`~/work/Projects/sec-extraction-v114/_dev/tools/README.md`) and travel in the deploy patch (`deploy-tools-v1141.patch` since 26 September). Its release-class lines are in [tools-readme-release.patch](tools-readme-release.patch), applied at gate 12 (see the end of this file). The one edit left for §12 "Before the window", step 4, is on the worktree README's line 19:

```text
This is checker 1.8, not deployed; the live services run checker 1.6 until the deploy.
```


becomes

```text
This is checker 1.8, deployed on <date>.
```


Step 4 changes only that sentence, so the release patch (whose hunks are at lines 46–52 and 117–123) still applies after it; this was checked on 25 September, and rechecked on 26 September against the worktree README with its checker 1.8 sentence.

If Austin approves window step 6a (the `TMPDIR` drop-ins, `cockpit/deploy/PROPOSED-tmpdir.md`), the worktree README's line 209 also goes stale: in "`cockpit/deploy/PROPOSED-tmpdir.md` proposes moving both services' temporary files off the root disk; it is not applied.", change "it is not applied" to "it was applied at the deploy on <date> (window step 6a)". Make that edit in the worktree before the deploy patch is taken if the approval comes first, or in the checkout at step 6a. Line 209 is outside the release patch's hunks, so the patch still applies.

---

## Part 1. Deploy (§12, window step 9a)

Apply after the worker restart (window step 9) and before the smoke tests, or right after them. All of these describe the deployed code; none changes a research convention. D11 and D23 also state what the window step 10 smoke tests check (every v1.13.2 version shows its stored errors and warnings; the pilots differ only as S1 documents, re-derived for checker 1.8 before the deploy), so apply those two once step 10 has passed.

**Gate 3a.** When Austin requests the commit of the deployed code, stage these lines with it by explicit paths (`_dev/COCKPIT_BUILD.md`, `README.md`, `_dev/HANDOFF.md`, `_dev/RESEARCH_QUESTIONS.md`, `_dev/cockpit/README.md`, `_dev/CHRONOLOGY.md`), separately from the instruction export. Gate 0 commits the earlier uncommitted changes to these files first (`pre-existing/`). The maintenance README is committed only with this folder (gate 13), and `lesson/` only if Austin decides to.

### D1. `_dev/COCKPIT_BUILD.md:47` (audit D row 38; S2)

Current, line 47 (whole line):

```text
- `choices`: mapping field names to allowed labels from the checker. Preserve existing unusual values visibly; do not silently normalize old data.
```

Replace with:

```text
- `choices`: mapping field names to allowed labels from the checker for the displayed version's `ledger_schema` (`check_lean.choice_lists`; a working copy has its base's schema, and one deal can hold versions of both): a v1.13.2 and a 29-column workbook get different lists (the 29-column ledger adds the bid-term columns and its Deadline outcomes, and offers `Extended (late bid accepted)`, not `Late bids accepted`). A 29-column workbook's lists follow its rules, v1.14.1 by default or v1.14 for a run of the v1.14 instruction, chosen from the instruction's SHA-256. The payload's `ledger_schema` says which applies; an unreadable header gives no choices. Preserve existing unusual values visibly; do not silently normalize old data.
```


### D2. `_dev/COCKPIT_BUILD.md`, new line after line 58 (S4, from `evidence/s4/s4-cockpit-build.diff`)

Current, line 58 (whole line):

```text
- `{type:'review',uid,status,note}` records review status.
```

Insert this new line after it (S4's text, verbatim):

```text
- `{type:'bulk_update',sheet:'Deal ledger',uids,values}` sets Process and/or Round (no other column) on many ledger rows, such as a deal's renumbered rounds. It counts as one of a save's 100 operations however many rows it names; `uids` must be distinct live rows (or `new-*` client UIDs from the same save), Process a whole number of 1 or more, Round a whole number of 0 or more or `post`. Each row is recorded, diffed and attributed as under its own update, and row review marks are kept. The ledger editor's **Select** mode stages one after a confirmation naming the events that change.
```


### D3. `_dev/COCKPIT_BUILD.md`, new line after line 61 (additional; S2 with MIG-C)

The edit API already had a rebase operation before v1.14 (the "Use as working-copy base…" action) without a line here; MIG-C adds its preview and the carry-over of finding judgments.

Current, line 61 (whole line):

```text
- `{type:'restore',target_revision}` restores a saved snapshot as a new revision with visible history. Do not erase historical changes.
```

Insert this new line after it:

```text
- `{type:'rebase',target_version}` makes another version the working copy's base, as one new revision. Row marks and row threads stay with the old rows (a restore of the pre-rebase revision brings them back); finding judgments carry over with a `carried_over` record, and their implementation and verification reset. `GET /api/deal/<slug>/rebase?to=<id>` previews this without saving: the counts of revisions, edits, row marks, finding decisions and row threads that stop applying, and both ledger schemas.
```


### D4. `_dev/COCKPIT_BUILD.md:69` (audit D row 39; S3's proposed text, updated for the wave-2 past-revision downloads)

Current, line 69 (whole line):

```text
`GET /api/deal/<slug>/export?version=working` returns XLSX. Preserve four sheets, typed dates/numbers, formats, row references and filters. Raw version exports return the original bytes. Optionally support a per-history-revision export, without mutating state.
```

Replace with:

```text
`GET /api/deal/<slug>/export?version=working` returns XLSX named `<slug>-working-r<N>.xlsx`: the four sheets (typed dates/numbers, formats, row references and filters preserved) plus a fifth sheet, Source, with the EDGAR filing index and complete-submission links and the provenance (Background pages; filing, instruction and raw-workbook hashes; base version; revision; the deal's review status; export time), written by the cockpit and never by the model. `&source=0` returns the four sheets alone, the same sheets `Workspace.export` renders; `Workspace.export`, which `export_repo.py` and `verify_catalog.py` use, stays four-sheet. A past revision (`?version=rev:N`, from History) downloads the same way under the same name pattern, read only, without mutating state. Raw version exports return the original bytes; `&source=1` adds the Source sheet (`<slug>-<version>-with-source.xlsx`). Any other `source` value is HTTP 400.
```


### D5. Root `README.md`, new paragraph after line 10 (audit D row 8, line 5)

Line 5 introduces the list of four sheets and stays as it is. The Source sheet goes after the list:

Current, line 10 (whole line):

```text
- **Deal facts**: deal-level fields such as the parties, price, initiation, advisers and a short account of the process.
```

Insert after it, with a blank line before:

```text
A workbook downloaded from the cockpit's working copy adds a fifth sheet, Source, with the filing's EDGAR links and the download's provenance. The cockpit writes it, never the model; the four-sheet download, which the checker accepts, leaves it out.
```


### D6. Root `README.md:16` (audit D row 8, line 16)

Current, line 16 (this passage of the line, exactly):

```text
records decisions and revision history, and exports Excel.
```

Replace with:

```text
records decisions and revision history, and exports Excel (by default with the Source sheet above). Its checker and value lists follow each workbook's ledger schema and rules, v1.13.2, v1.14 or v1.14.1; checker 1.8 and the v1.14.1 cockpit changes were deployed on <date>.
```


### D7. Root `README.md:19` (additional; a "now" line that goes stale at the deploy; re-quoted 26 September)

Current, line 19 on 26 September (this passage of the line, exactly):

```text
It is not published, not the cockpit default and not deployed, and its five-run retest has not been run.
```

Replace with:

```text
Its code (checker 1.8 and the cockpit, catalog, migration and analysis tools) was deployed on <date>; the v1.14.1 instruction is not yet published or the cockpit default<, and its five-run retest has not been run | ; its five-run retest was run on <date>>.
```


### D8. Root `README.md:48` (additional; optional)

Current, line 48 (this passage of the line, exactly):

```text
environment, mechanical checking, isolated runs, effort sweeps and offline validation.
```

Replace with:

```text
environment, mechanical checking, isolated runs, effort sweeps, review helpers, analysis tables, reviewed-work migration and offline validation.
```


### D9. `_dev/HANDOFF.md:79` (audit D row 18, which cited line 64)

Current, line 79 (this passage of the line, exactly):

```text
findings and decisions, saved history, changes, restore and XLSX export.
```

Replace with:

```text
findings and decisions, saved history, changes, restore and XLSX export (the working-copy download adds a Source sheet with the EDGAR links and provenance, S3), value lists and compare that follow each workbook's ledger schema (S2), a rebase that shows beforehand what stops applying (MIG-C), a bulk Process/Round edit (S4), and checker 1.8 (S1, updated for v1.14.1: v1.14.1 rules by default, v1.14 rules for runs of the v1.14 instruction), deployed on <date>.
```


### D10. `_dev/HANDOFF.md:5` (additional; the deploy sentence only; its instruction sentence changes at gate 9, R7)

Current, line 5 (this passage of the line, exactly):

```text
its instruction candidate is not published, not the cockpit default and not deployed, and none of its code is deployed.
```

Replace with:

```text
its code was deployed on <date> (§12: checker 1.8 and the cockpit, catalog and tool changes, updated for v1.14.1); its instruction candidate is not published and not the cockpit default.
```


### D11. `_dev/HANDOFF.md:14` (additional)

Current, line 14 (whole line):

```text
- **Uncommitted work is live.** Since 24 September, 22:02 UTC, both services have run this checkout's uncommitted tree (`git status`): checker 1.6, which applies the 24 September draft's rules to ledgers with a `Stock %` column and checks every other workbook as v1.13.2; the editor's new value lists; and the deal-level Review status ([taxonomy record](maintenance/2026-09-24-bid-terms-taxonomy/README.md), [cockpit guide](cockpit/README.md)). V114_SPEC §13 gate 0 commits it on its own, before any v1.14 change; the earlier changes to files the v1.14 work edits are saved as patches in that folder's `pre-existing/`. Do not edit code under `_dev/tools/` in this checkout: the services run it (V114_SPEC §0).
```

Replace with:

```text
- **The v1.14.1 code is live.** Since <date>, <time> UTC, both services have run the v1.14 code updated for v1.14.1, deployed from the separate worktree (V114_SPEC §12 as updated by PIPELINE_UPGRADE_SPEC WP7; `deploy-tools-v1141.patch`): checker 1.8, which applies the v1.14.1 rules to ledgers with a `Stock %` column (the v1.14 rules to runs of the v1.14 instruction, chosen from the instruction's SHA-256) and checks every other workbook as v1.13.2; value lists, compare and the Review tab's checker line by ledger schema and rules; the Source sheet in downloads; the safe rebase; the bulk Process/Round edit; the catalog lookup; and the migration and analysis tools; the Opus 5.5 medium extraction default (WP1, <deployed on <date> | deployed with this code>). Every v1.13.2 version reproduced its stored checker result; the two pilots read <n> errors / <n> warnings (Mac-Gray) and <n> / <n> (Providence & Worcester) under 1.8, against their stored 1.6 results of 1 / 16 and 0 / 14 (1.7 read 1 / 18 and 0 / 16). Backup `<backup>`; rollback copy `~/work/archive/v114-deploy/pre-v114-tools.tgz`; baselines in `~/work/archive/v114-deploy/`. <Committed at `<sha>` (gate 3a) | Not yet committed: gate 3a commits it by explicit paths>. Code changes still go through a separate worktree and a deploy Austin orders.
```


### D12. `_dev/HANDOFF.md:17` (additional)

Current, line 17 (this passage of the line, exactly):

```text
The candidate is not published and not the cockpit default, and none of it is deployed. Austin takes the gates in §13; the deploy (§12) comes before any v1.14 run.
```

Replace with:

```text
The candidate is not published and not the cockpit default. The code was deployed on <date> (§12, gate 3); the next gates are the cockpit draft `v1.14.1` (gate 4) and the five-run v1.14.1 retest (gate 5; PIPELINE_UPGRADE_SPEC WP9).
```


### D13. `_dev/HANDOFF.md:30` (additional; re-quoted 26 September)

Current, line 30 on 26 September (this passage of the line, exactly). The WP1 restart will change it again, so at the deploy replace whatever restart clause the line then holds:

```text
both were restarted on 26 September at 12:02:33 UTC for the approved Astra-high default change only ([receipt](maintenance/2026-09-26-astra-default-pro-verification/deployment.json)).
```

Replace with:

```text
both were last restarted on <date> at <time> UTC, for the v1.14.1 deploy. The unit files are <unchanged | changed at window step 6a: <what>>; reference copies are in `_dev/tools/cockpit/deploy/`.
```


### D14. `_dev/HANDOFF.md:19` (additional)

The counts are those of the integrated worktree on 25 September; replace them with the §12 step 2 run's counts. The WP1–WP6 changes add tests, so they will differ.

Current, line 19 (whole line):

```text
- **Tests** (25 September, on the current uncommitted tree, run in the separate worktree): `python3 -m unittest discover -s _dev/tools -p 'test_*.py'` 199 pass; `python3 -m pytest -q -p no:cacheprovider _dev/tools/cockpit/acceptance/test_http.py` 14 pass; `npx vitest run` in `_dev/tools/cockpit/frontend` 53 pass (5 files). The browser suites were not rerun. The earlier 207 Python, 13 HTTP and 52 vitest tests are phase 5's staged build (23 September, before the 24 September changes): 207 is `pytest _dev/tools`, which also collects the HTTP tests (on the current tree it collects 213, that is 199 + 14), and all seven browser suites passed then ([phase 5 PROGRESS](maintenance/2026-09-23-cockpit-phase5-hardening/PROGRESS.md)).
```

Replace with:

```text
- **Tests** (<date>, on the deployed tree, §12 "Before the window" step 2): `python3 -m unittest discover -s _dev/tools -p 'test_*.py'` <292> pass; `python3 -m pytest -q -p no:cacheprovider _dev/tools/cockpit/acceptance/test_http.py` <20> pass; `npx vitest run` in `_dev/tools/cockpit/frontend` <77> pass (<8> files); the seven browser suites pass (`test_browser.mjs` <60> checks). Before the deploy the live tree had 199, 14 and 53 (5 files).
```


### D15. `_dev/HANDOFF.md:73` (additional)

Current, line 73 (this passage of the line, exactly):

```text
the v1.14 code is built in a separate worktree (see Current state) and reaches this checkout only at a deploy Austin orders.
```

Replace with:

```text
the v1.14 code, updated for v1.14.1, was built in a separate worktree and deployed to this checkout on <date>; later code changes follow the same route (build and test in a separate worktree, deploy on Austin's order).
```


### D16. `_dev/RESEARCH_QUESTIONS.md:3` (additional)

Current, line 3 (this passage of the line, exactly):

```text
The v1.14 candidate that adopts them is in preparation: it is not published, not the cockpit default and not deployed.
```

Replace with:

```text
The v1.14.1 candidate that adopts them is not yet published or the cockpit default; checker 1.8, which checks v1.14.1 ledgers (and v1.14 ones under `--rules v1.14`), was deployed on <date>.
```


### D17. `_dev/cockpit/README.md:20` (audit D row 36; S3's and CK's download text)

Current, line 20 (whole line):

```text
4. Save, inspect **Changes**, then export Excel when needed. **History** preserves saved revisions and their attribution. Restoring any earlier revision, including the starting base, creates a new revision rather than erasing history.
```

Replace with:

```text
4. Save, inspect **Changes**, then export Excel when needed. The working copy downloads as `<deal>-working-r<N>.xlsx` with a fifth sheet, Source: the EDGAR filing index and complete-submission links, the Background pages, the filing, instruction and raw-workbook hashes, the base version, the revision, the deal's review status (with "edited since" where it applies) and the export time. The cockpit writes it, never the model, and the checker rejects a workbook that has it; choose "Four sheets only (checker format)" from the menu beside Export Excel for a checker-ready file. An original version downloads as its stored bytes unless you choose "With Source sheet". **History** preserves saved revisions and their attribution; each revision has **Download** (the same two forms, read only) and **Compare with working copy**. Restoring any earlier revision, including the starting base, creates a new revision rather than erasing history.
```


### D18. `_dev/cockpit/README.md:18`, appended sentence (S4's user-guide step)

Current, line 18 (this passage of the line, exactly):

```text
**Clone to split** starts from an existing event and clears Count so a cohort is not silently counted twice.
```

Replace with:

```text
**Clone to split** starts from an existing event and clears Count so a cohort is not silently counted twice. To set Process or Round on many events at once (for example after renumbering rounds), choose **Select** above the event list, tick events (shift-click ticks a range), then **Set Process/Round…**; the dialog names the events that change, and the edit is staged with your other edits and saved as one revision.
```


### D19. `_dev/cockpit/README.md:19`, appended sentence (additional; S2)

Current, line 19 (this passage of the line, exactly):

```text
Use **Review** for the mechanical report, recorded candidate findings, prior decisions and supporting documents.
```

Replace with:

```text
Use **Review** for the mechanical report, recorded candidate findings, prior decisions and supporting documents. Its checker line names the checker version and the rules (v1.13.2, v1.14 or v1.14.1) of the live check and, for an original version, what the checker found when the version was imported; the value lists in the editor follow the same rules.
```


### D20. `_dev/cockpit/README.md:36` (additional; MIG-C)

Current, line 36 (this passage of the line, exactly):

```text
To work from it, open that version and choose **Use as working-copy base…** with a reason; the previous working state stays in History and can be restored.
```

Replace with:

```text
To work from it, open that version and choose **Use as working-copy base…** with a reason. The dialog first lists what stops applying: revisions saved on the current base, row marks and row threads (they stay with the old rows), and finding decisions (judgments carry over; implementation and verification reset). The previous working state stays in History; restore the pre-rebase revision, not revision 0, to undo a rebase.
```


### D21. Maintenance `README.md`, new line after line 13 (audit D row 43; the checker 1.7 line)

Current, line 13 (whole line):

```text
- Tests: 199 Python unit tests, the cockpit import tests and 14 HTTP tests pass. The frontend is unchanged, so the browser and vitest suites were not rerun.
```

Insert after it, as a new paragraph:

```text
Checker 1.8 and the rest of the v1.14 code, updated for v1.14.1, were deployed on <date>, <time> UTC (V114_SPEC §12 as updated by PIPELINE_UPGRADE_SPEC WP7; `release/deploy-tools-v1141.patch`; both services restarted; no model runs; backup `<backup>`). `check_lean.py` 1.8 (SHA-256 `<sha>`, taken at the deploy) applies the v1.14.1 rules to ledgers with a `Stock %` column, or the v1.14 rules under `--rules v1.14` (the cockpit chooses from the instruction's SHA-256), and checks every other workbook as v1.13.2. All nine `extraction/` workbooks and the five v1.13.2 run versions reproduce their stored results, and the fifteen v1.14 trial workbooks reproduce their stored `check.json` under `--rules v1.14`; the two pilots read <n> / <n> and <n> / <n> under 1.8, against their stored 1.6 results of 1 / 16 and 0 / 14 (1.7 read 1 / 18 and 0 / 16, with exactly the differences `evidence/s1/REPRODUCTION.md` documents).
```


### D22. Maintenance `README.md:49` (additional)

Current, line 49 (this passage of the line, exactly):

```text
Nothing is published, made the cockpit default or deployed:
```

Replace with:

```text
Nothing is published or made the cockpit default; the code was deployed on <date> (§12):
```


### D23. `_dev/CHRONOLOGY.md`, new row after line 56 (additional; the deploy record)

Current, line 56 (whole line):

```text
| 25 Sep | V114_SPEC: Austin's decisions D1–D27 make v1.14 a system-wide upgrade (instruction, checker, cockpit, tools, moving reviewed work, a first analysis tool, documentation, deploy and release), after four read-only system audits and a review of the spec's first draft | An agent team implements its work packages: the instruction candidate in the maintenance folder, the code in a separate worktree. Nothing published, made default or deployed; Austin takes the gates (§13) | [V114_SPEC](maintenance/2026-09-24-bid-terms-taxonomy/V114_SPEC.md), [audits](maintenance/2026-09-24-bid-terms-taxonomy/systemic-audit/) |
```

Insert after it:

```text
| <date>, <time> UTC | v1.14 code, updated for v1.14.1, deployed at Austin's order (V114_SPEC §12; PIPELINE_UPGRADE_SPEC WP7, `deploy-tools-v1141.patch`): checker 1.8 (S1, WP2), cockpit schema awareness with rules chosen from the instruction's SHA-256 and a safe rebase (S2, MIG-C, WP4), the Source sheet in downloads (S3), the bulk Process/Round edit (S4), the catalog lookup and verifier (S5), the standalone, migration and analysis tools (S7, MIG-T, P, WP3, WP5, WP6) and deploy readiness (OPS); both services restarted; no model runs | Every v1.13.2 version reproduces its stored checker result; the pilots read <n> / <n> and <n> / <n> under 1.8 (stored 1.6: 1 / 16 and 0 / 14). The instruction is unchanged: v1.13.2 stays published, the default and the repository file. <Committed at `<sha>` | Not yet committed> | [V114_SPEC §12](maintenance/2026-09-24-bid-terms-taxonomy/V114_SPEC.md), [PIPELINE_UPGRADE_SPEC](maintenance/2026-09-26-v1141-streamline/PIPELINE_UPGRADE_SPEC.md), [release/](maintenance/2026-09-24-bid-terms-taxonomy/release/) |
```


### D24. Maintenance `README.md:64` (additional; the lead, 25 September, 23:45 UTC: a "now" line written at the end of wave 3)

Current, line 64 (this passage of the line, exactly):

```text
Next: the lead's report to Austin (§7.14), then Austin's gates (§13), starting with gate 0
```

Replace with:

```text
Next: Austin's remaining gates (§13), after the deploy of <date>; gate 0
```


### D25. `_dev/HANDOFF.md:71` (additional; same origin)

Current, line 71 (this passage of the line, exactly):

```text
the v1.14 deliverables of the spec's three waves (none published or deployed)
```

Replace with:

```text
the v1.14 deliverables of the spec's three waves (the code, updated for v1.14.1, deployed on <date>; the v1.14.1 instruction not yet published)
```


### D26. `_dev/HANDOFF.md:91` (additional; same origin)

Current, line 91 (this passage of the line, exactly):

```text
None of it is deployed, published or committed, and no model run has been made.
```

Replace with:

```text
The code was deployed on <date> (§12); the v1.14.1 instruction is not yet published.
```

Line numbers are those of 25 September, 23:45 UTC; if D9 to D15 have changed HANDOFF by then, find each passage by its text. D24 to D26 correct text the final "now" refresh wrote; whether gate 0 and gate 1 are still ahead at the deploy is for whoever applies them to check.

---

## Part 2. Release (§13, gates 8, 9 and 12)

### At gate 8 (when Austin sends the replacement questions)

### R1. `lesson/independent-audit-2026-09-23/questions-for-alex/README.md:5` (audit D row 51)

`lesson/` is untracked evaluation material; this edit is for its own record. The DOCX is still being condensed, so its SHA-256 is taken when it is sent (on 25 September, 22:55 UTC, it was `31e6909b…`, which will change).

Current, line 5 (this passage of the line, exactly):

```text
the current version (SHA-256 `faab1d66…`;
```

Replace with:

```text
the 24 September version, current until <date> (SHA-256 `faab1d66…`;
```

And insert after line 1 (the title), with a blank line before and after:

```text
**Replaced on <date>.** Austin sent Alex the replacement questions of 25 September (V114_SPEC §5, D19), rebuilt for v1.14.1 (PIPELINE_UPGRADE_SPEC WP8): `_dev/maintenance/2026-09-24-bid-terms-taxonomy/Questions_for_Alex_2026-09-25.docx`, SHA-256 `<sha>`, <how and where it was sent>. The 24 September document below is kept unchanged.
```


### At gate 9 (publish as `v1.14.1`, make it the default, export the instruction)

Under PIPELINE_UPGRADE_SPEC WP9, v1.14.1 is published in the cockpit as `v1.14.1`. Its stored SHA-256 must equal `8bdb7c205512c9bcf55ffa7623fba0a8bb4aabaed23c99845fa88b4a80cc8a79`. It becomes the default only after Austin accepts the five-run retest. The v1.14 candidate may first be published as a frozen `v1.14` to give the trial runs provenance, but it never becomes the default. Run `export_repo.py instruction v1.14.1` only at the release, because it overwrites the frozen repository instruction.

### R2. `AGENTS.md:12` (audit D row 2; §13 gate 9 wording)

Current, line 12 (whole line):

```text
- `SEC_Deal_Ledger_Extraction_Instruction.md`: the working instruction (v1.13.2, frozen). Agents edit it only with Austin's approval. Austin and Alex version instructions in the cockpit app (see below); the app never changes this file.
```

Replace with:

```text
- `SEC_Deal_Ledger_Extraction_Instruction.md`: the working instruction (v1.14.1, frozen; exported on <date> from the cockpit's published `v1.14.1`, SHA-256 `8bdb7c205512c9bcf55ffa7623fba0a8bb4aabaed23c99845fa88b4a80cc8a79`). Agents edit it only with Austin's approval. Austin and Alex version instructions in the cockpit app (see below); the app never changes this file, which `_dev/tools/cockpit/export_repo.py` writes for a commit Austin requests.
```


### R3. `AGENTS.md:16` (audit D row 4)

Current, line 16 (this passage of the line, exactly):

```text
Older instruction history is in Git; see `_dev/CHRONOLOGY.md`.
```

Replace with:

```text
Older instruction history is in Git; see `_dev/CHRONOLOGY.md`. The v1.14.1 decision record is `<_dev/maintenance/2026-09-24-bid-terms-taxonomy/V114_SPEC.md | _dev/DECISIONS_v1.14.md>` (Austin's decisions D1–D27 of 25 September; §13 gate 13 chooses the form), as amended by `_dev/maintenance/2026-09-26-v1141-streamline/V1141_SPEC.md` (R1–R6, H1–H4 and D1–D6 of 26 September).
```


### R4. Root `README.md:14` (audit D row 6)

Current, line 14 (whole line):

```text
- **Instruction.** The working extraction instruction is v1.13.2 and is frozen. Further edits require Austin's approval and must be general rather than justified by a single reviewed deal.
```

Replace with:

```text
- **Instruction.** The working extraction instruction is v1.14.1 and is frozen: published in the cockpit as `v1.14.1` and made the default on <date>, and exported to `SEC_Deal_Ledger_Extraction_Instruction.md` on <date> (SHA-256 `8bdb7c205512c9bcf55ffa7623fba0a8bb4aabaed23c99845fa88b4a80cc8a79`). v1.13.2 stays in Git history and as a published cockpit version<; the trialled v1.14 candidate is a frozen cockpit version kept for the trial runs' provenance | >. Further edits require Austin's approval and must be general rather than justified by a single reviewed deal.
```


### R5. Root `README.md:18` (additional; after D7)

Current, line 19 (whole line, as D7 leaves it at the deploy, with that step's values in place of its placeholders; re-quoted 26 September):

```text
- **Next step.** The v1.14 upgrade ([specification](_dev/maintenance/2026-09-24-bid-terms-taxonomy/V114_SPEC.md)) is now aimed at v1.14.1, a streamlined candidate instruction written after the fifteen-run v1.14 trial ([V1141_SPEC](_dev/maintenance/2026-09-26-v1141-streamline/V1141_SPEC.md); pipeline changes in [PIPELINE_UPGRADE_SPEC](_dev/maintenance/2026-09-26-v1141-streamline/PIPELINE_UPGRADE_SPEC.md)). Its code (checker 1.8 and the cockpit, catalog, migration and analysis tools) was deployed on <date>; the v1.14.1 instruction is not yet published or the cockpit default<, and its five-run retest has not been run | ; its five-run retest was run on <date>>. Reviewed work moves onto v1.14.1 deal by deal, once that deal's v1.14.1 run has been reviewed.
```

Replace with:

```text
- **Next step.** v1.14.1 of the instruction, checker and cockpit is in place ([V114_SPEC](_dev/maintenance/2026-09-24-bid-terms-taxonomy/V114_SPEC.md), [V1141_SPEC](_dev/maintenance/2026-09-26-v1141-streamline/V1141_SPEC.md) and [PIPELINE_UPGRADE_SPEC](_dev/maintenance/2026-09-26-v1141-streamline/PIPELINE_UPGRADE_SPEC.md); code deployed on <date>, instruction published on <date> and made the default on <date>, after the five-run retest). The remaining deals are re-extracted under it, and reviewed work moves onto v1.14.1 deal by deal, once that deal's v1.14.1 run has been reviewed.
```


### R6. Root `README.md:24` (audit D row 6, which cited line 23)

Current, line 24 (whole line):

```text
| [`SEC_Deal_Ledger_Extraction_Instruction.md`](SEC_Deal_Ledger_Extraction_Instruction.md) | The working extraction instruction, v1.13.2 (frozen). |
```

Replace with:

```text
| [`SEC_Deal_Ledger_Extraction_Instruction.md`](SEC_Deal_Ledger_Extraction_Instruction.md) | The working extraction instruction, v1.14.1 (frozen). |
```


### R7. `_dev/HANDOFF.md:5` (audit D row 10; the instruction sentences only, after D10)

Current, line 5 (this passage of the line, exactly):

```text
The working instruction is **v1.13.2, frozen**. A v1.14 upgrade is being prepared under [V114_SPEC.md](maintenance/2026-09-24-bid-terms-taxonomy/V114_SPEC.md) (Austin's decisions D1–D27, 25 September);
```

Replace with:

```text
The working instruction is **v1.14.1, frozen**: published in the cockpit as `v1.14.1` (id `<id>`) and made the default on <date>, and exported to `SEC_Deal_Ledger_Extraction_Instruction.md` on <date> (SHA-256 `8bdb7c205512c9bcf55ffa7623fba0a8bb4aabaed23c99845fa88b4a80cc8a79`); v1.13.2 stays in Git history and as a published cockpit version. The upgrade is specified in [V114_SPEC.md](maintenance/2026-09-24-bid-terms-taxonomy/V114_SPEC.md) (Austin's decisions D1–D27, 25 September) and [V1141_SPEC.md](maintenance/2026-09-26-v1141-streamline/V1141_SPEC.md) (R1–R6, H1–H4 and D1–D6, 26 September);
```


After D10 the rest of that sentence reads "its code was deployed on <date> …; its instruction candidate is not published and not the cockpit default." At gate 9 delete that last clause ("; its instruction candidate is not published and not the cockpit default"), so that the sentence ends "…; its code was deployed on <date> (§12: checker 1.8 and the cockpit, catalog and tool changes, updated for v1.14.1)."

### R8. `_dev/HANDOFF.md:16` (additional)

Current, line 16 (whole line):

```text
- **Instructions in the cockpit.** v1.13.2, published and the default; draft `a4ca26ecfa92`, the 24 September v1.14 draft, unpublished; draft `73f21eb8c09a`, text identical to v1.13.2, unused.
```

Replace with:

```text
- **Instructions in the cockpit.** v1.14.1 (id `<id>`), published by <person> on <date> and made the default by <person> on <date><; v1.14 (id `<id>`), the trialled candidate, published frozen on <date> for the trial runs' provenance, never the default | >; v1.13.2, published, the default until then; draft `a4ca26ecfa92`, the 24 September v1.14 draft, unpublished; draft `73f21eb8c09a`, text identical to v1.13.2, unused.
```


### R9. `_dev/HANDOFF.md:59` (audit D row 15, which cited line 46)

Current, line 59 (whole line):

```text
| `SEC_Deal_Ledger_Extraction_Instruction.md` | The only working extraction instruction; v1.13.2. |
```

Replace with:

```text
| `SEC_Deal_Ledger_Extraction_Instruction.md` | The only working extraction instruction; v1.14.1 (exported <date> from the cockpit's published `v1.14.1`, the default; SHA-256 `8bdb7c205512c9bcf55ffa7623fba0a8bb4aabaed23c99845fa88b4a80cc8a79`). |
```


### R10. `_dev/RESEARCH_QUESTIONS.md:3` (audit D row 23; after D16)

Current, line 3 (this passage of the line, exactly):

```text
The working instruction is v1.13.2; its conventions are sections E1–E14
```

Replace with:

```text
The working instruction is v1.14.1 (published and made the cockpit default on <date>); its conventions are sections E1–E14
```


and replace D16's sentence ("The v1.14.1 candidate that adopts them is not yet published or the cockpit default; checker 1.8, which checks v1.14.1 ledgers (and v1.14 ones under `--rules v1.14`), was deployed on <date>.") with:

```text
v1.14.1 adopts them. The provisional answers were <sent to Alex on <date> | not yet sent to Alex>.
```


### R11. `_dev/cockpit/README.md:42` (audit D row 37)

Current, line 42 (this passage of the line, exactly):

```text
v1.13.2, the repository's working instruction, was imported as the first published version and the default.
```

Replace with:

```text
v1.13.2, then the repository's working instruction, was imported as the first published version and the default. v1.14.1 was published on <date> by <person> and made the default on <date> by <person>; it has been the repository's working instruction since its export on <date>.
```


### R12. `_dev/CHRONOLOGY.md`, new row at the end of the table (audit D row 22; §13 gate 9, with D1–D27)

After line 56, or after D23's row if that was added.

Insert:

```text
| <date> | v1.14.1 published in the cockpit as `v1.14.1` (id `<id>`, SHA-256 `8bdb7c205512c9bcf55ffa7623fba0a8bb4aabaed23c99845fa88b4a80cc8a79`) by <person> and made default by <person>; exported to `SEC_Deal_Ledger_Extraction_Instruction.md` at Austin's request | Decisions D1–D27 of 25 September, amended by R1–R6, H1–H4 and D1–D6 of 26 September (V1141_SPEC); consistency review R; checker 1.8 and cockpit S2/S3 deployed <date>; the fifteen-run v1.14 trial and the five-run v1.14.1 retest, reviewed against the edited v1.13.2 working copies; provisional decisions sent to Alex <date or not yet> | V114_SPEC, V1141_SPEC, packet <…> |
```


§13's text of this row says "D1–D26"; D27 (the §8 coding calls Austin confirmed) is part of the decisions, so the row says D1–D27. For links in the last cell, use `[V114_SPEC](maintenance/2026-09-24-bid-terms-taxonomy/V114_SPEC.md)`, `[V1141_SPEC](maintenance/2026-09-26-v1141-streamline/V1141_SPEC.md)` and the packet's path.

### At gate 12 (`extraction/`, D25; §13 gate 12 step 7)

These assume the relocation (D25): the nine v1.13.2 workbooks move, bytes unchanged, to `_dev/reviews/2026-09-22-opus55-reextraction/workbooks/`, the catalog is repointed, and the v1.14.1 blind runs are exported to `extraction/`. Apply them in the gate 12 commit, with `d25-tools.patch` and `tools-readme-release.patch`. Gate 11 (rebases) will already have changed the "What is ready for Austin" section of HANDOFF, which should then be rewritten as a whole; G5 is only the minimum.

### G1. `AGENTS.md:14` (audit D row 3)

Current, line 14 (whole line):

```text
- `extraction/`: the current blind extractions, made by Claude Opus 5.5 at medium effort under v1.13.2 on 22 September (`_dev/reviews/2026-09-22-opus55-reextraction/`; the replaced Opus 5 high workbooks are archived outside the checkout and recoverable from Git at `03d59b1`). `_dev/cockpit/catalog.json` holds one immutable version per deal, these nine extractions, which are unreviewed and not research-ready. Earlier Opus 5 drafts and correction passes remain only as evidence in their review packets. Preserve raw outputs when a separate revision is authorized.
```

Replace with:

```text
- `extraction/`: the current blind extractions, made by <engine> at <effort> effort under v1.14.1 on <dates> (`_dev/reviews/<packet>/`) and exported from the cockpit on <date>. They are <unreviewed | …> and not research-ready. The nine Opus 5.5 medium v1.13.2 extractions of 22 September moved, bytes unchanged, to `_dev/reviews/2026-09-22-opus55-reextraction/workbooks/` (the Opus 5 high workbooks before them are recoverable from Git at `03d59b1`); they remain the cockpit's catalog versions, and the working-copy bases of the deals not yet rebased onto their v1.14.1 run. `_dev/cockpit/catalog.json` names <only those nine | those nine and the v1.14.1 exports>. Earlier Opus 5 drafts and correction passes remain only as evidence in their review packets. Preserve raw outputs when a separate revision is authorized.
```


### G2. Root `README.md:15` (audit D row 7)

Current, line 15 (whole line):

```text
- **Extractions.** `extraction/` holds nine blind extractions, one per deal, made by Claude Opus 5.5 at medium effort under v1.13.2 on 22 September. They are **unreviewed and not research-ready**. Checker results are mechanical: they record structural errors and warnings, not accuracy.
```

Replace with:

```text
- **Extractions.** `extraction/` holds nine blind extractions, one per deal, made by <engine> at <effort> effort under v1.14.1 (<dates>). They are **<unreviewed> and not research-ready**. The v1.13.2 extractions of 22 September, which the edited cockpit working copies started from, are kept in `_dev/reviews/2026-09-22-opus55-reextraction/workbooks/`. Checker results are mechanical: they record structural errors and warnings, not accuracy.
```


### G3. Root `README.md:26` (additional; optional)

Current, line 26 (whole line):

```text
| `extraction/` | The current blind extractions, one `<deal>.xlsx` per deal. |
```

Replace with:

```text
| `extraction/` | The current blind extractions under v1.14.1, one `<deal>.xlsx` per deal. |
```


### G4. `_dev/HANDOFF.md:5` (audit D row 10, the `extraction/` sentence)

Current, line 5 (this passage of the line, exactly):

```text
The current workbooks in `extraction/` are Opus 5.5 medium extractions of all nine deals ([re-extraction packet](reviews/2026-09-22-opus55-reextraction/README.md)); the replaced Opus 5 high originals are archived outside the checkout and recoverable from Git at `03d59b1`.
```

Replace with:

```text
The workbooks in `extraction/` are the v1.14.1 blind runs of the nine deals (<engine> <effort>, <dates>; [packet](reviews/<packet>/README.md)), exported on <date>. The Opus 5.5 medium v1.13.2 extractions of 22 September ([re-extraction packet](reviews/2026-09-22-opus55-reextraction/README.md)) moved, bytes unchanged, to that packet's `workbooks/` and stay the catalog versions; the Opus 5 high originals before them are recoverable from Git at `03d59b1`.
```


### G5. `_dev/HANDOFF.md:26` (additional)

Current, line 26 (this passage of the line, exactly):

```text
their Opus 5.5 medium v1.13.2 extraction in `extraction/` (22 September), which is also the working-copy base.
```

Replace with:

```text
their Opus 5.5 medium v1.13.2 extraction of 22 September, since <date> in `reviews/2026-09-22-opus55-reextraction/workbooks/`, which is the working-copy base unless the deal has been rebased onto its v1.14.1 run.
```


### G6. `_dev/HANDOFF.md:53` (additional)

Current, line 53 (this passage of the line, exactly):

```text
receipts, checker results and hashes for the nine current workbooks, and the catalog's import and live verification.
```

Replace with:

```text
receipts, checker results and hashes for the nine v1.13.2 workbooks (in its `workbooks/` folder since <date>), and the catalog's import and live verifications.
```


### G7. `_dev/HANDOFF.md:61` (audit D row 16, which cited line 48)

Current, line 61 (whole line):

```text
| `extraction/` | Current Opus 5.5 medium v1.13.2 extractions of all nine deals; the cockpit's catalog versions and working-copy bases for them. Run versions live in the ignored cockpit state. |
```

Replace with:

```text
| `extraction/` | The v1.14.1 blind extractions of the nine deals (<engine> <effort>, <dates>; packet `_dev/reviews/<packet>/`), exported from the cockpit on <date>. Run versions live in the ignored cockpit state. |
```


### G8. `_dev/HANDOFF.md:63` (additional)

Current, line 63 (whole line):

```text
| `_dev/reviews/2026-09-22-opus55-reextraction/` | Receipts, checker results and hashes for the nine Opus 5.5 medium extractions, and the catalog's import and live verification. |
```

Replace with:

```text
| `_dev/reviews/2026-09-22-opus55-reextraction/` | The nine Opus 5.5 medium v1.13.2 extractions (`workbooks/`, moved from `extraction/` on <date>, bytes unchanged; the cockpit's catalog versions), with their receipts, checker results and hashes, and the catalog's import and live verifications (`catalog-verification-<UTC timestamp>.json`). |
```


### G9. `_dev/COCKPIT_BUILD.md:73` (audit D row 40)

Current, line 73 (this passage of the line, exactly):

```text
Since 22 September each deal has one version, its Opus 5.5 medium extraction `opus55-medium`, which is also the default base; earlier workbooks remain only as packet evidence.
```

Replace with:

```text
Each catalog deal has one catalog version, its Opus 5.5 medium v1.13.2 extraction `opus55-medium` (22 September), which is also the default base. Since <date> its `path` is `_dev/reviews/2026-09-22-opus55-reextraction/workbooks/<slug>.xlsx`, where the workbook moved, bytes unchanged, from `extraction/` (id, hash and instruction version kept). Run versions, and the base of a rebased working copy, come from the `versions` table of the working-state database. Earlier workbooks remain only as packet evidence.
```


### G10. `_dev/reviews/2026-09-21-datalink-pilot/README.md:3` (audit D row 48)

Current, line 3 (this passage of the line, exactly):

```text
Since 22 September the current `extraction/datalink.xlsx` is a different, newer Opus 5.5 medium draft, and the cockpit shows only that draft.
```

Replace with:

```text
A different, newer Opus 5.5 medium v1.13.2 draft of 22 September is the cockpit's catalog version; since <date> it is at `_dev/reviews/2026-09-22-opus55-reextraction/workbooks/datalink.xlsx`, and `extraction/datalink.xlsx` is the v1.14.1 run `<id>` (<date>). The cockpit's Datalink working copy <is based on that draft | was rebased onto the v1.14.1 run on <date>>.
```


### G11. `_dev/reviews/2026-09-21-mac-gray-pilot/README.md:3` (additional; the "now" text S6 wrote on 25 September)

Current, line 3 (this passage of the line, exactly):

```text
Since 22 September the current `extraction/mac-gray.xlsx` is a different, newer Opus 5.5 medium draft. The cockpit's Mac-Gray working copy is based on that draft and applies R01 (revisions 6–7);
```

Replace with:

```text
A different, newer Opus 5.5 medium v1.13.2 draft of 22 September is the cockpit's catalog version; since <date> it is at `_dev/reviews/2026-09-22-opus55-reextraction/workbooks/mac-gray.xlsx`, and `extraction/mac-gray.xlsx` is the v1.14.1 run `<id>`. The cockpit's Mac-Gray working copy <is based on that draft and applies R01 (revisions 6–7) | was rebased onto the v1.14.1 run on <date>, with what still held of the earlier review ported as revision <n>>;
```


### G12. `_dev/tools/README.md` lines 49 and 120 (audit D rows 30 and 32)

In [tools-readme-release.patch](tools-readme-release.patch) (SHA-256 `59d44598ef31a10e51583dd8694defe726f5f9a9b4616fa71c820c764b532dad` since its lines were retargeted to v1.14.1 on 26 September; the 25 September version, `581bbb29…58c1`, is kept as `tools-readme-release.patch.pre-v1141`), made with `diff -u` between two copies of the worktree README after the deploy-class edits, with paths `a/_dev/tools/README.md` and `b/_dev/tools/README.md`. From `$LIVE`, after the deploy patch (`deploy-tools-v1141.patch`) and §12 step 4:

```text
git apply --check _dev/maintenance/2026-09-24-bid-terms-taxonomy/release/tools-readme-release.patch
git apply _dev/maintenance/2026-09-24-bid-terms-taxonomy/release/tools-readme-release.patch
```


Rollback: `git apply -R` the same file. Line 49 names the relocated workbooks, the unchanged catalog ids and hashes, and `verify_catalog.py`'s new path check; line 120 says that catalog deals, too, can now be exported to `extraction/`. If Austin makes the exports catalog entries (gate 12.6), line 120's last sentence already covers it ("a path it names later becomes immutable too"), but `verify_catalog.py` must first accept two catalog versions per deal (release/README.md step 7).

## Left alone (historical)

`_dev/COCKPIT_APP_SPEC.md`, CHRONOLOGY line 42, the 22 September re-extraction README, `lesson/README.md`, and the dated deploy record in the maintenance README (lines 9–13), which D21 adds to rather than edits.
