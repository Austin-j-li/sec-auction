import { text } from './api';
import { displayName, shortTime } from './trace';

// Pure helpers for instruction versions (phase 4): ordering, labels, validation and a line diff.

export const REMINDER = 'A change should be general — the objective, the work process, honesty about uncertainty, a repaired contradiction or a deletion — never a rule justified by one reviewed deal (AGENTS.md).';
export const NAME_MAX = 40;
export const NOTE_MAX = 2000;
export const TEXT_MAX_BYTES = 400 * 1024;
const NAME_RE = /^[\p{L}\p{N}._ -]+$/u;

export const sha7 = sha => text(sha).slice(0, 7);
export const isDraft = item => item?.status === 'draft';
export const textBytes = value => new TextEncoder().encode(text(value)).length;

// Published versions first, then drafts, each keeping the server's (newest first) order.
export function orderInstructions(items) {
  const list = items || [];
  return [...list.filter(item => !isDraft(item)), ...list.filter(isDraft)];
}
export function defaultInstructionId(payload) {
  return payload?.default_id || (payload?.items || []).find(item => item.is_default)?.id || null;
}
// "v1.13.2 · default", "draft 3f2a9c1 (Alex)"; a draft whose label does not say so is marked.
export function instructionOptionLabel(item) {
  const label = text(item?.label || item?.name || item?.id);
  const draft = isDraft(item) && !/^draft\b/i.test(label) ? ' · draft' : '';
  return `${label}${draft}${item?.is_default ? ' · default' : ''}`;
}
// "Published by Austin · 23 Sep 14:05" or "Draft by Alex · saved 23 Sep 14:05".
export function instructionByline(item) {
  if (!item) return '';
  if (isDraft(item)) {
    const saved = item.updated_at ? ` · saved ${shortTime(item.updated_at)}` : '';
    const by = item.updated_by && item.updated_by !== item.created_by ? ` by ${displayName(item.updated_by)}` : '';
    return `Draft by ${displayName(item.created_by)}${saved}${saved ? by : ''}`;
  }
  const who = item.published_by || item.created_by, when = item.published_at || item.created_at;
  return `Published by ${displayName(who)}${when ? ` · ${shortTime(when)}` : ''}`;
}

// A publish name: 1–40 letters, digits, ".", "-", "_" or spaces, not used by another published version.
export function nameProblem(name, items = []) {
  const value = text(name).trim();
  if (!value) return 'Give the version a name.';
  if (value.length > NAME_MAX) return `At most ${NAME_MAX} characters.`;
  if (!NAME_RE.test(value)) return 'Use letters, digits, “.”, “-”, “_” and spaces only.';
  if (items.some(item => item.name && item.name.toLowerCase() === value.toLowerCase())) return 'Another version already has this name.';
  return '';
}
export function noteProblem(note) {
  const value = text(note).trim();
  if (!value) return 'Say what changed and why.';
  if (value.length > NOTE_MAX) return `At most ${NOTE_MAX} characters.`;
  return '';
}

// ── Line diff ─────────────────────────────────────────────────────────
// Myers' O((N+M)·D) algorithm after trimming the common head and tail. When the lines differ in more
// than maxEdits places, the untrimmed middle is shown as one replaced block (exact: false).

const splitLines = value => text(value).split('\n');

function myers(a, b, a0, a1, b0, b1, maxEdits) {
  const n = a1 - a0, m = b1 - b0, limit = Math.min(n + m, maxEdits), offset = limit + 1;
  const v = new Int32Array(2 * limit + 3);
  const trace = [];
  let found = -1;
  for (let d = 0; d <= limit && found < 0; d++) {
    for (let k = -d; k <= d; k += 2) {
      let x = k === -d || (k !== d && v[offset + k - 1] < v[offset + k + 1]) ? v[offset + k + 1] : v[offset + k - 1] + 1;
      let y = x - k;
      while (x < n && y < m && a[a0 + x] === b[b0 + y]) { x++; y++; }
      v[offset + k] = x;
      if (x >= n && y >= m) { found = d; break; }
    }
    trace.push(v.slice(offset - d, offset + d + 1)); // trace[d][k + d] = furthest x on diagonal k after d edits
  }
  if (found < 0) return null;
  const out = [];
  let x = n, y = m;
  for (let d = found; d > 0; d--) {
    const prev = trace[d - 1], at = k => prev[k + d - 1];
    const k = x - y;
    const prevK = k === -d || (k !== d && at(k - 1) < at(k + 1)) ? k + 1 : k - 1;
    const prevX = at(prevK), prevY = prevX - prevK;
    while (x > prevX && y > prevY) { x--; y--; out.push({ type: 'same', a: a0 + x, b: b0 + y }); }
    if (prevK === k + 1) out.push({ type: 'add', b: b0 + prevY });
    else out.push({ type: 'del', a: a0 + prevX });
    x = prevX; y = prevY;
  }
  while (x > 0 && y > 0) { x--; y--; out.push({ type: 'same', a: a0 + x, b: b0 + y }); }
  return out.reverse();
}

