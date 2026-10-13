import React, { useEffect } from 'react';
import { Button, Field, Select } from '@fluentui/react-components';
import { ArrowClockwiseIcon, CaretRightIcon, DownloadSimpleIcon, MinusIcon, PlusIcon } from '@phosphor-icons/react';
import Comments from './Comments';
import { count, rowId, text } from './api';
import { exportLinks } from './downloads';
import { Dot, Empty, Loading, Message, SeverityGlyph } from './ui';
import { importCheckText, liveCheckText } from './runs';

function labelStatus(value) { return text(value).replaceAll('_', ' '); }
export function friendlyDate(value) {
  if (!value) return '';
  const d = new Date(value);
  return Number.isNaN(d.getTime()) ? text(value) : d.toLocaleString();
}

const VERDICT_TONE = { pass: 'success', pass_with_warnings: 'warning', fail: 'error' };
const CHANGE_TYPE = { update: 'Update', insert: 'Insert', delete: 'Delete', move: 'Move', restore: 'Restore', review: 'Review' };

function IssueRow({ issue, location }) {
  return <li className={`issue ${issue.severity || 'info'}`}>
    <SeverityGlyph severity={issue.severity} size={16}/>
    <code className="issue-code">{location && <span className="issue-location">{location} · </span>}{issue.code || issue.severity}</code>
    <span className="issue-message">{issue.message}</span>
  </li>;
}

function MechanicalPanel({ deal }) {
  const check = deal.check || {}, summary = check.summary || {}, warnings = deal.workspace?.reference_warnings || [];
  const errors = summary.errors ?? check.errors ?? 0, warningCount = summary.warnings ?? check.warnings ?? 0;
  const status = check.status || 'not checked';
  // Which checker made the result on screen, and for an original what the checker found when it was imported.
  const selected = deal.workspace?.selected_version;
  const original = selected && selected !== 'working' ? deal.versions?.find(version => version.id === selected) : null;
  const allIssues = [
    ...(deal.ledger?.rows || []).flatMap(row => (row.issues || []).map(issue => ({ ...issue, sheet: 'Deal ledger', row: rowId(row) }))),
    ...(deal.rounds?.rows || []).flatMap(row => (row.issues || []).map(issue => ({ ...issue, sheet: 'Rounds', row: row.excel_row }))),
    ...(deal.questions?.rows || []).flatMap(row => (row.issues || []).map(issue => ({ ...issue, sheet: 'Questions', row: rowId(row) }))),
    ...(check.other_issues || []),
  ];
  return <details className="mechanical-panel">
    <summary title={liveCheckText(check)}>
      <CaretRightIcon size={16} className="caret" aria-hidden="true"/>
      <span className="summary-title">Mechanical check</span>
      <span className="summary-meta mono">
        <span className={errors > 0 ? 'tone-error' : ''}>{count(errors, 'error')}</span>
        {' · '}{count(warningCount, 'warning')}{' · '}
        <span className={`verdict tone-${VERDICT_TONE[status] || 'muted'}`}><Dot tone={VERDICT_TONE[status] || 'muted'}/> {labelStatus(status)}</span>
      </span>
    </summary>
    <div className="mechanical-content">
      <p className="checker-lines mono">{liveCheckText(check)}{original && <><br/>{importCheckText(original.checker)}</>}</p>
      <p className="fine-print">Automated checks cover workbook structure and selected consistency rules. They do not establish source completeness or human review.{check.scope_note ? ` ${check.scope_note}` : ''}</p>
      {warnings.length > 0 && <>
        <h4 className="block-label">Reference warnings</h4>
        <ul className="issue-list">
          {warnings.map((warning, i) => <IssueRow key={i} issue={{ severity: 'warning', code: warning.question || 'reference', message: warning.message || text(warning) }}/>)}
        </ul>
      </>}
      {allIssues.length > 0
        ? <ul className="issue-list">
            {allIssues.map((issue, i) => <IssueRow key={i} issue={issue} location={`${issue.sheet || 'Workbook'}${issue.row ? ` · ${issue.row}` : ''}`}/>)}
          </ul>
        : <p>No mechanical issues listed for this version.</p>}
    </div>
  </details>;
}

// Alex's must-flag list (voice notes ¶169–187): what each review_list.py category asks a person to check.
const FLAG_CATEGORIES = {
  unknown_type: ['Unknown type on a winner or Formal bidder', '175–176'],
  qualified_count: ['Count qualified or unsized in the Note', '177'],
  type_unsplit_count: ['Count that does not split bidder types', '177'],
  inferred_exit: ['Inferred exit', '178'],
  unexplained_exit: ['Exit with no stated reason', '178'],
  deadline_outcome: ['Deadline outcome', '174'],
  partial_only: ['Only partial bids', '184'],
  non_per_share_price: ['Price not per share', '185'],
  non_dollar_price: ['Currency not dollars', '185'],
  round_opened: ['Round start', '173'],
  multi_process: ['More than one process', '186'],
  conditions_unclear: ['Formal bid with Conditions Unclear', '179'],
  none_on_silence: ['Formal bid with Conditions None on silent columns', '179'],
  initiation_differs: ['Initiation differs from D5', '38–39, 68'],
};

