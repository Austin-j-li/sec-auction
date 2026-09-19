# -*- coding: utf-8 -*-
"""Build extraction/providence-worcester.xlsx from rows_source.py + rows_ledger.py.

Runs programmatic checks (quote coverage, ordering, date pairs, counts) and
prints results. Writes the six required sheets: Deal ledger, Summary,
Questions, Source text (visible); AI original, Lists (hidden).
"""
import datetime as dt
import re
import sys
import unicodedata

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule

import rows_source as SRC
import rows_ledger as LED

BLOCKS = {}
for line in open("filing_blocks.txt", encoding="utf-8"):
    m = re.match(r"\[\[(\d+)\|([^|]+)\|p(\d+)\]\] (.*)", line)
    if m:
        BLOCKS[int(m.group(1))] = (m.group(2), int(m.group(3)), m.group(4))


def printed(page):
    return page - 7 if page >= 8 else None


# ---------------------------------------------------------------- source rows
source_rows = []
pid = 0
for bi, label in SRC.BACKGROUND:
    pid += 1
    tag, pg, txt = BLOCKS[bi]
    section = label if label else "Background of the Merger"
    if bi in (646, 649):
        section = "Background of the Merger (continuation)"
    source_rows.append({"id": "P-%03d" % pid, "section": section,
                        "page": printed(pg), "text": txt, "bi": bi})

for xid, section, bis, page_override, note in SRC.ADDITIONAL:
    txt = " ".join(BLOCKS[b][2] for b in bis)
    if note:
        txt = txt + "  [Layout note: " + note + "]"
    pg = page_override or printed(BLOCKS[bis[0]][1])
    source_rows.append({"id": xid, "section": section, "page": pg,
                        "text": txt, "bi": bis[0]})

SRC_BY_ID = {r["id"]: r for r in source_rows}

# ------------------------------------------------------------ quote checking
def norm(s):
    s = unicodedata.normalize("NFKC", s)
    for a, b in (("\u2019", "'"), ("\u2018", "'"), ("\u201c", '"'),
                 ("\u201d", '"'), ("\u2014", "-"), ("\u2013", "-"),
                 ("\u2011", "-"), ("\u00a0", " ")):
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip().lower()

corpus = norm(" ".join(BLOCKS[i][2] for i in sorted(BLOCKS)))
corpus_by_bi = {i: norm(BLOCKS[i][2]) for i in BLOCKS}

quote_fail = []
quote_total = 0
for r in LED.ROWS:
    for q in re.findall(r"\u201c([^\u201c\u201d]+)\u201d", r["why"]):
        quote_total += 1
        if norm(q) not in corpus:
            quote_fail.append((r["rowid"], q[:90]))

# --------------------------------------------------------------- row checks
problems = []
ids = [r["rowid"] for r in LED.ROWS]
if len(ids) != len(set(ids)):
    problems.append("duplicate Row ids")
for i, r in enumerate(LED.ROWS):
    if r["n"] != i + 1:
        problems.append(r["rowid"] + ": n not sequential")
    if not r["wdate"]:
        problems.append(r["rowid"] + ": missing working date")
    if not r["dmethod"] or not r["dbasis"]:
        problems.append(r["rowid"] + ": missing date basis/method")
    if r["dbasis"] == "Reported day" and r["dmethod"] != "Reported":
        problems.append(r["rowid"] + ": Reported-day basis with non-Reported method")
    if r["dmethod"] == "Reported" and r["dbasis"] != "Reported day":
        problems.append(r["rowid"] + ": Reported method with non-Reported-day basis")
    if r["dmethod"] == "Inferred" and r["dbasis"] != "Inferred day":
        problems.append(r["rowid"] + ": Inferred method mismatch")
    if r["dfrom"] and r["dto"] and r["dfrom"] > r["dto"]:
        problems.append(r["rowid"] + ": from > to")
    if r["wdate"] and r["dfrom"] and r["wdate"] < r["dfrom"]:
        problems.append(r["rowid"] + ": working before from")
    if r["wdate"] and r["dto"] and r["wdate"] > r["dto"]:
        problems.append(r["rowid"] + ": working after to")
    if r["dbasis"] == "Reported day" and r["dfrom"] != r["dto"]:
        problems.append(r["rowid"] + ": reported day bounds differ")
    if r["what"] == "Round opened" and not r["rfinal"]:
        problems.append(r["rowid"] + ": round without finality")
    if r["what"] == "Deadline" and not r["dtreat"]:
        problems.append(r["rowid"] + ": deadline without treatment")
    if r["obasis"].startswith("Inferred") and not r["terms"].startswith("Inferred:"):
        problems.append(r["rowid"] + ": inferred row lacks basis tag")
    if not r["page"]:
        problems.append(r["rowid"] + ": missing page")
    if r["what"] in ("Bid", "Bid reaffirmed") and not r["cdetail"]:
        problems.append(r["rowid"] + ": bid without conditions detail")

# working date order check
prev = None
for r in LED.ROWS:
    w = r["wdate"]
    if prev and w < prev:
        problems.append(r["rowid"] + ": working date decreases")
    prev = w

# page consistency: the Page field is the main (first) source paragraph
for r in LED.ROWS:
    sid = r["source"][0]
    sr = SRC_BY_ID.get(sid)
    if sr and sr["page"] and sr["page"] != r["page"]:
        problems.append("%s: page %s vs %s page %s" % (r["rowid"], r["page"], sid, sr["page"]))

print("quotes checked:", quote_total, "failures:", len(quote_fail))
for rid, q in quote_fail:
    print("  QUOTE-FAIL", rid, q)
print("structure problems:", len(problems))
for p in problems:
    print("  PROBLEM", p)

# formula expectation check: replicate the Summary SUMIFS criteria in Python
def sumifs(event=None, rnd=None, obasis=None):
    tot = 0
    for r in LED.ROWS:
        if r["include"] != "Yes":
            continue
        if event and r["what"] != event:
            continue
        if rnd is not None and str(r["rnd"]) != str(rnd):
            continue
        if obasis and r["obasis"] != obasis:
            continue
        if r["count"] is None:
            continue
        tot += r["count"]
    return tot

