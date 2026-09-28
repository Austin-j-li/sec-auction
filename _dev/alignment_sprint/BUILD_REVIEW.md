# Version 1 build review and fix list

28 September 2026. Four independent, read-only Claude Opus 5.5 reviews of the Codex build (`378b94b`, BUILD_REPORT.md): instruction draft, source application (round map and workbook check), checker and analysis tools, and cockpit/fresh state/runbook. Each finding below was reproduced or checked against the source by its reviewer. No blocker was found in the draft or the reports; one was found in the checker. The live app, its state and services were not touched; no extraction ran.

Test reruns: full `_dev/tools` Python tree 358 passed (229 subtests); cockpit Python 148 passed; vitest 77 passed; core browser suite 63 passed; a scratch `vite build` is byte-identical to the committed `dist/`.

The fix pass applies the 28 September rulings (DECISIONS.md) and the items below, then stops for re-review. Publication, switch-over and any extraction still wait for Austin.

## 1. Rulings to apply (DECISIONS.md, 28 September)

1. Missed due date: replace E14 l.326's first two sentences, drop the D2 l.93 "missed due date by a bidder that continues" event and the D3 l.117 clause; checker, review queue, ROUND_MAP (Kraton J June 29) and WORKBOOK_CHECK follow.
2. Finality resets after a (d) restart: E6 (c) wording; derive/checker round logic; ROUND_MAP Synacor P3 round 4 January 6, 2021.
3. Financing: remove the precedence clause at E12 l.288 and reconciliation 16; checker if it encodes it.
4. Round 1 dating: E6 l.189 wording (a period counts from its start; undated fallback chain); ROUND_MAP Penford August 28, 2014 and Synacor May 8, 2018 / August 25, 2019 / July 13, 2020.

## 2. Instruction draft

Should fix:
- **S1.** Restore the scope guard dropped from C l.39, limited so it does not suppress Part F: "Outside Questions and Review items (Part F), add no alternative codings, extra rows or commentary."
- **S2.** l.261/l.28 (copy the earlier row) conflict with l.265 (code conditions at that time) for a confirmation-by-documents row. Say that row copies the price only and codes its condition columns from its own window (DECISIONS F2: "conditions as the filing shows").
- **S4.** l.191 and l.195 overlap (a Datalink-type request could carry out round 2 and lose round 3). l.191: "Its own first request for offers to all the admitted parties carries it out …".

Minor:
- **M2.** (d) l.201 dropped v0's "with one bidder"; say continued talks with the former exclusivity holder are not a renewed approach.
- **M3.** l.133 initiation: "activist-influenced only if" should be "if".
- **M4.** Example 3 (l.357–358) should show P3's "not invited" Note.
- **M5.** Add to CHANGE_MAP's wording-edit list: E13 l.317 (dropped "made after closing … whatever the filing calls it"), E10 l.267 (dropped "only where the filing presents it as a proposal, offer or indication"), E3 l.165 (dropped "its Count is the filing's total minus those named rows"). Restore any that was not intended.
- **M1.** F7 said sTec June 20 "becomes a Review item"; no O1 category covers it. Use an existing category if one fits; otherwise let it lapse (no new category for one deal).

Kept as drafted (settled by DECISIONS; no ruling needed): Part C reread (DRAFTING_SPEC:72, test later); mixed-initiation Note (P5); Route 2 timing (evening ruling 3, F1); F2 "Same as #n" names the latest price-stating offer; Penford A's spells (below).

## 3. Round map and workbook check

Should fix:
- **sTec E and F are whole-company entrants**, not partial-only: "In total sTec executed six non-disclosure agreements related to the exploration of a potential sale of the company" (p.27) includes E (April 4) and F (April 11); both later switched to "limited, select assets" and so Withdrew (E1 l.145). Only C is partial-only. Fix ROUND_MAP:64 and W09; the auction has 6 parties, not 4.
- **W42** cites a "June 14" outreach date; the filing says "Later in June, Raymond James also contacted 14 financial sponsors". 14 is a count.
- **Synacor CLP's January 21 initial merger draft** came after definitive negotiation began January 6: under F2 it is a dated confirmation by documents, replacing the bounded row.

