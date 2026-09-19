# -*- coding: utf-8 -*-
"""Data for the PetSmart / Argos ledger (first pass)."""

DEAL = "PetSmart"

# ---------------------------------------------------------------- source paragraphs
# P rows: background pp. 21-26 (assembled in build.py from pages.json)
# X rows: additional passages used. Each entry: (id, section, page, text) - text pulled from pages.json
X_REFS = [
    ("X-001", "The Merger - Reasons for the Merger", "27", ("27", "3")),
    ("X-002", "The Merger - Reasons for the Merger", "28", ("28", "17")),
    ("X-003", "The Merger - Reasons for the Merger", "28", ("28", "20")),
    ("X-004", "The Merger - Reasons for the Merger", "28", ("28", "23")),
    ("X-005", "The Merger - Reasons for the Merger", "29", ("29", "9")),
    ("X-006", "The Merger - Opinion of J.P. Morgan", "30", ("30", "10")),
    ("X-007", "The Merger - Opinion of J.P. Morgan", "30", ("30", "11")),
    ("X-008", "The Merger - Opinion of J.P. Morgan", "34", ("34", "43")),
    ("X-009", "The Merger - Opinion of J.P. Morgan", "37", ("37", "2")),
    ("X-010", "The Merger - Projected Financial Information", "37", ("37", "6")),
    ("X-011", "The Merger - Financing", "40", ("40", "3")),
    ("X-012", "The Merger - Financing", "40", ("40", "5")),
    ("X-013", "The Merger - Financing", "40", ("40", "8")),
    ("X-014", "The Merger - Financing", "40", ("40", "11")),
    ("X-015", "The Merger - Financing", "40", ("40", "14")),
    ("X-016", "The Merger - Financing", "41", ("41", "2")),
    ("X-017", "The Merger - Financing", "41", ("41", "14")),
    ("X-018", "The Merger - Financing", "41", ("41", "16")),
    ("X-019", "The Merger - Financing", "42", ("42", "9")),
    ("X-020", "The Merger - Termination Fee Commitment Letters", "44", ("44", "9")),
    ("X-021", "The Merger - Termination Fee Commitment Letters", "45", ("45", "1")),
    ("X-022", "The Merger - Voting Support Agreement", "45", ("45", "14")),
    ("X-023", "The Merger - Regulatory Approvals", "52", ("52", "3")),
    ("X-024", "The Merger - Regulatory Approvals", "52", ("52", "6")),
    ("X-025", "The Merger - Litigation", "52", ("52", "8")),
    ("X-026", "Market Price of the Company's Common Stock", "76", ("76", "22")),
    ("X-027", "Summary", "1", ("1", "11")),
    ("X-028", "Summary", "1", ("1", "20")),
    ("X-029", "Summary", "2", ("2", "20")),
    ("X-030", "Summary", "5", ("5", "19")),
    ("X-031", "Summary", "5", ("5", "29")),
    ("X-032", "Annex A - Agreement and Plan of Merger", "A", ("98", "1")),
    ("X-033", "The Merger Agreement - Representations of Parent: Financing", "A-19", ("116", "6")),
    ("X-040", "The Merger - Opinion of J.P. Morgan", "37", ("37", "3")),
    ("X-038", "Summary - When the Merger Becomes Effective", "3", ("3", "34")),
    ("X-039", "Annex A - Notices", "A-46", None),  # assembled in build.py
]

# Additional X rows assembled from tables (text form)
X_TABLE = [
    ("X-034", "The Merger - Projected Financial Information (table, p. 38)",
     "38",
     "Projections provided to the board and J.P. Morgan and later made available to Parent, Merger Sub and members of the Buyer Group "
     "(dollars in million; fiscal year ends): Revenue - 2014E Jan-15: $7,081 | 2015E Jan-16: $7,456 | 2016E Jan-17: $7,869 | "
     "2017E Jan-18: $8,331 | 2018E Jan-19: $8,822 | 2019E Jan-20: $9,329. EBITDA (defined as earnings before interest, taxes, "
     "depreciation and amortization, adjusted to exclude one-time Profit Improvement Program costs incurred in Q3 2014) - "
     "$967 | $1,060 | $1,223 | $1,326 | $1,422 | $1,515. Net Income - $445 | $490 | $588 | $646 | $700 | $748. "
     "Cash Flow from Operations - $617 | $721 | $825 | $851 | $913 | $972."),
    ("X-035", "The Merger - Projected Financial Information (table, p. 39)",
     "39",
     "Projections provided to the board and J.P. Morgan but not made available to Parent, Merger Sub or Buyer Group members "
     "(dollars in million except per share; fiscal year ends): Adjusted EBITDA - 2014E Jan-15: $848 | 2015E Jan-16: $936 | "
     "2016E Jan-17: $1,088 | 2017E Jan-18: $1,181 | 2018E Jan-19: $1,269 | 2019E Jan-20: $1,352. Earnings Per Share - "
     "$4.45 | $5.01 | $6.37 | $7.39 | $8.44 | $9.50 (share counts assumed: 100.1m FY2014, 97.8m FY2015, 92.4m FY2016, "
     "87.4m FY2017, 82.9m FY2018, 78.8m FY2019). Unlevered Free Cash Flow - $404 | $506 | $595 | $605 | $652 | $695."),
    ("X-036", "The Merger - Projected Financial Information (table, p. 39)",
     "39",
     "Extrapolations for fiscal years 2020-2024 provided to the board and J.P. Morgan but not made available to Parent, Merger Sub or "
     "Buyer Group members (dollars in million; fiscal year ends): Revenue - 2020E Jan-21: $9,794 | 2021E Jan-22: $10,229 | "
     "2022E Jan-23: $10,597 | 2023E Jan-24: $10,883 | 2024E Jan-25: $11,101. Adjusted EBITDA - $1,419 | $1,482 | $1,536 | "
     "$1,577 | $1,609. Unlevered Free Cash Flow - $731 | $765 | $793 | $815 | $832."),
    ("X-037", "Market Price of the Company's Common Stock (table, p. 76)",
     "76",
     "Quarterly high/low sales prices: 2015 First Quarter (through January 30) high $81.95 / low $81.00. 2014: Q1 $72.04/$61.47; "
     "Q2 $70.12/$54.69; Q3 $72.35/$59.25; Q4 $81.97/$63.21. 2013: Q1 $68.99/$60.15; Q2 $69.89/$60.42; Q3 $70.95 (high, as printed) / "
     "$65.53; Q4 $75.36/$64.05."),
]

# ---------------------------------------------------------------- ledger rows
# column order used by the writer
LEDGER_KEYS = ["num", "when", "who", "what", "process", "round", "type", "terms",
               "formality", "conditions", "why", "source", "review", "reviewer_note",
               "row_id", "include", "count", "date_from", "date_to", "working",
               "date_basis", "date_method", "price_low", "price_high", "price_kind",
               "price_origin", "currency", "all_cash", "cash_close", "cond_detail",
               "due_date", "deadline_treat", "round_finality", "decided_by",
               "exit_reason", "outcome_basis", "page", "related", "deal"]

def R(**kw):
    d = {k: None for k in LEDGER_KEYS}
    d.update(kw)
    d["deal"] = DEAL
    d["include"] = "Yes"
    return d

rows = []

