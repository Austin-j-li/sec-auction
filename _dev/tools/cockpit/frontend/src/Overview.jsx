import React, { useState } from 'react';
import { Button, Checkbox } from '@fluentui/react-components';
import { EyeIcon, PlusIcon, WarningCircleIcon } from '@phosphor-icons/react';
import { count } from './api';
import { hiddenLine, listedDeals, reviewByline, reviewText } from './deals';
import { Empty } from './ui';
import { displayName, tallyText } from './trace';
import { liveCheckText } from './runs';

function CheckLine({ check }) {
  if (!check) return null;
  const errors = check.errors ?? 0, warnings = check.warnings ?? 0;
  return <small className="mono" title={liveCheckText(check, check.ledger_schema)}>
    {errors > 0
      ? <span className="tone-error"><WarningCircleIcon size={12} aria-hidden="true"/> {count(errors, 'error')}</span>
      : count(errors, 'error')}
    {' · '}{count(warnings, 'warning')}
  </small>;
}

// "Alex · 1 run, 12 edits, 3 comments since you last looked"; nothing when nothing is new.
function UnseenLine({ unseen }) {
  const parts = Object.entries(unseen?.by || {})
    .map(([actor, counts]) => [actor, tallyText({ runs: counts?.runs || 0, edits: counts?.edits || 0, comments: counts?.comments || 0 })])
    .filter(([, summary]) => summary)
    .map(([actor, summary]) => `${displayName(actor)} · ${summary}`);
  if (!parts.length) return null;
  return <small className="unseen-line">{parts.join('; ')} since you last looked</small>;
}

// onUnhide(slug) is given to people who may unhide; it resolves when the list has been reloaded.
export default function Overview({ deals, onOpen, onAdd, onUnhide }) {
  const [showHidden, setShowHidden] = useState(false);
  const [unhiding, setUnhiding] = useState(null);
  const { rows, hiddenCount, visible } = listedDeals(deals, showHidden);
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

  async function unhide(event, slug) {
    event.stopPropagation();
    setUnhiding(slug);
    try { await onUnhide(slug); } finally { setUnhiding(null); }
  }

  return <>
    <div className="overview-title">
      <h1>Deal ledgers</h1>
      <p><span className="mono">{count(visible, 'deal')}</span> · open one to inspect the filing and edit its working copy</p>
      {onAdd && <Button appearance="secondary" className="add-deal-button" icon={<PlusIcon size={16}/>} onClick={onAdd}>Add deal</Button>}
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
          {rows.map(item => <tr key={item.slug} className={item.hidden ? 'hidden-deal' : undefined} tabIndex={0} onClick={() => onOpen(item.slug)} onKeyDown={event => onRowKey(event, item.slug)}>
            <td>
              <a className="deal-link" href={`/deal/${item.slug}`} tabIndex={-1} onClick={event => onLinkClick(event, item.slug)}>{item.name || item.target || item.slug}</a>
              <small className="mono">{item.slug}</small>
              {item.active_jobs > 0 && <small className="running-line">Extraction running</small>}
              {item.hidden ? <small className="hidden-line"><span className="hidden-mark" title={hiddenLine(item)}>Hidden</span>
                {onUnhide && <Button appearance="subtle" className="link-button" icon={<EyeIcon size={14}/>} disabled={unhiding === item.slug} onClick={event => unhide(event, item.slug)}>Unhide</Button>}
              </small> : <UnseenLine unseen={item.unseen}/>}
            </td>
            <td className="mono">
              {item.form_type || '—'}
              <small>{item.date_filed || ''}</small>
            </td>
            <td>
              {item.pending ? 'No extraction yet' : item.base_label || item.instruction_version || 'Working'}
              <small className="mono">{item.pending ? '' : item.working_revision != null ? `Revision ${item.working_revision}` : ''}</small>
            </td>
            <td className="number mono">{item.rows ?? '—'}</td>
            <td className="number mono">{item.rounds ?? '—'}</td>
            <td className="number mono">{item.questions ?? '—'}</td>
            <td>
              <span className="mono">{item.quotes_total != null ? `${item.quotes_located ?? 0} / ${item.quotes_total} quotes located` : '—'}</span>
              <CheckLine check={item.check}/>
            </td>
            <td>
              <span className={`status-text${item.deal_review?.edited_since && item.deal_review.status === 'reviewed' ? ' tone-warning' : ''}`}>{item.deal_review ? reviewText(item.deal_review) : item.review_status || 'unreviewed'}</span>
              {reviewByline(item.deal_review) && <small>{reviewByline(item.deal_review)}</small>}
              {item.error && <small className="tone-error">{item.error}</small>}
            </td>
          </tr>)}
        </tbody>
      </table>
    </div>
    {hiddenCount > 0 && <Checkbox className="hidden-toggle deal-hidden-toggle" label={`Show hidden (${hiddenCount})`} checked={showHidden} onChange={(_, data) => setShowHidden(Boolean(data.checked))}/>}
    {rows.length > 0 && <p className="table-footnote">Quote location is a location aid, not validation.</p>}
    {!deals.length && <Empty>No deal workbooks are available yet.</Empty>}
    {deals.length > 0 && !rows.length && <Empty>Every deal is hidden.</Empty>}
  </>;
}
