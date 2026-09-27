# Unblinded comparison of the five model/effort settings

Written after `01_blind_findings.md` was frozen and `administration/blind-key.json`, the run receipts, `check.json` reports, the GPT Pro review (`pro-review/`) and the research context (`ref/`, `lesson/`, the 25 September Questions for Alex) were opened. Nothing in the blind file was edited after unblinding; the two score revisions below are stated as revisions with their reasons.

## 1. Key

| Deal | A | B | C | D | E |
|---|---|---|---|---|---|
| Mac-Gray | Astra high | Opus 5.5 medium | Sol xhigh | Astra xhigh | Opus 5.5 xhigh |
| Providence & Worcester | Sol xhigh | Astra high | Astra xhigh | Opus 5.5 xhigh | Opus 5.5 medium |
| sTec | Opus 5.5 medium | Astra xhigh | Astra high | Opus 5.5 xhigh | Sol xhigh |

## 2. Scores by setting

Blind scores are exactly those in `01_blind_findings.md` §7. Revised scores apply two changes made after reading the Pro review and re-reading E10 and Part B; each is explained in §4 and touches rows I had already recorded as findings.

| Setting | Mac-Gray | P&W | sTec | Mean (blind) | Mean (revised) |
|---|---|---|---|---|---|
| Opus 5.5 medium | 9.5 (B) | 9.25 (E) | 9.75 → 9.0 (A) | **9.50** | **9.25** |
| Astra high | 9.75 (A) | 8.25 (B) | 8.75 → 9.0 (C) | 8.92 | 9.00 |
| Opus 5.5 xhigh | 9.25 → 8.5 (E) | 9.0 (D) | 8.5 → 8.0 (D) | 8.92 | 8.50 |
| Astra xhigh | 8.25 (D) | 8.25 (C) | 8.5 → 9.0 (B) | 8.33 | 8.50 |
| Sol xhigh | 8.25 (C) | 9.0 → 8.0 (A) | 8.5 → 7.75 (E) | 8.58 | 8.00 |

Denominators: one run per cell, three deals, fifteen workbooks; 15 ledgers with 1,024 rows read in full. **No workbook contained a material factual error** (wrong price, date, party, type or agreed term). The spread above is entirely convention handling, omissions of secondary rows, unsupported precision in a few cells, and padding. With one replicate per cell, a difference of a point or less between settings is not evidence of anything; the qualitative patterns in §5 are what the pilot supports.

`scores.csv` beside this file holds the per-workbook blind and revised scores with the deductions itemized.

## 3. Operational record (from receipts and `check.json`; not used for scoring)

| Setting | Elapsed (s) per deal MG / PW / ST | Continuations | Output tokens (MG / PW / ST) | Reported cost | Checker warnings (MG / PW / ST) |
|---|---|---|---|---|---|
| Opus 5.5 medium | 805 / 765 / 791 | 0 | 92k / 84k / 85k | $3.41 / $3.15 / $3.73 | 30 / 13 + 1 error / 18 |
| Opus 5.5 xhigh | 1,440 / 1,360 / 1,502 | 0 | 165k / 154k / 170k | $6.64 / $5.79 / $7.35 | 34 / 23 / 29 |
| Astra high | 801 / 799 / 787 | 0 | 23k / 23k / 23k (+6–7k reasoning) | not reported | 8 / 9 / 12 |
| Astra xhigh | 1,042 / 1,142 / 1,456 | 0 | 30k / 31k / 38k (+10–13k) | not reported | 8 / 10 / 3 |
| Sol xhigh | 563 / 734 / 869 | 0 | 26k / 33k / 40k (+10–17k) | not reported | 5 / 6 / 8 |

All fifteen runs completed inside the 120-minute allowance with exit code 0, no resumptions, no web or delegation tool calls and zero possible shell-network commands (`administration/outcomes.json`). `ISOLATION_PREFLIGHT.json` records the filesystem isolation of each environment. The Codex-side runs (Astra, Sol) report input tokens of 1.0–3.8 million per run, 87–93 % served from cache; Opus reports only output tokens and a dollar cost. Subscription costs for the Codex runs are not in the receipts and I do not estimate them.

Checker warnings are almost all `ledger.note_length` (Notes over 40 words). The Opus workbooks write longer Notes (mean 24–36 words, tails to 48) and so collect most of the warnings; that is style, not quality. The single checker **error** (P&W Opus medium, Rounds round 3) is a format mismatch: Due dates reads "none stated (G&W's own offer expiry, 6:00 p.m. 08/13/2016, is not a target due date)" rather than the exact string "none stated". The content is right.

