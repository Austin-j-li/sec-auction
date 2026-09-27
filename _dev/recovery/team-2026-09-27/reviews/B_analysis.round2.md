1. **Major — invented finality rule changes comparison results.** [_dev/tools/compare_alex.py:267](/Users/austinli/Projects/sec-auction/_dev/tools/compare_alex.py:267) requires `Announced as final` for codes ending in `Ann`. The recorded contract says `Ann` selects announcement **events**; finality remains final versus non-final. Evidence: `/tmp/recov/all_calls_since_0924.jsonl:740`, contract §11, original line 192.

   This incorrectly flags P&W’s Alex row 6045 against an `Inferred final` round. Conversely, `Final Round Inf Ann` incorrectly agrees with that finality. The reconstructed test at `test_compare_alex.py:129` enforces the error.

   **Fix:** use `recorded_finality in derive.FINAL` for all final-round codes, retain the event distinctions, and correct both test cases. An in-memory correction restores the pilot’s **27 agreeing events**, matching the historical VM record at JSONL line 1130; current code gives 26. Update the report’s finality claim and its statement that no historical event-status reference exists.

Verification: independently replayed the snapshots and subsequent edits. Both production tools and migration tests match exactly; analysis tests have only a Mac path-resolution adjustment and trailing-blank-line difference. All five analysis totals match the VM record, regenerated tables match the executor’s saved CSVs, and migration register/triage counts reproduce.

The pytest rerun was **blocked by sandbox permissions**: all 55 tests fail during temporary-directory setup. File-writing CLI smokes were likewise unavailable; their computation paths were exercised read-only in memory.

**Verdict: ACCEPT-WITH-FIXES**Orchestrator finding (after round-1 fixes), severity major:
Rerun of compare_alex.py on the 24 Sep v1.14 P&W pilot
(`_dev/recovery/2026-09-27-cockpit/raw/deal__providence-worcester__export_version_opus55-medium-20260924-2241-38bc24.xlsx`, `--rules v1.14`)
now gives event statuses 26 agree / 3 unaligned / 3 exit-other / 2 finality differs / 1 not compared / 1 disagree.
The VM recorded 27 agree / 3 unaligned / 3 exit-other / 1 finality differs / 1 not compared / 1 disagree (this matched before round 1).
Mac-Gray pilot still matches (32 agree / 2 exit-other). One P&W row moved from agree to "event agrees, round finality differs",
so the new final-round rule (Deadline / Deadline set / Deadline revised / Round opened distinction) is stricter than the VM's.
Fix: find the row, reconcile the final-round rule with the contract text in evidence so both pilots reproduce the recorded tallies,
and add a regression test. Outputs: /tmp/recov/work/B/pilot_recheck/.