function MustFlagPanel({ deal, onJumpRow }) {
  const queue = deal.review_queue;
  if (!queue) return null;
  const items = queue.items || [];
  const groups = (queue.categories || Object.keys(FLAG_CATEGORIES))
    .map(category => [category, items.filter(item => item.category === category)])
    .filter(([, list]) => list.length);
  const ledgerRows = new Map((deal.ledger?.rows || []).map(row => [rowId(row), row]));
  return <details className="mechanical-panel must-flag-panel">
    <summary>
      <CaretRightIcon size={16} className="caret" aria-hidden="true"/>
      <span className="summary-title">Must-flag list</span>
      <span className="summary-meta mono">{queue.error ? 'not available' : `${count(items.length, 'item')} · ${groups.length} of ${Object.keys(FLAG_CATEGORIES).length} checks`}</span>
    </summary>
    <div className="mechanical-content">
      <p className="fine-print">Cells Alex asked a person to look at (voice notes ¶169–187). The list is read from the workbook cells; it does not check them against the filing.</p>
      {queue.error && <Message type="warning" title="The must-flag list could not be built for this version." detail={queue.error}/>}
      {!queue.error && !groups.length && <p>No must-flag items in this version.</p>}
      {groups.map(([category, list]) => {
        const [label, paragraphs] = FLAG_CATEGORIES[category] || [category, ''];
        return <section key={category} className="flag-group">
          <h4 className="block-label">{label}{paragraphs ? ` · ¶${paragraphs}` : ''} <span className="mono">({list.length})</span></h4>
          <ul className="flag-list">
            {list.map((item, i) => {
              const row = item.sheet === 'Deal ledger' ? ledgerRows.get(text(item.row)) : null;
              return <li key={i}>
                {row?.uid && onJumpRow
                  ? <Button appearance="subtle" className="link-button" onClick={() => onJumpRow(row.uid)}><span className="mono">#{rowId(row)}</span>&nbsp;{row.cells?.Event}</Button>
                  : <span className="flag-location mono">{[item.sheet, item.row].filter(Boolean).join(' · ')}</span>}
                <span className="flag-detail">{[item.who, item.detail].filter(Boolean).join(' · ')}</span>
              </li>;
            })}
          </ul>
        </section>;
      })}
    </div>
  </details>;
}

export function ReviewTab({ deal, onJumpRow, trace }) {
  return <div className="review-tab paper-column">
    <MechanicalPanel deal={deal}/>
    <MustFlagPanel deal={deal} onJumpRow={onJumpRow}/>
    {trace && <div className="discussion"><Comments trace={trace} target={{ kind: 'deal' }} heading="Discussion"/></div>}
  </div>;
}

function ChangeValue({ value, tone }) {
  if (value && typeof value === 'object') {
    const entries = Array.isArray(value) ? value.map((item, i) => [String(i + 1), item]) : Object.entries(value);
    return <dl className={`change-fields ${tone}`}>
      {entries.map(([key, item]) => <div key={key}>
        <dt className="mono">{key}</dt>
        {item && typeof item === 'object'
          ? <dd>{JSON.stringify(item)}</dd>
          : text(item) ? <dd>{text(item)}</dd> : <dd className="blank">—</dd>}
      </div>)}
    </dl>;
  }
  return <div className={`change-text ${tone}`}>{text(value)}</div>;
}

function Change({ change }) {
  const hasBefore = change.before != null && change.before !== '';
  const hasAfter = change.after != null && change.after !== '';
  return <div className="change">
    <div className="change-head">
      <strong>{change.sheet || 'Record'}{change.record_label ? ` · ${change.record_label}` : change.uid ? ` · ${change.uid}` : ''}{change.field ? ` · ${change.field}` : ''}</strong>
      <span className="change-type mono">{CHANGE_TYPE[change.type] || text(change.type)}</span>
    </div>
    {(hasBefore || hasAfter) && <div className="change-body">
      {hasBefore && <>
        <span className="change-label"><MinusIcon size={12} className="tone-error" aria-hidden="true"/> Before</span>
        <ChangeValue value={change.before} tone="removed"/>
      </>}
      {hasAfter && <>
        <span className="change-label"><PlusIcon size={12} className="tone-success" aria-hidden="true"/> After</span>
        <ChangeValue value={change.after} tone="added"/>
      </>}
    </div>}
  </div>;
}

