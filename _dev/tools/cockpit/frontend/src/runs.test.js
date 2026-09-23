import { describe, expect, it } from 'vitest';
import { activeRunLabel, dateWithYear, failureText, formatElapsed, jobElapsed, orderVersions, planUsageText, runSummary, usageText, validTimeout, versionOptionLabel } from './runs';
import { shortTime, tally, tallyText } from './trace';
import { compareQuery } from './api';

const at = minutes => new Date(Date.UTC(2026, 8, 23, 14, 0) + minutes * 60000).toISOString();

describe('failure reasons in words', () => {
  const job = (failure_reason, extra = {}) => ({ state: 'failed', actor: 'alex', failure_reason, ...extra });
  it('names whose plan hit its usage limit and when it resets', () => {
    expect(failureText(job('usage_limit', { result: { usage_limit_resets_at: at(60) } }))).toBe(`Alex’s Claude plan hit its usage limit; it resets ${shortTime(at(60))}`);
    expect(failureText(job('usage_limit'))).toBe('Alex’s Claude plan hit its usage limit');
  });
  it('words the known reasons', () => {
    expect(failureText(job('provider_refusal'))).toBe('The model refused');
    expect(failureText(job('timeout'))).toBe('Ran past the time limit');
    expect(failureText({ state: 'timed_out', actor: 'alex' })).toBe('Ran past the time limit');
    expect(failureText(job('not_connected'))).toBe('No Claude account connected');
    expect(failureText({ state: 'cancelled', actor: 'austin', failure_reason: 'cancelled' })).toBe('Cancelled by Austin');
    expect(failureText({ state: 'cancelled', actor: 'austin', cancelled_by: 'alex' })).toBe('Cancelled by Alex');
    expect(failureText(job('worker_restart'))).toBe('Interrupted by a server restart');
  });
  it('shows any other reason verbatim and nothing for a successful run', () => {
    expect(failureText(job('provider_error'))).toBe('Failed (provider_error)');
    expect(failureText({ state: 'completed', actor: 'alex' })).toBe(null);
  });
});

describe('elapsed time', () => {
  it('formats seconds, minutes and hours', () => {
    expect(formatElapsed(45)).toBe('45 s');
    expect(formatElapsed(12 * 60 + 5)).toBe('12 min 05 s');
    expect(formatElapsed(3600 + 2 * 60 + 59)).toBe('1 h 02 min');
    expect(formatElapsed(null)).toBe('');
    expect(formatElapsed(-1)).toBe('');
  });
  it('ticks from the start for active jobs and uses the recorded duration for finished ones', () => {
    const now = Date.parse(at(10));
    expect(jobElapsed({ state: 'running', started_at: at(0) }, now)).toBe(600);
    expect(jobElapsed({ state: 'queued', started_at: null }, now)).toBe(null);
    expect(jobElapsed({ state: 'completed', started_at: at(0), ended_at: at(20), result: { elapsed_seconds: 700 } }, now)).toBe(700);
    expect(jobElapsed({ state: 'failed', started_at: at(0), ended_at: at(3) }, now)).toBe(180);
  });
});

describe('plan usage and cost', () => {
  it('formats the account record as percentages with the time it was seen', () => {
    const plan = { at: at(5), five_hour: { utilization: 0.1, resets_at: at(60) }, seven_day: { utilization: 0.29 } };
    expect(planUsageText(plan)).toBe(`5-hour: 10% · weekly: 29% · as of ${shortTime(at(5))}`);
  });
  it('accepts a raw rate-limit record and percentage values', () => {
    expect(planUsageText({ unifiedWindows: { five_hour: { utilization: 42 }, seven_day: { utilization: 7 } } })).toBe('5-hour: 42% · weekly: 7%');
    expect(planUsageText(null)).toBe('');
    expect(planUsageText({ at: at(0) })).toBe('');
  });
  it('sums tokens and shows the cost', () => {
    expect(usageText({ tokens: { input_tokens: 900000, output_tokens: 300000 }, cost_usd: 3.4 })).toBe('1.2 M tokens · $3.40');
    expect(usageText({ tokens: { output_tokens: 4500 } })).toBe('5 k tokens');
    expect(usageText(null)).toBe('');
  });
  it('dates an expiry with its year', () => {
    expect(dateWithYear('2027-09-23T12:00:00Z')).toMatch(/^2[34] Sep 2027$/);
  });
  it('summarises a run and validates the time limit', () => {
    expect(runSummary('medium', 'austin')).toBe('Opus 5.5 · medium · v1.13.2 · on Austin’s Claude plan · usually 10–15 minutes');
    expect([validTimeout('90'), validTimeout('9'), validTimeout('361'), validTimeout('12.5'), validTimeout('')]).toEqual([true, false, false, false, false]);
  });
});

