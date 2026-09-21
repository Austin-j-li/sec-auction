# Kraton: substantive review of the existing v1.11 workbook

Verdict: **usable after targeted corrections and a round-convention decision.** The winner, price sequence, principal competitive stages, non-comparable segment bids, and Party H's valuation-revealing withdrawal are well represented. The clearest factual miss is Parent's exact dated NDA in the merger agreement. The round count and cash earnout coding need explicit research decisions; they should not be disguised as settled source facts.

This retrospective review changed no workbook or instruction. Filing references use `/tmp/sec-extraction-review-20260921/kraton/filing.txt` paragraph labels. Ledger event #n is worksheet row n+1.

## Source coverage and old-reference status

- Read all of the background P00548-P00622, pp.31-41, all 62 ledger events, all three Rounds entries, all eight Questions, and all Deal facts.
- Checked Parent's operating-company description P00527 p.29, the consideration/financing and agreement context, the management-projection section P00763-P00784 pp.52-54, and the June3 confidentiality-agreement definition P01472 Annex A-4. The projections chapter names the board/J.P. Morgan as recipients; it does not establish an omitted delivery to a specific bidder. The stage-specific management access is captured in the ledger.
- Read newer voice notes V0078-V0086 and applicable cross-case guidance. Relevant case-specific Kraton paragraphs have no explicit colored runs in the formatting export; the comment export is empty.
- Old reference rows **96-130 are substantive**, not placeholders. They contain NDAs, bids, and exits. The March3 PDF email pp.1-2 identifies nine cases personally augmented/corrected by Alex; Kraton is not one. These are inherited Chicago RA coding. V0079 explicitly says Alex had not previously read this deal. New voice guidance and independent filing reconstruction therefore outrank old labels.

## Independent reconstruction and arithmetic

The late-2020 plan included selling CST while attempting acquisitions/combinations of other parties' polymer businesses. The failed effort to buy A/B's businesses is not a Kraton sale approach. May20, 2021 is the whole-company sale decision; May24 directs the 14-party outreach. The filing explicitly distinguishes 14 contacted prospects and one inbound strategic party. Ten sign NDAs (six strategic, four financial), five decline. Nine of those ten attend management meetings (five strategic, four financial), so the unnamed signer who withdraws rather than attend is strategic. CST parties C/D/E/G receive their own management meetings and are separately tracked; D/E leave June23/June18.

By July2 there are four whole-company bids: A $42-45, H $41-43, Parent $41, I $40. K proposes the chemical segment at 9-10x adjusted EBITDA; C/G propose portions of CST at $100m/$330m. J's first whole-company proposal is awaited. July6 asks the four whole-company bidders to improve by July19. A/Parent move to $45, H to $42-45, I refuses to improve $40, and J gives its first $38-41 range. July20 advances A/H/Parent to greater diligence while continuing to evaluate component bids. A later final letter asks for September8 agreement markups and September15 final prices. H leaves August20 because it cannot sustain its previous range.

The final priced sequence is Parent $46 (September15), A $40.50 plus a separate $1.3bn polymer alternative (September17), Parent $46.50 (September20), A $42 plus earnout (September21), and A $44 plus a revised earnout (September24). The board rejects the earnout/package risks and signs $46.50 cash September27, announcing separately that morning. K's revised September9 9.5x/$1.25bn chemical proposal cannot be substituted for a whole-company price; the board's $44-51 and $46-48 SOTP analyses are not bidder offers.

Arithmetic under the workbook's NDA-membership assumptions: 10 initial NDA entrants plus four CST entrants; subtract one unnamed NDA withdrawal, E/D withdrawals, and three residual NDA non-submitters, leaving eight (A/H/Parent/I/J/K/C/G). July20 removes I/J, August4 removes G, August20 removes H, leaving Parent/A/K/C. One additional post-Reuters financial NDA entrant has uncertain entry timing and never bids, then is closed at signing. At signing the five possible live units reconcile as one winner plus A/K/C/that financial party. The initial 15 outreach/inbound prospects plus six additional post-Reuters contacts must not be conflated with 11 total NDA parties or with the separate CST participants. The workbook captures those populations separately.

## Confirmed corrections

### K1. Parent's June 3 NDA is specifically dated in the supplied filing

**Class:** confirmed source omission and false uncertainty. **Severity:** medium. **Confidence:** high.

