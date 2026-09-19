---
name: typesafe-jev-rounds-2026-09-19
description: Three rounds of TypeSafe/Jev checker experiments on the nine graded workbooks; what worked, what to build, unmet gates
metadata:
  type: project
---

Three read-only Jev (jev-1.13.0) experiment rounds on 19 Sep 2026, in `_dev/jev_experiments_2026-09-19/`, `_dev/typesafe_followup_2026-09-19/`, `_dev/jev_round3_2026-09-19/` (each has RESULTS.md). Related: [[clean-run-comparison-2026-09-19]].

Round 3 findings: event-scoped price Choice (supported/contradicted/insufficient, built from Who/When/Event/ordinal, passage ±2 paragraphs, Note excluded) caught 185/185 planted price swaps on real rows, 0 false `contradicted`; the round-1 actor-only Noul passed 25/92 same-party swaps. Wider passages cause false flags. Sentence-level row-or-`none` selection found 5 of 8 graded omissions; `none` at confidence ≥0.9 gave 15 flags over nine workbooks, all truly absent.

Proposal (not applied, awaiting Austin): build `_dev/tools/jev_check.py` with a price pass and an omission pass, outside the extraction sandbox. No instruction change.

**Why:** Jev costs about a cent per workbook and returns calibrated typed answers; useful as reviewer queue, never as editor.
**How to apply:** Unmet gates before adoption: graded workbooks on unseen deals (Penford, sTec), a cheap generative-model control, repeat runs. Never store the TypeSafe key in files; pass via env var.
