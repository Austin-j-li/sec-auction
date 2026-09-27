# E_facts — authoritative current-state fact sheet

**As of 26 September 2026, ~21:00 UTC** (the last moment the VM is evidenced), compiled 27 September on the laptop.
Purpose: the single source the repo's state docs (`AGENTS.md`, `README.md`, `_dev/HANDOFF.md`, root `HANDOFF.md`,
`_dev/CHRONOLOGY.md`, `_dev/RESEARCH_QUESTIONS.md`, `_dev/COCKPIT_APP_SPEC.md`, `_dev/COCKPIT_BUILD.md`,
`_dev/cockpit/README.md`, `_dev/tools/README.md`) must be made to agree with.

## Evidence keys used on every claim

| Key | Source |
|---|---|
| **[S1]** | `_dev/recovery/2026-09-27-cockpit/` — live-cockpit GET snapshot, 27 Sep 10:55 UTC (`README.md`, `raw/*.json`, `instructions/*.md`) |
| **[S2-EV]** | `/tmp/recov/evidence/<path>.json` — per-file Read/Write/Edit tool events from the VM transcripts, cited by timestamp |
| **[S2-CALLS]** | `/tmp/recov/all_calls_since_0924.jsonl` — all tool calls since 24 Sep, cited by line index (`idx N`) and ts |
| **[DIGEST]** | `/tmp/calib/2026-09-2*.md` session digests, cited by file + line |
| **[ASTRA]** | `/tmp/calib/astra_report.md`, cited by line |
| **[GAP]** | `_dev/recovery/GAP.md`, cited by line |
| **[LAPTOP]** | Direct inspection of the laptop working tree, 27 Sep |

Everything below is historical evidence, not a live check. Nothing was re-run against the VM (unreachable) or the cockpit.

---

## 0. Recovery situation (context for every "must say now")

- The development tree is the VM checkout `/home/uctpiaj/work/Projects/sec-extraction` (plus worktree
  `sec-extraction-v114`; the third worktree `sec-extraction-v114-trial-20260926` was **removed** on 26 Sep).
  **SSH to the Condenser VM is unavailable since 27 Sep because the weekly bastion certificate expired**; the cockpit
  web app itself was still serving that morning through Cloudflare Access. [S1 `README.md`:3]
- Laptop and `origin/extraction-v2` are both at **`679d4fc`** ("Cockpit phase 5", 23 Sep). **Nothing after 23 September
  was committed anywhere.** The VM's main checkout had **91 uncommitted entries** (its `git status`, 26 Sep 20:43) and
  `sec-extraction-v114` **74 more** (26 Sep 18:46). [GAP:3]; corroborated by `git worktree list` showing all three trees
  at `679d4fc` on 26 Sep 18:38 [ASTRA:61].
- Recovery happens on branch **`local-recovery-2026-09-27`**, off `679d4fc`; rebuilt material is to be reconciled against
  the VM tree when SSH returns. [TEAM_BRIEF:4; GAP:78]
- The 27 Sep cockpit snapshot is **the only off-VM copy of cockpit state after 23 September**. [S1 `README.md`:5]
- **Lost / VM-only:** `_dev/cockpit/state/workspace.sqlite3` and its stored-file tree, `~/backups/ledger-cockpit/`,
  the uncommitted source (checker 1.8, analysis/migration/provenance tools, server/worker/frontend), the
  `2026-09-2{4,5,6}-*` maintenance packets, `_dev/reviews/2026-09-26-*`, the questionnaire DOCX, the `sec-extraction-v114`
  worktree. [S1 `README.md`:57-64; GAP:34-36, 64-71]
- Last verified backup: **`~/backups/ledger-cockpit/20260926-193859Z`** — taken *before* the 20:18 publication and the
  five reruns; no later backup is evidenced. [ASTRA:75]

---

## 1. Instruction versions, hashes, default, who published and when

All four cockpit-stored texts are in `_dev/recovery/2026-09-27-cockpit/instructions/`; I recomputed SHA-256 on the
laptop copies and each matches the hash the cockpit records [S1 `raw/instructions.json`; LAPTOP `shasum -a 256`].

| Version / id | SHA-256 | Status in cockpit | Created / published by, when | Size |
|---|---|---|---|---|
| **v1.14.1**, id `08caed447f7d` | `8a93df3cc6d989386958e9cb2d74ab34ebc0f07d281e8cc398605a388e066c98` | **published, DEFAULT** (`default_id: 08caed447f7d`) | created_by `austin` 26 Sep **20:18:24**; published_by `austin`, published_at **26 Sep 20:18:33 UTC**; `edits: 2` | 353 lines, 6,500 words (laptop `wc`) |
| v1.13.2, id `513c8e3e8159` | `513c8e3e8159e4a6bceccd6ffca32a246302736329a0c7137b64dd3b7ffcd304` | published, no longer default | created/published by `system`, **23 Sep 16:58:19** ("Imported from `SEC_Deal_Ledger_Extraction_Instruction.md` in the repository") | 269 lines, 5,557 words |
| draft `a4ca26ecfa92` — the 24 Sep **v1.14 pilot draft** | `f9595d7413149f86c074f1d4b9ef96a5a24b3d8dd9b6c11061b0bd6e889aea97` | **draft, never published, never default** | `austin`, **24 Sep 22:41:09**; label "draft f9595d7 (Austin)"; `edits: 2` | 288 lines, 6,600 words |
| draft `73f21eb8c09a` — unused | `513c8e3e…cd304` (byte-identical to v1.13.2) | draft, unused | `austin`, **24 Sep 09:26:36** | 269 lines |

Cockpit note recorded on v1.14.1: *"Streamlined v1.14 (29 columns; 40-word Notes; Same as #n; five-Question cap), with
the 26 Sep wording edits on rounds, Count, Initiation, diligence, CVR and the process Question. Checked by checker 1.8."*
[S1 `raw/instructions.json`]

**Texts that exist but were never cockpit versions**

- **25 Sep v1.14 candidate**, SHA-256 `c2d47a47…8ab27`, 9,747 words, the frozen input of the 15-run trial; implements
  D1–D27; **never published**. [ASTRA:27; GAP:23]
- **26 Sep v1.14.1 candidate as reviewed**, SHA-256 `8bdb7c205512c9bcf55ffa7623fba0a8bb4aabaed23c99845fa88b4a80cc8a79`,
  6,417 words. **This hash was not the published text.** After Austin approved eight wording fixes it became
  `8a93df3c…66c98`; the reviewed text is preserved on the VM as
  `_dev/maintenance/2026-09-26-v1141-streamline/checks/candidate-8bdb7c20-as-reviewed.md` (directory listing confirms the
  file exists). [ASTRA:28; S2-CALLS idx 1175 (20:47:38) and idx 1167 (20:46:54, `ls checks/` output)]
