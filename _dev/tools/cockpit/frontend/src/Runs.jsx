import React, { useEffect, useState } from 'react';
import { Button, Checkbox, Field, Input, Select } from '@fluentui/react-components';
import { StopIcon, WarningIcon, XIcon } from '@phosphor-icons/react';
import { count } from './api';
import { defaultInstructionId, instructionOptionLabel, orderInstructions } from './instructions';
import { accountEngines, accountLabel, activeRunLabel, CANCELLABLE_STATES, checkerLabel, connectHint, DEFAULT_EFFORT, DEFAULT_TIMEOUT, effortFor, extractNotice, FABLE_WARNING, failureText, formatElapsed, isActive, jobElapsed, jobEngineLabel, jobInstructionLabel, pickEngine, planUsageText, runSummary, STATE_LABELS, stateTone, TIMEOUT_RANGE, usageText, validTimeout } from './runs';
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
        checker && [checkerLabel(checker), count(checker.errors ?? 0, 'error'), count(checker.warnings ?? 0, 'warning')].filter(Boolean).join(' · '),
      ].filter(Boolean);
      return <article className="run-item" key={job.id} data-state={job.state}>
        <div className="run-head">
          <div>
            <strong><Dot tone={stateTone(job.state)}/>{STATE_LABELS[job.state] || job.state}{job.cancel_requested && isActive(job) ? ' · cancelling' : ''}</strong>
            <span className="mono">{[`${jobEngineLabel(job)} · ${job.params?.effort || '—'}`, jobInstructionLabel(job), displayName(job.actor), shortTime(job.created_at)].join(' · ')}</span>
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

