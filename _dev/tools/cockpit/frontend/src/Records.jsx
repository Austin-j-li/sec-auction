import React, { useEffect, useRef, useState } from 'react';
import { Button, Field, Input, Select, Textarea } from '@fluentui/react-components';
import { ArrowDownIcon, ArrowsSplitIcon, ArrowUpIcon, ChatCircleIcon, CheckSquareIcon, InfoIcon, ListChecksIcon, PlusIcon, QuotesIcon, SquareIcon, TrashIcon, WarningIcon } from '@phosphor-icons/react';
import SplitPane from './SplitPane';
import Comments from './Comments';
import { count, recordValues, rowId, sheetColumns, sheetRows, text } from './api';
import { addPart, listControl, offListValue, OTHER } from './choices';
import { pickRows } from './bulk';
import { changedByOther, displayName, initials, shortTime } from './trace';
import { Dot, Empty, SeverityGlyph } from './ui';

const LONG_FIELDS = new Set(['Note', 'Quote and page', 'Reviewer note', 'Question', 'Recommended answer', 'Why, with page', 'Rows affected', 'What changes if answered differently', 'How opened', 'Who was in', 'Due dates', 'Deadline outcome', 'Bids received', 'How it ended', 'Value']);
const DATE_FIELDS = new Set(['Sort date', 'Date from', 'Date to', 'Opened']);
const NUMERIC_FIELDS = new Set(['#', 'Process', 'Count', 'Price low', 'Price high', 'CVR/earnout value']);
const MONO_FIELDS = new Set(['#', 'When', 'Sort date', 'Date from', 'Date to', 'Opened', 'Process', 'Round', 'Price low', 'Price high', 'CVR/earnout value', 'Count', 'Page', 'Q']);
const EVIDENCE_FIELD = 'Quote and page';
const SEVERITY_RANK = { error: 0, warning: 1, info: 2 };
const ISSUE_CAP = 5;

export function compact(value, length = 118) {
  const s = text(value);
  return s.length > length ? `${s.slice(0, length - 1)}…` : s;
}

function isMonoField(field) {
  return field !== EVIDENCE_FIELD && (MONO_FIELDS.has(field) || /date|price|count|page/i.test(field));
}

function revealSelectedListItem(container, selector, horizontalChild = null) {
  const target = container?.querySelector(selector);
  if (!container || !target) return;
  if (container.parentElement?.classList.contains('split-horizontal')) {
    const scroller = horizontalChild ? container.querySelector(horizontalChild) : container;
    if (!scroller) return;
    const item = target.getBoundingClientRect(), view = scroller.getBoundingClientRect();
    if (item.left < view.left + 12) scroller.scrollLeft += item.left - view.left - 12;
    else if (item.right > view.right - 12) scroller.scrollLeft += item.right - view.right + 12;
  } else {
    const item = target.getBoundingClientRect(), view = container.getBoundingClientRect();
    const head = container.querySelector('.section-head')?.getBoundingClientRect().height || 0;
    if (item.top < view.top + head + 12 || item.bottom > view.bottom - 12) container.scrollTop += item.top - view.top - head - Math.min(90, container.clientHeight * 0.22);
  }
}

function useRevealSelected(listRef, selector, horizontalChild, selectedKey) {
  useEffect(() => {
    const container = listRef.current;
    if (!container) return;
    const reveal = () => revealSelectedListItem(container, selector, horizontalChild);
    const frame = requestAnimationFrame(reveal);
    const observer = new ResizeObserver(reveal);
    observer.observe(container);
    return () => { cancelAnimationFrame(frame); observer.disconnect(); };
  }, [selectedKey]);
}

function sortedIssues(issues) {
  return [...(issues || [])].sort((a, b) => (SEVERITY_RANK[a.severity] ?? 2) - (SEVERITY_RANK[b.severity] ?? 2));
}

