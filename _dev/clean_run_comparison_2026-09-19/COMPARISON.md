# Clean-run comparison: full vs v1.5 vs v1.8 (19 September 2026)

**Setup.** Three instructions (full 13,618 words; v1.5 short form 11,713; v1.8 lean 5,493), three deals (Providence & Worcester, Mac-Gray, PetSmart), two runs each = 18 sessions. Same model and setting as Austin's runs (DeepSeek flash, max). One session per deal, each inside a bubblewrap sandbox that exposes only its own folder: the instruction and the one filing. No git history, no `ref/`, no audit folders, no checker, no shared temp folder, web fetch denied. A scan of every tool call found no outside or web access. One session (full, Providence, run 1) was cut off by the harness mid-task and resumed in the same sandboxed session. Total API cost about $3.30.

**Scoring.** One scoring agent per deal, candidates under neutral labels, fixed rubric (`score/RUBRIC.md`): the filing is ground truth, Alex's hand rows and voice notes say what he wants, and any disagreement with his rows was checked against the filing first. Mechanical metrics, quote checks and structure tables are scripted (`score/*.py`, `score/*.tsv`).

## Result in one line
On the facts the research uses (bids, prices, formality, NDA counts, live bidders per stage, order) the three versions cannot be told apart: differences between versions are no larger than differences between two runs of the same version. v1.8 gets there with a third of the text to review.

## Scores (0 to 10, "how close to what Alex wants")

| Deal | full run 1 / run 2 | v1.5 run 1 / run 2 | v1.8 run 1 / run 2 |
|---|---|---|---|
| Providence | 8.5 / 7.3 | 7.6 / 6.8 | 7.1 / 6.5 |
| Mac-Gray | 6.5 / 6.0 | 7.0 / 7.5 | 8.0 / 9.0 |
| PetSmart | 7.0 / 8.5 | 5.0 / 6.5 | 7.5 / 8.0 |
| Mean, all three | 7.3 | 6.7 | 7.7 |
| Mean without Providence | 7.0 | 6.5 | 8.1 |

Two runs of the same version differ by up to 1.5 points, so a gap under about 1 point is noise. No version is untouched by these deals: the full instruction contains worked examples taken from Providence, and v1.8 was written by an agent that had just studied this model's output on all three deals (its "tighten dates before sorting" paragraph and its re-read for advisers answer failures seen on PetSmart). Read the last row with that in mind; it does not overturn the one-line result.

## Totals over six ledgers per version

| | full | v1.5 | v1.8 |
|---|---|---|---|
| Priced bids missed (of 72) | 3 | 2 | 2 |
| Spurious bids | 0 | 0 | 0 |
| Ledgers with the wrong number of rounds | 2 | 4 | 1 |
| Serious factual errors | 1 | 3 | 0 |
| Minor factual errors | 13 | 18 | 8 |
| Omissions Alex would want | 1 | 4 | 5 |
| Rows Alex would delete | 50 | 40 | 29 |
| Ledger rows, average | 53 | 51 | 47 |
| Words per row | 151 | 162 | 52 |
| Rows flagged for review | 80% | 85% | 28% |
| Model-made copy of the filing | 6,000 to 14,000 words | same | none |
| Quotations found in the filing | 94 to 100% | 83 to 100% (the 83% run is partly my checker counting source-id strings as quotations) | 94 to 100% |
| Minutes per deal / cost per deal | 18 / $0.21 | 18 / $0.21 | 12 / $0.13 |

