// =============================================================
// STR-R2B Step 3 · StrategistWarRoom
// Master shell · §08 entry point · canvas ref 03/desktop.html
// -------------------------------------------------------------
// Wraps the seven War Room surfaces in the existing R2A chrome:
//   <StrategistThemeProvider><ControlRoomBackdrop>...</></>.
// Desktop ≥1024 px: CSS Grid 2-col / 3-row.
//   Row 1: Conquest panel (L1) | Mission Board (L2)
//   Row 2: Dasha Timeline (L3) full width
//   Row 3: Pitru-Rin (L4) | Golden Hour (L5)
// Mobile <768 px: horizontal snap-scroll strip -- pass layout="snap".
// =============================================================

import { useState } from 'react';
import { band, bandVerdict, BAND_TOKEN } from './utils';
import ConquestGauge from './ConquestGauge';
import FactorTable from './FactorTable';
import MissionCard from './MissionCard';
import DashaTimeline from './DashaTimeline';
import PitruRinLedger from './PitruRinLedger';
import GoldenHourStrip from './GoldenHourStrip';
import Gate0SubHeader from './Gate0SubHeader';

// R2A imports -- see notes/wiring patch · DO NOT modify these files
import StrategistThemeProvider from '../StrategistThemeProvider';
import ControlRoomBackdrop from '../ControlRoomBackdrop';

import './war-room.css';

// ── Conquest Panel (composition of gauge + factors) ──────────
function ConquestPanel({ conquestScore, factors, stampLabel }) {
  const bandKey = band(conquestScore.score);
  return (
    <div className="cg-panel">
      <div className="cg-panel__left">
        <div className="cg-panel__heading">
          <h3 className="cg-panel__title">Conquest Score</h3>
          {stampLabel && <div className="cg-panel__stamp">{stampLabel}</div>}
        </div>
        <ConquestGauge score={conquestScore.score} size="production" />
        <p className="cg-panel__verdict">{bandVerdict(bandKey)}</p>
      </div>
      <FactorTable factors={factors} />
    </div>
  );
}

// ── Mission Board (variant toolbar + grid) ──────────────────
function MissionBoardPanel({ missions = [] }) {
  const [variant, setVariant] = useState('module');

  return (
    <div className="wr-panel">
      <div className="wr-panel__head">
        <div>
          <h3 className="wr-panel__title">Mission Board</h3>
          <div className="wr-panel__sub" style={{ marginTop: 4 }}>
            {missions.length} active mission{missions.length === 1 ? '' : 's'}
          </div>
        </div>
        <div className="mb-panel__toolbar" role="tablist" aria-label="Mission variant">
          {MissionCard.VARIANTS.map(v => (
            <button
              key={v}
              type="button"
              role="tab"
              aria-selected={variant === v}
              className={`mb-panel__pill ${variant === v ? 'mb-panel__pill--on' : ''}`}
              onClick={() => setVariant(v)}
            >
              {v}
            </button>
          ))}
        </div>
      </div>

      <div className={`mc-grid mc-grid--${variant}`}>
        {missions.map((m, i) => (
          <MissionCard
            key={m.id || i}
            mission={m}
            variant={variant}
            id={m.code || m.id}
          />
        ))}
      </div>
    </div>
  );
}

/**
 * StrategistWarRoom -- master shell
 *
 * props
 *   conquestScore  { score, stampLabel? }
 *   factors[]      → FactorTable
 *   missions[]     → Mission Board (engine emit shape, §05)
 *   dasha          → DashaTimeline
 *   transition     → DashaTimeline
 *   pitruRin[]     → PitruRinLedger
 *   pitruDelta     → PitruRinLedger netDelta
 *   goldenHour[]   → GoldenHourStrip windows
 *   kpVerdict      → Gate 0 sub-header
 *   locationLabel  → GH strip subheader
 *   dateLabel      → GH day rail
 *   layout         "grid" (default) | "snap" (mobile)
 *   onRecalibrate  callback for Gate 0 CTA
 */
export default function StrategistWarRoom({
  conquestScore = { score: 0 },
  factors = [],
  missions = [],
  dasha,
  transition,
  pitruRin = [],
  pitruDelta,
  pitruEmptyMeta,
  goldenHour = [],
  kpVerdict = '',
  locationLabel,
  dateLabel,
  layout = 'grid',
  onRecalibrate = () => {},
}) {
  return (
    <StrategistThemeProvider>
      <ControlRoomBackdrop>
        <div className="wr">
          <Gate0SubHeader
            score={conquestScore.score}
            kpVerdict={kpVerdict}
            onRecalibrate={onRecalibrate}
          />

          {layout === 'snap' ? (
            <div className="wr__snap">
              <ConquestPanel
                conquestScore={conquestScore}
                factors={factors}
                stampLabel={conquestScore.stampLabel}
              />
              <MissionBoardPanel missions={missions} />
              <DashaTimeline dasha={dasha} transition={transition} compact />
              <PitruRinLedger
                debts={pitruRin}
                netDelta={pitruDelta}
                emptyMeta={pitruEmptyMeta}
              />
              <GoldenHourStrip
                windows={goldenHour}
                locationLabel={locationLabel}
                dateLabel={dateLabel}
              />
            </div>
          ) : (
            <div className="wr__grid">
              <div>
                <ConquestPanel
                  conquestScore={conquestScore}
                  factors={factors}
                  stampLabel={conquestScore.stampLabel}
                />
              </div>
              <div>
                <MissionBoardPanel missions={missions} />
              </div>

              <div className="wr__cell--full">
                <DashaTimeline dasha={dasha} transition={transition} />
              </div>

              <div>
                <PitruRinLedger
                  debts={pitruRin}
                  netDelta={pitruDelta}
                  emptyMeta={pitruEmptyMeta}
                />
              </div>
              <div>
                <GoldenHourStrip
                  windows={goldenHour}
                  locationLabel={locationLabel}
                  dateLabel={dateLabel}
                />
              </div>
            </div>
          )}
        </div>
      </ControlRoomBackdrop>
    </StrategistThemeProvider>
  );
}
