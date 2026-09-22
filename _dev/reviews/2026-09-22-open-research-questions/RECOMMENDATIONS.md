# Mac-Gray R01 and Meredith scope: recommendations

22 September 2026. **Recommendations only; no decision or workbook change has been implemented.** The complete frozen v1.13.2 instruction, current records, selected workbooks, relevant filing passages and annexes, preserved adjudications, and original reference notes were read. Meredith’s full Background, pp. 58–77, was read in order. This is a bounded research review, not whole-deal acceptance.

**Recommend dated material-term events for Mac-Gray. Recommend Other-scope coding for Meredith’s LMG proposals and exclusion from structural estimation. Meredith’s estimation exclusion is already explicit in Alex’s reference notes; the current unresolved-status record missed that evidence.**

## Versions reviewed

When this review was written, earlier on 22 September, the [catalog](../../cockpit/catalog.json) selected these originals; both hashes were independently verified. Later that day the catalog was replaced by one Opus 5.5 medium version per deal, so these versions are no longer in the cockpit and the IDs below do not apply to the current `extraction/` drafts. All event IDs below refer to these pre-change versions. Excel ledger row = event ID + 1.

| Workbook | Version and SHA-256 |
| --- | --- |
| [Mac-Gray](../2026-09-21-mac-gray-pilot/acceptance/extraction/mac-gray.xlsx) | `mac-gray-candidate`, v1.13.2; `db85a39b00bb98702e73ad3e891cb4ab50202f2e032fcb3278ef0e6e45f351e1`; 58 events, 13 Bids, 3 rounds, 9 Questions |
| Meredith (archived; git `03d59b1:_dev/reviews/2026-09-21-v1132-cockpit/raw/extraction/meredith.xlsx`) | `v1132-raw`; `178c1f0c8419ef19503ad52e1b1fa40132d5f3b35e1d32f62e8c62205d951c89`; 78 events, 24 Bids, 10 Other-scope bids, 13 Questions; human review pending |

## 1. Mac-Gray: preserve material economic changes as events

[Instruction E2/E10](../../../SEC_Deal_Ledger_Extraction_Instruction.md) gives rows to changes in commitment, target requirements and communicated material economic terms. Routine drafting remains in Notes. Fees and sponsor recourse cross that materiality threshold here: the [filing](../../../raw_filing/mac-gray_2013-12-04_DEFM14A.htm), pp. 43–44, expressly identifies the heavily negotiated target fee, funding/damages protection and possible deterrence of competing proposals as board considerations.

Recommend **Bid** for bidder proposals and **Other material event** for target demands. This applies existing rules without changing the instruction, but [R01](../2026-09-21-mac-gray-pilot/acceptance/RESEARCH_DECISION.md) expressly reserves the materiality choice for Austin. Alex’s Mac-Gray voice notes discuss conditionality, not this fee-row convention. His Meredith comment that broader contract-term research belongs to another project supports keeping the threshold narrow.

### Eight additions if approved

None has its own substantive event in the current workbook. Partial coverage in existing Notes must be moved or cross-referenced, not duplicated. Dates and excerpts below were independently checked against printed pages.

| Addition | Source-supported change | Placement against current IDs |
| --- | --- | --- |
| **M1: Bid, 09/21–09/23/2013** | Final package adds $15m regulatory reverse fee and express no financing contingency, pp. 37–38: “the inclusion of a $15 million "reverse" termination fee payable by CSC/Pamplona to Mac-Gray”. Pamplona’s 100% funding repeats its September 9/18 commitment. | After #44 / Excel 45, before #45 / Excel 46. Remove later terms from #44’s Note. Bounds 09/21–09/23; Sort date 09/22. |
| **M2: Other material event, 09/25–10/07** | Target requests buyer/sponsor breach liability and target fee about 2.5% of equity value, p. 38: “which Mac-Gray proposed should approximate 2.5% of the total equity value of the transaction”. No inferred dollar fee. | Around #49–#51 / Excel 50–52. Preserve full interval; Sort date 10/01. Ordering against #51’s bounded Moab event is unobserved. |
| **M3: Bid, 10/05** | Buyer’s revised sponsor commitment-letter draft proposes sponsor liability, capped at an unspecified amount, p. 39: “would be limited to an unspecified dollar amount.” | After interval-sorted #51 / Excel 52; before M4/current #52. Do not backdate the later $50m cap. |
| **M4: Bid, 10/07** | Buyer merger markup “proposed a $15 million Mac-Gray termination fee”, about 4.4%, p. 39. | After M3; before current #52 / Excel 53. |
| **M5: Bid, 10/08** | Sponsor damages cap specified, p. 39: “which Kirkland proposed, at the direction of CSC/Pamplona, be capped at $50 million.” | After M4, before M6/current #52. |
| **M6: Other material event, later 10/08** | Target offers acceptance of cap and counters $10.5m target fee, about 3.0%, pp. 39–40: “proposed a $10.5 million Mac-Gray termination fee”. | After M5, before #52. October 9’s board report confirms agreement on the cap; it is not another offer. |
| **M7: Other material event, 10/11** | Target conditions extension on fee no higher than $11m, about 3.2%, and communicates that position, p. 40: “a Mac-Gray termination fee of not more than $11 million”. | After #52 / Excel 53, before M8/#53 / Excel 54. |
| **M8: Bid, later 10/11** | Buyer accepts $11m target fee, pp. 40–41: “the representative of CSC/Pamplona telephoned Mr. Daoust and agreed to the $11 million” (p. 40). | After M7, before #53 / Excel 54. Move dated acceptance from #53’s Note. |

