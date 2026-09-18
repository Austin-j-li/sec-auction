# Providence & Worcester: independent comparison of four extraction runs
**Austin Li / Alex Gorbenko — 18 September 2026**

## Verdict

**Overall ranking: 1. Astra high; 2. Fable 5.1 high; 3. DeepSeek 4.1 Flash max; 4. Muse Spark 1.3 xhigh.**

Use **Astra for the next quality-first extraction pilot among these four tested configurations**, with the readable-output override and continued human review. Fable is a close second, not a clearly inferior reader of the deal. DeepSeek is a worthwhile development candidate but not the current replacement. Muse requires more repair than its shorter output suggests.

This ranks **the four supplied artifacts**, not model families in general. The gap between Astra and Fable is much smaller than the gap between either and Muse. None is ready to be accepted without checking consequential judgments. A strongest-model policy is compatible with this recommendation; these files cannot establish which model is strongest across all available systems or other deals.

### Separate judgments

| Run | Substantive extraction quality | Presentation and practical correction | Main reason for its position |
|---|---|---|---|
| Astra | Best overall first-pass coverage and preservation of judgment, narrowly. Handles final offer states, the G&W continuation, reversion, and source conflict carefully. | Very wide and heavily normalized; avoidable date-display inconsistencies and repetitive review packets. | Most defensible starting record under quality-first priorities, after targeted chronology and checkpoint repairs. |
| Fable | Close to Astra. Sound price histories, explicit alternatives and participant-count reasoning. | Best self-contained navigation of the submitted runs, particularly Summary and SourceParagraphs, but still far too many tabs/columns. | Its exclusion code for G&W conflicts with its own correct explanation; some material dates/actions are bundled. Several disagreements with Astra are legitimate conventions, not errors. |
| DeepSeek | Useful extraction with many correct core facts and strong quotation fidelity. | Readable labels but broad tables; multiple exact-date claims need manual correction. | Confuses report/communication/action dates in consequential places and contains a deadline-link error. Some final offer-state information remains only in Events. |
| Muse | Weakest: omissions of separately usable observations, unsupported cash coding and inconsistent identities/links. | Shorter, but reconstruction and repair burden is high. | Corrupt canonical references, forward/cyclic proposal chains, broad event bundles and paraphrases presented as exact evidence. |

There is no pseudo-precise overall score. Counting rows, words, “high confidence” labels or a workbook's own validation assertions would be a poor substitute for this adjudication.

## 1. Basis, provenance and limits

I inspected the four workbooks programmatically, including their cell contents, formulas, source quotations, key relationships, dimensions and visible layouts. I read the full Providence background and checked the relevant other filing sections: transaction/party descriptions, consideration, board reasons, signed financing terms, regulatory developments and source dates. The native HTML, not another model's extraction, is the factual source.

I also examined Alex's collection instructions, his own voice-note comments and summary, and inline annotations across the **269 rows belonging to the nine reference deals**. The other Chicago-RA entries were not used as trusted examples. Annotations in `AG:AI` were read as cell text, not confused with separate Excel comment objects. “Claude's reading” and the separate AI analysis in the notes document are secondary synthesis. Alex's endorsement of a general summary does not turn every AI paraphrase into an independently established transaction fact.

The nine reference blocks contain examples, corrections, hypotheses and questions. In particular, Providence `AG6026` asks about initiation; `AH6035` asks about the formal threshold; `AG6058` questions an unannounced endpoint. Those are not settled coded truths.

**Source notation.** `BG-001`–`BG-029` refer to the supplied Providence background paragraphs, checked against the full filing, printed pp.27–32. “Reasons p.33” and “p.34” refer to the full filing outside the background. Workbook references are physical sheet/cell coordinates in the submitted originals, not event IDs. References to `deal_details!…` concern Alex's original workbook. The demo's Sources sheet preserves the background and supplementary passages.

### Comparability is limited

