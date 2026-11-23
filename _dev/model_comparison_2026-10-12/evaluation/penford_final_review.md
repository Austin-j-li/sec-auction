# Penford final comparison

Replacement reviewer report, 12 October 2026. This report completes the original review after its reviewer could not resume.
The original source inventory and interim A/B review remain intact. This report does not replace either file.
The reviewer received neutral labels only. No engine identity or operational receipt informed the judgment.

The reviewer read the source background and current instruction before the candidates. All four sheets of A, B, and C received review.
Important interim claims received independent source checks. Agreement between candidates was not evidence.
No workbook, masked data, instruction, or frozen report changed. No extraction, model call, web request, test, or assertion ran.

Sources are the current instruction, the supplied Penford filing, the protocol, the two permitted Penford reports, and the three masked dumps.
Source lines below refer to `raw_filing/penford_2014-12-29_DEFM14A.htm`. Printed pages accompany those lines.
Candidate references use Excel row numbers. A reference such as `P43` names the cell, not the ledger event number.

## Confirmed findings

These findings were fixed before the final rank. The disputed readings below do not enter these counts.
One cause counts once for each affected candidate, even when it affects several cells.

| Label | Major | Moderate | Minor | Confirmed causes |
| --- | ---: | ---: | ---: | --- |
| A | 0 | 1 | 0 | P1 |
| B | 0 | 1 | 1 | P1, P4 |
| C | 1 | 1 | 2 | P2, P3, P4, P5 |

### P1 — The final reaffirmation omits a stated financing condition

**Moderate. A: Deal ledger P43. B: Deal ledger P48.** Both cells say `Not stated`.

The decisive evidence is the board's dated approval, not an automatic backward application of the executed agreement:

1. On October 14, Fortnum confirmed $19 and the plan to proceed. Source: page 32, lines 2735–2736.
2. That day, the board reviewed the transaction and approved it. Source: pages 32–33, lines 2741–2763.
3. The next section expressly gives the reasons for that unanimous decision. Source: page 33, lines 2766–2769.
4. One reason states that the merger obligation “is not subject to any financing condition.” Source: page 34, line 2842.
5. Execution followed that evening. Source: page 33, lines 2764–2765.

Part B, instruction line 28, admits condition evidence from the reaffirmation to execution.
The board passage reports the proposal's existing condition. It reports no later removal of a financing condition.
E10, line 261, permits a Same-offer row to change a condition reported anew.
E12, lines 285–288, supports `Committed` from the express absence of a financing condition. `Not stated` therefore loses required evidence.

The source also supports the existing-facilities treatment, `Not needed`.
Page 45, lines 4245–4247, describes available cash and the revolving credit agreement.
Section 4.6 states access to sufficient existing facilities as of the agreement date: page A-24, lines 9101–9103.
These passages support C's `Not needed` at Deal ledger P40; they do not recode earlier offers.

A and B retain the financing basis in their execution Notes, W46 and W51.
Those Notes do not fill the earlier required financing cells.
The defect changes one financing observation in each candidate. Price, Formality, participant counts, and the `Unclear` summary remain intact.

This confirms the interim finding through stronger, dated evidence. The result does not depend only on the signed agreement's same-day date.

### P2 — Two exits carry the round entered instead of the round left

**Major. C: Deal ledger G33 and G34.** Both cells say `2` for the inferred exclusions of Parties C and D.

The board selected Ingredion for definitive negotiation on October 3. Source: pages 30–31, lines 2676–2692.
No source invitation preserves C or D in that next stage. Party A receives a separate invitation on October 4.
Source: page 31, lines 2694–2695. D's later refusal appears on October 8, lines 2703–2704.

C itself dates both inferred exits to October 3 and says each party was not invited.
Its Rounds E2/J2 and E3 correctly show four entrants in round 1 and only two in round 2.
The error is in the exit rows' round assignment, not the selected date, party, exit label, or Count.

E8, instruction line 233, explicitly says: “An exit row carries the round being left.”
E14, lines 328–336, closes uninvited parties at the next stage's opening.
The opening marker precedes its caused exits, but those exits still carry round 1.

The wrong cells attach two losses to round 2. They conflict with the stated round population and alter the stage of both exit observations.
That affects participation by stage, the instruction's first research priority. The protocol therefore supports Major severity.
This is one cause affecting two rows. The correct Rounds summary limits the damage but does not repair the ledger cells.

### P3 — An effective date becomes an exact NDA execution date

