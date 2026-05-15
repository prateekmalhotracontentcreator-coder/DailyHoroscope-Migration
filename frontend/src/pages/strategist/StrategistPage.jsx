import { SEO } from '../../components/SEO';
import { PremiumGateCard } from '../../components/PremiumRoute';
import React, { useEffect, useRef, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ArrowRight, ChevronDown } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { WarRoomStateProvider, useWarRoom } from '../../components/WarRoomStateProvider';
import ConquestGauge from '../../components/ConquestGauge';
import HurdleAlert from '../../components/HurdleAlert';
import KrishnaOracleGrid from '../../components/KrishnaOracleGrid';

const BACKEND = process.env.REACT_APP_BACKEND_URL || '';
const SEVEN_DAYS_MS = 7 * 24 * 60 * 60 * 1000;
const LOGIN_REDIRECT = { state: { from: { pathname: '/strategist' } } };

const LAYERS = [
  {
    id: 'layer-0',
    n: 0,
    short: 'Oracle',
    title: 'Gate 0 -- Krishna Prashnavali Oracle',
    tagline: 'Ask Krishna before any campaign. One verdict determines the day's route into the War Room.',
    icon: '⚔️',
  },
  {
    id: 'layer-1',
    n: 1,
    short: 'Astrology',
    title: 'Astrology Engine',
    tagline: 'Birth-chart timing, command planet, and dasha weather form your strategic operating system.',
    icon: '🪐',
  },
  {
    id: 'layer-2',
    n: 2,
    short: 'LK Scan',
    title: 'Lal Kitab 5-Gate Diagnosis',
    tagline: 'Debt, dormant houses, Mercury collisions, and geographic alignment stay visible in one strip.',
    icon: '🜂',
  },
  {
    id: 'layer-3',
    n: 3,
    short: 'Missions',
    title: 'Strategist Engine + Hurdles',
    tagline: 'Mission triggers, hurdle alerts, and surrogate pivots surface only when the path is ready.',
    icon: '🎯',
  },
  {
    id: 'layer-4',
    n: 4,
    short: 'Action Plan',
    title: '43-Day Remedy Roadmap',
    tagline: 'Your streak, debt clearance, and next threshold become an execution board instead of static data.',
    icon: '📿',
  },
  {
    id: 'layer-5',
    n: 5,
    short: 'Report',
    title: 'Executive Intelligence Brief',
    tagline: 'A premium output layer for the user who wants the whole battle plan in one polished brief.',
    icon: '📜',
  },
];

const GATE_ZERO_PATHS = [
  { verdict: 'YES', icon: '✅', title: 'War Room unlocked', body: 'Path is clear. Missions, action plans, and the report layer stay fully active.' },
  { verdict: 'WAIT', icon: '⏳', title: 'Pre-Flight Mode', body: 'Rituals and LK tracker work take priority until the War Room clears itself.' },
  { verdict: 'NO', icon: '🛑', title: 'Score to 60%', body: 'Conquest Probability must rise above the re-test threshold before a new oracle pass.' },
  { verdict: 'PRAY', icon: '🙏', title: 'Full Surrender', body: 'Purple-path remedies, mantra work, and debt audit lead the recovery route.' },
];

const SCORE_BANDS = [
  { range: '85-99%', title: 'Sovereign Dominance', body: 'Expansion / All-In', tone: 'border-emerald-500/35 bg-emerald-500/10 text-emerald-300' },
  { range: '60-84%', title: 'Operational Friction', body: 'Patch & Pivot', tone: 'border-amber-500/35 bg-amber-500/10 text-amber-300' },
  { range: '40-59%', title: 'Strategic Siege', body: 'Hold Ground / Remedy', tone: 'border-orange-500/35 bg-orange-500/10 text-orange-300' },
  { range: '0-39%', title: 'Karmic Lockdown', body: 'Withdraw / Full Reset', tone: 'border-red-500/35 bg-red-500/10 text-red-300' },
];

const WAR_ROOM_CONFIG = {
  OFFENSIVE_GOLD: {
    label: '⚔️ OFFENSIVE -- RITUALS OPEN',
    kicker: 'Expansion window live',
    shell: 'border-gold/30 bg-gradient-to-br from-gold/20 via-gold/8 to-transparent',
    chip: 'border-gold/30 bg-gold/12 text-gold',
  },
  GOLDEN_HOUR: {
    label: '🌅 GOLDEN HOUR -- ACT NOW',
    kicker: '30-minute execution window',
    shell: 'border-orange-400/45 bg-gradient-to-br from-orange-500/30 via-red-500/20 to-transparent strategist-signal-pulse',
    chip: 'border-orange-400/35 bg-orange-500/12 text-orange-200',
  },
  DEFENSIVE_MIDNIGHT: {
    label: '🌙 DEFENSIVE -- RITUALS LOCKED',
    kicker: 'Night protocol active',
    shell: 'border-slate-700/70 bg-gradient-to-br from-slate-950 via-slate-900/95 to-[#08111f]',
    chip: 'border-slate-700/70 bg-slate-800/70 text-slate-200',
  },
};

function StrategistStarField({ opacity = 0.6 }) {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return undefined;

    const context = canvas.getContext('2d');
    let frameId = 0;

    const resize = () => {
      canvas.width = canvas.offsetWidth;
      canvas.height = canvas.offsetHeight;
    };

    resize();
    window.addEventListener('resize', resize);

    const stars = Array.from({ length: 120 }, () => ({
      x: Math.random(),
      y: Math.random(),
      radius: Math.random() * 1.5 + 0.25,
      speed: Math.random() * 0.008 + 0.002,
      phase: Math.random() * Math.PI * 2,
    }));

    const draw = (time) => {
      context.clearRect(0, 0, canvas.width, canvas.height);
      stars.forEach((star) => {
        const alpha = 0.24 + 0.72 * Math.abs(Math.sin(time * star.speed + star.phase));
        context.beginPath();
        context.arc(star.x * canvas.width, star.y * canvas.height, star.radius, 0, Math.PI * 2);
        context.fillStyle = `rgba(197,160,89,${alpha * opacity})`;
        context.fill();
      });
      frameId = requestAnimationFrame(draw);
    };

    frameId = requestAnimationFrame(draw);

    return () => {
      cancelAnimationFrame(frameId);
      window.removeEventListener('resize', resize);
    };
  }, [opacity]);

  return <canvas ref={canvasRef} className="pointer-events-none absolute inset-0 h-full w-full" />;
}

function LayerPill({ layer, status, onClick }) {
  const styles = {
    active: 'border-gold/50 bg-gold/15 text-gold shadow-[0_14px_40px_rgba(197,160,89,0.16)]',
    locked: 'border-white/10 bg-white/[0.03] text-muted-foreground',
    complete: 'border-emerald-500/35 bg-emerald-500/12 text-emerald-300',
    blocked: 'border-red-500/35 bg-red-500/12 text-red-300',
  };
  const statusIcon = status === 'locked' ? '🔒' : status === 'complete' ? '✓' : status === 'blocked' ? '⛔' : layer.icon;

  return (
    <button
      type="button"
      onClick={() => onClick(layer.id)}
      className={`inline-flex min-w-[78px] items-center justify-center gap-2 rounded-full border px-3 py-2 text-xs font-semibold transition hover:-translate-y-0.5 ${styles[status] || styles.locked}`}
    >
      <span className="text-sm leading-none">{statusIcon}</span>
      <span className="font-mono text-[10px] tracking-[0.2em] text-current/70">L{layer.n}</span>
      <span className="hidden sm:inline">{layer.short}</span>
    </button>
  );
}

