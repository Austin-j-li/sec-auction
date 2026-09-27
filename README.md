# SEC deal-ledger project

This repository supports research by Austin Li and Alex Gorbenko on informal and formal bidding in takeover auctions. Each deal's "Background of the Merger" section, taken from its SEC merger filing, is turned into an Excel deal ledger: an event-by-event record of the sale process, from which one can read how many bidders were live at each stage, which round each bid belonged to, whether it was formal or informal, and at what price.

A ledger workbook has four sheets, defined in the instruction:

- **Deal ledger**: one row per substantive event in event order, plus process and round markers, each supported by a quotation from the filing;
- **Rounds**: one line per bidding round, with who was admitted, due dates, bids received and how the round ended;
- **Questions**: open coding questions, each with a recommended answer, the supporting page and the rows affected;
- **Deal facts**: deal-level fields such as the parties, price, initiation, advisers and a short account of the process.

A workbook downloaded from the cockpit's working copy adds a fifth sheet, Source, with the filing's EDGAR links and the download's provenance. The cockpit writes it, never the model; the four-sheet download, which the checker accepts, leaves it out.

## Current state (26 September 2026, evening)

- **Instruction.** The repository's working extraction instruction, `SEC_Deal_Ledger_Extraction_Instruction.md`, is v1.13.2 and is frozen; extractions run outside the cockpit use it. In the cockpit, v1.14.1 was published and made the default on 26 September (SHA-256 `8a93df3c…6c98`); v1.13.2 stays published there. Exporting v1.14.1 to the repository file is a later step Austin orders. Further edits require Austin's approval and must be general rather than justified by a single reviewed deal.
- **Extractions.** `extraction/` holds nine blind extractions, one per deal, made by Claude Opus 5.5 at medium effort under v1.13.2 on 22 September. They are **unreviewed and not research-ready**. Checker results are mechanical: they record structural errors and warnings, not accuracy.
- **Review cockpit.** The editable review cockpit is live at <https://lines.dealextract.org>, behind Cloudflare Access for Austin and Alex. It shows each filing beside its workbook, allows editing of all four sheets, records decisions and revision history, and exports Excel (by default with the Source sheet above). Its checker and value lists follow each workbook's ledger schema and rules, v1.13.2, v1.14 or v1.14.1; checker 1.8 and the v1.14.1 cockpit changes were deployed on 26 September 2026. Edits are kept separately from the preserved original workbooks. Its interface was redesigned and redeployed on 23 September 2026.
- **Review.** In the cockpit, eight of the nine deals have working copies edited with Astra's help and independently audited, with three clusters reverted on 24 September; no deal-level review status is set, and Datalink's working copy is unedited. Austin has added four more deals there (Medivation, Zep, Pepco Holdings and Imprivata). The handoff records the case-level decisions to check: Mac-Gray's R01 ruling, which its working copy applies, and Datalink's round structure, which Austin settled on 26 September (Datalink follows the v1.14.1 text, four rounds, superseding the earlier F9 ruling's five).
- **Extraction engine (26 September).** Claude Opus 5.5 at medium effort is the default extractor again, reversing that morning's switch to GPT-6-Astra at high effort; it has been live since the deploy that evening. Astra stays selectable.
- **Next step.** The v1.14 upgrade ([specification](_dev/maintenance/2026-09-24-bid-terms-taxonomy/V114_SPEC.md)) became v1.14.1, a streamlined instruction written after the fifteen-run v1.14 trial ([V1141_SPEC](_dev/maintenance/2026-09-26-v1141-streamline/V1141_SPEC.md); pipeline changes in [PIPELINE_UPGRADE_SPEC](_dev/maintenance/2026-09-26-v1141-streamline/PIPELINE_UPGRADE_SPEC.md)). Its code (checker 1.8 and the cockpit, catalog, migration and analysis tools) was deployed on 26 September 2026; the instruction was published in the cockpit and made its default the same evening, and its five-run retest (Mac-Gray, Providence & Worcester, sTec, Synacor, Datalink) was run then ([results](_dev/reviews/2026-09-26-v1141-retest/README.md); the five runs are cockpit versions, raw and unreviewed). Still to come, each on Austin's order: exporting v1.14.1 to the repository file, sending Alex the questionnaire, committing the work, re-extracting the other deals, moving reviewed work onto v1.14.1 deal by deal once that deal's v1.14.1 run has been reviewed, and then updating `extraction/`.

## Repository layout

| Path | Contents |
|---|---|
| [`SEC_Deal_Ledger_Extraction_Instruction.md`](SEC_Deal_Ledger_Extraction_Instruction.md) | The repository's working extraction instruction, v1.13.2 (frozen); the cockpit's default is v1.14.1. |
| [`raw_filing/`](raw_filing/) | The nine filings as fetched from EDGAR; [`MANIFEST.csv`](raw_filing/MANIFEST.csv) records each source link and SHA-256 hash. |
| `extraction/` | The current blind extractions, one `<deal>.xlsx` per deal. |
| `ref/` | Alex's collection instructions, voice notes and hand-coded deals. For evaluation only. |
| [`_dev/`](_dev/) | Pipeline tools, the cockpit, review packets, research questions and development history. |

The nine deals are Datalink, Kraton, Mac-Gray, Meredith, Penford, PetSmart, Providence & Worcester, sTec and Synacor.

## Extracting a deal

Extraction follows [AGENTS.md](AGENTS.md). In brief:

- the extracting agent uses only the instruction and the assigned filing in `raw_filing/`, and saves its workbook as `extraction/<deal>.xlsx`;
- it must not read `ref/`, `_dev/`, `lesson/`, other workbooks in `extraction/` or the git history, since these contain earlier analyses and hand-coded answers and would invalidate a blind extraction;
- it does not use the web or identify anonymous bidders from outside knowledge.

Extractions are run only on Austin's command. Each run is isolated in a sandbox with one instruction and one filing, and the mechanical checker is run afterwards, outside the sandbox. Revising an existing workbook against review findings is a separate, explicitly requested mode. The commands are in the [tools guide](_dev/tools/README.md).

## Where to go next

- [Development handoff](_dev/HANDOFF.md): current direction, per-deal review boundaries, engineering status and next work. Start here for anything beyond reading this page.
- [Research questions](_dev/RESEARCH_QUESTIONS.md): resolved decisions, pending deal choices and provisional conventions.
- [Cockpit guide](_dev/cockpit/README.md): how to review and edit a deal in the cockpit, from filing navigation to saving, restoring and exporting.
- [Cockpit build contract](_dev/COCKPIT_BUILD.md): the cockpit's API and storage design, the 23 September redesign and its verification limits.
- [Tools guide](_dev/tools/README.md): environment, mechanical checking, isolated runs, effort sweeps, review helpers, analysis tables, reviewed-work migration and offline validation.
- [Chronology](_dev/CHRONOLOGY.md): an index of historical instruction versions and review evidence. Earlier instructions live in git history and must not be restored into the checkout.