- The **eight approved wording fixes** are PIPELINE_UPGRADE_REPORT candidate issues **2 and 4–10**; issue 6
  (documentation-only diligence) was implemented as **Incomplete**, not the report's proposed **Complete** — a
  deviation Claude disclosed. [S2-CALLS idx 1175; ASTRA:29; DIGEST `2026-09-26T1845_a7e6612a.md` "One deviation: for the
  documentation-only rule (issue 6) I used Incomplete instead of the report's Complete"]

**Authorship / attribution (important, and corrected on the VM itself)**

The cockpit records `published_by: austin` and every run `started_by: austin` [S1]. That attribution is the **browser
account**, not manual human action: a **forked Claude session acted through Austin's browser session** to publish, set
the default and start the five reruns. The original session first told Austin he had done it himself and corrected this
at 20:52. [DIGEST `2026-09-26T1845_a7e6612a.md` 20:52:46 "A forked copy of this session did this, in your browser
session… I told you earlier that you'd done it yourself; that was wrong"; ASTRA:97] The VM docs were then edited to say
"at Austin's order, under his account" rather than "by Austin" [S2-CALLS idx 1253, 20:50:34].

**Repository instruction file**

- On the VM at 20:45–20:52 the root `SEC_Deal_Ledger_Extraction_Instruction.md` was **still v1.13.2**;
  `export_repo.py instruction v1.14.1 --write` had **not** been run and remained an explicit GATE.
  [S2-CALLS idx 1175, idx 1263; ASTRA:34]
- **Contradiction with the laptop as it stands now:** the laptop file
  `/Users/austinli/Projects/sec-auction/SEC_Deal_Ledger_Extraction_Instruction.md` hashes to
  **`8a93df3c…66c98`** (v1.14.1) with mtime **27 Sep 12:17** [LAPTOP]. Every other state doc still has the 23 Sep
  baseline mtime (23 Sep 22:08). This file was therefore written **today, during this recovery session**, not recovered
  from the VM; GAP:25 still lists the export as "Pending export". Treat the VM's state (v1.13.2 in the repo file) as the
  26 Sep fact, and the laptop's v1.14.1 root file as a recovery-branch action that must be described as such.

**Two evidence Reads of the repository instruction** exist on the VM (24 Sep 21:55 latest), with no Write/Edit —
consistent with "never exported". [S2-EV `SEC_Deal_Ledger_Extraction_Instruction.md.json`: 2 Read events, last
2026-09-24T21:55:41Z]

---

## 2. Checker / pipeline versions and behaviours

### 2.1 Deployment fact

The v1.14-derived code, **retargeted to v1.14.1**, was deployed to the main VM checkout at Austin's order on
**26 Sep 19:41 UTC** (`deploy-tools-v1141.patch`, WP7 which includes WP1). Tests before deploy: **336 unit, 20 HTTP,
77 vitest**. Frontend rebuilt; `ledger-cockpit` and `ledger-worker` restarted at 19:41 and again **19:45** to load the
published instruction's hash; the worker was restarted again during the retest. Backup
`~/backups/ledger-cockpit/20260926-193859Z`; rollback tarball `~/work/archive/v1141-deploy/pre-v1141-tools.tgz`;
`dist.old` kept. [S2-CALLS idx 1175, idx 1193 (20:48:15), idx 1164 (20:46:48); ASTRA:41]
Caveat carried from the evidence: the 336/20/77 figure is **not** evidence that the full browser/release gates were
rerun. [ASTRA:41]

### 2.2 `check_lean.py` — **checker 1.8**

- Selector `--rules v1.14 | v1.14.1`. The cockpit chooses by mapping the **instruction's SHA-256** through
  `check_lean.RULES_BY_INSTRUCTION`. A **29-column workbook with no known instruction defaults to v1.14.1**; the fifteen
  trial workbooks keep **v1.14** by explicit selection. [S2-CALLS idx 699 (19:02:57, tools README text)]
- Final hash map after publication: **`8a93df3c…` (published v1.14.1) and `8bdb7c20…` (its reviewed text) → v1.14.1;
  `c2d47a47…` → v1.14; 24 Sep draft `f9595d74…` → v1.14.** Both v1.14.1 hashes map to the same rules. The `8a93df3c`
  entry was added **after** publication, in both trees. [S2-CALLS idx 1246 (20:50:09, tools README replacement),
  idx 1187 (20:48:02 SendMessage: "new hash 8a93df3c…6c98, added to RULES_BY_INSTRUCTION in both trees")]
- v1.14.1 rules enforced (from the tools README text the VM wrote): a **Note over 40 words is an error**; `Inferred = Y`
  only on exit, `Round opened` and `Process restarted` rows; `Formality Unclear` only on cohort rows; `Antitrust Y`
  requires `Regulatory Concern`; `Stock %` a number 0–100, `Part stock`, `Not stated` or `Varies`. [S2-CALLS idx 699]
- Later refinement of the same README paragraph: **Count required on `Bidding group changed`** (a blank Count on a
  process marker is only a **warning**); Round 0 after round 1 opened is an **error**; `"Same as #n"` must point to an
  earlier bid row of the same bidder; `Bid reaffirmed` is Formal with `"Same as #n"`. **Warnings** for: a Heavy row whose
  Note does not start `H1:`/`H2:`/`H3:`, Light lacking `Due diligence` Complete or Incomplete, a Question over 60 words,
  and **above five Questions — the process Question not counted**. [S2-CALLS idx 902 (19:23:27)]
- The report field **`ledger_schema`** states which rules applied. Any workbook that is not 29-column is checked as
  v1.13.2, unchanged. [S2-EV `_dev/tools/README.md.json`, Edit 2026-09-24T22:02:49Z (the checker-1.6 ancestor of this
  wording); S2-CALLS idx 699]
- **Version lineage:** 1.5 (recorded on the nine catalog imports) → **1.6** deployed 24 Sep 22:02 (v1.14-draft rules on
  `Stock %` ledgers) → **1.7** built 25 Sep in `sec-extraction-v114`, never deployed → **1.8** deployed 26 Sep 19:41.
  [S1 per-version `checker.checker_version`; ASTRA:13, :15; S2-EV `_dev/tools/README.md.json` 24 Sep 22:02 Edit]
- Source state on the VM: `check_lean.py` 1,882 lines, full Read from the v114 tree at 18:32, then merged into main and
  given the `8a93df3c` `RULES_BY_INSTRUCTION` entry. `test_check_lean.py` 786 lines (v114 tree, full Read).
  [GAP:41-42; S2-EV `_dev/tools/check_lean.py.json` events 18:32:24–18:53:36]

### 2.3 `derive_analysis.py` — **0.3**, analysis contract **0.2**

Confirmed by the literal edit `TOOL_VERSION = "0.2" / CONTRACT_VERSION = "0.1"` → `TOOL_VERSION = "0.3" /
CONTRACT_VERSION = "0.2"` at 26 Sep 19:11:21 in `sec-extraction-v114`. [S2-EV `_dev/tools/derive_analysis.py.json`]
Other behaviour changes in the same 19:11–19:12 edit run [same source]:

- Gains `--rules v1.14|v1.14.1`; a 29-column workbook has identical headers under both, so `--rules` says which
  instruction made it; **with no selection it is read under v1.14.1** (check_lean's default).
- Field-level `Inferred` is **v1.14 only**; under v1.13.2 **and v1.14.1** `Inferred` marks an inferred *event*, so on an
  exit row it is an inferred exit.
- New `RETIRED_V1141` set: switches a v1.14.1 workbook cannot feed, because the content they compared was deleted or the
  rule became mechanical.
- **P1** implemented: `USABLE_PRICE_KINDS` / `upfront_price_kind()` — what the two price cells give, from validated
  values only (a point needs two valid equal prices; a range two valid ordered unequal ones; a filled-but-invalid cell or
  a reversed range is invalid). P1 is the surviving item of the Astra packet's `AMENDMENT_SPEC.md`. [S2-CALLS idx 1261]
- `stock_bounds()` gains note/v1141 handling: v1.14 records a stated range in the cell, **v1.14.1 (E13) records
  `Part stock` with the range in the Note**.
- `package_basis()` switches on schema rather than a `v114` bool; `auction_screen()` gains `uncertain=False` because
  **v1.14.1 E1 has no `Uncertain`**.
- GAP additionally describes 0.3 as providing **T0–T3 formality readings**; source is a 1,037-line full Read plus these
  8 edits. [GAP:43]. Tests `test_derive_analysis.py`, 556 lines, Exact from the v114 tree [GAP:44].
- Retest outputs exist on the VM under `_dev/reviews/2026-09-26-v1141-retest/analysis/`: `derive_analysis` folders for
  all five deals, plus `formality_agreement.py`/`.json`/`.csv`. [DIGEST `2026-09-26T1845_a7e6612a.md`:707-709]

### 2.4 `migrate_review.py`

Deployed 26 Sep with the **v1.14.1 impact tags**. Documented behaviour after the 20:50 README edit: *"moves reviewed
v1.13.2 work onto a deal's v1.14.1 run (D24; a v1.14 run with `--rules v1.14`), tagging the facts that v1.14.1's changes
(R1–R6, V1141_SPEC D1–D6) or V114_SPEC's D1–D27 require judging again."* CLI gains `[--rules v1.14]` on `triage`.
[S2-CALLS idx 1246; idx 1164]. Source: 975-line full Read + 2 edits; tests `test_migrate_review.py` 478 lines, Exact.
[GAP:45-46]

### 2.5 `compare_alex.py`

New tool, **no content anywhere in the evidence** — class **Rebuild**. [GAP:47] What is known:
- It exists in the VM tree (`git status` untracked list shows `_dev/tools/compare_alex.py` and
  `_dev/tools/test_compare_alex.py`). [S2-CALLS idx 337 (26 Sep 12:41:51), idx 489 (18:32:25)]
- Analysis contract 0.1 names it: *"Tool: `_dev/tools/derive_analysis.py` 0.2, with `_dev/tools/compare_alex.py` for the
  side-by-side with Alex's coding."* [S2-CALLS idx 538 (18:33:42), quoting `ANALYSIS_CONTRACT.md`]
- It emits at least `{"ledger_schema": ledger["schema"], "alex_file…}` at `compare_alex.py:351`. [S2-CALLS idx 535]

### 2.6 Default model and other pipeline items

- **Default extraction engine: Claude Opus 5.5 at medium effort** (`claude-opus-5-5`, transport `opus`), restored by
  Austin on the evening of 26 Sep, reversing that morning's GPT-6-Astra-high default; **live since the 19:41 deploy**.
  `prepare` defaults to that transport/model/effort. **GPT-6-Astra stays selectable and keeps high effort as its own
  default** (`--provider sol`). [S2-CALLS idx 699, idx 1147/1148; S2-EV `AGENTS.md.json` Edit 20:46:00]
- Astra-high had been made default at **26 Sep 12:02:33 UTC** with a service restart for that change only.
  [S2-CALLS idx 709 (CHRONOLOGY row); ASTRA:16]
- Also deployed: `effort_sweep.py` and `sandbox/run_model.py` updates; cockpit schema awareness, safe rebase, the
  **Source** sheet in downloads, the bulk Process/Round edit, the catalog lookup, `provenance.py`. [S2-CALLS idx 1175,
  idx 1193]
- Per-user run cap (`runs.CAPS`) is **2**; it was raised to 3 for the retest batch and **restored to 2**.
  [S2-CALLS idx 1018, idx 1254]
- `diff_workbooks.py`, `fetch_filing.py`, `findings_text.py` and their tests were modified, **no content in evidence**
  (Rebuild; likely 29-column schema updates). [GAP:49]

---

## 3. Cockpit state (deals, versions, working-copy bases, reruns, check results)

Snapshot taken 27 Sep 10:55 UTC; it is the state left at ~20:55 on 26 Sep, unchanged since (no writes). [S1 README:3]

**13 deals.** Nine catalog deals (Datalink, Kraton, Mac-Gray, Meredith, Penford, PetSmart, Providence & Worcester, sTec,
Synacor) plus four added in the cockpit: Medivation (23 Sep), Zep, Pepco Holdings, Imprivata (24 Sep). Filings for the
four added deals are not in `raw_filing/` but their text is in `raw/filing__<slug>.json`. [S1 `raw/deals.json`; S1
README:44-45]

### 3.1 Working copies — all still based on v1.13.2

Every deal's `workspace.base_instruction_version` is **v1.13.2**, `base_instruction_sha256` `513c8e3e…cd304`,
`base_ledger_schema` v1.13.2. **No working copy has been rebased onto a v1.14.1 run.** [S1 per-deal `workspace`]

| Deal | Working revision | Base version | Live working-copy check (checker 1.8, v1.13.2 rules) | review_status |
|---|---:|---|---|---|
| Datalink | 0 | `opus55-medium` (catalog) | 0 E / 21 W | unreviewed; Austin review pending |
| Kraton | 4 | `opus55-medium` | 0 E / 20 W | unreviewed; Austin review pending |
| Mac-Gray | 8 | `opus55-medium` | 0 E / 24 W | unreviewed; Austin review pending |
| Meredith | 4 | `opus55-medium` | 0 E / 15 W | unreviewed; Austin review pending |
| Penford | 2 | `opus55-medium` | 0 E / 15 W | unreviewed; Austin review pending |
| PetSmart | 2 | `opus55-medium` | 0 E / 20 W | unreviewed; Austin review pending |
| Providence & Worcester | 16 | `opus55-medium` | 0 E / 13 W | unreviewed; Austin review pending |
| sTec | 1 | `opus55-medium` | 0 E / 20 W | unreviewed; Austin review pending |
| Synacor | 1 | `opus55-medium` | 0 E / 9 W | unreviewed; Austin review pending |
| Medivation | 0 | `opus55-medium-20260923-1631-9dd02c` | 0 E / 3 W | unreviewed |
| Zep | 0 | `opus55-xhigh-20260924-0926-ee06ac` | 0 E / 21 W | unreviewed |
| Pepco Holdings | 0 | `opus55-medium-20260924-0943-b762af` | 2 E / 27 W | unreviewed |
| Imprivata | 0 | `opus55-xhigh-20260924-1651-fe7897` | 0 E / 22 W | unreviewed |

Deal-level `deal_review.status` is `in_review` where a working copy exists (no status explicitly set), matching the
handoff's "shown as In review by default". [S1; S2-EV `_dev/HANDOFF.md.json` 18:46 snapshot line 42]
Eight of the nine catalog deals have edited working copies; **Datalink has none**. [S1 README:47-55, matches the
18:46 handoff exactly]

### 3.2 All stored run versions

| Deal | Version id | Instruction | Engine/effort | Started (UTC) | Checker recorded at import |
|---|---|---|---|---|---|
| Datalink | `opus55-medium` (catalog) | v1.13.2 | Opus 5.5 medium | 22 Sep | 1.5 — 0 E / 21 W |
| Kraton | `opus55-medium` | v1.13.2 | Opus 5.5 medium | 22 Sep | 1.5 — 0 E / 20 W |
| Mac-Gray | `opus55-medium` | v1.13.2 | Opus 5.5 medium | 22 Sep | 1.5 — **1 E** / 26 W |
| Meredith | `opus55-medium` | v1.13.2 | Opus 5.5 medium | 22 Sep | 1.5 — 0 E / 16 W |
| Penford | `opus55-medium` | v1.13.2 | Opus 5.5 medium | 22 Sep | 1.5 — 0 E / 15 W |
| PetSmart | `opus55-medium` | v1.13.2 | Opus 5.5 medium | 22 Sep | 1.5 — **1 E** / 22 W |
| P&W | `opus55-medium` | v1.13.2 | Opus 5.5 medium | 22 Sep | 1.5 — 0 E / 12 W |
| sTec | `opus55-medium` | v1.13.2 | Opus 5.5 medium | 22 Sep | 1.5 — 0 E / 21 W |
| Synacor | `opus55-medium` | v1.13.2 | Opus 5.5 medium | 22 Sep | 1.5 — **1 E** / 8 W |
| PetSmart | `opus55-medium-20260923-1528-4d8363` | v1.13.2 | Opus 5.5 medium | 23 Sep 15:28:19 | 1.5 — 1 E / 6 W |
| Medivation | `opus55-medium-20260923-1631-9dd02c` | v1.13.2 | Opus 5.5 medium | 23 Sep 16:31:00 | 1.5 — 0 E / 3 W |
| Zep | `opus55-xhigh-20260924-0926-ee06ac` | v1.13.2 | Opus 5.5 **xhigh** | 24 Sep 09:26:06 | 1.5 — 0 E / 21 W |
| Pepco Holdings | `opus55-medium-20260924-0943-b762af` | v1.13.2 | Opus 5.5 medium | 24 Sep 09:43:14 | 1.5 — 2 E / 27 W |
| Imprivata | `opus55-xhigh-20260924-1651-fe7897` | v1.13.2 | Opus 5.5 **xhigh** | 24 Sep 16:51:08 | 1.5 — 0 E / 22 W |
| Mac-Gray | `opus55-medium-20260924-2241-d7d267` | v1.14 **draft** `f9595d7` (pilot) | Opus 5.5 medium | 24 Sep 22:41:20 | **1.6**, schema v1.14 — 1 E / 16 W |
| P&W | `opus55-medium-20260924-2241-38bc24` | v1.14 **draft** `f9595d7` (pilot) | Opus 5.5 medium | 24 Sep 22:41:19 | **1.6**, schema v1.14 — 0 E / 14 W |
| **Mac-Gray** | `opus55-medium-20260926-2019-1d1d60` | **v1.14.1** | Opus 5.5 medium | **26 Sep 20:19:06** | **1.8**, schema v1.14.1 — **0 E / 2 W** |
| **P&W** | `opus55-medium-20260926-2019-366a73` | **v1.14.1** | Opus 5.5 medium | **26 Sep 20:19:06** | **1.8** — **0 E / 2 W** |
| **sTec** | `opus55-medium-20260926-2027-0643aa` | **v1.14.1** | Opus 5.5 medium | **26 Sep 20:27:11** | **1.8** — **1 E / 3 W** |
| **Synacor** | `opus55-medium-20260926-2028-342883` | **v1.14.1** | Opus 5.5 medium | **26 Sep 20:28:43** | **1.8** — **0 E / 6 W** |
| **Datalink** | `opus55-medium-20260926-2032-350a91` | **v1.14.1** | Opus 5.5 medium | **26 Sep 20:32:04** | **1.8** — **1 E / 4 W** |

All from [S1 per-deal `versions[]` and `raw/deal__*_version_*.json`; rerun table also [S1 README:32-40] and
[ASTRA:45-53]]. Every version's `started_by` is `austin` (browser account; see §1 attribution).
**34 stored version workbooks total, all present as `.xlsx` exports in the snapshot.** [GAP:32]

Arithmetic cross-check: the nine catalog versions' recorded counts sum to **3 errors and 161 warnings**, exactly the
figure the 26 Sep 18:46 handoff gives for "the nine workbooks". [S1; S2-EV `_dev/HANDOFF.md.json` 18:46, line 50]

### 3.3 The five v1.14.1 reruns (retest) in detail

Ordered by Austin ("publish it in the cockpit, and then do the 5 deal rerun"; Datalink "extracted with the new system").
Checked after each run by checker 1.8 under the v1.14.1 rules. Three ran concurrently after the cap was lifted to 3.
[S2-CALLS idx 1018 (20:42:57, the retest README heredoc)]

| Deal | Minutes | Cost USD | Checker 1.8 | Rows (trial rows) |
|---|---:|---:|---|---|
| mac-gray | 8 | 2.25 | 0 E / 2 W | 53 (64) |
| providence-worcester | 9 | 2.29 | 0 E / 2 W | 58 (63) |
| stec | 7 | 1.77 | 1 E / 3 W | 56 (66) |
| synacor | 13 | 2.94 | 0 E / 6 W | — |
| datalink | 9 | 2.34 | 1 E / 4 W | — |

Acceptance (`acceptance.json`, `retest_acceptance.py`) [S2-CALLS idx 1018]:
- **Mac-Gray** all pass: 16 unnamed signers `Did not submit` dated 23 July (row 17); October liability revisions are
  blank-price Bid rows (47, 48); Party A's 18 September bid Heavy (H1) and Formal (row 37).
- **P&W** script reports FAIL on "16 non-submitters, Count 16", but the workbook has 16 — Party A's own `Did not submit`
  (row 16) plus a cohort of 15 (row 17), as E3 requires. **The check is too strict, not the workbook.** Party E not H2,
  G&W Regulatory Concern (51), Party C not `Not begun` (23) pass. REVIEW flag on NDA rows 8–10, 22.
- **sTec:** Company H `Dropped by target` by 16 May, reason "Would not improve earlier offer" (37); WDC's standstill
  warning a Bid with H3, no price (54); two rounds.
- **Synacor:** 3 processes, 6 rounds.
- **Datalink:** 1 process, **4 rounds** (F9 recorded 5) — expected and accepted under Austin's 26 Sep decision. Round 1
  opens **28 January** (first price negotiation with Party A), not F9's 29 January. Rounds 2 (6 June) and 4 (1 October)
  are trigger (d); round 3 (16 August) is the announced final round.
- **All five:** no Note over 40 words; at most four Questions besides the process Question; fewer rows than the trial for
  the three trial deals.

Checker findings [same source]:
- **Both errors are the same slip:** sTec row 56 and Datalink row 76 carry **Count 1 on the `Merger announced` row**,
  whose Who is the winner. D1 col. 20 blanks Count "on rows about no bidder"; the checker treats `Merger announced` as a
  no-bidder row. **This is a v1.14.2 wording candidate, not a per-deal patch.**
- Warnings: Questions over 60 words in **every** deal (D4); Synacor's two `Process restarted` rows have blank Count
  (rows 14, 22); sTec row 19 a one-sided price without floor/ceiling wording; Datalink row 71 an `Exclusivity changed`
  row possibly repeating bid row 69.

### 3.4 Other cockpit state

- **Accounts:** Austin connected Claude 23 Sep 15:26; Alex connected 24 Sep 09:19 and **has made no run**. All extraction
  jobs were started under Austin's account. [S2-EV `_dev/HANDOFF.md.json` 18:46, line 17]
- **Review marks:** 454 reviewed and 66 needs-decision across all **520** Deal-ledger rows; these are agent-assisted
  review work, **not Austin's review**. One finding decision (**Mac-Gray R01**, present in the snapshot as
  `raw/document__mac-gray__mac-gray-r01.json` and in Mac-Gray's `findings[]`) and **three comment threads**.
  [S2-EV `_dev/HANDOFF.md.json` 18:46 line 42; S1 `raw/deal__mac-gray.json` findings/documents; ASTRA:11]
- Three edit clusters were reverted on 24 Sep: Kraton revision 4, Meredith revision 4, PetSmart revision 2.
  [S2-EV `_dev/HANDOFF.md.json` 18:46 line 42]
- **`ledger_schema` on the v1.14.1 rerun payloads is `v1.14.1`**; on every working copy it is `v1.13.2`. One deal can
  therefore hold versions of both schemas — the reason `choices` is schema-dependent. [S1; S2-CALLS idx 1232]

---

## 4. Decisions made 24–26 September, with dates and evidence pointers

| When (UTC) | Decision | Evidence |
|---|---|---|
| 24 Sep 08:25–08:40 | Austin approved trimming questions Alex had already answered; the (older) questionnaire was replaced in team Dropbox, hash matched. **No direct message to Alex.** | [ASTRA:12], DIGEST `2026-09-24T0822_431d7060.md` 08:27:13, 08:40:45 |
| 24 Sep, day | Austin specified the **expanded bid taxonomy** (22 → 29 columns). Claude interpreted Austin's "confided … sitting right next to him" as confirmation with Alex. | [ASTRA:13], DIGEST `2026-09-24T0949_67eb2572.md` 17:48:50 |
| 24 Sep 22:02 | **Checker 1.6** + editor value lists + deal-level Review status deployed; services ran the uncommitted tree from then. | [S2-EV `_dev/tools/README.md.json` Edit 22:02:49]; [S2-EV `_dev/HANDOFF.md.json` 18:46 line 16] |
| 24 Sep 22:39–22:54 | Austin: "Proceed." v1.14 cockpit **draft** created (`a4ca26ecfa92`) and two pilots run as Austin, Opus 5.5 medium: Mac-Gray 1 E/16 W, P&W 0/14. **Draft never published; working copies unchanged.** | [ASTRA:14]; [S1 `raw/instructions.json`, per-deal versions] |
| 25 Sep, to ~23:30 | Austin's **D1–D27** decisions; v1.14 candidate (`c2d47a47…`, 9,747 words) frozen after independent review R (27 findings, all fixed); checker 1.7, analysis/migration/provenance tools and cockpit changes built in `sec-extraction-v114`. **Built, not deployed or published.** Originating session transcript is absent. | [ASTRA:15, :27]; [S2-EV `_dev/HANDOFF.md.json` 18:46 lines 19, 93] |
| 26 Sep, morning–10:10 | **15 authorized blind runs** (3 deals × 5 settings) packaged; Pro and Fable grading disagreed. | [ASTRA:16] |
| 26 Sep 12:02:33 | **GPT-6-Astra high made the extraction default**; both services restarted for that change only. | [S2-CALLS idx 709 CHRONOLOGY row; ASTRA:16] |
| 26 Sep 16:10–16:50 | Austin's rulings settle the two sixteen-bidder cohorts, Company H's target-side exit, and commitment-only bids without fresh prices → **H1–H4**. | [ASTRA:16]; DIGEST `2026-09-26T1158_e6632a28.md` 16:10:10, 16:50:09 |
| 26 Sep 17:07–18:44 | Austin chooses simpler defaults, forecasts counting as evidence, the **NDA test** for diligence, and a **return to Opus medium**. Claude drafts v1.14.1, then the pipeline spec. **Austin approves Q1–Q4 at 18:44.** Trial packet relocation verified (296 files identical); redundant trial worktree removed. | [ASTRA:17]; DIGEST `2026-09-26T1717_b88de679.md` 17:28:10, 18:41:46, 18:44:39 |
| 26 Sep 19:43:46 | Austin's questionnaire answer explicitly chooses **all wording fixes, default now, cockpit runs**. | [ASTRA:98]; [S2-CALLS idx 948 (19:41:58) — the AskUserQuestion options he chose among] |
| 26 Sep 19:41 | **Deploy** (WP7 incl. WP1): checker 1.8, rules selector, derive_analysis 0.3, migrate_review, Opus 5.5 medium default. Services restarted; again 19:45 for the hash map. | [S2-CALLS idx 1175, 1193]; [ASTRA:41] |
| 26 Sep 20:18:24 / 20:18:33 | **v1.14.1 created and published, and made the cockpit default**, id `08caed447f7d`, hash `8a93df3c…66c98`, under Austin's account at his order. v1.13.2 stays published, no longer default. | [S1 `raw/instructions.json`]; [ASTRA:42]; [S2-CALLS idx 1253] |
| 26 Sep 20:19–20:32 | **Five v1.14.1 reruns** started and completed (§3.3). | [S1]; [ASTRA:43-53]; [S2-CALLS idx 1018] |
| 26 Sep, after retest | **Austin: Datalink follows the v1.14.1 text — four rounds**, superseding the 21 Sep **F9** five-round ruling. "The same reasoning applies to Kraton and Meredith." Closes candidate issue 1. | [S2-CALLS idx 1175, idx 1216, idx 1208] |
| 26 Sep 20:43–20:55 | Two sessions collided over documentation; the fork stopped its staleness agent, the original session took ownership; ~45-file cleanup and questionnaire regeneration reported complete. **No commit, push, or questionnaire delivery.** Final exchange: `lesson/` is old but not the kind of staleness that needs fixing; Claude is not permitted to open it. | [ASTRA:19]; [S2-CALLS idx 1187, idx 1212]; DIGEST `2026-09-26T1845_a7e6612a.md` 20:52:46–20:55:04 |

**Content of the 26 Sep rulings, for the docs:**
- **H1** Company H is `Dropped by target` when the final-round letters went to WDC and Company D (by 16 May), reason
  "Would not improve earlier offer". **H2** P&W's sixteen inferred non-submitters. **H3** Mac-Gray's permitted 23 July
  inferred closure. **H4** non-price commitment changes keep a blank price and are **not** new price observations.
  [S2-CALLS idx 689, idx 705]
- **R1** "Same offer" replaces express incorporation (E10): only a row whose bidder says its earlier offer stands copies
  that row ("Same as #n"). **R2** evidence window replaces the date-level evidence rule — what the filing says about a
  bid up to that bidder's next row describes it, **forecasts included**. **R3** cohort closure: unnamed members of a
  total with no reported offer are one `Did not submit` row at the first due date after they appear, Count by
  subtraction, **no range, no Question**. **R4** limits H2 to a period tied to diligence alone. **R5** removes E14's
  reserve and continuing-discussion exceptions: a bidder not invited into the next stage is `Dropped by target` when it
  opens. **R6** makes `Not begun` an **NDA test**, not a diligence-access test. [S2-CALLS idx 705]
- **D1–D6 (V1141_SPEC)**: D1 drops the "refers back" route — a revision is Formal only if it meets a route itself;
  D6 makes "after a suspension" trigger (d) — a pause of ≥30 days with no request, or an ended exclusivity period; the
  count-once sentence was cut. E5 becomes a checkable test: ≥90 days with no reported sale contact (or a reported end),
  no offer outstanding, then a fresh target step. E9 has five deadline outcomes: Extended, Extended (late bid accepted),
  Enforced, Passed without action, Unclear. E13 puts a stated stock range in the Note under `Part stock`. E1 drops
  `Uncertain`. [S2-CALLS idx 689, idx 1175]
- **Q1–Q4 (PIPELINE_UPGRADE_SPEC §3, approved 18:44)**: Q1 a `--rules v1.14|v1.14.1` selector chosen from the
  instruction hash; Q2 the process Question does **not** count toward the five-Question cap; Q3 D1–D6 as the candidate
  has them; Q4 Mac-Gray Party B's 18 September bid becomes Contingent and Heavy (H1) under R2. [S2-CALLS idx 705]
- **Astra packet consequences:** `AMENDMENT_SPEC.md` A1–A4 superseded (**P1 survives and is implemented in the deployed
  `derive_analysis.py` 0.3**); `DECISION_BRIEF_2026-09-26.md` §§1–4, §6, §7 resolved. [S2-CALLS idx 705, idx 1261]

---

## 5. Open items / next steps (as left at ~21:00 on 26 Sep)

**GATEs — each needs Austin** [S2-CALLS idx 1175, idx 1164, idx 1263; DIGEST `2026-09-26T1845_a7e6612a.md` 20:52:46;
ASTRA:57]:

1. **Kraton's two rounds.** The regenerated questionnaire now shows Kraton as following the v1.14.1 text (**two
   rounds**), extrapolated from Austin's Datalink reasoning ("the same reasoning applies") and the published sentence
   that a selection asking for no offers opens no round. **This is an assistant extrapolation and explicitly awaits
   Austin's confirmation.** Meredith is named in the same "same reasoning applies" sentence but the questionnaire change
   was made only for Kraton. [DIGEST `2026-09-26T1845_a7e6612a.md`:721, :751; S2-CALLS idx 1175, idx 1216; ASTRA:103]
2. **Rebasing working copies onto v1.14.1 runs, and gate 12.** No working copy has been rebased; gate 12 (moving the
   nine `extraction/` workbooks, still the 22 Sep v1.13.2 Opus extractions) is not done. The per-deal rule stands: a
   working copy stays as it is until that deal's **v1.14.1** run has been reviewed; then rebase and port what still
   holds as one attributed revision (D24). Gate 12's patch is `release-gate12.patch` in the taxonomy packet's
   `release/`. [S2-CALLS idx 1175, idx 1208, idx 1268]
3. **Alex questionnaire — rebuilt, not sent.** Final state: `Questions_for_Alex_2026-09-25.docx`, SHA-256
   **`76b9c635…6e84`**, 5,198 words, 12 pages, all 61 excerpts found on their cited pages; the pre-retest build
   (`f201a70e…243a`) is kept in `evidence/a2/pre-retest/`, and the 25 Sep original in `evidence/a2/pre-v1141/`;
   `page-01…12.png` and `page.pdf` re-rendered. 3.3(a) Formality-agreement table recomputed from the reruns:
   **Mac-Gray 13/13, P&W 12/14**. 3.1 now shows Datalink decided (four rounds, round 1 from 28 January) and Kraton
   following the same text. **Not sent to Alex; no direct message to Alex at any point.**
   [DIGEST `2026-09-26T1845_a7e6612a.md`:700-706, :695, :721; ASTRA:55]
   *Open sub-question Austin was asked:* the recompute used the saved `alex_bids.csv` tables in the taxonomy packet
   (made from Alex's `ref/` file on 24 Sep); nothing in `ref/` was read directly. Austin was asked whether even those
   tables are off-limits. [DIGEST same, "Where Alex's labels came from"]
4. **v1.14.2 — Count wording on the `Merger announced` row.** Candidate wording:
   *"Blank on rows about no bidder and on announcement rows (Sale process, Bid, Merger announced), except …"*.
   It is a **proposal only; no publication evidenced.** Also queued for v1.14.2: the four V1141_SPEC §7 known issues and
   report issue 3 (round-1 date), which were not changed. [S2-CALLS idx 1018, idx 1022; ASTRA:30]
5. **Repository export.** `python3 _dev/tools/cockpit/export_repo.py instruction v1.14.1 --write` has not been run;
   the repository file stays v1.13.2 and agents extracting **outside** the app must follow it. [S2-CALLS idx 1175]
6. **Commits and pushes.** None since `679d4fc`. Gate 0 (commit the live uncommitted work on its own, using the
   `pre-existing/` patches) is still first. [S2-CALLS idx 1175, idx 1193]
7. **Migration registers** not regenerated — they need `lesson/`, which the assistant may not open. Austin was asked for
   permission; the conversation ended on that topic. [S2-CALLS idx 1175; DIGEST 20:54:46–20:55:04]
8. **Housekeeping:** install the unit-file `TMPDIR` change (`_dev/tools/cockpit/deploy/PROPOSED-tmpdir.md`); remove
   `dist.old` after acceptance; optional scaffolding in the trial packet not deleted —
   `pro-review/package/` (5.3 MB, byte-identical to the zip beside it), `inputs/raw_filing/` (3.8 MB, copies of three
   filings), `raw-workspace.tar.gz` files (8 MB total), an empty `tmp/`. [S2-CALLS idx 1175; DIGEST "Leftover
   scaffolding"]
9. **Acceptance still owed:** Alex's own run on his plan (phase 2 acceptance); phase 4's remaining acceptance runs (one
   on each new engine). The "draft run and published run on the same filing" item is now satisfiable by Mac-Gray and
   P&W (24 Sep draft pilots + 26 Sep v1.14.1 runs) but **was not checked against the acceptance item**.
   [S2-CALLS idx 1193, idx 1175]

**Left deliberately stale on the VM** (do not "fix" in recovery): `V114_SPEC.md` (hash and line numbers pinned by the
25 Sep staleness review); `ASTRA_APPROVAL_SPEC.md:447` dead memo link (byte-preserved file);
`PROPOSED_DOC_LINES.md:637` and `systemic-audit/D:151` (look broken, are proposed link text relative to `_dev/`);
dated historical reports; `v1.14.1_candidate.diff` (still against the pre-edit text, as the CHANGELOG note says).
[DIGEST `2026-09-26T1845_a7e6612a.md`:711-719]

---

## 6. Per state doc: the VM's final edits, and what each must say now

Evidence coverage warning: `/tmp/recov/evidence/` has per-file JSON for only **five** of the ten docs
(`AGENTS.md`, `README.md`, `SEC_Deal_Ledger_Extraction_Instruction.md`, `_dev/HANDOFF.md`, `_dev/COCKPIT_APP_SPEC.md`,
`_dev/tools/README.md`). For `_dev/CHRONOLOGY.md`, `_dev/RESEARCH_QUESTIONS.md`, `_dev/COCKPIT_BUILD.md`,
`_dev/cockpit/README.md` and root `HANDOFF.md` the only evidence is the **heredoc/`python3 -` bash edits** in
`all_calls_since_0924.jsonl`. Those show the *deltas applied*, never the full final file, so every doc below is
class **Rebuild** in GAP's sense [GAP:70] — the rewrite must be driven by §§1–5 of this sheet, not by patching.

The laptop's copies of all ten are at the 23 Sep baseline (mtime 23 Sep 22:08) [LAPTOP]. **Many of the VM's final edits
have `old_string`s that do not exist in the laptop baseline**, because they replace text added by unseen 24–26 Sep
edits. Do not attempt literal replay.

### 6.1 `AGENTS.md`

VM final edits — the only two tool-level Edits on this file after 21 Sep, both at 26 Sep 20:46
[S2-EV `AGENTS.md.json`]:

- **20:46:00.598** — OLD: *"`_dev/maintenance/2026-09-26-v1141-streamline/`). The change is built and tested but not yet
  live: the running services keep the Astra-high default until Austin orders the WP1 restart. GPT-6-Astra stays
  selectable and keeps high effort as its own default."*
  → NEW: *"`_dev/maintenance/2026-09-26-v1141-streamline/`); it has been live since the v1.14.1 code deploy of
  26 September. GPT-6-Astra stays selectable and keeps high effort as its own default."*
- **20:46:02.756** — OLD: *"…the app never changes this file."*
  → NEW: *"…the app never changes this file. Since 26 September the cockpit's default instruction is v1.14.1, published
  there; it reaches this file only when Austin orders its export, so extractions run outside the app still follow this
  file."*
- **Collision, recorded:** at 20:46:15 the *other* session ran a `python3 -` edit (idx 1147) intending nearly the same
  two changes ("It has been live since the v1.14.1 deploy (26 September, 19:41 UTC)…" / "…this file stays v1.13.2 until
  Austin orders its export."). Its first `assert s.count(a)==1` **raised AssertionError** because the Edit above had
  already landed, so **nothing from idx 1147 was written**. The Edit-tool wording is the final text.
  [S2-CALLS idx 1147 result: `AssertionError`, then `git diff --stat AGENTS.md` = 3 insertions/3 deletions]
- Earlier that evening, at 19:02:22, the same file had been changed from *"GPT-6-Astra at high effort is the default
  extraction model (Austin approved the switch on 26 September after the blinded 15-run v1.14 trial; …)"* to
  *"Opus 5.5 at medium effort is the default extraction model again (Austin, 26 September, reversing that morning's
  GPT-6-Astra-high default; V1141_SPEC §9 …)"* + the "not yet live" sentence later removed above.
  [S2-CALLS idx 691]

**Must say now.** Laptop line 20 currently reads *"Claude Opus 5.5 at medium effort is the default extraction model
(22 September effort sweep, `_dev/reviews/2026-09-22-opus55-sol6-sweep/`)"* [LAPTOP]. The value is right by coincidence;
the provenance is wrong. It must say: Opus 5.5 medium is the default **again**, Austin's 26 September evening decision
reversing that morning's GPT-6-Astra-high default (V1141_SPEC §9), **live since the 26 September v1.14.1 deploy**;
GPT-6-Astra stays selectable and keeps high effort as its own default. Line 12 must gain the cockpit-default sentence
above. Both must be written in the laptop's recovery framing (the VM is the live system; this checkout is a recovery
branch).

### 6.2 `README.md` (root)

No Write/Edit events in the per-file evidence after 23 Sep 09:33 [S2-EV `README.md.json`: 1 Write, 2026-09-23T09:33:07Z].
All 24–26 Sep changes are heredoc edits:

- **19:02:32** [S2-CALLS idx 693] — replaced the "Next step" bullet, adding an "Extraction engine (26 September)" bullet
  (Opus medium restored, "built and tested; goes live when Austin orders the service restart") and retargeting the
  v1.14 upgrade to v1.14.1 ("not published, not the cockpit default and not deployed, and its five-run retest has not
  been run").
- **20:46:15** [S2-CALLS idx 1148] — seven replacements, all applied:
  - heading `## Current state (25 September 2026)` → `## Current state (26 September 2026, evening)`
  - Instruction bullet → *"The repository's working extraction instruction, `SEC_Deal_Ledger_Extraction_Instruction.md`,
    is v1.13.2 and is frozen; extractions run outside the cockpit use it. In the cockpit, v1.14.1 was published and made
    the default on 26 September (SHA-256 `8a93df3c…6c98`); v1.13.2 stays published there. Exporting v1.14.1 to the
    repository file is a later step Austin orders. …"*
  - new paragraph after the sheet list: *"A workbook downloaded from the cockpit's working copy adds a fifth sheet,
    Source, with the filing's EDGAR links and the download's provenance. The cockpit writes it, never the model; the
    four-sheet download, which the checker accepts, leaves it out."*
  - *"records decisions and revision history, and exports Excel"* → *"… (by default with the Source sheet above). Its
    checker and value lists follow each workbook's ledger schema and rules, v1.13.2, v1.14 or v1.14.1; checker 1.8 and
    the v1.14.1 cockpit changes were deployed on 26 September 2026."*
  - engine bullet → *"… it has been live since the deploy that evening. Astra stays selectable."*
  - the "not deployed / retest not run" sentence → *"Its code (checker 1.8 and the cockpit, catalog, migration and
    analysis tools) was deployed on 26 September 2026; the instruction was published in the cockpit and made its default
    the same evening, and its five-run retest (Mac-Gray, Providence & Worcester, sTec, Synacor, Datalink) was run then
    ([results](_dev/reviews/2026-09-26-v1141-retest/README.md); raw, unreviewed). …"*
  - tools line gains "review helpers, analysis tables, reviewed-work migration"; layout table row →
    *"| The repository's working extraction instruction, v1.13.2 (frozen); the cockpit's default is v1.14.1. |"*
- **20:46:20** [idx 1151] — *"The handoff records the case-level decisions to check: Mac-Gray's R01 ruling, which its
  working copy applies, and Datalink's round structure, which Austin settled on 26 September (Datalink follows the
  v1.14.1 text, four rounds, superseding the earlier F9 ruling's five)."*
- **20:46:25** [idx 1154] — "is now aimed at v1.14.1" → "**became** v1.14.1"; and "…the five runs are cockpit versions,
  raw and unreviewed".
- **20:50:46** [idx 1257] — final "Still to come" list: *"exporting v1.14.1 to the repository file, sending Alex the
  questionnaire, committing the work, re-extracting the other deals, moving reviewed work onto v1.14.1 deal by deal once
  that deal's v1.14.1 run has been reviewed, and then updating `extraction/`."*

**Must say now:** all of the above, state-dated **26 September 2026, evening**, plus a recovery note that the laptop
tree is `679d4fc` + a recovery branch and that the cockpit state described lives only on the VM/snapshot.

### 6.3 root `HANDOFF.md` — **does not exist on the laptop**

`ls: cannot access 'HANDOFF.md'` [LAPTOP]. It is a new, untracked VM file, titled
**"# Handoff: Austin's decisions after discussing the v1.14 reviews"**, dated 26 September, opening
*"**Read this first.** This replaces the earlier root handoff in full, at Austin's request. Its old recommendations on
Mac-Gray, Company H and questions for Alex are superseded by the decisions below."* [S2-CALLS idx 1257 result, `sed -n
1,34p HANDOFF.md`]

Known final structure and content [S2-CALLS idx 705 (19:03:47, the section insert), 706, 1164, 1167, 1253, 1261, 1262]:

- `## Update, 26 September 2026 (evening): v1.14.1 and the pipeline upgrade` inserted before `## Purpose and status`,
  with the rubric *"This section is newer than everything below it. Where it conflicts with a later section, it wins."*
- **What was decided:** the v1.14.1 candidate (`8bdb7c20…8a79` **as reviewed**, 6,417 words — later amended to
  *"`v1.14.1_candidate.sha256` now records the edited text's hash; see the status note"*); pipeline decisions Q1–Q4;
  engine Opus 5.5 medium.
- **What R1–R6 superseded** — the six-bullet list reproduced in §4 above.
- **Status note added at 20:46:48:** *"Austin approved eight wording fixes (PIPELINE_UPGRADE_REPORT candidate issues 2
  and 4–10), applied to the candidate file, new SHA-256 `8a93df3c…66c98`; the reviewed text is kept as
  `checks/candidate-8bdb7c20-as-reviewed.md` … both hashes map to the v1.14.1 rules. … published in the cockpit as
  v1.14.1 (id `08caed447f7d`) and made the default at 20:18 UTC. The repository instruction is still v1.13.2."*
  (reworded at 20:50:34 to *"At Austin's order the edited text was published … under his account"*).
- **"Built, deployed, pending" table (status 26 September, 20:45 UTC)**, final rows: Engine revert **live since 19:41**;
  WP2–WP6 **deployed at 19:41** (checker 1.8, hash-keyed rules selector with unknown → v1.14.1, `derive_analysis.py` 0.3
  / contract 0.2, `migrate_review.py` with v1.14.1 impact tags); **Deploy (WP7, includes WP1) done** with the 336/20/77
  tests and the backup path; **Publish and default done at Austin's order, under his account, 20:18**; **Five-run retest
  done**; **GATEs still needing Austin** = export, migration registers, rebases + gate 12, TMPDIR unit files,
  `dist.old`, commits/pushes, questionnaire.
- *"(P1 survives and is being implemented)"* → *"(P1 survives and is implemented in the deployed `derive_analysis.py`
  0.3)"*; hash-map parenthesis → *"(`8bdb7c20…` and, since the wording fixes, `8a93df3c…` v1.14.1; `c2d47a47…` v1.14;"*.
- Questionnaire note → *"The v1.14.1 candidate was `8bdb7c20…8a79` as reviewed, and is `8a93df3c…6c98` after the
  approved wording fixes, the text published as v1.14.1."*
- **Trial worktree** paragraph: `sec-extraction-v114-trial-20260926` removed; packet at
  `_dev/reviews/2026-09-26-v114-15-run-trial/` (296 files, hashes verified); read as evidence, never edit.
- It also carries a `lesson/` reference at line ~127 and the reconciliation note at line ~120
  (*"`lesson/` was not touched"*). [S2-CALLS idx 1275]

**Must say now:** recreate it with this structure, updated so the "pending" column reflects §5, and with `lesson/`
references removed or explicitly marked dropped (the recovery rule is that `lesson/` is dropped and never recreated
[TEAM_BRIEF:38] — this **contradicts** the VM's own final position that `lesson/` is retained and needed for the
migration registers [S2-CALLS idx 1175; DIGEST 20:55:04]; flag, do not silently resolve).

### 6.4 `_dev/HANDOFF.md`

Best-evidenced doc: a **full Read of the whole file at 26 Sep 18:46:04** (100 lines) [S2-EV `_dev/HANDOFF.md.json`,
last event], then a dense sequence of heredoc edits at 19:04 and 20:47–20:51. The 18:46 snapshot is the pre-deploy
baseline; every later edit is known. Final state:

- **Section header replaced** (20:47:38, idx 1175): the 19:04 update section became
  `## Update, 26 September 2026 (evening, 20:45 UTC): v1.14.1 deployed, published and retested`, whose body is the
  "Now / Still GATEs for Austin / Trial packet" block quoted in §5 and §2.1 above.
- 20:47:45 (idx 1177): Q1–Q4 bullet softened to *"…stand; Q1's rules selector and Q2's process-Question exemption from
  the cap of five are in the deployed checker."*
- 20:47:54 (idx 1184): **Current direction** line rewritten from *"GPT-6-Astra at high effort is the extraction
  default…"* to *"**Opus 5.5 at medium effort is the extraction default** (Austin, 26 September evening, reversing that
  morning's GPT-6-Astra-high default; live since the 19:41 UTC deploy)."*, and *"This default change does not publish
  v1.14…"* → *"Neither default change authorized another extraction. Opus 5.5 medium is the provenance of the existing
  raw workbooks and of the five v1.14.1 retest runs."*
- 20:48:15 (idx 1193): heading → `## Build snapshot (25 September, brought up to date on 26 September, 20:45 UTC; the
  update above takes precedence)`; *"Uncommitted work is live"* bullet → *"**The v1.14.1 code is live, uncommitted.**
  Since 26 September, 19:41 UTC…"*; **Instructions-in-the-cockpit bullet** → lists v1.14.1 (`08caed447f7d`,
  `8a93df3c…6c98`) published 20:18 and default, v1.13.2 published, draft `a4ca26ecfa92` unpublished, draft
  `73f21eb8c09a` unused; services bullet → restarted **19:41 and 19:45**, worker again during the retest, unit files
  unchanged; **Tests bullet** → *"336 pass / 20 pass / 77 pass … Before the deploy the live tree had 199, 14 and 53"*;
  "Waiting on Austin" rewritten to the §5 gate list.
- 20:48:31 (idx 1203): the run-version table gains the **five v1.14.1 retest rows** exactly as in §3.2; the "two pilots
  are superseded drafts" line gains *"The five v1.14.1 retest runs are raw and unreviewed …; no working copy has been
  rebased onto them."*; the Datalink review-boundary cell gains *"**Austin superseded it on 26 September**: Datalink
  follows the v1.14.1 text, four rounds"*; the layout table row for the instruction file gains *"(the cockpit's default
  is v1.14.1, not yet exported here)"*; the Engineering paragraph gains the S1/S2/S3/S4/MIG-C feature list and
  *"checker 1.8 …, deployed on 26 September 2026"*.
- 20:48:39 (idx 1208): "Next work" item 0 gains the 20:45 status note; item 1 retargeted to **v1.14.1**; the F9 sentence
  replaced by *"Austin decided on 26 September that Datalink follows the v1.14.1 text (four rounds), superseding the
  January-round ruling (F9); the same reasoning applies to Kraton and Meredith."*; *"the seven runs made there so far"*
  → *"the twelve runs made there so far (seven by 24 September and the five v1.14.1 retest runs of 26 September)"*.
- 20:48:45 (idx 1211): opening paragraph → *"These decisions were approved and are now written into v1.14.1 (published
  and the cockpit default since 26 September); no working copy implements them yet."*
- 20:50:34/38 (idx 1253, 1254): attribution changed to "at Austin's order / under his account"; and
  *"The per-user run cap was raised to 3 for this batch and is restored to 2 (the code is as deployed)."*
- 20:51:13 (idx 1264): backup/rollback detail folded into the update section; "started by Austin" → "started under
  Austin's account" throughout.

**Must say now:** the 18:46 snapshot **as amended by all of the above**, i.e. the v1.14.1-deployed-published-retested
state, twelve cockpit runs, five v1.14.1 versions, all working copies still on v1.13.2, the §5 gate list — plus the
recovery preface (VM unreachable, this checkout is `679d4fc` + recovery branch, cockpit facts come from the 27 Sep
snapshot).

### 6.5 `_dev/CHRONOLOGY.md`

No per-file evidence JSON. Two heredoc edits:

- **19:04:34** (idx 709) — five new rows appended before the *"The cleanup was committed with v1.10 and v1.11"* anchor:
  the blinded fifteen-run comparison; `| 26 Sep, 12:02 UTC | GPT-6-Astra at high effort made the extraction default …`;
  Austin's four settled treatments H1–H4; `| 26 Sep | V1141_SPEC: rulings R1–R6 and decisions D1–D6; the v1.14.1
  candidate instruction (6,417 words, SHA-256 8bdb7c20…8a79); engine back to Opus 5.5 medium |`; and the
  PIPELINE_UPGRADE_SPEC / Q1–Q4 row. (19:04:40, idx 710, was a one-newline fixup.)
- **20:49:08** (idx 1225) — deleted a stray blank line at index 56 and inserted **three more rows** after the
  PIPELINE_UPGRADE_SPEC row:
  - `| 26 Sep, 19:41 UTC | v1.14 code, updated for v1.14.1, deployed at Austin's order (V114_SPEC §12;
    PIPELINE_UPGRADE_SPEC WP7 …): checker 1.8 with the v1.14 / v1.14.1 rules selector keyed on the instruction's SHA-256
    (unknown → v1.14.1), cockpit schema awareness and a safe rebase, the Source sheet in downloads, the bulk
    Process/Round edit, the catalog lookup, derive_analysis.py 0.3 (contract 0.2), migrate_review.py with the v1.14.1
    impact tags, the runner and sweep updates, and the Opus 5.5 medium extraction default; … | Tests 336 unit, 20 HTTP,
    77 vitest … dist.old kept for rollback |`
  - `| 26 Sep, 20:18 UTC | After approving eight wording fixes …, Austin publishes it in the cockpit as v1.14.1
    (id 08caed447f7d, SHA-256 8a93df3c…6c98) and makes it the cockpit default | The reviewed text 8bdb7c20…8a79 is kept
    in the packet's checks/; both hashes map to v1.14.1. v1.13.2 stays published, no longer the default. The repository
    instruction stays v1.13.2 (not exported) |` (wording adjusted at 20:49:13, idx 1227; attribution at 20:50:34 to
    *"it is published in the cockpit at his order, under his account"*)
  - `| 26 Sep, 20:19 UTC | Five-run v1.14.1 retest, started in the cockpit at Austin's order under his account
    (Opus 5.5 medium; per-user cap raised to 3 for the batch, then restored to 2): Mac-Gray, Providence & Worcester,
    sTec, Synacor, Datalink | All completed; all V1141_SPEC §10 step-6 behaviours hold; no Note over 40 words; fewer
    rows than the trial. Austin then decided that Datalink follows the v1.14.1 text, four rounds, superseding F9's five
    (same reasoning for Kraton and Meredith), closing candidate issue 1 |`

**Must say now:** these eight rows, in order, appended to the laptop's table (which currently ends at 23 Sep — the
25 Sep V114_SPEC row is itself not on the laptop and must be added too, per the 19:04 evidence showing it already
present on the VM as `| 25 Sep | V114_SPEC: Austin's decisions D1–D27 make v1.14 a system-wide upgrade …`).

