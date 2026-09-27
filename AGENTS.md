# AGENTS.md

This project turns the "Background of the Merger" section of an SEC merger filing into an Excel deal ledger, for research on informal and formal bidding in takeover auctions (Austin Li and Alex Gorbenko).

## If you are asked to extract a deal
- Follow `SEC_Deal_Ledger_Extraction_Instruction.md` exactly. Use only that instruction and the filing you are given in `raw_filing/`.
- Save the workbook in `extraction/` as `<deal>.xlsx`.
- Do not read `_dev/`, `ref/`, other workbooks in `extraction/`, or git history. They contain analyses and the researcher's hand-coded answers, and reading them invalidates the extraction.
- Do not use the web. Do not identify anonymous bidders from outside knowledge.

## Layout
- `SEC_Deal_Ledger_Extraction_Instruction.md`: the instruction, version 0. Agents edit it only with Austin's approval.
- `raw_filing/`: filings to extract, fetched from EDGAR by `_dev/tools/fetch_filing.py`. `MANIFEST.csv` records each file's source link and SHA-256.
- `extraction/`: blind extractions under v0, one `<deal>.xlsx` per deal. Empty until Austin orders the v0 re-extraction. Preserve raw outputs; a revision is a separate, authorized pass.
- `ref/`: Alex's collection instructions, voice notes and hand-coded deals. For evaluation only. `seed.csv` (built by `_dev/tools/make_seed.py`) lists each deal's filing link and holds no answers.
- `_dev/`: tools and development guidance, not for extraction runs. Start with `_dev/STATUS.md`.

## Version 0
On 27 September 2026 Austin reset the project to version 0 and deleted everything from earlier instruction versions: workbooks, review packets, snapshots, decision records and compatibility code. Git history keeps them. Do not restore them, cite them as current, or add fallbacks for older schemas. Work only with v0.

## If you are asked to work on the pipeline itself
- Read `_dev/STATUS.md` first.
- For engineering, pick models by task: Astra for hard design and review (strong but expensive, sometimes erratic), Sol for well-specified implementation, Opus 5.5 or Fable 5.1 for design, implementation and integration. Opus 5.5 at medium effort is the default extraction model; Sol, Astra and Fable are used only when named.
- The cockpit is the shared extraction app on the VM (spec `_dev/COCKPIT_APP_SPEC.md`). Its source is not in this checkout. In it, Austin and Alex may each add deals, start extractions on their own subscription and publish instruction versions. The app records the browser account for each action; that attribution alone does not prove who clicked. An app version reaches the repository only through the VM's export script on Austin's request.
- Outside the app, an agent changes the instruction only with Austin's approval and runs extractions only on his command. Building or testing tools does not authorize a real model run. Change the instruction only where the change is general (objective, work process, honesty about uncertainty, a repaired contradiction, a deletion); never add a rule justified by one reviewed deal.
- Comparison runs must be isolated: one instruction and one filing per sandboxed session (`_dev/tools/sandbox/run_model.py`; usage in `_dev/tools/README.md`). Run the checker after the run, never where the extracting agent can see it. Revision mode is a separate, explicitly requested pass that may see the selected workbook and findings.
- Checking is mechanical and offline. Delete run folders and other scaffolding once their results are recorded.
- Commit and push finished work to GitLab (`origin`) at the end of each work session, on the current branch. Never force-push, rewrite pushed history, or commit secrets, caches or credentials.

This checkout is the `local-recovery-2026-09-27` branch. SSH to the VM has been unavailable since the 27 September certificate expiry.