rows.append(R(
    row_id="R001", num=1,
    when="06/18/2014 (first service observed)",
    who="PetSmart — Wachtell, Lipton, Rosen & Katz (legal adviser)",
    what="Adviser service observed", process=1, round=0,
    terms="Legal adviser to PetSmart; observed advising the board at the 06/18/2014 meeting and throughout the process. Retention date not disclosed.",
    why="Service observed at the board meeting reviewing strategic and financial alternatives: “the board reviewed, together with a financial advisor and with Wachtell, Lipton, Rosen & Katz (“Wachtell Lipton”), its legal advisor, the various strategic and financial alternatives potentially available to the Company”. First narrative mention is not proof of retention on that date; no engagement date is reported (p. 21).",
    source="P-009", review="Q7", date_from="06/18/2014", date_to="06/18/2014",
    working="06/18/2014", date_basis="Reported day", date_method="Reported", page=21,
    related="R004 (co-adviser)",
))

rows.append(R(
    row_id="R002", num=2,
    when="07/03/2014; advocacy continued over July–August 2014",
    who="JANA Partners (activist stockholder)",
    what="Activist pressure", process=1, round=0,
    terms="Schedule 13D disclosing a 9.9% stake and intent to engage with management and the board on a strategic review including a sale; amendments and public letters advocating a sale over July–August; in-person meeting with Company representatives 07/10/2014.",
    why="Sale advocacy by a disclosed 9.9% holder: “JANA had acquired 9.9% of the Company’s outstanding common stock and that JANA intended to engage in discussions with management and the board with respect to a review of strategic alternatives, including a sale of the Company”; later “JANA Partners filed several amendments to its Schedule 13D and publicly disclosed letters to the board, advocating for a sale of PetSmart” (p. 22).",
    source="P-011", review="Q1", date_from="07/03/2014", date_to="08/31/2014",
    working="07/03/2014", date_basis="Reported interval", date_method="Assigned: bound", page=22,
))

rows.append(R(
    row_id="R003", num=3,
    when="07/07/2014 (letter); call 07/10/2014",
    who="Longview Asset Management (stockholder)",
    what="Activist pressure", process=1, round=0,
    terms="Public letter urging the board to consider a sale and stating Longview would consider rolling part or all of its holdings into acquirer equity rather than receive cash if needed to enable a transaction; long-term investor; reiterated sale advocacy in a 07/10/2014 call. Rollover support later formed 12/12/2014 (R034).",
    why="“Longview made public a letter to the board in which Longview stated that the board should consider the a sale of the Company (as well as other strategic alternatives)”; Longview said it “would consider, depending on the parties and terms involved, rolling part or all of its holdings into equity of the acquiring entity rather than receive cash consideration” (p. 22). The filing describes Longview as “a long-term investor” (p. 29).",
    source="P-011; P-020", review="Q7", date_from="07/07/2014", date_to="07/10/2014",
    working="07/07/2014", date_basis="Reported interval", date_method="Assigned: bound", page=22,
))

rows.append(R(
    row_id="R004", num=4,
    when="July 2014 (retained); engagement letter effective 08/21/2014",
    who="PetSmart — J.P. Morgan Securities LLC (financial adviser)",
    what="Adviser engaged", process=1, round=0,
    terms="Retained July 2014 after interviewing several candidates for M&A, valuation, financing and capital-markets experience; engagement letter effective 08/21/2014; rendered the board's fairness opinion (oral 12/13/2014; written 12/14/2014); fee up to approximately $39 million, a substantial portion payable only if the merger is consummated. Disclosed relationships with Buyer Group members of approximately $110 million over two years (p. 37) and a James Crown/Longview connection (p. 37, p. 45).",
    why="“In July, after interviewing several potential financial advisors, the Company retained J.P. Morgan as financial advisor” (p. 22). “Pursuant to an engagement letter effective as of August 21, 2014, the Company retained J.P. Morgan as its financial advisor in connection with a possible transaction” (p. 30).",
    source="P-010; X-006; X-009; X-040; X-022", review="Q7", date_from="07/01/2014", date_to="07/31/2014",
    working="07/16/2014", date_basis="Reported interval", date_method="Assigned: midpoint", page=22,
    related="R001 (co-adviser)",
))

rows.append(R(
    row_id="R005", num=5,
    when="08/07/2014",
    who="Industry Participant (unnamed privately held strategic party)",
    what="Bidder interest", process=1, round=0, type="Strategic",
    terms="Unpriced inbound approach: Industry Participant told J.P. Morgan it might be interested in re-visiting Spring 2014 discussions about a possible combination of the two companies if PetSmart pursued strategic alternatives. Scope: whole-company combination. Not invited into the process (R010).",
    why="“Industry Participant might be interested in re-visiting the conversations that had taken place in the Spring concerning the feasibility of a possible combination of the two Companies” (p. 22). Spring 2014 discussions were PetSmart-initiated explorations of acquiring Industry Participant, which said it was not for sale and raised antitrust concerns (p. 21); retained only as context.",
    source="P-012; P-007", review="Q7", date_from="08/07/2014", date_to="08/07/2014",
    working="08/07/2014", date_basis="Reported day", date_method="Reported", page=22,
    related="R010 (exclusion)",
))

rows.append(R(
    row_id="R006", num=6,
    when="08/13/2014",
    who="PetSmart board",
    what="Target sale decision", process=1, round=0,
    terms="Determined to explore strategic alternatives including a possible sale to maximize stockholder value; instructed management to plan the Profit Improvement Plan; authorized the ad hoc committee (Chairman Gregory Josefowicz; Rakesh Gangwal; Thomas Stemberg) to oversee the process; decided to announce the exploration publicly; planned J.P. Morgan outreach for the second half of September or early October 2014. Exploration, not an irrevocable commitment to sell.",
    why="“(1) determined to explore strategic alternatives (including a possible sale of the Company) for the Company to maximize value for stockholders including by commencing a process to determine the potential value that could be achieved via a sale of the Company”; “(3) authorized the ad hoc committee to oversee the sale exploration process” (p. 22).",
    source="P-013", review="Q1", date_from="08/13/2014", date_to="08/13/2014",
    working="08/13/2014", date_basis="Reported day", date_method="Reported", page=22,
))

rows.append(R(
    row_id="R007", num=7,
    when="mid-August through 10/31/2014",
    who="24 financial participants (cohort)",
    what="Contact", process=1, round=0, type="Financial",
    terms="Inbound sale-process contacts of the 27 potential participants disclosed for the period from the middle of August to the end of October 2014: 24 financial participants (potential lead buyers as well as large suppliers of equity capital to lead buyers). Spans the run-up to Round 1; assigned to Round 0 as the pre-opening contact wave.",
    why="“During this period, J.P. Morgan was contacted by 27 potential participants in a sale process, including three strategic parties (not counting Industry Participant) and 24 financial participants (including potential lead buyers as well as large suppliers of equity capital to lead buyers)” (p. 23). Date bounded by “since the August 13 board meeting” and “the middle of August through the end of October”. Conflict preserved: the reasons section states “more than 25 potential participants” (p. 27); the specific 27 is used and both are shown in the Summary.",
    source="P-016; P-017", review="Q1; Q2", count=24,
    date_from="08/14/2014", date_to="10/31/2014", working="08/14/2014",
    date_basis="Approximate window", date_method="Assigned: bound", page=23,
))

rows.append(R(
    row_id="R008", num=8,
    when="mid-August through 10/31/2014",
    who="3 strategic parties (cohort; excluding Industry Participant)",
    what="Contact", process=1, round=0, type="Strategic",
    terms="Strategic share of the 27 disclosed inbound contacts from the middle of August to the end of October 2014; no strategic party signed a non-disclosure agreement or submitted an indication of interest on the filing's account.",
    why="“including three strategic parties (not counting Industry Participant) and 24 financial participants” (p. 23). None of the 15 confidentiality agreements in the first week of October 2014 was with a strategic party (“15 potentially interested financial buyers”, p. 23).",
    source="P-016; P-018", review="Q2", count=3,
    date_from="08/14/2014", date_to="10/31/2014", working="08/14/2014",
    date_basis="Approximate window", date_method="Assigned: bound", page=23,
))

