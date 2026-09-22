# Mac-Gray: two-cell verification repair (revision notes)

Scope: the two corrections authorized in `checker_report.md` (the development lead's repair of wording introduced by C06). No new extraction, cleanup or research-convention decision was made. Sources used: the frozen `SEC_Deal_Ledger_Extraction_Instruction.md`, `raw_filing/mac-gray_2013-12-04_DEFM14A.htm`, `extraction/mac-gray.xlsx` and `checker_report.md`.

## Change 1: Questions!D6 (Q5, "Why, with page")

- Old: "Only three indications were reviewed on 07/25 (p. 33);"
- New: "Three round-1 indications and Party A's June 21 proposal were reviewed on 07/25 (p. 33);"
- Filing basis (pp. 33–34): at the July 25, 2013 meeting "representatives of BofA Merrill Lynch reviewed the preliminary indications of interest received from Party B, Party C and CSC/Pamplona as well as the Party A June 21 proposal." The old wording implied that only three offers were considered. The new wording separates the three new round-1 submissions from the four offers reviewed.
- The rest of the cell is unchanged.

## Change 2: Rounds!E2 (Round 1, "Who was in")

- Old: "Unnamed: some of 16 other financial NDA signers (#17), number signed by the 07/23 due date unknown (signing continued after it: Party A 08/05; Q5)."
- New: "Unnamed financial NDA signers admitted by the 07/23 due date: 0–16, unknown (no individual signing dates; 16 is the eventual total of other financial NDA signers, not a known population at the deadline, #17; signing continued after it: Party A 08/05; Q5)."
- Filing basis (p. 32): "Over the next two months a total of 20 potential bidders, including two strategic bidders (Party A and CSC/Pamplona) and 18 financial bidders (including Party B and Party C), entered into confidentiality agreements". No individual signing dates are given for the 16 unnamed financial signers. "Some of 16" implied that at least one had signed by the deadline, which the filing does not establish. Instruction Part B and E3 require an explicit range where the count is not supported, so the cell now states 0–16, unknown.
- Kept: the three named signers (CSC/Pamplona; Party B, Party C), the August 5 evidence (Party A's 08/05 NDA), the #17 and Q5 references, and the Party A "still being received, not admitted" text.
- No numeric Count cell and no closure bound (#37, Rounds!J2/J3) was changed.

## Verification

A full comparison of the original and saved workbooks found:

- Package: the same 12 parts in the same order. Every part except `xl/worksheets/sheet2.xml` (Rounds) and `xl/worksheets/sheet3.xml` (Questions) is byte-identical, including styles, workbook, relationships, theme and document properties.
- In those two sheets, all XML outside the cell elements is identical: dimensions, column widths, sheet views/freeze panes, merges, and any validations or controls. Cell counts are unchanged (40 and 70). The only differing cell elements are Rounds!E2 and Questions!D6. Both keep their original style index (`s="2"`) and inline-string type.
- Cell by cell across all four sheets (value, style, number format, font, fill, border, alignment, hyperlink, comment): the only differences are the values of Rounds!E2 and Questions!D6.

Exactly two cell changes were made, and no other value, format, reference, structure or control changed.
