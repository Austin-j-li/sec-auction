#!/usr/bin/env python3
"""The two steps that ran inline in the session between grading and unblinding, kept for the record.

save:   writes each Claude grader's structured output (the workflow's result list) to
        grades/<label>.<grader>.json and checks every grade set covers its reference's test ids.
freeze: hashes every grade file into the packet's grades-freeze.json. It ran after the access
        audit (which reads only the key's label set) and before `blind.py score`, the first step
        that uses the key's arm mapping.
"""

import collections
import datetime
import hashlib
import json
from pathlib import Path


def save(workflow_output: Path, out: Path) -> None:
    results = json.loads(workflow_output.read_text())["result"]
    queue = {item["label"]: item["deal"] for item in json.loads((out / "queue.json").read_text())}
    tests = {deal: [t["id"] for t in json.loads((out / "reference" / f"{deal}.json").read_text())["tests"]]
             for deal in set(queue.values())}
    for result in results:
        got = [g["id"] for g in result["grades"] or []]
        wanted = tests[queue[result["label"]]]
        duplicated = [i for i, n in collections.Counter(got).items() if n > 1]
        assert set(got) == set(wanted) and not duplicated, (result["label"], result["grader"])
        (out / "grades" / f"{result['label']}.{result['grader']}.json").write_text(
            json.dumps({"grader": result["grader"], "grades": result["grades"]}, indent=1))


def freeze(out: Path, target: Path) -> None:
    files = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((out / "grades").glob("*.json"))}
    record = {
        "frozen_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "before_unblinding": True,
        "note": "SHA-256 of every grade file (label.grader.json) before the label key was read; labels are opaque.",
        "grade_files": files,
        "access_audit": hashlib.sha256((out / "access-audit.json").read_bytes()).hexdigest(),
        "inputs": json.loads((out / "inputs.json").read_text()),
        "all_grades_digest": hashlib.sha256("".join(f"{k}:{v}\n" for k, v in files.items()).encode()).hexdigest(),
    }
    assert not target.exists()
    target.write_text(json.dumps(record, indent=1) + "\n")