describe('version dropdown', () => {
  const versions = [
    { id: 'working', kind: 'working', label: 'Working copy' },
    { id: 'catalog-a', kind: 'raw', label: 'Opus 5.5 medium', instruction_version: 'v1.13.2' },
    { id: 'run-old', kind: 'raw', label: 'Opus 5.5 · high · v1.13.2 — Alex, 23 Sep 10:00', instruction_version: 'v1.13.2', started_at: at(0) },
    { id: 'run-hidden', kind: 'raw', label: 'Hidden run', started_at: at(30), hidden: true },
    { id: 'run-new', kind: 'raw', label: 'Opus 5.5 · low · v1.13.2 — Austin, 23 Sep 15:00', started_at: at(60), is_base: true },
    { id: 'catalog-b', kind: 'raw', label: 'Second catalog' },
  ];
  it('lists the working copy first, then runs newest first, then catalog versions, without hidden ones', () => {
    const { working, originals, hiddenCount } = orderVersions(versions, { baseId: 'catalog-a' });
    expect(working.map(v => v.id)).toEqual(['working']);
    expect(originals.map(v => v.id)).toEqual(['run-new', 'run-old', 'catalog-a', 'catalog-b']);
    expect(hiddenCount).toBe(1);
  });
  it('shows hidden versions when asked, or when one is on screen', () => {
    expect(orderVersions(versions, { showHidden: true }).originals.map(v => v.id)).toEqual(['run-new', 'run-hidden', 'run-old', 'catalog-a', 'catalog-b']);
    expect(orderVersions(versions, { selected: 'run-hidden' }).originals.map(v => v.id)).toContain('run-hidden');
  });
  it('marks the base from is_base, else from the workspace base id', () => {
    const marked = orderVersions(versions, { baseId: 'catalog-a' }).originals;
    expect(marked.filter(v => v.is_base).map(v => v.id)).toEqual(['run-new']);
    const fallback = orderVersions(versions.map(({ is_base, ...v }) => v), { baseId: 'catalog-a' }).originals;
    expect(fallback.filter(v => v.is_base).map(v => v.id)).toEqual(['catalog-a']);
  });
  it('labels options without repeating the instruction version', () => {
    const [runNew, , catalogA] = orderVersions(versions, { baseId: 'catalog-a' }).originals;
    expect(versionOptionLabel(runNew)).toBe('Opus 5.5 · low · v1.13.2 — Austin, 23 Sep 15:00 · base');
    expect(versionOptionLabel(catalogA)).toBe('Opus 5.5 medium · v1.13.2');
    expect(versionOptionLabel({ id: 'run-hidden', label: 'Hidden run', hidden: true })).toBe('Hidden run · hidden');
    expect(versionOptionLabel(versions[0])).toBe('Working copy · editable');
  });
  it('builds the compare query', () => {
    expect(compareQuery('acme', 'v1', 'working')).toBe('/api/deal/acme/compare?from=v1&to=working');
  });
});

describe('run activity', () => {
  it('counts runs apart from edits and comments', () => {
    const items = ['extraction', 'extraction_failed', 'revision', 'comment', 'hide'].map((kind, id) => ({ id, kind }));
    expect(tally(items)).toEqual({ runs: 2, edits: 1, comments: 1, other: 1 });
    expect(tallyText({ runs: 1, edits: 2 })).toBe('1 run, 2 edits');
  });
});

describe('active run badge', () => {
  const now = Date.parse(at(2.5));
  it('shows elapsed time for one active run and nothing when idle', () => {
    expect(activeRunLabel([{ state: 'running', started_at: at(0) }, { state: 'completed' }], now)).toBe('Extracting · 2 min 30 s');
    expect(activeRunLabel([{ state: 'queued' }], now)).toBe('Extraction queued');
    expect(activeRunLabel([{ state: 'running', started_at: at(0) }, { state: 'checking', started_at: at(1) }], now)).toBe('2 extractions running');
    expect(activeRunLabel([{ state: 'failed' }], now)).toBe('');
    expect(activeRunLabel(null, now)).toBe('');
  });
});
