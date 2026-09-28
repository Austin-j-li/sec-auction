#!/usr/bin/env python3
"""Backups of the cockpit's state, restores and the restore rehearsal.

    python3 _dev/tools/cockpit/backup.py create [--repo-root R] [--dest D] [--keep-days 14]
    python3 _dev/tools/cockpit/backup.py restore <backup-dir> --state <dir> [--replace]
    python3 _dev/tools/cockpit/backup.py rehearse [--repo-root R] [--dest D]

A backup is `<dest>/<YYYYMMDD-HHMMSS>Z/`, by default under `~/backups/ledger-live/`: the
workspace database copied with SQLite's online backup API (so a running server or worker is
never interrupted), the file store (`filings/`, `instructions/`, `versions/`, `jobs/`) and
`manifest.json` with every file's hash, the code on disk (git HEAD, checker version, hash of
the frontend's index) and a summary of the working copies and comments. EDGAR lookup caches, the worker lock and credentials (kept outside the
state directory) are not backed up; after a restore, users reconnect their accounts. The
rehearsal restores a fresh backup into a temporary repository root and compares it with the
backup through the same data layer the server uses.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from cockpit import data, runs  # noqa: E402

REPO = HERE.parents[2]
STATE = Path("_dev/cockpit/state")
DB = "workspace.sqlite3"
STORE = ("filings", "instructions", "versions", "jobs")
SERVICES = ("ledger-cockpit", "ledger-worker")
# Not the earlier app's ~/backups/ledger-cockpit/: pruning below removes every dated backup older than
# --keep-days in its destination, and must never reach that app's nightlies (SWITCHOVER.md).
DEFAULT_DEST = Path.home() / "backups/ledger-live"
STAMP_RE = re.compile(r"\d{8}-\d{6}Z\Z")
STAMP = "%Y%m%d-%H%M%SZ"
INPUTS = ("_dev/cockpit/catalog.json", "raw_filing", "SEC_Deal_Ledger_Extraction_Instruction.md")


class BackupError(RuntimeError):
    pass


def _sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"), default=str)


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _rows(conn: sqlite3.Connection | None, query: str, params: tuple = ()) -> list[dict[str, Any]]:
    """Rows as dicts; a missing database or table reads as empty."""
    if conn is None:
        return []
    try:
        return [dict(row) for row in conn.execute(query, params)]
    except sqlite3.OperationalError:
        return []


def _error(exc: BaseException) -> dict[str, str]:
    return {"error": f"{type(exc).__name__}: {exc}"}


# ---- summary and comparison ----------------------------------------------------------


def slugs(cockpit: data.Cockpit) -> list[str]:
    """Catalog deals and deals added in the cockpit."""
    if not cockpit.workspace.available:
        return []
    return sorted(set(cockpit.workspace.catalog()["deals"]) | {row["slug"] for row in cockpit.deals.added()})


def comment_rows(conn: sqlite3.Connection | None, slug: str) -> dict[str, list[dict[str, Any]]]:
    return {"threads": _rows(conn, "SELECT * FROM threads WHERE slug=? ORDER BY id", (slug,)),
            "comments": _rows(conn, "SELECT c.* FROM comments c JOIN threads t ON c.thread_id=t.id WHERE t.slug=? ORDER BY c.id", (slug,)),
            "edits": _rows(conn, "SELECT e.* FROM comment_edits e JOIN comments c ON e.comment_id=c.id JOIN threads t ON c.thread_id=t.id WHERE t.slug=? ORDER BY e.comment_id, e.at, e.previous_body", (slug,))}


def summarize(cockpit: data.Cockpit) -> dict[str, Any]:
    """Per deal: the working revision, its base and a hash of its sheets; thread and comment counts and a hash of the comment rows."""
    ws = cockpit.workspace
    summary: dict[str, Any] = {}
    conn = ws._connect()
    try:
        for slug in slugs(cockpit):
            try:
                item = ws.item(slug)
                if item.get("pending"):
                    entry: dict[str, Any] = {"revision": 0, "base": None, "content_sha256": None}
                else:
                    state, row, base = ws._state(slug, item, conn)
                    entry = {"revision": row["revision"] if row else 0, "base": base["id"], "content_sha256": _digest(state["sheets"])}
            except Exception as exc:  # noqa: BLE001 - one unreadable deal is recorded, not fatal
                entry = _error(exc)
            rows = comment_rows(conn, slug)
            summary[slug] = {**entry, "threads": len(rows["threads"]), "comments": len(rows["comments"]), "comments_sha256": _digest(rows)}
    finally:
        if conn: conn.close()
    return summary


def _part(read) -> Any:
    try:
        return read()
    except Exception as exc:  # noqa: BLE001 - an error is compared like any other value
        return _error(exc)


WORKING_KEYS = ("pending", "ledger", "rounds", "questions", "facts", "findings", "row_review", "versions")
WORKSPACE_KEYS = ("revision", "base_version", "base_sha256", "updated_at", "updated_by")


def _working(cockpit: data.Cockpit, slug: str) -> dict[str, Any]:
    payload = cockpit.workspace.deal(slug)
    return {**{key: payload.get(key) for key in WORKING_KEYS}, "workspace": {key: payload["workspace"].get(key) for key in WORKSPACE_KEYS}}


def snapshot(cockpit: data.Cockpit) -> dict[str, Any]:
    """Everything a restore must reproduce, read only through the cockpit's read paths."""
    ws = cockpit.workspace
    conn = ws._connect()
    try:
        deals = {}
        for slug in slugs(cockpit):
            deals[slug] = {
                "working copy": _part(lambda: _working(cockpit, slug)),
                "history": _part(lambda: ws.history(slug)),
                "comments": _part(lambda: {"threads": cockpit.trace.comments(slug), "edits": comment_rows(conn, slug)["edits"]}),
                "versions": _part(lambda: runs.imported_versions(ws, slug)),
            }
        texts = {}
        instructions = {"rows": _rows(conn, "SELECT * FROM instructions ORDER BY id"),
                        "edits": _rows(conn, "SELECT * FROM instruction_edits ORDER BY instruction_id, seq"),
                        "default": _rows(conn, "SELECT * FROM settings WHERE key='default_instruction'")}
        for row in instructions["rows"] + instructions["edits"]:
            texts[row["sha256"]] = _part(lambda: cockpit.instructions.text(row["sha256"]))
        instructions["texts"] = texts
        return {"deals": deals, "added deals": _part(cockpit.deals.added),
                "hidden deals": _rows(conn, "SELECT * FROM hidden_deals ORDER BY slug"),
                "deal review": _rows(conn, "SELECT * FROM deal_review ORDER BY slug"),
                "instructions": instructions, "summary": summarize(cockpit)}
    finally:
        if conn: conn.close()


