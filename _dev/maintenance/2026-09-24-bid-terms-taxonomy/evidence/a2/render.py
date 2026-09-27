"""Render a DOCX for visual inspection: DOCX -> HTML (mammoth) -> PDF (headless Chrome) -> PNG (pdftoppm).

Usage: python render.py <file.docx> <out_dir> [--prefix page]

This approximates Word's layout: mammoth keeps paragraphs, headings, tables and
bold, but not Word's fonts, shading, column widths or row heights, so the CSS
below restores the main ones by hand.
"""

import argparse
import re
import subprocess
import tempfile
from pathlib import Path

import mammoth

STYLE_MAP = """
p[style-name='Title'] => h1.title:fresh
p[style-name='Byline'] => p.byline:fresh
p[style-name='Excerpt'] => p.excerpt:fresh
p[style-name='Small'] => p.small:fresh
p[style-name='List Bullet'] => ul > li:fresh
r[style-name='Reference'] => span.ref
"""

CSS = """
@page { size: 8.5in 11in; margin: 0.8in 0.9in; }
body { font-family: Georgia, Gelasio, serif; font-size: 10.5pt; color: #1F2A37; line-height: 1.3; }
h1.title { font-size: 20pt; color: #1F4E79; margin: 0 0 2pt; }
h1 { font-size: 14pt; color: #1F4E79; margin: 14pt 0 5pt; break-after: avoid; }
h2 { font-size: 11.5pt; color: #1F4E79; margin: 10pt 0 3pt; break-after: avoid; }
h3 { font-size: 10.5pt; color: #1F4E79; margin: 8pt 0 2pt; break-after: avoid; }
p { margin: 0 0 6pt; }
p.byline { color: #5A6472; font-size: 11pt; margin-bottom: 12pt; }
p.small { color: #5A6472; font-size: 9pt; }
p.excerpt { font-size: 9pt; margin: 0 0 3pt 0.25in; }
span.ref { font-size: 7.5pt; color: #5A6472; }
ul { margin: 0 0 4pt; }
table { border-collapse: collapse; width: 100%; margin: 2pt 0 8pt; }
td, th { border: 0.5pt solid #A9B4C2; padding: 3pt 5pt; vertical-align: top; font-size: 9pt; text-align: left; }
th { background: #E4EBF2; color: #1F4E79; }
td p, th p { margin: 0 0 2pt; white-space: pre-wrap; }
td[colspan] { background: #F4F6F8; height: 0.42in; }
table:not(:has(th)) td { background: #F4F6F8; height: 0.5in; }
tr { break-inside: avoid; }
tr:has(+ tr > td[colspan]) { break-after: avoid; }  /* a 2b item stays with its comment row */
table:not(:has(td[colspan])) { break-inside: avoid; }  /* short tables stay on one page, as keep-with-next does in Word */
"""


# Word's fixed column widths (inches, as in build_docx.py), keyed by the first header cell.
WIDTHS = {"Rule": (2.75, 2.45, 1.5), "#": (0.3, 2.55, 1.95, 1.35, 0.55), "Round": (0.6, 3.05, 3.05), "Reading": (0.7, 3.2, 1.3, 1.5)}


def _colgroup(match):
    widths = WIDTHS.get(match.group(2).strip())
    if not widths:
        return match.group(0)
    cols = "".join(f"<col style='width:{w / sum(widths) * 100:.1f}%'>" for w in widths)
    return f"<table style='table-layout:fixed'><colgroup>{cols}</colgroup>{match.group(1)}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("docx", type=Path)
    parser.add_argument("out_dir", type=Path)
    parser.add_argument("--prefix", default="page")
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    with args.docx.open("rb") as handle:
        result = mammoth.convert_to_html(handle, style_map=STYLE_MAP)
    for message in result.messages:
        print("mammoth:", message)
    html_body = re.sub(r"<table>(<thead><tr><th><p>(?:<strong>)?([^<]*))", _colgroup, result.value)
    work = Path(tempfile.mkdtemp())
    html = work / "doc.html"
    html.write_text(f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head>"
                    f"<body>{html_body}</body></html>", encoding="utf-8")
    pdf = args.out_dir / f"{args.prefix}.pdf"
    subprocess.run(["/opt/google/chrome/chrome", "--headless", "--disable-gpu", "--no-sandbox",
                    "--no-pdf-header-footer", f"--print-to-pdf={pdf}", html.as_uri()],
                   check=True, capture_output=True, timeout=90)  # Chrome keeps its temporary profile under TMPDIR
    subprocess.run(["pdftoppm", "-png", "-r", "80", str(pdf), str(args.out_dir / args.prefix)], check=True)
    print(f"rendered {pdf} and {len(list(args.out_dir.glob(args.prefix + '-*.png')))} pages")


if __name__ == "__main__":
    main()
