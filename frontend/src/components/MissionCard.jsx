import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function MissionCard({ mission }) {
  const navigate = useNavigate();
  if (!mission) return null;

  const {
    mission_name, mission_objective, strategy, pivot_action,
    kpi_target, trigger_condition, remedy_id, id,
  } = mission;

  return (
    <div className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-4">
      <div className="flex items-start justify-between gap-2 mb-2">
        <h3 className="font-semibold text-sm text-gold leading-tight">{mission_name || `Mission #${id}`}</h3>
        {trigger_condition && (
          <span className="text-xs font-mono text-muted-foreground shrink-0 bg-gold/10 px-1.5 py-0.5 rounded">
            {trigger_condition}
          </span>
        )}
      </div>
      {mission_objective && <p className="text-xs text-foreground mb-1">🎯 {mission_objective}</p>}
      {strategy && <p className="text-xs text-muted-foreground mb-1">⚔️ {strategy}</p>}
      {pivot_action && <p className="text-xs text-muted-foreground mb-1">🔄 {pivot_action}</p>}
      {kpi_target && <p className="text-xs text-muted-foreground mb-2">📊 {kpi_target}</p>}
      {remedy_id && (
        <button
          onClick={() => navigate('/lk-remedies/tracker')}
          className="text-xs border border-gold/30 text-gold rounded px-2 py-0.5 hover:bg-gold/10 transition"
        >
          + Add Remedy #{remedy_id} to Tracker
        </button>
      )}
    </div>
  );
}
