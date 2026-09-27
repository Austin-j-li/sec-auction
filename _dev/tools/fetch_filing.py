#!/usr/bin/env python3
"""Fetch merger filings from SEC EDGAR into raw_filing/, using ref/seed.csv.

    python3 _dev/tools/fetch_filing.py penford stec     # fetch these deals
    python3 _dev/tools/fetch_filing.py --list penf      # show seed rows matching "penf"
    python3 _dev/tools/fetch_filing.py --verify         # re-download every filing in the manifest and compare

For each deal the script downloads the filing's complete submission text file,
cuts out the main document (the one whose type equals the seed's form type) and
saves its bytes unchanged as raw_filing/<deal>_<date filed>_<FORM>.htm. Every saved file gets a
line in raw_filing/MANIFEST.csv (source link, time, size, SHA-256). Files already
present are left alone unless --force is given.

For tender offers (SC TO-T), the offer-to-purchase exhibit EX-99.(A)(1)(A)
is saved instead of the cover form. Seed rows marked "review" are refused.

Standard library only. SEC asks for a named User-Agent and at most 10 requests
a second; this script makes at most 4.
"""
import argparse
import csv
import hashlib
import html
import io
import os
import re
import sys
import time
import tempfile
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SEED = ROOT / "ref" / "seed.csv"
RAW = ROOT / "raw_filing"
MANIFEST = RAW / "MANIFEST.csv"
MANIFEST_FIELDS = ["file", "deal", "form_type", "date_filed", "source_url", "document", "fetched_utc", "bytes", "sha256"]

USER_AGENT = os.environ.get("SEC_USER_AGENT", "Austin Li junyu.li.24@ucl.ac.uk")
MIN_GAP = 0.25  # seconds between requests
_last_request = [0.0]


class FetchError(Exception):
    pass


def get(url):
    wait = _last_request[0] + MIN_GAP - time.monotonic()
    if wait > 0:
        time.sleep(wait)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return resp.read()
        except OSError as e:  # URLError and HTTPError included
            code = getattr(e, "code", None)
            if attempt == 2 or (code is not None and code not in (429, 500, 502, 503)):
                raise FetchError("%s: %s" % (url, e))
            time.sleep(5 * (attempt + 1))
        finally:
            _last_request[0] = time.monotonic()


DOCUMENT_RE = re.compile(rb"<DOCUMENT>\n<TYPE>([^\n]*)\n.*?</DOCUMENT>", re.S)
ARCHIVE = r"https://www\.sec\.gov/Archives/edgar/data/(\d+)/"
INDEX_LINK = re.compile(ARCHIVE + r"(?:\d{18}/)?(\d{10}-\d{2}-\d{6})-index\.html?$")
SUBMISSION_LINK = re.compile(ARCHIVE + r"(?:\d{18}/)?(\d{10}-\d{2}-\d{6})\.txt$")
DOCUMENT_LINK = re.compile(ARCHIVE + r"(\d{18})/([A-Za-z0-9][A-Za-z0-9._-]*)$")
BACKGROUND = re.compile(r"background\s+of\s+the\s+(?:merger|offer|transaction|proposed|acquisition)", re.I)


def submission_link(url):
    """Return (complete submission link, document name or None) for an EDGAR archive link.

    Accepts a filing index page, the complete submission text file, or one document
    in the filing's folder. Anything else raises FetchError.
    """
    url = (url or "").strip().split("#")[0].split("?")[0].replace("http://", "https://", 1)
    for pattern in (INDEX_LINK, SUBMISSION_LINK):
        m = pattern.match(url)
        if m:
            return "https://www.sec.gov/Archives/edgar/data/%s/%s.txt" % m.groups(), None
    m = DOCUMENT_LINK.match(url)
    if m:
        cik, folder, name = m.groups()
        accession = "%s-%s-%s" % (folder[:10], folder[10:12], folder[12:])
        return "https://www.sec.gov/Archives/edgar/data/%s/%s.txt" % (cik, accession), name
    raise FetchError("not an EDGAR filing link: use a filing index (…-index.htm), a complete submission (.txt) "
                     "or a document under https://www.sec.gov/Archives/edgar/data/")


