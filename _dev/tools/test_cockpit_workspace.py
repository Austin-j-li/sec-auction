"""Disposable fixture tests for editable cockpit storage and HTTP boundaries."""
from __future__ import annotations

import datetime as dt
import hashlib
import io
import json
import os
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from unittest.mock import patch

from openpyxl import load_workbook

from cockpit import data, server
from cockpit.workspace import WorkspaceError, Conflict
from test_cockpit import build_repo


def fixture(root: Path) -> tuple[data.Cockpit, bytes]:
    build_repo(root)
    path = root / "extraction/alpha-deal.xlsx"
    original = path.read_bytes()
    catalog = {"schema_version": 1, "deals": {"alpha-deal": {
        "name": "Alpha Deal", "default_base": "v1132-raw",
        "versions": [{"id": "v1132-raw", "label": "Raw v1.13.2", "path": "extraction/alpha-deal.xlsx", "sha256": hashlib.sha256(original).hexdigest(), "instruction_version": "1.13.2", "kind": "raw", "review_status": "unreviewed"}],
        "findings": [{"id": "F1", "title": "Finding one", "detail": "Review event", "rule": "E2", "source_version": "v1132-raw", "source_label": "Raw", "source_rows": [2], "evidence": [], "proposed_change": "Consider correction", "needs_recheck": True, "judgment": "unreviewed", "implementation": "not_applied", "verification": "unchecked", "note": "", "actor": None, "at": None}],
        "documents": [{"id": "report", "label": "Report", "source_version": "v1132-raw", "kind": "report", "path": "_dev/reviews/report.md"}],
    }}}
    (root / "_dev/cockpit").mkdir(parents=True)
    (root / "_dev/reviews").mkdir(parents=True)
    (root / "_dev/reviews/report.md").write_text("A report", encoding="utf-8")
    (root / "_dev/cockpit/catalog.json").write_text(json.dumps(catalog), encoding="utf-8")
    (root / "SEC_Deal_Ledger_Extraction_Instruction.md").write_text("# Synthetic instruction\n\n**Revision of 1 January 2026, v1.13.2.**\n\nRead the filing.\n", encoding="utf-8")
    return data.Cockpit(root), original


class WorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.cockpit, self.original = fixture(self.root)
        self.ws = self.cockpit.workspace
        self.base = hashlib.sha256(self.original).hexdigest()

    def tearDown(self): self.temp.cleanup()

    def save(self, ops, revision=0, reason="Review edit", actor="austin"):
        return self.ws.edit("alpha-deal", {"revision": revision, "base_sha256": self.base, "reason": reason, "operations": ops}, actor)

    def test_read_only_get_and_immutable_export(self):
        payload = self.cockpit.deal("alpha-deal")
        self.assertEqual(payload["workspace"]["revision"], 0)
        self.assertEqual(payload["ledger"]["rows"][-1]["excel_row"], 8)
        self.assertFalse(self.ws.db_path.exists())
        self.assertEqual(self.ws.export("alpha-deal", "v1132-raw"), self.original)
        self.assertEqual(self.ws.document("alpha-deal", "report")["text"], "A report")

    def test_deal_without_default_base_is_a_clear_error(self):
        catalog_path = self.root / "_dev/cockpit/catalog.json"
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        del catalog["deals"]["alpha-deal"]["default_base"]
        catalog_path.write_text(json.dumps(catalog), encoding="utf-8")
        with self.assertRaisesRegex(WorkspaceError, "no default_base"):
            data.Cockpit(self.root).deal("alpha-deal")

    def test_typed_edit_history_restart_and_restore(self):
        row = self.cockpit.deal("alpha-deal")["ledger"]["rows"][0]
        result = self.save([{"type": "update", "sheet": "Deal ledger", "uid": row["uid"], "values": {"Price low": "12.5", "Sort date": "2020-03-04", "Reviewer note": "=source wording"}}])
        self.assertEqual(result["workspace"]["revision"], 1)
        self.assertEqual(result["ledger"]["rows"][0]["cells"]["Price low"], "12.5")
        wb = load_workbook(io.BytesIO(self.ws.export("alpha-deal")))
        self.assertEqual(wb["Deal ledger"]["H2"].value, 12.5)
        self.assertIsInstance(wb["Deal ledger"]["T2"].value, dt.datetime)
        self.assertEqual(wb["Deal ledger"]["S2"].data_type, "s")
        self.assertEqual(wb["Deal ledger"]["S2"].value, "=source wording")
        self.assertEqual(self.root.joinpath("extraction/alpha-deal.xlsx").read_bytes(), self.original)
        reopened = data.Cockpit(self.root)
        self.assertEqual(reopened.deal("alpha-deal")["workspace"]["revision"], 1)
        self.assertIn("12.5", json.dumps(reopened.workspace.history("alpha-deal")))
        self.assertIn("12.5", json.dumps(reopened.workspace.changes("alpha-deal")))
        self.assertTrue(all(change["record_label"] for change in reopened.workspace.history("alpha-deal")["history"][0]["changes"]))
        self.assertTrue(any("Event #1" in change["record_label"] for change in reopened.workspace.history("alpha-deal")["history"][0]["changes"]))
        restored = reopened.workspace.edit("alpha-deal", {"revision": 1, "base_sha256": self.base, "reason": "Restore raw", "operations": [{"type": "restore", "target_revision": 0}]}, "alex")
        self.assertEqual(restored["workspace"]["revision"], 2)
        self.assertEqual(restored["ledger"]["rows"][0]["cells"]["Price low"], "10")
        self.assertEqual(len(reopened.workspace.history("alpha-deal")["history"]), 3)

    def test_post_round_event_can_be_updated_and_cloned_with_typed_cells(self):
        rows = self.cockpit.deal("alpha-deal")["ledger"]["rows"]
        original = rows[-1]
        updated = self.save([{"type": "update", "sheet": "Deal ledger", "uid": original["uid"], "values": {"Round": "post", "Event": "Merger announced"}}])
        post = updated["ledger"]["rows"][-1]
        self.assertEqual(post["cells"]["Round"], "post")
        clone_values = dict(post["cells"])
        clone_values.pop("#")
        clone_values["Who"] = "Cloned post event"
        clone_values["Count"] = ""
        cloned = self.save([{"type": "insert", "sheet": "Deal ledger", "after_uid": post["uid"], "values": clone_values}], revision=1)
        new_row = cloned["ledger"]["rows"][-1]
        self.assertEqual((new_row["cells"]["Round"], new_row["cells"]["Who"], new_row["cells"]["Count"]), ("post", "Cloned post event", ""))
        wb = load_workbook(io.BytesIO(self.ws.export("alpha-deal")))
        ws = wb["Deal ledger"]
        headers = [cell.value for cell in ws[1]]
        round_cell = ws.cell(ws.max_row, headers.index("Round") + 1)
        price_cell = ws.cell(ws.max_row, headers.index("Price low") + 1)
        date_cell = ws.cell(ws.max_row, headers.index("Sort date") + 1)
        self.assertEqual((round_cell.value, round_cell.data_type), ("post", "s"))
        self.assertEqual((price_cell.value, price_cell.data_type), (10, "n"))
        self.assertIsInstance(date_cell.value, dt.datetime)
        self.assertEqual(wb["Rounds"].cell(2, 2).data_type, "n")
        wb.close()

    def test_atomic_stale_and_deleted_references(self):
        rows = self.cockpit.deal("alpha-deal")["ledger"]["rows"]
        first, second = rows[0]["uid"], rows[1]["uid"]
        with self.assertRaises(WorkspaceError):
            self.save([{"type": "update", "sheet": "Deal ledger", "uid": first, "values": {"Who": "Changed"}}, {"type": "delete", "sheet": "Deal ledger", "uid": first}])
        self.assertEqual([entry["revision"] for entry in self.ws.history("alpha-deal")["history"]], [0])
        with self.assertRaises(WorkspaceError): self.save([{"type": "delete", "sheet": "Deal ledger", "uid": first, "replacement_uid": None}])
        saved = self.save([{"type": "delete", "sheet": "Deal ledger", "uid": first, "replacement_uid": second}])
        self.assertEqual(saved["ledger"]["rows"][0]["uid"], second)
        self.assertEqual(saved["questions"]["rows"][0]["cells"]["Rows affected"], "#1")
        with self.assertRaises(Conflict): self.save([{"type": "review", "uid": second, "status": "reviewed", "note": ""}])

    def test_insert_move_and_question_flags(self):
        payload = self.cockpit.deal("alpha-deal")
        first = payload["ledger"]["rows"][0]["uid"]
        result = self.save([{"type": "insert", "sheet": "Deal ledger", "after_uid": None, "values": {"Who": "New", "Event": "Contact", "Sort date": "2020-02-29"}}])
        self.assertEqual([row["id"] for row in result["ledger"]["rows"]], list(range(1, 8)))
        self.assertEqual(result["questions"]["rows"][0]["cells"]["Rows affected"], "#2, #3")
        inserted = result["ledger"]["rows"][0]["uid"]
        self.assertEqual(result["ledger"]["rows"][1]["uid"], first)
        moved = self.save([{"type": "move", "sheet": "Deal ledger", "uid": inserted, "after_uid": first}], revision=1)
        self.assertEqual(moved["ledger"]["rows"][0]["uid"], first)
        question = moved["questions"]["rows"][0]["uid"]
        renamed = self.save([{"type": "update", "sheet": "Questions", "uid": question, "values": {"Q": "Q2"}}], revision=2)
        self.assertEqual(renamed["ledger"]["rows"][0]["cells"]["Flag"], "Q2")

    def test_finding_and_review_attribution(self):
        uid = self.cockpit.deal("alpha-deal")["ledger"]["rows"][0]["uid"]
        result = self.save([{"type": "finding", "id": "F1", "judgment": "supported", "implementation": "not_applied", "verification": "unchecked", "note": "Needs source check"}, {"type": "review", "uid": uid, "status": "needs_decision", "note": "Check date"}], actor="alex")
        self.assertEqual(result["findings"][0]["actor"], "alex")
        self.assertEqual(result["row_review"][uid]["actor"], "alex")
        self.assertEqual(result["findings"][0]["implementation"], "not_applied")

    def test_finding_implementation_can_remain_unassessed(self):
        result = self.save([{"type": "finding", "id": "F1", "judgment": "unreviewed", "implementation": "unassessed", "verification": "unchecked", "note": "Current copy not checked"}], actor="alex")
        finding = result["findings"][0]
        self.assertEqual((finding["judgment"], finding["implementation"], finding["verification"]), ("unreviewed", "unassessed", "unchecked"))
        self.assertEqual(finding["actor"], "alex")
        reopened = data.Cockpit(self.root)
        self.assertEqual(reopened.deal("alpha-deal")["findings"][0]["implementation"], "unassessed")

    def test_huge_range_rejected(self):
        q = self.cockpit.deal("alpha-deal")["questions"]["rows"][0]["uid"]
        with self.assertRaisesRegex(WorkspaceError, "too large"):
            self.save([{"type": "update", "sheet": "Questions", "uid": q, "values": {"Rows affected": "#1-#999999999"}}])

    def test_new_rows_can_anchor_later_batch_operations(self):
        first = self.cockpit.deal("alpha-deal")["ledger"]["rows"][0]["uid"]
        saved = self.save([
            {"type": "insert", "sheet": "Deal ledger", "client_uid": "new-one", "after_uid": first, "values": {"Who": "First new"}},
            {"type": "insert", "sheet": "Deal ledger", "client_uid": "new-two", "after_uid": "new-one", "values": {"Who": "Second new"}},
            {"type": "move", "sheet": "Deal ledger", "uid": "new-two", "after_uid": first},
            {"type": "review", "uid": "new-one", "status": "reviewed", "note": "Confirmed"},
        ])
        rows = saved["ledger"]["rows"]
        self.assertEqual([row["cells"]["Who"] for row in rows[:3]], ["Alpha", "Second new", "First new"])
        self.assertEqual(saved["row_review"][rows[2]["uid"]]["status"], "reviewed")

    def test_interior_narrative_range_blocks_dangling_delete(self):
        rows = self.cockpit.deal("alpha-deal")["ledger"]["rows"]
        first, middle, last = rows[0]["uid"], rows[1]["uid"], rows[2]["uid"]
        state = self.save([{"type": "update", "sheet": "Deal ledger", "uid": first, "values": {"Note": "Compare #1-#3"}}])
        with self.assertRaises(WorkspaceError):
            self.save([{"type": "delete", "sheet": "Deal ledger", "uid": middle}], revision=1)
        state = self.save([{"type": "delete", "sheet": "Deal ledger", "uid": middle, "replacement_uid": last}], revision=1)
        self.assertEqual(state["ledger"]["rows"][0]["cells"]["Note"], "Compare #1, #2")

    def test_batch_literals_use_pre_save_event_numbers(self):
        rows = self.cockpit.deal("alpha-deal")["ledger"]["rows"]
        saved = self.save([
            {"type": "insert", "sheet": "Deal ledger", "client_uid": "new-bid", "after_uid": rows[0]["uid"], "values": {"Who": "New bidder"}},
            {"type": "update", "sheet": "Deal ledger", "uid": rows[2]["uid"], "values": {"Note": "See #2 and unknown #999"}},
        ])
        self.assertEqual(saved["ledger"]["rows"][3]["cells"]["Note"], "See #3 and unknown #999")

    def test_failed_render_rolls_back_and_excel_length_is_bounded(self):
        uid = self.cockpit.deal("alpha-deal")["ledger"]["rows"][0]["uid"]
        operation = {"type": "update", "sheet": "Deal ledger", "uid": uid, "values": {"Note": "A change"}}
        with patch.object(self.ws, "_render_xlsx", side_effect=RuntimeError("synthetic render failure")):
            with self.assertRaisesRegex(RuntimeError, "synthetic render failure"):
                self.save([operation])
        self.assertEqual([entry["revision"] for entry in self.ws.history("alpha-deal")["history"]], [0])
        with self.assertRaisesRegex(WorkspaceError, "32767"):
            self.save([{**operation, "values": {"Note": "😀" * 20000}}])
        self.assertEqual([entry["revision"] for entry in self.ws.history("alpha-deal")["history"]], [0])

    def test_replacement_chain_and_late_deleted_reference_rejected(self):
        rows = self.cockpit.deal("alpha-deal")["ledger"]["rows"]
        first, unreferenced = rows[0]["uid"], rows[-1]["uid"]
        with self.assertRaises(WorkspaceError):
            self.save([
                {"type": "delete", "sheet": "Deal ledger", "uid": first, "replacement_uid": unreferenced},
                {"type": "delete", "sheet": "Deal ledger", "uid": unreferenced},
            ])
        with self.assertRaises(WorkspaceError):
            self.save([
                {"type": "delete", "sheet": "Deal ledger", "uid": unreferenced},
                {"type": "update", "sheet": "Deal ledger", "uid": first, "values": {"Note": "Later see #7"}},
            ])
        self.assertEqual([entry["revision"] for entry in self.ws.history("alpha-deal")["history"]], [0])

    def test_question_rename_updates_narrative_and_late_old_reference_rejected(self):
        payload = self.cockpit.deal("alpha-deal")
        question = payload["questions"]["rows"][0]["uid"]
        round_uid = payload["rounds"]["rows"][0]["uid"]
        ledger_uid = payload["ledger"]["rows"][0]["uid"]
        with self.assertRaises(WorkspaceError):
            self.save([
                {"type": "update", "sheet": "Questions", "uid": question, "values": {"Q": "Q2"}},
                {"type": "update", "sheet": "Rounds", "uid": round_uid, "values": {"How opened": "Old Q1 again"}},
            ])
        saved = self.save([
            {"type": "update", "sheet": "Rounds", "uid": round_uid, "values": {"How opened": "Review Q1"}},
            {"type": "update", "sheet": "Questions", "uid": question, "values": {"Q": "Q2"}},
        ])
        self.assertEqual(saved["rounds"]["rows"][0]["cells"]["How opened"], "Review Q2")
        self.assertEqual(saved["ledger"]["rows"][0]["cells"]["Flag"], "Q2")
        with self.assertRaises(WorkspaceError):
            self.save([{"type": "delete", "sheet": "Questions", "uid": question}], revision=1)


class HTTPTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.cockpit, _ = fixture(self.root)
        self.httpd = server.make_server(0, self.cockpit, quiet=True)
        self.port = self.httpd.server_address[1]
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.httpd.shutdown(); self.httpd.server_close(); self.temp.cleanup()

    def request(self, path, body=None, headers=None):
        req = urllib.request.Request(f"http://127.0.0.1:{self.port}{path}", data=body, headers=headers or {})
        try:
            with urllib.request.urlopen(req, timeout=20) as response: return response.status, json.loads(response.read()) if response.headers.get_content_type() == "application/json" else response.read()
        except urllib.error.HTTPError as exc: return exc.code, json.loads(exc.read())

    def test_session_and_write_guards(self):
        status, session = self.request("/api/session")
        self.assertEqual(status, 200)
        self.assertTrue(session["can_edit"])
        row = self.cockpit.deal("alpha-deal")["ledger"]["rows"][0]
        body = json.dumps({"revision": 0, "base_sha256": self.cockpit.deal("alpha-deal")["workspace"]["base_sha256"], "reason": "Test", "operations": [{"type": "review", "uid": row["uid"], "status": "reviewed", "note": "okay"}]}).encode()
        base_headers = {"Content-Type": "application/json", "Origin": f"http://127.0.0.1:{self.port}", "X-Cockpit-CSRF": session["csrf_token"]}
        self.assertEqual(self.request("/api/deal/alpha-deal/edit", body, {**base_headers, "X-Cockpit-CSRF": "bad"})[0], 403)
        self.assertEqual(self.request("/api/deal/alpha-deal/edit", body, {**base_headers, "Origin": "https://evil.invalid"})[0], 403)
        self.assertEqual(self.request("/api/deal/alpha-deal/edit", body, base_headers)[0], 200)
        self.assertEqual(self.request("/api/deal/alpha-deal/edit", body, base_headers)[0], 409)
        self.assertEqual(self.request("/api/document/alpha-deal/..%2F..%2Fsecret")[0], 404)
        self.assertEqual(self.request("/assets/..%2Fserver.py")[0], 404)

    def test_public_identity_requires_configured_host_and_access_email(self):
        with patch.dict(os.environ, {"COCKPIT_PUBLIC_ORIGIN": "https://lines.dealextract.org"}):
            public = {"Host": "lines.dealextract.org", "Cf-Access-Authenticated-User-Email": "junyu.li.24@ucl.ac.uk"}
            status, session = self.request("/api/session", headers=public)
            self.assertEqual(status, 200)
            self.assertEqual((session["user"], session["can_edit"]), ("austin", True))
            status, anonymous = self.request("/api/session", headers={"Host": "lines.dealextract.org"})
            self.assertEqual(status, 200)
            self.assertFalse(anonymous["can_edit"])
            row = self.cockpit.deal("alpha-deal")["ledger"]["rows"][0]
            body = json.dumps({"revision": 0, "base_sha256": self.cockpit.deal("alpha-deal")["workspace"]["base_sha256"], "reason": "Public fixture", "operations": [{"type": "review", "uid": row["uid"], "status": "reviewed", "note": "okay"}]}).encode()
            headers = {**public, "Content-Type": "application/json", "Origin": "https://lines.dealextract.org", "X-Cockpit-CSRF": session["csrf_token"]}
            self.assertEqual(self.request("/api/deal/alpha-deal/edit", body, headers)[0], 200)
            self.assertEqual(self.cockpit.deal("alpha-deal")["row_review"][row["uid"]]["actor"], "austin")


if __name__ == "__main__": unittest.main()