rows.append(R(
    row_id="R009", num=9,
    when="08/19/2014",
    who="PetSmart (issuer)",
    what="Sale process announced", process=1, round=0,
    terms="Press release issued concurrent with the second quarter earnings announcement: the Company determined to explore strategic alternatives including a possible sale to maximize stockholder value. Purpose included alerting parties not contacted so they could contact J.P. Morgan.",
    why="“On August 19, 2014, concurrent with its second quarter earnings announcement, the Company issued a press release announcing that it determined to explore strategic alternatives for the Company to maximize value for stockholders, including a possible sale of the Company” (p. 23).",
    source="P-014; P-013", review="Q1", date_from="08/19/2014", date_to="08/19/2014",
    working="08/19/2014", date_basis="Reported day", date_method="Reported", page=23,
))

rows.append(R(
    row_id="R010", num=10,
    when="by 08/27/2014 (committee direction after 08/13/2014; communicated 08/22 and 08/27/2014)",
    who="PetSmart board / ad hoc committee",
    what="Target decision", process=1, round=0,
    terms="Industry Participant not invited into the exploratory sale process because of the very high antitrust-clearance risk (near-certain second request; eight months to a year or longer, with no assurance of success), the risk of providing competitively advantageous information, and the risk of disrupting or delaying the process. J.P. Morgan communicated the concerns on 08/22; Industry Participant again expressed interest on 08/27; J.P. Morgan said it would not be invited but any proposal would be considered by the board; no contact since. Reaffirmed 10/03/2014 (R013).",
    why="Committee direction after the 08/13 meeting: “the ad hoc committee directed J.P. Morgan to communicate to Industry Participant the board’s concerns as a result of which Industry Participant would not be invited to participate in the exploratory process”; “The J.P. Morgan representative stated that Industry Participant would not be invited into the exploratory process, but that if Industry Participant were to wish to submit a proposal or other communication to the Company, the board would consider it. There has been no contact between PetSmart and Industry Participant (or between any of their respective representatives) since August 27, 2014” (p. 23).",
    source="P-015; P-014; P-017", review="Q1", date_from="08/13/2014", date_to="08/27/2014",
    working="08/27/2014", date_basis="Approximate window", date_method="Assigned: bound", page=23,
    related="R005 (IP interest)",
))

rows.append(R(
    row_id="R011", num=11,
    when="first week of October 2014 (10/01–10/07)",
    who="PetSmart / J.P. Morgan",
    what="Round opened", process=1, round=1,
    terms="R1 anchor: confidentiality-agreement wave — the Company entered into confidentiality and standstill agreements with 15 potentially interested financial buyers (R012). Purpose: solicit non-binding preliminary indications of interest (due 10/30/2014) and select the final round. Candidate anchors rejected and preserved as rows: R006 (08/13/2014 sale decision; planned outreach was for the second half of September/early October, not within about a week of the decision), R009 (08/19/2014 public announcement, which supplemented rather than replaced solicitation), R013 (10/03/2014 board meeting), R007/R008 (mid-August–October inbound contact wave, which the filing reports as contacts coming to J.P. Morgan).",
    why="The filing reports no dated target outreach wave; participants came to the target. The first target-organized step admitting participants to a stage is the confidentiality-agreement wave: “In the first week of October 2014, the Company entered into confidentiality and standstill agreements with 15 potentially interested financial buyers” (p. 23).",
    source="P-018; P-019; P-016; P-017", review="Q1",
    date_from="10/01/2014", date_to="10/07/2014", working="10/01/2014",
    date_basis="Approximate window", date_method="Assigned: bound", page=23,
    round_finality="Not final",
    related="R012 (anchor event); R006; R009; R013 (rejected candidates)",
))

rows.append(R(
    row_id="R012", num=12,
    when="first week of October 2014 (10/01–10/07)",
    who="15 financial buyers (cohort)",
    what="NDA signed", process=1, round=1, type="Financial",
    terms="Confidentiality and standstill agreements executed with 15 potentially interested financial buyers; all 15 engaged in due diligence during October, received management presentations with senior management, and received detailed financial and business-plan information including the Profit Improvement Plan. Standstill provisions bar these parties from submitting (or seeking permission to submit) a higher bid once a definitive transaction agreement is signed (R043).",
    why="“In the first week of October 2014, the Company entered into confidentiality and standstill agreements with 15 potentially interested financial buyers, all 15 of which, during the month of October engaged in due diligence, received management presentations involving the Company’s senior-most management, and received detailed financial and business plan information, including detailed information concerning the Profit Improvement Plan” (p. 23).",
    source="P-018; X-002", review="Q2", count=15,
    date_from="10/01/2014", date_to="10/07/2014", working="10/01/2014",
    date_basis="Approximate window", date_method="Assigned: bound", page=23,
    related="R011 (round anchor); R020 (below-$80 submitters); R045 (inferred non-submitters)",
))

rows.append(R(
    row_id="R013", num=13,
    when="10/03/2014",
    who="PetSmart board",
    what="Material process update", process=1, round=1,
    terms="Board updated on the sale process and the completed Profit Improvement Plan: approximately 15 parties had expressed interest among the 27 contacted; board reaffirmed, for the August reasons, the determination not to invite Industry Participant into the process. (Aggregate contacts are recorded at R007/R008.)",
    why="“the board was informed that approximately 15 parties had expressed interest in participating in the process”; “the board reviewed and, for the reasons discussed in August, reaffirmed the determination not to invite Industry Participant to participate in the sale process” (p. 23).",
    source="P-017", review="Q1", date_from="10/03/2014", date_to="10/03/2014",
    working="10/03/2014", date_basis="Reported day", date_method="Reported", page=23,
    related="R007; R008; R010",
))

rows.append(R(
    row_id="R014", num=14,
    when="10/30/2014",
    who="PetSmart (deadline for bidders)",
    what="Deadline", process=1, round=1,
    terms="Non-binding preliminary indications of interest due; six of the potentially interested parties submitted on this date; J.P. Morgan spoke with all parties, including non-submitters, from 10/30 to 11/02 about their rationales; the board reviewed the indications on 11/03 (R021). Deadline communicated during October 2014 (day not disclosed; carried on R011/R014).",
    why="“During October, the potential bidders were informed that non-binding preliminary indications of interest would be due on October 30, 2014”; “On October 30, six of the potentially interested parties submitted indications of interest” (p. 23–24).",
    source="P-019; P-021; P-022", review="Q5", date_from="10/30/2014", date_to="10/30/2014",
    working="10/30/2014", date_basis="Reported day", date_method="Reported", page=23,
    due_date="10/30/2014", deadline_treat="Enforced", related="R011; R021",
))

# ---- Round 1 IOIs -----------------------------------------------------------
IOI_DETAIL = "Fin: not stated; DD required: substantive (period not stated); DD open: yes; Excl: not stated"
IOI_WHY = ("Round 1 asked for “non-binding preliminary indications of interest” (p. 23); the bidder “submitted indications of interest” on the "
           "10/30/2014 deadline (p. 24). Preliminary non-binding indication in a two-stage process in which a further substantial diligence stage "
           "(November) and definitive documentation followed before any written final bid; financing not stated. Heavy by context; the filing attaches "
           "no financing or diligence condition to the indication itself.")

