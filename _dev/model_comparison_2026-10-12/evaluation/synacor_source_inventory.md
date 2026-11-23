# Synacor: independent source inventory

Recorded on 12 October 2026, before access to any comparison workbook.

This is a source inventory, not a reference workbook. It separates required observations from choices that need review.
No model output, reference workbook, history, identity map, or other development document informed this inventory.

## Sources and method

- Instruction: `SEC_Deal_Ledger_Extraction_Instruction.md`, Version 1, with the amendments through 12 October 2026.
- Filing: `raw_filing/synacor_2021-03-03_SCTO-T.htm`.
- Protocol: `_dev/model_comparison_2026-10-12/evaluation/PROTOCOL.md`.
- Instruction SHA-256: `e6e1e2f3b53378bdb6770762d33fe9b84090c2ae27301d5bf725e0c3f629eb13`.
- Filing SHA-256: `2ea05ceef8c7315f7bf81743a70f67a2574e545cb303e48152efd6803b749b0e`.

The task named a 16 March DEFM14A file. That basename does not exist. The permitted filename check found the 3 March Schedule TO exhibit.
The exhibit itself states 3 March 2021 on its cover, at source line 64.

I read the complete background, in order, at source lines 1923–2221. Its printed pages are 30–38.
I then read the cover, party descriptions, financing description, and merger consideration summary.
The final price agrees across the cover, background opinion account, and merger consideration summary.
I used the HTML text as a reader. I ran no model, test, or assertion.

Locations below use original HTML line numbers. Page numbers are printed filing pages, not browser pages.
Quoted fragments preserve source words after HTML entity decoding and ordinary whitespace normalization.

## Main research observations

1. The source supports three separate whole-company sale efforts: 2018, 2019, and July 2020–February 2021.
2. Company B's merger-of-equals talks do not join the whole-company contest. Synacor's proposed purchase of Company D also stays outside it.
3. The 2020 outreach covers both whole-company and segment transactions. Its 14 confidentiality agreements do not establish 14 known whole-company bidders.
4. Company E, CLP, and Company H require separate participation tracks. Company G and Company I make partial proposals.
5. Company E leaves the whole-company contest on 14 December 2020, when it changes to a 35% tender proposal.
6. The reported bid deadline is 17 September 2020. Exclusivity dates, offer expiry dates, and the public tender expiry are different events.
7. Renewed outreach on 27 October and 18–21 December requires an E6(d) review. CLP's selection on 6 January requires E6(c).
8. The January document submission and February changes to commitments require review under the amended E10 rule.

## Governing instruction locations

| Rule | Instruction location | Consequence here |
| --- | --- | --- |
| B | Lines 24–30 | Preserve source precision. Apply each bid's evidence window. Do not copy conditions across revisions. |
| D2 | Lines 83–102 | Separate advisers, contacts, price feedback, exclusivity, bids, exits, and the merger announcement. |
| D3 | Lines 106–119 | Count distinct bidder units in each round. Exclude contacts that never enter. |
| D5 | Lines 129–135 | Initiation comes from process 1. Record an auction screen for each process. |
| E1 | Lines 141–149 | Exclude partial parties and merger-of-equals counterparties from the whole-company population. |
| E2 | Lines 151–155 | Record material requirements and bidder responses. Exclude routine meetings and legal drafts. |
| E3 | Lines 157–171 | A contact is not entry. Reconcile named participants within reported entrant totals. |
| E4 | Lines 173–175 | A shareholder rollover does not create a joint bidder. |
| E5 | Lines 177–183 | Test all three process conditions. Measure the gap from the last reported sale contact. |
| E6 | Lines 185–211 | Use target acts to map rounds. Review both renewed approaches after the first exclusivity period. |
| E7–E9 | Lines 213–247 | Keep contacts, executed agreements, date bounds, and bid deadlines separate. |
| E10–E11 | Lines 249–281 | Record price revisions, conditions on proceeding, and the first qualifying document confirmation. |
| E12–E13 | Lines 283–317 | Do not infer cash, committed financing, complete diligence, or a synthetic price range. |
| E14 | Lines 319–342 | Close each participation once. Apply the continued-invitation exception before an inferred exit. |
| F | Lines 383–397 | Include the mandatory process Question and the specified Review items. |

## Participant and scope register

