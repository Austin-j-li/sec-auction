# Mac-Gray controlled revision: verified result

**All 13 accepted corrections are implemented. The final revision recovers two missing events, restores material option terms, and removes the unsupported exact first-round bidder population and July 23 cohort closure.** The development lead verified every changed cell and both inserted rows. Two wording defects introduced in the first pass were identified and repaired before acceptance.

The final workbook is [extraction/mac-gray.xlsx](extraction/mac-gray.xlsx). It is a separate revision of the preserved raw v1.13.2 draft; the original v1.13 baseline and raw v1.13.2 output remain unchanged. Verification is by Codex, the development lead. Human benchmark validation and review-time savings remain untested.

## Result and verification boundary

| Measure | Raw v1.13.2 | Verified revision |
| --- | --- | --- |
| Ledger events | 53 | 55 |
| Bid events | 13 | 13; core fields unchanged |
| Rounds | 3 | 3; boundaries, due dates, outcomes and finality unchanged |
| Questions | 9 | 9 |
| Mechanical errors | 1 | 0 |
| Mechanical warnings | 8 | 13 |

The complete comparison contains **68 changes to existing cells**: 29 substantive or directly dependent edits, 21 event-number updates and 18 reference updates. Two additional rows were checked in full, including their blank cells. The ledger filter and its hidden named range expand by two rows. No original event was deleted.

All changes fall within the accepted correction packet or necessary dependencies. The analysis checks the final changes and their effects; it is not a fresh whole-filing certification of every unchanged cell.

## Verification of each accepted correction

Coordinates below refer to the final workbook. Event numbers are final unless a prior number is expressly stated. The [complete cell diff](verification/CELL_DIFF.md) contains untruncated before/after text and the full inserted rows; [per-cell verification](verification/cell-verification.json) records each disposition.

| Task | Changed cells or events | Source/rule and result |
| --- | --- | --- |
| C01 — Q9 counterfactual | Questions D10, F10 | P.39 reports Kirkland's October 7 returned merger-agreement draft. E10/E11 require reconsidering a reaffirmation under the alternative Informal reading. The false “no markup/no formal bid” claim is removed; no reaffirmation is added under the retained Formal classification. |
| C02 — adviser quotation | Deal ledger Q3 | The new p.27 excerpt supports the April authorization to work with BofA, matching the existing date. The historical engagement Note and later adviser events are preserved. Part B/D2. |
| C03 — rollover permission quotation | Deal ledger Q46 | P.38 explicitly supports the target allowing Moab to resume rollover discussions. The new quote supports the action rather than only Moab's wish. Date and event unchanged. Part B. |
| C04 — outreach timing | Deal ledger B12, B13 | P.32 says “during the next several weeks” after June 24, without a July endpoint. The wording now preserves that precision, with the same lower bound and blank Date to. B/E8. |
| C05 — July bid sequence | Deal ledger P23 | Pp.33–34 distinguish C's oral bid reviewed at the meeting from its written revision later July 25. The Note now preserves that sequence; both bids and the late-bid outcome remain. B/E8/E9. |
| C06 — anonymous bidder timing | Events #17/#37; Rounds E2/J2/E3/J3; Q5; Q2's dependent population statement | Pp.32–36 support the eventual 16-person residual cohort, not an exact first-deadline population. R1 now says **0–16, unknown** for the anonymous signers admitted by July 23. One inferred closure uses the later complete final-stage set as a conservative upper bound. Details below. B/E3/E8/E14. |
| C07 — voting agreements | Added event #50, Excel row 51 | P.39 dates execution September 27; the Note distinguishes effectiveness at October 14 signing. The row records shareholder support, with no bidder Count or bid fields. P.37 supports the prior request. E2/D2. |
| C08 — option terms | Deal ledger P41 | P.36 supports 10% of new equity, strike at B's initial cost basis, vesting on the base-case projections over five years, excluding future acquisitions. These terms are restored. B's $21.50 package valuation, $19 cash/$2.50 options attribution and financing qualification remain. D1/E13. |
| C09 — exclusivity-extension request | Added event #52, Excel row 53; P54 dependency | P.40 reports a request already made by the October 9 meeting and later discusses the October 15 requested expiry and conditional authorization. P.41 dates execution October 12. The request now has its own bounded-date event; the execution remains separate. No bid deadline is created. D2/E2/E8. |
| C10 — round-map alternative | Questions D2, F2 | E6 explicitly makes the first final solicitation a round even with unchanged bidders; p.36 establishes that request. The unsupported merger of rounds and the claim that the numeral determines Formality are removed. The retained map and E5 analysis are preserved. E6/E11/F. |
| C11 — first-contact Count | Deal ledger M4 | One named Party A supports Count 1. The April 8 Target interest is still a contact, not entry. P.27; D1/E3. |
| C12 — inferred request timing | Deal ledger O15 | The June 28 upper bound for communicating the July 23 deadline is derived from the first dated package, as the existing Note explains. It now carries Inferred = Y. P.32; B/E8/E9. |
| C13 — opening order | Events #9/#10 and numbering dependencies | The June 24 marker precedes the other R1 act. Both acts retain their dates and substance. The mechanical opening-order error is gone; no round was added. |

