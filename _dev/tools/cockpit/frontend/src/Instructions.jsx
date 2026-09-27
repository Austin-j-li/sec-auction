import React, { useCallback, useDeferredValue, useEffect, useMemo, useRef, useState } from 'react';
import { Button, Checkbox, Field, Input, Textarea } from '@fluentui/react-components';
import { CopySimpleIcon, FloppyDiskIcon, PaperPlaneTiltIcon, StarIcon, XIcon } from '@phosphor-icons/react';
import { count, instructionPath, instructionsAction, json, text } from './api';
import { defaultInstructionId, foldRows, inlineChange, instructionByline, isDraft, lineDiff, nameProblem, NOTE_MAX, noteProblem, orderInstructions, REMINDER, sha7, sideBySide, TEXT_MAX_BYTES, textBytes } from './instructions';
import { formatBytes } from './deals';
import { displayName, knownUser, shortTime } from './trace';
import { Dot, Empty, Loading, Message } from './ui';

// Instructions: every version of the extraction instruction. Published versions are frozen; drafts are edited here,
// published under a new name, and one published version is the default for new runs.

const STALE = 'Someone saved this draft since you opened it.';

function urlSelection() {
  const params = new URLSearchParams(location.search);
  const seq = params.get('seq');
  return { id: params.get('id'), seq: seq && /^\d+$/.test(seq) ? Number(seq) : null };
}
function writeUrl(id, seq) {
  const params = new URLSearchParams();
  if (id) params.set('id', id);
  if (id && seq != null) params.set('seq', seq);
  const query = params.toString();
  history.replaceState(null, '', `/instructions${query ? `?${query}` : ''}`);
}

