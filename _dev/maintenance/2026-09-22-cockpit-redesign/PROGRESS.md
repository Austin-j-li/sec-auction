# Ledger cockpit redesign: progress at the wrap-up checkpoint (22 Sep 2026, about 23:20)

> **Status, 23 Sep 2026:** Fable signed off after round 2 (round-1 fixes below). The build was deployed to `dist/` and `ledger-cockpit.service` restarted, and test_browser passed 46/46 against the deployed build. The COCKPIT_BUILD "Design" note is written. Known issues 4 and 7 are closed. The desaturation check (item 10) passed in Fable's review. The `before/`, `after/` and `preview-dist/` paths below refer to scratchpad copies that were not kept, and the one-off preview and capture scripts were removed. Statements below that `dist/` or the service were untouched describe the state before deploy.

Nothing is committed, and `_dev/tools/cockpit/dist/` is untouched (`git status` shows no changes there). The live service on port 8778 was not touched. Preview servers: 8791 (synthetic fixture, restarted once to reset its state) and 8792 (real catalog, read-only), both serving `preview-dist/`.

## Checklist against DESIGN_BRIEF.md

### §3 Tokens
- [x] 3.1 Colour: one `:root` block with all brief tokens. There are no hex values outside `:root`, no `!important` and no `text-transform`.
- [x] 3.2 Type: Cabinet Grotesk, IBM Plex Mono and Source Serif 4, self-hosted in `src/fonts` with `@font-face` and `font-display: swap`. Figures, dates, ids and codes are mono with `tnum`. The filing is set in serif at 15/24 with a 66ch measure. Nothing is below 12 px.
- [x] 3.3 Fluent theme: `createLightTheme(brand)` plus the brief's overrides in `src/theme.js`, applied through `<FluentProvider theme={cockpitTheme} className="cockpit">`. `webLightTheme` is gone. I also added hover and press tokens (tint and rule) from the same neutral family.
- [x] 3.4 Space, radius, rules, elevation and z-index are tokenised. Controls are 28 px and icons 16 px.
- [x] 3.5 Motion: transitions are 120 ms and colour-only. `<details>` and banners use 180 ms. The GSAP fade is opacity-only at 0.24 s. The selected quote flashes once. With reduced motion all durations are 0 and the flash is off.

### §4 Components
- [x] 4.1 Global bar: 40 px, a text wordmark (Fluent subtle `button.wordmark`), the context after a rule, and access as dot plus text. The favicon and theme-color are in `index.html`. See the known issues for the favicon's location.
- [x] 4.2 Overview: ruled table with one heavy head rule. Deal names are real `<a>` links, while row click, Enter and Space still open the deal. Numbers are mono and right-aligned. Review state is shown as the raw API string. The "Location aid, not validation" note appears once, as a footnote. The eyebrow and ghost numeral are gone.
- [x] 4.3 Deal bar: one 56 px row at 1440. The subline is mono and reads "… · from <base> · Revision N". The Version select is 240 px wide, with a lock glyph and a `title` when the version is read-only. "Export Excel" is a Fluent `Button as="a"`. The work-state dot sits beside Save, and "Last saved by" moved to the History head and the work-state `title`. Under 820 px the bar stacks. Deviation: at narrow widths the work-state sits on the Version row rather than below the buttons, to meet the checklist's 260 px chrome budget.
- [x] 4.4 Tabs: ink underline, mono counts, no chips, and the native scrollbar hidden. Added `id`, `aria-controls`, `aria-labelledby`, arrow-key, Home and End roving, and `tabIndex=-1` on inactive tabs.
- [x] 4.5 Event rows: ruled two-line rows. Line 1 holds the mono number and date, `p. N` and a review dot. Line 2 holds the title and a truncated detail, with the full text in `title`. The selected row has an accent rule and tint. The compact strip uses 168 px rows. Sheet items follow the same recipe.
- [x] 4.6 Editor:
  - the `#N` is mono;
  - Move up, Move down and Clone to split are subtle buttons, with Delete set apart in error text;
  - the source summary is a single line;
  - issues are a ruled glyph list, errors first, capped at 5 with "Show N more";
  - fields with issues show a severity glyph after their label;
  - the evidence field comes first, in serif, spanning both columns;
  - numeric and date inputs are mono;
  - textareas grow with their content up to 40vh and keep `resize: both`;
  - reference links are subtle accent buttons;
  - Row review is a ruled section with its explanation moved into the Status hint;
  - edited fields show a warning left rule and "· edited" (aria-hidden, so accessible names are unchanged).
  - Not applicable: the separate "Page" input the brief mentions. The data has only the combined "Quote and page" column.