| Party | Source identity | Scope and count treatment | Evidence |
| --- | --- | --- | --- |
| Company A | Private investment firm; Financial | Whole-company bidder in 2018. One unit. | p. 30, lines 1929–1935 |
| Company B | Public software company; Strategic | Merger of equals. Exclude from whole-company counts and auction screen. | p. 30, lines 1936–1938 |
| Company C | Public software company; Strategic | Whole-company bidder in 2019. Cash and stock proposal. | pp. 30–31, lines 1939–1954 |
| Company D | Public software company; Strategic | Synacor first proposes to acquire D. The later merger does not establish a sale of Synacor to D. | p. 31, lines 1956–1957, 1967–1978 |
| Company E | Investment subsidiary of a public financial-services company; Financial | Partial interest in 2019. Whole-company bidder from July 2020. Partial bidder from 14 December 2020. | pp. 31–32, lines 1958–1961, 1991–2005; pp. 34–35, lines 2081–2096 |
| Company F | Information and technology services company; Strategic | Portal and advertising business only. No whole-company entry or exit. | p. 31, lines 1960–1966 |
| Company G | Financial acquirer that invests in enterprise software; Financial | Software and services business only. No whole-company entry or exit. | pp. 32–33, lines 2013–2027 |
| Company H | Public software acquirer; Strategic | Whole-company interest. Its NDA, admission, exit, and re-entry dates need careful reconciliation. | p. 33, lines 2031–2035; pp. 34–36, lines 2061–2072, 2107–2151 |
| Company I | Public media company; Strategic | Portal and advertising business only. No whole-company entry or exit. | p. 34, lines 2073–2079; p. 35, lines 2112–2114 |
| CLP | Centre Lane Partners, LLC; Financial | Whole-company bidder and winner. Combine its funds and acquisition shells into one unit. | p. 32, line 2003; p. 28, lines 1851–1863 |
| 180 Degree | Affiliate of director Kevin Rendino | Proposed rollover holder with Company E. No independent bid or joint bidder unit. | pp. 32–33, lines 2004–2005, 2029, 2040–2041 |

CLP's party description states: “primarily engaged in the business of managing private investment funds” (p. 28, lines 1855–1857).
The acquisition shells do not add bidders. A consistent CLP or fully expanded CLP name is appropriate throughout the ledger.

## Process and round map

### Process 1: Company A and the 2018 outreach

Company A approaches before its 10 January 2018 NDA. It bids on 6 February and 25 April.
Liontree then contacts approximately 12 additional parties after its 8 May appointment.
Company A declines the proposed value on 20 June. The other outreach produces no indication of interest.

The preferred round map puts the A proposals in round 0 and opens round 1 on 8 May.
E6 dates undated outreach at the last dated sale step. Its bilateral fallback applies where the target never contacts other buyers.
An earlier January round opening needs a stated interpretation of that fallback. It cannot erase the later outreach.

The first source event establishes bidder-led initiation. Routine strategic reviews in the opening paragraph do not establish a prior target sale decision.
The screen is Not met on the reported NDA evidence: one whole-company NDA party, Company A.
The approximately 12 contacts do not establish 12 admissions or 12 signed NDAs.

### Process 2: Company C and the 2019 outreach

The next whole-company effort starts with Company C's March 2019 NDA.
The gap from the last dated A contact, 20 June 2018, exceeds 90 days.
Company B's intervening merger-of-equals talks do not interrupt that gap under E1 and E5.
Use an inferred Process restarted marker if no earlier explicit whole-process termination is supported.

Company C bids on 13 August 2019. Canaccord's 25 August mandate produces outreach to 18 additional parties.
The preferred map puts the C bid in round 0 and opens round 1 on 25 August.
Company C and Synacor agree in October not to pursue the transaction. The 18 contacts produce no offer.

The screen is Not met on the reported NDA evidence: one whole-company NDA party, Company C.
The Company B, E, and F agreements do not increase that whole-company count.

### Process 3: July 2020 through the CLP agreement

The next fresh whole-company step is 13 July 2020, when Synacor takes up Company E's acquisition interest.
The gap from Company C's October 2019 end exceeds 90 days.
The Company D transaction is a proposed acquisition by Synacor and does not keep Synacor's sale process open.

