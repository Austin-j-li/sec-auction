# Synacor percentage-price adjudication

**Recommendation: do not count this as a confirmed instruction error.** The endpoints support a defensible exact calculation. The instruction does not clearly resolve this percentage-range case.

The assigned row is candidate A, Deal ledger Excel row 43. It records $1.485 and $1.7625 for CLP's September 22 revision. The supplied Note explicitly gives the endpoint calculations. This review uses that row description, the current instruction, and the source filing only.

## Source

On September 17, CLP proposes $1.35–$1.41 per share. On September 22, CLP says it would consider a 10%–25% increase per share from its earlier indication, subject to further diligence. Thus, the later communication expressly incorporates the earlier price. Both passages appear on printed p. 33: [HTML lines 2038–2040](/home/uctpiaj/work/Projects/sec-auction/raw_filing/synacor_2021-03-03_SCTO-T.htm:2038) and [2046–2048](/home/uctpiaj/work/Projects/sec-auction/raw_filing/synacor_2021-03-03_SCTO-T.htm:2046).

The calculations are exact:

- Lower endpoint: $1.35 × 1.10 = $1.485.
- Upper endpoint: $1.41 × 1.25 = $1.7625.

These are the outer bounds from the two reported ranges. The filing does not expressly state the resulting dollar range or explain how each percentage maps to each earlier endpoint.

## Instruction

[Part B, lines 24–26](/home/uctpiaj/work/Projects/sec-auction/SEC_Deal_Ledger_Extraction_Instruction.md:24) permits exact calculations from reported figures, but prohibits invented ranges and requires the source's precision and qualifiers.

[E10, line 253](/home/uctpiaj/work/Projects/sec-auction/SEC_Deal_Ledger_Extraction_Instruction.md:253) requires each revision's own evidence. It also requires blank price cells when no new price is stated. This communication states a quantified price change and expressly identifies its base. Use of that base is not silent inheritance from another bid.

[E13, lines 310–312](/home/uctpiaj/work/Projects/sec-auction/SEC_Deal_Ledger_Extraction_Instruction.md:310) requires per-share endpoints for the bidder's own range. It expressly bars some conversions, including total-value bids without a per-share figure. It gives no comparable prohibition for a percentage revision of an identified per-share price.

## Ruling

A strict reading can reserve the price cells for an expressly stated dollar range and place this percentage revision in the Note. Another reading permits the disclosed calculation under Part B. The endpoints use reported bounds; they introduce no estimated midpoint, outside figure, or unreported percentage.

The distinction between a derived outer bound and the bidder's own new range remains unresolved. It prevents a decisive error finding. Preserve the source's “would consider” and diligence qualifications in any treatment. This ruling covers only the numeric endpoints; it does not assess other cells.

**Final count: zero confirmed errors for this disputed endpoint calculation.** Record an instruction ambiguity if the comparison tracks unresolved issues.
