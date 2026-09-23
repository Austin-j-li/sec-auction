import React, { useEffect, useRef, useState } from 'react';
import { Button, Field, Input } from '@fluentui/react-components';
import { ArrowLeftIcon, MagnifyingGlassIcon, XIcon } from '@phosphor-icons/react';
import { dealsAction, json } from './api';
import { formatBytes, LOOKUP_ACTIVE, seedAction, seedReview, validName, validSlug } from './deals';
import { Empty, Loading, Message } from './ui';

const LOOKUP_POLL_MS = 1000;

// Add a deal from the seed list or a pasted EDGAR link. The worker fetches the filing;
// the person then picks the document, checks the name and adds it (optionally extracting at once).
export default function AddDealDialog({ session, dialogRef, onClose, onOpen, onAdded }) {
  const [tab, setTab] = useState('seed');
  const [query, setQuery] = useState('');
  const [results, setResults] = useState(null);
  const [searchError, setSearchError] = useState('');
  const [url, setUrl] = useState('');
  const [seedRow, setSeedRow] = useState(null);
  const [lookup, setLookup] = useState(null);
  const [choice, setChoice] = useState({ document: '', name: '', slug: '' });
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const searchSerial = useRef(0);

  useEffect(() => {
    const text = query.trim();
    if (!text) { setResults(null); setSearchError(''); return; }
    const serial = ++searchSerial.current;
    const timer = setTimeout(() => {
      json(`/api/seed?${new URLSearchParams({ q: text })}`)
        .then(data => { if (serial === searchSerial.current) { setResults(data?.rows || []); setSearchError(''); } })
        .catch(err => { if (serial === searchSerial.current) setSearchError(err.message); });
    }, 200);
    return () => clearTimeout(timer);
  }, [query]);

  // Poll a running lookup; when it completes, preselect its document and suggested names.
  useEffect(() => {
    if (!lookup || !LOOKUP_ACTIVE.has(lookup.state)) return;
    const timer = setTimeout(async () => {
      try {
        const next = await json(`/api/lookup/${lookup.id}`);
        setLookup(next);
        if (next.state === 'completed' && next.result) {
          setChoice({ document: next.result.preselected || '', name: next.result.suggested?.name || '', slug: next.result.suggested?.slug || '' });
        }
      } catch (err) { setLookup(current => current && { ...current, state: 'failed', error: err.message }); }
    }, LOOKUP_POLL_MS);
    return () => clearTimeout(timer);
  }, [lookup]);

  async function startLookup(link, row = null) {
    setError(''); setBusy(true); setSeedRow(row);
    try {
      const data = await dealsAction(session, { action: 'lookup', url: link, ...(row ? { seed_deal: row.deal } : {}) });
      setLookup(data.lookup);
    } catch (err) { setError(err.message); }
    finally { setBusy(false); }
  }
  function chooseSeed(row) {
    const action = seedAction(row);
    if (action === 'open') onOpen(row.deal);
    else if (action === 'lookup') startLookup(row.index_url, row);
    else { setSeedRow(row); setTab('link'); setUrl(''); setError(''); }
  }
  async function add(extract) {
    setError(''); setBusy(true);
    try {
      const data = await dealsAction(session, { action: 'add', lookup_id: lookup.id, document: choice.document, slug: choice.slug.trim(), name: choice.name.trim() });
      onAdded(data.slug, extract);
    } catch (err) { setError(`The deal could not be added: ${err.message}`); setBusy(false); }
  }
  function back() { setLookup(null); setError(''); setChoice({ document: '', name: '', slug: '' }); }

  const result = lookup?.state === 'completed' ? lookup.result : null;
  const chosen = result?.documents?.find(doc => doc.filename === choice.document);
  const ready = Boolean(chosen?.html && validSlug(choice.slug.trim()) && validName(choice.name));

  return <div className="modal-backdrop" role="presentation">
    <div className="modal add-deal-modal" ref={dialogRef} role="dialog" aria-modal="true" aria-label="Add a deal">
      <div className="modal-head">
        <h2>Add a deal</h2>
        <Button appearance="subtle" className="icon-button" disabled={busy} onClick={onClose} aria-label="Close" icon={<XIcon size={16}/>}/>
      </div>

      {!lookup && <>
        <div className="segmented" role="tablist" aria-label="Source">
          {[['seed', 'Search the seed'], ['link', 'Paste a link']].map(([key, label]) =>
            <button key={key} type="button" role="tab" aria-selected={tab === key} className={tab === key ? 'active' : ''} onClick={() => { setTab(key); setError(''); }}>{label}</button>)}
        </div>
        {tab === 'seed' && <div className="seed-search">
          <Field label="Deal name">
            <Input data-autofocus value={query} contentBefore={<MagnifyingGlassIcon size={16} aria-hidden="true"/>} placeholder="Type part of a target name" onChange={(_, data) => setQuery(data.value)}/>
          </Field>
          {searchError && <p className="run-error mono">{searchError}</p>}
          {results && !results.length && <Empty>No seed rows match.</Empty>}
          {results?.length > 0 && <ul className="seed-results" aria-label="Seed rows">
            {results.map(row => {
              const review = seedReview(row.status), action = seedAction(row);
              return <li key={row.deal}>
                <div>
                  <strong>{row.target_name}</strong>
                  <small className="mono">{row.deal} · {row.form_type} · {row.date_filed}</small>
                  {review && <small className="tone-warning">Needs review: {review}</small>}
                </div>
                <Button appearance={action === 'open' ? 'subtle' : 'secondary'} disabled={busy} onClick={() => chooseSeed(row)}>
                  {action === 'open' ? 'Open' : action === 'lookup' ? 'Choose' : 'Paste link'}
                </Button>
              </li>;
            })}
          </ul>}
        </div>}
        {tab === 'link' && <form onSubmit={event => { event.preventDefault(); if (url.trim()) startLookup(url.trim(), seedRow); }}>
          {seedRow && <p>The seed has no usable link for <strong>{seedRow.target_name}</strong> ({seedReview(seedRow.status)}). Paste the filing's EDGAR link.</p>}
          <Field label="EDGAR link" hint="A filing index (…-index.htm), a complete submission (.txt) or a document under www.sec.gov/Archives/edgar/data/">
            <Input data-autofocus className="mono" value={url} onChange={(_, data) => setUrl(data.value)} placeholder="https://www.sec.gov/Archives/edgar/data/…"/>
          </Field>
          <div className="modal-actions">
            <Button type="submit" appearance="primary" disabled={busy || !url.trim()}>{busy ? 'Looking up…' : 'Look up'}</Button>
          </div>
        </form>}
      </>}

      {lookup && LOOKUP_ACTIVE.has(lookup.state) && <Loading label="Fetching the filing from EDGAR"/>}
      {lookup?.state === 'failed' && <>
        <Message type="error" title="The filing could not be fetched." detail={lookup.error}/>
        <div className="modal-actions"><Button appearance="secondary" icon={<ArrowLeftIcon size={16}/>} onClick={back}>Back</Button></div>
      </>}

      {result && <form className="lookup-result" onSubmit={event => { event.preventDefault(); if (ready) add(false); }}>
        <p className="mono lookup-head">{[result.form_type, result.date_filed && `filed ${result.date_filed}`, result.header?.subject_company || result.header?.filer].filter(Boolean).join(' · ')}</p>
        {result.warnings?.map(text => <Message key={text} type="warning" title={text}/>)}
        <fieldset className="document-choice">
          <legend>Document to extract from</legend>
          {result.documents.map(doc => <label key={doc.filename} className={doc.html ? '' : 'disabled'}>
            <input type="radio" name="document" value={doc.filename} checked={choice.document === doc.filename} disabled={!doc.html}
              onChange={() => setChoice(current => ({ ...current, document: doc.filename }))}/>
            <span>
              <span className="mono">{doc.type}</span> {doc.description && doc.description !== doc.type ? doc.description : ''}
              <small className="mono">{doc.filename} · {formatBytes(doc.bytes)}{doc.html ? '' : ' · not HTML'}</small>
            </span>
          </label>)}
        </fieldset>
        {chosen && !chosen.background && <Message type="warning" title="This document has no “Background of the Merger” or similar heading." detail="You can still add it."/>}
        <Field label="Deal name" validationState={validName(choice.name) ? 'none' : 'error'} validationMessage={validName(choice.name) ? undefined : 'Give the deal a name (up to 120 characters)'}>
          <Input value={choice.name} onChange={(_, data) => setChoice(current => ({ ...current, name: data.value }))}/>
        </Field>
        <Field label="Short name" hint="Used in links and file names; cannot be changed later" validationState={validSlug(choice.slug.trim()) ? 'none' : 'error'}
          validationMessage={validSlug(choice.slug.trim()) ? undefined : 'Lower-case letters, digits and hyphens'}>
          <Input className="mono" value={choice.slug} onChange={(_, data) => setChoice(current => ({ ...current, slug: data.value }))}/>
        </Field>
        {result.seed && <p className="lookup-source">From the seed row <span className="mono">{result.seed.deal}</span>.</p>}
        {error && <p className="run-failure tone-error" role="alert">{error}</p>}
        <div className="modal-actions">
          <Button appearance="secondary" icon={<ArrowLeftIcon size={16}/>} disabled={busy} onClick={back}>Back</Button>
          <Button type="submit" appearance="secondary" disabled={busy || !ready}>{busy ? 'Adding…' : 'Add'}</Button>
          <Button appearance="primary" disabled={busy || !ready} onClick={() => add(true)}>Add and extract</Button>
        </div>
      </form>}
      {!result && error && <p className="run-failure tone-error" role="alert">{error}</p>}
    </div>
  </div>;
}
