#!/usr/bin/env python3
"""Grading-side analysis for the sweep report, run after `blind.py score` and `effort_sweep.py summarize`.

Reads the unblinding key, the per-grader grade files and the packet's summary.json, and writes
<out>/analysis.json plus Markdown tables on stdout:
  - per-arm and per-deal scores (family-balanced, and each family separately);
  - the protocol's decision rule within each provider;
  - grader agreement: Claude-Claude and Claude-Astra score gaps, item-level agreement, full-level
    (pass vs fail) disagreements, and the duplicate controls' score gaps.

Scoring of failures follows PROTOCOL.md: a cell that the model itself failed (time limit, no or
incomplete workbook) scores 0 for its arm; infrastructure failures are retried and never scored.
"""

import argparse
import json
from pathlib import Path
import statistics

INFRASTRUCTURE = ("provider_exit", "provider_error", "worker_error")
PROVIDER_ARMS = {"opus": ("opus-5-5-medium", "opus-5-5-high"), "sol": ("gpt-6-sol-high", "gpt-6-sol-xhigh")}


def mean(values):
    values = [v for v in values if v is not None]
    return round(statistics.mean(values), 2) if values else None


def main():
    root = argparse.ArgumentParser()
    root.add_argument("--packet", required=True)
    root.add_argument("--out", required=True)
    root.add_argument("--key", required=True)
    args = root.parse_args()
    packet, out = Path(args.packet), Path(args.out)
    key = json.loads(Path(args.key).read_text())
    bundles = json.loads((out / "bundle-scores.json").read_text())
    summary = json.loads((packet / "summary.json").read_text())
    references = {deal: {t["id"]: t for t in json.loads((out / "reference" / f"{deal}.json").read_text())["tests"]}
                  for deal in {v["deal"] for v in key.values()}}

    # Cell scores: graded completed cells, plus model failures at 0.
    cells = {}
    for run in summary["runs"]:
        if run["mismatches"] or run["failure_reason"] in INFRASTRUCTURE:
            continue
        entry = {"arm": run["arm"], "deal": run["deal"], "replicate": run["replicate"], "state": run["state"]}
        graded = next((b for b in bundles.values() if b["cell"] == run["id"] and not b["duplicate"]), None)
        if run["state"] == "completed" and graded:
            entry.update(score=graded["score"], claude=graded["claude_mean"], astra=graded["astra"])
        elif run["state"] != "completed":
            entry.update(score=0.0, claude=0.0, astra=0.0, failed=run["failure_reason"])
        else:
            entry.update(score=None, claude=None, astra=None, ungraded=True)
        cells[run["id"]] = entry

    arms = sorted({c["arm"] for c in cells.values()})
    deals = sorted({c["deal"] for c in cells.values()})
    table = {}
    for arm in arms:
        rows = [c for c in cells.values() if c["arm"] == arm]
        table[arm] = {
            "n": len(rows), "failed": sum(1 for c in rows if "failed" in c),
            "score": mean(c["score"] for c in rows), "claude": mean(c["claude"] for c in rows),
            "astra": mean(c["astra"] for c in rows),
            "completed_only_score": mean(c["score"] for c in rows if "failed" not in c),
            "deals": {deal: {"scores": [c["score"] for c in sorted(rows, key=lambda c: c["replicate"]) if c["deal"] == deal],
                             "mean": mean(c["score"] for c in rows if c["deal"] == deal)} for deal in deals},
        }

    # Decision rule, within each provider.
    decision = {}
    for provider, (low, high) in PROVIDER_ARMS.items():
        if low not in table or high not in table:
            continue
        spreads = [max(s) - min(s) for arm in (low, high) for d in table[arm]["deals"].values()
                   if len(s := [x for x in d["scores"] if x is not None]) >= 2]
        pooled = round(statistics.mean(spreads), 2) if spreads else None
        threshold = max(2.0, pooled or 0.0)
        gaps = {deal: (round(table[high]["deals"][deal]["mean"] - table[low]["deals"][deal]["mean"], 2)
                       if table[high]["deals"][deal]["mean"] is not None and table[low]["deals"][deal]["mean"] is not None else None)
                for deal in deals}
        wins = [deal for deal, gap in gaps.items() if gap is not None and gap > threshold]
        decision[provider] = {"lower": low, "higher": high, "pooled_replicate_spread": pooled, "threshold": threshold,
                              "gap_by_deal": gaps, "deals_where_higher_clears": wins,
                              "mean_gap": round(table[high]["score"] - table[low]["score"], 2)
                              if table[high]["score"] is not None and table[low]["score"] is not None else None,
                              "recommended": high if len(wins) >= 2 and table[high]["score"] > table[low]["score"] else low}

    # Grader agreement.
    grades = {}
    for path in (out / "grades").glob("*.json"):
        label, grader = path.name.split(".")[:2]
        grades.setdefault(label, {})[grader] = {g["id"]: g for g in json.loads(path.read_text())["grades"]}
    pairs = {"claude1-claude2": [], "claude-astra": []}
    items = {"claude1-claude2": [0, 0], "claude-astra": [0, 0]}
    full_level = []
    family_by_arm = {}
    for label, by_grader in grades.items():
        info, entry = key[label], bundles[label]
        scores = {g: v["score"] for g, v in entry["graders"].items()}
        if {"claude1", "claude2"} <= scores.keys():
            pairs["claude1-claude2"].append(abs(scores["claude1"] - scores["claude2"]))
        if entry["claude_mean"] is not None and entry["astra"] is not None:
            pairs["claude-astra"].append(entry["claude_mean"] - entry["astra"])
            if not info["duplicate"]:
                family_by_arm.setdefault(info["arm"], []).append(entry["claude_mean"] - entry["astra"])
        for test_id, test in references[info["deal"]].items():
            marks = {g: by_grader[g][test_id]["grade"] for g in by_grader if test_id in by_grader[g]}
            if {"claude1", "claude2"} <= marks.keys():
                items["claude1-claude2"][0] += marks["claude1"] == marks["claude2"]
                items["claude1-claude2"][1] += 1
            for claude in ("claude1", "claude2"):
                if {claude, "astra"} <= marks.keys():
                    items["claude-astra"][0] += marks[claude] == marks["astra"]
                    items["claude-astra"][1] += 1
            if {"pass", "fail"} <= set(marks.values()):
                full_level.append({"label": label, "deal": info["deal"], "test": test_id, "weight": test["weight"],
                                   "marks": marks, "reasons": {g: by_grader[g][test_id]["reason"] for g in marks}})
    duplicates = []
    for label, info in key.items():
        if info["duplicate"]:
            original = next(l for l, v in key.items() if v["cell"] == info["cell"] and not v["duplicate"])
            first, second = bundles[original]["score"], bundles[label]["score"]
            duplicates.append({"cell": info["cell"], "original": first, "duplicate": second,
                               "gap": round(abs(first - second), 2) if first is not None and second is not None else None})
    agreement = {
        "claude1_claude2_mean_abs_gap": mean(pairs["claude1-claude2"]),
        "claude_minus_astra_mean": mean(pairs["claude-astra"]),
        "claude_astra_mean_abs_gap": mean(abs(x) for x in pairs["claude-astra"]),
        "item_agreement": {k: round(a / n, 3) if n else None for k, (a, n) in items.items()},
        "claude_minus_astra_by_arm": {arm: mean(v) for arm, v in sorted(family_by_arm.items())},
        "duplicate_controls": duplicates,
        "full_level_disagreements": len(full_level),
    }
    result = {"cells": cells, "arms": table, "decision": decision, "agreement": agreement, "full_level": full_level}
    (out / "analysis.json").write_text(json.dumps(result, indent=1, sort_keys=True))

    print("| arm | cells | failed | score | Claude graders | Astra | " + " | ".join(deals) + " |")
    print("|---" * (6 + len(deals)) + "|")
    for arm in arms:
        t = table[arm]
        per = " | ".join(f"{t['deals'][d]['mean']} ({', '.join(str(s) for s in t['deals'][d]['scores'])})" for d in deals)
        print(f"| {arm} | {t['n']} | {t['failed']} | {t['score']} | {t['claude']} | {t['astra']} | {per} |")
    print(json.dumps({"decision": decision, "agreement": {k: v for k, v in agreement.items() if k != "duplicate_controls"},
                      "duplicates": duplicates}, indent=1))


if __name__ == "__main__":
    main()
