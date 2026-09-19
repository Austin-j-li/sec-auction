"""Round 3, experiment O: omission discovery at sentence level.
Stage 1 (code): split Background paragraphs that round 1 tagged with an event kind into sentences.
Stage 2 (Jev): tag each sentence with the same eight event kinds.
Stage 3 (Jev): per tagged sentence and workbook, select the ledger row that records it, or `none`.
Read-only; no workbook is modified."""
import json, re, sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
HERE = Path(__file__).resolve().parent
R1 = HERE.parent / "jev_experiments_2026-09-19"
sys.path.insert(0, str(R1))
import lib
from lib import paragraphs, quotes, locate, ledger, FILINGS, ROOT
from exp_coverage import KINDS
lib.RAW = HERE / "raw"; lib.RAW.mkdir(exist_ok=True)

ABBR = r"(?<!\bMr)(?<!\bMs)(?<!\bMrs)(?<!\bDr)(?<!\bInc)(?<!\bCo)(?<!\bCorp)(?<!\bNo)(?<!\bL\.P)(?<!\bL\.L\.C)(?<!\bU\.S)(?<!\b[A-Z])"


def sentences(p):
    parts = re.split(ABBR + r"\.\s+(?=[A-Z\"(])", p)
    return [s.strip() + ("" if s.strip().endswith(".") else ".") for s in parts if len(s.strip()) > 30]


def tag(deal, i, k, sent, para):
    state = {"paragraph": para, "sentence": sent}
    qs = {kind: {"type": "noul", "instructions": f"Does `sentence` itself report that {v}? Judge `sentence` only; `paragraph` is context for names and dates."} for kind, v in KINDS.items()}
    return lib.ask(state, qs, f"O1_{deal}_{i}_{k}")["answers"]


def rowtxt(r):
    price = f" | price {r.get('Price low')}" + (f"-{r.get('Price high')}" if r.get("Price high") not in (None, "", r.get("Price low")) else "") if r.get("Price low") not in (None, "") else ""
    return f"{r.get('When')} | {r.get('Who')} | {r.get('Event')}{price} | {(r.get('Note') or '')[:240]}"


def match(deal, model, i, k, sent, para, kinds, near):
    state = {"paragraph": para, "target_sentence": sent}
    crit = {f"row_{r['_sheet_row']}": rowtxt(r) for r in near}
    crit["none"] = "None of the ledger rows records the event reported in the target sentence, either as the row's own event or in its note."
    crit["not_an_event"] = "The target sentence reports no discrete event of these kinds (background, reasoning, description or discussion only)."
    what = "; or ".join(KINDS[x] for x in kinds)
    qs = {"match": {"type": "choice", "criteria": crit,
                    "instructions": f"`target_sentence` (from a merger filing; `paragraph` gives context) appears to report that {what}. Each option describes one row of a research ledger as date | party | event | note. Select the row that records the event reported in `target_sentence`: same party or group, same action, consistent date and terms, allowing paraphrase and allowing the event to be summarised in a row's note. A related event with a different party, date or action does not count."}}
    a = lib.ask(state, qs, f"O2_{deal}_{model}_{i}_{k}")["answers"]["match"]
    return {"deal": deal, "model": model, "para": i, "sent": k, "kinds": kinds, "n_rows": len(near), "choice": a["choice"], "confidence": a["confidence"],
            "p_none": a["probabilities"]["none"], "p_not_event": a["probabilities"]["not_an_event"]}


if __name__ == "__main__":
    cov = json.loads((R1 / "results_coverage.json").read_text())
    sents, res = [], []
    for deal in FILINGS:
        paras, (a, b) = paragraphs(deal)
        todo = [(i, k, s) for i in range(a, b) if max(cov[deal]["tags"][str(i)].values()) > 0.5 for k, s in enumerate(sentences(paras[i]))]
        with ThreadPoolExecutor(8) as ex:
            tags = list(ex.map(lambda t: tag(deal, t[0], t[1], t[2], paras[t[0]]), todo))
        tagged = []
        for (i, k, s), t in zip(todo, tags):
            kinds = [x for x, v in t.items() if v["noul"] > 0.5]
            sents.append({"deal": deal, "para": i, "sent": k, "text": s, "tags": {x: v["noul"] for x, v in t.items()}})
            if kinds:
                tagged.append((i, k, s, kinds))
        print(deal, len(todo), "sentences", len(tagged), "tagged", flush=True)
        for model in ["opus", "sol", "deepseek"]:
            rows = ledger(ROOT / f"_dev/model_comparison_2026-09-19/workbooks/{model}/{deal}.xlsx")
            for r in rows:
                r["_para"] = next((j for j in (locate(paras, q) for q in quotes(r.get("Quote and page"))) if j is not None), None)
            jobs = [(deal, model, i, k, s, paras[i], kinds, [r for r in rows if r["_para"] is not None and abs(r["_para"] - i) <= 5]) for i, k, s, kinds in tagged]
            with ThreadPoolExecutor(8) as ex:
                res += list(ex.map(lambda j: match(*j), jobs))
    (HERE / "results_omit_sentences.json").write_text(json.dumps(sents, indent=1))
    (HERE / "results_omit.json").write_text(json.dumps(res, indent=1))
    print(len(sents), "sentences;", len(res), "match calls")
