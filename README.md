# SEC deal-ledger project

This repository supports research by Austin Li and Alex Gorbenko on informal and formal bidding in takeover auctions. Each deal's "Background of the Merger" section, taken from its SEC merger filing, is turned into an Excel deal ledger: an event-by-event record of the sale process, from which one can read how many bidders were live at each stage, which round each bid belonged to, whether it was formal or informal, and at what price.

A ledger workbook has four sheets, defined in the instruction:

- **Deal ledger**: one row per substantive event in event order, plus process and round markers, each supported by a quotation from the filing;
- **Rounds**: one line per bidding round, with who was admitted, due dates, bids received and how the round ended;
- **Questions**: open coding questions, each with a recommended answer, the supporting page and the rows affected;
- **Deal facts**: deal-level fields such as the parties, price, initiation, advisers and a short account of the process.

## Current state (23 September 2026)

- **Instruction.** The working extraction instruction is v1.13.2 and is frozen. Further edits require Austin's approval and must be general rather than justified by a single reviewed deal.
- **Extractions.** `extraction/` holds nine blind extractions, one per deal, made by Claude Opus 5.5 at medium effort under v1.13.2 on 22 September. They are **unreviewed and not research-ready**. Checker results are mechanical: they record structural errors and warnings, not accuracy.
- **Review cockpit.** The editable review cockpit is live at <https://lines.dealextract.org>, behind Cloudflare Access for Austin and Alex. It shows each filing beside its workbook, allows editing of all four sheets, records decisions and revision history, and exports Excel. Edits are kept separately from the preserved original workbooks. Its interface was redesigned and redeployed on 23 September 2026.
- **Next step.** Austin's source review of the nine workbooks is pending. The handoff records the known case-level decisions to check (Datalink's round structure and Mac-Gray's R01 ruling).

## Repository layout

| Path | Contents |
|---|---|
| [`SEC_Deal_Ledger_Extraction_Instruction.md`](SEC_Deal_Ledger_Extraction_Instruction.md) | The working extraction instruction, v1.13.2 (frozen). |
| [`raw_filing/`](raw_filing/) | The nine filings as fetched from EDGAR; [`MANIFEST.csv`](raw_filing/MANIFEST.csv) records each source link and SHA-256 hash. |
| `extraction/` | The current blind extractions, one `<deal>.xlsx` per deal. |
| `ref/` | Alex's collection instructions, voice notes and hand-coded deals. For evaluation only. |
| [`_dev/`](_dev/) | Pipeline tools, the cockpit, review packets, research questions and development history. |

The nine deals are Datalink, Kraton, Mac-Gray, Meredith, Penford, PetSmart, Providence & Worcester, sTec and Synacor.

## Extracting a deal

Extraction follows [AGENTS.md](AGENTS.md). In brief:

- the extracting agent uses only the instruction and the assigned filing in `raw_filing/`, and saves its workbook as `extraction/<deal>.xlsx`;
- it must not read `ref/`, `_dev/`, other workbooks in `extraction/` or the git history, since these contain earlier analyses and hand-coded answers and would invalidate a blind extraction;
- it does not use the web or identify anonymous bidders from outside knowledge.

Extractions are run only on Austin's command. Each run is isolated in a sandbox with one instruction and one filing, and the mechanical checker is run afterwards, outside the sandbox. Revising an existing workbook against review findings is a separate, explicitly requested mode. The commands are in the [tools guide](_dev/tools/README.md).

## Where to go next

- [Development handoff](_dev/HANDOFF.md): current direction, per-deal review boundaries, engineering status and next work. Start here for anything beyond reading this page.
- [Research questions](_dev/RESEARCH_QUESTIONS.md): resolved decisions, pending deal choices and provisional conventions.
- [Cockpit guide](_dev/cockpit/README.md): how to review and edit a deal in the cockpit, from filing navigation to saving, restoring and exporting.
- [Cockpit build contract](_dev/COCKPIT_BUILD.md): the cockpit's API and storage design, the 23 September redesign and its verification limits.
- [Tools guide](_dev/tools/README.md): environment, mechanical checking, isolated runs, effort sweeps and offline validation.
- [Chronology](_dev/CHRONOLOGY.md): an index of historical instruction versions and review evidence. Earlier instructions live in git history and must not be restored into the checkout.
