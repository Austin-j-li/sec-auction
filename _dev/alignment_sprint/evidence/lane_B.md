# Lane B audit: bids, Formality, conditions, prices

Auditor B, 27 September 2026. Sources: instruction v0 (cited by rule and line), Alex's voice notes (V¶n, with color), Alex's collection instructions (CI p.N), `_dev/STATUS.md`. Filings opened to test rules: Providence & Worcester, Mac-Gray, Penford, PetSmart, Kraton, sTec, Synacor, Meredith, Datalink (backgrounds only).

Colors: black = important/easier; dark red = important/difficult; blue = less important/easier; magenta = less important/difficult. V¶129–166 are "Claude's reading" and weigh less than Alex's own words.

Settled rulings in STATUS are not reopened. Where an item touches one, it says so. In particular, the settled evidence window covers **conditions**; it says nothing about **Formality**, which items B1–B3 concern.

## Counts

| Type | High | Medium | Low | Total |
|---|---|---|---|---|
| CONFLICT | 1 | 2 | 1 | 4 |
| MISSING | 1 | 2 | 2 | 5 |
| ADDED | 0 | 1 | 2 | 3 |
| AMBIGUOUS | 3 | 3 | 2 | 8 |
| **Total** | 5 | 8 | 7 | 20 |

Most important: **B1** (when documents make a bid Formal; Penford over-counts Formal bids), **B2** (a late markup that turns an offer formal gets no row; Providence Aug 4), **B6** (the H2 carve-out leaves long diligence-plus-exclusivity periods out of Heavy).

---

## B1. Route 1 lets documents exchanged apart from the bid make it Formal

- **Instruction:** E11, line 251: "the bidder submits, with a priced proposal or in support of one, a markup or its own draft of the merger agreement". Part B, line 28: "A bid is described by what the filing says about it from its communication up to that bidder's next bid".
- **Alex:** V¶19 (dark red): record "bids that come with the markups to the merger agreement and/or voting agreements as formal." V¶67 (black): Penford is a deal marked as "having more formal bids than previously thought". V¶71 (black): Ingredion's early bids ($18.25–18.50, $18.50, $19) are informal, "we know". V¶74 (black): "All earlier bids by Ingredion have been informal"; the formal offer is the Oct 14 confirmation. CI p.7: formal "if the bidder also submits/returns a draft or the marked-up copy".
- **Type / severity:** AMBIGUOUS, High. "In support of one" has no time limit, and Part B's window runs to the bidder's next bid. The settled window ruling in STATUS covers conditions only, so it does not decide this.
- **Deals:**
  - **Penford.** Ingredion's banker delivered an initial draft merger agreement on Sep 6 (filing p. 28). Ingredion's counsel circulated revised drafts on Oct 8, 10 and 13 (pp. 31–32). Under the loose reading, the Aug 10 $18.00 bid (window to Sep 17), the Sep 17 $18.25–18.50 bid and the Oct 2 $19.00 bid are all Formal because a buyer draft "supports" them. Under the strict reading ("comes with"), all are Informal, and Oct 14 is Formal through route 3 (Bid reaffirmed). Alex's coding is the strict reading.
  - **Kraton.** Party A's markup came on Sep 8; its priced proposals came on Sep 17, 21 and 24. Under the loose reading, all are Formal by route 1. Under the strict reading, Sep 17 is still route 1, because the markup answered a letter that asked for both markups and prices; Sep 21 and 24 are not, and depend on B3 and B4.
- **Recommended fix.** Replace route 1 in E11 with:
  > (1) the bid comes with a markup or the bidder's own draft of the merger agreement or a voting agreement: submitted in the same communication as the priced proposal, or in the bidder's response to a target request that asked for both price and documents. Documents exchanged at another time do not make an earlier or later bid Formal; E10 says when they earn a row.

  Add to Part B, after line 28: "Formality is judged at the bid's communication; the window applies to the condition columns."
- **Needs Alex?** Yes. Ask this together with B2: "Providence Aug 4: Party B's counsel sent a revised merger-agreement draft, and you want a formal $24 row (V¶30). Penford Oct 8/10/13: Ingredion's counsel sent revised drafts, and you treat Ingredion as informal until the Oct 14 confirmation (V¶74). Penford Sep 6: Ingredion's banker sent the initial draft. What makes Providence Aug 4 a formal bid and Penford Oct 8 or Sep 6 not?"
- **Confidence:** high that the wording is ambiguous and that Penford bites; medium on the best rule.

