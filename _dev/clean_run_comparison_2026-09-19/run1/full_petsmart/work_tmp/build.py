# -*- coding: utf-8 -*-
"""Build petsmart.xlsx from deal_data.py + the parsed filing text."""
import json, re, sys
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.hyperlink import Hyperlink
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles.differential import DifferentialStyle
from openpyxl.formatting import Rule

sys.path.insert(0, '/home/uctpiaj/work/work_tmp')
from deal_data import LEDGER_KEYS, LEDGER_ROWS, X_REFS, X_TABLE, DEAL

DATA = json.load(open('/home/uctpiaj/work/work_tmp/pages.json'))
OUT = '/home/uctpiaj/work/extraction/petsmart.xlsx'

def norm(t):
    t = t.replace('\xa0', ' ').replace('\u200b', '').replace('\u2009', ' ').replace('\u202f', ' ')
    return re.sub(r'\s+', ' ', t).strip()

# ------------------------------------------------------------------ source text
def get_para(page, idx):
    for d in DATA:
        if d['page'] == page and str(idx) in [str(k) for k in range(len(d['paras']))]:
            if str(idx).isdigit() and int(idx) < len(d['paras']):
                t = norm(d['paras'][int(idx)])
                if t and t != 'TABLE OF CONTENTS':
                    return t
    raise KeyError((page, idx))

def get_by_i(i, j):
    for d in DATA:
        if d['i'] == i:
            return norm(d['paras'][j])
    raise KeyError((i, j))

# assemble P rows (background pp. 21-26)
def norm_check(t):
    t = t.replace('\xa0', ' ').replace('\u200b', '').replace('\u2009', ' ')
    return re.sub(r'\s+', ' ', t).strip()

p_raw = []
for d in DATA:
    if not (d['page'] and d['page'].isdigit()):
        continue
    p = int(d['page'])
    if not (21 <= p <= 26):
        continue
    for t in d['paras']:
        t = norm_check(t)
        if not t or t == 'TABLE OF CONTENTS':
            continue
        p_raw.append((p, t))

p_rows = []
pid = 0
def section_for(t):
    if t == 'THE MERGER (PROPOSAL 1)':
        return "The Merger (Proposal 1) — heading"
    if t == 'Certain Effects of the Merger':
        return "Certain Effects of the Merger — heading"
    if t.startswith(('If the merger agreement is adopted', 'Upon the consummation', 'Our common stock is currently registered')):
        return "Certain Effects of the Merger"
    if t == 'Background of the Merger':
        return "Background of the Merger — heading"
    if t == 'Reasons for the Merger':
        return "Reasons for the Merger — heading"
    if t.startswith(('On December 13, 2014, the board unanimously approved', 'In the course of making the unanimous decision', 'Attractive Value.')):
        return "Reasons for the Merger"
    return "Background of the Merger"

for p, t in p_raw:
    pid += 1
    base = f"P-{pid:03d}"
    sec = section_for(t)
    if len(t) > 2000:
        # split at a sentence boundary near the middle
        mid = len(t) // 2
        cut = t.find('. ', mid - 300)
        if cut == -1:
            cut = mid
        else:
            cut += 1
        p_rows.append((base + "a", sec, p, t[:cut].strip()))
        p_rows.append((base + "b", sec, p, "(continued) " + t[cut:].strip()))
    else:
        p_rows.append((base, sec, p, t))

x_rows = []
for xid, section, page, ref in X_REFS:
    if ref is None:
        continue
    pg, idx = ref
    if pg.isdigit() and int(pg) <= 90:
        txt = get_para(pg, idx)
    else:
        txt = get_by_i(int(pg), int(idx))
    x_rows.append((xid, section, page, txt))

# X-039: notices block (Parent notice + Simpson Thacher copy)
notices = []
for j in [4, 5, 6, 7, 8, 9, 10, 11]:
    notices.append(get_by_i(143, j))
x_rows.append(("X-039", "Annex A - Agreement and Plan of Merger - Notices (A-46)", "A-46",
               " / ".join(notices)))

x_rows.extend(X_TABLE)
x_rows.sort(key=lambda r: (0 if r[0].startswith('X-0') else 1, r[0]))
# keep X rows in numeric order
def xkey(r):
    m = re.match(r'X-(\d+)', r[0]); return int(m.group(1))
x_rows.sort(key=xkey)

SRC = p_rows + x_rows
src_row_of = {}
for i, (sid, sec, pg, txt) in enumerate(SRC, start=3):  # row 1 header, row 2 note
    src_row_of[sid] = i

# resolve base ids like P-013 -> first part row
def resolve_sid(sid):
    if sid in src_row_of:
        return src_row_of[sid]
    for k in src_row_of:
        if k.startswith(sid) and len(k) == len(sid) + 1 and k[-1] in 'ab':
            return src_row_of[k]
    return None

# ------------------------------------------------------------------ ledger sheet
wb = Workbook()
ws = wb.active
ws.title = "Deal ledger"

HEADERS = ["#", "When", "Who", "What happened", "Process", "Round", "Type",
           "Terms or outcome", "Formality", "Conditions level", "Why and evidence",
           "Source", "Review", "Reviewer note",
           "Row id", "Include", "Count", "Date from", "Date to", "Working date",
           "Date basis", "Date method", "Price low", "Price high", "Price kind",
           "Price origin", "Currency", "All cash", "Cash at closing",
           "Conditions detail", "Due date", "Deadline treatment", "Round finality",
           "Decided by", "Exit reason", "Outcome basis", "Page", "Related rows", "Deal"]

ws.append(HEADERS)
for r in LEDGER_ROWS:
    ws.append([r.get(k) for k in LEDGER_KEYS])

last = ws.max_row
NL = len(HEADERS)  # 39 -> AM

def d(s):
    if s is None: return None
    return datetime.strptime(s, "%m/%d/%Y")

for row in ws.iter_rows(min_row=2, max_row=last):
    for c in row:
        key = HEADERS[c.column - 1]
        v = c.value
        if key in ("Date from", "Date to", "Working date", "Due date") and isinstance(v, str):
            c.value = d(v)
            c.number_format = "MM/DD/YYYY"
        elif key in ("Price low", "Price high", "Cash at closing") and isinstance(v, (int, float)):
            c.number_format = "#,##0.00"
        elif key in ("Count", "Process", "Page") and isinstance(v, (int, float)):
            c.number_format = "0"
        c.alignment = Alignment(wrap_text=True, vertical="top")

