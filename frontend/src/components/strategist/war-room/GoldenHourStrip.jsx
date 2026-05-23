// =============================================================
// STR-R2B Step 3 · GoldenHourStrip
// Brief §4.6 · Layer 5 · canvas ref 02/05 · ART 5.1
// -------------------------------------------------------------
// Horizontal strip of time-window cards. Active window earns NOW pulse
// and live countdown. Day rail below visualises 0-24h chronologically.
// useNow() drives the 1-second tick (R-02 -- real-time becomes real here).
//
// Q-06 retained -- day rail visible.
// Q-07 retained -- NOW pip animates (1.4 s pulse).
// =============================================================

import { planetColor, useNow, parseHM, formatHMS } from './utils';

const TYPE_LABEL = {
  auspicious:   'Auspicious',
  defensive:    'Defensive',
  inauspicious: 'Inauspicious',
};
const TYPE_VERDICT_SUFFIX = {
  auspicious:   'Auspicious',
  defensive:    'Defensive',
  inauspicious: 'Inauspicious · Hold',
};

function asDate(v, ref) {
  if (v instanceof Date) return v;
  if (typeof v === 'string' && /^\d{1,2}:\d{2}$/.test(v)) return parseHM(v, ref);
  return new Date(v);
}

function statusFor(window, now) {
  const start = asDate(window.start, now);
  const end   = asDate(window.end, now);
  if (now < start) return { state: 'upcoming', start, end };
  if (now > end)   return { state: 'complete', start, end };
  return { state: 'active', start, end };
}

function timeRangeLabel(start, end) {
  const fmt = (d) =>
    `${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`;
  return `${fmt(start)} → ${fmt(end)}`;
}

function GoldenHourCard({ window, now }) {
  const { state, start, end } = statusFor(window, now);
  const planet = (window.planet || 'sun').toLowerCase();
  const type = window.type || 'auspicious';
  const verdict =
    state === 'active'   ? `${TYPE_LABEL[type]} · Live` :
    state === 'upcoming' ? `${TYPE_LABEL[type]} · Upcoming` :
                           `${TYPE_LABEL[type]} · Complete`;

  return (
    <article
      className={`gh-card ${state === 'active' ? 'gh-card--active' : ''}`}
      data-type={type}
      data-planet={planet}
    >
      {state === 'active' && <span className="gh-now">Now</span>}

      <span className="gh-card__planet" style={{ color: planetColor(planet) }}>
        <span className="pip" style={{ background: planetColor(planet) }} />
        {planet.charAt(0).toUpperCase() + planet.slice(1)}
      </span>

      <h4 className="gh-card__name">{window.name}</h4>
      <p className="gh-card__time">
        {timeRangeLabel(start, end).split(' → ').map((t, i, arr) => (
          <span key={i}>
            {t}
            {i < arr.length - 1 && <span className="arrow">→</span>}
          </span>
        ))}
      </p>

      {state === 'active' && (
        <div className="gh-card__countdown" aria-live="polite">
          {formatHMS(end - now)}
          <small>Remaining</small>
        </div>
      )}

      <div className="gh-card__type">{verdict}</div>
    </article>
  );
}

// ── Day rail (Q-06) ─────────────────────────────────────────
function DayRail({ windows, now, dateLabel }) {
  const dayStart = new Date(now); dayStart.setHours(0, 0, 0, 0);
  const dayMs = 24 * 60 * 60 * 1000;
  const nowPct = ((now - dayStart) / dayMs) * 100;

  const segments = windows.map((w, i) => {
    const s = asDate(w.start, now);
    const e = asDate(w.end,   now);
    const left  = Math.max(0, ((s - dayStart) / dayMs) * 100);
    const width = Math.max(0.6, ((e - s) / dayMs) * 100);
    return { i, type: w.type || 'auspicious', left, width };
  });

  return (
    <div className="gh-rail">
      <div className="gh-rail__head">
        <div className="gh-rail__title">Day-rail · 00:00 → 24:00 IST</div>
        <div className="gh-rail__date">{dateLabel}</div>
      </div>
      <div className="gh-rail__track">
        {segments.map((s) => (
          <span
            key={s.i}
            className="gh-rail__seg"
            data-type={s.type}
            style={{ left: `${s.left}%`, width: `${s.width}%` }}
          />
        ))}
        <span className="gh-rail__now" style={{ left: `${nowPct}%` }} />
      </div>
      <div className="gh-rail__hours">
        <span>00</span><span>04</span><span>08</span><span>12</span>
        <span>16</span><span>20</span><span>24</span>
      </div>
    </div>
  );
}

/**
 * GoldenHourStrip
 *
 * props
 *   windows[]: { name, planet, start, end, type }
 *     start/end: 'HH:MM' string OR Date OR ISO string
 *     type: 'auspicious' | 'defensive' | 'inauspicious'
 *   locationLabel?: string   e.g. "Mumbai · 19.0760 N · 24 May 2026"
 *   dateLabel?:     string   e.g. "24 May 2026"
 *   showDayRail?:   boolean  (default true -- Q-06)
 *   tickMs?:        number   (default 1000 -- Q-07 + R-02 live data)
 */
export default function GoldenHourStrip({
  windows = [],
  locationLabel,
  dateLabel,
  showDayRail = true,
  tickMs = 1000,
}) {
  const now = useNow(tickMs);

  return (
    <div className="wr-panel">
      <div className="wr-panel__head">
        <div>
          <h3 className="wr-panel__title">Golden Hour · Today</h3>
          {locationLabel && (
            <div className="wr-panel__sub" style={{ marginTop: 4 }}>{locationLabel}</div>
          )}
        </div>
        <div style={{
          display: 'inline-flex', alignItems: 'center', gap: 14,
          fontFamily: 'var(--font-mono)', fontSize: 10,
          letterSpacing: '0.18em', textTransform: 'uppercase',
          color: 'var(--ink-3)',
        }}>
          <span style={{ display: 'inline-flex', alignItems: 'center', gap: 6 }}>
            <i style={{ width: 8, height: 8, borderRadius: '50%', background: 'var(--emerald)' }} />
            Auspicious
          </span>
          <span style={{ display: 'inline-flex', alignItems: 'center', gap: 6 }}>
            <i style={{ width: 8, height: 8, borderRadius: '50%', background: 'var(--amber)' }} />
            Defensive
          </span>
          <span style={{ display: 'inline-flex', alignItems: 'center', gap: 6 }}>
            <i style={{ width: 8, height: 8, borderRadius: '50%', background: 'var(--red)' }} />
            Inauspicious
          </span>
        </div>
      </div>

      <div className="gh-strip">
        {windows.map((w, i) => (
          <GoldenHourCard key={w.id || w.name || i} window={w} now={now} />
        ))}
      </div>

      {showDayRail && <DayRail windows={windows} now={now} dateLabel={dateLabel} />}
    </div>
  );
}
