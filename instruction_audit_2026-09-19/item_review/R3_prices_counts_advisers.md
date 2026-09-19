# R3 — items 4 (bound prices), 9 ("counts" in §1), 12 (adviser dates)

Reviewer note: read the revised instruction in full, Alex's collection instructions, his voice notes
(including his own closing summary), his hand-collected sheet read cell-by-cell with openpyxl for font
colour, the three filing backgrounds, and the twelve old model workbooks. Verdicts below.

| Item | Verdict | One line |
|---|---|---|
| 4. "At least $X" | **KEEP WITH REWORDING** | Placement matches Alex's sheet; the rule has no ceiling case, no headline-price guard and collides with the valuation-statement bullet. |
| 9. "counts" in §1 | **KEEP WITH REWORDING** (8 words) | Redundant with §7.3, which already does the work; make it a cross-check so it cannot license overriding an exact narrative count. |
| 12. Adviser dates | **KEEP WITH REWORDING** | Alex's revealed practice is exactly this rule, but the sentence is unscoped and, read literally, drags a re-engagement row back before its own termination row. |

---

## Item 4 — "At least $X" price bounds (§9.4)

### (a) Current wording

§9.4, second bullet, verbatim:

> - "At least $X" or "at or above $X": set Price kind = Bound only, put X in Price low, leave Price
>   high blank, and begin the constraint in Terms or outcome with `Bound: ≥ X` followed by the filing's
>   words. The cell is a bound, not a bid. Where the wording is ambiguous between a floor on the whole
>   range and a level the range merely reached, say so in Questions.

It replaced (patch tag `B2-bound`, `apply_instruction_patch.py:277`):

> - "A range reached at least $80" constrains its upper endpoint, not its lower endpoint. Leave both
>   numeric price cells blank, set Bound only, and write the precise constraint in Terms or outcome.

Two other §9.4 bullets bear on this: "Do not average a range"; and, two bullets later, "A valuation
statement is not necessarily an offer. Keep its value and comparison in text, not in the bid-price cells."

### (b) Evidence from Alex's materials

**The legacy schema, measured.** `ref/deal_details_Alex_2026.xlsx`, sheet `deal_details`, 9,335 priced
rows. Price columns are `bid_value` (T), `bid_value_pershare` (U), `bid_value_lower` (V),
`bid_value_upper` (W); missing is the string `"NA"`, never blank.

- **798 rows have lower ≠ upper (a real range). In 798 of 798, `bid_value == bid_value_lower`** — never
  the upper endpoint, never the midpoint. So the headline price variable for a range is its low end.
- **48 rows are one-sided** (exactly one of lower/upper numeric). **In all 48, `bid_value` and
  `bid_value_pershare` are `NA`.** The bound never becomes a price.
- Of the 48, **14 are lower-only** (a floor: ≥ X) and **34 are upper-only** (a ceiling: ≤ X).

Alex's email in the collection instructions fixes what that means for estimation: "bid_value and
bid_value_pershare: normally, these are equal… The only relevant thing for us is bid_value_pershare";
"bid_value_lower and bid_value_upper: for informal bids, if an interval is submitted."

So the inherited convention is: **a bound goes in the endpoint cell on the side of the inequality; the
other endpoint and the headline per-share price stay empty.** Direction is carried by which cell is filled.

**The PetSmart row itself.** Row 6428 (`PETSMART INC`, "Unnamed party 1", 10/30/2014, Informal):
`bid_value=NA, bid_value_pershare=NA, bid_value_lower=80, bid_value_upper=NA`. Every cell carries the
**theme-default text colour (`theme:1`), not the explicit `FFFF0000` red** Alex's own edits use — so on
the red/black convention this is **an inherited Chicago RA row he kept**, not his edit. (Same for 47 of
the 48 one-sided rows; only STEC 7153 is explicit red. Worth re-checking if authorship is load-bearing:
`theme:1` is a theme reference, normally rendering black, not a literal black RGB.) But he read that
exact sentence
and reasoned about it (voice note III.3, his words):

