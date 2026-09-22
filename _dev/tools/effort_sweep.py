#!/usr/bin/env python3
"""Plan, run and summarise an effort sweep: the same filings extracted by several arms.

An arm is a provider, model and effort level (opus:claude-opus-5-5:medium, sol:gpt-6-sol:high).
Every cell is an ordinary isolated run, prepared and launched through sandbox/run_model.py with
one instruction and one filing. The provider binaries, the instruction and the runner are pinned
for the whole sweep. The checker runs afterwards, outside the sandbox. Each finished run's
receipts, workbook, checker report and compressed event log are copied into the sweep's review
packet, after which its run folder can be deleted.
"""

from __future__ import annotations

import argparse
from collections import Counter
import csv
import datetime as dt
import gzip
import json
import os
from pathlib import Path
import random
import re
import shutil
import statistics
import subprocess
import sys
import time

from openpyxl import load_workbook

import check_lean
from sandbox import run_model

PROJECT = Path(__file__).resolve().parents[2]
RUNNER = Path(run_model.__file__).resolve()
INSTRUCTION = PROJECT / run_model.INSTRUCTION_NAME
BINARY_ENV = {"opus": "SEC_CLAUDE_BIN", "sol": "SEC_CODEX_BIN"}
RECEIPT_FILES = ("metadata.json", "prompt.txt", "launch.json", "command.json", "status.json",
                 "validation.json", "provider-results.json", "stderr.log", "launcher.log")
FINISHED = ("completed", "failed", "timed_out")
# Failures of the provider or worker rather than of the extraction; they can be retried, and a
# run of them (a usage limit, an outage, expired credentials) stops the sweep.
RETRYABLE = ("provider_exit", "provider_error", "worker_error")
MAX_CONSECUTIVE_RETRYABLE = 3
# List prices per million tokens, used to reprice every Claude cell by one formula. Codex reports
# no cost, and a GPT subscription price per token is not published, so Sol cells are not priced.
PRICES = {
    "claude-opus-5-5": {"input": 4.0, "output": 20.0, "cache_read": 0.20, "cache_write_1h": 8.0, "cache_write_5m": 5.0},
    "claude-opus-5": {"input": 5.0, "output": 25.0, "cache_read": 0.50, "cache_write_1h": 10.0, "cache_write_5m": 6.25},
}
# A shell command that could reach the network from inside the sandbox (which shares the host network).
NETWORK = re.compile(r"\b(curl|wget|urllib|requests\.|http\.client|socket\.|pip3? install)\b|https?://", re.I)


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def filings() -> dict[str, str]:
    with (PROJECT / "raw_filing" / "MANIFEST.csv").open(newline="", encoding="utf-8") as stream:
        return {row["deal"]: row["file"] for row in csv.DictReader(stream)}


def plan(args: argparse.Namespace) -> None:
    packet = Path(args.packet)
    if (packet / "plan.json").exists():
        raise SystemExit(f"refusing to overwrite {packet / 'plan.json'}")
    manifest = filings()
    deals = args.deals.split(",")
    unknown = [deal for deal in deals if deal not in manifest]
    arms = []
    for spec in args.arms:
        provider, _, rest = spec.partition(":")
        model, _, effort = rest.rpartition(":")
        if provider not in BINARY_ENV or model not in run_model.MODELS[provider] or effort not in run_model.EFFORTS[provider]:
            unknown.append(spec)
            continue
        arms.append({"arm": f"{model.removeprefix('claude-')}-{effort}", "provider": provider,
                     "model": model, "effort": effort})
    if unknown or not arms:
        raise SystemExit(f"not an available deal or arm (provider:model:effort): {', '.join(unknown) or 'no arms'}")
    if not 10 <= args.timeout_minutes <= 360:
        raise SystemExit("--timeout-minutes must be between 10 and 360")
    cells = []
    for replicate in range(1, args.replicates + 1):
        # Every replicate block covers all deal-arm pairs in its own seeded random order, so the
        # arms are interleaved over the same period instead of run one after another.
        block = [(deal, arm) for deal in deals for arm in arms]
        random.Random(f"{args.seed}-{replicate}").shuffle(block)
        for deal, arm in block:
            cells.append({"id": f"{deal}-{arm['arm']}-r{replicate}", "deal": deal, "filing": manifest[deal],
                          **arm, "replicate": replicate, "timeout_minutes": args.timeout_minutes})
    packet.mkdir(parents=True, exist_ok=True)
    run_model.write_json(packet / "plan.json", {
        "created_at": now_iso(), "deals": deals, "arms": arms, "replicates": args.replicates,
        "seed": args.seed, "cells": cells,
    })
    print(f"{len(cells)} cells planned in {packet / 'plan.json'}")