All five new Bids: CSC/Pamplona; Strategic; Process 1, Round 3; Count 1; **$21.25 in both price cells, All cash Yes**, explicitly carried unchanged from current #44. Formal remains appropriate: M1 continues the genuine final solicitation; October communications revise definitive documents/negotiations. These are changed offers, not Bid reaffirmed. Exact-date rows use that date in all three date fields; reported events leave Inferred blank.

Recommend Conditions **Heavy for M1** because of its exclusive-period request; **Unclear for October’s communications**, which do not affirm diligence completion or expressly limit conditions to documentation. Funding is committed, but pp. 38–39 still discuss diligence. Do not automatically copy September’s Heavy label or infer None from eventual signing. A Light classification needs its own affirmative E12 rationale. Target rows use Who Mac-Gray, blank Count/Type and blank bid fields.

### Necessary dependent edits and interpretation

- **#44 / P45:** separate September 21 terms from M1’s later settlement. **#53 / P54:** keep October 12 extension execution, referencing M7/M8. Preserve **#52 / Excel 53**, the earlier extension request, and **#46 / Excel 47**, September 24 execution. Their already recorded process acts require no duplicates.
- **#57 / P58:** retain signing, with blank price fields; preserve final sponsor-cap context. Add **Q10** for R01; update workbook Q7 / Excel 8 and Q9 / Excel 10 plus affected flags. Q9’s counterfactual must account for the new October definitive-document Bids rather than manufacture an extra reaffirmation. Renumber and repair every dependent reference.
- Result: **66 events, 18 Bids, three rounds, ten Questions**. Rounds R3 still has **three distinct bidding parties**. No new round, bidder, exit or deadline follows from these additions.

The $15m reverse fee is buyer-to-target; the negotiated $15m→$11m target fee runs in the opposite direction. The $50m cap limits **Pamplona’s damages**, not all buyer liability or the $594m funding commitment. Final financing text explicitly leaves buyer-entity damages unlimited (pp. 6, 59); final fee triggers are in Annex A §9.04, pp. A-54–A-55. None of these contingent amounts changes the $21.25 closing price.

The strongest alternative retains all dated changes in Notes and keeps 13 Bids. It avoids inflating apparent offer counts but conceals proposal timing. Prefer the event record, then distinguish **five changes of terms from five new price observations** in analysis. Do not treat them as independent valuation draws. No such downstream filter is claimed implemented.

## 2. Meredith: economic scope determines coding

### Filing facts and existing research guidance

The [filing](../../../raw_filing/meredith_2021-11-08_DEFM14A.htm) describes pre-separation Meredith as NMG plus LMG (p. 1). It explains that the tax-efficient sale structure leaves **“LMG RemainCo (the Meredith Corporation legal entity then owning the LMG segment only)”** (p. 59).

At the agreed closing, NMG, MNI, People TV and corporate functions go to NMG SpinCo; existing holders receive its shares one for one. Gray acquires the remaining local television business through the surviving Meredith corporation (pp. 2–3, 50–51, 126–127). Annex A p. A-1 makes distribution a merger condition; Annex D pp. D-7–D-8 expressly separates RemainCo and SpinCo businesses, and p. D-12 allocates assets and the SpinCo cash payment.

Thus **Meredith Corporation is the legal target; LMG excluding MNI/People TV is Gray’s economic acquisition**. Buying all shares of that residual entity does not acquire the original combined business.

[Alex’s original voice notes](../../../ref/alex_voice_notes_2026-08.docx), section VI, are decisive. References below use 1-based Word body paragraph numbers:

- **¶95**, beginning “[Alex] Meredith cannot be a part of the estimation”: expressly excludes it because the acquired segment has no observed market price, while recommending retention for reduced-form/descriptive work.
- **¶97, item 2:** calls its bids partial, requests a flag, and distinguishes a much-earlier spin with an observable stand-alone price from simultaneous separation/acquisition.
- **¶99–100:** warns that Party D’s cash covers levered assets and retained equity; debt arithmetic does not solve the missing segment market-price problem.
- **¶184, summary L:** again requires flagging partial-bid deals “like Meredith”.