### 6.6 `_dev/RESEARCH_QUESTIONS.md`

No per-file evidence JSON. Two heredoc edits:

- **19:02:00** (idx 689) — eight replacements, all applied: a new *"**Update, 26 September 2026: v1.14.1.**"* paragraph
  after the "supersedes the old '16 questions'" line; Q7 Company H gains *"**Settled 26 September (H1):** Company H is
  Dropped by target when the final-round letters went to WDC and Company D (by 16 May), with reason Would not improve
  earlier offer; v1.14.1 states it generally (E14 inferred exit 1, R5)."*; E10 item gains H4; the Datalink/F9 item gains
  the D6 trigger-(d) and four-round reading; E5's 90-day test; D1 (the refers-back route is gone); R1 Same offer making
  WDC's 10 June bid Informal "as Alex coded it"; the October 13 valuation-statement reading; E9's five deadline
  outcomes.
- **20:48:53** (idx 1216) — five replacements: *"The working instruction is v1.13.2"* → *"The **repository's** working
  instruction is v1.13.2"*; *"The v1.14 candidate that adopts them is in preparation…"* → *"The v1.14 candidate that
  first adopted them was never published; v1.14.1 (below) carries them."*; the "not published/not default/not deployed"
  status sentence → *"Status, 26 September, 20:45 UTC: after eight approved wording fixes (SHA-256 now `8a93df3c…6c98`),
  v1.14.1 was published in the cockpit and made its default; checker 1.8 … was deployed the same day; and the five-run
  retest was run … The repository instruction stays v1.13.2 until Austin orders the export. The provisional answers have
  not yet been sent to Alex."*; the Datalink item gains **"Decided 26 September (Austin): Datalink follows the v1.14.1
  text, four rounds; F9 is superseded for Datalink, and the same reasoning applies to Kraton and Meredith. The v1.14.1
  retest run of Datalink has four rounds. The questionnaire's 3.1 … predates this decision."**; heading
  *"- **Datalink F9 is resolved:**"* → *"- **Datalink F9 was resolved, then superseded:**"*.

