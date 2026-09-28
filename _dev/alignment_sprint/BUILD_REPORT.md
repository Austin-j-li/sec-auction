# Version 1 build report

27 September 2026. The Version 1 draft, tools and development cockpit are built on `version-1` in `~/work/Projects/sec-auction`. The required checks pass. This is the build handoff in BUILD_SPEC section 8; it is not publication, deployment or research acceptance. No extraction was run.

## What was built

| Deliverable | Result and where to read |
|---|---|
| Instruction | [Version 1 draft](draft/SEC_Deal_Ledger_Extraction_Instruction.md), retaining the 29-column/four-sheet contract. The protected root instruction remains Version 0. |
| Decision trace | [CHANGE_MAP](draft/CHANGE_MAP.md): all 41 R/F/P/O themes, evening rulings, C1–C18, both directions of clause mapping, reconciliations and every cockpit adapter. |
| Source application | [ROUND_MAP](draft/ROUND_MAP.md): all nine deals, every derive cell, fixed process/round anchors and retest anchors, with unresolved alternatives visible. |
| Workbook comparison | [WORKBOOK_CHECK](draft/WORKBOOK_CHECK.md): all 321 relevant event rows and all 123 Formal/Informal rows in Alex's nine deal ranges; differences, agreements, missing events and unavailable fields are distinguished. |
| Tools | Version 1 checker and editor choices; Q/R validation; updated count, condition, deadline and formality checks; analysis updates; eleven independently switchable review-queue categories; filing index links. Tests accompany these changes. |
| Cockpit | Restored the VM archive's app, adapted it to the current tools, rebuilt the frontend, and removed old rules selection. Pending catalog deals, mixed initiation, R links/save/rename/delete and checker labels work. A deal's first successful imported run becomes a persisted base, including when runs finish out of order. |
| Fresh state | [`fresh_state.py`](../tools/cockpit/fresh_state.py) reads the source through a read-only SQLite backup, retains account metadata and added deals with verified filings, and publishes into an absent destination. Old work, instructions/defaults, comments and jobs do not carry over. External provider credentials retain their existing location. |
| Later deployment | [SWITCHOVER](SWITCHOVER.md) covers a separate approved deployment worktree, job/runner drain, backup/archive, fresh state, frontend, service drop-ins, TMPDIR, smoke checks and rollback. No step was executed. |
| Check evidence | [CHECK_REPORT](draft/CHECK_REPORT.md) records instruction checks, the hand-made workbook, independent reviews, suites, copied-state rehearsal and operational boundaries. |

The instruction's SHA-256 is `01110a1af35a0a3a4afaf0a2d2e77b67ce5f4cccf573356679cecef346825ee3`. It has 395 lines, seven synthetic examples and no named deal or researcher in its rules. The change map covers all 86 nonblank added/replaced lines and checks 197 line references.

GPT team work followed the explicitly requested Codex model-team skill. Astra handled drafting, source judgment and independent reviews; Sol implemented the tools, backend, frontend and state-copy script. No worker ran an extraction or committed independently.

## Tests and rehearsal

| Check | Final result |
|---|---|
| Entire Python tree: `PYTHONUSERBASE=~/work/.local python3 -m pytest _dev/tools -q` | **358 tests and 229 subtests passed**, 110.13 seconds. |
| HTTP acceptance | **22 passed**, included in the Python total; also run separately. |
| Frontend vitest | **77 passed in 8 files**. |
| Headless core, deals, instructions, runs and trace suites | **138 checks passed**: 63, 25, 24, 12 and 14 respectively. |
| Browser resize and responsive suites | Passed; **7 responsive widths** checked. |
| Production frontend build | Passed. |
| Pending catalog verification | **9 of 9 passed**, with filing hashes checked and no old workbook base or review packet. |
| Hand-made Version 1 workbook | **0 errors, 0 warnings, 0 information items**. Wrong signing Count and required-exclusivity/None mutations each produced the expected error; restoring them restored the clean result. |
| Instruction and reports | Decision/reverse coverage, labels, rule references, fixed anchors, prohibited-name/history wording, report coordinates and whitespace checks passed. |

