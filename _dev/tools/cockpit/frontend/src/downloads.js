// Excel download links: pure functions shared by the deal page.
// The working copy and a past revision ("rev:N", from History) download with a Source sheet (EDGAR links and
// provenance) unless asked for their four sheets; the server names them {slug}-working-r{N}.xlsx. A version
// downloads as its stored bytes unless asked for the Source sheet.

export function exportLinks(slug, version) {
  const href = `/api/deal/${slug}/export?version=${encodeURIComponent(version)}`;
  const past = /^rev:\d+$/.test(version);
  return version === 'working' || past
    ? { href, title: `${past ? `Revision ${version.slice(4)}’s` : 'The working copy’s'} four sheets and a Source sheet with the EDGAR link and provenance`,
      other: { href: `${href}&source=0`, label: 'Four sheets only (checker format)' } }
    : { href, title: 'The stored workbook, unchanged',
      other: { href: `${href}&source=1`, label: 'With Source sheet' } };
}
