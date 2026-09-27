# Lane C: VM decisions (23–26 Sep) against the laptop alignment sprint (27 Sep)

Read-only comparison. "VM" = snapshot at `scratchpad/vm/vm-tree` ($S). "Today" = `_dev/alignment_sprint/DECISIONS.md` (DEC), `DRAFTING_SPEC.md` (DS), `_dev/STATUS.md` (ST). Every today item is later (27 Sep) than every VM item (21–26 Sep). v0 is byte-for-byte the v1.14.1 text except the title (checked: v0 still has "A selection that asks for no offers opens no round", "commitment letter", "diligence alone", "Record reported exits first", the issue-8 price sentence and the issue-7 Initiation wording), so every VM ruling written into v1.14.1 survives into the draft unless a sprint decision changes it.

## Verdict

1. Compatible as a successor: DS starts from the exact VM-approved text (v1.14.1 = v0), so everything the VM settled in the text carries forward unless a sprint decision changes it; most changes rest on Alex's words and legitimately override under the working rule.
2. But DEC's working-rule line ("only the same-offer rule contradicted Alex") was checked only against ST's settled list, not the VM's 25–26 Sep rulings. At least eleven further VM rulings are overturned without being named (list 2, items C3–C13), and several changes rest on fresh Austin calls rather than Alex's words: F3, R7(b), R6 applied to rounds and the Synacor Dec 30 round. Route 2 in a final round (DS §4.8) rests on Alex's CI p.9 with no Austin ruling, and it reverses a v0 sentence.
3. Must add before drafting: (a) a change-map section that names each overturned VM ruling (R4, D3, V114 D14, V1141 D1/V114 D9, V114 D12, the V1141 Initiation cut, candidate issue 2, D8's Synacor option A, D11's Enforced, the VM Kraton map in which J never exits, the Party E acceptance cell); (b) the VM retest acceptance list as regression anchors in DS §7/§9, marking which cells change on purpose; (c) a deploy note: VM checker 1.8 checks any unknown instruction hash as v1.14.1, so the new version must not be published in the cockpit before its checker is deployed there.
4. Also add: a ruling or explicit deferral for the two VM open issues nobody decided (the process Question firing on defaults; Formality/Conditions on Other-scope bid rows, which is every Meredith bid), and a statement in ROUND_MAP of where Synacor's reopened round opens (Oct 27, Dec 30 or both) and which arm of (d) fires.
5. Alex list: DEC says "None open" while ST still lists open items, and the VM's source-hierarchy question, Penford Party A reading and exit-reason merge were dropped without a decision; DS §10 closes the list at approval, so record them as dropped or deferred rather than let them vanish.

## 1. AGREE

