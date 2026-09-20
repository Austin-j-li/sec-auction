# Revision notes — mac-gray.xlsx

Workbook reviewed against `SEC_Deal_Ledger_Extraction_Instruction.md` (v1.8 lean) and the
filing `raw_filing/mac-gray_2013-12-04_DEFM14A.htm` (DEFM14A, 12/04/2013; background pp. 27–41).
All 21 checker findings are listed below with the decision taken and the reason.

**Summary:** 18 findings acted on (findings 4–21), 3 rejected (findings 1–3).
Edits were confined to the Flag column of the Deal ledger and the Account field of Deal facts.
No rows were added or removed; no other cell was touched.

---

## Findings 1–3 — "probably absent from the ledger (agreements)" — model judgment — **no change**

### 1. MacDonald voting agreements (negotiated 09/24–09/27/2013, entered into 09/27/2013)
**Decision: no row added.** The passage is confirmed in the filing (p. 38): "Between
September 24, 2013 and September 27, 2013, Kirkland and outside counsel to Mr. MacDonald
negotiated the terms of the MacDonald voting agreements … which became effective upon entry
into the merger agreement."

It does not earn a row under C2. It changes no participant, no bidder's information, no price or
commitment, no target requirement, no process timing and no outcome; it is the negotiation of
transaction documents ancillary to the merger agreement, and C2 excludes "negotiation of legal
terms; successive agreement drafts". C4 is explicit that a shareholder's lock-up-style support
does not create a bidding group or a participant. There is also no event label in B2 that fits it.

The instruction's treatment is to fold it into a related Note, and the ledger already does so:
row #48 (Merger agreement signed) records "MacDonald and Moab voting agreements" among the
signing-package terms. Adding a row would duplicate that and enlarge a ledger C2/A asks to keep
small.

### 2. Board determination and approval of the merger agreement (10/14/2013)
**Decision: no row added.** Confirmed at p. 41. C2 excludes "board review of an offer already
recorded", and B2 provides a single **Merger agreement signed** row for the execution of the
agreement — which the ledger has at #48, on the same date, carrying the agreed price and
consideration. The board's approval is the internal step that produced that signing, not a
separate event that changes participation, price, requirements, timing or outcome.