expect = {
    "nda (Summary formula)": sumifs(event="NDA signed"),
    "contacts (Summary formula)": sumifs(event="Contact"),
    "R1 bidder units": sumifs(event="Bid", rnd=1),
    "R2 bidder units": sumifs(event="Bid", rnd=2),
    "R3 bidder units": sumifs(event="Bid", rnd=3) + sumifs(event="Bid reaffirmed", rnd=3),
    "inferred exits residual": sumifs(obasis="Inferred: residual"),
    "inferred exits silent": sumifs(obasis="Inferred: silent"),
}
print("formula expectations (replicated criteria):", expect)

# ------------------------------------------------------------------- styling
HDR = Font(bold=True, color="FFFFFF", size=10)
HDRFILL = PatternFill("solid", fgColor="1F4E79")
SUBHDR = Font(bold=True, size=10, color="1F4E79")
WRAP = Alignment(wrap_text=True, vertical="top")
TOP = Alignment(vertical="top")
DATEFMT = "MM/DD/YYYY"
RED_BOLD = Font(color="FFC00000", bold=True)

wb = Workbook()

# ------------------------------------------------------------------ ledger
ws = wb.active
ws.title = "Deal ledger"
cols = [
    ("#", 5), ("When", 26), ("Who", 24), ("What happened", 15), ("Process", 8),
    ("Round", 7), ("Type", 10), ("Terms or outcome", 60), ("Formality", 11),
    ("Conditions level", 11), ("Why and evidence", 70), ("Source", 13),
    ("Review", 9), ("Reviewer note", 16),
    ("Row id", 8), ("Include", 8), ("Count", 7), ("Date from", 11),
    ("Date to", 11), ("Working date", 12), ("Date basis", 14),
    ("Date method", 15), ("Price low", 9), ("Price high", 9),
    ("Price kind", 12), ("Price origin", 13), ("Currency", 9),
    ("All cash", 9), ("Cash at closing", 10), ("Conditions detail", 60),
    ("Due date", 11), ("Deadline treatment", 14), ("Round finality", 13),
    ("Decided by", 10), ("Exit reason", 18), ("Outcome basis", 14),
    ("Page", 6), ("Related rows", 22), ("Deal", 14),
]
for i, (name, width) in enumerate(cols, 1):
    c = ws.cell(row=1, column=i, value=name)
    c.font = HDR
    c.fill = HDRFILL
    c.alignment = Alignment(wrap_text=True, vertical="center")
    ws.column_dimensions[get_column_letter(i)].width = width

DEF_KEYS = ["n", "when", "who", "what", "process", "rnd", "type", "terms",
            "formality", "cond", "why"]
EXP_KEYS = ["rowid", "include", "count", "dfrom", "dto", "wdate", "dbasis",
            "dmethod", "plow", "phigh", "pkind", "porigin", "currency",
            "allcash", "cashclose", "cdetail", "duedate", "dtreat", "rfinal",
            "decided", "exit", "obasis", "page", "related"]
KEYS = DEF_KEYS + ["source", "review", "reviewer"] + EXP_KEYS
KEYS[KEYS.index("reviewer")] = "reviewer_note"

def cellval(r, k):
    v = r.get(k)
    if k in ("dfrom", "dto", "wdate", "duedate") and v:
        return dt.date.fromisoformat(v)
    return v

for ridx, r in enumerate(LED.ROWS, start=2):
    vals = []
    vals.append(r["n"]); vals.append(r["when"]); vals.append(r["who"])
    vals.append(r["what"]); vals.append(r["process"]); vals.append(int(r["rnd"]) if str(r["rnd"]).strip() else "")
    vals.append(r["type"]); vals.append(r["terms"]); vals.append(r["formality"])
    vals.append(r["cond"]); vals.append(r["why"])
    vals.append("; ".join(r["source"])); vals.append(r["review"]); vals.append("")
    vals.append(r["rowid"]); vals.append(r["include"]); vals.append(r["count"])
    vals.append(cellval(r, "dfrom")); vals.append(cellval(r, "dto"))
    vals.append(cellval(r, "wdate")); vals.append(r["dbasis"]); vals.append(r["dmethod"])
    vals.append(r["plow"]); vals.append(r["phigh"]); vals.append(r["pkind"])
    vals.append(r["porigin"]); vals.append(r["currency"]); vals.append(r["allcash"])
    vals.append(r["cashclose"]); vals.append(r["cdetail"]); vals.append(cellval(r, "duedate"))
    vals.append(r["dtreat"]); vals.append(r["rfinal"]); vals.append(r["decided"])
    vals.append(r["exit"]); vals.append(r["obasis"]); vals.append(r["page"])
    vals.append(r["related"]); vals.append("PWRR\u2013G&W")
    for cidx, v in enumerate(vals, 1):
        c = ws.cell(row=ridx, column=cidx, value=v)
        c.alignment = WRAP
        if cidx in (18, 19, 20, 31):
            c.number_format = DATEFMT
        if cidx in (23, 24, 29):
            c.number_format = "0.00"

# source hyperlinks to the first passage row
from openpyxl.worksheet.hyperlink import Hyperlink
src_row = {r["id"]: i + 2 for i, r in enumerate(source_rows)}
for ridx, r in enumerate(LED.ROWS, start=2):
    first = r["source"][0]
    cell = ws.cell(row=ridx, column=12)
    cell.hyperlink = Hyperlink(ref=cell.coordinate, location="'Source text'!A%d" % src_row[first],
                               target=None, tooltip="Go to %s in Source text" % first)
    cell.font = Font(color="0563C1", underline="single", size=11)

LAST = len(LED.ROWS) + 1
ws.freeze_panes = "D2"
ws.auto_filter.ref = "A1:AM%d" % LAST

# expandable groups collapsed
ws.column_dimensions.group("O", "AM", outline_level=1, hidden=True)