export default function InstructionsPage({ session, onDirtyChange }) {
  const [list, setList] = useState(null);
  const [listError, setListError] = useState('');
  const [selectedId, setSelectedId] = useState(() => urlSelection().id);
  const [seq, setSeq] = useState(() => urlSelection().seq);
  const [detail, setDetail] = useState(null);
  const [detailError, setDetailError] = useState('');
  const [seqView, setSeqView] = useState(null);
  const [draftText, setDraftText] = useState('');
  const [saveState, setSaveState] = useState('');
  const [conflict, setConflict] = useState(false);
  const [busy, setBusy] = useState(false);
  const [actionError, setActionError] = useState('');
  const [publishing, setPublishing] = useState(false);
  const [view, setView] = useState('text');
  const serial = useRef(0);
  const canWrite = Boolean(session.can_edit && knownUser(session.user));

  const item = detail?.item?.id === selectedId ? detail.item : null;
  const draft = isDraft(item);
  const dirty = Boolean(draft && seq == null && detail && draftText !== text(detail.text));
  useEffect(() => { onDirtyChange?.(dirty); }, [dirty]);
  useEffect(() => () => onDirtyChange?.(false), []);
  useEffect(() => { document.title = 'Instructions · Ledger cockpit'; }, []);

  const loadList = useCallback(async () => {
    try {
      const data = await json('/api/instructions');
      setList(data || { items: [] }); setListError('');
      return data;
    } catch (err) {
      setListError(err.message);
      return null;
    }
  }, []);
  useEffect(() => {
    loadList().then(data => {
      if (!data) return;
      setSelectedId(current => current && data.items?.some(entry => entry.id === current) ? current : defaultInstructionId(data) || data.items?.[0]?.id || null);
    });
  }, [loadList]);

  // The selected version's current text (and, for drafts, the editor's starting text).
  const loadDetail = useCallback(async id => {
    const token = ++serial.current;
    setDetailError(''); setConflict(false); setSaveState('');
    try {
      const data = await json(instructionPath(id));
      if (token !== serial.current) return;
      setDetail(data); setDraftText(text(data?.text));
    } catch (err) {
      if (token === serial.current) { setDetail(null); setDetailError(err.message); }
    }
  }, []);
  useEffect(() => { if (selectedId) loadDetail(selectedId); }, [selectedId, loadDetail]);
  useEffect(() => { if (selectedId) writeUrl(selectedId, seq); }, [selectedId, seq]);
  // One edit from the history, read only.
  useEffect(() => {
    setSeqView(null);
    if (!selectedId || seq == null) return;
    let alive = true;
    json(instructionPath(selectedId, seq))
      .then(data => { if (alive) setSeqView({ seq, text: text(data?.text), parent_text: data?.parent_text ?? null }); })
      .catch(err => { if (alive) setSeqView({ seq, error: err.message }); });
    return () => { alive = false; };
  }, [selectedId, seq]);

  function select(id) {
    if (id === selectedId && seq == null) return;
    if (dirty && !window.confirm('This draft has unsaved changes. Discard them and open another version?')) return;
    setActionError(''); setSeq(null);
    if (id !== selectedId) { setDetail(null); setSelectedId(id); setView('text'); }
  }
  function applyDetail(data) {
    setDetail(data); setDraftText(text(data?.text)); setConflict(false);
    if (data?.item?.id && data.item.id !== selectedId) { setSelectedId(data.item.id); setSeq(null); setView('text'); }
  }
  async function act(action, after) {
    setBusy(true); setActionError('');
    try {
      const data = await instructionsAction(session, action);
      after(data);
      return true;
    } catch (err) {
      setActionError(err.message);
      return false;
    } finally {
      setBusy(false);
    }
  }
  async function save() {
    if (!dirty || saveState === 'saving' || conflict) return;
    setSaveState('saving'); setActionError('');
    try {
      const data = await instructionsAction(session, { action: 'save', id: item.id, text: draftText, base_sha256: item.sha256 });
      setDetail(data); setDraftText(text(data?.text)); setSaveState('saved');
      loadList();
    } catch (err) {
      setSaveState('');
      if (err.status === 409) setConflict(true);
      else setActionError(`The draft could not be saved: ${err.message}`);
    }
  }
  function reload() {
    if (dirty && !window.confirm('Reloading replaces your text with the saved draft. Copy anything you want to keep first. Reload now?')) return;
    loadDetail(item.id); loadList();
  }
  function newDraft() {
    if (dirty && !window.confirm('This draft has unsaved changes. Discard them and start a new draft?')) return;
    act({ action: 'draft', from: item.id }, data => { applyDetail(data); loadList(); });
  }
  function makeDefault() {
    if (!window.confirm(`Make ${item.label || item.name} the default instruction? New extractions will preselect it; runs already started keep theirs.`)) return;
    act({ action: 'default', id: item.id }, data => { if (data?.items) setList(data); else loadList(); loadDetail(item.id); });
  }
  async function publish(name, note) {
    return act({ action: 'publish', id: item.id, name, note }, data => { applyDetail(data); setPublishing(false); loadList(); });
  }

  const items = orderInstructions(list?.items);
  const parent = item?.parent_id ? items.find(entry => entry.id === item.parent_id) : null;
  const parentLabel = item?.parent_label || parent?.label || item?.parent_id;
  const edits = detail?.history || [];
  const bytes = draft ? textBytes(draftText) : 0;
  const tooLarge = bytes > TEXT_MAX_BYTES;
  const shownText = seq != null ? seqView?.text : draft ? draftText : text(detail?.text);
  const shownParent = seq != null ? seqView?.parent_text ?? detail?.parent_text : detail?.parent_text;
  const hasParent = shownParent != null;
  const entry = seq != null ? edits.find(edit => edit.seq === seq) : null;

  return <>
    <div className="overview-title">
      <h1>Instructions</h1>
      <p>Each run gets exactly one instruction text, frozen when the run is requested. Published versions never change.</p>
    </div>
    {listError && <Message type="error" title="The instructions could not be loaded." detail={listError}/>}
    {!list && !listError && <Loading label="Loading instructions"/>}
    {list && <div className="instructions-layout">
      <nav className="instruction-list" aria-label="Instruction versions">
        {!items.length && <Empty>No instruction versions yet.</Empty>}
        <ul>
          {items.map(entry => <li key={entry.id}>
            <button type="button" className={`instruction-entry ${entry.id === selectedId ? 'selected' : ''}`} aria-current={entry.id === selectedId ? 'true' : undefined} onClick={() => select(entry.id)}>
              <strong>{entry.label || entry.name || entry.id}{entry.is_default && <span className="default-mark"><StarIcon size={12} weight="fill" aria-hidden="true"/>default</span>}</strong>
              <small><Dot tone={isDraft(entry) ? 'warning' : 'success'}/>{instructionByline(entry)}</small>
              {entry.parent_id && <small>from {entry.parent_label || entry.parent_id}</small>}
            </button>
          </li>)}
        </ul>
      </nav>
      <section className="instruction-detail" aria-live="polite">
        {detailError && <Message type="error" title="This version could not be loaded." detail={detailError}/>}
        {!item && !detailError && selectedId && <Loading label="Loading the version"/>}
        {item && <>
          <div className="section-head instruction-head">
            <h2>{item.label || item.name}</h2>
            <span className="instruction-status"><Dot tone={draft ? 'warning' : 'success'}/>{draft ? 'Draft' : 'Published'}{item.is_default ? ' · default' : ''}</span>
            {canWrite && <span className="instruction-actions">
              {!draft && !item.is_default && <Button appearance="secondary" icon={<StarIcon size={16}/>} disabled={busy} onClick={makeDefault}>Make default</Button>}
              <Button appearance="secondary" icon={<CopySimpleIcon size={16}/>} disabled={busy} onClick={newDraft}>New draft from this</Button>
              {draft && <Button appearance="primary" icon={<PaperPlaneTiltIcon size={16}/>} disabled={busy || dirty || seq != null} title={dirty ? 'Save the draft before publishing' : undefined} onClick={() => setPublishing(true)}>Publish…</Button>}
            </span>}
          </div>
          <dl className="settings-status instruction-meta">
            <div><dt>{draft ? 'Started' : 'Created'}</dt><dd><span>{displayName(item.created_by)} · <span className="mono">{shortTime(item.created_at)}</span></span></dd></div>
            {draft && item.updated_at && <div><dt>Last saved</dt><dd><span>{displayName(item.updated_by)} · <span className="mono">{shortTime(item.updated_at)}</span></span></dd></div>}
            {!draft && item.published_at && <div><dt>Published</dt><dd><span>{displayName(item.published_by)} · <span className="mono">{shortTime(item.published_at)}</span></span></dd></div>}
            {item.parent_id && <div><dt>Parent</dt><dd><button type="button" className="text-link" onClick={() => select(item.parent_id)}>{parentLabel}</button></dd></div>}
            <div><dt>SHA-256</dt><dd className="mono sha">{item.sha256}</dd></div>
            {edits.length > 0 && <div><dt>Edits</dt><dd>{count(edits.length, 'saved text')}</dd></div>}
          </dl>
          {item.note && <div className="instruction-note"><h3>Change note</h3><p>{item.note}</p></div>}
          {actionError && <p className="settings-error tone-error" role="alert">{actionError}</p>}

          {seq != null && <div className="history-view-line">
            <span>{entry ? <>Edit {entry.seq} by {displayName(entry.author)} · <span className="mono">{shortTime(entry.at)} · {sha7(entry.sha256)}</span></> : `Edit ${seq}`} · read only</span>
            <Button appearance="subtle" className="link-button" onClick={() => setSeq(null)}>{draft ? 'Back to the draft' : 'Back to the current text'}</Button>
          </div>}

          {draft && seq == null && canWrite && <p className="section-note reminder">{REMINDER}</p>}
          <div className="instruction-view-bar">
            {hasParent ? <div className="segmented" role="group" aria-label="View">
              <button type="button" className={view === 'text' ? 'active' : ''} aria-pressed={view === 'text'} onClick={() => setView('text')}>{draft && seq == null && canWrite ? 'Edit' : 'Text'}</button>
              <button type="button" className={view === 'diff' ? 'active' : ''} aria-pressed={view === 'diff'} onClick={() => setView('diff')}>Changes from {parentLabel}</button>
            </div> : <span className="section-note">{item.parent_id ? 'The parent text is not available.' : 'No parent version to compare with.'}</span>}
            {draft && seq == null && <span className={`work-state ${dirty ? 'unsaved' : ''}`}>
              <Dot tone={dirty ? 'warning' : saveState === 'saved' ? 'success' : 'muted'}/>{saveState === 'saving' ? 'Saving…' : dirty ? 'Unsaved changes' : saveState === 'saved' ? 'Saved' : 'No unsaved changes'}
            </span>}
            {draft && seq == null && canWrite && <Button appearance="primary" icon={<FloppyDiskIcon size={16}/>} disabled={!dirty || saveState === 'saving' || conflict || tooLarge} onClick={save}>Save draft</Button>}
          </div>
          {conflict && <Message type="warning" title={STALE}>
            <p>Your text is still in the editor but cannot be saved over theirs. Copy anything you want to keep, then reload to continue from the saved draft.</p>
            <div className="message-actions"><Button appearance="secondary" onClick={reload}>Reload the draft</Button></div>
          </Message>}
          {tooLarge && <p className="settings-error tone-error">The text is {formatBytes(bytes)}; an instruction can be at most {formatBytes(TEXT_MAX_BYTES)}.</p>}

          {seq != null && seqView?.error ? <Message type="error" title="This edit could not be loaded." detail={seqView.error}/>
            : seq != null && !seqView ? <Loading label={`Loading edit ${seq}`}/>
            : view === 'diff' && hasParent ? <DiffView before={shownParent} after={shownText} beforeLabel={parentLabel} afterLabel={seq != null ? `Edit ${seq}` : draft ? 'This draft' : item.label}/>
            : draft && seq == null && canWrite ? <Textarea className="instruction-editor" aria-label="Instruction text" value={draftText} resize="vertical" readOnly={saveState === 'saving'}
                onChange={(_, data) => { setDraftText(data.value); if (saveState === 'saved') setSaveState(''); }}
                onKeyDown={event => { if ((event.ctrlKey || event.metaKey) && event.key === 's') { event.preventDefault(); save(); } }}/>
            : <pre className="instruction-text">{shownText}</pre>}

          {edits.length > 0 && <div className="instruction-history">
            <h3>Edit history</h3>
            <ol>
              {[...edits].reverse().map((edit, index) => <li key={edit.seq} className={edit.seq === seq ? 'selected' : ''}>
                <span><strong>Edit {edit.seq}</strong>{edit.seq === 1 ? ' · started' : ''}{index === 0 ? ' · current text' : ''}</span>
                <span>{displayName(edit.author)} · <span className="mono">{shortTime(edit.at)} · {sha7(edit.sha256)}</span></span>
                {edit.seq === seq ? <span className="tone-muted">Shown above</span>
                  : <Button appearance="subtle" className="link-button" onClick={() => { if (dirty && !window.confirm('Your unsaved text stays in the editor while you look. View this edit?')) return; setSeq(edit.seq); }}>View</Button>}
              </li>)}
            </ol>
          </div>}
        </>}
      </section>
    </div>}
    {publishing && item && <PublishDialog item={item} items={items} busy={busy} error={actionError} onPublish={publish} onClose={() => { setPublishing(false); setActionError(''); }}/>}
  </>;
}