## B2. A late markup or confirmation that makes an offer properly formal earns no row

- **Instruction:** E10 Revisions, line 237: a new row for a "change to price, consideration mix, CVR/earnout, a condition column, financing commitment, reverse termination fee or bidder or sponsor liability". E2, line 149: "successive drafts" fold into a Note. E10 Same offer, line 243: a Same-offer row only "when a bidder says its earlier offer stands".
- **Alex:** V¶30 (dark red): when a bidder "reconfirms the same offer" with "a revised markup ... with no conditions or very light conditions", that "needs to be captured, this is bid revision"; Providence needs "an additional row on August 4" for Party B's formal $24.00 offer. V¶31 (dark red): figuring out "when an informal bid is revised and becomes formal" is required judgment. V¶135 (Claude's reading) agrees.
- **Type / severity:** MISSING, High. The event Alex treats as the formal bid gets no row.
- **Deals:**
  - **Providence, Aug 4.** "legal counsel for Party B provided a revised draft of the merger agreement" (p. 31). It restates no price and no condition, and Party B says nothing about its offer standing. Instruction: no row, and Party B's formal observation stays the July LOI (Formal with Light conditions). Alex: an Aug 4 Bid row at $24, Formal, with light or no conditions.
  - **Penford, Oct 14.** "Mr. Fortnum called Mr. Malkoski to confirm the proposed price of $19.00" (p. 32). The instruction captures this, because it is an express confirmation (Bid reaffirmed). So the gap is specific to confirmation by documents. The main fix below would also add a Penford Bid reaffirmed row at Oct 8, Sidley's first draft after the Oct 3 decision, six days before the Oct 14 confirmation Alex names. That shift is what the Needs-Alex question tests.
- **Recommended fix.** Add to E10, after Same offer (line 243):
  > **Confirmation by documents.** After the target has begun definitive negotiation with a bidder, a markup or draft of the merger agreement that the bidder itself submits, with no new price, is a Bid reaffirmed row for that bidder's latest offer. Record one such row per bidder at its first such submission, and another only if the filing reports a changed term with a later one. Target-sent drafts never earn a row.

  In E2, change "successive drafts" to "successive drafts, except as E10 records a bidder's confirmation by documents".

  Once Alex answers B1's question, this could instead be limited to the first bidder-submitted documents after an Informal latest bid. That limit would give Penford Oct 8 rather than Oct 14, and would drop Providence Aug 4, because Party B's July LOI already had a markup. His answer decides between the two.
- **Needs Alex?** Yes. It is the same contrast question as B1.
- **Confidence:** high on the gap; medium on the rule.

## B3. A price-only revision drops a Formal bidder to Informal

- **Instruction:** E11, line 251: "A later revision, including one that changes only the price, is Formal only if it meets a route itself."
- **Alex:** V¶19–20 (dark red): Formality follows the documents; keep flexibility for reinterpretation. V¶30 (dark red): he calls such bids "formal with conditions", a status that persists until revised. He gives no rule for price-only revisions. STATUS lists "price-only revisions" under Open with Alex.
- **Type / severity:** CONFLICT, Medium. Alex's framing implies Formality persists while the bidder's documents stay on the table. The instruction resets it with each revision. This is an inference from his framing, not something he said.
- **Deals:**
  - **Providence, G&W.** The Jul 21 LOI came with markups: Formal. The Jul 26 revised LOI raised the price to $22.15 "in response to feedback" and brought no new documents. The round was not announced as final, so it is Informal. The result is a Formal → Informal sequence within one round with the same documents.
  - **sTec, WDC.** The May 28 bid came with a markup: Formal. The Jun 10 range bid and the Jun 14 $6.85 bid were "otherwise on the transaction terms previously proposed on May 28" (p. 32). They are Formal only if route 2 applies. If Alex's "not the final round" reading of sTec stands (V¶125; STATUS open), both are Informal.
- **Recommended fix.** Add to E11:
  > A revision by a bidder whose last bid was Formal by route 1 stays Formal by route 1 when it changes only price, consideration or conditions and the filing does not report that the bidder withdrew or replaced its documents.

  Alternatively, defer the question to estimation by recording one raw fact per bid row: "Documents on table: Y where the bidder's markup or draft is outstanding at this bid." Formality then stays procedural, and derive can carry it forward.
- **Needs Alex?** Yes: "If a bidder that has submitted a merger-agreement markup later changes only its price, without new documents, is the new bid formal (Providence G&W Jul 26; sTec WDC Jun 14)?"
- **Confidence:** medium.

