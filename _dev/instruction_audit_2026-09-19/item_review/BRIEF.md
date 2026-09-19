# Brief: in-depth review of 15 unconfirmed items in the revised extraction instruction

## Background
Austin Li (PhD researcher) and Prof. Alex Gorbenko study informal bids in takeover auctions. An AI model reads the "Background of the Merger" of an SEC merger filing and produces a deal ledger in Excel: one row per event (contacts, NDAs, bids with a Formal/Informal label and a None/Light/Heavy conditions flag, round openings, deadlines, dropouts, signing). The data feeds descriptive work and structural estimation of auctions with informal and formal rounds. First-order variables: number of live bidders per stage, round assignment, the formal/informal label, event ORDER, bid prices. Alex wants flexibility to reinterpret at estimation (e.g. treat a formal-but-heavily-conditioned bid as informal) and cares more about the sequence of events than exact dates. He reviews workbooks by hand and dislikes bloated ledgers.

The instruction was revised on 19 Sep 2026 after an audit against Alex's own documents. Most edits were confirmed by Austin. FIFTEEN items are in the instruction but NOT yet individually confirmed. Austin wants a careful recommendation on each before he runs any extraction. Nothing has been run with the revised instruction.

## Files (READ-ONLY — do not modify anything except your own output file)
Repo: /home/uctpiaj/Projects/Sec_extraction_new
- Revised instruction (the thing under review): SEC_Deal_Ledger_Extraction_Instruction.md — read it IN FULL.
- What changed and why: instruction_audit_2026-09-19/INSTRUCTION_CHANGELOG.md ; exact wording changes: instruction_audit_2026-09-19/instruction_changes.diff
- Audit behind the changes: instruction_audit_2026-09-19/FINAL_instruction_audit.md ; evaluation of open questions: instruction_audit_2026-09-19/QUESTIONS_evaluation.md ; helper reports in instruction_audit_2026-09-19/helpers/
- Alex's originals: ref/ (alex_voice_notes_2026-08.docx, CollectionInstructions_Alex_2026.pdf, deal_details_Alex_2026.xlsx). Text extractions, if the scratch folder still exists:
  SCRATCH=/tmp/claude-82775/-home-uctpiaj-Projects-Sec-extraction-new/f11e904c-2474-4c33-876a-ea725692d60d/scratchpad
  $SCRATCH/alex_notes.txt (voice notes on 8 deals + his own closing summary; leading [hex] tag = his colour code: [] important & easy, [8B0000] important & hard, [0000CD] minor & easy, [8B008B] minor & hard; the middle "Claude's reading" section is an AI summary, not his words), $SCRATCH/alex_collection_instructions.txt (collection instructions + March 2026 email; black text = Chicago RAs' rules, "Alex's addition" boxes = his), $SCRATCH/alex_hand_collected_9deals.txt (his hand-corrected rows for nine deals with comments; font colour lost — red = his own edit, black = RA row he kept; re-read fonts from the xlsx with openpyxl if authorship matters).
  If SCRATCH is gone, re-extract from ref/ (python3 + openpyxl, pdftotext, unzip the docx).
- Filings: raw_filing/*.htm ; plain text in $SCRATCH/filing/<deal>_bg.txt (background section) and <deal>_full.txt, deals = providence-worcester, mac-gray, petsmart.
- The 12 earlier model workbooks (made under the OLD instruction) as text: $SCRATCH/dump/<model>_<deal>.txt (models opus, ds, sol, glm); originals in extraction/*.xlsx. Useful to see how models actually behave.
- pro_review_2026-09-18/audit_notes_2026-09-18.md section A: description of Alex's worksheet, his vocabularies and every comment verbatim.

## Decisions Austin has already made (fixed — do not reopen)
Judge extractions by Alex's checklist, not GPT Pro's. Every row gets an always-filled, order-respecting Working date with a Date method; honest window stays in Date from/Date to. Every NDA signer who did not win gets an exit row that says clearly in what fashion it was out (Outcome basis: Stated / Inferred: residual / Inferred: exclusivity / Inferred: silent / Inferred: identity). Rivals are Dropped by target when exclusivity is executed and Re-entered if they return. Information-access rows kept; deal-terms, rollover-thread and post-NDA meeting rows cut. No interactive pause; batch runs. Conditions level rates what the bid itself carries; a Conditions detail column keeps financing / diligence required / diligence open / exclusivity. Deadline treatment values are defined from ledger rows (Enforced = date passed, no extension, target took its next step on the bids in hand).

## The 15 unconfirmed items
Six that need a real decision:
1. LATE RECONFIRMATION ROW (§9.1 "Late reconfirmation", §12 example C): a bidder returning a revised agreement draft or confirming its price late in a definitive-agreement stage gets a `Bid reaffirmed` row — Formal, price Carried forward, flagged. Example: Providence Party B, Aug 4, $24 (Alex's voice note I.14; his red hand-collected row 6054).
2. CALIBRATION EXAMPLE B (§12.B): the five undated late-July Providence LOIs get Working date July 20 (deadline) AND a Date from/Date to window of July 20–22, the upper bound being Alex's cross-paragraph reading of "the Transaction Committee met … on July 22 … and … July 27 … to review the LOIs". Alternative: window July 20–27, Working date still July 20.
3. ROUND-1 START (§6.3): round 1 opens when the target or its banker first solicits buyers (first outreach wave, or the launch decision when outreach follows at once); a sale decision or press release that defers outreach is round 0; the round-1 row states `R1 anchor:` and lists other candidate rows. PetSmart → Alex's Oct 3; counter-view: the Aug 19 press release was itself a solicitation (Opus's reading).
4. "AT LEAST $X" (§9.4): X in Price low, Price high blank, Price kind = Bound only, `Bound: ≥ X` in Terms, ambiguity raised in Questions. Replaces "leave both price cells blank". Example: PetSmart's third bidder ("ranges that reached at least $80.00").
5. TERMINATED PROCESS CLOSES ITS PARTICIPANTS (§10.2): the `Process terminated` row closes everyone still live in that attempt; no individual inferred exit rows. No example among the three deals (Zep in Alex's sheet has one).
6. FINANCING SUPPORTER / COHORT MEMBERS COMBINING (§5.3): a party that finances another bidder's offer does not bid; supported bidder keeps its name with `Support: [party] (financing)`; supporter gets `Joined group` only if it was still a live bidder; when anonymous NDA signers combine (PetSmart Bidder 3) the row states "units −1"; never backfill an NDA the filing does not report.
Nine small ones:
7. Round finality phrase at the start of Terms on each `Round opened` row: `Announced as final` / `Inferred final` / `Not final` (§6.3).
8. `Treatment: …` prefix at the start of Terms on each `Deadline` row (§8.3). (The treatment definitions themselves are confirmed.)
9. "counts" added to the list of things the model may resolve from the rest of the filing (§1).
10. New-process test: largely new participants after dormancy → new process; same participants resuming → same process (§6.2).
11. Design choices: `Date method` as its own column; `Outcome basis` as its own column (alternative: a text prefix only); `Information access changed` as its own event label (§11.2, §11.3).
12. Adviser dates: Working date = earliest date the adviser is shown selected or acting; all disclosed dates listed (§5.4).
13. "Signing alone never creates" a reaffirmation row (§9.1).
14. Per-stage stock check: entrants − exits + re-entries, never negative, only the winner left at signing (§13.3).
15. Go-shop entrants are closed at go-shop expiry (§10.2).

## Standard for your findings
For each item assigned to you: (a) quote the exact current wording in the instruction; (b) evidence from Alex's documents (quote + location; say whether it is his own rule/red edit, a dictated voice note, or an inherited RA row) and from the filing text where a deal example is involved; (c) apply the rule by hand to every relevant case in the three filings (and, from his sheet/notes, to his other six deals where possible) and say what rows it would produce — look for cases where the wording is ambiguous, produces something Alex would object to, or collides with another rule in the instruction; (d) downstream risk: how could the resulting cells mislead an estimation or a reviewer, and how reversible is the choice after hundreds of deals are extracted; (e) verdict: KEEP AS IS / KEEP WITH REWORDING (give the exact replacement text, minimal) / DROP / CHANGE TO ALTERNATIVE (say which) — with confidence and what you could not check. Be concrete and skeptical; do not pad; do not defend an item just because it is already in the instruction. Do not modify the instruction or any other repo file.
