#!/bin/bash
# usage: astra_confirm.sh <slice> <effort> <prior review file> <out name>
set -u
slice=$1; effort=$2; prior=$3; out=/tmp/recov/reviews/$4
prompt="You are the confirming reviewer for recovery slice ${slice}. Read /tmp/recov/TEAM_BRIEF.md (especially 'Proportionality'), the prior review ${prior}, and the 'Fixes' section(s) of /tmp/recov/reports/${slice}.md. For each numbered finding in the prior review, check the repository and evidence and say FIXED or NOT FIXED with a one-line pointer. Then list only NEW blocker or major defects introduced by the fixes, if any. Do not re-audit the rest of the slice, do not run pytest, and do not raise minor or stylistic points. End with a verdict line: ACCEPT or ACCEPT-WITH-FIXES (only if something is NOT FIXED or a new blocker/major exists)."
codex exec -m gpt-6-astra -c model_reasoning_effort=${effort} -s read-only -C /Users/austinli/Projects/sec-auction \
  -o "$out" "$prompt" > /tmp/recov/runs/${slice}.confirm.log 2>&1
echo "exit=$? confirm=${slice}"; tail -n 3 "$out"
