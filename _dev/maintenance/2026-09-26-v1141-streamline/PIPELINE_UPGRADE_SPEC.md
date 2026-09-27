# Pipeline upgrade for v1.14.1: implementation spec

**Status: ready for an implementing agent. Austin approved Q1–Q4 (§3) on 26 September. Each step marked GATE still needs his separate go.** This file is written for a fresh agent with no memory of the conversation that produced it. It is self-contained; read the files in §1 before starting.

> **Status, 26 September, about 20:45 UTC: implemented and deployed.** WP1–WP9 are done or executed: see [`PIPELINE_UPGRADE_REPORT.md`](PIPELINE_UPGRADE_REPORT.md) and [`deployment-v1141.json`](deployment-v1141.json) (deploy at 19:41 UTC). The candidate text was edited with Austin's approval after this spec (hash now `8a93df3c…6c98`); Austin published it in the cockpit as v1.14.1 at 20:18 UTC (id `08caed447f7d`, SHA-256 `8a93df3cc6d989386958e9cb2d74ab34ebc0f07d281e8cc398605a388e066c98`: the reviewed `8bdb7c20…8a79` plus candidate issues 2 and 4–10 of `PIPELINE_UPGRADE_REPORT.md`) and made it the cockpit default. The retest is done ([results](../../reviews/2026-09-26-v1141-retest/README.md)). Still GATEs for Austin: exporting the repository instruction (still v1.13.2), commits and pushes, sending the questionnaire, regenerating the migration registers (needs `lesson/`), rebasing working copies and gate 12, installing the unit-file changes (`TMPDIR`), and removing `dist.old`.

26 September 2026. It consolidates:
- `V1141_SPEC.md` §7 (checker and analysis), §9 (engine) and §10 (plan);
- `CHANGELOG_v1.14.1_candidate.md`;
- three read-only scans of the pipeline made after the candidate was drafted. They covered the checker and analysis, the cockpit and runner, and the docs, questionnaire and ancillary tools.

Line numbers are from those scans and may have drifted. Search for the quoted code rather than trusting the number.

## 0. Goal and boundaries

Make every part of the pipeline agree with the v1.14.1 instruction, switch the default extractor back to Opus 5.5 at medium effort, and prepare (not perform) the retest and release.

**Authorized by this spec:** code, test and doc changes in the places §2 names, and offline tests.

**Not authorized, each needs Austin's explicit go (GATE):**
- restarting `ledger-cockpit` or `ledger-worker`, or any other change to live services;
- any extraction or model run, including the retest;
- publishing an instruction version in the cockpit or changing the cockpit default;
- rebasing working copies, or moving the nine workbooks ("gate 12");
- commits and pushes;
- sending anything to Alex;
- editing the instruction candidate text. Its SHA-256 is fixed at `8bdb7c20…8a79`. If you find a defect in it, report it; do not fix it.

Follow the project's `AGENTS.md`. The folders `ref/`, `lesson/` and the workbooks in `extraction/` are off limits to extraction agents. You are not one, but you do not need them. Never restore an old instruction into the checkout.

## 1. Read first

1. `_dev/maintenance/2026-09-26-v1141-streamline/SEC_Deal_Ledger_Extraction_Instruction_v1.14.1_candidate.md`: the rules everything must match.
2. `CHANGELOG_v1.14.1_candidate.md` and `v1.14.1_candidate.diff`, in the same folder: what changed from v1.14.
3. `V1141_SPEC.md`, same folder: §3 (settled decisions R1–R6, H1–H4), §7, §9, §10.
4. `_dev/HANDOFF.md` and the root `HANDOFF.md`: the project state.
5. `_dev/maintenance/2026-09-24-bid-terms-taxonomy/V114_SPEC.md` §12–§13 (deploy and release) and `release/README.md`: how the v1.14 build was meant to ship.

## 2. Where to work

