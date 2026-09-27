# B_analysis recovery report

## Files

| File | Provenance | Evidence and replay | Unresolved |
|---|---|---|---|
| `_dev/tools/derive_analysis.py` | REPLAYED | Full v114 Read 2026-09-26 19:08:35Z, continuation Read 19:08:38Z (1,037 contiguous lines); 13 successful Edit calls 19:11:15–19:12:19Z, plus later Bash edits and checks in `all_calls_since_0924.jsonl` through 19:17:49Z. All 13 Edit old strings applied once to the reconstructed Read. | Later Bash mutations prevent an exact hash comparison with the unreachable VM. Outputs match the five recorded VM rerun summaries. Depends on `check_lean.py` 1.8 names `RULES_29_COLUMN`, `SCHEMA_V1141`, `is_29_column`, and `ledger_schema(path, rules)`; that file belongs to another slice. |
| `_dev/tools/test_derive_analysis.py` | REPLAYED | Full v114 Read 2026-09-26 19:08:46Z (556 lines); 0 direct Edit calls; later Bash edits and test runs 19:14:33–19:15:41Z. | Exact VM hash unavailable. |
| `_dev/tools/migrate_review.py` | REPLAYED | Full v114 Read 2026-09-26 19:08:31Z (975 lines); Bash edit 19:11:30Z and 2 successful Edit calls 19:11:44Z, 19:12:06Z. Both Edit old strings applied once after the Read. | Exact VM hash unavailable; default `AUDIT_DIR` still names the VM's retired `lesson/` source, but the tool only reads it and the smoke passed an empty temporary audit directory. |
| `_dev/tools/test_migrate_review.py` | REPLAYED | Full v114 Read 2026-09-26 19:09:05Z (478 lines); 0 direct Edit calls; later Bash changes and 17-test success at 19:13:25Z. | Exact VM hash unavailable. |
| `_dev/tools/compare_alex.py` | REBUILT | No full VM Read. Reconstructed from the 2026-09-26 `all_calls_since_0924.jsonl` partial reads, `--rules` edit at 19:13:46–19:13:53Z, 20:45:45Z CLI and output sample, `PIPELINE_UPGRADE_SPEC.md`, and observed Mac-Gray/P&W alignment totals. | VM source and exact hash unavailable. |
| `_dev/tools/test_compare_alex.py` | REBUILT | No full VM Read. Reconstructed from 19:13:36Z partial test read, CLI/output observations, and the compare spec. Covers bidder/price/date alignment, CVR package basis, event code map, red-font provenance, rules selector, and output files. | VM source and exact hash unavailable. |

New fixture files under `_dev/tools/`: none. The six candidate files were already present in the shared checkout at the start of this slice. Review then prompted corrections in `compare_alex.py` and `test_compare_alex.py`, recorded below.

## Checks

- `python3 -m pytest _dev/tools/test_derive_analysis.py _dev/tools/test_migrate_review.py _dev/tools/test_compare_alex.py -q` — exit 0; **52 passed, 50 subtests passed in 2.16s**.
- `python3 _dev/tools/derive_analysis.py <five snapshot v1.14.1 exports> --deal <slug> --rules v1.14.1 --out /tmp/recov/work/B/derive_check/<slug>` — all five exit 0. The first attempt against the pre-existing `/tmp/recov/work/B/derive/<slug>` directories exited 2 because the required output folders were nonempty; the rerun used fresh folders.

| Deal | bids | other scope | rounds | participation | deal | review items | VM 20:46:02Z record |
|---|---:|---:|---:|---:|---:|---:|---|
| mac-gray | 16 | 0 | 3 | 13 | 1 | 1 | match |
| providence-worcester | 14 | 0 | 3 | 28 | 1 | 4 | match |
| stec | 9 | 0 | 2 | 16 | 1 | 1 | match |
| synacor | 11 | 6 | 6 | 21 | 3 | 5 | match |
| datalink | 22 | 0 | 4 | 23 | 1 | 5 | match |