# header style + freeze + filter
hf = Font(bold=True, color="FFFFFF")
hfill = PatternFill("solid", fgColor="1F4E78")
for c in ws[1]:
    c.font = hf; c.fill = hfill
    c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
ws.freeze_panes = "D2"
ws.auto_filter.ref = f"A1:{get_column_letter(NL)}{last}"

widths = {"A": 4.5, "B": 21, "C": 27, "D": 19, "E": 8, "F": 7.5, "G": 11, "H": 52,
          "I": 11, "J": 11, "K": 62, "L": 15, "M": 7, "N": 14, "O": 7.5, "P": 8,
          "Q": 7, "R": 10.5, "S": 10.5, "T": 11, "U": 13, "V": 12.5, "W": 9.5,
          "X": 9.5, "Y": 11.5, "Z": 12, "AA": 8.5, "AB": 9, "AC": 11.5, "AD": 38,
          "AE": 11, "AF": 13, "AG": 12.5, "AH": 9, "AI": 20, "AJ": 13.5, "AK": 6,
          "AL": 21, "AM": 9}
for col, w in widths.items():
    ws.column_dimensions[col].width = w

# row heights (rough auto-fit for wrapped text)
for i, r in enumerate(LEDGER_ROWS, start=2):
    need = 1
    for key, chars in (("terms", 60), ("why", 75), ("cond_detail", 45), ("who", 30), ("when", 24), ("related", 24)):
        v = r.get(key)
        if v:
            need = max(need, len(str(v)) / chars)
    ws.row_dimensions[i].height = max(15, min(240, 13.2 * (need + 0.4)))

# expandable column groups (collapsed)
groups = [("O", "P"), ("Q", "Q"), ("R", "V"), ("W", "AA"), ("AB", "AC"), ("AD", "AD"),
          ("AE", "AG"), ("AH", "AJ"), ("AK", "AK"), ("AL", "AL"), ("AM", "AM")]
for a, b in groups:
    ws.column_dimensions.group(a, b, outline_level=1, hidden=True)

# data validation
LISTS = {
    "What happened": ["Target interest","Bidder interest","Target sale decision","Activist pressure","Activist involvement","Adviser engaged","Adviser service observed","Adviser ended","Contact","NDA signed","Round opened","Deadline set","Deadline revised","Deadline","Target decision","Information access changed","Material process update","Exclusivity changed","Bid","Bid reaffirmed","Offer update","Other-scope bid","Valuation statement","Bidding group changed","Joined group","Dropped by target","Withdrew","Did not submit","Participation paused","Re-entered","Not selected at signing","Sale process announced","Bid announced","Merger announced","Merger agreement signed","Go-shop changed","Process terminated","Process restarted","Agreement terminated","Closed"],
    "Type": ["Strategic","Financial","Mixed","Unknown"],
    "Formality": ["Formal","Informal","Insufficient evidence","Varies"],
    "Conditions level": ["None","Light","Heavy","Insufficient evidence","Varies"],
    "Include": ["Yes","No"],
    "Date basis": ["Reported day","Inferred day","Reported interval","Approximate window","Relative only","Undated"],
    "Date method": ["Reported","Inferred","Assigned: deadline","Assigned: decision day","Assigned: midpoint","Assigned: bound","Assigned: sequence"],
    "Price kind": ["Point","Bidder range","Group envelope","Bound only","Undisclosed"],
    "Price origin": ["Stated","Carried forward","Inferred"],
    "All cash": ["Yes","No","Not stated"],
    "Deadline treatment": ["Enforced","Extended","Late bids accepted","Passed without action","Unclear","No deadline stated"],
    "Round finality": ["Announced as final","Inferred final","Not final"],
    "Decided by": ["Bidder","Target","Both","Unknown"],
    "Exit reason": ["Value below market price","Value at or below market price","Value below earlier offer","Value at earlier offer","Would not improve earlier offer","Lower offer than rivals","Terms or process","Other stated reason","Not stated"],
    "Outcome basis": ["Stated","Inferred: residual","Inferred: exclusivity","Inferred: silent","Inferred: identity"],
}
LORDER = [k for k in HEADERS if k in LISTS] + [k for k in LISTS if k not in HEADERS]

wl = wb.create_sheet("Lists")
for j, key in enumerate(LORDER, start=1):
    wl.cell(row=1, column=j, value=key).font = Font(bold=True)
    for i, v in enumerate(LISTS[key], start=2):
        wl.cell(row=i, column=j, value=v)
    wl.column_dimensions[get_column_letter(j)].width = max(14, min(40, len(key) + 4))

dv_cache = {}
dv_map = {}
for key in LISTS:
    col_idx = HEADERS.index(key) + 1
    L = get_column_letter(col_idx)
    j = LORDER.index(key) + 1
    Lj = get_column_letter(j)
    n = len(LISTS[key]) + 1
    dv = DataValidation(type="list", formula1=f"Lists!${Lj}$2:${Lj}${n}", allow_blank=True)
    dv.error = "Use a value from the Lists sheet."
    dv.errorTitle = "Controlled category"
    ws.add_data_validation(dv)
    dv.add(f"{L}2:{L}{last}")

# conditional formatting: changed cells vs AI original (match by Row id)
red = DifferentialStyle(font=Font(color="C00000", bold=True))
rng = f"A2:{get_column_letter(NL)}{last}"
rule_new = Rule(type="expression", dxf=red, stopIfTrue=False,
                formula=[f'AND($O2<>"",ISNA(MATCH($O2,\'AI original\'!$O:$O,0)))'])
rule_chg = Rule(type="expression", dxf=red, stopIfTrue=False,
                formula=[f'AND($O2<>"",NOT(ISNA(MATCH($O2,\'AI original\'!$O:$O,0))),NOT(EXACT(""&INDEX(\'AI original\'!$A:$AM,MATCH($O2,\'AI original\'!$O:$O,0),COLUMN()),""&A2)))'])
ws.conditional_formatting.add(rng, rule_new)
ws.conditional_formatting.add(rng, rule_chg)