// Side-by-side changes, parent on the left. Unchanged stretches fold unless "Show all lines" is ticked.
function DiffView({ before, after, beforeLabel, afterLabel }) {
  const deferred = useDeferredValue(after);
  const [all, setAll] = useState(false);
  const diff = useMemo(() => lineDiff(before, deferred), [before, deferred]);
  const rows = useMemo(() => { const full = sideBySide(diff.ops); return all ? full : foldRows(full, 2); }, [diff, all]);
  const changed = diff.added + diff.removed > 0;
  return <div className="diff-view">
    <div className="diff-summary">
      <span className="mono">{changed ? `${count(diff.removed, 'line')} removed · ${count(diff.added, 'line')} added` : 'No changes from the parent'}</span>
      {!diff.exact && <span className="tone-warning">Too many changes to match line by line; the changed stretch is shown as one block.</span>}
      {changed && <Checkbox label="Show all lines" checked={all} onChange={(_, data) => setAll(Boolean(data.checked))}/>}
    </div>
    {changed && <div className="diff-scroll">
      <table className="diff-table">
        <colgroup><col className="diff-num"/><col/><col className="diff-num"/><col/></colgroup>
        <thead><tr><th colSpan={2}>{beforeLabel}</th><th colSpan={2}>{afterLabel}</th></tr></thead>
        <tbody>
          {rows.map((row, index) => row.kind === 'gap'
            ? <tr key={index} className="diff-gap"><td colSpan={4}>{count(row.count, 'unchanged line')}</td></tr>
            : <DiffRow key={index} row={row}/>)}
        </tbody>
      </table>
    </div>}
  </div>;
}

