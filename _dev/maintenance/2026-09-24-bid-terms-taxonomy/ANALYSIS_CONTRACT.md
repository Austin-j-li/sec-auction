# Analysis contract, version 0.2

26 September 2026 (version 0 and 0.1 on 25 September, 0.2 on 26 September; §13 lists the changes). Package P of [V114_SPEC.md](V114_SPEC.md) (D22, §7.10, §9.6), with WP3 of the [v1.14.1 pipeline upgrade](../2026-09-26-v1141-streamline/PIPELINE_UPGRADE_SPEC.md) and P1 of the [Astra amendment](../2026-09-26-astra-default-pro-verification/AMENDMENT_SPEC.md) (§5). Tool: `_dev/tools/derive_analysis.py` 0.3, with `_dev/tools/compare_alex.py` for the side-by-side with Alex's coding. Both are in the separate working copy and not deployed.

This contract says how a ledger becomes estimation tables. It is mechanical: every variable is either computed by a fixed rule from named ledger columns, or it is a **switch** whose choice belongs to Alex. **No switch has a default.** The tool emits every variant side by side and never picks one. Nothing here is research acceptance (§9.5): a table the tool produces from a ledger is only as good as the ledger.

The tool never corrects the ledger. Where the ledger's parts disagree (the Rounds sheet against the rows, an exit with no entry), it computes what the rows say and puts the disagreement on the manifest's `review` list.

Status labels used below:
- **Mechanical**: fixed by this contract; a later version changes it only by a new contract version.
- **Switch (Alex)**: a research choice awaiting Alex; every variant is emitted and none is the default.
- **Not derivable**: the ledger cannot supply it.