### 3. Special Committee executive session and recommendation to the Board (10/14/2013)
**Decision: no row added.** Confirmed at p. 41. Same reasoning as finding 2, and a step further
removed: it is a committee recommendation on an offer (CSC/Pamplona's $21.25, already recorded at
#41) that the ledger records, taken on the day of signing. C2's no-row list covers it directly.
The checker's own confidence on this one is the lowest of the three (0.86), consistent with it
being a restatement of finding 2.

---

## Findings 4–20 — Questions "Rows affected" cite ledger rows whose Flag omits the Q id — certain — **acted on**

These are genuine inconsistencies. B1 col. 18 defines **Flag** as "id of an open Question touching
this row", and B4 gives each Question a **Rows affected** list. A row the Question names as
affected is by definition a row the Question touches, so the two must agree. In every one of the
17 cases the citation in the Questions sheet is sound on the filing and the instruction — the
answer to the Question would change something in the cited row — so the defect is an
under-filled Flag column, not an over-broad citation. **Fix applied: the missing Q id was added to
the Flag cell of each cited row** (existing ids kept, separated by "; " as already used on #37).

After the edit, Rows affected and Flag agree in both directions for all six Questions: every cited
row carries the id, and no row carries an id that is not cited. 28 of 49 rows now carry a flag —
each because a genuinely open Question would alter a cell in it, which is what D asks for; the
flags are still concentrated (Q6 on the nine winner rows, Q4 on the four final-round bids, and so
on) rather than spread over every row.

| Finding | Question | Ledger row | Flag now | Why the Question touches the row |
|---|---|---|---|---|
| 4 | Q1 round map | #8 Target sale decision, 06/24/2013 | Q1 | Q1 asks where round 1 opens. The ledger opens it at the outreach (#9, C8 rule 1); the live alternative is C8 rule 2, the 06/24 decision that launched the outreach, which would make #8 the Round opened row and move it out of round 0. |
| 5 | Q1 | #25 Party A NDA, 08/05/2013 | Q1 | Q1's own "What changes if answered differently" names #25 as moving to round 1. |
| 6 | Q1 | #26 information access, 08/06–08/27/2013 | Q1 | Named in Q1's alternative as moving to round 1. |
| 7 | Q1 | #27 Deadline set, 08/27/2013 | Q1 | Under the alternative boundary (round 2 opening with the 08/27 letter) this row becomes the Round opened row; its Event and Round both change. Per C11, a Round opened row that sets the due date needs no separate Deadline set row, so #27 would be absorbed. |
| 8 | Q2 deadline outcomes | #21 Party B bid, 07/24/2013 | Q2 | Q2 asks whether the 07/23 and 09/09 due dates were "Late bids accepted" or "Enforced". That turns on exactly these four one-day-late bids; #21 is one of the two bids that makes 07/23 "Late bids accepted" (C11: a bid is late only if its Date from falls after the due date), and its Note states the lateness. |
| 9 | Q2 | #22 Party C bid, 07/24/2013 | Q2 | As for #21. |
| 10 | Q2 | #31 Party A bid, 09/10/2013 | Q2 | The 09/09 due date's outcome rests on this bid and #32. |
| 11 | Q2 | #32 Party C bid, 09/10/2013 | Q2 | As for #31. |
| 12 | Q5 pricing of Party B's package | #44 Party B Dropped by target, by 09/24/2013 | Q5 | Q5's alternative ("cash-only $19.00 would rank Party B below CSC/Pamplona's $20.75") changes #44's Exit reason: on the recorded $21.50 reading the exit reason is "Terms or process" (the committee preferred certainty over a higher face value, p. 37); on a $19.00 reading, "Lower offer than rivals" (C16). |
| 13 | Q6 winner's type | #10 CSC/Pamplona Contact, by 06/28/2013 | Q6 | Q6 asks whether CSC/Pamplona is Strategic or Mixed. Every CSC/Pamplona row carries Type = Strategic in col. 4, so a different answer rewrites that cell on each of them. |
| 14 | Q6 | #17 NDA signed, 07/11/2013 | Q6 | As above. |
| 15 | Q6 | #18 Bid $18.50, 07/23/2013 | Q6 | As above. |
| 16 | Q6 | #28 Bid $19.50, 09/09/2013 | Q6 | As above. |
| 17 | Q6 | #35 Bid $20.75, 09/18/2013 | Q4; Q6 | As above; Q4 flag retained. |
| 18 | Q6 | #41 Bid $21.25, 09/21/2013 | Q4; Q6 | As above; Q4 flag retained. |
| 19 | Q6 | #42 Exclusivity changed, 09/24/2013 | Q6 | As above. |
| 20 | Q6 | #47 Exclusivity extended, 10/12/2013 | Q6 | As above. |

Q3 (rows #13, #20) and Q4 (rows #35, #36, #37, #41) were already consistent and were not touched.
Row #48 already carried Q6.

**Alternative considered and rejected.** Each mismatch could instead have been cleared by deleting
the row from the Questions sheet's "Rows affected" list. That was rejected: the citations are
correct on the merits, and D requires a Question to state "the rows it would move", so removing a
row that the answer really would move would replace a formatting inconsistency with a substantive
error and lose information the reviewer needs.

---

## Finding 21 — Deal facts, Account has 7 sentences; B5 asks for five or six — certain — **acted on**

Confirmed: the Account ran to seven sentences. B5 requires "Account (five or six plain sentences)".

**Fix applied:** the fourth and fifth sentences were joined with ", and", leaving six sentences and
no loss of content. Changed from:

> … Revised indications on September 9-10 ranged from $16.00 to $19.50. A request for final
> indications by September 18 drew $20.75 from CSC/Pamplona, …

to:

> … Revised indications on September 9-10 ranged from $16.00 to $19.50, and a request for final
> indications by September 18 drew $20.75 from CSC/Pamplona, …

The two sentences describe consecutive steps of the same solicitation sequence, so merging them
was the least invasive way to meet the limit. No fact, figure, date or name in the Account was
altered.

---

## Checks after editing

- Deal ledger, Rounds, Questions, Deal facts, in that order; no sheets added; row counts unchanged
  (49 ledger rows, 3 round lines, 6 Questions, 16 Deal facts fields).
- Every Q id in a "Rows affected" list now appears in the Flag cell of the cited row, and every Q id
  in a Flag cell appears in that Question's "Rows affected" list.
- Account is six sentences.
- Header freeze at A2, filters, wrap text and the MM/DD/YYYY date formats on Sort date, Date from,
  Date to, Opened and the Deal facts date fields are intact; dates remain real Excel dates.
- Saved in place as `extraction/mac-gray.xlsx`.
