# v1.14 implementation: report to Austin (V114_SPEC §7.14)

25 September 2026, about 23:59 UTC. Lead: Claude Opus 5.5.

All the work packages in §7 are built, reviewed and tested. They cover the instruction candidate and its review, the checker, the cockpit, the standalone tools, the migration and analysis tools, the documentation lines, and the deploy and release patches. The optional S4 is built too.

Nothing is deployed, published, committed or sent:
- no model or extraction run was made;
- no cockpit instruction version was created;
- no service was restarted or deployed to;
- no workbook, working copy, cockpit state, `extraction/` or `catalog.json` was edited;
- nothing was sent to Alex.

Every step from here is yours (§13).

## 1. The instruction candidate

- **File:** [SEC_Deal_Ledger_Extraction_Instruction_v1.14_candidate.md](SEC_Deal_Ledger_Extraction_Instruction_v1.14_candidate.md), 340 lines.
- **SHA-256:** `c2d47a479d09eb46d0ab9fbf887568fcf13e972e2e11acbf08d5cdfab468ab27`.
- **Header:** "**Revision of 25 September 2026, v1.14.**", frozen after review R.
- **Diff against the 24 September draft:** [v1.14_candidate.diff](v1.14_candidate.diff). The draft is unchanged (`f9595d74…`).
- **[CHANGELOG](CHANGELOG_v1.14_candidate.md):** every change with its source (a D-number, a §8 item or "Astra"). All 69 §3.1 lines and all 121 lines that audit C §1 names are listed as changed or confirmed unchanged: 74 changed, 47 confirmed. It also records the drafting choices the spec left open.

Drafting choices to note:
- Neutral numbers replace the deal-derived ones: "Ref: $20.00 close 02/08/2019; 25% premium" and "40–60".
- "Three weeks" replaces §4's "thirty days" in the H2 example, since it could not be confirmed that thirty days is not a filing's figure.
- The CVR example names the four condition columns rather than "components", since Antitrust takes Y or blank.
- There is no sentence about the SEC link. The pipeline adds it (D20), and such a sentence would be project text.

## 2. Review R and how it was resolved

[R_REVIEW.md](R_REVIEW.md). Five independent reviewers read the candidate, each through one lens:
1. definitions and consistency;
2. cascade coverage;
3. fidelity to the spec;
4. hygiene and value lists;
5. an extraction model's reading.

A consolidator verified and merged their findings: 27 kept (2 must-fix, 17 should-fix, 8 notes) and 8 rejected with reasons. The two must-fix findings were:
- **R16:** a sentence sent "consideration" columns to Not stated, which the checker rejects for prices.
- **R24:** E14's pre-check before inferring an exit blocked the very transitions it introduced.

All 27 were fixed, with each resolution in the CHANGELOG. An agent independent of both the writer and the fixer re-checked the result:
- every finding is resolved;
- the §9.1 checklist passes;
- the value lists agree with the finalized checker 1.7 and the cockpit choices (58 of 58 checks). The one intended difference is that the checker still accepts `Late bids accepted` with a warning.

The re-check left two notes:
- **RC1 (open, your call):** E14's lead-in could say more explicitly that when participation continues past one transition, the next one is tested. It is polish. Any edit changes the hash, so it belongs in a later draft (gate 7) or in a fix before gate 4 if you want it.
- **RC2 (done):** a stale CHANGELOG sentence about the checker's message, now fixed.

**Process slip.** While tracing a draft example, one R reviewer ran a recursive text search over `_dev/`. It printed two lines from `_dev/cockpit/state/instructions/`, which R was not authorized to read. Nothing was changed. The lines repeated draft text already in this folder. R_REVIEW.md records it.

## 3. Tests

Run in the separate worktree with `TMPDIR` under `/home/uctpiaj/work/tmp/v114-scratch/` ([evidence/final/tests.txt](evidence/final/tests.txt)):

