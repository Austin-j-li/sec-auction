import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { Button, Field, FluentProvider, Input, Select } from '@fluentui/react-components';
import { ArrowLeftIcon, DownloadSimpleIcon, FloppyDiskIcon, LockSimpleIcon, XIcon } from '@phosphor-icons/react';
import gsap from 'gsap';
import Filing from './Filing';
import SplitPane from './SplitPane';
import TabScroller from './TabScroller';
import Overview from './Overview';
import ActivityPage from './Activity';
import WhatsNew from './WhatsNew';
import { compact, LedgerTab, SheetTab } from './Records';
import { ChangesTab, DocumentText, friendlyDate, HistoryTab, ReviewTab } from './Review';
import { Dot, Loading, Message } from './ui';
import { cockpitTheme } from './theme';
import { commentAction, count, json, markSeen, markSeenOnLeave, recordValues, rowId, saveDeal, sheetColumns, sheetRows, text } from './api';
import { countThreads, displayName, EDIT_KINDS, knownUser } from './trace';
import './style.css';

const SHEETS = { ledger: 'Deal ledger', rounds: 'Rounds', questions: 'Questions', facts: 'Deal facts' };
const SHEET_TABS = Object.fromEntries(Object.entries(SHEETS).map(([key, sheet]) => [sheet, key]));
const TABS = [['ledger', 'Ledger'], ['rounds', 'Rounds'], ['questions', 'Questions'], ['facts', 'Deal facts'], ['review', 'Review'], ['changes', 'Changes'], ['history', 'History']];
const EMPTY = { user: '', can_edit: false, csrf_token: '' };
const NO_FIELDS = new Set();

function routeFromLocation() {
  const match = location.pathname.match(/^\/deal\/([a-z0-9][a-z0-9-]*)\/?$/);
  if (match) return { slug: match[1], page: 'deal' };
  return { slug: null, page: /^\/activity\/?$/.test(location.pathname) ? 'activity' : 'overview' };
}
function clone(value) { return structuredClone(value); }
function confirmLoss() { return window.confirm('You have unsaved edits. Discard them and leave this view?'); }
function failure(title, err) { return { title, detail: err?.message || text(err) }; }