| Stage candidate | Preferred treatment | Source and uncertainty |
| --- | --- | --- |
| July 2020 outreach | Round 1. Broad outreach on both whole and partial scope. | p. 32, lines 1991–2001. The board direction follows the 13 July events; outreach spans mid-July to mid-September. Preserve the source precision. |
| 13 September committee formation | Continue round 1. | p. 32, lines 2007–2011. Authority to negotiate with E is not an express decision for definitive negotiation. |
| 17 September request for E's best price | Continue round 1. | p. 33, lines 2036–2037. This is a request to one bidder, with no express final stage. |
| 23 September E exclusivity and definitive work | Round 2, Inferred final, under E6(c). | p. 34, lines 2064–2066. The target executes the LOI and ends competing discussions. |
| 27 October renewed outreach after exclusivity ends | Round 3, under E6(d). | p. 34, lines 2067–2071. Fresh approaches follow the 23 October expiry. Continued E talks alone would not suffice. |
| 18–21 December renewed approach to CLP and H | Round 4 is the preferred E6(d) treatment. | p. 35, lines 2107–2109. More than 30 days separate this request from the 27 October outreach. Review whether it merely carries out that earlier stage. |
| 30 December decision to continue CLP, H, and I talks | Continue the current round. | pp. 35–36, lines 2116–2136. The source says “continue”; E already left whole-company scope. No new stage is express. |
| 4 January requests for improvements and H's offer | Continue the current round. | p. 36, lines 2137–2144. The source does not establish a new common final stage. |
| 6 January selection of CLP for definitive work | Next round, Inferred final, under E6(c). | p. 36, lines 2148–2151. The $2.00 offer is reported before the committee's selection. |
| 7 January executed CLP LOI | Exclusivity execution within the round opened by the 6 January decision. | p. 36, lines 2153–2154. Do not create another round for the same implemented decision. |
| 8–10 February price negotiations | Continue the CLP definitive round. | pp. 37–38, lines 2182–2220. No further common solicitation or new admission occurs. |

This preferred map has five rounds in process 3. The December boundary remains a material interpretation for comparison.
The map must include a process Question. E6(d) and any inferred opening also trigger that requirement.

For July, 13 July is a plausible opening date if the adjacent target direction takes that date.
An interval treatment also needs review under E6 and E8. Do not replace “middle” with an invented exact outreach date.
Do not let a broad interval's Sort date silently move the actual September bid dates.

## Chronological event inventory

The IDs below identify source observations. They do not prescribe workbook row numbers.
One observation can require separate marker and substantive rows. Some rows are conditional on a scope or participation decision.

### 2018 and 2019

| ID | Date or bound | Required observation or review | Source anchor |
| --- | --- | --- | --- |
| S01 | Before or by 10 January 2018 | Company A first expresses acquisition interest. Preserve the unknown earlier day. Separate the NDA execution. | p. 30, lines 1929–1931: “after expressing interest in exploring a potential acquisition of the Company” |
| S02 | 10 January 2018 | A signs a mutual NDA with a target standstill. Whole-company entry. | p. 30, lines 1929–1931 |
| S03 | 6 February 2018 | A submits a non-binding acquisition indication. Price and consideration are undisclosed. | p. 30, lines 1931–1932 |
| S04 | 25 April 2018 | A submits an updated acquisition indication. Keep a separate Bid despite the absent price. | p. 30, lines 1931–1932 |
| S05 | 8 May 2018 | Liontree first acts as target financial adviser. Note the stated 31 December engagement end. | p. 30, lines 1932–1934 |
| S06 | After the 8 May engagement | Approximately 12 additional strategic and financial contacts. Round 1 opening requires E6's date rule. Count stays blank for the qualified total. | p. 30, lines 1933–1935 |
| S07 | 20 June 2018 | A declines the earlier proposed value. Record its participation end. No offer results from the additional outreach. | p. 30, lines 1934–1935: “unable to support the transaction at the proposed value” |
| S08 | October 2018 | B and Synacor agree to explore a business combination. Treat the NDA and talks within the merger-of-equals scope. | p. 30, lines 1936–1938 |
| S09 | Later in October 2018 | Synacor proposes a merger of equals to B. Other material event; not a whole-company Bid. | p. 30, lines 1937–1938 |
| S10 | December 2018 | The parties execute that indication. Preserve the agreement as a merger-of-equals act. | p. 30, line 1938 |
| S11 | March 2019 | B and Synacor end the merger-of-equals talks. This is not a whole-company bidder exit or a new sale process. | p. 30, line 1938 |
| S12 | March 2019 | C signs a mutual NDA for a potential business combination. Whole-company scope follows from its later acquisition proposal. Process 2 starts. | p. 30, lines 1939–1941 |
| S13 | 1 July 2019 | Synacor proposes to acquire D. Exclude this target-as-buyer transaction from the sale ledger. | p. 31, lines 1956–1957 |
| S14 | Third quarter 2019; 30 July | Segment divestiture outreach to approximately five parties; E executes its partial-scope NDA. F uses an existing commercial NDA. Preserve context with the partial proposals. | p. 31, lines 1958–1961 |
| S15 | 13 August 2019 | C offers to acquire Synacor for cash and stock. Bid; price unknown; Stock % Part stock. | p. 30, lines 1940–1941 |
| S16 | 25 August 2019 | Canaccord first acts on C's proposal and other target alternatives. Separate Adviser, outreach, and the round marker as required. | p. 31, lines 1962–1965 |
| S17 | After the 25 August mandate | Canaccord contacts 18 additional parties. None submits an indication. Do not invent their NDAs or admissions. | p. 31, lines 1963–1965 |
| S18 | 15 September 2019 | F submits an indication for the portal and advertising business. Other-scope bid; amount undisclosed. | p. 31, lines 1960–1961, 1966 |
| S19 | October 2019 | C and Synacor mutually stop the transaction. Close C once. Review whether the wording also supports a whole-process termination marker. | p. 31, lines 1953–1954 |
| S20 | 1 January–29 June 2020 | D transaction: LOI, definitive agreement, and termination. Preserve as excluded context; it does not establish Synacor as the acquisition target. | p. 31, lines 1967–1978 |

