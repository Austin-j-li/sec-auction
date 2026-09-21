# Instruction v1.13: the objective-led rewrite becomes the working instruction

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
| v1.12's seven edits carry over. | The honesty sentence, whole-background reading with annexes, the paragraph-by-paragraph reread, the exact-value support check, exact-subtraction examples, and finality describing the round as the target ran it. |

Q3 (one-sided prices) needs no text change. Q7 (Company H continuing invitation) stays unadopted.

## Evidence and its limits

The rewrite was run as "v1.12.1", before the round definition was added, against v1.11 and v1.12 on the eight reviewed deals: `git show acc9986:_dev/reviews/2026-09-21/instruction_comparison.md`. On Opus it beat v1.11 and tied v1.12; DeepSeek flash made a quarter as many checker errors under it. Round boundaries were unstable under every version, which is why the round definition was added. **No extraction has run under v1.13 as it now reads, and none under any of these versions on an unseen filing.**
