# Model comparison preflight status

19 September 2026. No filing extraction or grading was run.

## Installed runtime and requested model checks

- bubblewrap 0.11.1
- Codex CLI 0.155.1
- Claude Code 2.1.278
- OpenCode 2.0.9
- Python 3.14.7 with openpyxl 3.1.5
- The local Codex model registry lists `gpt-5.6-sol` and supports `xhigh`.
- The local OpenCode registry identifies `deepseek/deepseek-flash` as DeepSeek V4.1 Flash and lists `max` as a supported reasoning effort.

## Connectivity and tool-use probes

### Claude Opus

Status: complete end to end.

The sandbox invoked `claude --model opus --effort high` in safe mode with only Bash, Read and Write enabled, no MCP servers, no Chrome, no session persistence, and no web tools. The response metadata resolved the alias to `claude-opus-5` from the first-party provider. It reported zero web-search requests and no permission denials. The model read the toy input, imported openpyxl 3.1.5, wrote `smoke.xlsx` and `result.txt`, and the administrator reopened and validated the workbook outside the sandbox. Duration was 10.6 seconds. The original credential file was bound read-only into the temporary sandbox home; no credential copy exists in this directory.

Claude's experiment-design warning was that isolated run directories alone are insufficient for blind grading if workbook author/creator fields, filenames, timestamps or presentation order reveal model identity.

### DeepSeek V4.1 Flash

Status: provider connectivity verified; OpenCode route still needs repair.

A direct provider request with `model=deepseek-flash`, thinking enabled and `reasoning_effort=max` completed in 3.71 seconds and returned `model=deepseek-flash`. Its safe metadata is in `deepseek_direct_probe.json`. DeepSeek warned that logs, workbook metadata, run IDs and stylistic artifacts can unblind graders; it recommended normalized properties and filenames, randomized IDs and a preregistered rubric.

Two isolated OpenCode attempts used `--model deepseek/deepseek-flash#max`. Both failed before the provider request with `provider.no-route: Model unavailable: deepseek/deepseek-flash`; the second retained the non-secret local model registry cache. The minimal DeepSeek API credential was explicitly forwarded after `--clearenv`, so the remaining issue is OpenCode provider discovery/routing in fresh state, not demonstrated API unavailability. Preserve both failed event files; do not launch deal runs until a fresh-state OpenCode toy probe succeeds.

### GPT-5.6-Sol

Status: model connectivity verified; sandbox tool runtime incomplete.

The sandbox invoked `codex exec --model gpt-5.6-sol -c 'model_reasoning_effort="xhigh"'` with ephemeral state, ignored user configuration and rules, no project files mounted, and the original Codex credential file bound read-only. GPT-5.6-Sol answered and the event log records 400 reasoning output tokens. The shell action then failed closed because only the main Codex executable had been mounted: the companion `codex-code-mode-host` executable was absent. No toy workbook was written. Mount the complete Codex release `bin` directory, make the per-run model cache writable, and require a successful repeat of the same toy probe before extraction.

## Isolation evidence and remaining gate

Each bubblewrap probe used a fresh tmpfs home and temporary filesystem, a clear environment, a read-only toy input, a provider-specific output directory, and the common Python runtime. No filing, instruction, reference, earlier workbook, Git history, project memory, plugin, hook or MCP server was mounted. Network remained shared because it is required for provider APIs; disabled web tools and a filing-only prompt are controls, not physical API-only egress enforcement.

The preflight directory contains no file named as an auth token, credential, private key or certificate, and no credential was printed. Before launching the nine runs, the gate is: repair the OpenCode fresh-state route, mount Codex's complete tool host, rerun both toy probes successfully, freeze hashes and sanitized commands in the run manifest, and audit the resulting logs for secrets and external retrieval.
