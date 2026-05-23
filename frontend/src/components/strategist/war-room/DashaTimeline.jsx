// =============================================================
// STR-R2B Step 3 · DashaTimeline
// Brief §4.4 · Layer 3 · canvas ref 02/03 · ART 3.1
// -------------------------------------------------------------
// Three nested bars stacked vertically -- Mahadasha / Antardasha / Pratyantar.
// Planet-coloured fill, glow on active. 25/50/75% tick marks.
// Transition strip below, recoloured to whichever tier is next.
// =============================================================

import { planetColor } from './utils';

const TIER_LABEL = { mahadasha: 'Mahadasha', antardasha: 'Antardasha', pratyantar: 'Pratyantar' };
const TIER_SHORT = { mahadasha: 'MD',       antardasha: 'AD',         pratyantar: 'PD' };

function pct(elapsed, total) {
  if (!total) return 0;
  return Math.max(0, Math.min(100, (elapsed / total) * 100));
}

function formatRemaining(elapsed, total) {
  const remDays = Math.max(0, total - elapsed);
  if (remDays >= 365) {
    return { val: (remDays / 365).toFixed(1), unit: 'yr' };
  }
  if (remDays >= 30) {
    return { val: Math.round(remDays / 30), unit: 'mo' };
  }
  return { val: Math.round(remDays), unit: 'd' };
}

function formatTotal(total) {
  if (total >= 365) return `${(total / 365).toFixed(1)} yr`;
  if (total >= 30)  return `${Math.round(total / 30)} mo`;
  return `${total} d`;
}

function Bar({ tier, planet, elapsedDays, totalDays, startedLabel, endsLabel, active = true, compact = false }) {
  const filled = pct(elapsedDays, totalDays);
  const rem = formatRemaining(elapsedDays, totalDays);
  const planetColorCss = planetColor(planet);

  return (
    <div
      className={`dt-bar ${active ? 'dt-bar--active' : ''}`}
      style={{ '--planet': planetColorCss }}
    >
      <div className="dt-bar__head" style={{ marginBottom: compact ? 6 : 8 }}>
        <div>
          <span
            className="dt-bar__planet"
            style={{ color: planetColorCss, fontSize: compact ? 13 : 15 }}
          >
            <span className="pip" style={{ background: planetColorCss }} />
            {planet.charAt(0).toUpperCase() + planet.slice(1)}
            <span className="dt-bar__tier" style={{ fontSize: compact ? 9 : 10 }}>
              {compact ? TIER_SHORT[tier] : TIER_LABEL[tier]}
            </span>
          </span>
        </div>
        <div className="dt-bar__remaining" style={{ fontSize: compact ? 10.5 : 11.5 }}>
          <strong>{rem.val} {rem.unit}</strong> remaining · of {formatTotal(totalDays)}
        </div>
      </div>
      <div className="dt-bar__track" style={{ height: compact ? 18 : 26 }}>
        <div
          className="dt-bar__fill"
          style={{ width: `${filled}%`, background: planetColorCss, color: planetColorCss }}
        />
        {!compact && (
          <>
            <span className="dt-bar__tick" style={{ left: '25%' }} />
            <span className="dt-bar__tick" style={{ left: '50%' }} />
            <span className="dt-bar__tick" style={{ left: '75%' }} />
          </>
        )}
      </div>
      {!compact && (
        <div className="dt-bar__label-strip">
          <span>{startedLabel}</span>
          <span>{filled.toFixed(1)}% elapsed · {Math.round(elapsedDays)} d / {totalDays} d</span>
          <span>{endsLabel}</span>
        </div>
      )}
    </div>
  );
}

/**
 * DashaTimeline
 *
 * props
 *   dasha {
 *     mahadasha:  { planet, elapsedDays, totalDays, startedLabel?, endsLabel? },
 *     antardasha: { planet, elapsedDays, totalDays, ... },
 *     pratyantar: { planet, elapsedDays, totalDays, ... } | null
 *   }
 *   transition {
 *     from: planet, to: planet, tier: 'mahadasha'|'antardasha'|'pratyantar',
 *     daysUntil: number
 *   }
 *   anchorLabel  {string?}  e.g. "Anchor 24 May 2026 · 09:42 IST"
 *   compact      {boolean?} mobile-tight density
 */
export default function DashaTimeline({ dasha, transition, anchorLabel, compact = false }) {
  if (!dasha) return null;

  return (
    <div className="wr-panel">
      <div className="wr-panel__head">
        <div>
          <h3 className="wr-panel__title">Dasha Timeline</h3>
          <div className="wr-panel__sub" style={{ marginTop: 4 }}>Vimshottari · current cycle</div>
        </div>
        {anchorLabel && <div className="wr-panel__sub">{anchorLabel}</div>}
      </div>

      <div className="dt-stack">
        {dasha.mahadasha && <Bar tier="mahadasha" {...dasha.mahadasha} compact={compact} />}
        {dasha.antardasha && <Bar tier="antardasha" {...dasha.antardasha} compact={compact} />}
        {dasha.pratyantar && <Bar tier="pratyantar" {...dasha.pratyantar} compact={compact} />}
      </div>

      {transition && (
        <div
          className="dt-transition"
          style={{ borderLeftColor: planetColor(transition.from) }}
        >
          <div>
            <div
              className="dt-transition__label"
              style={{ color: planetColor(transition.from) }}
            >
              Next change
            </div>
            <div className="dt-transition__body">
              <span className="from" style={{ color: planetColor(transition.from) }}>
                {transition.from.charAt(0).toUpperCase() + transition.from.slice(1)}
              </span>
              {' → '}
              <span className="to" style={{ color: planetColor(transition.to) }}>
                {transition.to.charAt(0).toUpperCase() + transition.to.slice(1)}
              </span>
              {' · '}
              {TIER_LABEL[transition.tier]}
            </div>
          </div>
          <div
            className="dt-transition__count"
            style={{ color: planetColor(transition.from) }}
          >
            {transition.daysUntil}
            <small>days</small>
          </div>
        </div>
      )}
    </div>
  );
}
