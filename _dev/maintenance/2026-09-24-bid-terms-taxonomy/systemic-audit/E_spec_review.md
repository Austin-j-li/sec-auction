# E. Review of V114_SPEC.md (system upgrade spec)

25 September 2026. This is a read-only review, written from the point of view of the team that has to build from the spec.

**Inputs read:**
- `V114_SPEC.md`, compared line by line with `/home/uctpiaj/work/tmp/V114_SPEC_before_systemic_2026-09-25.md`;
- audits A–D;
- the 24 September draft;
- `TAXONOMY_DRAFT5.md`;
- `ASTRA_APPROVAL_SPEC.md`;
- the cited code and documents.

**What I ran:**
- `grep`, `sed`, `sha256sum` and `git diff` (read-only);
- `openpyxl` in read-only mode on the two pilot workbooks and on `extraction/providence-worcester.xlsx`;
- SQLite only through `file:…?mode=ro`.

**What I did not do:** no HTTP requests, restarts, model runs, or edits other than this file.

**One observation about the database.** Immediately after one of my `mode=ro` reads (19:47 UTC), `workspace.sqlite3-wal` and `-shm` existed in `_dev/cockpit/state/`. They were gone by 19:48. `workspace.sqlite3` itself kept its mtime of 24 September, 22:53. Finding 17 uses this.

**Severity:**
- **Blocker:** following the spec as written damages the live service, produces inconsistent research data, or sets an acceptance check that a correct implementation cannot pass.
- **Should fix:** the team would have to guess, would breach a scope rule, or would be misled by a wrong fact.
- **Minor:** wording, citations or small omissions.

**Where the requested focus areas land:**

| Focus area | Findings |
|---|---|
| D15 and exclusivity | 2, 11 |
| D18 and Other-scope rows | 12 |
| D7 scope | 11, 12, 13 |
| Deadline outcome sets | 13, 26 |
| Header | 25 |
| Gate order | 1, 5, 6, 30 |
| Live checkout vs working copy | 5, 6, 8 |
| Scope and safety leaks | 5, 6, 7, 9, 13, 17, 19, 20 |

---

## Blockers

### 1. Relocating the nine workbooks (D25, gate 12) makes the nine catalog deals vanish from the live cockpit, and gate 12.4 then fails

**Location:**
- §1 D25: "Repoint their catalog paths, keeping the id, hash and instruction version, so the working copies still resolve".
- §7.7: "tests show that after relocation the working copies still resolve (same id and hash)".
- §13 gate 12: step 1 `git mv`; step 4 "run the tests and the fixed `verify_catalog.py`"; step 5 "export the v1.14 runs".

**Problem.** Repointing the catalog is not enough. The cockpit lists and resolves a catalog deal only if `extraction/<slug>.xlsx` exists. As a result:
- Between steps 12.1 and 12.5, all nine deals, including the eight reviewed working copies, return 404 in the running services.
- Step 12.4's `verify_catalog.verify()` raises.
- Any deal left without an exported file stays invisible.

**Evidence:**
- `data.py:686-694`: `slugs()` globs `extraction/*.xlsx`.
- `data.py:709`: `resolve()` raises `DealNotFound` when `extraction/<slug>.xlsx` is missing.
- `workspace.py:319`: `Workspace.deal` calls `cockpit.resolve`.
- `verify_catalog.py:80`: `payload = cockpit.deal(slug)`.
- Audit B10 stated this dependency ("lists and resolves a catalog deal only if `extraction/<slug>.xlsx` exists"). The spec kept only the hash half of it.

**Fix.** Add to §7.7 (S5):

> "Change `Cockpit.slugs()` and `Cockpit.resolve()` so that a catalog deal is listed and resolved from `catalog.json` and `raw_filing/MANIFEST.csv`, with its workbook taken from the catalog base's `path`, not from the presence of `extraction/<slug>.xlsx`. This part is deployed at gate 3: it changes nothing while the files are in place. Test: in a temporary root with `extraction/<slug>.xlsx` removed, the deal lists, its working copy renders and exports, and `verify_catalog` passes."

In gate 12:
- stop both services for steps 1–5;
- run step 4 after step 5.

In D25, add after "still resolve": "(with S5's resolution change deployed)".

### 2. D13/E10 and D15 prescribe different rows for a later exclusivity requirement

**Location:**
- §1 D13: "Same-price changes to bidder commitments (… financing or closing conditions) are Bid rows".
- §3 E10: "Every communicated material revision of … bidder commitment is a Bid row, including same-price changes to conditions".
- §1 D15: "A later exclusivity request gets its own row. It is an Exclusivity changed row … If it comes with a material revision of the offer, it is one Bid row".
- §3 E10 and §4: "whether the bid is a first bid or a revision".

**Problem.** The draft codes Exclusivity = Required when "the bid … is conditioned on exclusivity" (line 230), and line 224 counts Exclusivity among "the five condition columns". So a later, same-price "we will not proceed without exclusivity" is two things at once:
- a same-price change to conditions, which E10/D13 make a Bid row;
- a later request, which D15 makes an Exclusivity changed row.

