// =============================================================
// STR-R2B Step 3 · War Room utilities
// -------------------------------------------------------------
// planetColor()    → CSS-var string for a planet name
// band()           → 'sovereign' | 'friction' | 'siege' | 'lockdown'
// bandVerdict()    → locked Q-03 verdict copy (Temple-approved)
// useNow()         → React hook · returns a Date that re-renders every 1s
// =============================================================

import { useEffect, useState } from 'react';

// --- planet colour -------------------------------------------------
const PLANETS = ['sun','moon','mars','mercury','jupiter','venus','saturn','rahu','ketu'];

/**
 * Returns the CSS custom-property reference for a planet.
 * Always read through `var()` so theme overrides still flow.
 *   planetColor('jupiter') → 'var(--planet-jupiter)'
 */
export function planetColor(name) {
  const key = String(name || '').toLowerCase();
  return PLANETS.includes(key) ? `var(--planet-${key})` : 'var(--ink-2)';
}

// --- conquest band -------------------------------------------------
/**
 * Pure score→band derivation. Thresholds from Brief §4.3 -- literal.
 *   75-99 → sovereign · 50-74 → friction · 25-49 → siege · 0-24 → lockdown
 */
export function band(score) {
  const s = Math.max(0, Math.min(99, Number(score) || 0));
  if (s >= 75) return 'sovereign';
  if (s >= 50) return 'friction';
  if (s >= 25) return 'siege';
  return 'lockdown';
}

/**
 * Locked verdict copy -- Q-03, Temple Team approved verbatim.
 * Step 3 hard-codes these. Do not edit without a brief amendment.
 */
const VERDICTS = {
  sovereign: 'Command is yours. Mount the offensive.',
  friction:  'Hold the line. Move only on prepared ground.',
  siege:     'Conserve. Refuse engagement except defensive.',
  lockdown:  'Stand down. Remediate before the next window.',
};
export function bandVerdict(bandKey) {
  return VERDICTS[bandKey] || '';
}

// --- band tone helpers --------------------------------------------
export const BAND_TOKEN = {
  sovereign: '--emerald',
  friction:  '--amber',
  siege:     '--orange',
  lockdown:  '--red',
};

export function bandLabel(bandKey) {
  return bandKey ? bandKey.charAt(0).toUpperCase() + bandKey.slice(1) : '';
}

// --- live "now" hook ----------------------------------------------
/**
 * Re-renders every `tickMs` (default 1000ms). Returns a Date.
 * Used by GoldenHourStrip for live countdown + active-window detection.
 *
 *   const now = useNow();          // 1 s tick
 *   const now = useNow(60_000);    // 60 s tick (cheaper for non-second UI)
 */
export function useNow(tickMs = 1000) {
  const [now, setNow] = useState(() => new Date());
  useEffect(() => {
    const id = setInterval(() => setNow(new Date()), tickMs);
    return () => clearInterval(id);
  }, [tickMs]);
  return now;
}

// --- time helpers (used by GoldenHourStrip) -----------------------
/**
 * Parses "HH:MM" against a reference date (defaults to today).
 * Returns a Date at that wall-clock time, same Y-M-D as ref.
 */
export function parseHM(hm, ref = new Date()) {
  const [h, m] = String(hm).split(':').map(Number);
  const d = new Date(ref);
  d.setHours(h || 0, m || 0, 0, 0);
  return d;
}

export function formatHMS(ms) {
  const total = Math.max(0, Math.floor(ms / 1000));
  const h = String(Math.floor(total / 3600)).padStart(2, '0');
  const m = String(Math.floor((total % 3600) / 60)).padStart(2, '0');
  const s = String(total % 60).padStart(2, '0');
  return `${h}:${m}:${s}`;
}
