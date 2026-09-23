# Phase 4 (instructions and engines) build contract

Implements §§5.2, 6.1, 6.3 and 9 of [the app spec](../../COCKPIT_APP_SPEC.md): instruction versions edited in the app (drafts, publish, default), runs with a chosen instruction, and the Fable 5.1, GPT-6-Sol and GPT-6-Astra engines with a per-user ChatGPT sign-in. Phases 1–3 rules stay (identity, CSRF, design, the worker, versions and bases). Backups, docs (§11) and hiding deals are phase 5.

Claude-only build (Austin, 23 September): Opus 5.5 leads and writes the backend and runner; an Opus 5.5 subagent writes the frontend. Do not read `ref/`, `_dev/reviews/` or `_dev/side-notes/`. Building and testing make no model calls; real runs need Austin's go-ahead.

## Research guarantees (unchanged)

- A run sees exactly one instruction text and one filing in the same bubblewrap sandbox; the checker runs afterwards, outside it.
- A run's instruction is the exact text frozen under its SHA-256 when the run is **requested**. Later draft edits never touch it. The version records the hash, and Compare reports whether two versions share it.
- Published instruction texts never change. Nothing in the app edits `SEC_Deal_Ledger_Extraction_Instruction.md`; it stays v1.13.2 until an export Austin requests (phase 5).
- A run uses the starting user's own plan for the engine's provider, never the other user's.

## Engines

| id | Label | Runner provider | Model | Account | Efforts | Note |
|---|---|---|---|---|---|---|
| `opus55` | Opus 5.5 | `opus` (the Claude transport) | `claude-opus-5-5` | claude | low–max | default, medium |
| `fable51` | Fable 5.1 | `opus` | `claude-fable-5-1` | claude | low–max | *experimental*; warning text in spec §6.1 |
| `sol6` | GPT-6-Sol | `sol` (the Codex transport) | `gpt-6-sol` | chatgpt | low–max | |
| `astra6` | GPT-6-Astra | `sol` | `gpt-6-astra` | chatgpt | low–max | |

`ultra` is never offered. The registry lives in `cockpit/runs.py` (`ENGINES`) and is served to the page in `GET /api/account`.

## Runner (`_dev/tools/sandbox/run_model.py`)

