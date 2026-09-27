#!/usr/bin/env python3
"""Preserve and package finished runs without reading or grading workbook cells."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import random
import shutil
import tarfile

PACKET = Path(__file__).resolve().parents[1]
PROJECT = PACKET.parents[2]
RUNS = PROJECT / "_dev/runs" / PACKET.name


def read(path):
    return json.loads(path.read_text())


def write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2) + "\n")


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def preserve_workspace(cell_id):
    source = RUNS / cell_id
    dest = PACKET / "runs" / cell_id
    archive = dest / "raw-workspace.tar.gz"
    if not source.exists():
        assert archive.exists() and (dest / "raw-workspace-manifest.json").exists()
        return
    inventory = {}
    for p in sorted(source.rglob("*")):
        if p.is_symlink():
            raise RuntimeError(f"Unexpected output symlink: {p}")
        if p.is_file():
            inventory[str(p.relative_to(source))] = sha(p)
    with tarfile.open(archive, "w:gz") as tar:
        tar.add(source, arcname=cell_id)
    verified = {}
    with tarfile.open(archive, "r:gz") as tar:
        for item in tar:
            if item.isfile():
                rel = str(Path(item.name).relative_to(cell_id))
                h = hashlib.sha256()
                with tar.extractfile(item) as f:
                    for chunk in iter(lambda: f.read(1024 * 1024), b""):
                        h.update(chunk)
                verified[rel] = h.hexdigest()
    assert verified == inventory, cell_id
    assert all(sha(source / rel) == value for rel, value in inventory.items()), cell_id
    write(dest / "raw-workspace-manifest.json", {
        "files": inventory, "archive_sha256": sha(archive), "verified": True,
    })
    shutil.rmtree(source)


def main():
    plan = read(PACKET / "plan.json")
    setup = read(PACKET / "SETUP.json")
    pin = read(PACKET / "pin.json")
    assert sha(Path(plan["instruction"]["path"])) == plan["instruction"]["sha256"]
    for rel, digest in setup["tools"].items():
        assert sha(PROJECT / rel) == digest, rel
    for binary in pin["binaries"].values():
        assert sha(Path(binary["path"])) == binary["sha256"]
    for deal, filing in setup["filings"].items():
        assert sha(PACKET / "inputs/raw_filing" / filing["file"]) == filing["sha256"], deal
    cells = plan["cells"]
    assert len(cells) == 15 and len({c["id"] for c in cells}) == 15
    missing = [c["id"] for c in cells if not (PACKET / "runs" / c["id"] / "receipt.json").exists()]
    if missing:
        raise SystemExit(f"Not finished: {len(missing)} receipts still absent")
    key_path = PACKET / "administration/blind-key.json"
    if key_path.exists():
        key = read(key_path)
    else:
        key = {}
        for deal in plan["deals"]:
            group = [c for c in cells if c["deal"] == deal]
            random.SystemRandom().shuffle(group)
            for label, cell in zip("ABCDE", group):
                key[f"{deal}/{label}"] = cell
        write(key_path, key)
    labels = {cell["id"]: label for label, cell in key.items()}
    outcomes, blinded = [], []
    for cell in cells:
        folder = PACKET / "runs" / cell["id"]
        receipt = read(folder / "receipt.json")
        status = read(folder / "status.json")
        metadata = read(folder / "metadata.json")
        assert receipt["state"] in ("completed", "failed", "timed_out")
        assert not receipt["mismatches"], cell["id"]
        assert metadata["mode"] == "extract"
        assert metadata["instruction_sha256"] == plan["instruction"]["sha256"]
        assert metadata["filing_sha256"] == setup["filings"][cell["deal"]]["sha256"]
        workbook = folder / f"{cell['deal']}.xlsx"
        # Preserve even an unreadable/partial output; it is not silently discarded.
        original = RUNS / cell["id"] / "extraction" / workbook.name
        if not workbook.exists() and original.exists():
            shutil.copy2(original, workbook)
        digest = sha(workbook) if workbook.exists() else None
        if receipt.get("workbook_sha256"):
            assert digest == receipt["workbook_sha256"]
        label = labels[cell["id"]]
        blind_path = PACKET / "blinded" / f"{label}.xlsx"
        if workbook.exists():
            blind_path.parent.mkdir(parents=True, exist_ok=True)
            if not blind_path.exists():
                shutil.copy2(workbook, blind_path)
            assert sha(blind_path) == digest
            workbook.chmod(0o444)
            blind_path.chmod(0o444)
        preserve_workspace(cell["id"])
        outcomes.append({
            "id": cell["id"], "deal": cell["deal"], "model": cell["model"],
            "effort": cell["effort"], "state": status["state"],
            "failure_reason": status.get("failure_reason"),
            "started_at": status.get("started_at"), "ended_at": status.get("ended_at"),
            "elapsed_seconds": status.get("elapsed_seconds"),
            "workbook": str(workbook.relative_to(PACKET)) if workbook.exists() else None,
            "workbook_sha256": digest, "readable_xlsx": status.get("workbook_valid_xlsx", False),
            "mechanical_check": str((folder / "check.json").relative_to(PACKET)) if (folder / "check.json").exists() else None,
            "possible_shell_network_commands": len(receipt.get("network_commands", [])),
            "web_or_delegation_tool_calls": receipt.get("web_or_delegation", []),
            "grading_performed": False,
        })
        blinded.append({
            "deal": cell["deal"], "label": label.split("/")[1],
            "file": f"{label}.xlsx" if workbook.exists() else None,
            "sha256": digest, "administrative_state": status["state"],
            "readable_xlsx": status.get("workbook_valid_xlsx", False),
        })
    protected = read(PACKET / "protected-before.json")
    changed = [name for name, digest in protected.items() if not Path(name).is_file() or sha(Path(name)) != digest]
    write(PACKET / "protected-after.json", {
        "checked_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "changed_paths": changed, "files_checked": len(protected),
    })
    write(PACKET / "blinded/manifest.json", {
        "instruction": "../inputs/SEC_Deal_Ledger_Extraction_Instruction.md",
        "instruction_sha256": plan["instruction"]["sha256"],
        "filings": "../inputs/raw_filing/", "copies_byte_identical": True,
        "labels_randomized_separately_per_deal": True,
        "entries": sorted(blinded, key=lambda r: (r["deal"], r["label"])),
    })
    completion = {
        "finished_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "planned": len(cells), "finished": len(outcomes),
        "completed": sum(o["state"] == "completed" for o in outcomes),
        "workbooks_present": sum(o["workbook"] is not None for o in outcomes),
        "grading_performed": False, "corrections_performed": False,
        "live_files_changed": changed,
        "worktree_retirement": "/home/uctpiaj/work/archive/sec-extraction-worktrees/2026-09-26/sec-extraction-astra-audit.manifest.json",
        "runs": outcomes,
    }
    write(PACKET / "administration/outcomes.json", completion)
    # The grader may read this before unblinding: omit model/run identifiers.
    write(PACKET / "COMPLETION.json", {k: v for k, v in completion.items() if k != "runs"})
    print(json.dumps({k: v for k, v in completion.items() if k != "runs"}, indent=2))


if __name__ == "__main__":
    main()
