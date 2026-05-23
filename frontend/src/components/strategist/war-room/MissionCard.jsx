// =============================================================
// STR-R2B Step 3 · MissionCard
// Brief §4.2 · Layer 2 · canvas ref 02/02 · ART 2.1/2.2/2.3
// -------------------------------------------------------------
// SINGLE component, three variants -- "brief" | "module" | "terminal".
// Schema follows §05 of the Step 3 Delivery Plan (engine emit):
//   trigger_condition · strategy · decision_logic
//   pivot_logic · pivot_action · kpi_target
//
// Canvas placeholder keys (trigger / on_hit / fallback / window / aspect)
// are REPLACED -- Temple Team rewrote against the actual strategist_engine.py emit.
//
// Q-04 dynamic pips -- Pratyantar renders only when non-null.
// =============================================================

import { useState } from 'react';
import { planetColor } from './utils';

const PLANETS = ['sun','moon','mars','mercury','jupiter','venus','saturn','rahu','ketu'];
const COMMAND_LABEL = (p) => `${p.charAt(0).toUpperCase() + p.slice(1)} · Command`;

// ── Status / phase chip mapping ──────────────────────────────
const STATUS_CHIP = {
  active:    { tone: 'emerald', label: 'Active',    pip: true },
  completed: { tone: 'muted',   label: 'Completed', pip: true },
  locked:    { tone: 'muted',   label: 'Locked',    pip: true },
};
const PHASE_CHIP = {
  peak: { tone: 'gold',  label: 'Peak'  },
  heat: { tone: 'amber', label: 'Heat'  },
};
const APPROVAL_CHIP = {
  approved:              { tone: 'emerald', label: 'Approved' },
  pending_human_review:  { tone: 'amber',   label: 'Pending Human Review' },
};

// ── Sub-atoms ────────────────────────────────────────────────
function PlanetBadge({ planet }) {
  const p = (planet || 'jupiter').toLowerCase();
  const c = planetColor(p);
  return (
    <span
      className="mc__planet"
      data-planet={p}
      style={{
        color: c,
        borderColor: `color-mix(in srgb, ${c} 45%, transparent)`,
        background: `color-mix(in srgb, ${c} 10%, transparent)`,
      }}
    >
      <span className="mc__planet-dot" style={{ background: c }} />
      {COMMAND_LABEL(p)}
    </span>
  );
}

function Chip({ tone, children, pip }) {
  return (
    <span className={`wr-chip wr-chip--${tone}`}>
      {pip && <span className="wr-chip__pip" />}
      {children}
    </span>
  );
}

// Q-04 dynamic pips -- two when no Pratyantar, three when set
function DashaAlignment({ dasha }) {
  if (!dasha) return null;
  const { mahadasha, antardasha, pratyantar } = dasha;
  const items = [
    { planet: mahadasha,  tier: 'MD' },
    { planet: antardasha, tier: 'AD' },
  ];
  if (pratyantar) items.push({ planet: pratyantar, tier: 'PD' });

  return (
    <div className="mc__dasha">
      <span className="mc__dasha-tag">Calibrated to</span>
      {items.map((it, i) => (
        <span key={i} style={{ display: 'inline-flex', alignItems: 'center', gap: 10 }}>
          {i > 0 && <span className="mc__dasha-sep">·</span>}
          <span className="mc__dasha-planet">
            <span className="pip" style={{ background: planetColor(it.planet) }} />
            {it.planet.charAt(0).toUpperCase() + it.planet.slice(1)} · {it.tier}
          </span>
        </span>
      ))}
    </div>
  );
}

// ── Terminal trigger block (§05 schema) ─────────────────────
function TerminalTrigger({ m }) {
  // Six rows · keys left-aligned, string values right of the key column,
  // comments in --ink-mute. Matches the §05 reference render.
  const rows = [
    { k: 'trigger_condition', v: m.trigger_condition, c: 'string -- maps to TRIGGER_MAP key' },
    { k: 'strategy',          v: m.strategy,          c: 'mission strategy' },
    { k: 'decision_logic',    v: m.decision_logic,    c: 'reasoning behind the call' },
    { k: 'pivot_logic',       v: m.pivot_logic,       c: 'condition that triggers a pivot' },
    { k: 'pivot_action',      v: m.pivot_action,      c: 'what to do when pivot fires' },
    { k: 'kpi_target',        v: m.kpi_target,        c: 'success metric' },
  ];
  return (
    <div className="mc__trigger" role="region" aria-label="Trigger code">
      {rows.map(({ k, v, c }) => (
        <div key={k} className="mc__trigger-row">
          <span className="mc__trigger-k">{k}</span>
          <span>
            <span className="mc__trigger-s">"{v ?? ''}"</span>
            <span className="mc__trigger-c"># {c}</span>
          </span>
        </div>
      ))}
    </div>
  );
}

// ── Main component ──────────────────────────────────────────
/**
 * MissionCard
 *
 * props
 *   mission   {object}   shape in §05 of Step 3 Delivery Plan
 *   variant   {"brief" | "module" | "terminal"}
 *   id        {string?}  number/code shown in the topline (defaults to mission.id)
 *   onAddRemedy {function?}
 */
