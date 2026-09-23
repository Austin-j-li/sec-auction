# Ledger cockpit: pre-redesign audit

> Note (23 Sep 2026): the screenshot and build folders this audit refers to (`before/`, `baseline/`, `preview-dist/`) lived in a session scratchpad and were not kept.

Audited 22 September 2026 on branch `extraction-v2` (HEAD `da70736`, clean tree). No source files, no `dist/`, no live service state were touched. Every path below is relative to `_dev/tools/cockpit/` unless it is absolute.

- Screenshots: `before/` (62 PNG files plus `before/index.json`)
- Preview build: `preview-dist/`, byte-identical to the live `dist/` (same asset hashes `index-CJ4TqS6Y.js` and `index-DckwINfp.css`)
- Preview server: `serve_preview.py` · capture script: `capture_before.mjs`
- Baseline test logs: `baseline/*.log`. All five suites pass on the current build.

---

## 0. What matters most (read this first)

1. **The seeded font never renders.** `style.css:4` sets `font-family: Cabinet` on `:root`, but `FluentProvider` (`main.jsx:434`, `webLightTheme`) re-declares `"Segoe UI", -apple-system, BlinkMacSystemFont, Roboto…` on its wrapper and on every Fluent control. A computed-style probe counted 135 text nodes in Segoe/system fallback, 67 in Georgia (the filing), and **1** in Cabinet (`.page-marker`). The 500 weight is never requested (`document.fonts` reports it `unloaded`). On Austin's Mac the whole UI renders in SF; on Linux it renders in Roboto. That fallback is the main reason the app "looks like a default".
2. **There are no design tokens.** `style.css` has **157 distinct hex colours**, zero CSS custom properties (the only variable is the `--split-size` layout var), 19 font sizes from 9 to 72 px, 6 radii and 18 `!important` overrides fighting Fluent. A redesign should start by introducing a token layer.
3. **The "sheets" are not sheets.** Each of Ledger, Rounds, Questions and Deal facts is a *list of cards plus a two-column form for one record* (`main.jsx:391`, `main.jsx:421`). Nowhere can a researcher see the ledger as a table or compare rows. This is the biggest structural gap for a "spreadsheet-like" review tool. Changing it is a product decision, and the tests pin the list+editor DOM (§4).
4. **The live service serves `dist/` straight from this checkout** (`server.py:134-146` reads files per request; `dist/` is committed to Git). `npm run build` writes to `../dist` with `emptyOutDir: true` (`frontend/vite.config.js:6`), so a plain build **changes the live site immediately**, and it breaks the site while the folder is empty. Always build to a separate directory (§5).
5. **Tests pin a lot of DOM.** They depend on class names, ARIA roles and names, exact strings, native `<select>` elements, and `window.confirm` dialogs. Section 4 lists them all.

---

## 1. Frontend component map

### Files

| File | Lines | Role |
|---|---|---|
| `frontend/src/main.jsx` | 434 | Whole app: `App` state machine plus every view component. Several components are written as single lines of more than 2,000 characters (lines 363, 371, 391, 421, 427). |
| `frontend/src/Filing.jsx` | 122 | Filing pane: search, page jump, quote highlights, text selection that fills a quote |
| `frontend/src/SplitPane.jsx` | 102 | Resizable two-pane grid (pointer, keyboard, double-click reset, localStorage `cockpit.layout.*`) |
| `frontend/src/TabScroller.jsx` | 54 | Horizontally scrolling tab strip with ← → overflow buttons |
| `frontend/src/api.js` | 68 | `json()` fetch wrapper, `saveDeal`, row helpers, `filingRanges`, `segments` (highlight splitting) |
| `frontend/src/api.test.js` | 26 | 3 vitest tests for `segments` and `filingRanges` |
| `frontend/src/style.css` | 94 | All styling. Rules are minified onto single lines, so each line holds dozens of rules. |
| `frontend/src/fonts/cabinet-{400,500,700}.woff2` | — | Self-hosted "Cabinet" |
| `frontend/index.html` | 13 | `<title>Ledger cockpit</title>`, `color-scheme: light`. No favicon, no description. |
| `app.js`, `style.css`, `index.html` (cockpit root) | — | **Legacy** read-only page. `server.py:145` falls back to it when `dist/index.html` is missing, and serves it under `/static/`. It is not part of the React app. |

### Routes (must be preserved per `_dev/COCKPIT_BUILD.md`)
`/` shows the overview. `/deal/<slug>` shows the deal workspace (`main.jsx:19-22`). The hash `#row-<n>` selects ledger row n on load (`main.jsx:140-143`) and is rewritten on every row selection (`main.jsx:168`). The app uses `history.pushState` with a guard against leaving unsaved edits.

### Tree