# ------------------------------------------------------------------ Source text
wst = wb.create_sheet("Source text")
wst.append(["Paragraph", "Section", "Page", "Text"])
wst.append(["—", "Note", None,
            "Text reproduced from the filing's HTML with layout-only normalization: whitespace collapsed to single spaces; non-breaking, thin and zero-width characters removed. Wording, qualifications, errors and meaningful punctuation preserved. Paragraph IDs were assigned by the extractor (the filing has no paragraph IDs). P-001–P-036 = the merger description and complete Background of the Merger (printed pp. 21–26), in source order, with the longest paragraph split into identified continuations. P-037–P-040 = the opening Reasons for the Merger passages used (p. 26). X-001 onward = additional filing passages, tables and annex text used by the ledger and Summary."])
for sid, sec, pg, txt in SRC:
    wst.append([sid, sec, pg, txt])
for c in wst[1]:
    c.font = hf; c.fill = hfill; c.alignment = Alignment(horizontal="center")
for col, w in {"A": 11, "B": 42, "C": 7, "D": 130}.items():
    wst.column_dimensions[col].width = w
wst.freeze_panes = "A2"
for row in wst.iter_rows(min_row=2):
    for c in row:
        c.alignment = Alignment(wrap_text=True, vertical="top")
# link from ledger Source cells to main source paragraph
for i, r in enumerate(LEDGER_ROWS, start=2):
    src = r.get("source") or ""
    first = src.split(";")[0].strip()
    rn = resolve_sid(first)
    cell = ws.cell(row=i, column=HEADERS.index("Source") + 1)
    if rn:
        try:
            cell.hyperlink = Hyperlink(ref=cell.coordinate, location=f"'Source text'!A{rn}")
            cell.font = Font(color="0563C1", underline="single")
        except Exception:
            pass

# row ids for cross-reference helper
row_of_id = {r["row_id"]: i for i, r in enumerate(LEDGER_ROWS, start=2)}

# ------------------------------------------------------------------ Summary
wsm = wb.create_sheet("Summary")
wsm.column_dimensions["A"].width = 34
wsm.column_dimensions["B"].width = 150

def sec(title):
    wsm.append([title, None])
    c = wsm.cell(row=wsm.max_row, column=1)
    c.font = Font(bold=True, size=12, color="1F4E78")

def line(label, text):
    wsm.append([label, text])
    wsm.cell(row=wsm.max_row, column=1).font = Font(bold=True)
    for c in wsm[wsm.max_row]:
        c.alignment = Alignment(wrap_text=True, vertical="top")

wsm.append(["PetSmart / Argos Holdings — deal ledger summary (first pass)", None])
wsm.cell(row=1, column=1).font = Font(bold=True, size=14)

sec("Status")
line("Status", "AI first pass; not human-approved. Instruction revision: 19 September 2026 (Pro). Supplied source: PetSmart, Inc. Definitive Proxy Statement (DEFM14A), filed 2015-02-02; source file raw_filing/petsmart_2015-02-02_DEFM14A.htm; background at printed pp. 21–26; annexes A–C included. Coverage: entire filing (85 numbered pages + annexes). Last recheck: not run since delivery; AI original mirrors the delivered ledger.")
line("Commercial account", "PetSmart's board was already reviewing strategic and capital-structure alternatives after a weak Q1 2014 earnings report when JANA Partners filed a 9.9% Schedule 13D (07/03/2014) and Longview publicly urged a sale (07/07/2014); the board decided on 08/13/2014 to explore strategic alternatives including a possible sale, announced the exploration on 08/19/2014 and retained J.P. Morgan (engagement letter effective 08/21/2014). J.P. Morgan was contacted by 27 potential participants (24 financial; 3 strategic) and the Company signed confidentiality and standstill agreements with 15 financial buyers in the first week of October 2014; six submitted non-binding indications of interest on 10/30/2014. On 11/03/2014 the board advanced the four bidders whose indications were at or above $80.00 — the Buyer Group (a BC Partners-led consortium), Bidder 2 and two unnamed finalists that were authorized to combine as “Bidder 3” — to a final round. Final bids on 12/10/2014 were $80.70 (Buyer Group) and $80.35 (Bidder 2) per share in cash; Bidder 3 dropped out. Asked to improve, Bidder 2 submitted a best-and-final $81.50 on 12/12/2014 while the Buyer Group moved from an oral $82.50 to a best-and-final $83.00; the board approved the Buyer Group's offer on 12/13/2014 and the merger agreement, Longview rollover and voting agreements were executed and announced on 12/14/2014. As of the 02/02/2015 proxy date no alternative proposal had emerged; closing (expected in the first half of 2015) is not observed in this filing.")

sec("Deal facts")
line("Target", "PetSmart, Inc. (Delaware; NASDAQ: PETM; 1,404 stores and 202 in-store boarding facilities in the United States, Canada and Puerto Rico) (p. 16).")
line("Focal acquirer", "Argos Holdings Inc. (“Parent”) and Argos Merger Sub Inc.; at closing owned by the Buyer Group — a consortium of funds advised by BC Partners, Inc., La Caisse de dépôt et placement du Québec, affiliates of GIC Special Investments Pte Ltd, affiliates of StepStone Group LP and, after 12/12/2014, Longview Asset Management, LLC. Type: Financial (PE-led consortium; Sources X-027, X-033).")
line("Agreed consideration", "$83.00 per share in cash; all cash; no CVR or contingent component (pp. 1–2, 21). Merger agreement dated as of 12/14/2014 (Annex A; X-032).")
line("Signing / announcement / completion", "Signed 12/14/2014; announced by joint press release 12/14/2014; expected closing first half of 2015 — no completion observed in this filing (R040, R041).")
line("Filing", "DEFM14A definitive proxy statement, dated/filed 02/02/2015 (t1500073-defm14a.htm); special meeting 03/06/2015; record date 01/29/2015; 99,455,151 shares outstanding on the record date (pp. 2, 17).")
line("Source file", "raw_filing/petsmart_2015-02-02_DEFM14A.htm (background pp. 21–26; annexes A–C).")
line("Market benchmarks", "Unaffected closing price 07/02/2014: $59.81 (premium of 38.8% per the filing, p. 26); closing 12/09/2014: $78.82; closing 12/12/2014 (last trading day before announcement): $77.67; closing 01/30/2015: $81.71 (pp. 34, 76).")

