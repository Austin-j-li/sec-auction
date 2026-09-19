#!/usr/bin/env python3
"""Dump a ledger workbook to plain text, whatever its schema, for side-by-side scoring.
usage: dump_workbook.py in.xlsx out.txt   (the model-made 'Source text' copy of the filing and hidden sheets are skipped)"""
import sys, datetime, openpyxl
def fmt(v):
    if v is None: return ''
    if isinstance(v,(datetime.datetime,datetime.date)): return v.strftime('%Y-%m-%d')
    if isinstance(v,float) and v==int(v): return str(int(v))
    return str(v).replace('\n',' / ').strip()
def main(src,dst):
    wb=openpyxl.load_workbook(src)
    out=[]
    for ws in wb.worksheets:
        if ws.sheet_state!='visible' or ws.title.lower().startswith('source'):
            out.append(f"##### SHEET {ws.title!r} ({ws.sheet_state}, {ws.max_row} rows) -- skipped"); continue
        out.append(f"##### SHEET {ws.title!r} ({ws.max_row} rows x {ws.max_column} cols)")
        rows=[[fmt(c) for c in r] for r in ws.iter_rows(values_only=True)]
        hdr=None
        for i,r in enumerate(rows):
            if not any(r): continue
            filled=sum(1 for c in r if c)
            if hdr is None and filled>=5 and all(len(c)<40 for c in r if c):
                hdr=r; out.append('HEADER: '+' | '.join(c for c in r if c)); continue
            if hdr and filled>=3:
                out.append(f"--- row {i+1}")
                for h,c in zip(hdr,r):
                    if c: out.append(f"   {h or '?'}: {c}")
            else:
                out.append(' | '.join(c for c in r if c))
    open(dst,'w').write('\n'.join(out)+'\n')
if __name__=='__main__': main(*sys.argv[1:3])
