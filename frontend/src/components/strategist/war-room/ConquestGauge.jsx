// =============================================================
// STR-R2B Step 3 · ConquestGauge
// Brief §4.3 · Layer 1 atom · canvas ref 02/01 · ART 1.1 + 1.3
// -------------------------------------------------------------
// SVG ring 0-99, colour-coded by band. Two sizes:
//   "production" -- 220px, with score + band label inside the ring
//   "compact"    -- 44px, naked ring (Gate 0 sub-header)
//
// Derives band internally via band(score) -- pure function, no state.
// =============================================================

import { band } from './utils';

const CIRC = 628.3;   // 2π·100 -- rounded to one decimal · matches canvas
const RADIUS = 100;
const VIEW = 240;

export default function ConquestGauge({
  score = 0,
  size = 'production',
  showVerdict = false,   // kept for API parity -- verdict copy lives in parent
}) {
  const s = Math.max(0, Math.min(99, Number(score) || 0));
  const bandKey = band(s);
  const offset = CIRC * (1 - s / 99);

  return (
    <div className={`cg cg--${size} cg--${bandKey}`} aria-label={`Conquest Score ${s} of 99`}>
      <svg className="cg__svg" viewBox={`0 0 ${VIEW} ${VIEW}`}>
        <circle
          className="cg__track"
          cx={VIEW / 2} cy={VIEW / 2} r={RADIUS}
          strokeDasharray={CIRC}
          strokeDashoffset="0"
        />
        <circle
          className="cg__fill"
          cx={VIEW / 2} cy={VIEW / 2} r={RADIUS}
          strokeDasharray={CIRC}
          strokeDashoffset={offset}
        />
      </svg>

      {size === 'production' && (
        <div className="cg__center">
          <div className="cg__score">{s}</div>
          <div className="cg__max">/ 99</div>
          <div className="cg__band">{bandKey.charAt(0).toUpperCase() + bandKey.slice(1)}</div>
        </div>
      )}
    </div>
  );
}
