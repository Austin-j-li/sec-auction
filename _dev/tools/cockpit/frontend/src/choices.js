import { text } from './api';

// The editor's value lists (the deal payload's `choices`, those of the displayed version's schema) suggest values;
// they never block one. The server does not enforce them and the checker may accept values they lag behind.

// A field whose value lists one outcome per deadline, separated by semicolons ("Extended; Enforced").
export const MULTI_FIELDS = new Set(['Deadline outcome']);
// The drop-down entry that switches a listed field to free text.
export const OTHER = '__other__';

export const valueParts = value => text(value).split(';').map(part => part.trim()).filter(Boolean);
// "Extended" plus "Enforced" gives "Extended; Enforced".
export const addPart = (value, part) => [...valueParts(value), part].join('; ');

// The control for a field: null without a list; 'multi' for a multi-part field (free text and a picker that adds a
// part); 'select' for a blank or listed value (the list, Blank and Other…); 'text' for a value off the list, such as
// a v1.13.2 value shown under v1.14 lists. The reader's choice for the field overrides that: 'other' (they chose
// Other…) gives free text, 'list' (they chose "Choose from the list") gives the drop-down whatever the value.
export function listControl(field, value, options, mode) {
  if (!Array.isArray(options) || !options.length) return null;
  if (MULTI_FIELDS.has(field)) return 'multi';
  if (mode === 'other') return 'text';
  if (mode === 'list') return 'select';
  return !text(value) || options.includes(text(value)) ? 'select' : 'text';
}

// The value a drop-down shows that is not on its list (typed after Other…, or stored off the list), or null. The
// drop-down keeps it as its own entry until the reader picks another, so it is never cleared unseen.
export const offListValue = (value, options) => text(value) && !options.includes(text(value)) ? text(value) : null;
