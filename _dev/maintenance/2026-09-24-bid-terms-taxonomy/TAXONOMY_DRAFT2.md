# Bid terms and conditions: proposed ledger columns (draft 2, 24 September 2026)

Proposal for a new instruction version after v1.13.2. Today a bid's specific conditions live only in its free-text Note, beside a single summary level (Conditions = None, Light, Heavy or Unclear, rule E12). The researchers want each condition they care about in its own coded column so it can be filtered and counted.

Conditions they care about: due diligence, financing, antitrust, other regulatory approvals, exclusivity, earnouts/CVRs, and the cash/stock mix of consideration. Termination fees and reverse termination fees are deliberately out of scope.

## Where the columns go

On the Deal ledger, the single column **All cash** is replaced by three consideration columns, and five condition columns follow **Conditions**:

… Price low · Price high · **Stock %** · **CVR/earnout** · **CVR/earnout max** · Formality · Conditions · **Due diligence** · **Financing** · **Regulatory** · **Antitrust** · **Exclusivity** · Count …

They are filled on the rows that carry Formality and Conditions today (Bid, Bid reaffirmed, Other-scope bid) and left blank on every other row, including Merger agreement signed.

## 1. Consideration

**Price low / Price high** hold the upfront per-share amount only. A CVR or earnout is never added into the price cells; it goes in the two CVR columns.

| Column | Values | Rule |
|---|---|---|
| **Stock %** | a number from 0 to 100, or `Part stock`, `Not stated`, `Varies` | Stock's share of the bid's upfront per-share value, to one decimal. 0 when the filing says the consideration is all cash; 100 when all stock. For cash and stock, compute only from figures the filing gives for that bid (e.g. $20 cash + $10 in stock = 33.3; or an implied per-share value the filing reports for that bid, minus the cash). Never use a share price from outside the filing. `Part stock` when the filing shows a stock component but gives no figure to compute its share (e.g. an exchange ratio with no reported value); the Note gives the ratio. For a cash/stock election with a proration cap, use the aggregate mix the bid sets. Other securities (preferred stock, notes) count as stock and the Note names them. A dollar price alone does not establish cash: `Not stated`. |
| **CVR/earnout** | `Y` or blank | Y when the bid includes any contingent payment, whatever the filing calls it (CVR, earnout, contingent consideration, milestone payment). The two terms are merged because filings use them interchangeably. Blank means none reported. |
| **CVR/earnout max** | $ per share, or blank | The most the contingent payment can pay per share, as the filing states it. Blank when CVR/earnout is blank or the maximum is not stated. |

## 2. Conditions

| Column | Values (firmest first) |
|---|---|
| **Due diligence** | `Complete` — the bid says no further diligence is needed. · `Confirmatory` — only confirmatory, limited or expedited diligence remains. · `Substantive` — the bid requires further substantive diligence, or a stated multi-week or exclusive diligence period. · `Not begun` — the bid states no diligence condition, but the filing shows the bidder had not yet had diligence access (no data room, no management meetings). · `Not stated` · `Varies` |
| **Financing** | `Not needed` — the filing reports the bidder will fund from cash on hand or existing facilities, or the bid is all stock. · `Committed` — the filing reports signed debt/equity commitment letters covering the bid, with no financing condition. · `Contingent` — financing not committed: a financing condition, a highly confident letter or other non-binding lender support, financing reported as not yet arranged, or any mix in which one part is uncommitted. · `Not stated` · `Varies` |
| **Regulatory** | `No concern` — approvals are mentioned for this bid with no concern reported, or the bidder says it expects no approval problem. · `Concern` — the filing reports a regulatory or antitrust risk for this bid: expected divestitures, a second request, a long approval timeline, or the target or its advisers questioning closing certainty. · `Concern, bidder bears risk` — the same, and the bid commits the bidder to absorb it (a divestiture commitment, a "hell or high water" undertaking, a regulatory reverse fee). · `Not stated` · `Varies` |
| **Antitrust** | `Y` or blank. Y when the filing names antitrust or competition review in connection with this bid: HSR, the DOJ, the FTC, the European Commission or another merger-control authority, competitive overlap, or divesting an overlapping business. Blank means another kind of approval, or a type the filing does not identify. Y requires Regulatory to be filled. |
| **Exclusivity** | `Required` — the bid is conditioned on the target granting exclusivity. · `Requested` — the bidder asks for exclusivity without making it a condition. · `Not stated` · `Varies`. The requested period goes in the Note. |

**Antitrust vs. other regulation.** The two often cannot be told apart in a filing, so no split is forced. Regulatory covers every approval; Antitrust = Y flags only the cases the filing clearly identifies as antitrust. In analysis: Regulatory filled with Antitrust = Y is antitrust; Regulatory filled with Antitrust blank is other or unidentified.

## 3. Rules for all the new columns

1. **Not stated is not a negative.** A negative value (Complete, Not needed, No concern, Stock % = 0) needs the filing's support. Silence is `Not stated` (or blank for the Y markers).
2. **Cohort rows** whose members differ get `Varies`. A Y marker on a cohort row means every member carries it; if only some do, `Varies`.
3. **No carrying forward.** Each bid row records what the filing reports for that bid. A revised bid described only by its new price gets `Not stated` for terms the filing does not mention, unless the filing says the other terms were unchanged. (Forward-filling is easy in analysis; a fill made during extraction cannot be told apart afterwards.)
4. **Evidence.** The row's Quote and page supports its main claim. For any coded value it does not support, the Note gives the page: "Fin: commitment letters (p. 34)".
5. **The Note** keeps only what the columns cannot hold: the lender's name, the exclusivity period, the CVR trigger, conditions outside this list (right to reprice, management rollover, bidder shareholder vote).

## 4. Relation to the Conditions summary (E12)

Conditions (None, Light, Heavy, Unclear) stays as the summary level. The checker flags contradictions between it and the new columns:

- Heavy is required when Financing = `Contingent`, Due diligence = `Substantive`, or Regulatory = `Concern`.
- None requires Due diligence = `Complete`, Financing = `Not needed` or `Committed`, and Regulatory not `Concern`.
- Due diligence = `Not begun` with no other Heavy trigger matches today's Unclear ("the narrative shows diligence still open while the bid states no condition").

Later, the summary level could be computed from the columns instead of judged.

## 5. Open decisions

1. Price cells hold the upfront amount only, excluding any CVR (assumed above; v1.13.2 does not say).
2. Whether Regulatory = `Concern, bidder bears risk` still counts as Heavy.
