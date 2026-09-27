# Pipeline upgrade for v1.14.1: report

26 September 2026, about 19:30 UTC. This implements `PIPELINE_UPGRADE_SPEC.md`: WP1–WP6 and WP8 are done, and WP7 and WP9 are prepared but not executed.

> **Status, 26 September, about 20:45 UTC.** The report below is as written at 19:30 and is not revised. Since then, all ordered by Austin: the WP7 deploy (runbook B, includes WP1) was done at 19:41 UTC ([`deployment-v1141.json`](deployment-v1141.json)), so checker 1.8, derive_analysis 0.3 and the Opus 5.5 medium default are live; the candidate was edited with candidate issues 2 and 4–10 (new SHA-256 `8a93df3cc6d989386958e9cb2d74ab34ebc0f07d281e8cc398605a388e066c98`; the reviewed text is kept at [`checks/candidate-8bdb7c20-as-reviewed.md`](checks/candidate-8bdb7c20-as-reviewed.md)); Austin published it in the cockpit as v1.14.1 (id `08caed447f7d`) at 20:18 UTC and made it the default; the five-deal retest ran at 20:19 and passed ([results](../../reviews/2026-09-26-v1141-retest/README.md)); Austin decided Datalink (issue 1). WP3 item 8 is done: the 3.3(a) table is recomputed from the retest and the questionnaire rebuilt (`../2026-09-24-bid-terms-taxonomy/evidence/a2/README.md`). The GATE list at the end has a matching note.

**Nothing live changed.**
- **Services:** `ledger-cockpit` and `ledger-worker` still run the build started at 12:02:33 UTC, which has the Astra-high default and checker 1.6. The live `dist/` was not rebuilt.
- **Not done:** no extraction or model call, no publish, no default change, no rebase, no commit, no push, and nothing sent to Alex.
- **Instruction candidate:** unchanged, SHA-256 `8bdb7c205512c9bcf55ffa7623fba0a8bb4aabaed23c99845fa88b4a80cc8a79`, checked at the end.
- **Main checkout:** its earlier uncommitted work and `_dev/cockpit/state/` are preserved. Before any change, both trees were backed up to the session scratchpad.
- **Off limits:** `ref/`, `lesson/` and the workbooks in `extraction/` were not read.

Subagents (Opus) did WP3, WP5, WP8 and the WP7 doc retargeting. I checked each one's work against the spec and reran the suites myself.

## Decisions applied (Austin, 26 September)

| # | Applied as |
|---|---|
| Q1 | `check_lean.py` takes `--rules v1.14\|v1.14.1` (and `LeanChecker(rules=…)`), and `derive_analysis.py` takes `--rules`. `compare_alex.py` and `migrate_review.py triage` got the same option. `check_lean.RULES_BY_INSTRUCTION` maps `8bdb7c20…` to v1.14.1 and `c2d47a47…` to v1.14; `rules_for_instruction()` is the one lookup, used by the cockpit, the worker, the runner and the sweep. A 29-column workbook with no known instruction is checked as v1.14.1. The 15 trial workbooks keep v1.14 by explicit selection. **Addition:** the 24 September draft `f9595d74…` also maps to v1.14, so the Mac-Gray and P&W pilot runs keep the rules they were run and checked under. |
| Q2 | The process Question does not count toward the five. The checker, the sweep and the retest script share one recognizer, `check_lean.is_process_question`. |
| Q3 | D1–D6 as the candidate implements them. The checker encodes D1 (routes), D3 (the Light rule) and D4 (five Questions). D5 needed no change, and D6 cannot be checked mechanically. |
| Q4 | The questionnaire's 2b-6 and its 3.3(a) commentary now make Mac-Gray Party B Contingent and Heavy (H1) as a consequence of R2. |

## Changes

