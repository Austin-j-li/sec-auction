import React, { useCallback, useEffect, useRef, useState } from 'react';
import { Button, Field, Input } from '@fluentui/react-components';
import { ArrowSquareOutIcon, CaretRightIcon } from '@phosphor-icons/react';
import { accountAction, chatgptAction, json } from './api';
import { CHATGPT_CONNECT_ACTIVE_STATES, CONNECT_ACTIVE_STATES, dateWithYear, planUsageText } from './runs';
import { displayName, knownUser, shortTime } from './trace';
import { Dot, Loading } from './ui';

// Settings: the signed-in person's Claude and ChatGPT accounts, which pay for the extractions they start.

const POLL_MS = 2000;
const CONNECT_STEPS = { queued: 'Starting the sign-in…', completing: 'Checking the code…' };

export default function SettingsPage({ session }) {
  const [account, setAccount] = useState(null);
  const [loadError, setLoadError] = useState('');
  const [actionError, setActionError] = useState('');
  const [busy, setBusy] = useState(false);
  const [code, setCode] = useState('');
  const [token, setToken] = useState('');
  const alive = useRef(true);
  const user = session.user;
  const canWrite = Boolean(session.can_edit && knownUser(user));

  const refresh = useCallback(async () => {
    try {
      const data = await json('/api/account');
      if (alive.current) { setAccount(data || {}); setLoadError(''); }
    } catch (err) {
      if (alive.current) { setAccount(current => current || {}); setLoadError(err.message); }
    }
  }, []);
  useEffect(() => { alive.current = true; document.title = 'Settings · Ledger cockpit'; refresh(); return () => { alive.current = false; }; }, [refresh]);

  const claude = account?.claude || {};
  const connect = account?.connect || null;
  const connecting = Boolean(connect && CONNECT_ACTIVE_STATES.has(connect.state));
  const gptConnecting = Boolean(account?.chatgpt_connect && CHATGPT_CONNECT_ACTIVE_STATES.has(account.chatgpt_connect.state));
  useEffect(() => {
    if (!connecting && !gptConnecting) return;
    const timer = setInterval(refresh, POLL_MS);
    return () => clearInterval(timer);
  }, [connecting, gptConnecting, refresh]);

  async function act(action, after) {
    setBusy(true); setActionError('');
    try {
      const data = await accountAction(session, action);
      if (alive.current) { setAccount(data || {}); setLoadError(''); after?.(); }
    } catch (err) {
      if (alive.current) setActionError(err.message);
    } finally {
      if (alive.current) setBusy(false);
    }
  }
  function disconnect() {
    if (!window.confirm('Disconnect your Claude account? Extractions you start will not run until you connect again.')) return;
    act({ action: 'disconnect' });
  }

  if (!account) return <>
    <div className="overview-title"><h1>Settings</h1></div>
    <Loading label="Loading your account"/>
  </>;

  const usage = planUsageText(claude.plan_usage);
  return <>
    <div className="overview-title">
      <h1>Settings</h1>
      <p>{user ? displayName(user) : 'Signed-out visitor'}</p>
    </div>
    <section className="settings-section" aria-labelledby="claude-account-head">
      <div className="section-head"><h2 id="claude-account-head">Claude account</h2></div>
      <p className="section-note">Extractions you start run on your own Claude plan with a token saved on the cockpit server. It is never shown again or used for anyone else’s runs.</p>
      {loadError && <p className="settings-error tone-error">Your account status could not be loaded: {loadError}</p>}
      {!canWrite && <p className="settings-line">Sign in with edit access to connect a Claude account.</p>}
      <dl className="settings-status">
        <div><dt>Status</dt><dd>{claude.connected
          ? <><Dot tone="success"/>Connected{claude.connected_at && <> since <span className="mono">{shortTime(claude.connected_at)}</span></>}</>
          : <><Dot tone="muted"/>Not connected</>}</dd></div>
        {claude.connected && claude.expires_at && <div><dt>Expires</dt><dd className="mono">{dateWithYear(claude.expires_at)}</dd></div>}
        {claude.connected && <div><dt>Plan usage</dt><dd className="mono">{usage || 'Not known yet; it is recorded after your first run'}</dd></div>}
      </dl>
      {canWrite && !connecting && <div className="settings-actions">
        <Button appearance={claude.connected ? 'secondary' : 'primary'} disabled={busy} onClick={() => act({ action: 'connect' }, () => setCode(''))}>{claude.connected ? 'Reconnect Claude account' : 'Connect Claude account'}</Button>
        {claude.connected && <Button appearance="secondary" className="danger-outline" disabled={busy} onClick={disconnect}>Disconnect</Button>}
      </div>}
      {connect && <ConnectFlow connect={connect} busy={busy} code={code} onCode={setCode} canWrite={canWrite}
        onSubmit={() => act({ action: 'code', job_id: connect.job_id, code: code.trim() }, () => setCode(''))}
        onCancel={() => act({ action: 'cancel', job_id: connect.job_id })}/>}
      {actionError && <p className="settings-error tone-error" role="alert">{actionError}</p>}
      {canWrite && <details className="settings-fallback">
        <summary><CaretRightIcon size={14} className="caret" aria-hidden="true"/>Paste a token instead</summary>
        <p>On a computer with Claude Code installed, run <code className="mono">claude setup-token</code>, approve the request with your claude.ai login, and paste the token it prints (it starts with <code className="mono">sk-ant-oat</code>). The token is saved on the cockpit server like a connected account.</p>
        <form className="settings-inline" onSubmit={event => { event.preventDefault(); act({ action: 'token', token: token.trim() }, () => setToken('')); }}>
          <Field label="Token"><Input type="password" autoComplete="off" value={token} onChange={(_, data) => setToken(data.value)}/></Field>
          <Button type="submit" appearance="secondary" disabled={busy || !token.trim()}>Save token</Button>
        </form>
      </details>}
    </section>
    <ChatGPTSection session={session} account={account} canWrite={canWrite} onAccount={data => { setAccount(data || {}); setLoadError(''); }} alive={alive}/>
  </>;
}