We have user-supplied model/reasoning labels, but not the complete prompts, conversation histories, exact model identifiers/builds, extraction timestamps, attachment order, actual file representations exposed to each model, tool permissions, output limits, retries, repair interactions or run transcripts. We also lack token usage, elapsed time and costs.

The workbooks indicate different implementation choices, but do not establish why they occurred. A broken link could be a reading error, a generation error or an untested spreadsheet-writer defect. The delivered artifact still needs repair, regardless of cause. The model recommendation is provisional precisely because the experiment did not isolate those factors.

No four-model rerun, blinded human grading exercise or timing study was conducted in this review. The demonstration is a new independent adjudication, **not a fifth benchmark run**.

## 2. What the filing actually supports

The central sequence is:

Party A expressed interest in equity/JV arrangements in late 2015; PWRR engaged GHF on January 27, 2016. The board approved exploration on March 14, the committee authorized outreach on March 24, and GHF actually contacted 11 strategic and 18 financial buyers in the week of March 28. The initial population yielded 11 strategic and 14 financial NDA signers. None of that establishes a priced whole-company offer by Party A. [BG-001–004, pp.27–28.]

Nine written IOIs arrived May 19–June 1, with a group price envelope of $17.93–$26.50. Two low bidders were excluded and seven invited to presentations and further diligence. Mid-June instructions requested LOIs and markups by July 20. New strategic entrant Party C signed an NDA, offered $21 on July 12 and subsequently received expanded access/presentation. [BG-007–011, pp.28–29.]

The six later LOI bidders were B, G&W, E, D, C and F. B/G&W/D submitted merger/voting markups; E supplied material issues and proposed changes. G&W's July 21 package was $21.15, including $20.02 cash plus a stated $1.13 CVR; July 26 increased it to $22.15, including $21.02 cash plus the CVR. All LOIs had material diligence or price-assumption issues. One strategic and one financial bidder did not submit LOIs; their identities and reasons are not given. [BG-012–019, pp.29–30.]

The committee selected B/G&W and excluded the other LOI bidders. D/E sought re-entry: August 1 brought D's $24 and E's $23.81 with financing support from F. August 2 E withdrew the higher proposal and confirmed $21.26. D would not continue diligence without a no-signing commitment the target declined to provide; D's exact withdrawal day is not separately stated. [BG-020–021, p.30.]

B was prioritized on August 4, but both finalists continued diligence. B's revised draft that day does not prove elimination of all conditions. On August 9 G&W was warned about an intended rival agreement but expressly allowed to continue diligence. G&W then offered $25 cash on August 12, without the CVR. B declined to raise $24. After comparing the documents and regulatory routes, the board selected G&W; signing occurred August 12 and public announcement August 15. [BG-022–028, pp.30–32; cover letter independently states the signing date.]

These facts permit a three-phase analytical map, but they do not turn every preferred boundary into an exact reported date.

## 3. Consequential findings, with original-cell references

### A. Source conflict: NDA totals are not a simple arithmetic exercise

The early narrative gives 11+14=25 signers; Party C later enters as a buyer that had not previously participated and executes an NDA. Yet the board's Reasons section says that, during the process, **25** buyers entered confidentiality agreements and six submitted LOIs. That is a genuine tension within the filing. [BG-004, p.28; BG-011, p.29; Reasons, p.33, paragraph beginning “the fact that the Company conducted a lengthy and thorough process”.]

Astra `Counts!M14/N15` records reported 25 and a conditional lower bound of 26. Fable `Counts!M8/N9/X9` also preserves the conflict and prefers the chronological interpretation; it does not simply miss the summary. DeepSeek `Counts!L4:L5/W4:W5` preserves both 26 and 25 and discusses alternatives, but putting **26 in count_exact** is stronger than its own unresolved-overlap caveat warrants.

Muse `Counts!P3` includes Party C among the early signers, while `W3` describes C as a later addition. This is an internal identity/population inconsistency, not merely disagreement about the summary.