| Tree | Use |
|---|---|
| `~/work/Projects/sec-extraction-v114` (detached worktree at `679d4fc`, all work uncommitted) | **All code changes.** It holds the only copy of the built v1.14 code: checker 1.7, `derive_analysis.py`, `migrate_review.py`, `compare_alex.py`, `cockpit/provenance.py`, the new frontend modules and the service units. Do not delete or reset it. |
| `~/work/Projects/sec-extraction` (main, branch `extraction-v2`) | Live services run its code. Change code here only for the §9 engine revert (WP1). Docs and maintenance packets live here. Preserve its existing uncommitted work and the ignored cockpit state (`_dev/cockpit/state/`). |

The 15-run v1.14 trial packet is at `_dev/reviews/2026-09-26-v114-15-run-trial/` in main. It is evidence: read it, never edit it.

## 3. Decisions (approved by Austin, 26 September)

Austin approved the recommended option for each. Implement them as written, and list them in the final report.

| # | Decision | Approved |
|---|---|---|
| Q1 | How the tools tell v1.14.1 workbooks from v1.14 ones. The headers are identical (29 columns, "Stock %"). | Add a rules selector (`--rules v1.14` or `v1.14.1`) to `check_lean.py` and `derive_analysis.py`. The cockpit passes it from the instruction version's SHA-256 through a small map in one module (`8bdb7c20…` → v1.14.1; `c2d47a47…` → v1.14). A 29-column workbook with no known instruction defaults to **v1.14.1**. The 15 trial workbooks keep v1.14 by explicit selection. |
| Q2 | Does the process Question count toward the five-Question cap? | No. The candidate's Part F says it does not count, which matches V1141_SPEC §7 and §10. |
| Q3 | V1141_SPEC D1–D6 | As the candidate implements them. |
| Q4 | R2 ("forecasts count") changes a questionnaire example: the Mac-Gray committee's 19 September remark that Party B "would likely be financing … with third party debt" makes Party B Contingent and Heavy (H1). | Accept it as a consequence of R2 and note it in the questionnaire reconciliation (WP8). |

## 4. Work packages

The order in §5 matters. Each package ends with its tests passing.

### WP1. Engine back to Opus 5.5 medium (V1141_SPEC §9)

Revert the Astra-default delta recorded in `_dev/maintenance/2026-09-26-astra-default-pro-verification/astra-default.patch`, in **both trees**:

- **`_dev/tools/cockpit/runs.py`:** `DEFAULT_ENGINE = "opus55"`. `DEFAULT_EFFORT` stays medium for opus55 and high for astra6.
- **`_dev/tools/cockpit/worker.py`:** a job with no engine selection runs on Opus.
- **`_dev/tools/cockpit/frontend/src/runs.js`:**
  - `DEFAULT_ENGINE` becomes Opus 5.5 · medium, and `DEFAULT_EFFORT` becomes medium.
  - Preselect Opus when the Claude account is connected; otherwise fall back to the first connected engine.
  - An explicit choice is always kept.
- **`_dev/tools/sandbox/run_model.py`:**
  - `prepare` defaults to provider opus, model `claude-opus-5-5`, effort medium.
  - Astra keeps `MODEL_DEFAULT_EFFORT = high` when chosen explicitly.
  - Fix the help text that names Astra as the default (around lines 832–839).
- **Tests:** in `runs.test.js`, `test_cockpit_runs.py`, `test_cockpit_deals.py`, `test_cockpit_phase4.py` and `test_run_model.py`, flip the default assertions. Keep the provenance tests: historical jobs are never relabelled.
- **Frontend build:** rebuild `dist/` in each tree. Keep the old asset files in main so open tabs keep working.
- **Docs:** update the engine line in `AGENTS.md`, the root `README.md`, `_dev/HANDOFF.md`, `_dev/tools/README.md`, `_dev/cockpit/README.md` and `_dev/CHRONOLOGY.md`.
- **GATE, live deploy in main.** The checks below are the deploy run's procedure, taken from V1141_SPEC §9:
  1. No jobs are active.
  2. The focused tests pass and the build is done.
  3. Restart both services.
  4. Confirm the extraction dialog shows "Opus 5.5 · medium", without starting a run.
  5. Write a receipt in this folder.

  WP1 can ship on its own before everything else.

