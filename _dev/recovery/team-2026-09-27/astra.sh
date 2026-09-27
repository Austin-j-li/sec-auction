#!/bin/bash
# usage: astra.sh <slice> <effort>
set -u
slice=$1; effort=$2
out=/tmp/recov/reviews/${slice}.md
mkdir -p /tmp/recov/reviews
prompt="You are the independent reviewer for recovery slice ${slice}. Read /tmp/recov/TEAM_BRIEF.md, the slice spec /tmp/recov/slices/${slice}.md, and the executor's report /tmp/recov/reports/${slice}.md. Then verify the executor's work against the evidence yourself: spot-check replays against /tmp/recov/evidence and /tmp/recov/all_calls_since_0924.jsonl, re-run the slice's tests and acceptance checks (read-only sandbox: if you cannot run something, say so), look for holes: evidence events the executor skipped, unresolved Edit mismatches papered over, invented behaviour not backed by evidence, missing acceptance items, false claims in the report. Stay proportionate: flag only defects that matter for correctness or for faithfully recovering the VM state; do not propose redesigns or extra features. Output a numbered findings list, each with severity (blocker/major/minor), file:line or evidence pointer, and the concrete fix. End with a verdict line: ACCEPT, ACCEPT-WITH-FIXES, or REJECT."
codex exec -m gpt-6-astra -c model_reasoning_effort=${effort} -s read-only -C /Users/austinli/Projects/sec-auction \
  -o "$out" "$prompt" > /tmp/recov/runs/${slice}.review.log 2>&1
echo "exit=$? review=${slice}"; tail -n 3 "$out"
