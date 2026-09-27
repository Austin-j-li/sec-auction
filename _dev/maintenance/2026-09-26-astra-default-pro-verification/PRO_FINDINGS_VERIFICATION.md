# Verification of Pro's extraction review — 26 September 2026

## Conclusion and scope

Pro's main diagnosis is supported: the material weaknesses concern participation and exit timing, evidence available at the date of a bid, and important commitment changes that disappear from structured condition fields. Most are failures to follow the tested instruction, not reasons to expand its taxonomy. There are also several judgments in Pro's preferred readings that should remain qualified.

This is a source check of consequential findings, not a second scoring exercise. Pro's scores are unchanged. The review read the relevant sale narratives in all three supplied filings, inspected the relevant cells across the 15 workbooks and their Questions/Rounds sheets, and compared them with the tested instruction and relevant direct Alex voice passages. It is not a certification of every cell, all 1,024 quotations, or all concerns across Alex's other deals. No workbook has been corrected.

The original report and inputs are in the [Pro packet](/home/uctpiaj/work/Projects/sec-extraction/_dev/reviews/2026-09-26-v114-15-run-trial/pro-review/). The absolute packet path is `/home/uctpiaj/work/Projects/sec-extraction/_dev/reviews/2026-09-26-v114-15-run-trial/pro-review`.

The instruction actually tested is `c2d47a479d09eb46d0ab9fbf887568fcf13e972e2e11acbf08d5cdfab468ab27`. The report PDF is `e954ada430d29ac31d7b37ff0cbc289a9ab1e55791d40d2b1398c7fd92d12dbb`. Letter identities are deal-specific. In the tables, `A #33` means event number 33 in anonymous workbook A's **Deal ledger**, not Excel row 33. Filing page numbers are the printed page labels.

Local reading evidence:

- [Mac-Gray filing text](evidence/mac-gray_2013-12-04_DEFM14A.txt); original HTML is in the Pro packet's `package/filings/`.
- [Providence & Worcester filing text](evidence/providence-worcester_2016-09-20_DEFM14A.txt).
- [sTec filing text](evidence/stec_2013-08-08_DEFM14A.txt).
- [Read-only workbook cell dump](evidence/workbook-cells.json), indexed by deal/letter and sheet.
- [Numbered voice-note paragraphs](evidence/alex-voice-paragraphs.txt). Paragraph 129 onward is labelled Claude's reading and is not treated as Alex's own speech.

## Mac-Gray

| ID | Finding and evidence | Verification and consequence |
|---|---|---|
| MG1 | Pro pp. 3–4: B #24 and E #23 close the anonymous NDA residual as non-submitters by July 23. Filing pp. 31–34 reports the 20 NDAs over two months and dates Party A's NDA August 5; text lines 1518–1535, 1595–1634. | **Confirmed error.** A lifetime NDA total is not the population eligible at an earlier deadline. B's blank Count and explanatory Question do not repair the row's unsupported exit label/date. E3/E14 already prohibit this reading. |
| MG2 | D #42 waits until September 11 for residual closure. The August 27 letter names all four continuing bidders, after the two-month NDA interval; p. 35, lines 1635–1642. A #33 uses a bounded closure by August 27. | **Confirmed late bound.** August 27 is the earlier supported transition under E14. It bounds disappearance; it does not prove 16 observed rejection decisions on that day. |
| MG3 | B #41 and E #39 make Party B's September 18 package Financing Contingent / Heavy H1. The new package is on p. 36; the committee's subsequent comparison says financing would likely use affiliated equity and third-party debt and involve greater risk, p. 37; lines 1685–1698, 1715–1726. | **Confirmed overstatement.** A likely source and comparative risk do not establish uncommitted financing for this bid. September 9's absence of a firm commitment is not automatically carried forward. A #45's Not stated / Unclear is better supported by the existing E10/E12 rule. The approved spec already settles this example. |
| MG4 | E #37 labels CSC's September 18 bid Light using confirmatory diligence described for September 25–October 7; p. 38, lines 1754–1767. | **Confirmed backdating.** Later confirmatory work does not establish that only confirmatory work remained on September 18. |
| MG5 | B #55/#57 put $21.25 and Committed financing into the October 5/8 sponsor-liability revisions. The relevant communications discuss an unspecified damages cap and then a $50m cap, p. 39, lines 1779–1805. | **Confirmed unsupported carry.** Preserve the commitment events, but the communications do not themselves restate or incorporate those price/funding values. Eventual signing at the old price does not establish a newly quoted price on these dates. A #61/#62 appropriately leave price blank. |
| MG6 | Pro prefers A #44's financing carry for Party A's September 18 reiteration over C #45/D #46. Source: earlier indication lacked a firm financing commitment, p. 35; September 18 calls its previous $18–19 indication best and final, p. 36; lines 1650–1658, 1685–1698. | **Qualified; not a settled correction.** Reiterating an offer can incorporate its terms. An earlier absence of commitment documents is also a dated status fact, which E10 says must be judged at the new date. The filing does not clearly say that this status remained unchanged. Pro's preferred Heavy reading should not be imported automatically. Retain the earlier fact in the Note; distinguish it from a continuing express financing condition. |
| MG7 | Pro pp. 3–4 favors more consistent Formal coding for the late sponsor-document negotiations. A #61 is Formal; #62, an oral cap proposal, is Informal. | **Convention-dependent.** E11 supplies communication-specific routes; a late negotiation is not automatically Formal. Preserve the documentary support and flag a consequential ambiguity. A general rule making all late commitment changes Formal would change the convention, not merely fix a source error. |
| MG8 | Pro notes C's thinner information history. The filing separately describes customer-information restrictions for strategic bidders and synergy discussions, pp. 34–35, lines 1595–1634. No synergy disclosure appears in C's Note/When fields. | **Confirmed omission.** The information supplied to competing bidders matters for the research; existing E2 supports a material information event. This needs a source-to-ledger check, not a new condition category. |

