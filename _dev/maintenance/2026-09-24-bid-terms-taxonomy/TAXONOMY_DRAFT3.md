# Bid terms and conditions: proposed ledger columns (draft 3, 24 September 2026)

Proposal for an instruction version after v1.13.2; not yet an instruction. Draft 2 applied Austin's three comments (no Consideration column, highly confident and uncommitted financing coded Contingent, termination fees out of scope). Fable 5.1 at xhigh then reviewed draft 2 against twelve filings ([REVIEW_FABLE.md](REVIEW_FABLE.md)); this draft takes in that review, with the departures listed at the end.

Today a bid's specific conditions live only in its Note beside one summary level (Conditions, E12). These columns give each condition the researchers named its own coded cell.

## Where the columns go

On the Deal ledger, **All cash** is replaced by three consideration columns, and six condition columns follow **Conditions**:

… Price low · Price high · **Stock %** · **CVR/earnout** · **CVR/earnout value** · Formality · Conditions · **Due diligence** · **Financing** · **Regulatory** · **Antitrust** · **Bidder bears reg. risk** · **Exclusivity** · Count …

They are filled on Bid, Bid reaffirmed and Other-scope bid rows, and blank on every other row, including Merger agreement signed.

## 1. Consideration

**Price cells (amends E13).** Price low and Price high hold the upfront per-share value. A contingent payment is never added in; it goes in the CVR columns. E13 today puts a stated package value, CVR included, in the price cells; this replaces that sentence. Example: G&W's $21.15, "$20.02 cash at closing and $1.13 in the form of a contingent value right" (P&W), becomes Price 20.02, CVR/earnout Y, CVR/earnout value 1.13, with the $21.15 package in the Note.