# conditional formatting vs AI original (row id match, not row position)
new_rule = FormulaRule(formula=['AND($O2<>"",ISNA(MATCH($O2,\'AI original\'!$O:$O,0)))'], font=RED_BOLD)
chg_rule = FormulaRule(formula=['AND($O2<>"",$A2<>INDEX(\'AI original\'!$A:$AM,MATCH($O2,\'AI original\'!$O:$O,0),COLUMN()))'], font=RED_BOLD)
ws.conditional_formatting.add("A2:AM%d" % LAST, new_rule)
ws.conditional_formatting.add("A2:AM%d" % LAST, chg_rule)

# -------------------------------------------------------------------- Lists
ls = wb.create_sheet("Lists")
lists = {
    "EventLabels": ["Target interest", "Bidder interest", "Target sale decision",
        "Activist pressure", "Activist involvement", "Adviser engaged",
        "Adviser service observed", "Adviser ended", "Contact", "NDA signed",
        "Round opened", "Deadline set", "Deadline revised", "Deadline",
        "Target decision", "Information access changed", "Material process update",
        "Exclusivity changed", "Bid", "Bid reaffirmed", "Offer update",
        "Other-scope bid", "Valuation statement", "Bidding group changed",
        "Joined group", "Dropped by target", "Withdrew", "Did not submit",
        "Participation paused", "Re-entered", "Not selected at signing",
        "Sale process announced", "Bid announced", "Merger announced",
        "Merger agreement signed", "Go-shop changed", "Process terminated",
        "Process restarted", "Agreement terminated", "Closed"],
    "TypeList": ["Strategic", "Financial", "Mixed", "Unknown"],
    "FormalityList": ["Formal", "Informal", "Insufficient evidence", "Varies"],
    "ConditionsList": ["None", "Light", "Heavy", "Insufficient evidence", "Varies"],
    "IncludeList": ["Yes", "No"],
    "DateBasisList": ["Reported day", "Inferred day", "Reported interval",
        "Approximate window", "Relative only", "Undated"],
    "DateMethodList": ["Reported", "Inferred", "Assigned: deadline",
        "Assigned: decision day", "Assigned: midpoint", "Assigned: bound",
        "Assigned: sequence"],
    "PriceKindList": ["Point", "Bidder range", "Group envelope", "Bound only", "Undisclosed"],
    "PriceOriginList": ["Stated", "Carried forward", "Inferred"],
    "AllCashList": ["Yes", "No", "Not stated"],
    "DeadlineTreatList": ["Enforced", "Extended", "Late bids accepted",
        "Passed without action", "Unclear", "No deadline stated",
        "Extended; Late bids accepted"],
    "RoundFinalityList": ["Announced as final", "Inferred final", "Not final"],
    "DecidedByList": ["Bidder", "Target", "Both", "Unknown"],
    "ExitReasonList": ["Value below market price", "Value at or below market price",
        "Value below earlier offer", "Value at earlier offer",
        "Would not improve earlier offer", "Lower offer than rivals",
        "Terms or process", "Other stated reason", "Not stated"],
    "OutcomeBasisList": ["Stated", "Inferred: residual", "Inferred: exclusivity",
        "Inferred: silent", "Inferred: identity"],
}
col = 1
for name, vals in lists.items():
    hc = ls.cell(row=1, column=col, value=name)
    hc.font = SUBHDR
    for i, v in enumerate(vals, start=2):
        ls.cell(row=i, column=col, value=v)
    rng = "Lists!$%s$2:$%s$%d" % (get_column_letter(col), get_column_letter(col), len(vals) + 1)
    from openpyxl.workbook.defined_name import DefinedName
    wb.defined_names.add(DefinedName(name, attr_text=rng))
    col += 1

DV_RANGES = {
    "EventLabels": "D2:D%d" % LAST, "TypeList": "G2:G%d" % LAST,
    "FormalityList": "I2:I%d" % LAST, "ConditionsList": "J2:J%d" % LAST,
    "IncludeList": "P2:P%d" % LAST, "DateBasisList": "U2:U%d" % LAST,
    "DateMethodList": "V2:V%d" % LAST, "PriceKindList": "Y2:Y%d" % LAST,
    "PriceOriginList": "Z2:Z%d" % LAST, "AllCashList": "AB2:AB%d" % LAST,
    "DeadlineTreatList": "AF2:AF%d" % LAST, "RoundFinalityList": "AG2:AG%d" % LAST,
    "DecidedByList": "AH2:AH%d" % LAST, "ExitReasonList": "AI2:AI%d" % LAST,
    "OutcomeBasisList": "AJ2:AJ%d" % LAST,
}
for name, rng in DV_RANGES.items():
    dv = DataValidation(type="list", formula1="=" + name, allow_blank=True, showDropDown=False)
    ws.add_data_validation(dv)
    dv.add(rng)
ls.sheet_state = "hidden"

# ---------------------------------------------------------------- AI original
ai = wb.create_sheet("AI original")
for i, (name, _w) in enumerate(cols, 1):
    c = ai.cell(row=1, column=i, value=name)
    c.font = HDR
    c.fill = HDRFILL
for ridx in range(2, LAST + 1):
    for cidx in range(1, len(cols) + 1):
        src = ws.cell(row=ridx, column=cidx)
        c = ai.cell(row=ridx, column=cidx, value=src.value)
        c.number_format = src.number_format
ai.sheet_state = "hidden"

# -------------------------------------------------------------------- Summary
su = wb.create_sheet("Summary")
su.column_dimensions["A"].width = 44
su.column_dimensions["B"].width = 130
su.column_dimensions["C"].width = 14

def block(title):
    r = su.max_row + 2
    c = su.cell(row=r, column=1, value=title)
    c.font = Font(bold=True, size=11, color="1F4E79")
    return r + 1

def line(label, value, formula=False):
    r = su.max_row + 1
    a = su.cell(row=r, column=1, value=label)
    a.alignment = TOP
    b = su.cell(row=r, column=2, value=value)
    b.alignment = WRAP
    return r

