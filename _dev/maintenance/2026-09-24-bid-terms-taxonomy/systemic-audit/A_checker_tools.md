# Audit A: checker and standalone tools for v1.14

25 September 2026. Scope: `_dev/tools/check_lean.py` (1.6) and `test_check_lean.py`; `diff_workbooks.py`, `effort_sweep.py`, `findings_text.py`, `fetch_filing.py`, `make_seed.py`; `sandbox/run_model.py`; their tests; the checker paragraph in `_dev/tools/README.md`. Measured against `V114_SPEC.md` §1–§4, §7 and §9, and the 24 September draft instruction.

**Method.** **[ran]** means I executed it on copies in `/tmp/audit_A_checker/` with `PYTHONDONTWRITEBYTECODE=1`. **[read]** means I read the code at the cited lines. **Inferred** marks conclusions I did not execute. Nothing in the repository was edited except this file. I read the cockpit database only through a `mode=ro` URI. I sent no HTTP requests and started no model runs.

**Baselines [ran]:**
- Checker 1.6 reproduces every stored result exactly: the nine `extraction/` workbooks against their 22 September receipts (checker 1.5), and all seven cockpit run versions against their `check.json` (the two pilots were checked by 1.6, the other five by 1.5). The issue lists are identical.
- My slice's tests (80: `test_check_lean` 20, `test_run_model` 38, `test_fetch_filing` 10, `test_effort_sweep` 9, `test_review_helpers` 3) pass in a copy laid out like the repository.
- Unittest discovery over `_dev/tools` collects 199 tests, which matches §9.4. I collected them but did not run the full suite.

---

## 1. Claims

**Claim 1: CONFIRMED [ran, read].**
- `DEADLINE_OUTCOMES` (`check_lean.py:261-267`) contains `Late bids accepted` and not `Extended (late bid accepted)`.
- `check_rounds` (`:1297-1307`) raises `controlled.deadline_outcome` for any other value. It never consults `self.ledger_schema`.
- Test: I copied `_dev/cockpit/state/versions/mac-gray/opus55-medium-20260924-2241-d7d267/mac-gray.xlsx` to /tmp.
  - The unchanged copy gives `fail: 1 error(s), 16 warning(s)`, identical to its stored `check.json`. The one error is `round.opening_order`.
  - After changing Rounds G2 (P1 R1) from `Late bids accepted` to `Extended (late bid accepted)`:
    ```
    python3 check_lean.py --workbook wb/mg_pilot_ext.xlsx --filing filings/mac-gray_2013-12-04_DEFM14A.htm --output out/mg_ext.json
    fail: 2 error(s), 16 warning(s)
    error controlled.deadline_outcome Rounds 2 Deadline outcome Unallowed deadline outcome value(s): ['Extended (late bid accepted)'].
    ```
- The synthetic v1.14 fixture gives the same result.

