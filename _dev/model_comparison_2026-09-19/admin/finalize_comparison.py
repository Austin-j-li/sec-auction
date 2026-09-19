#!/usr/bin/env python3
"""Verify blind locks, freeze adjudication, then reveal identities and report."""
import csv
import datetime
import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parents[1]
DEALS = ['mac-gray', 'petsmart', 'providence-worcester']
NAMES = {'sol': 'GPT-5.6-Sol xhigh', 'opus': 'Claude Opus 5 high', 'deepseek': 'DeepSeek V4.1 Flash max'}

def read(p):
    return json.loads(p.read_text())

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

lock = read(B/'admin/blind_score_validation.json')
assert not lock['validation_problems'] and not lock['identities_revealed']
for deal in DEALS:
    root = B/'grading'/deal
    assert read(root/'grade_status.json')['exit_code'] == 0
    for key, rel in [('reference_sha256','reference/reference.json'), ('scores_sha256','grade/scores.json'), ('notes_sha256','grade/scoring_notes.md')]:
        assert sha(root/'work/output'/rel) == lock['locks'][deal][key], (deal,key)
aroot = B/'grading/providence-worcester'
astatus = read(aroot/'adjudicate_status.json')
assert astatus['state'] == 'finished' and astatus['exit_code'] == 0
adj = read(aroot/'work/output/adjudicate/adjudication.json')
freeze = {'frozen_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'primary_lock_sha256': sha(B/'admin/blind_score_validation.json'), 'primary_locks':lock['locks'], 'adjudication_sha256':sha(aroot/'work/output/adjudicate/adjudication.json'), 'adjudication_notes_sha256':sha(aroot/'work/output/adjudicate/adjudication.md'), 'identities_revealed':False}
assert not (B/'admin/unblinding.json').exists(), 'Already revealed; do not overwrite chronology'
(B/'admin/final_blind_lock.json').write_text(json.dumps(freeze,indent=2)+'\n')

# First identity-map read happens only after the final blind lock above.
maps = {d:read(B/'admin'/f'blind_map_{d}.json') for d in DEALS}
unblind = {'revealed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(), 'final_blind_lock_sha256':sha(B/'admin/final_blind_lock.json'), 'mappings':maps}
(B/'admin/unblinding.json').write_text(json.dumps(unblind,indent=2)+'\n')
results = {m:{'model':NAMES[m], 'deals':{}} for m in NAMES}
for d in DEALS:
    scores = read(B/'grading'/d/'work/output/grade/scores.json')
    for label, identity in maps[d].items():
        c = scores['candidates'][label]
        results[identity['model']]['deals'][d] = {'blind_label':label, 'score_100':c['score_100'], 'category_scores':c['category_scores'], 'critical_errors':c['critical_errors']}
for model,r in results.items():
    r['mean_score_100'] = sum(v['score_100'] for v in r['deals'].values())/3
    r['critical_root_causes'] = sum(len(v['critical_errors']) for v in r['deals'].values())
ranked = sorted(results,key=lambda m:results[m]['mean_score_100'],reverse=True)
(B/'comparison_scores.json').write_text(json.dumps({'basis':'Equal-weight mean of three frozen 100-point deal scores; AM01 leaves scores unchanged','models':results,'ranking':ranked},indent=2)+'\n')
with (B/'comparison_scores.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['model',*DEALS,'mean','critical_root_causes'])
    for m in ranked:
        r=results[m];w.writerow([r['model'],*[r['deals'][d]['score_100'] for d in DEALS],r['mean_score_100'],r['critical_root_causes']])

findings=read(B/'admin/anonymous_findings.json')
inventory=read(B/'admin/run_inventory.json')['runs']
metrics=read(B/'admin/workbook_metrics.json')
lines=[
    '# Blind model comparison — patched v1.8 lean', '',
    f"All nine requested extractions and blind grading are complete. **{NAMES[ranked[0]]} has the highest mean score in this three-deal experiment: {results[ranked[0]]['mean_score_100']:.2f}/100.** This is a small development-set result, not a general model ranking or acceptance of the workbooks as research-ready.", '',
    '| Model / effort | Mac-Gray | PetSmart | Providence–Worcester | Mean / 100 | Critical root causes |',
    '|---|---:|---:|---:|---:|---:|'
]
for m in ranked:
    r=results[m];lines.append(f"| {r['model']} | "+' | '.join(f"{r['deals'][d]['score_100']:.2f}" for d in DEALS)+f" | **{r['mean_score_100']:.2f}** | {r['critical_root_causes']} |")
lines += ['', 'Scores measure the frozen weighted tests. Critical errors are separate source-reviewed root causes, not extra score deductions. The same root cause may affect several research fields. In particular, 100/100 on Providence means passing its 33 weighted tests; its unscored notes and Questions still contain errors.', '',
    '## Concrete findings', '']
for d in DEALS:
    lines += [f'### {d}', '']
    for m in ranked:
        label=results[m]['deals'][d]['blind_label']
        lines += [f"- **{NAMES[m]} ({label}):** {findings[d][label]}"]
    lines += ['', f"Evidence: [full scoring notes](grading/{d}/work/output/grade/scoring_notes.md), [test-by-test scores](grading/{d}/work/output/grade/scores.json), [source reference](grading/{d}/work/output/reference/reference.md). Row numbers above are worksheet rows unless stated otherwise.", '']
lines += ['## What this says about the new instruction', '',
    'The project now has a compact 22-column ledger with four sheets, and explicit rules for re-entry and target-organized rounds. This experiment tested the patched instruction verbatim. The current instruction and full filing governed scoring; Alex’s hand rows and voice notes were assessed separately for compatibility. Earlier hand-coded conventions were not treated as automatic ground truth.', '',
    'The outputs generally preserve major prices and bid sequences. The remaining differences concentrate on reconstruction of competition: group counts, round boundaries, closing out bidders, and distinguishing reported dates from inferred bounds. The Mac-Gray extra-round error shows that the round patch does not eliminate all interpretation differences. PetSmart still exposes the difference between constituent firms and one joint bidding unit. Providence still exposes the need to close a bidder at an earlier named continuation set rather than defaulting to signing.', '',
    'This experiment does not identify the causal effect of the patch: there is no matched unpatched control or repeated sampling here. It supplies a clean baseline for the next unseen filings. No instruction edits were made.', '',
    '## Isolation and blind evaluation', '',
    '1. Each extractor had a fresh bubblewrap session, one identical instruction and one full filing, plus runtime tools and minimal provider authentication. No researcher answers, project history, previous outputs, personal memory or shared agent context were supplied. All nine used identical prompt bytes within each deal.',
    '2. The actual clients were Codex 0.155.1 (gpt-5.6-sol, xhigh), Claude Code 2.1.278 (claude-opus-5, high), and OpenCode 2.0.9 (deepseek/deepseek-flash, max). Claude and DeepSeek connectivity and tool execution were tested before the experiment. The API networking path remained available; isolation was not an OS-enforced API-only egress firewall. Command-log review found no outside-source retrieval.',
    '3. Fresh GPT-6-Astra high sessions built source-only references before seeing candidates: 45 Mac-Gray tests, 40 PetSmart tests, 33 Providence tests. A separate fresh session per deal graded all three candidates against that locked reference.',
    '4. Candidate identities were independently randomized for each deal. Workbook creator/application metadata and archive timestamps were neutralized; cell data, formulas and styles were preserved. Original workbooks were kept byte-for-byte. The graders could see neutral candidates, filings and source references, but not model maps or extraction logs. Writing style could still provide clues, so this is identity masking rather than a guarantee against inference.',
    '5. All 354 candidate/test credits were recomputed. Source references, scores and notes were hashed before model identities were revealed. A fresh identity-blind adjudicator resolved the one reference amendment before unblinding. The administrator did not revise scores after revealing identities.', '',
    'Each deal has 100 points: participation 30; rounds 25; formality and conditions 20; chronology 10; bids/prices 10; other material coverage 5. Credits are 0, 0.5 or 1 per fixed test. The three deals have equal weight in the model mean. No points are awarded for verbosity, formatting or question count.', '',
    'The lean-schema mechanical checker runs outside the extracting sandbox. Version 1.1 was applied uniformly to all nine candidates; it corrects overly strict parsing of explanatory labels and treats broad Question links as review leads. Its quote matches and counts are diagnostic leads, not semantic judgments. Original version-1 reports remain archived.', '',
    '## Reference correction', '',
    'AM01 corrects the Providence reference: Annex A-48 explicitly describes the Company–Parent confidentiality agreement as dated April 3, 2016. The original inventory overgeneralized that individual NDA dates were absent. A fresh blind adjudicator checked the parties, passage, relevant rows and T01 treatment. The amendment changes no candidate score and adds no new weighted test. “Dated” does not independently establish when signatures were delivered; the exact-date note should cite the annex.', '',
    'The original reference is preserved. See the [independent adjudication](grading/providence-worcester/work/output/adjudicate/adjudication.md), [original blind score lock](admin/blind_score_validation.json), [final blind lock](admin/final_blind_lock.json), and [timestamped identity reveal](admin/unblinding.json).', '',
    '## Execution and review burden', '',
    '| Model | Mean extraction time | Ledger rows, all 3 | Words per ledger row | Questions, all 3 |',
    '|---|---:|---:|---:|---:|'
]
for m in ranked:
    runs=[r for r in inventory if r['run'].startswith(m+'_')];ms=[x for x in metrics if x['model']==m]
    n=sum(x['ledger_rows'] for x in ms);words=sum(x['ledger_words'] for x in ms)
    lines.append(f"| {NAMES[m]} | {sum(x['elapsed_seconds'] for x in runs)/180:.2f} min | {n} | {words/n:.1f} | {sum(x['questions'] for x in ms)} |")
lines += ['',
    'Times are observed wall-clock extraction times under concurrent local runs, excluding preflight, reference building and grading. Counts and text volume are review-burden proxies; no human correction minutes were measured. Detailed per-candidate review and compatibility observations are in the scoring notes.', '',
    'DeepSeek’s client reported approximately $0.348 for its three extractions. Claude’s CLI reported approximately $9.045 at list-rate valuation for its three extractions; this is not the marginal subscription charge. Sol billing was unavailable. These are client estimates, not verified invoices, and should not be treated as a complete comparable cost study. Token accounting differs across clients.', '',
    '## Deliverables and limitations', '',
    '- [All nine original workbooks](nine_workbooks.zip), organized by model and deal, with SHA256 checksums.',
    '- [Machine-readable results](comparison_scores.json) and [CSV scores](comparison_scores.csv).',
    '- [Input/model manifest](MANIFEST.json), [execution inventory](admin/run_inventory.json), [integrity verification](admin/final_integrity.json), and [frozen rubric](admin/RUBRIC.md).',
    '- Per-deal source references, detailed row-level scoring notes, Questions and Alex-compatibility assessments are linked above.', '',
    'All nine sessions exited successfully and produced readable four-sheet workbooks. Input hashes match the frozen manifest; collected workbooks and archive entries match original run outputs. The experiment did not visually render the workbooks. No commits or pushes were made.', '',
    'There is one run per model per deal, only three development filings, one grader model family, and no human adjudication of all 118 tests. Reference construction itself can miss facts, as AM01 illustrates. The ranking therefore supports choosing the next validation run; it does not establish statistical superiority or readiness for unattended production. Fix the listed substantive errors before accepting these rows into the research dataset.', ''
]
(B/'COMPARISON.md').write_text('\n'.join(lines))
print(json.dumps({'ranking':ranked,'scores':{m:{'mean':results[m]['mean_score_100'],'deals':{d:results[m]['deals'][d]['score_100'] for d in DEALS},'critical_root_causes':results[m]['critical_root_causes']} for m in ranked}},indent=2))
