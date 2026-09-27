"""Create a clean cockpit state from an older state directory.

Usage: python3 _dev/tools/cockpit/fresh_state.py OLD_STATE NEW_STATE

Only account metadata, added-deal rows, and their verified filing files cross the
boundary. The source database is opened read-only and captured with SQLite's
online backup API, which includes committed WAL transactions. NEW_STATE must not
exist. The repository catalog and instruction are supplied by the application.
"""
from __future__ import annotations

import argparse
import ctypes
import errno
import hashlib
import os
import re
import shutil
import sqlite3
import stat
import sys
import tempfile
from contextlib import closing
from pathlib import Path


DATABASE = "workspace.sqlite3"
TABLES = {
    "accounts": {"user", "provider", "connected_at", "expires_at"},
    "added_deals": {"slug", "name", "form_type", "date_filed", "file", "source_kind",
                    "seed_deal", "index_url", "source_url", "document", "fetched_utc",
                    "bytes", "sha256", "added_by", "added_at"},
}
SLUG = re.compile(r"[a-z0-9][a-z0-9-]{0,59}\Z")
SHA256 = re.compile(r"[0-9a-f]{64}\Z")


class FreshStateError(ValueError):
    """The source state or destination cannot be used safely."""


def _contained(path: Path, parent: Path) -> bool:
    return path == parent or parent in path.parents


def _validate_paths(source: Path, destination: Path) -> tuple[Path, Path]:
    if source.is_symlink() or not source.is_dir():
        raise FreshStateError("source must be a real state directory")
    if destination.exists() or destination.is_symlink():
        raise FreshStateError("destination already exists")
    if not destination.parent.is_dir():
        raise FreshStateError("destination parent does not exist")
    old = source.resolve(strict=True)
    new = destination.resolve(strict=False)
    if _contained(old, new) or _contained(new, old):
        raise FreshStateError("source and destination overlap")
    database = source / DATABASE
    if database.is_symlink() or not database.is_file():
        raise FreshStateError("source database is missing or is a symlink")
    return database, new


def _snapshot(database: Path, target: Path) -> None:
    with closing(sqlite3.connect(f"{database.resolve().as_uri()}?mode=ro", uri=True, timeout=30)) as source:
        source.execute("PRAGMA query_only=ON")
        with closing(sqlite3.connect(target)) as copy:
            source.backup(copy)


def _table_sql(snapshot: sqlite3.Connection, name: str) -> str:
    row = snapshot.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (name,)).fetchone()
    if row is None or not row[0]:
        raise FreshStateError(f"source lacks required {name} table")
    columns = {column[1] for column in snapshot.execute(f"PRAGMA table_info({name})")}
    if not TABLES[name] <= columns:
        raise FreshStateError(f"source {name} table is incompatible with the app")
    return row[0]


def _copy_tables(snapshot_path: Path, new_database: Path) -> tuple[int, list[tuple[str, str, int, str]]]:
    with closing(sqlite3.connect(f"{snapshot_path.as_uri()}?mode=ro", uri=True)) as source:
        source.row_factory = sqlite3.Row
        schemas = {name: _table_sql(source, name) for name in TABLES}
        added = [tuple(row) for row in source.execute("SELECT slug, file, bytes, sha256 FROM added_deals")]
        counts = {}
        with closing(sqlite3.connect(new_database)) as target:
            with target:
                for name, sql in schemas.items():
                    target.execute(sql)
                    width = len(source.execute(f"SELECT * FROM {name} LIMIT 0").description)
                    rows = source.execute(f"SELECT * FROM {name}")
                    target.executemany(f"INSERT INTO {name} VALUES ({','.join('?' for _ in range(width))})",
                                       (tuple(row) for row in rows))
                    counts[name] = target.execute(f"SELECT count(*) FROM {name}").fetchone()[0]
                if target.execute("PRAGMA quick_check").fetchone()[0] != "ok":
                    raise FreshStateError("new database failed its integrity check")
    return counts["accounts"], added