def _differ(before: Any, after: Any) -> str:
    """A short description of where two values first differ."""
    if isinstance(before, dict) and isinstance(after, dict):
        for key in sorted(before.keys() | after.keys(), key=str):
            if key not in before or key not in after:
                return f"{key}: only in the {'restore' if key in after else 'source'}"
            if before[key] != after[key]:
                return f"{key}.{_differ(before[key], after[key])}"
    if isinstance(before, list) and isinstance(after, list):
        if len(before) != len(after):
            return f"{len(before)} vs {len(after)} entries"
        index = next(i for i, (a, b) in enumerate(zip(before, after)) if a != b)
        return f"[{index}].{_differ(before[index], after[index])}"
    return f"{_canonical(before)[:120]} vs {_canonical(after)[:120]}"


def compare_summaries(source: dict[str, Any], restored: dict[str, Any], label: str = "summary") -> list[dict[str, Any]]:
    differences = []
    for slug in sorted(source.keys() | restored.keys()):
        left, right = source.get(slug, {}), restored.get(slug, {})
        for part, keys in (("working copy", ("revision", "base", "content_sha256", "error")), ("comments", ("threads", "comments", "comments_sha256"))):
            if any(left.get(key) != right.get(key) for key in keys):
                differences.append({"deal": slug, "part": part, "detail": f"{label} " + _differ({k: left.get(k) for k in keys}, {k: right.get(k) for k in keys})})
    return differences


def compare_snapshots(source: dict[str, Any], restored: dict[str, Any]) -> list[dict[str, Any]]:
    differences = []
    for slug in sorted(source["deals"].keys() | restored["deals"].keys()):
        left, right = source["deals"].get(slug), restored["deals"].get(slug)
        if left is None or right is None:
            differences.append({"deal": slug, "part": "deal", "detail": f"only in the {'restore' if left is None else 'source'}"})
            continue
        for part in left:
            if left[part] != right.get(part):
                differences.append({"deal": slug, "part": part, "detail": _differ(left[part], right.get(part))})
    differences += compare_summaries(source["summary"], restored["summary"])
    for part in ("added deals", "hidden deals", "instructions"):
        if source[part] != restored[part]:
            differences.append({"deal": None, "part": part, "detail": _differ(source[part], restored[part])})
    return differences


