#!/usr/bin/env python3
"""Build one scoring folder per deal with neutral candidate labels. usage: prep_scoring.py <runs root>
Writes score/deals/<deal>/{filing_background,alex_hand_rows,alex_voice_notes}.txt, <label>.xlsx/.txt, and score/label_map.json (kept away from the scorers)."""
import sys, os, glob, json, random, shutil, subprocess
root=os.path.abspath(sys.argv[1]); here=os.path.dirname(os.path.abspath(__file__))
random.seed(20260919); out=f"{here}/deals"; os.makedirs(out,exist_ok=True); mp={}
shutil.copy(f"{root}/gold/alex_closing_summary.txt",f"{out}/alex_closing_summary.txt")
for deal in ('providence-worcester','mac-gray','petsmart'):
    d=f"{out}/{deal}"; os.makedirs(d,exist_ok=True)
    for k in ('filing_background','alex_hand_rows','alex_voice_notes'): shutil.copy(f"{root}/gold/{deal}_{k}.txt",f"{d}/{k}.txt")
    cands=[]
    for run in sorted(glob.glob(f"{root}/run*/*_{deal}")):
        xs=[f for f in glob.glob(f"{run}/extraction/*.xlsx") if not os.path.basename(f).startswith('.~')]
        if xs: cands.append((run.replace(root+'/',''),xs[0]))
    random.shuffle(cands); mp[deal]={}
    for i,(run,x) in enumerate(cands):
        lab='KLMNPQRSTUVW'[i]; mp[deal][lab]=run
        shutil.copy(x,f"{d}/{lab}.xlsx"); subprocess.run([sys.executable,f"{here}/dump_workbook.py",x,f"{d}/{lab}.txt"],check=True)
    print(deal,len(cands),'candidates')
json.dump(mp,open(f"{here}/label_map.json",'w'),indent=1)