function LayerSection({ layer, children, action, muted = false }) {
  return (
    <section id={layer.id} className={`scroll-mt-32 rounded-[30px] border p-6 sm:p-8 ${muted ? 'border-white/8 bg-white/[0.02]' : 'border-gold/15 bg-card/90 shadow-[0_25px_90px_rgba(2,6,23,0.18)]'}`}>
      <div className="mb-6 flex flex-wrap items-start justify-between gap-4">
        <div className="max-w-3xl">
          <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-gold/25 bg-gold/[0.06] px-3 py-1 text-[11px] uppercase tracking-[0.24em] text-gold">
            <span>{layer.icon}</span>
            <span>Layer {layer.n}</span>
          </div>
          <h2 className="text-2xl font-cinzel text-foreground sm:text-3xl">{layer.title}</h2>
          <p className="mt-2 max-w-3xl text-sm leading-7 text-muted-foreground sm:text-base">{layer.tagline}</p>
        </div>
        {action}
      </div>
      {children}
    </section>
  );
}

function Gate0Panel({ onVerdict }) {
  const [gridMatrix, setGridMatrix] = useState([]);
  const [loadingGrid, setLoadingGrid] = useState(true);
  const [selectedIndex, setSelectedIndex] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    let mounted = true;

    fetch(`${BACKEND}/api/oracle/krishna-prashnavali/meta`, { credentials: 'include' })
      .then((response) => response.json())
      .then((data) => {
        if (!mounted) return;
        setGridMatrix(data.grid_matrix || []);
      })
      .catch(() => {
        if (!mounted) return;
        setError('Unable to load Oracle grid.');
      })
      .finally(() => {
        if (mounted) setLoadingGrid(false);
      });

    return () => {
      mounted = false;
    };
  }, []);

  async function handleCellSelect({ row, col, index }) {
    setSelectedIndex(index);
    setSubmitting(true);
    setError('');

    try {
      const response = await fetch(`${BACKEND}/api/strategist/gate0/select`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ row, col }),
      });
      const data = await response.json();
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
    <div className="rounded-[26px] border border-gold/20 bg-[#0c1524]/92 p-5 shadow-[0_22px_60px_rgba(2,6,23,0.22)] sm:p-6">
      <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="text-[11px] uppercase tracking-[0.28em] text-gold/70">Gate 0 Clearance</p>
          <p className="mt-1 text-xl font-cinzel text-foreground">Consult Krishna Before You Commit</p>
        </div>
        <Link to="/krishna-prashnavali" className="inline-flex items-center gap-2 rounded-full border border-gold/20 bg-gold/[0.05] px-4 py-2 text-xs font-semibold text-gold transition hover:bg-gold/[0.12]">
          Full Oracle <ArrowRight className="h-3.5 w-3.5" />
        </Link>
      </div>

      <p className="mb-4 max-w-3xl text-sm leading-7 text-muted-foreground">
        Touch one cell. The answer routes today's strategist state into YES, WAIT, NO, or PRAY.
      </p>

      {error ? <p className="mb-4 rounded-2xl border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-300">{error}</p> : null}

      {loadingGrid ? (
        <div className="rounded-2xl border border-white/8 bg-white/[0.03] px-4 py-10 text-center text-sm text-muted-foreground">
          Loading Oracle grid...
        </div>
      ) : (
        <div className="overflow-x-auto rounded-2xl border border-white/8 bg-black/10 p-3">
          <KrishnaOracleGrid
            gridMatrix={gridMatrix}
            selectedIndex={selectedIndex}
            disabled={submitting}
            revealEnabled={false}
            onSelect={handleCellSelect}
          />
        </div>
      )}

      {submitting ? <p className="mt-4 text-center text-sm font-medium text-gold">Reading Oracle...</p> : null}
    </div>
  );
}

function VerdictBanner({ verdict, reading }) {
  const configs = {
    YES: {
      shell: 'border-emerald-500/35 bg-emerald-500/10 text-emerald-200',
      heading: '✅ YES -- Path is Clear',
      body: reading?.answer?.meaning?.english_block || 'The path is favorable. Proceed with your strategic mission.',
    },
    WAIT: {
      shell: 'border-orange-500/35 bg-orange-500/10 text-orange-200',
      heading: '⏳ WAIT -- Pre-Flight Mode',
      body: reading?.answer?.meaning?.english_block || 'Patience is required. Build your remedy rhythm, then re-enter.',
    },
    NO: {
      shell: 'border-red-500/35 bg-red-500/10 text-red-200',
      heading: '🛑 NO -- Strategic Realignment Required',
      body: reading?.answer?.meaning?.english_block || 'Resistance is active. Raise your conquest score before a re-test.',
    },
    PRAY: {
      shell: 'border-purple-500/35 bg-purple-500/10 text-purple-200',
      heading: '🙏 PRAY -- Full Surrender Path',
      body: reading?.answer?.meaning?.english_block || 'Krishna calls you inward first. Complete mantra and debt work before the next mission.',
    },
  };
  const config = configs[verdict] || configs.WAIT;

  return (
    <div className={`rounded-[24px] border p-5 ${config.shell}`}>
      <p className="text-lg font-semibold">{config.heading}</p>
      <p className="mt-2 text-sm leading-7 text-current/80">{config.body}</p>
    </div>
  );
}

function PraySurrenderPanel() {
  const [context, setContext] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let mounted = true;

    fetch(`${BACKEND}/api/strategist/surrender-context`, { credentials: 'include' })
      .then((response) => response.json())
      .then((data) => {
        if (mounted) setContext(data);
      })
      .catch(() => {
        if (mounted) setContext(null);
      })
      .finally(() => {
        if (mounted) setLoading(false);
      });

    return () => {
      mounted = false;
    };
  }, []);

  const score = context?.conquest_score ?? null;
  const pointsTo75 = context?.points_to_75 ?? null;
  const percent = score != null ? Math.min(100, Math.round((score / 75) * 100)) : 0;

  return (
    <div className="rounded-[26px] border border-purple-500/35 bg-[linear-gradient(135deg,rgba(88,28,135,0.34),rgba(30,27,75,0.52))] p-5 shadow-[0_18px_50px_rgba(76,29,149,0.18)]">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div className="max-w-2xl">
          <p className="text-[11px] uppercase tracking-[0.28em] text-purple-300/90">PRAY Verdict Active</p>
          <h3 className="mt-2 text-2xl font-cinzel text-purple-50">Full Surrender Path</h3>
          <p className="mt-2 text-sm leading-7 text-purple-100/80">
            Krishna calls you inward before any outward campaign. Mantra work, debt clearance, and surrender steps remain the priority until 75%.
          </p>
        </div>
        <div className="rounded-full border border-purple-400/30 bg-purple-500/10 px-4 py-2 text-xs font-semibold text-purple-100">
          Threshold: 75%
        </div>
      </div>

      {score != null ? (
        <div className="mt-5 rounded-2xl border border-purple-400/20 bg-black/10 p-4">
          <div className="mb-2 flex items-center justify-between gap-3 text-xs text-purple-100/70">
            <span>Conquest score</span>
            <span>{pointsTo75} pts to re-test</span>
          </div>
          <div className="flex items-end gap-4">
            <p className="text-4xl font-bold text-purple-50">{score}%</p>
            <div className="flex-1 pb-2">
              <div className="h-2 overflow-hidden rounded-full bg-purple-950/50">
                <div className="h-full rounded-full bg-gradient-to-r from-purple-500 via-fuchsia-400 to-pink-300 transition-all duration-500" style={{ width: `${percent}%` }} />
              </div>
            </div>
          </div>
        </div>
      ) : null}

      {!loading && context?.featured_mantra ? (
        <div className="mt-5 rounded-2xl border border-purple-400/20 bg-purple-950/20 p-4">
          <p className="text-[11px] uppercase tracking-[0.24em] text-purple-200/80">
            Featured Mantra -- {context.featured_mantra.deity || context.featured_mantra.remedy_area}
          </p>
          <p className="mt-3 text-xl text-purple-50">{context.featured_mantra.mantra_devanagari}</p>
          <p className="mt-1 text-sm italic text-purple-200/85">{context.featured_mantra.mantra_transliteration}</p>
          {context.featured_mantra.guidance ? (
            <p className="mt-3 text-sm leading-7 text-purple-100/75">{context.featured_mantra.guidance}</p>
          ) : null}
        </div>
      ) : null}

      {context?.gate1_narrative ? (
        <div className="mt-5 rounded-2xl border border-amber-500/25 bg-amber-500/[0.08] p-4">
          <p className="text-[11px] uppercase tracking-[0.24em] text-amber-300">Karmic Debt Status</p>
          <p className="mt-2 text-sm leading-7 text-amber-50/80">{context.gate1_narrative}</p>
        </div>
      ) : null}

      {context?.surrender_steps?.length ? (
        <div className="mt-5 grid gap-3 md:grid-cols-3">
          {context.surrender_steps.slice(0, 3).map((step, index) => (
            <div key={`${step}-${index}`} className="rounded-2xl border border-white/8 bg-white/[0.03] p-4">
              <p className="text-[11px] uppercase tracking-[0.22em] text-purple-200/70">Step {index + 1}</p>
              <p className="mt-2 text-sm leading-7 text-purple-50/80">{step}</p>
            </div>
          ))}
        </div>
      ) : null}

      <div className="mt-5 flex flex-wrap gap-3">
        <Link to="/mantra-remedies" className="inline-flex items-center gap-2 rounded-full border border-purple-400/30 bg-purple-400/12 px-4 py-2 text-sm font-semibold text-purple-50 transition hover:bg-purple-400/20">
          Mantra Remedies <ArrowRight className="h-4 w-4" />
        </Link>
        <Link to="/lk-remedies/debt-audit" className="inline-flex items-center gap-2 rounded-full border border-amber-400/30 bg-amber-400/12 px-4 py-2 text-sm font-semibold text-amber-100 transition hover:bg-amber-400/20">
          LK Debt Audit <ArrowRight className="h-4 w-4" />
        </Link>
      </div>
    </div>
  );
}

