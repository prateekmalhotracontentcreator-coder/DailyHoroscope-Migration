// ─────────────────────────────────────────────────────────────────────────────
// StrategistThemeProvider.jsx
// STR-R2-A · Visual Foundation
//
// Holds the Strategist module's theme-mode state. Four states:
//   "light"        · default; matches rest of web app
//   "dark"         · navy/charcoal, gold accents
//   "cr-ambient"   · Control Room Variant A (muted green grid)
//   "cr-tactical"  · Control Room Variant B (brighter green grid)
//
// Persists to localStorage under STRATEGIST_THEME_KEY. Reads on mount,
// guards against legacy / invalid values, and broadcasts a `strategist:mode`
// CustomEvent for any non-React surface that needs to listen.
// ─────────────────────────────────────────────────────────────────────────────

import React, {
  createContext, useCallback, useContext, useEffect, useMemo, useState,
} from 'react';

export const STRATEGIST_MODES = ['light', 'dark', 'cr-ambient', 'cr-tactical'];
export const STRATEGIST_THEME_KEY = 'strategist_theme_mode';
const DEFAULT_MODE = 'light';

const StrategistThemeContext = createContext({
  mode: DEFAULT_MODE,
  setMode: () => {},
  isControlRoom: false,
  controlRoomVariant: null,
});

function isValidMode(m) {
  return STRATEGIST_MODES.indexOf(m) !== -1;
}

function readInitialMode() {
  if (typeof window === 'undefined') return DEFAULT_MODE;
  try {
    const stored = window.localStorage.getItem(STRATEGIST_THEME_KEY);
    if (stored && isValidMode(stored)) return stored;
  } catch (_) { /* localStorage unavailable -- fall through */ }
  return DEFAULT_MODE;
}

export function StrategistThemeProvider({ children, initialMode }) {
  const [mode, setModeState] = useState(() =>
    isValidMode(initialMode) ? initialMode : readInitialMode()
  );

  const setMode = useCallback((next) => {
    if (!isValidMode(next)) return;
    setModeState(next);
    try {
      window.localStorage.setItem(STRATEGIST_THEME_KEY, next);
    } catch (_) { /* ignore */ }
    try {
      window.dispatchEvent(new CustomEvent('strategist:mode', { detail: { mode: next } }));
    } catch (_) { /* ignore */ }
  }, []);

  // Cross-tab sync
  useEffect(() => {
    function onStorage(e) {
      if (e.key === STRATEGIST_THEME_KEY && isValidMode(e.newValue)) {
        setModeState(e.newValue);
      }
    }
    window.addEventListener('storage', onStorage);
    return () => window.removeEventListener('storage', onStorage);
  }, []);

  const value = useMemo(() => {
    const isCR = mode === 'cr-ambient' || mode === 'cr-tactical';
    return {
      mode,
      setMode,
      isControlRoom: isCR,
      controlRoomVariant: isCR ? (mode === 'cr-tactical' ? 'tactical' : 'ambient') : null,
    };
  }, [mode, setMode]);

  return (
    <StrategistThemeContext.Provider value={value}>
      <div className="strategist-module" data-mode={mode}>
        {children}
      </div>
    </StrategistThemeContext.Provider>
  );
}

export function useStrategistTheme() {
  return useContext(StrategistThemeContext);
}

export default StrategistThemeProvider;