Package P reads Bid rows as price observations (D22), so the two readings give different data. Further gaps:
- **D15 disagrees with §3, §4 and §8.** D15 says "material revision"; §3, §4 and §8 say "a first bid or a revision".
- **Bid reaffirmed or a non-material message.** No rule covers a request made with a Bid reaffirmed row or with a non-material message.
- **The next revision.** Nothing says how the next revision codes Exclusivity after a separate request.
- **Terminology.** Part A calls exclusivity "a term". Audit C §2 item 26 flagged the "condition columns" wording at line 224. The spec does not disposition it.

**Evidence:**
- draft lines 224 and 230;
- §2, Part A item 3;
- ASTRA_APPROVAL_SPEC.md §4.2: "If it materially revises the offer, use Bid … otherwise use Exclusivity changed". There, the request itself can be the material revision.

**Fix.** In §3 E10 and §4 (Exclusivity), add:

> "For E10, exclusivity is a term, not a condition. A request for, or requirement of, exclusivity made after the bid, with no change of price, consideration or other commitment, is an Exclusivity changed row, never a same-price Bid row. A request made in the same communication as a Bid or Bid reaffirmed row is coded on that row. A later bid row codes Exclusivity from its own communication; an earlier standing request carries over only by express incorporation."

Also:
- In D15, change "If it comes with a material revision of the offer" to "If it is made in the same communication as a bid".
- Change line 224's "the five condition columns" to "the five columns after Conditions".
- Align S1 change 6(a) with this (finding 11).

### 3. The row-mark totals are wrong in three places, so MIG acceptance cannot pass

**Location:**
- §7.9: "434 row marks "reviewed" and 66 "needs decision"".
- §9.6: "their row-mark totals match the database (434 reviewed, 66 needs decision on 25 September)".
- §11: "434 reviewed, 66 needs decision".

**Evidence.** A `mode=ro` read of `row_review` in the latest `revisions.snapshot` per deal gives the counts below. Every Deal ledger row is marked (75 + 58 + 88 + 51 + 47 + 63 + 61 + 77 = 520). Audit B §4 carried the same error ("434", and "The 500 row marks").

| Deal | Reviewed | Needs decision |
|---|---|---|
| Kraton | 57 | 18 |
| Mac-Gray | 56 | 2 |
| Meredith | 61 | 27 |
| Penford | 47 | 4 |
| PetSmart | 42 | 5 |
| P&W | 60 | 3 |
| sTec | 58 | 3 |
| Synacor | 73 | 4 |
| **Total** | **454** | **66** |

**A second problem.** §7.9 defines the register as "one item per estimation-relevant fact". That has no one-to-one relation to rows, so "row-mark totals" of a register is undefined.

**Fix:**
- Replace 434 with 454 in all three places.
- In §9.6, write: "Each register also lists every Deal ledger row of the latest snapshot with its row mark; per deal, the marks equal the database's (454 reviewed and 66 needs decision on 25 September; re-read at test time)."

### 4. The documented pilot delta omits warning 6(a), so S1's reproduction, §9.2 and the §12 smoke test cannot all pass

**Location:**
- §7.3 change 6, adopted by §8 ("The four in S1 change 6 are adopted").
- §7.3 Reproduction: "Mac-Gray gains 2 legacy warnings and loses 2 `exit.inferred_reason` warnings; P&W gains 2 legacy warnings".
- §9.2: "The four optional warnings fire … nowhere in the stored results except as S1 documents".
- §12 step 10: "the pilots differ only as S1 documents".

**Evidence:**
- Audit A12(a) found "2 hits, both in the Mac-Gray pilot (#31/#32 and #39/#40) … (a) adds 2 warnings to Mac-Gray".
- Confirmed in `…/mac-gray/opus55-medium-20260924-2241-d7d267/mac-gray.xlsx`: #31 is a Bid with Exclusivity Requested, and #32 is an Exclusivity changed row with the same Who (CSC/Pamplona) and Sort date. #39/#40 are the same.
- Neither pilot has an Other-scope row. A12 found 0 hits for the other two checks.

**Fix.** In §7.3 Reproduction, write:

> "Mac-Gray gains 2 `rounds.deadline_outcome_legacy` and 2 D15-duplicate warnings and loses 2 `exit.inferred_reason` warnings; P&W gains 2 legacy warnings. The other three optional warnings add none."

---

## Should fix

### 5. The deploy patch is the whole `_dev/tools` diff: it ships release-time code and text at gate 3, and it cannot carry the doc lines outside `_dev/tools` or binary files

