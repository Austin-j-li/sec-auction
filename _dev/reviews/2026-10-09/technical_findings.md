# Source and implementation findings

Reviewed repository: `2e781023289eab42b7a3ead0b8d5977525450211`.
Deployed source: `9f0750e0a5663fd9f5dbba622373da5da4591957`.

Three Astra reviews and a Sol implementation review supplied these findings. The root agent reconciled them with the live inventory and browser.

The findings support source correction before research use and isolation repair before further blind extraction. Proposed repairs below are not implemented changes.

## Findings with direct research effects

### Datalink round and participation error

**Priority: high. Actual live output.**

Input: `versions/datalink/opus55-medium-20260928-1531-b29df5/datalink.xlsx` under the live state directory.

- `Rounds!B2:B5` records four rounds.
- `Deal ledger!E38/G38` assigns the August 16 letter to Deadline set, round 2.
- `Deal ledger!B42/E42/T42` closes two unnamed parties as Did not submit on August 30.
- `Questions!C4` assumes the unnamed parties were implicitly invited to submit final proposals.

The filing names five admitted parties on July 27 at `raw_filing/datalink_2016-11-29_DEFM14A.htm:3305`. The August 16 letter names only Insight, Party B, and Party C at line 3332.

Instruction lines 193–197 require a new round for this narrower common request. Lines 328–336 close uninvited parties at that opening, absent a later target admission. `ROUND_MAP.md:46` and `DECISIONS.md:267` record the approved result.

The output understates rounds and retains two bidders for 14 extra days. The October 26 opening exists at Excel row 70; its Round becomes five after the missing stage.

Smallest consumer verification: open the two filing passages beside Excel rows 38 and 42 and `Questions!C4`. Review all dependent round assignments and exits together.

### Price reversion and observation masks

**Priority: medium. Verified effect in current analysis.**

Location: `derive_analysis.py:713–772`; related checker at `check_lean.py:919`.

Providence Party E's live ledger records:

| Ledger event | Date | Price | Representation |
|---|---|---:|---|
| #33 | Late July | 21.26 | Original offer |
| #50 | August 1 | 23.81 | Revised offer |
| #52 | August 2 | 21.26 | Same as #33; withdraws #50 and confirms original |

Filing page 30 confirms this sequence. Instruction E10, line 253, makes a return to an older price a revision.

Current code assigns zero to both price-observation masks for #52. Deployed code assigns one to both. The new suppression trusts the `Same as` label without a check for an intervening different price.

This is an output contradiction with a measurable analysis effect. It does not show that suppression of ordinary copied prices is wrong.

Proposed repair: flag references that cross an intervening different price. Resolve the ledger classification before the mask discards the observation.

Consumer evidence: the reviewer derived the actual saved Providence file and inspected events #50 and #52 with the source. No workbook edit occurred.

### Qualified total versus residual count

**Priority: medium. Verified unsupported lower bound.**

Location: `derive_analysis.py:257–262`; qualifier bound at line 93.

Medivation ledger #9 represents Other NDA signers. Its Note qualifies the total as several parties, includes Sanofi, and subtracts Sanofi and possibly Pfizer.

Filing page 22 reports several total signers, including Sanofi. Pfizer already signed. The parser reads the qualifier but ignores the residual arithmetic.

Current output gives the residual cohort `count_lo=2`, then process `live_lo=4`. The source does not establish two additional signers. The workbook's Auction screen reports only at least two parties overall.

Deployed code gives three through its unparsed-count fallback. Neither treatment resolves the residual arithmetic. The quoted-qualifier change increases the unsupported minimum.

Proposed repair: distinguish a total qualifier from a residual qualifier. Preserve uncertainty where subtraction cannot be resolved.

Consumer evidence: derive Medivation and inspect participation event #9 against its Note and page 22.

### Cumulative participants versus simultaneous participants

**Priority: medium. Verified false inconsistency warning.**

Location: `derive_analysis.py:830–833`.

Synacor process 3, round 3 contains Company E and CLP. Company E leaves on December 14. CLP returns on December 18–21.

The maximum simultaneous live count is one. The round nevertheless contains two distinct participants. The program incorrectly compares the latter total against the former maximum.

The same comparison mixes contacts and entrants: Mac-Gray lists 50 contacts against 20 maximum live entrants; Imprivata lists 15 against seven.

D3 describes stage invitations. E3 describes entry through NDA, bid, or admission. Neither cumulative invitations nor all contacts must equal simultaneous live entrants.

The Synacor false warning exists in both deployed and current code. The latest maximum correction does not repair this population mismatch.

Proposed repair: compare equivalent populations. Keep invitations, distinct participants, and simultaneous competitors separate.

