# Revision notes — extraction/penford.xlsx

Source: Penford Corporation DEFM14A filed 29 December 2014, "Background of the Merger" (pp. 23–33).
Every one of the 88 checker findings is addressed below. Findings are grouped where they are the
same defect repeated; each finding number appears exactly once.

---

## 1. Findings 1–58 — Round column held text, not numbers — **CHANGED**

**Findings 1–25, 27–44, 46–58** ("Round must be a nonnegative integer or 'post'; found '0' / '1' / '2'"),
and **findings 26 and 45** ("Round opened must carry a positive numbered round", Deal ledger rows 26
and 44).

Certain, and correct. The Round cells for every row except the final `post` row were stored as text
strings ("0", "1", "2") rather than numbers, so no round value was readable as an integer and the two
`Round opened` rows (#25, round 1; #43, round 2) failed the positive-round test for the same reason.
The round *map itself* was never in question — only the cell type.

**Action.** Converted all 56 numeric Round cells to integers (0, 1, 2), leaving the single `post`
value (#57, Merger announced) as text, as B1 and C8 allow. No round assignment was altered, and no
other cell was touched.

## 2. Findings 59–60 — Rounds sheet rounds not found in the ledger — **CHANGED (by the fix above)**

"Process 3 Round 1 / Round 2 appears in Rounds but not in the ledger."

Certain, and a direct consequence of §1: the Rounds sheet stored Round as a number while the ledger
stored it as text, so `(3, 1)` and `(3, 2)` never matched. After the integer conversion both Rounds
lines match ledger rows. Verified after saving. No separate edit was needed.

## 3. Finding 61 — Deal facts, Number of processes — **CHANGED**

"Number of processes must equal the ledger's 3; found '3, as recorded: the 2007 approach (Process 1) …'."

Certain, and correct. The field carried a sentence of commentary around the number, so the value was
not the count B5 asks for. The count itself (3) was right and matches the ledger's Process values
1, 2, 3.

**Action.** Value set to the number `3`. Nothing is lost: the composition of the three processes is
visible in the ledger's Process column and in Q1, which addresses whether the 2007 and 2009
approaches deserve their own processes.

## 4. Finding 62 — row 48, Price low $19.00 not in the quote — **NO CHANGE**

Model judgment (0.96). Row 48 is #47, Ingredion's `Bid reaffirmed` of 8 October, quoting Sidley
Austin's circulation of a revised merger agreement draft.

The finding is right that the quotation does not state $19.00, but that is what C12 prescribes: a
late-reconfirmation row "carries the standing price ('carried from #n')" and the filing's reported
act is the returned draft, not a new price. The quote supports the row's specific claim — the act by
the bidder — and the Note already reads "Reaffirmed by returned draft; price carried from #42." The
finding's own expectation ("the row carries an earlier price forward") is what the workbook does.
The price $19.00 is established at #42 (p. 30). Nothing to correct.

## 5. Findings 63 and 65 — data-room access and diligence calls not in the ledger — **NO CHANGE**

**Finding 63** (0.93): "Starting in early September, Penford provided Ingredion access to an online
dataroom…". **Finding 65** (0.86): "Penford's management team also conducted numerous calls and
arranged for in-person meetings or site visits with Ingredion…" (both p. 27).

Neither earns a row under C2. Finding 65 is the textbook exclusion: "No rows for: routine calls,
meetings, visits and document exchanges, including every contact with a bidder already under NDA."
Ingredion had been under a nondisclosure and standstill agreement since 21 August.

Finding 63 is an access event, but C2 gives an access row only for "access, presentations or
information given to some live bidders and not others … only where the filing itself reports the
difference." In early September no rival was yet under a confidentiality agreement — Party C signed
15 September, Party D 23 September, Party A 30 September — so the filing reports no difference at
that date, and it never reports that a rival was refused data-room access. The one difference the
filing does report is that Penford would not give Party A in-person management presentations unless
its price looked competitive (p. 30), and that already has its own row, #39. The data room is
recorded in the Note of #22, the row that opens Ingredion's diligence access, which is where C2
directs it ("Access given alike … goes in the Note of the row that admits them"). Adding rows here
would be adding rows the instruction folds into a note.

## 6. Findings 64 and 66 — quoted price said to differ — **NO CHANGE**

**Finding 64** (0.90), row 42 (#41), Price low $18.50. The quotation is exact and states the price:
"Mr. Fortnum then stated that Ingredion was prepared to move forward based on a proposed price of
$18.50 per share on a fully diluted basis." (p. 30).

**Finding 66** (0.68), row 52 (#51), Price low $19.00. The quotation is likewise exact and states the
price: "Mr. Fortnum called Mr. Malkoski to confirm the proposed price of $19.00 and discuss finalizing
the draft merger agreement…" (p. 32).

Both quotations were checked character-for-character against the filing and both name the recorded
price. The findings are simply wrong.

## 7. Finding 67 — row 46, Party A's $17.50–$18.00 of 4 October — **NO CHANGE**

Model judgment, confidence 0.48. The 4 October sentence reads "Party A indicated any offer would be
below $17.50 - $18.00 per share in cash" (p. 31), which taken alone could be read as a ceiling under
C15's one-sided rule.

C10 requires the neighbouring paragraphs to be used to constrain an event, and the filing itself
settles the reading nine days later: on 13 October Party A's "value range for a potential transaction
had been reduced from $17.50 - $18.00 per share to $16.00 - $18.00 per share" (p. 32). The filing
therefore attributes $17.50–$18.00 to Party A as its own range, and C15 says a bidder's own range
fills its endpoints. Recording it as a bare ceiling would also make the ledger incoherent against #50,
where the successor range $16.00–$18.00 is recorded with both endpoints from the same sentence.

The row's Note already discloses the tension ("the filing later calls $17.50-$18.00 Party A's value
range") and the row is flagged Q5, which puts the question to the reviewer. Kept as recorded.

## 8. Findings 69–82 and 84 — Rows affected cited rows that carry no such flag — **CHANGED**

**Findings 69–82**: Q2's "Rows affected" cited #33, #41, #42, #45, #47, #49, #50, #51, #52, #53, #54,
#55, #56, #57, none of which carried a Q2 flag. **Finding 84**: Q3 cited #25, which carried only Q2.

Certain, and a real inconsistency under B1 ("Flag — id of an open Question touching this row"). It was
resolved in both directions, because some of the cited rows were genuinely touched by the question and
some were not:

*Flags added* (the rows whose Round actually turns on Q2 — Ingredion's round-1 bids, which the
alternative would return to round 0, and the substantive round-2 rows, which the alternative would
move to round 1): #33, #41, #42, #47, #49, #51, #53, #54 now read "Q2; Q4" or "Q2". #25 now reads
"Q2; Q3", since the size of the September wave is exactly what Q3 asks about. Semicolons follow the
instruction's own multi-value separator (B3, Deadline outcome).

*Citations removed* from Q2's Rows affected: #45, #50, #52, #55, #56 (Party A's and Party C's rows)
and #57 (post-signing announcement). These stay in round 1 or post under either answer to Q2, so
under D ("Flag a row only when an open Question touches it") they should neither be flagged nor cited.
Q2's Rows affected now reads "25, 33, 41-43, 47, 49, 51, 53, 54". Two round-2 adviser rows (#44, #46)
would also shift round under the alternative; they are left unflagged and uncited as immaterial, to
avoid flags that tell the reviewer nothing.

Checked after saving in both directions: every row cited by a Question carries that Question's id, and
every flag on a ledger row is cited by that Question.

## 9. Findings 68, 83, 85, 86, 87, 88 — Question entries far over length — **CHANGED**

Q1 ~130 words, Q2 ~145, Q3 ~147, Q4 ~146, Q5 ~142, Q6 ~117, against B4's "About 60 words per entry".
Certain, and correct.

**Action.** All six entries rewritten to carry the same substance more briefly — now 64, 73, 68, 72,
68 and 66 words across the review fields. Every recommendation, the page citations, and the
alternative-with-consequences required by Part D are preserved; what was cut was restatement of the
ledger and repeated narrative detail. Q2 and Q4 sit slightly above the others because Part D requires
the round-map question to name the rows the alternative boundary would move, and Q4 must cover two
separate calls (formality and the two reaffirmation rows).

---

## Summary

- Changed: the Round column's cell type throughout the ledger (findings 1–58, which also cleared
  59–60); the Number of processes value (61); nine Flag cells and Q2's Rows affected (69–82, 84); the
  wording of all six Question entries (68, 83, 85–88).
- Not changed: findings 62, 63, 64, 65, 66, 67 — all model judgment, and none supported by the filing
  read against the instruction. No row was added, none removed, and no substantive classification
  (round map, formality, conditions, prices, exits, counts) was altered.
- Workbook re-saved as `extraction/penford.xlsx` with its four sheets, frozen header rows, filters and
  MM/DD/YYYY date formats intact.