**Must say now:** exactly that, and it must keep the 22 September correction that Q3 and Q7 are no longer withheld.

### 6.7 `_dev/COCKPIT_APP_SPEC.md`

Per-file evidence has **one Write, 23 Sep 11:52:01**, and nothing later [S2-EV `_dev/COCKPIT_APP_SPEC.md.json`] — so the
laptop baseline equals the VM text up to 23 Sep. One heredoc edit afterwards:

- **20:49:20** (idx 1230), four replacements, all applied:
  - `(default: GPT-6-Astra, high, current default instruction; Austin's 26 September update);` →
    `(default: Claude Opus 5.5, medium, current default instruction; Austin's 26 September evening decision, reversing
    that morning's GPT-6-Astra-high default);`
  - `| Engines | GPT-6-Astra (default, high; Austin's 26 September update), Claude Opus 5.5, Claude Fable 5.1 and
    GPT-6-Sol, at every effort the runner allows.` → `| Engines | Claude Opus 5.5 (default, medium; restored
    26 September evening), Claude Fable 5.1, GPT-6-Sol and GPT-6-Astra (high by default when chosen), at every effort
    the runner allows.`
  - `- **Engine**: GPT-6-Astra (default, high), Claude Opus 5.5, …` → `- **Engine**: Claude Opus 5.5 (default),
    Claude Fable 5.1 (marked *experimental*), GPT-6-Sol, GPT-6-Astra.`
  - example summary line `"GPT-6-Astra · high · v1.13.2 · on Alex's ChatGPT plan."` →
    `"Opus 5.5 · medium · v1.14.1 · on Alex's Claude plan · usually 10–15 minutes."`
  - **Note:** the three `old_string`s naming "Austin's 26 September update" are **not in the laptop's 23 Sep baseline**;
    an unseen 26 Sep morning edit introduced them. The laptop already reads
    `(default: Claude Opus 5.5, medium, current default instruction)` (line 10),
    `| Engines | Claude Opus 5.5 (default, medium), Claude Fable 5.1, GPT-6-Sol and GPT-6-Astra, …` (line 23),
    `- **Engine**: Claude Opus 5.5 (default), …` (line 88) and the example
    `"Opus 5.5 · medium · v1.13.2 · on Alex's Claude plan · about 10–15 minutes."` (line 92) [LAPTOP]. So the only real
    deltas to apply are the 26 September attribution parenthetical, "restored 26 September evening" / "GPT-6-Astra
    (high by default when chosen)", and `v1.13.2` → `v1.14.1` plus "usually 10–15 minutes" in the example line.
    Rewrite from the new text, do not replay.