function PreFlightPanel({ gateStatus, conquestScore }) {
  if (gateStatus === 'pray_blocked') return <PraySurrenderPanel />;

  if (gateStatus === 'wait_active') {
    return (
      <div className="rounded-[26px] border border-orange-500/35 bg-[linear-gradient(135deg,rgba(249,115,22,0.18),rgba(124,45,18,0.26))] p-5">
        <p className="text-[11px] uppercase tracking-[0.28em] text-orange-200/80">WAIT Verdict</p>
        <h3 className="mt-2 text-2xl font-cinzel text-orange-50">Pre-Flight Mode</h3>
        <p className="mt-2 max-w-2xl text-sm leading-7 text-orange-100/80">
          Oracle asks for patience first. Build your LK rhythm and the War Room auto-unlocks once the remedy sequence stabilizes.
        </p>
        <div className="mt-4 flex flex-wrap gap-3">
          <Link to="/lk-remedies/tracker" className="inline-flex items-center gap-2 rounded-full border border-orange-400/35 bg-orange-400/12 px-4 py-2 text-sm font-semibold text-orange-50 transition hover:bg-orange-400/20">
            Start LK Tracker <ArrowRight className="h-4 w-4" />
          </Link>
        </div>
      </div>
    );
  }

  if (gateStatus === 'no_blocked') {
    const progress = conquestScore != null ? Math.min(100, Math.round((conquestScore / 60) * 100)) : 0;

    return (
      <div className="rounded-[26px] border border-red-500/35 bg-[linear-gradient(135deg,rgba(153,27,27,0.28),rgba(69,10,10,0.34))] p-5">
        <p className="text-[11px] uppercase tracking-[0.28em] text-red-200/80">NO Verdict</p>
        <h3 className="mt-2 text-2xl font-cinzel text-red-50">Conquest Score Required -- 60%+</h3>
        <p className="mt-2 max-w-2xl text-sm leading-7 text-red-100/78">
          Resistance is active. Raise your remedy score, repair momentum, and re-test at Gate 0 once the threshold clears.
        </p>

        <div className="mt-5 rounded-2xl border border-red-500/20 bg-black/10 p-4">
          <div className="mb-2 flex items-center justify-between gap-3 text-xs text-red-100/70">
            <span>Current score</span>
            <span>Target: 60%</span>
          </div>
          <div className="flex items-end gap-4">
            <p className="text-4xl font-bold text-red-50">{conquestScore ?? '--'}%</p>
            <div className="flex-1 pb-2">
              <div className="h-2 overflow-hidden rounded-full bg-red-950/50">
                <div className="h-full rounded-full bg-gradient-to-r from-red-600 via-orange-500 to-amber-400 transition-all duration-500" style={{ width: `${progress}%` }} />
              </div>
            </div>
          </div>
        </div>

        <div className="mt-4 flex flex-wrap gap-3">
          <Link to="/lk-remedies/remedies" className="inline-flex items-center gap-2 rounded-full border border-red-400/30 bg-red-400/12 px-4 py-2 text-sm font-semibold text-red-50 transition hover:bg-red-400/20">
            Browse Remedies <ArrowRight className="h-4 w-4" />
          </Link>
          <Link to="/lk-remedies/tracker" className="inline-flex items-center gap-2 rounded-full border border-gold/30 bg-gold/12 px-4 py-2 text-sm font-semibold text-gold transition hover:bg-gold/20">
            LK Tracker <ArrowRight className="h-4 w-4" />
          </Link>
        </div>
      </div>
    );
  }

  return null;
}

function Scoreboard({ sb }) {
  const progress = sb.next_threshold ? Math.min(100, Math.round((sb.conquest_score / sb.next_threshold) * 100)) : 100;
  const verdictStyles = {
    YES: 'border-emerald-500/35 bg-emerald-500/10 text-emerald-300',
    WAIT: 'border-orange-500/35 bg-orange-500/10 text-orange-300',
    NO: 'border-red-500/35 bg-red-500/10 text-red-300',
    PRAY: 'border-purple-500/35 bg-purple-500/10 text-purple-300',
  };

  return (
    <div className="grid gap-5 lg:grid-cols-[1.2fr_0.8fr]">
      <div className="rounded-[26px] border border-gold/20 bg-[#0c1422]/92 p-5">
        <p className="text-[11px] uppercase tracking-[0.3em] text-gold/70">Success & Debt Scoreboard</p>
        <div className="mt-4 flex flex-wrap items-end justify-between gap-4">
          <div>
            <p className="text-5xl font-bold text-gold sm:text-6xl">{sb.conquest_score}%</p>
            <p className="mt-2 text-base text-foreground">{sb.score_tier}</p>
            <p className="text-sm text-muted-foreground">{sb.score_directive}</p>
          </div>
          <div className="rounded-2xl border border-white/8 bg-white/[0.03] px-5 py-4 text-right">
            <p className="text-[11px] uppercase tracking-[0.24em] text-muted-foreground">Ritual Streak</p>
            <p className="mt-2 text-4xl font-bold text-emerald-300">
              {sb.streak_days}
              <span className="ml-2 text-2xl">{sb.streak_days >= 7 ? '🔥' : 'd'}</span>
            </p>
            <p className="mt-1 text-sm text-muted-foreground">{sb.streak_tier}</p>
          </div>
        </div>

        {sb.next_threshold ? (
          <div className="mt-5">
            <div className="mb-2 flex items-center justify-between gap-3 text-xs text-muted-foreground">
              <span>Progress to {sb.next_threshold_label}</span>
              <span>{sb.points_to_next} pts remaining</span>
            </div>
            <div className="h-3 overflow-hidden rounded-full bg-gold/10">
              <div className="h-full rounded-full bg-gradient-to-r from-gold/60 via-gold/80 to-gold transition-all duration-500" style={{ width: `${progress}%` }} />
            </div>
          </div>
        ) : null}
      </div>

      <div className="grid gap-4">
        <div className="rounded-[24px] border border-white/8 bg-white/[0.03] p-4">
          <p className="text-[11px] uppercase tracking-[0.24em] text-muted-foreground">Karmic Debt</p>
          <div className={`mt-3 inline-flex rounded-full border px-3 py-1.5 text-sm font-semibold ${sb.karmic_debt_cleared ? 'border-emerald-500/30 bg-emerald-500/10 text-emerald-300' : 'border-amber-500/30 bg-amber-500/10 text-amber-300'}`}>
            {sb.karmic_debt_cleared ? 'Cleared ✓' : 'Active ⚠'}
          </div>
        </div>

        <div className="rounded-[24px] border border-white/8 bg-white/[0.03] p-4">
          <p className="text-[11px] uppercase tracking-[0.24em] text-muted-foreground">Last Gate 0</p>
          {sb.gate0_last_verdict ? (
            <>
              <div className={`mt-3 inline-flex rounded-full border px-3 py-1.5 text-sm font-semibold ${verdictStyles[sb.gate0_last_verdict] || 'border-white/10 bg-white/[0.04] text-foreground'}`}>
                {sb.gate0_last_verdict}
              </div>
              <p className="mt-2 text-sm text-muted-foreground">
                {sb.gate0_days_since === 0 ? 'Today' : `${sb.gate0_days_since}d ago`}
              </p>
            </>
          ) : (
            <p className="mt-3 text-sm text-muted-foreground">No strategist oracle verdict logged yet.</p>
          )}
        </div>
      </div>
    </div>
  );
}

