// -----------------------------------------------------------------
// StrategistActionPlanPage.jsx
// Source: STR-2G · StrategistActionPlan.html  (CD delivery)
// Built: 2026-05-29  (STR-OP-13)
//
// 2G composition shell -- assembles five Phase 2 surface modules in
// chart-led order per A1 §5:
//   §01 Digest      ← 2F ConquestScoreboard (compact bar always; detail in briefing)
//   §02 Diagnostics ← 2E LKGateSummaries
//   §03 Verdict     ← 2C OracleVerdictBanners (briefing) / VerdictCompact (command)
//   §04 Active Path ← switch(verdict): 2D (no/wait) · 2I (pray) · ClearanceCard (yes)
//   §05 Action Queue ← new 2G-owned component
//
// ONE page-level density control (Command / Briefing) drives every section.
// Modules render with showToggle=false; their A/B is set by the page density.
//
// KP Gate 0 panel -- standalone, above the sections per TT process map.
// Wires to /api/strategist/dashboard. KP gate fields stub until STR-2A2 lands.
//
// CSS imports: all Phase 2 component CSS + strategist-2g-actionplan.css
// -----------------------------------------------------------------

import React, { useState, useEffect } from 'react';
import StrategistThemeProvider from '../../components/strategist/StrategistThemeProvider';
import { StrategistThemeToggle } from '../../components/strategist/StrategistThemeToggle';

// Phase 2 components
import ConquestScoreboard, { KarmicChip } from '../../components/strategist/phase2/ConquestScoreboard';
import LKGateSummaries from '../../components/strategist/phase2/LKGateSummaries';
import OracleVerdictBanners from '../../components/strategist/phase2/OracleVerdictBanners';
import ReentryLoop from '../../components/strategist/phase2/ReentryLoop';
import PrayPath from '../../components/strategist/phase2/PrayPath';
import KPGate0Panel from '../../components/strategist/phase2/KPGate0Panel';
import { SegPill, VerdictChip } from '../../components/strategist/phase2/StrategistPrimitives';

// Phase 2 CSS
import '../../styles/strategist-tokens.css';
import '../../styles/strategist-2f-scoreboard.css';
import '../../styles/strategist-2e-lkgates.css';
import '../../styles/strategist-2c-oracle.css';
import '../../styles/strategist-2d-reentry.css';
import '../../styles/strategist-2i-praypath.css';
import '../../styles/strategist-2b-gate0.css';
import '../../styles/strategist-2g-actionplan.css';

const BACKEND = process.env.REACT_APP_BACKEND_URL || '';

// -----------------------------------------------------------------
// DENSITY MAP -- page density → each module's A/B (per 2G Q-02·b)
// -----------------------------------------------------------------
const DENSITY_MAP = {
  command:  { board: 'compact',  diag: 'list',  pray: 'focus'    },
  briefing: { board: 'expanded', diag: 'grid',  pray: 'triptych' },
};

// -----------------------------------------------------------------
// GATE ADAPTER -- normalises backend gate_summaries shape to the
// CD-expected LKGateSummaries gate object shape.
//
// Backend shape:  { gate, name, status(UPPERCASE), narrative, ...extras }
// CD shape:       { id, code, name, facet, status(lowercase), narrative,
//                   asideLabel, asideValue }
// -----------------------------------------------------------------
const STATUS_MAP = {
  CLEAR: 'clear', ACTIVE: 'active', WARNING: 'warning', DORMANT: 'dormant',
  CONFLICT: 'warning', UNKNOWN: 'clear',
};

const GATE_META = {
  1: { code: 'G01', facet: 'Karmic Debt',      asideLabel: 'Pitru Rin' },
  2: { code: 'G02', facet: 'Sleeping Houses',  asideLabel: 'Dormant' },
  3: { code: 'G03', facet: 'Year Cycle',       asideLabel: 'Year lord' },
  4: { code: 'G04', facet: 'Mercury Scan',     asideLabel: 'Status' },
  5: { code: 'G05', facet: 'Geographical',     asideLabel: 'Direction' },
};