For S07, Value below earlier offer fits the stated inability to support A's earlier value. The row must preserve the actual comparison.
For S19, the filing gives no price reason. Do not invent a market-value comparison or a rival's higher price.
A stated adviser contract expiry does not alone prove an actual adviser termination. Review such a row before a source-error finding.

### July–September 2020

| ID | Date or bound | Required observation or review | Source anchor |
| --- | --- | --- | --- |
| S21 | 13 July 2020 | Rendino relays E's potential whole-company interest. Synacor directs Canaccord to pursue it. Process 3 starts. | p. 32, lines 1991–1993 |
| S22 | 13 July 2020 | E and Synacor amend their NDA. The standstill extends through 30 July 2021. This supports E's current-process confidentiality entry. | p. 32, lines 1994–1995 |
| S23 | Mid-July to mid-September | Canaccord contacts 37 parties, other than A–D, about the company or its software and services business. | p. 32, lines 1996–1997 |
| S24 | During that outreach | Fourteen contacted parties execute NDAs and receive confidential information. Reconcile named parties within this total. Separate partial scope. | p. 32, lines 1997–1998 |
| S25 | During that outreach | Parties still involved receive a 17 September due date for non-binding indications. Record Deadline set or include it in the opening marker. | p. 32, lines 1998–1999 |
| S26 | Same period | Management contacts eight parties about the portal and advertising business. These are partial contacts, not eight whole-company entrants. | p. 32, lines 1999–2001 |
| S27 | 8 September 2020 | CLP signs the confidentiality agreement with a standstill. This is a named NDA within the outreach reconciliation. | p. 32, line 2003 |
| S28 | 10 September 2020 | E offers $2.00 per share, all cash, for all equity and awards. The 180 Degree rollover does not change whole-company scope. | p. 32, lines 2004–2005 |
| S29 | 13 September 2020 | Gunderson first appears as target counsel on the sale. The board authorizes a special committee to negotiate with E. | p. 32, lines 2007–2011 |
| S30 | 14 September 2020 | G offers for software and services only. Cash consideration; equity and third-party debt finance the proposal. Other-scope bid. | pp. 32–33, lines 2013–2027 |
| S31 | 14 September 2020 | 180 Degree confirms rollover support, subject to diligence. Put this support in the related E note; do not add a bidder. | p. 33, line 2029 |
| S32 | By 16 September 2020 | H expresses more serious whole-company interest but cannot yet provide an LOI. Preserve first contact and participation uncertainty. | p. 33, lines 2031–2035 |
| S33 | 17 September 2020 | Synacor requests E's best purchase price through a revised LOI and an adviser call. Other material event for price feedback. | p. 33, lines 2036–2037 |
| S34 | 17 September 2020 | CLP offers $1.35–$1.41 per share, cash, for all equity and awards. It uses committed private-equity capital. | p. 33, lines 2038–2039 |
| S35 | 17 September 2020 | The bid deadline arrives. Infer non-submission for the remaining eligible unnamed whole-company NDA members under E14. | p. 32, lines 1998–1999 |
| S36 | 18 September 2020 | E reaffirms $2.00 and requests exclusivity until 23 October. The rollover term remains. Bid, with same-offer treatment. | p. 33, lines 2040–2041 |
| S37 | 21–22 September 2020 | The committee directs requests for higher G and CLP prices. Canaccord speaks to them on 22 September. | p. 33, lines 2043–2048 |
| S38 | 22 September 2020 | G says it cannot increase its partial purchase price. Review as a ceiling or reaffirmation of its partial proposal under E10. | p. 33, lines 2046–2048 |
| S39 | 22 September 2020 | CLP says it would consider a 10%–25% increase, subject to further diligence. This is a communicated conditional Bid. | p. 33, lines 2046–2048 |
| S40 | 22 September 2020 | Bhise encourages H to submit a whole-company proposal. This prevents an unsupported deadline exit if H is a live entrant. | pp. 33–34, lines 2048–2062 |
| S41 | 23 September 2020 | E and Synacor execute the LOI and start definitive work. Record exclusivity execution and the next round. | p. 34, lines 2064–2066 |
| S42 | 23 September 2020 | The target and Canaccord terminate other active transaction discussions because of exclusivity. Close CLP and any other live whole-company rivals once. | p. 34, lines 2064–2065 |

