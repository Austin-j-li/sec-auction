import React from 'react';
import { WarningCircleIcon } from '@phosphor-icons/react';
import { count } from './api';
import { Empty } from './ui';

function CheckLine({ check }) {
  if (!check) return null;
  const errors = check.errors ?? 0, warnings = check.warnings ?? 0;
  return <small className="mono">
    {errors > 0
      ? <span className="tone-error"><WarningCircleIcon size={12} aria-hidden="true"/> {count(errors, 'error')}</span>
      : count(errors, 'error')}
    {' · '}{count(warnings, 'warning')}
  </small>;
}

export default function Overview({ deals, onOpen }) {
  // Plain left-click and keyboard go through the in-app navigation (unsaved-edit guard);
  // modified clicks and middle-click keep the link's native behaviour.
  function onLinkClick(event, slug) {
    if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) { event.stopPropagation(); return; }
    event.preventDefault();
    event.stopPropagation();
    onOpen(slug);
  }
  function onRowKey(event, slug) {
    if (event.target !== event.currentTarget) return;
    if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); onOpen(slug); }
  }

  return <>
    <div className="overview-title">
      <h1>Deal ledgers</h1>
      <p><span className="mono">{count(deals.length, 'deal')}</span> · open one to inspect the filing and edit its working copy</p>
    </div>
    <div className="deal-table-wrap">
      <table className="deal-table">
        <thead>
          <tr>
            <th>Deal</th>
            <th>Filing</th>
            <th>Working copy</th>
            <th className="number">Events</th>
            <th className="number">Rounds</th>
            <th className="number">Questions</th>
            <th>Source evidence</th>
            <th>Review state</th>
          </tr>
        </thead>
        <tbody>
          {deals.map(item => <tr key={item.slug} tabIndex={0} onClick={() => onOpen(item.slug)} onKeyDown={event => onRowKey(event, item.slug)}>
            <td>
              <a className="deal-link" href={`/deal/${item.slug}`} tabIndex={-1} onClick={event => onLinkClick(event, item.slug)}>{item.name || item.target || item.slug}</a>
              <small className="mono">{item.slug}</small>
            </td>
            <td className="mono">
              {item.form_type || '—'}
              <small>{item.date_filed || ''}</small>
            </td>
            <td>
              {item.base_label || item.instruction_version || 'Working'}
              <small className="mono">{item.working_revision != null ? `Revision ${item.working_revision}` : ''}</small>
            </td>
            <td className="number mono">{item.rows ?? '—'}</td>
            <td className="number mono">{item.rounds ?? '—'}</td>
            <td className="number mono">{item.questions ?? '—'}</td>
            <td>
              <span className="mono">{item.quotes_total != null ? `${item.quotes_located ?? 0} / ${item.quotes_total} quotes located` : '—'}</span>
              <CheckLine check={item.check}/>
            </td>
            <td>
              <span className="status-text">{item.review_status || 'unreviewed'}</span>
              {item.error && <small className="tone-error">{item.error}</small>}
            </td>
          </tr>)}
        </tbody>
      </table>
    </div>
    {deals.length > 0 && <p className="table-footnote">Quote location is a location aid, not validation.</p>}
    {!deals.length && <Empty>No deal workbooks are available yet.</Empty>}
  </>;
}