function DiffRow({ row }) {
  const parts = row.kind === 'change' ? inlineChange(row.left.text, row.right.text) : null;
  const cell = (side, pieces, tone) => side
    ? <><td className="diff-n mono">{side.n}</td><td className={`diff-line ${tone}`}>{pieces ? <>{pieces[0]}<span className="diff-mid">{pieces[1]}</span>{pieces[2]}</> : side.text || ' '}</td></>
    : <><td className="diff-n"/><td className="diff-line diff-empty"/></>;
  const leftTone = row.kind === 'same' ? '' : 'diff-del', rightTone = row.kind === 'same' ? '' : 'diff-add';
  return <tr>{cell(row.left, parts?.left, leftTone)}{cell(row.right, parts?.right, rightTone)}</tr>;
}

function PublishDialog({ item, items, busy, error, onPublish, onClose }) {
  const [name, setName] = useState('');
  const [note, setNote] = useState('');
  const [tried, setTried] = useState(false);
  const ref = useRef(null);
  const nameError = nameProblem(name, items), noteError = noteProblem(note);
  useEffect(() => {
    const previous = document.activeElement;
    ref.current?.querySelector('input')?.focus();
    const onKeyDown = event => { if (event.key === 'Escape' && !busy) { event.preventDefault(); onClose(); } };
    window.addEventListener('keydown', onKeyDown);
    return () => { window.removeEventListener('keydown', onKeyDown); previous?.focus?.(); };
  }, [busy]);
  function submit(event) {
    event.preventDefault(); setTried(true);
    if (!nameError && !noteError) onPublish(name.trim(), note.trim());
  }
  return <div className="modal-backdrop" role="presentation">
    <div className="modal publish-modal" ref={ref} role="dialog" aria-modal="true" aria-label="Publish this draft">
      <div className="modal-head">
        <h2>Publish {item.label}</h2>
        <Button appearance="subtle" className="icon-button" onClick={onClose} aria-label="Close" icon={<XIcon size={16}/>}/>
      </div>
      <p>Publishing freezes this text under a name. It can then be chosen for runs or made the default; it can never be edited again. The draft’s current text has SHA-256 <span className="mono">{sha7(item.sha256)}</span>.</p>
      <form onSubmit={submit}>
        <Field label="Name" hint="Letters, digits, “.”, “-”, “_” and spaces; at most 40 characters. Names are never reused." validationState={tried && nameError ? 'error' : 'none'} validationMessage={tried && nameError ? nameError : undefined}>
          <Input className="mono" value={name} onChange={(_, data) => setName(data.value)} placeholder="e.g. v2.0 draft"/>
        </Field>
        <Field label="Change note" hint={`What changed and why. ${note.length}/${NOTE_MAX}`} validationState={tried && noteError ? 'error' : 'none'} validationMessage={tried && noteError ? noteError : undefined}>
          <Textarea value={note} resize="vertical" rows={4} onChange={(_, data) => setNote(data.value)}/>
        </Field>
        <p className="section-note reminder">{REMINDER}</p>
        {error && <p className="run-failure tone-error" role="alert">{error}</p>}
        <div className="modal-actions">
          <Button appearance="secondary" onClick={onClose} disabled={busy}>Cancel</Button>
          <Button type="submit" appearance="primary" disabled={busy}>{busy ? 'Publishing…' : 'Publish'}</Button>
        </div>
      </form>
    </div>
  </div>;
}