> "the background says that in round one, 6 bidders have submitted IOIs, 3 bidders among them initially
> indicated price ranges that reached at least $80/share… Buyer Group and another bidder are only 2 out
> of 3 bidders who bid at least $80. Bidder 2 is initially below $80. This means that there is one bidder
> that has still been unaccounted for that has initially bid at least $80. Later on, the background
> confirms this, saying that they will allow the four bidders who had indicated a price or range at or
> above $80/share to proceed."

and concluded for PetSmart overall "the AI reading of this deal as well as my new reading of it appears
to be very consistent with the earlier hand-collected database." He re-derived the third bidder and left
row 6428 untouched. That is tacit endorsement of `lower=80` — weaker than a red edit, but he did not miss it.

**Alex's own red bound row.** Row 7153 (`S T E C INC`, Company D, 04/23/2013, Informal) is entirely red
— his own added row — with `bid_value=NA, bid_value_pershare=NA, lower=5.6, upper=NA`. So when Alex
himself creates a bound row he uses the same shape: endpoint cell filled, headline price NA.

### (c) Hand application

**What is actually known about PetSmart's third bidder.** Both sentences, from `petsmart_bg.txt`:

1. "Three bidders initially indicated price ranges that reached at least $80.00 per share, including the
   Buyer Group, which indicated a range of $81.00 to $83.00 per share, and another bidder, which
   suggested a range of $80.00 to $85.00 per share."
2. "The board determined to allow the four bidders that had indicated a price or range at or above
   $80.00 per share to proceed to the final round of the sale process."

Certain: the third bidder's range has an **upper endpoint ≥ $80**. Sentence 2 is the only support for a
floor, and it is ambiguous: "a price **or** range at or above $80.00" reads either as "the whole range
lies at or above $80" (which would give lower ≥ 80, and is consistent with all three disclosed ranges —
$81–83, $80–85, $81–84 — each of which has its low end at or above $80) or as a loose restatement of
sentence 1. **Alex takes the first reading** ("the background confirms this"). I judge it supported but
not certain; this is exactly the ambiguity the current bullet's last sentence tells the model to raise in
Questions, which is the right handling.

Note the sign asymmetry under the two readings. If lower ≥ 80 (Alex), then `Price low = 80`
*understates* the true low end — conservative. If only upper ≥ 80, `Price low = 80` is unsupported. The
old rule's alternative, `Price high = 80`, is worse under either reading: read naively it says the
bidder's ceiling was $80, making the third ≥$80 bidder look like the cheapest of the four.

**The three designs on this row.**

| Design | Cells | What a reviewer/export sees |
|---|---|---|
| (a) current | low 80, high blank, kind Bound only | matches row 6428 exactly; number survives; needs a flag to stop it reading as a bid low |
| (b) old rule | both blank, kind Bound only | number survives only as prose; contradicts row 6428; the one numeric fact about a round-1 finalist is lost |
| (c) dedicated `Price bound` field | low/high blank, new column | unambiguous, but a fifteenth expandable field that maps to nothing in Alex's schema, and Price low/high export blank again |

(b) is what all four old models produced, faithfully and with good reasoning — e.g. `glm` raised Q8:
"Populating $80.00 as the low endpoint of R027 … would create false precision and distort price
progression analysis"; `opus`, `ds` and `glm` all wrote out that the constraint is on the upper endpoint.
So the old bullet *was* applied. But it leaves PetSmart's round 1 with four submitters carrying numbers
and one carrying none, when Alex's own sheet carries the number. (c) is a new column Alex did not ask
for, on a dimension he calls secondary, and it still leaves the legacy cells empty. **(a) is right on
placement.** Its problems are gaps, not the design.

