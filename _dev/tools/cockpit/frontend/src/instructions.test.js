import { describe, expect, it } from 'vitest';
import { defaultInstructionId, foldRows, inlineChange, instructionByline, instructionOptionLabel, lineDiff, nameProblem, noteProblem, orderInstructions, sideBySide, textBytes } from './instructions';
import { shortTime } from './trace';

// Rebuild both texts from the ops: a correct diff reproduces each side exactly.
function rebuild(ops) {
  return {
    before: ops.filter(op => op.type !== 'add').map(op => op.text).join('\n'),
    after: ops.filter(op => op.type !== 'del').map(op => op.text).join('\n'),
  };
}
const lines = list => list.join('\n');

describe('line diff', () => {
  it('finds nothing to change in equal texts', () => {
    const diff = lineDiff('a\nb\nc', 'a\nb\nc');
    expect(diff).toMatchObject({ exact: true, added: 0, removed: 0 });
    expect(diff.ops.map(op => op.type)).toEqual(['same', 'same', 'same']);
  });
  it('marks a changed, an inserted and a deleted line', () => {
    const diff = lineDiff(lines(['one', 'two', 'three', 'four']), lines(['one', 'TWO', 'three', 'new', 'four']));
    expect(diff.ops.map(op => `${op.type[0]}:${op.text}`)).toEqual(['s:one', 'd:two', 'a:TWO', 's:three', 'a:new', 's:four']);
    expect([diff.added, diff.removed]).toEqual([2, 1]);
    const removal = lineDiff(lines(['a', 'b', 'c']), lines(['a', 'c']));
    expect(removal.ops.filter(op => op.type !== 'same')).toEqual([{ type: 'del', a: 1, text: 'b' }]);
  });
  it('handles empty sides', () => {
    expect(lineDiff('', 'x\ny').ops.map(op => op.type)).toEqual(['del', 'add', 'add']);
    expect(lineDiff('x', '').ops.map(op => op.type)).toEqual(['del', 'add']);
  });
  it('reproduces both texts for scrambled inputs and is minimal for a known case', () => {
    let seed = 7;
    const rand = () => (seed = (seed * 1103515245 + 12345) % 2147483648) / 2147483648;
    for (let round = 0; round < 50; round++) {
      const a = Array.from({ length: Math.floor(rand() * 30) }, () => 'abcde'[Math.floor(rand() * 5)]);
      const b = Array.from({ length: Math.floor(rand() * 30) }, () => 'abcde'[Math.floor(rand() * 5)]);
      const diff = lineDiff(lines(a), lines(b));
      expect(rebuild(diff.ops)).toEqual({ before: lines(a), after: lines(b) });
    }
    // Myers' classic example: ABCABBA → CBABAC needs 5 edits.
    const classic = lineDiff(lines([...'ABCABBA']), lines([...'CBABAC']));
    expect(classic.added + classic.removed).toBe(5);
  });
  it('falls back to one replaced block when the texts differ too much', () => {
    const a = Array.from({ length: 300 }, (_, i) => `a${i}`), b = Array.from({ length: 300 }, (_, i) => `b${i}`);
    const diff = lineDiff(lines(['head', ...a, 'tail']), lines(['head', ...b, 'tail']), { maxEdits: 50 });
    expect(diff.exact).toBe(false);
    expect([diff.added, diff.removed]).toEqual([300, 300]);
    expect(diff.ops[0]).toMatchObject({ type: 'same', text: 'head' });
    expect(diff.ops.at(-1)).toMatchObject({ type: 'same', text: 'tail' });
    expect(rebuild(diff.ops)).toEqual({ before: lines(['head', ...a, 'tail']), after: lines(['head', ...b, 'tail']) });
  });
  it('diffs a 70 KB instruction-sized text quickly', () => {
    const base = Array.from({ length: 280 }, (_, i) => `Paragraph ${i}: ${'lorem ipsum '.repeat(20)}`);
    const edited = base.map((line, i) => i % 40 === 0 ? `${line} (revised)` : line).filter((_, i) => i !== 100);
    const started = performance.now();
    const diff = lineDiff(lines(base), lines(edited));
    expect(performance.now() - started).toBeLessThan(500);
    expect(diff.exact).toBe(true);
    expect([diff.added, diff.removed]).toEqual([7, 8]);
  });
});

