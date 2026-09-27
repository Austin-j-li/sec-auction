# Lane B: VM activity since 26 Sep 2026 20:00 UTC

Checked 27 Sep 20:36–20:40 UTC over SSH, read-only.

## Verdict

- **No instruction, default, run, deployed code, cockpit or commit change after 26 Sep 20:45 UTC.** The last change to the cockpit database was at 26 Sep 20:41:52: the Datalink import, the fifth v1.14.1 retest run. No comment, working-copy edit, or deal add or hide happened after that either. The live database's rows match the 27 Sep 03:30 nightly backup exactly. The worker cap in live `runs.py` is back at `per_user: 2` (checked by grep; it matches the v114 copy).
- **One exception: uncommitted working-tree edits until 20:52 on 26 Sep, nothing after.** Two VM Claude sessions (a7e6612a and its fork aa666d5e) finished a staleness pass on about 60 files in `~/work/Projects/sec-extraction`. Most are docs. The rest are one review script (`grading/mechanical_check.py`), a docx for Alex with its evidence files, and a new `_dev/tools/cockpit/deploy/PROPOSED-tmpdir.md`. None of it was committed. HEAD in both checkouts is still `679d4fc` (23 Sep), and the live tree has 99 uncommitted paths. No file in either checkout changed after 26 Sep 21:00.
- **Nothing from Alex's account.** His last recorded action is 24 Sep: he connected Claude at 09:19 and viewed Zep at 09:29.
- **The 19:59 transcript change is not a conversation.** `f40a7cfe` is an idle, still-running 22 Sep Claude process. Every ~3 h 52 min it appends an `artifact-autoreact-ledger` bookkeeping line; the last came at 27 Sep 19:59:38. Its last real message is dated 22 Sep 23:19. The Codex databases were touched today because a Codex Desktop client connected over SSH at 27 Sep 20:26:54. It only listed threads and ran git and pwd probes; it started no turn.
- **SSH.** The first SSH login after 26 Sep 20:45 was at 27 Sep 20:26 (the Codex Desktop client), followed by laptop sessions from 20:31. All used the same ED25519 key. Earlier today the only traffic was through the public cockpit URL (Cloudflare tunnel): an automated read of every deal at 10:54, and a page load at 14:38. Neither can be attributed, and both were GET-only.

## Timeline (UTC)