Q2's removal of “19 to 20” is a necessary C06 dependency. It was separately examined rather than accepted merely because the reviser changed it. The numeric count depended on the same unsupported deadline population.

## Participation accounting and its remaining uncertainty

The filing establishes twenty NDA signers eventually: A, B, C, CSC/Pamplona and sixteen other financial signers. A entered earlier through its June bid, so its later NDA is not another entry. The record accounts for all twenty exactly once: sixteen in the anonymous closure, C at the September 18 non-submission, A/B at September 24 exclusivity, and CSC/Pamplona at signing.

The anonymous cohort's **actual entry dates, July 23 eligibility and actual exit dates remain unknown**. The first pass's unsupported July 23 closure is replaced by an inferred “Dropped by target, **by September 11**” event. The final request explicitly names only A, B, C and CSC/Pamplona, after the retrospective two-month NDA window. The earlier July 25 or August transitions cannot safely date all sixteen because individual signings are unknown.

September 11 is a conservative bound, not the day all sixteen exited and not evidence that they stayed live until then. Their earlier individual paths may include non-submission or exclusion at different transitions. The NDA row's Sort date and placement cannot be used to turn that uncertain population into an exact earlier live count. The revision preserves this limitation in its Notes, Rounds and Q5.

## Errors caught during verification

The first revision introduced two wording defects within C06:

1. Q5 said only three indications were reviewed July 25. The filing names three round-1 indications plus A's June 21 proposal. The final text includes both.
2. R1 said “some” of the sixteen unnamed signers were admitted, implying a positive lower bound. The final text says “0–16, unknown”.

A second isolated Opus pass repaired **only Questions D6 and Rounds E2**. A strict comparison confirms those are its only cell changes. All other workbook package parts are byte-identical to the first pass, including the complete ledger sheet. See [repair verification](repair-verification.json). Both provider outputs and their original notes are preserved so the first-pass defects remain visible.

## Checks completed

- Compared every cell across all four sheets, matching all 53 original events by identity rather than comparing shifted row positions. All 13 bids retain bidder identity, type, dates, process, round, prices, cash classification, Formality, Conditions and Count. Deal facts is unchanged.
- Verified the 75 event-reference occurrences resolve and checked every Question's explicit row list against ledger Flags. All original references affected by renumbering map to the same events.
- Verified both new rows' complete contents against their passages and D1/D2. Their dates are real Excel dates, and required non-bid fields stay blank.
- Located all 55 ledger quotations on their cited printed pages, with each within 30 words. This checks quotation accuracy and page attribution; the separate substantive review above checks the changed claims.
- Compared 1,334 matched cells' resolved font, fill, border, alignment, protection and number formats: unchanged. New rows use the same column styles. Filters, freeze panes, sheet order, column widths and annotations were checked. The only intended control change is the extended ledger filter/named range. The writer also normalizes equivalent date-style definitions and updates the modification timestamp; these have no changed cell-format effect.
- Inspected wrapped content previews for the changed ledger rows, Rounds and Q5. These were fallback previews from cell values and widths; native Excel rendering was not available. No workbook layout changes were introduced.
- Ran the checker after each completed provider session. The final **0 errors / 13 warnings** comprise five long Notes, seven long Questions, and the already identified false positive about missing deadline-outcome Questions. Required evidence/uncertainty was retained; no duplicate Questions were added to silence the checker.
- Verified that the frozen instruction, source filing, v1.13 baseline, raw v1.13.2 draft, original audit/adjudication and production runner retained their recorded hashes.

The exclusions in the packet remain excluded: the reverse-fee/economic-terms boundary, a separate information-state row for A, the April authorization label, the withdrawn full-access-row proposal, contact-unit ambiguity and Conditions interpretation. No new convention was adopted.

## Execution and retained evidence

Both sessions used Claude Opus 5 high through the existing isolated revision runner with task-specific prompts pinned before first launch. The reviser saw only the instruction, filing, selected workbook and adjudicated packet. The checker and lead's independent verification were outside the model session. Production code and instruction text were not edited.

| Pass | Elapsed model time | Reported provider cost |
| --- | --- | --- |
| Controlled revision | 340.131 seconds | $2.763831 |
| Two-cell verification repair | 67.912 seconds | $0.4859345 |
| Total revision work | 408.043 seconds (6.8 minutes) | **$3.2497655** |

These are provider-reported costs, not account billing. Human active-review time was not measured. The earlier extraction/audit cost $7.1015065; the complete Mac-Gray model workflow including revision and repair reports $10.351272.

Key evidence: [accepted corrections](ACCEPTED_CORRECTIONS.md), [repair corrections](REPAIR_CORRECTIONS.md), [complete cell comparison](verification/CELL_DIFF.md), [per-cell verification](verification/cell-verification.json), [final checks](verification/final-checks.json), [source paragraphs](source-passages.json), [mechanical report](mechanical-check.json), and `provenance/` / `pass-1/provenance/`. Disposable run folders are removed after recording the results. No commit or push was performed.

Final workbook SHA-256: `f54295a242057b0e6f72fddf9555d6b4c007eea10c9fc13b1202b659439e112e`.
