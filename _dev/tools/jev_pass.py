#!/usr/bin/env python3
"""Optional second-reader pass for check_lean.py, using TypeSafe's Jev model.

Two checks, both read-only and both producing review leads, never verdicts:

* price: for each priced ledger row whose quotation can be located, ask whether
  the quoted paragraph (plus two either side) supports that price for that
  party at that event.
* omission: tag Background paragraphs, then their sentences, by event kind; for
  each event sentence ask which nearby ledger row records it, or ``none``.

Question wording, passage width and the confidence cuts come from the round 1-3
experiments (``_dev/jev_checker/RESULTS_round*.md``) and were read off three
development deals with ``jev-1.13.0``. Change them only with a new experiment.

The API key is read from the TYPESAFE_API_KEY environment variable and is never
written anywhere. Responses are cached by request content under ``.jev_cache/``
so a rerun makes no new calls.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import time
import unicodedata
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

import openpyxl
from bs4 import BeautifulSoup

MODEL = "jev-1.13.0"
API_URL = "https://api.typesafe.ai/v1/systemone"
DEFAULT_CACHE = Path(__file__).resolve().parent / ".jev_cache"
TOP_TIER = 0.9
SECOND_TIER = 0.75

KINDS = {
    "bid": "a bidder submits, revises, confirms or reaffirms a priced proposal, indication of interest or offer for the company",
    "nda_access": "a party signs a confidentiality agreement, or is given (or denied) data room access, management meetings, projections or other diligence information",
    "exit": "a potential buyer withdraws, declines to bid, is told it will not advance, or is otherwise excluded from the process",
    "deadline": "the target or its banker sets, changes or communicates a bid deadline, process letter or request for final offers",
    "contact": "the target or its banker contacts potential buyers, or a potential buyer approaches the target, including counts of parties contacted",
    "adviser": "a financial or legal adviser is retained, engaged, terminated or first shown acting for the target, a committee or a bidder",
    "exclusivity": "exclusivity is requested, authorised, granted, signed or extended",
    "agreements": "a voting, support or rollover agreement, a special committee, or the merger agreement itself is formed, approved or signed",
}

SUPPORT = {
    "supported": "The source states this price (or range) for this party at this specific event. Trailing zeros and wording may differ.",
    "contradicted": "The source describes this specific event by this party and gives a different price or range for it, or the claimed figure belongs to another party, another event, or only one component of the package.",
    "insufficient": "The source does not state a price for this specific event, for example because a standing earlier price is merely confirmed without being restated.",
}

ABBR = (
    r"(?<!\bMr)(?<!\bMs)(?<!\bMrs)(?<!\bDr)(?<!\bInc)(?<!\bCo)(?<!\bCorp)(?<!\bNo)"
    r"(?<!\bL\.P)(?<!\bL\.L\.C)(?<!\bU\.S)(?<!\b[A-Z])"
    r"(?<!\bp\.m)(?<!\ba\.m)(?<!\bLtd)(?<!\bJr)"  # added after round 3, which split sentences at "5 p.m."
)


class JevUnavailable(Exception):
    """The pass cannot run or finish; the mechanical report stands alone."""


# ---------------------------------------------------------------- filing text


def norm(s: Any) -> str:
    s = unicodedata.normalize("NFKC", s or "")
    s = s.replace("“", '"').replace("”", '"').replace("’", "'").replace("‘", "'")
    s = re.sub(r"[‐-―]", "-", s)
    return re.sub(r"\s+", " ", s).strip()


def paragraphs(filing: Path) -> tuple[list[str], tuple[int, int]]:
    """All paragraphs of the filing, and the index span of the Background section."""
    soup = BeautifulSoup(filing.read_bytes(), "lxml")
    paras = []
    for el in soup.find_all(["p", "div", "td"]):
        if el.find(["p", "div", "td", "table"]):
            continue
        t = norm(el.get_text(" "))
        if len(t) > 40 or re.fullmatch(
            r"(background of the (merger|offer)|reasons for the merger.*|recommendation of .*)", t, re.I
        ):
            paras.append(t)
    heads = [i for i, t in enumerate(paras) if re.fullmatch(r"background of the (merger|offer)", t, re.I)]
    if not heads:
        raise JevUnavailable("Background section heading not found in the filing")
    start = heads[-1] + 1
    end = next(
        (
            i
            for i in range(start, len(paras))
            if len(paras[i]) < 120 and re.match(r"(reasons for the merger|recommendation of)", paras[i], re.I)
        ),
        None,
    )
    if end is None or end - start < 5:
        raise JevUnavailable("End of the Background section not found in the filing")
    return paras, (start, end)


def quotes(cell: Any) -> list[str]:
    qs = [norm(q) for q in re.findall(r"“(.+?)”", cell or "", flags=re.S)]
    if not qs and cell:  # unquoted style: text followed by (p. N)
        qs = [norm(x) for x in re.split(r"\(pp?\.[^)]*\)", cell) if len(x.strip()) > 15]
    return qs


def locate(paras: list[str], q: str) -> int | None:
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


def sentences(p: str) -> list[str]:
    parts = re.split(ABBR + r"\.\s+(?=[A-Z\"(])", p)
    return [s.strip() + ("" if s.strip().endswith(".") else ".") for s in parts if len(s.strip()) > 30]


def ledger(workbook: Path, paras: list[str]) -> list[dict[str, Any]]:
    ws = openpyxl.load_workbook(workbook, data_only=True)["Deal ledger"]
    rows = list(ws.iter_rows(values_only=True))
    hdr = [str(h).strip() for h in rows[0]]
    out = []
    for n, r in enumerate(rows[1:], start=2):
        if any(v not in (None, "") for v in r):
            d = {h: (v.strftime("%Y-%m-%d") if hasattr(v, "strftime") else v) for h, v in zip(hdr, r)}
            d["_sheet_row"] = n
            d["_para"] = next(
                (j for j in (locate(paras, q) for q in quotes(d.get("Quote and page"))) if j is not None), None
            )
            out.append(d)
    return out


# ------------------------------------------------------------------ API calls


class Asker:
    """One System One call per request; responses cached by request content."""

    def __init__(self, cache_dir: Path, api_key: str | None) -> None:
        self.cache_dir = cache_dir
        self.api_key = api_key
        self.client: Any = None
        self.new_calls = 0
        cache_dir.mkdir(parents=True, exist_ok=True)
        # Files restored from the experiments carry a tag prefix; match on the hash alone.
        self.index = {f.stem.rsplit("_", 1)[-1]: f for f in cache_dir.glob("*.json")}

    def __call__(self, state: dict[str, Any], questions: dict[str, Any]) -> dict[str, Any]:
        body = {"state": state, "model": MODEL, "questions": questions}
        h = hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()[:16]
        if h in self.index:
            return json.loads(self.index[h].read_text())["response"]["answers"]
        if not self.api_key:
            raise JevUnavailable("TYPESAFE_API_KEY is not set and the answer is not in the cache")
        import httpx

        if self.client is None:
            self.client = httpx.Client(timeout=120, headers={"Authorization": "Bearer " + self.api_key})
        for attempt in range(6):
            t0 = time.time()
            try:
                r = self.client.post(API_URL, json=body)
            except httpx.HTTPError as exc:
                raise JevUnavailable(f"network error: {type(exc).__name__}") from exc
            if r.status_code in (429, 500, 502, 503, 504):
                time.sleep(float(r.headers.get("retry-after", 2**attempt)))
                continue
            break
        if r.status_code != 200:
            raise JevUnavailable(f"TypeSafe API returned {r.status_code}")
        resp = r.json()
        f = self.cache_dir / f"{h}.json"
        f.write_text(json.dumps({"request": body, "response": resp, "latency_s": round(time.time() - t0, 3)}, indent=1))
        self.index[h] = f
        self.new_calls += 1
        return resp["answers"]


# ---------------------------------------------------------------- price check


def num(v: Any) -> float | None:
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def ptxt(lo: float, hi: float | None) -> str:
    return f"${lo:.2f}" if hi is None or hi == lo else f"${lo:.2f} to ${hi:.2f}"


def describe(row: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    """Event description from ledger columns only (no Note: it often restates the price)."""
    who = row["Who"]
    mine = [r for r in rows if r.get("Who") == who and num(r.get("Price low")) is not None]
    same_day = [r for r in mine if r.get("Sort date") == row.get("Sort date")]
    d = f'the event recorded as "{row.get("Event")}" by "{who}", dated {row.get("When")}'
    if len(same_day) > 1:
        k = [r["_sheet_row"] for r in same_day].index(row["_sheet_row"]) + 1
        d += f" (proposal {k} of {len(same_day)} that this party made on that date, in order)"
    elif len(mine) > 1:
        k = [r["_sheet_row"] for r in mine].index(row["_sheet_row"]) + 1
        d += f" (priced proposal {k} of {len(mine)} by this party over the whole process, in date order)"
    return d


def price_question(row: dict[str, Any], rows: list[dict[str, Any]]) -> dict[str, Any]:
    p = ptxt(num(row["Price low"]), num(row.get("Price high")))
    return {
        "scoped": {
            "type": "choice",
            "criteria": SUPPORT,
            "instructions": f"A research ledger claims that at {describe(row, rows)}, the total per-share value of the proposal was {p}. Judge this claim against `passage` only. Bind party, date, event and price together: a figure that the passage gives for a different party, a different date or proposal, or for only the cash part of a package does not support the claim.",
        }
    }


def price_pass(ask: Asker, rows: list[dict[str, Any]], paras: list[str]) -> tuple[list[dict[str, Any]], dict[str, int]]:
    priced = [r for r in rows if num(r.get("Price low")) is not None]
    located = [r for r in priced if r["_para"] is not None]

    def one(row: dict[str, Any]) -> dict[str, Any]:
        i = row["_para"]
        state = {"passage": {"before": paras[max(0, i - 2):i], "cited_paragraph": paras[i], "after": paras[i + 1:i + 3]}}
        return ask(state, price_question(row, rows))["scoped"]

    with ThreadPoolExecutor(8) as ex:
        answers = list(ex.map(one, located))

    issues = []
    for row, a in zip(located, answers):
        if a["choice"] == "supported":
            continue
        p = ptxt(num(row["Price low"]), num(row.get("Price high")))
        conf = round(a.get("confidence") or 0.0, 2)
        if a["choice"] == "contradicted":
            code, tier = "jev.price_contradicted", "price_contradicted"
            text = f"The quoted passage appears to give a different price than {p} for this event."
            expected = False
        else:
            expected = row.get("Event") == "Bid reaffirmed" or bool(re.search(r"\bcarried\b", str(row.get("Note") or ""), re.I))
            code, tier = "jev.price_not_stated", "price_not_stated"
            text = f"The quoted passage does not appear to state {p} for this event."
            if expected:
                text += " Expected here: the row carries an earlier price forward."
        issues.append(
            {"severity": "review", "code": code, "sheet": "Deal ledger", "row": row["_sheet_row"], "column": "Price low",
             "message": text, "basis": "jev", "confidence": conf, "tier": tier, "expected": expected}
        )
    return issues, {"priced_rows": len(priced), "priced_rows_checked": len(located)}


# ------------------------------------------------------------- omission check


def rowtxt(r: dict[str, Any]) -> str:
    price = f" | price {r.get('Price low')}" + (f"-{r.get('Price high')}" if r.get("Price high") not in (None, "", r.get("Price low")) else "") if r.get("Price low") not in (None, "") else ""
    return f"{r.get('When')} | {r.get('Who')} | {r.get('Event')}{price} | {(r.get('Note') or '')[:240]}"


def omission_pass(ask: Asker, rows: list[dict[str, Any]], paras: list[str], span: tuple[int, int]) -> tuple[list[dict[str, Any]], dict[str, int]]:
    a, b = span

    def tag_paragraph(i: int) -> dict[str, Any]:
        state = {"previous_paragraph": paras[i - 1], "paragraph": paras[i]}
        qs = {k: {"type": "noul", "instructions": f"Does `paragraph` report that {v}? Judge `paragraph` only; `previous_paragraph` is context for names and dates."} for k, v in KINDS.items()}
        return ask(state, qs)

    def tag_sentence(job: tuple[int, int, str]) -> dict[str, Any]:
        i, _, sent = job
        state = {"paragraph": paras[i], "sentence": sent}
        qs = {k: {"type": "noul", "instructions": f"Does `sentence` itself report that {v}? Judge `sentence` only; `paragraph` is context for names and dates."} for k, v in KINDS.items()}
        return ask(state, qs)

    def match(job: tuple[int, int, str, list[str]]) -> dict[str, Any]:
        i, _, sent, kinds = job
        near = [r for r in rows if r["_para"] is not None and abs(r["_para"] - i) <= 5]
        state = {"paragraph": paras[i], "target_sentence": sent}
        crit = {f"row_{r['_sheet_row']}": rowtxt(r) for r in near}
        crit["none"] = "None of the ledger rows records the event reported in the target sentence, either as the row's own event or in its note."
        crit["not_an_event"] = "The target sentence reports no discrete event of these kinds (background, reasoning, description or discussion only)."
        what = "; or ".join(KINDS[x] for x in kinds)
        qs = {"match": {"type": "choice", "criteria": crit,
                        "instructions": f"`target_sentence` (from a merger filing; `paragraph` gives context) appears to report that {what}. Each option describes one row of a research ledger as date | party | event | note. Select the row that records the event reported in `target_sentence`: same party or group, same action, consistent date and terms, allowing paraphrase and allowing the event to be summarised in a row's note. A related event with a different party, date or action does not count."}}
        return ask(state, qs)["match"]

    with ThreadPoolExecutor(8) as ex:
        ptags = list(ex.map(tag_paragraph, range(a, b)))
        todo = [(i, k, s) for i, t in zip(range(a, b), ptags) if max(v["noul"] for v in t.values()) > 0.5
                for k, s in enumerate(sentences(paras[i]))]
        stags = list(ex.map(tag_sentence, todo))
        tagged = [(i, k, s, kinds) for (i, k, s), t in zip(todo, stags)
                  if (kinds := [x for x, v in t.items() if v["noul"] > 0.5])]
        answers = list(ex.map(match, tagged))

    issues = []
    for (i, _, sent, kinds), ans in zip(tagged, answers):
        conf = ans.get("confidence") or 0.0
        if ans["choice"] != "none" or conf < SECOND_TIER:
            continue
        top = conf >= TOP_TIER
        issues.append(
            {"severity": "review", "code": "jev.event_missing", "sheet": "Deal ledger", "row": None, "column": None,
             "message": ("Probably absent" if top else "Possibly absent") + f" from the ledger ({', '.join(kinds)}): \"{sent}\"",
             "basis": "jev", "confidence": round(conf, 2), "tier": "missing_top" if top else "missing_second",
             "background_paragraph": i - a + 1}
        )
    stats = {"background_paragraphs": b - a, "event_sentences": len(tagged),
             "none_any_confidence": sum(x["choice"] == "none" for x in answers)}
    return issues, stats


# ---------------------------------------------------------------------- entry


def run(workbook: Path, filing: Path, cache_dir: Path = DEFAULT_CACHE, api_key: str | None = None) -> dict[str, Any]:
    """Return {"issues": [...], "summary": {...}}. Never raises: a failure becomes one info issue."""
    ask = Asker(cache_dir, api_key if api_key is not None else os.environ.get("TYPESAFE_API_KEY"))
    issues: list[dict[str, Any]] = []
    summary: dict[str, Any] = {"model": MODEL, "passes_run": []}

    def skipped(what: str, exc: Exception) -> None:
        reason = str(exc) if isinstance(exc, JevUnavailable) else f"{type(exc).__name__}: {exc}"
        issues.append({"severity": "info", "code": "jev.skipped", "sheet": None, "row": None, "column": None,
                       "message": f"Jev {what} skipped ({reason}). Mechanical checks are unaffected.", "basis": "jev"})

    try:
        paras, span = paragraphs(filing)
        rows = ledger(workbook, paras)
        summary["rows_not_located"] = sum(r["_para"] is None for r in rows)
        for r in rows:
            if r["_para"] is None:
                issues.append({"severity": "info", "code": "jev.row_not_located", "sheet": "Deal ledger", "row": r["_sheet_row"],
                               "column": "Quote and page", "basis": "jev",
                               "message": "Quotation not found inside one filing paragraph, so Jev did not check this row."})
    except Exception as exc:  # a second reader must never take the mechanical report down with it
        skipped("pass", exc)
    else:
        for name, check in (("price", lambda: price_pass(ask, rows, paras)),
                            ("omission", lambda: omission_pass(ask, rows, paras, span))):
            try:
                found, stats = check()
            except Exception as exc:
                skipped(f"{name} check", exc)
            else:
                issues += found
                summary.update(stats)
                summary["passes_run"].append(name)
    summary["new_api_calls"] = ask.new_calls
    summary["model_judgments"] = sum(x["severity"] == "review" for x in issues)
    return {"issues": issues, "summary": summary}
