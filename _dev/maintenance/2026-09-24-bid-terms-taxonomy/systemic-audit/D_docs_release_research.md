# D. Documentation, release procedure and research consumers: v1.14 systemic audit

25 September 2026. Read-only audit. The only file written is this report. No services were contacted, no model was run, and SQLite was read through `mode=ro` URIs. I checked the live services with `systemctl --user is-active` / `show` only.

**Evidence convention.** A statement with a file:line citation, or marked (V), was checked in the tree, the database or Git. Statements marked (I) are my inference or recommendation. Every decision marked **[A]** is Austin's to take.

**Read in `ref/` (evaluation audit):**
- `deal_details_Alex_2026.xlsx`: headers, value domains, row counts per deal and red-font correction markers. I also aligned Mac-Gray and P&W bid rows to the pilot versions and recorded agreement counts only.
- `CollectionInstructions_Alex_2026.pdf`: full text.
- `alex_voice_notes_2026-08.docx`: text search for the price and estimation passages.
- `seed.csv`: identifying columns.

Outside the repo I read `…/sec-v114-recommendation-review-2026-09-25/sources/qa.txt` and `questions.txt`. No hand-coded values are reproduced here.

**`lesson/`** is untracked. It holds 166 files (7.4 MB) created 23–24 September:
- the Astra eight-deal review, with lesson files, per-deal traces keyed to working-copy UIDs, and the recovered operating history;
- the five-reviewer independent audit (`lesson/independent-audit-2026-09-23/`): inventories, verdict CSVs, proposals R1–R4 and recommendations;
- the 24 September revert record;
- the 22 and 24 September Questions for Alex DOCX files.

It is evaluation material ("do not expose them to a blind extracting model", `lesson/README.md:3`). Neither AGENTS.md nor the README tells an extracting agent to avoid it (row 1 below). It is not in `.gitignore`, so `git add -A` would commit it.

---

## 1. Stale statements

Classes:
- **NOW**: update now, describing the candidate as not deployed.
- **DEPLOY**: update when the separate working copy's code goes live.
- **REL-D**: update at publish/default.
- **REL-X**: update at repository export.
- **HIST**: leave alone.

V114_SPEC §0 (lines 53–56) lets agents write only this folder, `_dev/HANDOFF.md` and `_dev/RESEARCH_QUESTIONS.md` in the checkout. Every other NOW row needs Austin's scope approval **[A]**.

