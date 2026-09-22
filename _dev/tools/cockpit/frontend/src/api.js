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

export function saveDeal(slug, session, payload) {
  return json(`/api/deal/${encodeURIComponent(slug)}/edit`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-Cockpit-CSRF': session.csrf_token },
    body: JSON.stringify(payload),
  });
}

export const text = value => value == null ? '' : String(value);
export const rowId = row => text(row?.id || row?.cells?.['#'] || row?.cells?.Q || row?.excel_row);
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
