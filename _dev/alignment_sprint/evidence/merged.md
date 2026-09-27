# Merged findings: v0 instruction against Alex's conventions

27 September 2026. Four independent Opus 5.5 auditors (lanes A rounds/processes, B bids/Formality/conditions, C participants/exits, D output/work process plus a coverage sweep of V¶1–187) each read the full v0 instruction, the voice notes and the collection instructions, and checked examples against the filings. They did not read `_dev/ALEX_ALIGNMENT.md` (the earlier audit). Full reports with draft instruction text: `lane_A.md`, `lane_B.md`, `lane_C.md`, `lane_D.md` in this folder. Item IDs below (A1, B6, …) point into those files.

64 raw items merge into 37 themes. Severity is the highest of the merged items. "Alex?" means the lanes think Alex must answer before adoption.

Coverage note: lane D's sweep found 4 voice paragraphs "Not covered" (V¶29, V¶98, V¶117, V¶179) and 6 "Conflicts" (V¶82, V¶119, V¶169, V¶171–173). All ten are picked up by themes below (P7, P7, O5, O1; R1, P5, O2, O2, O1, O1).

## R. Rounds, stages and processes

| # | Theme | Items | Sev. | Proposed fix (short) | Alex? |
|---|---|---|---|---|---|
| R1 | A common request for new offers to some but not all of a round's eligible parties opens a round | A1 | High | Rewrite E6(a); eligible = entered and could bid, bid or not; carve-out: follow-ups inside a final round continue it. Passes Kraton July 6 (ruling); must not fire on PetSmart Dec 10, Providence mid-June, Mac-Gray Aug 27 | No (Kraton ruling + V¶173A) |
| R2 | An offer-less selection opens the round at the decision, not at the later request | A2 | High | Replace E6 l.187 sentence; non-selected parties' drops date at the decision. Moves Mac-Gray round 2 to July 25 (Alex V¶44), Kraton round 3 to July 20, Providence round 2 to June 1 | Yes (confirm general) |
| R3 | Trigger (d) (30-day pause / exclusivity expiry) is not Alex's; interacts with R2 | A3 | Med (High with R2) | Tighten (d): only after the previous round ended and no stage in progress; carrying out a decided stage is not "again". Otherwise R2 + (d) gives Mac-Gray four rounds | Yes (Datalink Oct 2016) |
| R4 | Finality: "final round" label vs a request for non-binding offers; can a final round be informal; how far route 2 reaches | A4, B4, B5, B20 | High | A4: offer Alex Rule L (label) vs Rule S (substance; sTec 3 rounds). Decouple E11 route 2 from the label. B4: route 2 covers every bid by an invited finalist in a round announced final (CI p.9). B5: new raw Rounds column "Solicitation asked for" (words on finality, binding, markup requested). B20: no change | Yes (already open in STATUS) |
| R5 | Round 1 in bidder-approached deals starts at the target's sale/market-check decision, not the first NDA | A5 | High | Replace the "where buyers came to the target" clause of E6 l.191. Penford Aug 10 $18 becomes round 0. Side effect: purely bilateral deals get a single final round 1 | Yes (thin evidence: V¶71 omits $18 but never says round 0) |
| R6 | Rounds and the sale decision only for whole-company outreach | A6 | High | Insert "for the whole company (E1)" in E6 l.179, l.191 and D2 l.85. Stops Kraton's 2020 CST-segment outreach opening a round (else 4 rounds) | No (V¶96, CI p.7) |
| R7 | Round dating and ordering details | A7, A8, A13, A14 = C14 | Low | Undated outreach following a decision dates at the decision; an unreported opening dated "by first offer" with Date from = end of previous round; a late answer to an earlier solicitation carries the round open when it arrives; on one date, Round opened precedes the exits it causes (CI p.8) | No |
| R8 | Process boundary: 90 days measured from which contact; MOE / target-as-buyer talks inside the gap | A9, B14 | High | A9: choose Rule C (latest supported date; sTec one process, against V¶118) or Rule M (calendar months when an end is month-dated; sTec two processes). Add "a message that only ends talks is not a contact". B14: MOE and target-buying talks are not sale contacts or negotiation for E5 (Synacor Company D) | Yes (already in STATUS) |
| R9 | Deadline outcomes: "Enforced" should mean decisive action; record the effective close | A10, A11 | Med | Enforced = selected/excluded bidders, opened next stage, or chose a bidder; board review or feedback alone = Passed without action. None of 13 checked deadlines changes. Add "(last late response [date])" to Extended | No |

