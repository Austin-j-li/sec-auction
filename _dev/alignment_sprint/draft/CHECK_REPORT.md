# Version 1 check report

27 September 2026. These checks concern the build and a hand-applied reading of its rules. No extraction model was run. A passing mechanical check does not establish source accuracy or research acceptance.

## Instruction checks

The draft retains all 29 ledger columns, the four-sheet contract, 30 event labels and D1–D5, E1–E14 and H1–H3 identifiers. All 22 rule identifiers resolve. The change map covers all 41 R/F/P/O themes, the evening rulings, C1–C18, and all 86 nonblank added or replaced lines. The drafter checked 197 line references; the manager independently checked theme/identifier coverage and named-deal exclusions.

The injection defense is the first line. Searches found no real deal, acquirer or researcher names, no rule-history wording, and no added instruction to expose reasoning. The quoted withdrawal phrase “for now” and event labels containing “changed” retain their ordinary meanings. Seven example blocks are balanced: the original five, adjusted where required, and two new synthetic examples. Column/value vocabulary and rule references were compared with the D lists and checker choices.

Draft SHA-256: `01110a1af35a0a3a4afaf0a2d2e77b67ce5f4cccf573356679cecef346825ee3`.

ROUND_MAP gives a source-backed entry for every fixed section-7 process/round anchor, every derive cell and every retest anchor. Its date and participation alternatives remain approval items; the map is not a new extraction. WORKBOOK_CHECK reports disagreements separately and changes no rule or workbook.

## Hand-made workbook and independent tool review

The manager generated the synthetic workbook with `test_check_lean.build_version_1_smoke_fixture` and ran `LeanChecker` directly. It returned **0 errors, 0 warnings, 0 information items** under checker **Version 1**. This one workbook includes mixed initiation, Q/R links, a signing Count of 1, a silent Formal bid with Conditions None, and a bid with required exclusivity and Conditions Light.

Two negative mutations were checked independently: signing Count 2 produced `ledger.count_signing`; required exclusivity with Conditions None produced `conditions.none_support`. Restoring the cells restored the clean verdict.

A fresh Astra reviewer independently reproduced and retested corrections for signing participation/scope, round-opening counts with intervening same-day entries and multiple openings, explicit H triggers, required exclusivity, and review-queue currency/type/price-basis coverage. Q/R sequences, caps, existing-row links, omitted-source-event R items and F2 restatement markers also passed the bounded review. No remaining actionable issue was found in that review; it did not substitute for the complete test suite or filing review.

## Automated suites

| Check | Result |
|---|---|
| Full Python suite: `PYTHONUSERBASE=~/work/.local python3 -m pytest _dev/tools -q` | **358 passed, 229 subtests passed**, 110.13 seconds; includes the HTTP acceptance tests. |
| HTTP acceptance, also run separately | **22 passed**; these are included in the full Python count, not additional tests. |
| Frontend: `npm test` in `cockpit/frontend` | **77 passed in 8 files**. |
| Headless browser core/deals/instructions/runs/trace suites | **138 checks passed**: 63 / 25 / 24 / 12 / 14. |
| Headless resize and responsive suites | Both passed; responsive checks covered **7 widths**. |
| Frontend production build | Passed. |
| Pending catalog verification | **9 of 9 passed**. |

The first complete Python run had 357 passes and one failure: an export test compared XLSX ZIP bytes even though export timestamps can change. The test now deliberately waits across the timestamp boundary and compares every archive member after normalizing only the generated core modified-time field. Its focused rerun and the full rerun above passed. This correction does not omit ledger cells, source sheets or provenance from the comparison.

The Python fixtures, HTTP suites and browser run suites use synthetic ledgers and fake runner/provider commands. The real model path was not exercised. Frontend assets were rebuilt with `npm run build` in this clone. The final core and Runs browser reruns passed 63 and 12 checks after the backend corrections.

A separate nine-deal catalog verification passed: all nine catalog entries have matching filing metadata/hashes and no old base workbook, findings or review documents. Git diff whitespace checks passed.

## Copied-live-state rehearsal

The live WAL database was opened with `mode=ro` and copied using SQLite's online backup API, then its filings directory was copied. The snapshot passed `PRAGMA integrity_check`. The fresh-state script retained **3 provider-account records for 2 users, 4 added-deal rows and 4 verified filings**. The retained table rows matched the snapshot exactly. Before app initialization, only accounts and added_deals existed; no old instructions/default, work, comments, activity or jobs carried over. Provider token files were not opened or copied.

The new clone's server ran on **127.0.0.1:8879**, using this scratch copy, with no worker loop. Browser/API checks confirmed:

- All thirteen deals appeared pending; Datalink and all four added deals opened with filings.
- The instruction pages seeded the unchanged root **Version 0**, published and default, as BUILD_SPEC requires before approval.
- Add Deal's seed search worked. A real SEC lookup for Penford returned six documents and its filing-index link. Only that lookup was processed directly; no extraction was submitted and the extraction-job count stayed zero.
- A hand-made test ledger was added only to the scratch catalog after the thirteen-deal check. Its note was edited and saved, its R1 flag opened the Questions view, and its Review tab showed checker Version 1 with zero errors/warnings. The initial blank-cell wrapping defect was corrected and rechecked. Pending catalog provenance and Count help were corrected as well.
- The manager inspected overview, pending-deal and saved-ledger Review screenshots. No browser page errors were observed in the final smoke.

The private server was stopped. The scratch database, filings, hand-made workbook and test state were deleted after results were recorded. No test copy is a replacement for the live state.

## Boundaries and remaining limits

Hashes of **125 watched live code/instruction/catalog files**, **8 installed unit/drop-in files**, and the **4 protected development files** (root instruction, AGENTS, root README, STATUS) matched the initial baseline. The development extraction directory contains no workbooks. No live service, unit, backup timer or backup directory was changed, and no extraction job was submitted.

All 125 staged files passed credential-pattern and forbidden-artifact-path checks. No state, database, credential, cache or dependency directory was staged, and none of the four protected files was staged. The private test port was closed before scratch deletion.

Real extraction quality, provider authentication/refresh, real-model completion/import and the live switch-over are untested and await Austin's authorization. The first-run app path was tested only with stubs. Instruction publication, deployment, moving extraction-v2 and the protected documentation updates were not performed. Reports' flagged interpretation and workbook disagreements still need Austin's judgment.