function worstSeverityByField(issues) {
  const map = new Map();
  for (const issue of sortedIssues(issues)) if (issue.column && !map.has(issue.column)) map.set(issue.column, issue.severity || 'info');
  return map;
}

// One ruled list: severity glyph, checker code in mono, message. Errors first; capped at five rows.
function Issues({ issues, pageHint }) {
  const [expanded, setExpanded] = useState(false);
  const list = sortedIssues(issues);
  if (pageHint) list.push({ severity: 'info', message: pageHint });
  if (!list.length) return null;
  const shown = expanded ? list : list.slice(0, ISSUE_CAP);
  return <div className="issues">
    <ul>
      {shown.map((issue, i) => <li key={i} className={`issue ${issue.severity || 'info'}`} data-field={issue.column || undefined}>
        <SeverityGlyph severity={issue.severity} size={16}/>
        <code className="issue-code">{issue.code || issue.severity || 'info'}</code>
        <span className="issue-message">{issue.column && <span className="issue-column">{issue.column} · </span>}{issue.message}</span>
      </li>)}
    </ul>
    {list.length > ISSUE_CAP && <Button appearance="subtle" className="text-button" onClick={() => setExpanded(value => !value)}>
      {expanded ? 'Show fewer' : `Show ${list.length - ISSUE_CAP} more`}
    </Button>}
  </div>;
}

export function fieldLabel(field, severity, dirty) {
  if (!severity && !dirty) return field;
  return {
    children: <>
      {field}
      {severity && <span className="label-glyph" aria-hidden="true"><SeverityGlyph severity={severity} size={12}/></span>}
      {dirty && <span className="edited-mark" aria-hidden="true"> · edited</span>}
    </>,
  };
}

// Last changed by: hidden until the field is hovered or focused; links to that revision in History.
function FieldAuthor({ author, field, onOpenRevision }) {
  if (!author?.actor) return null;
  const label = [displayName(author.actor), author.at && shortTime(author.at), author.revision != null && `revision ${author.revision}`].filter(Boolean).join(' · ');
  return <span className="field-author">
    <Button appearance="subtle" className="link-button" aria-label={`${field} last changed by ${label}; open history`} onClick={() => onOpenRevision?.(author.revision)}>{label}</Button>
  </span>;
}

// Initials of the other person who changed this row since the reader's last visit, and its open-thread count.
function RowMarks({ trace, uid }) {
  const other = changedByOther(trace?.authors?.[uid], trace?.user, trace?.seenRevision);
  const open = trace?.counts?.[uid]?.open || 0;
  if (!other && !open) return null;
  return <span className="row-marks mono">
    {other && <span className="initials-mark" title={`Changed by ${displayName(other)} since your last visit`}>{initials(other)}</span>}
    {open > 0 && <span className="thread-mark" title={count(open, 'open thread')}><ChatCircleIcon size={12} aria-hidden="true"/>{open}<span className="sr-only"> open threads</span></span>}
  </span>;
}