Browser commands are the seven `node _dev/tools/cockpit/acceptance/test_*.mjs` entry points: browser, deals, instructions, runs, trace, resize and responsive. Frontend tests/build run in `_dev/tools/cockpit/frontend`. Test run paths use synthetic workbooks and fake provider/runner commands.

The first full Python run produced 357 passes and one failure in a provenance export test. XLSX timestamps made two otherwise equal exports differ as ZIP bytes. The corrected test waits across that boundary and compares every archive member, normalizing only the generated modified-time field. The focused rerun and final full suite pass. Independent reviews also found and closed errors in signing participation/scope, same-day round-opening counts, H-trigger/exclusivity handling, review currency/price coverage and base selection when runs finish out of order. The manual app smoke found blank edited cells lacked wrapping; that was fixed and rechecked. No known failing build check remains.

A read-only online backup of the live WAL database plus its filings supplied the rehearsal. Fresh state retained **3 provider-account records for 2 users, 4 added deals and 4 hash-verified filings**; retained rows matched the snapshot. No provider credential file was opened or copied. Before app initialization only the retained tables existed. Initialization seeded the unchanged root **Version 0** as published/default, as the build spec requires before approval.

The clone's private server ran on `127.0.0.1:8879` against scratch state, with no worker loop. All thirteen deals appeared pending; Datalink and the four added deals opened with filings. Instruction pages and seed search worked. A real Penford EDGAR lookup returned six documents and the index link; only that lookup was processed. A synthetic fourteenth deal was then added only to scratch state to test saving a note, following an R1 flag to Questions and seeing checker Version 1 with zero errors/warnings. The extraction-job count stayed zero. Overview, pending-deal and saved-ledger Review screenshots were inspected. The private server was stopped and scratch state was deleted after recording these results.

## Boundaries and checks not performed

All build changes are in `sec-auction`. Final hashes matched the starting hashes for **125 watched live code/instruction/catalog files**, **8 installed unit/drop-in files**, and the clone's **4 protected files**: root instruction, AGENTS, root README and `_dev/STATUS.md`. No live service or timer was stopped, restarted or edited; live state and backups were not written by this build. The development extraction directory contains no workbook.

The 125 staged files passed a credential-pattern and forbidden-artifact-path scan: no state/database, provider key, private key, credential literal, dependency directory or cache was staged. The four protected files are absent from the staged changes. The private test port was confirmed closed, and the build scratch directory, including the copied live state and filings, was removed.

The following remain untested or deliberately unperformed:

- **Real extraction quality and completion/import.** No model was asked to produce a ledger. Stubs establish engineering behavior, not source accuracy or research reliability.
- **Provider sign-in/refresh.** Existing metadata was copied; external credentials were not exercised. A future live check must verify connection behavior under the users' own accounts.
- **Live switch-over and Version 1 publication.** The runbook was written only. Before deployment, the approved draft must replace the root instruction in a new approved commit. Deploying this build commit would still seed Version 0.
- **Whole-workbook certification.** The comparison covers the required themes and identified ranges. Alex's workbook has no Conditions/process/round/count/review-ID fields corresponding to several new outputs. Missing fields are not agreement.
- **Spreadsheet runtime rendering.** The source reviewer could not access the spreadsheet workspace runtime, so it inspected the existing XLSX read-only using ZIP/XML. The workbook was neither edited nor recalculated. The cockpit's separate synthetic workbook/export paths were tested.

## Items waiting for Austin: instruction and research choices

These are the items flagged in CHANGE_MAP. Their presence does not authorize a rule change or another run.

1. **Part C reread test.** Keep the required paragraph reread in this draft; decide whether to authorize a later comparison of its cost and extra source coverage.
2. **Mixed-initiation Note.** Approve using the Note on the target's first step to record both sides' dated first steps. The case where no round 1 ever opens retains existing wording and is not given an invented rule.
3. **Synacor's January selection.** Decide whether finality resets after the October reopening. Literal current rules give three P3 rounds; a reset would permit a fourth at January 6/7. Both preserve October 27 reopening and December 30 continuation.
4. **Deadline versus continuing interest.** Confirm the case of a bidder still considering participation but neither excluded from a new stage nor supplying an accepted late response. Non-invitation closes participation; the retained no-exit-from-a-missed-date rule is not silently deleted.
5. **Extraction reliability.** Admission decisions, document-confirmation rows and uncapped R items need a separately authorized real extraction comparison. This build cannot settle their variance.
6. **Route 2 timing.** Approve the communication-time reading: a later final letter does not retrospectively turn an earlier bid Formal.
7. **F2 price reference.** Approve referencing the latest price-stating offer when a blank-price commitment revision intervenes before a document confirmation. This does not carry conditions forward.
8. **Penford A's intermediate participation.** Decide whether October 3 non-invitation closes its spell before October 4 re-entry, or continued target interest keeps it live. Its three Informal offers and October 14 final exit remain fixed.
9. **Source and workbook outcomes.** Rule on the alternatives and comparison findings listed next. Neither report changes the draft or Alex's workbook by itself.