**Gap 1 — no ceiling case.** The bullet covers only "at least $X" / "at or above $X". **34 of the 48
legacy one-sided rows are ceilings**, so the commonest bound direction in Alex's own data has no rule at
all. A ceiling attached to a live offer ("we are prepared to go up to $X", "our revised indication is no
more than $X") currently falls through to no rule and is coded by guess.

The nearest case in the three pilot deals is PetSmart, 12/10/2014: "Bidder 3 verbally communicated to
J.P. Morgan that their valuation would not be above the current stock price of approximately $78 per
share." That one is **not** governed by the bound rule even after the fix, because it is a valuation
statement made instead of bidding ("Bidder 3 did not submit a written offer") — §9.4's valuation bullet
and §10.3's "A **Valuation statement** can stand alone when material and no offer is made" keep its number
in text. Worth recording that this is where the instruction and Alex's sheet still diverge: row 6449
codes it `Bidder 3 | 78 | 78 | 78 | 78 | Informal | 12/10/2014` — a point informal bid (theme-default
text, RA row, kept). The changelog lists "PetSmart Bidder 3's $78" under "needs no instruction change",
so I am not reopening it; I flag only that the divergence is real and is a numeric one, and that if it is
ever reopened, `Price high = 78, Bound only` is the coding that sits between blank and Alex's point.

**Gap 2 — precedence collision.** The bound bullet and the valuation bullet sit two lines apart and give
opposite instructions for "Party X said its valuation was at least $20". Nothing says which wins.

**Gap 3 — the headline-price guard is missing.** "The cell is a bound, not a bid" states the intent but
not the mechanic. In the legacy schema the mechanic is `bid_value = NA`. In the new schema there is no
headline price field, so an export will derive one — and the only available rule, learned from 798/798
range rows, is `bid_value := Price low`. That silently converts the PetSmart bound into an $80 informal
bid, pooled with $81–83, $80–85 and $78 in any round-1 price average. `Price kind = Bound only` is a
sufficient guard *only if every consumer reads it*, and Alex's legacy schema has no column to receive it.

**Other phrasings.** "In excess of $X", "no less than $X" → floor. "Up to $X", "no more than $X", "not
above $X", "below $X" → ceiling. "Low-to-mid $20s" is not a bound but an imprecise range: the filing
supplies no endpoints, so both cells stay blank with the phrase in Terms — writing 20–25 would be
invented precision (§3.3). "A premium of at least 20%" is a bound on a derived quantity, not a per-share
price; §9.4 already says "Numeric per-share calculations are not entered as stated prices", so it belongs
in Terms. Worth naming these so the model does not reason by analogy into the price cells.

### (d) Downstream risk and reversibility

- **Mis-averaging.** A Bound only row exported as `bid_value_lower` with a derived `bid_value` enters
  every price mean, price-progression and "informal bid level" statistic as a real bid. For PetSmart this
  pulls the round-1 informal level toward $80 from a bidder whose bid may have been anywhere below it.
- **Stage counts are unaffected** — the bidder is still one live unit in round 1, which is the
  first-order variable. So the risk is confined to prices.
- **Reversible**, provided Terms carries the filing's exact words and the inequality sign. Then any later
  re-coding (blank it, move it to the other cell, drop the row from price work) is a re-read of one text
  field across a few dozen rows, not a re-extraction. That is the argument for keeping the number **and**
  for making the wording mandate both the sign and the quotation. Irreversible only if the number is
  stored with no direction — which is what the current bullet risks for ceilings, since it gives them
  no home at all.

### (e) Verdict

**KEEP WITH REWORDING.** Replace the single bullet with:

> - A one-sided price statement fills the endpoint cell on the side of the inequality and leaves the
>   other blank: a floor ("at least $X", "at or above $X", "in excess of $X", "no less than $X") in
>   **Price low**; a ceiling ("up to $X", "no more than $X", "not above $X") in **Price high**. Set Price
>   kind = Bound only and begin Terms or outcome with `Bound: ≥ X` or `Bound: ≤ X` followed by the
>   filing's words. A Bound only row states no bid level: leave Cash at closing blank, never average it
>   with actual bids, and never treat the cell as a submitted endpoint. This applies to a communicated
>   offer or indication; a valuation statement that is not an offer keeps its number in text under the
>   bullet below. A bound on a premium, multiple or aggregate value is not a per-share bound and stays in
>   Terms. An imprecise range ("low-to-mid $20s") supplies no endpoints: leave both cells blank. Where the
>   wording is ambiguous between a floor on the whole range and a level the range merely reached, say so
>   in Questions.

PetSmart's third bidder then gets: `Bid`, Count 1, Informal, Price low 80.00, Price high blank, Price
kind Bound only, **Price origin Stated** — the $80.00 figure is the filing's own number, and Price origin
records where the *number* came from, not how the bidder was individuated (the inference that a third
such bidder exists belongs in Why and evidence; "Inferred" is reserved for a number the model derived) —
Terms beginning `Bound: ≥ 80.00 — "price ranges that reached at least $80.00 per share"; the 11/03
decision describes the four advancing bidders as having "indicated a price or range at or above $80.00
per share"`, plus a Questions entry on the two readings. That is row 6428 with the ambiguity documented.

**Confidence: high** on the gaps (direction, precedence, headline guard) and on the placement matching
Alex's sheet; **medium** on which reading of sentence 2 Alex would defend if pressed — he asserts the
floor reading in the voice note but calls the whole situation "probably too complicated for the AI".

**Not checked:** the STEC source sentence behind Alex's red 5.6 bound (no STEC filing in the repo), so I
infer from cell placement that it was a "≥" phrasing; the source sentences behind the other 47 legacy
one-sided rows; whether an export script already exists that maps Price low to a headline price (none in
the repo).

---

## Item 9 — "counts" added to the §1 consult list

### (a) Current wording

§1, final sentence of the third paragraph (patch tag `S1-counts`; the word `counts` is the whole edit):

> Consult the filing's merger-party descriptions, transaction summary, agreement terms and adviser's
> analysis as needed to resolve buyer type, consideration, dates, **counts** and conflicts.

### (b) Evidence

Alex's collection instructions §3.4, NDA table, **Chicago black text** (an inherited rule he kept, not
his addition):

