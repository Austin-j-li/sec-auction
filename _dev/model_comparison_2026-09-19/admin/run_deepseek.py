#!/usr/bin/env python3
"""Isolated DeepSeek OpenCode 2 runner. No credentials are persisted or logged."""
import argparse, datetime, hashlib, json, os, pathlib, shutil, subprocess, time

PROJECT=pathlib.Path(__file__).resolve().parents[3]
BASE=pathlib.Path(__file__).resolve().parents[1]
HOME=pathlib.Path('/home/uctpiaj')
NODE=HOME/'.nvm/versions/node/v24.21.0'
PYTHON=HOME/'miniforge3'

def config():
    return {
      '$schema':'https://opencode.ai/config.json',
      'providers':{'deepseek':{
        'name':'DeepSeek','env':['DEEPSEEK_API_KEY'],
        'package':'@opencode/ai/providers/openai-compatible',
        'settings':{'baseURL':'https://api.deepseek.com/v1'},
        'models':{'deepseek-flash':{
          'modelID':'deepseek-flash','name':'DeepSeek V4.1 Flash',
          'capabilities':{'tools':True,'input':['text'],'output':['text']},
          'compatibility':{'reasoningField':'reasoning_content'},
          'limit':{'context':1000000,'output':384000},
          'variants':[{'id':'max','body':{'thinking':{'type':'enabled'},'reasoning_effort':'max'}}]
        }}
      }},
      'permissions':[{'action':'*','resource':'*','effect':'allow'}]+[
        {'action':a,'resource':'*','effect':'deny'} for a in ['webfetch','websearch','subagent','skill','question']
      ],
      'agents':{'build':{'permissions':[{'action':'question','resource':'*','effect':'deny'}]}}
    }

def main():
    p=argparse.ArgumentParser();p.add_argument('deal');p.add_argument('--probe',action='store_true');a=p.parse_args()
    run=BASE/('preflight' if a.probe else 'runs')/('deepseek_'+a.deal)
    if (run/'manifest.json').exists():raise SystemExit('Refusing to overwrite an existing run')
    work=run/'work'; state=run/'state'
    for q in [work/'raw_filing',work/'extraction',state/'config/opencode',state/'data',state/'cache',state/'state']:
        q.mkdir(parents=True,exist_ok=True)
    (state/'config/opencode/opencode.jsonc').write_text(json.dumps(config(),indent=2))
    if a.probe:
        (work/'toy.txt').write_text('sandbox-ok\n')
        prompt='Read toy.txt. Use Python and openpyxl to create extraction/smoke.xlsx with one sheet Smoke and A1 containing sandbox-ok. Verify it by reopening. Do not use the web, external files, skills or subagents. Finish with a short status.'
    else:
        shutil.copyfile(PROJECT/'SEC_Deal_Ledger_Extraction_Instruction.md',work/'SEC_Deal_Ledger_Extraction_Instruction.md')
        source=next((PROJECT/'raw_filing').glob(a.deal+'_*.htm'))
        shutil.copyfile(source,work/'raw_filing'/source.name)
        prompt=f'Read SEC_Deal_Ledger_Extraction_Instruction.md in this folder and follow it. Extract the deal whose filing is in raw_filing/ and save the finished workbook in extraction/ as {a.deal}.xlsx. Work only from this instruction and this filing.'
    (run/'prompt.txt').write_text(prompt+'\n')
    hashes={str(x.relative_to(work)):hashlib.sha256(x.read_bytes()).hexdigest() for x in work.rglob('*') if x.is_file()}
    env={'PATH':f'{NODE}/bin:{PYTHON}/bin:/usr/bin:/bin','HOME':str(HOME),'USER':'uctpiaj','LANG':'C.UTF-8',
         'DEEPSEEK_API_KEY':json.loads((HOME/'.local/share/opencode/auth.json').read_text())['deepseek']['key']}
    cmd=['bwrap','--unshare-all','--share-net','--die-with-parent','--new-session',
         '--ro-bind','/usr','/usr','--symlink','usr/bin','/bin','--symlink','usr/sbin','/sbin',
         '--symlink','usr/lib','/lib','--symlink','usr/lib64','/lib64']
    for s in ['/etc/ssl','/etc/ca-certificates','/etc/resolv.conf','/etc/hosts','/etc/nsswitch.conf','/etc/alternatives','/etc/passwd','/etc/group','/etc/localtime','/run/systemd/resolve']:
        if pathlib.Path(s).exists():cmd+=['--ro-bind',s,s]
    cmd+=['--proc','/proc','--dev','/dev','--tmpfs','/tmp','--tmpfs','/run/user','--tmpfs',str(HOME),
          '--ro-bind',str(NODE),str(NODE),'--ro-bind',str(PYTHON),str(PYTHON),
          '--bind',str(work),str(HOME/'work'),'--bind',str(state),str(HOME/'.xdg')]
    if not a.probe:
        for x in [work/'SEC_Deal_Ledger_Extraction_Instruction.md',* (work/'raw_filing').glob('*')]:
            cmd+=['--ro-bind',str(x),str(HOME/'work'/x.relative_to(work))]
    for k,v in {'XDG_DATA_HOME':str(HOME/'.xdg/data'),'XDG_CONFIG_HOME':str(HOME/'.xdg/config'),'XDG_STATE_HOME':str(HOME/'.xdg/state'),'XDG_CACHE_HOME':str(HOME/'.xdg/cache')}.items():cmd+=['--setenv',k,v]
    cmd+=['--chdir',str(HOME/'work'),'opencode','run','--standalone','--auto','--agent','build','--model','deepseek/deepseek-flash#max','--format','json',prompt]
    manifest={'model':'deepseek/deepseek-flash','effort':'max','client':'OpenCode 2.0.9','input_sha256':hashes,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'running','command':cmd}
    (run/'manifest.json').write_text(json.dumps(manifest,indent=2))
    start=time.monotonic()
    with (run/'events.jsonl').open('w') as out,(run/'stderr.log').open('w') as err:
        proc=subprocess.Popen(cmd,env=env,stdout=out,stderr=err,start_new_session=True)
        (run/'pid').write_text(str(proc.pid))
        try:code=proc.wait(timeout=180 if a.probe else 5400)
        except subprocess.TimeoutExpired:
            import signal
            os.killpg(proc.pid,signal.SIGTERM);code=124
    manifest.update(exit_code=code,elapsed_seconds=round(time.monotonic()-start,2),status='finished',ended_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
    (run/'manifest.json').write_text(json.dumps(manifest,indent=2))
    print(json.dumps({'run':str(run),'exit_code':code,'elapsed_seconds':manifest['elapsed_seconds']}))
if __name__=='__main__':main()
