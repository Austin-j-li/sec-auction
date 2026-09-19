#!/usr/bin/env bash
# usage: resume.sh <run folder> ...  Continues, inside the same sandbox and session, any run that ended without a workbook (up to 3 nudges).
cd "$(dirname "$0")"
NUDGE="Continue the task from where you stopped. The finished workbook is not yet saved in extraction/."
for R in "$@"; do (
  for n in 1 2 3; do
    ls $R/extraction/*.xlsx >/dev/null 2>&1 && break
    echo "resume $n" >> $R.resumes
    timeout 4500 ./sandbox_resume.sh "$R" "$NUDGE" < /dev/null >> $R.log 2>> $R.err; echo $? > $R.exit; date +%s > $R.end
  done
  echo "$R resumed=$(wc -l < $R.resumes 2>/dev/null || echo 0) exit=$(cat $R.exit) files=$(ls $R/extraction | tr '\n' ' ')"
) & sleep 5; done; wait