def current_pin(providers) -> dict:
    """Each provider's binary, the instruction and the runner, as they are now."""
    binaries = {}
    for provider in sorted(providers):
        if not os.environ.get(BINARY_ENV[provider]):
            raise SystemExit(f"set {BINARY_ENV[provider]} to a pinned binary for the whole sweep")
        binary = Path(os.environ[BINARY_ENV[provider]]).resolve()
        binaries[provider] = {"path": str(binary), "sha256": run_model.sha256(binary)}
    return {"binaries": binaries, "instruction_sha256": run_model.sha256(INSTRUCTION),
            "runner_sha256": run_model.sha256(RUNNER)}


def pin_drift(pin: dict, now: dict) -> list[str]:
    """What in `now` differs from the recorded pin."""
    changed = [key for key in ("instruction_sha256", "runner_sha256") if pin.get(key) != now[key]]
    for provider, binary in now["binaries"].items():
        recorded = pin.get("binaries", {}).get(provider, {})
        if any(recorded.get(key) != value for key, value in binary.items()):
            changed.append(f"{provider} binary")
    return changed


def pin_sweep(packet: Path, providers) -> dict:
    """Record the pin at the first run; afterwards refuse anything that differs from it."""
    now, recorded = current_pin(providers), packet / "pin.json"
    if recorded.exists():
        changed = pin_drift(read_json(recorded), now)
        if changed:
            raise SystemExit(f"{', '.join(changed)} differ from {recorded}; the sweep must use one set of "
                             f"binaries, one instruction and one runner")
        return read_json(recorded)
    for binary in now["binaries"].values():
        binary["version"] = subprocess.run([binary["path"], "--version"], capture_output=True, text=True,
                                           check=True).stdout.strip()
    pin = {**now, "recorded_at": now_iso()}
    run_model.write_json(recorded, pin)
    return pin


def cell_mismatches(cell: dict, run_dir: Path, pin: dict) -> list[str]:
    """Ways a run folder differs from its planned cell or from the sweep's pin."""
    metadata = read_json(run_dir / "metadata.json") if (run_dir / "metadata.json").is_file() else {}
    expected = {
        "mode": "extract", "provider": cell["provider"], "deal": cell["deal"], "filing_name": cell["filing"],
        "model": cell["model"], "effort": cell["effort"], "timeout_seconds": cell["timeout_minutes"] * 60,
        "instruction_sha256": pin["instruction_sha256"], "runner_sha256": pin["runner_sha256"],
    }
    problems = [f"metadata {key}" for key, value in expected.items() if metadata.get(key) != value]
    if (run_dir / "command.json").is_file():
        command = read_json(run_dir / "command.json")
        binary = pin["binaries"].get(cell["provider"], {}).get("sha256")
        problems += [f"command {key}" for key, value in (("provider_binary_sha256", binary),
                                                         ("runner_sha256", pin["runner_sha256"]))
                     if command.get(key) != value]
    return problems


def audit_events(events_path: Path) -> dict[str, list[str]]:
    """Shell commands that look able to reach the network, and any web or delegation tool use.

    Claude reports tool calls as assistant tool_use blocks; Codex as completed items.
    """
    found: dict[str, list[str]] = {"network_commands": [], "web_or_delegation": []}
    for event in run_model.events(events_path):
        blocks = (event.get("message") or {}).get("content") or []
        for block in blocks if isinstance(blocks, list) else []:
            if not isinstance(block, dict) or block.get("type") != "tool_use":
                continue
            if block.get("name") == "Bash":
                command = str((block.get("input") or {}).get("command", ""))
                if NETWORK.search(command):
                    found["network_commands"].append(command[:500])
            elif block.get("name") in ("WebFetch", "WebSearch", "Agent", "Task"):
                found["web_or_delegation"].append(str(block.get("name")))
        item = event.get("item") if event.get("type") == "item.completed" else None
        if isinstance(item, dict):
            if item.get("type") == "command_execution" and NETWORK.search(str(item.get("command", ""))):
                found["network_commands"].append(str(item.get("command"))[:500])
            elif item.get("type") in ("web_search", "collab_tool_call", "mcp_tool_call"):
                found["web_or_delegation"].append(str(item.get("type")))
    return found