- **Settled case treatments.** Company H Dropped by target by May 16, reason Would not improve earlier offer; P&W 16 non-submitters (Party A + cohort of 15); Mac-Gray 16 unnamed signers Did not submit by July 23; commitment-only changes are blank-price Bid rows, target fee in a Note. VM: root HANDOFF §§1–4 (H1–H4), V1141_SPEC §3. Today: ST "Settled rulings".
- **Not invited means dropped at the stage opening, whatever the bidder was told.** VM: V1141 R5, E14 inferred exit 1. Today: P3, and the "Stage questions" ruling (Datalink "still considering" parties dropped, Re-entered if they return) in DEC.
- **Cohort closure and named-party overlap.** VM: V1141 R3, E3 Cohorts. Today: P1 and P2 refine it and ST keeps the P&W/Mac-Gray counts; the direction is the same.
- **Evidence window with forecasts (R2), Not begun as an NDA test (R6), memorandum not diligence access.** VM: V1141 §3 R2/R6; DECISION_BRIEF §7 resolved by R6. Today: ST "Same offer and conditions" (window, forecasts, NDA test); P4 ("Sending a memorandum ... never creates an NDA signed row").
- **Conditions on proceeding are a Bid with H3 and a blank price.** VM: V1141 D2, E10. Today: F7 keeps it and adds that routine legal bargaining is not a Bid.
- **Trigger (d): a 30-day pause or an ended exclusivity.** VM: V1141 D6. Today: R3 keeps it and adds a guard; Datalink Oct 1 stays a round in both.
- **Whole-company scope.** Partial bidders are outside counts and exits. VM: V114 D7, D18 (Other-scope price cells blank). Today: R6 extends this to rounds and to the sale decision; ST's Meredith ruling (price cells blank, amounts in the Note, descriptive only). Meredith is excluded from structural estimation in both (VM root HANDOFF "What remains"; ST).
- **Count on announcement and signing rows.** VM retest README "Checker findings": candidate v1.14.2 wording, blank Count on announcement rows. VM candidate issue 5: Count filled on Process terminated/restarted/Bidding group changed. Today: O3 adopts both and adds Count 1 on Merger agreement signed. Today resolves the VM's pending v1.14.2 item.
- **Inferred Round opened.** VM: candidate issue 4 (approved). Today: R7(a), which adds Date from and the "by [first offer]" form.
- **Five Questions, with the process Question outside the cap.** VM: V1141 D4; PIPELINE_UPGRADE_SPEC §3 Q2. Today: DS §6 "Review items" row (the cap counts Q ids only).
- **Engine and writing.** Both use Opus 5.5 at medium as the default extractor and follow Anthropic's prompting guidance: no emphasis, reasons kept, one home per rule, synthetic examples in tags, no thinking-steering. VM: V1141 §2, §9. Today: DS §5; AGENTS.md.
- **Deferred to estimation or tooling.** Market data (VM V114 D23 = today O5); analysis choices kept as switches with no default (VM V114 D22 = ST "Choices for estimation"); filing link added by the pipeline, not the model (VM V114 D20 ≈ today O7 deferred).
- **Finality by what the target did, not its label.** VM: V114 D8, E6 ("Infer rounds from what the target does, not from ... vocabulary"). Today: R4 "substance over label". The principle agrees; the sTec outcome conflicts (C8).
- **Financing without a firm commitment is Contingent.** VM: V1141 E12 Financing ("a source named without a commitment"). Today: F6 restates it.
- **Adviser rows are target-side.** VM: V1141 Part D Adviser. Today: P7 refines it (dating, renamed banks, shareholders' advisers go in Notes).

## 2. CONFLICT

Format: VM → Today · basis of today's rule · concrete effect. Today is later in every case.

**C1. Same offer vs confirmation by documents (known conflict (a)).**
- VM: copy an offer only when the bidder says it stands (V1141 R1; E10 Same offer; root HANDOFF "What R1–R6 superseded"; ST settled "Same offer and conditions"). A revision is otherwise coded from its own communication.
- Today: F2 (DEC "F2"). After definitive negotiation begins, a bidder's own revised markup or draft with no new price is a Bid reaffirmed row that copies its latest price ("Same as #n"), one per bidder unless terms change. DS §4.10 carves out drafts that also state a change or a condition.
- Basis: Alex's V¶30. DEC records it as the one known override; ST must be updated at approval (DS §10).
- Effect: Providence Party B gets an Aug 4 Bid reaffirmed at $24, Formal, not None. Penford Ingredion gets an Oct 8 Bid reaffirmed at $19, Formal, so Formality arrives six days before Alex's own Oct 14 date (V¶74). Most winners gain one row. Analysis: F2 rows begin "Same as #n", so the VM's `same_offer_of` switch and the issue-8 sentence ("the price a Same-offer row copies is not a new price observation") must be extended to cover them.

**C2. Round maps: F9, "same reasoning", Kraton, Datalink, Meredith (known conflict (b)).**
- What F9 was: Austin's 21 Sep Datalink ruling (RESEARCH_QUESTIONS "Datalink F9"; CHRONOLOGY 21 Sep). January's bilateral stage with Party A is round 1 (Jan 29, inferred) and June's broad outreach is round 2, five rounds in all (Jan 29 / Jun 6 / Jul 27 / Aug 16 / Oct 1).
- 26 Sep supersession (`_dev/HANDOFF.md` update; PIPELINE_UPGRADE_REPORT candidate issue 1): follow the v1.14.1 text. That gives four rounds: Jan 28 (first price negotiation, since buyers came to the target), Jun 6 (d), Aug 16 (b; the offer-less Jul 27 selection opens nothing under the approved issue-2 sentence), Oct 1 (d).
- What "same reasoning" meant (MAP_RECHECK "For Decision 1"; a2 README "Datalink (3.1)"): apply the text's offer-less-selection rule rather than case rulings. Kraton gets two rounds, with Jul 6 inside round 1 and the Jul 20 admission plus the Aug 11 letter as one round. Meredith's Dec 21 admission and Jan 12 final letter become one round.
- Today, Kraton: three rounds. R1 May 24; R2 Jul 6 (trigger (a), under R1); R3 Jul 20 (selection decision, under R2), made final by the Aug 11 letter. Sources: ST "Kraton rounds (27 Sep 13:48 UTC)", DS §7, DEC R1/R2. Basis: Alex (V¶82, V¶173). Effect: one more informal round. Party J is dropped Jul 6, Re-entered Jul 19 and dropped Jul 20 (VM: J missed Jun 29, continued, no exit under D10). Party I is dropped Jul 20.
- Today, Datalink: still four rounds, but a different map: R1 Jun 1 or the outreach date (R5; DS §7 says "derive whether the outreach followed within a week"), R2 Jul 27 (R2), R3 Aug 16 (DS §4.3), R4 Oct 1. Basis: Alex's R5 (V¶71, V¶173; Alex's own reading puts round 1 at the bank's first contact, MAP_RECHECK Datalink) and R2 (V¶44). Effect: Jan–May becomes round 0, so Party A's January–April proposals leave round 1. Round 1 moves from Jan 28 to June (Jun 1 or the outreach date; the VM had Jun 6 as round 2), and Jul 27 now opens a round. The two admitted parties without Aug 16 letters drop at Aug 16 under both maps. Same count, different bids per round.
- Today, Meredith: no whole-company rounds at all (DS §7; DS §4.12; R6). Basis: ST's economic-scope ruling, which the laptop records as settled. The VM treated Meredith coding as still "pending" (RESEARCH_QUESTIONS "Meredith workbook coding is pending"), and the 22 Sep RECOMMENDATIONS proposed it. Effect: the Rounds sheet is empty and Whole-company bids is No. There is no structural effect, since Meredith is descriptive-only in both.
- Verdict: today's round rule (a selection opens the stage) reverses the VM's approved issue-2 sentence. VM's "same reasoning" is fully overturned for Kraton (Alex), changed in substance for Datalink (Alex), and made moot for Meredith (scope).

**C3. H2 and bundled diligence periods.**
- VM: R4 (V1141 §3), a period counts toward H2 only if tied to diligence alone. Example 4 ("45 days' exclusivity ... to complete due diligence and negotiate") is not H2 and gives Conditions Unclear. PRO_FINDINGS PW4 called Party E's H2 a "confirmed error", and the retest acceptance says "P&W: Party E not H2" (retest README; V1141 §10 step 6).
- Today: F4. Two weeks or more tied to diligence "alone or together with negotiation or exclusivity" is H2, and Example 4 becomes Heavy.
- Basis: Alex V¶19.
- Effect: P&W Party E (60 days of exclusivity for diligence and documents) becomes Heavy H2, reversing a VM acceptance cell. Any exclusivity-plus-diligence bid moves to Heavy, which lowers Formal-and-not-Heavy counts (T1/T1u).

**C4. Committed financing with silent diligence, and silence on Formal bids.**
- VM: D3(a) (V1141 §6, approved as Q3 in PIPELINE_UPGRADE_SPEC §3): committed financing with silent diligence is Unclear, the second Light route is removed, and a negative value needs the filing's words (E12).
- Today: F5. For a Formal bid, silence is None when each column meets None or is Not stated and exclusivity is not Required (DS §4.6).
- Basis: Alex V¶125, V¶183.
- Effect: sTec WDC May 28 becomes None. Formal final-round bids with silent diligence move from Unclear to None or Light; the VM retest shows CSC/Pamplona Sep 18/21 fell to Unclear under D3. Informal silent bids stay Unclear. The questionnaire's 3.3(a) T1u numbers change again.

**C5. Exclusivity and the Conditions level.**
- VM: V114 D14 (Final): exclusivity never changes Formality or the Conditions level. Part A says "exclusivity and contingent payments change neither".
- Today: F5. Required exclusivity makes Conditions at least Light, and A.3 is rewritten (DS §4.7).
- Basis: Alex V¶19 (with V¶49 kept for Formality).
- Effect: a bid with Exclusivity Required can no longer be None.

**C6. Price-only revision after a Formal bid, and the reach of route 3.**
- VM: V1141 D1(a) and V114 D9 (a revision must meet a route itself); spec §6 warned that "(b) would label oral price bumps Formal". Route 3 covered Bid reaffirmed only.
- Today: F3 (Formality persists while the bidder's markup is on the table), and R4 negotiation formality (any bid after definitive negotiation begins is Formal).
- Basis: F3 is an Austin call for Alex; route 3 rests on V¶27.
- Effect: Providence G&W Jul 26 $22.15 goes from Informal to Formal, which matches Alex's coding and fixes a retest disagreement. Phoned-in bumps after negotiation begins become Formal: exactly the outcome the VM rejected.

**C7. Round-opening rule (triggers (a) and selection).**
- VM: E6 (a) requires "selects which bidders advance and asks them for new offers". Repeated improvement requests continue the round. The approved issue-2 sentence says a selection that asks for no offers opens no round.
- Today: R1 (a common request to some but not all eligible parties opens a round, counting never-bidding NDA signers as eligible) and R2 (a documented decision admitting parties opens the stage).
- Basis: Alex V¶82, V¶173, V¶44.
- Effect: Kraton gains Jul 6 (C2). Mac-Gray round 2 moves from the Aug 27 letter (v1.14.1 text) back to Jul 25; the VM's recommended map was already Jul 25 (MAP_RECHECK Mac-Gray §5), so today restores the VM's intent. Providence round 2 opens by Jun 1. PetSmart's final round opens Nov 3. DEC R1 accepts that improvement requests which leave out never-bidding signers open rounds.

**C8. sTec rounds and processes.**
- VM: MAP_RECHECK sTec Map A, recommended. The May 16 "final round process letters" make round 2 Announced as final; May 29 stays inside it; one process under E5; no round 3. The retest acceptance says "sTec ... two rounds".
- Today: R4 finality. May 16 opens round 2, Not final ("non-binding proposals"). May 29 "best and final" opens round 3, final. R8 gives 2 processes (91 days, Nov 14 to Feb 13). Sources: DEC R4, R8; DS §7.
- Basis: Austin for Alex; matches V¶118, V¶124–125 (Alex's Map C).
- Effect: round 2 bids lose route 2, WDC May 28 stays Formal by its markup, and process 1 is added. This reverses a VM acceptance cell.

**C9. Deadline outcome "Enforced".**
- VM: V114 D11 and V1141 E9: Enforced when the target "acted on the bids in hand (evaluated, selected or gave feedback)".
- Today: R9. Enforced needs a decisive action (select, exclude, open a stage, choose a bidder). Board review or price feedback alone is Passed without action.
- Basis: Alex V¶122–124.
- Effect: probably nothing in the nine deals. Every Enforced the VM recorded (Mac-Gray Sep 18, PetSmart Oct 30, Kraton Jul 19, sTec May 30, Synacor Sep 17, 2020) is followed by a selection or exclusivity. sTec May 3 was already Extended (late bid accepted) on the VM. The change bites on new deals where only review or feedback follows a due date.

**C10. Mandatory review flags.**
- VM: V114 D12 (Final): Alex's A–M flag list is not mandatory. V1141 §1 goal 2: applying a default never triggers a Question, range, extra row or long Note.
- Today: O1. Uncapped mandatory Review items (R ids) are added beside the five Questions, and "Applying a default ... may be a Review item".
- Basis: Alex V¶169–187.
- Effect: every workbook gains R rows, the checker and Questions sheet change (DS §6), and there is more output per run.

**C11. Initiation.**
- VM: V1141 Part D D5 dropped "mixed or unclear". Any Activist row before round 1 makes the deal activist-influenced (issue 7 added Round opened as target-led).
- Today: P5. Activist-influenced only when a "Demands sale" Activist row precedes the first target sale step; "mixed" is restored.
- Basis: V¶119, V¶39, CI p.5.
- Effect: sTec (Balch Hill "Sale one option") is not activist-influenced; Mac-Gray is mixed. `derive_analysis` initiation must change.

**C12. Round 1 date.**
- VM: E6, where buyers came to the target, round 1 opens at the first NDA or price negotiation. Candidate issue 3 was left open ("no wording was proposed").
- Today: R5 plus the PetSmart ruling and DS §4.1. The "never contacts beyond" clause applies; an undated outreach is dated at the board meeting before the first NDAs.
- Basis: Alex V¶71, V¶173, V¶55.
- Effect: Datalink R1 moves from Jan 28 to Jun 1, PetSmart R1 is Oct 3, and Penford's Aug 10 $18 goes to round 0. This resolves VM issue 3, but differently from the retest run.

**C13. Synacor Dec 30, 2020.**
- VM: V114 D8 adopted option A (Oct 27 reopening), "not B (30 December)"; Dec 30 is a step inside round 3 (MAP_RECHECK Synacor §2). The retest: "3 processes, 6 rounds, as recorded".
- Today: DEC "Stage questions": "Synacor: an added round from Dec 30, 2020"; R3 says v0 (d) already fires (ADOPT_NEXT). DS §7 marks it "derive".
- Basis: a fresh Austin call ("restart after exclusivity lapses"), with no Alex source; V¶109 is about processes. There was "further outreach" to CLP, G and H on Dec 18–21, so no 30-day pause ends on Dec 30. If (d) fires there, it is the exclusivity arm with Oct 27 read as outreach rather than a request for offers. That most likely moves the reopened round from Oct 27 to Dec 30 (D8's rejected option B) rather than adding one, though DEC and DS ("derive") do not say which.
- Effect: D8 is reversed either way. ROUND_MAP must state whether Oct 27 survives and which arm of (d) fires.

**C14. Formality route 1: commitment letters and timing.**
- VM: V1141 §5 kept "a commitment letter or a voting agreement" in route 1, "preserving Mac-Gray's 5 October coding"; a markup "with a priced proposal or in support of one".
- Today: F9 (a commitment letter alone is not Formal) and F1 (the documents must come in the same communication, or answer a request for both).
- Basis: F9 rests on V¶47; F1 is Austin for Alex (V¶74).
- Effect: Penford Ingredion Aug 10, Sep 17 and Oct 2 stay Informal. Mac-Gray Oct 5 loses route 1 but is Formal by broadened route 3 (exclusivity executed Sep 24), so the label likely holds.

**C15. Route 2 inside a final round.**
- VM: E11, "an unsolicited bid during a final round carries that round's number but not route 2". The solicited case was left open (PIPELINE_UPGRADE_SPEC §7).
- Today: DS §4.8. Every bid by an invited bidder during a final round is route 2, including unrequested revisions.
- Basis: CI p.9, applied by the drafter. Austin did not rule; DS flags it.
- Effect: this reverses a v0 sentence, not just a gap. Late or unrequested final-round bids (e.g. sTec WDC Jun 10/14 under a final round) could become Formal unless DS §4.9's re-entry lapse applies.

**C16. NDA dating.**
- VM: E7, "If the filing dates only the sending of the agreement or of information, When is 'by [that date]'" (an upper bound).
- Today: P4. An agreement sent but not signed gets no row. Where execution is reported but undated, the sending date is a lower bound. Information sent is an upper bound only where signing came first.
- Basis: V¶12, CI p.6.
- Effect: NDA When cells change direction on those rows.

**C17. Closing order in E14.**
- VM: "Record reported exits first".
- Today: P3, "Close each participation at the earliest supported closing event, reported or inferred."
- Basis: this follows the VM's own Company H ruling.
- Effect: a later reported withdrawal no longer displaces an earlier inferred drop. It agrees with H1 in substance.

**C18. Tooling: the rules selector.**
- VM: PIPELINE_UPGRADE_SPEC §3 Q1. `--rules`, and a hash map where an unknown 29-column workbook defaults to v1.14.1.
- Today: the v0 reset removed `--rules` and the compatibility branches (ST "Operational"). DS §6 "Version": "no compatibility branch".
- Basis: an Austin reset.
- Effect: see must-add (c). On the VM, a new-version workbook would be checked under v1.14.1 rules and fail on R ids, `mixed`, and Count on signing.

## 3. VM-SETTLED, TODAY SILENT (preserve or decide)

Base text (v1.14.1 = v0) already carries these; the drafter must not drop them while rewriting:
- **D10:** a missed due date without departure is not an exit (E14). Today's R1 and R2 change Kraton J through selection, not through D10. Keep D10 for continuing bidders.
- **V1141 D5:** nine exit reasons kept, and the merge into seven "revisit with Alex". Silent today; the Alex question was dropped.
- **V114 D5 financing precedence:** "not subject to a financing condition" outranks unsigned or highly-confident debt (E12 Committed). F6 must not override it. F6 applies where the filing says financing is not firm.
- **Candidate issue 8:** a copied price is not a new price observation. Extend it to F2 rows (C1).
- **Candidate issues 6 and 9:** "only documentation remains" is Incomplete and Light; for a CVR, use the maximum and list the rest in the Note. F10 must keep them.
- **V114 D15/D27:** a later exclusivity request alone is an Exclusivity changed row; alternatives in one communication are separate rows; a package that cannot be split leaves price cells blank.
- **V114 D17 / V1141 E1:** the merger-of-equals counterparty is outside the contest, with the talks as Other material event rows. R8 uses this for the process gap only; keep E1.

Pending on the VM, still undecided today:
- **Process Question fires on outcomes the defaults decide** (PIPELINE_UPGRADE_SPEC §7; CHANGELOG "Open points"). Today does not address it. O1 adds a related Review item but keeps the process Question. Decide or defer explicitly.
- **Other-scope bid rows still need Formality and Conditions** under F's delivery check. Not addressed. Every Meredith bid is Other-scope, and R6 makes that more common.
- **Price-only revisions lose earlier conditions** (Not stated, so Unclear). F5 now fixes Formal bids only. Informal price bumps still go Unclear.
- **Retest checker warnings not addressed:** Questions over 60 words in every deal (DS §5 keeps the cap and O1 adds uncapped R items); Datalink row 71 Exclusivity changed repeating bid row 69; sTec row 19 one-sided price wording.

Operational VM state and GATEs the spec does not sequence (VM `_dev/HANDOFF.md` "Still GATEs"; root HANDOFF table):
- The published cockpit default is v1.14.1 (`08caed447f7d`), with checker 1.8 and derive 0.3 live. The export to the repository was never run, the migration registers (need `lesson/`) were never regenerated, and the unit-file TMPDIR change and `dist.old` removal are pending.
- **V114 D24/D25:** eight edited working copies hold reviewed row marks (454 reviewed / 66 needs decision) and the Mac-Gray R01 finding decision. The rule was to rebase deal by deal and port the review as one attributed revision. Today plans a fresh re-extraction and comparison with Alex. Record what happens to that review work.
- **VM derive 0.3 features:** P1 `upfront_price_kind`, `same_offer_of`, `same_offer_restatements`, `initiation_check`. All four names appear in the laptop `derive_analysis.py`. DS §6 must extend them to F2 and `mixed`.
- **The questionnaire** (`Questions_for_Alex_2026-09-25.docx`, `76b9c635…`) was built and never sent. ST says the laptop copy was deleted; the VM copy survives.

## 4. TODAY-SETTLED, VM SILENT

These are new rules with no VM counterpart:
- R3 guard: carrying out a stage is not asking again.
- R7(b): a late answer carries the round that is open when it arrives.
- R7(c): same-day order.
- R9: "last late response" date in How it ended.
- F10: CVR with an unstated date.
- F11: a retrospective label.
- F12: the target's preference between alternatives.
- P2: re-contact subtraction.
- P6: type split by arithmetic.
- P8: bounds from linked events.
- P9: renamed bidders.
- P10: public/private/non-US Note.
- P11: Contact includes the opening outreach.
- P7: adviser details.
- O4: signed acquirer's post-signing changes.
- O6: "Also p. N".
- O8: go-shop definition.
- O9: Rounds reconciliation.
- R8: last-dated-contact measure; target-buying talks are not sale contacts.
- R6: whole-company-only rounds.
- DS §4.5: one definition of "definitive negotiation".
- DS §4.11: a decision taken during a rival's exclusivity opens nothing.
- DS §4.12: E1 economic-scope sentence.
- DS §5: the "say how the run ends" paragraph.

## Alex questions: VM open, today dropped or resolved

The VM had five items left for Alex (DECISION_BRIEF §8; a2 README), plus FYIs.
- **Round maps (3.1):** decided by Austin for Alex or from Alex's notes (Kraton, Datalink, sTec, PetSmart).
- **Count ranges (3.2), primary Formality reading (3.3a), dropout vs censoring (3.3c):** moved to ST "Choices for estimation" as robustness switches. They are no longer questions, but are not dropped as research choices.
- **Source hierarchy (3.5):** still listed in ST "Open with Alex". No DEC theme covers it, and DEC says "None open". This is inconsistent until ST is updated (DS §10).
- **Penford Party A** (Oct 4 threshold, Oct 13 valuation statement, Oct 14 bid; questionnaire 3.4): ST still lists it. No DEC theme covers it (F11 bears on it). Dropped silently.
- **V1141 D5 exit-reason merge ("revisit with Alex"):** dropped silently.
- **Provisional VM items that went to Alex for yes/no** (V114 D5, D7, D11, D17; 2b rows): now superseded by R6, R9, F6 and R8, or silently kept.

## Retest and trial evidence bearing on today

- **Retest error "Count 1 on Merger announced" (sTec, Datalink):** fixed by O3.
- **Synacor "Process restarted" blank Count warning:** O3 makes Count required there.
- **P&W Formality agreement fell to at best 12 of 14 under v1.14.1** (retest README "Formality readings"). F3 flips G&W Jul 26 to Formal, as Alex coded it. Party B's Jul 20 bid is still in a non-final round under today's Providence map (R3 opens by Jul 27), so T3 still disagrees. G&W Jul 21 (Formal, Alex Informal) may move under F1 if its markup was not in the same communication. Check this in ROUND_MAP.
- **Mac-Gray T1u fell (CSC/Pamplona Sep 18/21 went Unclear under D3):** F5 likely restores it, if those bids are Formal and exclusivity was not Required.
- **Retest acceptance cells that today reverses on purpose:** sTec "two rounds" (now 3 rounds and 2 processes); P&W "Party E not H2" (now H2); Datalink "round 1 Jan 28" (now Jun 1); Synacor "6 rounds" (reopened round moves to Dec 30, or a seventh round). Cells that should survive: Mac-Gray 16 by Jul 23; October liability rows as blank-price Bids; Party A Sep 18 Heavy H1 and Formal; P&W 16 non-submitters; G&W Aug 12 Regulatory Concern; Party C not Not begun; Company H dropped by May 16; the WDC standstill row as a Bid with H3.
- **The 15-run v1.14 trial** (trial README; V1141 §1): no material factual errors, but disagreement across six edge zones and more rows at higher effort. That drove the VM's "defaults, no Questions" design. O1's uncapped Review items and the new judgment rules (R2 decisions, F2 once per bidder, R4 substance over label) reintroduce some of that variance. The re-extraction comparison DEC plans is the right test; note the risk in the change map.