function OnboardingRequired() {
  const steps = [
    {
      n: 1,
      title: 'Complete LK Onboarding',
      desc: 'Enter birth details, family census, and office location. This powers your natal chart and Digbala direction.',
      to: '/lk-remedies/onboard',
      cta: 'Start Onboarding',
      tone: 'border-gold/30 bg-gold/[0.08]',
    },
    {
      n: 2,
      title: 'Run the 5-Gate Diagnosis',
      desc: 'Audit karmic debt, dormant houses, Mercury collisions, and your active cycle.',
      to: '/lk-remedies/report',
      cta: 'Run Diagnosis',
      tone: 'border-amber-500/30 bg-amber-500/[0.08]',
    },
    {
      n: 3,
      title: 'Return to the War Room',
      desc: 'Once the chart and diagnosis exist, strategist missions, score, and timing load automatically.',
      to: null,
      cta: null,
      tone: 'border-emerald-500/25 bg-emerald-500/[0.06]',
    },
  ];

  return (
    <div className="rounded-[26px] border border-gold/20 bg-[#0c1422]/92 p-5">
      <p className="text-[11px] uppercase tracking-[0.28em] text-gold/70">War Room Setup Required</p>
      <h3 className="mt-2 text-2xl font-cinzel text-foreground">Astrology Engine Needs Your Profile</h3>
      <p className="mt-2 max-w-2xl text-sm leading-7 text-muted-foreground">
        Strategist stays visual-first, but the chart and LK engine still need your setup data before the live panels can activate.
      </p>

      <div className="mt-5 grid gap-3 md:grid-cols-3">
        {steps.map((step) => (
          <div key={step.n} className={`rounded-2xl border p-4 ${step.tone}`}>
            <p className="text-[11px] uppercase tracking-[0.22em] text-gold/80">Step {step.n}</p>
            <p className="mt-2 text-lg font-semibold text-foreground">{step.title}</p>
            <p className="mt-2 text-sm leading-7 text-muted-foreground">{step.desc}</p>
            {step.cta ? (
              <Link to={step.to} className="mt-4 inline-flex items-center gap-2 text-sm font-semibold text-gold transition hover:text-gold/85">
                {step.cta} <ArrowRight className="h-4 w-4" />
              </Link>
            ) : null}
          </div>
        ))}
      </div>
    </div>
  );
}

function AstrologyStrip({ data }) {
  if (!data) return null;
  if (!data.command_planet) return <OnboardingRequired />;

  const cards = [
    { label: 'Command Planet', value: data.command_planet || '--' },
    { label: 'Power Direction', value: data.success_direction || '--' },
    { label: 'Current Dasha', value: data.mahadasha || '--' },
    { label: 'Antardasha', value: data.antardasha || '--' },
  ];

  return (
    <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
      {cards.map((card) => (
        <div key={card.label} className="rounded-[24px] border border-gold/15 bg-[#0c1422]/92 p-5">
          <p className="text-[11px] uppercase tracking-[0.24em] text-muted-foreground">{card.label}</p>
          <p className="mt-3 text-2xl font-semibold text-foreground">{card.value}</p>
        </div>
      ))}
    </div>
  );
}

function LKGateStatus({ gates }) {
  if (!gates?.length) return null;

  return (
    <div className="grid gap-4 lg:grid-cols-2">
      {gates.map((gate) => {
        const isWarning = ['WARNING', 'DORMANT', 'RAHU_COLLISION', 'EMPTY_VESSEL'].includes(gate.status);
        const isClear = ['CLEAR', 'ACTIVE'].includes(gate.status);
        const tone = isWarning
          ? 'border-amber-500/30 bg-amber-500/[0.08]'
          : isClear
            ? 'border-emerald-500/25 bg-emerald-500/[0.06]'
            : 'border-white/8 bg-white/[0.03]';

        return (
          <div key={gate.gate} className={`rounded-[24px] border p-5 ${tone}`}>
            <div className="flex items-center justify-between gap-3">
              <p className="text-lg font-semibold text-foreground">Gate {gate.gate} -- {gate.name}</p>
              <div className={`h-2.5 w-2.5 rounded-full ${isWarning ? 'bg-amber-400' : isClear ? 'bg-emerald-400' : 'bg-muted-foreground'}`} />
            </div>
            <p className="mt-3 text-sm leading-7 text-muted-foreground">{gate.narrative}</p>
          </div>
        );
      })}
    </div>
  );
}

function MissionQuickLinks({ data }) {
  const links = [
    { to: '/strategist/missions', label: 'Mission Board', sub: 'View all active missions', accent: 'border-gold/25 bg-gold/[0.06]' },
    { to: '/lk-remedies/tracker', label: 'LK Tracker', sub: `Day ${data.ritual_streak ?? 0} ritual log`, accent: 'border-amber-500/25 bg-amber-500/[0.08]' },
    { to: '/strategist/surrogate', label: 'Surrogate Bridge', sub: 'Activate missing-relative workaround', accent: 'border-white/10 bg-white/[0.03]' },
    { to: '/strategist/action-plan', label: '43-Day Action Plan', sub: 'Open the remedy roadmap', accent: 'border-gold/30 bg-gradient-to-br from-gold/12 to-gold/[0.03]' },
  ];

  return (
    <div className="space-y-5">
      <div className="grid gap-4 md:grid-cols-2">
        <div className="rounded-[24px] border border-gold/20 bg-[#0c1422]/92 p-5">
          <p className="text-[11px] uppercase tracking-[0.24em] text-muted-foreground">Active Missions</p>
          <p className="mt-3 text-5xl font-bold text-gold">{data.active_missions_count ?? '--'}</p>
        </div>
        <div className="rounded-[24px] border border-emerald-500/20 bg-emerald-500/[0.06] p-5">
          <p className="text-[11px] uppercase tracking-[0.24em] text-emerald-100/75">Ritual Streak</p>
          <p className="mt-3 text-5xl font-bold text-emerald-300">{data.ritual_streak ?? 0}</p>
        </div>
      </div>

      <div className="grid gap-3">
        {links.map((link) => (
          <Link key={link.to} to={link.to} className={`group flex items-center justify-between rounded-[24px] border p-5 transition hover:-translate-y-0.5 ${link.accent}`}>
            <div>
              <p className="text-lg font-semibold text-foreground">{link.label}</p>
              <p className="mt-1 text-sm text-muted-foreground">{link.sub}</p>
            </div>
            <ArrowRight className="h-5 w-5 text-gold transition group-hover:translate-x-1" />
          </Link>
        ))}
      </div>
    </div>
  );
}

function Layer3Locked() {
  return (
    <div className="rounded-[26px] border border-gold/10 bg-gold/[0.03] p-6 text-center">
      <p className="text-[11px] uppercase tracking-[0.24em] text-muted-foreground">Locked Until Gate 0 Clears</p>
      <p className="mt-2 text-xl font-cinzel text-foreground">Mission Engine Is Standing By</p>
      <p className="mx-auto mt-2 max-w-2xl text-sm leading-7 text-muted-foreground">
        Consult the oracle above to unlock live missions, hurdle alerts, surrogate actions, and the full strategist action rail.
      </p>
    </div>
  );
}