def record(cell: dict, run_dir: Path, packet: Path, pin: dict) -> dict:
    """Copy one finished run into the packet and check its workbook outside the sandbox."""
    dest = packet / "runs" / cell["id"]
    dest.mkdir(parents=True, exist_ok=True)
    for name in RECEIPT_FILES:
        if (run_dir / name).is_file():
            shutil.copy2(run_dir / name, dest / name)
    events = run_dir / "events.jsonl"
    if events.is_file():
        with events.open("rb") as source, gzip.open(dest / "events.jsonl.gz", "wb") as target:
            shutil.copyfileobj(source, target)
    status = read_json(run_dir / "status.json")
    workbook = run_dir / "extraction" / f"{cell['deal']}.xlsx"
    receipt = {
        "cell": cell, "state": status.get("state"), "failure_reason": status.get("failure_reason"),
        "mismatches": cell_mismatches(cell, run_dir, pin),
        **(audit_events(events) if events.is_file() else {"network_commands": [], "web_or_delegation": []}),
        "workbook_sha256": None, "check_summary": None, "recorded_at": now_iso(),
    }
    if status.get("workbook_valid_xlsx"):
        shutil.copy2(workbook, dest / workbook.name)
        receipt["workbook_sha256"] = run_model.sha256(workbook)
        report = check_lean.LeanChecker(workbook, PROJECT / "raw_filing" / cell["filing"]).run()
        run_model.write_json(dest / "check.json", report)
        receipt["check_summary"] = report["summary"]
    run_model.write_json(dest / "receipt.json", receipt)
    return receipt


def retry_failed(packet: Path, runs_dir: Path) -> None:
    """Move provider and worker failures aside, keeping them visible, so their cells run again."""
    for receipt_path in sorted((packet / "runs").glob("*/receipt.json")):
        receipt = read_json(receipt_path)
        if receipt["failure_reason"] not in RETRYABLE:
            continue
        cell_id = receipt["cell"]["id"]
        attempt = 1 + len(list((packet / "retried").glob(f"{cell_id}-attempt*")))
        (packet / "retried").mkdir(exist_ok=True)
        receipt_path.parent.rename(packet / "retried" / f"{cell_id}-attempt{attempt}")
        if (runs_dir / cell_id).exists():
            (runs_dir / "retried").mkdir(parents=True, exist_ok=True)
            (runs_dir / cell_id).rename(runs_dir / "retried" / f"{cell_id}-attempt{attempt}")
        print(f"retrying {cell_id} (earlier attempt kept as attempt {attempt})", flush=True)


def run_command(pin: dict, *argv: str) -> None:
    # Every prepare, launch and worker resolves the pinned binaries, not whatever PATH holds now.
    env = {**os.environ, **{BINARY_ENV[provider]: binary["path"] for provider, binary in pin["binaries"].items()}}
    subprocess.run([sys.executable, str(RUNNER), *argv], check=True, stdout=subprocess.DEVNULL, env=env)


def worker_alive(run_dir: Path) -> bool:
    try:
        os.kill(read_json(run_dir / "launch.json")["launcher_pid"], 0)
        return True
    except (OSError, KeyError, ValueError):
        return False