**Must say now:** §13 defaults = Claude Opus 5.5 · medium · the current default published instruction (v1.14.1);
Astra selectable, high by default when chosen.

### 6.8 `_dev/COCKPIT_BUILD.md`

No per-file evidence JSON. One heredoc edit, **20:49:35** (idx 1232), six replacements, all applied — these are the
`PROPOSED_DOC_LINES.md` Part-1 entries D1–D4 plus two:

- **D1** `choices` becomes schema-and-rules dependent: *"mapping field names to allowed labels from the checker for the
  displayed version's `ledger_schema` (`check_lean.choice_lists`; a working copy has its base's schema, and one deal can
  hold versions of both) … A 29-column workbook's lists follow its rules, v1.14.1 by default or v1.14 for a run of the
  v1.14 instruction, chosen from the instruction's SHA-256. The payload's `ledger_schema` says which applies; an
  unreadable header gives no choices."*
- **D2** new op `{type:'bulk_update',sheet:'Deal ledger',uids,values}` — sets Process and/or Round on many rows, counts
  as **one** of a save's 100 operations, `uids` must be distinct live rows or `new-*` client UIDs, Process ≥ 1,
  Round ≥ 0 or `post`; each row recorded, diffed, attributed; row review marks kept; staged from the editor's **Select**
  mode behind a confirmation.
