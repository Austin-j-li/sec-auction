import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { Button, Field, FluentProvider, Input, Select, Spinner, Textarea, webLightTheme } from '@fluentui/react-components';
import { ArrowClockwiseIcon, ArrowDownIcon, ArrowLeftIcon, ArrowRightIcon, ArrowUpIcon, CaretDownIcon, DownloadSimpleIcon, FloppyDiskIcon, ListIcon, PlusIcon, TrashIcon, WarningCircleIcon, XIcon } from '@phosphor-icons/react';
import gsap from 'gsap';
import Filing from './Filing';
import { count, json, recordValues, rowId, saveDeal, sheetColumns, sheetRows, text } from './api';
import './style.css';

const SHEETS = { ledger: 'Deal ledger', rounds: 'Rounds', questions: 'Questions', facts: 'Deal facts' };
const TABS = [['ledger', 'Ledger'], ['rounds', 'Rounds'], ['questions', 'Questions'], ['facts', 'Deal facts'], ['review', 'Review'], ['changes', 'Changes'], ['history', 'History']];
const LONG_FIELDS = new Set(['Note', 'Quote and page', 'Reviewer note', 'Question', 'Recommended answer', 'Why, with page', 'Rows affected', 'What changes if answered differently', 'How opened', 'Who was in', 'Due dates', 'Deadline outcome', 'Bids received', 'How it ended', 'Value']);
const DATE_FIELDS = new Set(['Sort date', 'Date from', 'Date to', 'Opened']);
const NUMERIC_FIELDS = new Set(['#', 'Process', 'Count', 'Price low', 'Price high']);
const EMPTY = { user: '', can_edit: false, csrf_token: '' };

function routeFromLocation() {
  const match = location.pathname.match(/^\/deal\/([a-z0-9][a-z0-9-]*)\/?$/);
  return match ? { slug: match[1] } : { slug: null };
}
function clone(value) { return structuredClone(value); }
function labelStatus(value) { return text(value).replaceAll('_', ' '); }
function compact(value, length = 118) { const s = text(value); return s.length > length ? `${s.slice(0, length - 1)}…` : s; }
function friendlyDate(value) { if (!value) return ''; const d = new Date(value); return Number.isNaN(d.getTime()) ? text(value) : d.toLocaleString(); }
function confirmLoss() { return window.confirm('You have unsaved edits. Discard them and leave this view?'); }

