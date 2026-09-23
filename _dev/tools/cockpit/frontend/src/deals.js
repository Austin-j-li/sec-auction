// Add deal and hide deal helpers: pure functions shared by the pages and their tests.

import { dayLabel, displayName } from './trace';

export const SLUG_PATTERN = /^[a-z0-9][a-z0-9-]*$/;
export const validSlug = value => SLUG_PATTERN.test(value || '') && value.length <= 60;
export const validName = value => Boolean((value || '').trim()) && value.trim().length <= 120;
export const LOOKUP_ACTIVE = new Set(['queued', 'running']);

// "412 KB", "1.6 MB".
export function formatBytes(bytes) {
  if (!Number.isFinite(bytes) || bytes < 0) return '';
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${Math.round(bytes / 1024)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

// A seed row's status in words: '' when it is ready, else the reason it needs review.
export function seedReview(status) {
  const value = (status || '').trim();
  return !value || value === 'ok' ? '' : value.replace(/^review:\s*/, '');
}

// What choosing a seed row does: open it, look its filing up, or ask for a pasted link.
export function seedAction(row) {
  if (row?.in_cockpit) return 'open';
  return row?.index_url ? 'lookup' : 'paste';
}

// The deal list leaves hidden deals out unless asked; `visible` counts the rest.
export function listedDeals(deals, showHidden = false) {
  const all = deals || [];
  const hiddenCount = all.filter(item => item.hidden).length;
  return { rows: showHidden ? all : all.filter(item => !item.hidden), hiddenCount, visible: all.length - hiddenCount };
}

// "Hidden by Alex on 23 Sep".
export function hiddenLine(item) {
  if (!item?.hidden) return '';
  const when = new Date(item.hidden_at || NaN);
  return `Hidden by ${displayName(item.hidden_by)}${Number.isNaN(when.getTime()) ? '' : ` on ${dayLabel(when)}`}`;
}
