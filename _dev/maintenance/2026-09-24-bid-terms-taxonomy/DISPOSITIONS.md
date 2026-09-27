# Dispositions of the systemic audit findings (v1.14)

25 September 2026, wave 3; checked and completed at about 23:20 UTC. This file gives the disposition of every finding in the five audits in [systemic-audit/](systemic-audit/): A (checker and tools), B (cockpit), C (instruction cascade), D (documentation, release and research) and E (review of the spec's first system draft). It answers [V114_SPEC.md](V114_SPEC.md) §7.14, "the disposition of every audit finding".

**Sources.**
- The spec, whose order of authority puts it above the audits (§0). Where the spec settles a finding differently from the audit's proposal, the spec wins and the note says so.
- The package reports from waves 1 and 2, and the wave-3 report on the deploy and release documentation lines.
- Direct checks:
  - the worktree `/home/uctpiaj/work/Projects/sec-extraction-v114`: code read at the cited lines; the full unit suite (292 tests) and the HTTP suite (20 tests) re-run, both OK, with `PYTHONDONTWRITEBYTECODE=1` and `TMPDIR` under `v114-scratch`; `git status` unchanged afterwards;
  - the checker `check_lean.py` 1.7, SHA-256 `fa953928…607f`; the worktree `_dev/tools/README.md`, SHA-256 `c87c9bf2…1ec4` (the lead edited line 49 at 23:10 UTC, during this check);
  - the candidate, SHA-256 `c2d47a47…ab27`, checked by grep;
  - the deliverables in this folder: `evidence/`, `migration/` (row marks recounted: 454 reviewed, 66 needs decision, 520 rows, 1,561 facts), `analysis/`, `release/` (`d25-tools.patch`; `tools-readme-release.patch`, regenerated at 23:11 and checked to apply to the current worktree README; `PROPOSED_DOC_LINES.md`, updated at 23:12; `deploy-tools.patch` and `release-gate12.patch`, first made at 23:13), `pre-existing/` (21 patches), the CHANGELOG, `R_REVIEW.md` and the DOCX;
  - the "now" documentation lines in the live checkout.

Nothing is deployed, published or committed.

**Dispositions.**

| Disposition | Meaning |
|---|---|
| done | Implemented and checked. The note names the package and the file, test or deliverable. **done, part open** means part of the finding remains; the remainder is in the open items. |
| not adopted | Rejected. The note cites the spec section or decision that rejects it. |
| deferred | Left to one of Austin's gates or the backlog. For a documentation line, the note names the proposed text in [release/PROPOSED_DOC_LINES.md](release/PROPOSED_DOC_LINES.md) (entries D1–D23 for the deploy, R1–R12 and G1–G12 for the release). |
| applied to the spec | The current spec had already corrected or adopted the finding before implementation began. This covers every E item and the "errors in V114_SPEC" sections of A–D. Where code or text followed, the note says where. |
| not applicable | A confirmed fact, a historical line, or a finding with nothing to act on. |

**Counts.**

| Audit | Rows | done | done, part open | not adopted | deferred | applied to the spec | not applicable |
|---|---|---|---|---|---|---|---|
| A | 33 | 22 | 0 | 0 | 0 | 10 | 1 |
| B | 49 | 30 | 2 | 1 | 0 | 13 | 3 |
| C | 92 | 73 | 0 | 0 | 0 | 17 | 2 |
| D | 94 | 35 | 6 | 2 | 24 | 16 | 11 |
| E | 46 | 0 | 0 | 0 | 0 | 45 | 1 |
| **Total** | **314** | **160** | **8** | **3** | **24** | **101** | **18** |

Some findings appear in several audits, for example the gate order (B1, D §7.1 and E). Each audit's rows are counted separately. No finding is left without a disposition.

The 24 deferred rows are all in audit D: documentation lines applied at the deploy or the release, gate actions, and the backlog. Proposed text now exists for every deferred documentation line. Most "applied to the spec" rows also have their implementation done; the note says where.

No "done" claim was found false. Two notes were corrected (A-§2.1's record, B-§5.4's test), and the open items were brought up to date with wave 3: the release lines of the tools README are now in `release/tools-readme-release.patch`, the deploy and release lines outside `_dev/tools` are drafted, and a first deploy patch exists but predates two open fixes.

---

## A. Checker and standalone tools

| ID | Finding | Disposition | Where, and note |
|---|---|---|---|
| A-Claim 1 | Checker 1.6 rejects `Extended (late bid accepted)` in every workbook | done | S1: `DEADLINE_OUTCOMES_V114`, chosen by schema (`check_lean.py:281`, `:1433`). |
| A-Claim 2 | `diff_workbooks.py` reports every row across schemas | done | S7; see A8. |
| A-Claim 3 | No rule checks Bids received against the ledger; do not add one | done | No rule added (§7.3 "Do not add"). S1's re-review after R confirms. |
| A-Claim 4 | Spec citations: the `exit.inferred_reason` rule cited 2 lines off; the rest correct | applied to the spec | §7.3 now cites `:924-932`. |
| A-Claim 5 | 1.6 never requires a bid price, so D18 needs a new v1.14-only rule | done | S1: `bid.other_scope_per_share` (`check_lean.py:695`). Synacor #54 and #59 stay clean under v1.13.2. |
| A-§2.1 | Every §3–§4 rule reviewed: only A1–A4 and A6 (plus the optional A12) are needed; no Did not submit, live-count or Concern-to-Heavy rule | done | S1's review, re-run against the frozen candidate after R in wave 2. The one further change: `ledger.exclusivity_duplicate` now covers every bid event (R18, D27). Record: `evidence/s1/REPRODUCTION.md` §3 and §5.1. |
| A1 | Deadline outcome sets by schema, with a warning for the legacy value | done | S1. The legacy message uses the spec's wording (E26), not the audit's. Each pilot gains 2 legacy warnings (`evidence/s1/`). |
| A2 | Antitrust with an incompatible Regulatory value becomes an error | done | S1 (`check_lean.py:702-709`). The test that expected a warning now expects an error. |
| A3 | Other-scope bid rows leave the per-share cells blank | done | S1. Tests cover each cell, including Price high alone (added in wave 2). |
| A4 | `exit.inferred_reason` does not run on v1.14 workbooks | done | S1 (`check_lean.py:1045`), with a v1.14 twin test (`test_check_lean.py:373`). |
| A5 | Keep the name `DEADLINE_OUTCOMES`; export the v1.14 set | done | S1 kept the name and added `DEADLINE_OUTCOMES_V114`, `deadline_outcomes()` and `choice_lists()`. S2 uses `choice_lists` (`workspace.py:377`). |
| A6 | A CVR value on a Varies row: no checker change; the instruction says "only where CVR/earnout is Y" | done | The candidate says so in D1 item 12 (line 59) and E13 (line 299, "on a Varies row the amounts go in the Note"); `bid.cvr_value_marker` is unchanged. The Varies-with-value case A §2.3 suggests was added by the lead in wave 3 (`test_check_lean.py`, in `test_v114_value_lists_and_consistency_rules`). |
| A7 | Record the checker version wherever results are stored | done | Worker: S2 (`worker.py:323`, into `versions.checker` and `jobs.result.checker`). Sweep receipts and the first line of the findings: S7. |
| A8 | `diff_workbooks.py` cannot compare across schemas | done | S7. Acceptance in `evidence/s7/`: the equal-content pair shows 0 row changes; the pilot pair shows 42 matched, 11 removed and 15 added. |
| A9 | `effort_sweep.py`: candidate instruction, added deals, bid key | done | S7: `plan --instruction`, `--filing-dir`, Event in the key, Other-scope rows counted separately, checker version and schema in receipts. |
| A10 | `run_model.py` revision mode needs schema and sheet guards | done | S7 (`sandbox/run_model.py:266`, `:348`): it refuses a workbook without exactly four sheets before any run, records `revised_from_ledger_schema`, and requires `--instruction` for a v1.14 workbook. The audit's further risk, revising a v1.13.2 workbook under a candidate, has no adopted guard: §7.8 omits it, and §0 treats unlisted proposals as not adopted. |
| A11 | Record the instruction's source, not only its hash | done | S7 (`run_model.py:342`, `instruction_source`). |
| A12 | Optional v1.14 warnings (a)–(e) | done | S1 adopted (a), (c), (d) and (e) as change 6: (a) was widened after R to every bid event, and (d) follows E11's wording. (b) is not adopted (§8, Pipeline). The checks A12 itself rejected are not added (§7.3 "Do not add"). |
| A13 | Stale wording in the checker and the tools README | done | S1 rewrote `check_lean.py:40` and `:73` and README line 19 (rewritten again in wave 3). README line 158 no longer says findings include "optional model judgments" (rewritten by the lead in wave 3; a deploy-class line, §7.12). |
| A14 | One helper for the EDGAR index link | done | S3: `fetch_filing.index_link()` (`fetch_filing.py:95`), used by `fetch_filing.verify`, `deals.py:240` and `provenance.py:76`. |
| A15 | Messages that revision passes read word for word | done | S1: the Varies message covers partial reporting; the Financing message names H1; the inference-note message adds the inferred field (v1.14 only). |
| A-§2.3 | Test assertions that change in 1.7 | done | Done: `:510` now expects an error; a v1.14 twin of `:320-341`; `:506` and `:509` kept; the fixtures from `:496` extended with the §9.2 cases; `test_review_helpers.py` updated by S7; `test_effort_sweep.py` values kept; the CVR Varies-with-value case added in wave 3 (A6). |
| A-§2.4 | Cross-schema comparison tooling (items 1–5) | done | S7. §7.8 adopted all five items, including `--include-source` and the "E12 rules changed" flag (E26). |
| A-§3.1 | Spec: the rule is at `:924-932` | applied to the spec | §7.3 change 4. |
| A-§3.2 | Spec: the pilots change, so they do not "reproduce" | applied to the spec | §7.3 Reproduction and §9.2. S1's pilot deltas match. |
| A-§3.3 | Spec §9.2: Exclusivity Varies on a one-bidder row is an error | applied to the spec | §9.2, first bullet. |
| A-§3.4 | Spec: an inferred date cannot be told from an inferred exit, so skip the rule on v1.14 | applied to the spec | §7.3 change 4; implemented in S1. |
| A-§3.5 | Spec: `workspace.py` imports `DEADLINE_OUTCOMES` | applied to the spec | §7.3 change 1. |
| A-§3.6 | Spec: the two Varies interactions | applied to the spec | §7.3 change 5 and §3 D1. |
| A-§3.7 | Spec: §7 misses `diff_workbooks.py` | applied to the spec | §7.8 (S7). |
| A-§3.8 | Spec: the review list names rules the checker does not have | applied to the spec | §7.3, "Review of the existing rules". |
| A-§3.9 | Spec: sweep receipts lack the checker version | applied to the spec | §7.8; implemented in S7. |
| A-facts | Baselines (1.6 reproduces every stored result; 199 tests collected); the §2.2 "No change needed" list; the §3 statements that checked out | not applicable | Facts. S1 re-confirmed the reproduction under 1.7. |

## B. Cockpit

| ID | Finding | Disposition | Where, and note |
|---|---|---|---|
| B-Claim 1 | Results are stored permanently with no checker version, and no screen shows one | done | S2 stores `checker_version` and `ledger_schema` from now on; older runs read their receipt; no receipt is rewritten (see B2). Deploying before any run is §13 gate 3. |
| B-Claim 2 | Choice lists change only after a restart; the editor blocks unlisted and multi-part values | done | S2 (see B3 and B5), with the wave-2 fix that brings the drop-down back ("Choose from the list"). The restart is §12 step 7. |
| B-Claim 3 | The payload has no schema; compare walks one column set; one choice list per field | done | S2 (see B3 and B4). |
| B-Claim 4 | S3 facts: download route, shared export, four-sheet test, `index_url` | done | S3. |
| B-Claim 5 | S5 facts: stale `verify_catalog.py`, overwrite risk, export refusal, importer constants | done | S5 (see B10 and E18). |
| B-Claim 6 | The worker's default-instruction fallback is unreachable for new jobs | done | OPS: a job with no instruction now fails with `instruction_missing` (`worker.py:260`). The label for old jobs is kept (S2; E14). |
| B1 | Under the old gate order, runs are checked and reviewed with 1.6 | applied to the spec | §13 gate 3 deploys before any run (§8, Release). The deploy itself is Austin's (gate 3). |
| B2 | No screen shows a checker version | done | S2: the Review tab ("Live check" and "At import", `runs.js:187-194`), the Runs tab, the version picker and an All deals tooltip. Catalog versions read their 22 September receipt (E27). |
| B3 | The payload needs the schema; choices must follow the displayed version's schema | done | S2: `data.py:1014`, falling back to `check_lean.ledger_schema()`; choices at `workspace.py:377`. |
| B4 | Compare across schemas drops columns | done | S2 (`workspace.py:641`); unit and HTTP tests in both directions. |
| B5 | The editor cannot enter multi-part or unlisted values | done | S2: Deadline outcome is free text with a picker that builds "A; B"; other lists have "Other…". Wave 2 fixed returning to the list (`choices.js`). |
| B6 | A rebase drops reviewed work silently; past revisions cannot be compared or downloaded | done | MIG-C in S2: `rev:N` compare and download; the rebase preview counts what stops applying; judgments carry over (`carried_over`); orphaned threads read "on an earlier base (revision N)" (`trace.py:238`). S2 also fixed an existing bug that made every rebase of an edited copy fail with 409. The undo instruction is in the dialog (E32). |
| B7 | A working copy's columns are fixed by its base | done | S2 keeps the invariant and adds a test for it. |
| B8 | The five-sheet download fails the checker; the docs say the download equals the export | done, part open | S3: `?source=0` gives four sheets; files are named `{slug}-working-r{N}.xlsx`; the checker stays strict (tested); tools README line 118 and the comment in `test_cockpit_export.py` are fixed. Open: `_dev/COCKPIT_BUILD.md:69`, a deploy line outside `_dev/tools` (proposed text D4; §12 step 9a). |
| B9 | Sources for the provenance sheet | done | S3 (`provenance.py`): index and `.txt` links, instruction hash, revision, and `deal_review` status with "edited since", all read in one transaction. |
| B10 | Writing v1.14 workbooks to `extraction/` would break eight working copies | done | S5: catalog deals are found from the catalog (`data.py:686-741`), deployed at gate 3; `release/d25-tools.patch` and `release/README.md` cover gate 12. The move itself is gate 12 (open items). |
| B11 | Publishing keeps the text's hash, so the header and the draft's parent must be settled before runs | done | The candidate header is final (C01; §3 Header). §8 chooses published v1.13.2 as the parent, one of the two options the audit offered. Creating the draft is Austin's (gate 4). |
| B12 | A restart invalidates the write token in open tabs | done | OPS, fixed further in wave 2: after a 403, `api.js` fetches the session again and retries once. This deploy still needs a reload (§12 step 11; Austin tells Alex). |
| B13 | The root disk is nearly full | done, part open | The worktree and scratch files are under `/home/uctpiaj/work` (§0). The TMPDIR drop-ins are proposed in `deploy/PROPOSED-tmpdir.md`. Open: installing them (Austin, §12 step 6a). The root disk is now 83% full, with 1.6 GB free. |
| B14 | The server and worker unit files are not in the repository | done | OPS: `deploy/ledger-cockpit.service`, `.d/20-public-origin.conf` and `ledger-worker.service`. |
| B15 | The backup manifest does not identify the running code | done | OPS: `backup.py` records `checker_version` and `dist_index_sha256`; there is no database change. The manual backup is §12 step 3. |
| B16 | One save is capped at 100 operations | done | S4: one `bulk_update` operation, counted once against the cap (`workspace.py:832`). |
| B17 | One acceptance mode, `--actual-catalog-readonly`, points at the live checkout | done | Handled as a rule, as the audit proposed: §0 forbids that mode and puts evidence under `v114-scratch`. The browser suites ran on temporary roots. The code is unchanged. |
| B18 | `CVR/earnout value` is missing from the field sets | done | S2 (`Records.jsx:14-15`). |
| B19 | The Extract dialog does not warn about schemas | done | S2 (`runs.js:198-203`). |
| B20 | Dead instruction fallback and hard-coded label | done | S2: `LEGACY_INSTRUCTION_LABEL` (`runs.js:7`). OPS fails a new job that has no instruction. |
| B21 | The deal list rechecks every edited deal on every request | done | OPS: a per-deal cache keyed by revision, base, filing and `CHECKER_VERSION` (`workspace.py:338`). The first load after a restart is still slow. |
| B-MS 1 | Mixed schemas: compare | done | See B4. |
| B-MS 2 | Mixed schemas: choices and `ledger_schema` | done | See B3. |
| B-MS 3 | Mixed schemas: row marks, threads and field authors keyed by uid | done | They stay keyed by uid. MIG-C counts what stops applying, carries judgments over and relabels threads. |
| B-MS 4 | Mixed schemas: `record_label`, trace, digest and review status | not applicable | The audit found no change needed. |
| B-MS 5 | Mixed schemas: the All deals list follows the checker | done | The checker version is a tooltip (S2). |
| B-MS 6 | Mixed schemas: `DATE_FIELDS` and `NUMBER_FIELDS` | not applicable | No change needed. |
| B-MS 7 | Mixed schemas: `Records.jsx` field sets | done | See B18. |
| B-MS 8 | Mixed schemas: sorting and filtering | not applicable | No change needed. |
| B-MS 9 | Mixed schemas: compare's row keys are noisy across runs | not adopted | §7.4 asks for no keyed matching in the cockpit. Cross-run matching is S7's diff (§7.8) and MIG-T's aligner (§7.9). |
| B-§3 | Deploy checklist | applied to the spec | §12 is adapted from it, with E5, E7 and E29. Running it is Austin's (gate 3). |
| B-§4 at stake | Eight edited working copies: "434 reviewed and 66 needs decision", one finding decision, three threads | applied to the spec | §7.9 and §11 use E3's 454 and 66. MIG-T's `verify` and a recount of `migration/*/rows.csv` give 454 and 66 on 520 rows. |
| B-§4 today | What the code cannot do: view, compare or download a past revision; carry marks or comments across versions | done | MIG-C (see B6); B7's invariant kept. |
| B-§4 options | O1 by default, then O2 deal by deal; O3–O5 | applied to the spec | D24 adopts O1, then O2; O3–O5 are not adopted. MIG-C and MIG-T are built. |
| B-§4 steps | Before each rebase: set the status, download with the Source sheet, note the revision; rebase Datalink freely | applied to the spec | §13 gate 11, with In review as the status (E15). This is Austin's (gate 11). |
| B-§5.1 | Spec: gate order | applied to the spec | §13 gate 3. |
| B-§5.2 | Spec: the idle check is too narrow | applied to the spec | §12, window step 1. |
| B-§5.3 | Spec: S5 citations and the missing fix | applied to the spec | §7.7. |
| B-§5.4 | Spec: S2 must use the displayed version's schema; editor; round trip | applied to the spec | §7.4 items 2, 3 and 6. Implemented in S2: the round-trip test `test_cockpit_workspace.py:483`, and the pilot round trip in `evidence/s2/pilot-round-trip.json`. |
| B-§5.5 | Spec: S3 omissions | applied to the spec | §7.5. Implemented in S3. |
| B-§5.6 | Spec: the server stores and shows the checker version; the server imports the checker once | applied to the spec | §7.4 item 5 and §0. |
| B-§5.7 | Spec: cite `server.py:185-194` | applied to the spec | §0. |
| B-§5.8 | Spec: test baselines | applied to the spec | §9.4 (14 HTTP tests). |

## C. Instruction cascade

C-numbers refer to entries in [CHANGELOG_v1.14_candidate.md](CHANGELOG_v1.14_candidate.md). The CHANGELOG accounts for all 121 lines that audit C §1 names: 74 changed and 47 confirmed unchanged. Review R's 27 findings were fixed, and its re-check found all of them resolved.

| ID | Finding | Disposition | Where, and note |
|---|---|---|---|
| C-H1 | The "on those rows" anchor (55–64) | done | Item 8 stays the one definition of bid rows. The blanks are separate sentences (C11, C79), and F.4 repeats them (C78). |
| C-H2 | Three contradictions, at 230, 208 and 160 | done | 230: deleted (C51). 208: alternatives kept as the exception, split by scope (C40; D27). 160: stated as the convention for where a process starts (C32). |
| C-H3 | Bid reaffirmed carries state at 210 | done | Express incorporation (C42, C44), candidate line 230. |
| C-H4 | D10 does not reach E14 (257, 264) | done | C66 and C70: "not necessarily permanent" and the "21 signers" example are gone. |
| C-H5 | D7 misses several places | done | C19, C21, C24–C27, C30, C33, C65, C68, C69, C72, C76. |
| C-H6 | The spec's D-numbers collide with the instruction's D1–D5 | done | Grep: only the instruction's own section references remain. |
| C-H7 | Penford's figure at 247 | done | Replaced by "Ref: $20.00 close 02/08/2019; 25% premium" (C61). |
| C-§1 Part A | Part A rows: the four edits and their cascades | done | Part A is the spec's text byte for byte (C02). The cascades are as in C-H5, plus E10 (C42). |
| C-§1 B, C | Header, B and C rows, including Inferred = Y on an unannounced round and the two no-op items | done | C01, C03–C09. An unannounced Round opened row is Inferred = Y (line 181). No text was added for the no-ops (§3 C). |
| C-§1 D, F | D1–D5 and F rows: where a missed submission is recorded, Bids received scope, a Question's issue type without a new column, D5 labels untouched | done | C10–C23 and C75–C78. The issue type goes in the Question's text (line 331). The D5 labels are unchanged. |
| C-§1 E1–E5 | E1–E5 rows: unresolved scope; merger of equals in the instruction's own words | done | C24–C33. |
| C-§1 E6–E9 | E6–E9 rows: round 1's lead sentence, decision date against outreach date, Round opened as the first row, no "Alex's convention" | done | C34–C39; the Round opened rule is in E8 (C38, line 208). |
| C-§1 E10–E14 | E10–E14 rows: which row holds the termination fee, an unsolicited bid in a final round, incompatible package bases, E14's roles | done | C40–C73. |
| C-§1 E12 | E12 rows: H1–H3, the boundary with Concern, the D5 list, exclusivity, CVR, cohorts, dates, examples | done | C45–C59 and C80; the examples are neutral (see E9). |
| C-§1 [I] | Other cascade proposals marked as inference: 226 (a later passage counts only if it dates the fact), 81 (keep the first-contact Note), 89 (add a missed submission and price feedback to Other material event), 241 (the Note names H1–H3); the D3 list order is cosmetic | done | C48, C15, C17 and C58. The order needs no change. |
| C-§2.1 | 55–64 anchor | done | As C-H1. |
| C-§2.2 | 208: alternative structures against "one communication, one row" | done | C40. The spec keeps the exception (§3 E10; D27), so the audit's reading as a contradiction to remove is settled that way. |
| C-§2.3 | 210 state carry | done | As C-H3. |
| C-§2.4 | 230 "stops when refused" | done | C51. |
| C-§2.5 | 160, E5(b) against "silence does not prove inactivity" | done | C32. |
| C-§2.6 | 257 and 264 | done | As C-H4. |
| C-§2.7 | 255 and 265 need the reserve and continuing-discussion exceptions | done | C64, C71. |
| C-§2.8 | 256: Withdrew does not cover a switch | done | C65. |
| C-§2.9 | 260: how partial-only participation closes | done | C68: no exit rows; the last row's Note says how talks ended. |
| C-§2.10 | 262: Exit reason is unconditionally Not stated | done | C69. |
| C-§2.11 | 24: "one of three things" | done | C03. |
| C-§2.12 | 26: false precision against E14's transition labels | done | C04. |
| C-§2.13 | 28 and 68 are written per row | done | C06, C14. |
| C-§2.14 | 173: lead sentence and decision date | done | C35. |
| C-§2.15 | 198: Sort date for undated outreach | done | C38 (R15). |
| C-§2.16 | 237: Light's "expedited" | done | C53. |
| C-§2.17 | 228: Concern against H3 | done | C56. |
| C-§2.18 | 227: the Contingent list is not subordinated to D5 | done | C49. |
| C-§2.19 | 249: partial reporting | done | C62. |
| C-§2.20 | 57 and 251: the CVR value needs Y | done | C11, C63. |
| C-§2.21 | 245 and 247: the Other-scope exception; incompatible bases | done | C60, C61. |
| C-§2.22 | 112, 153 and 163 are not limited to the whole company | done | C21, C30, C33. |
| C-§2.23 | 88: Exclusivity changed has no D15 exception | done | C16. |
| C-§2.24 | 220: a Heavy example with no trigger | done | C45. |
| C-§2.25 | 129: a second definition of Bid; unresolved scope | done | E1 (line 133) makes Bid the whole-company label and refers to E10. Unresolved scope stays outside the counts, with a Question (C24). R rejected a further "circular definition" point. |
| C-§2.26 | 224: "the five condition columns" | done | C47 names the columns. |
| C-§2.27 | 14 against "do not infer a valuation" | done | C73: the extractor records the exit; the model interprets it. |
| C-§3 | Part A references resolve, but E10's only after E10 changes | done | C42 (line 228). R's §9.1 check: every reference resolves. |
| C-§4.1 | Columns, fields and sheets equal the checker's | done | Still equal: S1's `compare_lists.py` finds 23 of 23 equal; R's re-check passes 58 of 58 value-list checks. |
| C-§4.2 | The Acquirer type list is not stated | done | Candidate line 125 (§3 D5; E Appendix A). |
| C-§4.3 | CVR/earnout and Antitrust markers are narrower than the checker's | done | C10, C12. |
| C-§4.4 | The CVR value requires Y | done | C11. |
| C-§4.5 | Antitrust severity | done | S1 (A2). |
| C-§4.6 | Stock % wording | done | C62 (D16; "40–60"). |
| C-§4.7 | Deadline outcome set | done | C20 and C39 in the candidate; S1 (A1) in the checker. |
| C-§4.8 | `exit.inferred_reason` gives false warnings | done | S1 (A4). |
| C-§4.9 | The checker enforces an unstated Round opened rule | done | C38. |
| C-§4.10 | Other-scope price blanks | done | C11 and C79 in the candidate; S1 (A3) in the checker. |
| C-§4.11 | The cockpit's choices omit No deadline stated and offer All cash for every schema | done | S2 via `choice_lists`. Checked in the code: both schemas' lists include No deadline stated; All cash appears only for v1.13.2. |
| C-§5.1 | No deal names | done | The §9.1 grep is clean (A1, R, and again here). |
| C-§5.2 | 247: Penford's figures | done | C61. |
| C-§5.3 | 249: "50–75" | done | C62 ("40–60"; §3 rules, E31). The checker's `controlled.stock_pct` message now says "40-60" too (S1, wave 2; checked). |
| C-§5.4 | Header | done | C01. |
| C-§5.5 | Spec text that must not be copied: "Alex's convention", "fixes the recurring error", "remain deferred", "v1.14 only", the table caption, decision IDs | done | Grep is clean. Alex's name appears only in the unchanged research credit on line 4. |
| C-§6 D18 | Re-anchor D1; the E13 exception; E1 | done | C11, C60, C79, C24. |
| C-§6 D16 | Stock % partial reporting; the CVR value only with Y | done | C62, C11, C63. |
| C-§6 D10 | 264, 257, and where a missed submission is recorded | done | C66, C68, C70, C22. |
| C-§6 D7 (1) | Scope for 153, 163 and 112; Withdrew; 260; 129 | done | C21, C30, C33, C65, C68, C24. |
| C-§6 D7 (2) | Inferred-exit transitions apply to the whole company only | done | C69. |
| C-§6 D15 | 88; 230; a request made in the bid letter | done | C16, C51, C43. |
| C-§6 D1 | Remove the Bid reaffirmed carry | done | C44. |
| C-§6 D13 | Which row's Note holds the termination fee; add the reverse fee to the Note list at 68 | done | The termination fee's row is in E10. The reverse-fee addition to D1 item 23 was not adopted: the audit marked it [I], §3 does not list it, and E12 Financing already puts any reverse fee in the Note (CHANGELOG, "Not added"). |
| C-§6 D5 | Subordinate the whole Contingent list | done | C49. |
| C-§6 D14 | Light's "expedited" | done | C53. |
| C-§6 D3 | The boundary between Concern and H3 | done | C56. |
| C-§6 D8 (1) | D8 cites an "explicit final solicitation" rule that neither E6 contains | applied to the spec | §8 reads it as Astra's finality rule, and D8's text no longer uses the phrase. Implemented in C36. |
| C-§6 D8 (2) | Round 1's lead sentence; decision date against outreach date | done | C35, C38. |
| C-§6 D12 | No change to F | done | F's judgment rule is kept. |
| C-§6 D2, D6, D19–D21 | No instruction change; line 40 stays "exactly four sheets" | done | Line 40 is unchanged. |
| C-§7.1 | Spec S:152: the sentence is already half present at 232 | applied to the spec | §3 D1. |
| C-§7.2 | Spec S:151 omits the anchor | applied to the spec | §3 D1. |
| C-§7.3 | Spec S:259 paraphrases 224 and does not name 210 | applied to the spec | §3 E10, express incorporation. |
| C-§7.4 | Spec S:258 against the alternatives at 208 | applied to the spec | §3 E10 keeps the exception; D27. |
| C-§7.5 | "A letter alone" is new text | applied to the spec | §3 E11. |
| C-§7.6 | S:146 and S:148 are not changes | applied to the spec | §3 C: "No change". |
| C-§7.7 | S:213 contradicts 160(b) without naming it | applied to the spec | §3 E5. |
| C-§7.8 | S:325 amends only the last sentence | applied to the spec | §4, Financing. |
| C-§7.9 | "Expedited" against H2 | applied to the spec | §4, H2. |
| C-§7.10 | "Usually Withdrew" against Withdrew's definition | applied to the spec | §3 E1: "Widen Withdrew". |
| C-§7.11 | A name grep misses the figures | applied to the spec | §9.1 greps "12.10", "49%" and "50–75". |
| C-§7.12 | The Heavy example at 220 | applied to the spec | §4 Heavy, last bullet; §9.1. |
| C-§7.13 | Incomplete reach lists in §9.1 | applied to the spec | §9.1. |
| C-§7.14 | D8's "explicit final solicitation" | applied to the spec | §1 D8 and §8. |
| C-§7.15 | The header's exact form | applied to the spec | §3 Header. |
| C-§7.16 | Items verified correct | not applicable | Nothing to act on. |
| C-§7.17 | Checker citation at S:457 | applied to the spec | §7.3 cites `:924-932`. |
| C-§4 other lists | Lists already equal or unaffected: Event labels (no label added), Type, Formality, Conditions, the condition-column values, Finality, Initiation, Exit reason, Auction screen and Whole-company bids (format unchanged), Inferred, Flag, Round, Count and Quote | not applicable | Still equal (C-§4.1). Auction screen's meaning follows D7 (C25). |

## D. Documentation, release and research

Row numbers are those of audit D §1; the live files' line numbers have since moved, and `PROPOSED_DOC_LINES.md` gives the current ones. "Now" lines were written by S6 in the live checkout; each was checked there. Deploy and release lines are drafted as proposed text (entries D1–D23, R1–R12, G1–G12) and applied at the gates.

| ID | Finding | Disposition | Where, and note |
|---|---|---|---|
| D-intro | `lesson/` is untracked and not ignored, so `git add -A` would commit it | applied to the spec | §0: never stage with `git add -A`; gate 0 stages `lesson/` only if Austin decides; gate 13 decides whether to commit it. |
| D-1 | `AGENTS.md:8` and the root README's do-not-read list lack `lesson/` | done | S6 (`AGENTS.md:8`; `README.md:37`). |
| D-2 | `AGENTS.md:12`: the working instruction | deferred | Release line, gate 9. Proposed text R2. |
| D-3 | `AGENTS.md:14`: `extraction/` | deferred | Gate 12.7. Proposed text G1. |
| D-4 | `AGENTS.md:16`: the v1.14 decision record | deferred | Gate 9. Proposed text R3, which needs gate 13's choice of record. |
| D-5 | Root README 12 and 17: current state | done | S6. |
| D-6 | Root README 14 and 23: "v1.13.2 (frozen)" | deferred | Gate 9. Proposed text R4 and R6 (the table row is now line 24). |
| D-7 | Root README 15: the nine extractions | deferred | Gate 12. Proposed text G2. |
| D-8 | Root README 5 and 16: four sheets; Excel export | deferred | Deploy line, §12 step 9a. Proposed text D5 and D6. |
| D-9 | HANDOFF line 1: date | done | S6. |
| D-10 | HANDOFF line 5: v1.14 status | done, part open | S6 wrote the "now" part (not published, not the default, not deployed). Open: the deploy sentence (D10, step 9a), the instruction sentences (R7, gate 9) and the `extraction/` sentence (G4, gate 12). |
| D-11 | HANDOFF 11–23: session state | done | S6: "Current state (25 September)". |
| D-12 | HANDOFF 27: "nine deals … none reviewed" | done | S6: thirteen deals, their run versions and the latest revisions. |
| D-13 | HANDOFF 32: Mac-Gray R01 | done | S6: applied at revisions 6–7. |
| D-14 | HANDOFF 33: source review pending | done | S6: edited and audited; Austin's source review is still pending (true under gate 11). |
| D-15 | HANDOFF 46: the working instruction | deferred | Gate 9. Proposed text R9 (now line 59). |
| D-16 | HANDOFF 48: `extraction/` are "the cockpit's only versions" | done, part open | S6 wrote the "now" part. Open: the release part, G7 (now line 61), at gate 12. |
| D-17 | HANDOFF 55–56: maintenance list | done | S6. |
| D-18 | HANDOFF 64: XLSX export | deferred | Deploy line, §12 step 9a. Proposed text D9 (now line 79). |
| D-19 | HANDOFF 77: next work | done | S6; updated in wave 2 to follow §7.13's order. |
| D-20 | CHRONOLOGY: no rows after 23 September | done | S6 added eleven dated rows; wave 2 repaired a dead link. |
| D-21 | CHRONOLOGY 42 | not applicable | Historical; left alone (§7.12). |
| D-22 | CHRONOLOGY: the new release row | deferred | Gate 9. Proposed text R12, with "D1–D27". |
| D-23 | RESEARCH_QUESTIONS 3 | done, part open | S6 wrote the "now" part. Open: the release part, R10, at gate 9 (after the deploy line D16). |
| D-24 | RESEARCH_QUESTIONS 18: Mac-Gray R01 | done | S6. |
| D-25 | RESEARCH_QUESTIONS 19: Datalink F9 | done | S6. |
| D-26 | RESEARCH_QUESTIONS 27–31: provisional conventions | done | S6. |
| D-27 | RESEARCH_QUESTIONS 33: source hierarchy | done | S6. It is also asked in the DOCX (§3.5, "Which source governs"). |
| D-28 | RESEARCH_QUESTIONS 37: reference share prices | done | S6. |
| D-29 | Tools README 19: the checker paragraph | done | S1 wrote it in the worktree; wave 3 corrected it to the final 1.7 ("This is checker 1.7, not deployed; …"). §12 step 4 changes that sentence to "deployed on <date>". |
| D-30 | Tools README 49: the importer's paths | deferred | Release line, gate 12. Now in `release/tools-readme-release.patch` (G12; `git apply --check` passed). |
| D-31 | Tools README 118: the export and the download are the same bytes | done | S3, refined in wave 3, in the worktree. |
| D-32 | Tools README 120: only added deals can be exported | deferred | Release line, gate 12. Now in `release/tools-readme-release.patch` (G12). |
| D-33 | Tools README 111–112: the example `instruction v1.14` | not applicable | It becomes correct at publication. |
| D-34 | Cockpit README 9: "None has been reviewed" | done | S6; clarified in wave 2. |
| D-35 | Cockpit README 13: Mac-Gray | done | S6. |
| D-36 | Cockpit README 20: export | deferred | Deploy line, §12 step 9a. Proposed text D17 (S3's and wave 2's download text). |
| D-37 | Cockpit README 42: publication | deferred | Gate 9. Proposed text R11. |
| D-38 | `COCKPIT_BUILD.md:47`: `choices` | deferred | Deploy line, §12 step 9a. Proposed text D1. The spec wins over the audit's "the deal's `ledger_schema`": choices follow the displayed version's schema, for a working copy its base's (§7.4 item 2; B3). D1 first followed the audit; the lead corrected it at 23:12. |
| D-39 | `COCKPIT_BUILD.md:69`: four sheets | deferred | Deploy line, §12 step 9a. Proposed text D4. |
| D-40 | `COCKPIT_BUILD.md:73`: one version per deal | deferred | Gate 12. Proposed text G9. |
| D-41 | `COCKPIT_APP_SPEC.md` | not applicable | Historical (§7.12). |
| D-42 | Maintenance README 7 | done, part open | S6 wrote the "now" part: the paste instruction is removed and the candidate supersedes the draft. Open: the first sentence ("which stays v1.13.2 and frozen") becomes false at gate 9. `PROPOSED_DOC_LINES.md` has no entry for it; §7.12's release list omits it. |
| D-43 | Maintenance README 11–13 | deferred | Historical record, left alone. A checker 1.7 line is added at the deploy: proposed text D21 (§12 step 9a). |
| D-44 | Maintenance README 26: optional note on Alex's red-font corrections | not adopted | §7.12 does not list it, and §0 treats unlisted proposals as not adopted. The fact is in `ANALYSIS_CONTRACT.md` and in P's `compare_alex` output. |
| D-45 | Maintenance README 28: "Next …" | done | S6. |
| D-46 | Maintenance README: list of deliverables | done | S6 added a status block, refreshed at about 23:30 UTC with every deliverable's status, the evidence folders and the contents of `release/`. |
| D-47 | Mac-Gray pilot README 3 | done | S6. |
| D-48 | Datalink pilot README 3 | deferred | Gate 12. Proposed text G10. |
| D-49 | Re-extraction README | not applicable | Historical. |
| D-50 | `lesson/README.md` | not applicable | Historical. A pointer file is needed only if Austin commits `lesson/` (gate 13). |
| D-51 | `lesson/…/questions-for-alex/README.md:5` | deferred | When Austin sends the DOCX (gate 8). Proposed text R1; its DOCX hash is a placeholder until A2's final file. |
| D-52 | `runs.js:6`: hard-coded `'v1.13.2'` label | done | S2 did it the spec's way (§7.4 item 8; E14): `LEGACY_INSTRUCTION_LABEL` stays for jobs with no recorded instruction. The audit's "derive it from the default" is not adopted. |
| D-53 | `import_results.py` and `verify_catalog.py`: hard-coded paths | done | S5: `release/d25-tools.patch`, regenerated against the integrated tree and applied at gate 12. Deploy-state `verify_catalog.py` is rewritten (E18). |
| D-§2.1 | How past versions reached the file | not applicable | Facts. |
| D-§2.2 | What `export_repo.py` does | not applicable | Facts, used at gates 9 and 12. |
| D-§2.3 | Who may change the file | not applicable | Respected: the team exported nothing. |
| D-§2.4 | Proposed release procedure, steps 0–14 | applied to the spec | §13, gates 0–13: deploy before runs; header fixed before the draft; the draft made from v1.13.2; export at publication. Each step is Austin's. The header step is done (C01). Nothing decides whether to leave the unused draft `73f21eb8c09a` (§11); that is Austin's. |
| D-§2.4 row | Proposed CHRONOLOGY row | applied to the spec | §13 gate 9 has the text. Note: it says "Decisions D1–D26", as does §0's table, but the decisions run to D27. Proposed text R12 uses D1–D27. |
| D-§2.4 AGENTS | Proposed `AGENTS.md` edits at release | deferred | Gates 9 and 12 (rows D-2 to D-4; proposed text R2, R3 and G1). |
| D-§2.5 | `extraction/` and `catalog.json`: options (a)–(c) | applied to the spec | D25 adopts (a); (b) and (c) are not adopted. The code is done in S5. Item 5, whether the repository copies become catalog entries, is Austin's at gate 12.6. |
| D-§2.6 | Held-out deals | applied to the spec | §8, "Held-out deals"; gates 5 and 6. Runs and any export are Austin's. |
| D-§2.7 | No change to `seed.csv` or `MANIFEST.csv` | done | Both unchanged. S3 reads `seed.csv`'s `index_url`, which agrees with `index_link()` for all nine deals. |
| D-§3.1a | Grading references are pinned to v1.13.2 | not adopted | §7.8: historical; do not reuse them for v1.14 without re-keying. |
| D-§3.1b | `effort_sweep.py` bid keys | done | S7. |
| D-§3.1c | `diff_workbooks.py` | done | S7. |
| D-§3.1d | One-off verification scripts, `lesson/` scripts, `make_seed.py` | not applicable | Historical or unaffected. |
| D-§3.1e | No script compares ledgers with Alex's coding; no estimation code | done | P: `compare_alex.py` and `derive_analysis.py`. |
| D-§3.2 | Structure of Alex's data | not applicable | Facts, used by P. |
| D-§3.3 | Map from Alex's columns to the ledger | done, part open | P: contract §§2, 6 and 9–11, and the code map in `compare_alex.py`. Open: which Exit reason maps to DropM and which to DropBelowM (P's question to Austin). |
| D-§3.4 | `bid_type` against Formality and Conditions | done | P reproduces the counts (`analysis/README.md`). Mac-Gray: 13 of 13 aligned; T0 matches 13, T1 11. P&W: 14 of 14 aligned; T0 matches 11, T1 14. The comparison goes to Alex as Decision 3b in the DOCX. |
| D-§4a | Contract elements that are mechanical: inputs, bidder units, parsing counts, partial scope, rounds, deadline classes, prices, cohort Varies, exit codes, dates | done | `ANALYSIS_CONTRACT.md` 0.1 and `derive_analysis.py` 0.2; outputs in `analysis/`. |
| D-§4b | Contract elements blocked on Alex: ranges, eligible bidders not admitted, merger of equals, same-price observations, upfront or package, the primary Formality reading, Unclear, inferred exits, the initiator, source hierarchy | done | Each is a switch with no default, emitted side by side (D22; §7.10). The answers come from Alex (DOCX §3; gate 8). The merger-of-equals "counted" variant is not computed: the rows are listed for a manual rebuild. |
| D-§4c | Which version is "the data" | deferred | Austin's decision (P's question). The tool accepts either and records which. |
| D-§4d | Market data | deferred | D23; §7.15. |
| D-§5 | Market-data supplement | deferred | D23; §7.15 keeps its outline. Blockers: the data licence and network access (Austin); the reference date and share counts (Alex). |
| D-§6 context | What exists today, and why it fails for v1.14 | not applicable | Facts. D24 and MIG answer them. |
| D-§6.1 | Reviewed-facts register | done | MIG-T: 8 deals, 520 rows, 1,561 facts. `verify` gives 454 reviewed and 66 needs decision (recounted here). It writes under `migration/`, as §7.9 authorizes, not `_dev/eval/`. |
| D-§6.2 | Content aligner | done | MIG-T (`migrate_review.py`). |
| D-§6.3 | Four-bucket triage | done | MIG-T, on both pilots. Wave 2 split "agrees" into accept and review lists. |
| D-§6.4 | Porting path | done, part open | Port batches for the two pilots are in `migration/<deal>/`; the team never applies them. Open: applying batches and setting the status is Austin's (gate 11), and two MIG-T questions (below). |
| D-§6.5 | Datalink and the held-out four | deferred | Gates 6 and 11. Datalink can be rebased freely. |
| D-§7.1 | Spec: gate order | applied to the spec | §13 gate 3. |
| D-§7.2 | Spec: "held-out" Medivation, Zep and Pepco | applied to the spec | §8 and gate 5: "not used to tune E6–E14". |
| D-§7.3 | Spec: gate 5 review has no mechanism | applied to the spec | MIG (§7.9), gate 6. MIG-T is done. |
| D-§7.4 | Spec: relocation, not overwrite; receipts packet | applied to the spec | D25, §7.7, and gate 5 (receipts copied). |
| D-§7.5 | Spec: header before the draft | applied to the spec | §3 Header and §8; C01. |
| D-§7.6 | Spec: S6 omits documents | applied to the spec | D26 and §7.12; S6 is done for "now". |
| D-§7.7 | Spec: "reviewed" working copies | applied to the spec | §7.12 and gate 11. S6 uses the corrected wording. |
| D-§7.8 | Spec: P&W #52 differs between versions | applied to the spec | §9.3 names the pilot. |
| D-§7.9 | Spec: S5 citations | applied to the spec | §7.7. |
| D-§7.10 | Spec: S3 needs no new derivation; use the seed | applied to the spec | §7.5 uses the seed and cross-checks it (S3). |
| D-§7.11 | Spec §11 is correct; the second draft is unlisted | applied to the spec | §11 lists `73f21eb8c09a`. |
| D-§7.12 | 199 against 207 tests | done | S6 explains in HANDOFF which runner gives which count. |

