import { SEO } from '../components/SEO';
import { PremiumGateCard } from '../components/PremiumRoute';
import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { WarRoomStateProvider, useWarRoom } from '../components/WarRoomStateProvider';
import ConquestGauge from '../components/ConquestGauge';
import HurdleAlert from '../components/HurdleAlert';
import KrishnaOracleGrid from '../components/KrishnaOracleGrid';

const BACKEND = process.env.REACT_APP_BACKEND_URL || '';

const WAR_ROOM_LABEL = {
  OFFENSIVE_GOLD:     '⚔️ OFFENSIVE — Rituals OPEN',
  GOLDEN_HOUR:        '🌅 GOLDEN HOUR — Act NOW',
  DEFENSIVE_MIDNIGHT: '🌙 DEFENSIVE — Rituals LOCKED',
};

// ── Layer badge pill ──────────────────────────────────────────────────────────
function LayerBadge({ n, label, status }) {
  const colors = {
    active:   'border-gold/40 bg-gold/10 text-gold',
    locked:   'border-white/10 bg-white/[0.03] text-muted-foreground',
    complete: 'border-emerald-500/40 bg-emerald-500/10 text-emerald-400',
    blocked:  'border-red-500/30 bg-red-500/[0.06] text-red-400',
  };
  return (
    <div className={`flex items-center gap-2 rounded-lg border px-3 py-1.5 text-xs font-medium ${colors[status] || colors.locked}`}>
      <span className="font-mono opacity-60">L{n}</span>
      <span>{label}</span>
    </div>
  );
}

// ── Gate 0 compact oracle panel ───────────────────────────────────────────────
function Gate0Panel({ onVerdict }) {
  const [gridMatrix, setGridMatrix] = useState([]);
  const [loadingGrid, setLoadingGrid] = useState(true);
  const [selectedIndex, setSelectedIndex] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetch(`${BACKEND}/api/oracle/krishna-prashnavali/meta`, { credentials: 'include' })
      .then(r => r.json())
      .then(d => setGridMatrix(d.grid_matrix || []))
      .catch(() => setError('Unable to load Oracle grid.'))
      .finally(() => setLoadingGrid(false));
  }, []);

  async function handleCellSelect({ row, col, index }) {
    setSelectedIndex(index);
    setSubmitting(true);
    setError('');
    try {
      const res = await fetch(`${BACKEND}/api/strategist/gate0/select`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ row, col }),
      });
      const data = await res.json();
      const verdict = data?.reading?.answer?.verdict_display || 'WAIT';
      onVerdict(verdict, data?.reading || null);
    } catch {
      setError('Unable to generate Krishna guidance right now.');
      setSelectedIndex(null);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-5">
      <div className="flex items-center justify-between mb-3">
        <div>
          <p className="text-[10px] uppercase tracking-widest text-muted-foreground">Gate 0 — Oracle Clearance</p>
          <p className="text-sm font-semibold text-foreground mt-0.5">Ask Krishna Before You Enter</p>
        </div>
        <Link to="/krishna-prashnavali" className="text-[10px] text-muted-foreground hover:text-gold transition">
          Full Oracle →
        </Link>
      </div>
      <p className="text-xs text-muted-foreground mb-4 leading-relaxed">
        Touch one cell. Krishna's answer determines your mission clearance for today.
      </p>
      {error && <p className="text-amber-400 text-xs mb-3">{error}</p>}
      {loadingGrid ? (
        <p className="text-xs text-muted-foreground">Loading Oracle grid…</p>
      ) : (
        <div className="overflow-x-auto">
          <KrishnaOracleGrid
            gridMatrix={gridMatrix}
            selectedIndex={selectedIndex}
            disabled={submitting}
            revealEnabled={false}
            onSelect={handleCellSelect}
          />
        </div>
      )}
      {submitting && <p className="text-xs text-gold mt-3 text-center">Reading Oracle…</p>}
    </div>
  );
}