## F. Formality, conditions and prices

| # | Theme | Items | Sev. | Proposed fix (short) | Alex? |
|---|---|---|---|---|---|
| F1 | Route 1: documents sent at another time make a bid Formal ("in support of one" has no time limit) | B1 | High | Route 1 only when the markup comes with the priced proposal or in the response to a request for both price and documents; "Formality is judged at the bid's communication; the window applies to conditions". Penford Aug 10, Sep 17, Oct 2 become Informal, as Alex codes them | Yes (joint question with F2) |
| F2 | A bidder's later markup with no new price (confirmation by documents) gets no row | B2 | High | New E10 "Confirmation by documents": bidder-submitted draft after definitive negotiation begins = Bid reaffirmed row. Gives Providence Aug 4 (Alex V¶30) but also adds Penford Oct 8, earlier than Alex's Oct 14 | Yes: "What makes Providence Aug 4 a formal bid and Penford Oct 8 / Sep 6 not?" |
| F3 | A price-only revision drops a Formal bidder to Informal | B3 | Med | Either carry route-1 Formality forward while documents stay on the table, or record raw "Documents on table: Y" per bid row and decide at estimation | Yes (already in STATUS "price-only revisions") |
| F4 | H2 carve-out: diligence periods that also cover exclusivity/negotiation escape Heavy | B6 | High | H2 = a period of two weeks or more tied to remaining diligence, alone or with negotiation or exclusivity, not called confirmatory. Replace Example 4. Providence G&W and Party E July LOIs become Heavy | Yes (brief) |
| F5 | Silence gives Unclear where Alex reads "no conditions" | B7 | Med | New Conditions value "None stated" (no trigger, nothing reported); keep Unclear for mixed evidence | Yes |
| F6 | Existing facilities named alongside "no firm financing commitment" | B8 | Med | Where the filing says no firm commitment, Financing is Contingent whatever sources are named (V¶47) | No |
| F7 | "Conditions on proceeding" turns merger-agreement negotiation into Heavy bid rows | B9 | Med | Restrict to conditions outside the definitive documents; positions on agreement terms are negotiation (E2); adviser summaries are not bidder statements. Fixes sTec Jun 20 | No |
| F8 | Regulatory risk never makes a bid Heavy | B10 | Low | Defer to estimation; raw columns already exist. Optional H4 if Alex wants | Yes (low priority) |
| F9 | A commitment letter alone makes a bid Formal by route 1 | B19 | Low | Remove "a commitment letter" from route 1 (V¶47: financing does not change Formality) | Yes (brief) |
| F10 | Contingent extra payment with no stated payment date may be coded a range | B15 | Low | A range only when alternative upfront prices are given; any other future-contingent amount is CVR/earnout (Kraton Party A Sep 24, V¶84) | No |
| F11 | A later passage calling an approach an "indication" makes it a Bid | B13 | Med | Judge from the passage reporting the communication; later labels go in the Note (Penford Jul 17, V¶68) | No |
| F12 | Which alternative structure enters the price series | B17 | Low | Note records the target's stated preference; estimation chooses | No |

## P. Participants, entry, counts, exits, advisers, dates

