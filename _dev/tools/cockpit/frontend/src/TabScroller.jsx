import React, { useCallback, useEffect, useRef, useState } from 'react';
import { ArrowLeftIcon, ArrowRightIcon } from '@phosphor-icons/react';

export default function TabScroller({ activeTab, children }) {
  const strip = useRef(null);
  const tabs = useRef(null);
  const [position, setPosition] = useState({ overflow: false, left: false, right: false });

  const measure = useCallback(() => {
    const wrapper = strip.current, scroller = tabs.current;
    if (!wrapper || !scroller) return;
    const overflow = scroller.scrollWidth > wrapper.clientWidth + 1;
    const left = overflow && scroller.scrollLeft > 1;
    const right = overflow && scroller.scrollLeft + scroller.clientWidth < scroller.scrollWidth - 1;
    setPosition(previous => previous.overflow === overflow && previous.left === left && previous.right === right ? previous : { overflow, left, right });
  }, []);

  const keepActiveVisible = useCallback(() => {
    const scroller = tabs.current, active = scroller?.querySelector('[aria-selected="true"]');
    if (!scroller || !active) return;
    const item = active.getBoundingClientRect(), view = scroller.getBoundingClientRect();
    if (item.left < view.left) scroller.scrollLeft += item.left - view.left - 8;
    else if (item.right > view.right) scroller.scrollLeft += item.right - view.right + 8;
    measure();
  }, [measure]);

  useEffect(() => {
    const wrapper = strip.current, scroller = tabs.current;
    if (!wrapper || !scroller) return;
    let mounted = true;
    const onGeometry = () => { keepActiveVisible(); measure(); };
    const observer = new ResizeObserver(onGeometry);
    observer.observe(wrapper);
    observer.observe(scroller);
    scroller.addEventListener('scroll', measure, { passive: true });
    onGeometry();
    document.fonts?.ready.then(() => { if (mounted) onGeometry(); });
    return () => { mounted = false; observer.disconnect(); scroller.removeEventListener('scroll', measure); };
  }, [keepActiveVisible, measure]);
  useEffect(() => { measure(); }, [children, measure]);
  useEffect(() => { keepActiveVisible(); }, [activeTab, keepActiveVisible]);

  function scroll(direction) {
    const scroller = tabs.current;
    if (!scroller) return;
    scroller.scrollBy({ left: direction * Math.max(140, scroller.clientWidth * 0.72), behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' });
  }

  // Arrow-key roving between tabs (automatic activation); inactive tabs are not tab stops.
  function onKeyDown(event) {
    if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
    const items = [...(tabs.current?.querySelectorAll('[role="tab"]') || [])];
    const current = items.indexOf(document.activeElement);
    if (current < 0) return;
    event.preventDefault();
    const next = event.key === 'Home' ? 0 : event.key === 'End' ? items.length - 1 : (current + (event.key === 'ArrowRight' ? 1 : -1) + items.length) % items.length;
    items[next].focus();
    items[next].click();
  }

  return <div ref={strip} className={`tab-strip ${position.overflow ? 'has-overflow' : ''}`}>
    <button type="button" className="tab-scroll-control" aria-label="Scroll workspace tabs left" disabled={!position.left} onClick={() => scroll(-1)}><ArrowLeftIcon size={16}/></button>
    <nav ref={tabs} className="tabs" role="tablist" aria-label="Workspace tabs" onKeyDown={onKeyDown}>{children}</nav>
    <button type="button" className="tab-scroll-control" aria-label="Scroll workspace tabs right" disabled={!position.right} onClick={() => scroll(1)}><ArrowRightIcon size={16}/></button>
  </div>;
}
