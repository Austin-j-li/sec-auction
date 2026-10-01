# Status

Version 1, 28 September 2026. This is the only status record. Records from before the 27 September reset are not current guidance.

## State

- **Instruction:** [Version 1](../SEC_Deal_Ledger_Extraction_Instruction.md), SHA-256 `05d8668d…05de4`, approved by Austin on 28 September 2026. Every rule traces to a ruling in the [decision log](alignment_sprint/DECISIONS.md) (27–28 September, rulings 1–9); the [change map](alignment_sprint/draft/CHANGE_MAP.md) links each clause to its ruling. The build, its reviews and fixes are in [BUILD_REPORT](alignment_sprint/BUILD_REPORT.md), [BUILD_REVIEW](alignment_sprint/BUILD_REVIEW.md) and [VERSION1_REREVIEW](alignment_sprint/VERSION1_REREVIEW.md). Changes need Austin's approval and must be general.
- **Extractions:** none. `extraction/` is empty. The nine deals are to be re-extracted under Version 1 on Austin's command, by default with Opus 5.5 at medium effort, and compared with Alex's workbook. Report agreement on codings produced by single-deal rules separately (ruling 9: Synacor round 4, Penford A, PetSmart October 3, sTec rounds and processes, WDC June 10, Datalink August 16 and round 5, Meredith scope, Penford July 17, Kraton J). Only a held-out test on deals not used in drafting measures generalization.
- **Cockpit:** live since 28 September 2026 at https://lines.dealextract.org, from the detached deployment worktree `~/work/Projects/ledger-live`, now at `9f0750e` ([switch-over record](alignment_sprint/SWITCHOVER.md#deployment-record-28-september-2026); redeployed 29 September to add GPT-6.1-Sol). Version 1 is its only instruction and the default (seeded, attributed to "System"). 13 deals, no versions yet. Identity comes only from verified Cloudflare Access tokens, loopback included (`COCKPIT_REQUIRE_ACCESS=1`). The old app, its checkouts and its nightlies are deleted; there is no rollback. Nightly backups go to `~/backups/ledger-live/`. Source changes are made here in `sec-auction` and reach the app only by moving the deployment worktree to a new commit and restarting the three units.

## Open

- **Questions for Alex:** none (decision log).
- **Filing readings left open** ([round map](alignment_sprint/draft/ROUND_MAP.md)): Datalink A's March 29 proposal as a range or CVR (W51), Synacor H on November 2, PetSmart Bidder 3's exit, Kraton's post-publicity signer, Datalink A and the July 18 due date, Meredith D's April markup and price (W30). The rules give no single answer; no rule was added for them.
- **Later tests:** Part C's paragraph-by-paragraph reread (cost against extra coverage).
- **Deferred:** price-normalization inputs (O5), the filing link written by the runner (O7), regulatory risk and Heavy (F8).

## Settled rulings (do not reopen)

The decision log is the full record. The rulings most often misread:

- **Meredith:** use economic scope before the transaction-related separation (NMG plus LMG). LMG proposals are Other-scope bids: reported amounts go in the Note, and price cells stay blank. Parties that bid only partially get no exit rows. Meredith is excluded from structural estimation and kept for descriptive and reduced-form work (`DESCRIPTIVE_ONLY` in `derive_analysis.py`). Sources: filing p. 59; voice ¶95, 97, 184.
- **sTec Company H:** dropped by the target by May 16; the reason is "would not improve earlier offer".
- **Non-submitters:** a bidder asked to bid by a due date that has not bid by then exits at the due date (Did not submit), whatever it says about still considering, unless the target considers its late bid, admits it, gives it more time or asks it for an offer before the next round opens (rulings 1, 5, 6). Providence & Worcester has 16 inferred non-submitters (Party A plus a cohort of 15); Mac-Gray has 16 unnamed financial signers, closed by July 23.
- **Not invited:** a bidder left out of a stage exits when it opens, unless the target did not tell it it was out and asks it for an offer before the stage ends (rulings 7, 8).
- **Commitment-only changes:** a change in the bidder's commitment is a Bid row. Without a newly stated price, the price cells stay blank. Target termination fees go in dated Notes.
- **Same offer and conditions:** copy an offer when the bidder says it stands, or when, after definitive negotiation begins, the bidder confirms it by its own revised draft of the merger agreement (F2, which replaced "only when the bidder says it stands"). The evidence window for conditions runs to the bidder's next bid, exclusivity, exit, signing or process-only request, and includes forecasts. "Not begun" uses the NDA test.

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

## Operational

- **Where work happens:** on the VM, in `~/work/Projects/sec-auction`, branch `extraction-v2` (Version 1 was built on `version-1`). Commit and push finished work to GitHub (`origin`, private) at the end of each session; GitLab is retired. The laptop checkout and `local-recovery-2026-09-27` are retired.
- **Live app:** unchanged since 26 September. Its uncommitted work is archived on branches `vm-live-2026-09-26` and `vm-v114-2026-09-26`; backups are in `~/backups/`. The old folders are deleted a week after a clean switch-over (evening ruling 7).
- **Until the switch-over:** `tools/sandbox/run_model.py` runs the root instruction (now Version 1) and the checker enforces Version 1 only, so the live app's v1.14.1 ledgers are not checked by these tools.
- **Leftovers:** two acceptance fixture servers started on 23 September from the live folder are still running (PIDs 2651214 and 2807890); stop them on Austin's word.