| # | file:line | Statement | Class | Proposed text or action |
|---|---|---|---|---|
| 1 | AGENTS.md:8; README.md:36 | Do-not-read list: `_dev/`, `ref/`, other workbooks, git history | NOW [A] | Add `lesson/`. It holds hand-coding-derived evaluation material. |
| 2 | AGENTS.md:12 | "the working instruction (v1.13.2, frozen)" | REL-X | "the working instruction (v1.14, frozen; exported on <date> from the cockpit's published `v1.14`, SHA-256 `<sha>`). Agents edit it only with Austin's approval… `export_repo.py` writes it for a commit Austin requests." |
| 3 | AGENTS.md:14 | extraction/ "made by Claude Opus 5.5 at medium effort under v1.13.2 on 22 September… catalog.json holds one immutable version per deal, these nine extractions" | REL-X | Rewrite per the catalog decision (§2.5). Name the v1.14 packet, and the archive path of the v1.13.2 originals, which remain the bases of the edited working copies. |
| 4 | AGENTS.md:16 | Points to RESEARCH_QUESTIONS and CHRONOLOGY only | REL-X | Add the v1.14 decision record (V114_SPEC folder, or a `_dev/DECISIONS_v1.14.md`). |
| 5 | README.md:12, :17 | "Current state (23 September 2026)"; "Austin's source review of the nine workbooks is pending" | NOW [A] | 25 September state: eight working copies are edited and audited; the v1.14 candidate is in preparation and is not published or deployed. |
| 6 | README.md:14, :23 | "v1.13.2 and is frozen"; table "v1.13.2 (frozen)" | REL-X | v1.14. |
| 7 | README.md:15 | "nine blind extractions… under v1.13.2… unreviewed" | REL-X | Per the catalog decision. |
| 8 | README.md:5, :16 | "four sheets"; cockpit "exports Excel" | DEPLOY | "The ledger has four sheets. A downloaded working copy adds a `Source` sheet with the EDGAR link and provenance (D20)." |
| 9 | HANDOFF.md:1 | "— 23 September 2026" | NOW | 25 September. |
| 10 | HANDOFF.md:5 | "The working instruction is **v1.13.2, frozen**." | NOW, then REL-X | Now, add: "A v1.14 candidate is being prepared under `maintenance/2026-09-24-bid-terms-taxonomy/V114_SPEC.md` (D1–D21). It is not published, not the cockpit default and not deployed. Unpublished draft `a4ca26ecfa92` holds the 24 September draft." At export: v1.14. |
| 11 | HANDOFF.md:11–23 | Session state at 23 September 18:10, including :14 "Alex has not yet connected or run" | NOW | Replace with the current state. (V) Alex connected Claude on 24 September at 09:19 UTC and has made no run; all 8 extraction jobs are Austin's. `ledger-cockpit` has run the uncommitted tree (checker 1.6, deal-review status, `dist/`) since the 24 September 22:02 UTC restart. |
| 12 | HANDOFF.md:27 | "nine deals, each with one immutable version… None has been reviewed." | NOW | "Thirteen deals: the nine catalog deals plus Medivation, Zep, Pepco Holdings and Imprivata, each added deal with one v1.13.2 run version. Run versions also exist for PetSmart (23 September) and for the Mac-Gray and P&W pilots (24 September, v1.14 draft). Eight working copies are edited. Latest revisions: Mac-Gray 8, P&W 16, PetSmart 2, sTec 1, Penford 2, Synacor 1, Kraton 4, Meredith 4; Datalink none. No deal-level review status has been recorded." (V, DB) |
| 13 | HANDOFF.md:32 | Mac-Gray: "the current draft is not yet revised to it" | NOW | "R01 is applied in the working copy (revisions 6–7, 23 September); the raw version is unchanged." (V: revision reasons) |
| 14 | HANDOFF.md:33 | Seven deals: "Austin's source review is pending" | NOW | "Edited 23 September (Astra-assisted); independently audited (`lesson/independent-audit-2026-09-23/`); three clusters reverted 24 September." |
| 15 | HANDOFF.md:46 | "The only working extraction instruction; v1.13.2." | REL-X | v1.14. Also give the cockpit default. |
| 16 | HANDOFF.md:48 | extraction/ "…the cockpit's only versions" | NOW, then REL-X | Now: drop "the cockpit's only versions", since run versions exist. At export: per the catalog decision. |
| 17 | HANDOFF.md:55–56 | Maintenance list ends at 22 September | NOW | Add `2026-09-23-cockpit-phase1…5` and `2026-09-24-bid-terms-taxonomy`. |
| 18 | HANDOFF.md:64 | "…XLSX export" | DEPLOY | Add the Source sheet (S3), schema-aware choices (S2) and checker 1.7 (S1). |
| 19 | HANDOFF.md:77 | "Austin reviews the nine current workbooks… including applying the Mac-Gray R01 decision" | NOW | Next work is V114_SPEC §7 and this report's §2. |
| 20 | CHRONOLOGY.md, after :45 | No rows after 23 September | NOW [A] | Add dated rows: phases 1–5 (commits `e4b06db`…`679d4fc`); first cockpit runs (PetSmart, Medivation, 23 September); the eight-deal Astra review (23 September); the independent audit (23–24 September); the revert (24 September); Zep, Pepco and Imprivata added and run (24 September); the 24 September Questions DOCX; taxonomy confirmed, checker 1.6 deployed 22:02 UTC and pilots run 22:41 (24 September); V114_SPEC (25 September). |
| 21 | CHRONOLOGY.md:42 | "The current Opus 5.5 Mac-Gray draft is not yet revised to it" | HIST | Leave. The new 23 September row records R01 in revisions 6–7. |
| 22 | CHRONOLOGY.md (new row) | — | REL-D / REL-X | Row text in §2.4. |
| 23 | RESEARCH_QUESTIONS.md:3 | "The working instruction is v1.13.2" | NOW, then REL-X | Now: "…v1.13.2. The v1.14 candidate (V114_SPEC) adopts the final and provisional answers below; it is unpublished." At export: v1.14. |
| 24 | RESEARCH_QUESTIONS.md:18 | "…Mac-Gray draft… has not been revised" | NOW | "Applied in the working copy (revisions 6–7). v1.14 makes it the general E10 rule (D13, final)." |
| 25 | RESEARCH_QUESTIONS.md:19 | Datalink F9 "the verified revision implements the ruling" | NOW | Add: that revision was on the earlier Opus 5 draft. The current draft has four rounds (re-extraction README:67). F9 stands until Austin decides under D8, and package M re-checks it. |
| 26 | RESEARCH_QUESTIONS.md:27–31 | Five "provisional conventions for Alex" | NOW | Item 1 (process boundaries): E5/D8 and Decision 1. Item 2 (sTec rounds): Decision 1. Item 3 (formal timing): D9, provisional (Alex Q5). Item 4 (WDC 10 June): D9 plus express incorporation. Item 5 (Penford Party A): the Part 2 reading is still open (§5). |
| 27 | RESEARCH_QUESTIONS.md:33 | Source hierarchy | NOW | "Open; in the replacement questions (V114_SPEC §5)." |
| 28 | RESEARCH_QUESTIONS.md:37 | "reference share prices with their own dates" | NOW (minor) | Add: filing-reported references stay in Notes (E13); a market series is backlog item P2 (§5). |
| 29 | tools/README.md:19 | Checker paragraph: "v1.14 (draft)…" and its rule list | DEPLOY | Written with S1 in the separate copy: version 1.7, Antitrust error, blank prices on Other-scope rows, two Deadline-outcome sets and the `Late bids accepted` warning. |
| 30 | tools/README.md:49 | Importer builds "one version per deal… `extraction/<deal>.xlsx`" | REL-X | Only if the catalog is relocated. Name the new paths and the updated importer and verifier. |
| 31 | tools/README.md:118 | Deal export uses "the same bytes as the cockpit's Excel download" | DEPLOY | After S3 this holds only for version downloads without the Source option. The working-copy download gains a Source sheet; `Workspace.export` does not. |
| 32 | tools/README.md:120 | "…in practice only added deals can be exported" | REL-X | After relocation, catalog deals' `extraction/<slug>.xlsx` becomes exportable. |
| 33 | tools/README.md:111–112 | Example `instruction v1.14` | — | Becomes correct once the version is published under that name. |
| 34 | cockpit/README.md:9 | "…None has been reviewed." | NOW [A] | "Eight working copies have edits (see History); no deal-level Review status is set." |
| 35 | cockpit/README.md:13 | Mac-Gray "The displayed extraction has not yet been revised to it." | NOW [A] | "The raw extraction is unrevised; the working copy applies R01 (revisions 6–7)." |
| 36 | cockpit/README.md:20 | "export Excel when needed" | DEPLOY | Source sheet; version-download option; schema-specific choices; S4 bulk Process/Round edit, if built. |
| 37 | cockpit/README.md:42 | "v1.13.2… was imported as the first published version and the default." | REL-D | Add "v1.14 was published on <date> by <person> and made the default on <date> by <person>." |
| 38 | COCKPIT_BUILD.md:47 | `choices`: "allowed labels from the checker" | DEPLOY | "…for the deal's `ledger_schema`" (S2). |
| 39 | COCKPIT_BUILD.md:69 | Working export: "Preserve four sheets" | DEPLOY | The working-copy download adds a fifth `Source` sheet. `Workspace.export`, which `export_repo.py` and `verify_catalog.py` use, stays four-sheet. |
| 40 | COCKPIT_BUILD.md:73 | "Since 22 September each deal has one version… default base" | REL-X | Per the catalog decision. Run versions come from the `versions` table. |
| 41 | COCKPIT_APP_SPEC.md:92, :112, :185, :193–194 | v1.13.2 examples; repository "stays v1.13.2 until someone deliberately exports" | HIST | Approved design record; still accurate as design. |
| 42 | maintenance README:7 | "…which stays v1.13.2 and frozen. To use it, start a draft… and paste this text." | NOW (2nd sentence); REL-X (1st) | Now: "It is cockpit draft `a4ca26ecfa92`. The v1.14 candidate (A1) supersedes it." |
| 43 | maintenance README:11–13 | "check_lean.py 1.6… all five cockpit run versions" | HIST | Dated deploy record. Add a line for 1.7 at DEPLOY. |
| 44 | maintenance README:26 | bid_type comparison | HIST (verified, §3.4) | Optional note: Mac-Gray and P&W are among the nine deals Alex corrected (red font); for Kraton, Meredith, Synacor, Datalink and Pepco, his workbook holds uncorrected Chicago coding. |
| 45 | maintenance README:28 | "Next: …review the two versions' condition columns by hand; then decide whether to publish the draft." | NOW | "Superseded by V114_SPEC §7/D21: the pilots are superseded drafts; the candidate, not the draft, is what may be published." |
| 46 | maintenance README:30–41 | Deliverables list | NOW (as packages land) | Add the candidate hash, CHANGELOG, R findings, MAP_RECHECK, the DOCX and `systemic-audit/`. |
| 47 | reviews/2026-09-21-mac-gray-pilot/README.md:3 | "not frozen or research-ready while R01 remains for Austin"; "the cockpit shows only that draft" | NOW [A] | R01 was decided on 22 September (`acceptance/RESEARCH_DECISION.md`) and applied in working copy revisions 6–7. The cockpit also holds the 24 September pilot version. |
| 48 | reviews/2026-09-21-datalink-pilot/README.md:3 | "the current `extraction/datalink.xlsx` is a different, newer Opus 5.5 medium draft" | REL-X | Name the v1.14 file and the relocated v1.13.2 original. |
| 49 | reviews/2026-09-22-opus55-reextraction/README.md | Whole file | HIST | — |
| 50 | lesson/README.md:3, :5–14 | "reviewed event by event by Astra-only subagents at xhigh"; "Final revision" PetSmart 1, Kraton 3, Meredith 3 | HIST | Superseded twice: the audit calls the process claim "overstated" (audit README §1.1), and live revisions after the revert are 2, 4 and 4 (V). `revert-2026-09-24.md` declares the lesson files pre-revert records. If `lesson/` is committed, add a pointer file rather than editing. |
| 51 | lesson/…/questions-for-alex/README.md:5 | 24 September DOCX is "the current version" | REL (when Austin sends A2) | Add the replacement's hash and date. |
| 52 | frontend/src/runs.js:6 (used :51, :141–142) | `INSTRUCTION_VERSION = 'v1.13.2'` fallback label | DEPLOY (software slice) | Derive it from the default instruction. |
| 53 | cockpit/import_results.py:23–36, :217; verify_catalog.py:73, :75, :83 | Hard-coded nine deals, `extraction/{deal}.xlsx`, v1.13.2 hash, revision 0 | REL-X | Change together with the catalog (§2.5). |

