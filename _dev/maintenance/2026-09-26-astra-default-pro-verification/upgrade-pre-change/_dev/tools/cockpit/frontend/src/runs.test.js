import { describe, expect, it } from 'vitest';
import { accountEngines, activeRunLabel, dateWithYear, effortFor, extractNotice, failureText, importCheckText, jobEngineLabel, jobInstructionLabel, LEGACY_INSTRUCTION_LABEL, liveCheckText, pickEngine, formatElapsed, jobElapsed, orderVersions, planUsageText, rebaseLines, runSummary, usageText, validTimeout, versionOptionLabel } from './runs';
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
  it('names the ChatGPT plan and account for GPT runs, and adds the provider message', () => {
    const gpt = { account: 'chatgpt', engine: 'sol6' };
    expect(failureText(job('usage_limit', { params: gpt, result: { usage_limit_message: 'You have hit your usage limit. Try again at 3 PM.' } })))
      .toBe('Alex’s ChatGPT plan hit its usage limit. You have hit your usage limit. Try again at 3 PM.');
    expect(failureText(job('usage_limit', { params: gpt }))).toBe('Alex’s ChatGPT plan hit its usage limit');
    expect(failureText(job('not_connected', { params: gpt }))).toBe('No ChatGPT account connected');
    expect(failureText(job('login_expired', { params: gpt }))).toBe('Alex’s ChatGPT login has expired; reconnect in Settings');
    expect(failureText(job('usage_limit', { params: { account: 'claude' } }))).toBe('Alex’s Claude plan hit its usage limit');
  });
  it('names Fable’s safety filter for a Fable refusal only', () => {
    expect(failureText(job('provider_refusal', { params: { engine: 'fable51', account: 'claude' } }))).toBe('Blocked by Fable’s safety filter');
    expect(failureText(job('provider_refusal', { params: { engine: 'astra6', account: 'chatgpt' } }))).toBe('The model refused');
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
    expect(runSummary('medium', 'austin', undefined, 'v1.13.2')).toBe('Opus 5.5 · medium · v1.13.2 · on Austin’s Claude plan · usually 10–15 minutes');
    expect(runSummary('high', 'austin')).toBe('Opus 5.5 · high · default instruction · on Austin’s Claude plan');
    expect(runSummary('high', 'austin', { id: 'fable51', label: 'Fable 5.1', account: 'claude' }, 'draft 3f2a9c1 (Alex)')).toBe('Fable 5.1 · high · draft 3f2a9c1 (Alex) · on Austin’s Claude plan');
    expect(runSummary('medium', 'alex', { id: 'sol6', label: 'GPT-6-Sol', account: 'chatgpt' }, 'v1.14')).toBe('GPT-6-Sol · medium · v1.14 · on Alex’s ChatGPT plan');
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

describe('engines', () => {
  const engines = [
    { id: 'opus55', label: 'Opus 5.5', account: 'claude', efforts: ['low', 'medium', 'high', 'xhigh', 'max', 'ultra'], default_effort: 'medium', connected: false },
    { id: 'fable51', label: 'Fable 5.1', account: 'claude', efforts: ['low', 'medium', 'high'], default_effort: 'medium', connected: false, experimental: true },
    { id: 'sol6', label: 'GPT-6-Sol', account: 'chatgpt', efforts: ['low', 'medium', 'high'], default_effort: 'high', connected: true },
    { id: 'astra6', label: 'GPT-6-Astra', account: 'chatgpt', efforts: ['low', 'medium'], connected: true },
  ];
  it('reads the account’s engines without ultra, and falls back to Opus 5.5 before phase 4', () => {
    const list = accountEngines({ engines });
    expect(list[0].efforts).toEqual(['low', 'medium', 'high', 'xhigh', 'max']);
    expect(list[3].default_effort).toBe('medium');
    expect(accountEngines({ claude: { connected: true } })).toMatchObject([{ id: 'opus55', label: 'Opus 5.5', account: 'claude', connected: true, default_effort: 'medium' }]);
    expect(accountEngines(null)[0].connected).toBe(false);
  });
  it('preselects Opus 5.5 when usable, else the first connected engine', () => {
    const list = accountEngines({ engines });
    expect(pickEngine(list).id).toBe('sol6');
    expect(pickEngine(list, 'astra6').id).toBe('astra6');
    expect(pickEngine(list, 'fable51').id).toBe('sol6');
    expect(pickEngine(accountEngines({ engines: engines.map(e => ({ ...e, connected: true })) })).id).toBe('opus55');
    expect(pickEngine(list.map(e => ({ ...e, connected: false })))).toBe(null);
  });
  it('keeps an effort the new engine offers, else its default', () => {
    const [, , sol, astra] = accountEngines({ engines });
    expect(effortFor(sol, 'low')).toBe('low');
    expect(effortFor(astra, 'high')).toBe('medium');
    expect(effortFor(sol, 'max')).toBe('high');
  });
  it('labels a run’s engine and instruction, with the phase 2 defaults', () => {
    expect(jobEngineLabel({ params: { engine_label: 'GPT-6-Astra' } })).toBe('GPT-6-Astra');
    expect(jobEngineLabel({ params: { effort: 'high' } })).toBe('Opus 5.5');
    expect(jobInstructionLabel({ params: { instruction: { label: 'draft 3f2a9c1 (Alex)' } } })).toBe('draft 3f2a9c1 (Alex)');
    expect(jobInstructionLabel({})).toBe('v1.13.2');
    expect(LEGACY_INSTRUCTION_LABEL).toBe('v1.13.2');
  });
});

describe('which checker made a result', () => {
  it('labels the live check and the check at import', () => {
    expect(liveCheckText({ checker_version: '1.7' }, 'v1.14')).toBe('Live check: checker 1.7, v1.14 rules');
    expect(liveCheckText({}, null)).toBe('Live check: checker version unknown');
    expect(importCheckText({ checker_version: '1.6', ledger_schema: 'v1.14', errors: 1, warnings: 16 })).toBe('At import: checker 1.6, 1 error, 16 warnings');
    expect(importCheckText({ checker_version: null, errors: 0, warnings: 2 })).toBe('At import: checker version not recorded, 0 errors, 2 warnings');
    expect(importCheckText(null)).toBe('At import: not recorded');
  });
  it('adds the checker version to the version picker', () => {
    expect(versionOptionLabel({ id: 'run', label: 'Opus 5.5 · medium · draft f9595d7 (Austin) — Austin, 24 Sep 22:41', checker: { checker_version: '1.6', errors: 1, warnings: 16 } }))
      .toBe('Opus 5.5 · medium · draft f9595d7 (Austin) — Austin, 24 Sep 22:41 · checker 1.6');
    expect(versionOptionLabel({ id: 'opus55-medium', label: 'Opus 5.5 medium extraction', instruction_version: 'v1.13.2', checker: { checker_version: '1.5' }, is_base: true }))
      .toBe('Opus 5.5 medium extraction · v1.13.2 · checker 1.5 · base');
  });
});

describe('the Extract dialog’s line about the working copy', () => {
  const working = { revision: 8, base_instruction_version: 'v1.13.2', base_instruction_sha256: 'a'.repeat(64), base_ledger_schema: 'v1.13.2' };
  it('appears only when the run’s instruction is not the working copy’s', () => {
    expect(extractNotice(working, { sha256: 'a'.repeat(64), name: 'v1.13.2' })).toBe('');
    expect(extractNotice(working, { sha256: 'b'.repeat(64), name: 'v1.14' }))
      .toBe('The working copy (revision 8) is under v1.13.2 with v1.13.2 columns. This run becomes a separate version and is not merged into it; using it as the base replaces the working copy.');
    expect(extractNotice({ ...working, base_instruction_sha256: null, revision: 0 }, { sha256: 'b'.repeat(64), name: 'v1.13.2' })).toBe('');
    expect(extractNotice({ ...working, base_instruction_sha256: null, revision: 0 }, { sha256: 'b'.repeat(64), name: null }))
      .toBe('The working copy is under v1.13.2 with v1.13.2 columns. This run becomes a separate version and is not merged into it; using it as the base replaces the working copy.');
    expect(extractNotice(null, { sha256: 'b' })).toBe('');
  });
});

describe('the rebase dialog', () => {
  it('lists what stops applying, with counts', () => {
    const preview = {
      current: { id: 'opus55-medium', ledger_schema: 'v1.13.2', revision: 8 }, target: { id: 'run', ledger_schema: 'v1.14' },
      deal_review: { status: 'in_review', revision: 8, actor: 'austin' },
      stops_applying: { revisions: 8, edits: 42, row_marks: { total: 58, reviewed: 56, needs_decision: 2, unreviewed: 0 },
        finding_decisions: { total: 1, judgments_kept: 1, reset: 1 }, row_threads: { total: 1, open: 1, resolved: 0 } },
    };
    expect(rebaseLines(preview)).toEqual([
      'The columns change from v1.13.2 to v1.14.',
      '8 revisions saved on the current base (42 edits to its rows) stop applying. They stay in History; restoring revision 8, not revision 0, brings them back.',
      '58 row marks stop applying (56 reviewed, 2 needs decision).',
      '1 finding judgment carries over; the implementation and verification of 1 reset.',
      '1 row thread (1 open) stays with the old rows and reads “on an earlier base (revision 8)”.',
      'The deal’s review status stays, marked as edited since revision 8.',
    ]);
    expect(rebaseLines({ current: { revision: 0 }, target: {}, stops_applying: { revisions: 0, edits: 0, row_marks: { total: 0 }, finding_decisions: { total: 0 }, row_threads: { total: 0 } } }))
      .toEqual(['No revisions have been saved on the current base.']);
    expect(rebaseLines(null)).toEqual([]);
  });
});
