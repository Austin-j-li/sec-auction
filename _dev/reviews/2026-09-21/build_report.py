#!/usr/bin/env python3
"""Package reviewed Markdown and verified coverage using the report contract."""

import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
DEALS = ["petsmart", "penford", "providence-worcester", "mac-gray", "kraton", "stec", "synacor", "meredith"]
TITLE = "SEC extraction quality review"
VERDICTS_SQL = """-- :verdicts contains case_verdicts.json; this query presents reviewed judgments.
SELECT json_extract(value, '$.deal') AS deal,
       json_extract(value, '$.case') AS "case",
       json_extract(value, '$.verdict') AS verdict,
       json_extract(value, '$.main_issue') AS main_issue,
       json_extract(value, '$.reference') AS reference,
       json_extract(value, '$.priority') AS priority
FROM json_each(:verdicts)
ORDER BY priority"""
COVERAGE_SQL = """-- :verification contains input_verification.json; :verdicts contains case_verdicts.json.
SELECT json_extract(v.value, '$.case') AS "case",
       json_extract(c.value, '$.ledger_events') AS ledger_events
FROM json_each(:verification, '$.cases') AS c
JOIN json_each(:verdicts) AS v
  ON json_extract(c.value, '$.deal') = json_extract(v.value, '$.deal')
ORDER BY ledger_events DESC"""


def read_json(name):
    return json.loads((BASE / name).read_text())


def portable_text(text):
    text = re.sub(r"/tmp/sec-extraction-review-20260921(?:/[\w.-]+)*/?", "numbered source exports", text)
    text = re.sub(r"\[([^\]]+)\]\((?:[^)]+\.md)\)", r"\1", text)
    return text


def case_body(name, title):
    lines = (BASE / f"{name}.md").read_text().splitlines()
    if lines and lines[0].startswith("# "):
        lines.pop(0)
    text = "\n".join(lines).strip()
    text = re.sub(r"^(#{2,5}) ", r"\1# ", text, flags=re.M)
    return portable_text(f"## {title}\n\n{text}")


