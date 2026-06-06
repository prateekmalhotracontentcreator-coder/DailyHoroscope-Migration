// -----------------------------------------------------------------
// KPGate0Panel.jsx
// Source: STR-2B · KPGate0Panel.html  (CD delivery)
// Extracted + converted: 2026-05-29
// 6-step recipe: PROCESS_CD_INTEGRATION_PROTOCOL.md
//
// Standalone component on StrategistActionPlanPage (per TT process map).
//
// Canvas review control (fresh/aging/due SegPill) removed as specified
// in CD's own integration note: "CC removes it; the live askedDaysAgo decides."
//
// Exports:
//   default  KPGate0Panel          -- main component, receives { gate, asOf }
//   named    Gate0Panel            -- the single Gate 0 inline panel
//   named    KPVerdictChipProofStrip -- verdict proof set (CD canvas, retained per TT)
//
// CSS: import '../../../styles/strategist-2b-gate0.css'
// -----------------------------------------------------------------

// Step 1 -- React import
import React from 'react';

// Step 5 -- shared primitives
import { VerdictChip, SectionHeader } from './StrategistPrimitives';

// -----------------------------------------------------------------
// Re-consult threshold (v2 Q-04)
// -----------------------------------------------------------------
const RECONSULT_AFTER_DAYS = 30;

// Derive window tone from days since reading
function getWindowMeta(days) {
  if (days > RECONSULT_AFTER_DAYS) {
    return { label: 'past 30-day window', tone: 'var(--red)' };
  }
  if (days > 20) {
    return { label: 'approaching re-consult', tone: 'var(--amber)' };
  }
  return { label: 'within window', tone: 'var(--emerald)' };
}

const ArrowIcon = () => (
  <svg className="kp-panel__cta-arrow" viewBox="0 0 12 12" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="2" y1="6" x2="10" y2="6"/><polyline points="7,3 10,6 7,9"/>
  </svg>
);

// -----------------------------------------------------------------
// Gate0Panel -- the single Gate 0 inline panel
// Step 2: gate data received as prop (was window.SEEKER.kpGate0)
// Canvas FRESHNESS control removed per CD's integration note.
//
// Props: { gate }
//   gate.verdict       -- 'yes'|'wait'|'no'|'pray'
//   gate.question      -- the question text
//   gate.askedDaysAgo  -- number of days since reading
//   gate.readAt        -- formatted reading date string
//   gate.sublord       -- sub-lord chain string
//   gate.significators -- array of house codes
//   gate.cuspalRuler   -- planet string
//
// onReconsult / onViewReading -- action callbacks wired by parent page
// -----------------------------------------------------------------
export function Gate0Panel({ gate, onReconsult, onViewReading }) {
  const verdict = (gate?.verdict ?? 'wait').toLowerCase();
  const days = gate?.askedDaysAgo ?? 0;
  const readAt = gate?.readAt ?? '--';
  const due = days > RECONSULT_AFTER_DAYS;
  const { label: windowLabel, tone: windowTone } = getWindowMeta(days);

  return (
    <article className={`kp-panel kp-panel--${verdict}`}>
      <div className="kp-panel__left">
        <span className="kp-panel__eyebrow">
          Standing verdict &middot; <b>Gate 0</b>
          <VerdictChip type={verdict} active />
        </span>

        <span className="kp-panel__q-label">The question put to the oracle</span>
        <p className="kp-panel__question">{gate?.question ?? '--'}</p>

        <span className="kp-panel__age">
          <b>{days}</b> days since reading
          <span className="kp-panel__age-sep">&middot;</span>
          last read {readAt}
        </span>

        <div className="kp-panel__cta-row">
          {due ? (
            <React.Fragment>
              <button type="button" className="kp-panel__cta" onClick={onReconsult}>
                Re-consult Gate 0 <ArrowIcon />
              </button>
              <button type="button" className="kp-panel__cta-secondary" onClick={onViewReading}>
                View this reading
              </button>
            </React.Fragment>
          ) : (
            <React.Fragment>
              <span className="kp-panel__fresh-note">Reading holds &middot; no re-consult due</span>
              <button type="button" className="kp-panel__cta-secondary" onClick={onViewReading}>
                View this reading
              </button>
            </React.Fragment>
          )}
        </div>
      </div>

      <aside className="kp-aside">
        {/* Show KP chain detail only when data is present; hide blank rows otherwise */}
        {(gate?.sublord && gate.sublord !== '--') || (gate?.significators ?? []).length > 0 || (gate?.cuspalRuler && gate.cuspalRuler !== '--') ? (
          <>
            <span className="kp-aside__lbl">KP reading detail</span>
            <div className="kp-aside__rows">
              <div className="kp-aside__row">
                <span className="kp-aside__k">Sub-lord chain</span>
                <span className="kp-aside__v">{gate?.sublord ?? '--'}</span>
              </div>
              <div className="kp-aside__row">
                <span className="kp-aside__k">Significators</span>
                <span className="kp-aside__sig">
                  {(gate?.significators ?? []).map((h) => <span key={h}>{h}</span>)}
                </span>
              </div>
              <div className="kp-aside__row">
                <span className="kp-aside__k">Cuspal ruler</span>
                <span className="kp-aside__v">{gate?.cuspalRuler ?? '--'}</span>
              </div>
            </div>
          </>
        ) : null}
        <div className="kp-aside__div" />
        <div className="kp-aside__stat" style={{ '--kp-window': windowTone }}>
          <span className="kp-aside__stat-num">{days}<small>days</small></span>
          <span className="kp-aside__stat-sub">{windowLabel}</span>
        </div>
      </aside>
    </article>
  );
}

