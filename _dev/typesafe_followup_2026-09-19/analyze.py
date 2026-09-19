"""Analyze saved responses only. Makes no API requests."""
import collections, json, statistics
from pathlib import Path
P=Path(__file__).resolve().parent
cases=json.loads((P/'cases.json').read_text())['cases']
run=json.loads((P/'run.json').read_text())
records={r['case_id']:r for r in run['records']}
failures=[];summary={}

def tally(rows, question, predict, expected):
    correct=0;high_total=0;high_correct=0
    for c in rows:
        a=records[c['id']]['response']['answers'][question]
        pred=predict(a);gold=expected(c);ok=pred==gold
        correct+=ok
        if a.get('confidence',-1)>=0.9: high_total+=1;high_correct+=ok
        if not ok: failures.append({'case_id':c['id'],'question':question,'predicted':pred,'expected':gold,'answer':a})
    return {'correct':correct,'total':len(rows),'confidence_ge_09_correct':high_correct,'confidence_ge_09_total':high_total}

for variant in ['correct','wrong']:
    rows=[c for c in cases if c['experiment']=='price' and c['variant']==variant]
    summary['price_'+variant]={
      'legacy':tally(rows,'legacy',lambda a:a['noul']>=0.5,lambda c:c['variant']=='correct'),
      'scoped':tally(rows,'scoped',lambda a:a['choice'],lambda c:c['expected']['scoped'])}
    decisions=[]
    for c in rows:
        a=records[c['id']]['response']['answers']
        correct=all(a[k]['choice']==c['expected'][k] for k in ['low','high'])
        decisions.append(correct)
        if not correct:failures.append({'case_id':c['id'],'question':'selection','predicted':[a[k]['choice'] for k in ['low','high']],'expected':[c['expected'][k] for k in ['low','high']],'answer':{k:a[k] for k in ['low','high']}})
    summary['price_'+variant]['selection']={'correct':sum(decisions),'total':len(decisions)}
rows=[c for c in cases if c['experiment']=='price_missing']
summary['missing']=tally(rows,'scoped',lambda a:a['choice'],lambda c:c['expected']['scoped'])
rows=[c for c in cases if c['experiment']=='coverage']
summary['coverage']={}
for variant in ['exact','paraphrase','distractor','empty']:
    rr=[c for c in rows if c['variant']==variant]
    summary['coverage'][variant]={
      'binary':tally(rr,'covered',lambda a:a['noul']>=0.5,lambda c:c['expected']['covered']),
      'selection':tally(rr,'match',lambda a:a['choice'],lambda c:c['expected']['match'])}
rows=[c for c in cases if c['experiment']=='finance']
summary['financing']=tally(rows,'financing',lambda a:a['choice'],lambda c:c['expected']['financing'])
summary['financing_breakdown']={v:tally([c for c in rows if c['variant']==v],'financing',lambda a:a['choice'],lambda c:c['expected']['financing']) for v in ['committed','missing','silent']}
summary['conditions_unscored']=[{'case_id':c['id'],'financing_expected':c['expected']['financing'],'answer':records[c['id']]['response']['answers']['conditions']} for c in rows]
latencies=[sum(a['latency_s'] for a in r['attempts']) for r in records.values()]
tokens=sum(r['response']['usage']['input_tokens'] for r in records.values())
summary['service']={'logical_calls':len(records),'http_attempts':sum(len(r['attempts']) for r in records.values()),'input_tokens':tokens,'estimated_cost_usd':tokens/1e6*0.042,'median_latency_s':statistics.median(latencies),'p95_latency_s':sorted(latencies)[int(.95*(len(latencies)-1))],'wall_seconds':run['elapsed_s'],'models':dict(collections.Counter(r['response']['model'] for r in records.values()))}
summary['failures']=list({(f['case_id'],f['question']):f for f in failures}.values())
summary['amount_only_baseline']={}
for v in ['correct','wrong']:
    import re
    rr=[c for c in cases if c['experiment']=='price' and c['variant']==v]
    passed=0
    for c in rr:
        amounts={float(x.replace(',','')) for z in c['state']['passage'] for x in re.findall(r'\$\s*(\d[\d,]*(?:\.\d+)?)',z['text'])}
        passed+=all(a in amounts for a in c['claim'])
    summary['amount_only_baseline'][v]={'accepted':passed,'total':len(rr)}
if (P/'ablation_run.json').exists():
    arun=json.loads((P/'ablation_run.json').read_text())
    acases=json.loads((P/'ablation_cases.json').read_text())['cases']
    aa={r['case_id']:r['response']['answers'] for r in arun['records']}
    summary['ablation']={}
    for v in ['correct','wrong']:
        rr=[c for c in acases if c['experiment']=='price' and c['variant']==v]
        summary['ablation']['scoped_noul_'+v]={'correct':sum((aa[c['id']]['scoped_noul']['noul']>=.5)==(v=='correct') for c in rr),'total':len(rr)}
    rr=[c for c in acases if c['experiment']=='finance']
    summary['ablation']['source_only_financing']={'correct':sum(aa[c['id']]['financing']['choice']==c['expected']['financing'] for c in rr),'total':len(rr),'details':[{'case_id':c['id'],'expected':c['expected']['financing'],'answer':aa[c['id']]['financing']} for c in rr]}
    all_records=run['records']+arun['records']
    ts=sum(r['response']['usage']['input_tokens'] for r in all_records)
    ls=[sum(a['latency_s'] for a in r['attempts']) for r in all_records]
    summary['combined_service']={'logical_calls':len(all_records),'http_attempts':sum(len(r['attempts']) for r in all_records),'input_tokens':ts,'estimated_cost_usd':ts/1e6*.042,'median_latency_s':statistics.median(ls),'p95_latency_s':sorted(ls)[int(.95*(len(ls)-1))],'api_run_wall_seconds':run['elapsed_s']+arun['elapsed_s']}
(P/'summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps({k:v for k,v in summary.items() if k!='conditions_unscored'},indent=2))
