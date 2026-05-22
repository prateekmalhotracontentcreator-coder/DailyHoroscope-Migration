import React, { useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const PLANET_STYLES = {
  Sun: 'border-amber-400/35 bg-amber-500/10 text-amber-200',
  Moon: 'border-sky-300/35 bg-sky-400/10 text-sky-100',
  Mercury: 'border-emerald-400/35 bg-emerald-500/10 text-emerald-200',
  Venus: 'border-pink-400/35 bg-pink-500/10 text-pink-200',
  Mars: 'border-red-400/35 bg-red-500/10 text-red-200',
  Jupiter: 'border-gold/35 bg-gold/10 text-gold',
  Saturn: 'border-slate-400/35 bg-slate-500/10 text-slate-200',
  Rahu: 'border-violet-400/35 bg-violet-500/10 text-violet-200',
  Ketu: 'border-fuchsia-400/35 bg-fuchsia-500/10 text-fuchsia-200',
};

const PLANETS = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Rahu', 'Ketu'];

function inferMissionPlanet(mission) {
  const candidates = [
    mission?.planet_lord,
    mission?.command_planet,
    mission?.trigger_condition,
    mission?.mission_name,
    mission?.strategy,
  ].filter(Boolean);

  for (const candidate of candidates) {
    const planet = PLANETS.find((item) => String(candidate).toLowerCase().includes(item.toLowerCase()));
    if (planet) return planet;
  }

  return '';
}

function ExpandableCopy({ label, text, previewLength = 120, collapsedByDefault = true, expandLabel = 'Show more', collapseLabel = 'Show less' }) {
  const [expanded, setExpanded] = useState(!collapsedByDefault);

  if (!text) return null;

  const shouldTruncate = text.length > previewLength;
  const visibleText = expanded || !shouldTruncate ? text : `${text.slice(0, previewLength).trim()}...`;

  return (
    <div className="rounded-2xl border border-white/8 bg-white/[0.03] p-4">
      <p className="text-[11px] uppercase tracking-[0.22em] text-muted-foreground">{label}</p>
      <p className="mt-2 text-sm leading-7 text-foreground/85">{visibleText}</p>
      {shouldTruncate ? (
        <button
          type="button"
          onClick={() => setExpanded((current) => !current)}
          className="mt-3 text-xs font-semibold text-gold transition hover:text-gold/85"
        >
          {expanded ? `▲ ${collapseLabel}` : `▼ ${expandLabel}`}
        </button>
      ) : null}
    </div>
  );
}

export default function MissionCard({ mission, commandPlanet = '' }) {
  const navigate = useNavigate();
  const missionPlanet = useMemo(() => inferMissionPlanet(mission), [mission]);
  if (!mission) return null;

  const {
    mission_name,
    mission_objective,
    strategy,
    decision_logic,
    pivot_logic,
    pivot_action,
    kpi_target,
    trigger_condition,
    remedy_id,
    id,
    approval_status,
  } = mission;
  const isCommandPlanet = missionPlanet && commandPlanet && missionPlanet.toLowerCase() === commandPlanet.toLowerCase();
  const planetTone = PLANET_STYLES[missionPlanet] || 'border-white/10 bg-white/[0.03] text-muted-foreground';
  const statusTone = approval_status === 'approved'
    ? 'border-emerald-500/30 bg-emerald-500/10 text-emerald-300'
    : approval_status === 'pending_human_review'
      ? 'border-amber-500/30 bg-amber-500/10 text-amber-300'
      : 'border-white/10 bg-white/[0.03] text-muted-foreground';

  return (
    <article className="h-full rounded-[26px] border border-gold/20 bg-gold/[0.04] p-4 shadow-sm sm:p-5">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div className="min-w-0 flex-1">
          <div className="flex flex-wrap items-center gap-2">
            <span className="rounded-full border border-gold/25 bg-gold/[0.07] px-3 py-1 text-[11px] uppercase tracking-[0.22em] text-gold">
              Mission #{id}
            </span>
            {missionPlanet ? (
              <span className={`rounded-full border px-3 py-1 text-[11px] font-medium ${planetTone}`}>
                {missionPlanet} Mission
              </span>
            ) : null}
            {isCommandPlanet ? (
              <span className="rounded-full border border-gold/40 bg-gold/10 px-3 py-1 text-[11px] font-medium text-gold">
                ⭐ Command Planet Active
              </span>
            ) : null}
          </div>
          <h3 className="mt-3 text-lg font-semibold leading-tight text-gold">{mission_name || `Mission #${id}`}</h3>
          {mission_objective ? <p className="mt-2 text-sm leading-7 text-foreground/90">🎯 {mission_objective}</p> : null}
        </div>
        {trigger_condition ? (
          <span className="shrink-0 rounded-full border border-white/10 bg-white/[0.03] px-3 py-1 text-[11px] font-mono text-muted-foreground">
            {trigger_condition}
          </span>
        ) : null}
      </div>

      <div className="mt-4 space-y-3">
        {strategy ? (
          <div className="rounded-2xl border border-white/8 bg-white/[0.03] p-4">
            <p className="text-[11px] uppercase tracking-[0.22em] text-muted-foreground">Strategy</p>
            <p className="mt-2 text-sm leading-7 text-foreground/85">{strategy}</p>
          </div>
        ) : null}

        <ExpandableCopy
          label="Decision Logic"
          text={decision_logic}
          previewLength={120}
          collapsedByDefault={true}
          expandLabel="Show more"
          collapseLabel="Hide"
        />

        {pivot_action ? (
          <div className="rounded-2xl border border-white/8 bg-white/[0.03] p-4">
            <p className="text-[11px] uppercase tracking-[0.22em] text-muted-foreground">Pivot Action</p>
            <p className="mt-2 text-sm leading-7 text-foreground/85">{pivot_action}</p>
          </div>
        ) : null}

        <ExpandableCopy
          label="Pivot Logic"
          text={pivot_logic}
          previewLength={120}
          collapsedByDefault={true}
          expandLabel="Show Pivot Logic"
          collapseLabel="Hide Pivot Logic"
        />
      </div>

      <div className="mt-4 flex flex-wrap items-center gap-2">
        {kpi_target ? (
          <span className="rounded-full border border-gold/25 bg-gold/[0.08] px-3 py-1 text-[11px] font-medium text-gold">
            KPI: {kpi_target}
          </span>
        ) : null}
        <span className={`rounded-full border px-3 py-1 text-[11px] font-medium ${statusTone}`}>
          {approval_status ? approval_status.replaceAll('_', ' ') : 'live trigger'}
        </span>
      </div>

      {remedy_id && (
        <button
          type="button"
          onClick={() => navigate('/lk-remedies/tracker')}
          className="mt-4 inline-flex items-center rounded-full border border-gold/30 px-3 py-1.5 text-xs font-semibold text-gold transition hover:bg-gold/10"
        >
          + Add Remedy #{remedy_id} to Tracker
        </button>
      )}
    </article>
  );
}