---

## 2. Release procedure

### 2.1 How past versions reached the file (V)

- **v1.8 to v1.12.1** were committed directly: `c93d0a3`, `407a6e4`, `59e2325`, `3216a85`, `f89170c`.
- **v1.13** was committed in `1657676` (6-line diff) on branch `instruction-v1.12.1` and merged in `d3a5b2b`. The next commit, `33dcc88`, updated AGENTS.md. The decision record is `_dev/DECISIONS_v1.13.md` (CHRONOLOGY:24).
- **v1.13.1** was never committed and no run used it (DECISIONS_v1.13.md:17, :27).
- **v1.13.2** was approved by Austin (DECISIONS_v1.13.md:18, :33–37). It reached Git in the consolidation commit `03d59b1` (22 September), together with AGENTS.md, CHRONOLOGY, DECISIONS_v1.13, HANDOFF and the catalog. It has been SHA-256 `513c8e3e…` ever since.
- **The cockpit imported the file** once, on 23 September at 16:58 UTC. It became published `v1.13.2`, set by `system`, and the default (`instructions.py:88–109`; DB).
- **No version has yet gone from the cockpit to the repository.** `export_repo.py` (commit `679d4fc`) has been exercised only on fixtures (`test_cockpit_export.py`).

### 2.2 What `export_repo.py` does (V)

**Instruction exports:**
- It resolves a 12-character id or a case-insensitive name (:83–86) and refuses drafts (:87–88).
- It checks the stored text against its hash (:94–95) and writes the bytes verbatim to `SEC_Deal_Ledger_Extraction_Instruction.md` (:96, :166–171).
- By default it is a dry run. It never commits.
- The catalog guard (:148–153) never blocks an instruction, because the catalog names no instruction path.

**Deal exports:**
- The workbook bytes come from `Workspace.export(slug, version)` and go to `extraction/<slug>.xlsx`.
- For an added deal, it also writes the filing and a `MANIFEST.csv` row (:126–142).
- It refuses any path the catalog names. The catalog names all nine `extraction/<slug>.xlsx` files, so every catalog-deal export is refused today.

### 2.3 Who may change the file (V)

AGENTS.md sets three rules:
- :12: "Agents edit it only with Austin's approval… the app never changes this file."
- :21: an app version "reaches the repository only through `_dev/tools/cockpit/export_repo.py`, run for a commit Austin requests."
- :22: outside the app, an agent changes the instruction only with Austin's approval, and only for general changes.

Either Austin or Alex may publish a version or change the default in the app. The repository file changes only at Austin's request.

### 2.4 Proposed procedure

It revises V114_SPEC §7's gate order (see §7, item 1).