- **D3** new op `{type:'rebase',target_version}` — makes another version the base as one new revision; row marks and row
  threads stay with the old rows; finding judgments carry over with a `carried_over` record and their implementation and
  verification reset; `GET /api/deal/<slug>/rebase?to=<id>` previews the counts that stop applying and both ledger
  schemas.
- **D4** export contract: `GET /api/deal/<slug>/export?version=working` → `<slug>-working-r<N>.xlsx`, four sheets **plus
  a fifth sheet, Source** (EDGAR filing-index and complete-submission links; Background pages; filing, instruction and
  raw-workbook hashes; base version; revision; deal review status; export time), written by the cockpit and never by the
  model; `&source=0` returns the four sheets alone; `Workspace.export` (used by `export_repo.py` and
  `verify_catalog.py`) stays four-sheet; `?version=rev:N` downloads a past revision the same way.
- *"Since 22 September the cockpit shows only the nine Opus 5.5 medium extractions, one version per deal;"* →
  *"Since 22 September the **catalog holds** only the nine Opus 5.5 medium extractions, one version per deal, **beside
  run versions started in the cockpit**;"*
- Checked in the same run (idx 1144, 20:46:01): D1's replacement text was already present; **D2, D3, D4 were reported
  "replacement present: False"** immediately before idx 1232 applied them — i.e. idx 1232 is the edit that landed them.