| Suite | Command | 25 Sep baseline | Now |
|---|---|---|---|
| Unit | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s _dev/tools -p 'test_*.py'` | 199 | 292 pass |
| HTTP | `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider _dev/tools/cockpit/acceptance/test_http.py` | 14 | 20 pass |
| vitest | `(cd _dev/tools/cockpit/frontend && npx vitest run)` | 53 (counted; run on 25 Sep: 53 pass) | 77 pass, 8 files |
| Browser | the seven `acceptance/*.mjs` suites, against the worktree's built `dist/`, evidence folders under the scratch folder | not run | all pass: browser 60 checks, deals 25, instructions 24, runs 12, trace 14, resize, responsive; no browser errors |

- **One unexplained failure.** One full unit run in 21 had a single failure. My command kept only the summary line, so which test failed was not recorded. The 20 further runs all passed, 8 of them four at a time under load. It is not tied to a change I can identify.
- **Release state.** The worktree with `release/release-gate12.patch` applied passes 294 unit and 20 HTTP tests.
- **Acceptance evidence by package** is in `evidence/<package>/`:
  - S1's reproduction: every v1.13.2 workbook and stored v1.13.2 run result reproduces exactly under 1.7. The pilots change only as §7.3 documents: Mac-Gray gains 2 legacy and 2 D15-duplicate warnings and loses 2 `exit.inferred_reason` warnings; P&W gains 2 legacy warnings.
  - The S2 round trip, the S3 downloads, S5 relocation, the S7 cross-schema diff, the MIG-C rebase tests, and the P and MIG-T acceptance tests.
- **Not verified:** the deploy itself (§12) and a live smoke test, both yours to order.

## 4. Map re-check

[MAP_RECHECK.md](MAP_RECHECK.md), read-only. For each deal, one analyst checked the map and a separate skeptic checked the analyst; I verified the skeptics' points.

| Deal | What would change under §3 | Conflict with a recorded ruling |
|---|---|---|
| Kraton | Recommendation: two rounds. The 20 July admission and the final bid procedures letter become one round. | None. |
| Datalink | Recommendation: keep F9's round 1. | F9's recorded "five rounds" stands until you decide. Counting each stage once would give four rounds; that goes to Alex as Decision 1. |
| sTec | Recommendation: map A, with no round 3 and round 2 Announced as final. | None. Maps B (the current one) and C (Alex's voice note) go to Decision 1. |
| Synacor | The round map is unchanged. The changes come from D7 (Company E leaves the whole-company contest on 14 December) and D17 (Company B's talks become events outside the counts). | None. |
| Mac-Gray | Outcomes become Extended (late bid accepted), Extended (late bid accepted), Enforced. | None. Q7-A's prediction for 18 September holds. |
| PetSmart | 30 October becomes Enforced (reading A); Unclear stays the genuine alternative. | None. The 24 September revert keeps its facts. |

## 5. Replacement Questions for Alex

[Questions_for_Alex_2026-09-25.docx](Questions_for_Alex_2026-09-25.docx), SHA-256 `64ddad6cdb5935a62510157c42dd7e31bd5356f3dfd091a6307436ef6a3b4353`, 4,559 words (2,541 before the case appendix), 10 rendered pages. It was condensed from 6,013 words. It follows §5: what changed; 2a, five decisions for information; 2b, eight provisional rules to circle yes or no; the open decisions; and a case appendix with exact excerpts and printed pages.

Two independent checks were run: one after the first build, and one after condensing, which found two meaning losses and eight smaller problems, all fixed. Every excerpt is checked against the filings; I also checked the fixes and the three newly added filing quotes myself.

It is **not sent**. The original 24 September document is unchanged (`faab1d66…`).

**Rendering.** There is no Word or LibreOffice on the VM. The document was rendered through HTML and headless Chrome to page images and inspected there. Open it in Word before sending, to check page breaks and fonts. The build and render scripts are in `evidence/a2/`.

## 6. The separate working copy and the patches

- **Worktree:** `/home/uctpiaj/work/Projects/sec-extraction-v114`. It is detached at `679d4fc`, carries the live checkout's uncommitted diff, then waves 1–3.
- **Baseline of the live `_dev/tools/`:** `/home/uctpiaj/work/archive/v114-deploy/baseline-2026-09-25/`, taken at the moment the worktree was made. At about 23:45 UTC the live `_dev/tools/` still equalled it, as §12 step 1 requires.
- **Diff against the live `_dev/tools/`:** 61 files, +7,290 / −258 lines.
  - Changed files: the checker, the cockpit's data, workspace, worker, server, runs, trace and backup code, the frontend, the standalone tools and the tests.
  - New files: `provenance.py` (the Source sheet), `derive_analysis.py`, `compare_alex.py`, `migrate_review.py`, the frontend `choices.js`, `downloads.js` and `bulk.js`, their tests, and `cockpit/deploy/` (the reference unit files and the TMPDIR proposal).
- **Built `dist/`:** in the worktree (`index.html` SHA-256 `3691b1e4…c9a0`, `index-CuRy_YpQ.js`, `index-Dn1N504S.css`). It travels separately, as §12 step 8 says. The live `dist/` is untouched.
- **[release/deploy-tools.patch](release/deploy-tools.patch)** (SHA-256 `068b8ef747fd670c2aa99d23c4d4386f5b469ebf776544d416bd3c731bf6f26d`): the whole deploy, baseline → worktree, made with `git diff --no-index --binary` and applied with `git apply` from the live root.
  - Applied to a copy of the baseline, it reproduces the worktree exactly.
  - `git apply --check` from the live checkout passes; nothing was applied.
  - At the deploy, §12 steps 4–5 retake it after the README line-19 edit.
- **[release/release-gate12.patch](release/release-gate12.patch)** (SHA-256 `6a4be25a…eca1`): for gate 12. It is `d25-tools.patch` plus `tools-readme-release.patch`, and applies on top of the deploy tree.
  - `d25-tools.patch` was regenerated after wave 2, which added a test to the same file. The wave-1 version is kept for the record.
  - The gate-12 steps are in [release/README.md](release/README.md).

## 7. Proposed documentation lines outside `_dev/tools`

[release/PROPOSED_DOC_LINES.md](release/PROPOSED_DOC_LINES.md): each entry gives the exact current text and the exact replacement. An independent check fixed 14 problems in it and confirmed every quoted "current" passage against the live files.

| Part | Entries | When |
|---|---|---|
| Deploy | D1–D26 | §12 window step 9a |
| Release | R1 | gate 8, when the DOCX is sent |
| Release | R2–R12 | gate 9 |
| Release | G1–G12 | gate 12 |

The "now" lines were written in the checkout as D26 allows:
- the root README;
- HANDOFF;
- RESEARCH_QUESTIONS;
- CHRONOLOGY;
- the cockpit README;
- the Mac-Gray pilot README;
- `AGENTS.md` line 8, which now adds `lesson/` to the do-not-read list;
- this folder's README.

## 8. Pre-existing uncommitted work

21 patches in [pre-existing/](pre-existing/), one per file that `git status` showed as modified or deleted before any edit. Each was taken with `git diff --binary HEAD` and checked to reverse-apply exactly. Gate 0 can stage them with `git apply --cached`.

## 9. Analysis contract and the derive tool

[ANALYSIS_CONTRACT.md](ANALYSIS_CONTRACT.md) (version 0.1) and [analysis/](analysis/README.md) hold the derive tool's tables for:
- the Mac-Gray pilot;
- the P&W pilot;
- `extraction/mac-gray.xlsx` (v1.13.2);
- Mac-Gray's working copy, rendered from a backup-API copy of a read-only connection.

Every manifest is complete, and every Deadline outcome value gets a class. The side-by-side with Alex's `bid_type` aligns 13 of 13 Mac-Gray bids and 14 of 14 P&W bids, and reproduces audit D §3.4's counts:

| Reading | Mac-Gray | P&W |
|---|---|---|
| Recorded Formality | 13 of 13 | 11 of 14 |
| Formal and not Heavy | 11 of 13 | 14 of 14 |

No reading is the default. The research choices are switches with no default. A separate session's review prompted three hardenings:
- a basis label on the CVR package;
- no mechanical removal of a party's earlier whole-company participation;
- an inferred exit told apart from an inferred field.

## 10. Migration registers and the triage demonstration

[migration/](migration/README.md) holds registers for all eight edited deals. Their row marks equal the database's: 454 reviewed and 66 needs decision on 520 rows, making 1,561 facts. The aligner and triage were run on the two pilots against their working copies:

| Pilot | Agrees | Differs, rule changed | Differs, rule unchanged | Omitted or inserted |
|---|---|---|---|---|
| Mac-Gray | 130 facts (56 to accept after a spot check) | 3 | 2 | 37 |
| P&W | 130 facts (67 to accept after a spot check) | 14 | 4 | 39 |

Only supported facts that v1.14 leaves unchanged can be accepted. No bid row is ever ported as "reviewed", because its new columns were never reviewed. The port batches are prepared and never applied.

The live database, `catalog.json`, `extraction/` and the versions folder hash the same before and after the runs, and the tools open SQLite only read-only.

## 11. Audit findings

[DISPOSITIONS.md](DISPOSITIONS.md) covers all 314 findings of audits A–E:

| Disposition | Count |
|---|---|
| done | 160 |
| done, part open | 8 |
| not adopted | 3 |
| deferred to a gate or the backlog | 24 |
| applied to the spec before implementation | 101 |
| not applicable | 18 |

Its closing list gives each open item with its owner and gate.

## 12. Root disk

83% used, 1.6 GB free on `/`, against 97% (341 MB) on the spec's 25 September snapshot. The work volume `/home/uctpiaj/work` has 324 GB free after the scratch sandboxes were removed. Everything here was built on the work volume.

## 13. Open items

**Questions the spec left open:**
1. **P (analysis):**
   - Which Exit reason maps to Alex's DropM and which to DropBelowM? Audit D pairs them without saying, and his definitions are in `ref/CollectionInstructions_Alex_2026.pdf`, which P was not authorized to read.
   - Is the estimation data the raw v1.14 runs or the reviewed working copies?
   - Does a Stock % range that starts at 0 give all_cash 0 or missing? It gives 0 now, per S7's crosswalk.
   - Should the tool take the instruction version?
2. **MIG (gate 11):**
   - Should the port batch carry old row marks at all? It now ports "reviewed" only for fully supported, unchanged facts.
   - A batch over 100 operations, likely for Meredith: split it into several revisions, or raise the cap?
3. **S5 (gate 12.6):** if the v1.14 exports also become catalog entries, `verify_catalog.py`'s one-version-per-deal check must be relaxed in the same commit.
4. **OPS (§12 step 6a):** install the TMPDIR drop-ins in `_dev/tools/cockpit/deploy/PROPOSED-tmpdir.md`? If yes, one README sentence changes first.
5. **RC1:** the optional E14 lead-in polish (§2 above).
6. **The DOCX:** open it in Word; decide whether its length is right before sending. It is about 14% over the 4,000-word target set for the condensing. The facts that could still go are listed in `evidence/a2/README.md`.

**Small items:**
- This folder's README line 7 ("stays v1.13.2 and frozen") becomes false at gate 9, and no proposed line covers it. Add one at gate 9.
- The spec says "D1–D26" in its §0 table and in the gate-9 CHRONOLOGY template, although the decisions run to D27. The proposed lines use D1–D27; the spec is left as you wrote it.

**Other things to know:**
- **A separate session**, not this team, wrote three things on 25 September:
  - `_dev/maintenance/2026-09-25-staleness-cleanse/` (a review of the spec);
  - `RECOMMENDATION_REVIEW.md` in this folder, a redirect for Astra's links;
  - `sources/README.md`.

  Its implementation concerns about P and MIG were folded in (§9, §10).
- **S5** is not in §7.13's wave list. It ran in wave 1, because it has no dependency and gate 3 must deploy its lookup change.
- **S4** is built, and it counts as one of a save's 100 operations however many rows it sets.
- **Scratch.** The package sandboxes, merge bases and copies under `/home/uctpiaj/work/tmp/v114-scratch/` were removed once merged. The scratch folder keeps:
  - the agents' temp folders, which hold the A2 venv and the S1 reproduction inputs;
  - `patchwork/`, where the patches are made;
  - `browser-evidence/`;
  - the merge and patch scripts;
  - the wave result files.

**Your gates, in order (§13):**
- 0: commit the earlier work from `pre-existing/`.
- 1: accept this.
- 2: the pilot condition review, with Alex.
- 3: deploy (§12), with 3a to commit.
- 4: the cockpit draft.
- 5–6: the blind runs and their review.
- 7: settle the text.
- 8: send the DOCX.
- 9: publish and export.
- 10: re-extract.
- 11: move reviewed work.
- 12: `extraction/`.
- 13: records.
