# Current research state and decisions

Updated 27 September 2026 after checking the recovered files, original reference notes and decision records. This is the current entry point; Austin requested deletion of the old `_dev/HANDOFF.md`. Historical packets describe their dated work, not additional current approval holds.

## Evidence boundary and current state

The latest saved cockpit observation is **27 September 2026, 10:55:33 UTC**. All 162 files in its [index](recovery/2026-09-27-cockpit/INDEX.json) match their recorded sizes and SHA-256 hashes. Later local decisions are included below. This is not a live VM check.

- **Instruction:** the root [v1.14.1 instruction](../SEC_Deal_Ledger_Extraction_Instruction.md) exactly matches the published cockpit text, SHA-256 `8a93df3cc6d989386958e9cb2d74ab34ebc0f07d281e8cc398605a388e066c98`. The saved cockpit identifies it as the default. Copying it here was Austin's approved laptop recovery action; it does not establish that the VM repository export happened.
- **Raw workbooks:** the nine files in `extraction/` remain the 22 September Opus 5.5 medium v1.13.2 extractions. Preserve them separately from review edits.
- **Working copies:** all 13 cockpit working copies still have v1.13.2 bases. Eight are `in_review`, five `unreviewed`; none is accepted. Eight edited original deals have 454 `reviewed` row marks and 66 `needs_decision` marks. These record earlier assisted review, not Austin's completed acceptance, and are not 66 distinct research choices.
- **Mechanical checks:** the nine original deals' saved working copies total **0 errors / 157 warnings**. The older **3 errors / 161 warnings** describes the raw re-extraction set, not these working copies. Checks do not establish substantive accuracy.
- **New runs:** five separate raw v1.14.1 versions exist, all Opus 5.5 medium; none has become its working copy's base. The [retest packet](reviews/2026-09-26-v1141-retest/README.md) records targeted behavioural checks, not complete source review.

| New v1.14.1 run | Saved errors / warnings | Saved rounds |
|---|---:|---:|
| Mac-Gray | 0 / 2 | 3 |
| Providence & Worcester | 0 / 2 | 3 |
| sTec | 1 / 3 | 2 |
| Synacor | 0 / 6 | 6 across 3 processes |
| Datalink | 1 / 4 | 4 |

The two errors are Count 1 on Merger announced (sTec event 56, Datalink event 76). Their correction is decided but not present in these saved raw versions. The four other original deals, Kraton, Meredith, Penford and PetSmart, have no v1.14.1 run in the snapshot.

## Decisions to discuss now

Distinguish a filing error under an existing rule from a change to the research convention. The published instruction governs extraction until Austin authorizes a change. Alex's outstanding confirmation does not make every existing default an unresolved instruction.

### 1. sTec: when did the final round begin?

**Open reconciliation with Alex:** May 16's final-round letters versus May 29's best-and-final request. The [filing](../raw_filing/stec_2013-08-08_DEFM14A.htm), printed p. 30, calls the earlier letters final round process letters and later describes the proposals as non-binding. Alex's voice note (body paragraph 125) calls the May 28 offer formal but says the round was not final.

Under current E6, finality describes the announced procedure; non-binding does not itself mean Not final. The v1.14.1 run has two rounds, consistent with questionnaire map A. Alex's alternative starts the final stage later and counts three. The old working copy's extra round after WDC's May 31 withdrawal has no identified v1.14.1 trigger; it is not another equally supported current-rule option.

**Recommendation, not a new ruling:** retain the published-rule reading while asking Alex whether his intended research convention differs. Discuss the general meaning of a final stage, not just how to make this deal match a label. Company H's exit is settled separately below.

### 2. Conflicting reference sources

**Open with Alex:** what governs when his spring hand coding and later voice notes disagree? Examples are sTec finality and Providence & Worcester Party A's departure.

The questionnaire offers voice notes first, hand coding first, or a distinction between general conventions and case-specific factual readings. **Recommendation, not an approved hierarchy:** an explicitly agreed research convention governs coding; filing facts are checked against the filing; conflicting reference readings are brought to Alex rather than automatically treating either reference as ground truth. Model agreement with hand coding is not an accuracy measure where the intended convention differs.

### Other confirmations under existing rules

The [recovered questionnaire](maintenance/2026-09-24-bid-terms-taxonomy/Questions_for_Alex_2026-09-25.docx), sections 2b and 3.4, asks Alex to confirm working conventions on financing commitments, partial bidders, round triggers, merger-of-equals talks, price-only revisions, the condition evidence window, missed due dates and deadline outcomes. Penford Party A's October 4/13 valuation statements versus its October 14 $16 bid remain a specific confirmation. The process-boundary convention (E5's three-part test, including a reported end or 90-day silence) also awaits his confirmation in the research record.

