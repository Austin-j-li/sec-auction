#!/usr/bin/env python3
"""PreToolUse allowlist hook for isolated Antigravity (agy) extraction runs.

Allows only local filesystem, search, and shell-command tools. Web, browser,
subagent, workflow, scheduling, MCP, and user-prompt tools are hard-denied even
when `--dangerously-skip-permissions` is active.
"""
from __future__ import annotations

import json
import sys

ALLOWED_TOOLS = frozenset({
    "view_file",
    "read_file",
    "view_file_outline",
    "view_code_item",
    "list_dir",
    "find_by_name",
    "grep_search",
    "codebase_search",
    "write_to_file",
    "write_file",
    "replace_file_content",
    "multi_replace_file_content",
    "edit_file",
    "run_command",
    "command_status",
    "send_command_input",
    "manage_task",
})


def _deny(reason: str) -> int:
    sys.stdout.write(json.dumps({"decision": "deny", "reason": reason}) + "\n")
    sys.stdout.flush()
    return 0


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:  # noqa: BLE001 - fail closed on malformed hook input
        return _deny("Malformed PreToolUse payload")
    if not isinstance(payload, dict):
        return _deny("Malformed PreToolUse payload")
    tool_call = payload.get("toolCall")
    name = tool_call.get("name") if isinstance(tool_call, dict) else None
    if not isinstance(name, str) or not name:
        name = payload.get("tool_name") if isinstance(payload.get("tool_name"), str) else ""
    if not name:
        return _deny("Malformed PreToolUse payload")
    if name in ALLOWED_TOOLS:
        sys.stdout.write('{"decision": "allow"}\n')
        sys.stdout.flush()
        return 0
    return _deny(f"Tool {name!r} is disabled in the isolated SEC extraction sandbox.")


if __name__ == "__main__":
    raise SystemExit(main())
