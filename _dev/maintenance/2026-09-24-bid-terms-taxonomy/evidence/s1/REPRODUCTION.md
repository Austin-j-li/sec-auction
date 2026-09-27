# S1: checker 1.7, reproduction and rule review

25 September 2026. Package S1 of `V114_SPEC.md` §7.3. The code is in the S1 sandbox (`/home/uctpiaj/work/tmp/v114-scratch/pkg/s1/_dev/tools/check_lean.py`, SHA-256 `41ea880f504d96d0e9936bb8db0fef5391c4e5ab4d09f1f069ef691c3127c49c`), not in the live checkout. The live services still run checker 1.6. Nothing here was deployed, and no stored `check.json` was rewritten.

Files in this folder:
- `REPRODUCTION.md`: this note.
- `reproduction.json`: for each of the 16 workbooks, the stored summary, the 1.6 and 1.7 summaries, and the issue deltas (1.7 against stored, and 1.7 against 1.6).
- `reproduce.py`: the script that produced it. It ran in `/home/uctpiaj/work/tmp/v114-scratch/tmp/s1/repro/`, on copies of the inputs.

Wave 2 replaced `reproduce.py` and added files; see §5. The wave-1 script is still at `/home/uctpiaj/work/tmp/v114-scratch/tmp/s1/repro/reproduce.py`.

## 1. What 1.7 changes

All of the new rules apply only when the Deal ledger header has `Stock %` (`schema_for_header`). v1.13.2 workbooks are checked exactly as in 1.6.

| § 7.3 | Change | Code | Severity |
|---|---|---|---|
| 1 | Deadline outcome set chosen by `self.ledger_schema` through `deadline_outcomes(schema)`. v1.14 accepts `Extended (late bid accepted)`. In v1.14, `Late bids accepted` is accepted, still counts toward `rounds.deadline_count`, and gives a warning. v1.13.2 keeps its set, so there `Extended (late bid accepted)` is still `controlled.deadline_outcome`. | `rounds.deadline_outcome_legacy`: "'Late bids accepted' is replaced in v1.14 by the wider 'Extended (late bid accepted)' (E9)." | warning |
| 2 | Antitrust with a Regulatory value other than No concern, Concern or Varies | `conditions.antitrust_regulatory` (code and message unchanged) | warning → **error** |
| 3 | An Other-scope bid row with Price low, Price high or CVR/earnout value filled. One issue per filled cell. | `bid.other_scope_per_share` | error |
| 4 | `exit.inferred_reason` no longer runs on v1.14 workbooks. | — | — |
| 5 | Varies. The markers already accept `Y`/`Varies` (`MARKER`). `bid.varies_single` and `bid.cvr_value_marker` are kept. | — | — |
| 6 | Four review warnings (v1.14 only; see below) | see below | warning |
| 7 | Messages. `bid.varies_single` now mentions partial reporting. `conditions.financing_heavy` names H1. In v1.14 only, `ledger.inference_note` adds "or naming the inferred field". The first two rules already run only on v1.14 workbooks. The third runs on both schemas, so its new wording is gated by schema, and the v1.13.2 message is unchanged. | — | — |
| 8 | `CHECKER_VERSION = "1.7"` and a new `CHECKER_REVISION`. The "v1.14 (draft)" wording is gone from the revision text and the `LEDGER_COLUMNS_V114` comment. The checker paragraph of `_dev/tools/README.md` (line 19) is rewritten and says 1.7 is not deployed until the v1.14 deploy. | — | — |
| 9 | `ledger_schema(path)`, `schema_for_header(header)`, `deadline_outcomes(schema)` and `choice_lists(schema)`. The seam's names and signatures are kept. `DEADLINE_OUTCOMES` keeps its name and its v1.13.2 value. `workspace.py` imports it. | — | — |

**The four review warnings** follow the codes' existing `area.detail` style:

