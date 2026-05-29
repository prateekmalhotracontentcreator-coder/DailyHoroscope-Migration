// -----------------------------------------------------------------
// LKGateSummaries.jsx
// Source: STR-2E · LKGateSummaries.html  (CD delivery)
// Extracted + converted: 2026-05-29
// 6-step recipe: PROCESS_CD_INTEGRATION_PROTOCOL.md
//
// Exports:
//   default  LKGateSummaries  -- main page component, receives { gates, asOf }
//   named    LKStatusChip     -- clear / active / warning / dormant chip
//   named    ToneBar          -- 5-tick coloured gate status bar
//   named    GateRow          -- list-view gate row
//   named    GateCard         -- grid-view gate card
//   named    LKStatusChipProofStrip -- 4-status proof set (CD canvas, retained per TT)
//
// CSS: import '../../../styles/strategist-2e-lkgates.css'
//      (import in the page that uses this component)
// -----------------------------------------------------------------

// Step 1 -- React import
import React, { useState } from 'react';

// Step 5 -- shared primitives
import { SegPill, SectionHeader } from './StrategistPrimitives';

// -----------------------------------------------------------------
// LKStatusChip · sibling of VerdictChip · A1 split
// clear=emerald · active=gold · warning=amber · dormant=red
// CSS: .lk-chip defined in strategist-2e-lkgates.css
// -----------------------------------------------------------------
const LK_META = {
  clear:   { label: 'Clear',   pip: true,  glyph: null },
  active:  { label: 'Active',  pip: true,  glyph: null },
  warning: { label: 'Warning', pip: true,  glyph: null },
  dormant: { label: 'Dormant', pip: false, glyph: '○' },
};

export function LKStatusChip({ status }) {
  const meta = LK_META[status] || LK_META.clear;
  return (
    <span className={`lk-chip lk-chip--${status}`}>
      {meta.glyph ? <span aria-hidden="true">{meta.glyph}</span> : null}
      {meta.pip ? <span className="lk-chip__pip" /> : null}
      {meta.label}
    </span>
  );
}

// -----------------------------------------------------------------
// ToneBar -- five coloured ticks summarising gate states
// -----------------------------------------------------------------
export function ToneBar({ gates }) {
  return (
    <span className="tone-bar" aria-hidden="true">
      {gates.map((g) => (
        <span key={g.id} className={`tone-bar__tick tone-bar__tick--${g.status}`} title={`${g.id} · ${g.status}`} />
      ))}
    </span>
  );
}

// -----------------------------------------------------------------
// GateRow -- list view row
// Step 2: gate data received as prop (was window.SEEKER.gates[])
// -----------------------------------------------------------------
export function GateRow({ gate }) {
  return (
    <article className={`lk-row lk-row--${gate.status}`}>
      <div className="lk-row__code">
        <b>{gate.code}</b>
        {gate.id}
      </div>
      <div className="lk-row__body">
        <div className="lk-row__title-line">
          <span className="lk-row__name">{gate.name}</span>
          <span className="lk-row__facet">{gate.facet}</span>
        </div>
        <p className="lk-row__narrative">{gate.narrative}</p>
      </div>
      <div className="lk-row__aside">
        <LKStatusChip status={gate.status} />
        <div className={`lk-row__aside-detail lk-row__aside-detail--${gate.status}`}>
          {gate.asideLabel}
          <b>{gate.asideValue}</b>
        </div>
      </div>
    </article>
  );
}

// -----------------------------------------------------------------
// GateCard -- grid view card (2+3 layout)
// -----------------------------------------------------------------
export function GateCard({ gate }) {
  return (
    <article className={`lk-card lk-card--${gate.status}`}>
      <div className="lk-card__top">
        <span className="lk-card__code">Gate {gate.code}</span>
        <LKStatusChip status={gate.status} />
      </div>
      <h3 className="lk-card__name">{gate.name}</h3>
      <p className="lk-card__facet">{gate.facet}</p>
      <p className="lk-card__narrative">{gate.narrative}</p>
      <div className="lk-card__aside">
        <span>{gate.asideLabel}</span>
        <b>{gate.asideValue}</b>
      </div>
    </article>
  );
}

