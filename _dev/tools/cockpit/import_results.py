"""Build a pending catalog of the filed deals from the repository filing manifest.

No historical workbook, receipt or review packet is an input. The resulting deals
receive their first base only after a successful cockpit run.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DEALS = (
    "datalink", "kraton", "mac-gray", "penford", "petsmart",
    "providence-worcester", "stec", "synacor",
)
NAMES = {"mac-gray": "Mac-Gray", "petsmart": "PetSmart", "stec": "sTec",
         "providence-worcester": "Providence & Worcester"}


class CatalogError(RuntimeError):
    pass


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def manifest(root: Path) -> dict[str, dict[str, str]]:
    path = root / "raw_filing/MANIFEST.csv"
    with path.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    found = {row["deal"]: row for row in rows}
    if len(found) != len(rows) or set(found) != set(DEALS):
        raise CatalogError("filing manifest must contain exactly the catalog deals")
    for slug, row in found.items():
        filename = row.get("file", "")
        if not filename or Path(filename).name != filename or ".." in filename:
            raise CatalogError(f"unsafe filing filename for {slug}")
        filing = root / "raw_filing" / filename
        if not filing.is_file() or sha256(filing) != row.get("sha256"):
            raise CatalogError(f"filing is missing or differs from its manifest hash: {slug}")
        if not all(row.get(field) for field in ("form_type", "date_filed", "source_url")):
            raise CatalogError(f"filing metadata is incomplete: {slug}")
    return found


def build_catalog(root: Path) -> dict:
    filings = manifest(root)
    return {"schema_version": 1, "deals": {
        slug: {"name": NAMES.get(slug, slug.title()), "filing": filings[slug],
               "versions": [], "findings": [], "documents": []}
        for slug in DEALS}}


def atomic_json(path: Path, value: dict) -> None:
    """Create a new file without replacing an existing catalog or another writer's result."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    try:
        os.link(temporary, path)
    finally:
        temporary.unlink()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path, help="new catalog path; the existing catalog is never replaced")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    output = args.output or root / "_dev/cockpit/catalog.json"
    atomic_json(output, build_catalog(root))
    print(f"Created pending catalog for {len(DEALS)} deals at {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