## 4. Where I revised a blind score, and why

Two changes after unblinding, both traceable to findings already written in `01`:

1. **sTec, WDC's no-waiver ultimatum (20–23 June 2013, pp. 33–34).** Blind, I recorded Astra xhigh (B) and Astra high (C) as "aggressive" for typing it as an unpriced Bid, Formal, Heavy (H3), and did not penalize Opus medium (A), Opus xhigh (D) and Sol (E) for leaving it an Other material event. Re-reading E10 ("a same-price change to conditions … is its own Bid row"), E2 ("a change in … a bidder's commitments earns a row even when it was negotiated through drafts") and the R01 decision that v1.14 generalized, the Bid/H3 coding is the rule and the Other material event is the deviation. I moved 0.5 from B and C to A, D and E. This is the one place where the Pro review changed my reading of the instruction rather than my reading of the filing.
2. **Mac-Gray, Opus xhigh (E) #23.** Blind, I noted but did not deduct for Count = 16 on a "Did not submit by 07/23" row when the cohort's eligibility on 23 July is unproven. E14 requires "a bound where its size or a submitter's membership is uncertain" and Part B forbids an exact non-submitter count for a group not shown eligible as a whole. Opus medium (B) gave the bound; E did not. Deducted 0.5 as a single-row convention deviation. I also deducted 0.25 for E #34's Note ("range unchanged" when the range moved from $17–19 to $18–19), which Pro spotted and I had missed.

Three further deductions are additions, not reversals: Sol's P&W workbook (A) has two off-by-one cross-references (#33 "revises #25" for #26; #47 "after #39" for #43) and a Note asserting that BMO conveyed the competing **$25** figure to Party B when the filing says only "a revised LOI at a higher price" (p. 31); that last one misstates what a bidder was told, which Part A item 5 makes a research variable (−0.5, −0.25, −0.25). Astra high's sTec workbook (C) places Company G among the "nine uninterested" parties without support (−0.25). Sol's sTec workbook (E) codes Company D's 23 April diligence "Not stated" although the filing reports D "detailed their additional diligence requirements" (−0.25), and neither Opus medium nor Sol recovered the 2009 date of the underlying WDC NDA from Annex A-3 (−0.25 each).

## 5. What the pilot supports about the settings

**Every setting produced a research-usable ledger for every deal.** The worst workbook (Sol on sTec, 7.75 revised) needs about six cell-level corrections and one row retyped; the best (Astra high on Mac-Gray, Opus medium on Mac-Gray, Opus medium on P&W) need one or two Question resolutions and nothing else. Nobody invented a bid, a party, a price, a date or a quotation. The 2026-08 voice-note failure modes (duplicated NDAs, invented dropouts, missing contact events, execution/announcement conflated, winner type missing, IOI and bid as two rows) are absent from all fifteen.

**Opus 5.5 medium was the most consistent setting.** Its three workbooks (9.5, 9.25, 9.0 revised) each sit on the consensus map, apply E14's first transition with an honest bound, treat Party B's options as a CVR, record the differential information access, keep Company H in reserve, and flag every debatable call. Its only deductions are a pedantic 47–48 contact residual, a missing 22–23 March Party A meeting row, the sTec ultimatum typing, and a pre-process adviser row shared by every setting. It also ran in about 13 minutes at $3.2–3.7 per deal.

**Astra high was the best single workbook and the least consistent setting.** On Mac-Gray it produced the cleanest ledger of the fifteen (9.75): the 27 August closure of the anonymous residual, financing carried into Party A's reiteration, the sponsor-liability revisions as unpriced Bid rows with prices blank, three buyer advisers recovered from Annex A. On P&W it mislabelled the sixteen-plus non-IOI signers "Dropped by target" (E14's first transition, Did not submit, applies because the filing says every potential buyer was advised to submit), gave a 16–24 range that admits IOIs from non-signers the filing never suggests, added two post-signing rows E2 excludes, and omitted the 22–23 March Party A meeting (8.25). On sTec it was very good (9.0) with one unsupported cohort assignment.

