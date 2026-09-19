"""Experiment B: source-to-ledger coverage. Stage 1 tags every Background paragraph by event kind.
Stage 2 asks, per tagged paragraph and workbook, whether the nearby ledger rows already capture it."""
import json, sys
from concurrent.futures import ThreadPoolExecutor
from lib import *

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


def tag(deal, i, paras):
    state = {"previous_paragraph": paras[i - 1], "paragraph": paras[i]}
    qs = {k: {"type": "noul", "instructions": f"Does `paragraph` report that {v}? Judge `paragraph` only; `previous_paragraph` is context for names and dates."} for k, v in KINDS.items()}
    return ask(state, qs, f"B1_{deal}_{i}")["answers"]


def covered(deal, model, i, paras, near, kinds):
    state = {"paragraph": paras[i], "ledger_rows": [{k: r.get(k) for k in ("When", "Who", "Event", "Price low", "Price high", "Note")} for r in near]}
    qs = {k: {"type": "noul", "instructions": f"`paragraph` reports that {KINDS[k]}. Is every such event in `paragraph` recorded by some entry in `ledger_rows` (same party, same kind of event, consistent date)?",
              "criteria": {"true": "Each such event has a matching ledger entry, possibly summarised in an entry's Note.", "false": "At least one such event in the paragraph has no matching ledger entry."}} for k in kinds}
    return ask(state, qs, f"B2w5_{deal}_{model}_{i}")["answers"]


if __name__ == "__main__":
    out = {}
    for deal in FILINGS:
        paras, (a, b) = paragraphs(deal)
        with ThreadPoolExecutor(8) as ex:
            tags = dict(zip(range(a, b), ex.map(lambda i: tag(deal, i, paras), range(a, b))))
        out[deal] = {"tags": {i: {k: v["noul"] for k, v in t.items()} for i, t in tags.items()}, "coverage": {}}
        for model in ["opus", "sol", "deepseek"]:
            rows = ledger(ROOT / f"_dev/model_comparison_2026-09-19/workbooks/{model}/{deal}.xlsx")
            for r in rows:
                r["_para"] = next((j for j in (locate(paras, q) for q in quotes(r.get("Quote and page"))) if j is not None), None)
            jobs = []
            for i, t in tags.items():
                kinds = [k for k, v in t.items() if v["noul"] > 0.5]
                if kinds:
                    near = [r for r in rows if r["_para"] is not None and abs(r["_para"] - i) <= 5]
                    jobs.append((i, near, kinds))
            with ThreadPoolExecutor(8) as ex:
                ans = list(ex.map(lambda j: covered(deal, model, j[0], paras, j[1], j[2]), jobs))
            out[deal]["coverage"][model] = {j[0]: {"n_near": len(j[1]), "direct": sum(r["_para"] == j[0] for r in j[1]), **{k: v["noul"] for k, v in a_.items()}} for j, a_ in zip(jobs, ans)}
    (HERE / "results_coverage.json").write_text(json.dumps(out, indent=1))