**Recommendation:** keep each scoped assertion. Prefer an **at-least-26 chronological interpretation, conditional on the early population being distinct from C**, but do not certify an exact whole-process total. An imprecise retrospective summary is a plausible explanation, not a proved correction. The auction screen passes under either count. No unknown bidder should be invented or deleted to balance this.

### B. G&W was not actually excluded on August 9

Fable `Events!R59` is `bidder_excluded`, but `L59` correctly says this was not a permanent exclusion and G&W remained active. Muse `Events!E40/H40` makes a similar exclusion/displacement coding choice while also reporting continued diligence. The filing says G&W requested permission to continue diligence to improve its offer and that the request was granted. [BG-023, p.31.]

This is not evidence that either model completely misunderstood the narrative. It is a **canonical variable conflicting with the narrative qualification**. An analyst filtering exclusion events could wrongly create an exit/re-entry history for the winner.

Astra's corresponding August 9 record (`Events` row 69, event E068) and DeepSeek's treatment preserve the adverse notice without a false exit.

**Recommendation:** code intended rival signing/continued participation, not bidder exclusion. This is one substantive reason to prefer Astra over Fable narrowly.

### C. Event/report dates: DeepSeek repeatedly stores more precision than the source supports

| Original location | Problem | Filing support and correction |
|---|---|---|
| DeepSeek `Events!C12:D12` | The two additional Class I approaches are dated April 7 as exact reported actions. | At the April 7 meeting management said it **had also approached** them. Record “by April 7,” not contacts on that day. BG-006, p.28. |
| DeepSeek `Events!C14:D14` | April 27 is the exact date of setting the initial IOI deadline. | The board reported buyers **had been advised** of May 10. Communication date is unknown. BG-007, pp.28–29. |
| DeepSeek `Events!W15:X15` | Deadline postponement is bounded April 28–May 10. | “Subsequently postponed to May 19” does not prove the change occurred before May 10. Preserve the supported window without that extra constraint. BG-007. |
| DeepSeek `Events!C46:D47` | D's request and withdrawal receive August 2, exact reported. | August 2 explicitly dates E's withdrawal/reversion. D's adjacent sequence lacks its own day. August 2 is a plausible inference, not a reported fact. BG-021, p.30. |
| DeepSeek `Rounds!I3` | The “latest general deadline” points to E021, the deadline-setting event. | The requested submission date is July 20; the setting communication occurred mid-June. This repeats the distinction Alex explicitly emphasizes. BG-009, p.29. |

These are not cosmetic date formats. They can affect waiting times, deadline enforcement and assignment of offers near boundaries. The appropriate repair is not simply a different midpoint.

### D. Astra's chronology is not clean despite its stronger overall extraction

Astra `Events!B49` displays approximately July 27 for finalist selection, while the next exclusion row `B50` displays approximately July 25. `Y49:Z49` fixes the working selection window to July 27, but `Y50:Z50` allows an earlier exclusion. The filing says the remaining bidders were contacted **subsequently**. [BG-020, p.30.]

Likewise, `Events!B22:B24` displays the June 1 review followed by approximately May 27 exclusion/admission rows. The source describes May 23 and June 1 reviews and a selection whose precise day is not uniquely stated. The problem is treating independent midpoint assignments as an intelligible chronology.

The D condition sequence is displayed around August 6 before records with August 3/4 dates (`Events` rows 61–67; `Bids` rows 14–15). D's date is genuinely uncertain; a broad interval can be correct while the preferred reading order is unnecessarily confusing.

**Recommendation:** show intervals/source wording and supported precedence; stop promoting midpoints into the principal date display. These are repairable but real defects. Astra does not earn a clean chronology grade.

### E. Party B's August 4 draft: disagreement is partly caused by the old instruction

Alex `deal_details!AC6054` says “Executed,” and `AG6054` says the earlier bid was confirmed after diligence. Voice note I.14 proposes an unconditional $24 offer on August 4. The raw filing establishes a revised draft from B's counsel, a target response August 5 and continuing diligence July 27–August 11. Actual signing is August 12. [BG-022–024 and BG-028.]