| # | Step | Type | Detail |
|---|---|---|---|
| 0 | Commit the live but uncommitted work separately | **[A]** decides; M executes | The checker 1.6 taxonomy work, the deal-review status feature, `dist/` and the docs. This keeps the release diff limited to v1.14. |
| 1 | Accept the candidate (gate 1) | **[A]** | Prerequisites: A1 hash, diff and CHANGELOG; R resolved; `MAP_RECHECK.md`. |
| 2 | Fix the header before the draft exists | **[A]** | §3 of the spec sets "v1.14 (candidate)". Published text is immutable (`instructions.py:213–214`) and is exported verbatim, so a header edit after evaluation changes the hash. (I) Recommend the final header "Revision of <date>, v1.14." now, so that the evaluated text is byte-identical to the published and exported one. |
| 3 | Deploy S1–S3 before any run (moved from gate 7) | **[A]** commands; M executes | Reasons in §7, item 1. Checks: read the `jobs` table (`mode=ro`) for queued or running jobs; run `backup.py create`; build beside `dist/` and swap; restart both services; verify (tools README:130–139); confirm that v1.13.2 receipts reproduce. |
| 4 | Create the cockpit draft (gate 3) | **[A]**, Austin in person in the app (attributed) | "New draft from" published `v1.13.2`, so the editor's parent diff reads v1.14 against v1.13.2. Paste the text and save. M: confirm the draft's SHA-256 equals the candidate file's. **[A]** Leave or ignore the unused draft `73f21eb8c09a`, whose text is unchanged v1.13.2 (V). |
| 5 | Evaluation runs (gate 4) | **[A]** chooses deals, engine and effort, one run each, and the budget | Precedent: $27.69 for nine Opus 5.5 medium runs; the pilots cost $2.78 and $2.82. M: record run ids in a new packet and copy receipts from `_dev/cockpit/state/versions/<deal>/<id>/`. That path is ignored by Git, and `export_repo.py` copies workbooks only. |
| 6 | Review (gate 5) | **[A]** and Alex | §6. |
| 7 | Settle the text | **[A]** | Unchanged: publish this draft. Changed: new draft, rerun the affected deals, or accept an unevaluated diff. |
| 8 | Send A2 to Alex | **[A]** | (I) Sending before step 9 lets his answers reach v1.14 rather than v1.14.1. By design (§1 of the spec, "Provisional") it can also follow publication. |
| 9 | Publish as `v1.14`, then Make default (gate 6) | **[A]**, in person in the app | Publishing only renames the draft and sets its status; id and hash stay the same (`instructions.py:235–244`). Runs already made on the draft keep their "draft …" label and a NULL `instruction_version` (`worker.py:348–354`). Compare still treats equal hashes as the same instruction. |
| 10 | Export the instruction | **[A]** requests a commit; M executes | `export_repo.py instruction v1.14` (dry run: `513c8e3e… -> <sha>`), then `--write`, then verify the hash. Update the docs marked REL-X in rows 2, 4, 6, 10, 15 and 23, and add the CHRONOLOGY row. (I) Do this at step 9: until then, CLI runs use the repository file (`run_model.py:264`) while the app uses v1.14. |
| 11 | Re-extract (gate 8) | **[A]**: which deals; whether step-5 runs count | If the text is unchanged, step-5 runs are already v1.14 runs (same hash). Extract only the remaining deals, and redo the two pilots, which ran on the 24 September draft (`f9595d74…`). M: packet with receipts. |
| 12 | Working copies | **[A]**, per deal | §6: rebase onto the v1.14 run and port the review, or keep the v1.13.2 working copy until the port is done. |
| 13 | Catalog and workbook export (gate 9) | **[A]** chooses the §2.5 option; M executes | Then update AGENTS:14, README:15, HANDOFF:48, tools README:49 and :120, COCKPIT_BUILD:73 and the Datalink packet README:3. Run the tests and `verify_catalog` (after it is fixed) and take a backup. |
| 14 | Records and staging | **[A]** | Commit this folder or write `_dev/DECISIONS_v1.14.md`. Decide whether to commit `lesson/`. Stage paths explicitly; no `git add -A`. |

**Proposed CHRONOLOGY row (REL):**

> | <date> | v1.14 published in the cockpit as `v1.14` (id `<id>`, SHA-256 `<sha>`) by <person> and made default by <person>; exported to `SEC_Deal_Ledger_Extraction_Instruction.md` at Austin's request | Decisions D1–D21 of 25 September; consistency review R; checker 1.7 and cockpit S2/S3 deployed <date>; <n> evaluation runs, reviewed against the edited v1.13.2 working copies; provisional decisions sent to Alex <date/not yet> | [V114_SPEC](maintenance/2026-09-24-bid-terms-taxonomy/V114_SPEC.md), packet `<…>` |

**Proposed AGENTS.md Layout edits (REL-X):**
- :12: as in row 2.
- :14: "`extraction/`: blind extractions under v1.14 by <model/effort> on <date> (`_dev/reviews/<packet>/`). The 22 September v1.13.2 extractions, which are the bases of the edited cockpit working copies, are at `<archive path>` and stay in `_dev/cockpit/catalog.json`." Adjust to the option chosen.
- :16: add the v1.14 decision record.
- :8: add `lesson/` (this is NOW, row 1).

### 2.5 `extraction/` and `catalog.json`

**Constraint (V).** A version resolves by `path` and is re-hashed on every read (`workspace.py:162–168`). A working copy is tied to `base_id` plus `base_sha256` (`workspace.py:179–186`). Overwriting `extraction/<slug>.xlsx`, even with the catalog guard lifted, would therefore break every working copy on that base. Eight deals have one. Choose **[A]** among:

- **(a) Relocate (I, recommended).**
  1. `git mv` the nine originals, bytes unchanged, for example to `_dev/reviews/2026-09-22-opus55-reextraction/workbooks/`.
  2. Edit only `path` in the catalog. Keep the id `opus55-medium`, the `sha256` and `instruction_version: v1.13.2`.
  3. In the same commit, update `import_results.py` (it would otherwise regenerate the old paths) and `verify_catalog.py` (:73, :75, :83).
  4. Then run `export_repo.py deal <slug> --version <v1.14 id> --write`.
  5. Decide whether to add the repository copies to the catalog. Adding them makes the committed file the durable cockpit version but duplicates the run version. Leaving them out keeps one entry, and the run version then lives only in the ignored state and its 14-day backups.