## B4. How far route 2 reaches inside a final round

- **Instruction:** E11, line 251: route 2 applies when the bidder "answers a solicitation the target announced as final, binding or best-and-final"; "An unsolicited bid during a final round carries that round's number ... but not route 2." E6, line 189 treats improvement requests as events within the round.
- **Alex:** CI p.9, on final-round letters: "Record all bids of OTPP, A, and B after that date as formal." CI p.7: formal "if the company announced a final round of bidding that only a subset of bidders is invited to". The voice notes are silent.
- **Type / severity:** AMBIGUOUS, High. The instruction does not say whether answers to improvement requests, late answers, or an invited finalist's unsolicited improvements "answer" the final solicitation. CI says every bid by an invited bidder after the letter is formal.
- **Deals:**
  - **Kraton.** A "final bid procedures letter" was sent to Party A, Party H and Parent. After the board told Party A its Sep 17 $40.50 was inadequate, Party A sent $42.00 with an earnout (Sep 21) and $44.00 "best and final" (Sep 24). Unsolicited reading: Informal. CI: Formal.
  - **PetSmart, Dec 12.** The Buyer Group's oral $82.50 and $83.00 "best and final" answered the Dec 10 improvement request. Most readers would say route 2 applies, but the text does not say so.
  - **Providence.** The rounds were not announced as final, so route 2 does not bite there.
- **Recommended fix.** Replace the last sentence of E11 with:
  > Route 2 covers every bid, including an improvement, a late answer or an unrequested revision, that a bidder invited to a round announced as final makes between the round's opening and its end. A party not invited to that round that bids during it carries the round's number but not route 2.
- **Needs Alex?** Confirm only: "CI p.9 treats every bid by the invited bidders after the final-round letter as formal. Does that still hold, including unrequested improvements (Kraton Party A Sep 21/24)?"
- **Confidence:** high.

## B5. "Final" solicitations that ask for non-binding indications

- **Instruction:** E11 route 2 (line 251); E6(b), line 183: "first asks for final, binding or best-and-final offers"; Finality, line 195.
- **Alex:** CI p.8 provides for "a final round of informal bids" ("Final Round Inf Ann"). V¶48 (black): Mac-Gray Party A's $18–19 "best and final" in the final stage stays Formal. V¶124–125 (dark red): sTec's May 16 letters open "round two of informal bidding", and May 28 is "not the final round". STATUS already lists the round and finality convention as open.
- **Type / severity:** AMBIGUOUS, Low for extraction. The case is an estimation choice (T3), and the underlying question is already open with Alex.
- **Deals:**
  - **Mac-Gray, Sep 11.** The target requested "final indications of interest". The instruction records Formal (route 2). CI p.8 would record a final informal round. V¶48 records Formal.
  - **sTec, May 16.** The target sent "final round process letters". The May 29 board minutes call the answers "non-binding proposals". The instruction records Announced as final, and every answer is route 2. Alex says the round is not final.
- **Recommended fix.** Do not change Formality. Add a raw Rounds column, **Solicitation asked for**: the solicitation's own words on finality ("final", "binding", "best and final", "non-binding"), and whether it requested a markup (Y/N/not stated). Estimation can then build CI's "final informal round" without re-reading the filing.
- **Needs Alex?** Fold into the open STATUS question: "When a target asks for 'final' but non-binding indications (Mac-Gray Sep 11, sTec May 16), is that a final round, and are the answers formal?"
- **Confidence:** high.

## B6. The H2 carve-out keeps long diligence-plus-exclusivity periods out of Heavy

- **Instruction:** E12 H2, line 268: "A period that also covers negotiation or exclusivity is not tied to diligence alone." Example 4, lines 331–334: Party G's "45-day exclusivity period to complete due diligence and negotiate" is Conditions Unclear, "Not H2".
- **Alex:** V¶19 (dark red): conditions such as "extensive due diligence, exclusivity, or financing requirements ... that can materially affect ... completion certainty" define heavy conditionality. V¶49 (black): exclusivity itself should not downgrade a formal bid. That supports keeping exclusivity out as a trigger, not letting it cancel a diligence trigger.
- **Type / severity:** CONFLICT, High, because it flips Conditions from Unclear to Heavy for two of three Providence finalists' LOIs. The carve-out turns the longest diligence demands into Unclear while shorter pure-diligence periods are Heavy.
- **Deals:** Providence, July LOIs (p. 29–30), all on one page:
  - Party D: "subject to a four-week diligence period". Instruction: Heavy (H2).
  - G&W: "subject to a three-week exclusive diligence period". Instruction: not H2, Due diligence Incomplete, Conditions Unclear.
  - Party E: "subject to a 60-day exclusivity period for due diligence and negotiation". Instruction: Unclear.
  - Under V¶19, all three are heavy.