def run(args: argparse.Namespace) -> None:
    packet = Path(args.packet).resolve()
    sweep = read_json(packet / "plan.json")
    providers = {cell["provider"] for cell in sweep["cells"]}
    pin = pin_sweep(packet, providers)
    runs_dir = Path(args.runs_dir or run_model.RUNS / packet.name).resolve()
    if args.retry_failed:
        retry_failed(packet, runs_dir)
    wanted = set(args.only.split(",")) if args.only else None
    pending = [cell for cell in sweep["cells"]
               if not (packet / "runs" / cell["id"] / "receipt.json").exists()
               and (wanted is None or wanted & {cell["id"], cell["arm"], cell["deal"], cell["provider"]})]
    # Cells already launched by an interrupted driver count against the cap before any new one starts.
    pending.sort(key=lambda cell: not (runs_dir / cell["id"] / "status.json").exists())
    versions = ", ".join(binary.get("version", provider) for provider, binary in pin["binaries"].items())
    print(f"{len(pending)} cells to run with concurrency {args.concurrency}; binaries {versions}", flush=True)
    active: dict[str, tuple[dict, Path]] = {}
    consecutive_retryable = 0
    while pending or active:
        while pending and len(active) < args.concurrency:
            cell = pending.pop(0)
            run_dir = runs_dir / cell["id"]
            if not (run_dir / "status.json").exists():
                changed = pin_drift(pin, current_pin(providers))
                if changed:
                    raise SystemExit(f"{', '.join(changed)} changed during the sweep; stopping before {cell['id']}")
                if not (run_dir / "metadata.json").exists():
                    run_command(pin, "prepare", "--provider", cell["provider"], "--run-dir", str(run_dir),
                                "--deal", cell["deal"], "--filing", cell["filing"], "--model", cell["model"],
                                "--effort", cell["effort"], "--timeout-minutes", str(cell["timeout_minutes"]))
                problems = cell_mismatches(cell, run_dir, pin)
                if problems:
                    raise SystemExit(f"{run_dir} does not match its planned cell ({', '.join(problems)}); "
                                     f"move it aside and run again")
                run_command(pin, "launch", "--provider", cell["provider"], "--run-dir", str(run_dir))
            active[cell["id"]] = (cell, run_dir)
            print(f"{now_iso()} started {cell['id']}", flush=True)
        time.sleep(args.poll)
        for cell_id, (cell, run_dir) in list(active.items()):
            status_path = run_dir / "status.json"
            state = read_json(status_path).get("state") if status_path.exists() else None
            if state not in FINISHED:
                if worker_alive(run_dir):
                    continue
                time.sleep(5)  # the worker writes its final status just before it exits
                state = read_json(status_path).get("state") if status_path.exists() else None
                if state not in FINISHED:
                    raise SystemExit(f"worker for {cell_id} exited without a final status; inspect {run_dir}")
            receipt = record(cell, run_dir, packet, pin)
            del active[cell_id]
            print(f"{now_iso()} finished {cell_id}: {receipt['state']} {receipt['failure_reason'] or ''} "
                  f"checker={receipt['check_summary']}", flush=True)
            consecutive_retryable = consecutive_retryable + 1 if receipt["failure_reason"] in RETRYABLE else 0
            if consecutive_retryable >= MAX_CONSECUTIVE_RETRYABLE:
                pending.clear()  # let running cells finish, start no more
                print(f"{consecutive_retryable} provider or worker failures in a row: starting no more cells. "
                      f"Fix the cause, then run again with --retry-failed.", flush=True)


def words(value) -> int:
    return len(str(value).split()) if value not in (None, "") else 0


def ledger_stats(path: Path) -> dict:
    """Size and bid keys of a workbook with the four required sheets; empty if it lacks them."""
    book = load_workbook(path, read_only=True, data_only=True)
    try:
        if book.sheetnames != run_model.SHEETS:
            return {}
        rows = {name: list(book[name].iter_rows(values_only=True)) for name in run_model.SHEETS}
    finally:
        book.close()

    def filled(sheet):
        return [row for row in rows[sheet][1:] if any(cell not in (None, "") for cell in row)]

    header = rows["Deal ledger"][0] if rows["Deal ledger"] else ()
    ledger = [dict(zip(header, row)) for row in filled("Deal ledger")]
    bids = [row for row in ledger if row.get("Event") in check_lean.BID_EVENTS]
    notes = [words(row.get("Note")) for row in ledger]
    return {
        "events": len(ledger), "bids": len(bids), "rounds": len(filled("Rounds")),
        "questions": len(filled("Questions")),
        "note_words_mean": round(statistics.mean(notes), 1) if notes else 0,
        "bid_keys": sorted(f"{row.get('Price low')}|{row.get('Price high')}|{row.get('Date from')}" for row in bids),
    }


def assistant_usage(events_gz: Path) -> dict:
    """Claude token usage from the per-message records, for a run killed before its final usage report."""
    by_message: dict[str, dict] = {}
    with gzip.open(events_gz, "rt", encoding="utf-8", errors="replace") as lines:
        for line in lines:
            try:
                event = json.loads(line)
            except ValueError:
                continue
            message = event.get("message") if isinstance(event, dict) and event.get("type") == "assistant" else None
            if isinstance(message, dict) and message.get("id") and isinstance(message.get("usage"), dict):
                by_message[message["id"]] = message["usage"]
    totals: Counter = Counter()
    for usage in by_message.values():
        totals.update({key: value for key, value in usage.items() if key.endswith("_tokens") and isinstance(value, int)})
        cache = usage.get("cache_creation") or {}
        totals.update({"cache_write_1h_tokens": cache.get("ephemeral_1h_input_tokens") or 0,
                       "cache_write_5m_tokens": cache.get("ephemeral_5m_input_tokens") or 0})
    return dict(totals)