## Items waiting for Austin: round-map alternatives

| Question | Applied reading and alternative |
|---|---|
| Penford R1 date | First contacts bounded September 1–9. August 28 requires an outreach-within-seven-days premise not demonstrated by the filing. |
| Synacor early R1 dates | P1 outreach after May 8 through June 20, 2018; P2 after August 25 through October 31, 2019; P3 mid-July 2020 with July 13 lower bound. Earlier NDA dates do not supply the fallback when wider outreach later occurs. July 13 exact versus July 13–19 remains a precision choice. |
| Synacor January round | Three P3 rounds under the existing restriction; four if the earlier finality resets. No reset rule was invented. |
| Penford A's spells | October 3 exit/October 4 re-entry versus continuous participation; the fixed October 14 exit and Informal prices survive both. |
| Late responses and exits | Mac-Gray's September 21 revision as late required response versus improvement; Providence's unnamed latest late arrival; Datalink C's October 20 projection withholding versus definite October 26 exclusivity exit. Preserve bounds/review items where the filing does not settle the question. |

Meredith D's April markup/price linkage (W30) and Synacor H's membership among the NDA entrants (W23) are additional source judgments. They do not have a mechanically checkable answer.

## Items waiting for Austin: workbook comparison register

The following is the complete W01–W47 register. Exact cells, both codings, filing pages and theme IDs are in [WORKBOOK_CHECK](draft/WORKBOOK_CHECK.md). Some entries are already settled departures under later decisions; others concern missing transitions, precision or different schemas, rather than an erroneous workbook value. W01 appears twice in that report for the same five cells and is counted once here.

