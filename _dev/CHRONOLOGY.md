# Development chronology

Everything below except the current items was removed from the working tree on 20 September 2026 and lives in git history. To look at removed material: `git show <commit>:<path>` or `git checkout <commit> -- <path>`.

| When | What | Outcome | Where |
|---|---|---|---|
| to mid-Sep 2026 | Pro's long instruction (39-column ledger), four Providence runs, Pro's review package | Starting point | commit `0780777` |
| 19 Sep | Instruction audit against Alex's documents; patch batches; over-engineering audit | Patch list; questions for Alex (kept as `OPEN_QUESTIONS_for_Alex.md`) | `f1de7d9:_dev/instruction_audit_2026-09-19/` |
| 19 Sep | First DeepSeek full-vs-short runs | **Invalid**: runs could see other material | `f1de7d9:_dev/contaminated_runs_2026-09-19/` |
| 19 Sep | Clean sandboxed comparison of full, v1.5 and v1.8 instructions (DeepSeek, two run sets) | Versions tie on facts; v1.8 far cheaper to review; v1.8 adopted and patched | `f1de7d9:_dev/clean_run_comparison_2026-09-19/`, commit `c93d0a3` |
| 19 Sep | Blind model comparison on patched v1.8: Opus 5, GPT-5.6-Sol, DeepSeek; GPT-6-Astra graders | Opus 96.4, Sol 87.1, DeepSeek 86.6; Opus workbooks become canonical | report kept in `_dev/model_comparison/`; runs, logs, all nine workbooks, preflight in `f1de7d9:_dev/model_comparison_2026-09-19/` and `..._preflight_...`; commit `87aae86` |
| 19 Sep | Jev (TypeSafe) rounds 1–3 as post-extraction checker | Price and missing-event checks work on the development deals; not yet built | reports kept in `_dev/jev_checker/`; code, cached API responses in `f1de7d9:_dev/jev_experiments_2026-09-19/`, `typesafe_followup_2026-09-19/`, `jev_round3_2026-09-19/`; early notes in `87aae86:_dev/jev_research_2026-09-19/` |
| 20 Sep | Tidy-up | Old 39-column checker `check_ledger.py` replaced by `check_lean.py`; stale folders removed | commit after `f1de7d9` |

Not in git: the command-line tools' own state folders from the comparison (caches and plugins, 643 MB, no research content) were deleted on 20 September 2026.