| Column | Values | Rule |
|---|---|---|
| **Stock %** | a number to one decimal; a range `a–b` where the filing states one; `Part stock`; `Not stated`; `Varies` | Stock's share of the bid's upfront per-share value. **0** when the filing says the price is in cash ("$25.00 per share in cash" suffices). **100** when all stock. For cash and stock, compute only from figures the filing gives for that bid; never use an outside share price. A stated range stays a range ("stock representing 50% to 75% of the consideration" → `50–75`, Pepco). **Part stock** when a stock component is shown with no figure to compute its share ("a combination of cash and stock to be determined", Meredith); an exchange ratio goes in the Note. An election with a proration cap takes the aggregate mix the bid sets. Other securities count as stock and the Note names them. Shares of a spun-off company distributed beside the merger are not consideration; name them in the Note. A dollar price alone does not establish cash: `Not stated`. Numbers are stored as numbers; ranges and codes as text. |
| **CVR/earnout** | `Y` or blank | Y when the bid includes a payment made after closing that depends on future events, whatever the filing calls it: CVR, earnout, contingent consideration, milestone payment, or a security whose payout depends on performance (such as Party B's options, Mac-Gray). Such securities are CVR/earnout, not stock. A price that depends on criteria is CVR/earnout only when the filing shows the extra amount is paid after closing; otherwise it is a price range under E13 and the Note quotes the criteria ("at least $10.30 … as high as $10.75 per share if certain financial criteria were met", Datalink). Blank means none reported. |
| **CVR/earnout value** | $ per share, or blank | The per-share amount the filing states for the contingent payment. The Note says whether it is a maximum, a face amount, or someone's valuation, and whose. Filled only when CVR/earnout = Y. |

## 2. Conditions

| Column | Values | Rule |
|---|---|---|
| **Due diligence** | `Complete` · `Confirmatory` · `Unspecified` · `Substantive` · `Not begun` · `Not stated` · `Varies` | **Complete**: the filing says no diligence remains. **Confirmatory**: only confirmatory, limited or expedited diligence; a stated diligence period under two weeks; or substantive diligence reported complete without a statement that none remains. **Unspecified**: the bid is subject to diligence with no indication of its extent ("subject to customary diligence review", Meredith). **Substantive**: further diligence described as substantive or extensive, a stated diligence period of two weeks or more, or an exclusive diligence period. **Not begun**: the bid states no diligence condition, but the filing shows the bidder had not yet had diligence access. A stated condition beats Not begun. Where two values fit, take the heavier: Substantive, then Unspecified, then Confirmatory, then Complete ("more in-depth and confirmatory due diligence", Mac-Gray → Substantive). |
| **Financing** | `Not needed` · `Committed` · `Contingent` · `Not stated` · `Varies` | **Not needed**: funded from cash on hand or existing facilities, or all stock. **Committed**: the bidder cannot walk away for lack of financing — signed commitment letters, a sponsor or parent committing the full price, or the bid stated not to be subject to a financing condition ("not subject to any financing condition", Medivation; "not contingent upon third party debt financing", Synacor). **Contingent**: a financing condition, a highly confident letter or other non-binding lender support, financing not yet arranged or still being explored, or any part uncommitted. Contingent wins when the filing reports both a source and the absence of a commitment (Mac-Gray Party A: credit facilities, but "did not include a firm financing commitment"). |
| **Regulatory** | `No concern` · `Concern` · `Not stated` · `Varies` | **No concern**: the filing reports the target, its advisers or the bidder expecting no material obstacle, or a clean or prompt approval path, for this bid. **Concern**: the filing reports a regulatory risk for this bid — expected divestitures, a second request, a long approval timeline, doubt about closing — including a process-wide risk the filing applies to every bidder. **Not stated**, including a bare mention that approvals are required. |
| **Antitrust** | `Y` or blank | Y when the Regulatory value or the bidder's risk commitment concerns an antitrust or competition law or authority (HSR, the DOJ, the FTC, the European Commission, another competition authority, or the words antitrust or competition). Blank means another kind of approval (FCC, STB, state utility commissions) or a type the filing does not identify. Requires Regulatory filled or Bidder bears reg. risk = Y. |
| **Bidder bears reg. risk** | `Y` or blank | Y when the bid commits the bidder to absorb regulatory risk: a divestiture commitment ("committed to divest its Flint-Saginaw-Bay City station", Meredith) or a hell-or-high-water undertaking. A markup deleting such an undertaking leaves it blank and the Note says so (Kraton). Independent of Regulatory: a bidder can commit even where no concern is reported. |
| **Exclusivity** | `Required` · `Requested` · `Not stated` · `Varies` | **Required**: the bid, or the bidder's stated willingness to continue, is conditioned on exclusivity, including a bidder that stops when refused ("was not prepared to move forward … without an exclusivity agreement", Zep). **Requested**: asked for, assumed, or a draft exclusivity agreement supplied, without a condition. A request made while the bid stands and before its next revision counts for that bid and also gets its own Exclusivity changed row (D2). The period goes in the Note. |

**Antitrust vs. other regulation.** No split is forced where the filing does not make one. Regulatory records the level of approval risk for every kind of approval; Antitrust = Y marks the cases the filing identifies as antitrust. In analysis, Regulatory filled with Antitrust = Y is antitrust; with Antitrust blank, other or unidentified.

## 3. Rules for all the new columns

1. **Not stated is not a negative.** Complete, Not needed, No concern and Stock % = 0 need the filing's support. Silence is `Not stated`, or blank for the Y markers.
2. **Cohort rows** whose members differ get `Varies`. A Y marker on a cohort row means every member carries it; if only some do, `Varies`.
3. **No carrying forward**, with two exceptions. Each bid row records what the filing reports for that bid, as E12 already does for Conditions. (a) Bid reaffirmed copies the standing values, Note "carried from #n", as E10 does for Conditions. (b) Where the filing says the other terms were unchanged ("otherwise on the transaction terms previously proposed", sTec; "otherwise materially unchanged", Meredith), copy the prior row's values, Note "Terms: as #n (p. x)".
4. **Timing.** A fact from outside the Background, such as the merger agreement summary, fills a bid row only if the filing dates it no later than that bid; otherwise it goes in the Merger agreement signed Note.
5. **Evidence.** One page cite covers every code drawn from the row's quoted passage; cite separately only codes drawn from elsewhere ("Fin: p. 34").
6. **The Note** keeps what the columns cannot: the lender, the exclusivity period, the CVR trigger and value basis, and conditions outside this list (right to reprice, management rollover, bidder shareholder vote).

## 4. Relation to Conditions (E12) and the checker

Conditions (None, Light, Heavy, Unclear) stays as the summary level. Checker rules:

- **Heavy** is required when Financing = Contingent or Due diligence = Substantive.
- **None** requires Due diligence = Complete, Financing = Not needed or Committed, and Regulatory ≠ Concern.
- **Light** requires Due diligence = Confirmatory, or Financing = Not needed or Committed with Due diligence = Complete or Not stated.
- **Warning** when every condition column is Not stated and Conditions ≠ Unclear: the Note must name the condition outside the columns that supports the level.
- Regulatory = Concern, Bidder bears reg. risk and Exclusivity do not force a level. (A regulatory concern is often process-wide, as at Pepco; E11 already keeps exclusivity requests out of the classification; an exclusive diligence period reaches the summary through Due diligence.)
- CVR/earnout value requires CVR/earnout = Y. Antitrust = Y requires Regulatory filled or Bidder bears reg. risk = Y.

Instruction edits this implies: D1 columns; E12 Heavy/Light/None restated against the columns; the E13 price sentence; E13's All cash paragraph replaced by the Stock % rule; and the stale All cash references in D2 (Merger agreement signed) and F.4.

## 5. Open decisions for Austin and Alex

1. **E13 amendment**: price cells upfront only, excluding any CVR. Recommended; it changes the current rule.
2. **Due diligence = Unspecified**: whether an unqualified diligence condition counts as Heavy. Recommended: do not force a level yet; decide once the column shows how often it occurs.
3. **Regulatory grounds on exit rows**: filling Regulatory and Antitrust on Contact, Dropped by target and Withdrew rows where the filing gives regulatory reasons (PetSmart kept Industry Participant out over "the very high risk that … would not receive antitrust clearances"). Useful for counting live bidders, but outside bid terms. Recommended: defer.

## Departures from Fable's review

- **Financing**: Fable proposed a separate `No condition` value; it is folded into Committed, keeping Austin's firm/contingent split and the R01 walk-away test.
- **Due diligence**: Fable coded an unqualified diligence condition as Substantive. Draft 3 adds `Unspecified` instead, since the instruction forbids making a value more exact than its evidence (Part B).
- **CVR/earnout**: Fable treated any price that rises if criteria are met as a CVR. Draft 3 limits CVR/earnout to payments made after closing; a pre-signing contingency stays a range under E13.
- **Carry-forward**: Fable read E12 as state-based. E12 already records "what the filing reports the bid itself to carry"; only Bid reaffirmed carries state (E10). Its two exceptions and the Unclear warning are adopted; forcing Conditions = Unclear is not.
- **Regulatory = Concern forcing Heavy**: dropped, following Fable's own Pepco example.
- **Exit rows**: left as open decision 3.

The twelve filings contain few CVRs or earnouts, so those two columns are the least tested.