### WP2. Checker 1.8 (`_dev/tools/check_lean.py` in the v114 tree)

Bump `CHECKER_VERSION` to "1.8" and update the module docstring and revision text. Add a `SCHEMA_V1141` constant, or an equivalent rules flag, per Q1. Keep the v1.14 rules reachable, so the trial workbooks still check as they did.

Changes under the v1.14.1 rules. Items 1–7 come from V1141_SPEC §7; items 8–22 are new from the scans.

1. A Note over 40 words is an **error**.
2. Inferred = Y is allowed only on exit, Round opened and Process restarted rows.
3. Formality = Unclear is an error except on cohort rows. A cohort row is one whose Count is above 1, or whose Who names a group.
4. Antitrust = Y requires Regulatory = Concern.
5. Stock % must be a number from 0 to 100, Part stock, Not stated or Varies. A range such as "40-60" is an **error**. The candidate's E13 says a stated range is Part stock, with the range in the Note.
6. Warn at more than five Questions, not counting the process Question. See item 12 for how to recognise it.
7. Compare the Rounds Due dates text by prefix, which fixes "none stated (…)".
8. CVR/earnout and Antitrust take Y or blank only. Remove `Varies` from their accepted values (around lines 232 and 678–681) and from `choice_lists` (around lines 472–483).
9. Initiation takes target-led, bidder-led or activist-influenced only. Remove "mixed" and "unclear" (around lines 155–158, 273–279 and 1724), including from the field label text.
10. Auction screen entries start with Met or Not met. Remove "Uncertain" and "count unknown" (around lines 1747–1762).
11. Delete the warnings for the removed mandatory Questions: the deadline-outcome Question for every round, and the process-map Question on every deal (around lines 1658–1673). The one remaining requirement is a process Question when the deal has more than one process. Triggers (d) and inferred rounds cannot be detected mechanically, so don't try.
12. **Recognising the process Question.** Treat a Question as the process Question when its text or Rows affected names a Process terminated or Process restarted row, or begins "Process:". Pick one rule, document it in the checker's docstring, and add a test.
13. Question length: each entry must be at most 60 words, replacing the 90-word total around lines 1625–1629.
14. The `ledger.inference_note` error (around lines 1076–1085) becomes a warning. It applies only to Process restarted rows and cohort Did not submit rows, which the candidate says carry Note arithmetic. Fix the message, which still says "or naming the inferred field".
15. Count is required, and positive, on Process terminated, Process restarted and Bidding group changed rows, as well as on the rows that already need it. Keep Round opened as a no-bidder row. A marker that closes zero bidders leaves Count blank (document this).
16. Round 0: a row with Round 0 after its process's round-1 Round opened row is an error.
17. Note prefixes:
    - A Note that starts "Same as #n" must point to an earlier bid row with the same Who.
    - A Heavy row's Note begins "H1:", "H2:" or "H3:", after any "Same as #n. ".
    - The `conditions.level_unsupported` warning (around lines 728–735) becomes this prefix check.
18. Bid reaffirmed rows must be Formal and carry "Same as #n".
19. Conditions = Light requires Due diligence Complete or Incomplete. The second Light route was removed.
20. The "Count: 11–14" range pattern (around lines 944–950): under v1.14.1, a Count Note may state a qualifier ("Count: more than ten") but not a range the model made up. Accept a qualifier; warn on a numeric range.
21. Fix stale references: "F.4" (around line 696) and "(B, F.3)" (around line 1046). The current Part F has three numbered delivery conditions and no F.3 or F.4 audit checks.
22. `test_check_lean.py`:
    - Replace the fixture bid that is Heavy with Due diligence Not begun and no trigger (around lines 76–90 and 195–200).
    - Remove the Q1 that exists only to silence the process-map warning (around lines 151–160).
    - Update the Varies tests (around lines 549 and 761), the Initiation test (around line 438), the Uncertain test (around line 340) and the Stock % range tests (around lines 569–571 and 735).
    - Add a test for each new rule, under both rule sets.