def index_link(url):
    """Return the filing index page for a complete submission link (…/<accession>.txt -> …/<accession>-index.htm).

    Anything but a complete submission link raises FetchError; the link is derived, never fetched.
    """
    m = SUBMISSION_LINK.match((url or "").strip())
    if not m:
        raise FetchError("not an EDGAR complete submission link (.txt): %s" % url)
    return "https://www.sec.gov/Archives/edgar/data/%s/%s-index.htm" % m.groups()


def _header_value(header, key):
    m = re.search(r"^\s*" + re.escape(key) + r":\s*(.+?)\s*$", header, re.M)
    return m.group(1) if m else ""


def parse_submission(data):
    """The header and document list of a complete submission text file."""
    head = data.split(b"<DOCUMENT>", 1)[0].decode("latin-1")
    filed = _header_value(head, "FILED AS OF DATE")
    names = {}
    for section in ("SUBJECT COMPANY", "FILER", "FILED BY"):
        m = re.search(r"^" + section + r":\s*$(.*?)(?=^\S|\Z)", head, re.M | re.S)
        if m:
            names[section] = _header_value(m.group(1), "COMPANY CONFORMED NAME")
    documents = []
    for m in DOCUMENT_RE.finditer(data):
        block = m.group(0)
        field = lambda tag: (re.search(rb"<" + tag + rb">([^\n]*)\n", block) or [None, b""])[1].decode("latin-1").strip()
        name = field(b"FILENAME")
        is_html = name.lower().endswith((".htm", ".html"))
        text = " ".join(html.unescape(re.sub(r"<[^>]*>", " ", block.decode("utf-8", "replace"))).split()) if is_html else ""
        documents.append({"type": m.group(1).decode("latin-1").strip(), "filename": name, "description": field(b"DESCRIPTION"),
                          "bytes": len(block) + 1, "html": is_html, "background": bool(BACKGROUND.search(text))})
    return {
        "form_type": _header_value(head, "CONFORMED SUBMISSION TYPE"),
        "date_filed": "%s-%s-%s" % (filed[:4], filed[4:6], filed[6:8]) if re.fullmatch(r"\d{8}", filed) else "",
        "subject_company": names.get("SUBJECT COMPANY", ""),
        "filer": names.get("FILER", "") or names.get("FILED BY", ""),
        "documents": documents,
    }


def default_document(documents, form_type):
    """The main document by the seed rule, or None when the rule does not pick exactly one."""
    wanted = "EX-99.(A)(1)(A)" if form_type == "SC TO-T" else form_type if form_type in ("DEFM14A", "PREM14A") else None
    hits = [d["filename"] for d in documents if wanted and d["type"] == wanted and d["html"]]
    return hits[0] if len(hits) == 1 else None


def document_bytes(data, filename):
    """The saved bytes of one named document: its <DOCUMENT> block and a newline."""
    hits = [m.group(0) + b"\n" for m in DOCUMENT_RE.finditer(data)
            if (re.search(rb"<FILENAME>([^\n]*)\n", m.group(0)) or [None, b""])[1].decode("latin-1").strip() == filename]
    if len(hits) != 1:
        raise FetchError("expected one document named %s, found %d" % (filename, len(hits)))
    return hits[0]


def main_document(index_url, form_type, document=None):
    """Return (submission link, document name, document bytes) for the selected document.

    The document is cut out of the filing's complete submission text file, not
    downloaded as a web page: EDGAR adds a tracking script to the HTML pages it
    serves, so a page download is not the filing as filed. The text file is
    served untouched, and a document block from it equals the served page minus
    that script. Tender offers use the offer-to-purchase exhibit. If a manifest
    filename is supplied, require that exact document as well as its type.
    """
    document_type = "EX-99.(A)(1)(A)" if form_type == "SC TO-T" else form_type
    url = re.sub(r"-index\.html?$", ".txt", index_url)
    text = get(url)
    hits = []
    for m in DOCUMENT_RE.finditer(text):
        if m.group(1).decode("ascii", "replace").strip() != document_type:
            continue
        name = re.search(rb"<FILENAME>([^\n]*)\n", m.group(0))
        name = name.group(1).decode("ascii", "replace").strip() if name else ""
        if not document or name == document:
            hits.append((name, m.group(0) + b"\n"))
    if len(hits) != 1:
        wanted = document_type + (" named " + document if document else "")
        raise FetchError("%s: expected one %s document, found %d" % (url, wanted, len(hits)))
    name, data = hits[0]
    if not name.lower().endswith((".htm", ".html")):
        raise FetchError("%s: main document is not HTML (%s)" % (url, name or "no name"))
    return url, name, data