### 6.9 `_dev/cockpit/README.md`

No per-file evidence JSON. Two heredoc edits:

- **19:03:10** (idx 702) — engine list: *"Choose the engine (Claude Opus 5.5 by default when your Claude account is
  connected, otherwise the first connected engine; GPT-6-Astra; Claude Fable 5.1, marked experimental …; GPT-6-Sol), the
  effort (Astra defaults to high; the other cockpit engines default to medium)"* plus a sentence about the change being
  built but not live.
- **20:49:56** (idx 1241) — eight replacements, all applied:
  - versions paragraph gains *"such as the five v1.14.1 retest runs of 26 September (Mac-Gray, Providence & Worcester,
    sTec, Synacor and Datalink; raw and unreviewed)"*
  - Datalink line gains *"Austin superseded it on 26 September: Datalink follows the v1.14.1 text, which gives four
    rounds."*
  - **Select / Set Process/Round…** bulk-edit instructions added after "Clone to split"
  - Review tab: *"Its checker line names the checker version and the rules (v1.13.2, v1.14 or v1.14.1) of the live check
    and, for an original version, what the checker found when the version was imported; the value lists in the editor
    follow the same rules."*
  - step 4 rewritten for the **Source sheet** download (`<deal>-working-r<N>.xlsx`), the "Four sheets only (checker
    format)" menu item, "With Source sheet" for original versions, and per-revision **Download**
  - the "built but not live" sentence → *"…and has been live since that evening's deploy."*
  - **Use as working-copy base…** gains the rebase preview description and *"restore the pre-rebase revision, not
    revision 0, to undo a rebase."*
  - instructions paragraph gains *"v1.14.1 was published on 26 September, under Austin's account at his order, and made
    the default; the repository file stays v1.13.2 until Austin orders its export."*

