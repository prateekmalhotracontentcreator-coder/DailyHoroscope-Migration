import React from 'react';

export default function HurdleAlert({ hurdle, onDismiss }) {
  if (!hurdle) return null;
  const { ui_warning, mission_name, strategy, id } = hurdle;

  return (
    <div className="rounded-xl border border-red-500/40 bg-red-500/10 p-4 mb-3">
      <div className="flex items-start justify-between gap-2">
        <div>
          <p className="text-red-400 font-semibold text-sm mb-1">
            🚨 {ui_warning || 'High Alert: Karmic Hurdle Detected'}
          </p>
          {mission_name && <p className="text-xs text-muted-foreground">{mission_name}</p>}
          {strategy && <p className="text-xs text-muted-foreground mt-0.5">Recommended: {strategy}</p>}
        </div>
        {onDismiss && (
          <button
            onClick={() => onDismiss(id)}
            className="text-muted-foreground text-sm shrink-0 hover:text-foreground"
          >
            ✕
          </button>
        )}
      </div>
    </div>
  );
}