def compare(source: data.Cockpit, restored: data.Cockpit) -> list[dict[str, Any]]:
    """Differences between two cockpits' states, per deal and overall. Empty when they match."""
    return compare_snapshots(snapshot(source), snapshot(restored))


def table_rows(db: Path) -> dict[str, Any]:
    """Every user table's schema and rows, in a stable order."""
    conn = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    try:
        tables = {}
        for name, sql in conn.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"):
            rows = conn.execute(f'SELECT * FROM "{name}"').fetchall()
            tables[name] = {"sql": sql, "rows": sorted(rows, key=repr)}
        return tables
    finally:
        conn.close()


def compare_tables(source: Path, restored: Path) -> list[dict[str, Any]]:
    left, right = table_rows(source), table_rows(restored)
    differences = []
    for name in sorted(left.keys() | right.keys()):
        if name not in left or name not in right:
            differences.append({"deal": None, "part": "tables", "detail": f"table {name} only in the {'restore' if name in right else 'source'}"})
        elif left[name] != right[name]:
            detail = "schema differs" if left[name]["sql"] != right[name]["sql"] else f"{len(left[name]['rows'])} vs {len(right[name]['rows'])} rows, contents differ"
            differences.append({"deal": None, "part": "tables", "detail": f"table {name}: {detail}"})
    return differences


# ---- create ----------------------------------------------------------------------------


def _store_files(state: Path) -> list[Path]:
    """Regular files of the store, relative to the state directory."""
    files = []
    for name in STORE:
        top = state / name
        if not top.is_dir() or top.is_symlink():
            continue
        for folder, dirs, names in os.walk(top):
            dirs[:] = sorted(d for d in dirs if not (Path(folder) / d).is_symlink())
            for entry in sorted(names):
                path = Path(folder) / entry
                if path.is_file() and not path.is_symlink() and not entry.endswith(("-wal", "-shm")):
                    files.append(path.relative_to(state))
    return files


def _git_head(root: Path) -> str | None:
    try:
        found = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    return found.stdout.strip() or None if found.returncode == 0 else None


def _code_on_disk(root: Path) -> dict[str, str | None]:
    """The code on disk beside `git_head`, which misses uncommitted changes: the checker's version
    and the hash of the served `dist/index.html`, which names the frontend's hashed assets."""
    checker, index = root / "_dev/tools/check_lean.py", root / "_dev/tools/cockpit/dist/index.html"
    try:
        found = re.search(r'^CHECKER_VERSION = "([^"]+)"', checker.read_text(encoding="utf-8"), re.M)
    except OSError:
        found = None
    return {"checker_version": found.group(1) if found else None, "dist_index_sha256": _sha(index) if index.is_file() else None}


