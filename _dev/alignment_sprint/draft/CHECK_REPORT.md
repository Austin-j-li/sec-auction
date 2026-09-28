# Version 1 check report

27 September 2026; updated 28 September 2026 after the re-review fixes. These checks concern the build and a hand-applied reading of its rules. No extraction model was run. A passing mechanical check does not establish source accuracy or research acceptance.

## Instruction checks

Re-run on 28 September 2026 after the re-review fixes (rulings 6 and 7 of 28 September and VERSION1_REREVIEW §1–3), by script and by reading. The Finality paragraph moved ahead of E6's triggers and E14 gained one paragraph, so the draft is two lines longer and CHANGE_MAP's line references were regenerated.

- **File.** 397 lines, 54,717 bytes. Draft SHA-256: `bf14a469a5f5a9a1317fdede7295cd476f2a6230d095a2e5f74863f6001e1c39` (fix pass: `5264450c019ba4f6a55c419fd229076994bc503aa4b323afd232ac0dd5efbf3a`; first build: `01110a1af35a0a3a4afaf0a2d2e77b67ce5f4cccf573356679cecef346825ee3`). 9,038 words, 177 more than at `8cc64cc`; E14's closing events and the paragraph after them grew from 333 to 409 words, mostly the two definitions ruling 6 requires.
- **Output contract.** 29 ledger columns numbered 1–29, the four-sheet sentence, 10 Rounds columns and 30 event labels, the same set as the checker's `EVENTS`. Every value in the checker's type, formality, conditions, stock, due-diligence, financing, regulatory, exclusivity, exit-reason, finality, initiation and deadline-outcome lists appears in the draft. The value “Extended (late bid accepted)” is unchanged.
- **Rule references.** All 22 identifiers (D1–D5, E1–E14, H1–H3) are defined and no other is cited. Part references resolve to headings A–F; triggers (a)–(d) are defined and every trigger reference resolves; E14's “event 1” and “event 3” name its numbered closing events.
- **Change map coverage.** Every one of the 41 R/F/P/O themes, Evening 1–7, the seven 28 September rulings and the Stage-questions and Q8 records has a forward row, and every re-review item has an entry. Against the root instruction, 105 nonblank draft lines are added or replaced; the reverse table covers all 101 substantive ones (the other four are `<example>` tags). All 337 linked and 43 plain-text line references in CHANGE_MAP resolve to a nonblank line (114 distinct lines), every link label matches its anchor, and each reference was checked against the line it names. At `8cc64cc` the map had 247 links to 101 lines, not 241.
- **Removed or collapsed text.** The exception inside closing event 3 is now the one E14 paragraph at L336; the duplicates listed in VERSION1_REREVIEW §3 have one home each (CHANGE_MAP, “Re-review fixes”). Searches for “takes its late bid”, “entertains”, “fresh final-round”, “touches” and “as defined below” find nothing; “considers” is the only verb for late bids and re-entry, and “accepted” survives only in the value name “Extended (late bid accepted)”.
- **Fixed anchors, clause level.** Kraton: R1 May 24; R3 July 20 is carried out by the August 11 letter; Party J Did not submit June 29, Re-entered by July 19, Dropped by target July 20. Mac-Gray: the August 27 letter carries out round 2. Penford R1 August 28, 2014, and Party A one spell to Not selected at signing October 14 (ruling 7), as the §7 anchor has it. Providence R1 by the “week of March 28” outreach. PetSmart R1 October 3. sTec: May 16 Not final (the filing calls the requested proposals non-binding), May 29 final; Company H still Dropped by target by May 16. Synacor process 3: October 27 (d), December 30 continues it, January 6, 2021 opens round 4 by (c). Datalink: August 16 (a) and October 1 (d). The filing-level application is ROUND_MAP's.
- **Names and wording.** No deal, party, acquirer, adviser, activist or researcher name from the nine filings or the project (“Parent” appears only in synthetic Example 5). No “v0”, “Version 0”, “no longer” or “instead of”; “now” appears only in the quoted withdrawal “for now”, and “changed” only in event labels and descriptions of events. No capitals for emphasis (only acronyms and the date format MM/DD/YYYY), no thinking-steering lines, and no request for reasoning. The injection defense is line 1. Seven example blocks are balanced, all with synthetic names.
- **Whitespace.** No trailing spaces, tabs, carriage returns or double spaces; final newline present; `git diff --check` is clean.

ROUND_MAP gives a source-backed entry for every fixed section-7 process/round anchor, every derive cell and every retest anchor, and every deadline outcome now follows from E9 and E14's tests without a reading choice. Its remaining open questions are filing readings. Two results are listed for Austin because a ruling's effect list or Alex's workbook says otherwise: the sTec May 3 outcome (Enforced, since D bid on April 23) and Providence D and E, which ruling 7 as generalized keeps live through round 3 (WORKBOOK_CHECK W49). The quotations in ROUND_MAP and WORKBOOK_CHECK were re-checked by script against the filings' text. WORKBOOK_CHECK reports disagreements separately and changes no rule or workbook.

## Hand-made workbook and independent tool review