| Code | Fires when | Anchor |
|---|---|---|
| `ledger.exclusivity_duplicate` | An Exclusivity changed row has the same Who (after whitespace normalization) and Sort date as a Bid or Bid reaffirmed row whose Exclusivity is Requested or Required. Message: "…if this row repeats the bid's own request, remove it (E10); a grant, execution or extension is its own event." | The Exclusivity changed row, column Event |
| `rounds.extended_without_new_date` | An `Extended` outcome has no Deadline set or Deadline revised row in its round with a Sort date on or after its own Deadline row. Outcomes are paired with the round's Deadline rows in ledger order. The check runs only when the two counts agree; otherwise `rounds.deadline_count` already reports the round. | Rounds row, column Deadline outcome |
| `exit.activity_without_reentry` | An exit row is followed, in the same Process, by a Bid, Bid reaffirmed, NDA signed or Bidding group changed row with the same Who, and no Re-entered row for that Who comes between them. Other-scope bid rows do not count. The warning fires once per exit, on the first such row. | The later row, column Event |
| `bid.other_scope_note` | An Other-scope bid row has a blank Note. | Note |

**Not added**, as §7.3 requires:
- Concern → Heavy;
- any rule linking CVR or Exclusivity to the Conditions level;
- a Deal facts allowance (the 17-field rule is unchanged);
- a Bids received count, or any bidder-unit arithmetic;
- a rule tying Light to Due diligence, or requiring a Heavy Note to name its trigger;
- audit A12(b) ("Bid reaffirmed carries Formal and a Flag"), which §8 rejects.

## 2. Reproduction

**Inputs.** All were copied into the temp dir. None was read in place and changed.
- The nine `extraction/*.xlsx` workbooks. Their stored results are `_dev/reviews/2026-09-22-opus55-reextraction/receipts/<deal>/check.json`, from checker 1.5.
- Seven cockpit run versions from `_dev/cockpit/state/versions/<deal>/<id>/`, each workbook with its `check.json`:
  - five v1.13.2 runs, checked by 1.5;
  - the two v1.14-draft pilots, checked by 1.6.
- Each filing named in the version's `metadata.json`, from `raw_filing/` or `_dev/cockpit/state/filings/`. Every filing matched the SHA-256 in its metadata.

**Method.** `reproduce.py` loads checker 1.6 from the wave-1 base (`wave1-base/_dev/tools/check_lean.py`, SHA-256 `f5e2e4cf…`) and 1.7 from the S1 sandbox, and runs both in-process on each workbook. For each checker it compares against the stored `check.json`:
- the issue lists, as multisets of (severity, code, sheet, row, column, message);
- `summary`;
- `status`.

It ignores `checker_version`, `checker_revision`, `ledger_schema`, `workbook`, `filing` and `basis`.

**Results.**

| Workbook | Schema | Stored (checker) | 1.6 = stored | 1.7 = stored | 1.7 delta |
|---|---|---|---|---|---|
| extraction/datalink | v1.13.2 | 0 e / 21 w (1.5) | yes | yes | none |
| extraction/kraton | v1.13.2 | 0 / 20 (1.5) | yes | yes | none |
| extraction/mac-gray | v1.13.2 | 1 / 26 (1.5) | yes | yes | none |
| extraction/meredith | v1.13.2 | 0 / 16 (1.5) | yes | yes | none |
| extraction/penford | v1.13.2 | 0 / 15 (1.5) | yes | yes | none |
| extraction/petsmart | v1.13.2 | 1 / 22 (1.5) | yes | yes | none |
| extraction/providence-worcester | v1.13.2 | 0 / 12 (1.5) | yes | yes | none |
| extraction/stec | v1.13.2 | 0 / 21 (1.5) | yes | yes | none |
| extraction/synacor | v1.13.2 | 1 / 8 (1.5) | yes | yes | none |
| imprivata/opus55-xhigh-20260924-1651-fe7897 | v1.13.2 | 0 / 22 (1.5) | yes | yes | none |
| medivation/opus55-medium-20260923-1631-9dd02c | v1.13.2 | 0 / 3 (1.5) | yes | yes | none |
| pepco-holdings/opus55-medium-20260924-0943-b762af | v1.13.2 | 2 / 27 (1.5) | yes | yes | none |
| petsmart/opus55-medium-20260923-1528-4d8363 | v1.13.2 | 1 / 6 (1.5) | yes | yes | none |
| zep/opus55-xhigh-20260924-0926-ee06ac | v1.13.2 | 0 / 21 (1.5) | yes | yes | none |
| **mac-gray/opus55-medium-20260924-2241-d7d267** (pilot) | v1.14 | 1 / 16 (1.6) | yes | no, as documented | 1 / 18: +2 legacy, +2 D15 duplicate, −2 inferred reason |
| **providence-worcester/opus55-medium-20260924-2241-38bc24** (pilot) | v1.14 | 0 / 14 (1.6) | yes | no, as documented | 0 / 16: +2 legacy |