- **(b)** Keep `extraction/` at v1.13.2 until reviewed v1.14 working copies exist, and state in AGENTS:14 that it predates the current instruction.
- **(c)** Export reviewed working copies (`--version working`) instead of blind runs. AGENTS:14 calls `extraction/` "blind extractions", so that wording must change.

### 2.6 Held-out deals (Medivation, Zep, Pepco, Imprivata)

**Facts (V):**
- All four are cockpit-added deals with one unreviewed v1.13.2 run and no working-copy revisions.
- Zep and Imprivata ran at Opus 5.5 **xhigh**; Medivation and Pepco at medium.
- Medivation, Zep and Imprivata are among the nine deals Alex hand-corrected. Pepco is not.
- Medivation, Zep and Pepco were read when designing the taxonomy (§7, item 2).

**Procedure:**
- **[A]** Run them in step 5 at medium, one run each, and do not expose v1.14 review findings to anyone building later instruction changes.
- **[A]** Whether to export them. `export_repo.py deal <slug>` writes `extraction/<slug>.xlsx`, the filing to `raw_filing/` and a MANIFEST row (:126–142), which turns them into repository development deals. (I) Keep them cockpit-only until any evaluation claim based on them is recorded.

### 2.7 `ref/seed.csv` and `raw_filing/MANIFEST.csv`

- **`seed.csv`: no change.** It holds identifying columns only, built by `make_seed.py` from Alex's workbook; do not rerun. Its `index_url` equals the MANIFEST-derived filing index URL for all nine deals (V, 9/9), which serves S3.
- **`MANIFEST.csv`: no change for the nine.** Rows and filings are added only if added deals are exported.
- **MANIFEST has no `index_url` column.** An exported added deal's index URL remains only in `added_deals`.

---

## 3. Research consumers and Alex's data

### 3.1 Readers of ledgers found in `_dev/`, `lesson/` and `ref/` (V)

| Reader | What it reads | v1.14 impact |
|---|---|---|
| `_dev/reviews/2026-09-22-opus55-sol6-sweep/grading/scripts/blind.py`, with `reference/<deal>.json` | Dumps the four sheets by header, so it is schema-agnostic. The references for six deals (40–45 weighted tests each) are pinned to v1.13.2 semantics. | Reuse needs re-keying of the tests that mention All cash (2–7 per deal), Conditions (5–9), Formality (5–9) and Deadline outcome (2 per deal). Kraton, Meredith and Penford have no reference. |
| `_dev/tools/effort_sweep.py:309–333` (`ledger_stats`) | Requires exactly four sheets; `bid_keys` = Price low\|Price high\|Date from | Other-scope rows now have blank prices (D18) and CVR packages are split. bid_keys from v1.13.2 and v1.14 runs are not comparable. |
| `_dev/tools/diff_workbooks.py` | Matches whole rows with difflib | Degenerates across 22-column and 29-column rows. |
| `_dev/reviews/…/verify_correction_pass.py`; Datalink `*.py.txt` | One-off v1.13.2 verifications | Historical. |
| `lesson/operating-history/…/write_trace.py`, `verify_deliverables.py` | UID-keyed traces; `verify_deliverables.py` only hashes `ref/` files | Tied to v1.13.2 bases. |
| `_dev/tools/make_seed.py` | Identifying columns of Alex's workbook | None. |

**What does not exist (V):**
- No script compares any ledger with `ref/deal_details_Alex_2026.xlsx`. The comparison at maintenance README:26 has no committed code.
- There is no estimation code, notebook, `.mat`, `.m`, `.R` or `.do` file in the repository. Alex's voice notes refer to "the .mat file" kept outside it.

### 3.2 Structure of Alex's data (V)

- **Layout.** One sheet, `deal_details`: 9,335 rows × 35 columns, 390 deals keyed by `DealNumber`. The first column is an unnamed index.
- **Missing values.** Stored as the string `NA`, so numeric columns have mixed types.
- **Provenance.** Alex's corrections are marked only by **red font**, and only in nine deals: P&W, Medivation, Imprivata, Zep, PetSmart, Penford, Mac-Gray, Saks and sTec. Every other deal, including Datalink, Kraton, Meredith, Synacor and Pepco, holds Chicago RA coding.
- **Units:**
  - `bid_value_unit` is one of dollar, million, billion, Unspecified or NA; `multiplier` is 1, 1e6, 1e9 or NA.
  - `bid_value_pershare` = `bid_value` × `multiplier` / `cshoc` on all 24 numeric aggregate-value rows. On all 3,107 dollar rows, `bid_value_pershare` = `bid_value`.
  - Dates are Excel datetimes. The instructions use MM/DD/YYYY; Alex edited only `bid_date_rough`.
- **Codes:**
  - `bid_type`: Formal, Informal or NA; one row has the typo `Informsl`.
  - `all_cash`: 1, 0 or NA.
  - `bidder_type_*`: 0/1 indicators.
  - `bidder_type_note`: codes such as S, F, "Non-US public S".
  - `bid_note`: 29 event codes.

### 3.3 Mapping to the v1.14 ledger

Types: **E** = exact, **D** = derivable (formula given), **N** = not derivable.

