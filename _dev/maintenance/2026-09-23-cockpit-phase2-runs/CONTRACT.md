# Phase 2 (accounts and runs) build contract

Implements §§4–6 of [the app spec](../../COCKPIT_APP_SPEC.md) for existing deals: connect a Claude account, start and cancel isolated Opus 5.5 extractions from the cockpit, import finished runs as immutable versions, rebase the working copy onto a version, compare any two versions, and hide versions. Adding deals is phase 3; other engines and instruction editing are phase 4. In this phase the engine is always Claude Opus 5.5 (`claude-opus-5-5`) with a chosen effort, and the instruction is the repository's `SEC_Deal_Ledger_Extraction_Instruction.md` (v1.13.2).

Claude-only build: Opus 5.5 writes the backend (`_dev/tools/cockpit/*.py`, `_dev/tools/sandbox/run_model.py`, tests, systemd unit) and integrates; an Opus 5.5 subagent writes the frontend (`_dev/tools/cockpit/frontend/src/`). Read the phase 1 contract (`../2026-09-23-cockpit-phase1-trace/CONTRACT.md`) for conventions (identity, CSRF, design rules). Do not read `ref/`, `_dev/reviews/`, `_dev/side-notes/`.

## Research guarantees (unchanged)

A run sees exactly the instruction and one filing inside the existing bubblewrap sandbox (`run_model.py`); the checker runs after the provider exits, outside the sandbox; imported workbooks are never edited. No revision mode in the app. A run uses the token of the user who started it and never the other user's.

## Runner changes (`_dev/tools/sandbox/run_model.py`)

- **Cancel**: the `worker` subcommand handles SIGTERM by terminating the current provider process group (SIGTERM, then SIGKILL after 20 s) and ends with `state: "cancelled"`, `failure_reason: "cancelled"`, still writing usage and validation.
- **Plan usage**: Claude's stream has `{"type":"rate_limit_event","rate_limit_info":{status, rateLimitType, resetsAt, unifiedWindows:{five_hour:{utilization,resetsAt}, seven_day:{…}}}}`. `status.json` gains `plan_usage`: the last `rate_limit_info` seen (or null).
- **Usage limit**: if the run did not complete and any rate-limit event had `status: "rejected"`, `failure_reason` is `"usage_limit"` (checked before `provider_error`), and `status.json` gains `usage_limit_resets_at` (ISO time from `resetsAt`).
- The per-user token path is passed with the existing `SEC_CLAUDE_OAUTH_TOKEN_FILE` variable.

## Storage

Same SQLite file. New tables (created idempotently on write connections, as in phase 1):

```sql
CREATE TABLE IF NOT EXISTS jobs (
  id TEXT PRIMARY KEY, kind TEXT NOT NULL,          -- 'extract' | 'connect_claude'
  slug TEXT, actor TEXT NOT NULL, created_at TEXT NOT NULL,
  state TEXT NOT NULL,     -- extract: queued|preparing|running|checking|importing|completed|failed|timed_out|cancelled
                           -- connect: queued|waiting_for_code|completing|completed|failed|cancelled
  params TEXT NOT NULL,    -- JSON: {model, effort, timeout_minutes} for extract
  cancel_requested INTEGER NOT NULL DEFAULT 0,
  input TEXT,              -- connect: the pasted code, cleared after use
  pid INTEGER, run_dir TEXT, started_at TEXT, ended_at TEXT,
  failure_reason TEXT, error TEXT,
  result TEXT,             -- JSON: extract {usage, plan_usage, checker{errors,warnings}, continuations, elapsed_seconds, usage_limit_resets_at}; connect {link}
  version_id TEXT);
CREATE TABLE IF NOT EXISTS accounts (user TEXT NOT NULL, provider TEXT NOT NULL, connected_at TEXT NOT NULL, expires_at TEXT, PRIMARY KEY (user, provider));
CREATE TABLE IF NOT EXISTS plan_usage (user TEXT NOT NULL, provider TEXT NOT NULL, at TEXT NOT NULL, info TEXT NOT NULL, PRIMARY KEY (user, provider));
CREATE TABLE IF NOT EXISTS versions (
  slug TEXT NOT NULL, id TEXT NOT NULL, label TEXT NOT NULL, path TEXT NOT NULL, sha256 TEXT NOT NULL,
  kind TEXT NOT NULL,                  -- 'raw'
  engine TEXT NOT NULL, model TEXT NOT NULL, effort TEXT NOT NULL,
  instruction_version TEXT, instruction_sha256 TEXT NOT NULL, filing_sha256 TEXT NOT NULL,
  started_by TEXT NOT NULL, started_at TEXT NOT NULL, finished_at TEXT NOT NULL,
  receipts TEXT NOT NULL,              -- repository-relative folder with the run receipts and check.json
  checker TEXT NOT NULL,               -- JSON {errors, warnings}
  hidden INTEGER NOT NULL DEFAULT 0, hidden_by TEXT, hidden_at TEXT,
  PRIMARY KEY (slug, id));
```

