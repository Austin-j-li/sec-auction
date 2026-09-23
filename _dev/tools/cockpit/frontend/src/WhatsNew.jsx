import React, { useState } from 'react';
import { Button } from '@fluentui/react-components';
import { CaretRightIcon } from '@phosphor-icons/react';
import { compact } from './Records';
import { displayName, groupSessions, KIND_LABELS, shortTime, tally, tallyText, timeRange } from './trace';

// "What's new": the other person's unseen activity in this deal, grouped by person and session.

function itemLabel(item) {
  if (item.kind === 'revision') return `Revision ${item.revision ?? ''}`.trim();
  if (item.kind === 'restore') return `Restore · revision ${item.revision ?? ''}`.trim();
  if (item.kind === 'rebase') return `Rebase${item.revision != null ? ` · revision ${item.revision}` : ''}`;
  if (!item.thread_id && KIND_LABELS[item.kind]) return KIND_LABELS[item.kind];
  const where = item.target?.kind === 'deal' ? 'the deal' : item.target?.label ? compact(item.target.label, 70) : '';
  return `${KIND_LABELS[item.kind] || item.kind}${where ? ` on ${where}` : ''}`;
}

export default function WhatsNew({ news, onMarkRead, onMarkUnread, onOpenItem }) {
  const [collapsed, setCollapsed] = useState(false);
  const groups = groupSessions(news.items);
  const totals = tallyText(tally(news.items));
  const people = [...new Set(news.items.map(item => displayName(item.actor)))].join(', ');
  return <section className="whats-new" aria-label="What’s new">
    <div className="whats-new-head">
      <button className="whats-new-toggle" aria-expanded={!collapsed} onClick={() => setCollapsed(value => !value)}>
        <CaretRightIcon size={14} className="caret" aria-hidden="true"/>
        <strong>What’s new</strong>
        <span className="whats-new-meta">{people} · {totals} since your last visit</span>
      </button>
      {news.status === 'read'
        ? <span className="whats-new-actions"><span className="whats-new-meta">Marked as read</span><Button appearance="subtle" className="link-button" disabled={news.busy} onClick={onMarkUnread}>Mark unread</Button></span>
        : <Button appearance="subtle" className="link-button" disabled={news.busy} onClick={onMarkRead}>Mark as read</Button>}
    </div>
    {news.error && <p className="whats-new-error tone-error">{news.error}</p>}
    {!collapsed && <div className="whats-new-body">
      {groups.map(group => <details key={`${group.actor}-${group.start}`} className="whats-new-group">
        <summary>
          <CaretRightIcon size={14} className="caret" aria-hidden="true"/>
          <span><strong>{displayName(group.actor)}</strong> · <span className="mono">{timeRange(group.start, group.end)}</span> · {tallyText(tally(group.items))}</span>
        </summary>
        <ul>
          {group.items.map(item => <li key={item.id}>
            <button className="whats-new-item" onClick={() => onOpenItem(item)}>
              <span className="mono">{shortTime(item.at)}</span>
              <span className="whats-new-kind">{itemLabel(item)}</span>
              {item.summary && <span className="whats-new-summary">{item.summary}</span>}
            </button>
          </li>)}
        </ul>
      </details>)}
    </div>}
  </section>;
}