NDA reuse, WDC's addendum and exit/re-entry chronology, contact-cohort reconciliation, projections/adviser events and dated reference prices are source-review tasks under existing rules unless review exposes a genuine convention conflict. Do not automatically turn each into a new research decision.

## Choices for estimation, not blockers to ledger review

Alex explicitly asked to preserve procedural Formality and conditionality separately, then allow reinterpretation during estimation ([voice notes](../ref/alex_voice_notes_2026-08.docx), paragraphs 19–20, 47–49). A primary estimator mapping need not be chosen to finish extraction or review. The [analysis tool](tools/derive_analysis.py) computes variants and records `default: None`.

| Choice still unselected | Available interpretations | Discussion needed |
|---|---|---|
| Primary Formality reading | T0: recorded Formality; T1: Formal and not Heavy; T1u: Formal with None/Light only; T2: Formal with a single price; T3: Formal in an announced/inferred final round | Which interpretation matches the economic model? Unclear conditions are not proof of either commitment or heavy conditions. Compare alternatives as robustness checks; do not choose by best fit to two hand-coded deals. |
| Inferred exits | Treat as dropout, or retain as an uncertain/censored observation without inferring bidder value from the disappearance | A ledger convention dating an unreported departure is not evidence that a bidder chose to leave at that date. The estimator's treatment of the observation process remains to be specified. |
| Inferred counts | Use as recorded; or use as recorded with a robustness check setting aside inferred counts; or another specified treatment | Keep reported totals, arithmetic residuals and inferred exit timing distinct. Do not reopen the settled ledger arithmetic merely to discuss estimation. |

These are questionnaire §§3.2–3.3. Other code options, such as upfront versus contingent-package price and keeping same-offer rows as event observations, need an explicit analysis specification when used; their existence is not evidence of a new coding disagreement. In particular, **copied same-offer prices and blank-price commitment changes are already not new price observations under E10**. The v1.14.1 code retires the eligible-but-unadmitted, process-initiator and merger-of-equals switches; do not present them as pending choices.

## Settled decisions: implement and review, do not reopen

| Topic | Current ruling | Implementation boundary |
|---|---|---|
| Kraton rounds, 27 September | Two rounds. July 6 improvement request continues round 1; July 20 selection requests no offers; round 2 opens at the subsequent final bid letter after August 11. | Verified against Austin's explicit answer at 12:46 UTC and recorded in commit `764757f`. The saved old working copy still has three rounds (July 20 and August 11 openings); no v1.14.1 rerun exists. Alex's different three-round map opens on July 6. |
| Datalink rounds, 26 September | Four under v1.14.1, superseding F9's five; the retest opens round 1 on January 28. | Present in the raw retest, not a completed source review or working-copy migration. |
| Announcement Count, 27 September | Clear Count in the two announcement rows during review; clarify wording with the next general instruction revision, not a standalone v1.14.2 now. | Recorded in `764757f`; saved raw runs still contain the values. |
| sTec Company H, H1 | Dropped by target by May 16; reason Would not improve earlier offer. | Present in the raw v1.14.1 retest; old Q7 approval hold is obsolete. |
| Non-submitters, H2/H3 and R3 | P&W 16 inferred non-submitters; Mac-Gray 16 unnamed financial signers closed by July 23. Apply named/cohort reconciliation. | P&W retest represents 16 as Party A plus a cohort of 15; the acceptance script's demand for a single Count-16 row was too strict. Estimation interpretation remains separate. |
| Commitment-only changes, R01/H4 | Bidder commitment changes are Bid rows; without a newly stated price, price cells stay blank and create no new price observation. Target termination fees stay in dated Notes. | Current v1.14.1 treatment supersedes older recommendations to repeat the standing price. |
| Same offer and conditions, R1–R6 | Copy only when the bidder says its offer stands; evidence through its next bid, exclusivity, exit or signing includes forecasts; diligence-only duration for H2; omitted invitees exit when the next stage opens; Not begun uses the NDA test. | Published extraction defaults, subject to source review. Distinguish the case H1–H4 rulings from E12's H1–H3 condition triggers. |
| Older Q3, one-sided prices | No longer withheld; existing instruction covers the treatment. | Any remaining row defect is reviewed under the supplied instruction. |
| Meredith scope and estimation | Economic scope: LMG proposals are partial relative to pre-separation Meredith. Exclude from structural estimation; retain descriptive/reduced-form use. Alex's position reaffirmed by Austin, 27 September. | Exclusion is already in working-copy facts and analysis code; scope-dependent workbook edits await source review. See implementation details below. |

### Meredith scope: settled 27 September

**Settled:** Alex explicitly described Meredith's bids as partial; Austin confirmed in this discussion, “yes this is settled.” Use the economic scope of pre-separation Meredith (NMG plus LMG), not the residual legal shell, for this transaction-related simultaneous separation. No further approval of that principle is pending.