// Changes: the working copy against its base by default; "Compare" picks any two versions (rows matched by sheet key).
export function ChangesTab({ data, loading, compare, onCompare }) {
  const custom = compare && !compare.isDefault;
  const heading = custom ? 'Compare versions' : 'Changes from base';
  const note = custom
    ? [data?.from_label, data?.to_label].every(Boolean) ? `${data.from_label} → ${data.to_label}` : 'Version comparison'
    : data?.base_label ? `Compared with ${data.base_label}` : 'Working copy comparison';
  return <div className="changes-tab paper-column">
    <div className="section-head">
      <h2>{heading}</h2>
      <span className="head-count">{note}</span>
    </div>
    {compare?.options?.length > 1 && <div className="compare-controls" role="group" aria-label="Compare">
      <Field label="From"><Select value={compare.from} onChange={(_, value) => onCompare({ from: value.value, to: compare.to })}>
        {compare.options.map(item => <option key={item.id} value={item.id}>{item.label}</option>)}
      </Select></Field>
      <Field label="To"><Select value={compare.to} onChange={(_, value) => onCompare({ from: compare.from, to: value.value })}>
        {compare.options.map(item => <option key={item.id} value={item.id}>{item.label}</option>)}
      </Select></Field>
      {custom && <Button appearance="subtle" className="link-button" onClick={() => onCompare(null)}>Base against working copy</Button>}
    </div>}
    {custom && data?.same_instruction === false && <p className="section-note compare-note">These versions were made under different instructions, so some differences may come from the instruction rather than the extraction.</p>}
    {loading && <Loading label="Loading changes"/>}
    {!loading && !data?.changes?.length && <Empty>{custom ? 'No differences between these versions.' : 'No differences from this working copy’s base.'}</Empty>}
    {!loading && data?.changes?.length > 0 && <div className="change-list">
      {data.changes.map((change, index) => <Change key={index} change={change}/>)}
    </div>}
  </div>;
}

// A past revision downloads like the working copy: with the Source sheet, or its four sheets. The server names
// the file {slug}-working-r{N}.xlsx.
function RevisionDownloads({ slug, revision }) {
  const links = exportLinks(slug, `rev:${revision}`);
  return <>
    <Button as="a" appearance="subtle" className="link-button" icon={<DownloadSimpleIcon size={16}/>} href={links.href} title={links.title} download>Download</Button>
    <Button as="a" appearance="subtle" className="link-button" href={links.other.href} title={links.other.label} download>Four sheets</Button>
  </>;
}

// A past revision can be downloaded or compared with the working copy without restoring it (read only).
export function HistoryTab({ data, loading, editable, onRestore, lastSaved, focus, slug, onCompareRevision }) {
  useEffect(() => {
    if (!focus || !data) return;
    const frame = requestAnimationFrame(() => document.getElementById(`revision-${focus.revision}`)?.scrollIntoView({ block: 'start' }));
    return () => cancelAnimationFrame(frame);
  }, [focus?.nonce, data]);
  return <div className="history-tab paper-column">
    <div className="section-head">
      <h2>Revision history</h2>
      <span className="head-count">Restoring creates a new revision and preserves this record.</span>
    </div>
    {lastSaved && <p className="section-note">{lastSaved}</p>}
    {loading && <Loading label="Loading history"/>}
    {!loading && !data?.history?.length && <Empty>No saved revisions yet.</Empty>}
    {!loading && data?.history?.map(item => <article className={`history-item ${focus?.revision === item.revision ? 'focused' : ''}`} id={`revision-${item.revision}`} key={item.revision}>
      <div className="history-head">
        <div>
          <strong>Revision <span className="mono">{item.revision}</span></strong>
          {(item.at || item.actor) && <span className="mono">{[friendlyDate(item.at), item.actor].filter(Boolean).join(' · ')}</span>}
        </div>
        <div className="history-actions">
          {slug && <RevisionDownloads slug={slug} revision={item.revision}/>}
          {onCompareRevision && item.revision !== data.history[0]?.revision && <Button appearance="subtle" className="link-button" onClick={() => onCompareRevision(item.revision)}>Compare with working copy</Button>}
          {editable && <Button appearance="secondary" icon={<ArrowClockwiseIcon size={16}/>} onClick={() => onRestore(item.revision)}>Restore</Button>}
        </div>
      </div>
      <p>{item.reason || 'Saved edit'}</p>
      {item.summary && item.summary !== count(item.changes?.length || 0, 'change') && <div className="history-summary mono">{typeof item.summary === 'string' ? item.summary : JSON.stringify(item.summary)}</div>}
      {item.changes?.length > 0 && <details open={focus?.revision === item.revision || undefined}>
        <summary><CaretRightIcon size={16} className="caret" aria-hidden="true"/><span className="mono">{count(item.changes.length, 'change')}</span></summary>
        {item.changes.map((change, i) => <Change key={i} change={change}/>)}
      </details>}
    </article>)}
  </div>;
}
