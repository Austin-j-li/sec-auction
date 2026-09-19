#!/usr/bin/env python3
"""Fresh source-only reference / opaque-candidate grading sessions."""
import argparse,datetime,hashlib,json,os,pathlib,shutil,subprocess,time
BASE=pathlib.Path(__file__).resolve().parents[1]
PROJECT=BASE.parents[1]
H=pathlib.Path('/home/uctpiaj')
RELEASE=H/'.codex/packages/standalone/releases/0.155.1-x86_64-unknown-linux-musl'

def main():
 p=argparse.ArgumentParser();p.add_argument('deal');p.add_argument('stage',choices=['reference','grade','adjudicate']);a=p.parse_args()
 root=BASE/'grading'/a.deal;work=root/'work';out=work/'output'/a.stage;out.mkdir(parents=True,exist_ok=True)
 state=root/('state_'+a.stage);state.mkdir(exist_ok=True)
 if (root/(a.stage+'_status.json')).exists():raise SystemExit('Stage already launched')
 if a.stage=='reference':
  (work/'raw_filing').mkdir(exist_ok=True)
  src=next((PROJECT/'raw_filing').glob(a.deal+'_*.htm'));shutil.copyfile(src,work/'raw_filing'/src.name)
  shutil.copyfile(PROJECT/'SEC_Deal_Ledger_Extraction_Instruction.md',work/'SEC_Deal_Ledger_Extraction_Instruction.md')
  shutil.copyfile(BASE/'admin/RUBRIC.md',work/'RUBRIC.md')
  prompt='You are an independent source-reference evaluator. Read RUBRIC.md and the entire supplied extraction instruction. Perform Stage 1 only using the single full filing in raw_filing/. No candidate workbooks exist yet. Write output/reference/reference.md and output/reference/reference.json with the source-backed inventory and fixed weighted tests exactly as specified. Check test weights sum to 100 and category totals match the rubric. Use only mounted files; no web, memories, skills, subagents, or other deals. You may use Python and BeautifulSoup. Complete the reference, not a plan.'
 elif a.stage=='grade':
  prompt='You are an independent identity-blind evaluator. Read RUBRIC.md, the current extraction instruction, and locked reference files in output/reference/. Perform Stage 2. The candidates are in candidates/ as neutral .xlsx and .txt files. Use the full filing in raw_filing/ to verify claims, read every candidate sheet and evaluate all locked tests. Mechanical checker outputs in checks/ are leads only. Optional Alex source transcripts in alex/ are only for the separate compatibility assessment. Write output/grade/scores.json and output/grade/scoring_notes.md exactly as specified. Do not edit reference or candidates. No model identities, logs or earlier comparisons are available; do not guess identities. No web, skills, subagents or external files. Complete all three candidates, and recompute scores from test weights with Python before finishing.'
 else:
  prompt=(work/'ADJUDICATION_PROMPT.txt').read_text()
 (root/(a.stage+'_prompt.txt')).write_text(prompt+'\n')
 shutil.copyfile(H/'.codex/models_cache.json',state/'models_cache.json')
 cmd=['bwrap','--unshare-all','--share-net','--die-with-parent','--new-session','--clearenv','--ro-bind','/usr','/usr','--symlink','usr/bin','/bin','--symlink','usr/sbin','/sbin','--symlink','usr/lib','/lib','--symlink','usr/lib64','/lib64']
 for s in ['/etc/ssl','/etc/ca-certificates','/etc/resolv.conf','/etc/hosts','/etc/nsswitch.conf','/etc/alternatives','/etc/passwd','/etc/group','/etc/localtime','/run/systemd/resolve']:
  if pathlib.Path(s).exists():cmd+=['--ro-bind',s,s]
 cmd+=['--proc','/proc','--dev','/dev','--tmpfs','/tmp','--tmpfs','/run/user','--tmpfs',str(H),'--ro-bind',str(H/'miniforge3'),str(H/'miniforge3'),'--bind',str(state),str(H/'.codex'),'--ro-bind',str(RELEASE),str(RELEASE),'--ro-bind',str(H/'.codex/auth.json'),str(H/'.codex/auth.json'),'--bind',str(work),str(H/'work')]
 for rel in ['SEC_Deal_Ledger_Extraction_Instruction.md','RUBRIC.md','raw_filing']+(['output/reference','candidates','checks','alex'] if a.stage!='reference' else [])+(['output/grade'] if a.stage=='adjudicate' else []):
  if (work/rel).exists():cmd+=['--ro-bind',str(work/rel),str(H/'work'/rel)]
 for k,v in {'HOME':str(H),'USER':'uctpiaj','LANG':'C.UTF-8','CODEX_HOME':str(H/'.codex'),'PATH':f'{H}/miniforge3/bin:/usr/bin:/bin'}.items():cmd+=['--setenv',k,v]
 cmd+=['--chdir',str(H/'work'),str(RELEASE/'bin/codex'),'exec','--ephemeral','--ignore-user-config','--ignore-rules','--skip-git-repo-check','--dangerously-bypass-approvals-and-sandbox','--json','--model','gpt-6-astra','-c','model_reasoning_effort="high"','-c','web_search="disabled"',prompt]
 start=time.monotonic();status={'model':'gpt-6-astra','effort':'high','stage':a.stage,'state':'running','started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 sp=root/(a.stage+'_status.json');sp.write_text(json.dumps(status,indent=2))
 with (root/(a.stage+'_events.jsonl')).open('w') as o,(root/(a.stage+'_stderr.log')).open('w') as e:
  proc=subprocess.Popen(cmd,stdout=o,stderr=e,start_new_session=True);status['pid']=proc.pid;sp.write_text(json.dumps(status,indent=2))
  try:rc=proc.wait(timeout=5400)
  except subprocess.TimeoutExpired:
   import signal
   os.killpg(proc.pid,signal.SIGTERM);rc=124
 status.update(state='finished',exit_code=rc,elapsed_seconds=round(time.monotonic()-start,2),outputs={str(f.relative_to(work)):hashlib.sha256(f.read_bytes()).hexdigest() for f in out.glob('*') if f.is_file()})
 sp.write_text(json.dumps(status,indent=2));print(json.dumps(status))
if __name__=='__main__':main()