def _safe_file_name(value: object) -> bool:
    return isinstance(value, str) and value not in ("", ".", "..") and not value.startswith(".") \
        and "/" not in value and "\\" not in value and "\x00" not in value


def _copy_filings(source: Path, stage: Path, added: list[tuple[str, str, int, str]]) -> None:
    store = source / "filings"
    if added and (store.is_symlink() or not store.is_dir()):
        raise FreshStateError("source filings directory is missing or is a symlink")
    for slug, name, size, digest in added:
        if not isinstance(slug, str) or not SLUG.fullmatch(slug) or not _safe_file_name(name):
            raise FreshStateError("added deal has an unsafe filing path")
        if not isinstance(size, int) or size < 0 or not isinstance(digest, str) or not SHA256.fullmatch(digest):
            raise FreshStateError("added deal has invalid filing metadata")
        folder = store / slug
        path = folder / name
        if folder.is_symlink() or not folder.is_dir() or path.is_symlink() or not path.is_file():
            raise FreshStateError("an added-deal filing is missing or is a symlink")
        output = stage / "filings" / slug
        output.mkdir(parents=True, exist_ok=False)
        hasher = hashlib.sha256()
        copied = 0
        descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        with os.fdopen(descriptor, "rb") as reader, (output / name).open("xb") as writer:
            if not stat.S_ISREG(os.fstat(reader.fileno()).st_mode):
                raise FreshStateError("an added-deal filing is not a regular file")
            while block := reader.read(1024 * 1024):
                copied += len(block)
                hasher.update(block)
                writer.write(block)
        if copied != size or hasher.hexdigest() != digest:
            raise FreshStateError("an added-deal filing does not match its database record")


def _publish(stage: Path, destination: Path) -> None:
    """Atomically install the finished directory without replacing a racing creator."""
    try:
        rename = ctypes.CDLL(None, use_errno=True).renameat2
    except AttributeError as exc:
        raise FreshStateError("atomic no-replace rename is unavailable") from exc
    rename.argtypes = (ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint)
    rename.restype = ctypes.c_int
    if rename(-100, os.fsencode(stage), -100, os.fsencode(destination), 1) != 0:
        code = ctypes.get_errno()
        if code == errno.EEXIST:
            raise FreshStateError("destination already exists")
        raise OSError(code, os.strerror(code))


def create(source: Path | str, destination: Path | str) -> dict[str, int]:
    """Build and publish a fresh state; leave no destination on validation failure."""
    source, destination = Path(source), Path(destination)
    database, destination = _validate_paths(source, destination)
    stage = Path(tempfile.mkdtemp(prefix=".fresh-state-", dir=destination.parent))
    published = False
    try:
        snapshot = stage / ".snapshot.sqlite3"
        _snapshot(database, snapshot)
        accounts, added = _copy_tables(snapshot, stage / DATABASE)
        snapshot.unlink()
        for sidecar in (stage / ".snapshot.sqlite3-wal", stage / ".snapshot.sqlite3-shm"):
            sidecar.unlink(missing_ok=True)
        _copy_filings(source, stage, added)
        os.chmod(stage / DATABASE, 0o600)
        if destination.exists() or destination.is_symlink():
            raise FreshStateError("destination already exists")
        _publish(stage, destination)
        published = True
        return {"accounts": accounts, "added_deals": len(added), "filings": len(added)}
    finally:
        if not published and stage.exists():
            shutil.rmtree(stage)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("old_state", type=Path)
    parser.add_argument("new_state", type=Path)
    args = parser.parse_args(argv)
    try:
        summary = create(args.old_state, args.new_state)
    except (FreshStateError, OSError, sqlite3.Error):
        print("Fresh state was not created; check the source and destination.", file=sys.stderr)
        return 1
    print(f"Fresh state created: {summary['accounts']} accounts, {summary['added_deals']} added deals, {summary['filings']} filings.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
