# Slice C — instruction and documentation packets (exact restoration)
Files you own: `SEC_Deal_Ledger_Extraction_Instruction.md` (root), and everything under
`_dev/maintenance/2026-09-24-bid-terms-taxonomy/`, `_dev/maintenance/2026-09-26-astra-default-pro-verification/`,
`_dev/maintenance/2026-09-26-v1141-streamline/`, `_dev/reviews/2026-09-26-v114-15-run-trial/`,
`_dev/reviews/2026-09-26-v1141-retest/`.

Steps:
1. Root instruction: copy `_dev/recovery/2026-09-27-cockpit/instructions/v1.14.1_08caed447f7d.md` byte-exact to
   `SEC_Deal_Ledger_Extraction_Instruction.md` (Austin approved). Verify SHA-256 = the published hash recorded in the
   snapshot INDEX/instructions API JSON (starts `8a93df3c`). If the cockpit's export_repo would transform the text
   (e.g. strip a header), check `_dev/tools/cockpit/export_repo.py` at HEAD and follow it; report.
2. For every packet file under the directories above that appears in `/tmp/recov/evidence/INDEX.json` or as a heredoc /
   python write in `/tmp/recov/all_calls_since_0924.jsonl` (paths may be absolute under any of the three VM trees —
   map `sec-extraction-v114-trial-20260926/...` and `sec-extraction-v114/...` to the same repo-relative path, main tree
   wins on conflict, latest content wins within a tree): materialize its final content by rule 2 of the brief.
   Partial reads → write only if you can show the read covers the whole file (compare with `wc` output in evidence);
   otherwise do NOT write a truncated file: list it as missing.
   Binary files (png, docx, xlsx) cannot be recovered from text; list them.
3. The two instruction candidates (v1.14 candidate in taxonomy packet, v1.14.1 candidate in streamline packet): check
   against any sha256 recorded in evidence (`c2d47a47…`, `8bdb7c20…`); report whether they match.
4. v1.14.1 retest packet: copy the five 26 Sep rerun `.xlsx` exports from the snapshot into
   `_dev/reviews/2026-09-26-v1141-retest/` using the file names the VM packet used (find them in evidence; if unknown use
   `<slug>.xlsx`), and restore its README (final version: the fork session overwrote it; take the last write in time).
5. Questionnaire DOCX: if `evidence/a2/build_docx.py` is recoverable and its inputs exist locally, regenerate the DOCX
   into the packet (python-docx if installed; if not installed, do not install — report). Note in the packet README
   (one line) that the DOCX was regenerated on 27 Sep from the recovered builder.
6. Add `_dev/recovery/RESTORED_PACKETS.md`: table of every packet file: restored (EXACT/REPLAYED) / missing / binary lost,
   with the evidence timestamp used.
Acceptance: every restored file traces to a concrete evidence event; no truncated files; hash checks reported.
Effort guidance: mechanical, but be rigorous about completeness of reads.
