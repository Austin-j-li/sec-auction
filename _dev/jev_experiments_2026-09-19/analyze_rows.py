import json, collections
R = json.load(open('results_rows.json'))
def rate(rs, f): 
    v=[f(r) for r in rs if f(r) is not None]; return f"{sum(v)}/{len(v)}"
orig=[r for r in R if r['variant']=='orig']
print("rows checked:",len(orig))
for T in (0.5,0.3,0.15):
    print(f"\nthreshold noul<{T}")
    for q in ('actor','event','price'):
        lo=lambda r:(r['answers'][q]['noul']<T) if q in r['answers'] else None
        line=f" {q:6} orig flagged {rate(orig,lo)}"
        for v in ('planted_price','planted_actor','planted_exitlabel'):
            pl=[r for r in R if r['variant']==v]
            if any(q in r['answers'] for r in pl): line+=f" | {v[8:]} {rate(pl,lo)}"
        print(line)
# choice checks
ex=[r for r in orig if 'exit_label' in r['answers']]
print("\nexit label agrees with ledger:",rate(ex,lambda r:r['answers']['exit_label']['choice']==r['event']))
pl=[r for r in R if r['variant']=='planted_exitlabel']
print("planted exit label: Jev disagrees with planted label:",rate(pl,lambda r:r['answers']['exit_label']['choice']!=r['event']))
print("exit reason agrees:",rate(ex,lambda r:r['answers']['exit_reason']['choice']==r['exit_reason']))
print(collections.Counter((r['exit_reason'],r['answers']['exit_reason']['choice']) for r in ex if r['answers']['exit_reason']['choice']!=r['exit_reason']).most_common(12))
print("inferred vs express:",collections.Counter((r['inferred'] or '-', r['answers']['exit_express']['noul']>0.5) for r in ex))
ac=[r for r in orig if 'all_cash' in r['answers']]
print("all cash agrees:",rate(ac,lambda r:r['answers']['all_cash']['choice']==r['all_cash']))
for r in ac:
    if r['answers']['all_cash']['choice']!=r['all_cash']: print('  ',r['deal'],r['model'],r['row'],r['who'],'ledger',r['all_cash'],'jev',r['answers']['all_cash']['choice'],round(r['answers']['all_cash']['confidence'],2))