The pilots' deltas are exactly the ones §7.3 documents.
- **Mac-Gray pilot:**
  - `+ rounds.deadline_outcome_legacy` on Rounds rows 2 and 3 (P1 R1 and P1 R2);
  - `+ ledger.exclusivity_duplicate` on Excel rows 33 and 41, which are #32 (paired with #31) and #40 (paired with #39);
  - `− exit.inferred_reason` on Excel rows 51 and 52, which are #50 (Party A) and #51 (Party B).
  - The one error, `round.opening_order`, stays.
- **P&W pilot:** `+ rounds.deadline_outcome_legacy` on Rounds rows 2 and 3.
- The other three review warnings add nothing to either pilot.

`ledger_schema(path)` agrees with the checker's own `ledger_schema` on all 16 workbooks.

**The review warnings on the v1.13.2 workbooks, for diagnosis only.** 1.7 does not run the review warnings on v1.13.2 workbooks. To check that their conditions are not noisy, I applied the same conditions to all 16 workbooks as if they were v1.14 (script `diagnose.py`, temp dir only):
- `ledger.exclusivity_duplicate`: the 2 Mac-Gray pilot hits only. v1.13.2 workbooks have no Exclusivity column.
- `rounds.extended_without_new_date`: 0 hits. Six rounds use `Extended`: Kraton P1R1, Meredith P1R3, PetSmart P1R2 (twice), sTec P1R2 and Medivation P1R2. Each has a Deadline revised or Deadline set row on or after the Extended deadline. In Medivation (#25/#26) and the PetSmart run (#34/#36), the Deadline revised row has the same Sort date as the Deadline row. So the check compares Sort dates ("on or after") rather than ledger position after the Deadline row: both readings pass here, and the date reading is less likely to flag a same-day revision placed before its Deadline row.
- `exit.activity_without_reentry`: 0 hits. The P&W pilot's Party D and Party E exits (#37, #38) are followed by Re-entered rows (#40, #41).
- `bid.other_scope_note`: 0 hits in 21 Other-scope rows (Kraton 5, Meredith 10, Synacor 6).
- The new `bid.other_scope_per_share` would flag only v1.13.2 Synacor #54 and #59 (price 2, 2), as the spec says. Gating it to v1.14 keeps them clean.

None of the review warnings needed narrowing.

## 3. Review of the existing rules against the candidate (§7.3)

The A1 candidate was not yet in this folder when S1 finished. So this review is against spec §3–§4, D1–D27 and the 24 September draft lines those sections cite, as the brief directs. **Re-run it once R's fixes to the candidate land.** Audit A §2.1 made the first pass on checker 1.6. This pass checks 1.7.

| Spec rule | What 1.7 does | Verdict |
|---|---|---|
| B: four kinds of value; Inferred marks an event or a field | `ledger.inference_note` requires a Note on an Inferred row. The v1.14 message adds "or naming the inferred field". | Agrees |
| B, F.3: an inferred exit may carry a reported reason | `exit.inferred_reason` is skipped on v1.14 (change 4) | Agrees |
| B: evidence applies at its own date; express incorporation | No rule | Silent (compatible) |
| D1: one list of bid rows (Bid, Bid reaffirmed, Other-scope bid) | `BID_EVENTS`. All bid-row fields are required on all three. | Agrees |
| D1, D18: Other-scope rows leave the per-share cells blank | `bid.other_scope_per_share` (change 3). Stock % stays required (`controlled.stock_pct`). | Agrees |
| D1, D16: CVR/earnout and Antitrust take Y, Varies or blank | `MARKER` | Agrees |
| D1: CVR/earnout value only where CVR/earnout is Y; on Varies the amounts go in the Note | `bid.cvr_value_marker` requires exactly Y | Agrees, once A1 adds the sentence (audit A6) |
| D2: a Bidder interest with a price is a Bid | Prices on non-bid rows are errors (`bid.fields_on_nonbid`) | Agrees |
| D2, D10, E14: Did not submit only where participation ends; no exit for a continuing bidder | No Did not submit arithmetic. `exit.activity_without_reentry` flags an exit followed by activity. | Agrees; review warning only |
| D2, D15: a request made in the bid's own communication is coded on that bid row | Exclusivity changed is a non-bid row, so its term cells must be blank. `ledger.exclusivity_duplicate` flags the old two-row pattern. | Agrees |
| D3: Deadline outcome values | `DEADLINE_OUTCOMES_V114` plus `No deadline stated` pairing (change 1) | Agrees. The one intended difference (§9.1): `Late bids accepted` is still accepted, with a warning. |
| D3: Bids received counts distinct whole-company units | Required non-blank only | Silent. No count is added (do-not-add list). |
| D4, F: seven Question columns; Part F's map and deadline Questions | `QUESTION_COLUMNS`; `questions.process_round_map` and `questions.deadline_outcomes` warnings | Agrees (D12 keeps Part F's rule) |
| F.4: required bid fields | Stock %, Formality, Conditions and the four condition columns on every bid row | Agrees |
| D5, D20: no new Deal facts field | Exactly 17 fields, four sheets | Agrees; kept strict |
| D5: Acquirer type values | `TYPES` (Strategic, Financial, Mixed, Unknown), prefix match | Agrees if A1 lists these four values (audit C §4) |
| E1, D7: whole-company counts; partial-only parties outside them | No live-count or auction arithmetic. Count is per row. | Silent (compatible) |
| E3, E4: exact counts only when supported | `ledger.count_bidder` / `ledger.count_uncertain` | Agrees |
| E5: processes | Consecutive from 1 | Agrees |
| E6, D8: count a stage once; an unannounced round is inferred | One Round opened per numbered round; none on round 0 or post; the Inferred row needs a Note | Agrees |
| E8: Round opened is the first row of its round | `round.opening_order` | Agrees |
| E9, D11 | `rounds.deadline_count`; a superseded date has no Deadline row. `rounds.extended_without_new_date` is a review warning for "a later due date was set". | Agrees |
| E10, D13: same-price commitment revisions are Bid rows | No rule on repeated prices | Silent (compatible) |
| E11, D9: Formality | Value list only | Agrees |
| E12 H1: Contingent requires Heavy | `conditions.financing_heavy`; the message now names H1 | Agrees |
| E12, D3: Concern never forces Heavy; None excludes Concern | `conditions.none_support`; no Concern → Heavy rule | Agrees |
| E12, D4, D14: CVR and exclusivity never change the level | No rule. A test adds CVR Y with a value, and each Exclusivity value, at every level: no issue. | Agrees |
| E12: Antitrust qualifies a Regulatory value | `conditions.antitrust_regulatory`, now an error (change 2) | Agrees |
| E12 cohorts, D16: Varies | `bid.varies_single` on Count = 1; a cohort with Financing Varies and Conditions Unclear passes | Agrees |
| E12: Light's two routes; Heavy names H1–H3 | No rule tying Light to diligence; no Note-trigger rule | Agrees (do-not-add list) |
| E13: Stock % values; "a package that cannot be split leaves the price cells blank" | `controlled.stock_pct`; no price is ever required | Agrees |

