import React from 'react';
import { Button, Field, Select, Textarea } from '@fluentui/react-components';
import { ArrowClockwiseIcon, CaretRightIcon, FileTextIcon, MinusIcon, PlusIcon } from '@phosphor-icons/react';
import { count, rowId, text } from './api';
import { Dot, Empty, Loading, Message, SeverityGlyph } from './ui';
import { fieldLabel } from './Records';

function labelStatus(value) { return text(value).replaceAll('_', ' '); }
export function friendlyDate(value) {
  if (!value) return '';
  const d = new Date(value);
  return Number.isNaN(d.getTime()) ? text(value) : d.toLocaleString();
}

const JUDGMENT_TONE = { unreviewed: 'muted', supported: 'success', rejected: 'error', deferred: 'warning' };
const VERDICT_TONE = { pass: 'success', pass_with_warnings: 'warning', fail: 'error' };
const CHANGE_TYPE = { update: 'Update', insert: 'Insert', delete: 'Delete', move: 'Move', restore: 'Restore', review: 'Review', finding: 'Finding' };

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
  const allIssues = [
    ...(deal.ledger?.rows || []).flatMap(row => (row.issues || []).map(issue => ({ ...issue, sheet: 'Deal ledger', row: rowId(row) }))),
    ...(deal.rounds?.rows || []).flatMap(row => (row.issues || []).map(issue => ({ ...issue, sheet: 'Rounds', row: row.excel_row }))),
    ...(deal.questions?.rows || []).flatMap(row => (row.issues || []).map(issue => ({ ...issue, sheet: 'Questions', row: rowId(row) }))),
    ...(check.other_issues || []),
  ];
  return <details className="mechanical-panel">
    <summary>
      <CaretRightIcon size={16} className="caret" aria-hidden="true"/>
      <span className="summary-title">Mechanical check</span>
      <span className="summary-meta mono">
        <span className={errors > 0 ? 'tone-error' : ''}>{count(errors, 'error')}</span>
        {' · '}{count(warningCount, 'warning')}{' · '}
        <span className={`verdict tone-${VERDICT_TONE[status] || 'muted'}`}><Dot tone={VERDICT_TONE[status] || 'muted'}/> {labelStatus(status)}</span>
      </span>
    </summary>
    <div className="mechanical-content">
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

function Finding({ finding, open, editable, dirty, onToggle, onEdit, onFindEvidence }) {
  const judgment = finding.judgment || 'unreviewed';
  const decision = finding.recorded_decision, correction = finding.recorded_correction;
  return <article className="finding">
    <button className="finding-title" onClick={onToggle} aria-expanded={open}>
      <span className="finding-heading">
        <strong>{finding.title || finding.id}</strong>
        <small>{[finding.source_label || finding.source_version, finding.rule].filter(Boolean).join(' · ')}{' · '}<span className="mono">{finding.id}</span></small>
      </span>
      <span className={`finding-state mono tone-${JUDGMENT_TONE[judgment] || 'muted'}`}><Dot tone={JUDGMENT_TONE[judgment] || 'muted'}/>{judgment}</span>
      <CaretRightIcon size={16} className="caret" aria-hidden="true"/>
    </button>
    {open && <div className="finding-body">
      <p>{finding.detail}</p>
      {finding.proposed_change && <div className="labelled">
        <h4 className="block-label">Recorded proposal</h4>
        <p>{finding.proposed_change}</p>
      </div>}
      {decision && <div className="labelled">
        <h4 className="block-label">Prior decision by {decision.actor}{decision.at && <> · <span className="mono">{decision.at}</span></>}</h4>
        <p>{decision.decision}</p>
      </div>}
      {correction && <div className="labelled">
        <h4 className="block-label">Prior correction{correction.actor ? ` by ${correction.actor}` : ''}</h4>
        <p className="meta-line">{[correction.status && labelStatus(correction.status), correction.version, correction.source_document].filter(Boolean).join(' · ')}</p>
        {correction.scope && <p>{correction.scope}</p>}
        {correction.qualification && <p>{correction.qualification}</p>}
      </div>}
      {finding.needs_recheck && <Message type="warning" title="This finding needs rechecking against the displayed version."/>}
      {finding.evidence?.length > 0 && <div className="finding-evidence labelled">
        <h4 className="block-label">Recorded evidence</h4>
        {finding.evidence.map((evidence, index) => <figure key={index}>
          <blockquote><mark className="quote-mark">{evidence.quote}</mark></blockquote>
          <figcaption>
            <cite className="mono">{evidence.page ? `p. ${evidence.page}` : 'Page not recorded'}</cite>
            {evidence.quote && <Button appearance="subtle" className="link-button" onClick={() => onFindEvidence(evidence)}>Find quote in filing</Button>}
          </figcaption>
        </figure>)}
      </div>}
      {finding.source_rows?.length > 0 && <div className="source-rows labelled">
        <h4 className="block-label">Source row references</h4>
        <p><span className="mono">{finding.source_rows.join(', ')}</span> · These refer to {finding.source_label || finding.source_version || 'the recorded source version'}.</p>
      </div>}
      <div className="decision-grid">
        <Field label={fieldLabel('Finding judgment', null, dirty.has('judgment'))} className={dirty.has('judgment') ? 'is-dirty' : ''}>
          <Select value={judgment} disabled={!editable} onChange={(_, data) => onEdit(finding.id, 'judgment', data.value)}>
            <option value="unreviewed">Unreviewed</option>
            <option value="supported">Supported</option>
            <option value="rejected">Rejected</option>
            <option value="deferred">Deferred</option>
          </Select>
        </Field>
        <Field label={fieldLabel('Correction implementation', null, dirty.has('implementation'))} className={dirty.has('implementation') ? 'is-dirty' : ''}>
          <Select value={finding.implementation || 'unassessed'} disabled={!editable} onChange={(_, data) => onEdit(finding.id, 'implementation', data.value)}>
            <option value="unassessed">Not assessed</option>
            <option value="not_applied">Not applied</option>
            <option value="applied">Applied</option>
          </Select>
        </Field>
        <Field label={fieldLabel('Verification', null, dirty.has('verification'))} className={dirty.has('verification') ? 'is-dirty' : ''}>
          <Select value={finding.verification || 'unchecked'} disabled={!editable} onChange={(_, data) => onEdit(finding.id, 'verification', data.value)}>
            <option value="unchecked">Unchecked</option>
            <option value="verified">Verified</option>
          </Select>
        </Field>
      </div>
      <Field label={fieldLabel('Decision note', null, dirty.has('note'))} className={dirty.has('note') ? 'is-dirty' : ''}>
        <Textarea resize="none" className="resizable-textarea" rows={3} value={finding.note || ''} disabled={!editable} onChange={(_, data) => onEdit(finding.id, 'note', data.value)}/>
      </Field>
      {finding.actor && <p className="audit-line mono">Last decision by {finding.actor}{finding.at ? ` · ${friendlyDate(finding.at)}` : ''}</p>}
    </div>}
  </article>;
}

