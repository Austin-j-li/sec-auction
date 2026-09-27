import { count, text } from './api';
import { displayName, shortTime } from './trace';

// Pure helpers for accounts, extraction runs and versions (phase 2).

export const EFFORTS = ['low', 'medium', 'high', 'xhigh', 'max'];
export const DEFAULT_EFFORT = 'medium';
export const FABLE_WARNING = 'Fable’s safety filter often blocks runs partway (6 of 11 test prompts); a blocked run fails and must be restarted.';
const ACCOUNT_NAMES = { claude: 'Claude', chatgpt: 'ChatGPT' };
export const DEFAULT_ENGINE = { id: 'opus55', label: 'Opus 5.5', account: 'claude', efforts: EFFORTS, default_effort: DEFAULT_EFFORT };
const ENGINE_EFFORT = { astra6: 'high' };  // Astra's own default when chosen explicitly.
export const DEFAULT_TIMEOUT = 90;
export const TIMEOUT_RANGE = [10, 360];
export const ACTIVE_STATES = new Set(['queued', 'preparing', 'running', 'checking', 'importing']);
export const CANCELLABLE_STATES = new Set(['queued', 'preparing', 'running']);
export const CONNECT_ACTIVE_STATES = new Set(['queued', 'waiting_for_code', 'completing']);
export const CHATGPT_CONNECT_ACTIVE_STATES = new Set(['queued', 'waiting_for_approval']);
export const STATE_LABELS = {
  queued: 'Queued', preparing: 'Preparing', running: 'Running', checking: 'Checking', importing: 'Importing',
  completed: 'Completed', failed: 'Failed', timed_out: 'Timed out', cancelled: 'Cancelled',
};
export const STATE_TONES = { completed: 'success', failed: 'error', timed_out: 'error', cancelled: 'muted' };

// The engines the signed-in person may choose, from GET /api/account. Before phase 4 the server sends none:
// then Opus 5.5 alone, available when the Claude account is connected. "ultra" is never offered.
export function accountEngines(account) {
  const list = Array.isArray(account?.engines) && account.engines.length ? account.engines
    : [{ ...DEFAULT_ENGINE, connected: Boolean(account?.claude?.connected) }];
  return list.map(engine => {
    const efforts = (engine.efforts?.length ? engine.efforts : EFFORTS).filter(effort => effort !== 'ultra');
    const preferred = ENGINE_EFFORT[engine.id] || DEFAULT_EFFORT;
    const fallback = efforts.includes(preferred) ? preferred : efforts[0];
    return { ...engine, label: engine.label || engine.id, efforts, default_effort: efforts.includes(engine.default_effort) ? engine.default_effort : fallback, connected: Boolean(engine.connected) };
  });
}
// Preselect Opus 5.5 when usable, else the first connected engine; preserve an explicit selection.
export function pickEngine(engines, current = null) {
  const usable = (engines || []).filter(engine => engine.connected);
  return usable.find(engine => engine.id === current) || usable.find(engine => engine.id === DEFAULT_ENGINE.id) || usable[0] || null;
}
// Keep the chosen effort when the new engine offers it, else use the engine's default.
export const effortFor = (engine, current) => engine?.efforts?.includes(current) ? current : engine?.default_effort || DEFAULT_EFFORT;
export const accountLabel = account => ACCOUNT_NAMES[account] || text(account);
export const connectHint = engine => `connect your ${accountLabel(engine?.account)} account in Settings`;

export const isActive = job => ACTIVE_STATES.has(job?.state);
export const stateTone = state => ACTIVE_STATES.has(state) ? 'warning' : STATE_TONES[state] || 'muted';

// Which plan a run used: "Claude plan" or "ChatGPT plan", from the job's recorded account (Claude before phase 4).
export const planName = account => account === 'chatgpt' ? 'ChatGPT plan' : 'Claude plan';
export const jobEngineLabel = job => text(job?.params?.engine_label) || 'Opus 5.5';
export const jobInstructionLabel = job => text(job?.params?.instruction?.label) || 'instruction not recorded';

// The failed or cancelled outcome of a run, in words. Null for a run that has not failed.
export function failureText(job) {
  const reason = job?.failure_reason || (job?.state === 'timed_out' ? 'timed_out' : job?.state === 'cancelled' ? 'cancelled' : null);
  if (!reason) return job?.state === 'failed' ? 'Failed' : null;
  const name = displayName(job.actor), account = job.params?.account;
  switch (reason) {
    case 'usage_limit': {
      const resets = job.result?.usage_limit_resets_at, message = text(job.result?.usage_limit_message).trim();
      return `${name}’s ${planName(account)} hit its usage limit${resets ? `; it resets ${shortTime(resets)}` : ''}${message ? `. ${message}` : ''}`;
    }
    case 'provider_refusal': return job.params?.engine === 'fable51' ? 'Blocked by Fable’s safety filter' : 'The model refused';
    case 'login_expired': return `${name}’s ChatGPT login has expired; reconnect in Settings`;
    case 'timeout':
    case 'timed_out': return 'Ran past the time limit';
    case 'not_connected': return `No ${account === 'chatgpt' ? 'ChatGPT' : 'Claude'} account connected`;
    case 'cancelled': return `Cancelled by ${displayName(job.cancelled_by || job.actor)}`;
    case 'worker_restart': return 'Interrupted by a server restart';
    default: return `Failed (${reason})`;
  }
}