Astra `Bids!W15` calls the August 4 observation a `commitment_revision`. The document update is real, but **stronger commitment is not separately demonstrated**. Its heavy conditionality is a defensible conservative judgment, not proof that all conditions remained unchanged.

DeepSeek (`Events` row 50) and Fable (`Events` row 57) retain a document-update event without creating another priced Bids row. That was explicitly allowed by base §8.1 and its Providence calibration example. **Do not score these outputs as missing a required new formal bid merely because Astra emitted another Bids row.**

Fable's row also carries the August 5 target response under an August 4 headline, reducing chronological granularity. Muse compresses more of this development into surrounding negotiation text.

**Demo:** separate August 4 and 5; retain $24 as carried forward; show a formal document checkpoint with heavy preferred/possible light conditionality; no new-price or execution claim. Whether the update qualifies as a substantive new commitment version is a research convention requiring calibration.

### F. Final B offer and refusal to increase

Astra `Bids` row 17 and Fable's final B proposal row retain a final $24 standing-offer assessment. DeepSeek records the refusal in `Events` row 59 but does not provide the equivalent final offer-state row in Bids; Muse also lacks that separately usable final observation.

This is a **coverage/representation weakness**, not a failure to mention B's refusal at all. It matters because comparing final offers using only Bids would otherwise compare G&W's final developed package to B's earlier diligence-heavy state.

The source supports final reaffirmation as a contextual assessment: B's final documents were available, the board asked whether B would improve, and B declined. It does **not** establish voluntary withdrawal or private value exactly equal to $24. Alex's old `AC6056` “Drop” should not be treated as an unquestionable fact. [BG-025–026, pp.31–32.]

### G. E's August 2 reversion must remain usable

Astra, Fable and DeepSeek separately retain E's restored $21.26 proposal. Muse `Events!H37` mentions it inside a bundle spanning July 29–August 2, but its Bids table has no separate restored-offer observation.

That bundle also combines D/E re-entry, two August 1 revised bids, E's withdrawal/reversion and D's conditions/withdrawal. It is readable prose but not a satisfactory independently filterable research record.

The source explicitly distinguishes withdrawal of E's revised proposal from confirmation of its original proposal. [BG-021, p.30.] The demo separates those observations.

### H. CVR is not synonymous with “not all cash”

Muse `Bids!AY5:AY6` sets `all_cash=0` for G&W's July offers. The filing states fixed cash plus a CVR linked to a property sale but does not explicitly specify the CVR settlement medium. Contingency alone does not establish non-cash settlement. [BG-014, p.29.]

The other three runs handle the components and unknown settlement more carefully. They should not be faulted for declining to call the full package certain cash.

**Recommendation:** preserve package value, fixed closing cash, contingent stated component and settlement status separately. A cash-only flag can remain unconfirmed. The final $25 cash offer is clear and separately removes the CVR. [BG-024, p.31.]

### I. Material conditions and source-time leakage

DeepSeek's condition discussion for E's August 1 proposal (`Bids!I12`) draws on its withdrawal the next day. That later behavior is an outcome, not an as-of-August-1 offer condition. The express 30-day diligence requirement already supports a heavy assessment; no hindsight is needed. [BG-021.]

Fable's financing-support discussion should similarly not turn the presence of F support into an expressly necessary dependency or a firm financing commitment. A financing-support relationship is disclosed; its exact commitment/contingency terms are not.

The final merger agreement expressly lacks a financing condition. That is available from Reasons p.34 and appropriately helps characterize the signed transaction. It cannot be projected backward onto G&W's July LOIs. Astra makes this temporal distinction particularly clearly in its final transaction records.

### J. Type, consortium and initial identity inferences

All four correctly have enough material to identify G&W as a strategic buyer; the full filing p.21 also establishes public listing and U.S. corporate identity. Naming an acquisition vehicle separately must not add a competing bidder.