- Allow-list: `opus` gains `claude-fable-5-1`; `sol` gains `gpt-6-astra`. The served-model check and disabled refusal fallback apply to every Claude model.
- `SEC_CODEX_AUTH_FILE` names the Codex `auth.json` to bind read-only (default `~/.codex/auth.json`); the 7-hour rule applies to it. `models_cache.json` still comes from the host `~/.codex`.
- Fable's safeguard block ("…safeguards flagged this message…" in a result or assistant text) counts as a refusal → `provider_refusal`.
- Codex usage limit: a Sol run that did not finish and whose event log or stderr says "hit your usage limit" → `usage_limit`, with `usage_limit_message` (the provider's sentence) in `status.json`.
- `prepare --instruction` already takes any file; the cockpit passes its store copy.

## Instructions: storage

Same SQLite file, created idempotently:

```sql
CREATE TABLE IF NOT EXISTS instructions (
  id TEXT PRIMARY KEY,               -- 12 hex characters
  name TEXT UNIQUE,                  -- set on publish; null for a draft
  status TEXT NOT NULL,              -- 'draft' | 'published'
  parent_id TEXT, sha256 TEXT NOT NULL,   -- current text
  note TEXT,                         -- publish change note
  created_by TEXT NOT NULL, created_at TEXT NOT NULL, updated_by TEXT NOT NULL, updated_at TEXT NOT NULL,
  published_by TEXT, published_at TEXT);
CREATE TABLE IF NOT EXISTS instruction_edits (instruction_id TEXT NOT NULL, seq INTEGER NOT NULL, sha256 TEXT NOT NULL, author TEXT NOT NULL, at TEXT NOT NULL, PRIMARY KEY (instruction_id, seq));
CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT NOT NULL, updated_by TEXT NOT NULL, updated_at TEXT NOT NULL);
```

- Texts: `_dev/cockpit/state/instructions/<sha256>.md`, content-addressed, written atomically, never replaced.
- First use imports the repository's `SEC_Deal_Ledger_Extraction_Instruction.md` as a published version named from its header (`v1.13.2`), author `system`, and makes it the default (`settings.default_instruction`).
- Names: 1–40 characters of letters, digits, `.`, `-`, `_`, space; unique across published versions, never reused. Change note 1–2000 characters. Text 1 character to 400 KB, UTF-8.
- Drafts are never deleted. A draft's every save appends an `instruction_edits` row (seq 1 is its creation).
- Activity (slug `""`, account-wide): `instruction_draft` ("Started draft 3f2a9c1 from v1.13.2"), `instruction_published` ("Published v1.14: <note>"), `instruction_default` ("Made v1.14 the default instruction"). Draft saves are recorded only in the draft's own history.

## Instructions: API

- `GET /api/instructions` → `{default_id, items: [item…]}`, published first (newest first), then drafts (newest first). `item`: `{id, name, status, label, parent_id, parent_label, sha256, note, created_by, created_at, updated_by, updated_at, published_by, published_at, is_default, edits}` where `label` is the name, or `draft <sha7> (<Name>)` for a draft (author = `created_by`), and `edits` is the count.
- `GET /api/instructions/<id>` → `{item, text, parent_text, history: [{seq, sha256, author, at}]}`; `?seq=<n>` returns that edit's text instead of the current one. `parent_text` is the parent's current text, or null.
- `POST /api/instructions` (CSRF, known users) with one of:
  - `{action: "draft", from: <id>}` → new draft copying `from`'s current text, parent `from`. Returns the detail payload.
  - `{action: "save", id, text, base_sha256}` → drafts only; 409 if `base_sha256` is not the current sha (someone else saved). Unchanged text is a no-op. Returns the detail payload.
  - `{action: "publish", id, name, note}` → drafts only; freezes it. Returns the detail payload.
  - `{action: "default", id}` → published only. Returns the list payload.
  Published versions refuse `save` and `publish` with 409.

## Extraction jobs

- `POST /api/deal/<slug>/jobs` `{action: "extract", engine: "opus55", effort, timeout_minutes, instruction_id}`. `engine` defaults to `opus55`, `instruction_id` to the default. Refused (409) if the user has not connected the engine's account. The job's `params` become `{engine: <id>, engine_label, model, provider, account, effort, timeout_minutes, instruction: {id, label, name|null, status, sha256}}` — the sha is taken now, so a later draft edit does not change the run.
- The worker prepares with `--provider <provider> --model <model> --instruction state/instructions/<sha>.md` (after checking the file's hash), and gives the runner `SEC_CLAUDE_OAUTH_TOKEN_FILE` (claude) or `SEC_CODEX_AUTH_FILE` (chatgpt) for the starting user.
- Version id `<engine id>-<effort>-<yyyymmdd-hhmm>-<sha6>`; label `<Engine label> · <effort> · <instruction label> — <Name>, <D Mon HH:MM>`. `versions` gains `instruction_id`; `engine` holds the engine label and `instruction_version` the published name (null for a draft).
- Activity summaries name the engine and the instruction label.
- New failure reason `login_expired`: a ChatGPT login under 7 hours from expiry that a refresh could not renew ("Alex's ChatGPT login has expired; reconnect in Settings").

## ChatGPT accounts

- `codex login --device-auth` in a pipe (no pseudo-terminal), `CODEX_HOME=~/.config/sec-extraction/users/<user>/codex` (0700), in a worker thread. The worker parses the link (`https://auth.openai.com/codex/device`) and the one-time code (`XXXX-XXXXX`, ANSI stripped), stores them in the job result, state `waiting_for_approval`; on exit 0 with an `auth.json`, the account is `connected` and `expires_at` is the access token's expiry. Fifteen minutes, a failed exit or cancel end it. Job kind `connect_chatgpt`; one live per user.
- `accounts` row provider `chatgpt`; `expires_at` is refreshed from `auth.json` on every account read.
- **Refresh** (spike S2): when a connected user's access token has under 24 hours left and that user has no active GPT job, the worker (at most once an hour per user, under a per-user lock) runs `codex exec --ephemeral --skip-git-repo-check -s read-only -m gpt-6-sol -c model_reasoning_effort="low" "Reply with OK."` in an empty temp folder with the user's writable `CODEX_HOME`, then records whether `last_refresh` advanced. A queued GPT job whose user's token has under 7 hours left waits for this refresh; if the refresh does not renew it, the job fails `login_expired`. GPT jobs never start while that user's refresh runs.
- Disconnect deletes the user's Codex home (refused while that user's GPT runs are active).

## Accounts API

- `GET /api/account` gains `chatgpt: {connected, connected_at, expires_at, last_refresh}`, `chatgpt_connect: {job_id, state, link, code, error} | null`, and `engines: [{id, label, name, account, efforts, default_effort, experimental, note, connected}]`.
- `POST /api/account/chatgpt` `{action: "connect" | "cancel" (job_id) | "disconnect"}` → `GET /api/account`.

## Frontend

- **Instructions page** `/instructions`, linked in the header. A list (name or draft label, status, author, date, parent, default mark); selecting one shows its meta, note, hash and text. **New draft from this** on any version. **Make default** on a published non-default one (confirm). A draft opens in an editor (monospace textarea) with a side-by-side line diff against its parent (toggle), **Save draft** (409 → "Someone saved this draft since you opened it" with a reload), **Publish…** (dialog: name, required change note), its edit history (each entry viewable). The editor shows the advisory reminder: "A change should be general — the objective, the work process, honesty about uncertainty, a repaired contradiction or a deletion — never a rule justified by one reviewed deal (AGENTS.md)."
- **Extract dialog**: Engine select (all four; one whose account is not connected is disabled with "connect your Claude/ChatGPT account in Settings"); Fable shows the spec §6.1 warning; Effort limited to the engine's efforts, default medium; Instruction select (published, then drafts marked "draft"), default preselected; time limit. Summary: "Fable 5.1 · high · draft 3f2a9c1 (Alex) · on Austin's Claude plan" (+ "· usually 10–15 minutes" for Opus 5.5 at medium). Plan usage shown for Claude engines.
- **Settings**: a ChatGPT section like Claude's: status (connected since, login expires, last refreshed), **Connect ChatGPT account** → "1. Open this link and sign in with your ChatGPT account" + "2. Enter this code: XXXX-XXXXX" and "Waiting for you to approve…" (poll 2 s), Cancel, Disconnect (confirm; tells where to revoke: chatgpt.com → Settings → Security).
- **Runs tab**: the engine label from `params.engine_label`, the instruction label; failure texts name the plan (`usage_limit` → "Alex's ChatGPT plan hit its usage limit" + provider message if any; `provider_refusal` for `fable51` → "Blocked by Fable's safety filter"; `login_expired`).
- Activity renders the three instruction kinds (link to `/instructions`).

## Tests

- Python: runner allow-list, `SEC_CODEX_AUTH_FILE`, Fable refusal and Codex usage-limit classification; instruction store (import, draft, save and stale save, publish rules, names, default, edit history, frozen text); jobs API with engines and instructions (account check, frozen sha, params); worker passes provider, model, instruction path and the right credential variable, labels and ids; ChatGPT connect with a fake `codex` (link and code, approval, cancel), refresh (advance, failure → `login_expired`).
- Browser `test_instructions.mjs`: draft, edit, stale save, publish, default; a draft run and a published run on the same deal with the fake worker, and Compare reporting different instructions; the Extract dialog's engine gating; the ChatGPT connect flow with a fake `codex`.
- All earlier suites stay green.

## Acceptance (spec §12)

A draft run and a published run on the same filing show different instruction hashes; each engine completes one isolated run. Both need real model runs and Austin's go-ahead.