> "Note, there usually are instances when management reports to the board about the progress of the
> takeover. This often provides a summary of how many NDAs have been signed. Use this information to
> **double check** the collected information."

"Double check", not "use as the total". His own voice notes point the same way, and all his count
examples are inside the background or the board-update paragraphs, not elsewhere in the filing: PetSmart
2 — "there are statements like at least 27 bidders have been contacted. The deal background, however,
clearly states that 27 is the precise number"; Kraton 1 — "there is clarity that 10 have signed NDA
agreements… if we go a little bit deeper into the background and look at page 35…". His one explicit
instruction to leave the background is for **types**, not counts (Kraton 2: the winner's type from the
"parties involved in the merger" chapter). His summary item E asks only that an uncertain NDA count be
flagged.

### (c) Hand application to the two known traps

**Providence.** Background: "representatives of GHF contacted 11 potential strategic buyers (including
Party A) and 18 potential financial buyers. Each of the potential strategic buyers and 14 potential
financial buyers subsequently executed confidentiality agreements" → 25. Then "In early July 2016, a
potential strategic buyer that had not previously been part of the process ('Party C') approached the
Company… After executing a confidentiality agreement, Party C was provided the memorandum" → **26**.
Reasons section (p.33): "a broad group of potential bidders… **25 of whom** entered into confidentiality
agreements with the Company and received information related to the Company and **six of whom** submitted
non-binding letters of intent." The Reasons total omits Party C. Its "six" refers to the late-July LOIs,
not the nine May IOIs — a different population at a different stage.

**PetSmart.** Background: 27 contacted; 15 NDAs; "On October 30, six of the potentially interested
parties submitted indications of interest." Reasons (p.27): "contacted or were contacted by **more than
25** potential participants, entered into non-disclosure agreements with and engaged in due diligence or
provided management presentation to **15** potential bidders, received first round indications of
interest from **5 bidder groups**." Two of the three conflict with the narrative.