The 16 September committee meeting alone does not establish an admission or a new round.
The 21 September meeting alone also opens no stage. Its actual price requests matter under E2.
The source does not report a bidder-specific difference in the general confidential access given after the 14 NDAs.

### October–December 2020

| ID | Date or bound | Required observation or review | Source anchor |
| --- | --- | --- | --- |
| S43 | 23 October 2020 | E's exclusivity expires. Record Exclusivity changed. | p. 34, line 2067 |
| S44 | 27 October 2020 | The committee asks Canaccord to renew prior outreach. Bhise approaches H again. Review re-entry and open the E6(d) round. | p. 34, lines 2068–2071 |
| S45 | 27 October 2020 | H requests updated financial information. This is a process-only request; receipt of the information is not stated. | p. 34, lines 2070–2071 |
| S46 | 2 November 2020 | H remains interested but cannot submit while another transaction remains under pursuit. Review a temporary withdrawal versus continued interest. | p. 34, line 2072 |
| S47 | 19 November 2020 | I signs an NDA for the portal and advertising business and starts diligence. Partial context only. | p. 34, lines 2073–2075 |
| S48 | 8 December 2020 | I submits a partial LOI for the portal and advertising business. Other-scope bid; amount undisclosed. | p. 34, lines 2076–2079 |
| S49 | After 8 December 2020 | Further partial outreach produces no near-term proposal. Do not invent whole-company entry or another whole-company round. | p. 34, line 2080 |
| S50 | 14 December 2020 | E substitutes a $2.00 per-share tender for 35% of the shares. It requests a standstill waiver, management changes, board rights, and a rights plan. | pp. 34–35, lines 2081–2096 |
| S51 | 14 December 2020 | E states it no longer wants its earlier 100% transaction. Required Withdrew; note “continued on a partial basis”. | p. 35, lines 2096–2097 |
| S52 | 17–18 December 2020 | The committee requests support for E's revised structure and a meeting with its CEO nominee. E agrees to provide analysis. Review material process requirements; exclude routine meeting arrangements. | p. 35, lines 2099–2105 |
| S53 | 18–21 December 2020 | Synacor directs renewed approaches to CLP, G, and H. CLP and H show preliminary interest. CLP then accelerates diligence. | p. 35, lines 2107–2109 |
| S54 | 18–21 December 2020 | G states it will not pay more for the software and services business. Review another partial price ceiling or reaffirmation. | p. 35, line 2109 |
| S55 | 29 December 2020 | I reaffirms its partial interest. Part of its consideration depends on recent business performance. Record the contingent component separately. | p. 35, lines 2112–2113 |
| S56 | 29 December 2020 | E adds a 20% minimum tender condition and requires a public board recommendation. Its partial offer expires by 4 January. | p. 35, lines 2113–2114 |
| S57 | 30 December 2020 | The committee decides to let E's partial proposal expire and continue CLP, H, and I discussions. It directs further non-binding LOIs. | pp. 35–36, lines 2116–2136 |

S50 and S51 are different observations: the partial bid and the end of whole-company participation.
The 30 December decision cannot create a second whole-company exit for E.
An E14 exception must support any uninterrupted CLP participation across the September exclusivity event. The reported termination itself argues against that exception.

### January–February 2021