### WP1. Engine back to Opus 5.5 medium (both trees)
- **`cockpit/runs.py`:** `DEFAULT_ENGINE = "opus55"`, and `MODEL`/`ENGINE` name Opus 5.5 again. The per-engine `DEFAULT_EFFORT` stays: medium, and high for astra6. `LEGACY_ENGINE` stays opus55.
- **`cockpit/worker.py`:** no change needed. A job with no engine selection already falls back to `LEGACY_ENGINE`, which is Opus.
- **`frontend/src/runs.js`:** `DEFAULT_ENGINE` is Opus 5.5 · medium and `DEFAULT_EFFORT` is medium. Astra keeps high through `ENGINE_EFFORT`. Opus is preselected when the Claude account is connected; otherwise the first connected engine is. An explicit choice is kept.
- **`sandbox/run_model.py`:** `prepare` defaults to provider opus, which runs `claude-opus-5-5` at medium. `MODEL_DEFAULT_EFFORT` keeps Astra at high when it is chosen. The help texts are fixed. The sol transport's first model is still gpt-6-astra, so `--provider sol` alone gives Astra high.
- **Tests:**
  - `test_cockpit_phase4.py`: the default test now expects Opus medium, and an explicit Astra choice gets high.
  - `test_run_model.py`: the default prepare is opus medium, and explicit sol gets Astra high.
  - `runs.test.js`: the summary and preselection assertions are flipped.
  - Provenance tests are unchanged, so legacy jobs are still not relabelled. `test_cockpit_runs.py` and `test_cockpit_deals.py` already pass an explicit engine and needed no edit.
- **Frontend:**
  - Main's frontend is built into `wp1-main-dist/` in this folder, **not into the live `dist/`**. The server reads `dist/` from disk, so a build there would have changed the live page before the GATE.
  - The v114 tree's `dist/` is rebuilt.
  - The swap commands, which keep the old assets, are in `DEPLOY_RUNBOOK.md`.
- **Docs:** the engine lines in `AGENTS.md`, the root `README.md`, `_dev/HANDOFF.md`, `_dev/tools/README.md` (both trees), `_dev/cockpit/README.md` and `_dev/CHRONOLOGY.md`. They say the change is "built; live after the WP1 restart".

### WP2. Checker 1.8 (`check_lean.py`, v114 tree)
- **Version and docs:** version 1.8 with new revision text. The docstring documents the rules selector and three mechanical readings:
  - a cohort row is one with Count above 1, or whose Who starts with a number or names a group ("parties", "bidders", "signers" …);
  - the process Question is the first Question beginning "Process:" or citing a Process terminated or Process restarted row by #;
  - a process marker that closes no one leaves Count blank.
- **Constants:** `SCHEMA_V1141`, `RULES_29_COLUMN`, `is_29_column()`, `markers()`, `initiation_values()`, `fact_field_options()`, `is_cohort()`, `is_process_question()` and `rules_for_instruction()`. `choice_lists("v1.14.1")` gives CVR/earnout and Antitrust `["Y"]` and three Initiation values.
- **The v1.14.1 rules, by spec item:**
  1. A Note over 40 words is an error (`ledger.note_length`).
  2. Inferred = Y on any row but an exit, Round opened or Process restarted is an error (`ledger.inferred_event`).
  3. Formality Unclear on a non-cohort row is an error (`bid.formality_unclear`).
  4. Antitrust Y without Regulatory Concern is an error.
  5. A Stock % range is an error, with a message pointing to Part stock.
  6. More than five Questions besides the process Question is a warning (`questions.count`).
  7. Rounds Due dates is compared by prefix ("none stated (…)").
  8. CVR/earnout and Antitrust take Y or blank.
  9. Initiation takes three values, and the long field label is refused.
  10. The auction screen must start Met or Not met and give a number; Uncertain and "count unknown" are refused.
  11. The mandatory map and deadline-outcome Question warnings are off. A new warning, `questions.process_missing`, fires on more than one process with no process Question.
  12. The process Question is recognized as documented above, and is tested.
  13. A Question entry over 60 words is a warning.
  14. `ledger.inference_note` is a warning that applies only to inferred Process restarted rows and cohort Did not submit rows. The message is fixed.
  15. Count is required on Bidding group changed rows. A blank Count on a process marker is a warning (`ledger.count_marker`). Round opened stays a row about no bidder.
  16. A Round 0 row after its process's round-1 Round opened row is an error (`round.zero_after_opening`).
  17. "Same as #n" must point to an earlier bid row with the same Who (error, `ledger.same_as`). A Heavy row's Note must begin H1:, H2: or H3: after any "Same as #n. " (warning, `conditions.heavy_trigger`, replacing `conditions.level_unsupported` under v1.14.1).
  18. A Bid reaffirmed row must be Formal and carry "Same as #n" (errors).
  19. Light with Due diligence neither Complete nor Incomplete is a **warning** (`conditions.light_support`); see the candidate issues below for why not an error.
  20. A Count Note qualifier ("Count: more than ten") is accepted silently. A numeric range, or "unknown", is a warning (`ledger.count_range`).
  21. The stale "F.4" and "(B, F.3)" references are fixed.
  22. The tests are updated (see below).
