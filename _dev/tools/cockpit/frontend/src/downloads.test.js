import { describe, expect, it } from 'vitest';
import { exportLinks } from './downloads';

describe('Excel download links', () => {
  it('gives the working copy its Source sheet by default and four sheets as the option', () => {
    const links = exportLinks('mac-gray', 'working');
    expect(links.href).toBe('/api/deal/mac-gray/export?version=working');
    expect(links.other).toEqual({ href: '/api/deal/mac-gray/export?version=working&source=0', label: 'Four sheets only (checker format)' });
  });

  it('keeps a version raw by default and offers the Source sheet', () => {
    const links = exportLinks('mac-gray', 'opus55-medium');
    expect(links.href).toBe('/api/deal/mac-gray/export?version=opus55-medium');
    expect(links.title).toBe('The stored workbook, unchanged');
    expect(links.other).toEqual({ href: '/api/deal/mac-gray/export?version=opus55-medium&source=1', label: 'With Source sheet' });
  });

  it('downloads a past revision like the working copy', () => {
    const links = exportLinks('mac-gray', 'rev:3');
    expect(links.href).toBe('/api/deal/mac-gray/export?version=rev%3A3');
    expect(links.title).toBe('Revision 3’s four sheets and a Source sheet with the EDGAR link and provenance');
    expect(links.other).toEqual({ href: '/api/deal/mac-gray/export?version=rev%3A3&source=0', label: 'Four sheets only (checker format)' });
  });

  it('encodes the version id', () => {
    expect(exportLinks('d', 'a b').other.href).toBe('/api/deal/d/export?version=a%20b&source=1');
  });
});
