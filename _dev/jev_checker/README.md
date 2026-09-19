# Jev in this project: what it is, what we found, what we decided

Written 20 September 2026 as a handoff of the discussion between Austin and the assistant. Austin is new to language-model tooling; keep explanations in plain words.

## What Jev is

Jev is a small, fast model sold by TypeSafe. It does not write text. You give it a short piece of text and a narrow question, and it picks from a fixed set of answers (yes/no, or one of several options) with a number saying how sure it is. One question takes under half a second; checking all nine comparison workbooks cost about 11 cents. Because the answers are fixed options, ordinary code can ask hundreds of questions and sort the replies.

The extractors (Opus and others) read a filing and write a whole ledger. Jev cannot do that. It is a cheap second reader.

## What we tested (19 September, three rounds; details in RESULTS_round1–3.md)

1. **Is each row's price right for that bid?** Code takes the paragraph a row quotes and asks Jev whether it supports the row's price. When the question names the bidder, the date and which offer it was, Jev caught all 185 deliberately planted wrong prices and raised no false "wrong price" alarm on 105 real rows. A looser question naming only the bidder missed 25 of 92 cases where the wrong price was the same bidder's other offer. Wording matters. Passage width matters too: the quoted paragraph plus two either side works; wider causes false alarms.
2. **Did the extractor leave an event out?** Code goes through the Background section sentence by sentence; for each sentence that reports an event, Jev picks the ledger row that records it, or "none". Confident "none" answers form a short list (0–6 sentences per workbook). It found 5 of 8 omissions the blind grading had identified, including the Mac-Gray voting agreements that all three extractors missed. It missed three, one because Jev does not see a returned draft contract as a bid.
3. **All cash or not?** (round 1) Jev disagreed with the ledger on exactly the two Providence rows the grader marked wrong.

Not useful: exit labels, generic "is this row right", rounds, bidder counts, dates. Those need the whole story of the deal, and they are where extractors lose most points. They stay with the reviewer and the mechanical checker.

## Decisions reached in discussion

- **Jev stays a checker, not a preprocessing step.** The scarce resource is Austin's and Alex's checking time, not the extractor's reading time: a Background section is about a hundred paragraphs, and extractors already get the easy parts right. As a checker, a Jev miss costs nothing. As a filter in front of the extractor, a Jev miss becomes an extraction error. Jev must never decide what text the extractor sees.
- **The mechanical script and Jev are not redundant.** The script (`_dev/tools/check_lean.py`) checks form: allowed labels, date order, quotations present in the filing. It is exact, free and offline. Jev checks meaning. Keep exact checks in code; never ask a model what code can compute.
- **Merge them at the user's end: one command, one report.** Mechanical checks first, then Jev (it reuses the script's work of locating quotations). Report in order of seriousness: rules broken; prices that look contradicted; events that look missing; warnings. Mark each item as certain (script) or a model judgment with its confidence. The Jev step is optional: with no key or network the command still runs the mechanical part. Runs outside the extraction sandbox; never edits a workbook. **Not yet built; this is the next task.**
- **Next experiment after that: a revision loop.** Extractor writes the ledger; the checker flags; the flags go back to the extractor for one revision pass in which it fixes each flag or says why not. Open questions: does it fix real omissions without breaking correct rows, and does it add trivial rows to satisfy flags? Needs a careful isolated run and Austin's go-ahead.
- **Considered and set aside:** giving the extractor a Jev-made checklist of event sentences before extraction. Safer than filtering, but it may push the extractor towards sentence-by-sentence recording, against Alex's convention of folding small events into notes.
- **Where cheap high-volume judgment would really pay: the whole sample.** If the project grows to hundreds of filings, Jev could screen them: is this a merger proxy with a Background section, where does it start and end, was there more than one bidder, is it worth a full extraction. Open question put to Austin, unanswered: how many deals are planned?

## Limits to keep in mind

Everything was tested on the same three development deals. The confidence cut-offs (0.9, 0.75) were read off that data. No unseen deal has been tried (Penford and sTec are candidates once they have graded ledgers), no ordinary cheap language model was run on the same questions for comparison, and nothing was repeated to measure run-to-run variation.

## Practical

- The scripts here need the nine comparison workbooks and saved API responses, which are in git history. From the project's top folder:
  `git checkout f1de7d9 -- _dev/jev_experiments_2026-09-19 _dev/jev_round3_2026-09-19 _dev/typesafe_followup_2026-09-19 _dev/model_comparison_2026-09-19/workbooks && git reset -q`
  With saved responses restored, reruns make no new API calls.
- New calls need `TYPESAFE_API_KEY` set in the shell. The key is in no file, on purpose. The key used on 19 September was pasted into a chat and should be replaced.
- Model used: `jev-1.13.0`. Docs: https://docs.typesafe.ai/llms.txt
