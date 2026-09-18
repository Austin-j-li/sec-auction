# Audit notes, 18 September 2026

Five read-only audits run before editing the extraction instructions. Each section is the reader's own report, unedited. Known corrections to these reports are listed at the end.


---

# A. Alex's nine reference blocks: how his worksheet actually works

# Alex's `deal_details_Alex_2026.xlsx` — evidence-based description

Scope: 269 rows in the nine trusted blocks. 7 of those Alex marks for deletion (Saks 7013–7015 pink "Bad" style; Penford 6461–6464 grey fill) → **262 valid rows**. Counts below are over all 269 unless noted.

## 1. Column inventory

**No column has `hidden=True`, none has width 0, there is no outline grouping.** Alex made columns "invisible" by narrowing them to width ≈0.8–1.55 (`<cols>` in `xl/worksheets/sheet1.xml`). Columns with *no* `<col>` entry (J, Z, AD, AI) keep the default width ~8.4, i.e. visible.

| Col | Header | Width / visible? | Content in the 9 blocks | Non-"NA" rows |
|---|---|---|---|---|
| A | *(blank header)* | 7.09 vis | deal index int (6879 etc.), constant per deal | 269 |
| B | TargetName | 24.1 vis | block key | 269 |
| C | gvkeyT | **0.91 invis** | constant | 269 |
| D | DealNumber | **1.09 invis** | SDC id, constant | 269 |
| E | Acquirer | 12.8 vis | constant per deal **except MacGray**: E6934–E6960 = `CSC purchased by Pamplona in May/2013` (black font, i.e. RA's) | 269 |
| F | gvkeyA | **1.09 invis** | mostly NA | 105 |
| G | DateAnnounced | 10.5 vis | constant | 269 |
| H | DateEffective | 10.0 vis | constant | 269 |
| I | DateFiled | **0.82 invis** | constant | 269 |
| J | FormType | *(no entry)* vis | DEFM14A / SC TO-T | 269 |
| K | URL | 7.8 vis | filing link, constant | 269 |
| L | Auction | 6.8 vis | always 1 | 269 |
| M | BidderID | 7.9 vis | **event sequence number**, fractional for inserted events | 269 |
| N | BidderName | 15.5 vis | bidder / IB / cohort label; NA on pure marker rows | 225 |
| O–R | bidder_type_financial / _strategic / _mixed / _nonUS | **1.54/1.36/1.09/1.00 invis** | 0/1 dummies, NA on 75 rows | 194 each |
| S | bidder_type_note | 10.5 vis | the field Alex actually uses | 204 |
| T | bid_value | 8.5 vis | = per-share price; **= lower bound when a range** | 75 |
| U | bid_value_pershare | 13.3 vis | equals T everywhere except 7013 | 74 |
| V | bid_value_lower | 10.0 vis | = T; the only populated value in "at least $X" bids | 79 |
| W | bid_value_upper | 10.5 vis | = T for point bids, upper for ranges | 75 |
| X | bid_value_unit | **1.36 invis** | `dollar` ×80, `billion` ×1 (7013, to be deleted) | 81 |
| Y | multiplier | **1.00 invis** | 1 ×80, 1e9 ×1 (7013) | 81 |
| Z | bid_type | *(no entry)* vis | Formal 23 / Informal 58 | 81 |
| AA | bid_date_precise | **0.82 invis** | **not maintained** — see §3 | 187 |
| AB | bid_date_rough | 10.7 vis | **the working date column** | 267 |
| AC | bid_note | 18.6 vis | event label | 188 |
| AD | all_cash | *(no entry)* vis | 1 ×52, 0 ×1 (6954), `'NA '` ×1 (6073, trailing space) | 54 |
| AE | additional_note | 8.8 vis | **empty in all 269 rows** | 0 |
| AF | cshoc | 8.7 vis | shares outstanding, only 4 deals | 47 |
| AG–AH | comments_1/2 | 30.2 / 13.8 vis | free text | 73 / 40 |
| AI | comments_3 | *(no entry)* vis | one cell only (AI6095) | 1 |

**Really used:** B, E, G, H, K, M, N, S, T/U/V/W, Z, AB, AC, AD, AG, AH. **Carried along:** A, C, D, F, I, J, L, O–R, X, Y, AA, AE, AF.

## 2. Vocabularies

**`bid_note` (AC), 28 distinct, 188 populated; 81 rows are bid rows with AC = NA.**
NDA 52 · Drop 44 · DropTarget 12 · IB 10 · Executed 10 · Final Round Ann 8 · Final Round 8 · Final Round Inf Ann 7 · Final Round Inf 7 · Bidder Interest 6 · Bidder Sale 3 · Final Round Ext Ann 3 · Final Round Ext 3 · Target Sale 2 · Activist Sale 1 · Target Sale Public 1 · Sale Press Release 1 · Bid Press Release 1 · DropAtInf 1 · DropBelowInf 1 · Terminated 1 · Restarted 1 · **Target Interest 1 (AC6928)** · **IB Terminated 1 (AC6929)** · **Exclusivity 30 days 1 (AC6405)** · **Final Round Inf Ext Ann 1 (AC6943)** · **Final Round Inf Ext 1 (AC6948)**.

- **Not in the written instructions:** `Target Interest`, `IB Terminated`, `Exclusivity 30 days`, `Final Round Inf Ext Ann`, `Final Round Inf Ext` (the Ext×Inf cross-product is implied but never spelled out).
- **In the instructions, never used:** `DropBelowM`; plain `Press Release` (only the two refinements `Sale Press Release` / `Bid Press Release` appear).
- **Divergence from instructions:** §3.5 says record Formal/Informal *in Bid Note*; in the sheet it lives in `bid_type` (Z) and bid rows carry AC = NA. Only one row has both (Z6054 Formal + AC6054 Executed).

**`bid_type` (Z):** Formal 23, Informal 58, NA 188.
**`bidder_type_note` (S):** F 99 · S 91 · NA 65 · `Non-US public S` 9 · `S/F` 3 (P&W consortium 6051/6052/6057) · `11S, 14F` 1 (S6027) · `S and F` 1 (S6387).
**`all_cash` (AD):** 1 ×52, 0 ×1, `'NA '` ×1, NA ×215. 29 of the 81 bid rows have no all_cash.
**`bid_value_unit` (X) / `multiplier` (Y):** `dollar`/1 ×80; `billion`/1000000000 ×1 — **only at 7013, the row Alex says to delete**. The enterprise-value machinery has zero trusted use.

## 3. Row-shape conventions

**Rows per deal:** P&W 36 · Medivation 16 · Imprivata 29 · Zep 23 · PetSmart 53 · Penford 25 (21 valid) · MacGray 34 · Saks 25 (22 valid) · sTec 28.

- **Bid row** (e.g. 6090): N, O–R, S, T=U=V, W, X=dollar, Y=1, **Z=Informal/Formal, AC=NA**, AD sometimes.
- **NDA row** (6083): N, type, all price fields NA, Z=NA, **AC=NDA**.
- **Drop row** (6042): N, type, AC=Drop/DropTarget/DropAtInf/DropBelowInf, no price.
- **Round/deadline row** (6032, 6040, 6045, 6058): **N=NA, O–S=NA**, only AB + AC.
- **IB row** (6025, 6385, 6408): N = bank name, O–S usually NA, AC=IB. Exception S6996 = `F` for Goldman Sachs (wrong; instructions say leave type blank).
- **Executed row** (6059, 6104, 6460): own row, N = winner, **S filled but O–R = NA**, no price, AC=Executed. AB ≈ signing date: = DateAnnounced at 6104/6407/6460, G−1 at 6485/6960/7018/7171, G−2 at 6073, G−3 at 6059.
- **Winning-bid rows keep AC = NA:** Alex *removed* labels in red at AC6103, AC7016, AC7170 and added a separate Executed row instead.

**Cohorts:** `16 parties` (N6030), `9 parties` (6029), `2 parties` (6031), `1 party` (6043), `24 parties` (6387), `19 parties` (6392), `16 financial bidders` (6934), `25 parties, including Parties A, B` (6027), `Several parties, including Sanofi` (6065), `5 parties, 4F and 1S` (N6390, red). Type split goes in **S**: `11S, 14F` (S6027), `S and F` (S6387), with O=P=Q=1.
**Consortia / joint bidders:** slash notation in N — `Party E/F` (6051–6057), `CSC/Pamplona` (6937–6960), `Sponsor A/E` (7005–7015), with S = `S/F` where mixed.
**Unnamed bidders:** `Unnamed party 1..12`, `Bidder 1..3`, `Strategic 1..3`, `Sponsor A/B/E/G`, `Another financial sponsor` (N6085/6087, red — Alex's replacement for a blank).

**Ranges:** T = U = V = **lower bound**, W = upper (6029 17.93/26.5; 6091 17/18; 6390 20/22; 6395 21.5/23). "At least $X" bids store **V only** (6428, 6998, 6999, 7153). Price-less informal bids exist (6429, 6430: unit=dollar, all four values NA).

**Fractional BidderID:** inserted events get .3/.5/.7/.8/.9/.95 before ID 1 (6024=0.3, 6025=0.5, 6026=0.7; PetSmart 0.7/0.8/0.9/0.95) and .5/.3/.7 between integers (6040=13.5, 6450=38.2, 6451=38.3, 6453=38.7). Ordering is by **event sequence, not date**: AB is non-monotone at 6087, 6436, 6935.

**AA vs AB.** AB is populated on 267/269 rows (missing: 7012, 7014). AA disagrees with AB on **37 rows, all of them red**. AA is *not* a maintained "precise date": on red rows it is a copy of a neighbouring row's AA (6066/6068/6069 ← 08/14 from 6070; 6088/6093 ← 06/09 from 6090–6092; 6099/6102 ← 06/24 from 6098; 7165–7167 ← 05/16 from 7162; 6960 ← 09/21 from 6957; 7144–7146 ← 04/04 from 7147). **6054** is row 6035 duplicated wholesale (Party B, 24, Formal, AA 07/20) with only AB→08/04 and AC→Executed changed — which is why it is the unique row carrying both `bid_type` and `bid_note`. **6059** is the reverse: AA=08/15 = DateAnnounced while AB=08/12 = the last bid date. Treat AA as noise; AB is the date. (Inference, stated as such.)

**Vague dates → start of period, recorded in AB:** "Early July" → 07/01 (AB6033), "Mid-June" → 06/15 (AB6032), "5/6–6/9" → 05/06 (AB6080), "over the next few weeks" → 05/23 (AB6399), "In February 2013" → 02/15 (AB6997), "In late May" → 06/03 (AB7004).

**Drops are both:** grouped (6030 "16 parties", 6075, 6392, 6399, 6942) and one-per-bidder (6046–6049; 6436–6443). Re-entry after a drop is recorded as a new bid row with comment "Reengaged" (6050, 6051 after DropTarget 6047).

## 4. Red-font cells

Red = `FFFF0000`. 2,649 red cells; 78 rows are **wholly new** (every field red) and ~30 rows are **single-field corrections**.

| Deal | red cells | new rows | field-level corrections |
|---|---|---|---|
| P&W | 200 | 8 (6024,6025,6026,6040,6045,6054,6058,6059) | N/S/AB 6027; AC 6031,6032,6046–6049; AB 6033; **Z 6036, 6041 (Formal→Informal)** |
| Medivation | 143 | 7 (6060,6062,6063,6066,6068,6069,6073) | — |
| Imprivata | 210 | 9 (6076,6077,6079,6088,6093,6095,6099,6102,6104) | N 6085,6087; AC 6097 (DropAtInf), 6100 (DropBelowInf), 6103 (→NA) |
| Zep | 195 | 9 (6385,6386,6389,6393,6394,6398,6401,6402,6407) | N 6390; AB 6399,6400,6403,6406; AC 6405 |
| PetSmart | 310 | 15 | N/AB 6435; AB+AC 6444,6445 (DropTarget) |
| Penford | 107 | 5 (6465,6467,6477,6481,6485) | AC 6470 (NDA); AB 6478 |
| MacGray | 237 | 11 | AB 6936; AC 6951,6958,6959 |
| Saks | 93 | 4 (6996,6997,7011,7018) | AB 7004,7005,7007; AC 7006,7016 |
| sTec | 220 | 10 | AC 7154,7155,7170; **Z 7169** |

By column: AC 99 · AB 92 · N 83 · Z 81 · S 79 · M/O–R/T–Y/AA/AD–AF 78 each · AG 70 · AH 40.
**What Alex adds most:** process-scaffolding rows the RAs never collected — IB (10), Executed (10), Final Round Ann/Inf/Ext family (29 of 36), start-of-process rows (Bidder Interest/Bidder Sale/Target Sale/Activist Sale/press releases, 15). **What he corrects most:** `bid_note` (mainly Drop→DropTarget, 12 of 12 DropTarget cells are red), `bid_date_rough`, cohort names/type splits, and three Formal→Informal downgrades.

## 5. Every comment in AG:AI, verbatim

Tags: **[CONV]** settled convention · **[Q]** open question/doubt · **[COND]** condition detail · **[LEGAL]** counsel/adviser · **[OTH]** other. **⚠** = Alex himself unsure.

### Providence & Worcester
- AG6024 **[CONV]** (pink) "Bidder interest suggested, but no bid"
- AG6025 **[LEGAL]** "Legal advisor: Hinckley Allen"
- AG6026 **[Q]⚠** (pink) "No concrete offer from Party A and a large time gap, so perhaps this is Target Sale?"
- AG6031 **[OTH]** "In view of the substantial amount of management time that would be required for management presentations, the Transaction Committee concluded that the two low bidders should be excluded from that process. The Transaction Committee authorized representatives of GHF to schedule in-person management presentations with the remaining seven potential buyers and allow these parties to conduct additional due diligence. These potential buyers were given access to an internet data site to conduct legal and financial due diligence."
- AG6032 **[CONV]** "Mid-june 2016"
- AH6032 **[Q]⚠** "This is probably something we will not collect, but for now…"
- AG6033 **[Q]⚠** "Early july 2016 - what should be the appropriate date? July 1?"
- AG6035 **[CONV]** "Late july -- but the deadline was july 20"
- AH6035 **[Q]⚠[COND]** "expedited DD; what is the threshold for \"formal\"?"
- AH6036 **[COND]** "60 day exclusive DD + negotiation of documentation"
- AH6037 **[COND]** "4 week DD"
- AH6038 **[COND]** "30 day DD"
- AH6039 **[COND]** "30 day DD"
- AG6041 **[OTH]** "20.02 cash + 1.13 CVR"
- AH6041 **[COND]** "3 week exclusive DD"
- AG6044 **[OTH]** "21.02 cash + 1.13 CVR"
- AG6045 **[OTH]** " Target worried about the delays inherent in managing on-site due diligence by multiple parties and the difficulties of maintaining the confidentiality of the discussions. The Transaction Committee concluded that the Company should proceed with confirmatory due diligence and negotiations with G&W and Party B because of the higher offers made by each of G&W and Party B relative to the other potential buyers."
- AG6050 **[CONV]** "Reengaged"
- AH6050 **[COND]** "30 day exclusive DD"
- AG6051 **[CONV]** "Reengaged"
- AH6051 **[COND]** "30 day DD; Financing support from Party F"
- AG6054 **[CONV]** "Confirm 7/20/2016 bid after DD"
- AH6054 **[COND]** "Restrict from soliciting competing bids"
- AG6055 **[OTH]** "all cash"
- AH6055 **[COND]** "Expire 8/13/2016, restrict from soliciting competing bids, regulatory approval needed"
- AG6056 **[OTH]** "Refused to increase offer"
- AG6057 **[OTH]** "Did not engage for a while"
- AG6058 **[Q]⚠** "The deadline apparently was not announced to the bidders, this was the time when the English auction was stopped by the target"
- AG6059 **[CONV]** "Latest bid executed"

### Medivation
- AG6063 **[LEGAL]** "Legal advisor: Cooley. May 2: Pfizer's contact that was viewed well by the target. No mention of the IB engagement earlier"
- AH6067 **[COND]** "DD 1 week"
- AG6069 **[Q]⚠** "(Pfizer + several other parties); [SEVERAL: at least 3?]"

### Imprivata
- AH6076 **[COND]** "Confirmatory DD <=30 days"
- AH6077 **[COND]** "Confirmatory DD <=30 days"
- AH6078 **[COND]** "Confirmatory DD <=30 days"
- AG6079 **[LEGAL]** "Legal counsel: Goodwin"
- AG6080 **[Q]⚠** "Telecom company. bid_date is 5/6-6/9. How to record this?"
- AH6080 **[OTH]** "These parties were selected based on their experience and interest in the security and/or healthcare technology and information services industries and likely capability to execute and finance such a transaction on an expeditious basis."
- AG6081 **[OTH]** "Software company"
- AH6081 **[OTH]** "In particular, the Board discussed the potential disruptions to the Company's business during a protracted process, the risk of leaks that might arise from contacting other parties, and the potential impact of such leaks on the Company's business, including the potential loss of customers and employees."
- AG6082 **[OTH]** "Software company"
- AH6082 **[OTH]** "The Board also discussed the potential need to disclose during such process proprietary and confidential information to competitors and potential competitors."
- AG6087 **[Q]⚠** "Dropped shortly after NDA, how to record given that we do not know NDA date here?"
- AG6089 **[CONV]** "Deadline for indications of interest 6/9"
- AH6089 **[OTH]** "Not a strategic fit for bidder"
- AG6090 **[CONV]** "F bidder, so all cash"
- AH6090 **[COND]** "DD, no financing \"among other conditions\""
- AG6091 **[CONV]** "F bidder, so all cash"
- AH6091 **[COND]** "DD, no financing \"among other conditions\""
- AH6092 **[COND]** "DD, no financing \"among other conditions\""
- AH6094 **[OTH]** "Other internal corporate priorities"
- AG6095 **[OTH]** "[VARIANCE OF PROPOSALS MATTERS -- ON TOP OF THE AVERAGE AND THE MAX? see the adjacent text. STRATEGIC PRESENCE MATTERS -- DD may give the target a chance that S revalues it at a higher value?]"
- AH6095 **[OTH]** "Because Sponsor A, Sponsor B and Thoma Bravo had submitted proposals within close range of each other, the Board authorized Barclays to advance all three parties to the second phase of the strategic process. In an effort to attempt to have strategic parties involved in the process, the Board also directed Barclays to contact Strategic 3 and encourage it to continue to participate in the process and to submit a proposal."
- AI6095 **[OTH]** "Continued: The Board also discussed that although there were no known actual conflicts at the time, because of the potential for management conflicts of interest to arise in the context of a potential sale to a financial sponsor, the Board would form a special committee"
- AH6096 **[OTH]** "Other internal corporate priorities, overlap in tech"
- AH6097 **[CONV]** "After DD: confirmed in communications their informal bid basically"

### Zep
- AG6385 **[LEGAL]** "Legal advisor: King & Spalding"
- AG6386 **[LEGAL]** "Legal advisor: King & Spalding" *(duplicate of AG6385)*
- AG6390 **[Q]⚠** "This field needs to be expanded to 5 bidders; one of them bid 20, another 22, another three [20,22]?"
- AG6399 **[Q]⚠** "[OVER THE NEXT FEW WEEKS: WHAT SHOULD BE THE DATE?]"
- AH6399 **[OTH]** "Over the next few weeks, five of the remaining six interested parties communicated to representatives of BofA Merrill Lynch that they were unable to proceed with the process due to concerns regarding valuation and, in some cases, the interested parties' own internal initiatives and strategic priorities. The sixth remaining interested party declined to respond to BofA Merrill Lynch's communications regarding a potential transaction."
- AG6401 **[CONV]** "[THIS IS THE EXAMPLE OF THE EARLIER AUCTION THAT WAS TERMINATED! CAN USE]"
- AH6402 **[COND]** "No financing condition (highly conf letter), 45 days exclusivity, go-shop"
- AH6404 **[OTH]** "[USEFUL FOR TARGET MOTIVATION] Our board of directors also considered again the importance of limiting any distractions that might be associated with pursuing another potential sale of the Company. "
- AH6406 **[COND]** "Go-shop 30 days, term fee, reverse term fee"

### PetSmart
- AG6408 **[LEGAL]** "Legal advisor: Wachtell Lipton"
- AG6412 **[OTH]** "PetSmart tried to acquire a firm from the same industry in March 2014, but it was \"not for sale\" and would require antitrust clearance that seemed difficult to obtain"
- AG6413 **[OTH]** "May 21, 2014: quarter earnings announcement, weaker than expected performance and guidance for remainder of year, lead to communications to sell company"
- AG6414 **[CONV]** "NDA first week of October"

### Penford
- AG6461 **[CONV]** "[EVERYTHING IN GREY SHOULD NOT BE HERE]"
- AG6466 **[OTH]** "This NDA is a 'Secrecy Agreement', i.e. lacks certain features of a standard NDA and standstill agreement"
- AG6467 **[LEGAL]** "Legal counsel: Perkins Coie"
- AH6467 **[Q]⚠** "It looks like DB was already seleected on July 30, and provided some advice on Aug 11, even though an engagement letter was signed on Sep 11. Which date should be used?"
- AG6477 **[OTH]** "After further discussion, with input from Deutsche Bank, the directors present at the board meeting unanimously directed management to proceed to negotiate and finalize a definitive agreement with Ingredion."
- AG6479 **[Q]⚠** "10/11/2014: draft financial statements for the fiscal year ended August 31, 2014 (referred to as the 2014 draft financial statements), which reflected lower volume, lower revenue and lower EBITDA than was projected in the materials previously provided to Ingredion from Penford's strategic plan. Does this represent legal risk? How do reps and warranties look like in the merger agreement?"

### Mac-Gray
- AG6928 **[CONV]** "Not an official sale, but T approached Party A"
- AG6930 **[CONV]** "Sale process discussed since May 9; BofA offered some valuations on May 30 before being reemgaged as IB"
- AG6939 **[OTH]** "the Special Committee concluded that it would be advisable to stage the disclosure of such information to each of the bidders to the extent that a bidder's indication of interest and other actions demonstrated its seriousness in acquiring Mac-Gray on terms viewed favorably by the Special Committee. "
- AG6945 **[OTH]** "[DIFFERENT DD INFO FOR DIFFERENT BIDDERS, S VS F + DEGREE OF INTEREST] Party B and Party C, in light of the fact that they were financial bidders, were given broad access to an electronic data site, and Party A and CSC/Pamplona, in light of the fact that they were strategic bidders, were given somewhat limited access to this electronic data site, with access to customer data, including customer locations, being reserved until later in the process as part of the staging discussed at the July 25th Special Committee meeting."
- AH6946 **[COND]** "Exclusivity 2 weeks"
- AH6947 **[COND]** "No firm financing commitment"
- AH6949 **[COND]** "No firm financing commitment"
- AH6950 **[COND]** "No firm financing commitment"
- AH6952 **[COND]** "Exclusivity 2 weeks"
- AG6954 **[OTH]** "19 in cash, rest in options/earnouts (2.5 is the bidder's valuation of these)"
- AH6954 **[COND]** "No firm financing commitment"
- AH6957 **[COND]** "Exclusivity 2 weeks"
- AH6960 **[COND]** "Exclusivity 2 weeks"

### Saks
- AG6996 **[OTH]** "For the past several years, Goldman Sachs, one of Saks' longstanding financial advisors, has participated in these reviews. One such review took place in December 2012."
- AG6997 **[CONV]** "In February 2013"
- AG6998 **[LEGAL]** "Legal counsel: Wachtell Lipton"
- AG7004 **[OTH]** "In late May 2013, media reports began to appear stating that Saks had engaged Goldman Sachs to explore a potential sale of Saks."
- AG7007 **[CONV]⚠** "[This clearly happened after Final Round Ann -- so the day is approximate] In early July 2013, Sponsor E informed Saks that Sponsor A was no longer intending to be a primary participant in a potential transaction and that Sponsor E had entered into discussions with Sponsor G, a private equity firm, regarding a potential joint acquisition of Saks."
- AG7009 **[CONV][COND]** "formal, with committed debt and equity financing"
- AG7010 **[COND]** "Several weeks of DD required, no availability of financing"
- AG7013 **[CONV]** (pink) "Should be deleted: unsolicited letter, no NDA, no further contact, no price per share"
- AG7015 **[CONV]** (pink) "Not a separate bid, should be deleted"
- AG7019 **[COND]** "Go-shop until Sep 6"

### sTec
- AG7144 **[OTH]** "Approximately two weeks later, the President of Company B contacted Mr. Manouch Moshayedi to inform Mr. Moshayedi that he had shared sTec's information with Company B's executive management, but that Company B's management had determined that it was not interested in acquiring sTec and believed that it could independently develop the technology it needed to compete in enterprise SSDs."
- AG7145 **[OTH]** "In mid-March, 2013, the head of corporate development for Company D, a participant in the storage industry, contacted our management to express the interest of Company D in exploring a potential acquisition of the company. At the direction of the special committee, members of our management met with representatives of Company D to discuss their potential interest."
- AG7146 **[OTH]** "On March 26, a board meeting discussed \"the lack of interest from financial buyers in light of the company's recent financial performance and the potential difficulties this created for financial buyers to use debt to finance a purchase of the company, and the fact that strategic buyers would likely attribute the greatest value to the company and its business... it was in the best interests of the company and its shareholders to confidentially approach strategic buyers that the board believed would be most likely to have interest in a potential acquisition of the company to explore their interest, but to also further conduct a limited confirmatory exploration of interest of financial buyers.\""
- AG7147 **[LEGAL]** "Legal counsel: Gibson Dunn"
- AG7154 **[OTH]** "indicated it was also only interested in purchasing limited, select assets of sTec, and as a result the special committee decided not to continue discussions"
- AG7155 **[OTH]** "indicated it was also only interested in purchasing limited, select assets of sTec, and as a result the special committee decided not to continue discussions"
- AG7157 **[OTH]** "Indicated it would not continue the process"
- AG7163 **[OTH]** "Indicated it is not able to increase its indicated value range"
- AG7164 **[OTH]** "various interesting covenants, e.g. not to sue by target CEO, included"
- AG7166 **[CONV]** "For Company D"
- AG7167 **[OTH]** "Later extended until 6/10/2023 as WDC was thinking about dropping"
- AG7168 **[OTH]** "Company D would not be in a position to actively conduct due diligence for more than two weeks and was disengaging from the process."
- AG7169 **[OTH]** "WDC had given serious consideration to not proceeding with a transaction, that WDC did not view the acquisition of sTec as essential to its SSD strategy in light of other available alternatives (including internal development efforts), and that according to WDC certain business factors related to the company had also influenced WDC's decision to lower the price from its May 30, 2013 written indication of interest at $9.15 per share in cash, as well as a change in its bidding strategy from the prior approach it had adopted."
- AH7169 **[OTH]** "The board of directors' disappointment in the latest proposal and the significant change from its prior proposal, that the board would not respond to a proposal with a range, and that if WDC desired to proceed, WDC must submit a proposal reflecting its best offer"
- AG7170 **[OTH]** "From June 16 to June 22, 2013, WDC conducted additional due diligence, including confirmatory due diligence calls."
- AG7171 **[OTH]** "From June 16 to June 22, 2013, WDC conducted additional due diligence, including confirmatory due diligence calls." *(duplicate of AG7170)*

**Role split:** AH is predominantly condition text (30 of 40 match DD/financing/exclusivity/go-shop/term-fee/standstill wording); AG is reasons, legal counsel, date approximations and filing quotes (23 of 73).

## 6. Stress test of the proposed flat ledger

| Feature in the data | Fails because | Minimal fix |
|---|---|---|
| Cohort rows with counts **and** type splits: `25 parties, including Parties A, B` + `11S, 14F` (N/S6027), `5 parties, 4F and 1S` (6390), `16 financial bidders` (6934) | one `who` + one `bidder type` cell | `party_count` int + allow `bidder_type` = mixed with a `type_split` free-text; keep the "including …" names in `who` |
| Joint bidders / consortia: `Party E/F`, `CSC/Pamplona`, `Sponsor A/E`, and the A/E→E/G recomposition at AG7007 | one bidder per row | keep slash notation in `who` **plus** a `bidder_group_members` column; a consortium's composition changes mid-process |
| Ranges and "at least $X" | price + lower + upper handles ranges, but note **Alex's price = lower bound**, and 6428/6998/6999/7153 have *only* a lower bound, 6429/6430 have **no** price at all on a real bid | define `price` = point price, blank for ranges; allow lower-only; allow a bid row with no price at all |
| Mixed consideration: 6041/6044 "20.02 cash + 1.13 CVR" (all_cash=1), 6954 "19 cash, rest in options/earnouts" (all_cash=0) | one price, one cash flag | `consideration_note` free text + `cash_share`; the 9-row precedent is internally inconsistent already |
| Enterprise-value bids (7013: 2.6 billion, multiplier 1e9, no per-share) | no unit/multiplier in the proposal | `value_basis` (per-share / total) + `value_unit`; low priority — the only case is a row Alex deletes |
| Multiple processes: Zep `Terminated` 6401 / `Restarted` 6402; Penford's 2007/2009 NDAs greyed out | one chronology per deal | `process_id` int (1,2,…) or a `process_phase` column, plus an explicit rule on when an earlier attempt is in scope |
| Press-release / activist rows (6062, 6409, 6411) | not bidder events | already covered by the label vocabulary — just keep `who` blank-able |
| Deadline / extension rows (6032, 6040, 6099, 6102, 6943, 6948, 7166, 7167) | `who` is empty and price is empty on 8 label types | allow marker rows; `Final Round × {Inf} × {Ext} × {Ann}` is a 3-flag cross-product — encode as `round_type` + `is_announcement` + `is_extension` rather than 12 flat strings |
| Legal counsel (9 instances, all in AG) | no column | `target_legal_counsel` on the Summary sheet, one per deal (all 9 occurrences are deal-level) |
| **Two rows per real-world act**: `Bidder Sale` 6060 + first bid 6061 same day; 6077+6078; 6931+6932; `Final Round Inf` 6040 dated same day as bids 6035–6039 | one event label per row forces duplicates | either accept duplicate rows (Alex's choice) or add a boolean `initiates_process` on the bid row |
| Date *ranges*: "bid_date is 5/6-6/9" (AG6080), "over the next few weeks" (AG6399) | one date + approx flag | `date_end` optional column; document the start-of-period default |
| Ordering ≠ date (6087, 6436, 6935; cohort rows dated at the end of a window) | sortable single date column | keep an explicit `seq` column (Alex's fractional BidderID) as the sort key |
| Conditionality | Alex records conditions as **free text** (30 AH cells): DD length, exclusivity, financing, go-shop, term fee, standstill | keep `conditions_text` alongside `conditionality none/light/heavy`; the coarse code alone loses everything he collected |

## 7. Internally inconsistent / likely mistakes — do not copy

- **Duplicate & out-of-order BidderIDs:** M6066 = 5 but 5 already exists at M6070 (should be ~3.5); M6960 = 21 but 21 exists at M6957 (should be ~23.5).
- **Two deletion conventions:** pink "Bad" style (Saks 7013–7015) vs grey fill (Penford 6461–6464, flagged by AG6461); and integer IDs simply vanish — PetSmart missing 30, 33, 34, 35, 41; Penford 16; sTec 8.
- **Type dummies vs note:** O–R filled at 6024 but left NA at 6997, 7144, 7145 and on *every* Executed row, where only S is filled. S6996 = `F` for Goldman Sachs — that's "financial *advisor*", not a bidder type; the instructions say leave IB type blank.
- **N6386** (`Target Sale`) carries `BofA Merrill Lynch`; instructions say Bidder blank for Target Sale. Its comment duplicates AG6385.
- **AC6028** (G&W, 04/13/16): no bid_note, no bid_type, no price — an unlabelled event row (almost certainly NDA) left uncorrected.
- **AB7012 and AA7012 both empty** (Sponsor G Drop) — a dated event with no date.
- **`all_cash` unreliable:** AG6090/AG6091 assert "F bidder, so all cash" yet AD6090/AD6091 = NA; AD6073 = `'NA '` with a trailing space; 29 of 81 bid rows blank; 6041/6044 (cash + CVR) coded 1 while 6954 (cash + earnouts) coded 0.
- **Typos:** N7017 `Spnosor A/E`; N6463/N6464 `A diffferent party`; AG7167 "6/10/2023" (should be 2013); AG6930 "reemgaged"; E5-6 mojibake in the PetSmart Acquirer string (`dÃ©pÃ´t`).
- **E6934–E6960** put a free-text note (`CSC purchased by Pamplona in May/2013`) into the Acquirer field for 24 of 34 MacGray rows — a deal-level fact smuggled into a constant column.
- **AA (bid_date_precise) is stale on every red row** — copy-pasted, contradicts AB 37 times. Any pipeline reading AA will be wrong.
- **Instruction/sheet divergence:** Formal/Informal lives in `bid_type`, not `bid_note`; `DropBelowM` and bare `Press Release` never used; §2 ("ignore stale processes") and §3.9 ("record Terminated/Restarted") conflict, and Alex resolves it differently in Zep (recorded) vs Penford (greyed out) with no stated rule.

## Could not determine

- Whether AA was ever meaningfully maintained, or what Alex intended by the copied values (inference only, from the ±4-row duplication pattern).
- What the deleted integer BidderIDs (PetSmart 30/33/34/35/41, Penford 16, sTec 8) contained — the RA baseline `deal_details.xlsx` is **not** in `/home/uctpiaj/Projects/sec2/ref/` (only the PDF, this workbook, `alex_voice_notes_2026-08.docx`, and a companion .md), so I could not diff.
- Why AB6403 was moved 02/10→02/19 (matching the `Restarted` row 6402) while AA kept 02/10.
- Whether `Executed` at 6054 means "Party B delivered an executed agreement" (Party B is not the winner) or is an artifact of the row being a copy of 6035 — the label appears once on a loser and nine times on winners.
- The meaning of column A (constant per deal, e.g. 6879 for Saks; not a row number, not gvkey).
- Whether the grey fill in Penford is Alex's or inherited — AG6461's text is **not** red (theme 1 = black), unlike all his other additions.

---

# B. Stress test of the flat ledger on Mac-Gray and PetSmart

# Flat-ledger stress test: Mac-Gray & PetSmart

## 1. The professor's ledgers

Reading key: `ord` = col M (event order, fractional inserts for structural rows — **not** a bidder ID). Price shown as `lo–hi` (T/U/V/W; for a range he puts the **lower** bound in T and U, so a separate "price" column is redundant). Dates = `AA → AB`; AA (precise) is blank when no exact day is disclosed, AB is always the working date.

### MAC GRAY CORP — rows 6927–6960, **34 rows**

```
row   ord   who                  typ  price      F/I       AA→AB                  bid_note                  cash  comment
6927  0.5   BofA Merrill Lynch   -    -          -         →2013-04-05            IB                        -
6928  0.7   Party A              S    -          -         →2013-04-08            Target Interest           -     "Not an official sale, but T approached Party A"
6929  0.8   BofA Merrill Lynch   -    -          -         →2013-05-15            IB Terminated             -
6930  0.9   BofA Merrill Lynch   -    -          -         →2013-05-31            IB                        -     discussed since May 9; valuations May 30 pre-reengagement
6931  0.95  Party A              S    -          -         06-21→06-21            Bidder Sale               -
6932  1     Party A              S    17–19      Informal  06-21→06-21            -                         1
6933  1.5   (none)               -    -          -         →2013-06-24            Final Round Inf Ann       -
6934  2     16 financial bidders F    -          -         →2013-07-15            NDA                       -
6935  3     Party B              F    -          -         06-28→06-28            NDA                       -
6936  4     Party C              F    -          -         06-20→06-30            NDA                       -
6937  5     CSC/Pamplona         S    -          -         07-11→07-11            NDA                       -
6938  6     CSC/Pamplona         S    18.5       Informal  07-23→07-23            -                         1
6939  6.5   (none)               -    -          -         →2013-07-23            Final Round Inf           -     staged disclosure quote
6940  7     Party B              F    17–18      Informal  07-24→07-24            -                         1
6941  8     Party C              F    15–17      Informal  07-24→07-24            -                         1
6942  9     16 financial bidders F    -          -         07-25→07-25            Drop                      -
6943  9.5   (none)               -    -          -         →2013-07-25            Final Round Inf Ext Ann   -
6944  10    Party C              F    16–16.5    Informal  07-25→07-25            -                         1
6945  11    Party A              S    -          -         08-05→08-05            NDA                       -     S vs F data-room access differed
6946  12    CSC/Pamplona         S    19.5       Informal  09-09→09-09            -                         1     Exclusivity 2 weeks
6947  13    Party B              F    18.5       Informal  09-09→09-09            -                         1     No firm financing commitment
6948  13.5  (none)               -    -          -         →2013-09-09            Final Round Inf Ext       -
6949  14    Party A              S    18–19      Informal  09-10→09-10            -                         1     No firm financing commitment
6950  15    Party C              F    16–17      Informal  09-10→09-10            -                         1     No firm financing commitment
6951  16    (none)               -    -          -         09-11→09-11            Final Round Ann           -
6952  17    CSC/Pamplona         S    20.75      Formal    09-18→09-18            -                         1     Exclusivity 2 weeks
6953  18    Party A              S    18–19      Formal    09-18→09-18            -                         1
6954  19    Party B              F    21.5       Formal    09-18→09-18            -                         0     $19 cash + options (bidder values at 2.5); no firm financing
6955  20    Party C              F    -          -         09-18→09-18            Drop                      -
6956  20.5  (none)               -    -          -         09-11→09-18            Final Round               -
6957  21    CSC/Pamplona         S    21.25      Formal    09-21→09-21            -                         1     Exclusivity 2 weeks
6958  22    Party A              S    -          -         09-24→09-24            DropTarget                -
6959  23    Party B              F    -          -         09-24→09-24            DropTarget                -
6960  21*   CSC/Pamplona         S    -          -         09-21→10-14            Executed                  -     Exclusivity 2 weeks   (*ord 21 duplicated)
```

### PETSMART INC — rows 6408–6460, **53 rows**

```
row   ord   who               typ price     F/I       AA→AB               bid_note              cash comment
6408  0.7   J.P. Morgan       -   -         -         →2014-07-01         IB                    -    Legal advisor: Wachtell Lipton
6409  0.8   (none)            -   -         -         →2014-07-03         Activist Sale         -
6410  0.9   (none)            -   -         -         →2014-08-13         Target Sale Public    -
6411  0.95  (none)            -   -         -         →2014-08-19         Sale Press Release    -
6412  1     Unnamed party 1   F   -         -         →2014-10-07         NDA                   -    Industry Participant note (Mar 2014)
6413  2     Unnamed party 2   F   -         -         →2014-10-07         NDA                   -    May 21 earnings miss note
6414  3     Unnamed party 3   F   -         -         →2014-10-07         NDA                   -    "NDA first week of October"
6415-6423  4–12  Unnamed parties 4–12   F   -   -     →2014-10-07         NDA                   -
6424  13    Bidder 1          F   -         -         →2014-10-07         NDA                   -
6425  14    Bidder 2          F   -         -         →2014-10-07         NDA                   -
6426  15    Buyer Group       F   -         -         →2014-10-07         NDA                   -
6427  15.5  (none)            -   -         -         →2014-10-15         Final Round Inf Ann   -
6428  16    Unnamed party 1   F   80–(NA)   Informal  10-30→10-30         -                     -
6429  17    Unnamed party 2   F   (none)    Informal  10-30→10-30         -                     -
6430  18    Unnamed party 3   F   (none)    Informal  10-30→10-30         -                     -
6431  19    Buyer Group       F   81–83     Informal  10-30→10-30         -                     -
6432  20    Unnamed party 4   F   80–85     Informal  10-30→10-30         -                     -
6433  21    Bidder 2          F   78        Informal  10-30→10-30         -                     -
6434  21.5  (none)            -   -         -         →2014-10-30         Final Round Inf       -
6435  22    Bidder 2          F   81–84     Informal  10-30→11-02         -                     -
6436  22.5  Unnamed party 5   F   -         -         10-30→10-30         Drop                  -
6437-6443 23–29 Unnamed parties 6–12  F  -  -         10-30→10-30         Drop                  -
6444  31    Unnamed party 2   F   -         -         →2014-11-03         DropTarget            -
6445  32    Unnamed party 3   F   -         -         →2014-11-03         DropTarget            -
6446  34.5  (none)            -   -         -         →2014-11-15         Final Round Ann       -
6447  36    Buyer Group       F   80.70     Formal    12-10→12-10         -                     1
6448  37    Bidder 2          F   80.35     Formal    12-10→12-10         -                     1
6449  38    Bidder 3          F   78        Informal  12-10→12-10         -                     -
6450  38.2  Unnamed party 1   F   -         -         11-03→12-10         Drop                  -
6451  38.3  Unnamed party 4   F   -         -         →2014-12-10         Drop                  -
6452  38.5  (none)            -   -         -         →2014-12-10         Final Round           -
6453  38.7  (none)            -   -         -         →2014-12-10         Final Round Ext Ann   -
6454  39    Bidder 2          F   81.50     Formal    12-12→12-12         -                     1
6455  40    Buyer Group       F   82.50     Formal    12-12→12-12         -                     1
6456  40.3  Buyer Group       F   83.00     Formal    12-12→12-12         -                     1
6457  40.5  (none)            -   -         -         →2014-12-12         Final Round Ext       -
6458  42    Bidder 2          F   -         -         12-14→12-14         Drop                  -
6459  43    Bidder 3          F   -         -         12-14→12-14         Drop                  -
6460  43.5  Buyer Group       F   -         -         12-12→12-14         Executed              1
```

**Structural quirks worth copying or avoiding.** (a) Ranges: lower bound duplicated into `bid_value`/`per_share` — so *Price / Low / High* in your proposal collapses to **Low / High**. (b) `AA`/`AB` are not "exact vs approximate": when both are filled and differ they are a **window** (6435 Oct 30→Nov 2; 6450 Nov 3→Dec 10) or a **set→due** pair on structural rows (6956 Sep 11→Sep 18; 6460 Dec 12→Dec 14, bid→signing). A single Date + flag cannot carry this; you need technical `date_lo`/`date_hi`. (c) His rough-date convention is inconsistent ("in July"→Jul 1; "first week of Oct"→Oct 7; "over the next two months"→Jul 15; "during October"→Oct 15) — state a rule rather than imitate. (d) 6936 Party C precise 2013-06-20 vs BG-027's June 30 is a data error. (e) Order numbers 30, 33, 34, 35, 41 are missing in PetSmart and 21 is duplicated in Mac-Gray — the gap at 30 is exactly where **Bidder 1's missing exit row** belongs (15 NDAs − 6 IOIs = 9 non-submitters, but only 8 Drop rows). That single arithmetic hole is the strongest argument for a per-row **N** column: `SUM(N)` by What/Round makes such gaps detectable without a Counts sheet.

## 2. Cases the flat columns handle badly

### Mac-Gray

| Para | Situation | His cells | Minimal fix |
|---|---|---|---|
| BG-004/005 | Target's bank *approaches* Party A, no bid | 6928 `Target Interest` | Your label list has only *Bidder Interest* / *Target Sale*. Need the full 2×2: **Target Interest, Bidder Interest, Target Sale, Bidder Sale** — Mac-Gray uses exactly the two you omitted |
| BG-019 | Party A bids unsolicited before any process exists | 6931+6932, ord 0.95/1 | `Round #` must allow **0 = pre-process**; keep the real date, do not fold into round 1 |
| BG-023 | 50 parties to be contacted, 15 S / 35 F | *no row* (voice note II.2 wants it) | New label **Contact**, cohort row, `N=50`, `Direction=outbound`, type split via two rows (15 S, 35 F) or a `Type note` |
| BG-024 | 20 NDAs over two months, 2 S / 18 F incl. B & C | 6934 "16 financial bidders" cohort + 4 named rows | Cohort rows allowed, but the **residual** must be disjoint from named rows — 16, not 18; 0 unnamed strategics. `N` + `Named?` flag makes this checkable |
| BG-024/032/033 | Jul 23 deadline; bids arrive Jul 23, 24, 24, 25 with no disclosed extension | 6939/6943 conflate it | **Soft-deadline** case exists in Mac-Gray, not just STEC. Need `Deadline enforcement` = observed_cutoff / extended / late_accepted / unclear |
| BG-035 vs BG-044 | Round 2 opens Jul 25 with **no deadline**; deadline set Aug 27 for Sep 9 | 6943 "…Ext Ann" at Jul 25; **nothing at Aug 27** | "Ann" fuses *round opened* with *deadline set*. Split into **Round opened / Deadline set / Deadline revised / Deadline reached**; `Round #` carries the count, so "Final Round Inf Ext" naming disappears |
| BG-048/049 | CSC 100% committed capital; B, A, C each *lack* firm commitment | free text in AE-comments (6947/6949/6950) | Professor wants **absence** recorded on the bid row. `Conditions` tag column (multi-valued) with `no_financing_commitment`; a none/light/heavy scalar alone loses which condition |
| BG-048/054/057 | CSC conditions each bid on 2-week exclusivity | comment "Exclusivity 2 weeks" ×3 | Exclusivity is a **tag, not a formality downgrade** (voice note II.7). Keep in `Conditions`, never in Formal/Informal |
| BG-054 | Party B: $21.50 = $19 cash + options *bidder-valued* at $2.50 | 6954, `all_cash=0`, comment | `All cash` = No + `Cash at close` technical column + `Conditions=contingent_consideration`. Do not let $21.50 enter a cash series |
| BG-054 | Party A "reiterates $18–19 as best and final" | 6953 Formal, range kept | Range on a **formal** bid is legitimate (voice note II.6). Don't force a point price |
| BG-056/057 | Target proposes $21.25; CSC accepts same day | 6957 only | One bid row; the target's ask belongs in `Reason`, not a bid row (`target_price_request` folds to note) |
| BG-061/073 | Exclusivity executed Sep 24, extended Oct 12 | *no row*; only 6958/6959 DropTarget Sep 24 | Add an **Exclusivity** label (legacy precedent exists: "Exclusivity 30 days"). It is what *explains* the two DropTarget rows |
| BG-006/062 | Goodwin Procter first appears May 9 (target); Kirkland is CSC's counsel | *no rows* (voice note II.9 wants May 9) | Adviser rows keyed to **first mention**, with role+client in the Bidder-type cell: `Adviser to T (legal)`, `Adviser to B (legal)` |
| BG-079 | Oct 15 public announcement, day after signing | *no row* (6960 Executed only) | Separate **Announced** row — mandated repeatedly (2.I) |
| — | CSC (operating co) + Pamplona (sponsor) | typed `S` | State the rule: sponsor-backed operating company is **Strategic**, not Mixed |

### PetSmart

| Para | Situation | His cells | Minimal fix |
|---|---|---|---|
| BG-005/007 | Industry Participant approaches, then is deliberately **not invited** | *no rows at all* | Bidder Interest row + `Outcome=pre_entry_exclusion` in Reason. Penford note 3: record the contact, **no Drop row** where no stage was entered |
| BG-008 | 27 **inbound** contacts, 3 S / 24 F, "including equity providers" | *no row* | Contact cohort row with `N=27`, `Direction=inbound`; counting-unit caveat (equity providers ≠ lead buyers) in Reason |
| BG-009/010/011 | Round 1 opens Oct 3 (board meeting); NDAs first week Oct; Oct 30 deadline communicated "during October" | 6427 dated **Oct 15** | Voice note III.1 puts round 1 at Oct 3. **Round opened ≠ Deadline set** again |
| BG-012 | "Three bidders indicated ranges that **reached at least $80**" | 6428 `lower=80, upper=NA` | §8.4 says the *upper* endpoint is ≥80. Direct conflict — see §6 |
| BG-012 | Two IOI bidders whose prices are never disclosed | 6429/6430 Informal, price blank | Price cells **may be empty on a bid row**; don't drop the row and don't invent a price |
| BG-012 | Bidder 2 bids $78, then $81–84 "from Oct 30 to Nov 2" | 6433 then 6435, window Oct 30→Nov 2 | Same-day/near-day revisions must sort in narrative order (III.4). `#` column + `date_lo/date_hi` |
| BG-013 | Nov 3: target eliminates, **and** none would go above their initial indications | 6444/6445 `DropTarget` | Compound: agency = target **and** valuation ref = at-IOI. The legacy labels can't co-occur. Use `What=Drop` + technical `Exit agency` + `Exit valuation ref`; derive the legacy label |
| BG-014 | Two invited bidders merge into "Bidder 3" | 6450/6451 **Drop** for constituents; Bidder 3 appears as a new Who with no NDA row | This inflates dropouts and breaks §14. Fix: **Consortium** row for the new unit; constituents get **Joined group**, not Drop; technical `Unit members` |
| BG-016 | Dec 15 target completion; bids Dec 5 → moved to Dec 10 | *missing*; only Dec 10→12 at 6453 | **Deadline revised** row carrying prior and new date; two revisions here, not one |
| BG-017 | Dec 6 markups; Buyer Group provides financing commitments, Bidder 2 does not | *no rows* | Document-only arrivals are **not** new bids, but financing status changes between versions and must ride the **next** bid row |
| BG-020 | Bidder 3: valuation "would not be above ~$78"; no written offer | 6449 coded as an **Informal $78 bid** | Needs a **Valuation statement** label (no price fields) + Drop `reason=not_submitted`. Conflict with §8.1 — see §6 |
| BG-011/019/022 | Longview rollover; confidentiality agreement with the Buyer Group | *no rows* (correct) | Explicitly **not** an NDA, not a bidder, not a consortium (III.7). A note on the bid row only |
| BG-023 | Dec 12: Buyer Group oral $82.50, then $83 hours later | 6455/6456 ord 40 / 40.3 | Two rows, order preserved — your `#` handles this, keep it |
| BG-025 | Executed **and** announced on Dec 14 | 6460 `Executed` only | Two rows, same date |

## 3. Patterns from the other five deals

| Deal | Pattern | Minimal fix |
|---|---|---|
| Meredith | Bids for segments / individual studios, not the whole company | Technical `Whole company` = yes/partial/unknown; deal-level flag when any bid is partial (2.L) |
| Meredith | $2.5bn for *levered assets*, 50% stake retained; equity vs EV | `Unit` (dollar/million/billion) + `Value basis` (per_share / equity / EV); leave per-share empty, flag (2.M) |
| Meredith | Party D Apr 29 **dual proposal** ($2.66bn/50.2% retained vs $2.76bn/34%) | Two rows sharing an `Alt group` id; never a range |
| Meredith | Gray bids $16.99 → $16.55 → **reverts** to $16.99 after signing | Reversion is a **new row at the old price**, `price_origin=reverted` |
| Meredith | Public bidding after the merger agreement is signed | `Round #` allowed value **"post"**; not a go-shop |
| Meredith | Deloitte as **tax** adviser | Adviser role vocabulary = legal / financial / tax |
| Synacor, STEC | Multiple sequential sale **processes** (9-month, 3-month gaps) | `Process #` column (1,2,…); always flag when >1 (VII.1) |
| Synacor | Go-shop mis-identified | Distinct label **Go-shop start/end**; must follow an Executed row |
| STEC | May 3 deadline passes, bids keep arriving, nothing happens | `Deadline enforcement` (as above); this is the soft-deadline flag |
| STEC | Winner cuts price late; premium may be unchanged | Technical `Market price ref` + its date on the bid row (also PetSmart's ~$78) |
| STEC | Activist suggests sale without demanding it | Separate **Activist involvement** from **Activist Sale** |
| Kraton | Party A bid with an **earnout** | `All cash = Yes` + `Conditions=contingent_consideration`; not "Mixed" |
| Kraton | Party H drops because valuation < its own IOI | `Exit valuation ref` = below_market / at_IOI / below_IOI / cannot_raise / unknown → maps to DropM/DropAtInf/DropBelowInf |
| Kraton, Penford | Winner's type absent from the background | Type resolved from elsewhere in the filing; always flag if still unknown (2.C/2.D) |
| Penford | Bidder cites target's stock price — not a bid | **Valuation statement** label again (also PetSmart Bidder 3) |

## 4. Recommended column list

**Visible (14).** Every one earns its place from a case above.

| # | Column | Allowed values / note |
|---|---|---|
| 1 | `#` | Integer, narrative order. Replaces his fractional M. Settles PetSmart Dec 12 $82.50→$83 and Bidder 2's Oct 30→Nov 2 revision |
| 2 | `Date` | One real date, always filled |
| 3 | `Date flag` | exact / approx / inferred |
| 4 | `Who` | Party name, cohort name ("16 financial bidders"), or adviser |
| 5 | `N` | **Added.** 1 for a named party; the count for a cohort row. Counts stay derived (`SUM(N)`) with no Counts sheet, and the missing Bidder 1 row surfaces as an arithmetic gap |
| 6 | `Type` | Strategic / Financial / Mixed / Unknown, + public\|private, + non-US; **or** `Adviser to T (legal\|financial\|tax)` / `Adviser to B (…)`. **Added use:** reuses a dead cell on adviser rows instead of a client column (Kirkland↔CSC) |
| 7 | `What happened` | Fixed list, §5 |
| 8 | `Process #` | 1, 2, … **Added** — Synacor, STEC |
| 9 | `Round #` | 0 (pre-process) / 1, 2, 3… / post / n/a. **Added values** — Party A's Jun 21 bid; Meredith post-signing |
| 10 | `Low` / 11 `High` | **Merged from your Price/Low/High**; his own T duplicates V. Point bid ⇒ Low=High. May be empty on a bid row (PetSmart 6429/6430) |
| 12 | `Formal/Informal` | Formal / Informal / n/a |
| 13 | `Conditions` | **Replaces your none/light/heavy.** Multi-valued tags: `none`, `no_financing_commitment`, `financing_committed`, `substantive_diligence`, `confirmatory_diligence`, `exclusivity_requested`, `regulatory_risk`, `contingent_consideration`, `terms_open`, `not_assessable`. A scalar cannot record *which* condition, and the professor wants the **absence** of financing recorded specifically |
| 14 | `All cash` | Yes / No / Unknown |
| 15 | `Reason + quote (p.)` | **Merged from your "AI's reason" + "Filing quote + page"** — one cell, reason then quote and page. Saves a visible column; reviewers read them together anyway |

**Dropped from your proposal:** *Price* (redundant with Low/High); *AI unsure flag* as a visible column — demote to technical `Q id` (blank = confident); *Human correction columns* — put them to the right of the technical block, one paired `_fix` per correctable field, so the AI original always stays visible.

**Right-hand technical columns:** `date_lo`, `date_hi` (his AA/AB window; also deadline set→due), `deadline_date`, `deadline_enforcement` (observed_cutoff \| extended \| late_accepted \| unclear \| n/a), `exit_agency` (bidder \| target \| joint \| unknown \| not_selected), `exit_valuation_ref` (below_market \| at_IOI \| below_IOI \| cannot_raise \| not_submitted \| unknown), `unit` (dollar \| million \| billion), `value_basis` (per_share \| equity \| EV), `whole_company` (yes \| partial \| unknown), `cash_at_close`, `market_price_ref` + `market_price_date`, `alt_group`, `unit_members`, `named` (Y/N), `direction` (inbound \| outbound), `legacy_bid_note` (derived), `Q id`, `para id`.

**Row granularity.** One row per bidder per event by default. A **cohort row is allowed only when every member shares an identical history** — same NDA date, same fate, never individually named. Mac-Gray's "16 financial bidders" qualifies (NDA Jul 15, Drop Jul 25); PetSmart's 15 do not, because 6 later bid and 9 did not, which is why he enumerated them. A cohort must be **disjoint from every named row in the same population** (16, not 18). Counts then reduce to `SUM(N)` filtered on What/Round, with `named` separating the residual — no Counts table, and counts remain derived, as he insists.

## 5. "What happened" vocabulary

| Display label | Legacy `bid_note` | §10 code |
|---|---|---|
| Target interest | `Target Interest` | `initial_sale_contact` |
| Bidder interest | `Bidder Interest` | `acquisition_interest_expressed` |
| Target sale | `Target Sale` | `sale_exploration_authorized` |
| Bidder sale | `Bidder Sale` | (none — unsolicited approach triggering the process) |
| Activist sale / Activist involvement | `Activist Sale` | `activist_sale_advocacy` / `activist_involvement` |
| Adviser engaged / ended | `IB`, `IB Terminated` | `financial_adviser_engagement`, `advisory_engagement_ended` |
| Contact | — **(no legacy label)** | `initial_sale_contact` |
| NDA | `NDA` | `confidentiality_agreement_executed` |
| Round opened | part of `Final Round … Ann` | `round_opened` |
| Deadline set / revised / reached | `Final Round Ann`, `… Ext Ann`; `Final Round`, `… Inf`, `… Ext` | `bid_deadline_set`, `bid_deadline_revised`, `bid_submission_deadline` |
| Bid | (blank, with `bid_type`) | `acquisition_proposal_submitted` |
| Valuation statement | — **(no legacy label)** | `bidder_valuation_statement` |
| Consortium formed / Joined group | — **(no legacy label)** | `bidding_group_changed` |
| Exclusivity granted / extended / ended | `Exclusivity 30 days` (1 use) | `exclusivity_granted/extended/ended` |
| Drop | `Drop`, `DropM`, `DropAtInf`, `DropBelowInf`, `DropTarget` | `bidder_withdrew`, `bidder_excluded`, `bid_not_submitted` |
| Sale announced (process) | `Target Sale Public`, `Sale Press Release` | `sale_process_publicly_announced` |
| Bid announced | `Bid Press Release` | `acquisition_proposal_publicly_announced` |
| Executed | `Executed` | `merger_agreement_executed` |
| Announced | — **(no legacy label)** | `merger_agreement_publicly_announced` |
| Go-shop start / end | — | `post_signing_solicitation_started/ended` |
| Terminated / Restarted | `Terminated`, `Restarted` | `sale_process_terminated/restarted` |

**Note the legacy spelling is `DropM` (109 uses), not `DropBelowM`.** The five Drop variants become **one label + two technical columns** (`exit_agency`, `exit_valuation_ref`); the legacy string is then derived, not typed. This is required because PetSmart BG-013 is simultaneously target-agency *and* at-IOI, which no single legacy label can express.

**Professor labels with no clean counterpart:** `Final Round Inf Ext` / `Inf Ext Ann` — ambiguous between "second informal round" and "deadline revision"; only `Round #` disambiguates, which is why they should disappear. `Target Sale Public` fuses the board decision with the announcement (he has a separate `Sale Press Release` six days later — genuinely two events). `Bid Press Release` (1 use) survives for post-signing public bidding.

**§10 codes to fold into `Reason` rather than give rows:** `strategic_alternatives_review`, `confidentiality_agreement_updated`, `due_diligence_access_changed` (BG-043 — he put it in a comment), `management_presentation` (four in Mac-Gray, none in his ledger), `bidder_admitted` (implied by `Round #`), `proposal_document_update` (PetSmart Dec 6), `target_price_request` (Mac-Gray Sep 19/21), `material_information_update`, `transaction_approved`, `other_material_process_event`.

**Expectation to set:** his ledger is a *floor*. The voice-note-mandated additions (contacts, round opens, deadline sets/revisions, Announced, advisers with clients, exclusivity) take Mac-Gray from 34 to roughly 45 rows and PetSmart from 53 to roughly 60.

## 6. Open questions only the professor can settle

1. **"Ranges that reached at least $80" (PetSmart BG-012).** He coded `lower=80, upper=NA` (6428); §8.4 says the *upper* endpoint is ≥$80 and the lower must stay empty. These are opposite. Which convention governs?
2. **"Not above ~$78" (PetSmart BG-020).** He coded an Informal $78 bid (6449) and later a Drop; §8.1/§13 forbid creating a bid from a valuation ceiling. Bid row or Valuation statement row?
3. **Consortium constituents.** He gives Unnamed 1 and Unnamed 4 `Drop` rows and introduces "Bidder 3" as a fresh party. That double-counts exits and breaks the §14 check. Confirm: `Joined group` instead of `Drop`, with the group as a new unit?
4. **Losers at signing.** He writes `Drop` on the execution date (6458/6459, 6955) even where the filing says nothing. Keep the convention with `exit_agency=not_selected`, or leave them without an exit row?
5. **Cohort vs enumeration.** Is the identical-history rule in §4 the rule he wants, and should residual cohorts always be stated as the *disjoint* remainder (Mac-Gray 16, not 18)?
6. **Round naming.** Mac-Gray: does round 2 informal open Jul 25 (BG-035) with the Sep 9 deadline set on Aug 27, making the Sep 18 formal round 3? His sheet's "Final Round Inf Ext" labels leave this unstated.

## What I did not check

The full DEFM14A HTML for either deal (including the "Parties involved" sections that resolve winner type); the filings for Penford, Kraton, Meredith, Synacor and STEC — those patterns come from the voice notes only, not from source text; `ref/CollectionInstructions_Alex_2026.pdf` and `ref/SEC_Merger_Auction_Companion_Decision_Note.md`; §12 of the long instruction (the field dictionary for the current multi-table output); the current AI-generated workbooks under `auctions/data/reads/`; and any formula-driven cells in the professor's workbook, since I read it with `data_only=True`.

---

# C. What the four model workbooks reveal about the instruction

All four resolve as keys — Muse's failures are semantic, not dangling. Here is the report.

---

# What the four Providence workbooks reveal about the INSTRUCTION

Sizes: Events **83/70/64/46** rows × **75/70/73/68** cols; Bids **16/14/13/12** rows × **76/66/72/65** cols (astra/fable/ds/muse).

## 1. Field usage audit

**(a) Dead in all four.** Two groups, which must not be treated alike:

*Concept absent in this deal* (demote to optional; confirm across deals before deleting — the instruction's own examples for them are PetSmart, L220/L479/L569): Events `target_requested_price`, `target_price_relation/basis/scope` (0–3%); Bids `alternative_bundle_id` (0/0/0/0); Bids `price_constraint` (0/7/0/0).

*True dead weight regardless of deal*: `record_status` (u=1 `ai_first_pass` everywhere), per-row `deal_id`/`process_id` (u=1), Events `price_currency`/`price_unit` (≤1%), `deadline_for_party_id` (≤2%). Astra adds `source_link`='Open source' ×83. Bids `currency`, `acquisition_scope`, `original_scale`, `share_class`, `core_bid_eligible` are single-*deal* constants — move to Deal level, don't delete.

**(b) Filled by some, not others — the ambiguous requirements** (widest spreads):

| Column | astra | fable | ds | muse |
|---|---|---|---|---|
| Events.`date_lower`/`date_upper` | 93/99% | 96/97% | **25/22%** | 100% |
| Events.`judgment_note` | **2%** | 44% | 92% | 100% |
| Events.`rationale_speaker_id` | **0%** | 13% | 5% | **89%** |
| Events.`related_event_ids` | **0%** | 1% | 17% | **98%** |
| Events.`subject_party_id` | 100% | 90% | **11%** | 78% |
| Events.`round_label` | 100% | 87% | **0%** | 85% |
| Bids.`response_event_id` | 81% | 93% | 100% | **8%** |
| Bids.`exclusivity_status` | 100% | 100% | 100% | **25%** |

Also here, not in (a): `valuation_relation`/`valuation_reference` fill **exactly once in every model** — on B's refusal to raise. That is the professor's DropAtInf, used correctly. Rare but load-bearing: keep as one compact field. Fable's `normalization_formula` (14/14 constant prose) is permitted by L502 ("Calculation and actual inputs, **or reason** the proposal cannot be compared"), so it is ambiguity, not a wrong-kind error.

**(c) Wrong KIND of value.** Almost all Muse:
- `Events!after_event_ids` = **`reported`** (r14, r17, r26, r46); `Events!related_event_ids` = **`reported_sequence`** (same rows) — the `order_basis` enum written into ID fields.
- `Events!relationship_ids` r35 = `"bidder-target NDA population unchanged"`; `Events!origin_round_id` r37 = `"not granted (D/E exclusivity-like requests declined)"` — prose in ID fields.
- `Bids!normalization_input_evidence_ids` — **9/12 rows are prose** (`"no conversion attempted (no bridge inputs)"`, r2–r4, r7).
- `Bids!previous_bid_id` — **three 2-cycles**: r5↔r6 (G&W), r7↔r12 (E), r8↔r11 (D).
- `date_display_us` **is not sortable**: single-date cells = astra 76/83, ds 48/64, **fable 35/70, muse 23/46**. Astra puts filing prose in it (`Events!B10`=`"subsequently"`, `B16`=`"had been advised; reported April 27, 2016"`); fable puts the whole window in it. §12.7's "readable U.S. display with approximation visibly marked" invites both.
- No `"NA"` strings anywhere. Astra instead invented five `<field>_status` columns (`Bids!price_per_share_status` etc.) under §12.1's permission.

## 2. Divergence map

| Fact | astra | fable | ds | muse | Instruction |
|---|---|---|---|---|---|
| Event / Bid rows | 83 / 16 | 70 / 14 | 64 / 13 | 46 / 12 | **Ambiguous.** L304 "a row records a distinct action… not simply a sentence" sets no granularity floor. |
| Round 1 start | `E004` Mar 14 board | `E07` Mar 24 committee | `E006` Mar 24 | `E07` wk of Mar 28 outreach | **Ambiguous by design.** L142 offers *both* "first actual sale-directed outreach" as default *and* "a definite board authorization… can establish its operative launch". Four models, three answers. |
| **27 Jul exclusion of C, D, E, F** | **1 grouped row** `Events!r50`, ~07/25 — *before* the 07/27 selection at r49 | **1 grouped row** r45, subjects `Party C\|D\|E\|F` | **1 grouped row** r39, `(after 07/27/2016)` | **0 rows** — folded into admission r35 | **Permissive on grouping** (`subject_party_id` accepts a list, L468; L300/L374 allow combining homogeneous cases). Nobody split because nothing requires per-bidder rows. Muse separately erred by folding exclusion into the admission row. |
| **"16 of 25 NDA signers never bid"** | absent | absent | absent | absent | **Instruction never asks for it.** §6.1 covers assertions and unique participation but defines no signers-who-never-submitted metric. fable `Counts!r21` and ds `Counts!r13` compute only *contacted-but-no-NDA* = 4. |
| Nine-IOI envelope | `Bids!r2` `core_bid_eligible=`**True** | r2 **False** | r2 **True** | r2 **True**, formality `indeterminate` | **Ambiguous.** L510 forbids an envelope "enter[ing] individual bid statistics" but never says which flag encodes that. |
| GHF→BMO | `Events!r56`, one mandate | r47, one mandate | Parties only, no event | no event; Review r11 | **Clear (L116) and all four complied.** A rule that works. |
| Party A exit | no exit row | no exit row | no exit row | no exit row | **Clear (L66/L291) and all four complied.** Correctly left unresolved. |
| **9 Aug G&W notice** | `r69` `other_material_process_event` + r70 access — no exit | `r59` **`bidder_excluded`**, `exit_agency=target` | `r52` other + r53 access — no exit | `r40` **`bidder_excluded`**, "temporarily displaced" | **The instruction actively caused this.** L326 routes displacement *into* `bidder_excluded` ("distinguish temporary exclusivity displacement"). Fable/muse followed the text. Worse, 9 Aug wasn't exclusivity at all — G&W was told of intent to sign with B and allowed to continue. The missing code is "notified of rival selection, remained active." |
| **Party B final $24** | `Bids!r17` reaffirmation, formal/light | `Bids!r15` reaffirmation | **no Bids row**; `Events!r59` `bidder_valuation_statement` | **no Bids row**; `Events!r43` same | **Ambiguous.** L216 ("an actual final reaffirmation… creates a version") and L329 (`bidder_valuation_statement` is "not itself an offer") both fit the same sentence. |
| E formality (issues list, no markup) | formal | **informal** | formal | **indeterminate** | Ambiguous — §8.2 L231 covers markups, not an issues summary. |
| D/E Aug 1–2 round | R3 | **R02** (receipt R03) | R3 | R3 | Permissive by design (L144 `receipt_round_id`). |
| Conditionality | heavy 13 / light 2 / n-a 1 | 11/2/1 | 10/1/2 | 10/1/1 | **Converged.** §8.3's operational test works. |
| Bidder types, 7 named | identical | identical | identical | identical | **Converged.** §4.1 works. |
| Date-precision classes used | 5 | **6** | 4 | 3 | Only fable used all six. |

## 3. Granularity

Classifying `event_code` against the instruction's own legacy map (L359: Target Sale, Bidder Interest, IB, NDA, Final Round Ann/Inf/Ext, Drop family incl. valuation-reference, Executed, Terminated/Restarted) plus bid submission:

| | astra | fable | ds | muse |
|---|---|---|---|---|
| **Core ledger rows** | **36** | **37** | **30** | **22** |
| **Extra context rows** | **47** | **33** | **34** | **24** |
| of which `other_material_process_event` | 15 | 13 | 10 | 9 |
| `due_diligence_access_changed` | 10 | 4 | 6 | 3 |
| `proposal_document_update` | 6 | 4 | 6 | 1 |
| `initial_sale_contact` / `bidder_admitted` | 6 | 5 | 7 | 8 |
| `strategic_alternatives_review` | 5 | 1 | 1 | 0 |

Core is comparatively stable (22–37, 1.7×); context varies 24–47 (2.0×) and is **more than half of astra's sheet**. Driving sentences:
- **L353** `other_material_process_event` — "do not use as a dumping ground" — it *became* the dumping ground (9–15 rows, the largest single code in three of four).
- **L150** "Record material differences in access to management, customer information, a data room, site visits" immediately followed by "Do not log every routine conversation or document upload". Astra took sentence one (10 diligence rows), muse sentence two (3).
- **L218** "A bidder's submission of revised agreement documents is at least a document-update event" — mandates priceless rows.
- **L152** "Retain stated target rationales… Attribute each rationale to the decision-maker" — muse `rationale_speaker_id` 89% vs astra 0%.
- **§14/L576** lists ten things that must be "accounted for", which reads as a row quota.

## 4. Bidder type

**No model put type on a bid or event row — there is no type column in Events or Bids in any of the four**, because §12.7 and §12.8 don't list one. It lives only in `Parties.bidder_type`, so the most basic column on the professor's sheet is a join away in every workbook. All four agree on the seven named bidders (G&W/A/B/C/E/F strategic, D financial). Cohorts diverge: fable (`Parties!r24–26`), ds (`r21–23`), muse (`r21–22`) write `unknown`; **astra leaves 10 cohorts empty** (`Parties!r23–29, r32–34`), reading §12.5 L444 ("Empty as not applicable for non-bidders") as covering bidder cohorts.

## 5. Invented sheets and columns

- **fable `SourceParagraphs` (46 rows)** — ¶id + printed page + section + full text. The most useful artifact in the set; it makes every locator checkable without opening the filing, and made my §8 quote check possible.
- **fable `Summary` (9)** / **ds `Summary` (12)** — useful; fable `r8` "Price path" and ds `r6–r9` are the one-screen answer to the research question.
- **ds Events `qid`/`ev_basis`/`ev_conf`/`ev_reason`/`ev_premises` + Bids `ev_structure_reason`/`ev_form_reason`/`ev_cond_reason`** — diagnostic: DeepSeek spontaneously **inlined the evidence basis, confidence and reason onto the row** rather than making a reader join Evidence. Two of its eight additions (`ev_form_conf`, `ev_cond_conf`) are 0% filled.
- **ds `Notes` (9)** — `r5` delimiter and `r6` missingness are real; the rest restates the instruction. **muse `Cover` (12)** — no value, restates the instruction. **astra `*_status` ×5** — mixed; `source_link` is a constant.
- **astra has no Validation sheet at all**, though §1 L13 and §14 L588 require a validation report.

## 6. Evidence sheet — not earning its cost

| | rows | distinct quotes | duplication | Bids-subject rows | ev/bid |
|---|---|---|---|---|---|
| astra | **511** | 161 | **68%** | 120 | **7.5** |
| fable | 222 | 142 | 13% | 53 | 3.3 |
| ds | 197 | 68 | **65%** | 39 | 3.0 |
| muse | 29 | 21 | 0% | 5 | 1.0 |

Astra's Evidence sheet is **6.2× its Events sheet**, carrying 161 distinct quotes across 511 rows. All `evidence_ids` resolve in all four workbooks, so it is structurally sound — it is simply expensive: the 68%/65% duplication is the same quote re-entered per field, which is exactly what §12.1 L397 demands ("An interpretation must have its own Evidence entry naming the table, record and field"). Muse shows the opposite failure: 29 rows covering 46 events + 12 bids + 21 parties is under-evidenced to the point of uselessness.

## 7. Review sheet

| | items | policy-confirmation | with recommendation | priority |
|---|---|---|---|---|
| astra | 18 | 1 | **18/18** | 2 blocking, 13 material, 3 routine |
| fable | 16 | 2 | 16/16 | 9 material, 7 routine |
| ds | 12 | 1 | 12/12 | 8 material, 4 routine |
| muse | 13 | 1 | 13/13 | 1 blocking, 8 material, 4 routine |

**Every item in all four carries a model recommendation** — §11 L383 worked. L35's "at most one policy-confirmation item" worked (fable's 2 is the only breach). The failure is elsewhere: **astra `Review!r8–r12` are five rows with identical question text** ("Verify all conditionality assessments in this bidder history"), driven by §11 L376 "Review **all** bid conditionality assessments during the initial pilot… Do not silently waive this pilot check", read as per-bidder. Genuinely consequential: astra `r3` (round map), `r5` (NDA conflict, blocking), `r7` (formality), `r13` (CVR/consideration, blocking), `r14` (exit agency), `r17` (B's Aug 4 version) — **6 of 18**; comparably 6/16 fable, 5/12 ds, 4/13 muse. The rest is category-coverage boilerplate confirming decisions the model already made correctly.

## 8. Self-reported Validation vs. truth

**astra — no Validation sheet.** §14's six check groups are unreported in the file.

**fable**: "Chronology qualified — **seven** events have no representative date (E09, E11, E14, E15, E17, E53, E54)" ❌ — **actually nine**; `E02` and `E25` are also empty. Its Coverage (14 bid versions), Evidence and Structure claims hold.

**ds**: "Coverage **pass** — every disclosed core proposal and meaningful revision is recorded" ❌ — **Party B's final $24 has no Bids row** (only `Events!r59`), and ds emits **zero `bid_not_submitted` events** while asserting 2 non-submitters in `Counts!r10`. "Structure **pass** — all IDs resolve" ❌ semantically (`Rounds!I3` points the latest general deadline at the deadline-*setting* event). Chronology "qualified" is honest.

**muse — five `pass` of six, four of them false**: "Evidence pass" ❌, **2 of 21 quotes are exact** (rest are paraphrases with ellipses, e.g. `Evidence!r4`). "Structure pass — all IDs resolve (checked in build)" ❌ — `Deal!signing_event_id=E34` resolves to a *due-diligence* event (`Events!r36`) and `announcement_event_id=E35` to the D/E bundle (`Events!r37`), plus three `previous_bid_id` 2-cycles. "Chronology pass" ❌ — `Events!r33` date cell is `"07/22/2016 + 07/27/2016"`. "Coverage pass" ❌ — no Bids row for E's Aug 2 reversion or B's final position.

**Crucial nuance for the rewrite:** I checked every `evidence_ids`, `previous_bid_id` and `event_id` in all four workbooks — **zero dangling keys anywhere, including Muse**. Muse's references all exist; they point at the *wrong row*. A key-existence validator would have passed it.

**Pattern: self-validation as written is worthless.** The weakest extraction claimed five passes; the strongest shipped none.

## 9. Top 10 recommendations

1. **Fix the row grammar: one row per (event × bidder).** Enumerate row-triggering actions directly from L359's legacy map — that list already *is* the professor's sheet. Everything else becomes an explicitly optional context row behind a flag. Addresses the 24–47 context spread (§3) and the collapsed 27-July exclusions (§2).
2. **Require the four July-27 exclusions as four rows.** All four models grouped or dropped them because nothing forbids grouping (§2). Make per-bidder-per-event the *format*, not a principle to infer from L304.
3. **Kill `other_material_process_event`** — 9–15 rows/model, the largest code in three of four despite L353's own warning. Either name the missing codes or make it context-only.
4. **Add the two missing codes: "notified of rival selection / displaced but still active" and "declined to improve".** L326 currently routes displacement into `bidder_excluded`, which is why fable and muse coded the *winner* as excluded on 9 Aug; §9 L296 defines refusal-to-raise but §10 gives it no code, which is why ds and muse lost B's final $24 (§2).
5. **Put `bidder_type`, price and formality on the ledger row.** No workbook has type in Events or Bids (§4) because the schema never asked; every basic question currently needs a join to Parties.
6. **Prune, distinguishing two kinds of empty.** Delete outright: `record_status`, per-row `deal_id`/`process_id`, Events `price_currency`/`price_unit`, `deadline_for_party_id`, astra-style `source_link`. Demote to optional pending more deals: `target_requested_price`/`_relation`/`_basis`/`_scope`, `alternative_bundle_id`, `price_constraint` (absent *concepts* here, not unused fields). Keep `valuation_relation` — used once per model, correctly. If the flat ledger has one round column, `receipt_round_id`/`evaluated_in_round_ids` fold into a note; otherwise keep `receipt_round_id`, which fable used deliberately.
7. **Replace the date model with two ISO columns plus one 3-value class.** `date_lower`/`date_upper` fill ranges 22%→100% and the display column is unsortable in 2 of 4 (50%). Specify `date_start`/`date_end` (always both, equal when exact) and ban prose in any date column (astra `Events!B10`=`"subsequently"`).
8. **Collapse Evidence into the row.** Astra's 511 rows at 68% duplication and ds's 197 at 65% both fail §12.1's economics — and ds independently invented inline `ev_basis`/`ev_conf`/`ev_reason` columns (§5). Follow the model that fought the spec: one `quote` + `locator` per row; reserve a separate Evidence sheet for genuine multi-premise inferences only.
9. **Make fable's `SourceParagraphs` a required helper sheet** (¶id, page, section, text). The single most useful invention across the four, and the precondition for any quote verification.
10. **Replace self-validation with mechanical assertions, and cap Review at ~6 items.** Specify checks a script can run *and that catch semantic errors*: every `*_id` resolves **and points at the correct row type** (Muse's did the first, not the second), `previous_bid_id` acyclic, every bidder with a bid has exactly one terminal outcome row, counts reconcile. Drop §14's self-graded pass/qualified/failed (§8). Replace §11 L376's "review all conditionality assessments" with one grouped item — it alone produced astra's five duplicate rows (§7).

## What I did not check

Deal, Processes and Relationships sheets beyond spot references; cell formatting, filters, freeze panes, hidden columns, formulas; whether each `supporting_quote` *supports the specific field* claimed (only whether it is verbatim); quotes against the **full DEFM14A** — my check used `background.txt` only, so out-of-background misses (astra 24, fable 16, ds 21, all from Summary/cover-letter/Reasons passages) are expected and are **not** errors, and my ✅ on fable's and ds's evidence claims is consistent with, but does not independently reproduce, the pro review's full-filing check (163/163 and 194/194); the reviewer's own demonstration workbook; and the four models' chat transcripts, where astra's missing validation report may have been delivered.

---

# D. Requirements coverage: Alex's materials vs Pro's two instructions

Requirements-coverage audit of BASE + OVERRIDE against Alex's materials.

**Citations.** Voice notes by section.point (I.14, 2.K). PDF by printed page/section. BASE = `SEC_Merger_Auction_Extraction_Instruction.md`, OVERRIDE = `pro_review_2026-09-18/SEC_Readable_Excel_Output_Instruction.md`, both by file line (L). "Claude's reading" treated as secondary AI synthesis, never cited as an Alex requirement. The two copies of BASE (`sec2/` root and `pro_review_2026-09-18/`) are byte-identical.

**Not checked:** `deal_details_Alex_2026.xlsx`; `Providence_Worcester_Review_Demonstration.xlsx`; `Providence_Demo_Snapshot.json`; the raw `providence-worcester_*.htm`. I did **not** verify Pro's factual adjudications (Aug 4, Sept 18/24, PetSmart 27 contacts, A/B vs B/C) against the filings — I report only that they contradict Alex and where. The PDF's §3.2.1 spreadsheet screenshots have no text layer.

---

## 1. Requirements coverage matrix

### 1a. Email — "the most important fields"

| # | Requirement | BASE | OVERRIDE | Verdict |
|---|---|---|---|---|
| E1–E4 | TargetName, Acquirer, DateAnnounced, DateEffective | §12.2 L403–407 | §4 L49 | covered |
| E5 | URL — direct link to the readable deal background | §12.2 L405 `source_url`, but L56 "Do not invent an SEC accession number, URL, page number" + L405 "Unsupported metadata remains empty" | §4 L49; §9 L164 "source URL if established" | **partially covered** — field exists, blank unless Austin's pipeline injects it; neither doc says it must be an input |
| E6 | bidderID = events in historical order, fractional numbers so events can be inserted | §12.7 L465 `event_order` "integer display order"; §10 L359 "An old event index called `BidderID` must never become the new stable bidder identifier" | §5 L67 "Order" | **partially covered / contradicted** on fractional insertion |
| E7 | `bidder_type_note` as a per-row most-important field | §12.5 L444 (Parties sheet only; not on Events or Bids) | §4 L53 only, a "concise labelled phrase" in Deal-guide prose | **partially covered (BASE) / missing as joinable data (OVERRIDE)** — see 2f |
| E8 | bid_value / bid_value_pershare; only per-share matters | §12.8 L497–499 | §7 L138 | covered |
| E9 | bid_value_lower / upper for interval IOIs | §12.8 L498 | §6 L126 | covered |
| E10 | bid_type informal/formal | §12.8 L503 `assessed_formality` | §6 L113 | covered (renamed) |
| E11 | bid_date_rough/precise; "I did not bother with this distinction and simply edited bid_date_rough" | §7.1 L176–197; §12.7 L470–472 (nine date fields) | §5 L94–100 | **over-engineered / partly contradicted** — 2a |
| E12 | bid_note vocabulary describing the event | §10 L306–353; L359 legacy map (prose) | §5 L71 | covered semantically; **no column carries the legacy label** — 2g |
| E13 | all_cash | §12.8 L501 | §7 L138 | covered |
| E14 | cshoc — shares outstanding | **absent** (0 hits); only L275 explains division | **absent** | **missing** — 2l |
| E15 | comments_1–3, "definitely legal counsel" | §4.3 L116 | §4 L53 | covered |
| E16 | MM/DD/YYYY U.S. dates | §7.1 L178; §12.7 L472 | §5 L68 | covered |

### 1b. Collection-instructions PDF (§2, §3.2–3.9, §4)

| # | Requirement | BASE | OVERRIDE | Verdict |
|---|---|---|---|---|
| P1 | §2.1 auction = multiple bidders executed NDAs | §3.2 L82 | §4 L49 | covered |
| P2 | §2.1 Alex: collect adviser agreements; legal-adviser name, no date | §3.2 L82; §4.3 L116; §6 L162 | §4 L53 | covered |
| P3 | §2.1 ignore stale-process NDAs | §3.2 L82; §5.2 L132 | — | covered |
| P4 | §2.3 two press-release types | §10 L344, L345, L348 | §5 L90 | covered |
| P5 | §3.2 Target Sale / Target Sale Public / Sale Press Release | §10 L309, L310, L344 | §4 L45 | covered; legacy names only partly in L359 map |
| P6 | §3.2 Bidder Sale + Bid Press Release | §5.1 L126; §10 L345 | — | covered |
| P7 | §3.2 record both Target Sale and Bidder Sale when both occur | §5.1 L122–124 | — | covered |
| P8 | §3.2 Bidder Interest (interest, no bid) | §10 L312 | — | covered |
| P9 | §3.2 Activist Sale, own line, normally before Target Sale | §10 L313–314 | — | covered (ordering convention unstated) |
| P10 | §3.3 IB retention; primary adviser if several | §4.3 L116; §10 L315 | §4 L53 | covered |
| P11 | §3.4 only signed/executed NDAs | §6 L162 | — | covered |
| P12 | §3.4 name unnamed signers a1, a2 …; update if later named | §4.2 L102–104: undistinguishable group "must receive a **cohort ID**, not invented individual histories" | §3 L39; §4 L53 | **contradicted** (C1-adjacent; 2m) |
| P13 | §3.4 cross-check counts against board summaries | §6.1 L168 | §4 L55 | covered |
| P14 | §3.4 bidder type; "the operative word is 'Chief Executive'" | §4.1 L96 "A CEO title … alone is insufficient"; C4 L30 | §4 L53 | **contradicted** — but Chicago text, not Alex's (2m) |
| P15 | §3.5 only whole-company bids | §3.1 L72–74 | §7 L138 | covered (C5 adds excluded-context rows) |
| P16 | §3.5 record a range as e.g. 7.5-8 | §12.8 L498 | §6 L126 | covered |
| P17 | §3.5 group range X–Y recorded as that bidder's bid | C1 L27; §8.4 L269 "not evidence that each bidder offered that range" | §6 L126 | **contradicted** (declared; 2m) |
| P18 | §3.5 "any bid expressed as a range is also … informal" | L21; §8.2 L233 | §6 L124 "A formal range is possible" | **contradicted, correctly** — superseded by Alex's own II.6 |
| P19 | §3.5 formal if final round announced, or markup returned | §8.2 L231–232 | §6 L113 | covered |
| P20 | §3.6 Drop / DropBelowM | §9 L296; §12.7 L478 | §7 L140 | semantics covered; **label missing** |
| P21 | §3.6 Alex: DropBelowInf / DropAtInf / DropTarget | §9 L296 `valuation_relation` | §7 L140 | semantics covered; **label missing**; DropTarget vs C6 (2m) |
| P22 | §3.6 record earlier dropout even if bidder re-enters | §9 L290 | §5 L89 | covered |
| P23 | §3.7 Final Round Ann / Final Round / Inf / Ext | §10 L321–324; L434 `finality_at_time`; L359 | §4 L51 | semantics covered; **label missing** |
| P24 | §3.7 round-announcement rows precede the Drop/DropTarget rows | §7.1 L196 generically | §5 L67 | **partially covered** — convention unstated |
| P25 | §3.8 Executed | §10 L347 | §5 L90 | covered |
| P26 | §3.9 Terminated / Restarted | §5.2 L130–132; §10 L341–343 | §3 L39 | covered |
| P27 | §4 after final-round process letters, later bids formal | §8.2 L232 | — | covered |
| P28 | §4 don't record a part-of-company bid | §3.1 L72 | — | covered |

### 1c. Voice notes I — Providence

| # | Requirement | BASE | OVERRIDE | Verdict |
|---|---|---|---|---|
| I.1 | Quarter / "week of March 28" narrow the window | §7.1 L184–185 | §5 L96 | covered |
| I.2 | date_assigned mis-interpolated from bounds | §7.1 L194; §12.7 L472 | §5 L98 | covered |
| I.3 | Contact ≠ NDA; don't bunch them | §6 L160–162; §10 L311, L317 | §5 L81 | covered |
| I.4 | No double-counted NDAs; memorandum ≠ new NDA; keep only `nda_signed` | §6 L162 (both sentences explicitly) | §4 L55 | covered |
| I.5 | participation_count is a constructed variable, not a fact | §6.1 L166; but §12.9 stores `derived_result` | §4 L55 | **partially covered / over-engineered** — 2d |
| I.6 | Don't track contacts after NDA — "that's gonna blow up the database" | §5.4 L150; §6 L160 | §5 L83 | **partially covered / over-engineered** — 2e |
| I.7 | Deadline-set ≠ deadline-expiry | §7.2 L200; §10 L322–324 | §5 L86 | covered |
| I.8 | Merge round_index and round_count | §5.3 L136 | §5 L69 | covered |
| I.9 | Narrative vs database order; cross-paragraph tightening; flag | §7.1 L192, L196; §11 L369 | §5 L100 | covered |
| I.9b | G&W July 26 revision still round 2; "July 27 is a fair assessment of the deadline" | §13 L562 says July 27 "is not automatically an announced July 27 deadline" | — | **contradicted, silently** — 2i |
| I.10 | Markup ⇒ formal; separate none/light/heavy conditionality for later reinterpretation | §8.2 L231; §8.3 L246–251; L238 | §6 L113–114, L124 | covered |
| I.11 | Party A never left round 1 (low-confidence but useful) | §9 L300 and §2.3 L66 forbid it | — | **contradicted** — 2j |
| I.12 | Infer unannounced round starts; scan for finality language | §5.3 L138, L142, L146 | §4 L51 | covered |
| I.13 | Renamed/acquired IB is one adviser | §4.3 L116 | §4 L53 | covered |
| I.14 | Revision informal→formal; add Aug 4 row, Party B formal unconditional $24 | §8.1 L216, L218; **§13 L561 rejects the conclusion** | §6 L104 | **contradicted, silently** — 2i |
| I.15 | Execution (Aug 12) and public announcement (Aug 15) as two dates | §10 L347–348 | §5 L90 | covered |

### 1d. Voice notes II — Mac-Gray

| # | Requirement | BASE | OVERRIDE | Verdict |
|---|---|---|---|---|
| II.1 | Target approached first ⇒ target interest; keep sequence; initiation "a bit of both" | §5.1 L122–124 (`…mixed`) | §4 L45 | covered |
| II.2 | Missing contact events though counts appear; NDA arithmetic; unstated round-1 start; duplicated advisers | §6.1 L166; §4.2 L104; §5.3 L142; §4.3 L116 | §4 L53, L55 | covered |
| II.3 | Round 2 starts July 25; Aug 27 announcement of a Sept 9 deadline | §5.3 L138; §7.2 L200–202 | §4 L51 | covered |
| II.4 | Party A's NDA is Aug 5; no other strategics | §13 L563 (verbatim case) | — | covered |
| II.5 | "conditions in the same row as the bid itself"; record the *lack* of financing | §8.3 L244 "in the bid row"; §12.8 L505 "explicitly uncommitted" | §6 L114–115 | **covered in principle, contradicted in layout** — 2b |
| II.6 | $18–19 best-and-final range stays formal | §8.2 L233; §13 L564 | §6 L124 | covered |
| II.7 | Exclusivity recorded; must not downgrade formality | §8.3 L257 | §6 L124 | covered |
| II.8 | Invented dropout; real date Sept 24; target-driven; the two are B and C | §2.1 L48, §14 L578 (anti-invention); §13 L565 rejects "B/C" | §10 L178 | covered on invention; **facts contradicted silently** — 2i |
| II.9 | Record the legal adviser's first mention (May 9) to keep event ordering | §4.3 L116 `first_service`; but §10 L355 puts it in "Parties/Relationships, not fabricated retention events" | those sheets abolished (§3 L39); only §4 L53 prose | **partially covered (BASE) / missing from the chronology (OVERRIDE)** |

### 1e. Voice notes III — PetSmart

| # | Requirement | BASE | OVERRIDE | Verdict |
|---|---|---|---|---|
| III.1 | "first week of October" + Oct 3 meeting ⇒ Oct 3–7; meeting also starts round 1 | §7.1 L186; §5.3 L142 | §5 L96 | covered (L186 more conservative) |
| III.2 | "at least 27" is in fact precise | §6.1 L170 "Do not convert a filing's literal 'at least' to an exact count unless other evidence establishes the total" | §4 L59 | **partially contradicted** — burden reversed vs III.2/V.1 |
| III.3 | A third ≥$80 bidder exists; "reached at least $80" bounds the *upper* endpoint | §8.4 L270; §13 L566 | §6 L126 | covered |
| III.4 | Same-day bids by one bidder in narrative order | §7.1 L196; §14 L582 | §5 L100 | covered |
| III.5 | 2 IOI non-advancers dropped by target; 9 NDA-only = reason unknown | §9 L287, L291, L300 | §7 L140 | covered (decision note disputes the fact; not exposed to the model) |
| III.6 | Deadline revisions as their own rows (Dec 10→12); not a new round | §7.2 L202; §5.3 L140; §13 L568 | §5 L86 | covered |
| III.7 | Equity rollover ≠ consortium formation | §4.3 L112; §10 L339; §13 L570 | §4 L53 | covered |

### 1f. Voice notes IV — Penford

| # | Requirement | BASE | OVERRIDE | Verdict |
|---|---|---|---|---|
| IV.1 | Historical stock-price citation is not an IOI | §8.1 L212; §10 L312 | §5 L88 | covered |
| IV.2 | Winner's type always identifiable from elsewhere in the filing | §4.1 L98 | §4 L53 | covered |
| IV.3 | Contacted-and-declined = contact row only; never-contacted = no dropout row | §9 L287, L300 | §5 L89 | covered |
| IV.4 | Absent an explicit start, round 1 begins when the sale process starts | §5.3 L142 | §4 L51 | covered |
| IV.5 | Oct 3 direction to finalize a definitive agreement starts round 2, one bidder | §5.3 L138; §2.1 L44 | §4 L51 | covered |
| IV.6 | Record whom each legal adviser represents | §4.3 L116; §12.6 L458 | §4 L53 | covered |
| IV.7 | Oct 14 confirmation of $19 should be recorded as a formal offer | §8.2 L234 supports; §8.1 L214 "A target's request to confirm a price is not proof that the bidder confirmed it" pushes back | §6 L122 | **partially covered / in tension** |
| IV.8 | "possibly add a row saying that no explicit deadline has been stated"; non-winners dropped at the end | §7.2 L206 (a blank, not a row); §9 L294 | §4 L51 | **partially covered** — 2k |

### 1g. Voice notes V — Kraton

| # | Requirement | BASE | OVERRIDE | Verdict |
|---|---|---|---|---|
| V.1 | Exact counts and type splits usually recoverable; 15 contacts not 14 | §6.1 L168–172 | §4 L55 | covered (same "at least" tension) |
| V.2 | Winner type from "Parties Involved in the Merger"; flag every typeless formal bidder | §4.1 L98; §11 L373 | §8 L152 | covered |
| V.3 | Rounds by our definition, not the banker's (round 2 starts July 6) | §5.3 L138 | §4 L51 | covered |
| V.4 | Dropout reasons: below market / at own IOI / below own IOI / plain | §9 L296; §12.7 L478 | §7 L140 | covered |
| V.5 | Earnout = cash + contingent, not mixed; separate column or row | §8.3 L259; §12.8 L500 | §6 L124 | covered |
| V.6 | Merger-agreement date and announcement as two rows | §10 L347–348 | §5 L90 | covered |

### 1h. Voice notes VI — Meredith

| # | Requirement | BASE | OVERRIDE | Verdict |
|---|---|---|---|---|
| VI.1 | A board discussion of selling a *segment* is not the start of a sale process | §3.1 L78 covers only the converse; §5.1 L122 generic | — | **partially covered** — inferable, never stated |
| VI.2 | Flag deals with only partial bids | §3.1 L76; §11 L378 | §7 L140 | covered |
| VI.3 | Note a tax adviser where disclosed | §12.5 L443 generic "adviser" | §4 L53 | weakly covered (low priority in his own words) |
| VI.4 | Levered-asset bid: subtract net debt ($1.975bn) from EV, divide by shares | §8.4 L275 (method only); **no field stores net debt or share count** | absent | **partially covered** — 2l |
| VI.5 | Detailed deal terms are a *different* project | §5.4 L154 "not a comprehensive legal-terms project" | §7 L144 | covered (correctly excluded) |
| VI.6 | Dual proposal = two bids, not a range; prefer the cash-out structure | §8.1 L220 `alternative_bundle_id`, "Preserve which, if any, the target preferred" | §6 L126 | covered |
| VI.7 | Execution + announcement mis-recorded as "terminated" + "sale process announced" | §10 L341–343 vs L347–348 | §5 L90 | covered |
| VI.8 | 16.99→16.55→16.99 reversion; cross-check the fairness-opinion section | §8.1 L216; §12.8 L494 `reversion`; §1 L15 generic | §5 L89 | covered on reversion; **fairness-opinion cross-check not stated** |

### 1i. Voice notes VII–VIII — Synacor, STEC

| # | Requirement | BASE | OVERRIDE | Verdict |
|---|---|---|---|---|
| VII.1 | 9-month gap = new process; 4-day post-exclusivity = same; flag every multi-process call | §5.2 L132 ("no fixed three-month, nine-month or other gap rule"); §11 L371 | §3 L39 | covered |
| VII.2 | Separate the sale-process announcement from the merger-agreement announcement | §10 L344, L348 | §5 L90 | covered |
| VII.3 | Winner type from context (PE fund financing) | §4.1 L98 | §4 L53 | covered |
| VII.4 | Go-shop is post-signing solicitation | §1 L17; §10 L349 | §4 L57 | covered |
| VIII.0 | Track the target's changing stock price through the process | §8.4 L279 only; **no field anywhere** | absent | **missing** — 2l |
| VIII.1 | 3-month contact gap = two processes | §5.2 L132 | — | covered |
| VIII.2 | Record an activist present but not pushing a sale | §10 L314 `activist_involvement` | — | covered |
| VIII.3 | New board member ≠ consortium | §4.3 L112 | §4 L53 | covered |
| VIII.4 | "at least" NDA counts; duplicated contacts (WDC, Company H) | §6 L160; §6.1 L170 | §4 L55 | covered |
| VIII.5 | Soft deadlines — record whether enforced | §7.2 L204 `deadline_enforcement`; §12.4 L435; §11 L370 | §7 L140 lists only "deadline scope/replacement/expiry type" — **enforcement absent** | covered in BASE; **weakened in OVERRIDE** |
| VIII.6 | WDC's $9.15 IOI with markup, no conditions, mid-process = formal | §8.2 L231, L236 | §6 L122 | covered |
| VIII.7 | Merger-agreement date vs announcement date | §10 L347–348 | §5 L90 | covered |

### 1j. "Alex's summary" — 1, 2.A–2.M, 3

| # | Requirement | BASE | OVERRIDE | Verdict |
|---|---|---|---|---|
| 1a | Interactive, real-time flagging so a wrong round count is fixed before it propagates | §11 L363 "…early **when the session allows progress messages**"; "Continue with a complete provisional extraction unless…" | §2 L17 "Produce a complete first pass, not an assignment for the reviewer" — no interactivity | **contradicted / missing** — 2h |
| 1b | "record the deal background link, including the page" | §2.2 L56; §12.10 L533 | §5 L73; §9 L164 | covered for page; **URL not guaranteed** (E5) |
| 1c | Accepts this blocks large background batches | §1.1 L23 | §8 L152 | covered |
| 2.A | Flag round ends/starts, board meetings near deadlines, re-approached bidders, unstated round-1 ⇒ first IB contacts; infer round names | §11 L369; §5.3 L138, L140, L142 | §4 L51; §8 L152 | covered |
| 2.B | Flag an extension **or the absence of one**; record it | §11 L370; §7.2 L204 | §4 L51 | covered (BASE); thin in OVERRIDE |
| 2.C | Unknown winner type always flagged | §11 L373 | §8 L152 | covered |
| 2.D | Unknown formal-bidder type flagged | §11 L373 | §8 L152 | covered |
| 2.E | Uncertain NDA counts / "mixed" types flagged | §11 L372 | §8 L152 | covered |
| 2.F | Uncertain dropout reason flagged | §11 L374 | §8 L152 | covered |
| 2.G | Conditionality human-verified for the first several deals | §11 L376 "Do not silently waive this pilot check" | §8 L152 | covered |
| 2.H | "Exact dates are less interesting … the order of events must be precise" | §7.1 L196; §14 L582 — but nine date columns L470–472 | §5 L100 | covered on order; **over-engineered on dates** — 2a |
| 2.I | Execution vs announcement; process vs end-of-process announcement | §10 L344, L347–348 | §5 L90 | covered |
| 2.J | "just keep one line per advisor name"; flag unclear affiliation | §4.3 L116 keeps one actor but "retain genuinely different engagements"; §11 L377 | §4 L53 | **partially covered** — deliberately richer than "one line" |
| 2.K | "For some reason, indications of interest and bids are recorded as separate rows. Why is this necessary?" | §8.1 L214 "One IOI and the bid represented by that IOI are **one proposal**, not two submissions"; §8.2 L240 | §6 L104 | **covered in text — reintroduced by the Timeline/Offers split** — 2b/2c |
| 2.L | Flag deals without whole-company bids | §3.1 L76; §11 L378 | §7 L140 | covered |
| 2.M | Flag unclear currency/units and EV-vs-equity | §8.4 L273, L275; §11 L378 | §6 L126; §7 L138 | covered |
| 3 | Less pervasive issues also flagged | §11 L371, L379 | §8 L152 | covered |

---

## 2. Contradictions and over-reach

**(a) Dates.** Email p.2: *"I did not bother with this distinction and simply edited bid_date_rough. We want to know the sequence of events but not necessarily the exact date"*; 2.H: *"Exact dates are less interesting to me, but the order of events must be precise."* BASE answers with nine date columns per event (L470–472) and a nine-row lexical table (L180–190). OVERRIDE then removes the one column he actually filled — L98: *"Retain the base instruction's representative-date convention only in a separate technical field where applicable"*; L96: *"'After August 1; exact day not disclosed' is usable output."* Combined with BASE L194 (*"If bounds are one-sided or unknown, leave the representative date empty"*), no column is guaranteed to hold one sortable date per row. **Over-engineered on precision, under-specified on the single output he uses.**

**(b) Conditions in the bid row.** II.5: *"ideally we want to have conditions in the same row as the bid itself."* BASE complies (L244: *"Record financing, diligence, regulatory/completion issues … in the bid row"*). OVERRIDE splits every bid across two sheets — L77: *"Keep names and prices in Timeline even though a focused version is also in Offers. This is a readable mirror, not a second submission."* Each bid appears twice; conditionality lives only on the Offers copy, so the chronological row a human reads does not carry it. The duplication he objected to moves from rows to sheets.

**(c) 2.K, IOI and bid.** Both docs state the rule correctly (BASE L214; OVERRIDE L104, one row per economically distinct version). But OVERRIDE L104 adds a **checkpoint** row — *"when preserving a document or condition development is useful but a new submission … is not established"* — on top of the Timeline mirror. One bid yields 2–4 physical rows. L128 mitigates (*"Checkpoints and mirrors do not add bidders or new priced submissions"*) but does not restore one-bid-one-row.

**(d) participation_count.** I.5: *"participation_count is a constructed variable, and it is not a fact that we extract."* BASE L166 agrees at event level (*"Do not emit a standalone `participation_count` event"*) — then §12.9 stores it on both sides: `claim_role` = *"`reported_summary` or `derived_result`"* (L517), with `input_event_ids`, `calculation`, `reconciliation_group_id`, `reconciliation_status` (L520–521). OVERRIDE L55 keeps it as "Participation checks". He asked for the number to be *recoverable*; he got a reconciliation subsystem. **Over-engineered.**

**(e) Post-NDA contacts.** I.6: *"there will be tons of these contacts … that's gonna blow up the database."* BASE has the prohibition (L150, L160) but §10 supplies six post-NDA codes that invite exactly those rows — `due_diligence_access_changed` (L319), `management_presentation` (L320, *"retain individual timing when relevant"*), `proposal_document_update` (L332), `target_price_request` (L333), `material_information_update` (L340), `confidentiality_agreement_updated` (L318) — plus four exclusivity codes (L334–337). OVERRIDE L83 repeats the caution, but L81 pushes the other way: *"A broad row containing a bidder's re-entry, two parties' revised bids, a reversion and a withdrawal is too compressed."* **Over-reach relative to I.6.**

**(f) bidder_type.** BASE puts it on Parties only (L444). OVERRIDE abolishes Parties (L39) and relocates type to Deal-guide prose (L53: *"concise labelled phrases rather than many mostly empty columns"*). Its own technical minimums omit it — Timeline L136 lists "participant identity links", Offers L138 "bidder unit". Under the controlling document **bidder type has no typed column anywhere**; estimation code cannot join on a phrase.

**(g) Legacy vocabulary.** BASE L359 maps it in prose only: *"'Drop/DropBelowM/DropBelowInf/DropAtInf/DropTarget' → participation outcome plus agency and valuation-reference fields."* I searched both documents: **no output column carries a legacy label.** The nearest are `source_stage_label` (L430, the *filing's* wording) and `source_bid_label` (L495, IOI/LOI wording) — neither is the research vocabulary. Reconstructing `DropBelowInf` requires joining `event_code` + `exit_agency` + `valuation_relation` + `reference_bid_id`. **Cheapest high-value fix in this audit: one `legacy_bid_note` column.**

**(h) Interactivity.** Summary 1 asks for real-time flagging *"via the interactive Claude Desktop app"*, motivated by one failure mode: a wrong round count the human must then fix on every row. BASE L363 downgrades it to *"when the session allows progress messages"* and insists on continuing to a complete pass. OVERRIDE drops it — §2's heading is *"Produce a complete first pass, not an assignment for the reviewer."* The substitute, propagation, is disclaimed by OVERRIDE L156: *"an accepted correction requires regenerating a versioned reviewed view … Do not claim automatic propagation."* His motivating case is unsolved both ways.

**(i) Silent factual overrides — the single biggest structural problem.** BASE §13 decides against Alex in three rows, presented to the model as *"Correct extraction consequence"*: L561 *"Do not infer that every condition was removed on August 4"* (vs I.14, which asks for that row); L562 July 27 *"is not automatically an announced July 27 deadline"* (vs I.9b *"July 27 is a fair assessment"*); L565 *"Do not identify B/C as the two continuing rivals"* (vs II.8). Pro's reasoning exists only in the decision note (§3 L44/45/47) — and **both documents exclude that note from the model's materials**: BASE L5 *"its development materials and companion decision note are not required"*; OVERRIDE L15 *"not needed by a future extracting model."* The extracting model inherits Pro's verdict with no trace that the professor said the opposite, and no review category reopens it. Neither document contains any instruction of the form "where this guidance departs from Alex's recorded reading, raise it."

**(j) I.11, Party A.** Alex: *"low-confidence, but useful … this kind of inference requires a bit of cross checking and, I guess, a bit of human judgment."* BASE bans it twice — L66 *"Absence of a later named mention does not prove a bidder's identity, withdrawal, or round of exit"*; L300 *"Do not infer the identity of a missing strategic bidder from the fact that a named strategic bidder disappears."* Correct as a bar on *asserting* it, but he wanted a flagged hypothesis and neither document offers a home: there is no review category for inferred cohort-membership exclusions, and `identity_status=mapping_uncertain` (L446) records uncertainty, not a hypothesis. **Silent override.**

**(k) Deadlines.** VIII.5 well covered in BASE (L204 `deadline_enforcement=observed_cutoff|extended|late_submissions_accepted|…`, plus L435 and review category L370) but **absent from OVERRIDE's technical minimum** (L140 lists only "deadline scope/replacement/expiry type"). III.6 fully covered (L202, L323, L568). IV.8 **not**: BASE L206 offers only *"The observed end of a round can be recorded even when no deadline was announced"* — a blank cell, indistinguishable from an extraction miss across 800 deals.

**(l) Stock price, net debt, shares outstanding.** BASE contains **zero** occurrences of "stock price" or "shares outstanding"; its only provision is L279 *"Collect disclosed market-price benchmarks and their dates when relevant to an offer comparison or withdrawal statement"* — which has **no receiving field in any of the ten tables**, and is scoped to comparisons, not a series. L275 explains normalization but no field stores the net-debt or share-count inputs (only free-text `normalization_formula`, L502). OVERRIDE: zero hits for shares, net debt, market price or stock price. **Missing in both**, against VIII intro, VI.4 and email `cshoc`.

**(m) C1–C7 vs the written record.** Accuracy correction first: PDF §3.4 Table 1 (CEO heuristic) and §3.5 Table 2 (copy the X–Y envelope) carry **no "Alex's addition" box** — per his email p.1, *"Everything in black is instructions by Chicago guys"*. They are inherited text, not rules he wrote.
- **C1** (L27) replaces §3.5's envelope-copying and §3.4's a1/a2 placeholders with cohorts/envelopes. Chicago rule; Alex's own Zep comment (`AG6390`) treats expansion as an open question. Declared as needing approval.
- **C2** (L28) is not a replacement but an **accretion** onto his one-rough-date practice (see 2a).
- **C3** (L29) implements I.10/II.5 faithfully; the none/light/heavy thresholds (L246–251) are Pro's and are labelled as such.
- **C4** (L30) replaces §3.4's *"the operative word is 'Chief Executive'"* — Chicago text. Analytically right; IV.2/V.2 only demand that types be *resolved*, and Alex never defends the CEO test.
- **C5** (L31) is a genuine addition: §3.5 records only whole-company bids; C5 keeps excluded-context rows with `core_bid_eligible=false`. Row growth he did not ask for, though it serves VI.2/2.L.
- **C6** (L32) is the one policy that overrides text **Alex actually wrote**: his §3.6 addition defines `DropTarget` = *"target does not invite the bidder to the final round"*, and II.8 says of the Sept 24 exclusivity grant *"the other two are dropped out by the target … it's the target that drops them."* C6 recodes that as temporary displacement.
- **C7** (L33) is consistent with 2.A–2.M; BASE L376 explicitly refuses to waive the conditionality check.

---

## 3. Dangling BASE↔OVERRIDE references

OVERRIDE L9 supersedes *"the ten-table mandate in base §1, the mandatory physical schemas and table names in §12, the requirement for a separate field-level Evidence table, and conflicting presentation, validation-report and final-delivery requirements in §§14–15."* Everything below either survives that list while pointing at an abolished object, or sits ambiguously inside it.

| BASE line | Text | Why it dangles |
|---|---|---|
| 48 | *"Use field-specific entries in Evidence."* | Evidence table abolished; OVERRIDE L142 substitutes but never repoints this sentence. |
| 58 | *"Each substantive record must link to Evidence entries containing: source filename…"* | No target for the link. |
| 166 | *"In Counts, preserve each consequential source assertion … In Events, preserve the underlying contact…"* | Counts → Deal guide "Participation checks" (L55); Events → Timeline. Sits in substantive §6.1, not §12. |
| 168, 523, 525 | *"Keep the source total in Counts"*; the emit-either/or rule | L168 is substantive §6.1 text naming an abolished sheet. |
| 330 | `acquisition_proposal_submitted` — *"link proposal versions **in Bids**"* | Bids → Offers. |
| 355 | *"Legal-adviser names and first observed service normally belong in **Parties/Relationships**"* | Both abolished (L39); the only home left is Deal-guide prose, outside the chronology (see II.9). |
| 357 | *"do not emit duplicate `round_opened` rows just because the same decision is also **linked from Rounds**"* | Rounds abolished. |
| 383 | *"Each Review item must contain … affected IDs/fields"* | Party/round/count IDs have no defining sheet; OVERRIDE L150 says "specific affected entries" without restoring an ID scheme. |
| 550 (§12.12) | *"In **Bids**, put the date, bidder name, round … In **Events**, put sequence…"* | §12.12 is presentation, not named in L9's list, so it plausibly survives — pointing at two renamed sheets and duplicating OVERRIDE §5/§6. |
| 74, 496 | `core_bid_eligible=false` | Survives (OVERRIDE L138 "scope") but the column has no declared name under five sheets. |

**Mechanism removed, requirement retained:**
- L536 *"An assessment using multiple passages should have a conclusion entry linked to premise entries, each with its actual quote."* With no Evidence table there are no entries to link. OVERRIDE L116 asks Offers to *"identify additional premises for a cross-paragraph judgment"*; the Timeline Evidence column (L73) asks only for *"a short exact supporting quotation."* **Cross-paragraph premise chains — the mechanism I.9 and III.3 depend on — lose their home on the Timeline.**
- L391 assigns ID prefixes `D, P, R, A, L, E, B, C, V, Q` for ten tables; L393 mandates `evidence_ids`, `review_issue_ids`, `record_status` on every record. OVERRIDE L136 still requires "participant identity links" and "process/round key or number" but never says where those IDs are defined, and drops `record_status` for Timeline.
- L588 *"Report `pass`, `qualified` or `failed` for these **six** check groups"* vs OVERRIDE L184's **three**. Precedence settles the count, not the content: BASE's *Identity and quantities* (L580) and *Chronology* (L582) have no counterpart, so a model following OVERRIDE alone drops the denominator and representative-date checks.
- L13 *"Also provide a short plain-language process summary and a validation report"* survives as a remnant of a superseded sentence.

## 4. Candidate deletions

| BASE section | Lines | Bytes | Recommendation |
|---|---|---|---|
| §1.1 policy table C1–C7 + Status column | 19–36 | 3,397 | **Cut from the model's copy.** *"requires research approval before treating the new representation as final"* is governance addressed to Austin and Alex; the extractor cannot act on approval status. Keep each policy's operative half inline in §3–§9. |
| §12 field dictionary (12.1–12.12) | 387–553 | ~22,500 | **Merge, don't delete.** OVERRIDE L104 leans on §12's definitions (*"under the base definitions"*), so fold §12's field *semantics* into OVERRIDE §7 as one list, then delete §12. §12.3/12.4/12.5/12.6/12.9/12.10 describe sheets no longer produced (~9 KB) — those go outright. |
| §13 worked calibration examples | 554–571 | 3,638 | **Cut 7 of 11 rows.** Deal-specific facts carrying their own warning (L556), and three contradict Alex (2i). Keep the PetSmart ≥$80 endpoint row (L566) and the Mac-Gray 20-signer partition (L563). |
| §14 completion checks | 572–589 | 2,780 | **Cut**, after folding *Identity and quantities* and *Chronology* into OVERRIDE §10, which currently loses them. |
| §15 final response | 590–595 | 796 | **Cut** — duplicated by OVERRIDE L186–188. |

≈ **33 KB of 87 KB (38%)** is superseded, duplicated or governance-only; realistic saving after merging §12's semantics into OVERRIDE §7 is **30–35 KB**. Separately, BASE holds 83 "Do not" sentences, 26 "never/Never", 16 "invent"; roughly a quarter are restatements (L66 / L291 / L300 on absence-of-mention; L48 / L397 / L536 on field-level evidence) and could be said once.

## 5. Rules a flat one-row-per-event ledger still needs

1. **Cross-deal stacking.** Five per-deal sheets, ~800 deals, no statement of how they concatenate into one panel keyed on `deal_id`. BASE L391 puts `deal_id` on every record; OVERRIDE never mentions it. Row-key uniqueness across workbooks is undefined.
2. **Row identity after a human edit.** BASE L465 makes `event_order` an *"integer display order"*. Alex's fractional scheme existed so an inserted event does not renumber the deal. Nothing says what happens to `event_order`, `after_event_ids` and mirrors when a reviewer inserts a row.
3. **Four coexisting anonymous-party schemes**, no precedence: PDF `a1, a2`; BASE L102 "Party A"; L102 `U001`; L102 cohort ID. Reruns can relabel the same party.
4. **Cohort rows.** When one sentence reports N bidders doing one thing — one row or N? BASE L523 says "either … or" and fixes no default, so row counts are not comparable across deals or reruns.
5. **Stock / exchange-ratio consideration.** The price schema assumes cash per share; `all_cash=0` (L501) flags stock but no field holds an exchange ratio or its valuation date. S-4s are in scope per PDF §1.
6. **Source precedence within a filing.** VI.8 wants the fairness-opinion section used to cross-check the last bid; BASE L11/L379 flag contradictions but give no rule for which section wins.
7. **Non-USD offers.** `currency` exists (L499); no FX rule, no conversion date.
8. **Winner marking.** Deal carries `acquirer_party_id`, but no bid-level or party-level winner flag — "which row is the winning bid" is a join, not a column.
9. **Price rounding/precision** is unspecified.
10. **Market-data rows.** If VIII intro's stock-price series is added, the ledger needs an actor, an event code and a rule separating market observations from process events.

---

# E. Pro demo workbook vs Alex's Providence ledger, row by row

# Providence demo workbook vs. the professor's ledger — row-level comparison

Notation: **P####** = `deal_details_Alex_2026.xlsx!deal_details` Excel row; **TL r##** = `Providence_Worcester_Review_Demonstration.xlsx!Timeline` Excel row (data rows 6–65 = Order 1–60); **OF r##** = `Offers` Excel row (6–21 = O01–O16); **BG-0##** = paragraph ID in `background.txt`.

## 1(a) Professor's 36 rows → demo

| P-row | Professor (M / N / date / AC / Z) | Demo TL | Demo OF | Agreement / disagreement |
|---|---|---|---|---|
| 6024 | 0.3 Party A, AB 2015-12-31, Bidder Interest, S | r6 | — | Who/what/type agree. Demo window 10/01–12/31/2015 (TL r6 M/N) vs his point 12/31. His AA=2016-07-22 on this row is internally inconsistent (see 6026). |
| 6025 | 0.5 GHF, 2016-01-27, IB; AG "Legal advisor: Hinckley Allen" | r7 (+r10) | — | Date/adviser agree. Demo splits legal counsel to TL r10 (03/24, first mention). |
| 6026 | 0.7, AB 2016-03-14, Target Sale | r8 | — | Agrees. Again AA=2016-07-22, unexplained. |
| 6027 | 1, "25 parties incl. A, B", AB 2016-03-28, NDA, "11S, 14F" | r12 (NDA) + r11 (contacts) | — | Counts agree (11+14=25; TL U=25). **Date disagreement**: he dates NDAs 03/28; demo leaves NDA undated and dates *contacts* 03/28–04/03. He also lists Party B among 03/28 signers though B is first met 04/21. |
| 6028 | 2, G&W, 2016-04-13, (blank label) | r13 | — | **Date disagreement**: his 04/13 vs demo 04/03–04/06. |
| 6029 | 3, "9 parties", 17.93 / lower 17.93 / upper 26.5, Informal, AB 2016-05-19 | r21 | r6 (O01) | Who/what/price/formality agree. **Date**: his point 05/19 vs demo interval 05/19–06/01. Demo keeps the envelope out of individual-range fields (OF T/U). |
| 6030 | 4, "16 parties", 2016-06-01, Drop | **none** | — | **No demo counterpart.** The 25 NDA signers minus 9 IOI submitters. Demo never records the 16 non-bidders. |
| 6031 | 5, "2 parties", 2016-06-01, DropTarget | r23 | — | Agrees on who/what. Date: his 06/01 vs demo window 05/23–06/01 "selection day uncertain". |
| 6032 | 6, AB 2016-06-15, Final Round Inf Ann; AH "probably something we will not collect" | r25 | — | Date/content agree (demo 06/11–06/19). **Label divergence**: he marks an announced informal final round; demo TL r25 F says "not an expressly announced final round". His own AH downgrades the row. |
| 6033 | 7, Party C, AB 2016-07-01, NDA, S; AG "what should be the appropriate date? July 1?" | r27 + r28 | — | Agrees. Demo answers his question with windows (interest 07/01–07/10; NDA 07/01–07/12) and splits interest from NDA. |
| 6034 | 8, Party C, 21.00, Informal, 07/12 | r29 | r7 | Full agreement (who/date/price/formality/type). |
| 6035 | 9, Party B, 24.00, Formal, 07/20; AH "expedited DD" | r33 | r9 | Who/price/formality agree. **Date**: his 07/20 vs demo 07/20–07/27. |
| 6036 | 10, Party E, 21.26, **Informal**, 07/20; AH "60 day exclusive DD" | r34 | r10 | **Formality disagreement** (demo Formal, medium). Type S agrees. Date as above. |
| 6037 | 11, Party D, 21.00, **Informal**, 07/20, F; AH "4 week DD" | r35 | r11 | **Formality disagreement** (demo Formal, high). Type financial agrees. |
| 6038 | 12, Party C, 19.30, Informal, 07/20; AH "30 day DD" | r36 | r12 | Agrees on everything but date precision. |
| 6039 | 13, Party F, 19.20, Informal, 07/20, **S='F' financial** | r37 | r13 | **Bidder-type disagreement** (demo strategic). Formality agrees (both informal). |
| 6040 | 13.5, AB 2016-07-20, Final Round Inf | r31 | — | Agrees (round-2 deadline 07/20). |
| 6041 | 14, G&W, 21.15, **Informal**, 07/21, **AD=1 all-cash**; AG "20.02 + 1.13 CVR" | r32 | r8 | Who/date/price components agree. **Formality disagreement** (demo Formal). **all_cash disagreement**: he sets 1; demo leaves OF AA blank, medium `cash_plus_CVR_settlement_unspecified`. |
| 6042 | 15, Party A, 07/22, Drop, S | **none** | — | **No demo counterpart.** Demo TL r40 refuses to identify either LOI non-submitter as Party A. |
| 6043 | 16, "1 party", 07/22, Drop | r40 (shared) | — | Demo merges 6042+6043 into one row; no date (his 07/22 is not in the filing); demo notes one strategic + one financial. |
| 6044 | 17, G&W, 22.15, Formal, 07/26, AD=1 | r39 | r14 | Agrees who/date/price/formality. **all_cash** disagreement as 6041. Note he codes 07/21 informal and 07/26 formal on identical documentation. |
| 6045 | 17.5, AB 2016-07-27, Final Round Ann | r41 (+r38) | — | Date/decision agree. **Label divergence**: announced vs. demo's "Round 3 inferred, not announced finality". |
| 6046 | 18, Party E, 07/27, DropTarget | r42 (shared) | — | Demo compresses four bidder exits into **one** row, undated ("After selection; D/E notified before 07/29"). |
| 6047 | 19, Party D, 07/27, DropTarget, F | r42 (shared) | — | as above |
| 6048 | 20, Party C, 07/27, DropTarget, S | r42 (shared) | — | as above |
| 6049 | 21, Party F, 07/27, DropTarget, **F** | r42 (shared) | — | as above + type disagreement (6039). |
| 6050 | 22, Party D, 24.00, **Informal**, 08/01; AG "Reengaged" | r45 | r15 | Who/date/price agree. Formality disagreement (demo Formal). |
| 6051 | 23, **"Party E/F"** mixed (Q=1, S/F), 23.81, Informal, 08/01 | r46 | r16 | **Bidder-unit disagreement**: demo keeps E as submitter, F as financing supporter. Price/date agree; formality disagrees. |
| 6052 | 24, "Party E/F", 21.26, Informal, 08/02 | r48 | r17 | Price/date agree; bidder unit and formality disagree. Demo labels it withdrawal-and-reversion. |
| 6053 | 25, Party D, 08/02, Drop, F | r49 | r18 (O13) | **Date disagreement**: demo refuses 08/02, uses 08/01–08/12. |
| 6054 | 25.5, Party B, 24.00, Formal, AA 07/20 / AB 08/04, **AC='Executed'**; AG "Confirm 7/20 bid after DD" | r52 | r19 (O14) | Row exists in both. **Substantive disagreement**: demo calls it a *document checkpoint*, `individual_bid_eligible=FALSE`, conditionality **heavy**; he (and voice I.14) want a formal **unconditional** $24 bid revision. `AC='Executed'` on Party B is anomalous (elsewhere 'Executed' marks the winner, cf. P6020, P6059). |
| 6055 | 26, G&W, 25.00, Formal, 08/12, AD=1; AH expiry 8/13 | r56 | r20 (O15) | Full agreement incl. all-cash and expiry. |
| 6056 | 27, Party B, 08/12, **Drop**; AG "Refused to increase offer" | r59 | r21 (O16) | **Convention divergence**: demo records a maintained standing offer, explicitly not a withdrawal. Same underlying fact. |
| 6057 | 28, "Party E/F", 08/12, Drop | **none** | — | **No demo counterpart.** Demo has no terminal E event after 08/02. |
| 6058 | 28.3, AB 2016-08-12, Final Round; AG "English auction stopped by the target" | r57/r60 (partial) | — | No dedicated round-close row in the demo; its R3 packet states the same substance ("no announced final submission deadline"). |
| 6059 | 28.5, G&W, AA 08/15 / AB 08/12, Executed | r61 + r62 | — | Agrees. Demo **splits** execution (08/12) from public announcement (08/15) into two rows — exactly voice I.15. |

## 1(b) Demo Timeline → professor

**32 rows have a counterpart**: r6→6024, r7→6025, r8→6026, r11/r12→6027, r13→6028, r21→6029, r23→6031, r25→6032, r27/r28→6033, r29→6034, r31→6040, r32→6041, r33→6035, r34→6036, r35→6037, r36→6038, r37→6039, r38/r41→6045, r39→6044, r40→6042+6043, r42→6046–6049, r45→6050, r46→6051, r48→6052, r49→6053, r52→6054, r56→6055, r57/r60→6058, r59→6056, r61/r62→6059.

**28 rows with no counterpart:**

| TL row (Order) | Event | Class |
|---|---|---|
| r10 (5) | Outreach authorized 03/24; Hinckley Allen first observed | **Useful** — II.9 (record adviser's first mention); summary 2.A (round-1 start = first contacts) |
| r11 (6) | Broad outreach, 29 contacts, week of 03/28 | **Useful** — I.3 (contact ≠ NDA), II.2 ("the event itself is not recorded"), summary 2.A |
| r14 (9) | Two additional Class I railroads approached by 04/07 | **Useful** — implied contact event (II.2), affects counts |
| r15 (10) | Party B introductory meeting 04/21 | **Useful** — named pre-NDA contact; contradicts P6027's 03/28 dating |
| r17 (12) | Initial bid deadline set (May 10), by 04/27 | **Useful** — I.7 (deadline set vs expired) |
| r18 (13) | Deadline extended 05/10→05/19 | **Useful** — I.7; summary pt 13 / 2.B (extensions as own rows) |
| r19 (14) | Original scheduled deadline 05/10 (superseded) | **Useful** — I.7 |
| r20 (15) | Revised scheduled deadline 05/19 | **Useful** — I.7 |
| r22 (17) | Committee reviews IOIs 05/23 and 06/01 | **Useful** — summary 2.A (committee meeting at/after deadline must be flagged) |
| r24 (19) | Seven admitted; data-site access expanded | **Useful** — round-2 start marker; summary 2.A |
| r47 (42) | Committee evaluates revised LOIs; GHF→BMO succession 08/01 | **Useful** — I.13 / summary 2.J (one adviser, not two) |
| r54 (49) | 08/09 target tells G&W it intends to sign with a rival; G&W allowed to continue | **Useful** — prevents the false exit/re-entry pair other runs produced (change log C04) |
| r58 (53) | Board asks BMO whether B will raise price 08/12 | **Useful** — the target's price solicitation; the mechanism behind his own "English auction stopped" note (P6058) |
| r62 (57) | Public announcement 08/15 | **Useful** — I.15 / summary 2.I |
| r9 (4) | Management met Party A 03/22–23 | Harmless context (pre-NDA) |
| r16 (11) | Information memorandum distributed to NDA signers | Harmless context — and the explicit anti-double-count record I.4 asks for (U blank, no new NDA) |
| r26 (21) | Target posts merger/voting/disclosure templates 06/29, 06/30, 07/11 | Harmless context |
| r44 (39) | D and E express re-entry interest 07/29 | Harmless context (he folds it into "Reengaged" comments) |
| r51 (46) | Committee prioritizes Party B 08/04 | Harmless context |
| r57 (52) | Final offers compared, board 08/12 | Harmless context |
| r60 (55) | Board approves G&W 08/12 | Harmless context (approval ≠ execution) |
| r63 (58) | STB petition 09/01 | Harmless context (post-signing) |
| r64 (59) | BMO affiliate conflict, board reconsiders 09/06 | Harmless context (post-signing) |
| r65 (60) | Voting-trust form to STB 09/14 | Harmless context (post-signing) |
| r30 (25) | Party C data-site access + management presentation 07/14 | **I.6 "blow up the database"** — post-NDA diligence contact |
| r43 (38) | On-site diligence 07/27–08/11 | **I.6** (load-bearing as *evidence* for conditionality, not as a ledger row) |
| r50 (45) | Counterdrafts to B 08/01 and G&W 08/03; diligence answers 08/03 | **I.6** — draft exchange |
| r53 (48) | Target counterdraft to B 08/05 | **I.6** — draft exchange |
| r55 (50) | Counsel discussions 08/10–08/11; physical diligence complete | **I.6** — draft/diligence detail |

## 2. Adjudication of the disagreements

**Formality — three-way.** BG-012: "Party B, G&W and another bidder ('Party D') also provided mark-ups of the draft merger agreement and voting agreement. One bidder ('Party E') provided a summary of material issues and proposed changes".

| Bid | Professor (Z) | I.10 rule applied to BG-012 | Demo (OF AB) | Verdict |
|---|---|---|---|---|
| G&W 07/21 (P6041) | Informal | Formal + conditions (markups incl. disclosure letter, BG-014) | Formal | **Demo right**, sheet stale |
| Party D 07/20 (P6037) | Informal | Formal + conditions (BG-012) | Formal | **Demo right**, sheet stale |
| Party B 07/20 (P6035) | Formal | Formal + conditions | Formal | agree |
| Party C / F (P6038/6039) | Informal | Informal (no markup in BG-012) | Informal | agree |
| Party E 07/20, 08/01, 08/02 (P6036/6051/6052) | Informal | **Informal** — "summary of material issues", not a markup | Formal (medium) | **Demo is the outlier against both**; it flags this itself (R4, change log C11) |

**Party F type.** BG-018: "Party F (a strategic buyer)". **Demo right**; P6039/P6049 code F financial (O=1, S='F').

**Party E/F as one bidder.** BG-021: "Party E submitted a revised LOI, along with financing support, from Party F". **Demo right** on the submitting unit; his `bidder_type_mixed=1` (P6051/6052/6057) is his *type taxonomy*, not a claim of joint control — the flat ledger needs both a `financing_support_from` field and his mixed flag without renaming the bidder.

**G&W introductory date.** BG-005: "Between April 3, 2016 and April 6, 2016". **Demo right**; P6028's 04/13 is unsupported.

**The 16-party drop dated 06/01 (P6030).** BG-008 gives 9 IOIs and a 7-of-9 partition; it never states what happened to the other 16 NDA signers or when. **Neither is supported by the text**; his 06/01 is an inference, the demo's omission loses the fact that 16 signers never bid. Record it as an inferred non-submission cohort with no date.

**Party A drop 07/22 (P6042).** No paragraph mentions Party A after BG-007. **Demo right to refuse**; note his own voice I.11 now argues A exited in round *one*, contradicting his 07/22 row.

**Late-July LOI window.** BG-020: the committee met "on July 22, 2016 and in person after the regular quarterly Board meeting on July 27, 2016, to review the LOIs". Voice I.9 infers 07/20–07/22. Demo uses 07/20–07/27 (TL r33–r37 M/N). **Alex's tighter bound is better supported**; the demo's is merely literal. The demo *did* fix I.9's ordering complaint — C's 07/12 IOI is Order 24, ahead of the late-July LOIs at Orders 28–32.

**Party B 08/04 (P6054 / voice I.14).** BG-023: "On August 4, 2016, legal counsel for Party B provided a revised draft of the merger agreement" — no price, no unconditionality language. Demo's literal reading is defensible; Alex's is an expert inference he has explicitly asked for. **Unresolved by the filing** — the demo's "heavy" condition label, not the row's existence, is the live dispute.

**Party B 08/12 (P6056).** BG-026: "Party B indicated that it would not increase its price." No withdrawal language. His `Drop` is a *convention* (every bidder gets a terminal exit row in his ledger), not a misreading — and it is what makes his sheet answer "each bidder's exit" by construction.

**Party D 08/02 (P6053).** BG-021 dates only E's withdrawal to August 2; D's refusal shares the sentence but not the date. Demo technically right; its 08/01–08/12 window is looser than needed.

**Final-round announcement (P6045 / P6032).** BG-020's "proceed with confirmatory due diligence and negotiations with G&W and Party B" is precisely the "less lucky" signal voice I.12 says counts. Demo calls round 3 "inferred, not announced" — which also matches I.12's own words ("round three ... was not announced"). **Convention difference, not an error.**

**all_cash with a CVR (P6041/6044 vs OF r8/r14).** BG-014 gives $20.02 cash + $1.13 CVR. The cross-deal summary (pt 5) states an earnout is "a cash offer with a contingent payment, not a mixed offer", i.e. Alex's rule gives all_cash=1. **The demo departs from his stated convention** (leaves OF AA blank, R5/C08).

## 3. Duplication audit

Every price, formality and conditionality label exists in at least three places: Timeline prose (E/F), Offers prose (C/D/E) and Offers typed columns (Q/V/W/AB/AC). All **price** copies agree exactly (16/16 offers checked: $17.93–26.50, 21.00, 21.15/20.02/1.13, 24.00, 21.26, 19.30, 19.20, 22.15/21.02/1.13, 24.00, 23.81, 21.26, 25.00 all-cash, 24.00 ×3). All **formality/conditionality** copies agree where both exist. Counts agree: TL r11 T=29 = Deal guide B44; TL r12 U=25 = B47; TL r28 U=1 = B48; TL r38 prose "seventh LOI version" = B57.

Mismatches found:

1. **`Offers!A` vs `Timeline!B`, 5 rows** — OF r9–r13 say "Late July; before selection"; TL r33–r37 say "Late July; before **final** selection". §6 requires the same date expression.
2. **Review references between mirrors, 3 rows** — TL r39 H = `R3,R5` vs OF r14 H = `R4,R5`; TL r46 H = `R4,R6` vs OF r16 H = `R1,R4,R6`; TL r48 H = `R4,R6` vs OF r17 H = `R1,R4,R6`.
3. **Visible prose asserts a bound its typed columns do not hold** — TL r42 B says "D/E notified **before 07/29**" but L/M/N are all blank; the 07/29 bound is unrecoverable by export. (TL r30 similarly states an exact 07/14 presentation date but stores it only as `date_upper`, leaving `reported_exact_date` empty.)
4. **`Review decisions!D` "Affected entries" is stale in both directions** — R1 declares `T03–T06, T17–T20, T33–T42` but T04, T20, T34, T35, T37, T38, T41, T42 do not cite R1, while T01 does and is not declared; R3 declares `T12–T20, T26–T36, T51` but T16–T19, T27–T32, T35, T51 do not cite it; R5 declares O01 and O16, neither of which cites R5; R6 declares T36/T38/T40/T42 which do not cite it and omits T46 which does; R7 declares "all sheets" and is cited by nothing.

`previous_observation_id` chain is clean — O07→O02, O09→O03, O10→O06, O11→O05, O12→O11, O13→O10, O14→O04, O15→O09, O16→O14; all backward, **no cycles** (C01's claim verified). `Sources!C` is a character-exact normalized reproduction of all 29 `BG-###` paragraphs of `background.txt`, with matching page labels (0 differences).

## 4. Conformance audit — violations

**§5 / §6 visible columns: pass.** All nine required Timeline columns (A–I) and all nine Offers columns (A–I) present, in order, 10 pt, wrapped, frozen at C6.

**§7 minimum technical fields — Timeline (J–V), missing:**
- **process/round key or number** — Stage is prose in C only; no typed key. (Prose is consistent and filterable; the violation is the missing typed key.)
- **participant identity links** — Participant is prose in D; no `party_id`. **There is no bidder-type field anywhere in either sheet.**
- **canonical offer link** — Offers→Timeline exists (OF K) but not the reverse.
- **event role**, **reported source wording**, **review state** — all absent.

**§7 — Offers (J–AG), missing:** **any date field** (date exists only as text in A; typed dates live on Timeline and must be joined via K); typed `bidder_id`; reported bindingness/document state; scope; typed condition/financing/diligence/exclusivity facts (prose only in E/F — the field Alex's I.10 and summary 2.G most want); typed review references.

**§7 event-specific facts — not typed anywhere:** deadline scope/replacement/expiry type (TL r17–r20, r31 prose only); admission destination; **exit agency/reason** (prose only — blocks summary 2.F); information change; decision-maker rationale; publicity type. Participant-count scope *is* typed (TL T/U/V).

**§8: pass.** `Review decisions!G6:G12` carries a real list validation `"Pending,Accepted,Corrected,Deferred"`; H reason, I reviewer/date present; all human cells blank (G pre-set "Pending", which §8 permits); AI adjudication change log present as a separate table (`DemoChanges` A17:K29, C01–C12).

**§9 violations:**
- **No `<autoFilter>` element on any of the 10 table definitions** (`xl/tables/table1–10.xml`). The tables exist and are sortable from the ribbon, but the filter dropdowns Excel normally shows are not pre-enabled.
- **Orphan data row outside its table**: `Deal guide!A60:B60` ("G&W July 26 additional version" = 1) sits below `ParticipationChecks` (A41:E58), separated by blank row 59.
- **Formulas inside a sortable table use plain cell addresses, not structured references**: `B44 =B42+B43`, `B47 =B45+B46`, `B49 =B47+B48`, `B54 =B53+B48`, `B57 =B55+B60`. Sorting the table breaks all five; B57 additionally points outside the table to the orphan row.
- **One hyperlink mis-targets**: `Timeline!G7` prints the quote "Following this presentation, the Board approved…" (which lives in `Sources!C7`, BG-001 · 2/2) but links to `Sources!A6` (BG-001 · 1/2). The other 194 of 195 links resolve to a row whose text contains the printed quote (all 8 spot-checks and the full 76-link sweep of Timeline/Offers evidence cells pass).
- **Frozen panes partial**: §9 asks for frozen date *and participant* columns; Timeline freezes A:B only — Participant (D) scrolls away. Offers freezes A:B, which does include Bidder.
- Merged cells: only title bands (A1:E1, A2:E3, A15:I15, A49:E49) — **compliant**. No "NA"/"N/A" strings anywhere (0 found). Prices stored as numbers with `0.00` format; Timeline L/M/N are real datetimes with `yyyy-mm-dd`. No macros, no external connections (file parts confirm). §10 "mirror values agree" fails on the three items in §3.
- §4 partial: `StageMap` (A16:E19) has only 5 columns; §4's per-phase fields (submission objective, admitted population, deadline history, announced-vs-inferred finality) are compressed into prose column C.

`Providence_Audit_Manifest.json` claims "source links and freeze-pane XML were verified" and `excel_gui_test: "Not performed"` — honest about the GUI, but the one mis-targeted link and the three mirror mismatches were not caught by the self-check.

## 5. Sortability / filterability

| Query | Feasible? | Blocking column |
|---|---|---|
| (i) all bids by strategic bidders | **Impossible from this workbook by filter.** Requires manual join to `Deal guide!B25:B30` prose ("Strategic · anonymous"). | **No `bidder_type` field on Offers or Timeline, visible or hidden.** The professor's P-sheet has it on every row (O/P/Q/R/S). |
| (ii) formal bids with heavy conditionality | Yes. Visible `Offers!D/E` begin with "Formal\n"/"Heavy\n", so a *begins-with* text filter works; clean equality filtering needs hidden `AB`/`AC`. | needs hidden columns for clean filtering |
| (iii) every round-2 event in date order | Filter yes (`Timeline!C` = "2 · Updated proposals"). **True date sort: no.** Sorting visible B sorts text ("Late July…" before "07/21/2016"); hidden L/M/N are three sparse columns (48%/41%/45% filled) with no single key. Sorting by A (Order) restores narrative, not date, order. | **no single sortable date key on Timeline** (representative date deliberately unused per §5) |
| (iv) each bidder's exit event and reason | **Not achievable.** Hidden `Timeline!K` filters `bidder_excluded` / `bidder_withdrew` / `bid_not_submitted`, but TL r42 bundles **four** bidders' exits into one row, TL r40 bundles two non-submitters, and Party E has no terminal exit row at all. Reason is prose in E/F. | merged multi-bidder rows + no `party_id` + no typed `exit_reason` |
| (v) days between round deadline and next board meeting | Only with hidden columns, and only if you know the convention. Deadlines are typed (`L`: 05/10, 05/19, 07/20); but meetings are bundled — TL r22 holds *two* meetings (M=05/23, N=06/01) and TL r38 holds two (M=07/22, N=07/27), so "next meeting" must be read out of `date_lower`. Arithmetic is possible; it is not a filter operation. | one-meeting-per-row granularity; no single date column |

## 6. Hidden-column inventory

**Timeline J–V (60 data rows)**

| Col | Name | Type | Fill | Professor equivalent |
|---|---|---|---|---|
| J | record_id | str | 100% | ~M BidderID (his is fractional: 0.3, 13.5, 17.5, 25.5, 28.3, 28.5) |
| K | event_code | str, 21 distinct | 100% | ~AC bid_note (11 labels) |
| L | reported_exact_date | date | 48% | AA bid_date_precise |
| M | date_lower | date | 41% | none |
| N | date_upper | date | 45% | none |
| O | date_basis | str, 17 distinct | 100% | none |
| P | source_ids | str | 100% | none |
| Q | after_record_id | str | 38% | none (implicit in M ordering) |
| R | order_basis | str, 3 distinct | 100% | none |
| S | source_document | str | 100% | ~K URL (deal-level) |
| T | unique_contact_count_contribution | int | 8% | none |
| U | new_NDA_count_contribution | int | 3% | none |
| V | count_scope_note | str | 15% | none |

**Offers J–AG (16 data rows)**

| Col | Name | Type | Fill | Professor equivalent |
|---|---|---|---|---|
| J/K | offer_id / timeline_id | str | 100% | none |
| L | round_number | int (1–3) | 100% | none (he has no round field at all) |
| M | observation_kind | str, 10 distinct | 100% | partly AC |
| N | previous_observation_id | str | 56% | none |
| O/P | price_origin / price_form | str | 100% | none |
| Q | point_per_share | num | 93% | T bid_value / U bid_value_pershare |
| R/S | individual_range_low/high | num | **0%** | V/W bid_value_lower/upper |
| T/U | group_envelope_low/high | num | 6% | he puts the envelope *into* V/W |
| V | fixed_cash_per_share | num | 18% | AG comment text only |
| W | stated_CVR_component | num | 12% | AG comment text only |
| X/Y | currency / share_basis | str | 100% | X bid_value_unit, Y multiplier |
| Z | settlement_medium | str, 3 distinct | 100% | none |
| AA | all_cash | int | 6% | AD all_cash (he fills it far more often) |
| AB | assessed_formality | str | 100% | Z bid_type |
| AC | assessed_conditionality | str, 3 distinct | 100% | **none** (AH free-text comments only) |
| AD/AE | individual_bid_eligible / submission-or-reaffirmation | bool | 100% | none |
| AF/AG | source_ids / source_document | str | 100% | none |
| — | *(no date field)* | — | — | AA/AB |
| — | *(no bidder type)* | — | — | **O/P/Q/R/S — present on every one of his rows** |

## 7. What must survive the flat-ledger redesign

1. **Evidence quote + printed page + native hyperlink into a Sources sheet that holds the full background verbatim.** 195 working internal links; `Sources!C` is character-exact against `background.txt`. His sheet has no evidence at all. This is the single biggest gain and directly serves summary pt 1 ("record the deal background link, including the page").
2. **The AI-reason column with explicit confidence and a named alternative** (`Timeline!F`, `Offers!D/E`) — the "unsure flag" the redesign wants already exists in usable form.
3. **Grouped review packets with human-only status** — 7 packets covering 76 flagged rows, with a validated `Pending/Accepted/Corrected/Deferred` dropdown, reason, reviewer/date, and an immutable AI baseline. Fixes summary pt 1's complaint that a single round-boundary error forces the human to re-edit every row.
4. **The AI adjudication change log** (C01–C12) citing the superseded cell by address, e.g. `Alex: deal_details!S6039/S6049`, `deal_details!AC6054/AG6054`. Keeps the "who changed what and on what filing basis" audit trail.
5. **Integer `Order` plus a stable record key**, replacing his fractional `BidderID` hack.
6. **Interval dating with `date_lower`/`date_upper`/`date_basis` and an explicit `order_basis` of `reported_sequence` vs `display_only`** — answers I.1, I.2 and I.9 head-on; his sheet can only hold two point dates.
7. **Contact / NDA / memorandum split with per-row count contributions and a visible 25-vs-≥26 conflict** (I.3, I.4, I.5).
8. **Deadline set / revised / scheduled as separate rows** (I.7, summary 2.B) and **execution split from public announcement** (I.15, summary 2.I).
9. **Price decomposition into package, fixed cash and CVR, with the group envelope kept out of the individual-range fields**, plus `previous_observation_id` chaining (verified acyclic) so a bid revision is traceable — the mechanism I.14 needs.

**And the three things the redesign must add back, which the demo loses:** a **bidder-type field on every row** (blocker for test (i)); **one row per event per bidder** so exits are not bundled (TL r40, r42 collapse six bidder exits into two rows — blocker for test (iv), and the reason his ledger answers the question by construction); and a **single sortable date key plus a typed round key on the event ledger** (blockers for (iii) and (v)). Also add typed `exit_reason` and `conditionality` (summary 2.F, 2.G), and reconsider whether IOI and bid need separate rows at all — summary 2.K asks this directly.

---

**Not checked:** quotes against the original `providence-worcester_2016-09-20_DEFM14A.htm` (only against `Sources`, which I did verify against `background.txt`); printed page-number accuracy; visual rendering in Excel (freeze panes, table styling, link behaviour and text clipping were verified from openpyxl and the raw XML only — no GUI test, same limitation the manifest declares); `Providence_Demo_Snapshot.json` cell-by-cell against the .xlsx; the 87 KB `SEC_Merger_Auction_Extraction_Instruction.md`, so §8's "keep all mandatory review categories from the base instruction" is unverified; the professor's codebook (`CollectionInstructions_Alex_2026.pdf`), so his `bid_note` label definitions are inferred from usage; and the other four run workbooks referenced in the change log.

---

# Corrections to the reports above

1. Report B recommends replacing the none/light/heavy conditionality flag with condition tags. Alex (voice note I.10) asks for the flag itself. Keep the flag and add a conditions column beside it.
2. Report B recommends hiding the "AI unsure" flag. Alex's summary items 2.A to 2.M are all about flagging. Keep it visible.
3. On all_cash with a CVR or earnout: Alex's stated rule (voice note V.5) treats it as cash plus a contingent payment, so all_cash = 1. Pro's demo leaves it blank. Follow Alex's rule and mark it as a convention.