function ActionPlanCard({ missionsUnlocked, gateStatus, conquestScore }) {
  if (!missionsUnlocked) {
    const label = gateStatus === 'pray_blocked'
      ? 'Full surrender rhythm active'
      : gateStatus === 'no_blocked'
        ? `Raise score to 60%${conquestScore != null ? ` from ${conquestScore}%` : ''}`
        : 'Pre-flight sequence active';

    return (
      <div className="rounded-[26px] border border-gold/15 bg-[#0c1422]/92 p-5">
        <p className="text-[11px] uppercase tracking-[0.24em] text-gold/70">43-Day Remedy Rail</p>
        <h3 className="mt-2 text-2xl font-cinzel text-foreground">Action Plan will deepen once Gate 0 clears</h3>
        <p className="mt-2 text-sm leading-7 text-muted-foreground">{label}. LK Tracker, debt audit, and remedies remain the active battlefield for now.</p>
        <div className="mt-4 flex flex-wrap gap-3">
          <Link to="/strategist/action-plan" className="inline-flex items-center gap-2 rounded-full border border-gold/30 bg-gold/12 px-4 py-2 text-sm font-semibold text-gold transition hover:bg-gold/20">
            View 43-Day Roadmap <ArrowRight className="h-4 w-4" />
          </Link>
          <Link to="/lk-remedies/tracker" className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/[0.03] px-4 py-2 text-sm font-semibold text-foreground transition hover:bg-white/[0.06]">
            Open LK Tracker <ArrowRight className="h-4 w-4" />
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="rounded-[26px] border border-gold/20 bg-[#0c1422]/92 p-5">
      <p className="text-[11px] uppercase tracking-[0.24em] text-gold/70">43-Day Remedy Rail</p>
      <h3 className="mt-2 text-2xl font-cinzel text-foreground">Your roadmap is live</h3>
      <p className="mt-2 text-sm leading-7 text-muted-foreground">
        Use the strategist action plan to coordinate ritual momentum, remedy sequencing, and the next conquest threshold.
      </p>
      <div className="mt-4 flex flex-wrap gap-3">
        <Link to="/strategist/action-plan" className="inline-flex items-center gap-2 rounded-full border border-gold/30 bg-gold/12 px-4 py-2 text-sm font-semibold text-gold transition hover:bg-gold/20">
          Open Action Plan <ArrowRight className="h-4 w-4" />
        </Link>
        <Link to="/lk-remedies/tracker" className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/[0.03] px-4 py-2 text-sm font-semibold text-foreground transition hover:bg-white/[0.06]">
          Log Today's Ritual <ArrowRight className="h-4 w-4" />
        </Link>
      </div>
    </div>
  );
}

function ReportLaunchCard({ missionsUnlocked }) {
  return (
    <div className={`rounded-[28px] border p-6 ${missionsUnlocked ? 'border-gold/20 bg-[linear-gradient(135deg,rgba(197,160,89,0.16),rgba(15,23,42,0.52))]' : 'border-white/10 bg-white/[0.03]'}`}>
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div className="max-w-2xl">
          <p className="text-[11px] uppercase tracking-[0.28em] text-gold/70">Premium Output Layer</p>
          <h3 className="mt-2 text-2xl font-cinzel text-foreground">Executive Intelligence Brief</h3>
          <p className="mt-2 text-sm leading-7 text-muted-foreground">
            Conquest Probability, gate verdict, 7-day battle plan, and remedy override logic are bundled into one premium strategist brief.
          </p>
        </div>
        <div className="rounded-full border border-gold/25 bg-gold/[0.08] px-4 py-2 text-xs font-semibold text-gold">
          Premium PDF
        </div>
      </div>

      <div className="mt-5 flex flex-wrap gap-3">
        <Link to="/strategist/report" className="inline-flex items-center gap-2 rounded-full border border-gold/30 bg-gold px-5 py-3 text-sm font-semibold text-stone-950 transition hover:bg-gold/90">
          Open Intelligence Brief <ArrowRight className="h-4 w-4" />
        </Link>
        <Link to="/strategist/missions" className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/[0.03] px-5 py-3 text-sm font-semibold text-foreground transition hover:bg-white/[0.06]">
          Review Mission Board <ArrowRight className="h-4 w-4" />
        </Link>
      </div>

      {!missionsUnlocked ? (
        <p className="mt-4 text-sm text-muted-foreground">
          Gate 0 still governs access quality here. You can enter the report route, but the richest strategist context arrives once the War Room clears.
        </p>
      ) : null}
    </div>
  );
}

function ModuleIntroScreen({ userName, birthDate, commandPlanet, currentDasha, onConsultOracle }) {
  return (
    <div className="relative overflow-hidden rounded-[34px] border border-gold/20 bg-[linear-gradient(140deg,rgba(12,20,34,0.96),rgba(24,16,10,0.92))] p-6 shadow-[0_32px_100px_rgba(2,6,23,0.28)] sm:p-8">
      <div className="pointer-events-none absolute -right-16 top-0 h-44 w-44 rounded-full bg-gold/15 blur-3xl" />
      <div className="pointer-events-none absolute -left-12 bottom-0 h-32 w-32 rounded-full bg-orange-500/10 blur-3xl" />

      <div className="relative">
        <p className="text-[11px] uppercase tracking-[0.34em] text-gold/80">War Room Wake-Up</p>
        <h2 className="mt-3 max-w-4xl text-3xl font-cinzel text-foreground sm:text-4xl">
          Welcome back, {userName} -- Your War Room is Active
        </h2>
        <div className="mt-4 flex flex-wrap gap-3 text-sm text-muted-foreground">
          {birthDate ? <span className="rounded-full border border-white/10 bg-white/[0.03] px-3 py-1.5">{birthDate}</span> : null}
          {commandPlanet ? <span className="rounded-full border border-white/10 bg-white/[0.03] px-3 py-1.5">Command Planet: {commandPlanet}</span> : null}
          {currentDasha ? <span className="rounded-full border border-white/10 bg-white/[0.03] px-3 py-1.5">Current Dasha: {currentDasha}</span> : null}
        </div>
        <p className="mt-5 text-lg italic text-gold/90">"Your Mission Begins"</p>

        <div className="mt-6 flex flex-wrap gap-3">
          {LAYERS.map((layer, index) => (
            <div
              key={layer.id}
              className="strategist-badge-rise rounded-full border border-gold/20 bg-gold/[0.07] px-4 py-2 text-sm text-gold"
              style={{ animationDelay: `${index * 200}ms` }}
            >
              {layer.icon} L{layer.n} · {layer.short}
            </div>
          ))}
        </div>

        <button
          type="button"
          onClick={onConsultOracle}
          className="mt-7 inline-flex items-center gap-2 rounded-full bg-gold px-6 py-3 text-sm font-semibold text-stone-950 transition hover:bg-gold/90"
        >
          Consult the Oracle
          <ChevronDown className="h-4 w-4" />
        </button>
      </div>
    </div>
  );
}

function formatBirthDate(dateValue) {
  if (!dateValue) return '';
  const parsed = new Date(dateValue);
  if (Number.isNaN(parsed.getTime())) return dateValue;
  return parsed.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' });
}

function Dashboard() {
  const { user } = useAuth();
  const { state: warState, countdown } = useWarRoom();
  const sectionRefs = useRef({});
  const [gateStatus, setGateStatus] = useState('loading');
  const [conquestScore, setConquestScore] = useState(null);
  const [freshVerdict, setFreshVerdict] = useState(null);
  const [lastVerdict, setLastVerdict] = useState(null);
  const [dash, setDash] = useState(null);
  const [dashLoading, setDashLoading] = useState(true);
  const [dashError, setDashError] = useState('');
  const [hurdles, setHurdles] = useState([]);
  const [showFactors, setShowFactors] = useState(false);
  const [introDismissed, setIntroDismissed] = useState(false);
  const [welcomeName, setWelcomeName] = useState('Commander');
  const [welcomeBirthDate, setWelcomeBirthDate] = useState('');

  useEffect(() => {
    try {
      const draft = JSON.parse(localStorage.getItem('strategist-profile-draft') || 'null');
      const isValid = draft && (Date.now() - draft.timestamp) < SEVEN_DAYS_MS;
      setWelcomeName(isValid && draft.name ? draft.name : user?.name || 'Commander');
      setWelcomeBirthDate(isValid && draft.dob ? formatBirthDate(draft.dob) : '');
    } catch {
      setWelcomeName(user?.name || 'Commander');
      setWelcomeBirthDate('');
    }
  }, [user]);

  useEffect(() => {
    let mounted = true;

    fetch(`${BACKEND}/api/strategist/gate0/status`, { credentials: 'include' })
      .then((response) => response.json())
      .then((data) => {
        if (!mounted) return;
        setGateStatus(data.status || 'required');
        setConquestScore(data.conquest_score ?? null);
        setLastVerdict(data.last_verdict ?? null);
      })
      .catch(() => {
        if (mounted) setGateStatus('required');
      });

    return () => {
      mounted = false;
    };
  }, []);

  useEffect(() => {
    let mounted = true;

    async function loadDashboard() {
      // If the landing-page form stored birth data in localStorage, persist it to
      // the backend first so _build_war_room_state can compute Vimshottari Dasha.
      try {
        const draft = JSON.parse(localStorage.getItem('strategist-profile-draft') || 'null');
        if (draft?.dob) {
          await fetch(`${BACKEND}/api/strategist/profile`, {
            method: 'POST',
            credentials: 'include',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              dob: draft.dob,
              tob: draft.tob || '',
              city: draft.city || '',
            }),
          });
        }
      } catch {
        // Best-effort -- do not block dashboard if birth-data save fails
      }

      if (!mounted) return;

      try {
        const response = await fetch(`${BACKEND}/api/strategist/dashboard`, { credentials: 'include' });
        const data = await response.json();
        if (!mounted) return;
        if (data.error) throw new Error(data.error);
        setDash(data);
      } catch (error) {
        if (mounted) setDashError(error.message);
      } finally {
        if (mounted) setDashLoading(false);
      }
    }

    loadDashboard();

    return () => {
      mounted = false;
    };
  }, []);

  useEffect(() => {
    let mounted = true;

    fetch(`${BACKEND}/api/strategist/hurdles`, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({}),
    })
      .then((response) => response.json())
      .then((data) => {
        if (mounted) setHurdles(data.hurdles || []);
      })
      .catch(() => {
        if (mounted) setHurdles([]);
      });

    return () => {
      mounted = false;
    };
  }, []);

  useEffect(() => {
    if (dashLoading || !dash) return;
    try {
      const draft = JSON.parse(localStorage.getItem('strategist-profile-draft') || 'null');
      const isValid = draft && (Date.now() - draft.timestamp) < SEVEN_DAYS_MS;
      if (isValid) localStorage.removeItem('strategist-profile-draft');
    } catch {
      // Ignore malformed draft payloads.
    }
  }, [dashLoading, dash]);

  function handleVerdict(verdict, reading) {
    setFreshVerdict({ verdict, reading });
    setLastVerdict(verdict);
    setIntroDismissed(true);

    if (verdict === 'YES') {
      setGateStatus('clear');
      return;
    }
    if (verdict === 'WAIT') {
      setGateStatus('wait_active');
      return;
    }
    if (verdict === 'NO') {
      setGateStatus('no_blocked');
      return;
    }
    setGateStatus('pray_blocked');
  }

  function scrollToSection(sectionId) {
    const node = sectionRefs.current[sectionId];
    if (!node) return;
    node.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  const missionsUnlocked = gateStatus === 'clear';
  const blocked = ['wait_active', 'no_blocked', 'pray_blocked'].includes(gateStatus);
  const needsGate0 = gateStatus === 'required';
  const showIntro = needsGate0 && !lastVerdict && !freshVerdict && !introDismissed;
  const currentDasha = dash?.mahadasha || 'Pending Dasha';
  const warConfig = WAR_ROOM_CONFIG[warState] || WAR_ROOM_CONFIG.OFFENSIVE_GOLD;

  const layerStatus = (layerNumber) => {
    if (layerNumber === 0) return missionsUnlocked ? 'complete' : 'active';
    if (layerNumber === 1 || layerNumber === 2) return dash?.command_planet ? 'complete' : 'active';
    if (layerNumber === 3) return missionsUnlocked ? 'active' : blocked ? 'blocked' : 'locked';
    if (layerNumber === 4 || layerNumber === 5) return missionsUnlocked ? 'active' : 'locked';
    return 'locked';
  };

  return (
    <div className="min-h-screen bg-background text-foreground">
      <style>{`
        .strategist-signal-pulse {
          animation: strategistPulse 1.8s ease-in-out infinite;
        }
        .strategist-badge-rise {
          opacity: 0;
          transform: translateY(16px);
          animation: strategistRise 0.72s ease forwards;
        }
        @keyframes strategistPulse {
          0%, 100% { box-shadow: 0 0 0 rgba(251, 146, 60, 0); }
          50% { box-shadow: 0 0 42px rgba(251, 146, 60, 0.18); }
        }
        @keyframes strategistRise {
          from {
            opacity: 0;
            transform: translateY(16px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      `}</style>

      <div className="relative overflow-hidden border-b border-gold/10 bg-[linear-gradient(180deg,#07111e_0%,#0b1525_62%,rgba(11,21,37,0.84)_100%)]">
        <StrategistStarField opacity={0.55} />
        <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_18%_18%,rgba(197,160,89,0.18),transparent_24%),radial-gradient(circle_at_82%_10%,rgba(249,115,22,0.12),transparent_22%)]" />

        <div className="relative mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8 lg:py-10">
          <div className="flex flex-wrap items-start justify-between gap-5">
            <div className="max-w-3xl">
              <p className="text-[11px] uppercase tracking-[0.34em] text-gold/80">Premium Integrated Vedic Career Mentor</p>
              <h1 className="mt-3 text-4xl font-cinzel text-foreground sm:text-5xl">The Strategist</h1>
              <p className="mt-4 max-w-3xl text-base leading-8 text-white/72">
                Bloomberg Terminal for Karma. Six intelligence layers, one live War Room, and a strategist shell that keeps the current mission state obvious at every step.
              </p>
            </div>
            <Link
              to="/lk-remedies/onboard"
              className="inline-flex items-center gap-2 rounded-full border border-gold/25 bg-gold/[0.08] px-4 py-2 text-sm font-semibold text-gold transition hover:bg-gold/[0.14]"
            >
              Redo Setup <ArrowRight className="h-4 w-4" />
            </Link>
          </div>

          <div className={`mt-8 rounded-[30px] border p-6 sm:p-8 ${warConfig.shell}`}>
            <div className="flex flex-wrap items-center justify-between gap-5">
              <div>
                <div className={`inline-flex items-center gap-2 rounded-full border px-3 py-1.5 text-[11px] uppercase tracking-[0.24em] ${warConfig.chip}`}>
                  <span>{warConfig.kicker}</span>
                </div>
                <p className="mt-4 text-2xl font-cinzel text-foreground sm:text-3xl">{warConfig.label}</p>
              </div>
              <div className="text-left sm:text-right">
                <p className="text-[11px] uppercase tracking-[0.24em] text-muted-foreground">Golden Hour Countdown</p>
                <p className="mt-2 text-4xl font-bold text-foreground sm:text-5xl">{countdown || '00:00:00'}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {warState === 'GOLDEN_HOUR' ? (
        <div className="fixed inset-x-4 bottom-4 z-40 rounded-2xl border border-orange-400/35 bg-[linear-gradient(135deg,rgba(249,115,22,0.92),rgba(220,38,38,0.92))] px-4 py-3 text-sm text-white shadow-[0_25px_60px_rgba(127,29,29,0.34)] md:hidden">
          <div className="flex items-center justify-between gap-3">
            <span className="font-semibold">Golden Hour</span>
            <span className="font-mono text-base">{countdown || '00:00:00'}</span>
          </div>
        </div>
      ) : null}

      <div className="sticky top-0 z-30 border-b border-gold/10 bg-background/80 backdrop-blur-xl">
        <div className="mx-auto flex max-w-7xl gap-2 overflow-x-auto px-4 py-3 sm:px-6 lg:px-8">
          {LAYERS.map((layer) => (
            <LayerPill key={layer.id} layer={layer} status={layerStatus(layer.n)} onClick={scrollToSection} />
          ))}
        </div>
      </div>

      <div className="mx-auto max-w-7xl space-y-6 px-4 py-8 sm:px-6 lg:px-8">
        {dashError ? (
          <div className="rounded-[26px] border border-amber-500/30 bg-amber-500/10 p-5">
            <p className="text-sm text-amber-200">{dashError}</p>
            <Link to="/lk-remedies/onboard" className="mt-3 inline-flex items-center gap-2 text-sm font-semibold text-gold transition hover:text-gold/85">
              Complete LK Onboarding first <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
        ) : null}

        {showIntro ? (
          <ModuleIntroScreen
            userName={welcomeName}
            birthDate={welcomeBirthDate}
            commandPlanet={dash?.command_planet}
            currentDasha={currentDasha}
            onConsultOracle={() => {
              setIntroDismissed(true);
              scrollToSection('layer-0');
            }}
          />
        ) : null}

        <section ref={(node) => { sectionRefs.current['overview'] = node; }} className="grid gap-6 xl:grid-cols-[1.05fr_0.95fr]">
          <div className="rounded-[30px] border border-gold/18 bg-card/90 p-6 sm:p-8">
            <p className="text-[11px] uppercase tracking-[0.28em] text-gold/70">Conquest Probability</p>
            <div className="mt-4 flex justify-center">
              <div className="origin-top scale-[1.45] sm:scale-[1.6]">
                <ConquestGauge {...(dash?.conquest_probability || {})} />
              </div>
            </div>
            <div className="mt-6 flex justify-center">
              <button
                type="button"
                onClick={() => setShowFactors((current) => !current)}
                className="inline-flex items-center gap-2 rounded-full border border-gold/20 bg-gold/[0.05] px-4 py-2 text-sm font-semibold text-gold transition hover:bg-gold/[0.1]"
              >
                How is this calculated?
                <ChevronDown className={`h-4 w-4 transition ${showFactors ? 'rotate-180' : ''}`} />
              </button>
            </div>

            {showFactors && dash?.conquest_probability?.factors?.length ? (
              <div className="mt-5 grid gap-3 md:grid-cols-2">
                {dash.conquest_probability.factors.map((factor) => (
                  <div key={`${factor.factor}-${factor.detail}`} className="rounded-2xl border border-white/8 bg-white/[0.03] p-4">
                    <div className="flex items-center justify-between gap-3">
                      <p className="text-sm font-semibold text-foreground">{factor.factor.replaceAll('_', ' ')}</p>
                      <span className={`text-sm font-semibold ${factor.delta >= 0 ? 'text-emerald-300' : 'text-red-300'}`}>
                        {factor.delta >= 0 ? `+${factor.delta}` : factor.delta}
                      </span>
                    </div>
                    <p className="mt-2 text-sm leading-7 text-muted-foreground">{factor.detail}</p>
                  </div>
                ))}
              </div>
            ) : null}
          </div>

          <div className="grid gap-4">
            {SCORE_BANDS.map((band) => (
              <div key={band.title} className={`rounded-[24px] border p-4 ${band.tone}`}>
                <p className="text-[11px] uppercase tracking-[0.24em]">{band.range}</p>
                <p className="mt-2 text-lg font-semibold">{band.title}</p>
                <p className="mt-1 text-sm opacity-80">{band.body}</p>
              </div>
            ))}
          </div>
        </section>

        <div ref={(node) => { sectionRefs.current['layer-0'] = node; }}>
          <LayerSection layer={LAYERS[0]}>
            <div className="space-y-5">
              {gateStatus === 'loading' ? (
                <div className="rounded-2xl border border-white/8 bg-white/[0.03] px-4 py-10 text-center text-sm text-muted-foreground">
                  Checking Oracle clearance...
                </div>
              ) : null}

              {needsGate0 ? (
                <>
                  {lastVerdict ? (
                    <div className="rounded-2xl border border-gold/20 bg-gold/[0.04] px-4 py-4 text-sm text-muted-foreground">
                      Previous verdict: <span className="font-semibold text-gold">{lastVerdict}</span>. Your score now qualifies you for a fresh strategist re-test.
                    </div>
                  ) : null}
                  <Gate0Panel onVerdict={handleVerdict} />
                </>
              ) : null}

              {missionsUnlocked && lastVerdict ? (
                <div className="rounded-2xl border border-emerald-500/30 bg-emerald-500/[0.07] px-4 py-4 text-sm text-emerald-100">
                  Gate 0 cleared. Oracle verdict: <span className="font-semibold text-emerald-300">{lastVerdict}</span>.
                </div>
              ) : null}

              {freshVerdict && !needsGate0 ? <VerdictBanner verdict={freshVerdict.verdict} reading={freshVerdict.reading} /> : null}
              {blocked ? <PreFlightPanel gateStatus={gateStatus} conquestScore={conquestScore} /> : null}

              <div className="grid gap-4 md:grid-cols-2">
                {GATE_ZERO_PATHS.map((path) => (
                  <div key={path.verdict} className="rounded-[24px] border border-white/8 bg-white/[0.03] p-4">
                    <p className="text-lg font-semibold text-foreground">{path.icon} {path.verdict}</p>
                    <p className="mt-2 text-sm text-foreground">{path.title}</p>
                    <p className="mt-1 text-sm leading-7 text-muted-foreground">{path.body}</p>
                  </div>
                ))}
              </div>
            </div>
          </LayerSection>
        </div>

        <div ref={(node) => { sectionRefs.current['layer-1'] = node; }}>
          <LayerSection layer={LAYERS[1]}>
            {dashLoading ? (
              <div className="rounded-2xl border border-white/8 bg-white/[0.03] px-4 py-10 text-center text-sm text-muted-foreground">
                Loading War Room data...
              </div>
            ) : dash ? (
              <AstrologyStrip data={dash} />
            ) : (
              <AstrologyStrip data={null} />
            )}
          </LayerSection>
        </div>

        <div ref={(node) => { sectionRefs.current['layer-2'] = node; }}>
          <LayerSection layer={LAYERS[2]} action={<Link to="/lk-remedies/report" className="inline-flex items-center gap-2 text-sm font-semibold text-gold transition hover:text-gold/85">Full Report <ArrowRight className="h-4 w-4" /></Link>}>
            {dash?.gate_summaries?.length ? (
              <LKGateStatus gates={dash.gate_summaries} />
            ) : (
              <div className="rounded-2xl border border-white/8 bg-white/[0.03] px-4 py-10 text-center text-sm text-muted-foreground">
                Complete onboarding and the LK engine will populate this layer.
              </div>
            )}
          </LayerSection>
        </div>

        <div ref={(node) => { sectionRefs.current['layer-3'] = node; }}>
          <LayerSection layer={LAYERS[3]}>
            {missionsUnlocked && hurdles.length ? (
              <div className="mb-5 space-y-3">
                {hurdles.slice(0, 2).map((hurdle) => (
                  <HurdleAlert key={hurdle.id || hurdle.mission_name || hurdle.ui_warning} hurdle={hurdle} />
                ))}
              </div>
            ) : null}

            {missionsUnlocked && dash ? <MissionQuickLinks data={dash} /> : <Layer3Locked />}
          </LayerSection>
        </div>

        <div ref={(node) => { sectionRefs.current['layer-4'] = node; }}>
          <LayerSection layer={LAYERS[4]}>
            <div className="space-y-5">
              {dash?.scoreboard ? <Scoreboard sb={dash.scoreboard} /> : null}
              <ActionPlanCard missionsUnlocked={missionsUnlocked} gateStatus={gateStatus} conquestScore={conquestScore} />
            </div>
          </LayerSection>
        </div>

        <div ref={(node) => { sectionRefs.current['layer-5'] = node; }}>
          <LayerSection layer={LAYERS[5]}>
            <ReportLaunchCard missionsUnlocked={missionsUnlocked} />
          </LayerSection>
        </div>

        <div className="rounded-[28px] border border-white/8 bg-white/[0.02] p-6 text-sm text-muted-foreground">
          <div className="grid gap-6 lg:grid-cols-2">
            <div>
              <h2 className="text-lg font-semibold text-foreground">What is The Strategist?</h2>
              <p className="mt-2 leading-7">
                The Strategist is EverydayHoroscope&apos;s Vedic Business War Room: a decision-support system that combines Krishna Prashnavali, Lal Kitab diagnostics, and live dasha-aware timing into one premium surface for leaders and founders.
              </p>
            </div>
            <div>
              <h2 className="text-lg font-semibold text-foreground">Why Gate 0 comes first</h2>
              <p className="mt-2 leading-7">
                Strategy is not only about data here. Gate 0 checks divine timing before offensive action, so every downstream mission, action plan, and report honors the oracle route before execution begins.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function StrategistLanding() {
  const navigate = useNavigate();

  const schema = {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: [
      {
        '@type': 'Question',
        name: 'What is The Strategist?',
        acceptedAnswer: {
          '@type': 'Answer',
          text: 'The Strategist is a Vedic business strategy system combining Lal Kitab diagnostics, Krishna Prashnavali oracle, and a live mission board for founders and serious decision-makers.',
        },
      },
      {
        '@type': 'Question',
        name: 'How does the Gate 0 oracle work?',
        acceptedAnswer: {
          '@type': 'Answer',
          text: 'Gate 0 is powered by the Krishna Prashnavali oracle. You receive a YES, WAIT, NO, or PRAY verdict before the War Room fully opens.',
        },
      },
      {
        '@type': 'Question',
        name: 'What is a Conquest Score?',
        acceptedAnswer: {
          '@type': 'Answer',
          text: 'The Conquest Score is a strategist readiness metric derived from command-planet strength, direction alignment, karmic debt, ritual streak, and transit windows.',
        },
      },
    ],
  };

  return (
    <div className="min-h-screen overflow-hidden bg-background text-foreground">
      <SEO
        title="The Strategist -- Vedic Business War Room"
        description="A premium Vedic strategist surface for founders and professionals. Gate 0 Krishna Oracle, Lal Kitab diagnostics, live missions, Conquest Score, and executive intelligence."
        url="https://www.everydayhoroscope.in/strategist"
        schema={schema}
        noindex={true}
      />

      <div className="relative overflow-hidden border-b border-gold/10 bg-[linear-gradient(180deg,#060d18_0%,#0b1525_58%,rgba(11,21,37,0.9)_100%)]">
        <StrategistStarField opacity={0.62} />
        <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_22%_18%,rgba(197,160,89,0.18),transparent_24%),radial-gradient(circle_at_80%_14%,rgba(249,115,22,0.12),transparent_22%)]" />
        <div className="relative mx-auto max-w-6xl px-4 py-20 sm:px-6 lg:px-8">
          <div className="max-w-4xl">
            <div className="inline-flex items-center gap-2 rounded-full border border-gold/25 bg-gold/[0.06] px-4 py-2 text-xs uppercase tracking-[0.3em] text-gold/80">
              <span>⚔️</span>
              <span>Premium Integrated Vedic Career Mentor</span>
            </div>
            <h1 className="mt-6 text-5xl font-cinzel text-foreground sm:text-6xl lg:text-7xl">The Strategist</h1>
            <p className="mt-5 max-w-3xl text-lg leading-8 text-white/72 sm:text-xl">
              Bloomberg Terminal for Karma. Six intelligence layers. One War Room. Built for founders, executives, and serious decision-makers.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <button
                type="button"
                onClick={() => navigate('/login', LOGIN_REDIRECT)}
                className="inline-flex items-center gap-2 rounded-full bg-gold px-6 py-3 text-sm font-semibold text-stone-950 transition hover:bg-gold/90"
              >
                Enter the War Room <ArrowRight className="h-4 w-4" />
              </button>
              <Link to="/the-strategist" className="inline-flex items-center gap-2 rounded-full border border-white/12 bg-white/[0.03] px-6 py-3 text-sm font-semibold text-foreground transition hover:bg-white/[0.06]">
                Open Full Landing <ArrowRight className="h-4 w-4" />
              </Link>
            </div>
          </div>

          <div className="mt-14 grid gap-4 md:grid-cols-3">
            {[
              {
                title: 'Gate 0 first',
                body: 'The strategist path begins with Krishna clearance before any campaign goes live.',
              },
              {
                title: '823 mapped rules',
                body: 'Lal Kitab remedy intelligence and strategist mission rules surface as one coordinated system.',
              },
              {
                title: 'Score + state machine',
                body: 'Golden Hour, conquest thresholds, and hurdle alerts keep the War Room feeling operational.',
              },
            ].map((item) => (
              <div key={item.title} className="rounded-[24px] border border-white/8 bg-white/[0.03] p-5">
                <p className="text-lg font-semibold text-foreground">{item.title}</p>
                <p className="mt-2 text-sm leading-7 text-muted-foreground">{item.body}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="mx-auto max-w-6xl space-y-6 px-4 py-10 sm:px-6 lg:px-8">
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {GATE_ZERO_PATHS.map((path) => (
            <div key={path.verdict} className="rounded-[24px] border border-white/8 bg-white/[0.03] p-5">
              <p className="text-lg font-semibold text-foreground">{path.icon} {path.verdict}</p>
              <p className="mt-2 text-sm text-foreground">{path.title}</p>
              <p className="mt-1 text-sm leading-7 text-muted-foreground">{path.body}</p>
            </div>
          ))}
        </div>

        <div className="grid gap-6 xl:grid-cols-[0.95fr_1.05fr]">
          <div className="rounded-[28px] border border-gold/15 bg-card/90 p-6">
            <p className="text-[11px] uppercase tracking-[0.28em] text-gold/70">Six Layers of Intelligence</p>
            <div className="mt-5 space-y-3">
              {LAYERS.map((layer) => (
                <div key={layer.id} className="rounded-2xl border border-white/8 bg-white/[0.03] p-4">
                  <p className="text-sm font-semibold text-foreground">{layer.icon} Layer {layer.n} -- {layer.title}</p>
                  <p className="mt-2 text-sm leading-7 text-muted-foreground">{layer.tagline}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="rounded-[28px] border border-gold/15 bg-card/90 p-6">
            <p className="text-[11px] uppercase tracking-[0.28em] text-gold/70">Conquest Score Bands</p>
            <div className="mt-5 grid gap-3 md:grid-cols-2">
              {SCORE_BANDS.map((band) => (
                <div key={band.title} className={`rounded-2xl border p-4 ${band.tone}`}>
                  <p className="text-[11px] uppercase tracking-[0.24em]">{band.range}</p>
                  <p className="mt-2 text-lg font-semibold">{band.title}</p>
                  <p className="mt-1 text-sm opacity-80">{band.body}</p>
                </div>
              ))}
            </div>
            <div className="mt-6 rounded-2xl border border-gold/20 bg-gold/[0.05] p-5">
              <p className="text-lg font-semibold text-foreground">Public SEO route moved</p>
              <p className="mt-2 text-sm leading-7 text-muted-foreground">
                The canonical indexed strategist story now lives on <Link to="/the-strategist" className="font-semibold text-gold hover:underline">/the-strategist</Link>. This route remains a product surface for login and premium gating.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function StrategistPage() {
  const { user, loading: authLoading } = useAuth();
  const locationSlug = localStorage.getItem('lk_location_slug') || 'new-delhi';

  if (authLoading) return null;

  if (!user) return <StrategistLanding />;

  if (!user.is_premium) {
    return (
      <PremiumGateCard
        feature="The Strategist"
        description="The Vedic Business War Room -- KP oracle, LK diagnostics, Missions, and Conquest Score -- is an exclusive Premium feature. Upgrade to activate your war room."
      />
    );
  }

  return (
    <WarRoomStateProvider locationSlug={locationSlug}>
      <SEO title="The Strategist -- War Room" noindex={true} />
      <Dashboard />
    </WarRoomStateProvider>
  );
}
