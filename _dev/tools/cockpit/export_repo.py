"""Export a cockpit instruction or deal into the repository, for a commit Austin requests.

    export_repo.py [--repo-root STATE_ROOT] [--out-root CHECKOUT] instruction <name-or-id> [--write]
    export_repo.py [--repo-root STATE_ROOT] [--out-root CHECKOUT] deal <slug> --version <id>|working [--write]

--repo-root is the checkout whose _dev/cockpit/state the cockpit uses; --out-root is the
checkout the files are written to (by default the same folder). After the Version 1
switch-over the state lives in the deployment folder, so export into the development clone:

    export_repo.py --repo-root ~/work/Projects/ledger-live --out-root ~/work/Projects/sec-auction ...

--write refuses an output folder that is a Git checkout with a detached HEAD, which is how
the switch-over leaves the running deployment folder.

An instruction export writes a published version's stored text into
SEC_Deal_Ledger_Extraction_Instruction.md, after checking the text against its hash.
A deal export writes a version's workbook (or the working copy, rendered by the same
code as the cockpit's download) to extraction/<slug>.xlsx; for a deal added in the
cockpit it also writes the filing to raw_filing/ and its MANIFEST.csv row. Paths that
either checkout's catalog.json references as immutable originals are never overwritten.

Without --write nothing is written: each target is printed with its current SHA-256
(or "new") and the SHA-256 it would get. The script never commits, and never calls a
model or the network.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import io
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import fetch_filing  # noqa: E402
from cockpit import data  # noqa: E402
from cockpit.instructions import ID_RE, REPOSITORY_INSTRUCTION  # noqa: E402
from cockpit.workspace import WorkspaceError  # noqa: E402

MANIFEST = "raw_filing/MANIFEST.csv"


class Refused(Exception):
    pass


def _sha(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def catalog_paths(value: Any) -> set[str]:
    """Every "path" that catalog.json references, anywhere in it."""
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            if key == "path" and isinstance(item, str):
                found.add(Path(item).as_posix())
            else:
                found |= catalog_paths(item)
    elif isinstance(value, list):
        for item in value:
            found |= catalog_paths(item)
    return found


def _utc(stamp: str) -> str:
    """The manifest's fetched_utc format: 2026-09-21T22:16:19Z."""
    try:
        return dt.datetime.fromisoformat(stamp).astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return stamp


# ---- plans ---------------------------------------------------------------------------


def instruction_plan(cockpit: data.Cockpit, ident: str) -> list[tuple[str, bytes]]:
    conn = cockpit.workspace._connect()
    if conn is None:
        raise Refused("the cockpit has no workspace database")
    try:
        try:
            rows = conn.execute("SELECT * FROM instructions").fetchall()
        except Exception as exc:
            raise Refused("the cockpit has no instructions") from exc
    finally:
        conn.close()
    row = next((r for r in rows if ID_RE.fullmatch(ident) and r["id"] == ident), None)
    row = row or next((r for r in rows if r["name"] and r["name"].lower() == ident.lower()), None)
    if row is None:
        raise Refused(f"no instruction named or with id {ident!r}")
    if row["status"] != "published":
        raise Refused(f"instruction {row['id']} is a draft; only published versions can be exported (publish it in the cockpit first)")
    path = cockpit.instructions.path(row["sha256"])
    try:
        content = path.read_bytes()
    except OSError as exc:
        raise Refused(f"the stored text of {row['name']} is missing ({path.name})") from exc
    if _sha(content) != row["sha256"]:
        raise Refused(f"the stored text of {row['name']} does not match its content address {row['sha256']}; nothing exported")
    return [(REPOSITORY_INSTRUCTION, content)]


def manifest_content(root: Path, added: dict[str, Any]) -> bytes:
    """MANIFEST.csv with the added deal's row added or updated, in the file's existing format."""
    path = root / MANIFEST
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    fields = next(csv.reader(io.StringIO(text)), None) or list(fetch_filing.MANIFEST_FIELDS)
    rows = list(csv.DictReader(io.StringIO(text)))
    entry = {"file": added["file"], "deal": added["slug"], "form_type": added["form_type"], "date_filed": added["date_filed"],
             "source_url": added["source_url"], "document": added["document"], "fetched_utc": _utc(added["fetched_utc"]),
             "bytes": str(added["bytes"]), "sha256": added["sha256"]}
    for row in rows:
        if row.get("file") == entry["file"] and row.get("deal") not in (None, "", entry["deal"]):
            raise Refused(f"{MANIFEST} already lists {entry['file']} for deal {row['deal']}")
    was_sorted = [r.get("file") for r in rows] == sorted(r.get("file") for r in rows)
    index = next((i for i, row in enumerate(rows) if row.get("file") == entry["file"]), None)
    if index is None:
        rows.append(entry)
    else:
        rows[index] = entry
    if was_sorted:
        rows.sort(key=lambda r: r.get("file") or "")
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=fields, lineterminator="\r\n" if "\r\n" in text else "\n", extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue().encode("utf-8")


