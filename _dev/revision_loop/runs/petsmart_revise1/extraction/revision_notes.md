# Revision notes — petsmart.xlsx

Checked each of the 15 findings in `checker_report.md` against
`SEC_Deal_Ledger_Extraction_Instruction.md` and the DEFM14A in `raw_filing/`.
Four changes were made, all in response to findings. Nothing else in the
workbook was touched.

---

## Findings 1–9 — Q1 cites #34–#42, but those rows are not flagged Q1
**[warning; certain] — accepted; workbook changed.**

Real inconsistency. Part D says "Flag a row only when an open Question touches
it", and Q1 is the mandatory process/round-map Question, which must give "the
most plausible alternative boundary with the rows it would move".

The citation is correct, not the flags. Under Q1's alternative reading — the
12/10 instruction to submit improved bids opening a third round rather than
extending round 2 — #33 becomes a Round opened row and every row after it that
currently sits in round 2 (#34–#42) changes its Round value. So Q1 genuinely
touches all nine rows.

**Change:** added `Q1` to the Flag cell of ledger rows #34–#42. Row #38 already
carried Q2 and now reads `Q1; Q2`; the other eight were blank and now read `Q1`.

**Rejected alternative:** trimming Q1's "Rows affected" to `#9, #13, #24, #33`.
That would have silenced the checker but left the reviewer without the list of
rows the alternative boundary moves, which is exactly what Part D asks the
round-map Question to supply.

## Finding 10 — Q1 runs to about 134 words against the instruction's 60
**[warning; certain] — accepted; workbook changed.**

B4 asks for "About 60 words per entry". Q1 was the longest entry in the sheet.
Condensed Question, Recommended answer, "Why, with page" and "What changes if
answered differently" while keeping every substantive element the instruction
requires: the round map claimed, the reason it was read that way with pages, the
alternative boundary, and the rows it would move. Now 83 words.

## Finding 11 — Q2 runs to about 113 words
**[warning; certain] — accepted; workbook changed.**

Same rule. Condensed Recommended answer, "Why, with page" and "What changes if
answered differently"; the Question line was already tight and is unchanged. The
deadline-outcome claims (10/30 Enforced, 12/05 superseded before arrival, 12/10
Extended, 12/12 Enforced) and both alternatives are preserved. Now 83 words.

While rewriting, the page citation for the replacement of the 12/05 due date was
given as p. 25: "the Company set the evening of Wednesday, December 10 ... as the
deadline for submission of final bids" falls after the page-24 break.

## Finding 12 — Q3 cites #32, but #32 is not flagged Q3
**[warning; certain] — accepted; workbook changed — citation dropped, not flag added.**

Real inconsistency, but here the citation is what is wrong. Q3 asks who formed
Bidder 3 and whether both members were live final-round invitees. Row #32 is
Bidder 3's "Did not submit" on 12/10. If Q3 were answered the other way — the
second member had been eliminated on 11/03 and re-entered — no cell of #32 would
change: Bidder 3 is still one bidding unit (C3: "investors making a joint offer"
are one bidder), still did not submit on 12/10, still Count 1. The rows that
would change are #27 (the Bidding group changed row) and the two members' own
bid rows #17 and #18, all of which are flagged Q3.

**Change:** Q3's "Rows affected" is now `#17, #18, #27`. Row #32's flag is left
as `Q5`, which is the Question that does bear on it (who ended Bidder 3's
participation).

## Finding 13 — Q3 runs to about 114 words
**[warning; certain] — accepted; workbook changed.**

Same rule as findings 10 and 11. Condensed Recommended answer, "Why, with page"
and "What changes if answered differently". Now 85 words.

The old "Why" cited the Reasons section's "two other bidding groups" as p. 26;
that passage sits after the page-26 break, on p. 27 (the same paragraph row #42
correctly cites as p. 27). Rather than carry a wrong page into the shortened
text, the rewritten "Why" rests on the Background at p. 24–25 — four bidders
advanced, three units appear afterwards — and keeps the counter-evidence that
p. 24 says only one of the two was "invited into the final round".

## Finding 14 — Deal facts, Account "appears to have 7 sentences"
**[warning; certain] — not accepted; no change.**

B5 asks for "five or six plain sentences". The Account has six. The seventh
"sentence" is an artifact of splitting on a full stop followed by a capital: the
abbreviation "J.P. Morgan" is cut into "J.P." and "Morgan was approached by 27
parties ...". Removing that split leaves exactly six sentences:

1. weak Q1 results, JANA and Longview pressure, the 08/13 decision, the 08/19
   announcement, Industry Participant kept out;
2. 27 parties, 15 confidentiality agreements, six indications on 10/30;
3. 11/03 advancement of the four at or above $80.00, Bidder 3 formed;
4. the 12/10 bids and Bidder 3's non-submission;
5. the 12/12 improved bids;
6. 12/13 approval and 12/14 signing and announcement.

Six is within the permitted range, so there is no error to correct under the
instruction, and the Account was left as written rather than reworded to suit
the counting method.

## Finding 15 — Deal ledger row 41 (#40): quotation not found inside one paragraph
**[info; model judgment, confidence 0.00] — not accepted; no change.**

This finding reports only that the checker could not verify the row, not that
anything is wrong. Row #40 is the Simpson Thacher adviser row, quoting "with a
copy to: Simpson Thacher and Bartlett LLP" (p. A-46).

Checked against the filing. The words are exact and the page is right: the
notices block in Section 8.7 of the merger agreement sits on the page whose
footer reads A-46, and the text runs "To Parent or Merger Sub: / Argos Holdings
Inc. c/o BC Partners ... / with a copy to: / Simpson Thacher and Bartlett LLP
425 Lexington Avenue ...". The quotation is continuous as printed; it is not a
splice of separate passages (Part D). It fails an automatic paragraph match only
because the notices block is laid out as table cells, so "with a copy to:" and
the Simpson Thacher address are separate HTML elements.

The quotation was also left alone because shortening it to a single element
would weaken the row: "Simpson Thacher and Bartlett LLP 425 Lexington Avenue"
alone does not show whose counsel the firm is, whereas the "with a copy to:"
line under "To Parent or Merger Sub:" is what supports the row's claim that it
acted for Parent.

---

## Summary of edits

| Sheet | Cell(s) | Edit | Finding |
|---|---|---|---|
| Deal ledger | Flag, rows #34–#42 | added `Q1` (row #38 became `Q1; Q2`) | 1–9 |
| Questions | Q1: Question, Recommended answer, Why, What changes | condensed 134 → 83 words | 10 |
| Questions | Q2: Recommended answer, Why, What changes | condensed 113 → 83 words | 11 |
| Questions | Q3: Rows affected | `#17, #18, #27, #32` → `#17, #18, #27` | 12 |
| Questions | Q3: Recommended answer, Why, What changes | condensed 114 → 85 words | 13 |

No rows were added or removed on any sheet. No ledger classification, price,
date, count or quotation was altered. Header row, freeze panes, filters, wrap
text, column widths and the MM/DD/YYYY date formats are unchanged. After the
edits every row cited in a "Rows affected" cell carries that Question's id in
its Flag, and every flag on a ledger row is cited by the Question it names.

## Observation outside the findings (not acted on)

Deal facts, "Number of processes" holds a date value (01/01/1900) rather than the
number 1 — the classic symptom of `1` written into a date-formatted cell. No
finding points to it, so under the brief for this revision it was left as it is.