| Alex column | v1.14 source | Type and formula |
|---|---|---|
| TargetName, Acquirer | Deal facts Target, Acquirer | E (text; normalize names). Join via `seed.csv` `deal_number`. |
| DealNumber | none (`seed.csv` `deal_number` ↔ slug) | D via the seed join. |
| gvkeyT, gvkeyA | none | N (Compustat). |
| DateAnnounced | Deal facts "Merger announced"; the Merger announced row's Date from | D (date parse). |
| DateEffective | none (after the filing cutoff, E8) | N. |
| DateFiled, FormType | Deal facts "Filing type and date"; MANIFEST | D. |
| URL | `seed.csv` `index_url`; S3 Source sheet | D from pipeline metadata, not from the ledger. |
| Auction | Deal facts "Auction screen" | D: 1 if any process entry starts "Met", NA if "Uncertain". The screen counts independent acquirers per process (E1); Chicago counts NDA signers. |
| BidderID | # | D as a rank only. Alex's IDs are fractional, and his rows are a subset of the ledger's. |
| BidderName | Who | E for named bidders. Cohort rows expand to a1…an only when Count is exact; ranges cannot be expanded. |
| bidder_type_financial / _strategic / _mixed | Type | D: 1{Type = Financial / Strategic / Mixed}; Unknown → NA. |
| bidder_type_nonUS; the public/private parts of bidder_type_note | none | N (Note text at most). |
| bid_value | Price low/high; aggregate amounts only in the Note | D for per-share bids; N for aggregate bids. |
| bid_value_pershare | Price + CVR/earnout value | D: point price = Price low = Price high. **Package = Price + CVR/earnout value**, verified on 3/3 CVR rows (Mac-Gray Party B; P&W G&W ×2). Aggregate bids need shares outstanding (N; see §5). |
| bid_value_lower / _upper | Price low / Price high (plus CVR value for the package) | E for upfront amounts; D for the package. |
| bid_value_unit, multiplier | Deal facts "Currency and units" (deal level) | D ("dollar", 1) when the price cells are filled; N otherwise. |
| bid_type | Formality, plus Conditions under a declared transformation | D per policy (§3.4). |
| bid_date_precise | Date from, if Date from = Date to | D. |
| bid_date_rough | Sort date | D (approximately). E8's midpoint rule matches his mid-month convention. |
| bid_note | Event, Exit reason, Rounds Finality and Deadline outcome | D by code map: NA→Bid/Bid reaffirmed (whole-company only); NDA→NDA signed; Drop→Withdrew; DropM/DropBelowM→Withdrew + "Value below market price" / "Value at or below market price"; DropBelowInf / DropAtInf→Withdrew + "Value below earlier offer" / "Value at earlier offer"; DropTarget→Dropped by target; Executed→Merger agreement signed; IB / IB Terminated→Adviser / Adviser ended; Target Sale→Target sale decision; Target Sale Public / Sale Press Release→plus Sale process announced; Bidder Sale→Bid with a first-contact Note; Bid Press Release→Bid announced; Bidder / Target Interest→same labels; Activist Sale→Activist; Terminated / Restarted→Process terminated / restarted; "Exclusivity 30 days"→Exclusivity changed; Final Round Ann / Final Round / Inf / Ext→Deadline set / Deadline / Deadline revised in the round whose Finality marks it final. The final-round mapping depends on the round map, a convention (D8). Did not submit and Not selected at signing have no Alex code. |
| all_cash | Stock % | D: 1 if Stock % = 0; 0 if Stock % > 0 or Part stock; NA if Not stated or Varies. A CVR does not change it (voice-notes summary, item 5). |
| additional_note, comments_1–3 | Note, Questions | N (free text). |
| cshoc | none | N (Compustat; §5). |

### 3.4 bid_type against Formality and Conditions (V)

I aligned the pilot versions' Bid and Bid reaffirmed rows to Alex's labelled rows by bidder, price (upfront, or upfront + CVR) and nearest date. All rows aligned: 13/13 for Mac-Gray and 14/14 for P&W.

| Reading | Mac-Gray | P&W |
|---|---|---|
| Formality alone | **13/13** | 11/14 |
| Formality ∧ Conditions ≠ Heavy | 11/13 | **14/14** |

The maintenance README:26 claim holds. No single reading reproduces both deals; the best is 25 of 27.

Alex's own August rule (voice notes, item 10, and II.6–7) is a menu, "robust to different interpretations":
- markup = Formal;
- heavy conditionality may be reinterpreted as informal;
- alternatively, every pre-final-stage bid is informal;
- a range on a formal bid may be reinterpreted;
- exclusivity never downgrades a bid.

The transformation is therefore a declared policy set, not a single fact.

---

## 4. Analysis contract outline

**Purpose (I).** A versioned document plus an offline reference script that turns a v1.14 ledger into estimation input under named policies. It emits several outputs side by side. It records the ledger version id and hash, the instruction hash, the contract version and the policy id. It never writes into the ledger.

| Element | Definition from v1.14 | Status |
|---|---|---|
| Inputs and sample | `ledger_schema` v1.14; raw run or reviewed working-copy export; Auction screen "Met"; Whole-company bids Yes; Meredith descriptive-only (settled, RESEARCH_QUESTIONS:20) | Mechanical. Which version counts as "the data" is **[A]**. |
| Bidder units | E3: parent + shell = 1; joint bidders = 1; Bidding group changed | Mechanical |
| Live counts | E14: first entries + re-entries − exits − group and process closures. Count is exact, otherwise a bound in the Note prefix ("Count: at least 11 / approximately 20 / 11–14 / unknown"), which parses to [lo, hi]. | Parsing is mechanical. **What estimation does with a range is blocked on Alex: V114_SPEC §5 Q1 / Decision 3** (use bounds; presume the ordinary sequence; or one bound). |
| Eligibility and admission | Rounds "Who was in", including "still being received, not admitted"; NDA-interval rule (E3/E4) | Free text, so only partly mechanical. Whether eligible-but-unadmitted bidders count is blocked on Alex. |
| Partial scope (D7, D18) | Whole-company contest only. Other-scope rows are excluded and carry no prices. A switch closes participation (a Withdrew row whose Note says talks continued). A break-up weighed against a sale raises a Question naming the parties. | Exclusion is mechanical. The switch is flagged only in Note text (a gap). D7 is provisional (Alex Q2). The optional wider count is manual. |
| Merger of equals (D17) | Alternative map given where scope is unresolved | Blocked (Alex Q4) |
| Rounds and stages | Map (Process, Round, Finality) to model stages; round 0 and post-signing excluded; D8 counts each stage once | Mechanical given a map; the map is provisional (Decision 1). |
| Deadlines (D10, D11) | Per due date: Enforced = hard; Extended or "Extended (late bid accepted)" = extended; Passed without action = soft; Unclear = missing. A missed deadline is not an exit; Did not submit ends participation. Per-bidder differences appear only in Notes. | Mechanical. D10 and D11 are provisional (Alex Part 2, Q7). |
| Bid observations | Bid and Bid reaffirmed rows. Same-price commitment revisions are Bid rows (D13). | **New decision:** is a same-price commitment revision a new price observation or a change of terms? **[A]**/Alex |
| Prices | Upfront (Price low/high); package = upfront + CVR value; one-sided statements fill one cell; imprecise ranges blank; Stock % → all_cash; payment form is irrelevant for informal bids (Alex, Q&A P267) | Mechanical. Choosing upfront or package as the estimation price is Alex's call. |
| Cohort components (D16) | Varies; the split is only in the Note | Mechanical: treat as missing at cohort level. |
| Formality/Conditions transformation | Policies: T0 Formality as recorded; T1 Formal ∧ Conditions ∈ {None, Light}; T1u, T1 with Unclear counted as Heavy; T2 a range on a Formal bid becomes Informal; T3 everything before the final stage is Informal; exclusivity never downgrades (D14). | Each policy is mechanical. **The primary policy is blocked on Alex** (§3.4: his spring coding follows T0 on one deal and T1 on the other). |
| Unclear / Not stated | Never coerced. Missing, or bounded by best and worst case. | Blocked on Alex |
| Exits | Exit reason maps to Alex's Drop codes (§3.3). Inferred exits have Inferred = Y and Exit reason Not stated. Actor, timing and reason are separate (E14). | Mapping is mechanical. Whether inferred exits enter as dropouts or as censoring is blocked on Alex. |
| Dates and order | Sort date is the sequence key; Date from/to are bounds | Mechanical |
| Judgement variables | Process initiator: Alex says "re-generate it in the estimation code" (Q&A P96); winner's type | Rule to be declared. Alex. |
| Source hierarchy | Spring hand coding versus August notes | Blocked (V114_SPEC §5) |
| Market data | §5 | Blocked (data access **[A]**; reference date, Alex) |

