# Recovery slice C_packets report

## Root instruction

- `SEC_Deal_Ledger_Extraction_Instruction.md`: **EXACT**. Copied the published v1.14.1 bytes from `_dev/recovery/2026-09-27-cockpit/instructions/v1.14.1_08caed447f7d.md`. The cockpit instruction API record gives SHA-256 `8a93df3cc6d989386958e9cb2d74ab34ebc0f07d281e8cc398605a388e066c98`; source and destination both match. `_dev/tools/cockpit/export_repo.py` `instruction_plan` reads `path.read_bytes()` and returns those bytes for the repository path, with no header removal or text transform.

## Candidate hashes

- v1.14 candidate: `c2d47a479d09eb46d0ab9fbf887568fcf13e972e2e11acbf08d5cdfab468ab27` — **match** against the recorded 26 Sep 17:07 hash.
- v1.14.1 reviewed candidate: `8bdb7c205512c9bcf55ffa7623fba0a8bb4aabaed23c99845fa88b4a80cc8a79` — **match**, preserved at `checks/candidate-8bdb7c20-as-reviewed.md`. The later 19:44:19 approved eight-replacement script produces the packet's final candidate hash `8a93df3cc6d989386958e9cb2d74ab34ebc0f07d281e8cc398605a388e066c98`, identical to the published instruction. The earlier hash does not describe the final candidate.

## Retest exports and questionnaire

- Copied five cockpit snapshot exports to the VM packet's slug names (`mac-gray.xlsx`, `providence-worcester.xlsx`, `stec.xlsx`, `synacor.xlsx`, `datalink.xlsx`). Their SHA-256 prefixes match the version IDs in the final 20:42:57 retest README: `1d1d60`, `366a73`, `0643aa`, `342883`, `350a91`.
- `build_docx.py` was replayed from the 18:54:14 complete 809-line read through the final 20:49:17 edit. SHA-256 `1ee0c8040148e0964fe4abffeb6cb10324590f2bb2b09d46383f9ac2b3f0df1c` matches the VM's reported final builder hash. All nine filing inputs are local. `python-docx` 1.2.0 was installed. The builder uses a hard-coded VM checkout path, so a temporary copy changed only that path for the local run; the packet builder retains the VM text. The regenerated DOCX has 5,198 words (3,091 before the appendix), as the VM README records. Its ZIP hash is not claimed equal to the VM file because ZIP timestamps vary. The packet README records the 27 September regeneration.

## Unresolved

- `grading/mechanical_check.py`: the 20:48:57 Edit expects a docstring absent from the available earlier scratch script. The VM's 20:44:46 first 30 lines confirm an intervening rewrite. No complete final source was found; an inaccurate scratch copy was removed.
- `AMENDMENT_SPEC.md`: available `sed -n 1,146p` output stops at its section 8 heading, with no proof it covers the whole file. It was not written. Other files marked `missing` in the table likewise have no complete final text.
- Original trial workbooks and their blinded copies, VM rendered PNG/PDF files, old DOCX copies, ZIP/tar/log binaries have no recoverable bytes. The five cockpit retest exports are separate and were restored.
- `analysis/formality_agreement.py` is restored, but its input `analysis/compare-alex-*/alex_bids.csv` files are unavailable. Its generated CSV/JSON were not fabricated.

## Checks run

- Published instruction, v1.14 candidate, reviewed v1.14.1 candidate, final v1.14.1 candidate, and builder SHA-256 comparison: **5/5 matched**.
- Five retest workbook SHA-256 prefixes versus their version IDs: **5/5 matched**.
- `python3 /tmp/recov/build_docx_local.py --check-only`: **exit 0**, `excerpts checked: 61 parts in 19 cases, all found on the cited pages`.
- `python3 /tmp/recov/build_docx_local.py --out _dev/maintenance/2026-09-24-bid-terms-taxonomy/Questions_for_Alex_2026-09-25.docx --date 2026-09-26`: **exit 0**, `words: 5198 (3091 in parts 1-3, 2107 in the case appendix)`.
- ZIP integrity and `word/document.xml` check on regenerated DOCX: **passed**.
- `ast.parse` on the four restored Python files: **4/4 passed**.
- No pytest command was run; this documentation slice names no test file.

## Per-file evidence and disposition

The following is the per-file table. Timestamps are evidence events, not file creation claims. `missing` and `binary lost` entries were inventoried but not written.

