import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

const BACKEND = process.env.REACT_APP_BACKEND_URL || '';

const TYPE_CONFIG = {
  gate0:    { dot: 'bg-gold',          badge: 'text-gold border-gold/40 bg-gold/10',          label: 'ORACLE' },
  remedy:   { dot: 'bg-emerald-400',   badge: 'text-emerald-400 border-emerald-400/40 bg-emerald-400/10', label: 'REMEDY' },
  debt:     { dot: 'bg-amber-400',     badge: 'text-amber-400 border-amber-400/40 bg-amber-400/10',       label: 'DEBT' },
  mercury:  { dot: 'bg-blue-400',      badge: 'text-blue-400 border-blue-400/40 bg-blue-400/10',          label: 'MERCURY' },
  surrender:{ dot: 'bg-purple-400',    badge: 'text-purple-400 border-purple-400/40 bg-purple-400/10',    label: 'PRAY' },
  mission:  { dot: 'bg-muted-foreground', badge: 'text-muted-foreground border-border bg-card',           label: 'MISSION' },
};

function ActionCard({ action }) {
  const cfg = TYPE_CONFIG[action.type] || TYPE_CONFIG.mission;
  return (
    <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-4 flex gap-4">
      <div className="flex flex-col items-center pt-1 gap-2 shrink-0">
        <span className="text-[10px] font-bold text-muted-foreground tabular-nums w-5 text-center">
          {String(action.priority).padStart(2, '0')}
        </span>
        <span className={`h-2 w-2 rounded-full ${cfg.dot}`} />
      </div>
      <div className="min-w-0 flex-1">
        <div className="flex items-center gap-2 flex-wrap mb-1">
          <span className={`text-[10px] font-semibold uppercase tracking-wider px-1.5 py-0.5 rounded border ${cfg.badge}`}>
            {cfg.label}
          </span>
          <p className="text-sm font-semibold text-foreground">{action.label}</p>
        </div>
        {action.detail && (
          <p className="text-xs text-muted-foreground leading-relaxed mb-3 line-clamp-3">{action.detail}</p>
        )}
        <Link
          to={action.cta_path}
          className="inline-block rounded-lg border border-gold/30 bg-gold/10 px-3 py-1.5 text-xs font-semibold text-gold hover:bg-gold/20 transition"
        >
          {action.cta_label} →
        </Link>
      </div>
    </div>
  );
}

function ActiveRemedyCard({ remedy }) {
  if (!remedy) return null;
  return (
    <div className="rounded-xl border border-emerald-500/30 bg-emerald-500/[0.06] p-4 mb-5">
      <p className="text-[11px] uppercase tracking-widest text-muted-foreground mb-2">Active LK Remedy — Day {remedy.streak_days}</p>
      <p className="text-sm leading-relaxed text-foreground mb-1">{remedy.rule_text}</p>
      {remedy.planet && (
        <p className="text-xs text-muted-foreground">Planet: <span className="text-gold font-semibold">{remedy.planet}</span>
          {remedy.house ? ` · House ${remedy.house}` : ''}
        </p>
      )}
      <Link to="/lk-remedies/tracker" className="mt-3 inline-block text-xs text-gold hover:underline">
        View Tracker →
      </Link>
    </div>
  );
}

export default function StrategistActionPlanPage() {
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    document.title = 'Action Plan | The Strategist';
    fetch(`${BACKEND}/api/strategist/action-plan`, {
      credentials: 'include',
    })
      .then(r => r.json())
      .then(d => {
        if (d.detail) throw new Error(d.detail);
        setData(d);
      })
      .catch(e => setError(e.message))
      .finally(() => setLoading(false));
  }, [token]);

  if (loading) return (
    <div className="min-h-screen bg-background flex items-center justify-center text-muted-foreground text-sm">
      Building your Action Plan…
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-b from-yellow-950/20 to-background text-foreground">
      <div className="max-w-2xl mx-auto px-4 py-8">

        {/* Header */}
        <div className="mb-6">
          <button
            onClick={() => navigate('/strategist')}
            className="text-xs text-muted-foreground hover:text-gold mb-3 inline-block"
          >
            ← War Room
          </button>
          <h1 className="text-2xl font-playfair font-semibold text-foreground">Action Plan</h1>
          <p className="text-sm text-muted-foreground mt-1">Prioritised mission sequence based on your current Oracle, LK, and Astrological state.</p>
        </div>

        {error && (
          <div className="rounded-xl border border-amber-500/30 bg-amber-500/10 p-4 mb-5">
            <p className="text-amber-400 text-sm">{error}</p>
            <Link to="/lk-remedies/onboard" className="text-gold text-xs underline mt-1 block">
              Complete LK Onboarding first →
            </Link>
          </div>
        )}

        {data && (
          <>
            {/* Score summary strip */}
            <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-4 mb-5 flex items-center justify-between gap-4 flex-wrap">
              <div>
                <p className="text-[10px] uppercase tracking-widest text-muted-foreground">Conquest Score</p>
                <p className="text-2xl font-bold text-gold mt-0.5">{data.conquest_score}<span className="text-base">%</span></p>
                <p className="text-xs text-muted-foreground">{data.score_tier}</p>
              </div>
              <div className="text-center">
                <p className="text-[10px] uppercase tracking-widest text-muted-foreground">Streak</p>
                <p className="text-2xl font-bold text-emerald-400 mt-0.5">{data.streak_days}<span className="text-base">d</span></p>
              </div>
              <div className="text-center">
                <p className="text-[10px] uppercase tracking-widest text-muted-foreground">Gate 0</p>
                {data.gate0?.verdict ? (
                  <>
                    <p className={`text-lg font-bold mt-0.5 ${
                      data.gate0.verdict === 'YES' ? 'text-emerald-400' :
                      data.gate0.verdict === 'WAIT' ? 'text-orange-400' :
                      data.gate0.verdict === 'NO' ? 'text-red-400' : 'text-purple-400'
                    }`}>{data.gate0.verdict}</p>
                    <p className="text-[10px] text-muted-foreground">
                      {data.gate0.days_since === 0 ? 'Today' : `${data.gate0.days_since}d ago`}
                      {data.gate0.expired ? ' · Expired' : ''}
                    </p>
                  </>
                ) : (
                  <p className="text-sm text-muted-foreground mt-0.5">None</p>
                )}
              </div>
            </div>

            {/* Active remedy */}
            <ActiveRemedyCard remedy={data.active_remedy} />

            {/* Priority action list */}
            <p className="text-[11px] uppercase tracking-widest text-muted-foreground mb-3">
              {data.priority_actions?.length || 0} Priority Actions
            </p>
            {data.priority_actions?.length > 0 ? (
              <div className="space-y-3">
                {data.priority_actions.map(a => (
                  <ActionCard key={a.priority} action={a} />
                ))}
              </div>
            ) : (
              <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-6 text-center">
                <p className="text-gold font-semibold">All clear — no urgent actions.</p>
                <p className="text-sm text-muted-foreground mt-1">Maintain your streak and monitor the Scoreboard.</p>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
