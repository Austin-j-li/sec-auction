import { describe, expect, it } from 'vitest';
import { filingRanges, segments } from './api';

describe('source text highlighting', () => {
  it('preserves the full source text through overlapping quote and search marks', () => {
    const source = 'The board met. The bidder submitted a revised proposal.';
    const parts = segments(source, [{ from: 4, to: 28, rowIndex: 0 }, { from: 19, to: 43, rowIndex: 1 }], 'bidder');
    expect(parts.map(part => part.text).join('')).toBe(source);
    expect(parts.some(part => part.rows.length === 2)).toBe(true);
    expect(parts.find(part => part.text === 'bidder')?.search).toBe(true);
  });

  it('keeps multi-block evidence ranges tied to the same event', () => {
    const blocks = [{ text: 'Alpha beta' }, { text: 'Gamma delta' }];
    const rows = [{ quote: { located: true, start: { block: 0, offset: 6 }, end: { block: 1, offset: 5 } } }];
    const ranges = filingRanges(rows, blocks);
    expect(ranges.get(0)).toEqual([{ from: 6, to: 10, rowIndex: 0 }]);
    expect(ranges.get(1)).toEqual([{ from: 0, to: 5, rowIndex: 0 }]);
  });

  it('ignores invalid source offsets instead of changing the rendered text', () => {
    const blocks = [{ text: 'Complete filing text' }];
    expect(filingRanges([{ quote: { located: true, start: { block: -1, offset: 0 }, end: { block: 0, offset: 2 } } }], blocks).size).toBe(0);
    expect(segments(blocks[0].text).map(part => part.text).join('')).toBe(blocks[0].text);
  });
});