- `python3 _dev/tools/compare_alex.py <snapshot rerun export> --deal <slug> --rules v1.14.1 --out /tmp/recov/work/B/compare_<slug>` — Mac-Gray exit 0, 13/13 labelled bids aligned; T0 13/13, T1 11/13, T1u 9/13, T2 12/13, T3 13/13. P&W exit 0, 14/14 aligned; T0 11/14, T1 12/14, T1u 12/14, T2 11/14, T3 12/14. These match the retest README's 13/13 T0/T3 Mac-Gray and best 12/14 P&W bounds.
- `migrate_review.load_run(<snapshot mac-gray working export>, 'mac-gray')` — v1.13.2, 58 ledger rows, 3 rounds, 9 questions, 17 facts; row counts equal the saved cockpit JSON projection. Constructed a temporary SQLite `revisions` row from that projection with typed date cells, outside the repo. `migrate_review.py register mac-gray --state-db /tmp/recov/work/B/migrate_smoke/snapshot_revisions.sqlite3 --audit-dir /tmp/recov/work/B/migrate_smoke/no_audit --filings /tmp/recov/work/B/migrate_smoke/no_filings --out /tmp/recov/work/B/migrate_smoke/register` — exit 0; revision 8, 58 rows (56 reviewed, 2 needs decision), 181 facts. `triage` of the saved v1.14.1 Mac-Gray export against it — exit 0; 40/58 ledger rows and 3/3 rounds aligned; 116 agreeing facts, 19 changed-rule facts, 43 omitted/inserted facts. A self-triage of the saved v1.13.2 working export — exit 0; 56/58 ledger rows and 3/3 rounds aligned. The temporary projection omits the VM's independent-audit inventory, filing locator and threads, so these triage counts are a dry-run check, not a release assessment. No port batch was applied.

## Fixes

- **Event-code map (review finding 1):** Updated `compare_alex.py` to follow the recorded analysis contract §11, original line 192: Bidder Sale → Bid; Sale Press Release → Sale process announced; Target Sale Public also allows Sale process announced; added Bid Press Release, Terminated, Restarted and `Exclusivity …`; final-round variants now distinguish Deadline, Deadline set, Deadline revised and Round opened. `Ann` selects announcement events; finality is checked separately. Labelled-bid code checks use the same map. Added tests for these code families and the final-round announcement distinction.
- **Event date window (finding 2):** `match_code` now requires a ledger event within 31 days, inclusive, of either Alex precise or rough date for every code, including Drop. It reports the nearer gap. Added tests for 20-day Drop, 31/32-day boundary, a 365-day NDA, both-date fallback and absent dates.
- **Price tolerance (finding 3):** Changed tolerance to half a cent, inclusive; added checks at 0.004, 0.005, 0.006 and 0.01. The tiny floating-point allowance applies only at the 0.005 boundary.
- **Correction provenance (finding 4):** Whole-row threshold is 30 red cells; only `comments_1–3` count as comments-only. `additional_note` in red is a correction. Added threshold and comment-column tests.
- `python3 -m pytest _dev/tools/test_derive_analysis.py _dev/tools/test_migrate_review.py _dev/tools/test_compare_alex.py -q` — exit 0; **55 passed, 65 subtests passed in 2.19s**.
- Re-ran `compare_alex.py` on the saved Mac-Gray and P&W v1.14.1 exports into `/tmp/recov/work/B/compare_fixed_<slug>` — both exit 0. Labelled-bid alignment and T0–T3 totals remain 13/13 and 14/14 aligned, with the same reading totals reported above. Mac-Gray event statuses changed from 31 agree / 1 unaligned / 2 exit-other to 30 / 2 / 2. P&W changed from 26 agree / 5 unaligned / 1 not compared / 1 finality mismatch / 1 disagree / 2 exit-other to 25 / 5 / 1 / 2 / 1 / 2. The 24 September v1.14 pilots do have a historical VM status reference; the v1.14.1 reruns do not.

## Fixes (round 2)

- **Final-round finality:** The earlier reconstruction required `Announced as final` for codes ending in `Ann`. The recorded analysis contract §11 (`/tmp/recov/all_calls_since_0924.jsonl`, line 740, original line 192) says `Ann` selects an announcement event; the round's Finality is final for both `Announced as final` and `Inferred final`. `compare_alex.py` now uses `derive.FINAL` for every final-round code. Added a focused test for the 24 September P&W pilot's Alex row 6045: `Final Round Ann` agrees with ledger row 35, `Round opened`, round 3, `Inferred final`. The test also checks that `Final Round Inf Ann` differs on that finality.
- `python3 -m pytest _dev/tools/test_derive_analysis.py _dev/tools/test_migrate_review.py _dev/tools/test_compare_alex.py -q` — exit 0; **56 passed, 65 subtests passed in 2.13s**.
- Re-ran both 24 September v1.14 pilots with `--rules v1.14` into `/tmp/recov/work/B/pilot_recheck/round2_pw/` and `round2_mg/`; both CLIs exited 0. P&W: **27 agree, 3 unaligned, 3 exit-other, 1 finality differs, 1 not compared, 1 disagree**, matching the recorded VM tally. Row 6045 is now `agree`; row 6058 remains the one finality mismatch (`Final Round` against a `Not final` round). Mac-Gray remains **32 agree, 2 exit-other**, matching its VM summary. Labelled-bid alignment remains 14/14 for P&W and 13/13 for Mac-Gray.
