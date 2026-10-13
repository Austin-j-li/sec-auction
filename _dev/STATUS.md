# Status

Version 1, 28 September 2026. This is the only status record. Records from before the 27 September reset are not current guidance.

## State

- **Instruction:** [Version 1](../SEC_Deal_Ledger_Extraction_Instruction.md), SHA-256 `e6e1e2f3…9eb13`, approved by Austin on 28 September 2026; D5's "mixed" Initiation amended on 8 October 2026 (the target must move first); E10 and E12 amended on 9 October 2026 (a return to an older price is a revision, not a Same offer; a time limit on an offer never triggers H3); Part B, D3 and E12 amended on 12 October 2026 (the condition columns describe the bid at its communication; Who was in counts admitted bidders, not contacts). The 28 September text had SHA-256 `05d8668d…05de4`, the 8 October text `87f4efdc…61054`, the 9 October text `3f67be55…01252`. The live cockpit publishes the 12 October text as "v1.1", its default instruction since 12 October 2026 at 15:35 UTC; the 28 September text stays published there as "Version 1". Every rule traces to a ruling in the [decision log](alignment_sprint/DECISIONS.md) (27–28 September, rulings 1–9; 8, 9 and 12 October); the [change map](alignment_sprint/draft/CHANGE_MAP.md) links each clause to its ruling. The build, its reviews and fixes are in [BUILD_REPORT](alignment_sprint/BUILD_REPORT.md), [BUILD_REVIEW](alignment_sprint/BUILD_REVIEW.md) and [VERSION1_REREVIEW](alignment_sprint/VERSION1_REREVIEW.md). Changes need Austin's approval and must be general.
- **Extractions:** all 12 listed deals now have a fresh GPT-6-Astra xhigh result under v1.1, with Fast service requested. The 12 runs started in parallel on 12 October 2026, from 20:24:55 to 20:25:15 Europe/London. All completed, and all working copies now use their Astra originals at revision 1. The checker reported zero errors and 12 warnings; the cockpit located all 712 ledger quotes. This is mechanical verification, not substantive acceptance. The earlier Opus originals remain unchanged. No workbook is exported, and `extraction/` stays empty. See the [batch record](astra_batch_2026-10-12/README.md). Compare the new results with Alex's workbook in a separate review. Report agreement on rules derived from reviewed deals separately from held-out evidence.
- **Cockpit:** live since 28 September 2026 at https://lines.dealextract.org, from the detached deployment worktree `~/work/Projects/ledger-live`, now at `357bef8` ([switch-over record](alignment_sprint/SWITCHOVER.md#deployment-record-28-september-2026); redeployed 29 September to add GPT-6.1-Sol; released 10 October 2026 at 11:36 UTC from `9f0750e` to `1a2ac17930465944a8f2f11cc16863e76ec61e89`, PRs #1 to #12, backup `~/backups/ledger-live/releases/20261010-113623Z-before-1a2ac17/`, record `~/work/sec-auction-deployment/releases/20261010-113623Z/`; released 12 October 2026 at 15:29 UTC from `1a2ac17` to `a8ecea3d35e57a8c1f6201753f82022318da2ecb`, PRs #13 to #15, backup `~/backups/ledger-live/releases/20261012-152938Z-before-a8ecea3/`, record `~/work/sec-auction-deployment/releases/20261012-152938Z/`). It has two published instructions: "Version 1" (the 28 September text, seeded, attributed to "System") and "v1.1" (the 12 October text, the default since 12 October 2026; published by Claude on Austin's request and recorded under Austin, record `~/work/sec-auction-deployment/releases/20261012-153458Z-instruction/`; Austin renamed it from "Version 1 - 12 Oct 2026" at 15:39 UTC after the backup `~/backups/ledger-live/releases/20261012-153953Z-before-instruction-rename/`; the activity feed keeps the first name). 12 listed deals, each with a 28 September Opus original and a 12 October Astra original; Meredith left the deal list in the 10 October release (its rows stay in the database and the backups). Identity comes only from verified Cloudflare Access tokens, loopback included (`COCKPIT_REQUIRE_ACCESS=1`). Since the 10 October release, a request without a verified reader can read only `/api/session`; every other `/api/` read returns 401. Extraction runs have no network except HTTPS to their model API (Austin, 9 October 2026). The old app, its checkouts and its nightlies are deleted; there is no rollback. Nightly backups go to `~/backups/ledger-live/`. Source changes are made here in `sec-auction` and reach the app only by moving the deployment worktree to a new commit and restarting the three units. The 12 October release at 20:24 Europe/London deployed PRs #18 and #20, with a backup before release. The batch used temporary limits of 12 total and 12 per user. Those limits returned to four total and two per user after completion. See the [release receipt](astra_batch_2026-10-12/release.json).

## Open

- **Cockpit review:** all 12 new Astra working copies are marked In review. Their 12 mechanical warnings appear in the [batch record](astra_batch_2026-10-12/README.md). The earlier ruling records identify rows in the September originals; the new working copies need their own substantive review. The batch does not resolve the separate analytical admission issue from the earlier comparison.
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
- **Same offer and conditions:** copy an offer when the bidder says it stands, or when, after definitive negotiation begins, the bidder confirms it by its own revised draft of the merger agreement (F2, which replaced "only when the bidder says it stands"). A return to an older price is a revision, not a Same offer (9 October 2026). The evidence window for conditions runs to the bidder's next bid, exclusivity, exit, signing or process-only request, and includes forecasts. The columns describe the bid as it stood at its communication; a later change in the window goes in the Note (12 October 2026). "Not begun" uses the NDA test.

## Choices for estimation (not blockers)

Alex asked to record procedural Formality and conditionality separately and reinterpret them during estimation (voice ¶19–20, 47–49). `derive_analysis.py` computes the variants with `default: None`.

- **Primary Formality reading:**
  - T0: recorded Formality
  - T1: Formal and not Heavy
  - T1u: Formal with None/Light conditions only
  - T2: Formal unless the price is a range or a one-sided bound (a bid with no stated price keeps T0; 12 October 2026)
  - T3: Formal in a final round

  Compare them as robustness checks. Do not choose by best fit to hand-coded deals.
- **Inferred exits:** treat them as dropouts, or as censored observations.
- **Inferred counts:** use them as recorded, with or without a robustness check that sets them aside.

## Operational

- **Where work happens:** the Claude Code project "sec-auction" at claude.ai/code. Its threads start from `extraction-v2`, work on their own branches and open pull requests; Austin merges them. Project setup: [CLOUD_PROJECT.md](CLOUD_PROJECT.md). GitLab, the laptop checkout and `local-recovery-2026-09-27` are retired.
- **The VM** (`~/work/Projects/sec-auction`) keeps the live cockpit, paid extraction runs, Codex and the backups. Cloud threads reach it through the protected ARC connection (`arc exec condenser`). Deployment stays in the same cloud task; follow [CLOUD_DEPLOYMENT.md](CLOUD_DEPLOYMENT.md). Remote Control remains optional.
- **Comparison runs:** the 28–29 September runs are recorded in [model_comparison_2026-09](model_comparison_2026-09/README.md). Their run folders are deleted.
- **12 October comparison:** three random active deals, each with Astra, Sol 6.1, and Opus 5.5 at xhigh. All nine started together; both GPT arms requested Fast service. All nine completed with zero checker errors. The [report](model_comparison_2026-10-12/README.md) separates source findings, timing, and program defects. Original workbooks and receipts are preserved; temporary run folders are deleted. The live app and its default model did not change.
