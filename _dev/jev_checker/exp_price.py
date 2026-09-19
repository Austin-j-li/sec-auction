"""Round 3, experiment P: event-scoped price verification built from ledger columns only,
run on the real priced rows of the nine comparison workbooks, with same-party price swaps planted.
Control: round 1's actor-only Noul on the same rows. Read-only; no workbook is modified."""
import json, sys, copy
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "jev_experiments_2026-09-19"))
import lib
from lib import paragraphs, quotes, locate, ledger, FILINGS, ROOT
lib.RAW = HERE / "raw"; lib.RAW.mkdir(exist_ok=True)

import os, re
LEADIN = os.environ.get("LEADIN") == "1"
MONTH = re.compile(r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\b")

SUPPORT = {
    "supported": "The source states this price (or range) for this party at this specific event. Trailing zeros and wording may differ.",
    "contradicted": "The source describes this specific event by this party and gives a different price or range for it, or the claimed figure belongs to another party, another event, or only one component of the package.",
    "insufficient": "The source does not state a price for this specific event, for example because a standing earlier price is merely confirmed without being restated.",
}


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def ptxt(lo, hi):
    return f"${lo:.2f}" if hi is None or hi == lo else f"${lo:.2f} to ${hi:.2f}"


def describe(row, rows):
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


def questions(row, rows, lo, hi):
    who, p = row["Who"], ptxt(lo, hi)
    return {
        "scoped": {"type": "choice", "criteria": SUPPORT,
                   "instructions": f"A research ledger claims that at {describe(row, rows)}, the total per-share value of the proposal was {p}. Judge this claim against `passage` only. Bind party, date, event and price together: a figure that the passage gives for a different party, a different date or proposal, or for only the cash part of a package does not support the claim."},
        "actor_only": {"type": "noul", "instructions": f"Does the passage state that \"{who}\" offered, proposed or indicated a price of {p} per share (the same number may be written without trailing zeros)?",
                       "criteria": {"true": f"The per-share figure {p} appears in the passage as this party's price.", "false": "The passage gives a different figure for this party, or no figure."}},
    }


def run(job):
    deal, model, row, rows, paras, i, variant, lo, hi, src = job
    j = i - 2
    if LEADIN:  # extend back to the nearest paragraph that carries a calendar date (bullet lists put the date in their lead-in)
        j = i
        while j > max(0, i - 8) and not MONTH.search(paras[j]):
            j -= 1
        j = min(j, i - 2)
    state = {"passage": {"before": paras[max(0, j):i], "cited_paragraph": paras[i], "after": paras[i + 1:i + 3]}}
    resp = lib.ask(state, questions(row, rows, lo, hi), f"{'PD' if LEADIN else 'P'}_{deal}_{model}_{row['_sheet_row']}_{variant}")
    a = resp["answers"]
    return {"deal": deal, "model": model, "row": row["_sheet_row"], "who": row["Who"], "when": row.get("When"), "event": row.get("Event"),
            "variant": variant, "claimed": [lo, hi], "true": [num(row["Price low"]), num(row.get("Price high"))], "swap_source_row": src,
            "scoped": a["scoped"]["choice"], "scoped_conf": a["scoped"].get("confidence"), "scoped_dist": a["scoped"].get("distribution") or a["scoped"].get("probabilities"),
            "actor_only": a["actor_only"]["noul"], "tokens": resp["usage"]["input_tokens"]}


if __name__ == "__main__":
    jobs = []
    for deal in FILINGS:
        paras, _ = paragraphs(deal)
        for model in ["opus", "sol", "deepseek"]:
            rows = ledger(ROOT / f"_dev/model_comparison_2026-09-19/workbooks/{model}/{deal}.xlsx")
            priced = []
            for r in rows:
                if num(r.get("Price low")) is None:
                    continue
                r["_para"] = next((j for j in (locate(paras, q) for q in quotes(r.get("Quote and page"))) if j is not None), None)
                if r["_para"] is not None:
                    priced.append(r)
            for r in priced:
                lo, hi = num(r["Price low"]), num(r.get("Price high"))
                jobs.append((deal, model, r, rows, paras, r["_para"], "orig", lo, hi, None))
                # planted: same party's price from another of its rows; else another party's price cited within two paragraphs
                same = [o for o in priced if o["Who"] == r["Who"] and (num(o["Price low"]), num(o.get("Price high"))) != (lo, hi)]
                near = [o for o in priced if o["Who"] != r["Who"] and abs(o["_para"] - r["_para"]) <= 2 and (num(o["Price low"]), num(o.get("Price high"))) != (lo, hi)]
                for kind, pool in (("swap_same_party", same), ("swap_near_party", near)):
                    if pool:
                        o = min(pool, key=lambda o: (abs(o["_para"] - r["_para"]), abs(o["_sheet_row"] - r["_sheet_row"])))
                        jobs.append((deal, model, r, rows, paras, r["_para"], kind, num(o["Price low"]), num(o.get("Price high")), o["_sheet_row"]))
    if len(sys.argv) > 1:
        jobs = jobs[:int(sys.argv[1])]
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(run, jobs))
    (HERE / ("results_price_leadin.json" if LEADIN else "results_price.json")).write_text(json.dumps(res, indent=1))
    print(len(res), "calls", sum(r["tokens"] for r in res), "input tokens")