rows.append(R(
    row_id="R015", num=15,
    when="10/30/2014",
    who="Buyer Group (BC Partners-led consortium)",
    what="Bid", process=1, round=1, type="Financial",
    terms="Non-binding preliminary indication of a range of $81.00–$83.00 per share, in cash; one of the three submitters whose ranges reached at least $80.00; advanced to the final round on 11/03 (R021).",
    formality="Informal", conditions="Heavy",
    why=IOI_WHY + " Range: “the Buyer Group, which indicated a range of $81.00 to $83.00 per share” (p. 24).",
    source="P-021; P-019; P-022", review="Q4", count=1,
    date_from="10/30/2014", date_to="10/30/2014", working="10/30/2014",
    date_basis="Reported day", date_method="Reported",
    price_low=81.0, price_high=83.0, price_kind="Bidder range", price_origin="Stated",
    currency="USD", all_cash="Not stated", cond_detail=IOI_DETAIL, page=24,
    related="R029 (later bid); R021",
))

rows.append(R(
    row_id="R016", num=16,
    when="10/30/2014",
    who="Unnamed financial bidder 1 (IOI range $80.00–$85.00)",
    what="Bid", process=1, round=1, type="Financial",
    terms="Non-binding preliminary indication of a range of $80.00–$85.00 per share; one of the three submitters whose ranges reached at least $80.00; advanced to the final round (R021). Identity as a Bidder 3 member is a hypothesis only (Q3).",
    formality="Informal", conditions="Heavy",
    why=IOI_WHY + " “another bidder, which suggested a range of $80.00 to $85.00 per share” (p. 24).",
    source="P-021; P-022", review="Q4", count=1,
    date_from="10/30/2014", date_to="10/30/2014", working="10/30/2014",
    date_basis="Reported day", date_method="Reported",
    price_low=80.0, price_high=85.0, price_kind="Bidder range", price_origin="Stated",
    currency="USD", all_cash="Not stated", cond_detail=IOI_DETAIL, page=24,
    related="R021; R023–R025 (possible identity; Q3)",
))

rows.append(R(
    row_id="R017", num=17,
    when="10/30/2014",
    who="Unnamed financial bidder 2 (IOI range reached at least $80.00)",
    what="Bid", process=1, round=1, type="Financial",
    terms="Bound: ≥ $80 — one of the three bidders whose initially indicated ranges “reached at least $80.00 per share”; endpoints not disclosed; advanced to the final round (R021). Identity as a Bidder 3 member is a hypothesis only (Q3).",
    formality="Informal", conditions="Heavy",
    why=IOI_WHY + " “Three bidders initially indicated price ranges that reached at least $80.00 per share” (p. 24). The filing does not give this bidder's endpoints; the wording is ambiguous between a floor on the whole range and a level the range reached (Q6).",
    source="P-021; P-022", review="Q4; Q6", count=1,
    date_from="10/30/2014", date_to="10/30/2014", working="10/30/2014",
    date_basis="Reported day", date_method="Reported",
    price_low=80.0, price_kind="Bound only", price_origin="Stated",
    currency="USD", all_cash="Not stated", cond_detail=IOI_DETAIL, page=24,
    related="R021; R023–R025 (possible identity; Q3)",
))

rows.append(R(
    row_id="R018", num=18,
    when="10/30/2014",
    who="Bidder 2",
    what="Bid", process=1, round=1, type="Financial",
    terms="Non-binding preliminary indication of $78.00 per share; increased to a range of $81.00–$84.00 during 10/30–11/02 discussions (R019); advanced to the final round (R021).",
    formality="Informal", conditions="Heavy",
    why=IOI_WHY + " “another bidder (which we refer to as “Bidder 2”), which had initially indicated a price of $78.00” (p. 24).",
    source="P-021; P-019", review="Q4", count=1,
    date_from="10/30/2014", date_to="10/30/2014", working="10/30/2014",
    date_basis="Reported day", date_method="Reported",
    price_low=78.0, price_high=78.0, price_kind="Point", price_origin="Stated",
    currency="USD", all_cash="Not stated", cash_close=78.0, cond_detail=IOI_DETAIL, page=24,
    related="R019 (revises); R021",
))

rows.append(R(
    row_id="R020", num=20,
    when="10/30/2014",
    who="2 unnamed financial submitters (cohort; indications below $80.00)",
    what="Bid", process=1, round=1, type="Financial",
    terms="Two of the six submitters indicated prices below $80.00 per share; values not disclosed; not advanced to the final round (closed at R022). Count 2 = the two submitting units; no individual prices exist in the filing.",
    formality="Informal", conditions="Heavy",
    why=IOI_WHY + " Six parties submitted on 10/30 and only four “bidders that had indicated a price or range at or above $80.00” were allowed to proceed (p. 24), leaving two submitters below the threshold whose prices are not disclosed (p. 24).",
    source="P-021; P-022", review="Q2", count=2,
    date_from="10/30/2014", date_to="10/30/2014", working="10/30/2014",
    date_basis="Reported day", date_method="Reported",
    price_kind="Undisclosed", all_cash="Not stated", cond_detail=IOI_DETAIL, page=24,
    related="R022 (dropped)",
))

# Inferred residual cohort (id R045; new unused identifier per instruction)
rows.append(R(
    row_id="R045", num=20.5,
    when="by 10/30/2014",
    who="9 unnamed financial NDA signers (cohort; no indication submitted)",
    what="Did not submit", process=1, round=1, type="Financial",
    terms="Inferred: residual — 15 NDA signers − 6 submitters = 9 non-submitters; no indication of interest reported from these signers by the 10/30/2014 deadline. CLOSED by inference; no decision date, motive or voluntary withdrawal is inferred, and no individual rows are created for anonymous members.",
    why="Base and continuing set from the same passages: “In the first week of October 2014, the Company entered into confidentiality and standstill agreements with 15 potentially interested financial buyers” (p. 23); “On October 30, six of the potentially interested parties submitted indications of interest” (p. 24). Arithmetic 15 − 6 = 9. Base assumes every submitter was among the 15 signers and that the Buyer Group counts as one signer/unit (Q2).",
    source="P-018; P-021; P-022", review="Q2; Q3", count=9,
    date_from="10/30/2014", working="10/30/2014",
    date_basis="Relative only", date_method="Assigned: deadline",
    decided_by="Unknown", exit_reason="Not stated", outcome_basis="Inferred: residual", page=23,
    related="R012 (base population); R015–R020 (submitters)",
))

rows.append(R(
    row_id="R019", num=19,
    when="10/30–11/02/2014; day not disclosed",
    who="Bidder 2",
    what="Bid", process=1, round=1, type="Financial",
    terms="Revised indication of $81.00–$84.00 per share after J.P. Morgan's 10/30–11/02 calls; first Bid row for this bidder in the round (R018) carries the Count.",
    formality="Informal", conditions="Heavy",
    why=IOI_WHY + " “As a result of its discussions with J.P. Morgan, another bidder (which we refer to as “Bidder 2”), which had initially indicated a price of $78.00, increased its indication to a range of $81.00 to $84.00 per share” (p. 24). Discussions ran 10/30–11/02; the revision day is not disclosed.",
    source="P-021", review="Q6", count=0,
    date_from="10/30/2014", date_to="11/02/2014", working="11/01/2014",
    date_basis="Reported interval", date_method="Assigned: midpoint",
    price_low=81.0, price_high=84.0, price_kind="Bidder range", price_origin="Stated",
    currency="USD", all_cash="Not stated", cond_detail=IOI_DETAIL, page=24,
    related="revises R018; R021",
))