```
FluentProvider(webLightTheme)                         main.jsx:434
└─ App                                                main.jsx:43
   ├─ Header  <header.global-header>                  main.jsx:368
   │   button.wordmark (span.brand-mark "L" + "Ledger cockpit") · span.header-context ("Deal ledgers"|"Deal workspace")
   │   div.header-user (user name + span.edit-access "Edit access" | "Read only" | "Loading session")
   ├─ [no slug] main.overview-wrap                    main.jsx:333
   │   ├─ Spinner "Loading deals"  (div.center-state)
   │   ├─ Message(error)
   │   └─ Overview                                    main.jsx:371
   │       div.overview-title (span.eyebrow "Research workspace", h1 "Deal ledgers", p count, span.overview-total giant number)
   │       div.deal-table-wrap > table.deal-table (8 cols; whole <tr> clickable, tabIndex 0, Enter opens)
   │       div.empty "No deal workbooks are available yet."
   └─ [slug] main.deal-shell                          main.jsx:337
       ├─ Spinner "Loading <slug>"
       ├─ Message(error | warning+conflict actions "Download staged edits" / "Discard edits and load latest")
       ├─ div.deal-toolbar                            main.jsx:341-345
       │   div.deal-identity: button.back-link "All deals", h1 deal name, div.deal-subline "<form> · <date> · Working from <base> · Revision N" | "Source version"
       │   div.toolbar-actions: label.version-control "Version" + Fluent Select (native <select>, aria-label "Version")
       │                        a.export-link "Export Excel" (download) · Fluent Button primary "Save changes"/"Saving…"
       │   div.save-line: span.work-state[aria-live] ("N unsaved changes"|"Saved"|"No unsaved edits"|"Read only version")
       │                  span.save-feedback "Revision saved" (GSAP fade) · "Last saved by … · date"
       ├─ div.mobile-switch[role=group aria-label="Visible pane"]: Buttons "Filing" / "Workspace" (≤820px only)
       ├─ SplitPane.workbench (collapsible; hidden handle ≤820px)   main.jsx:347
       │   ├─ div.filing-column > Filing <section.filing-pane aria-label="SEC filing">   Filing.jsx:103
       │   │    div.filing-tools: .filing-caption, .filing-search (Input "Search filing", .search-count "i / n", ↑ ↓ subtle buttons),
       │   │                      form.page-jump (label "Page", Input#filing-page, Button "Go")
       │   │    div.page-error[role=alert] · div.selection-action ("Use selected text for quote")
       │   │    div.pane-state (Spinner "Loading filing" | error text)
       │   │    div.filing-scroll > div.filing-paper > .page-marker(.approximate) + div.filing-block[data-block](.heading|.table-row|.background-start)
       │   │         mark.quote-mark(.selected)[data-row-index] · mark.search-mark[data-search-index]
       │   ├─ div.split-handle[role=separator]
       │   └─ section.workspace-column[aria-label="Deal workspace"]
       │        TabScroller div.tab-strip(.has-overflow) > button.tab-scroll-control ×2 + nav.tabs[role=tablist]
       │            7 × button[role=tab][aria-selected] (+ <small> counts for Ledger/Rounds/Questions/Review)
       │        div.workspace-scroll(.editor-scroll)[role=tabpanel]
       │          ├─ LedgerTab  SplitPane.ledger-layout (mobileStack)          main.jsx:377-392
       │          │    div.record-list: .section-head (h2 "Events", count, Button "Add"), div.event-list > EventSummary×n
       │          │         button.event-item(.selected)#row-N: .event-line(.event-number, .event-date, .event-review), strong, .event-detail, .quote-location(.missing)
       │          │    div.record-editor: .editor-head (eyebrow "Selected event", h2 "#N Event", p, .editor-nav ↑↓ icon buttons)
       │          │         .record-actions (Move up / Move down / Clone to split / Delete)
       │          │         .source-summary ("Source evidence", status text, "Show in filing")
       │          │         Issues (.issues > .issue.error|.warning|.info)
       │          │         RecordForm .field-grid (Fluent Field+Input|Select|Textarea per column; .span-all, .evidence-field)
       │          │         QuestionLinks .reference-links ("Linked questions", Buttons aria-label "Open question Qn")
       │          │         .review-box (h3 "Row review", Select "Status", Textarea "Review note")
       │          ├─ SheetTab  div.other-sheet > .section-head (h2 sheet, count, "Add row") + SplitPane.sheet-body   main.jsx:408-421
       │          │    div.sheet-list > button.sheet-item(.selected) (strong + span)
       │          │    div.sheet-editor: .editor-head h3, .record-actions, Issues, RecordForm, ReferenceLinks ("Referenced events")
       │          ├─ ReviewTab div.review-tab                                    main.jsx:427
       │          │    .section-head h2 "Review findings" · p.section-intro · MechanicalPanel <details.mechanical-panel> (main.jsx:425)
       │          │    .documents (Buttons → document modal) · article.finding × n:
       │          │       button.finding-title[aria-expanded] (strong, small, .finding-state + caret)
       │          │       .finding-body: p, .finding-proposal, .recorded-decision, Message(warning), .finding-evidence blockquote+cite+"Find quote in filing",
       │          │                      .source-rows, .decision-grid (Selects "Finding judgment"/"Correction implementation"/"Verification"), Textarea "Decision note", .audit-line
       │          ├─ ChangesTab div.changes-tab (h2 "Changes from base", Change×n .change/.change-head/.change-label/pre)   main.jsx:429-431
       │          └─ HistoryTab div.history-tab (h2 "Revision history", article.history-item: .history-head, "Restore", p reason, .history-summary, <details> changes)   main.jsx:432
       ├─ div.save-dock (only when dirty & editable): Field "Reason for this revision" (hint "Appears in history") + Button "Save N change(s)"   main.jsx:360
       ├─ Delete modal  .modal-backdrop > .modal[role=dialog aria-label="Delete record"]  main.jsx:363
       └─ Document modal .modal.document-modal[role=dialog aria-label="Recorded document"] (pre text)  main.jsx:364
```

### Interactive states (where they live)