**Does §7.3 as revised handle them?** §7.3 reads: "Preserve exact, approximate, lower-bound and
qualitative count language… Equally, do not add 'at least', 'approximately' or a range that the filing
does not use: a number the filing states exactly is recorded as exact. Where a board update or the
Reasons section states a total, use it to check the narrative count and reconcile the two in Summary."
Applied: 27 stays exact against "more than 25" (the "states exactly" clause is explicit); 26 NDAs stay
against the Reasons' 25, "reconciled" meaning both shown, not one overwritten; six IOI submitters stay
against "5 bidder groups". §3.2 supplies the tie-break — "Prefer the passage with the most specific,
directly relevant evidence, not automatically the background or automatically a summary" — which points
to the dated narrative in every one of these cases. So **§7.3 plus §3.2 already do the work**, and the
"reconcile in Summary" phrasing does not tell the model to correct the narrative count.

**Empirically the models already behave.** Under the *old* instruction (no §7.3 reconciliation sentence
at all), all four preserved both numbers: `opus` — "'more than 25 potential participants', a compatible
lower bound… 27 is the exact figure"; `sol` — "Six IOIs versus five bidder groups… preserved as a source
conflict"; `glm` — "'five bidder groups' (Reasons) is the post-teaming group count, kept distinct from
six submitting parties"; `sol` on Providence — "This makes the ledger-observed NDA count 26, while
another filing passage describes 25 signers; preserve the conflict." The only wobble is `opus`, which
wrote that if the Reasons' 5 "were preferred the cohort would be ten" — it preferred the narrative, but
it entertained letting a summary number move a residual cohort. That is the failure mode to foreclose.

**What the §1 word actually does.** Nothing directional: the four places §1 names are "merger-party
descriptions, transaction summary, agreement terms and adviser's analysis". **The Reasons section and
board updates — where counts live — are not in that list.** So "counts" does not send the model where
the counts are; §7.3 does. It is redundant. Its only live reading is the unhelpful one: that a count from
a summary elsewhere in the filing is a legitimate way to "resolve" a count.

### (d) Downstream risk and reversibility

Low but asymmetric. A wrongly "resolved" count changes the residual cohort in §10.2 (PetSmart: 9
non-submitters vs 10), the per-stage balance in §13.2/§13.3, and the auction screen base — all
first-order for the number of live bidders per stage. It is also the specific error Alex has already
complained about twice (PetSmart 2, Kraton 1). Fully reversible per deal if both numbers are in Summary,
which §7.3 requires; irreversible only if the narrative number was never recorded.

### (e) Verdict

**KEEP WITH REWORDING**, minimal — change the tail of the §1 sentence from

> …as needed to resolve buyer type, consideration, dates, counts and conflicts.

to

> …as needed to resolve buyer type, consideration, dates and conflicts, and to cross-check counts
> (section 7.3).

Eight words. It keeps the addition, makes it a check rather than a source of truth, and points at the
section that actually governs. **DROP** is also defensible — the word is redundant — but the reword costs
nothing and closes the one reading that could hurt.

**Confidence: high** that the word is redundant and that §7.3+§3.2 cover the traps; **medium** on
whether any model would actually misuse it, since none did under the older, weaker text.

**Not checked:** deals beyond the three pilots for Reasons-vs-narrative conflicts of other shapes (e.g. a
Reasons total *larger* than the narrative, where the narrative is genuinely incomplete); whether Alex
would rather see the Reasons number in a dedicated Summary field than in prose.

---

## Item 12 — adviser dates (§5.4)

### (a) Current wording

§5.4, second paragraph, with the added sentence in bold (patch tag `B2-adviser`):

> Use **Adviser engaged** for an actual reported engagement or engagement approval, specifying which. If
> the filing only shows an adviser already providing services, use **Adviser service observed** at the
> earliest supported service date or window. First narrative mention is not proof of retention on that
> date. Long-standing service may have no ascertainable commencement date. **Use the earliest date the
> filing shows the adviser selected or acting for that client as the Working date, and list every
> disclosed date (selected, first advice, engagement letter) in Terms or outcome.**

