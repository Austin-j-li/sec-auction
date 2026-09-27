# CHANGELOG: v1.14 candidate instruction

25 September 2026. Package A1 of [V114_SPEC.md](V114_SPEC.md) §7.1, revised the same day to resolve the findings of review R ([R_REVIEW.md](R_REVIEW.md); spec §7.2). §7 below lists each finding and its resolution; §1–§5 describe the text after those changes.

| File | SHA-256 |
|---|---|
| Base: [SEC_Deal_Ledger_Extraction_Instruction_v1.14_draft.md](SEC_Deal_Ledger_Extraction_Instruction_v1.14_draft.md) (288 lines, unchanged) | `f9595d7413149f86c074f1d4b9ef96a5a24b3d8dd9b6c11061b0bd6e889aea97` |
| Candidate: [SEC_Deal_Ledger_Extraction_Instruction_v1.14_candidate.md](SEC_Deal_Ledger_Extraction_Instruction_v1.14_candidate.md) (340 lines) | `c2d47a479d09eb46d0ab9fbf887568fcf13e972e2e11acbf08d5cdfab468ab27` |

Full diff: [v1.14_candidate.diff](v1.14_candidate.diff) (`diff -u` of the draft against the candidate). Hash line: [v1.14_candidate.sha256](v1.14_candidate.sha256).

