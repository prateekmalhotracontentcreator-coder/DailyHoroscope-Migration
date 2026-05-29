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
import { StrategistThemeToggle } from '@/components/strategist/StrategistThemeToggle';
import { StrategistLanding } from './StrategistPage';
import '@/styles/strategist-tokens.css';

export default function StrategistExecutivePage() {
  return (
    <StrategistThemeProvider>
      {/* Floating Strategist theme toggle -- top-right, module-scoped */}
      <div style={{ position: 'fixed', top: 16, right: 20, zIndex: 50 }}>
        <StrategistThemeToggle />
      </div>
      <StrategistLanding />
    </StrategistThemeProvider>
  );
}
