#!/bin/bash
# usage: sol.sh <slice> <effort> [extra prompt file]
set -u
slice=$1; effort=$2
mkdir -p /tmp/recov/work /tmp/recov/reports /tmp/recov/runs
prompt="You are the executor for recovery slice ${slice}. Read /tmp/recov/TEAM_BRIEF.md, then /tmp/recov/slices/${slice}.md, and carry it out completely. Write your report to /tmp/recov/reports/${slice}.md."
if [ $# -ge 3 ]; then prompt="$prompt Then read $3: it contains review findings you must address; append a 'Fixes' section to your report."; fi
codex exec -m gpt-6-sol -c model_reasoning_effort=${effort} -c 'service_tier="priority"' \
  -s workspace-write --add-dir /tmp/recov -C /Users/austinli/Projects/sec-auction \
  -o /tmp/recov/runs/${slice}.last.md "$prompt" > /tmp/recov/runs/${slice}.log 2>&1
echo "exit=$? slice=${slice}"
