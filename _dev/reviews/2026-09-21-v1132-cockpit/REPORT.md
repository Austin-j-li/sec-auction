# Nine-deal v1.13.2 cockpit import

**Retired, 22 September 2026:** the seven raw workbooks this report lists (formerly `raw/extraction/<deal>.xlsx` in this packet) have left the checkout. Each is recoverable with `git show 03d59b1:_dev/reviews/2026-09-21-v1132-cockpit/raw/extraction/<deal>.xlsx`; the SHA-256 values below identify them. Paths to them in this packet's JSON records are historical. The cockpit catalog described below has also been replaced by one Opus 5.5 medium version per deal.

All seven authorized isolated Claude Opus 5 high extractions completed once. Their prepared instruction and source hashes match the frozen inputs; provider success, readable four-sheet XLSX, reported model, output hashes and separately run mechanical checks were verified from preserved receipts. The checker is mechanical and does not certify substantive correctness. Austin's source review remains pending for these seven drafts.

Frozen instruction SHA-256: `513c8e3e8159e4a6bceccd6ffca32a246302736329a0c7137b64dd3b7ffcd304`.

| New raw draft | SHA-256 | Checker errors | Warnings | Provider-reported cost |
| --- | --- | ---: | ---: | ---: |
| Kraton | `be4549979af56dcb7fc56b9b6e33295989d28e1be84ddbb02c4c683a3c0dd2e9` | 0 | 10 | $3.836 |
| Meredith | `178c1f0c8419ef19503ad52e1b1fa40132d5f3b35e1d32f62e8c62205d951c89` | 0 | 12 | $4.085 |
| Penford | `e860a97753bd73758dc1c788fb2403e3c78f48a41a28811c91b921db287f14f7` | 0 | 18 | $3.074 |
| PetSmart | `e6e46be37e22030f3ad8116815988a37c570c99281928d7c38276fcd5bd04bc9` | 0 | 10 | $4.096 |
| Providence & Worcester | `b73bf344f07b32e75837118f8edabc1418e28f31a1163d986bc352a94c3e270e` | 0 | 12 | $2.808 |
| sTec | `85f28228f875a8ac8cfae9059cf5442f4724d94e999dd2f1974adba82b93305a` | 0 | 18 | $4.684 |
| Synacor | `b9a746897d987d96200542b72cee3c19067e5b9d877ccb94aaf725c3f5023f2b` | 1 | 8 | $4.853 |

Seven-run reported cost: $27.436. This is provider list-price reporting, not account billing.

Reused Datalink raw SHA-256: `499d2f2259f10bcb3895a08538bcbf4f686c55a4d568c0a6ded9096ee9449358`; reused Mac-Gray raw SHA-256: `9422bc6b0d14c19033771a51bb6432e2054f16ba55e9b07df02c73c3d28ac279`. Their existing pilot provenance and separate checks remain in their original packets. All nine canonical workbooks, nine filings, manifest, runner and instruction match the protected pre-batch hashes.

The catalog preserves each raw v1.13.2 output, the eight original v1.13 baselines, and the separately verified Datalink and Mac-Gray controlled revisions. The earlier verified revisions are lead-verified correction passes, not human benchmark approvals. Datalink's retained checker result is one page-break quotation false positive and 24 length warnings; its verification report documents the exception. Neither revision overwrites a raw workbook.

A newer Mac-Gray acceptance-correction candidate is the default working base: 58 events, 13 bids, 3 rounds and 9 Questions; checker 0 errors and 13 warnings. The previous 55-event verified revision remains separately selectable. The acceptance packet verifies supported A01–A11 changes but explicitly marks consequential R01 research-decision pending, accepted=false and frozen_for_research=false. The candidate is not research-ready; no R01 treatment was applied. Its acceptance report, decision, analytical-use and coverage documents are linked in the catalog.

The seven new v1.13.2 drafts have no imported substantive findings; Austin's source review remains pending. Datalink and Mac-Gray audit findings retain their source-version labels and lead assessments as attributed notes. Only Austin's documented Datalink F9 ruling is carried as a user decision. No fresh substantive audit, new revision, instruction edit, commit or push was performed for this batch.

Current cockpit finding judgments remain unreviewed and implementation is unassessed. Earlier applied corrections appear separately as attributed `recorded_correction` entries tied to the verified Datalink and Mac-Gray versions; they do not mark Austin's current review complete.

Evidence: `batch.json`, `protected-inputs.json`, `receipts/<deal>/`, `checks/<deal>.json`, `import-verification.json`, `catalog-verification.json`, `cleanup.json`, and `_dev/cockpit/catalog.json`. After root reviewed the preserved evidence, only the seven exact disposable batch run folders and administrator script were removed; `cleanup.json` records their hashes and verified absence.
