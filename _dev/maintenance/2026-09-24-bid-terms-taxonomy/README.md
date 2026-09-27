# Bid terms and conditions taxonomy (24 September 2026)

Austin and Alex confirmed the taxonomy in person on 24 September; Austin decided that price cells hold the upfront amount only.

- [TAXONOMY_DRAFT5.md](TAXONOMY_DRAFT5.md): the confirmed taxonomy and the reasoning behind it. Drafts 2 to 4 are kept as history.
- [REVIEW_FABLE.md](REVIEW_FABLE.md): Fable 5.1 xhigh review of draft 2 against twelve filings ([prompt](REVIEW_PROMPT.md); 34 turns, $7.75).
- [SEC_Deal_Ledger_Extraction_Instruction_v1.14_draft.md](SEC_Deal_Ledger_Extraction_Instruction_v1.14_draft.md): the full v1.14 draft instruction. It is not the repository instruction, which stays v1.13.2 and frozen. It is cockpit draft `a4ca26ecfa92`, unpublished. The v1.14 candidate (below) is written from it and supersedes it; the draft stays unchanged.

Implemented and deployed 24 September, 22:02 UTC (both services restarted; no model runs):

- `_dev/tools/check_lean.py` 1.6 selects the v1.14 rules when the ledger has a `Stock %` column and checks every other workbook as v1.13.2. All nine `extraction/` workbooks and all five cockpit run versions reproduce their stored results exactly.
- `_dev/tools/cockpit/workspace.py` offers the new value lists in the editor and stores Stock % and CVR/earnout value figures as numbers.
- Tests: 199 Python unit tests, the cockpit import tests and 14 HTTP tests pass. The frontend is unchanged, so the browser and vitest suites were not rerun.

## Pilot, 24 September (Austin's go-ahead)

The v1.14 text is the cockpit draft `a4ca26ecfa92`, "draft f9595d7 (Austin)", unpublished; its hash equals this folder's file. Two isolated Opus 5.5 medium runs on it, started from Austin's cockpit session:

| Deal | Version | Time | Cost | Checker |
|---|---|---|---|---|
| Mac-Gray | `opus55-medium-20260924-2241-d7d267` | 10 min 27 s | $2.78 | v1.14; 1 error (round-opening order, as in the v1.13.2 draft), 16 warnings |
| Providence & Worcester | `opus55-medium-20260924-2241-38bc24` | 11 min 49 s | $2.82 | v1.14; 0 errors, 14 warnings |

Every bid row has all the new columns and no value-list or E12 consistency error. The codes follow the draft's rules on the cases Fable raised: CSC/Pamplona's 100% funding Committed and Party A's named facilities without a firm commitment Contingent; Party B's options CVR/earnout 2.5 on $19 upfront; G&W's $20.02 upfront plus a $1.13 CVR; CSC's and Party D's exclusivity Required; G&W's final STB review a regulatory Concern with Antitrust blank.

Against Alex's hand-coded `bid_type` (ref/deal_details_Alex_2026.xlsx): Formality alone reproduces all 13 Mac-Gray labels, and Formality with "not Heavy" reproduces all 14 Providence & Worcester labels. Alex coded Mac-Gray's contingent-financing final bids Formal and P&W's heavily conditional markups Informal, so each deal matches one reading; both are formulas on the pilot's columns. Stock % matches his all-cash coding on P&W (0 for G&W only, Not stated elsewhere). This is a consistency check on two deals, not a review of the codes against the filings.

Superseded by the 25 September spec (below): the two pilots are superseded drafts, and the candidate, not this draft, is what may be published. Whether the pilot condition review still gates publishing is for Austin to decide with Alex (V114_SPEC §13, gate 2).

## Specification for the v1.14 system upgrade, 25 September

