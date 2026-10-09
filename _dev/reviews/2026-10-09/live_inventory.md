# Live inventory, 9 October 2026

Evidence time: 14:35–14:40 UTC. Scope: repository state, deployment, database, retained outputs, backups, and data paths.

Root decision supported: choose the baseline for the pipeline review. The live app retains raw Version 1 outputs. It records no review acceptance.

## Material facts

1. The review checkout is `2e781023289eab42b7a3ead0b8d5977525450211`. The original checkout is `e0f73ee12bd916dae3e43e552c822968443bbade`. The live checkout is `9f0750e0a5663fd9f5dbba622373da5da4591957`. Each checkout was clean at 14:35 UTC. All three instruction files match SHA-256 `05d8668d7778eb3e985599fec0a42c62fd4e41575e542af935d2d4ff8af05de4`.
2. The cockpit and worker run from `/home/uctpiaj/work/Projects/ledger-live`. Their PIDs are 2662766 and 2662767. Both use `/usr/bin/python3.12`. Both started on 29 September at 22:12:59 UTC. Their current systemd restart counts are zero. No process has a `sandbox/run_model.py` argument. The tunnel and Remote Control services are active.
3. The cockpit process sets `COCKPIT_REQUIRE_ACCESS=1`. Its public origin is `https://lines.dealextract.org`. This confirms the effective flag. This inventory does not independently verify the token verifier. Root separately used an existing authenticated browser session.
4. The read-only database shows 15 completed jobs: 13 extractions and two account connections. It shows no failed or active jobs. The 13 extractions finished on 28 September. The latest completion is 15:56:12 UTC. Each version records `claude-opus-5-5`, medium effort, and the same Version 1 instruction hash. All 13 workbook paths exist. Each workbook matches its database hash.
5. The database shows zero revisions, review rows, comments, threads, and hidden deals. It holds 13 base versions and four added deals. It holds one published instruction and one seed edit. The default instruction is `05d8668d7778`. No recorded review acceptance exists. A browser draft is outside this evidence.
6. The saved deployed checker receipts total 52 errors and 40 warnings. Five versions have errors. These are mechanical results from 28 September. The table below gives their exact counts. They do not establish source accuracy. This inventory did not rerun the checker. The separate CLI review owns the current-source check.
7. The newest backup is `~/backups/ledger-live/20261009-134250Z`. Its manifest records 13:42:50 UTC, live commit `9f0750e`, and checker Version 1. All 110 recorded file and database hashes match. Its table counts match the live counts above. No manifest exists for 8 October or the scheduled 9 October 03:30 run. The next timer trigger is 10 October 03:30 UTC. The gap's cause remains unverified. The available user journal returns zero rows since 7 October.
8. The review checkout's status record correctly states 13 cockpit runs and 13 versions (`_dev/STATUS.md:8-9`). The original checkout's status record still states no extractions and no versions (`_dev/STATUS.md:8-9`). Every checkout's `extraction/` contains only its empty placeholder. No exported workbook exists there. Later review code exists in the review checkout; the live app remains at `9f0750e`.
9. Retained external filings remain real files on the work disk. Each checkout's `raw_filing/` holds nine filings and one manifest: 12,897,163 bytes total. The live added-filings store holds four files: 7,222,485 bytes. These paths have no symbolic links. They do not follow the supplied instruction to keep all ingested data on RDSS. The retained filings predate 5 October. RDSS README line 7 expressly requires new downloads there. This inventory does not infer any new post-rule download. Work disk free space is 294 GB. RDSS free space is 1.6 TB.

## Raw output counts

These counts come from the retained XLSX files and their saved `check.json` receipts. Row counts exclude headers.

| Deal | Ledger rows | Round rows | Question rows | Saved errors | Saved warnings |
|---|---:|---:|---:|---:|---:|
| Datalink | 78 | 4 | 11 | 1 | 5 |
| Imprivata | 46 | 2 | 12 | 0 | 3 |
| Kraton | 57 | 3 | 15 | 0 | 5 |
| Mac-Gray | 54 | 3 | 10 | 0 | 1 |
| Medivation | 28 | 2 | 10 | 1 | 2 |
| Meredith | 47 | 0 | 6 | 41 | 1 |
| Penford | 44 | 2 | 11 | 0 | 2 |
| Pepco Holdings | 47 | 2 | 8 | 0 | 4 |
| PetSmart | 50 | 2 | 10 | 0 | 4 |
| Providence & Worcester | 68 | 3 | 13 | 1 | 1 |
| sTec | 63 | 3 | 12 | 0 | 3 |
| Synacor | 63 | 6 | 18 | 8 | 4 |
| Zep | 51 | 5 | 10 | 0 | 5 |

Comparison workbooks under `_dev/model_comparison_2026-09/` are separate artifacts. They are not the 13 deployed versions above.

## Retained output paths

Live root: `/home/uctpiaj/work/Projects/ledger-live`.

