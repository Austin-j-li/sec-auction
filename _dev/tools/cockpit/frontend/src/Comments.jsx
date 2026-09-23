import React, { useEffect, useRef, useState } from 'react';
import { Button, Field, Textarea } from '@fluentui/react-components';
import { CaretRightIcon } from '@phosphor-icons/react';
import { count, text } from './api';
import { displayName, shortTime, threadsFor } from './trace';
import { Message } from './ui';

// Threads on one target (a row, a finding, or the whole deal). Each action posts at once; nothing goes through the unsaved-edits dock.

const excerpt = (value, length = 90) => { const s = text(value).replace(/\s+/g, ' ').trim(); return s.length > length ? `${s.slice(0, length - 1)}…` : s; };
const apiTarget = target => target.kind === 'deal' ? { kind: 'deal' } : target.kind === 'finding' ? { kind: 'finding', uid: target.uid } : { kind: 'row', sheet: target.sheet, uid: target.uid };

function Draft({ label, initial = '', submitLabel, busy, onSubmit, onCancel }) {
  const [body, setBody] = useState(initial);
  return <div className="comment-draft">
    <Field label={label}>
      <Textarea value={body} resize="none" className="resizable-textarea comment-textarea" rows={2} disabled={busy} onChange={(_, data) => setBody(data.value)}/>
    </Field>
    <div className="comment-draft-actions">
      <Button appearance="secondary" disabled={busy || !body.trim()} onClick={async () => { if (await onSubmit(body) && !onCancel) setBody(''); }}>{submitLabel}</Button>
      {onCancel && <Button appearance="subtle" disabled={busy} onClick={onCancel}>Cancel</Button>}
    </div>
  </div>;
}

function CommentItem({ comment, trace, run, busy }) {
  const [editing, setEditing] = useState(false);
  if (comment.deleted) return <div className="comment deleted">
    <p className="comment-meta">Comment deleted by {displayName(comment.deleted.by)}{comment.deleted.at && <> · <span className="mono">{shortTime(comment.deleted.at)}</span></>}</p>
  </div>;
  const own = trace.canComment && comment.actor === trace.user;
  async function remove() {
    if (window.confirm('Delete this comment? The thread will show that you deleted it.')) await run({ action: 'delete', comment_id: comment.id });
  }
  return <div className="comment">
    <p className="comment-meta">
      <span className="comment-author">{displayName(comment.actor)}</span>
      {' · '}<span className="mono">{shortTime(comment.at)}</span>
      {comment.edited_at && <span title={`Edited ${shortTime(comment.edited_at)}${comment.edit_count ? ` · ${count(comment.edit_count, 'earlier version')} kept` : ''}`}> · edited</span>}
      {own && !editing && <span className="comment-tools">
        <Button appearance="subtle" className="link-button" disabled={busy} onClick={() => setEditing(true)}>Edit</Button>
        <Button appearance="subtle" className="link-button" disabled={busy} onClick={remove}>Delete</Button>
      </span>}
    </p>
    {editing
      ? <Draft label="Edit comment" initial={comment.body} submitLabel="Save comment" busy={busy} onCancel={() => setEditing(false)}
          onSubmit={async body => { const ok = await run({ action: 'edit', comment_id: comment.id, body }); if (ok) setEditing(false); return ok; }}/>
      : <p className="comment-body">{comment.body}</p>}
  </div>;
}

