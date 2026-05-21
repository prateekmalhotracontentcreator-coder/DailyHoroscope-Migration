// ─────────────────────────────────────────────────────────────────────────────
// StrategistExecutivePage.jsx
// Executive overview page -- repurposed Codex overview, accessible inside
// The Strategist module at /strategist/executive.
//
// Shows the original Codex-built StrategistLanding as a module-internal
// executive summary / overview surface, wrapped with the Strategist theme.
// ─────────────────────────────────────────────────────────────────────────────

import React from 'react';
import { StrategistThemeProvider } from '@/components/strategist/StrategistThemeProvider';
import { StrategistLanding } from './StrategistPage';
import '@/styles/strategist-tokens.css';

export default function StrategistExecutivePage() {
  return (
    <StrategistThemeProvider>
      <StrategistLanding />
    </StrategistThemeProvider>
  );
}
