import React, { useEffect, useMemo, useRef, useState } from 'react';
import { Button, Input, Spinner } from '@fluentui/react-components';
import { ArrowDownIcon, ArrowUpIcon, MagnifyingGlassIcon } from '@phosphor-icons/react';
import { filingRanges, segments, text } from './api';

export default function Filing({ filing, loading, error, deal, selectedUid, scrollRequest, searchRequest, onSelectRow, onQuoteSelection }) {
  const pane = useRef(null);
  const [query, setQuery] = useState('');
  const [activeMatch, setActiveMatch] = useState(0);
  const [page, setPage] = useState('');
  const [pageError, setPageError] = useState('');
  const [selection, setSelection] = useState(null);
  const blocks = filing?.blocks || [];
  const rows = deal?.ledger?.rows || [];
  const selectedIndex = rows.findIndex(row => row.uid === selectedUid);
  const ranges = useMemo(() => filingRanges(rows, blocks), [rows, blocks]);
  const pageMap = useMemo(() => new Map((filing?.pages || []).map(item => [item.block, text(item.page)])), [filing]);
  const needle = query.trim();
  const matches = useMemo(() => {
    if (!needle) return [];
    const folded = needle.toLocaleLowerCase();
    const found = [];
    blocks.forEach((block, index) => {
      const hay = text(block.text).toLocaleLowerCase();
      let cursor = 0;
      while (found.length < 5000) {
        const at = hay.indexOf(folded, cursor);
        if (at < 0) break;
        found.push({ block: index, offset: at });
        cursor = at + Math.max(folded.length, 1);
      }
    });
    return found;
  }, [blocks, needle]);
  const matchByPosition = useMemo(() => new Map(matches.map((match, index) => [`${match.block}:${match.offset}`, index])), [matches]);
  const matchesByBlock = useMemo(() => {
    const grouped = new Map();
    for (const match of matches) {
      if (!grouped.has(match.block)) grouped.set(match.block, []);
      grouped.get(match.block).push({ from: match.offset, to: match.offset + needle.length });
    }
    return grouped;
  }, [matches, needle]);

  useEffect(() => setActiveMatch(0), [query]);
  useEffect(() => {
    if (!searchRequest) return;
    setQuery(searchRequest.text || '');
    if (searchRequest.page) setPage(text(searchRequest.page).replace(/^p(?:p)?\.\s*/i, ''));
  }, [searchRequest]);
  useEffect(() => {
    if (!searchRequest?.page || !filing || matches.length) return;
    const requested = text(searchRequest.page).match(/\d+/)?.[0];
    const found = [...pageMap].find(([, number]) => number === requested);
    if (found) pane.current?.querySelector(`[data-block="${found[0]}"]`)?.scrollIntoView({ block: 'start' });
  }, [searchRequest, filing, matches.length, pageMap]);
  useEffect(() => {
    if (!matches.length || !pane.current) return;
    const target = pane.current.querySelector(`[data-search-index="${Math.min(activeMatch, matches.length - 1)}"]`);
    target?.scrollIntoView({ block: 'center', behavior: 'instant' });
  }, [activeMatch, matches]);
  useEffect(() => {
    if (selectedIndex < 0 || !pane.current) return;
    const mark = pane.current.querySelector(`[data-row-index~="${selectedIndex}"]`);
    mark?.scrollIntoView({ block: 'center', behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' });
  }, [selectedUid, selectedIndex, scrollRequest, rows[selectedIndex]?.quote?.start?.block, rows[selectedIndex]?.quote?.start?.offset, filing]);

  function captureSelection() {
    const chosen = window.getSelection();
    if (!chosen?.rangeCount || chosen.isCollapsed) { setSelection(null); return; }
    const range = chosen.getRangeAt(0);
    const startNode = range.startContainer.nodeType === Node.ELEMENT_NODE ? range.startContainer : range.startContainer.parentElement;
    const endNode = range.endContainer.nodeType === Node.ELEMENT_NODE ? range.endContainer : range.endContainer.parentElement;
    const startBlock = startNode?.closest?.('[data-block]');
    const endBlock = endNode?.closest?.('[data-block]');
    if (!startBlock || !endBlock || !pane.current?.contains(startBlock) || !pane.current?.contains(endBlock)) { setSelection(null); return; }
    const content = range.cloneContents();
    content.querySelectorAll('.page-marker').forEach(node => node.remove());
    content.querySelectorAll('.filing-block').forEach(node => node.after(document.createTextNode(' ')));
    const quote = text(content.textContent).replace(/\s+/g, ' ').trim();
    if (!quote) { setSelection(null); return; }
    const startIndex = Number(startBlock.dataset.block), endIndex = Number(endBlock.dataset.block);
    const startPage = [...pageMap].filter(([index]) => index <= startIndex).at(-1)?.[1] || text(blocks[startIndex]?.page);
    const endPage = [...pageMap].filter(([index]) => index <= endIndex).at(-1)?.[1] || text(blocks[endIndex]?.page);
    const pageLabel = startPage && endPage && startPage !== endPage ? `pp. ${startPage}–${endPage}` : startPage ? `p. ${startPage}` : '';
    setSelection({ quote, pageLabel });
  }

  function jumpPage(event) {
    event.preventDefault();
    const found = [...pageMap].find(([, number]) => number.toLocaleLowerCase() === page.trim().toLocaleLowerCase());
    if (found) { setPageError(''); pane.current?.querySelector(`[data-block="${found[0]}"]`)?.scrollIntoView({ block: 'start' }); }
    else setPageError(`Page ${page.trim()} was not found in this filing.`);
  }

  function renderText(block, index) {
    const pieces = segments(block.text, ranges.get(index) || [], needle, matchesByBlock.get(index) || []);
    return pieces.map((piece, pieceIndex) => piece.rows.length || piece.search
      ? <mark key={pieceIndex} className={`${piece.rows.length ? 'quote-mark' : ''} ${piece.rows.includes(selectedIndex) ? 'selected' : ''} ${piece.search ? 'search-mark' : ''}`} data-row-index={piece.rows.join(' ')} data-search-index={piece.search ? matchByPosition.get(`${index}:${piece.from}`) : undefined} onClick={() => piece.rows.length && onSelectRow(rows[piece.rows[0]].uid, true)} title={piece.rows.length ? piece.rows.map(i => `#${text(rows[i]?.id)}`).join(', ') : undefined}>{piece.text}</mark>
      : <React.Fragment key={pieceIndex}>{piece.text}</React.Fragment>);
  }

  return <section className="filing-pane" aria-label="SEC filing">
    <div className="filing-tools">
      <div className="filing-caption"><strong>SEC filing</strong><span>{[deal?.filing?.form_type, deal?.filing?.date_filed].filter(Boolean).join(' · ')}</span></div>
      <div className="filing-search"><Input aria-label="Search filing" contentBefore={<MagnifyingGlassIcon size={16}/>} placeholder="Search filing" value={query} onChange={(_, data) => setQuery(data.value)}/><span className="search-count">{query ? `${matches.length ? activeMatch + 1 : 0} / ${matches.length}` : ''}</span><Button appearance="subtle" icon={<ArrowUpIcon size={16}/>} aria-label="Previous match" disabled={!matches.length} onClick={() => setActiveMatch(i => (i - 1 + matches.length) % matches.length)}/><Button appearance="subtle" icon={<ArrowDownIcon size={16}/>} aria-label="Next match" disabled={!matches.length} onClick={() => setActiveMatch(i => (i + 1) % matches.length)}/></div>
      <form className="page-jump" onSubmit={jumpPage}><label htmlFor="filing-page">Page</label><Input id="filing-page" size="small" value={page} onChange={(_, data) => { setPage(data.value); setPageError(''); }} placeholder="e.g. 31"/><Button size="small" type="submit" disabled={!page.trim()}>Go</Button></form>
    </div>
    {pageError && <div className="page-error" role="alert">{pageError}</div>}
    {selection && onQuoteSelection && <div className="selection-action"><span>{selection.quote.slice(0, 90)}{selection.quote.length > 90 ? '…' : ''}</span><Button size="small" onClick={() => { onQuoteSelection(selection); setSelection(null); }}>Use selected text for quote</Button></div>}
    {loading && <div className="pane-state"><Spinner label="Loading filing"/></div>}
    {error && <div className="pane-state error" role="alert">{error}</div>}
    {!loading && !error && <div className="filing-scroll" ref={pane} onMouseUp={captureSelection} onKeyUp={captureSelection}>
      <div className="filing-paper">
        {blocks.map((block, index) => <React.Fragment key={index}>
          {pageMap.has(index) && <div className={`page-marker ${deal?.pages_reliable ? '' : 'approximate'}`}>Page {pageMap.get(index)}{deal?.pages_reliable ? '' : ' (approximate)'}</div>}
          <div data-block={index} className={`filing-block ${block.kind === 'h' ? 'heading' : block.kind === 'row' ? 'table-row' : ''} ${index === deal?.background_block ? 'background-start' : ''}`}>{renderText(block, index)}</div>
        </React.Fragment>)}
      </div>
    </div>}
  </section>;
}