The main tree's `check_lean.py` (1.6) has an older v1.14-draft branch with the same problems. **Do not edit it.** It is replaced when the v114 tree is deployed (WP7). Do not publish v1.14.1 in the live cockpit before that deploy.

### WP3. Analysis (`derive_analysis.py` and `ANALYSIS_CONTRACT.md`)

`derive_analysis.py` is in the v114 tree. `ANALYSIS_CONTRACT.md` is at `_dev/maintenance/2026-09-24-bid-terms-taxonomy/ANALYSIS_CONTRACT.md` in main. Bump `TOOL_VERSION` (0.2) and `CONTRACT_VERSION` (0.1), and update the tool docstring and the contract header.

1. **P1** from `_dev/maintenance/2026-09-26-astra-default-pro-verification/AMENDMENT_SPEC.md` §5, as written:
   - Add `upfront_price_kind`.
   - A bid row with a blank price is not a price observation (H4).
   - Fix Mac-Gray A #61/#62: their `price_obs__same_price_as_new` and `price_obs__same_price_as_terms` must not be 1.
2. **`same_offer_of`**, from the "Same as #n" Note prefix. Reconcile it with `same_price_revision` (around line 655; contract lines 126–127): a Same-offer row copies its price and must not also count as a new same-price revision.
3. **Inferred exits:**
   - On an exit row, Inferred = Y means an inferred exit. Remove the Note-wording classifier that sorts inferred exits into exit, field or unresolved (around lines 88–100, 327, 345–363 and 615–622).
   - Remove field-level Inferred from the contract (lines 170–171 and 209–214; items 11 and 14).
   - Without this change, nearly every v1.14.1 inferred exit becomes "unresolved" under the censoring switch.
4. **Initiation** (around lines 107 and 136): the v1.14.1 rule is mechanical. An Activist row before round 1 wins; otherwise the earliest Target interest or Target sale decision row (target-led) or Bidder interest or Bid row (bidder-led) decides, all in process 1. Implement it that way, and turn the `process_initiator` switch into a consistency check against Deal facts.
5. **Auction screen** (around lines 434–450; contract lines 35–39): remove the Uncertain handling. `estimation_sample` no longer goes missing on Uncertain.
6. **Features that depend on removed content:**
   - The eligible-but-unadmitted switch and the `not_admitted` column (around lines 130, 157 and 752; contract lines 88–90 and 155) rely on the Rounds "Who was in" lists, which v1.14.1 deleted. Under v1.14.1 a bidder that is not invited gets an exit row (R5). Retire the switch for v1.14.1 workbooks, and keep it for v1.14 ones.
   - The merger-of-equals switch (around lines 139, 773 and 807; contract line 158) relies on the alternative-map Question, which v1.14.1 deleted. Retire it for v1.14.1.
   - The count-ranges switch (around line 241): v1.14.1 creates no ranges. Keep reading a qualifier.
7. **Price basis:**
   - `package_basis` (around lines 82 and 314; contract line 119) cites the old E13 subtraction rules. v1.14.1 E13 instead leaves the price blank when only a package value is stated, and fills CVR/earnout value with the maximum, the Note saying which.
   - `stock_bounds` (around lines 255–261; contract lines 121–122) and `diff_workbooks.all_cash_for_stock` should read Part stock with the range in the Note.
8. After the retest (not now): recompute the Formality-reading agreement table (questionnaire 3.3(a)).

Update `test_derive_analysis.py` to match, with v1.14 and v1.14.1 fixtures side by side.

### WP4. Cockpit (v114 tree)