function gateAsideValue(g) {
  const gn = g.gate;
  const statusLabel = STATUS_MAP[g.status] || 'clear';
  if (gn === 2) return `${g.dormant_count || 0} dormant`;
  if (gn === 3) return g.planet || '--';
  if (gn === 5) return g.direction || '--';
  return statusLabel.charAt(0).toUpperCase() + statusLabel.slice(1);
}

function normalizeGates(rawGates) {
  if (!Array.isArray(rawGates) || rawGates.length === 0) return [];
  return rawGates.map((g) => {
    const meta = GATE_META[g.gate] || { code: `G0${g.gate}`, facet: '', asideLabel: 'Status' };
    return {
      id:         meta.code,
      code:       meta.code,
      name:       g.name || meta.code,
      facet:      meta.facet,
      status:     STATUS_MAP[g.status] || 'clear',
      narrative:  g.narrative || '',
      asideLabel: meta.asideLabel,
      asideValue: gateAsideValue(g),
    };
  });
}

// -----------------------------------------------------------------
// BANNERS -- hardcoded per field map (from OracleVerdictBanners BANNERS const)
// Used by VerdictCompact (Command density §03 render)
// -----------------------------------------------------------------
const BANNERS = {
  yes:  { headline: 'Advance Now', reasoning: 'Jupiter opens the 10th; the gain axis is unobstructed for the named action.', cta: 'Proceed' },
  wait: { headline: 'Hold Position', reasoning: 'Mercury retrograde shadow touches communication channels; defer until 9 Jun.', cta: 'Set Reminder' },
  no:   { headline: 'Stand Down', reasoning: 'Rahu in the 7th activates a partnership counter-signal; act now and yield the gain.', cta: 'View Re-entry Path' },
  pray: { headline: 'The Path is Devotional', reasoning: 'Saturn--Rahu fold in the 9H axis -- the karmic ledger must be addressed before temporal action.', cta: 'Begin the Offering' },
};

// -----------------------------------------------------------------
// ACTION QUEUE content (2G-owned · §05)
// Three moves distilled from verdict + diagnostics. Each ties back to
// a gate or the directive. Hardcoded scaffold -- future: live from API.
// -----------------------------------------------------------------
const ACTION_QUEUE = [
  {
    tone: 'em',
    move: 'Hold the Wednesday ritual',
    done: 4, total: 9,
    why: 'The streak is the cheapest route to Sovereign -- five weeks of unbroken cadence closes the gap. Do not change the form.',
    whyBold: { 'five weeks': true },
    src: { gate: 'G05', label: 'Devotional · + directive' },
    window: { l: 'cadence', v: 'weekly · Wed', crit: false },
  },
  {
    tone: 'amber',
    move: 'Tarpan on the next amavasya',
    done: 0, total: 1,
    why: 'The pitru thread at the 9H midpoint frays -- one tarpan seals it before it ripens to a 12H drain.',
    src: { gate: 'G04', label: 'Pitru · warning' },
    window: { l: 'window', v: '6 days', crit: true },
  },
  {
    tone: 'gold',
    move: 'Clear the 6H dormant-house chore',
    done: 1, total: 3,
    why: 'Routine work activates the first of three sleeping houses -- the 6th opens before the 8th and 12th follow.',
    src: { gate: 'G02', label: 'Sleeping Houses' },
    window: { l: 'cadence', v: '6H · weekly', crit: false },
  },
];

function firstMeaningfulString(...values) {
  for (const value of values) {
    if (typeof value === 'string' && value.trim()) return value.trim();
  }
  return '';
}