**Reading this file.** "Draft → candidate" gives line numbers in the two files; "new" means inserted text. For C42 the draft lines named are those of the rules it replaces, not its position in the text. Sources: D1–D27 are the decisions in spec §1 (never the instruction's own sheet sections D1–D5); "§3 X" and "§4" are the spec's section-by-section changes; "§8: …" names a choice in spec §8; "Astra" means an item of Astra's §5 that spec §3 adopts as proposed, condensed. Audit references are to `systemic-audit/` (C = instruction cascade, E = spec review).

The candidate was built by line-anchored edits that assert each old text, so every line not listed below is byte-identical to the draft. The changes after review R were applied the same way, on top of the first edits. They added no line, so the candidate line numbers are those R reviewed.

## 1. Changes

| ID | Draft → candidate | Part | Change | Source |
|---|---|---|---|---|
| C01 | 3 → 3 | Header | "**Revision of 25 September 2026, v1.14.**", in v1.13.2's exact form (bold, final period, no "(draft)" or "(candidate)"). | §3 Header; §8: Header; audit E25 |
| C02 | 10, 14, 16, 20 → 10, 14, 16, 20 | A | Part A replaced by spec §2's text verbatim (quote markers removed): the departures sentence; "for the whole company" in item 1; item 3 rewritten; "change" for "upgrade". Lines 8, 12, 15, 17–19 were already identical. | D2; D4; D7; D14; §8: Part A wording |
| C03 | 24 → 24 | B | "One of three things" replaced by four kinds of value (reported, exact calculation, classification, inference). Inferred = Y marks an inferred event or an inferred material field, whose Note names the field. Ordinary application of a convention is a classification: the label E14's transitions give an inferred exit is one, though the exit itself is inferred and takes Inferred = Y (R2). | Astra (§3 B); D1; §3 E14 |
| C04 | 26 → 26 | B | False-precision list: "an exit label or reason that neither the filing nor E14's transition rules establish". | Astra (§3 B) |
| C05 | new → 28 | B | New paragraph "Evidence applies at its own date": a later passage establishes an earlier fact only if it dates it; no backward projection; an earlier row's value is not evidence except under express incorporation (E10). This is the one statement of date applicability; E10, E12 and Due diligence refer to it. | Astra (§3 B); D1 (note on express incorporation) |
| C06 | 28 → 30 | B | Quotation duty per field: an inferred event quotes its anchor; for an inferred field, the Note gives the anchor's page. | Astra (§3 B) |
| C07 | 32 → 34 | C | Read: build an inventory of dated acts, each with actor and scope. | Astra (§3 C) |
| C08 | 33 → 35 | C | Map: also fix participant and cohort relationships, keeping eligibility for a solicitation apart from admission to a stage. | Astra (§3 C) |
| C09 | 36 → 38 | C | After any correction, reconcile counts, round membership, prices, # references, deadline outcomes and process totals. | Astra (§3 C) |
| C79 | 54 → 56 | D1 | Item 9 Price high adds "Both stay blank on Other-scope bid rows (item 12).", so the blanks are met beside the price items; item 8's list stays the anchor and item 12 keeps the rule (R3). | D18; §3 D1 |
| C10 | 56 → 58 | D1 | Item 11 CVR/earnout: Y, Varies or blank. | §3 D1; D16 |
| C11 | 57 → 59 | D1 | Item 12 CVR/earnout value: only where CVR/earnout is Y. Separate sentence: "On Other-scope bid rows, leave Price low, Price high and CVR/earnout value blank, and give the amount, units and scope in the Note." Item 8's list ("Bid, Bid reaffirmed and Other-scope bid rows") is kept as the one definition of bid rows, so "on those rows" in items 10–19 still reaches Other-scope rows. | D18; §3 D1; §8: D18; audit C headline 1 |
| C12 | 63 → 65 | D1 | Item 18 Antitrust: Y, Varies or blank. | §3 D1; D16 |
| C13 | 67 → 69 | D1 | Item 22 Inferred: the event or a material field on the row (Part B). | Astra (§3 B, D1) |
| C14 | 68 → 70 | D1 | Item 23 Note: "for an inference, what is inferred and how you know" (was "on an inferred row"). | Astra (§3 B) |
| C15 | 81 → 83 | D2 | Bidder interest: an approach without making a Bid (E10); an approach that communicates an acquisition proposal, its price disclosed or not, is a Bid whose Note says it was the first contact. D2 refers to E10's definition and states no test of its own (R4). | Astra (§3 D2); §3 E10 |
| C16 | 88 → 90 | D2 | Exclusivity changed: a request made in a bid's own communication is coded on that bid row instead (E10). | D15; §8: D15 |
| C17 | 89 → 91 | D2 | Other material event examples add price feedback, a continuing bidder's missed submission (E14), and merger-of-equals talks while the sale role is unresolved (E1). | D10 (§3 D2); Astra (§3 E2); D17 and §8: Merger-of-equals talks |
| C18 | 93 → 95 | D2 | Exit labels: "each ends a period of participation". No new label. | D10 |
| C19 | 108 → 110 | D3 | Who was in: admitted bidders first; then, separately, parties eligible but not admitted, "still being received, not admitted" (kept), and continuing alternatives such as a partial offer; an NDA signed at some point does not admit a party. | Astra (§3 D3); D7 |
| C20 | 110 → 112 | D3 | Deadline outcome values in E9's first-that-fits order (R5): Extended, `Extended (late bid accepted)` (replacing `Late bids accepted`), Enforced, Passed without action, Unclear; `No deadline stated` only when none was set (kept). | D11; §3 E9 |
| C21 | 112 → 114 | D3 | Bids received: distinct whole-company bidder units, not bid rows; any Other-scope bids received in the round are named, with their bidders, separately in the same cell (R6). | D7; §3 D3; §8: Scope details; Astra |
| C22 | 113 → 115 | D3 | How it ended: name any bidder that missed a due date but continued. | D10; §8: continuing bidder's missed submission |
| C23 | new → 125 | D5 | "Acquirer type begins with Strategic, Financial, Mixed or Unknown (E3)." The field labels and parentheticals at line 121 are unchanged. | §3 D5; §8: Acquirer type; audit C §4 |
| C24 | 129 → 133–137 | E1 | Scope rewritten: the counts follow the whole-company contest; the Bid definition moves to E10 (E1 refers to it); Other-scope rows leave Price low, Price high and CVR/earnout value blank (D1; R7). New paragraph on partial-only parties (outside counts and screen, no exit rows, dated Other-scope bid rows with scope and amounts in the Note, last row's Note says how talks ended; unresolved scope kept out with a Question, merger-of-equals talks following their own rule (R8); change of scope at its date; a later partial proposal does not recast earlier involvement; switch closes whole-company participation, usually Withdrew; return gets Re-entered; break-up Question). New paragraph on merger-of-equals talks (no test of one's own; Other material event rows while the sale role is unresolved, each Note naming the act: an agreement, a proposal and its terms, the end of talks (R9); counterparty outside the contest; Question with the alternative map). | D7; D17; D18; §8: Scope details; §8: Merger-of-equals talks; Astra; audit E12 |
| C25 | 131 → 139 | E1 | Auction screen: independent prospective acquirers "of the whole company"; partial-only parties' agreements do not count; where the result turns on a party whose scope or sale role is unresolved, such as a merger-of-equals counterparty, the entry is Uncertain (R10). Format unchanged. | D7; D17; §3 E1 ("Uncertainty is kept"); Astra |
| C26 | 135 → 143 | E2 | A change in an offer's price, consideration or a bidder's commitments (E10's terms, so the target's termination fee stays in a Note) earns a row even when negotiated through drafts (R11), taking priority over the legal-negotiation exclusion; unchanged document exchanges stay out; a target requirement and a bidder's acceptance or counter are separate events; price feedback and explanatory information earn rows when they pass the test. | D13; Astra |
| C27 | 143 → 151–153 | E3 | Entry means entry into the whole-company contest; a party partial from the start does not enter, and neither does a merger-of-equals counterparty while its sale role is unresolved (R12). New "Participation" paragraph: participation, eligibility, admission and reserve or alternative status kept apart (the one definition of participation); an NDA signed in an interval does not prove eligibility at a deadline inside it. | D7; D17; Astra |
| C28 | 147 → 157 | E3 | A later-named cohort member "is not entered again". | Astra |
| C29 | 149 → 159 | E3 | Never get an exact number of non-submitters by subtracting bids from a group not wholly eligible at that deadline. | Astra; D10 |
| C30 | 153 → 163 | E4 | Count is the number of resulting live whole-company units. | D7 |
| C31 | 159 → 169 | E5 | (a): an existing NDA alone does not show that negotiations were continuing. | Astra |
| C32 | 160 → 170 | E5 | (b): the three-month test fixes where a new process starts; it does not show that a participant was inactive (E14). | Astra; §8: E5(b) |
| C33 | 163 → 173 | E5 | Markers close whole-company participation; each period closes once; a return does not by itself start a new process; unresolved merger-of-equals continuity gets the alternative map in the process Question. | D7; D17; Astra |
| C34 | 171 → 181 | E6 | Deleted "opens a distinct information stage tied to new offers". Added: deliberate reopening of rival solicitation after a suspension opens a round (unless E5 starts a new process); a reopened round is dated at the outreach, never the authorization, with an undated outreach's Sort date inside its window after the authorization day; count each stage once; an unannounced round's Round opened row has Inferred = Y; routine follow-up and one bidder's unsolicited return continue the round. | D8; Astra; §8: Round dates; §8: D8's wording; audit E10 |
| C35 | 173 → 183 | E6 | Round 1 opens at the first sale stage the target organized, including substantive bilateral negotiation; "Use, in order:" becomes "Use the earliest supported of:"; the decision-date route is kept; a preliminary unsolicited approach alone does not open it; later broad outreach does not demote an earlier requested-bid stage; approaches and unsolicited proposals made before round 1 opens are round 0, so E6 agrees with E11's rule for an unsolicited bid made during a final round (R13). | D8; Astra; §8: Round dates; §8: An unsolicited bid in a final round |
| C36 | 177 → 187 | E6 | Finality describes the procedure the target announced or visibly put in place, not which bid came last or whether a bid is Formal (E11). | D8; Astra |
| C37 | 181 → 191 | E7 | Sending, executing and supplying information are separate facts, each dated on its own evidence; look in the annexes for dated execution evidence. A reused agreement's first row becomes the party's entry only where E3 counts one (R14). | Astra; D7 |
| C38 | 198 → 208 | E8 | Sort date's decision-day rule excepts undated reopened outreach, which takes the window's midpoint (rounding earlier), or the day after the authorization where that midpoint is not after it or the authorization is the only known bound (E6; R15); where supported order conflicts with reported days, keep the days and raise a Question; a Round opened row is the first row of its round in the ledger (the checker's `round.opening_order`). | D8; §3 E6; Astra; §8: Round dates |
| C39 | 204 → 214–222 | E9 | Outcomes as a first-that-fits list: Extended (even after evaluation); Extended (late bid accepted) for an overdue required response considered with no new date; Enforced (invited improvements with no new date are bargaining within the round; Enforced does not mean bargaining ended); Passed without action; Unclear. Then: record the facts before choosing; no inferred invitation from banker conversations; differing outcomes in Notes or a Question; a missed response and an exit are separate questions. | D11; §8: D11 and a new date after evaluation; Astra; audit E26 |
| C40 | 208 → 226 | E10 | The one definition of a Bid: a communicated acquisition proposal (oral, conditional, non-binding, pre-NDA, unsuccessful, undisclosed-price), with E1 deciding scope; a market reference, hypothetical ceiling, threshold refusal or valuation statement is not by itself a proposal, and ambiguity gets a Question. One offer communication is one row; the exception for alternative structures is kept: Bid rows for whole-company alternatives, Other-scope bid rows for partial ones. | Astra; §8: Alternative structures; audit C §2 items 2 and 25; audit E12 |
| C41 | 208 → 228 | E10 | Every communicated material revision of price, consideration or bidder commitment is a Bid row, including same-price changes to conditions, funding, a reverse termination fee or bidder or sponsor liability; a material same-price revision takes Bid, not Bid reaffirmed. The target's termination fee goes in the Note of the row where it is agreed or changed, else of Merger agreement signed. Signing adds no price row. | D13; §8: The target's termination fee; Astra |
| C42 | 224, 210 → 230 | E10 | Express incorporation replaces line 224's copy rule and line 210's state carry: carry only the terms the filing says were carried, within the stated scope, Note "Terms: as #n (p. x)" naming what was carried; judge status facts such as diligence at the new date. Anything else the filing does not address is Not stated in Stock %, Due diligence, Financing, Regulatory and Exclusivity, and blank in CVR/earnout, CVR/earnout value and Antitrust; on a same-price revision the price cells hold the earlier price only where the filing shows it unchanged, noted like any carried term, and otherwise stay blank (R16). | D1 (note: express incorporation replaces TAXONOMY_DRAFT5 §3.3(a)–(b)); §3 E10; §3 D1; D13; Astra |
| C43 | new → 232 (replaces 230's two-row rule; see C51) | E10 | Exclusivity is a term, not a condition or a bidder commitment (Part A), and a request for it is not by itself a material revision (R17); a request in the same communication as a bid row (Bid, Bid reaffirmed or Other-scope bid) is coded on that row, first bid or revision, with no Exclusivity changed row (R18); a later request with no other change is an Exclusivity changed row, never a same-price Bid row, and does not recode the bid; a later bid codes Exclusivity from its own communication, with carry-over only by express incorporation. | D15; §8: D15; D27; audit E2 |
| C44 | 210 → 234 | E10 | Bid reaffirmed keeps its gate, standing price and Formality = Formal; "as they stand at that date, updated by anything the filing reports by then" replaced by coding "its other columns by the same evidence and date rule as a revision". | D1 (express incorporation); Astra |
| C45 | 220 → 244 | E11 | The unlabelled Heavy example ("record Formal with Conditions = Heavy") removed: "a Formal bid stays Formal at any Conditions level". "A letter alone" added to what does not change the label (new text). | §4 (line 220); §9.1; Astra |
| C46 | new → 246 | E11 | A price-only revision is Formal only on its own basis or where the bidder expressly refers back to earlier Formal terms; negotiating from an earlier markup does not make it Formal; later document work cannot show earlier engagement; an unsolicited bid during a final round carries that round's number, but route 2 applies only if it answers that solicitation. | D9; Astra; §8: An unsolicited bid in a final round |
| C47 | 224 → 250 | E12 | "The five condition columns" replaced by the named columns (Due diligence, Financing, Regulatory, Antitrust, Exclusivity); coding at the bid's date (Part B), carrying earlier terms only by express incorporation (E10); financing signed after a bid does not make it Committed. Copy rule removed (see C42). The outside-background timing sentence is kept. | §4 Exclusivity and Dates; D1; audit C §2 item 26 |
| C48 | 226 → 252 | E12 | Due diligence: a later passage counts only if it dates the fact (Part B); Not begun needs affirmative support (no data-room mention is not enough; an NDA alone does not show diligence began). "Substantive diligence finished … is Incomplete" kept. | §4 (Astra); §8: Diligence (D27) |
| C49 | 227 → 253 | E12 | Financing precedence: "Contingent, unless the bid is stated not to be subject to a financing condition"; that statement makes the bid Committed over the whole Contingent list (unsigned or draft letters, highly confident support); the Note records the lender documents and any reverse termination fee. Walk-away wording of Committed kept. | D5; §8: Consequence of D5 (D27) |
| C50 | 228 → 254 | E12 | Regulatory: a bare approval requirement is Not stated and kept in the Note. | D3 (§4) |
| C51 | 230 → 256 | E12 | Exclusivity: "including a bidder that stops when refused" deleted; a later refusal or departure does not show an earlier request was a condition unless the filing connects them; "codes that bid and also gets its own Exclusivity changed row" replaced by a pointer to E10; a separate grant, extension or ending is its own row; an express statement that none was sought goes in the Note (no "No" value); exclusivity is a term and never changes Formality or the level. | D14; D15; §4 |
| C52 | 232 → 258 | E12 | "In every column" → "In each column"; Not stated means the filing reports nothing for this bid that supports another value, and a statement that fits no value (a bare statement that approvals are required, or that no exclusivity was sought) leaves the column Not stated and goes in the Note (R19); "A Y in CVR/earnout or Antitrust on a cohort row means every member carries it; if only some do, Varies." | D16; D3; §3 D1; §4 Exclusivity |
| C80 | 236 → 262 | E12 | None: "Regulatory not Concern (silence stays Not stated)" in place of "no regulatory concern", which could be read as the value No concern (R20). The definition is otherwise kept. | D3; D6; §9.1 bullet 3 |
| C53 | 237 → 263 | E12 | Light's "expedited" diligence applies only where H2 does not. Light keeps both routes. | D14; D6; §8: D14 and H2 |
| C54 | 238 → 264 | E12 | Heavy triggers labelled H1 (Financing Contingent), H2 (substantive remaining diligence, or a stated period of two weeks or more for remaining diligence, even if called expedited; replaces "a stated multi-week period"), H3 (a stated bidder right to reprice, an unresolved transaction-specific prerequisite, or an identified obstacle to completion for this bid). | §4; D3; D14 |
| C55 | 239 → 265 | E12 | Unclear: "a cohort's members do not all support one level" (was "differ"). | §4 Cohorts |
| C56 | new → 267 | E12 | H2 and H3 limits: exclusivity, time to signing and negotiation periods are not diligence periods; an express confirmatory-or-limited statement defeats H2, the period test included; open diligence without substance or a period is not H2 (see Unclear). H3's obstacle is one the bid depends on; ordinary approvals, routine documentation, generic risk language, a CVR/earnout and exclusivity do not qualify; a weighed regulatory risk, including doubt about closing, is Concern and is H3 only if the bid depends on it; Regulatory = Concern does not by itself meet H3, and the level follows the other evidence (R21). | §4; D3; D14; §8: D14 and H2; §8: Concern and H3 (D27) |
| C57 | new → 269 | E12 | Cohort level: common level only when every member supports it, else Unclear with the composition in the Note; one Heavy member does not make the cohort Heavy; cohort-wide Financing = Contingent is Heavy (H1). | §4 Cohorts (Astra) |
| C58 | 241 → 271 | E12 | New sentence: "A CVR/earnout is consideration, not a condition: by itself it neither makes a bid Heavy nor prevents None." The Note names the Heavy trigger (H1, H2 or H3). | D4; §4 |
| C59 | new → 273–289 | E12 | Examples table: a condensed version of spec §4's table in neutral wording, with no filing phrase or number: "repeats its earlier terms except the price" (not "terms previously proposed"), "several weeks of exclusivity" (not "five weeks"), "Three weeks expressly required" (for "Thirty days"). The CVR row reads "the CVR does not change the Conditions level" (R22) and the confirmatory-only row "Light, unless H1 or H3 applies" (R23). Every Heavy entry names H1 or H2. | §8: Examples; §4; audit E9 |
| C60 | 245 → 293 | E13 | Price cells: "On Other-scope bid rows, both stay blank (D1)." | D18 |
| C61 | 247 → 295 | E13 | A bid stated as a total or an exchange ratio fills the price cells, on a Bid or Bid reaffirmed row, only from a stated per-share figure (was the unscoped "per-share cells"; R7); a package value goes in the price cells "of a Bid or Bid reaffirmed row"; subtract a contingent part only from compatible figures, never a maximum from a package on another basis; where parts cannot be separated, price cells blank, package and basis in the Note, and a Question if it matters. The reference example is now neutral ("Ref: $20.00 close 02/08/2019; 25% premium"); "record only the prices the filing states, not a price history". | D18; Astra; §8: A package that cannot be split (D27); §3 rules for writing (line 247); D23; audit C headline 7 |
| C62 | 249 → 297 | E13 | Stock % range example "40–60" (was "50–75"); Varies covers partial reporting (E12). | §3 rules for writing (line 249); audit E31; D16 |
| C63 | 251 → 299 | E13 | CVR/earnout value is filled only where CVR/earnout is Y (a Varies row puts the amounts in the Note) and is blank on Other-scope bid rows. | §3 D1; D16; D18 |
| C64 | 255 → 303 | E14 | Dropped by target: leaving a bidder out of one stage while the target keeps it in reserve or in continuing discussions is not an exit. | Astra |
| C65 | 256 → 304 | E14 | Withdrew also covers leaving the whole-company contest by switching to a partial offer (E1). | D7; §8: Scope details (D27) |
| C66 | 257 → 305 | E14 | Did not submit: a non-submission that ends participation, reported or inferred when the bidder is never mentioned again and not carried forward. "Not necessarily permanent" deleted. | D10 |
| C67 | 258 → 306 | E14 | Not selected at signing "is not a withdrawal". | Astra |
| C68 | 260 → 308–312 | E14 | New: a bidder that misses a due date but continues gets no exit and no re-entry; the miss goes in the Deadline or Deadline revised row's Note and the Rounds line's How it ended, with an Other material event row only if it passes the row test. Exits only for entrants to the whole-company contest: a partial-only party gets none, and its last row's Note says how its talks ended; leaving the whole-company contest is not leaving a partial transaction; Re-entered covers a return from a partial offer. New: actor, timing and reason each judged on its own evidence; record the exit and its evidence, and infer no valuation or exact exclusion date from a disappearance. | D10; D7; §8: continuing bidder's missed submission; Astra; audit C §2 item 27 |
| C69 | 262 → 314 | E14 | Inferred transitions apply to whole-company participants: infer closure at the first transition that applies, unless the filing shows the participation continuing past it (a continuing solicitation, a still-active offer, ongoing diligence or explicit reserve status after that point), so the check does not block the exclusivity and signing transitions (R24); "Exit reason Not stated unless the filing reports one". | D7; D10; Astra; §3 E14; §3 F.3 |
| C70 | 264 → 316 | E14 | Inferred Did not submit requires that the bidder is neither mentioned again nor carried forward by the narrative (R25); the arithmetic subtracts only from the group eligible at that deadline and gives a bound ("Count: at least 4; at least 12 invited, 8 submitted"); the lifetime-signer subtraction example is removed. | D10; Astra |
| C71 | 265 → 317 | E14 | Inferred Dropped by target excepts reserve status and continuing discussions. | Astra |
| C72 | 271 → 323 | E14 | Live whole-company bidder units. | D7 |
| C73 | 273 → 325 | E14 | The first four Exit reasons record how the filing compares the bidder's value with a benchmark; a reported comparison stays in the Note even when Exit reason is Not stated. | Astra |
| C74 | 279 → 331 | F | A recommendation may be to keep a range or an unknown, never an invented point; the Question column says whether the issue is a source gap, a permitted inference, a convention choice or a researchers' decision (no new column); related rows grouped where readable. The judgment rule is unchanged. | D12; Astra |
| C75 | 281 → 333 | F | The final audit looks for omitted events as well as wrong rows. | Astra |
| C76 | 283 → 335 | F | F.1 reconciles participation and live units for the whole-company contest; partial-only parties are accounted for by their own rows. | D7 |
| C77 | 285 → 337 | F | F.3: an inferred exit's label follows E14's transition rules and its Exit reason is Not stated unless the filing reports one. | Astra (§3 F.3) |
| C78 | 286 → 338 | F | F.4 adds: every Other-scope bid row leaves Price low, Price high and CVR/earnout value blank. | D18 |

## 2. Spec §3.1 lines

| Part | Draft line | Status | Candidate | Change or reason |
|---|---|---|---|---|
| A | 20 | changed | 20 | C02 ("upgrade" → "change") |
| B | 24 | changed | 24 | C03 |
| B | 26 | changed | 26 | C04; C05 follows it |
| B | 28 | changed | 30 | C06 |
| B | 67 | changed | 69 | C13 |
| B | 68 | changed | 70 | C14 |
| D1 | 53 | confirmed unchanged | 55 | Item 8's list stays the one definition of bid rows, which "on those rows" in items 10–19 anchors to; the Other-scope blanks are a separate sentence (C11). |
| D1 | 54 | changed | 56 | C79: "the same" still inherits item 8; a pointer to item 12's blanks follows (R3). |
| D1 | 55 | confirmed unchanged | 57 | Stock % stays required on Other-scope rows (§8: D18). |
| D1 | 56 | changed | 58 | C10 |
| D1 | 57 | changed | 59 | C11 |
| D1 | 58–62 | confirmed unchanged | 60–64 | The anchor still resolves; the value lists equal the checker's `FORMALITY`, `CONDITIONS`, `DUE_DILIGENCE`, `FINANCING`, `REGULATORY`. |
| D1 | 63 | changed | 65 | C12 |
| D1 | 64 | confirmed unchanged | 66 | Values equal `EXCLUSIVITY`; which row carries a request is E10's rule (C43). |
| D2 | 81 | changed | 83 | C15 |
| D2 | 88 | changed | 90 | C16 |
| D2 | 89 | changed | 91 | C17 |
| D2 | 93 | changed | 95 | C18 |
| D3 | 108 | changed | 110 | C19 |
| D3 | 110 | changed | 112 | C20 |
| D3 | 112 | changed | 114 | C21 |
| D3 | 113 | changed | 115 | C22 |
| E1 | 129 | changed | 133–137 | C24 |
| E1 | 131 | changed | 139 | C25 |
| E3 | 143 | changed | 151–153 | C27 |
| E4 | 153 | changed | 163 | C30 |
| E5 | 160 | changed | 170 | C32 |
| E5 | 163 | changed | 173 | C33 |
| E6 | 171 | changed | 181 | C34 |
| E6 | 173 | changed | 183 | C35 |
| E8 | 198 | changed | 208 | C38 |
| E10 | 208 | changed | 226, 228 | C40, C41 |
| E10 | 210 | changed | 234 | C44; its state carry is replaced by C42 (230) |
| E11 | 220 | changed | 244 | C45 (also the E12 row below); C46 follows it |
| E12 | 220 | changed | 244 | C45: the Heavy example is removed rather than labelled |
| E12 | 224 | changed | 250 | C47 (copy rule replaced by C42) |
| E12 | 226 | changed | 252 | C48 |
| E12 | 227 | changed | 253 | C49 |
| E12 | 228 | changed | 254 | C50; the Concern/H3 boundary is in C56 |
| E12 | 230 | changed | 256 | C51; its two-row rule is replaced by C43 (232) |
| E12 | 232 | changed | 258 | C52 |
| E12 | 237 | changed | 263 | C53 |
| E12 | 238 | changed | 264 | C54; C56 and C57 follow the level list |
| E12 | 239 | changed | 265 | C55 |
| E12 | 241 | changed | 271 | C58; C59 follows it |
| E13 | 245 | changed | 293 | C60 |
| E13 | 247 | changed | 295 | C61 |
| E13 | 249 | changed | 297 | C62 |
| E13 | 251 | changed | 299 | C63 |
| E14 | 255 | changed | 303 | C64 |
| E14 | 256 | changed | 304 | C65 |
| E14 | 257 | changed | 305 | C66 |
| E14 | 260 | changed | 308–312 | C68 |
| E14 | 262 | changed | 314 | C69 |
| E14 | 263 | confirmed unchanged | 315 | Blank line. |
| E14 | 264 | changed | 316 | C70 |
| E14 | 265 | changed | 317 | C71 |
| E14 | 266 | confirmed unchanged | 318 | Displacement by a rival's executed exclusivity; now scoped to whole-company participants by the lead-in (C69), which does not block it for a rival whose offer is still active (R24); "a request for exclusivity drops no one" already agrees with D15. |
| E14 | 267 | confirmed unchanged | 319 | Closure at signing; scoped by the lead-in (C69), which does not block it for a bidder last seen in diligence (R24); agrees with "Signing with another bidder is not a voluntary withdrawal" (C67). |
| E14 | 268 | confirmed unchanged | 320 | Blank line. |
| E14 | 269 | confirmed unchanged | 321 | Named-versus-residual reconciliation already matches E3's cohort rule (C28). |
| E14 | 271 | changed | 323 | C72 |
| F | 283 | changed | 335 | C76 |
| F | 285 | changed | 337 | C77 |
| F | 286 | changed | 338 | C78 |

## 3. Every line audit C §1 names

All 121 draft lines named in audit C §1 (its draft-line, cascade and notes columns, ranges expanded) are listed here.

**Changed (74 lines):**

| Draft | Candidate | Change | | Draft | Candidate | Change |
|---|---|---|---|---|---|---|
| 3 | 3 | C01 | | 177 | 187 | C36 |
| 10 | 10 | C02 | | 181 | 191 | C37 |
| 14 | 14 | C02 | | 198 | 208 | C38 |
| 16 | 16 | C02 | | 204 | 214–222 | C39 |
| 20 | 20 | C02 | | 208 | 226, 228 | C40, C41 |
| 24 | 24 | C03 | | 210 | 234; 230 | C44; C42 |
| 26 | 26 | C04, C05 | | 220 | 244–246 | C45, C46 |
| 28 | 30 | C06 | | 224 | 250; 230 | C47; C42 |
| 32 | 34 | C07 | | 226 | 252 | C48 |
| 33 | 35 | C08 | | 227 | 253 | C49 |
| 36 | 38 | C09 | | 228 | 254 | C50 |
| 54 | 56 | C79 | | 230 | 256; 232 | C51; C43 |
| 56 | 58 | C10 | | 232 | 258 | C52 |
| 57 | 59 | C11 | | 236 | 262 | C80 |
| 63 | 65 | C12 | | 237 | 263 | C53 |
| 67 | 69 | C13 | | 238 | 264 | C54 |
| 68 | 70 | C14 | | 239 | 265–269 | C55–C57 |
| 81 | 83 | C15 | | 241 | 271–289 | C58, C59 |
| 88 | 90 | C16 | | 245 | 293 | C60 |
| 89 | 91 | C17 | | 247 | 295 | C61 |
| 93 | 95 | C18 | | 249 | 297 | C62 |
| 108 | 110 | C19 | | 251 | 299 | C63 |
| 110 | 112 | C20 | | 255 | 303 | C64 |
| 112 | 114 | C21 | | 256 | 304 | C65 |
| 113 | 115 | C22 | | 257 | 305 | C66 |
| 129 | 133–137 | C24 | | 258 | 306 | C67 |
| 131 | 139 | C25 | | 260 | 308–312 | C68 |
| 135 | 143 | C26 | | 262 | 314 | C69 |
| 143 | 151–153 | C27 | | 264 | 316 | C70 |
| 147 | 157 | C28 | | 265 | 317 | C71 |
| 149 | 159 | C29 | | 271 | 323 | C72 |
| 153 | 163 | C30 | | 273 | 325 | C73 |
| 159 | 169 | C31 | | 279 | 331 | C74 |
| 160 | 170 | C32 | | 281 | 333 | C75 |
| 163 | 173 | C33 | | 283 | 335 | C76 |
| 171 | 181 | C34 | | 285 | 337 | C77 |
| 173 | 183 | C35 | | 286 | 338 | C78 |

Line 121 (→ 123) is unchanged, with C23 inserted after it; it is listed below.

**Confirmed unchanged (47 lines):**

| Draft | Candidate | Reason |
|---|---|---|
| 35 | 37 | Reread already checks each paragraph both ways (§3 C: no change). |
| 40 | 42 | "Exactly four sheets" stays: the SEC link and provenance are added by the pipeline (D20); "Stock % = 0" was already there. |
| 44 | 46 | D1's lead paragraph stays; the Round opened ordering rule is in E8 (C38). |
| 53, 55 | 55, 57 | See §2 above (the bid-row anchor). |
| 58, 59, 60, 61, 62 | 60–64 | See §2 above. |
| 64 | 66 | See §2 above. |
| 86 | 88 | The Round opened label stays; its first-row rule is in E8 (C38). |
| 90 | 92 | "The price may be undisclosed" agrees with E10's Bid definition. |
| 94 | 96 | Re-entered stays; the return from a partial offer is covered in E1 and E14 (C24, C68). |
| 96 | 98 | Merger agreement signed stays; E10 points to it for the target's termination fee and says signing adds no price row (C41). |
| 104, 105, 106, 107 | 106–109 | Rounds column names equal the checker's `ROUND_COLUMNS`. |
| 109 | 111 | "None stated" still pairs with No deadline stated (checker `rounds.no_deadline_pair`). |
| 111 | 113 | The Finality values stay (`FINALITY`); their meaning is sharpened in E6 (C36). |
| 117 | 119 | D4's seven columns stay (`QUESTION_COLUMNS`); the issue type goes in the Question column and the recommendation rule in F (C74). |
| 121 | 123 | Field labels and parentheticals stay byte-identical (`FACT_FIELD_OPTIONS`); the Acquirer type values follow as a separate sentence (C23). |
| 137 | 145 | Information-access differences matter for any live bidder (Part A item 5); E1 limits only the counts. |
| 157 | 167 | E5's lead stays. |
| 158, 162, 170, 172, 215, 219, 263, 268 | 168, 172, 180, 182, 239, 243, 315, 320 | Blank lines. |
| 161 | 171 | E5(c) stays; E6's reopened-round trigger defers to it ("unless E5 starts a new process"). |
| 169 | 179 | E6's round definition stays. |
| 202 | 212 | E9's lead stays; it already says a superseded date gets no Deadline row and no outcome. |
| 214 | 238 | E11's lead stays. |
| 216, 217, 218 | 240–242 | E11's three routes stay; the limits on price-only revisions, later documents and unsolicited final-round bids follow as a new paragraph (C46). |
| 229 | 255 | Antitrust stays; Varies on the marker is in E12's cohort paragraph (C52); "Filled only where Regulatory is No concern, Concern or Varies" matches the checker. |
| 234 | 260 | The order Heavy → None → Light → Unclear stays (§4). |
| 266, 267, 269 | 318, 319, 321 | See §2 above. |
| 277 | 329 | F's required map and deadline Questions stay (D12); the merger-of-equals, unresolved-scope and break-up Questions are "the Questions the conventions call for". |
| 284 | 336 | F.2 stays. |

## 4. Drafting choices the spec left to A1

1. **Header date.** The day the text was frozen after R's fixes (spec §3 Header), in v1.13.2's form. `date -u` gave 25 September 2026 when the fixes were applied, the same day the candidate was first written, so the header text did not change (R1); the hash changed with the fixes.
2. **The Other-scope blanks in D1** are a separate sentence at the end of item 12, after the three amount columns, so item 8's list stays the anchor for "on those rows". Item 9 points to that sentence (C79, R3).
3. **Acquirer type** is "begins with Strategic, Financial, Mixed or Unknown (E3)", a separate sentence after the field list. The checker accepts a qualifier after the value (`starts_with_canonical`), so "begins with" states what it enforces.
4. **Neutral figures:** "Ref: $20.00 close 02/08/2019; 25% premium" (2019 dates, like the instruction's other examples); Stock % range "40–60"; the bound example "Count: at least 4; at least 12 invited, 8 submitted".
5. **Examples table.** A markdown table in E12 after the level rules. Spec §4's "Thirty days" became "Three weeks", because I could not confirm it is not from a filing (I did not read filings) and three weeks is above the two-week threshold. The CVR-only row names the four Not stated columns, since Antitrust is blank, not Not stated.
6. **Merger of equals.** The "no control-surrendered-or-premium screen" is phrased as "do not settle the sale role with a test of your own, such as who gains control or whether a premium is paid", because the instruction never had such a screen to remove.
7. **Undated reopened outreach.** E6 asks for a Sort date inside its window after the authorization day. After R15, E8 prescribes the day: the window's midpoint (rounding earlier), or the day after the authorization where that midpoint is not after it or the authorization is the only known bound, so the general fallback can never land on the authorization day.
8. **D3's Deadline outcome list** gives the five values in E9's first-that-fits order (R5), so the two lists cannot be read as different precedences.
9. **The unsolicited final-round bid** is stated in E11 (with a pointer to E6), as spec §3 E11 places it, and is not widened to every open round.
10. **Participation** gets its own paragraph in E3, the single definition that D3, E14 and F.1 use.
11. **The inferred-closure reason** (spec §3 B) is resolved in F.3 (C77) and E14 line 262 (C69), not by a new sentence in B. B's false-precision list now excepts E14's transitions (C04).
12. **Not added:** a reverse fee in D1 item 23's Note list (audit C [I]; E12 Financing already puts any reverse termination fee in the Note); a "blank on every other row" sentence in D1; any statement about the pipeline's SEC link (D20: the model never writes it).
13. **Bid definition.** E1 keeps the scope rule and refers to E10; E10 holds the one definition. The "include pre-NDA, oral, unsuccessful and undisclosed-price proposals" list moved from E1 to E10. D2's Bidder interest also refers to it and states no test of its own (C15, R4).

## 5. Self-check against spec §9.1

Restated after the changes in §7.

| §9.1 bullet | Result |
|---|---|
| One definition each of Formality (E11), Conditions (E12), scope (E1), participation (E3), Bid (E10), date applicability (B); replaced shortcuts removed | Met. Formality at 238–246, Conditions at 250–271 (the columns named at 250), scope at 133–139, participation at 153, Bid at 226 and date applicability at 28. D2 now refers to E10's Bid definition instead of stating a priced-proposal test (83, R4), and E2 uses E10's terms, price, consideration or a bidder's commitments (143, R11). Scope reaches the merger-of-equals counterparty in E1's precedence (135, R8), the auction screen (139, R10) and E3's entry rule (151, R12). Removed, not wrapped: the three-things rule, "on an inferred row", "not necessarily permanent", "including a bidder that stops when refused", "opens a distinct information stage tied to new offers", "Use, in order", the lifetime-signer subtraction, "the five condition columns", the copy rule (224), the reaffirmation state carry (210), the unlabelled Heavy example (220), "also gets its own Exclusivity changed row", "a stated multi-week period"; and, after R, "without a priced proposal", "economic terms", "per-share cells", "for this rule", "Conditions unchanged", "partial-only bidders" in Bids received and "first check for" in E14. A grep finds none of them. |
| Value lists agree with the checker | Met, by a script run against a copy of the integrated checker 1.7 (`check_lean.py`, SHA-256 `41ea880f…c49c`): 42 of 42 checks pass. The re-check (R_REVIEW.md) repeated it against the finalized checker (`fa953928…607f`): 58 of 58 pass. D1 items 13–19 equal `FORMALITY`, `CONDITIONS`, `DUE_DILIGENCE`, `FINANCING`, `REGULATORY`, `EXCLUSIVITY`; CVR/earnout and Antitrust are Y, Varies or blank (`MARKER`); CVR/earnout value only with Y (D1, E13); D3 and E9 give `DEADLINE_OUTCOMES_V114`, now in the same first-that-fits order (R5), and D3 adds `No deadline stated` (together equal to `choice_lists("v1.14")["Deadline outcome"]`); Stock % codes equal `STOCK_CODES` and "40–60" matches `STOCK_RANGE_RE`; exit reasons equal `EXIT_REASONS`; D2 labels equal `EVENTS`; Type and Acquirer type values equal `TYPES`; Initiation values equal `INITIATION`; the D1, D3 and D4 columns equal `LEDGER_COLUMNS_V114`, `ROUND_COLUMNS` and `QUESTION_COLUMNS`; all 17 D5 labels are accepted by `FACT_FIELD_OPTIONS`; every other `choice_lists("v1.14")` list equals the instruction's, and it offers no All cash. Price low, Price high and CVR/earnout value are never sent to Not stated: E10's default names the columns that take Not stated and those left blank, and a same-price revision's price cells hold the earlier price only where the filing shows it unchanged (230, R16). E1 and E13 name the price cells, so Stock % stays required on Other-scope rows (133, 295, R7). The one intended difference: the instruction omits `Late bids accepted`, which the checker still accepts in a v1.14 workbook, with a warning (S1). |
| Unknown never a negative; regulatory silence never No concern; Light only by its two routes | Met. Not stated means the filing reports nothing for this bid that supports another value; a statement that fits no value, such as a bare statement that approvals are required or that no exclusivity was sought, stays Not stated and goes in the Note; a negative value needs the filing's support (258, R19). Not begun needs affirmative support (252). None reads "Regulatory not Concern (silence stays Not stated)" (262, R20). Light keeps both routes, with "expedited" limited by H2 (263). |
| No text makes Concern, a CVR or exclusivity Heavy; every Heavy example names H1–H3 | Met. Lines 16, 256, 267 and 271 say the opposite, and 267 adds "Regulatory = Concern does not by itself meet H3; the level follows the other evidence" (R21). The Heavy entries in the table name H1 or H2 (280, 283); the confirmatory-only row names only H1 or H3 (279, R23); line 220's example is removed; the cohort rule names H1 (269). |
| One evidence and date rule; no wholesale copying at 224 or 210 | Met. B's date paragraph (28) and E10's express incorporation (230), which now also settles a same-price revision's price cells (R16); E12 (250) and Bid reaffirmed (234) refer to them. The CVR example no longer reads as a copy of the earlier level (277, R22). |
| D7 reaches E1, E3, E4, E5, D3, E14 (256, 260, 262–269, 271) and F.1; D10 reaches D2 and E14 (257, 264); D11 reaches D3 and E9; D18 reaches D1, E1, E13 (245, 247, 251) and F.4 | Met (D7: C19, C21, C24, C25, C27, C30, C33, C37, C65, C68, C69, C72, C76; D10: C17, C18, C22, C66, C68, C69, C70; D11: C20, C39; D18: C11, C79, C24, C60, C61, C63, C78). After R, Bids received names Other-scope bids, not only partial-only bidders (114, R6); E14's continuation test no longer blocks its own exclusivity and signing transitions (314, R24); the D10 condition at 316 has one reading (R25); item 9 points to the Other-scope blanks (56, R3); E1 and E13 name the price cells (133, 295, R7). |
| No deal name, figure or phrase from a deal; no spec decision number; no project-status text | Met, grep re-run on the text after R. Case-sensitive grep for Mac-Gray, Providence, Worcester, Kraton, Datalink, sTec, STEC, Synacor, Penford, PetSmart, Meredith, Medivation, Zep, Pepco, Imprivata, WDC, G&W, CSC, Pamplona, P&W, Saks and "Company/Party" letters (except the draft's generic "Party A"): none. "12.10", "49%", "50–75", "08/08/2014", "terms previously proposed", "five weeks", "thirty days", "30 days": none. D-numbers: only the instruction's own D1–D5 as section references (headings at 44, 78, 102, 117, 121; "one label from D2" at 52; "(D1)" at 133, 293, 299; "(D2)" at 228). Project-status words (Alex, Astra, deferred, pilot, checker, cockpit, provisional, "this fixes", "v1.14 only", spec, taxonomy): none, except the research credit on line 4, unchanged since v1.13.2, and the header's version. The text added after R cites only instruction parts ("(Part A)" at 232, "(item 12)" at 56, E-sections). |
| Every §3.1 line changed or confirmed unchanged | Met (§2 above; draft 54 is now changed, C79). |
| Header in final form | Met: "**Revision of 25 September 2026, v1.14.**", the day the text was frozen after R's fixes (`date -u`). |
| Every reference to Part A resolves | Met: "use judgment from Part A" (129), "the five uses in Part A" (331) and, after R, "a term, not a condition or a bidder commitment (Part A)" (232) resolve to Part A's closing paragraph, items 1–5 and item 3; inside Part A, "(E10)" resolves through 228 (C41). Part A (8–20) is unchanged by the fixes and equals spec §2. |

## 6. Candidate hash

`c2d47a479d09eb46d0ab9fbf887568fcf13e972e2e11acbf08d5cdfab468ab27  SEC_Deal_Ledger_Extraction_Instruction_v1.14_candidate.md`

The hash R reviewed was `6e0a8c41f99391127a2af5ecdd42b3b1a419fb1b172fb992702c777d7a5ee379`.

## 7. Changes after review R

R's findings are in [R_REVIEW.md](R_REVIEW.md). Every must_fix, should_fix and note finding is fixed; none is rejected. The wording is R's proposed fix unless the table says otherwise. Candidate lines are those of the fixed text, which has the same line numbers as the text R reviewed. No line outside these changed.

| R | Severity | Resolution | Candidate lines | Change | Entry |
|---|---|---|---|---|---|
| R1 | note | fixed | 3 | Header date set to the freeze day after the fixes: `date -u` gave 25 September 2026, so the header text is unchanged; the SHA-256 and the diff were recomputed. | C01; §4 item 1; §6 |
| R2 | should_fix | fixed | 24 | "…the label E14's transition rules give an inferred exit is one, though the exit itself is inferred and takes Inferred = Y." | C03 |
| R3 | should_fix | fixed | 56 | Item 9 adds "Both stay blank on Other-scope bid rows (item 12)." Items 8 and 12 unchanged. Draft line 54 is now changed. | C79 (new) |
| R4 | should_fix | fixed | 83 | Bidder interest: "without making a Bid (E10)"; an approach that communicates a proposal, "its price disclosed or not", is a Bid. | C15 |
| R5 | note | fixed | 112 | Values in E9's order: Extended, Extended (late bid accepted), Enforced, Passed without action, Unclear. The item's existing closing "(E9)" is kept, so none is added after Unclear. | C20; §4 item 8 |
| R6 | should_fix | fixed | 114 | "Name any Other-scope bids received in the round, with their bidders, separately in the same cell (E1)." | C21 |
| R7 | should_fix | fixed | 133, 295 | 133: "leave its Price low, Price high and CVR/earnout value blank (D1)"; 295: "and, on a Bid or Bid reaffirmed row, fill the price cells only if the filing gives a per-share figure". | C24; C61 |
| R8 | should_fix | fixed | 135 | "…with a Question naming the party; merger-of-equals talks follow their own rule below." | C24 |
| R9 | note | fixed | 137 | "(an agreement, a proposal and its terms, the end of talks)". | C24 |
| R10 | should_fix | fixed | 139 | After "… do not count.": "Where the result turns on a party whose scope or sale role is unresolved, such as a merger-of-equals counterparty (E1), the entry is Uncertain." | C25 |
| R11 | should_fix | fixed | 143 | "A change in an offer's price, consideration or a bidder's commitments (E10) earns a row even when it was negotiated through drafts." | C26 |
| R12 | should_fix | fixed | 151 | "…does not enter, and neither does a merger-of-equals counterparty while its sale role is unresolved (E1)." | C27 |
| R13 | should_fix | fixed | 183 | "Approaches and unsolicited proposals made before round 1 opens are **round 0**, …". | C35 |
| R14 | note | fixed | 191 | "…, which becomes its entry where E3 counts one." | C37 |
| R15 | should_fix | fixed | 208 | "…except that undated reopened outreach takes the window's midpoint (rounding earlier), or the day after the authorization where that midpoint is not after it or the authorization is the only known bound (E6); otherwise …". | C38; §4 item 7 |
| R16 | must_fix | fixed | 230 | "Anything else the filing does not address for the new bid is Not stated in Stock %, Due diligence, Financing, Regulatory and Exclusivity, and blank in CVR/earnout, CVR/earnout value and Antitrust. On a same-price revision the price cells hold the earlier price only where the filing shows it unchanged, noted like any carried term; otherwise they stay blank." | C42 |
| R17 | note | fixed | 232 | "**Exclusivity** is a term, not a condition or a bidder commitment (Part A): a request for it is not by itself a material revision." | C43 |
| R18 | note | fixed | 232 | "made in the same communication as a bid row (Bid, Bid reaffirmed or Other-scope bid), whether a first bid or a revision, is coded on that row". | C43 |
| R19 | should_fix | fixed | 258 | "**Not stated** means the filing reports nothing for this bid that supports another value; a statement that fits no value, such as a bare statement that approvals are required or that no exclusivity was sought, leaves the column Not stated and goes in the Note. A negative value … needs the filing's support." | C52 |
| R20 | should_fix | fixed | 262 | None: "…Financing Committed or Not needed, Regulatory not Concern (silence stays Not stated) and no other material condition." Draft line 236 is now changed. | C80 (new) |
| R21 | should_fix | fixed | 267 | Adds "Regulatory = Concern does not by itself meet H3; the level follows the other evidence." | C56 |
| R22 | should_fix | fixed | 277 | Coding: "CVR/earnout columns filled; the CVR does not change the Conditions level". | C59 |
| R23 | note | fixed | 279 | "Light, unless H1 or H3 applies". | C59 |
| R24 | must_fix | fixed | 314 | "…infer closure at the first transition that applies, unless the filing shows the participation continuing past it: a continuing solicitation, a still-active offer, ongoing diligence or explicit reserve status after that point. Give the inferred closure Inferred = Y, …". | C69; §2 rows 266, 267 |
| R25 | should_fix | fixed | 316 | "no submission reported, and neither mentioned again nor carried forward by the narrative". | C70 |
| R26 | should_fix | fixed | CHANGELOG only | C42 reads "224, 210 → 230"; C43 reads "new → 232 (replaces 230's two-row rule; see C51)"; the §2 and §3 rows for draft 208 read "226, 228" with C40, C41; the §3 rows for draft 210, 224 and 230 also name C42 and C43 at 230 and 232. | C42; C43; §2; §3 |
| R27 | note | fixed | CHANGELOG only | §1 updated (C03, C15, C20, C21, C24–C27, C35, C37, C38, C42, C43, C52, C56, C59, C61, C69, C70) with new entries C79 and C80, each with its source; §2–§4 updated; §5 restated. Audit C §1's lines are now 74 changed and 47 confirmed unchanged. | §1–§5 |

R's rejected items stand. One of them, the checker message that gave "50-75" as a range example (`controlled.stock_pct`), was checker text for S1, not instruction text; the finalized checker 1.7 (`check_lean.py`, SHA-256 `fa953928…607f`) gives "40-60", the candidate's neutral range.