- [V114_SPEC.md](V114_SPEC.md) records Austin's 25 September decisions (D1–D27). It specifies v1.14 as a system-wide upgrade, in work packages for an implementation team:
  - the instruction candidate, with an independent review of it and the list of draft lines it must change;
  - a re-check of the round maps;
  - the replacement Questions for Alex;
  - checker 1.7;
  - cockpit schema awareness: the payload, choice lists, editor, cross-schema compare, and the checker version shown;
  - the SEC link and provenance in the downloaded Excel;
  - a cross-schema workbook diff, and guards in the runner and the effort sweep;
  - moving the eight reviewed v1.13.2 working copies onto v1.14 (register, aligner, triage, and a safe rebase);
  - a first analysis tool and contract, with a side-by-side against Alex's hand coding;
  - deploy readiness, a deploy checklist, and the release procedure, including relocating the v1.13.2 `extraction/` workbooks;
  - documentation.
- [systemic-audit/](systemic-audit/) holds the four read-only audits behind it (A checker and tools, B cockpit, C instruction cascade, D documentation, release and research) and E, a fresh-eyes review of the spec's first system draft, whose findings the spec applies.
- The spec's first version (SHA-256 `477be57f…`) covered the instruction, checker 1.7, the round-trip test, the SEC link and documentation. Its gate order would have run v1.14 evaluations before the new checker was deployed; the upgrade spec deploys first.
- It revises GPT-6-Astra's approval spec, copied unchanged as [ASTRA_APPROVAL_SPEC.md](ASTRA_APPROVAL_SPEC.md), with its evidence record [ASTRA_RECOMMENDATION_REVIEW.md](ASTRA_RECOMMENDATION_REVIEW.md). The rest of Astra's working folder moved here on 25 September: [INSTRUCTION_CHANGE_PLAN.md](INSTRUCTION_CHANGE_PLAN.md) and [sources/](sources/), which holds text copies of Alex's documents and the only local copy of his August Q&A (evaluation material; never an input to extraction). Astra's links to `RECOMMENDATION_REVIEW.md` open a short redirect of that name ([RECOMMENDATION_REVIEW.md](RECOMMENDATION_REVIEW.md)) to `ASTRA_RECOMMENDATION_REVIEW.md` here; a separate session wrote it on 25 September, with [sources/README.md](sources/README.md), which records where the relocated Q&A now lives.
- The spec authorizes no model run, publication, deploy, commit or message to Alex.

**Status, 25 September, about 23:30 UTC.** The agent team has finished all three waves of the spec's work order (§7.13). Nothing is published, made the cockpit default or deployed: the candidate is written in this folder, the code (checker 1.7, the cockpit, catalog and tool changes, the migration and analysis tools) in a separate worktree, `~/work/Projects/sec-extraction-v114`, where it is built and tested. No model run, cockpit instruction version, commit or message to Alex has been made. Austin takes the gates (§13). Deliverables in this folder:

- `SEC_Deal_Ledger_Extraction_Instruction_v1.14_candidate.md`, with `CHANGELOG_v1.14_candidate.md` and `v1.14_candidate.diff`, its full diff against the draft (package A1): done, and frozen after review R. Header "Revision of 25 September 2026, v1.14."; SHA-256 `c2d47a479d09eb46d0ab9fbf887568fcf13e972e2e11acbf08d5cdfab468ab27` (also in `v1.14_candidate.sha256`). It is not published, not the cockpit default and not exported;
- `R_REVIEW.md`, the independent consistency review of the candidate (package R): done. 27 findings (2 must-fix, 17 should-fix, 8 notes), all fixed; its re-check found every finding resolved and the value lists in agreement with checker 1.7 (58 of 58 checks);
- `MAP_RECHECK.md`, the round-map re-check of six deals (package M, read-only): done;
- `ANALYSIS_CONTRACT.md` and `analysis/`, the analysis tool's contract and its runs on the two pilots, a v1.13.2 workbook and a working copy (package P): done. The side-by-side with Alex's coding reproduces audit D's counts;
- `migration/<deal>/`, the reviewed-facts registers for the eight edited deals (454 reviewed and 66 needs decision, on 520 rows) and the triage demonstrated on the two pilots (package MIG): done. The port batches are prepared, never applied;
- `Questions_for_Alex_2026-09-25.docx`, the replacement Questions for Alex (package A2): done; 4,559 words (2,541 before the case appendix) and 10 rendered pages, condensed from 6,013 words, with the independent check's ten fixes applied (SHA-256 `64ddad6c…4353`). It is not sent: sending is Austin's action (§13, gate 8). On 26 September it was reconciled with v1.14.1 and rebuilt (SHA-256 `f201a70e…243a`; the 25 September file is kept in `evidence/a2/pre-v1141/`; see `evidence/a2/README.md`);
- `DISPOSITIONS.md`, the disposition of all 314 audit findings (§7.14): done;
- `evidence/<package>/`, test and reproduction records: `s1`, `s2`, `s3`, `s4`, `s5`, `s7`, `ops`, `a2`, `w2ck` (the wave-2 editor checks) and `final` (the last full test run on the worktree);
- `release/`, the material for the deploy and the release (§12, §13), none of it applied: `deploy-tools.patch`, the whole `_dev/tools/` change for the deploy (61 files), taken from the baseline of the live `_dev/tools/` made with the worktree (`~/work/archive/v114-deploy/baseline-2026-09-25`) to the worktree; at about 23:30 UTC the live `_dev/tools/` still equalled the baseline; `release-gate12.patch`, for gate 12 (`d25-tools.patch` plus `tools-readme-release.patch`); `d25-tools.patch`, regenerated against the integrated tree (`d25-tools-wave1.patch` is kept for the record); `tools-readme-release.patch`; `PROPOSED_DOC_LINES.md`, the proposed text for the deploy and release documentation lines outside `_dev/tools/`; and `README.md`, the D25 steps;
- `pre-existing/`, 21 patches of the files the earlier sessions had already modified, so that gate 0 can commit those changes on their own.

Tests on the worktree, against the 25 September baselines (unit 199, HTTP 14, vitest 53): `python3 -m unittest discover -s _dev/tools -p 'test_*.py'` runs 292 tests, which pass (on 25 September one full run of 21 had a single failure; 20 further runs, 8 of them four at a time, all passed, and which test failed was not recorded); `python3 -m pytest -q -p no:cacheprovider _dev/tools/cockpit/acceptance/test_http.py` 20 pass; `npx vitest run` in `_dev/tools/cockpit/frontend` 77 pass (8 files); the seven browser suites pass against the worktree's built `dist/` (`evidence/final/tests.txt`).

Next: the lead's report to Austin (§7.14), then Austin's gates (§13), starting with gate 0 (commit the earlier sessions' uncommitted work on its own, using the `pre-existing/` patches) and gate 1 (accept the candidate, `MAP_RECHECK.md` and the report).

**Status, 26 September, about 20:45 UTC.** The release is v1.14.1, not v1.14 ([2026-09-26-v1141-streamline](../2026-09-26-v1141-streamline/)); the statements above about what is not deployed or published are superseded. The code shipped as `release/deploy-tools-v1141.patch` (checker 1.8, derive_analysis 0.3, the Opus 5.5 medium default), deployed at 19:41 UTC ([receipt](../2026-09-26-v1141-streamline/deployment-v1141.json)); `release/deploy-tools.patch` was never applied. Austin published the edited v1.14.1 candidate in the cockpit as v1.14.1 at 20:18 UTC (id `08caed447f7d`, SHA-256 `8a93df3cc6d989386958e9cb2d74ab34ebc0f07d281e8cc398605a388e066c98`, the reviewed `8bdb7c20…8a79` plus eight approved wording fixes) and made it the cockpit default. The five-deal retest passed ([results](../../reviews/2026-09-26-v1141-retest/README.md)); Austin decided Datalink follows the v1.14.1 text (four rounds), superseding F9. The questionnaire was rebuilt with the retest's 3.3(a) numbers and the Datalink decision ([evidence/a2/README.md](evidence/a2/README.md)); it is not sent. Still GATEs for Austin: exporting the repository instruction (still v1.13.2), commits and pushes (gate 0 included), sending the questionnaire, regenerating the migration registers (needs `lesson/`), rebasing working copies and gate 12, installing the unit-file changes (`TMPDIR`), and removing `dist.old`.