Earlier tentative valuation ideas in ¶91–94 do not override ¶95’s conclusion. Reference recollections of later completion dates are not imported into the November 8 filing ledger. **Estimation exclusion is an existing research disposition; the remaining task is authorized coding/status alignment.**

### Minimal scope correction

Apply E1 to the economic company before the transaction-specific separation. Recommend:

1. Clarify **Deal facts!B2**: pre-separation Meredith contains NMG and LMG; this process sells selected stations and then LMG. Replace **B14** with **“No — proposals cover selected LMG stations or the LMG business following separation of NMG; none acquires pre-separation Meredith including NMG (Q5).”**
2. Change Bid to **Other-scope bid** on these 24 current events, with Excel rows in parentheses: **#11 (12), #12 (13), #13 (14), #20 (21), #23 (24), #35 (36), #41 (42), #42 (43), #44 (45), #48 (49), #49 (50), #51 (52), #54 (55), #55 (56), #57 (58), #58 (59), #63 (64), #66 (67), #67 (68), #70 (71), #72 (73), #73 (74), #74 (75), #75 (76)**. Ten station-offer rows already have this label. Keep signing/announcement labels.
3. Rewrite **Q5 / Questions Excel 6**, replacing its closing-legal-shell justification with economic scope and Alex’s exclusion. Extend its affected-row list/flags to later offers. Clarify consideration/basis in **Deal facts!B5/B15** and relevant Notes. Preserve participants, dates and process history. Auction screen “Met, 17 parties” describes this mixed-scope process, not 17 whole-company bidders.

D1 explicitly permits price cells on Other-scope rows. **Retain Gray’s reported per-share prices**, including H/I values in Excel **67, 71, 73–76**. E1 prevents misattributing these as whole-Meredith prices; it does not require deleting supported segment prices. Keep enterprise-value rows’ price cells blank under E13; do not derive earlier per-share values from later debt/share-count assumptions.

Gray’s **All cash = Yes** describes consideration for LMG. Distributed NMG shares are retained business ownership, not Gray-issued consideration. The old shareholders’ total package is nevertheless cash **plus NMG ownership**. Party D’s cash plus combined-company equity remains No.

### Separate April 13 omission

Insert one dated **Other-scope bid** before current **#41 / Excel 42**. On **04/13/2021**, Party D submits the revised NMG-spin/LMG-sale structure, and Party E changes from selling stations for cash to contributing them for ownership (p. 66):

> “Party E would be contributing television stations to the new combined company in exchange for an ownership interest rather than selling the stations to the new company for cash.”

Use Party D; existing Financial classification; Process 1/current Round 3; Count 1; exact dates; All cash No; Formal supported by its April 8 merger markup; Conditions Heavy for unresolved diligence/structure/financing. Price cells stay blank: no new full-package per-share amount is stated. Update Q5/Q6/Q10 references and flags. Do not claim NMG-spin structuring first arose April 13: discussions already appear April 2 (p. 65).

This follows existing E2/E10 independently of the whole-company choice. Together, these bounded edits yield **79 events, 35 Other-scope offers, zero whole-company Bids**; they do not establish overall draft accuracy.

### Research implications and limits

The offers also differ within LMG scope:

- **April 14, #41–42 / Excel 42–43, p. 66:** Gray excludes MNI; Party B includes it. Party D’s April offers include it too.
- **April 29, #57–58 / Excel 58–59, p. 69:** $2.66bn with 50.2% retained equity versus $2.76bn with 34% are distinct alternatives. Keep both.
- **May 1–2, p. 70:** $1.975bn closing net debt is agreed, turning Gray’s $2.7bn enterprise value into $725m shareholder cash. Do not backdate this allocation.
- **May 13, #63 / Excel 64, pp. 71–72:** $2.76bn includes a $36m Gray break fee, leaves 19% equity, excludes MNI and adds stations. Reported $14.99/share is only the cash dividend.
- **May 26, #67 / Excel 68, p. 74:** $16.51/share cash plus 10% equity, additional stations and changed financing again alter the package. Cash alone cannot rank it against Gray.

Later SpinCo payment adjustments do not reduce Gray’s $16.99 payment (p. 127), but affect the separated businesses’ economics. Dotdash’s separate NMG acquisition (pp. 4, 51, 77; Annex H) does not retroactively make Gray a whole-company bidder or provide an unaffected LMG market price. Combining eventual sale prices would use negotiated outcomes as the benchmark Alex found missing.

Retain Meredith for suitably qualified descriptive analysis; exclude it from structural estimation as Alex specified. No estimator/export filter is claimed implemented. No frozen instruction, existing workbook, catalog, decision document or preserved evidence was changed; no extraction or workbook-revision run, deployment, commit or push occurred.