| State | Implementation | Screenshot |
|---|---|---|
| Overview loading | Fluent `Spinner` "Loading deals" centred (`main.jsx:333`) | d01 |
| Deal loading | Spinner "Loading <slug>" (`main.jsx:338`); `setDeal(null)` clears the whole workspace on every version switch (`main.jsx:131`) | — |
| Filing loading / error | `Filing.jsx:111-112`, plain Spinner, then red text | d04, d33 |
| Tab loading (Changes/History) | Spinner (`main.jsx:429, 432`) | — |
| Empty | `div.empty` grey centred sentence (`main.jsx:371, 391, 421, 427, 429, 432`) | d20, d21 |
| Error | `Message` banner with a Phosphor warning icon (`main.jsx:369`). It shows raw server strings ("unknown deal", "internal error (RuntimeError)…"). | d31, d32, d34 |
| Unknown deal | Banner only, with no back link and no toolbar | d32 |
| Page jump error | `.page-error` strip (`Filing.jsx:109`) | d09 |
| Selection | `.event-item.selected` / `.sheet-item.selected` (blue left rule plus a pale blue background); the filing mark changes from `mark.quote-mark` (#fce880) to `.selected` (#e4af32) | d05, r04 |
| Hover | background tint only, with no transition | d03, d06 |
| Focus | Fluent's controls use their own underline. Explicit `:focus-visible` rules exist only for `.split-handle` and `.tab-scroll-control` (`style.css:28, 64`). `tbody tr:focus{outline:none}` removes the overview's focus ring (`style.css:6`). | d11, d12 |
| Editing / dirty | Local `ops[]` array. The toolbar shows "N unsaved changes" in amber. The fixed `.save-dock` appears bottom-right. There is **no per-field changed marker**. The count is operations, not fields: editing two fields of one row shows "1 unsaved change". | d22, n11 |
| New row | Event labelled "New" until saved | d24 |
| Saving | `saveState='saving'`: all inputs disabled, Version select disabled, button "Saving…" | — |
| Saved | "Saved" plus GSAP-faded "Revision saved" and "Last saved by …" | d25 |
| Conflict (409) | warning banner plus two buttons; draft kept | d30 |
| Read-only (immutable version or no edit rights) | Inputs disabled but restyled to look readable (`style.css:19-22`, `!important`); Save disabled; "Read only version" | d29, r03 |
| Version picker | Native `<select>` (Fluent `Select`); options `label · instruction_version`. The live catalog has exactly 2 per deal: `working` and `opus55-medium`. | d28, d29 |
| Unsaved-navigation guard | `window.confirm` (`main.jsx:41`), `beforeunload`, popstate guard (`main.jsx:83-92`) | — |
| Restore | `window.confirm` (`main.jsx:301`), then POST restore | d27 |
| Findings | Accordion, one open at a time (`findingOpen`); decisions staged as ops | d16-d18, r08-r09 |
| Modals | Custom. Focus goes to the first button, Tab is trapped, Escape closes and focus returns (`main.jsx:107-121`). Clicking the backdrop does nothing. | d19, d23, n12 |
| Keyboard | Global `j`/`k`/`ArrowDown`/`ArrowUp` step ledger rows whenever focus is not in a form control or separator (`main.jsx:93-101`). This also hijacks page arrow-scrolling and fires while a modal is open. Nothing in the UI tells users about it. | — |
| Split panes | Drag, arrow keys (Shift ×4), Home/End, double-click reset; size saved in localStorage per `desktop`/`mobile` key (`SplitPane.jsx`) | d12 |
| Resizable textareas | `resize: both` on the Fluent wrapper (`style.css:39-40`) | — |

### Responsive behaviour

| Width | Behaviour |
|---|---|
| > 1200 | Filing and workspace side by side (filing default 47%, min 280; workspace min 400). The inner list+editor stays in columns until the workspace is ≤ 680 px wide (`SplitPane.jsx:5, 31`). **At 1440 with default split, the workspace is about 760 px, so columns hold. At 1280 and 1024 the inner layout already flips to the horizontal "card strip".** |
| 821–1200 | Filing tools stack (`style.css:18`) |
| ≤ 1150 | Tighter paddings (`style.css:11`) |
| ≤ 820 | Only one pane shows. `.mobile-switch` toggles Filing and Workspace; the main splitter is hidden (`style.css:12, 46`). The inner layout returns to columns at 768 because the workspace is full width again. |
| ≤ 560 | Inner list becomes a horizontal strip of 150 px cards above the editor with a row-resize handle (`style.css:13, 17, 47-56`). Header context hidden. |
| max-height ≤ 680 | Tighter toolbar (`style.css:94`) |
| container ≤ 440 / 520 | Field grid → 1 column; filing tools and decision grid stack (`style.css:44-45`) |

At 400 px, the header, toolbar, pane switch, tab strip and event strip take about 510 of 860 px before the editor starts (n02). The tab strip shows the arrow buttons *and* a native scrollbar at the same time.

---

## 2. CSS inventory (`frontend/src/style.css`)

**Architecture.** One global stylesheet imported by `main.jsx:10`. The file has no layers, tokens, modules or naming scheme beyond ad-hoc BEM-ish class names. Rules are minified onto lines 4-22. A later "append" section (lines 24-94) re-declares earlier rules, and the media queries appear out of order (lines 11-13, 17-18, 46-56, 94). Some rules are duplicated: the `.split-horizontal …` rules at lines 47-56 and 76-92, and `.record-list`/`.sheet-list` at lines 17 and 52. `.deal-shell{min-height:600px}` (line 7) is overridden by `min-height:0` (line 59). Fluent classes (`.fui-*`) are styled from outside with 18 `!important`s.

**Custom properties.** Only `--split-size` (set inline by `SplitPane.jsx:97`). There are no colour, spacing or type tokens.

**Fonts.**
- `@font-face` Cabinet 400/500/700 (`style.css:1-3`), `font-display: swap`. As noted in §0, Fluent overrides it almost everywhere.
- Effective UI font: `"Segoe UI", "Segoe UI Web (West European)", -apple-system, BlinkMacSystemFont, Roboto, "Helvetica Neue", sans-serif` (Fluent `webLightTheme`).
- Filing: `Georgia, serif` 13px / 1.72 (`style.css:8 .filing-paper`).
- Document modal `pre`: Cabinet (`style.css:10`).
- No monospace font anywhere and **no `font-variant-numeric: tabular-nums`**, even for prices, counts, dates, event numbers and revision numbers.

**Type scale (font-size × number of declarations).**
9px×3 · 10px×7 · 11px×28 · 12px×18 · 13px×14 · 14px×1 · 15px×3 · 16px×2 · 17px×1 · 18px×2 · 19px×2 · 20px×1 · 22px×1 · 24px×1 · 25px×1 · 32px×1 · 40px×1 · 55px×1 · 72px×1. Fluent adds 14px/20px for all inputs and buttons.
- Headings: h1 25px (global), deal h1 24px/20px narrow, overview h1 40px/32px, overview ghost number 72px/55px, h2 19px, `.section-head h2` 18px, `.editor-head h2` 22px with **line-height 20px** from Fluent (tighter than the font size), h3 16px/19px.
- 38 declarations at 9-11px, used for list metadata, hints, badges, issues and audit lines.
- Weights: 700 ×13 plus `bold` ×1, 400 and 500 once each in `@font-face` only. In effect the app uses 400 and 700, plus Fluent's 600 on buttons.
- Letter-spacing: `-.025em` (h1-h3), `.04em` (table th), `.05em`, `.08em` (page marker), `.1em` (eyebrow).
- Line-heights: 1, 1.1, 1.2, 1.25×2, 1.3, 1.35, 1.45×2, 1.5×2, 1.72, .85.
- `text-transform`: uppercase on `.eyebrow`, `.deal-table th`, `.page-marker`, `.change-label`. **capitalize** on `.status-text`, `.finding-state` and `.change-head span`. The capitalize rule changes research strings on screen: "unreviewed; Austin review pending" displays as "Unreviewed; Austin Review Pending" (r01).

**Colour.** 157 unique hex values. Grouped:
- *Text/ink (blue-grey family):* #202a35 (root), #263746, #263543, #26313c, #2c3d51, #182c45, #183d72, #213d62, #405164, #415973, #425267, #45556a, #4a657d, #50677f, #536275, #566476, #586979, #5a6877, #5d6b7d, #5f6f7e, #5f7082, #607b99, #637184, #64748a, #65778a, #66788b, #66798b, #667c90, #687888, #688096, #697788, #697889, #6f7c8a, #708091, #708092, #738194, #748597, #768596, #788594, #788694, #788796, #7b8794, #7b8997, #7e8b99, #83909e, #8a97a4, and Fluent's neutral #242424 on headings and selects. **More than 45 near-identical greys**, and cool blue-grey text sits next to Fluent's neutral grey.
- *Accent blues (the one accent, spread over many values):* #1555a4, #174f92, #1d55a6, #21558b, #2262b2, #235a9e, #245a9d, #245ea7, #265b99, #2869b4, #386a9d, #426ca4, #466b95, #4a6b91, and Fluent brand #0f6cbd on the primary buttons. That makes about 15 blues, where one would do.
- *Surfaces:* #fff, #f3f5f7 (app ground), #f8fafc, #f7f9fc, #f6f9fc, #f6f9fd, #f4f7fb, #f3f7fb, #f2f6fb, #f1f5fa, #f1f6fb, #eff5fb, #eff5fd, #edf4fd, #edf4ff, #eaf3fe, #eaf2ff, #edf2f6, #edf0f3, #e9edf1 (filing well), #e8edf3.
- *Borders:* #d9e0e6, #dbe2e9, #dde3e8, #dde6ef, #d6dde5, #d9e1e8, #d9e3ed, #dce3e9, #dce5ed, #d1dce6, #d8e0e8, #e1e6eb, #e1e8ef, #e2e7ed, #e3e9ef, #e3eaf0, #e6edf3, #e7edf2, #e9eef2, #c8d4e2, #c9d9ef, #cfdae5, #cddff4, #dfe7ef.
- *Scrollbars/handles:* #52779c thumb on #dfe7ef track (11-12px, `style.css:61-74`), #7994b2, #8295aa, #aab9c8, #6b92b8.
- *Quote yellow:* #fce880 (mark), #e4af32 (selected), #ffe7aa (search), #fff8db / #ead9a0 (selection bar), #fffbee / #ebdfa2 / #745a20 / #59430e (source summary), #fffdf1 (evidence textarea), #fff9e7 / #e4c766 / #806b35 (finding evidence).
- *Warning amber:* #fff8e8, #ead69c, #7b5a17, #fff7e8, #d3a03f, #fff7e7, #d7a544, #fff4e2, #ead5aa, #8b5b15, #9e661a, #a06a26, #79611f, #887046.
- *Error red:* #fff1ef, #e2bdb8, #8c342e, #c96054, #a63a34, #a13d34.
- *Success green:* #256342, #486f55.
- *Overlays:* #14233788 (modal backdrop), #182c4610, #1f3d5d30, #071e3c45 (shadows).

**Radii.** 2px (handle grip), 3px ×2 (badges), 4px ×6, 5px ×4 (brand mark, history, scrollbar thumbs), 6px (save dock), 7px ×2 (deal table, modal), plus Fluent's 4px on controls.

**Shadows.** `0 4px 20px #182c4610` (filing paper), `0 8px 30px #1f3d5d30` (save dock), `0 20px 70px #071e3c45` (modal), `0 0 0 2px #e4af32` (selected mark), and box-shadow tricks for the splitter grip dots.

**z-index.** 1 (tab scroll focus), 2 (split handle), 10 (save dock), 50 (modal). Fluent portals are not used, because the selects are native.

**Spacing.** No scale. Paddings include 4/5/6/7/8/9/10/11/12/13/14/15/16/17/18/19/20/21/23/24/25/27/28/30/32/36/42/48/60/80/85/90 px. Gaps range 1-27 px.

**Motion.** No CSS transitions anywhere. GSAP is used for one 0.28 s fade of "Revision saved" (`main.jsx:102-106`). There are smooth `scrollIntoView` calls. A reduced-motion guard exists (`style.css:14`).

**Scrollbars.** Heavy custom 11-12px blue-grey scrollbars on the tabs, editor and workspace (`style.css:61-74`). With the 8 px grip-dot splitters, the ledger view at 1440 shows **four scrollbars and two grips in one row** (r03).

---

## 3. Build

- `frontend/package.json`: React 19.1.1, `@fluentui/react-components` 9.72.3, `@phosphor-icons/react` 2.1.10, `gsap` 3.13.0; dev: Vite 6.3.6, `@vitejs/plugin-react` 4.7.0, vitest 3.2.4. Scripts: `dev` (vite on 127.0.0.1), `build`, `test` (vitest run).
- `frontend/vite.config.js`: `build: { outDir: '../dist', emptyOutDir: true }`; dev proxy `/api` → `http://127.0.0.1:8765` (a fixed port that nothing currently runs on).
- `frontend/node_modules/` **exists** (ignored by `.gitignore:13`). Node v22.22.2. The build takes about 8 s and produces `index-*.js` 466 KB (142 KB gzip), `index-*.css` 27 KB, and three woff2 files.
- `dist/` **is committed** and served live by `ledger-cockpit.service` (port 8778, `lines.dealextract.org`). The current `dist/` matches the source: a rebuild reproduced identical hashes.
- The server serves only `HERE/dist/index.html` and `HERE/dist/assets/*` (`server.py:131-146`). A different build directory can be served only through a shim (see `serve_preview.py`) or Playwright route interception (the tests' `COCKPIT_TEST_DIST`).
- Playwright comes from `/home/uctpiaj/work/vm-browser/node_modules/playwright/index.mjs` and uses Chrome at `/opt/google/chrome/chrome`.

---

## 4. Test constraints the redesign must keep passing

Baseline on the current build (22 Sep, all run against temp fixtures, repo tree unchanged afterwards):

| Suite | Result |
|---|---|
| `acceptance/test_browser.mjs` | **46/46 assertions passed** |
| `acceptance/test_resize.mjs` | passed |
| `acceptance/test_responsive.mjs` | passed |
| `acceptance/test_http.py` | 11 passed (backend only) |
| `frontend` vitest (`api.test.js`) | 3 passed |

Fixture (`acceptance/test_http.py:34 synthetic_repo`): one deal, slug `synthetic`, named "Synthetic Acme". It has 3 ledger rows ("Invitation", "Offer", "Signing"), Q1 "When did Party A bid?" with Rows affected "#2-#3", one round ("Invitation #1"), facts "Target = Synthetic Acme", finding F1 "Uncertain date", and document "Synthetic finding". The version ids are `working` and `v1132-raw`. The session user is `local` with edit access. The fixture's check report includes the code `presentation.wrap_text`.

### 4.1 Roles, accessible names and text (Playwright `getByRole` / `getByText`)
Playwright name matching is **substring and case-insensitive unless `exact: true`**, and locators are **strict** (two matches fail).

- heading **"Deal ledgers"** on `/`
- overview rows: `getByRole('row').filter({hasText:'Synthetic Acme'})`, count 1, and **clicking the row opens the deal**. `capture_catalog.mjs` also needs `.deal-table tbody tr` (count 9 on the real catalog).
- heading **"Synthetic Acme"** (the deal h1)
- textbox **"Search filing"** (also `input[aria-label="Search filing"]`); text **"1 / 1"** exact (the search counter format `${i} / ${n}`)
- textbox **"Page"** exact; button **"Go"** exact
- button **"Show in filing"**
- button **"Open question Q1"** (an aria-label on the linked-question button)
- tabs: `getByRole('tab', {name: /^Ledger(\b|$)/})`, and the same pattern for **Rounds, Questions, Deal facts, Review, Changes, History**. Count badges may follow the label, but the label must come first. Tabs expose `aria-selected="true"`. `getByRole('tabpanel')` must be visible.
- textboxes by label: **"Note"** (exact, inside `.record-editor`), **"Event"**, **"When"** (exact), **"How opened"**, **"Recommended answer"**, **"Value"**, **"Decision note"**, **"Reason for this revision"**
- **native `<select>`** comboboxes (Playwright `selectOption`): **"Version"** (option values are version ids: `working`, `v1132-raw`; `{index:1}` must be an immutable version) and **"Finding judgment"** (value `supported`). Replacing these with a custom listbox breaks `selectOption`.
- buttons: **"Save changes"** (unique; disabled when read-only or pending), **"All deals"**, **"Clone to split"**, **"Move up"**, **"Delete"** (exact, unique on the page), **"Stage deletion"**, **"Restore"** (inside `.history-item`), **"Download staged edits"**, **"Discard edits and load latest"**, **"Find quote in filing"**, **"Add"** (inside `.record-list .section-head`), a button matching **/Uncertain date/** (the finding title), a button matching **/#2 Offer/** inside `.reference-links`, **"Scroll workspace tabs left"** and **"Scroll workspace tabs right"** (enabled or disabled according to overflow position)
- The save dock button must **not** contain the substring "Save changes". It is currently "Save N change(s)".
- link **"Export Excel"** that triggers a download (`.xlsx`)
- dialog **"Delete record"**. Focus must move inside it on open; Escape closes it and returns focus to the "Delete" button.
- group **"Visible pane"** with buttons **"Filing"** and **"Workspace"** (at 390 px); region **"SEC filing"**
- texts: **"Revision saved"** (exact; shows after each save), **"Read only version"**, **"No unsaved edits"** (exactly one match), **"Source version"** (capture_catalog), **"Browser edited all four sheets"** and **/local/** in History, "Synthetic Acme UI" inside the tabpanel (Changes), **"Review findings"** heading (capture_catalog)
- `.deal-subline` must contain **"Revision N"**, and on the real catalog **"Opus 5.5 medium extraction"**.
- **`window.confirm` dialogs** are relied on: unsaved navigation via "All deals" is dismissed and must keep `/deal/synthetic`; Restore is accepted; "Discard edits and load latest" is accepted. An in-page confirm would break three checks unless the tests change.
- URL: clicking `mark.quote-mark` must set hash `#row-1`; choosing a referenced event sets `#row-2`.
- While a save is pending, the Note textbox and the Version select must be disabled.

### 4.2 Class selectors and DOM structure
`test_browser`: `.filing-block`, `mark.search-mark`, `.filing-scroll` (scroll container; `scrollTop > 0` after page jump), `mark.quote-mark`, `mark.quote-mark.selected`, `.event-item` (with the event title in its text), `.sheet-editor h3` (innerText exactly `Q1`), `.reference-links`, `.record-editor`, `.mechanical-panel summary` (clickable `<details>`), `.mechanical-content`, `.history-item`, `.filing-pane`, `.deal-subline`.

`test_resize`:
- `.event-item.selected`, `mark.selected` (must be inside `.filing-scroll`'s visible box on load and reload)
- `.workbench > .split-handle`, `.ledger-layout > .split-handle`, `.sheet-body > .split-handle`: direct children, draggable, focusable, with ArrowRight/Home/End/dblclick behaviour
- `.filing-column`, `.record-list`, `.sheet-list`, `.workspace-column` (widths); `.ledger-layout` toggles classes **`split-horizontal` / `split-vertical`**
- `.other-sheet > .section-head h2` with exact text Rounds / Questions / Deal facts; `.sheet-body` custom property `--split-size` must equal the list width within 2 px
- `.record-editor .resizable-textarea` (first; wraps a `textarea`; corner-drag changes width and height, height > 260 allowed), `.finding-title`, `.finding-body .resizable-textarea`, `.review-box .resizable-textarea`
- At 850 px, `.workspace-column` must be ≥ 398 px wide; at 390 px, `.ledger-layout > .split-handle` must be visible and `split-horizontal` set
- localStorage persistence of pane sizes across reload; resizing must not create a draft (the text "No unsaved edits" stays)

`test_responsive`:
- For widths **1440, 1280, 1024, 850, 768, 560, 390**: no document horizontal overflow; `.record-editor` width ≥ 350.
- `.ledger-layout` must be **columns at 1440 and 768 and `split-horizontal` at 1280, 1024, 850, 560 and 390**, with `--split-size` equal to the list width (columns) or height (compact) within 2 px. This pins the current 680 px `STACK_WIDTH` behaviour and the default 47 % filing split.
- In compact mode, `.event-item.selected .quote-location` must end 8 px or more above the bottom of `.event-list`.
- `.tabs` (nav) with `[aria-selected="true"]` kept visible after resize.
- Widening a `.record-editor .resizable-textarea` must create horizontal overflow **on `.record-editor`**, which is scrollable with a native horizontal scrollbar at its bottom edge.
- At 1024×600, the document height must be ≤ 600 (no body scroll), and `.save-dock` must be fully on screen when dirty.
- Drafts must survive viewport reflow.

`test_http.py` checks the backend only, plus `/assets/%2e%2e/...` → 404. `capture_catalog.mjs` writes into `_dev/reviews/...` and asserts details of the real catalog. **Do not run it casually.**

### 4.3 Build-contract constraints (`_dev/COCKPIT_BUILD.md`, "Design")
The contract asks for "calm document-focused styling"; dials variance 4, motion 3, density 8; **preserve blue control accents and yellow quotation highlights on a single light theme**; Cabinet Grotesk self-hosted; **official Fluent UI React controls and one Phosphor icon family**; GSAP only for restrained feedback with reduced-motion handling; inputs with visible labels, error/saved/unsaved states, keyboard access and strong contrast; on narrow screens a Filing/Workspace switch; never truncate or rewrite research text. Austin's "looks too AI" verdict may justify revisiting some of these (e.g. Fluent's look). Confirm with him before dropping Fluent or the blue/yellow rule.

---

## 5. How to build and preview (without touching the live site)

```bash
REPO=/home/uctpiaj/work/Projects/sec-extraction
S=/home/uctpiaj/work/tmp/claude-1001/-home-uctpiaj-work-Projects-sec-extraction/f40a7cfe-b924-48c0-a4af-8188cd3279d3/scratchpad/redesign

# Build to a separate directory. Never `npm run build`: it empties the live dist/.
cd $REPO/_dev/tools/cockpit/frontend && npx vite build --outDir $S/preview-dist --emptyOutDir

# Serve that build against the disposable synthetic fixture (editable; temp state discarded on exit)
cd $REPO && python3 $S/serve_preview.py --dist $S/preview-dist --port 8791
#   → http://127.0.0.1:8791/  and  http://127.0.0.1:8791/deal/synthetic

# Optional: the same build against the REAL nine-deal catalog, forced read-only (COCKPIT_REQUIRE_ACCESS=1 → can_edit false; no state DB exists, GETs open none)
cd $REPO && python3 $S/serve_preview.py --dist $S/preview-dist --port 8792 --actual-catalog-readonly

# Acceptance against the staged build (evidence redirected out of the repo)
cd $REPO
COCKPIT_TEST_DIST=$S/preview-dist COCKPIT_BROWSER_EVIDENCE=$S/baseline/browser     node _dev/tools/cockpit/acceptance/test_browser.mjs
COCKPIT_TEST_DIST=$S/preview-dist COCKPIT_RESIZE_EVIDENCE=$S/baseline/resize       node _dev/tools/cockpit/acceptance/test_resize.mjs
COCKPIT_TEST_DIST=$S/preview-dist COCKPIT_RESPONSIVE_EVIDENCE=$S/baseline/responsive node _dev/tools/cockpit/acceptance/test_responsive.mjs
python3 -m pytest -q -p no:cacheprovider _dev/tools/cockpit/acceptance/test_http.py
(cd _dev/tools/cockpit/frontend && npx vitest run)

# Re-capture screenshots (both preview servers running)
node $S/capture_before.mjs     # writes $S/before/*.png — copy and change OUT for an "after" set
```

Notes:
- `test_browser.mjs` defaults its evidence folder to `_dev/reviews/2026-09-21-v1132-cockpit/cockpit-verification` inside the repo. Always set `COCKPIT_BROWSER_EVIDENCE`.
- `COCKPIT_TEST_DIST` makes the tests serve assets from the staged directory through Playwright routing. Without it they use the live `dist/`.
- For hot reload, `npm run dev` proxies `/api` to port 8765. Run `serve_preview.py --port 8765 --dist $S/preview-dist` and open the Vite URL.
- Deploying means replacing `dist/`. The service reads files per request, so no restart is needed. Only do this when Austin authorises it.

---

## 6. Screenshot index (`before/`)

Desktop 1440×900 against the synthetic fixture (d*), 1024 and 850 (m*), 400×860 narrow (n*), and the real catalog read-only (r*).

| File | What it shows |
|---|---|
| `d01-overview-loading.png` | Overview while `/api/deals` is pending (Fluent Spinner) |
| `d02-overview-fixture.png` | Overview / landing page, synthetic fixture (1 deal) |
| `d03-overview-row-hover.png` | Overview table row hover |
| `d04-deal-filing-loading.png` | Deal open, filing pane still loading |
| `d05-deal-ledger-default.png` | Deal workspace default: filing left, Ledger tab (event list + editor) right |
| `d06-ledger-event-hover.png` | Hover on an event list item |
| `d07-ledger-editor-scrolled.png` | Editor scrolled to bottom: linked questions + Row review box |
| `d08-filing-search.png` | Filing search with counter and highlights |
| `d09-filing-page-error.png` | Page-jump error strip |
| `d10-filing-selection-quote-bar.png` | Selected filing text, yellow "Use selected text for quote" bar; issue list pushing the form down |
| `d11-field-focus.png` | Keyboard focus on an editor field (Fluent underline) |
| `d12-splitter-focus.png` | Focused filing/workspace splitter |
| `d13-rounds.png` / `d14-questions.png` / `d15-deal-facts.png` | Other sheets: list + editor |
| `d16-review-collapsed.png` | Review tab: intro, mechanical `<details>`, documents, collapsed finding |
| `d17-review-mechanical-open.png` | Mechanical check expanded |
| `d18-review-finding-open.png` | Finding expanded: proposal, recheck warning, evidence, decision selects |
| `d19-document-modal.png` | Recorded-document modal |
| `d20-changes-empty.png` | Changes empty state |
| `d21-history-base.png` | History with revision 0 only |
| `d22-editing-dirty-save-dock.png` | Dirty: amber "1 unsaved change" (2 fields edited), save dock **covering form fields** |
| `d23-delete-modal-references.png` | Delete modal with replacement-event select |
| `d24-new-row-staged.png` | Clone to split: staged "New" event |
| `d25-saved.png` | After save: "Saved · Revision saved · Last saved by local" |
| `d26-changes-list.png` | Changes with before/after (insert rendered as raw JSON) |
| `d27-history-revisions.png` | History revision with changes expanded (link-blue body text) |
| `d28-version-select-focused.png` | Version picker (native select; the open list is OS-drawn and not capturable). Options: "Working copy · v1.13.2", "Synthetic raw · v1.13.2" |
| `d29-readonly-version.png` | Immutable version: read-only fields, Save disabled |
| `d30-conflict-warning.png` | 409 conflict banner with Download / Discard |
| `d31-save-error.png` | Save failure banner (raw server string) |
| `d32-unknown-deal-error.png` | Unknown slug: lone "unknown deal" banner, blank page, no back link |
| `d33-filing-error.png` | Filing failure: red text in filing pane |
| `d34-overview-error.png` | Overview API failure |
| `m-1024-ledger.png` | 1024 laptop: inner list already a horizontal card strip |
| `m-850-ledger.png` | 850: same strip, filing narrow |
| `n01-overview.png` | 400: overview table scrolls sideways |
| `n02-ledger-workspace.png` | 400: chrome takes about 510 px before the editor; tab arrows plus scrollbar; event strip |
| `n03-ledger-editor-scrolled.png` | 400: editor scrolled |
| `n04-filing.png` | 400: filing pane |
| `n05-rounds.png` … `n07-deal-facts.png` | 400: other sheets |
| `n08-review.png` / `n09-review-finding-open.png` | 400: review |
| `n10-history-tabs-overflow.png` | 400: History tab with tab overflow |
| `n11-editing-dirty.png` | 400: dirty, full-width save dock |
| `n12-delete-modal.png` | 400: delete modal |
| `r01-overview-real.png` / `r02-overview-real-full.png` | Real 9-deal overview (read-only), including the capitalize mangling of the review state |
| `r03-datalink-ledger.png` | Datalink (71 events): most of the filing is highlighted yellow |
| `r04-datalink-event-21.png` | Event #21 selected, filing scrolled to its quote |
| `r05`–`r07` | Datalink Rounds / Questions / Deal facts: long text trapped in small scrolling textareas |
| `r08-datalink-review.png` / `r09-datalink-finding-open.png` | Datalink review / finding |
| `r10-datalink-mechanical.png` | Datalink mechanical check expanded |
| `r11-datalink-history.png` | Datalink history (revision 0) |
| `r12-datalink-narrow.png` / `r13-datalink-narrow-filing.png` | Datalink at 400 px |

---

## 7. Diagnosis against the redesign checklist

Context: a dense, light-theme research tool used for hours, where the filing text and cell values are the content. The marketing items in the checklist (hero, photos, grain, testimonials, legal links) do not apply. The notes below adapt the checklist to this kind of tool.

### 7.1 Typography
1. **The declared font never applies.** Fluent's `webLightTheme` wins (`main.jsx:434`, `style.css:4`). The UI is Segoe/SF/Roboto, the same "system default" look as every Fluent or Microsoft sample. The rule `.fui-Input, .fui-Textarea, .fui-Select{font-family:Cabinet…}` (`style.css:4`) targets the wrappers, but the inner `<input>` and `<select>` keep Fluent's atomic class. The fix is to set the theme tokens (`fontFamilyBase`) through `createLightTheme`/a custom theme, not CSS overrides.
2. **The scale is chaotic.** There are 19 sizes, with 38 declarations at 9-11 px (`style.css:6-10, 13, 17, 91`). For hours of reading, 9-10 px metadata (`.tabs small`, `.event-review`, `.quote-location`, `.field-grid .fui-Field__hint`, `.change-label`, narrow `.event-number`/`.event-detail` at 9 px, `style.css:13`) is too small. Four or five steps would be enough.
3. **Numbers are proportional.** No `tabular-nums` is set on prices, counts, dates, the `#` column, revision numbers or the overview's Events/Rounds/Questions columns (`style.css:6 .deal-table .number`). A ledger tool needs aligned figures, and probably a mono or tabular face for IDs, dates and prices.
4. **Only two weights** (700 and 400) carry all the hierarchy; every label, tab, badge, number and heading is 700 (`style.css`, 13 declarations). The result is flat and shouty.
5. **All-caps tracked labels everywhere:** `.eyebrow` "RESEARCH WORKSPACE" and "SELECTED EVENT" (`main.jsx:371, 391`; `style.css:6`), `.deal-table th` (`style.css:6`), `.page-marker` "PAGE 2 (APPROXIMATE)" (`style.css:8`) and `.change-label` BEFORE/AFTER (`style.css:10`). This is a classic AI-template pattern.
6. **`text-transform: capitalize` rewrites research text:** `.status-text` (`style.css:6`), `.finding-state` and `.change-head span` (`style.css:10`). "unreviewed; Austin review pending" is shown as "Unreviewed; Austin Review Pending". This conflicts with the contract's "do not change research text".
7. **The filing's reading measure is too long and the type too small:** Georgia 13 px inside a 770 px paper gives about 95-100 characters per line (`style.css:8 .filing-paper`). This is the text read most in the app.
8. **Heading line-heights clash with Fluent:** `.editor-head h2` is 22 px on a 20 px line-height, and `.section-head h2` is 18/20 (Fluent's inherited `line-height: 20px`).
9. **A giant decorative count.** `.overview-total` is a 72 px, 1.28:1-contrast ghost "9" (`main.jsx:371`, `style.css:6`). It is a pure AI-dashboard flourish.

### 7.2 Colour and surfaces
1. **No palette.** 157 hex values, about 45 greys and about 15 accent blues, all hand-picked per rule (§2). Adjacent elements use almost-but-not-quite matching colours (`#dbe2e9` vs `#d9e0e6` vs `#dde3e8` borders).
2. **Mixed grey families.** Custom cool blue-greys (#202a35…#8a97a4) sit next to Fluent's neutral #242424 headings, #bdbdbd disabled text and #f0f0f0 disabled fill (d05 toolbar: the Save button is neutral grey beside blue-tinted everything).
3. **Two accent blues on the same toolbar.** Fluent brand #0f6cbd (primary Save, mobile switch) and custom #235a9e/#1555a4 (`.export-link`, links, tabs). The "Export Excel" pseudo-button (`style.css:7`) is hand-styled to imitate a Fluent button and does not match it.
4. **"Callout soup": seven different tinted boxes with a 3 px left rule.** `.issue` (blue, amber or red), `.finding-proposal`, `.finding-evidence blockquote`, `.recorded-decision`, `.reference-warnings`, `.selected` list items and `.filing-block.table-row` (`style.css:8-10, 16`). Add the yellow-bordered `.source-summary` (`style.css:9`), the `.review-box` card, the `.mechanical-panel` card, `.history-item` cards containing `.change` cards (card in card, `style.css:10`), and the filing "paper" card with a shadow inside a grey well (`style.css:8`). Every piece of information sits in a box.
5. **Quote highlighting has lost its signal.** On real deals nearly every paragraph is #fce880, and the selected quote (#e4af32) differs only slightly (r03, r04). No hue or underline distinguishes "selected" from "has a quote", or "located" from "search hit".
6. **Status colour is weak and inconsistent.** Issues use pastel fills with 11 px text. "Source located" is 10 px green. Review state is plain grey capitalised text (`.status-text`). Error count and warning count are plain small text in the overview (`main.jsx:371`).
7. **Generic, untinted shadows:** save dock `0 8px 30px`, modal `0 20px 70px` (`style.css:9-10`). They are acceptable but floaty; the save dock looks like a toast over the form.
8. **Low-contrast text** (WCAG AA needs 4.5:1 for small text): `.tabs small` 2.65:1 (`style.css:9`), `.header-context` 3.66, `.section-head span` 3.61, `.event-date` 3.79, `.empty` 3.58, `.audit-line` 3.26, `.finding-title small` 3.48, `.field-grid .fui-Field__hint` 3.73, `.save-line` 3.76, disabled Fluent button text 1.65, disabled tab arrow 1.97.

### 7.3 Layout
1. **The "sheet" is a form, not a grid.** Ledger rows can only be read one at a time in a two-column, 20-field form (`main.jsx:394-406`); the list shows only title, date and who. Researchers cannot scan a column (for example every "Type" or every "Price low") or compare neighbouring events. The same applies to Rounds, Questions and Facts. Facts in particular, a two-column key/value sheet, should simply be a table.
2. **Fields have no hierarchy.** Every column gets an equal Fluent Field in `.field-grid` (`style.css:9`). The evidence quote, the most important field for review, is one textarea among twenty, halfway down. Long fields use fixed-height textareas that scroll inside a scroll pane inside a split pane (r06: Question and "Why, with page" are cut off with inner scrollbars).
3. **Chrome eats vertical space.** Header 56 px plus a 124 px deal toolbar (`style.css:5, 7`) before any content. The `.save-line` sits on its own row, right-aligned and far from the Save button. At 400 px about 510 px of 860 is chrome (n02).
4. **Scrollbars and handles form a visual fence.** Four heavy scrollbars and two 8 px grip-dot splitters stand in one horizontal band (r03; `style.css:25-29, 61-74`).
5. **The compact card strip appears too early.** At 1280 and 1024 (common laptop widths) the event list turns into 150 px horizontal cards (m-1024; `SplitPane.jsx:5 STACK_WIDTH=680`). Scrolling 71 events sideways is poor. The tests currently pin this (§4.2).
6. **Issues come before content.** Up to five pastel red boxes of checker codes (`controlled.type`, `bid.fields_on_nonbid`) push the form below the fold (d10, m-850; `main.jsx:373`, `style.css:9`). They are shown as plain text, not tied to the field they concern.
7. **The save dock overlaps the form** (d22). It is `position: fixed` over the editor (`style.css:9 .save-dock`) and duplicates the toolbar's Save button.
8. **The overview is card-in-page.** The table sits in a bordered, rounded wrapper under a centred-feeling hero (eyebrow, 40 px h1, ghost number) (`main.jsx:371`). Every row repeats "Location aid, not validation", and rows are about 100 px tall for 3 lines of metadata (r01).
9. **Review, Changes and History are narrow centred columns** (max-width 950, `style.css:10`) inside a pane that is already narrow. The mix of centred and edge-to-edge panes looks inconsistent.

### 7.4 Interactivity and states
1. **Focus visibility is incomplete.** No `:focus-visible` style is set for `.event-item`, `.sheet-item`, `.tabs button`, `.finding-title`, `.back-link`, `.wordmark`, `.modal-head button` or `.deal-table tr`; the last has its outline actively removed (`style.css:6`). The UA default ring is inconsistent across browsers.
2. **The tabs are not full ARIA tabs.** They have no `id`/`aria-controls`, the tabpanel has no `aria-labelledby`, and there is no arrow-key roving: all seven tabs are tab stops (`main.jsx:350-351`, `TabScroller.jsx:51`). The tablist is a `<nav>`, a landmark role overridden by `role=tablist`.
3. **The overview row is not a link** (`main.jsx:371`). It uses `onClick` plus `tabIndex` plus Enter only (no Space), so it cannot open in a new tab, be middle-clicked or be copied as a link.
4. **The pane switch has no pressed state.** "Filing"/"Workspace" toggles primary/secondary appearance without `aria-pressed` (`main.jsx:346`).
5. **The global row-stepping keys** (j/k/↑/↓, `main.jsx:93-101`) are undiscoverable, steal ↑/↓ from page scrolling, and still fire while a modal is open.
6. **Loading states are generic spinners** (`main.jsx:333, 338, 364, 429, 432`; `Filing.jsx:111`). A version switch blanks the entire workspace, filing included, then re-renders (`main.jsx:131`).
7. **Error states give raw server strings and dead ends.** "unknown deal" with no link back (d32; `main.jsx:339`); "internal error (RuntimeError); see the server log" (d31); the filing error is bare red text (`Filing.jsx:112`). A session failure prefixes "Session:" into the page-level banner (`main.jsx:82`).
8. **`window.confirm` / native dialogs** for unsaved navigation, restore and discard (`main.jsx:41, 297, 301`). This is inconsistent with the custom modals, but the tests rely on it (§4.1).
9. **Dirty state is not shown per field.** Changed inputs, staged deletions and moved rows carry no marker. The unsaved count counts operations, not fields.
10. **Hover and pressed feedback** is background-only with zero transition. That suits a tool, but there is no pressed state on custom buttons (event items, finding titles).
11. **The version picker** is a native select (required by tests) labelled "Working copy · v1.13.2". Nothing explains that "Working copy" is editable and the other version is immutable until you pick it (the "Read only version" text appears far right).
12. **Empty states** are grey centred sentences (`.empty`, `style.css:9`). That is fine in tone but visually indistinguishable from loading text.
13. **Modal backdrops** do not close on click. The document modal renders a whole report in a `<pre>` set in Cabinet (`style.css:10`).

### 7.5 Components
1. **Generic, untuned Fluent v9 look.** Stock inputs with bottom-accent underlines, stock subtle buttons and stock selects. Combined with the missing font, this reads as "Microsoft sample app".
2. **A monogram brand mark.** The blue rounded square with "L" (`main.jsx:368`, `style.css:5`) is a textbook AI placeholder logo.
3. **Pill/badge counts** in tabs (`.tabs small`, grey chips, `style.css:9`) and a pale-blue "Edit access" chip (`style.css:5`).
4. **Buttons of five kinds** share the toolbar and editor: Fluent primary, Fluent secondary (small), Fluent subtle icon, the custom `.export-link` anchor, and custom text buttons (`.back-link`, `.wordmark`). "Move up / Move down / Clone to split / Delete" is a row of four equal small buttons, with no grouping and no danger styling on Delete (`main.jsx:391`).
5. **Accordion findings** show a caret and capitalised judgment text but no status colour or icon (`main.jsx:427`).
6. **History shows raw data.** `JSON.stringify` output for inserted rows (`main.jsx:430`), and change bodies inherit link-blue colour from `.history-item details{color:#466b95}` (`style.css:10`, d27).
7. **Filing toolbar.** Search, count, ↑↓ and Page/Go are crammed into two grid rows. The disabled "Go" is a grey slab (d05).

### 7.6 Iconography
1. There is one Phosphor family (good), but icon sizes vary: 15, 16, 17, 18, 19 and 20 px (`main.jsx:342-364, 369, 391, 421, 432`; `Filing.jsx:106`; `TabScroller.jsx:50-52`).
2. There are unused imports: `ListIcon`, `ArrowRightIcon` and `useMemo` in `main.jsx:1, 4`.
3. **No favicon** (`frontend/index.html`). The tab shows a blank page icon.
4. Icons are not used where they would help scanning, such as status (located or missing quote, reviewed, needs decision, issue severity) or sheet tabs. Where they are used, they are decoration on buttons.

### 7.7 Code quality
1. **One-line mega-components.** `main.jsx:363` (delete modal), `:371` (Overview), `:391` (LedgerTab JSX), `:421` (SheetTab), `:427` (ReviewTab), each 2,000-6,000 characters. Diffs of a redesign will be unreadable unless these are split first. Splitting them does not change behaviour.
2. **Minified CSS by hand** (`style.css:4-22`). It has duplicated and out-of-order media rules (lines 11-18, 46-56, 76-94), 18 `!important`s to defeat Fluent (lines 19-22, 39-40), no tokens, and hard-coded pixel sizes everywhere.
3. **Semantics.** `<main>`, `<header>` and `<section>` exist, but the list panes are `<div>`s of `<button>`s with no list semantics. There is no `<aside>` for the filing and no skip link. The deal toolbar is not a `<header>`/`<nav>`. Issues are `<div>`s with no `role="status"` or field association.
4. **The bundle weight is mostly unused.** 466 KB JS (142 KB gzip): Fluent (for Button/Field/Input/Select/Spinner/Textarea) plus GSAP for a single fade.
5. **Inline style** appears only for `--split-size` (acceptable). The z-index values are 1/2/10/50, ad hoc but small.
6. **Legacy duplicate UI** (`app.js`, `style.css` and `index.html` at the cockpit root) is still served as the fallback (`server.py:28, 145, 148-152`). A redesign should leave it or retire it deliberately.
7. **Meta.** There is a title (and a per-deal `document.title`, which is good) but no favicon or theme-color. Social meta tags are irrelevant for this private tool.

### 7.8 Accessibility gaps (consolidated)
- Contrast failures listed in §7.2.8 (tab counts 2.65:1 are the worst).
- Text at 9-10 px in list metadata and hints.
- Missing or inconsistent focus rings (§7.4.1); the overview row outline is removed.
- Incomplete tab pattern (§7.4.2); no `aria-pressed` on the pane switch.
- Clickable `<tr>` without link semantics or Space support.
- Global arrow-key capture (§7.4.5).
- Colour alone distinguishes a quote highlight, the selected quote and a search hit (`style.css:8`).
- `role="alert"` is used for every Message, including the persistent "needs rechecking" warning inside a finding (`main.jsx:369, 427`). Screen readers announce these as interruptions.
- No skip link and no landmark for the filing pane (it is a `<section aria-label>`, which is acceptable).
- `aria-live` is on `.work-state` only; save success, failure and conflict rely on `role=alert` banners.

### 7.9 AI-default patterns, as a list
1. Monogram "L" in a blue rounded square (`main.jsx:368`)
2. Uppercase tracked eyebrows "RESEARCH WORKSPACE" and "SELECTED EVENT" (`main.jsx:371, 391`)
3. Giant pale ghost statistic "9" (`main.jsx:371`, `style.css:6`)
4. Tinted callout boxes with 3 px left borders for every kind of information (§7.2.4)
5. Card-inside-card surfaces: history → change, page → table wrapper, well → paper (§7.2.4)
6. Unthemed Fluent/system font; the specified brand font never appears (§7.1.1)
7. Pastel badge chips for counts and access (`style.css:5, 9`)
8. Blue-grey everything, with about 15 almost-identical blues (§2)
9. Uppercase table headers in 11 px (`style.css:6`)
10. The same sub-caption repeated on every row ("Location aid, not validation", `main.jsx:371`)
11. Explainer paragraphs as page furniture: "A finding is a recorded candidate…" and "Review status records a reader's judgment…" (`main.jsx:391, 427`). They are useful once and noise afterwards; consider a tooltip or a one-line note.
12. Centred max-width column for Review, Changes and History inside a working pane (`style.css:10`)
13. Heavy custom scrollbars styled in the accent colour (`style.css:61-74`)

---

## 8. Suggested priorities for the redesign agent (not decisions)
1. Build the token layer (colour, type, space, radius, elevation), and make Fluent use it through a custom theme (`createLightTheme` / `FluentProvider theme`). Doing this first fixes the font.
2. Choose a UI face plus a tabular or mono face for figures and IDs. Enlarge the filing text and cut its measure to about 70 characters. Set the minimum text size to 12 px.
3. Collapse the chrome: fold header and deal toolbar into one bar, put save status next to Save, and give the save dock a docked (non-overlapping) position.
4. Rethink highlight semantics in the filing: unselected, selected and search hit should differ by more than lightness.
5. Replace the callout soup with one issue style tied to fields, one quote style and one prior-decision style.
6. Decide with Austin whether the Ledger gets a table view. If it does, the list+editor classes and `split-*` behaviour that the tests pin must stay, or the tests must be updated deliberately.
7. Keep every selector and string in §4, or change the test in the same commit and say so.