### sTec deadline outcome and grader conflict

**Priority: medium. Actual live and comparison output; flawed saved evaluation claim.**

Location: comparison `stec-opus-5-5-medium-r1.xlsx`, `Rounds!G2/J2`, and the live sTec file's same cells.

The output calls May 3 Extended (late bid accepted). It treats Company D's May 10 document as the late required response. Six other comparison setups give the same outcome; Astra medium uses Extended; Enforced.

The filing records D's verbal offer above $5.60 on April 23, at `raw_filing/stec_2013-08-08_DEFM14A.htm:2374`. Line 2397 describes its later document as confirmation. The next-stage letters appear at line 2432.

The approved correction at `DECISIONS.md:265` says Enforced. `ROUND_MAP.md:65` explains that May 10 is a revision, not a missing required response.

The Sonnet comparison grade endorses Extended at `verdicts/sonnet55_stec.md:6`. The Sol grade claims verification of the shared outcomes at `verdicts/sol61_stec.md:21–29`.

A blind grade and model agreement can therefore preserve a shared error. This error concerns deadline discipline, not workbook polish.

Separate limit: Alex calls this a soft deadline at voice paragraphs 122–124. The approved Enforced convention uses the later May 15–16 selection. Do not equate that label with timely deadline discipline.

## Blind extraction and the live app

### Shared network defeats the intended evidence boundary

**Priority: high. Capability verified; historical use unproved.**

Location: `sandbox/run_model.py:381` uses `--share-net`. Codex bypasses its own sandbox at line 458. Claude retains shell access at lines 467–468.

The server's read routes return deal data without verified identity authorization; see `cockpit/server.py:153`. Write protections and the effective Access flag do not change that read-route behavior.

A benign bubblewrap request with the same network flags reached the deal API. It returned HTTP 200 and 13 deals. No further access probe followed once reachability was established.

An extractor can therefore reach other workbooks, review material, or external sources through shell commands. Tool-level web bans do not prevent that route.

This proves an access capability, not actual contamination. No evidence shows that a saved extraction used it. File hashes establish current integrity, not isolation during the original run.

Proposed repair: deny general network and host-service access while retaining a narrow provider route. After repair, use the same benign consumer request to inspect access behavior. Do not start a paid extraction to establish that barrier.

### Mandatory-review integration is not deployed

**Priority: medium. Deployment gap, not missing GitHub implementation.**

Current `cockpit/data.py:1039–1057` derives the queue. `frontend/src/Review.jsx:89–125` displays it.

The adapter consumed all 13 immutable live workbooks. It returned 193 prompts without errors, including ten for sTec, 19 for Synacor, and two for Meredith.

The deployed files omit this adapter and panel. The live browser's sTec Review tab shows only recorded findings and mechanical checks.

Proposed next verification: after an authorized release, open that tab and inspect the ten prompts. Then verify their source meanings. A visible prompt is not an accepted finding.

### Publication does not compare the displayed instruction hash

**Priority: medium. Latent source-verified defect.**

Location: `cockpit/instructions.py:238–246`; frontend `Instructions.jsx:144,309`.

The dialog says publication freezes the displayed text. The request sends no displayed hash. The server selects the latest draft and publishes it without a hash comparison.

If another user saves a new draft after the first user opens the dialog, the first user's action can publish unseen text. Publication attribution then names that user's account.

Draft saves contain a conflict check. Publication lacks the equivalent guard. This behavior exists in both reviewed states. There is no evidence that it occurred.

A future consumer verification should use a disposable workspace and two tabs. It should inspect the published text and conflict response. No write-flow verification occurred on the live app.

### Row review state survives a data edit

**Priority: medium. Latent source-verified defect with partial mitigation.**

Location: `cockpit/workspace.py:784–788,839,853`; `frontend/src/Records.jsx:191,205`.

Single and bulk updates retain `row_review`. The record lacks a revision or content hash. The interface displays the retained Reviewed mark after the content changes.

A price or exit edit can therefore leave an obsolete row mark. The whole-deal edited-since notice partly mitigates this. No current false acceptance is established; all current live deals remain Unreviewed.

A future consumer verification should mark and edit a row in a disposable workspace. It should inspect the row status and whole-deal warning.

### Data destinations still use the work disk

**Priority: medium. Current path design conflicts with the supplied storage rule.**

Location: `cockpit/deals.py:69,74–78,209–212`; `fetch_filing.py:36,215,229`.

The app writes filings and lookup submissions beneath its state directory. The CLI writes beneath `raw_filing/`. Current resolved paths are ordinary work-disk directories.

These destinations do not meet the supplied RDSS rule for ingested data and adjacent receipts. Retained files predate 5 October; this review does not allege a later download.