function RecordForm({ sheet, columns, row, choices, editable, onEdit, dirtyFields, authors, onOpenRevision }) {
  const values = recordValues(row, sheet);
  // Listed fields the reader switched to free text with Other… ('other') or back with "Choose from the list"
  // ('list'), for this record only.
  const [modes, setModes] = useState(() => new Map());
  useEffect(() => setModes(new Map()), [row.uid]);
  const setMode = (field, mode) => setModes(current => new Map(current).set(field, mode));
  const severities = worstSeverityByField(row.issues);
  const ordered = columns.includes(EVIDENCE_FIELD) ? [EVIDENCE_FIELD, ...columns.filter(field => field !== EVIDENCE_FIELD)] : columns;
  return <div className="field-grid">
    {ordered.map(field => {
      const rawChoices = choices?.[field] || choices?.[sheet]?.[field];
      const options = Array.isArray(rawChoices) ? rawChoices : null;
      const value = text(values[field]);
      const isDate = DATE_FIELDS.has(field);
      const isNumber = NUMERIC_FIELDS.has(field) && field !== '#' && field !== 'Round';
      const isEvidence = field === EVIDENCE_FIELD;
      const isLong = LONG_FIELDS.has(field) || value.length > 140;
      const dirty = Boolean(dirtyFields?.has(field));
      const hint = field === 'Count' ? 'Counts whole-company bidder units. Leave blank when the event has no bidder count or the figure is qualified.'
        : field === 'Sort date' ? 'Excel date used to order events.'
        : isEvidence ? 'Exact source wording and printed page; select filing text to fill.'
        : undefined;
      const change = (_, data) => onEdit(sheet, row.uid, field, data.value);
      const control = listControl(field, value, options, modes.get(field));
      const offList = control === 'select' ? offListValue(value, options) : null;
      let input, picker = null;
      if (control === 'select') {
        input = <Select value={value} disabled={!editable} onChange={(event, data) => data.value === OTHER ? setMode(field, 'other') : change(event, data)}>
          {offList && <option value={offList}>{offList} (not on the list)</option>}
          <option value="">Blank</option>
          {options.map(option => <option key={option} value={option}>{option}</option>)}
          <option value={OTHER}>Other…</option>
        </Select>;
      } else if (control === 'multi') {
        // One outcome per deadline, "A; B": typed freely, or built by adding listed values (the picker sits
        // outside the Field, so the text box alone carries the field's label).
        input = <Input value={value} disabled={!editable} onChange={change}/>;
        picker = <Select className="add-part" aria-label={`Add a ${field} value`} value="" disabled={!editable} onChange={(_, data) => { if (data.value) onEdit(sheet, row.uid, field, addPart(value, data.value)); }}>
          <option value="">Add an outcome…</option>
          {options.map(option => <option key={option} value={option}>{option}</option>)}
        </Select>;
      } else if (isLong) {
        input = <Textarea value={value} disabled={!editable} resize="none" className={`resizable-textarea ${isEvidence ? 'serif-textarea' : ''}`} rows={value.length > 350 ? 5 : 3} onChange={change}/>;
      } else {
        input = <Input
          type={isDate && /^\d{4}-\d{2}-\d{2}$/.test(value) ? 'date' : 'text'}
          inputMode={isNumber ? 'decimal' : undefined}
          value={value}
          input={isMonoField(field) ? { className: 'mono' } : undefined}
          disabled={!editable || (sheet === 'Deal ledger' && field === '#')}
          onChange={change}/>;
      }
      const classes = ['field-cell', isLong && 'span-all', isEvidence && 'evidence-field', dirty && 'is-dirty'].filter(Boolean).join(' ');
      const chooseFromList = <Button appearance="subtle" className="link-button" disabled={!editable} onClick={() => setMode(field, 'list')}>Choose from the list</Button>;
      const listHint = offList ? 'Not on this version’s list; pick a listed value to replace it'
        : control === 'text' && (modes.get(field) === 'other' ? chooseFromList : <>Not on this version’s list. {chooseFromList}</>);
      return <div key={field} className={classes}>
        <Field label={fieldLabel(field, severities.get(field), dirty)} hint={hint || listHint || undefined}>{input}</Field>
        {picker}
        <FieldAuthor author={authors?.[field]} field={field} onOpenRevision={onOpenRevision}/>
      </div>;
    })}
  </div>;
}