Also in force: "Use **Adviser ended** for material termination and preserve a later new mandate. Approval
and subsequent contract signature can share a row recording both dates unless separate timing matters.
Deduplicate appearances, not real mandate changes." … "Never open a second adviser row for a renamed or
acquired firm already on the ledger." … "Flag an unclear client affiliation." Count is blank on adviser
rows (§7.2).

### (b) Evidence

**Alex's own rules.** Collection instructions §3.3 (his addition): "Collect information on the investment
bank engaged by the target… Most of the time, there will be only one advisor, but sometimes there are
several at once… there should be a primary advisor whom we should record. Otherwise, record all… Bid
Note: Record 'IB'. Date: Record the date of the event." §2 (his addition): "Financial advisors sign
agreements around the start of a deal process. Legal advisors are often retained for a long time, so
agreements have likely been signed much before the deal process starts – **there is no need to collect
the date but the name of a legal advisor should be collected**."

**His voice notes (his words).**
- Providence 13: "an investment bank that the target has retained as their financial adviser has two
  different names… the original bank that they've contacted has been acquired by a different bank later
  on. So to my mind, this is a single adviser."
- Mac-Gray 2: "there is some duplication of advisers being retained, for more specific details, please
  refer to the spreadsheet."
- Mac-Gray 9: "Goodwin Procter, a legal adviser, is recorded to have been retained at the end of the
  process… this legal adviser has been present at least since the beginning of the sale process… So it
  would be good to **at the very least record the first instance, May 9, in which this legal adviser is
  mentioned** in the deal background. We want to keep a clear ordering of events."
- Penford 6: "there is information, in early October, about legal advisers to the eventual winner
  Ingredion and to a large target shareholder, SEACOR. The AI records these legal advisers, but it
  doesn't record whom they are legal advisers to. It would be useful to record this information."
- Summary H: "**Exact dates are less interesting to me, but the order of events must be precise** because
  allocating a bid to a wrong round of bidding is not good."
- Summary J: "We have many duplicate rows. Advisors often get recorded multiple times, and it should be
  an easy fix to just **keep one line per advisor name**. Any time an affiliation of an advisor is
  unclear, this should be flagged for human verification."

**His red comment on Penford row 6467** (Deutsche Bank, `bid_note=IB`, `rough=07/30/2014`, entire row
red = his own):

> "It looks like DB was already **seleected on July 30**, and provided some **advice on Aug 11**, even
> though an **engagement letter was signed on Sep 11**. Which date should be used?"

He had all three dates, put **the earliest (selected)** in the operative date column, and asked the open
question. Item 12 answers it in the direction he already chose, and "list every disclosed date" preserves
the other two so the answer can be changed.

**Medivation row 6063** (J.P. Morgan, red): `precise=06/29/2016, rough=05/02/2016`, comment "Legal
advisor: Cooley. May 2: Pfizer's contact that was viewed well by the target. No mention of the IB
engagement earlier." Two adviser dates on one row.

**Saks row 6996** (Goldman Sachs, red): `rough=12/15/2012`, comment "For the past several years, Goldman
Sachs, one of Saks' longstanding financial advisors, has participated in these reviews. One such review
took place in December 2012." Long-standing service with no start date, dated at the earliest month it is
shown acting — exactly `Adviser service observed` with a window.

**The decisive one — Mac-Gray BofA, three red rows he wrote himself:**

| xl row | date | bid_note | comment |
|---|---|---|---|
| 6927 | 04/05/2013 | IB | — |
| 6929 | 05/15/2013 | **IB Terminated** | — |
| 6930 | 05/31/2013 | IB | "Sale process discussed since May 9; BofA offered some valuations on May 30 before being reemgaged as IB" |