**Location:**
- §12, before the window, step 4: "`diff -ruN <baseline> <worktree>/_dev/tools`".
- D25: "Update `import_results.py` and `verify_catalog.py` in the same commit" (as the move).
- Gate 12.3: "apply S5's `import_results.py` and `verify_catalog.py` changes".
- §7.3 change 8: "describing code that is not deployed as not deployed".
- §7.12 Deploy: "drafted in the separate working copy …; applied with the deploy: … `_dev/COCKPIT_BUILD.md` (47, 69); the root README (5, 16); HANDOFF (64); the cockpit README (20)".

**Problem:**
- **(a) Relocated paths ship early.** S5's relocated paths would go live, and into the next commit, nine gates before the move they must accompany.
- **(b) Stale "not deployed" text.** `_dev/tools/README.md:19` would go live still saying "not deployed".
- **(c) Release lines ship early.** Release-class lines drafted in the worktree (tools README 49 and 120) would go live at deploy.
- **(d) Some doc lines are never applied.** §12 has no step that applies the Deploy-class lines outside `_dev/tools`.
- **(e) Binary files are lost.** `diff -ruN` writes "Binary files … differ" for any binary fixture, so the patch cannot apply it.

**Fix.** Replace §12 step 4 with:

> "Make two patches with `git diff --no-index --binary` from the baseline to the worktree's `_dev/tools`. (1) The deploy patch excludes S5's path constants in `import_results.py` and `verify_catalog.py` and the Release-class lines. (2) The release patch holds only those, and is applied at gate 12.3. Before making (1), change `_dev/tools/README.md:19` to 'deployed <date>'."

Also:
- Deliver the Deploy- and Release-class lines for files outside `_dev/tools` as proposed text in the report.
- Add §12 step 9a: "Apply the Deploy-class doc lines listed in S6."

### 6. Commits: gate 0 cannot separate the earlier session's doc changes from the team's wave-1 edits, and no gate commits the deployed v1.14 code

**Location:**
- §13 gate 0: "Commit the live uncommitted work separately (… `dist/` and the docs), so the v1.14 diff stands alone".
- §7.13 Wave 1: "S6's 'now' lines".
- §0, which allows the team to write `_dev/cockpit/README.md` now.

**Problem:**
- **The README is already mixed.** `git diff HEAD -- _dev/cockpit/README.md` shows the deal-review session's uncommitted hunk at `@@ -10,0 +11,2 @@`. That sits between the "now" lines 9 and 13 that the team will edit.
- **Hunk staging is unavailable.** Interactive staging (`git add -p`) is not available in this environment. After wave 1, gate 0 cannot commit the earlier session's doc changes on their own.
- **The v1.14 code is never committed.** After gate 3, the live tree carries uncommitted v1.14 code, and no gate (9, 12 or 13) commits it.

**Fix.** In §0, add:

> "Before editing a file that `git status` shows as modified, save `git diff HEAD -- <file>` as `pre-existing/<file>.patch` in this folder; at gate 0 stage it with `git apply --cached`."

Add a gate 3a: "At a commit Austin requests, commit the deployed code by explicit paths, separately from the instruction export."

### 7. §12 has the team contact Alex

**Location:** §12 window step 1: "Ask Alex and Austin to save their work and close their cockpit tabs"; step 11: "Tell both users to reload any open tab".

**Problem.** §0 forbids "sending anything to Alex", and "the team" carries out §12.

**Fix:**
- Step 1: "Austin confirms that he and Alex have saved their work and closed their tabs. The team does not contact Alex."
- Step 11: "Austin tells Alex to reload."

### 8. §0's read authorizations do not cover the inputs other packages need

**Location:** §0: "read-only access to the cockpit state for packages M, MIG and P …; reading … `ref/seed.csv` for package P, and `lesson/` for package MIG".

**Problem:**
- **M** must read the 24 September reverts in `lesson/independent-audit-2026-09-23/` (§6, "Recorded rulings").
- **A2** must read the original DOCX in `lesson/…/questions-for-alex/` (§5: "Keep Q1's options", "Part 2", "Decision 1").
- **S1** reproduction reads the seven run versions' workbooks and `check.json`, and the added deals' filings in `_dev/cockpit/state/filings/` (§7.3).
- **S2's round trip** ("a pilot copied into a temporary workspace") and **S7's** "real Mac-Gray pair" read a pilot version.
- **S3** reads `ref/seed.csv`.
- **`lesson/` is not in the worktree.** It is untracked, so a worktree made from HEAD lacks it.

**Fix:**

> "Read-only access to the cockpit state (SQLite through `file:…?mode=ro`; version and filing files by copying) for M, MIG, P, S1, S2 and S7; `lesson/` for M, MIG and A2, read at its absolute path in the live checkout; `ref/seed.csv` for S3 and P; `ref/deal_details_Alex_2026.xlsx` for P only."

### 9. The §4 examples destined for E12 reuse reviewed deals' wording and mirror the §9.3 regression cases

**Location:**
- §8: "A condensed version of §4's table goes into E12".
- §4: "None names a deal".
- §3: "Name no deal, and use no figure taken from a deal".
- §9.3: "never a target to tune the instruction against".