Sources: audit D §3.3 (the map from Alex's columns to the ledger) and §4 (the contract outline), audit E item 13, and the 24 September draft instruction's column definitions (D1–D5, E1–E14) as V114_SPEC §3 changes them. Version 0.1 follows the frozen v1.14 candidate's definitions where they bear on the tool: Part B (field-level Inferred), E1 and E3 (scope, entry and the switch to a partial offer), E13 (the CVR/earnout value and its basis) and E14 (exits). Version 0.2 adds the v1.14.1 candidate (SHA-256 `8bdb7c20…8a79`): Part B (Inferred marks events only; a blank price is not a price observation, H4), D5 (Initiation from the first row), E1 (the auction screen without Uncertain), E10 (Same offer, "Same as #n"), E13 (a package stated only as a whole leaves the price blank; the CVR/earnout value is the stated amount, the maximum where several; a Stock % range is Part stock with the range in the Note) and E14 (a bidder not invited into a stage is Dropped by target, R5). Where a rule below names no rule set it applies to every schema.

## 1. Inputs and provenance

| Item | Rule | Status |
|---|---|---|
| Input | One ledger workbook: a raw version (read from a copy of the version file), a four-sheet working-copy export, or a five-sheet cockpit download. | Mechanical |
| Schema | `check_lean.ledger_schema(path, rules)` (S1's helper; the one detector: a "Stock %" Deal ledger column marks a 29-column workbook). No second detector. | Mechanical |
| Rules (Q1) | v1.14 and v1.14.1 workbooks have the same 29 columns, so `--rules v1.14` or `--rules v1.14.1` says which instruction made one (the cockpit maps the instruction's SHA-256 through `check_lean.rules_for_instruction`). With no selection a 29-column workbook is **v1.14.1**; the 15 v1.14 trial workbooks are read with `--rules v1.14`. A v1.13.2 workbook ignores the selection. The manifest records `ledger_schema` and `rules_requested`. `compare_alex.py` takes the same option. | Mechanical |
| v1.13.2 input | Accepted with the columns it has. All cash gives `all_cash`. The condition-based readings T1 and T1u are missing (§7). There are no CVR/earnout columns, so the package is not derivable; v1.13.2 prices may include contingent value, which the Note describes. The manifest records all of this under `columns_missing` and `readings`. | Mechanical |
| Source sheet | A fifth sheet named `Source` (S3) is read as label/value pairs, with hyperlink targets, and copied into the manifest (`input.source_sheet`). Its layout is not assumed. | Mechanical |
| Working copy | `--working-copy SLUG` renders the working copy with the cockpit's own `Workspace.export`, in a temporary root, from a copy of `workspace.sqlite3` made with the SQLite backup API over a `mode=ro` connection, plus copies of `catalog.json` and the working base's workbook. The base is the latest revision's, else the catalog's default, else, for a deal added in the cockpit, its oldest imported version (as `Workspace.item` does). `Workspace` never runs on the live state. The rendered workbook is temporary unless `--keep-export` is given. A `mode=ro` connection to a WAL database can leave SQLite's own empty `-shm` and `-wal` files beside it; the database itself does not change. | Mechanical |
| Deal slug | `--deal`, else read from the file name as the tool and the cockpit name files: `-working-rN`, `-working`, `-with-source` and the Source sheet's version ID are stripped, and a name that begins with a known slug (`ref/seed.csv`, `catalog.json`) followed by a version suffix gives that slug, with a warning. A name that matches no known slug is kept and warned about. The slug decides `descriptive_only` (§2). | Mechanical |
| Output folder | `--out` must be new or empty, and not under `extraction/`, `raw_filing/`, `ref/` or `_dev/cockpit/` of the tool's checkout or of `--repo-root`. | Mechanical |
| Manifest | `manifest.json`: tool and contract versions, input path, SHA-256 and kind, sheets, `ledger_schema`, `rules_requested`, checker version, Source-sheet provenance, working-copy provenance (revision, base id, the hash of the base copy that was rendered, copy time), missing columns, readings computed and missing, the switches the schema feeds and, for v1.14.1, the retired ones with the reason (`switches_retired`), every Deadline outcome value with its class, row counts per output, the review list and warnings. `incomplete` lists any required key that is missing and any Deadline outcome value without a class; it must be empty. | Mechanical |

Which version counts as "the data" for estimation (a raw run or a reviewed working copy) is Austin's decision, not the tool's.

## 2. Sample

| Variable | Output | Source | Derivation | Status |
|---|---|---|---|---|
| `auction_status`, `auction_count_lo`, `auction_count_hi` | deal.csv, one row per process | Deal facts "Auction screen" | Each entry "Met / Not met (process n): …" is parsed per process; v1.14 and v1.13.2 also have "Uncertain". v1.14.1 (E1) has no Uncertain, so there an Uncertain entry is not read (the checker rejects it) and the process gets the "no Auction screen entry could be parsed" warning. Count: "a–b" gives bounds; "at least n" a lower bound; "n parties" gives n; "count unknown" none. An entry without "(process n)" is process 1 only when it is the only entry. | Mechanical |
| `auction_met` | deal.csv | as above | 1 for Met, 0 for Not met, missing for Uncertain (v1.14 and v1.13.2) or an unread entry. The screen counts independent prospective acquirers with a confidentiality agreement (E1); Chicago's `Auction` counted NDA signers, so the two differ by construction. | Mechanical |
| `whole_company` | deal.csv | Deal facts "Whole-company bids" | 1 if it starts "Yes", 0 if "No", else missing. | Mechanical |
| `descriptive_only` | deal.csv | deal slug | 1 for Meredith, which Alex keeps for descriptive work only (settled; `_dev/RESEARCH_QUESTIONS.md`). | Mechanical |
| `estimation_sample` | deal.csv | the three above | 1 if `auction_met` = 1, `whole_company` = 1 and not `descriptive_only`; 0 if any fails; missing if the screen is Uncertain (v1.14 and v1.13.2 only) or unread, or Whole-company bids unreadable. Under v1.14.1 every entry is Met or Not met, so it goes missing only on an entry the checker rejects. | Mechanical |

## 3. Bidder units and scope

| Variable | Rule | Status |
|---|---|---|
| Bidder unit (`unit`) | The Who text without parenthetical remarks, case-folded. E3 makes a parent and its shell, and joint bidders, one unit; the ledger names the unit, so the tool follows the name. A unit written with and without a parenthetical ("CSC/Pamplona", "CSC/Pamplona (…)") is one unit; a different name is a different unit. | Mechanical |
| Whole-company scope (D7) | Every row except Other-scope bid rows. The rows of a partial-only candidate (below) stay in the counts as the ledger records them. | Mechanical (D7 is provisional, Alex Q2) |
| Partial-only candidate | A Who whose every bid row (Bid, Bid reaffirmed, Other-scope bid) is an Other-scope bid. This only **nominates** a party for review: a bidder may enter the whole-company contest, make no priced whole-company offer and then switch to a partial offer, and E1 says a later partial proposal does not make earlier involvement partial after the fact. So the tool never removes such a party's rows from `participation.csv` or the live counts. Each candidate is listed once on the review list, and its other rows are also copied to `other_scope.csv`. | Mechanical (a review nomination) |
| Candidate with an exit row | The ledger's own rows decide. An exit (Dropped by target, Withdrew, Did not submit, Not selected at signing) or a Re-entered row shows whole-company participation, since partial-only parties get no exit rows (E1, E14): the entry and the exit count like any other, and the review item names the exit as the switch. If that exit comes after the party's first Other-scope bid, the review item says so, because E1 closes participation at the switch. | Mechanical |
| Candidate with no exit row | Either partial from the start (E1, E3: no entry) or a switch whose exit row is missing; the ledger cannot tell them apart. Its entry is kept as a bound, "entry (scope uncertain)": [0, n] with point 0, the point following E1's convention that a party with no exit row is partial-only. The review item says which case must be checked. | Mechanical (a bound, not a removal) |
| `other_scope.csv` | The Other-scope bid rows of any party, with `reason` "Other-scope bid", and the other rows of partial-only candidates, with `reason` "partial-only candidate (also in participation.csv)". Prices are blank on v1.14 and v1.14.1 Other-scope rows (D18; v1.14.1 D2). | Mechanical |
| A switch to a partial offer | The ledger closes whole-company participation with an exit row (usually Withdrew) whose Note says talks continued (E1). The tool counts that exit like any other. A switch by a party that also made whole-company bids is not flagged (it is not a candidate); a candidate's switch is named on the review list. | Mechanical (gap: a switch after whole-company bids is in the Note only) |
| Break-up weighed against a sale | Only in a Question naming the parties (D7). A wider count must be rebuilt by hand. | Not derivable |

## 4. Live counts (participation.csv)

One row per participation event in the whole-company contest, per process, in ledger order, with the live units after it; Round opened rows are included, so each round's opening count is visible. E14's formula: **live units = first entries + re-entries − exits − group and process closures**, each counted once. Count is never summed across rows as a population.

| Element | Rule | Status |
|---|---|---|
| Row count | `Count` when it is a positive integer. Otherwise the Note's "Count: …" prefix: "a–b" → [a, b]; "at least n" → [n, open]; "more than n" → [n+1, open]; "at most n" → [1, n]; "fewer/less than n" → [1, n−1]; "approximately / about n" → [1, open] with point n; "unknown" or "not stated" → [1, open]. No prefix, or an unreadable one, → [1, open] and a review item. v1.14.1 creates no ranges (B, E3): a numeric range is still read as bounds, and is a review item; a qualifier ("more than ten" written with a figure) is read as before. Output: `count_kind`, `count_lo`, `count_hi`, `count_point` (blank = open or unknown). | Mechanical |
| Entry | A unit's first NDA signed, Bid or Bid reaffirmed row in the process (E3: signing or reusing a confidentiality agreement, bidding). Admission to a stage has no row of its own, so it is not an entry here. | Mechanical |
| Entry of uncertain membership | A unit first seen **bidding** after a cohort (Count other than 1) has entered the process may be one of that cohort's members (E3 keeps later-named members inside the cohort's Count). Its entry adds [0, count] with point 0. An NDA signed row always adds its count (E3: a cohort row holds the remainder). | Mechanical |
| Entry of uncertain scope | A partial-only candidate with no exit row (§3): its entry adds [0, count] with point 0, change "entry (scope uncertain)". | Mechanical |
| Re-entry | A Re-entered row adds its count; one without a recorded exit for the unit is listed. | Mechanical |
| Exit | Dropped by target, Withdrew, Did not submit, Not selected at signing: subtracts the row's count. An exit of a Who with no recorded entry (a residual cohort, or members of an earlier cohort under another name) is subtracted and listed. A second exit of the same unit, or an exit after its win, without a Re-entered row is listed and not subtracted again. | Mechanical |
| Win | Merger agreement signed closes the signing unit's participation (E14: "or the win"). | Mechanical |
| Group change | Bidding group changed: the change is M − N where the Note says "N … units become M" (E4's wording); otherwise [−1, +1] with no point, and a review item. | Mechanical |
| Process closure | Process terminated closes every live unit of its process; Process restarted closes those of the previous process (E5). A closure Count that differs from the point estimate is listed. | Mechanical |
| Bounds | `live_lo` = lower bounds of entries − upper bounds of exits, never below 0 (an exit with an open upper bound sets it to 0); `live_hi` = upper bounds of entries − lower bounds of exits, blank (open) once any entry is open above; `live_point` uses the point values and is blank once any point is unknown. `delta_lo`, `delta_hi` and `delta_point` give each row's signed change (blank = open). | Mechanical |
| How estimation uses a range | Emitted as `live_lo`, `live_hi` (bounds, or one bound) and `live_point` (the ordinary sequence presumed: a party first seen bidding after cohorts is presumed a cohort member, "approximately n" is n). | **Switch (Alex): count ranges** |
| End of process | If the point estimate is not 0 at the end of a process, the units still open (at the filing cutoff, or an exit is missing) are listed. | Mechanical |
| Did not submit in v1.13.2 | v1.13.2 called it "not necessarily permanent"; v1.14 (D10) makes it an exit that ends participation. The tool treats it as an exit in both and lists a later bid by the same unit without a Re-entered row. | Mechanical |

`bids.csv` carries `live_lo`, `live_hi` and `live_point` after each bid row, so a bid can be read against the rivals live at that moment.

## 5. Rounds, finality and deadlines (rounds.csv)

One row per Rounds line (process, round).

| Variable | Source | Derivation | Status |
|---|---|---|---|
| `opened`, `how_opened`, `finality`, `how_it_ended` | Rounds | As recorded. Finality: Announced as final, Inferred final, Not final (E6). | Mechanical (the map is provisional under D8; Alex Decision 1) |
| `due_dates_reached` | Rounds "Due dates" | The first date in each "→"-separated part, skipping parts marked "superseded before arrival" or "future at filing". | Mechanical |
| `deadline_values`, `deadline_classes`, `deadline_legacy` | Rounds "Deadline outcome" | Split on ";", one value per due date reached, in order; each value gets one class (table below). A value matches a label exactly, or begins with it followed by a non-alphanumeric character, so annotations survive. | Mechanical (D10, D11 provisional; Alex Part 2, Q7) |
| `deadline_rows` | Deal ledger | The number of Deadline rows in the round. A different number of dated outcomes is listed. | Mechanical |
| `bidders_bid_lo`, `bidders_bid_hi`, `bidders_bid` | bids.csv | Distinct whole-company units with a Bid or Bid reaffirmed row in the round; a cohort row contributes its count bounds. Distinct Who values are distinct units, as E3's remainder rule requires. | Mechanical |
| `bids_received_count`, `bids_received_check` | Rounds "Bids received" | The cell's leading integer is the whole-company count (§3 D3). "ok" if it lies within the bounds above, "mismatch" (listed) if not, "not compared" if the cell has no leading integer. Named partial bids in the same cell are not counted. | Mechanical |
| `who_was_in_count`, `not_admitted` | Rounds "Who was in" | The leading integer (bidders admitted, or invited under v1.14.1); `not_admitted` = Y where a v1.14 or v1.13.2 cell lists bidders "still being received, not admitted". v1.14.1 deleted those lists: a bidder not invited into a stage gets a Dropped by target exit (E14, R5), so `not_admitted` is always blank there. | Mechanical |
| `live_open_lo/hi/point`, `live_max_hi` | participation | Live units at the Round opened row, and the largest upper bound during the round. A `who_was_in_count` above `live_max_hi` is listed. | Mechanical |
| Eligible but unadmitted bidders as live | the two above | Variant "admitted only": `who_was_in_count`. Variant "all live units": the ledger's live counts, which include parties still being received. | **Switch (Alex): eligible but unadmitted** (v1.14 and v1.13.2; retired for v1.14.1, whose live counts already close the uninvited) |

**Deadline classes, one per due date:**

| Deadline outcome value | Class | Note |
|---|---|---|
| Enforced | hard | |
| Extended | extended | |
| Extended (late bid accepted) | extended | v1.14 (E9, D11) |
| Late bids accepted | extended | flagged `legacy`: the v1.13.2 value, or legacy in a v1.14 workbook (checker warning) |
| Passed without action | soft | |
| Unclear | missing | |
| No deadline stated | no deadline | only when no date was set |
| blank | not reached | no due date reached while operative |
| anything else | `unmapped` | listed; the manifest is then incomplete |

A missed deadline without departure is not an exit (D10); per-bidder differences in a round's deadline appear only in Notes and Questions.

## 6. Bid observations and prices (bids.csv)

One row per whole-company Bid and Bid reaffirmed row. Other-scope bids are in `other_scope.csv`.

| Variable | Source | Derivation | Status |
|---|---|---|---|
| Identifying fields | #, When, Sort date, Date from, Date to, Who, Type, Event, Process, Round | As recorded; `unit` as §3. Sort date is the sequence key; Date from and Date to are bounds. | Mechanical |
| `count`, `count_lo`, `count_hi` | Count, Note | §4. | Mechanical |
| `price_low`, `price_high` | Price low, Price high | Upfront per-share amounts (E13). One-sided statements fill one cell; imprecise ranges are blank; under v1.14.1 a package stated only as a whole leaves both blank (the package is in the Note). | Mechanical |
| `upfront_price_kind` | Price low, Price high | P1, from validated values only (a valid price is a finite number above 0, as below): `point` (two valid, equal prices), `range` (two valid prices, low below high), `lower_bound` (only Price low, valid), `upper_bound` (only Price high, valid), `not_available` (both blank), `invalid` (a filled cell that is not a valid price, or Price low above Price high; a review item). `not_available` is not "no economic price" or "commitment-only": it also covers an undisclosed offer and an inseparable package, and the row stays in bids.csv with all its other fields. Users of point-price models also require `point`. | Mechanical |
| `cvr_earnout`, `cvr_value` | CVR/earnout, CVR/earnout value | As recorded (29-column workbooks, v1.14 and v1.14.1, only). | Mechanical |
| `package_low`, `package_high` | Price + CVR/earnout value | Package = upfront + CVR/earnout value, per endpoint; equal to upfront where no CVR is marked; missing where a CVR is marked (Y or Varies) without a value, where a filled price cell is not a valid price (below), and for v1.13.2 input. Verified on the three CVR rows in the pilots (audit D §3.3). No value is dropped or invented: `package_basis` says what the sum is. | Mechanical |
| `package_basis` | CVR/earnout, CVR/earnout value, Note | What the package is, so that sums of different kinds are not read as comparable. **v1.14.1:** E13 fixes the basis: the CVR/earnout value is the stated per-share amount, the maximum where several (the Note says which), so every package with a CVR is "upfront + CVR/earnout value (the stated per-share amount, the maximum where several; E13)" and the Note is not read. The "missing" and "not marked Y" values below still apply, plus "missing: the price range is reversed". **v1.14:** the v1.14 E13 says the Note tells "whether that is a maximum, a face amount or someone's valuation, and whose", and never to add a maximum to a package valued on another basis. The tool reads the Note's sentences that state the CVR/earnout amount or name a CVR, earnout, contingent value or payment, or milestone, and looks for a maximum ("maximum", "up to", "as much as", "at most", "capped"), a face amount ("face amount", "face value", "nominal amount", "nominal value"; "on its face" is not one) or a valuation ("valuation", "values", "valued", "'s value", "'s figure", "'s estimate", "estimated value", "estimated at", "worth"; an "estimated closing" is not one). Values: "upfront only (no CVR/earnout)"; "upfront + CVR/earnout value (a valuation, per the Note)"; "… (a face amount, per the Note)"; "… (a maximum, per the Note): an upper bound, not comparable with packages on another basis"; "… (basis not stated in the Note)"; "… (the Note reads as more than one basis: …)"; "upfront + CVR/earnout value, with CVR/earnout not marked Y"; "missing: no upfront price"; "missing: a price cell is not a valid price"; "missing: CVR/earnout marked without a value"; "missing: CVR/earnout Varies on a cohort row (amounts in the Note)"; and, for v1.13.2 input, "not derivable: v1.13.2 has no CVR/earnout columns". Every basis the tool reads from the Note is a review item: a maximum, an unstated or mixed basis and an unmarked value as problems, a single valuation or face amount as "confirm the package basis", since a keyword reading can mislabel ordinary wording. | Mechanical (the reading of the Note nominates; a reviewer confirms) |
| Estimation price | the three above | Variant "upfront": `price_low`, `price_high`. Variant "package": `package_low`, `package_high`, compared only among bids with the same `package_basis`. | **Switch (Alex): upfront or package** |
| `stock_pct`, `stock_kind`, `stock_lo`, `stock_hi` | Stock %, Note | A number n → [n, n]; Not stated and Varies are kinds with no bounds. v1.14: a stated range "a–b" → kind "range", [a, b]; Part stock has no bounds. v1.14.1 (E13) records a stated range as Part stock with the range in the Note: Part stock whose Note gives a percentage range ("40–60%", "40 to 60%") → kind "part stock (range in the Note)", [a, b] (0 ≤ a ≤ b ≤ 100); other Part stock has no bounds; a range in the cell, which v1.14.1 does not allow, → kind "range (not a v1.14.1 value)", [a, b], and a review item. | Mechanical |
| `all_cash` | Stock % (v1.14, v1.14.1); All cash (v1.13.2) | One mapping for both schemas: the 29-column Stock % goes through S7's crosswalk (`diff_workbooks.all_cash_for_stock`) to the All cash value it stands for, then Yes → 1, No → 0, anything else → missing. So 0 → 1; a figure above 0 (up to 100), a stated range with an upper end above 0 (including "0–50") or Part stock (including v1.14.1's Part stock with the range in the Note) → 0; Not stated, Varies, blank or an invalid value → missing. A CVR does not change it (audit D §3.3). v1.13.2: Yes → 1, No → 0, Not stated → missing. | Mechanical |
| `formality`, `conditions`, `due_diligence`, `financing`, `regulatory`, `antitrust`, `exclusivity` | the columns of the same names | As recorded. Varies on a cohort row is kept; the split is only in the Note, so it is missing at cohort level. | Mechanical |
| `inferred`, `flag` | Inferred, Flag | As recorded. | Mechanical |
| Price validity | Price low, Price high | A price the checker accepts (`bid.price_type`): a finite number above 0. A filled cell that is not one (text, zero, negative) is a review item, gives no point price for T2 and no package (`package_basis` "missing: a price cell is not a valid price"). `price_low` and `price_high` still show the cell as read, so the ledger's value is not dropped. | Mechanical |
| `same_offer_of` | Note | n where the Note begins "Same as #n" (E10's Same-offer row: the bidder says its earlier offer stands, and the row copies #n, changing only the date, Round, Formality and conditions reported anew). Read in every schema; only v1.14.1 writes the prefix (v1.14 wrote "Terms: as #n", which is not read). A prefix that does not point to an earlier whole-company bid row of the same unit, or a Same-offer row whose prices differ from #n's, is a review item. | Mechanical |
| `same_price_revision` | Price low, Price high, CVR/earnout value, `same_offer_of` | Y on a Bid row (not Bid reaffirmed) whose Price low, Price high and CVR/earnout value equal those of the same unit's previous Bid or Bid reaffirmed row in the process, **unless it is a Same-offer row**: a Same-offer row copies its price by E10, so it is a restatement (`same_offer_of`), never also a same-price revision. The previous row is literally the unit's last bid row, whatever it holds: a blank-price row in between breaks the comparison (no unseen price continuity is inferred). Rows with both prices blank are never marked. Equal recorded figures do not prove identical economic terms. This covers D13's same-price commitment revisions and any same-price repeat. | Mechanical |
| New price observation | `upfront_price_kind`, `same_price_revision` | Variant "new observation": `price_obs__same_price_as_new`, 1 on every row whose `upfront_price_kind` is point, range or a bound, 0 on not_available and invalid (P1, H4). Variant "change of terms only": `price_obs__same_price_as_terms`, as the first but also 0 on rows marked `same_price_revision`. Bid reaffirmed rows are told apart by Event; Same-offer rows by `same_offer_of` (next row). P1 applies to every schema. | **Switch (Alex): same-price revisions** |
| Restatements | `same_offer_of` | Variant "kept": every bids.csv row. Variant "dropped": rows with `same_offer_of` blank. A Same-offer row's price-observation flags follow the row above, as for any row; the two switches are independent. | **Switch (Alex): Same-offer restatements** (questionnaire 3.3(b)) |
| `round_finality` | Rounds Finality of the bid's round | As recorded; blank for round 0, post, or a round with no Rounds line (listed). T3 reads a blank as not final (§7). | Mechanical |

## 7. Formality readings

Each reading is computed for every bid; **none is the default**. As V114_SPEC §7.10 settles, a bid recorded Formal is Formal under a reading when the reading's test holds and **Informal otherwise**. The only missing values are a bid whose recorded Formality is Unclear (or blank), which is missing under every reading, and T1 and T1u on v1.13.2 input, which has no Conditions levels. An Informal bid is Informal under every reading.

| Reading | A bid recorded Formal is Formal when | Otherwise |
|---|---|---|
| T0 | always (Formality as recorded) | |
| T1 | Conditions is not Heavy (None, Light or Unclear; also a blank or unlisted value, which is listed for review) | Informal |
| T1u | Conditions is None or Light (Unclear counts as Heavy; a blank or unlisted value is not None or Light) | Informal |
| T2 | Price low and Price high are both present, both valid prices (finite numbers above 0, as the checker requires) and equal. A one-sided price, a bid with no stated price, and an unsplittable package whose price cells E13 leaves blank have no point price | Informal |
| T3 | its round is a numbered round whose Rounds line records Finality Announced as final or Inferred final | Informal: round 0, round post, a round with no Rounds line (listed for review), and any other Finality |

Exclusivity never changes a reading (D14). Which reading is primary is **Switch (Alex): Formality reading** (Decision 3b). How Unclear is treated is **Switch (Alex): Unclear**: Formality Unclear and deadline Unclear are missing as above; Conditions Unclear is not Heavy under T1 and Heavy under T1u, so T1 and T1u are its two bounds.

On the two pilots, recorded Formality alone (T0) matches Alex's labels on 13 of 13 Mac-Gray bids and 11 of 14 P&W bids; "Formal and not Heavy" (T1) on 11 of 13 and 14 of 14 (audit D §3.4, reproduced in [analysis/](analysis/README.md)).

## 8. The switches (none has a default)

| Switch | Source | Variants emitted |
|---|---|---|
| Count ranges | D22; Alex Q1 / Decision 3 | `live_lo`, `live_hi` (bounds, or one bound); `live_point` (ordinary sequence presumed) |
| Unclear | D22 | missing (Formality, deadlines); T1 against T1u for Conditions |
| Primary Formality reading | D22; Decision 3b | T0, T1, T1u, T2, T3 |
| Same-price revisions as new price observations | D22; D13; Decision 3b; P1 | `price_obs__same_price_as_new`, `price_obs__same_price_as_terms` (both 0 where no price is available) |
| Same-offer restatements kept or dropped | v1.14.1 E10 (R1); questionnaire 3.3(b) | every bid row against rows with `same_offer_of` blank |
| Inferred exits as dropouts or censoring | D22; Decision 3b | `exit__inferred_as_dropout`, `exit__inferred_as_censoring` (v1.14 only: "unresolved" where the Note does not show whether the departure or only a field is inferred; §9) |
| Eligible but unadmitted bidders as live (v1.14 and v1.13.2; retired for v1.14.1) | audit D §4; §7.10 | `who_was_in_count` against the ledger's live counts |
| Upfront or package as the estimation price | audit D §4; §7.10 | `price_low/high` against `package_low/high`, the package read with its `package_basis` (§6) |
| Process initiator (v1.14 and v1.13.2; a check for v1.14.1, below) | audit D §4; §7.10; Alex's Q&A ("re-generate it in the estimation code") | `initiation_recorded` (Deal facts) against `initiation_first_event`: the first Target interest or Target sale decision (target-led), Bidder interest or Bid (bidder-led), or Activist (activist-influenced) row in the process, with `initiation_first_row`. Rows of a partial-only candidate with no exit row (§3) are skipped, since it may never have been in the whole-company contest; where one of its rows would have come first, that is a review item. |
| Merger-of-equals talks counted or not (v1.14 and v1.13.2; retired for v1.14.1) | D17; audit D §4; §7.10 | "Not counted" is the ledger as recorded (every output). "Counted" is **not derivable**: the alternative map lives in a Question's text. `merger_of_equals_rows` lists the rows and Questions that mention a merger of equals, for a manual rebuild. |

The manifest's `switches` list carries the switches the workbook's schema feeds, and `readings.default` is null.

**Retired for v1.14.1** (listed with the reason in the manifest's `switches_retired`; still emitted for v1.14 and v1.13.2 workbooks):
- *Eligible but unadmitted*: v1.14.1 deleted the Rounds lists of bidders not admitted, and a bidder not invited into a stage gets a Dropped by target exit (E14, R5), so the live counts already exclude it. `not_admitted` is blank.
- *Merger of equals*: v1.14.1 deleted the alternative-map Question; the counterparty stays outside the whole-company contest unless the filing reports the target being sold to it, and the talks are Other material event rows (E1). `merger_of_equals_rows` lists those rows only, and no warning is given.
- *Process initiator*: D5 makes Initiation mechanical. `initiation_first_event` follows D5 for each process: an Activist row before round 1 (Round 0) of the process decides activist-influenced; otherwise the earliest Target interest or Target sale decision row (target-led) or Bidder interest or Bid row (bidder-led) decides, a later Activist row counting for nothing. Rows of a partial-only candidate with no exit row are skipped as above. `initiation_check` (deal.csv, process 1 only, since D5 reads process 1) compares the Deal facts value with it: "agrees" (the value begins with the derived label), "differs" (a review item on the Deal facts sheet), "not recorded" or "not derivable (no initiating row)". For v1.14 and v1.13.2 it is blank. The checker does not make this comparison.

## 9. Exits

| Variable | Source | Rule | Status |
|---|---|---|---|
| `exit_actor` | Event | Dropped by target → target; Withdrew → bidder; Did not submit → bidder (a non-submission); Not selected at signing → target (it signed with another). | Mechanical |
| Timing | When, Sort date, Date from, Date to, Inferred | As recorded: an inferred exit has Inferred = Y, When "by …", and Date to the transition's latest supported date (E14). | Mechanical |
| `exit_reason` | Exit reason | As recorded. Inferred exits carry Not stated unless the filing reports a reason (E14). Actor, timing and reason are kept separate (E14). | Mechanical |
| `alex_drop_code` | Event, Exit reason | Dropped by target → DropTarget. Withdrew with "Value below earlier offer" → DropBelowInf; "Value at earlier offer" → DropAtInf; either market-price reason → DropM or DropBelowM (audit D §3.3 names the pair without saying which reason is which); any other reason → Drop. Did not submit and Not selected at signing have no Alex code. | Mechanical (the DropM/DropBelowM pairing is open) |
| `exit_inferred` | Inferred, Note | What Inferred = Y marks on an exit row. Blank: not inferred (a reported exit). v1.13.2 and v1.14.1 input: "inferred exit", since their Inferred marks inferred events only (v1.14.1 Part B allows it only on exit, Round opened and Process restarted rows); the Note is not read. v1.14 input only, where Part B's field-level Inferred may mark an inferred field of an exit the filing reports and the Note names the field: "inferred exit" where the Note says the exit itself is inferred ("Inferred exit", "Inferred: closure", "exit inferred"); "inferred field: date" (or exit reason, type, count; several are listed) where the Note names only inferred fields ("Date inferred", "inferred timing", "the exit reason was inferred") and nothing in the row points to an inferred exit; otherwise "unresolved", a review item. An inferred exit carries inferred fields too (E14 dates it at the transition), so these signs keep a named field unresolved: When starting "by " (E14's form), silence ("never mentioned again", "from silence", "no submission", "no further"), a transition or E14 named, or cohort arithmetic ("25 NDA signers - 9 IOI bidders"). The reading is strict: a sign never makes an exit "inferred exit" either; it goes to a reviewer. | Mechanical (unresolved goes to a reviewer) |
| Inferred exits | `exit_inferred` | Variant "dropout": `exit__inferred_as_dropout` (every exit a dropout). Variant "censoring": `exit__inferred_as_censoring`: "censored" on an inferred exit; "dropout" on a reported exit, including (v1.14) one with only an inferred field; "unresolved" where `exit_inferred` is unresolved (v1.14 only), never a dropout classification by default. | **Switch (Alex): inferred exits** |

## 10. What the ledger cannot supply

- Compustat identifiers (`gvkeyT`, `gvkeyA`) and the target's shares outstanding (`cshoc`), so aggregate bids (total equity or enterprise value) cannot be put per share; their amounts stay in the Note.
- The effective date (`DateEffective`): it falls after the filing, the ledger's evidence cutoff (E8).
- Bidder nationality and public or private status (`bidder_type_nonUS`, parts of `bidder_type_note`), beyond Note text.
- Market prices and premiums over an unaffected price (D23, backlog); filing-reported references stay in Notes.
- Free-text comments (Alex's `additional_note`, `comments_1–3`); the ledger's Notes and Questions are not variables.
- The filing's URL and filing metadata, which come from the pipeline (`seed.csv`, the Source sheet), not from the ledger.

## 11. The side-by-side with Alex's coding (`compare_alex.py`)

A review aid (D22, §9.5): never a target for the instruction, never shown to an extraction run, and on a held-out deal run only at Austin's request (§13, gate 6). Its outputs derive from `ref/` and stay in evaluation folders.

- **Join:** the deal slug to `ref/seed.csv`'s `deal_number`, to Alex's `DealNumber`.
- **Labelled bids:** Alex rows whose `bid_type` is Formal or Informal (the one "Informsl" typo is Informal). Each is aligned to at most one whole-company Bid or Bid reaffirmed row, and each ledger row to at most one Alex row:
  - price: Alex's lower and upper values equal the ledger's upfront pair, or its package pair (upfront + CVR/earnout value), to half a cent;
  - bidder: the same name, a shared "/"-separated part ("Party E/F" and "Party E") or one name inside the other, or cohorts of the same size ("9 parties" and "9 IOI bidders"); a price-and-date match within 7 days with no name match is reported as such;
  - date: Alex's precise date, else his rough date, against the row's Date from–Date to window (0 inside it); ties go to the pair whose rough date is closer.
- **Reported per aligned bid:** agreement of `bid_type` with T0, T1, T1u, T2 and T3 (a missing reading is not compared); of `all_cash`; and whether Alex's per-share value equals the upfront price or the package.
- **Codes (`bid_note`)** against Event and Exit reason, by audit D §3.3's map: NA → Bid or Bid reaffirmed (whole company); NDA → NDA signed; Drop → Withdrew; DropM, DropBelowM → Withdrew with a market-price reason; DropBelowInf, DropAtInf → Withdrew with the earlier-offer reasons; DropTarget → Dropped by target; Executed → Merger agreement signed; IB, IB Terminated → Adviser, Adviser ended; Target Sale → Target sale decision; Target Sale Public → that or Sale process announced; Sale Press Release → Sale process announced; Bidder Sale → Bid; Bid Press Release → Bid announced; Bidder Interest, Target Interest → the same labels; Activist Sale → Activist; Terminated, Restarted → Process terminated, Process restarted; "Exclusivity …" → Exclusivity changed; "Final Round [Inf] [Ext] [Ann]" → Deadline set or Round opened for Ann (a Round opened row that sets the due date needs no Deadline set row, E9), plus Deadline revised for Ext Ann, Deadline or Deadline revised for Ext, Deadline otherwise, in a round whose Finality is final, or not final where the code says Inf. A labelled bid's code is checked on its aligned row. Other rows are matched by bidder (when Alex names one; a cohort by its size) within 31 days of either of his dates. Statuses: agree; event agrees, round finality differs; exit, other label or reason (a Drop code against another exit label, such as Did not submit, which has no Alex code); disagree; unaligned.
- **Provenance:** each Alex row is marked "Alex: whole row in red (added or rewritten)" (30 or more red cells), "Alex: red-font correction" (a red cell outside the comment columns), "Alex: red comments only (coding as Chicago)" (red only in `comments_1–3`), or "Chicago coding". `red_cells` names the red columns. Red is font colour FFFF0000, or FF9C0006 (dark red; two P&W cells and 98 Saks cells). Only nine deals carry corrections: P&W, Medivation, Imprivata, Zep, PetSmart, Penford, Mac-Gray, Saks and sTec; any other deal is all Chicago coding.
- **Outputs:** `alex_bids.csv`, `alex_events.csv`, `summary.json`.

## 12. Calls made in versions 0, 0.1 and 0.2

Where the spec is silent, the contract takes the conservative choice and records it here:
1. T2 reads "Price low equals Price high" as two present, valid (checker-accepted) and equal prices, so a Formal bid with no stated price, a one-sided price, an unsplittable package with both price cells blank, or a non-numeric price is Informal under T2 (§7.10's "otherwise Informal").
2. T3 reads a round with no recorded final Finality as not final: round 0, round post and a numbered round with no Rounds line are Informal under T3 (§7.10's "otherwise Informal"); the missing Rounds line is listed for review.
3. A Formal bid with a blank or unlisted Conditions value is Formal under T1 (it is not Heavy) and Informal under T1u (it is not None or Light), as §7.10's wording gives, and is listed for review.
4. The package is missing where a CVR is marked without a value.
5. "Approximately n" is a bound [1, open] with point n, not an exact count.
6. A party first seen bidding after cohort entries is of uncertain membership (§4).
7. The merger-of-equals "counted" variant is not computed.
8. The review list lives in `manifest.json` (`review`), since §7.10 fixes the six output files.
9. `compare_alex.py` treats DropM and DropBelowM as one family (§9), and accepts Round opened for a "Final Round … Ann" code (§11).
10. (0.1) A partial-only candidate is nominated, never removed: with an exit row it counts in full until the exit; with none its entry is the bound [0, n], point 0 (§3, §4).
11. (0.1; from 0.2 for v1.14 workbooks only, since v1.14.1 has no field-level Inferred) A v1.14-schema workbook is read under the candidate's field-level Inferred. The two pilots were made under the 24 September draft, whose Inferred marked events only; their inferred exits name no field, so they are listed as unresolved rather than classed from the schema.
12. (0.1) `package_basis` is read from the Note by keyword; the package's value is never changed by it, and every basis read from the Note is a review item (a single valuation or face amount as a confirmation), since keywords can mislabel ordinary wording.
13. (0.1) `all_cash` follows S7's crosswalk, as MIG-T does, so the two tools and `diff_workbooks.py --crosswalk` share one mapping. §7.8 maps any range to No, so a stated range starting at 0 ("0–50") is 0, where version 0 left it missing under §7.10's "above 0". A range that includes 0 does not establish stock; if that matters, the crosswalk and this contract change together.
14. (0.1; from 0.2 for v1.14 workbooks only) An exit whose Note names an inferred field is a reported exit with that field inferred only where nothing in the row points to an inferred exit (item 11, §9); otherwise it is unresolved.
15. (0.1) A filled price cell the checker rejects gives no package but stays in `price_low`/`price_high` as read (§6).
16. (0.1) A partial-only candidate with no exit row does not initiate its process in `initiation_first_event` (§8); a candidate with an exit row does, since the ledger records its whole-company participation.
17. (0.2) A 29-column workbook with no rules selected is v1.14.1 (Q1). The v1.14 readings stay reachable with `--rules v1.14`, so the 15 trial workbooks read as they did, apart from P1 and the new columns.
18. (0.2) P1 and `same_offer_of` apply to every schema. P1 was written for v1.14 and states a general fact about the price cells; `same_offer_of` fires only on a "Same as #n" prefix, which only v1.14.1 writes. The field-level Inferred reading, the Uncertain auction status, `not_admitted`, the Note-keyword `package_basis` and the three retired switches stay for v1.14 (and, where they applied, v1.13.2) workbooks, because their content differs from v1.14.1's.
19. (0.2) A Same-offer row is never a `same_price_revision`; its price-observation flags follow P1 like any row, and whether restatements are kept is its own switch, so the two choices do not interact.
20. (0.2) A reversed price range (Price low above Price high) is `invalid`: no price observation, no package, and a review item.
21. (0.2) `initiation_first_event` reads D5's "precedes round 1" as Round 0 in that process, which D1 gives every row before round 1 opens; the check covers process 1 only.
22. (0.2) `diff_workbooks.all_cash_for_stock` needs no change for v1.14.1: Part stock, with or without a range in the Note, already maps to No.

## 13. Versioning

The contract version is in every manifest (`contract_version`). Any change to a rule above, or a default chosen after Alex answers, is a new contract version with a dated entry here; the tool's `CONTRACT_VERSION` changes with it. Alex's answers (V114_SPEC §5, Decision 3 and 3b) decide the switches; until then the tool emits every variant.

- **0 (25 September 2026).** First version; tool 0.1.
- **0.1 (25 September 2026), tool 0.2.** Hardening after a review; no decision reopened and no switch given a default.
  - `package_basis` in `bids.csv` (§6), following E13's definition of the CVR/earnout value; review items for a maximum, an unstated or mixed basis and an unmarked value.
  - Partial-only parties are candidates for review, not removed from participation or the live counts (§3, §4).
  - `exit_inferred` in `participation.csv`; the censoring variant is "unresolved" where the Note does not resolve field-level Inferred (§9).
  - T2 requires two present, valid, equal prices (§7); an invalid price cell is a review item (§6).
  - `all_cash` through S7's crosswalk (§6).
  - `compare_alex.py` reports `ledger_package_basis` beside the aligned package.
  - After a second review, still 0.1 (same day, before any integration; every run in `analysis/` was regenerated with it): a named inferred field counts only where nothing in the row points to an inferred exit (§9, item 14); the CVR keywords are tighter and every basis read from the Note is a review item (§6, item 12); an invalid price cell gives no package (§6, item 15); a partial-only candidate with no exit row does not initiate the process (§8, item 16).

  On the analysis runs (see [analysis/README.md](analysis/README.md)): the compare-alex agreement counts are unchanged; the pilots' inferred exits (Mac-Gray #23, #50, #51; P&W #17, #57) move from "censored" to "unresolved" in the censoring variant and become review items; P&W #34's package (G&W, $21.02 + $1.13) is listed because its Note does not state the CVR's basis. After the second review the tables are byte-identical; two review items are added, Mac-Gray #42 and P&W #33, each a CVR valuation to confirm.

- **0.2 (26 September 2026), tool 0.3.** v1.14.1 (pipeline upgrade WP3) and P1. No switch has a default; three are retired for v1.14.1 only.
  - The rules selector `--rules v1.14|v1.14.1`, default v1.14.1 for a 29-column workbook; `rules_requested` and `switches_retired` in the manifest (§1, §8). `compare_alex.py` passes it through.
  - P1: `upfront_price_kind` in bids.csv; a row whose price is not available or invalid is no price observation under either variant; a reversed range is invalid (§6). Mac-Gray A #61/#62 (tool 0.2: both flags 1) now have both flags 0; nothing else in that run changes.
  - `same_offer_of` in bids.csv, a Same-offer row is not a `same_price_revision`, and the restatements switch (§6, §8).
  - v1.14.1: Inferred = Y on an exit is an inferred exit, with no Note reading (§9); Initiation by D5 with `initiation_check` in deal.csv, replacing the process-initiator switch (§8); no Uncertain auction status (§2); `not_admitted` and the eligible-but-unadmitted and merger-of-equals switches retired (§5, §8); `package_basis` from v1.14.1 E13 (§6); a Stock % range read from a Part stock Note (§6); a numeric Count range is a review item (§4).
  - Changed or added output fields: bids.csv `upfront_price_kind`, `same_offer_of`, `price_obs__same_price_as_new`, `price_obs__same_price_as_terms`, and for v1.14.1 `package_basis`, `stock_kind`, `stock_lo`, `stock_hi`; deal.csv `initiation_check`, and for v1.14.1 `initiation_first_event`, `initiation_first_row`, `auction_status`, `merger_of_equals_rows`; rounds.csv `not_admitted` (v1.14.1); participation.csv `exit_inferred`, `exit__inferred_as_censoring` (v1.14.1). Outputs made under 0.1 remain readable under 0.1.