def deal_plan(cockpit: data.Cockpit, slug: str, version: str, out_root: Path | None = None) -> list[tuple[str, bytes]]:
    ws = cockpit.workspace
    if not data.SLUG_RE.fullmatch(slug or ""):
        raise Refused(f"invalid deal {slug!r}")
    try:
        content = ws.export(slug, version)
    except (data.DealNotFound, WorkspaceError) as exc:
        raise Refused(f"{slug} {version}: {exc}") from exc
    plan = [(f"extraction/{slug}.xlsx", content)]
    added = cockpit.deals.added(slug)
    if added and slug not in ws.catalog()["deals"]:
        row = added[0]
        filing = cockpit.deals.filing_path(row).read_bytes()
        if _sha(filing) != row["sha256"]:
            raise Refused(f"the saved filing of {slug} does not match its recorded SHA-256; nothing exported")
        plan += [(f"raw_filing/{row['file']}", filing), (MANIFEST, manifest_content(out_root or ws.root, row))]
    return plan


# ---- output --------------------------------------------------------------------------


def detached_checkout(root: Path) -> bool:
    """True when root is inside a Git checkout whose HEAD is detached, as the running deployment folder is."""
    def git(*args: str) -> int:
        return subprocess.run(["git", "-C", str(root), *args], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30).returncode
    try:
        return git("rev-parse", "--is-inside-work-tree") == 0 and git("symbolic-ref", "-q", "HEAD") != 0
    except (OSError, subprocess.SubprocessError):
        return False


def check_targets(cockpit: data.Cockpit, plan: list[tuple[str, bytes]], out_root: Path | None = None) -> None:
    protected = catalog_paths(cockpit.workspace.catalog()) if cockpit.workspace.available else set()
    target_catalog = (out_root or cockpit.workspace.root) / "_dev/cockpit/catalog.json"
    if target_catalog.is_file():
        protected |= catalog_paths(json.loads(target_catalog.read_text(encoding="utf-8")))
    for relative, _ in plan:
        if relative in protected:
            raise Refused(f"{relative} is an immutable original referenced by _dev/cockpit/catalog.json; "
                          "it is not overwritten. Changing it needs a separate, requested edit of the catalog.")


def run(cockpit: data.Cockpit, plan: list[tuple[str, bytes]], write: bool, out_root: Path | None = None) -> list[str]:
    check_targets(cockpit, plan, out_root)
    root = out_root or cockpit.workspace.root
    if write and detached_checkout(root):
        raise Refused(f"{root} is a checkout with a detached HEAD, like the running deployment folder; "
                      "export into the development clone with --out-root")
    lines = []
    for relative, content in plan:
        target = root / relative
        current = _sha(target.read_bytes()) if target.is_file() else "new"
        new = _sha(content)
        lines.append(f"{relative}  {current} -> {new}" + ("  (unchanged)" if current == new else ""))
    if write:
        for relative, content in plan:
            target = root / relative
            if target.is_file() and _sha(target.read_bytes()) == _sha(content):
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            fetch_filing.atomic_write(target, content)
    lines.append("written" if write else "dry run: nothing written; pass --write to write")
    return lines


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo-root", type=Path, default=data.REPO_ROOT, help="the checkout whose cockpit state is exported")
    parser.add_argument("--out-root", type=Path, help="the checkout written to (default: --repo-root)")
    commands = parser.add_subparsers(dest="command", required=True)
    one = commands.add_parser("instruction", help="write a published instruction to " + REPOSITORY_INSTRUCTION)
    one.add_argument("name", help="published name (e.g. Version 1) or 12-character id")
    one.add_argument("--write", action="store_true")
    deal = commands.add_parser("deal", help="write a deal's workbook (and an added deal's filing) to the repository")
    deal.add_argument("slug")
    deal.add_argument("--version", required=True, help="a version id, or 'working' for the working copy")
    deal.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    cockpit = data.Cockpit(args.repo_root.resolve())
    out_root = args.out_root.resolve() if args.out_root else cockpit.workspace.root
    try:
        if not out_root.is_dir():
            raise Refused(f"output folder {out_root} does not exist")
        plan = instruction_plan(cockpit, args.name) if args.command == "instruction" else deal_plan(cockpit, args.slug, args.version, out_root)
        lines = run(cockpit, plan, args.write, out_root)
    except (Refused, OSError, ValueError, WorkspaceError) as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 1
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
