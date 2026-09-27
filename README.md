# SEC deal-ledger project

This repository supports research by Austin Li and Alex Gorbenko on informal and formal bidding in takeover auctions. Each deal's "Background of the Merger" section, taken from its SEC merger filing, is turned into an Excel deal ledger: an event-by-event record of the sale process, from which one can read how many bidders were live at each stage, which round each bid belonged to, whether it was formal or informal, and at what price.

A ledger workbook has four sheets, defined in the instruction:

- **Deal ledger**: one row per substantive event in event order, plus process and round markers, each supported by a quotation from the filing;
- **Rounds**: one line per bidding round, with who was admitted, due dates, bids received and how the round ended;
- **Questions**: open coding questions, each with a recommended answer, the supporting page and the rows affected;
- **Deal facts**: deal-level fields such as the parties, price, initiation, advisers and a short account of the process.

## Current status

Version 0 as of 27 September 2026: the instruction is v0, `extraction/` is empty, and every deal is to be re-extracted. See [status](_dev/STATUS.md) for open research questions and pending work.

## Repository layout

| Path | Contents |
|---|---|
| [`SEC_Deal_Ledger_Extraction_Instruction.md`](SEC_Deal_Ledger_Extraction_Instruction.md) | The extraction instruction, version 0. |
| [`raw_filing/`](raw_filing/) | The nine filings as fetched from EDGAR; [`MANIFEST.csv`](raw_filing/MANIFEST.csv) records each source link and SHA-256 hash. |
| `extraction/` | Blind extractions under v0, one `<deal>.xlsx` per deal. |
| `ref/` | Alex's collection instructions, voice notes and hand-coded deals. For evaluation only. |
| [`_dev/`](_dev/) | Status, the Alex-alignment audit, the cockpit app spec and the pipeline tools. |

The nine deals are Datalink, Kraton, Mac-Gray, Meredith, Penford, PetSmart, Providence & Worcester, sTec and Synacor.

## Extracting a deal

Extraction follows [AGENTS.md](AGENTS.md). In brief:

- the extracting agent uses only the instruction and the assigned filing in `raw_filing/`, and saves its workbook as `extraction/<deal>.xlsx`;
- it must not read `ref/`, `_dev/`, other workbooks in `extraction/` or the git history, since these contain earlier analyses and hand-coded answers and would invalidate a blind extraction;
- it does not use the web or identify anonymous bidders from outside knowledge.

Extractions are run only on Austin's command. Each run is isolated in a sandbox with one instruction and one filing, and the mechanical checker is run afterwards, outside the sandbox. Revising an existing workbook against review findings is a separate, explicitly requested mode. The commands are in the [tools guide](_dev/tools/README.md).

## Where to go next

- [Status](_dev/STATUS.md): open research questions, settled rulings and pending work.
- [Alex-alignment audit](_dev/ALEX_ALIGNMENT.md): where the v0 instruction departs from Alex's voice notes, with a work order.
- [Cockpit app spec](_dev/COCKPIT_APP_SPEC.md): the shared extraction app on the VM.
- [Tools guide](_dev/tools/README.md): environment, mechanical checking, isolated runs, review helpers and analysis tables.
