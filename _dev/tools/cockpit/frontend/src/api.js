export async function json(path, options = {}) {
  const response = await fetch(path, { cache: 'no-store', headers: { Accept: 'application/json', ...options.headers }, ...options });
  let body;
  try { body = await response.json(); } catch { body = null; }
  if (!response.ok) {
    const error = new Error(body?.error || `${response.status} ${response.statusText}`);
    error.status = response.status;
    throw error;
  }
  return body;
}

const writeHeaders = session => ({ 'Content-Type': 'application/json', 'X-Cockpit-CSRF': session.csrf_token });
const send = (path, session, payload) => json(path, { method: 'POST', headers: writeHeaders(session), body: JSON.stringify(payload) });
// A server restart issues a new write token, so an open tab's first write is refused. The refused request changed
// nothing: fetch the session once more and, for the same user, retry once with the new token (kept on the shared session).
// The fresh token is compared with the one this request sent, not the session's current one, so every write refused
// with the old token is retried, also when another write refused at the same time has already updated the session.
async function post(path, session, payload) {
  const sent = session.csrf_token;
  try { return await send(path, session, payload); }
  catch (error) {
    if (error.status !== 403 || error.message !== 'write authorization failed') throw error;
    const fresh = await json('/api/session').catch(() => null);
    if (!fresh?.csrf_token || fresh.user !== session.user || fresh.csrf_token === sent) throw error;
    session.csrf_token = fresh.csrf_token;
    return send(path, session, payload);
  }
}
const dealPath = (slug, rest) => `/api/deal/${encodeURIComponent(slug)}/${rest}`;

export function saveDeal(slug, session, payload) { return post(dealPath(slug, 'edit'), session, payload); }
// One comment action (create, reply, edit, delete, resolve, reopen); the response is the deal's full thread list.
export function commentAction(slug, session, action) { return post(dealPath(slug, 'comments'), session, action); }
// The working copy's review status, set at the revision being viewed: {status, revision} -> {deal_review}.
export function setDealReview(slug, session, status, revision) { return post(dealPath(slug, 'review'), session, { status, revision }); }
export function markSeen(slug, session, activityId) { return post(dealPath(slug, 'seen'), session, { activity_id: activityId }); }
// Leaving a deal: the request must survive navigation and page unload. Resolves (never rejects) when it lands.
export function markSeenOnLeave(slug, session, activityId) {
  try { return fetch(dealPath(slug, 'seen'), { method: 'POST', keepalive: true, headers: writeHeaders(session), body: JSON.stringify({ activity_id: activityId }) }).catch(() => {}); }
  catch { return Promise.resolve(); }
}
// Phase 2. Claude account: {action: connect | code | cancel | token | disconnect, ...}; the response is GET /api/account.
export function accountAction(session, action) { return post('/api/account/claude', session, action); }
// Extraction jobs: {action: 'extract', engine, effort, timeout_minutes, instruction_id} or {action: 'cancel', job_id}; the response is the jobs list.
export function jobAction(slug, session, action) { return post(dealPath(slug, 'jobs'), session, action); }
// Imported versions: {action: 'hide' | 'unhide', version_id}.
export function versionAction(slug, session, action) { return post(dealPath(slug, 'versions'), session, action); }
// Phase 3. Add a deal: {action: 'lookup', url, seed_deal?} -> {lookup}; {action: 'add', lookup_id, document, slug, name} -> {slug}.
export function dealsAction(session, action) { return post('/api/deals', session, action); }
// Phase 5. Hide a deal for both users: {action: 'hide' | 'unhide'} -> {slug, hidden, hidden_by, hidden_at}.
export function dealVisibility(slug, session, action) { return post(`/api/deals/${encodeURIComponent(slug)}/visibility`, session, { action }); }
// Phase 4. ChatGPT account: {action: connect | cancel (job_id) | disconnect}; the response is GET /api/account.
export function chatgptAction(session, action) { return post('/api/account/chatgpt', session, action); }
// Instruction versions: {action: 'draft', from} | {action: 'save', id, text, base_sha256} | {action: 'publish', id, name, note}
// return the detail payload; {action: 'default', id} returns the list payload.
export function instructionsAction(session, action) { return post('/api/instructions', session, action); }
export function instructionPath(id, seq = null) { return `/api/instructions/${encodeURIComponent(id)}${seq != null ? `?seq=${encodeURIComponent(seq)}` : ''}`; }
export function compareQuery(slug, from, to) { return `${dealPath(slug, 'compare')}?${new URLSearchParams({ from, to })}`; }
export function activityQuery({ actor = '', slug = '', kind = '', before = '', limit = 100 } = {}) {
  const params = new URLSearchParams(Object.entries({ actor, slug, kind, before, limit }).filter(([, value]) => value !== '' && value != null));
  return `/api/activity?${params}`;
}