**Two existing rules to recheck after R.** Neither is changed here.
- `conditions.level_unsupported` (1.6, v1.14 only). It warns when Due diligence, Financing and Regulatory are all Not stated but Conditions is None, Light or Heavy, and says "the Note must name the condition that supports the level (E12)".
  - It is not the forbidden "a Heavy Note must name its trigger" rule. It never checks the Note, and it is a warning.
  - It does match the draft's "Begin a bid row's Note with the fact driving its level". If A1 drops that sentence, R should say whether the message still fits.
- `controlled.stock_pct` (v1.14 only). Its message gives "a stated range such as '50-75'". §3 treats "50–75" as Pepco's figure, and the candidate must replace it in the instruction. Checker messages reach revision passes word for word (A15), but the message is not instruction text, and §7.3 does not list it. So I left it. If Austin wants it neutral, changing it affects only v1.14 findings: no stored result has a `controlled.stock_pct` issue, so reproduction would not change.

## 4. Tests

In the S1 sandbox, with `TMPDIR=/home/uctpiaj/work/tmp/v114-scratch/tmp/s1` and `PYTHONDONTWRITEBYTECODE=1`:
- `python3 -m unittest discover -s _dev/tools -p 'test_*.py'`: 209 passed. The baseline was 199; `test_check_lean.py` went from 20 tests to 30.
- `python3 -m pytest -q -p no:cacheprovider _dev/tools/cockpit/acceptance/test_http.py`: 14 passed.
- `(cd _dev/tools/cockpit/frontend && npx vitest run)`: 53 passed. `node_modules` was copied from the checkout; the S1 package does not touch the frontend.