The $21.50 Party B package is $19 cash plus performance options the bidder valued at $2.50, not $21.50 upfront cash. A #45 preserves this distinction. A deferred performance security belongs in CVR/earnout under the tested definition. That feature alone does not make the bid Heavy.

## Providence & Worcester

| ID | Finding and evidence | Verification and consequence |
|---|---|---|
| PW1 | Pro pp. 5–7 praises B #18's conditional 16–24 residual. Initial narrative: 11 strategic plus 14 financial NDA signers; subsequent approaches and nine IOIs, pp. 28–29, lines 1307–1329; late Party C, lines 1336–1342; later global total, p. 33, lines 1460–1464. | **Main uncertainty confirmed; exact range qualified.** B exposes its overlap assumptions rather than pretending 25 minus 9 is uniquely identified. Its 16–24 bound still depends on the claimed initial-cohort membership of at least one IOI bidder and on the population definition. It is not an independently established headcount. A complete membership map cannot be recovered from the totals alone. |
| PW2 | A #17 and E #18 use residual non-submission closures despite uncertainty about population membership and deadline eligibility; same source passages. | **Confirmed overstatement.** A subtraction can bound an unaccounted-for population without proving every residual participant declined an invitation or missed that deadline. E14 already distinguishes these claims. |
| PW3 | D #9 records 11 strategic NDA signers while #11 and #16 separately record G&W and Party B, acknowledging possible inclusion in the 11. | **Confirmed unresolved overlap.** These must not be treated as disjoint entries. This is a risk to live-count reconstruction, not proof that 27 distinct bidders existed; simply summing every Count would itself violate E3/E14. |
| PW4 | D #30/#49 makes Party E Heavy H2 because it sought 60 days' exclusivity for diligence and definitive documentation; p. 30, lines 1344–1363. | **Confirmed error under explicit E12.** A combined exclusivity/negotiation interval does not establish 60 days of remaining diligence. Required exclusivity may be supported without Heavy being supported. Contrast G&W's expressly requested three weeks of due diligence, which can meet H2. |
| PW5 | E #24 puts Party C's July 12 diligence at Not begun because data-room access came later. Before bidding it had signed an NDA and received the confidential memorandum; p. 29, lines 1336–1342. | **Confirmed unsupported negative.** No data room yet is not affirmative proof of no diligence access. Use the evidence of access and remaining work; do not automatically infer either Not begun or Complete. |
| PW6 | E #56 attaches the board's later August 12 regulatory comparison to G&W's morning bid. Morning offer/10:30 meeting: p. 31, lines 1398–1406; afternoon assessment: p. 32, lines 1416–1427. | **Confirmed temporal overreach for bid-time knowledge.** The regulatory assessment exists, but the filing does not establish it was available with the morning offer. B #58 preserves it as a later event. Similar expected paths also do not mean there was no regulatory risk. |
| PW7 | A #54 says the competing $25 price was conveyed to Party B. The committee directed the banker to report a higher price; p. 31, lines 1398–1406. | **Confirmed unsupported information claim.** The fact that the reader knows the rival price does not show Party B was told the number. Correct the information account without changing the observed $25 offer. |
| PW8 | A #33 says G&W's revision revises #25; its earlier bid is #26. A #47 refers back to #39 for Party D; #39 is Party E and the relevant D row is #43. | **Confirmed reference errors.** These are within-workbook checks; no new extraction convention is needed. |
| PW9 | The filing says differing transaction-expense and change-in-control assumptions affect offer comparability, p. 30, lines 1344–1363. A lacks that caveat in its Notes. | **Confirmed omission.** Preserve the comparison basis without inventing adjusted prices. Existing E2/E13 already support it. |
| PW10 | Pro questions exact August 2 placement of Party D's withdrawal. The paragraph begins with Party E's August 2 communication and then describes D's refusal to shorten its diligence period, p. 30, lines 1364–1380. | **Qualified date criticism.** A same-day reading is plausible from the paragraph, while a wider bound is more conservative. The filing's sequencing is not enough to declare every August 2 placement definitely wrong. State the inference if material. |

