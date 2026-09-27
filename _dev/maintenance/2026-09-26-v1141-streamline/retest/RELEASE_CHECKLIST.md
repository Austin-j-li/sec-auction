# v1.14.1 release checklist

26 September 2026. Prepared under `PIPELINE_UPGRADE_SPEC.md` WP9 and V1141_SPEC §10 step 7. **Every step is a GATE: nothing here has been done, and each needs Austin's go.**

> **Status, 26 September, about 20:45 UTC.** Done by Austin, after the WP7 deploy (19:41 UTC): §1 and §3 steps 2–3. The draft holds the edited candidate, so its hash is not the `8bdb7c20…` below; `check_lean.RULES_BY_INSTRUCTION` maps both hashes to v1.14.1. Austin published it in the cockpit as v1.14.1 at 20:18 UTC (id `08caed447f7d`, SHA-256 `8a93df3cc6d989386958e9cb2d74ab34ebc0f07d281e8cc398605a388e066c98`: the reviewed `8bdb7c20…8a79` plus candidate issues 2 and 4–10 of `PIPELINE_UPGRADE_REPORT.md`) and made it the cockpit default, just before the retest ([results](../../../reviews/2026-09-26-v1141-retest/README.md)); the retest then passed. §2 is not recorded as done. Still GATEs: §3 step 4 (rebasing, gate 12) and §4 (the repository instruction is still v1.13.2).

Order: WP7 deploy → cockpit draft → retest → release decision. Do not publish v1.14.1 in the live cockpit before the WP7 deploy: the live checker 1.6 would check and edit v1.14.1 runs under the 24 September draft's rules.

## 1. Draft in the cockpit (GATE)

1. In the cockpit's Instructions tab, start a draft from v1.13.2.
2. Paste the full text of `SEC_Deal_Ledger_Extraction_Instruction_v1.14.1_candidate.md`, with LF line endings and one trailing newline, and save.
3. Check the stored hash equals `8bdb7c205512c9bcf55ffa7623fba0a8bb4aabaed23c99845fa88b4a80cc8a79`. The checker's rules map (`check_lean.RULES_BY_INSTRUCTION`) keys on this hash: any other bytes are checked as v1.14.1 only by the unknown-instruction default, and a later v1.14 re-check could not tell them apart.
4. Name it "v1.14.1" when it is published (step 3), not before.

## 2. Optional: give the trial runs provenance (GATE)

Publish the v1.14 candidate (`../2026-09-24-bid-terms-taxonomy/SEC_Deal_Ledger_Extraction_Instruction_v1.14_candidate.md`, hash `c2d47a47…ab27`) as a frozen "v1.14" first. Its hash already maps to the v1.14 rules, so any run imported under it is checked as v1.14.

## 3. Release decision (GATE, after the retest)

1. Austin reviews `RETEST_PLAN.md`'s acceptance output and the REVIEW items.
2. If accepted: publish the draft as "v1.14.1". Frozen versions never change.
3. Make v1.14.1 the cockpit default, as a separate step.
4. Rebasing working copies onto v1.14.1 runs, and moving the nine workbooks ("gate 12", `../2026-09-24-bid-terms-taxonomy/release/release-gate12.patch`), are separate decisions. Rebasing resets row marks and finding decisions (V114_SPEC, working-copy note).

## 4. Repository instruction (GATE, at release only)

`python3 _dev/tools/cockpit/export_repo.py instruction v1.14.1` previews the export; with `--write` it overwrites the frozen repository instruction (`SEC_Deal_Ledger_Extraction_Instruction.md`, v1.13.2). Run it with `--write` only at release, for a commit Austin requests. Never restore an old instruction into the checkout.