function extractKpGuidancePayload(raw) {
  const source = raw?.report || raw?.session || raw?.reading || raw?.data || raw || {};
  const sourceText = typeof source === 'string' ? source : '';
  const guidance = firstMeaningfulString(
    source?.guidance,
    source?.guidance_text,
    source?.oracle_guidance,
    source?.answer_text,
    source?.reading_text,
    source?.summary,
    source?.message,
    source?.content,
    source?.report_text,
    raw?.guidance,
    raw?.guidance_text,
    raw?.message,
    sourceText,
  );
  const mantra = firstMeaningfulString(
    source?.mantra,
    source?.mantra_text,
    source?.remedy?.mantra,
    source?.recommendation?.mantra,
    raw?.mantra,
  );
  return { guidance, mantra };
}

function formatDaysAgoLabel(daysSince) {
  if (daysSince == null || Number.isNaN(Number(daysSince))) return 'recently';
  const days = Number(daysSince);
  if (days <= 0) return 'today';
  if (days === 1) return '1 day ago';
  return `${days} days ago`;
}

function shouldShowKpGuidance(verdict) {
  return ['wait', 'no', 'pray'].includes((verdict || '').toLowerCase());
}

// -----------------------------------------------------------------
// Section frame component (from 2G composition shell)
// -----------------------------------------------------------------
function Section({ n, title, label, children }) {
  return (
    <section className="ap-sec" data-screen-label={label}>
      <div className="ap-sec__head">
        <span className="ap-sec__n">{n}</span>
        <h3 className="ap-sec__title">{title}</h3>
      </div>
      {children}
    </section>
  );
}

// -----------------------------------------------------------------
// Arrow icon (shared by VerdictCompact and ClearanceCard)
// -----------------------------------------------------------------
const ArrowSvg = ({ s = 11 }) => (
  <svg width={s} height={s} viewBox="0 0 12 12" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="2" y1="6" x2="10" y2="6" /><polyline points="7,3 10,6 7,9" />
  </svg>
);

// -----------------------------------------------------------------
// §03 · VerdictCompact -- Command density of the 2C banner (2G Q-02·b)
// Chip + headline + one-line reasoning + CTA. No signal rail.
// CSS: .ap-vc  (strategist-2g-actionplan.css)
// -----------------------------------------------------------------
function VerdictCompact({ verdict, onCtaClick }) {
  const b = BANNERS[verdict] || BANNERS.wait;
  return (
    <div className={`ap-vc ap-vc--${verdict}`}>
      <div className="ap-vc__chip-col">
        <span className="ap-vc__eyebrow">Verdict</span>
        <VerdictChip type={verdict} active />
      </div>
      <div className="ap-vc__text">
        <h2 className="ap-vc__headline">{b.headline}</h2>
        <p className="ap-vc__reason">&ldquo;{b.reasoning}&rdquo;</p>
      </div>
      <button type="button" className="ap-vc__cta" onClick={onCtaClick}>
        {b.cta} <ArrowSvg />
      </button>
    </div>
  );
}

// -----------------------------------------------------------------
// §04 · ClearanceCard -- YES verdict · quiet greenlight (2G Q-03 · new)
// CSS: .ap-clear  (strategist-2g-actionplan.css)
// -----------------------------------------------------------------
function ClearanceCard({ directive }) {
  return (
    <div className="ap-clear">
      <span className="ap-clear__seal" aria-hidden="true">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <polyline points="4,12.5 10,18 20,6" />
        </svg>
      </span>
      <div className="ap-clear__body">
        <span className="ap-clear__eyebrow">Greenlit &middot; no path required</span>
        <p className="ap-clear__line">You&apos;re cleared to move. Hold what&apos;s working.</p>
        <p className="ap-clear__directive">
          Standing directive &middot;{' '}
          <b>&ldquo;{directive || 'Hold your cadence'}&rdquo;</b>
          {' '}&mdash; the chart re-reads on demand, or automatically at the next score change.
        </p>
      </div>
      <div className="ap-clear__reread">
        <span className="ap-clear__reread-l">Next re-read</span>
        <span className="ap-clear__reread-v">On demand</span>
        <span className="ap-clear__reread-sub">or auto &middot; at score &Delta;</span>
      </div>
    </div>
  );
}

