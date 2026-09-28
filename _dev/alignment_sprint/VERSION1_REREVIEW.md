# Version 1 re-review: duplication, overengineering, instruction following, confounding facts

28 September 2026, at `b9be68f`. Five independent, read-only Claude Opus 5.5 reviews:
- duplication;
- overengineering;
- fidelity to DECISIONS;
- followability, by a reader given only the draft and the filings, who tested nine real passages;
- confounding facts.

No repo edits and no ledgers. Protected files are unchanged and nothing was deployed. All seven examples follow the rules. Every filing quote the reviewers checked is correct.

Legend: **A** = Austin decides; **M** = mechanical fix under existing rulings; **E** = engineering simplification.

## 1. Rule defects found independently by more than one lane

| # | Issue | Lanes | Fix | Type |
|---|---|---|---|---|
| 1 | E9 "Extended: a later due date was set for any bidder" also fits the next round's own due date. Literally, sTec May 28, Mac-Gray July 23 and September 9, and Kraton June 29 would all be Extended; ROUND_MAP silently reads it narrowly. | followability, facts | "a later due date for the same request, set before the target acted on the bids in hand; a new round's due date is not an extension" | A |
| 2 | Late-bid verb: E9 says "considered", E14 event 3 says "takes", re-entry (l.336) says "entertains (responds to or considers)", and the label and D3 say "accepted". The same bid can come out as no exit or as exit plus re-entry. | duplication, followability, fidelity (checker message) | One verb everywhere, defined: "the target considers it: replies to the bidder about it or its board discusses that offer; a briefing on communications is not enough" | A |
| 3 | "Gives it more time" is undefined (sTec D May 31; Synacor H September 22 "encourage it to submit a proposal"). | followability, facts | "asks or allows it to bid after the due date, before the next round opens". Synacor H then never leaves before the September 23 exclusivity (Dropped by target there). | A |
| 4 | A.3 (l.16) still describes Formality as the Version 0 two-route test; routes 2 and 3 now reach further. | duplication, facts | A.3 points to E11 (documents, final round, definitive negotiation) | M |

## 2. Instruction-following gaps (literal reading gives two codings)