def main():
    verification = read_json("input_verification.json")
    verdicts = read_json("case_verdicts.json")
    parameters = {"verification": json.dumps(verification), "verdicts": json.dumps(verdicts)}
    with sqlite3.connect(":memory:") as connection:
        connection.row_factory = sqlite3.Row
        verdicts = [dict(row) for row in connection.execute(VERDICTS_SQL, parameters)]
        coverage = [dict(row) for row in connection.execute(COVERAGE_SQL, parameters)]
    now = datetime.now(timezone.utc).isoformat()
    sources = [
        {"id": "summary", "label": "Review synthesis and adjudicated case verdicts", "path": "_dev/reviews/2026-09-21/README.md"},
        {"id": "coverage", "label": "Verified v1.11 workbook coverage and source hashes", "path": "_dev/reviews/2026-09-21/input_verification.json", "query": {"sql": COVERAGE_SQL}},
        {"id": "verdict-data", "label": "Reviewed case verdicts; SQL only projects these judgments for display", "path": "_dev/reviews/2026-09-21/case_verdicts.json", "query": {"sql": VERDICTS_SQL}},
        {"id": "reference-audit", "label": "Alex reference provenance audit", "path": "_dev/reviews/2026-09-21/alex_reference_audit.md"},
        {"id": "adjudication", "label": "Independent challenge of material findings", "path": "_dev/reviews/2026-09-21/adjudication.md"},
        {"id": "voice", "label": "Alex August voice notes", "path": "ref/alex_voice_notes_2026-08.docx"},
        {"id": "older-instructions", "label": "Alex older collection instructions", "path": "ref/CollectionInstructions_Alex_2026.pdf"},
        {"id": "older-workbook", "label": "Alex reference workbook including inherited RA records", "path": "ref/deal_details_Alex_2026.xlsx"},
        {"id": "current-instruction", "label": "Current v1.11 extraction instruction", "path": "SEC_Deal_Ledger_Extraction_Instruction.md"},
    ]
    blocks = [{"id": "title", "type": "markdown", "body": f"# {TITLE}"}]
    summary = (BASE / "README.md").read_text()
    summary = re.sub(r"^# [^\n]+\n", "", summary, count=1).strip()
    sections = re.split(r"(?=^## )", summary, flags=re.M)
    for index, section in enumerate(sections):
        if section.strip():
            blocks.append({"id": f"summary-{index}", "type": "markdown", "body": portable_text(section.strip()), "sourceId": "summary"})
    blocks += [
        {"id": "case-table-heading", "type": "markdown", "body": "## Case verdicts\n\nEach verdict describes the corrections and decisions still needed for research use. A strong extraction is not a certification of every unobserved bidder state."},
        {"id": "case-table", "type": "table", "tableId": "verdicts"},
        {"id": "coverage-heading", "type": "markdown", "body": "## Coverage of the review\n\nThe reviewers read every ledger event, round, question and deal-fact entry across the eight workbooks, plus each complete filing background and relevant other sections. The chart shows the number of extracted events inspected, not an accuracy score, a count of true source events, or a measure of review difficulty. All eight saved mechanical checks had zero errors; those checks establish structure and quotation occurrence only.", "sourceId": "coverage"},
        {"id": "coverage-chart", "type": "chart", "chartId": "coverage"},
    ]
    names = {row["deal"]: row["case"] for row in verdicts}
    for deal in DEALS:
        sources.append({"id": deal, "label": f"{names[deal]} complete case evidence and findings", "path": f"_dev/reviews/2026-09-21/{deal}.md"})
        sources.append({"id": f"{deal}-workbook", "label": f"{names[deal]} reviewed v1.11 workbook", "path": f"extraction/{deal}.xlsx"})
        filing = next(name for name in verification["sources"] if name.startswith(f"raw_filing/{deal}_"))
        sources.append({"id": f"{deal}-filing", "label": f"{names[deal]} supplied SEC filing", "path": filing})
        blocks.append({"id": f"case-{deal}", "type": "markdown", "body": case_body(deal, names[deal]), "sourceId": deal})
    blocks.append({"id": "reference-details", "type": "markdown", "body": case_body("alex_reference_audit", "Reference provenance and interpretation"), "sourceId": "reference-audit"})
    blocks.append({"id": "challenge-details", "type": "markdown", "body": case_body("adjudication", "Independent challenge of the material findings"), "sourceId": "adjudication"})
    artifact = {
        "surface": "report",
        "manifest": {
            "version": 1, "surface": "report", "title": TITLE, "generatedAt": now,
            "blocks": blocks, "sources": sources,
            "tables": [{
                "id": "verdicts", "title": "Verdicts for the eight extractions", "dataset": "verdicts",
                "sourceId": "verdict-data", "defaultSort": {"field": "priority", "direction": "asc"},
                "density": "spacious", "layout": "full",
                "columns": [{"field": key, "label": label, "type": "text"} for key, label in [("case", "Case"), ("verdict", "Verdict"), ("main_issue", "Main remaining issue"), ("reference", "Older reference provenance")]] + [{"field": "priority", "label": "Review order", "format": "number"}],
            }],
            "charts": [{
                "id": "coverage", "title": "Ledger events reviewed", "subtitle": "Existing v1.11 rows per case; coverage, not accuracy",
                "showDescription": True, "type": "bar", "dataset": "coverage", "sourceId": "coverage", "layout": "full",
                "encodings": {"x": {"field": "case", "type": "nominal", "label": "Case"}, "y": {"field": "ledger_events", "type": "quantitative", "label": "Ledger events", "format": "number"}},
                "settings": {"orientation": "horizontal", "showValues": True, "sort": "descending"},
                "palette": {"kind": "sequential", "name": "blue"},
            }],
        },
        "snapshot": {"version": 1, "generatedAt": now, "status": "ready", "datasets": {"verdicts": verdicts, "coverage": coverage}},
        "sources": sources,
    }
    (BASE / "artifact.json").write_text(json.dumps(artifact, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"blocks": len(blocks), "case_reports": len(DEALS), "sources": len(sources), "artifact_bytes": (BASE / "artifact.json").stat().st_size}))


if __name__ == "__main__":
    main()