// -----------------------------------------------------------------
// §05 · QueuePips -- discrete pip track (lifted from 2D pattern)
// -----------------------------------------------------------------
function QueuePips({ done, total }) {
  return (
    <div className="ap-q__pip-track" aria-hidden="true">
      {Array.from({ length: total }, (_, i) => (
        <span key={i} className={`ap-q__pip${i < done ? ' ap-q__pip--done' : ''}`} />
      ))}
    </div>
  );
}

// -----------------------------------------------------------------
// §05 · ActionQueueModule -- new 2G-owned component
// Three moves from verdict + diagnostics, each cited to a gate.
// CSS: .ap-queue, .ap-q  (strategist-2g-actionplan.css)
// -----------------------------------------------------------------
function ActionQueueModule({ density }) {
  const cmd = density === 'command';
  return (
    <ul className="ap-queue">
      {ACTION_QUEUE.map((m, i) => (
        <li key={i} className={`ap-q ap-q--${m.tone}${cmd ? ' ap-q--command' : ''}`}>
          <span className="ap-q__n">{String(i + 1).padStart(2, '0')}</span>
          <div className="ap-q__body">
            <p className="ap-q__move">{m.move}</p>
            <p className="ap-q__why">{m.why}</p>
            <span className="ap-q__src">
              <span className="dot" aria-hidden="true"></span>
              distilled from &middot; <b>{m.src.gate}</b> &middot; {m.src.label}
            </span>
          </div>
          <div className="ap-q__progress">
            <div className="ap-q__progress-head">
              <span>Progress</span><b>{m.done} / {m.total}</b>
            </div>
            <QueuePips done={m.done} total={m.total} />
          </div>
          <div className="ap-q__window">
            {m.window.l}
            <b className={m.window.crit ? 'crit' : ''}>{m.window.v}</b>
          </div>
        </li>
      ))}
    </ul>
  );
}

function ApKpGuidance({ verdict, daysSince, guidance, mantra }) {
  const [open, setOpen] = useState(false);

  if (!shouldShowKpGuidance(verdict)) return null;

  return (
    <div className="ap-kp-guidance">
      <button
        type="button"
        className="ap-kp-guidance__header"
        onClick={() => setOpen((prev) => !prev)}
        aria-expanded={open}
      >
        <span>
          ◆ Oracle Guidance
          <span className="ap-kp-guidance__meta">last read: {formatDaysAgoLabel(daysSince)}</span>
        </span>
        <span>{open ? '▴ collapse' : '▾ expand'}</span>
      </button>
      {open && (
        <div className="ap-kp-guidance__body">
          <p>{guidance || 'Return to Gate 0 to receive new Oracle guidance.'}</p>
          {mantra ? (
            <div className="ap-kp-guidance__mantra">{mantra}</div>
          ) : null}
          <a href="/strategist" className="ap-kp-guidance__cta">
            Re-enter Gate 0
          </a>
        </div>
      )}
    </div>
  );
}

// -----------------------------------------------------------------
// Active-path source metadata for §04 Section sub-header
// -----------------------------------------------------------------
// -----------------------------------------------------------------
// Loading / Locked / Error shells
// -----------------------------------------------------------------
function ShellState({ children }) {
  return (
    <StrategistThemeProvider>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '60vh', gap: '1rem', padding: '0 1.5rem' }}>
        {children}
      </div>
    </StrategistThemeProvider>
  );
}

