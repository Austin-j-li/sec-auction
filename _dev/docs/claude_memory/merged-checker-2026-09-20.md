---
name: merged-checker-2026-09-20
description: The merged checker exists; check_lean.py plus optional Jev step jev_pass.py, one report; what it reproduced and what is still unvalidated
metadata:
  type: project
---

Built 20 Sep 2026 on branch `jev-checker`, merged into `extraction-v2`. `_dev/tools/check_lean.py` runs mechanical checks, then (if `TYPESAFE_API_KEY` is set, or `--jev on` with saved answers) `_dev/tools/jev_pass.py`: event-scoped price check and sentence-level missing-event check, round 3 wording, `jev-1.13.0` pinned, cuts 0.9/0.75. Model judgments carry `basis: "jev"` and never change status or exit code. Saved answers live in `_dev/tools/.jev_cache/` (gitignored; restorable from `f1de7d9`). Usage and results are in `_dev/jev_checker/README.md`. See [[jev-design-decisions-2026-09-20]], [[typesafe-jev-rounds-2026-09-19]].

On the three canonical Opus workbooks it reproduced round 3's omission counts exactly and gave the same price answer on 36 of 36 rows when asked afresh.

**Why:** Austin decided one command, one report; Jev optional.
**How to apply:** still unvalidated on unseen deals (Penford, sTec filings needed), no generative-model control, cut-offs read off three deals. Not included: all-cash check, returned-draft reaffirmation rule. Next planned: compare flags with grading notes, then the revision loop with Austin's go-ahead. Austin pastes API keys into chat; use them inline via env var only, never in a file, and remind him to rotate.