| Time | Actor | Event | Source |
|---|---|---|---|
| 26 Sep 20:08–20:19 | VM Claude a7e6612a ("v1.14.1 pipeline upgrade") and its fork aa666d5e | The original session's browser tool hung. The fork, working in Austin's signed-in VM browser, created draft `08caed447f7d` (20:18:24), published it as **v1.14.1** and made it the default (20:18:33), then queued 5 extract jobs (20:19:04). The cockpit records all of this as `austin`. A later message from session a7e6612a says the fork did it, not Austin by hand. | cockpit `activity` 57–59, `instructions`, `settings`; transcripts aa666d5e and a7e6612a |
| 26 Sep 20:19–20:41:52 | ledger-worker; user `austin` | Five Opus 5.5 medium runs on v1.14.1 (instruction sha 8a93df3c), checked by checker 1.8. Mac-Gray 0 errors / 2 warnings, P&W 0/2, sTec 1/3, Synacor 0/6, Datalink 1/4. About $1.8–2.9 each. | cockpit `jobs`, `versions`, `activity` 60–64; worker journal |
| 26 Sep 20:29–20:43 | Codex thread 01a0df68 (VS Code, gpt-6-astra high) | User prompt: "i have done some changes. scan through and lmk the status". Spawned three audit subagents (Kant, Hegel, Leibniz; role `evidence_explorer`). Last item 20:42:22. Threads shut down at 23:20. No later turns. | codex `state_5.sqlite`, `thread_history_1.sqlite`, `logs_2.sqlite` |
| 26 Sep 20:31–20:32:11 | fork aa666d5e (on the user's "parallelize the rest") | Raised the worker cap to 3 in `runs.py`, restarted ledger-worker (20:32:03) so Datalink could start, then set the cap back to 2 and restarted again (20:32:11). The worker has run as PID 929934 since then. `runs.py` mtime 20:32:11; on 27 Sep a grep confirmed it holds `CAPS = {"total": 4, "per_user": 2}`. | aa666d5e transcript; worker journal |
| 26 Sep 20:42–20:52 | a7e6612a and fork aa666d5e, plus subagents | Wrote the retest write-up `_dev/reviews/2026-09-26-v1141-retest/` (README and analysis CSVs) and the deploy receipt `deployment-v1141.json`. The staleness pass then edited about 60 files: AGENTS.md, README.md, HANDOFF.md, `_dev/HANDOFF.md`, CHRONOLOGY, RESEARCH_QUESTIONS, COCKPIT_APP_SPEC/BUILD, the v1.14/v1.14.1 packets, the taxonomy packet, `Questions_for_Alex_2026-09-25.docx` with its a2 evidence PNGs and PDF, and older review READMEs. It also added `_dev/tools/cockpit/deploy/PROPOSED-tmpdir.md`. The fork's staleness agent was stopped at 20:48 after the two sessions coordinated. None of this was committed, pushed or sent to Alex. | file mtimes; transcripts a7e6612a and aa666d5e (subagents ad2095e4, ae9154da, aef263bf, af5887b7) |
| 26 Sep 20:52:46 | a7e6612a | Final report: "v1.14.1 is live … Nothing was committed, pushed or sent to Alex." | a7e6612a transcript |
| 26 Sep 20:54–20:55 | Austin → a7e6612a | User: "lesson are stale now?" The agent answered from other docs without opening `lesson/`. **This is the last real message in any VM agent transcript.** | a7e6612a transcript |
| 26 Sep 20:55 | Codex housekeeping | `goals_1`/`memories_1` sqlite mtimes. The memories job's last finish was 20:29:53. | file mtimes |
| 26 Sep 23:20 | Codex app-server | Shutdown of thread 01a0df68 and its subagents (teardown only). | codex logs |
| 26 Sep 20:46 → 27 Sep 20:26 | Codex app-server | Only the background `list_models` poll, about 50 per hour. One timeout error at 27 Sep 16:55. | codex logs |
| every ~3 h 52 min from 26 Sep 20:47 to 27 Sep 19:59:38 | idle Claude process f40a7cfe (started 22 Sep) | Appended `artifact-autoreact-ledger` lines (bookkeeping for artifact `bde38bab…`; no threads, no turns). This explains the transcript's 19:59 mtime. | local transcript copy |
| 27 Sep 03:30 | backup timer | Nightly backup `~/backups/ledger-cockpit/20260927-033000Z`. It shows the same 17 table counts as live (activity 64, jobs 23, versions 12, instructions 4). A row-by-row comparison against the live DB matches. | backup `manifest.json`; read-only comparison |
| 27 Sep 06:11 | vm-browser-chrome | One GCM "connection reset" log line. No other activity. | journal |
| 27 Sep 10:54:02–10:55:20 | **unattributed**, via the public cockpit URL (tunnel) | 177 GETs in 78 s: `/api/session`, `/api/account`, all 13 deals (deal, filing, history, changes, comments, jobs, activity, and exports of every version plus `working`), every instruction and each edit step (4 × 404 for steps that do not exist), `/api/activity`, `/api/seed`. No POST. This looks like a scripted full read or export. The cockpit logs do not record the user. | cockpit journal |
| 27 Sep 14:38:57–14:39:01 | **unattributed**, via the tunnel | Browser page load: `/`, assets, `/api/session`, `/api/deals`. GET only. | cockpit journal |
| 26 Sep 20:45 → 27 Sep 20:40 | hermes-gateway (Slack bot) | Continuous "Failed to connect (Session is closed); Retrying" loop, about 7,900 lines per hour. It did not function, and it is unrelated to the project. | journal |
| 27 Sep 20:26:54 | Codex Desktop client v26.924.22138, over SSH (the first SSH login since 26 Sep) | Started `codex app-server proxy`: initialize, auth status, thread list, plugin sync, `marketplace/add`, one `fs/remove`, and about 25 `process/spawn` calls (`pwd -P`, git status probes). `model/list` at 20:28. No thread turn. This is why the Codex state DB mtimes and WAL files changed today. | codex `logs_2.sqlite`; `ps`; sshd journal |
| 27 Sep 20:31–20:39 | laptop agents (this investigation and a parallel lane), same SSH key | Read-only SSH commands. | sshd journal |

## Service health (27 Sep 20:37)

- ledger-cockpit: active since 26 Sep 19:45:09 (PID 862517). Last POST 26 Sep 20:19:04.
- ledger-worker: active since 26 Sep 20:32:11 (PID 929934). Its journal has 14 lines since 26 Sep 20:00, the last at 20:41:52 (Datalink imported). Nothing after that.
- cloudflared: active. The vm-browser-* units are active. The failed units are only the xdg portals.
- Latest backup: `20260927-033000Z`. Its manifest records git_head `679d4fc` and checker 1.8.

## Cockpit accounts (for reference)

`austin` has connected Claude (since 23 Sep) and ChatGPT (expires 3 Oct). `alex` has connected Claude (since 24 Sep 09:19). Across all history, Alex's account shows 1 job (`connect_claude`, 24 Sep) and 1 `seen` row (Zep, 24 Sep 09:29); no runs, edits, comments or instruction actions.

## Caveats

- The cockpit does not record who made GET requests, and all tunnel traffic reaches it as 127.0.0.1. So the 10:54 and 14:38 reads cannot be tied to Austin, Alex or an agent from VM logs alone. The 4 × 404s at the next edit step of each instruction look like a script that loops until it gets a 404. A quick search of the laptop's Claude transcripts found no cockpit API calls between 10:30 and 11:10. The laptop's first Codex session on 27 Sep started at 11:37, after the crawl. So it is still unattributed.
- My first read-only open of `workspace.sqlite3` (`mode=ro`) at 20:36:43 created empty `-wal`/`-shm` side files, because the DB is in WAL mode. They were gone at the next check. The DB file itself (mtime 26 Sep 20:41:52) and its rows were unchanged. Later reads used `immutable=1`.
- `wtmp` does not record non-pty SSH sessions. The sshd journal (`_COMM=sshd-session`) was used for logins instead. It shows no accepted login between 26 Sep 20:45 and 27 Sep 20:26.
