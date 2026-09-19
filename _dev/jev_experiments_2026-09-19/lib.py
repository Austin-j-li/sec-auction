"""Shared helpers for the Jev experiments: filing paragraphs, quote location, API calls."""
import json, os, re, time, hashlib, unicodedata
from pathlib import Path
import httpx, openpyxl
from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
RAW = HERE / "raw"
FILINGS = {p.name.split("_")[0]: p for p in (ROOT / "raw_filing").glob("*.htm")}
MODEL = "jev-1.13.0"


def norm(s):
    s = unicodedata.normalize("NFKC", s or "")
    s = s.replace("“", '"').replace("”", '"').replace("’", "'").replace("‘", "'")
    s = re.sub(r"[‐-―]", "-", s)
    return re.sub(r"\s+", " ", s).strip()


def paragraphs(deal):
    """Background-section paragraphs of the filing, in order."""
    soup = BeautifulSoup(FILINGS[deal].read_bytes(), "lxml")
    paras = []
    for el in soup.find_all(["p", "div", "td"]):
        if el.find(["p", "div", "td", "table"]):
            continue
        t = norm(el.get_text(" "))
        if len(t) > 40 or re.fullmatch(r"(background of the (merger|offer)|reasons for the merger.*|recommendation of .*)", t, re.I):
            paras.append(t)
    heads = [i for i, t in enumerate(paras) if re.fullmatch(r"background of the (merger|offer)", t, re.I)]
    start = heads[-1] + 1
    end = next(i for i in range(start, len(paras)) if len(paras[i]) < 120 and re.match(r"(reasons for the merger|recommendation of)", paras[i], re.I))
    return paras, (start, end)


def quotes(cell):
    qs = [norm(q) for q in re.findall(r"“(.+?)”", cell or "", flags=re.S)]
    if not qs and cell:  # unquoted style: text followed by (p. N)
        qs = [norm(x) for x in re.split(r"\(pp?\.[^)]*\)", cell) if len(x.strip()) > 15]
    return qs


def locate(paras, q):
    """Index of the paragraph containing quote q (tolerating ellipses), else None."""
    parts = [p.strip() for p in re.split(r"\.\.\.|…|\[[^\]]*\]", q) if len(p.strip()) > 15]
    if not parts:
        return None
    for i, t in enumerate(paras):
        if all(p.lower() in t.lower() for p in parts):
            return i
    key = max(parts, key=len)[:60].lower()
    for i, t in enumerate(paras):
        if key in t.lower():
            return i
    return None


def ledger(path):
    ws = openpyxl.load_workbook(path, data_only=True)["Deal ledger"]
    rows = list(ws.iter_rows(values_only=True))
    hdr = [str(h).strip() for h in rows[0]]
    out = []
    for n, r in enumerate(rows[1:], start=2):
        if any(v not in (None, "") for v in r):
            d = {h: (v.strftime("%Y-%m-%d") if hasattr(v, "strftime") else v) for h, v in zip(hdr, r)}
            d["_sheet_row"] = n
            out.append(d)
    return out


_client = None
def ask(state, questions, tag):
    """One System One call; raw request/response cached under raw/ by content hash."""
    global _client
    body = {"state": state, "model": MODEL, "questions": questions}
    h = hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()[:16]
    f = RAW / f"{tag}_{h}.json"
    if f.exists():
        return json.loads(f.read_text())["response"]
    if _client is None:
        _client = httpx.Client(timeout=120, headers={"Authorization": "Bearer " + os.environ["TYPESAFE_API_KEY"]})
    for attempt in range(6):
        t0 = time.time()
        r = _client.post("https://api.typesafe.ai/v1/systemone", json=body)
        if r.status_code in (429, 500, 502, 503, 504):
            time.sleep(float(r.headers.get("retry-after", 2 ** attempt)))
            continue
        break
    if r.status_code != 200:
        raise RuntimeError(f"{r.status_code}: {r.text[:500]}")
    resp = r.json()
    f.write_text(json.dumps({"request": body, "response": resp, "latency_s": round(time.time() - t0, 3)}, indent=1))
    return resp
