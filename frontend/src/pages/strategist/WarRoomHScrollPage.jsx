// ─────────────────────────────────────────────────────────────────────────────
// WarRoomHScrollPage.jsx
// STR-CD-WRS · War Room Horizontal Snap-Scroll
// Route: /strategist/war-room
//
// Canvas: Codex Commission (6)/Phase 2 Commission/STR-CD-WRS · WarRoomHScroll.html
// Full-viewport true snap -- one layer per screen.
// 5 panels: L1 Conquest Score · L2 Missions · L3 Diagnostics · L4 Scoreboard · L5 Timeline
// Sticky Gate 0 header · bottom dot/arrow nav · 4 theme modes.
//
// Data: /api/strategist/dashboard · /api/strategist/gate0/status · /api/strategist/missions
// Theme: StrategistThemeProvider (light/dark/cr-ambient/cr-tactical)
// ─────────────────────────────────────────────────────────────────────────────

import React, {
  useState, useEffect, useRef, useCallback,
} from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { PremiumGateCard } from '../../components/PremiumRoute';
import StrategistThemeProvider, { useStrategistTheme } from '../../components/strategist/StrategistThemeProvider';
import { StrategistThemeToggle } from '../../components/strategist/StrategistThemeToggle';
import { SEO } from '../../components/SEO';
import '../../styles/strategist-tokens.css';
import '../../styles/war-room-hscroll.css';

const BACKEND = process.env.REACT_APP_BACKEND_URL || '';
const GOLDEN_BUFFER_MS = 30 * 60 * 1000; // 30 min before sunset
const PANEL_STORAGE_KEY = 'str-wrs.panel';

// ─────────────────────────────────────────────────────────────────────────────
// Utility: planet abbreviation → CSS class  (e.g. "Saturn" → "wrs-dp-sat")
// ─────────────────────────────────────────────────────────────────────────────
const PLANET_DP_CLASS = {
  Sun: 'wrs-dp-sun', Moon: 'wrs-dp-moon', Mars: 'wrs-dp-mars',
  Mercury: 'wrs-dp-merc', Jupiter: 'wrs-dp-jup', Venus: 'wrs-dp-ven',
  Saturn: 'wrs-dp-sat', Rahu: 'wrs-dp-rahu', Ketu: 'wrs-dp-ketu',
};

const PLANET_MISSION_CLASS = {
  Sun: 'wrs-m-sun', Moon: 'wrs-m-moon', Mars: 'wrs-m-mars',
  Mercury: 'wrs-m-merc', Jupiter: 'wrs-m-jup', Venus: 'wrs-m-ven',
  Saturn: 'wrs-m-sat', Rahu: 'wrs-m-rahu', Ketu: 'wrs-m-ketu',
};

const PLANET_ABBR = {
  Sun: 'Su', Moon: 'Mo', Mars: 'Ma', Mercury: 'Me',
  Jupiter: 'Ju', Venus: 'Ve', Saturn: 'Sa', Rahu: 'Ra', Ketu: 'Ke',
};

function planetDpClass(name) {
  if (!name) return 'wrs-dp-sat';
  const key = Object.keys(PLANET_DP_CLASS).find(
    (k) => name.toLowerCase().includes(k.toLowerCase()),
  );
  return PLANET_DP_CLASS[key] || 'wrs-dp-jup';
}

function planetMissionClass(name) {
  if (!name) return 'wrs-m-sun';
  const key = Object.keys(PLANET_MISSION_CLASS).find(
    (k) => name.toLowerCase().includes(k.toLowerCase()),
  );
  return PLANET_MISSION_CLASS[key] || 'wrs-m-sun';
}

function planetAbbr(name) {
  if (!name) return '?';
  const key = Object.keys(PLANET_ABBR).find(
    (k) => name.toLowerCase().includes(k.toLowerCase()),
  );
  return PLANET_ABBR[key] || name.slice(0, 2);
}

