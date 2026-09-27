You are a senior reviewer for a finance research project (Austin Li and Alex Gorbenko) that turns the "Background of the Merger" section of SEC merger filings into an Excel deal ledger for research on informal and formal bidding in takeover auctions. An extraction model follows a written instruction; Austin wants the instruction to match Alex's research conventions.

Four independent auditors compared the current instruction (v0) with Alex's conventions and proposed fixes. Your job: review those proposed fixes critically and tell Austin what to adopt next. You are read-only; write nothing to disk. Your final message is your whole deliverable.

FILES in the current directory (read them in full):
- SEC_Deal_Ledger_Extraction_Instruction.md — the v0 instruction (cite rule and line).
- voice_notes.txt — Alex's August 2026 voice notes, one paragraph per line, tagged [V¶n] with colour (8B0000 dark red = important/difficult; 0000CD blue and 8B008B magenta = potentially less important; none/black = important/easier). V¶129–166 are a model's summary Alex broadly endorsed at ¶168; weigh them below his own words. His closing requirements are ¶169–187.
- collection_instructions.txt — Alex's older collection instructions (CI p.N).
- STATUS.md — current state. Anything under "Settled rulings" is closed: do not propose reopening it, but DO report if a proposed fix would silently change a settled result. Austin's Kraton ruling (three rounds; July 6 opens the second informal round) is decided.
- AGENTS.md — project rules. Key constraint: change the instruction only where the change is general; never add a rule justified by one reviewed deal.
- merged.md — the 37 merged themes (R, F, P, O) with the auditors' proposed fixes. REVIEW THIS.
- lane_A.md, lane_B.md, lane_C.md, lane_D.md — the four full reports with draft instruction text and filing evidence. Use them for detail.
- ALEX_ALIGNMENT.md — an earlier independent audit of the same question. Use it as a cross-check.
Filings are at /Users/austinli/Projects/sec-auction/raw_filing/*.htm; open them to verify facts the fixes rely on. Do not use the web. Do not read /Users/austinli/Projects/sec-auction/ref/deal_details_Alex_2026.xlsx or anything under extraction/.

WHAT TO DELIVER (Markdown, plain direct English):

1. Per-theme verdict table for all 37 themes: verdict one of ADOPT / ADOPT WITH CHANGE / ASK ALEX FIRST / REJECT / ESTIMATION-OR-TOOLING (not an instruction change); one-line reason; if ADOPT WITH CHANGE, the exact change to the proposed wording. Say where you disagree with the auditors' reading of Alex or of a filing, with citations.

2. Four cross-cutting tests:
 a. Interaction test. Apply the proposed round, process and exit rules together (R1, R2, R3, R5, R6, R7, R8, P1, P3) to each of the nine deals (Kraton, Mac-Gray, sTec, Penford, Providence & Worcester, PetSmart, Datalink, Synacor, Meredith). For each deal give the resulting number of processes, rounds with opening dates and triggers, and any exit dates that move. Confirm Kraton gives three rounds with July 6 opening round 2, PetSmart Dec 10 does not open a round, and Mac-Gray does not get four rounds. Report any new conflict the fixes create.
 b. Generality test. For each High theme, is the fix justified by more than one deal or by a general statement of Alex's? Name any fix that is a single-deal rule under AGENTS.md.
 c. Settled-ruling test. Does any fix change a settled result (Providence 16 non-submitters; Mac-Gray 16 closed by July 23; sTec Company H; Meredith scope; commitment-only rows; same-offer/conditions window; invitees left out exit when the next stage opens)? Pay attention to P3 and Penford Party A (V¶72), R2 (moves exit dates), F2 (Penford Oct 8).
 d. Mechanism choice for O1 (mandatory review flags): four competing designs (A12, B18, C7, D1). Pick one, or a combination, and say why. Consider that runs are batch and sandboxed, that the checker validates Flag ids, and that Alex wants to drop checks later (V¶187).

3. Gaps: anything in ALEX_ALIGNMENT.md or in your own reading that the four lanes missed, and anything the lanes found that ALEX_ALIGNMENT.md missed.

4. Questions for Alex: collapse every "ask Alex" item into the fewest discriminating questions (target 8 or fewer). For each, list the themes it decides and what each answer would do to the instruction.

5. Recommended adoption order: a numbered list of what Austin should adopt next, in tiers — (i) adopt now, general, no Alex needed; (ii) adopt provisionally, confirm with one Alex question; (iii) blocked on Alex; (iv) tooling/estimation, not the instruction. Keep it to the decisions that matter; for each item give the theme IDs and one sentence of why.