**Cells:** Deal ledger C12/P12/U12/V12 (#11); Questions B4/C4/D4 (Q3); Rounds E2. Q3 says "No party is named as a signer" and treats Parent's NDA membership as assumed.

**Evidence:** P01472, Annex A-4, defines the confidentiality agreement as "between Parent and the Company dated June 3, 2021". Old reference AA96/AB96 already carries June3 and AC96=NDA; the correction is independently supported by the filing, not accepted merely from the old workbook.

**Rules:** A requires checking other filing sections for dates/counts; C3 residual cohorts and C9 NDA events.

**Consequence:** The winner's date of entry is unnecessarily obscured inside the six-strategic cohort and an uncertainty that the filing resolves remains in a Question.

**Smallest correction:** Split Parent's June3 NDA into its own row and reduce the strategic residual from six to five, retaining total initial NDAs=10. Update Q3 so uncertainty concerns only parties not independently identified as signers. Do not increase the auction-screen count.

### K2. September 8 is a markup deadline, not a bid-price deadline

**Class:** confirmed C11 event-scope error. **Severity:** low. **Confidence:** high.

**Cells:** Deal ledger E45/P45 (#44); Rounds F4/G4; Questions B6/C6/D6 (Q5).

**Evidence:** P00592 p.37 distinguishes "markups of a draft merger agreement by September 8" from "final indications of interest by September 15". P00602 p.38 reports both remaining bidders submitted markups September8. C11: "Only bid due dates are deadlines". The current `Deadline` row and `Passed without action` outcome suggest a bid deadline that elapsed without a selection step, when the requested drafting submissions actually arrived.

**Smallest correction:** Preserve the September8 markup submission and definitive terms as an appropriately labeled material event or connected Note, but remove the bid-deadline outcome. September15 remains the bid deadline, with A's late September17 price correctly accepted. This does not change formality: the markups are relevant support for the subsequent final bids.

### K3. The post-Reuters financial party's inferred signing closure uses the wrong exit label

**Class:** confirmed C16 classification error. **Severity:** low. **Confidence:** high.

**Cells:** Deal ledger E63/P63 (#62); Questions E7; potentially the ending description of its stage.

**Evidence:** P00580/P00583 pp.35-36 says the financial entrant signed an NDA, met management, and "did not submit any proposal". No deadline or admission to a specific dated solicitation is established. P63 expressly says the filing does not state when it stopped and it is being "closed at signing". C16 reserves `Did not submit` for a specified solicitation and supplies `Not selected at signing` as the fallback for participants last seen under NDA or diligence.

**Smallest correction:** Use inferred `Not selected at signing` dated by September27, preserving that no proposal was reported and the uncertain entry/stage timing. The total entry/exit arithmetic is unchanged; the fix prevents inferring a deadline-based dropout that the source never establishes.

### K4. Party J's exit is assigned to a round the workbook says it never entered

**Class:** internal round-assignment inconsistency under C8. **Severity:** low. **Confidence:** high on inconsistency; medium on preferred full reconstruction.

**Cells:** G36/P36 (#35), compared with G29/P29 (#28) and Rounds E3.

The workbook deliberately assigns J's late first proposal to R1 and says it was "not admitted" to R2; nevertheless G36 assigns the July20 exit to R2. C8 says an exit carries the round being left. P00584/P00585 pp.36 establish the proposal and exclusion but do not resolve a separate invitation into the July6 improved-offer group.

**Smallest correction:** If retaining the existing late-R1 interpretation, assign its exit R1. If admitting J into R2 upon the July19 review is intended instead, revise the Rounds description and bid/entry interpretation consistently. The exit date and whole-process count do not change.

## Material convention decisions

### K5. Three rounds versus the explicit first-final-request rule

**Class:** C8 coding tension requiring adjudication. **Severity if changed:** high for round-level data. **Confidence:** high on source chronology and literal rule; medium on intended convention.

**Cells:** Deal ledger #33/#37 (G34/G38), subsequent G values; Rounds C4/D4/H4; Questions C2/F2 (Q1).

P00585 p.36, July20, invites A/H/Parent to the "second round" and supplies greater financial/diligence information. It does not announce final offers or indicate that definitive negotiations have begun. P00588 August11 authorizes a draft agreement; P00592 p.37 says the final procedures letter followed that meeting. On a literal reading of C8 (first final solicitation opens a round even with unchanged bidders), this is a separate fourth round. The source does not prove the July20 stage was already final when opened.

The strongest defense of the current three-round map is that July20 launches one coherent final competition, and the August letter implements it; C8 also asks for the smallest coherent map and for scanning every paragraph of a round for finality. Alex V0082 calls the eventual formal round "round three" while insistently distinguishing the July6 informal advancement from the banker's two-round description. His comment predicts the subsequent formal round; it does not identify its exact opening date.

**Decision:** Prefer a separately dated final-solicitation opening under the explicit current C8 sentence, or explicitly approve the continuous July20-to-final-price stage and clarify that rule. Q1 usefully exposes the four-round alternative. Do not date a reported final announcement July20 using only the later letter. Preserve July6 as a distinct informal stage either way; that is directly supported by V0082 and the four-party improvement request.

### K6. Cash earnout guidance is not implemented as a positive cash classification

**Class:** newer Alex guidance mismatch, with filing-evidence limitation. **Severity:** medium. **Confidence:** high on mismatch; medium on a source-only correction to Yes.

**Cells:** J55/J56/P55/P56 (#54/#55); old reference AD127/AD128 are also NA.

P00614/P00616 p.40 describe $42 then $44 per share plus an earnout; the final earnout pays holders 50% of incremental net chemical-sale proceeds above thresholds if a binding sale agreement is entered before the main closing. Alex V0084 explicitly says this is a cash offer with an extra contingent cash payment, not mixed consideration. Current J55/J56 are `Not stated`, not `No`, and the earnout trigger is recorded. This avoids the mixed-offer error but does not implement Alex's positive classification.

C15 gives Yes for cash plus a cash-settled earnout, while also saying a dollar price alone does not establish cash. The supplied background never explicitly says the $42/$44 base itself is cash. **Decision:** either adopt Alex's Kraton-specific interpretation and code Yes, preserving the cash-contingent terms, or retain Not stated as a source-only limitation and raise a targeted Question. Do not classify these as mixed merely because payment is contingent, and do not insert an invented total price for the contingent upside.

### K7. Conditions that depend on inference should remain visible

**Class:** bounded uncertainty, not further confirmed errors.

- **L49/L50 (#48/#49):** A's September17 proposal is "subject to additional due diligence" (P00608 p.39). Heavy is plausible, but the text does not specify its scale or period. September24's confirmatory condition cannot by itself prove September17 diligence was substantive. Q8 appropriately identifies the Unclear alternative. September17's Formal whole-company label is independently supported by the final solicitation and September8 markup.
- **L24/P24 (#23):** K's initial proposal is labeled Heavy based partly on August30's report that it was "still subject to significant due diligence and the receipt of firm financing commitments" (P00596 p.37). The word "still" is evidence of continuing conditions, so this is not automatically prohibited hindsight. Nevertheless keep the later observation date visible and avoid treating a newly learned condition as an exact dated initial financing fact. The initial proposal also expressly refused a simultaneous back-to-back segment sale (P00577).
- **L47/L52 (#46/#51):** Parent's Light final bids are defensible: September15 says substantially all diligence completed; September8's terms explicitly remove financing as a closing condition (P00602/P00607). A draft debt commitment letter on September20 is not, by itself, a filing statement that financing is uncommitted. Q7 appropriately flags that distinction. None would need stronger affirmative readiness evidence.
- **J/K cohort membership and live counts:** Q3 admits that J/K membership in the ten-NDA cohort is inferred. The first-round process/invitation sequence supports it, but do not claim the identities are expressly enumerated. Initial exact population totals are not uncertain merely because names are incomplete. C/D/E/G's separate CST meetings (P00571) support their distinct tracked participation and do not support inventing NDAs for them, as the old sheet did.

## Correct results and rejected apparent errors

- Parent is resolved as strategic using the petrochemical-company description in P00527, p.29; no unknown winner remains. Formal bidder A is strategic. This directly answers V0081.
- Six strategic and four financial initial signers are correctly recorded, and the additional post-Reuters financial signer makes 11 total qualifying NDA parties. The 14-plus-one initial contacts are preserved separately, answering V0080 without double counting repeated steps.
- A's initial H20/I20=$42/$45 preserves the source range; the old reference V108/W108=$42/$42 loses the upper endpoint. Current September17 date for A's $40.50 bid is correct; old AA125/AB125=September14 is not.
- Party H's `Value below earlier offer` at N43 is exactly the economic information in P00594 and Alex V0083. Party I's refusal to improve $40 is preserved in its exit note and in the Rounds response count. It need not be invented as a new priced bid.
- K/C are not dropped merely because the board preferred a whole-company strategy. P00578/P00585 retain their proposals; P00600 requests K's updated proposal. Old AC112/AC113 mark premature July2 drops. Current signing closures avoid that source contradiction.
- Component bids are not converted into whole-company per-share numbers, and the board's SOTP valuation ranges are not fabricated bidder offers. A's polymer alternative is separated from its whole-company offer, with its own Informal label because scope-specific formal evidence is absent.
- Current formal final-stage bids do not inherit the old sheet's Informal labels: Parent/A submitted requested merger markups, and their September offers answer the final solicitation. This is current C13 evidence, not retrospective promotion because Parent later wins.
- Agreement execution and public announcement are separate September27 events, as V0085 requires. J.P. Morgan's first acting date is distinguished from the later formal engagement, and adviser clients are identified.

## Limits

The final round count, inferred entrant timing after Reuters, and some conditionality judgments require researcher adjudication. They do not justify replacing the well-supported bid sequence. No percentage accuracy is given because the old sheet is neither complete nor error-free, and no adjudicated gold standard exists. No web, git history, prior model grades, extraction run, or workbook revision was used.
