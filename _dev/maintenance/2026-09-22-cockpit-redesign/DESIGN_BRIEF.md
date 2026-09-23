# Ledger cockpit: design direction brief

Art direction for the redesign of `_dev/tools/cockpit/frontend/src`. Written 22 September 2026 against the audit in `AUDIT.md` (HEAD `da70736`) and the `before/` screenshots. The implementer follows this brief exactly; where it is silent, choose the plainer option.

Sources of truth, in order: (1) the test constraints in AUDIT §4, (2) this brief, (3) `_dev/COCKPIT_BUILD.md` "Design". If two conflict, stop and report rather than improvise.

---

## 1. Concept: working papers

The cockpit is an analyst's working-paper set laid beside the filing it was drawn from. That material culture is specific: the EDGAR text is typewritten and paginated; the printed prospectus is a serif document ruled into sections; the ledger is a register of numbered lines with figures that sit in columns; the working papers carry the researcher's own marks in one ink and one highlighter. Nothing in that world is a card, a chip or a tile. Hierarchy comes from rules, alignment and weight, not from boxes and fills. So the redesign is built on three faces with distinct jobs (a grotesk for the interface, a text serif for the filing, a typewriter mono for every figure, date, identifier and checker code), one neutral ink family on white paper with a barely warm stone ground, one control blue used only where the user acts, and one yellow used only where the filing has been quoted. Surfaces are flat. Separation is by 1 px hairlines and by a single heavier rule under column heads. Density is high because the users are two researchers who sit with this for hours: 12 to 13 px data, 24 to 32 px rows, 8 px gutters. The result should feel like a well-set register that happens to be interactive, not like a dashboard template.

---

## 2. Named defaults to avoid

Every item below is banned. The first group is what the app does today (with the audit reference); the second is what an AI redesign drifts toward.

Present now, to remove:
1. Monogram "L" in a blue rounded tile as a logo (`.brand-mark`).
2. Uppercase tracked eyebrows: "RESEARCH WORKSPACE", "SELECTED EVENT", "PAGE 2 (APPROXIMATE)", "BEFORE/AFTER" (`.eyebrow`, `.page-marker`, `.change-label`).
3. Uppercase 11 px table headers with letter-spacing (`.deal-table th`).
4. The giant ghost numeral "9" (`.overview-total`).
5. Tinted boxes with a 3 px left border for every kind of information: issues, proposals, evidence, recorded decisions, reference warnings, table rows in the filing, the yellow "Source evidence" box (AUDIT §7.2.4).
6. Cards inside cards: history item > change card; page > bordered table wrapper; grey well > shadowed "paper"; the "Row review" card inside the editor.
7. Pill and chip badges: tab counts, "Edit access", "Recorded documents" chips.
8. `text-transform: capitalize` on research strings (`.status-text`, `.finding-state`, `.change-head span`).
9. Blue-grey text everywhere, with about 45 near-identical greys and 15 blues.
10. Two different accent blues on one toolbar (Fluent brand `#0f6cbd` next to custom `#235a9e`).
11. Heavy 11 to 12 px scrollbars coloured in the accent, and 8 px grip-dot splitters.
12. Centred narrow columns (max-width 950) for Review, Changes and History inside a working pane.
13. A floating toast-like save dock overlapping the form.
14. Explainer paragraphs as permanent page furniture ("A finding is a recorded candidate…", "Review status records a reader's judgment…", "Location aid, not validation" on every row).
15. Rows of four identical small buttons with Delete undistinguished from Move up.
16. Generic centred spinners and grey centred sentences that look identical for loading, empty and error.

Stock looks the implementer must not introduce:
17. Cream or parchment page colour (anything warmer than the tokens below), and italic accent words in headings.
18. Numbered "01 / 02" section labels, roman numerals as decoration, or mono eyebrow labels above headings.
19. Pill buttons, pill inputs, or any radius above 6 px.
20. Gradients of any kind: backgrounds, buttons, logo tiles, text.
21. Glassmorphism, backdrop blur, noise or grain overlays, "spotlight" borders, tinted "premium" shadows.
22. Hero blocks, marketing spacing (anything above 32 px vertical padding), parallax, scroll-driven animation, staggered entry animations.
23. Skeleton shimmer loaders.
24. An icon in front of every heading or tab; emoji anywhere.
25. Inter, Roboto, Segoe or the system font as the visible interface face.
26. Dark-mode toggles or a dark theme in this pass.
27. Coloured status text without a shape (dot or glyph) beside it.
28. Bold (700) used for hierarchy on labels, tabs, metadata or table headers. 700 is reserved for the deal name and page h1 only.
29. Colour-tinted card backgrounds for sections ("light blue panel for review", "light yellow panel for evidence").
30. Sentence-length button labels, exclamation marks, "Oops", "Successfully".

---

## 3. Tokens

All tokens live in one `:root` block at the top of `style.css` and are mirrored into the Fluent theme in `main.jsx` (see §3.3 and §5). No hex value may appear in `style.css` outside `:root`. No `!important` may remain.

### 3.1 Colour

Light theme only (the build contract asks for a single light theme; do not add dark values).

```css
:root {
  /* neutral family: stone, barely warm (hue ~60, chroma ~1) */
  --paper:        #ffffff;   /* filing text, inputs, the working surface */
  --ground:       #f4f4f1;   /* app ground behind panes, headers, list columns */
  --tint:         #ebebe6;   /* hover on rows and list items; table head fill */
  --rule:         #e3e3de;   /* hairline separators (1.29:1 – decorative only) */
  --rule-strong:  #c9c9c2;   /* pane dividers, table head rule, splitter idle */
  --border-ctl:   #94948c;   /* input and button borders (3.06:1 on paper) */
  --ink:          #1a1a18;   /* primary text (17.4:1) */
  --ink-2:        #4a4a45;   /* secondary text: sublines, values in lists (8.9:1) */
  --ink-3:        #66665f;   /* metadata, labels, hints, placeholders (5.8:1 paper, 5.3:1 ground) */
  --ink-disabled: #7d7d76;   /* disabled control text (3.8:1 on ground) */

  /* one accent: control blue (retained from the build contract, see §5) */
  --accent:       #1f4f99;   /* links, primary button fill, focus ring, selected rule (7.96:1) */
  --accent-hover: #1c4a91;
  --accent-press: #1a4589;
  --accent-tint:  #eef3fa;   /* selected row background, active pane switch */
  --accent-wash:  #dbe7f8;   /* search-hit fill in the filing (ink 13.9:1) */

  /* semantic */
  --error:        #a12d22;   --error-bg:   #fbeeec;   /* 7.2:1 paper, 6.4:1 bg */
  --warning:      #7a4b00;   --warning-bg: #fdf3df;   /* 7.4:1 paper, 6.7:1 bg */
  --success:      #1e6b3d;   --success-bg: #e9f4ec;   /* 6.5:1 paper, 5.8:1 bg */

  /* quotation yellow: the one functional highlight (see §4.6) */
  --quote:        #fff1a8;   /* every located quote (ink 15.3:1) */
  --quote-active: #ffd23f;   /* the selected quote (ink 12.1:1) */
  --quote-rule:   #9a6f00;   /* 2 px underline under the selected quote (4.5:1 paper, 3.1:1 on quote-active) */

  --backdrop:     rgba(26, 26, 24, 0.45);
}
```

