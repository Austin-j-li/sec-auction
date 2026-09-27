# Analysis runs, 25 September 2026 (package P)

These folders hold the outputs of `_dev/tools/derive_analysis.py` 0.2 and `_dev/tools/compare_alex.py` under [analysis contract version 0.1](../ANALYSIS_CONTRACT.md), regenerated on 25 September after the hardening pass described at the end. The tools live in separate working copies (first `/home/uctpiaj/work/tmp/v114-scratch/pkg/p`, the hardening pass and its review fixes `/home/uctpiaj/work/tmp/v114-scratch/pkg/w2pm`) and are not deployed.

**What these runs check.** They check the tool, not the ledgers (V114_SPEC §9.6). None of this is research acceptance (§9.5). The side-by-side with Alex's coding is a review aid: it is never a target for the instruction and never reaches an extraction run.

**Evaluation material.** The two `compare-alex-*` folders are derived from `ref/deal_details_Alex_2026.xlsx` and `ref/seed.csv`. Like `ref/` and `sources/`, they must not reach an extraction run or the instruction text.

## Runs

Every input was a copy in the package's temporary folder, so each manifest's `input.path` points there; the SHA-256 identifies the file. The current runs read fresh copies in `/home/uctpiaj/work/tmp/v114-scratch/tmp/w2pm-fix/inputs`, byte-identical to the first runs' inputs (same SHA-256). No workbook was written in this checkout. The runs were redone three times on 25 September: after the first review fixes (the derive tables byte-identical, only the compare-alex provenance labels changed), after the hardening pass, and after that pass's review (below; tables byte-identical, two review items added).

| Folder | Input | SHA-256 (first 12) | Schema | bids | rounds | participation | review items |
|---|---|---|---|---|---|---|---|
| `mac-gray-pilot-d7d267/` | Mac-Gray pilot version `opus55-medium-20260924-2241-d7d267` (24 September draft) | `d7d26784ec3b` | v1.14 | 13 | 3 | 13 | 4 |
| `providence-worcester-pilot-38bc24/` | P&W pilot version `opus55-medium-20260924-2241-38bc24` | `38bc2463c706` | v1.14 | 14 | 3 | 26 | 8 |
| `mac-gray-v1.13.2-extraction/` | `extraction/mac-gray.xlsx` | `407615092e6d` | v1.13.2 | 13 | 3 | 13 | 0 |
| `mac-gray-working-copy/` | Mac-Gray's cockpit working copy, revision 8 (base `opus55-medium`, which is `extraction/mac-gray.xlsx`), rendered by `--working-copy mac-gray` | `de1f3f14315d` (the rendered export, not kept; exports are not byte-deterministic: earlier runs' were `1703b535353c`, `cda60643db57` and `791970af030b`) | v1.13.2 | 16 | 3 | 13 | 0 |
| `compare-alex-mac-gray-pilot-d7d267/` | the Mac-Gray pilot against Alex's rows for deal 2575867020 | Alex file `b0bd73ddc016` | | | | | |
| `compare-alex-providence-worcester-pilot-38bc24/` | the P&W pilot against Alex's rows for deal 2994881020 | Alex file `b0bd73ddc016` | | | | | |

The working copy was rendered by the cockpit's own `Workspace.export` in a temporary root, from a copy of the database made with the SQLite backup API over a `mode=ro` connection (manifest `input.working_copy`). The first run pointed `--repo-root` at this checkout. The reruns pointed it at a folder in the package's temporary folder that held plain file copies of `workspace.sqlite3` (SHA-256 `9aee511007b4`, with no `-wal` file beside it when copied), `catalog.json` and `extraction/mac-gray.xlsx`. The tool then took its backup-API copy from that copy, so no SQLite connection was opened on the live state. The tables are byte-identical to the first run's. Its 16 bids include the three same-price Bid rows added under R01 (revisions 6–7), which the tool marks `same_price_revision`.

## Acceptance (§9.6 P)

**Every manifest is complete.** All four have every required key, a SHA-256, a `ledger_schema` from `check_lean.ledger_schema`, and an empty `incomplete` list. The two v1.13.2 inputs record `T1` and `T1u` as missing, `all_cash` from All cash, and the package as not derivable (`package_basis` says so on every bid). The manifests now record checker 1.7 (the first runs were made with 1.6).

**Every Deadline outcome value gets a class.**

| Run | Round 1 | Round 2 | Round 3 |
|---|---|---|---|
| Mac-Gray pilot | Late bids accepted → extended, legacy | Late bids accepted → extended, legacy | Enforced → hard |
| P&W pilot | Late bids accepted → extended, legacy | Late bids accepted → extended, legacy | No deadline stated → no deadline |
| Mac-Gray v1.13.2 | Late bids accepted → extended, legacy | Late bids accepted → extended, legacy | Enforced → hard |
| Mac-Gray working copy | Late bids accepted → extended, legacy | Late bids accepted → extended, legacy | Enforced → hard |

