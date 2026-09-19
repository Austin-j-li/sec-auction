#!/usr/bin/env python3
"""Check every quotation (25+ characters inside quotation marks) in each ledger against the filing's full text."""
import sys, re, glob, os, openpyxl, html
from bs4 import BeautifulSoup
root=sys.argv[1]
def norm(s):
    s=html.unescape(s).replace('\xa0',' ')
    s=re.sub(r'[“”„‟"]','"',s); s=re.sub(r"[‘’‚‛']","'",s); s=re.sub(r'[‐‑‒–—―]','-',s)
    return re.sub(r'\s+',' ',s).strip().lower()
cache={}
def filing(deal):
    if deal not in cache:
        f=glob.glob(f"{root}/run1/full_{deal}/raw_filing/*.htm")[0]
        cache[deal]=norm(BeautifulSoup(open(f,encoding='utf-8',errors='replace').read(),'lxml').get_text(' '))
    return cache[deal]
print("runset\tvariant\tdeal\tquotes\tfound\tnot_found\tpct_found\trows_with_quote\tledger_rows")
for run in sorted(glob.glob(f"{root}/run*/*_*")):
    if not os.path.isdir(run) or run.endswith('.xdg'): continue
    runset=run.split('/')[-2]; variant,deal=run.split('/')[-1].split('_',1)
    x=glob.glob(f"{run}/extraction/*.xlsx")[0]; wb=openpyxl.load_workbook(x)
    led=next(w for w in wb.worksheets if 'ledger' in w.title.lower()); rows=list(led.iter_rows(values_only=True))
    hi=next(i for i,r in enumerate(rows) if r and str(r[0]).strip()=='#'); body=[r for r in rows[hi+1:] if r and r[0] is not None and any(r[1:])]
    T=filing(deal); q=f=0; rq=0; miss=[]
    hdr=rows[hi]; qcol=next((i for i,h in enumerate(hdr) if h and str(h).strip().lower().startswith('quote')),None)
    class M:  # whole-cell quotation (v1.8 'Quote and page' column): drop the page reference and outer quote marks
        def __init__(s,t): s.t=t
        def group(s,i): return s.t
    for r in body:
        had=False
        for ci,c in enumerate(r):
            if not isinstance(c,str): continue
            if ci==qcol:
                t=re.sub(r'\(\s*(?:pp?\.?\s*)?[\d\s,\-–]+\)','',c).strip(' “”"\'.;')
                ms=[M(t)] if len(t)>=25 else []
            else: ms=list(re.finditer(r'[“"]([^“”"]{25,}?)[”"]',c))
            for m in ms:
                had=True; q+=1; s=norm(m.group(1)).strip(' .,;"')
                parts=[p.strip(' .,;') for p in re.split(r'\s*(?:\.\.\.|…|\[[^\]]*\])\s*',s) if len(p.strip())>=15]
                ok=all(p in T for p in parts) if parts else s in T
                f+=ok
                if not ok: miss.append(s[:90])
        rq+=had
    print(f"{runset}\t{variant}\t{deal}\t{q}\t{f}\t{q-f}\t{round(100*f/max(1,q))}\t{rq}\t{len(body)}")
    for m in miss[:3]: print("    miss:",m,file=sys.stderr)
