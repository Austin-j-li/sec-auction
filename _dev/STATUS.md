# Status

Version 0, 27 September 2026. This is the only status record. Older records were deleted in the v0 reset and are not current guidance.

## State

- **Instruction:** [v0](../SEC_Deal_Ledger_Extraction_Instruction.md), SHA-256 `cbb1f35c…96ce`. It is not yet aligned with Alex (next section). Changes need Austin's approval and must be general.
- **Extractions:** none. `extraction/` is empty. All nine deals are to be re-extracted under v0 on Austin's command, by default with Opus 5.5 at medium effort.
- **Cockpit:** runs on the VM, reachable again since 27 September evening (see Operational below). This checkout has no cockpit source; the app code is on branch `vm-live-2026-09-26`. The app still has its earlier instruction versions and working copies; they predate v0.

## First task: align the instruction with Alex

Following the instruction does not make a coding research-correct where the instruction departs from Alex's stated conventions. The [alignment audit](ALEX_ALIGNMENT.md) lists these departures and gives a six-discussion work order. It is an audit, not an approved amendment. Resolve each departure as a general definition, then amend the instruction with Austin's approval.

Austin's rulings to build in:
- **Kraton rounds** (27 September, 13:48 UTC): follow Alex's three rounds, with July 6 opening the second informal round. The current round rule (a repeated improvement request continues a round, and an offer-less selection opens none) conflicts with this. Reconcile the rule generally, not case by case.
- **Announcement Count:** clarify the Count wording on announcement rows in the next general revision.

Items raised by the audit, to check against the filings:
- **Mac-Gray:** Alex opens the second informal stage on July 25.
- **sTec:**
  - Alex sees two processes.
  - He does not treat the activist as the initiator.
  - He judges the May 3 deadline soft.
- **Mandatory human-verification flags:** Alex's list (voice notes ¶169–178) is not implemented by the current five-question ceiling.
- **Non-invitation versus exclusion**, and the missing market-price / EV-normalization work.

## Open with Alex

- **Round and finality convention.** sTec: Alex calls the May 16 letters the start of "round two of informal bidding" (voice ¶124). He says the May 28 Formal bid is not in the final round (¶125). He does not say when the final round starts. His older collection instructions (p. 8) allow a final round of informal bids. Keep stage numbering, finality and bid Formality separate.
- **Conflicting reference sources.** What governs when his spring hand coding and his later voice notes disagree? Examples: sTec finality, and the departure of Providence & Worcester's Party A. Recommendation, not approved: an agreed convention governs; filing facts are checked against the filing; conflicting readings go to Alex, and neither reference is treated as ground truth.
- **Working conventions to confirm:**
  - financing commitments
  - partial bidders
  - round triggers
  - merger-of-equals talks
  - price-only revisions
  - the condition evidence window
  - missed due dates and deadline outcomes
  - the process-boundary test (a reported end, or 90 days of silence)
  - Penford Party A's valuation statements of October 4 and 13, against its October 14 $16 bid

The earlier questionnaire was deleted in the reset and was never sent. A new one needs Austin's authorization to send.

## Settled rulings (do not reopen)

- **Meredith:** use economic scope before the transaction-related separation (NMG plus LMG). LMG proposals are therefore Other-scope bids: reported amounts go in the Note, and price cells stay blank. Parties that bid only partially get no exit rows. Meredith is excluded from structural estimation and kept for descriptive and reduced-form work (`DESCRIPTIVE_ONLY` in `derive_analysis.py`). Sources: filing p. 59; voice ¶95, 97, 184.
- **sTec Company H:** dropped by the target by May 16; the reason is "would not improve earlier offer".
- **Non-submitters:** Providence & Worcester has 16 inferred non-submitters (Party A plus a cohort of 15). Mac-Gray has 16 unnamed financial signers, closed by July 23. Reconcile named parties and cohorts.
- **Commitment-only changes:** a change in the bidder's commitment is a Bid row. Without a newly stated price, the price cells stay blank. Target termination fees go in dated Notes.
- **Same offer and conditions:** copy an offer only when the bidder says it stands. The evidence window for conditions runs to the bidder's next bid, exclusivity, exit or signing, and includes forecasts. Invitees left out of the next stage exit when it opens. "Not begun" uses the NDA test.

## Choices for estimation (not blockers)

Alex asked to record procedural Formality and conditionality separately and reinterpret them during estimation (voice ¶19–20, 47–49). `derive_analysis.py` computes the variants with `default: None`.

- **Primary Formality reading:**
  - T0: recorded Formality
  - T1: Formal and not Heavy
  - T1u: Formal with None/Light conditions only
  - T2: Formal with a single price
  - T3: Formal in a final round

  Compare them as robustness checks. Do not choose by best fit to hand-coded deals.
- **Inferred exits:** treat them as dropouts, or as censored observations.
- **Inferred counts:** use them as recorded, with or without a robustness check that sets them aside.

## Operational: the VM is back (27 September, evening)

- The VM was reachable again on 27 September. Nothing changed there after 26 September 20:52 UTC ([reconciliation](alignment_sprint/VM_RECONCILIATION.md)). The app still runs v1.14.1 as its default, whose text is v0's apart from the title.
- Its uncommitted work is archived on branches `vm-live-2026-09-26` (the live checkout the services run from) and `vm-v114-2026-09-26`. Backups are in `~/backups/` on the VM. The live files were not changed.
- Version 1 is to be built on the VM per [BUILD_SPEC.md](alignment_sprint/BUILD_SPEC.md), on branch `version-1`. The app is rebuilt from the archive and wired to the new tools, then restarts on a fresh catalog at a switch-over Austin orders. Development moves to the VM; this laptop checkout is retired after the handoff.
- Correction to the earlier list: the v0 checker does not reject v1.14 or v1.14.1 ledgers, which have the same 29 columns. It checks them under v0 rules: correctly for v1.14.1, wrongly without warning for the 24 September v1.14 drafts. v1.13.2 ledgers get a column error and many knock-on errors. Dropping the v0 tools into the live app would break every deal page, the check step of every run, editing and Add Deal ([lane D](alignment_sprint/vm_check/lane_D_ops.md)).
- Withdrawn VM handoff gates: `export_repo.py instruction v1.14.1 --write` (it would overwrite the instruction file), gate 12 (moving the extraction workbooks), and rebasing working copies onto v1.14.1 runs.