1. **Rules selection plumbing (Q1).** The instruction's SHA-256, or the version it resolves to, reaches:
   - the live check (`workspace.py`, around line 347);
   - the post-run check (`worker.py`, around line 312), and the stored `ledger_schema`;
   - the editor's value lists (`workspace.py`, around line 377);
   - the rules label (`runs.js`, around lines 189–192), which shows "v1.14.1 rules" for v1.14.1 runs;
   - the revision guard (`run_model.py`, around line 284).
2. **Value lists:** the editor's lists come from the checker's `choice_lists` (WP2 item 8). Deal facts are edited through their Value column, so the Initiation fix lives in the checker alone.
3. **Stock % storage:** `workspace.py` (around lines 683–684) stores a range as text. Under v1.14.1, reject a range and point to Part stock.
4. **`Records.jsx` Count hint** (around line 138; line 131 in main): it says to leave Count blank "when the cohort size is uncertain". Change it to: "Blank only for a qualified figure ('more than ten'); a cohort's Count is the filing's total minus the members recorded by name."
5. **`Instructions.jsx`** (around line 312): the placeholder "v1.14" becomes a neutral example.
6. **Tests:** frontend (vitest), `test_cockpit_*.py`, and the HTTP acceptance test. Add one test: a v1.14.1-hash run is checked under the v1.14.1 rules, and a v1.14-hash run under the v1.14 rules.

Publishing needs no code. `instructions.py` is generic, and nothing pins a v1.14 hash.

### WP5. Review migration (`migrate_review.py`, v114 tree)

`_impact` (around lines 355–397) marks a reviewed fact "unchanged", and so auto-accepts it when a new run agrees, unless a v1.14 decision (D1–D27) touches it. Under v1.14.1 that would accept changed codings unchecked.

- **Add impact tags for:** R1–R6; D1–D6 of V1141_SPEC; and the structural cuts, which are:
  - not-invited bidders are Dropped by target;
  - the narrower Formality routes;
  - the new Sort-date ladder;
  - bidders' advisers move to Notes;
  - Contact versus interest around round 1;
  - the closed list for Other material event;
  - Initiation from the first row;
  - express incorporation removed (lines 381 and 387 still tag it).
- **Text:** update the bucket and action texts ("v1.14", around lines 103–104).
- **Regenerate** every `_dev/maintenance/2026-09-24-bid-terms-taxonomy/migration/*/register.json` and `triage-*` file, and update `migration/README.md` (around line 22).
- **Tests:** `test_migrate_review.py`.

### WP6. Runner, sweep and retest tooling

1. **Instruction path:** `run_model.py prepare` falls back to the repository's v1.13.2 when no `--instruction` is given (around line 298). The retest must pass the v1.14.1 candidate path explicitly. Write the exact retest commands into the retest plan (WP9) so this cannot be missed.
2. **`effort_sweep.py`** (around lines 327–331):
   - Report the maximum Note length as well as the mean.
   - Report the Question count without the process Question (Q2).
3. **Retest grading:** write a small offline script, or a checklist, from V1141_SPEC §10 step 6's acceptance list. Do **not** reuse the trial's rubric:
   - `administration/GRADING_KICKOFF_prior_to_pro_dispatch.md` (line 30) rewards "dates and bounds";
   - `grading/README.md` (line 22) asks for non-submitters "with a bound";
   - `grading/mechanical_check.py` has no Note cap.

   All three would score v1.14.1 behaviour as wrong.

### WP7. Deploy package