export function ReviewTab({ deal, editable, open, onToggle, onEdit, dirtyFor, onFindEvidence, onOpenDocument }) {
  const findings = deal.findings || [], documents = deal.documents || [];
  return <div className="review-tab paper-column">
    <div className="section-head">
      <h2>Review findings</h2>
      <span className="head-count mono">{count(findings.length, 'recorded finding')}</span>
    </div>
    <p className="section-note">A finding is a recorded candidate or judgment. Deciding it here does not edit the workbook; a correction needs a separate data edit and verification.</p>
    <MechanicalPanel deal={deal}/>
    {documents.length > 0 && <div className="documents">
      <span className="reference-label">Recorded documents</span>
      {documents.map(item => <Button key={item.id} appearance="subtle" className="link-button" icon={<FileTextIcon size={16}/>} onClick={() => onOpenDocument(item)}>{item.label}</Button>)}
    </div>}
    {findings.length
      ? <div className="finding-list">
          {findings.map(finding => <Finding key={finding.id} finding={finding} open={open === finding.id} editable={editable} dirty={dirtyFor(finding.id)}
            onToggle={() => onToggle(open === finding.id ? null : finding.id)} onEdit={onEdit} onFindEvidence={onFindEvidence}/>)}
        </div>
      : <Empty>No recorded findings for this version.</Empty>}
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

export function ChangesTab({ data, loading }) {
  return <div className="changes-tab paper-column">
    <div className="section-head">
      <h2>Changes from base</h2>
      <span className="head-count">{data?.base_label ? `Compared with ${data.base_label}` : 'Working copy comparison'}</span>
    </div>
    {loading && <Loading label="Loading changes"/>}
    {!loading && !data?.changes?.length && <Empty>No differences from this working copy’s base.</Empty>}
    {!loading && data?.changes?.length > 0 && <div className="change-list">
      {data.changes.map((change, index) => <Change key={index} change={change}/>)}
    </div>}
  </div>;
}

export function HistoryTab({ data, loading, editable, onRestore, lastSaved }) {
  return <div className="history-tab paper-column">
    <div className="section-head">
      <h2>Revision history</h2>
      <span className="head-count">Restoring creates a new revision and preserves this record.</span>
    </div>
    {lastSaved && <p className="section-note">{lastSaved}</p>}
    {loading && <Loading label="Loading history"/>}
    {!loading && !data?.history?.length && <Empty>No saved revisions yet.</Empty>}
    {!loading && data?.history?.map(item => <article className="history-item" key={item.revision}>
      <div className="history-head">
        <div>
          <strong>Revision <span className="mono">{item.revision}</span></strong>
          {(item.at || item.actor) && <span className="mono">{[friendlyDate(item.at), item.actor].filter(Boolean).join(' · ')}</span>}
        </div>
        {editable && <Button appearance="secondary" icon={<ArrowClockwiseIcon size={16}/>} onClick={() => onRestore(item.revision)}>Restore</Button>}
      </div>
      <p>{item.reason || 'Saved edit'}</p>
      {item.summary && item.summary !== count(item.changes?.length || 0, 'change') && <div className="history-summary mono">{typeof item.summary === 'string' ? item.summary : JSON.stringify(item.summary)}</div>}
      {item.changes?.length > 0 && <details>
        <summary><CaretRightIcon size={16} className="caret" aria-hidden="true"/><span className="mono">{count(item.changes.length, 'change')}</span></summary>
        {item.changes.map((change, i) => <Change key={i} change={change}/>)}
      </details>}
    </article>)}
  </div>;
}

// Recorded documents read as text; only lines that look like typed tables are set in mono.
export function DocumentText({ value }) {
  const lines = text(value).split('\n');
  return <pre className="document-text">
    {lines.map((line, i) => <span key={i} className={/\S {2,}\S|\t|\|/.test(line) ? 'mono' : undefined}>{line}{i < lines.length - 1 ? '\n' : ''}</span>)}
  </pre>;
}
