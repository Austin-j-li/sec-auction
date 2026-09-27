import { describe, expect, it } from 'vitest';
import { bulkChanges, bulkReason, bulkValues, eventList, pickRows, stageBulk, stagedCount, updateToExtend, withoutBulkRow } from './bulk';

const event = (uid, n, process = '1', round = '1') => ({ uid, id: n ? String(n) : '', cells: { '#': n ? String(n) : '', Process: process, Round: round } });
const ROWS = [event('a', 1), event('b', 2, '1', '2'), event('c', 3), event('d', 4, '2', 'post'), event('new-x', null)];

describe('bulk Process and Round edits', () => {
  it('takes a Process of 1 or more and a Round of 0 or more or post; a blank box leaves the column alone', () => {
    expect(bulkValues('2', '')).toEqual({ values: { Process: '2' }, error: '' });
    expect(bulkValues(' 02 ', '0')).toEqual({ values: { Process: '2', Round: '0' }, error: '' });
    expect(bulkValues('', 'Post')).toEqual({ values: { Round: 'post' }, error: '' });
    expect(bulkValues('', '').error).toBe('Enter a Process, a Round, or both.');
    expect(bulkValues('0', '1').error).toMatch(/^Process/);
    expect(bulkValues('1.5', '').error).toMatch(/^Process/);
    expect(bulkValues('', '-1').error).toMatch(/^Round/);
    expect(bulkValues('', 'later').error).toMatch(/^Round/);
    expect(bulkValues('1234567890', '').error).toMatch(/^Process/);
  });

  it('counts only the selected events the values change, in ledger order', () => {
    const picked = new Set(['d', 'a', 'b', 'new-x']);
    expect(bulkChanges(ROWS, picked, { Round: '2' }).map(row => row.uid)).toEqual(['a', 'd', 'new-x']);
    expect(bulkChanges(ROWS, picked, { Process: '1' }).map(row => row.uid)).toEqual(['d']);
    expect(bulkChanges(ROWS, new Set(['b']), { Process: '1', Round: '2' })).toEqual([]);
  });

  it('names the events as ranges, with unsaved events counted', () => {
    expect(eventList([ROWS[0], ROWS[1], ROWS[2], ROWS[4]])).toBe('#1–#3, 1 new event');
    expect(eventList([ROWS[3], ROWS[0]])).toBe('#1, #4');
    expect(eventList([])).toBe('');
  });

  it('toggles on a click and adds a range on a shift-click from the last event clicked', () => {
    const order = ROWS.map(row => row.uid);
    const one = pickRows(order, new Set(), null, 'b');
    expect([...one]).toEqual(['b']);
    expect([...pickRows(order, one, 'b', 'b')]).toEqual([]);
    expect([...pickRows(order, one, 'b', 'd', true)].sort()).toEqual(['b', 'c', 'd']);
    expect([...pickRows(order, one, 'd', 'a', true)].sort()).toEqual(['a', 'b', 'c', 'd']);
    expect([...pickRows(order, one, null, 'c', true)].sort()).toEqual(['b', 'c']);
  });

  it('stages one bulk_update for saved events and folds the values into an unsaved insert', () => {
    const insert = { type: 'insert', sheet: 'Deal ledger', client_uid: 'new-x', after_uid: 'a', values: { Who: 'New', Round: '1' } };
    const ops = stageBulk([insert], ['a', 'new-x', 'c'], { Round: '2' });
    expect(ops).toEqual([{ ...insert, values: { Who: 'New', Round: '2' } }, { type: 'bulk_update', sheet: 'Deal ledger', uids: ['a', 'c'], values: { Round: '2' } }]);
    expect(insert.values.Round).toBe('1');  // the staged list is not changed in place
    expect(stageBulk([insert], ['new-x'], { Round: '2' })).toHaveLength(1);
    expect(stagedCount(ops)).toBe(3);
  });

  it('drops a deleted event from a staged bulk_update, and the operation once empty', () => {
    const ops = [{ type: 'bulk_update', sheet: 'Deal ledger', uids: ['a', 'c'], values: { Round: '2' } }, { type: 'update', sheet: 'Deal ledger', uid: 'a', values: { Note: 'x' } }];
    expect(withoutBulkRow(ops, 'a')[0].uids).toEqual(['c']);
    expect(withoutBulkRow(withoutBulkRow(ops, 'a'), 'c')).toEqual([ops[1]]);
  });

  it('puts a field edit after a staged bulk_update that covers the event', () => {
    const before = { type: 'update', sheet: 'Deal ledger', uid: 'a', values: { Round: '3' } };
    const bulk = { type: 'bulk_update', sheet: 'Deal ledger', uids: ['a', 'c'], values: { Round: '2' } };
    expect(updateToExtend([before], 'Deal ledger', 'a')).toBe(before);
    expect(updateToExtend([before, bulk], 'Deal ledger', 'a')).toBeNull();
    expect(updateToExtend([before, bulk], 'Deal ledger', 'b')).toBeNull();
    const after = { type: 'update', sheet: 'Deal ledger', uid: 'a', values: { Round: '4' } };
    expect(updateToExtend([before, bulk, after], 'Deal ledger', 'a')).toBe(after);
    expect(updateToExtend([bulk], 'Rounds', 'a')).toBeNull();
  });

  it('writes a default save reason', () => {
    expect(bulkReason({ Process: '2', Round: '1' }, 12)).toBe('Set Process 2 and Round 1 on 12 events');
    expect(bulkReason({ Round: 'post' }, 1)).toBe('Set Round post on 1 event');
  });
});
