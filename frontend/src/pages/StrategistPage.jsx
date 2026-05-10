import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { WarRoomStateProvider, useWarRoom } from '../components/WarRoomStateProvider';
import ConquestGauge from '../components/ConquestGauge';
import HurdleAlert from '../components/HurdleAlert';

const BACKEND = process.env.REACT_APP_BACKEND_URL || '';

const WAR_ROOM_BG = {
  OFFENSIVE_GOLD:    'from-yellow-950/30 to-background',
  GOLDEN_HOUR:       'from-orange-950/40 to-background',
  DEFENSIVE_MIDNIGHT: 'from-blue-950/40 to-background',
};

const WAR_ROOM_LABEL = {
  OFFENSIVE_GOLD:    '⚔️ OFFENSIVE — Rituals OPEN',
  GOLDEN_HOUR:       '🌅 GOLDEN HOUR — Act NOW',
  DEFENSIVE_MIDNIGHT: '🌙 DEFENSIVE — Rituals LOCKED',
};

function Dashboard() {
  const { state: warState, countdown } = useWarRoom();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [dismissedHurdles, setDismissedHurdles] = useState([]);
  const token = localStorage.getItem('token') || '';

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

  const bgGrad = WAR_ROOM_BG[warState] || WAR_ROOM_BG.OFFENSIVE_GOLD;

  if (loading) return (
    <div className="min-h-screen bg-background flex items-center justify-center text-muted-foreground text-sm">
      Initialising War Room…
    </div>
  );

  return (
    <div className={`min-h-screen bg-gradient-to-b ${bgGrad} text-foreground`}>
      <div className="max-w-2xl mx-auto px-4 py-8">
        {/* War Room State Banner */}
        <div className={`rounded-xl border ${warState === 'GOLDEN_HOUR' ? 'border-orange-500/50 bg-orange-500/10 animate-pulse' : 'border-gold/20 bg-gold/[0.04]'} p-4 mb-5 text-center`}>
          <p className="text-sm font-semibold text-gold">{WAR_ROOM_LABEL[warState]}</p>
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
            {/* Conquest Gauge */}
            <div className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-5 mb-4 text-center">
              <h2 className="text-sm font-semibold text-muted-foreground mb-3">Conquest Probability</h2>
              <ConquestGauge {...(data.conquest_probability || {})} />
            </div>

            {/* Command Intel */}
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

            {/* Quick Links */}
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
