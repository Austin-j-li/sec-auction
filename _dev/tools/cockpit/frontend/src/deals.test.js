import { describe, expect, it } from 'vitest';
import { formatBytes, seedAction, seedReview, validName, validSlug } from './deals';

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
});
