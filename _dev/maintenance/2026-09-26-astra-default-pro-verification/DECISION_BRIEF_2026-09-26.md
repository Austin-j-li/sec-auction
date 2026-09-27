# Decision brief: what remains for Austin after the 26 September handoff

> **Status note, 26 September 2026 (added after the v1.14.1 candidate; body unchanged).** Resolved: §§1–4 by R1–R6 and D2 of [V1141_SPEC](../2026-09-26-v1141-streamline/V1141_SPEC.md) §3 and §6 (1a becomes Same offer, R1; 1b becomes the evidence window with forecasts, R2; 1c follows from R2's window; §2 becomes R3; §3 becomes R4; §4 becomes R5, with Company H Dropped by target and reason Would not improve earlier offer); §6 by the switch back to Opus 5.5 medium, so the retest is five Opus 5.5 medium runs, not three Astra-high runs (V1141_SPEC §10 step 5; not yet run, GATE); §7 by R6 (Not begun only before an NDA). §5 (P1) is approved and implemented under [PIPELINE_UPGRADE_SPEC](../2026-09-26-v1141-streamline/PIPELINE_UPGRADE_SPEC.md) WP3. §8 is carried out in the reconciled questionnaire (`../2026-09-24-bid-terms-taxonomy/evidence/a2/README.md`); it has not been sent.

26 September 2026. Prepared for Austin by Claude, after the root `HANDOFF.md` recorded four settled treatments (Company H dropped; P&W 16 non-submitters; Mac-Gray 23 July closure; commitment changes without fresh prices). Nothing here changes an instruction, workbook, tool or cockpit state. Each section gives the source text, the current rule, the proposal on the table, what the trial workbooks did, the options, and a recommendation.

Source files: filings in the trial packet (`inputs/raw_filing/`); the tested candidate (SHA `c2d47a47…ab27`); `AMENDMENT_SPEC.md` and `PRO_FINDINGS_VERIFICATION.md` in this folder; the 25 September questionnaire; Alex's numbered voice notes in `evidence/`.

| # | Decision | Stakes | Needs Alex? | Recommendation |
|---|---|---|---|---|
| 1 | What a "same offer" reference carries, and whether same-day or later assessments describe a bid (A1) | High: changes Heavy/Unclear on final bids, which feeds the Formality readings | No | Split A1 into three rulings (1a carry with Inferred; 1b same-day assessment allowed; 1c later diligence passages not allowed) |
| 2 | General wording for residual-cohort closure and named-party overlap (A2) | High: live-bidder counts | No | Replace A2 with the wording in §2 |
| 3 | Joint diligence-and-negotiation periods and H2 (A3) | Medium | No | Approve A3 |
| 4 | Company H: general rule, date and exit reason | Low for counts, medium as a precedent | No | Dropped by target by 16 May; reason Would not improve earlier offer |
| 5 | Analysis-tool amendment P1 | Medium: stops blank-price rows counting as price observations | No | Approve P1 as written |
| 6 | Retest and release | Operational | No | Three isolated Astra-high runs on the revised candidate, then decide on publication |
| 7 | Does a confidential memorandum count as diligence access? | Low (three trial rows) | Optional | Decide yourself: yes |
| 8 | What to send Alex, and when | Process | It is about him | Send after the candidate is revised; five items remain |

---

## 1. Offer terms versus status facts (amendment A1)

### The problem

A bidder often refers back to an earlier proposal: "its previous indication … was its best and final offer". The question is what that reference carries forward. Some things are **terms** the bidder is offering (price, structure, a financing condition). Others are **status facts** about the world on an earlier date (no commitment letter yet; diligence unfinished). Separately, the filing sometimes describes the bid in a board discussion held hours or days after it arrived, or describes diligence in a passage dated later.

### Current rule (tested candidate)

- E10, express incorporation: "Carry a term from an earlier row only where the filing says it was carried, and only within the scope stated … Judge status facts, such as how far diligence had got, at the new date."
- E12: conditions record "what the filing reports for the bid at the date it was made … earlier terms carry over only by express incorporation." Due diligence may use "a later passage … only if it dates the fact". E12's example table: "The board weighs a regulatory risk common to every bidder … → Regulatory Concern".

### Proposal A1 (not approved)

Carry only offer terms. "A statement about an earlier state of affairs, such as unfinished diligence or financing documents that were not yet committed, is not itself a term". Otherwise Not stated, with the earlier fact kept in the Note. In E12: "A later assessment or improvement is not knowledge at the earlier bid date." Its acceptance table names "a board assessment occurs later that day" as not usable.

### The three cases it decides

**(a) Mac-Gray, Party A, 18 September.**

> 10 Sept: "Party A submitted a revised indication of interest with an all-cash purchase price of $18.00 to $19.00 per share, to be financed by outstanding credit facilities or affiliated equity sources … Neither Party A's nor Party C's revised indication of interest included a firm financing commitment." (p. 35)
>
> 18 Sept: "Party A reiterated in a telephone call … that its previous indication of interest with an all-cash purchase price of $18.00 to $19.00 per share was its best and final offer." (p. 36)

| Workbooks | Financing on 18 Sept | Conditions |
|---|---|---|
| Astra high, Opus medium, Opus xhigh | Contingent ("Terms: as #n") | Heavy (H1) |
| Sol xhigh, Astra xhigh | Not stated | Unclear |

Under A1 the second group is right. Pro and my breakdown preferred the first group. The verification report (MG6) called it "qualified; not a settled correction".

**Why it matters downstream.** Party A's 18 September bid is Formal (it answers the final-round request). Under the questionnaire's Formality readings, T1 counts a bid as formal when it is Formal and not Heavy, with Unclear counting as not Heavy. So the same bid is *formal* under T1 if coded Unclear and *not formal* if coded Heavy. The same issue hits Party B's 18 September bid (below).

**(b) P&W, G&W's 12 August bid and the regulatory assessment.**

> Morning: G&W's revised LOI at $25 had arrived; "The Transaction Committee met at 10:30 a.m. on August 12 … directed representatives of BMO to inform Party B that another party had submitted a revised LOI at a higher price." (p. 31)
>
> Afternoon, same day, before signing: the board was told "the STB approval process for G&W and Party B would be different since G&W owned connecting railroads", called STB counsel about "the risks associated with each process … and the likely timeframe", and "determined that the timeframe for, and the likelihood of, obtaining the required regulatory approval was not materially different". (pp. 31–32)

Opus medium and Opus xhigh code Regulatory = Concern on G&W's bid; the other three code Not stated, and Astra high records the assessment as its own later event. Under the current text (date-level, plus the "board weighs a risk" example) Concern is permitted. Under A1 it is not, because the assessment was hours after the bid. The verification report (PW6) sided with A1.

**(c) Mac-Gray, CSC's 18 September bid and "confirmatory" diligence.**

> The only statement that CSC's remaining work was confirmatory is dated 25 September–7 October, after exclusivity: "CSC and Pamplona were granted full access … and conducted confirmatory business and legal due diligence" (p. 38). The earlier "follow-up and confirmatory" calls (27 Aug–3 Sept, p. 35) were with Parties B, C and A, not CSC.

Opus xhigh codes CSC's 18 September bid Light citing p. 38. The current rule already forbids that (the later passage does not date the fact to 18 September). A1 would say it again.

**Related: Mac-Gray, Party B, 18 September financing.** The 9 September bid "did not include a firm financing commitment" (p. 35). The 18 September package says nothing on financing. On 19 September the committee "noted that Party B would likely be financing the transaction with a combination of equity from affiliated funds and third party debt capital, which would involve more risk" (p. 37). Opus medium (marked Inferred) and Opus xhigh (not marked) code Contingent/Heavy. The questionnaire's item 2b.6 already says analysis would not use the 19 September remark, and the verification report (MG3) agrees. This follows whatever you decide in 1a and 1b.

### Options

- **Adopt A1 whole.** Clean and conservative. Cost: the analysis sees Party A's reiterated offer and Party B's package as Unclear rather than Heavy, even though a human reader would say nothing changed in eight days. The Note keeps the earlier fact, but analysis code reads cells, not Notes.
- **Reject A1; keep the current text.** Leaves the split you saw: three models carried, two did not.
- **Split it (recommended).**
  - **1a. A bidder that expressly re-offers its earlier proposal unchanged carries that proposal's financing and diligence state, marked Inferred = Y, with "Terms: as #n".** Code a status as changed only where the filing reports a change. This matches how Alex reads "same offer" and what three of five models did, and the Inferred flag keeps it separable.
  - **1b. A board or adviser assessment made while considering a bid, before the next bid arrives, describes that bid.** This keeps the E12 example working. It covers G&W (same afternoon) and Party B (the committee meeting that reviewed that package), each marked Inferred where the assessment is a forecast ("would likely").
  - **1c. A passage dated after a later event, such as exclusivity or another bid, does not describe an earlier bid.** This is the current rule stated plainly. It rules out CSC's Light.

## 2. General wording for your cohort decisions (amendment A2)

### Your settled cases

- Mac-Gray: 20 NDA signers "over the next two months" after 24 June; package holders "were instructed to submit by July 23" (p. 32). Named: Party A (strategic, signed 5 August), CSC/Pamplona, Party B, Party C. Your ruling: the 16 unnamed financial signers are Did not submit, Count 16, dated 23 July, Inferred, reason Not stated.
- P&W: 11 strategic + 14 financial signers after the 28 March outreach (p. 28); "each potential buyer had been advised to submit" by 10 May, moved to 19 May (p. 29); nine IOIs. Your ruling: 25 − 9 = 16, Did not submit, Count 16, Inferred, reason Not stated, assuming the nine bidders are among the 25; no double-counting of later mentions.

### Why A2 must change

A2 as drafted says: "an NDA cohort accumulated after an early deadline cannot all become Did not submit by that deadline" and "A residual subtraction does not establish invitation, non-submission or an exact departure date unless those premises are supported." That forbids your Mac-Gray ruling and makes the P&W subtraction contestable. The candidate's E3 already has a sentence pointing the same way ("An NDA signed at some point in an interval does not prove eligibility at a deadline inside that interval"; "Never get an exact number of non-submitters by subtracting bids from a group that was not, as a whole, eligible at that deadline"). Those two sentences need to be softened too, or the models will keep splitting.

Alex's voice notes support the ordinary-sequence approach: PetSmart ("For the remaining 9 bidders with NDAs but without IOIs … that should be recorded as unknown", para. 60), Mac-Gray ("This only leaves 2 strategics and 16 financials that are unnamed … the math has to check out", para. 41), and P&W on double counting (paras. 12–13). The questionnaire's 3.2 option B ("the ordinary-sequence count, with the bounds for robustness") was already the 24 September recommendation.

### Proposed replacement for A2 (E14, before the inferred-closure list)

> Where the filing reports a group only as a total and gives no individual dates, assume the ordinary sequence: members signed, received the information and were eligible for the first solicitation that followed. Close unnamed members who made no reported submission as Did not submit by that solicitation's due date, Count by exact arithmetic under that assumption, Inferred = Y, Exit reason Not stated, and state the assumption in one sentence in the Note. Use a later transition only where the filing shows that an unnamed member entered after the deadline or continued past it. A named party the filing shows entering late, or continuing, is handled on its own row and does not move the remainder.
>
> A named party that may belong to a group whose total the filing states stays inside that total: do not enter it again as an additional entrant; its own row records its later steps. Enter it separately only where the filing establishes it is outside the group.

And soften E3's two sentences to: "An NDA signed at some point in an interval does not by itself prove eligibility at a deadline inside that interval; for unnamed members, apply E14's ordinary-sequence assumption." Replace A2's check F.2 text only where it conflicts.

### What it changes in the trial outputs

| Setting | Mac-Gray residual | P&W residual | P&W named-party overlap |
|---|---|---|---|
| Opus medium | matches (Count blank) | matches | fine |
| Opus xhigh | matches exactly | Did not submit, 16–18 | would no longer enter G&W and Party B separately |
| Astra high | Dropped, 27 Aug → would change | Dropped, 16–24 → would change | fine |
| Astra xhigh | Dropped, 11 Sept → would change | Dropped, 16 → label changes | fine |
| Sol | Dropped, 27 Aug → would change | Did not submit, "at least 16" | fine |

**What this does not settle** (Alex, questionnaire 3.3(c)): whether an inferred non-submission is treated in estimation as a dropout or as censoring. The ledger's Inferred flag keeps both possible.

## 3. Joint diligence-and-negotiation periods (amendment A3)

**Source.** P&W, Party E's late-July LOI: "$21.26 per share (subject to a 60-day exclusivity period for due diligence and negotiation of definitive documentation)" (p. 30). Contrast G&W's LOI, which asked for three weeks of exclusive due diligence, and Party D's four-week diligence period: those are diligence periods.

**Current rule.** E12: H2 is "remaining diligence the filing reports as substantive, or a stated period of two weeks or more for remaining diligence"; "an exclusivity period, the time to signing or a negotiation period is not a diligence period". Example: "A request for several weeks of exclusivity; no stated diligence period → … normally Unclear."

**A3.** Add: "A single period requested jointly for diligence and agreement negotiations does not establish that diligence itself requires that period; apply H2 only if the filing separately supports substantive remaining diligence or a diligence period of at least two weeks."

**Trial.** Opus xhigh coded Party E Heavy (H2) on two rows and flagged it; four models coded Unclear.

**Consideration.** Alex's voice note 10 wants the Heavy flag for anything that "can materially affect the value of the deal or completion certainty". A 60-day exclusivity demand arguably does, but the ledger captures it separately (Exclusivity = Required, period in the Note), so it is not lost.

**Recommendation.** Approve A3. It makes the current text explicit and matches four of five models.

## 4. Company H: rule, date and reason

**Source (sTec pp. 29–30, 34).**

> 15 May: "Company H submitted a written non-binding indication of interest … in the range of $5.00 – $5.75 per share in cash."
>
> "Also during this time period [weeks of 13 and 20 May] … BofA Merrill Lynch contacted Company H and indicated that the price range Company H had submitted was not sufficient to move them forward in the process. The Company H representative was told that Company H could submit a revised indication of interest, which would be considered by the special committee."
>
> 16 May: "After the meeting … BofA Merrill Lynch sent final round process letters and a draft merger agreement to WDC and Company D."
>
> 23 May: "Company H remained interested in a potential acquisition … but … was not able to increase its indicated value range."
>
> June: "Company H had repeatedly stated it could not increase its price above the range of $5.00 to $5.75"; the committee judged a superior proposal from E, F or H "remote".

**Current rule.** E14: Dropped by target covers a target that "refuses it the next stage", but "neither is leaving a bidder out of one stage while the target keeps it in reserve or in continuing discussions" an exit. All five models read the invitation to resubmit as reserve status and coded H **Not selected at signing** (four with reason Would not improve earlier offer; Sol with Not stated). Alex's spring hand coding has H **withdrawing**. Your decision: **Dropped by target**.

**General rule to add (E14, after the reserve sentence).**

> Telling a bidder that its offer is not enough to advance, while leaving the door open to a better offer, is not reserve status: the bidder is Dropped by target when the stage proceeds without it. It is in reserve only where the target keeps negotiating with it or the filing describes it as a fallback or alternative. If it later returns with an offer the target entertains, record Re-entered.

**Date options.**

- **By 16 May (recommended).** The final-round letters went to WDC and Company D only, so the advancing set is complete without H. This is E14's existing "complete advancing set" transition and needs no new date logic. H is out before the final round opens, so the final round's live count is two.
- **Window 15–23 May.** This dates the rejection call itself, which the filing leaves undated within two weeks. The Sort date midpoint would fall on 19 May, after the final round opened, so H would count as live at the opening. That contradicts the substance of your decision.

**Reason options.**

- **Would not improve earlier offer (recommended).** E14 already says: "A bidder asked to improve that declines takes Would not improve earlier offer even where the target then chooses a rival." H was invited to improve and said it could not.
- **Lower offer than rivals.** The filing never compares H to rivals in those words.

**What to tell Alex.** His coding has H withdrawing. The handoff says not to leave this pending; a one-line note in the reconciled questionnaire ("we code the target's refusal to advance H as the exit; H's 23 May reply supplies the reason") is enough.

## 5. Analysis amendment P1

**The defect.** In the analysis tool, every Bid row sets `price_obs__same_price_as_new = 1`, and `price_obs__same_price_as_terms` is suppressed only when numeric prices match a previous row. Mac-Gray A's two October liability rows have blank prices and both flags equal 1, so an analyst filtering on the flags counts them as price observations (reproduced in `analysis-diagnostics/mac-gray/bids.csv`).

**P1.** Add a derived `upfront_price_kind` (point, range, lower_bound, upper_bound, not_available, invalid) computed from Price low/high. Set both price-observation flags to 0 when the kind is not_available or invalid. Keep every Bid row in `bids.csv`. Bump the analysis contract and tool versions. No workbook column or cockpit schema change.

**Fit with your decision 4.** You approved keeping the commitment events without presenting them as fresh prices, and said to fix the analysis contract "proportionately" without adding an extraction column. P1 adds an analysis output field, not an extraction column. The handoff notes you have not reviewed its specific fields.

**Recommendation.** Approve P1 as written. It is the smallest change that makes the blank price mean "no price observed here" to analysis code.

## 6. Retest and release

**Where things stand.** v1.13.2 is published and the default instruction; the v1.14 candidate is unpublished; the upgrade is undeployed; the Astra-high engine default is live. Only you can order an extraction, a publication or a deployment.

**Options.**

- **No retest.** Revise the candidate, run the offline checker and synthetic examples, then publish. This is fast, but the untested wording is exactly what failed to align five models before.
- **Three runs, Astra high, one per deal (recommended).** Mac-Gray and P&W test the cohort wording; sTec tests the Company H rule and the standstill condition. Each run took about 13 minutes on Astra high in the trial, and all three can run at once in isolated sandboxes. A second model would only be needed if you want to check that the wording, not the model, closes the splits; if so, add Opus 5.5 medium for six runs.
- **Repeat the fifteen-run sweep.** Not needed for a wording check.

**Acceptance for the retest.**

- Every cohort closure matches your four decisions.
- No named party is counted twice.
- Company H is Dropped by target by 16 May.
- The October rows have blank prices, and P1 shows them as not_available.
- The flags from decisions 1a, 1b and 1c appear where expected.

## 7. Is a confidential memorandum diligence access?

**Rule.** E12: "Not begun: the bidder had not yet had diligence access when it bid … Not begun needs affirmative support … an NDA alone does not show that diligence began." "Diligence access" is not defined.

**Trial.** Three contested rows, all P&W:

- Opus xhigh coded the nine May IOIs Not begun.
- Opus xhigh and Opus medium coded Party C's 12 July IOI Not begun.

(The Mac-Gray Party A 21 June "Not begun" rows are pre-NDA and uncontroversial.)

**Source.**

- For the May IOIs, the committee later allowed the seven advancing bidders "to conduct **additional** due diligence" with data-site access (p. 29), which implies some diligence had already happened.
- For Party C: "After executing a confidentiality agreement, Party C was provided the memorandum … On July 12, 2016, Party C submitted an IOI … Subsequently, Party C was provided access to the internet data site" (p. 29).

**Options.**

- **(i) Access means confidential company information under an NDA** (memorandum, management presentation, data site). Then all three rows are Incomplete.
- **(ii) Access means a data room or equivalent.** Then all three rows stay Not begun, except that the May IOIs sit awkwardly with "additional".

**Recommendation.** Decide yourself: (i). It is a definition, not a research estimand, and it matches the verification report (PW5). Tell Alex in one line.

## 8. What goes to Alex, and when

The handoff says not to send anything yet. Once decisions 1–7 are written into the candidate, the questionnaire needs these changes:

| Section | Status after your decisions |
|---|---|
| 3.1 Round maps (Decision 1) | Still Alex's. |
| 3.2 Counts given as ranges | The ledger default is now the ordinary-sequence count (your MG/PW rulings, option B). Reword the Mac-Gray example: it currently says "0 to 16 … missed 23 July". Alex still chooses what estimation uses. |
| 3.3(a) Primary Formality reading | Still Alex's. Your decision 1 changes which trial bids are Heavy or Unclear, so the agreement table should be recomputed after the retest. |
| 3.3(b) Same-price commitment changes as price observations | Settled by your decision 4. Remove, or replace with an FYI. |
| 3.3(c) Inferred exits as dropout or censoring | Still Alex's. Reword its Mac-Gray example to the settled coding. |
| 3.4 Company H | Settled by you. Replace with an FYI noting the difference from his hand coding. Penford Party A stays. |
| 3.5 Which source governs | Still Alex's. Note that the Company H and Party A examples are now decided by you. |

**Five items remain for Alex:**

- round maps;
- the estimation use of ranges;
- the primary Formality reading;
- dropout versus censoring;
- which source governs.

Add the Penford Party A reading, plus the FYIs on Company H and diligence access.

**Recommendation.** Send the reconciled questionnaire after the retest, so the Formality agreement table reflects the revised wording.