**Extra effort did not buy accuracy in this pilot.** Opus xhigh scored below Opus medium on all three deals (blind and revised) while taking 1.8 times as long and costing about twice as much. Its extra output went into more rows (74 on Mac-Gray, with duplicated admission and inferred contact rows), longer Notes, and, on sTec, an inferred third round that E6 does not support and that changes the round of WDC's two June bids. Astra xhigh scored below Astra high on Mac-Gray (the residual closed at 11 September, one stage later than the 27 August letter supports; an oral cap proposal coded Formal) and on P&W (the same residual mislabel as Astra high, plus a Party B contact row missing), and above it only on sTec, where the two are within a quarter point. The Pro review reached the same qualitative conclusion on effort ("Opus xhigh scores below Opus medium on each of these three cases"; Astra xhigh "does not improve the first two cases").

**Sol xhigh was the fastest (9–14 minutes) and the least careful with small facts.** Its ledgers are lean and structurally right, but it carries the only three unsupported Note claims in the fifteen (P&W: two wrong row references and the "$25 conveyed" assertion), an unflagged Heavy (H2) on Mac-Gray's 9 September CSC bid, a Regulatory = Concern with Antitrust blank, a missing exclusivity-request row, a Question that denies a two-month gap that exists, an unsupported "Terms or process" exit reason for WDC, and the partial-only reading of sTec's E and F that departs from the convention the other four applied. None of these is a wrong price or date; all are the kind of thing a reviewer must catch cell by cell.

**Row count and Note length are not quality.** The three longest ledgers (sTec Astra xhigh 86 rows; Mac-Gray Astra xhigh 74; sTec Astra high 74) and the three shortest (P&W Sol 60; P&W Opus medium 63; Mac-Gray Opus medium and Sol 64) are spread across the score range. Padding (inferred Contact rows that repeat NDA rows, duplicate adviser rows, admission rows duplicating Round opened) appears in Astra xhigh and Opus xhigh more than elsewhere.

## 6. Agreement and disagreement with the GPT Pro review

Pro's ranking (Astra high 93.3 > Astra xhigh 91.3 > Sol = Opus medium 85.0 > Opus xhigh 80.7) and mine (Opus medium 9.25 > Astra high 9.0 > Opus xhigh = Astra xhigh 8.5 > Sol 8.0) agree on: Mac-Gray Astra high as the best workbook; both xhigh settings failing to beat their cheaper counterparts; the same set of "gray zones" (residual cohort closure, later-passage condition states, unpriced commitment revisions, E/F scope, the extra sTec round); and the finding that nothing material was fabricated. We disagree on three convention calls, and those calls drive the rank difference:

1. **Mac-Gray's sixteen anonymous financial signers.** Pro treats "Did not submit by 23 July" as a "substantive participation error" and scores Opus medium 82 and Opus xhigh 80 largely on it. I read E14 as making Did not submit the first transition for parties the filing says were instructed to submit by 23 July (p. 32: every party furnished the package "were instructed to submit by July 23"), with the eligibility doubt handled by a bound; Opus medium gave the bound (Count blank, "up to 16"), so I do not penalize it; Opus xhigh gave an exact 16, which I now penalize once. Pro's preferred closure (27 August, Astra high and Sol) is equally an inference; the instruction, not the extractor, is what leaves three transitions available. This is decision R1 in `03`.
2. **P&W's sixteen-plus non-IOI signers.** Pro rewards Astra high's "Dropped by target … 16–24" as "the strongest treatment of uncertainty" and penalizes Sol, Opus xhigh and Opus medium for "Did not submit … although eligibility not established". Here the filing does establish eligibility ("each potential buyer had been advised to submit a non-binding indication of interest by May 10", p. 29), so Did not submit is E14's first transition and the correct label; the uncertainty is about the count (at least 16), which Sol, Opus xhigh and Opus medium all expressed as a bound. Pro did not address the label. I also do not think 16–24 is an honest bound: the nine IOIs came from parties with the memorandum, which only NDA signers had.
3. **P&W Opus xhigh.** Pro scores it lowest of the fifteen (78) for separate G&W and Party B NDA entries beside the 11-strategic cohort, for "Not begun" diligence on the IOIs, for Party E's Heavy (H2), and for Regulatory Concern on G&W's 12 August bid. I recorded all four; the first is a literal application of E3 ("belongs to an earlier cohort only if the filing establishes it") with both readings disclosed in Q3; the others are permitted readings, each flagged with its alternative. I deducted 0.5 for the double-count risk and 0.25 for the Light call; Pro deducted roughly twenty points. Reasonable graders can weigh flagged ambiguity differently, but a workbook that states both readings and their row effects is easier to repair than one that silently picks one.