| Packet file (repo-relative) | Status | Evidence timestamp / basis |
|---|---|---|
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/ANALYSIS_CONTRACT.md` | missing | 2026-09-26T18:54:09Z VM inventory; no full content |
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/ASTRA_APPROVAL_SPEC.md` | missing | 2026-09-26T18:54:09Z VM inventory; no full content |
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/ASTRA_RECOMMENDATION_REVIEW.md` | missing | 2026-09-26T18:54:09Z VM inventory; no full content |
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/CHANGELOG_v1.14_candidate.md` | missing | 2026-09-26T18:54:09Z VM inventory; no full content |
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/DISPOSITIONS.md` | missing | 2026-09-26T18:54:09Z VM inventory; no full content |
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/INSTRUCTION_CHANGE_PLAN.md` | missing | 2026-09-26T18:54:09Z VM inventory; no full content |
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/MAP_RECHECK.md` | missing | 2026-09-26T18:54:09Z VM inventory; no full content |
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/Questions_for_Alex_2026-09-25.docx` | REBUILT | 2026-09-26T18:54:14Z builder read; 2026-09-27 regenerated |
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/README.md` | REPLAYED | 2026-09-26T20:44:55Z complete cat; 20:51:35 append |
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/RECOMMENDATION_REVIEW.md` | missing | 2026-09-26T18:54:09Z VM inventory; no full content |
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/REPORT_v1.14_implementation.md` | missing | 2026-09-26T18:54:09Z VM inventory; no full content |
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/REVIEW_FABLE.md` | missing | 2026-09-26T18:54:09Z VM inventory; no full content |
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/REVIEW_PROMPT.md` | missing | 2026-09-26T18:54:09Z VM inventory; no full content |
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/R_REVIEW.md` | missing | 2026-09-26T18:54:09Z VM inventory; no full content |
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/SEC_Deal_Ledger_Extraction_Instruction_v1.14_candidate.md` | EXACT | 2026-09-26T17:08:07.850Z Read |
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/SEC_Deal_Ledger_Extraction_Instruction_v1.14_draft.md` | EXACT | 2026-09-27 cockpit snapshot `instructions/draft-a4ca26ecfa92_a4ca26ecfa92.md`; SHA-256 `f9595d74…89aea97` matches 2026-09-26T18:54:45.749Z evidence |
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/TAXONOMY_DRAFT2.md` | missing | 2026-09-26T18:54:09Z VM inventory; no full content |
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/TAXONOMY_DRAFT3.md` | EXACT | 2026-09-24T10:47:21.262Z Write |
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/TAXONOMY_DRAFT4.md` | REPLAYED | 2026-09-24T10:47:21Z Draft3; 10:53:44, 10:53:54, 13:19:01 edits |
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/TAXONOMY_DRAFT5.md` | REPLAYED | 2026-09-24T13:19:01Z Draft4; 17:49:29, 22:02:57, 2026-09-26T20:51:35 edits |
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/V114_SPEC.md` | missing | 2026-09-26T18:54:09Z VM inventory; no full content |
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/evidence/a2/README.md` | REPLAYED | 2026-09-26T18:54:09Z+18:54:11Z complete cat; 19:01:32, 20:49:05, 20:49:17 edits; 27 Sep note |
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/evidence/a2/build_docx.py` | REPLAYED | 2026-09-26T18:54:14Z full read; 8 Python edits + 2 sed edits through 20:49:17Z |
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/evidence/a2/page-01.png` | binary lost | 2026-09-26T19:00:24.345Z |
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/evidence/a2/page-02.png` | binary lost | 2026-09-26T19:00:24.851Z |
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/evidence/a2/page-03.png` | binary lost | 2026-09-26T19:00:30.683Z |
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/evidence/a2/page-04.png` | binary lost | 2026-09-26T19:00:31.254Z |
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/evidence/a2/page-05.png` | binary lost | 2026-09-26T19:00:25.513Z |
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/evidence/a2/page-06.png` | binary lost | 2026-09-26T20:48:43.031Z |
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/evidence/a2/page-07.png` | binary lost | 2026-09-26T20:48:43.443Z |
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/evidence/a2/page-08.png` | binary lost | 2026-09-26T20:48:47.635Z |
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/evidence/a2/page-09.png` | binary lost | 2026-09-26T20:49:05Z README records 12-page render; binary unavailable |
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/evidence/a2/page-10.png` | binary lost | 2026-09-26T20:49:05Z README records 12-page render; binary unavailable |
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/evidence/a2/page-11.png` | binary lost | 2026-09-26T20:49:05Z README records 12-page render; binary unavailable |
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/evidence/a2/page-12.png` | binary lost | 2026-09-26T20:49:05Z README records 12-page render; binary unavailable |
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/evidence/a2/page.pdf` | binary lost | 2026-09-26T18:54:09Z VM inventory; no full content |
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/evidence/a2/pre-retest/Questions_for_Alex_2026-09-25.docx` | binary lost | 2026-09-26T18:54:09Z VM inventory; no full content |
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/evidence/a2/render.py` | EXACT | 2026-09-26T18:54:11Z complete cat; SHA-256 cb8910af |
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/migration/README.md` | REPLAYED | 2026-09-26T19:08:35Z complete cat; 19:18:38, 20:51:35 edits |
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/release/PROPOSED_DOC_LINES.md` | REPLAYED | 2026-09-26T20:44:10Z full read; 20:51:35 edit |
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/release/README.md` | REPLAYED | 2026-09-26T19:20:09Z full read; 3 edits + 19:22:29 script + 20:51:35 edit |
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/v1.14_candidate.diff` | missing | 2026-09-26T18:54:09Z VM inventory; no full content |
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/v1.14_candidate.sha256` | REPLAYED | 2026-09-26T17:07:34Z recorded hash |
| `_dev/maintenance/2026-09-26-astra-default-pro-verification/AMENDMENT_SPEC.md` | missing | 2026-09-26T18:54:18Z VM inventory; no full content |
| `_dev/maintenance/2026-09-26-astra-default-pro-verification/DECISION_BRIEF_2026-09-26.md` | REPLAYED | 2026-09-26T16:56:35Z heredoc; 19:02:16 status edit |
| `_dev/maintenance/2026-09-26-astra-default-pro-verification/PRO_FINDINGS_VERIFICATION.md` | missing | 2026-09-26T18:54:18Z VM inventory; no full content |
| `_dev/maintenance/2026-09-26-astra-default-pro-verification/README.md` | REPLAYED | 2026-09-26T18:54:18Z complete cat; 19:02:16, 20:51:42 edits |
| `_dev/maintenance/2026-09-26-astra-default-pro-verification/astra-default.patch` | missing | 2026-09-26T18:54:18Z VM inventory; no full content |
| `_dev/maintenance/2026-09-26-astra-default-pro-verification/before.json` | missing | 2026-09-26T18:54:18Z VM inventory; no full content |
| `_dev/maintenance/2026-09-26-astra-default-pro-verification/build.log` | missing | 2026-09-26T18:54:18Z VM inventory; no full content |
| `_dev/maintenance/2026-09-26-astra-default-pro-verification/deployment-status.txt` | missing | 2026-09-26T18:54:18Z VM inventory; no full content |
| `_dev/maintenance/2026-09-26-astra-default-pro-verification/deployment.json` | missing | 2026-09-26T18:54:18Z VM inventory; no full content |
| `_dev/maintenance/2026-09-26-astra-default-pro-verification/frontend-tests.log` | missing | 2026-09-26T18:54:18Z VM inventory; no full content |
| `_dev/maintenance/2026-09-26-astra-default-pro-verification/live-dialog-verification.json` | missing | 2026-09-26T18:54:18Z VM inventory; no full content |
| `_dev/maintenance/2026-09-26-astra-default-pro-verification/preservation-verification.json` | missing | 2026-09-26T18:54:18Z VM inventory; no full content |
| `_dev/maintenance/2026-09-26-astra-default-pro-verification/python-tests.log` | missing | 2026-09-26T18:54:18Z VM inventory; no full content |
| `_dev/maintenance/2026-09-26-astra-default-pro-verification/task-delta-main.patch` | missing | 2026-09-26T18:54:18Z VM inventory; no full content |
| `_dev/maintenance/2026-09-26-astra-default-pro-verification/task-delta-upgrade.patch` | missing | 2026-09-26T18:54:18Z VM inventory; no full content |
| `_dev/maintenance/2026-09-26-astra-default-pro-verification/task-delta.json` | missing | 2026-09-26T18:54:18Z VM inventory; no full content |
| `_dev/maintenance/2026-09-26-astra-default-pro-verification/upgrade-final-tests.log` | missing | 2026-09-26T18:54:18Z VM inventory; no full content |
| `_dev/maintenance/2026-09-26-astra-default-pro-verification/upgrade-frontend-tests.log` | missing | 2026-09-26T18:54:18Z VM inventory; no full content |
| `_dev/maintenance/2026-09-26-astra-default-pro-verification/upgrade-retest.log` | missing | 2026-09-26T18:54:18Z VM inventory; no full content |
| `_dev/maintenance/2026-09-26-astra-default-pro-verification/upgrade-tests.log` | missing | 2026-09-26T18:54:18Z VM inventory; no full content |
| `_dev/maintenance/2026-09-26-v1141-streamline/CHANGELOG_v1.14.1_candidate.md` | REPLAYED | 2026-09-26T17:28:00Z Write; 20:50:41 edit |
| `_dev/maintenance/2026-09-26-v1141-streamline/DEPLOY_RUNBOOK.md` | REPLAYED | 2026-09-26T19:27:51Z Write; 20:50:41 edit |
| `_dev/maintenance/2026-09-26-v1141-streamline/PIPELINE_UPGRADE_REPORT.md` | REPLAYED | 2026-09-26T19:29:53Z Write; 20:51:11 edits |
| `_dev/maintenance/2026-09-26-v1141-streamline/PIPELINE_UPGRADE_SPEC.md` | REPLAYED | 2026-09-26T19:20:07Z full read; 20:50:41 edit |
| `_dev/maintenance/2026-09-26-v1141-streamline/SEC_Deal_Ledger_Extraction_Instruction_v1.14.1_candidate.md` | REPLAYED | 2026-09-26T19:08:22Z full read; 19:44:19 eight replacements; SHA-256 8a93df3c |
| `_dev/maintenance/2026-09-26-v1141-streamline/STALENESS_CHECK.md` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/maintenance/2026-09-26-v1141-streamline/V1141_SPEC.md` | REPLAYED | 2026-09-26T18:45:49.357Z full read (includes 17:15:01 corrections); 20:50:41 status insertion; 20:50:48 step-9 edit |
| `_dev/maintenance/2026-09-26-v1141-streamline/checks/candidate-8bdb7c20-as-reviewed.md` | EXACT | 2026-09-26T19:08:22Z full read; SHA-256 8bdb7c20 |
| `_dev/maintenance/2026-09-26-v1141-streamline/checks/recheck_trial.py` | EXACT | 2026-09-26T18:58:24Z heredoc |
| `_dev/maintenance/2026-09-26-v1141-streamline/deployment-v1141.json` | REPLAYED | 2026-09-26T20:44:31Z complete cat; 20:48:56, 20:49:07 edits |
| `_dev/maintenance/2026-09-26-v1141-streamline/retest/RELEASE_CHECKLIST.md` | REPLAYED | 2026-09-26T19:18:51Z Write; 19:18:59, 20:50:41, 20:50:48, 20:50:57 edits |
| `_dev/maintenance/2026-09-26-v1141-streamline/retest/RETEST_PLAN.md` | REPLAYED | 2026-09-26T19:18:37Z Write; 20:50:41, 20:50:57 edits |
| `_dev/maintenance/2026-09-26-v1141-streamline/retest/acceptance.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/maintenance/2026-09-26-v1141-streamline/retest/retest_acceptance.py` | EXACT | 2026-09-26T19:17:40Z heredoc |
| `_dev/maintenance/2026-09-26-v1141-streamline/v1.14.1_candidate.sha256` | REPLAYED | 2026-09-26T20:50:41Z recorded printf |
| `_dev/reviews/2026-09-26-v114-15-run-trial/COMPLETION.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/GRADING_KICKOFF.md` | REPLAYED | 2026-09-26T11:58:44Z complete cat; 20:48:47 edit |
| `_dev/reviews/2026-09-26-v114-15-run-trial/ISOLATION_PREFLIGHT.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/README.md` | REPLAYED | 2026-09-26T20:44:41Z complete cat; 20:48:47 edit |
| `_dev/reviews/2026-09-26-v114-15-run-trial/SETUP.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/administration/GRADING_KICKOFF_prior_to_pro_dispatch.md` | REPLAYED | 2026-09-26T11:59:44Z complete cat; 20:48:47 edit |
| `_dev/reviews/2026-09-26-v114-15-run-trial/administration/VERIFICATION.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/administration/anonymization-v2.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/administration/blind-key.json` | EXACT | 2026-09-26T12:30:58Z complete cat |
| `_dev/reviews/2026-09-26-v114-15-run-trial/administration/finalize.py` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/administration/outcomes.json` | EXACT | 2026-09-26T12:30:58Z complete cat |
| `_dev/reviews/2026-09-26-v114-15-run-trial/administration/status.py` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/blinded/mac-gray/A.xlsx` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/blinded/mac-gray/B.xlsx` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/blinded/mac-gray/C.xlsx` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/blinded/mac-gray/D.xlsx` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/blinded/mac-gray/E.xlsx` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/blinded/manifest.json` | EXACT | 2026-09-26T11:59:03Z complete cat |
| `_dev/reviews/2026-09-26-v114-15-run-trial/blinded/providence-worcester/A.xlsx` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/blinded/providence-worcester/B.xlsx` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/blinded/providence-worcester/C.xlsx` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/blinded/providence-worcester/D.xlsx` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/blinded/providence-worcester/E.xlsx` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/blinded/stec/A.xlsx` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/blinded/stec/B.xlsx` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/blinded/stec/C.xlsx` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/blinded/stec/D.xlsx` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/blinded/stec/E.xlsx` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/driver-launch.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/driver.log` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/grading/01_blind_findings.md` | EXACT | 2026-09-26T12:30:43.988Z Write |
| `_dev/reviews/2026-09-26-v114-15-run-trial/grading/02_unblinded_comparison.md` | EXACT | 2026-09-26T12:37:32.540Z Write |
| `_dev/reviews/2026-09-26-v114-15-run-trial/grading/03_instruction_and_research_decisions.md` | REPLAYED | 2026-09-26T12:40:41Z Write; 20:48:47 edit |
| `_dev/reviews/2026-09-26-v114-15-run-trial/grading/04_fable_vs_pro_disagreements.md` | EXACT | 2026-09-26T16:09:41Z heredoc |
| `_dev/reviews/2026-09-26-v114-15-run-trial/grading/README.md` | REPLAYED | 2026-09-26T12:41:11Z Write; 16:09:47, 20:48:47 edits |
| `_dev/reviews/2026-09-26-v114-15-run-trial/grading/mechanical_check.py` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/grading/mechanical_check_results.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/grading/scores.csv` | EXACT | 2026-09-26T12:39:09.256Z Write |
| `_dev/reviews/2026-09-26-v114-15-run-trial/inputs/SEC_Deal_Ledger_Extraction_Instruction.md` | EXACT | 2026-09-26T12:00:12.840Z Read |
| `_dev/reviews/2026-09-26-v114-15-run-trial/inputs/raw_filing/mac-gray_2013-12-04_DEFM14A.htm` | EXACT | 2026-09-26T20:48:25Z cmp confirms equality with raw_filing |
| `_dev/reviews/2026-09-26-v114-15-run-trial/inputs/raw_filing/providence-worcester_2016-09-20_DEFM14A.htm` | EXACT | 2026-09-26T20:48:25Z cmp confirms equality with raw_filing |
| `_dev/reviews/2026-09-26-v114-15-run-trial/inputs/raw_filing/stec_2013-08-08_DEFM14A.htm` | EXACT | 2026-09-26T20:48:25Z cmp confirms equality with raw_filing |
| `_dev/reviews/2026-09-26-v114-15-run-trial/parallel-start.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/pin.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/plan.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/pro-review/PRO_RESPONSE.txt` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/pro-review/REQUEST.md` | EXACT | 2026-09-26T20:44:41Z complete cat |
| `_dev/reviews/2026-09-26-v114-15-run-trial/pro-review/SEC_Anonymous_Extraction_Review.pdf` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/pro-review/SEC_Anonymous_Extraction_Review.txt` | EXACT | 2026-09-26T12:31:57.435Z Read |
| `_dev/reviews/2026-09-26-v114-15-run-trial/pro-review/UNBLINDED_RESULTS.md` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/pro-review/anonymous_sec_extraction_review.zip` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/pro-review/dispatch-receipt.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/pro-review/package/MANIFEST.json` | EXACT | 2026-09-26T11:59:03Z complete cat |
| `_dev/reviews/2026-09-26-v114-15-run-trial/pro-review/package/README.md` | EXACT | 2026-09-26T11:59:03Z complete cat |
| `_dev/reviews/2026-09-26-v114-15-run-trial/pro-review/package/instruction_v1.14.md` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/pro-review/retrieval-receipt.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/pro-review/unblinded-scores.csv` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/pro-review/unblinded-scores.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/protected-after.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/protected-before.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-gpt-6-astra-high-r1/check.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-gpt-6-astra-high-r1/command.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-gpt-6-astra-high-r1/events.jsonl.gz` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-gpt-6-astra-high-r1/launch.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-gpt-6-astra-high-r1/launcher.log` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-gpt-6-astra-high-r1/mac-gray.xlsx` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-gpt-6-astra-high-r1/metadata.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-gpt-6-astra-high-r1/prompt.txt` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-gpt-6-astra-high-r1/raw-workspace-manifest.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-gpt-6-astra-high-r1/raw-workspace.tar.gz` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-gpt-6-astra-high-r1/receipt.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-gpt-6-astra-high-r1/status.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-gpt-6-astra-high-r1/stderr.log` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-gpt-6-astra-high-r1/validation.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-gpt-6-astra-xhigh-r1/check.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-gpt-6-astra-xhigh-r1/command.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-gpt-6-astra-xhigh-r1/events.jsonl.gz` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-gpt-6-astra-xhigh-r1/launch.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-gpt-6-astra-xhigh-r1/launcher.log` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-gpt-6-astra-xhigh-r1/mac-gray.xlsx` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-gpt-6-astra-xhigh-r1/metadata.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-gpt-6-astra-xhigh-r1/prompt.txt` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-gpt-6-astra-xhigh-r1/raw-workspace-manifest.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-gpt-6-astra-xhigh-r1/raw-workspace.tar.gz` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-gpt-6-astra-xhigh-r1/receipt.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-gpt-6-astra-xhigh-r1/status.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-gpt-6-astra-xhigh-r1/stderr.log` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-gpt-6-astra-xhigh-r1/validation.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-gpt-6-sol-xhigh-r1/check.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-gpt-6-sol-xhigh-r1/command.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-gpt-6-sol-xhigh-r1/events.jsonl.gz` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-gpt-6-sol-xhigh-r1/launch.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-gpt-6-sol-xhigh-r1/launcher.log` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-gpt-6-sol-xhigh-r1/mac-gray.xlsx` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-gpt-6-sol-xhigh-r1/metadata.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-gpt-6-sol-xhigh-r1/prompt.txt` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-gpt-6-sol-xhigh-r1/raw-workspace-manifest.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-gpt-6-sol-xhigh-r1/raw-workspace.tar.gz` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-gpt-6-sol-xhigh-r1/receipt.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-gpt-6-sol-xhigh-r1/status.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-gpt-6-sol-xhigh-r1/stderr.log` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-gpt-6-sol-xhigh-r1/validation.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-opus-5-5-medium-r1/check.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-opus-5-5-medium-r1/command.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-opus-5-5-medium-r1/events.jsonl.gz` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-opus-5-5-medium-r1/launch.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-opus-5-5-medium-r1/launcher.log` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-opus-5-5-medium-r1/mac-gray.xlsx` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-opus-5-5-medium-r1/metadata.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-opus-5-5-medium-r1/prompt.txt` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-opus-5-5-medium-r1/provider-results.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-opus-5-5-medium-r1/raw-workspace-manifest.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-opus-5-5-medium-r1/raw-workspace.tar.gz` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-opus-5-5-medium-r1/receipt.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-opus-5-5-medium-r1/status.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-opus-5-5-medium-r1/stderr.log` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-opus-5-5-medium-r1/validation.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-opus-5-5-xhigh-r1/check.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-opus-5-5-xhigh-r1/command.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-opus-5-5-xhigh-r1/events.jsonl.gz` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-opus-5-5-xhigh-r1/launch.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-opus-5-5-xhigh-r1/launcher.log` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-opus-5-5-xhigh-r1/mac-gray.xlsx` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-opus-5-5-xhigh-r1/metadata.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-opus-5-5-xhigh-r1/prompt.txt` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-opus-5-5-xhigh-r1/provider-results.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-opus-5-5-xhigh-r1/raw-workspace-manifest.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-opus-5-5-xhigh-r1/raw-workspace.tar.gz` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-opus-5-5-xhigh-r1/receipt.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-opus-5-5-xhigh-r1/status.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-opus-5-5-xhigh-r1/stderr.log` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/mac-gray-opus-5-5-xhigh-r1/validation.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-gpt-6-astra-high-r1/check.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-gpt-6-astra-high-r1/command.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-gpt-6-astra-high-r1/events.jsonl.gz` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-gpt-6-astra-high-r1/launch.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-gpt-6-astra-high-r1/launcher.log` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-gpt-6-astra-high-r1/metadata.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-gpt-6-astra-high-r1/prompt.txt` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-gpt-6-astra-high-r1/providence-worcester.xlsx` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-gpt-6-astra-high-r1/raw-workspace-manifest.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-gpt-6-astra-high-r1/raw-workspace.tar.gz` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-gpt-6-astra-high-r1/receipt.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-gpt-6-astra-high-r1/status.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-gpt-6-astra-high-r1/stderr.log` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-gpt-6-astra-high-r1/validation.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-gpt-6-astra-xhigh-r1/check.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-gpt-6-astra-xhigh-r1/command.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-gpt-6-astra-xhigh-r1/events.jsonl.gz` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-gpt-6-astra-xhigh-r1/launch.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-gpt-6-astra-xhigh-r1/launcher.log` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-gpt-6-astra-xhigh-r1/metadata.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-gpt-6-astra-xhigh-r1/prompt.txt` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-gpt-6-astra-xhigh-r1/providence-worcester.xlsx` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-gpt-6-astra-xhigh-r1/raw-workspace-manifest.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-gpt-6-astra-xhigh-r1/raw-workspace.tar.gz` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-gpt-6-astra-xhigh-r1/receipt.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-gpt-6-astra-xhigh-r1/status.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-gpt-6-astra-xhigh-r1/stderr.log` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-gpt-6-astra-xhigh-r1/validation.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-gpt-6-sol-xhigh-r1/check.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-gpt-6-sol-xhigh-r1/command.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-gpt-6-sol-xhigh-r1/events.jsonl.gz` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-gpt-6-sol-xhigh-r1/launch.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-gpt-6-sol-xhigh-r1/launcher.log` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-gpt-6-sol-xhigh-r1/metadata.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-gpt-6-sol-xhigh-r1/prompt.txt` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-gpt-6-sol-xhigh-r1/providence-worcester.xlsx` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-gpt-6-sol-xhigh-r1/raw-workspace-manifest.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-gpt-6-sol-xhigh-r1/raw-workspace.tar.gz` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-gpt-6-sol-xhigh-r1/receipt.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-gpt-6-sol-xhigh-r1/status.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-gpt-6-sol-xhigh-r1/stderr.log` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-gpt-6-sol-xhigh-r1/validation.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-opus-5-5-medium-r1/check.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-opus-5-5-medium-r1/command.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-opus-5-5-medium-r1/events.jsonl.gz` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-opus-5-5-medium-r1/launch.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-opus-5-5-medium-r1/launcher.log` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-opus-5-5-medium-r1/metadata.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-opus-5-5-medium-r1/prompt.txt` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-opus-5-5-medium-r1/providence-worcester.xlsx` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-opus-5-5-medium-r1/provider-results.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-opus-5-5-medium-r1/raw-workspace-manifest.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-opus-5-5-medium-r1/raw-workspace.tar.gz` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-opus-5-5-medium-r1/receipt.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-opus-5-5-medium-r1/status.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-opus-5-5-medium-r1/stderr.log` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-opus-5-5-medium-r1/validation.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-opus-5-5-xhigh-r1/check.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-opus-5-5-xhigh-r1/command.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-opus-5-5-xhigh-r1/events.jsonl.gz` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-opus-5-5-xhigh-r1/launch.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-opus-5-5-xhigh-r1/launcher.log` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-opus-5-5-xhigh-r1/metadata.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-opus-5-5-xhigh-r1/prompt.txt` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-opus-5-5-xhigh-r1/providence-worcester.xlsx` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-opus-5-5-xhigh-r1/provider-results.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-opus-5-5-xhigh-r1/raw-workspace-manifest.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-opus-5-5-xhigh-r1/raw-workspace.tar.gz` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-opus-5-5-xhigh-r1/receipt.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-opus-5-5-xhigh-r1/status.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-opus-5-5-xhigh-r1/stderr.log` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/providence-worcester-opus-5-5-xhigh-r1/validation.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-gpt-6-astra-high-r1/check.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-gpt-6-astra-high-r1/command.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-gpt-6-astra-high-r1/events.jsonl.gz` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-gpt-6-astra-high-r1/launch.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-gpt-6-astra-high-r1/launcher.log` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-gpt-6-astra-high-r1/metadata.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-gpt-6-astra-high-r1/prompt.txt` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-gpt-6-astra-high-r1/raw-workspace-manifest.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-gpt-6-astra-high-r1/raw-workspace.tar.gz` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-gpt-6-astra-high-r1/receipt.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-gpt-6-astra-high-r1/status.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-gpt-6-astra-high-r1/stderr.log` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-gpt-6-astra-high-r1/stec.xlsx` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-gpt-6-astra-high-r1/validation.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-gpt-6-astra-xhigh-r1/check.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-gpt-6-astra-xhigh-r1/command.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-gpt-6-astra-xhigh-r1/events.jsonl.gz` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-gpt-6-astra-xhigh-r1/launch.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-gpt-6-astra-xhigh-r1/launcher.log` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-gpt-6-astra-xhigh-r1/metadata.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-gpt-6-astra-xhigh-r1/prompt.txt` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-gpt-6-astra-xhigh-r1/raw-workspace-manifest.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-gpt-6-astra-xhigh-r1/raw-workspace.tar.gz` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-gpt-6-astra-xhigh-r1/receipt.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-gpt-6-astra-xhigh-r1/status.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-gpt-6-astra-xhigh-r1/stderr.log` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-gpt-6-astra-xhigh-r1/stec.xlsx` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-gpt-6-astra-xhigh-r1/validation.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-gpt-6-sol-xhigh-r1/check.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-gpt-6-sol-xhigh-r1/command.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-gpt-6-sol-xhigh-r1/events.jsonl.gz` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-gpt-6-sol-xhigh-r1/launch.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-gpt-6-sol-xhigh-r1/launcher.log` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-gpt-6-sol-xhigh-r1/metadata.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-gpt-6-sol-xhigh-r1/prompt.txt` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-gpt-6-sol-xhigh-r1/raw-workspace-manifest.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-gpt-6-sol-xhigh-r1/raw-workspace.tar.gz` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-gpt-6-sol-xhigh-r1/receipt.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-gpt-6-sol-xhigh-r1/status.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-gpt-6-sol-xhigh-r1/stderr.log` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-gpt-6-sol-xhigh-r1/stec.xlsx` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-gpt-6-sol-xhigh-r1/validation.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-opus-5-5-medium-r1/check.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-opus-5-5-medium-r1/command.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-opus-5-5-medium-r1/events.jsonl.gz` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-opus-5-5-medium-r1/launch.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-opus-5-5-medium-r1/launcher.log` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-opus-5-5-medium-r1/metadata.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-opus-5-5-medium-r1/prompt.txt` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-opus-5-5-medium-r1/provider-results.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-opus-5-5-medium-r1/raw-workspace-manifest.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-opus-5-5-medium-r1/raw-workspace.tar.gz` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-opus-5-5-medium-r1/receipt.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-opus-5-5-medium-r1/status.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-opus-5-5-medium-r1/stderr.log` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-opus-5-5-medium-r1/stec.xlsx` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-opus-5-5-medium-r1/validation.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-opus-5-5-xhigh-r1/check.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-opus-5-5-xhigh-r1/command.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-opus-5-5-xhigh-r1/events.jsonl.gz` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-opus-5-5-xhigh-r1/launch.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-opus-5-5-xhigh-r1/launcher.log` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-opus-5-5-xhigh-r1/metadata.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-opus-5-5-xhigh-r1/prompt.txt` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-opus-5-5-xhigh-r1/provider-results.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-opus-5-5-xhigh-r1/raw-workspace-manifest.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-opus-5-5-xhigh-r1/raw-workspace.tar.gz` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-opus-5-5-xhigh-r1/receipt.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-opus-5-5-xhigh-r1/status.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-opus-5-5-xhigh-r1/stderr.log` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-opus-5-5-xhigh-r1/stec.xlsx` | binary lost | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v114-15-run-trial/runs/stec-opus-5-5-xhigh-r1/validation.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v1141-retest/README.md` | REPLAYED | 2026-09-26T20:42:57Z final heredoc; 20:52:31 append |
| `_dev/reviews/2026-09-26-v1141-retest/analysis/formality_agreement.csv` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v1141-retest/analysis/formality_agreement.json` | missing | 2026-09-26T11:58:50Z VM inventory; no full content |
| `_dev/reviews/2026-09-26-v1141-retest/analysis/formality_agreement.py` | REPLAYED | 2026-09-26T20:46:22Z heredoc; 20:46:36 sed |
| `_dev/reviews/2026-09-26-v1141-retest/datalink.xlsx` | EXACT | 2026-09-27 cockpit export; 26 Sep version hash 350a91 |
| `_dev/reviews/2026-09-26-v1141-retest/mac-gray.xlsx` | EXACT | 2026-09-27 cockpit export; 26 Sep version hash 1d1d60 |
| `_dev/reviews/2026-09-26-v1141-retest/providence-worcester.xlsx` | EXACT | 2026-09-27 cockpit export; 26 Sep version hash 366a73 |
| `_dev/reviews/2026-09-26-v1141-retest/stec.xlsx` | EXACT | 2026-09-27 cockpit export; 26 Sep version hash 0643aa |
| `_dev/reviews/2026-09-26-v1141-retest/synacor.xlsx` | EXACT | 2026-09-27 cockpit export; 26 Sep version hash 342883 |