c = su.cell(row=1, column=1, value="SUMMARY \u2014 Providence & Worcester Railroad Company (PWRR) / Genesee & Wyoming Inc. (G&W)")
c.font = Font(bold=True, size=13)
line("Status", "AI first pass; not human-approved. Instruction revision of 19 September 2026 (Pro). Source coverage: the single supplied filing, DEFM14A proxy statement of Providence and Worcester Railroad Company (file providence-worcester_2016-09-20_DEFM14A.htm); no other sources. Last recheck: none \u2014 first pass as delivered; derived outputs are as of this version.")

r = block("1. Status and commercial account")
for s in [
 "Initiation: in Q4 2015 PWRR's Chairman/CEO and VP/Chief Commercial Officer met Class I rail partner Party A on commercial matters; Party A floated joint ventures and equity interest, prompting a Board subcommittee banker search and the 01/27/2016 engagement of GHF (whose business was acquired by BMO on 08/01/2016) as the target's financial adviser.",
 "Process: on 03/14/2016 the Board approved a change-in-control process; the week-of-03/28/2016 outreach wave and April confidentiality agreements produced nine non-binding IOIs (received 05/19-06/01/2016, $17.93-$26.50 as-converted) and later six LOIs (late July 2016, $19.20-$24.00), with Party B and G&W chosen on 07/27/2016 for confirmatory diligence and definitive negotiation.",
 "Competition: G&W opened at $21.15 per share (including a $1.13 CVR tied to a South Quay property sale) and revised to $22.15 on 07/26/2016 after target feedback that its price and CVR were not competitive, while Party B led at $24.00; Party D ($24.00) and Party E ($23.81, with Party F financing support) briefly re-entered on 08/01/2016 and were both out again by 08/02/2016.",
 "Selection: with the target preparing to sign with Party B, G&W returned on 08/12/2016 with an all-cash $25.00 LOI (CVR dropped, offer expiring 6:00 p.m. on 08/13/2016); Party B, asked whether it would improve, declined; the Board determined G&W's offer was the superior proposal, BMO delivered its fairness opinion, and the merger agreement was signed the same day.",
 "Outcome: $25.00 per share in cash (preferred converts 100-for-1 plus accrued/unpaid dividends), a 53% premium over the 08/12/2016 close of $16.30; announced 08/15/2016. STB relief was sought 09/01/2016 (exemption petition) and 09/14/2016 (voting-trust submission); closing was expected in Q4 2016 and is not observed in the filing. No go-shop and no post-signing competing proposal are reported.",
 "Coverage: one sale process (P1) with three analytical rounds; 26 executed bidder confidentiality agreements (25 in the March-April wave plus late entrant Party C) per the ledger arithmetic against the filing's stated 25; nine IOI submissions and six LOI submissions. Open items: the anonymous two low bidders, the 16 inferred non-submitters, Party A's mapping, and the two additional Class I rail approaches (Q3/Q4).",
]:
    line("", s)

r = block("2. Deal facts")
for lab, val in [
 ("Target", "Providence and Worcester Railroad Company (PWRR), a Rhode Island corporation; regional freight railroad (approx. 516 route miles; MA/RI/CT/NY); NASDAQ: PWX (X-005)."),
 ("Focal acquirer and type", "Genesee & Wyoming Inc. (G&W), Strategic: an operating short-line/regional freight railroad group (owns/leases 121 freight railroads; NYSE: GWR); acquisition through Pullman Acquisition Sub Inc., a shell formed 08/12/2016 (one bidder unit) (X-006)."),
 ("Agreed consideration", "$25.00 per share in cash for common stock; each preferred share automatically converts into 100 common shares plus accrued/unpaid dividends; options and RSUs are cashed out on a $25.00 basis. All cash, fixed at closing (X-009, X-003)."),
 ("Signing / announcement / completion", "Signed 08/12/2016; announced by press release 08/15/2016 before the NASDAQ open; completion not observed \u2014 expected Q4 2016; outside date 12/31/2016 (02/28/2017 if only STB approval remains) (X-008, X-026). The 10/26/2016 special meeting and shareholder vote are scheduled after the filing date."),
 ("Filing identity and date", "DEFM14A filed by Providence and Worcester Railroad Company; proxy letter dated 09/19/2016; record date 09/16/2016; source file raw_filing/providence-worcester_2016-09-20_DEFM14A.htm; background at printed pages 27-32."),
 ("Advisers' economics", "BMO aggregate fee approx. $2.52 million, majority payable at closing (X-022). G&W's financial adviser is not disclosed."),
]:
    line(lab, val)

r = block("3. Process and round map (P1)")
for lab, val in [
 ("P1 R0 \u2014 prior interest (Q4 2015 - 03/14/2016)", "Party A interest (R001), Board subcommittee (R002), GHF engagement (R003), 03/14/2016 process decision (R004); candidate R1 anchors kept as R005 and R004. No Round 0 opening row required."),
 ("P1 R1 \u2014 interest and IOIs", "Opened week of 03/28/2016 (R007; anchor = first outreach wave; panel Q1). Scope: 29 contacted (R008/R009), 25 wave NDA signers (R012/R013). Deadlines: set 05/10/2016 (R015; Extended \u2014 superseded by the 05/19/2016 revision), revised 05/19/2016 (R016), due 05/19/2016 Enforced (R017). Outcome: 9 IOIs $17.93-$26.50 (R018); 16 inferred non-submitters (R019); 2 low bidders dropped (R021); 7 advance. Finality: Not final."),
 ("P1 R2 \u2014 diligence stage and LOIs", "Opened 06/01/2016 (R020; seven advancing bidders admitted to management presentations and data site). Deadline set mid-June for 07/20/2016 (R023); due row R028 = Late bids accepted (G&W's 07/21 LOI considered). Scope: 7 + late entrant Party C = 8. Outcome: 6 LOIs (R029-R033, R036; G&W revised R037), 2 electors did not submit (R034/R035), 4 dropped 07/27/2016 (R039-R042), 2 continue. Finality: Not final."),
 ("P1 R3 \u2014 definitive negotiation", "Opened 07/27/2016 (R038; G&W and Party B finalists; on-site diligence 07/27-08/11/2016). Scope: 2 finalists plus re-entries by Party D (R043) and Party E (R045). Outcome: D withdrew 08/02/2016 (R048); E confirmed its original $21.26 (R047) and closes inferred-silent at signing (R055); B declines to improve and is Not selected at signing (R054); G&W wins with $25.00 (R053) and signs (R056). Finality: Inferred final."),
 ("Post-signing", "No go-shop and no competing proposal reported in the supplied filing; announcement 08/15/2016 (R057). Regulatory steps (STB 09/01 and 09/14/2016) are summarized here only. No second process."),
]:
    line(lab, val)

