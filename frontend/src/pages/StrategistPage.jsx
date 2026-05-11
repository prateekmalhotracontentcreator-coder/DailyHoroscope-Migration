import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { WarRoomStateProvider, useWarRoom } from '../components/WarRoomStateProvider';
import ConquestGauge from '../components/ConquestGauge';
import HurdleAlert from '../components/HurdleAlert';
import KrishnaOracleGrid from '../components/KrishnaOracleGrid';

const BACKEND = process.env.REACT_APP_BACKEND_URL || '';

const WAR_ROOM_BG = {
  OFFENSIVE_GOLD:     'from-yellow-950/30 to-background',
  GOLDEN_HOUR:        'from-orange-950/40 to-background',
  DEFENSIVE_MIDNIGHT: 'from-blue-950/40 to-background',
};

const WAR_ROOM_LABEL = {
  OFFENSIVE_GOLD:     '⚔️ OFFENSIVE — Rituals OPEN',
  GOLDEN_HOUR:        '🌅 GOLDEN HOUR — Act NOW',
  DEFENSIVE_MIDNIGHT: '🌙 DEFENSIVE — Rituals LOCKED',
};

// ── Gate 0 oracle panel ────────────────────────────────────────────────────────
function Gate0Panel({ token, onVerdict }) {
  const [gridMatrix, setGridMatrix] = useState([]);
  const [loadingGrid, setLoadingGrid] = useState(true);
  const [selectedIndex, setSelectedIndex] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetch(`${BACKEND}/api/oracle/krishna-prashnavali/meta`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then(r => r.json())
      .then(d => setGridMatrix(d.grid_matrix || []))
      .catch(() => setError('Unable to load Oracle grid. Please refresh.'))
      .finally(() => setLoadingGrid(false));
  }, [token]);

  async function handleCellSelect({ row, col, index }) {
    setSelectedIndex(index);
    setSubmitting(true);
    setError('');
    try {
      // Single endpoint: injects live astro context + records to kp_sessions
      const res = await fetch(`${BACKEND}/api/strategist/gate0/select`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
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
    <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-5 mb-5">
      <p className="text-[11px] uppercase tracking-widest text-muted-foreground mb-1">Gate 0 — Oracle Clearance</p>
      <h2 className="text-lg font-semibold text-foreground mb-2">Ask Krishna Before You Enter the War Room</h2>
      <p className="text-sm text-muted-foreground mb-5 leading-relaxed">
        Touch one cell. Lord Krishna's answer determines your mission clearance for today.
      </p>
      {error && <p className="text-amber-400 text-sm mb-4">{error}</p>}
      {loadingGrid ? (
        <p className="text-sm text-muted-foreground">Loading Oracle grid…</p>
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
      {submitting && (
        <p className="text-sm text-gold mt-4 text-center">Reading Oracle…</p>
      )}
    </div>
  );
}

// ── Verdict banner after Gate 0 selection ─────────────────────────────────────
function VerdictBanner({ verdict, reading }) {
  const configs = {
    YES: {
      border: 'border-emerald-500/40 bg-emerald-500/10',
      heading: '✅ YES — Path is Clear',
      body: reading?.answer?.meaning?.english_block || 'The path is favorable. Proceed with your strategic mission.',
    },
    WAIT: {
      border: 'border-orange-500/40 bg-orange-500/10',
      heading: '⏳ WAIT — Begin Your Remedy Plan First',
      body: reading?.answer?.meaning?.english_block || 'Patience is required. Activate your LK Tracker streak, then return.',
    },
    NO: {
      border: 'border-red-500/40 bg-red-500/10',
      heading: '🛑 NO — Strategic Realignment Required',
      body: reading?.answer?.meaning?.english_block || 'Resistance is active. Reach 60% Conquest Probability through remedies, then re-test.',
    },
    PRAY: {
      border: 'border-purple-500/40 bg-purple-500/10',
      heading: '🙏 PRAY — Full Surrender Path',
      body: reading?.answer?.meaning?.english_block || 'Krishna calls you to full surrender. Complete Mantra practice and LK Debt Audit. Return at 75% score.',
    },
  };
  const cfg = configs[verdict] || configs.WAIT;
  return (
    <div className={`rounded-xl border ${cfg.border} p-4 mb-4`}>
      <p className="font-semibold text-sm mb-1">{cfg.heading}</p>
      <p className="text-sm text-muted-foreground leading-relaxed">{cfg.body}</p>
    </div>
  );
}

// ── PRAY Full Surrender panel ─────────────────────────────────────────────────
function PraySurrenderPanel({ token }) {
  const [ctx, setCtx] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${BACKEND}/api/strategist/surrender-context`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then(r => r.json())
      .then(setCtx)
      .catch(() => setCtx(null))
      .finally(() => setLoading(false));
  }, [token]);

  const score = ctx?.conquest_score ?? null;
  const ptsTo75 = ctx?.points_to_75 ?? null;
  const pct = score != null ? Math.min(100, Math.round((score / 75) * 100)) : 0;

  return (
    <div className="rounded-xl border border-purple-500/40 bg-purple-500/[0.06] p-5 mb-4 space-y-4">
      {/* Header */}
      <div>
        <p className="font-semibold text-sm text-purple-300 mb-1">🙏 Full Surrender Path — PRAY Verdict Active</p>
        <p className="text-xs text-muted-foreground leading-relaxed">
          Krishna calls you inward before any outward mission. Complete the surrender sequence below, then re-test at Gate 0 when your score reaches 75%.
        </p>
      </div>

      {/* Score progress to 75% */}
      {score != null && (
        <div>
          <div className="flex justify-between text-[10px] text-muted-foreground mb-1">
            <span>Conquest score: <span className="text-purple-300 font-semibold">{score}%</span></span>
            <span>{ptsTo75} pts to re-test threshold (75%)</span>
          </div>
          <div className="h-2 rounded-full bg-purple-900/40 overflow-hidden">
            <div
              className="h-full rounded-full bg-gradient-to-r from-purple-600 to-purple-400 transition-all duration-500"
              style={{ width: `${pct}%` }}
            />
          </div>
        </div>
      )}

      {/* Featured mantra */}
      {!loading && ctx?.featured_mantra && (
        <div className="rounded-lg border border-purple-500/30 bg-purple-900/20 p-4">
          <p className="text-[10px] uppercase tracking-widest text-purple-400 mb-2">
            Featured Mantra — {ctx.featured_mantra.deity || ctx.featured_mantra.remedy_area}
          </p>
          <p className="text-xl leading-relaxed text-purple-100 font-medium mb-1">
            {ctx.featured_mantra.mantra_devanagari}
          </p>
          <p className="text-xs text-purple-300 italic mb-2">
            {ctx.featured_mantra.mantra_transliteration}
          </p>
          <div className="flex flex-wrap gap-3 text-[10px] text-muted-foreground">
            <span>Frequency: <span className="text-purple-300">{ctx.featured_mantra.frequency}</span></span>
          </div>
          {ctx.featured_mantra.guidance && (
            <p className="text-[11px] text-muted-foreground mt-2 leading-relaxed">{ctx.featured_mantra.guidance}</p>
          )}
          <Link to="/mantra-remedies" className="mt-3 inline-block text-xs text-purple-300 hover:text-purple-100 hover:underline">
            Full Mantra Library →
          </Link>
        </div>
      )}

      {/* Gate 1 debt status */}
      {ctx?.gate1_narrative && (
        <div className="rounded-lg border border-amber-500/30 bg-amber-500/[0.06] p-3">
          <p className="text-[10px] uppercase tracking-widest text-amber-400 mb-1">Karmic Debt Status</p>
          <p className="text-xs text-muted-foreground leading-relaxed">{ctx.gate1_narrative}</p>
          <Link to="/lk-remedies/debt-audit" className="mt-2 inline-block text-xs text-amber-400 hover:underline">
            Run Debt Audit →
          </Link>
        </div>
      )}

      {/* Surrender steps */}
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

      {/* CTAs */}
      <div className="flex gap-3 flex-wrap pt-1">
        <Link to="/mantra-remedies" className="inline-block rounded-lg border border-purple-500/50 bg-purple-500/20 px-4 py-2 text-sm font-semibold text-purple-300 hover:bg-purple-500/30 transition">
          Mantra Remedies →
        </Link>
        <Link to="/lk-remedies/debt-audit" className="inline-block rounded-lg border border-amber-500/40 bg-amber-500/10 px-4 py-2 text-sm font-semibold text-amber-300 hover:bg-amber-500/20 transition">
          LK Debt Audit →
        </Link>
      </div>
    </div>
  );
}

// ── Pre-flight action panel for WAIT and NO verdicts ──────────────────────────
function PreFlightPanel({ gateStatus, conquestScore, token }) {
  if (gateStatus === 'pray_blocked') {
    return <PraySurrenderPanel token={token} />;
  }

  if (gateStatus === 'wait_active') {
    return (
      <div className="rounded-xl border border-orange-500/40 bg-orange-500/10 p-5 mb-4">
        <p className="font-semibold text-sm mb-2">⏳ Remedy Plan Required</p>
        <p className="text-sm text-muted-foreground leading-relaxed mb-4">
          Oracle asks for patience. Start your LK Remedy Plan and build a daily streak. War Room unlocks once your streak is active.
        </p>
        <Link to="/lk-remedies/tracker" className="inline-block rounded-lg border border-orange-500/50 bg-orange-500/20 px-4 py-2 text-sm font-semibold text-orange-300 hover:bg-orange-500/30 transition">
          Start LK Tracker →
        </Link>
      </div>
    );
  }

  if (gateStatus === 'no_blocked') {
    return (
      <div className="rounded-xl border border-red-500/40 bg-red-500/10 p-5 mb-4">
        <p className="font-semibold text-sm mb-2">🛑 Conquest Score Required — 60%+</p>
        {conquestScore != null && (
          <p className="text-sm text-muted-foreground mb-2">Current score: <span className="font-bold text-red-400">{conquestScore}%</span></p>
        )}
        <p className="text-sm text-muted-foreground leading-relaxed mb-4">
          Oracle sees resistance. Complete your remedy cycle to raise your Conquest Probability above 60%, then re-test at Gate 0.
        </p>
        <div className="flex gap-3 flex-wrap">
          <Link to="/lk-remedies/remedies" className="inline-block rounded-lg border border-red-500/50 bg-red-500/20 px-4 py-2 text-sm font-semibold text-red-300 hover:bg-red-500/30 transition">
            Browse Remedies →
          </Link>
          <Link to="/lk-remedies/tracker" className="inline-block rounded-lg border border-gold/30 bg-gold/10 px-4 py-2 text-sm font-semibold text-gold hover:bg-gold/20 transition">
            LK Tracker →
          </Link>
        </div>
      </div>
    );
  }

  return null;
}

// ── Success & Debt Scoreboard ─────────────────────────────────────────────────
function Scoreboard({ sb }) {
  const pct = sb.next_threshold
    ? Math.min(100, Math.round((sb.conquest_score / sb.next_threshold) * 100))
    : 100;

  const verdictColor = {
    YES:  'text-emerald-400',
    WAIT: 'text-orange-400',
    NO:   'text-red-400',
    PRAY: 'text-purple-400',
  }[sb.gate0_last_verdict] || 'text-muted-foreground';

  return (
    <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-5 mt-1">
      <p className="text-[11px] uppercase tracking-widest text-muted-foreground mb-4">Success &amp; Debt Scoreboard</p>

      {/* Score + tier */}
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

      {/* Progress bar to next threshold */}
      {sb.next_threshold && (
        <div className="mb-4">
          <div className="flex justify-between text-[10px] text-muted-foreground mb-1">
            <span>Progress to {sb.next_threshold_label}</span>
            <span>{sb.points_to_next} pts remaining</span>
          </div>
          <div className="h-2 rounded-full bg-gold/10 overflow-hidden">
            <div
              className="h-full rounded-full bg-gradient-to-r from-gold/60 to-gold transition-all duration-500"
              style={{ width: `${pct}%` }}
            />
          </div>
        </div>
      )}

      {/* Status row */}
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
              <p className="text-[10px] text-muted-foreground">
                {sb.gate0_days_since === 0 ? 'Today' : `${sb.gate0_days_since}d ago`}
              </p>
            </>
          ) : (
            <p className="text-sm text-muted-foreground">None yet</p>
          )}
        </div>
      </div>
    </div>
  );
}

// ── War Room dashboard (shown when Gate 0 is clear) ───────────────────────────
function WarRoomDashboard({ token }) {
  const { state: warState, countdown } = useWarRoom();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetch(`${BACKEND}/api/strategist/dashboard`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then(r => r.json())
      .then(d => {
        if (d.error) throw new Error(d.error);
        setData(d);
      })
      .catch(e => setError(e.message))
      .finally(() => setLoading(false));
  }, [token]);

  const bgLabel = WAR_ROOM_LABEL[warState] || WAR_ROOM_LABEL.OFFENSIVE_GOLD;

  if (loading) return (
    <div className="text-center text-muted-foreground text-sm py-8">Loading War Room…</div>
  );

  return (
    <>
      <div className={`rounded-xl border ${warState === 'GOLDEN_HOUR' ? 'border-orange-500/50 bg-orange-500/10 animate-pulse' : 'border-gold/20 bg-gold/[0.04]'} p-4 mb-5 text-center`}>
        <p className="text-sm font-semibold text-gold">{bgLabel}</p>
        {countdown && <p className="text-2xl font-mono text-orange-400 mt-1">{countdown}</p>}
      </div>

      {error && (
        <div className="rounded-xl border border-amber-500/30 bg-amber-500/10 p-4 mb-4">
          <p className="text-amber-400 text-sm">{error}</p>
          <Link to="/lk-remedies/onboard" className="text-gold text-xs underline mt-1 block">
            Complete LK Onboarding first →
          </Link>
        </div>
      )}

      {data && (
        <>
          <div className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-5 mb-4 text-center">
            <h2 className="text-sm font-semibold text-muted-foreground mb-3">Conquest Probability</h2>
            <ConquestGauge {...(data.conquest_probability || {})} />
          </div>

          {/* 5-Gate LK Summary */}
          {data.gate_summaries?.length > 0 && (
            <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-4 mb-4">
              <p className="text-[11px] uppercase tracking-widest text-muted-foreground mb-3">Lal Kitab — 5-Gate Status</p>
              <div className="space-y-2">
                {data.gate_summaries.map(g => {
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
              <Link to="/lk-remedies/report" className="mt-3 inline-block text-xs text-gold hover:underline">
                Full LK Diagnosis Report →
              </Link>
            </div>
          )}

          <div className="grid grid-cols-2 gap-3 mb-4">
            <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-4 text-center">
              <p className="text-xs text-muted-foreground mb-1">Command Planet</p>
              <p className="text-gold font-bold text-lg">{data.command_planet}</p>
            </div>
            <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-4 text-center">
              <p className="text-xs text-muted-foreground mb-1">Power Direction</p>
              <p className="text-gold font-bold text-lg">{data.success_direction}</p>
            </div>
            <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-4 text-center">
              <p className="text-xs text-muted-foreground mb-1">Ritual Streak</p>
              <p className="text-emerald-400 font-bold text-lg">{data.ritual_streak} days</p>
            </div>
            <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-4 text-center">
              <p className="text-xs text-muted-foreground mb-1">Active Missions</p>
              <p className="text-gold font-bold text-lg">{data.active_missions_count}</p>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3 mb-4">
            <Link to="/strategist/missions" className="rounded-xl border border-gold/20 bg-gold/[0.04] p-4 text-center hover:bg-gold/10 transition">
              <p className="text-xs text-muted-foreground mb-1">Mission Board</p>
              <p className="text-gold font-semibold text-sm">View All →</p>
            </Link>
            <Link to="/lk-remedies/tracker" className="rounded-xl border border-gold/20 bg-gold/[0.04] p-4 text-center hover:bg-gold/10 transition">
              <p className="text-xs text-muted-foreground mb-1">LK Tracker</p>
              <p className="text-gold font-semibold text-sm">Day {data.ritual_streak} →</p>
            </Link>
            <Link to="/strategist/surrogate" className="rounded-xl border border-gold/20 bg-gold/[0.04] p-4 text-center hover:bg-gold/10 transition">
              <p className="text-xs text-muted-foreground mb-1">Surrogate Bridge</p>
              <p className="text-gold font-semibold text-sm">Activate →</p>
            </Link>
            <Link to="/strategist/action-plan" className="rounded-xl border border-gold/30 bg-gradient-to-br from-gold/15 to-gold/5 p-4 text-center hover:bg-gold/20 transition">
              <p className="text-xs text-muted-foreground mb-1">Action Plan</p>
              <p className="text-gold font-semibold text-sm">View →</p>
            </Link>
            <Link to="/strategist/report" className="rounded-xl border border-gold/20 bg-gold/[0.04] p-4 text-center hover:bg-gold/10 transition">
              <p className="text-xs text-muted-foreground mb-1">Intelligence Brief</p>
              <p className="text-gold font-semibold text-sm">Premium →</p>
            </Link>
          </div>

          {/* Success & Debt Scoreboard */}
          {data.scoreboard && <Scoreboard sb={data.scoreboard} />}
        </>
      )}
    </>
  );
}

// ── Main page ─────────────────────────────────────────────────────────────────
function Dashboard() {
  const { state: warState } = useWarRoom();
  const bgGrad = WAR_ROOM_BG[warState] || WAR_ROOM_BG.OFFENSIVE_GOLD;
  const token = localStorage.getItem('token') || '';

  const [gateStatus, setGateStatus] = useState('loading'); // loading | required | clear | wait_active | no_blocked | pray_blocked
  const [conquestScore, setConquestScore] = useState(null);
  const [freshVerdict, setFreshVerdict] = useState(null); // { verdict, reading } set immediately after Oracle tap
  const [lastVerdict, setLastVerdict] = useState(null);

  useEffect(() => {
    fetch(`${BACKEND}/api/strategist/gate0/status`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then(r => r.json())
      .then(d => {
        setGateStatus(d.status || 'required');
        setConquestScore(d.conquest_score ?? null);
        setLastVerdict(d.last_verdict ?? null);
      })
      .catch(() => setGateStatus('required'));
  }, [token]);

  function handleVerdict(verdict, reading) {
    setFreshVerdict({ verdict, reading });
    setLastVerdict(verdict);
    if (verdict === 'YES') {
      setGateStatus('clear');
    } else if (verdict === 'WAIT') {
      setGateStatus('wait_active');
    } else if (verdict === 'NO') {
      setGateStatus('no_blocked');
    } else {
      setGateStatus('pray_blocked');
    }
  }

  const showDashboard = gateStatus === 'clear';
  const blocked = ['wait_active', 'no_blocked', 'pray_blocked'].includes(gateStatus);

  return (
    <div className={`min-h-screen bg-gradient-to-b ${bgGrad} text-foreground`}>
      <div className="max-w-2xl mx-auto px-4 py-8">

        {gateStatus === 'loading' && (
          <div className="text-center text-muted-foreground text-sm py-12">
            Checking Oracle clearance…
          </div>
        )}

        {gateStatus === 'required' && (
          <>
            {lastVerdict && (
              <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-3 mb-4 text-center">
                <p className="text-xs text-muted-foreground">
                  Previous verdict: <span className="text-gold font-semibold">{lastVerdict}</span> — Score now qualifies you for re-test.
                </p>
              </div>
            )}
            <Gate0Panel token={token} onVerdict={handleVerdict} />
          </>
        )}

        {freshVerdict && gateStatus !== 'loading' && gateStatus !== 'required' && (
          <VerdictBanner verdict={freshVerdict.verdict} reading={freshVerdict.reading} />
        )}

        {blocked && (
          <PreFlightPanel gateStatus={gateStatus} conquestScore={conquestScore} token={token} />
        )}

        {showDashboard && (
          <WarRoomDashboard token={token} />
        )}

      </div>
    </div>
  );
}

export default function StrategistPage() {
  const locationSlug = localStorage.getItem('lk_location_slug') || 'new-delhi';
  return (
    <WarRoomStateProvider locationSlug={locationSlug}>
      <Dashboard />
    </WarRoomStateProvider>
  );
}