// ─────────────────────────────────────────────────────────────────────────────
// computeGoldenData: derives golden hour display data from sunset ISO string
// ─────────────────────────────────────────────────────────────────────────────
function computeGoldenData(sunsetIso) {
  if (!sunsetIso) return null;
  const sunset = new Date(sunsetIso).getTime();
  if (Number.isNaN(sunset)) return null;

  const now = Date.now();
  const goldenStart = sunset - GOLDEN_BUFFER_MS;

  // Formatted window / sunset strings
  const fmt = (ts) => new Date(ts).toLocaleTimeString('en-IN', {
    hour: '2-digit', minute: '2-digit', hour12: false, timeZone: 'Asia/Kolkata',
  });
  const windowStr = `${fmt(goldenStart)} - ${fmt(sunset)} IST`;
  const sunsetStr = `${fmt(sunset)} IST`;

  let warState = 'offensive';
  let minsToOpen = null;

  if (now < goldenStart) {
    warState = 'offensive';
    minsToOpen = Math.round((goldenStart - now) / 60000);
  } else if (now <= sunset) {
    warState = 'golden';
    minsToOpen = Math.round((sunset - now) / 60000);
  } else {
    warState = 'defensive';
    minsToOpen = 0;
  }

  return { warState, minsToOpen, windowStr, sunsetStr };
}

// ─────────────────────────────────────────────────────────────────────────────
// shapeDasha: maps dashboard dasha fields → display shape for Panel 5
// ─────────────────────────────────────────────────────────────────────────────
function shapeDasha(dashboard) {
  if (!dashboard?.current_mahadasha) return null;

  const today = Date.now();

  function pct(startStr, endStr) {
    if (!startStr || !endStr) return 0;
    const s = new Date(startStr).getTime();
    const e = new Date(endStr).getTime();
    if (Number.isNaN(s) || Number.isNaN(e) || e <= s) return 0;
    return Math.min(100, Math.max(0, Math.round(((today - s) / (e - s)) * 100)));
  }

  function fmt(str) {
    if (!str) return '';
    const d = new Date(str);
    return Number.isNaN(d.getTime())
      ? ''
      : d.toLocaleDateString('en-IN', { month: 'short', year: 'numeric' });
  }

  return {
    maha: {
      planet: dashboard.current_mahadasha,
      abbr: planetAbbr(dashboard.current_mahadasha),
      dpClass: planetDpClass(dashboard.current_mahadasha),
      pct: pct(dashboard.current_mahadasha_start, dashboard.current_mahadasha_end),
      endsLabel: fmt(dashboard.current_mahadasha_end),
    },
    antar: dashboard.current_antardasha
      ? {
          planet: dashboard.current_antardasha,
          abbr: planetAbbr(dashboard.current_antardasha),
          dpClass: planetDpClass(dashboard.current_antardasha),
          pct: pct(dashboard.current_antardasha_start, dashboard.current_antardasha_end),
          endsLabel: fmt(dashboard.current_antardasha_end),
        }
      : null,
    egressLabel: dashboard.current_mahadasha_end
      ? `Transition · ${dashboard.current_mahadasha} → ${
          dashboard.next_mahadasha || '...'
        } · ${fmt(dashboard.current_mahadasha_end)}`
      : null,
  };
}

// ─────────────────────────────────────────────────────────────────────────────
// normalizeGates: same adapter as StrategistWarRoomPage & StrategistActionPlanPage
// ─────────────────────────────────────────────────────────────────────────────
const STATUS_MAP = {
  CLEAR: 'clear', ACTIVE: 'active', WARNING: 'warning', DORMANT: 'dormant',
  CONFLICT: 'warning', UNKNOWN: 'clear',
};
const GATE_META = {
  1: { name: 'Karmic Debt · Pitru Rin',   desc: 'Ancestral ledger scan' },
  2: { name: 'House Awakening',            desc: 'Active house this cycle' },
  3: { name: 'Year Cycle Planet',          desc: 'Year-lord influence' },
  4: { name: 'Mercury Scan',               desc: 'Service-debt flag' },
  5: { name: 'Geographical Alignment',     desc: 'Office vs power direction' },
};

function normalizeGates(rawGates) {
  if (!Array.isArray(rawGates) || rawGates.length === 0) return [];
  return rawGates.map((g) => {
    const meta = GATE_META[g.gate] || { name: g.name || `Gate ${g.gate}`, desc: g.narrative || '' };
    const status = STATUS_MAP[g.status] || 'clear';
    const chipMap = {
      active: 'Active', warning: 'Flagged', dormant: 'Dormant', clear: 'Favourable',
    };
    return {
      n: `Gate ${g.gate}`,
      name: g.name || meta.name,
      desc: g.narrative || meta.desc,
      status,
      chip: chipMap[status] || 'Clear',
    };
  });
}

