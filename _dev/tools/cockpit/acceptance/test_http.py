"""End-to-end HTTP contract checks against a disposable synthetic repository.

Run from the repository root: python3 -m pytest -q _dev/tools/cockpit/acceptance/test_http.py
No real filing, workbook, catalog, or working-state database is opened by this suite.
"""

from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io
import json
import sys
import tempfile
import threading
import time
from pathlib import Path

import openpyxl
from openpyxl.comments import Comment
from openpyxl.styles import PatternFill
import pytest
import requests

TOOLS = Path(__file__).resolve().parents[2]
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from cockpit import data, server  # noqa: E402
import check_lean  # noqa: E402


def synthetic_repo(root: Path) -> tuple[Path, str]:
    """Make a small, traceable four-sheet deal with no research content."""
    extraction = root / "extraction"
    filings = root / "raw_filing"
    catalog_dir = root / "_dev/cockpit"
    docs = root / "_dev/reviews/synthetic"
    for directory in (extraction, filings, catalog_dir, docs):
        directory.mkdir(parents=True, exist_ok=True)
    (root / "SEC_Deal_Ledger_Extraction_Instruction.md").write_text("# Synthetic instruction\n\n**Revision of 1 January 2026, v1.13.2.**\n\nRead the filing.\nSave the workbook.\n", encoding="utf-8")

    filing = ("""<html><body><h1>Background of the Merger</h1>
    <p>1</p><p>Acme invited bids from three parties.</p>
    <p>Acme received an offer from Party A.</p>
    <p>Acme signed the merger agreement.</p>
    """ + "".join(f"<p>Synthetic page one filler paragraph {n}.</p>" for n in range(60)) + """
    <p>2</p><p>Later supplemental discussion is searchable.</p>
    </body></html>""").encode("utf-8")
    filing_path = filings / "synthetic.htm"
    filing_path.write_bytes(filing)
    with (filings / "MANIFEST.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["file", "deal", "form_type", "date_filed", "source_url", "document", "fetched_utc", "bytes", "sha256"])
        writer.writeheader()
        writer.writerow({"file": filing_path.name, "deal": "synthetic", "form_type": "DEFM14A", "date_filed": "2026-01-10", "source_url": "https://example.invalid/synthetic", "document": filing_path.name, "fetched_utc": "2026-01-10T00:00:00Z", "bytes": len(filing), "sha256": hashlib.sha256(filing).hexdigest()})

    wb = openpyxl.Workbook()
    ledger = wb.active
    ledger.title = "Deal ledger"
    ledger.append(check_lean.LEDGER_COLUMNS)
    rows = [
        {"#": 1, "When": "2026-01-01", "Who": "Acme", "Type": "Contact", "Event": "Invitation", "Process": 1, "Round": 1, "Count": 3, "Note": "Three parties contacted", "Quote and page": "Acme invited bids from three parties. (p. 1)", "Sort date": dt.datetime(2026, 1, 1), "Date from": dt.datetime(2026, 1, 1)},
        {"#": 2, "When": "Date uncertain", "Who": "Party A", "Type": "Bid", "Event": "Offer", "Process": 1, "Round": 1, "Price low": 12.5, "Price high": 12.5, "Count": None, "Note": "Follow-up to #1", "Quote and page": "Acme received an offer from Party A. (p. 1)", "Flag": "Q1", "Sort date": None, "Date from": None},
        {"#": 3, "When": "2026-01-03", "Who": "Acme", "Type": "Agreement", "Event": "Signing", "Process": 1, "Round": 1, "Note": "After #2", "Quote and page": "Acme signed the merger agreement. (p. 1)", "Flag": "Q1", "Sort date": dt.datetime(2026, 1, 3), "Date from": dt.datetime(2026, 1, 3)},
    ]
    for values in rows:
        ledger.append([values.get(field) for field in check_lean.LEDGER_COLUMNS])
    for field in ("Sort date", "Date from", "Date to"):
        column = check_lean.LEDGER_COLUMNS.index(field) + 1
        for excel_row in range(2, 5):
            ledger.cell(excel_row, column).number_format = "mm/dd/yyyy"
    ledger.auto_filter.ref = f"A1:{openpyxl.utils.get_column_letter(len(check_lean.LEDGER_COLUMNS))}4"
    ledger.freeze_panes = "A2"
    ledger.cell(2, check_lean.LEDGER_COLUMNS.index("Who") + 1).fill = PatternFill("solid", fgColor="FFCCDDEE")
    ledger.cell(2, check_lean.LEDGER_COLUMNS.index("Reviewer note") + 1).value = "=1+1"
    ledger.cell(4, check_lean.LEDGER_COLUMNS.index("Event") + 1).hyperlink = "https://example.invalid/record"
    ledger.cell(4, check_lean.LEDGER_COLUMNS.index("Note") + 1).comment = Comment("Preserve synthetic annotation", "Fixture")

    rounds = wb.create_sheet("Rounds")
    rounds.append(check_lean.ROUND_COLUMNS)
    rounds.append([{"Process": 1, "Round": 1, "Opened": dt.datetime(2026, 1, 1), "How opened": "Invitation #1", "Who was in": "Party A", "Bids received": 1}.get(field) for field in check_lean.ROUND_COLUMNS])
    rounds.cell(2, check_lean.ROUND_COLUMNS.index("Opened") + 1).number_format = "mm/dd/yyyy"
    rounds.auto_filter.ref = f"A1:J2"

    questions = wb.create_sheet("Questions")
    questions.append(check_lean.QUESTION_COLUMNS)
    questions.append([{"Q": "Q1", "Question": "When did Party A bid?", "Recommended answer": "Date unknown", "Rows affected": "#2-#3"}.get(field) for field in check_lean.QUESTION_COLUMNS])
    questions.auto_filter.ref = "A1:G2"

    facts = wb.create_sheet("Deal facts")
    facts.append(check_lean.FACT_COLUMNS)
    facts.append(["Target", "Synthetic Acme"])
    facts.append(["Number of processes", 1])
    facts.auto_filter.ref = "A1:B3"
    workbook = extraction / "synthetic.xlsx"
    wb.save(workbook)
    wb.close()
    original_hash = hashlib.sha256(workbook.read_bytes()).hexdigest()

    (docs / "finding.md").write_text("# Synthetic finding\nCheck uncertain bid date.\n", encoding="utf-8")
    catalog = {"schema_version": 1, "deals": {"synthetic": {
        "name": "Synthetic Acme", "default_base": "v1132-raw",
        "versions": [{"id": "v1132-raw", "label": "Synthetic raw", "path": "extraction/synthetic.xlsx", "sha256": original_hash, "instruction_version": "v1.13.2", "kind": "raw", "review_status": "unreviewed"}],
        "findings": [{"id": "F1", "title": "Uncertain date", "detail": "Date remains unknown", "rule": "E8", "source_version": "v1132-raw", "source_label": "Synthetic raw", "source_rows": [2], "evidence": [{"quote": "Acme received an offer from Party A.", "page": "1"}], "proposed_change": "Review date", "needs_recheck": True, "judgment": "unreviewed", "implementation": "not_applied", "verification": "unchecked", "note": "", "actor": None, "at": None}],
        "documents": [{"id": "finding", "label": "Synthetic finding", "source_version": "v1132-raw", "kind": "report", "path": "_dev/reviews/synthetic/finding.md"}],
    }}}
    (catalog_dir / "catalog.json").write_text(json.dumps(catalog), encoding="utf-8")
    return workbook, original_hash


class HttpFixture:
    def __init__(self, root: Path):
        self.root = root
        self.cockpit = data.Cockpit(root)
        self.httpd = server.make_server(0, self.cockpit, quiet=True)
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        self.base = f"http://127.0.0.1:{self.httpd.server_port}"
        self.client = requests.Session()

    def close(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(timeout=5)
        self.client.close()

    def get(self, path: str, **kwargs):
        return self.client.get(self.base + path, timeout=30, **kwargs)

    def session(self):
        response = self.get("/api/session")
        assert response.status_code == 200, response.text
        return response.json()

    def post(self, path: str, payload, *, csrf=None, origin=None, content_type="application/json", headers=None):
        csrf = self.session()["csrf_token"] if csrf is None else csrf
        hdrs = {"X-Cockpit-CSRF": csrf, "Content-Type": content_type}
        if origin != "omit":
            hdrs["Origin"] = origin or self.base
        if headers:
            hdrs.update(headers)
        return self.client.post(self.base + path, data=json.dumps(payload) if content_type == "application/json" else payload, headers=hdrs, timeout=30)

    def edit(self, payload, **kwargs):
        return self.post("/api/deal/synthetic/edit", payload, **kwargs)


@pytest.fixture
def env():
    with tempfile.TemporaryDirectory(prefix="cockpit-acceptance-") as folder:
        root = Path(folder)
        workbook, original_hash = synthetic_repo(root)
        http = HttpFixture(root)
        try:
            yield http, workbook, original_hash
        finally:
            http.close()


def deal(http, version="working"):
    response = http.get(f"/api/deal/synthetic?version={version}")
    assert response.status_code == 200, response.text
    return response.json()


def save(http, snapshot, operations, reason="Synthetic acceptance change"):
    payload = {"revision": snapshot["workspace"]["revision"], "base_sha256": snapshot["workspace"]["base_sha256"], "reason": reason, "operations": operations}
    return http.edit(payload)


def row(snapshot, sheet, index=0):
    rows = snapshot["facts"] if sheet == "Deal facts" else snapshot[{"Deal ledger": "ledger", "Rounds": "rounds", "Questions": "questions"}[sheet]]["rows"]
    return rows[index]


def xlsx(response):
    assert response.status_code == 200, response.text
    return openpyxl.load_workbook(io.BytesIO(response.content), data_only=False)


def test_baseline_catalog_source_and_raw_are_read_only(env):
    http, workbook, original_hash = env
    initial = deal(http)
    assert initial["workspace"]["revision"] == 0
    assert initial["workspace"]["editable"] is True
    assert {v["id"] for v in initial["versions"]} == {"working", "v1132-raw"}
    assert initial["findings"][0]["judgment"] == "unreviewed"
    assert initial["ledger"]["rows"][1]["cells"]["Count"] == ""
    assert initial["ledger"]["rows"][1]["cells"]["Date from"] == ""
    raw_payload = deal(http, "v1132-raw")
    original_report = check_lean.LeanChecker(workbook, http.root / "raw_filing/synthetic.htm").run()
    assert raw_payload["check"]["summary"] == original_report["summary"]
    attached_sheets = {"Deal ledger", "Rounds", "Questions"}
    expected_other = [issue for issue in original_report["issues"] if issue.get("sheet") not in attached_sheets or not isinstance(issue.get("row"), int) or issue.get("row") == 1]
    assert [(issue["code"], issue.get("sheet"), issue.get("row")) for issue in raw_payload["check"]["other_issues"]] == [(issue["code"], issue.get("sheet"), issue.get("row")) for issue in expected_other]
    assert initial["check"]["summary"] == raw_payload["check"]["summary"]
    assert http.get("/api/document/synthetic/finding").json()["text"].startswith("# Synthetic finding")
    assert "Acme invited bids" in json.dumps(http.get("/api/filing/synthetic").json())
    assert hashlib.sha256(http.get("/api/deal/synthetic/export?version=v1132-raw").content).hexdigest() == original_hash
    with (http.root / "raw_filing/MANIFEST.csv").open(newline="", encoding="utf-8") as handle:
        source_hash = next(csv.DictReader(handle))["sha256"]
    assert hashlib.sha256((http.root / "raw_filing/synthetic.htm").read_bytes()).hexdigest() == source_hash
    raw = deal(http, "v1132-raw")
    assert raw["workspace"]["editable"] is False
    assert workbook.read_bytes() == http.get("/api/deal/synthetic/export?version=v1132-raw").content


def test_four_sheet_edits_typed_export_decision_and_restart(env):
    http, workbook, original_hash = env
    initial = deal(http)
    ops = [
        {"type": "update", "sheet": "Deal ledger", "uid": row(initial, "Deal ledger", 1)["uid"], "values": {"Price low": 13.25, "Price high": 13.25, "Count": "", "Date from": "", "Sort date": "2026-01-02"}},
        {"type": "update", "sheet": "Rounds", "uid": row(initial, "Rounds")["uid"], "values": {"Opened": "2026-01-02", "Bids received": 2}},
        {"type": "update", "sheet": "Questions", "uid": row(initial, "Questions")["uid"], "values": {"Recommended answer": "Still uncertain"}},
        {"type": "update", "sheet": "Deal facts", "uid": row(initial, "Deal facts", 0)["uid"], "values": {"Value": "Synthetic Acme Revised"}},
        {"type": "finding", "id": "F1", "judgment": "supported", "implementation": "not_applied", "verification": "unchecked", "note": "Synthetic-only judgment"},
        {"type": "review", "uid": row(initial, "Deal ledger", 1)["uid"], "status": "needs_decision", "note": "Date unknown"},
    ]
    saved = save(http, initial, ops, "Edit four sheets and record judgment")
    assert saved.status_code == 200, saved.text
    payload = saved.json()
    assert payload["workspace"]["revision"] == 1
    assert payload["ledger"]["rows"][1]["cells"]["Count"] == ""
    assert payload["ledger"]["rows"][1]["cells"]["Date from"] == ""
    assert payload["findings"][0]["judgment"] == "supported"
    assert payload["findings"][0]["actor"] == http.session()["user"]
    assert payload["row_review"][row(initial, "Deal ledger", 1)["uid"]]["status"] == "needs_decision"
    assert len(http.get("/api/deal/synthetic/changes").json()["changes"]) >= 6
    history = http.get("/api/deal/synthetic/history").json()["history"]
    assert history[0]["reason"] == "Edit four sheets and record judgment"
    assert history[0]["actor"] == http.session()["user"]
    assert any(change["field"] == "Value" and change["after"] == "Synthetic Acme Revised" for change in history[0]["changes"])

    exported = xlsx(http.get("/api/deal/synthetic/export?version=working"))
    ledger = exported["Deal ledger"]
    def cell(sheet, excel_row, field):
        columns = [c.value for c in exported[sheet][1]]
        return exported[sheet].cell(excel_row, columns.index(field) + 1)
    assert cell("Deal ledger", 3, "Price low").value == 13.25
    assert cell("Deal ledger", 3, "Price low").data_type == "n"
    assert cell("Deal ledger", 3, "Count").value is None
    assert cell("Deal ledger", 3, "Date from").value is None
    assert isinstance(cell("Deal ledger", 3, "Sort date").value, dt.datetime)
    assert isinstance(cell("Rounds", 2, "Opened").value, dt.datetime)
    assert cell("Rounds", 2, "Bids received").data_type == "n"
    assert cell("Deal facts", 2, "Value").value == "Synthetic Acme Revised"
    assert cell("Deal ledger", 2, "Who").fill.fgColor.rgb == "FFCCDDEE"
    assert cell("Deal ledger", 2, "Reviewer note").value == "=1+1"
    assert cell("Deal ledger", 4, "Event").hyperlink.target == "https://example.invalid/record"
    assert cell("Deal ledger", 4, "Note").comment.text == "Preserve synthetic annotation"
    assert list(exported.sheetnames) == ["Deal ledger", "Rounds", "Questions", "Deal facts"]
    assert ledger.auto_filter.ref.endswith("4")
    exported.close()
    assert hashlib.sha256(workbook.read_bytes()).hexdigest() == original_hash

    http.close()
    restarted = HttpFixture(http.root)
    try:
        reloaded = deal(restarted)
        assert reloaded["workspace"]["revision"] == 1
        assert reloaded["findings"][0]["note"] == "Synthetic-only judgment"
        assert reloaded["ledger"]["rows"][1]["cells"]["Price low"] == "13.25"
    finally:
        restarted.close()


def test_insert_move_references_delete_restore_and_history(env):
    http, workbook, original_hash = env
    initial = deal(http)
    uid1, uid2, uid3 = [r["uid"] for r in initial["ledger"]["rows"]]
    inserted = save(http, initial, [{"type": "insert", "sheet": "Deal ledger", "after_uid": uid1, "values": {"When": "Date unknown", "Who": "Party B", "Event": "Synthetic insertion", "Count": "", "Date from": "", "Note": "New event"}}], "Insert uncertain event")
    assert inserted.status_code == 200, inserted.text
    state = inserted.json()
    assert [r["id"] for r in state["ledger"]["rows"]] == [1, 2, 3, 4]
    new_uid = state["ledger"]["rows"][1]["uid"]
    assert state["ledger"]["rows"][2]["uid"] == uid2
    assert state["ledger"]["rows"][2]["cells"]["Note"] == "Follow-up to #1"
    assert state["ledger"]["rows"][3]["cells"]["Note"] == "After #3"
    assert "#3" in state["questions"]["rows"][0]["cells"]["Rows affected"]
    assert "#4" in state["questions"]["rows"][0]["cells"]["Rows affected"]
    assert state["ledger"]["rows"][1]["cells"]["Count"] == ""
    assert state["ledger"]["rows"][1]["cells"]["Date from"] == ""

    moved = save(http, state, [{"type": "move", "sheet": "Deal ledger", "uid": uid3, "after_uid": uid1}], "Move signing before bid")
    assert moved.status_code == 200, moved.text
    state = moved.json()
    assert [r["uid"] for r in state["ledger"]["rows"]] == [uid1, uid3, new_uid, uid2]
    assert state["ledger"]["rows"][1]["cells"]["Note"] == "After #4"
    assert "#4" in state["questions"]["rows"][0]["cells"]["Rows affected"]
    assert "#2" in state["questions"]["rows"][0]["cells"]["Rows affected"]
    assert "#3" not in state["questions"]["rows"][0]["cells"]["Rows affected"]

    rejection = save(http, state, [{"type": "delete", "sheet": "Deal ledger", "uid": uid2}], "Reject dangling reference")
    assert rejection.status_code == 400, rejection.text
    assert deal(http)["workspace"]["revision"] == 2
    invalid = save(http, state, [{"type": "delete", "sheet": "Deal ledger", "uid": uid2, "replacement_uid": "not-live"}], "Invalid replacement")
    assert invalid.status_code == 400, invalid.text
    replacement = save(http, state, [{"type": "delete", "sheet": "Deal ledger", "uid": uid2, "replacement_uid": uid3}], "Replace deleted reference")
    assert replacement.status_code == 200, replacement.text
    state = replacement.json()
    assert [r["uid"] for r in state["ledger"]["rows"]] == [uid1, uid3, new_uid]
    assert state["ledger"]["rows"][1]["cells"]["Note"] == "After #2"
    assert "#2" in state["questions"]["rows"][0]["cells"]["Rows affected"]
    assert workbook.exists() and hashlib.sha256(workbook.read_bytes()).hexdigest() == original_hash

    restored = save(http, state, [{"type": "restore", "target_revision": 0}], "Restore original snapshot")
    assert restored.status_code == 200, restored.text
    state = restored.json()
    assert state["workspace"]["revision"] == 4
    assert [r["uid"] for r in state["ledger"]["rows"]] == [uid1, uid2, uid3]
    assert state["ledger"]["rows"][2]["cells"]["Note"] == "After #2"
    history = http.get("/api/deal/synthetic/history").json()["history"]
    assert [item["revision"] for item in history] == [4, 3, 2, 1, 0]
    assert http.get("/api/deal/synthetic/changes").json()["changes"] == []


def test_same_batch_insert_references_client_uid_and_unknown_refs(env):
    http, _, _ = env
    initial = deal(http)
    uid1, uid2, uid3 = [r["uid"] for r in initial["ledger"]["rows"]]
    operations = [
        {"type": "insert", "sheet": "Deal ledger", "after_uid": uid1, "client_uid": "new-temporary-a", "values": {"Event": "Discarded synthetic A", "Note": "temporary"}},
        {"type": "insert", "sheet": "Deal ledger", "after_uid": "new-temporary-a", "client_uid": "new-temporary-b", "values": {"Event": "Kept synthetic B", "Note": "temporary"}},
        {"type": "move", "sheet": "Deal ledger", "uid": "new-temporary-a", "after_uid": "new-temporary-b"},
        {"type": "delete", "sheet": "Deal ledger", "uid": "new-temporary-a"},
        {"type": "update", "sheet": "Deal ledger", "uid": uid3, "values": {"Note": "see #2; unknown #999 remains"}},
    ]
    response = save(http, initial, operations, "Resolve client UIDs and original references")
    assert response.status_code == 200, response.text
    state = response.json()
    assert [r["cells"]["Event"] for r in state["ledger"]["rows"]] == ["Invitation", "Kept synthetic B", "Offer", "Signing"]
    assert state["ledger"]["rows"][2]["uid"] == uid2
    assert state["ledger"]["rows"][3]["uid"] == uid3
    assert state["ledger"]["rows"][3]["cells"]["Note"] == "see #3; unknown #999 remains"
    assert state["ledger"]["rows"][1]["uid"] not in ("new-temporary-a", "new-temporary-b")
    assert "#3" in state["questions"]["rows"][0]["cells"]["Rows affected"]
    assert "#4" in state["questions"]["rows"][0]["cells"]["Rows affected"]


def test_question_id_rename_updates_ledger_flags_and_duplicate_blocks(env):
    http, _, _ = env
    initial = deal(http)
    renamed = save(http, initial, [{"type": "update", "sheet": "Questions", "uid": row(initial, "Questions")["uid"], "values": {"Q": "Q2"}}], "Rename synthetic question")
    assert renamed.status_code == 200, renamed.text
    state = renamed.json()
    assert state["questions"]["rows"][0]["cells"]["Q"] == "Q2"
    assert [item["cells"]["Flag"] for item in state["ledger"]["rows"]] == ["", "Q2", "Q2"]
    duplicate = save(http, state, [{"type": "insert", "sheet": "Questions", "after_uid": row(state, "Questions")["uid"], "values": {"Q": "Q2", "Question": "Duplicate synthetic ID"}}], "Reject duplicate question")
    assert duplicate.status_code == 400, duplicate.text
    assert deal(http)["workspace"]["revision"] == 1


def test_unassessed_finding_implementation_is_attributed(env):
    http, _, _ = env
    initial = deal(http)
    decision = {"type": "finding", "id": "F1", "judgment": "deferred", "implementation": "unassessed", "verification": "unchecked", "note": "Synthetic source review pending"}
    response = save(http, initial, [decision], "Record provisional implementation state")
    assert response.status_code == 200, response.text
    finding = response.json()["findings"][0]
    assert finding["implementation"] == "unassessed"
    assert finding["judgment"] == "deferred"
    assert finding["actor"] == "local" and finding["at"]
    assert deal(http)["findings"][0]["implementation"] == "unassessed"


def test_post_round_can_be_edited_cloned_and_exported_as_text(env):
    http, _, _ = env
    initial = deal(http)
    event = row(initial, "Deal ledger", 2)
    post = save(http, initial, [{"type": "update", "sheet": "Deal ledger", "uid": event["uid"], "values": {"Round": "post", "Note": "Synthetic post-signing event"}}], "Mark synthetic post round")
    assert post.status_code == 200, post.text
    state = post.json()
    assert state["ledger"]["rows"][2]["cells"]["Round"] == "post"
    cloned = save(http, state, [{"type": "insert", "sheet": "Deal ledger", "after_uid": event["uid"], "client_uid": "new-post-clone", "values": {"When": "Date unknown", "Event": "Synthetic post clone", "Round": "post", "Count": "", "Date from": ""}}], "Clone post round event")
    assert cloned.status_code == 200, cloned.text
    state = cloned.json()
    assert state["ledger"]["rows"][3]["cells"]["Round"] == "post"
    exported = xlsx(http.get("/api/deal/synthetic/export?version=working"))
    column = check_lean.LEDGER_COLUMNS.index("Round") + 1
    assert exported["Deal ledger"].cell(4, column).value == "post"
    assert exported["Deal ledger"].cell(4, column).data_type == "s"
    assert exported["Deal ledger"].cell(5, column).value == "post"
    assert exported["Deal ledger"].cell(5, column).data_type == "s"
    exported.close()


def test_atomic_stale_formula_and_question_id_guards(env):
    http, _, _ = env
    initial = deal(http)
    uid = row(initial, "Deal ledger", 0)["uid"]
    base = {"revision": 0, "base_sha256": initial["workspace"]["base_sha256"], "reason": "Rejected batch"}
    invalid_batches = [
        [{"type": "update", "sheet": "Deal facts", "uid": row(initial, "Deal facts", 0)["uid"], "values": {"Value": "Would change"}}, {"type": "update", "sheet": "Questions", "uid": row(initial, "Questions")["uid"], "values": {"Q": "Q0"}}],
        [{"type": "update", "sheet": "Deal ledger", "uid": uid, "values": {"Nonexistent column": "x"}}],
    ]
    for ops in invalid_batches:
        response = http.edit({**base, "operations": ops})
        assert response.status_code == 400, response.text
        assert deal(http)["workspace"]["revision"] == 0
        assert row(deal(http), "Deal ledger")["cells"]["Note"] == "Three parties contacted"
    good = save(http, initial, [{"type": "update", "sheet": "Deal ledger", "uid": uid, "values": {"Note": "Saved once"}}])
    assert good.status_code == 200, good.text
    stale = save(http, initial, [{"type": "update", "sheet": "Deal ledger", "uid": uid, "values": {"Note": "Stale overwrite"}}])
    assert stale.status_code == 409, stale.text
    wrong_hash = http.edit({"revision": 1, "base_sha256": "0" * 64, "reason": "Wrong base", "operations": [{"type": "update", "sheet": "Deal ledger", "uid": uid, "values": {"Note": "Wrong base"}}]})
    assert wrong_hash.status_code == 409, wrong_hash.text
    assert row(deal(http), "Deal ledger")["cells"]["Note"] == "Saved once"

    literal = '=HYPERLINK("https://example.invalid", "not a link")'
    current = deal(http)
    edited = save(http, current, [{"type": "update", "sheet": "Deal ledger", "uid": uid, "values": {"Note": literal}}], "Literal formula-like source text")
    assert edited.status_code == 200, edited.text
    exported = xlsx(http.get("/api/deal/synthetic/export?version=working"))
    note = exported["Deal ledger"].cell(2, check_lean.LEDGER_COLUMNS.index("Note") + 1)
    original_formula = exported["Deal ledger"].cell(2, check_lean.LEDGER_COLUMNS.index("Reviewer note") + 1)
    assert note.value == literal and note.data_type == "s"
    assert original_formula.value == "=1+1" and original_formula.data_type == "f"
    exported.close()


def test_huge_range_is_bounded_without_state_change(env):
    http, _, _ = env
    initial = deal(http)
    payload = {"revision": 0, "base_sha256": initial["workspace"]["base_sha256"], "reason": "Reject huge range", "operations": [{"type": "update", "sheet": "Questions", "uid": row(initial, "Questions")["uid"], "values": {"Rows affected": "#1-#1000000000"}}]}
    started = time.monotonic()
    response = http.edit(payload)
    elapsed = time.monotonic() - started
    assert response.status_code == 400, response.text
    assert elapsed < 5, f"unbounded range validation took {elapsed:.1f}s"
    assert deal(http)["workspace"]["revision"] == 0


def test_session_security_origin_csrf_and_path_boundaries(env, monkeypatch):
    http, _, _ = env
    initial = deal(http)
    uid = row(initial, "Deal ledger")["uid"]
    payload = {"revision": 0, "base_sha256": initial["workspace"]["base_sha256"], "reason": "Security probe", "operations": [{"type": "update", "sheet": "Deal ledger", "uid": uid, "values": {"Note": "Must not save"}}]}
    assert http.session()["can_edit"] is True  # explicitly local test server
    denied = [
        http.edit(payload, csrf="wrong"),
        http.edit(payload, origin="https://evil.example"),
        http.edit(payload, origin="http://127.0.0.1:9999"),
        http.edit(payload, origin=http.base.replace("http://", "https://")),
        http.edit(payload, origin="https://evil.example", headers={"X-Forwarded-Host": "evil.example"}),
        http.edit(payload, origin="omit"),
        http.edit(payload, content_type="text/plain"),
        http.edit(payload, headers={"Host": "lines.example.invalid", "Origin": "https://lines.example.invalid"}),
        http.post("/api/deal/../synthetic/edit", payload),
        http.post("/api/deal/%2e%2e%2fsynthetic/edit", payload),
    ]
    assert all(response.status_code in (400, 403, 404, 405, 415) for response in denied), [(i, r.status_code, r.text[:120]) for i, r in enumerate(denied)]
    assert http.get("/api/document/synthetic/%2e%2e%2f%2e%2e%2fref%2fanswers").status_code == 404
    assert http.get("/assets/%2e%2e/%2e%2e/ref/answers").status_code == 404
    assert http.get("/api/deal/%2e%2e%2fsynthetic").status_code == 404
    oversized = http.post("/api/deal/synthetic/edit", {"padding": "x" * (server.MAX_JSON + 1)})
    assert oversized.status_code == 413, oversized.text[:200]
    assert deal(http)["workspace"]["revision"] == 0
    monkeypatch.setenv("COCKPIT_PUBLIC_ORIGIN", "https://lines.example.invalid")
    public_headers = {"Host": "lines.example.invalid", "Origin": "https://lines.example.invalid"}
    unknown = http.edit(payload, headers={**public_headers, "Cf-Access-Authenticated-User-Email": "intruder@example.invalid"})
    missing = http.edit(payload, headers=public_headers)
    assert unknown.status_code == 403 and missing.status_code == 403
    assert deal(http)["workspace"]["revision"] == 0
    # Synthetic request headers alone must not be reported as a real Cloudflare login test.


def test_catalog_allowlist_rejects_ref_and_symlink_escape(env):
    http, _, _ = env
    secret = "SYNTHETIC-SECRET-MUST-NOT-LEAK"
    ref = http.root / "ref"
    ref.mkdir()
    (ref / "secret.txt").write_text(secret, encoding="utf-8")
    catalog_path = http.root / "_dev/cockpit/catalog.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    doc = catalog["deals"]["synthetic"]["documents"][0]
    doc["path"] = "ref/secret.txt"
    catalog_path.write_text(json.dumps(catalog), encoding="utf-8")
    response = http.get("/api/document/synthetic/finding")
    assert response.status_code in (400, 404), response.text
    assert secret not in response.text

    outside = http.root.parent / (http.root.name + "-outside.txt")
    outside.write_text(secret, encoding="utf-8")
    try:
        link = http.root / "_dev/reviews/synthetic/escape.txt"
        link.symlink_to(outside)
        doc["path"] = "_dev/reviews/synthetic/escape.txt"
        catalog_path.write_text(json.dumps(catalog), encoding="utf-8")
        response = http.get("/api/document/synthetic/finding")
        assert response.status_code in (400, 404), response.text
        assert secret not in response.text
    finally:
        outside.unlink(missing_ok=True)


def test_instruction_versions_and_engines_over_http(env, monkeypatch):
    http, _, _ = env
    listing = http.get("/api/instructions").json()
    [base] = listing["items"]
    assert (base["name"], base["is_default"]) == ("v1.13.2", True)
    assert http.get("/instructions").status_code == 200
    assert http.get("/api/instructions/zzz").status_code == 404
    assert http.get(f"/api/instructions/{base['id']}?seq=x").status_code == 400
    draft = http.post("/api/instructions", {"action": "draft", "from": base["id"]})
    assert draft.status_code == 200, draft.text
    item = draft.json()["item"]
    saved = http.post("/api/instructions", {"action": "save", "id": item["id"], "text": "New text\n", "base_sha256": item["sha256"]})
    stale = http.post("/api/instructions", {"action": "save", "id": item["id"], "text": "Other\n", "base_sha256": item["sha256"]})
    assert (saved.status_code, stale.status_code) == (200, 409)
    assert http.get(f"/api/instructions/{item['id']}?seq=1").json()["text"] == draft.json()["text"]
    assert http.post("/api/instructions", {"action": "save", "id": item["id"], "text": "x"}, csrf="wrong").status_code == 403
    monkeypatch.setenv("COCKPIT_PUBLIC_ORIGIN", "https://lines.example.invalid")
    public = {"Host": "lines.example.invalid", "Origin": "https://lines.example.invalid", "Cf-Access-Authenticated-User-Email": "intruder@example.invalid"}
    assert http.post("/api/instructions", {"action": "default", "id": base["id"]}, headers=public).status_code == 403
    assert http.post("/api/account/chatgpt", {"action": "connect"}, headers=public).status_code == 403
    account = http.get("/api/account").json()
    assert [engine["id"] for engine in account["engines"]] == ["opus55", "fable51", "sol6", "astra6"]
    assert account["chatgpt"]["connected"] is False
    refused = http.post("/api/deal/synthetic/jobs", {"action": "extract", "engine": "sol6"})
    assert refused.status_code == 409 and "ChatGPT" in refused.json()["error"]