| # | Theme | Items | Sev. | Proposed fix (short) | Alex? |
|---|---|---|---|---|---|
| P1 | "A named party that may belong to the group stays inside it" is right for entry totals, wrong for later groups | C1 | High | Split the clause: inside for entrant totals; for later-step groups only if the filing places it there or arithmetic requires; a named party whose mentions ended is not placed in a later unnamed group. Protects Providence Party A (settled 16) | No |
| P2 | Re-contacted parties double counted in cohort totals | C2 | Med | Subtract every member already having a row in this process for the same kind of step (V¶13, ¶121) | No |
| P3 | "Record reported exits first" conflicts with the settled non-invitation exit; label for non-invitation | C3 (+ B outside note) | High | A reported exit governs only if it precedes the inferred closing event; later reports set the reason (reproduces sTec Company H). Note "not invited" vs "excluded". TENSION: Penford Party A is dropped at Oct 3 then re-enters Oct 14, while V¶72 says the target was "not explicitly excluding" NDA signers — not reopening the settled rule, but Austin should see it | Yes (label only) |
| P4 | NDA dating from sending of the agreement points the wrong way; memoranda misread as NDAs | C4, D12 | Med | Agreement sent but not signed: no row. Sent date is a lower bound on signing; information sent under it is an upper bound. Sending a memorandum never creates an NDA row (V¶12) | No |
| P5 | Activist presence vs activist initiation; mixed initiation | C5, D6, C6 | Med | Competing schemes: C5 widens Activist to "urges a review of alternatives that includes a sale" and makes Initiation follow the earliest row with "activist present" as a suffix; D6 uses a Note prefix "Demands sale" / "Sale one option" read by derive. C6 adds "target-led, then bidder bid (date)" for Mac-Gray-type cases | Yes |
| P6 | Type splits obtainable by exact arithmetic across passages | C8 | Med | Allow the split when exact arithmetic from the filing's figures gives it (sTec nine decliners = 1 F + 8 S) | No |
| P7 | Advisers: renamed banks, engagement date, tax and shareholder advisers | C9, C10, C11, D8 | Low | One row through a rename; date from engagement on the sale; tax adviser gets a row; shareholder's adviser in that shareholder's Note; unclear client is a review item | Yes (tax, brief) |
| P8 | Date bounds from logical links; Sort date purpose | C12, C13 | Low | Bound undated events by linked dated events (a review bounds from above); state Sort date is for ordering only | No |
| P9 | Bidder names that change within a filing | C15 | Low | One Who string per bidder unit; later name throughout, earlier in Note | No |
| P10 | Public/private and non-US status | C16 = D10 | Low | Note on first row if Alex still wants it (CI p.7 only) | Yes |
| P11 | Does the outreach that opens round 1 get Contact rows? | C17 | Low | Contact includes the outreach that opens round 1 (V¶40) | No |

## O. Output, review and work process

| # | Theme | Items | Sev. | Proposed fix (short) | Alex? |
|---|---|---|---|---|---|
| O1 | Alex's mandatory review flags (V¶169–187) vs the five-Question cap and "applying a default is never a Question" | A12, B18, C7, D1 | High | FOUR COMPETING MECHANISMS: A12 a Rounds "Boundary check" column + forced process Question when an alternative changes the count; B18 fixed "Check:" entries in Questions outside the cap; C7 a Flag value "R" / Review section; D1 tool-generated review list for everything derivable from cells + R-numbered Review items for four non-derivable kinds (meeting within 7 days after a due date, Formal coded IOI/LOI, unclear adviser client, cross-paragraph facts) + checker accepts R ids. Pick one | D1 asks whether post-run review satisfies him |
| O2 | Alex wants flags IN REAL TIME; runs are batch | D2 | High | Checkpoint after Map when a person is present: show processes, rounds, NDA totals, winner type; wait for confirmation. No-person runs unchanged. Cockpit needs a pause step | Yes (+ Austin on cockpit) |
| O3 | Count and Who on announcement and signing rows (Austin's requested clarification) | D3 | Med | Explicit label-by-label Count rule; Merger agreement signed: Who = winner, Count 1; announcements blank; checker list aligned | No (Austin) |
| O4 | Signed acquirer's revisions after signing | B16, D4 | Med | Admit the signed acquirer's changes in price/consideration/commitments, incl. a return to an earlier offer, and amendments; add a final check of last agreed price against the merger-agreement summary and fairness opinion (D4's fuller text) | No |
| O5 | EV / totals / shares / net debt / market price / separation | B11, B12, D5 | Med | Keep E13 (no conversion by extractor). Add Deal facts: value basis, share count, net debt, separation (with page). State in Part A that market prices come from data after extraction | Yes (which share count; confirm CRSP) |
| O6 | Facts that rest on two passages: one quote, no reasoning | D7 | Med | "Also p. N" pointer at the end of the Note | No |
| O7 | Filing link in the workbook | D9 | Low | Runner writes it from MANIFEST.csv; extractor leaves empty | No |
| O8 | Go-shop undefined | D11 | Low | Define; open a round only when solicitation under the clause is reported (Synacor false go-shop, V¶113) | No |
| O9 | Rounds-sheet counts restate the ledger; no rule on disagreement | D13 | Low | Correct whichever misstates the filing so they agree | No |

## Voice notes vs collection instructions (lanes B, A)

Range bids formal (voice) vs informal (CI p.7); partial bids flagged (voice) vs dropped (CI); final informal round allowed (CI p.8); all bids after final letter formal (CI p.9); per-share conversion by dividing (CI p.2) vs net-debt adjustment (V¶100); subset condition for a final round (CI p.7) absent from voice. STATUS lists "conflicting reference sources" as open with Alex.

## Possible slip in Alex's notes

V¶50 names Mac-Gray Parties B and C as dropped on 24 September; the filing shows A and B dropped (exclusivity) and C not submitting on 18 September (lane C, low confidence).
