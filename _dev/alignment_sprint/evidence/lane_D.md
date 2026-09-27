# Lane D audit: output, work process, and voice-note coverage

Auditor D, 27 September 2026. Sources read in full: the v0 instruction (`SEC_Deal_Ledger_Extraction_Instruction.md`, cited by section and line, "L"), Alex's voice notes (V¶), his collection instructions (CI p.N), `_dev/STATUS.md`. Consulted for mechanics: `_dev/tools/check_lean.py`, `_dev/tools/derive_analysis.py`. Filings opened: sTec, Meredith, Synacor (text searches only). Not read: `_dev/ALEX_ALIGNMENT.md`, `extraction/`, `ref/`, git history.

Settled rulings in STATUS are not reopened. Where an item touches Meredith or sTec, the fix is general and the ruling stands.

Counts: 13 Part 1 items (3 CONFLICT, 4 MISSING, 1 ADDED, 5 AMBIGUOUS; 2 High, 5 Medium, 6 Low). Part 2 covers all 187 paragraphs.

---

## Part 1. Output and work process

### D1. Mandatory human-verification flags against the five-Question cap

- **Instruction:** F, L343: "Raise at most five Questions … Applying a default is never a Question." L343: "A Question that further reading would resolve is reading still to do." Only the process Question is required (L345). D1 col 25 (L73) and the checker (`Flag must contain only question ids such as Q1`) allow only Question ids in Flag.
- **Alex:** V¶172 (black): "the AI should ALWAYS flag for human review several types of information", then A–M (V¶173–185, black), plus V¶186 (multiple processes) and V¶187 (checks can be dropped later as the AI improves). Supporting: V¶17, V¶24 (magenta), V¶50 (red), V¶110 (red), V¶133, V¶136, V¶141, V¶148.
- **Type / severity:** CONFLICT, High. The instruction treats a flag as a sign of an unresolved choice and caps it. Alex treats a flag as a verification step that happens even when the extractor is confident. Most of his categories are exactly where a default applies (an inferred exit with reason Not stated, an Unknown type after search, a qualified NDA count), so the instruction forbids raising them.
- **Deals where it bites:** all nine. Examples: Kraton and Mac-Gray round openings (A); sTec May 3 soft deadline (B); Penford, Kraton, Synacor winner type (C); Providence, Mac-Gray, Petsmart, Kraton NDA totals (E); Kraton Party H, Petsmart non-submitters (F); sTec WDC May 28 IOI with markup (K); sTec Company A's bank (J); Meredith partial and EV bids (L, M).
- **Recommended fix.** Split two kinds of entry. Questions stay as they are: capped, for real two-way codings. Review items are new: uncapped, fixed categories, and many of them need no work from the extractor.
  1. **Tool-generated (no instruction text).** A review script (extend `derive_analysis.py`'s `review` list, or a separate `review_list.py`) lists every case derivable from cells: C (Deal facts Acquirer type Unknown); D (a Formal bid row with Type Unknown); E (Count blank with a "Count: more than …" Note, or an NDA/Contact cohort with Type Unknown); F (exit rows with Exit reason Not stated or Inferred = Y); B (every Rounds Deadline outcome, and every "No deadline stated"); L (Whole-company bids = No); M (Currency and units not "US dollars per share", or any bid Note giving enterprise value or a total); processes (Number of processes > 1); each Round opened row, with its trigger. Each entry gives the row, the Quote and page, and a link to the filing page (see D9). A table of categories, each with an on/off switch, lets Austin drop checks as Alex allows (V¶187).
  2. **Instruction text for what the ledger cannot show.** Add to Part F, after L345:

     > **Review items.** Besides Questions, list on the Questions sheet, numbered R1, R2 … in row order and without a cap, each case of the following, with the page: (a) a target board or committee meeting held on a bid due date or within seven days after it that opened no round, with what it decided; (b) a bid the filing calls an indication of interest, letter of intent or proposal that you coded Formal; (c) an adviser whose client the filing leaves unclear; (d) a row whose date, count or bidder identity rests on passages in different paragraphs. A Review item states the fact and the coding you chose; Recommended answer is that coding. Put R ids in the Flag column of the rows they touch. Review items are not Questions and do not count toward the five. In "What changes if answered differently", give the alternative coding, or "—" if none.

     Replace L343's sentence "Applying a default is never a Question" with "Applying a default is never a Question; it may be a Review item."
  3. **Conditionality (V¶179).** Handled by the tool: for the first N deals (Austin sets N), list every bid row's Conditions and trigger for review. No instruction text.
- **Checker/schema change:** `check_lean.py` Flag pattern accepts `R\d+` as well as `Q\d+`; Questions sheet ids accept `R\d+`; the five-Question cap and process-Question logic count Q ids only; the 60-word limit applies to both. No new sheet or column.
- **Needs Alex?** Yes. "Your list A–M asks for flags. If we generate B, C, D, E, F, L and M from the finished ledger as a review list with page links, and the extractor itself flags only round-ending meetings, formal-looking IOIs, unclear adviser affiliation and cross-paragraph facts, does that meet your requirement, or do you need each of these raised during the run? For conditionality (G), for how many deals should every bid's conditions be reviewed? And is 'within seven days after a due date' (our proposed threshold) the right window for a meeting "a bit after the deadline"?"
- **Confidence:** High that this is the largest output gap; medium on the exact split between tool and instruction.

### D2. Real-time interactive collaboration against a batch, sandboxed run

- **Instruction:** C, L34–37 (Read, Map, Draft, Reread) with no point at which a person confirms anything; F, L353: "Reply with the workbook path and anything you could not do." AGENTS.md requires one sandboxed session per comparison run, with the checker run afterwards.
- **Alex:** V¶169 (black): "the AI flags these cases to the human IN REAL TIME". V¶170: a wrong round count means the human re-numbers every row; the same for processes. V¶171: he accepts that this rules out large background batches "until the AI is capable of recording the number of rounds, processes, NDAs, etc. very reliably".
- **Type / severity:** CONFLICT, High. The cost Alex names (re-numbering every row after a wrong round map) comes from the order of work: the map is fixed before rows are written, and nobody sees it until delivery.
- **Deals where it bites:** Kraton (three rounds; STATUS ruling), Mac-Gray (July 25 stage), sTec (two processes), Synacor (processes), Penford (October 3 final round).
- **Recommended fix.** Add a checkpoint after Map, active only when a person is present. Insert after C step 2 (L35):

  > **2a. Check the map.** If a person is taking part in this session, show them, before writing rows: each process with its dates and the E5 test result; each round with its opening act, trigger, due dates and finality; contact and NDA totals by type with their pages; the winner and its Type. Write rows only after the person confirms or corrects the map, and follow their correction. In a run with no person present, continue, and give the same map as a Review item whose Question begins "Map:".

  This keeps comparison runs isolated and unchanged (no person present). The cockpit needs a pause-and-confirm step; that is outside this checkout.
- **Checker/schema change:** none beyond D1.
- **Needs Alex?** Yes. "Would it be enough for the AI to stop once per deal, after it has mapped processes, rounds, NDA counts and the winner's type, and wait for you or Austin to confirm before it writes the ledger, with every other flag reviewed after the run?" Austin must also decide whether the cockpit supports a pause.
- **Confidence:** High on the conflict; medium on whether one checkpoint satisfies Alex.

### D3. Count and Who on announcement and signing rows (Austin's request)

- **Instruction:** D1 col 20, L68: "Blank on rows about no bidder, except Process terminated, Process restarted and Bidding group changed." D1 col 3 (L51) gives Who for bidders and "the target (also for process-wide events)". Nothing says who the Who is, or what Count is, on Merger agreement signed, Merger announced or Bid announced.
- **Mechanics:** `check_lean.py` `NO_BIDDER_COUNT_EVENTS` forces Count blank on the three announcement labels, Adviser, Adviser ended, Round opened and the deadline labels. Merger agreement signed, Go-shop changed, Exclusivity changed, Other material event, Target sale decision and Activist are in neither the forced-blank list nor the required list, so either value passes. `derive_analysis.py` treats Merger agreement signed as the winner's "win" for its Who. A Bid announced row is about a bidder, so the instruction's words suggest Count 1 while the checker rejects it.
- **Alex:** V¶32, V¶85, V¶111, V¶126, V¶137, V¶181 (black): signing and its announcement are separate rows; the sale-process announcement is separate from the merger announcement. He does not address Count. STATUS: "clarify the Count wording on announcement rows."
- **Type / severity:** AMBIGUOUS, Medium (it affects every deal, but not live counts if the checker is followed).
- **Deals where it bites:** all nine (every deal has a signing and a merger announcement); Petsmart and Synacor also have sale-process announcements; any deal with a public bid has Bid announced.
- **Recommended fix.** Replace D1 col 20 (L68) with:

  > 20. **Count**: the bidder units the row's Who stands for: 1, or the number the filing states or exact arithmetic gives (E3). Fill it on Target interest, Bidder interest, Contact, NDA signed, bid rows, Exclusivity changed, exit rows, Re-entered, and Other material event rows about bidders. Merger agreement signed: Who is the winning bidder unit and Count is 1. Required on Process terminated, Process restarted and Bidding group changed (E4, E5). Blank on Target sale decision, Activist, Adviser, Adviser ended, Round opened, the deadline rows, Go-shop changed and the announcement rows (Sale process announced, Bid announced, Merger announced), even where Who names a bidder: a public disclosure does not change who is participating.

  And add to D2, L99: "Who on Sale process announced and Merger announced is the target; on Bid announced, the bidder whose bid became public."
- **Checker change:** add Target sale decision, Activist and Go-shop changed to `NO_BIDDER_COUNT_EVENTS`; add a rule that Merger agreement signed has Count 1 (error) and a Who that also appears on an earlier bid row (warning).
- **Needs Alex?** No. Austin decides.
- **Confidence:** High.

### D4. Events after signing: the signed acquirer's revisions

- **Instruction:** E2, L149: "After signing, record only the merger announcement, competing proposals and their process events, go-shop activity, and termination of the agreement." E6, L193: post-signing events outside an organized solicitation are round "post".
- **Alex:** V¶104 (black): in a post-signing contest the signed acquirer offered $16.99, then $16.55 with other changes, then returned to $16.99; the AI recorded only the $16.55 and not the reversion. "We need to figure out how to be careful about this." He suggests checking the last bid against the financial adviser's opinion section. V¶105: "this deal has a public round of bidding". Filing check: Meredith, p. 76 (the page footer following the passage), "On May 31, 2021, Gray … reduced its offer to $2.803 enterprise value ($16.55 per share in cash)", after the May 3 signing.
- **Type / severity:** AMBIGUOUS, Medium. "Competing proposals" reads as third-party proposals; the signed acquirer's own revisions and agreement amendments are not clearly admitted. E10 (L237) would record a return to an older price, but only if the row is admitted first.
- **Deals where it bites:** Meredith (descriptive only under the settled ruling; that ruling stands); any deal with a post-signing topping contest and matching rights.
- **Recommended fix.** Replace the last sentence of E2 (L149) with:

  > After signing, record only: the merger announcement; each proposal from a party other than the signed acquirer, and the process events around it; each change the signed acquirer offers or agrees to in price, consideration or its commitments, including a return to an earlier offer (a Bid or Other-scope bid row, by E1, coded under E10); an amendment of the merger agreement that changes them; go-shop activity; and termination of the agreement.

  And add to C step 4 (L37): "Check the last agreed price and consideration against the filing's summary of the merger agreement and the financial adviser's opinion; if they differ from your last row, reread the background."
- **Checker change:** none.
- **Needs Alex?** No.
- **Confidence:** Medium-high.

### D5. What is collected now and what is left for enrichment: share count, net debt, market price, separations

- **Instruction:** E13, L283: "fill the price cells only if the filing gives a per-share figure"; a total or enterprise value "goes in the Note with its basis"; "A stated reference price or premium goes in the Note"; "If bids are not per share or not in US dollars, say so in Deal facts." D5 (L125) has no field for shares outstanding, net debt or a separation. E13, L285: "spun-off shares are not consideration."
- **Alex:** V¶100 (blue): the filing gives net debt allocated to the remaining segment, which converts enterprise values to equity per share. V¶142 (Claude's reading): "capture net debt and shares outstanding so enterprise-value and per-share offers can be normalized." V¶185 (black): EV-based bids should be flagged. V¶117 (black): track the target's stock price through the process, because a lower dollar bid may be a higher premium. V¶97 (black): whether a spin-off completed before the sale decides whether the deal can be estimated. CI p.2: `bid_value` is divided by shares outstanding (`cshoc`, from COMPUSTAT) to get `bid_value_pershare`; "The only relevant thing for us is bid_value_pershare." STATUS lists "the missing market-price / EV-normalization work".
- **Type / severity:** MISSING, Medium. The extractor is barred from converting (correctly, since the share count is a judgment), but nothing records the inputs the filing itself gives, so the conversion later means rereading the filing.
- **Deals where it bites:** Meredith (EV and dollar-total bids, separation; settled as descriptive only, so the fields serve reduced-form work); any deal where early bids are totals or enterprise values.
- **Recommended fix.** Add three Deal facts fields after "Currency and units of bid prices" (L125):

  > **Share count**: the fully diluted share count the filing states, with its date and page, where any whole-company bid is stated other than per share; else "Not needed". **Net debt**: the net debt, or the bridge from enterprise to equity value, the filing states, with date and page, where any bid is stated as enterprise value; else "Not needed". **Separation**: any spin-off or segment sale the deal depends on, with its announcement and completion dates; else "None".

  Add to Part A after L20: "Market prices, premiums computed from market data, and share counts from databases are added after extraction. Record a reference price or premium only where the filing states it (E13)."
- **Checker/schema change:** `FACT_FIELDS` gains the three fields; `derive_analysis.py` writes them to `deal.csv`.
- **Needs Alex?** Yes. "For bids stated as totals or enterprise values, should the per-share conversion use the fully diluted count in the fairness opinion, the basic count at the record date, or COMPUSTAT `cshoc`? And is the conversion done by us after extraction rather than by the AI?"
- **Confidence:** Medium.

### D6. Activist presence against activist initiation

- **Instruction:** D2, L86: "**Activist**: a shareholder presses the target for a sale." D5, L129: Initiation is "activist-influenced if an Activist row precedes round 1".
- **Alex:** V¶119 (black): the sTec activist "did not openly try to make the target sell itself" but suggested selling as one option; "I do not think that the sale process here is driven by the activist pressure … But it is still worthwhile to record the presence of an activist who would not be against the sale." V¶39 (black): Mac-Gray initiation is "a bit of both"; keep all interactions so initiation can be reinterpreted. CI p.5: 'Activist Sale' "if an activist is pressuring the target to sell itself". Filing check: sTec, December 6, 2012 Balch Hill letter "urging our board to reduce costs, focus on products with a SAS interface, and explore strategic alternatives".
- **Type / severity:** CONFLICT, Medium. Under the current text the extractor must choose between leaving out an activist Alex wants recorded (if "explore strategic alternatives" is not "presses for a sale") or coding the deal activist-influenced, which Alex rejects.
- **Deals where it bites:** sTec (STATUS audit item, now checked against the filing); Petsmart (activist demanding a sale; activist-influenced is right there).
- **Recommended fix.** Replace D2 L86 with:

  > **Activist**: a shareholder urges the target, publicly or in a communication the filing reports, to sell itself or to explore strategic alternatives. The Note begins "Demands sale" or "Sale one option", and quotes the demand.

  Replace the first clause of D5 L129 with: "activist-influenced if an Activist row whose Note begins 'Demands sale' precedes round 1 of process 1; an activist that lists a sale as one option is recorded but does not decide Initiation."
  Mixed initiation (V¶39) needs no change: the ledger keeps the sequence of Target interest, Bidder interest and Bid rows, and D5's rule gives one reading.
- **Checker/schema change:** `derive_analysis.py` Initiation derivation must read the Note prefix on Activist rows.
- **Needs Alex?** Yes. "When an activist urges the board to 'explore strategic alternatives' among other demands, should the deal count as activist-influenced, or only when the activist demands a sale?"
- **Confidence:** High on the conflict; medium on the wording.

### D7. Facts that rest on two passages: one quote, no reasoning

- **Instruction:** B, L30: "Copy it exactly, from one passage, at most 30 words, with the printed page." D1 col 23 (L71): Note has "No reasoning or justification". A, L20: "state the coding, not the reasoning".
- **Alex:** V¶17 (black): cross-paragraph dating (Providence round-two bids fixed to July 20–22 from three passages) "should be flagged for human review". V¶45 (red): Mac-Gray Party A's NDA is dated from p. 34 against a total on p. 32. V¶57 (magenta): Petsmart's fourth ≥$80 bidder is deduced across passages. V¶110 (red): "it is important to understand why the AI has made this judgment". V¶170: the human should be sent "directly … to the relevant part of the deal background".
- **Type / severity:** AMBIGUOUS, Medium. The row can cite only one page, so the reviewer cannot find the second passage that decides the date, count or identity, and the ban on reasoning removes the pointer.
- **Deals where it bites:** Providence, Mac-Gray, Petsmart, Kraton (Party H and I types on p. 35 against the contact total).
- **Recommended fix.** Add to B after L30:

  > Where a row's date, count or bidder identity also rests on a passage on another page, end the Note with "Also p. N" for each such page. This is a pointer, not reasoning.

  And D1's Review category (d) flags the row (see D1).
- **Checker change:** allow and ignore a trailing "Also p. N" in Note; optionally check that N is within Background pages.
- **Needs Alex?** No.
- **Confidence:** Medium-high.

### D8. Advisers: renamed banks, unclear clients, non-target and non-financial advisers

- **Instruction:** D2, L87: "one Adviser row per target financial or legal adviser, when first shown selected or acting … Bidders' advisers go in the Note of the bidder's first row." Adviser ended exists. D5 fields: Target financial advisers, Target legal advisers.
- **Alex:** V¶29 (black): a bank acquired and renamed mid-process is one adviser. V¶73 (black): record whom advisers act for (winner and a large shareholder, SEACOR). V¶98 (blue): the tax adviser matters because it can push the deal structure. V¶182 (black): one line per adviser; "Any time an affiliation of an advisor is unclear, this should be flagged". V¶152: an unnamed bank recorded as the target's was Company A's. CI p.6: record the primary adviser, else all.
- **Type / severity:** MISSING, Low. The first-mention and one-row rules are covered; the rename could produce a spurious Adviser ended and a second Adviser row; shareholder and tax advisers have no place.
- **Deals where it bites:** Providence (renamed bank), Penford (SEACOR's counsel), sTec (Company A's bank), Meredith (Deloitte, tax).
- **Recommended fix.** Replace D2 L87 with:

  > **Adviser; Adviser ended**: one Adviser row per target adviser (financial, legal, or another the filing names, such as tax), when first shown selected or acting; the Note gives its role. A bank renamed or acquired during the process stays one adviser, with both names in the Note and no Adviser ended row. Advisers to a bidder go in the Note of the bidder's first row; advisers to a shareholder, in the Note of that shareholder's first row. An adviser whose client is unclear is a Review item (F).
- **Checker change:** none.
- **Needs Alex?** Yes, briefly. "Should target advisers other than financial and legal ones (for example tax) get their own rows?"
- **Confidence:** Medium.

### D9. The filing link in the workbook

- **Instruction:** B, L30 and D1 col 24 (L72) give the printed page per row; D5 has "Filing type and date" but no link.
- **Alex:** V¶170 (black): "we should also record the deal background link, including the page, in the database". CI p.2 lists URL among the most important fields.
- **Type / severity:** MISSING, Low.
- **Deals where it bites:** all.
- **Recommended fix.** Tool-side, not extractor-side (the extractor must not use the web and does not receive the URL): the runner writes a Deal facts field "Filing link" from `raw_filing/MANIFEST.csv` `source_url` after the run, and the review list (D1) links each item to the page. Add to D5's field list, after Filing type and date, "Filing link (filled by the runner; leave empty)".
- **Checker change:** `FACT_FIELDS` gains "Filing link", allowed empty.
- **Needs Alex?** No.
- **Confidence:** High.

### D10. Public, private and non-US status of bidders

- **Instruction:** D1 col 4 (L52) and E3 (L159): Type is Strategic, Financial, Mixed or Unknown only.
- **Alex:** CI p.7 (collection instructions, not repeated in the voice notes): "also record status as public vs private and non-US if information is available", e.g. "non-US public S".
- **Type / severity:** MISSING, Low. Possibly dropped on purpose; the voice notes never ask for it.
- **Deals where it bites:** any deal with a foreign or listed bidder.
- **Recommended fix.** If Alex still wants it, add to E3's Type paragraph: "On a bidder's first row, the Note says 'public', 'private' or 'non-US' where the filing states it." No new column.
- **Checker change:** none.
- **Needs Alex?** Yes. "Your 2026 collection instructions record public/private and non-US status for each bidder. Do you still want that, and is a Note enough?"
- **Confidence:** Medium.

### D11. Go-shop undefined

- **Instruction:** D2, L101: "Go-shop changed: a change to or the end of a go-shop; Round opened records its start". E6, L193: "An organized go-shop opens the next round of the same process."
- **Alex:** V¶113 (black): "I am not sure if the AI understands what a go-shop is", defining it as the target approaching additional bidders after signing; "This has clearly not happened here." Filing check: the Synacor SC TO-T has no occurrence of "go-shop".
- **Type / severity:** AMBIGUOUS, Low.
- **Deals where it bites:** Synacor (a false go-shop); any deal whose agreement has a go-shop clause but no reported solicitation.
- **Recommended fix.** Add to E6 after L193:

  > A go-shop is a period after signing in which the merger agreement lets the target solicit competing proposals. Open a round for it only where the filing reports that the target or its adviser contacted parties under that clause. A clause with no reported solicitation goes in the Note of Merger agreement signed with its end date. Post-signing contacts without such a clause are not a go-shop.
- **Checker change:** none.
- **Needs Alex?** No.
- **Confidence:** Medium-high.

### D12. Dating NDAs by the sending of information

- **Instruction:** E7, L199: "If the filing dates only the sending of the agreement or of information, When is 'by [that date]'."
- **Alex:** V¶12 (black): the AI "misreads the memorandums that have been offered to bidders who have already signed NDAs as separate NDA agreements … and they get double counted." V¶134.
- **Type / severity:** AMBIGUOUS, Low. The clause dates an NDA the filing reports; it does not create one. But "or of information" invites treating a memorandum mailing as NDA evidence, which is the error Alex names.
- **Deals where it bites:** Providence, Mac-Gray, Kraton.
- **Recommended fix.** Replace the sentence in L199 with:

  > If the filing reports that a party signed but dates only the sending of the agreement, or of information that went only to signers, When is "by [that date]". Sending a memorandum or opening a data room never creates an NDA signed row or adds a signer.
- **Checker change:** none.
- **Needs Alex?** No.
- **Confidence:** Medium.

### D13. Per-round counts stated twice

- **Instruction:** D3 cols 5 and 9 (L112, L116): "Who was in: … number, by type, with names"; "Bids received: the number of whole-company bidder units that bid in the round". E14 L308: live units are built from rows and "Count is not summed across rows".
- **Alex:** V¶13 (black): participation counts are "a constructed variable, and it is not a fact that we extract". V¶134.
- **Type / severity:** ADDED, Low. The ledger follows Alex (no count rows). The Rounds sheet asks the extractor to restate counts that `derive_analysis.py` rebuilds from rows and then compares ("disagreements with the Rounds sheet"). Useful as a cross-check, but when they disagree nothing says which governs.
- **Deals where it bites:** all multi-round deals.
- **Recommended fix.** Add to D3 after L106: "Who was in and Bids received restate the ledger's rows for the round. Where they disagree, correct whichever misstates the filing so that they agree."
- **Checker change:** none (derive already compares).
- **Needs Alex?** No.
- **Confidence:** Medium.

### Checked and found consistent (no change)

- **Signing, merger announcement and sale-process announcement** (V¶32, 85, 103, 111, 126, 137, 181): D2 L99–100 and E5 L173 (Process terminated only when the filing says the attempt ended) cover them. Only Count/Who needed work (D3).
- **Deadline set, revised, reached; no-deadline rounds** (V¶15, 61–63, 75, 122–124, 174 recording part): E9 L221–231, D3 cols 6–7. The flagging part is D1.
- **Event order and same-day order** (V¶59, 180): E8 L217. Sort date uses Date from, not a midpoint, which answers V¶10; CI p.2's mid-month midpoint is superseded, and Alex says exact dates matter less than order (V¶180, CI p.2).
- **Invented high-confidence facts** (V¶50, 141): B L24–30 (reported fact, exact calculation or convention; one exact quote), and the checker confirms each quote occurs in the filing. The checker proves occurrence, not support, so D1's review list remains necessary.
- **Contacts after NDA not recorded; declined contacts get no exit** (V¶14, 70): E7 L199, E3 L157, E14.
- **IOI and bid are one row** (V¶183): E10 L235 "One communication is one row".
- **Conditions in the bid's own row; absence of financing recorded** (V¶46–47): D1 cols 14–19, E12 H1.
- **Termination fees:** E10 L235; Alex does not ask for them; STATUS settled ruling ("Target termination fees go in dated Notes"). Not reopened.
- **Honesty about uncertainty:** "Inferred = Y" (B L24), qualified counts kept (E3 L163), no invented ranges (B L26), and Questions with a recommendation (F). What is missing is the mandatory review, not honesty (D1).

---

## Part 2. Coverage sweep, V¶1–V¶187

Status values: Covered, Partly, Not covered, Conflicts, No request (headings, legend, motivation, figures, summaries that add no new request), Out of scope (Alex says not this project). Lanes A (rounds, stages), B (bid terms), C (participants, exits) are marked; their auditors hold the depth. Colour in brackets where not black.

| V¶ | Request or ruling (short) | Status | Instruction clause | Lane / item |
|---|---|---|---|---|
| V¶1 | Title | No request | — | — |
| V¶2 | Legend: black | No request | — | — |
| V¶3 | Legend: red [8B0000] | No request | — | — |
| V¶4 | Legend: blue [0000CD] | No request | — | — |
| V¶5 | Legend: magenta [8B008B] | No request | — | — |
| V¶6 | Legend: grey [595959] | No request | — | — |
| V¶7 | Heading: Providence | No request | — | — |
| V¶8 | Intro | No request | — | — |
| V¶9 | Quarter = 90-day window; "week of" = 7 days | Covered | E8 L209–210 | D |
| V¶10 | Assigned date interpolated wrongly from bounds | Covered | E8 L217 (Sort date = reported day or Date from; no interpolation) | D |
| V¶11 | Contact and NDA are separate events | Covered | E7 L199 | D/C |
| V¶12 | No double counting; memoranda are not NDAs; only NDA signed | Covered (residual) | E7 L199, E3 L157 | D12 |
| V¶13 | Participation count is constructed, not extracted | Covered | E14 L308; no count rows | D13 |
| V¶14 | Do not record contacts after NDA | Covered | E7 L199 (first contacts); E2 L149 | C |
| V¶15 | Deadline set vs deadline expired are different dates | Covered | E9 L221 | A |
| V¶16 | Merge round_index and round_count | Covered | D1 col 7 L55 (one Round column) | A |
| V¶17 | Order must follow narrative; cross-paragraph dates; flag for review | Partly | E8 L215–217 order and bounds; flag missing | D1, D7 |
| V¶18 | Providence G&W July 26 revision stays in round two; July 27 as deadline | Partly | E6 L189 (extra time continues round); E9 L226 late bid accepted | A |
| V¶19 | Markup = formal; separate none/light/heavy conditions [red] | Covered | E11 L251; E12 L263–277 | B |
| V¶20 | Flexibility to reinterpret formality in estimation [red] | Covered | A L16; STATUS estimation variants | B |
| V¶21 | Two admitted bidders don't bid; identify who [magenta] | Partly | E14 L302–304 (rules 3–4) | C |
| V¶22 | Party A never left round one; the dropout is unnamed [magenta] | Partly | E14 L302 (named bidder never mentioned again: Did not submit at due date) | C |
| V¶23 | Why the first approacher matters [magenta] | No request | — | — |
| V¶24 | Such inference needs human judgment [magenta] | Partly | no flag for it | D1 |
| V¶25 | Infer unstated round starts [red] | Covered | E6 L187 (inferred Round opened) | A |
| V¶26 | Finality often unstated; late LOIs quite formal [red] | Partly | E6 L195; E11 L251 (labels do not decide) | A/B |
| V¶27 | Negotiating agreement with one bidder signals final round [red] | Covered | E6 L184 trigger (c); L195 Inferred final | A |
| V¶28 | Scan all paragraphs of a round for finality [red] | Covered | C1 L34 | A |
| V¶29 | Renamed bank is one adviser | Not covered | D2 L87 silent | D8 |
| V¶30 | Reconfirmed offer with clean markup becomes formal; new row [red] | Covered | E10 L237, L243; E11 L251 | B |
| V¶31 | Judgment needed [red] | No request | — | — |
| V¶32 | Record signing and announcement dates separately | Covered | D2 L99; D5 L125 | D |
| V¶33 | Why announcement date matters | No request | — | — |
| V¶34 | Learn from hand-coded major facts | No request (evaluation, not extraction; AGENTS forbids reading ref/) | — | — |
| V¶35 | Austin to read backgrounds; keep adjusting | No request | — | — |
| V¶36 | Heading: Mac-Gray | No request | — | — |
| V¶37 | Intro | No request | — | — |
| V¶38 | Target approached first: Target interest, not Bidder interest | Covered | D2 L83; D5 L129 | D/C |
| V¶39 | Mixed initiation; keep all interactions | Covered | ledger rows kept; D5 L129 gives one reading | D6 |
| V¶40 | Contact event with counts missing | Covered | E7 L199 (reconcile to totals); E3 L161 | C |
| V¶41 | NDA arithmetic: named plus cohort | Covered | E3 L161 | C |
| V¶42 | Round one starts at the June 24 decision; July 23 deadline | Covered | E6 L191 | A |
| V¶43 | Duplicated advisers | Covered | D2 L87 (one row per adviser) | D8 |
| V¶44 | Round two July 25; deadline announced Aug 27 | Partly (lane A to confirm against E6 L187) | E6 L182, L187; E9 L221 | A |
| V¶45 | Party A NDA Aug 5; no double count across pages [red] | Covered | E3 L161; cross-page pointer missing | C, D7 |
| V¶46 | Conditions recorded as a separate row | Covered | D1 cols 14–19 | B |
| V¶47 | Conditions on the bid row; record lack of financing | Covered | D1 cols 14–19; E12 L258, L267 | B |
| V¶48 | Best-and-final range stays formal; reinterpret later | Covered | E11 route 2; E13 L281 | B |
| V¶49 | Exclusivity does not downgrade formality | Covered | A L16; E12 L261, L277 | B |
| V¶50 | Invented facts; more human verification [red] | Partly | B L24–30 (evidence); review missing | D1 |
| V¶51 | Record legal adviser's first mention | Covered | D2 L87 | D8 |
| V¶52 | Summary | No request | — | — |
| V¶53 | Heading: Petsmart | No request | — | — |
| V¶54 | Intro | No request | — | — |
| V¶55 | First week + meeting narrows date; meeting starts round one | Covered | E8 L209, L213–215; E6 L191 | D/A |
| V¶56 | "At least 27" where the filing is exact | Covered | E3 L163 | C |
| V¶57 | Hidden fourth ≥$80 bidder by arithmetic [magenta] | Partly | E3 L161; E13 L281 | C/B, D7 |
| V¶58 | Note it even if rare [magenta] | Partly | as V¶57 | C |
| V¶59 | Same-bidder same-day bids in text order | Covered | E8 L217 | D |
| V¶60 | Target drops two IOI bidders; nine NDA-only reasons unknown | Covered | E14 L291, L304, L310 | C |
| V¶61 | Two-day extension continues round two | Covered | E6 L189; E9 L221 | A |
| V¶62 | Record deadline revisions as rows | Covered | E9 L221 (Deadline revised) | A |
| V¶63 | Cheap to collect revisions | Covered | E9 L221 | A |
| V¶64 | Rollover is not a consortium | Covered | E4 L167 | C |
| V¶65 | Summary | No request | — | — |
| V¶66 | Heading: Penford | No request | — | — |
| V¶67 | Intro | No request | — | — |
| V¶68 | Approach citing stock price is Bidder interest, not a bid | Covered | D2 L84; E10 L247 | B/C |
| V¶69 | Winner type always findable in filing | Covered | E3 L159; C1 L34 | C, D1 |
| V¶70 | Declining contact: contact only, no exit; never-contacted gets no row | Covered | E7 L199; E3 L157; E14 | C |
| V¶71 | Round one starts when the sale process starts | Covered | E6 L191 | A |
| V¶72 | Oct 3 board directive opens final round two [red] | Covered | E6 L184 (c); L195 | A |
| V¶73 | Record whom legal advisers act for (winner, shareholder) | Partly | D2 L87 (bidder advisers in Note); shareholder advisers not placed | D8 |
| V¶74 | Oct 14 confirmation is a formal bid | Covered | E10 L245; E11 route 3 | B |
| V¶75 | No-deadline rounds recorded as such | Covered | D3 L113–114 | A |
| V¶76 | Remaining non-winners drop at end; exclusivity drops rivals | Covered | E14 L301, L304 | C |
| V¶77 | Summary | No request | — | — |
| V¶78 | Heading: Kraton | No request | — | — |
| V¶79 | Intro | No request | — | — |
| V¶80 | Exact NDA and contact counts by type | Covered | E3 L161–163; E7 L199 | C |
| V¶81 | Winner type from "parties" chapter; flag Unknown winner and formal bidders | Partly | E3 L159 covered; flag missing | C, D1 |
| V¶82 | Kraton: July 6 opens second informal round | Conflicts | E6 L187–189 (STATUS ruling: reconcile generally) | A |
| V¶83 | Exit reasons: below market, at IOI, below IOI | Covered | E14 L310 | C |
| V¶84 | Earnout is not a mixed offer | Covered | E13 L285–287 | B |
| V¶85 | Signing and announcement are two rows | Covered | D2 L99 | D |
| V¶86 | Summary | No request | — | — |
| V¶87 | Heading: Meredith | No request | — | — |
| V¶88 | Intro | No request | — | — |
| V¶89 | [grey] Shreye on bid/market ratio | No request | — | — |
| V¶90 | [grey] Spin-off timing question | No request | — | — |
| V¶91 | [grey] Remainco market price options | No request | — | — |
| V¶92 | [grey] Spin-off facts | No request | — | — |
| V¶93 | [grey] Remainco share of price | No request | — | — |
| V¶94 | [grey] DCF range | No request | — | — |
| V¶95 | [grey] Meredith out of estimation, kept for descriptive | Covered (settled) | STATUS settled; `DESCRIPTIVE_ONLY` | — |
| V¶96 | Segment-sale discussion is not the start of a sale | Covered | E1 L139 | A |
| V¶97 | Partial-only deal must be flagged; spin-off timing decides use | Partly | D5 "Whole-company bids"; E1; no flag; no separation field | D1, D5 |
| V¶98 | [blue] Tax adviser worth noting | Not covered | D2 L87 (financial or legal only) | D8 |
| V¶99 | [blue] Levered-asset bid not comparable | Partly | E1 L139 (unresolved scope → Other-scope); E13 L283 | B |
| V¶100 | [blue] Net debt converts EV to equity per share | Partly | E13 L283 (Note with basis); no net-debt field | D5 |
| V¶101 | [magenta] Merger-agreement provisions for another project | Out of scope | E2 L149 folds legal terms | — |
| V¶102 | [magenta] Dual proposal is two bids; record the cash-out one | Partly | E10 L235 (separate rows); no preferred marker | B |
| V¶103 | Signing mislabeled as termination and sale announcement | Covered | D2 L99–100; E5 L173 | D |
| V¶104 | Post-signing back-and-forth by signed acquirer; check against opinion | Partly | E2 L149 ambiguous | D4 |
| V¶105 | Lessons: $ vs per share, EV, public round, partial bids | Partly | D5 currency field; E13 L283; E6 L193; E1 | D4, D5 |
| V¶106 | Heading: Synacor | No request | — | — |
| V¶107 | Processes vs rounds is the question | Covered | E5 | A |
| V¶108 | 9-month gap is a new process [red] | Covered | E5 L171 | A |
| V¶109 | 4-day gap after exclusivity is not a new process [red] | Covered | E5 L171(a); E6 L185 (d) | A |
| V¶110 | Flag multi-process deals; know why [red] | Covered | F L345 (process Question with E5 results) | A/D |
| V¶111 | Sale-process vs merger announcement | Covered | D2 L99 | D |
| V¶112 | Winner type from financing context | Covered | E3 L159 | C |
| V¶113 | Go-shop misunderstood | Partly | D2 L101; E6 L193; no definition | D11 |
| V¶114 | Summary | No request | — | — |
| V¶115 | Heading: sTec | No request | — | — |
| V¶116 | Winner lowered its offer late | Covered | E10 L237 | B |
| V¶117 | Track target stock price through the process | Not covered (enrichment) | E13 L283 stated reference only | D5 |
| V¶118 | sTec: 3-month gap, two processes | Covered | E5 L171 (90 days) | A |
| V¶119 | Activist present but not the initiator; record it | Conflicts | D2 L86; D5 L129 | D6 |
| V¶120 | New board member is not a consortium | Covered | E4 L167 | C |
| V¶121 | "At least" NDAs; duplicate contacts | Covered | E3 L163; E7 L199 | C |
| V¶122 | Soft May 3 deadline [red] | Covered | E9 L228 (Passed without action) | A |
| V¶123 | Record whether deadlines were enforced [red] | Covered | E9 L223–231; D3 col 7 | A |
| V¶124 | May 16 drops start informal round two [red] | Covered | E6 L182 (a) | A |
| V¶125 | WDC May 28 markup IOI is formal, not final round [red] | Covered | E11 L251 route 1 | B |
| V¶126 | Signing and announcement separate | Covered | D2 L99 | D |
| V¶127 | Summary; soft deadlines | Covered | E9 | A |
| V¶128 | Heading: Summary | No request | — | — |
| V¶129 | Heading: Claude's reading | No request | — | — |
| V¶130 | Intro | No request | — | — |
| V¶131 | Round boundaries from target decisions; start and deadline distinct | Partly | E6; E9 (Kraton conflict, V¶82) | A |
| V¶132 | Gap-plus-continuity; flag multi-process deals | Covered | E5 L171; F L345 | A |
| V¶133 | Cross-reference dates; flag such deals | Partly | E8; flag missing | D1, D7 |
| V¶134 | Double counting; count constructed | Covered | E3, E7, E14 L308 | C, D13 |
| V¶135 | Conditionality flag; revisions to formal | Covered | E11, E12 | B |
| V¶136 | Always resolve and flag winner/formal-bidder type | Partly | E3 L159; flag missing | D1 |
| V¶137 | Three dates distinct | Covered | D2 L99 | D |
| V¶138 | Advisers: dedupe, first mention, client, renames | Partly | D2 L87 | D8 |
| V¶139 | Missing events; same-day order | Covered | E7 L199; E8 L217 | D |
| V¶140 | Dropout precision; no rows for never-contacted | Covered | E14 | C |
| V¶141 | Invented facts imply mandatory verification | Partly | B; review missing | D1 |
| V¶142 | Flag deals without whole-company bids; capture net debt and shares | Partly | D5 fields; E13 | D1, D5 |
| V¶143 | Extensions, soft deadlines, no-deadline; rollover not consortium | Covered | E9; D3; E4 | A/C |
| V¶144 | Heading: Excel comments | No request | — | — |
| V¶145 | Intro and counts | No request | — | — |
| V¶146 | Round boundaries (56 rows) | Partly | E6 (as V¶131) | A |
| V¶147 | Missing and duplicate rows; mixed totals duplicating S+F | Covered | E3 L161; D2 L87; E10 L235 | C |
| V¶148 | Type labeling; cohort types; flag Unknown winners | Partly | E3 L159–161; flag missing | C, D1 |
| V¶149 | Counts; rows that should not exist | Covered | E2 L149; E3; E4; E9 L221 | C |
| V¶150 | Conditions as structured data; partial bids | Covered | E12; E13; E1 | B |
| V¶151 | Wrong dates; dropouts for never-contacted; reason names | Covered | E8; E14 | C |
| V¶152 | Advisers mis-attributed; formal mislabels | Partly | D2 L87; E11 | D8, B |
| V¶153 | Long tail list | Covered | per items above | — |
| V¶154 | Which deals suffer most | No request | — | — |
| V¶155 | Summary of fixes | Covered | per items above | — |
| V¶156 | Heading: Figures | No request | — | — |
| V¶157 | (empty) | No request | — | — |
| V¶158 | [grey] Figure 1 caption | No request | — | — |
| V¶159 | (empty) | No request | — | — |
| V¶160 | [grey] Figure 2 caption | No request | — | — |
| V¶161 | (empty) | No request | — | — |
| V¶162 | [grey] Figure 3 caption | No request | — | — |
| V¶163 | (empty) | No request | — | — |
| V¶164 | [grey] Figure 4 caption | No request | — | — |
| V¶165 | (empty) | No request | — | — |
| V¶166 | [grey] Figure 5 caption | No request | — | — |
| V¶167 | Heading: Alex's summary | No request | — | — |
| V¶168 | Endorses Claude's reading | No request | — | — |
| V¶169 | Interactive, real-time flagging | Conflicts | C L34–37; F L353 (batch delivery) | D2 |
| V¶170 | Wrong round count forces renumbering; record link and page | Partly | B L30 page; no link; no checkpoint | D2, D9 |
| V¶171 | Accepts no large background batches for now | Conflicts | batch model (AGENTS, F) | D2 |
| V¶172 | Always flag the following | Conflicts | F L343 (cap; default never a Question) | D1 |
| V¶173 | A: round-ending meetings, drops, first outreach; rounds from process not labels | Conflicts (flag); Covered (inference from process, E6 L179) | F L343; E2 L149 folds board review | D1, A |
| V¶174 | B: flag and record extensions or their absence | Partly | E9 records; no flag | D1 |
| V¶175 | C: flag unknown winner type | Partly | E3 L159; no flag | D1 |
| V¶176 | D: flag unknown type of formal bidder | Partly | E3 L159; no flag | D1 |
| V¶177 | E: flag uncertain NDA counts or unsplit types | Partly | E3 L161–163 (Note "Count: …"); no flag | D1 |
| V¶178 | F: flag uncertain exit reasons | Partly | E14 L310 (Not stated); no flag | D1 |
| V¶179 | G: verify conditionality for the first deals | Not covered | — | D1 |
| V¶180 | H: order of events must be precise | Covered | E8 L217 | D |
| V¶181 | I: signing vs announcement, needs no verification | Covered | D2 L99 | D |
| V¶182 | J: one line per adviser; flag unclear affiliation | Partly | D2 L87; no flag | D1, D8 |
| V¶183 | K: IOI and bid one row; flag formal-looking IOIs | Partly | E10 L235 one row; no flag | D1 |
| V¶184 | L: flag partial-only deals | Partly | D5 "Whole-company bids"; no flag | D1 |
| V¶185 | M: flag unclear currency, units, EV vs equity | Partly | D5 currency field; E13 L283 | D1, D5 |
| V¶186 | Other issues (multiple processes) flagged if not learned | Covered | F L345 | A |
| V¶187 | Drop checks as the AI improves | Partly | nothing configurable | D1 |

**Tally of the 187 paragraphs:** No request 55; Out of scope 1; Covered 82; Partly 39; Not covered 4 (V¶29, V¶98, V¶117, V¶179); Conflicts 6 (V¶82, V¶119, V¶169, V¶171, V¶172, V¶173). Not covered or Conflicts: 10.