Future path changes must preserve frozen hashes. Copy and compare each frozen file before a link replaces its old path. Keep derived results with the project.

The work mount currently has 294 GB free. This review does not claim imminent exhaustion.

## Comparison evidence and its limits

### Imprivata supports a narrow Opus advantage

The retained source is the live added filing, `imprivata_2016-08-10_DEFM14A.htm`. At line 2152, Sponsor B describes a price it would offer if it submitted. Line 2184 says only Thoma Bravo submitted on July 8.

| Comparison output | Representation |
|---|---|
| Sol high | Formal Bid at `Deal ledger!E43/M43`; Not selected at signing at E54. |
| Sol xhigh | Formal Bid at E41/M41; target exit on June 30 at E43. |
| Astra medium and high | Repeat the Formal Bid and June 30 exit. |
| Opus medium | Other material event at E35; Did not submit July 8 at E41. |

The source supports the saved Opus preference on these consequential fields. It does not establish a general model ranking.

### Graded files and live files differ

Hashes and cell contents establish these differences:

| Deal | Graded Opus medium file | Live Opus medium file |
|---|---|---|
| sTec | 66 ledger events | 63 ledger events |
| Imprivata | Two processes; bidder-led | One process; mixed |

Live Imprivata `Deal facts!B10:B12` records the one-process view. `Questions!C4` excludes the 2015 approaches because no proposal occurred. The saved grade rejects that interpretation in `sonnet55_imprivata.md:22,48`.

The source dates the named bidder's first contact to June 2015 and its next contact to January 2016. Process treatment needs explicit source adjudication. A comparison grade cannot transfer across different files.

### The reference workbook is not unquestioned ground truth

The team verified three material reference conflicts:

| Reference cells | Source |
|---|---|
| Meredith `deal_details!U539:W539`: 15.51 | Filing line 9115 says 16.51. |
| Kraton `deal_details!V108:W108`: 42–42 | Filing line 2656 says 42–45. |
| Datalink `deal_details!AB2872/AC2872`: November 1, Executed | Filing line 3567 places $11.25 on November 2; line 3633 places execution on November 6. |

These confirm inherited findings W35, W32, and W33. Preserve the difference between source fact, research convention, and reference error.

### No general accuracy claim follows

There are two deals and one extraction per setup. The same Opus medium output is reused across two grades. Opus supplies all saved grades. Opus high and Astra remain ungraded in the retained evidence.

sTec supplied several rules during development. The saved grades do not separately report those codings as ruling 9 requires. The original prompts, event logs, and sandbox inputs were deleted after the comparison record.

The retained evidence supports a provisional extraction default. It supports neither generalization nor acceptance of the 13 live files.

## Consumer checks completed

The current checker consumed all 13 live workbooks with their real filing paths. The reviewer printed results without assertions or a test suite.

| Diagnostic | Stored receipts | Current checker |
|---|---:|---:|
| Errors | 52 | 51 |
| Warnings | 40 | 42 |

Only three issue changes occurred. Medivation's quoted-count error disappeared. Medivation and PetSmart each gained one deadline-extension warning.

Current errors are Meredith 41 Count errors, Synacor eight quote errors, Datalink one inferred-event error, and Providence one exact-date error. Neither this total nor quote location establishes source accuracy.

The recent code makes useful corrections: known cohort members no longer add another entrant; ordinary copied offers no longer add a price observation. Equal inexact entry and exit counts can cancel. Round maxima use the corrected opening state.

T0–T3 remain distinct, with no selected primary interpretation. The reviewer found no further actionable defect in the inspected partial-scope, coalition, or variant logic. This is a bounded result, not exhaustive correctness.

The review did not run paid extraction, test suites, backup restoration, or live write-flow checks. It did not change source code, the instruction, or any input workbook.

## Source paths

The [live inventory](live_inventory.md) records every live version ID. All live workbook paths follow:

```text
/home/uctpiaj/work/Projects/ledger-live/_dev/cockpit/state/versions/<slug>/<version-id>/<slug>.xlsx
```

Core repository sources:

- [Instruction](../../../SEC_Deal_Ledger_Extraction_Instruction.md).
- [Analysis derivation](../../tools/derive_analysis.py).
- [Mechanical checker](../../tools/check_lean.py).
- [Sandbox runner](../../tools/sandbox/run_model.py).
- [Cockpit server](../../tools/cockpit/server.py).
- [Decision log](../../alignment_sprint/DECISIONS.md).
- [Model comparison](../../model_comparison_2026-09/README.md).

Line references use the reviewed commit. Workbook references distinguish Excel coordinates from ledger event numbers marked with #.