// ─────────────────────────────────────────────────────────────────────────────
// normalizeMissions: maps /api/strategist/missions → canvas SEEKER.missions shape
// ─────────────────────────────────────────────────────────────────────────────
function normalizeMissions(rawMissions) {
  if (!Array.isArray(rawMissions) || rawMissions.length === 0) return [];
  return rawMissions.map((m) => {
    const planet = m.trigger_planet || m.planet || 'Sun';
    return {
      cls: planetMissionClass(planet),
      planet: m.trigger_planet_house
        ? `${planet} · ${m.trigger_planet_house}`
        : planet,
      name: m.mission_name || m.name || 'Active Mission',
      obj: m.objective || m.description || '',
      pivot: m.pivot_action || m.pivot || '',
      kpi: m.kpi_target || m.kpi || '',
      rem: m.lk_remedy_ref || m.remedy_ref || '',
    };
  });
}

// ─────────────────────────────────────────────────────────────────────────────
// SVG Gauge component
// ─────────────────────────────────────────────────────────────────────────────
const CIRC = 628.3;
const VIEW = 240;
const RADIUS = 100;

function WrsGauge({ score, max, tier }) {
  const s = Math.max(0, Math.min(max, score));
  const offset = CIRC * (1 - s / max);
  return (
    <div className="wrs-gauge" aria-hidden="true">
      <svg viewBox={`0 0 ${VIEW} ${VIEW}`}>
        <circle className="wrs-gauge__track" cx={VIEW / 2} cy={VIEW / 2} r={RADIUS} strokeDasharray={CIRC} strokeDashoffset="0" />
        <circle className="wrs-gauge__fill" cx={VIEW / 2} cy={VIEW / 2} r={RADIUS} strokeDasharray={CIRC} strokeDashoffset={offset} />
      </svg>
      <div className="wrs-gauge__center">
        <div className="wrs-gauge__score">{s}</div>
        <div className="wrs-gauge__max">/ {max}</div>
        {tier && <div className="wrs-gauge__tier">{tier}</div>}
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// Layer head
// ─────────────────────────────────────────────────────────────────────────────
function WrsLayerHead({ n, title, sub }) {
  return (
    <div className="wrs-layer-head">
      <span className="wrs-layer-head__n">{n}</span>
      <h2 className="wrs-layer-head__title">{title}</h2>
      {sub && <p className="wrs-layer-head__sub">{sub}</p>}
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// Verdict chip
// ─────────────────────────────────────────────────────────────────────────────
function WrsVerdictChip({ type, active }) {
  const t = (type || 'wait').toLowerCase();
  return (
    <span className={`wrs-verdict-chip wrs-verdict-chip--${t} ${active ? 'wrs-verdict-chip--active' : ''}`}>
      {t === 'pray'
        ? <span aria-hidden="true">◆</span>
        : <span className="wrs-verdict-chip__pip" />}
      {t.charAt(0).toUpperCase() + t.slice(1)}
    </span>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// PANEL 1 · Conquest Score
// ─────────────────────────────────────────────────────────────────────────────
function PanelConquest({ data }) {
  if (!data) return null;

  const { score, max, tier, warState, verdict, karmicCleared, streak, kpGate0 } = data;

  const stateSegs = [
    { k: 'offensive', cls: 'wrs-state-seg--off',  label: 'Offensive',   sub: 'press the attack' },
    { k: 'golden',    cls: 'wrs-state-seg--gold',  label: 'Golden Hour', sub: 'ritual window' },
    { k: 'defensive', cls: 'wrs-state-seg--def',   label: 'Defensive',   sub: 'hold the fortress' },
  ];

  return (
    <div className="wrs-inner">
      <WrsLayerHead n="L1" title="Conquest Score" sub="Your live success probability and the posture it commands." />
      <div className="wrs-conquest">
        <WrsGauge score={score} max={max || 99} tier={tier} />
        <div className="wrs-conquest__right">
          <div className="wrs-state-banner">
            {stateSegs.map((st) => (
              <div
                key={st.k}
                className={`wrs-state-seg ${st.cls} ${warState === st.k ? 'wrs-state-seg--on' : ''}`}
                aria-current={warState === st.k}
              >
                <div className="wrs-state-seg__k">{st.label}</div>
                <div className="wrs-state-seg__s">{st.sub}</div>
              </div>
            ))}
          </div>
          <div className="wrs-card wrs-conquest-rows">
            <div className="wrs-crow">
              <div className="wrs-crow__l">Rank</div>
              <div className="wrs-crow__b">
                <strong>{tier || '--'}</strong>
              </div>
              <div className="wrs-crow__a">conquest score</div>
            </div>
            <div className="wrs-crow">
              <div className="wrs-crow__l">Karmic</div>
              <div className="wrs-crow__b">
                {karmicCleared
                  ? <span className="wrs-karmic-chip">Cleared</span>
                  : <span style={{ color: '#E3A341' }}>Active</span>}
                {karmicCleared && <em>&nbsp;ledger balanced · gates open</em>}
              </div>
              <div className="wrs-crow__a">Gate 1</div>
            </div>
            <div className="wrs-crow">
              <div className="wrs-crow__l">Verdict</div>
              <div className="wrs-crow__b">
                <WrsVerdictChip type={verdict || 'wait'} active />
              </div>
              <div className="wrs-crow__a">
                {kpGate0?.daysAgo != null ? `Gate 0 · ${kpGate0.daysAgo}d ago` : 'Gate 0'}
              </div>
            </div>
            {streak && (
              <div className="wrs-crow">
                <div className="wrs-crow__l">Streak</div>
                <div className="wrs-crow__b"><strong>{streak.days}</strong> <em>days</em></div>
                <div className="wrs-crow__a">{streak.tier || '--'}</div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// PANEL 2 · Missions
// ─────────────────────────────────────────────────────────────────────────────
function PanelMissions({ missions }) {
  const activeMission = missions?.[0];

  return (
    <div className="wrs-inner">
      <WrsLayerHead n="L2" title="Missions" sub="Transit-triggered moves -- each with a pivot and a measurable target." />
      {activeMission && (
        <div className="wrs-ticker">
          <span className="wrs-ticker__live" aria-hidden="true" />
          <span className="wrs-ticker__tag">Active</span>
          <span className="wrs-ticker__text">
            <b>{activeMission.name}</b>
            {activeMission.obj ? ` -- ${activeMission.obj}` : ''}
          </span>
        </div>
      )}
      {missions && missions.length > 0 ? (
        <div className="wrs-missions">
          {missions.map((m) => (
            <article key={m.name} className={`wrs-mission ${m.cls}`}>
              <div className="wrs-mission__top">
                <h3 className="wrs-mission__name">{m.name}</h3>
                <span className="wrs-mission__planet">{m.planet}</span>
              </div>
              {m.obj && (
                <div className="wrs-mission__row">
                  <span className="wrs-mission__k">Objective</span>
                  <span className="wrs-mission__v">{m.obj}</span>
                </div>
              )}
              {m.pivot && (
                <div className="wrs-mission__row">
                  <span className="wrs-mission__k">Pivot</span>
                  <span className="wrs-mission__v">{m.pivot}</span>
                </div>
              )}
              {m.kpi && (
                <div className="wrs-mission__row">
                  <span className="wrs-mission__k">KPI</span>
                  <span className="wrs-mission__v">
                    <span className="wrs-mono">{m.kpi}</span>
                  </span>
                </div>
              )}
              {m.rem && (
                <div className="wrs-mission__foot">
                  <span className="wrs-mission__rem">remedy · <b>{m.rem}</b></span>
                </div>
              )}
            </article>
          ))}
        </div>
      ) : (
        <div className="wrs-no-missions">
          Missions load once Gate 0 is cleared and the LK engine has your profile.
          <Link to="/strategist/war-room" style={{ color: 'var(--gold)', marginTop: 8, display: 'block' }}>
            Consult Gate 0 →
          </Link>
        </div>
      )}
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// PANEL 3 · Diagnostics
// ─────────────────────────────────────────────────────────────────────────────
function PanelDiagnostics({ gates, pitruActive }) {
  const chipCls = {
    active: 'wrs-status-chip--active',
    warning: 'wrs-status-chip--warning',
    dormant: 'wrs-status-chip--dormant',
    clear: 'wrs-status-chip--clear',
  };

  return (
    <div className="wrs-inner">
      <WrsLayerHead n="L3" title="Diagnostics" sub="The five Lal Kitab gates that bend your probability." />
      {pitruActive && (
        <div className="wrs-debt-strip">
          <span className="wrs-debt-strip__l">Pitru Rin · ancestral debt</span>
          <span className="wrs-debt-strip__v">
            Active at Gate 1 -- costing <b>−20</b> to Conquest.
          </span>
        </div>
      )}
      {gates && gates.length > 0 ? (
        <div className="wrs-gates">
          {gates.map((g) => (
            <div key={g.n} className="wrs-gate">
              <span className="wrs-gate__n">{g.n}</span>
              <div className="wrs-gate__body">
                <div className="wrs-gate__name">{g.name}</div>
                <div className="wrs-gate__desc">{g.desc}</div>
              </div>
              <span className={`wrs-status-chip ${chipCls[g.status] || 'wrs-status-chip--clear'}`}>
                {g.chip}
              </span>
            </div>
          ))}
        </div>
      ) : (
        <div className="wrs-no-missions">
          Complete LK onboarding to activate gate diagnostics.
        </div>
      )}
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// PANEL 4 · Scoreboard
// ─────────────────────────────────────────────────────────────────────────────
function PanelScoreboard({ scoreboard, score }) {
  const sb = scoreboard || {};
  const currentScore = score || sb.conquest_score || 0;

  const bands = [
    { cls: 'wrs-band--sov',  r: '85-99', s: 'Sovereign', t: 'Expansion / All-In',      min: 85 },
    { cls: 'wrs-band--fri',  r: '60-84', s: 'Friction',  t: 'Patch & Pivot',            min: 60 },
    { cls: 'wrs-band--sie',  r: '40-59', s: 'Siege',     t: 'Hold Ground / Remedy',     min: 40 },
    { cls: 'wrs-band--lock', r: '0-39',  s: 'Lockdown',  t: 'Withdraw / Reset',          min: 0 },
  ];

  const activeBand = bands.find((b, i) => {
    const next = bands[i + 1];
    return currentScore >= b.min && (next ? currentScore < next.min + (bands[i].min - next.min) : true);
  }) || bands.find((b) => currentScore >= b.min);

  return (
    <div className="wrs-inner">
      <WrsLayerHead n="L4" title="Scoreboard" sub="Streaks, discipline, debt cleared -- and where today's score lands." />
      <div className="wrs-board">
        <div className="wrs-stat">
          <div className="wrs-stat__l">Ritual streak</div>
          <div className="wrs-stat__v">{sb.streak_days ?? '--'}<small> days</small></div>
          <div className="wrs-stat__sub"><b>{sb.streak_tier || '--'}</b></div>
        </div>
        <div className="wrs-stat">
          <div className="wrs-stat__l">Conquest score</div>
          <div className="wrs-stat__v">{currentScore}<small> / 99</small></div>
          <div className="wrs-stat__sub">{sb.score_tier || '--'}</div>
        </div>
        <div className="wrs-stat">
          <div className="wrs-stat__l">Karmic debt</div>
          <div className="wrs-stat__v" style={{ fontSize: 20 }}>
            {sb.karmic_debt_cleared ? 'Cleared' : 'Active'}
          </div>
          <div className="wrs-stat__sub">Gate 1 status</div>
        </div>
      </div>
      <div className="wrs-bands">
        {bands.map((b) => {
          const isNow = activeBand?.s === b.s;
          return (
            <div key={b.s} className={`wrs-band ${b.cls} ${isNow ? 'wrs-band--on' : ''}`}>
              <span className="wrs-band__r">{b.r}</span>
              <span>
                <span className="wrs-band__s">{b.s}</span>
                {' '}
                <span className="wrs-band__t">· {b.t}</span>
              </span>
              {isNow
                ? <span className="wrs-band__now">◂ you · {currentScore}</span>
                : <span />}
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// PANEL 5 · Timeline
// ─────────────────────────────────────────────────────────────────────────────
function PanelTimeline({ dasha, golden }) {
  return (
    <div className="wrs-inner">
      <WrsLayerHead n="L5" title="Timeline" sub="The dasha clock and the day's ritual window." />
      <div className="wrs-tl-grid">
        {/* Dasha column */}
        <div className="wrs-dasha">
          {dasha?.maha ? (
            <div className={`wrs-dasha-chip ${dasha.maha.dpClass}`}>
              <span className="wrs-dasha-chip__planet">{dasha.maha.abbr}</span>
              <div>
                <div className="wrs-dasha-chip__k">Mahadasha</div>
                <div className="wrs-dasha-chip__v">{dasha.maha.planet}</div>
                <div className="wrs-timing-bar">
                  <div className="wrs-timing-bar__fill" style={{ width: `${dasha.maha.pct}%` }} />
                </div>
              </div>
              <div className="wrs-dasha-chip__pct">
                <b>{dasha.maha.pct}%</b><br />elapsed
              </div>
            </div>
          ) : (
            <div className="wrs-no-missions" style={{ minHeight: 80 }}>
              Dasha data loads after birth chart setup.
            </div>
          )}
          {dasha?.antar && (
            <div className={`wrs-dasha-chip ${dasha.antar.dpClass}`}>
              <span className="wrs-dasha-chip__planet">{dasha.antar.abbr}</span>
              <div>
                <div className="wrs-dasha-chip__k">Antardasha</div>
                <div className="wrs-dasha-chip__v">{dasha.antar.planet}</div>
                <div className="wrs-timing-bar">
                  <div className="wrs-timing-bar__fill" style={{ width: `${dasha.antar.pct}%` }} />
                </div>
              </div>
              <div className="wrs-dasha-chip__pct">
                <b>{dasha.antar.pct}%</b><br />elapsed
              </div>
            </div>
          )}
          {dasha?.egressLabel && (
            <div className="wrs-dasha-egress">{dasha.egressLabel}</div>
          )}
        </div>

        {/* Golden Hour column */}
        <div className="wrs-golden">
          <div className="wrs-golden__top">
            <span className="wrs-golden__glyph" aria-hidden="true" />
            <span className="wrs-golden__title">Golden Hour</span>
          </div>
          {golden ? (
            <>
              <div className="wrs-golden__count">
                {golden.warState === 'golden'
                  ? <>{golden.minsToOpen}<small> min remaining</small></>
                  : golden.warState === 'defensive'
                    ? <span style={{ fontSize: 20 }}>After sunset</span>
                    : <>{golden.minsToOpen}<small> min to open</small></>}
              </div>
              <p className="wrs-golden__sub">
                The ritual window opens 30 minutes before sunset. Remedies performed inside it carry the most weight.
              </p>
              <div className="wrs-golden__win">
                <span>window</span>
                <span><b>{golden.windowStr}</b></span>
              </div>
              <div className="wrs-golden__win">
                <span>sunset</span>
                <span><b>{golden.sunsetStr}</b></span>
              </div>
            </>
          ) : (
            <p className="wrs-golden__sub" style={{ marginTop: 8 }}>
              Golden Hour data loads from the Panchang engine. Ensure your location is set.
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// Panel registry
// ─────────────────────────────────────────────────────────────────────────────
const PANELS = [
  { id: 'conquest',    label: 'Conquest Score' },
  { id: 'missions',    label: 'Missions' },
  { id: 'diagnostics', label: 'Diagnostics' },
  { id: 'scoreboard',  label: 'Scoreboard' },
  { id: 'timeline',    label: 'Timeline' },
];

// ─────────────────────────────────────────────────────────────────────────────
// WarRoomShell -- the full H-scroll layout with real data
// ─────────────────────────────────────────────────────────────────────────────
function WarRoomShell({ dashboard, gate0Status, missions, loading }) {
  const { mode } = useStrategistTheme();
  const scrollerRef = useRef(null);
  const idxRef = useRef(0);

  const [idx, setIdx] = useState(() => {
    try {
      const n = parseInt(localStorage.getItem(PANEL_STORAGE_KEY), 10);
      return Number.isFinite(n) && n >= 0 && n < PANELS.length ? n : 0;
    } catch {
      return 0;
    }
  });

  idxRef.current = idx;

  // ── Scroll helpers (nav bug fix from canvas: smooth attempt + guaranteed fallback) ──
  const setScrollInstant = useCallback((sc, left) => {
    const prev = sc.style.scrollBehavior;
    sc.style.scrollBehavior = 'auto';
    sc.scrollLeft = left;
    sc.style.scrollBehavior = prev;
  }, []);

  const goTo = useCallback((n) => {
    const clamped = Math.max(0, Math.min(PANELS.length - 1, n));
    const sc = scrollerRef.current;
    if (sc) {
      const target = clamped * sc.clientWidth;
      try { sc.scrollTo({ left: target, behavior: 'smooth' }); } catch (e) { setScrollInstant(sc, target); }
      clearTimeout(sc.__goT);
      sc.__goT = setTimeout(() => {
        if (Math.abs(sc.scrollLeft - target) > 4) setScrollInstant(sc, target);
      }, 440);
    }
    setIdx(clamped);
  }, [setScrollInstant]);

  // Restore saved panel on mount (instant, no animation)
  useEffect(() => {
    const sc = scrollerRef.current;
    if (sc && idx > 0) setScrollInstant(sc, idx * sc.clientWidth);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Persist active panel
  useEffect(() => {
    try { localStorage.setItem(PANEL_STORAGE_KEY, String(idx)); } catch { /* ignore */ }
  }, [idx]);

  // Re-align on resize
  useEffect(() => {
    const onResize = () => {
      const sc = scrollerRef.current;
      if (sc) setScrollInstant(sc, idxRef.current * sc.clientWidth);
    };
    window.addEventListener('resize', onResize);
    return () => window.removeEventListener('resize', onResize);
  }, [setScrollInstant]);

  // Sync dot to manual swipe
  const onScroll = useCallback(() => {
    const sc = scrollerRef.current;
    if (!sc) return;
    const n = Math.round(sc.scrollLeft / sc.clientWidth);
    if (n !== idxRef.current) setIdx(n);
  }, []);

  // Keyboard arrow nav
  useEffect(() => {
    const onKey = (e) => {
      if (e.target && /^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName)) return;
      if (e.key === 'ArrowRight') { e.preventDefault(); goTo(idxRef.current + 1); }
      else if (e.key === 'ArrowLeft') { e.preventDefault(); goTo(idxRef.current - 1); }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [goTo]);

  // ── Derived display data ──────────────────────────────────────────────────
  const conquest = dashboard?.conquest_probability || {};
  const scoreboard = dashboard?.scoreboard || {};
  const gates = normalizeGates(dashboard?.gate_summaries ?? []);
  const dashaData = shapeDasha(dashboard);
  const goldenData = dashboard?.sunset_iso ? computeGoldenData(dashboard.sunset_iso) : null;
  const normalizedMissions = normalizeMissions(missions);
  const pitruActive = Boolean(dashboard?.diagnosis_summary?.pitru_rin_active);
  const verdict = (scoreboard.gate0_last_verdict || gate0Status?.last_verdict || '').toLowerCase();
  const karmicCleared = scoreboard.karmic_debt_cleared ?? false;

  const kpGate0 = {
    question: gate0Status?.last_question || scoreboard.gate0_last_question || 'No consultation on record.',
    verdict: verdict,
    daysAgo: scoreboard.gate0_days_since ?? gate0Status?.days_since ?? null,
  };

  const conquestPanelData = {
    score: Number(conquest.score) || 0,
    max: Number(conquest.max) || 99,
    tier: scoreboard.score_tier || conquest.tier || '--',
    warState: goldenData?.warState || 'offensive',
    verdict,
    karmicCleared,
    streak: scoreboard.streak_days != null
      ? { days: scoreboard.streak_days, tier: scoreboard.streak_tier }
      : null,
    kpGate0,
  };

  return (
    <div className="wrs-shell" data-mode={mode} style={{ height: '100%' }}>
      {/* Top bar */}
      <div className="wrs-topbar">
        <Link to="/strategist/snapshot" className="wrs-topbar__back">← Overview</Link>
        <span className="wrs-topbar__title">
          <b>War Room</b> · Strategist
        </span>
        <div className="wrs-topbar__right">
          <StrategistThemeToggle size="sm" />
        </div>
      </div>

      {/* Sticky Gate 0 */}
      <div className="wrs-gate0">
        <div className="wrs-gate0__id">
          <span className="wrs-gate0__eyebrow">Gate 0 · Krishna Prashnavali</span>
          <span className="wrs-gate0__q">"{kpGate0.question}"</span>
        </div>
        <WrsVerdictChip type={verdict || 'wait'} active />
        <div className="wrs-gate0__meta">
          <div className="wrs-gate0__days">
            consulted<br />
            <b>{kpGate0.daysAgo != null ? `${kpGate0.daysAgo} days ago` : '--'}</b>
          </div>
          <Link to="/krishna-prashnavali" className="wrs-gate0__cta">Re-consult Gate 0</Link>
        </div>
      </div>

      {/* Horizontal snap scroller */}
      {loading ? (
        <div className="wrs-loading">
          <div className="wrs-loading__dot" />
          Calibrating War Room...
        </div>
      ) : (
        <div
          className="wrs-scroller"
          ref={scrollerRef}
          onScroll={onScroll}
          tabIndex={-1}
          aria-label="War Room layers"
        >
          <section className="wrs-panel" aria-label="Conquest Score">
            <PanelConquest data={conquestPanelData} />
          </section>
          <section className="wrs-panel" aria-label="Missions">
            <PanelMissions missions={normalizedMissions} />
          </section>
          <section className="wrs-panel" aria-label="Diagnostics">
            <PanelDiagnostics gates={gates} pitruActive={pitruActive} />
          </section>
          <section className="wrs-panel" aria-label="Scoreboard">
            <PanelScoreboard scoreboard={scoreboard} score={Number(conquest.score) || 0} />
          </section>
          <section className="wrs-panel" aria-label="Timeline">
            <PanelTimeline dasha={dashaData} golden={goldenData} />
          </section>
        </div>
      )}

      {/* Bottom nav */}
      <div className="wrs-nav">
        <div className="wrs-nav__label">
          Layer <b>{idx + 1}</b> / {PANELS.length} · <b>{PANELS[idx].label}</b>
        </div>
        <div className="wrs-nav__dots" role="tablist" aria-label="Layer indicator">
          {PANELS.map((P, i) => (
            <button
              key={P.id}
              type="button"
              role="tab"
              aria-selected={i === idx}
              aria-label={P.label}
              className={`wrs-dot ${i === idx ? 'wrs-dot--on' : ''}`}
              onClick={() => goTo(i)}
            />
          ))}
        </div>
        <div className="wrs-nav__arrows">
          <button
            type="button"
            className="wrs-arrow"
            onClick={() => goTo(idx - 1)}
            disabled={idx === 0}
            aria-label="Previous layer"
          >
            <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="10,3 5,8 10,13" />
            </svg>
          </button>
          <button
            type="button"
            className="wrs-arrow"
            onClick={() => goTo(idx + 1)}
            disabled={idx === PANELS.length - 1}
            aria-label="Next layer"
          >
            <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="6,3 11,8 6,13" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// Data-fetching wrapper
// ─────────────────────────────────────────────────────────────────────────────
function WarRoomHScrollInner() {
  const { user, loading: authLoading } = useAuth();
  const navigate = useNavigate();

  const [loading, setLoading] = useState(true);
  const [dashboard, setDashboard] = useState(null);
  const [gate0Status, setGate0Status] = useState(null);
  const [missions, setMissions] = useState([]);

  useEffect(() => {
    if (authLoading) return;
    if (!user) { navigate('/login', { state: { from: { pathname: '/strategist/war-room' } } }); return; }

    // Persist any draft birth data (same pattern as StrategistPage)
    async function persistDraftIfNeeded() {
      try {
        const draft = JSON.parse(localStorage.getItem('strategist-profile-draft') || 'null');
        if (draft?.dob) {
          await fetch(`${BACKEND}/api/strategist/profile`, {
            method: 'POST',
            credentials: 'include',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ dob: draft.dob, tob: draft.tob || '', city: draft.city || '' }),
          });
        }
      } catch { /* best-effort */ }
    }

    async function loadAll() {
      await persistDraftIfNeeded();

      const [dashRes, gate0Res, missionRes] = await Promise.allSettled([
        fetch(`${BACKEND}/api/strategist/dashboard`, { credentials: 'include' }).then((r) => r.json()),
        fetch(`${BACKEND}/api/strategist/gate0/status`, { credentials: 'include' }).then((r) => r.json()),
        fetch(`${BACKEND}/api/strategist/missions`, { credentials: 'include' }).then((r) => r.json()),
      ]);

      if (dashRes.status === 'fulfilled' && !dashRes.value?.error) {
        setDashboard(dashRes.value);
        // Clear draft once dashboard loads
        try {
          const draft = JSON.parse(localStorage.getItem('strategist-profile-draft') || 'null');
          if (draft?.dob) localStorage.removeItem('strategist-profile-draft');
        } catch { /* ignore */ }
      }
      if (gate0Res.status === 'fulfilled') setGate0Status(gate0Res.value);
      if (missionRes.status === 'fulfilled') {
        const raw = missionRes.value;
        setMissions(Array.isArray(raw) ? raw : (raw?.missions || []));
      }

      setLoading(false);
    }

    loadAll();
  }, [authLoading, user, navigate]);

  if (authLoading) return null;

  if (!user?.is_premium) {
    return (
      <PremiumGateCard
        feature="The Strategist -- War Room"
        description="The horizontal War Room with live Conquest Score, Missions, Diagnostics, Scoreboard, and Timeline is a Premium feature. Upgrade to activate your full war room."
      />
    );
  }

  return (
    <WarRoomShell
      dashboard={dashboard}
      gate0Status={gate0Status}
      missions={missions}
      loading={loading}
    />
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// Default export -- wrapped in StrategistThemeProvider
// ─────────────────────────────────────────────────────────────────────────────
export default function WarRoomHScrollPage() {
  return (
    <StrategistThemeProvider>
      <SEO title="The Strategist -- War Room" noindex />
      {/* Full-viewport layout: override the page container to fill height */}
      <style>{`
        .war-room-fullvp { height: calc(100vh - var(--navbar-height, 64px)); overflow: hidden; }
      `}</style>
      <div className="war-room-fullvp">
        <WarRoomHScrollInner />
      </div>
    </StrategistThemeProvider>
  );
}
