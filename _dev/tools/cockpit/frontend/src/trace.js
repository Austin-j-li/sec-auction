import { count, text } from './api';

// Pure helpers for attribution, comments and "since your last visit" (phase 1, trace).

const NAMES = { austin: 'Austin', alex: 'Alex', local: 'Local' };
const INITIALS = { austin: 'AL', alex: 'AG', local: 'LO' };
export const SESSION_GAP_MS = 30 * 60 * 1000;
export const EDIT_KINDS = new Set(['revision', 'restore']);
export const COMMENT_KINDS = new Set(['comment', 'reply']);
export const THREAD_KINDS = new Set(['comment', 'reply', 'resolve', 'reopen', 'comment_edit', 'comment_delete']);
export const KIND_LABELS = { revision: 'Revision', restore: 'Restore', comment: 'Comment', reply: 'Reply', resolve: 'Resolved', reopen: 'Reopened', comment_edit: 'Comment edited', comment_delete: 'Comment deleted' };

export function displayName(actor) {
  const key = text(actor);
  return NAMES[key] || (key ? key[0].toUpperCase() + key.slice(1) : 'Someone');
}
export function initials(actor) { return INITIALS[text(actor)] || text(actor).slice(0, 2).toUpperCase(); }
// Only a signed-in person (or the loopback actor) has a read marker and write access to comments.
export const knownUser = user => Boolean(user) && user !== 'unknown';

const time = value => { const t = Date.parse(value); return Number.isNaN(t) ? 0 : t; };
const pad = n => String(n).padStart(2, '0');
const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
const dayLabel = d => `${d.getDate()} ${MONTHS[d.getMonth()]}`;
export function shortTime(value) {
  const d = new Date(value);
  return Number.isNaN(d.getTime()) ? text(value) : `${dayLabel(d)} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
}
export function timeRange(start, end) {
  const a = new Date(start), b = new Date(end);
  if (Number.isNaN(a.getTime()) || Number.isNaN(b.getTime())) return shortTime(start);
  if (b - a < 60000) return shortTime(start);
  return dayLabel(a) === dayLabel(b) ? `${shortTime(start)}–${pad(b.getHours())}:${pad(b.getMinutes())}` : `${shortTime(start)}–${shortTime(end)}`;
}

// Group activity by actor and session: a gap of more than 30 minutes in one actor's activity starts a new session.
// Returns groups newest first; each group's items are newest first.
export function groupSessions(items, gap = SESSION_GAP_MS) {
  const ordered = [...(items || [])].sort((a, b) => time(a.at) - time(b.at) || (a.id ?? 0) - (b.id ?? 0));
  const open = new Map(), groups = [];
  for (const item of ordered) {
    let group = open.get(item.actor);
    if (!group || time(item.at) - time(group.end) > gap) {
      group = { actor: item.actor, start: item.at, end: item.at, items: [] };
      open.set(item.actor, group); groups.push(group);
    }
    group.end = item.at; group.items.unshift(item);
  }
  return groups.sort((a, b) => time(b.end) - time(a.end));
}

export function tally(items) {
  const edits = items.filter(item => EDIT_KINDS.has(item.kind)).length;
  const comments = items.filter(item => COMMENT_KINDS.has(item.kind)).length;
  return { edits, comments, other: items.length - edits - comments };
}
export function tallyText({ edits = 0, comments = 0, other = 0 }) {
  return [edits && count(edits, 'edit'), comments && count(comments, 'comment'), other && `${other} other`].filter(Boolean).join(', ');
}

// The other actor who changed any field of this row in a revision after the reader's last visit, or null.
export function changedByOther(authors, user, seenRevision) {
  if (!knownUser(user) || !authors) return null;
  const since = seenRevision ?? 0;
  let latest = null;
  for (const author of Object.values(authors)) {
    if (author?.actor && author.actor !== user && (author.revision ?? 0) > since && (!latest || author.revision > latest.revision)) latest = author;
  }
  return latest?.actor || null;
}

export const threadKey = target => target?.kind === 'deal' ? 'deal' : text(target?.uid);
export function countThreads(threads) {
  const counts = {};
  for (const thread of threads || []) {
    const key = threadKey(thread.target);
    counts[key] ||= { open: 0, resolved: 0 };
    counts[key][thread.resolved ? 'resolved' : 'open']++;
  }
  return counts;
}
export function threadsFor(threads, target) {
  return (threads || []).filter(thread => {
    const t = thread.target || {};
    if (target.kind === 'deal') return t.kind === 'deal' || (t.kind === 'row' && thread.target_missing);
    return t.kind === target.kind && t.uid === target.uid && (target.kind !== 'row' || !thread.target_missing);
  });
}