// ── Verdict banner ────────────────────────────────────────────────────────────
function VerdictBanner({ verdict, reading }) {
  const configs = {
    YES:  { border: 'border-emerald-500/40 bg-emerald-500/10', heading: '✅ YES — Path is Clear', body: reading?.answer?.meaning?.english_block || 'The path is favorable. Proceed with your strategic mission.' },
    WAIT: { border: 'border-orange-500/40 bg-orange-500/10',  heading: '⏳ WAIT — Begin Your Remedy Plan First', body: reading?.answer?.meaning?.english_block || 'Patience is required. Activate your LK Tracker streak, then return.' },
    NO:   { border: 'border-red-500/40 bg-red-500/10',        heading: '🛑 NO — Strategic Realignment Required', body: reading?.answer?.meaning?.english_block || 'Resistance is active. Reach 60% Conquest Probability through remedies, then re-test.' },
    PRAY: { border: 'border-purple-500/40 bg-purple-500/10',  heading: '🙏 PRAY — Full Surrender Path', body: reading?.answer?.meaning?.english_block || 'Krishna calls you to full surrender. Complete Mantra practice and LK Debt Audit.' },
  };
  const cfg = configs[verdict] || configs.WAIT;
  return (
    <div className={`rounded-xl border ${cfg.border} p-4`}>
      <p className="font-semibold text-sm mb-1">{cfg.heading}</p>
      <p className="text-sm text-muted-foreground leading-relaxed">{cfg.body}</p>
    </div>
  );
}