Changes in `test_check_lean.py`:
- `:510` (Antitrust) now expects an error. `:506` and `:509` are unchanged.
- The fixture list from `:496` gains:
  - Concern with None is an error;
  - an Other-scope row with its prices, or with a CVR value, is an error;
  - an Other-scope row with no Note gives a warning.
- A v1.14 twin of the `:320-341` inferred-exit test: `date.exact_day_mismatch` still fires, and `exit.inferred_reason` does not.
- New tests covering §9.2:
  - CVR Y with a value, and each Exclusivity value, at each Conditions level adds no issue;
  - Concern passes with Light, Heavy and Unclear;
  - a cohort with Financing Varies and Conditions Unclear passes;
  - Other-scope rows: a v1.14 row with blank per-share cells passes, and a v1.13.2 row with prices passes;
  - the Deadline outcome sets for both schemas, including that the legacy value counts toward `rounds.deadline_count`;
  - each of the three sequence warnings, with positive and negative cases (an Other-scope bid after an exit does not fire; a same-day Deadline revised row silences Extended; v1.13.2 never runs them);
  - message gating: the v1.13.2 inference-note message is unchanged, and the v1.14 message is extended;
  - the seam helpers: `ledger_schema` returns None for an unreadable workbook and for one without a Deal ledger sheet, plus `schema_for_header`, `deadline_outcomes` and `choice_lists`.

## 5. Wave 2: checker 1.7 against the frozen candidate

25 September 2026. S1 finalized (spec §7.3, §7.13 wave 2). The review in §3 was re-run against the frozen candidate, `SEC_Deal_Ledger_Extraction_Instruction_v1.14_candidate.md` (SHA-256 `c2d47a479d09eb46d0ab9fbf887568fcf13e972e2e11acbf08d5cdfab468ab27`, equal to `v1.14_candidate.sha256`), after review R's fixes (`R_REVIEW.md`; CHANGELOG §7). The code is in the wave-2 S1 sandbox, `/home/uctpiaj/work/tmp/v114-scratch/pkg/w2s1/_dev/tools/check_lean.py` (SHA-256 `fa95392809c58001cd90d2de700fa788dd2da690d5f332a4342e5cfa3421607f`), not in the live checkout. `CHECKER_VERSION` stays `1.7`: 1.7 has not been deployed, so no stored result carries it.

Files added or replaced in this folder:
- `compare_lists.py`: compares the checker's column and value lists with an instruction's text. Reads only; writes nothing.
- `reproduce.py` (replaced): takes explicit paths and refuses to overwrite its output (§5.3).
- `diagnose.py` (new here; it had been only in the wave-1 temp dir): the same treatment.
- `reproduction_wave2.json`, `diagnosis_wave2.json`: their outputs for this wave. `reproduction.json` is wave 1's and is unchanged.
- `inputs_wave2.sha256`: SHA-256 of the 77 input copies (§5.2).

### 5.1 Rule review

**Value lists.** `compare_lists.py --checker <w2s1 check_lean.py> --instruction <candidate>` reports all 23 comparisons equal, and exits 0:
- the columns of the Deal ledger (D1), Rounds (D3) and Questions (D4);
- the 30 Event labels (D2) and the 17 Deal facts fields (D5);
- Deadline outcome, as listed in D3 and in E9, against `deadline_outcomes("v1.14")`. `No deadline stated` is kept, and `Late bids accepted` appears nowhere in the candidate;
- Exit reason, Finality, Type, Formality, Conditions, the four condition columns and Initiation;
- the Y/Varies markers, the Stock % codes and the Acquirer type prefixes.

Run against the 24 September draft, the same script reports 6 differences (among them the Deadline outcomes and the "50–75" example), so it does detect a mismatch.

**R's fixes that touch a rule the checker encodes.**

