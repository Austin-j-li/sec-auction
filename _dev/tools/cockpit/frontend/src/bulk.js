import { rowId, text } from './api';

// Process and Round set on many ledger events at once, as when a deal's rounds are renumbered. The selected events
// become one staged `bulk_update` operation (one of the server's 100 a save, however many rows), saved with the
// other staged edits as one revision. The server takes only these two columns, with the values the checker accepts:
// a Process of 1 or more, and a Round of 0 or more or `post`.

// The values to set from the dialog's two boxes; a blank box leaves that column as it is on each event.
export function bulkValues(process, round) {
  const values = {}, p = text(process).trim(), r = text(round).trim().toLowerCase();
  if (p) {
    if (!/^\d{1,9}$/.test(p) || Number(p) < 1) return { values: {}, error: 'Process must be a whole number of 1 or more.' };
    values.Process = String(Number(p));
  }
  if (r) {
    if (r !== 'post' && !/^\d{1,9}$/.test(r)) return { values: {}, error: 'Round must be a whole number of 0 or more, or post.' };
    values.Round = r === 'post' ? r : String(Number(r));
  }
  return { values, error: Object.keys(values).length ? '' : 'Enter a Process, a Round, or both.' };
}

// The selected events, in ledger order, that the values would change.
export function bulkChanges(rows, picked, values) {
  return rows.filter(row => picked.has(row.uid) && Object.entries(values).some(([field, value]) => text(row.cells?.[field]) !== value));
}

// "#2–#4, #7, 1 new event": the events named in the confirmation.
export function eventList(rows) {
  const numbers = rows.filter(row => !row.uid.startsWith('new-')).map(row => Number(rowId(row))).filter(Number.isInteger).sort((a, b) => a - b);
  const parts = [];
  for (const n of numbers) {
    const last = parts.at(-1);
    if (last && n === last[1] + 1) last[1] = n; else parts.push([n, n]);
  }
  const fresh = rows.length - numbers.length;
  return [...parts.map(([a, b]) => a === b ? `#${a}` : `#${a}–#${b}`), fresh && `${fresh} new event${fresh === 1 ? '' : 's'}`].filter(Boolean).join(', ');
}

// A click on an event in select mode toggles it; a shift-click adds every event from the last one clicked.
export function pickRows(order, picked, anchor, uid, extend = false) {
  const next = new Set(picked), from = order.indexOf(anchor), to = order.indexOf(uid);
  if (extend && from >= 0 && to >= 0) order.slice(Math.min(from, to), Math.max(from, to) + 1).forEach(item => next.add(item));
  else if (next.has(uid)) next.delete(uid);
  else next.add(uid);
  return next;
}

// Stage the values on the given events: an unsaved new event takes them in its insert, the rest in one bulk_update.
export function stageBulk(ops, uids, values) {
  const next = structuredClone(ops), stable = [];
  for (const uid of uids) {
    const insert = next.find(op => op.type === 'insert' && op.client_uid === uid);
    if (insert) Object.assign(insert.values, values); else stable.push(uid);
  }
  if (stable.length) next.push({ type: 'bulk_update', sheet: 'Deal ledger', uids: stable, values: { ...values } });
  return next;
}

// The staged update that a field edit extends: the record's last update, unless a bulk_update staged after it covers
// the record. The server applies operations in order, so the edit must then follow the bulk one as a new update.
export function updateToExtend(ops, sheet, uid) {
  for (let i = ops.length - 1; i >= 0; i--) {
    const op = ops[i];
    if (op.type === 'bulk_update' && op.sheet === sheet && op.uids.includes(uid)) return null;
    if (op.type === 'update' && op.sheet === sheet && op.uid === uid) return op;
  }
  return null;
}

// A staged deletion takes its event out of any staged bulk_update, dropping one left with no events.
export function withoutBulkRow(ops, uid) {
  return ops.map(op => op.type === 'bulk_update' ? { ...op, uids: op.uids.filter(item => item !== uid) } : op)
    .filter(op => op.type !== 'bulk_update' || op.uids.length);
}

// Staged edits as the reader counts them: a bulk_update counts once per event it changes.
export const stagedCount = ops => ops.reduce((sum, op) => sum + (op.type === 'bulk_update' ? op.uids.length : 1), 0);

// The default save reason for a bulk edit: "Set Process 2 and Round 1 on 12 events".
export function bulkReason(values, events) {
  const parts = Object.entries(values).map(([field, value]) => `${field} ${value}`).join(' and ');
  return `Set ${parts} on ${events} event${events === 1 ? '' : 's'}`;
}
