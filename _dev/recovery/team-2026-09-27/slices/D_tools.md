# Slice D — remaining offline tools updated for the v1.14 29-column schema
Files you own: `_dev/tools/sandbox/run_model.py`, `_dev/tools/test_run_model.py`, `_dev/tools/diff_workbooks.py`,
`_dev/tools/effort_sweep.py`, `_dev/tools/test_effort_sweep.py`, `_dev/tools/fetch_filing.py`,
`_dev/tools/test_fetch_filing.py`, `_dev/tools/findings_text.py`, `_dev/tools/test_review_helpers.py`, plus their test
fixtures, and `_dev/tools/test_diff_workbooks.py` / `test_findings_text.py` if they exist.

Goal: bring these to the VM's 26 Sep state. Evidence is thin: grep `/tmp/recov/all_calls_since_0924.jsonl` for each
file name (diffs in `git diff` output, test output, edit commands) and `/tmp/recov/evidence/_dev/tools/sandbox/run_model.py.json`.
Known facts: default extraction model is Claude Opus 5.5 at medium effort again (26 Sep); v1.14 ledger is 29 columns,
4 sheets (read the v1.14.1 instruction at `_dev/recovery/2026-09-27-cockpit/instructions/v1.14.1_08caed447f7d.md` for the
exact schema); tools must keep reading v1.13.2 workbooks.
Rules: apply only changes the evidence shows or that the v1.14 schema forces (a tool that would crash or mis-read a
29-column workbook). No speculative features. For each file, list the evidence events used and each change's reason.
Acceptance:
1. `python3 -m pytest` on the test files you own passes.
2. Smoke: `diff_workbooks.py` between a v1.13.2 and a v1.14.1 export of mac-gray from the snapshot, and between two
   v1.14.1 exports if available; `findings_text.py` on a v1.14.1 export; `run_model.py --help` (or its dry path) shows
   Opus 5.5 medium default. No live model calls. Outputs to `/tmp/recov/work/D/`.