**Moderate. C: Deal ledger AB4 and AC4; associated B4, AA4, and W4.**
The Date from and Date to cells both say July 20, 2014. The Note admits that the execution day is not stated.

After the July 19 meeting, the source says the parties subsequently executed an agreement “effective as of July 20, 2014”.
Source: page 24, lines 2472–2479. The next dated event is July 22, lines 2480–2483.
An effective date does not establish the execution day.

E7, instruction line 215, requires the execution date. E8, lines 221–233, preserves bounds for undated events.
Part B, line 26, prohibits greater precision than the source supplies.
The July 19–22 surrounding dates support bounds; they do not prove July 20 execution.

The error narrows an entrant's date to an unsupported exact day.
The effective-date qualification in B4 and the honest Note do not repair AB4/AC4.
A and B preserve the undated execution and surrounding bounds at their ledger row 4.

### P4 — A price-feedback quotation loses its negation

**Minor. B: Deal ledger X13. C: Deal ledger X12.**

Both quotations start with “believe that it reflected the full value of Penford’s business.”
The sentence starts on the preceding page and includes “but did not”.
Source: pages 26–27, lines 2548–2549 and 2558.
The source says the proposal did not reflect full value.

Part B, instruction line 30, requires a quotation that supports its row's claim.
The selected fragment omits the words that make the assessment negative.
Both Notes correctly retain the negative assessment. Therefore, this is a local evidence defect, not a wrong price-feedback observation.
The same cause applies to B and C. A does not share it.

### P5 — Questions entries exceed the word limit

**Minor. C: Questions B2:F2 and B6:F6.**

D4, instruction line 123, limits each Questions entry to 60 words.
C's Q1 contains 86 whitespace-separated words across its five substantive cells. Its R4 contains 64 by the same measure.
These counts exclude the ID and empty Reviewer note. Q1 exceeds 60 even without its Rows affected cell.

This is one length-control cause, not a separate finding for each cell or entry.
The discussion preserves the relevant uncertainty. The excess length does not change an economic observation.
A and B have no Questions entry above this limit by the same measure.

## Material coverage review

This review checked required observations, not only differences among candidates.
The table uses `L` for Deal ledger, `R` for Rounds, and `F` for Deal facts.
Ranges below name the inspected Excel rows; they are not ledger event numbers.

