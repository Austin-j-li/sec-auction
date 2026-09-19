#!/usr/bin/env python3
"""Validate and freeze anonymous scores before identity reveal."""
import collections,datetime,hashlib,json,pathlib,sys
BASE=pathlib.Path(__file__).resolve().parents[1]
def main():
 out={};problems=[];locks={}
 for deal in ['mac-gray','petsmart','providence-worcester']:
  root=BASE/'grading'/deal;work=root/'work'
  sp=work/'output/grade/scores.json';rp=work/'output/reference/reference.json'
  if not sp.exists():problems.append(f'{deal}: scores absent');continue
  status=json.loads((root/'grade_status.json').read_text())
  if status.get('state')!='finished':problems.append(f'{deal}: grader still active');continue
  ref=json.loads(rp.read_text());scores=json.loads(sp.read_text());tests={t['id']:t for t in ref['tests']}
  refhash=hashlib.sha256(rp.read_bytes()).hexdigest()
  if refhash!=json.loads((root/'reference_lock.json').read_text())['sha256']:problems.append(f'{deal}: reference hash changed')
  out[deal]={}
  for label,c in scores['candidates'].items():
   rows=c['tests'];ids=[r['id'] for r in rows]
   if len(ids)!=len(set(ids)) or set(ids)!=set(tests):problems.append(f'{deal}/{label}: wrong test ID set');continue
   cats=collections.defaultdict(float)
   for r in rows:
    credit=r['credit']
    if credit not in [0,0.5,1]:problems.append(f'{deal}/{label}/{r["id"]}: invalid credit {credit}');continue
    t=tests[r['id']];cats[t['category']]+=t['weight']*credit
   total=sum(cats.values())
   out[deal][label]={'recomputed_score_100':round(total,6),'reported_score_100':c.get('score_100'),'category_scores':dict(cats),'critical_errors':c.get('critical_errors',[]),'omissions':c.get('omissions',[])}
   if abs(float(c.get('score_100',total))-total)>0.00001:problems.append(f'{deal}/{label}: reported total differs from recomputation')
  locks[deal]={'reference_sha256':refhash,'scores_sha256':hashlib.sha256(sp.read_bytes()).hexdigest(),'notes_sha256':hashlib.sha256((work/'output/grade/scoring_notes.md').read_bytes()).hexdigest()}
 report={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scores':out,'validation_problems':problems,'locks':locks,'identities_revealed':False}
 (BASE/'admin/blind_score_validation.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({'scores':out,'validation_problems':problems},indent=2))
 return 1 if problems else 0
if __name__=='__main__':sys.exit(main())