## E. Review of the spec's first system draft

The spec applied all 33 findings before implementation began (§11: "its findings are applied here"). The notes give the state of implementation.

| ID | Finding | Disposition | Where, and note |
|---|---|---|---|
| E1 | Relocation makes the catalog deals vanish; gate 12 then fails | applied to the spec | §7.7, D25 and gate 12 (services stopped; export before verify). Done in S5 (`data.py:686-741`, catalog lookup; `test_cockpit_catalog.py`, including a relocated download test from wave 2). The move is gate 12. |
| E2 | D13/E10 and D15 prescribe different rows for a later exclusivity request | applied to the spec | §3 E10, §4 Exclusivity and D15's cross-reference. Done in C43, C47 and S1's duplicate warning. D15's own text still says "material revision"; §3 and §8 widen it, and the candidate follows them. |
| E3 | Row-mark totals are 454/66, not 434 | applied to the spec | §7.9, §9.6 and §11. Done: MIG-T `verify` gives 454/66. |
| E4 | The pilot delta omits warning 6(a) | applied to the spec | §7.3, Reproduction. Done: S1 matches it. |
| E5 | The deploy patch ships release code and cannot carry binaries | applied to the spec | §12 steps 4, 5 and 9a. Done: the D25 paths and the release lines of the tools README are kept out of the worktree, in `release/d25-tools.patch` and `release/tools-readme-release.patch` (together `release/release-gate12.patch`); the deploy lines outside `_dev/tools` are proposed text; `release/deploy-tools.patch` (61 files, made with `git diff --no-index --binary`) carries no D25 path. Open: that patch predates open items 1 and 2 and §12 step 4, so it must be retaken. |
| E6 | Gate 0 cannot separate the earlier session's work; no gate commits the deployed code | applied to the spec | §0 and gate 3a. Done: 21 patches in `pre-existing/`. The commits are Austin's (gates 0 and 3a). |
| E7 | §12 has the team contact Alex | applied to the spec | §12 steps 1 and 11. |
| E8 | §0's read permissions miss packages' inputs | applied to the spec | §0. |
| E9 | The §4 examples reuse deals' wording | applied to the spec | §3, §4, §8, §9.1 and §9.3 (†). Done: C59; the grep is clean. |
| E10 | The round-date rule departs from D8 | applied to the spec | §3 E6 and §8, Round dates. Done: C34, C35, C38. |
| E11 | Two optional warnings conflict with D7 and D15 | applied to the spec | §7.3 change 6. Done in S1. |
| E12 | Merger-of-equals talks and partial alternatives have no row type | applied to the spec | §3 E1 and E10, §8, D27. Done: candidate lines 91 and 137, and C40. |
| E13 | P leaves mappings and switches open | applied to the spec | §7.10 and S1 change 9. Done in P (with wave-2 hardening) and `check_lean.ledger_schema()`. |
| E14 | S2.8 would label the pre-phase-4 jobs v1.14 | applied to the spec | §7.4 item 8. Done in S2. |
| E15 | Gate 11.1 would mark unreviewed copies Reviewed; the Source sheet repeats it | applied to the spec | Gate 11.1 and §7.5. Done: S3's wording (with wave 2's past-revision fix). Gate 11 is Austin's. |
| E16 | §5 asks Alex yes or no on final decisions | applied to the spec | §5, 2a and 2b. Done: the DOCX splits them ("2a. Decided, for information"; "2b. Provisional: yes or no"). |
| E17 | §9 has no acceptance for MIG-C, S5 or the runner guards | applied to the spec | §9.6. Done: MIG-C HTTP test (`test_http.py:828`), S5 tests, S7's guard test, and MIG-T's `mode=ro` test and hash check. |
| E18 | S5 does not say what `verify_catalog.py` asserts | applied to the spec | §7.7. Done in S5: four assertions; a timestamped file; refuses to overwrite. |
| E19 | Location of Alex's Q&A lost; `~/work/tmp` is both scratch and source | applied to the spec | §11 pointer (`sources/` in this folder); §0 uses `v114-scratch`. |
| E20 | Held-out hygiene has no disposition | applied to the spec | §8 and gate 6. `compare_alex` has run only on the pilots. |
| E21 | Wrong line citations | applied to the spec | §7.3 change 8 and §7.7. |
| E22 | A2's dependencies are stated three ways | applied to the spec | §5: M, R and P. |
| E23 | §0 names too many pilot READMEs | applied to the spec | §0. |
| E24 | Stale lines with no disposition | applied to the spec | §7.12. Done: maintenance README 7 and HANDOFF 18 (S6); tools README 158 (the lead, wave 3). |
| E25 | The header date is unspecified | applied to the spec | §3 Header. Done: C01, "Revision of 25 September 2026, v1.14." |
| E26 | The meaning of `Late bids accepted` is lost | applied to the spec | §7.3 message, §7.8 label and flags, §9.1. Done in S1 and S7. |
| E27 | Catalog versions have no receipt pointer | applied to the spec | §7.4 item 5. Done in S2. |
| E28 | D20 and S3 disagree on version downloads | applied to the spec | §8, Provenance. Done in S3 (raw by default; `?source=1`). |
| E29 | §12 lacks OPS's unit step | applied to the spec | §12 step 6a. OPS wrote the commands; installing them is Austin's. |
| E30 | Order loop between R and S1/S2 | applied to the spec | §7.13 wave 2. Done: R re-checked 58 of 58 value lists against the finalized checker. |
| E31 | "50–75" at line 249 | applied to the spec | §3. Done: C62. |
| E32 | No instruction for undoing a rebase | applied to the spec | Gate 11. Done: the rebase dialog says "restoring revision N, not revision 0, brings them back" (`runs.js:217`). |
| E33 | S7's acceptance names an undefined pair | applied to the spec | §9.6. Done in S7. |
| E-App A 1 | A §2.4 flags and "D11 (wider)" | applied to the spec | Through E26. |
| E-App A 2 | A13: tools README 158 | applied to the spec | Through E24. Still open (deploy line). |
| E-App A 3 | B6: undoing a rebase; "edited since"; Changes tab | applied to the spec | Through E15 and E32. |
| E-App A 4 | B10: lookup depends on `extraction/<slug>.xlsx` | applied to the spec | Through E1. |
| E-App A 5 | B20: keep the fallback label | applied to the spec | Through E14. |
| E-App A 6 | C §2 item 26: exclusivity as a "condition column" | applied to the spec | Through E2. |
| E-App A 7 | C §5: "50–75" at line 249 | applied to the spec | Through E31. |
| E-App A 8 | D row 42: maintenance README 7 | applied to the spec | Through E24. |
| E-App A 9 | D §2.6 and §6.5: held-out hygiene | applied to the spec | Through E20. |
| E-App A 10 | D §4: the four further switches | applied to the spec | Through E13. |
| E-App A 11 | D §7 item 12: test counts in HANDOFF 18 | applied to the spec | Through E24. |
| E-App A 12 | C §4: the Acquirer type list | applied to the spec | §3 D5. Done: candidate line 125. |
| E-App B, C | Citations checked; diff against the previous spec | not applicable | The incorrect items are E1, E3, E4 and E21. |