def repriced_cost(model: str, tokens: dict, write_1h: int, write_5m: int) -> float | None:
    prices = PRICES.get(model)
    if not prices or not tokens:
        return None
    unsplit = max((tokens.get("cache_creation_input_tokens") or 0) - write_1h - write_5m, 0)
    cost = ((tokens.get("input_tokens") or 0) * prices["input"] + (tokens.get("output_tokens") or 0) * prices["output"]
            + (tokens.get("cache_read_input_tokens") or 0) * prices["cache_read"]
            + (write_1h + unsplit) * prices["cache_write_1h"] + write_5m * prices["cache_write_5m"])
    return round(cost / 1e6, 4)


def multiset_jaccard(a: list, b: list) -> float:
    first, second = Counter(a), Counter(b)
    union = sum((first | second).values())
    return round(sum((first & second).values()) / union, 3) if union else 1.0


def summarize(args: argparse.Namespace) -> None:
    packet = Path(args.packet)
    grades = read_json(packet / "grades.json") if (packet / "grades.json").exists() else {}
    retried = Counter(read_json(path)["cell"]["arm"] for path in (packet / "retried").glob("*/receipt.json"))
    rows = []
    for receipt_path in sorted((packet / "runs").glob("*/receipt.json")):
        receipt, folder = read_json(receipt_path), receipt_path.parent
        cell, status = receipt["cell"], read_json(folder / "status.json")
        provider, tokens = status.get("provider") or {}, (status.get("usage") or {}).get("tokens") or {}
        write_1h, write_5m = provider.get("cache_write_1h_tokens") or 0, provider.get("cache_write_5m_tokens") or 0
        partial = cell["provider"] == "opus" and (status.get("state") == "timed_out" or not tokens)
        if partial and (folder / "events.jsonl.gz").is_file():
            # A killed Claude invocation never reports its usage; count every message it made instead.
            tokens = assistant_usage(folder / "events.jsonl.gz")
            write_1h, write_5m = tokens.pop("cache_write_1h_tokens", 0), tokens.pop("cache_write_5m_tokens", 0)
        row = {
            "id": cell["id"], "arm": cell["arm"], "provider": cell["provider"], "deal": cell["deal"],
            "replicate": cell["replicate"], "state": receipt["state"], "failure_reason": receipt["failure_reason"],
            "mismatches": receipt["mismatches"], "continuations": status.get("continuations"),
            "network_commands": len(receipt["network_commands"]), "web_or_delegation": len(receipt["web_or_delegation"]),
            "served_models": provider.get("served_models"), "cost_reported": (status.get("usage") or {}).get("cost_usd"),
            "cost_repriced": repriced_cost(cell["model"], tokens, write_1h, write_5m), "cost_is_partial": partial,
            "output_tokens": tokens.get("output_tokens"),
            "thinking_tokens": provider.get("thinking_tokens", tokens.get("reasoning_output_tokens")),
            "turns": provider.get("num_turns"), "api_seconds": round((provider.get("duration_api_ms") or 0) / 1000, 1) or None,
            "elapsed_seconds": status.get("elapsed_seconds"),
            "checker_errors": (receipt["check_summary"] or {}).get("errors"),
            "checker_warnings": (receipt["check_summary"] or {}).get("warnings"),
            "score": (grades.get(cell["id"]) or {}).get("score"),
        }
        if receipt["state"] == "completed" and (folder / f"{cell['deal']}.xlsx").is_file():
            row.update(ledger_stats(folder / f"{cell['deal']}.xlsx"))
        if (folder / "check.json").is_file():
            row["checker_error_codes"] = dict(Counter(issue["code"] for issue in read_json(folder / "check.json")["issues"]
                                                      if issue["severity"] == "error"))
        rows.append(row)

    by_arm: dict[str, dict] = {}
    for arm in dict.fromkeys(row["arm"] for row in rows):
        # A run that does not match its planned cell or the pin is reported but never averaged.
        cells = [row for row in rows if row["arm"] == arm and not row["mismatches"]]
        done = [row for row in cells if row["state"] == "completed"]
        per_deal: dict[str, list] = {}
        for row in done:
            per_deal.setdefault(row["deal"], []).append(row)

        def mean(key):
            values = [row[key] for row in done if isinstance(row.get(key), (int, float))]
            return round(statistics.mean(values), 3) if values else None

        pairs = [(first, second) for deal_rows in per_deal.values()
                 for i, first in enumerate(deal_rows) for second in deal_rows[i + 1:]]
        priced = [row["cost_repriced"] for row in cells if row["cost_repriced"] is not None]
        by_arm[arm] = {
            "cells": len(cells), "completed": len(done), "retried_attempts": retried.get(arm, 0),
            "excluded_mismatched": sum(1 for row in rows if row["arm"] == arm and row["mismatches"]),
            "failures": {row["id"]: row["failure_reason"] for row in cells if row["state"] != "completed"},
            "continuations": sum(row.get("continuations") or 0 for row in cells),
            "total_spend_repriced": round(sum(priced), 2) if priced else None,
            "spend_per_completed": round(sum(priced) / len(done), 3) if priced and done else None,
            **{f"mean_{key}": mean(key) for key in ("score", "cost_repriced", "cost_reported", "output_tokens",
                                                   "thinking_tokens", "turns", "api_seconds", "elapsed_seconds",
                                                   "checker_errors", "checker_warnings", "events", "note_words_mean")},
            "replicate_pairs": len(pairs),
            "mean_bid_jaccard": round(statistics.mean(multiset_jaccard(a.get("bid_keys", []), b.get("bid_keys", []))
                                                      for a, b in pairs), 3) if pairs else None,
            "mean_bid_count_gap": round(statistics.mean(abs((a.get("bids") or 0) - (b.get("bids") or 0))
                                                        for a, b in pairs), 2) if pairs else None,
            "same_round_count_share": round(sum(a.get("rounds") == b.get("rounds") for a, b in pairs) / len(pairs), 3) if pairs else None,
            "mean_event_gap": round(statistics.mean(abs((a.get("events") or 0) - (b.get("events") or 0))
                                                    for a, b in pairs), 2) if pairs else None,
        }
    summary = {"generated_at": now_iso(), "runs": rows, "by_arm": by_arm}
    run_model.write_json(packet / "summary.json", summary)
    columns = ["completed", "mean_score", "spend_per_completed", "mean_output_tokens", "mean_thinking_tokens",
               "mean_elapsed_seconds", "mean_checker_errors", "mean_checker_warnings", "mean_events",
               "mean_bid_jaccard", "same_round_count_share", "continuations"]
    lines = ["| arm | " + " | ".join(columns) + " |", "|---" * (len(columns) + 1) + "|"]
    for arm, values in by_arm.items():
        lines.append(f"| {arm} | " + " | ".join(str(values.get(column)) for column in columns) + " |")
    print("\n".join(lines))


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    sub = root.add_subparsers(dest="command", required=True)
    p = sub.add_parser("plan", help="write a seeded, interleaved run order")
    p.add_argument("--packet", required=True, help="review packet directory for the sweep")
    p.add_argument("--deals", required=True, help="comma-separated deals from raw_filing/MANIFEST.csv")
    p.add_argument("--arms", nargs="+", required=True, help="provider:model:effort, e.g. opus:claude-opus-5-5:medium")
    p.add_argument("--replicates", type=int, default=2)
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--timeout-minutes", type=int, default=run_model.TIMEOUT_SECONDS // 60)
    p.set_defaults(func=plan)
    p = sub.add_parser("run", help="prepare, launch and record the planned cells (authorized runs only)")
    p.add_argument("--packet", required=True)
    p.add_argument("--runs-dir", help="run root (default: _dev/runs/<packet name>)")
    p.add_argument("--concurrency", type=int, default=3)
    p.add_argument("--only", help="comma-separated cell ids, arms, deals or providers to run now")
    p.add_argument("--retry-failed", action="store_true", help="run provider and worker failures again")
    p.add_argument("--poll", type=float, default=30)
    p.set_defaults(func=run)
    p = sub.add_parser("summarize", help="per-run and per-arm metrics from recorded receipts")
    p.add_argument("--packet", required=True)
    p.set_defaults(func=summarize)
    return root


if __name__ == "__main__":
    parsed = parser().parse_args()
    parsed.func(parsed)