None of these ledgers has a blank Deadline outcome or `Extended (late bid accepted)`. A read of copies of all 16 ledgers available (the nine in `extraction/` and the seven cockpit version workbooks) found only Enforced, Extended, Late bids accepted, No deadline stated, Passed without action and Unclear, and each classed. Blank ("not reached"), `Extended (late bid accepted)` and an unknown value are covered by the unit tests (`test_derive_analysis.py`).

**The side-by-side reproduces audit D §3.4.**

| | Mac-Gray pilot | P&W pilot |
|---|---|---|
| Alex-labelled bids aligned | 13 of 13 | 14 of 14 |
| T0, recorded Formality alone | **13 of 13** | 11 of 14 |
| T1, Formal and not Heavy | 11 of 13 | **14 of 14** |
| T1u, Formal and None or Light | 11 of 13 | 13 of 14 |
| T2, Formal and a point price | 12 of 13 | 11 of 14 |
| T3, Formal in a final round | 13 of 13 | 11 of 14 |

No reading is the default. On these two deals no single reading reproduces both; T3 happens to match Mac-Gray fully and P&W on 11 of 14.

Alignment: Mac-Gray's 13 all align by bidder, price and date. P&W's 14 align by bidder (11), by part of a name ("Party E/F" to "Party E", 2) and by cohort size ("9 parties" to "9 IOI bidders", 1). One Mac-Gray bid and two P&W bids align on the package (upfront + CVR/earnout value): Party B's $21.50 on 18 September 2013, and G&W's $21.15 and $22.15 in July 2016.

Other agreement, for review:
- `all_cash`: Mac-Gray 12 of 13; the exception is Party B's 18 September bid, which Alex codes 0 because of its options, while the contract follows audit D §3.3 (a CVR does not change `all_cash`). P&W: 3 of 3 compared; Alex leaves the rest NA and the pilot records Stock % Not stated.
- Codes (`bid_note`): Mac-Gray 32 agree, and 2 "Drop" rows where the ledger has Did not submit, which has no Alex code. P&W 27 agree; 3 exits under another label (Did not submit or Not selected at signing against "Drop"); 3 unaligned (Alex's 25-party NDA row against the ledger's two NDA cohorts, and his "Party A" and "1 party" drops, which have no ledger exit); 1 disagree (his whole-row-red "Executed" row for Party B on 4 August, a Bid reaffirmed in the pilot); and 1 where the event agrees but not the round's finality ("Final Round" on 12 August against the round-2 Deadline row; the pilot's round 3 set no due date).
- Provenance: Mac-Gray has 4 rows with red coded fields, 8 with red only in the comment columns (coding as Chicago), 11 whole rows in red and 11 Chicago rows. P&W has 10, 11, 8 and 7. No Mac-Gray labelled bid has a red `bid_type`. Three P&W labelled bids do: Party E on 20 July, G&W on 21 July, and Alex's added Party B row.

## Review items the derive tool raised

Both pilots, the inferred exits (added in this pass): Mac-Gray #23 (16 NDA signers who did not submit), #50 (Party A) and #51 (Party B); P&W #17 (about 16 NDA signers submitting no IOI) and #57 (Party E, not selected at signing). Each has Inferred = Y and a Note that names neither an inferred field nor an inferred exit. The pilots were made under the 24 September draft, whose Inferred marked events only, but the tool reads a v1.14-schema workbook under the candidate's field-level Inferred (contract §9, §12 item 11). So their censoring variant is "unresolved", not "censored". The two v1.13.2 runs are unaffected: their inferred exits are "inferred exit" and "censored" as before.

P&W pilot, #34 (added in the hardening pass): G&W's $21.02 + $1.13 CVR. Its Note gives the package ($22.15) without saying whose figure the $1.13 is, so `package_basis` reads "basis not stated in the Note". #33, the same CVR, says "(G&W's figure)" and reads as a valuation, as does Mac-Gray's #42 (Party B's $2.50, "Party B's value"); since the second review both are listed as "confirm the package basis", because the basis is read by keyword. No package value changed.

P&W pilot, four exits of a Who with no recorded entry, each subtracted as a residual: #17 (about 16 NDA signers who submitted no IOI), #18 (two low IOI bidders), #31 and #32 (the unnamed strategic and financial non-submitters). They are members of the NDA and IOI cohorts under other names. The P&W live counts therefore carry wide bounds (the lower bound is 0 after #17's "approximately 16"); the presumed-sequence point estimate goes 25 → 7 advanced → 8 with Party C → 6 after the two non-submitters → 2 selected → 4 with the two re-entries → 3 after Party D withdrew → 0 after signing.

Apart from the three inferred exits and #42's basis to confirm, the Mac-Gray runs raise none: live units rise to 20 after the NDA cohort and end at 0 at signing; every Bids received count agrees with the rows. Neither pilot has an Other-scope bid or a partial-only candidate, so the partial-only change does not touch these runs.

## Reproduce

