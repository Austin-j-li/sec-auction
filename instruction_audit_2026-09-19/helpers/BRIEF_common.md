# Common brief: audit of the extraction instruction against Alex's documents

## Background
Austin Li (PhD researcher) and Prof. Alex Gorbenko study informal bids in takeover auctions. An AI reads the "Background of the Merger" of an SEC filing and produces a deal ledger (Excel). The current extraction instruction, `SEC_Deal_Ledger_Extraction_Instruction_v2.md`, was largely written by GPT Pro. It says of itself that it is "a working research specification, not a claim that Alex has approved every operational choice."

GPT Pro then reviewed 12 extractions (4 models x 3 deals) against that instruction and produced 83 "corrective findings". Pro never saw Alex's documents. Austin suspects Pro (and therefore the instruction) has tunnel vision in places: it optimises for epistemic/source-fidelity purity in ways Alex, the actual data user, does not want. Austin's one concrete example: the instruction/Pro penalise assigning a date to a vaguely dated event, whereas Alex has said assigning a rough date is acceptable because what matters is preserving the chronology/sequence of events (while being aware of the quirks that creates). Austin believes there are more such cases he cannot recall offhand.

## The task
Audit the INSTRUCTION against ALEX'S DOCUMENTS. Alex's documents are the authority on what the data is for and what conventions he wants. Find every place where the instruction:
- (A) is STRICTER / more conservative than Alex wants (forbids or discourages something Alex asks for or does himself),
- (B) is LOOSER than Alex wants or contradicts him,
- (C) is SILENT on something Alex asks for,
- (D) spends effort/complexity on things Alex never asked for and that plausibly crowd out what he does want (over-engineering),
- (E) matches Alex well (list briefly, so the final picture is balanced).
Also note (F) places where Alex's own documents are inconsistent with each other, ambiguous, or where his preferred convention has real quirks/costs that Austin should be aware of before adopting it. Do not assume Alex is always right; do assume he is the user whose needs define the target. Test Austin's hypothesis rather than assuming it.

Where useful, show the practical consequence: how the instruction's choice played out in the 12 workbooks or in Pro's 83 findings (e.g. a Pro "defect" that is actually what Alex wants, or an Alex complaint nobody caught).

## Files (all read-only; do NOT modify anything in the repo)
Repo: /home/uctpiaj/Projects/Sec_extraction_new
- Instruction under audit: /home/uctpiaj/Projects/Sec_extraction_new/SEC_Deal_Ledger_Extraction_Instruction_v2.md  (read it IN FULL; ~62KB)
- Alex's originals: /home/uctpiaj/Projects/Sec_extraction_new/ref/  (alex_voice_notes_2026-08.docx, CollectionInstructions_Alex_2026.pdf, deal_details_Alex_2026.xlsx)
- Text extractions of Alex's docs (use these; consult originals if something looks off):
  SCRATCH=/tmp/claude-82775/-home-uctpiaj-Projects-Sec-extraction-new/f11e904c-2474-4c33-876a-ea725692d60d/scratchpad
  - $SCRATCH/alex_notes.txt  — voice notes on 8 deals + his summary. Leading [hex] tag is his colour code: [] black = important & easy; [8B0000] red = important & hard; [0000CD] blue = not first-order, easy; [8B008B] magenta = not first-order, hard; [595959] grey = other project. Note the middle "Claude's reading" section is an AI summary, not Alex's words; "Alex's summary" at the end IS his.
  - $SCRATCH/alex_collection_instructions.txt — his data-collection instructions + his March 2026 email (includes his view on rough vs precise dates).
  - $SCRATCH/alex_hand_collected_9deals.txt — his hand-corrected rows for 9 deals (Providence, Medivation, Imprivata, Zep, PetSmart, Penford, Mac-Gray, Saks, sTec) with his comments. This shows what he actually DOES (e.g. how he dates vague events, when he records Drop / DropTarget, what he calls Formal). Font colour (red = his correction) is lost in this extract.
  - /home/uctpiaj/Projects/Sec_extraction_new/pro_review_2026-09-18/audit_notes_2026-09-18.md — an earlier evidence-based description of how Alex's worksheet works (section A lists all his comments verbatim and his vocabularies; useful, but it is a secondary source).
- Pro's review of the 12 extractions: /home/uctpiaj/Projects/Sec_extraction_new/model_review_2026-09-18/results/  (SEC_12_Extraction_Model_Review.md, SEC_12_Extraction_Issue_Register.csv, GPT_Pro_Final_Response.md)
- The 12 workbooks dumped to text: $SCRATCH/dump/<model>_<deal>.txt  (models: opus, ds, sol, glm; deals: providence-worcester, mac-gray, petsmart). Filing text: $SCRATCH/filing/<deal>_bg.txt (background section) and <deal>_full.txt.

## Leads already noticed (verify, don't just repeat; they are starting points, not conclusions)
1. Alex's email: for "mid-February" a rough date 2/15 is fine — "We want to know the sequence of events but not necessarily the exact date." His voice-note summary item H: "Exact dates are less interesting to me, but the order of events must be precise". Instruction section 8.1 leaves Working date blank for one-sided windows and warns against contextual exact dates; Pro scored several "unsupported exact date / overprecise date" defects.
2. Alex's hand-collected rows give nearly every participant an exit (e.g. Providence "16 parties — Drop 06/01/2016", i.e. 25 NDAs minus 9 IOIs; "Party A Drop 07/22"; "Party E/F Drop 08/12 — did not engage for a while"). Instruction section 10 says record supported changes, "not an accounting closure", "No exit row is required for every NDA signer". Pro scored PetSmart's 15−6=9 non-submitter row as a Major defect although Alex's PetSmart note 5 asks for it.
3. Mac-Gray: Alex wants rivals "dropped by target" when exclusivity is granted (Sep 24); instruction section 10.1 says exclusivity => "Participation paused", not an exit.
4. Providence Aug 4: Alex wants a priced Formal $24 bid-revision row for Party B (his note 14; his hand-collected row 25.5); instruction section 9.1 says a further draft is not a bid.
5. PetSmart Longview rollover: Alex says not a consortium; instruction 5.3 agrees, yet all four models coded "Bidding group changed".
6. Alex wants tight cross-paragraph date inference (late July -> Jul 20-22; first week Oct -> Oct 3-7) and round starts tied to board meetings; instruction 8.1 says "Tighten a window only when a passage actually constrains that event."

## Standards for your findings
- Every finding needs BOTH sides quoted verbatim with location: instruction section number + quote; Alex document + deal/item number (or Excel line) + quote. No paraphrase-only findings.
- Say which direction (A–F), how much it matters for Alex's research use (High / Medium / Low, with one-line reason — think: would it change a bidder count, a round assignment, a formal/informal label, event order, or reviewer workload?), and your confidence.
- Propose the smallest fix: either a sketch of the instruction patch, or the exact question Austin should put to Alex when only Alex can decide.
- Be concrete and skeptical. Don't pad. Don't rewrite the instruction.