Party B's August 4 revised markup supports a Formal reaffirmation under the tested rule, as in B #52. The same narrative says financial, legal and environmental diligence continued July 27–August 11 (p. 31, lines 1383–1395). It does not establish an unconditional offer.

## sTec

| ID | Finding and evidence | Verification and consequence |
|---|---|---|
| ST1 | A #63, D #64 and E #67 leave the late standstill-waiver restriction in Other material event rows with condition cells blank. B #82 and C #70 code a Bid with Heavy H3. Filing pp. 33–34, lines 1470–1492: WDC may not proceed if sTec unilaterally waives the provisions. | **Confirmed substantive difference.** This changes willingness to proceed and qualifies under existing E10 and H3. Preserve a commitment-revision Bid even without a newly stated price. No additional condition category is needed. |
| ST2 | D #51 opens a third round on May 31 after WDC withdraws. The filing shows Party D still seeking more time and then being told of the delay and allowed to continue; pp. 31–32, lines 1400–1434. | **Two rounds better supported by existing E6.** Continuing an existing bidder's work after a rival withdraws does not itself establish a new solicitation stage. A third-round interpretation can remain an explicit alternative map rather than the default reconstruction. |
| ST3 | E #15/#17 excludes E/F's NDA entries as partial-only based on their later asset proposals; #24/#26 do not record the switch out of the whole-company contest. Earlier NDA history and later scope change: pp. 27–28, lines 1311–1323 and subsequent April 24 narrative. | **Confirmed convention violation, not proof of initial intent.** E1/E3 prevent later partial proposals from rewriting earlier participation absent earlier scope evidence. Do not claim the filing affirmatively proves each party originally intended a whole-company purchase. |
| ST4 | C #16 assigns Company G to the original nine uninterested parties. Source names Company A and the financial sponsor within that group, p. 27, lines 1304–1307; G's later withdrawal is separately described. | **Confirmed unsupported membership.** G's withdrawal does not identify it as one of the original nine. The actual overlap remains unresolved. |
| ST5 | E #22 leaves Party D's April 23 diligence Not stated. The source describes the management presentation and requests for further information, p. 28, lines 1327–1333. | **Confirmed missing supported state.** Access plus remaining work supports Incomplete here; no H2 period or substantive-work claim follows automatically. |
| ST6 | Pro objects to an exact June 20 date for the standstill communication. June 20 dates the revised draft; the following discussion is within negotiations continuing through June 23, pp. 33–34. | **Qualified date criticism.** June 20 is a plausible contextual reading; June 20–23 is a conservative bound. The condition itself is clear. Do not turn a preferred bound into a confidently proven correction of the exact date. |
| ST7 | B #72/#74 preserve Formality on WDC's June 10/14 lower offers through express references to the May 28 transaction terms while leaving diligence Not stated. Filing p. 32, lines 1430–1452. | **Supported treatment.** Expressly incorporated document terms and current diligence status are different kinds of evidence. A blanket instruction to copy all earlier fields would undo this useful distinction. |
| ST8 | The June 19 cost-reduction projections were supplied after price agreement; p. 46, lines 1990–1993. B #80 and C #68 record the information event. | **Supported material event.** Preserve what information was supplied and when, distinct from earlier forecasts. This can affect the research without changing the bid price or condition level. |