// In select mode (picked is true or false) a click picks the event for a bulk edit instead of opening it.
function EventSummary({ row, selected, onClick, review, trace, picked = null }) {
  const c = row.cells || {};
  const isNew = row.uid.startsWith('new-');
  const date = c.When || 'Date unstated';
  const detail = [c.Who, c.Process && `Process ${c.Process}`, c.Round !== '' && c.Round != null && `Round ${c.Round}`].filter(Boolean).join(' · ');
  const reviewLabel = review?.status === 'reviewed' ? 'Reviewed' : review?.status === 'needs_decision' ? 'Needs decision' : '';
  const picking = picked !== null;
  return <button id={`row-${rowId(row)}`} className={`event-item ${selected ? 'selected' : ''} ${picked ? 'picked' : ''}`} onClick={onClick}
    aria-pressed={picking ? picked : undefined} onMouseDown={picking ? event => { if (event.shiftKey) event.preventDefault(); } : undefined}>
    <span className="event-line">
      {picking && <span className="pick-mark" aria-hidden="true">{picked ? <CheckSquareIcon size={14} weight="fill"/> : <SquareIcon size={14}/>}</span>}
      {isNew
        ? <span className="event-number mono tone-warning"><Dot tone="warning"/> New</span>
        : <span className="event-number mono">#{rowId(row)}</span>}
      <span className="event-date mono" title={date}>{date}</span>
      <RowMarks trace={trace} uid={row.uid}/>
      {row.quote && (row.quote.located
        ? <span className="quote-location mono">{row.quote.found_page ? `p. ${row.quote.found_page}` : 'located'}</span>
        : <span className="quote-location missing"><WarningIcon size={12} className="tone-warning" aria-hidden="true"/> no quote</span>)}
      {reviewLabel && <span className="event-review"><Dot tone={review.status === 'reviewed' ? 'success' : 'warning'} title={reviewLabel}/><span className="sr-only">{reviewLabel}</span></span>}
    </span>
    <span className="event-text" title={[c.Event, detail].filter(Boolean).join(' · ')}>
      <strong>{c.Event || 'Untitled event'}</strong>
      {detail && <span className="event-detail">{detail}</span>}
    </span>
  </button>;
}

function QuestionLinks({ flag, questions, onOpen }) {
  const ids = [...new Set([...text(flag).matchAll(/\b[QR]\d+\b/gi)].map(match => match[0].toUpperCase()))];
  const linked = ids.map(id => questions.find(question => text(question.id).toUpperCase() === id || text(question.cells?.Q).toUpperCase() === id)).filter(Boolean);
  if (!linked.length) return null;
  return <div className="reference-links">
    <span className="reference-label">Linked questions and review items</span>
    {linked.map(question => {
      const id = question.id || question.cells?.Q;
      return <Button key={question.uid} appearance="subtle" className="link-button" aria-label={`Open question ${id}`} onClick={() => onOpen(question.uid)}>
        <span className="mono">{id}</span>{' · '}{compact(question.cells?.Question, 58)}
      </Button>;
    })}
  </div>;
}

function ReferenceLinks({ value, deal, onJumpRow }) {
  const source = text(value), numbers = new Set();
  for (const match of source.matchAll(/#?(\d+)\s*(?:-|–|to)\s*#?(\d+)/g)) {
    const start = Number(match[1]), end = Number(match[2]);
    if (end >= start && end - start <= 50) for (let n = start; n <= end; n++) numbers.add(n);
  }
  for (const match of source.matchAll(/(?:^|[,;\s])#?(\d+)\b/g)) numbers.add(Number(match[1]));
  const rows = deal.ledger?.rows?.filter(row => numbers.has(Number(rowId(row)))) || [];
  if (!rows.length) return null;
  return <div className="reference-links">
    <span className="reference-label">Referenced events</span>
    {rows.map(row => <Button key={row.uid} appearance="subtle" className="link-button" onClick={() => onJumpRow(row.uid, true)}>
      <span className="mono">#{rowId(row)}</span>{' '}{row.cells?.Event}
    </Button>)}
  </div>;
}

function RecordActions({ editable, canUp, canDown, onUp, onDown, onClone, onDelete }) {
  if (!editable) return null;
  return <div className="record-actions">
    <Button appearance="subtle" disabled={!canUp} icon={<ArrowUpIcon size={16}/>} onClick={onUp}>Move up</Button>
    <Button appearance="subtle" disabled={!canDown} icon={<ArrowDownIcon size={16}/>} onClick={onDown}>Move down</Button>
    {onClone && <Button appearance="subtle" icon={<ArrowsSplitIcon size={16}/>} onClick={onClone}>Clone to split</Button>}
    <Button appearance="subtle" className="danger" icon={<TrashIcon size={16}/>} onClick={onDelete}>Delete</Button>
  </div>;
}

function SourceSummary({ row, onShowFiling }) {
  const quote = row.quote;
  return <div className="source-summary">
    {quote?.located
      ? <span className="source-status"><QuotesIcon size={16} className="tone-quote" aria-hidden="true"/>
          <span>Quote located{quote.found_page && <> · <span className="mono">p. {quote.found_page}</span></>}{quote.occurrences > 1 && <> · <span className="mono">{quote.occurrences}</span> occurrences</>}</span>
        </span>
      : row.cells?.[EVIDENCE_FIELD]
        ? <span className="source-status"><WarningIcon size={16} className="tone-warning" aria-hidden="true"/><span>Quote not located in the filing</span></span>
        : <span className="source-status"><InfoIcon size={16} className="tone-muted" aria-hidden="true"/><span>No quote recorded</span></span>}
    {quote?.located && <Button appearance="secondary" onClick={() => onShowFiling(row.uid)}>Show in filing</Button>}
  </div>;
}

export function LedgerTab({ deal, selectedUid, onSelect, onShowFiling, onOpenQuestion, onStep, onAdd, onMove, onDelete, onEdit, onReview, onBulk, editable, selection, dirtyFor, reviewDirty, trace }) {
  const rows = deal.ledger?.rows || [];
  const index = rows.findIndex(row => row.uid === selectedUid);
  const row = selection || rows[0];
  const review = row ? deal.row_review?.[row.uid] || { status: 'unreviewed' } : null;
  const reviewTouched = row ? reviewDirty(row.uid) : new Set();
  const editorRef = useRef(null);
  const listRef = useRef(null);
  useEffect(() => { if (editorRef.current) editorRef.current.scrollTop = 0; }, [row?.uid]);
  useRevealSelected(listRef, '.event-item.selected', '.event-list', row?.uid);
  // Select mode picks events for a bulk Process/Round edit; null outside it. Picks of rows since removed are ignored.
  const [picked, setPicked] = useState(null);
  const anchor = useRef(null);
  const picking = Boolean(editable && onBulk && picked);
  const pickedRows = picking ? rows.filter(item => picked.has(item.uid)) : [];
  const togglePicking = () => { setPicked(picking ? null : new Set()); anchor.current = null; };
  function pick(uid, extend) {
    setPicked(current => pickRows(rows.map(item => item.uid), current, anchor.current, uid, extend));
    anchor.current = uid;
  }

  return <SplitPane className="ledger-layout" name="Event list and editor" storageKey="ledger" mobileStack mobileDefaultSize={128} defaultSize={250} minStart={140} minEnd={360}>
    <div className="record-list" ref={listRef}>
      <div className={`section-head ${picking ? 'picking' : ''}`}>
        <h2>Events</h2>
        <span className="head-count mono">{count(rows.length, 'event')}</span>
        {editable && onBulk && rows.length > 0 && <Button appearance="subtle" className="pick-toggle" icon={<ListChecksIcon size={16}/>} aria-pressed={picking} title={picking ? 'Leave select mode' : 'Select events to set Process or Round on several at once'} onClick={togglePicking}>{picking ? 'Done' : 'Select'}</Button>}
        {editable && !picking && <Button appearance="secondary" icon={<PlusIcon size={16}/>} onClick={() => onAdd('Deal ledger')}>Add</Button>}
        {picking && <div className="pick-bar" role="toolbar" aria-label="Selected events">
          <span className="pick-count mono" aria-live="polite">{pickedRows.length} selected</span>
          <Button appearance="subtle" className="link-button" onClick={() => setPicked(new Set(rows.map(item => item.uid)))}>All</Button>
          <Button appearance="subtle" className="link-button" disabled={!pickedRows.length} onClick={() => setPicked(new Set())}>None</Button>
          <Button appearance="secondary" disabled={!pickedRows.length} onClick={() => onBulk(pickedRows.map(item => item.uid))}>Set Process/Round…</Button>
          <span className="pick-hint">Shift-click selects a range</span>
        </div>}
      </div>
      <div className="event-list">
        {rows.length
          ? rows.map(item => <EventSummary key={item.uid} row={item} selected={item.uid === row?.uid} review={deal.row_review?.[item.uid]} trace={trace}
              picked={picking ? picked.has(item.uid) : null} onClick={event => picking ? pick(item.uid, event.shiftKey) : onSelect(item.uid)}/>)
          : <Empty>No events in this ledger. Add the first event to begin.</Empty>}
      </div>
    </div>
    <div className="record-editor" ref={editorRef}>
      {row ? <>
        <div className="editor-head">
          <div>
            <h2><span className="record-id mono">{row.uid.startsWith('new-') ? 'New' : `#${rowId(row)}`}</span> {row.cells?.Event || 'event'}</h2>
            <p><span className="mono">{row.cells?.When || 'Date unstated'}</span>{row.cells?.Who ? ` · ${row.cells.Who}` : ''}</p>
          </div>
          <div className="editor-nav">
            <Button appearance="subtle" className="icon-button" aria-label="Previous event" icon={<ArrowUpIcon size={16}/>} disabled={index <= 0} onClick={() => onStep(-1)}/>
            <Button appearance="subtle" className="icon-button" aria-label="Next event" icon={<ArrowDownIcon size={16}/>} disabled={index < 0 || index >= rows.length - 1} onClick={() => onStep(1)}/>
          </div>
        </div>
        <RecordActions editable={editable} canUp={index > 0} canDown={index >= 0 && index < rows.length - 1}
          onUp={() => onMove('Deal ledger', row.uid, -1)} onDown={() => onMove('Deal ledger', row.uid, 1)}
          onClone={() => onAdd('Deal ledger', row.uid)} onDelete={() => onDelete('Deal ledger', row.uid)}/>
        <SourceSummary row={row} onShowFiling={onShowFiling}/>
        <Issues key={row.uid} issues={row.issues} pageHint={deal.pages_reliable ? row.page_hint : null}/>
        <RecordForm sheet="Deal ledger" columns={deal.ledger.columns} row={row} choices={deal.choices} editable={editable} onEdit={onEdit} dirtyFields={dirtyFor('Deal ledger', row.uid)} authors={trace?.authors?.[row.uid]} onOpenRevision={trace?.onOpenRevision}/>
        <QuestionLinks flag={row.cells?.Flag} questions={deal.questions?.rows || []} onOpen={onOpenQuestion}/>
        <section className="review-box">
          <h3>Row review</h3>
          <div className="review-fields">
            <Field label={fieldLabel('Status', null, reviewTouched.has('status'))} className={reviewTouched.has('status') ? 'is-dirty' : ''} hint="Records a reader’s judgment; it does not certify that the filing is complete.">
              <Select value={review.status || 'unreviewed'} disabled={!editable} onChange={(_, data) => onReview(row.uid, data.value)}>
                <option value="unreviewed">Unreviewed</option>
                <option value="reviewed">Reviewed</option>
                <option value="needs_decision">Needs decision</option>
              </Select>
            </Field>
          </div>
        </section>
        {trace && <Comments key={row.uid} trace={trace} target={{ kind: 'row', sheet: 'Deal ledger', uid: row.uid }}/>}
      </> : <Empty>Select an event or add a new one.</Empty>}
    </div>
  </SplitPane>;
}

export function SheetTab({ deal, sheet, selectedUid, onSelect, onAdd, onMove, onDelete, onEdit, editable, onJumpRow, dirtyFor, trace }) {
  const rows = sheetRows(deal, sheet);
  const selected = rows.find(row => row.uid === selectedUid) || rows[0];
  const index = rows.findIndex(row => row.uid === selected?.uid);
  const columns = sheetColumns(deal, sheet);
  const editorRef = useRef(null), listRef = useRef(null);
  useEffect(() => { if (editorRef.current) editorRef.current.scrollTop = 0; }, [selected?.uid]);
  useRevealSelected(listRef, '.sheet-item.selected', null, selected?.uid);
  const noun = sheet === 'Deal facts' ? 'fact' : sheet === 'Questions' ? 'question' : 'round';

  return <div className="other-sheet">
    <div className="section-head">
      <h2>{sheet}</h2>
      <span className="head-count mono">{count(rows.length, noun)}</span>
      {editable && <Button appearance="secondary" icon={<PlusIcon size={16}/>} onClick={() => onAdd(sheet)}>Add row</Button>}
    </div>
    <SplitPane className="sheet-body" name={`${sheet} list and editor`} storageKey={`sheet.${sheet.toLowerCase().replaceAll(' ', '-')}`} mobileStack mobileDefaultSize={96} defaultSize={220} minStart={140} minEnd={360}>
      <div className="sheet-list" ref={listRef}>
        {rows.map(row => {
          const values = recordValues(row, sheet);
          const title = sheet === 'Deal facts' ? values.Field : sheet === 'Questions' ? values.Q || values.Question : `Process ${values.Process || '—'} · Round ${values.Round || '—'}`;
          const body = sheet === 'Deal facts' ? values.Value : sheet === 'Questions' ? values.Question : values['How opened'];
          return <button key={row.uid} className={`sheet-item ${row.uid === selected?.uid ? 'selected' : ''}`} onClick={() => onSelect(sheet, row.uid)}>
            <span className="sheet-item-head"><strong className={sheet === 'Deal facts' ? '' : 'mono'}>{title || 'New row'}</strong><RowMarks trace={trace} uid={row.uid}/></span>
            <span className="sheet-item-body" title={text(body)}>{text(body)}</span>
          </button>;
        })}
        {!rows.length && <Empty>No records on this sheet.</Empty>}
      </div>
      <div className="sheet-editor" ref={editorRef}>
        {selected ? <>
          <div className="editor-head">
            <h3>{sheet === 'Deal facts' ? selected.field || 'New fact' : sheet === 'Questions' ? selected.cells?.Q || 'New question' : `Round ${selected.cells?.Round || '—'}`}</h3>
          </div>
          <RecordActions editable={editable} canUp={index > 0} canDown={index < rows.length - 1}
            onUp={() => onMove(sheet, selected.uid, -1)} onDown={() => onMove(sheet, selected.uid, 1)}
            onDelete={() => onDelete(sheet, selected.uid)}/>
          <Issues key={selected.uid} issues={selected.issues}/>
          <RecordForm sheet={sheet} columns={columns} row={selected} choices={deal.choices} editable={editable} onEdit={onEdit} dirtyFields={dirtyFor(sheet, selected.uid)} authors={trace?.authors?.[selected.uid]} onOpenRevision={trace?.onOpenRevision}/>
          {sheet === 'Questions' && selected.cells?.['Rows affected'] && <ReferenceLinks value={selected.cells['Rows affected']} deal={deal} onJumpRow={onJumpRow}/>}
          {trace && <Comments key={`${sheet}:${selected.uid}`} trace={trace} target={{ kind: 'row', sheet, uid: selected.uid }}/>}
        </> : <Empty>Select a record or add one.</Empty>}
      </div>
    </SplitPane>
  </div>;
}
