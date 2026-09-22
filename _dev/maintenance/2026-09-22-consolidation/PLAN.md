# Consolidation cleanup plan — 22 September 2026

Austin authorized hard deletion of the Grok and GPT-5.6-Sol extraction comparison results. The exact pre-deletion paths, byte counts, and SHA-256 hashes are in `deletion-inventory.json`; it includes ignored files and the `.git` pointers. No copy or backup of the discarded comparisons will be made. `protected-inputs-before.json` records all 20 cockpit catalog workbook versions, ten `raw_filing/` files, the instruction, production runner and catalog before cleanup. No production SQLite file existed at inventory time.

| Target | Files | Bytes | Disposition |
| --- | ---: | ---: | --- |
| `/home/uctpiaj/work/Projects/sec-extraction-grok-v113` | 153 | 42,866,709 | Remove entire worktree, then branch `grok/v1.13-eight-deals`. |
| `/home/uctpiaj/work/Projects/sec-extraction-sol-opus-v113` | 217 | 17,425,002 | Remove entire worktree, then branch `codex/v1.13-sol-opus-comparison`. |
| Main `_dev/reviews/2026-09-21-three-models` | 12 | 2,218,775 | Delete folder after parent handoff edits remove active references. |
| Main `_dev/PIPELINE_DIRECTION.md` | 1 | 8,486 | Delete after parent handoff carries forward relevant review boundaries. |
| Detached worktree `.../worktrees/7877/sec-extraction` | 141 | 18,523,456 | Preserve directory inode for live processes; delete its project files, unregister exactly this worktree, and leave `RELOCATED.md` with the main checkout and Astra packet destinations. |

The detached tree's 23 files absent from main are exactly the Astra packet copied byte-for-byte to `_dev/side-notes/2026-09-21-astra-mac-gray/`: 22 manifest entries plus `EVIDENCE_MANIFEST.json` (99,536 bytes total). The ten other differing files are old snapshots of the main supporting documents, ignore rules and cockpit code. In particular, main's Datalink documents include Austin's later F9 decision; main's cockpit code includes the subsequent editable implementation. The detached handoff/chronology also mention the Astra trial; the original trial record survives in the side-note packet. The per-file differences are in `detached_7877_worktree-vs-main.json`.

The process scan found only four references to a removal target: PIDs 1756020, 1756031, 1756045 and 1756217 have the detached directory as their cwd. None had target file descriptors or mapped files. They are sleeping MCP/advisor children of the Codex app server. Do not kill or restart them. Keep the detached top directory's inode and exact path. The user systemd cockpit service points to the main checkout. A dry-run `git worktree prune -n -v --expire now` proposed no cleanup before retirement. For detached registration, verify its `.git` pointer names only `.git/worktrees/sec-extraction`, remove exactly that pointer and admin directory, then verify `git worktree list` retains main only. Do not run a broad forced prune. The two branch worktrees have dedicated admin entries; remove with Git's worktree command after rechecking their paths and inventories, then delete the named branch refs.

The bounded visualization tree `/home/uctpiaj/work/agent-homes/.codex-20260905-222709/visualizations/2026/09/21` contains zero files, so there are no exported comparison copies there.

The parent lead reviewed the inventory and directed execution. After removing the detached project's files, a fresh prune dry run identified only its `.git/worktrees/sec-extraction` registration; the actual prune removed that same single registration. `cleanup-result.json` records removal and exact counts. `protected-inputs-after.json` confirms that all 33 protected files matched their pre-cleanup byte counts and hashes. The Astra packet, Git worktree/branch status, and live process cwd boundary were also verified after cleanup.
