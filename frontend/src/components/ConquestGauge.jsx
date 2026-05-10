import React from 'react';

const TIER_COLOR = {
  'Sovereign Dominance': '#FFD700',
  'Operational Friction': '#FFC42E',
  'Strategic Siege': '#F97316',
  'Karmic Lockdown': '#EF4444',
};

export default function ConquestGauge({ score = 0, tier = '', directive = '', narrative = '' }) {
  const color = TIER_COLOR[tier] || '#c5a059';
  const r = 56;
  const circ = 2 * Math.PI * r;
  const pct = score / 99;
  const dash = pct * circ;

  return (
    <div className="flex flex-col items-center text-center">
      <svg width="140" height="140">
        <circle cx="70" cy="70" r={r} fill="none" stroke="rgba(197,160,89,0.12)" strokeWidth="12" />
        <circle
          cx="70" cy="70" r={r} fill="none"
          stroke={color} strokeWidth="12"
          strokeDasharray={`${dash} ${circ}`}
          strokeLinecap="round"
          transform="rotate(-90 70 70)"
          style={{ transition: 'stroke-dasharray 1s ease' }}
        />
        <text x="70" y="65" textAnchor="middle" fill={color} fontSize="26" fontWeight="bold">{score}%</text>
        <text x="70" y="82" textAnchor="middle" fill="#888" fontSize="9">{directive}</text>
      </svg>
      {tier && <p className="text-xs font-semibold mt-1" style={{ color }}>{tier}</p>}
      {narrative && <p className="text-xs text-muted-foreground mt-1 max-w-xs">{narrative}</p>}
    </div>
  );
}