**Problem.** Several §4 rows restate the reviewed cases in §9.3, as below. Once they are in the instruction, those §9.3 checks test copying, not generalization.

| §4 example row | Source deal | Matching §9.3 case |
|---|---|---|
| "otherwise on the terms previously proposed" | sTec's words: "otherwise on the transaction terms previously proposed" (`raw_filing/stec_2013-08-08_DEFM14A.htm`) | "WDC's June readoption" |
| "Five weeks of exclusivity" | Synacor Company E | "five-week request" |
| The process-wide regulatory row | P&W, G&W | P&W regulatory case |
| "no financing condition; commitment letters still drafts" | Kraton | "Kraton financing" |

**Fix.** Revise §8:

> "A condensed version of §4's table goes into E12 with neutral wording and figures, and no quotation or number from a filing (for example, 'the bidder repeats its earlier terms except the price'; 'a request for several weeks of exclusivity')."

Also:
- Mark the §9.3 cases that an E12 example covers, and do not cite them as evidence of generalization.
- Add "terms previously proposed" and "five weeks" to the §9.1 grep.

### 10. The round-date rule in §3 and §8 departs from D8 and contradicts §9.3

**Location:**
- §3 E6: "One date rule for round 1 and for a reopened round: the outreach itself, or the launching decision where outreach followed within about a week".
- §8, "Round dates".
- §1 D8: "Adopt Astra's E6".
- §9.3: "Synacor and Datalink, renewed outreach | Date of the outreach itself, not the board authorization".

**Problem.** Astra's E6 says: "Use the effective outreach date, distinguishing it from an earlier board authorization" (ASTRA_APPROVAL_SPEC.md:194). The previous spec said: "Use the date the outreach actually happened, not the earlier board authorization". The new rule dates a reopened round at the board decision when outreach follows within a week. That overrides D8, which ranks higher, and contradicts §9.3.

**Fix.** Either keep D8:

> "A reopened round is dated at the outreach itself, never at the authorization; round 1 keeps line 173's decision-date route."

or record the unified rule as an amendment to D8 and change §9.3 to: "Date of the outreach, or of the launching decision if outreach followed within about a week; not routine contact".

### 11. Two adopted optional warnings conflict with D7 or D15

**Location:** §7.3 change 6: "an exit followed by activity of the same Who with no Re-entered"; "an Exclusivity changed row with the same Who and Sort date as a Bid row whose Exclusivity is Requested or Required".

**Problem:**
- **The exit warning fires on every correct D7 switch.** Under D7, a bidder that switches to a partial offer gets Withdrew and continues with Other-scope bid rows, with no Re-entered (§3 E1; §9.3 "Synacor Company E … partial talks continue as Other-scope rows"). "Activity" is also undefined.
- **The D15 warning has gaps.** It omits Bid reaffirmed rows, which audit A12a included. It also flags a legitimate same-day grant or execution, which §4 makes "its own event".

**Fix:**
- Exit warning: "an exit followed, in the same process, by a Bid, Bid reaffirmed, NDA signed or Bidding group changed row of the same Who, with no Re-entered between; Other-scope bid rows do not count".
- D15 warning: "…as a Bid or Bid reaffirmed row whose Exclusivity is Requested or Required". Its message: "if this row repeats the bid's own request, remove it (E10); a grant, execution or extension is its own event".

### 12. Scope edge cases around D7, D17 and D18: merger-of-equals talks and partial alternatives have no clear row type

**Location:**
- §3 E1: "A proposal of unresolved scope stays an Other-scope bid row (line 129), outside the whole-company counts".
- §3 E1 and D17: "Merger of equals … record the dated talks and the disclosed roles".
- §3 E10: "alternative structures offered in one communication are separate Bid rows ("alternative to #n")".
- D18.

**Problem:**
- **Merger-of-equals talks.** A merger-of-equals proposal whose sale role is unclear is a proposal of unresolved scope. It would therefore become an Other-scope row: prices blank under D18, and outside the counts and the auction screen. That pre-empts the alternative map D17 asks for. Neither the spec nor Astra (ASTRA:160, :186) gives its label. §5 still asks Alex about it (Synacor, Company B).
- **Partial alternatives.** E10 makes every alternative in one communication a Bid row, so a partial alternative (§9.3, "Kraton, Party K") would carry prices, against E1 and D18.

**Fix.** In §3 E1, add:

> "Merger-of-equals talks whose sale role is unresolved are recorded as [Bid rows with a Question | Other material event rows], never as Other-scope bid rows; the Question gives the alternative map."

Austin chooses the bracketed option; record the choice in §8. In E10, write: "…separate rows ("alternative to #n"): Bid rows for whole-company alternatives, Other-scope bid rows for partial ones".

### 13. Package P (the analysis tool) leaves mappings to guesswork and silently drops open research switches