- **Recommended fix.** Replace H2 with:
  > **H2**: the filing ties a period of two weeks or more to remaining diligence, alone or together with negotiation or exclusivity, and does not call that diligence confirmatory.

  Replace Example 4's last line with: "Row: ... Conditions Heavy; Note 'H2: 45 days' exclusivity for diligence and negotiation'." Exclusivity stays out of the trigger list (line 277).
- **Needs Alex?** Yes, briefly: "Is a bid 'subject to a 60-day exclusivity period for due diligence and negotiation' heavily conditional, like one subject to a four-week diligence period?"
- **Confidence:** high on the conflict.

## B7. Silence yields Unclear where Alex reads "no conditions"

- **Instruction:** E12, line 255: "A negative value (Complete, Not needed, No concern) needs the filing's words. Silence is Not stated". Line 273: None requires "Due diligence is Complete"; line 275: Unclear otherwise.
- **Alex:** V¶125 (dark red): WDC's May 28 bid "has a markup. It has no conditions". V¶183 (black) describes the same bid as coming "without conditions". V¶30 (dark red): late revised markups carry "no conditions or very light conditions".
- **Type / severity:** CONFLICT, Medium. The T1 reading ("Formal and not Heavy") treats Unclear like None, so the reading Alex most often uses survives; the T1u reading does not.
- **Deals:**
  - **sTec, WDC May 28.** The filing is silent on financing and conditions, and the target was "endeavoring to complete diligence". Instruction: Financing Not stated, Due diligence Incomplete, Conditions Unclear. Alex: None.
  - **Providence, Party B at Aug 4** (if B2 adds that row): on-site diligence runs to Aug 11, so the instruction records Incomplete / Unclear or Light. Alex: none or very light.
- **Recommended fix.** Keep the evidence standard, but separate "nothing reported" from "mixed or doubtful". Add a Conditions value:
  > **None stated**: no H trigger holds, and the filing reports no diligence, financing or regulatory condition for the bid.

  Keep **Unclear** for bids whose reported facts point both ways, and for cohort rows. This records the raw distinction and leaves estimation free to read None stated as None.
- **Needs Alex?** Yes: "For a markup bid where the filing names no condition, should we record 'none stated' separately from 'none', or treat silence as none?"
- **Confidence:** medium.

## B8. Existing facilities named alongside "no firm financing commitment"

- **Instruction:** E12 Financing, line 258: "**Not needed**: cash on hand, existing facilities or all stock. **Contingent**: ... a source named without a commitment."
- **Alex:** V¶47 (black): "I would rather record the lack of financing guarantees than their presence", because the lack is what may downgrade a bid.
- **Type / severity:** AMBIGUOUS, Medium. Both values fit, and the choice decides H1 (Heavy).
- **Deals:**
  - **Mac-Gray, Party A, Sep 10.** Its bid was "to be financed by outstanding credit facilities or affiliated equity sources" and "Neither Party A's nor Party C's revised indication of interest included a firm financing commitment" (p. 35). One reading gives Not needed and no H1. The other gives Contingent and Heavy. The Sep 18 Same-offer row copies whichever is chosen.
  - **Mac-Gray, Party B.** Party B is Contingent on either reading, matching V¶47.
- **Recommended fix.** Add to Financing:
  > Where the filing says the bid lacks a firm or committed financing arrangement, Financing is Contingent, whatever sources it names.
- **Needs Alex?** No. It follows V¶47.
- **Confidence:** medium.

## B9. "Conditions on proceeding" turns legal-term negotiation into Heavy bid rows

- **Instruction:** E10, line 239: "A bidder's statement that it will not proceed unless something happens, or may not proceed if something happens, is a Bid row coded H3". H3, line 269.
- **Alex:** V¶19 (dark red): "I don't want detailed conditions"; he wants a none/light/heavy flag for conditions that "materially affect the value of the deal or completion certainty". V¶125 (dark red): WDC's bid is unconditional. E2 (line 149) itself folds "other negotiation of legal terms" into Notes.
- **Type / severity:** ADDED, Medium. The rule is broader than Alex's intent and contradicts E2.
- **Deals:**
  - **sTec, Jun 20.** WDC's counsel said WDC "would view it as improper if sTec unilaterally waived" its don't-ask-don't-waive provisions, "indicating that WDC may not move forward" (p. 34). Instruction: a new WDC Bid row, Heavy (H3), four days before signing. Alex: WDC stays unconditional.
  - **Mac-Gray, Sep 11.** The banker reported it "unlikely that any of these parties would move forward in the process without the express support of Mr. MacDonald" (p. 35). A reader could create H3 rows for four bidders.
