# Slice A — checker 1.8
Files you own: `_dev/tools/check_lean.py`, `_dev/tools/test_check_lean.py`, and any fixture files under `_dev/tools/` that
test_check_lean.py needs and that did not exist at 679d4fc (list them in your report).

Goal: rebuild checker 1.8 as it stood in the VM main checkout on 26 Sep evening: v1.13.2 rules plus v1.14.1 rules,
selected by instruction SHA-256 (`RULES_BY_INSTRUCTION`, including `8a93df3c…` for published v1.14.1; the v1.14
candidate / pilot hashes too if evidence shows them), 29-column v1.14 ledger schema, 4 sheets.

Evidence: `/tmp/recov/evidence/_dev/tools/check_lean.py.json` (full Reads in the v114 tree 26 Sep 18:32/18:53, then
Edits; then merge into main and the hash-table edit), `test_check_lean.py.json`, bash_mentions, and
`/tmp/recov/all_calls_since_0924.jsonl` (grep `check_lean`, `RULES_BY_INSTRUCTION`, `CHECKER_VERSION`).
Check `_dev/maintenance/2026-09-26-v1141-streamline/PIPELINE_UPGRADE_SPEC.md` and `PIPELINE_UPGRADE_REPORT.md`
content in evidence for the intended behaviour.

Acceptance:
1. `python3 -m pytest _dev/tools/test_check_lean.py -q` passes.
2. Reproduction against the cockpit: for every `raw/deal__*_version_*.json` in the snapshot whose `check.checker_version`
   is "1.8", run your checker on the matching exported `.xlsx` (`raw/deal__<slug>__export_version_<version>.xlsx`)
   with the instruction that version used (published v1.14.1 is `instructions/v1.14.1_08caed447f7d.md`) and the
   filing text available in the snapshot (`raw/filing__<slug>.json`) or `raw_filing/`. Compare errors/warnings counts
   and the individual issues (rule ids, rows) against the stored `check` object and any per-row check data in that
   JSON. Expected summaries: datalink 1 err/4 warn, mac-gray 0/2, providence-worcester 0/2, stec 1/3, synacor 0/6.
   Write the script you use to `/tmp/recov/work/A_repro.py` (scaffold, not in repo) and put a per-deal diff table in
   your report. Also run the checker on the v1.13.2 versions and report whether results match their stored checks
   (they may have been checked by an older version; say so).
3. The v1.13.2 path must still behave as at 679d4fc for v1.13.2 inputs (run the old test cases that remain).
Effort guidance: this is the hardest slice; be precise, replay edits exactly.