- [x] 4.7 Filing:
  - one tools row that wraps under 1200 px;
  - no grey well and no paper shadow;
  - page markers are mono, and "(approximate)" carries a warning glyph;
  - table rows are mono `pre` in `overflow-x` blocks;
  - a "Background section" label marks the background start;
  - three highlight states: quote, selected (darker fill plus underline) and search (wash plus dotted underline, with an outline on the current hit);
  - the selection bar sits on the ground colour with a primary button;
  - page errors and filing errors are banners.
- [x] 4.8 Review:
  - a left-aligned 880 px column, with the intro as a single 12 px note;
  - a mechanical summary with mono counts and a verdict dot;
  - ruled issue list;
  - documents as link buttons;
  - finding rows show a dot and the lowercase judgment;
  - labelled paragraphs;
  - evidence in serif with the same yellow mark as the filing;
  - the recheck banner is `role="status"`.
- [x] 4.9 Changes and History:
  - ruled entries, with Before and After in sentence case plus a glyph;
  - inserted rows render as `dl` field: value lists instead of JSON;
  - removed text is error with line-through, added text is success;
  - history uses the caret summary with body text in ink.
- [x] 4.10 No badges anywhere: status is always a dot or a glyph plus text.
- [x] 4.11 Version picker: see 4.3.
- [x] 4.12 Buttons: all Fluent, in primary, secondary and subtle only. `.back-link` and `.wordmark` are Fluent subtle buttons. "Stage deletion" is secondary with error text and border. The tab-scroll arrows stay native, because they are test-pinned custom controls.
- [x] 4.13 Inputs: theme outline, 28 px, placeholders in ink-3. Read-only fields render as paper with ink-2 text, which needed `opacity: 1` to undo Chrome's disabled-select dimming.
- [x] 4.14 Focus: one 2 px accent ring on rows, tabs, finding titles, summaries, overview rows (the old outline removal is gone), splitters and tab arrows.
- [x] 4.15 Scrollbars are thin and grey. Splitters are 1 px lines that thicken to 2 px accent. The save dock is docked at the bottom of the workspace column on desktop and fixed on narrow screens. Modals and banners are restyled, with error text first and the server string in mono second. The unknown-deal banner has an "All deals" button. Loading shows a tiny spinner, left-aligned. Empty states show a Tray glyph and a sentence. A version switch keeps the filing mounted.
- [x] 4.16 Narrow: three-row deal bar, a segmented pane switch with `aria-pressed`, the compact strip and a fixed dock. Chrome at 400 px measures 255 px on Datalink.

### §5 Constraints
- [x] 5.1 Selectors, ARIA, strings, native selects and `window.confirm` are kept. All five suites pass.
- [x] 5.2 Fluent 9.72.3 and Phosphor only. No new dependency: the fonts were copied via `npm pack`.
- [x] 5.3 Yellow quote scheme: see 4.7.
- [~] 5.4 Accent `#1f4f99` is applied. **Not done: the note in `_dev/COCKPIT_BUILD.md` "Design".** My instructions limited me to frontend files.
- [x] 5.5 Capitalize removed. No `text-transform` anywhere.
- [x] 5.6 Built only with `npx vite build --outDir preview-dist`.
- [x] 5.7 Research text is not truncated, except list rows, whose full text is in `title`.
- [x] 5.8 Mega components split into `Overview.jsx`, `Records.jsx`, `Review.jsx` and `ui.jsx`, with `theme.js` separate. `style.css` rewritten unminified in the required order.
- [x] 5.9 and 5.10: minimum 12 px; `role="alert"` only on error banners.

