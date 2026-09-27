Orchestrator finding (after round-1 fixes), severity major:
Rerun of compare_alex.py on the 24 Sep v1.14 P&W pilot
(`_dev/recovery/2026-09-27-cockpit/raw/deal__providence-worcester__export_version_opus55-medium-20260924-2241-38bc24.xlsx`, `--rules v1.14`)
now gives event statuses 26 agree / 3 unaligned / 3 exit-other / 2 finality differs / 1 not compared / 1 disagree.
The VM recorded 27 agree / 3 unaligned / 3 exit-other / 1 finality differs / 1 not compared / 1 disagree (this matched before round 1).
Mac-Gray pilot still matches (32 agree / 2 exit-other). One P&W row moved from agree to "event agrees, round finality differs",
so the new final-round rule (Deadline / Deadline set / Deadline revised / Round opened distinction) is stricter than the VM's.
Fix: find the row, reconcile the final-round rule with the contract text in evidence so both pilots reproduce the recorded tallies,
and add a regression test. Outputs: /tmp/recov/work/B/pilot_recheck/.
