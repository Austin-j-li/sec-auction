// Ledger review cockpit (iteration 1, read-only).
// Left pane: the filing, rendered once per deal, every located ledger quote
// wrapped in <mark>. Right pane: tabs of ledger row cards, rounds, questions,
// deal facts and checker findings. All filing and workbook text is inserted
// with textContent / createElement, never innerHTML.
"use strict";

const app = document.getElementById("app");
const crumbs = document.getElementById("crumbs");
const bar = document.getElementById("bar");

const filingCache = new Map();   // slug -> {file, filing}: /api/filing payload (large; fetched once per page load)
let lastReader = "";             // reader name from the most recent deal payload
let view = null;                 // state of the open deal page, or null on the deals list
let routeToken = 0;              // guards against out-of-order async route loads

/* ------------------------------------------------------------ helpers */

function el(tag, attrs, ...kids) {
  const e = document.createElement(tag);
  if (attrs) {
    for (const [k, v] of Object.entries(attrs)) {
      if (v == null || v === false) continue;
      if (k === "class") e.className = v;
      else if (k === "text") e.textContent = v;
      else if (k === "hidden") e.hidden = true;
      else if (k.startsWith("on")) e.addEventListener(k.slice(2), v);
      else e.setAttribute(k, v === true ? "" : String(v));
    }
  }
  for (const kid of kids.flat()) {
    if (kid == null || kid === false || kid === "") continue;
    e.append(kid instanceof Node ? kid : document.createTextNode(String(kid)));
  }
  return e;
}

async function getJSON(path) {
  const r = await fetch(path, { cache: "no-store", headers: { Accept: "application/json" } });
  let body = null;
  try { body = await r.json(); } catch (_) { /* non-JSON error page */ }
  if (!r.ok) throw new Error((body && body.error) || `${r.status} ${r.statusText} for ${path}`);
  return body;
}

const str = v => (v == null ? "" : String(v));
const plural = (n, word) => `${n} ${word}${n === 1 ? "" : "s"}`;

function statusBadge(check) {
  if (!check) return el("span", { class: "badge", text: "not checked" });
  const errors = check.errors ?? check.summary?.errors ?? 0;
  const warnings = check.warnings ?? check.summary?.warnings ?? 0;
  const cls = check.status === "pass" ? "ok" : check.status === "pass_with_warnings" ? "warning" : "error";
  const label = check.status === "unreadable" ? "workbook or filing unreadable"
    : check.status === "error" ? "checker could not run"
    : errors || warnings ? [errors ? plural(errors, "error") : "", warnings ? plural(warnings, "warning") : ""].filter(Boolean).join(" · ")
    : "checker pass";
  return el("span", { class: `badge ${cls}`, title: `checker status: ${check.status}` , text: label });
}

function sevClass(sev) { return sev === "error" ? "error" : sev === "warning" ? "warning" : "info"; }

// Render text with "#12" references (ledger rows) and "Q3" references
// (questions, only where opts.questions is true: "Q4" can also be a fiscal
// quarter) turned into in-page links. Only used on workbook text.
const REF_RE = /#(\d+)\b|\bQ(\d+)\b/g;
function linkedText(text, opts = {}) {
  const frag = document.createDocumentFragment();
  const s = str(text);
  let last = 0;
  if (view) {
    for (const m of s.matchAll(REF_RE)) {
      const isRow = m[1] != null;
      if (isRow && opts.rows === false) continue;
      if (!isRow && opts.questions !== true) continue;
      const key = isRow ? m[1] : `Q${m[2]}`;
      const exists = isRow ? view.rowByKey.has(key) : view.qByKey.has(key);
      if (!exists) continue;
      if (m.index > last) frag.append(s.slice(last, m.index));
      const a = el("a", { class: "ref", href: isRow ? `#row-${encodeURIComponent(key)}` : `#q-${encodeURIComponent(key)}`, text: m[0] });
      a.addEventListener("click", e => {
        e.preventDefault(); e.stopPropagation();
        if (isRow) { showTab("ledger"); selectRow(view.rowByKey.get(key), { scrollCard: true, scrollFiling: true, flash: true }); }
        else showQuestion(key);
      });
      frag.append(a);
      last = m.index + m[0].length;
    }
  }
  if (last < s.length) frag.append(s.slice(last));
  return frag;
}