sec("Process and round map")
line("Process 1", "Single continuing sale attempt (08/2014–12/2014); outcome: signed with the Buyer Group 12/14/2014. No process termination, restart, exclusivity grant or competing post-signing proposal is reported; no multi-process assessment required (Q1).")
line("Round 0", "Pre-process (March–mid-August 2014): March authorization to contact Industry Participant, May earnings and stockholder communications, 06/18 board review and committee formation, JANA/Longview advocacy and the inbound contacts wave (R002–R010). No Round opened row required (section 6.3).")
line("Round 1", "Opened R011 (Working 10/01/2014; anchor = first confidentiality-agreement wave; rejected candidates kept at R006, R009, R013, R007/R008). Objective: solicit non-binding preliminary indications and select the final round. Participants: 15 financial NDA signers (R012). Deadline: 10/30/2014, treatment Enforced (R014). Finality: Not final (non-binding preliminary indications; no final/best-and-final solicitation and no move to definitive negotiation in this round). Ended with the 11/03/2014 selection; tally: 15 entering − 9 inferred non-submitters − 2 stated eliminations = 4 continuing.")
line("Round 2", "Opened R021 (11/03/2014; selection of the four bidders ≥$80.00). Objective: final-round diligence, definitive-document negotiation and final bids. Deadline history: initially 12/05/2014 (communication day not disclosed) → revised to the evening of 12/10/2014 (R027; Extended) → improved bids due 12/12/2014 (R033; 12/10 treated Extended, 12/12 Enforced) (R028, R033). Finality: Announced as final (the filing describes the final round and solicited final/best-and-final offers). Ended in signing: 4 entering independent units → 2 Joined closures + Bidder 3 = 3 units → Bidder 3 out (R032; Count 2 affected members) → Bidder 2 out at signing (R042) → 1 winner (Buyer Group).")
line("Post-signing", "R043: no unsolicited alternative proposal as of 02/02/2015; the 15 diligence parties' standstills bar higher bids after a definitive agreement; no go-shop period described. No competing proposal, agreement termination or closing reported.")
line("Auction screen", "MET — 15 independent prospective acquiring bidder units executed bidder-target confidentiality agreements for this process (all financial; no lender-only, adviser or rollover-holder agreements counted; Longview's confidentiality agreement with the Buyer Group is excluded; no earlier-attempt agreements reused). Evidence: R012 (p. 23).")

sec("Participants and advisers")
line("Buyer Group", "Financial (PE-led consortium of BC Partners, CDPQ, GIC affiliates, StepStone affiliates; Longview admitted as rollover supporter effective 12/12/2014). First bid: 10/30/2014 ($81.00–$83.00); final bids $80.70 (12/10) → oral $82.50 → best-and-final $83.00 (12/12); winner (no exit row). Carried Count 1 in Round 1 and 1 in Round 2.")
line("Bidder 2", "Financial (type derived from the cohort description “15 potentially interested financial buyers”, p. 23; flagged Q7). 10/30: $78.00 → $81.00–$84.00; 12/10: $80.35; 12/12: $81.50 best and final. Closed: Not selected at signing 12/14/2014, Outcome basis Stated (Lower offer than rivals).")
line("Unnamed financial bidder 1", "Financial. 10/30: $80.00–$85.00 range; advanced to the final round (R016). Possible identity as a Bidder 3 member — hypothesis only (Q3).")
line("Unnamed financial bidder 2", "Financial. 10/30: range reached at least $80.00 (endpoints not disclosed; Bound only); advanced to the final round (R017). Possible identity as a Bidder 3 member — hypothesis only (Q3).")
line("Two unnamed submitters", "Financial cohort of 2. 10/30: indications below $80.00, values not disclosed; closed Dropped by target 11/03/2014 (Stated; Lower offer than rivals).")
line("Bidder 3", "Combination of the two unnamed finalists (R023–R025); not an economic exit for its members. 12/10: valuation communication not above ~$78/share (R031); Did not submit (R032; Decided by Both; Value at or below market price; Count 2 units).")
line("Nine non-submitters", "Financial. 15 NDA signers − 6 submitters = 9; inferred Did not submit at the 10/30/2014 deadline (R045); Outcome basis Inferred: residual; Decided by Unknown; Not stated.")
line("Industry Participant", "Unnamed privately held strategic party. Bidder interest 08/07/2014; not invited to the process (Target decision by 08/27/2014); never entered — no exit row.")
line("Longview", "Long-term stockholder (managed ~9% of shares at the merger-agreement date). Advocacy 07/07/2014; rollover support formed 12/12/2014 (R034) and resolved 12/14/2014 (R039; 3,012,050 shares, ~$250 million; voting agreement over 7,424,591 shares ≈ 7.5%). Not a bidder; excluded from NDA counts.")
line("JANA Partners", "Activist stockholder; 9.9% 13D (07/03/2014) and public sale advocacy (R002).")
line("J.P. Morgan", "Financial adviser to PetSmart: retained July 2014; engagement letter effective 08/21/2014; fairness opinion 12/13–14/2014; fee up to ~$39 million. Disclosed conflicts: relationships with Buyer Group members worth ~$110 million over two years; James Crown (JPMorgan Chase board; Longview client) (pp. 30, 37, 45).")
line("Wachtell Lipton", "Legal adviser to PetSmart: service observed from 06/18/2014; retention date not disclosed (R001).")
line("Simpson Thacher", "Legal counsel to Parent/Merger Sub: first appearance as notice recipient (Attention: Ryerson Symons) in the executed merger agreement, page A-46 (R044); engagement date not disclosed (Q7).")
line("Other advisers", "Innisfree M&A Incorporated acted as proxy solicitation agent (p. 14); not carried as a deal adviser. Financing sources (not advisers): debt — Citigroup, Barclays, Deutsche Bank, Nomura, Jefferies with RBC, Macquarie and Natixis joinders; equity investors — BC European Capital IX-1 to 11 LP, Kokoro Investment Pte. Ltd., CDPQ, StepStone entities, Longview (X-018, X-033).")