Rules of use:
- Text is `--ink`, `--ink-2` or `--ink-3`. Nothing else, except semantic and accent text.
- `--accent` appears only on: links, the primary button, the focus ring, the selected-item rule and tint, the active tab underline, the search-hit wash, and the "Use selected text for quote" button. It never colours headings, labels, counts or scrollbars.
- Semantic fills (`*-bg`) appear only on banners (`Message`), never on lists, issues or sections. Semantic text always has a glyph or dot beside it (see §4.10).
- `--tint` and `--accent-tint` are the only "panel" colours; no other fills.

### 3.2 Type

Three families, all self-hosted in `src/fonts/` with `@font-face` and `font-display: swap`, all latin subsets:

| Role | Family | Files | Weights |
|---|---|---|---|
| Interface (`--font-ui`) | Cabinet Grotesk (already bundled: `cabinet-400/500/700.woff2`; the files are ITF "Cabinet Grotesk", no `tnum` feature) | keep | 400, 500, 700 |
| Figures, dates, ids, codes (`--font-mono`) | IBM Plex Mono | `ibm-plex-mono-400.woff2`, `ibm-plex-mono-500.woff2` from the `@fontsource/ibm-plex-mono` package's `files/ibm-plex-mono-latin-{400,500}-normal.woff2` (`npm pack @fontsource/ibm-plex-mono@5` in the scratchpad, copy the two files; do not add the package as a dependency) | 400, 500 |
| Filing text and quoted evidence (`--font-serif`) | Source Serif 4 | `source-serif-4-400.woff2`, `source-serif-4-400i.woff2`, `source-serif-4-600.woff2` from `@fontsource/source-serif-4@5` `files/source-serif-4-latin-{400-normal,400-italic,600-normal}.woff2`, same method | 400, 400 italic, 600 |

Both npm registries and Google Fonts were reachable from this machine at audit time; the fontsource files are the licensed (OFL) woff2 latin subsets and are the preferred source. If the registry is unreachable, download the same three families' latin woff2 from Google Fonts CSS instead. Never load fonts from a CDN at runtime: the tool runs behind Cloudflare Access and must not leak requests.

```css
:root {
  --font-ui:    "Cabinet Grotesk", "Helvetica Neue", Arial, sans-serif;
  --font-mono:  "IBM Plex Mono", "SFMono-Regular", Menlo, Consolas, monospace;
  --font-serif: "Source Serif 4", Georgia, "Times New Roman", serif;

  /* scale: nothing below 12 px */
  --fs-12: 12px;  --lh-12: 16px;   /* metadata, labels, hints, mono figures in lists, counts */
  --fs-13: 13px;  --lh-13: 18px;   /* body data, inputs, list titles, buttons */
  --fs-14: 14px;  --lh-14: 20px;   /* finding bodies, modal text, quoted evidence */
  --fs-15: 15px;  --lh-15: 24px;   /* filing text (serif) */
  --fs-16: 16px;  --lh-16: 22px;   /* section h2, editor record title */
  --fs-20: 20px;  --lh-20: 26px;   /* deal name h1, overview h1 */

  --fw-regular: 400;  --fw-medium: 500;  --fw-bold: 700;
  --tracking-tight: -0.01em;  /* h1 only */
}
```

- Interface text is Cabinet 400; emphasis is Cabinet 500. 700 only on the two h1s (deal name, "Deal ledgers").
- Every number, date, price, count, event `#`, question id, revision number, sha prefix, page number and checker code (`controlled.type`) is set in `--font-mono` with `font-variant-numeric: tabular-nums` and `font-feature-settings: "tnum"`. Mono runs 0.5 px smaller optically, so mono at `--fs-12` beside Cabinet at `--fs-13` is the standard pairing; never mix them in the same word.
- The filing is `--font-serif` at `--fs-15/--lh-15`, measure `max-width: 66ch`. Filing headings are serif 600 at 15 px; nothing in the filing is uppercase.
- Letter-spacing is 0 everywhere except `--tracking-tight` on h1. No `text-transform` anywhere. Sentence case for every label and heading.
- `font-synthesis: none` stays on `:root`.

### 3.3 Fluent theme (the only way the font actually applies)

`main.jsx` must build the theme with `createLightTheme` and token overrides; `webLightTheme` is removed. This is what fixes AUDIT §0.1.

