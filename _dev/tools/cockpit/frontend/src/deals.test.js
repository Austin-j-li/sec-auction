import { describe, expect, it } from 'vitest';
import { formatBytes, hiddenLine, listedDeals, seedAction, seedReview, validName, validSlug } from './deals';

describe('add deal helpers', () => {
  it('validates short names and deal names', () => {
    expect(validSlug('beta-holdings')).toBe(true);
    expect(validSlug('Beta')).toBe(false);
    expect(validSlug('-beta')).toBe(false);
    expect(validSlug('a'.repeat(61))).toBe(false);
    expect(validName('  ')).toBe(false);
    expect(validName('Beta Holdings')).toBe(true);
  });
  it('formats sizes and seed states', () => {
    expect(formatBytes(900)).toBe('900 B');
    expect(formatBytes(420000)).toBe('410 KB');
    expect(formatBytes(1641964)).toBe('1.6 MB');
    expect(seedReview('ok')).toBe('');
    expect(seedReview('review: 2 target names')).toBe('2 target names');
    expect(seedAction({ in_cockpit: true, index_url: 'x' })).toBe('open');
    expect(seedAction({ index_url: 'https://www.sec.gov/x-index.htm' })).toBe('lookup');
    expect(seedAction({ index_url: '' })).toBe('paste');
  });
  it('leaves hidden deals out of the list unless asked', () => {
    const deals = [{ slug: 'a' }, { slug: 'b', hidden: true }, { slug: 'c', hidden: false }];
    expect(listedDeals(deals)).toEqual({ rows: [deals[0], deals[2]], hiddenCount: 1, visible: 2 });
    expect(listedDeals(deals, true).rows.map(item => item.slug)).toEqual(['a', 'b', 'c']);
    expect(listedDeals(null)).toEqual({ rows: [], hiddenCount: 0, visible: 0 });
  });
  it('says who hid a deal and when', () => {
    expect(hiddenLine({ hidden: true, hidden_by: 'alex', hidden_at: '2026-09-23T12:00:00+00:00' })).toBe('Hidden by Alex on 23 Sep');
    expect(hiddenLine({ hidden: true, hidden_by: 'austin', hidden_at: null })).toBe('Hidden by Austin');
    expect(hiddenLine({ hidden: false, hidden_by: null })).toBe('');
  });
});