**Location:** §7.10:
- deadline classes: "Enforced as hard; Extended and `Extended (late bid accepted)` as extended; Passed without action as soft; Unclear as missing";
- "T2: T0 on point prices only"; "T3: T0 only in a round whose finality is …";
- `bids.csv`: "the seven term and condition columns";
- `participation.csv`: "per whole-company unit";
- input: "a four-sheet working-copy export";
- `manifest.json`: "`ledger_schema` (from the S1 helper)".

**Problem:**
- **Unmapped deadline values.** Some values the tool will meet have no class:
  - `Late bids accepted`, which appears on the Mac-Gray and P&W pilots' Rounds rows 2–3 and in v1.13.2 input;
  - `No deadline stated` (P&W pilot, row 4);
  - blank.

  §9.6 requires P to run on both pilots.
- **T2 and T3 are incomplete.** They do not say what a bid outside the condition gets: Informal, or missing.
- **"Seven term and condition columns" matches no list.** Ten columns run from Stock % to Exclusivity.
- **No rule for partial-only parties.** Their NDA and Contact rows carry no scope, so "per whole-company unit" needs a rule.
- **Bids received mixes values.** The cell now holds a whole-company count plus named partial bids (§3 D3), so "where its count can be parsed" needs a pattern.
- **Audit D §4 switches are dropped.** It lists further choices blocked on Alex: eligible-but-unadmitted bidders; upfront versus package as the estimation price; the process initiator; merger-of-equals treatment. D22 forbids defaults, and the spec neither lists these as switches nor rejects them.
- **"The S1 helper" is never built.** No package delivers it: S1's eight changes add no header-reading function, and S2.1 depends on it too.
- **No safe source for working-copy exports.** A working-copy export can come only from the live server, which is not authorized, or from `Workspace` on the live state. `Workspace._connect()` opens a plain connection, not `mode=ro` (`workspace.py:196-201`).

**Fix:**
- Add deadline classes: "`Late bids accepted` (v1.13.2, or legacy in v1.14): extended, flagged `legacy`; `No deadline stated`: no deadline; blank: not reached".
- T2: "Formal if T0 is Formal and Price low = Price high, otherwise Informal". T3: "Formal if T0 is Formal and the round's Finality is Announced as final or Inferred final, otherwise Informal".
- Name the columns: Stock %, CVR/earnout, CVR/earnout value, Due diligence, Financing, Regulatory, Antitrust, Exclusivity.
- Partial-only rule: "a Who whose every bid row is an Other-scope bid is partial-only; its other rows go to `other_scope.csv` and the review list".
- Either add audit D §4's four choices as switches with no default, or emit both variants (upfront and package; counts with and without eligible-but-unadmitted bidders).
- Add S1 change 9: "`check_lean.ledger_schema(path)` reads the header only".
- Input: "working-copy exports are rendered in a temporary root from a copy of the database made with the SQLite backup API from a `mode=ro` connection".

### 14. S2.8 would label the three pre-phase-4 jobs "v1.14" once v1.14 is the default

**Location:** §7.4 item 8: "Replace the hard-coded `'v1.13.2'` fallback label (`frontend/src/runs.js:6`) with the default instruction's name."

**Problem.** The fallback applies only to jobs with no recorded instruction (`runs.js:51`: `jobInstructionLabel = job => … || INSTRUCTION_VERSION`). A `mode=ro` read of `jobs.params` shows these are the three pre-phase-4 extract jobs: PetSmart (23 September, 15:28), P&W (16:19, cancelled) and Medivation (16:30). All three ran the repository v1.13.2 (audit B, Claim 6 and B20). After gate 9 their provenance would read v1.14.

**Fix:**

> "Keep 'v1.13.2' as the label for jobs with no recorded instruction (rename it `LEGACY_INSTRUCTION_LABEL`). Use the default instruction's name only as `runSummary`'s default for a new run."

### 15. Gate 11.1 would mark untrusted reviews "Reviewed", and the Source sheet would carry that status onto the rebased copy

**Location:**
- §13 gate 11.1: "set the deal's review status, which records "reviewed at revision N"".
- §7.5: "the deal's review status from the `deal_review` table, with the revision at which it was set".

**Problem:**
- **"Reviewed" would misdescribe the copies.** The statuses are `unreviewed | in_review | reviewed` (`trace.py:35`). §7.12 describes the eight copies as "independently audited, three clusters reverted … no deal-level review status set". Audit D §6.4 says to set Reviewed "only after a checked review".
- **The Source sheet would repeat it.** After a rebase the payload reports `edited_since` (`_dev/COCKPIT_BUILD.md:60`; audit B6), but S3 prints the status and revision only.

**Fix:**
- Gate 11.1: "set the status to In review, as a bookmark at revision N, unless Austin has reviewed that working copy".
- S3: "the status, the revision at which it was set, and 'edited since' where the working revision is later".

### 16. §5 puts Final decisions to Alex as yes-or-no questions

**Location:**
- §1: ""Provisional" means … goes to Alex for a yes or no".
- §5, part 2: "Adopted decisions, yes or no".

