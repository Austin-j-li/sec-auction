# SEC deal-ledger project

This repository supports research by Austin Li and Alex Gorbenko on informal and formal bidding in takeover auctions. Each deal's "Background of the Merger" section, taken from its SEC merger filing, is turned into an Excel deal ledger: an event-by-event record of the sale process, from which one can read how many bidders were live at each stage, which round each bid belonged to, whether it was formal or informal, and at what price.

A ledger workbook has four sheets, defined in the instruction:

- **Deal ledger**: one row per substantive event in event order, plus process and round markers, each supported by a quotation from the filing;
- **Rounds**: one line per bidding round, with who was admitted, due dates, bids received and how the round ended;
- **Questions**: open coding questions, each with a recommended answer, the supporting page and the rows affected;
- **Deal facts**: deal-level fields such as the parties, price, initiation, advisers and a short account of the process.

A workbook downloaded from the cockpit's working copy adds a fifth sheet, Source, with the filing's EDGAR links and the download's provenance. The cockpit writes it, never the model; the four-sheet download, which the checker accepts, leaves it out.

## Current status (27 September 2026)

Start with [current status and research decisions](_dev/RESEARCH_QUESTIONS.md). It separates settled rulings, choices still needed from Austin and Alex, review work, and the VM recovery boundary. The local evidence cutoff is the **27 September, 10:55 UTC cockpit snapshot**; Condenser is temporarily unavailable and later live state is not established.

- **Instruction:** the local root file is the published v1.14.1 text (`8a93df3c…66c98`), copied with Austin's approval during recovery. This does not establish that the VM repository export ran. Further instruction edits require Austin's approval.
- **Data:** the nine `extraction/` workbooks remain the 22 September Opus 5.5 medium v1.13.2 outputs. The snapshot has thirteen working copies, all still based on v1.13.2, and five separate raw v1.14.1 reruns. No deal has completed Austin's source review; the data are not research-ready.
- **Recovery:** checker 1.8 and analysis/migration tools were replayed or rebuilt from VM traces. The 24–26 September cockpit app source remains VM-only; reconcile recovered files against it when access returns. See the [gap inventory](_dev/recovery/GAP.md) and [recovery record](_dev/recovery/team-2026-09-27/README.md).
- **Next:** discuss the open coding conventions and review each new run against its filing before rebasing and porting accepted prior review.

## Repository layout

| Path | Contents |
|---|---|
| [`SEC_Deal_Ledger_Extraction_Instruction.md`](SEC_Deal_Ledger_Extraction_Instruction.md) | v1.14.1 on this laptop recovery branch; the VM repository file was v1.13.2 on 26 September. The cockpit's default is v1.14.1. |
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

- [Current status and research decisions](_dev/RESEARCH_QUESTIONS.md): the starting point for settled rulings, unresolved choices, review work and recovery limits.
- [Cockpit guide](_dev/cockpit/README.md): how to review and edit a deal in the cockpit, from filing navigation to saving, restoring and exporting.
- [Cockpit build contract](_dev/COCKPIT_BUILD.md): the cockpit's API and storage design, the 23 September redesign and its verification limits.
- [Tools guide](_dev/tools/README.md): environment, mechanical checking, isolated runs, effort sweeps, review helpers, analysis tables, reviewed-work migration and offline validation.
- [Chronology](_dev/CHRONOLOGY.md): an index of historical instruction versions and review evidence. Earlier instructions live in git history and must not be restored into the checkout.
