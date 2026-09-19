# Extraction execution status

Updated 19 September 2026 at 16:30 UTC. All six Sol and Opus candidate extractions are complete. This file records administration only; no candidate has been opened for semantic review or corrected.

## Frozen inputs

- Instruction SHA-256: `f7e73a6673166597f2bd7c8c0457f72ba996585f1351595d00cd653f7a37009d`
- Mac-Gray filing SHA-256: `e6ea7bd00cfc389c28e5139a3d23aafcc684f7b65ff54d699f3c5be11bbc4301`
- PetSmart filing SHA-256: `52c93afa5897d1878441e76050f3c9607972624ea1e4105c29be815f4bf04ca9`
- Providence & Worcester filing SHA-256: `32d7a2738c95c29fa98fccc6a874a5e2acbfd0b7fc87a1f3e9145c60f627378a`

Every Sol and Opus run has its own copied instruction and filing plus per-run metadata containing these hashes. Each sandbox mounts only one instruction, one filing, one writable extraction directory, its provider runtime and its private client state. The root instruction was not modified.

## Models and launcher fixes

- Sol: exact model `gpt-5.6-sol`, effort `xhigh`, Codex CLI 0.155.1. The first preflight could reach the model but lacked the sibling `codex-code-mode-host`. The extraction harness mounts the complete standalone release read-only and gives each run a fresh writable Codex state. A new end-to-end toy probe then passed: shell execution, openpyxl 3.1.5, file writes and host workbook reopen.
- Opus: exact returned model ID `claude-opus-5`, effort `high`, Claude Code 2.1.278. Its prior end-to-end sandbox probe passed. Extraction uses safe mode, no session persistence, an empty MCP configuration, and only Bash, Read and Write tools; WebFetch, WebSearch and Task are denied.

The shared Sol/Opus harness is `run_model.py`. It preserves stdout events, stderr, command metadata, status, elapsed time and exit code. On completion it opens the expected workbook read-only outside the extractor sandbox and records only file validity, sheet names, size and SHA-256. It never repairs or overwrites a candidate.

## Run identifiers

| Run | Worker PID | Client PID | Launch time (UTC) |
|---|---:|---:|---|
| `opus_mac-gray` | 784884 | 784887 | 16:13:55 |
| `opus_petsmart` | 784886 | 784894 | 16:13:55 |
| `opus_providence-worcester` | 784899 | 784902 | 16:13:55 |
| `sol_mac-gray` | 786883 | 786885 | 16:15:15 |
| `sol_petsmart` | 786919 | 786946 | 16:15:15 |
| `sol_providence-worcester` | 786948 | 787026 | 16:15:15 |

All six have a 5,400-second ceiling. No automatic retry or checker-driven correction is enabled.

## Completed candidates

| Run | Exit | Seconds | Bytes | Candidate SHA-256 |
|---|---:|---:|---:|---|
| `opus_mac-gray` | 0 | 466.072 | 21,026 | `f599dd89d2d0f3e8e320389b5c78e1bacdc95420983438444c3b67186229175a` |
| `opus_petsmart` | 0 | 451.210 | 20,942 | `67a23b67bd66da2b84a1672ef85d8a37e6b79ebb2ff01432aceb591a5e8af4cb` |
| `opus_providence-worcester` | 0 | 546.270 | 22,455 | `458414ab3b3484d12250f1a1c41adb0b681dd924a8f6e5b8fc4bf9d6b75b2f38` |
| `sol_mac-gray` | 0 | 763.811 | 19,784 | `e568558177f2be1a8441aef7522eec6325fc9249cd533e20cca32ef609f20d0f` |
| `sol_petsmart` | 0 | 755.973 | 19,208 | `0db5afd35cb026e723dd8d3a115e087f785a9fe26a9f38ed3f16d4076dd9ef26` |
| `sol_providence-worcester` | 0 | 835.247 | 20,142 | `3c48ea690503acdd36bc8b695e6ddd74b76b7ff10d405e79c8cbd036a526389c` |

Every candidate reopened successfully as an XLSX and contains exactly the four expected sheet names: `Deal ledger`, `Rounds`, `Questions`, and `Deal facts`. These were read-only host checks. The candidate files were not repaired, normalized or overwritten.

## Source-use audit

The complete tool streams were checked for `curl`, `wget`, HTTP URLs and common Python network clients. No matching external-retrieval command appeared. Opus reported `webSearchRequests=0` for all three runs and no permission denials. Its tool events contain only the permitted local Bash/Read operations. Sol command events contain only local filesystem, Python and shell work.

Authentication was supplied only through read-only mounts from the external user credential stores. Bubblewrap left zero-byte destination placeholders in the private state directories after unmounting; all seven Sol/Opus and Sol-smoke placeholders were verified as empty and removed. No credential or key data remains in these run directories.