The full background calls F **strategic** [BG-018], contrary to Alex's old `S6039/S6049`. The old E/F mixed-bidder representation (`N6051/S6051`, with financing noted at `AH6051`) is stronger than BG-021 establishes. The current outputs generally improve on that old reference by keeping financing support distinct from a proven consortium.

Party A's exit is a different matter: voice note I.11 expressly offers a low-confidence narrative inference that A never advanced. The filing does not identify A among initial bidders, the two low exclusions or the later non-submitters. A lack of later named mentions is not enough to resolve that mapping. Preserving uncertainty here is good extraction, not lack of judgment.

## 4. Disagreements that should not be treated as objective errors

### E's issues summary: formal or informal?

Fable `Bids!I6:J6` prefers informal: only an issues/proposed-changes summary is reported, not full markups. Astra `Bids!F6:G6` and DeepSeek prefer formal based on substantive engagement with merger/voting terms.

Both interpretations have a rationale. Alex clearly establishes actual bidder markups as strong formal evidence; he does not supply a settled universal threshold for a substantive issues list. Diligence and exclusivity should not mechanically decide formality.

The demo uses **formal at medium confidence**, with Fable's informal alternative preserved. This is a proposed calibration, not a factual finding that Fable misread the filing. It should be revisited before estimation, especially because E's subsequent versions inherit it.

### D/E August bids: current negotiation phase or earlier response round?

Fable `Bids!T11:T13` assigns the August 1–2 revisions/reversion to R02 while separately recognizing receipt during R03. Astra and DeepSeek use the final-negotiation phase.

The base instruction allowed primary response-round and receipt-round distinctions. Fable's choice is therefore not simple instruction noncompliance. I prefer R03 because these are re-entry attempts against the selected finalists after exclusion, not merely delayed responses to the original July 20 solicitation. The demo preserves that preference and the alternative in R1.

### March launch, June selection and finality

March 14 strategy approval, March 24 outreach authorization and week-of-March-28 actual outreach are all relevant. Alex's later general default favors actual outreach for an unlabelled first-round start; the base instruction also allowed operative authorization. These mixed instructions partly explain different round starts.

Similarly, a mid-June process letter is not the only plausible second-round start: admission and enhanced access were authorized after the May/June reviews. The demo anchors that substantive transition and retains uncertainty over the exact selection day.

July 27 can serve as a working transition/end-of-stage date, but not a reported replacement deadline. The final negotiations are inferred as final; their “final” status is not an expressly announced July deadline.

## 5. Evidence fidelity, links and self-validation

A mechanical check compared nonempty `Evidence.verbatim_quote` cells with the full filing after normalizing HTML entities, Unicode representation and whitespace:

| Run | Nonempty quote cells checked | Contiguous normalized matches |
|---|---:|---:|
| Muse | 21 | 2 |
| DeepSeek | 194 | 194 |
| Astra | 507 | 506 |
| Fable | 163 | 163 |

These are **not accuracy scores**. Muse's nonmatches commonly reflect ellipses, altered punctuation or stitched/paraphrased text, not necessarily invented underlying facts. Conversely, DeepSeek's exact quotations coexist with incorrect date attribution. Matching text does not establish the associated date, identity, phase or judgment.

I did not count hundreds of repeated quotation cells as independent corroboration. Astra's much larger Evidence table contains repeated premises supporting different fields. Its single nonmatch should not be read as a demonstrated material factual error.

Muse also has substantive reference failures. `Deal!L2=E34` points to on-site diligence (`Events` row 36), not signing. `Deal!M2=E35` points to the D/E bundle (`Events` row 37), not public announcement. The correct signing/announcement events exist elsewhere; the summary's canonical links are stale.

Muse `Bids!AA5` points the initial G&W LOI to its later revision, while `AA6` points back. Similar forward references appear in the initial E/D histories (`AA7:AA8`). This is not harmless formatting: a prior-version graph must not cycle. Additional fields contain values of the wrong kind, such as “reported” in predecessor-ID fields. A validator must check both key existence **and semantic compatibility**; a valid event ID can still identify the wrong event.