| Source item | A | B | C | Source and judgment |
| --- | --- | --- | --- | --- |
| Earlier approaches | F12 | F12 | F12 | Page 23, lines 2448–2449: 2007/2009 only. Correctly outside numbered processes under E5. |
| July interest and valuation | L2–3 | L2–3 | L2–3 | Page 24, lines 2463–2477. No invented $16 bid. Bidder-led initiation is supported. |
| First NDA and entry | L4 | L4 | L4 | Page 24, lines 2478–2483. One entry each; C's date precision is P3. |
| Target advisers | L5, L9 | L5, L9 | L5, L8 | Page 25, lines 2494–2516. Perkins Coie's July role and Deutsche Bank's August advice remain distinct from later engagement. |
| August prices | L6, L8 | L6, L8 | L6–7 | Page 25, lines 2509–2513. All retain $17 and $18 cash as separate Informal bids. |
| August price feedback | L7, L13 | L7, L13 | L6 Note, L12 | Pages 25–27, lines 2509–2510 and 2548–2561. Facts retained; B/C quotation defect is P4. |
| Target exploration decision | L10 | L10 | L9 | Pages 25–26, lines 2514–2533. Qualified exploration is preserved. |
| Party A approach | L11 | L11 | L10 | Page 26, lines 2534–2537. Interest and typical-premium valuation remain visible; no fabricated number. |
| SEACOR inquiry | L12 | L12 | L11 | Page 26, lines 2534–2538. Correctly outside entrants after its refusal. |
| Exclusivity requests | L14–15 | L14–15 | L13 and Note | Page 27, lines 2560–2566. Both refusals remain visible; no invented executed or required exclusivity. |
| Replacement NDA and access | L16 | L16 | L14 | Page 27, lines 2565–2570. Replacement does not create another acquirer or entry. |
| Round 1 opening | L17; R2 | L17; R2 | L15; R2 | Pages 27–28, lines 2571–2601. August 28 authorization and early-September outreach satisfy E6. |
| Six-party outreach | L18–21, L26 | L19–22, L28 | L16–19, L24 | Pages 28–29, lines 2598–2613 and 2635–2644; page 32, lines 2744–2747. No seventh party invented. |
| Non-entrants B/E/F | Contact Notes | Contact Notes | Contact Notes | Pages 28–30, lines 2606–2609 and 2653–2654. No unsupported NDA or exit. G receives no invented contact. |
| C, D, and A NDAs | L22, L24, L28 | L23, L25, L30 | L20, L22, L26 | Pages 28–30, lines 2610–2613, 2629–2630, and 2660–2663. September 15, 23, and 30 preserved. |
| September price range | L23 | L24 | L21 | Page 29, lines 2621–2625. $18.25–$18.50 remains one Informal range, not two alternatives. |
| September price feedback | L25 | L26 | L23 | Page 29, lines 2631–2634. Communicated dissatisfaction remains visible. |
| C's presentation | L27 | L29 | L25 | Page 29, lines 2645–2646. September 25 access difference receives a row. |
| A's information and gate | L28–29 | L30–31 | L26–27 | Page 30, lines 2660–2663. NDA, supplied information, and conditional management access remain visible. |
| October target price preference | L30–32 | L32–35 | L28–29 | Page 30, lines 2664–2672. $20 remains target feedback, not an acquisition bid or deadline. |
| October 2 oral bid | L31 | L34 | L29 | Page 30, lines 2670–2672. All retain $18.50 before the same-day improvement. Diligence ambiguity remains below. |
| October 2 written bid | L33 | L36 | L30 | Page 30, lines 2673–2675. All retain $19 as Informal at communication. |
| Definitive round and selection | L34, L37; R3 | L37, L40; R3 | L31–32; R3 | Pages 30–31, lines 2676–2692. Round 2 starts October 3; Inferred final is supported. |
| C/D exclusions | L35–36 | L38–39 | L33–34 | Page 31, lines 2690–2695; E14. All infer October 3 exclusion; C assigns the wrong round in P2. |
| A's ceiling and invitation | L38 | L41–42 | L35 | Page 31, lines 2694–2695. The invitation correctly preserves A. Ceiling endpoint choices remain separate below. |
| First document reaffirmation | L39 | L43 | L36 | Page 31, line 2702. All record the October 8 submission as Formal and copy $19. |
| Later unchanged drafts | No added bid | No added bid | No added bid | Pages 31–32, lines 2709–2711 and 2733–2734. Correctly no repeated document-only confirmations. |
| Weaker actual results | L40 | L45 | L37 | Pages 31–32, lines 2712–2723. October 11 delivery to Ingredion remains a material information event. |
| Valuation warning | L41 | L46 | L38 | Page 32, lines 2728–2730. No invented lower bid, right to reprice, or H3 condition. |
| A's later offers | L42, L44 | L47, L49 | L39, L41 | Page 32, lines 2731–2732 and 2738–2740. $16–$18 and then $16 remain separate Informal bids. |
| Final reaffirmation | L43 | L48 | L40 | Page 32, lines 2735–2736. All retain Formal $19. A/B financing omission is P1. |
| A's final closure | L45 | L50 | L43 | Pages 32–33, lines 2738–2765. All use Not selected at signing, not withdrawal. Reason ambiguity remains below. |
| Agreement and announcement | L46–47 | L51–52 | L42, L44 | Page 33, lines 2762–2765. All distinguish October 14 execution from October 15 announcement. |
| Bid deadlines | R2–3 | R2–3 | R2–3 | No bid due date appears in the background. All correctly use no deadline stated. |
| Round populations and bid units | R2–3 | R2–3 | R2–3 | All summaries show four then two entrants, and one then two distinct bidder units. C's ledger conflict is P2. |
| Final consideration | F5; L46 | F5; L51 | F5; L42 | Page 54, lines 4649–4651, and page B-1, lines 10916–10920, confirm $19 cash. |
| Other Deal facts | F2–18 | F2–18 | F2–18 | Core identities, dates, adviser roles, one process, bidder-led initiation, and four-party auction screen reconcile with the source. |

All candidates preserve five new Ingredion price communications and two required reaffirmations.
All preserve Party A's three October price communications.
All treat Prospect Sub as part of Ingredion and SEACOR's support as shareholder support, not a joint bidder.
None creates a process restart, partial bid, go-shop solicitation, or Activist row from unsupported evidence.

All candidates use cash only where their offer evidence supports it.
They do not turn the pre-selection September 6 draft into automatic Formality for the September or October 2 bids.
They retain the later antitrust concern without spreading it across every earlier offer.