Identical in all 18 ledgers: NDA totals (26, 20, 15), zero order inversions among bids and exits, zero invented bids, the same formal/informal labels (all three versions label heavily conditioned mark-up bids Formal + Heavy where Alex's hand rows say Informal; his own mapping rule recovers his label).

Format: one v1.5 Providence run stored every date as text and has a malformed Summary formula, which a reviewer sorting by date would hit at once. Six of the twelve full and v1.5 workbooks fail the fixed Conditions detail format because the filing states diligence periods in days. The date-labelling failure seen in the earlier contaminated batch did not recur in any clean run.

v1.8's five omissions: the re-entry rows for Parties D and E in both Providence runs (one issue, counted per run), Party B's 4 August row in one run, the 29-party contact wave in one run, and one bidder left without its own row in PetSmart.

## Differences that held in both runs (so probably real)
1. **v1.8 has no re-entry marker.** In Providence both v1.8 runs close Parties D and E, show their later bids, then close them again. The prose and the Rounds sheet give the right live count, but counting entry and exit rows gives the wrong one. Dropping the "Re-entered" label was a cut too far; restoring it costs one line.
2. **v1.5 opened a spurious third round in PetSmart, both runs**, at the November process letter, so every final bid carries round 3 instead of 2. Full and v1.8 did not. The trigger is the sentence "the target's first request for final offers also opens a round", which all three versions contain.
3. **All versions over-split Mac-Gray**: five of six runs add a "round 4" when the committee selects CSC/Pamplona and moves to exclusivity. Only one v1.8 run gives Alex's three rounds. The runs cite the rule that does it: "a new round begins when the target ... moves to definitive negotiation with selected bidders". That clause fires before the exception ("exclusivity inside an established final stage is not a new round") is considered. It is a conflict between two sentences present in all three versions, not a length problem.
4. **Full is best on Providence, and that is partly taught.** Party B's 4 August reconfirmation row, which Alex asks for by name, appears in both full runs, no v1.5 run and one v1.8 run. The full instruction carries a worked example of exactly that row.
5. **Review burden.** v1.8 ledgers: about 360 characters per row, a quote and page on every row, a quarter of rows flagged, a one-screen Rounds sheet whose first question is the open round call. Full and v1.5: over 1,000 characters per row and most rows flagged, so the flag points nowhere.

## Not resolved by any version
PetSmart round 1 lands on 1 or 4 October (Alex: 3 October; he bounds the NDA wave to 3 to 7 October); Party A's exit round in Providence varies run to run; whether Party D is out on 2 August varies. These are the open convention questions for Alex, not prompt-length effects.

## Caveats
Two runs per cell, one mid-tier model, three deals on which the rules were developed, an AI scorer (blind labels, but layout gives the family away, and the 0 to 10 score includes review burden, which favours v1.8 by construction). The component rows above do not depend on that.

## What v1.8 suspends from decisions Austin already made, and what the test says about each

| Austin's decision (in full and v1.5) | In v1.8 | What these runs show |
|---|---|---|
| Re-entered and Participation paused labels | Dropped; a return is just a new Bid row | Against the cut: both v1.8 Providence runs close D and E twice. Restore Re-entered. |
| Mandatory Questions coverage (kept by name in v1.5) | Replaced by "flag only open calls" | For the cut: full and v1.5 flag 80 to 85% of rows and every scorer said the flag points nowhere; v1.8 flags 28% and its first question is the open round call. |
| Date basis and Date method columns | Dropped; Sort date, Date from, Date to kept | No evidence either way: the pairing failure did not recur in clean runs, and order was perfect in all 18 ledgers. Only the "ceremony" argument remains. |
| Outcome basis values (Stated / Inferred: residual, exclusivity, silent, identity) | One Inferred flag plus a plain note | Not isolated. Every signer was closed once in all versions except the v1.8 re-entry case. |
| Conditions detail string | Dropped; level plus plain words in the note | Level assignments were the same across versions; the fixed string failed format in 6 of 12 workbooks. Alex asked for a flag only. |
| Count-0 identity row for a named party that vanishes | Dropped; note in the residual row plus a question | Mixed: full and v1.5 place Party A in a round (twice in Alex's round, twice in the round he rejects); v1.8 leaves it open as a question. |
| Information-access rows as their own label | Folded into "Other material event" | Not isolated. Scorers listed some access rows among rows Alex would delete, in every version. |
| Model-made Source text sheet | Dropped; quote and page on every row | For the cut: quotation accuracy was the same, with 6,000 to 14,000 fewer words of output. |
| Self-check reporting, baseline sheet, examples (already cut in v1.5) | Absent | v1.5 lost the 4 August row that the full version's Providence example teaches; otherwise no visible effect. |

## Recommendation
The decision rule fixed in advance in the audit was: adopt the lean version if it matches on the facts within run-to-run noise and halves the review cost. It does both. So v1.8 is the better base, with the calls in the table above as Austin's to make, not mine. Patches indicated by the test, for whichever base is chosen: restore "Re-entered" (v1.8); resolve the round-rule conflict so that selecting a winner or granting exclusivity after a round opened as final ends that round instead of opening another, and a process letter inside that round opens nothing (all versions); accept days as well as weeks wherever Conditions detail is kept (full, v1.5); pin the quote-cell format (v1.8). Then test on deals the instruction has never seen (Penford, sTec), which needs those filings.

Files: `instructions/` (the three texts), `run1/`, `run2/` (18 run folders with logs), `score/deals/<deal>/{reference.md, scores.json, scoring_notes.md}`, `score/combined.json`, `score/metrics.tsv`, `score/structure.tsv`, `score/quote_check.tsv`, `score/format_check.txt`, `score/label_map.json`. Rerun with `./launch.sh <runset> <variant>`.
