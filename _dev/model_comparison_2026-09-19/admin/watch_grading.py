#!/usr/bin/env python3
"""Advance each deal to blind grading only after reference and all runs finish."""
import datetime,json,pathlib,subprocess,sys,time
BASE=pathlib.Path(__file__).resolve().parents[1]
DEALS=['mac-gray','petsmart','providence-worcester']
def read(p):
 try:return json.loads(p.read_text())
 except (FileNotFoundError,json.JSONDecodeError):return {}
def main():
 deadline=time.monotonic()+7200;seen={}
 while time.monotonic()<deadline:
  states={}
  for deal in DEALS:
   root=BASE/'grading'/deal
   grade=read(root/'grade_status.json')
   if grade:states[deal]='grading_'+grade.get('state','unknown');continue
   ref=read(root/'reference_status.json')
   if ref.get('state')!='finished':states[deal]='awaiting_reference';continue
   if ref.get('exit_code')!=0:states[deal]='reference_failed';continue
   runs=[]
   for model in ['sol','opus','deepseek']:
    runs.append(read(BASE/'runs'/f'{model}_{deal}'/('manifest.json' if model=='deepseek' else 'status.json')))
   if any(x.get('state',x.get('status')) not in ['completed','finished'] for x in runs):states[deal]='awaiting_extractions';continue
   if any(x.get('exit_code')!=0 for x in runs):states[deal]='extraction_failed';continue
   if (root/'preparation_error.txt').exists():states[deal]='preparation_needs_review';continue
   p=subprocess.run([sys.executable,str(BASE/'admin/prepare_blind.py'),deal],capture_output=True,text=True)
   (root/'preparation_log.txt').write_text(p.stdout+p.stderr)
   if p.returncode:
    (root/'preparation_error.txt').write_text(p.stdout+p.stderr);states[deal]='preparation_needs_review';continue
   with (root/'grade_supervisor.log').open('w') as log:
    proc=subprocess.Popen([sys.executable,str(BASE/'admin/run_grader.py'),deal,'grade'],stdin=subprocess.DEVNULL,stdout=log,stderr=log,start_new_session=True)
   states[deal]=f'grading_launched_pid_{proc.pid}'
  if states!=seen:
   print(datetime.datetime.now(datetime.timezone.utc).isoformat(),json.dumps(states),flush=True);seen=states
  (BASE/'admin/pipeline_status.json').write_text(json.dumps({'updated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'deals':states},indent=2))
  if all(v=='grading_finished' for v in states.values()):return
  time.sleep(15)
if __name__=='__main__':main()