- **Do not use `deploy-tools.patch`.** The 25 September `release/deploy-tools.patch` no longer applies to either tree: `git apply --check` fails on `runs.js`, `runs.test.js`, `run_model.py` and `test_cockpit_phase4.py`, because the Astra-default change touched the same lines. After WP1–WP6, regenerate a deploy patch (or file list) from the v114 tree against main, and dry-run it with `git apply --check`.
- **`release-gate12.patch`** still applies cleanly. Retarget its comments from "v1.14" to "v1.14.1".
- **Retarget the release docs to v1.14.1:** `release/README.md` and `release/PROPOSED_DOC_LINES.md` (line 12 and lines 125–215), where "checker 1.7" becomes "checker 1.8" and "export the v1.14 runs" becomes "export the v1.14.1 runs".
- **GATE, deploy.** Follow V114_SPEC §12's procedure, updated:
  1. No active jobs.
  2. Take a backup.
  3. Apply the regenerated patch.
  4. Run the tests and the build.
  5. Restart both services, keeping the old assets.
  6. Verify the extraction dialog and one read-only workbook view.
  7. Write a receipt.

### WP8. Docs and the questionnaire (main tree)

1. **The questionnaire.** `Questions_for_Alex_2026-09-25.docx` is built by `_dev/maintenance/2026-09-24-bid-terms-taxonomy/evidence/a2/build_docx.py`, so edit the builder and rebuild; the page PNG renders come from `render.py`. Beyond V1141_SPEC §10 step 8 (3.2, 3.3 and 3.4), these items change. Line numbers are in `build_docx.py`:
   - **2a "Carried terms" (around line 540):** express incorporation is deleted. Rewrite it around Same offer (R1) and mark it Changed.
   - **2a (around line 534):** H2 becomes "a period tied to diligence alone" (R4).
   - **2b-2 (around line 552) and 2b-4 (around line 558):** both still require Questions that E1 deleted. A switch to a partial offer is now "Withdrew, continued on a partial basis".
   - **2b-3 (around line 555) and 3.1 (around lines 662 and 670):** the rounds rules changed:
     - "after a suspension" is now E6(d), a pause of 30 days or more or an ended exclusivity period;
     - the "count once" sentence is gone;
     - E6(b) opens a round at the first final request even when the bidders are unchanged.

     Re-derive the Kraton and Datalink A/B options and the "recommended" marks.
   - **2b-5 (around line 561):** "refers back to earlier Formal terms" is gone. sTec WDC's 10 June bid is now Informal, which matches Alex's coding, so the Changed note flips.
   - **2b-6 (around line 566) and the 3.3(a) commentary (around line 716):** Party B becomes H1 under R2 (Q4).
   - **2b-8 (around line 571):** the deadline ladder now has five values. Recheck the PetSmart example.
   - **3.2 (around line 697):** v1.14.1 forbids ledger ranges, so the item becomes an FYI. Keep only the question about how counts are used in estimation.
   - **3.4 Penford Party A (around line 736):** now a valuation statement (Other material event) with no Question.
   - **3.3(b) and 3.4 Company H:** remove as settled, with notes to Alex (V1141_SPEC §10 step 8).
   - **Title (around lines 626 and 636):** v1.14 becomes v1.14.1.
   - Keep the numbering and the crosswalk.

   Nothing goes to Alex without Austin (GATE).
2. **`_dev/RESEARCH_QUESTIONS.md`:**
   - line 10 (Q7 Company H) is settled by H1, and line 18 (Mac-Gray R01) by H4;
   - lines 19 and 27: trigger (d), and the 90-day test;
   - lines 29–30: the "refers back" route and express incorporation are gone, and WDC's 10 June bid is Informal;
   - line 31: 13 October is a valuation statement;
   - line 37: the five-value deadline ladder.
3. **Astra packet** (`_dev/maintenance/2026-09-26-astra-default-pro-verification/`):
   - Mark `AMENDMENT_SPEC.md` superseded by V1141_SPEC §7, except P1, which WP3 implements.
   - Mark `DECISION_BRIEF_2026-09-26.md` §§1–4, §6 (the Astra retest) and §7 (settled by R6) resolved.
   - Add the same note to the packet README's "Read first" list.
4. **Main-tree READMEs:**
   - root `README.md` (line 18): the "Next step" line names v1.14. Point it to v1.14.1.
   - `_dev/tools/README.md`: line 19 describes the checker's checks (checker 1.8), and lines 111–112 give the example `export_repo.py instruction v1.14.1`. Make the same change in the v114 tree's copy.