- **Also under v1.14.1:** the replaced deadline outcome "Late bids accepted" is not an allowed value.
- **v1.14 rules:** unchanged; they are checker 1.7's behaviour.
- **Not edited:** main's checker 1.6.
- **`test_check_lean.py`:**
  - The fixture bid is no longer Heavy with no trigger; it is now Unclear, pre-NDA.
  - The existing tests run explicitly under `rules="v1.14"`.
  - `build_v1141_fixture` has no silencing Q1.
  - The Varies, Initiation, Uncertain and Stock % range cases each have a v1.14.1 counterpart.
  - A new class, `LeanCheckerV1141Tests`, has 26 tests, each asserting the v1.14.1 result and the v1.14 result it replaces.
  - `build_examples_fixture` turns the candidate's five Examples into one v1.14.1 deal. It is kept, with its check, in `checks/examples/`.
- **Consumers adapted to the new schema value:** `derive_analysis.py` (three `is_29_column` checks) and the `run_model.py` revision guard. Several tests' default-schema expectations changed from "v1.14" to "v1.14.1", because the default is intended.

### WP3. Analysis (`derive_analysis.py` 0.3, contract 0.2)
- **Rules selector (Q1):** `--rules` and a `rules` parameter. The manifest records `rules_requested` and `switches_retired`.
- **P1:** a new column, `upfront_price_kind`; a blank-price bid row is not a price observation (H4); Mac-Gray A #61/#62 are fixed. Both flags go 1 → 0 on the trial workbook, confirmed read-only.
- **`same_offer_of`:** read from the "Same as #n" prefix. A Same-offer row is never a `same_price_revision`. A new switch, `same_offer_restatements` (kept or dropped), lets analysis choose. A bad pointer, or a price that differs from #n's, goes on the review list.
- **Inferred exits:** under v1.14.1 and v1.13.2, Inferred = Y on an exit means an inferred exit. **Departure:** the Note-wording classifier is kept for v1.14 workbooks only, because v1.14 did let Inferred mark a field. The contract marks calls 11 and 14 "v1.14 only".
- **Initiation:** derived by the D5 rule (an Activist row in round 0 wins; otherwise the first Target interest or Target sale decision, target-led, or Bidder interest or Bid, bidder-led). A new `deal.csv` column, `initiation_check`, compares it with Deal facts. The `process_initiator` switch is retired under v1.14.1.
- **Auction screen:** no Uncertain status under v1.14.1.
- **Retired under v1.14.1 only:** `not_admitted` and the eligible-but-unadmitted switch, and the merger-of-equals switch. The count-ranges switch still reads a qualifier.
- **Price basis:** `package_basis` uses the fixed E13 basis under v1.14.1. `stock_bounds` reads a range from a Part stock Note. `diff_workbooks.all_cash_for_stock` needed no change, since it already maps Part stock to No.
- **Other files:**
  - `compare_alex.py` got `--rules`.
  - `ANALYSIS_CONTRACT.md` (main) records every changed column, switch and call, a "Retired for v1.14.1" section, and a dated 0.2 entry.
  - `test_derive_analysis.py` runs v1.14 and v1.14.1 fixtures side by side, with 10 new tests.
- **Item 8** (recompute the Formality-reading table) waits for the retest.

