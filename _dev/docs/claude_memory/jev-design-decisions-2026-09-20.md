---
name: jev-design-decisions-2026-09-20
description: Decisions from Austin's discussion of Jev's role: checker not preprocessor, merge with mechanical script, revision loop next, corpus screening later
metadata:
  type: project
---

Full write-up in repo: `_dev/jev_checker/README.md`. Decisions with Austin (20 Sep 2026): Jev stays a post-extraction checker, never a filter in front of the extractor; merge `check_lean.py` and Jev into one command and one report (Jev step optional, exact checks stay in code); next experiment is a revision loop feeding flags back to the extractor; corpus-level screening is where cheap volume judgments pay if the sample grows. Unanswered: how many deals Austin and Alex plan. See [[typesafe-jev-rounds-2026-09-19]], [[user-plain-language]].

**Why:** reviewer time is the bottleneck, not extractor reading; a Jev miss as checker is harmless, as filter it becomes an error.
**How to apply:** build the merged checker first; do not run extractions or change the instruction without Austin's go-ahead.