Each workbook is at `_dev/cockpit/state/versions/<slug>/<version-id>/<slug>.xlsx`. Its directory also retains `metadata.json`, `status.json`, and `check.json`.

| Slug | Version ID |
|---|---|
| datalink | opus55-medium-20260928-1531-b29df5 |
| imprivata | opus55-medium-20260928-1546-e652a1 |
| kraton | opus55-medium-20260928-1438-a1abe0 |
| mac-gray | opus55-medium-20260928-1420-10355a |
| medivation | opus55-medium-20260928-1531-4031a4 |
| meredith | opus55-medium-20260928-1438-2ba2d9 |
| penford | opus55-medium-20260928-1430-b704c0 |
| pepco-holdings | opus55-medium-20260928-1541-c4166b |
| petsmart | opus55-medium-20260928-1430-afdd33 |
| providence-worcester | opus55-medium-20260928-1420-8091a7 |
| stec | opus55-medium-20260928-1448-468449 |
| synacor | opus55-medium-20260928-1448-ae0ad0 |
| zep | opus55-medium-20260928-1537-b8400a |

Imprivata filing: `_dev/cockpit/state/filings/imprivata/imprivata_2016-08-10_DEFM14A.htm`.

Its SHA-256 is `c6e0661982bb95f9bd4397393cd84c74ab34c5d278890a28c926652fdc283910`. This matches `added_deals`.

Datalink filing: `raw_filing/datalink_2016-11-29_DEFM14A.htm`. The catalog records SHA-256 `437e0e7a76ea1326ddfcc81c2b287b2b15354752ae1bab6798b02a014ff7d4d3`.

## Exact evidence queries

Run each Git command within the named checkout. The recorded clean result is empty output from `git status --short`.

```bash
git rev-parse HEAD
git status --short
git log -1 --format='%h %ci %s'
sha256sum SEC_Deal_Ledger_Extraction_Instruction.md
systemctl --user show ledger-cockpit.service ledger-worker.service ledger-backup.service ledger-backup.timer sec-auction-remote.service -p Id -p LoadState -p ActiveState -p SubState -p MainPID -p WorkingDirectory -p ExecStart -p FragmentPath -p LastTriggerUSec -p NextElapseUSecRealtime
systemctl --user show ledger-cockpit.service ledger-worker.service ledger-backup.service -p Id -p ActiveEnterTimestamp -p ExecMainStartTimestamp -p ExecMainExitTimestamp -p ExecMainStatus -p NRestarts
df -h /home/uctpiaj/work /mnt/rdss/austin/data
```

The database connection used `sqlite3.connect(path.as_uri() + '?mode=ro', uri=True)`. It did not use `immutable`. `PRAGMA journal_mode` returned `wal`.

```sql
SELECT kind,state,COUNT(*) n,MIN(created_at) earliest,MAX(ended_at) latest FROM jobs GROUP BY kind,state;
SELECT state,failure_reason,COUNT(*) n FROM jobs WHERE state NOT IN ('completed') GROUP BY state,failure_reason;
SELECT id,kind,slug,state,created_at,started_at,pid,run_dir FROM jobs WHERE state IN ('queued','running','checking','importing','preparing');
SELECT slug,id,path,sha256,model,effort,instruction_version,instruction_sha256,started_at,finished_at,checker,hidden FROM versions ORDER BY slug,started_at;
SELECT slug,COUNT(*) n,MAX(revision) latest_revision,MAX(at) latest_at FROM revisions GROUP BY slug;
SELECT status,COUNT(*) n,MIN(at) earliest,MAX(at) latest FROM deal_review GROUP BY status;
SELECT id,name,status,sha256,created_at,updated_at,published_at FROM instructions;
SELECT key,value,updated_at FROM settings WHERE key LIKE '%instruction%';
SELECT slug,file,fetched_utc,bytes,sha256 FROM added_deals ORDER BY slug;
SELECT provider,COUNT(*) n,COUNT(DISTINCT user) users FROM accounts GROUP BY provider;
SELECT kind,COUNT(*) n,MIN(at) earliest,MAX(at) latest FROM activity GROUP BY kind;
```

SHA-256 checks used `hashlib.sha256(path.read_bytes()).hexdigest()`. XLSX reads used `openpyxl.load_workbook(path, read_only=True, data_only=True)`. No program assertion or test suite ran.

The process inspection read `/proc/<pid>/cwd`, `/proc/<pid>/exe`, and the program arguments. It reported only matching program paths. It read two named cockpit environment flags. It did not print credentials.

The source explains version paths at live `_dev/tools/cockpit/worker.py:343-361`. It explains the instruction store at `_dev/tools/cockpit/instructions.py:61-64`. It explains the seed edit at `_dev/tools/cockpit/instructions.py:105-108`. It explains backup manifests at `_dev/tools/cockpit/backup.py:346-349`.

No model run, export, source edit, database edit, service change, or deployment occurred. The only new file is this review report.