### WP4. Cockpit (v114 tree)
- **Rules plumbing:** `Workspace.rules_for(version)` maps the version's instruction hash to rules. It feeds the live check (`data.Cockpit.check(..., rules)`, whose cache key includes the rules), the saved-revision check, `build_deal_payload`'s fatal-check fallback, `base_ledger_schema`, the rebase preview's `ledger_schema` and the editor's value lists (`choices`).
- **Worker:** the post-run check passes `--rules` from the frozen instruction hash, or the run's metadata hash, so the stored `ledger_schema` follows.
- **Revision guard:** `run_model.py` takes the rules from the `--instruction` hash. `revised_from_ledger_schema` records v1.14 or v1.14.1, and the message says "v1.14 or v1.14.1 workbook".
- **Rules label:** `runs.js`'s label shows whatever the server returns ("v1.14.1 rules"), with a test.
- **Stock % in the editor:** `_coerce` rejects a range unless the base's rules are v1.14, and points to Part stock.
- **`Records.jsx`:** the Count hint now reads "Blank only for a qualified figure (‘more than ten’); a cohort’s Count is the filing’s total minus the members recorded by name."
- **`Instructions.jsx`:** the placeholder is now "e.g. v2.0 draft".
- **Tests:**
  - `test_cockpit_workspace.test_rules_follow_the_versions_instruction`: a v1.14-hash run shows v1.14 rules and lists, a v1.14.1-hash run and an unknown one show v1.14.1, and the Stock % range error follows.
  - `test_cockpit_phase4.test_the_run_is_checked_under_the_rules_of_its_instruction`: the worker's post-run check is v1.14 or v1.14.1 by instruction.
  - The runner test gained a v1.14-hash revision case.
- **Publishing:** needs no code, as the spec says.

