#!/usr/bin/env python3
"""Read-only run inventory, execution metrics and tool-access leads for audit."""
import collections,datetime,hashlib,json,pathlib,re
BASE=pathlib.Path(__file__).resolve().parents[1]

def events(path):
 if not path.exists():return
 for line in path.read_text(errors='replace').splitlines():
  try:yield json.loads(line)
  except json.JSONDecodeError:continue

def main():
 rows=[];leads=[]
 for run in sorted((BASE/'runs').glob('*')):
  if not run.is_dir():continue
  family,deal=run.name.split('_',1)
  if family=='deepseek':
   meta=json.loads((run/'manifest.json').read_text());status=meta;work=run/'work';ins=work/'SEC_Deal_Ledger_Extraction_Instruction.md'
  else:
   meta=json.loads((run/'metadata.json').read_text());status=json.loads((run/'status.json').read_text());work=run;ins=run/'input/SEC_Deal_Ledger_Extraction_Instruction.md'
  r={'run':run.name,'model':meta.get('model'),'effort':meta.get('effort'),'state':status.get('state',status.get('status')),'exit_code':status.get('exit_code'),'elapsed_seconds':status.get('elapsed_seconds'),'instruction_sha256':hashlib.sha256(ins.read_bytes()).hexdigest(),'tool_calls':0,'input_tokens':0,'output_tokens':0,'reasoning_tokens':0,'reported_api_cost_usd':None}
  seen=set();cost=0;actual=set()
  for e in events(run/'events.jsonl'):
   calls=[]
   if family=='deepseek':
    part=e.get('part',{})
    if e.get('type')=='tool_use':calls.append((part.get('id'),part.get('tool'),part.get('state',{}).get('input',{})))
    if e.get('type')=='step_finish':
     t=part.get('tokens',{});r['input_tokens']+=t.get('input',0)+t.get('cache',{}).get('read',0);r['output_tokens']+=t.get('output',0);r['reasoning_tokens']+=t.get('reasoning',0);cost+=part.get('cost',0)
   elif family=='sol':
    it=e.get('item',{})
    if it.get('type')=='command_execution':calls.append((it.get('id'),'shell',it.get('command')))
    elif it.get('type') in ['web_search','mcp_tool_call']:calls.append((it.get('id'),it.get('type'),it))
    if e.get('type')=='turn.completed':
     t=e.get('usage',{});r['input_tokens']=t.get('input_tokens',0);r['output_tokens']=t.get('output_tokens',0);r['reasoning_tokens']=t.get('reasoning_output_tokens',0)
   else:
    if e.get('type')=='assistant':
     m=e.get('message',{});actual.add(m.get('model','unknown'))
     for c in m.get('content',[]):
      if c.get('type')=='tool_use':calls.append((c.get('id'),c.get('name'),c.get('input')))
    if e.get('type')=='result':
     r['reported_list_cost_usd']=e.get('total_cost_usd');r['duration_api_ms']=e.get('duration_api_ms')
     for model,u in e.get('modelUsage',{}).items():
      actual.add(model);r['input_tokens']+=u.get('inputTokens',0)+u.get('cacheReadInputTokens',0)+u.get('cacheCreationInputTokens',0);r['output_tokens']+=u.get('outputTokens',0);r['reasoning_tokens']+=u.get('thinkingTokens',0)
   for cid,tool,inp in calls:
    if cid in seen:continue
    seen.add(cid);r['tool_calls']+=1;s=json.dumps(inp,ensure_ascii=False)
    flags=[]
    if str(tool).lower() in ['webfetch','websearch','web_search','task','subagent','mcp_tool_call']:flags.append('external_or_delegation_tool')
    if re.search(r'(?i)\b(curl|wget)\s|requests\.(get|post)|urlopen\(|urllib\.request|https?://',s):flags.append('network_string_review')
    if re.search(r'(/Projects/|/\.codex/memories|/ref/|/\.git/|_dev/|\.credentials\.json|auth\.json)',s):flags.append('outside_source_path_review')
    if flags:leads.append({'run':run.name,'tool':tool,'call_id':cid,'flags':flags,'input':inp})
  if family=='deepseek':r['reported_api_cost_usd']=cost
  if actual:r['returned_models']=sorted(actual)
  files=list((work/'extraction').glob('*.xlsx'));r['workbooks']=[{'name':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]
  rows.append(r)
 out={'updated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'runs':rows,'tool_audit_leads':leads,'notes':['Network strings are review leads, not proof of network use.','DeepSeek cost is client-reported API cost; Opus list cost is not subscription marginal cost.','Sol usage may aggregate multiple model turns; interpretation follows CLI emitted usage.']}
 (BASE/'admin/run_inventory.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({'runs':[{k:r.get(k) for k in ['run','state','elapsed_seconds','exit_code']} for r in rows],'audit_leads':len(leads)},indent=2))
if __name__=='__main__':main()