He invented a bid-note value (`IB Terminated`) that the Chicago instructions do not contain, in order to
record the sequence. Against the filing: Board authorised management "to work with BofA Merrill Lynch" on
**April 5, 2013**; termination letter sent **May 15, 2013**; Board "unanimously approved the engagement of
BofA Merrill Lynch" on **May 30**; "On **May 31, 2013**, Mac-Gray entered into an engagement letter with
BofA Merrill Lynch". He also did **not** use BofA's actual earlier engagement date — "Mac-Gray engaged
BofA Merrill Lynch on October 23, 2012" for the 2011-2012 Discussions, a different mandate.

### (c) Hand application

**Does the terminate/re-engage sequence get three rows or one? Three.** Alex wrote three. Summary J
("one line per advisor name") is about spurious repeats of the same event; §5.4's "Deduplicate
appearances, not real mandate changes" is the correct reading, and his own `IB Terminated` row settles it.
All four old models independently produced the same three-row shape (`Adviser engaged` 10/23/2012,
`Adviser ended` 05/14–15/2013, `Adviser engaged` 05/30–31/2013 with wd 05/30), so the behaviour is stable
without the new sentence.

**The contradiction.** The added sentence has no antecedent scope: it says "the Working date", not "the
Working date of its first row". Read literally it applies to *every* adviser row, including the May 31
re-engagement — whose "earliest date the filing shows the adviser selected or acting for that client" is
April 5, 2013, or arguably October 23, 2012. That places the re-engagement **before its own termination
row**, violating §8.2 ("Working dates never decrease down the ledger") and §13.4. It also sits
immediately after "First narrative mention is not proof of retention on that date" and then mandates the
earliest date — a reader can take the new sentence as cancelling the warning it follows.

§13.4 would catch the order break as a check failure, but the likelier model response is worse: widen
`Date from` on the re-engagement row back to April so the Working date sits inside its own window. That
manufactures a false honest window, which no check catches and which is exactly the kind of silent
invented precision §3.3 forbids.

**The apparent "earliest vs midpoint" collision is not one.** The sentence selects *which event* anchors
the row; §8.1 then assigns the *day* inside that event's window. PetSmart: the board on 06/18/2014
"authorized the vetting and retention of a financial advisor" and met "together with a financial advisor"
(unnamed); the background says "**In July**, after interviewing several potential financial advisors, the
Company retained J.P. Morgan"; and elsewhere in the filing, "Pursuant to an engagement letter **effective
as of August 21, 2014**, the Company retained J.P. Morgan". §5.4 picks the July retention as the event
(not the August letter, which would put JPM's engagement after the 08/07 call *to* JPM and the 08/13
board meeting it attended — an order break); §8.1 rule 4 then assigns 07/16 as the window midpoint. Alex
wrote 07/01. Under his own summary H that 15-day difference is immaterial; the order is identical. All
four old models already produced exactly `07/01..07/31 wd=07/16` with the 08/21 letter noted, so the
sentence codifies what they do.

One live trap the sentence does not close: `glm` opened a separate row for "Unnamed financial advisor"
on 06/18/2014. The unnamed 06/18 adviser is demonstrably **not** J.P. Morgan (JPM was retained in July
"after interviewing several potential financial advisors"), so a model applying "earliest date shown
acting" loosely could instead date JPM to 06/18. One clause prevents both outcomes.

**Row counts per deal, revised instruction vs Alex's sheet.**