function Thread({ thread, trace, run, busy }) {
  const resolved = thread.resolved;
  const [open, setOpen] = useState(!resolved);
  const [replying, setReplying] = useState(false);
  const ref = useRef(null);
  const focused = trace.focus?.threadId === thread.id;
  useEffect(() => { setOpen(!resolved); }, [Boolean(resolved)]);
  useEffect(() => {
    if (!focused) return;
    setOpen(true);
    requestAnimationFrame(() => ref.current?.scrollIntoView({ block: 'nearest' }));
  }, [focused, trace.focus?.nonce]);
  const [first, ...replies] = thread.comments || [];
  const resolvedBy = resolved && `Resolved by ${displayName(resolved.by || thread.resolved_by)}`;
  const context = thread.target_missing && <p className="thread-context">Record removed · {thread.target?.label}</p>;
  if (!open) return <div className={`thread is-resolved ${focused ? 'focused' : ''}`} ref={ref}>
    <button className="thread-collapsed" aria-expanded="false" onClick={() => setOpen(true)}>
      <CaretRightIcon size={14} className="caret" aria-hidden="true"/>
      <span className="thread-resolved-by">{resolvedBy}</span>
      <span className="thread-excerpt">{first?.deleted ? 'Comment deleted' : excerpt(first?.body)}</span>
      <span className="mono">{count(thread.comments?.length || 0, 'comment')}</span>
    </button>
  </div>;
  return <div className={`thread ${focused ? 'focused' : ''}`} ref={ref}>
    {context}
    {resolved && <button className="thread-collapsed" aria-expanded="true" onClick={() => setOpen(false)}>
      <CaretRightIcon size={14} className="caret" aria-hidden="true"/>
      <span className="thread-resolved-by">{resolvedBy}{resolved.at && <> · <span className="mono">{shortTime(resolved.at)}</span></>}</span>
    </button>}
    {first && <CommentItem comment={first} trace={trace} run={run} busy={busy}/>}
    {replies.length > 0 && <div className="replies">
      {replies.map(comment => <CommentItem key={comment.id} comment={comment} trace={trace} run={run} busy={busy}/>)}
    </div>}
    {trace.canComment && !replying && <div className="thread-actions">
      <Button appearance="subtle" className="link-button" disabled={busy} onClick={() => setReplying(true)}>Reply</Button>
      <Button appearance="subtle" className="link-button" disabled={busy} onClick={() => run({ action: resolved ? 'reopen' : 'resolve', thread_id: thread.id })}>{resolved ? 'Reopen' : 'Resolve'}</Button>
    </div>}
    {replying && <div className="replies">
      <Draft label={resolved ? 'Reply (reopens the thread)' : 'Reply'} submitLabel="Reply" busy={busy} onCancel={() => setReplying(false)}
        onSubmit={async body => { const ok = await run({ action: 'reply', thread_id: thread.id, body }); if (ok) setReplying(false); return ok; }}/>
    </div>}
  </div>;
}

export default function Comments({ trace, target, heading = 'Comments' }) {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const threads = threadsFor(trace.threads, target);
  const unsaved = target.kind === 'row' && text(target.uid).startsWith('new-');
  async function run(action) {
    setBusy(true); setError('');
    try { await trace.post(action); return true; }
    catch (err) { setError(err?.message || text(err)); return false; }
    finally { setBusy(false); }
  }
  const open = threads.filter(thread => !thread.resolved).length;
  return <section className="comments" aria-label={heading}>
    <div className="comments-head">
      <h4>{heading}</h4>
      {threads.length > 0 && <span className="head-count mono">{count(open, 'open thread')}{threads.length > open ? ` · ${threads.length - open} resolved` : ''}</span>}
    </div>
    {trace.threadsError && <p className="comments-note">Comments could not be loaded. {trace.threadsError}</p>}
    {!trace.threadsError && !trace.threads && <p className="comments-note">Loading comments…</p>}
    {threads.map(thread => <Thread key={thread.id} thread={thread} trace={trace} run={run} busy={busy}/>)}
    {trace.threads && !threads.length && !trace.canComment && <p className="comments-note">No comments.</p>}
    {error && <Message type="error" title="The comment action did not go through." detail={error}/>}
    {trace.canComment && (unsaved
      ? <p className="comments-note">Save this new record before commenting on it.</p>
      : <Draft label="New comment" submitLabel="Comment" busy={busy} onSubmit={body => run({ action: 'create', target: apiTarget(target), body })}/>)}
  </section>;
}