export const text = value => value == null ? '' : String(value);
export const rowId = row => text(row?.id || row?.cells?.['#'] || row?.cells?.Q || row?.excel_row);
// The id for a new Questions row: the first free R number when it copies a review item (R1, R2, …),
// otherwise the first free Q number.
export function nextQuestionId(rows, copied = null) {
  const prefix = /^R\d+$/i.test(text(copied?.cells?.Q).trim()) ? 'R' : 'Q';
  const used = new Set(rows.map(item => text(item.cells?.Q).trim().toUpperCase()));
  let number = 1;
  while (used.has(`${prefix}${number}`)) number++;
  return `${prefix}${number}`;
}
export const count = (n, singular) => `${n} ${singular}${n === 1 ? '' : 's'}`;
export const sheetRows = (deal, sheet) => sheet === 'Deal facts' ? deal.facts || [] : ({ 'Deal ledger': deal.ledger, Rounds: deal.rounds, Questions: deal.questions }[sheet]?.rows || []);
export const sheetColumns = (deal, sheet) => sheet === 'Deal facts' ? ['Field', 'Value'] : ({ 'Deal ledger': deal.ledger, Rounds: deal.rounds, Questions: deal.questions }[sheet]?.columns || []);
export const recordValues = (row, sheet) => sheet === 'Deal facts' ? { Field: text(row.field), Value: text(row.value) } : { ...row.cells };

export function filingRanges(rows, blocks) {
  const ranges = new Map();
  rows.forEach((row, rowIndex) => {
    const quote = row.quote;
    if (!quote?.located || !quote.start || !quote.end) return;
    const begin = quote.start.block, end = quote.end.block;
    if (!Number.isInteger(begin) || !Number.isInteger(end) || begin < 0 || end >= blocks.length || begin > end) return;
    for (let block = begin; block <= end; block++) {
      const length = text(blocks[block]?.text).length;
      const from = block === begin ? Math.max(0, Math.min(length, quote.start.offset)) : 0;
      const to = block === end ? Math.max(0, Math.min(length, quote.end.offset)) : length;
      if (to <= from) continue;
      if (!ranges.has(block)) ranges.set(block, []);
      ranges.get(block).push({ from, to, rowIndex });
    }
  });
  return ranges;
}

export function segments(value, quoteRanges = [], search = '', allowedMatches = null) {
  const valueText = text(value);
  const cuts = new Set([0, valueText.length]);
  const matches = [];
  if (allowedMatches) matches.push(...allowedMatches);
  else if (search) {
    const haystack = valueText.toLocaleLowerCase(), needle = search.toLocaleLowerCase();
    let cursor = 0;
    while (cursor < valueText.length && matches.length < 1000) {
      const at = haystack.indexOf(needle, cursor);
      if (at < 0) break;
      matches.push({ from: at, to: at + search.length });
      cursor = at + Math.max(1, search.length);
    }
  }
  for (const range of [...quoteRanges, ...matches]) { cuts.add(range.from); cuts.add(range.to); }
  const points = [...cuts].sort((a, b) => a - b);
  return points.slice(0, -1).map((from, i) => {
    const to = points[i + 1];
    return { from, to, text: valueText.slice(from, to), rows: [...new Set(quoteRanges.filter(r => r.from <= from && r.to >= to).map(r => r.rowIndex))], search: matches.some(r => r.from <= from && r.to >= to) };
  }).filter(part => part.text);
}
