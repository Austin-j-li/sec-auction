"""Synthetic evidence tests for the cockpit catalog importer."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import openpyxl

from cockpit import import_results as imp


def write_json(path: Path, value: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def make_book(path: Path) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    book = openpyxl.Workbook()
    book.active.title = imp.SHEETS[0]
    for name in imp.SHEETS[1:]:
        book.create_sheet(name)
    book.save(path)
    return imp.sha256(path)


class ImportTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_forbidden_document_path(self) -> None:
        safe = self.root / "_dev/review.md"
        safe.parent.mkdir()
        safe.write_text("safe")
        (self.root / "ref").mkdir()
        (self.root / "ref/answer.md").write_text("answer")
        self.assertEqual(imp.checked_path(self.root, "_dev/review.md"), safe)
        for path in ("../outside", "/etc/passwd", "ref/answer.md", "_dev/missing.md"):
            with self.subTest(path=path), self.assertRaises(imp.ImportErrorEvidence):
                imp.checked_path(self.root, path)

    def test_workbook_hash_and_schema(self) -> None:
        path = self.root / "raw.xlsx"
        digest = make_book(path)
        self.assertEqual(imp.workbook(self.root, "raw.xlsx", digest), digest)
        with self.assertRaises(imp.ImportErrorEvidence):
            imp.workbook(self.root, "raw.xlsx", "0" * 64)
        bad = openpyxl.Workbook()
        bad.save(self.root / "bad.xlsx")
        with self.assertRaises(imp.ImportErrorEvidence):
            imp.workbook(self.root, "bad.xlsx")

    def test_batch_refuses_incomplete_and_false_provider_success(self) -> None:
        batch_path = self.root / imp.REVIEW / "batch.json"
        write_json(batch_path, {"state": "running", "runs": {}})
        with self.assertRaisesRegex(imp.ImportErrorEvidence, "incomplete"):
            imp.verify_batch(self.root, {}, {})
        runs = {deal: {"state": "completed"} for deal in imp.NEW_DEALS}
        write_json(batch_path, dict(state="completed", runs=runs,
                                    instruction_sha256=imp.INSTRUCTION_HASH,
                                    model="claude-opus-5", effort="high"))
        protected = {}
        manifest = {}
        for deal in imp.NEW_DEALS:
            source = f"{deal}.htm"
            protected[f"raw_filing/{source}"] = hashlib.sha256(deal.encode()).hexdigest()
            manifest[deal] = {"file": source}
            folder = self.root / imp.REVIEW / "receipts" / deal
            book = f"{imp.REVIEW}/raw/extraction/{deal}.xlsx"
            digest = make_book(self.root / book)
            write_json(folder / "receipt.json", dict(state="completed", workbook_sha256=digest,
                check_summary={"errors": 0, "warnings": 1}))
            write_json(folder / "metadata.json", dict(model="claude-opus-5", effort="high",
                instruction_sha256=imp.INSTRUCTION_HASH,
                filing_sha256=protected[f"raw_filing/{source}"]))
            write_json(folder / "status.json", dict(state="completed", exit_code=0))
            write_json(folder / "validation.json", {"valid_xlsx": True, "sha256": digest})
            write_json(folder / "provider-results.json", [dict(subtype="success", is_error=False,
                modelUsage={"claude-opus-5": {}})])
            write_json(self.root / imp.REVIEW / "checks" / f"{deal}.json",
                       {"summary": {"errors": 0, "warnings": 1}})
        receipts = imp.verify_batch(self.root, protected, manifest)
        self.assertEqual(set(receipts), set(imp.NEW_DEALS))
        penford = self.root / imp.REVIEW / "receipts/penford/provider-results.json"
        write_json(penford, [{"subtype": "success", "modelUsage": {"claude-sonnet": {}}}])
        with self.assertRaisesRegex(imp.ImportErrorEvidence, "success/model"):
            imp.verify_batch(self.root, protected, manifest)

    def test_recorded_austin_ruling_keeps_provenance(self) -> None:
        write_json(self.root / imp.DATA / "fresh_findings.json", {"findings": [
            {"id": "F9", "claim": "Change first-round boundary", "affected_rows": [3],
             "rules": ["E6"], "evidence": [], "proposed_correction": "Move January to round 0"}
        ]})
        ruling = imp.datalink_findings(self.root)[0]
        self.assertEqual(ruling["source_version"], "v1132-raw")
        self.assertEqual(ruling["judgment"], "unreviewed")
        self.assertEqual(ruling["recorded_decision"]["actor"], "Austin Li")
        self.assertEqual(ruling["implementation"], "unassessed")
        self.assertEqual(ruling["recorded_correction"]["version"], "datalink-verified")
        self.assertTrue(ruling["needs_recheck"])
        write_json(self.root / imp.MAC / "audit/findings.json", {"findings": [
            {"id": "F01", "problem": "Incorrect Q9 counterfactual", "rule": "E10",
             "affected_rows": ["Questions Q9"], "quote": "a quote", "page": "39",
             "proposed_correction": "Revise Q9"}
        ]})
        mac = imp.mac_findings(self.root)
        self.assertEqual(len(mac), 5)  # audit F01 plus four distinct lead findings
        self.assertEqual(mac[0]["recorded_correction"]["version"], "mac-gray-verified")
        self.assertEqual(mac[0]["implementation"], "unassessed")
        self.assertTrue(all(f["judgment"] == "unreviewed" for f in mac))

    def test_full_catalog_versions_with_synthetic_workbooks(self) -> None:
        root = self.root
        instruction = root / "SEC_Deal_Ledger_Extraction_Instruction.md"
        instruction.write_text("synthetic frozen instruction")
        instruction_hash = imp.sha256(instruction)
        manifest_rows = ["file,deal,sha256"]
        raw_hashes = {}
        protected = {"SEC_Deal_Ledger_Extraction_Instruction.md": instruction_hash}
        for deal in imp.DEALS:
            source = root / "raw_filing" / f"{deal}.htm"
            source.parent.mkdir(parents=True, exist_ok=True)
            source.write_text(f"synthetic filing for {deal}")
            digest = imp.sha256(source)
            manifest_rows.append(f"{deal}.htm,{deal},{digest}")
            protected[f"raw_filing/{deal}.htm"] = digest
            if deal != "datalink":
                prior = f"extraction/{deal}.xlsx"
                protected[prior] = make_book(root / prior)
            raw = (f"{imp.REVIEW}/raw/extraction/{deal}.xlsx" if deal in imp.NEW_DEALS
                   else "extraction/datalink.xlsx" if deal == "datalink"
                   else f"{imp.MAC}/raw/extraction/mac-gray.xlsx")
            raw_hashes[deal] = make_book(root / raw)
            if deal == "datalink":
                protected[raw] = raw_hashes[deal]
        manifest = root / "raw_filing/MANIFEST.csv"
        manifest.write_text("\n".join(manifest_rows) + "\n")
        protected["raw_filing/MANIFEST.csv"] = imp.sha256(manifest)
        write_json(root / imp.REVIEW / "protected-inputs.json", {"sha256": protected})
        write_json(root / imp.DATA / "fresh_findings.json", {"findings": []})
        write_json(root / imp.MAC / "audit/findings.json", {"findings": []})
        write_json(root / imp.MAC / "provenance/extraction/validation.json", {"sha256": raw_hashes["mac-gray"]})
        def metadata(deal):
            return {"mode": "extract", "model": "claude-opus-5", "effort": "high",
                    "instruction_sha256": instruction_hash,
                    "filing_sha256": protected[f"raw_filing/{deal}.htm"],
                    "filing_name": f"{deal}.htm"}
        good_status = {"state": "completed", "exit_code": 0}
        good_provider = {"subtype": "success", "is_error": False,
                         "modelUsage": {"claude-opus-5": {}}}
        write_json(root / imp.DATA / "provenance.json", {
            "runs": {"extraction": {"metadata": metadata("datalink"), "status": good_status,
                     "provider_result": good_provider,
                     "validation": {"valid_xlsx": True, "sha256": raw_hashes["datalink"]}}},
            "raw_workbook_sha256": raw_hashes["datalink"]})
        write_json(root / imp.MAC / "provenance/extraction/metadata.json", metadata("mac-gray"))
        write_json(root / imp.MAC / "provenance/extraction/status.json", good_status)
        write_json(root / imp.MAC / "provenance/extraction/provider-summary.json", {
            "result": good_provider, "raw_workbook_sha256": raw_hashes["mac-gray"]})
        write_json(root / imp.MAC / "provenance/extraction/validation.json", {
            "valid_xlsx": True, "sha256": raw_hashes["mac-gray"]})
        data_rev = make_book(root / imp.DATA / "revision/datalink_revised.xlsx")
        write_json(root / imp.DATA / "revision/post_hashes.json", {"revised_workbook_sha256": data_rev})
        write_json(root / imp.DATA / "revision/structural_verification.json", {"four_sheets_in_required_order": True})
        write_json(root / imp.DATA / "revision/reference_audit.json", {"all_targets_exist": True, "question_flags_bidirectional_match": True})
        mac_rev = make_book(root / imp.MAC / "revision/extraction/mac-gray.xlsx")
        mac_candidate = make_book(root / imp.MAC_ACCEPTANCE / "extraction/mac-gray.xlsx")
        write_json(root / imp.MAC / "revision/verification/final-checks.json", {
            "final_workbook_sha256": mac_rev, "all_protected_inputs_unchanged": True,
            "no_unexpected_cell_changes_remain": True})
        for relative in (
            f"{imp.DATA}/fresh_review.md", f"{imp.DATA}/ADJUDICATION.md",
            f"{imp.DATA}/inventory_comparison.md", f"{imp.DATA}/revision/INVENTORY_VERIFICATION.md",
            f"{imp.DATA}/revision/VERIFICATION.md", f"{imp.DATA}/revision/CORRECTION_BRIEF.md",
            f"{imp.MAC}/REPORT.md", f"{imp.MAC}/audit/review.md",
            f"{imp.MAC}/ADJUDICATION.md", f"{imp.MAC}/revision/VERIFICATION.md",
            f"{imp.MAC}/revision/ACCEPTED_CORRECTIONS.md",
            f"{imp.MAC_ACCEPTANCE}/ACCEPTANCE.md",
            f"{imp.MAC_ACCEPTANCE}/ACCEPTED_CORRECTIONS.md",
            f"{imp.MAC_ACCEPTANCE}/RESEARCH_DECISION.md",
            f"{imp.MAC_ACCEPTANCE}/ANALYTICAL_USE.md",
            f"{imp.MAC_ACCEPTANCE}/FILING_COVERAGE.md",
        ):
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("accepted corrections implemented\n")
        data_receipts = {deal: {"workbook_sha256": raw_hashes[deal],
                                "checker_summary": {"errors": 0, "warnings": 1},
                                "reported_cost_usd": 1.0} for deal in imp.NEW_DEALS}
        with mock.patch.object(imp, "INSTRUCTION_HASH", instruction_hash), \
             mock.patch.object(imp, "verify_batch", return_value=data_receipts), \
             mock.patch.object(imp, "verify_mac_candidate", return_value={"workbook_sha256": mac_candidate, "r01_pending": True}), \
             mock.patch.object(imp, "workbook", wraps=imp.workbook) as checked:
            # The checked Mac-Gray final hash is fixed by the preserved real
            # packet; patch only that literal fixture-specific check.
            def fixture_workbook(r, relative, expected=None):
                if relative.endswith("revision/extraction/mac-gray.xlsx"):
                    expected = mac_rev
                return checked._mock_wraps(r, relative, expected)
            checked.side_effect = fixture_workbook
            catalog, provenance = imp.build_catalog(root)
        self.assertEqual(set(catalog["deals"]), set(imp.DEALS))
        self.assertEqual(catalog["deals"]["datalink"]["default_base"], "datalink-verified")
        self.assertEqual(catalog["deals"]["mac-gray"]["default_base"], "mac-gray-candidate")
        self.assertEqual(len(catalog["deals"]["mac-gray"]["versions"]), 4)
        self.assertEqual(catalog["deals"]["mac-gray"]["versions"][-1]["sha256"], mac_candidate)
        self.assertTrue(any(f["id"] == "mac-gray-r01" and f["source_version"] == "mac-gray-candidate"
                            for f in catalog["deals"]["mac-gray"]["findings"]))
        self.assertEqual(catalog["deals"]["kraton"]["default_base"], "v1132-raw")
        self.assertEqual(len(catalog["deals"]["kraton"]["versions"]), 2)
        for deal in imp.NEW_DEALS:
            self.assertEqual(catalog["deals"][deal]["findings"], [])
            self.assertEqual(catalog["deals"][deal]["documents"], [])
        self.assertNotIn("three-model", json.dumps(catalog))
        self.assertNotIn("three-model", imp.report_text(catalog, provenance))
        self.assertEqual(len(provenance["new_extractions"]), 7)
        self.assertEqual(provenance["reused_raw"]["datalink"]["source_sha256"],
                         protected["raw_filing/datalink.htm"])
        bad_meta = metadata("mac-gray")
        bad_meta["model"] = "claude-sonnet"
        write_json(root / imp.MAC / "provenance/extraction/metadata.json", bad_meta)
        with mock.patch.object(imp, "INSTRUCTION_HASH", instruction_hash), \
             self.assertRaisesRegex(imp.ImportErrorEvidence, "Reused raw provenance"):
            imp.verify_reused(root, protected, {d: {"file": f"{d}.htm"} for d in imp.DEALS})


if __name__ == "__main__":
    unittest.main()
