#!/usr/bin/env bash
# usage: launch.sh <runset folder> <variant> [<variant> ...]   e.g. launch.sh run1 full v15
# One sandboxed session per (variant, deal), all in parallel, each retried if it dies at start-up.
cd "$(dirname "$0")"; SET=$1; shift; L=()
for v in "$@"; do for R in $SET/${v}_*; do [ -d "$R" ] || continue; case "$R" in *.xdg) continue;; esac; L+=("$R"); done; done
exec ./relaunch.sh "${L[@]}"
