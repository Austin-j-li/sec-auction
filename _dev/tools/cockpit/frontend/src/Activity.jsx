import React, { useEffect, useRef, useState } from 'react';
import { Button, Field, Select } from '@fluentui/react-components';
import { activityQuery, json, text } from './api';
import { displayName, INSTRUCTION_KINDS, KIND_LABELS, shortTime } from './trace';
import { Empty, Loading, Message } from './ui';

// Account-wide activity: every save and comment action across deals, newest first, filterable by person, deal and type.

const PAGE = 100;
const PEOPLE = ['austin', 'alex', 'local'];

export default function ActivityPage({ deals, onOpenDeal, onOpenInstructions }) {
  const [filters, setFilters] = useState({ actor: '', slug: '', kind: '' });
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [more, setMore] = useState(false);
  const serial = useRef(0);
  const names = new Map((deals || []).map(item => [item.slug, item.name || item.target || item.slug]));

  async function fetchPage(before = '') {
    const token = ++serial.current;
    setLoading(true); setError('');
    try {
      const data = await json(activityQuery({ ...filters, before, limit: PAGE }));
      if (token !== serial.current) return;
      const list = Array.isArray(data) ? data : data?.items || [];
      setItems(current => before ? [...current, ...list] : list);
      setMore(list.length === PAGE);
    } catch (err) {
      if (token === serial.current) setError(err.message);
    } finally {
      if (token === serial.current) setLoading(false);
    }
  }
  useEffect(() => { document.title = 'Activity · Ledger cockpit'; }, []);
  useEffect(() => { fetchPage(); }, [filters.actor, filters.slug, filters.kind]);
  const setFilter = key => (_, data) => setFilters(current => ({ ...current, [key]: data.value }));
  function onLinkClick(event, slug, version) {
    if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault(); onOpenDeal(slug, version);
  }
  // Instruction events are account-wide (slug ""): they link to the Instructions page, at the version when the feed names it.
  const instructionHref = item => `/instructions${item.instruction_id ? `?id=${encodeURIComponent(item.instruction_id)}` : ''}`;
  function onInstructionClick(event, item) {
    if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault(); onOpenInstructions(item.instruction_id || null);
  }
  // A finished extraction links to the version it produced (when the feed names it).
  const versionHref = item => `/deal/${item.slug}?version=${encodeURIComponent(item.version_id)}`;

  return <>
    <div className="overview-title">
      <h1>Activity</h1>
      <p>Every saved revision, comment action, extraction run and instruction change, newest first</p>
    </div>
    <div className="activity-filters">
      <Field label="Person"><Select value={filters.actor} onChange={setFilter('actor')}>
        <option value="">Everyone</option>
        {PEOPLE.map(actor => <option key={actor} value={actor}>{displayName(actor)}</option>)}
      </Select></Field>
      <Field label="Deal"><Select value={filters.slug} onChange={setFilter('slug')}>
        <option value="">All deals</option>
        {(deals || []).map(item => <option key={item.slug} value={item.slug}>{names.get(item.slug)}</option>)}
      </Select></Field>
      <Field label="Type"><Select value={filters.kind} onChange={setFilter('kind')}>
        <option value="">All types</option>
        {Object.entries(KIND_LABELS).map(([kind, label]) => <option key={kind} value={kind}>{label}</option>)}
      </Select></Field>
    </div>
    {error && <Message type="error" title="Activity could not be loaded." detail={error}/>}
    {items.length > 0 && <div className="deal-table-wrap">
      <table className="deal-table activity-table">
        <thead><tr><th>When</th><th>Person</th><th>Deal</th><th>Type</th><th>Detail</th></tr></thead>
        <tbody>
          {items.map(item => <tr key={`${item.slug || '-'}-${item.kind}-${item.id}`}>
            <td className="mono">{shortTime(item.at)}</td>
            <td>{displayName(item.actor)}</td>
            <td>{item.slug
              ? <a className="deal-link" href={`/deal/${item.slug}`} onClick={event => onLinkClick(event, item.slug)}>{item.name || names.get(item.slug) || item.slug}</a>
              : INSTRUCTION_KINDS.has(item.kind) ? <a className="deal-link" href={instructionHref(item)} onClick={event => onInstructionClick(event, item)}>Instructions</a>
              : <span className="tone-muted">All deals</span>}</td>
            <td>{KIND_LABELS[item.kind] || item.kind}{item.revision != null && <small className="mono">Revision {item.revision}</small>}</td>
            <td className="activity-detail">
              {text(item.summary)}
              {item.target && <small>{item.target.kind === 'deal' ? 'Deal discussion' : item.target.label || item.target.uid}</small>}
              {item.kind === 'extraction' && item.version_id && <small><a className="deal-link" href={versionHref(item)} onClick={event => onLinkClick(event, item.slug, item.version_id)}>Open version</a></small>}
            </td>
          </tr>)}
        </tbody>
      </table>
    </div>}
    {loading && <Loading label="Loading activity"/>}
    {!loading && !error && !items.length && <Empty>No activity matches these filters.</Empty>}
    {more && !loading && <Button appearance="secondary" className="load-more" onClick={() => fetchPage(items.at(-1)?.id)}>Load more</Button>}
  </>;
}