// -----------------------------------------------------------------
// KPVerdictChipProofStrip -- verdict proof set
// CD design canvas component. No live data. Retained per TT variant policy.
// -----------------------------------------------------------------
export function KPVerdictChipProofStrip() {
  return (
    <div className="kp-proof">
      <div className="kp-proof__head">
        <span className="kp-proof__eyebrow">VerdictChip system &middot; the live feed drives this axis</span>
        <span className="kp-proof__note">
          Shell renders the stub verdict (Yes). CC swaps in the live KP verdict &mdash; chip type stays full gold on PRAY
        </span>
      </div>
      <div className="kp-proof__row">
        <VerdictChip type="yes" />
        <VerdictChip type="wait" />
        <VerdictChip type="no" />
        <VerdictChip type="pray" />
      </div>
    </div>
  );
}

// -----------------------------------------------------------------
// KPGate0Panel -- main exported component (standalone on ActionPlanPage)
// Receives: { gate, asOf }
//   gate  -- KP Oracle reading object (from /api/krishna-prashnavali or similar)
//   asOf  -- display timestamp string
//
// Live API field map:
//   gate.verdict       <- KP Oracle last verdict
//   gate.question      <- KP Oracle question text
//   gate.askedDaysAgo  <- days since last reading
//   gate.readAt        <- formatted reading date
//   gate.sublord       <- sub-lord chain
//   gate.significators <- array of house codes
//   gate.cuspalRuler   <- cuspal ruler planet
//
// Note: when STR-2A2 (KP Oracle integration) lands, this component
// wires to /api/krishna-prashnavali for live gate data.
// -----------------------------------------------------------------
export default function KPGate0Panel({ gate, asOf, onReconsult, onViewReading, showProofStrip = false }) {
  return (
    <>
      <SectionHeader
        title="KP Gate 0"
        meta="Krishna Prashnavali · shell"
        right={null}
      />

      <Gate0Panel
        gate={gate}
        onReconsult={onReconsult}
        onViewReading={onViewReading}
      />

      {showProofStrip && <KPVerdictChipProofStrip />}
    </>
  );
}