/* ------------------------------------------------------------ routing */

function navigate(path) {
  if (location.pathname + location.hash !== path) history.pushState(null, "", path);
  route();
}

document.addEventListener("click", e => {
  const a = e.target.closest("a[data-nav]");
  if (!a || e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
  e.preventDefault();
  navigate(a.getAttribute("href"));
});
window.addEventListener("popstate", route);

function route() {
  const m = location.pathname.match(/^\/deal\/([a-z0-9][a-z0-9-]*)\/?$/);
  if (m) {
    if (view && view.slug === m[1]) { applyHash(); return; }
    openDeal(m[1]);
  } else {
    openIndex();
  }
}

/* ------------------------------------------------------------ deals list */

async function openIndex() {
  const token = ++routeToken;
  view = null;
  document.body.classList.remove("on-deal");
  document.title = "Ledger cockpit";
  crumbs.replaceChildren();
  renderReaderOnly();
  app.replaceChildren(el("p", { class: "loading", text: "Loading deals…" }));
  let deals;
  try { deals = await getJSON("/api/deals"); }
  catch (err) { if (token === routeToken) app.replaceChildren(el("p", { class: "error", text: `Could not load deals: ${err.message}` })); return; }
  if (token !== routeToken) return;

  const tbody = el("tbody");
  for (const d of deals) {
    const href = `/deal/${d.slug}`;
    const located = d.quotes_located ?? 0, total = d.quotes_total ?? 0;
    const tr = el("tr", { onclick: e => { if (!e.target.closest("a")) navigate(href); } },
      el("td", null, el("a", { class: "slug", href, "data-nav": true, text: d.slug }), el("span", { class: "target", text: str(d.target) }),
        d.error ? el("span", { class: "target short", text: str(d.error) }) : null),
      el("td", { class: "filed" }, str(d.form_type), el("span", { class: "target", text: str(d.date_filed) })),
      el("td", { class: "num", text: str(d.rows) }),
      el("td", { class: "num", text: str(d.rounds) }),
      el("td", { class: "num", text: str(d.questions) }),
      el("td", null, statusBadge(d.check)),
      el("td", { class: "num" }, el("span", { class: located < total ? "short" : "", text: `${located} / ${total}` })),
    );
    tbody.append(tr);
  }
  const table = el("table", { class: "deals" },
    el("thead", null, el("tr", null,
      el("th", { text: "Deal" }), el("th", { text: "Filing" }), el("th", { class: "num", text: "Ledger rows" }),
      el("th", { class: "num", text: "Rounds" }), el("th", { class: "num", text: "Questions" }),
      el("th", { text: "Checker" }), el("th", { class: "num", text: "Quotes located" }))),
    tbody);
  app.replaceChildren(el("div", { class: "index" }, el("div", { class: "inner" },
    el("h2", { text: "Deal ledgers" }),
    el("p", { class: "lead", text: `${plural(deals.length, "deal")}. Read-only: open a deal to read its ledger beside the filing.` }),
    deals.length ? table : el("p", { class: "dim", text: "No extracted workbooks with a filing were found." }))));
}

function renderReaderOnly() {
  bar.replaceChildren();
  if (lastReader) bar.append(el("span", { class: "reader", title: "reader (display only)", text: lastReader }));
}

/* ------------------------------------------------------------ deal page */

const LEDGER_HIDDEN = new Set(["#", "When", "Who", "Type", "Event", "Process", "Round", "Price low", "Price high",
  "Quote and page", "Sort date", "Date from", "Date to"]);
const LEDGER_FIELDS = ["All cash", "Formality", "Conditions", "Count", "Exit reason", "Inferred", "Note", "Flag", "Reviewer note"];
const LINKED_FIELDS = new Set(["Note", "Flag", "Reviewer note"]);

function rowKey(r) { const id = str(r.id).trim(); return id || `r${r.excel_row}`; }

async function openDeal(slug) {
  const token = ++routeToken;
  document.body.classList.add("on-deal");
  crumbs.replaceChildren(el("a", { class: "back", href: "/", "data-nav": true, text: "← deals" }), el("span", { class: "slug", text: slug }));
  bar.replaceChildren();
  app.replaceChildren(el("p", { class: "loading", text: `Loading ${slug}…` }));
  view = null;

  // Fetch the deal and (unless cached) the filing in parallel.
  const cached = filingCache.get(slug);
  const filingP = cached ? null
    : getJSON(`/api/filing/${slug}`).then(filing => ({ filing }), err => ({ err }));
  let deal;
  try { deal = await getJSON(`/api/deal/${slug}`); }
  catch (err) { if (token === routeToken) app.replaceChildren(el("p", { class: "error", text: `Could not load ${slug}: ${err.message}` })); return; }
  if (token !== routeToken) return;

  lastReader = str(deal.reader);
  const rows = deal.ledger?.rows || [];
  view = {
    slug, deal, rows, sel: -1,
    rowByKey: new Map(rows.map((r, i) => [rowKey(r), i])),
    qByKey: new Map((deal.questions?.rows || []).map(q => [str(q.id).trim(), q])),
    cards: [], qCards: new Map(), marks: new Map(), blockEls: [], filingReady: false, tab: "ledger",
  };
  document.title = `${slug} · Ledger cockpit`;
  const target = (deal.facts || []).find(f => f.field === "Target");
  if (target) crumbs.append(el("span", { class: "target", text: str(target.value) }));

  buildDealLayout();
  renderBar();
  applyHash({ initial: true });
  loadFiling(slug, token, cached, filingP);
}

function renderBar() {
  const v = view, n = v.rows.length;
  const prev = el("button", { title: "previous row (k / ↑)", text: "◀", onclick: () => step(-1) });
  const next = el("button", { title: "next row (j / ↓)", text: "▶", onclick: () => step(1) });
  prev.disabled = v.sel <= 0; next.disabled = v.sel >= n - 1;
  v.posEl = el("span", { class: "pos", text: positionText() });
  v.prevBtn = prev; v.nextBtn = next;
  bar.replaceChildren(v.posEl, statusBadge(v.deal.check),
    el("span", { class: "reader", title: "reader (display only)", text: v.deal.reader || "" }), prev, next);
}

function positionText() {
  const v = view, n = v.rows.length;
  return v.sel >= 0 ? `row ${v.sel + 1} of ${n}` : `row – of ${n} · j/k to step`;
}

function updateBarPosition() {
  const v = view, n = v.rows.length;
  v.posEl.textContent = positionText();
  v.prevBtn.disabled = v.sel <= 0; v.nextBtn.disabled = v.sel >= n - 1;
}

function buildDealLayout() {
  const v = view, d = v.deal;
  v.filingEl = el("section", { class: "filing", "aria-label": "filing" });
  v.filingNote = el("div", { class: "fnote" });
  v.docEl = el("div", { class: "doc" }, el("p", { class: "placeholder", text: "Loading filing…" }));
  v.filingEl.append(v.filingNote, v.docEl);
  fillFilingNote();

  const tabs = [
    ["ledger", "Ledger", v.rows.length],
    ["rounds", "Rounds", d.rounds?.rows?.length ?? 0],
    ["questions", "Questions", d.questions?.rows?.length ?? 0],
    ["facts", "Deal facts", d.facts?.length ?? 0],
    ["checker", "Checker", (d.check?.summary?.errors ?? 0) + (d.check?.summary?.warnings ?? 0) || ""],
  ];
  v.tabBtns = new Map(); v.panels = new Map();
  const tabBar = el("nav", { class: "tabs", role: "tablist" });
  const side = el("section", { class: "side", "aria-label": "ledger" }, tabBar);
  for (const [key, label, count] of tabs) {
    const b = el("button", { role: "tab", onclick: () => showTab(key) }, label, count !== "" ? el("span", { class: "n", text: String(count) }) : null);
    v.tabBtns.set(key, b); tabBar.append(b);
    const p = el("div", { class: "panel", role: "tabpanel", hidden: key !== "ledger" });
    v.panels.set(key, p); side.append(p);
  }
  renderLedgerPanel(v.panels.get("ledger"));
  renderRoundsPanel(v.panels.get("rounds"));
  renderQuestionsPanel(v.panels.get("questions"));
  renderFactsPanel(v.panels.get("facts"));
  renderCheckerPanel(v.panels.get("checker"));
  showTab("ledger");

  v.docEl.addEventListener("click", onFilingClick);
  app.replaceChildren(el("div", { class: "split" }, v.filingEl, side));
}

function fillFilingNote() {
  const v = view, f = v.deal.filing || {};
  const located = v.rows.filter(r => r.quote && r.quote.located).length;
  const withQuote = v.rows.filter(r => r.quote).length;
  const parts = [
    el("span", { text: [f.form_type, f.date_filed, f.file].filter(Boolean).join(" · ") }),
    el("span", { class: located < withQuote ? "warnnote" : "", text: `${located} of ${withQuote} quotes located` }),
  ];
  if (!v.deal.pages_reliable) parts.push(el("span", { class: "warnnote", text: "printed page numbers not reliably detected: page markers are approximate and page hints are off" }));
  if (v.deal.background_block != null) parts.push(el("a", { href: "#", text: "↳ Background", onclick: e => { e.preventDefault(); scrollToBackground(); } }));
  v.filingNote.replaceChildren(...parts);
}

function showTab(key) {
  const v = view; if (!v || !v.panels.has(key)) return;
  v.tab = key;
  for (const [k, b] of v.tabBtns) { b.classList.toggle("on", k === key); b.setAttribute("aria-selected", k === key ? "true" : "false"); }
  for (const [k, p] of v.panels) p.hidden = k !== key;
}

/* ---------- ledger cards */

function issueBadges(issues) {
  return (issues || []).map(i => el("span", {
    class: `badge ${sevClass(i.severity)}`,
    title: `${i.severity}${i.column ? ` · ${i.column}` : ""}: ${str(i.message)}`,
    text: i.code || i.severity,
  }));
}

function issueList(issues, hint) {
  const ul = el("ul", { class: "issues" });
  for (const i of issues || []) {
    ul.append(el("li", { class: sevClass(i.severity) },
      el("span", { class: "code", text: `${i.severity} ${i.code || ""}${i.column ? ` [${i.column}]` : ""}` }), str(i.message)));
  }
  if (hint) ul.append(el("li", { class: "hint" }, el("span", { class: "code", text: "page hint (cockpit, not checker)" }), str(hint).replace(/^page hint:\s*/i, "")));
  return ul;
}

function renderLedgerPanel(panel) {
  const v = view;
  if (!v.rows.length) { panel.append(el("p", { class: "dim", text: "The ledger has no rows." })); return; }
  const frag = document.createDocumentFragment();
  v.rows.forEach((r, i) => {
    const c = r.cells || {};
    const hint = v.deal.pages_reliable ? r.page_hint : null;
    const badges = el("span", { class: "badges" }, issueBadges(r.issues));
    if (hint) badges.append(el("span", { class: "badge hint", title: `Cockpit page hint (not a checker finding): ${hint}`, text: "page hint" }));
    if (r.quote && !r.quote.located) badges.append(el("span", { class: "badge bad", title: "the cockpit could not find this quote in the filing", text: "quote not found" }));

    const typeEvent = [c["Type"], c["Event"]].filter(x => str(x)).join(" · ");
    const pr = [str(c["Process"]) && `process ${c["Process"]}`, str(c["Round"]) && `round ${c["Round"]}`].filter(Boolean).join(" · ");
    const card = el("article", { class: "card", id: `row-${rowKey(r)}`, "data-i": i },
      el("div", { class: "top" },
        el("span", { class: "id", title: `Excel row ${r.excel_row}`, text: `#${str(r.id)}` }),
        str(c["When"]) ? el("span", { class: "when", text: c["When"] }) : null,
        str(c["Who"]) ? el("span", { class: "who", text: c["Who"] }) : null,
        badges),
      typeEvent || pr ? el("div", { class: "sub", text: [typeEvent, pr].filter(Boolean).join("   ·   ") }) : null);

    const dl = el("dl");
    const lo = str(c["Price low"]), hi = str(c["Price high"]);
    if (lo || hi) dl.append(el("dt", { text: "Price" }), el("dd", { text: lo && hi && lo !== hi ? `${lo} – ${hi}` : lo && hi ? lo : lo ? `${lo} (low)` : `${hi} (high)` }));
    const extra = (v.deal.ledger.columns || []).filter(col => !LEDGER_HIDDEN.has(col) && !LEDGER_FIELDS.includes(col));
    for (const col of [...LEDGER_FIELDS.filter(f => f !== "Flag" && f !== "Reviewer note"), ...extra]) {
      const val = str(c[col]); if (!val) continue;
      dl.append(el("dt", { text: col }), el("dd", { class: val.length > 180 ? "long" : "" }, LINKED_FIELDS.has(col) ? linkedText(val) : val));
    }
    const qp = str(c["Quote and page"]);
    if (qp) dl.append(el("dt", { text: "Quote" }), el("dd", { class: "quote" }, qp));
    for (const col of ["Flag", "Reviewer note"]) {
      const val = str(c[col]); if (!val) continue;
      dl.append(el("dt", { text: col }), el("dd", null, linkedText(val, { questions: true })));
    }
    if (dl.childElementCount) card.append(dl);
    if (r.quote && !r.quote.located) card.append(el("div", { class: "notfound", text: "Quote not found in the filing" }));
    else if (r.quote && r.quote.located) {
      if (r.quote.occurrences > 1) card.append(el("div", { class: "found", text: `occurs ${r.quote.occurrences} times in the filing; the one on the cited page (else the first) is highlighted` }));
    }
    const details = el("div", { class: "details", hidden: true });
    if ((r.issues && r.issues.length) || hint) details.append(issueList(r.issues, hint));
    card.append(details);
    card.addEventListener("click", e => { if (e.target.closest("a")) return; selectRow(i, { scrollFiling: true }); });
    v.cards.push({ card, details });
    frag.append(card);
  });
  panel.append(frag);
}

/* ---------- rounds, questions, facts, checker */

function renderRoundsPanel(panel) {
  const rounds = view.deal.rounds || { columns: [], rows: [] };
  if (!rounds.rows?.length) { panel.append(el("p", { class: "dim", text: "No rounds." })); return; }
  for (const r of rounds.rows) {
    const c = r.cells || {};
    const title = [str(c["Process"]) && `Process ${c["Process"]}`, str(c["Round"]) && `Round ${c["Round"]}`].filter(Boolean).join(" · ") || `Excel row ${r.excel_row}`;
    const dl = el("dl");
    for (const col of rounds.columns || []) {
      if (col === "Process" || col === "Round") continue;
      const val = str(c[col]); if (!val) continue;
      dl.append(el("dt", { text: col }), el("dd", null, linkedText(val)));
    }
    panel.append(el("article", { class: "card rd", title: `Excel row ${r.excel_row}` },
      el("div", { class: "top" }, el("span", { class: "id", text: title }), el("span", { class: "badges" }, issueBadges(r.issues))),
      dl, r.issues?.length ? issueList(r.issues) : null));
  }
}

function renderQuestionsPanel(panel) {
  const qs = view.deal.questions || { columns: [], rows: [] };
  if (!qs.rows?.length) { panel.append(el("p", { class: "dim", text: "No open questions." })); return; }
  for (const q of qs.rows) {
    const c = q.cells || {}, id = str(q.id).trim();
    const dl = el("dl");
    for (const col of qs.columns || []) {
      if (col === "Q" || col === "Question") continue;
      const val = str(c[col]); if (!val) continue;
      dl.append(el("dt", { text: col }), el("dd", null, linkedText(val)));
    }
    const card = el("article", { class: "card q", id: `q-${id}`, title: `Excel row ${q.excel_row}` },
      el("div", { class: "top" }, el("span", { class: "id", text: id || "?" }), el("span", { class: "badges" }, issueBadges(q.issues))),
      str(c["Question"]) ? el("div", { class: "question" }, linkedText(c["Question"])) : null,
      dl, q.issues?.length ? issueList(q.issues) : null);
    if (id) view.qCards.set(id, card);
    panel.append(card);
  }
}

function showQuestion(key) {
  const card = view.qCards.get(key); if (!card) return;
  showTab("questions");
  card.scrollIntoView({ block: "start" });
  flash(card);
}

function flash(node) { node.classList.remove("flash"); void node.offsetWidth; node.classList.add("flash"); }

function renderFactsPanel(panel) {
  const facts = view.deal.facts || [];
  if (!facts.length) { panel.append(el("p", { class: "dim", text: "No deal facts." })); return; }
  const tb = el("tbody");
  for (const f of facts) tb.append(el("tr", null, el("td", { text: str(f.field) }), el("td", null, linkedText(f.value))));
  panel.append(el("table", { class: "facts" }, tb));
}

function renderCheckerPanel(panel) {
  const v = view, ch = v.deal.check || {};
  const s = ch.summary || {};
  const box = el("div", { class: "checker" });
  box.append(el("div", { class: "summary" },
    el("div", null, statusBadge(ch), " ",
      el("span", { class: "dim", text: `${plural(s.errors ?? 0, "error")} · ${plural(s.warnings ?? 0, "warning")} · ${s.information ?? 0} information${ch.checker_version ? ` · checker ${ch.checker_version}` : ""}` })),
    ch.scope_note ? el("p", { text: ch.scope_note }) : null,
    el("p", { text: "Page hints on cards are the cockpit's own comparison of cited and found pages. They are not checker findings." })));

  const section = (title, items) => {
    box.append(el("h3", { text: title }));
    if (!items.length) { box.append(el("p", { class: "none", text: "None." })); return; }
    const ul = el("ul", { class: "issues" });
    for (const [loc, i] of items) ul.append(el("li", { class: sevClass(i.severity) }, loc,
      el("span", { class: "code", text: `${i.severity} ${i.code || ""}${i.column ? ` [${i.column}]` : ""}` }), str(i.message)));
    box.append(ul);
  };

  const ledgerItems = [];
  v.rows.forEach((r, idx) => (r.issues || []).forEach(i => {
    const a = el("a", { class: "loc ref", href: `#row-${encodeURIComponent(rowKey(r))}`, text: `#${str(r.id)}`,
      onclick: e => { e.preventDefault(); showTab("ledger"); selectRow(idx, { scrollCard: true, scrollFiling: true, flash: true }); } });
    ledgerItems.push([a, i]);
  }));
  const roundItems = [];
  for (const r of v.deal.rounds?.rows || []) for (const i of r.issues || []) {
    roundItems.push([el("span", { class: "loc", text: `P${str(r.cells?.["Process"])} R${str(r.cells?.["Round"])}` }), i]);
  }
  const qItems = [];
  for (const q of v.deal.questions?.rows || []) for (const i of q.issues || []) {
    const id = str(q.id).trim();
    qItems.push([el("a", { class: "loc ref", href: `#q-${id}`, text: id || `row ${q.excel_row}`, onclick: e => { e.preventDefault(); showQuestion(id); } }), i]);
  }
  const other = (ch.other_issues || []).map(i => [el("span", { class: "loc", text: [i.sheet, i.row ? `row ${i.row}` : ""].filter(Boolean).join(" ") }), i]);
  section("Ledger rows", ledgerItems);
  section("Rounds", roundItems);
  section("Questions", qItems);
  section("Deal facts and workbook", other);
  panel.append(box);
}

/* ---------- filing */

async function loadFiling(slug, token, cached, filingP) {
  const file = str(view.deal.filing?.file);
  let filing = cached && cached.file === file ? cached.filing : null;
  if (!filing) {
    const got = await (filingP || getJSON(`/api/filing/${slug}`).then(f => ({ filing: f }), err => ({ err })));
    if (got.err) { if (token === routeToken && view) view.docEl.replaceChildren(el("p", { class: "error", text: `Could not load the filing: ${got.err.message}` })); return; }
    filing = got.filing;
    filingCache.set(slug, { file, filing });
  }
  if (token !== routeToken || !view || view.slug !== slug) return;
  renderFiling(filing);
  view.filingReady = true;
  if (view.sel >= 0 && view.pendingScroll) scrollFilingToRow(view.sel);
  else scrollToBackground();
  view.pendingScroll = false;
}

// Build per-block highlight ranges from the rows' located quotes.
// Returns Map(blockIndex -> [[from, to, rowIndex, quoteStartsHere], ...]). End offsets are exclusive.
function quoteRanges(blocks) {
  const byBlock = new Map();
  view.rows.forEach((r, i) => {
    const q = r.quote;
    if (!q || !q.located || !q.start || !q.end) return;
    const b0 = q.start.block, b1 = q.end.block;
    if (!(b0 >= 0 && b1 >= b0 && b1 < blocks.length)) return;
    for (let b = b0; b <= b1; b++) {
      const len = str(blocks[b].text).length;
      const from = b === b0 ? Math.max(0, Math.min(len, q.start.offset)) : 0;
      const to = b === b1 ? Math.max(0, Math.min(len, q.end.offset)) : len;
      if (to <= from) continue;
      if (!byBlock.has(b)) byBlock.set(b, []);
      byBlock.get(b).push([from, to, i, b === b0]);
    }
  });
  return byBlock;
}

function renderFiling(filing) {
  const v = view, blocks = filing.blocks || [];
  const ranges = quoteRanges(blocks);
  const pageStarts = new Map((filing.pages || []).map(p => [p.block, p.page]));
  const frag = document.createDocumentFragment();
  const marks = new Map();
  v.blockEls = new Array(blocks.length);

  for (let b = 0; b < blocks.length; b++) {
    const blk = blocks[b];
    if (pageStarts.has(b)) {
      frag.append(el("div", { class: `pg${v.deal.pages_reliable ? "" : " unsure"}`, "data-page": pageStarts.get(b),
        text: `p. ${pageStarts.get(b)}${v.deal.pages_reliable ? "" : " ?"}` }));
    }
    const kind = blk.kind === "h" ? "h" : blk.kind === "row" ? "row" : "p";
    const text = str(blk.text);
    const rs = ranges.get(b);
    const extra = b === v.deal.background_block ? " bg" : rs ? "" : !VISIBLE_RE.test(text) ? " blank" : isFurniture(blk, text) ? " furniture" : "";
    const node = el(kind === "p" ? "p" : "div", { class: `blk ${kind}${extra}`, "data-b": b });
    if (!rs) node.textContent = text;
    else appendHighlighted(node, text, rs, marks);
    v.blockEls[b] = node;
    frag.append(node);
  }
  v.marks = marks;
  v.docEl.replaceChildren(frag);
  if (v.sel >= 0) setMarksSelected(v.sel, true);
}

// Characters that print something (zero-width spaces and table bars do not).
const VISIBLE_RE = /[^\s\u200b\u200c\u200d\u2060\ufeff|]/;
const TOC_LINK_RE = /^(?:back\s+to\s+)?table\s+of\s+contents$/i;

// Page furniture: the printed folio that page detection read, and the
// "Table of Contents" back-link at the top of each page. Shown dimmed; the
// text stays so quote offsets are unaffected.
function isFurniture(blk, text) {
  const t = text.replace(/[\s\u200b\u200c\u200d\u2060\ufeff]+/g, " ").trim();
  if (TOC_LINK_RE.test(t)) return true;
  if (blk.page == null || t.length > 16) return false;
  const core = t.replace(/^[\s\-\u2013\u2014]+|[\s\-\u2013\u2014]+$/g, "").replace(/^\(\s*([ivxlc]+)\s*\)$/i, "$1").replace(/\s+/g, "");
  return core === String(blk.page);
}

// Split text at every range boundary; each segment covered by one or more
// quotes becomes one <mark data-rows="i j">, so overlapping quotes never nest.
function appendHighlighted(node, text, rs, marks) {
  const cuts = new Set([0, text.length]);
  for (const [f, t] of rs) { cuts.add(f); cuts.add(t); }
  const pts = [...cuts].sort((a, b) => a - b);
  for (let k = 0; k < pts.length - 1; k++) {
    const a = pts[k], z = pts[k + 1];
    if (z <= a) continue;
    const seg = text.slice(a, z);
    const cover = rs.filter(([f, t]) => f <= a && t >= z).map(r => r[2]);
    if (!cover.length) { node.append(seg); continue; }
    const uniq = [...new Set(cover)].sort((x, y) => x - y);
    // Mark where a quote begins so adjacent quotes do not read as one band.
    const starts = rs.some(([f, , , first]) => first && f === a);
    const m = el("mark", { class: starts ? "qs" : null, "data-rows": uniq.join(" "), title: uniq.map(i => `#${str(view.rows[i].id)}`).join(", ") }, seg);
    for (const i of uniq) { if (!marks.has(i)) marks.set(i, []); marks.get(i).push(m); }
    node.append(m);
  }
}

function setMarksSelected(i, on) {
  for (const m of view.marks.get(i) || []) m.classList.toggle("sel", on);
}

function onFilingClick(e) {
  const m = e.target.closest("mark[data-rows]");
  if (!m || !view) return;
  const ids = m.getAttribute("data-rows").split(" ").map(Number).filter(Number.isInteger);
  if (!ids.length) return;
  // Overlapping quotes: clicking again cycles through the rows that share this passage.
  const at = ids.indexOf(view.sel);
  const next = at >= 0 ? ids[(at + 1) % ids.length] : ids[0];
  showTab("ledger");
  selectRow(next, { scrollCard: true });
}

function scrollToBackground() {
  const v = view; if (!v || !v.blockEls.length) return;
  const b = v.deal.background_block;
  const node = b != null ? v.blockEls[b] : null;
  if (node) v.filingEl.scrollTop = Math.max(0, node.offsetTop - 44);
}

function scrollFilingToRow(i) {
  const v = view;
  const ms = v.marks.get(i);
  if (ms && ms.length) {
    const first = ms[0];
    // Centre the start of the quote in the filing pane without moving the page.
    const paneRect = v.filingEl.getBoundingClientRect(), mRect = first.getBoundingClientRect();
    const delta = mRect.top - paneRect.top - Math.max(60, v.filingEl.clientHeight * 0.3);
    v.filingEl.scrollTop += delta;
  }
}

/* ---------- selection */

function selectRow(i, opts = {}) {
  const v = view;
  if (!v || i == null || i < 0 || i >= v.rows.length) return;
  if (v.sel >= 0 && v.sel !== i) {
    const old = v.cards[v.sel]; old.card.classList.remove("sel"); old.details.hidden = true;
    setMarksSelected(v.sel, false);
  }
  v.sel = i;
  const cur = v.cards[i];
  cur.card.classList.add("sel");
  cur.details.hidden = !cur.details.childElementCount;
  setMarksSelected(i, true);
  updateBarPosition();
  const hash = `#row-${encodeURIComponent(rowKey(v.rows[i]))}`;
  if (location.hash !== hash) history.replaceState(null, "", `/deal/${v.slug}${hash}`);
  if (opts.scrollCard) cur.card.scrollIntoView({ block: "nearest" });
  if (opts.flash) flash(cur.card);
  if (opts.scrollFiling) {
    if (v.filingReady) scrollFilingToRow(i); else v.pendingScroll = true;
  }
}

function step(d) {
  const v = view; if (!v || !v.rows.length) return;
  const i = v.sel < 0 ? (d > 0 ? 0 : v.rows.length - 1) : Math.max(0, Math.min(v.rows.length - 1, v.sel + d));
  showTab("ledger");
  selectRow(i, { scrollCard: true, scrollFiling: true });
}

function applyHash(opts = {}) {
  const v = view; if (!v) return;
  const m = location.hash.match(/^#row-(.+)$/);
  if (m) {
    let key; try { key = decodeURIComponent(m[1]); } catch (_) { key = m[1]; }
    if (v.rowByKey.has(key)) { showTab("ledger"); selectRow(v.rowByKey.get(key), { scrollCard: true, scrollFiling: true }); return; }
  }
  const q = location.hash.match(/^#q-(.+)$/);
  if (q) { let key; try { key = decodeURIComponent(q[1]); } catch (_) { key = q[1]; } showQuestion(key); return; }
  if (!opts.initial && v.filingReady) scrollToBackground();
}

/* ------------------------------------------------------------ keyboard */

document.addEventListener("keydown", e => {
  if (e.metaKey || e.ctrlKey || e.altKey) return;
  const t = e.target;
  if (t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName))) return;
  if (e.key === "Escape" && document.body.classList.contains("on-deal")) { e.preventDefault(); navigate("/"); return; }
  if (!view) return;
  if (e.key === "j" || e.key === "ArrowDown") { e.preventDefault(); step(1); }
  else if (e.key === "k" || e.key === "ArrowUp") { e.preventDefault(); step(-1); }
});

route();
