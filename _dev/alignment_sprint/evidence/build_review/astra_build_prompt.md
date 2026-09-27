You are reviewing a build specification before it is handed to an agent team that has none of the context behind it. Repository: /Users/austinli/Projects/sec-auction (branch local-recovery-2026-09-27, commit 44e3446). Read-only: change nothing.

Documents under review:
- _dev/alignment_sprint/BUILD_SPEC.md (entry point: VM setup, app rebuild, stop points)
- _dev/alignment_sprint/DRAFTING_SPEC.md (instruction draft and tool changes; sections 4.13–4.15, the section 7 regression anchors and section 8 item 6 are new tonight)
- _dev/alignment_sprint/DECISIONS.md, especially "Evening rulings" at the end (all decisions there are Austin's final rulings)

Supporting material:
- Current instruction: SEC_Deal_Ledger_Extraction_Instruction.md; tools: _dev/tools/check_lean.py, _dev/tools/derive_analysis.py, _dev/tools/fetch_filing.py
- Alex's sources: _dev/alignment_sprint/evidence/voice_notes.txt, collection_instructions.txt; ref/deal_details_Alex_2026.xlsx
- VM reconciliation: _dev/alignment_sprint/VM_RECONCILIATION.md and _dev/alignment_sprint/vm_check/*.md
- The app code as deployed on the VM: git branch origin/vm-live-2026-09-26 (use `git show origin/vm-live-2026-09-26:<path>` or `git ls-tree`), e.g. _dev/tools/cockpit/{data,workspace,worker,deals,provenance,server,runs,instructions}.py, _dev/cockpit/catalog.json. A snapshot of the VM tree including a copy of the app's SQLite state is at /private/tmp/claude-501/-Users-austinli-Projects-sec-auction/9347f1c0-862f-41cd-84cb-0e8e34390ba2/scratchpad/vm/vm-tree (open the database only with sqlite URI mode=ro&immutable=1). It contains live account tokens: never print token values.
- Filing text: /private/tmp/claude-501/-Users-austinli-Projects-sec-auction/9347f1c0-862f-41cd-84cb-0e8e34390ba2/scratchpad/audit/txt/*.txt

Ground rules for this review:
- The decisions are settled. Do not reopen or re-argue any decision, the working rule, or the choice to archive old app data. Do not propose new process, new documents, new tooling or extra safeguards unless their absence would concretely cause a wrong result, a broken app, lost data or a leaked secret.
- Report only findings that would (a) make a competent builder with no other context guess or get it wrong, (b) produce a ledger outcome that contradicts a decision or a section 7 anchor, (c) break the rebuilt app, or (d) risk the live app, data or secrets. Style preferences, wording polish and "could be clearer" are out of scope.
- Every finding needs evidence (file:line or quoted text, or a query result) and the smallest fix, stated as the exact wording or change.

Check in particular:
1. Evening ruling 2 / reconciliation 14 (a bidder's own statement of the price it would offer is a Bid, incl. a ceiling or range) against F11, E10, V¶68 and the other anchors: does it create a wrong outcome anywhere in the nine deals' anchors?
2. Evening ruling 1 / reconciliation 13 (Synacor round opens Oct 27, 2020 by (d); Dec 30 continues) against R3, E6 (d), R8 and the Synacor process map.
3. Part B against the actual app code on vm-live-2026-09-26: is the adapter list complete enough for the tests to find the rest; will a deal with no version work or does the spec need to say more; does keeping only the accounts table plus deals/filings leave the fresh state consistent (foreign keys, settings, plan_usage, added_deals, hidden_deals, migrations table); anything the switch-over runbook must cover that the spec omits.
4. Anything in BUILD_SPEC that could lead a builder to change the live checkout, stop the services, or commit a secret.

Output: a numbered list, each item tagged BLOCKER or SHOULD, with evidence and the smallest fix. At most 12 items; merge duplicates. If there are no blockers, say "No blockers" first. No preamble, no summary of the documents.
