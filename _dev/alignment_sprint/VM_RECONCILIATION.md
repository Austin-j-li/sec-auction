# VM against the laptop: where things stand and how to proceed

27 September 2026, evening. Four read-only agents worked from a snapshot of the VM. Nothing on the VM was changed. The lane reports are in `vm_check/`: lane A covers recovery, lane B today's activity, lane C decisions and lane D operations. Nothing here is approved.

## 1. Facts

- **Same instruction.** The laptop's v0 is the VM's v1.14.1 text byte for byte except the title line. The cockpit's current default is therefore the base the sprint audited.
- **Nothing happened on the VM since 26 Sep 20:52 UTC.** No runs, instruction changes, commits or activity from Alex. The last cockpit write was the fifth v1.14.1 retest import at 20:41. The 19:59 file change today was an idle old session writing bookkeeping lines. Someone read every deal through the public URL at 10:54 today, reads only; this was probably the laptop recovery.
- **The VM still has work the laptop does not.** Both VM checkouts sit at `679d4fc` (23 Sep) with uncommitted work: 99 paths in the main checkout and 78 in `sec-extraction-v114`. The laptop's recovery commit `ae03c85` holds reconstructions or nothing for much of it:
  - the exact cockpit code, including the frontend modules `bulk.js`, `choices.js` and `downloads.js`;
  - the root `HANDOFF.md`;
  - the 15-run trial packets and the Pro review;
  - the evidence for the Astra-default verification;
  - the V114_SPEC analysis files;
  - the staleness-cleanse folder;
  - the filings of the four deals added in the app.

  The laptop's own `_dev/recovery/GAP.md` already names these gaps, so nothing was lost without anyone knowing. None of it is on GitLab yet.
- **The live app runs from that uncommitted checkout.** The worker starts the checker and runner fresh for each job. Any file change there takes effect on the next request or job, without a restart.

## 2. Decisions: the VM's rulings against today's sprint

Today's spec is a compatible successor. Every sprint decision is later than every VM ruling, and most rest on Alex's words, so they override under the working rule. The sprint knowingly changed the v0 sentences involved. What it did not say is that many of those sentences were Austin's own 25–26 Sep rulings. The change map should name each one. The main reversals are listed below; lane C has the full list, C1–C18.

| VM ruling (25–26 Sep) | Today | Basis |
|---|---|---|
| Copy an offer only when the bidder says it stands | F2: Bid reaffirmed copies the price | Alex V¶30 |
| Datalink: four rounds from the text; the same reasoning applies to Kraton (two rounds) | Kraton three rounds; Datalink four rounds on a different map (round 1 in June); Meredith no whole-company rounds | Alex V¶82, V¶173; R5; Meredith ruling |
| H2 counts only a period for diligence alone | F4: a bundled period counts | Alex V¶19 |
| Silent diligence with committed financing is Unclear | F5: silence on a Formal bid is None | Alex V¶125, V¶183 |
| Exclusivity never changes Conditions | Required exclusivity means at least Light | Alex V¶19 |
| An offer-less selection opens no round | R1 and R2 | Alex V¶44, V¶82, V¶173 |
| sTec: one process, May 16 is the final round | Two processes; May 29 is the final round | Alex V¶118, V¶124–125 |
| "mixed" initiation dropped; Alex's flag list not mandatory | "mixed" restored; uncapped Review items | Alex |
| Route 1 accepts a commitment letter or a markup sent separately | F9 and F1 | Alex V¶47 |

**Additions the spec needs before drafting (all small):**
1. **Name the overturned VM rulings** in the change map (C1–C16).
2. **Turn the 26 Sep retest acceptance checks into fixed test cases.**
   - Intended reversals: sTec rounds, Providence Party E, the Datalink round 1 date, Synacor.
   - Results that must survive:
     - Mac-Gray's 16 financial signers closed by Jul 23.
     - The blank-price commitment Bids.
     - Mac-Gray Party A Sep 18: Heavy and Formal.
     - Providence's 16 non-submitters.
     - sTec Company H.
     - The WDC standstill row.
3. **Place Synacor's reopening round.** The round map must say whether Oct 27 survives next to Dec 30, and which part of trigger (d) fires.
4. **Settle two VM open issues nobody decided:**
   - **The process Question** fires even when the defaults already settle the outcome.
   - **Other-scope bid rows** (every Meredith bid) are still required to carry Formality and Conditions.

   My defaults, pending your ruling:
   - Ask the process Question only when the defaults leave the outcome open.
   - Leave Formality and Conditions blank on Other-scope rows. The Meredith ruling already treats those bids as Note-only.
5. **Analysis tool:** a copied F2 price is not a new price observation, and the same-offer switch covers F2 rows.
6. **Record the dropped Alex items** (which source governs, Penford Party A, the exit-reason merge) as closed by the working rule or deferred. DECISIONS says none are open, but STATUS still lists them.

## 3. Operations

- **Replacing the VM's tools with the laptop's v0 tools would break the app.** Every deal page, every run's check step (after the paid extraction), editing, and Add Deal would fail. Checking out the laptop branch in the live folder would delete the app, the catalog and the nine starting workbooks.
- **The VM's checker 1.8 already checks v0 correctly.** v0 has the same hash rules and the same 29 columns as v1.14.1; both checkers gave identical counts on the five 26 Sep runs. STATUS is wrong that v0 tools "reject" old ledgers. On v1.13.2 workbooks, which all 13 working copies are, they produce a column error followed by dozens of knock-on errors.
- **Two VM handoff gates are now harmful:**
  - `export_repo.py instruction v1.14.1 --write` would overwrite the v0 file.
  - Gate 12 moves the extraction workbooks.

  Withdraw both.

## 4. How to proceed (each step needs Austin's go-ahead)

1. **Save the VM's work now, without touching the live files.**
   - Take a fresh backup of the app's state.
   - In the main VM checkout, run `git switch -c vm-live-2026-09-26`, commit by explicit paths (leave out `dist.old/` and `lesson/`, scan the staged files for secrets) and push.
   - Do the same for the `sec-extraction-v114` worktree.

   This is safe: switching to a new branch at the same commit changes no files under the running services.
2. **Treat the VM branch as the app's history and the laptop branch as the research line.** Do not merge them into each other; that would give about 100 modify/delete conflicts. No force-push is needed.
3. **Add the six items in section 2 to DRAFTING_SPEC**, including your rulings on item 4.
4. **Draft Version 1 on the laptop**, building the §6 tool changes on the laptop's v0 tools. In the change map, list the app adapter as later VM work: a `rules=` argument, `choice_lists()` for the current format only, and `fetch_filing.index_link`.
5. **Deploy Version 1 to the app deliberately.**
   - Build it in a separate VM worktree from the VM branch.
   - Run all the test suites against a copy of the app's state.
   - Then do one ordered restart that also installs the TMPDIR fix and removes `dist.old`.
   - Rollback: point the services back at the old folder.
6. **Decide what happens to the app's old data at that deploy.** The eight hand-edited working copies hold 454 reviewed row marks; Providence alone has 16 revisions.
   - My recommendation: archive them, start Version 1 with a fresh catalog, and carry the reviewed judgments into the Version 1 review by hand.
   - The alternative, keeping them editable, means rebuilding the migration tool the v0 reset deleted.
7. **Skip publishing v0 in the app.** It is the same text as the current default, and re-extracting under it would be spent before Version 1 lands.