5. **Handoffs and chronology:** the root `HANDOFF.md`, `_dev/HANDOFF.md` and `_dev/CHRONOLOGY.md` record:
   - v1.14.1 and its hash;
   - the engine change;
   - what R1–R6 superseded;
   - the removal of the trial worktree, whose packet now lives in `_dev/reviews/2026-09-26-v114-15-run-trial/`.

### WP9. Retest and release preparation (V1141_SPEC §10 steps 5–9)

Prepare, do not run:

- **Retest plan:** five isolated runs of Opus 5.5 medium, one per sandbox, all launched at once with no revision pass, on Mac-Gray, P&W, sTec, Synacor and Datalink. The plan gives the exact `run_model.py` commands with `--instruction` pointing at the candidate (WP6.1), the acceptance checklist (WP6.3), and where results go (`_dev/reviews/<date>-v1141-retest/`). **GATE: Austin orders the runs.**
- **Release checklist:**
  1. Publish in the cockpit as a draft named "v1.14.1": start from v1.13.2, paste the candidate, save, and check the stored hash equals `8bdb7c20…8a79` (LF line endings, trailing newline).
  2. Optionally publish the v1.14 candidate first as a frozen "v1.14", to give the trial runs provenance.
  3. Make v1.14.1 the default only after Austin accepts the retest.

  **GATE.** Do not run `export_repo.py instruction` until release: it overwrites the frozen repository instruction.

## 5. Sequence

1. **WP1**, the engine revert, in both trees. Code and tests now; the live deploy only at GATE.
2. **WP2 → WP3 → WP4 → WP5 → WP6** in the v114 tree. WP2 first, because WP3 and WP4 consume its rules selector and value lists. Run the full offline test suite after each package.
3. **WP8** docs, in parallel with step 2. The questionnaire rebuild comes last, after the retest results where §10 asks for them (3.3(a)).
4. **WP7:** build the deploy package, dry-run it, then GATE.
5. **WP9:** publish as a draft, run the retest, and have Austin decide on the release. Each step is a GATE.

Deploying the v1.14 code without the v1.14.1 changes would open a window where v1.14.1 runs are checked and edited under v1.14 rules. No released v1.14 needs its own deploy, so deploy once, after step 2.

## 6. Tests and acceptance

Offline, in the v114 tree:

```bash
python3 -m unittest discover -s _dev/tools -p 'test_*.py'
```

```bash
python3 -m pytest -q -p no:cacheprovider _dev/tools/cockpit/acceptance/test_http.py
```

```bash
cd _dev/tools/cockpit/frontend && npx vitest run && npm run build
```

Acceptance for this upgrade, before any GATE:

- all three suites pass, with new tests for each WP2 rule under both rule sets;
- the 15 trial workbooks check under `--rules v1.14` with the same results as before (compare with their stored `check.json`);
- the five synthetic Examples in the candidate, entered as a tiny v1.14.1 fixture workbook, pass the checker with no errors;
- `derive_analysis.py` on the fixture yields `same_offer_of` for Example 2, and no price observation for Example 5;
- the regenerated deploy patch passes `git apply --check` against main;
- a final report in this folder (`PIPELINE_UPGRADE_REPORT.md`) lists every change, the Q1–Q4 choices, test counts and the open GATEs.

## 7. Known issues in the candidate to report, not fix

These were left open in `CHANGELOG_v1.14.1_candidate.md`, for Austin:

- **Price-only revisions lose the earlier terms:** the condition columns become Not stated, and Conditions usually Unclear.
- **The required process Question** fires on outcomes the defaults already decide.
- **Route 2 for a solicited revision inside an announced final round** is not decided.
- **Other-scope bid rows** still need Formality and Conditions under F's delivery check 2.

If the checker or analysis work exposes another contradiction in the candidate, record it in the final report with a proposed wording; do not change the candidate.