### 6.10 `_dev/tools/README.md`

Per-file evidence has **one Edit on 24 Sep 22:02:49** [S2-EV `_dev/tools/README.md.json`]:
OLD *"…Required long Notes and documented uncertain Counts are review warnings."* → NEW adds
*"The ledger header selects the rules: a `Stock %` column marks a v1.14 (draft) workbook, whose bid-term columns get
their value lists and the E12 consistency rules (Financing Contingent requires Heavy; None requires Complete diligence
and committed or unneeded financing); any other header is checked as v1.13.2, unchanged. The report's `ledger_schema`
says which applied."* — this is the **checker 1.6** documentation.

Then heredoc edits:
- **19:02:57** (idx 699) — inserted the `**Checker 1.8 (built, not deployed).**` paragraph (full text quoted in §2.2);
  engine default → Opus 5.5 medium; `--provider sol` note; `export_repo.py instruction v1.14` examples → `v1.14.1`.
- **19:03:04** (idx 701) — export_repo caveat: *"The v1.14.1 example below is for its release only: v1.14.1 is not yet
  published in the cockpit, and `--write` replaces the frozen v1.13.2 instruction (a GATE)."*
- **19:23:27** (idx 902, applied, printed `ok`) — the checker-rule sentence rewritten to the error/warning split quoted
  in §2.2.
- **19:20:34** (idx 880) and **19:23:49** (idx 906) edited the **v114-tree** copy of the same file; at 20:45:38 (idx
  1130) a `diff` of main vs v114 `_dev/tools/README.md` was run to reconcile them.
- **20:50:09** (idx 1246) — seven final replacements, all applied:
  - *"This is checker 1.8, not deployed; the live services run checker 1.6 until the deploy."* →
    **"This is checker 1.8, deployed on 26 September 2026."**
  - hash map → *"(`8a93df3c…`, the published v1.14.1, and `8bdb7c20…`, its reviewed text before the 26 September
    wording fixes, v1.14.1; `c2d47a47…` v1.14; and the 24 September draft `f9595d74…` v1.14)"*
  - export_repo caveat → *"v1.14.1 is published in the cockpit and its default (26 September), but `--write` replaces
    the frozen v1.13.2 repository instruction, which waits for Austin's order (a GATE)."*
  - `derive_analysis.py` usage gains `[--rules v1.14|v1.14.1]`; the tool line → **"`derive_analysis.py` (0.3) … under the
    analysis contract (version 0.2 …)"**; *"v1.13.2 ledgers are accepted with the columns they have"* gains *"; a
    29-column ledger is read under the v1.14.1 rules unless `--rules v1.14` says it was made under the v1.14
    instruction."*
  - `migrate_review.py triage` usage gains `[--rules v1.14]`; the tool line → the D24 sentence quoted in §2.4.

**Must say now:** checker **1.8 deployed 26 September**, the four-entry hash map, Opus 5.5 medium default, the
`derive_analysis.py` 0.3 / contract 0.2 and `migrate_review.py` lines, and the export GATE — **plus** `compare_alex.py`,
which the laptop's README does not mention at all and whose content is lost (mark it explicitly as a tool that exists on
the VM and must be rebuilt).

---

## 7. Contradictions and uncertainties — flagged, not resolved

1. **Root instruction file: v1.13.2 (VM, 26 Sep) vs v1.14.1 (laptop, now).** Every VM source says the export was never
   run and the repository file was still v1.13.2 [S2-CALLS idx 1175, 1263; ASTRA:34; GAP:25]. The laptop file now hashes
   to `8a93df3c…66c98` with mtime 27 Sep 12:17 [LAPTOP]. Recovery-session action, not recovered history.
2. **Who published.** Cockpit attribution is `austin` [S1]; the original session first said Austin acted himself, then
   corrected at 20:52 that a **forked Claude session used his browser account** [DIGEST 20:52:46; ASTRA:97]. Database
   attribution does not establish manual human action.
3. **`lesson/`: dropped vs required.** TEAM_BRIEF:38 and GAP:71 say `lesson/` is dropped and must never be recreated
   (Austin: "stale, not wanted"). The VM's own final state lists **regenerating the migration registers from `lesson/`**
   as an outstanding gate, and Austin's last message asked whether `lesson/` is stale without resolving it
   [S2-CALLS idx 1175; DIGEST 20:54:46–20:55:04]. The registers therefore have no evidenced path forward.
4. **"The rerun passed" is too broad.** Two checker errors remained (sTec row 56, Datalink row 76) plus length/marker
   warnings; the P&W acceptance failures were declared script false alarms after inspection. This supports a bounded
   behavioural check, not extraction accuracy. [ASTRA:99; S2-CALLS idx 1018]
5. **sTec Count: model error or wording gap.** One session called the sTec Count entry a model mistake; the fork called
   the same behaviour defensible under ambiguous wording. Both then proposed the general v1.14.2 clarification. The
   mechanical failure is verified; responsibility is interpretive. [ASTRA:100]
6. **Model ranking is unstable.** The reported leader moved Opus → Astra → Opus as reviews and Austin's rulings changed;
   one run per setting/deal does not establish a ranking. The early "no material factual errors" headline sits uneasily
   with later acknowledged unsupported claims. [ASTRA:101]
7. **Alex's approval of the taxonomy is second-hand**, inferred by Claude from Austin's ambiguous "confided … sitting
   right next to him". No questionnaire has ever been sent to Alex directly. [ASTRA:12, :103]
8. **Kraton is an extrapolation, not a decision.** Austin decided Datalink; the assistant applied "the same reasoning"
   to Kraton (two rounds) in the questionnaire and asked for confirmation. Meredith is named in the same breath but was
   not changed in the questionnaire. [DIGEST :721, :751; S2-CALLS idx 1208]
9. **Two sessions collided on the same docs at 20:43–20:52.** The fork's staleness agent and the original session both
   edited `AGENTS.md`, `README.md`, `HANDOFF.md`, `_dev/HANDOFF.md`, CHRONOLOGY, RESEARCH_QUESTIONS, the cockpit/tools
   READMEs and the v1141 packet; the retest README and `deployment-v1141.json` were each overwritten once.
   [S2-CALLS idx 1187, idx 1212; ASTRA:102] One concrete casualty is recorded in §6.1 (idx 1147 AssertionError). The
   final VM files were never independently re-read whole, so §6 is deltas, not a verified final text.
10. **Questionnaire hash moved twice on 26 Sep.** `f201a70e…243a` (pre-retest rebuild, recorded in the 19:03 root-handoff
    edit) → `76b9c635…6e84` (final post-retest rebuild, 5,198 words, 12 pages). Earlier documents still cite the older
    hash. [S2-CALLS idx 705; DIGEST :700-706]
11. **Datalink round-1 date.** F9 said 29 January; the v1.14.1 text and the retest give **28 January**; the questionnaire
    was changed to 28 January by the assistant on that basis. [S2-CALLS idx 1018; DIGEST :752]
12. **GAP:41 vs the evidence on `check_lean.py` provenance.** GAP calls it "Near" — a v114-tree full Read at 18:32 then a
    merge into main plus the `8a93df3c` `RULES_BY_INSTRUCTION` edit. The merge itself is attested only by the fork's
    SendMessage ("added to RULES_BY_INSTRUCTION in both trees", idx 1187), not by a captured diff. Treat the merged main
    copy as unverified.
13. **No evidence file exists for five of the ten state docs** (§6 preamble). Their VM final text is known only as
    deltas over a baseline that itself is not on the laptop.
14. **Backup gap.** The only verified backup (`20260926-193859Z`) predates the publication and the five reruns; no later
    backup is evidenced, and the backup implementation covers the database and stored-file tree only — not the dirty
    repository, maintenance packets or credentials. [ASTRA:75, :77]
