import React, { useEffect, useRef, useState } from 'react';

const HANDLE = 8;
const STEP = 10;
const STACK_WIDTH = 680;

function savedSize(key) {
  try {
    const value = Number(localStorage.getItem(`cockpit.layout.${key}`));
    return Number.isFinite(value) && value > 0 ? value : null;
  } catch { return null; }
}

function persistSize(key, value) {
  try {
    if (value == null) localStorage.removeItem(`cockpit.layout.${key}`);
    else localStorage.setItem(`cockpit.layout.${key}`, String(Math.round(value)));
  } catch { /* Browser storage can be unavailable in a private session. */ }
}

function clamp(value, total, minStart, minEnd) {
  const maximum = Math.max(minStart, total - minEnd - HANDLE);
  return Math.min(maximum, Math.max(minStart, value));
}

export default function SplitPane({ className, name, storageKey, defaultSize, minStart, minEnd, mobileDefaultSize = 160, mobileStack = false, collapsible = false, children }) {
  const root = useRef(null);
  const drag = useRef(null);
  const [viewportWidth, setViewportWidth] = useState(() => window.innerWidth);
  const [bounds, setBounds] = useState({ width: 0, height: 0 });
  const compact = mobileStack && (viewportWidth <= 560 || (bounds.width > 0 && bounds.width <= STACK_WIDTH));
  const hidden = collapsible && viewportWidth <= 820;
  const key = `${storageKey}.${compact ? 'mobile' : 'desktop'}`;
  const [sizes, setSizes] = useState({});
  const total = compact ? bounds.height : bounds.width;
  const effectiveTotal = total || (collapsible ? viewportWidth : 0);
  const minimum = compact ? 96 : minStart;
  const trailingMinimum = compact ? 160 : minEnd;
  const stored = sizes[key] === undefined ? savedSize(key) : sizes[key];
  const preferred = stored ?? (compact ? mobileDefaultSize : typeof defaultSize === 'function' ? defaultSize(total || viewportWidth) : defaultSize);
  const size = effectiveTotal ? clamp(preferred, effectiveTotal, minimum, trailingMinimum) : preferred;
  const maximum = effectiveTotal ? Math.max(minimum, effectiveTotal - trailingMinimum - HANDLE) : Math.max(minimum, size);

  useEffect(() => {
    const onResize = () => setViewportWidth(window.innerWidth);
    window.addEventListener('resize', onResize);
    return () => window.removeEventListener('resize', onResize);
  }, []);
  useEffect(() => {
    const observer = new ResizeObserver(([entry]) => {
      const { width, height } = entry.contentRect;
      setBounds(previous => previous.width === width && previous.height === height ? previous : { width, height });
    });
    if (root.current) observer.observe(root.current);
    return () => observer.disconnect();
  }, []);

  function update(next, store = false) {
    const adjusted = clamp(next, effectiveTotal, minimum, trailingMinimum);
    setSizes(previous => ({ ...previous, [key]: adjusted }));
    if (store) persistSize(key, adjusted);
  }

  function onPointerDown(event) {
    if (event.button !== 0 || hidden) return;
    drag.current = { coordinate: compact ? event.clientY : event.clientX, size };
    event.currentTarget.setPointerCapture(event.pointerId);
    event.preventDefault();
  }
  function onPointerMove(event) {
    if (!drag.current) return;
    const coordinate = compact ? event.clientY : event.clientX;
    update(drag.current.size + coordinate - drag.current.coordinate);
  }
  function onPointerUp(event) {
    if (!drag.current) return;
    const coordinate = compact ? event.clientY : event.clientX;
    const finalSize = clamp(drag.current.size + coordinate - drag.current.coordinate, effectiveTotal, minimum, trailingMinimum);
    drag.current = null;
    update(finalSize, true);
    if (event.currentTarget.hasPointerCapture(event.pointerId)) event.currentTarget.releasePointerCapture(event.pointerId);
  }
  function onKeyDown(event) {
    const backward = compact ? event.key === 'ArrowUp' : event.key === 'ArrowLeft';
    const forward = compact ? event.key === 'ArrowDown' : event.key === 'ArrowRight';
    if (!backward && !forward && event.key !== 'Home' && event.key !== 'End') return;
    event.preventDefault();
    event.stopPropagation();
    update(event.key === 'Home' ? minimum : event.key === 'End' ? maximum : size + (forward ? 1 : -1) * (event.shiftKey ? STEP * 4 : STEP), true);
  }
  function reset() {
    setSizes(previous => ({ ...previous, [key]: null }));
    persistSize(key, null);
  }

  const [first, second] = React.Children.toArray(children);
  return <div ref={root} className={`${className} resizable-split ${compact ? 'split-horizontal' : 'split-vertical'}`} style={{ '--split-size': `${size}px` }}>
    {first}
    <div className="split-handle" role="separator" tabIndex={hidden ? -1 : 0} aria-label={`Resize ${name}`} aria-orientation={compact ? 'horizontal' : 'vertical'} aria-valuemin={Math.round(minimum)} aria-valuemax={Math.round(maximum)} aria-valuenow={Math.round(size)} title={`Drag to resize ${name}. Double-click to reset. Use arrow keys, Home, or End.`} onPointerDown={onPointerDown} onPointerMove={onPointerMove} onPointerUp={onPointerUp} onLostPointerCapture={() => { drag.current = null; }} onKeyDown={onKeyDown} onDoubleClick={reset}/>
    {second}
  </div>;
}
