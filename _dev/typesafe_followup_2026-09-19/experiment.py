"""Bounded public-filing judgment experiments. Credentials from env or hidden prompt only."""
import argparse, concurrent.futures, getpass, hashlib, json, os, re, statistics, time
from pathlib import Path
import httpx
from bs4 import BeautifulSoup
import unicodedata

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
MODEL = 'jev-1.13.0'

def norm(s):
    s = unicodedata.normalize('NFKC', s).translate(str.maketrans({'“':'"','”':'"','’':"'",'‘':"'"}))
    return re.sub(r'\s+', ' ', re.sub(r'[‐-―]', '-', s)).strip()

def source(deal):
    path = next((ROOT/'raw_filing').glob(deal+'_*.htm'))
    soup = BeautifulSoup(path.read_bytes(), 'lxml')
    paras = []
    for el in soup.find_all(['p','div','td']):
        if el.find(['p','div','td','table']): continue
        t = norm(el.get_text(' '))
        if len(t)>40 or re.fullmatch(r'(background of the (merger|offer)|reasons for the merger.*|recommendation of .*)',t,re.I): paras.append(t)
    return path, paras

def choice(instructions, criteria): return dict(type='choice',instructions=instructions,criteria=criteria)
def noul(instructions, yes, no): return dict(type='noul',instructions=instructions,criteria={'true':yes,'false':no})
def money(x): return '$'+format(x,'.2f')
def price_text(lo,hi): return money(lo) if lo==hi else money(lo)+' to '+money(hi)