- Tokens live outside the repository in `~/.config/sec-extraction/users/<user>/claude-oauth-token` (directory 0700, file 0600), the same protection the runner already requires for its token file. They are never returned by the API or logged. (Spec §5.3 asked for encryption at rest; with the key on the same VM that adds little, so file permissions are the control. Recorded as a deviation.)
- Imported versions: `_dev/cockpit/state/versions/<slug>/<version-id>/` holding `<slug>.xlsx`, `check.json` and the receipts `metadata.json`, `command.json`, `status.json`, `validation.json`, `provider-results.json`, `prompt.txt`. Failed runs keep their receipts in `_dev/cockpit/state/jobs/<job-id>/`. The `_dev/runs/cockpit-<job-id>` run folder is deleted after either.
- Version ids: `opus55-<effort>-<YYYYMMDD-HHMM>-<first 6 of sha256>`. Label: `Opus 5.5 · <effort> · v1.13.2 — <Name>, <D Mon HH:MM>` (UTC).

## Working base, rebase, restore

- The working copy's base is the `base_id` of its latest revision, else the catalog's `default_base`. (`_state` currently compares the latest revision to the catalog default and raises; it now resolves the base from the revision.)
- `Workspace.item(slug)` merges DB versions (including hidden ones) after the catalog versions, so `version()`, `deal(version=…)` and `export` work for imported versions.
- New edit operation, alone in its request: `{"type": "rebase", "target_version": "<id>"}`. The new revision's snapshot is the target version's state, its base is the target, and its `changes` are the diff from the previous working state. Activity kind `rebase`. Refused if the target is already the base or hidden.
- `restore` to revision R also restores R's base (revision 0 means the catalog `default_base`).
- `field_authors` needs no change: a rebase's diff attributes every row to the rebaser.

## Compare

`GET /api/deal/<slug>/compare?from=<version id|working>&to=<version id|working>` returns `{"from_label", "to_label", "same_instruction": bool, "changes": [...]}` with the same change shape as `/changes`. Rows are matched by a sheet key, not by uid: ledger `#`, Rounds `(Process, Round)`, Questions `Q`, Deal facts `Field`; unmatched rows are inserts or deletes. `same_instruction` compares instruction hashes when both versions have one, else null.

## Worker (`_dev/tools/cockpit/worker.py`, `ledger-worker.service`)

A separate user service (`KillMode=process`, `Restart=always`) running `python3 _dev/tools/cockpit/worker.py`. Every 2 s it:

1. **Reattaches or fails orphans**: a job in `preparing|running|checking|importing` whose `pid` is dead is finalised from its run folder's `status.json` if that exists (completed runs are then checked and imported), else `failed / worker_restart`.
2. **Cancels**: for `cancel_requested` jobs: queued → `cancelled`; running → SIGTERM to the runner worker's pid (the runner records `cancelled`).
3. **Starts extract jobs** in creation order within the caps: at most 4 running extract jobs overall and 2 per user. Start = `run_model.py prepare --provider opus --run-dir _dev/runs/cockpit-<id> --deal <slug> --filing <file> --model claude-opus-5-5 --effort <e> --timeout-minutes <t>`, then spawn `run_model.py worker --provider opus --run-dir …` in a new session with `SEC_CLAUDE_OAUTH_TOKEN_FILE` set to the starting user's token file; record its pid. The filing is the deal's file in `raw_filing/` per the manifest. A user without a connected Claude account → `failed / not_connected`.
4. **Finishes** jobs whose runner exited: read `status.json`; `completed` → `checking` (run `check_lean.py` outside the sandbox) → `importing` → `completed` with `version_id`; otherwise the runner's state and `failure_reason`. Store `plan_usage` for the user. Write activity rows: kind `extraction` (summary e.g. "Opus 5.5 · medium · v1.13.2 extraction finished: 0 errors, 12 warnings") or `extraction_failed` (summary names the reason).
5. **Connect jobs** (one live per user; a new one cancels the old): run `claude setup-token` in a pseudo-terminal (500 columns) with a scratch HOME and `BROWSER=/bin/false`; parse the `https://claude.com/cai/oauth/authorize…` link; store it in `result.link`; state `waiting_for_code`. When `input` arrives, write it plus Enter, clear `input`, state `completing`, and read until a token matching `sk-ant-oat\d\d-[A-Za-z0-9_-]{20,}` appears; save it (0600), upsert `accounts` (expires in 365 days), state `completed`. Ten minutes without a code, an exit without a token, or cancel → `failed`/`cancelled` with a plain error. Connect sessions run in threads so they do not block extract jobs.

The HTTP server never starts processes or makes network calls; it only writes job rows.

## API (all writes: same identity, CSRF, Origin and size checks; `unknown` cannot write)

