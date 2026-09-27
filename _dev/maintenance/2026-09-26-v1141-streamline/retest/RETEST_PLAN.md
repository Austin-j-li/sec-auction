# v1.14.1 retest plan

26 September 2026. Prepared under `PIPELINE_UPGRADE_SPEC.md` WP9 and V1141_SPEC §10 steps 5–6. **Nothing here has been run. GATE: Austin orders the runs.**

> **Status, 26 September, about 20:45 UTC: done.** After the deploy, Austin published it in the cockpit as v1.14.1 at 20:18 UTC (id `08caed447f7d`, SHA-256 `8a93df3cc6d989386958e9cb2d74ab34ebc0f07d281e8cc398605a388e066c98`: the reviewed `8bdb7c20…8a79` plus candidate issues 2 and 4–10 of `PIPELINE_UPGRADE_REPORT.md`) and made it the cockpit default. At 20:19 UTC he started the five runs as cockpit extract jobs (Opus 5.5 medium, v1.14.1), not with the sweep commands below, so the runs pinned `8a93df3c…6c98`, not the `8bdb7c20…` hash this plan names. All five completed and were checked by checker 1.8 under the v1.14.1 rules; every §10 step-6 behaviour holds. Results: [retest README](../../../reviews/2026-09-26-v1141-retest/README.md). Datalink gave four rounds, and Austin decided that Datalink follows the v1.14.1 text (four rounds; F9 superseded). "Afterwards": the 3.3(a) table is recomputed and the questionnaire rebuilt (`../../2026-09-24-bid-terms-taxonomy/evidence/a2/README.md`). The run folders under `_dev/runs/` were not used.

## What runs

Five isolated runs, all launched at once, with no revision pass:

| Deal | Filing | Why |
|---|---|---|
| mac-gray | `mac-gray_2013-12-04_DEFM14A.htm` | carried the disputes (H3, H4, R1) |
| providence-worcester | `providence-worcester_2016-09-20_DEFM14A.htm` | carried the disputes (H2, R4, R6) |
| stec | `stec_2013-08-08_DEFM14A.htm` | carried the disputes (H1, R5, D2) |
| synacor | `synacor_2021-03-03_SCTO-T.htm` | the reopening rule, E6(d) |
| datalink | `datalink_2016-11-29_DEFM14A.htm` | the F9 ruling |

Each run is Opus 5.5 (`claude-opus-5-5`) at medium effort, one instruction and one filing per sandbox. The instruction is the v1.14.1 candidate, SHA-256 `8bdb7c205512c9bcf55ffa7623fba0a8bb4aabaed23c99845fa88b4a80cc8a79`.

## Where to run it

