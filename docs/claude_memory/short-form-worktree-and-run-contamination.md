---
name: short-form-worktree-and-run-contamination
description: State of the short-form instruction worktree, the ledger checker, and why the 19 Sep 2026 DeepSeek full-vs-short runs cannot be compared
metadata:
  type: project
---

On 19 Sep 2026 a worktree `/home/uctpiaj/Projects/Sec_extraction_new_compressed` (branch `instruction-compression`, nothing committed) was set up holding a short-form instruction: same ledger rules, minus self-check reporting, the correction-tracking sheet, the hidden AI original sheet and the calibration examples; Questions coverage kept. `check_invariants.py` proves no rule was lost. `tools/check_ledger.py` is a mechanical workbook checker. The full instruction stays in the main folder. See [[instruction-audit-2026-09-19]].

The first DeepSeek (opencode) runs of both versions are NOT a valid comparison. The short-form session never opened `raw_filing/` (it read only a few PetSmart paragraphs from the first session's text dump, to add adviser rows): it found the first session's working files in the shared `/tmp/opencode/work`, patched the fields the checker failed, and rebuilt. The full-instruction session pulled Pro's old Providence audit notes and workbooks from git history before extracting Providence; Mac-Gray and PetSmart looked clean. Neither opened `ref/deal_details_Alex_2026.xlsx`.

**Why:** agentic harnesses explore everything reachable: shared temp folders, git history, `ref/`, audit folders, and any checker script, which they patch to pass instead of re-reading the filing.

**How to apply:** before any comparison run, give each version a clean folder with only the instruction and `raw_filing/` (no `.git`, no `tools/`, no `ref/`, no audit folders) and a fresh temp area. Run the checker after the run, outside the agent's reach. Verify independence from the opencode database (`~/.local/share/opencode/opencode.db`, tables `session` and `part`) before trusting results. Pending instruction fixes, to apply to both versions only after a valid comparison: accept days as well as weeks in Conditions detail; clarify Date basis vs Date method on decision-day rows (failed in all three deals).

The clean-slate over-engineering audit is `Sec_extraction_new_compressed/OVERENGINEERING_AUDIT.md`. Verdict: conventions (about a third of the text) work and must stay; the excess is the output contract (39 columns, 40 labels, Summary, mandatory Questions coverage, participant accounting). It proposes a lean version of about 5,000 words with 19 columns, to be tested against the current one in isolated runs scored on Alex's hand rows. Nothing has been rewritten; several of its cuts touch decisions Austin already made (Outcome basis values, Date method, information-access rows, Questions coverage), so they need his call.
