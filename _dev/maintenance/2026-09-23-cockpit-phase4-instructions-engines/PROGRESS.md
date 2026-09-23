# Phase 4 (instructions and engines): build record

Contract: [CONTRACT.md](CONTRACT.md). Built by Opus 5.5 on 23 September 2026 (Austin: "build phase 4"): Opus 5.5 led and wrote the runner, backend and tests; an Opus 5.5 subagent wrote the frontend and `test_instructions.mjs`. No model was called in building or testing.

## What was built

- **Runner** (`run_model.py`): allow-list adds `claude-fable-5-1` (Claude transport, `--provider opus`) and `gpt-6-astra` (Codex transport, `--provider sol`). `SEC_CODEX_AUTH_FILE` names the Codex login to bind read-only (default the host's); the 7-hour rule applies to it. Fable's "safeguards flagged" block is `provider_refusal`. A Codex "hit your usage limit" error (from error or failed-turn events, or stderr, never from command output) is `usage_limit` with `usage_limit_message`.
- **Instructions** (`cockpit/instructions.py`, new): content-addressed texts in `_dev/cockpit/state/instructions/<sha256>.md`; `instructions`, `instruction_edits` and `settings` tables. The repository instruction is imported on first use as published `v1.13.2`, the default. Drafts (with edit history and stale-save refusal), publish (unique name, required note, frozen), make default (published only). Activity kinds `instruction_draft`, `instruction_published`, `instruction_default` with slug `""`.
- **Engines and runs** (`cockpit/runs.py`, `worker.py`): `ENGINES` registry (Opus 5.5, Fable 5.1, GPT-6-Sol, GPT-6-Astra) served in `GET /api/account`. An extract request names engine and instruction; the instruction's hash is frozen into the job when requested. The worker checks the stored text's hash, prepares with the engine's provider, model and `--instruction`, and passes the starting user's Claude token or Codex login. Version ids `<engine>-<effort>-<time>-<hash>`; labels name engine and instruction (`draft 3f2a9c1 (Alex)` for drafts); `versions.instruction_id` added.
- **ChatGPT accounts**: `connect_chatgpt` jobs run `codex login --device-auth` in a staging `CODEX_HOME`, publish the link and code, and on approval move it to `~/.config/sec-extraction/users/<user>/codex/` (0700, `auth.json` 0600); a failed or cancelled sign-in leaves an existing login untouched. Refresh per spike S2: under 24 hours left and no GPT run of that user going → one `codex exec` (GPT-6-Sol, low) with the user's writable `CODEX_HOME`, at most hourly; a queued GPT job within 7 hours of expiry waits for it and fails `login_expired` if it does not renew. Disconnect deletes the login (refused during that user's GPT runs); Claude disconnect is now refused only during Claude runs.
- **Server**: `GET /api/instructions`, `GET /api/instructions/<id>[?seq=n]`, `POST /api/instructions`, `POST /api/account/chatgpt`, page route `/instructions`.
- **Compare**: a catalog version without a hash is matched to the published instruction of the same name, so the nine catalog versions (v1.13.2) compare as the same instruction as runs on the imported v1.13.2.
- **Frontend**: Instructions page (list, detail, new draft, editor with side-by-side Myers line diff against the parent, save with stale handling, publish dialog, make default, edit history, AGENTS.md reminder, unsaved-text guard); Extract dialog with engine (unconnected ones disabled with a hint), Fable warning, effort, instruction, summary; Settings ChatGPT section (link and code, polling, cancel, disconnect with revoke hint); Runs tab and failure texts by engine and plan; Activity renders instruction items.
- **Docs**: cockpit README (ChatGPT, engines, Instructions) and tools README (transports, `SEC_CODEX_AUTH_FILE`, worker sign-in and refresh, fixture).

## Decisions made in the build

- The runner keeps its provider names: `opus` means the Claude Code transport and `sol` the Codex transport, so existing commands and receipts keep their meaning.
- The ChatGPT refresh is a real one-word model call on the user's plan (the only refresh path spike S2 found). It runs only when a login is within a day of expiry, so about once per ten-day login. Whether a call a day before expiry actually renews is still unconfirmed (host token expires 24 September 11:38 UTC); if it does not, the call after expiry will, and GPT runs wait in the meantime.
- No paste fallback for ChatGPT (the device flow needs no pseudo-terminal).
- Instruction activity is account-wide (slug `""`), shown on the Activity page, not in a deal's digest. The draft activity line names the draft by its hash at creation.
- Reading the instruction list creates the database if it is missing (it imports v1.13.2 on first use).

## Tests

See the session's run: Python (`test_cockpit_phase4.py`, 11 new; runner tests for Fable, Astra/Codex login and usage limit), `test_http.py` (new instruction/engine test), vitest (50), and browser suites on the staged build including the new `test_instructions.mjs`. Results are recorded under "Verification" below.

## Verification (23 September, 16:58 UTC)

- On the staged build: Python 189 passed (`python3 -m pytest -q _dev/tools`); `test_http.py` 12; vitest 50; browser `test_browser`, `test_resize`, `test_responsive`, `test_deals` and the new `test_instructions.mjs` (24 checks: ChatGPT device sign-in, engine gating, draft/stale save/publish/default, a Fable run on v1.13.2 and a Sol run on a draft completing with different instruction hashes, Compare's note, Activity) all passed.
- Deployed: `dist/` rebuilt, the live database backed up first (online backup, outside the repository), both services restarted at 16:57 UTC. `test_runs` and `test_trace` then passed on the deployed `dist/`. Live: `/api/instructions` lists published default `v1.13.2` whose hash (`513c8e3e8159…`) matches the repository file; ten deals listed; `/instructions` serves.

## Not yet done

- **Acceptance (spec §12):** a draft run and a published run on the same filing with different instruction hashes, and one isolated run per engine (Fable 5.1, GPT-6-Sol, GPT-6-Astra). These are real model runs and need Austin's go-ahead; GPT runs also need a connected ChatGPT account.
- Confirm on 24 September that the refresh renews a per-user Codex login.