sec("Counts and reconciliation")
line("Contacts", "Filing assertions: 27 potential participants contacted/inbound mid-August–end-October (3 strategic + 24 financial) (p. 23); “more than 25 potential participants” (p. 27); approximately 15 parties expressed interest as of 10/03/2014 (p. 23). Ledger: R007 Count 24 financial + R008 Count 3 strategic = 27. Industry Participant is separate and not counted in the 27.")
line("NDA units", "Filing assertion: 15 financial buyers signed confidentiality and standstill agreements in the first week of October 2014 (p. 23). Ledger formula (Count, NDA signed, Include=Yes): ")
line("Round 1 submitting units", "Filing assertions: “six of the potentially interested parties submitted indications of interest” (p. 24); reasons section: “received first round indications of interest from 5 bidder groups” (p. 27) — conflict preserved and reviewed (Q2). Ledger formula (Count, Bid, Round 1): ")
line("Round 1 residual non-submitters", "Formula (Count, Did not submit, Round 1): ")
line("Round 2 written bids", "Filing assertion: two final bid letters (Buyer Group; Bidder 2) plus one verbal indication (Bidder 3) on 12/10/2014 (p. 25). Ledger formula (Count, Bid, Round 2): ")
line("Per-stage balance", "Round 1: 15 entering (15 NDA signers) − 9 inferred non-submitters (R045) − 2 stated eliminations (R022) = 4 continuing units. Round 2: 4 independent units enter; the two unnamed finalists combine (R024, R025 close 2 independent units; Bidder 3 counts as one continuing unit) → 3 units; Bidder 3 exits (R032 — the combined unit's non-submission; Count 2 records the two affected members, not a second stock reduction) → 2 units; Bidder 2 exits at signing (R042) → 1 winner (Buyer Group). Unit balance: 4 − 2 + 1 − 1 − 1 = 1. Inferred share of exits: 9 of 14 unit closures (1 inferred row); all other closures are stated.")
line("Outcome tallies (occurrences/affected units, not unique firms)", "Dropped by target: 2 (R022). Did not submit: 11 (R045 9 + R032 2). Joined group: 2 (R024, R025). Not selected at signing: 1 (R042). Formula (Dropped): ")
line("Signing state", "At signing only the winner (Buyer Group) remains live; no go-shop expiry applies (none described).")

sec("Comparability and inputs")
line("Consideration structure", "All cash $83.00/share; no CVR, earnout or share alternative. Do not treat the ~$8.4 billion total funding need as equity value.")
line("Financing", "Total funds required ≈ $8.4 billion: debt up to ≈ $6.2 billion plus a $750 million ABL facility (≈ $6.95 billion of total facilities: $4.3bn TLB, $750m ABL, $1.9bn bridge/senior notes expected in lieu), cash equity commitments up to ≈ $1.83 billion, Longview rollover ≈ $250 million (3,012,050 shares) and ≈ $425 million of Company cash available at closing. No financing condition (pp. 5, 40–42).")
line("Termination fees", "$510 million Parent termination fee (funded by Buyer Group members other than Longview under commitment letters); $255 million Company termination fee in specified superior-proposal circumstances (pp. 28, 44–45).")
line("J.P. Morgan analyses (attributed, not offers)", "TV/LTM EBITDA reference 8.5x–11.0x → implied $70.50–$91.50 per share; public-multiples implied equity ranges $62.00–$83.00 (FV/EBITDA), $64.00–$82.50 (FV/adjusted EBITDA), $65.25–$77.75 (P/E); DCF sensitivity ranges $65.00–$95.25 (pp. 33–34, 36).")
line("Glossary", "NDA = confidentiality/non-disclosure agreement; IOI = indication of interest; LBO = leveraged buyout; rollover = holder contributes shares to the buyer's vehicle instead of taking cash; standstill = contractual bar on bid/proposal activity after a definitive agreement; go-shop = post-signing solicitation period (none described here); Superior Proposal = defined in the merger agreement (X-003).")

# fix the participants line for the nine non-submitters
for row in wsm.iter_rows():
    if row[0].value == "Nine non-submitters":
        row[1].value = "Financial. 15 NDA signers − 6 submitters = 9; inferred Did not submit at the 10/30/2014 deadline (R045); Outcome basis Inferred: residual; Decided by Unknown; Not stated."

# insert Count formulas as real formulas in column C
FORMULAS = {
 "NDA units": "=SUMIFS('Deal ledger'!$Q:$Q,'Deal ledger'!$D:$D,\"NDA signed\",'Deal ledger'!$P:$P,\"Yes\")",
 "Round 1 submitting units": "=SUMIFS('Deal ledger'!$Q:$Q,'Deal ledger'!$D:$D,\"Bid\",'Deal ledger'!$F:$F,1,'Deal ledger'!$P:$P,\"Yes\")",
 "Round 1 residual non-submitters": "=SUMIFS('Deal ledger'!$Q:$Q,'Deal ledger'!$D:$D,\"Did not submit\",'Deal ledger'!$F:$F,1,'Deal ledger'!$P:$P,\"Yes\")",
 "Round 2 written bids": "=SUMIFS('Deal ledger'!$Q:$Q,'Deal ledger'!$D:$D,\"Bid\",'Deal ledger'!$F:$F,2,'Deal ledger'!$P:$P,\"Yes\")",
 "Outcome tallies (occurrences/affected units, not unique firms)": "=SUMIFS('Deal ledger'!$Q:$Q,'Deal ledger'!$D:$D,\"Dropped by target\",'Deal ledger'!$P:$P,\"Yes\")",
}
for row in wsm.iter_rows():
    lab = row[0].value
    if lab in FORMULAS:
        wsm.cell(row=row[0].row, column=3, value=FORMULAS[lab]).font = Font(bold=True)
        wsm.cell(row=row[0].row, column=3).alignment = Alignment(wrap_text=True, vertical="top")

# ------------------------------------------------------------------ Questions
wsq = wb.create_sheet("Questions")
QH = ["Q", "Review topic", "Recommended answer", "Why and source", "Affected rows/fields",
      "Consequence of changing it", "Status", "Reviewer note"]
