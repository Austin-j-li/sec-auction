# A2: replacement Questions for Alex (V114_SPEC D19, §5)

## Updated after the v1.14.1 retest (26 September 2026, about 20:45 UTC)

**Status: rebuilt locally, not sent.** Nothing goes to Alex without Austin (GATE). This supersedes the status and "Outstanding" list of the next section.

| | |
|---|---|
| File | `../../Questions_for_Alex_2026-09-25.docx` (same name; byline 26 September 2026) |
| SHA-256 | `76b9c6359ce3560d8940d0fa98e21560295c82a361b20b143e534bdfe6586e84` |
| Size and words | 51,732 bytes; 5,198 words (3,091 in parts 1–3, 2,107 in the appendix) |
| Rendering | 12 pages (`page-01.png` … `page-12.png`, `page.pdf`), built and rendered with the commands below |
| Builder | `build_docx.py`, SHA-256 `1ee0c804…df1c`; 61 excerpts in 19 cases, all found on their cited pages |
| Before this change | `pre-retest/`: the 26 September afternoon DOCX (`f201a70e…243a`) and builder (`a53fda3f…0b96`); its page renders were overwritten |

What changed:
- **3.3(a) recomputed** from the v1.14.1 retest workbooks ([retest](../../../../reviews/2026-09-26-v1141-retest/README.md); Opus 5.5 medium, published v1.14.1 `8a93df3c…6c98`). `derive_analysis.py` 0.3 `--rules v1.14.1` on the Mac-Gray and P&W versions, then `compare_alex.align` against Alex's labels as stored in `../../analysis/compare-alex-*/alex_bids.csv` (not re-read from `ref/`). Script and outputs: `../../../../reviews/2026-09-26-v1141-retest/analysis/formality_agreement.py`, `.json`, `.csv`. The same script logic on the two 24 September pilots reproduces the old table exactly. All 13 and 14 labelled bids aligned.

  | Reading | Mac-Gray, of 13 (trial) | P&W, of 14 (trial) |
  |---|---|---|
  | T0 | 13 (13) | 11 (11) |
  | T1 | 11 (11) | 12 (14) |
  | T1u | 9 (11) | 12 (13) |
  | T2 | 12 (12) | 11 (11) |
  | T3 | 13 (13) | 12 (11) |

  Mac-Gray T1u falls because CSC/Pamplona's 18 and 21 September bids are now Unclear (silent diligence), not Light. P&W: Party D's 1 August bid is now Informal (agrees); G&W's 21 July bid is Formal, Unclear (Alex Informal) and its 26 July bid Informal (Alex Formal, 2b item 5); Party B's 20 July bid is in a round that is not final, so T3 reads it Informal (Alex Formal). The commentary under the table says so; the `RETEST_PENDING` marker is gone.
- **Datalink (3.1): decided.** Austin decided on 26 September that Datalink follows the v1.14.1 text: four rounds (map A), superseding F9's five. Round 1 opens 28 January (first price negotiation), not F9's 29 January, as the retest extraction also has. Kraton is shown as following the same text (map A, two rounds). The answer box asks only sTec to circle a map, and takes comments on Kraton and Datalink.
- **Published wording (the eight changes, `8a93df3c…`):** 2b item 3 (Rounds) adds "A selection that asks for no offers opens no round; the round opens at the request that follows", and its "Changed?" cell says so; 2a Same offer adds that the copied price is not a new price observation. The other six changes (Count on Round opened, inferred Round opened, Initiation, diligence "only documentation remains", CVR value, the "Process:" prefix and cohort Who) touch no rule the questionnaire quotes.

Still open: sending the document (GATE, Austin).

## Reconciled with v1.14.1 (26 September 2026)

**Status (historical; see above): rebuilt locally, not sent.** Nothing goes to Alex without Austin (GATE). The document was reconciled with the v1.14.1 candidate (`8bdb7c20…8a79`) under `../../../2026-09-26-v1141-streamline/PIPELINE_UPGRADE_SPEC.md` WP8.1 and `V1141_SPEC.md` §10 step 8. The sections below this one describe the 25 September build and are kept as history.