## Alex's voice notes: what the source check does and does not settle

| Voice passage | Disposition |
|---|---|
| Paragraphs 13, 41 and 45: constructed participation histories and subtraction of named parties from aggregate NDA counts. | Retain this objective. Prevent overlap, and retain bounds where identities or eligibility are uncertain. Exact arithmetic cannot make uncertain group membership exact. |
| Paragraphs 15, 17–19 and 44: announcement versus deadline dates, stages, document engagement, and conditionality. | Already represented by the candidate's separate event dates, rounds/finality, Formality and Conditions. The trial does not justify merging those dimensions. |
| Paragraph 30: PW Party B August 4 should be formal and unconditional at $24. | Formal reaffirmation is supported. Unconditional is not established by the filing, which reports ongoing diligence. Preserve the disagreement rather than silently treating the voice interpretation as source evidence. |
| Paragraphs 46–47: financing facts should be visible on the bid row and can matter for later analytical classification. | Supported objective. The recorded financing state and the research interpretation must remain distinct; current spec D5 and the analysis switches already expose that choice. |
| Paragraph 117: market-price history is needed to interpret changing bids. | Still an external research-data task, not a reason to fetch prices during blind extraction. This amendment does not implement the market-data backlog. |
| Paragraph 118: treat sTec's November–February gap as two processes. | The filing dates the initial November approach but not the cancellation precisely (pp. 24–25, lines 1222–1245). The candidate's three E5 tests cannot be conclusively met from an exact three-month inactivity interval. Keep a map question; do not invent a cessation date. |
| Paragraphs 122–125: sTec soft deadline, second round, and May 28 formal/no-condition bid. | The stages and document engagement are supported. A markup does not itself prove no remaining conditions or completed diligence. Do not turn “formal” into “unconditional.” |

These checks do not close Alex's remaining research choices: the primary formal-bid reading, treatment of unknown conditions, count bounds, inferred exits, repeated same-price commitments and price-comparison basis. Most already appear in the approved spec's replacement Questions; they need reconciliation, not a duplicate questionnaire.

## Reproduced analysis-tool gap

The upgrade already implements D22's analysis switches. Pro was right about the danger of counting commitment events as new price observations, but adding a new extraction event type is unnecessary.

An offline invocation of the upgrade's `derive_analysis.py` on Mac-Gray A produced [bids.csv](analysis-diagnostics/mac-gray/bids.csv). For both #61 and #62:

| Field | Observed output |
|---|---|
| `price_low`, `price_high` | both blank |
| `same_price_revision` | blank |
| `price_obs__same_price_as_new` | 1 |
| `price_obs__same_price_as_terms` | 1 |

The implementation only detects repeated prices when at least one price is present; the two observation flags nevertheless default to 1. This matches the present analysis contract, so it is an underspecified output contract rather than evidence of a coding departure from that contract. A consumer using the flags alone can count an event with no usable upfront price. The proposed amendment adds an explicit mechanical price-availability classification and makes these flags depend on it. The events and all source fields remain in the output; no price is filled in.

## What to adopt

Adopt the main temporal-evidence, overlap and structured-condition findings. Qualify Pro's exact-date objections, its preferred Party A financing carry, its preferred late-negotiation formality and the apparently precise PW residual bound. Keep the trial's model ranking as a small descriptive pilot, not an independent proof of all preferred workbook cells.

The [amendment proposal](AMENDMENT_SPEC.md) separates small instruction clarifications, a concrete analysis-tool amendment and corrections already warranted by existing rules. It proposes no new extraction or correction run.
