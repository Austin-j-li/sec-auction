"""Independently verify frozen grading arithmetic; run from the workspace root."""
import json
import hashlib
from pathlib import Path
from collections import defaultdict

root = Path(__file__).resolve().parents[2]
ref_path = root / 'output/reference/reference.json'
ref = json.loads(ref_path.read_text())
scores = json.loads((root / 'output/grade/scores.json').read_text())
assert scores['reference_sha256'] == hashlib.sha256(ref_path.read_bytes()).hexdigest()
tests = {t['id']: t for t in ref['tests']}
assert len(tests) == len(ref['tests']) == 40
assert sum(t['weight'] for t in tests.values()) == 100
weights = defaultdict(float)
subweights = defaultdict(float)
for t in tests.values():
    weights[t['category']] += t['weight']
    if 'subdimension' in t:
        subweights[t['subdimension']] += t['weight']
assert dict(weights) == ref['validation']['category_totals']
assert dict(subweights) == {'formality': 10, 'conditions': 10}
assert set(scores['candidates']) == {'Candidate-A', 'Candidate-B', 'Candidate-C'}
required = {'tests', 'score_100', 'category_scores', 'critical_errors', 'other_errors',
            'omissions', 'compliance_observations', 'review_burden', 'alex_compatibility'}
for label, candidate in scores['candidates'].items():
    assert required <= set(candidate)
    assert len(candidate['tests']) == 40
    assert {t['id'] for t in candidate['tests']} == set(tests)
    categories = defaultdict(float)
    score = 0
    credits = defaultdict(int)
    for grade in candidate['tests']:
        assert set(grade) == {'id', 'credit', 'reason', 'rows', 'source_pages'}
        assert grade['credit'] in (0, 0.5, 1)
        assert grade['reason'] and grade['rows'] and grade['source_pages']
        source_test = tests[grade['id']]
        points = source_test['weight'] * grade['credit']
        categories[source_test['category']] += points
        score += points
        credits[grade['credit']] += 1
    assert score == candidate['score_100']
    assert dict(categories) == candidate['category_scores']
    print(f'{label}: {score:g}/100; credits {dict(credits)}; categories {dict(categories)}')
assert scores['ranking_with_reasons'] == sorted(scores['ranking_with_reasons'], key=lambda x: -x['score_100'])
assert scores['proposed_reference_amendments'] == []
print('Verified 120 test grades, 100-point denominator, stored totals, categories and reference hash.')