The [current working copy](recovery/2026-09-27-cockpit/raw/deal__meredith.json), revision 4, has 26 `Bid` rows for LMG proposals and 10 `Other-scope bid` rows for station proposals. Its Whole-company bids field explicitly calls the legal-entity treatment provisional. Its **Q7** recommends economic pre-separation scope but still carries the old request for confirmation; that request is now resolved. Q7 here is the workbook's question, not the old cross-deal Company H question.

The [filing](../raw_filing/meredith_2021-11-08_DEFM14A.htm), printed p. 59, describes simultaneous NMG separation and sale of LMG RemainCo, the Meredith legal entity then owning only LMG. Alex's [original voice notes](../ref/alex_voice_notes_2026-08.docx), body paragraphs 95, 97 and 184, identify the partial acquisition and lack of an observed market price for the acquired segment.

**Implementation of the settled principle:** use economic scope immediately before the transaction-related simultaneous separation. This does not classify a business spun off much earlier as permanently partial. The LMG proposals would be Other-scope bids relative to pre-separation Meredith; purchasing every share of the residual legal entity does not purchase both original businesses. Preserve the reported prices, terms and chronology with their scope. Under v1.14.1 D2/E1, reported amounts, units and scope belong in the Note on Other-scope bids; Price low, Price high and CVR/earnout value stay blank. Do not mechanically apply the old Q7 proposal to the new schema. Review whole-company live counts, Rounds Bids received, the auction screen and exit/re-entry rows together; partial-only parties receive no exit rows. Current Q6/Q11 exit and re-entry proposals therefore also need review.

**Already settled:** exclude Meredith from structural estimation and retain it for descriptive/reduced-form work. This is explicit in Alex's notes, the current working-copy facts and `derive_analysis.py`'s `DESCRIPTIVE_ONLY`. Do not ask for that decision again. Older recommendations refer to superseded workbooks and row numbers.

## Review and recovery work

1. Review each new run in both directions: rows against filing support, and the filing against omitted required events. Resolve real convention conflicts with Austin. Review can proceed while estimation choices remain open.
2. After that deal's review and authorization, rebase its working copy and port still-valid earlier review as an attributed revision. Do not inherit acceptance for facts changed by v1.14.1. Updating the nine `extraction/` files is a separate release action. New extractions require Austin's command.
3. The questionnaire was recovered/rebuilt and has **not been sent in the available record**. Its published-rule summaries are evidence, not a replacement decision register. Confirm its dated maps and provenance before preparing a send-ready revision; sending requires explicit authorization.
4. Review-migration registers have not been regenerated for v1.14.1. Austin dropped the stale `lesson/` input. The replacement input must preserve rulings, revision provenance and unresolved facts; do not invent a clean audit or recreate the dropped directory. The status of saved `alex_bids.csv` comparison inputs is also unresolved. See the [recovery reports](recovery/team-2026-09-27/README.md).
5. Laptop offline tools were replayed or rebuilt. The recovery report records 313 passing tests and one macOS failure requiring Linux `/proc`; this is a past recovery check, not a test run from this documentation update. The 24–26 September cockpit app source remains unreconciled on the VM. Compare the recovery branch with the VM before claiming equivalence. Snapshot exports are not a restorable database/credential backup.
6. VM reconciliation/export, a fresh backup, Alex's own-account run, remaining new-engine acceptance runs, the proposed `TMPDIR` unit changes and `dist.old` cleanup remain operational work, not research choices. Model runs and deployment remain separately authorized. The last verified VM backup in the recovered record is `20260926-193859Z`, before publication and the five retests.

## Source map

- [Snapshot index](recovery/2026-09-27-cockpit/INDEX.json) and `raw/deal__<deal>.json`: dated state, actual working-copy questions, versions and review marks.
- [Published instruction](../SEC_Deal_Ledger_Extraction_Instruction.md): current extraction conventions; no instruction changed in this documentation update.
- [Questionnaire builder](maintenance/2026-09-24-bid-terms-taxonomy/evidence/a2/build_docx.py): sections 2b and 3.1–3.5, supporting excerpts and analysis alternatives.
- [Original voice notes](../ref/alex_voice_notes_2026-08.docx): Alex's own research guidance. Paragraph numbers above count direct Word body paragraphs, including empty ones.
- [v1.14.1 retest](reviews/2026-09-26-v1141-retest/README.md), [approved specification](maintenance/2026-09-26-v1141-streamline/V1141_SPEC.md) and [recovery team record](recovery/team-2026-09-27/README.md): bounded verification and provenance. Their older status statements are historical.
- [Chronology](CHRONOLOGY.md): dated history and older decisions. The deleted handoff remains recoverable in Git before this update; do not restore it as current guidance.