```js
import { createLightTheme } from '@fluentui/react-components';
const brand = { 10:'#06101f', 20:'#0b1a35', 30:'#0f244b', 40:'#122f62', 50:'#163b79', 60:'#1a4589',
  70:'#1c4a91', 80:'#1f4f99', 90:'#3663a7', 100:'#4d78b5', 110:'#668dc3', 120:'#82a3d0',
  130:'#9fb9dd', 140:'#bccfe8', 150:'#d8e4f2', 160:'#eef3fa' };
const cockpitTheme = {
  ...createLightTheme(brand),
  fontFamilyBase: '"Cabinet Grotesk", "Helvetica Neue", Arial, sans-serif',
  fontFamilyMonospace: '"IBM Plex Mono", SFMono-Regular, Menlo, Consolas, monospace',
  fontFamilyNumeric: '"IBM Plex Mono", SFMono-Regular, Menlo, Consolas, monospace',
  fontSizeBase200: '12px', lineHeightBase200: '16px',
  fontSizeBase300: '13px', lineHeightBase300: '18px',
  fontSizeBase400: '14px', lineHeightBase400: '20px',
  fontSizeBase500: '16px', lineHeightBase500: '22px',
  fontSizeBase600: '20px', lineHeightBase600: '26px',
  fontWeightSemibold: 500, fontWeightBold: 700,
  borderRadiusSmall: '2px', borderRadiusMedium: '3px', borderRadiusLarge: '4px', borderRadiusXLarge: '6px',
  colorNeutralBackground1: '#ffffff', colorNeutralBackground2: '#f4f4f1', colorNeutralBackground3: '#ebebe6',
  colorNeutralForeground1: '#1a1a18', colorNeutralForeground2: '#4a4a45', colorNeutralForeground3: '#66665f',
  colorNeutralForeground4: '#66665f', colorNeutralForegroundDisabled: '#7d7d76',
  colorNeutralStroke1: '#94948c', colorNeutralStroke2: '#c9c9c2', colorNeutralStroke3: '#e3e3de',
  colorNeutralStrokeAccessible: '#66665f', colorNeutralStrokeDisabled: '#c9c9c2',
  colorNeutralBackgroundDisabled: '#f4f4f1',
  colorStrokeFocus2: '#1f4f99',
};
<FluentProvider theme={cockpitTheme} className="cockpit">
```