- **Recommended fix.** Add to E10, "Conditions on proceeding":
  > This applies to conditions outside the definitive documents: a third party's support, a business or financial outcome, a price test. A bidder's position on a term of the merger agreement or ancillary documents under negotiation is negotiation (E2) and goes in the Note of its latest bid row. An adviser's summary of what bidders are likely to require is not a bidder's statement.
- **Needs Alex?** No, but show him the sTec Jun 20 coding.
- **Confidence:** medium-high.

## B10. Regulatory concern never makes a bid Heavy

- **Instruction:** E12, lines 265–275: Heavy only through H1–H3; H3 excludes "ordinary approvals". A regulatory Concern only blocks None.
- **Alex:** V¶19 (dark red): anything affecting "completion certainty" belongs in the heavy/light judgment. V¶150 (Claude's reading) lists regulatory among the conditions.
- **Type / severity:** ADDED, Low. The instruction makes a specific choice Alex never stated. It is consistent with his wish for a coarse flag, and the Regulatory and Antitrust columns keep the raw fact.
- **Deals:**
  - **Kraton, Party A Sep 24.** The board weighed "complexity, timing and risks (including regulatory risks)" (p. 40): Regulatory Concern, and with "confirmatory due diligence", Conditions Light.
  - **Penford, Ingredion.** Divestiture requirements were negotiated (p. 31): Regulatory Concern, Antitrust Y, Conditions not Heavy.
- **Recommended fix.** Defer to estimation. Record the raw facts as now (Regulatory, Antitrust, Note). If Alex wants it, add: "H4: the filing reports that the bidder requires, or the target expects, divestitures or a second request."
- **Needs Alex?** Yes, low priority: "Should antitrust risk (divestitures, second request) make a bid heavily conditional, or stay a separate flag?"
- **Confidence:** medium.

## B11. Per-share values from total, equity or enterprise-value bids, and the inputs to normalize them

- **Instruction:** E13, line 283: a total, enterprise-value or exchange-ratio bid "goes in the Note with its basis; fill the price cells only if the filing gives a per-share figure." D5 (line 125) records only "Currency and units of bid prices".
- **Alex:**
  - CI p.2: bid_value for the whole company "has to be divided by the number of shares outstanding to get bid_value_pershare. The only relevant thing for us is bid_value_pershare."
  - V¶100 (blue): subtract net debt from enterprise value, then divide by shares.
  - V¶105 (black): bids come in dollars versus per share, and in enterprise versus equity value.
  - V¶185 (black): flag bids whose currency or units are unclear, and flag enterprise-value bids.
  - V¶142 (Claude's reading): "capture net debt and shares outstanding so enterprise-value and per-share offers can be normalized."
- **Type / severity:** MISSING, Medium. CI and the instruction conflict on who divides; the voice notes ask for the inputs and the flag.
- **Deals:**
  - **Meredith.** Settled as Other-scope for the LMG bids, so their price cells stay blank. The flag and inputs still matter for descriptive use.
  - **Kraton.** Party K's and Party A's segment bids are stated as enterprise values (Other-scope).
  - **Synacor.** Company C's cash-and-stock LOI gives no figures.
  - In the nine deals, every whole-company bid I checked is per share, so the effect grows with the sample, not in these deals.
- **Recommended fix.** Keep E13's price rule, which preserves the evidence standard. Add to D5 after "Currency and units of bid prices":
  > **Value basis**: Per share, or list the bids stated as total equity value, enterprise value or exchange ratio. **Shares outstanding**: the fully diluted count the filing states, with its date and page, else "Not stated". **Net debt**: the figure the filing states, with date and page, else "Not stated".

  Per-share conversion then happens at estimation, as CI p.2 intends.
- **Needs Alex?** Yes: "Should the extraction convert total or enterprise-value bids to per share using the filing's share count and net debt, or record the inputs and convert at estimation?"
- **Confidence:** high.

## B12. Target market price through the process

- **Instruction:** E13, line 283: "A stated reference price or premium goes in the Note". The Exit reason values use market-price comparisons (line 310).
- **Alex:**
  - V¶117 (black): "we need to keep track of the target's changing stock price throughout the entire sale process", because the premium may be steady while the dollar value falls (sTec).
  - V¶105 (black): Meredith is useless because the premium cannot be computed.
  - CI p.8: DropBelowM.
- **Type / severity:** MISSING, Low for extraction. Daily prices come from market data, not from the filing.
- **Deals:**
  - **sTec.** WDC fell from $9.15 to $6.85, and the premium is not in the ledger.
  - **Penford.** The filing states the premium for each Ingredion bid. Those figures land in Notes but are not structured.
- **Recommended fix.** Defer to estimation. Merge daily prices from market data (for example CRSP) on each row's Sort date. Keep the Note's "Ref:" format so filing-stated references can be checked against market data.
- **Needs Alex?** Yes, to confirm: "Will the market price series come from CRSP at estimation, with the filing's stated reference prices used only as a check?"
- **Confidence:** high.

## B13. A later description can make a non-bid approach look like a Bid

- **Instruction:** E10, line 247: "A statement is a Bid only where the filing presents it as a proposal, offer or indication"; otherwise it is a valuation statement. The rule does not say which passage decides.
- **Alex:** V¶68 (black): on Jul 17, Ingredion "cited the target's stock price over some historical period ... There is no bid here. This is indeed bidder interest which came without a bid."
- **Type / severity:** AMBIGUOUS, Medium. It changes the bid count and the price series.
- **Deals:**
  - **Penford.** The Jul 17 passage says Gordon "did not cite a specific number but noted Penford's 52-week high of approximately $16.00" (Jul 17 passage). The Sep 29 board passage calls it "Ingredion's initial indication of $16.00 (based on the 52-week high)" (p. 30). Under the later passage, Jul 17 is a $16 Bid in round 0. Under the Jul 17 passage, it is Bidder interest plus a valuation statement. Alex: no bid.
- **Recommended fix.** Add to E10, "Valuation remarks":
  > Judge this from the passage that reports the communication. A later passage that calls it an indication or offer does not make it a Bid; quote that description in the Note.
- **Needs Alex?** No. V¶68 decides it.
- **Confidence:** high.

## B14. Merger-of-equals and target-as-buyer talks inside the process test

- **Instruction:** E1, line 143: an MOE counterparty "stays outside the whole-company contest unless the filing reports that the target is being sold to it." E1, line 139: "A target's attempt to buy another company is not its sale process." E5, line 171 tests (a) "no bidder was in negotiation" and (b) "no reported sale contact between the target ... and any prospective acquirer". It does not say whether MOE or target-as-buyer counterparties count.
- **Alex:** V¶108 (dark red): Synacor's break runs from the end of the Company C talks (Oct 2019) to Company E's approach (Jul 2020), "a 9 month gap ... these are indeed different processes." V¶132 (Claude's reading) agrees.
- **Type / severity:** AMBIGUOUS, High, because it changes the process count.
- **Deals:**
  - **Synacor.** In that gap the target negotiated an all-stock deal with Company D, starting from the target's own offer to buy Company D. The deal had a "combined company ownership split", was signed Feb 11, 2020 and was terminated Jun 29, 2020 (p. 31). If Company D counts as a prospective acquirer in negotiation, E5(a) and E5(b) fail, and Company C's and Company E's efforts are one process. If it does not, the result is two processes, as Alex says.
  - **Synacor, Company B.** The target's "merger of equals" LOI in Dec 2018 raises the same question for an earlier break.
- **Recommended fix.** Add to E5 (a sentence only; process rules belong to another lane):
  > Talks with a merger-of-equals counterparty outside the contest, or about the target acquiring another company, are not sale contacts under (b) and are not negotiation under (a).
- **Needs Alex?** No. V¶108 implies it; confirm when the process questions go to him.
- **Confidence:** medium. Whether the Company D deal is an MOE or a sale of the target is itself a reading of the filing.

## B15. Contingent amounts with an unstated payment date may be coded as a range

- **Instruction:** E13, line 287: "A price that depends on criteria is a CVR/earnout only if the extra amount is paid after closing; otherwise it is a range."
- **Alex:** V¶84 (black): Kraton Party A's earnout "is not a mixed offer ... a cash offer with an extra contingent payment ... upon clearing certain thresholds"; it belongs in a separate column or row.
- **Type / severity:** AMBIGUOUS, Low.
- **Deals:**
  - **Kraton, Party A Sep 24.** It offered $44.00 plus 50% of net proceeds above thresholds "if Kraton entered into a binding agreement to sell its chemical business to a third party prior to the closing" (p. 40). The trigger falls before closing, and the payment date is not stated. One reading gives a range with no upper figure (both price cells blank under E13's imprecise-range rule). The other gives Price 44.00 with CVR/earnout Y. Alex's reading is the second.
- **Recommended fix.** Replace the sentence with:
  > A price that depends on criteria is a range only when the filing gives the alternative upfront prices. Any other additional amount that depends on future events is a CVR/earnout, including when the filing does not say when it is paid.
- **Needs Alex?** No.
- **Confidence:** medium.

## B16. Revisions by the signed acquirer after signing

- **Instruction:** E2, line 149: "After signing, record only the merger announcement, competing proposals and their process events, go-shop activity, and termination of the agreement."
- **Alex:** V¶104 (black): Gray's post-signing bids went $16.99 → $16.55 → back to $16.99, and "The AI does not record this bouncing back and forth ... We need to figure out how to be careful about this."
- **Type / severity:** AMBIGUOUS, Medium. It is unclear whether the incumbent's matching offers count as "competing proposals and their process events".
- **Deals:**
  - **Meredith.** Gray's revised terms are Other-scope under the settled ruling, but they still need rows.
  - The same question arises in any topping contest.
- **Recommended fix.** In E2, after "competing proposals", insert "and the signed acquirer's revised offers in response to them".
- **Needs Alex?** No.
- **Confidence:** high.

## B17. Which of a bidder's alternative structures enters the price series

- **Instruction:** E10, line 235: "Alternative structures offered in one communication are separate rows ('alternative to #n')."
- **Alex:** V¶102 (magenta): Party D's dual proposal consists of separate bids, and "we should record the 2.76 billion, which gives target shareholders a better out," given the target's stated preference.
- **Type / severity:** MISSING, Low. The instruction keeps both alternatives, which is consistent with Alex, but gives no marker for the one Alex would use.
- **Deals:**
  - **Meredith.** Party D's two alternatives are both Other-scope under the settled ruling.
  - **Kraton, Party A Sep 17.** Its whole-company bid is a Bid row, and the segment alternative is Other-scope, so there is no choice to make.
- **Recommended fix.** Defer to estimation. Add to E10: "Where the filing reports the target's preference between alternatives, the Note of each alternative row says so." Estimation chooses.
- **Needs Alex?** No.
- **Confidence:** high.

## B18. Mandatory verification flags for Formality and conditions

- **Instruction:** Part F, line 343: at most five Questions; "Applying a default is never a Question."
- **Alex:** V¶183 (black): "anytime an IOI seems like a formal bid because of the markup and no conditions, the AI should flag it for human verification." V¶179 (black): conditionality should be human-verified "for the first several deals".
- **Type / severity:** MISSING, Medium. The general flag list (V¶172–185) is already on STATUS's list; this item covers only the lane-B entries.
- **Deals:**
  - sTec WDC May 28 (an IOI coded Formal).
  - Providence's July LOIs (LOIs with markups).
  - Kraton Parent.
- **Recommended fix.** In Part F, add fixed checks outside the five-Question limit: "Check: Formal bid labelled indication, IOI or non-binding"; "Check: Formal bid with Conditions Heavy". List them in Questions with "Check:" and flag their rows. Whether to check all conditions for the first N deals is a process choice for Austin, not an instruction rule.
- **Needs Alex?** No. He asked for it.
- **Confidence:** high.

## B19. A commitment letter as a route-1 definitive document

- **Instruction:** E11, line 251: "another definitive transaction document (a commitment letter or a voting agreement)".
- **Alex:** V¶47 (black): financing guarantees' "presence keeps the informal bid informal and the formal bid formal." V¶19 (dark red) names merger-agreement and voting-agreement markups only.
- **Type / severity:** CONFLICT, Low. The instruction lets financing documents make a bid Formal; Alex says financing presence does not change Formality.
- **Deals:**
  - None of the nine bites on this alone. Where commitment letters appear (Mac-Gray CSC Oct 5, Datalink Party B Aug 30, PetSmart Dec 12), a merger-agreement markup or a definitive negotiation is also present.
  - The case arises when an indication of interest arrives with executed commitment letters and no markup. Datalink's board asked Party A for a proposal with "executed commitment letters", which shows the pattern exists. Instruction: Formal. Alex: Informal with Financing Committed.
- **Recommended fix.** Remove "a commitment letter" from route 1. Keep commitment letters in Financing. Commitment-only change rows (settled) then take Formality from routes 2–3, or from B3's carry-forward rule if adopted.
- **Needs Alex?** Yes, briefly: "Does an indication of interest with executed financing commitments but no merger-agreement markup count as formal?"
- **Confidence:** medium.

## B20. A route-2 Formal bid needs no subset of bidders

- **Instruction:** E6(b), line 183: "first asks for final, binding or best-and-final offers, even from unchanged bidders"; route 2, line 251.
- **Alex:** CI p.7: formal "if the company announced a final round of bidding that only a subset of bidders is invited to". The voice notes do not repeat the subset condition. V¶27 (dark red) accepts finality without it.
- **Type / severity:** ADDED, Low. This is consistent with the later voice notes.
- **Deals:**
  - **sTec, Kraton, PetSmart.** Their final rounds were in any case narrowed to a subset.
  - A final round sent to every remaining bidder would differ.
- **Recommended fix:** none. Note the difference from CI.
- **Needs Alex?** No.
- **Confidence:** high.

---

## Where the voice notes and the collection instructions disagree (lane B)

| Point | CI | Voice notes | Instruction | Note |
|---|---|---|---|---|
| Range bids | p.7: "any bid expressed as a range is also to be classified as informal" | V¶48 (black): Mac-Gray Party A's $18–19 best and final "is currently recorded as formal. And I think I want to keep it this way" | Follows the voice notes; estimation reading T2 handles it | No change |
| Partial bids | p.7 and p.9: do not record | V¶97 and V¶184: flag them; keep for descriptive work | Other-scope rows | Settled (Meredith) |
| Final round of informal bids | p.8: allowed | V¶124–125: sTec's informal round 2 | Route 2 makes any "final" round's answers Formal | B5; open in STATUS |
| Bids after a final-round letter | p.9: all formal | Silent | Unsolicited bids are not route 2 | B4 |
| Per-share from totals | p.2: divide by shares | V¶100: net-debt adjustment | Price blank, amount in Note | B11 |
| Subset condition for a final round | p.7 | Absent | Absent | B20 |

## Checked and consistent

- Formality and conditions are recorded separately (A.3, line 16; E11; E12), as V¶19–20 ask; Formality can be reinterpreted at estimation.
- Exclusivity never downgrades Formality or triggers H3 (line 277), as in V¶49.
- CVR/earnout sits apart from price and from Stock %, as in V¶84 and V¶135. Mac-Gray Party B's options are coded CVR Y at $2.50 on a $19.00 upfront price. Providence G&W's $1.13 CVR sits apart from the $20.02 cash.
- Financing Contingent covers "no firm commitment" (Mac-Gray Party B), as in V¶47. A statement that a sponsor covers 100% of the price is Committed (CSC/Pamplona, V¶46).
- Bid reaffirmed is Formal, which covers Penford's Oct 14 as V¶74 wants.
- A return to an older price is a new row (E10, line 237), as in V¶104.
- Same-day bids keep the filing's order, as in V¶59.
- One communication is one row; an IOI is not duplicated, as in V¶183.
- An approach without a proposal is Bidder interest (D2, line 84), as in V¶68 and CI p.5. B13 covers the one gap.
- A shareholder rollover does not make a bid partial or a group (E1, line 139; E4, line 167), as in V¶64.
- A cohort range goes on the cohort row (E13, line 281), as in CI p.7.
- Alternative structures are separate rows, as in V¶102. B17 covers which one to use.
- A mark-up of the voting agreement counts for route 1, as in V¶19.
- Filing labels ("non-binding", "LOI") do not decide Formality (E11), as in V¶26, V¶125 and V¶183.
- The Mac-Gray Sep 18 best-and-final reiteration by Party A comes out Formal (route 2), as V¶48 wants (whether a request for 'final indications' should invoke route 2 is B5).

## Outside my lane

- **Penford Party A at Oct 3.** E14 inferred-exit rule 1 (line 300) drops Party A (NDA signed Sep 30) as "not invited into a stage when it opens" when round 2 opens by trigger (c). V¶72 (dark red) says the target is "not explicitly excluding other bidders who have previously signed NDAs". Party A then bids on Oct 14, which needs a Re-entered row.
- **Human-verification flags.** Alex's full list (V¶172–185) against the five-Question ceiling is already on STATUS.
- **Kraton rounds and sTec finality** are already open in STATUS. B5's raw "Solicitation asked for" field would support either ruling.