Minor:
- sTec D's April 23 "a price greater than $5.60" is a floor, not a ceiling (WORKBOOK_CHECK:147); Alex's 5.6 lower bound is right.
- W47: PetSmart's six indications are dated exactly October 30; only Bidder 2's revision is bounded.
- W34: Synacor AB612 (December 29) matches a real reaffirmation; the workbook lacks the December 8 letter, it does not misdate.
- Kraton (ROUND_MAP:62): "late submissions considered by July 2" is unsupported ("By July 2, 2021, Kraton received four indications"); "A is rejected September 26" is not an exit, A is Not selected at signing September 27.
- W23: H counts among the 14 signers under P1; not an open question.

Settled alternatives (apply, no ruling needed): Penford A Dropped by target October 3 (not invited), Re-entered October 4, Not selected October 14; Mac-Gray September 18 deadline Enforced (September 21 answers the target's own exclusivity condition); Datalink C Dropped by target October 26 (October 20 is an information-access row); Providence latest late arrival Extended, bounded May 20–June 1; Synacor processes by ruling 4.

## 4. Checker and analysis tools

Blocker:
- **`check_lean.py:820-822` `round.zero_after_opening`** errors when a round-0 bidder's opening-caused exit follows the round-1 Round opened row, exactly the order E8/R7(c) and E14 rule 1 require. Exempt exit rows; add a round-1 test mirroring `test_opening_live_is_after_same_day_exits_in_previous_round`.

Should fix:
- **`check_lean.py:885`**: an Other-scope alternative in the same communication ends the signer's live status, so a correct signing Count 1 errors. Use derive's rule: a party is outside the contest only if every bid is Other-scope or it Withdrew to partial.
- **Initiation** depends on Round opened's Who matching Deal facts Target exactly, and checker and derive disagree (`check_lean.py:1832-1838`, `derive_analysis.py:750-768`). Treat the first round-1 Round opened row as the target's step in both.
- **Formal bid coded Unclear** where E12 requires None passes silently (`check_lean.py:698-711`). Add a warning.

Minor: signing row with Who = target passes; process Question after an inferred round (Inferred = Y) not required; R items whose Rows affected mix rows and an omitted event are not parsed; signer identity compared exactly while derive strips parentheses; `review_list.py --output` lacks derive's path guard.

## 5. Cockpit, fresh state and runbook

Security (affects the live app now; fix separately, on Austin's order):
- **`server.py:74-83`** trusts `Cf-Access-Authenticated-User-Email` whenever `Host` equals the public origin and never verifies Cloudflare's signed token. A local process sending a forged Host and Alex's email got his identity, edit rights and CSRF token on a scratch server; it could start paid runs on either subscription. Verify `Cf-Access-Jwt-Assertion`, or require a secret header only cloudflared adds.

Should fix:
- **SWITCHOVER.md:36** drain query omits `timed_out` (`worker.py:68`), so past timed-out jobs look outstanding forever.
- **Export after the switch**: `export_repo.py:188` reads and writes the same `--repo-root`; with state in `ledger-live` it would write into the running deploy folder. Add a separate output folder or a runbook procedure.
- **Backup prune** (`backup.py:310`, 14 days) in the shared `~/backups/ledger-cockpit/` will delete the old app's nightlies; the `version-1-*` pre-switch backup survives. Separate folders or exclude the old pattern.
- **Version 1 attribution**: seeded as "system" (`instructions.py:105`, SWITCHOVER:116) against BUILD_SPEC B5 ("Austin publishes Version 1 … under his account"). Austin to choose.

Minor: `fresh_state.py:63` `mode=ro` open creates `-wal`/`-shm` in the old state folder when no connection holds it; the Version 0 check comes after seeding and has no recovery step; `npm ci`/build run during the outage (do before, or check `dist/` hashes); no `mkdir -p` for the worker and backup drop-in folders; hidden deals reappear (say so); cloning an R review item assigns a Q id (`main.jsx:524-527`); about 6 MB of `/tmp/cockpit-*-acceptance` evidence left on the near-full disk.

Checked and sound: fresh state's read-only copy, retained tables, filing hashes, no credential access and atomic no-replace install; first-import base under out-of-order completion; runbook order and rollback; path containment, slug/ID patterns and bound SQL.