# ---- Round 2 -----------------------------------------------------------------
rows.append(R(
    row_id="R021", num=21,
    when="11/03/2014",
    who="PetSmart board",
    what="Round opened", process=1, round=2,
    terms="Board selected the four bidders whose indications were at or above $80.00 per share (Buyer Group, Bidder 2 and two unnamed bidders) to proceed to the final round of the sale process. Purpose: final-round diligence, negotiation of definitive documentation and final bids; the Company circulated a form of merger agreement with instructions to submit comments together with final bids (p. 24). Final bids were initially planned for 12/05/2014 (communication date not disclosed), then revised to 12/10 and an improvement deadline of 12/12 (R027, R028, R033).",
    why="“The board determined to allow the four bidders that had indicated a price or range at or above $80.00 per share to proceed to the final round of the sale process” (p. 24). The filing calls this stage the final round and the later solicitation was for “final bids” and “best and final” offers (pp. 24–26).",
    source="P-022; P-025; P-026", review="Q1",
    date_from="11/03/2014", date_to="11/03/2014", working="11/03/2014",
    date_basis="Reported day", date_method="Reported", page=24,
    round_finality="Announced as final",
    related="R011 (prior round); R022; R027",
))

rows.append(R(
    row_id="R022", num=22,
    when="by 11/03/2014 (notified after the board meeting; day not disclosed)",
    who="2 unnamed financial submitters (cohort; indications below $80.00)",
    what="Dropped by target", process=1, round=1, type="Financial",
    terms="Notified by J.P. Morgan following the 11/03 board meeting that they were eliminated; none indicated any interest or ability to remain in the process at price levels above their own initial indications. Excluded from the final round (Round 2).",
    why="“Following this meeting, representatives of J.P. Morgan notified the eliminated parties, none of which indicated any interest or ability to remain in the process at price levels above their respective initial indications” (p. 24).",
    source="P-022; P-021", review="Q3", count=2,
    date_from="11/03/2014", working="11/03/2014",
    date_basis="Relative only", date_method="Assigned: decision day",
    decided_by="Target", exit_reason="Lower offer than rivals", outcome_basis="Stated", page=24,
    related="R020 (their bids); R021",
))

rows.append(R(
    row_id="R023", num=23,
    when="after 11/03/2014; day not disclosed",
    who="Unnamed finalist (sought equity partner); Unnamed finalist (would exit unless permitted to partner) → Bidder 3",
    what="Bidding group changed", process=1, round=2,
    terms="Formation of “Bidder 3”: two of the four final-round bidders requested, and the ad hoc committee authorized, working together — one had indicated a desire to work with an equity partner given the size of a PetSmart acquisition, the other had said it would drop out of the process if not permitted to work together; they had worked together on previous large leveraged buyouts. Composition: 4 independent final-round units → 3; the net units −1 is effected through the two Joined group rows (R024, R025); this row states the composition and carries no unit change of its own. Count 2 = members affected.",
    why="“Two of the bidders (one of which had been invited into the final round but had indicated a desire to work with an equity partner in light of the size of an acquisition of PetSmart, and the other of which had indicated to J.P. Morgan that it would drop out of the process if not permitted to work together with another bidder) requested permission to work together.”; “the ad hoc committee authorized these two bidders to work together. We refer to these two bidders together as “Bidder 3.”” (p. 24).",
    source="P-023; P-022", review="Q3", count=2,
    date_from="11/03/2014", working="11/03/2014",
    date_basis="Relative only", date_method="Assigned: bound", page=24,
    related="R024; R025; R032",
))

rows.append(R(
    row_id="R024", num=24,
    when="after 11/03/2014; day not disclosed",
    who="Unnamed finalist (sought equity partner)",
    what="Joined group", process=1, round=2, type="Financial",
    terms="Joined Bidder 3 (with the other unnamed finalist); independent participation closed. Stage count falls by one: 4 independent units → 3 with Bidder 3 counting as one unit. Not an economic exit.",
    why="One of the two finalists that “requested permission to work together”; “the ad hoc committee authorized these two bidders to work together. We refer to these two bidders together as “Bidder 3.”” (p. 24). Closing of the independent unit follows section 5.3; net unit effect stated once on this row.",
    source="P-023", review="Q3", count=1,
    date_from="11/03/2014", working="11/03/2014",
    date_basis="Relative only", date_method="Assigned: bound",
    outcome_basis="Stated", page=24,
    related="R023 (formation); R025",
))

rows.append(R(
    row_id="R025", num=25,
    when="after 11/03/2014; day not disclosed",
    who="Unnamed finalist (would exit unless permitted to partner)",
    what="Joined group", process=1, round=2, type="Financial",
    terms="Joined Bidder 3 (with the other unnamed finalist); independent participation closed; no separate count effect — the net 4 → 3 unit change is recorded once at R024.",
    why="One of the two finalists that “requested permission to work together”; “the ad hoc committee authorized these two bidders to work together. We refer to these two bidders together as “Bidder 3.”” (p. 24).",
    source="P-023", review="Q3", count=1,
    date_from="11/03/2014", working="11/03/2014",
    date_basis="Relative only", date_method="Assigned: bound",
    outcome_basis="Stated", page=24,
    related="R023 (formation); R024",
))

rows.append(R(
    row_id="R026", num=26,
    when="November 2014; after the third quarter earnings announcement (day not disclosed)",
    who="PetSmart / J.P. Morgan",
    what="Information access changed", process=1, round=2,
    terms="Updated FY2014 financial projections: following the Q3 earnings announcement, at the request of bidders and the direction of the board, J.P. Morgan provided the bidders with updates to the Company's FY2014 projections. FY2014–FY2019 projections had earlier been provided to the board and J.P. Morgan, with portions made available to Parent, Merger Sub and Buyer Group members; FY2020–2024 extrapolations and certain metrics were provided to the board and J.P. Morgan only (R026 covers the revision of projections after bidding began; the update was given to the bidders alike).",
    why="“Following the Company’s third quarter earnings announcement and, at the request of bidders and the direction of the board and the Company, representatives of J.P. Morgan provided the bidders with updates to the Company’s fiscal year 2014 financial projections” (p. 24); “Following the release of the Company’s third fiscal quarter financial results, selected income statement line items for fiscal year 2014 only were updated to reflect actual performance and better visibility into the performance of the Company’s profit improvement plan”; “Portions of these projections were also made available to Parent, Merger Sub and members of the Buyer Group in connection with their respective consideration and evaluation of a merger with the Company” (p. 37).",
    source="P-024; X-010; X-034; X-035; X-036", review="Q1",
    date_from="11/01/2014", date_to="11/30/2014", working="11/15/2014",
    date_basis="Reported interval", date_method="Assigned: midpoint", page=24,
))