Pro's report is careful and its per-row citations checked out wherever I tested them. Its main contribution over my blind pass is the E10 reading of the sTec ultimatum, which I adopted, and four small factual slips it caught (Sol's cross-references and "$25", Opus xhigh's "range unchanged", Astra high's Company G). Its main weakness is treating one side of an open E14 question as settled and grading fifteen workbooks against it.

## 7. Cross-deal consistency of each setting on the eleven ambiguity points

Read down a column to see whether a setting applied the same rule across deals. "—" means the point did not arise.

| Point | Opus medium | Opus xhigh | Astra high | Astra xhigh | Sol xhigh |
|---|---|---|---|---|---|
| Residual cohort closure: label / date (MG; PW) | Did not submit at due date, bound (MG, PW) | Did not submit at due date, exact 16 (MG); Did not submit, bound (PW) | Dropped by target at advancement (MG 8/27; PW 6/1) | Dropped by target at advancement (MG 9/11; PW 6/1) | Dropped by target 8/27 (MG); Did not submit, bound (PW) |
| Later-passage financing inference (MG Party B 9/18) | Contingent, Inferred = Y | Contingent, not marked | Not stated | Not stated | Not stated |
| H2 from "in-depth"/"60-day for diligence" (MG 9/9; PW Party E) | Unclear; Unclear | Heavy; Heavy | Unclear; Unclear | Unclear; Unclear | Heavy; Unclear |
| Light from later "confirmatory" (MG 9/18–9/23; PW B 8/4, G&W 8/12) | Light (9/21–23); Unclear (PW) | Light (MG); Light (PW B, G&W) | Unclear (MG); Unclear (PW) | Light (MG 10/5) / Unclear; Unclear (PW) | Unclear; Unclear |
| Regulatory Concern from reverse fee / STB comparison | Not stated; Concern (PW) | Concern + Antitrust Y; Concern | Not stated; Not stated | Concern, Antitrust blank (MG); Not stated (PW) | Concern, Antitrust blank; Not stated |
| Sponsor-liability revisions as Bid rows with price (MG 10/5, 10/8) | Bid, price carried | Bid, price carried, Inferred | Bid, price blank | Bid, price blank | Bid (10/5, 10/8) + Bid reaffirmed 10/7, price blank |
| Ultimatum as Bid/H3 (ST) | No (OME) | No (OME) | Yes | Yes | No (OME) |
| Formality of 9/21 "last and best" (MG) | Formal | Formal | Formal | Formal | Informal |
| Round map | Consensus | Consensus (MG, PW); extra round 3 (ST) | Consensus | Consensus | Consensus |
| sTec E and F | Entrants, Withdrew | Entrants, Withdrew | Entrants, Withdrew | Entrants, Withdrew | Partial-only |
| Company H exit (ST) | Not selected at signing, Would not improve | Same | Same | Same | Not selected at signing, Not stated |

Opus medium and Astra high are each internally consistent across their three deals on every point but one (Astra high's Sol-like closure on Mac-Gray versus its P&W label, both "Dropped by target" but for different transitions). Astra xhigh is consistent except on H2/Light. Opus xhigh is consistent but more willing to infer states from later passages and to add structure (the third round). Sol is the least consistent setting across deals (H2 Heavy on Mac-Gray, Unclear on P&W; Concern on Mac-Gray, Not stated on P&W).

## 8. Recommendation on model and effort for this workflow

For extraction runs under v1.14 as written, keep **Opus 5.5 medium as the default**: best mean score on this pilot, most consistent across deals, cheapest and fastest of the Claude settings, and the setting whose remaining defects are Question-level rather than cell-level. **Astra high is a good second extractor** for the deals Austin and Alex want double-coded; on the evidence here it is at least as careful on the source and sometimes cleaner, but it applies E14's residual closure differently and once labelled a cohort's exit wrongly, so its output needs the same convention review. **Neither xhigh setting earned its cost or time**: on this pilot both produced more rows and more inference, not fewer errors. **Sol xhigh** is fast and structurally sound but was the only setting with unsupported Note claims and should not be a sole extractor.

These are pilot observations from one run per cell on three deals chosen because they exercise the instruction's hard cases; they are not estimates of model-wide accuracy, and the ranking between Opus medium and Astra high could flip on a different draw of three deals.