r = block("4. Participants and advisers")
for lab, val in [
 ("PWRR", "Target; Board and Transaction Committee (Barrett (Chair), Anderson, Garvey; Director Smith recused over GATX's 4.92% common stake)."),
 ("G&W (+ Merger Sub)", "Winner; Strategic. First recorded involvement: the 04/03-04/06/2016 convention introductions within the contacted cohort (P-007); LOIs R036/R037, final bid R053, signing R056."),
 ("Party A", "Strategic Class I rail partner; first interest Q4 2015 (R001); within the contacted/Nda cohorts; last seen at the 04/22/2016 memorandum distribution; closed by an Inferred: identity Did-not-submit row (R022, Count 0) \u2014 likely inside the 16 non-submitters, alternatively one of the two low bidders (Q4)."),
 ("Party B", "Strategic; introductory meeting 04/21/2016 (R014); LOI $24.00 (R029); finalist; returned draft 08/04/2016 (R049, late reconfirmation); declined to improve 08/12/2016; Not selected at signing (R054, Stated; exit reason Would not improve earlier offer)."),
 ("Party C", "Strategic late entrant; approach and NDA early July 2016, catch-up access (R024-R026); IOI $21.00 (R027); LOI $19.30 (R032); Dropped 07/27/2016 (R041)."),
 ("Party D", "Financial; LOI $21.00 with markups (R031); finalist; dropped then re-entered 08/01/2016 with a $24.00 revised LOI (R043/R044); Withdrew 08/02/2016 when its no-sign commitment demand was declined (R048)."),
 ("Party E", "Strategic; LOI $21.26 (R030); finalist; dropped then re-entered with a $23.81 revised LOI supported by Party F (R045/R046); withdrew the revised bid and confirmed $21.26 (R047); closes inferred-silent at signing (R055)."),
 ("Party F", "Strategic; LOI $19.20 (R033); dropped 07/27/2016 (R042); financing supporter of Party E's revised LOI (recorded on R046; no new row for an exited supporter)."),
 ("Cohorts", "25 wave NDA signers (11 strategic + 14 financial; R012/R013) including 16 inferred non-submitters (R019); 9 anonymous IOI bidders (R018); 2 anonymous low bidders (R021); 2 anonymous LOI electors (R034/R035). Cohorts are not additional parties to their members."),
 ("Eder Trusts / GATX", "Eder Trusts: 842,742 common (17.3%) and 500 preferred (78.1%) at record date; executed the voting agreement with G&W and the Company at signing (R056) (X-025). GATX: 4.92% common holder; no approach or bid reported."),
 ("Advisers", "GHF/BMO \u2014 target financial adviser, engaged 01/27/2016; acquisition of GHF by BMO noted 08/01/2016; fairness opinion 08/12/2016; fee approx. $2.52M; 09/06/2016 Board consideration of BMO's omitted affiliate lending relationship with G&W (confirmed not material; P-034, X-023) (R003). Hinckley, Allen & Snyder LLP \u2014 target legal counsel, service observed from 03/24/2016 (R006). Simpson Thacher & Bartlett LLP \u2014 G&W legal counsel, service observed from 08/10/2016 (R051). Unnamed Company STB counsel (R052)."),
]:
    line(lab, val)

r = block("5. Counts and auction screen")
line("Auction screen", "Met: more than one independent prospective acquiring bidder unit executed bidder-target confidentiality agreements in this process (11 strategic + 14 financial = 25 in the wave, plus late entrant Party C = 26). No lender-only, adviser or rollover agreements are included; no reuse from an earlier attempt is reported.")
line("NDA signatures (ledger formula)", "=SUMIFS('Deal ledger'!$Q:$Q,'Deal ledger'!$D:$D,\"NDA signed\",'Deal ledger'!$P:$P,\"Yes\")", True)
line("Contacts (ledger formula)", "=SUMIFS('Deal ledger'!$Q:$Q,'Deal ledger'!$D:$D,\"Contact\",'Deal ledger'!$P:$P,\"Yes\")", True)
line("R1 bidder units (formula)", "=SUMIFS('Deal ledger'!$Q:$Q,'Deal ledger'!$D:$D,\"Bid\",'Deal ledger'!$F:$F,1,'Deal ledger'!$P:$P,\"Yes\")", True)
line("R2 bidder units (formula)", "=SUMIFS('Deal ledger'!$Q:$Q,'Deal ledger'!$D:$D,\"Bid\",'Deal ledger'!$F:$F,2,'Deal ledger'!$P:$P,\"Yes\")", True)
line("R3 bidder units (formula)", "=SUMIFS('Deal ledger'!$Q:$Q,'Deal ledger'!$D:$D,\"Bid\",'Deal ledger'!$F:$F,3,'Deal ledger'!$P:$P,\"Yes\")+SUMIFS('Deal ledger'!$Q:$Q,'Deal ledger'!$D:$D,\"Bid reaffirmed\",'Deal ledger'!$F:$F,3,'Deal ledger'!$P:$P,\"Yes\")", True)
line("Inferred exit units (formula)", "=SUMIFS('Deal ledger'!$Q:$Q,'Deal ledger'!$AJ:$AJ,\"Inferred: residual\",'Deal ledger'!$P:$P,\"Yes\")+SUMIFS('Deal ledger'!$Q:$Q,'Deal ledger'!$AJ:$AJ,\"Inferred: silent\",'Deal ledger'!$P:$P,\"Yes\")", True)
line("Reconciliation of source totals", "Filing assertion '25' NDA signers at X-012 describes the wave group (11 strategic + 14 financial per P-006); the ledger adds Party C (R025) because the filing says Party C had not previously been part of the process. Six LOI submissions (X-012) match R029-R033 and R036; the nine IOIs (P-011) match R018. The contact sum of 30 excludes blank-count rows (two Class I approaches, R010; Party B's individual meeting, R014) and excludes Party A's Q4 2015 detail row (R001), which is an additional included contact record also inside the 29-cohort.")
line("Per-stage balance (entrants - stated exits - inferred exits = continuing)", "R1: 25 - 2 - 16 = 7 (inferred share of exits 16/18). R2: 8 (7 + Party C) - 6 (2 electors + 4 dropped) - 0 = 2. R3: 4 (2 finalists + D and E re-entries) - 3 (D withdrew, B not selected stated, E not selected inferred) = 1 (G&W). At signing only the winner remains; participants 26 + 2 re-entries; outcome tallies are occurrences/affected units (D and E each appear in a drop and a later exit), not unique permanent exits.")
line("Bid-version vs unit counts", "Seven R2 Bid rows but six R2 units (Party C's IOI and LOI are one unit; G&W's revision carries Count 0). Three R3 priced submissions plus two reaffirmations but four R3 units (Party E appears in both a bid and a reaffirmation; R047 Count 0). Row count does not establish submission count.")