**Claim 2: CONFIRMED, with a correction to the mechanism [ran, read].**
- How the diff works:
  - `diff_workbooks.py:17-21` turns each row into one tuple of cells.
  - `:45` matches rows with difflib on those whole tuples.
  - Cells are compared by position (`:47-54`, labelled with the *before* sheet's header) only when a replaced block has the same length on both sides.
- Across schemas the header and every data row differ, so no row ever matches:
  - `extraction/mac-gray.xlsx` (v1.13.2, 53 rows) against the Mac-Gray pilot (v1.14, 57 rows) gives `Deal ledger: 112 change(s)`. That is 54 "removed row" lines plus 58 "added row" lines: every row, header included, with no cell-level output.
  - With equal row counts, I rendered the pilot in v1.13.2 columns: same content, All cash derived from Stock %. The diff gives `Deal ledger: 846 change(s)`, reporting all 58 rows with misaligned labels, e.g. `row 1 -> 1, Note: was Note / now Financing`. The Note text shows up as appearing in `col 23`.
- So every row is reported, not "nearly every". Column misalignment is visible only when the row counts match; otherwise the output is whole-row removal and addition.

**Claim 3: CONFIRMED [read, ran].**
- `Bids received` appears only in `ROUND_COLUMNS` (`check_lean.py:115`) and in the required-cell loop (`:1224-1237`, `rounds.required`). No rule counts it against the ledger.
- D3's "count distinct bidder units" therefore needs no checker change.
- Do not add one. It would need bidder-unit arithmetic, which the checker disclaims (`:4-6`, `scope_note` `:1680-1683`).

**Claim 4: PARTLY [read].**
- `check_lean.py:633`: correct. The condition is at `:633`, the `"warning"` severity at `:635`, and the message runs to `:640`.
- `test_check_lean.py:510`: correct.
- `check_lean.py:922-930`: **off by two.** `exit.inferred_reason` is at `:924-932`; lines `:922-923` close the preceding `controlled.exit_reason` call.
- `:1526-1538`: correct for the enforcement (`facts.fields`, `:1525-1538`). The 17 fields themselves are `FACT_FIELDS` (`:131-149`), with label variants at `:150-169`.
- `worker.py:318-319`: correct.
  - `:319` stores only `{"errors", "warnings"}`, written to `versions.checker` at `:354-358`.
  - Read-only check: `mac-gray … '{"errors": 1, "warnings": 16}'`, with no version recorded.
- `data.py:984`: correct. It reports `checker_version` from the in-process check at `:738`.
- §0's `worker.py:50` and `:311` are also correct.

**Claim 5: REFUTED [ran, read].**
- Checker 1.6 never requires a price on any bid row. Its only price rules are:
  - `bid.price_type` (`:845-860`), which checks the type only when a cell is filled;
  - `bid.price_order` (`:861-870`);
  - `bid.one_sided_price` (`:887-898`), a warning when exactly one endpoint is filled.
- The draft's D2 says "The price may be undisclosed."
- Synthetic test: an Other-scope bid row with both prices blank passes under v1.14 and under v1.13.2.
- Real data: these Other-scope rows have both prices blank, and their workbooks reproduce their stored zero-error results:
  - `extraction/kraton.xlsx` #9, #10, #27, #56, #60;
  - Meredith, all 10 of its Other-scope rows;
  - Synacor #17, #30, #52, #58.
- So D18 needs only a new rule gated to v1.14 (A3), not an inverted one.
- D18's "Stock % stays required" already holds: a blank Stock % on an Other-scope row gives `controlled.stock_pct` [ran].

---

## 2. Findings

### 2.1 Every §3–§4 rule against checker 1.6

| Rule | What 1.6 does | Verdict | Change |
|---|---|---|---|
| D7: whole-company live counts; partial-only parties outside them | No live-count or auction arithmetic (`:4-6`). Auction screen: format only (`:1588-1605`). Whole-company bids: format only (`:1606-1616`). Count is required on Other-scope rows as on any bid row (`:821-843`); this is per row, not a live count. | Silent. **No count includes Other-scope rows.** | None |
| D10: no exit for a missed deadline | Nothing requires Did not submit for non-submitters. Exit rows only need an Exit reason (`:914-923`). | Silent | None |
| E6: count each stage once | Rounds consecutive (`:1151-1159`); exactly one Round opened per round (`:1160-1170`); none on round 0 or post (`:792-801`). | Agrees | None |
| E8: `round.opening_order` | Error (`:1171-1179`). It fires on the Mac-Gray pilot (Excel row 12). | Agrees | None. E8's fix is aimed at the model. |
| E10 and D13: same-price Bid rows | No rule on repeated prices. | Silent (compatible) | None |
| Bid reaffirmed gate | None. Fields are required as on any bid row (`:871-886`). | Silent | Optional (A12b) |
| D15: request with a revision is one row; a later request is Exclusivity changed | Exclusivity changed is a non-bid row, so every term column, Exclusivity included, must be blank (`:899-911`). | Agrees | Optional (A12a) |
| D16: Varies on cohort rows | `MARKER = {Y, Varies}` (`:228`, `:621-624`). Varies passes on cohort rows and is an error on Count = 1 (`:642-645`). | Agrees, except for a CVR value with Varies | A6 |
| §3 B: field-level Inferred | `ledger.inference_note` (`:953-961`) agrees. `exit.inferred_reason` (`:924-932`) contradicts it. | **Contradicts** | A4 |
| F.3 addition ("Not stated unless the filing reports one") | The same `exit.inferred_reason` rule. | **Contradicts** | A4 |
| H1: Financing Contingent requires Heavy | `conditions.financing_heavy` error (`:649-650`), on cohort rows too [ran]. | Agrees | None |
| Cohorts: Financing Varies with Conditions Unclear | Passes [ran]. | Agrees | None |
| D3: Concern does not force Heavy; None excludes Concern | `conditions.none_support` (`:651-658`); no Concern-to-Heavy rule. [ran] Concern passes with Light, Heavy and Unclear, and is an error with None. | Agrees | None. Do not add Concern → Heavy. |
| D4 and D14: CVR and exclusivity never change the level | No rule. [ran] CVR = Y with a value, plus Exclusivity Required, pass at None, Light, Heavy and Unclear. | Agrees | None (forbidden to add) |
| D11: Deadline outcome sets | One set with no schema branch (`:261-267`, `:1297-1307`). | **Contradicts** | A1 |
| D11: number of deadlines = number of outcomes | `rounds.deadline_count` (`:1287-1325`); No deadline stated paired with "none stated" (`:1277-1295`, `:1326-1334`). A superseded date has no Deadline row, so no outcome. | Agrees | None |
| D18: per-share cells blank on Other-scope rows | No rule. | Silent; needs a new rule | A3 |
| D18: Stock % stays required | `controlled.stock_pct` on every bid row (`:589-619`). | Agrees | None |
| Antitrust with an incompatible Regulatory value | Warning (`:633-640`). | Contradicts S1.1 | A2 |
| F.4: required fields | The controlled checks on bid rows (`:871-886`) cover exactly Stock %, Formality, Conditions, Due diligence, Financing, Regulatory and Exclusivity. | Agrees | None |
| D5 and D20: no new Deal facts field | Exactly 17 fields (`:1525-1538`); exactly four sheets (`:1638-1643`). | Agrees | Keep strict; see A10 for S3 downloads. |
| E3 and E4: exact counts only when supported | Count, or a "Count: …" Note giving a bound, estimate or unknown (`:802-843`). | Agrees | None |
| Part F: mandatory map and deadline Questions | Warnings (`:1501-1516`). | Agrees with the draft's Part F, which D12 keeps | None, unless A1 drops "Always include" |
| D2: Bidder interest with a price is a Bid | Prices on non-bid rows are errors (`:899-911`). | Agrees | None |

The review list in §7 S1 therefore produces exactly one change: `exit.inferred_reason` (A4). The checker has no Did not submit rule and no live-count rule. Its count rules (E3) and its Round opened ordering rule (E6, E8) agree with the candidate as specified. It has no rule on same-price Bid rows (E10).

### 2.2 Findings

**A1. Deadline outcome sets by schema, with a legacy warning.**
- **File:** `check_lean.py:261-267`, `:1297-1307`.
- **Now [ran]:** `Extended (late bid accepted)` is an error in every workbook (claim 1).
- **v1.14 needs:**
  - the v1.14 set, plus `No deadline stated`, handled as now;
  - `Late bids accepted` as a warning in v1.14 workbooks;
  - v1.13.2 unchanged.
- **Change:**
  - Keep `DEADLINE_OUTCOMES` as the v1.13.2 set (see A5).
  - Add `DEADLINE_OUTCOMES_V114 = {"Enforced", "Extended", "Extended (late bid accepted)", "Passed without action", "Unclear"}`.
  - At `:1298`, choose the set by `self.ledger_schema`.
  - In v1.14, raise a warning (`rounds.deadline_outcome_legacy`: "renamed 'Extended (late bid accepted)' in the v1.14 candidate (E9)") and still count the value for `rounds.deadline_count`.
- **Prototype [ran]:**
  - The nine `extraction/` workbooks and the five v1.13.2 run versions are identical to stored.
  - Each pilot gains exactly 2 legacy warnings.
  - `Extended (late bid accepted)` passes under v1.14 and is still an error under v1.13.2.
- **Severity:** release blocker.
- **Spec:** §7 S1.3.

**A2. Antitrust with an incompatible Regulatory value becomes an error.**
- **File:** `check_lean.py:634-635`.
- **Now [ran]:** a warning.
- **Change:** set the severity to `"error"` and keep the code and message. No gate is needed: `check_bid_terms` runs only for v1.14 (`:885-886`), and neither pilot has a case.
- **Prototype [ran]:** only `test_check_lean.py:510` fails.
- **Severity:** needed for v1.14.
- **Spec:** §7 S1.1.

**A3. Other-scope bid rows keep their per-share cells blank.**
- **File:** `check_lean.py`, `check_bid_terms` (`:583-666`).
- **Now [ran]:** no rule (claim 5).
- **Change:** in `check_bid_terms`, which runs for v1.14 only, add an error when the row's Event is `Other-scope bid` and Price low, Price high or CVR/earnout value is filled. Suggested code `bid.other_scope_per_share`, citing D1 and F.4.
- **Prototype [ran]:**
  - A v1.14 Other-scope row with a price or a CVR value is an error; blank passes.
  - v1.13.2 Synacor #54 and #59 (price 2, 2) stay clean.
  - No stored result changes.
- **Severity:** needed for v1.14.
- **Spec:** §7 S1.2.

**A4. `exit.inferred_reason` must not apply to v1.14 workbooks.**
- **File:** `check_lean.py:924-932`.
- **Now [ran]:** the rule warns whenever Inferred = Y and the Exit reason is not "Not stated". In the Mac-Gray pilot it fires on #50 (Party A, "Lower offer than rivals") and #51 (Party B, "Terms or process"). Both are inferred exclusivity displacements whose reasons are quoted from the filing (p. 37).
- **v1.14:** two changes each make this legitimate:
  - Under §3 B, Inferred = Y may mark only a field.
  - The F.3 addition allows a reported reason on an inferred exit.
- The checker cannot tell "a reported exit with an inferred date" from "an inferred exit with a reported reason". The only implementable form of the §7 S1 request is not to run the rule on v1.14 workbooks.
- **Change:** `elif not v114 and record["Inferred"] == "Y" and exit_reason != "Not stated":`.
- **Prototype [ran]:**
  - v1.13.2 results are unchanged, and `test_check_lean.py:341` still passes.
  - The Mac-Gray pilot loses its 2 `exit.inferred_reason` warnings.
- **Severity:** needed for v1.14.
- **Spec:** §7 S1 names the problem but not this answer.

**A5. Other modules import the checker's constants.**
- **File:** `cockpit/workspace.py:353`, which uses `sorted(check_lean.DEADLINE_OUTCOMES)`; also `:350-356`, which use `ALL_CASH`, `MARKER` and `CONDITION_COLUMNS`.
- **Now [read]:** the cockpit takes one choice list per field from the checker.
- **Change:**
  - S1 must keep `DEADLINE_OUTCOMES` (and `ALL_CASH`) under their names.
  - S1 must export the v1.14 set, either as `DEADLINE_OUTCOMES_V114` or through a helper `deadline_outcomes(schema)`, so that S2 can build choices by `ledger_schema`.
  - Renaming the constant would, by inference, raise AttributeError in every deal payload.
  - Until S2 ships, a v1.14 working copy is offered only `Late bids accepted` (inferred).
- **Severity:** needed for v1.14; a release blocker if the constant is renamed. Ship S1 and S2 together.
- **Spec:** §7 S2 covers the choices, but not this coupling.

**A6. A CVR/earnout value on a `Varies` row.**
- **File:** `check_lean.py:630-631` (`bid.cvr_value_marker`).
- **Now [ran]:** on a cohort row with CVR/earnout = Varies, a filled CVR/earnout value is an error. The rule demands exactly Y.
- **v1.14:** §3 D1 lets the markers be Varies, but no text says whether the value may accompany Varies. §9.1 requires the instruction and the checker to agree.
- **Change:** no checker change. A1 should add to D1 item 12 and E13: "Filled only where CVR/earnout is Y; on a Varies row the amounts go in the Note."
  - This matches TAXONOMY_DRAFT5 §1 and §4, and D16's "the split goes in the Note".
  - A per-share value on a row where only some members carry it would mislead analysis.
- **Severity:** needed for v1.14 (consistency).
- **Spec:** no.

**A7. Record the checker version wherever results are stored.**
- **Files:**
  - `worker.py:319`;
  - `effort_sweep.py:213` (the receipt's `check_summary` is `report["summary"]` only);
  - `findings_text.py:19` (header line: no version or schema).
- **Now [read]:** only the full `check.json` records `checker_version` and `ledger_schema`.
- **Change:**
  - Add `checker_version` and `ledger_schema` to the worker's summary (spec) and to the sweep receipt.
  - Add a first line to the findings, e.g. "Checker 1.7; v1.14 ledger rules", so that a revision pass sees which rule set applied.
- **Severity:**
  - worker: needed (spec);
  - sweep receipt and findings: nice to have.
- **Spec:** §7 S1 covers the worker only.

**A8. `diff_workbooks.py` cannot compare across schemas.**
- **File:** `diff_workbooks.py:17-54`.
- **Now [ran]:** see claim 2.
- **v1.14 needs:** at gate 5, reviewers compare v1.14 runs with v1.13.2 reviewed working copies.
- **Change:** see §2.4.
- **Severity:** needed for v1.14 review.
- **Spec:** no. §10 and §7 S2 cover only the cockpit's `_diff` (`workspace.py:497`, confirmed [read]).

**A9. `effort_sweep.py` cannot run a candidate instruction or the held-out deals.**
- **Files:**
  - the instruction is fixed at `effort_sweep.py:37`, pinned at `:114` and enforced by `cell_mismatches` (`:148-153`);
  - `prepare` passes no `--instruction` (`:275-277`);
  - deals come only from `raw_filing/MANIFEST.csv` (`:64-66`, `:211`), so the four added deals are excluded (Medivation, Zep, Pepco, Imprivata; their filings are in `_dev/cockpit/state/filings/`).
- **Metric problems [read, inferred]:**
  - `ledger_stats` counts every `BID_EVENTS` row as a bid (`:326`), Other-scope rows included.
  - It keys bids on `Price low|Price high|Date from` (`:332`). Under D18, Other-scope rows in v1.14 become `None|None|date`, so replicate agreement mixes whole-company and partial rows.
- **Change:**
  - `plan --instruction <file>` recorded in `plan.json`, pinned by hash and passed to `prepare`;
  - `--filing-dir` support for added deals;
  - put Event in the bid key, and report whole-company Bid rows separately from Other-scope rows.
  - `test_effort_sweep.py:208-209` keeps its values, since its fixture has only Bid rows.
- **Severity:** nice to have. Blind v1.14 runs go through the cockpit, which passes `--instruction`.
- **Spec:** no.

**A10. `run_model.py` revision mode has no schema or sheet guard.**
- **Files:**
  - the default instruction is the frozen v1.13.2 text (`:264`);
  - the revision prompt (`:290-300`) says the workbook was "made by following" the supplied instruction;
  - `prepare` does not inspect the `--revise-from` workbook (`:247-252`);
  - completion requires exactly four sheets (`:445`, `:663`, `:682-683`).
- **Risks [read, inferred]:**
  - Revising a v1.14 workbook without `--instruction` silently runs it under v1.13.2.
  - Revising a v1.13.2 workbook under the candidate cannot migrate it, since the prompt forbids changes no finding points to.
  - An S3 working-copy download (five sheets) given as `--revise-from` ends as `workbook_incomplete` after a paid run.
  - [ran] The checker gives the same five-sheet download `schema.sheets` (error).
- **Change, in `prepare`:**
  - refuse a `--revise-from` workbook whose sheets are not exactly `SHEETS`;
  - record `revised_from_ledger_schema` (a `Stock %` header means v1.14);
  - require an explicit `--instruction` when that schema is v1.14.
- Keep the checker's four-sheet rule strict. A model-written `Source` sheet must fail (D20).
- **Severity:** nice to have; needed if revision mode is used during v1.14.
- **Spec:** no.

**A11. `run_model.py` metadata names the instruction only by hash.**
- **File:** `run_model.py:302-322`.
- **Now [read]:** `instruction_name` is always the fixed file name, and a candidate is identified only by `instruction_sha256`.
- **Change:** add `instruction_source` (the path given to `--instruction`, or "working instruction").
- **Severity:** nice to have.
- **Spec:** no.

**A12. Optional mechanical checks for v1.14 (warnings, v1.14 only).**
- These are general, never assign a level, and are neither listed nor forbidden by the spec.
- Hit counts [ran] are over the nine `extraction/` workbooks and all seven run versions:
  - **a. D15 duplicate.** An Exclusivity changed row with the same Who and Sort date as a Bid or Bid reaffirmed row whose Exclusivity is Requested or Required. **2 hits**, both in the Mac-Gray pilot (#31/#32 and #39/#40, made under TAXONOMY_DRAFT5:40, which D15 reverses). v1.13.2 workbooks have no Exclusivity column.
  - **b. Bid reaffirmed carries Formality = Formal and a Flag.** E10 says this in both v1.13.2 (`:203`) and the draft (`:210`). **0 hits** in six rows.
  - **c. Each `Extended` outcome has a later Deadline set or Deadline revised row in its round.** This is D11's "a later due date was set". **0 hits** in six rounds.
  - **d. An exit followed by bid, NDA or group activity of the same Who in the same process, with no Re-entered between** (E14). **0 hits**. It matches Who exactly, so it catches only an obvious omission.
  - **e. An Other-scope bid row with a blank Note** (D18 puts the amount there). Not measured; trivial.
- If adopted, each pilot delta must be documented; (a) adds 2 warnings to Mac-Gray.
- **Considered and rejected:**
  - checking Bids received against the ledger (claim 3);
  - Light with Due diligence Not begun (Light's routes need judgment);
  - Heavy with a Note that names no H-trigger (only if A1 makes naming mandatory);
  - Conditions ≠ Unclear while a component is Varies (members can share a level across Varies);
  - anything tying Concern, CVR or Exclusivity to the level (D3, D4, D14).
- **Severity:** nice to have.
- **Spec:** no.

**A13. Stale wording in the checker and the README.**
- **Files:**
  - `check_lean.py:2`, `:9`, `:39-44` (`CHECKER_REVISION`) and `:73` say "v1.14 (draft)";
  - `README.md:19` says "(draft)", lists "an inferred exit's reason" as a general cross-check, and names only two E12 rules;
  - `README.md:158` says findings include "optional model judgments", but `findings_text.py` emits none.
- **Change:** 1.7 text should say:
  - v1.14 candidate rules, chosen by the `Stock %` header;
  - Antitrust error; Other-scope per-share blanks; Deadline outcome sets by schema, with the legacy warning;
  - `exit.inferred_reason` for v1.13.2 only;
  - the checker version in stored summaries;
  - "not deployed" until Austin deploys.
- **Severity:** needed.
- **Spec:** §7 S1 and S6.

**A14. The EDGAR index-link derivation is duplicated.**
- **Files:** `fetch_filing.py:237` and `cockpit/deals.py:240`, both `source_url[:-4] + "-index.htm"`.
- **v1.14 needs:** S3 must derive the index link for the nine seed deals ("never guess a URL").
- **Change:** add an `index_link(submission_url)` helper beside `submission_link()` (`:75-92`), validated with `SUBMISSION_LINK` and covered by a test. Use it in all three places.
- **Severity:** nice to have.
- **Spec:** §7 S3 needs the derivation but not the helper.

**A15. Checker messages reach revision passes word for word.**
- **Files:** `check_lean.py:645`, `:650`, `:957`, relayed by `findings_text.py:27`.
- **Change, for v1.14:**
  - `bid.varies_single`: say "Varies is for cohort rows, including partial reporting (D16)";
  - `conditions.financing_heavy`: name H1;
  - `ledger.inference_note`: add "or names the inferred field" (§3 B).
- **Severity:** nice to have.
- **Spec:** no.

**No change needed [read]:**
- `make_seed.py` reads identifying columns only and is independent of the schema.
- `fetch_filing.py`, apart from A14.
- `run_model.py`'s extraction prompt (`:281-285`), which is schema-neutral.
- Its four-sheet validation, which D20 requires.

### 2.3 Tests whose assertions change in 1.7

| Test | Now | In 1.7 |
|---|---|---|
| `test_check_lean.py:510` | Expects `conditions.antitrust_regulatory` as a warning | **Must change** to an error (A2). Confirmed: it is the only existing test that fails on the prototype. |
| `test_check_lean.py:320-341` (`:341`) | Expects the `exit.inferred_reason` warning on the v1.13.2 fixture | Unchanged if A4 is gated (prototype passes). Add a v1.14 twin that asserts no flag. |
| `test_check_lean.py:509` | Exclusivity Varies on a one-bidder row is an error | Unchanged. It contradicts §9.2's first bullet as written (§3 below). |
| `test_check_lean.py:506` | A CVR value with a blank marker is an error | Unchanged (A6). Add a Varies-with-value case once A1 decides. |
| `test_check_lean.py:487-494` | `ledger_schema == "v1.14"` | Unchanged unless the label changes. |
| `test_check_lean.py:496-538` | v1.14 lists and consistency rules | Extend with the §9.2 cases: Other-scope rows, deadline sets and legacy warning, Antitrust error, cohort Financing Varies. |
| `test_review_helpers.py:17-47` | Positional output format: number to text; an added trailing column shown as `New field [text]` | Changes if A8 changes the output format. Keep the type display. |
| `test_effort_sweep.py:208-209` | Replicate Jaccard on Bid-only fixtures | Unchanged by A9's key change. |
| Cockpit tests (outside this slice) | Choice lists from `DEADLINE_OUTCOMES` | Break only if A5's name is changed. |

### 2.4 Cross-schema comparison tooling (A8, proposal)

Extend `diff_workbooks.py` (openpyxl and difflib only):
1. **Align columns by header.** Report columns present in only one workbook once per sheet, then compare shared columns by name.
2. **Match rows by a key, not whole tuples:**
   - Deal ledger: (Event, Who, Sort date), with an optional second pass matching the quoted passage;
   - Rounds: (Process, Round);
   - Questions: Q;
   - Deal facts: Field.

   Unmatched rows are listed as added or removed. [ran] A prototype on the equal-content pair reports 0 changes, against 846. On the real v1.13.2-run versus v1.14-run pair it matches 38 rows and lists 15 removed and 19 added.
3. **Skip a `Source` sheet by default** (S3 downloads), with `--include-source` to show it.
4. **A `--crosswalk` mode** labels differences that come from the schema:
   - **All cash and Stock %:** Yes ↔ 0; No ↔ a number above 0, a range or Part stock; Not stated ↔ Not stated. v1.14 `Varies` has no v1.13.2 equivalent.
   - **Price basis (E13):** a v1.13.2 price may include a CVR in the package. Show the v1.14 price together with its CVR/earnout value where CVR = Y, labelled "E13 basis", not equated.
   - **Other-scope rows:** suppress price differences where v1.14 is blank, labelled "D18".
   - **Deadline outcome:** `Late bids accepted` ↔ `Extended (late bid accepted)`, labelled "D11 (wider)". The meanings differ, so show both.
   - **New condition columns:** "added in v1.14", with no comparison. Conditions is compared but flagged "E12 rules changed" (D14: exclusivity no longer contributes to Heavy).
5. **Event-count summary before and after:** Bid, Bid reaffirmed, Other-scope bid, Exclusivity changed, Did not submit, Re-entered and Round opened. Reviewers see the effects of D13, D15, D10, D7 and E6 at a glance.

The v1.13.2 side is the cockpit's working-copy download. After S3 that download has five sheets; item 3 handles it.

---

## 3. Errors in V114_SPEC (this slice)

1. **§7 S1, `check_lean.py:922-930`:** the rule is at `:924-932`.
2. **§7 S1, "The pilots may show only the documented new warnings", and §9.2, "the stored run results all reproduce":** S1's own `exit.inferred_reason` review removes warnings as well. The prototype shows two deltas:
   - Mac-Gray pilot: +2 `rounds.deadline_outcome_legacy`, −2 `exit.inferred_reason`;
   - P&W pilot: +2 legacy warnings.

   Reword to "documented changes", and except the pilots from "reproduce".
3. **§9.2, first bullet, "any Exclusivity value … adds no issue":** Exclusivity `Varies` on a one-bidder row is an error under the existing and correct `bid.varies_single` (`check_lean.py:642-645`; asserted at `test_check_lean.py:509`). Reword to "any Exclusivity value valid for the row (Varies only on a cohort row)".
4. **§7 S1, "a reported exit with an inferred date must not be flagged", and §9.2, "(if S1 changes it)":** the checker cannot tell that case from an inferred exit with a reported reason, which the new F.3 clause also allows. The change is firm: skip the rule on v1.14 workbooks (A4).
5. **§7 S1.3 is incomplete:** `DEADLINE_OUTCOMES` is imported by `cockpit/workspace.py:353`. S1 must keep that name for the v1.13.2 set and export the v1.14 set for S2 (A5).
6. **§7 S1.4, "Confirm":** confirmed (`MARKER`, `:228`, `:621-624`), with two interactions the spec does not state:
   - Varies is an error on a one-bidder row;
   - a CVR/earnout value requires exactly Y (`:630`).

   The second needs a sentence in A1 (A6).
7. **§10 and §7, "the cross-schema diff gap":** it is fixed only for the cockpit's `_diff` (S2). `diff_workbooks.py`, the review helper the README advertises, has the same gap and is not in §7 (A8).
8. **§7 S1 review list, "the Did not submit and live-count rules (E14, E1)":** the checker has neither kind of rule. The review's result is "no change"; only `exit.inferred_reason` changes (§2.1).
9. **§7 S1, last bullet:** the stored summary also lacks the version in `effort_sweep.py:213` receipts (A7, minor).

These §7 and §9 statements checked out:
- S1.2: Synacor #54 and #59 carry prices 2 and 2.
- S1.3: both pilots use `Late bids accepted` on two Rounds lines each.
- The 17-field rule.
- The `worker.py` and `data.py` citations.
- §9.2's Concern, Contingent and cohort statements [ran].
- §9.4's 199 tests (collected).

Scratch folder `/tmp/audit_A_checker/` deleted after the run.