| ID | Deal | Difference or question to review |
|---|---|---|
| W01 | Kraton | Five September final-stage bids: workbook Informal; draft Formal. |
| W02 | Kraton | J needs July 6 exit/July 19 re-entry before its July 20 exit. |
| W03 | Kraton | Partial-only parties' drop rows are not whole-company exits. |
| W04 | Mac-Gray | Sixteen non-submitters close by July 23, not July 25. |
| W05 | Mac-Gray | July 25 opens a non-final selection stage; workbook marks final informal extension. |
| W06 | Mac-Gray | C's September 18 closure is Did not submit, not an unexplained Drop. |
| W07 | sTec | May 16 is non-final; May 29 opens announced final bidding. |
| W08 | sTec | H is excluded by May 16; May 23 supplies its reason. |
| W09 | sTec | E/F partial scope must be resolved before counting target-eliminated whole-company bidders. |
| W10 | Penford | October 3 is inferred final, not a final invitation to A/C/D. |
| W11 | Penford | C/D non-invitation closes by October 3, not their later report/signing dates. |
| W12 | Providence | Initial 16 are A plus 15 by May 19; do not identify later unnamed non-submitters as A. |
| W13 | Providence | July 27 is inferred final; August 12 is selection/signing, not a communicated deadline. |
| W14 | Providence | F's financing support does not establish a joint E/F bidder. |
| W15 | PetSmart | Adopted stage openings are October 3 and November 3; later letter/marker dates do not replace them. |
| W16 | PetSmart | Fifteen signers minus six submitters leaves nine closures, while workbook supplies eight. |
| W17 | PetSmart | Group combination is a transition; Bidder3's spell ends by December 10, not anew at signing. |
| W18 | Datalink | Two parties not sent final letters close August 16, not September 1. |
| W19 | Datalink | A's March offer is not a new July offer carrying the new bidders' range; cohort counts need reconciliation. |
| W20 | Datalink | B/C have September 2 exits and October re-entry; C's October 20 versus 26 exit remains open. |
| W21 | Datalink | B withdraws October 24, not November 6. |
| W22 | Synacor | Merger-of-equals and partial talks do not bridge whole-company processes or create whole-company exits. |
| W23 | Synacor | H's earlier exclusivity closure depends on supported entry; E's scope switch is December 14, not December 4. |
| W24 | Meredith | Partial/LMG offers do not supply whole-company rounds, counts or exits. |
| W25 | Providence | D/G&W markups and retained-markup revisions make three workbook Informal bids Formal. |
| W26 | Providence | August 4 is a revised draft/confirmation, not execution; diligence remained incomplete. |
| W27 | Penford | October 8 F2 confirmation is additional to October 14; inconsistent date columns are not two events. |
| W28 | PetSmart | Bidder3's about-78 ceiling is Formal and high-only, not an Informal point price. |
| W29 | Meredith | Eight partial bids become Formal through markup/retention/definitive negotiation. |
| W30 | Meredith | D's April 15/23/26/29 Formality depends on whether markup and price answer one qualifying request; keep both readings visible. |
| W31 | Meredith | May 28 is Formal; intervening May 31 conditional and reduced offers cannot collapse into June 2 execution. |
| W32 | Kraton | A's first range is 42–45; response dates are bounded where appropriate; A's 40.50 is September 17. |
| W33 | Datalink | Separate November 1 price 11, November 2 agreement at 11.25 and November 6 signing. |
| W34 | Synacor | I's partial bid is December 8; CLP reaches 2 by January 6, not January 8. |
| W35 | Meredith | D's May 26 price is 16.51, not 15.51. |
| W36 | Meredith | Preserve EV, units and alternatives without invented per-share conversion; schema differences alone do not make EV wrong. |
| W37 | Providence | Preserve actual/bounded arrivals instead of assigning all responses the due date. |
| W38 | Kraton | NDA dates require intervals and scope distinctions, not uniform exact signatures. |
| W39 | Mac-Gray | NDA cohort intervals and named date bounds differ from rough midpoint stamps. |
| W40 | Providence | March 28 outreach is not 25 execution dates; C's signature remains bounded. |
| W41 | PetSmart | First-week-October NDA bounds do not prove fifteen October 7 executions. |
| W42 | Datalink | June 6 begins outreach; it is not every signature date, especially for later financial contacts. |
| W43 | Synacor | NDA interval midpoints are not exact dates; retain partial scopes and supported individual dates. |
| W44 | Meredith | November 16 outreach does not date all subsequent NDA executions; retain partial scope. |
| W45 | PetSmart | July 3 sale-one-option differs from July 10 sale demand; overall activist influence agrees. |
| W46 | Mac-Gray | Preserve the 21.5 package's 19 upfront/2.5 contingent components. |
| W47 | PetSmart | Initial bid dates and B2's revised bid retain source bounds rather than due-day precision. |

Missing-event follow-ups are separate from those same-fact comparisons:

- **Mac-Gray:** October 7 clean F2 confirmation, if distinct from a changed commitment; October 5/8 liability changes are blank-price bids.
- **sTec:** June 20 standstill condition is a single H3 bid with blank price, overriding F2; May 31 withdrawal/June 10 return transitions are absent.
- **Penford:** the October 8 document confirmation is missing as a separate event (W27).
- **Datalink:** September 26/28 and October 8 changed commitments require their own events; do not manufacture unchanged-price confirmations.
- **Synacor:** the first bidder-revised draft is bounded after the January 27 target revision and before signing, not the initial January 21 draft.
- **Meredith:** the first bidder-revised draft after the late-April target drafts and before May 3 signing is bounded; May 31 changed offers remain separate.
- **Kraton/PetSmart:** generic continued drafting/completion does not identify an extra F2 observation. **Providence:** the August 4 event exists; W26 concerns its description and diligence status.

The absent Conditions, process/round totals, signing Count and Q/R fields cannot validate their new counterparts. sTec's omitted 2012 attempt/activist event and Synacor's missing process boundaries are coverage gaps, not contrary workbook process totals. Other comparable agreements are recorded in the source report.