// "45 s", "12 min 05 s", "1 h 02 min".
export function formatElapsed(seconds) {
  if (seconds == null || !Number.isFinite(seconds) || seconds < 0) return '';
  const total = Math.floor(seconds), h = Math.floor(total / 3600), m = Math.floor((total % 3600) / 60), s = total % 60;
  const pad = n => String(n).padStart(2, '0');
  if (h) return `${h} h ${pad(m)} min`;
  if (m) return `${m} min ${pad(s)} s`;
  return `${s} s`;
}

const time = value => { const t = Date.parse(value); return Number.isNaN(t) ? null : t; };
// Seconds a job has run: ticking from its start while active, else the recorded or measured duration.
export function jobElapsed(job, now = Date.now()) {
  const start = time(job?.started_at);
  if (isActive(job)) return start == null ? null : Math.max(0, (now - start) / 1000);
  if (Number.isFinite(job?.result?.elapsed_seconds)) return job.result.elapsed_seconds;
  const end = time(job?.ended_at);
  return start == null || end == null ? null : Math.max(0, (end - start) / 1000);
}

// Header badge for a deal's active runs: "Extracting · 2 min 30 s", "Queued", or "2 extractions running".
export function activeRunLabel(jobs, now = Date.now()) {
  const active = (jobs || []).filter(isActive);
  if (active.length === 0) return '';
  if (active.length > 1) return `${active.length} extractions running`;
  const [job] = active;
  if (job.state === 'queued') return 'Extraction queued';
  const elapsed = formatElapsed(jobElapsed(job, now));
  return elapsed ? `Extracting · ${elapsed}` : 'Extracting';
}

// "1.2 M tokens · $3.40" from a runner usage record ({tokens: {...}, cost_usd}); '' when absent.
export function usageText(usage) {
  if (!usage || typeof usage !== 'object') return '';
  const tokens = Object.values(usage.tokens || {}).filter(Number.isFinite).reduce((sum, n) => sum + n, 0);
  const parts = [];
  if (tokens > 0) parts.push(tokens >= 1e6 ? `${(tokens / 1e6).toFixed(1)} M tokens` : tokens >= 1e3 ? `${Math.round(tokens / 1e3)} k tokens` : `${tokens} tokens`);
  if (Number.isFinite(usage.cost_usd)) parts.push(`$${usage.cost_usd.toFixed(2)}`);
  return parts.join(' · ');
}

// Utilization arrives as a fraction (0.1) or a percentage (10); show a whole percentage.
function percent(value) {
  if (!Number.isFinite(value)) return null;
  return `${Math.round(value <= 1 ? value * 100 : value)}%`;
}
// "5-hour: 10% · weekly: 29% · as of 23 Sep 14:05". Accepts the account's normalised record
// ({at, five_hour: {utilization}, seven_day: {…}}) or a raw rate_limit_info ({unifiedWindows: {…}}).
export function planUsageText(plan, at) {
  if (!plan || typeof plan !== 'object') return '';
  const windows = plan.unifiedWindows || plan;
  const five = percent(windows.five_hour?.utilization), week = percent(windows.seven_day?.utilization);
  const parts = [five && `5-hour: ${five}`, week && `weekly: ${week}`].filter(Boolean);
  if (!parts.length) return '';
  const when = plan.at || at;
  if (when) parts.push(`as of ${shortTime(when)}`);
  return parts.join(' · ');
}

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
// "23 Sep 2027": a date far enough away that the year matters.
export function dateWithYear(value) {
  const d = new Date(value);
  return Number.isNaN(d.getTime()) ? text(value) : `${d.getDate()} ${MONTHS[d.getMonth()]} ${d.getFullYear()}`;
}

// "Fable 5.1 · high · draft 3f2a9c1 (Alex) · on Austin’s Claude plan"; Opus 5.5 at medium adds "· usually 10–15 minutes".
// The Extract dialog passes the chosen instruction, which starts as the default one.
export function runSummary(effort, user, engine = DEFAULT_ENGINE, instructionLabel = '') {
  const parts = [engine.label, effort, instructionLabel || 'default instruction', `on ${displayName(user)}’s ${planName(engine.account)}`];
  if (engine.id === 'opus55' && effort === 'medium') parts.push('usually 10–15 minutes');
  return parts.join(' · ');
}

export function validTimeout(value) {
  const n = Number(value);
  return Number.isInteger(n) && n >= TIMEOUT_RANGE[0] && n <= TIMEOUT_RANGE[1];
}

// Versions produced by a cockpit run carry who started them and when; catalog versions do not.
export const isImported = version => Boolean(version?.imported ?? version?.started_at);