---

## 5. Market-data supplement (P2) outline

**What Alex asked for (V, voice notes; line numbers refer to the extracted paragraph list):**
- **sTec (≈ line 117):** "keep track of the target's changing stock price throughout the entire sale process… the premium over and above the market price… may be the same or even higher."
- **Meredith (≈ lines 89–95):** the bid-to-market-price ratio (Shreye, from SDC); the stock price one day before and one day after the spin-off; the total target's price 4 weeks before announcement; a Remainco price "unaffected by ongoing acquisition talks". Meredith was excluded because no segment price exists.
- **Meredith (≈ line 105):** "the premium over the market price" paid by the winner.
- **Meredith item 4 (≈ line 100):** net debt, to convert enterprise-value bids into equity per share.
- **Q&A text:** no share-price request found (searched share price, stock price, market price, premium, unaffected).
- **Alex's workbook** already carries `gvkeyT`/`gvkeyA` and `cshoc`, and uses `cshoc` to put aggregate bids on a per-share basis (§3.2).

**What a join needs (I):**
1. **Identifiers.** Deal slug → `seed.csv` `deal_number` → `DealNumber` → `gvkeyT` → CRSP PERMNO through the CCM link, with link-date validity. Unmatched deals are flagged, never guessed.
2. **Dates.** Per bid: the last trading day before Sort date, or before Date from for windows. Per deal: an "unaffected" date rule, for example 4 weeks before the first leak or the announcement. **The rule is Alex's decision.**
3. **Price field.** Close price; unadjusted versus split/dividend-adjusted across the window (CRSP CFACPR); currency (target in USD; flag otherwise).
4. **Shares outstanding** for aggregate bids: `cshoc` date versus CRSP SHROUT versus the filing's own count (Alex's collection instructions: "to be verified"). Net debt for EV-based bids.
5. **Separation.** A separate table (deal, date, price, source, identifiers, adjustment, vintage and query hash). It is never written into the ledger or shown to extraction. Filing-reported references stay in Notes (E13: "Ref: $12.10 close 08/08/2014; 49% premium"). Premiums are computed downstream under a declared policy.
6. **Blockers.** Data licence and network access (WRDS, CRSP, Compustat): **[A]**. Reference-date and shares-source rules: Alex.

---

## 6. Review migration: reviewing v1.14 runs without redoing eight reviews

**What exists (V):**
- **Cockpit Compare** (`workspace.py:441–466`) matches ledger rows by `#`, Rounds by (Process, Round), Questions by Q and Facts by Field (`:112`). Its `_diff` walks only the right-hand version's columns (`:497`); S2 fixes that with a column union.
- **Rebase** ("Use as working-copy base…") replaces the whole working state with the new base (`:766–773`). Row review statuses, finding judgments and UID-keyed threads stay behind in History. Three comments exist today, on Mac-Gray and P&W.
- **A working copy cannot gain v1.14 columns.** Updates to fields not in the state's columns are rejected (`:618–621`).
- **`diff_workbooks.py`** matches whole rows.
- **Version-independent precedent:** the Datalink and Mac-Gray pilots' filing-keyed, frozen **source inventories** (S01…), against which each workbook was mapped (`reviews/2026-09-21-*-pilot/source_inventory.md`, `inventory_comparison.md`, `inventory-comparison.md`).
- **Content carrying filing cites** ("p.38 b601"), rules and verdicts, but keyed to v1.13.2 UIDs and final `#`: the audit's per-change `inventory/<deal>.csv` and `deals/<deal>-verdicts.csv` (318 changes), `lesson/trace/…`, V114_SPEC §9.3 (16 cases) and Astra §7.4.

**Why these fail for v1.14 (V/I):**
- New runs have different event counts and new UIDs, so matching by `#` or by UID pairs unrelated rows.
- D8 can shift round numbers, so matching by (Process, Round) fails too.
- The v1.13.2 working copy cannot be migrated in place.
- Rebasing discards the review state.