| | |
|---|---|
| File | `../../Questions_for_Alex_2026-09-25.docx` (same name, so existing links hold; the byline now reads 26 September 2026) |
| SHA-256 | `f201a70ef900b952b3c0e501375ce8552e0b938ea9869f0b28a48c3519f0243a` |
| Size and words | 51,576 bytes; 5,091 words (2,984 in parts 1–3, 2,107 in the appendix), by the count described below |
| Rendering | 11 pages (`page-01.png` … `page-11.png`, `page.pdf`) |
| Builder | `build_docx.py`, SHA-256 `a53fda3f…0b96`; 61 excerpts in 19 cases, all found on their cited pages |
| Before this change | `pre-v1141/`: the 25 September DOCX (`Questions_for_Alex_2026-09-25-pre-v1141.docx`, `64ddad6c…4353`), its builder (`65b1681d…1937`), `page.pdf` and the ten page PNGs |

Built as before, except that Chrome needs a short `TMPDIR` (a long one fails with "Socket path too long"):

```
export TMPDIR=/home/uctpiaj/work/tmp/a2v1141 PYTHONDONTWRITEBYTECODE=1; mkdir -p "$TMPDIR"
V=/home/uctpiaj/work/tmp/v114-scratch/tmp/a2/venv/bin/python
$V build_docx.py --out ../../Questions_for_Alex_2026-09-25.docx --date 2026-09-26
$V render.py ../../Questions_for_Alex_2026-09-25.docx . --prefix page
```

A rebuild with the same `--date` reproduced `word/document.xml`, `styles.xml`, `footer1.xml` and `docProps/core.xml` byte for byte. No D-number or "Decision n" appears outside the small reference style. V1141_SPEC's own D1 and D6 are written "v1.14.1 D1" and "v1.14.1 D6" so they do not collide with V114_SPEC's D-numbers. Numbering (2a rows, 2b items 1–8, 3.1–3.5, C1–C19) and the D-number crosswalk are kept.

**What changed, item by item** (builder text in `DECIDED`, `PROVISIONAL` and `build()`):

| Item | Change |
|---|---|
| Title, part 1 | v1.14 → v1.14.1 |
| 2a Exclusivity | H2 counts only a period of two weeks or more tied to diligence alone (R4); a period that also covers exclusivity or negotiation does not |
| 2a Carried terms | Now **Same offer** (R1), marked Changed. Case: Mac-Gray Party A's 18 September reiteration copies its uncommitted financing (Heavy) and is Formal by the final request. WDC 10 June and Meredith Party B 20 April are revisions with a new price and are not copied |
| 2a Commitment changes | Adds "price blank, not a new price observation" (H4) |
| 2b-2 Partial bidders | The Question on weighing partial offers is gone (E1); a switch is "Withdrew, continued on a partial basis" (Synacor Company E, 14 December 2020) |
| 2b-3 Rounds | The four listed triggers; "after a suspension" becomes 30 days or an ended exclusivity (E6(d)); the count-once sentence is gone. Synacor 27 October follows Company E's exclusivity expiring on 23 October (p. 34) |
| 2b-4 Merger of equals | The Question is gone; the counterparty stays outside unless the filing reports a sale to it |
| 2b-5 Formality | The reference-back route is gone. WDC's 10 June bid is Informal, matching Alex's coding; G&W's 26 July bid stays Informal |
| 2b-6 Conditions | R2 window with forecasts (Q4): Mac-Gray Party B's 18 September package is Financing Contingent and Heavy (H1) from the committee's 19 September "would likely be financing" remark (p. 37) |
| 2b-7 Missed due dates | The miss is its own dated event (E14 makes it an Other material event row). Not in the WP8.1 list; changed for accuracy |
| 2b-8 Deadlines | The five-value ladder; PetSmart rechecked (below) |
| 3.1 | Kraton and Datalink options re-derived (below); sTec map B has no v1.14.1 trigger |
| 3.2 | An FYI that the ledger records no ranges; the question is only how estimation uses the counts. Examples reworded: Datalink 13, Mac-Gray 16 |
| 3.3(a) | Numbers kept and marked "to be recomputed after the v1.14.1 retest" (`RETEST_PENDING` in the builder). Commentary: Party B is now H1 under 2b-6 (Q4); Party A copies its financing under 2a; committed financing with silent diligence is now Unclear, not Light (V1141_SPEC D3), which can move bids between T1 and T1u |
| 3.3(b) | Removed as a question; an FYI note keeps the letter: settled by Austin as option B (H4) |
| 3.3(c) | Mac-Gray example reworded to the settled coding (16, by 23 July) |
| 3.4 | Company H is an FYI: dropped by the target by 16 May, reason "would not improve earlier offer" (H1 of the root handoff). Penford Party A: 4 and 13 October are valuation statements, 14 October its bid, no Question |
| C1 | Retitled "Mac-Gray, Parties A and B, 2013"; two excerpts added for Party A (pp. 35 and 36), both checked against the filing |