wsq.append(QH)
Q = []
Q.append([
 "Q1", "Process and round map (single process; R1 anchor; R2 finality; rejected alternatives)",
 "Keep one process (1) and two numbered rounds. R1 opens at the first confidentiality-agreement wave (first week of October 2014; R011, anchor recorded on the round row), Not final, ending with the 11/03/2014 selection. R2 opens at the 11/03/2014 finalist selection (R021), Announced as final, with deadline history 12/05 → 12/10 (Extended) → 12/12 (Enforced). Rejected R1 anchors, each kept as its own row: R006 (08/13 sale decision — planned outreach was late Sep/early Oct, not within about a week), R009 (08/19 announcement — supplemented, did not replace, solicitation), R013 (10/03 board meeting), R007/R008 (inbound contact wave mid-Aug–Oct). Rejected alternative: splitting a third round at the 12/04–05 final-bid instruction — rejected because the filing shows a final-bid plan (12/05 due) already inside the final round and the instruction only accelerated it; the 12/10 improvement request is a Deadline revised, not a new round (section 8.3).",
 "Background pp. 21–26; R011 anchor evidence: “In the first week of October 2014, the Company entered into confidentiality and standstill agreements with 15 potentially interested financial buyers” (p. 23); selection: “proceed to the final round of the sale process” (p. 24); deadline changes pp. 24–25; improvement instruction p. 25; finality signals pp. 25–26 (“final bids”, “best and final”).",
 "R006; R007; R008; R009; R011; R013; R021; R027; R028; R033 (Round, Date, Round finality, R1 anchor tag, # order)",
 "Moving R1 to 08/13, 08/19 or 10/03 would pull the contact wave and/or NDA solicitation into a different round and shift the 10/30 deadline history; splitting R2 would add a round and convert the 12/10 milestone into a round opening, changing Round and Round finality values.",
 "Pending", ""])
Q.append([
 "Q2", "Counts, base populations and overlaps (6 submitters vs 5 bidder groups; 15-signer base; Buyer Group as one unit; two eliminated submitters)",
 "Use the background's six submitting units — Buyer Group, Bidder 2, Unnamed financial bidder 1 ($80–85), Unnamed financial bidder 2 (≥$80), and the two unnamed below-$80 submitters (cohort) — and treat the 15 NDA signers as 15 bidder units with the Buyer Group as one unit throughout (its formation and whether its members signed separately are not disclosed). Residual non-submitters = 15 − 6 = 9 (R045; inferred). Preserve and flag the reasons-section conflict “received first round indications of interest from 5 bidder groups” (p. 27) against “six of the potentially interested parties submitted indications of interest” (p. 24): the background's specific six is preferred; the Summary shows both.",
 "p. 23 (“15 potentially interested financial buyers”); p. 24 (six submitters; four ≥$80 advanced); p. 27 (process summary; 5 bidder groups; two other bidding groups unwilling to make a definitive offer above $81.50).",
 "R007; R008; R012; R015–R020; R022; R045; Summary count block",
 "If the Buyer Group's members were separate NDA signers or submitted separately, the 15 − 6 = 9 residual and the four-finalist arithmetic change; if the reasons-section “5 groups” is preferred, the Round 1 bidder tally becomes 5 groups (still six parties) and the residual derivation must be restated.",
 "Pending", ""])
Q.append([
 "Q3", "Inferred closing rows and identity hypotheses (every inferred closing row, grouped by transition)",
 "Confirmed inferences: (a) 10/30/2014 — 9 non-submitters, Inferred: residual (15 − 6 = 9), Unknown/Not stated (R045); (b) 11/03/2014 — the 2 below-$80 submitters were Dropped by target, stated (R022); (c) the two finalists' combination — Joined group rows (R024, R025), stated; (d) 12/10/2014 — Bidder 3 Did not submit, stated, Both/Value at or below market price (R032); (e) 12/14/2014 — Bidder 2 Not selected at signing, stated (R042). Identity hypothesis only: the two unnamed finalists that combined (R023–R025) are most likely the same units as Unnamed financial bidders 1 and 2 (R016, R017), because they are the only finalists other than the Buyer Group and Bidder 2; not entered as settled identity. The two eliminated submitters (R022) sit inside the residual cohort derivation and are not individually identified.",
 "p. 24 (submissions; four ≥$80 advanced; two bidders authorized to work together as Bidder 3); p. 25 (Bidder 3 did not submit); p. 27 (Bidder 2's best and final).",
 "R016; R017; R020; R022; R045; R023–R025; R032; R042",
 "If the identity mapping is accepted, link the IOI rows to the Joined-group rows in Related rows; if rejected, the residual cohort derivation and “four finalists” description stay unchanged but two unnamed units remain unmapped to their IOIs.",
 "Pending", ""])
Q.append([
 "Q4", "Offers, formality and conditionality (round-1 IOIs; final bids; Bidder 3 valuation; oral $82.50)",
 "Round-1 IOIs: Informal formality; Conditions Heavy by context (non-binding preliminary indications in a two-stage process with a further substantial diligence stage; no financing or diligence condition stated in the filing). Alternative flagged: Insufficient evidence for conditions if context-based Heavy is rejected (the automatic Heavy-by-context rule presupposes no substantive diligence access, which these bidders had). Final bids (12/10: $80.70/$80.35; 12/12: $81.50/$82.50/$83.00): Formal (returned acquisition-agreement and transaction-document markups; best-and-final responses; price confirmation for Bidder 2) and Light (final-documentation condition only; Buyer Group committed financing evidenced 12/06; Bidder 2's commitment documents evidenced 12/12). Bidder 3's 12/10 communication is a Valuation statement, not a priced bid — no price cells, formality or conditions. Buyer Group's oral $82.50 and written $83.00 are retained as two Bid rows (price change preserved; same-evening sequence).",
 "p. 24 (non-binding preliminary indications; range details); p. 25 (12/10 bids; documents and financing commitments); p. 26 (12/12 offers; substantial executability; price confirmation); section 9 conventions.",
 "R015–R020 (Formality; Conditions level; Conditions detail); R029–R037 (same); R031 (Price kind/origin; formality blank); R036/R037 (# order same day); R035 (Count 0)",
 "Reclassifying IOI conditions as Insufficient evidence changes the Summary's conditionality picture but not counts; treating the oral $82.50 as part of one communication would drop a Bid row and shift Count; populating price cells for the $78 valuation would misstate it as a bid.",
 "Pending", ""])
