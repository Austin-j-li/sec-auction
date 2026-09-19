"""Adaptive diagnostic phase. Keep first-run labels; do not relabel failures."""
import copy,json
from experiment import HERE,noul
main=json.loads((HERE/'cases.json').read_text())
cases=[]
for c in main['cases']:
    cc=copy.deepcopy(c)
    if c['experiment']=='price':
        cc['questions']={'scoped_noul':noul(c['questions']['scoped']['instructions']+' Is that exact claim supported?',
          'The source explicitly supports the entire price/range for this bidder at this event and price basis.',
          'The price is different, belongs to another event/bidder/component, or evidence is missing.')}
    elif c['experiment']=='finance':
        cc['questions']={'financing':c['questions']['financing']}
        del cc['state']['conditions_rule']
    else:continue
    cc['id']='ablation_'+c['id'];cases.append(cc)
main['cases']=cases
main['adaptive_note']='Designed after first run. Price: isolate event-specific question wording while retaining Noul. Financing: same question, remove unrelated overall-conditions rule and companion question. Not a held-out test.'
(HERE/'ablation_cases.json').write_text(json.dumps(main,indent=2))
print('Frozen',len(cases),'adaptive diagnostic cases')
