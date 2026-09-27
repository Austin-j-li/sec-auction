# Handoff: Austin's decisions after discussing the v1.14 reviews

26 September 2026. **Read this first.** This replaces the earlier root handoff in full, at Austin's request. Its old recommendations on Mac-Gray, Company H and questions for Alex are superseded by the decisions below.

## Update, 26 September 2026 (evening): v1.14.1 and the pipeline upgrade

This section is newer than everything below it. Where it conflicts with a later section, it wins; the older text is kept as history and marked where superseded.

**What was decided.**
- **v1.14.1 candidate instruction.** `_dev/maintenance/2026-09-26-v1141-streamline/SEC_Deal_Ledger_Extraction_Instruction_v1.14.1_candidate.md`, SHA-256 `8bdb7c205512c9bcf55ffa7623fba0a8bb4aabaed23c99845fa88b4a80cc8a79` as reviewed, 6,417 words (`v1.14.1_candidate.sha256` now records the edited text's hash; see the status note). It streamlines the tested v1.14 candidate (`c2d47a47…ab27`) under [V1141_SPEC](_dev/maintenance/2026-09-26-v1141-streamline/V1141_SPEC.md) and implements the four settled treatments below (H1–H4), Austin's rulings R1–R6 and D1–D6. Its text is frozen: report defects, do not edit it. *(Status, 26 September, 20:45 UTC: Austin approved eight wording fixes (PIPELINE_UPGRADE_REPORT candidate issues 2 and 4–10), applied to the candidate file, new SHA-256 `8a93df3cc6d989386958e9cb2d74ab34ebc0f07d281e8cc398605a388e066c98`; the reviewed text is kept as `checks/candidate-8bdb7c20-as-reviewed.md` in that folder, and both hashes map to the v1.14.1 rules. At Austin's order the edited text was published in the cockpit as v1.14.1 (id `08caed447f7d`), under his account, and made the default at 20:18 UTC. The repository instruction is still v1.13.2.)*
- **Pipeline decisions Q1–Q4 (Austin, 26 September),** in [PIPELINE_UPGRADE_SPEC](_dev/maintenance/2026-09-26-v1141-streamline/PIPELINE_UPGRADE_SPEC.md) §3: a `--rules v1.14|v1.14.1` selector for the checker and analysis, chosen in the cockpit from the instruction's hash (`8bdb7c20…` and, since the wording fixes, `8a93df3c…` v1.14.1; `c2d47a47…` v1.14; an unknown 29-column workbook defaults to v1.14.1; the fifteen trial workbooks keep v1.14); the process Question does not count toward the five-Question cap; D1–D6 as the candidate has them; and Mac-Gray Party B's 18 September bid becomes Contingent and Heavy (H1) under R2.
- **Engine.** Opus 5.5 at medium effort is the default extractor again (V1141_SPEC §9), reversing the same day's GPT-6-Astra-high default. Astra stays selectable and keeps high effort as its own default.

**What R1–R6 superseded** (v1.14 candidate text and the 26 September proposals):
- **R1 Same offer** replaces express incorporation (E10): only a row whose bidder says its earlier offer stands copies that row ("Same as #n"); any other revision is coded from its own communication.
- **R2 evidence window** replaces the date-level evidence rule and "a later passage establishes an earlier fact only if it expressly dates that fact": what the filing says about a bid up to that bidder's next row describes it, forecasts included.
- **R3 cohort closure** replaces the E3/E14 bounds and ranges ("never get an exact number of non-submitters by subtracting…", "giving a bound"): unnamed members of a total with no reported offer are one Did not submit row at the first due date after they appear, Count by subtraction, no range, no Question.
- **R4** limits H2 to a period tied to diligence alone ("remaining diligence the filing reports as substantive" and "even one called expedited" are gone).
- **R5** removes E14's reserve and continuing-discussion exceptions: a bidder not invited into the next stage is Dropped by target when it opens.
- **R6** makes Not begun an NDA test, not a diligence-access test.
- In the Astra packet, `AMENDMENT_SPEC.md` A1–A4 are superseded (P1 survives and is implemented in the deployed `derive_analysis.py` 0.3) and `DECISION_BRIEF_2026-09-26.md` §§1–4, §6 and §7 are resolved; both carry status notes.

**Built, deployed, pending** (status 26 September, 20:45 UTC).

| Item | State |
|---|---|
| Engine revert (WP1) | Live since the WP7 deploy (19:41 UTC): Opus 5.5 medium is the default; Astra stays selectable at high effort |
| Checker 1.8, analysis, cockpit rules plumbing, review migration, runner tooling (WP2–WP6) | Deployed at 19:41 UTC with WP7: checker 1.8, the rules selector keyed on the instruction's SHA-256 (unknown → v1.14.1), `derive_analysis.py` 0.3 (contract 0.2), `migrate_review.py` with the v1.14.1 impact tags |
| Docs and questionnaire (WP8) | Done in this checkout. The questionnaire is reconciled and rebuilt (`Questions_for_Alex_2026-09-25.docx`, now `f201a70e…243a`; the 25 September file is kept in `evidence/a2/pre-v1141/`); its 3.3(a) agreement table waited for the retest, which is now done. Not sent |
| Deploy (WP7, includes WP1) | Done at Austin's order, 19:41 UTC: `deploy-tools-v1141.patch` applied, tests 336 unit / 20 HTTP / 77 vitest, frontend rebuilt, both services restarted ([receipt](_dev/maintenance/2026-09-26-v1141-streamline/deployment-v1141.json); backup `/home/uctpiaj/backups/ledger-cockpit/20260926-193859Z`). `dist.old` is kept for rollback |
| Publish and default | Done at Austin's order, under his account, 20:18 UTC: v1.14.1 (id `08caed447f7d`, SHA-256 `8a93df3c…6c98`) published and made the cockpit default; v1.13.2 stays published |
| Five-run retest | Done: at Austin's order, five Opus 5.5 medium runs under v1.14.1 were started under his account at 20:19 UTC (Mac-Gray, P&W, sTec, Synacor, Datalink); all completed ([results](_dev/reviews/2026-09-26-v1141-retest/README.md)). Austin then decided that Datalink follows the v1.14.1 text, four rounds, superseding F9's five (the same reasoning applies to Kraton and Meredith) |
| GATEs still needing Austin | `export_repo.py instruction v1.14.1 --write` (the repository file stays v1.13.2 until then); regenerating the migration registers; rebasing working copies onto v1.14.1 runs and gate 12 (moving the nine `extraction/` workbooks); installing the unit-file (TMPDIR) changes; removing `dist.old`; commits and pushes; sending the questionnaire to Alex |

**Trial worktree.** The `sec-extraction-v114-trial-20260926` worktree was removed on 26 September. Its packet is at `_dev/reviews/2026-09-26-v114-15-run-trial/` in this checkout (296 files, hashes verified); read it as evidence, never edit it.

## Purpose and status

Austin wants a reliable extraction pipeline that captures the sale process with informed human judgment and leaves Alex only substantive research decisions. Do not turn every reasonable inference into a blocker or a new questionnaire item. Distinguish filing facts, adopted inferences and unknowns, and use the adopted inferences consistently.

**The four treatments below are settled for the next revision. They have not been implemented.** *(Superseded, 26 September evening: they are now written into the v1.14.1 text (see the update above), published and the cockpit default since 26 September; checker 1.8 and `derive_analysis.py` 0.3 apply its rules, and the five retest runs are the only workbooks made under it so far.)* This conversation inspected the filings, voice-note excerpts, candidate, questionnaire, reviews and workbook cell dumps. It did not edit instructions, analysis code, workbooks or cockpit state. The final request authorized this handoff and removal of the stale one. Only this file and the opening pointer in the development handoff were changed for that request.

Austin asked to discuss changes before proceeding to concrete work. Continue from his decisions without asking him to approve them again; discuss remaining substantive choices before implementation. This handoff is not a command to launch extractions or perform release actions.

## Settled decisions

### 1. sTec: Company H was dropped by the target

**Austin's direction:** "h should be dropped." sTec declined to advance H because its price was too low. H's continued interest does not keep it an active competitor when the target does not want its offer.

The filing sequence (pp. 29-30):

- May 15: H offered $5.00-$5.75 per share.
- The target told H its price was insufficient to advance, while allowing it to submit an improved offer.
- May 16: final-round letters went to WDC and Company D.
- May 23: H said it remained interested but could not raise its price.
- Before signing, the board considered H's potential to make a superior offer remote because it repeatedly could not improve (p. 34). This does not establish continued active negotiation.

**Adopt target-side rejection (Dropped by target), preserving the inadequate price and inability to improve in the account.** A conditional willingness to reconsider a better offer is not, by itself, enough to keep the rejected bidder live. The exact rejection date was not settled as a calendar day; derive the supported window and use the existing exit-reason vocabulary when implementing.

The agent initially over-weighted "remained interested" and recommended keeping H available until signing. That recommendation is withdrawn. Anonymity is not an independent reason: Company D was also anonymized and advanced.

Reconcile candidate E3/E14, Rounds and questionnaire section 3.4/C18. Any instruction repair must express the general distinction between actual continuation and an invitation to return with a better offer, rather than a Company H exception. Do not leave this case's substantive treatment pending or revive the old Q7 withholding status.

### 2. Providence: sixteen inferred first-round non-submitters

**Austin explicitly approved:** use the ordinary population reading: **25 NDA signers minus nine first-round bidders equals 16 non-submitters**, with inferred disappearance, unknown reason and no double-counting of later mentions.

The working assumption is that the nine first-round bidders belong to the 25 signers. State it briefly; do not present individual membership or departure as directly reported. Later contacts and receipt of a memorandum do not create additional entrants. Preserve genuinely new entrants, such as Party C, separately.

Alex's voice notes support the approach, with these attribution limits:

- Providence items 4-5 warn against duplicated contacts/NDAs and say participation counts should be constructed from the underlying events.
- Providence item 11 infers that Party A did not get beyond round one from its disappearance, explicitly calling this low-confidence but useful. This discussion did not assign Party A to a specific anonymous exit row.
- PetSmart item 5 gives a direct parallel: fifteen NDA signers, six offers, nine non-submitters, with the reason unknown.
- Alex did **not** explicitly prescribe the Providence 25-minus-nine subtraction in that section. Austin approved this application of his approach.

**Use Did not submit, Count 16, inferred, Exit reason Not stated, with the population assumption disclosed.** The filing expressly reports invitations to submit (p. 29). Withdraw PW2's earlier "confirmed overstatement" verdict. The earlier 16-24 alternative is not the required main coding under Austin's decision.

No exact Providence exit day was chosen in this discussion. Reconcile its bounds with the initial solicitation: May 10 was superseded by May 19, and offers were received through June 1.

### 3. Mac-Gray: July 23 is permitted as the inferred closure date

**Austin explicitly permitted:** record **16 inferred non-submitters assigned July 23**, with unknown reason and a short note that individual signing/departure dates are unavailable.

The accounting is twenty CA signers: two strategic and eighteen financial. Financial Parties B and C submitted offers, leaving sixteen unnamed financial signers with no reported offers. The filing aggregates signing "over the next two months" after June 24, across the July 23 deadline. Party A is a known August 5 signer, but it is strategic and outside these sixteen. We have no affirmative evidence that any of the sixteen signed late.

The adopted reconstruction assumes the unnamed residual belongs to the initial solicitation and uses its deadline to assign closure. **Use Did not submit, Count 16, Inferred Y, Exit reason Not stated, and July 23 as the assigned date, with the inference disclosed.** Do not call this a directly observed voluntary withdrawal or say they were unable to bid. Their actual departure dates remain unknown.

**Correction to the earlier review:** withdraw MG1's categorical "confirmed error" treatment of the July 23 inference. The agent was too rigid in treating a debatable coding convention as a demonstrated factual error. The previous handoff's instruction to retain that criticism is superseded; its preferred August 27 closure is no longer the required main treatment for this cohort.

Claude had already adopted substantially this approach:

| Trial output | Existing treatment |
|---|---|
| Opus 5.5 medium, Mac-Gray B #24 | Did not submit by July 23, Inferred Y, reason Not stated; Count blank with "16 closed" and "up to 16" qualifications; Rounds closes the sixteen. |
| Opus 5.5 xhigh, Mac-Gray E #23 | Did not submit by July 23, Count 16, Inferred Y, reason Not stated; missing signing dates disclosed. Closest to Austin's approved treatment. |
| Fable's subsequent review | Defended the July 23 inference, especially medium's qualified version; its revised grading still penalized xhigh's exact count under the tested wording. |

The next revision should permit the adopted inference in general terms and align the population, dates, Notes and Rounds. Existing D10 still applies: a bidder actually shown continuing after a missed deadline is not exited. Do not apply anonymous-residual closure to such a bidder.

Reconsider the earlier criticism accordingly. Preserve original trial outputs and historical review scores; do not silently rewrite grading or infer a new universal model ranking.

### 4. Commitment changes: preserve events without manufacturing new price quotations

**Austin agreed:** this does not need another question for Alex.

Mac-Gray's buyer offered $21.25 per share on September 21. October 5 and October 8 negotiations concerned the sponsor's liability if the buyer failed to complete, including a proposed $50 million cap. These are material changes around the standing offer; those communications do not newly quote the purchase price.

**Keep the commitment changes as ledger events under the existing Bid-row convention (R01/D13), retain their connection to the standing $21.25 offer, and do not count them as additional newly quoted prices.** A blank price on a communication's row does not mean the standing price vanished. It can remain context without being presented as a fresh quotation.

The analysis defect is concrete: Mac-Gray A #61/#62 have blank upfront prices while both price_obs__same_price_as_new and price_obs__same_price_as_terms are 1. Fix that event-versus-price distinction in the analysis contract/tool when implementing. Preserve the events; do not fill prices merely to satisfy a numeric flag or add an extraction column simply to solve the downstream problem.

Specific API fields and the older P1 proposal's full implementation detail were not separately reviewed here. Keep implementation proportionate to the approved behavior. Actual price revisions and express reaffirmations still follow their existing rules; this decision concerns the non-price commitment changes discussed here.

Reconcile amendment A4/P1, analysis contract sections 6/8 and questionnaire section 3.3(b)/C6. Stop presenting these October liability negotiations as an unresolved question for Alex about fresh price observations.

## What remains to do

*(26 September evening: the reconciliations below are done or overtaken. V1141_SPEC replaces the amendment spec, the questionnaire and research questions are reconciled, and `lesson/` was not touched. See the update above.)*

These decisions supersede contrary recommendations in the following unchanged documents:

- [Earlier amendment spec](_dev/maintenance/2026-09-26-astra-default-pro-verification/AMENDMENT_SPEC.md): revise A2 to permit the adopted inferences, reconcile Company H, and simplify A4/P1 around the approved behavior. A1 (dated status facts) and A3 (diligence duration) were not approved in this discussion.
- [Earlier source verification](_dev/maintenance/2026-09-26-astra-default-pro-verification/PRO_FINDINGS_VERIFICATION.md): MG1 and PW2 are superseded as described above; related population/closure recommendations must be read accordingly. Its other findings were not all adjudicated here.
- [25 September questionnaire](_dev/maintenance/2026-09-24-bid-terms-taxonomy/Questions_for_Alex_2026-09-25.docx): reconcile sections 3.2, 3.3(b)-(c), 3.4 and their examples; preserve numbering and the crosswalk to D1-D27. Do not send anything to Alex.
- [Research questions](_dev/RESEARCH_QUESTIONS.md) and [older deal questions](lesson/alex-questions.md): historical row references and "pending" labels do not override these decisions or establish current workbook cells.

**On resumption:** explain any remaining substantive changes plainly before implementing. A coherent next proposal should incorporate the four settled treatments and identify what actually remains open. Keep the taxonomy and four-sheet, 29-column extraction format. General instruction edits must be consistent across Part A, E3/E10/E14, examples, Rounds and analysis definitions.

Unrelated pending work remains: the primary analytical Formality reading and treatment of Unclear; upfront versus contingent-package price; provisional financing, scope, round and deadline conventions; and remaining deal-specific maps. This discussion did not choose an estimation model for all inferred exits, all uncertain populations or all express reaffirmations. Do not use broader questions to reopen the case treatments above. Datalink's five-round F9 ruling and Meredith's exclusion from structural estimation remain settled. *(26 September evening: Austin superseded F9; Datalink follows the v1.14.1 text, four rounds. Meredith's exclusion stands.)* External market-price history is a separate task.

## Operational continuity

The engine choice remains **GPT-6-Astra high**. Austin did not reverse it here. *(Superseded later on 26 September: Opus 5.5 medium is the default again, live since the 19:41 UTC deploy. See the update above.)* The recorded earlier state was v1.13.2 published/default, the v1.14 candidate unpublished and its upgrade undeployed, with the isolated fifteen-run comparison completed. Live service/job/database state was not rechecked for this handoff; use [the development handoff](_dev/HANDOFF.md) for dated operational history and verify it before operational action.

File hashes checked while replacing this handoff:

| File | SHA-256 |
|---|---|
| Frozen root instruction, v1.13.2 | 513c8e3e8159e4a6bceccd6ffca32a246302736329a0c7137b64dd3b7ffcd304 |
| Tested v1.14 candidate | c2d47a479d09eb46d0ab9fbf887568fcf13e972e2e11acbf08d5cdfab468ab27 |
| 25 September questionnaire | 64ddad6cdb5935a62510157c42dd7e31bd5356f3dfd091a6307436ef6a3b4353 |

These files remain unchanged. Approved decisions are not yet reflected in their contents. *(Later on 26 September the questionnaire was reconciled and rebuilt: its SHA-256 is now `f201a70ef900b952b3c0e501375ce8552e0b938ea9869f0b28a48c3519f0243a`; the file with the hash above is kept as `_dev/maintenance/2026-09-24-bid-terms-taxonomy/evidence/a2/pre-v1141/Questions_for_Alex_2026-09-25-pre-v1141.docx`. The v1.14.1 candidate was `8bdb7c20…8a79` as reviewed, and is `8a93df3c…6c98` after the approved wording fixes, the text published as v1.14.1.)*

| Checkout | Role |
|---|---|
| /home/uctpiaj/work/Projects/sec-extraction | Live main checkout; preserve its existing uncommitted work and cockpit state. Services run its code. |
| /home/uctpiaj/work/Projects/sec-extraction-v114 | Upgrade implementation, deployed to the main checkout on 26 September (WP7); use it, or another separate worktree, for subsequent code changes, not live _dev/tools/. |
| _dev/reviews/2026-09-26-v114-15-run-trial/ (main checkout) | Preserved comparison inputs, outputs and reviews. Moved from the removed `sec-extraction-v114-trial-20260926` worktree on 26 September; 296 files, hashes verified. |

No extraction, workbook correction/rebase, publication, deployment, commit or push was performed or newly commanded by the handoff-writing request. No team mode or external consultation was requested. Do not automatically rerun the trial, change the engine default, merge entire dirty trees or apply old deployment patches without reconciling them with the already implemented Astra-default change.

## Evidence

- [V114_SPEC and D1-D27](_dev/maintenance/2026-09-24-bid-terms-taxonomy/V114_SPEC.md), [tested candidate](_dev/maintenance/2026-09-24-bid-terms-taxonomy/SEC_Deal_Ledger_Extraction_Instruction_v1.14_candidate.md), [map re-check](_dev/maintenance/2026-09-24-bid-terms-taxonomy/MAP_RECHECK.md) and [analysis contract](_dev/maintenance/2026-09-24-bid-terms-taxonomy/ANALYSIS_CONTRACT.md). Prior decisions remain applicable except where this discussion supersedes them.
- [Numbered Alex voice notes](_dev/maintenance/2026-09-26-astra-default-pro-verification/evidence/alex-voice-paragraphs.txt): Providence paragraphs 12-24; Mac-Gray 41-45; PetSmart 60; sTec 121-125. Paragraph 129 onward is Claude's interpretation, not Alex's speech. Alex's statement about dropping bidders on May 16 is not an explicit Company H adjudication.
- Filing text: [sTec](_dev/maintenance/2026-09-26-astra-default-pro-verification/evidence/stec_2013-08-08_DEFM14A.txt), [Providence](_dev/maintenance/2026-09-26-astra-default-pro-verification/evidence/providence-worcester_2016-09-20_DEFM14A.txt), [Mac-Gray](_dev/maintenance/2026-09-26-astra-default-pro-verification/evidence/mac-gray_2013-12-04_DEFM14A.txt). Relevant printed pages: sTec 29-30/34; Providence 28-29; Mac-Gray 32-35/39.
- [Workbook cell dumps](_dev/maintenance/2026-09-26-astra-default-pro-verification/evidence/workbook-cells.json). Letters are deal-specific; # identifies the event, not the Excel row.
- [Fable's unblinded comparison](/home/uctpiaj/work/Projects/sec-extraction/_dev/reviews/2026-09-26-v114-15-run-trial/grading/02_unblinded_comparison.md), particularly sections 4 and 6; [blind findings](/home/uctpiaj/work/Projects/sec-extraction/_dev/reviews/2026-09-26-v114-15-run-trial/grading/01_blind_findings.md); [Pro report](/home/uctpiaj/work/Projects/sec-extraction/_dev/reviews/2026-09-26-v114-15-run-trial/pro-review/SEC_Anonymous_Extraction_Review.pdf). These are historical evaluations, not authority to override Austin's decisions here.

## Suggested continuation

> Read the root HANDOFF.md. Treat Austin's Company H rejection, Providence sixteen-non-submitter reconstruction, Mac-Gray July 23 inferred closure, and treatment of non-price commitment changes as settled. Do not repeat the old claim that Claude's July 23 inference was a confirmed factual error. Discuss remaining substantive changes in plain language before implementing; preserve source evidence and distinguish approved decisions from changes actually made.