// Returns {ops, exact, added, removed}. Each op is {type: 'same' | 'del' | 'add', a?, b?, text} with 0-based line indexes.
export function lineDiff(before, after, { maxEdits = 2000 } = {}) {
  const a = splitLines(before), b = splitLines(after);
  let head = 0;
  while (head < a.length && head < b.length && a[head] === b[head]) head++;
  let endA = a.length, endB = b.length;
  while (endA > head && endB > head && a[endA - 1] === b[endB - 1]) { endA--; endB--; }
  let middle = myers(a, b, head, endA, head, endB, maxEdits);
  const exact = Boolean(middle);
  if (!middle) {
    middle = [];
    for (let i = head; i < endA; i++) middle.push({ type: 'del', a: i });
    for (let j = head; j < endB; j++) middle.push({ type: 'add', b: j });
  }
  const ops = [];
  for (let i = 0; i < head; i++) ops.push({ type: 'same', a: i, b: i });
  ops.push(...middle);
  for (let i = endA, j = endB; i < a.length; i++, j++) ops.push({ type: 'same', a: i, b: j });
  let added = 0, removed = 0;
  for (const op of ops) {
    op.text = op.type === 'add' ? b[op.b] : a[op.a];
    if (op.type === 'add') added++;
    if (op.type === 'del') removed++;
  }
  return { ops, exact, added, removed };
}

// Side-by-side rows: a run of removed and added lines is paired row by row.
// Row: {kind: 'same' | 'change' | 'del' | 'add', left: {n, text} | null, right: {n, text} | null}; n is 1-based.
export function sideBySide(ops) {
  const rows = [];
  let dels = [], adds = [];
  const flush = () => {
    for (let i = 0; i < Math.max(dels.length, adds.length); i++) {
      const left = dels[i] ? { n: dels[i].a + 1, text: dels[i].text } : null;
      const right = adds[i] ? { n: adds[i].b + 1, text: adds[i].text } : null;
      rows.push({ kind: left && right ? 'change' : left ? 'del' : 'add', left, right });
    }
    dels = []; adds = [];
  };
  for (const op of ops || []) {
    if (op.type === 'del') dels.push(op);
    else if (op.type === 'add') adds.push(op);
    else { flush(); rows.push({ kind: 'same', left: { n: op.a + 1, text: op.text }, right: { n: op.b + 1, text: op.text } }); }
  }
  flush();
  return rows;
}

// Folds unchanged stretches longer than 2·context+1 rows into {kind: 'gap', count}, keeping context rows around changes.
export function foldRows(rows, context = 2) {
  const out = [];
  let i = 0;
  while (i < rows.length) {
    if (rows[i].kind !== 'same') { out.push(rows[i++]); continue; }
    let j = i;
    while (j < rows.length && rows[j].kind === 'same') j++;
    const keepHead = i === 0 ? 0 : context, keepTail = j === rows.length ? 0 : context;
    if (j - i > keepHead + keepTail + 1) {
      out.push(...rows.slice(i, i + keepHead), { kind: 'gap', count: j - i - keepHead - keepTail }, ...rows.slice(j - keepTail, j));
    } else out.push(...rows.slice(i, j));
    i = j;
  }
  return out;
}

// The differing middle of two changed lines, for highlighting: {left: [head, middle, tail], right: [...]}.
export function inlineChange(before, after) {
  const a = text(before), b = text(after);
  let head = 0;
  while (head < a.length && head < b.length && a[head] === b[head]) head++;
  let tail = 0;
  while (tail < a.length - head && tail < b.length - head && a[a.length - 1 - tail] === b[b.length - 1 - tail]) tail++;
  const cut = value => [value.slice(0, head), value.slice(head, value.length - tail), value.slice(value.length - tail)];
  return { left: cut(a), right: cut(b) };
}
