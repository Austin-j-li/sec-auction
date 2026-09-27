# D_tools recovery report

## Files

- `_dev/tools/sandbox/run_model.py` — REBUILT. No complete VM snapshot; one partial Read on 2026-09-21 15:44 and Bash evidence 2026-09-26 18:48:39 (Opus default), 19:09:47 (instruction-aware revision schema), 19:10:47 (runner changes), and 19:24:32 (main-tree merge conflict). Replayed edits: 0. Local changes restore Opus 5.5 medium by default, Astra high when explicitly selected, and a 29-column revision guard keyed to the supplied instruction. Exact VM source equality unresolved.
- `_dev/tools/test_run_model.py` — REBUILT. No complete snapshot or replayed edits; 2026-09-26 18:49:07 and 19:10:47 Bash test edits. Local tests cover default transport and 29-column revision. Exact VM source equality unresolved.
- `_dev/tools/diff_workbooks.py` — REBUILT. No complete snapshot or replayed edits; 2026-09-26 18:32:46 Bash shows the earlier implementation, and 19:09:00 shows the v1.14 crosswalk. Local comparison reads sheets by header name and handles `All cash`/`Stock %` across 26- and 29-column ledgers. Exact VM source equality unresolved.
- `_dev/tools/effort_sweep.py` — REBUILT. No complete snapshot or replayed edits; 2026-09-26 19:16:09 Bash gives the pinned-instruction checker and process-Question metrics changes. Local code also carries the schema-aware ledger statistics and planned filing/instruction path changes evidenced by the pipeline upgrade packet. Exact VM source equality unresolved.
- `_dev/tools/test_effort_sweep.py` — REBUILT. No complete snapshot or replayed edits; 2026-09-26 19:16:09 Bash gives the Note and process-Question test. Exact VM source equality unresolved.
- `_dev/tools/fetch_filing.py` — REBUILT classification (baseline retained; VM exactness unverified), no recovery change. No later relevant edit or schema-dependent behavior found in the evidence; the script fetches filings, not ledger workbooks. Replayed edits: 0.
- `_dev/tools/test_fetch_filing.py` — REBUILT classification (baseline retained; VM exactness unverified), no recovery change. No later relevant edit or schema-dependent behavior found. Replayed edits: 0.
- `_dev/tools/findings_text.py` — REBUILT. No complete snapshot or replayed edits; 2026-09-26 18:32:46 Bash shows the earlier implementation. Local change labels checker version and ledger rules when a report supplies them. Exact VM source equality unresolved.
- `_dev/tools/test_review_helpers.py` — REBUILT. No complete snapshot or replayed edits; 2026-09-26 19:03:45 Bash shows v1.14.1 schema expectation edits. Local tests cover crosswalk and findings label. Exact VM source equality unresolved.
- `_dev/tools/test_diff_workbooks.py`, `_dev/tools/test_findings_text.py` — absent; relevant helper tests are in `test_review_helpers.py`.
- No owned test fixtures required a change.

## Checks

- `python3 -m pytest _dev/tools/test_run_model.py _dev/tools/test_effort_sweep.py _dev/tools/test_fetch_filing.py _dev/tools/test_review_helpers.py -q` — **68 passed, 58 subtests passed**, 1.13 s.
- `python3 _dev/tools/diff_workbooks.py <Mac-Gray v1.13.2 export> <Mac-Gray v1.14.1 export> --crosswalk` — exit 0; 292 changes, saved to `/tmp/recov/work/D/mac_gray_v1132_to_v1141.diff.txt`.
- `python3 _dev/tools/diff_workbooks.py <Mac-Gray v1.14.1 export> <same export>` — exit 0; 0 changes, saved to `/tmp/recov/work/D/mac_gray_v1141_self.diff.txt`. Only one Mac-Gray v1.14.1 export was available in the snapshot.
- `python3 _dev/tools/check_lean.py --workbook <Mac-Gray v1.14.1 export> --filing raw_filing/mac-gray_2013-12-04_DEFM14A.htm --rules v1.14.1 --output /tmp/recov/work/D/mac_gray_v1141.check.json` — exit 0; checker 1.8 reported 0 errors and 2 warnings.
- `python3 _dev/tools/findings_text.py /tmp/recov/work/D/mac_gray_v1141.check.json /tmp/recov/work/D/mac_gray_v1141.findings.md` — exit 0; 2 findings written.
- `python3 _dev/tools/sandbox/run_model.py prepare --help` — exit 0; help names Opus 5.5 as default provider/model and Claude medium as default effort. Saved to `/tmp/recov/work/D/run_model_prepare_help.txt`.

No model runs, network calls, commits, or changes to evidence or data files.

## Fixes

Round-two review: `/tmp/recov/reviews/D_tools.round2.md` (ACCEPT-WITH-FIXES).

1. `_dev/tools/diff_workbooks.py` — D18: when a matched modern `Other-scope bid` has blank `Price low` and/or `Price high` where the legacy row has a value, crosswalk mode suppresses those cell-level differences and emits one aggregate count. It works in either workbook order. The test `test_crosswalk_counts_blank_other_scope_prices_in_both_directions` checks both directions. No Mac-Gray row met that D18 pattern, so its smoke diff has no D18 count.
2. `_dev/tools/diff_workbooks.py` — D11: workbook-level schema direction now reaches the Rounds comparison. `Late bids accepted` versus `Extended (late bid accepted)` carries `crosswalk: D11 (wider)` in either order. The test `test_crosswalk_marks_wider_deadline_choice_in_both_directions` checks both directions.
3. `_dev/tools/test_review_helpers.py` — added the two regression tests above. Both files remain REBUILT; the review cites the main-tree README read at 2026-09-26 20:45:16.451 as the evidence for these crosswalk requirements. Replayed edits: 0.

Post-fix checks:

- `python3 -m pytest _dev/tools/test_run_model.py _dev/tools/test_effort_sweep.py _dev/tools/test_fetch_filing.py _dev/tools/test_review_helpers.py -q` — **70 passed, 58 subtests passed**, 1.16 s.
- Mac-Gray v1.13.2 → v1.14.1 and reverse `diff_workbooks.py --crosswalk` — exit 0 each; 265 changes each, two `D11 (wider)` labels each. Files: `/tmp/recov/work/D/mac_gray_v1132_to_v1141.diff.txt`, `/tmp/recov/work/D/mac_gray_v1141_to_v1132.diff.txt`.

The first-pass 292-change smoke result above is superseded by the post-fix 265-change result. When Rounds started using the crosswalk, the smoke check exposed equal deadline values being reported as changes; the same issue already affected equal Conditions values. The fix labels changed cells only, removes those false positives, and still shows the two D11 differences.