describe('side-by-side rows', () => {
  it('pairs removed and added lines and numbers each side', () => {
    const rows = sideBySide(lineDiff(lines(['a', 'b', 'c', 'd']), lines(['a', 'B', 'x', 'd'])).ops);
    expect(rows.map(row => row.kind)).toEqual(['same', 'change', 'change', 'same']);
    expect(rows[1]).toEqual({ kind: 'change', left: { n: 2, text: 'b' }, right: { n: 2, text: 'B' } });
    const lopsided = sideBySide(lineDiff(lines(['a', 'b', 'c']), lines(['a', 'x', 'y', 'z', 'c'])).ops);
    expect(lopsided.map(row => row.kind)).toEqual(['same', 'change', 'add', 'add', 'same']);
    expect(lopsided[3]).toEqual({ kind: 'add', left: null, right: { n: 4, text: 'z' } });
  });
  it('folds long unchanged stretches around changes', () => {
    const before = Array.from({ length: 20 }, (_, i) => `l${i}`);
    const after = before.map((line, i) => i === 10 ? 'changed' : line);
    const folded = foldRows(sideBySide(lineDiff(lines(before), lines(after)).ops), 2);
    expect(folded.map(row => row.kind === 'gap' ? `gap${row.count}` : row.kind)).toEqual(['gap8', 'same', 'same', 'change', 'same', 'same', 'gap7']);
    expect(foldRows(sideBySide(lineDiff('a\nb', 'a\nb').ops))).toEqual([{ kind: 'gap', count: 2 }]);
  });
  it('highlights the differing middle of a changed line', () => {
    expect(inlineChange('The bidder offered $10.', 'The bidder offered $12 in cash.')).toEqual({
      left: ['The bidder offered $1', '0', '.'], right: ['The bidder offered $1', '2 in cash', '.'],
    });
    expect(inlineChange('same', 'same')).toEqual({ left: ['same', '', ''], right: ['same', '', ''] });
  });
});

describe('instruction list helpers', () => {
  const items = [
    { id: 'd1', status: 'draft', label: 'draft 3f2a9c1 (Alex)', created_by: 'alex', updated_by: 'austin', updated_at: '2026-09-23T14:05:00Z' },
    { id: 'p1', status: 'published', name: 'v1.13.2', label: 'v1.13.2', is_default: true, published_by: 'system', published_at: '2026-09-22T10:00:00Z' },
    { id: 'p2', status: 'published', name: 'v1.14', label: 'v1.14', published_by: 'austin', published_at: '2026-09-23T09:00:00Z' },
  ];
  it('orders published versions before drafts and finds the default', () => {
    expect(orderInstructions(items).map(item => item.id)).toEqual(['p1', 'p2', 'd1']);
    expect(defaultInstructionId({ default_id: 'p2', items })).toBe('p2');
    expect(defaultInstructionId({ items })).toBe('p1');
    expect(defaultInstructionId(null)).toBe(null);
  });
  it('labels options and bylines', () => {
    expect(items.map(instructionOptionLabel)).toEqual(['draft 3f2a9c1 (Alex)', 'v1.13.2 · default', 'v1.14']);
    expect(instructionOptionLabel({ status: 'draft', label: 'Scratch' })).toBe('Scratch · draft');
    expect(instructionByline(items[0])).toBe(`Draft by Alex · saved ${shortTime('2026-09-23T14:05:00Z')} by Austin`);
    expect(instructionByline(items[2])).toBe(`Published by Austin · ${shortTime('2026-09-23T09:00:00Z')}`);
  });
  it('validates publish names and change notes', () => {
    expect(nameProblem('v1.14.1', items)).toBe('');
    expect(nameProblem('v1.14', items)).toBe('Another version already has this name.');
    expect(nameProblem('  ', items)).toBe('Give the version a name.');
    expect(nameProblem('v1/14', items)).toMatch(/^Use letters/);
    expect(nameProblem('x'.repeat(41), items)).toBe('At most 40 characters.');
    expect(noteProblem('Clarify the objective')).toBe('');
    expect(noteProblem(' ')).toBe('Say what changed and why.');
    expect(noteProblem('x'.repeat(2001))).toBe('At most 2000 characters.');
  });
  it('measures text in UTF-8 bytes', () => {
    expect(textBytes('a—b')).toBe(5);
  });
});
