# Instruction v1.11: contradiction resolutions

20 September 2026. Austin requested further polishing and resolution of the instruction's self-contradictions, using a team of Sol agents. The root read the supplied evening handoff and project guidance, commissioned four focused Sol reviews, edited the instruction, and commissioned a fifth Sol agent for an independent fresh read. The editorial reviewer also checked the changes against the starting v1.10 text.

This is a substantive consistency pass, not a claim of unchanged meaning. Where v1.10 admitted two implementations, v1.11 selects one explicitly. These resolutions are working conventions, not newly confirmed statements of Alex's research preferences.

## Decisions

| Issue | Resolution in v1.11 |
| --- | --- |
| Filename and sheet-order disagreement | Use `extraction/<deal>.xlsx`, matching AGENTS and the sandbox runner. Sheet order is Deal ledger, Rounds, Questions, Deal facts. |
| Required announcement forbidden after signing | C2 expressly permits the merger announcement and material events of competing post-signing proposals. C5's adviser coverage explicitly respects that limit. |
| Routine communication vs material events | C2 excludes routine contacts and drafts, with explicit access and reaffirmation exceptions. |
| Round 0 called a numbered round | Only rounds 1 and above have Round opened rows and Rounds lines. Round 0 and post do not. |
| Mandatory Questions vs uncertainty-only Questions | The map, each due-date round, and each late-reconfirmation sequence require review Questions even if clear. Other Questions follow the stated mandatory triggers or the material-uncertainty test. No alternative boundary need be invented. |
| Flags without Questions; multiple Questions per row | Each Flag links to Questions-sheet IDs, including mandatory review items. Multiple IDs are permitted. |
| Three process tests vs an unconditional example | All three C7 tests govern. A party not carried forward satisfies only test (a); it does not independently create a process. The two-month review trigger and three-month break test remain distinct. |
| Reused NDA excluded by the screen's definition | A qualifying agreement may be newly executed or expressly reused. Reuse can establish participation without a new NDA signed row. |
| One auction-screen cell for multiple processes and a go-shop | Report each process separately; for post-signing additions, preserve both its full-process result and pre-signing subtotal. Bounds can establish Met without inventing an exact Count. |
| One exit per person vs return and later departure | Track continuous periods of participation within each process. Same-process return after an exit uses Re-entered; a later process uses fresh entry. First contacts are likewise scoped to each process. |
| Termination/lapse leaves participants without an exit row | Process terminated closes remaining participation collectively. After a lapse, Process restarted identifies unresolved closures in the earlier process. Neither closure gets duplicate individual exits. |
| Group changes break live-bidder arithmetic | Identify units before and after the change. Count the resulting live units and state the net change; do not duplicate that membership transition with exits or re-entry. |
| Disappearing named party vs anonymous residual | A proven named residual member can get its own exit, subtracted from the cohort. Uncertain membership stays in the intact cohort with an explanation; the signing fallback cannot close it twice. |
| Lower bounds or estimates cannot occupy exact numeric Count | Leave Count blank and preserve the qualifier in Who and a `Count:` explanation in Note. Reconcile bounds as bounds. Repeated bids and NDA instruments are not additional entries. |
| Exact inferred-exit dates vs “by” evidence | Inferred exits retain supported bounds and use the transition as their sorting anchor. An assigned Sort date is not promoted into a reported event date. Separate evidence may supply a lower bound. |
| A quarter described as both endpoints and ninety days | Use actual quarter endpoints, calendar unless the filing identifies a fiscal quarter. Calendar quarters do not have a uniform 90-day length. |
| First undated row has no preceding Sort date | Use the first dated event's sort key, or the filing date solely as a sort key if no event is dated, explaining the latter in the map Question. Event-date bounds remain evidence-based. |
| Deadline reached and subsequently extended | Keep the reached Deadline row and use Extended when a later due date revises the same round; that outcome takes precedence over intervening evaluation. |
| Superseded/future dates forced into event rows or outcomes | Keep them in Due dates with annotations; no Deadline row or outcome until reached while operative. No dates set means No deadline stated; dates set but none reached means a blank outcome with explanation. |
| Go-shop has a label but no round mechanics | An organized go-shop opens the next numbered round in the same process unless C7 establishes a new one. Round opened records its start; Go-shop changed records later changes/end. The period's expiry alone is neither a bid deadline nor proof that all participants exited. |
| Universal closure fabricates post-signing departures | Apply the supported closure rules first. Participation still unresolved at the source cutoff remains open; never close a new post-signing entrant at an earlier signing. |
| Late reconfirmation can be backdated | Use the first bidder act for which all three C12 tests hold. The returned-draft route is explicitly distinct from ordinary express confirmations. |
| Conditions categories overlap; continuation is ambiguous | For an individual bid, apply Heavy, then None, then Light, otherwise Unclear. Differing cohort conditions remain Unclear. Carry-forward needs reported continuation, except for C12's returned-draft rule. Narrative-only open diligence has the stated Unclear treatment. |
| Undefined consideration value and package-price placement | Define All cash = Not stated. A reported per-share package value is the total bid value, with components and attribution in Note; no conversion from enterprise/equity totals is invented. |
| Required evidence cannot always fit 40 words | Forty words is a target. Required details may exceed it when references or shorter wording cannot preserve them; the checker flags the excess for review. The 30-word exact-quotation limit remains. |
| One act needs a boundary marker and a substantive row | B1 and C7 explicitly permit separate required process/round markers alongside a coincident Bid or Target sale decision, without duplicating entry. Existing go-shop/deadline combinations remain explicit exceptions. |

