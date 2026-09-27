import { describe, expect, it } from 'vitest';
import { addPart, listControl, offListValue, valueParts } from './choices';

const OUTCOMES = ['Enforced', 'Extended', 'Extended (late bid accepted)', 'No deadline stated', 'Passed without action', 'Unclear'];
const FORMALITY = ['Formal', 'Informal', 'Unclear'];

describe('listed fields in the editor', () => {
  it('builds a multi-part deadline outcome from a blank cell', () => {
    expect(addPart('', 'Extended')).toBe('Extended');
    expect(addPart('Extended', 'Enforced')).toBe('Extended; Enforced');
    expect(addPart(' Extended ;  ', 'Enforced')).toBe('Extended; Enforced');
    expect(valueParts('Late bids accepted; Enforced')).toEqual(['Late bids accepted', 'Enforced']);
  });
  it('gives a deadline outcome free text with a picker, whatever it holds', () => {
    expect(listControl('Deadline outcome', '', OUTCOMES)).toBe('multi');
    expect(listControl('Deadline outcome', 'Late bids accepted', OUTCOMES)).toBe('multi');
  });
  it('keeps the drop-down for blank and listed values, and free text for others or after Other…', () => {
    expect(listControl('Formality', '', FORMALITY)).toBe('select');
    expect(listControl('Formality', 'Formal', FORMALITY)).toBe('select');
    expect(listControl('Formality', 'Formal', FORMALITY, 'other')).toBe('text');
    expect(listControl('All cash', 'Yes', ['Varies', 'Y'])).toBe('text');
    expect(listControl('Note', 'x', undefined)).toBeNull();
    expect(listControl('Formality', '', [])).toBeNull();
  });
  it('brings the drop-down back with "Choose from the list", keeping a typed off-list value visible', () => {
    // Other…, then a value typed off the list: free text.
    expect(listControl('Formality', 'Formal-ish', FORMALITY, 'other')).toBe('text');
    // "Choose from the list": the drop-down again, with the typed value as its own entry until another is picked.
    expect(listControl('Formality', 'Formal-ish', FORMALITY, 'list')).toBe('select');
    expect(offListValue('Formal-ish', FORMALITY)).toBe('Formal-ish');
    // A stored off-list value can be brought to the list the same way.
    expect(listControl('Deadline outcome', 'Late bids accepted', OUTCOMES, 'list')).toBe('multi');
    expect(listControl('All cash', 'Yes', ['Varies', 'Y'], 'list')).toBe('select');
    expect(offListValue('Formal', FORMALITY)).toBeNull();
    expect(offListValue('', FORMALITY)).toBeNull();
  });
});