r = block("6. Comparability and inputs (glossary below)")
for lab, val in [
 ("Scope and structure", "No other-scope or partial proposals are reported: the IOIs and LOIs were for 100% of the common stock on an as-converted basis. G&W's $1.13 CVR (South Quay property sale) was a contingent cash component of a whole-company offer, not a separate asset deal."),
 ("LOI comparability", "The six LOI prices were 'based on different assumptions and requirements related to transaction expenses and change in control payments' (P-022) and are not normalized here; they are not like-for-like quotes. The $17.93-$26.50 IOI figure is a group envelope across nine bids, not any member's range."),
 ("BMO analyses (not offers)", "Selected publicly traded companies: implied $10.95-$15.09; selected precedent transactions: $10.54-$26.50; discounted cash flow: $10.82-$12.34; each added the $12.5 million South Quay book value and was prepared on a fully-diluted basis against the $25.00 consideration (X-018 to X-021). These are valuation analyses, not bids."),
 ("Market benchmarks", "Common stock close $16.30 on 08/12/2016 (last trading day before announcement; the 53% premium benchmark) and $24.88 on 09/16/2016 (last trading day before the proxy) (X-011, X-013)."),
 ("Share and capital inputs (record date 09/16/2016)", "4,866,593 common shares outstanding; 640 preferred shares (8 holders) convertible 100-for-1; preferred is non-cumulative with dividends limited to $5.00 per share per year (X-007, X-027). Directors and executive officers held 1,107,002 common (22.7%) and 500 preferred (78.1%) (X-028); the Eder Trusts held 842,742 common (17.3%) and 500 preferred (78.1%) (X-025)."),
 ("Labeled calculation (convention, not a stated value)", "As-converted equity value at $25.00 = (4,866,593 common + 640 preferred x 100) x $25.00 = 4,930,593 x $25.00 = approx. $123.26 million, using record-date counts and excluding option/RSU dilution; the 08/12/2016 board materials may have used different counts. The $3.785 million termination fee is described by the filing as approximately 3% of transaction value (implied value approx. $126 million on the filing's own arithmetic)."),
 ("Projections (summary)", "Management projections used by BMO: revenue 18.1/35.3/37.3/41.4/43.6 $M for 2016(Q3-Q4)-2020; tax-affected EBIT 2.1/(0.5)/0.2/1.4/2.8; unlevered free cash flow (1.7)/(0.5)/(0.1)/1.4/1.9 (X-024). Projections, not facts or offers."),
 ("Glossary", "NDA = confidentiality/non-disclosure agreement; IOI = indication of interest; LOI = letter of intent; CVR = contingent value right; as-converted = treating preferred as 100 common shares; STB = Surface Transportation Board; R0-R3 = analytical rounds of Process 1; wave cohort = the 25 buyers that signed NDAs after the March 2016 outreach."),
]:
    line(lab, val)

# ------------------------------------------------------------------ Questions
qs = wb.create_sheet("Questions")
qcols = [("Q", 6), ("Review topic", 30), ("Recommended answer", 90),
         ("Why and source", 60), ("Affected rows/fields", 34),
         ("Consequence of changing it", 45), ("Status", 10), ("Reviewer note", 16)]
for i, (name, w) in enumerate(qcols, 1):
    c = qs.cell(row=1, column=i, value=name)
    c.font = HDR
    c.fill = HDRFILL
    qs.column_dimensions[get_column_letter(i)].width = w

