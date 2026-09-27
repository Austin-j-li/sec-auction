# v1.14 system upgrade specification

25 September 2026. Decisions by Austin Li. Handoff to an implementation team.

v1.14 upgrades the whole system, not only the extraction instruction. This spec covers:
- the instruction: Part A and every other part;
- the checker;
- the cockpit: server, worker, editor and downloads;
- the standalone tools;
- moving the reviewed v1.13.2 work onto v1.14;
- a first analysis tool that turns ledgers into estimation data;
- the documentation;
- the deploy and release procedure.

It replaces Astra's approval spec ([ASTRA_APPROVAL_SPEC.md](ASTRA_APPROVAL_SPEC.md), copied unchanged from Astra's working folder; on 25 September that folder's other files, `INSTRUCTION_CHANGE_PLAN.md` and `sources/`, moved here and the folder was removed) wherever the two differ. Astra's spec and its evidence record ([ASTRA_RECOMMENDATION_REVIEW.md](ASTRA_RECOMMENDATION_REVIEW.md)) still hold detail and source citations. Use them where this spec is silent, never against it.

Order of authority:
1. the decisions in §1;
2. the rules and packages in §2–§13;
3. the four audit reports in [systemic-audit/](systemic-audit/), for line-level detail: [A](systemic-audit/A_checker_tools.md) checker and tools, [B](systemic-audit/B_cockpit.md) cockpit, [C](systemic-audit/C_instruction_cascade.md) instruction cascade, [D](systemic-audit/D_docs_release_research.md) documentation, release and research. A proposal in an audit that this spec does not adopt is not adopted;
4. Astra's spec;
5. older drafts.

The frozen repository instruction `SEC_Deal_Ledger_Extraction_Instruction.md` (v1.13.2) changes only at release (§13, gate 9), at Austin's request.

| § | Content |
|---|---|
| 0 | For the team: scope, safety, the separate working copy |
| 1 | Decisions D1–D26 |
| 2 | Part A, verbatim |
| 3 | Instruction changes, section by section; the draft lines to change (§3.1) |
| 4 | Conditions (E12), consolidated |
| 5 | Replacement Questions for Alex (package A2) |
| 6 | Map re-check (package M) |
| 7 | Work packages, by layer of the system |
| 8 | Choices made without asking Austin |
| 9 | Acceptance |
| 10 | How this differs from Astra's spec |
| 11 | References |
| 12 | Deploy checklist |
| 13 | Release procedure and Austin's gates |

## 0. For the team

Read these first:
- `AGENTS.md`;
- `_dev/HANDOFF.md` (out of date; S6 fixes it);
- this folder's `README.md`;
- [TAXONOMY_DRAFT5.md](TAXONOMY_DRAFT5.md), the column set Austin and Alex confirmed on 24 September;
- the 24 September draft instruction, [SEC_Deal_Ledger_Extraction_Instruction_v1.14_draft.md](SEC_Deal_Ledger_Extraction_Instruction_v1.14_draft.md) (SHA-256 `f9595d74…`), which is the base text;
- the audit report for your layer in `systemic-audit/`.

**Authorized by this spec:**
- the work packages in §7;
- local files in this folder, including new subfolders for package outputs;
- code and test changes in a separate working copy (below);
- in this checkout, the documentation lines of class "now" listed in S6 (D26);
- offline tests;
- read-only access to the cockpit state for packages M, MIG, P, S1, S2 and S7: SQLite only through `file:…?mode=ro` URIs, and version and filing files only by copying them;
- reading `lesson/` for packages M, MIG and A2, at its absolute path in the live checkout (it is untracked, so a worktree made from `HEAD` lacks it);
- reading `ref/seed.csv` for packages S3 and P, and `ref/deal_details_Alex_2026.xlsx` for package P only.

These are evaluation uses: nothing derived from `ref/` or `lesson/` may reach an extraction run.

**Not authorized:**
- model or extraction runs, including runs on the cockpit;
- creating, publishing or making default a cockpit instruction version;
- service deploys or restarts, and changes to systemd units;
- HTTP requests to the live services;
- edits to any workbook, cockpit working copy or cockpit state, including applying migration edits;
- moving or overwriting files in `extraction/`, or editing `_dev/cockpit/catalog.json` (D25 is a release step);
- edits to the frozen instruction;
- Dropbox changes, or sending anything to Alex;
- commits and pushes.

Each of these needs Austin's command. App actions are attributed to a person, so do not act as Austin in the cockpit unless he asks.

**The live services run from this checkout. Do not edit code here.**
- `ledger-worker` starts `_dev/tools/check_lean.py` afresh for every job (`worker.py:50`, `:311`) and stores the result permanently. A half-built checker would write permanent receipts for any run Austin or Alex starts.
- `ledger-cockpit` imports `check_lean` once, when it starts (`workspace.py:20`), for the live recheck and the editor's choice lists. It keeps the old checker until it is restarted.
- `ledger-cockpit` serves `_dev/tools/cockpit/dist/` from disk on every request (`server.py:185-194`). Rebuilding `dist/` here would put a new frontend live at once.

So make every change under `_dev/tools/` (code, tests, `dist/` and `_dev/tools/README.md`) in a separate git worktree or copy of the checkout:
1. Create it under `/home/uctpiaj/work/`, never under `/tmp`. The root disk, which holds `/tmp` and the nightly backups, was 97% full (341 MB free) on 25 September.
2. Create it from `HEAD`. Apply the checkout's uncommitted diff (`git diff --binary HEAD`) and copy the untracked files under `_dev/tools/`.
3. At the same moment, keep a baseline copy of the live `_dev/tools/`, without `node_modules` or `dist/`. The deploy patch is taken against it (§12).
4. For the frontend, copy `node_modules` from the checkout (491 MB) rather than downloading it.

Run HTTP and browser tests there only against a temporary state directory, never against `_dev/cockpit/state/` or the live services. Never use `serve_fixture.py --actual-catalog-readonly`: it serves the live checkout and opens a write connection to its database (audit B17). Put `TMPDIR` and every `COCKPIT_*_EVIDENCE` folder under `/home/uctpiaj/work/tmp/v114-scratch/`. Delete nothing else under `/home/uctpiaj/work/tmp`: other sessions and tools use it. The code reaches the live checkout only when Austin orders a deploy (§12).

Files that do not affect the services may be written in this checkout:
- this folder's deliverables;
- `_dev/HANDOFF.md` and `_dev/RESEARCH_QUESTIONS.md`;
- the "now" lines listed in S6 (D26): the root `README.md`, `_dev/CHRONOLOGY.md`, `_dev/cockpit/README.md`, the Mac-Gray pilot README (`_dev/reviews/2026-09-21-mac-gray-pilot/README.md`, line 3), and the do-not-read line of `AGENTS.md`.

**The working tree has uncommitted changes from earlier sessions** (see `git status`):
- the 24 September taxonomy work (checker 1.6, `workspace.py`, tests, the tools README);
- a deal-review-status feature (`server.py`, `trace.py`, `backup.py`, the acceptance tests, frontend sources, `dist/`, `_dev/COCKPIT_BUILD.md` and `_dev/cockpit/README.md`).

Build on them as they are. Never revert them. Before editing any file that `git status` shows as modified, save its earlier changes as `pre-existing/<path>.patch` in this folder (`git diff HEAD -- <file>`), so that gate 0 can commit them on their own with `git apply --cached` (interactive staging is not available here). `lesson/` is untracked and not ignored, so never stage with `git add -A`.

## 1. Decisions

"Final" means Austin's decision. "Provisional" means it is adopted in v1.14 and goes to Alex for a yes or no in the replacement questions (§5); if he disagrees, a later version changes it.

