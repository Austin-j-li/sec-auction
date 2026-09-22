# Mac-Gray: Astra high versus the raw Opus draft

**Astra produced the stronger raw v1.13.2 draft on this case. It addressed the four material problems identified in the earlier Mac-Gray adjudication without seeing those findings. It is still not a finished one-pass result: one mechanical ordering error remains, the first-round membership description needs tightening, and previously open conventions remain open.**

## What improved

| Issue | Raw Opus v1.13.2 | Raw Astra high |
| --- | --- | --- |
| Anonymous NDA cohort | Treats all 16 as non-submitters by July 23 despite unknown signing dates | Preserves the timing uncertainty and infers closure by the later, complete August 27 solicitation |
| September 27 voting agreements | Execution date appears only in the signing Note | Own dated event, correctly distinguishing execution from effectiveness at signing |
| Party B option terms | Omits material strike/vesting details | Preserves initial-cost strike, five-year base-case vesting and exclusion of acquisitions |
| Exclusivity-extension request | Folded into October 12 execution | Own request event **by October 9**, separately from execution |

Astra also improves the Moab-permission quotation, preserves the order of C's July 25 written revision, and finds three role-qualified buyer-side adviser/intermediary disclosures in Annex A. The [full assessment](ASSESSMENT.md) distinguishes these findings from representation choices and lists the exact rows and source pages.

All 13 bids retain the same bidder, date, round, price endpoints, cash classification, Formality and Conditions as Opus. Both have three rounds, opening June 24, July 25 and September 11. The improvement is principally in participation timing, event coverage and supporting terms, not the core price series.

## What still needs attention

- **Round marker:** Astra #12 is assigned to R1 before #13 opens it; both are June 24. This is the same mechanical ordering defect as Opus. A small row-order correction is needed.
- **Membership presentation:** Rounds correctly separates solicited contacts from eventual signers and says the early count is unknown, but should explicitly label A's offer as still being received while A was not yet admitted. It should identify the confirmed first-stage admissions directly.
- **Research and representation choices:** the treatment of later economic commitment terms as a separate bid, the old buy-side BofA engagement, and some information-access rows need the distinctions documented in the assessment. They are not all established extraction mistakes.

No new material price, bid-date, bidder-identity or final-stage error was found in the inspected record. This is a lead review of one familiar case, not a fully adjudicated benchmark or proof of completeness. The four recovered material problems are a targeted result; they are not a general accuracy score.

## Controlled run and validation

| Measure | Opus v1.13.2 extraction | Astra extraction |
| --- | --- | --- |
| Model / effort requested | Claude Opus 5 / high | GPT-6-Astra / high |
| Ledger events | 53 | 74 |
| Rounds / Questions | 3 / 9 | 3 / 8 |
| Separate checker v1.5 | 1 error, 8 warnings | 1 error, 4 warnings |
| Extraction time | 473.448 seconds, 7.9 minutes | 668.391 seconds, 11.1 minutes |
| Provider-reported extraction cost | $3.0989005 | Not reported |

The one Astra session ran from 23:09:13 to 23:20:21 UTC on 21 September 2026. It received the same unchanged instruction, filing and standard extraction prompt as Opus. Bubblewrap exposed only these research inputs and an empty output folder; a runtime preflight verified that `_dev`, `ref` and git history were absent. No old workbook, audit, adjudication or source inventory was visible. Web search and delegation were disabled, and the 32 completed shell commands showed no external-source or nested-model calls. The provider completed successfully in one thread/turn. Its own rereading and checks occurred within that initial session; there was no external feedback or revision pass.

The command and runtime configuration explicitly request `gpt-6-astra` with `high` effort, which the local model registry supports. Codex's completion event reports usage but does not independently repeat a returned model identifier. The legacy runner transport key is `sol`; the actual command, metadata and runtime record identify Astra. Production runner code was not changed.

Reported usage: 3,168,686 input tokens, of which 2,978,176 were cached; 19,362 output tokens and 3,034 reasoning-output tokens. These are provider fields, not a dollar-cost estimate. No human review-time saving was measured.

The lead reread the entire merger background (pp.27–41), checked the additional cited financing and annex passages, applied the 20-item bounded source inventory, compared all 13 bids and checked every ledger quotation against its cited page. All 74 quotations were located. Eventual participation reconciles to 20 entries, 19 exits and one winner; earlier membership stays qualified. Quote matching and mechanical checking do not by themselves establish substantive correctness.

The four checker warnings comprise three long Questions and one false positive claiming deadline-outcome Questions are absent; Q2–Q4 cover those outcomes. The extractor reported that its own validation passed; the separate checker found the marker-order error. The raw output was preserved before checking and has not been edited.

## Development implication

This is enough evidence to justify a fresh unseen-case Astra trial under the same frozen instruction. It is not enough to switch the default extractor or remove adjudication. The useful result is that a single unassisted Astra extraction handled the main participation uncertainty and recovered material details that the raw Opus extraction and its fresh audit did not resolve together. The separately requested controlled Opus revision was not executed as part of this Astra trial, so no comparison with a revised Opus workbook is claimed.

## Evidence

- [Raw Astra workbook](raw/extraction/mac-gray.xlsx).
- [Source assessment and criterion-by-criterion comparison](ASSESSMENT.md).
- [Pre-run protocol](PROTOCOL.md), `protocol-freeze.json` and `provenance/`.
- [Separate mechanical report](mechanical-check.json), [bid comparison](structured-comparison.json), [quotation/page checks](quote-page-check.json) and [participation arithmetic](participation-check.json).
- [Original extractor response](extractor-response.md), preserved as received. Its sandbox-local workbook link is historical; use the raw workbook link above.

Astra raw workbook SHA-256: `ee14d55c1f3aea0b793c5ad01507beefb12cb575071a696cf4489a6b30660f42`.

The instruction, both existing Mac-Gray raw workbooks and the other protected research files remain unchanged. Results and provenance are preserved here; disposable run state is removed after verification. No commit or push was made.