| ID | Date or bound | Required observation or review | Source anchor |
| --- | --- | --- | --- |
| S58 | 4 January 2021 | CLP offers $1.88 per share in cash for all equity and awards. The two-step structure still buys the whole company. | p. 36, lines 2137–2141 |
| S59 | 4 January 2021 | CLP says it can fund the full amount through equity and its proposal does not depend on third-party debt. Code from this communication. | p. 36, lines 2139–2140 |
| S60 | 4 January 2021 | The committee seeks better CLP and E offers and a written H proposal. Record material price feedback or proposal requests. | p. 36, lines 2141–2142 |
| S61 | 4 January 2021 | E declines an invitation to resume a 100% acquisition. Its partial tender expires after that day. No whole-company re-entry or second exit. | p. 36, lines 2143–2144 |
| S62 | 5 January 2021 | Synacor asks CLP for a higher price and sends an LOI with price still open. No new CLP Bid merely because it will review the request. | p. 36, lines 2145–2147 |
| S63 | By 6 January 2021 | Canaccord reports CLP's increase to $2.00 and its request for 30 days of exclusivity. Preserve the communication date bound. | p. 36, lines 2148–2149 |
| S64 | 6 January 2021 | The committee chooses the CLP LOI and definitive negotiation. Open the E6(c) round after the reported bid. | p. 36, lines 2150–2151 |
| S65 | By 6 January 2021 | If H remains a whole-company entrant, close it at exclusion from the CLP stage under E14. This precedes the later exclusivity execution. | p. 36, lines 2150–2151 |
| S66 | 7 January 2021 | CLP and Synacor execute the LOI. Record executed exclusivity; do not add a price observation without a new offer. | p. 36, lines 2153–2154 |
| S67 | 8 January and later weeks | The parties start and pursue diligence. Use only within eligible condition windows; ordinary sessions need no rows. | pp. 36–37, lines 2154–2169 |
| S68 | 21 January 2021 | CLP's counsel sends its initial merger agreement draft. First qualifying document confirmation after definitive negotiation. | p. 37, lines 2170–2171 |
| S69 | 27 January 2021 | The target draft adds a reverse termination fee and restrictions on the equity letter. Review the new material requirement separately from routine legal changes. | p. 37, lines 2172–2175 |
| S70 | Rest of January into February | The parties continue diligence and exchange drafts. This supports Incomplete where the bid's evidence window reaches it. | p. 37, lines 2176–2177 |
| S71 | 8 February 2021 | The board requires $2.20 to consider approval. Canaccord relays it. CLP says it will consult its investment committee. | p. 37, lines 2182–2185 |
| S72 | 9–10 February 2021 | Negotiations reduce the target termination fee to $3.0 million. CLP refuses a reverse termination fee. Review the bidder commitment response under E10. | p. 37, lines 2186–2190 |
| S73 | After that refusal, by 10 February | CLP requires support agreements from two significant stockholders. Review a separate condition-on-proceeding Bid. The source says “subsequently”. | pp. 37–38, lines 2190–2202 |
| S74 | Later on 10 February 2021 | CLP offers $2.20, requires a $3.5 million target termination fee, and demands execution that day and announcement the next morning. | p. 38, lines 2204–2206 |
| S75 | 10 February 2021 | The fairness account confirms $2.20 cash. The board approves. Ordinary approval does not add a duplicate price Bid. | p. 38, lines 2207–2218 |
| S76 | Later on 10 February 2021 | Parties execute the merger and support agreements. CLP Fund V, Parent, and Purchaser execute the equity letter. Winner Count 1. | p. 38, line 2219 |
| S77 | 11 February 2021 | Synacor announces the merger agreement before markets open. Separate Merger announced row; Who is Synacor. | p. 38, lines 2220–2221 |

S68 should copy only the latest stated price and consideration cells under the document-confirmation rule.
Its conditions come from its own window. Its price is not a new price observation.
The bidder's legal adviser, Thompson Hine, belongs in a bidder note. It is not a target Adviser row.

## Bid economics and conditions

| Bid event | Firm source requirements | Review limits |
| --- | --- | --- |
| A, 6 February and 25 April 2018 | Two whole-company proposals; price undisclosed; Informal absent another E11 route. | Do not invent cash or financing facts. The prior NDA prevents Not begun merely from early timing. |
| C, 13 August 2019 | Whole company; Part stock; price undisclosed; Informal. | Cash-and-stock does not prove all financing is available. |
| F, 15 September 2019 | Other-scope bid; price cells blank. | The source gives no price, cash share, or financing terms. |
| E, 10 September 2020 | $2.00 cash; whole-company; rollover does not create partial scope or a group. | The rollover holder's diligence condition is not automatically E's own condition. |
| G, 14 September 2020 | Other-scope bid; cash consideration; debt and equity financing; H1 applies absent a commitment. | Keep an unknown segment value out of per-share cells. The cross-page scope needs a review locator. |
| CLP, 17 September 2020 | $1.35–$1.41 cash; committed capital from its private-equity vehicles. | Do not turn private-equity funding into debt financing or mark it contingent without contrary evidence. |
| E, 18 September 2020 | Same offer at $2.00; Requested exclusivity through 23 October. | Request alone does not mean Required. Do not make a long exclusivity period an H2 trigger without a diligence tie. |
| CLP, 22 September 2020 | Conditional verbal increase of 10%–25%; further diligence remains. | Record the stated percentage in the Note. Do not fabricate a per-share range from two earlier endpoints. Earlier financing does not copy across this revision. |
| I, 8 December 2020 | Partial proposal; amount undisclosed. | Do not apply the later contingent payment term backwards to this bid. |
| E, 14 December 2020 | Partial tender for 35%; $2.00 per share in the Note; price cells blank. | Management, board, and rights-plan requirements matter. Ordinary approval language is not enough for H3 without a condition on proceeding. |
| I, 29 December 2020 | Partial proposal with a performance-dependent payment; CVR/earnout Y; amount unknown. | The contingent component alone does not make conditions Heavy. Price and CVR value cells stay blank for partial scope. |
| E, 29 December 2020 | Partial proposal; minimum tender and public recommendation requirements. | Offer expiry on 4 January is not a bid due date. The public-recommendation condition requires an H3 review. |
| CLP, 4 January 2021 | $1.88 cash; explicit absence of dependency on third-party debt supports Committed. | A final signed equity letter in February cannot establish January's financing state. The January words must support it. |
| CLP, by 6 January 2021 | $2.00 revision and Requested 30-day exclusivity. The bid precedes the target's selection. | Review Informal versus any claimed earlier definitive decision. Do not apply the later selection retrospectively. Do not copy condition fields without a same-offer basis. |
| CLP, 21 January 2021 | Formal Bid reaffirmed by first document confirmation; copy the latest stated offer's price and consideration only. | Diligence continues. Review the pending equity-letter language within this window. Do not assume complete diligence or signed commitments. |
| CLP, 9–10 February 2021 | Review the reverse-fee refusal and subsequent stockholder support requirement as changed commitments. | New-price cells stay blank when price is not restated. Two actions are not automatically one communication. |
| CLP, 10 February 2021 | $2.20 revision; Formal after definitive negotiation. Note the $3.5 million target fee. | The same-day execution and next-morning announcement limits are not H3. Apply current-window conditions; do not inherit every earlier condition. |

