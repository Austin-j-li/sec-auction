"""Import preserved extraction results and prior review records into the cockpit.

This tool reads evidence only. It refuses a partial or inconsistent nine-deal
batch and writes the catalog atomically. It never changes source workbooks.
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
NEW_DEALS = tuple(d for d in DEALS if d not in {"datalink", "mac-gray"})
REVIEW = "_dev/reviews/2026-09-21-v1132-cockpit"
MAC = "_dev/reviews/2026-09-21-mac-gray-pilot"
MAC_ACCEPTANCE = f"{MAC}/acceptance"
DATA = "_dev/reviews/2026-09-21-datalink-pilot"
INSTRUCTION_HASH = "513c8e3e8159e4a6bceccd6ffca32a246302736329a0c7137b64dd3b7ffcd304"
SHEETS = ["Deal ledger", "Rounds", "Questions", "Deal facts"]


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


def version(id: str, label: str, path: str, digest: str, instruction: str,
            kind: str, status: str) -> dict:
    return dict(id=id, label=label, path=path, sha256=digest,
                instruction_version=instruction, kind=kind,
                review_status=status)


def document(root: Path, id: str, label: str, source: str, kind: str, path: str) -> dict:
    checked_path(root, path)
    return dict(id=id, label=label, source_version=source, kind=kind, path=path)


def finding(id: str, title: str, detail: str, rule: str, source: str,
            label: str, rows: list, evidence: list, proposed: str,
            note: str, *, needs_recheck: bool = False,
            judgment: str = "unreviewed", actor: str = "", at: str = "") -> dict:
    return dict(id=id, title=title, detail=detail, rule=rule,
                source_version=source, source_label=label, source_rows=rows,
                evidence=evidence, proposed_change=proposed,
                needs_recheck=needs_recheck, judgment=judgment,
                implementation="unassessed", verification="unchecked",
                note=note, actor=actor, at=at)


def recorded_correction(version: str, scope: str, source_document: str) -> dict:
    return {"version": version, "scope": scope, "status": "lead_verified",
            "actor": "Codex development lead", "source_document": source_document}


def datalink_findings(root: Path) -> list[dict]:
    raw = read_json(root, f"{DATA}/fresh_findings.json")
    assessments = {
        "F1": "Development lead assessed this as supported for correction.",
        "F2": "Development lead assessed type and timing split as supported; price placement was narrowed in adjudication.",
        "F3": "Development lead assessed the dated NDA omission as supported.",
        "F4": "Development lead assessed the hindsight-based Conditions label as unsupported.",
        "F5": "Development lead assessed the cash inference as unsupported.",
        "F6": "Development lead supported a clearer round summary but rejected an extra event.",
        "F7": "Development lead assessed the unchanged confirmations as unsupported new Bid rows.",
        "F8": "Development lead rejected the proposed earlier exits as corrections.",
        "F9": "Austin ruled on 2026-09-21 to retain January as round 1 and June as round 2; January 29 remains inferred.",
        "F10": "Development lead assessed the material new closing conditions as supported.",
        "F11": "Development lead found no required separate projections event.",
    }
    corrected = {
        "F1": "Exact non-submitter Counts replaced with qualified ranges; linked summaries revised.",
        "F2": "Known strategic and financial IOI cohorts split; combined price range retained only in Notes.",
        "F3": "Insight's dated June 14 NDA added from Annex A.",
        "F4": "November Conditions changed to Unclear; September Conditions remain qualified interpretations.",
        "F5": "November 2 All cash changed to Not stated; signed consideration remains separately recorded.",
        "F6": "Round 2 summary clarified as nine new IOIs plus Party A's standing offer; no duplicate July bid added.",
        "F7": "Duplicate unchanged-confirmation Bid rows removed while reported confirmations stay in Notes.",
        "F9": "Q1 records Austin's retained five-round ruling; January opening remains inferred.",
        "F10": "A separate September 26 bid records newly proposed closing conditions; its cross-page quotation has a documented checker exception.",
    }
    result = []
    for item in raw["findings"]:
        fid = item["id"]
        entry = finding(
            f"datalink-audit-{fid.lower()}", f"Audit {fid}: {item['claim'][:100]}",
            item["claim"], "; ".join(item.get("rules", [])), "v1132-raw",
            "Datalink v1.13.2 raw audit", item.get("affected_rows", []),
            item.get("evidence", []), item.get("proposed_correction", ""),
            assessments[fid] + " See the original audit and adjudication documents. "
            "Other lead assessments are not Austin acceptance.",
            needs_recheck=True,
        )
        if fid == "F9":
            entry["recorded_decision"] = {
                "actor": "Austin Li", "at": "2026-09-21",
                "decision": "Retain January's bilateral stage as round 1 and June's broad outreach as round 2; keep five rounds. January 29 remains inferred.",
                "source_document": "datalink-adjudication",
            }
        if fid in corrected:
            entry["recorded_correction"] = recorded_correction(
                "datalink-verified", corrected[fid], "datalink-verification")
        result.append(entry)
    lead_l1 = finding("datalink-lead-l1", "Lead L1: separate requested exclusivity event",
            "The lead source inventory found the requested 30-day exclusivity period recorded only in a Note in the raw draft. The later controlled revision records the request separately.",
            "E2", "v1132-raw", "Datalink source-first lead assessment", [], [],
            "See the separate request representation and its bounded date in the verified revision.",
            "Development lead assessment from ADJUDICATION.md, not an Austin-adopted finding. The revised workbook's correction was lead-verified within the documented scope.",
            needs_recheck=True)
    lead_l1["recorded_correction"] = recorded_correction(
        "datalink-verified", "Requested exclusivity event added with no lower date bound or rival exit.",
        "datalink-verification")
    mechanical_m1 = finding("datalink-mechanical-m1", "Mechanical M1: round-opening row order",
            "The raw checker reported a round-opening order error. The verified revision reorders the same-day opening before events assigned to that round.",
            "E6", "v1132-raw", "Datalink checker and lead adjudication", [], [],
            "Keep January as round 1 under Austin's recorded F9 decision; check row ordering.",
            "Mechanical finding, not a substantive certification. The original checker report and revision verification remain available.",
            needs_recheck=True)
    mechanical_m1["recorded_correction"] = recorded_correction(
        "datalink-verified", "Same-day round opening moved before assigned events; round boundary unchanged.",
        "datalink-verification")
    result.extend([lead_l1, mechanical_m1])
    return result


def mac_findings(root: Path) -> list[dict]:
    raw = read_json(root, f"{MAC}/audit/findings.json")
    assessments = {
        "F01": "Development lead supported a correction to Q9's counterfactual.",
        "F02": "Development lead identified a genuine economic-terms boundary for Austin.",
        "F03": "Development lead called this a representation judgment, not a confirmed omission.",
        "F04": "Development lead called this a classification judgment.",
        "F05": "Development lead did not accept this as stated; the separate cohort timing concern appears in the adjudication.",
        "F06": "Development lead supported only a quotation correction.",
        "F07": "Development lead supported a quotation correction.",
        "F08": "Development lead supported a precision correction.",
        "F09": "Development lead rejected this false blank-cell claim.",
        "F10": "Development lead supported a narrow chronology correction.",
    }
    corrected = {
        "F01": "Q9 alternative-formality counterfactual corrected; no new reaffirmation under retained Formal classification.",
        "F06": "April adviser quotation replaced; adviser events retained.",
        "F07": "Rollover-permission quotation replaced with clause supporting target authorization.",
        "F08": "Outreach timing wording corrected without an invented July endpoint.",
        "F10": "July 25 oral and later written bid sequence clarified; both bids retained.",
    }
    result = []
    for item in raw["findings"]:
        fid = item["id"]
        entry = finding(
            f"mac-gray-audit-{fid.lower()}", f"Audit {fid}: {item['problem'][:100]}",
            item["problem"], item.get("rule", ""), "v1132-raw",
            "Mac-Gray v1.13.2 raw audit", item.get("affected_rows", []),
            [{"quote": item["quote"], "page": item["page"]}] if item.get("quote") else [],
            item.get("proposed_correction", ""),
            assessments[fid] + " A separate verified revision addresses accepted corrections within its documented scope; this finding remains sourced to the raw draft. Human review is pending. See original adjudication and verification.",
            needs_recheck=True,
        )
        if fid in corrected:
            entry["recorded_correction"] = recorded_correction(
                "mac-gray-verified", corrected[fid], "mac-gray-verification")
        result.append(entry)
    for id, title, detail, rule, proposed in (
        ("L01", "Anonymous cohort timing", "The lead assessment found that the raw draft closes all sixteen anonymous financial NDA signers by July 23 without evidence they were all eligible then.", "B; E3; E8; E14", "Preserve the eventual total but represent first-round eligibility and individual exit timing as uncertain."),
        ("L03", "September 27 voting agreements", "The lead assessment found a separately dated shareholder-support event missing from the raw ledger.", "E2; D2", "Record the dated execution separately from the later signing effect."),
        ("L04", "Party B option terms", "The lead assessment found material option-package terms missing from the raw Note.", "D1; E13", "Restore the stated strike, vesting, equity share and valuation limits."),
        ("L05", "Exclusivity extension request", "The lead assessment found the request to extend exclusivity folded into later execution in the raw draft.", "D2; E2; E8", "Represent the bounded-date request separately from execution."),
    ):
        entry = finding(
            f"mac-gray-lead-{id.lower()}", f"Lead {id}: {title}", detail, rule,
            "v1132-raw", "Mac-Gray lead adjudication", [], [], proposed,
            "Development lead assessment from ADJUDICATION.md. The separate final revision reports this correction as lead-verified; human review remains pending.",
            needs_recheck=True,
        )
        entry["recorded_correction"] = recorded_correction(
            "mac-gray-verified", f"{proposed} Final revision reports this task implemented.",
            "mac-gray-verification")
        result.append(entry)
    return result


def verify_batch(root: Path, protected: dict, manifest: dict) -> dict:
    batch = read_json(root, f"{REVIEW}/batch.json")
    if batch.get("state") != "completed" or set(batch.get("runs", {})) != set(NEW_DEALS):
        raise ImportErrorEvidence("Seven-deal batch is incomplete")
    if batch.get("instruction_sha256") != INSTRUCTION_HASH or batch.get("model") != "claude-opus-5" or batch.get("effort") != "high":
        raise ImportErrorEvidence("Batch instruction/model/effort differs")
    receipts = {}
    for deal in NEW_DEALS:
        entry = batch["runs"][deal]
        receipt = read_json(root, f"{REVIEW}/receipts/{deal}/receipt.json")
        metadata = read_json(root, f"{REVIEW}/receipts/{deal}/metadata.json")
        status = read_json(root, f"{REVIEW}/receipts/{deal}/status.json")
        validation = read_json(root, f"{REVIEW}/receipts/{deal}/validation.json")
        results = json.loads((root / REVIEW / "receipts" / deal / "provider-results.json").read_text())
        if entry.get("state") != "completed" or receipt.get("state") != "completed" or status.get("state") != "completed" or status.get("exit_code") != 0:
            raise ImportErrorEvidence(f"Provider did not complete successfully: {deal}")
        if metadata.get("model") != "claude-opus-5" or metadata.get("effort") != "high":
            raise ImportErrorEvidence(f"Prepared model/effort differs: {deal}")
        if not results or not any(
            r.get("subtype") == "success" and not r.get("is_error")
            and "claude-opus-5" in r.get("modelUsage", {})
            for r in results
        ):
            raise ImportErrorEvidence(f"Provider success/model evidence missing: {deal}")
        if not validation.get("valid_xlsx"):
            raise ImportErrorEvidence(f"Output validation failed: {deal}")
        for key, expected in (("instruction_sha256", INSTRUCTION_HASH),
                              ("filing_sha256", protected[f"raw_filing/{manifest[deal]['file']}"])):
            if metadata.get(key) != expected:
                raise ImportErrorEvidence(f"Prepared {key} mismatch: {deal}")
        bookpath = f"{REVIEW}/raw/extraction/{deal}.xlsx"
        digest = workbook(root, bookpath, receipt.get("workbook_sha256"))
        if digest != validation.get("sha256"):
            raise ImportErrorEvidence(f"Prepared output hash differs: {deal}")
        check = read_json(root, f"{REVIEW}/checks/{deal}.json")
        if not isinstance(check.get("summary"), dict):
            raise ImportErrorEvidence(f"Separate checker report missing: {deal}")
        if check["summary"] != receipt.get("check_summary"):
            raise ImportErrorEvidence(f"Checker receipt differs: {deal}")
        receipts[deal] = dict(workbook_sha256=digest, provider_state=status["state"],
                              checker_summary=check["summary"],
                              reported_cost_usd=status.get("usage", {}).get("cost_usd"),
                              model_seconds=status.get("elapsed_seconds"),
                              source_sha256=protected[f"raw_filing/{manifest[deal]['file']}"])
    return receipts


def verify_reused(root: Path, protected: dict, manifest: dict) -> dict:
    """Confirm the two reused raw runs from their original provider receipts."""
    result = {}
    data = read_json(root, f"{DATA}/provenance.json")
    data_run = data["runs"]["extraction"]
    mac_meta = read_json(root, f"{MAC}/provenance/extraction/metadata.json")
    mac_status = read_json(root, f"{MAC}/provenance/extraction/status.json")
    mac_provider = read_json(root, f"{MAC}/provenance/extraction/provider-summary.json")
    mac_validation = read_json(root, f"{MAC}/provenance/extraction/validation.json")
    for deal, metadata, status, provider, validation, raw in (
        ("datalink", data_run["metadata"], data_run["status"], data_run["provider_result"],
         data_run["validation"], "extraction/datalink.xlsx"),
        ("mac-gray", mac_meta, mac_status, mac_provider["result"], mac_validation,
         f"{MAC}/raw/extraction/mac-gray.xlsx"),
    ):
        source_hash = protected[f"raw_filing/{manifest[deal]['file']}"]
        if any((metadata.get("mode") != "extract", metadata.get("model") != "claude-opus-5",
                metadata.get("effort") != "high", metadata.get("instruction_sha256") != INSTRUCTION_HASH,
                metadata.get("filing_sha256") != source_hash,
                metadata.get("filing_name") != manifest[deal]["file"],
                status.get("state") != "completed", status.get("exit_code") != 0,
                provider.get("subtype") != "success", provider.get("is_error") is not False,
                "claude-opus-5" not in provider.get("modelUsage", {}),
                validation.get("valid_xlsx") is not True)):
            raise ImportErrorEvidence(f"Reused raw provenance differs: {deal}")
        digest = workbook(root, raw, validation.get("sha256"))
        if deal == "datalink" and digest != protected[raw]:
            raise ImportErrorEvidence("Datalink protected raw hash differs")
        result[deal] = dict(workbook_sha256=digest, source_sha256=source_hash,
                            instruction_sha256=INSTRUCTION_HASH, model="claude-opus-5",
                            effort="high", provider_success=True)
    if data.get("raw_workbook_sha256") != result["datalink"]["workbook_sha256"]:
        raise ImportErrorEvidence("Datalink provenance output hash differs")
    if mac_provider.get("raw_workbook_sha256") != result["mac-gray"]["workbook_sha256"]:
        raise ImportErrorEvidence("Mac-Gray provenance output hash differs")
    return result


def verify_mac_candidate(root: Path, manifest: dict, preceding_sha256: str) -> dict:
    """Check the completed acceptance-correction packet without deciding R01."""
    folder = root / MAC_ACCEPTANCE
    status = read_json(root, f"{MAC_ACCEPTANCE}/acceptance-status.json")
    evidence = read_json(root, f"{MAC_ACCEPTANCE}/EVIDENCE_MANIFEST.json")
    comparison = read_json(root, f"{MAC_ACCEPTANCE}/verification/comparison.json")
    protected = read_json(root, f"{MAC_ACCEPTANCE}/verification/protected-inputs.json")
    metadata = read_json(root, f"{MAC_ACCEPTANCE}/provenance/metadata.json")
    provider_status = read_json(root, f"{MAC_ACCEPTANCE}/provenance/status.json")
    provider = read_json(root, f"{MAC_ACCEPTANCE}/provenance/provider-summary.json")["result"]
    validation = read_json(root, f"{MAC_ACCEPTANCE}/provenance/validation.json")
    mechanical = read_json(root, f"{MAC_ACCEPTANCE}/mechanical-check.json")
    if (status.get("status") != "research_decision_pending" or status.get("accepted") is not False
            or status.get("frozen_for_research") is not False
            or not any("R01" in str(x) for x in status.get("pending_research_decisions", []))
            or status.get("known_supported_corrections_unapplied") != []):
        raise ImportErrorEvidence("Mac-Gray acceptance status does not support candidate label")
    if evidence.get("snapshot_status") != "review_complete_supported_corrections_verified_R01_pending":
        raise ImportErrorEvidence("Mac-Gray evidence snapshot status differs")
    for item in evidence.get("files", []):
        path = checked_path(root, f"{MAC_ACCEPTANCE}/{item['path']}")
        if path.stat().st_size != item["bytes"] or sha256(path) != item["sha256"]:
            raise ImportErrorEvidence(f"Mac-Gray acceptance artifact differs: {item['path']}")
    for relative, item in protected.items():
        if not item.get("unchanged") or item.get("actual") != item.get("expected") or sha256(checked_path(root, relative)) != item["expected"]:
            raise ImportErrorEvidence(f"Mac-Gray acceptance protected input differs: {relative}")
    if (metadata.get("mode") != "revise" or metadata.get("model") != "claude-opus-5"
            or metadata.get("effort") != "high" or metadata.get("instruction_sha256") != INSTRUCTION_HASH
            or metadata.get("filing_sha256") != manifest["mac-gray"]["sha256"]
            or metadata.get("revised_from_sha256") != preceding_sha256
            or metadata.get("report_sha256") != sha256(folder / "ACCEPTED_CORRECTIONS.md")
            or provider_status.get("state") != "completed" or provider_status.get("exit_code") != 0
            or provider.get("subtype") != "success" or provider.get("is_error") is not False
            or "claude-opus-5" not in provider.get("modelUsage", {})):
        raise ImportErrorEvidence("Mac-Gray acceptance provider provenance differs")
    candidate_path = f"{MAC_ACCEPTANCE}/extraction/mac-gray.xlsx"
    digest = workbook(root, candidate_path, validation.get("sha256"))
    if (digest != status.get("candidate_sha256") or digest != comparison.get("after_sha256")
            or comparison.get("before_sha256") != preceding_sha256
            or comparison.get("unexpected_content_or_control_changes") != []
            or comparison.get("R01") != "not decided; no economic-term bids added"):
        raise ImportErrorEvidence("Mac-Gray candidate comparison or hash differs")
    if (mechanical.get("summary", {}).get("errors") != status.get("mechanical_errors")
            or mechanical.get("summary", {}).get("warnings") != status.get("mechanical_warnings")
            or status.get("events") != 58 or status.get("bid_rows") != 13
            or status.get("rounds") != 3 or status.get("questions") != 9):
        raise ImportErrorEvidence("Mac-Gray candidate structure or checker status differs")
    return {"workbook_sha256": digest, "previous_revision_sha256": preceding_sha256,
            "status": status["status"], "r01_pending": True,
            "provider_model": "claude-opus-5", "effort": "high",
            "checker_summary": mechanical["summary"],
            "evidence_files_hash_verified": len(evidence["files"]),
            "protected_inputs_hash_verified": len(protected)}


def build_catalog(root: Path) -> tuple[dict, dict]:
    protected = read_json(root, f"{REVIEW}/protected-inputs.json")["sha256"]
    for relative, digest in protected.items():
        if sha256(checked_path(root, relative)) != digest:
            raise ImportErrorEvidence(f"Protected input changed: {relative}")
    if protected["SEC_Deal_Ledger_Extraction_Instruction.md"] != INSTRUCTION_HASH:
        raise ImportErrorEvidence("Frozen instruction hash differs")
    with (root / "raw_filing/MANIFEST.csv").open(newline="", encoding="utf-8") as stream:
        manifest = {row["deal"]: row for row in csv.DictReader(stream)}
    if set(manifest) != set(DEALS):
        raise ImportErrorEvidence("Filing manifest does not contain exactly nine deals")
    for deal, row in manifest.items():
        if protected[f"raw_filing/{row['file']}"] != row["sha256"]:
            raise ImportErrorEvidence(f"Manifest source hash mismatch: {deal}")
    receipts = verify_batch(root, protected, manifest)
    reused = verify_reused(root, protected, manifest)
    catalog = {"schema_version": 1, "deals": {}}
    mac_candidate = None
    for deal in DEALS:
        name = {"mac-gray": "Mac-Gray", "petsmart": "PetSmart", "stec": "sTec",
                "providence-worcester": "Providence & Worcester"}.get(deal, deal.title())
        if deal == "datalink":
            raw_path = "extraction/datalink.xlsx"
            raw_status = "lead_reviewed; human review pending"
        elif deal == "mac-gray":
            raw_path = f"{MAC}/raw/extraction/mac-gray.xlsx"
            raw_status = "lead_reviewed; human review pending"
        else:
            raw_path = f"{REVIEW}/raw/extraction/{deal}.xlsx"
            raw_status = "unreviewed; Austin review pending"
        raw_hash = workbook(root, raw_path)
        if deal == "datalink" and raw_hash != protected["extraction/datalink.xlsx"]:
            raise ImportErrorEvidence("Datalink reused raw hash differs")
        if deal == "mac-gray":
            mac_record = read_json(root, f"{MAC}/provenance/extraction/validation.json")
            if raw_hash != mac_record.get("sha256"):
                raise ImportErrorEvidence("Mac-Gray reused raw hash differs")
        if deal in NEW_DEALS and raw_hash != receipts[deal]["workbook_sha256"]:
            raise ImportErrorEvidence(f"New raw hash differs: {deal}")
        versions = [version("v1132-raw", "v1.13.2 raw", raw_path, raw_hash,
                            "v1.13.2", "raw", raw_status)]
        if deal != "datalink":
            prior = f"extraction/{deal}.xlsx"
            digest = workbook(root, prior, protected[prior])
            versions.append(version("v113-baseline", "v1.13 original baseline", prior, digest,
                                    "v1.13", "raw", "historical original; human review pending"))
        docs = []
        findings = []
        default = "v1132-raw"
        if deal == "datalink":
            verified_path = f"{DATA}/revision/datalink_revised.xlsx"
            verification_doc = f"{DATA}/revision/VERIFICATION.md"
            verified_hash = read_json(root, f"{DATA}/revision/post_hashes.json").get("revised_workbook_sha256")
            verified_report = (root / verification_doc).read_text(encoding="utf-8")
            if "accepted corrections implemented" not in verified_report.lower() or not verified_hash:
                raise ImportErrorEvidence("Datalink final verification evidence absent")
            rev_hash = workbook(root, verified_path, verified_hash)
            structural = read_json(root, f"{DATA}/revision/structural_verification.json")
            references = read_json(root, f"{DATA}/revision/reference_audit.json")
            if not structural.get("four_sheets_in_required_order") or not references.get("all_targets_exist") or not references.get("question_flags_bidirectional_match"):
                raise ImportErrorEvidence("Datalink structural verification incomplete")
            versions.append(version("datalink-verified", "Verified correction pass (lead)",
                                    verified_path, rev_hash, "v1.13.2", "revision",
                                    "lead-verified corrections; 1 documented checker quotation exception; human review pending"))
            default = "datalink-verified"
            findings = datalink_findings(root)
            docs = [
                document(root, "datalink-audit", "Fresh independent audit", "v1132-raw", "review", f"{DATA}/fresh_review.md"),
                document(root, "datalink-adjudication", "Lead adjudication and Austin F9 ruling", "v1132-raw", "adjudication", f"{DATA}/ADJUDICATION.md"),
                document(root, "datalink-inventory", "Source-first inventory comparison", "v1132-raw", "inventory", f"{DATA}/inventory_comparison.md"),
                document(root, "datalink-correction-brief", "Accepted correction brief for controlled revision", "v1132-raw", "correction_brief", f"{DATA}/revision/CORRECTION_BRIEF.md"),
                document(root, "datalink-verification", "Verified correction pass and checker exception", "datalink-verified", "verification", verification_doc),
                document(root, "datalink-inventory-verification", "Frozen inventory revisit", "datalink-verified", "inventory", f"{DATA}/revision/INVENTORY_VERIFICATION.md"),
            ]
        elif deal == "mac-gray":
            revised = f"{MAC}/revision/extraction/mac-gray.xlsx"
            final = read_json(root, f"{MAC}/revision/verification/final-checks.json")
            if not final or not (root / MAC / "revision/VERIFICATION.md").exists():
                raise ImportErrorEvidence("Mac-Gray final verification absent")
            rev_hash = workbook(root, revised, "f54295a242057b0e6f72fddf9555d6b4c007eea10c9fc13b1202b659439e112e")
            if final.get("final_workbook_sha256") != rev_hash or not final.get("all_protected_inputs_unchanged") or not final.get("no_unexpected_cell_changes_remain"):
                raise ImportErrorEvidence("Mac-Gray final verification differs")
            versions.append(version("mac-gray-verified", "Verified correction pass (lead)", revised, rev_hash,
                                    "v1.13.2", "revision", "lead-verified corrections; human review pending"))
            mac_candidate = verify_mac_candidate(root, manifest, rev_hash)
            candidate_path = f"{MAC_ACCEPTANCE}/extraction/mac-gray.xlsx"
            versions.append(version("mac-gray-candidate", "Latest correction candidate (R01 pending)",
                                    candidate_path, mac_candidate["workbook_sha256"],
                                    "v1.13.2", "revision",
                                    "source review and supported corrections verified; R01 pending; not research-ready"))
            default = "mac-gray-candidate"
            findings = mac_findings(root)
            findings.append(finding(
                "mac-gray-r01", "R01: fee and guarantee changes as same-price bids",
                "The acceptance review leaves a consequential convention decision open: whether material termination-fee and guarantee changes communicated by bidders receive separate same-price Bid events, or remain dated terms in existing Notes. The current candidate retains 13 Bid rows; no R01 choice was applied.",
                "E2; E10", "mac-gray-candidate",
                "Mac-Gray acceptance candidate: R01 pending", [], [],
                "Austin's decision is required before any R01 correction pass or research freeze. See the research-decision document for both treatments.",
                "The acceptance packet explicitly states that R01 was excluded from the verified A01–A11 correction pass. This is a pending research choice, not an accepted correction.",
                needs_recheck=True,
            ))
            docs = [
                document(root, "mac-gray-pilot-report", "Pilot report and provenance", "v1132-raw", "report", f"{MAC}/REPORT.md"),
                document(root, "mac-gray-audit", "Fresh independent audit", "v1132-raw", "review", f"{MAC}/audit/review.md"),
                document(root, "mac-gray-adjudication", "Lead adjudication", "v1132-raw", "adjudication", f"{MAC}/ADJUDICATION.md"),
                document(root, "mac-gray-corrections", "Accepted correction brief for controlled revision", "v1132-raw", "correction_brief", f"{MAC}/revision/ACCEPTED_CORRECTIONS.md"),
                document(root, "mac-gray-verification", "Verified correction pass", "mac-gray-verified", "verification", f"{MAC}/revision/VERIFICATION.md"),
                document(root, "mac-gray-acceptance", "Latest acceptance review; R01 pending", "mac-gray-candidate", "review", f"{MAC_ACCEPTANCE}/ACCEPTANCE.md"),
                document(root, "mac-gray-acceptance-corrections", "Verified A01–A11 correction brief", "mac-gray-candidate", "correction_brief", f"{MAC_ACCEPTANCE}/ACCEPTED_CORRECTIONS.md"),
                document(root, "mac-gray-r01", "Pending R01 research decision", "mac-gray-candidate", "research_decision", f"{MAC_ACCEPTANCE}/RESEARCH_DECISION.md"),
                document(root, "mac-gray-analytical-use", "Analytical-use restrictions", "mac-gray-candidate", "limitations", f"{MAC_ACCEPTANCE}/ANALYTICAL_USE.md"),
                document(root, "mac-gray-filing-coverage", "Filing coverage and boundary", "mac-gray-candidate", "coverage", f"{MAC_ACCEPTANCE}/FILING_COVERAGE.md"),
            ]
        catalog["deals"][deal] = dict(name=name, default_base=default,
                                      versions=versions, findings=findings, documents=docs)
    provenance = {"instruction_sha256": INSTRUCTION_HASH,
                  "protected_inputs_sha256": protected,
                  "new_extractions": receipts,
                  "reused_raw": reused,
                  "mac_gray_candidate": mac_candidate,
                  "reused_raw_sha256": {d: catalog["deals"][d]["versions"][0]["sha256"] for d in ("datalink", "mac-gray")}}
    return catalog, provenance


def atomic_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def report_text(catalog: dict, provenance: dict) -> str:
    rows = []
    for deal in NEW_DEALS:
        r = provenance["new_extractions"][deal]
        check = r["checker_summary"]
        rows.append(f"| {catalog['deals'][deal]['name']} | `{r['workbook_sha256']}` | {check['errors']} | {check['warnings']} | ${r['reported_cost_usd']:.3f} |")
    total_cost = sum(r["reported_cost_usd"] for r in provenance["new_extractions"].values())
    return "\n".join([
        "# Nine-deal v1.13.2 cockpit import",
        "",
        "All seven authorized isolated Claude Opus 5 high extractions completed once. Their prepared instruction and source hashes match the frozen inputs; provider success, readable four-sheet XLSX, reported model, output hashes and separately run mechanical checks were verified from preserved receipts. The checker is mechanical and does not certify substantive correctness. Austin's source review remains pending for these seven drafts.",
        "",
        f"Frozen instruction SHA-256: `{provenance['instruction_sha256']}`.",
        "",
        "| New raw draft | SHA-256 | Checker errors | Warnings | Provider-reported cost |",
        "| --- | --- | ---: | ---: | ---: |",
        *rows,
        "",
        f"Seven-run reported cost: ${total_cost:.3f}. This is provider list-price reporting, not account billing.",
        "",
        f"Reused Datalink raw SHA-256: `{provenance['reused_raw_sha256']['datalink']}`; reused Mac-Gray raw SHA-256: `{provenance['reused_raw_sha256']['mac-gray']}`. Their existing pilot provenance and separate checks remain in their original packets. All nine canonical workbooks, nine filings, manifest, runner and instruction match the protected pre-batch hashes.",
        "",
        "The catalog preserves each raw v1.13.2 output, the eight original v1.13 baselines, and the separately verified Datalink and Mac-Gray controlled revisions. The earlier verified revisions are lead-verified correction passes, not human benchmark approvals. Datalink's retained checker result is one page-break quotation false positive and 24 length warnings; its verification report documents the exception. Neither revision overwrites a raw workbook.",
        "",
        "A newer Mac-Gray acceptance-correction candidate is the default working base: 58 events, 13 bids, 3 rounds and 9 Questions; checker 0 errors and 13 warnings. The previous 55-event verified revision remains separately selectable. The acceptance packet verifies supported A01–A11 changes but explicitly marks consequential R01 research-decision pending, accepted=false and frozen_for_research=false. The candidate is not research-ready; no R01 treatment was applied. Its acceptance report, decision, analytical-use and coverage documents are linked in the catalog.",
        "",
        "The seven new v1.13.2 drafts have no imported substantive findings; Austin's source review remains pending. Datalink and Mac-Gray audit findings retain their source-version labels and lead assessments as attributed notes. Only Austin's documented Datalink F9 ruling is carried as a user decision. No fresh substantive audit, new revision, instruction edit, commit or push was performed for this batch.",
        "",
        "Current cockpit finding judgments remain unreviewed and implementation is unassessed. Earlier applied corrections appear separately as attributed `recorded_correction` entries tied to the verified Datalink and Mac-Gray versions; they do not mark Austin's current review complete.",
        "",
        "Evidence: `batch.json`, `protected-inputs.json`, `receipts/<deal>/`, `checks/<deal>.json`, `import-verification.json`, `catalog-verification.json`, `cleanup.json`, and `_dev/cockpit/catalog.json`. After root reviewed the preserved evidence, only the seven exact disposable batch run folders and administrator script were removed; `cleanup.json` records their hashes and verified absence.",
        "",
    ])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    catalog, provenance = build_catalog(root)
    output = args.output or root / "_dev/cockpit/catalog.json"
    if output == root / "_dev/cockpit/catalog.json":
        atomic_json(root / REVIEW / "import-verification.json", provenance)
        report = root / REVIEW / "REPORT.md"
        report.write_text(report_text(catalog, provenance), encoding="utf-8")
    atomic_json(output, catalog)
    print(f"Imported {len(catalog['deals'])} deals to {output}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ImportErrorEvidence as exc:
        print(f"Import refused: {exc}", file=sys.stderr)
        raise SystemExit(2)
