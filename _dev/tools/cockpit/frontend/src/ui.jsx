import React from 'react';
import { Spinner } from '@fluentui/react-components';
import { InfoIcon, TrayIcon, WarningIcon, XCircleIcon } from '@phosphor-icons/react';

// Shared status primitives: every coloured status carries a dot or a glyph (brief §4.10).

export function Dot({ tone = 'muted', title }) {
  return <span className={`dot dot-${tone}`} title={title} aria-hidden={title ? undefined : 'true'}/>;
}

export function SeverityGlyph({ severity, size = 16 }) {
  if (severity === 'error') return <XCircleIcon size={size} className="tone-error" aria-hidden="true"/>;
  if (severity === 'warning') return <WarningIcon size={size} className="tone-warning" aria-hidden="true"/>;
  return <InfoIcon size={size} className="tone-muted" aria-hidden="true"/>;
}

const BANNER_GLYPH = { error: XCircleIcon, warning: WarningIcon, info: InfoIcon };

// Banner: human sentence first, the raw server string second in mono. role="alert" only for errors.
export function Message({ type = 'info', title, detail, children, className = '' }) {
  const Glyph = BANNER_GLYPH[type] || InfoIcon;
  return <div className={`message ${type} ${className}`.trim()} role={type === 'error' ? 'alert' : 'status'}>
    <Glyph size={20} aria-hidden="true"/>
    <div className="message-body">
      {title && <p className="message-title">{title}</p>}
      {detail && <p className="message-detail">{detail}</p>}
      {children}
    </div>
  </div>;
}

export function Loading({ label }) {
  return <div className="loading-state"><Spinner size="tiny" label={label}/></div>;
}

export function Empty({ children }) {
  return <div className="empty"><TrayIcon size={16} aria-hidden="true"/><span>{children}</span></div>;
}