function App() {
  const [route, setRoute] = useState(routeFromLocation);
  const [deals, setDeals] = useState(null);
  const [deal, setDeal] = useState(null);
  const [filing, setFiling] = useState(null);
  const [session, setSession] = useState(EMPTY);
  const [loading, setLoading] = useState(false);
  const [filingLoading, setFilingLoading] = useState(false);
  const [error, setError] = useState('');
  const [filingError, setFilingError] = useState('');
  const [saveState, setSaveState] = useState('');
  const [ops, setOps] = useState([]);
  const [reason, setReason] = useState('');
  const [selectedUid, setSelectedUid] = useState(null);
  const [selectedBySheet, setSelectedBySheet] = useState({});
  const [tab, setTab] = useState('ledger');
  const [version, setVersion] = useState('working');
  const [mobilePane, setMobilePane] = useState('workspace');
  const [filingSearchRequest, setFilingSearchRequest] = useState(null);
  const [filingScrollRequest, setFilingScrollRequest] = useState(0);
  const [historyData, setHistoryData] = useState(null);
  const [changesData, setChangesData] = useState(null);
  const [auxLoading, setAuxLoading] = useState(false);
  const [conflict, setConflict] = useState(false);
  const [deletePrompt, setDeletePrompt] = useState(null);
  const [findingOpen, setFindingOpen] = useState(null);
  const [documentOpen, setDocumentOpen] = useState(null);
  const [documentData, setDocumentData] = useState(null);
  const [documentError, setDocumentError] = useState('');
  const [docLoading, setDocLoading] = useState(false);
  const saveFlash = useRef(null);
  const modalRef = useRef(null);
  const modalReturnFocus = useRef(null);
  const routeSerial = useRef(0);
  const filingCache = useRef(new Map());
  const dirty = ops.length > 0;
  const editable = Boolean(session.can_edit && deal?.workspace?.editable && saveState !== 'saving');
  const slug = route.slug;

  useEffect(() => { json('/api/session').then(setSession).catch(err => setError(`Session: ${err.message}`)); }, []);
  useEffect(() => {
    const listener = event => { if (dirty) { event.preventDefault(); event.returnValue = ''; } };
    window.addEventListener('beforeunload', listener);
    return () => window.removeEventListener('beforeunload', listener);
  }, [dirty]);
  useEffect(() => {
    const listener = () => { if (saveState === 'saving' || (dirty && !confirmLoss())) { history.pushState(null, '', slug ? `/deal/${slug}${location.hash}` : '/'); return; } setRoute(routeFromLocation()); };
    window.addEventListener('popstate', listener);
    return () => window.removeEventListener('popstate', listener);
  }, [dirty, slug, saveState]);
  useEffect(() => {
    const listener = event => {
      if (!deal || event.metaKey || event.ctrlKey || event.altKey || /^(INPUT|TEXTAREA|SELECT)$/.test(event.target?.tagName || '')) return;
      if (event.key === 'j' || event.key === 'ArrowDown') { event.preventDefault(); stepRow(1); }
      if (event.key === 'k' || event.key === 'ArrowUp') { event.preventDefault(); stepRow(-1); }
    };
    window.addEventListener('keydown', listener);
    return () => window.removeEventListener('keydown', listener);
  });
  useEffect(() => {
    if (!saveFlash.current || saveState !== 'saved' || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    const tween = gsap.fromTo(saveFlash.current, { opacity: 0, y: -4 }, { opacity: 1, y: 0, duration: 0.28, ease: 'power2.out' });
    return () => tween.kill();
  }, [saveState]);
  useEffect(() => {
    if (!deletePrompt && !documentOpen) return;
    modalReturnFocus.current = document.activeElement;
    modalRef.current?.querySelector('button')?.focus();
    const onKeyDown = event => {
      if (event.key === 'Escape') { event.preventDefault(); setDeletePrompt(null); setDocumentOpen(null); return; }
      if (event.key !== 'Tab' || !modalRef.current) return;
      const focusables = [...modalRef.current.querySelectorAll('button:not(:disabled), input:not(:disabled), select:not(:disabled), textarea:not(:disabled), a[href]')];
      if (!focusables.length) return;
      if (event.shiftKey && document.activeElement === focusables[0]) { event.preventDefault(); focusables.at(-1).focus(); }
      else if (!event.shiftKey && document.activeElement === focusables.at(-1)) { event.preventDefault(); focusables[0].focus(); }
    };
    window.addEventListener('keydown', onKeyDown);
    return () => { window.removeEventListener('keydown', onKeyDown); modalReturnFocus.current?.focus?.(); };
  }, [Boolean(deletePrompt), Boolean(documentOpen)]);

  function navigate(path) {
    if (saveState === 'saving') return;
    if (dirty && !confirmLoss()) return;
    history.pushState(null, '', path);
    setRoute(routeFromLocation());
  }
  const load = useCallback(async (currentSlug, currentVersion = 'working') => {
    const token = ++routeSerial.current;
    setLoading(true); setError(''); setConflict(false); setDeal(null); setOps([]); setSaveState(''); setHistoryData(null); setChangesData(null); setFindingOpen(null); setDocumentOpen(null);
    try {
      if (!currentSlug) {
        const list = await json('/api/deals');
        if (token === routeSerial.current) { setDeals(list); document.title = 'Ledger cockpit'; }
      } else {
        const data = await json(`/api/deal/${currentSlug}?version=${encodeURIComponent(currentVersion)}`);
        if (token !== routeSerial.current) return;
        setDeal(data); setVersion(currentVersion); setTab('ledger');
        const hash = location.hash.match(/^#row-(.+)$/);
        const target = hash && data.ledger?.rows?.find(row => rowId(row) === decodeURIComponent(hash[1]));
        const initial = target?.uid || data.ledger?.rows?.[0]?.uid || null;
        setSelectedUid(initial); setSelectedBySheet({ 'Deal ledger': initial });
        document.title = `${data.name || currentSlug} · Ledger cockpit`;
        const cached = filingCache.current.get(currentSlug);
        if (cached) { setFiling(cached); setFilingLoading(false); }
        else {
          setFiling(null); setFilingLoading(true); setFilingError('');
          json(`/api/filing/${currentSlug}`).then(source => { filingCache.current.set(currentSlug, source); if (token === routeSerial.current) setFiling(source); }).catch(err => { if (token === routeSerial.current) setFilingError(err.message); }).finally(() => { if (token === routeSerial.current) setFilingLoading(false); });
        }
      }
    } catch (err) { if (token === routeSerial.current) setError(err.message); }
    finally { if (token === routeSerial.current) setLoading(false); }
  }, []);
  useEffect(() => { load(slug, 'working'); }, [slug, load]);
  useEffect(() => {
    if (!slug || !deal || !['changes', 'history'].includes(tab)) return;
    let alive = true;
    setAuxLoading(true);
    json(`/api/deal/${slug}/${tab}`).then(data => { if (alive) { if (tab === 'changes') setChangesData(data); else setHistoryData(data); } }).catch(err => { if (alive) setError(err.message); }).finally(() => { if (alive) setAuxLoading(false); });
    return () => { alive = false; };
  }, [slug, deal?.workspace?.revision, tab]);

  function selectRow(uid, fromFiling = false) {
    const row = deal?.ledger?.rows?.find(item => item.uid === uid);
    if (!row) return;
    setSelectedUid(uid); setSelectedBySheet(current => ({ ...current, 'Deal ledger': uid })); setTab('ledger');
    history.replaceState(null, '', `/deal/${slug}#row-${encodeURIComponent(rowId(row))}`);
    if (fromFiling) setMobilePane('workspace');
  }
  function selectOther(sheet, uid) { setSelectedBySheet(current => ({ ...current, [sheet]: uid })); }
  function stepRow(delta) {
    const rows = deal?.ledger?.rows || [];
    if (!rows.length) return;
    const index = rows.findIndex(item => item.uid === selectedUid);
    selectRow(rows[Math.max(0, Math.min(rows.length - 1, index + delta))].uid);
  }
  function switchVersion(id) { if (dirty && !confirmLoss()) return; load(slug, id); }

  function editValue(sheet, uid, field, value) {
    setDeal(current => {
      const next = clone(current);
      const record = sheetRows(next, sheet).find(item => item.uid === uid);
      if (!record) return current;
      if (sheet === 'Deal facts') { if (field === 'Field') record.field = value; else record.value = value; }
      else { record.cells[field] = value; if (sheet === 'Deal ledger' && field === '#') record.id = value; if (sheet === 'Questions' && field === 'Q') record.id = value; }
      return next;
    });
    setOps(previous => {
      const next = clone(previous);
      const insert = next.find(op => op.type === 'insert' && op.client_uid === uid);
      if (insert) { insert.values[field] = value; return next; }
      const update = next.find(op => op.type === 'update' && op.sheet === sheet && op.uid === uid);
      if (update) update.values[field] = value;
      else next.push({ type: 'update', sheet, uid, values: { [field]: value } });
      return next;
    });
    setSaveState('');
  }
  function addRow(sheet, cloneUid = null) {
    if (!editable) return;
    const rows = sheetRows(deal, sheet);
    const selected = rows.find(row => row.uid === (cloneUid || selectedBySheet[sheet]));
    const afterUid = selected?.uid || rows.at(-1)?.uid || null;
    const values = Object.fromEntries(sheetColumns(deal, sheet).map(field => [field, cloneUid ? text(recordValues(selected, sheet)[field]) : '']));
    if (sheet === 'Deal ledger') { values['#'] = ''; if (cloneUid) values.Count = ''; }
    if (sheet === 'Questions') {
      const used = new Set(rows.map(item => text(item.cells?.Q)));
      let number = 1; while (used.has(`Q${number}`)) number++;
      values.Q = `Q${number}`;
    }
    const temporary = `new-${crypto.randomUUID()}`;
    const row = sheet === 'Deal facts' ? { uid: temporary, field: values.Field, value: values.Value } : { uid: temporary, id: '', excel_row: null, cells: values, issues: [], quote: null };
    setDeal(current => {
      const next = clone(current), list = sheetRows(next, sheet), index = list.findIndex(item => item.uid === afterUid);
      list.splice(index + 1, 0, row); return next;
    });
    const insertValues = { ...values };
    if (sheet === 'Deal ledger') delete insertValues['#'];
    setOps(previous => [...previous, { type: 'insert', sheet, client_uid: temporary, after_uid: afterUid, values: insertValues }]);
    selectOther(sheet, temporary);
    if (sheet === 'Deal ledger') setSelectedUid(temporary);
    setSaveState('');
  }
  function moveRow(sheet, uid, direction) {
    if (!editable) return;
    const rows = sheetRows(deal, sheet), index = rows.findIndex(row => row.uid === uid), nextIndex = index + direction;
    if (index < 0 || nextIndex < 0 || nextIndex >= rows.length) return;
    const afterUid = direction < 0 ? rows[index - 2]?.uid || null : rows[index + 1].uid;
    setDeal(current => { const next = clone(current), list = sheetRows(next, sheet), [row] = list.splice(index, 1); list.splice(nextIndex, 0, row); return next; });
    setOps(previous => [...previous, { type: 'move', sheet, uid, after_uid: afterUid }]);
    setSaveState('');
  }
  function requestDelete(sheet, uid) {
    const row = sheetRows(deal, sheet).find(item => item.uid === uid);
    if (!row || !editable) return;
    setDeletePrompt({ sheet, uid, hasReferences: Boolean(row.has_references), label: sheet === 'Deal ledger' ? `#${rowId(row)} ${compact(row.cells?.Event, 50)}` : sheet === 'Deal facts' ? row.field : compact(row.cells?.Q || row.cells?.Question || row.cells?.Round, 70), replacement: '' });
  }
  function deleteRow() {
    if (!deletePrompt) return;
    const { sheet, uid, replacement } = deletePrompt;
    setDeal(current => { const next = clone(current), rows = sheetRows(next, sheet), index = rows.findIndex(row => row.uid === uid); rows.splice(index, 1); return next; });
    setOps(previous => {
      const predecessor = previous.find(op => op.type === 'insert' && op.client_uid === uid)?.after_uid || null;
      const next = previous.filter(op => !(op.uid === uid && ['update', 'move', 'review'].includes(op.type)));
      if (uid.startsWith('new-')) return next.filter(op => !(op.type === 'insert' && op.client_uid === uid)).map(op => op.after_uid === uid ? { ...op, after_uid: predecessor } : op);
      const op = { type: 'delete', sheet, uid };
      if (sheet === 'Deal ledger' && replacement) op.replacement_uid = replacement;
      next.push(op); return next;
    });
    const left = sheetRows(deal, sheet).filter(row => row.uid !== uid);
    selectOther(sheet, left[0]?.uid || null);
    if (sheet === 'Deal ledger') setSelectedUid(left[0]?.uid || null);
    setDeletePrompt(null); setSaveState('');
  }
  function setReview(uid, status, note) {
    setDeal(current => { const next = clone(current); next.row_review = { ...next.row_review, [uid]: { ...(next.row_review?.[uid] || {}), status, note } }; return next; });
    setOps(previous => {
      const next = clone(previous), existing = next.find(op => op.type === 'review' && op.uid === uid);
      if (existing) Object.assign(existing, { status, note }); else next.push({ type: 'review', uid, status, note });
      return next;
    }); setSaveState('');
  }
  function setFinding(id, field, value) {
    setDeal(current => { const next = clone(current), finding = next.findings?.find(item => item.id === id); if (finding) finding[field] = value; return next; });
    setOps(previous => {
      const next = clone(previous), existing = next.find(op => op.type === 'finding' && op.id === id);
      if (existing) existing[field] = value;
      else { const finding = deal.findings.find(item => item.id === id); next.push({ type: 'finding', id, judgment: finding.judgment || 'unreviewed', implementation: finding.implementation || 'unassessed', verification: finding.verification || 'unchecked', note: finding.note || '', [field]: value }); }
      return next;
    }); setSaveState('');
  }
  async function save() {
    if (!dirty || !editable || saveState === 'saving' || conflict) return;
    setSaveState('saving'); setError('');
    const operations = ops.map(op => ({ ...op }));
    try {
      const result = await saveDeal(slug, session, { revision: deal.workspace.revision, base_sha256: deal.workspace.base_sha256, reason: reason.trim() || 'Cockpit edit', operations });
      const selectedRow = deal.ledger?.rows?.find(row => row.uid === selectedUid);
      const stable = selectedUid?.startsWith('new-') ? null : selectedUid;
      const localLedgerIndex = deal.ledger?.rows?.findIndex(row => row.uid === selectedUid) ?? -1;
      const savedSheetSelection = Object.fromEntries(Object.entries(selectedBySheet).map(([sheet, uid]) => {
        const localIndex = sheetRows(deal, sheet).findIndex(row => row.uid === uid);
        return [sheet, uid?.startsWith('new-') ? sheetRows(result, sheet)[localIndex]?.uid || null : uid];
      }));
      setDeal(result); setOps([]); setReason(''); setSaveState('saved'); setConflict(false); setChangesData(null); setHistoryData(null);
      setSelectedUid(result.ledger?.rows?.find(row => row.uid === stable)?.uid || result.ledger?.rows?.[localLedgerIndex]?.uid || result.ledger?.rows?.find(row => rowId(row) === rowId(selectedRow))?.uid || result.ledger?.rows?.[0]?.uid || null);
      setSelectedBySheet(savedSheetSelection);
    } catch (err) { setError(err.message); setConflict(err.status === 409); setSaveState('error'); }
  }
  function downloadDraft() {
    const draft = { deal: slug, based_on_revision: deal.workspace.revision, base_sha256: deal.workspace.base_sha256, reason, operations: ops };
    const url = URL.createObjectURL(new Blob([JSON.stringify(draft, null, 2)], { type: 'application/json' }));
    const link = document.createElement('a'); link.href = url; link.download = `${slug}-unsaved-edits.json`; link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
  function discardAndReload() { if (confirmLoss()) load(slug, 'working'); }
  async function restore(revision) {
    if (!editable) return;
    if (dirty && !confirmLoss()) return;
    if (!window.confirm(`Restore revision ${revision} as a new working revision? The current version remains in history.`)) return;
    setError(''); setSaveState('saving');
    try {
      const result = await saveDeal(slug, session, { revision: deal.workspace.revision, base_sha256: deal.workspace.base_sha256, reason: `Restore revision ${revision}`, operations: [{ type: 'restore', target_revision: revision }] });
      setDeal(result); setOps([]); setHistoryData(null); setChangesData(null); setSaveState('saved');
      setSelectedUid(result.ledger?.rows?.some(row => row.uid === selectedUid) ? selectedUid : result.ledger?.rows?.[0]?.uid || null);
      setSelectedBySheet({});
    } catch (err) { setError(err.message); setConflict(err.status === 409); setSaveState('error'); }
  }
  async function openDocument(item) {
    setDocumentOpen(item); setDocumentData(null); setDocumentError(''); setDocLoading(true);
    try { setDocumentData(await json(`/api/document/${slug}/${encodeURIComponent(item.id)}`)); }
    catch (err) { setDocumentError(err.message); }
    finally { setDocLoading(false); }
  }
  function chooseQuote(selection) {
    if (!editable) return;
    const row = deal.ledger?.rows?.find(item => item.uid === selectedUid);
    if (!row) { setError('Select a ledger event before using filing text.'); return; }
    const quote = selection.quote.replace(/\s+/g, ' ').trim();
    editValue('Deal ledger', row.uid, 'Quote and page', `“${quote}”${selection.pageLabel ? ` (${selection.pageLabel})` : ''}`);
    setMobilePane('workspace');
  }
  function showRowEvidence(uid) { selectRow(uid); setFilingScrollRequest(value => value + 1); setMobilePane('filing'); }
  function openQuestion(uid) { setSelectedBySheet(current => ({ ...current, Questions: uid })); setTab('questions'); setMobilePane('workspace'); }
  function findEvidence(evidence) {
    const quote = text(evidence.quote).replace(/\s+/g, ' ').trim();
    if (!quote) return;
    setFilingSearchRequest({ text: quote.replace(/^[^\p{L}\p{N}]+/u, '').slice(0, 32), page: evidence.page, nonce: Date.now() });
    setMobilePane('filing');
  }

  if (!slug) return <><Header onHome={() => navigate('/')} session={session}/><main className="overview-wrap">{loading && <div className="center-state"><Spinner label="Loading deals"/></div>}{error && <Message type="error">{error}</Message>}{deals && <Overview deals={deals} onOpen={s => navigate(`/deal/${s}`)}/>}</main></>;
  const ledgerRows = deal?.ledger?.rows || [];
  const selected = ledgerRows.find(row => row.uid === selectedUid);
  return <><Header onHome={() => navigate('/')} session={session} deal={deal}/>
    <main className="deal-shell">
      {loading && <div className="center-state"><Spinner label={`Loading ${slug}`}/></div>}
      {error && <Message type={conflict ? 'warning' : 'error'}>{conflict ? 'Another editor saved a newer revision. Your unsaved edits remain in this browser. ' : ''}{error}{conflict && <span className="conflict-actions"><Button size="small" onClick={downloadDraft}>Download staged edits</Button><Button size="small" onClick={discardAndReload}>Discard edits and load latest</Button></span>}</Message>}
      {deal && <>
        <div className="deal-toolbar">
          <div className="deal-identity"><button className="back-link" onClick={() => navigate('/')}><ArrowLeftIcon size={17}/> All deals</button><h1>{deal.name || deal.facts?.find(f => f.field === 'Target')?.value || slug}</h1><div className="deal-subline">{deal.filing?.form_type} · {deal.filing?.date_filed} · {deal.workspace?.selected_version === 'working' ? `Working from ${deal.versions?.find(item => item.id === deal.workspace?.base_version)?.label || deal.workspace?.base_version || 'base'} · Revision ${deal.workspace?.revision}` : 'Source version'}</div></div>
          <div className="toolbar-actions"><label className="version-control">Version <Select aria-label="Version" value={version} onChange={(_, data) => switchVersion(data.value)} disabled={saveState === 'saving'}>{(deal.versions || []).map(item => <option value={item.id} key={item.id}>{item.label || item.id}{item.instruction_version ? ` · ${item.instruction_version}` : ''}</option>)}</Select></label><a className="export-link" href={`/api/deal/${slug}/export?version=${encodeURIComponent(version)}`} download><DownloadSimpleIcon size={18}/> Export Excel</a><Button appearance="primary" icon={<FloppyDiskIcon size={18}/>} disabled={!dirty || !editable || saveState === 'saving' || conflict} onClick={save}>{saveState === 'saving' ? 'Saving…' : 'Save changes'}</Button></div>
          <div className="save-line"><span className={`work-state ${dirty ? 'unsaved' : ''}`} aria-live="polite">{dirty ? `${ops.length} unsaved ${count(ops.length, 'change').split(' ').slice(1).join(' ')}` : saveState === 'saved' ? 'Saved' : editable ? 'No unsaved edits' : 'Read only version'}</span><span ref={saveFlash} className="save-feedback">{saveState === 'saved' ? 'Revision saved' : ''}</span>{deal.workspace?.updated_by && <span>Last saved by {deal.workspace.updated_by}{deal.workspace.updated_at ? ` · ${friendlyDate(deal.workspace.updated_at)}` : ''}</span>}</div>
        </div>
        <div className="mobile-switch" role="group" aria-label="Visible pane"><Button appearance={mobilePane === 'filing' ? 'primary' : 'secondary'} onClick={() => setMobilePane('filing')}>Filing</Button><Button appearance={mobilePane === 'workspace' ? 'primary' : 'secondary'} onClick={() => setMobilePane('workspace')}>Workspace</Button></div>
        <div className="workbench">
          <div className={`filing-column ${mobilePane === 'filing' ? 'mobile-active' : ''}`}><Filing filing={filing} loading={filingLoading} error={filingError} deal={deal} selectedUid={selectedUid} scrollRequest={filingScrollRequest} searchRequest={filingSearchRequest} onSelectRow={selectRow} onQuoteSelection={editable ? chooseQuote : null}/></div>
          <section className={`workspace-column ${mobilePane === 'workspace' ? 'mobile-active' : ''}`} aria-label="Deal workspace">
            <nav className="tabs" role="tablist" aria-label="Workspace tabs">{TABS.map(([key, label]) => <button key={key} role="tab" aria-selected={tab === key} className={tab === key ? 'active' : ''} onClick={() => setTab(key)}>{label}{['ledger', 'rounds', 'questions'].includes(key) && <small>{sheetRows(deal, SHEETS[key]).length}</small>}{key === 'review' && deal.findings?.length > 0 && <small>{deal.findings.length}</small>}</button>)}</nav>
            <div className={`workspace-scroll ${['ledger', 'rounds', 'questions', 'facts'].includes(tab) ? 'editor-scroll' : ''}`} role="tabpanel">
              {tab === 'ledger' && <LedgerTab deal={deal} selectedUid={selectedUid} onSelect={selectRow} onShowFiling={showRowEvidence} onOpenQuestion={openQuestion} onStep={stepRow} onAdd={addRow} onMove={moveRow} onDelete={requestDelete} onEdit={editValue} onReview={setReview} editable={editable} selection={selected}/>}
              {['rounds', 'questions', 'facts'].includes(tab) && <SheetTab deal={deal} sheet={SHEETS[tab]} selectedUid={selectedBySheet[SHEETS[tab]]} onSelect={selectOther} onAdd={addRow} onMove={moveRow} onDelete={requestDelete} onEdit={editValue} editable={editable} onJumpRow={selectRow}/>}
              {tab === 'review' && <ReviewTab deal={deal} editable={editable} open={findingOpen} onToggle={setFindingOpen} onEdit={setFinding} onFindEvidence={findEvidence} onOpenDocument={openDocument}/>}
              {tab === 'changes' && <ChangesTab data={changesData} loading={auxLoading}/>}
              {tab === 'history' && <HistoryTab data={historyData} loading={auxLoading} editable={editable} onRestore={restore}/>}
            </div>
          </section>
        </div>
        {dirty && session.can_edit && deal?.workspace?.editable && <div className="save-dock"><Field label="Reason for this revision" hint="Appears in history"><Input value={reason} disabled={saveState === 'saving'} onChange={(_, data) => setReason(data.value)} placeholder="Describe the edit"/></Field><Button appearance="primary" icon={<FloppyDiskIcon size={17}/>} disabled={saveState === 'saving' || conflict} onClick={save}>Save {count(ops.length, 'change')}</Button></div>}
      </>}
    </main>
    {deletePrompt && <div className="modal-backdrop" role="presentation"><div className="modal" ref={modalRef} role="dialog" aria-modal="true" aria-label="Delete record"><div className="modal-head"><h2>Delete {deletePrompt.label}?</h2><button onClick={() => setDeletePrompt(null)} aria-label="Close"><XIcon size={20}/></button></div><p>This deletion is staged until you save. The record can be recovered from history after saving.</p>{deletePrompt.sheet === 'Deal ledger' && deletePrompt.hasReferences && <Field label="Replacement event" hint="This event has explicit references. Choose the event they should point to before deleting."><Select value={deletePrompt.replacement} onChange={(_, data) => setDeletePrompt(value => ({ ...value, replacement: data.value }))}><option value="">Choose a replacement</option>{ledgerRows.filter(row => row.uid !== deletePrompt.uid).map(row => <option key={row.uid} value={row.uid}>{row.uid.startsWith('new-') ? 'New event' : `#${rowId(row)}`} · {compact(row.cells?.Event, 35)}</option>)}</Select></Field>}<div className="modal-actions"><Button onClick={() => setDeletePrompt(null)}>Cancel</Button><Button appearance="primary" disabled={deletePrompt.hasReferences && !deletePrompt.replacement} onClick={deleteRow}>Stage deletion</Button></div></div></div>}
    {documentOpen && <div className="modal-backdrop" role="presentation"><div className="modal document-modal" ref={modalRef} role="dialog" aria-modal="true" aria-label="Recorded document"><div className="modal-head"><h2>{documentData?.title || documentOpen.label}</h2><button onClick={() => setDocumentOpen(null)} aria-label="Close"><XIcon size={20}/></button></div>{docLoading ? <Spinner label="Loading document"/> : documentError ? <Message type="error">{documentError}</Message> : <pre>{documentData?.text}</pre>}</div></div>}
  </>;
}

function Header({ onHome, session, deal }) { return <header className="global-header"><button className="wordmark" onClick={onHome}><span className="brand-mark">L</span> Ledger cockpit</button><span className="header-context">{deal ? 'Deal workspace' : 'Deal ledgers'}</span><div className="header-user">{session.user ? <>{session.user}{session.can_edit ? <span className="edit-access">Edit access</span> : <span>Read only</span>}</> : 'Loading session'}</div></header>; }
function Message({ type, children }) { return <div className={`message ${type}`} role="alert"><WarningCircleIcon size={19}/><div>{children}</div></div>; }

function Overview({ deals, onOpen }) { return <><div className="overview-title"><div><span className="eyebrow">Research workspace</span><h1>Deal ledgers</h1><p>{count(deals.length, 'deal')} available. Open a deal to inspect the filing and edit its working copy.</p></div><span className="overview-total">{deals.length}</span></div><div className="deal-table-wrap"><table className="deal-table"><thead><tr><th>Deal</th><th>Filing</th><th>Working copy</th><th className="number">Events</th><th className="number">Rounds</th><th className="number">Questions</th><th>Source evidence</th><th>Review state</th></tr></thead><tbody>{deals.map(item => <tr key={item.slug} onClick={() => onOpen(item.slug)} tabIndex={0} onKeyDown={event => { if (event.key === 'Enter') onOpen(item.slug); }}><td><strong>{item.name || item.target || item.slug}</strong><small>{item.slug}</small></td><td>{item.form_type || '—'}<small>{item.date_filed || ''}</small></td><td>{item.base_label || item.instruction_version || 'Working'}<small>{item.working_revision != null ? `Revision ${item.working_revision}` : ''}</small></td><td className="number">{item.rows ?? '—'}</td><td className="number">{item.rounds ?? '—'}</td><td className="number">{item.questions ?? '—'}</td><td>{item.quotes_total != null ? `${item.quotes_located ?? 0} / ${item.quotes_total} quotes located` : '—'}<small>Location aid, not validation</small>{item.check && <small>{item.check.errors ?? 0} mechanical errors · {item.check.warnings ?? 0} warnings</small>}</td><td><span className="status-text">{labelStatus(item.review_status || 'unreviewed')}</span>{item.error && <small className="error-text">{item.error}</small>}</td></tr>)}</tbody></table></div>{!deals.length && <div className="empty">No deal workbooks are available yet.</div>}</>; }

function Issues({ issues, pageHint }) { if (!issues?.length && !pageHint) return null; return <div className="issues">{(issues || []).map((issue, i) => <div key={i} className={`issue ${issue.severity || 'info'}`}><strong>{issue.code || issue.severity}</strong> {issue.column && <span>{issue.column} · </span>}{issue.message}</div>)}{pageHint && <div className="issue info">{pageHint}</div>}</div>; }
function EventSummary({ row, selected, onClick, review }) { const c = row.cells || {}; return <button id={`row-${rowId(row)}`} className={`event-item ${selected ? 'selected' : ''}`} onClick={onClick}><div className="event-line"><span className="event-number">{row.uid.startsWith('new-') ? 'New' : `#${rowId(row)}`}</span><span className="event-date">{c.When || 'Date unstated'}</span><span className="event-review">{review?.status === 'reviewed' ? 'Reviewed' : review?.status === 'needs_decision' ? 'Needs decision' : ''}</span></div><strong>{c.Event || 'Untitled event'}</strong><span className="event-detail">{[c.Who, c.Process && `Process ${c.Process}`, c.Round !== '' && c.Round != null && `Round ${c.Round}`].filter(Boolean).join(' · ')}</span>{row.quote && <span className={`quote-location ${row.quote.located ? '' : 'missing'}`}>{row.quote.located ? 'Source located' : 'Quote not located'}</span>}</button>; }
function QuestionLinks({ flag, questions, onOpen }) { const ids = [...new Set([...text(flag).matchAll(/\bQ\d+\b/gi)].map(match => match[0].toUpperCase()))]; const linked = ids.map(id => questions.find(question => text(question.id).toUpperCase() === id || text(question.cells?.Q).toUpperCase() === id)).filter(Boolean); return linked.length ? <div className="reference-links"><strong>Linked questions</strong>{linked.map(question => <Button key={question.uid} size="small" aria-label={`Open question ${question.id || question.cells?.Q}`} onClick={() => onOpen(question.uid)}>{question.id || question.cells?.Q} · {compact(question.cells?.Question, 58)}</Button>)}</div> : null; }

function LedgerTab({ deal, selectedUid, onSelect, onShowFiling, onOpenQuestion, onStep, onAdd, onMove, onDelete, onEdit, onReview, editable, selection }) {
  const rows = deal.ledger?.rows || [], index = rows.findIndex(row => row.uid === selectedUid), row = selection || rows[0], review = row ? deal.row_review?.[row.uid] || { status: 'unreviewed', note: '' } : null;
  const editorRef = useRef(null);
  const listRef = useRef(null);
  useEffect(() => { if (editorRef.current) editorRef.current.scrollTop = 0; }, [row?.uid]);
  useEffect(() => {
    const container = listRef.current, target = container?.querySelector('.event-item.selected');
    if (!container || !target) return;
    if (matchMedia('(max-width: 560px)').matches) container.querySelector('.event-list')?.scrollTo({ left: target.offsetLeft - 14, behavior: 'instant' });
    else container.scrollTop += target.getBoundingClientRect().top - container.getBoundingClientRect().top - Math.min(90, container.clientHeight * 0.22);
  }, [row?.uid]);
  return <div className="ledger-layout"><div className="record-list" ref={listRef}><div className="section-head"><div><h2>Events</h2><span>{count(rows.length, 'event')}</span></div>{editable && <Button size="small" icon={<PlusIcon size={15}/>} onClick={() => onAdd('Deal ledger')}>Add</Button>}</div><div className="event-list">{rows.length ? rows.map(item => <EventSummary key={item.uid} row={item} selected={item.uid === row?.uid} onClick={() => onSelect(item.uid)} review={deal.row_review?.[item.uid]}/>) : <div className="empty">No events in this ledger. Add the first event to begin.</div>}</div></div><div className="record-editor" ref={editorRef}>{row ? <><div className="editor-head"><div><span className="eyebrow">Selected event</span><h2>{row.uid.startsWith('new-') ? 'New' : `#${rowId(row)}`} {row.cells?.Event || 'event'}</h2><p>{row.cells?.When || 'Date unstated'}{row.cells?.Who ? ` · ${row.cells.Who}` : ''}</p></div><div className="editor-nav"><Button aria-label="Previous event" icon={<ArrowUpIcon size={16}/>} disabled={index <= 0} onClick={() => onStep(-1)}/><Button aria-label="Next event" icon={<ArrowDownIcon size={16}/>} disabled={index < 0 || index >= rows.length - 1} onClick={() => onStep(1)}/></div></div><div className="record-actions">{editable && <><Button size="small" disabled={index <= 0} icon={<ArrowUpIcon size={15}/>} onClick={() => onMove('Deal ledger', row.uid, -1)}>Move up</Button><Button size="small" disabled={index < 0 || index >= rows.length - 1} icon={<ArrowDownIcon size={15}/>} onClick={() => onMove('Deal ledger', row.uid, 1)}>Move down</Button><Button size="small" onClick={() => onAdd('Deal ledger', row.uid)}>Clone to split</Button><Button size="small" icon={<TrashIcon size={15}/>} onClick={() => onDelete('Deal ledger', row.uid)}>Delete</Button></>}</div><div className="source-summary"><strong>Source evidence</strong><span>{row.quote?.located ? `Quote located${row.quote.found_page ? ` on page ${row.quote.found_page}` : ''}${row.quote.occurrences > 1 ? ` · ${row.quote.occurrences} occurrences` : ''}` : row.cells?.['Quote and page'] ? 'Quote not located in filing' : 'No quote recorded'}</span>{row.quote?.located && <Button size="small" onClick={() => onShowFiling(row.uid)}>Show in filing</Button>}</div><Issues issues={row.issues} pageHint={deal.pages_reliable ? row.page_hint : null}/><RecordForm sheet="Deal ledger" columns={deal.ledger.columns} row={row} choices={deal.choices} editable={editable} onEdit={onEdit}/><QuestionLinks flag={row.cells?.Flag} questions={deal.questions?.rows || []} onOpen={onOpenQuestion}/><div className="review-box"><div><h3>Row review</h3><p>Review status records a reader’s judgment; it does not certify that the filing is complete.</p></div><Field label="Status"><Select value={review.status || 'unreviewed'} disabled={!editable} onChange={(_, data) => onReview(row.uid, data.value, review.note || '')}><option value="unreviewed">Unreviewed</option><option value="reviewed">Reviewed</option><option value="needs_decision">Needs decision</option></Select></Field><Field label="Review note"><Textarea value={review.note || ''} disabled={!editable} onChange={(_, data) => onReview(row.uid, review.status || 'unreviewed', data.value)} resize="vertical"/></Field></div></> : <div className="empty">Select an event or add a new one.</div>}</div></div>;
}

function RecordForm({ sheet, columns, row, choices, editable, onEdit }) { const values = recordValues(row, sheet); return <div className="field-grid">{columns.map(field => {
    const rawChoices = choices?.[field] || choices?.[sheet]?.[field];
    const options = Array.isArray(rawChoices) ? rawChoices : null;
    const value = text(values[field]);
    const isDate = DATE_FIELDS.has(field);
    const isNumber = NUMERIC_FIELDS.has(field) && field !== '#' && !(field === 'Round');
    const isLong = LONG_FIELDS.has(field) || value.length > 140;
    const hint = field === 'Count' ? 'Leave blank when the cohort size is uncertain.' : field === 'Sort date' ? 'Excel date used to order events.' : field === 'Quote and page' ? 'Exact source wording and printed page; select filing text to fill.' : undefined;
    const input = options && (!value || options.includes(value)) ? <Select value={value} disabled={!editable} onChange={(_, data) => onEdit(sheet, row.uid, field, data.value)}><option value="">Blank</option>{options.map(option => <option key={option} value={option}>{option}</option>)}</Select>
      : isLong ? <Textarea value={value} disabled={!editable} resize="vertical" rows={value.length > 350 ? 5 : 3} onChange={(_, data) => onEdit(sheet, row.uid, field, data.value)}/>
      : <Input type={isDate && /^\d{4}-\d{2}-\d{2}$/.test(value) ? 'date' : 'text'} inputMode={isNumber ? 'decimal' : undefined} value={value} disabled={!editable || (sheet === 'Deal ledger' && field === '#')} onChange={(_, data) => onEdit(sheet, row.uid, field, data.value)}/>;
    return <Field key={field} label={field} hint={hint} className={`${isLong ? 'span-all' : ''} ${field === 'Quote and page' ? 'evidence-field' : ''}`}>{input}</Field>;
  })}</div>; }

function SheetTab({ deal, sheet, selectedUid, onSelect, onAdd, onMove, onDelete, onEdit, editable, onJumpRow }) { const rows = sheetRows(deal, sheet), selected = rows.find(row => row.uid === selectedUid) || rows[0], index = rows.findIndex(row => row.uid === selected?.uid), columns = sheetColumns(deal, sheet); const editorRef = useRef(null), listRef = useRef(null); useEffect(() => { if (editorRef.current) editorRef.current.scrollTop = 0; const container = listRef.current, target = container?.querySelector('.sheet-item.selected'); if (container && target) { if (matchMedia('(max-width: 560px)').matches) container.scrollLeft = target.offsetLeft - 14; else container.scrollTop += target.getBoundingClientRect().top - container.getBoundingClientRect().top - Math.min(90, container.clientHeight * 0.22); } }, [selected?.uid]); return <div className="other-sheet"><div className="section-head"><div><h2>{sheet}</h2><span>{count(rows.length, sheet === 'Deal facts' ? 'fact' : sheet === 'Questions' ? 'question' : 'round')}</span></div>{editable && <Button icon={<PlusIcon size={16}/>} size="small" onClick={() => onAdd(sheet)}>Add row</Button>}</div><div className="sheet-body"><div className="sheet-list" ref={listRef}>{rows.map(row => { const values = recordValues(row, sheet), title = sheet === 'Deal facts' ? values.Field : sheet === 'Questions' ? values.Q || values.Question : `Process ${values.Process || '—'} · Round ${values.Round || '—'}`; return <button key={row.uid} className={`sheet-item ${row.uid === selected?.uid ? 'selected' : ''}`} onClick={() => onSelect(sheet, row.uid)}><strong>{title || 'New row'}</strong><span>{sheet === 'Deal facts' ? compact(values.Value) : sheet === 'Questions' ? compact(values.Question) : compact(values['How opened'])}</span></button>; })}{!rows.length && <div className="empty">No records on this sheet.</div>}</div><div className="sheet-editor" ref={editorRef}>{selected ? <><div className="editor-head"><h3>{sheet === 'Deal facts' ? selected.field || 'New fact' : sheet === 'Questions' ? selected.cells?.Q || 'New question' : `Round ${selected.cells?.Round || '—'}`}</h3></div><div className="record-actions">{editable && <><Button size="small" disabled={index <= 0} icon={<ArrowUpIcon size={15}/>} onClick={() => onMove(sheet, selected.uid, -1)}>Move up</Button><Button size="small" disabled={index >= rows.length - 1} icon={<ArrowDownIcon size={15}/>} onClick={() => onMove(sheet, selected.uid, 1)}>Move down</Button><Button size="small" icon={<TrashIcon size={15}/>} onClick={() => onDelete(sheet, selected.uid)}>Delete</Button></>}</div><Issues issues={selected.issues}/><RecordForm sheet={sheet} columns={columns} row={selected} choices={deal.choices} editable={editable} onEdit={onEdit}/>{sheet === 'Questions' && selected.cells?.['Rows affected'] && <ReferenceLinks value={selected.cells['Rows affected']} deal={deal} onJumpRow={onJumpRow}/>}</> : <div className="empty">Select a record or add one.</div>}</div></div></div>; }

function ReferenceLinks({ value, deal, onJumpRow }) { const source = text(value), numbers = new Set(); for (const match of source.matchAll(/#?(\d+)\s*(?:-|–|to)\s*#?(\d+)/g)) { const start = Number(match[1]), end = Number(match[2]); if (end >= start && end - start <= 50) for (let n = start; n <= end; n++) numbers.add(n); } for (const match of source.matchAll(/(?:^|[,;\s])#?(\d+)\b/g)) numbers.add(Number(match[1])); const rows = deal.ledger?.rows?.filter(row => numbers.has(Number(rowId(row)))) || []; return rows.length ? <div className="reference-links"><strong>Referenced events</strong>{rows.map(row => <Button key={row.uid} size="small" onClick={() => onJumpRow(row.uid, true)}>#{rowId(row)} {row.cells?.Event}</Button>)}</div> : null; }

function MechanicalPanel({ deal }) { const check = deal.check || {}, summary = check.summary || {}, warnings = deal.workspace?.reference_warnings || []; const allIssues = [...(deal.ledger?.rows || []).flatMap(row => (row.issues || []).map(issue => ({ ...issue, sheet: 'Deal ledger', row: rowId(row) }))), ...(deal.rounds?.rows || []).flatMap(row => (row.issues || []).map(issue => ({ ...issue, sheet: 'Rounds', row: row.excel_row }))), ...(deal.questions?.rows || []).flatMap(row => (row.issues || []).map(issue => ({ ...issue, sheet: 'Questions', row: rowId(row) }))), ...(check.other_issues || [])]; return <details className="mechanical-panel"><summary>Mechanical check · {summary.errors ?? check.errors ?? 0} errors, {summary.warnings ?? check.warnings ?? 0} warnings · {labelStatus(check.status || 'not checked')}</summary><div className="mechanical-content"><p>Automated checks cover workbook structure and selected consistency rules. They do not establish source completeness or human review.</p>{check.scope_note && <p>{check.scope_note}</p>}{warnings.length > 0 && <div className="reference-warnings"><strong>Reference warnings</strong>{warnings.map((warning, i) => <div key={i}>{warning.message || text(warning)}{warning.question ? ` · ${warning.question}` : ''}</div>)}</div>}{allIssues.length > 0 ? allIssues.map((issue, i) => <div key={i} className={`issue ${issue.severity || 'info'}`}><strong>{issue.sheet || 'Workbook'}{issue.row ? ` · ${issue.row}` : ''} · {issue.code || issue.severity}</strong> {issue.message}</div>) : <p>No mechanical issues listed for this version.</p>}</div></details>; }

function ReviewTab({ deal, editable, open, onToggle, onEdit, onFindEvidence, onOpenDocument }) { const findings = deal.findings || [], documents = deal.documents || []; return <div className="review-tab"><div className="section-head"><div><h2>Review findings</h2><span>{count(findings.length, 'recorded finding')}</span></div></div><p className="section-intro">A finding is a recorded candidate or judgment. Deciding it here does not edit the workbook; a correction needs a separate data edit and verification.</p><MechanicalPanel deal={deal}/>{documents.length > 0 && <div className="documents"><strong>Recorded documents</strong>{documents.map(item => <Button key={item.id} size="small" onClick={() => onOpenDocument(item)}>{item.label}</Button>)}</div>}{findings.length ? findings.map(finding => <article key={finding.id} className="finding"><button className="finding-title" onClick={() => onToggle(open === finding.id ? null : finding.id)} aria-expanded={open === finding.id}><span><strong>{finding.title || finding.id}</strong><small>{[finding.source_label || finding.source_version, finding.rule].filter(Boolean).join(' · ')}</small></span><span className="finding-state">{labelStatus(finding.judgment || 'unreviewed')}<CaretDownIcon size={16}/></span></button>{open === finding.id && <div className="finding-body"><p>{finding.detail}</p>{finding.proposed_change && <div className="finding-proposal"><strong>Recorded reviewer/lead proposal</strong><p>{finding.proposed_change}</p></div>}{finding.recorded_decision && <div className="recorded-decision"><strong>Recorded prior decision by {finding.recorded_decision.actor}</strong><span>{finding.recorded_decision.at}</span><p>{finding.recorded_decision.decision}</p></div>}{finding.recorded_correction && <div className="recorded-decision"><strong>Recorded prior correction{finding.recorded_correction.actor ? ` by ${finding.recorded_correction.actor}` : ""}</strong><span>{[finding.recorded_correction.status && labelStatus(finding.recorded_correction.status), finding.recorded_correction.version, finding.recorded_correction.source_document].filter(Boolean).join(" · ")}</span>{finding.recorded_correction.scope && <p>{finding.recorded_correction.scope}</p>}{finding.recorded_correction.qualification && <p>{finding.recorded_correction.qualification}</p>}</div>}{finding.needs_recheck && <Message type="warning">This finding needs rechecking against the displayed version.</Message>}{finding.evidence?.length > 0 && <div className="finding-evidence"><strong>Recorded evidence</strong>{finding.evidence.map((evidence, index) => <blockquote key={index}>{evidence.quote}<cite>{evidence.page ? `Page ${evidence.page}` : 'Page not recorded'}</cite>{evidence.quote && <Button size="small" onClick={() => onFindEvidence(evidence)}>Find quote in filing</Button>}</blockquote>)}</div>}{finding.source_rows?.length > 0 && <div className="source-rows"><strong>Source row references</strong><span>{finding.source_rows.join(', ')} · These refer to {finding.source_label || finding.source_version || 'the recorded source version'}.</span></div>}<div className="decision-grid"><Field label="Finding judgment"><Select value={finding.judgment || 'unreviewed'} disabled={!editable} onChange={(_, data) => onEdit(finding.id, 'judgment', data.value)}><option value="unreviewed">Unreviewed</option><option value="supported">Supported</option><option value="rejected">Rejected</option><option value="deferred">Deferred</option></Select></Field><Field label="Correction implementation"><Select value={finding.implementation || 'unassessed'} disabled={!editable} onChange={(_, data) => onEdit(finding.id, 'implementation', data.value)}><option value="unassessed">Not assessed</option><option value="not_applied">Not applied</option><option value="applied">Applied</option></Select></Field><Field label="Verification"><Select value={finding.verification || 'unchecked'} disabled={!editable} onChange={(_, data) => onEdit(finding.id, 'verification', data.value)}><option value="unchecked">Unchecked</option><option value="verified">Verified</option></Select></Field></div><Field label="Decision note"><Textarea resize="vertical" rows={3} value={finding.note || ''} disabled={!editable} onChange={(_, data) => onEdit(finding.id, 'note', data.value)}/></Field>{finding.actor && <p className="audit-line">Last decision by {finding.actor}{finding.at ? ` · ${friendlyDate(finding.at)}` : ''}</p>}</div>}</article>) : <div className="empty">No recorded findings for this version.</div>}</div>; }

function ChangesTab({ data, loading }) { return <div className="changes-tab"><div className="section-head"><div><h2>Changes from base</h2><span>{data?.base_label ? `Compared with ${data.base_label}` : 'Working copy comparison'}</span></div></div>{loading && <Spinner label="Loading changes"/>}{!loading && !data?.changes?.length && <div className="empty">No differences from this working copy’s base.</div>}{!loading && data?.changes?.map((change, index) => <Change key={index} change={change}/>)}</div>; }
function formatChangeValue(value) { return typeof value === 'object' ? JSON.stringify(value, null, 2) : text(value); }
function Change({ change }) { return <div className="change"><div className="change-head"><strong>{change.sheet || 'Record'}{change.record_label ? ` · ${change.record_label}` : change.uid ? ` · ${change.uid}` : ''}{change.field ? ` · ${change.field}` : ''}</strong><span>{labelStatus(change.type)}</span></div>{change.before != null && change.before !== '' && <div><span className="change-label">Before</span><pre>{formatChangeValue(change.before)}</pre></div>}{change.after != null && change.after !== '' && <div><span className="change-label">After</span><pre>{formatChangeValue(change.after)}</pre></div>}</div>; }
function HistoryTab({ data, loading, editable, onRestore }) { return <div className="history-tab"><div className="section-head"><div><h2>Revision history</h2><span>Restoring creates a new revision and preserves this record.</span></div></div>{loading && <Spinner label="Loading history"/>}{!loading && !data?.history?.length && <div className="empty">No saved revisions yet.</div>}{!loading && data?.history?.map(item => <article className="history-item" key={item.revision}><div className="history-head"><div><strong>Revision {item.revision}</strong><span>{friendlyDate(item.at)} · {item.actor}</span></div>{editable && <Button size="small" icon={<ArrowClockwiseIcon size={16}/>} onClick={() => onRestore(item.revision)}>Restore</Button>}</div><p>{item.reason || 'Saved edit'}</p>{item.summary && <div className="history-summary">{typeof item.summary === 'string' ? item.summary : JSON.stringify(item.summary)}</div>}{item.changes?.length > 0 && <details><summary>{count(item.changes.length, 'change')}</summary>{item.changes.map((change, i) => <Change key={i} change={change}/>)}</details>}</article>)}</div>; }

createRoot(document.getElementById('root')).render(<FluentProvider theme={webLightTheme}><App/></FluentProvider>);