The filing's labels “non-binding” and “letter of intent” do not decide Formality.
The September and early January price bids do not become Formal merely because later negotiations use definitive documents.
The 21 January document confirmation and February definitive bids are Formal under route 3.

The final signed deal uses committed equity and has no financing condition.
The source states that position on the cover and pp. 28–30, lines 1860–1863 and 1895–1906.
Those final terms cannot silently replace a prior bid's state. The equity letter is executed at S76, which closes the final bid's window.

The final price is $2.20 cash. The fairness account states that amount at p. 38, lines 2210–2213.
The cover states it at lines 27–37. The agreement summary converts each share to the defined Offer Price at p. 43, lines 2431–2434.

## Deadline and participation reconciliation

### The 17 September deadline

The source says: “Parties that remained involved in the process were requested to submit a non-binding indication of interest by September 17, 2020” (p. 32, lines 1998–1999).

Required treatment:

- Record the communicated due date and the operative Deadline row.
- Close eligible unnamed whole-company members with no reported offer under E14's cohort rule.
- E and CLP already submit by that date. Later revisions alone do not prove late delivery of their required initial proposals.
- H receives a further invitation on 22 September. Apply E14's exception before any inferred H non-submission exit.
- G's partial offer does not become a whole-company bid because it arrives before this deadline.

Enforced is the preferred deadline outcome. The target later chooses E and executes exclusivity on 23 September.
The source reports no revised bid due date and no accepted late first whole-company response.
Treat a different outcome as an economic claim that needs source support, not as a formatting defect.

### The 14 NDA parties

The source reports 37 outreach parties and 14 executed NDAs. It expressly combines whole-company and software-business scope.
Company E, CLP, G, and H may sit inside the 37 and 14. E3 forbids adding possibly included named entrants on top.
Company G is expressly partial-only. The source does not disclose every unnamed NDA party's scope.

A possible reconciliation allocates four named parties inside 14 and leaves ten unnamed parties.
It then removes G from the whole-company count, which yields 13 possible whole-company NDA parties.
That is an assumption about the unnamed scopes and H's membership. It is not an exact reported whole-company count.
E3 requires the inclusion treatment for a possible named member; it does not turn a mixed-scope total into known whole-company scope.

The auction screen is nevertheless Met in process 3. E and CLP are two independent whole-company participants with express confidentiality evidence.
A lower bound of two is secure. An exact higher screen number needs a scope note or Question.
Do not use an exact full-cohort count as a comparison oracle without that qualification.

### Named exits and returns

