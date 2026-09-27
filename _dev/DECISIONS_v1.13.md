# Instruction v1.13–v1.13.2: the objective-led rewrite and E6 clarifications

21 September 2026. Austin's decisions; Alex Gorbenko was out of reach, so conventions remain provisional.

v1.13 is 5,569 words against v1.12's 8,645. The workbook format is unchanged: four sheets, 22 ledger columns, the same labels and values, so the checker and cockpit read v1.11, v1.12 and v1.13 workbooks alike. The tested v1.12.1 text is commit `f89170c`. Earlier records: `git show 3216a85:_dev/DECISIONS_v1.12.md` and `git show 59e2325:_dev/DECISIONS_v1.11.md`.

## Decisions

| Decision | What changed |
| --- | --- |
| Change the instruction only where the change is general; never add a rule justified by one reviewed deal. | Governs everything below. |
| Replace the rule list with an objective-led text. | Parts: A what the ledger is for, B the evidence standard (reported, marked inference, or empty), C how to work (five steps, each with a finish condition), D the workbook, E fourteen fixed conventions, F questions and delivery (four checks). Section names change from C1–C16 to E1–E14. |
| Keep a convention only where two careful readers could choose differently; delete what judgment reaches from the objective. | Deleted: the confidentiality-agreement taxonomy, the supporter-closure rule, the renamed-bank rule, most of the process case list, deadline-precedence detail, the go-shop closure paragraph, Note-prefix formatting. Kept because the checker reads them: the "Count: at least 11" note form, "at least"/"no more than" price markers, the auction-screen value form. |
| Late reconfirmation shrinks to two sentences. | Record a reaffirmation only when the bidder acts; never to supply a formal bid that seems missing. |
| Processes keep the three continuity tests and drop most of the case list. | E5. |
| A round is one request for offers. | E6: the target asks a set of bidders to submit offers on common terms, and the round runs until that request is resolved. Bargaining over an offer already made (a counter, a request to improve or to name one price, exclusivity, documents) belongs to the round that offer answered, however many bidders remain. This follows Alex's collection instructions §3.6–3.7: rounds follow what the target does. |
| **v1.13.1: E6 opening repaired, then frozen.** v1.13's E6 said both "a new round begins with each new request" and "a request to improve a price stays in the round." Those competing triggers warranted clarification; observed extraction differences did not establish which wording caused a model's choice. | A round is a stage of the sale and runs until the target changes the stage or the set of bidders. Asking the round's bidders to improve, once or repeatedly, with or without a new deadline, continues the round. The residual finality-sentence ambiguity was subsequently removed in v1.13.2, with Austin's approval. |
| **v1.13.2: one-sentence E6 clarification, approved 21 September.** | Replace the finality paragraph's duplicate round-opening trigger with the sentence recorded below. Preserve the earlier first-final-request and repeated-improvement rules. No other instruction content changes; freeze the text for unseen-filing testing. |
| v1.12's seven edits carry over. | The honesty sentence, whole-background reading with annexes, the paragraph-by-paragraph reread, the exact-value support check, exact-subtraction examples, and finality describing the round as the target ran it. |

At the time of this rewrite, Q3 (one-sided prices) needed no text change and Q7 (Company H continuing invitation) remained unadopted. **Status correction, 22 September:** Austin confirmed that Q3 and Q7 are no longer withheld. The earlier disposition is historical and must not be presented as a current approval hold. His clarification does not restate a replacement coding treatment or establish that workbook corrections were implemented; see the current [research-question record](RESEARCH_QUESTIONS.md).

## Evidence and its limits

The rewrite was run as "v1.12.1", before the round definition was added, in a comparison using the eight development deals: `git show acc9986:_dev/reviews/2026-09-21/instruction_comparison.md`. Recorded model reviews preferred it to v1.11 and found it comparable to v1.12 on the tested Opus subset. Round boundaries remained unstable, motivating the added round definition. These small, largely single-run comparisons are not a fully adjudicated benchmark and do not establish perfect price extraction or that wording changes have no further effect.

**Status updated 22 September:** no v1.13.1 extraction ran. Under unchanged v1.13.2, Datalink supplied the authorized unseen-case extraction, Mac-Gray supplied a familiar-case pilot, and seven additional Opus runs completed the current nine-deal set. Controlled Opus corrections are preserved separately. The retired Sol/Grok comparison results were deleted on Austin's instruction; they are not part of the current model-selection plan. [Current status and decisions](RESEARCH_QUESTIONS.md) links the retained evidence and states the remaining review boundaries.

## Follow-up audit: clarification adopted as v1.13.2

The independent audit supplied by Austin on 21 September identified a residual ambiguity in v1.13.1's E6. Its earlier opening paragraph says the first final-offer request can open a round and repeated improvement requests can remain within it. The finality paragraph said "a final-offer request made later opens its own round," which could be read as a second, broader opening rule.

Austin approved proceeding with this replacement for the final sentence only:

> Finality describes the round as the target ran it; opening a later final round does not make the earlier stage final.

This removes the competing trigger and retains the prohibition on retroactive finality. It adds no new research convention and offers no guarantee of improved extraction. Relative to v1.13.1, the instruction changes only this sentence and its version label. The resulting v1.13.2 is frozen for unseen-filing testing. Approval for this clarification does not launch extraction, audit or revision runs.

The same audit separated an omitted Meredith economic-structure change under E2/E10 from its unresolved whole-company-scope convention. That observation concerned the then-reviewed draft, not a completed review of the newer v1.13.2 output. Persistent omissions must first be tested against existing rules, not automatically assigned new ones. [Current status and decisions](RESEARCH_QUESTIONS.md) records the current review workflow.
