# Reviewed-work migration: registers and the pilot triage (package MIG-T)

25 September 2026. V114_SPEC D24, §7.9 (MIG-T), §9.6, §13 gate 11. Built by `_dev/tools/migrate_review.py` (with `test_migrate_review.py`) in the separate working copy; the tool reaches the live checkout only at a deploy Austin orders.

> **Status, 26 September, about 20:45 UTC.** That deploy happened at 19:41 UTC: the live `migrate_review.py` has the v1.14.1 impact tags ([receipt](../../2026-09-26-v1141-streamline/deployment-v1141.json)). The registers and triage files here are still the 25 September ones; regenerating them needs `lesson/` and remains a GATE.

**v1.14.1 update (26 September, WP5 of `../../2026-09-26-v1141-streamline/PIPELINE_UPGRADE_SPEC.md`), not yet reflected in these files.** In the v114 working copy, `migrate_review.py` now targets v1.14.1. A fact touched by a v1.14.1 change is re-judged, never accepted on agreement. The tags are R1–R6, V1141_SPEC D1–D3 and D6 (written "v1.14.1 D1" …), and the structural cuts: "not invited: Dropped by target", "Formality routes", "Sort-date ladder", "bidders' advisers to Notes", "Contact vs interest", "Other material event list", "Initiation from the first row" (Initiation is now a register fact), "E5 process test", and "express incorporation removed", which replaces the old "express incorporation" tag. `IMPACT_TAGS_V1141` in the tool lists each tag and the facts it touches. The bucket reads "differs, v1.14.1 changed the rule", and `triage --rules v1.14` reads a run made under v1.14 (the default is v1.14.1). The registers and triages below were built by the earlier tool and still carry the v1.14 tags. Rebuilding them uses the command under Commands, which reads `lesson/independent-audit-2026-09-23` (`--audit-dir`) for status and basis. The WP5 agent was not allowed to read `lesson/`, so the rebuild waits for someone who may.

Nothing here changes a working copy. The port batches are prepared, never applied. The two pilots are superseded drafts of the 24 September instruction draft, so their triage tests the tool, not a migration (D21).

## What each deal folder holds

| File | Content |
|---|---|
| `rows.csv` | Every Deal ledger row of the latest working-copy snapshot, with its row mark (status, note, actor, time) and its count of comment threads. |
| `facts.csv`, `register.json` | The reviewed facts, in §7.9's order: participation and exits; the round map and deadline outcomes; each bid's price, Stock % (from All cash), Formality, Conditions and new terms; the order of events. `register.json` also holds the revision read, the finding decisions, the threads and the audit cross-checks. |
| `triage-<run id>.md`, `.json` | The four buckets, with counts and rows, the agrees bucket's accept and review lists, the alignment and the seeded spot-check sample (Mac-Gray and P&W only). |
| `port-batch-<run id>.json` | Edit requests in the cockpit edit API's format (`/api/deal/<deal>/edit`) for the accepted items (Mac-Gray and P&W only). |

## How a fact is built