rows.append(R(
    row_id="R027", num=27,
    when="12/04–12/05/2014; due date changed from 12/05/2014 to the evening of 12/10/2014",
    who="PetSmart ad hoc committee / J.P. Morgan",
    what="Deadline revised", process=1, round=2,
    terms="Extension: the initial plan set Friday 12/05/2014 as the date for submission of bids (communication day not disclosed; the board had targeted 12/15/2014 for completion); on 12/04–12/05 the ad hoc committee concluded matters could be accomplished faster and set the evening of Wednesday 12/10/2014 as the deadline for final bids (five rather than ten days before the anticipated completion date), reducing leak/public-disclosure risk. Bidders were asked to submit mark-ups of the merger agreement, other transaction documents and financing commitments in advance. Due date field carries the superseded 12/05/2014 date; no separate milestone row for it per section 8.3.",
    why="“The board had initially targeted Monday, December 15 for completion of the sale process, and had initially set Friday, December 5 as the date for submission of bids”; “on December 4 and December 5, 2014, after consultation with the Company’s financial and legal advisors, the ad hoc committee concluded that these matters could be accomplished in a shorter period of time”; “the Company set the evening of Wednesday, December 10 (five days, rather than 10 days prior to the anticipated December 15 completion date) as the deadline for submission of final bids” (pp. 24–25).",
    source="P-025; P-026", review="Q5",
    date_from="12/04/2014", date_to="12/05/2014", working="12/04/2014",
    date_basis="Reported interval", date_method="Assigned: bound", page=24,
    due_date="12/05/2014", deadline_treat="Extended",
    related="R021; R028",
))

rows.append(R(
    row_id="R028", num=28,
    when="12/10/2014 (evening)",
    who="PetSmart (deadline for finalists)",
    what="Deadline", process=1, round=2,
    terms="Final bids due; received in writing from the Buyer Group and Bidder 2 with revised transaction documents; Bidder 3 gave only a verbal indication and no written offer (R031, R032). The ad hoc committee then required improved bids (R033).",
    why="“the Company set the evening of Wednesday, December 10 (five days, rather than 10 days prior to the anticipated December 15 completion date) as the deadline for submission of final bids” (p. 25); “On December 10, PetSmart received final bid letters along with revised versions of the merger agreement and other transaction documents from the Buyer Group and from Bidder 2 and a verbal indication from Bidder 3” (p. 25).",
    source="P-026; P-030; P-031", review="Q5",
    date_from="12/10/2014", date_to="12/10/2014", working="12/10/2014",
    date_basis="Reported day", date_method="Reported", page=25,
    due_date="12/10/2014", deadline_treat="Extended",
    related="R027; R033",
))

rows.append(R(
    row_id="R029", num=29,
    when="12/10/2014",
    who="Buyer Group",
    what="Bid", process=1, round=2, type="Financial",
    terms="Final bid letter: $80.70 per share, in cash, with revised versions of the merger agreement and other transaction documents; financing commitment documents provided 12/06/2014 (p. 25); docs described as more favorable to the Company, less conditional and reflecting substantially more acceptance of the Company's positions. Bid not dependent on a Longview rollover.",
    formality="Formal", conditions="Light",
    why="“The Buyer Group offered $80.70 per share, in cash” (p. 25). Formal signal: “revised versions of the merger agreement and other transaction documents”; the Buyer Group's documents were “more favorable to the Company (including because they were less conditional and more likely to be completed and because they offered more certainty of protection for the Company in the unlikely event of non-completion of the transaction)” and “reflected substantially more acceptance of the Company’s positions” (p. 25); financing commitments provided (p. 25). Heavy triggers absent; the bid remained subject to final documentation; no diligence or financing condition is reported.",
    source="P-030; P-027", review="Q4", count=1,
    date_from="12/10/2014", date_to="12/10/2014", working="12/10/2014",
    date_basis="Reported day", date_method="Reported",
    price_low=80.7, price_high=80.7, price_kind="Point", price_origin="Stated",
    currency="USD", all_cash="Yes", cash_close=80.7,
    cond_detail="Fin: committed; DD required: not stated; DD open: not disclosed; Excl: not stated",
    page=25, related="R015 (initial indication); R037 (revised)",
))

rows.append(R(
    row_id="R030", num=30,
    when="12/10/2014",
    who="Bidder 2",
    what="Bid", process=1, round=2, type="Financial",
    terms="Final bid letter: $80.35 per share, in cash, with revised versions of the merger agreement and other transaction documents; indicated any Longview partnering would occur only after execution of a definitive agreement; bid not dependent on a Longview rollover.",
    formality="Formal", conditions="Light",
    why="“Bidder 2 offered $80.35 per share, in cash” (p. 25); “final bid letters along with revised versions of the merger agreement and other transaction documents” (p. 25). No Heavy trigger reported; the bid remained subject to final documentation; financing not stated at this date (commitment documents appear with the 12/12 submission, p. 26).",
    source="P-030; P-031", review="Q4", count=1,
    date_from="12/10/2014", date_to="12/10/2014", working="12/10/2014",
    date_basis="Reported day", date_method="Reported",
    price_low=80.35, price_high=80.35, price_kind="Point", price_origin="Stated",
    currency="USD", all_cash="Yes", cash_close=80.35,
    cond_detail="Fin: not stated; DD required: not stated; DD open: not disclosed; Excl: not stated",
    page=25, related="R019 (earlier indication); R035 (revised)",
))

rows.append(R(
    row_id="R031", num=31,
    when="12/10/2014",
    who="Bidder 3 (combined finalist group)",
    what="Valuation statement", process=1, round=2,
    terms="Verbal communication that its valuation would not be above the current stock price of approximately $78 per share; J.P. Morgan told Bidder 3 it was unlikely to be competitive. Treated as a valuation statement, not a priced bid: no per-share bid cells populated and no formality/conditionality assessment.",
    why="“Bidder 3 verbally communicated to J.P. Morgan that their valuation would not be above the current stock price of approximately $78 per share. J.P. Morgan communicated to Bidder 3 that it was unlikely to be competitive and accordingly Bidder 3 did not submit a written offer” (p. 25). A valuation statement is not an offer (section 9.4).",
    source="P-030", review="Q4", working="12/10/2014",
    date_from="12/10/2014", date_to="12/10/2014",
    date_basis="Reported day", date_method="Reported", page=25,
    related="R032; R023",
))

rows.append(R(
    row_id="R032", num=32,
    when="by 12/10/2014 (final bid deadline; no written offer submitted)",
    who="Bidder 3 (combined finalist group)",
    what="Did not submit", process=1, round=2, type="Financial",
    terms="No written final bid after J.P. Morgan told Bidder 3 its indication was unlikely to be competitive. Affects the two combined units (Count 2); the combination itself is recorded at R023–R025. Exit from the final round.",
    why="“J.P. Morgan communicated to Bidder 3 that it was unlikely to be competitive and accordingly Bidder 3 did not submit a written offer” (p. 25). Mixed mechanism — target discouragement followed by non-participation (Decided by Both).",
    source="P-030; P-023", review="Q3; Q4", count=2,
    date_from="12/10/2014", working="12/10/2014",
    date_basis="Relative only", date_method="Assigned: deadline",
    decided_by="Both", exit_reason="Value at or below market price",
    outcome_basis="Stated", page=25, related="R031 (valuation); R023–R025",
))

rows.append(R(
    row_id="R033", num=33,
    when="12/10/2014; improved bids due 12/12/2014",
    who="PetSmart ad hoc committee / J.P. Morgan",
    what="Deadline revised", process=1, round=2,
    terms="Extension and improvement request after the 12/10 deadline had passed: neither bid was viewed as the bidders' best offers and the bids were close; the ad hoc committee instructed J.P. Morgan to tell each bidder it needed to increase and to submit improved bids on 12/12/2014. J.P. Morgan confirmed to Bidder 2 on the evening of 12/12 that $81.50 was its best and final offer; both remaining bidders submitted improved offers that evening (R035–R037). The 12/12 date was reached and no further extension followed; the board acted on the bids in hand on 12/13.",
    why="“the ad hoc committee instructed J.P. Morgan to inform each bidder that it would need to increase its bid, and to instruct the bidders to submit improved bids on December 12, 2014” (p. 25); “neither of the bids represented the bidders’ respective best offers” (p. 25). Deadline revised, not a new round or fresh deadline set (section 8.3).",
    source="P-031; P-034", review="Q5",
    date_from="12/10/2014", date_to="12/10/2014", working="12/10/2014",
    date_basis="Reported day", date_method="Reported", page=25,
    due_date="12/12/2014", deadline_treat="Enforced",
    related="R028 (prior due date); R035; R037",
))