questions = [
 ("Q1", "Process and round map; R1 anchor; rejected boundary candidates; post-signing",
  "One process (P1). R1 opens with the week-of-03/28/2016 first outreach wave (R007); rejected anchor candidates are kept as rows: R005 (03/24/2016 committee authorization; launch within about a week) and R004 (03/14/2016 Board process decision). R2 opens 06/01/2016 (R020, selection of seven advancing bidders to management presentations and a data site); alternative boundary: the mid-June LOI instruction (R023), which would leave the presentation stage inside R1. R3 opens 07/27/2016 (R038, definitive negotiation with G&W and Party B). R1 and R2 are Not final; R3 is Inferred final. Post-signing: no go-shop, no competing proposal, no second process.",
  "Section 6.2-6.3; P-008 (wave), P-011 (selection), P-012 (LOI instruction), P-023 (finalists). Boundaries are analytical, not filing labels.",
  "R004, R005, R007, R020, R023, R038 (Round, Round finality, R1 anchor tag)",
  "Moving R2 to mid-June changes Round values for the 06/01/2016 rows and R029-R037; moving R1 to 03/24/2016 changes the R1 anchor tag and reorders one row; a second process would require a supported abandonment and fresh start, which the filing does not report.",
  "Pending", ""),
 ("Q2", "Deadline history and treatments",
  "IOI deadline set 05/10/2016 (R015; Extended by the revision), revised to 05/19/2016 (R016), due 05/19/2016 with treatment Enforced (R017): the next steps (05/23/2016 review, 06/01/2016 selection) used the bids in hand, and the 05/19-06/01 receipt window straddles the due date so no late acceptance is recorded. LOI deadline 07/20/2016 (set at R023, due at R028) with treatment Late bids accepted: G&W's 07/21/2016 LOI was considered and revised 07/26/2016 without any revision to the date. No other bid deadlines; the G&W 08/12/2016 offer expiry (6:00 p.m. 08/13/2016) is an offer term on R053, not a submission deadline.",
  "Section 8.3; P-010 (IOI deadlines), P-011 (IOI window), P-017 (G&W dates).",
  "R015, R016, R017, R023, R028 (Due date, Deadline treatment)",
  "Calling the 05/19/2016 date Late bids accepted or the 07/20/2016 date Enforced would misstate what followed; a notional extension of 07/20/2016 is not supported by the filing.",
  "Pending", ""),
 ("Q3", "NDA and population bases; cohort overlap",
  "Wave base is 25 NDA signers (11 strategic + 14 financial, R012/R013); Party C adds the 26th (R025). The filing's '25' (X-012) describes the wave. The nine IOIs are assumed to come from the 25 signers (R018/R019). The two LOI electors are assigned to the seven advancing bidders (R034/R035) rather than to the wider contacted group. Party B's membership in the 11 strategic buyers is assumed but not stated (R014 Count blank). The two additional Class I rail approaches (R010) have unresolved overlap with the 29-contact cohort (Count blank).",
  "Section 5.2, 7.3; P-006 (11+14), P-011 (nine IOIs), P-022 (electors), X-012 ('25').",
  "R008-R014, R018, R019, R022, R025, R026, R034, R035 (Count, Type, population text)",
  "If an IOI came from outside the 25, or Party B/Party C was inside the 25, the residual non-submitter count and the NDA total shift by those units; the auction screen stays Met either way.",
  "Pending", ""),
 ("Q4", "Participation outcomes, agency and every inferred closing row (grouped by transition)",
  "Inferred closings: 16 non-submitting wave signers at 05/19/2016 (R019; 25 - 9 = 16, Inferred: residual, Count 16); Party A identity row (R022, Count 0, recommended inside R019, alternative the two low bidders R021); Party E's silent close at signing (R055; last seen confirming $21.26 on 08/02/2016). Stated outcomes: two low IOI bidders dropped (R021); the two electors (R034/R035); E, D, C and F dropped 07/27/2016 (R039-R042); D's Withdrew on 08/02/2016 (R048) - read as withdrawal rather than a temporary pause, though the filing says 'at that time'; B's Not selected at signing (R054, Stated; Would not improve earlier offer) with actual agency Target. Every entrant is closed once per process (D and E re-enter first).",
  "Section 10.1-10.2; P-011, P-022, P-023, P-024, P-031, P-032.",
  "R019, R021, R022, R034-R035, R039-R042, R048, R054, R055 (Outcome basis, Decided by, Exit reason, Count)",
  "Relabeling D as Participation paused would require a further closing row at signing; treating Party A as one of the low bidders changes its label but not any count; declaring a different winner is not supported.",
  "Pending", ""),
 ("Q5", "Formality and conditions assessments (grouped)",
  "Formal: Party B's LOI via returned markups (R029) and its 08/04/2016 returned draft (R049, late reconfirmation flagged; price $24.00 carried forward, Conditions Light, DD open yes); G&W's LOIs (R036/R037) and 08/12/2016 bid (R053, Conditions Light, alternative reading None if the bid is treated as sign-ready); Party D's LOIs (R031/R044, Formality carried forward; R044 records the no-sign commitment request as Excl: requested (30 days)). Informal: the nine IOIs (R018), Party C's IOI/LOI (R027/R032), Party E's LOI and revised LOI (R030/R046, issues-summary default; borderline; R046 records Fin: represented for Party F's financing support) and E's reaffirmation (R047). Heavy levels rest on stated diligence periods: G&W 3 weeks; D 4 weeks/30 days; E 60 days and 30 days; C and F 30 days. No None assigned. Every Bid/Bid reaffirmed row carries a fixed-format Conditions detail string.",
  "Section 9.2-9.3; calibration examples C-D; P-016, P-017, P-018, P-022, P-024, P-027.",
  "R018, R026-R033, R036, R037, R044, R046, R047, R049, R053 (Formality, Conditions level, Conditions detail)",
  "Upgrading Party E to Formal without a returned-document or final-solicitation signal would misapply the issues-list default; downgrading G&W's 08/12/2016 bid to None would require support that it was sign-ready with diligence and documents complete.",
  "Pending", ""),
 ("Q6", "Prices, consideration, CVR and comparability",
  "The $17.93-$26.50 figure is the nine-IOI group envelope (R018) and is not entered on any member. G&W's cash-plus-CVR bids (R036/R037) are All cash Yes with fixed cash of $20.02/$21.02 and the $1.13 CVR only in text; the 08/12/2016 bid (R053) is $25.00 all cash with the CVR dropped. The six LOI prices rest on differing expense/change-in-control assumptions and are not normalized. Party E's reversion price is carried forward (R047). Preferred converts 100-for-1 plus dividends. The as-converted ~$123.26 million equity figure is a labeled calculation, not a stated transaction value.",
  "Section 9.4; P-017 (CVR), P-022 (assumptions), X-003/X-009 (consideration), X-007 (shares).",
  "R018, R027-R033, R036, R037, R041, R044, R046, R047, R053, R056 (Price low/high/kind/origin, All cash, Cash at closing)",
  "Putting the IOI envelope on individual rows would misattribute group pricing; converting the CVR or averaging ranges is prohibited; changing All cash for G&W would contradict the contingent-cash nature of the CVR.",
  "Pending", ""),
 ("Q7", "Working-date conventions and within-round ordering",
  "Conventions used: Q4 2015 rows share 11/15/2015 (midpoint; R001/R002); wave NDAs 04/09/2016 (midpoint of 03/28-04/22; R012/R013); IOI deadline revision 05/08/2016 (midpoint; R016); the five undated late-July LOIs take 07/20/2016 (Assigned: deadline) and are placed ahead of G&W's 07/21/2016 LOI (R029-R033 before R036) though their relative order is not observed; Party C's early-July rows take 07/05/2016 and its access row 07/05/2016 by sequence (spans to 07/14/2016; R024-R026). Sorting by Working date with # as tie-breaker reproduces the ledger order.",
  "Section 8.1-8.2; calibration example B (late-July LOIs and the 07/20/2016 deadline).",
  "R001, R002, R012, R013, R016, R023, R024, R025, R026, R029-R033 (Working date, Date method, Date from/to)",
  "Re-sequencing rows requires re-checking Working dates so the sort property holds; a reviewer preferring the 07/22/2016 review as the LOI receipt bound would narrow R029-R033 windows but not their Working dates.",
  "Pending", ""),
]
r = 1
for q in questions:
    r += 1
    for i, v in enumerate(q, 1):
        c = qs.cell(row=r, column=i, value=v)
        c.alignment = WRAP

