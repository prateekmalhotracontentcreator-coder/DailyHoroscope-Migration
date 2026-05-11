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
      const selectRes = await fetch(`${BACKEND}/api/oracle/krishna-prashnavali/select`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify({
          row, col,
          question_text: 'Should I proceed with my strategic mission?',
          focus_area: 'career',
          language_preference: 'bilingual',
          reveal_mode: 'instant',
        }),
      });
      const selectData = await selectRes.json();
      const verdict   = selectData?.reading?.answer?.verdict_display || 'WAIT';
      const answerSlot = selectData?.reading?.answer_slot || 1;
      const reportId  = selectData?.reading?.report_id || null;

      await fetch(`${BACKEND}/api/strategist/gate0/record`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify({ row, col, verdict, answer_slot: answerSlot, report_id: reportId }),
      });

      onVerdict(verdict, selectData?.reading || null);
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

// ── Pre-flight action panel for blocked verdicts ───────────────────────────────
function PreFlightPanel({ gateStatus, conquestScore }) {
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

  if (gateStatus === 'pray_blocked') {
    return (
      <div className="rounded-xl border border-purple-500/40 bg-purple-500/10 p-5 mb-4">
        <p className="font-semibold text-sm mb-2">🙏 Full Surrender — Score Required 75%+</p>
        {conquestScore != null && (
          <p className="text-sm text-muted-foreground mb-2">Current score: <span className="font-bold text-purple-400">{conquestScore}%</span></p>
        )}
        <p className="text-sm text-muted-foreground leading-relaxed mb-4">
          Krishna calls you to full surrender. Complete your Mantra practice and LK Debt Audit. Return when Conquest Probability reaches 75%.
        </p>
        <div className="flex gap-3 flex-wrap">
          <Link to="/mantra-remedies" className="inline-block rounded-lg border border-purple-500/50 bg-purple-500/20 px-4 py-2 text-sm font-semibold text-purple-300 hover:bg-purple-500/30 transition">
            Mantra Remedies →
          </Link>
          <Link to="/lk-remedies/debt-audit" className="inline-block rounded-lg border border-purple-500/50 bg-purple-500/20 px-4 py-2 text-sm font-semibold text-purple-300 hover:bg-purple-500/30 transition">
            LK Debt Audit →
          </Link>
        </div>
      </div>
    );
  }

  return null;
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

          <div className="grid grid-cols-2 gap-3">
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
            <Link to="/strategist/report" className="rounded-xl border border-gold/30 bg-gradient-to-br from-gold/15 to-gold/5 p-4 text-center hover:bg-gold/20 transition">
              <p className="text-xs text-muted-foreground mb-1">Intelligence Brief</p>
              <p className="text-gold font-semibold text-sm">Premium →</p>
            </Link>
          </div>
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
          <PreFlightPanel gateStatus={gateStatus} conquestScore={conquestScore} />
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
