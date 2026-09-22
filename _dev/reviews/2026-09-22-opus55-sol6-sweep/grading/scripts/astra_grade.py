#!/usr/bin/env python3
"""Grade blinded bundles with GPT-6-Astra through Codex: read-only, no web, no connectors, no subagents.

Each bundle gets one fresh `codex exec` session that must return a schema-valid grade for every
reference test. A session that misses tests or returns unparseable output is retried once.
"""

import argparse
import concurrent.futures
import json
from pathlib import Path
import subprocess

CODEX = "/home/uctpiaj/work/agent-homes/.codex-20260905-222709/packages/standalone/releases/0.155.1-x86_64-unknown-linux-musl/bin/codex"
DISABLED = ("apps", "plugins", "remote_plugin", "plugin_sharing", "browser_use", "browser_use_external",
            "browser_use_full_cdp_access", "in_app_browser", "computer_use", "image_generation", "multi_agent",
            "goals", "sleep_tool", "tool_suggest", "view_image", "skill_search", "skill_mcp_dependency_install",
            "mentions_v2", "workspace_dependencies", "hooks")
SCHEMA = {"type": "object", "additionalProperties": False, "required": ["grades"], "properties": {"grades": {
    "type": "array", "items": {"type": "object", "additionalProperties": False, "required": ["id", "grade", "rows", "reason"],
                               "properties": {"id": {"type": "string"}, "grade": {"type": "string", "enum": ["pass", "partial", "fail"]},
                                              "rows": {"type": "string"}, "reason": {"type": "string"}}}}}}


def grader_prompt(out: Path, label: str, deal: str, grader: str) -> str:
    return (Path(__file__).with_name("grader_prompt.txt").read_text()
            .format(workbook=out / "bundles" / label / "workbook.json", reference=out / "reference" / f"{deal}.json",
                    filing=out / "filings" / f"{deal}.htm", instruction=out / "instruction.md",
                    workdir=out / "work" / f"{label}.{grader}"))


def grade(label: str, deal: str, out: Path) -> str:
    wanted = {t["id"] for t in json.loads((out / "reference" / f"{deal}.json").read_text())["tests"]}
    target = out / "grades" / f"{label}.astra.json"
    if target.exists():
        return f"{label}: already graded"
    for attempt in (1, 2):
        raw = out / "grades" / "raw" / f"{label}.astra.attempt{attempt}.jsonl"
        command = [CODEX, "exec", "--ephemeral", "--ignore-user-config", "--ignore-rules", "--skip-git-repo-check",
                   "-s", "read-only", "--json", "--model", "gpt-6-astra", "-c", 'model_reasoning_effort="high"',
                   "-c", 'web_search="disabled"', *[p for f in DISABLED for p in ("--disable", f)],
                   "--output-schema", str(out / "schema.json"), "-C", str(out / "work" / f"{label}.astra"),
                   grader_prompt(out, label, deal, "astra")]
        with raw.open("w") as stdout:
            subprocess.run(command, stdin=subprocess.DEVNULL, stdout=stdout, stderr=subprocess.DEVNULL, timeout=3600)
        message = None
        for line in raw.read_text().splitlines():
            try:
                event = json.loads(line)
            except ValueError:
                continue
            if event.get("type") == "item.completed" and event["item"].get("type") == "agent_message":
                message = event["item"]["text"]
        try:
            grades = json.loads(message)["grades"]
        except (TypeError, ValueError, KeyError):
            continue
        missing = wanted - {g["id"] for g in grades}
        if not missing:
            target.write_text(json.dumps({"grader": "astra", "grades": grades}, indent=1))
            return f"{label}: graded on attempt {attempt}"
    return f"{label}: FAILED after two attempts"


if __name__ == "__main__":
    root = argparse.ArgumentParser()
    root.add_argument("--out", required=True)
    root.add_argument("--concurrency", type=int, default=3)
    args = root.parse_args()
    out = Path(args.out).resolve()  # absolute: the grader runs in its own work directory
    (out / "grades" / "raw").mkdir(parents=True, exist_ok=True)
    (out / "schema.json").write_text(json.dumps(SCHEMA))
    queue = json.loads((out / "queue.json").read_text())
    with concurrent.futures.ThreadPoolExecutor(args.concurrency) as pool:
        for result in pool.map(lambda item: grade(item["label"], item["deal"], out), queue):
            print(result, flush=True)