**Problem.** Part 2 lists D4, D13, D14 and D15, and express incorporation (D1), all of which are Final. The spec does not say what happens if Alex circles "no".

**Fix.** Split §5 part 2 into:
- "Decided (for information; comments welcome)": D4, D13, D14, D15 and express incorporation;
- "Provisional (yes or no)": D5, D7, D8, D9, D10, D11, D17, and the conditions half of Q5.

### 17. §9 has no acceptance for MIG-C, S5 or S7's runner guards, and two §9.6 checks are fragile

**Location:**
- §7.0: MIG is "Needed before any rebase", but §9.6 tests only MIG-T.
- §9.6: "The pilot triage fills all four buckets".
- §9.6: "The hashes of the state files … are the same before and after every MIG and P run".

**Problem:**
- **Untested features.** The rebase-safety features that D24 relies on have no acceptance. The same is true of S5 and of the `run_model.py` guards.
- **A check that depends on the data.** "Fills all four buckets" depends on the data, not on correctness.
- **A hash check that can fail for outside reasons.** The hash check fails whenever Austin or Alex saves during a run, and "state files" is undefined. Even a `mode=ro` reader can leave `-wal`/`-shm` files: I saw them immediately after my own read (see the method note).

**Fix.** Add to §9.6:

> "MIG-C: HTTP tests on a temporary state: a rebase keeps finding judgments and resets implementation and verification; the rebase dialog payload lists counts of revisions, marks, decisions and threads; `rev:N` compares and downloads without saving a revision; an orphaned thread reads 'on an earlier base (revision N)'. S5: `main()` refuses an existing output; relocation in a temporary root resolves (finding 1). S7: `prepare --revise-from` a five-sheet workbook exits non-zero before any model call."

Also:
- Replace "fills all four buckets" with "reports a count and the rows for each bucket".
- Replace the hash check with: "the tools open SQLite only through `mode=ro` (asserted by a test); `workspace.sqlite3`, `catalog.json`, `extraction/` and `state/versions/` hash the same before and after, with no cockpit save in between".

### 18. S5 does not say what `verify_catalog.py` should assert

**Location:** §7.7: "Its assertions are stale: … Give it a new output path, or make it refuse to overwrite". Gate 12.4 then runs "the fixed `verify_catalog.py`".

**Problem.** S5 lists what is stale but not what replaces it, so "fixed" is undefined.

**Fix.** Add:

> "Replace them with:
> - every catalog version's file exists and matches its SHA-256;
> - every working copy renders at its latest revision, and its base id and hash equal `revisions.base_id` and `base_sha256`;
> - the API version list starts with 'working' and contains every catalog and imported version;
> - for unedited deals only, the working export equals the base bytes and the displayed check equals a fresh check.
>
> Write the output to a new timestamped file."

### 19. Lost content: the location of Alex's August Q&A; and `~/work/tmp` is both scratch space and its only local copy

**Location.** The previous spec's §11 ended: "Alex's August Q&A is not in the repository. Its copy is `/home/uctpiaj/work/tmp/sec-v114-recommendation-review-2026-09-25/sources/2026-08-10_QA-dialogue-consolidated_v2.docx` … `sources/qa.txt` is a text extract of it."

**Problem:**
- **The pointer was removed.** It was removed without replacement, yet the spec still cites the Q&A: D7 ("August Q&A Q7d") and D20 ("Q&A of 12 Aug"). A2's case appendix needs it.
- **Scratch space and sources share one folder.** §0 puts `TMPDIR` and every `COCKPIT_*_EVIDENCE` folder under `/home/uctpiaj/work/tmp`. That folder also holds:
  - the Q&A sources (the folder exists);
  - the previous spec;
  - §12's rollback artefacts.

  A scratch clean-up there would delete them.

**Fix:**
- Restore the paragraph in §11.
- In §0 and §9.4, use `/home/uctpiaj/work/tmp/v114-scratch/` and add: "Delete nothing else under `~/work/tmp`."

---

## Minor

### 20. Held-out hygiene is undispositioned (audit D §2.6 and §6.5)

**Location:** §13 gate 5 and §8, "Held-out deals".

**Problem.** Audit D §2.6 asks that review findings on held-out deals be kept from anyone building later instruction changes. Audit D §6.5 asks that Alex's corrected coding be used only as a third reader. `compare_alex.py` could run on Imprivata, the only held-out deal Alex corrected.

**Fix.** Gate 6: "Keep held-out review findings in a separate packet that agents writing instruction changes do not read. Run `compare_alex.py` on a held-out deal only at Austin's request."

### 21. Wrong line citations

