"""Experiment A: ledger-to-source support checks on existing workbooks, plus planted corruptions.
Review of finished workbooks only; no extraction is run and no workbook is modified."""
import json, random, sys, copy
from concurrent.futures import ThreadPoolExecutor
from lib import *

EXITS = {
    "Dropped by target": "The target excluded the bidder, refused it the next stage, or signed exclusivity with a rival.",
    "Withdrew": "The bidder itself said it was ending its participation.",
    "Did not submit": "The bidder was invited to bid by a deadline and did not submit a bid.",
    "Not selected at signing": "The bidder was still bidding or still in the process when the target signed with someone else.",
    "No exit described": "The passage does not describe this party leaving or losing the process.",
}
REASONS = {
    "Value below market price": "Bidder indicated its valuation was below the current share price.",
    "Value at or below market price": "Bidder indicated it could not pay a premium to the share price.",
    "Value below earlier offer": "Bidder indicated it could now pay only less than its own earlier offer.",
    "Value at earlier offer": "Bidder's value stayed at its earlier offer.",
    "Would not improve earlier offer": "Bidder was unable or unwilling to raise its earlier offer.",
    "Lower offer than rivals": "Bidder's offer was lower than competing offers.",
    "Terms or process": "Exit due to contract terms, conditions, financing, timing, diligence or process issues, not price.",
    "Other stated reason": "Another reason is stated (strategy change, other priorities, etc.).",
    "Not stated": "The passage gives no reason for this party's exit.",
}


def packet(paras, i, k=2):
    return {"before": paras[max(0, i - k):i], "cited_paragraph": paras[i], "after": paras[i + 1:i + 1 + k]}


def questions(row):
    who, ev = row.get("Who"), row.get("Event")
    q = {
        "actor": {"type": "noul", "instructions": f"Does `passage.cited_paragraph` describe something done by, done to, or decided about the party called \"{who}\" (or a group that the passage shows includes it)?",
                  "criteria": {"true": "That party, or a cohort clearly containing it, is a subject of the cited paragraph.", "false": "The cited paragraph concerns other parties only."}},
        "event": {"type": "noul", "instructions": f"A research ledger records an event labelled \"{ev}\" for \"{who}\". Does the passage report facts that fit the label \"{ev}\" for that party?",
                  "criteria": {"true": "The passage reports such an event, or facts from which it directly follows.", "false": "The passage reports a different kind of event, or nothing of that kind."}},
    }
    lo, hi = row.get("Price low"), row.get("Price high")
    if isinstance(lo, (int, float)):
        p = f"${lo:.2f}" if lo == hi or hi is None else f"${lo:.2f} to ${hi:.2f}"
        q["price"] = {"type": "noul", "instructions": f"Does the passage state that \"{who}\" offered, proposed or indicated a price of {p} per share (the same number may be written without trailing zeros)?",
                      "criteria": {"true": f"The per-share figure {p} appears in the passage as this party's price.", "false": "The passage gives a different figure for this party, or no figure."}}
        if row.get("All cash") in ("Yes", "No"):
            q["all_cash"] = {"type": "choice", "instructions": f"What form of consideration does the passage state for the offer by \"{who}\"?",
                             "criteria": {"Yes": "Entirely cash, including cash plus a contingent value right or earnout that is itself paid in cash.",
                                          "No": "Includes shares, options, notes or other non-cash securities.",
                                          "Not stated": "The passage does not say what form the consideration takes."}}
    if ev in EXITS:
        q["exit_label"] = {"type": "choice", "instructions": f"How does the passage describe \"{who}\" leaving or losing the sale process?", "criteria": EXITS}
        q["exit_reason"] = {"type": "choice", "instructions": f"What reason does the passage give for \"{who}\" leaving the sale process or not continuing?", "criteria": REASONS}
        q["exit_express"] = {"type": "noul", "instructions": f"Does the passage expressly report that \"{who}\" left, was excluded from, was told it was out of, or declined to continue in the process?",
                             "criteria": {"true": "An exit, exclusion or notification is stated in words.", "false": "The exit can only be inferred, for example because the party is simply not mentioned among those continuing."}}
    return q


def check(deal, model, row, paras, variant="orig"):
    qs = quotes(row.get("Quote and page"))
    i = next((j for j in (locate(paras, x) for x in qs) if j is not None), None)
    if i is None:
        return None
    state = {"passage": packet(paras, i)}
    resp = ask(state, questions(row), f"A_{deal}_{model}_{row['_sheet_row']}_{variant}")
    return {"deal": deal, "model": model, "row": row["_sheet_row"], "variant": variant, "who": row.get("Who"), "event": row.get("Event"),
            "exit_reason": row.get("Exit reason"), "all_cash": row.get("All cash"), "inferred": row.get("Inferred"),
            "answers": resp["answers"], "tokens": resp["usage"]["input_tokens"]}


def corruptions(rows, rng):
    out = []
    named = sorted({r["Who"] for r in rows if r.get("Who") and len(r["Who"]) < 30 and isinstance(r.get("Price low"), (int, float))})
    for r in rows:
        if isinstance(r.get("Price low"), (int, float)):
            c = copy.copy(r); d = rng.choice([-1.5, -0.75, 0.5, 1.25])
            c["Price low"] = r["Price low"] + d
            c["Price high"] = r["Price high"] + d if isinstance(r.get("Price high"), (int, float)) else None
            out.append(("price", c))
            others = [n for n in named if n != r["Who"]]
            if others:
                c = copy.copy(r); c["Who"] = rng.choice(others); out.append(("actor", c))
        if r.get("Event") in EXITS and r["Event"] != "No exit described":
            c = copy.copy(r); c["Event"] = rng.choice([e for e in list(EXITS)[:4] if e != r["Event"]]); out.append(("exitlabel", c))
    return out


if __name__ == "__main__":
    rng = random.Random(20260919)
    jobs = []
    for deal in FILINGS:
        paras, _ = paragraphs(deal)
        for model in ["opus", "sol", "deepseek"]:
            rows = ledger(ROOT / f"_dev/model_comparison_2026-09-19/workbooks/{model}/{deal}.xlsx")
            jobs += [(deal, model, r, paras, "orig") for r in rows]
            jobs += [(deal, model, r, paras, "planted_" + k) for k, r in corruptions(rows, rng)]
    if len(sys.argv) > 1:
        jobs = jobs[:int(sys.argv[1])]
    with ThreadPoolExecutor(8) as ex:
        res = [x for x in ex.map(lambda j: check(*j), jobs) if x]
    (HERE / "results_rows.json").write_text(json.dumps(res, indent=1))
    print(len(jobs), "jobs", len(res), "answered", sum(r["tokens"] for r in res), "input tokens")