From the main checkout **after the WP7 deploy**, so that the sweep checks each workbook with checker 1.8 under the v1.14.1 rules. If Austin orders the retest before the deploy, run the same commands from `~/work/Projects/sec-extraction-v114` instead (its `raw_filing/` is byte-identical to main's; checked 26 September). Do not run them from main before the deploy: main's checker 1.6 would check the workbooks under the 24 September draft's rules.

## Commands

The runner falls back to the repository's v1.13.2 instruction when `--instruction` is missing (`run_model.py prepare`). Every command below passes the candidate explicitly, and step 3 stops the retest if any run pinned another hash.

```bash
cd ~/work/Projects/sec-extraction
```

1. Plan the sweep, pinning the candidate by hash. The seed only orders the launches.

```bash
python3 _dev/tools/effort_sweep.py plan --packet _dev/reviews/2026-MM-DD-v1141-retest --deals mac-gray,providence-worcester,stec,synacor,datalink --arms opus:claude-opus-5-5:medium --replicates 1 --seed 20260926 --instruction _dev/maintenance/2026-09-26-v1141-streamline/SEC_Deal_Ledger_Extraction_Instruction_v1.14.1_candidate.md
```

2. Check the plan pins the right instruction before anything is launched.

```bash
python3 -c "import json,sys; p=json.load(open('_dev/reviews/2026-MM-DD-v1141-retest/plan.json')); h=p['instruction']['sha256']; print(h); sys.exit(h!='8bdb7c205512c9bcf55ffa7623fba0a8bb4aabaed23c99845fa88b4a80cc8a79')"
```

3. Run all five at once. The sweep prepares each run with `--instruction`, launches it, and after it ends checks the workbook outside the sandbox and copies the receipts into the packet.

```bash
python3 _dev/tools/effort_sweep.py run --packet _dev/reviews/2026-MM-DD-v1141-retest --concurrency 5
```

4. Confirm every run's metadata names the candidate.

```bash
grep -h '"instruction_sha256"' _dev/runs/2026-MM-DD-v1141-retest/*/metadata.json | sort | uniq -c
```

Equivalent single-run commands, if the sweep is not used (repeat for each deal and filing above, then launch all five before waiting on any):

```bash
python3 _dev/tools/sandbox/run_model.py prepare --provider opus --model claude-opus-5-5 --effort medium --instruction _dev/maintenance/2026-09-26-v1141-streamline/SEC_Deal_Ledger_Extraction_Instruction_v1.14.1_candidate.md --run-dir _dev/runs/2026-MM-DD-v1141-retest/mac-gray --deal mac-gray --filing mac-gray_2013-12-04_DEFM14A.htm
```

```bash
python3 _dev/tools/sandbox/run_model.py launch --provider opus --run-dir _dev/runs/2026-MM-DD-v1141-retest/mac-gray
```

Replace `2026-MM-DD` with the run date. The runs use Austin's Claude subscription, as the trial did.

## Acceptance

Run the offline check after all five have finished, outside their sandboxes:

```bash
python3 _dev/maintenance/2026-09-26-v1141-streamline/retest/retest_acceptance.py --tools _dev/tools --workbook mac-gray=_dev/reviews/2026-MM-DD-v1141-retest/runs/<mac-gray cell>/mac-gray.xlsx --workbook providence-worcester=<path> --workbook stec=<path> --workbook synacor=<path> --workbook datalink=<path> --output _dev/reviews/2026-MM-DD-v1141-retest/acceptance.json
```

`--tools` must hold checker 1.8 (`~/work/Projects/sec-extraction-v114/_dev/tools` before the deploy). The script tests V1141_SPEC §10 step 6 and marks what it cannot judge as REVIEW:

- **Mac-Gray:** 16 unnamed signers Did not submit, dated 23 July, Count 16. The October liability revisions are Bid rows with blank prices (REVIEW: confirm the rows it lists). Party A's 18 September bid is Heavy with an "H1:" Note and Formal.
- **P&W:** a Did not submit row with Count 16. No named party entered beside the 25 (REVIEW: the NDA signed rows). No Party E bid coded H2. G&W's 12 August bid has Regulatory Concern. Party C's 12 July bid is not Due diligence Not begun.
- **sTec:** Company H Dropped by target by 16 May, reason Would not improve earlier offer. WDC's June standstill warning is a Bid with an "H3:" Note and no price. Two rounds.
- **Synacor and Datalink:** round maps against the recorded ones (Synacor three processes and six rounds; Datalink five rounds under F9). A difference is REVIEW, to be explained by trigger (d) and shown to Austin. The questionnaire work found that the v1.14.1 text gives Datalink four rounds, because the "count once" sentence is gone (see `PIPELINE_UPGRADE_REPORT.md`); expect REVIEW there.
- **All five:** no Note-length error; at most five Questions besides the process Question; for the three trial deals, no more ledger rows than the trial's Opus 5.5 medium workbooks (Mac-Gray 64, P&W 63, sTec 66).

Do not grade with the trial's rubric. `administration/GRADING_KICKOFF_prior_to_pro_dispatch.md` rewards "dates and bounds", `grading/README.md` asks for non-submitters "with a bound", and `grading/mechanical_check.py` has no Note cap; all three would score v1.14.1 behaviour as wrong.

## Afterwards

- Record results in `_dev/reviews/2026-MM-DD-v1141-retest/README.md`. Delete the run folders under `_dev/runs/` once the sweep has copied their receipts.
- Recompute the Formality-reading agreement table (questionnaire 3.3(a); WP3 item 8) from the retest workbooks with `derive_analysis.py --rules v1.14.1`, then rebuild the questionnaire.
- Austin decides the release (`RELEASE_CHECKLIST.md`).