## Ambiguous or defensible choices

These items carry no confirmed error count. The table distinguishes uncertainty from the clear rules in P1–P5.

| Issue and locations | Source, rule, and judgment |
| --- | --- |
| Party A on August 11: A L11; B L11; C L10 | Page 26, lines 2534–2537, reports acquisition interest and a typical-premium valuation basis. Whether it already constitutes an undisclosed-price proposal remains uncertain. Interest is defensible under E10. |
| October 4 ceiling: A L38; B L41; C L35; each Q1 | Page 31, lines 2694–2695, says an offer would be below a range. A/B use an outer upper bound of 18; C leaves both endpoints blank. E13 expressly defines a one-figure ceiling. Both treatments preserve the qualifier and raise the issue. |
| October 2 diligence: A L31/L33; B L34/L36; C L29/L30 | Page 30, lines 2667–2675, anticipates further information for a higher price. C codes the oral bid Incomplete; A/B use Not stated. The passage does not clearly state the bidder's remaining diligence requirement. |
| October 8 diligence: A L39; B L43; C L36 | Pages 31–32, lines 2712–2723, describe review of weaker actual results. A/C use Incomplete; B uses Not stated. Incomplete has stronger contextual support, but the scope of remaining diligence is not express. |
| Final diligence and copy reference: A L43; B L48; C L40 | A retains Incomplete; B retains Not stated. C refers to the latest offer that newly states $19, rather than its intervening document confirmation. E10's latest-stated-offer wording leaves a copy-reference question here. No candidate claims Complete. This is separate from newly reported finance evidence. |
| Party A's exit reason: A U45; B U50; C U43 | A uses Not stated; B/C use Lower offer than rivals. Pages 32–33 compare $16 and $19 but do not expressly isolate the individual rejection reason. The comparison supports B/C; A is conservative. |
| Projection rows outside the background: B L18/L44 | Page 43, lines 3664–3668, dates an August 28 plan update and October 10 delivery to Deutsche Bank. It does not date bidder receipt. E2 mentions projections revised after bids, but its information-access rule focuses on bidders. B disclaims bidder receipt. These extra rows receive no reward or confirmed penalty. |
| Feedback and repeated refusal combined with Notes: C L6/L13/L29 | Pages 25–27 and 30 preserve same-conversation feedback and the August 20–21 repeated refusal. C retains their substance in Notes. A/B use more separate rows. No material information loss establishes a separate confirmed error here. |
| October 2 clarification and October 4 invitation | A/C use Notes for some acts that B separates. All preserve the qualification of $20 and the invitation that keeps Party A live. More rows do not establish better coverage. |
| Round opening and selection rows | All candidates preserve the October 3 admission and selection, with a round marker and substantive selection row. No duplicate admission row is required beyond the information already recorded. |
| Finality | All use Inferred final. Pages 30–31 report definitive negotiation, without an express final-stage label. E6(c) supports this choice; no finality disagreement affects the rank. |
| Shareholder support | All retain SEACOR support in the execution Note. Earlier drafts discuss it without an express refusal condition. The final recital's separate communication time is unclear. No additional H3 bid is established. |

The source inventory contains one date imprecision: its conditions table places ongoing diligence on October 3.
The explicit earlier diligence update is on September 29; the October 3 paragraph describes the market check.
This review uses the filing and imposes no penalty from that inventory statement.

## Final per-deal rank

**A > B > C.** The distinction between A and B is narrow.

A and B preserve the same main economic record and share the final financing omission.
A ranks first because B adds the defective price-feedback quotation. That minor defect does not establish a broad accuracy gap.

C supplies the final financing basis that A and B omit.
However, its two exit-round cells misplace losses across stages, and its NDA bounds assert an unsupported execution day.
Those defects affect participation and chronology. They outweigh C's better final financing field under Part A's research priorities.
C also shares B's quotation defect and exceeds the Questions limit.

The rank does not depend on extra row counts, the disputed ceiling endpoints, or the diligence choices.
No candidate loses points for preserved information merely because another candidate gives it a separate row.

## Limits

The masked dumps establish cell values across the four sheets. They do not establish workbook formatting, filters, frozen headers, or file integrity.
This report makes no claim about checker results, runtime, token use, service tier, or cost.
It evaluates one supplied Penford output per neutral label. It does not establish accuracy across other deals or repeated runs.
