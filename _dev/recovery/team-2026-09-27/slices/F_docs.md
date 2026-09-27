# Slice F — current-state docs
Files you own: `AGENTS.md`, `README.md`, `HANDOFF.md` (root, new), `_dev/HANDOFF.md`, `_dev/CHRONOLOGY.md`,
`_dev/RESEARCH_QUESTIONS.md`, `_dev/COCKPIT_APP_SPEC.md`, `_dev/COCKPIT_BUILD.md`, `_dev/cockpit/README.md`,
`_dev/tools/README.md`.

Primary input: `/tmp/recov/work/E_facts.md` (cited fact sheet by the planner; §6 gives per-doc VM final edits and what each
must say now; §7 lists contradictions). Also the slice reports in `/tmp/recov/reports/` (A_checker, B_analysis, D_tools,
C_packets if present) for what the laptop now actually has.

Goal: bring each doc to the VM's 26 Sep ~21:00 state, where the evidence gives the VM's own wording (replay Edit/heredoc
deltas when their old text is present in the laptop file; otherwise write the new text from the fact sheet), then add the
laptop recovery facts that are true now:
- VM unreachable since the 27 Sep SSH certificate expiry; recovery branch `local-recovery-2026-09-27`; the cockpit on the VM
  is still live and remains the system of record for deal data and instruction versions.
- Root instruction file is now v1.14.1 (sha256 8a93df3c…66c98), copied from the cockpit snapshot with Austin's go-ahead on 27 Sep.
- What was rebuilt, its provenance (REPLAYED vs REBUILT) and its verification (e.g. checker 1.8 reproduces all 21 stored
  cockpit checks); what is lost (see `_dev/recovery/GAP.md`); cockpit app code for 24–26 Sep exists only on the VM.
- Reconciliation with the VM tree is required when SSH returns; laptop files marked REBUILT must be diffed against the VM's.
- `lesson/` is dropped (Austin: stale). Where the VM state named `lesson/` as an input to an open gate (migration registers),
  record the gate as open with its input to be decided; do not recreate `lesson/`.

Style: match the existing docs' voice (plain, factual, dated). Keep AGENTS.md short; it is read by extraction agents, so
the extraction section must remain correct for v1.14.1 (instruction version, `extraction/` still holds v1.13.2 workbooks).
Do not change `SEC_Deal_Ledger_Extraction_Instruction.md`. Do not document a claim the fact sheet marks uncertain as fact.
Acceptance: every state doc consistent with the fact sheet and with each other (versions, hashes, dates, defaults);
`python3 -m pytest _dev/tools -q -k "doc or readme or agents"` passes if such tests exist (report which ran).
List in your report each doc, what changed, and any fact-sheet contradiction you had to decide and how.