// Start an extraction: engine, effort, instruction and time limit. An engine whose account (Claude or ChatGPT) is not
// connected is listed but disabled; with no usable engine at all the dialog explains and links to Settings.
// working: the deal's workspace summary (its base's instruction and schema), for the line about the working copy.
export function ExtractDialog({ user, account, accountError, instructions, instructionsError, busy, error, onStart, onClose, onSettings, dialogRef, working = null }) {
  const engines = accountEngines(account);
  const [engineId, setEngineId] = useState(null);
  const [effort, setEffort] = useState(DEFAULT_EFFORT);
  const [instructionId, setInstructionId] = useState(null);
  const [timeout, setTimeoutMinutes] = useState(String(DEFAULT_TIMEOUT));
  const engine = pickEngine(engines, engineId);
  const items = orderInstructions(instructions?.items);
  const instruction = items.find(item => item.id === instructionId) || items.find(item => item.id === defaultInstructionId(instructions)) || items[0] || null;
  // Once the account arrives, settle on an engine and its default effort.
  useEffect(() => { if (engine && engine.id !== engineId) { setEngineId(engine.id); setEffort(current => engineId ? effortFor(engine, current) : engine.default_effort); } }, [engine?.id]);
  const timeoutOk = validTimeout(timeout);
  const usage = engine?.account === 'claude' ? planUsageText(account?.claude?.plan_usage) : '';
  const unavailable = engines.filter(item => !item.connected);
  const openSettings = event => { if (event.button === 0 && !event.metaKey && !event.ctrlKey && !event.shiftKey && !event.altKey) { event.preventDefault(); onSettings(); } };
  const missing = [...new Set(unavailable.map(item => item.account))]
    .map(name => `${unavailable.filter(item => item.account === name).map(item => item.label).join(' and ')}: ${connectHint({ account: name })}.`).join(' ');
  const warning = engine?.id === 'fable51' ? FABLE_WARNING : engine?.experimental ? engine.note : '';
  const info = !engine?.experimental && engine?.note ? engine.note : '';
  const notice = extractNotice(working, instruction);
  function chooseEngine(id) {
    const next = engines.find(item => item.id === id);
    if (!next?.connected) return;
    setEngineId(id); setEffort(current => effortFor(next, current));
  }
  function submit(event) {
    event.preventDefault();
    if (!timeoutOk || !engine) return;
    onStart({ engine: engine.id, effort: effortFor(engine, effort), timeout_minutes: Number(timeout), ...(instruction ? { instruction_id: instruction.id } : {}) });
  }
  return <div className="modal-backdrop" role="presentation">
    <div className="modal extract-modal" ref={dialogRef} role="dialog" aria-modal="true" aria-label="Start an extraction">
      <div className="modal-head">
        <h2>Start an extraction</h2>
        <Button appearance="subtle" className="icon-button" onClick={onClose} aria-label="Close" icon={<XIcon size={16}/>}/>
      </div>
      {!account && !accountError && <Loading label="Checking your accounts"/>}
      {accountError ? <>
        <p>Extractions run on the Claude or ChatGPT plan of the person who starts them, and your account status could not be loaded.</p>
        <p className="run-error mono">{accountError}</p>
        <div className="modal-actions">
          <Button appearance="secondary" onClick={onClose}>Close</Button>
          <Button as="a" appearance="primary" href="/settings" onClick={openSettings}>Open settings</Button>
        </div>
      </> : account && !engine ? <>
        <Field label="Engine" hint="Every engine needs a connected account.">
          <Select value={engines[0]?.id || ''} disabled={engines.length === 0}>
            {engines.map(item => <option key={item.id} value={item.id} disabled>{item.label}{item.experimental ? ' (experimental)' : ''} — {connectHint(item)}</option>)}
          </Select>
        </Field>
        <p className="extract-explain">Extractions run on the Claude or ChatGPT plan of the person who starts them, and you have not connected an account yet.</p>
        <div className="modal-actions">
          <Button appearance="secondary" onClick={onClose}>Close</Button>
          <Button as="a" appearance="primary" href="/settings" onClick={openSettings}>Open settings</Button>
        </div>
      </> : account && <form onSubmit={submit}>
        <Field label="Engine" hint={missing ? <>{missing} <a className="header-link" href="/settings" onClick={openSettings}>Open settings</a></> : undefined}>
          <Select value={engine.id} onChange={(_, data) => chooseEngine(data.value)}>
            {engines.map(item => <option key={item.id} value={item.id} disabled={!item.connected}>{item.label}{item.experimental ? ' (experimental)' : ''}{item.connected ? '' : ` — ${connectHint(item)}`}</option>)}
          </Select>
        </Field>
        {warning && <p className="extract-warning tone-warning"><WarningIcon size={16} aria-hidden="true"/><span>{warning}</span></p>}
        {info && <p className="extract-info">{info}</p>}
        <Field label="Effort">
          <Select value={effortFor(engine, effort)} onChange={(_, data) => setEffort(data.value)}>
            {engine.efforts.map(value => <option key={value} value={value}>{value}</option>)}
          </Select>
        </Field>
        <Field label="Instruction" hint={instructionsError ? `The instruction list could not be loaded (${instructionsError}); the run uses the default instruction.` : undefined}>
          {instructions ? <Select value={instruction?.id || ''} onChange={(_, data) => setInstructionId(data.value)}>
            {items.map(item => <option key={item.id} value={item.id}>{instructionOptionLabel(item)}</option>)}
          </Select> : !instructionsError && <Loading label="Loading instructions"/>}
        </Field>
        {notice && <p className="extract-warning tone-warning"><WarningIcon size={16} aria-hidden="true"/><span>{notice}</span></p>}
        <Field label="Time limit (minutes)" validationState={timeoutOk ? 'none' : 'error'} validationMessage={timeoutOk ? undefined : `A whole number from ${TIMEOUT_RANGE[0]} to ${TIMEOUT_RANGE[1]}`}>
          <Input className="mono" type="number" min={TIMEOUT_RANGE[0]} max={TIMEOUT_RANGE[1]} step={1} value={timeout} onChange={(_, data) => setTimeoutMinutes(data.value)}/>
        </Field>
        <p className="extract-summary mono">{runSummary(effortFor(engine, effort), user, engine, instruction?.label || (instructionsError ? 'default instruction' : '…'))}</p>
        {usage && <p className="extract-usage mono">{accountLabel(engine.account)} plan usage · {usage}</p>}
        {error && <p className="run-failure tone-error" role="alert">{error}</p>}
        <div className="modal-actions">
          <Button appearance="secondary" onClick={onClose}>Cancel</Button>
          <Button type="submit" appearance="primary" disabled={busy || !timeoutOk || (!instructions && !instructionsError)}>{busy ? 'Starting…' : 'Start extraction'}</Button>
        </div>
      </form>}
    </div>
  </div>;
}