The other three runs did not show the same unresolved-key pattern in the explicit link fields checked. That limited finding does not certify every cross-reference.

Own “pass” claims were not accepted as evidence. In particular, Muse's validation cannot overcome the independently observed stale references and cycles.

## 6. Presentation: the previous instruction is part of the problem

The previous specification required ten linked tables, a separate field-level evidence ledger and extensive physical schemas. Its brief instruction to put readable columns first did not resolve the underlying burden. The resulting event tables contain roughly 68–75 columns and offer tables roughly 65–76 columns. That architecture rewards exhaustive serialization more than economical human review.

Astra's evidence precision comes with substantial duplication and repetitive conditionality review packets (`Review` rows 8–12). Fable's Summary and SourceParagraphs help, but its thirteen tabs still require navigation. DeepSeek's labels are approachable but its tables remain very broad. Muse's shorter representation transfers effort to the researcher through bundled events and broken links rather than actually eliminating complexity.

**Instruction-caused problems:** too many mandatory tables/fields; field-level audit trails physically separated from the decision; too much freedom over submission versus checkpoint representation; an ambiguous operative-launch exception; representative dates promoted into human chronology; repeated policy/condition confirmations.

**Individual-run problems:** unsupported exact dates, an exclusion code inconsistent with continued participation, stale/cyclic IDs, scope-inconsistent NDA membership, CVR cash coding, absent independently usable reversion/final-offer states, and quotations not actually verbatim.

The new output instruction replaces the mandatory physical structure rather than merely restyling it. It does not approve the substantive C1–C7 defaults or change the research sample.

## 7. The demonstration workbook and its corrections

`Providence_Worcester_Review_Demonstration.xlsx` contains five visible sheets: **Deal guide, Timeline, Offers, Review decisions and Sources**.

Timeline contains 60 material/context records with names, prices, outcomes, judgments and source quotations locally readable. Offers contains 13 individual proposal/reaffirmation observations, one nine-bidder group envelope and two explicitly non-submission document/condition checkpoints. Those **16 displayed rows are not 16 new bids**.

Seven grouped review packets cover phase mapping, counts, deadlines, judgment calibration, consideration, participation outcomes and readiness. Twelve entries in a separate AI adjudication log on the same sheet identify original cells, changes, filing support and whether each change is a correction or a provisional convention. Human correction fields are blank and statuses Pending.

Sources contains the complete background and relevant additional filing passages. The principal sheets have native internal evidence/review links, frozen headers, filters and collapsed technical columns; numerical prices and date fields remain available for export. Ordinary reading does not require joining IDs. Hidden columns can be unhidden normally.

The demo is not a verbatim copy of Astra or an averaged consensus. It makes the independent judgments described above, including the qualified NDA count, current-phase re-entry assignment, E's provisional formality, B's August 4 checkpoint and the absence of a G&W exit. It also separates September 1 and September 14 regulatory filings, rather than bundling them into a single approximate event.

All four originals were preserved and their SHA-256 hashes rechecked. The manifest records file identities and mechanical test scope. Workbook layout previews, formulas, table extents and native hyperlink/freeze metadata were checked; **an interactive desktop Excel session was not run**. Free-text human notes do not automatically propagate corrections: a reviewed version must be regenerated and validated.

## 8. Immediate action

Use the base extraction instruction **plus the new presentation override plus the full new filing** for the next Astra extraction. Retain human verification of consequential structure, conditionality, participant counts and uncertain exits. Review the seven demo decision packets once to approve conventions that should generalize; do not silently treat the demo as those approvals.

Keep Fable as the close comparison candidate. Do not downgrade extraction quality to seek savings on the basis of Providence alone. The separate development note explains which lower-cost experiments are worth pursuing without changing the current extraction policy.
