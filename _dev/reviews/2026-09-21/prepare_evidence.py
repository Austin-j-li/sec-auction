#!/usr/bin/env python3
"""Read-only source exports for the September 2026 extraction quality review."""

import argparse
import hashlib
import json
import re
import subprocess
import zipfile
from datetime import date, datetime
from pathlib import Path
from xml.etree import ElementTree

import openpyxl
from bs4 import BeautifulSoup, NavigableString, Tag


ROOT = Path(__file__).resolve().parents[3]
DEALS = (
    "kraton", "mac-gray", "meredith", "penford", "petsmart",
    "providence-worcester", "stec", "synacor",
)


def scalar(value):
    return value.isoformat() if isinstance(value, (date, datetime)) else value


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def workbook_export(path):
    workbook = openpyxl.load_workbook(path, read_only=True, data_only=False)
    result = {}
    for sheet in workbook:
        rows = []
        for row in sheet:
            cells = {cell.coordinate: scalar(cell.value) for cell in row if cell.value is not None}
            if cells:
                rows.append(cells)
        result[sheet.title] = rows
    workbook.close()
    return result


def normalized(value):
    return re.sub(r"[^a-z0-9]", "", str(value).lower())


def filing_paragraphs(path):
    soup = BeautifulSoup(path.read_bytes(), "lxml")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    blocks = {"p", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6"}

    def walk(node):
        if isinstance(node, NavigableString):
            text = " ".join(str(node).split())
            if text:
                yield text
        elif isinstance(node, Tag):
            if node.name in blocks or (node.name == "div" and not node.find(list(blocks) + ["div"])):
                text = " ".join(node.get_text(" ", strip=True).split())
                if text:
                    yield text
            else:
                for child in node.children:
                    yield from walk(child)

    return list(walk(soup.body or soup))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    out = args.output
    out.mkdir(parents=True, exist_ok=True)
    manifest = {"root": str(ROOT), "sources": {}, "workbooks": {}, "reference": {}}
    source_paths = [ROOT / "SEC_Deal_Ledger_Extraction_Instruction.md"]
    source_paths += list((ROOT / "ref").glob("*"))
    source_paths += list((ROOT / "raw_filing").glob("*"))
    source_paths += list((ROOT / "extraction").glob("*.xlsx"))
    for path in source_paths:
        if path.is_file():
            manifest["sources"][str(path.relative_to(ROOT))] = {"sha256": digest(path), "bytes": path.stat().st_size}

    voice = ROOT / "ref/alex_voice_notes_2026-08.docx"
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    with zipfile.ZipFile(voice) as archive:
        doc = ElementTree.fromstring(archive.read("word/document.xml"))
        elements = doc.findall(".//w:p", ns)
        elements = [p for p in elements if "".join(t.text or "" for t in p.findall(".//w:t", ns)).strip()]
        paragraphs = ["".join(t.text or "" for t in p.findall(".//w:t", ns)) for p in elements]
        (out / "alex_voice_notes.txt").write_text("\n".join(f"V{i:04d} {p}" for i, p in enumerate(paragraphs, 1)) + "\n")
        formatted = []
        for i, element in enumerate(elements, 1):
            runs = []
            for run in element.findall(".//w:r", ns):
                color = run.find("w:rPr/w:color", ns)
                runs.append({"text": "".join(t.text or "" for t in run.findall(".//w:t", ns)), "color": None if color is None else color.attrib})
            formatted.append({"paragraph": f"V{i:04d}", "runs": runs})
        write_json(out / "alex_voice_formatting.json", formatted)
        manifest["reference"]["voice_paragraphs"] = len(paragraphs)
        manifest["reference"]["voice_has_tracked_changes"] = bool(doc.findall(".//w:ins", ns) or doc.findall(".//w:del", ns))
        manifest["reference"]["voice_has_comments"] = "word/comments.xml" in archive.namelist()
        if "word/comments.xml" in archive.namelist():
            comments = ElementTree.fromstring(archive.read("word/comments.xml"))
            write_json(out / "alex_voice_comments.json", [{"metadata": element.attrib, "text": " ".join(t.text or "" for t in element.findall(".//w:t", ns))} for element in comments])

    subprocess.run(["pdftotext", "-layout", str(ROOT / "ref/CollectionInstructions_Alex_2026.pdf"), str(out / "alex_collection_instructions.txt")], check=True)
    reference = workbook_export(ROOT / "ref/deal_details_Alex_2026.xlsx")
    reference_summary = {}
    for sheet, rows in reference.items():
        reference_summary[sheet] = {"nonempty_rows": len(rows), "first_rows": rows[:2]}
    write_json(out / "alex_workbook_inventory.json", reference_summary)

    for deal in DEALS:
        folder = out / deal
        folder.mkdir(exist_ok=True)
        workbook = workbook_export(ROOT / "extraction" / f"{deal}.xlsx")
        write_json(folder / "workbook.json", workbook)
        lines = []
        for sheet, rows in workbook.items():
            lines.append(f"## {sheet}")
            for row in rows:
                lines.append(json.dumps(row, ensure_ascii=False))
        (folder / "workbook.txt").write_text("\n".join(lines) + "\n")
        manifest["workbooks"][deal] = {sheet: len(rows) for sheet, rows in workbook.items()}
        matches = {}
        for sheet, rows in reference.items():
            selected = [row for row in rows[1:] if any(normalized(deal) in normalized(value) for value in row.values() if isinstance(value, str))]
            if selected:
                matches[sheet] = {"headers": rows[0], "rows": selected}
        write_json(folder / "alex_handcoded.json", matches)
        manifest["reference"][deal] = {sheet: len(value["rows"]) for sheet, value in matches.items()}
        filing = next((ROOT / "raw_filing").glob(f"{deal}_*.htm"))
        paragraphs = filing_paragraphs(filing)
        (folder / "filing.txt").write_text("\n".join(f"P{i:05d} {p}" for i, p in enumerate(paragraphs, 1)) + "\n")
        headings = [f"P{i:05d} {p[:220]}" for i, p in enumerate(paragraphs, 1) if re.search(r"background|reasons for|projections|certain information|parties to|purpose of|past contacts|negotiations|financial forecast", p, re.I)]
        (folder / "filing_index.txt").write_text("\n".join(headings) + "\n")
    write_json(out / "manifest.json", manifest)
    print(json.dumps({"output": str(out), "workbooks": manifest["workbooks"], "reference": manifest["reference"]}, indent=2))


if __name__ == "__main__":
    main()
