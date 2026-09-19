---
name: clean-run-comparison-2026-09-19
description: Sandboxed three-way test (full vs v1.5 vs v1.8 lean) of the deal-ledger instruction; where the harness, results and open calls live
metadata:
  type: project
---

On 19 Sep 2026 a clean comparison was run in `/home/uctpiaj/Projects/Sec_extraction_runs/`: full (13.6k words), v1.5 short form (11.7k) and v1.8 lean (5.5k, written by the audit agent, file `Sec_extraction_new_compressed/SEC_Deal_Ledger_Extraction_Instruction_v1.8_lean.md`), three deals, two runs each, DeepSeek flash max via opencode. Report: `COMPARISON.md` there. Follows [[short-form-worktree-and-run-contamination]].

Result: on bids, prices, formality, NDA counts, live bidders and order the versions are indistinguishable within run-to-run noise (about 1.5 points on a 0 to 10 score); v1.8 has a third of the words per row, 28% of rows flagged against 80 to 85%, 12 minutes against 18. Findings that held in both runs: v1.8 needs the Re-entered label back; all versions over-split rounds because "moves to definitive negotiation with selected bidders" fires before the exclusivity exception; v1.5 opened a spurious third PetSmart round; full's Providence edge is taught by its Providence examples.

**Why:** Austin suspected prompt bloat; the test shows the conventions matter and the output apparatus does not.

**How to apply:** v1.8 suspends several decisions Austin made (Outcome basis values, Date basis/method, Conditions detail, identity row, mandatory Questions coverage, information-access label); these are his calls, listed in a table in COMPARISON.md. Harness: `sandbox_run.sh` (bubblewrap, `--standalone`, key passed by environment, private XDG dirs), `launch.sh`, `relaunch.sh`, `resume.sh`; scoring in `score/` (blind labels, rubric, per-deal reference.md). opencode v2 keeps credentials in its database, not auth.json, and sometimes fails at start-up with "Model unavailable" or exits mid-task; retry and `--continue` handle both. Next step agreed in principle: held-out deals (Penford, sTec), which needs the filings; do not fetch from the web without asking.
