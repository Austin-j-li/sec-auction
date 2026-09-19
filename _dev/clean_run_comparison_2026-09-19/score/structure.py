#!/usr/bin/env python3
"""First-order structure of every ledger, schema-adaptive: rounds and opening dates, NDA counts, bids, formality, exits."""
import sys, glob, os, openpyxl, datetime, collections
root=sys.argv[1]
def d(v): return v.strftime('%m/%d') if isinstance(v,(datetime.date,datetime.datetime)) else str(v)[:10]
print("runset\tvariant\tdeal\trows\trounds(opened)\tNDA_count_sum\tbid_rows\tformal/informal/other\tcond H/L/N/other\treaffirmed\texit_rows\texit_count_sum\tinferred_exits\tadviser_rows\tdate_inversions")
for run in sorted(glob.glob(f"{root}/run*/*_*"),key=lambda r:(r.split('_',1)[1],r.split('/')[-1].split('_')[0],r)):
    if not os.path.isdir(run) or run.endswith('.xdg'): continue
    runset=run.split('/')[-2]; variant,deal=run.split('/')[-1].split('_',1)
    wb=openpyxl.load_workbook(glob.glob(f"{run}/extraction/*.xlsx")[0]); led=next(w for w in wb.worksheets if 'ledger' in w.title.lower())
    rows=list(led.iter_rows(values_only=True)); hi=next(i for i,r in enumerate(rows) if r and str(r[0]).strip()=='#')
    hdr=[str(h).strip() if h else '' for h in rows[hi]]; ix={h:i for i,h in enumerate(hdr) if h}
    body=[r for r in rows[hi+1:] if r and r[0] is not None and any(r[1:])]
    ev=ix.get('What happened',ix.get('Event')); sd=ix.get('Working date',ix.get('Sort date')); cl=ix.get('Conditions level',ix.get('Conditions'))
    g=lambda r,k: r[k] if k is not None else None
    ro=[(g(r,ix.get('Round')),d(g(r,sd))) for r in body if g(r,ev)=='Round opened']
    def num(v):
        try: return float(v)
        except: return 0
    nda=sum(num(g(r,ix.get('Count'))) for r in body if g(r,ev)=='NDA signed')
    bids=[r for r in body if g(r,ev) in('Bid','Bid reaffirmed')]
    fm=collections.Counter(g(r,ix.get('Formality')) for r in bids); c=collections.Counter(g(r,cl) for r in bids)
    EX=('Dropped by target','Withdrew','Did not submit','Not selected at signing','Closed')
    ex=[r for r in body if g(r,ev) in EX]
    inf=sum(1 for r in ex if (str(g(r,ix.get('Outcome basis')) or '').startswith('Inferred') or str(g(r,ix.get('Inferred')) or '').strip().upper()=='Y'))
    adv=sum(1 for r in body if str(g(r,ev)).startswith('Adviser'))
    ds=[g(r,sd) for r in body if isinstance(g(r,sd),(datetime.date,datetime.datetime))]; inv=sum(1 for a,b in zip(ds,ds[1:]) if b<a)
    print(f"{runset}\t{variant}\t{deal}\t{len(body)}\t{'; '.join(f'R{a}@{b}' for a,b in ro)}\t{nda:g}\t{len(bids)}\t{fm.get('Formal',0)}/{fm.get('Informal',0)}/{len(bids)-fm.get('Formal',0)-fm.get('Informal',0)}\t{c.get('Heavy',0)}/{c.get('Light',0)}/{c.get('None',0)}/{len(bids)-c.get('Heavy',0)-c.get('Light',0)-c.get('None',0)}\t{sum(1 for r in bids if g(r,ev)=='Bid reaffirmed')}\t{len(ex)}\t{sum(num(g(r,ix.get('Count'))) for r in ex):g}\t{inf}\t{adv}\t{inv}")
