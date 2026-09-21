# Development chronology

Current guidance is in [HANDOFF.md](HANDOFF.md); completed experiments live in git history at the commits named below. Entries describe the state at that time. Read removed material with `git show <commit>:<path>`; do not overwrite current files to inspect history.

| When | What | Outcome | Where |
|---|---|---|---|
| to mid-Sep 2026 | Pro's long instruction (39-column ledger), four Providence runs, Pro's review package | Starting point | commit `0780777` |
| 19 Sep | Instruction audit against Alex's documents; patch batches; over-engineering audit | Patch list; questions for Alex (`407a6e4:_dev/OPEN_QUESTIONS_for_Alex.md`) | `f1de7d9:_dev/instruction_audit_2026-09-19/` |
| 19 Sep | First DeepSeek full-vs-short runs | **Invalid**: runs could see other material | `f1de7d9:_dev/contaminated_runs_2026-09-19/` |
| 19 Sep | Clean sandboxed comparison of full, v1.5 and v1.8 instructions (DeepSeek, two run sets) | Versions tie on facts; v1.8 far cheaper to review; v1.8 adopted and patched | `f1de7d9:_dev/clean_run_comparison_2026-09-19/`, commit `c93d0a3` |
| 19 Sep | Blind model comparison on patched v1.8: Opus 5, GPT-5.6-Sol, DeepSeek; GPT-6-Astra graders | Opus 96.4, Sol 87.1, DeepSeek 86.6; Opus workbooks become canonical | report at `407a6e4:_dev/model_comparison/`; runs, logs, all nine workbooks, preflight in `f1de7d9:_dev/model_comparison_2026-09-19/` and `..._preflight_...`; commit `87aae86` |
| 19 Sep | Jev (TypeSafe) rounds 1–3 as post-extraction checker | Synthetic price swaps and some development omissions detected; prototype scope selected | reports at `407a6e4:_dev/jev_checker/`; code, cached API responses in `f1de7d9:_dev/jev_experiments_2026-09-19/`, `typesafe_followup_2026-09-19/`, `jev_round3_2026-09-19/`; early notes in `87aae86:_dev/jev_research_2026-09-19/` |
| 20 Sep | Tidy-up | Old 39-column checker `check_ledger.py` replaced by `check_lean.py`; stale folders removed | commit after `f1de7d9` |
| 20 Sep | Merged checker built | `check_lean.py` runs the mechanical checks, then the optional Jev step (`jev_pass.py`); one report. Reproduces round 3 on the Opus workbooks | `407a6e4:_dev/jev_checker/README.md` |
| 20 Sep | Five-deal checker/revision trial completed | Mechanical defects fixed, little substantive improvement; no Jev finding produced a workbook change | `407a6e4:_dev/revision_loop/` |
| 20 Sep | Convention recommendations, then instruction v1.9 | Adopted provisionally except Q3 and Q7 | `407a6e4:_dev/OPEN_QUESTIONS_recommendations_2026-09-20.md` |
| 20 Sep | Instruction v1.10 editorial tightening | Rule-inventory audit and fresh-reader conflict list | audit reports never committed; superseded by DECISIONS_v1.11.md |
| 20 Sep | Instruction v1.11 consistency pass with five Sol reviewers | Explicit participant/round/deadline/Question rules; protected Q3/Q7 decisions retained; no new extraction | `59e2325:_dev/DECISIONS_v1.11.md` |
| 20 Sep | Deep repo cleanup; Jev deleted | Historical material, run state and the Jev step removed from the checkout (no archive folder); tools repaired; checker v1.4 is mechanical only | this commit; earlier material at `407a6e4` and `f1de7d9` |
| 20 Sep | Eight blind Opus 5 extractions under v1.11 | All pass the mechanical checker; about $31 in total | workbooks in `extraction/` |
| 21 Sep | Eight-deal model review, pipeline research note, five-agent audit of both | Every bid price and date correct; 2–8% of rows per deal carry a consequential error (Meredith 12–15%), in counts, exits, round boundaries and conditionality. Staged pipeline not built | `git show acc9986:_dev/reviews/2026-09-21/README.md` (folder removed from the checkout) |
| 21 Sep | Instruction v1.12; checker v1.5; runner records tokens, cost and library versions; requirements pinned | General edits only; no extraction has tested v1.12 | [Decision record](`git show 3216a85:_dev/DECISIONS_v1.12.md`) |
| 21 Sep | Thirty-run comparison: v1.11, v1.12, v1.12.1 on DeepSeek flash (8 deals) and Opus (3 hard deals); runner gains a DeepSeek provider | Both new instructions beat v1.11 on Opus and tie each other; round maps unstable; DeepSeek right on prices, unreliable on judgment | [Comparison](`git show acc9986:_dev/reviews/2026-09-21/instruction_comparison.md`) |
| 21 Sep | Instruction v1.13: the objective-led rewrite becomes the working instruction, with a round defined as one request for offers | Untested as it now reads | [Decision record](DECISIONS_v1.13.md) |

The cleanup was committed with v1.10 and v1.11. The instruction and research inputs were unchanged by the cleanup itself.

Not in git: the command-line tools' own state folders from the comparison (caches and plugins, 643 MB, no research content) were deleted on 20 September 2026.