### §7 Review checklist
| # | Status | Note |
|---|---|---|
| 1 | pass | Probe on the ledger: 112 text nodes in Cabinet, 34 in Plex Mono, 68 in Source Serif, 0 in any other face. |
| 2 | pass | Scripted check of `style.css`. |
| 3 | pass | Visual check of d02, d05, d07, d18 and r01. |
| 4 | pass | r01: the review state renders as "unreviewed; Austin review pending". |
| 5 | pass | 1440: 40 + 56 + 35 (tabs) + 47 (section head). 400: 255. |
| 6 | pass | |
| 7 | pass | |
| 8 | pass | |
| 9 | pass | The save dock is docked. test_responsive confirms it at 1024×600. |
| 10 | pass | Visual check. I did not run a desaturation check. |
| 11 | pass | r03 and r04. |
| 12–14 | pass | |
| 15 | pass | |
| 16 | pass | Tab-walk probe: 2 px accent ring. Scrollable filing table rows were `tabIndex=-1` to avoid a flood of tab stops; see the known issues. |
| 17 | pass | |
| 18 | pass | d32, d33 and d20. |
| 19 | pass | The responsive matrix has no document overflow at any width. |
| 20 | pass | |
| 21 | pass | |
| 22 | partial | The favicon ships as a hashed asset. |

## Files changed (all under `_dev/tools/cockpit/frontend/`)
- Modified:
  - `index.html` (theme-color and favicon link)
  - `src/main.jsx`
  - `src/Filing.jsx`
  - `src/SplitPane.jsx` (grip span removed)
  - `src/TabScroller.jsx` (arrow roving)
  - `src/style.css` (full rewrite)
- New:
  - `src/theme.js`, `src/ui.jsx`, `src/Overview.jsx`, `src/Records.jsx`, `src/Review.jsx`, `src/favicon.svg`
  - `src/fonts/ibm-plex-mono-{400,500}.woff2`
  - `src/fonts/source-serif-4-{400,400i,600}.woff2`
- Not changed: `package.json`, `package-lock.json`, `vite.config.js`, backend, tests.

## Packages
- None added. The font files come from `npm pack @fontsource/ibm-plex-mono@5.3.0` and `@fontsource/source-serif-4@5.3.0` (OFL, latin woff2), unpacked in `scratchpad/fontpack/`, per brief §3.2 and §5.2.

## Test results (against `preview-dist`; evidence in `scratchpad/redesign/after-tests/`)
| Suite | Result |
|---|---|
| test_browser.mjs | 46/46 passed |
| test_resize.mjs | passed |
| test_responsive.mjs | passed. Matrix: columns at 1440 and 768, compact elsewhere; the editor is at least 390 px wide everywhere. |
| test_http.py | 11 passed |
| vitest | 3 passed |

No test edits.

## After screenshots
- `scratchpad/redesign/after/`: 62 PNGs with the same names as `before/`.
- Script: `capture_after.mjs`.
- The fixture must be fresh: restart the 8791 server before re-capturing, because the script saves revisions and expects "Revision 1".

## Known issues
1. **Favicon.** `server.py` serves only `/assets/`, `/fonts/` and the index, so a `public/favicon.svg` would get index.html back. The icon therefore lives in `src/favicon.svg` and Vite emits it as `/assets/favicon-<hash>.svg`. It works through the real server. The test harness routes serve `.svg` as text/html, which is harmless there.
2. **Filing table rows.** EDGAR table rows that overflow horizontally become Chrome "keyboard-focusable scrollers". Each one gets `tabIndex=-1`, so they are not dozens of tab stops, but those rows can only be scrolled sideways with a pointer or trackpad.
3. **Narrow work-state.** At 820 px and below, the work-state sits beside the Version select, not under Export and Save (see the 4.3 deviation).
4. **Findings have no dirty marker.** Finding decision fields show no per-field "edited" marker. The editor, the Row review Status and the Review note do.
5. **Record paths in Changes and History.** The `record_label` strings come from the server, so the ids inside them are not set in mono.
6. **Long event dates.** In the 250 px event list, long "When" strings ("June 2016 or later") are ellipsised. The full text is in `title`.
7. **Not written: the brief's `_dev/COCKPIT_BUILD.md` note** about the accent (§5.4).