| # | Issue | Fix | Type |
|---|---|---|---|
| 5 | sTec WDC June 14, the winning bid: "fresh final-round invitation" is undefined, so it can be read Formal or Informal. | "An invitation to a returning bidder is any request for an offer the target makes to it while a round announced as final is open." WDC June 14 is then Formal, matching Alex. | A (recommend) |
| 6 | Finality is defined after its uses and timed ambiguously. sTec May 16's letters are called non-binding only later, so rounds are 2 or 3; Datalink August 16 is circular. | Move Finality before the triggers; "wherever the filing so describes the request"; judge finality as it stood before the request being tested. This keeps sTec at 3 (R4 ruling). | M |
| 7 | E6 l.191 opens a round at a selection decision even within or after a final round (conflicts with l.195/199/205). | Add: "Such a decision opens nothing within or after a round announced as final, except under (c)." No anchor changes. | M |
| 8 | l.191/195: "all the admitted parties" should exclude parties whose withdrawal was already reported (R1). | "…still eligible" in both | M |
| 9 | An interval-dated opening (Providence, between July 22 and 27): Sort date = Date from conflicts with "when in doubt the round continues". | An opening dated only to an interval sorts at Date to. | M |
| 10 | (d) "solicited none" is undefined (Synacor October 27 → December 18). | "Outreach carrying out an opened round counts as soliciting." This follows evening ruling 1 and the R3 guard. | M |
| 11 | An entrant that turns partial without ever making a whole-company bid (sTec E/F, Kraton K) has no exit rule. | "An entrant that turns partial Withdrew at the turn, whoever ends talks." This matches the fix pass's sTec E/F. | M |
| 12 | Same-offer copy (l.261) keeps Unclear on a row that becomes Formal (F5). | "Formality by E11, Conditions by E12" | M |
| 13 | A closing condition in a markup (Datalink Insight's continued employment): H3 or routine drafting? | A closing condition in a markup is not H3 unless the bidder says it will not proceed without it. | A (recommend) |
| 14 | "Other securities count as stock" and the CVR definition collide (Mac-Gray B's performance-vesting options). | A security whose payout depends on performance is CVR/earnout (F10). Matches W46. | A (recommend) |
| 15 | Undefined edges: Kraton's "July 19, 2020" typo date; undated postponements vs "superseded before it arrived"; Providence's unnamed seven for "admitting named parties". | Short defaults: use the evident date and Note it; a postponement reported without a date counts from its report; "named or counted parties". | M |

## 3. Duplicates with differing copies (collapse to one home)

- Go-shop: D2 l.101 says every go-shop opens a round, but E6 l.209 requires reported solicitation. Point D2 to E6.
- Live-end: E3 l.161 omits "the win". Make l.338 the one home.
- Cohort rules: P1 (l.167) and P2 (l.169) conflict on entrant totals. Start l.169 with "Apart from entrant totals (above)". This keeps both decisions.
- Conditions window (B l.28) should also end at a process-only request (E10 l.257). D2 l.93's closed list should add "a bidder's acceptance of or counter to a target requirement, or a process-only request (E2, E10)".
- Note prefix order: D1 l.71 against E3 l.171.
- Count on process markers that close nothing: blank.
- F l.383 "touches" should read "names" (as D4 and the checker have it).
- Agreeing duplicates to collapse:
  - required exclusivity makes Conditions at least Light: A.3, E12 and l.307;
  - confirmation-by-documents copying: B l.28, l.261, l.265 (home l.265; B returns to "Only a Same-offer row copies an earlier row (E10)");
  - "Same as #n": home D1;
  - partial-only gets no exit: home E1;
  - an exit keeps its round: home E8;
  - an uninvited bid keeps the round's number;
  - valuation statement without an offer (D2 → E10);
  - D2 l.100 repeats D1 l.47;
  - F l.387 repeats D4.
- Delete as redundant:
  - E12 None's repeated clauses;
  - E13 l.311's ceiling sentence (E10 covers it);
  - E11 l.275's "A later final announcement does not qualify an earlier bid" (F1's "judged at the bid's communication" covers it).
- Restore O8's "under the same rules".
- Financing wording (ruling 3): add "or that financing is still being arranged" beside "lacks firm or committed financing", so Datalink C's "still exploring third-party financing" is Contingent as ruled.

## 4. Tools

- **Checker initiation bug:** it counts any round-1 opening as the target's step. A round 1 opened at the first NDA with an approaching bidder is not target-opened (D5). Follow D5.
- **`exit.late_bid_in_round` message** contradicts l.336 and assigns an E9 outcome. Replace it with a pointer (E14 closing event 3; E9). Warn only on a same-round Re-entered row, or a same-round Bid when the outcome is Extended (late bid accepted).
- **E: Signing Count check** (`check_lean.py:939–990`, `1447–1463`): replace the reconstruction of who is live with: error unless Count is blank or 1; warn on blank with a whole-company Bid, or on 1 with only Other-scope bids. This removes the drift from derive (T1).
- **Count-note parsing:** derive's `count_bounds` misses six qualifiers and number words ("Count: more than ten" returns unknown). Parse through the checker's regex.
- **E: `access.py`:** let `jwcrypto` check iss/aud/exp; one cached key set, refetched only on an unknown key (at most once a minute).
- **E: `export_repo.py`:** require `--out-root` with `--write`; drop the Git detached-HEAD probe.
- **E: `fresh_state.py`:** take a `backup.py` backup folder as input; stage into a `.partial-` folder and rename; keep the filing hash checks.
- **E: `deal_bases` table:** delete it. The first version by rowid is the first import, and versions are never deleted.
- **E: `review_list.py`:** one deal-level currency/units item instead of one per bid row; drop `--output`.
- **E: SWITCHOVER:** check the frontend build once at approval; at switch-over, confirm only that `dist/` is clean in git.
- **E, optional:** drop the catalog `filing` blocks and `verify_catalog.py`. They duplicate MANIFEST.csv now that the catalog holds no versions.

## 5. Stale or contradictory records

- **BUILD_REPORT's 27 September body** is superseded by its fix-pass section: old SHA and counts, Penford September 1–9, Synacor three rounds, W01–W47, W02 July 6, W34, and Synacor January 21. Mark it superseded or update it.
- **CHECK_REPORT:** test totals, "approval items", and the date.
- **Link counts:** 247 links to 101 lines, not 241; 88/84 changed lines, not 87/83.
- **CHANGE_MAP:** l.53 and l.254 should point to L332.
- **DECISIONS:** add supersession notes at l.81 (Kraton J), l.111 (Synacor December 30) and l.143 (sTec June 20).
- **WORKBOOK_CHECK:** W02 and W32 contradict each other on AB119.
- **Kraton J's July 19** is "by July 19" (p.36), not exact. Fix it in DECISIONS, ROUND_MAP and BUILD_REPORT.
- **Filing readings to fix in ROUND_MAP:**
  - sTec D's April 23 verbal indication is a Bid. Check whether it answers the May 3 request, which was sent April 23/26.
  - Re-entry is dated at the target's invitation, consistently. Synacor CLP re-enters by December 18–21; Providence D/E at the July 29 calls.

## 6. For Austin to confirm (settled by reviewers rather than by a ruling)

- Penford Party A: Dropped by target October 3 (not invited), Re-entered October 4, Not selected October 14. This is the literal E14 result; evening ruling 2 fixed only the October 14 exit.
- F7's sTec June 20 Review item lapses, with no new category.
- "Same as #n" names the latest priced offer (reconciliation 19). The mixed-initiation Note goes on Deal facts' Initiation.

## 7. Publication step (after approval)

- AGENTS.md, README.md and _dev/STATUS.md describe Version 0 and the laptop recovery branch.
- STATUS.md l.51's same-offer rule must change (F2; DECISIONS l.187).
- Also update `_dev/tools/README.md` l.3 and `_dev/COCKPIT_APP_SPEC.md` l.3 and l.192, which DRAFTING_SPEC §10 does not list.
- Until publication, `sandbox/run_model.py` defaults to the Version 0 root instruction while the checker enforces Version 1. No extraction should run on `version-1` before publication.