rows.append(R(
    row_id="R034", num=34,
    when="12/12/2014 (request early in the day; approval and confidentiality agreement later the same day)",
    who="Buyer Group / Longview (rollover support)",
    what="Material process update", process=1, round=2,
    terms="Rollover support formed/permitted: the Buyer Group requested permission to work more closely with Longview to include a rollover of a portion of Longview-managed shares in its bid, saying this might help achieve a higher price; the ad hoc committee approved; Longview and the Buyer Group executed a confidentiality agreement permitting exchange of detailed information including bid price (not previously shared); Wachtell Lipton instructed to provide a voting-agreement form to Longview. History: Longview offered a rollover on 07/07/2014; in October bidders were told Longview would roll up to 7.5 million shares on terms and price acceptable to Longview and were asked to indicate interest (not a participation condition); J.P. Morgan confirmed Longview's continued interest on the evening of 12/11/2014. Rollover support is not a bidding-group membership change.",
    why="“the Buyer Group requested permission to work more closely with Longview in order to include a rollover of a portion of the Company shares managed by Longview in the Buyer Group’s bid”; “After consultation with the Company’s financial and legal advisors, the ad hoc committee approved the Buyer Group’s request” (p. 25); “later that day, Longview and the Buyer Group entered into a confidentiality agreement permitting the exchange of detailed information between them, including bid price” (p. 26); October disclosure: “Longview had informed the Company that it would be willing to “roll-over” up to 7.5 million shares on terms and price acceptable to Longview” (p. 23).",
    source="P-032; P-033; P-031; P-019; P-020", review="Q6",
    date_from="12/12/2014", date_to="12/12/2014", working="12/12/2014",
    date_basis="Reported day", date_method="Reported", page=25,
    related="R039 (resolved); R037; R003",
))

rows.append(R(
    row_id="R035", num=35,
    when="12/12/2014 (evening)",
    who="Bidder 2",
    what="Bid", process=1, round=2, type="Financial",
    terms="Improved best-and-final offer: $81.50 per share, in cash, with a revised draft merger agreement and other transaction agreements and copies of its financing commitment documents; J.P. Morgan confirmed the same evening that $81.50 was Bidder 2's best and final offer.",
    formality="Formal", conditions="Light",
    why="“Bidder 2 submitted an offer of $81.50 per share, in cash.”; “Representatives of J.P. Morgan confirmed via a conversation with Bidder 2 on the evening of December 12, 2014 that $81.50 per share was its best and final offer” (p. 26); “each bidder submitted a revised draft of the merger agreement and other transaction agreements, and copies of their respective financing commitment documents” (p. 26). Responded to the established best-and-final solicitation (Formal); no Heavy trigger reported.",
    source="P-034; P-031", review="Q4", count=0,
    date_from="12/12/2014", date_to="12/12/2014", working="12/12/2014",
    date_basis="Reported day", date_method="Reported",
    price_low=81.5, price_high=81.5, price_kind="Point", price_origin="Stated",
    currency="USD", all_cash="Yes", cash_close=81.5,
    cond_detail="Fin: committed; DD required: not stated; DD open: not disclosed; Excl: not stated",
    page=26, related="revises R030; R042",
))

rows.append(R(
    row_id="R036", num=36,
    when="12/12/2014 (evening)",
    who="Buyer Group",
    what="Bid", process=1, round=2, type="Financial",
    terms="Oral improved offer of $82.50 per share, in cash; stated it was working to increase within the next few hours; superseded later the same evening (R037).",
    formality="Formal", conditions="Light",
    why="“The Buyer Group initially submitted an oral offer of $82.50 per share, in cash, but stated that it was working to increase the offer within the next few hours” (p. 26). Formal documentation carried forward from the 12/10 submission (p. 25) and the revised drafts submitted the same evening (p. 26).",
    source="P-034; P-030", review="Q4; Q6", count=0,
    date_from="12/12/2014", date_to="12/12/2014", working="12/12/2014",
    date_basis="Reported day", date_method="Reported",
    price_low=82.5, price_high=82.5, price_kind="Point", price_origin="Stated",
    currency="USD", all_cash="Yes", cash_close=82.5,
    cond_detail="Fin: committed; DD required: not stated; DD open: not disclosed; Excl: not stated",
    page=26, related="R037 (supersedes); R029",
))

rows.append(R(
    row_id="R037", num=37,
    when="12/12/2014 (evening)",
    who="Buyer Group",
    what="Bid", process=1, round=2, type="Financial",
    terms="Best-and-final offer of $83.00 per share, in cash, submitted with a revised merger agreement and other transaction agreements (“with few exceptions, in substantially executable form”) and financing commitment documents; the Buyer Group said that after increasing from $82.50 to $83.00 some or all members were unwilling or unable to offer additional consideration; Longview's $250 million rollover participation was described as helpful in achieving $83.00. Winning bid (R040).",
    formality="Formal", conditions="Light",
    why="“Later in the evening, the Buyer Group submitted a best and final offer of $83.00 per share, in cash. In addition, each bidder submitted a revised draft of the merger agreement and other transaction agreements, and copies of their respective financing commitment documents. The versions submitted by the Buyer Group were, with few exceptions, in substantially executable form” (p. 26); “Longview’s willingness to participate in the Buyer Group with respect to $250 million of the common stock was helpful in achieving an $83.00 per share price” (p. 27).",
    source="P-034; X-001", review="Q4", count=0,
    date_from="12/12/2014", date_to="12/12/2014", working="12/12/2014",
    date_basis="Reported day", date_method="Reported",
    price_low=83.0, price_high=83.0, price_kind="Point", price_origin="Stated",
    currency="USD", all_cash="Yes", cash_close=83.0,
    cond_detail="Fin: committed; DD required: not stated; DD open: not disclosed; Excl: not stated",
    page=26, related="revises R036; R029; R040",
))

rows.append(R(
    row_id="R038", num=38,
    when="12/13/2014",
    who="PetSmart board",
    what="Target decision", process=1, round=2,
    terms="Board reviewed the final bids and selected the Buyer Group; J.P. Morgan rendered its oral fairness opinion on the $83.00 all-cash consideration (written opinion 12/14/2014); the board unanimously determined the merger advisable and recommended adoption, subject to confirmation that remaining open points in the merger agreement were satisfactorily resolved, with authority to reconvene if needed.",
    why="“the merger consideration of $83.00 in cash to be paid to the holders of the Company’s common stock in the merger was fair, from a financial point of view, to such holders”; “the board unanimously determined that the merger agreement and the transactions contemplated thereby, including the merger, were advisable and in the best interests of PetSmart and its stockholders”; “The board’s determination was subject, however, to confirmation that the remaining open points in the merger agreement had been satisfactorily resolved” (p. 26).",
    source="P-035; X-007", review="Q1", working="12/13/2014",
    date_from="12/13/2014", date_to="12/13/2014",
    date_basis="Reported day", date_method="Reported", page=26,
    related="R037; R040",
))