The synthetic workbook from `test_check_lean.build_version_1_smoke_fixture` was run through `LeanChecker` again on 28 September after the re-review tool fixes. It returned **0 errors, 0 warnings, 0 information items** under checker **Version 1**. This one workbook includes mixed initiation, Q/R links, a signing Count of 1, a silent Formal bid with Conditions None, and a bid with required exclusivity and Conditions Light.

Two negative mutations were checked again: signing Count 2 produced the error `ledger.count_signing` (the check now allows only blank or 1, with warnings for a blank beside a whole-company bid or a 1 beside only Other-scope bids); required exclusivity with Conditions None produced `conditions.none_support`. Restoring the cells restored the clean verdict.

A fresh Astra reviewer independently reproduced and retested corrections for signing participation/scope, round-opening counts with intervening same-day entries and multiple openings, explicit H triggers, required exclusivity, and review-queue currency/type/price-basis coverage. Q/R sequences, caps, existing-row links, omitted-source-event R items and F2 restatement markers also passed the bounded review. No remaining actionable issue was found in that review; it did not substitute for the complete test suite or filing review.

## Automated suites

Re-run on 28 September 2026 after the re-review fixes:

| Check | Result |
|---|---|
| Full Python suite: `PYTHONUSERBASE=~/work/.local python3 -m pytest _dev/tools -q -p no:cacheprovider`, with TMPDIR in scratch | **377 passed, 284 subtests passed**, 102 seconds; includes the HTTP acceptance tests (25 passed, one new). |
| Frontend: `npx vitest run` in `cockpit/frontend` | **79 passed in 8 files**. The frontend source did not change, so `dist/` was not rebuilt. |
| Headless browser core suite, `test_browser.mjs` | **63 checks passed**. The trace suite, which uses signed Access tokens, passed 14 of 14 after the `access.py` change. |
| Hand-made Version 1 workbook | Clean; both negative mutations produce their errors (above). |

The deals, instructions, runs, resize and responsive browser suites were not re-run in this pass; they passed at the 28 September fix pass, and no frontend or deal/run code changed since. New tool tests were confirmed to fail on the code at `8cc64cc` (signing Count cases, the bilateral round-1 initiation cases, the late-bid warning, the count-note qualifiers and number words, and the deal-level currency item).

The 27 September results, for the record: 358 Python tests and 229 subtests, 77 vitest tests, 138 browser checks across five suites, the resize and responsive suites and a 9-of-9 pending catalog verification. The first complete Python run then had one timestamp-sensitive export test failure, fixed by comparing archive members after normalizing only the generated modified time.

## Copied-live-state rehearsal (27 September)

The live WAL database was opened with `mode=ro` and copied using SQLite's online backup API, then its filings directory was copied. The snapshot passed `PRAGMA integrity_check`. The fresh-state script retained **3 provider-account records for 2 users, 4 added-deal rows and 4 verified filings**. The retained table rows matched the snapshot exactly. Before app initialization, only accounts and added_deals existed; no old instructions/default, work, comments, activity or jobs carried over. Provider token files were not opened or copied.

The new clone's server ran on **127.0.0.1:8879**, using this scratch copy, with no worker loop. Browser/API checks confirmed:

- All thirteen deals appeared pending; Datalink and all four added deals opened with filings.
- The instruction pages seeded the unchanged root **Version 0**, published and default, as BUILD_SPEC requires before approval.
- Add Deal's seed search worked. A real SEC lookup for Penford returned six documents and its filing-index link. Only that lookup was processed directly; no extraction was submitted and the extraction-job count stayed zero.
- A hand-made test ledger was added only to the scratch catalog after the thirteen-deal check. Its note was edited and saved, its R1 flag opened the Questions view, and its Review tab showed checker Version 1 with zero errors/warnings. The initial blank-cell wrapping defect was corrected and rechecked. Pending catalog provenance and Count help were corrected as well.
- The manager inspected overview, pending-deal and saved-ledger Review screenshots. No browser page errors were observed in the final smoke.

The private server was stopped. The scratch database, filings, hand-made workbook and test state were deleted after results were recorded. No test copy is a replacement for the live state.

## Boundaries and remaining limits

In the 28 September re-review pass, `git status` shows no change to the protected files (root instruction, AGENTS, README, `_dev/STATUS.md`, DRAFTING_SPEC, BUILD_SPEC, BUILD_REVIEW, VERSION1_REREVIEW); DECISIONS.md gained only three italic supersession notes, appended to the lines they qualify so that line references elsewhere stay valid. The live app, its services, state and backups were not touched, and no extraction ran. The paragraphs below are the 27 September build's.

Hashes of **125 watched live code/instruction/catalog files**, **8 installed unit/drop-in files**, and the **4 protected development files** (root instruction, AGENTS, root README, STATUS) matched the initial baseline. The development extraction directory contains no workbooks. No live service, unit, backup timer or backup directory was changed, and no extraction job was submitted.

All 125 staged files passed credential-pattern and forbidden-artifact-path checks. No state, database, credential, cache or dependency directory was staged, and none of the four protected files was staged. The private test port was closed before scratch deletion.

Real extraction quality, provider authentication/refresh, real-model completion/import and the live switch-over are untested and await Austin's authorization. The first-run app path was tested only with stubs. Instruction publication, deployment, moving extraction-v2 and the protected documentation updates were not performed. Reports' flagged interpretation and workbook disagreements still need Austin's judgment.