Brand 80 is `--accent`, so `colorBrandBackground`, `colorBrandForeground1`, `colorBrandForegroundLink` and `colorCompoundBrandStroke` (the input focus underline) all resolve to the one blue automatically. Any remaining CSS override of a Fluent control uses the `.cockpit .fui-*` prefix (specificity 0,2,0 beats Griffel's atomic classes) instead of `!important`.

### 3.4 Space, radius, rules, elevation, layers

```css
:root {
  --sp-1: 2px; --sp-2: 4px; --sp-3: 8px; --sp-4: 12px; --sp-5: 16px; --sp-6: 24px; --sp-7: 32px;
  /* pane padding is --sp-5 on desktop, --sp-4 under 1150 px, --sp-3 under 560 px */

  --radius-0: 0;      /* rows, marks, rules, tabs, list items, page markers */
  --radius-1: 3px;    /* inputs, buttons, selects, banners */
  --radius-2: 6px;    /* modal only */

  --hairline: 1px solid var(--rule);
  --divider:  1px solid var(--rule-strong);   /* between panes; under table heads */

  --shadow-dock:  0 -1px 0 var(--rule-strong);            /* the save dock is docked, not floating: a top rule, no drop shadow */
  --shadow-modal: 0 12px 32px rgba(26, 26, 24, 0.18);     /* the only drop shadow in the app */

  --z-sticky: 1;     /* sticky section heads, table heads */
  --z-handle: 2;     /* split handles */
  --z-bar:    5;     /* global and deal bars */
  --z-dock:   10;    /* save dock */
  --z-modal:  50;    /* backdrop and modal */
}
```

Controls: inputs, selects and buttons are 28 px tall (Fluent `size="small"` is 24, `medium` is 32; use `medium` and set `.cockpit .fui-Input, .cockpit .fui-Select select, .cockpit .fui-Button { min-height: 28px }` with 13 px text). Icon-only buttons are 28×28. Icons are 16 px everywhere, `weight="regular"`; 20 px is allowed only inside banners.

### 3.5 Motion

- `--dur-1: 120ms` for colour, background, border and opacity on hover, press and focus. `--dur-2: 180ms` for `<details>` content, the selection bar and banner appearance. `--dur-3: 240ms` for the "Revision saved" fade (GSAP, existing).
- Easing: `--ease: cubic-bezier(0.2, 0, 0, 1)` for entrances; `ease-out` for exits. No springs, no bounce.
- What animates: colour and opacity only. Nothing translates, scales or slides. Layout never animates. The one exception is the selected quote in the filing: on selection its background may run once from `--paper` to `--quote-active` over 400 ms (GSAP or a CSS keyframe) so the eye finds it after `scrollIntoView`; it then stays at `--quote-active`.
- `@media (prefers-reduced-motion: reduce)` sets all durations to 0 and disables `scroll-behavior: smooth` and the flash. The existing guard stays.
- Hover: background to `--tint` (rows, list items, subtle buttons). Press: background to `--rule` on subtle buttons; primary goes to `--accent-press`. No transform on press.

---

## 4. Component-by-component direction

### 4.1 Global bar and brand
Becomes a 40 px bar on `--ground` with a bottom `--divider`. Left: the wordmark "Ledger cockpit" as plain text, Cabinet 500 at 14 px, `--ink`, no tile, no icon; it remains `button.wordmark` and navigates home. Next to it, the context ("Deal ledgers" / "Deal workspace") in `--ink-3` at 13 px separated by a 1 px vertical rule 16 px tall, not a dot. Right: user name in `--ink-2` 13 px, then the access state as a 6 px dot plus text at 12 px (dot `--success` for "Edit access", `--ink-3` for "Read only", `--warning` for "Loading session"); no chip. Favicon: add `frontend/public/favicon.svg`, a 16×16 mark of three horizontal 1.5 px rules in `--ink` with one vertical rule at x=5 (a ruled ledger column), and link it from `index.html` with `<meta name="theme-color" content="#f4f4f1">`.

Why: the tile monogram is the strongest "AI template" signal on every screen; a wordmark and a rule are how a working document is labelled.

### 4.2 Overview (landing)
`main.overview-wrap` keeps `max-width: 1500px`, padding `--sp-6 --sp-7`. The title block is one baseline row: `h1` "Deal ledgers" at `--fs-20` 700, then "9 deals" in `--font-mono --fs-12 --ink-3` on the same baseline (keep the sentence "9 deals available. Open a deal…" as the row's `p` but shorten the visible copy to "9 deals · open one to inspect the filing and edit its working copy"; the h1 text stays exactly "Deal ledgers"). Remove the eyebrow and the ghost numeral entirely.

The table loses its wrapper border, radius and white card. The overview page itself is `--paper` (`.overview-wrap { background: var(--paper); min-height: calc(100dvh - 40px) }`) and the table is ruled, not boxed. `th`: sentence case, `--fs-12` 500 `--ink-3`, padding `8px 12px`, `border-bottom: 1px solid var(--ink)` (the one heavy rule). `td`: `--fs-13`, padding `10px 12px`, `border-bottom: var(--hairline)`, vertical-align baseline. Row height about 56 px (two lines), not 100. Deal name: an `<a href="/deal/<slug>">` in `--accent` 500 (real link: middle-click and copy work); the whole `<tr>` remains clickable and focusable with the ring in §4.14, and Space must also activate it. Slug under the name in mono 12 `--ink-3`. Filing form and date: mono 12. Working copy: "Opus 5.5 medium extraction" 13 px, "Revision 0" mono 12 below. Events / Rounds / Questions: mono 13, right-aligned, header right-aligned too. Source evidence: "71 / 71 quotes located" in mono 13; below it "0 errors · 21 warnings" mono 12, with the error count in `--error` plus a 12 px `WarningCircle` glyph only when errors > 0. Delete the per-row "Location aid, not validation"; render it once as a footnote under the table in `--fs-12 --ink-3`. Review state: plain text, no `capitalize`, exactly as the API returns it.

Hover: row background `--tint`. Empty state: `div.empty` becomes a left-aligned 13 px sentence in `--ink-2` under the header rule, not centred.

### 4.3 Deal bar (toolbar)
Collapse from 124 px to 56 px, one row on `--ground` with a bottom `--divider`, `position: sticky; top: 0; z-index: var(--z-bar)`. Left group: `button.back-link` "All deals" as a subtle icon+text button (`ArrowLeft` 16, 13 px `--accent`), then `h1` deal name at `--fs-20` 700 `--ink`, then `div.deal-subline` inline on the same baseline in mono 12 `--ink-3`: `DEFM14A · 2016-11-29 · from Opus 5.5 medium extraction · Revision 0` (keep the exact substrings "Revision N", "Opus 5.5 medium extraction" and "Source version" that tests read; the separators are `·`). Right group (`div.toolbar-actions`): the `Version` label (12 px `--ink-3`) with the native Fluent `Select` (width 240, mono 13 for the option text is not possible in native options; leave the select's own font as Cabinet 13); "Export Excel" rendered as `<Button as="a" href=… download appearance="secondary" icon={<DownloadSimple/>}>` so it is a real link styled identically to other buttons (drop `.export-link`); then `div.save-line` moved **between** Export and Save: `span.work-state` in 12 px, with a dot: `--warning` dot + "N unsaved changes", `--success` dot + "Saved", `--ink-3` + "No unsaved edits" / "Read only version"; `span.save-feedback` "Revision saved" beside it; the "Last saved by … · date" line goes to the History tab head and the `title` attribute of the work-state span, not the bar. Finally the primary "Save changes" button.

Under 1150 px the subline wraps to a second line under the h1 (bar becomes 80 px). Under 820 px the bar stacks into three rows: name+subline, version select full width, Export + Save half-width each, work-state left under them (see §4.16).

### 4.4 Sheet tabs
`nav.tabs` sits on `--ground` with a bottom `--hairline`; tabs are text buttons 13 px `--ink-2`, padding `8px 12px`, no radius. Active: `--ink` 500 with a 2 px `--ink` underline sitting on the hairline (not blue: the accent is for actions, the tab is a place). Counts follow the label as mono 12 `--ink-3` with a 6 px gap and no chip; the label text stays first (tests match `/^Ledger(\b|$)/`). The `TabScroller` arrow buttons stay (tests) but the native scrollbar is hidden (`scrollbar-width: none; ::-webkit-scrollbar { display: none }`) so arrows and bar never show together. Add `id`/`aria-controls` and `aria-labelledby` on the tabpanel, and left/right arrow roving with `tabIndex=-1` on inactive tabs.

### 4.5 Event list and cards (Ledger, and the Rounds / Questions / Facts lists)
Not cards. `div.record-list` is a ruled register on `--paper` with a `--divider` on its right. `.section-head`: "Events" `h2` at `--fs-16` 500 with the count in mono 12 `--ink-3` on the same baseline, the "Add" button at the right as a small secondary button with `Plus` 16; padding `12px 16px`; `border-bottom: var(--divider)`; sticky at the top of the list (`--z-sticky`).

Each `button.event-item` is a row with `padding: 8px 12px 8px 16px`, `border-bottom: var(--hairline)`, `text-align: left`, no radius, `border-left: 2px solid transparent`. Layout, two lines:
- Line 1: `.event-number` mono 12 500 `--ink` ("#12"), `.event-date` mono 12 `--ink-2` ("2016-01-19" or "June 2016 or later"), and at the right end `.event-review` as a dot only (`--success` for reviewed, `--warning` for needs_decision, none for unreviewed) with `title`.
- Line 2: `strong` title 13 px 500 `--ink`, then `.event-detail` 12 px `--ink-3` truncated to one line with `text-overflow: ellipsis` (the full string stays in `title`).
- `.quote-location` moves onto line 1 right-aligned before the dot: mono 12 `--ink-3` "p. 27" when located; when missing, `Warning` 12 px glyph in `--warning` plus "no quote". The class stays (tests measure it).
Selected: `border-left-color: var(--accent); background: var(--accent-tint)`. Hover: `--tint`. Focus: §4.14. New (staged) rows: the number cell shows "New" in mono 12 `--warning` with a `--warning` dot.

In `split-horizontal` (compact) mode the same rows become 168 px wide compact cards laid out horizontally, still ruled (`border-right: var(--hairline)`), with the three lines stacked; the height stays ≥ the value the tests require for `.quote-location` to sit 8 px above the strip bottom.

`.sheet-item` (Rounds, Questions, Facts) follows the same row recipe: id or field in mono 12 500 on line 1, one-line truncated text 13 px on line 2.

### 4.6 Record editor (form)
`div.record-editor` on `--paper`, padding `16px 20px 32px`, scrollable. `.editor-head`: no eyebrow. `h2` "#N Event" with the `#N` part in mono (wrap it in `<span class="record-id">`) at `--fs-16` 500 and the title in Cabinet; the subline ("2016-01-19 · Party A") in 12 px `--ink-3`; the ↑ ↓ nav as two 28 px subtle icon buttons at the right.

`.record-actions`: a single row, `border-bottom: var(--hairline)`, `padding: 8px 0`. Left: "Move up", "Move down", "Clone to split" as subtle buttons with 16 px icons, 13 px. Right: "Delete" as a subtle button in `--error` text with `Trash` 16 (it stays the unique exact "Delete" button). Space between them makes Delete unmistakable without a red fill.

`.source-summary` stops being a yellow box. It becomes one line at 13 px: `Quotes` glyph 16 in `--quote-rule`, "Quote located · p. 27" (page in mono), or `Warning` 16 in `--warning` with "Quote not located in the filing"; the "Show in filing" button at the right as secondary small. Rule below.

Issues (`.issues`): one list, no fills, no left borders. Each `.issue` is a row `padding: 6px 0`, `border-bottom: var(--hairline)`, `font-size: 12px`, grid `16px auto 1fr`: severity glyph (`XCircle` `--error`, `Warning` `--warning`, `Info` `--ink-3`), the code in mono 12 `--ink-2` (`controlled.type`), then the message in `--ink`. Each row also gets `data-field` so the matching field label can show a 12 px severity glyph after its text (`Field` `label` slot). Sort errors first. The list is capped visually: after five rows show a "Show N more" text button.

Field grid: two columns `repeat(2, minmax(0, 1fr))`, gap `12px 16px`, one column under 440 px container width (existing rule). Labels: 12 px 500 `--ink-3` with 4 px below. Values: Fluent `Input`/`Select`/`Textarea` at 13 px, `--border-ctl` outline, radius 3. Mono class on the input slot for `#`, When, Sort date, Date from, Date to, Process, Round, Price low, Price high, Count, Page and any field whose name contains "date", "price", "count" or "page" (`input={{ className: 'mono' }}`). Field order changes: the evidence quote textarea (`.evidence-field`) and its page input move to the top of the grid, quote spanning both columns (`.span-all`), set in `--font-serif` 14/20 so it reads as filing text, followed by Page (mono, 96 px wide). Everything else keeps its current order. Hints: 12 px `--ink-3`. Read-only versions: inputs keep `--paper` background with `--ink-2` text and `--rule-strong` border (Fluent disabled tokens above already give this; remove the `!important` restyles).

Long-text fields: textareas default to `min-height: 96px` and auto-grow to their content up to 40 vh (`field-sizing: content` where supported, plus the existing `resize: both` on `.resizable-textarea`, which the tests need). This fixes r06's trapped text.

`.reference-links` ("Linked questions" / "Referenced events"): label 12 px 500 `--ink-3`, then buttons as subtle text buttons in `--accent` 13 px with the id in mono ("Q1 · When did Party A bid?").

`.review-box`: not a card. A section after a `--divider`, `h3` "Row review" at 13 px 500, the explanatory sentence moved into the Status field's hint at 12 px. Status select and note textarea as ordinary fields.

Dirty marking: a field whose value is staged gets a 2 px `--warning` left border on the Fluent input root (`.cockpit .fui-Input.is-dirty { border-left: 2px solid var(--warning) }`) and the label gets "· edited" in mono 12 `--warning`. This requires the editor to know which fields are in `ops`; it is a small lookup by `uid` and column.

### 4.7 Filing pane and quote highlighting
`section.filing-pane` background `--paper`. `.filing-tools`: one 44 px row on `--ground` with a bottom `--hairline`: "SEC filing" 13 px 500, form and date in mono 12 `--ink-3`, the search `Input` (`contentBefore` `MagnifyingGlass` 16, flex 1, min 160), `.search-count` mono 12 `--ink-3` (format stays `${i} / ${n}`), ↑ ↓ as 28 px subtle icon buttons, then "Page" label 12 px, `Input#filing-page` mono 72 px wide, "Go" secondary small. Under 1200 px the tools wrap to two rows (search row, page row) with the same heights. The disabled "Go" uses the disabled tokens (no grey slab).

Remove the grey well and the shadowed paper. `.filing-scroll` is `--paper`, padding `24px 32px 96px`. `.filing-paper` is a column `max-width: 66ch` (of the 15 px serif), `margin: 0 auto`, no border, no shadow, no background. Text: `--font-serif --fs-15/--lh-15 --ink`. `.filing-block` margin `0 0 12px`. `.filing-block.heading`: serif 600, margin-top 24 px. `.filing-block.table-row`: no left rule; render in mono 13/20 with `white-space: pre` inside an `overflow-x: auto` block (EDGAR tables are typewritten columns; a mono face keeps them aligned). `.filing-block.background-start`: `border-top: 1px solid var(--ink)`, padding-top 16 px, and a preceding mono 12 `--ink-3` label "Background section" (not uppercase).

`.page-marker`: mono 12 `--ink-3`, sentence case "Page 29", `border-top: var(--hairline)`, `padding-top: 6px`, `margin: 32px 0 16px`. `.approximate` appends " (approximate)" in `--warning` with a `Warning` 12 glyph; not orange text alone.

Highlighting (the functional signal; keep `mark.quote-mark`, `.selected`, `mark.search-mark`, `data-row-index`, `data-search-index`):
- `mark.quote-mark`: `background: var(--quote)`, `color: var(--ink)`, `box-decoration-break: clone`, `padding: 1px 0`, cursor pointer. Hover: `background: var(--quote-active)`.
- `mark.quote-mark.selected`: `background: var(--quote-active)`, `border-bottom: 2px solid var(--quote-rule)`, `padding-bottom: 0`. Selection differs by fill **and** an underline, so it survives the "everything is yellow" case (r03).
- `mark.search-mark`: `background: var(--accent-wash)`, `text-decoration: underline dotted var(--accent) 1.5px`, `text-underline-offset: 2px`. When a search hit is inside a quote, the wash replaces the yellow only for the matched substring and the dotted underline remains, so hue plus decoration distinguishes it. The current-hit (the `i` in `i / n`) additionally gets `outline: 2px solid var(--accent); outline-offset: 1px`.

`.selection-action` ("Use selected text for quote"): a 36 px row on `--ground` with a bottom hairline; the selected snippet in serif 13 `--ink-2` truncated; the button primary small. No yellow: yellow means "quoted", and this text is not yet.

`.page-error`: 12 px `--error` with `WarningCircle` 16, on `--error-bg`, `border-bottom: 1px solid var(--error)`, padding `6px 16px`.

`.pane-state`: loading = `Spinner size="tiny"` plus "Loading filing" 13 px `--ink-3`, left-aligned at the top of the column, padding 24 px; error = `Message` error banner inside the pane (not bare red text) whose body says "The filing could not be loaded." with the server string beneath in mono 12 `--ink-3`.

### 4.8 Findings and the Review tab
`div.review-tab` is left-aligned, `max-width: 880px`, padding `16px 24px 80px`, no centring. `.section-head`: `h2` "Review findings" `--fs-16` 500, count mono 12. The intro paragraph is removed from the page body and becomes the `title`/hint of the heading: render it as one 12 px `--ink-3` line directly under the heading, max two lines, not a paragraph block.

`details.mechanical-panel`: `summary` as a row `padding: 10px 0`, `border-top: var(--divider)`, `border-bottom: var(--hairline)`: `CaretRight` 16 rotating 90° when open (`--dur-2`), "Mechanical check" 13 px 500, then "0 errors · 21 warnings · pass with warnings" in mono 12 with the error number in `--error` when > 0 and the verdict text in `--success`/`--warning`/`--error` with a dot. `.mechanical-content`: the two disclaimer sentences as one 12 px `--ink-3` paragraph; then the checks as the same ruled issue rows as §4.6 (glyph, `Deal ledger · 2` mono, code mono, message), no fills.

`.documents`: "Recorded documents" 12 px 500 `--ink-3`, then subtle text buttons in `--accent` 13 px with `FileText` 16; no chip borders.

`article.finding`: `border-top: var(--hairline)`; the last has a bottom hairline too. `button.finding-title`: row `padding: 12px 0`, grid `1fr auto 16px`: `strong` 14 px 500 `--ink` and `small` 12 px `--ink-3` beneath ("Synthetic raw · E8", id in mono); `.finding-state` as a 6 px dot + judgment text exactly as stored (lowercase, no capitalize) in mono 12: `unreviewed` `--ink-3`, `supported` `--success`, `rejected` `--error`, `deferred` `--warning`; caret 16. Open: `aria-expanded` and the caret rotates.

`.finding-body` 14/20 `--ink-2`, padding `0 0 20px 0`. Sub-blocks are labelled paragraphs, not boxes: a 12 px 500 `--ink-3` label ("Recorded proposal", "Prior decision by Austin Li · 2026-09-21" with the date in mono) then the text in 14 px `--ink`. The recheck `Message(warning)` stays a banner (semantic fills are allowed on banners) but 12 px, `role="status"` not `alert`. `.finding-evidence`: label "Recorded evidence"; the `blockquote` is serif 14/20 with the quote text wrapped in `<mark class="quote-mark">` so evidence is yellow exactly like the filing (one meaning for one colour); `cite` mono 12 `--ink-3` "p. 1"; "Find quote in filing" as a subtle `--accent` text button. `.source-rows` mono 12. `.decision-grid`: three Fluent `Select`s (native, labelled "Finding judgment", "Correction implementation", "Verification"), labels 12 px; "Decision note" textarea; `.audit-line` mono 12 `--ink-3`.

### 4.9 Changes and History
Same container as §4.8 (left-aligned, 880). `.change` is not a card: a ruled entry `border-top: var(--hairline)`, `padding: 10px 0`. `.change-head`: the path "Deal ledger · Event #2 · Who" in 13 px 500 with ids in mono, and the type ("Update", "Insert", "Delete") right-aligned mono 12 `--ink-3` with no capitalize. Body: a two-column grid `96px 1fr`: label cell "Before" / "After" 12 px `--ink-3` sentence case (no uppercase), value cell 13 px `--ink` `white-space: pre-wrap`; deleted text in `--error` with a `line-through`, inserted in `--success`. Inserted rows are not shown as JSON: render the object as a `dl` of `field: value` rows (mono field names at 12 px). This is a display change only.

`.history-item`: ruled entry, `border-top: var(--divider)`, `padding: 12px 0`. `.history-head`: "Revision 1" 14 px 500 with the number in mono; timestamp and actor mono 12 `--ink-3` (locale string is fine); "Restore" as secondary small at the right. Reason 13 px `--ink`. `.history-summary` mono 12. The `<details>` uses the same caret summary as §4.8 and its content inherits `--ink`, not link blue. Empty Changes/History: a 13 px `--ink-2` sentence, left-aligned.

### 4.10 Badges and status
There are no badges. Status is always dot + text or glyph + text: 6 px dots (`display:inline-block; border-radius: 50%` is the one circular thing allowed) in `--success`, `--warning`, `--error`, `--ink-3`; glyphs are Phosphor `CheckCircle`, `Warning`, `XCircle`, `Info` at 16 (12 in list metadata). Counts are mono numbers. Text never changes case.

### 4.11 Version picker
Stays a native `<select>` through Fluent `Select` (tests). Visible label "Version" 12 px `--ink-3` to its left. Width 240. When the selected version is immutable, the `deal-subline` already shows "Source version"; add a `LockSimple` 14 glyph in `--ink-3` immediately before the select and set the select's `title` to "Read only version". Nothing else changes.

### 4.12 Buttons
Only Fluent `Button`. Four appearances, nothing custom:
- `primary`: `--accent` fill, white text 13 px 500, radius 3, height 28; hover `--accent-hover`; press `--accent-press`. One per view (Save changes; the dock's "Save N changes"; "Use selected text for quote"; the mobile pane switch active state).
- `secondary`: `--paper` fill, `--border-ctl` 1 px, `--ink` text; hover `--tint`. Export, Go, Add, Show in filing, Restore, Cancel.
- `subtle`: no border, `--ink-2` text; hover `--tint`. Move up/down, Clone, nav arrows, search arrows, document links, reference links, Delete (with `--error` text).
- `transparent`: never.
Icon-only buttons need `aria-label` (existing). `.back-link` and `.wordmark` are rendered with Fluent `Button appearance="subtle"` too, so there are no hand-styled button imitations left.

### 4.13 Inputs and selects
Fluent `Input` and `Select` with the theme tokens from §3.3: 1 px `--border-ctl` outline, radius 3, 28 px, 13 px text, `--paper` fill; placeholder `--ink-3`. Fluent's bottom focus underline stays and resolves to `--accent`. Mono class on numeric inputs (§4.6). Textareas share the outline and get `line-height: 20px`. Field labels are always visible (never placeholder-only). Error state: `validationState="error"` on `Field` with the message 12 px `--error` and a `XCircle` 12 glyph.

### 4.14 Focus rings
One rule for every custom interactive element (`.event-item`, `.sheet-item`, `.tabs button`, `.finding-title`, `.deal-table tbody tr`, `.split-handle`, `.tab-scroll-control`, `.modal-head button`, `.wordmark`, `mark.quote-mark` when it has `tabIndex`):
`:focus-visible { outline: 2px solid var(--accent); outline-offset: -2px; }` for rows and tabs (inset so it does not clip in scroll panes) and `outline-offset: 2px` for buttons and handles. Delete `tbody tr:focus { outline: none }`. Fluent controls keep their own ring, which the theme colours `--accent` via `colorStrokeFocus2`.

### 4.15 Scrollbars, splitters, save dock, modals, banners
Scrollbars: `scrollbar-width: thin; scrollbar-color: var(--rule-strong) transparent;` and for WebKit 8 px, thumb `--rule-strong` with radius 4, track transparent, thumb hover `--border-ctl`. Never the accent. `scrollbar-gutter: stable` stays on `.filing-scroll`.

Splitters (`.split-handle`): a 1 px `--rule-strong` line with an 8 px transparent hit area; no grip dots. On hover and focus the line becomes 2 px `--accent` (`--dur-1`); the focus ring rule above applies. Behaviour unchanged.

Save dock (`.save-dock`): docked, not floating. Desktop: `position: sticky; bottom: 0` at the end of `.workspace-column`, full width of the column, `--ground` background, `box-shadow: var(--shadow-dock)`, padding `8px 16px`, one row: "Reason for this revision" input (flex 1, label visible at 12 px to its left, hint "Appears in history" as `title` and Fluent `hint`), then the primary "Save N change(s)" (text unchanged: it must not contain "Save changes"). Narrow: same bar `position: fixed; bottom: 0; left: 0; right: 0`. It never covers form fields on desktop because the column reserves its height.

Modals: `.modal` `--paper`, radius 6, `--shadow-modal`, padding 20 px, width `min(520px, 100%)`; `h2` 16 px 500; body 13 px `--ink-2`; actions right-aligned with secondary Cancel and primary/`--error`-text "Stage deletion" (secondary appearance with `--error` text and border: a destructive action is still not a red fill). `.modal-backdrop` `--backdrop`. Document modal: the `pre` becomes serif 14/22 `white-space: pre-wrap` with mono only for lines that look tabular; keep the top hairline.

Banners (`Message`): 13 px, radius 3, 1 px border in the semantic colour, semantic fill, glyph 20 at the left, padding `8px 12px`; error `role="alert"`, warning and info `role="status"`. Error text is human first, server string second: "This deal could not be loaded." then the raw message in mono 12 `--ink-3`. The unknown-deal page keeps the global bar and adds an "All deals" subtle button inside the banner so there is a way back. Conflict banner keeps its two buttons (exact strings).

Loading: `Spinner size="tiny"` with its label 13 px `--ink-3`, left-aligned at the top of the pane it replaces (`.center-state` is renamed in CSS only if no test needs it; it does not). On a version switch, keep the filing pane mounted and only replace the workspace (set `deal` rows to null rather than the whole `deal`), so the filing does not blank.

Empty: 13 px `--ink-2` sentence, left-aligned under the section head, with a 16 px `--ink-3` glyph (`Tray`) before it so it differs from loading.

### 4.16 Narrow and mobile layout (≤ 820 px, and 400 px)
Breakpoints stay as in AUDIT §1 (1200, 1150, 820, 560, 680 container, 440/520 container). Order at 400 px, top to bottom: global bar 40; deal bar three rows (name+subline 44, version 36, Export|Save 36 with the work-state line 20) = 136; pane switch 36; tabs 36; then content. That is about 250 px of chrome instead of 510. The pane switch (`role=group` "Visible pane", buttons "Filing"/"Workspace") is a two-segment control: secondary buttons joined (`border-radius` only on the outer corners), the active one `appearance="primary"` and `aria-pressed="true"`. In `split-horizontal` mode the event strip is 88 px tall (three lines of 12/13 px) with rows of 168 px; the row-resize handle stays. The save dock is the fixed bottom bar. Field grid is one column under 440 px. Nothing scrolls horizontally except the strip and the overview table (`overflow-x: auto` on `.deal-table-wrap`).

---

## 5. Constraints the implementer must respect

1. **Every selector, ARIA role and name, string, native `<select>`, `window.confirm` and breakpoint in AUDIT §4** stays exactly as listed. In particular: `.event-item`, `.sheet-item`, `.record-editor`, `.record-list`, `.sheet-list`, `.sheet-body`, `.ledger-layout` with `split-horizontal`/`split-vertical`, `.workbench > .split-handle`, `.filing-scroll`, `.filing-block`, `mark.quote-mark(.selected)`, `mark.search-mark`, `.quote-location`, `.resizable-textarea`, `.finding-title`, `.finding-body`, `.review-box`, `.mechanical-panel summary`, `.mechanical-content`, `.history-item`, `.deal-subline`, `.deal-table tbody tr`, `.tabs`, `.save-dock`, `.reference-links`, `.sheet-editor h3`; the strings "Revision saved", "Read only version", "No unsaved edits", "Source version", "Save changes", "Save N change(s)", "Stage deletion", "Show in filing", "Find quote in filing", "Open question Qn", "All deals", "Export Excel", dialog "Delete record", group "Visible pane", region "SEC filing"; the `${i} / ${n}` counter; `#row-n` hashes; `STACK_WIDTH` 680 and the 47 % default split. Run all five suites from AUDIT §5 before and after.
2. **Keep Fluent UI React 9.72.3 and `@phosphor-icons/react` as the single icon family.** No new UI dependency. The font files are copied into `src/fonts/`, not installed as packages. GSAP stays for the "Revision saved" fade and the optional quote flash only.
3. **Keep the yellow quote highlight** as the functional signal, with the three-state scheme in §4.7 (`--quote`, `--quote-active` + underline, `--accent-wash` + dotted underline for search).
4. **Accent: keep blue, but one blue.** Recommendation: retain the contract's blue control accent and set it to `#1f4f99` (brand 80), replacing both Fluent's `#0f6cbd` and the fifteen custom blues. This is a value change inside the contract's rule, not a change of the rule; record "`#1f4f99` control blue, one value, actions only" in `COCKPIT_BUILD.md` "Design". I considered a non-blue accent (an ink-black primary, or the ochre of the quote rule) and rejected both: black primaries fight the ink hierarchy of a ruled page, and any yellow-adjacent accent would steal the meaning reserved for quotations.
5. **Fix the capitalize rule.** Delete `text-transform: capitalize` from `.status-text`, `.finding-state` and `.change-head span`, and add no `text-transform` anywhere. Research strings render exactly as stored.
6. **Never `npm run build`.** Build only with `npx vite build --outDir $S/preview-dist --emptyOutDir` and serve with `serve_preview.py` per AUDIT §5. Deploying to `dist/` requires Austin's authorisation.
7. **Do not truncate or rewrite research text.** Ellipsis truncation is allowed only in list rows (`.event-detail`, `.sheet-item span`) where the full text is one click away and present in `title`.
8. **Split the one-line mega components** (`main.jsx:363, 371, 391, 421, 427`) into readable multi-line JSX before restyling; no behaviour change. Rewrite `style.css` unminified, tokens first, then base, then components in tree order, then media queries in one section at the end.
9. Minimum text size 12 px; every text/background pair in this brief is AA and the implementer must not introduce new pairs.
10. `role="alert"` only on error banners; warnings and statuses use `role="status"`.

---

## 6. Out of scope: proposal to Austin (not in the implementation plan)

**Give the Ledger, Rounds and Questions sheets a table view, with the editor as a drawer.** Today each sheet is a list of two-line summaries plus a 20-field form for one record. A researcher cannot see the Type column for all 71 events, spot the two rows whose Price low is blank, or compare neighbouring rounds. Proposal:

- Add a "Table" / "Form" toggle in each sheet's `.section-head`. Table mode renders the sheet as a real `<table>` in the register style of §4.2: sticky mono column head, one row per record, tabular figures, dates and prices right-aligned, quote page as a mono cell, issues as a glyph cell, review dot. Columns are chosen from a checklist (default: #, When, Who, Type, Event, Process, Round, Price low, Price high, Count, Exit reason, Page), remembered in `localStorage`.
- Clicking a row opens the existing `.record-editor` as a right-hand drawer (desktop) or full pane (narrow), so the form, tests and `#row-n` behaviour are untouched. Form mode remains the default so `test_resize`/`test_responsive`, which pin the list+editor DOM and the `split-*` classes, keep passing; the table is an additive mode.
- In-cell editing comes later, if at all; first ship read-only scanning with click-to-edit in the drawer.
- Deal facts is a two-column key/value sheet and should be a table always.

Cost: about a day of frontend work plus one new acceptance check for the toggle. Benefit: the review moves from one-record-at-a-time to column scanning, which is what a "spreadsheet-like" review tool means.

---

## 7. Review checklist (for the after-screenshots)

1. Computed font on a tab label, a Fluent input value and a button is "Cabinet Grotesk"; on a price, date, `#` and checker code it is "IBM Plex Mono"; on the filing it is "Source Serif 4". Zero nodes in Segoe/Roboto/SF (probe as in AUDIT §0.1).
2. `style.css` has no hex outside `:root`, no `!important`, no `text-transform`, no font-size below 12 px.
3. No monogram tile, eyebrow, ghost numeral, chip, pill or left-border callout on any screen (d02, d05, d07, d18, r01).
4. Overview: ruled table with one heavy head rule, deal names are real links, numbers mono right-aligned, review state rendered exactly as the API string (r01 shows "unreviewed; Austin review pending" in lowercase).
5. Deal bar is one row of 56 px at 1440 with the work-state dot beside Save; chrome above the content at 1440 totals ≤ 136 px (40 + 56 + tabs 36 + section head), at 400 px ≤ 260 px.
6. Tabs: ink underline on the active tab, mono counts, no chips, no scrollbar visible beside the arrow buttons at 400 px.
7. Event rows: two lines, mono number and date, page in mono at the right, selected row has the 2 px accent rule and tint; hover tints; the compact strip at 1024 and 850 uses the same rows.
8. Editor: quote field first and in serif; Delete visually separated in error text; issues are a ruled glyph list with mono codes and no fills; the "Source evidence" line is text, not a yellow box; Row review is a ruled section, not a card.
9. Dirty state: an edited field shows the warning left rule and "edited" label; the work-state shows the warning dot; the save dock is docked (no form field hidden beneath it at 1024×600 or 1440×900).
10. Filing: no grey well, no paper shadow; serif 15/24 at ≤ 66ch; page markers in mono sentence case; table rows in mono; the selected quote shows the darker yellow and an underline; a search hit shows the blue wash and dotted underline, distinguishable in greyscale (check by desaturating r04 and d08).
11. Quote highlighting on Datalink (r03): unselected quotes are the pale yellow, only one span is `--quote-active`, and it is visible in the viewport after selecting event #21.
12. Review tab: left-aligned 880 column; finding rows with a dot + lowercase judgment in mono; proposals and prior decisions are labelled paragraphs; evidence is serif with the same yellow mark as the filing; the recheck banner is the only filled surface.
13. Mechanical check: summary line with mono counts and a coloured verdict dot; content is the ruled issue list (r10 shows no amber boxes).
14. Changes and History: ruled entries, "Before/After" in sentence case, inserted rows rendered as field: value rows, no JSON; history body text in ink, not blue.
15. Buttons: exactly four Fluent appearances; "Export Excel" is an `<a>` styled identically to secondary buttons; no hand-styled button imitations remain.
16. Focus: tabbing through overview rows, event rows, tabs, finding titles, splitters and buttons shows the 2 px accent ring on each; no element has `outline: none` without a replacement.
17. Scrollbars are thin and grey; splitters are 1 px lines that thicken to accent on hover/focus; the r03 "four scrollbars and two grips" band is gone.
18. Error and empty states: human sentence first, server string in mono second; unknown deal page has an "All deals" way back (d32); filing error is a banner, not red text (d33); empty Changes shows the glyph + sentence, distinguishable from loading.
19. Narrow (400 px): the three-row deal bar, segmented pane switch with `aria-pressed`, 88 px event strip, fixed bottom save dock; no horizontal document overflow at 1440, 1280, 1024, 850, 768, 560, 390.
20. Motion: hover and press transitions are 120 ms colour-only; nothing translates or scales; with `prefers-reduced-motion` no transition or flash runs.
21. All five suites in AUDIT §5 pass against `preview-dist`; `dist/` is unchanged (`git status` clean for `_dev/tools/cockpit/dist`).
22. `index.html` has the favicon and theme-color; the browser tab shows the ruled mark.