## Fixes

- Restored `_dev/maintenance/2026-09-26-v1141-streamline/V1141_SPEC.md` from the complete 2026-09-26T18:45:49.357Z Read, which already included the three 17:15:01.796Z corrections. Applied the 20:50:41.531Z status insertion and 20:50:48.908Z step-9 correction once. The question-count evidence now says 6–12 Questions; the row-count criterion is no more rows than the trial Opus-medium workbooks; the rebase warning names row marks and finding decisions. Updated its provenance row above.
- Copied the v1.14 draft byte-exact from the cockpit snapshot (`instructions/draft-a4ca26ecfa92_a4ca26ecfa92.md`) to the taxonomy packet. Its SHA-256 is `f9595d7413149f86c074f1d4b9ef96a5a24b3d8dd9b6c11061b0bd6e889aea97`, matching the 2026-09-26T18:54:45.749Z evidence. Corrected this report and `_dev/recovery/RESTORED_PACKETS.md` from missing to EXACT.
- Removed one repeated 20:45 status paragraph each from `release/README.md`, `release/PROPOSED_DOC_LINES.md`, and `migration/README.md`; these paragraphs came from the single 2026-09-26T20:51:35.340Z insertion.
- Post-fix checks: 4 corrected spec strings present and 3 stale strings absent; all 3 status paragraphs appear exactly once; draft bytes equal the snapshot and full SHA-256 matches. All checks passed. No pytest file is assigned to this slice.