**Re-derived, and on what evidence.**
- **Kraton (3.1).** v1.14.1's trigger (a) needs the target to select bidders *and* ask them for offers; the 20 July admission asked for none (p. 36, C15), and the first request was the final bid procedures letter after 11 August (p. 37). With count-once gone, the maps differ only on whether an offer-less selection is a round of its own. A (selection and letter one round: two rounds) stays **recommended**: under B round 2 would hold no request, due date or bid, against E6's definition of a round. E9 outcomes are unchanged under the new ladder (29 June Extended; 19 July Enforced; 15 September Extended (late bid accepted), Party A's 17 September bid considered, p. 39). 6 July stays in round 1 ("asking the round's bidders to improve … continues the round"). Source: `MAP_RECHECK.md` Kraton §2 and the filing excerpts in C15.
- **Datalink (3.1).** Same reading: the 27 July selection asked for nothing until the 16 August letter (p. 29, C16), so the triggers give A (four rounds). June is a round under E6(d): more than 30 days passed after the mid-March request and Party A's April proposals with no request (`MAP_RECHECK.md` Datalink §1–2). 1 October is a round under E6(d), after Insight's exclusivity lapsed (p. 32). No "recommended" mark: Austin's F9 ruling ("keep five rounds") stands until he decides, so the note says A is what the triggers give. **This is a decision for Austin before sending** (see below).
- **PetSmart (2b-8).** Under the five-value ladder, 30 October is **Enforced** without condition: no later due date was set (rule 1); Bidder 2's raise revised an on-time IOI, so no required response arrived late (rule 2); after the date J.P. Morgan heard the parties' rationales (30 October–2 November) and the board selected four bidders on 3 November (rule 3; p. 24, C14). The earlier "Unclear on reading B" turned on D11's "invited afterwards" wording, which v1.14.1 dropped. Q7-A's prediction (both Enforced) now holds outright. Source: `MAP_RECHECK.md` PetSmart §2 and C14.
- **Datalink count (3.2).** 10 strategic and 13 financial signers (p. 28); nine July IOIs, four strategic besides Party A (including Insight and Party B) and five financial (including Party C) (p. 29). Non-bidding signers: 23 − (A, B, C, Insight) − 6 other bidders = 13, the lower end of the old 13–16 range and `MAP_RECHECK.md`'s base rows #29 (5) and #33 (8).

**Outstanding.**
- 3.3(a): recompute the agreement table from the v1.14.1 retest workbooks (PIPELINE_UPGRADE_SPEC WP3 item 8), then remove the `RETEST_PENDING` marker. The retest has not been run (GATE).
- Datalink 3.1: Austin decides whether v1.14.1's four-round map replaces F9's five rounds, or whether the offer-less 27 July selection opens its own round. The retest's Datalink run (V1141_SPEC §10 step 6) will show which map the text produces.
- Datalink round 1: v1.14.1 opens a round where buyers came to the target "at the first NDA or price negotiation" with a whole-company bidder. That is the 28 January price reply (p. 27) or the 4 February NDA, not F9's inferred 29 January. The document keeps F9's date; Austin may want to confirm it.
- Sending the document (GATE).

25 September 2026. Local deliverable only: nothing was uploaded, sent or shared, and Alex was not contacted. Sending it is Austin's action (§13 gate 8).

## The document

| | |
|---|---|
| File | `../../Questions_for_Alex_2026-09-25.docx` (in the maintenance folder; the name carries the UTC date of the build) |
| SHA-256 | `64ddad6cdb5935a62510157c42dd7e31bd5356f3dfd091a6307436ef6a3b4353` |
| Size | 50,720 bytes |
| Word count | 4,559: 2,541 in parts 1–3 (title and byline included) and 2,018 in the case appendix (part 4). Counted as the words of every paragraph in the body, table cells included; a merged cell counts once; a line break counts as a space. `mammoth.extract_raw_text` gives 4,552, because it joins the words on either side of a line break. |
| Pages | 10 US Letter pages in the rendering below (parts 1–3 end on page 7); Word's count may differ |
| Replaces | `lesson/independent-audit-2026-09-23/questions-for-alex/Open_Questions_for_Alex_2026-09-24.docx`, SHA-256 `faab1d66…5220`. It is unchanged: its hash was the same before and after this work. |

This is the condensed version (see "Condensed" below), corrected after an independent review (see "Fixes after the review of the condensed version"). The verified version it condenses, SHA-256 `31e6909b…099a` (6,013 words, 12 rendered pages), is kept read-only with its README in `/home/uctpiaj/work/tmp/v114-scratch/a2-pre-condense/`.

The content follows §5:
1. **What changed**: one paragraph, and how to answer.
2. **2a. Decided, for information**: one table of five rows (D4, D14, D15, express incorporation, D13), each with the rule, a case with its page and a "Changed?" cell, and one comment box.
3. **2b. Provisional: yes or no**: one table of eight rows (D5, D7, D8, D17, D9, the conditions half of Q5, D10, D11), each with the rule, a case with its page, a "Changed?" cell and Yes/No to circle, followed by its own shaded comment row. A one-line note records that the regulatory rule confirmed on 24 September stands (D3).
4. **Open decisions**:
   - 3.1: Decision 1, with the Kraton, Datalink and sTec maps from `MAP_RECHECK.md`;
   - 3.2: Q1 / Decision 3, keeping Q1's options;
   - 3.3: Decision 3b: T0–T3 (and T1u) in one table with the side-by-side counts, same-price revisions and inferred exits;
   - 3.4: the readings still open (sTec Company H; Penford Party A);
   - 3.5: the source hierarchy.
5. **Case appendix**: C1–C19, 59 exact excerpts with printed pages (88 fragments between ellipses).

A D-number appears only as a small grey reference (the Word character style `Reference`, 7.5 pt). A script check found no D-number or "Decision n" outside that style.

## How it was built

```
export TMPDIR=/home/uctpiaj/work/tmp/v114-scratch/tmp/a2c PYTHONDONTWRITEBYTECODE=1
V=/home/uctpiaj/work/tmp/v114-scratch/tmp/a2/venv/bin/python   # python-docx 1.2.0, mammoth 1.12.2
$V build_docx.py --out ../../Questions_for_Alex_2026-09-25.docx --date 2026-09-25
$V render.py ../../Questions_for_Alex_2026-09-25.docx . --prefix page
```

- `build_docx.py` (SHA-256 `65b1681d…1937`) holds all the text and writes the DOCX. Its layout follows the 24 September document: US Letter, Georgia, navy headings and shaded answer boxes. It prints the word count as whole document, parts 1–3 and appendix.
- **Excerpt check.** Before writing, the build checks every excerpt against the filing in `raw_filing/`. The filings are read only; their hashes are in `raw_filing/MANIFEST.csv`. Each quoted fragment (fragments are split at " … ") must appear, after whitespace is normalized, in the text of the printed page or pages the appendix cites. A page label printed twice in a filing is refused as ambiguous. All 59 excerpts passed. A negative test on a copy of the final script (one fragment moved to the wrong page, one word altered in the restored Datalink letter) failed on both, as it should.
- **Reproducibility.** A rebuild with the same `--date` reproduces `word/document.xml`, `styles.xml`, `footer1.xml` and `docProps/core.xml` byte for byte. The DOCX hash differs between builds only because of the zip entry timestamps. The script in this folder is the one that made the delivered file.
- **Table XML.** Table and cell properties are written in schema order, which Word expects; a script check of all 15 tables found no out-of-order or duplicated `tblPr`/`tcPr` children. Table rows cannot split across pages; the 2b header row repeats on each page, and every paragraph of a 2b item row keeps with the next, so an item stays with its comment row. The other tables are short and are kept on one page the same way.
- **Page labels.** A non-breaking space follows "p." and "pp." everywhere outside quoted filing text, so a page number never starts a new line. A script check found no page label with a breaking space and no non-breaking space inside a quotation.

## Rendering, and its limits

`render.py` (SHA-256 `cb8910af…2855`) converts the DOCX in three steps:
1. mammoth, with a style map, turns it into HTML;
2. headless Chrome (Chrome for Testing 153) prints the HTML to `page.pdf`;
3. pdftoppm 24.02 turns the PDF into `page-01.png` … `page-10.png` at 80 dpi.

Its column widths now match the condensed tables (the five-column 2b table and the four-column readings table). Its CSS keeps a 2b item row with the comment row under it and keeps the short tables on one page; an older rule that kept any table with a merged cell unbroken pushed the whole 2b table to a new page and was replaced. I looked at all ten page images after the review fixes, and earlier at the nine of the first condensed build, and fixed what they showed: the 2b "Changed?" column was too narrow (widths rebalanced to 0.3, 2.55, 1.95, 1.35 and 0.55 inches), and answer options ran together on one line (each option is now on its own line). The notes above an answer box, and each case's excerpts but the last, are set to keep with the next paragraph, so in Word a question stays with its box and a case stays on one page.

**This rendering approximates Word's; it is not Word's.** Neither Word nor LibreOffice is installed on this machine, so the DOCX was not opened in Word.
- Mammoth drops Word's fonts, shading, column widths, row heights, paragraph alignment and empty paragraphs. `render.py` restores the main ones in CSS, keyed to the tables' header cells. In the rendering the Yes and No of 2b sit on adjacent lines; in Word an empty line separates them.
- Georgia is not installed. The rendering uses Gelasio, a metric-compatible substitute.
- Chrome does not apply Word's keep-with-next. In the rendering the 3.3(a) question sits at the foot of page 5 with its table on page 6, and C4, C12 and C16 each break across two pages; Word keeps these together. Page breaks, and so the page count, will differ in Word.

## Condensed (25 September)

§5 says "Keep it short". The verified version ran to 6,016 words by this count (3,541 in parts 1–3, 2,475 in the appendix). The first condensed build had 4,080 (2,494 and 1,586; 9 rendered pages; SHA-256 `081f8ee9…6441`). After the review fixes below it has 4,559 (2,541 and 2,018): against the verified version, parts 1–3 are 28% shorter, the appendix 18%, the whole 24%; the rendering fell from 12 pages to 10.

An earlier condensing pass was interrupted after editing the script and before rebuilding. Its edits were checked against the verified DOCX and kept where sound; where the compression changed a meaning they were redone:
- a revised bid's carried terms now name the reaffirmed bid too;
- D5 again names the bid it covers (one stated to have no financing condition);
- D13 says the change is to the bidder's commitments, so a target's change is not caught;
- D8 again dates a reopened round at the outreach, not the board's authorization (a point the review had asked for);
- WDC's 10 June bid refers back to 28 May terms that came with a markup, not to the markup itself;
- inferred exits are "recorded as" not submitting, not stated as fact;
- PetSmart's Bidder 2 excerpt again says the raise came "As a result of its discussions with J.P. Morgan", which bears on whether it was invited;
- the Company H excerpt again names BofA Merrill Lynch as the party that told H its range was not enough.

What was condensed:
- **Layout.** 2b is one table with a Yes/No column and a comment row under each item, instead of eight separate tables. The readings T0–T3 and T1u are defined in the side-by-side table, not in a separate list. Column headers are "Case" and "Changed?".
- **One sentence per rule.** Each rule in 2a and 2b is one sentence, keeping its conditions and exceptions.
- **No repetition between tables and appendix.** A case cell gives the case, the coding it gets, the printed page and the excerpt number; the filing facts behind it are left to the excerpt (for example Company E's request "until October 23, 2020", CSC/Pamplona's $15 million reverse fee, WDC's "terms previously proposed", Company H's feedback and Penford's quoted ranges). Two facts that were stated twice in parts 1–3 are now stated once, with a pointer: sTec's 30 May outcome against your coding (3.1, pointed to from 2b item 8), and the sTec example of the source question (3.5 points to 3.1).
- **Appendix excerpts cut to the operative sentence**, with " … " where words are cut. Where a cut removed the date from an excerpt, the label now gives it (for example "p. 35; 9 September"; "p. 24; 30 October to 2 November"), taken from the words the earlier excerpt quoted. The filing names are listed once at the top of the appendix instead of under each case, and case titles are "deal, party or topic, year".
- **Wording.** Part 1 and the notes under the maps were tightened; the 2b intro sentence was folded into part 1.

**Check that no fact, number, page or quotation changed.** A script (`/home/uctpiaj/work/tmp/v114-scratch/tmp/a2c/work/factcheck.py`) compared the condensed DOCX with the verified one:
- every number in the condensed text (prices, counts, dates, percentages, pages) occurs in the verified text;
- every quotation in parts 1–3 occurs verbatim in the verified text;
- every page citation in parts 1–3, with its excerpt number, occurs in the verified parts 1–3;
- every appendix fragment occurs in the verified excerpts of the same case, under the same page label.

On the final build it checked 88 fragments and reported no problems. Three fragments were added on purpose after the review; they are listed by name in the script and reported separately, and the build checks them against the filing (see below). On a copy with planted changes (a number, a page citation, a word in a quotation of Alex, a word in an excerpt) it reported all of them. The rules were also read against the verified text one by one. The script shows that surviving words are unchanged, not that operative words survived; that was checked by reading every excerpt against the claims it supports (see the fixes below).

**What the verified version said that the condensed one does not**, beyond the filing facts left to the appendix:
- the reason for provisional answers ("so that v1.14 need not wait");
- 3.3(a)'s sentence on why conditions are kept apart from Formality (T1 is defined in the table);
- in 3.3, that option B "records a change of terms only" and that under censoring "the bidder is no longer observed";
- in 3.4, "(not H's own withdrawal)", which the contrast with your coding ("H's own drop") still carries;
- the fuller voice-note quotation on sTec (the operative words, “this is not the final round”, are kept);
- appendix words outside the operative sentence, including G&W's $21.02 cash and $1.13 CVR split and the feedback that preceded it, Party B's $18.50 of 9 September, Meredith's earlier $2.3 billion, Parent's $46.00 and $46.50 offers and its note on diligence, Pamplona "committing to fund 100% of the capital", Mr. Malkoski's reply to Ingredion, and Kraton's 8 September markup date (not a deadline). None was cited in parts 1–3.

**Length against the target.** The target was parts 1–3 at about 2,000–2,400 words and the whole at about 4,000 or less. The first condensed build was about 4% and 2% over. The review fixes put accuracy first and added words: parts 1–3 are now 2,541 (6% over the band) and the whole 4,559 (14% over), most of the growth being operative words restored to the excerpts. Austin could cut about 130 words from parts 1–3 by dropping facts that §5 does not require: the regulatory note under 2b (20 words); the two "On 24 September …" comparisons in 3.4 (24); "A's prediction (both Enforced) holds, for PetSmart on the first reading" (12); the sentence on where your notes start Datalink's round 1 (17); the reason clause in the Kraton note (10); and the list of differing bids under the side-by-side table (about 45).

## Fixes after the review of the condensed version (25 September)

An independent review of the first condensed build (`081f8ee9…6441`) found no blockers, two major and eight minor defects. All ten are fixed in `build_docx.py`:
1. **C16, the Datalink letter (major).** "relating to their final proposals" is restored: "On August 16, 2016, Raymond James provided each of Insight, Party B and Party C with an instruction letter relating to their final proposals. … submit its proposal by 5:00 p.m. Eastern time on August 30, 2016" (p. 29). It is the only filing support for the letter being the first final request in 3.1.
2. **2b item 7, missed due dates (major).** "only a note" is replaced by the candidate's rule as the verified version put it: the bidder "gets no exit and no re-entry; the miss is noted. “Did not submit” is used only where participation ends." (The candidate records the miss in the Deadline row's Note and the Rounds line, and gives it its own row only if it passes the row test.)
3. **Part 1** now says plainly: "Some answers, decided and provisional, depart from a recommendation you saw or from a rule or wording you confirmed; each is marked Yes under “Changed”."
4. **2b item 1, "Changed?"**: "No. Consistent with option B of question 6(b), which was recommended."
5. **2b item 8, PetSmart**: "nor invited after the board acted" is restored.
6. **3.3(c)**: the example no longer says all 16 unnamed Mac-Gray signers are recorded as not submitting. It says those of the 16 who were eligible for 23 July and are never mentioned again are recorded as not submitting by it, "0 to 16 of them, as in 3.2", consistent with 3.2 and `MAP_RECHECK.md` (Mac-Gray §3: bounds; later signers are dropped by the target by 25 July).
7. **Appendix cuts that removed supporting words**, restored with ellipses where words are still cut:
   - C13: "a preliminary indication of interest, which they were instructed to submit by July 23, 2013" (the antecedent), and on 19 September "The Special Committee then discussed each of the three revised proposals";
   - C19: "Deutsche Bank encouraged Party A to submit a letter of interest that could be reviewed by the board of directors";
   - C14: "On October 30, six of the potentially interested parties submitted indications of interest" and J.P. Morgan's calls of 30 October to 2 November;
   - C15: on 20 July, "and to provide these parties with additional financial and other due diligence materials".
8. **2a, contingent payments**: the case now reads "$19.00 cash plus options Party B valued at $2.50, so upfront $19.00 and CVR/earnout $2.50" (p. 36; C1), and C1 again quotes "the remaining per share price to be paid in the form of options".
9. **2b comments**: each item has its own shaded comment row (at least 0.5 inch) under it, kept with the item, in place of the one box for all eight.
10. **Page labels**: a non-breaking space after "p." and "pp.", so "(pp. 33–34; C2)" no longer breaks after "pp.".

As the review asked, every other excerpt was re-read against the claims it supports, and these operative words were also restored from the verified version:
- C2: that the exclusivity request came in Company E's "revised letter of intent";
- C4: WDC's 10 June "price range of $6.60 to $7.10 per share in cash" (it is the price-only revision of 2b item 5);
- C6: that the $15 million reverse fee was "in the event regulatory clearance is not obtained", and that Kirkland's revised draft of the Pamplona commitment letter made the 5 October proposal;
- C7: "although Parent required debt financing to consummate the merger";
- C9: the full 27 October outreach ("to evaluate its interest in a potential transaction with the Company"), and that Company E's prior structure was "for 100% of the Company’s outstanding equity and equity awards";
- C12: that sTec's bankers "informed Company D’s representatives that timing for sTec’s process had been delayed, and that Company D had an opportunity to continue", and that D asked for time "to continue its ongoing due diligence review";
- C15: the 6 July request for bids "that ascribed a greater value to Kraton before making any determination" on the second round, and that the final bid procedures letter went "to Party A, Party H, and Parent";
- C16: the named signers in the non-disclosure counts, the board as the actor on 27 July, and the 1 October "interest … in reengaging in the process";
- C17: "at the direction of the board" (16 May) and "our board of directors directed BofA Merrill Lynch" (29 May);
- C19: that 13 October was "a discussion with representatives of Party A".

Three fragments not in the verified version were added from the filings, and the build's check found each on its cited page:
- C13, p. 32: "Over the next two months", the confidentiality agreements' signing window, which the 0-to-16 bound rests on;
- C13, p. 33, 25 July: "representatives of BofA Merrill Lynch reviewed the preliminary indications of interest received from Party B, Party C and CSC/Pamplona", the support for "day-late responses were considered";
- C14, p. 24: J.P. Morgan's calls were "to hear the parties’ respective rationales for the price levels suggested in their indications", which bears on whether Bidder 2's raise was invited.

One fix beyond the review: the first condensed build had turned PetSmart's "with no invitation reported" into "Bidder 2's uninvited raise", which claims more than the filing says. The verified wording is restored.

## Sources for what the document says Alex saw or wrote

- **What Alex saw on 24 September.** The question numbers, the options and which options were recommended come from the original DOCX, read from a copy.
- **The column rules he confirmed.** From `TAXONOMY_DRAFT5.md`: Part A item 3's "a contingent part of the price"; line 40 on a later exclusivity request; §3.3(b) on copying values.
- **Alex's own words.**
  - `sources/voice.txt`: Kraton item 3 (P82); sTec item 6 (P125); the start of round 1 (P173); exclusivity (P49); Providence and Worcester Party A (P22).
  - `sources/qa.txt`: the partial-bid remark, Q7d (P112).
- **Alex's spring coding.**
  - G&W, 26 July 2016, Formal: `analysis/compare-alex-providence-worcester-pilot-38bc24/alex_bids.csv`.
  - WDC, 10 June, Informal, and Company H as its own drop: the 24 September document.
  - sTec's final round extended to 10 June: `MAP_RECHECK.md`, which cites the audit's `deals/stec.md`.
  - P&W Party A's drop on 22 July: `lesson/independent-audit-2026-09-23/lessons-disposition.md`, PW-A.
- **Side-by-side numbers.** From P's `compare_alex` outputs (`analysis/compare-alex-*/summary.json`, `alex_bids.csv`), which confirm the spec's figures:
  - T0 matches Alex's labels on 13 of 13 Mac-Gray bids and 11 of 14 P&W bids;
  - T1 matches on 11 of 13 and 14 of 14;
  - T1u matches on 11 and 13, T2 on 12 and 11, T3 on 13 and 11.
  The bids that differ were read from `alex_bids.csv`.
- **Maps and deadline outcomes.** From `MAP_RECHECK.md` ("For Decision 1", "E9 under D11" and the deal sections).
- **Rule wording.** From the frozen candidate (`c2d47a47…`) and `R_REVIEW.md`.
- **The switches.** From `ANALYSIS_CONTRACT.md` §7–§8.

## Choices made where the spec is silent

- **D8's case.** The case column for D8 names Synacor, 27 October 2020, and Datalink, 1 October 2016 (option A's own examples, confirmed by the map re-check); §5 has "—".
- **sTec in Decision 1.**
  - "Show both maps" is read as map A (the re-check's recommendation) against map C (Alex's voice note), in tables.
  - Map B, the current ledger with a round 3, is described in one sentence and offered as a circle option.
  - Alex's spring coding is set beside them, as the re-check recommends.