From the working copy, with `TMPDIR` under `/home/uctpiaj/work/tmp/v114-scratch/`, on copies of the inputs:

```
python3 _dev/tools/derive_analysis.py <copy of the version workbook> --deal mac-gray --out <new folder>
python3 _dev/tools/derive_analysis.py --working-copy mac-gray --repo-root /home/uctpiaj/work/Projects/sec-extraction --out <new folder>
python3 _dev/tools/compare_alex.py <copy of the version workbook> --deal mac-gray --out <new folder> --alex <copy of ref/deal_details_Alex_2026.xlsx> --seed ref/seed.csv
```

Each writes only to its `--out` folder, which must be new or empty and not under `extraction/`, `raw_filing/`, `ref/` or `_dev/cockpit/` of the tool's checkout or of `--repo-root`. Without `--deal`, the slug is read from the file name (contract §1) and the manifest warns when it is a guess.

## Changes after review (25 September)

An independent review found one blocker and five minor points; all were fixed and the runs redone.
- **Readings follow §7.10's "otherwise Informal".** T3 is Informal for a Formal bid in round post or in a round with no Rounds line. T2 is Informal for a Formal bid with no stated price. T1 and T1u read a blank or unlisted Conditions value as not Heavy and as not None or Light, and list it for review. None of the bids in these runs is affected.
- **Deal slug from cockpit file names.** A download named `meredith-working.xlsx` or `meredith-<version>.xlsx` is now read as `meredith`, so it stays descriptive only.
- **An exit after a win** is listed and not subtracted a second time.
- **`--out` is also refused** under the data folders of `--repo-root`.
- **Working copies.** A deal added in the cockpit renders from its oldest imported version. The base hash is taken from the copy that was rendered.
- **Provenance labels** tell red coded fields from red comments only.

## Hardening pass (25 September, wave 2)

A separate review raised four points on package P; contract version 0.1 and tool 0.2 address them without reopening a decision (D22, §7.10). The runs above were regenerated with the same inputs and read-only rules.
- **Package basis.** `bids.csv` gains `package_basis`, read from the Note under E13 (a maximum, a face amount or someone's valuation), so packages of different kinds are not read as comparable. A maximum, an unstated or mixed basis, and a CVR value without CVR/earnout Y are review items. No package value is dropped or invented. `compare_alex.py`'s `alex_bids.csv` gains `ledger_package_basis`.
- **Partial-only parties.** A Who whose every bid row is Other-scope is now only a review candidate. With an exit row (a switch to a partial offer, E1) its entry and exit count in full; with none its entry counts as the bound [0, n], point 0. Its rows are never removed from `participation.csv` or the live counts.
- **Inferred exits.** `participation.csv` gains `exit_inferred`. Under field-level Inferred (v1.14), a reported exit whose Note names only an inferred field (a date, say) is a dropout in both variants; an exit the Note calls inferred is censored in the censoring variant; anything else is "unresolved" and a review item.
- **T2** needs two present, valid (checker-accepted) and equal prices; an invalid price cell is a review item. No bid in these runs changes.
- **`all_cash`** goes through S7's crosswalk (`diff_workbooks.all_cash_for_stock`). No bid in these runs changes.

**Headline numbers.** The compare-alex agreement counts are unchanged and still reproduce audit D §3.4 (the table above), as are the alignments (13 of 13, 14 of 14), `all_cash` agreement, per-share matches, code statuses and provenance counts. The derive tables change only by the two new columns, the five inferred exits' censoring variant ("censored" → "unresolved"), and the review items listed above (Mac-Gray pilot 0 → 3, P&W pilot 4 → 7, and 4 and 8 after the second review).

**After the hardening pass's review (same day, contract still 0.1).** A second review found one major and three minor points; all were fixed and the runs redone.
- **A named inferred field no longer proves a reported exit.** An inferred exit also carries inferred fields (E14 dates it at the transition), so "inferred field: …" now needs a row with no sign of an inferred exit: When "by …", silence wording, a transition or E14, or cohort arithmetic. Otherwise the exit is "unresolved" and a review item. The five pilot inferred exits were already unresolved; nothing changes in these runs.
- **CVR basis keywords.** "Face" must be "face amount" or "face value", and "estimate" must be an estimated value or "estimated at", so "on its face" and "estimated closing" no longer give a basis. Every basis read from the Note is now a review item, a single valuation or face amount as "confirm the package basis": Mac-Gray #42 and P&W #33 are added (review items 3 → 4 and 7 → 8).
- **An invalid price cell gives no package** (`package_basis` "missing: a price cell is not a valid price"); `price_low` and `price_high` still show the cell as read. No bid here has one.
- **Process initiator.** Rows of a partial-only candidate with no exit row no longer set `initiation_first_event`; where one would have come first, it is a review item. No run here has a candidate.

Every CSV is byte-identical to the hardening pass's; the manifests differ only in the two added review items, the input paths and, for the working copy, the export's hash; the compare-alex summaries only in their input paths.
