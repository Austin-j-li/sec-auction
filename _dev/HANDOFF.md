# Handoff (19 September 2026)

**Working instruction:** `SEC_Deal_Ledger_Extraction_Instruction.md` is v1.8 lean (about 5,600 words), patched with the Re-entered label and the round-rule fix. The patched text has not been run yet.

**Why v1.8:** `_dev/clean_run_comparison_2026-09-19/COMPARISON.md`. Full (13.6k words), v1.5 (11.7k) and v1.8 tie on the facts within run-to-run noise; v1.8 costs a third of the review text. The three tested texts are in `_dev/clean_run_comparison_2026-09-19/instructions/`.

**To rerun:** `_dev/clean_run_comparison_2026-09-19/launch.sh <runset> <variant>` runs one sandboxed opencode/DeepSeek session per deal (needs bubblewrap, opencode with a DeepSeek key, Python with openpyxl, bs4, lxml; paths in `sandbox_run.sh` are for the Ubuntu laptop). Check outputs afterwards with `_dev/tools/check_ledger.py` (written for the 39-column schema) and the scripts in `_dev/clean_run_comparison_2026-09-19/score/`.

**History:** `_dev/instruction_audit_2026-09-19/` (audit against Alex's documents, patch batches, over-engineering audit). `_dev/docs/claude_memory/` is a copy of the assistant's project memory; on a new laptop copy it to `~/.claude/projects/<project-path>/memory/`.

**Next:** run patched v1.8 once on the three deals; test on unseen deals (Penford, sTec; filings needed); then the open convention questions for Alex listed at the end of COMPARISON.md and in `_dev/instruction_audit_2026-09-19/QUESTIONS_evaluation.md`.

`_dev/contaminated_runs_2026-09-19/` holds the contaminated 19 Sep runs, kept for the record only.
