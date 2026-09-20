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

Tender offers (SC TO-T) are refused for now: their background section is in an
exhibit, not the main document. Seed rows marked "review" are refused too.

Standard library only. SEC asks for a named User-Agent and at most 10 requests
a second; this script makes at most 4.
"""
import argparse
import csv
import hashlib
import re
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SEED = ROOT / "ref" / "seed.csv"
RAW = ROOT / "raw_filing"
MANIFEST = RAW / "MANIFEST.csv"
MANIFEST_FIELDS = ["file", "deal", "form_type", "date_filed", "source_url", "document", "fetched_utc", "bytes", "sha256"]

USER_AGENT = "Austin Li junyu.li.24@ucl.ac.uk"
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


def main_document(index_url, form_type):
    """Return (submission link, document name, document bytes) for the filing's main document.

    The document is cut out of the filing's complete submission text file, not
    downloaded as a web page: EDGAR adds a tracking script to the HTML pages it
    serves, so a page download is not the filing as filed. The text file is
    served untouched, and a document block from it equals the served page minus
    that script.
    """
    url = re.sub(r"-index\.html?$", ".txt", index_url)
    text = get(url)
    hits = []
    for m in re.finditer(rb"<DOCUMENT>\n<TYPE>([^\n]*)\n.*?</DOCUMENT>", text, re.S):
        if m.group(1).decode("ascii", "replace").strip() == form_type:
            hits.append(m.group(0) + b"\n")
    if len(hits) != 1:
        raise FetchError("%s: expected one %s document, found %d" % (url, form_type, len(hits)))
    name = re.search(rb"<FILENAME>([^\n]*)\n", hits[0])
    name = name.group(1).decode("ascii", "replace").strip() if name else ""
    if not name.lower().endswith((".htm", ".html")):
        raise FetchError("%s: main document is not HTML (%s)" % (url, name or "no name"))
    return url, name, hits[0]


def read_csv(path):
    if not path.exists():
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_manifest(rows):
    rows.sort(key=lambda r: r["file"])
    with open(MANIFEST, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=MANIFEST_FIELDS)
        w.writeheader()
        w.writerows(rows)


def fetch(seed_row, manifest, force):
    deal = seed_row["deal"]
    if seed_row["status"] != "ok":
        raise FetchError("%s: seed row needs review first (%s)" % (deal, seed_row["status"]))
    if seed_row["form_type"] == "SC TO-T":
        raise FetchError("%s: tender offers are not handled yet" % deal)
    name = "%s_%s_%s.htm" % (deal, seed_row["date_filed"], seed_row["form_type"].replace(" ", ""))
    path = RAW / name
    recorded = any(r["file"] == name for r in manifest)
    if path.exists() and recorded and not force:
        return "%s: already present" % name

    url, document, data = main_document(seed_row["index_url"], seed_row["form_type"])
    if path.exists() and not force:  # a file from before the manifest: keep it, record what EDGAR has now
        if path.read_bytes() != data:
            raise FetchError("%s: differs from EDGAR's copy; rerun with --force to replace it" % name)
        note = "%s: existing file matches EDGAR byte for byte; recorded" % name
    else:
        path.write_bytes(data)
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
        index_url = r["source_url"][:-len(".txt")] + "-index.htm"
        remote = hashlib.sha256(main_document(index_url, r["form_type"])[2]).hexdigest()
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