def build():
    cases=[]
    sources={d:source(d) for d in ['providence-worcester','mac-gray','petsmart']}
    def packet(d,indices): return [{'paragraph_id':str(i),'text':sources[d][1][i]} for i in indices]
    # deal, focus paragraph, bidder, exact event, correct endpoints, plausible incorrect endpoints
    specs=[
      ('providence-worcester',353,'G&W','LOI submitted July 21, 2016',21.15,21.15,22.15,22.15),
      ('providence-worcester',353,'G&W','revised LOI submitted July 26, 2016',22.15,22.15,21.15,21.15),
      ('providence-worcester',353,'G&W','LOI submitted July 21, 2016, total consideration including CVR',21.15,21.15,20.02,20.02),
      ('providence-worcester',360,'Party D','revised LOI submitted August 1, 2016',24,24,23.81,23.81),
      ('providence-worcester',360,'Party E','revised LOI submitted August 1, 2016',23.81,23.81,21.26,21.26),
      ('providence-worcester',360,'Party E','original proposal confirmed August 2, 2016 after revised proposal withdrawn',21.26,21.26,23.81,23.81),
      ('providence-worcester',364,'G&W','revised LOI submitted August 12, 2016',25,25,24,24),
      ('mac-gray',217,'Party A','unsolicited proposal June 21, 2013',17,19,18,19),
      ('mac-gray',233,'Party B','preliminary indication July 24, 2013',17,18,15,17),
      ('mac-gray',233,'Party C','oral preliminary indication July 24, 2013',15,17,17,18),
      ('mac-gray',237,'Party C','written indication July 25, 2013',16,16.5,15,17),
      ('mac-gray',249,'CSC/Pamplona','revised indication September 9, 2013',19.5,19.5,18.5,18.5),
      ('mac-gray',249,'Party B','revised indication September 9, 2013',18.5,18.5,19.5,19.5),
      ('mac-gray',250,'Party A','revised indication September 10, 2013',18,19,16,17),
      ('mac-gray',250,'Party C','revised oral indication September 10, 2013',16,17,18,19),
      ('mac-gray',256,'CSC/Pamplona','proposal September 18, 2013',20.75,20.75,21.5,21.5),
      ('mac-gray',256,'Party B','proposal September 18, 2013, total package value attributed by bidder',21.5,21.5,19,19),
      ('mac-gray',256,'Party A','best and final confirmation September 18, 2013',18,19,16,17),
      ('mac-gray',260,'CSC/Pamplona','last and best offer confirmed September 21, 2013',21.25,21.25,20.75,20.75),
      ('petsmart',300,'Buyer Group','initial indication October 30, 2014',81,83,81,84),
      ('petsmart',300,'Bidder 2','initial indication October 30, 2014 before increase',78,78,81,84),
      ('petsmart',300,'Bidder 2','increased indication after discussions October 30 to November 2, 2014',81,84,78,78),
      ('petsmart',309,'Buyer Group','final bid letter December 10, 2014',80.7,80.7,80.35,80.35),
      ('petsmart',309,'Bidder 2','final bid letter December 10, 2014',80.35,80.35,80.7,80.7),
      ('petsmart',313,'Bidder 2','best and final offer evening December 12, 2014',81.5,81.5,82.5,82.5),
      ('petsmart',313,'Buyer Group','initial oral offer evening December 12, 2014 before later increase',82.5,82.5,83,83),
      ('petsmart',313,'Buyer Group','later best and final offer evening December 12, 2014',83,83,82.5,82.5),
    ]
    support_criteria={'supported':'The source explicitly supports the claimed price for this bidder at this exact event.',
      'contradicted':'The source gives a different price for the same bidder and event, or explicitly denies that submission. A different date, bidder or price component cannot support the claim.',
      'insufficient':'The supplied source does not establish the price at the specified event. Missing evidence is not contradiction; do not infer a carried-forward price.'}
    for j,(d,p,who,event,lo,hi,wl,wh) in enumerate(specs):
        evidence=packet(d,range(p-2,p+3))
        amounts=sorted(set(float(m.replace(',','')) for a in evidence for m in re.findall(r'\$\s*(\d[\d,]*(?:\.\d+)?)',a['text'])))
        opts={money(a):'Verbatim monetary amount found in source.' for a in amounts}|{'none':'No amount in the candidates is explicitly established for this endpoint at this event.'}
        for variant,l,h in [('correct',lo,hi),('wrong',wl,wh)]:
            pt=price_text(l,h)
            qs={
              'legacy':noul(f'Does the passage state that "{who}" offered, proposed or indicated a price of {pt} per share (the same number may be written without trailing zeros)?',f'The per-share figure {pt} appears in the passage as this party\'s price.','The passage gives a different figure for this party, or no figure.'),
              'scoped':choice(f'For {who}, evaluate the claim that the price at the event "{event}" was {pt} per share. Use only the source and bind the entire range, bidder, event and price basis together.',support_criteria),
              'low':choice(f'For {who} at the event "{event}", select the explicitly reported total per-share offer price, or lower endpoint if a range. Include attributed noncash package value. Exclude a component, equity total, rival price, or another offer by the same bidder. Select none when not established.',opts),
              'high':choice(f'For {who} at the event "{event}", select the explicitly reported total per-share offer price, or upper endpoint if a range. Include attributed noncash package value. Exclude a component, equity total, rival price, or another offer by the same bidder. Select none when not established.',opts)}
            cases.append(dict(id=f'price_{j:02}_{variant}',experiment='price',deal=d,paragraph=p,variant=variant,state={'passage':evidence},questions=qs,expected={'scoped':'supported' if variant=='correct' else 'contradicted','low':money(lo),'high':money(hi)},claim=[l,h]))
    for j,(d,p,who,event,l,h) in enumerate([
      ('providence-worcester',363,'Party B','returned draft August 4, 2016',24,24),
      ('mac-gray',239,'Party B','management presentation August 6, 2013',18.5,18.5),
      ('petsmart',306,'Bidder 2','comments submitted December 6, 2014',80.35,80.35),
      ('providence-worcester',362,'Party B','negotiation update August 4, 2016',24,24)]):
        cases.append(dict(id=f'missing_{j}',experiment='price_missing',deal=d,paragraph=p,variant='missing',state={'passage':packet(d,[p])},questions={'scoped':choice(f'For {who}, does the supplied passage explicitly state a price of {price_text(l,h)} per share at "{event}"? Do not infer a standing price.',support_criteria)},expected={'scoped':'insufficient'}))

    coverage=[
      ('mac-gray',267,'MacDonald, his wife and trust entered voting agreements on September 27, 2013.', 'September 27: MacDonald family voting agreements executed; effective on merger agreement entry.', 'September 21: CSC/Pamplona requested a MacDonald family voting agreement.'),
      ('mac-gray',245,'Bidders were instructed on August 27 to submit revised written proposals by September 9, 2013.', 'August 27 process letter sets September 9 deadline for revised written bids.', 'July 23 deadline for preliminary indications of interest.'),
      ('mac-gray',256,'Party B submitted a package valued at $21.50 per share on September 18, 2013, including $19 cash and $2.50 options.', 'Party B September 18: $21.50 package, cash $19 plus options valued by bidder at $2.50.', 'Party B September 9: all-cash offer of $18.50.'),
      ('providence-worcester',360,'Party E withdrew its $23.81 revised proposal on August 2, 2016 and confirmed its original $21.26 proposal.', 'August 2 Party E reverted to $21.26 after withdrawing the revised bid.', 'August 1 Party E raised its offer to $23.81 with Party F financing support.'),
      ('providence-worcester',353,'G&W increased its price to $22.15 on July 26, 2016, including $21.02 cash and $1.13 CVR.', 'July 26 G&W revised bid $22.15: $21.02 cash plus $1.13 CVR.', 'July 21 G&W bid $21.15: $20.02 cash plus $1.13 CVR.'),
      ('providence-worcester',363,'Party B counsel provided a revised merger agreement draft on August 4, 2016.', 'August 4: Party B returned a revised acquisition agreement through counsel.', 'August 5: the Company sent Party B revised merger agreement and disclosure letter.'),
      ('petsmart',305,'PetSmart set December 10, 2014 as the deadline for final bids.', 'Final bids now due the evening of December 10.', 'Final bids due December 5; transaction completion targeted December 15.'),
      ('petsmart',309,'Bidder 3 communicated valuation no higher than approximately $78 and did not submit a written offer on December 10.', 'December 10: Bidder 3 indicated a ceiling near $78; no written proposal followed.', 'December 10: Buyer Group $80.70 and Bidder 2 $80.35 cash final bids received.'),
      ('petsmart',313,'Buyer Group increased its December 12 oral $82.50 offer to a later best and final $83 offer.', 'Later December 12: Buyer Group final price $83 after earlier oral $82.50.', 'December 12: Buyer Group oral offer $82.50 and working to increase it.'),
      ('petsmart',306,'Buyer Group supplied financing commitment documents on December 6, 2014.', 'December 6: Buyer Group delivered financing commitments with its contract comments.', 'December 6: Bidder 2 supplied comments on draft transaction documents.')]
    for j,(d,p,event,paraphrase,distractor) in enumerate(coverage):
      for variant,rows in [('exact',[event]),('paraphrase',[paraphrase,distractor]),('distractor',[distractor]),('empty',[])]:
        criteria={f'row_{i}':r for i,r in enumerate(rows)}|{'none':'None of the supplied ledger rows records the target event with the same actors, date, action and material terms.'}
        cases.append(dict(id=f'coverage_{j:02}_{variant}',experiment='coverage',deal=d,paragraph=p,variant=variant,state={'source':packet(d,[p]),'target_event':event,'ledger_rows':{f'row_{i}':r for i,r in enumerate(rows)}},questions={
          'covered':noul('Is the target_event recorded in ledger_rows? Match the actual event, including its bidder, date, action and material terms, not just topic overlap.','At least one row records this same event.','No supplied row records this event.'),
          'match':choice('Select the ledger row that records target_event. A related event with a different date, bidder, amount or action does not count. Match by meaning, allowing paraphrase. Select none if absent.',criteria)},expected={'match':'row_0' if variant in ['exact','paraphrase'] else 'none','covered':variant in ['exact','paraphrase']}))

    finance=[
      ('mac-gray',[249],'CSC/Pamplona','September 9, 2013 revised indication','committed'),
      ('mac-gray',[249],'Party B','September 9, 2013 revised indication','missing'),
      ('mac-gray',[250],'Party A','September 10, 2013 revised indication','missing'),
      ('mac-gray',[250],'Party C','September 10, 2013 revised oral indication','missing'),
      ('mac-gray',[256],'CSC/Pamplona','September 18, 2013 proposal','committed'),
      ('mac-gray',[256],'Party B','September 18, 2013 proposal','silent'),
      ('mac-gray',[261,262],'CSC/Pamplona','September 21 to 23 final proposal','committed'),
      ('mac-gray',[217],'Party A','June 21, 2013 proposal','silent'),
      ('mac-gray',[232],'CSC/Pamplona','July 23, 2013 preliminary indication','silent'),
      ('providence-worcester',[352],'Party B','late July 2016 LOI','silent'),
      ('providence-worcester',[353],'G&W','July 21, 2016 LOI','silent'),
      ('providence-worcester',[355],'Party D','late July 2016 LOI','silent'),
      ('petsmart',[306],'Buyer Group','December 6, 2014 document submission','committed'),
      ('petsmart',[306],'Bidder 2','December 6, 2014 document submission','silent'),
      ('petsmart',[313],'Buyer Group','December 12, 2014 final bid','committed'),
      ('petsmart',[313],'Bidder 2','December 12, 2014 final bid','committed')]
    rules= (ROOT/'SEC_Deal_Ledger_Extraction_Instruction.md').read_text().split('### C14. Conditions')[1].split('### C15.')[0].strip()
    for j,(d,ps,who,event,gold) in enumerate(finance):
      cases.append(dict(id=f'finance_{j:02}',experiment='finance',deal=d,paragraphs=ps,variant=gold,state={'source':packet(d,ps),'conditions_rule':rules},questions={
       'financing':choice(f'For {who} at "{event}", what does the supplied source explicitly report about financing commitment? Judge only financing; do not import another bidder or date, or infer commitment from all-cash consideration.',{'committed':'Financing commitment provided, capital expressly committed, or financing not needed.','missing':'Explicitly no firm commitment, uncommitted financing, or financing contingency.','silent':'No explicit statement establishing either commitment or absence for this bidder at this event. Silence is not missing financing.'}),
       'conditions':choice(f'What Conditions label under conditions_rule applies to {who} at "{event}" based on the supplied source? Use Unclear if necessary context is missing.',{'None':'Affirmative readiness to sign and no remaining material conditions.','Light':'Only limited confirmatory diligence or final documentation; or committed financing without diligence condition.','Heavy':'Any Heavy trigger under conditions_rule.','Unclear':'Insufficient evidence/context.'})},expected={'financing':gold}))
    manifest={'model':MODEL,'labels':'Assistant-authored source reading; not human adjudicated','files':{d:{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for d,(p,_) in sources.items()},'cases':cases}
    (HERE/'cases.json').write_text(json.dumps(manifest,indent=2))
    print('Frozen',len(cases),'cases',flush=True)

def run(limit=None,repeat=False,phase='main'):
    cases=json.loads((HERE/('cases.json' if phase=='main' else 'ablation_cases.json')).read_text())['cases']
    if limit: cases=cases[:limit]
    if len(cases)>200: raise ValueError('Request budget exceeded')
    raw=HERE/('ablation_raw' if phase!='main' else ('repeat_raw' if repeat else 'raw'));raw.mkdir(exist_ok=True)
    key=os.environ.get('TYPESAFE_API_KEY') or getpass.getpass('TypeSafe API key (hidden): ')
    started=time.monotonic()
    def call(c):
        body={'model':MODEL,'state':c['state'],'questions':c['questions']}
        sha=hashlib.sha256(json.dumps(body,sort_keys=True).encode()).hexdigest()
        p=raw/(c['id']+'_'+sha[:12]+'.json')
        if p.exists(): return json.loads(p.read_text())
        attempt_logs=[]
        for attempt in range(3):
            t=time.monotonic()
            with httpx.Client(timeout=60,headers={'Authorization':'Bearer '+key}) as client:
                resp=client.post('https://api.typesafe.ai/v1/systemone',json=body)
            attempt_logs.append({'status':resp.status_code,'latency_s':time.monotonic()-t})
            if resp.status_code==200: break
            if resp.status_code not in (429,500,502,503,504): raise RuntimeError('TypeSafe HTTP '+str(resp.status_code))
            time.sleep(min(10,float(resp.headers.get('retry-after',2**attempt))))
        if resp.status_code!=200: raise RuntimeError('TypeSafe retries exhausted')
        record={'case_id':c['id'],'request_sha256':sha,'request':body,'response':resp.json(),'attempts':attempt_logs}
        p.write_text(json.dumps(record,indent=2));return record
    results=[]
    with concurrent.futures.ThreadPoolExecutor(4) as pool:
        for n,r in enumerate(pool.map(call,cases),1):
            results.append(r)
            if n%10==0: print('Completed',n,'/',len(cases),flush=True)
    key=None
    (HERE/('ablation_run.json' if phase!='main' else ('repeat_run.json' if repeat else 'run.json'))).write_text(json.dumps({'elapsed_s':time.monotonic()-started,'records':results},indent=2))
    print('Completed',len(results),'records in',round(time.monotonic()-started,2),'seconds',flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['build','run']);p.add_argument('--limit',type=int);p.add_argument('--repeat',action='store_true');p.add_argument('--phase',choices=['main','ablation'],default='main');a=p.parse_args()
    if a.action=='build':build()
    else:run(a.limit,a.repeat,a.phase)