---

## Open items

These are the deferred findings and the remainders of partly done ones, each with an owner and a gate.

**The lead, wave 3 (closed at about 23:45 UTC):**
1. Tools README line 158 rewritten (A13, E24). Done.
2. The CVR/earnout Varies-with-value test added (A6, A §2.3). Done.
3. The deploy patch retaken after 1 and 2 (§12 step 5; E5): `release/deploy-tools.patch`, 61 files, SHA-256 `068b8ef7…f26d`, reproduces the worktree's `_dev/tools` from the baseline and passes `git apply --check` from the live checkout; `release/release-gate12.patch` applies on top of it. At the deploy, §12 steps 4 and 5 retake it again after the line 19 edit (and, if step 6a is approved, after correcting the README sentence near line 197 that says the TMPDIR proposal "is not applied").
4. This folder's README refreshed (D-46). Still open: line 7's first sentence ("which stays v1.13.2 and frozen") becomes false at gate 9, and no proposed text covers it (D-42): add it to the release lines at gate 9.
5. Placeholders in `PROPOSED_DOC_LINES.md` stay by design: HANDOFF's test counts (D14) take the counts of §12 step 2, and R1's DOCX hash is the hash of the file actually sent at gate 8.
6. `release/README.md` names `tools-readme-release.patch` and `release-gate12.patch` (D-30, D-32). Done. The spec's §0 table and gate-9 row say "D1–D26" although the decisions run to D27; the spec is left as written for Austin (R12 already says D1–D27).