### WP5. Review migration (`migrate_review.py`, v114 tree)
- **Impact tags:** `IMPACT_TAGS_V1141` covers R1–R6, "v1.14.1 D1/D2/D3/D6" and the structural cuts (not invited → Dropped by target, Formality routes, Sort-date ladder, bidders' advisers to Notes, Contact vs interest, the Other material event list, Initiation from the first row, express incorporation removed). A tagged fact is "re-judge", never auto-accepted.
- **Additions:** an "E5 process test" tag; Initiation as a register fact; detection of Adviser rows that name a bidder.
- **Texts and options:** the bucket, action and header texts now say v1.14.1. `triage --rules` was added.
- **Tests:** three new.
- **Not done: regenerating `migration/*/register.json` and `triage-*`.** The inputs are the independent audit's files in `lesson/`, which this session may not read. The subagent stopped and changed no register. `migration/README.md` has a dated note. See the GATEs below.

### WP6. Runner, sweep and retest tooling
- **Instruction path:** `retest/RETEST_PLAN.md` gives the exact commands, all with `--instruction` pointing at the candidate, plus a hash check before launch and a metadata check after.
- **`effort_sweep.py`:**
  - `ledger_stats` adds `note_words_max`, `notes_over_40`, `questions_counted` (without the process Question) and `process_question`.
  - The per-arm summary adds `mean_note_words_max`, `max_note_words` and `mean_questions_counted`, and the printed table shows them.
  - The sweep's own post-run check passes the pinned instruction's rules.
  - One test was added.
- **`retest/retest_acceptance.py`:** new. It is an offline script built from V1141_SPEC §10 step 6, not from the trial's rubric: PASS, FAIL or REVIEW per item, with the rows to look at.

### WP7. Deploy package (prepared; the deploy is a GATE)
- **`release/deploy-tools-v1141.patch`:** SHA-256 `7256570979f1ce8c57e9ee04e531700dabd5758fd203278493357e333f9e15ba`, 62 files, `_dev/tools/` only, no `dist/`. It was checked three ways:
  - `git apply --check` passes against main (rerun at 19:27 UTC);
  - applied to a copy of main, it makes `_dev/tools/` identical to the v114 tree;
  - on that copy, 336 unit tests pass (1 skipped), plus 20 HTTP and 77 vitest.
- **Nothing lost from main:** a three-way comparison against the pre-Astra copies confirmed that no change made in main since the 25 September patch would be reverted. The only main-only README lines were ported into the v114 README first.
- **Old patch:** `deploy-tools.patch` is marked superseded, not deleted.
- **Gate-12 patches retargeted to v1.14.1:** `release-gate12.patch`, `d25-tools.patch` and `tools-readme-release.patch`, with `.pre-v1141` copies kept. Only added lines changed. `release-gate12.patch` passes `git apply --check` on a copy of main with the deploy patch applied.
- **`release/README.md` and `release/PROPOSED_DOC_LINES.md`:** retargeted (checker 1.8, v1.14.1 runs, the new patch name, the engine note). 55 replacements in the second file.
- **`DEPLOY_RUNBOOK.md`:** new. It gives the WP1-only deploy and the full deploy, with a build to `dist.new/`, the old assets copied across before the swap, the verification steps and a receipt.

### WP8. Docs and questionnaire (main tree)
- **Questionnaire:**
  - The builder `evidence/a2/build_docx.py` was edited for every WP8.1 item and for V1141 §10 step 8. The DOCX was rebuilt (`f201a70e…243a`, 11 pages), and so were the page renders.
  - The pre-change DOCX, builder and renders are in `evidence/a2/pre-v1141/`. All 61 excerpts were found on their cited pages.
  - The 3.3(a) numbers are marked "to be recomputed after the v1.14.1 retest".
  - Re-derived under the v1.14.1 triggers: **Kraton:** A (one round), still recommended; **Datalink:** A, four rounds, with no recommendation mark, because F9's five stand until Austin decides; **PetSmart:** 30 October is Enforced.
- **Other docs:**
  - `_dev/RESEARCH_QUESTIONS.md`: dated v1.14.1 notes on the listed items.
  - The Astra packet: status notes (AMENDMENT_SPEC superseded except P1; DECISION_BRIEF §§1–4, 6 and 7 resolved; a README note).
  - The root `README.md`: the Next step now points to v1.14.1.
  - `_dev/tools/README.md` (both trees): checker 1.8, the rules selector and the engine; the v114 copy is the post-deploy text.
  - The root `HANDOFF.md`, `_dev/HANDOFF.md` and `_dev/CHRONOLOGY.md`: dated sections on v1.14.1 and its hash, Q1–Q4, the engine change, what R1–R6 superseded, a built / deployed / GATE table, and the trial worktree's removal. Superseded statements are marked, not deleted.

### WP9. Retest and release (prepared; every step is a GATE)
- **`retest/RETEST_PLAN.md`:** five isolated Opus 5.5 medium runs, all at once, with no revision pass, on Mac-Gray, P&W, sTec, Synacor and Datalink. It gives the exact commands, the acceptance script and the results folder (`_dev/reviews/<date>-v1141-retest/`). It says to run after the WP7 deploy, or from the v114 tree if the retest comes first.
- **`retest/RELEASE_CHECKLIST.md`:** the cockpit draft (paste and check the hash), optionally a frozen v1.14 first, the release decision, the default switch, and `export_repo.py … --write` at release only.

## Tests

| Suite | v114 tree at start | v114 tree at end | Main copy after WP1 | Main copy + deploy patch |
|---|---|---|---|---|
| `unittest discover -s _dev/tools` | 294 pass | 336 pass | 201 pass | 336 pass (1 skipped) |
| `pytest …/test_http.py` | 20 pass | 20 pass | 14 pass | 20 pass |
| `vitest run` | 77 pass | 77 pass | 53 pass | 77 pass |
| `npm run build` | ok | ok | ok (to `wp1-main-dist/`) | not run (the deploy builds) |

- **Where the suites ran:** main's suites ran on a copy of main (without `ref/`, `lesson/`, `extraction/` and the cockpit state), so nothing ran against live paths. Each work package ended green.
- **Other acceptance checks (spec §6):**
  - The 15 trial workbooks check under `--rules v1.14` with the same issues as their stored `check.json`: **15 of 15 identical**, messages included (`checks/trial-recheck-v1.14.json`). Under v1.14.1, for information, they would fail on long Notes, field-level Inferred and Question counts, which shows why the selector matters (`checks/trial-recheck-v1.14.1.json`).
  - The five Examples as one v1.14.1 workbook: checker 1.8 gives **0 errors, 0 warnings** (`checks/examples/`).
  - `derive_analysis.py` on that workbook gives `same_offer_of` = 5 for Example 2 (row 14, with no `same_price_revision`), and no price observation for Example 5 (row 18) or Party G's priceless proposal (row 15).
  - The deploy patch passes `git apply --check` against main.
- **Dry run of the retest script:** run on the trial's Opus-medium workbooks, it flags exactly the disputed v1.14 behaviours. That checks the script only; it grades nothing.

## Where the spec was wrong or incomplete
1. **`release-gate12.patch` does not apply cleanly to main now.** It applies only after the deploy patch, as its own README says (it needs `data.catalog_deals`, `test_cockpit_catalog.py` and more). This is checked, and it is not a defect.
2. **WP5 regeneration needs `lesson/`,** which this task may not read. The tool is ready; the registers are unchanged.
3. **WP1's "rebuild `dist/` in each tree":** doing that in main would have changed the live page before the GATE, so main's build is staged (see WP1).
4. **WP2 item 19 severity:** a warning, not an error. Candidate issue 6 below explains why.

## What the candidate instruction got wrong or leaves open (reported, not fixed)

> **Status, 26 September, about 20:45 UTC.** Austin approved, and the candidate now carries, the proposed wording of issues **2, 4 (the second option: add the inferred-Round-opened sentence to E6), 5, 6, 7, 8, 9 and 10**. Issue 6 was placed under Due diligence **Incomplete** ("…confirmatory included, or that only documentation remains"), not under Complete as proposed, so that a documentation-only bid does not fall to None. **Issue 1 is decided:** Datalink follows the v1.14.1 text, four rounds; F9's five rounds are superseded for Datalink, and the same reasoning applies to Kraton and Meredith; the retest's Datalink run gave four rounds. **Issue 3 stays open:** no wording was proposed or applied. The retest opened Datalink's round 1 on 28 January, the first price negotiation. The four issues of spec §7 above were not changed by the edit. The retest found one more candidate for v1.14.2 (Count on a Merger announced row naming the winner; see the retest README).

The four known issues in spec §7 stand:
- price-only revisions lose the earlier terms;
- the required process Question fires on outcomes the defaults already decide;
- route 2 for a solicited revision inside an announced final round is undecided;
- Other-scope bid rows still need Formality and Conditions.

The work also found these:

1. **Datalink's round map changes.** With the "count once" sentence gone, E6's triggers give Datalink four rounds, not F9's five (July admission and August letter as one round). The retest's "maps unchanged" check will show this as REVIEW. **Austin must decide Datalink** before the questionnaire goes out. The same question decides Kraton and Meredith.
2. **Offer-less selection.** E6 does not say whether a selection with no request, followed by a first final letter, is one round or two, or on which date the round opens. Proposed: "A selection that asks for no offers opens no round; the round opens at the request that follows (E6(a) or (b))."
3. **Round 1 date when buyers came to the target.** "At the first NDA or price negotiation" gives Datalink 28 January or 4 February, not F9's 29 January.
4. **Inferred Round opened.** Part B and Part F name "an inferred Round opened" and "a round opened … by inference", but no rule says when a round is inferred, and the changelog lists the rule among the cuts. Proposed: delete both mentions, or add to E6 "Where the filing reports a stage's offers but not its opening, the Round opened row is Inferred = Y, dated at the first offer."
5. **Count on Round opened.** D1 column 20 exempts "process markers" from the blank-Count rule, while D1's opening calls rounds "markers" too. The checker keeps Round opened as a row about no bidder (spec WP2.15). Proposed: "…except Process terminated, Process restarted and Bidding group changed."
6. **Light with diligence Not stated.** E12's Light route "only documentation remains" can hold while Due diligence is Not stated, so the spec's "Light requires Complete or Incomplete" would be an error on a coding the text allows. I made it a warning. Proposed: add to E12 Due diligence, "Complete: … or that only documentation remains."
7. **Initiation can call a target-run sale bidder-led.** D5's list omits Round opened, so a filing with no board decision row ("the banker contacted 40 parties") is decided by the first Bid. Proposed: "…Target interest, Target sale decision or a Round opened row opened by the target's outreach, target-led; …"
8. **Same offer and price observations.** E10 says a row with no newly stated price "is not a new price observation", but a Same-offer row copies a price it does not restate. Analysis leaves this to the `same_offer_restatements` switch. Proposed, if it should be settled: "The copied price is not a new price observation."
9. **E13 "the Note says which"** (CVR value) is ambiguous: which amount, or on what basis? Proposed: "if several, the maximum, and the Note lists them."
10. **The process Question and cohort rows cannot be recognized from the text.** The checker needs a mechanical reading of both. Proposed, to make both checkable: "Begin the process Question 'Process:'", and in E3, "A cohort row's Who names the group ('12 financial NDA signers')."

## GATEs and open items for Austin

> **Status, 26 September, about 20:45 UTC.** Done: 2 (WP7 deploy, which made 1 unnecessary), 4 (Datalink: four rounds), 5 (the draft, with the edited text `8a93df3c…6c98`), 6 (retest, 3.3(a) recompute and questionnaire rebuild), 7 (published as v1.14.1 and made the default) and 12 (issues 2 and 4–10 applied; the new hash is in `RULES_BY_INSTRUCTION`). Still GATEs: 3 (migration registers, needs `lesson/`), 8 (repository export; `SEC_Deal_Ledger_Extraction_Instruction.md` is still v1.13.2), 9 (rebasing, gate 12), 10 (commits and pushes), 11 (sending the questionnaire), plus installing the unit-file changes (`TMPDIR`) and removing `dist.old` after acceptance.
1. **WP1 deploy** (`DEPLOY_RUNBOOK.md` A): restart both services and swap in `wp1-main-dist/`. It can ship alone.
2. **WP7 deploy** (runbook B): apply `deploy-tools-v1141.patch`, test, build, restart, verify and write a receipt. This replaces A if both are ordered. Deploy it before publishing v1.14.1 in the cockpit.
3. **Migration registers:** the regeneration needs someone allowed to read `lesson/`, or Austin's permission for an agent to. The commands are in `migration/README.md`. Use `--rules v1.14` for the two pilot triages.
4. **Datalink round map** (candidate issue 1), before the questionnaire goes to Alex.
5. **Cockpit draft "v1.14.1"**, with a hash check (`RELEASE_CHECKLIST.md` §1). Optionally, a frozen v1.14 first (§2).
6. **Retest** (`RETEST_PLAN.md`): five runs, then `retest_acceptance.py`, then the 3.3(a) recompute and the questionnaire rebuild.
7. **Release decision:** publish v1.14.1, then make it the default.
8. **`export_repo.py instruction v1.14.1 --write`**, at release only.
9. **Later decisions:** rebasing working copies, and gate 12 (moving the nine workbooks).
10. **Commits:** the live uncommitted work first (V114 gate 0), then this upgrade. Pushes also need Austin.
11. **The questionnaire to Alex.**
12. **Candidate wording:** issues 2–10 above, if Austin wants the text changed. Any change makes a new hash, which then needs a line in `RULES_BY_INSTRUCTION`.

## Where things are
- **This folder:** `PIPELINE_UPGRADE_REPORT.md`, `DEPLOY_RUNBOOK.md`, `wp1-main-dist/`, `checks/` (the trial recheck, the Examples fixture) and `retest/` (the plan, the checklist, the acceptance script).
- **Release:** `../2026-09-24-bid-terms-taxonomy/release/` (the deploy patch, the retargeted gate-12 patches and docs).
- **Code:** `~/work/Projects/sec-extraction-v114/_dev/tools/`, uncommitted.
  - Changed: `check_lean.py`, `derive_analysis.py`, `compare_alex.py`, `migrate_review.py`, `effort_sweep.py`, `sandbox/run_model.py`, `README.md`.
  - Cockpit: `data.py`, `runs.py`, `worker.py`, `workspace.py`, and in `frontend/src`: `runs.js`, `Records.jsx`, `Instructions.jsx`.
  - Their tests, and `dist/`.
- **Main-tree code (WP1 only):** `cockpit/runs.py`, `frontend/src/runs.js` and `runs.test.js`, `sandbox/run_model.py`, `test_cockpit_phase4.py`, `test_run_model.py`.
