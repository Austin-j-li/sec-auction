# What the laptop is missing from the Condenser VM, 27 September 2026

**Baseline.** The laptop and GitLab are both at `679d4fc`, cockpit phase 5, 23 September. The VM's `sec-extraction` checkout is on the same commit, with **91 uncommitted entries** (its `git status`, 26 Sep 20:43 UTC). The `sec-extraction-v114` worktree adds **74 more** (26 Sep 18:46). Nothing after 23 September was committed.

**Sources available on the laptop:**
- **S1:** the cockpit snapshot in `_dev/recovery/2026-09-27-cockpit/`.
- **S2:** local copies of the VM Claude transcripts, `~/.claude/projects/ssh-*`, 21–26 September, including subagent transcripts. The **24–25 September sessions that built v1.14, checker 1.7 and the cockpit changes are not among them.**
- **S3:** the live cockpit, read-only, while Access login works.

Recovery classes:
- **Done:** already on the laptop.
- **Exact:** the full text is in S2, from a Write or a complete Read, with no untracked change after it.
- **Near:** a full snapshot plus later Edit calls, or a merge; can be rebuilt, then must be checked against tests or hashes.
- **Rebuild:** only descriptions, diffs or partial reads exist; must be reimplemented.
- **Lost:** no content anywhere.

## 1. Instruction and research state

| Item | Class | Source |
|---|---|---|
| v1.14.1 as published (`8a93df3c…`), default | Done | S1 `instructions/v1.14.1_08caed447f7d.md` (hash verified) |
| v1.14 pilot draft (`f9595d74…`) | Done | S1 |
| v1.14 candidate (25 Sep, `c2d47a47…`, 15-run trial input) | Exact | S2: full Read of 341 lines on 26 Sep |
| v1.14.1 candidate as reviewed (`8bdb7c20…`) | Exact | S2: full Read of 354 lines |
| Root `SEC_Deal_Ledger_Extraction_Instruction.md` set to v1.14.1 | Done | Copied byte-exact from S1 at Austin's 27 Sep go-ahead; SHA-256 `8a93df3c…` verified |

## 2. Cockpit data

| Item | Class | Source |
|---|---|---|
| 13 deals: working copies, revision histories, comments, activity, jobs | Done | S1 |
| All 34 version workbooks, including the five v1.14.1 reruns and the 24 Sep pilots | Done | S1 |
| Filings for Medivation, Zep, Pepco Holdings, Imprivata | Done | S1 `raw/filing__*.json` |
| SQLite file, stored-file tree, user credentials (Claude/ChatGPT tokens) | Lost locally, still on VM | Not needed while the VM serves the cockpit |
| `~/backups/ledger-cockpit/` | Lost locally | VM only |

## 3. Offline pipeline code (`_dev/tools/`, not the cockpit)

| File | State on VM | Class | Evidence |
|---|---|---|---|
| `check_lean.py` (checker 1.8, picks v1.13.2 or v1.14.1 rules by instruction hash) | modified | Near | v114-tree full Read (1,882 lines, 18:32), then a merge into main and the `RULES_BY_INSTRUCTION` edit for `8a93df3c` |
| `test_check_lean.py` | modified | Exact (v114 tree) | full Read, 786 lines |
| `derive_analysis.py` (0.3, T0–T3 formality readings) | new | Near | full Read (1,037 lines), then 8 Edits at 19:11–19:12 |
| `test_derive_analysis.py` | new | Exact (v114 tree) | full Read, 556 lines |
| `migrate_review.py` | new | Near | full Read (975 lines), then 2 Edits |
| `test_migrate_review.py` | new | Exact (v114 tree) | full Read, 478 lines |
| `compare_alex.py`, `test_compare_alex.py` | new | Rebuild | no content in S2 |
| `sandbox/run_model.py` | modified (Opus default, v1.14 input handling) | Rebuild (small) | 70-line Read plus two diffs |
| `diff_workbooks.py`, `effort_sweep.py`, `fetch_filing.py`, `findings_text.py`, and their tests | modified | Rebuild | no content; likely 29-column schema updates |
| `README.md` (tools) | modified | Rebuild | none |

