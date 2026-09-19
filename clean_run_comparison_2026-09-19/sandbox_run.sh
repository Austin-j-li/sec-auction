#!/usr/bin/env bash
# Run one opencode session inside a bubblewrap sandbox that can see ONLY its own run folder.
# usage: sandbox_run.sh <run_folder> <prompt text>
# The run folder must already hold the instruction, raw_filing/ and an empty extraction/.
set -euo pipefail
RUN=$(readlink -f "$1"); PROMPT="$2"
MODEL="${MODEL:-deepseek/deepseek-flash#max}"
H=/home/uctpiaj
NODE=$H/.nvm/versions/node/v24.21.0
XDG="$RUN.xdg"                      # per-run opencode state, kept outside the folder the agent works in
mkdir -p "$XDG/data/opencode" "$XDG/config/opencode" "$XDG/state" "$XDG/cache/opencode"
# credentials: the DeepSeek key only, passed through the environment (never written into the run folder)
export DEEPSEEK_API_KEY="$(python3 -c "import json,os;print(json.load(open(os.path.expanduser('~/.local/share/opencode/auth.json')))['deepseek']['key'])")"
cat > "$XDG/config/opencode/opencode.jsonc" <<'JSON'
{ "$schema": "https://opencode.ai/config.json",
  "permission": { "edit": "allow", "bash": "allow", "webfetch": "deny", "external_directory": "allow" } }
JSON
[ -f $H/.cache/opencode/models.json ] && cp $H/.cache/opencode/models.json "$XDG/cache/opencode/" || true
RESOLV=()
[ -d /run/systemd/resolve ] && RESOLV=(--ro-bind /run/systemd/resolve /run/systemd/resolve)
exec bwrap --unshare-all --share-net --die-with-parent --new-session \
  --ro-bind /usr /usr --symlink usr/bin /bin --symlink usr/sbin /sbin --symlink usr/lib /lib --symlink usr/lib64 /lib64 \
  --ro-bind /etc/ssl /etc/ssl --ro-bind /etc/ca-certificates /etc/ca-certificates \
  --ro-bind /etc/resolv.conf /etc/resolv.conf --ro-bind /etc/hosts /etc/hosts --ro-bind /etc/nsswitch.conf /etc/nsswitch.conf \
  --ro-bind /etc/alternatives /etc/alternatives --ro-bind /etc/passwd /etc/passwd --ro-bind /etc/group /etc/group --ro-bind /etc/localtime /etc/localtime \
  "${RESOLV[@]}" \
  --proc /proc --dev /dev --tmpfs /tmp --tmpfs /run/user --tmpfs $H \
  --ro-bind $NODE $NODE --ro-bind $H/miniforge3 $H/miniforge3 \
  --bind "$RUN" $H/work --bind "$XDG" $H/.xdg \
  --setenv HOME $H --setenv USER uctpiaj \
  --setenv PATH "$NODE/bin:$H/miniforge3/bin:/usr/local/bin:/usr/bin:/bin" \
  --setenv XDG_DATA_HOME $H/.xdg/data --setenv XDG_CONFIG_HOME $H/.xdg/config \
  --setenv XDG_STATE_HOME $H/.xdg/state --setenv XDG_CACHE_HOME $H/.xdg/cache \
  --chdir $H/work \
  opencode run --standalone --auto --agent build --model "$MODEL" --format json --title "$(basename "$RUN")" "$PROMPT"