// The version dropdown: the working copy first, then originals newest first by started_at, catalog versions last
// (in catalog order). Hidden versions are left out unless asked for, or unless one is the version on screen.
export function orderVersions(versions, { baseId = null, showHidden = false, selected = null } = {}) {
  // When the server marks the base (is_base), trust it for every version; otherwise match the workspace base id.
  const reported = (versions || []).some(version => version?.is_base != null);
  const list = (versions || []).map((version, index) => ({ ...version, index, hidden: Boolean(version.hidden),
    is_base: version.kind !== 'working' && (reported ? Boolean(version.is_base) : Boolean(baseId) && version.id === baseId) }));
  const working = list.filter(version => version.kind === 'working' || version.id === 'working');
  const originals = list.filter(version => !working.includes(version) && (showHidden || !version.hidden || version.id === selected));
  originals.sort((a, b) => {
    const ta = time(a.started_at), tb = time(b.started_at);
    if (ta != null && tb != null) return tb - ta || a.index - b.index;
    if (ta != null) return -1;
    if (tb != null) return 1;
    return a.index - b.index;
  });
  return { working, originals, hiddenCount: list.filter(version => version.hidden).length };
}

export function versionOptionLabel(version) {
  if (version.kind === 'working' || version.id === 'working') return 'Working copy · editable';
  const label = text(version.label || version.id);
  const instruction = version.instruction_version && !label.includes(version.instruction_version) ? ` · ${version.instruction_version}` : '';
  const checker = checkerLabel(version.checker);
  return `${label}${instruction}${checker ? ` · ${checker}` : ''}${version.hidden ? ' · hidden' : ''}${version.is_base ? ' · base' : ''}`;
}

// A version's import check is fixed when imported; the live check uses the current checker.
export const checkerLabel = checker => checker?.checker_version ? `checker ${checker.checker_version}` : '';
export function liveCheckText(check) {
  return `Live check: ${checkerLabel(check) || 'checker version unknown'}`;
}
// "At import: checker 1.6, 1 error, 16 warnings", or "At import: not recorded".
export function importCheckText(checker) {
  if (!checker) return 'At import: not recorded';
  return `At import: ${[checkerLabel(checker) || 'checker version not recorded', count(checker.errors ?? 0, 'error'), count(checker.warnings ?? 0, 'warning')].join(', ')}`;
}

// The Extract dialog's one line when the run's instruction differs from the working copy's.
export function extractNotice(workspace, instruction) {
  if (!workspace || !instruction) return '';
  const known = workspace.base_instruction_sha256 && instruction.sha256;
  if (known ? workspace.base_instruction_sha256 === instruction.sha256 : text(workspace.base_instruction_version) === text(instruction.name)) return '';
  const under = workspace.base_instruction_version || 'another instruction';
  const revision = workspace.revision ? ` (revision ${workspace.revision})` : '';
  return `The working copy${revision} is under ${under}. This run becomes a separate version and is not merged into it; using it as the base replaces the working copy.`;
}

// The rebase dialog's list of what stops applying, from GET /api/deal/<slug>/rebase?to=<id>.
export function rebaseLines(preview) {
  if (!preview?.stops_applying) return [];
  const { revisions, edits, row_marks: marks, finding_decisions: findings, row_threads: threads } = preview.stops_applying;
  const current = preview.current || {}, target = preview.target || {};
  const revision = current.revision ?? 0;
  const agree = (n, one, many) => n === 1 ? one : many;
  const lines = [];
  lines.push(revisions ? `${count(revisions, 'revision')} saved on the current base (${count(edits || 0, 'edit')} to its rows) ${agree(revisions, 'stops', 'stop')} applying. ${agree(revisions, 'It stays', 'They stay')} in History; restoring revision ${revision}, not revision 0, brings ${agree(revisions, 'it', 'them')} back.`
    : 'No revisions have been saved on the current base.');
  if (marks?.total) lines.push(`${count(marks.total, 'row mark')} ${agree(marks.total, 'stops', 'stop')} applying (${[marks.reviewed && `${marks.reviewed} reviewed`, marks.needs_decision && `${marks.needs_decision} needs decision`, marks.unreviewed && `${marks.unreviewed} unreviewed`].filter(Boolean).join(', ')}).`);
  if (findings?.total) lines.push(`${count(findings.judgments_kept, 'finding judgment')} ${agree(findings.judgments_kept, 'carries', 'carry')} over${findings.reset ? `; the implementation and verification of ${findings.reset} reset` : ''}${findings.total > findings.judgments_kept ? `; ${findings.total - findings.judgments_kept} unjudged decision${findings.total - findings.judgments_kept === 1 ? '' : 's'} stop applying` : ''}.`);
  if (threads?.total) lines.push(`${count(threads.total, 'row thread')} (${threads.open} open) ${agree(threads.total, 'stays', 'stay')} with the old rows and ${agree(threads.total, 'reads', 'read')} “on an earlier base (revision ${revision})”.`);
  if (preview.deal_review?.actor && preview.deal_review.status !== 'unreviewed') lines.push(`The deal’s review status stays, marked as edited since revision ${preview.deal_review.revision}.`);
  return lines;
}
