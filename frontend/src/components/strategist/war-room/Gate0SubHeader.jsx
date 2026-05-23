// =============================================================
// STR-R2B Step 3 · Gate0SubHeader
// canvas ref 02/01 · ART 1.3 + 03/desktop nav
// -------------------------------------------------------------
// Sticky compact bar that surfaces the Conquest Score, KP Oracle
// verdict, and Re-Calibrate CTA -- visible on scroll above the panel grid.
// Uses ConquestGauge size="compact" so the score read stays in one place.
// =============================================================

import { band, bandLabel } from './utils';
import ConquestGauge from './ConquestGauge';

const BAND_CHIP = {
  sovereign: 'emerald',
  friction:  'amber',
  siege:     'orange',
  lockdown:  'red',
};

/**
 * Gate0SubHeader
 *
 * props
 *   score        {number 0-99}
 *   kpVerdict    {string}  italic line from the KP Oracle
 *   onRecalibrate {function?}
 */
export default function Gate0SubHeader({ score = 0, kpVerdict = '', onRecalibrate }) {
  const bandKey = band(score);
  return (
    <div className="gate0">
      <div className="gate0__left">
        <ConquestGauge score={score} size="compact" />
        <div>
          <div className="gate0__label">Conquest Score</div>
          <div className="gate0__score-row">
            <span className="gate0__score">{score}</span>
            <span className={`wr-chip wr-chip--${BAND_CHIP[bandKey]}`}>{bandLabel(bandKey)}</span>
          </div>
        </div>
      </div>

      <div className="gate0__rule" aria-hidden="true" />

      <div>
        <div className="gate0__label">KP Oracle Verdict</div>
        <div className="gate0__verdict">"{kpVerdict}"</div>
      </div>

      <div className="gate0__rule" aria-hidden="true" />

      <button type="button" className="gate0__recal" onClick={onRecalibrate}>
        Re-Calibrate ▸
      </button>
    </div>
  );
}