| R | Candidate line | What the checker does | Verdict |
|---|---|---|---|
| R18 | 232: a request "made in the same communication as a bid row (Bid, Bid reaffirmed or Other-scope bid) … is coded on that row, with no Exclusivity changed row" | Wave 1's `ledger.exclusivity_duplicate` looked only at Bid and Bid reaffirmed rows (§7.3 change 6 as written) | **Changed.** The warning now pairs an Exclusivity changed row with any bid row (`BID_EVENTS`) of the same Who and Sort date whose Exclusivity is Requested or Required. This follows R18 and D27 ("a request in any bid communication is coded on that bid row"). The message already said "bid row #n". Still a v1.14-only warning. |
| R3, R7 | 56, 59, 133, 293, 299, 338: Other-scope rows leave Price low, Price high and CVR/earnout value blank; Stock % stays required | `bid.other_scope_per_share` checks those three cells, one issue per filled cell; `controlled.stock_pct` still requires Stock % on every bid row | Agrees; no change. A new test covers Price high filled alone. |
| R16 | 230: unaddressed terms are Not stated in Stock % and the four condition columns, and blank in CVR/earnout, CVR/earnout value and Antitrust; a same-price revision's price cells stay blank unless the filing shows the price unchanged | Not stated is accepted in each of those five columns; the markers and the CVR value may be blank; no price is ever required | Agrees; no change |
| R19 | 258: a statement that fits no value leaves the column Not stated | No Exclusivity "No" value exists | Agrees |
| R20 | 262: None needs "Regulatory not Concern (silence stays Not stated)" | `conditions.none_support` fires on Regulatory = Concern only, never on Not stated. The message's "no regulatory Concern" names the value Concern. | Agrees; no change |
| R21 | 267: Concern does not by itself meet H3 | No Concern → Heavy rule (do-not-add list) | Agrees |
| R2, R24 | 24, 314: an inferred exit takes Inferred = Y; Exit reason Not stated unless the filing reports one | `exit.inferred_reason` does not run on v1.14 (change 4) | Agrees |
| R5 | 112: Deadline outcome values in E9's order | The value list is a set, and the editor list is sorted | Agrees |
| R6 | 114: Bids received names Other-scope bids separately | Required non-blank only | Agrees (no count, per the do-not-add list) |
| R10 | 139: an unresolved party makes the entry Uncertain | `facts.auction_screen` accepts Met, Not met or Uncertain, with a number or "count unknown"; the candidate's example "Met (process 1): 3 parties; Uncertain (process 2): count unknown" passes | Agrees |
| R4, R8, R9, R11–R15, R17, R22, R23, R25 | wording of Bid, scope, entry, rounds and dates | No mechanical rule depends on the wording | Silent (compatible) |

**The rest of the §3 table** holds against the frozen text, line by line: B (24, 28, 30), D1 items 8–29, D2, D3, D5, E1, E3–E14 and F.4 (338). The cross-references in every v1.14 message resolve in the candidate: E8, E9, E10, E12 (with H1), E14, D1 and F.4. So do the two items §3 left conditional. The CVR value on a Varies row goes in the Note (299), and Acquirer type begins with one of the four types (125).

**The two rules §3 asked to recheck after R.**
- `conditions.level_unsupported`. Line 271 keeps "Begin a bid row's Note with the fact driving its level, naming the trigger (H1, H2 or H3) for Heavy", so the message, "the Note must name the condition that supports the level (E12)", still fits. It stays a warning that never reads the Note, so it is not the forbidden Heavy-trigger rule. No change.
- `controlled.stock_pct`. The candidate's Stock % example is "40–60" (E13, 297). The message now reads "a stated range such as '40-60'", with the hyphen the checker's messages use; `STOCK_RANGE_RE` accepts a hyphen or an en dash. This is a message change only. No stored result has a `controlled.stock_pct` issue.

**Not added**, as in §1: nothing on §7.3's do-not-add list. Every change is in `check_lean.py` and `test_check_lean.py`: the two lines above and the tests in §5.4.

### 5.2 Reproduction

The inputs were copied afresh from the live checkout into `/home/uctpiaj/work/tmp/v114-scratch/tmp/w2s1/repro/`:
- the nine `extraction/*.xlsx` workbooks and their receipts;
- the seven cockpit versions: five v1.13.2 runs and the two pilots;
- the 13 filings.

All 77 files are byte-identical to wave 1's copies in `tmp/s1/repro/`; their hashes are in `inputs_wave2.sha256`. No stored `check.json` was rewritten.

Command, from `/home/uctpiaj/work/tmp/v114-scratch/tmp/w2s1`, with `$S1` this folder:

```
python3 $S1/reproduce.py --inputs repro --before /home/uctpiaj/work/tmp/v114-scratch/wave1-base/_dev/tools/check_lean.py \
    --after /home/uctpiaj/work/tmp/v114-scratch/pkg/w2s1/_dev/tools/check_lean.py --output out/reproduction_wave2.json
```