export default function MissionCard({
  mission,
  variant = 'module',
  id,
  onAddRemedy = () => {},
}) {
  const [decExpanded, setDecExpanded] = useState(false);
  const [pivExpanded, setPivExpanded] = useState(false);

  if (!mission) return null;
  const planet = (mission.command_planet || 'jupiter').toLowerCase();
  const status = STATUS_CHIP[mission.status] || STATUS_CHIP.active;
  const phase  = PHASE_CHIP[mission.phase];
  const approval = APPROVAL_CHIP[mission.approval];

  return (
    <article className={`mc ${variant === 'terminal' ? 'mc--terminal' : ''}`} data-planet={planet}>
      <div className="mc__pad">

        {/* Topline: code · planet badge · status · phase */}
        <div className="mc__topline">
          <span className="mc__num">{id || mission.id}</span>
          <PlanetBadge planet={planet} />
          <Chip tone={status.tone} pip>{status.label}</Chip>
          {phase && <Chip tone={phase.tone}>{phase.label}</Chip>}
          {variant === 'terminal' && (
            <span className="wr-chip wr-chip--muted">Sequence · 04 / 12</span>
          )}
        </div>

        {/* Title + objective */}
        <h4 className="mc__name">{mission.name}</h4>
        {mission.objective && <p className="mc__objective">{mission.objective}</p>}

        {/* ── BRIEF variant: header + objective + KPI only ── */}
        {variant === 'brief' && mission.kpi_target && (
          <div className="mc__kpi">
            <span>KPI</span>
            <strong>{mission.kpi_target}</strong>
          </div>
        )}

        {/* ── MODULE variant: strategy + expandable decision/pivot ── */}
        {variant === 'module' && (
          <>
            <div className="mc__schema">
              {mission.strategy && (
                <div className="mc__field">
                  <div className="mc__field-label">Strategy</div>
                  <div className="mc__field-body">{mission.strategy}</div>
                </div>
              )}

              {mission.decision_logic && (
                <div className="mc__field mc__field--bare">
                  <button
                    type="button"
                    className="mc__toggle"
                    aria-expanded={decExpanded}
                    onClick={() => setDecExpanded(v => !v)}
                  >
                    <span className="car">▸</span>
                    {decExpanded ? 'Hide' : 'Show'} Decision Logic
                  </button>
                  <div className={`mc__exp ${decExpanded ? 'mc__exp--open' : ''}`}>
                    <div className="mc__field-body">{mission.decision_logic}</div>
                  </div>
                </div>
              )}

              {(mission.pivot_logic || mission.pivot_action) && (
                <div className="mc__field mc__field--bare">
                  <button
                    type="button"
                    className="mc__toggle"
                    aria-expanded={pivExpanded}
                    onClick={() => setPivExpanded(v => !v)}
                  >
                    <span className="car">▸</span>
                    {pivExpanded ? 'Hide' : 'Show'} Pivot Logic
                  </button>
                  <div className={`mc__exp ${pivExpanded ? 'mc__exp--open' : ''}`}>
                    {mission.pivot_logic && (
                      <div className="mc__field-body" style={{ marginBottom: 10 }}>
                        {mission.pivot_logic}
                      </div>
                    )}
                    {mission.pivot_action && (
                      <>
                        <div className="mc__field-label" style={{ marginTop: 4 }}>Pivot Action</div>
                        <div className="mc__field-body">{mission.pivot_action}</div>
                      </>
                    )}
                  </div>
                </div>
              )}
            </div>

            {mission.kpi_target && (
              <div className="mc__kpi">
                <span>KPI</span>
                <strong>{mission.kpi_target}</strong>
              </div>
            )}

            <DashaAlignment dasha={mission.dasha_alignment} />

            <div className="mc__foot">
              {approval ? <Chip tone={approval.tone}>{approval.label}</Chip>
                        : <Chip tone="muted">-- No Status --</Chip>}
              <button type="button" className="mc__foot-cta" onClick={onAddRemedy}>
                + Add Remedy to Tracker
              </button>
            </div>
          </>
        )}

        {/* ── TERMINAL variant: all fields visible · §05 schema block ── */}
        {variant === 'terminal' && (
          <>
            <div className="mc__schema">
              <div className="mc__field">
                <div className="mc__field-label">Trigger code · engine emit</div>
                <TerminalTrigger m={mission} />
              </div>

              {mission.strategy && (
                <div className="mc__field">
                  <div className="mc__field-label">Strategy</div>
                  <div className="mc__field-body">{mission.strategy}</div>
                </div>
              )}
              {mission.decision_logic && (
                <div className="mc__field">
                  <div className="mc__field-label">Decision logic</div>
                  <div className="mc__field-body">{mission.decision_logic}</div>
                </div>
              )}
              {mission.pivot_logic && (
                <div className="mc__field">
                  <div className="mc__field-label">Pivot logic</div>
                  <div className="mc__field-body">{mission.pivot_logic}</div>
                </div>
              )}
              {mission.pivot_action && (
                <div className="mc__field">
                  <div className="mc__field-label">Pivot action</div>
                  <div className="mc__field-body">{mission.pivot_action}</div>
                </div>
              )}
            </div>

            {mission.kpi_target && (
              <div className="mc__kpi">
                <span>KPI</span>
                <strong>{mission.kpi_target}</strong>
              </div>
            )}

            <DashaAlignment dasha={mission.dasha_alignment} />

            <div className="mc__foot">
              <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                {approval ? <Chip tone={approval.tone}>{approval.label}</Chip>
                          : <Chip tone="muted">-- No Status --</Chip>}
                {mission.approval_stamp && (
                  <span style={{
                    fontFamily: 'var(--font-mono)',
                    fontSize: 10.5, color: 'var(--ink-3)',
                    letterSpacing: '0.12em',
                  }}>· {mission.approval_stamp}</span>
                )}
              </div>
              <button type="button" className="mc__foot-cta" onClick={onAddRemedy}>
                + Add Remedy to Tracker
              </button>
            </div>
          </>
        )}
      </div>
    </article>
  );
}

// Exposed for the MissionBoard panel toolbar
MissionCard.VARIANTS = ['brief', 'module', 'terminal'];
MissionCard.PLANETS = PLANETS;