r += 2
c = qs.cell(row=r, column=1, value="Section 13 check results (programmatic unless stated)")
c.font = Font(bold=True, size=11, color="1F4E79")
checks = [
 ("1", "Coverage and materiality", "Qualified", "All disclosed core offers, NDAs/contacts, selection steps, outcomes, signing and publicity are represented. Source limitations preserved: two anonymous low bidders, 16 anonymous residual non-submitters, Party A identity, two unresolved Class I approaches."),
 ("2", "Counts and population", "Qualified", "Summary arithmetic matches included counts (NDA 26; contacts 30 + additional records; R1/R2/R3 units 9/6/4). Bases flagged in Q3; per-stage balances shown with the inferred share."),
 ("3", "Participation continuity", "Passed", "Every entrant is closed once per process (exits, group joins or inferred rows), winner last; D and E re-entry rows precede their renewed bids; no participant stock goes negative."),
 ("4", "Dates and order", "Passed (programmatic)", "All rows have Working date and Date method; Working dates never decrease and match # order; no Working date outside its own bounds; Reported-day basis pairs only with Reported; no assigned date labelled Reported."),
 ("5", "Offers and classifications", "Qualified", "Every Bid/Bid reaffirmed row has Formality, Conditions level and a fixed-format Conditions detail. Borderline calls flagged: Party E formality (Q5); G&W 08/12/2016 Conditions Light vs None (Q5)."),
 ("6", "Structure and consistency", "Passed", "One Round opened row per round, each with finality; R1 row carries the R1 anchor tag and candidate rows; Deadline rows carry treatments matching the Summary map; inferred rows open with their Outcome basis; Page filled wherever Source is."),
 ("7", "Evidence", "Passed (programmatic)", "All %d ledger quotations were found in the cited source passages after whitespace/typographic normalization; page citations match the passage pages. Interpretation caveats for cross-paragraph judgments sit in Q1/Q7." % quote_total),
 ("8", "Review and workbook operation", "Qualified", "Row ids unique; filters, drop-down validations (Lists) and internal links are written; Summary formulas were validated by replicating their criteria against the ledger data (NDA 26, contacts 30, R1/R2/R3 units 9/6/4, inferred exits 17) but were not recalculated in a spreadsheet application - LibreOffice crashes in this environment on any workbook; conditional-format correction tracking against 'AI original' is built (red bold on changed values and new rows) but not exercised; 'AI original' holds the delivered values. Inspect for clipping after any human edit."),
]
r += 1
for i, h in enumerate(["#", "Check", "Status", "Notes"], 1):
    c = qs.cell(row=r, column=i, value=h)
    c.font = HDR; c.fill = HDRFILL
for ch in checks:
    r += 1
    for i, v in enumerate(ch, 1):
        c = qs.cell(row=r, column=i, value=v)
        c.alignment = WRAP

# ---------------------------------------------------------------- Source text
st = wb.create_sheet("Source text")
for i, (name, w) in enumerate([("Paragraph", 10), ("Section", 42), ("Page", 6), ("Text", 160)], 1):
    c = st.cell(row=1, column=i, value=name)
    c.font = HDR; c.fill = HDRFILL
    st.column_dimensions[get_column_letter(i)].width = w
r = 1
for srow in source_rows:
    r += 1
    st.cell(row=r, column=1, value=srow["id"])
    st.cell(row=r, column=2, value=srow["section"])
    st.cell(row=r, column=3, value=srow["page"])
    c = st.cell(row=r, column=4, value=srow["text"])
    c.alignment = WRAP
st.freeze_panes = "A2"
st.auto_filter.ref = "A1:D%d" % r

# ------------------------------------------------------------------- save
import os
# visible sheets first, in the required order; support sheets last
wb._sheets = [wb[n] for n in ["Deal ledger", "Summary", "Questions", "Source text",
                              "AI original", "Lists"]]
os.makedirs("extraction", exist_ok=True)
out = "extraction/providence-worcester.xlsx"
wb.save(out)
print("saved", out)
print("ledger rows:", len(LED.ROWS), "| source rows:", len(source_rows))

# summary of counts for the final report
counts = {}
for rr in LED.ROWS:
    if rr["count"]:
        counts.setdefault(rr["what"], 0)
        counts[rr["what"]] += rr["count"]
print("count totals by event:", counts)