**What must exist (I). All are offline and involve no model; each needs Austin's go-ahead to write under `_dev/eval/` or a review packet.**
1. **A reviewed-facts register per deal.** Build it mechanically from the latest working-copy snapshot (`revisions`, `mode=ro`) and the audit's verdict CSVs. Each item is one estimation-relevant fact in Part A order (participation and exits, round map, per-bid Formality and Conditions, order, prices). It carries:
   - its filing key: page, cockpit block id and quote;
   - the reviewed value;
   - its basis: reported, inference, or convention id (audit A1–A17);
   - its status: supported, reverted or unresolved;
   - its **v1.14 impact**: unchanged; re-judge under Dn (D5, D7, D9–D11, D13, D15, D16, D18, express incorporation, H1–H3); or new column with no reviewed value (the five condition components, CVR, Stock %).
   All cash maps to Stock % as Yes→0, No→>0 or Part stock, Not stated→Not stated.
2. **A content aligner.** Match v1.14 rows to register items by event family, normalized Who, Sort-date window overlap and price (± CVR), accepting unique matches only. Align Rounds by opening date and members.
3. **A triage report** in four buckets:
   - agrees: accept, with a seeded spot-check sample;
   - differs where v1.14 changed the rule: source check under v1.14;
   - differs where the rule is unchanged: source check (either a regression or an earlier review error);
   - omissions and insertions: completeness check.
4. **A porting path.** Rebase onto the v1.14 run, then apply the valid register items as one prepared, verified and attributed revision, on Austin's command. S4 bulk Process/Round edits help here. Set the deal-level status to "Reviewed" only after a checked review (audit F3/F9).
5. **Datalink:** use its bounded inventory (pp. 29–31) and F9; its current draft has no working-copy review. **Held-out four:** full review, with Alex's corrected coding (Medivation, Imprivata, Zep) as a third reader only.

---

## 7. Errors in V114_SPEC §7, §9, §11 (this slice)

1. **§7 gate order (lines 554–564): deploy (7) comes after the runs (4) and after publication (6).** (V) With checker 1.6 live:
   - a v1.14 workbook using `Extended (late bid accepted)` gets a permanent `controlled.deadline_outcome` error (`check_lean.py:261–265`, `:1298–1307`);
   - that error lands in the stored `check.json` the worker writes per run (`worker.py:311–319`), which S1 forbids rewriting;
   - the editor offers only the single value set (`workspace.py:349–357`), so reviewers at gate 5 cannot select the new value;
   - S3 provenance would be missing from the workbooks reviewed and sent.

   Deploy before gate 4.
2. **§7 gate 4 (line 558): "held-out deals: Medivation, Zep, Pepco and Imprivata".** (V)
   - The Medivation, Zep and Pepco filings were read in designing the taxonomy (`REVIEW_FABLE.md:7, :11, :15, :17, :19, :21, :29`). Zep and Pepco are definitional examples in `TAXONOMY_DRAFT3.md:34, :55, :72`, `TAXONOMY_DRAFT4.md:40, :60, :76` and `TAXONOMY_DRAFT5.md:40, :60, :76`. Only Imprivata is unmentioned.
   - The audit's held-out rule excludes "Medivation and anything already added or extracted in the cockpit" (`lesson/independent-audit-2026-09-23/recommendations.md:22`).
   - Their v1.13.2 versions are unreviewed, so a comparison measures change, not accuracy.
   - Zep and Imprivata ran at xhigh, not medium.

   Call them "not used to tune E6–E14", and not held-out for E12 and E13.
3. **§7 gate 5 (line 559): "Review them against §9.3 and the old working copies".** No mechanism exists (§6). The S2 column-union fix does not solve row alignment.
4. **§7 S5 and gates 8–9 (lines 518–520, 562–563).** The catalog decision is not just lifting a guard. An in-place overwrite breaks the eight working copies (hash check, `workspace.py:166–168`, `:185–186`). The originals must be relocated with the same id and hash, and `import_results.py` and `verify_catalog.py` updated. Also, `export_repo.py` exports no receipts, and run receipts live in ignored `state/`, so a packet step is missing.
5. **§3 header (line 127) versus §7 gates 3 and 6.** "v1.14 (candidate)" would be frozen into the published text and exported verbatim. Editing it after evaluation changes the hash. The spec needs a header decision before gate 3 (§2.4, step 2).
6. **§7 S6 (lines 522–529) omits documents that need updating:**
   - CHRONOLOGY (no rows after 23 September);
   - root README.md:12–17;
   - AGENTS.md:8 (`lesson/`);
   - cockpit README:9 and :13;
   - the Mac-Gray pilot README:3 (R01 "remains for Austin", which is stale);
   - the deploy-time rows in COCKPIT_BUILD:47 and :69 and tools README:118.

   §0 (lines 53–56) does not authorize those files, so Austin must approve the scope.
7. **§7 S6 (line 527): "eight of the nine deals have reviewed working-copy edits".** The audit found the review statuses untrustworthy (audit README §1.1), `lesson/README.md:16` says all eight "remain In review", and the `deal_review` table is empty (V). Say "edited, Astra-assisted, audited, with three clusters reverted".
8. **§9.3 (line 618) and §10 (line 648): "P&W #52".** This number is valid only in pilot `…38bc24`, where #52 is G&W's bid (Formal, Light, Concern). In the v1.13.2 extraction and working copy revision 16, #52 is Party E's Dropped by target (V). Name the version.
9. **§7 S5 (lines 513–514), minor citations.** "revision 0 (line 84)" is line 83. "one version per deal (lines 86–88)" is line 73; line 86 is the API list check.
10. **§7 S3 (lines 497–500), minor.** No derivation is needed. `ref/seed.csv` `index_url` is already recorded and read by the server (`deals.py:31`), and it equals the derived URL for 9/9 deals (V). Use it and cross-check.
11. **§11 (lines 667–680): verified correct.**
    - All hashes: frozen `513c8e3e…`; draft `f9595d74…` = cockpit draft `a4ca26ecfa92`; DOCX `faab1d66…`; voice notes `9ddb0a38…`; Astra `32dfe7de…`.
    - The pilot ids and the working-copy revision numbers.
    - The three services are active from this checkout.
    - Unlisted: a second, unused draft `73f21eb8c09a` (text = v1.13.2).
12. **Not checked (outside this slice):** the §9.4 Python baseline of 199 versus the 207 in HANDOFF.md:18 and the phase 5 PROGRESS (probably different runners).
