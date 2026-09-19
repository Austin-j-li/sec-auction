#!/usr/bin/env bash
# usage: relaunch.sh <run folder> ...   Re-runs sessions that died at start-up ("Model unavailable"), up to 4 tries each.
cd "$(dirname "$0")"
for R in "$@"; do (
  d=${R##*/}; d=${d#*_}; PROMPT=$(sed "s/DEAL/$d/" PROMPT.txt)
  for try in 1 2 3 4; do
    rm -rf "$R.xdg" $R.exit $R.end; date +%s > $R.start
    timeout 4500 ./sandbox_run.sh "$R" "$PROMPT" < /dev/null > $R.log 2> $R.err; rc=$?
    if grep -q '"provider.no-route"' $R.log && [ $(wc -l < $R.log) -le 2 ]; then sleep $((20*try)); continue; fi
    break
  done; echo $rc > $R.exit; date +%s > $R.end
  echo "$R exit=$rc tries=$try minutes=$(( ($(cat $R.end)-$(cat $R.start))/60 )) files=$(ls $R/extraction | tr '\n' ' ')"
) & sleep 15; done; wait
