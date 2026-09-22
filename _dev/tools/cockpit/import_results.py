"""Import the current extractions and deal-level review records into the cockpit.

The catalog holds one version per deal: the Claude Opus 5.5 medium extraction in
extraction/<deal>.xlsx, confirmed from its preserved run receipts. Earlier
workbooks and their row-keyed findings stay in their _dev/reviews/ packets.
This tool reads evidence only, refuses an incomplete or inconsistent nine-deal
set, and writes the catalog atomically. It never changes source workbooks.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import sys

import openpyxl

ROOT = Path(__file__).resolve().parents[3]
DEALS = (
    "datalink", "kraton", "mac-gray", "meredith", "penford", "petsmart",
    "providence-worcester", "stec", "synacor",
)
NAMES = {"mac-gray": "Mac-Gray", "petsmart": "PetSmart", "stec": "sTec",
         "providence-worcester": "Providence & Worcester"}
DATA = "_dev/reviews/2026-09-21-datalink-pilot"
MAC_ACCEPTANCE = "_dev/reviews/2026-09-21-mac-gray-pilot/acceptance"
REEXTRACT = "_dev/reviews/2026-09-22-opus55-reextraction"
INSTRUCTION_HASH = "513c8e3e8159e4a6bceccd6ffca32a246302736329a0c7137b64dd3b7ffcd304"
SHEETS = ["Deal ledger", "Rounds", "Questions", "Deal facts"]
OPUS55_MODEL = "claude-opus-5-5"
OPUS55_EFFORT = "medium"
VERSION_ID = "opus55-medium"


class ImportErrorEvidence(RuntimeError):
    pass


def read_json(root: Path, path: str) -> dict:
    return json.loads((root / path).read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for part in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(part)
    return h.hexdigest()


def checked_path(root: Path, relative: str) -> Path:
    if not relative or Path(relative).is_absolute() or ".." in Path(relative).parts:
        raise ImportErrorEvidence(f"Unsafe catalog path: {relative}")
    try:
        path = (root / relative).resolve(strict=True)
    except FileNotFoundError as exc:
        raise ImportErrorEvidence(f"Missing catalog path: {relative}") from exc
    if not path.is_relative_to(root.resolve()) or "ref" in path.relative_to(root.resolve()).parts:
        raise ImportErrorEvidence(f"Forbidden catalog path: {relative}")
    if not path.is_file():
        raise ImportErrorEvidence(f"Catalog path is not a file: {relative}")
    return path


def workbook(root: Path, relative: str, expected: str | None = None) -> str:
    path = checked_path(root, relative)
    digest = sha256(path)
    if expected and digest != expected:
        raise ImportErrorEvidence(f"Hash mismatch: {relative}")
    try:
        book = openpyxl.load_workbook(path, read_only=True, data_only=False)
        try:
            if book.sheetnames != SHEETS:
                raise ImportErrorEvidence(f"Workbook sheets differ: {relative}")
        finally:
            book.close()
    except Exception as exc:
        if isinstance(exc, ImportErrorEvidence):
            raise
        raise ImportErrorEvidence(f"Unreadable workbook: {relative}: {exc}") from exc
    return digest


def document(root: Path, id: str, label: str, source: str | None, kind: str, path: str) -> dict:
    checked_path(root, path)
    return dict(id=id, label=label, source_version=source, kind=kind, path=path)


def finding(id: str, title: str, detail: str, rule: str, source: str | None,
            label: str, rows: list, evidence: list, proposed: str,
            note: str, *, needs_recheck: bool = False,
            judgment: str = "unreviewed", actor: str = "", at: str = "") -> dict:
    return dict(id=id, title=title, detail=detail, rule=rule,
                source_version=source, source_label=label, source_rows=rows,
                evidence=evidence, proposed_change=proposed,
                needs_recheck=needs_recheck, judgment=judgment,
                implementation="unassessed", verification="unchecked",
                note=note, actor=actor, at=at)


def deal_records(root: Path, deal: str) -> tuple[list[dict], list[dict]]:
    """Case-level decisions that concern the filing, not any workbook's rows.

    They carry no source version: they were made while reviewing earlier drafts
    but apply to whichever extraction is displayed. Row-keyed audit findings,
    corrections and reports for those drafts remain only in their packets.
    """
    if deal == "datalink":
        adjudication = f"{DATA}/ADJUDICATION.md"
        checked_path(root, adjudication)
        ruling = finding(
            "datalink-f9", "Austin's ruling: January bilateral stage is round 1",
            "A 21 September audit of an earlier Datalink draft asked whether E6's ordering puts round 1 at "
            "the June 6 outreach, leaving Party A's pre-June activity in a round 0. Austin ruled to retain January's bilateral stage as round 1 and June's broad outreach "
            "as round 2, with five rounds overall. January 29 remains an inferred opening date. "
            "The adjudication calls this a case-level mapping decision, not an instruction change.",
            "E6", None, "Datalink case-level decision (21 September review)", [],
            [{"quote": "determined that our management should continue to pursue the opportunity with Party A",
              "page": "27"},
             {"quote": "As we requested in mid-March 2016", "page": "27"}],
            "Check the displayed extraction's round map against this ruling.",
            f"The ruling and its reasoning are in {adjudication}. The earlier draft's audit findings and "
            "lead-verified corrections referred to that draft's rows and remain in the Datalink pilot packet.",
            needs_recheck=True)
        ruling["recorded_decision"] = {
            "actor": "Austin Li", "at": "2026-09-21",
            "decision": "Retain January's bilateral stage as round 1 and June's broad outreach as round 2; keep five rounds. January 29 remains inferred.",
            "source_document": adjudication,
        }
        return [ruling], []
    if deal == "mac-gray":
        r01 = finding(
            "mac-gray-r01", "R01 decided: bidder-commitment changes as same-price bids",
            "Whether termination-fee and sponsor-guarantee changes communicated at an unchanged price receive "
            "separate same-price Bid events or remain dated terms in Notes. Austin decided by whether the term "
            "changes the bidder's ability to walk away.",
            "E2; E10", None, "Mac-Gray research decision (22 September)", [], [],
            "Check the displayed extraction against the decision: the September 21-23 final package and the "
            "October 5 and October 8 sponsor-liability proposals are same-price Bids; the October 7 and "
            "October 11 target-fee terms stay in dated Notes.",
            "The research-decision document sets out each change by filing page. The earlier candidate's other "
            "findings and corrections referred to its rows and remain in the Mac-Gray pilot packet.",
            needs_recheck=True)
        r01["recorded_decision"] = {
            "actor": "Austin Li", "at": "2026-09-22",
            "decision": "Bidder-commitment changes (reverse termination fee, sponsor damages cap or guarantee, "
                        "adding or dropping a financing or closing condition) are same-price Bids carrying the "
                        "standing price; the target termination fee stays in a dated Note; target requirements "
                        "on the bidder's commitment are Other material event.",
            "source_document": f"{MAC_ACCEPTANCE}/RESEARCH_DECISION.md",
        }
        docs = [document(root, "mac-gray-r01", "R01 research decision", None,
                         "research_decision", f"{MAC_ACCEPTANCE}/RESEARCH_DECISION.md")]
        return [r01], docs
    return [], []


def read_manifest(root: Path) -> dict:
    with (root / "raw_filing/MANIFEST.csv").open(newline="", encoding="utf-8") as stream:
        manifest = {row["deal"]: row for row in csv.DictReader(stream)}
    if set(manifest) != set(DEALS):
        raise ImportErrorEvidence("Filing manifest does not contain exactly nine deals")
    for deal, row in manifest.items():
        if sha256(checked_path(root, f"raw_filing/{row['file']}")) != row["sha256"]:
            raise ImportErrorEvidence(f"Filing hash differs from manifest: {deal}")
    return manifest


def verify_reextraction(root: Path, manifest: dict) -> dict:
    """Confirm the nine Opus 5.5 medium re-extractions now in extraction/ from their receipts."""
    summary = read_json(root, f"{REEXTRACT}/reextraction.json")
    if (summary.get("model") != OPUS55_MODEL or summary.get("effort") != OPUS55_EFFORT
            or summary.get("instruction_sha256") != INSTRUCTION_HASH
            or set(summary.get("deals", {})) != set(DEALS)):
        raise ImportErrorEvidence("Re-extraction summary is incomplete or differs")
    result = {}
    for deal in DEALS:
        entry = summary["deals"][deal]
        folder = f"{REEXTRACT}/receipts/{deal}"
        metadata = read_json(root, f"{folder}/metadata.json")
        status = read_json(root, f"{folder}/status.json")
        check = read_json(root, f"{folder}/check.json")
        results = json.loads((root / folder / "provider-results.json").read_text(encoding="utf-8"))
        read_json(root, f"{folder}/command.json")
        if any((metadata.get("mode") != "extract", metadata.get("provider") != "opus",
                metadata.get("model") != OPUS55_MODEL, metadata.get("effort") != OPUS55_EFFORT,
                metadata.get("instruction_sha256") != INSTRUCTION_HASH,
                metadata.get("filing_name") != manifest[deal]["file"],
                metadata.get("filing_sha256") != manifest[deal]["sha256"])):
            raise ImportErrorEvidence(f"Re-extraction prepared inputs differ: {deal}")
        if (status.get("state") != "completed" or status.get("exit_code") != 0
                or status.get("provider", {}).get("served_models") != [OPUS55_MODEL]):
            raise ImportErrorEvidence(f"Re-extraction did not complete successfully: {deal}")
        if not any(r.get("subtype") == "success" and not r.get("is_error")
                   and OPUS55_MODEL in r.get("modelUsage", {}) for r in results):
            raise ImportErrorEvidence(f"Re-extraction success/model evidence missing: {deal}")
        if not isinstance(check.get("summary"), dict) or check["summary"] != entry.get("check_summary"):
            raise ImportErrorEvidence(f"Re-extraction checker receipt differs: {deal}")
        digest = workbook(root, f"extraction/{deal}.xlsx", entry.get("new_sha256"))
        result[deal] = dict(workbook_sha256=digest, previous_sha256=entry.get("old_sha256"),
                            checker_summary=check["summary"],
                            reported_cost_usd=status.get("usage", {}).get("cost_usd"),
                            continuations=status.get("continuations"))
    return result


def build_catalog(root: Path) -> tuple[dict, dict]:
    opus55 = verify_reextraction(root, read_manifest(root))
    catalog = {"schema_version": 1, "deals": {}}
    for deal in DEALS:
        current = dict(id=VERSION_ID, label="Opus 5.5 medium extraction",
                       path=f"extraction/{deal}.xlsx", sha256=opus55[deal]["workbook_sha256"],
                       instruction_version="v1.13.2", kind="raw",
                       review_status="unreviewed; Austin review pending")
        findings, documents = deal_records(root, deal)
        catalog["deals"][deal] = dict(name=NAMES.get(deal, deal.title()), default_base=VERSION_ID,
                                      versions=[current], findings=findings, documents=documents)
    return catalog, {"opus55_medium": opus55}


def atomic_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    catalog, provenance = build_catalog(root)
    output = args.output or root / "_dev/cockpit/catalog.json"
    if output == root / "_dev/cockpit/catalog.json":
        atomic_json(root / REEXTRACT / "import-verification.json", provenance)
    atomic_json(output, catalog)
    print(f"Imported {len(catalog['deals'])} deals to {output}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ImportErrorEvidence as exc:
        print(f"Import refused: {exc}", file=sys.stderr)
        raise SystemExit(2)
