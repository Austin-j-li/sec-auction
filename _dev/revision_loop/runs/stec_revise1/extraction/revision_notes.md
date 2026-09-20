# Revision notes — sTec / WDC ledger (`extraction/stec.xlsx`)

Reviewed against `SEC_Deal_Ledger_Extraction_Instruction.md` (v1.8 lean) and
`raw_filing/stec_2013-08-08_DEFM14A.htm` ("Background of the Merger", pp. 23–35).

Checker row references are spreadsheet rows (header = row 1); ledger `#` values are
given where they differ. 24 findings: **17 acted on, 7 left unchanged.**

---

## 1. Deal facts, row 11, "Number of processes" — `1.` — ACTED ON

Certain. The cell held the text string `1.`, not a number, so it could not be matched
against the ledger's `Process = 1`. B5 lists the field as a count and B "Unsupported
numeric … cells stay empty, never zero" treats these as real values, not prose.

**Change:** value set to the number `1`. No substantive claim altered — the filing
supports a single continuing process (see finding 2 of the Questions sheet, Q1).

---

## 2. "Clean team agreement" of 06/18/2013 with WDC (nda_access, conf. 1.00) — NO CHANGE

Model judgment, and not supported by the instruction.

C9 is explicit: "A memorandum, process letter or data-room access given to parties that
have already signed is **not** another NDA; nor are drafts, amendments …". WDC had
already signed (addendum of 04/17/2013, ledger #21), so this is further data-room access
for an existing signatory, not a new confidentiality agreement. It therefore does not
touch the auction screen either, and the filing's own tally stands: "In total sTec
executed six non-disclosure agreements related to the exploration of a potential sale of
the company" (p. 28) — which is what Deal facts already records.

Nor does it earn a row under C2. It sits inside "From June 16 to June 22, 2013, WDC
conducted additional due diligence, including confirmatory due diligence calls" (p. 33) —
a document exchange with a bidder already under NDA, which C2 excludes by name. C2's
information-access exception requires a reported *difference* between live bidders; by
06/18 Company D had disengaged (06/05, ledger #54) and WDC was the only live bidder, so
there is no difference to record.

---

## 3. "our board of directors added Mr. Bahri to the special committee" (agreements, conf. 0.94) — NO CHANGE

Model judgment, not supported. A change in the composition of the target's own board
committee is not an event under C2: it does not change who is participating as a bidder,
what a bidder knows, an offer's price or commitment, what the target requires, the
timing, or the outcome. The fact is already carried where the instruction wants it — in
the Note of ledger #5, the 02/13/2013 Target sale decision row ("Bahri added
03/26/2013"). Adding a row would duplicate it.

---

## 4. Deal ledger, row 24 (ledger #23), Price low — "quoted passage gives a different price than $5.60" — NO CHANGE

Model judgment, contradicted by the instruction. The row is Company D's verbal
indication of 04/23/2013: "Company D provided a verbal indication of its interest to
pursue a transaction at a price greater than $5.60 per share" (p. 28).

C15: "A one-sided statement fills one cell — a floor ('at least $X') in **Price low** …
and the Note says which." "Greater than $5.60" is a floor, so $5.60 goes in Price low and
Price high stays empty. That is exactly what the row does, and the Note already says "a
floor of greater than $5.60 per share with no ceiling stated". $5.60 is the filing's own
figure; inventing a higher number would breach C15's bar on constructing prices.

---

## 5. Summer 2012 lunch with Mr. Hajeck of WDC (contact, conf. 0.86) — NO CHANGE

Model judgment, not supported on the facts of the filing.

The passage is not an approach about acquiring sTec. At the lunch "Mr. Hajeck inquired
about the interest of Mr. Manouch Moshayedi and Mr. Mark Moshayedi … in continuing to run
sTec and whether they had any plans to retire, but there was no further discussion between
WDC and sTec until the communications described below" (p. 24). The filing frames the
whole passage, including the 2011 Coyne lunch, as routine industry contact — "in keeping
with Mr. Moshayedi's practice of meeting from time-to-time with other executives in the
storage industry" — and states that "prior to the process described below, such approaches
have been general and exploratory in nature, and no specific transaction terms were
proposed" (pp. 23–24).

C2 gives "no rows for routine calls, meetings, visits"; C6 adds that "commercial
cooperation between the companies is not an offer"; C9's Contact row is for first
contacts about a transaction. None of the B2 labels fits: there is no Bidder interest
("a party approaches about acquiring the target"), no price, and no participation change.
A row here would also break the ledger's own treatment of Companies A, B and D, each of
which is recorded only because it raised an acquisition.

---

## 6. "BofA Merrill Lynch then contacted the company's officers and Dr. Daly to report the communication from WDC" (contact, conf. 0.84) — NO CHANGE

Model judgment, clearly wrong. This is the target's own banker reporting internally to the
target's officers and chairman on 05/31/2013 (p. 31). A **Contact** under C9 is a contact
between the target side and a prospective acquirer, not internal reporting within the
target side, and C2 excludes routine calls. The substance — WDC's withdrawal — is already
ledger #52.

---

## 7–15. Questions row 2 (Q1): "Rows affected" cites #55–#63, but those rows carry no Q1 flag — ACTED ON

Nine certain findings (#55, #56, #57, #58, #59, #60, #61, #62, #63).

Real inconsistency. B1 defines **Flag** as "id of an open Question touching this row", and
Q1 is the mandatory process-and-round-map question (Part D), whose alternative reading
moves precisely these rows into a round 3 or a second process. So the Question is right
that it touches them; the Flag cells were the omission. The workbook's own practice
confirms this direction: every row cited by Q2, Q4, Q5 and Q6 already carries its flag.

**Change:** Flag set to `Q1` on ledger rows #55, #57, #59, #60, #61, #62, #63, and to
`Q1, Q6` on #56 and #58, which were already flagged Q6. Nine flagged rows out of 63 does
not offend Part D's warning that "a flag on every row tells the reviewer nothing".

Q1's "Rows affected" was left as it stands, and no ledger content (Process, Round, dates,
prices) was touched: the recommended answer — one process, everything from 06/10 inside
round 2 — is what C8 requires, since round 2 was opened as final on 05/16 (p. 30) and a
further best-offer request to the same finalist is "how the final round ends, not a new
round".

---

## 16. Questions row 2 (Q1): about 139 words, instruction asks for about 60 — ACTED ON

Certain. B4: "About 60 words per entry." Rewritten to **61 words** across the five review
fields, keeping the reading, the alternative boundary, the rows it would move and the page
cites required by Part D.

---

## 17. Questions row 3 (Q2): about 131 words — ACTED ON

Certain. Rewritten to **65 words**. The three deadline outcomes, their evidence (pp. 29–31)
and the alternative are preserved; the repetition of dates already in the ledger was cut.

---

## 18–19. Questions row 4 (Q3): "Rows affected" cites #53 and #54, but neither carries a Q3 flag — ACTED ON

Two certain findings. Same defect and same fix as 7–15. Q3 asks whether Company D's
05/28 non-submission is an exit; if it were, #53 (the 05/31 offer to continue) and #54
(the 06/05 withdrawal) would both change — #54 would no longer be Company D's single exit
row. B1's Flag definition therefore covers them.

**Change:** Flag set to `Q3` on ledger rows #53 and #54. #46 already carried it.

---

## 20. Questions row 4 (Q3): about 123 words — ACTED ON

Certain. Rewritten to **64 words**.

---

## 21. Questions row 5 (Q4): about 138 words — ACTED ON

Certain. Rewritten to **65 words**.

---

## 22. Questions row 6 (Q5): about 91 words — ACTED ON

Certain. Rewritten to **61 words**. The exact quotation "decided not to continue
discussions with Company C" (p. 28) was kept verbatim.

---

## 23. Questions row 7 (Q6): "Rows affected" cites #58, but #58 carries no Q6 flag — ACTED ON

Certain, and a real omission: #56 was flagged Q6 and #58 was not, although Q6's
conditions judgment is what distinguishes the two bids.

**Change:** #58 Flag set to `Q1, Q6` (Q1 from findings 7–15, Q6 from this finding).

---

## 24. Questions row 7 (Q6): about 92 words — ACTED ON

Certain. Rewritten to **61 words**. Both quoted fragments — "a difference of opinion had
emerged internally" and "had been rejected" (pp. 31–32) — were checked against the filing
and kept exact.

---

## Summary of edits to `extraction/stec.xlsx`

| Sheet | Cells changed | Finding(s) |
|---|---|---|
| Deal facts | B11: `1.` → `1` | 1 |
| Deal ledger | Flag on ledger #53, #54 (→ `Q3`) | 18, 19 |
| Deal ledger | Flag on ledger #55, #57, #59–#63 (→ `Q1`) | 7, 9, 11–15 |
| Deal ledger | Flag on ledger #56, #58 (→ `Q1, Q6`) | 8, 10, 23 |
| Questions | Q1–Q6: Question, Recommended answer, Why with page, What changes — rewritten | 16, 17, 20, 21, 22, 24 |

No rows were added or removed (63 events, unchanged), no Process, Round, price,
formality, conditions, count, date or exit value was altered, and no "Rows affected"
citation was narrowed. Sheet order, frozen header rows, filters and wrap-text are
unchanged.
