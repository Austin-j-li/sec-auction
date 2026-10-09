# Status

Version 1, 28 September 2026. This is the only status record. Records from before the 27 September reset are not current guidance.

## State

- **Instruction:** [Version 1](../SEC_Deal_Ledger_Extraction_Instruction.md), SHA-256 `3f67be55…01252`, approved by Austin on 28 September 2026; D5's "mixed" Initiation amended on 8 October 2026 (the target must move first); E10 and E12 amended on 9 October 2026 (a return to an older price is a revision, not a Same offer; a time limit on an offer never triggers H3). The 28 September text had SHA-256 `05d8668d…05de4`, the 8 October text `87f4efdc…61054`. The live cockpit has only the 28 September text; publish the amended text there after the next release. Every rule traces to a ruling in the [decision log](alignment_sprint/DECISIONS.md) (27–28 September, rulings 1–9; 8 and 9 October); the [change map](alignment_sprint/draft/CHANGE_MAP.md) links each clause to its ruling. The build, its reviews and fixes are in [BUILD_REPORT](alignment_sprint/BUILD_REPORT.md), [BUILD_REVIEW](alignment_sprint/BUILD_REVIEW.md) and [VERSION1_REREVIEW](alignment_sprint/VERSION1_REREVIEW.md). Changes need Austin's approval and must be general.
- **Extractions:** 12 Version 1 runs in the cockpit, one for each deal (Opus 5.5 medium, 28 September 2026). None is exported, and `extraction/` is empty. The eight deals are to be re-extracted under Version 1 on Austin's command, by default with Opus 5.5 at medium effort, and compared with Alex's workbook. Report agreement on codings produced by single-deal rules separately (ruling 9: Synacor round 4, Penford A, PetSmart October 3, sTec rounds and processes, WDC June 10, Datalink August 16 and round 5, Penford July 17, Kraton J; 9 October: Imprivata Sponsor B). Only a held-out test on deals not used in drafting measures generalization.
- **Cockpit:** live since 28 September 2026 at https://lines.dealextract.org, from the detached deployment worktree `~/work/Projects/ledger-live`, now at `9f0750e` ([switch-over record](alignment_sprint/SWITCHOVER.md#deployment-record-28-september-2026); redeployed 29 September to add GPT-6.1-Sol). Version 1 is its only instruction and the default (seeded, attributed to "System"). 13 deals, each with one Version 1 version from 28 September; 12 after the next release, which drops Meredith from the deal list (its rows stay in the database and the backups). Identity comes only from verified Cloudflare Access tokens, loopback included (`COCKPIT_REQUIRE_ACCESS=1`). The old app, its checkouts and its nightlies are deleted; there is no rollback. Nightly backups go to `~/backups/ledger-live/`. Source changes are made here in `sec-auction` and reach the app only by moving the deployment worktree to a new commit and restarting the three units.

## Open

- **Questions for Alex:** none (decision log).
- **Filing readings left open** ([round map](alignment_sprint/draft/ROUND_MAP.md)): Datalink A's March 29 proposal as a range or CVR (W51), Synacor H on November 2, PetSmart Bidder 3's exit, Kraton's post-publicity signer, Datalink A and the July 18 due date. The rules give no single answer; no rule was added for them.
- **Later tests:** Part C's paragraph-by-paragraph reread (cost against extra coverage).
- **Deferred:** price-normalization inputs (O5), the filing link written by the runner (O7), regulatory risk and Heavy (F8).

## Settled rulings (do not reopen)

The decision log is the full record. The rulings most often misread:

- **Meredith:** dropped from the project by Austin on 9 October 2026. Its filing, catalog entry and seed row are removed; the dated records keep its earlier rulings.
- **sTec Company H:** dropped by the target by May 16; the reason is "would not improve earlier offer".
- **Non-submitters:** a bidder asked to bid by a due date that has not bid by then exits at the due date (Did not submit), whatever it says about still considering, unless the target considers its late bid, admits it, gives it more time or asks it for an offer before the next round opens (rulings 1, 5, 6). Providence & Worcester has 16 inferred non-submitters (Party A plus a cohort of 15); Mac-Gray has 16 unnamed financial signers, closed by July 23.
- **Time limits:** a time limit on an offer (an expiry, or a demand to sign or announce by a date) never triggers H3; the Note gives it (9 October 2026).
- **Not invited:** a bidder left out of a stage exits when it opens, unless the target did not tell it it was out and asks it for an offer before the stage ends (rulings 7, 8).
- **Commitment-only changes:** a change in the bidder's commitment is a Bid row. Without a newly stated price, the price cells stay blank. Target termination fees go in dated Notes.
- **Same offer and conditions:** copy an offer when the bidder says it stands, or when, after definitive negotiation begins, the bidder confirms it by its own revised draft of the merger agreement (F2, which replaced "only when the bidder says it stands"). A return to an older price is a revision, not a Same offer (9 October 2026). The evidence window for conditions runs to the bidder's next bid, exclusivity, exit, signing or process-only request, and includes forecasts. "Not begun" uses the NDA test.

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

- **Where work happens:** the Claude Code project "sec-auction" at claude.ai/code. Its threads start from `extraction-v2`, work on their own branches and open pull requests; Austin merges them. Project setup: [CLOUD_PROJECT.md](CLOUD_PROJECT.md). GitLab, the laptop checkout and `local-recovery-2026-09-27` are retired.
- **The VM** (`~/work/Projects/sec-auction`) keeps the live cockpit, paid extraction runs, Codex and the backups. Cloud threads reach it through the protected ARC connection (`arc exec condenser`). Deployment stays in the same cloud task; follow [CLOUD_DEPLOYMENT.md](CLOUD_DEPLOYMENT.md). Remote Control remains optional.
- **Comparison runs:** the 28–29 September runs are recorded in [model_comparison_2026-09](model_comparison_2026-09/README.md). Their run folders are deleted.