Other polish: name the actual Excel date columns; preserve When as text; define entry, live and admission; specify consecutive Q IDs; explain how a single exact quotation anchors an inferred row; make the delivery checklist use the same conventions as the body. Other-scope price changes retain the Other-scope bid label.

## Protected decisions

- The first price paragraph of C15, including the unapproved Q3 one-sided-price convention, is unchanged from the starting v1.10 text.
- The four C16 exit-label definitions and the Q7 sentence assigning Would not improve earlier offer are unchanged. The proposed Company H continuing-invitation exception and revised exit reason were not adopted. The original winner-selection wording for a reported Not selected at signing was retained, with timing made explicit.
- The three-month process threshold and two-month review trigger are preserved.
- The prior decision not to restore the redundant standalone “Do not infer Heavy” sentence remains in place.
- All 30 event labels, the four-sheet schema, column orders and Deal facts fields are preserved. Some labels' usage is now explicitly governed, particularly Go-shop changed and Process restarted.

## Verification

- Five Sol agents reviewed the instruction: participant lifecycle/counting; rounds/deadlines/dates; schema/evidence contract; editorial clarity/meaning drift; and an independent fresh reader. The fresh reader found one remaining structural-marker collision; after its repair, a targeted follow-up found no actionable issue in the affected rules. The editorial reviewer's targeted follow-up likewise confirmed its findings closed.
- Programmatic checks matched ledger, round and question columns against the checker, confirmed the unchanged Deal facts definition and 30 event labels, resolved all B/C section references, and checked the protected Q3/Q7 text and both time thresholds against the starting snapshot.
- `python3 -m unittest discover -s _dev/tools -p 'test_*.py'`: **17 tests pass**, including four new tests covering qualified Count versus accidental omission, required long Notes, future versus reached deadline outcomes, and unknown auction-screen counts. Jev tests use their existing mocked fixtures; no live model check or extraction was run.
- `git diff --check` passes.
- Checker v1.2 accepts the new representational cases while retaining errors for unexplained missing bidder Counts and missing reached-deadline outcomes. Long Notes and documented uncertain Counts remain review warnings, not assertions that the substance is correct.

The starting v1.10 instruction had SHA-256 `75a490bd3850a7064e64984e186fea87ec27af15bb01709597245163315d78e6` and 6,871 whitespace-delimited words. The final v1.11 has 8,421 words and SHA-256 `f41f43dcf991011743fb9143e60b22e19b5a86e9f70bb8c823e23de70c2688aa`. This pass adds explicit rules where the earlier draft left gaps; it is not a shortening exercise or a repeat of the earlier 551-rule preservation audit.

## Limits and next validation

No filing or real workbook was read for this pass. No extraction or workbook revision was run, and nothing was committed or pushed. The existing v1.8 workbooks still lag the instruction. Instruction review and synthetic checker tests do not establish extraction accuracy.

The research questions already awaiting Alex remain provisional: process boundaries, Company H and related round mapping, formal-offer timing, the WDC interpretation, and final-round admission. This pass gives internally consistent working rules; it does not settle those empirical disagreements. The next behavioral validation remains a separately authorized isolated extraction trial.
