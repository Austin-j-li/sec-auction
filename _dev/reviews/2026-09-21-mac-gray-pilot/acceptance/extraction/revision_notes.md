# Mac-Gray revision notes: acceptance-review corrections A01–A11

Input: `extraction/mac-gray.xlsx`, SHA-256 `f54295a242057b0e6f72fddf9555d6b4c007eea10c9fc13b1202b659439e112e` (55 events). This matches the packet's stated input.
Output: `extraction/mac-gray.xlsx`, SHA-256 `db85a39b00bb98702e73ad3e891cb4ab50202f2e032fcb3278ef0e6e45f351e1` (58 events).
Authority: `checker_report.md`, the lead's adjudicated correction packet (not an automatic checker report), under the frozen instruction v1.13.2. The only other sources used were the supplied filing (`raw_filing/mac-gray_2013-12-04_DEFM14A.htm`) and the input workbook.

Event numbers below are **input** numbers unless marked "now".

## Corrections made

| ID | Location | Change |
|---|---|---|
| A01 | Deal ledger, new rows now #54–#56 | Added three Adviser rows immediately before signing (input #54, now #57): Morgan Stanley & Co. LLC, Deutsche Bank Securities Inc., Evercore Group L.L.C. For each: When `by 10/14/2013`, Process 1, Round 3, Sort date and Date to 10/14/2013, Date from empty. Type, price fields, All cash, Formality, Conditions, Count, Exit reason, Inferred, Flag and Reviewer note are empty. The packet's Note and Quote are used verbatim. The quote was checked against Annex A §5.11 in the filing, and the section falls between the A-30 and A-31 page markers. Formatting copied from the existing Kirkland Adviser row. |
| A02 | #49 Kirkland & Ellis | When changed to `by 09/25/2013`; Date from cleared; Sort date and Date to remain 09/25/2013; Note replaced with the packet text; Quote unchanged. Checked against pp. 38–39. |
| A03 | #3 Party A | Quote and page replaced with the p. 27 passage on BofA's target-initiated call. It was checked against the filing. No other field changed. |
| A04 | #8, #23, #29 | #8 Note: "Unsolicited written proposal" → "Unsolicited proposal". #23 Note: "Written preliminary indication" → "Preliminary indication". #29 Note replaced with the packet text. Formality and Conditions unchanged. |
| A05 | #19 | Note sentence about communicating the decision replaced with the instruction wording (p. 33). |
| A06 | #7 | Note replaced with the packet text separating the 06/12 discussion from the 06/24 exclusion. |
| A07 | #46 | Note: "It then got…" → "During 09/25–10/07 it got…". No access row added. |
| A08 | #47 | Note now compares with $20.75 on 09/18 and $21.25 on 09/21. Exit reason (Not stated) and Inferred (Y) unchanged. |
| A09 | Questions Q4, Q6, Q8 | Only the "What changes if answered differently" cells replaced with the packet text. Recommended answers, Rows affected and row flags unchanged. |
| A10 | Questions Q5 | Recommended answer replaced with the packet text. Cohort rows #17/#37 unchanged (Count, Sort dates, event type, Date bounds, Rounds). |
| A11 | Deal facts, Account | "and Party C dropped out." → "and Party C did not submit or reiterate its earlier offer." Nothing else in the Account changed. |

## Dependent changes

- Renumbering: input #54 (signing) → #57 and input #55 (announcement) → #58. The # column now runs 1–58 without gaps.
- Internal references: every `#n` across all four sheets was checked. The only reference to a shifted event was in input #50's Note (MacDonald voting agreements): "(#54)" → "(#57)". No Rounds, Questions "Rows affected" or Flag entry referred to #54 or #55, so none changed.
- The Deal ledger filter range and its hidden filter-database name changed from A1:V56 to A1:V59.

## Checks carried out (original vs. revised workbook)

- A cell-by-cell comparison of all four sheets, with ledger rows after the insertion offset by three, shows only the changes listed above.
- Sheet order and names, headers, column widths, freeze panes (A2), cell styles and number formats (dates are still real Excel dates in MM/DD/YYYY) are identical. The three new rows use exactly the same style IDs as the existing Adviser rows.
- At XML level, styles.xml, theme, Rounds sheet XML and content types are byte-identical. The only differences are cell contents, the ledger dimension and filter range, the filter-database name, and the file's modified timestamp.
- The Deal ledger still has exactly 13 Bid rows, and their core fields are unchanged.
- Process and round assignments and population bounds are unchanged. Sort dates never decrease; the new rows' 10/14/2013 falls between 10/12 (#53) and signing on 10/14 (now #57).
- All Reviewer note columns (ledger and Questions) are still empty.

## Not performed (out of scope for this pass)

- No new extraction beyond the three authorized Adviser rows. No economic-term bids were added.
- The separate research question on fee/guarantee negotiations was not decided. No research-convention decisions were made.
- The Rounds sheet was not edited; no correction required it.
- No web sources or other models were used. The mechanical checker was not run here; it runs separately.