// ── PRAY full surrender panel ─────────────────────────────────────────────────
function PraySurrenderPanel() {
  const [ctx, setCtx] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${BACKEND}/api/strategist/surrender-context`, { credentials: 'include' })
      .then(r => r.json())
      .then(setCtx)
      .catch(() => setCtx(null))
      .finally(() => setLoading(false));
  }, []);

  const score   = ctx?.conquest_score ?? null;
  const ptsTo75 = ctx?.points_to_75  ?? null;
  const pct     = score != null ? Math.min(100, Math.round((score / 75) * 100)) : 0;

  return (
    <div className="rounded-xl border border-purple-500/40 bg-purple-500/[0.06] p-5 space-y-4">
      <div>
        <p className="font-semibold text-sm text-purple-300 mb-1">🙏 Full Surrender Path — PRAY Verdict Active</p>
        <p className="text-xs text-muted-foreground leading-relaxed">
          Krishna calls you inward before any outward mission. Complete the surrender sequence, then re-test when your score reaches 75%.
        </p>
      </div>
      {score != null && (
        <div>
          <div className="flex justify-between text-[10px] text-muted-foreground mb-1">
            <span>Conquest score: <span className="text-purple-300 font-semibold">{score}%</span></span>
            <span>{ptsTo75} pts to re-test (75%)</span>
          </div>
          <div className="h-2 rounded-full bg-purple-900/40 overflow-hidden">
            <div className="h-full rounded-full bg-gradient-to-r from-purple-600 to-purple-400 transition-all duration-500" style={{ width: `${pct}%` }} />
          </div>
        </div>
      )}
      {!loading && ctx?.featured_mantra && (
        <div className="rounded-lg border border-purple-500/30 bg-purple-900/20 p-4">
          <p className="text-[10px] uppercase tracking-widest text-purple-400 mb-2">
            Featured Mantra — {ctx.featured_mantra.deity || ctx.featured_mantra.remedy_area}
          </p>
          <p className="text-xl leading-relaxed text-purple-100 font-medium mb-1">{ctx.featured_mantra.mantra_devanagari}</p>
          <p className="text-xs text-purple-300 italic mb-2">{ctx.featured_mantra.mantra_transliteration}</p>
          {ctx.featured_mantra.guidance && (
            <p className="text-[11px] text-muted-foreground mt-2 leading-relaxed">{ctx.featured_mantra.guidance}</p>
          )}
          <Link to="/mantra-remedies" className="mt-3 inline-block text-xs text-purple-300 hover:underline">Full Mantra Library →</Link>
        </div>
      )}
      {ctx?.gate1_narrative && (
        <div className="rounded-lg border border-amber-500/30 bg-amber-500/[0.06] p-3">
          <p className="text-[10px] uppercase tracking-widest text-amber-400 mb-1">Karmic Debt Status</p>
          <p className="text-xs text-muted-foreground leading-relaxed">{ctx.gate1_narrative}</p>
          <Link to="/lk-remedies/debt-audit" className="mt-2 inline-block text-xs text-amber-400 hover:underline">Run Debt Audit →</Link>
        </div>
      )}
      {ctx?.surrender_steps?.length > 0 && (
        <ol className="space-y-2">
          {ctx.surrender_steps.map((step, i) => (
            <li key={i} className="flex gap-3 text-xs text-muted-foreground">
              <span className="shrink-0 font-bold text-purple-400">{i + 1}.</span>
              <span className="leading-relaxed">{step}</span>
            </li>
          ))}
        </ol>
      )}
      <div className="flex gap-3 flex-wrap pt-1">
        <Link to="/mantra-remedies" className="inline-block rounded-lg border border-purple-500/50 bg-purple-500/20 px-4 py-2 text-sm font-semibold text-purple-300 hover:bg-purple-500/30 transition">Mantra Remedies →</Link>
        <Link to="/lk-remedies/debt-audit" className="inline-block rounded-lg border border-amber-500/40 bg-amber-500/10 px-4 py-2 text-sm font-semibold text-amber-300 hover:bg-amber-500/20 transition">LK Debt Audit →</Link>
      </div>
    </div>
  );
}

// ── Pre-flight panel (WAIT / NO) ──────────────────────────────────────────────
function PreFlightPanel({ gateStatus, conquestScore }) {
  if (gateStatus === 'pray_blocked') return <PraySurrenderPanel />;

  if (gateStatus === 'wait_active') return (
    <div className="rounded-xl border border-orange-500/40 bg-orange-500/10 p-5">
      <p className="font-semibold text-sm mb-2">⏳ Pre-Flight Mode — Remedy Plan Required</p>
      <p className="text-sm text-muted-foreground leading-relaxed mb-4">
        Oracle asks for patience. Build your daily LK streak. War Room unlocks automatically once your streak is active.
      </p>
      <Link to="/lk-remedies/tracker" className="inline-block rounded-lg border border-orange-500/50 bg-orange-500/20 px-4 py-2 text-sm font-semibold text-orange-300 hover:bg-orange-500/30 transition">
        Start LK Tracker →
      </Link>
    </div>
  );

  if (gateStatus === 'no_blocked') return (
    <div className="rounded-xl border border-red-500/40 bg-red-500/10 p-5">
      <p className="font-semibold text-sm mb-2">🛑 Conquest Score Required — 60%+</p>
      {conquestScore != null && (
        <p className="text-sm text-muted-foreground mb-2">Current score: <span className="font-bold text-red-400">{conquestScore}%</span></p>
      )}
      <p className="text-sm text-muted-foreground leading-relaxed mb-4">
        Complete your remedy cycle to raise Conquest Probability above 60%, then re-test at Gate 0.
      </p>
      <div className="flex gap-3 flex-wrap">
        <Link to="/lk-remedies/remedies" className="inline-block rounded-lg border border-red-500/50 bg-red-500/20 px-4 py-2 text-sm font-semibold text-red-300 hover:bg-red-500/30 transition">Browse Remedies →</Link>
        <Link to="/lk-remedies/tracker" className="inline-block rounded-lg border border-gold/30 bg-gold/10 px-4 py-2 text-sm font-semibold text-gold hover:bg-gold/20 transition">LK Tracker →</Link>
      </div>
    </div>
  );

  return null;
}

// ── Scoreboard ────────────────────────────────────────────────────────────────
function Scoreboard({ sb }) {
  const pct = sb.next_threshold ? Math.min(100, Math.round((sb.conquest_score / sb.next_threshold) * 100)) : 100;
  const verdictColor = { YES: 'text-emerald-400', WAIT: 'text-orange-400', NO: 'text-red-400', PRAY: 'text-purple-400' }[sb.gate0_last_verdict] || 'text-muted-foreground';
  return (
    <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-5">
      <p className="text-[11px] uppercase tracking-widest text-muted-foreground mb-4">Success &amp; Debt Scoreboard</p>
      <div className="flex items-end justify-between mb-3">
        <div>
          <p className="text-3xl font-bold text-gold">{sb.conquest_score}<span className="text-lg">%</span></p>
          <p className="text-xs text-muted-foreground mt-0.5">{sb.score_tier} — {sb.score_directive}</p>
        </div>
        <div className="text-right">
          <p className="text-xs text-muted-foreground">Streak</p>
          <p className="text-lg font-bold text-emerald-400">{sb.streak_days}d</p>
          <p className="text-[10px] text-muted-foreground">{sb.streak_tier}</p>
        </div>
      </div>
      {sb.next_threshold && (
        <div className="mb-4">
          <div className="flex justify-between text-[10px] text-muted-foreground mb-1">
            <span>Progress to {sb.next_threshold_label}</span>
            <span>{sb.points_to_next} pts remaining</span>
          </div>
          <div className="h-2 rounded-full bg-gold/10 overflow-hidden">
            <div className="h-full rounded-full bg-gradient-to-r from-gold/60 to-gold transition-all duration-500" style={{ width: `${pct}%` }} />
          </div>
        </div>
      )}
      <div className="grid grid-cols-2 gap-3 text-center">
        <div className="rounded-lg border border-gold/10 bg-background/40 p-3">
          <p className="text-[10px] text-muted-foreground mb-1">Karmic Debt</p>
          <p className={`text-sm font-semibold ${sb.karmic_debt_cleared ? 'text-emerald-400' : 'text-amber-400'}`}>
            {sb.karmic_debt_cleared ? 'Cleared ✓' : 'Active ⚠'}
          </p>
        </div>
        <div className="rounded-lg border border-gold/10 bg-background/40 p-3">
          <p className="text-[10px] text-muted-foreground mb-1">Last Gate 0</p>
          {sb.gate0_last_verdict ? (
            <>
              <p className={`text-sm font-semibold ${verdictColor}`}>{sb.gate0_last_verdict}</p>
              <p className="text-[10px] text-muted-foreground">{sb.gate0_days_since === 0 ? 'Today' : `${sb.gate0_days_since}d ago`}</p>
            </>
          ) : (
            <p className="text-sm text-muted-foreground">None yet</p>
          )}
        </div>
      </div>
    </div>
  );
}

// ── 3-Step Onboarding prompt ──────────────────────────────────────────────────
function OnboardingRequired() {
  const steps = [
    {
      n: 1, title: 'Complete LK Onboarding',
      desc: 'Enter birth details, family census, and office location. Powers your natal chart, command planet, and Digbala direction.',
      cta: 'Start Onboarding →', to: '/lk-remedies/onboard',
      color: 'border-gold/40 bg-gold/[0.06]',
      ctaColor: 'border-gold/50 bg-gold/20 text-gold hover:bg-gold/30',
    },
    {
      n: 2, title: 'Run LK 5-Gate Diagnosis',
      desc: 'Audit karmic debt, house awakening, year cycle planet, Mercury scan, and geographical alignment.',
      cta: 'Run Diagnosis →', to: '/lk-remedies/report',
      color: 'border-amber-500/30 bg-amber-500/[0.04]',
      ctaColor: 'border-amber-500/40 bg-amber-500/10 text-amber-400 hover:bg-amber-500/20',
    },
    {
      n: 3, title: 'War Room Goes Live',
      desc: 'Your birth chart drives every signal — conquest probability, active missions, hurdle alerts, and remedy timing load automatically.',
      cta: null, to: null,
      color: 'border-emerald-500/20 bg-emerald-500/[0.03]', ctaColor: '',
    },
  ];
  return (
    <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-5">
      <p className="text-[10px] uppercase tracking-widest text-muted-foreground mb-1">Layer 1 — Astrology Engine</p>
      <p className="text-sm font-semibold text-foreground mb-1">3-Step War Room Setup</p>
      <p className="text-xs text-muted-foreground mb-4 leading-relaxed">
        Complete onboarding once. Your live birth chart, dasha, and LK diagnosis power every layer.
      </p>
      <div className="space-y-3">
        {steps.map(s => (
          <div key={s.n} className={`rounded-lg border ${s.color} p-4`}>
            <div className="flex items-start gap-3">
              <span className="shrink-0 flex h-6 w-6 items-center justify-center rounded-full border border-gold/30 bg-gold/10 text-[11px] font-bold text-gold">{s.n}</span>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-semibold text-foreground">{s.title}</p>
                <p className="text-xs text-muted-foreground mt-0.5 leading-relaxed">{s.desc}</p>
                {s.cta && (
                  <Link to={s.to} className={`mt-3 inline-block rounded-lg border px-3 py-1.5 text-xs font-semibold transition ${s.ctaColor}`}>
                    {s.cta}
                  </Link>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ── Layer 1: Astrology strip ──────────────────────────────────────────────────
function AstrologyStrip({ data }) {
  if (!data) return null;
  if (!data.command_planet) return <OnboardingRequired />;
  return (
    <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-4">
      <p className="text-[10px] uppercase tracking-widest text-muted-foreground mb-3">Layer 1 — Astrology Engine</p>
      <div className="grid grid-cols-2 gap-3">
        <div className="text-center">
          <p className="text-xs text-muted-foreground">Command Planet</p>
          <p className="text-gold font-bold text-xl mt-0.5">{data.command_planet}</p>
        </div>
        <div className="text-center">
          <p className="text-xs text-muted-foreground">Power Direction</p>
          <p className="text-gold font-bold text-xl mt-0.5">{data.success_direction}</p>
        </div>
        <div className="text-center">
          <p className="text-xs text-muted-foreground">Current Dasha</p>
          <p className="text-foreground font-semibold text-sm mt-0.5">{data.mahadasha || '—'}</p>
        </div>
        <div className="text-center">
          <p className="text-xs text-muted-foreground">Antardasha</p>
          <p className="text-foreground font-semibold text-sm mt-0.5">{data.antardasha || '—'}</p>
        </div>
      </div>
    </div>
  );
}

// ── Layer 2: LK 5-Gate status ─────────────────────────────────────────────────
function LKGateStatus({ gates }) {
  if (!gates?.length) return null;
  return (
    <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-4">
      <div className="flex items-center justify-between mb-3">
        <p className="text-[10px] uppercase tracking-widest text-muted-foreground">Layer 2 — Lal Kitab 5-Gate Diagnosis</p>
        <Link to="/lk-remedies/report" className="text-[10px] text-gold hover:underline">Full Report →</Link>
      </div>
      <div className="space-y-2">
        {gates.map(g => {
          const isWarning = ['WARNING', 'DORMANT', 'RAHU_COLLISION', 'EMPTY_VESSEL'].includes(g.status);
          const isClear   = ['CLEAR', 'ACTIVE'].includes(g.status);
          const dot = isWarning ? 'bg-amber-400' : isClear ? 'bg-emerald-400' : 'bg-muted-foreground';
          return (
            <div key={g.gate} className="flex items-start gap-3">
              <span className={`mt-1.5 h-2 w-2 shrink-0 rounded-full ${dot}`} />
              <div className="min-w-0">
                <span className="text-xs font-semibold text-foreground">Gate {g.gate} — {g.name}</span>
                <p className="text-xs text-muted-foreground leading-relaxed">{g.narrative}</p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ── Layer 3: Missions + quick links ──────────────────────────────────────────
function MissionQuickLinks({ data }) {
  return (
    <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-4">
      <p className="text-[10px] uppercase tracking-widest text-muted-foreground mb-3">Layer 3 — Strategist Engine</p>
      <div className="grid grid-cols-2 gap-3 mb-3">
        <div className="rounded-lg border border-gold/10 bg-background/40 p-3 text-center">
          <p className="text-xs text-muted-foreground">Active Missions</p>
          <p className="text-gold font-bold text-2xl mt-0.5">{data.active_missions_count ?? '—'}</p>
        </div>
        <div className="rounded-lg border border-gold/10 bg-background/40 p-3 text-center">
          <p className="text-xs text-muted-foreground">Ritual Streak</p>
          <p className="text-emerald-400 font-bold text-2xl mt-0.5">{data.ritual_streak ?? 0}d</p>
        </div>
      </div>
      <div className="grid grid-cols-2 gap-2">
        <Link to="/strategist/missions" className="rounded-lg border border-gold/20 bg-gold/[0.04] p-3 text-center hover:bg-gold/10 transition">
          <p className="text-xs text-muted-foreground">Mission Board</p>
          <p className="text-gold text-xs font-semibold mt-0.5">View All →</p>
        </Link>
        <Link to="/lk-remedies/tracker" className="rounded-lg border border-gold/20 bg-gold/[0.04] p-3 text-center hover:bg-gold/10 transition">
          <p className="text-xs text-muted-foreground">LK Tracker</p>
          <p className="text-gold text-xs font-semibold mt-0.5">Day {data.ritual_streak ?? 0} →</p>
        </Link>
        <Link to="/strategist/surrogate" className="rounded-lg border border-gold/20 bg-gold/[0.04] p-3 text-center hover:bg-gold/10 transition">
          <p className="text-xs text-muted-foreground">Surrogate Bridge</p>
          <p className="text-gold text-xs font-semibold mt-0.5">Activate →</p>
        </Link>
        <Link to="/strategist/action-plan" className="rounded-lg border border-gold/30 bg-gradient-to-br from-gold/15 to-gold/5 p-3 text-center hover:bg-gold/20 transition">
          <p className="text-xs text-muted-foreground">Action Plan</p>
          <p className="text-gold text-xs font-semibold mt-0.5">Today →</p>
        </Link>
        <Link to="/strategist/report" className="col-span-2 rounded-lg border border-gold/20 bg-gold/[0.04] p-3 text-center hover:bg-gold/10 transition">
          <p className="text-xs text-muted-foreground">Executive Intelligence Brief</p>
          <p className="text-gold text-xs font-semibold mt-0.5">Premium Report →</p>
        </Link>
      </div>
    </div>
  );
}

// ── Layer 3 locked placeholder ────────────────────────────────────────────────
function Layer3Locked() {
  return (
    <div className="rounded-xl border border-gold/10 bg-gold/[0.02] p-5 text-center opacity-60">
      <p className="text-xs text-muted-foreground mb-1">🔒 Layer 3 — Missions &amp; Action Plan</p>
      <p className="text-[11px] text-muted-foreground">Consult the Oracle above to unlock your active missions.</p>
    </div>
  );
}

// ── Main Dashboard ────────────────────────────────────────────────────────────
function Dashboard() {
  const { state: warState, countdown } = useWarRoom();

  // Gate 0
  const [gateStatus,    setGateStatus]    = useState('loading');
  const [conquestScore, setConquestScore] = useState(null);
  const [freshVerdict,  setFreshVerdict]  = useState(null);
  const [lastVerdict,   setLastVerdict]   = useState(null);

  // Dashboard data (shared between Layer 1, 2, and 3)
  const [dash,        setDash]        = useState(null);
  const [dashLoading, setDashLoading] = useState(true);
  const [dashError,   setDashError]   = useState('');

  useEffect(() => {
    fetch(`${BACKEND}/api/strategist/gate0/status`, { credentials: 'include' })
      .then(r => r.json())
      .then(d => {
        setGateStatus(d.status || 'required');
        setConquestScore(d.conquest_score ?? null);
        setLastVerdict(d.last_verdict ?? null);
      })
      .catch(() => setGateStatus('required'));
  }, []);

  useEffect(() => {
    fetch(`${BACKEND}/api/strategist/dashboard`, { credentials: 'include' })
      .then(r => r.json())
      .then(d => { if (d.error) throw new Error(d.error); setDash(d); })
      .catch(e => setDashError(e.message))
      .finally(() => setDashLoading(false));
  }, []);

  function handleVerdict(verdict, reading) {
    setFreshVerdict({ verdict, reading });
    setLastVerdict(verdict);
    if (verdict === 'YES')        setGateStatus('clear');
    else if (verdict === 'WAIT')  setGateStatus('wait_active');
    else if (verdict === 'NO')    setGateStatus('no_blocked');
    else                          setGateStatus('pray_blocked');
  }

  const missionsUnlocked = gateStatus === 'clear';
  const blocked          = ['wait_active', 'no_blocked', 'pray_blocked'].includes(gateStatus);
  const needsGate0       = gateStatus === 'required';

  const layerStatus = (n) => {
    if (n === 0) return missionsUnlocked ? 'complete' : 'active';
    if (n <= 2)  return 'active';
    if (n >= 3)  return missionsUnlocked ? 'active' : 'locked';
    return 'locked';
  };

  return (
    <div className="min-h-screen bg-background text-foreground">
      <div className="max-w-2xl mx-auto px-4 py-8 space-y-5">

        {/* ── Header ───────────────────────────────────────────────── */}
        <div>
          <div className="flex items-start justify-between gap-3">
            <div>
              <p className="text-[10px] uppercase tracking-widest text-muted-foreground mb-1">Bloomberg Terminal for Karma</p>
              <h1 className="text-2xl font-bold text-foreground">The Strategist</h1>
            </div>
            {gateStatus !== 'loading' && (
              <Link
                to="/lk-remedies/onboard"
                className="shrink-0 mt-1 rounded-lg border border-gold/30 bg-gold/[0.06] px-3 py-1.5 text-xs font-medium text-gold hover:bg-gold/15 transition"
              >
                Redo Setup
              </Link>
            )}
          </div>
          <p className="text-sm text-muted-foreground mt-2 leading-relaxed">
            A business intelligence war room powered by Lal Kitab, Vedic Astrology, and the Krishna Oracle.
            Your birth chart drives every signal — missions, remedies, and timing are all live.
          </p>
        </div>

        {/* ── Layer journey strip ───────────────────────────────────── */}
        <div className="flex flex-wrap gap-2">
          <LayerBadge n={0} label="Oracle Gate"  status={layerStatus(0)} />
          <LayerBadge n={1} label="Astrology"    status={layerStatus(1)} />
          <LayerBadge n={2} label="LK Diagnosis" status={layerStatus(2)} />
          <LayerBadge n={3} label="Missions"     status={layerStatus(3)} />
          <LayerBadge n={4} label="Action Plan"  status={layerStatus(4)} />
          <LayerBadge n={5} label="Report"       status={layerStatus(5)} />
        </div>

        {/* ── War state banner ──────────────────────────────────────── */}
        <div className={`rounded-xl border ${warState === 'GOLDEN_HOUR' ? 'border-orange-500/50 bg-orange-500/10 animate-pulse' : 'border-gold/20 bg-gold/[0.04]'} p-4 text-center`}>
          <p className="text-sm font-semibold text-gold">{WAR_ROOM_LABEL[warState] || WAR_ROOM_LABEL.OFFENSIVE_GOLD}</p>
          {countdown && <p className="text-2xl font-mono text-orange-400 mt-1">{countdown}</p>}
        </div>

        {/* ── Layer 1 — Astrology (always shown) ───────────────────── */}
        {dashLoading && (
          <div className="text-center text-muted-foreground text-sm py-2">Loading War Room data…</div>
        )}
        {dashError && (
          <div className="rounded-xl border border-amber-500/30 bg-amber-500/10 p-4">
            <p className="text-amber-400 text-sm">{dashError}</p>
            <Link to="/lk-remedies/onboard" className="text-gold text-xs underline mt-1 block">Complete LK Onboarding first →</Link>
          </div>
        )}
        {!dashLoading && dash && (
          <>
            <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-5 text-center">
              <p className="text-xs text-muted-foreground mb-3">Conquest Probability</p>
              <ConquestGauge {...(dash.conquest_probability || {})} />
            </div>
            <AstrologyStrip data={dash} />
          </>
        )}
        {!dashLoading && !dash && !dashError && <AstrologyStrip data={null} />}

        {/* ── Gate 0 — Oracle check (between Layer 1 and Layer 2) ──── */}
        {gateStatus === 'loading' && (
          <div className="text-center text-muted-foreground text-sm py-2">Checking Oracle clearance…</div>
        )}
        {needsGate0 && (
          <>
            {lastVerdict && (
              <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-3 text-center">
                <p className="text-xs text-muted-foreground">
                  Previous verdict: <span className="text-gold font-semibold">{lastVerdict}</span> — Score qualifies you for re-test.
                </p>
              </div>
            )}
            <Gate0Panel onVerdict={handleVerdict} />
          </>
        )}
        {missionsUnlocked && lastVerdict && (
          <div className="flex items-center gap-2 rounded-lg border border-emerald-500/30 bg-emerald-500/[0.06] px-4 py-2">
            <span className="h-2 w-2 rounded-full bg-emerald-400" />
            <p className="text-xs text-muted-foreground">Gate 0 cleared — Oracle verdict: <span className="font-semibold text-emerald-400">{lastVerdict}</span></p>
          </div>
        )}
        {freshVerdict && !needsGate0 && (
          <VerdictBanner verdict={freshVerdict.verdict} reading={freshVerdict.reading} />
        )}
        {blocked && (
          <PreFlightPanel gateStatus={gateStatus} conquestScore={conquestScore} />
        )}

        {/* ── Layer 2 — LK 5-Gate (AFTER Gate 0) ──────────────────── */}
        {dash && <LKGateStatus gates={dash.gate_summaries} />}

        {/* ── Layer 3 — Missions (unlocked or locked) ──────────────── */}
        {missionsUnlocked && dash ? (
          <div className="space-y-4">
            <MissionQuickLinks data={dash} />
            {dash.scoreboard && <Scoreboard sb={dash.scoreboard} />}
          </div>
        ) : (
          <Layer3Locked />
        )}

      </div>
    </div>
  );
}

function StrategistLanding() {
  const navigate = useNavigate();
  const pillars = [
    { icon: "🔱", title: "Gate 0 — Krishna Oracle", body: "Before any campaign, consult Lord Krishna via the 18×18 Prashnavali. The War Room unlocks only on YES or WAIT." },
    { icon: "📊", title: "5-Gate Lal Kitab Engine", body: "Your birth chart is decoded across 5 planetary gates — Finance, Career, Health, Relationships, Dharma. Each gate produces a live remedy plan." },
    { icon: "⚔️", title: "War Room Missions", body: "Live missions aligned to your Dasha — daily conquest actions with KPIs, deadlines, and surrogate rituals for blocked gates." },
    { icon: "📈", title: "Conquest Score & Streak", body: "Every logged action builds your Conquest Score. Hit thresholds to unlock advanced missions and premium strategy reports." },
  ];
  const schema = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      { "@type": "Question", "name": "What is The Strategist?", "acceptedAnswer": { "@type": "Answer", "text": "The Strategist is a Vedic business strategy system combining Lal Kitab planetary diagnostics, Krishna Prashnavali oracle, and a live mission board — built for founders, professionals, and serious decision-makers." } },
      { "@type": "Question", "name": "How does the Gate 0 oracle work?", "acceptedAnswer": { "@type": "Answer", "text": "Gate 0 is powered by the Krishna Prashnavali oracle. Before entering the War Room, you receive a YES, WAIT, NO, or PRAY verdict overlaid with your live Dasha and transits. The War Room unlocks on YES or WAIT; NO and PRAY trigger specific remedy paths." } },
      { "@type": "Question", "name": "What is a Conquest Score?", "acceptedAnswer": { "@type": "Answer", "text": "Your Conquest Score accumulates as you complete daily missions and remedy rituals. Higher scores unlock premium reports and advanced War Room features." } },
    ]
  };
  return (
    <div className="min-h-screen bg-background text-foreground">
      <SEO
        title="The Strategist — Vedic Business War Room"
        description="A Vedic strategy system for founders and professionals. Gate 0 Krishna Oracle, 5-Gate Lal Kitab diagnostics, live missions, Conquest Score, and premium intelligence reports — all driven by your birth chart."
        url="https://www.everydayhoroscope.in/strategist"
        schema={schema}
      />
      <div className="max-w-4xl mx-auto px-4 py-16">
        <div className="text-center mb-14">
          <p className="text-xs uppercase tracking-[0.3em] text-gold/70 mb-3">Vedic Strategy Intelligence</p>
          <h1 className="text-4xl sm:text-5xl font-playfair font-bold mb-4">The Strategist</h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto mb-8">
            The War Room that merges Krishna's oracle, Lal Kitab planetary analysis, and live mission tracking into one decisive command centre.
          </p>
          <button
            onClick={() => navigate('/login')}
            className="inline-flex items-center gap-2 rounded-xl bg-gold px-8 py-4 text-base font-semibold text-stone-950 shadow-lg hover:bg-gold/90 transition"
          >
            Enter the War Room →
          </button>
          <p className="mt-4 text-xs text-muted-foreground">Requires an EverydayHoroscope account · Free to join</p>
        </div>

        <div className="grid sm:grid-cols-2 gap-5 mb-14">
          {pillars.map(p => (
            <div key={p.title} className="rounded-2xl border border-gold/20 bg-gold/[0.04] p-6">
              <p className="text-2xl mb-3">{p.icon}</p>
              <h3 className="font-semibold text-foreground mb-2">{p.title}</h3>
              <p className="text-sm text-muted-foreground leading-6">{p.body}</p>
            </div>
          ))}
        </div>

        <div className="rounded-2xl border border-gold/20 bg-gold/[0.04] p-8 mb-14">
          <h2 className="text-2xl font-playfair font-semibold mb-6 text-center">How The War Room Works</h2>
          <ol className="space-y-5">
            {[
              ["Onboard your birth chart", "Enter your birth details. The engine auto-computes your Jyotish chart, Lal Kitab house positions, and current Dasha lord."],
              ["Gate 0 — Ask Krishna", "Before entering the War Room, you must consult the Krishna Prashnavali. Your answer (YES/WAIT/NO/PRAY) determines your entry path."],
              ["Diagnose all 5 Gates", "Each planetary gate is scored. Weak gates trigger remedy assignments. Strong gates unlock offensive missions."],
              ["Execute daily missions", "Your mission board updates with Dasha-aligned daily actions. Log completions to build your Conquest Score."],
              ["Read your Intelligence Brief", "A weekly Executive Report synthesises your chart, score, gate health, and strategic outlook."],
            ].map(([title, body], i) => (
              <li key={i} className="flex gap-4">
                <span className="w-7 h-7 rounded-full bg-gold/10 border border-gold/30 text-gold font-bold flex items-center justify-center shrink-0 text-sm">{i + 1}</span>
                <div>
                  <p className="font-semibold text-foreground mb-1">{title}</p>
                  <p className="text-sm text-muted-foreground leading-6">{body}</p>
                </div>
              </li>
            ))}
          </ol>
        </div>

        <div className="text-center">
          <h2 className="text-2xl font-playfair font-semibold mb-4">Ready to enter the War Room?</h2>
          <p className="text-muted-foreground text-sm mb-6">Build your Conquest Score. Unlock premium intelligence. Dominate your Dasha.</p>
          <button onClick={() => navigate('/register')} className="inline-flex items-center gap-2 rounded-xl bg-gold px-8 py-4 text-base font-semibold text-stone-950 hover:bg-gold/90 transition">
            Create Free Account →
          </button>
          <p className="mt-3 text-xs text-muted-foreground">Already registered? <button onClick={() => navigate('/login')} className="text-gold underline">Sign in</button></p>
        </div>
      </div>
    </div>
  );
}

export default function StrategistPage() {
  const { user, loading: authLoading } = useAuth();
  const locationSlug = localStorage.getItem('lk_location_slug') || 'new-delhi';

  if (authLoading) return null;

  // Logged-out → public landing (indexed by Google)
  if (!user) return <StrategistLanding />;

  // Logged-in, not premium → premium gate
  if (!user.is_premium) return (
    <PremiumGateCard
      feature="The Strategist"
      description="The Vedic Business War Room — KP oracle, LK diagnostics, Missions, and Conquest Score — is an exclusive Premium feature. Upgrade to activate your war room."
    />
  );

  // Premium → full dashboard
  return (
    <WarRoomStateProvider locationSlug={locationSlug}>
      <SEO title="The Strategist — War Room" noindex={true} />
      <Dashboard />
    </WarRoomStateProvider>
  );
}
