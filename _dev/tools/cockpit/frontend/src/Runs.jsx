import React, { useEffect, useState } from 'react';
import { Button, Checkbox, Field, Input, Select } from '@fluentui/react-components';
import { StopIcon, XIcon } from '@phosphor-icons/react';
import { count } from './api';
import { activeRunLabel, CANCELLABLE_STATES, DEFAULT_EFFORT, DEFAULT_TIMEOUT, EFFORTS, ENGINE_LABEL, failureText, formatElapsed, isActive, jobElapsed, planUsageText, runSummary, STATE_LABELS, stateTone, TIMEOUT_RANGE, usageText, validTimeout } from './runs';
import { displayName, shortTime } from './trace';
import { Dot, Empty, Loading, Message } from './ui';

// Header badge shown on every tab while this deal has an active run; it opens the Runs tab.
export function RunBadge({ jobs, onOpen }) {
  const [now, setNow] = useState(Date.now());
  const label = activeRunLabel(jobs, now);
  useEffect(() => {
    if (!label) return;
    const timer = setInterval(() => setNow(Date.now()), 1000);
    return () => clearInterval(timer);
  }, [Boolean(label)]);
  if (!label) return null;
  return <button type="button" className="run-badge" onClick={onOpen} title="Open the Runs tab"><Dot tone="warning"/><span className="mono">{label}</span></button>;
}

// Runs tab: this deal's extraction jobs, newest first. Active jobs tick once a second.
export function RunsTab({ jobs, error, loading, canCancel, onCancel, onOpenVersion, versions, hiddenCount = 0, showHidden, onShowHidden }) {
  const [now, setNow] = useState(Date.now());
  const anyActive = (jobs || []).some(isActive);
  useEffect(() => {
    if (!anyActive) return;
    const timer = setInterval(() => setNow(Date.now()), 1000);
    return () => clearInterval(timer);
  }, [anyActive]);
  const known = new Set((versions || []).map(version => version.id));
  return <div className="runs-tab paper-column">
    <div className="section-head">
      <h2>Extraction runs</h2>
      <span className="head-count mono">{jobs ? count(jobs.length, 'run') : ''}</span>
    </div>
    <p className="section-note">Each run gives the model only the instruction and this deal’s filing. A finished run becomes a read-only original; the working copy changes only when someone rebases onto it.</p>
    {hiddenCount > 0 && <Checkbox className="hidden-toggle" label={`Show hidden versions in the version list (${hiddenCount})`} checked={showHidden} onChange={(_, data) => onShowHidden(Boolean(data.checked))}/>}
    {error && <Message type="error" title="Runs could not be loaded." detail={error}/>}
    {loading && !jobs && <Loading label="Loading runs"/>}
    {jobs && !jobs.length && !error && <Empty>No extraction runs for this deal yet.</Empty>}
    {jobs?.map(job => {
      const failure = ['failed', 'timed_out', 'cancelled'].includes(job.state) ? failureText(job) : null;
      const result = job.result || {}, checker = result.checker;
      const elapsed = formatElapsed(jobElapsed(job, now));
      const meta = [
        elapsed && (isActive(job) ? `${elapsed} so far` : elapsed),
        usageText(result.usage),
        checker && `${count(checker.errors ?? 0, 'error')} · ${count(checker.warnings ?? 0, 'warning')}`,
      ].filter(Boolean);
      return <article className="run-item" key={job.id} data-state={job.state}>
        <div className="run-head">
          <div>
            <strong><Dot tone={stateTone(job.state)}/>{STATE_LABELS[job.state] || job.state}{job.cancel_requested && isActive(job) ? ' · cancelling' : ''}</strong>
            <span className="mono">{[`Opus 5.5 · ${job.params?.effort || '—'}`, displayName(job.actor), shortTime(job.created_at)].join(' · ')}</span>
          </div>
          <span className="run-actions">
            {job.state === 'completed' && job.version_id && known.has(job.version_id) && <Button appearance="subtle" className="link-button" onClick={() => onOpenVersion(job.version_id)}>Open version</Button>}
            {canCancel && CANCELLABLE_STATES.has(job.state) && !job.cancel_requested && <Button appearance="secondary" icon={<StopIcon size={16}/>} onClick={() => onCancel(job)}>Cancel</Button>}
          </span>
        </div>
        {meta.length > 0 && <p className="run-meta mono">{meta.join(' · ')}</p>}
        {failure && <p className={`run-failure ${job.state === 'cancelled' ? '' : 'tone-error'}`}>{failure}</p>}
        {job.error && job.state !== 'completed' && <p className="run-error mono">{job.error}</p>}
      </article>;
    })}
  </div>;
}