// -----------------------------------------------------------------
// StrategistActionPlanPage -- main export
// Fetches: /api/strategist/dashboard
// -----------------------------------------------------------------
export default function StrategistActionPlanPage() {
  const [loading, setLoading]     = useState(true);
  const [error, setError]         = useState('');
  const [locked, setLocked]       = useState(false);
  const [dashboard, setDashboard] = useState(null);
  const [density, setDensity]     = useState('briefing');
  const [gate0Status, setGate0Status] = useState(null);
  const [kpGuidance, setKpGuidance] = useState(null);

  // Fetch dashboard on mount
  useEffect(() => {
    let active = true;

    async function readJson(res) {
      const data = await res.json().catch(() => ({}));
      return { ok: res.ok, status: res.status, data };
    }

    async function load() {
      setLoading(true);
      setError('');
      setLocked(false);
      try {
        const [dashboardResult, gate0Result] = await Promise.allSettled([
          fetch(`${BACKEND}/api/strategist/dashboard`, { credentials: 'include' }).then(readJson),
          fetch(`${BACKEND}/api/strategist/gate0/status`, { credentials: 'include' }).then(readJson),
        ]);
        if (!active) return;

        const dashboardPayload = dashboardResult.status === 'fulfilled' ? dashboardResult.value : null;
        const gate0Payload = gate0Result.status === 'fulfilled' ? gate0Result.value : null;
        const data = dashboardPayload?.data || {};

        if (data?.error?.includes('LK profile missing')) { setLocked(true); return; }
        if (!dashboardPayload?.ok) throw new Error(data?.error || 'Unable to load action plan.');

        setDashboard(data);
        if (gate0Payload?.ok) setGate0Status(gate0Payload.data);

        const effectiveVerdict = (
          data?.scoreboard?.gate0_last_verdict
          || gate0Payload?.data?.last_verdict
          || ''
        ).toUpperCase();

        if (effectiveVerdict && effectiveVerdict !== 'YES') {
          const reportPayload = await fetch(
            `${BACKEND}/api/kp/sessions/last?context=strategist_gate0`,
            { credentials: 'include' },
          )
            .then(readJson)
            .catch(() => null);

          if (!active) return;

          const extracted = extractKpGuidancePayload(reportPayload?.data);
          setKpGuidance({
            verdict: effectiveVerdict.toLowerCase(),
            daysSince: data?.scoreboard?.gate0_days_since ?? null,
            guidance: extracted.guidance || 'Return to Gate 0 to receive new Oracle guidance.',
            mantra: extracted.mantra || '',
          });
        } else {
          setKpGuidance(null);
        }
      } catch (e) {
        if (!active) return;
        setError(e.message || 'Unable to load action plan right now.');
      } finally {
        if (active) setLoading(false);
      }
    }
    load();
    return () => { active = false; };
  }, []);

  if (loading) return (
    <ShellState>
      <p style={{ color: 'var(--gold)', fontFamily: 'var(--font-display)', fontSize: '1.1rem', letterSpacing: '0.08em' }}>
        Loading Action Plan&hellip;
      </p>
    </ShellState>
  );

  if (locked) return (
    <ShellState>
      <p style={{ color: 'var(--gold)', fontFamily: 'var(--font-display)', fontSize: '1.1rem' }}>Action Plan Locked</p>
      <p style={{ color: 'var(--strategist-fg-3)', fontSize: '0.9rem', textAlign: 'center', maxWidth: 340 }}>
        Complete your Strategist onboarding to activate the live engine.
      </p>
      <a href="/strategist" style={{ color: 'var(--gold)', textDecoration: 'underline', fontSize: '0.9rem' }}>
        Return to Strategist
      </a>
    </ShellState>
  );

  if (error) return (
    <ShellState>
      <p style={{ color: 'var(--gold)', fontFamily: 'var(--font-display)', fontSize: '1.1rem' }}>Action Plan Unavailable</p>
      <p style={{ color: 'var(--strategist-fg-3)', fontSize: '0.9rem', textAlign: 'center', maxWidth: 420 }}>{error}</p>
      <a href="/strategist/action-plan" style={{ color: 'var(--gold)', textDecoration: 'underline', fontSize: '0.9rem' }}>
        Retry
      </a>
    </ShellState>
  );

  if (!dashboard) return (
    <ShellState>
      <p style={{ color: 'var(--strategist-fg-3)', fontSize: '0.9rem' }}>Unable to map strategist engine output.</p>
    </ShellState>
  );

  // -----------------------------------------------------------------
  // Derived state from dashboard
  // -----------------------------------------------------------------
  const verdict   = (dashboard?.scoreboard?.gate0_last_verdict ?? 'wait').toLowerCase();
  const directive = dashboard?.scoreboard?.score_directive ?? '';
  const asOf      = new Date().toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' }) + ' IST';
  const d         = DENSITY_MAP[density];
  const guidanceVerdict = (dashboard?.scoreboard?.gate0_last_verdict || gate0Status?.last_verdict || '').toLowerCase();

  // Gates array for §02 Diagnostics -- normalised to CD LKGateSummaries shape
  const gates = normalizeGates(dashboard?.gate_summaries ?? []);

  // KP Gate 0 data -- shell values until STR-2A2 (KP Oracle integration) lands
  const gate0Days = dashboard?.scoreboard?.gate0_days_since ?? 0;
  const gate0 = dashboard?.scoreboard?.gate0_last_verdict
    ? {
        verdict:       verdict,
        question:      'Should I proceed with the named action in this Dasha period?',
        askedDaysAgo:  gate0Days,
        readAt:        gate0Days > 0 ? `${gate0Days} days ago` : 'Today',
        sublord:       dashboard?.scoreboard?.gate0_sublord       ?? '--',
        significators: dashboard?.scoreboard?.gate0_significators ?? [],
        cuspalRuler:   dashboard?.scoreboard?.gate0_cuspal_ruler  ?? '--',
      }
    : null;

  // -----------------------------------------------------------------
  // Render
  // -----------------------------------------------------------------
  return (
    <StrategistThemeProvider>

      {/* Floating nav -- back link (left) + theme toggle (right) */}
      <div style={{
        position: 'fixed', top: 16, left: 0, right: 0, zIndex: 50,
        display: 'flex', justifyContent: 'space-between', alignItems: 'center',
        padding: '0 20px', pointerEvents: 'none',
      }}>
        <a
          href="/strategist"
          style={{
            pointerEvents: 'auto',
            color: 'var(--strategist-fg-3)',
            fontFamily: 'var(--font-mono)',
            fontSize: '0.72rem', letterSpacing: '0.16em',
            textTransform: 'uppercase', textDecoration: 'none', opacity: 0.7,
          }}
          onMouseEnter={e  => { e.currentTarget.style.opacity = 1; }}
          onMouseLeave={e  => { e.currentTarget.style.opacity = 0.7; }}
        >
          &larr; War Room
        </a>
        <div style={{ pointerEvents: 'auto' }}>
          <StrategistThemeToggle />
        </div>
      </div>

      {/* Page root -- max-width container + top padding for nav */}
      <div style={{ maxWidth: 960, margin: '0 auto', paddingTop: 52 }}>

        {/* KP Gate 0 panel -- standalone above sections per TT process map */}
        {gate0 && (
          <div style={{ padding: '0 24px 20px' }}>
            <KPGate0Panel
              gate={gate0}
              asOf={asOf}
              onReconsult={() => { window.location.href = '/kp-oracle'; }}
              onViewReading={() => { window.location.href = '/kp-oracle'; }}
            />
          </div>
        )}

        {/* ── Sticky density strip (Q-02·b) ── */}
        <div className="ap-deck">
          <h2 className="ap-deck__title">
            <span className="diamond">&#9670;</span> Action Plan
          </h2>
          <div className="ap-deck__verdict">
            verdict <VerdictChip type={verdict} active />
          </div>
          <div className="ap-deck__control">
            <span className="ap-deck__control-lbl">density</span>
            <SegPill
              segments={[
                { value: 'command',  label: 'command'  },
                { value: 'briefing', label: 'briefing' },
              ]}
              value={density}
              onChange={setDensity}
              size="sm"
              ariaLabel="Page density"
            />
          </div>
        </div>

        {/* ── Five sections ── */}
        <div className="ap-body">

          {/* §01 · Digest -- 2F compact bar always; detail row in briefing */}
          <Section n="01" title="Digest" label="2G·01 Digest">
            <div className="ap-digest">
              <ConquestScoreboard
                data={dashboard}
                asOf={asOf}
                view="compact"
                showToggle={false}
              />
              {density === 'briefing' && (
                <div className="ap-digest__detail">
                  <div className="ap-digest__cell">
                    <span className="ap-digest__l">Rank</span>
                    <div className="ap-digest__v">
                      <strong>{dashboard?.scoreboard?.score_tier ?? '--'}</strong>
                    </div>
                    <span className="ap-digest__sub">
                      next &middot; {dashboard?.scoreboard?.next_threshold_label ?? '--'} &middot;{' '}
                      {dashboard?.scoreboard?.points_to_next ?? 0} to {dashboard?.scoreboard?.next_threshold ?? '--'}
                    </span>
                  </div>
                  <div className="ap-digest__cell">
                    <span className="ap-digest__l">Karmic</span>
                    <div className="ap-digest__v">
                      <KarmicChip state={dashboard?.scoreboard?.karmic_debt_cleared ?? 'Pending'} />
                    </div>
                    <span className="ap-digest__sub">ledger status</span>
                  </div>
                  <div className="ap-digest__cell">
                    <span className="ap-digest__l">Active verdict</span>
                    <div className="ap-digest__v">
                      <VerdictChip type={verdict} />
                    </div>
                    <span className="ap-digest__sub">answers the scanner above</span>
                  </div>
                  <div className="ap-digest__cell">
                    <span className="ap-digest__l">As of</span>
                    <div className="ap-digest__v"><strong>{asOf}</strong></div>
                    <span className="ap-digest__sub">re-read on demand</span>
                  </div>
                </div>
              )}
            </div>
          </Section>

          {/* §02 · Diagnostics -- LK gates list (command) / grid (briefing) */}
          <Section n="02" title="Diagnostics" label="2G·02 Diagnostics">
            <LKGateSummaries
              gates={gates}
              asOf={asOf}
              view={d.diag}
              showToggle={false}
            />
          </Section>

          {/* §03 · Verdict -- full banner (briefing) / compact line (command) */}
          <Section n="03" title="Verdict" label="2G·03 Verdict">
            {density === 'briefing' ? (
              <OracleVerdictBanners
                data={dashboard}
                asOf={asOf}
                onCtaClick={() => {}}
                onReadChartClick={() => { window.location.href = '/birth-chart'; }}
              />
            ) : (
              <VerdictCompact
                verdict={verdict}
                onCtaClick={() => {}}
              />
            )}
            <ApKpGuidance
              verdict={kpGuidance?.verdict || guidanceVerdict}
              daysSince={kpGuidance?.daysSince ?? dashboard?.scoreboard?.gate0_days_since ?? null}
              guidance={kpGuidance?.guidance}
              mantra={kpGuidance?.mantra}
            />
          </Section>

          {/* §04 · Active Path -- switch(verdict): 2D (no/wait) · 2I (pray) · ClearanceCard (yes) */}
          <Section n="04" title="Active Path" label="2G·04 Active Path">
            {verdict === 'pray' && (
              <PrayPath
                data={dashboard}
                asOf={asOf}
                onBegin={() => {}}
                view={d.pray}
                showToggle={false}
              />
            )}
            {(verdict === 'no' || verdict === 'wait') && (
              <ReentryLoop
                data={dashboard}
                asOf={asOf}
                density={density}
              />
            )}
            {verdict === 'yes' && (
              <ClearanceCard directive={directive} />
            )}
          </Section>

          {/* §05 · Action Queue -- new 2G-owned component */}
          <Section n="05" title="Action Queue" label="2G·05 Action Queue">
            <ActionQueueModule density={density} />
          </Section>

        </div>{/* end .ap-body */}
      </div>{/* end page root */}

    </StrategistThemeProvider>
  );
}