rows.append(R(
    row_id="R039", num=39,
    when="12/14/2014",
    who="Parent / Longview (rollover support)",
    what="Material process update", process=1, round=2,
    terms="Rollover support resolved: Parent and Longview entered into the rollover agreement — Longview contributes 3,012,050 shares (approximately $250 million worth) to Parent immediately before the effective time in exchange for equity interests in Parent; Longview receives the same $83.00 per share cash consideration for all other shares. Voting agreement among the Company, Parent and Longview covering 7,424,591 shares (approximately 7.5% of shares outstanding on the record date) to vote for the merger, subject to exceptions including a board change of recommendation.",
    why="“On December 14, 2014, the Parent and Longview entered into a rollover agreement (the “rollover agreement”) under which Longview has agreed to contribute 3,012,050 shares (“rollover shares”) to Parent immediately prior to the effective time in exchange for equity interests in Parent” (p. 41); “Longview will receive the same $83.00 per share merger consideration as the other holders of the Company’s common stock for all other shares of common stock beneficially owned by it (other than the rollover shares)” (p. 41); voting agreement: “to vote or cause to be voted 7,424,591 shares of common stock, which represent approximately 7.5% of the total outstanding shares” (p. 45).",
    source="X-016; X-017; X-022", review="Q6",
    date_from="12/14/2014", date_to="12/14/2014", working="12/14/2014",
    date_basis="Reported day", date_method="Reported", page=41,
    related="R034 (formed); R040",
))

rows.append(R(
    row_id="R040", num=40,
    when="12/14/2014",
    who="PetSmart; Argos Holdings Inc. (Parent); Argos Merger Sub Inc.",
    what="Merger agreement signed", process=1, round=2,
    terms="Agreed consideration $83.00 per share in cash (all-cash; no CVR or contingent component). Merger agreement dated as of 12/14/2014 executed with the Longview rollover and voting agreements, equity commitment letters from the Buyer Group (up to approximately $1.83 billion), termination fee commitment letters (aggregate cap $510 million) and committed debt financing (up to $6.95 billion of facilities; no financing condition to the merger). At closing Parent will be owned by the Buyer Group (BC Partners funds, La Caisse de dépôt et placement du Québec, affiliates of GIC Special Investments, affiliates of StepStone Group, Longview).",
    why="“On December 14, 2014, the parties executed the merger agreement, the voting agreement and related transaction agreements and issued a press release announcing the transaction” (p. 26); “each share of common stock outstanding at the effective time of the merger”; “will be cancelled and converted into the right to receive $83.00 in cash” (front letter); rollover/equity commitments (pp. 40–41). Signing is not an additional bid; price cells and formality/conditionality cells left blank per instruction.",
    source="P-036; X-032; X-031; X-015; X-018; X-020; X-021", review="Q6",
    date_from="12/14/2014", date_to="12/14/2014", working="12/14/2014",
    date_basis="Reported day", date_method="Reported",
    currency="USD", all_cash="Yes", cash_close=83.0, page=26,
    related="R037 (winning bid); R041; R043",
))

rows.append(R(
    row_id="R041", num=41,
    when="12/14/2014",
    who="PetSmart / Parent (issuer)",
    what="Merger announced", process=1, round=2,
    terms="Press release issued 12/14/2014 announcing the transaction: merger at $83.00 per share in cash; Parent to be owned by the Buyer Group; expected closing in the first half of 2015 (subject to stockholder adoption and other conditions).",
    why="“On December 14, 2014, the parties executed the merger agreement, the voting agreement and related transaction agreements and issued a press release announcing the transaction” (p. 26); expected timing: “We anticipate completing the merger in the first half of 2015” (p. 3).",
    source="P-036; X-038", review="Q8", working="12/14/2014",
    date_from="12/14/2014", date_to="12/14/2014",
    date_basis="Reported day", date_method="Reported", page=26,
    related="R040",
))

rows.append(R(
    row_id="R042", num=42,
    when="by 12/14/2014 (signing)",
    who="Bidder 2",
    what="Not selected at signing", process=1, round=2, type="Financial",
    terms="Bidder 2's $81.50 best-and-final offer (lower than the winning $83.00) was not selected; the board noted Bidder 2 had informed the Company its $81.50 was best and final. Bidder 2 remained willing to accommodate a Longview rollover only after execution of a merger agreement with it. No further participation reported.",
    why="“ultimately negotiated with the Buyer Group as well as two other bidding groups, neither of which was willing to make a definitive offer at a price above $81.50, which was lower than the $83.00 price offered by the Buyer Group.”; “The board noted that Bidder 2 had informed the Company’s representatives that $81.50 per share was its best and final offer” (p. 27).",
    source="X-001; P-035; P-034", review="Q3", count=1,
    date_from="12/14/2014", working="12/14/2014",
    date_basis="Relative only", date_method="Assigned: bound",
    decided_by="Target", exit_reason="Lower offer than rivals",
    outcome_basis="Stated", page=27, related="R035 (its final offer); R040",
))

rows.append(R(
    row_id="R043", num=43,
    when="as of 02/02/2015",
    who="PetSmart",
    what="Material process update", process=1, round="post",
    terms="Post-signing: as of the proxy date no person had made an unsolicited offer or proposal to acquire PetSmart. The 15 parties that engaged in due diligence are subject to standstill provisions preventing them from submitting (or even seeking permission to submit) a higher bid once a definitive transaction agreement was signed. The filing describes no post-signing solicitation (go-shop) period. No competing proposal, agreement termination or closing is reported.",
    why="“the fact that as of February 2, 2015, the date of this proxy statement, no person has made an unsolicited offer or proposal to acquire PetSmart” (p. 28); “the confidentiality agreements entered into by the 15 potentially interested parties that engaged in due diligence contained standstill provisions that prevent those parties from submitting (or even seeking permission to submit) a higher bid once the Company entered into a definitive transaction agreement with the winning sale process participant” (p. 28).",
    source="X-004; X-002; P-036", review="Q8",
    date_from="02/02/2015", date_to="02/02/2015", working="02/02/2015",
    date_basis="Reported day", date_method="Reported", page=28,
    related="R040",
))

rows.append(R(
    row_id="R044", num=44,
    when="by 12/14/2014 (first appearance; earlier service not disclosed)",
    who="Parent / Merger Sub — Simpson Thacher & Bartlett LLP (legal counsel)",
    what="Adviser service observed", process=1, round=2,
    terms="Counsel to Parent and Merger Sub; identified as the Parent-side notice recipient in the executed merger agreement (Attention: Ryerson Symons). First appearance in the filing is the 12/14/2014 agreement; no engagement date disclosed. Flagged for review with adviser client affiliations (Q7).",
    why="Merger agreement notice provision: “Simpson Thacher and Bartlett LLP 425 Lexington Avenue New York, NY 10017” and “Attention: Ryerson Symons” in the Parent/Merger Sub notice block (Annex A). First narrative mention is not proof of retention that day; the earliest supported date is the execution of the agreement.",
    source="X-039", review="Q7", page="A-46",
    date_from="12/14/2014", working="12/14/2014",
    date_basis="Relative only", date_method="Assigned: bound",
))

# reorder: the post-signing status row (R043) must come last; R044 (adviser, 12/14) before it
i44 = [i for i, r in enumerate(rows) if r["row_id"] == "R044"][0]
row44 = rows.pop(i44)
i43 = [i for i, r in enumerate(rows) if r["row_id"] == "R043"][0]
rows.insert(i43, row44)

# assign "#" by list position (R045 keeps a decimal insertion value)
for i, r in enumerate(rows, 1):
    r["num"] = i
for r in rows:
    if r["row_id"] == "R045":
        r["num"] = r["num"] - 0.5
ids = [r["row_id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate row ids"

LEDGER_ROWS = rows