- **Kinds.** Participation: one per entry or exit row (Event, Type, Count, Exit reason), plus the Auction screen and Whole-company bids facts. Round map: one per Rounds line (Process, Round, Opened, members, Finality) and one for its deadline (Due dates, Deadline outcome), the Number of processes fact, and the Process/Round assignment of each bid and exit row. Bids: price, Stock %, Formality, Conditions, and one "terms" fact for the v1.14 columns with no reviewed value (CVR/earnout, its value, Due diligence, Financing, Regulatory, Antitrust, Exclusivity). Order: one per ledger row (When, Sort date, Date from, Date to; When is free text, so it is shown and ported with the dates but not compared).
- **Filing key.** The page cited in Quote and page; the cockpit display block where the quote starts (`b<n>`, the numbering the audit cites, located with the cockpit's own locator); the quoted passage. A Rounds line takes the key of its Round opened row, its deadline the key of its Deadline row. Deal facts have none.
- **Basis.** *Convention* where the row is named by an open convention question in the audit's README §2 (A1–A17 and the deal-specific items) that bears on that kind of fact, or where an audit verdict on the fact's change names a convention, R01 or an Alex-stated rule. Else *inference* where Inferred is Y, the Note opens with "Inferred", or the value says it is inferred or assumed. Else *reported*.
- **Status.** *Unresolved* where the fact rests on an open convention question, an audit verdict on its change is overstated, unresolved or incorrect-and-not-reverted, or the row is marked Needs decision. Else *reverted* where an incorrect change was restored to the original (the 24 September revert; references renumbered since then are ignored). Else *supported*. Rounds lines and Deal facts carry no row mark, so their status comes from the audit alone.
- **v1.14 impact.** *Re-judge* under named decisions: D10 (Did not submit), D7 (Other-scope parties, scope wording, Auction screen, Whole-company bids), D8 (every round line and assignment, and the dates of Round opened rows), D11 (every deadline outcome, and the dates of Deadline, Deadline set and Deadline revised rows), D18 (Other-scope prices), D13 (Bid reaffirmed, same-price revisions, commitment-type Other material events), D9 and express incorporation (Formality of revisions and reaffirmations), H1–H3 on every Conditions value, with D5, D15, D16 and express incorporation where the row calls for them, and D15 on Exclusivity changed rows. *New column* for Stock % (the All cash crosswalk: Yes ↔ 0; No ↔ above 0, a range or Part stock; Not stated ↔ Not stated) and for the terms. The crosswalk is S7's own (`diff_workbooks.all_cash_for_stock` and `crosswalk`); the tool keeps no mapping of its own. Otherwise *unchanged*. The tags are mechanical flags from the row's Event, Note and neighbours; a reviewer confirms them.

## Aligner and triage

- **Rows.** Four passes, strictest first: the same Event; then the same event family (bid, exit, entry, round, adviser, public, process, other); then the family with three days' slack; then the family without the price test. No pass matches across event families. Every pass needs the same party (names normalized: case, punctuation, corporate suffixes, parenthetical short names, "(target)"), overlapping Sort-date windows and, where both rows are priced, the same price with or without the run's CVR/earnout value. A pass accepts a pair only when each row is the other's only candidate. Order is checked on the matched pairs; a same-day reordering is not counted as a change in order.
- **Rounds lines** match on an opening date within three days and at least half of the named members in common; then on the same opening date alone; then on at least half of the named members in common, whatever the date (an opening moved by more than three days). Unique matches only. Deal facts match on the field. Party names: a single letter counts only with the word before it, so "Party A" never matches "Party C (a strategic buyer)".
- **Buckets.** *Agrees*, in two lists: **accept** (after a seeded spot check), which holds only facts whose status is supported and whose v1.14 impact is unchanged; and **review**, the other agreeing facts, each with the reason it stays a review item. An agreement does not settle an unresolved fact (an open convention question, an audit verdict other than supported, a row marked Needs decision), a reverted one, a rule v1.14 changed or a new column (Stock %), and new columns inherit no acceptance. The spot-check sample is drawn from the accept list only. Then *differs where v1.14 changed the rule* (the fact's impact is not unchanged, or the difference comes from the schema, labelled as S7's crosswalk labels it: CVR shown apart, Other-scope prices blank (D18), Varies, `Late bids accepted` against `Extended (late bid accepted)`: shown, not equated); *differs where the rule is unchanged*; *omitted or inserted* (register facts whose row the run lacks, and run rows or lines no register row matches). Terms facts have no reviewed value and are listed apart for review under v1.14.
- **Port batch.** For each fact a reviewer accepts (`--accept`, one fact id per line), an `update` of the fields that differ, unless the difference comes from the schema or the reviewed value is not a v1.14 choice. Then a `review` operation carrying a row's mark to its matched run row, only where every fact of the row agrees or was accepted and ported. The mark is "reviewed" only where the old mark was reviewed and every fact of the row is supported with v1.14 impact unchanged; any fact to re-judge or any new column with no reviewed value makes it "needs_decision", so no bid row is ever ported as reviewed (its condition columns, CVR and Stock % are unreviewed; D12, gate 11.5). An order fact's update carries When with the dates, so the ported row keeps the checker's date rules (a test applies a batch after a rebase and finds no new checker issue). An accepted fact the batch cannot place (its row is omitted from the run, the difference comes from the schema, the reviewed value is not a v1.14 choice) is listed under `skipped` with the reason. Run uids are the ones the cockpit gives the run's rows once it is the base (tested against `workspace._base_state`). `revision` is left null: after the rebase, set it to the working copy's revision. One save takes at most 100 operations, so a larger batch is split into requests.

## Registers (all eight edited deals)

Read from the latest revision of each working copy. The row lists' marks equal the database's (`verify`, re-read after writing): **454 reviewed and 66 needs decision, 520 rows.**

| Deal | Revision read (saved, by) | Rows | Reviewed | Needs decision | Facts | Supported | Reverted | Unresolved | Reported | Inference | Convention | Unchanged | Re-judge | New column | Quotes located |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| kraton | r4 (2026-09-24 06:56, austin) | 75 | 57 | 18 | 243 | 146 | 0 | 97 | 141 | 19 | 83 | 93 | 109 | 41 | 239/239 |
| mac-gray | r8 (2026-09-23 21:41, austin) | 58 | 56 | 2 | 180 | 155 | 0 | 25 | 129 | 9 | 42 | 74 | 74 | 32 | 177/177 |
| meredith | r4 (2026-09-24 06:57, austin) | 88 | 61 | 27 | 338 | 126 | 3 | 209 | 267 | 18 | 53 | 98 | 168 | 72 | 334/334 |
| penford | r2 (2026-09-23 21:48, austin) | 51 | 47 | 4 | 119 | 104 | 0 | 15 | 108 | 5 | 6 | 72 | 33 | 14 | 114/114 |
| petsmart | r2 (2026-09-24 06:57, austin) | 47 | 42 | 5 | 133 | 109 | 0 | 24 | 120 | 7 | 6 | 58 | 54 | 21 | 130/130 |
| providence-worcester | r16 (2026-09-23 21:43, austin) | 63 | 60 | 3 | 191 | 175 | 0 | 16 | 172 | 3 | 16 | 90 | 71 | 30 | 187/187 |
| stec | r1 (2026-09-23 21:46, austin) | 61 | 58 | 3 | 138 | 115 | 0 | 23 | 117 | 0 | 21 | 82 | 42 | 14 | 134/134 |
| synacor | r1 (2026-09-23 21:49, austin) | 77 | 73 | 4 | 219 | 202 | 0 | 17 | 199 | 5 | 15 | 86 | 100 | 33 | 211/211 |
| **Total** | | **520** | **454** | **66** | **1,561** | **1,132** | **3** | **426** | **1,253** | **66** | **242** | **653** | **651** | **257** | **1,526/1,526** |

Other records in the registers: one finding decision (Mac-Gray R01: supported, applied); three threads (Mac-Gray deal, P&W deal, P&W row `2ffc0bdf`, #17). Every audit change on a current row carries a final `#` equal to the row's current number. Two convention references name Meredith rows without numbers and could not be tied to them: A11's "Meredith 26 LMG rows" (the rest of A11's Meredith entry, #37 and Deal facts, is tied) and A17's "Meredith LMG rows". Both are listed in Meredith's `register.json` (`convention_refs_not_resolved`); the LMG rows' basis therefore reads reported, not convention. Their status is unaffected: Meredith's 26 Bid rows are all marked Needs decision, so their facts are unresolved. Of Meredith's 209 unresolved facts, 183 belong to its 27 Needs decision rows; the rest rest on the round split (open question A1), other open questions or audit verdicts. The three reverted facts are Meredith #87's; Kraton #55's and #59's reverted cells stay unresolved because both rows are marked Needs decision.

## Pilot triage (a test of the tool)

| Deal and run | Rows matched / omitted / inserted | Rounds matched / omitted / inserted | Agrees | Differs, rule changed | Differs, rule unchanged | Omitted or inserted | Port batch |
|---|---|---|---|---|---|---|---|
| Mac-Gray, `opus55-medium-20260924-2241-d7d267` (SHA-256 `d7d26784…`) against r8 | 49 / 9 / 8 | 3 / 0 / 0 | 130 facts, 55 rows: accept 56 facts (35 rows), review 74 facts (32 rows) | 3 facts, 2 rows | 2 facts, 2 rows | 37 facts, 17 rows | 45 marks (22 reviewed, 23 needs decision; every bid row needs decision) |
| P&W, `opus55-medium-20260924-2241-38bc24` (SHA-256 `38bc2463…`) against r16 | 48 / 15 / 10 | 3 / 0 / 0 | 130 facts, 46 rows: accept 67 facts (38 rows), review 63 facts (28 rows) | 14 facts, 11 rows | 4 facts, 4 rows | 39 facts, 25 rows | 36 marks (17 reviewed, 19 needs decision; every bid row needs decision) |

The four bucket counts are the same as before the status guard (below); what changed is that the agrees bucket no longer offers every agreement for acceptance. Why the review lists hold what they do: Mac-Gray's 74 are 58 facts v1.14 re-judges (D8 on round lines, assignments and Round opened dates; H1–H3 with D5 and D15 on Conditions; D9 and express incorporation on revisions; D10, D11, D13 and D7), 11 Stock % facts (a new column) and 16 unresolved (a row marked Needs decision, an open convention question or an audit verdict); P&W's 63 are 50, 12 and 5. A fact can carry more than one reason.

Spot-check seed 1, five facts each, now drawn from the accept list only; before the guard the sample could draw an agreeing fact v1.14 re-judges or a Stock % fact (the first runs' samples held round assignments and a Stock % fact). The rows of every bucket are in the triage files. Examples: Mac-Gray #40, Party B's 09/18 $21.50, is $19.00 plus a $2.50 CVR in the pilot (rule changed: shown, not equated) and #31's Conditions Light is Unclear there (H1–H3); #47 and #48's Exit reason Not stated is Lower offer than rivals and Terms or process there (rule unchanged). P&W's G&W 07/21 and 07/26 bids are $20.02 and $21.02 plus a $1.13 CVR; the round-1 deadline outcome is Unclear in the working copy and `Late bids accepted` in the pilot; G&W's 08/12 Conditions is None against Light. P&W's Process 1 / Round 2 opens 06/01/2016 in the working copy and 05/27/2016 in the pilot with the same members; it is aligned by members and lands, with its Round opened row's dates, under the changed rule (D8). Its deadline agrees.

The pilot workbooks were copied from `_dev/cockpit/state/versions/` into the package's temporary folder, and read there.

## Commands

From the separate working copy, with `TMPDIR` under `/home/uctpiaj/work/tmp/v114-scratch/`:

```
L=/home/uctpiaj/work/Projects/sec-extraction
C="--state-db $L/_dev/cockpit/state/workspace.sqlite3 --audit-dir $L/lesson/independent-audit-2026-09-23 --filings $L/raw_filing --out $L/_dev/maintenance/2026-09-24-bid-terms-taxonomy/migration"
python3 _dev/tools/migrate_review.py register $C
python3 _dev/tools/migrate_review.py verify $C
python3 _dev/tools/migrate_review.py triage mac-gray <copy>/mac-gray.xlsx --run-id opus55-medium-20260924-2241-d7d267 $C
python3 _dev/tools/migrate_review.py triage providence-worcester <copy>/providence-worcester.xlsx --run-id opus55-medium-20260924-2241-38bc24 $C
```

The current files were built by the wave-2 working copy (`/home/uctpiaj/work/tmp/v114-scratch/pkg/w2pm`) into `/home/uctpiaj/work/tmp/v114-scratch/tmp/w2pm/migration` and copied here. The pilot workbooks were copies in `/home/uctpiaj/work/tmp/v114-scratch/tmp/w2pm/inputs` (the same SHA-256 as the version files).

## Live state before and after

The tool opens SQLite only through `file:…?mode=ro` (a test asserts it). Hashes of the live files; for the two folders, the SHA-256 of the sorted `sha256sum` listing of every file.

| Item | Before (20:41:09 UTC; again 20:58:25 and 20:59:42; after the review fixes 21:17:30 and 21:18:38) | After (20:58:45 and 20:59:51 UTC; after the review fixes 21:17:50 and 21:18:46) |
|---|---|---|
| `_dev/cockpit/state/workspace.sqlite3` | `9aee511007b49da684dfa0a9ca5108d1c7fc4fb07eeee5332d12c36c60c4c82f` | same |
| `_dev/cockpit/catalog.json` | `c48c979f9f4ff59b8452dc37735bb1a181e43ce4b60820b889bcf011b06bd193` | same |
| `extraction/` (9 files) | `603b9565456e0ee89ae4c6bd64f00347b39915072751f2b8b45004cc659685cb` | same |
| `_dev/cockpit/state/versions/` (56 files) | `f9b42e68f21fd80ff396e9c7c92563ab0a15ec0b08300d2fa7b9d9f3e1514bf1` | same |
| revisions table (read-only count and latest save) | 38 revisions, latest 2026-09-24T06:57:36Z | same |

Nothing differs, and the revisions table shows no cockpit save in between. At the first checks no `-wal` file was present. At the 21:17 and 21:18 checks a `-wal` and `-shm` pair was listed just after the check's own read-only query and was gone moments later; the revisions count and latest save are read through SQLite, which includes anything in the WAL, so no save happened in between either way.

**Wave 2 (hardening), 25 September.** The same hashes were taken before (21:36:44 UTC, and again 21:45:51 just before the run) and after (21:46:00 and 21:50:34 UTC) the rebuild of the registers, the verification and both triages:

| Item | Before (21:36:44 and 21:45:51 UTC) | After (21:46:00 UTC, and 21:50:34 UTC after every output was written and the three suites had run) |
|---|---|---|
| `_dev/cockpit/state/workspace.sqlite3` | `9aee511007b49da684dfa0a9ca5108d1c7fc4fb07eeee5332d12c36c60c4c82f` | same |
| `_dev/cockpit/catalog.json` | `c48c979f9f4ff59b8452dc37735bb1a181e43ce4b60820b889bcf011b06bd193` | same |
| `extraction/` (9 files) | `603b9565456e0ee89ae4c6bd64f00347b39915072751f2b8b45004cc659685cb` | same |
| `_dev/cockpit/state/versions/` (56 files) | `f9b42e68f21fd80ff396e9c7c92563ab0a15ec0b08300d2fa7b9d9f3e1514bf1` | same |
| revisions table | 38 revisions, latest 2026-09-24T06:57:36Z | same |

The folder hashes are the SHA-256 of `find . -type f | sort | xargs sha256sum` run inside each folder, as before. A `-wal` and `-shm` pair was listed just after each check's own read-only query and was absent at 21:44; as before, the revisions count is read through SQLite, so no save happened in between either way. The rebuilt `rows.csv`, `facts.csv` and `register.json` of all eight deals are byte-identical to the earlier ones (the crosswalk now comes from S7 and gives the same values); the verification again finds 454 reviewed and 66 needs decision; the port batches are unchanged; only the two triage files per pilot changed (the accept and review lists, and the spot-check sample).

**Wave 2, after the hardening pass's review, 25 September.** `migrate_review.py` did not change in this round (the review's four points were all in the derive tool). The registers, the verification and both triages were rebuilt once more, into `/home/uctpiaj/work/tmp/v114-scratch/tmp/w2pm-fix/migration`, from a plain file copy of `workspace.sqlite3` (SHA-256 `9aee5110…`, the same as above), so no SQLite connection was opened on the live file for the run itself; every output is byte-identical to the files here, which were therefore left as they were (verify: 454 reviewed and 66 needs decision; buckets 130/3/2/37 and 130/14/4/39; agrees accept/review 56/74 and 67/63). The same five hashes, taken at 22:00:51 UTC before the copies and runs and at 22:04:51 UTC after every output was written and the three suites had run, are identical to the table above (38 revisions, latest 2026-09-24T06:57:36Z).

The registers, the verification and both triages were regenerated at 21:18 UTC after an independent review of the tool (fixes: ported row marks, When carried with ported dates, the Rounds members pass, party-name matching, row references without numbers, skipped entries for unplaceable accepted facts, and no match across event families).