## 4. Cockpit application code (`_dev/tools/cockpit/`)

About 40 files: `server.py`, `worker.py`, `runs.py`, `workspace.py`, `data.py`, `deals.py`, `trace.py`, `backup.py`, `verify_catalog.py`, new `provenance.py`, 17 frontend sources (new `bulk.js`, `choices.js`, `downloads.js` and tests; `Records.jsx`, `Review.jsx`, `Runs.jsx`, `main.jsx`, `style.css` …), acceptance tests, `deploy/*.service`, and `dist/`.

**Class: Rebuild.** The transcripts only contain 23 September writes, which the phase 1–5 commit already supersedes. The 24–26 September changes were made in sessions whose transcripts are not on this laptop. What exists:
- the **built** frontend bundle, which can be downloaded from the live site (S3; minified, not source);
- the API responses in S1, which show the data model (29-column ledger, `choices`, `field_authors`, provenance, run versions).

## 5. Documents and packets (all untracked on the VM)

| Packet | Class | Recoverable from S2 |
|---|---|---|
| `_dev/maintenance/2026-09-24-bid-terms-taxonomy/` (taxonomy drafts 3–5, V114_SPEC, release/, migration/, evidence/a2 questionnaire builder and DOCX) | Mostly Rebuild | TAXONOMY_DRAFT3 (Write); `build_docx.py` (809-line Read, from before the 20:48 update); `release/PROPOSED_DOC_LINES.md` (823-line Read); `release/README.md` (123-line Read). **DOCX lost** (rebuildable from `build_docx.py` + the retest workbooks). |
| `_dev/maintenance/2026-09-25-staleness-cleanse/` | Lost | none |
| `_dev/maintenance/2026-09-26-astra-default-pro-verification/` | Partial | `DECISION_BRIEF_2026-09-26.md` (heredoc) |
| `_dev/maintenance/2026-09-26-v1141-streamline/` | Mostly Exact | V1141_SPEC (453-line Read), PIPELINE_UPGRADE_SPEC (Write + Read), PIPELINE_UPGRADE_REPORT, DEPLOY_RUNBOOK, CHANGELOG, retest/RETEST_PLAN, RELEASE_CHECKLIST (Writes). The status notes the 20:44–20:52 staleness agents added afterwards are Near. |
| `_dev/reviews/2026-09-26-v114-15-run-trial/` | Partial | grading/01–03, README, scores.csv (Writes); Pro review text (799-line Read). **The 15 trial workbooks are lost.** |
| `_dev/reviews/2026-09-26-v1141-retest/` | Partial | README (Write, later overwritten by the fork; its final text is in the fork transcript). Workbooks: Done via S1. Analysis outputs: regenerable once `derive_analysis.py` is rebuilt. |
| Root `HANDOFF.md` (new; the laptop version was later folded into `_dev/HANDOFF.md`) and edits to AGENTS.md, README.md, `_dev/HANDOFF.md`, CHRONOLOGY, RESEARCH_QUESTIONS, COCKPIT_APP_SPEC, COCKPIT_BUILD, `cockpit/README.md`, old packet READMEs | Rebuild | Only fragments; the current facts are known from S1 + S2, so rewrite rather than recover |
| `lesson/` | Dropped | Austin: stale, not wanted |

## 6. Consequences

- **What drives the work** (the v1.14.1 text, the five rerun workbooks, all review edits) is already on the laptop.
- **The offline checker and analysis for v1.14.1** can be rebuilt with fair confidence (§3 Near/Exact). This is what's needed to check or analyse any new extraction locally.
- **Rebuilding the cockpit application locally is not worth it** while the VM keeps serving. It would fork the live code, and the VM's version would conflict with it when SSH returns.
- Anything rebuilt locally should go on a separate branch, to be reconciled against the VM tree once SSH access returns.