**Austin's gates:**
7. **Gate 0:** commit the earlier sessions' work using the 21 `pre-existing/` patches (E6).
8. **Gate 3, the deploy** (B1, B-Claim 1, B-§3):
   - S1, S2 with MIG-C, S3, S4, S5's catalog lookup, S7 and OPS;
   - step 4: README line 19 to "deployed on <date>";
   - step 6a: the TMPDIR drop-ins, optional (B13, E29). The root disk is now 83% full, with 1.6 GB free;
   - step 9a: the deploy lines, `PROPOSED_DOC_LINES.md` Part 1 (D-8, D-18, D-36, D-38, D-39, D-43; B8);
   - step 11: Austin tells Alex to reload (B12).

   Gate 3a: commit the deployed code and its documentation lines (E6).
9. **Gate 4:** create the cockpit draft from published v1.13.2 and confirm its hash equals the candidate's (B11, D-§2.4). Leaving or ignoring the unused draft `73f21eb8c09a` is Austin's call.
10. **Gates 5 and 6:** the blind runs, including deals nobody read while designing v1.14 (D-§2.6, D-§7.2). Receipts are copied to a packet (D-§7.4). Held-out findings go to a separate packet, and `compare_alex` runs on a held-out deal only at Austin's request (E20, D-§6.5).
11. **Gate 8:** send the DOCX and apply R1 (D-51). Alex's answers settle the analysis switches and the source hierarchy (D-§4b, D-27).
12. **Gate 9:** publish, make default and export; apply R2–R12 (D-2, D-4, D-6, D-10, D-15, D-22, D-23, D-37). R3 (`AGENTS.md:16`) needs gate 13's choice of decision record.
13. **Gate 11:** move reviewed work deal by deal: set the status to In review, download with the Source sheet, rebase, apply the port batch (B-§4, D-§6.4). MIG-T asks Austin two questions:
    - whether the port batch should carry the old row marks at all;
    - how to apply a batch over 100 operations: as several revisions, or by raising the cap. `bulk_update` covers only Process and Round.
14. **Gate 12:** relocate `extraction/`; apply `d25-tools.patch` and `tools-readme-release.patch` (together `release-gate12.patch`); apply G1–G11 (B10, E1, D-§2.5; D-3, D-7, D-16, D-30, D-32, D-40, D-48). If the repository copies become catalog entries (12.6), `verify_catalog.py`'s one-version-per-deal check must be relaxed in the same commit (S5's question). The added deals stay cockpit-only unless Austin decides otherwise.
15. **Gate 13:** the records, and whether to commit `lesson/` (and so a pointer file; D-50, D-intro).

**Austin's other questions:**

16. **From package P** (D-§3.3, D-§4c). Answers are needed before P's tables are used for estimation:
    - the DropM/DropBelowM pairing;
    - whether "the data" means the raw runs or the reviewed working copies;
    - whether a Stock % range starting at 0 is all-cash 0 or missing;
    - whether `derive_analysis` should take the instruction version.

**Backlog:**

17. **Market data** (D-§4d, D-§5; D23, §7.15). Blockers: the data licence and network access (Austin); the reference date and share counts (Alex).
