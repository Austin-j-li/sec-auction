# Recovery team record, 27 September 2026

Five slices were rebuilt on the laptop by Codex workers: GPT-6-Sol as executor, GPT-6-Astra as reviewer. omp orchestrated them from 12:16; Claude Opus 5.5 took over at about 12:45 and ran the final confirm reviews.

| Slice | Files | Final verdict |
|---|---|---|
| A_checker | check_lean.py 1.8, its tests | ACCEPT-WITH-FIXES (report timestamp only; fixed) |
| B_analysis | derive_analysis.py 0.3, migrate_review.py, compare_alex.py, tests | ACCEPT (round 3 confirm) |
| C_packets | root instruction v1.14.1, maintenance and review packets | ACCEPT (round 2 confirm) |
| D_tools | run_model.py, diff_workbooks.py, effort_sweep.py, fetch_filing.py, findings_text.py, tests | ACCEPT |
| F_docs | AGENTS, README, HANDOFF, _dev docs | ACCEPT (round 2 confirm) |

Orchestrator checks: `compare_alex.py` on the 24 Sep v1.14 pilots reproduces the VM's event tallies (P&W 27/3/3/1/1/1, Mac-Gray 32/2). `pytest _dev/tools` with `TMPDIR=/private/tmp`: 313 passed, 1 failed. The failure, `test_cockpit_runs.py::…foreign_pid_is_not_the_runner`, is in unchanged cockpit code and needs Linux `/proc`, so it can't pass on macOS.

Each file's provenance class (EXACT / REPLAYED / REBUILT) is in `reports/<slice>.md`. All of it must still be diffed against the VM tree when SSH returns. The raw evidence extracts (`/tmp/recov/evidence`, `all_calls_since_0924.jsonl`) were not kept here; they can be regenerated from `~/.claude/projects/ssh-*`.