| Party | Required closure or bounded choice |
| --- | --- |
| A | One end on 20 June 2018. Do not add another exit at a later process marker. |
| C | One end in October 2019. A subsequent process restart closes no already-closed participation. |
| CLP | Ends on 23 September 2020 because active competing discussions stop. Returns through renewed target engagement in December, or by the accepted 4 January offer at latest. |
| E | Whole-company participation ends on 14 December 2020. Its January refusal to return does not add another exit. |
| H | September deadline survival follows the 22 September invitation if H entered. September exclusivity then ends its live participation. Later admission and the 2 November statement need explicit treatment. |
| H, final stage | If live on 6 January, inferred exclusion occurs at the CLP stage opening. A second 7 January or 10 February exit would duplicate it. |
| G, F, I | Partial-only parties. Do not invent whole-company withdrawals or non-selection exits. |
| Unnamed NDA members | Close each eligible whole-company member once, at its earliest supported event. Do not count the same unnamed cohort at both deadline and exclusivity. |

The 2 November H statement remains ambiguous. It reports continued interest but an inability to submit at that time.
Terms or process fits if that statement constitutes a temporary withdrawal. Continued interest is also plausible if no stage admission or withdrawal is established.
Any choice must reconcile the later December invitation and the January exclusion. Do not use later silence as proof of an earlier named exit.

## Difficult choices to preserve for the comparative review

| Issue | Recommended source-first position | Classification now |
| --- | --- | --- |
| Three processes | Record 2018, 2019, and 2020–2021. Exclude B and D from whole-company continuity. | Strong application of E1 and E5. |
| Explicit terminations of the first two efforts | Close the reported bidder once. Use inferred restarts where the source does not expressly end the full effort. | Marker choice needs review; process count is stronger than exact marker dates. |
| 2018 and 2019 round 1 dates | Use the later multibuyer outreach anchors, 8 May and 25 August. Earlier proposals remain round 0. | Preferred E6 application; review any early bilateral interpretation. |
| July 2020 round date | Preserve the adjacent 13 July direction and the mid-July outreach precision. | Source date ambiguity. |
| Exact whole-company NDA count | Secure screen lower bound two. Disclose any larger mixed-scope cohort allocation. | Unresolved source scope. |
| September E “best offer” request | Price feedback to one bidder; no automatic final round or Formal bid. | Strong default; review contrary procedural evidence. |
| 27 October reopening | Open an E6(d) round after E's exclusivity ends and renewed outreach occurs. | Strong E6(d) application. |
| 18–21 December reopening | Prefer a new E6(d) round after the solicitation gap. | Defensible alternative: implementation of the October stage. Required Review item either way. |
| H's 2 November state | Preserve both the stated interest and inability to submit. Reconcile the complete participation track. | Unresolved admission/exit interpretation. |
| CLP's 22 September price | Record a conditional bid with the reported percentage in the Note. Avoid a synthetic dollar range. | Strong E10/E13 application. |
| CLP's 6 January Formality | The offer precedes the target decision for definitive work. Use its own communication time. | Strong timing rule; exact communication day is bounded. |
| CLP document confirmation | Record 21 January as the first qualifying draft confirmation after definitive negotiation. | Strong E10 application. |
| February commitments | Review reverse-fee refusal and later support requirement separately. Preserve the absence of a newly stated price. | Material E10/E12 judgment; no automatic H3 from ordinary legal drafting. |
| Final-bid financing | Separate the final offer from later signed financing and earlier windows. | Window-sensitive coding; do not impose a benchmark from final deal facts alone. |

## Required review apparatus and exclusions

A complete extraction needs the mandatory Process Question. It should state the E5 results and the E6(d) choices.
The source supports further Questions about mixed-scope counts and H's participation, subject to Part F's five-Question limit.
Defaults belong in Review items rather than artificial Questions.

Part F calls for Review items on:

- The possible early bilateral rounds and the July date boundary.
- The 13, 16, and 21 September meetings where they bear on a proposed stage boundary or the 17 September deadline.
- The 27 October and December renewed approaches, including a boundary that the extractor keeps within one round.
- The 30 December and 6 January selections or requests where a round boundary is considered.
- Any Formal bid whose source label remains non-binding or LOI.
- Cross-page identity, count, scope, or date support, especially G and the 14-party reconciliation.

Do not reward the following extra observations without another applicable rule:

- A whole-company bidder unit for 180 Degree or each CLP acquisition shell.
- A new sale process for the B merger of equals or the D acquisition.
- An NDA or admission inferred from mere contact, absent the reported cohort reconciliation.
- A separate round for each improved price, committee meeting, or LOI execution.
- A bid deadline for E's partial-offer expiry, an exclusivity expiry, or the public tender expiry.
- A new bid for ordinary document exchanges after the first qualifying confirmation.
- A target Adviser row for CLP counsel Thompson Hine.
- A new equity financing bid merely because the parties execute the already agreed merger and equity documents together.

## State at completion

The source inventory is complete for the supplied filing. No comparison output was opened.
The material unresolved points are explicit above. They do not prevent later workbook review.
The parent should verify decisive comparative claims against the quoted source before the final model recommendation.