- **Decision 3b(a).** It lists T1u beside T0–T3. T1 against T1u is how the contract emits the "how to treat Unclear" switch of D22, so the question covers that switch too.
- **The source hierarchy.** Option C describes the working practice recorded in the independent audit (`lesson/…/questions-disposition.md`, B6): a general rule stated in the notes governs, and a remark about one deal is a reading to confirm.
- **Readings.**
  - Company H: the exit reason is left unstated, following the §5 wording (target-side nonadvancement, bounded timing, feedback kept).
  - Penford: 13 October gets an optional "a bid / not a bid" circle.
- **Headings.** The open decisions are numbered 3.1–3.5 for Alex, with the spec's names (Decision 1, 3, 3b) as small references.

## Not asked (for Austin)

- **Two further switches.** `ANALYSIS_CONTRACT.md` also has "eligible but unadmitted bidders as live" and "upfront or package price". D22 and §5 do not list them, so the document does not ask about them.
- **PetSmart's 30 October outcome** depends on a reading the re-check left open. The document states it conditionally.

## Revision after review (25 September, before condensing)

A review of the first build (5,872 words, SHA-256 `81a7874f…c392`) found one major and seven minor problems. All were fixed in the verified version (`31e6909b…`), the length problem only in part; the condensing above took it further. The fixes are all kept in the condensed text:
1. **sTec, 30 May (major).** The 3.1 note says your spring coding agrees with map A on the round count but extends the round to 10 June, where map A has 30 May Enforced (pp. 31–32). Map A's round-2 cell gives both outcomes (28 May Extended; 30 May Enforced); map C's cells give its outcomes. 2b item 8 names sTec's 30 May.
2. **Mac-Gray Party B's financing.** 2b item 6 says the committee's 19 September expectation is not a term of the bid; the 3.3 note says the trial ledger took Financing Contingent from that remark.
3. **PetSmart, 30 October.** The condition is the real hinge from `MAP_RECHECK.md`: Bidder 2 raised its on-time bid before the board acted on 3 November, with no invitation reported; Enforced if that is bargaining within the round, else Unclear, being neither an overdue response nor invited after the board acted.
4. **Synacor, 27 October.** C9 quotes the outreach ("on October 27, 2020, Mr. Bhise again reached out to Company H", p. 34), not the committee's authorization.
5. **Kraton C7.** The King & Spalding excerpt names its actor, with "Kraton's counsel" in the label.
6. **Item 3's "Changed?" cell** starts "Yes, in part.", matching part 1.
7. **Page ranges and excerpts for the maps.** The 3.1 headings cover every fact in the maps (Kraton pp. 33–39; Datalink pp. 27–32; sTec pp. 27–32, citing C4 and C17); C15 has Party A's 17 September bid and the Board's review of 18 September; C16 has the board's 29 January meeting.

Checks after the review fixes:
- all 59 excerpts were found on their cited pages, and the negative test failed as it should;
- the fact check above reported no problems beyond the three intended additions, and its own negative test caught every planted change;
- a rebuild with `--date 2026-09-25` reproduced `word/document.xml`, `styles.xml`, `footer1.xml` and `docProps/core.xml` byte for byte;
- a text search found no internal jargon (package names, wave, lens, spec, pilot, cockpit, checker, E-rule numbers); "package" appears only in its plain sense ("the 21–23 September 2013 package");
- no D-number or "Decision n" appears outside the small reference style; no page label keeps a breaking space; no non-breaking space was put inside a quotation;
- I looked at all ten rendered pages;
- the original 24 September DOCX is unchanged (`faab1d66…5220`).
