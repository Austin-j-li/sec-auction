# Cockpit snapshot, 27 September 2026

> **Status clarification, 27 September 2026:** This is the collection-time inventory from 10:55 UTC, not the latest local recovery status. The root instruction and offline tools/packets were recovered afterward; the v1.13.2-to-root comparison and VM-only list below describe the earlier state. See [current research state and decisions](../../RESEARCH_QUESTIONS.md) and the [completed recovery record](../team-2026-09-27/README.md).

This is a copy of the live cockpit (https://lines.dealextract.org), taken on 27 September at 10:55 UTC. SSH to the Condenser VM was unavailable that day because the weekly bastion certificate had expired, but the cockpit itself was still serving. The copy was made with GET requests only, through Austin's Cloudflare Access session. Nothing was written to the cockpit.

GitLab (`origin/extraction-v2`) held nothing newer than `679d4fc`, so this snapshot is the only off-VM copy of the cockpit state after 23 September.

`INDEX.json` maps each API path to its file under `raw/`, with the file's size and SHA-256.

## Instructions (`instructions/`)

The text of every stored instruction version. Each file's SHA-256 matches the hash the cockpit records.

| File | Status | SHA-256 | Recorded by |
|---|---|---|---|
| `v1.14.1_08caed447f7d.md` | published, **default** | `8a93df3c…66c98` | austin, 26 Sep 20:18 UTC |
| `v1.13.2_513c8e3e8159.md` | published | `513c8e3e…` (identical to the repository file) | system, 23 Sep |
| `draft-a4ca26ecfa92_a4ca26ecfa92.md` | draft (v1.14 pilot text) | `f9595d74…` | austin, 24 Sep 22:41 UTC |
| `draft-73f21eb8c09a_73f21eb8c09a.md` | unused draft | `513c8e3e…` (same text as v1.13.2) | austin, 24 Sep |

Each version's edit history is in `raw/instructions__<id>[_seq_N].json`.

## Deals (`raw/deal__<slug>*`)

For each of the 13 deals the snapshot holds:
- the working-copy payload (ledger, review marks, findings, versions, field authors);
- the full revision history, with changes per field;
- the changes against the working copy's base;
- comments, activity and run jobs;
- the filing payload;
- for every version, and for the working copy, the version payload and an `.xlsx` export.

v1.14.1 reruns of 26 September (checker results as the cockpit records them):

| Deal | Version | Errors | Warnings |
|---|---|---:|---:|
| Datalink | `opus55-medium-20260926-2032-350a91` | 1 | 4 |
| Mac-Gray | `opus55-medium-20260926-2019-1d1d60` | 0 | 2 |
| Providence & Worcester | `opus55-medium-20260926-2019-366a73` | 0 | 2 |
| sTec | `opus55-medium-20260926-2027-0643aa` | 1 | 3 |
| Synacor | `opus55-medium-20260926-2028-342883` | 0 | 6 |

Other versions in the snapshot:
- the v1.14 draft pilots of 24 September (Mac-Gray and P&W, `…20260924-2241-…`);
- the 23 September PetSmart run;
- the deals added in the cockpit: Medivation, Zep, Pepco Holdings and Imprivata. Their filings are not in `raw_filing/`, but their text is in `raw/filing__<slug>.json`.

Every working copy is still based on v1.13.2. Working revisions with saved edits:
- Kraton: 4
- Mac-Gray: 8
- Meredith: 4
- Penford: 2
- PetSmart: 2
- P&W: 16
- sTec: 1
- Synacor: 1

## What this snapshot does not contain

These exist only on the VM:
- the SQLite database file and its stored-file tree, although its content is largely represented above;
- the uncommitted source code: checker 1.8, the analysis, migration and provenance tools, and the server, worker and frontend changes;
- `_dev/maintenance/2026-09-2{4,5,6}-*` and `_dev/reviews/2026-09-26-*`, including the questionnaire DOCX;
- the `sec-extraction-v114` worktree;
- `~/backups/ledger-cockpit/`.