function App() {
  const [route, setRoute] = useState(routeFromLocation);
  const [deals, setDeals] = useState(null);
  const [deal, setDeal] = useState(null);
  const [filing, setFiling] = useState(null);
  const [session, setSession] = useState(EMPTY);
  const [loading, setLoading] = useState(false);
  const [versionLoading, setVersionLoading] = useState(false);
  const [filingLoading, setFilingLoading] = useState(false);
  const [error, setError] = useState(null);
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
  const [threads, setThreads] = useState(null);
  const [threadsError, setThreadsError] = useState('');
  const [news, setNews] = useState(null);
  const [focusThread, setFocusThread] = useState(null);
  const [focusRevision, setFocusRevision] = useState(null);
  const sessionRef = useRef(session);
  const leaveMark = useRef(null);
  const leaving = useRef(null);
  const saveFlash = useRef(null);
  const modalRef = useRef(null);
  const modalReturnFocus = useRef(null);
  const routeSerial = useRef(0);
  const filingCache = useRef(new Map());
  const loadedSlug = useRef(null);
  const reviewTouched = useRef(new Map());
  const findingBase = useRef(new Map());
  const dirty = ops.length > 0;
  const editable = Boolean(session.can_edit && deal?.workspace?.editable && saveState !== 'saving' && !versionLoading);
  const slug = route.slug;
  sessionRef.current = session;

  useEffect(() => { json('/api/session').then(setSession).catch(err => setError(failure('Your session could not be loaded.', err))); }, []);
  useEffect(() => {
    const listener = event => { if (dirty) { event.preventDefault(); event.returnValue = ''; } };
    window.addEventListener('beforeunload', listener);
    return () => window.removeEventListener('beforeunload', listener);
  }, [dirty]);
  useEffect(() => {
    const listener = () => {
      if (saveState === 'saving' || (dirty && !confirmLoss())) { history.pushState(null, '', slug ? `/deal/${slug}${location.hash}` : route.page === 'activity' ? '/activity' : '/'); return; }
      setRoute(routeFromLocation());
    };
    window.addEventListener('popstate', listener);
    return () => window.removeEventListener('popstate', listener);
  }, [dirty, slug, saveState, route.page]);
  useEffect(() => {
    const listener = event => {
      if (!deal || deletePrompt || documentOpen || event.defaultPrevented || event.metaKey || event.ctrlKey || event.altKey || event.target?.closest?.('[role="separator"]') || /^(INPUT|TEXTAREA|SELECT)$/.test(event.target?.tagName || '')) return;
      if (event.key === 'j' || event.key === 'ArrowDown') { event.preventDefault(); stepRow(1); }
      if (event.key === 'k' || event.key === 'ArrowUp') { event.preventDefault(); stepRow(-1); }
    };
    window.addEventListener('keydown', listener);
    return () => window.removeEventListener('keydown', listener);
  });
  useEffect(() => {
    if (!saveFlash.current || saveState !== 'saved' || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    const tween = gsap.fromTo(saveFlash.current, { opacity: 0 }, { opacity: 1, duration: 0.24, ease: 'power2.out' });
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
  useEffect(() => { if (!ops.length) { reviewTouched.current = new Map(); findingBase.current = new Map(); } }, [ops.length]);

  // Which fields carry a staged value, by sheet and record: drives the per-field "edited" marker.
  const dirtyFields = useMemo(() => {
    const map = new Map();
    const add = (key, fields) => { if (!map.has(key)) map.set(key, new Set()); fields.forEach(field => map.get(key).add(field)); };
    for (const op of ops) {
      if (op.type === 'update') add(`${op.sheet}|${op.uid}`, Object.keys(op.values || {}));
      if (op.type === 'insert') add(`${op.sheet}|${op.client_uid}`, Object.entries(op.values || {}).filter(([, value]) => text(value) !== '').map(([field]) => field));
    }
    return map;
  }, [ops]);
  const dirtyFor = useCallback((sheet, uid) => dirtyFields.get(`${sheet}|${uid}`) || NO_FIELDS, [dirtyFields]);
  const reviewDirty = useCallback(uid => (ops.some(op => op.type === 'review' && op.uid === uid) && reviewTouched.current.get(uid)) || NO_FIELDS, [ops]);
  // A finding field is edited when its staged value differs from the value loaded before the first edit.
  const findingDirty = useCallback(id => {
    const base = findingBase.current.get(id), op = ops.find(item => item.type === 'finding' && item.id === id);
    return base && op ? new Set(Object.keys(base).filter(field => op[field] !== base[field])) : NO_FIELDS;
  }, [ops]);

  function navigate(path) {
    if (saveState === 'saving') return;
    if (dirty && !confirmLoss()) return;
    history.pushState(null, '', path);
    setRoute(routeFromLocation());
  }
  const load = useCallback(async (currentSlug, currentVersion = 'working') => {
    const token = ++routeSerial.current;
    // A version switch keeps the current deal (and the filing pane) mounted; only the workspace waits.
    const sameDeal = Boolean(currentSlug) && loadedSlug.current === currentSlug;
    setError(null); setConflict(false); setOps([]); setSaveState(''); setHistoryData(null); setChangesData(null); setFindingOpen(null); setDocumentOpen(null);
    if (sameDeal) setVersionLoading(true);
    else { setLoading(true); setDeal(null); loadedSlug.current = null; }
    try {
      if (!currentSlug) {
        await leaving.current; // the overview's "since you last looked" must reflect a deal just left
        const list = await json('/api/deals');
        if (token === routeSerial.current) { setDeals(list); document.title = 'Ledger cockpit'; }
      } else {
        const data = await json(`/api/deal/${currentSlug}?version=${encodeURIComponent(currentVersion)}`);
        if (token !== routeSerial.current) return;
        loadedSlug.current = currentSlug;
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
          json(`/api/filing/${currentSlug}`)
            .then(source => { filingCache.current.set(currentSlug, source); if (token === routeSerial.current) setFiling(source); })
            .catch(err => { if (token === routeSerial.current) setFilingError(err.message); })
            .finally(() => { if (token === routeSerial.current) setFilingLoading(false); });
        }
      }
    } catch (err) {
      if (token === routeSerial.current) setError(failure(currentSlug ? 'This deal could not be loaded.' : 'The deal list could not be loaded.', err));
    } finally {
      if (token === routeSerial.current) { setLoading(false); setVersionLoading(false); }
    }
  }, []);
  useEffect(() => { load(slug, 'working'); }, [slug, route.page, load]);
  // Comment threads are deal-level (shared by every version); immutable versions show them read only.
  useEffect(() => {
    setThreads(null); setThreadsError(''); setFocusThread(null); setFocusRevision(null);
    if (!slug) return;
    let alive = true;
    json(`/api/deal/${slug}/comments`)
      .then(data => { if (alive) setThreads(data?.threads || []); })
      .catch(err => { if (alive) setThreadsError(err.message); });
    return () => { alive = false; };
  }, [slug]);
  // What's new: a snapshot of the unseen activity when the deal opens. Signed-in users only.
  useEffect(() => {
    setNews(null);
    if (!slug || !knownUser(session.user)) return;
    let alive = true;
    json(`/api/deal/${slug}/activity?limit=200`)
      .then(data => {
        const items = data?.items || [], unseen = items.filter(item => item.unseen);
        if (!alive || !unseen.length) return;
        setNews({ slug, items: unseen, previous: data.seen?.activity_id ?? 0, newest: items[0].id, status: 'pending', busy: false, error: '' });
        leaveMark.current = { slug, id: items[0].id };
      })
      .catch(() => {});
    return () => { alive = false; };
  }, [slug, session.user]);
  // Leaving a deal whose What's new panel was shown marks it read, unless the reader already chose read or unread.
  useEffect(() => {
    if (!slug) return;
    const flush = () => {
      const pending = leaveMark.current;
      leaveMark.current = null;
      if (pending && sessionRef.current.csrf_token) leaving.current = markSeenOnLeave(pending.slug, sessionRef.current, pending.id);
    };
    window.addEventListener('pagehide', flush);
    return () => { window.removeEventListener('pagehide', flush); flush(); };
  }, [slug]);
  useEffect(() => {
    if (!slug || !deal || !['changes', 'history'].includes(tab)) return;
    let alive = true;
    setAuxLoading(true);
    json(`/api/deal/${slug}/${tab}`)
      .then(data => { if (alive) { if (tab === 'changes') setChangesData(data); else setHistoryData(data); } })
      .catch(err => { if (alive) setError(failure(tab === 'changes' ? 'Changes could not be loaded.' : 'History could not be loaded.', err)); })
      .finally(() => { if (alive) setAuxLoading(false); });
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
  async function setSeen(status) {
    if (!news) return;
    leaveMark.current = null;
    setNews(current => ({ ...current, busy: true, error: '' }));
    try {
      const result = await markSeen(slug, session, status === 'read' ? news.newest : news.previous);
      if (result?.seen !== undefined) setDeal(current => current && ({ ...current, seen: result.seen }));
      setNews(current => ({ ...current, status, busy: false }));
    } catch (err) {
      setNews(current => ({ ...current, busy: false, error: `${status === 'read' ? 'Marking as read' : 'Marking unread'} failed: ${err.message}` }));
    }
  }
  function openRevision(revision) {
    if (revision == null) return;
    setTab('history'); setFocusRevision({ revision, nonce: Date.now() }); setMobilePane('workspace');
  }
  function openThread(target, threadId) {
    setFocusThread({ threadId, nonce: Date.now() });
    if (target?.kind === 'row' && sheetRows(deal, target.sheet).some(row => row.uid === target.uid)) {
      if (target.sheet === 'Deal ledger') selectRow(target.uid);
      else { selectOther(target.sheet, target.uid); setTab(SHEET_TABS[target.sheet]); }
    } else {
      if (target?.kind === 'finding') setFindingOpen(target.uid);
      setTab('review');
    }
    setMobilePane('workspace');
  }
  function openActivityItem(item) {
    if (EDIT_KINDS.has(item.kind)) openRevision(item.revision);
    else openThread(item.target, item.thread_id);
  }
  async function postComment(action) {
    const data = await commentAction(slug, session, action);
    setThreads(data?.threads || []);
  }

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
    const idLabel = sheet === 'Deal ledger' ? `#${rowId(row)}` : '';
    const label = sheet === 'Deal ledger' ? compact(row.cells?.Event, 50) : sheet === 'Deal facts' ? row.field : compact(row.cells?.Q || row.cells?.Question || row.cells?.Round, 70);
    setDeletePrompt({ sheet, uid, hasReferences: Boolean(row.has_references), idLabel, label, replacement: '' });
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
  // Review notes became comments (phase 1): the review operation carries only the status and an empty note.
  function setReview(uid, status) {
    const previous = deal.row_review?.[uid] || { status: 'unreviewed' };
    const touched = new Set(reviewTouched.current.get(uid) || []);
    if ((previous.status || 'unreviewed') !== status) touched.add('status');
    reviewTouched.current.set(uid, touched);
    setDeal(current => { const next = clone(current); next.row_review = { ...next.row_review, [uid]: { ...(next.row_review?.[uid] || {}), status } }; return next; });
    setOps(previousOps => {
      const next = clone(previousOps), existing = next.find(op => op.type === 'review' && op.uid === uid);
      if (existing) Object.assign(existing, { status, note: '' }); else next.push({ type: 'review', uid, status, note: '' });
      return next;
    });
    setSaveState('');
  }
  function setFinding(id, field, value) {
    if (!findingBase.current.has(id)) {
      const finding = deal.findings.find(item => item.id === id);
      findingBase.current.set(id, { judgment: finding.judgment || 'unreviewed', implementation: finding.implementation || 'unassessed', verification: finding.verification || 'unchecked' });
    }
    setDeal(current => { const next = clone(current), finding = next.findings?.find(item => item.id === id); if (finding) finding[field] = value; return next; });
    setOps(previous => {
      const next = clone(previous), existing = next.find(op => op.type === 'finding' && op.id === id);
      if (existing) existing[field] = value;
      else {
        const finding = deal.findings.find(item => item.id === id);
        next.push({ type: 'finding', id, judgment: finding.judgment || 'unreviewed', implementation: finding.implementation || 'unassessed', verification: finding.verification || 'unchecked', note: '', [field]: value });
      }
      return next;
    });
    setSaveState('');
  }
  async function save() {
    if (!dirty || !editable || saveState === 'saving' || conflict) return;
    setSaveState('saving'); setError(null);
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
    } catch (err) {
      setError(err.status === 409 ? failure('Another editor saved a newer revision. Your unsaved edits remain in this browser.', err) : failure('Your changes could not be saved.', err));
      setConflict(err.status === 409); setSaveState('error');
    }
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
    setError(null); setSaveState('saving');
    try {
      const result = await saveDeal(slug, session, { revision: deal.workspace.revision, base_sha256: deal.workspace.base_sha256, reason: `Restore revision ${revision}`, operations: [{ type: 'restore', target_revision: revision }] });
      setDeal(result); setOps([]); setHistoryData(null); setChangesData(null); setSaveState('saved');
      setSelectedUid(result.ledger?.rows?.some(row => row.uid === selectedUid) ? selectedUid : result.ledger?.rows?.[0]?.uid || null);
      setSelectedBySheet({});
    } catch (err) {
      setError(err.status === 409 ? failure('Another editor saved a newer revision. Your unsaved edits remain in this browser.', err) : failure('The revision could not be restored.', err));
      setConflict(err.status === 409); setSaveState('error');
    }
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
    if (!row) { setError({ title: 'Select a ledger event before using filing text.' }); return; }
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

  if (!slug) {
    const activity = route.page === 'activity';
    return <>
      <Header onNavigate={navigate} session={session} page={route.page}/>
      <main className="overview-wrap">
        {loading && !activity && <Loading label="Loading deals"/>}
        {error && <Message type="error" title={error.title} detail={error.detail}/>}
        {activity ? <ActivityPage deals={deals} onOpenDeal={s => navigate(`/deal/${s}`)}/> : deals && <Overview deals={deals} onOpen={s => navigate(`/deal/${s}`)}/>}
      </main>
    </>;
  }

  const ledgerRows = deal?.ledger?.rows || [];
  const selected = ledgerRows.find(row => row.uid === selectedUid);
  const baseLabel = deal?.versions?.find(item => item.id === deal.workspace?.base_version)?.label || deal?.workspace?.base_version || 'base';
  const versionLabel = item => item.kind === 'working'
    ? `Working copy · editable`
    : `${item.label || item.id}${item.instruction_version ? ` · ${item.instruction_version}` : ''} · original, read only`;
  const lastSaved = deal?.workspace?.updated_by ? `Last saved by ${deal.workspace.updated_by}${deal.workspace.updated_at ? ` · ${friendlyDate(deal.workspace.updated_at)}` : ''}` : '';
  const immutable = deal?.workspace?.selected_version !== 'working';
  const sublineParts = deal ? [deal.filing?.form_type, deal.filing?.date_filed, ...(immutable
    ? ['Original extraction, read only']
    : [`Working copy from ${baseLabel}`, `Revision ${deal.workspace?.revision}`])] : [];
  const showDock = dirty && session.can_edit && deal?.workspace?.editable;
  const workState = versionLoading ? { tone: 'muted', label: 'Loading version' }
    : dirty
    ? { tone: 'warning', label: `${ops.length} unsaved ${count(ops.length, 'change').split(' ').slice(1).join(' ')}` }
    : saveState === 'saved' ? { tone: 'success', label: 'Saved' }
    : editable ? { tone: 'muted', label: 'No unsaved edits' }
    : { tone: 'muted', label: 'Read only version' };
  const trace = deal && {
    user: session.user, threads, threadsError, focus: focusThread, post: postComment, onOpenRevision: openRevision,
    canComment: Boolean(session.can_edit && knownUser(session.user) && !immutable && !versionLoading && threads && !threadsError),
    counts: threads ? countThreads(threads) : deal.thread_counts || {},
    authors: deal.field_authors || {}, seenRevision: deal.seen?.revision,
  };

  return <>
    <Header onNavigate={navigate} session={session} page={route.page}/>
    <main className="deal-shell">
      {loading && <Loading label={`Loading ${slug}`}/>}
      {error && <Message type={conflict ? 'warning' : 'error'} title={error.title} detail={error.detail}>
        {conflict && <span className="message-actions">
          <Button appearance="secondary" onClick={downloadDraft}>Download staged edits</Button>
          <Button appearance="secondary" onClick={discardAndReload}>Discard edits and load latest</Button>
        </span>}
        {!deal && !loading && <span className="message-actions">
          <Button appearance="subtle" className="link-button" icon={<ArrowLeftIcon size={16}/>} onClick={() => navigate('/')}>All deals</Button>
        </span>}
      </Message>}
      {deal && <>
        <header className="deal-toolbar">
          <div className="deal-identity">
            <Button appearance="subtle" className="back-link" icon={<ArrowLeftIcon size={16}/>} onClick={() => navigate('/')}>All deals</Button>
            <h1>{deal.name || deal.facts?.find(f => f.field === 'Target')?.value || slug}</h1>
            <div className="deal-subline mono">
              {sublineParts.map((part, i) => <React.Fragment key={i}>{i > 0 && ' '}<span>{i > 0 && '· '}{part}</span></React.Fragment>)}
            </div>
          </div>
          <div className="toolbar-actions">
            <label className="version-control">
              <span>Version</span>
              {immutable && <LockSimpleIcon size={14} className="tone-muted" aria-hidden="true"/>}
              <Select aria-label="Version" title={immutable ? 'Read only version' : undefined} value={version} onChange={(_, data) => switchVersion(data.value)} disabled={saveState === 'saving'}>
                {(deal.versions || []).map(item => <option value={item.id} key={item.id}>{versionLabel(item)}</option>)}
              </Select>
            </label>
            <Button as="a" appearance="secondary" className="export-button" href={`/api/deal/${slug}/export?version=${encodeURIComponent(version)}`} download icon={<DownloadSimpleIcon size={16}/>}>Export Excel</Button>
            <div className="save-line">
              <span className={`work-state ${dirty ? 'unsaved' : ''}`} aria-live="polite" title={lastSaved || undefined}><Dot tone={workState.tone}/>{workState.label}</span>
              <span ref={saveFlash} className="save-feedback">{saveState === 'saved' ? 'Revision saved' : ''}</span>
            </div>
            <Button appearance="primary" className="save-button" icon={<FloppyDiskIcon size={16}/>} disabled={!dirty || !editable || saveState === 'saving' || conflict} onClick={save}>{saveState === 'saving' ? 'Saving…' : 'Save changes'}</Button>
          </div>
        </header>
        <div className="mobile-switch" role="group" aria-label="Visible pane">
          <Button appearance={mobilePane === 'filing' ? 'primary' : 'secondary'} aria-pressed={mobilePane === 'filing'} onClick={() => setMobilePane('filing')}>Filing</Button>
          <Button appearance={mobilePane === 'workspace' ? 'primary' : 'secondary'} aria-pressed={mobilePane === 'workspace'} onClick={() => setMobilePane('workspace')}>Workspace</Button>
        </div>
        <SplitPane className="workbench" name="Filing and workspace" storageKey="workbench" collapsible defaultSize={width => width * 0.47} minStart={280} minEnd={400}>
          <div className={`filing-column ${mobilePane === 'filing' ? 'mobile-active' : ''}`}>
            <Filing filing={filing} loading={filingLoading} error={filingError} deal={deal} selectedUid={selectedUid} scrollRequest={filingScrollRequest} searchRequest={filingSearchRequest} onSelectRow={selectRow} onQuoteSelection={editable ? chooseQuote : null}/>
          </div>
          <section className={`workspace-column ${mobilePane === 'workspace' ? 'mobile-active' : ''} ${showDock ? 'has-dock' : ''}`} aria-label="Deal workspace">
            {news?.slug === slug && <WhatsNew news={news} onMarkRead={() => setSeen('read')} onMarkUnread={() => setSeen('unread')} onOpenItem={openActivityItem}/>}
            <TabScroller activeTab={tab}>
              {TABS.map(([key, label]) => {
                const tabCount = ['ledger', 'rounds', 'questions'].includes(key) ? sheetRows(deal, SHEETS[key]).length : key === 'review' && deal.findings?.length > 0 ? deal.findings.length : null;
                return <button key={key} id={`tab-${key}`} role="tab" aria-selected={tab === key} aria-controls="workspace-panel" tabIndex={tab === key ? 0 : -1} className={tab === key ? 'active' : ''} onClick={() => setTab(key)}>
                  {label}{tabCount != null && <span className="tab-count mono">{tabCount}</span>}
                </button>;
              })}
            </TabScroller>
            <div id="workspace-panel" className={`workspace-scroll ${['ledger', 'rounds', 'questions', 'facts'].includes(tab) ? 'editor-scroll' : ''}`} role="tabpanel" aria-labelledby={`tab-${tab}`}>
              {versionLoading && <Loading label="Loading version"/>}
              {!versionLoading && <>
                {tab === 'ledger' && <LedgerTab deal={deal} selectedUid={selectedUid} onSelect={selectRow} onShowFiling={showRowEvidence} onOpenQuestion={openQuestion} onStep={stepRow} onAdd={addRow} onMove={moveRow} onDelete={requestDelete} onEdit={editValue} onReview={setReview} editable={editable} selection={selected} dirtyFor={dirtyFor} reviewDirty={reviewDirty} trace={trace}/>}
                {['rounds', 'questions', 'facts'].includes(tab) && <SheetTab deal={deal} sheet={SHEETS[tab]} selectedUid={selectedBySheet[SHEETS[tab]]} onSelect={selectOther} onAdd={addRow} onMove={moveRow} onDelete={requestDelete} onEdit={editValue} editable={editable} onJumpRow={selectRow} dirtyFor={dirtyFor} trace={trace}/>}
                {tab === 'review' && <ReviewTab deal={deal} editable={editable} open={findingOpen} onToggle={setFindingOpen} onEdit={setFinding} dirtyFor={findingDirty} onFindEvidence={findEvidence} onOpenDocument={openDocument} trace={trace}/>}
                {tab === 'changes' && <ChangesTab data={changesData} loading={auxLoading}/>}
                {tab === 'history' && <HistoryTab data={historyData} loading={auxLoading} editable={editable} onRestore={restore} lastSaved={lastSaved} focus={focusRevision}/>}
              </>}
            </div>
            {showDock && <div className="save-dock">
              <Field label="Reason for this revision" hint="Appears in history" orientation="horizontal">
                <Input value={reason} title="Appears in history" disabled={saveState === 'saving'} onChange={(_, data) => setReason(data.value)} placeholder="Describe the edit"/>
              </Field>
              <Button appearance="primary" className="save-button" icon={<FloppyDiskIcon size={16}/>} disabled={saveState === 'saving' || conflict} onClick={save}>Save {count(ops.length, 'change')}</Button>
            </div>}
          </section>
        </SplitPane>
      </>}
    </main>
    {deletePrompt && <div className="modal-backdrop" role="presentation">
      <div className="modal" ref={modalRef} role="dialog" aria-modal="true" aria-label="Delete record">
        <div className="modal-head">
          <h2>Delete {deletePrompt.idLabel && <><span className="mono">{deletePrompt.idLabel}</span> </>}{deletePrompt.label}?</h2>
          <Button appearance="subtle" className="icon-button" onClick={() => setDeletePrompt(null)} aria-label="Close" icon={<XIcon size={16}/>}/>
        </div>
        <p>This deletion is staged until you save. The record can be recovered from history after saving.</p>
        {deletePrompt.sheet === 'Deal ledger' && deletePrompt.hasReferences && <Field label="Replacement event" hint="This event has explicit references. Choose the event they should point to before deleting.">
          <Select value={deletePrompt.replacement} onChange={(_, data) => setDeletePrompt(value => ({ ...value, replacement: data.value }))}>
            <option value="">Choose a replacement</option>
            {ledgerRows.filter(row => row.uid !== deletePrompt.uid).map(row => <option key={row.uid} value={row.uid}>{row.uid.startsWith('new-') ? 'New event' : `#${rowId(row)}`} · {compact(row.cells?.Event, 35)}</option>)}
          </Select>
        </Field>}
        <div className="modal-actions">
          <Button appearance="secondary" onClick={() => setDeletePrompt(null)}>Cancel</Button>
          <Button appearance="secondary" className="danger-outline" disabled={deletePrompt.hasReferences && !deletePrompt.replacement} onClick={deleteRow}>Stage deletion</Button>
        </div>
      </div>
    </div>}
    {documentOpen && <div className="modal-backdrop" role="presentation">
      <div className="modal document-modal" ref={modalRef} role="dialog" aria-modal="true" aria-label="Recorded document">
        <div className="modal-head">
          <h2>{documentData?.title || documentOpen.label}</h2>
          <Button appearance="subtle" className="icon-button" onClick={() => setDocumentOpen(null)} aria-label="Close" icon={<XIcon size={16}/>}/>
        </div>
        {docLoading ? <Loading label="Loading document"/>
          : documentError ? <Message type="error" title="The document could not be loaded." detail={documentError}/>
          : <DocumentText value={documentData?.text}/>}
      </div>
    </div>}
  </>;
}

function Header({ onNavigate, session, page }) {
  const access = !session.user ? { tone: 'warning', label: 'Loading session' } : session.can_edit ? { tone: 'success', label: 'Edit access' } : { tone: 'muted', label: 'Read only' };
  const follow = path => event => {
    if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault(); onNavigate(path);
  };
  return <header className="global-header">
    <Button appearance="subtle" className="wordmark" onClick={() => onNavigate('/')}>Ledger cockpit</Button>
    <span className="header-context">{page === 'deal' ? 'Deal workspace' : page === 'activity' ? 'Activity' : 'Deal ledgers'}</span>
    <div className="header-user">
      {page !== 'activity' && <a className="header-link" href="/activity" onClick={follow('/activity')}>Activity</a>}
      {session.user && <span className="header-name">{displayName(session.user)}</span>}
      <span className="access-state"><Dot tone={access.tone}/>{access.label}</span>
    </div>
  </header>;
}

createRoot(document.getElementById('root')).render(<FluentProvider theme={cockpitTheme} className="cockpit"><App/></FluentProvider>);
