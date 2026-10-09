# Nine live workbooks beside Alex's reference

The existing comparator completed on all nine original live Version 1 workbooks. Each CLI command returned exit code zero.

These results establish comparison coverage. They require source review before research acceptance.

## Inputs and outputs

The input selection used a read-only join between `deal_bases` and `versions`. All nine records identify raw outputs from 28 September. Each output receipt records the workbook hash and reference hash.

The tool wrote only into `alex_comparison_outputs/<deal>/` under this review directory. Each directory contains `alex_bids.csv`, `alex_events.csv`, and `summary.json`.

Representative consumer command, with the actual input selected from the inventory:

```bash
python3 _dev/tools/compare_alex.py /home/uctpiaj/work/Projects/ledger-live/_dev/cockpit/state/versions/datalink/opus55-medium-20260928-1531-b29df5/datalink.xlsx --deal datalink --out _dev/reviews/2026-10-09/alex_comparison_outputs/datalink
```

The CLI requires a new or empty destination. Do not rerun it over the saved evidence. No tests, assertions, or model calls form part of these comparisons.

## Counts

| Deal | Reference rows | Aligned / labelled bids | Equal T0 / compared |
|---|---:|---:|---:|
| Datalink | 52 | 15 / 21 | 14 / 15 |
| Kraton | 35 | 13 / 15 | 8 / 13 |
| Mac-Gray | 34 | 13 / 13 | 13 / 13 |
| Meredith | 29 | 0 / 20 | 0 / 0 |
| Penford | 25 | 8 / 9 | 8 / 8 |
| PetSmart | 53 | 12 / 13 | 11 / 12 |
| Providence & Worcester | 36 | 13 / 14 | 11 / 13 |
| sTec | 28 | 7 / 7 | 7 / 7 |
| Synacor | 29 | 9 / 11 | 9 / 9 |
| **Total** | **321** | **90 / 123** | **81 / 90** |

T0 is the recorded Formality. Other equality counts are T1 78/90, T1u 69/90, T2 81/90, and T3 80/90. Do not choose a research variant by the highest match count.

## Why these are not accuracy rates

**Seven matches lack a bidder-name match.** Four concern Kraton and three concern PetSmart. PetSmart reference row 6430 maps one unnamed party to ledger cohort #22, whose Count is two. See `petsmart/alex_bids.csv:4`. The greedy alignment permits this fallback at `compare_alex.py:195–217`.

**The date policy differs from the inherited report.** The program prefers precise-date column AA at `compare_alex.py:199`. The inherited report uses edited column AB at `WORKBOOK_CHECK.md:11`. The discrepancy is not merely formatting.

For sTec reference rows 7165–7166, AA says May 16 while AB says May 28. Providence row 6054 has July 20 in AA and August 4 in AB. A preferred old date can change an alignment or its apparent quality.

**An event “agree” can conceal a date difference.** Datalink reference row 2873 maps November 6 to an October 24 withdrawal, a 13-day gap. See `datalink/alex_events.csv:53`. Event matches permit up to 31 days at `compare_alex.py:254`.

**The denominator omits unmatched ledger events.** The comparator does not separately report them as a measure of extracted-event coverage. It therefore cannot establish recall or precision for the full ledger.

**Some unmatched bids reflect scope.** Meredith has 41 Other-scope bids and no whole-company bids. Its 0/20 alignment does not establish twenty missing bids. Synacor G/I also involve partial scope.

**The reference has different fields and provenance.** It lacks equivalent Conditions, Process, Round, and participation-total columns. It also retains many original Chicago entries. Only seven labelled bids carry a red correction to `bid_type`.

## Concrete review leads

| Evidence | Observation | Interpretation limit |
|---|---|---|
| Datalink reference row 2868; live #61; CSV line 19 | Reference Formal versus live Informal for Party C's $11.25 | Needs source/route review, not automatic correction to the reference. |
| Penford reference row 6478; live #35 | Both live price cells blank despite a $17.50–18 Note | Review the source proposal and appropriate bound. |
| PetSmart reference row 6449; live #35; CSV line 11 | Informal reference versus Formal live bid; ceiling versus point | A common value does not establish identical price semantics. |
| Datalink Rounds | Four live rounds versus five adopted | Astra verifies the omitted August 16 stage and dependent exits. |
| PetSmart `Rounds!C2` | August 13 versus adopted October 3 | Verified workbook-versus-decision difference; source adjudication not repeated here. |
| Synacor `Rounds!C4` | July 19 versus adopted July 13 | Same limitation. Six total round rows remain consistent with the adopted process structure. |

The Synacor Note also says Company H never entered, while the adopted materials include H among the NDA signers. This remains a source-review lead. It is not a fresh participant-count ruling.

## Relation to older evidence

The inherited `WORKBOOK_CHECK.md` reviewed draft conventions and source themes on 27–28 September. It explicitly disclaims a new extraction or research sign-off. It does not prove comparison of the current live outputs.

Today's nine CLI outputs provide that automatic comparison. They still do not prove source accuracy or generalization. Ruling 9 requires separate treatment of codings shaped by rules developed from individual deals.

The input hashes make these results reproducible against the retained originals. Any future revision needs its own comparison record.