| Spec text | What the code shows | Fix |
|---|---|---|
| §7.3 change 8: "(draft)" at `check_lean.py:2`, `:9`, `:39-44`, `:73` | The wording is only at `:40` and `:73` (grep). `:2` and `:9` say "v1.14" without "(draft)". | Cite `:40` and `:73` |
| §7.7: `import_results.py` "`:217`" | The path is built at `:216`; `:217` is `instruction_version`. | Cite `:216` |
| §7.7: `verify_catalog.py` "`:83`" | `:83` is the revision-0 check, not a path. | Drop `:83` from the path list |
| §7.3: "Only change 4 is needed" | Changes 1–3 are also needed. | "The rule review adds only change 4; changes 1–3 come from D11, the Antitrust rule and D18." |

### 22. A2's dependencies are stated three ways

§5 says "A2 depends on packages M and P", while §7.0 and §7.13 say M, R and P. Change §5 to "M, R and P".

### 23. §0 names more pilot READMEs than S6 allows now

§0 says "the pilot READMEs under `_dev/reviews/`", but S6's "Now" class lists only `_dev/reviews/2026-09-21-mac-gray-pilot/README.md:3`; the Datalink README is Release class. Write "the Mac-Gray pilot README (line 3)".

### 24. Stale lines the audits named but the spec neither adopts nor rejects

| Line | What it says now | Flagged by | Proposed class |
|---|---|---|---|
| This folder's `README.md:7` | "To use it, start a draft from v1.13.2 … and paste this text", which points readers at the superseded draft | Audit D, row 42 | Now |
| `_dev/HANDOFF.md:18` | 207/13/52 tests, against the spec's 199/14/53 | Audit D §7, item 12 | Now |
| `_dev/tools/README.md:158` | "optional model judgments" | Audit A13 | Deploy |

### 25. The header date is unspecified

§3 gives "**Revision of <date>, v1.14.**" but not which date or when it may change. A later change alters the hash (audit B11). Add: "<date> is the day A1's text, after R's fixes, is frozen for gate 4. It changes only with a new draft at gate 7."

### 26. The meaning of `Late bids accepted` is lost

**Location:**
- §7.3 legacy message: "renamed in v1.14";
- §7.8 crosswalk: "`Late bids accepted` ↔ `Extended (late bid accepted)`";
- §9.1: "the checker's value lists and the cockpit's choices all agree".

**Problem.** D11 widened the value to any required response (§5, D11 row). Audit A §2.4 labelled the pair "D11 (wider) … show both". In v1.14 the checker still accepts the legacy value (with a warning), but the choices omit it. A §2.4's `--include-source` flag and its "E12 rules changed" flag on Conditions are neither adopted nor rejected.

**Fix:**
- Message: "replaced in v1.14 by the wider 'Extended (late bid accepted)' (E9)".
- Crosswalk label: "D11 (wider): shown, not equated".
- §9.1: add "…agree, except that the checker still accepts the legacy value with a warning".
- Adopt or reject A §2.4's two flags.

### 27. Catalog versions have no receipt pointer

§7.4 item 5 says "For existing versions, read both from the stored receipt `check.json`". The catalog versions have no `receipts` field. Their receipts are `_dev/reviews/2026-09-22-opus55-reextraction/receipts/<deal>/check.json` (checker 1.5, no `ledger_schema`). Add: "for catalog versions, read that receipt, or show 'At import: not recorded'".

### 28. D20 and S3 disagree on version downloads

D20 (Final) adds the link "to the workbook downloaded from the cockpit", while §7.5 says "Version downloads stay byte-identical by default". Record in §8: "Version downloads stay raw by default; the Source sheet is an option."

### 29. §12 lacks OPS's unit step

OPS says "Installing them is a deploy step" and proposes `TMPDIR` for both units, but §12 has no such step. Add step 6a: "If Austin approves, install the units and run `systemctl --user daemon-reload`."

### 30. The order has an R ↔ S1/S2 loop

§9.1 has R check that "the checker's value lists and the cockpit's choices all agree", but S1 is "finalized after R" and S2 ships with S1. In §7.13 wave 2, add: "…then S1 and S2 finalized; then R re-runs its §9.1 value-list check."

### 31. The deal-figure rule does not reach line 249

§3 bans figures taken from deals but names only line 247. Audit C §5 notes that line 249's "50–75" is Pepco's (`TAXONOMY_DRAFT5:28`). Either replace that range too, or state that it is exempt as a bare format.

### 32. There is no instruction for undoing a rebase

Audit B6 found that restoring revision 0 after a rebase returns to the catalog base, not the rebased one, and that the Changes tab shows 0 changes. Add to gate 11: "To undo a rebase, restore the pre-rebase revision N, not revision 0."

### 33. S7's acceptance names an undefined pair

§9.6 says "on the real Mac-Gray pair …", which is undefined; "reports no change" also needs `--crosswalk`, since the columns differ. Write: "`extraction/mac-gray.xlsx` against the Mac-Gray pilot; with `--crosswalk`, the equal-content pair reports no row changes."

---

## Appendix A. Audit findings the spec does not disposition

The spec does not adopt, reject or defer these audit findings:

| Audit finding | Covered by |
|---|---|
| A §2.4: `--include-source`, the Conditions "E12 rules changed" flag, "D11 (wider)" | 26 |
| A13: tools README:158 | 24 |
| B6: undoing a rebase with restore 0; "edited since"; Changes tab | 15, 32 |
| B10: resolution depends on `extraction/<slug>.xlsx` | 1 |
| B20: keep the fallback for old rows (dispositioned the wrong way) | 14 |
| C §2 item 26: Exclusivity as a "condition column" vs "a term" | 2 |
| C §5: line 249's "50–75" | 31 |
| D row 42: maintenance README:7 | 24 |
| D §2.6 and §6.5: held-out hygiene; Alex's coding as a third reader | 20 |
| D §4: eligibility, upfront vs package, initiator and merger-of-equals switches | 13 |
| D §7, item 12: test counts in HANDOFF:18 | 24 |

C §4 (the Acquirer type list is not stated in the instruction) is also undispositioned. It is harmless, since the checker enforces the list.

## Appendix B. Citations checked

**Correct:**
- **Worker, workspace, server and data:**
  - `worker.py:50, :311, :318-321, :253-260, :354-358`;
  - `workspace.py:20, :349-357 (:353), :497, :618-621, :742`;
  - `server.py:42, :176-178, :185-194`;
  - `data.py:968-989 (:984)`.
- **Checker and its tests:**
  - `check_lean.py:131-149, :261-267, :633-640 (:635), :924-932, :1297-1307, :1525-1538, :1637-1643`;
  - `test_check_lean.py:320-341, :496, :506, :509, :510`.
- **Frontend:** `Records.jsx:12-13, :123-152`; `runs.js:6`.
- **Tools and tests:**
  - `fetch_filing.py:237`; `deals.py:240`;
  - `test_http.py:200, :206, :252`; `test_cockpit_export.py:130`;
  - `verify_catalog.py:83-84, :85-87, :97-101, :103-108, :117-119, :127-132`;
  - `export_repo.py:148-153`; `run_model.py:264`; `serve_fixture.py:93-95`.
- **Documents:**
  - `COCKPIT_APP_SPEC.md:198, :201`; `COCKPIT_BUILD.md:47, :63, :69, :73, :84`;
  - `AGENTS.md:8, :12, :14, :16`; root `README.md:5, :12, :14–17, :23, :36`;
  - `HANDOFF.md:5, :32, :46, :48, :64`; `RESEARCH_QUESTIONS.md:3, :18, :19, :27, :33, :37`;
  - tools README 19, 49, 118, 120; cockpit README 9, 13, 20, 42.
- **Draft and taxonomy:**
  - every draft line cited in §3, §3.1 and §4 that I checked (24, 26, 28, 53–64, 67, 68, 88, 89, 108, 110, 112, 121, 129, 131, 143, 153, 160, 163, 171, 173, 198, 208, 210, 220, 224, 226–232, 237–241, 245–251, 255–271, 283–286);
  - `TAXONOMY_DRAFT5:40, :60, :76`.
- **Hashes (§11):** 513c8e3e…, f9595d74…, faab1d66…, 9ddb0a38…, 32dfe7de… and 477be57f….
- **Database facts (read `mode=ro`):**
  - drafts `a4ca26ecfa92` and `73f21eb8c09a`; the default `513c8e3e8159`;
  - the latest revisions; three threads; R01 supported, applied and verified; `deal_review` empty;
  - Alex's account connected on 24 September at 09:19 UTC, with no run by Alex.
- **Services and machine:** services active since 24 September, 22:02:00 UTC; root disk 97% full (343 MB free); `node_modules` 491 MB.
- **Tests and cost:** 14 HTTP tests; 53 vitest cases; $27.690 for the nine runs.
- **Workbooks:**
  - `seed.csv` `index_url` equals the derived URL for 9 of 9 deals;
  - P&W #52 is G&W's Bid of 12 August 2016 in the pilot, and Party E's Dropped by target in v1.13.2;
  - both pilots use `Late bids accepted` on Rounds rows 2–3.

**Incorrect:**
- the "434 reviewed" count (finding 3);
- the Mac-Gray pilot delta (finding 4);
- D25's "so the working copies still resolve" (finding 1);
- `check_lean.py:2` and `:9`, `import_results.py:217` and `verify_catalog.py:83` (finding 21).

## Appendix C. Diff against the previous spec

**Lost without replacement:** the location of the Q&A (finding 19).

**Changed in a way that conflicts with the rest:**
- the reopened-round date rule (finding 10);
- the fallback label (finding 14, new in this version).

**Changed and internally consistent:**
- the header (v1.14, no "(candidate)");
- C's reread and checkpoint items, now "no change";
- E11's "a letter alone", now marked as new text;
- review status in the Source sheet;
- S5 now prepares code;
- held-out wording;
- the analysis contract brought into scope;
- the gate order (deploy before runs).

Every other item of the previous version survives, in the same place or moved.
