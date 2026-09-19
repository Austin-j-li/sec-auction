---
name: pro-vs-alex-yardstick
description: GPT Pro's 12-extraction review (2026-09-18) grades against instruction v2 + source fidelity, not Alex's voice-note checklist; known points where the two conflict
metadata:
  type: project
---

GPT Pro's review of the 12 extractions (model_review_2026-09-18/) never saw Alex's voice notes (ref/alex_voice_notes_2026-08.docx). Its ranking (Opus > DeepSeek > Sol > GLM) is instruction-compliance + epistemic strictness, not "does this satisfy Alex". Scored on Alex's ~31 deal-specific asks for Providence / Mac-Gray / PetSmart, the four models are much closer together and Opus hits ~25 cleanly.

Places where instruction v2 (Pro-authored, says itself it is not Alex-ratified) or Pro's adjudication diverges from what Alex asked for:
- PetSmart 15 NDAs − 6 IOIs = 9 non-submitters: Alex wants the row (reason unknown); instruction §10.2 allows it; Pro scored it Major against Opus and GLM.
- Mac-Gray rivals at CSC/Pamplona exclusivity (Sep 24): Alex wants Party A/B "Dropped by target"; instruction §10.1 says "Participation paused"; Pro scored GLM's Dropped rows Major.
- Providence Aug 4 Party B: Alex wants a priced formal $24 bid-revision row; instruction §9.1 says a further draft is not a bid, so all four emit an unpriced "Offer update".
- PetSmart Longview rollover: Alex says not a consortium; instruction §5.3 agrees; all four models still code "Bidding group changed" because the filing defines Buyer Group to include Longview after Dec 12. Pro did not flag it.
- Cross-paragraph date narrowing (late July → Jul 20–22; first week Oct → Oct 3–7) and PetSmart round-1 start (Alex: Oct 3): no model does it.

**Why:** Austin asked how far the pipeline is from satisfying Alex; the answer depends on which yardstick is used, and several "defects" in Pro's register are things Alex asked for.
**How to apply:** When evaluating extractions or revising the instruction, score against Alex's notes directly and get Alex to rule on the conflicts above before treating Pro's register as the repair queue. Untested by these three deals: winner type, multiple processes, partial/EV bids, soft deadlines, go-shop (Penford, Kraton, Meredith, Synacor, STEC).