Q.append([
 "Q5", "Deadlines and treatments (10/30; 12/05; 12/10; 12/12)",
 "Summary map: 10/30/2014 IOI deadline — Enforced (board selected finalists on the bids in hand); 12/05/2014 initial final-bid date — Extended (superseded before arrival; recorded only in the Deadline revised row R027, no milestone row per section 8.3); 12/10/2014 — Extended (the ad hoc committee required improved bids); 12/12/2014 — Enforced (improved bids received; board acted on 12/13). The 12/10 improvement request is a Deadline revised (old 12/10, new 12/12), not a fresh Deadline set and not a new round. No separate Deadline set rows: the 10/30 communication (during October; day not disclosed) is carried on R011/R014 and the 12/05 plan on R021/R027. No late bids were accepted; no exclusivity was granted at any stage (Exclusivity changed rows not applicable).",
 "pp. 23–26: IOI due date and submissions; 12/05 initial date and the 12/04–05 revision; 12/10 final bids; 12/12 improvement instruction and offers; 12/13 board action.",
 "R014; R027; R028; R033 (Due date; Deadline treatment); Summary map; R021 (initial 12/05 plan)",
 "Alternative treatments: calling 12/10 “Passed without action” is rejected (action followed); treating the improvement request as a new Deadline set would duplicate the history; moving the revision to R027 vs a new row does not change the map.",
 "Pending", ""])
Q.append([
 "Q6", "Prices, bounds and consideration (UFB2 bound; Bidder 2 date; rollover and voting figures; cash treatment)",
 "Retain as recommended: UFB2's ≥$80 as Bound only with the ambiguity flagged (floor on the whole range vs a level the range reached); Bidder 2's $78.00 on 10/30 (Reported) and its revision assigned Working 11/01 (midpoint of the 10/30–11/02 discussion window); all-cash Yes for the priced final bids and the signing (payment form not stated for the October indications, so All cash = Not stated there); Cash at closing populated only for point prices ($78.00, $80.70, $80.35, $81.50, $82.50, $83.00 and the signing). Longview rollover: 3,012,050 shares ≈ $250 million; voting agreement 7,424,591 shares ≈ 7.5%; Longview receives $83.00 cash for all other shares. No equity value was computed (the filing gives a funding requirement, not an equity value).",
 "p. 24 (ranges; the three bidders “reached at least $80.00”); p. 26 (12/12 offers); p. 27 ($250 million helpful to $83.00); p. 41 (rollover shares; same $83.00 for other shares); p. 45 (voting agreement shares); p. 5 (funding summary).",
 "R017 (Price low; Price kind; Terms tag); R019 (Working date; Date method); R015–R020; R029–R037 (All cash; Cash at closing); R034; R039; R040; Summary comparability",
 "Treating the ≥$80 as a submitted endpoint would imply an unknown floor; averaging ranges is prohibited; treating rollover shares as consideration for cashed-out shares would misstate the all-cash nature of the merger consideration.",
 "Pending", ""])
Q.append([
 "Q7", "Bidder and adviser types, clients and conflicts (Bidder 2/unnamed types; adviser dates; JPM conflicts)",
 "Bidder types as recommended: Buyer Group Financial; Bidder 2, Unnamed financial bidders 1–2 and the unnamed submitters Financial, derived from the cohort description “15 potentially interested financial buyers” (p. 23) — flag if the reviewer wants Unknown pending direct evidence; Industry Participant Strategic (privately held; unnamed). Advisers: J.P. Morgan engaged July 2014 (engagement letter effective 08/21/2014) — the unnamed “financial advisor” present at the 06/18/2014 board meeting is NOT attributed to J.P. Morgan; Wachtell Lipton service observed from 06/18/2014 (retention not disclosed); Simpson Thacher first appears as Parent-side notice counsel in the executed agreement (by 12/14/2014; engagement not disclosed). J.P. Morgan conflict disclosures: ~$110 million of two-year relationships with Buyer Group members and the James Crown/Longview connection (pp. 37, 45) — retained in R004 for reviewer awareness.",
 "p. 22 (JPM retention; Wachtell service); p. 23 (financial buyers); p. 30 (engagement letter); p. 37 (relationships); p. 45 (Crown); Annex A p. A-46 (notices).",
 "R004; R001; R044; R015–R020 (Type); Summary participants/advisers",
 "Changing types to Unknown would not change counts but would leave the winner's rivals unclassified; moving adviser Working dates without disclosed engagement dates would imply false precision.",
 "Pending", ""])
Q.append([
 "Q8", "Post-signing status, regulatory/litigation treatment and closing (single Summary line items)",
 "As delivered: post-signing competitive activity is represented by R043 (no unsolicited proposals as of 02/02/2015; standstills; no go-shop described). Regulatory milestones (HSR filings 12/24/2014, early termination 01/07/2015; Canadian ARC request 12/30/2014, ARC issued 01/14/2015) and the seven Delaware class actions (p. 52) are kept as Summary-only lines per section 4. No Closed row: closing (expected first half of 2015) is not observed in the supplied filing. No Agreement terminated, Process terminated or Go-shop changed events exist in the source.",
 "p. 6 (regulatory summary); p. 52 (regulatory; litigation); p. 28 (no unsolicited offer; standstills); p. 3 (expected timing).",
 "R043; Summary status/map; absence of Closed/termination rows",
 "If the reviewer wants regulatory events in the ledger, add Material process update rows post-signing (one per milestone) — not recommended; adding a Closed row would fabricate an unobserved event.",
 "Pending", ""])
for q in Q:
    wsq.append(q)
for c in wsq[1]:
    c.font = hf; c.fill = hfill; c.alignment = Alignment(wrap_text=True, horizontal="center")
for col, w in {"A": 5, "B": 34, "C": 72, "D": 60, "E": 34, "F": 46, "G": 9, "H": 16}.items():
    wsq.column_dimensions[col].width = w
wsq.freeze_panes = "A2"