// Start an extraction. Without a connected Claude account the dialog explains and links to Settings.
export function ExtractDialog({ user, account, accountError, busy, error, onStart, onClose, onSettings, dialogRef }) {
  const [effort, setEffort] = useState(DEFAULT_EFFORT);
  const [timeout, setTimeoutMinutes] = useState(String(DEFAULT_TIMEOUT));
  const connected = Boolean(account?.claude?.connected);
  const usage = planUsageText(account?.claude?.plan_usage);
  const timeoutOk = validTimeout(timeout);
  return <div className="modal-backdrop" role="presentation">
    <div className="modal extract-modal" ref={dialogRef} role="dialog" aria-modal="true" aria-label="Start an extraction">
      <div className="modal-head">
        <h2>Start an extraction</h2>
        <Button appearance="subtle" className="icon-button" onClick={onClose} aria-label="Close" icon={<XIcon size={16}/>}/>
      </div>
      {!account && !accountError && <Loading label="Checking your Claude account"/>}
      {accountError || (account && !connected) ? <>
        <p>Extractions run on the Claude plan of the person who starts them, and {accountError ? 'your account status could not be loaded' : 'you have not connected a Claude account yet'}.</p>
        {accountError && <p className="run-error mono">{accountError}</p>}
        <div className="modal-actions">
          <Button appearance="secondary" onClick={onClose}>Close</Button>
          <Button as="a" appearance="primary" href="/settings" onClick={event => { if (event.button === 0 && !event.metaKey && !event.ctrlKey && !event.shiftKey && !event.altKey) { event.preventDefault(); onSettings(); } }}>Open settings</Button>
        </div>
      </> : account && <form onSubmit={event => { event.preventDefault(); if (timeoutOk) onStart({ effort, timeout_minutes: Number(timeout) }); }}>
        <dl className="extract-fixed">
          <div><dt>Engine</dt><dd>{ENGINE_LABEL} <small>More engines come later.</small></dd></div>
        </dl>
        <Field label="Effort">
          <Select value={effort} onChange={(_, data) => setEffort(data.value)}>
            {EFFORTS.map(value => <option key={value} value={value}>{value}</option>)}
          </Select>
        </Field>
        <Field label="Time limit (minutes)" validationState={timeoutOk ? 'none' : 'error'} validationMessage={timeoutOk ? undefined : `A whole number from ${TIMEOUT_RANGE[0]} to ${TIMEOUT_RANGE[1]}`}>
          <Input className="mono" type="number" min={TIMEOUT_RANGE[0]} max={TIMEOUT_RANGE[1]} step={1} value={timeout} onChange={(_, data) => setTimeoutMinutes(data.value)}/>
        </Field>
        <p className="extract-summary mono">{runSummary(effort, user)}</p>
        {usage && <p className="extract-usage mono">Plan usage · {usage}</p>}
        {error && <p className="run-failure tone-error" role="alert">{error}</p>}
        <div className="modal-actions">
          <Button appearance="secondary" onClick={onClose}>Cancel</Button>
          <Button type="submit" appearance="primary" disabled={busy || !timeoutOk}>{busy ? 'Starting…' : 'Start extraction'}</Button>
        </div>
      </form>}
    </div>
  </div>;
}