- `GET /api/account` → `{"user", "claude": {"connected": bool, "connected_at", "expires_at", "plan_usage": {"at", "five_hour": {"utilization", "resets_at"}, "seven_day": {…}} | null}, "connect": {"job_id", "state", "link", "error"} | null}` (the latest connect job if not completed more than 10 minutes ago).
- `POST /api/account/claude` with one of `{"action":"connect"}`, `{"action":"code","job_id","code"}`, `{"action":"cancel","job_id"}`, `{"action":"token","token"}` (paste fallback: validated by the regex, saved like a completed connect), `{"action":"disconnect"}`. Returns `GET /api/account`.
- `GET /api/deal/<slug>/jobs` → `{"jobs": [...]}` newest first (limit 30): `{id, state, actor, created_at, started_at, ended_at, params, failure_reason, error, result, version_id, cancel_requested}`.
- `POST /api/deal/<slug>/jobs` with `{"action":"extract","effort":"medium","timeout_minutes":90}` (effort in low|medium|high|xhigh|max; timeout 10–360) or `{"action":"cancel","job_id"}`. Extract is refused (409) if the user has no connected Claude account. Returns the jobs payload.
- `POST /api/deal/<slug>/versions` with `{"action":"hide"|"unhide","version_id"}` (imported versions only; hiding the current base is refused). Activity kinds `hide`/`unhide`.
- `GET /api/deal/<slug>/compare?from=&to=` (above).
- `GET /api/deal/<slug>` → each entry in `versions` gains `engine`, `effort`, `started_by`, `started_at`, `hidden`, `is_base`, `checker`; catalog versions get `engine: "Opus 5.5"`, `effort: "medium"` where known from their label, else null. Hidden versions are listed (the frontend hides them unless asked) so that links keep working. `workspace.base_version` is the resolved base.
- `GET /api/deals` → each deal gains `active_jobs` (count of queued/preparing/running/checking/importing) and `unseen.by[actor].runs` (activity kinds `extraction`, `extraction_failed`).
- `GET /api/activity` includes the new kinds.

## Frontend behaviour

Same design rules as phase 1.

1. **Settings page** `/settings`, linked from the header as the user's name. It has a Claude account section: status (connected since, expires, plan usage "5-hour: 10% · weekly: 29% · as of 23 Sep 14:05"); **Connect Claude account** → shows "1. Open this link and approve with your claude.ai login" (the link, opening in a new tab) and "2. Paste the code shown" (input + Submit), with Cancel; progress states and plain errors; a collapsed "Paste a token instead" fallback explaining `claude setup-token`; **Disconnect** with confirmation. Poll `GET /api/account` every 2 s while a connect is in progress.
2. **Extract** button in the deal toolbar (edit-capable users). Dialog: engine shown as fixed text "Claude Opus 5.5" (a note that more engines come later), effort select (default medium), time limit (default 90), and the summary line "Opus 5.5 · medium · v1.13.2 · on <Name>'s Claude plan · usually 10–15 minutes", plus plan usage if known. Not connected → the dialog explains and links to Settings instead of a Start button.
3. **Runs tab** in the deal workspace: the jobs list with state, who, when, elapsed (ticking for active jobs), effort, tokens/cost if present, checker counts, a link "Open version" for completed runs, and **Cancel** for queued/running ones. Failure reasons in words: `usage_limit` → "<Name>'s Claude plan hit its usage limit; it resets <time>", `provider_refusal` → "The model refused", `timeout`/`timed_out` → "Ran past the time limit", `not_connected` → "No Claude account connected", `cancelled` → "Cancelled by <Name>", `worker_restart` → "Interrupted by a server restart", others → "Failed (<reason>)". Poll `GET …/jobs` every 5 s while any job is active; when one completes, refresh the deal so the new version appears.
4. **Version dropdown**: Working copy first, then originals newest first by `started_at` (catalog versions last); the base is suffixed "· base". Hidden versions are omitted unless "Show hidden versions" is ticked (a small control next to the dropdown or in the Runs tab).
5. When viewing an original that is not the base: toolbar buttons **Use as working-copy base…** (confirm dialog with a required reason; posts the `rebase` edit; on success switch to the working copy) and **Hide** / **Unhide** for imported versions.
6. **Changes tab** gains "Compare" selectors (from/to over all versions plus Working copy; default from = base, to = Working copy) using `/compare`, with a note when `same_instruction` is false. The existing base-vs-working view is the default selection.
7. **Overview**: a muted "Extraction running" line for deals with `active_jobs > 0`; the digest line includes runs ("Alex · 1 run, 2 edits").
8. What's new and Activity render the new kinds (`extraction`, `extraction_failed`, `rebase`, `hide`, `unhide`); an `extraction` item links to its version.

## Tests and acceptance

- Runner unit tests (extend `_dev/tools/test_run_model.py`): SIGTERM cancel outcome; `plan_usage` capture; `usage_limit` classification.
- Backend tests (`_dev/tools/test_cockpit_runs.py`): DB versions merge into items; rebase/restore base resolution; hide rules; compare keyed matching; jobs API validation and caps; worker lifecycle with a **fake runner** (a script standing in for `run_model.py` that writes a copy of a fixture workbook and a `status.json`) covering completed → imported version, failed, cancelled, usage-limit, worker restart; connect flow with a fake `claude` that prints a link, reads a code and prints a token.
- Browser acceptance (`test_runs.mjs`) with the fake runner and fake `claude`: connect via the UI, start an extraction, see it complete and the version appear, open it, rebase onto it, compare, hide it.
- Real runs are separate and need Austin's go-ahead.