// ChatGPT: a device sign-in (link + one-time code) whose login the server keeps for this person's GPT runs.
function ChatGPTSection({ session, account, canWrite, onAccount, alive }) {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [disconnected, setDisconnected] = useState(false);
  const chatgpt = account?.chatgpt || {};
  const connect = account?.chatgpt_connect || null;
  const connecting = Boolean(connect && CHATGPT_CONNECT_ACTIVE_STATES.has(connect.state));
  async function act(action, after) {
    setBusy(true); setError('');
    try {
      const data = await chatgptAction(session, action);
      if (alive.current) { onAccount(data); after?.(); }
    } catch (err) {
      if (alive.current) setError(err.message);
    } finally {
      if (alive.current) setBusy(false);
    }
  }
  function disconnect() {
    if (!window.confirm('Disconnect your ChatGPT account? The cockpit deletes its copy of your login, and GPT runs you start will not run until you connect again. To revoke the login at OpenAI as well, open chatgpt.com → Settings → Security.')) return;
    act({ action: 'disconnect' }, () => setDisconnected(true));
  }
  return <section className="settings-section" aria-labelledby="chatgpt-account-head">
    <div className="section-head"><h2 id="chatgpt-account-head">ChatGPT account</h2></div>
    <p className="section-note">GPT-6.1-Sol and GPT-6-Astra runs you start use your own ChatGPT plan, through a login saved on the cockpit server. It is never used for anyone else’s runs.</p>
    {!canWrite && <p className="settings-line">Sign in with edit access to connect a ChatGPT account.</p>}
    <dl className="settings-status">
      <div><dt>Status</dt><dd>{chatgpt.connected
        ? <><Dot tone="success"/>Connected{chatgpt.connected_at && <> since <span className="mono">{shortTime(chatgpt.connected_at)}</span></>}</>
        : <><Dot tone="muted"/>Not connected</>}</dd></div>
      {chatgpt.connected && chatgpt.expires_at && <div><dt>Login expires</dt><dd className="mono">{shortTime(chatgpt.expires_at)}</dd></div>}
      {chatgpt.connected && <div><dt>Last refreshed</dt><dd className="mono">{chatgpt.last_refresh ? shortTime(chatgpt.last_refresh) : 'Not yet'}</dd></div>}
    </dl>
    {chatgpt.connected && <p className="settings-line">The server renews the login before it expires. If a renewal fails, GPT runs stop with “login has expired” until you reconnect.</p>}
    {canWrite && !connecting && <div className="settings-actions">
      <Button appearance={chatgpt.connected ? 'secondary' : 'primary'} disabled={busy} onClick={() => act({ action: 'connect' }, () => setDisconnected(false))}>{chatgpt.connected ? 'Reconnect ChatGPT account' : 'Connect ChatGPT account'}</Button>
      {chatgpt.connected && <Button appearance="secondary" className="danger-outline" disabled={busy} onClick={disconnect}>Disconnect</Button>}
    </div>}
    {disconnected && !chatgpt.connected && <p className="settings-line">Disconnected. To revoke the login at OpenAI too, open chatgpt.com → Settings → Security.</p>}
    {connect && <ChatGPTConnectFlow connect={connect} busy={busy} canWrite={canWrite} onCancel={() => act({ action: 'cancel', job_id: connect.job_id })}/>}
    {error && <p className="settings-error tone-error" role="alert">{error}</p>}
  </section>;
}