// -----------------------------------------------------------------
// LKStatusChipProofStrip -- 4-status chip proof set
// CD design canvas component. No live data. Retained per TT variant
// policy (all CD variants kept).
// -----------------------------------------------------------------
export function LKStatusChipProofStrip() {
  return (
    <div className="lk-proof">
      <div className="lk-proof__head">
        <span className="lk-proof__eyebrow">Status chip system &middot; proof set</span>
        <span className="lk-proof__note">
          Warning &rarr; amber &middot; Dormant &rarr; red &middot; split direction from A1 sign-off doc &sect;3
        </span>
      </div>
      <div className="lk-proof__row">
        <LKStatusChip status="clear" />
        <LKStatusChip status="active" />
        <LKStatusChip status="warning" />
        <LKStatusChip status="dormant" />
        <div className="lk-proof__rule" />
        <span className="lk-proof__label">sibling of VerdictChip &middot; imports nothing new &middot; token-driven</span>
      </div>
    </div>
  );
}

// Count gates by status
function gateCountSummary(gates) {
  return gates.reduce((m, g) => {
    m[g.status] = (m[g.status] || 0) + 1;
    return m;
  }, {});
}

// -----------------------------------------------------------------
// LKGateSummaries -- main exported component
// Receives: { gates, asOf }
//   gates  -- array from live API gate_summaries
//   asOf   -- display timestamp string
//
// Live API field map (PROCESS_CD_INTEGRATION_PROTOCOL.md §5):
//   gates  <- data.gate_summaries (array of gate objects)
//   Each gate object shape mirrors the SEEKER.gates stub:
//     { id, code, name, facet, status, narrative, asideLabel, asideValue }
// -----------------------------------------------------------------
// view: optional override ('list'|'grid'). When provided, hides internal toggle.
export default function LKGateSummaries({ gates = [], asOf, view: viewProp = null, showToggle }) {
  const [viewState, setViewState] = useState('list');
  const controlled = viewProp !== null;
  const view = controlled ? viewProp : viewState;
  const setView = controlled ? () => {} : setViewState;
  const showToggleActual = showToggle !== undefined ? showToggle : !controlled;

  // Step 6 -- safe fallback for loading state
  const safeGates = Array.isArray(gates) ? gates : [];
  const counts = gateCountSummary(safeGates);

  return (
    <>
      <SectionHeader
        title="Lal Kitab Diagnostics"
        meta={null}
        right={
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: 16 }}>
            <span className="lk-summary">
              <ToneBar gates={safeGates} />
              <span><b>{counts.clear || 0}</b> clear</span>
              <span className="lk-summary__sep">&middot;</span>
              <span><b>{counts.active || 0}</b> active</span>
              <span className="lk-summary__sep">&middot;</span>
              <span><b>{counts.warning || 0}</b> warn</span>
              <span className="lk-summary__sep">&middot;</span>
              <span><b>{counts.dormant || 0}</b> dorm</span>
            </span>
            {showToggleActual && (
              <SegPill
                segments={['list', 'grid']}
                value={view}
                onChange={setView}
                size="sm"
                ariaLabel="View density"
              />
            )}
          </div>
        }
      />

      {view === 'list' ? (
        <div className="lk-list">
          {safeGates.map((g) => <GateRow key={g.id} gate={g} />)}
        </div>
      ) : (
        <div className="lk-grid">
          <div className="lk-grid__row lk-grid__row--top">
            {safeGates.slice(0, 2).map((g) => <GateCard key={g.id} gate={g} />)}
          </div>
          <div className="lk-grid__row lk-grid__row--bot">
            {safeGates.slice(2, 5).map((g) => <GateCard key={g.id} gate={g} />)}
          </div>
        </div>
      )}

      <LKStatusChipProofStrip />
    </>
  );
}
