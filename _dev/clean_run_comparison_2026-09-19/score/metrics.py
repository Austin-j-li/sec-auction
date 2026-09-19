#!/usr/bin/env python3
"""Mechanical cost metrics for every run folder. usage: metrics.py <runs root> > metrics.tsv"""
import sys, os, re, glob, json, sqlite3, openpyxl
root=sys.argv[1]
def words(s): return len(re.findall(r'\S+',str(s))) if s is not None else 0
cols=['runset','variant','deal','workbook','sheets','ledger_rows','ledger_cols','ledger_words','words_per_row','other_sheet_words','source_copy_words','question_items','rows_flagged','pct_flagged','minutes','tool_calls','tokens_in','tokens_out','tokens_reasoning','cost_usd','exit']
print('\t'.join(cols))
for run in sorted(glob.glob(f"{root}/run*/*_*")):
    if not os.path.isdir(run) or run.endswith('.xdg'): continue
    runset=run.split('/')[-2]; variant,deal=run.split('/')[-1].split('_',1)
    rec=dict(runset=runset,variant=variant,deal=deal)
    xs=[f for f in glob.glob(f"{run}/extraction/*.xlsx") if not os.path.basename(f).startswith('.~')]
    rec['workbook']=os.path.basename(xs[0]) if xs else 'NONE'
    if xs:
        wb=openpyxl.load_workbook(xs[0]); rec['sheets']='; '.join(f"{w.title}{'(h)' if w.sheet_state!='visible' else ''}" for w in wb.worksheets)
        led=next((w for w in wb.worksheets if 'ledger' in w.title.lower()),wb.worksheets[0])
        rows=list(led.iter_rows(values_only=True)); hi=next((i for i,r in enumerate(rows) if r and str(r[0]).strip()=='#'),None)
        if hi is not None:
            hdr=rows[hi]; body=[r for r in rows[hi+1:] if r and r[0] is not None and any(r[1:])]
            rec['ledger_rows']=len(body); rec['ledger_cols']=sum(1 for h in hdr if h)
            rec['ledger_words']=sum(words(c) for r in body for c in r if isinstance(c,str)); rec['words_per_row']=round(rec['ledger_words']/max(1,len(body)),1)
            fi=[i for i,h in enumerate(hdr) if h and str(h).strip().lower() in ('review','flag')]
            if fi: fl=sum(1 for r in body if r[fi[0]] not in (None,'')); rec['rows_flagged']=fl; rec['pct_flagged']=round(100*fl/max(1,len(body)))
        ow=sw=0
        for w in wb.worksheets:
            if w is led or w.sheet_state!='visible': continue
            n=sum(words(c) for r in w.iter_rows(values_only=True) for c in r if isinstance(c,str))
            if w.title.lower().startswith('source'): sw+=n
            else: ow+=n
        rec['other_sheet_words']=ow; rec['source_copy_words']=sw
        q=next((w for w in wb.worksheets if w.title.lower().startswith('question')),None)
        if q: rec['question_items']=sum(1 for r in q.iter_rows(values_only=True) if r and r[0] and re.fullmatch(r'Q?\d+',str(r[0]).strip()))
    for k in ('start','end'):
        p=f"{run}.{k}"; rec[k]=int(open(p).read()) if os.path.exists(p) else None
    if rec.get('start') and rec.get('end'): rec['minutes']=round((rec['end']-rec['start'])/60,1)
    rec['exit']=open(f"{run}.exit").read().strip() if os.path.exists(f"{run}.exit") else 'running'
    db=f"{run}.xdg/data/opencode/opencode.db"
    if os.path.exists(db):
        try:
            con=sqlite3.connect(f"file:{db}?mode=ro",uri=True)
            r=con.execute("select cost,tokens_input,tokens_output,tokens_reasoning from session_v2 order by time_created desc limit 1").fetchone()
            if r: rec['cost_usd']=round(r[0] or 0,3); rec['tokens_in'],rec['tokens_out'],rec['tokens_reasoning']=r[1:]
        except Exception as e: rec['cost_usd']=f'err {e}'
    lg=f"{run}.log"
    if os.path.exists(lg): rec['tool_calls']=sum(1 for l in open(lg) if '"type":"tool_use"' in l)
    print('\t'.join(str(rec.get(c,'')) for c in cols))