function ChatGPTConnectFlow({ connect, busy, canWrite, onCancel }) {
  if (connect.state === 'completed') return <p className="settings-line tone-success">ChatGPT account connected.</p>;
  if (connect.state === 'cancelled') return <p className="settings-line">Connecting was cancelled.</p>;
  if (connect.state === 'failed') return <p className="settings-error tone-error">Connecting failed{connect.error ? `: ${connect.error}` : '.'}</p>;
  if (!CHATGPT_CONNECT_ACTIVE_STATES.has(connect.state)) return null;
  return <div className="connect-flow" aria-live="polite">
    {connect.state === 'waiting_for_approval' && connect.link ? <>
      <ol>
        <li>
          <span>Open this link and sign in with your ChatGPT account</span>
          <a className="connect-link mono" href={connect.link} target="_blank" rel="noopener noreferrer">{connect.link}<ArrowSquareOutIcon size={12} aria-hidden="true"/></a>
        </li>
        <li>
          <span>Enter this code: <strong className="device-code mono">{connect.code || '…'}</strong></span>
        </li>
      </ol>
      <p className="settings-line"><Dot tone="warning"/>Waiting for you to approve…</p>
    </> : <p className="settings-line"><Dot tone="warning"/>Starting the sign-in…</p>}
    {connect.error && <p className="settings-error tone-error">{connect.error}</p>}
    {canWrite && <Button appearance="secondary" disabled={busy} onClick={onCancel}>Cancel</Button>}
  </div>;
}

function ConnectFlow({ connect, busy, code, onCode, onSubmit, onCancel, canWrite }) {
  const active = CONNECT_ACTIVE_STATES.has(connect.state);
  if (connect.state === 'completed') return <p className="settings-line tone-success">Claude account connected.</p>;
  if (connect.state === 'cancelled') return <p className="settings-line">Connecting was cancelled.</p>;
  if (connect.state === 'failed') return <p className="settings-error tone-error">Connecting failed{connect.error ? `: ${connect.error}` : '.'}</p>;
  if (!active) return null;
  return <div className="connect-flow" aria-live="polite">
    {connect.state === 'waiting_for_code' && connect.link ? <ol>
      <li>
        <span>Open this link and approve with your claude.ai login</span>
        <a className="connect-link mono" href={connect.link} target="_blank" rel="noopener noreferrer">{connect.link}<ArrowSquareOutIcon size={12} aria-hidden="true"/></a>
      </li>
      <li>
        <span>Paste the code shown</span>
        <form className="settings-inline" onSubmit={event => { event.preventDefault(); if (code.trim()) onSubmit(); }}>
          <Field label="Code"><Input className="mono" autoComplete="off" value={code} disabled={busy} onChange={(_, data) => onCode(data.value)}/></Field>
          <Button type="submit" appearance="primary" disabled={busy || !code.trim()}>Submit</Button>
        </form>
      </li>
    </ol> : <p className="settings-line"><Dot tone="warning"/>{CONNECT_STEPS[connect.state] || 'Waiting for the sign-in link…'}</p>}
    {connect.error && <p className="settings-error tone-error">{connect.error}</p>}
    {canWrite && <Button appearance="secondary" disabled={busy} onClick={onCancel}>Cancel</Button>}
  </div>;
}