## Stop point

This build is delivered on `version-1`. Publication, replacing the root instruction, updating STATUS/AGENTS/root README, moving `extraction-v2`, deployment, cleanup of retired checkouts and any extraction wait for Austin. The remaining work at this handoff is substantive approval of the flagged choices, not another build or a live change.

## Fix pass (28 September 2026)

Four independent reviews (`BUILD_REVIEW.md`) found no blocker in the draft or the reports and one in the checker. Four Claude Opus 5.5 lanes then applied the fix list and the 28 September rulings (DECISIONS.md, rulings 1–5), each owning separate files; the orchestrator integrated and re-ran the suites. No extraction ran; the live app, its state, services and backups were not touched.

- **Instruction.** The four rulings are applied. Ruling 1 (missed due date, as refined) is stated once, as E14 closing event 3; the due date's outcome lives only in E9 (left as drafted) and re-entry only in the Re-entered rule. The review fixes are also applied: S1 scope guard restored beside Part F; S2 confirmation by documents copies only price and consideration; S4 "to all the admitted parties"; M2–M5; M1 lapses. CHANGE_MAP covers the rulings, marks reconciliations 1, 16 and 17 superseded and settles every earlier flagged item. Its 241 links and 30 plain references were re-verified. Draft: 395 lines, SHA-256 `5264450c019ba4f6a55c419fd229076994bc503aa4b323afd232ac0dd5efbf3a`.
- **Round map and workbook check.** Every fact was re-checked against the filings.
  - Kraton J: Did not submit June 29, Re-entered July 19, dropped July 20. June 29 is Extended (late bid accepted), last July 19.
  - sTec: E and F are whole-company entrants, giving 6 parties. D stays live until it Withdrew June 5.
  - Penford: round 1 August 28, 2014.
  - Synacor: round 1 May 8, 2018, August 25, 2019 and July 13, 2020; process 3 gains round 4 on January 6, 2021; CLP's January 21 draft is a confirmation by documents.
  - Datalink C Contingent (ruling 3). W42 fixed. The register now runs W01–W48, and the 321/123 row counts are unchanged.
  - Remaining open items are readings of the filing, listed in ROUND_MAP.
- **Checker and tools.**
  - The `round.zero_after_opening` blocker is fixed.
  - The signing Count follows derive's rule, and initiation is shared between checker and derive.
  - New warnings: `conditions.none_expected`, `ledger.signing_who`, `exit.did_not_submit_date` and `exit.late_bid_in_round`.
  - A process Question is now required after an inferred round, Rows affected accepts mixed row and event lists, and `review_list.py --output` is guarded.
  - The new tests fail on the old code.
- **Cockpit and runbook.**
  - The server takes a reader only from a Cloudflare Access token verified with `jwcrypto` (`access.py`). It fails closed until `COCKPIT_ACCESS_TEAM_DOMAIN` and `COCKPIT_ACCESS_AUD` are filled in the deploy drop-in at switch-over.
  - Runbook: the drain query includes `timed_out`, and exports go through `export_repo.py --out-root` (refused into a detached deploy folder).
  - Backups now go to `~/backups/ledger-live/`.
  - `fresh_state.py` leaves no `-wal`/`-shm` behind.
  - SWITCHOVER now checks the frontend before the outage, creates the drop-in folders and gives a Version 0 recovery step, and it notes that hidden deals reappear.
  - Cloning an R item keeps an R id.
  - The 27 September `/tmp` acceptance leftovers are deleted.
- **Tests after integration.** Full `_dev/tools` Python tree 374 passed, 246 subtests; vitest 79 passed. The app lane also ran the core browser suite (63), the trace, runs, instructions and deals suites, and the resize and responsive suites; all pass. `git diff --check` is clean.

Still open for Austin:
- Version 1's seeded attribution ("system" vs his account).
- Whether loopback access should require Access (`COCKPIT_REQUIRE_ACCESS=1`).
- A separate fix for the live app's header trust, which this build fixes only from the switch-over.
- The filing-reading items in ROUND_MAP.
- Two orphaned fixture servers from 23 September, started from the live folder (PIDs 2651214, 2807890), are still running. They were left alone.

A re-review of this fix pass comes before approval.