# check results block (results from checks run on the delivered version)
CHECKS = [
 ("Check 1 — Coverage and materiality", "Passed",
  "All disclosed core offers (6 round-1 indications; 12/10 and 12/12 final bids; Bidder 3's valuation), contacts/NDAs, the information-access revision, selection, participation outcomes, signing and publicity are recorded. Routine legal-term exchanges (12/06 comments, 12/08 revised drafts) are folded into the related bids per section 9.1; regulatory and litigation items are Summary-only per section 4. Inferred closing (R045) and the R023–R025 combination are explicit."),
 ("Check 2 — Counts and population (incl. per-stage balance)", "Qualified",
  "Ledger-derived counts reconcile to the filing's round-level assertions: NDA units 15; Round 1 bid units 6; Round 1 inferred non-submitters 9; Round 2 bid units 2; Dropped 2; Joined 2; Not selected 1 (live SUMIFS formulas in the Summary count block). Per-stage balance: R1 15 − 9 − 2 = 4; R2 4 − 2 + 1 − 1 − 1 = 1 winner. Unresolved source limitation preserved rather than resolved: “5 bidder groups” (p. 27) vs six submitting parties (p. 24) and the Buyer-Group-as-one-unit assumption (Q2)."),
 ("Check 3 — Participation continuity", "Passed",
  "Every participant that entered (15 NDA signers, of which 6 submitted) is closed: 9 inferred non-submitters (R045), 2 Dropped (R022), 2 Joined (R024/R025) → Bidder 3, Bidder 3 Did not submit (R032), Bidder 2 Not selected at signing (R042); the winner has no exit row. No bid, reaffirmation or resumed diligence follows a recorded outcome, so no Re-entered rows are required. Industry Participant and Longview never entered as bidders and take no outcome rows."),
 ("Check 4 — Dates and order", "Passed",
  "Programmatic: Working dates never decrease with # as tie-break; each Working date lies inside its own Date from/Date to; Reported day ⟺ Reported method and Inferred day ⟺ Inferred method (no assigned date labelled Reported); deadline communication, due dates, expiry and signing are distinct; the 12/04–05 and 12/10 revisions and the R045 decimal # (19.5) preserve sequence. Not tested in a spreadsheet application (see Check 8)."),
 ("Check 5 — Offers and classifications", "Qualified",
  "Every Bid row carries Formality, Conditions level and a fixed-format Conditions detail string (regex-checked); price kinds/origins/currencies/cash flags match the text; the valuation statement is not priced; signing carries no bid-price or formality/conditionality cells. Qualification: the Round 1 IOI Conditions level rests on process context without a condition stated in the filing (alternative Insufficient evidence flagged, Q4), and UFB2's ≥$80 bound wording is ambiguous (Q6)."),
 ("Check 6 — Structure and consistency (tags, finality, pairs)", "Passed",
  "One opening record per round (R011 Not final; R021 Announced as final); R011 carries the R1 anchor tag and the rejected candidate row ids; every Deadline row has a treatment matching the Summary map; every inferred outcome row opens with its Outcome basis value; revisions reference prior rows (R019→R018; R035→R030; R037→R036; R039→R034); Source and Page are filled together; date basis/method pairs are valid."),
 ("Check 7 — Evidence (quotes, paragraphs, pages)", "Passed",
  "Every quoted segment (≥25 characters) in the ledger verified as a contiguous substring of the normalized filing text (all 45 rows); source paragraph ids resolve to Source text rows; the first source paragraph's printed page matches the Page column; cross-paragraph premises (standstills p. 28, rollover/voting pp. 41/45, no-proposal status p. 28) are cited to their own passages."),
 ("Check 8 — Review and workbook operation", "Qualified",
  "Verified in the saved file: sheet order and hidden state; freeze panes and autofilter; 15 controlled-column data validations pointing at Lists; collapsed expandable column groups (11 groups); 45 internal Source hyperlinks; 2 conditional-formatting rules (red bold for new/changed Row ids vs AI original); 5 live SUMIFS formulas; AI original matches the delivered ledger (values-only, same Row ids). Not tested in Excel: LibreOffice is incomplete in this environment (missing /usr/lib/libreoffice/share/registry/main.xcd), so formulas were not recalculated and hyperlinks/conditional formatting were not exercised in an application; formula results were independently recomputed in Python (15/6/9/2/2 as expected). No changed-cell highlights exist at delivery."),
]
wsq.append([])
wsq.append(["CHECK RESULTS (section 13) — computed on the delivered version", "", "", "", "", "", "", ""])
hdr = wsq.max_row
for c in wsq[hdr]:
    c.font = Font(bold=True, size=12, color="1F4E78")
for name, result, note in CHECKS:
    wsq.append([name, result, note])
    wsq.cell(row=wsq.max_row, column=1).font = Font(bold=True)

# ------------------------------------------------------------------ AI original
wa = wb.create_sheet("AI original")
wa.append(HEADERS)
for r in LEDGER_ROWS:
    wa.append([r.get(k) for k in LEDGER_KEYS])
for c in wa[1]:
    c.font = Font(bold=True)
wa.freeze_panes = "D2"
for col, w in widths.items():
    wa.column_dimensions[col].width = w
for row in wa.iter_rows(min_row=2):
    for c in row:
        c.alignment = Alignment(wrap_text=True, vertical="top")
for row in wa.iter_rows(min_row=2):
    for c in row:
        key = HEADERS[c.column - 1]
        v = c.value
        if key in ("Date from", "Date to", "Working date", "Due date") and isinstance(v, str):
            c.value = d(v); c.number_format = "MM/DD/YYYY"
        elif key in ("Price low", "Price high", "Cash at closing") and isinstance(v, (int, float)):
            c.number_format = "#,##0.00"
        elif key in ("Count", "Process", "Page") and isinstance(v, (int, float)):
            c.number_format = "0"

# hide support sheets
wl.sheet_state = "hidden"
wa.sheet_state = "hidden"

# visible sheet order: Deal ledger, Summary, Questions, Source text, then hidden support
order = ["Deal ledger", "Summary", "Questions", "Source text", "Lists", "AI original"]
wb._sheets = [wb[n] for n in order]

wb.save(OUT)
print("saved", OUT)
print("ledger rows:", last - 1)
print("source rows:", len(SRC))
print("sheets:", wb.sheetnames)
