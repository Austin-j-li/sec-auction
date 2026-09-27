# Slice B — analysis and migration tools
Files you own: `_dev/tools/derive_analysis.py`, `_dev/tools/test_derive_analysis.py`, `_dev/tools/migrate_review.py`,
`_dev/tools/test_migrate_review.py`, `_dev/tools/compare_alex.py`, `_dev/tools/test_compare_alex.py`, plus fixtures
they need under `_dev/tools/` that did not exist at 679d4fc (list them).

Goal: rebuild as in VM main on 26 Sep evening.
- derive_analysis.py (0.3; T0–T3 formality readings over v1.14.x workbooks): full Read (~1037 lines) then 8 Edits at
  19:11–19:12 26 Sep — replay. Tests: full Read in v114 tree; check for later test edits.
- migrate_review.py (moves cockpit review edits/working copies from v1.13.2 to v1.14 schema): full Read (975 lines) then
  2 Edits — replay. Tests: full Read.
- compare_alex.py + test: no full content in evidence. Grep `/tmp/recov/all_calls_since_0924.jsonl` and `/tmp/calib/*.md`
  for `compare_alex` (65 hits): usage lines, CLI flags, output samples, test run output, the spec that commissioned it.
  Rebuild to match every observed CLI/output behaviour. It compares extraction workbooks with Alex's hand-coded deals
  in `ref/` (allowed here: this is pipeline evaluation, not an extraction run). Write a focused test file covering the
  observed behaviours.
Evidence files: `/tmp/recov/evidence/_dev/tools/{derive_analysis,test_derive_analysis,migrate_review,test_migrate_review}.py.json`.
Coordinate: `check_lean.py` is being rebuilt concurrently by another agent; if your code imports it, import only names
that exist at 679d4fc or are clearly defined in the evidence, and report the dependency.

Acceptance:
1. `python3 -m pytest _dev/tools/test_derive_analysis.py _dev/tools/test_migrate_review.py _dev/tools/test_compare_alex.py -q` passes.
2. Smoke: run derive_analysis on the five 26 Sep v1.14.1 rerun exports in `_dev/recovery/2026-09-27-cockpit/raw/`
   (`*_export_version_opus55-medium-20260926-*.xlsx`) and compare to any derive_analysis output recorded in evidence
   (the v1.14.1 retest README / analysis outputs); report matches/mismatches. Outputs go to `/tmp/recov/work/B/`, not the repo.
3. Smoke: run migrate_review against one v1.13.2 working copy from the snapshot in a dry-run / temp output; report.