| Deal | Revised §5.4 produces | Alex's sheet | Delta |
|---|---|---|---|
| Providence | GHF `Adviser engaged` 01/27 (Board "approved… and the Company engaged GHF" that day); Hinckley Allen `Adviser service observed` 03/24 (first shown acting, "participated in all meetings of the Transaction Committee"); Simpson Thacher `Adviser service observed` ~08/10 (G&W's counsel); **no BMO row** (§5.4 renaming rule) | 1 row (GHF 01/27) + "Legal advisor: Hinckley Allen" as a comment | +2, both names he asked for; the BMO suppression is his Providence 13 |
| Mac-Gray | BofA `Adviser engaged` 10/23/2012 (2011-12 mandate) and/or `Adviser service observed` 04/05/2013; `Adviser ended` 05/15; `Adviser engaged` 05/30–31; Goodwin Procter `Adviser service observed` **05/09** (his Mac-Gray 9, by name and date); Kirkland & Ellis `Adviser service observed` ~09/25 (CSC/Pamplona's counsel) | 3 rows, all BofA; no legal advisers at all | +2 (5 rows: one BofA opener) to +3 (6 rows: both) |
| PetSmart | J.P. Morgan `Adviser engaged` July 2014 (wd 07/16, 08/21 letter in Terms); Wachtell Lipton `Adviser service observed` 06/18 | 1 row (JPM 07/01) + "Legal advisor: Wachtell Lipton" as a comment | +1 |

Row growth is one or two per deal and is entirely names Alex asked for by name (Goodwin Procter, the
bidder-side counsel of Penford 6). Count is blank on adviser rows, so none of it touches a tally. I do not
adjudicate whether BofA's first row should be 10/23/2012 or 04/05/2013: both precede the termination and
preserve the order he cares about, and the October engagement is the thing the May 15 termination row
terminates, so a model that records it is not wrong.

**The legal-adviser date question is compatible, not superseded.** The collection instruction says "there
is no need to collect the date but the name… should be collected"; Mac-Gray 9 asks for "the first
instance, May 9". Recording `Adviser service observed` at the earliest observed service date satisfies
both: the name is captured, and the date is a low-stakes observation, not a claim of retention —
which is precisely what "First narrative mention is not proof of retention on that date" already says.

### (d) Downstream risk and reversibility

Adviser rows carry no Count, no price, no formality, so they cannot corrupt a first-order variable
directly. The one real risk is **order**: an adviser row dated wrongly early sits among round-0 events and,
if a model then widens `Date from` to justify it, plants a fabricated window. Per Alex's H, order is the
thing he insists on. Fully reversible — one row per adviser per mandate, all disclosed dates retained in
Terms, so re-dating is a text re-read.

### (e) Verdict

**KEEP WITH REWORDING.** Replace the added sentence with:

> Use the earliest date the filing shows the adviser selected or acting on that mandate as the Working
> date of its first row for that mandate; a later engagement, termination or re-engagement keeps its own
> date. List every disclosed date (selected, first advice, engagement letter) in Terms or outcome. An
> adviser the filing describes only generically, such as "a financial advisor", is not evidence that a
> later-named firm was the one present.

That keeps Alex's revealed practice (Penford, PetSmart, Saks), keeps the Mac-Gray three-row sequence
intact and in order, keeps the July-retention anchor for PetSmart while leaving the day to §8.1, and
closes the unnamed-adviser trap. Everything else in §5.4 stands.

Note for the reader: the sentence two lines above it — "use **Adviser service observed** at the earliest
supported service date or window" — states the same rule for the observed-service case. The added
sentence is not a second rule; its only new work is to extend the earliest-date anchor to an
`Adviser engaged` row and (with the reword) to stop it reaching rows that are not the adviser's first on
that mandate.

**Confidence: high** that Alex wants the earliest date and the full date list (his Penford question plus
three consistent rows), and that the BofA sequence is three rows; **high** that the unscoped sentence is
misapplicable as written; **medium** on whether he would object to the extra one-to-two adviser rows per
deal — his voice notes ask for them, but he dislikes bloat and has not seen them in a ledger.

**Not checked:** the exact semantics of `bid_date_precise` on Alex's own red rows — it carries what look
like unrelated dates on several (Providence 6054 `precise=07/20` on an 08/04 event; Medivation 6063
`precise=06/29` against a 05/02 comment; Penford 6467 `precise=08/21` while his comment names Jul 30,
Aug 11 and Sep 11), so I treated `bid_date_rough` as his operative date per his own email ("In my edited
9 deals, I did not bother with this distinction and simply edited bid_date_rough"); the Penford,
Imprivata, Zep, Saks and STEC filings themselves are not in the repo, so those rows were read from the
spreadsheet and his comments only; whether the Providence Transaction Committee met before 03/24 (which
would move Hinckley Allen's first observed service earlier).