| # | Decision | Source | Status |
|---|---|---|---|
| D1 | **Scope.** v1.14 adopts Astra's §5 section-by-section changes, as listed in §3 and modified by D2–D27. Two of these change rules in TAXONOMY_DRAFT5 §3.3, which Alex confirmed; see the note below the table. | Austin, 25 Sep | Final |
| D2 | **Part A.** Keep the 24 September draft's Part A with the edits in §2. Astra's proposed opening is not used. | Austin, 25 Sep | Final |
| D3 | **Regulatory.** Keep the TAXONOMY_DRAFT5 rule. Concern rules out None but does not set any level; E12's "identified obstacle to completion" can still make a bid Heavy on the evidence. Astra's narrower Concern and "Concern forces Heavy" are not adopted, in the instruction or the checker. A bare statement that approvals are required is Not stated. | Austin and Alex, 24 Sep (TAXONOMY_DRAFT5:60, :76); Austin, 25 Sep | Final |
| D4 | **CVR/earnout is consideration, not a condition.** By itself it neither makes a bid Heavy nor prevents None. | Austin, 25 Sep | Final. Tell Alex: it changes the Part A wording he saw on 24 Sep. |
| D5 | **Financing precedence (the walk-away test).** A bid stated not to be subject to a financing condition is Committed, even where the debt commitment is unsigned or in draft, or the lender support is only highly confident. The Note records the state of the lender documents and any reverse termination fee. Otherwise the draft's Committed and Contingent definitions apply. | Austin, 25 Sep | Provisional (Alex Q6(b); consistent with the option recommended to him) |
| D6 | **Light.** Keep the draft's Light, with both of its routes. Astra's stricter Light is not adopted. | Austin, 25 Sep | Final |
| D7 | **Partial-company bidders.** Whole-company live counts and the auction screen cover whole-company bidders only. Partial-only bidders keep their Other-scope rows, scope and dates. A bidder that switches to a partial offer leaves the whole-company contest at the switch. Where the target weighs a break-up or partial offer against a whole-company sale, raise a Question naming the parties so that a wider count can be rebuilt. | Austin, 25 Sep; Alex, August Q&A Q7d ("These do not compete against bids to sell the entire company") | Provisional (Alex Q2; changed from option C, recommended to him on 24 Sep) |
| D8 | **Rounds.** Adopt Astra's E6: count a stage once; a deliberate reopening of outreach opens a round; finality is the procedure the target announced or visibly put in place. Before any data changes, the team re-checks the maps under it and reports to Austin (package M). Austin's Datalink F9 ruling stands until he decides otherwise. | Austin, 25 Sep | Provisional (Alex Q3 and the round maps in Decision 1) |
| D9 | **Formality on a price-only revision: express reference only.** Formality carries over only when the bidder itself refers back to earlier terms that qualified as Formal under E11. That the target negotiated from an earlier markup, or later document work, does not by itself make the revision Formal. | Austin, 25 Sep | Provisional (Alex Q5; **changed** from option B, recommended to him on 24 Sep) |
| D10 | **A missed deadline without departure is not an exit.** A bidder that misses a due date but carries on gets no exit and no re-entry. Did not submit is used only where participation ends. | Austin, 25 Sep | Provisional (Alex Part 2, reading 2) |
| D11 | **Deadlines, option Q7-A with Alex's extension convention.** A later due date set for the solicitation is Extended, as before. Improvements the target invites after acting on the bids in hand, with no new due date set, are bargaining within the round: the deadline was Enforced. An overdue required response (first, revised or final) that the target still considered is an extension, recorded as `Extended (late bid accepted)`. | Austin, 25 Sep. The convention that an accepted late bid is an extension is Alex's, reported verbally by Austin on 25 Sep; it is not in Alex's written materials. | Provisional (Alex Q7) |
| D12 | **Part F keeps its judgment rule.** Raise a Question only for a call that could reasonably go the other way and matters. Alex's A–M flag list is not made mandatory. The v1.14 acceptance review of every offer's conditions is a reviewer step, not a model Question. | Austin, 25 Sep | Final |
| D13 | **R01 becomes the general E10 rule.** Same-price changes to bidder commitments (reverse fee, sponsor guarantee or damages cap, financing or closing conditions) are Bid rows. The target's termination fee stays in a dated Note. | Austin, 22 Sep (Mac-Gray R01); made general 25 Sep | Final |
| D14 | **Exclusivity never changes Formality or the Conditions level.** An exclusivity period is not a diligence period. A stated period of two weeks or more for remaining diligence counts toward Heavy under H2, unless the filing says only confirmatory or limited diligence remains. | Austin, 25 Sep (confirming the default); Alex, voice note II.7, on Formality | Final (answers Alex Q6(a) in principle) |
| D15 | **A later exclusivity request gets its own row.** It is an Exclusivity changed row and does not recode the earlier bid. If it comes with a material revision of the offer, it is one Bid row coded with the exclusivity, not a Bid row plus an Exclusivity changed row. This reverses TAXONOMY_DRAFT5:40. §8 extends the one-row rule to any bid communication; a later request with no other change is never a same-price Bid row (§3 E10). | Austin, 25 Sep | Final |
| D16 | **Varies covers partial reporting.** A cohort row uses Varies when the filing reports a term for only some members; the split goes in the Note. | Austin, 25 Sep | Final |
| D17 | **Merger of equals.** No "control surrendered or premium paid" screen. Record the dated talks and the disclosed roles. Flag the unclear scope and its effect on the process map, and give the alternative map where it stays unresolved. | Austin, 25 Sep | Provisional (Alex Q4; option C withdrawn) |
| D18 | **Other-scope bid rows leave the per-share amounts blank:** Price low, Price high and CVR/earnout value. The amount, units and scope go in the Note. The other bid columns stay required as on any bid row. This applies to v1.14 only. | Austin, 25 Sep | Final |
| D19 | **Replace the 24 September Questions for Alex** with the document specified in §5. Keep the original. Sending it is Austin's action. | Austin, 25 Sep | Final |
| D20 | **SEC link in the downloaded Excel.** The pipeline adds the filing's EDGAR link and run provenance to the workbook downloaded from the cockpit. The model never writes these. The stored raw version and the checker's four-sheet contract do not change. | Austin, 25 Sep; Alex, Q&A of 12 Aug | Final |
| D21 | **Pipeline scope.** Defer Astra's assisted map review (§7.3); S4 and MIG replace it. Do not hand-correct the two superseded pilots. Split Astra's Package A as §7 does. The analysis contract, first put in the backlog, is in scope under D22; market data stays in the backlog (D23). | Austin, 25 Sep; amended the same day | Final |
| D22 | **A first analysis tool.** Build a mechanical tool that turns a ledger into estimation tables, with a versioned analysis contract (package P). Choices that need Alex's answer are switches with no default: how to use count ranges, how to treat Unclear, which Formality reading is primary, whether same-price revisions are new price observations, and whether inferred exits are dropouts. A side-by-side with Alex's hand-coded `bid_type` is a review aid, never a target for tuning the instruction. | Austin, 25 Sep | Final; the switches go to Alex (§5) |
| D23 | **Market data stays in the backlog.** The target's share-price series needs an outside data source, which is Austin's call and may cost money. Filing-reported prices and premiums stay in the Notes (E13). §7.15 outlines the later join. | Austin, 25 Sep | Final |
| D24 | **Reviewed work moves deal by deal.** The eight v1.13.2 working copies stay as they are until that deal's v1.14 run has been reviewed. Then the deal is rebased onto the run, and what still holds of the old review is ported as one attributed revision. The team builds a reviewed-facts register, an aligner and a triage report, and the cockpit fixes that make a rebase safe (package MIG). | Austin, 25 Sep | Final |
| D25 | **`extraction/` at release.** Move the nine v1.13.2 workbooks, bytes unchanged, to `_dev/reviews/2026-09-22-opus55-reextraction/workbooks/`. Repoint their catalog paths, keeping the id, hash and instruction version, so the working copies still resolve (with S5's change to how the cockpit finds catalog deals, deployed at gate 3). Update `import_results.py` and `verify_catalog.py` in the same commit. Then export the v1.14 blind runs to `extraction/`. | Austin, 25 Sep | Final (carried out at a commit Austin requests) |
| D26 | **Documentation scope.** The team updates the current-state lines of the root README, CHRONOLOGY, the cockpit README and the pilot READMEs now, and adds `lesson/` to the do-not-read lists of AGENTS.md and the root README. Lines that make v1.14 the working instruction wait for the release. | Austin, 25 Sep | Final |
| D27 | **Coding calls confirmed.** Austin confirmed these §8 calls as written: merger-of-equals talks as events outside the counts; exclusivity as a term (a later request alone is an Exclusivity changed row; a request in any bid communication is coded on that bid row); alternative structures as separate rows; the four D7 scope details; Concern makes a bid Heavy only when the bid depends on it; two weeks or more of "expedited" diligence is H2; a package that cannot be split leaves the price cells blank; and the four carried over from the first version ("substantive diligence completed" is Incomplete; "no financing condition" outranks a highly confident letter; confirmatory-only defeats the two-week test; a new date set after evaluation is Extended). §8 marks them. | Austin, 25 Sep | Final, except where the underlying decision is provisional (D5, D7, D11, D17) |

**Note on the 24 September taxonomy.** Its decisions (the column set, upfront-only prices, Contingent for highly confident or uncommitted financing, and the rest in the v1.14 handoff) stand, with these changes:
- D4–D6 and D14–D16 refine them.
- D15 replaces TAXONOMY_DRAFT5:40.
- Under D1, **express incorporation** (§3 E10) replaces TAXONOMY_DRAFT5 §3.3(a)–(b). A revision now carries only the terms the filing says were carried, and a status fact such as diligence progress is judged at the new date instead of being copied.

Alex confirmed both of those rules, so both appear in the replacement questions (§5).

## 2. Part A, verbatim

Use this text as Part A of the candidate. It is the 24 September draft with four edits:
- a sentence about sales that depart from the auction pattern;
- "for the whole company" in item 1 (D7);
- item 3 rewritten (D4, D14; the heading no longer implies legal enforceability);
- "change" instead of "upgrade" in the last sentence.

> ## A. What the ledger is for
>
> You will read one SEC merger filing, chiefly its “Background of the Merger” (or “of the Offer”) section, and record the sale process as a small Excel ledger, one row per event. The ledgers feed structural estimation of takeover auctions in which a target first collects informal, non-binding bids, selects who advances, and then collects formal bids. Many sales depart from that pattern, with bilateral talks, changes of scope, soft deadlines, or efforts that stall and restart: record the process the filing reports, not the pattern, since the departures are themselves data. An expert reviewer will check your workbook by hand against the filing.
>
> The model reads the ledger as data, so each of these matters, in this order:
>
> 1. **How many bidders for the whole company are live at each stage**: who entered, who left, when, and by whose decision. This is the competition each bidder faced, and an exit tells the model something about that bidder's valuation.
> 2. **Which round each bid belongs to**, and where rounds and separate sale processes begin and end. A bid is read against the solicitation it answered and the rivals live at that moment.
> 3. **Whether each bid is formal or informal, and how conditional it is.** Formality is often open to interpretation, so the researchers estimate under more than one reading and need its evidence recorded separately. Formality records the procedure: whether the bid engaged with definitive documents or answered a final solicitation (E11). The condition columns record what could still change the price or stop the deal: diligence still to do, financing not committed, a regulatory concern (E12). In analysis, a formal bid carrying such conditions may be treated as informal, so a condition never changes the Formality label; a later revision that changes them is a new bid (E10). A contingent payment belongs with the price (item 5), not among the conditions, and exclusivity is recorded as a term; neither by itself changes Formality or the Conditions level.
> 4. **The order of events.** Bidders and the target react to what came before; the sequence matters more than the exact day.
> 5. **Bid prices and what they are made of**: the upfront amount, the stock share and any contingent payment, so that bids can be compared; and differences in what bidders were told or shown.
>
> These conventions cannot foresee every filing. Where they are silent, make the call that serves these five uses best, record it plainly, and raise a Question if it matters (Part F). Classify each offer and each stage as it stood at the time: what happened later does not change it.

Part A states the purpose. It must not become a second rulebook. Each rule in it has its operative form in Parts B–F, and every later reference to Part A ("use judgment from Part A", "the five uses in Part A") must still resolve. Audit C §3 confirms that all of them resolve against this text; "a later revision that changes them is a new bid (E10)" resolves only once E10 changes as below.

## 3. Instruction changes, section by section

Apply these to the 24 September draft. **This list is complete: an item in Astra's §5 that is not listed here is not adopted.** Each change cites its origin: a decision in §1, §8, or "Astra" where Astra's §5 text is adopted as proposed. Astra's section 5 gives fuller wording; condense it to the instruction's style. Keep changes general: no rule justified only by one deal. Draft line numbers refer to the 24 September draft.

**Rules for writing the candidate.**
- Write each rule in the instruction's own words. Copy no decision number from this spec: the instruction's own D1–D5 are its sheet sections, so "(D4)" would send a model to the Questions sheet. H1–H3 are instruction labels and may be used.
- Name no deal, and use no figure or wording taken from a deal. Replace the reference example at draft line 247 ("Ref: $12.10 close 08/08/2014; 49% premium", which is Penford's) and the range "50–75" at line 249 (Pepco's, TAXONOMY_DRAFT5:28) with neutral numbers. Examples use neutral wording, not a filing's phrases (§4).
- Add no project or provenance text: nothing like "this follows Alex's convention", "this fixes the recurring error", "remains deferred" or "v1.14 only".
- Use audit C §1 as the line-level map. The CHANGELOG lists every cascade line it names as changed or as confirmed unchanged.

**Header.** "**Revision of <date>, v1.14.**", keeping the bold and the final period, as in v1.13.2. The candidate carries its final header from the start (§8), so the text evaluated is the text published. `<date>` is the day the text, after R's fixes, is frozen for gate 4. It changes only with a new draft at gate 7, because any change alters the text's hash.

**B. Evidence** (Astra §3.2, §5 "B, D1 and F")
- Distinguish four kinds of value, replacing "Every cell is one of three things" (line 24):
  - reported facts;
  - exact calculations from reported inputs;
  - classifications under a convention;
  - inferences.
- Inferred = Y marks an inferred event **or an inferred material field**; the Note names the field. Ordinarily applying a fixed classification is not an inference. Change D1 item 22 (line 67) to match, and rewrite lines 28 and 68, which speak of "an inferred row", so that they work per field: the Note names the inferred field and the page of its anchor.
- An exit label that E14 assigns by its transition rules is a classification, not the false precision line 26 warns against.
- Evidence applies at its own date.
  - A later passage can establish an earlier fact only if it expressly dates that fact.
  - A later development is never projected backward.
  - An earlier row's value is not evidence that the value still applied, except where terms are expressly incorporated (E10).
- An inferred closure may have an unknown reason. Resolve the clash with F.3 (below).
- Keep B's precision, subtraction and quotation rules.

**C. How to work** (Astra §3.3)
- Read: while reading, build an inventory of dated acts, each with actor and scope.
- Map: also fix participant and cohort relationships, keeping apart eligibility for a solicitation and admission to it.
- After any correction, reconcile the dependent counts, round membership, prices, `#` references, deadline outcomes and process totals.
- No change for Astra's two-way reread (line 35 already checks each paragraph both ways) or for a promise of no human checkpoint (the draft makes none).

**D1. Deal ledger**
- Items 8, 9 and 12 (Price low, Price high, CVR/earnout value). Items 10–19 say "on those rows", pointing back to item 8's list "Bid, Bid reaffirmed and Other-scope bid rows" (line 53). Keep that list as the one definition of bid rows, so Stock %, Formality, Conditions and the condition columns still apply to Other-scope rows. State the D18 blanks as a separate sentence: "On Other-scope bid rows, leave Price low, Price high and CVR/earnout value blank, and give the amount, units and scope in the Note."
- Items 11 and 18 (CVR/earnout and Antitrust): Y, Varies or blank. The draft's items say "Y … else blank"; the checker's `MARKER` and TAXONOMY_DRAFT5 §3.2 already allow Varies. Line 232 already says "A Y on a cohort row means every member carries it". Add "if only some do, Varies" (D16), and make the sentence cover CVR/earnout as well as the condition columns.
- Item 12 and E13 (line 251): CVR/earnout value is filled only where CVR/earnout is Y. On a Varies row the amounts go in the Note. The checker enforces this (`bid.cvr_value_marker`).
- Item 22, Inferred: as in B.

**D2. Event labels**
- Bidder interest: an approach that *communicates an acquisition proposal* with a price is a Bid. A market reference, a hypothetical ceiling, or a refusal to pay above a threshold is not by itself a proposal (E10).
- Did not submit: redefine as in E14 (D10). No new label. A continuing bidder's missed submission goes in the Note of the round's Deadline or Deadline revised row and in the Rounds line's How it ended; it gets an Other material event row only if it passes the row test. Add missed submissions and price feedback to the examples of Other material event (line 89).
- Exclusivity changed (line 88): a request made in a bid's own communication is recorded on that bid row, not here (E10, E12).

**D3. Rounds**
- Who was in: keep apart those admitted to the stage, those eligible but not admitted, and continuing alternatives such as a partial offer still under consideration (D7). Keep "still being received, not admitted". Never list lifetime NDA signers as admitted.
- Deadline outcome values in v1.14: `Enforced`, `Extended`, `Extended (late bid accepted)`, `Passed without action`, `Unclear`; `No deadline stated` only when no date was set (D11).
- Bids received: count distinct whole-company bidder units, not revised-offer rows. Name any partial-only bids separately in the same cell (D7).

**D4 and F. Questions and delivery** (D12, plus the compatible parts of Astra's section 5)
- Keep F's judgment rule and "Give a recommendation every time". A recommendation may be to keep a range or an unknown; never invent a point to fill it.
- A Question says whether its issue is a gap in the source, a permitted inference, a choice of convention, or a decision for the researchers. This goes in the Question's text; the Questions sheet keeps its seven columns.
- Group related rows into one Question where that stays readable.
- The final audit looks for omitted events as well as wrong rows.
- **F.1:** participation and live units are reconciled for the whole-company contest. Partial-only parties are accounted for by their own rows (D7).
- **F.3:** keep its rule, and add: "an inferred exit's label follows E14's transition rules, and its Exit reason is Not stated unless the filing reports one".
- **F.4:** every Bid, Bid reaffirmed and Other-scope bid row has Stock %, Formality, Conditions, Due diligence, Financing, Regulatory and Exclusivity. Other-scope bid rows leave Price low, Price high and CVR/earnout value blank (D18).

**D5. Deal facts.** Add no field, and do not edit the field labels or their parentheticals at line 121: the checker accepts only those strings. State the Acquirer type values, which the checker already enforces but the draft never lists (audit C §4). The SEC link is added to the downloaded copy by the pipeline, not written by the model (D20). The auction screen follows E1. "Whole-company bids: No" continues to mark a partial-only deal for the research sample.

**E1. Scope and the auction screen** (D7, D17, Astra)
- The whole-company contest is primary.
- Partial-only bidders:
  - Record them as Other-scope bid rows, with scope, dates, and amounts in the Note.
  - They are not whole-company participants for live counts or the auction screen.
  - A party whose involvement the filing shows was partial from the start never enters the whole-company contest. It gets no exit rows (line 260); the Note of its last row says how the talks ended, if the filing reports it.
  - Mark a supported change of scope at its date.
- A proposal of unresolved scope stays an Other-scope bid row (line 129), outside the whole-company counts, with a Question naming the party. Merger-of-equals talks follow their own rule below.
- A switch from a whole-company offer to a partial one closes whole-company participation at the switch. Use the exit label the filing supports, usually Withdrew, and say in the Note that talks continued on a partial basis. Widen Withdrew (line 256) to cover this. Later partial proposals are Other-scope bid rows.
- If a bidder that switched later returns with a whole-company proposal in the same process, it gets Re-entered.
- A later partial proposal does not make earlier involvement partial after the fact.
- Where the target weighs a break-up or a partial offer against a whole-company sale, raise a Question naming the parties.
- The screen counts independent prospective acquirers of the whole company. Uncertainty is kept.
- Merger of equals, in the instruction's own words: no "control surrendered or premium paid" screen; record the dated talks and the disclosed roles; flag the unclear scope and its effect on the process map; give the alternative map where it stays unresolved (D17). While the sale role stays unresolved, the talks are Other material event rows (the Note names the act: agreement, proposal and its terms, end of talks), and the counterparty does not enter the whole-company contest. The Question gives the alternative map in which it does (§8).
- Carry the whole-company scope through every count:
  - E3's entry rule: entry means entry into the whole-company contest;
  - E4's live units (line 153) and E5's closure Count (line 163);
  - D3's Bids received (line 112);
  - E14's live-units formula (line 271) and inferred-exit transitions (lines 262–269);
  - F.1.

**E2. What earns a row** (D13, Astra)
- A change in economic terms or bidder commitments earns a row even when it was negotiated in drafts. This takes priority over the exclusion for routine legal negotiation.
- Keep routine, unchanged document circulation out.
- Distinguish a new requirement from the target and a bidder accepting or countering it.
- Price feedback, and information given to a bidder that explains its later behavior, earn a row when they pass the row test.

**E3 and E4. Participants and counts** (Astra)
- Keep apart:
  - process participation;
  - eligibility for a solicitation;
  - admission to a stage;
  - continuing reserve or alternative status.
- Counts:
  - Keep exact counts only when the filing reports them or they follow exactly.
  - An NDA signed at some point in an interval does not prove eligibility at a deadline inside that interval.
  - Never subtract bids from a group that did not apply at that deadline to get an exact count of non-submitters. Line 264's example ("21 signers − 2 earlier exits − 8 submitters = 11") does exactly that and is rewritten (E14).
- Reconcile named members with anonymous cohorts, so that a party later named is not entered twice.
- Joint bidding is different from financing support, rollover holders, shared advisers and board changes. This is already in E4; keep it.

**E5. Processes** (Astra)
- For individual participants, silence about contacts does not prove inactivity (E14). E5(b)'s test of about three months with no reported contact (line 160) stays, as the convention for where a new process starts. Say so, so the two rules do not read as contradictory.
- An existing NDA alone does not prove ongoing negotiations.
- Keep a reported termination apart from an inferred lapse.
- Close each period of participation once. Reconcile a process closure with individual exits, so nothing is subtracted twice.
- Returning participants enter a new process only if the filing supports one.
- A merger-of-equals episode may affect continuity. Where it stays unresolved, give the alternative map.

**E6. Rounds** (D8, Astra)
- Round 1:
  - Change the lead sentence (line 173), which says round 1 opens "when the target or its banker begins soliciting buyers", so that it covers bilateral negotiation: round 1 opens at the first sale stage the target organized.
  - Change "Use, in order:" to "**Use the earliest supported of:**".
  - Round 1 opens at the earliest supported sale stage the target organized, including substantive bilateral negotiation.
  - A preliminary unsolicited approach alone does not open it.
  - Later broad outreach does not push a genuine earlier requested-bid stage back to round 0.
- Count each stage the target organizes once:
  - Admission, common diligence and a later letter setting that stage's submission are steps within one round.
  - Another round needs a distinct solicitation or selection, or a materially changed basis for submission.
  - **Delete** the draft's trigger "opens a distinct information stage tied to new offers" (line 171).
- Reopened outreach:
  - Deliberately reopening rival solicitation after a suspension opens a new round in the same process, unless E5 starts a new process.
  - A reopened round is dated at the outreach itself, never at the earlier board authorization (D8). Round 1 keeps line 173's route, which may use the launching decision where outreach followed within about a week.
  - Where reopened outreach is undated, line 198's Sort-date rule ("the decision day for an undated consequence of a dated decision") must not put it on the authorization day: give the outreach's window and a Sort date inside it after the authorization. R checks the wording.
  - Routine follow-up does not open a round, and neither does one bidder returning unsolicited.
- An unannounced round (line 171) is an inferred event: its Round opened row has Inferred = Y.
- Extensions and repeated bargaining stay within the round.
- Finality describes the procedure the target announced or visibly put in place. It is separate from which bid came last, and from E11.

**E7 and E8. Contacts and dates** (Astra)
- Keep apart first contact, sending an NDA, executing it, supplying information, and reusing an earlier agreement.
- Look in the annexes for dated execution evidence.
- Keep supported order across paragraphs. Where it conflicts with reported exact dates, flag the conflict rather than moving the dates.
- **Round opened is the first row assigned to its round**, sharing the date of the act that triggered it where that fits. The checker already enforces this (`round.opening_order`); the draft never states it.

**E9. Deadlines** (D11)
- Record, for each due date the process reached while it was still in force, one outcome from this list, applying the first that fits:
  1. **Extended**: a later due date was set for that solicitation, generally or for one bidder, even after the bids in hand were evaluated.
  2. **Extended (late bid accepted)**: no new date was set, but the target considered an overdue *required* response to that solicitation (a first, revised or final response it had asked for). The source of this convention stays out of the instruction.
  3. **Enforced**: the target used the cutoff when taking its next step on the bids in hand. Improvements it invited afterwards, with no new due date set, are bargaining within the round; record them as their own rows, and they do not change Enforced. Enforced does not mean all bargaining ended.
  4. **Passed without action**: bidding or negotiation simply continued (a soft deadline).
  5. **Unclear**.
- Record due dates, bidder-specific extensions, the actual timing of responses, invitations and later decisions before choosing an outcome. Do not infer an invitation only because conversations with the banker came before a price increase.
- Where bidders' outcomes differ, keep the difference in the Notes or a Question.
- A due date superseded before it arrived gets no outcome.
- A missed response and an exit are separate questions (E14).

**E10. Bids and reaffirmations** (D13, D15, Astra)
- A Bid is a communicated acquisition proposal. Oral, conditional and non-binding proposals count. Where the source is ambiguous about whether a statement is a valuation or a proposal, raise a Question. Line 129 also defines a Bid; keep one definition and let the other refer to it.
- Every communicated material revision of price, consideration or bidder commitment is a Bid row, including same-price changes to conditions, funding commitments, reverse fees and bidder or sponsor liability. This replaces line 208's "every change of price or material economic terms", so that Part A item 3 resolves. A material same-price revision takes priority over the Bid reaffirmed label.
- The target's termination fee goes in the Note of the row where it is agreed or changed; where no row records that, in the Note of Merger agreement signed.
- Signing the agreement does not add a price row.
- One offer communication is one row; an indication of interest and an offer are not duplicates. The draft's exception stays: alternative structures offered in one communication are separate rows ("alternative to #n"), not a range (line 208): Bid rows for whole-company alternatives, Other-scope bid rows for partial ones.
- Exclusivity is a term, not a condition, for this rule (Part A item 3). A request for, or requirement of, exclusivity made in the same communication as a Bid or Bid reaffirmed row is coded on that row, whether the bid is a first bid or a revision (D15). One made later, with no change of price, consideration or other commitment, is an Exclusivity changed row, never a same-price Bid row. A later bid row codes Exclusivity from its own communication; an earlier standing request carries over only by express incorporation (below).
- **Express incorporation** replaces line 224's "copy the earlier row's values and write “Terms: as #n” in the Note", line 210's Bid reaffirmed carry ("as they stand at that date, updated by anything the filing reports by then") and TAXONOMY_DRAFT5 §3.3(a)–(b):
  - Carry only the terms the filing says were carried, within the stated scope. The Note reads "Terms: as #n (p. x)" and names what was carried.
  - Judge status facts such as diligence progress at the new date.
  - Otherwise use Not stated.
- Bid reaffirmed: keep the existing gate. Code its fields by the same rule.

**E11. Formality** (D9, Astra)
- A price-only revision is Formal only if it has its own basis under E11, or the bidder expressly refers back to earlier terms that were Formal (express reference only).
- Later document work cannot prove engagement at an earlier date.
- A final-round label does not make every unsolicited communication a response to that solicitation. An unsolicited bid made during a final round carries that round's number, but E11's final-solicitation route applies to it only if it answers that solicitation.
- Line 220 lists what does not decide the label: the filing's own words, a price range, an exclusivity request, lateness. Add "a letter alone" to that list; it is new text, not kept text.

**E12. Conditions.** See §4.

**E13. Price and consideration** (D18, Astra)
- The price cells (line 245) and package values (line 247) take the Other-scope exception (D18).
- Subtract contingent consideration from a package only when the filing gives compatible figures and their relationship. Never subtract a maximum from a package valued on a different basis. Where the parts cannot be separated on a compatible basis, leave the price cells blank, give the package figure and its basis in the Note, and raise a Question if the bid matters for comparison.
- Stock % (line 249): Varies also covers partial reporting (D16).
- A historical share-price series is downstream work, not the extractor's.

**E14. Exits** (D10, Astra)
- Before inferring a departure, check for:
  - a continuing solicitation;
  - a still-active offer;
  - ongoing diligence;
  - explicit reserve status.
- **Did not submit** records a non-submission that ends participation: reported, or inferred when the bidder is never mentioned again after the solicitation and the narrative does not carry it forward. Delete "not necessarily permanent" (line 257). Rewrite the inferred transition at line 264 to match; its example must use a bound, not a subtraction from lifetime signers.
- A bidder that misses a due date but continues gets no exit and no re-entry. It might ask for time, be invited to continue, or submit later in the round. See D2.
- Re-entered stays for a bidder that actually left and came back, including one returning from a partial offer (E1).
- Selection for one stage does not exclude a bidder from every continuing discussion. A whole-company exit is not a withdrawal from a partial transaction. Signing with another bidder is not a voluntary withdrawal. Lines 255 and 265 (Dropped by target when the advancing set is named without the bidder) take the exceptions for explicit reserve status and continuing discussions.
- Line 262: "Exit reason = Not stated, unless the filing reports one." The inferred transitions (lines 262–269) apply to whole-company participants (D7).
- Treat the exit's actor, timing and reason separately.
- Do not infer a valuation, or an exact exclusion date, from a disappearance. Part A says an exit tells the model something about valuation; word E14 so that the extractor records the exit and its evidence, and the model does the interpreting.
- Keep the source's price comparison in the Note even when Exit reason is Not stated.
- Regulatory reasons on exit rows remain deferred (no instruction text).

**Not adopted from Astra:**
- the proposed Part A (D2);
- Regulatory Concern forcing Heavy, and the narrower Concern definition (D3);
- the stricter Light (D6);
- financing precedence for "uncommitted" (D5);
- the mandatory review list in Part F (D12);
- the Deal facts metadata allowance (D20, S3);
- "substantive diligence completed" coded Not stated. The draft's Incomplete stays; see §8.
- any other Astra §5 item not listed above.

### 3.1 Draft lines A1 must change

Beyond the lines quoted above, these draft lines state a rule that §3 or §4 changes. Audit C §2 explains each conflict; each line must be changed or confirmed unchanged in the CHANGELOG.

| Part | Lines |
|---|---|
| A | 20 ("upgrade") |
| B | 24, 26, 28, 67, 68 |
| D1 | 53–64 (the "on those rows" anchor) |
| D2 | 81, 88, 89, 93 |
| D3 | 108, 110, 112, 113 |
| E1, E4, E5 | 129, 131, 143, 153, 160, 163 |
| E6, E8 | 171, 173, 198 |
| E10, E11 | 208, 210, 220, 224 |
| E12 | 220 (a Heavy example that names no trigger), 226, 227, 228, 230, 232, 237, 238, 239, 241 |
| E13 | 245, 247, 249, 251 |
| E14 | 255, 256, 257, 260, 262–269, 271 |
| F | 283, 285, 286 |

## 4. Conditions (E12), consolidated

Keep the draft's E12 structure, component definitions and the order Heavy → None → Light → Unclear. Make these changes.

**Heavy.** Label the three triggers so that Notes can name them.
- **H1**: Financing = Contingent.
- **H2**: remaining diligence that the filing reports as substantive, or a stated period of two weeks or more for remaining diligence.
  - An exclusivity period, time to signing, or a negotiation period is not a diligence period (D14).
  - An express statement that only confirmatory or limited diligence remains defeats H2, including the period test.
  - Where the narrative only shows diligence still open, without saying it is substantive or giving such a period, the draft's Unclear clause applies, not H2.
  - Light's "expedited" diligence (line 237) applies only where H2 does not: a stated period of two weeks or more, even if called expedited, is H2 unless the filing says only confirmatory or limited diligence remains.
- **H3**: another material condition the filing expressly states for this bid:
  - a bidder right to reprice;
  - an unresolved transaction-specific prerequisite on which proceeding depends;
  - an obstacle to completion that the filing identifies for this bid.

  Ordinary approvals, routine documentation, generic risk language, a CVR (D4) or exclusivity (D14) do not qualify. Regulatory = Concern does not by itself trigger H3. The level follows the other evidence (D3).

  The boundary with Concern (line 228 includes "doubt about closing"): H3's obstacle is one the filing states this bid depends on, such as a condition the bidder attaches or a consent or clearance without which it will not proceed. A regulatory risk that the board or the bidder weighs, including doubt about closing, is Regulatory = Concern. It makes the bid Heavy only if the filing states it as such a condition.
- Line 220 gives "record Formal with Conditions = Heavy" as an example. It must name its trigger or be removed.

**None, Light, Unclear.** Keep the draft's definitions (D6).

**Components:**
- **Due diligence.** Keep the draft. Add Astra's clarification: Not begun needs affirmative support. The absence of a data-room reference is not enough, and an NDA alone does not prove diligence began. Line 226 ("from the bid or from the rest of the background") is read with B's date rule: a later passage counts only if it dates the fact.
- **Financing.** Keep the draft, and add D5.
  - A bid stated not to be subject to a financing condition is Committed, whatever the state of the lender documents. The Note records unsigned or draft commitment letters, highly confident support, and any reverse fee.
  - The precedence covers the whole Contingent list at line 227 (a highly confident letter, financing not yet arranged, any part uncommitted), not only its last sentence. Amend "Where the filing reports both a source and the absence of a commitment, Contingent" to add: "unless the bid is stated not to be subject to a financing condition".
  - Keep the walk-away wording of Committed.
- **Regulatory and Antitrust.** Keep the draft (D3). Keep a bare approval requirement in the Note.
- **Exclusivity.**
  - Replace "A request made while the bid stands and before its next revision codes that bid and also gets its own Exclusivity changed row" with the E10 rule: a request made in a bid's own communication is coded on that bid row with no separate Exclusivity changed row; a later request with no other change is an Exclusivity changed row and does not recode the bid (D15).
  - Exclusivity is recorded as a term (Part A). Where the draft says "the five condition columns" (line 224), name the columns instead: Due diligence, Financing, Regulatory, Antitrust and Exclusivity.
  - Delete "including a bidder that stops when refused" (line 230). A later refusal or departure does not show that an earlier request was conditional, unless the source makes that connection.
  - A separate grant, extension or ending of exclusivity is its own event.
  - Keep an express statement that no exclusivity was sought in the Note; add no "No" value.
  - Keep: "Exclusivity never changes Formality or the Conditions level."
- **CVR** (a new sentence in E12's last paragraph): "A CVR/earnout is consideration, not a condition: by itself it neither makes a bid Heavy nor prevents None." CVR/earnout value is filled only where CVR/earnout is Y (§3 D1).
- **Cohorts.**
  - Give a cohort a common level only when every member supports it; otherwise use Unclear and describe the composition.
  - One Heavy member does not make the cohort Heavy.
  - A cohort-wide Financing = Contingent still means Heavy.
  - Varies follows D16 and the D1 sentence in §3.
- **Dates.**
  - Use evidence at the bid's date and express incorporation (E10).
  - Signed financing that appears after the bid does not recode the earlier offer.

**Examples that the instruction and the reviewers must agree on.** Put a condensed version in E12 (§8), in neutral wording with no quotation or number from a filing: for example, "the bidder repeats its earlier terms except the price", not "otherwise on the terms previously proposed"; "several weeks of exclusivity", not "five weeks". Several rows below mirror §9.3 cases, which is why the wording must not.

| Reported evidence | Coding |
|---|---|
| An otherwise unchanged offer adds a CVR | CVR columns filled; Conditions unchanged |
| CVR present; no other condition evidence | CVR = Y; components Not stated; Conditions Unclear |
| CVR present; expressly only confirmatory work remains | Light, unless H1–H3 applies |
| CVR present; financing expressly uncommitted; no statement that the bid has no financing condition | Contingent; Heavy (H1) |
| Bid stated not subject to a financing condition; commitment letters still drafts | Committed; the Note records the drafts and any reverse fee; the level follows diligence and H3 |
| Five weeks of exclusivity requested; no stated diligence period | Exclusivity recorded; not Heavy on duration; normally Unclear |
| Thirty days expressly required for remaining diligence | Heavy (H2) |
| Two weeks of confirmatory diligence expressly all that remains; financing committed | Light (H2 defeated) |
| The board weighs a regulatory risk that applies to every bidder; diligence limited, financing committed | Regulatory = Concern; Light possible; not None |
| Diligence complete, financing committed, bidder ready to sign, CVR present | None |
| Signed financing appears after the bid | The earlier offer is not recoded as Committed |
| A price-only revision "otherwise on the terms previously proposed"; diligence status not reported for the new date | Carried terms copied; Due diligence Not stated; the level follows what remains supported |
| Two of five cohort members contingent; three not stated | Financing = Varies ("2 of 5 contingent; rest not stated"); Conditions Unclear |

## 5. Replacement Questions for Alex (package A2)

**Output.**
- A local DOCX in this folder, rendered and visually inspected.
- Keep the original: `lesson/independent-audit-2026-09-23/questions-for-alex/Open_Questions_for_Alex_2026-09-24.docx` (SHA-256 `faab1d66…`).
- Do not upload or send it.
- Keep it short. Alex circles yes or no, or writes a comment.
- State each rule in words. Alex does not know this spec's numbering; a D-number may appear only as a small reference.
- A2 depends on packages M, R and P.

**1. What changed.** One paragraph:
- the v1.14 columns are confirmed;
- this document replaces the one of 24 September;
- Austin has adopted provisional answers, some of which differ from the recommendations Alex saw or from taxonomy rules Alex confirmed.

**2a. Decided, for information (comments welcome).** Austin's final decisions. One row each: the rule, a case where it matters with page, and a "changed" marker where it differs from 24 September.

| Decision | Case | Changed? |
|---|---|---|
| D4 CVR | Mac-Gray Party B | Yes: Part A wording |
| D14 exclusivity (answers Q6(a)) | Synacor Company E: not Heavy on duration alone | Yes: option A was recommended |
| D15 later exclusivity request | Penford | Yes: reverses TAXONOMY_DRAFT5:40 |
| Express incorporation (D1, §3 E10) | sTec WDC, 10 June; Meredith | Yes: TAXONOMY_DRAFT5 §3.3(b) copied all values |
| D13 same-price commitment changes as bids | Mac-Gray, September and October packages | — |

**2b. Provisional, yes or no.** Adopted in v1.14; if Alex says no, a later version changes it. Same columns.

| Decision | Case | Changed? |
|---|---|---|
| D5 financing (Q6(b)) | Kraton Parent | No: consistent with option B |
| D7 partial bidders (Q2) | Kraton Party K; Synacor Company E, 14 December | Yes: option C was recommended |
| D8 rounds (Q3): reopening opens a round; each stage counts once | — | Option A unchanged; the count-once rule is new |
| D17 merger of equals (Q4) | Synacor, Company B | Yes: option C withdrawn; the talks are recorded as events outside the counts, with the alternative map (neither A nor B) |
| D9 Formality on price-only revisions (Q5) | P&W G&W, 26 July; sTec WDC, 10 June | Yes: option B was recommended |
| Q5, the conditions half | Mac-Gray Party B, 18 September: silent on financing, so Not stated and Unclear | No: as option B |
| D10 missed deadlines (Part 2, reading 2) | sTec Company D | — |
| D11 deadlines (Q7) | Mac-Gray and PetSmart (from M) | Yes: the value is renamed as an extension, following his convention, and covers any required response, not only a first response |

D3 needs no question, since it keeps the 24 September taxonomy.

**3. Open decisions:**
- **Decision 1: round maps under the count-once rule.** Kraton's admission and procedure letter; Datalink, noting Austin's F9 ruling; sTec's finality on 16 May. Show both maps from package M.
- **Q1 / Decision 3: what estimation needs when counts are ranges.** Keep Q1's options. The ledger always keeps the bounds.
- **Decision 3b: the analysis readings (D22).** Which Formality reading is primary (the readings T0–T3 of package P). Show package P's side-by-side on Mac-Gray and P&W: recorded Formality alone matches his labels on 13 of 13 Mac-Gray bids and 11 of 14 P&W bids; "Formal and not Heavy" matches 11 of 13 and 14 of 14. His spring coding follows one reading on one deal and the other on the other. Also ask whether same-price commitment revisions (D13) are new price observations, and whether inferred exits enter as dropouts or as censoring.
- **Readings from Part 2 still open:**
  - sTec Company H: target-side nonadvancement with bounded timing and the price feedback kept;
  - Penford Party A: 4 October is a threshold, not a bid; 14 October is its bid; 13 October is ambiguous.
- **Source hierarchy.** When his spring hand coding and the August voice notes conflict, which governs? (`_dev/RESEARCH_QUESTIONS.md`)

**4. Case appendix.** Short source excerpts with printed pages for each case above.

## 6. Map re-check (package M)

This is a read-only analysis for Austin, using the rules in §3 (the candidate text may not exist yet).

**Deals:**
- Kraton, Datalink and sTec, for E6;
- Synacor, for the reopening rule;
- Mac-Gray and PetSmart, for E9 under D11.

**For each deal, compare the current map with the §3 rules.** The current map is:
- the latest cockpit working-copy snapshot, read from the `revisions` table of `_dev/cockpit/state/workspace.sqlite3` opened read-only (`mode=ro`);
- for Datalink, which has no working-copy edits, the base version and the verified pilot revision.

**Report for each deal:**
- the current map;
- the map under §3;
- the rows and Rounds lines that would move;
- any conflict with a recorded ruling;
- a recommendation.

**Recorded rulings to check against:**
- Datalink F9: `_dev/reviews/2026-09-21-datalink-pilot/revision/VERIFICATION.md`. That revision was made on the earlier Opus 5 draft; the current draft has four rounds.
- the 24 September reverts after the independent audit, `lesson/independent-audit-2026-09-23/`:
  - working-copy revision 4 for Kraton and Meredith;
  - revision 2 for PetSmart, which keeps its deadline outcome Unclear under v1.13.2's rule.

Deliver `MAP_RECHECK.md` in this folder. Edit no workbook, working copy or state.

## 7. Work packages

All code work happens in the separate working copy (§0).

### 7.0 Overview

| Package | Layer | What | Depends on | Severity |
|---|---|---|---|---|
| A1 | Instruction | The candidate text, CHANGELOG and diff | — | Release blocker |
| R | Instruction | Independent consistency review of A1 | A1 | Release blocker |
| M | Research | Round-map re-check | — | Needed for A2 |
| A2 | Research | Replacement Questions for Alex (DOCX) | M, R, P | Needed |
| S1 | Checker | `check_lean.py` 1.7 | §1; finalized after R | Release blocker |
| S2 | Cockpit | Schema awareness: payload, choices, editor, compare, checker version shown | S1 (ship together) | Release blocker |
| S3 | Cockpit | Source sheet in the downloaded Excel | — | Needed |
| S4 | Cockpit | Bulk Process/Round edit | S2 | Optional |
| S5 | Catalog code | Current, safe `verify_catalog.py`; catalog deals found from the catalog; the D25 release patch | — | Needed; the lookup change must be deployed before gate 12 |
| S6 | Documentation | Now, deploy and release lines | All | Needed |
| S7 | Standalone tools | Cross-schema workbook diff; runner and sweep guards | S1 | Diff needed; rest nice to have |
| MIG | Cockpit and tools | Reviewed-work migration: safe rebase, register, aligner, triage | S2 | Needed before any rebase |
| P | Analysis | Analysis contract v0 and the derive tool; side-by-side with Alex's coding | S1 helper | Needed (D22) |
| OPS | Operations | Deploy readiness | — | Nice to have; §12 is required |

### 7.1 A1: instruction candidate

- Write `SEC_Deal_Ledger_Extraction_Instruction_v1.14_candidate.md` from the 24 September draft, applying §2–§4, the rules for writing the candidate (§3) and §3.1.
- Leave the draft unchanged.
- Deliver `CHANGELOG_v1.14_candidate.md`, mapping each change to its source (a D-number, a §8 item or "Astra") and listing each §3.1 line as changed or confirmed unchanged.
- Deliver a full diff against the draft file. The folder is untracked, so use `diff -u` or `git diff --no-index`.
- Record the candidate's SHA-256.

### 7.2 R: independent consistency review of A1

- An agent other than A1's writer checks the candidate against §9.1 and records its findings in this folder.
- A1 fixes them before S1 finalizes.

### 7.3 S1: checker, `check_lean.py` 1.6 → 1.7

v1.14 rules still apply when the header has `Stock %`. v1.13.2 rules are unchanged. Audit A §2 holds prototypes of changes 1–4, each run against the stored results.

**Changes:**
1. **Deadline outcome sets by schema** (`check_lean.py:261-267`, `:1297-1307`).
   - Keep the name `DEADLINE_OUTCOMES` for the v1.13.2 set: `workspace.py:353` imports it, and a rename would break every deal payload.
   - Add `DEADLINE_OUTCOMES_V114`, with `Extended (late bid accepted)` in place of `Late bids accepted`, and choose the set by `self.ledger_schema`.
   - In a v1.14 workbook, `Late bids accepted` gives a warning (`rounds.deadline_outcome_legacy`, "replaced in v1.14 by the wider 'Extended (late bid accepted)' (E9)") and still counts toward `rounds.deadline_count`. Both pilots use it on two Rounds lines each and must still display.
   - Expose the per-schema value lists through one function that S2 calls for the editor's choices.
2. **Antitrust with an incompatible Regulatory value: error**, currently a warning (`check_lean.py:633-640`; the severity is at `:635`). No gate is needed: the rule runs only on v1.14 workbooks. Update the test that asserts the warning, `test_check_lean.py:510`.
3. **Other-scope bid rows must leave Price low, Price high and CVR/earnout value blank**, v1.14 only (code `bid.other_scope_per_share`). Checker 1.6 never requires a price on any bid row, so this is a new rule, not an inverted one. Under v1.13.2 rules it would flag Synacor #54 and #59, so it is gated.
4. **`exit.inferred_reason` (`check_lean.py:924-932`) does not run on v1.14 workbooks.** Under field-level Inferred and the F.3 addition, an inferred exit may carry a reported reason. The checker cannot tell an inferred date from an inferred exit, so skipping the rule is the only workable form.
5. **Varies.** CVR/earnout and Antitrust accept Varies (`MARKER`). Two existing rules stay: Varies on a row with Count = 1 is an error (`bid.varies_single`), and a CVR/earnout value requires CVR/earnout = Y (`bid.cvr_value_marker`). The instruction states the second (§3 D1).
6. **Optional warnings, v1.14 only** (audit A12):
   - an Exclusivity changed row with the same Who and Sort date as a Bid or Bid reaffirmed row whose Exclusivity is Requested or Required (the D15 duplicate). Message: "if this row repeats the bid's own request, remove it (E10); a grant, execution or extension is its own event";
   - an `Extended` outcome with no later Deadline set or Deadline revised row in its round;
   - an exit followed, in the same process, by a Bid, Bid reaffirmed, NDA signed or Bidding group changed row of the same Who, with no Re-entered between them. Other-scope bid rows do not count, so a switch to a partial offer (D7) does not fire it;
   - an Other-scope bid row with a blank Note.
7. **Messages** that revision passes read word for word (audit A15): the Varies message mentions partial reporting; the H1 message names H1; the inference-note message adds "or names the inferred field".
8. Bump `CHECKER_VERSION` and `CHECKER_REVISION`. Replace the "v1.14 (draft)" wording at `check_lean.py:40` and `:73`. Update the checker paragraph in `_dev/tools/README.md` (line 19), describing the code as not deployed until the deploy (§12 changes it).
9. **A schema helper,** `ledger_schema(path)`, that reads only the ledger header and returns `v1.14` or `v1.13.2` by the same `Stock %` test the checker uses. S2 and P use it; there must be one detector.

**Review of the existing rules against the candidate.** Audit A §2.1 checked every §3–§4 rule. The review adds only change 4; changes 1–3 come from D11, the Antitrust rule and D18. The checker has no live-count, Did not submit or Bids received arithmetic; do not add any. Re-run the review after R, in case A1 changes a rule the checker encodes.

**Do not add:**
- Concern → Heavy (D3);
- any CVR or exclusivity rule on the level;
- a Deal facts allowance for extra fields. The checker requires exactly the 17 fields (`FACT_FIELDS`, `check_lean.py:131-149`, enforced at `:1525-1538`), and an allowance would let a model write fake provenance that passes;
- a Bids received count, or any rule that needs bidder-unit arithmetic;
- a rule tying Light to Due diligence, or requiring a Heavy Note to name its trigger.

**Tests.**
- Change `test_check_lean.py:510` (warning → error). It is the only existing test that fails on the prototype.
- Add a v1.14 twin of `test_check_lean.py:320-341` for change 4.
- *Extend* the fixtures from line 496 with the cases in §9.2.
- Keep `:506` and `:509` unchanged.

**Reproduction.**
- All nine `extraction/` workbooks and the five v1.13.2 cockpit run versions reproduce their stored results exactly.
- The two pilots change only as documented: Mac-Gray gains 2 `rounds.deadline_outcome_legacy` warnings and 2 D15-duplicate warnings (#31/#32 and #39/#40, coded under the draft's old two-row rule), and loses 2 `exit.inferred_reason` warnings; P&W gains 2 legacy warnings. The other three optional warnings add none.
- Never rewrite a stored `check.json`.

S1 and S2 ship together, because S2 reads S1's constants.

### 7.4 S2: cockpit schema awareness

1. **The payload carries the schema.** Set `payload["ledger_schema"]` from the checker report (`data.py:968-989` drops it today). If the check fails fatally, fall back to S1's `ledger_schema(path)` helper; do not write a second detector.
2. **Choices follow the displayed version's schema.** Choices come from the S1 function, keyed by the schema of the version being shown; for the working copy, its base's schema. One deal can hold both schemas, so "the deal's schema" is not enough. Today `workspace.py:349-357` gives one list per field.
   - The v1.14 Deadline outcome list excludes `Late bids accepted`; stored legacy values still display, as text.
   - Both lists include `No deadline stated`, which the choices omit today.
   - `All cash` is offered only for v1.13.2; the v1.14 columns only for v1.14.
3. **The editor accepts what the checker accepts** (`Records.jsx:123-152`). Today a blank field can only be set to a listed value, and a multi-deadline value such as `Extended; Enforced` cannot be built from a blank cell. These values are common in the reviewed working copies.
   - Deadline outcome gets a free-text input with suggestions, or a picker that builds `A; B`.
   - Other listed fields keep the drop-down with an "Other…" free-text option, so reviewers are never blocked while the lists lag behind the checker.
   - The server keeps not enforcing the lists.
4. **Compare across schemas** (`workspace.py:497`). Walk the after-version's columns, then the columns only the before-version has. Test with a v1.13.2 and v1.14 pair.
5. **Show which checker produced which result** (audit B2).
   - Going forward, store `checker_version` and `ledger_schema` in `versions.checker` and `jobs.result.checker` (`worker.py:318-321`, `:354-358`).
   - For existing run versions, read both from the stored receipt `check.json` (in the folder `versions.receipts` names) when serving. Catalog versions have no receipt pointer: read `_dev/reviews/2026-09-22-opus55-reextraction/receipts/<deal>/check.json` (checker 1.5, no `ledger_schema`), or show "At import: not recorded". Never rewrite a receipt.
   - In the Review tab's mechanical check, show "Live check: checker 1.7, v1.14 rules" and, for a run version, "At import: checker 1.6, 1 error, 16 warnings".
   - In the Runs tab and the version picker, add the checker version. On the All deals page, add it as a tooltip.
6. **Round trip.** Add a test that takes a representative v1.14 workbook through import, edit, save, reload and export. Use a synthetic fixture, or a pilot copied into a temporary workspace. Numbers, ranges, blanks, Varies, dates, flags and `#` references must stay semantically equal, and the raw version's bytes and hash must not change. Audit B found that the backend already round-trips on a scratch copy; the test locks that in.
7. Add `CVR/earnout value` to `NUMERIC_FIELDS` and `MONO_FIELDS` (`frontend/src/Records.jsx:12-13`).
8. The hard-coded `'v1.13.2'` label (`frontend/src/runs.js:6`, used at `:51`) labels only the three jobs queued before phase 4, which carry no recorded instruction and did run v1.13.2. Keep it for them (rename it `LEGACY_INSTRUCTION_LABEL`), and use the default instruction's name only as the default for a new run.

### 7.5 S3: SEC link and provenance in the downloaded Excel (D20)

- **Where:** in the server's download route (`server.py:176-178`), not in `Workspace.export`, which `export_repo.py` and `verify_catalog.py` share. Those must keep producing the four-sheet, checker-valid workbook.
  - Working-copy downloads get a fifth sheet named `Source` by default, with a four-sheet option (`?source=0`). Name the file `{slug}-working-r{N}.xlsx`.
  - Version downloads stay byte-identical by default, and offer a "with Source sheet" option.
- **Contents:**
  - a clickable EDGAR link that a person can open;
  - the Background pages (from Deal facts);
  - the filing's SHA-256;
  - the instruction ID or version and its SHA-256 (from `_instruction_hash`);
  - the version ID;
  - the raw workbook's SHA-256;
  - the working revision number (the latest row in `revisions`);
  - the deal's review status from the `deal_review` table, with the revision at which it was set, and "edited since" where the working revision is later; or "not set" (§8);
  - the export time.

  Write "not recorded" for any value that is unknown.
- **Link source:**
  - Add one helper, `index_link()`, beside `submission_link()` in `fetch_filing.py`. It derives the EDGAR filing index URL from the complete-submission `.txt` URL, and replaces the two copies of that rule (`fetch_filing.py:237`, `cockpit/deals.py:240`).
  - Seed deals: `ref/seed.csv` already records `index_url`, and it equals the derived URL for all nine. Use it and cross-check it with the helper.
  - Added deals: `added_deals.index_url`.
  - Show both the index link and the complete-submission `.txt` link, labelled. Never guess a URL. Take hashes from receipts, never from file names.
- **The five-sheet file is not checker-valid** (`schema.sheets`), by design; keep the checker strict. S7 makes the runner's revision mode refuse it.
- **Tests:**
  - the working-copy download has five sheets with the right values; update `acceptance/test_http.py:252`, which expects four;
  - `?source=0` gives four sheets;
  - raw version downloads are unchanged (`test_http.py:200`, `:206`);
  - `export_repo.py` output is unchanged. Fix the comment at `test_cockpit_export.py:130`, which calls the export "the server's download bytes".
- Build any frontend change in the separate working copy. Its `dist/` already carries the other session's uncommitted feature; keep it.

### 7.6 S4: bulk Process/Round edit (optional; last)

This responds to Alex's complaint about renumbering rounds throughout a deal, and replaces the deferred map-review workflow.
- In the ledger editor, set Process and/or Round on selected rows as one saved, attributed revision. The edit API already saves atomic multi-row batches (`_dev/COCKPIT_BUILD.md:63`, `:84`).
- One save is capped at 100 operations (`workspace.py:742`), and v1.14 ledgers may pass 85 rows. Add one bulk operation, or raise the cap for it.
- Tests at the level the existing suites cover.

### 7.7 S5: catalog code

- **Make `verify_catalog.py` safe and current.** Its assertions are stale: revision 0 (`:83-84`), one version per deal (`:85-87`), an unedited working export (`:97-101`), a displayed check equal to a fresh check of the base (`:103-108`), and unchanged state files (`:117-119`). Today `verify()` raises before `main()` (`:127-132`) writes `_dev/reviews/2026-09-22-opus55-reextraction/catalog-verification.json`; updating the assertions alone would let it overwrite that evidence. Replace the assertions with these:
  - every catalog version's file exists and matches its SHA-256;
  - every working copy renders at its latest revision, and its base id and hash equal `revisions.base_id` and `base_sha256`;
  - the API's version list starts with "working" and contains every catalog and imported version;
  - for unedited deals only, the working export equals the base bytes and the displayed check equals a fresh check.

  Write the result to a new timestamped file, and refuse to overwrite an existing one. Do not run `main()` against the live state.
- **Find catalog deals from the catalog** (deployed at gate 3). Today the cockpit lists and resolves a catalog deal only if `extraction/<slug>.xlsx` exists (`data.py:686-694`, `:709`), so relocating the workbooks (D25) would make all nine deals, including the eight reviewed working copies, disappear. Change `slugs()` and `resolve()` so that a catalog deal is found from `catalog.json` and `raw_filing/MANIFEST.csv`, with its workbook taken from the catalog base's `path`. Nothing changes while the files are in place. Test: in a temporary root with `extraction/<slug>.xlsx` removed and the catalog path pointing elsewhere, the deal lists, its working copy renders and exports, and the new `verify_catalog` passes.
- **Prepare the rest of D25** as a separate release patch, applied at gate 12, not at the deploy:
  - `import_results.py` (`:23-36`, the path at `:216`) and `verify_catalog.py` (`:73`, `:75`) take the relocated paths under `_dev/reviews/2026-09-22-opus55-reextraction/workbooks/`;
  - tests show that after relocation the working copies still resolve (same id and hash), and that `export_repo.py` then accepts `extraction/<slug>.xlsx`, which the catalog no longer names (`export_repo.py:148-153`).
- Nothing in S5 touches the catalog or `extraction/` now.

### 7.8 S7: standalone tools

- **`diff_workbooks.py` across schemas** (audit A8 and A §2.4). Today it matches whole rows, so a v1.13.2 workbook against a v1.14 one reports every row as removed and added. Reviewers need this comparison (§13, gate 6).
  1. Align columns by header, and report once per sheet the columns present in only one workbook.
  2. Match rows by a key, not the whole row: Deal ledger by (Event, Who, Sort date), with an optional second pass on the quoted passage; Rounds by (Process, Round); Questions by Q; Deal facts by Field.
  3. Skip a `Source` sheet by default; `--include-source` compares it too.
  4. Add `--crosswalk`, which labels differences that come from the schema:
     - All cash to Stock %: Yes ↔ 0; No ↔ a number above 0, a range or Part stock; Not stated ↔ Not stated; v1.14's Varies has no equivalent;
     - the price shown with its CVR/earnout value, not equated with the old price;
     - Other-scope price differences suppressed where v1.14 is blank;
     - `Late bids accepted` against `Extended (late bid accepted)`, labelled "D11 (wider): shown, not equated";
     - the new condition columns marked "added in v1.14", and Conditions flagged "E12 rules changed".
  5. Print an event-count summary before and after.
  6. Update `test_review_helpers.py:17-47` if the output format changes.
- **`sandbox/run_model.py`** (audit A10, A11):
  - `prepare` refuses a `--revise-from` workbook that does not have exactly the four sheets, so an S3 download does not fail only after a paid run;
  - it records `revised_from_ledger_schema`, and requires `--instruction` for a v1.14 workbook;
  - it records `instruction_source` beside the instruction's hash;
  - until release, a command-line run of the candidate must pass `--instruction`: the default is the repository file, v1.13.2 (`run_model.py:264`).
- **`effort_sweep.py`** (audit A7, A9): `plan --instruction`; `--filing-dir` for added deals; Event in the bid key, with Other-scope rows reported separately; `checker_version` and `ledger_schema` in each receipt.
- **`findings_text.py`**: a first line naming the checker version.
- **Grading references** in `_dev/reviews/2026-09-22-opus55-sol6-sweep/grading/` are pinned to v1.13.2 meanings. They are historical; do not reuse them for v1.14 without re-keying.

### 7.9 MIG: moving reviewed work to v1.14 (D24)

**What is at stake** (read-only, 25 September; audit E corrected audit B's count): eight deals have edited v1.13.2 working copies. Every Deal ledger row of their latest snapshots is marked: 454 "reviewed" and 66 "needs decision" (520 rows). There is one finding decision (Mac-Gray R01, supported and applied) and three comment threads. Datalink has no edits. A working copy's columns are fixed by its base (`workspace.py:618-621`, `:265-316`), so a v1.13.2 working copy can never gain the v1.14 columns. Rebasing onto a new version today saves one revision and silently resets every row mark and finding decision, and detaches row threads.

**MIG-C: cockpit fixes** (deployed with S2):
- A past revision (`rev:N`) can be chosen as a read-only compare source and downloaded, without restoring it.
- The rebase dialog lists, with counts, what stops applying: revisions, row marks, finding decisions and row threads.
- Case-level finding judgments carry across a rebase; only their implementation and verification reset.
- A thread whose row is gone is labelled "on an earlier base (revision N)", not "Record removed".
- The Extract dialog adds one line when the deal's working copy is under another instruction or schema.
- Keep the invariant that a working copy's columns equal its base's.

**MIG-T: register, aligner and triage** (new modules, for example `_dev/tools/migrate_review.py` with `test_migrate_review.py`). They read only: the state through `mode=ro`, copies of version files, and `lesson/independent-audit-2026-09-23/` (`inventory/<deal>.csv`, `deals/<deal>-verdicts.csv`). They write only under this folder's `migration/<deal>/`.
1. **Register.** Per deal, from the latest working-copy snapshot, its row marks and finding decisions, and the audit's verdicts. It has two parts:
   - a row list: every Deal ledger row of the snapshot with its row mark;
   - facts: one item per estimation-relevant fact, in Part A's order (participation and exits, the round map and deadline outcomes, each bid's price, Formality and terms, the order of events).

   Each fact carries:
   - its filing key: page, cockpit block id and quote;
   - the reviewed value;
   - its basis: reported, inference, or a convention;
   - its status: supported, reverted or unresolved;
   - its v1.14 impact: unchanged; re-judge under a named decision (D5, D7, D9–D11, D13, D15, D16, D18, express incorporation, H1–H3); or a new column with no reviewed value (the condition components, CVR, Stock %). All cash maps to Stock % as in S7's crosswalk.
2. **Aligner.** Match a v1.14 run's rows to register items by event family, normalized Who, overlapping Sort-date windows and price (with or without the CVR). Accept unique matches only. Align Rounds lines by opening date and members.
3. **Triage report,** per deal, in four buckets:
   - agrees: accept, with a seeded spot-check sample;
   - differs where v1.14 changed the rule: check the source under v1.14;
   - differs where the rule is unchanged: check the source (a regression, or an earlier review error);
   - omitted or inserted: check completeness.
4. **Port batch.** For the items a reviewer accepts, a prepared edit batch in the edit API's format. The team never applies it. Austin applies it, or has it applied at his command, as one attributed revision after the rebase (§13, gate 11).

The tools open SQLite only through `mode=ro` URIs; a test asserts it.

Demonstrate MIG-T on existing data only: build the registers for all eight deals, and run the aligner and triage on the two pilots against their working copies. The pilots are superseded drafts, so this tests the tool, not a migration.

### 7.10 P: analysis contract and derive tool (D22)

**Contract.** Write `ANALYSIS_CONTRACT.md` (version 0) in this folder. For each variable: its source columns, its derivation, and its status, either mechanical or a switch awaiting Alex. Start from audit D §3.3 (the map from Alex's columns to the ledger) and D §4 (the contract outline). It covers:
- sample: Auction screen, Whole-company bids, and Meredith as descriptive only (`RESEARCH_QUESTIONS.md`);
- bidder units (E3), whole-company scope (D7) and Other-scope rows;
- live counts, exact or as bounds, parsed from Count and the Note's "Count: …" prefix;
- rounds, finality and deadline classes, one per due date:
  - Enforced: hard;
  - Extended and `Extended (late bid accepted)`: extended;
  - `Late bids accepted` (v1.13.2, or legacy in v1.14): extended, flagged `legacy`;
  - Passed without action: soft;
  - Unclear: missing;
  - No deadline stated: no deadline;
  - blank: not reached;
- bid observations and prices: upfront, and package = upfront + CVR/earnout value; Stock % to `all_cash` (1 if 0; 0 if above 0 or Part stock; missing if Not stated or Varies);
- the Formality readings, each computed, none the default. A bid whose recorded Formality is Unclear is missing under every reading:
  - T0: Formality as recorded;
  - T1: Formal if T0 is Formal and Conditions is not Heavy, otherwise Informal;
  - T1u: Formal if T0 is Formal and Conditions is None or Light, otherwise Informal;
  - T2: Formal if T0 is Formal and Price low equals Price high, otherwise Informal;
  - T3: Formal if T0 is Formal and the round's Finality is Announced as final or Inferred final, otherwise Informal;
- the switches, none with a default: the five of D22, plus four more that audit D §4 found blocked on Alex. The tool emits each variant side by side:
  - whether eligible but unadmitted bidders count as live;
  - upfront or package as the estimation price;
  - the process initiator;
  - merger-of-equals talks counted or not (D17's alternative map);
- exits: actor, timing and reason, and the map from Exit reason to Alex's drop codes;
- what the ledger cannot supply: Compustat identifiers, shares outstanding, the effective date.

**Tool.** New modules, for example `_dev/tools/derive_analysis.py` and `_dev/tools/compare_alex.py`, with tests. They run offline, never write into the repository's data or the cockpit state, and write only to an `--out` folder the user names.
- **Input:** a ledger workbook, either a raw version or a four-sheet working-copy export. A five-sheet download's Source sheet is read for provenance. A v1.13.2 workbook is accepted with the columns it has: All cash maps to `all_cash`, and the condition-based readings are missing. The manifest records which.
  - Raw versions are read from copies of the version files.
  - A working-copy export is rendered by the cockpit's own code in a temporary root, from a copy of the database made with the SQLite backup API from a `mode=ro` connection. `Workspace` opens its database for writing (`workspace.py:196-201`), so it must never run on the live state.
- **Outputs:**
  - `bids.csv`: one row per whole-company Bid and Bid reaffirmed row, with:
    - its identifying fields;
    - Price low, Price high, the package and `all_cash`;
    - Stock % parsed to bounds;
    - Formality, Conditions, CVR/earnout, CVR/earnout value, Due diligence, Financing, Regulatory, Antitrust and Exclusivity;
    - Inferred and Flag;
    - a `same_price_revision` marker;
    - the readings T0–T3;
  - `other_scope.csv`: the Other-scope bid rows, and the other rows of partial-only parties (a Who whose every bid row is an Other-scope bid), which also go to the review list;
  - `rounds.csv`: per process and round: opening, finality, due dates, outcomes and deadline classes, and the distinct whole-company bidders that bid. It also flags a mismatch with the Rounds line's Bids received, whose leading integer is the whole-company count (§3 D3); a cell with no leading integer is not compared;
  - `participation.csv`: per whole-company unit, its entry, exits, re-entries and group changes, and the live units at each event as bounds, following E14's formula (first entries plus re-entries, less exits and group and process closures). Disagreements with the Rounds sheet go to a review list; the tool never corrects the ledger;
  - `deal.csv`: the Deal facts, with the auction screen parsed per process;
  - `manifest.json`: the tool and contract versions, the input's path and SHA-256, its `ledger_schema` (from S1's helper), any Source-sheet provenance, and warnings.
- **Side-by-side with Alex's coding** (`compare_alex.py`). For deals in `ref/deal_details_Alex_2026.xlsx`, joined through `ref/seed.csv`'s `deal_number`:
  - align bid rows by bidder, price (upfront, or upfront + CVR) and nearest date;
  - report agreement of `bid_type` with each reading, of `all_cash`, of the per-share value, and of `bid_note` codes against Event and Exit reason (audit D §3.3 gives the code map);
  - mark whether each Alex row carries his red-font correction or the earlier Chicago coding. Only nine deals carry his corrections: P&W, Medivation, Imprivata, Zep, PetSmart, Penford, Mac-Gray, Saks and sTec.

  It is a review aid. It is never a target for the instruction (§9.5), and its output never reaches an extraction run. On a held-out deal it runs only at Austin's request (§13, gate 6).

### 7.11 OPS: deploy readiness

- Copy the `ledger-cockpit.service` (with `.d/20-public-origin.conf`) and `ledger-worker.service` unit files from `~/.config/systemd/user` into `_dev/tools/cockpit/deploy/` as reference copies, so they are reviewed and rolled back with the code. Installing any change to them is an optional deploy step (§12, window step 6a).
- Propose, for Austin to apply at deploy, `Environment=TMPDIR=%h/work/tmp` in both units, so per-request check files leave the nearly full root disk.
- Record `CHECKER_VERSION` and a hash of `dist/index.html` in the backup manifest (`backup.py`), which records only `git_head` while the services run uncommitted code.
- Optional:
  - on a 403, the frontend fetches `/api/session` again and retries once, since a restart invalidates the write token of open tabs (`server.py:42`);
  - cache the All deals recheck by slug, revision and checker version (it took 18 s cold on a scratch copy);
  - make a new job without an instruction fail explicitly (`worker.py:253-260`).
- Keep database changes additive (`add_column`), so the old code can read the new database on rollback.

### 7.12 S6: documentation

Audit D §1 lists each stale line with proposed text. Its classes:
- **Now** (D26; written in this checkout):
  - `_dev/HANDOFF.md`: the date; the v1.14 candidate's status (not published, not the default, not deployed); the current state (Alex connected his Claude account on 24 September and has made no run; the services have run the uncommitted tree since 24 September, 22:02 UTC); the test counts at line 18 (207 and others there, against the 25 September baselines in §11; say which runner gives which); thirteen deals and their versions; R01 applied in the Mac-Gray working copy (revisions 6–7), correcting line 32; the eight working copies described as "edited with Astra's help, independently audited, three clusters reverted on 24 September; no deal-level review status set"; the maintenance list; the next work.
  - `_dev/RESEARCH_QUESTIONS.md`: dispositions from §1 (lines 3, 18, 19, 27–31, 33, 37).
  - `_dev/CHRONOLOGY.md`: dated rows for 23–25 September.
  - The root `README.md`: the current-state lines (12, 17) and `lesson/` in the do-not-read list (36).
  - `AGENTS.md:8`: add `lesson/` to the do-not-read list.
  - `_dev/cockpit/README.md` (lines 9, 13) and `_dev/reviews/2026-09-21-mac-gray-pilot/README.md:3`.
  - This folder's `README.md`: status, the deliverables, and lines 7 (which still tells readers to paste the superseded draft) and 28, which the candidate supersedes.
- **Deploy** (applied at §12, window step 9a): `_dev/tools/README.md` (19, 118, 158), which is written in the separate working copy and travels in the deploy patch; and, delivered as proposed text in the report because they lie outside `_dev/tools/`, `_dev/COCKPIT_BUILD.md` (47, 69), the root README (5, 16), HANDOFF (64), the cockpit README (20) and a checker 1.7 line in this folder's README.
- **Release** (§13; delivered as proposed text, and `_dev/tools/README.md`'s lines in the release patch): `AGENTS.md` (12, 14, 16); the root README (14, 15, 23); HANDOFF (5, 46, 48); RESEARCH_QUESTIONS (3); `_dev/tools/README.md` (49, 120); `_dev/COCKPIT_BUILD.md` (73); the cockpit README (42); `_dev/reviews/2026-09-21-datalink-pilot/README.md:3`; the CHRONOLOGY row; the Questions for Alex README when the DOCX is sent.
- **Historical, leave alone:** `_dev/COCKPIT_APP_SPEC.md`, CHRONOLOGY line 42, the 22 September re-extraction README, and `lesson/README.md`.

Describe code that is not deployed as not deployed.

### 7.13 Order of work

- **Wave 1, in parallel:** A1; M; S1 (on the §1 rules); S2 with MIG-C; S3; S7; P (contract, and the tool tested on the pilots and the v1.13.2 extractions); MIG-T (the registers); OPS; S6's "now" lines.
- **Wave 2:** R on A1, then A1's fixes, then S1 and S2 finalized, then R re-runs its §9.1 value-list check against them. A2 once M, R and P's side-by-side are in.
- **Wave 3:** S4 if built; S6's deploy and release lines drafted; the deploy patch and the release patch prepared against the baseline (§12).
- **Final report.**

### 7.14 Report to Austin

At the end:
- the candidate's hash, diff and CHANGELOG;
- R's findings and how they were resolved;
- test results, with the exact commands and counts;
- `MAP_RECHECK.md`;
- the rendered DOCX;
- the location of the separate working copy, a summary of its diff against the live checkout, the deploy patch and the release patch;
- the proposed text for the deploy and release lines outside `_dev/tools/`;
- the `pre-existing/` patches (§0);
- the analysis contract, and the derive tool's output on the two pilots;
- the MIG registers, and the triage demonstration;
- the disposition of every audit finding: done, not adopted, or deferred;
- the root disk's free space;
- the list of open items.

### 7.15 Deferred and backlog

- **Astra §7.3, the two-stage assisted map review.** It conflicts with `_dev/COCKPIT_APP_SPEC.md:198` (a run sees only one instruction and one filing) and `:201` (revision mode is not offered in the app). It would cost about two paid runs per deal. Revisit only if v1.14 runs show map errors that S4 cannot fix.
- **Hand-correcting the pilot versions.** They are superseded drafts. Astra's §7.4 list, together with each deal's reviewed working copy, becomes the review checklist for the next v1.14 runs. There is one working copy per deal, so do not rebase a working copy onto a pilot: that would replace reviewed work (Mac-Gray revision 8, P&W revision 16).
- **Market data (D23).** Alex asked to track the target's share price through the sale process and to measure premiums over it (voice notes on sTec and Meredith). A later join needs:
  - identifiers: deal slug, then `seed.csv`'s `deal_number`, then Alex's `gvkeyT`, then a CRSP PERMNO through the CCM link, with link dates; unmatched deals are flagged, never guessed;
  - dates: per bid, the last trading day before its Sort date; per deal, an "unaffected" reference date whose rule is Alex's decision;
  - the price field, adjustment and currency;
  - shares outstanding for aggregate bids, and net debt for enterprise-value bids;
  - a separate table, never written into the ledger or shown to an extraction;
  - blockers: the data licence and network access (Austin), and the reference-date and share-count rules (Alex).
- **The primary analysis reading and the other D22 switches**: Alex's answers (§5).

## 8. Choices made without asking Austin (he may overrule any)

Items marked *Confirmed (D27)* were put to Austin on 25 September and confirmed as written. The rest remain defaults he may overrule.

**Instruction.**
- **D14 and H2.** *Confirmed (D27).* A stated period of two weeks or more counts toward Heavy only for remaining diligence not described as confirmatory. A period expressly limited to confirmatory work is Light (Astra's reading). Light's "expedited" applies only where H2 does not.
- **D11 and a new date after evaluation.** *Confirmed (D27).* A new due date set after the bids in hand were evaluated is still Extended, as in the draft and consistent with Alex's extension notes. Enforced covers invited improvements with no new date.
- **D15.** *Confirmed (D27).* An exclusivity request made in the same communication as a bid (a first bid, a revision or a reaffirmation) is coded on that bid row, not as two rows (Astra, extended beyond material revisions). For E10, exclusivity is a term, so a later request with no other change is an Exclusivity changed row, never a same-price Bid row.
- **D18.** On Other-scope rows, CVR/earnout value is blank too, and Stock % stays required.
- **Diligence.** *Confirmed (D27).* "Substantive diligence completed", with no statement that none remains, stays Incomplete, as in the draft and the confirmed taxonomy. Astra's Not stated is not adopted.
- **Consequence of D5.** *Confirmed (D27).* A "no financing condition" statement outranks every item of the Contingent list, including a highly confident letter.
- **Concern and H3.** *Confirmed (D27).* A regulatory risk the board or bidder weighs is Concern; it is an H3 obstacle only when the filing states the bid depends on it.
- **Part A wording:** "for the whole company" in item 1, "changes them" in item 3, and "does not change it" in the last sentence.
- **Header.** The candidate carries "v1.14" from the start, not "(candidate)", so the text evaluated is byte-identical to the text published and exported.
- **Alternative structures** *Confirmed (D27).* in one communication stay separate rows, as an exception to "one communication, one row" (Astra wrote "normally"): Bid rows for whole-company alternatives, Other-scope bid rows for partial ones.
- **E5(b)** stays as the convention for where a new process starts; "silence does not prove inactivity" governs individual participants and exits.
- **Scope details under D7.** *Confirmed (D27).* Withdrew covers a switch to a partial offer. Partial-only parties get no exit rows. Proposals of unresolved scope stay Other-scope rows with a Question. Bids received counts whole-company units and names partial bids separately.
- **Merger-of-equals talks (D17).** *Confirmed (D27).* While the sale role stays unresolved, they are Other material event rows and the counterparty does not enter the whole-company contest; the Question gives the alternative map in which it does. This is neither of the options Alex saw on 24 September (A: no rows; B: a sale attempt with the counterparty as a bidder), so §5 says so.
- **Round dates.** A reopened round is dated at the outreach, never at the authorization (D8, Astra). Round 1 keeps the draft's route, which may use the launching decision when outreach followed within about a week. An unannounced round's Round opened row has Inferred = Y.
- **Acquirer type.** The instruction states the values the checker already enforces.
- **An unsolicited bid in a final round** carries that round's number; the final-solicitation route of E11 applies only if it answers that solicitation.
- **A continuing bidder's missed submission** is recorded in the round's Deadline row Note and the Rounds line's How it ended.
- **A package that cannot be split** *Confirmed (D27).* on a compatible basis leaves the price cells blank, with the figure in the Note and a Question if it matters.
- **The target's termination fee** goes in the Note of the row where it is agreed or changed, else of Merger agreement signed.
- **Examples.** A condensed version of §4's table goes into E12, in neutral wording with no phrase or number from a filing. The §9.3 cases that an example mirrors are marked there and are not evidence of generalization.
- **D8's wording.** "Explicit final solicitation" in the first version of this spec is read as Astra's finality rule, since neither E6 text contains another rule.

**Pipeline.**
- **Checker transition.** The legacy `Late bids accepted` value is a warning, not an error, under v1.14 rules, so the pilots stay viewable.
- **`exit.inferred_reason`** does not run on v1.14 workbooks.
- **Optional checker warnings.** The four in S1 change 6 are adopted. Audit A12's "Bid reaffirmed carries Formal and a Flag" is not.
- **Provenance** lives in a fifth sheet on download rather than in Deal facts rows. It now includes the deal's review status (with "edited since" where it applies), because the uncommitted `deal_review` table gives one authoritative status. The working-copy download has a four-sheet option. Version downloads stay raw by default, with the Source sheet as an option, although D20 speaks of "the workbook downloaded": a raw version must stay byte-identical to its hash.
- **Editor.** Free text with suggestions for Deadline outcome, and an "Other…" option on listed fields.
- **Rebase.** Finding judgments carry across a rebase; implementation and verification reset.
- **Analysis tool.** Flat modules under `_dev/tools/`; v1.13.2 input accepted with fewer columns; output only to a named folder; all readings computed and none the default.
- **S4** is included as optional, in place of §7.3.
- **Repository copies.** Astra's spec and recommendation review are copied into this folder unchanged, with the other files of Astra's working folder (`INSTRUCTION_CHANGE_PLAN.md` and `sources/`), so their links resolve here. The one exception is the recommendation review's own name: Astra's links to `RECOMMENDATION_REVIEW.md` point to what is here `ASTRA_RECOMMENDATION_REVIEW.md`.

**Release.**
- **Gate order.** The new checker and cockpit code are deployed before any v1.14 run (gate 3). Under the first version of this spec, runs came before the deploy: they would have been checked by checker 1.6, which rejects `Extended (late bid accepted)`, with permanent results, and reviewers could not have chosen the new value in the editor (audits B1 and D §7).
- **Cockpit draft.** Created from published v1.13.2, so the app's parent diff reads v1.14 against v1.13.2.
- **Exporting the instruction** happens at publication (gate 9), so command-line runs and app runs use the same text.
- **Held-out deals.** Medivation, Zep and Pepco were read while designing the taxonomy, so they are "not used to tune E6–E14", not held out. Gate 5 should add deals nobody read while designing v1.14.
- **Held-out findings** stay in a separate packet that agents writing instruction changes do not read.
- **Gate 0.** The live uncommitted work is committed separately first, so the v1.14 diff stands alone. The deployed code gets its own commit (gate 3a).
- **Gate 11.** Before a rebase, the deal's status is set to In review as a bookmark, not Reviewed, unless Austin has reviewed that working copy: the eight copies were edited with Astra's help and audited, not reviewed.
- **The DOCX** is best sent before publication, so Alex's answers can reach v1.14.

## 9. Acceptance

**9.1 The instruction's consistency (checked by package R)**
- Parts A–F give one definition each of Formality, Conditions, scope, participation, Bid and date applicability. Replaced shortcuts are removed, not wrapped in exceptions.
- D1, the E12 and E13 prose, the examples in §4, the checker's value lists and the cockpit's choices all agree, including Varies on the markers, the CVR value's dependence on Y, and the Deadline outcome values. The one intended difference: the checker still accepts `Late bids accepted` in a v1.14 workbook, with a warning, while the instruction and the choices omit it.
- Unknown is never used as a negative. Regulatory silence is never No concern. Light is reached only by its two routes.
- No text says that a Regulatory Concern, a CVR or exclusivity makes a bid Heavy. Every Heavy example names H1, H2 or H3, including the example at draft line 220 if it stays.
- One evidence and date rule covers price changes, same-price commitment revisions and reaffirmations. No text still says to copy the earlier row's values wholesale, at line 224 or at line 210.
- D7's consequences reach E1, E3, E4, E5, D3, E14 (lines 256, 260, 262–269, 271) and F.1. D10's reach D2 and E14, including lines 257 and 264. D11's reach D3 and E9. D18's reach D1, E1, E13 (lines 245, 247, 251) and F.4.
- The instruction names no deal and uses no figure or phrase from one. Check with grep for the deal names, the replaced figures ("12.10", "49%", "50–75"), and the phrases "terms previously proposed" and "five weeks". It carries no decision number from this spec, and no project-status text. Every change traces to §1, §8 or an item in §3.
- Every §3.1 line is changed or confirmed unchanged in the CHANGELOG.
- The header has its final form.
- Every reference to Part A resolves.

**9.2 Synthetic checker fixtures (automated).** The checker never assigns a Conditions level, so these test consistency rules, not coding:
- Adding CVR/earnout = Y with a value, or an Exclusivity value, to a valid bid row at each Conditions level adds no issue. (Varies on a row with Count = 1 remains an error.)
- Regulatory = Concern passes with Light, Heavy or Unclear, and is an error with None (existing).
- Financing = Contingent with a level other than Heavy is an error (existing). A cohort row with Financing = Varies and Conditions = Unclear passes.
- Antitrust with an incompatible Regulatory value is an error.
- An Other-scope row with Price low, Price high or CVR/earnout value filled is an error under v1.14. v1.13.2 is unaffected.
- The Deadline outcome sets: v1.14 accepts the new set and warns on `Late bids accepted`; v1.13.2 is unchanged.
- A v1.14 inferred exit with a reported reason is not flagged by `exit.inferred_reason`; a v1.13.2 one still is.
- The four optional warnings fire on their cases and nowhere in the stored results except as S1 documents.
- v1.13.2 workbooks, the nine `extraction/` workbooks and the stored v1.13.2 run results all reproduce. The pilots change only as S1 documents.
- The S2 round trip and the S3 download tests pass. Raw bytes are unchanged.

**9.3 Human regression checklist.** Reviewers use this when reading filings. It is never an input to extraction and never a target to tune the instruction against. Claims about quality in general need held-out deals. The cases marked † are mirrored by an E12 example (§4), so they test that the rule was followed, not that it generalizes.

| Case | What must hold |
|---|---|
| Mac-Gray NDA interval | Eventual membership is not proof of eligibility at the deadline |
| Mac-Gray, same-price packages | Bid rows (D13) |
| Mac-Gray and PetSmart deadlines | As M finds under D11. Q7-A predicted Enforced for both; PetSmart's working copy keeps Unclear under v1.13.2's rule |
| Kraton, Party K | A partial alternative is recorded but kept out of whole-company counts, with a Question (D7) |
| Kraton financing † | "No financing condition" gives Committed, with the draft letters in the Note; earlier offers are coded on their own evidence (D5) |
| Kraton and Datalink, admission then letter | As M and Austin decide (D8) |
| Synacor Company E | Leaves the whole-company contest at the 14 December switch; its partial talks continue as Other-scope rows |
| Synacor Company E, five-week request † | An exclusivity period is not a diligence period |
| Synacor and Datalink, renewed outreach | Date of the outreach itself, not the board authorization; not routine contact |
| WDC's June readoption † | Express reference carries the terms and Formality, but not stale diligence status |
| P&W, G&W 26 July | Informal unless it expressly refers back (D9) |
| P&W, G&W's 12 August 2016 bid (#52 in pilot `…38bc24`; in the v1.13.2 workbooks #52 is a different row) † | A process-wide regulatory risk gives Concern; Light is allowed (D3) |
| Penford, later exclusivity request | Its own row; the earlier offer is unchanged (D15) |
| Penford, 4, 13 and 14 October | Threshold; ambiguous (a Question); bid |
| sTec Company D | No exit and no re-entry (D10) |
| sTec Company H | Actor, timing and reason kept separate, with bounds |

**9.4 Software**
- In the separate working copy, with `TMPDIR` under `/home/uctpiaj/work/tmp/v114-scratch/`:
  - unit tests: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s _dev/tools -p 'test_*.py'`. Baseline on 25 September: 199 passing. New tests add to it;
  - HTTP: `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider _dev/tools/cockpit/acceptance/test_http.py`. Baseline: 14 passing;
  - vitest: `(cd _dev/tools/cockpit/frontend && npx vitest run)`. Baseline: 53 cases (counted on 25 September, not run; running writes a cache, so run it only in the separate working copy);
  - the browser suites, through `serve_fixture.py` with a temporary root, where they can run.
- The S1 fixtures, the S2 round trip and the S3 download tests.
- Stored receipts are unchanged.

**9.5 What acceptance is not.** None of these is research acceptance: a clean checker report, exact quotations, label matches, or agreement among reviewers. Keep separate the run's execution status, mechanical validation, source review and the researchers' acceptance.

**9.6 The new packages**
- **S5:** `verify_catalog.py`'s `main()` refuses to overwrite an existing output. In a temporary root with a catalog workbook relocated and `extraction/<slug>.xlsx` removed, the deal lists, its working copy renders and exports, and `verify_catalog` passes.
- **S7:** with `--crosswalk`, `extraction/mac-gray.xlsx` rendered in v1.14 columns with the same content reports no row changes; `extraction/mac-gray.xlsx` against the Mac-Gray pilot reports keyed matches, removals and additions instead of every row. `run_model.py prepare --revise-from` a five-sheet workbook exits non-zero before any model call.
- **MIG-C,** in HTTP tests on a temporary state:
  - a rebase keeps finding judgments and resets their implementation and verification;
  - the rebase dialog's payload lists the counts of revisions, row marks, finding decisions and threads that stop applying;
  - `rev:N` compares and downloads without saving a revision;
  - an orphaned thread reads "on an earlier base (revision N)".
- **MIG-T:**
  - registers exist for all eight deals; per deal, the row list's marks equal the database's (454 reviewed and 66 needs decision on 25 September; re-read at test time);
  - the pilot triage reports a count and the rows for each of the four buckets;
  - the tools open SQLite only through `mode=ro` (a test asserts it), and `workspace.sqlite3`, `catalog.json`, `extraction/` and `_dev/cockpit/state/versions/` hash the same before and after a run with no cockpit save in between.
- **P:** the derive tool runs on both pilots and on a v1.13.2 workbook; every manifest is complete; every Deadline outcome value in them, including `Late bids accepted`, `No deadline stated` and blank, gets a class. The side-by-side aligns all Alex-labelled bids on the two pilots (13 of 13 Mac-Gray, 14 of 14 P&W) and reproduces audit D §3.4's agreement counts. This checks the tool, not the ledgers.

## 10. How this differs from Astra's spec, and why

The reviews behind these points ran on 25 September: four on Astra's spec, one on the first version of this spec, and the four system audits.

**Part A.** Astra's opening dropped:
- the estimation purpose;
- the ranked uses;
- the orientation (one filing, its Background, one row per event);
- the reason for the condition columns;
- the permission to use judgment.

It left references in E and F dangling. It also adopted, through the opening, rules that had not been agreed.

**Exits and valuation.** The current text never claimed that a disappearance reveals valuation. Alex's dropout codes treat exits as evidence about valuation.

**Regulatory.** "Concern forces Heavy" reversed a decision Austin and Alex confirmed together. It would make a signed winning bid, G&W's 12 August 2016 bid for P&W, Heavy over a risk the board found "not materially different" between the two bidders.

**Pipeline.** Several parts of §7 were already done, wrong or too large:
- the P0 checker fixtures and v1.13.2 compatibility already exist;
- the Deal facts provenance rows would break the checker's 17-field rule and let a model fake provenance;
- §7.3 conflicts with the cockpit spec;
- §7.4 overlooked the reviewed working copies, where Mac-Gray's R01 is already applied;
- Package A mixed research approval, a letter to Alex and software work.

**Analysis contract.** Astra made it P1. This spec first put it in the backlog, then brought in a mechanical first version whose research choices are switches for Alex (D22).

**Missing from Astra's spec:**
- that editing code in this checkout goes live, and that the server keeps the old checker until it restarts;
- that runs must come after the deploy;
- the checker version bump, and the checker version stored and shown;
- `ledger_schema` in the payload;
- the cross-schema diff gap, in the cockpit and in `diff_workbooks.py`;
- choice lists that ignore the schema, and an editor that cannot enter multi-part deadline values;
- that a rebase silently drops reviewed work, and a way to move it;
- the stale `verify_catalog.py`;
- `export_repo.py` refusing catalog paths, and the working copies that an overwrite of `extraction/` would break;
- the instruction lines that restate the old rules (§3.1).

## 11. References

| Item | Value |
|---|---|
| Frozen instruction v1.13.2 | `513c8e3e8159e4a6bceccd6ffca32a246302736329a0c7137b64dd3b7ffcd304` |
| 24 September v1.14 draft (base) | `f9595d7413149f86c074f1d4b9ef96a5a24b3d8dd9b6c11061b0bd6e889aea97`; cockpit draft `a4ca26ecfa92`, unpublished |
| Unused cockpit draft | `73f21eb8c09a`, text identical to v1.13.2 |
| 24 September Questions for Alex | `faab1d66d13a1053c2816a8aaed371c3caf49b6733a9005a4e0e949e12ed5220` |
| Alex's voice notes (`ref/alex_voice_notes_2026-08.docx`) | `9ddb0a38f3ffcabdbf7693ced379df3aa8b53a1c4d065990d09d57978af220fb` |
| Astra's spec (copied here) | `32dfe7deb51909781bc5077e08cc115dc0e524c5cdab18e0a40f87d2d5fc58be` |
| First version of this spec | `477be57f05c130a10f15961616fa22e958950e2b0c6dab5ae47f464fb76fd330` |
| System audits, 25 September | [A](systemic-audit/A_checker_tools.md), [B](systemic-audit/B_cockpit.md), [C](systemic-audit/C_instruction_cascade.md), [D](systemic-audit/D_docs_release_research.md) |
| Pilot versions | `mac-gray/opus55-medium-20260924-2241-d7d267`; `providence-worcester/opus55-medium-20260924-2241-38bc24` |
| Latest working-copy revisions, 25 September | Mac-Gray 8; P&W 16; PetSmart 2; sTec 1; Penford 2; Synacor 1; Kraton 4; Meredith 4; Datalink none |
| Row marks in the eight working copies | 454 reviewed, 66 needs decision, on all 520 Deal ledger rows (audit E; audit B's 434 was wrong); the `deal_review` table is empty |
| Spec review, 25 September | [E](systemic-audit/E_spec_review.md), on the first draft of this system spec; its findings are applied here |
| Test baselines, 25 September | unit 199 passing; HTTP 14 passing; vitest 53 cases (counted) |
| Live services | `ledger-cockpit`, `ledger-worker` and `ledger-backup.timer`, running from this checkout; the two services restarted 24 September, 22:02 UTC |
| Root disk | 97% full, 341 MB free, on 25 September |

Alex's August Q&A is not in the repository's tracked files. Its local copy is this folder's `sources/2026-08-10_QA-dialogue-consolidated_v2.docx` (from Dropbox `Bids_Extraction/alex_submission_2026-08-07/`); `sources/qa.txt` is a text extract of it. D7 and D20 cite it, and A2's case appendix needs it. `sources/` holds evaluation material: nothing in it may reach an extraction run.

## 12. Deploy checklist

On Austin's order only. Adapted from audit B §3, which gives the reasoning. `$LIVE` is `/home/uctpiaj/work/Projects/sec-extraction`.

**Before the window, in the separate working copy:**
1. Confirm that the live `_dev/tools/` has not moved since the baseline was taken:
   `diff -r --exclude node_modules --exclude __pycache__ --exclude dist <baseline> $LIVE/_dev/tools` must print nothing. If it prints anything, merge those changes first.
2. Run every suite in §9.4 and the tests of §9.6.
3. Build the frontend in the working copy (`npx vite build`), which writes its own `dist/`.
4. Change the checker paragraph of `_dev/tools/README.md` (line 19) from "not deployed" to "deployed <date>".
5. Make two patches with `git diff --no-index --binary` from the baseline to the worktree's `_dev/tools/`, comparing copies of both trees without `node_modules`, `__pycache__` and `dist/` (a plain `diff` cannot carry binary fixtures). Check that the patch paths apply from `$LIVE` (adjust with `-p<n>` and `--directory=_dev/tools` if needed):
   - the **deploy patch:** everything except the D25 path changes in `import_results.py` and `verify_catalog.py` and the release-class lines of `_dev/tools/README.md`;
   - the **release patch:** only those, applied at gate 12.

   The built `dist/` travels separately.

**The window** (away from 03:30 UTC, when `ledger-backup.timer` runs):
1. **Nothing is running.** The machine has no `sqlite3` command, so use Python, read-only:
   ```
   python3 -c "import sqlite3; c=sqlite3.connect('file:$LIVE/_dev/cockpit/state/workspace.sqlite3?mode=ro', uri=True); print(c.execute(\"SELECT kind, state, COUNT(*) FROM jobs WHERE state IN ('queued','preparing','running','checking','importing','waiting_for_code','completing','waiting_for_approval') GROUP BY kind, state\").fetchall())"
   ```
   It must print `[]`, and `pgrep -af run_model.py` must print nothing. Austin confirms that he and Alex have saved their work and closed their cockpit tabs. The team does not contact Alex.
2. **Disk:** `df -h / /home/uctpiaj/work`.
3. **Backup:** `python3 _dev/tools/cockpit/backup.py create`; note the path. Optionally `backup.py rehearse`, which must exit 0.
4. **Baselines,** in `~/work/archive/v114-deploy/` (not a temporary folder, so a clean-up cannot remove them): save `curl -s http://127.0.0.1:8778/api/deals` to `~/work/archive/v114-deploy/pre-v114-deals.json`, and the SHA-256 of every `check.json` and workbook under `_dev/cockpit/state/versions/`, of `extraction/*.xlsx`, `catalog.json` and the frozen instruction, to `~/work/archive/v114-deploy/pre-v114-hashes.txt`.
5. **Rollback copy:** `tar czf ~/work/archive/v114-deploy/pre-v114-tools.tgz --exclude=node_modules --exclude=dist _dev/tools`.
6. **Apply the deploy patch** to the live checkout from `$LIVE` (`git apply --check`, then `git apply`, with the path options found in step 5).
   - 6a. Only if Austin approves: install the changed unit files (for example `TMPDIR`, §7.11) and run `systemctl --user daemon-reload`.
7. **Restart the server:** `systemctl --user restart ledger-cockpit.service`. `journalctl --user -u ledger-cockpit -n 20 --no-pager` must show `ledger cockpit -> http://127.0.0.1:8778` and no traceback.
8. **Swap `dist/`,** after the server restart so that the new frontend never talks to the old API: copy the new build to `dist.new/`, then `mv dist dist.old && mv dist.new dist`.
9. **Restart the worker:** `systemctl --user restart ledger-worker.service`; the journal must show "cockpit worker started".
   - 9a. Apply the deploy-class documentation lines outside `_dev/tools/` (S6), from the report's proposed text.
10. **Smoke tests,** over loopback with GET requests only (they are attributed to `local`; do not POST):
    - `/api/session` answers;
    - `/api/deals` lists the same deals; every v1.13.2 version shows the same errors and warnings as before; the pilots differ only as S1 documents. The first call may take about 20 seconds;
    - `/api/deal/mac-gray?version=working`: `ledger_schema` is `v1.13.2`, and the checker version is 1.7;
    - the same with the Mac-Gray pilot's version: `ledger_schema` is `v1.14`, and the Deadline outcome choices include `Extended (late bid accepted)` but not `Late bids accepted`;
    - the working-copy download has five sheets and a correct Source sheet; `?source=0` has four;
    - a version download's SHA-256 equals the version's;
    - compare from the working copy to the pilot shows both `All cash` and the v1.14 columns;
    - `sha256sum -c ~/work/archive/v114-deploy/pre-v114-hashes.txt` is all OK;
    - Austin, on the public URL after a hard reload: the Review tab shows the checker version, and the pilots show "checker 1.6" for their stored results.
11. **Austin tells Alex to reload** any open tab, and reloads his own: a restart changes the write token.
12. After acceptance, remove `dist.old`. Keep the backup and the tarball for at least 14 days.

**Rollback.**
- Code: `mv dist dist.bad && mv dist.old dist`; restore `_dev/tools` from the tarball; restart `ledger-cockpit`, then `ledger-worker`. Versions imported under 1.7 keep their 1.7 receipts, which is correct: versions are immutable.
- Data, only if something damaged the state: stop both services; `python3 _dev/tools/cockpit/backup.py restore <backup> --state _dev/cockpit/state --replace`, which moves the current state aside; start both services. Anything saved after the backup is lost.

## 13. Release procedure and Austin's gates

Each gate is Austin's decision or command. "The team" means agents acting on his command.

0. **Commit the live uncommitted work separately** (the checker 1.6 taxonomy work, the deal-review status feature, `dist/` and the docs), so the v1.14 diff stands alone. Stage explicit paths. For files the team has since edited, stage the saved `pre-existing/` patches with `git apply --cached` instead of the whole file. Stage `lesson/` only if Austin decides to.
1. **Accept** the candidate text (after R), `MAP_RECHECK.md` and the team's report.
2. **Decide with Alex** whether the pilot condition review, which the 24 September handoff made a gate before publishing, still applies or is replaced by the review at gate 6.
3. **Deploy** S1, S2 with MIG-C, S3, S5's catalog lookup change, and any finished S4, S7 and OPS code (§12). This comes before any v1.14 run.
   - 3a. At a commit Austin requests, commit the deployed code and its documentation lines by explicit paths, separately from the instruction export.
4. **Create the cockpit draft,** in person in the app: "New draft from" published v1.13.2, paste the candidate, save. The team confirms that the draft's SHA-256 equals the candidate file's.
5. **Command a bounded set of blind runs**: which deals, engine, effort and budget. For scale: nine Opus 5.5 medium runs cost $27.69, and each pilot about $2.80.
   - Include deals nobody read while designing v1.14. Imprivata is one; add fresh deals from the seed if possible. Medivation, Zep and Pepco were read while designing the taxonomy (REVIEW_FABLE, TAXONOMY_DRAFT3–5), so call them "not used to tune E6–E14", not held out. Zep's and Imprivata's v1.13.2 runs were at xhigh effort, not medium.
   - The team copies each run's receipts from `_dev/cockpit/state/versions/<deal>/<id>/` to a review packet: the state is ignored by Git, and `export_repo.py` copies only workbooks.
6. **Review the runs:** MIG triage for the eight reviewed deals, §9.3, `diff_workbooks.py --crosswalk`, and P's tables as a review aid. Keep the held-out deals' review findings in a separate packet that agents writing later instruction changes do not read. Run `compare_alex.py` on a held-out deal only at Austin's request; Alex's corrected coding is a third reader there, not the answer.
7. **Settle the text.** If it is unchanged, publish this draft. If it changes, make a new draft and rerun the affected deals, or accept an unevaluated difference.
8. **Send the DOCX** to Alex, best before gate 9, so his answers can reach v1.14.
9. **Publish** as `v1.14` and **make it the default,** in person in the app. At the same time, at a commit Austin requests:
   - export the instruction: `python3 _dev/tools/cockpit/export_repo.py instruction v1.14` (a dry run, showing `513c8e3e… -> <sha>`), then with `--write`, then check the hash;
   - update the release lines of S6, including AGENTS.md:12 ("the working instruction (v1.14, frozen; exported on <date> from the cockpit's published `v1.14`, SHA-256 `<sha>`) …") and :16 (the v1.14 decision record);
   - add the CHRONOLOGY row: "<date> | v1.14 published in the cockpit as `v1.14` (id `<id>`, SHA-256 `<sha>`) by <person> and made default by <person>; exported to `SEC_Deal_Ledger_Extraction_Instruction.md` at Austin's request | Decisions D1–D26 of 25 September; consistency review R; checker 1.7 and cockpit S2/S3 deployed <date>; <n> evaluation runs, reviewed against the edited v1.13.2 working copies; provisional decisions sent to Alex <date or not yet> | V114_SPEC, packet <…>".
10. **Re-extract** the remaining deals. Runs from gate 5 on the same text already count. Redo the two pilots, which ran on the 24 September draft.
11. **Move reviewed work, deal by deal (D24).** For each deal whose v1.14 run passed review:
    1. set the deal's review status to In review, as a bookmark that records revision N. Set Reviewed only if Austin has reviewed that working copy: the eight copies were edited with Astra's help and audited, not reviewed;
    2. download the working copy with its Source sheet, and note the revision in HANDOFF;
    3. rebase onto the v1.14 run;
    4. apply the MIG port batch as one attributed revision (Austin, or at his command);
    5. re-review what the triage marked.

    To undo a rebase, restore the pre-rebase revision N, not revision 0: revision 0 returns to the catalog base. Datalink has no reviewed edits and can be rebased freely.
12. **Update `extraction/` (D25),** in one commit Austin requests, with S5's catalog lookup change already deployed (gate 3). Check the jobs table as in §12, then stop both services for steps 1–5:
    1. `git mv` the nine v1.13.2 workbooks, bytes unchanged, to `_dev/reviews/2026-09-22-opus55-reextraction/workbooks/`;
    2. repoint their catalog paths, keeping the id `opus55-medium`, the SHA-256 and `instruction_version: v1.13.2`;
    3. apply the release patch (S5's `import_results.py` and `verify_catalog.py` changes, and the release lines of `_dev/tools/README.md`);
    4. export the v1.14 runs: `export_repo.py deal <slug> --version <id> --write`;
    5. run the tests and the fixed `verify_catalog.py`, take a backup, and start both services;
    6. Austin decides whether the repository copies also become catalog entries;
    7. update AGENTS.md:14 and the other release lines of S6 that describe `extraction/`.

    The four added deals stay in the cockpit only unless Austin decides to export them, which would make them repository development deals.
13. **Records.** Commit this folder, or write `_dev/DECISIONS_v1.14.md` as the decision record. Decide whether `lesson/` is committed.