**Result: identical to wave 1.** For all 16 workbooks, a field-by-field comparison of `reproduction_wave2.json` with `reproduction.json` found the following equal:
- the workbook hash;
- both schema readings;
- the stored summary;
- checker 1.6's result;
- 1.7's status, summary and identical-to-stored flag;
- both issue deltas (1.7 against stored, and 1.7 against 1.6).

So:
- the nine `extraction/` workbooks and the five v1.13.2 runs reproduce their stored results exactly;
- the Mac-Gray pilot changes only as documented: +2 `rounds.deadline_outcome_legacy`, +2 `ledger.exclusivity_duplicate` (#32 and #40), and −2 `exit.inferred_reason`;
- the P&W pilot gains only +2 `rounds.deadline_outcome_legacy`.

The wider duplicate rule adds nothing, because neither pilot has an Other-scope bid row.

### 5.3 The scripts

`reproduce.py --inputs DIR --before CHECKER --after CHECKER --output FILE` and `diagnose.py --inputs DIR --checker CHECKER --output FILE`:
- no longer find anything relative to their own folder;
- stop with a usage error if an argument is missing, if FILE exists, or if its folder does not exist;
- create FILE exclusively (`open(..., "x")`).

Both refusals were exercised. Run with no argument, `reproduce.py` prints its usage and writes nothing, so the delivered `reproduction.json` cannot be overwritten. The input layout is in each script's docstring.

`reproduce.py`'s result keys are now `before`, `after`, `delta_after_vs_stored` and `delta_after_vs_before`, where wave 1 had `checker_1_6`, `checker_1_7`, `delta_1_7_vs_stored` and `delta_1_7_vs_1_6`. The rest of the file is as in wave 1, plus `inputs`.

`diagnose.py` applies the same conditions as wave 1's version. It adds the filled per-share cells on Other-scope rows, which is the evidence for §2's statement about Synacor.

### 5.4 The four review warnings, re-diagnosed

This is the evidence for §2's statement that the four review warnings fire nowhere else. Command, from the same folder:

```
python3 $S1/diagnose.py --inputs repro --checker /home/uctpiaj/work/tmp/v114-scratch/pkg/w2s1/_dev/tools/check_lean.py \
    --output out/diagnosis_wave2.json
```

`diagnosis_wave2.json` confirms each claim of §2 with the wave-2 checker:
- `ledger.exclusivity_duplicate`: only Mac-Gray pilot rows 33 and 41 (#32 and #40), now under the wider rule;
- `rounds.extended_without_new_date`: no hit. The six Extended outcomes are Kraton P1R1, Meredith P1R3, PetSmart P1R2 (the extraction and the run), sTec P1R2 and Medivation P1R2;
- `exit.activity_without_reentry`: no hit;
- `bid.other_scope_note`: no hit. There are 21 Other-scope rows (Kraton 5, Meredith 10, Synacor 6), none with a blank Note;
- per-share cells on Other-scope rows: only v1.13.2 Synacor #54 and #59 (Price low and Price high on each). The gate keeps them clean.

### 5.5 Tests

In the sandbox, with `TMPDIR=/home/uctpiaj/work/tmp/v114-scratch/tmp/w2s1` and `PYTHONDONTWRITEBYTECODE=1`:
- `python3 -m unittest discover -s _dev/tools -p 'test_*.py'`: 281 passed (280 on the integrated tree). `test_check_lean.py` went from 30 tests to 31.
- `python3 -m pytest -q -p no:cacheprovider _dev/tools/cockpit/acceptance/test_http.py`: 18 passed.
- `(cd _dev/tools/cockpit/frontend && npx vitest run)`: 66 passed. `node_modules` was copied from the checkout.

Test changes in `test_check_lean.py`:
- new `test_other_scope_price_high_alone_is_an_error`. An Other-scope row with only Price high filled gives exactly one `bid.other_scope_per_share` error, on Price high;
- `test_v114_review_warning_exclusivity_repeating_a_bid_request` gains an Other-scope bid case, which must fire;
- `test_v114_messages_name_the_rule_without_changing_v1132` asserts the '40-60' Stock % message.

Run against the wave-2 base checker, the second and third fail and the first passes, so each behaviour change is covered.
