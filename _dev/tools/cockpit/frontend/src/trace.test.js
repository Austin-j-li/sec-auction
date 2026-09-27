import { describe, expect, it } from 'vitest';
import { changedByOther, countThreads, displayName, groupSessions, initials, tally, tallyText, threadContext, threadsFor } from './trace';
import { activityQuery } from './api';

const at = minutes => new Date(Date.UTC(2026, 8, 23, 14, 0) + minutes * 60000).toISOString();

describe('activity sessions', () => {
  it('starts a new session after a gap of more than 30 minutes in one actor’s activity', () => {
    const items = [
      { id: 1, actor: 'alex', at: at(0), kind: 'revision' },
      { id: 2, actor: 'alex', at: at(30), kind: 'comment' },
      { id: 3, actor: 'alex', at: at(61), kind: 'revision' },
    ].reverse();
    const groups = groupSessions(items);
    expect(groups.map(group => group.items.map(item => item.id))).toEqual([[3], [2, 1]]);
    expect(groups[1]).toMatchObject({ start: at(0), end: at(30) });
  });

  it('keeps each actor’s sessions separate even when their activity interleaves', () => {
    const items = [
      { id: 1, actor: 'alex', at: at(0), kind: 'revision' },
      { id: 2, actor: 'austin', at: at(5), kind: 'comment' },
      { id: 3, actor: 'alex', at: at(20), kind: 'reply' },
      { id: 4, actor: 'austin', at: at(30), kind: 'resolve' },
    ];
    const groups = groupSessions(items);
    expect(groups.map(group => [group.actor, group.items.map(item => item.id)])).toEqual([['austin', [4, 2]], ['alex', [3, 1]]]);
  });

  it('summarises a session as edits, comments and other actions', () => {
    const items = ['revision', 'restore', 'comment', 'reply', 'resolve'].map((kind, id) => ({ id, kind }));
    expect(tally(items)).toEqual({ edits: 2, comments: 2, other: 1 });
    expect(tallyText(tally(items))).toBe('2 edits, 2 comments, 1 other');
    expect(tallyText({ edits: 0, comments: 1 })).toBe('1 comment');
  });
});

describe('people', () => {
  it('uses fixed initials and display names', () => {
    expect([initials('austin'), initials('alex'), initials('local')]).toEqual(['AL', 'AG', 'LO']);
    expect([displayName('austin'), displayName('alex'), displayName('local')]).toEqual(['Austin', 'Alex', 'Local']);
  });
});

describe('row changed by the other person since last seen', () => {
  const authors = { Event: { actor: 'alex', at: at(0), revision: 12 }, Who: { actor: 'austin', at: at(1), revision: 13 } };
  it('marks a row the other person changed after the reader’s seen revision', () => {
    expect(changedByOther(authors, 'austin', 11)).toBe('alex');
    expect(changedByOther(authors, 'austin', null)).toBe('alex');
  });
  it('shows nothing for one’s own changes, already-seen revisions or unknown readers', () => {
    expect(changedByOther(authors, 'austin', 12)).toBe(null);
    expect(changedByOther({ Who: authors.Who }, 'austin', 0)).toBe(null);
    expect(changedByOther(authors, 'unknown', 0)).toBe(null);
    expect(changedByOther(undefined, 'austin', 0)).toBe(null);
  });
});

describe('threads', () => {
  const threads = [
    { id: 't1', target: { kind: 'row', sheet: 'Deal ledger', uid: 'r1' }, resolved: null },
    { id: 't2', target: { kind: 'row', sheet: 'Deal ledger', uid: 'r1' }, resolved: { by: 'alex', at: at(0) } },
    { id: 't3', target: { kind: 'deal' }, resolved: null },
    { id: 't4', target: { kind: 'row', sheet: 'Rounds', uid: 'gone' }, target_missing: true, resolved: null },
  ];
  it('counts open and resolved threads per target', () => {
    expect(countThreads(threads)).toEqual({ r1: { open: 1, resolved: 1 }, deal: { open: 1, resolved: 0 }, gone: { open: 1, resolved: 0 } });
  });
  it('shows removed-row threads in the deal discussion', () => {
    expect(threadsFor(threads, { kind: 'deal' }).map(t => t.id)).toEqual(['t3', 't4']);
    expect(threadsFor(threads, { kind: 'row', uid: 'r1' }).map(t => t.id)).toEqual(['t1', 't2']);
  });
  it('builds the account-wide feed query without empty filters', () => {
    expect(activityQuery({ actor: 'alex', before: 57 })).toBe('/api/activity?actor=alex&before=57&limit=100');
  });
});

describe('a thread whose row is gone', () => {
  it('says where the row went', () => {
    expect(threadContext({ target_missing: true, target_context: 'on an earlier base (revision 8)' })).toBe('On an earlier base (revision 8)');
    expect(threadContext({ target_missing: true, target_context: 'record removed' })).toBe('Record removed');
    expect(threadContext({ target_missing: true })).toBe('Record removed');
    expect(threadContext({ target_missing: false, target_context: null })).toBe('');
  });
});