def read_csv(path):
    if not path.exists():
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def atomic_write(path, data):
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix="." + path.name, delete=False) as handle:
        temporary = Path(handle.name)
        try:
            handle.write(data)
            handle.close()
            temporary.chmod(0o644)  # NamedTemporaryFile makes 0600
            temporary.replace(path)
        finally:
            temporary.unlink(missing_ok=True)


def write_manifest(rows):
    rows.sort(key=lambda r: r["file"])
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=MANIFEST_FIELDS)
    writer.writeheader()
    writer.writerows(rows)
    atomic_write(MANIFEST, buffer.getvalue().encode("utf-8"))


def fetch(seed_row, manifest, force):
    deal = seed_row["deal"]
    if seed_row["status"] != "ok":
        raise FetchError("%s: seed row needs review first (%s)" % (deal, seed_row["status"]))
    name = "%s_%s_%s.htm" % (deal, seed_row["date_filed"], seed_row["form_type"].replace(" ", ""))
    path = RAW / name
    recorded = next((r for r in manifest if r["file"] == name), None)
    if path.exists() and recorded and not force:
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != recorded["sha256"] or len(data) != int(recorded["bytes"]):
            raise FetchError("%s: local file differs from its manifest; inspect it or use --force to refetch" % name)
        return "%s: already present; local hash verified" % name

    url, document, data = main_document(seed_row["index_url"], seed_row["form_type"])
    if path.exists() and not force:  # a file from before the manifest: keep it, record what EDGAR has now
        if path.read_bytes() != data:
            raise FetchError("%s: differs from EDGAR's copy; rerun with --force to replace it" % name)
        note = "%s: existing file matches EDGAR byte for byte; recorded" % name
    else:
        atomic_write(path, data)
        note = "%s: saved, %d bytes" % (name, len(data))
    manifest[:] = [r for r in manifest if r["file"] != name]
    manifest.append({
        "file": name, "deal": deal, "form_type": seed_row["form_type"], "date_filed": seed_row["date_filed"],
        "source_url": url, "document": document, "fetched_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
    })
    write_manifest(manifest)
    return note


def verify(manifest):
    bad = 0
    for r in manifest:
        path = RAW / r["file"]
        local = hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None
        index_url = index_link(r["source_url"])
        remote = hashlib.sha256(main_document(index_url, r["form_type"], r.get("document"))[2]).hexdigest()
        ok = local == r["sha256"] == remote
        bad += not ok
        print("%-60s %s" % (r["file"], "ok" if ok else "MISMATCH (local %s, EDGAR %s)" % (
            "missing" if local is None else "same as manifest" if local == r["sha256"] else "changed",
            "same as manifest" if remote == r["sha256"] else "changed")))
    return bad


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("deals", nargs="*", help="short names from the deal column of ref/seed.csv")
    ap.add_argument("--list", metavar="TEXT", help="show seed rows whose short or target name contains TEXT")
    ap.add_argument("--verify", action="store_true", help="re-download every manifest entry and compare hashes")
    ap.add_argument("--force", action="store_true", help="replace files that are already present")
    args = ap.parse_args()

    seed = read_csv(SEED)
    if not seed:
        sys.exit("ref/seed.csv is missing; run _dev/tools/make_seed.py")
    manifest = read_csv(MANIFEST)

    if args.list is not None:
        text = args.list.lower()
        for r in seed:
            if text in r["deal"] or text in r["target_name"].lower():
                print("%-34s %-8s %s  %s" % (r["deal"], r["form_type"], r["date_filed"], r["status"]))
        return
    if args.verify:
        sys.exit(1 if verify(manifest) else 0)
    if not args.deals:
        ap.error("name at least one deal, or use --list or --verify")

    by_name = {r["deal"]: r for r in seed}
    failed = 0
    for deal in args.deals:
        try:
            if deal not in by_name:
                raise FetchError("%s: not in ref/seed.csv (try --list)" % deal)
            print(fetch(by_name[deal], manifest, args.force))
        except FetchError as e:
            failed += 1
            print("FAILED " + str(e), file=sys.stderr)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