def _copy_database(source: Path, target: Path) -> dict[str, int]:
    """Copy with the online backup API, as a rollback-journal file, and check its integrity."""
    src = sqlite3.connect(source, timeout=30)
    try:
        dst = sqlite3.connect(target)
        try:
            src.backup(dst)
            dst.execute("PRAGMA journal_mode=DELETE")
            result = [row[0] for row in dst.execute("PRAGMA integrity_check")]
            if result != ["ok"]:
                raise BackupError(f"integrity check of the copy failed: {'; '.join(map(str, result))[:200]}")
            names = [row[0] for row in dst.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")]
            return {name: dst.execute(f'SELECT COUNT(*) FROM "{name}"').fetchone()[0] for name in names}
        finally:
            dst.close()
    finally:
        src.close()


def _summary_of(repo_root: Path, db: Path) -> dict[str, Any]:
    """The summary of a backed-up database, read with the checkout's inputs and store."""
    cockpit = data.Cockpit(repo_root)
    cockpit.workspace.db_path = db
    return summarize(cockpit)


def backups(dest: Path) -> list[Path]:
    """Finished backups made by this script, oldest first."""
    if not dest.is_dir():
        return []
    return sorted(p for p in dest.iterdir() if STAMP_RE.fullmatch(p.name) and p.is_dir() and not p.is_symlink() and (p / "manifest.json").is_file())


def prune(dest: Path, keep_days: int, now: dt.datetime | None = None) -> list[Path]:
    """Remove backups older than keep_days (always keeping the newest) and stale partial folders."""
    now = now or dt.datetime.now(dt.timezone.utc)
    cutoff = now - dt.timedelta(days=keep_days)
    found = backups(dest)
    removed = [p for p in found[:-1] if dt.datetime.strptime(p.name, STAMP).replace(tzinfo=dt.timezone.utc) < cutoff]
    removed += [p for p in dest.iterdir() if p.name.startswith(".partial-") and p.is_dir() and not p.is_symlink()] if dest.is_dir() else []
    for path in removed:
        shutil.rmtree(path)
    return removed


def create(repo_root: Path = REPO, dest: Path = DEFAULT_DEST, keep_days: int | None = 14, now: dt.datetime | None = None) -> Path:
    repo_root = Path(repo_root).resolve()
    state = repo_root / STATE
    if not (state / DB).is_file():
        raise BackupError(f"no workspace database at {state / DB}")
    if not dest.exists():
        dest.mkdir(mode=0o700, parents=True)
    now = now or dt.datetime.now(dt.timezone.utc)
    while (dest / now.strftime(STAMP)).exists():  # two backups in one second: the later takes the next free stamp
        now += dt.timedelta(seconds=1)
    stamp = now.strftime(STAMP)
    final, partial = dest / stamp, dest / f".partial-{stamp}"
    partial.mkdir(mode=0o700)
    try:
        # The database first: every version it names was written to the store before its row.
        tables = _copy_database(state / DB, partial / DB)
        files = []
        for relative in _store_files(state):
            target = partial / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(state / relative, target)
            files.append({"path": relative.as_posix(), "bytes": target.stat().st_size, "sha256": _sha(target)})
        manifest = {"created_at": now.isoformat(timespec="seconds"), "state": str(state), "git_head": _git_head(repo_root), **_code_on_disk(repo_root),
                    "database": {"path": DB, "bytes": (partial / DB).stat().st_size, "sha256": _sha(partial / DB), "tables": tables},
                    "files": files, "summary": _summary_of(repo_root, partial / DB)}
        (partial / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        os.rename(partial, final)
    except BaseException:
        shutil.rmtree(partial, ignore_errors=True)
        raise
    if keep_days is not None:
        prune(dest, keep_days, now)
    return final


# ---- restore ---------------------------------------------------------------------------


def verify(backup: Path) -> dict[str, Any]:
    """The manifest, after checking every listed file against its size and hash."""
    try:
        manifest = json.loads((backup / "manifest.json").read_text(encoding="utf-8"))
        entries = [manifest["database"], *manifest["files"]]
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise BackupError(f"{backup} has no readable manifest ({exc})") from exc
    for entry in entries:
        relative = Path(entry["path"])
        if relative.is_absolute() or ".." in relative.parts or not (relative.as_posix() == DB or relative.parts[0] in STORE):
            raise BackupError(f"manifest lists an unsafe path {entry['path']!r}")
        path = backup / relative
        if not path.is_file() or path.is_symlink() or path.stat().st_size != entry["bytes"] or _sha(path) != entry["sha256"]:
            raise BackupError(f"{entry['path']} does not match the manifest; nothing was restored")
    return manifest


def services_active() -> list[str]:
    try:
        found = subprocess.run(["systemctl", "--user", "is-active", *SERVICES], capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError) as exc:
        raise BackupError(f"cannot check whether {' and '.join(SERVICES)} are running ({exc})") from exc
    states = found.stdout.split()
    return [name for name, status in zip(SERVICES, states) if status in ("active", "activating", "reloading", "deactivating")]


def restore(backup: Path, target: Path, replace: bool = False, repo_root: Path = REPO, now: dt.datetime | None = None) -> Path:
    backup, target = Path(backup).resolve(), Path(target).absolute()
    manifest = verify(backup)
    live = {(Path(repo_root) / STATE).resolve(), Path(manifest.get("state") or "/nonexistent").resolve()}
    if target.resolve() in live:
        running = services_active()
        if running:
            raise BackupError(f"{target} is the live state and {', '.join(running)} {'is' if len(running) == 1 else 'are'} running; stop them first")
    occupied = target.exists() and (not target.is_dir() or any(target.iterdir()))
    if occupied and not replace:
        raise BackupError(f"{target} is not empty; restore into a new directory or pass --replace")
    stamp = (now or dt.datetime.now(dt.timezone.utc)).strftime(STAMP)
    building = target.with_name(f".{target.name}.restoring-{stamp}")
    if building.exists():
        shutil.rmtree(building)
    target.parent.mkdir(parents=True, exist_ok=True)
    building.mkdir()
    try:
        for entry in [manifest["database"], *manifest["files"]]:
            destination = building / entry["path"]
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(backup / entry["path"], destination)
        (building / "lookups").mkdir()
        if occupied:
            aside = target.with_name(f"{target.name}.before-restore-{stamp}")
            if aside.exists():
                raise BackupError(f"{aside} already exists")
            os.rename(target, aside)
        elif target.exists():
            target.rmdir()
        os.rename(building, target)
    except BaseException:
        shutil.rmtree(building, ignore_errors=True)
        raise
    return target


# ---- rehearse --------------------------------------------------------------------------


def stage_root(repo_root: Path, backup: Path, root: Path) -> data.Cockpit:
    """A repository root holding the restored state and the checkout's other inputs.

    Catalog workbooks are copied, not linked: the workspace refuses a path that resolves outside its root."""
    repo_root = Path(repo_root).resolve()
    for relative in INPUTS:
        source = repo_root / relative
        if source.exists():
            (root / relative).parent.mkdir(parents=True, exist_ok=True)
            (root / relative).symlink_to(source)
    catalog = data.Cockpit(repo_root).workspace.catalog()
    paths = {f"extraction/{slug}.xlsx" for slug in catalog["deals"]}
    paths |= {version["path"] for item in catalog["deals"].values() if isinstance(item, dict) for version in item.get("versions", []) if isinstance(version.get("path"), str)}
    for relative in sorted(paths):
        source = (repo_root / relative).resolve()
        if repo_root in source.parents and "ref" not in source.relative_to(repo_root).parts and source.is_file():
            (root / relative).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, root / relative)
    restore(backup, root / STATE, repo_root=repo_root)
    return data.Cockpit(root)


def rehearse(repo_root: Path = REPO, dest: Path = DEFAULT_DEST, keep_days: int | None = 14) -> dict[str, Any]:
    repo_root = Path(repo_root).resolve()
    backup = create(repo_root, dest, keep_days)
    manifest = verify(backup)
    source = data.Cockpit(repo_root)
    source.workspace.db_path = backup / DB
    root = Path(tempfile.mkdtemp(prefix=".rehearse-", dir=dest))
    try:
        restored = stage_root(repo_root, backup, root)
        before, after = snapshot(source), snapshot(restored)
        differences = compare_snapshots(before, after)
        differences += compare_summaries(manifest["summary"], after["summary"], "manifest summary")
        differences += compare_tables(backup / DB, root / STATE / DB)
    finally:
        shutil.rmtree(root, ignore_errors=True)
    return {"backup": str(backup), "deals": len(after["deals"]),
            "working_copies_equal": not any(d["part"] in ("deal", "working copy", "history", "versions") for d in differences),
            "comments_equal": not any(d["part"] == "comments" for d in differences),
            "differences": differences}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    commands = parser.add_subparsers(dest="command", required=True)
    make = commands.add_parser("create", help="back up the live state")
    make.add_argument("--repo-root", type=Path, default=REPO)
    make.add_argument("--dest", type=Path, default=DEFAULT_DEST)
    make.add_argument("--keep-days", type=int, default=14)
    back = commands.add_parser("restore", help="restore a backup into an empty or new state directory")
    back.add_argument("backup", type=Path)
    back.add_argument("--state", type=Path, required=True)
    back.add_argument("--replace", action="store_true", help="move a non-empty target aside first")
    back.add_argument("--repo-root", type=Path, default=REPO)
    check = commands.add_parser("rehearse", help="back up, restore into a temporary root and compare")
    check.add_argument("--repo-root", type=Path, default=REPO)
    check.add_argument("--dest", type=Path, default=DEFAULT_DEST)
    args = parser.parse_args(argv)
    try:
        if args.command == "create":
            print(create(args.repo_root, args.dest, args.keep_days))
        elif args.command == "restore":
            print(restore(args.backup, args.state, args.replace, args.repo_root))
        else:
            report = rehearse(args.repo_root, args.dest)
            print(json.dumps(report, indent=2, ensure_ascii=False))
            return 0 if not report["differences"] else 1
    except Exception as exc:  # noqa: BLE001 - one line, non-zero exit
        print(f"backup.py {args.command}: {type(exc).__name__}: {' '.join(str(exc).split())}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
