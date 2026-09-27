import { afterEach, describe, expect, it, vi } from 'vitest';
import { commentAction, filingRanges, saveDeal, segments } from './api';

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

describe('write token after a server restart', () => {
  const reply = (status, body) => Promise.resolve({ ok: status < 400, status, statusText: '', json: () => Promise.resolve(body) });
  const refused = () => reply(403, { error: 'write authorization failed' });
  afterEach(() => vi.unstubAllGlobals());

  it('fetches the session again and retries once with the new token', async () => {
    const fetch = vi.fn().mockReturnValueOnce(refused()).mockReturnValueOnce(reply(200, { user: 'alex', can_edit: true, csrf_token: 'new' }))
      .mockReturnValueOnce(reply(200, { saved: true }));
    vi.stubGlobal('fetch', fetch);
    const session = { user: 'alex', can_edit: true, csrf_token: 'old' };
    expect(await saveDeal('alpha', session, { revision: 1 })).toEqual({ saved: true });
    expect(fetch.mock.calls.map(([path, options]) => [path, options.headers['X-Cockpit-CSRF'] ?? null]))
      .toEqual([['/api/deal/alpha/edit', 'old'], ['/api/session', null], ['/api/deal/alpha/edit', 'new']]);
    expect(session.csrf_token).toBe('new');
  });

  it('retries every write refused with the old token when two are refused at the same time', async () => {
    const fetch = vi.fn((path, options) => path === '/api/session' ? reply(200, { user: 'alex', can_edit: true, csrf_token: 'new' })
      : options.headers['X-Cockpit-CSRF'] === 'new' ? reply(200, { saved: path }) : refused());
    vi.stubGlobal('fetch', fetch);
    const session = { user: 'alex', can_edit: true, csrf_token: 'old' };
    expect(await Promise.all([saveDeal('alpha', session, {}), commentAction('alpha', session, {})]))
      .toEqual([{ saved: '/api/deal/alpha/edit' }, { saved: '/api/deal/alpha/comments' }]);
    const writes = fetch.mock.calls.filter(([path]) => path !== '/api/session').map(([path, options]) => [path, options.headers['X-Cockpit-CSRF']]);
    expect(writes).toEqual([['/api/deal/alpha/edit', 'old'], ['/api/deal/alpha/comments', 'old'], ['/api/deal/alpha/edit', 'new'], ['/api/deal/alpha/comments', 'new']]);
    expect(session.csrf_token).toBe('new');
  });

  it('does not retry other refusals, another user, an unchanged token or a second refusal', async () => {
    const cases = [
      [reply(403, { error: 'only the author may change a comment' })],
      [refused(), reply(200, { user: 'austin', can_edit: true, csrf_token: 'new' })],
      [refused(), reply(200, { user: 'alex', can_edit: true, csrf_token: 'old' })],
      [refused(), reply(200, { user: 'alex', can_edit: true, csrf_token: 'new' }), refused()],
    ];
    for (const replies of cases) {
      const fetch = vi.fn();
      replies.forEach(item => fetch.mockReturnValueOnce(item));
      vi.stubGlobal('fetch', fetch);
      await expect(saveDeal('alpha', { user: 'alex', can_edit: true, csrf_token: 'old' }, {})).rejects.toMatchObject({ status: 403 });
      expect(fetch).toHaveBeenCalledTimes(replies.length);
    }
  });
});