## Exact next step
Review `after/` against `before/` with the art director. If it is approved:
- add the accent line to `_dev/COCKPIT_BUILD.md` "Design";
- run the desaturation check for checklist item 10 on d08 and r04.

Then deploy to `dist/`, and only with Austin's authorisation.

## Round 1 fixes (23 Sep 2026, art-director punch list)

Still uncommitted; `dist/`, backend, tests and `package.json` untouched. Preview rebuilt with `npx vite build --outDir preview-dist`; 8791 restarted before recapture.

| # | Status | What was done |
|---|---|---|
| 1 MUST | done | `.issue-code` no longer has `overflow-wrap: anywhere`. In `@container (max-width: 440px)` the issue grid is `16px minmax(0,1fr)` and `.issue-message` sits in column 2, so glyph + code are line 1 and the message is indented under the code (n02, m-850). |
| 2 MUST | done | `HistoryTab`: the meta line renders only when `at` or `actor` exists, joined with " · " only when both do (r11: Revision 0 has no stray dot). |
| 3 MUST | done | Subline parts are `<span>· part</span>` with a plain space between spans, so a wrapped line starts with "· " and never ends with one (n02, r12). "Revision N" and "Source version" substrings unchanged. |
| 4 MUST | done | New `@media (min-width: 821px) and (max-width: 1150px)`: `.deal-identity` is `display: contents`, so "All deals", the h1 (`flex: 1 1 0`) and the actions share line 1 and `.deal-subline` (`flex-basis: 100%; order: 1`) runs full width on line 2. Toolbar side padding `--sp-4`, Version select 172 px in that range. Measured bar height: 63 px at 850, 1024 and 1150 for the fixture and 8 of 9 real deals; Providence & Worcester's long name wraps to two lines at 850 (87 px). Nothing hidden. |
| 5 SHOULD | done | `.tab-strip.has-overflow .tabs` gets a mask that clears the 8 px scroller padding and fades to opaque at 20 px on both ends, so a clipped label no longer peeks beside an arrow (n08). No snap (avoids interfering with `keepActiveVisible`). |
| 6 SHOULD | done | `.split-handle` removed from the shared outline rule; `.split-handle:focus-visible { outline: none }` with a comment, since the 2 px accent `::before` rule is the focus indicator (d12). |
| 7 SHOULD | done | `13.5px` → `var(--fs-13)`. |
| 8 SHOULD | done | Delete modal title is `Delete <span class="mono">#N</span> Event?` for ledger rows (`idLabel` split from `label`); dialog name stays `aria-label="Delete record"` (d23). |
| 9 SHOULD | done | `.history-summary` is suppressed when it equals `count(changes.length, 'change')` (the server writes exactly that string); kept otherwise (d27). |
| 10 SHOULD | skipped | test_resize pins `.other-sheet > .section-head h2` as a direct child of `.other-sheet`, so the head cannot move into `.sheet-list`; `--split-size` lives on `.sheet-body`, a sibling, so CSS cannot size the head to the list column either. Left as is (d13). |
| 11 SHOULD | done | `.record-actions` gap is `var(--sp-3) var(--sp-2)`, so a wrapped Delete gets 8 px row gap. |
| Known issue 4 | done | Finding judgment, Correction implementation, Verification and Decision note get `.is-dirty` and the aria-hidden "· edited" label (shared `fieldLabel`, now exported from `Records.jsx`). `main.jsx` records each finding's loaded values on first edit (`findingBase`, reset when ops empty) and `findingDirty(id)` compares the staged op against them, so reverting a value clears its marker. |

Tests against the new `preview-dist` (evidence in `scratchpad/redesign/after-tests/`): test_browser 46/46, test_resize pass, test_responsive pass, test_http 11 passed, vitest 3 passed, unittest 128 OK. No test edits. `capture_after.mjs` re-shot all 62 screenshots into `after/` with no page errors. Style checks: 0 `!important`, no hex outside `:root`, no size below 12 px, no off-scale sizes.
