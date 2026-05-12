import { SEO } from '../components/SEO';
import React, { useEffect, useState } from 'react';
import MissionCard from '../components/MissionCard';

const BACKEND = process.env.REACT_APP_BACKEND_URL || '';
const PLANETS = ['', 'Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Rahu', 'Ketu'];

export default function StrategistMissionsPage() {
  const [missions, setMissions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filterPlanet, setFilterPlanet] = useState('');
  useEffect(() => {
    fetch(`${BACKEND}/api/strategist/missions`, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({}),
    })
      .then(r => r.json())
      .then(d => setMissions(d.missions || []))
      .catch(e => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  const filtered = filterPlanet
    ? missions.filter(m => (m.trigger_condition || '').includes(filterPlanet))
    : missions;

  return (
    <div className="min-h-screen bg-background text-foreground px-4 py-8 max-w-2xl mx-auto">
      <SEO title="Mission Board — The Strategist" noindex={true} />
      <div className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-5 mb-5">
        <h1 className="text-xl font-bold text-gold mb-3">Mission Board</h1>
        <div className="flex items-center gap-3">
          <label className="text-xs text-muted-foreground">Filter by planet:</label>
          <select
            value={filterPlanet}
            onChange={e => setFilterPlanet(e.target.value)}
            className="bg-background border border-gold/20 rounded px-2 py-1 text-xs text-foreground"
          >
            {PLANETS.map(p => <option key={p} value={p}>{p || 'All'}</option>)}
          </select>
        </div>
      </div>

      {loading && <p className="text-muted-foreground text-sm">Loading missions…</p>}
      {error && <p className="text-red-400 text-sm mb-4">{error}</p>}

      {!loading && filtered.length === 0 && (
        <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-5 text-center">
          <p className="text-muted-foreground text-sm">No active missions match current transits.</p>
          <p className="text-xs text-muted-foreground mt-1">Complete onboarding and run diagnosis to trigger missions.</p>
        </div>
      )}

      <div className="space-y-3">
        {filtered.map((m, i) => <MissionCard key={m.id || i} mission={m} />)}
      </div>

      {!loading && missions.length > 0 && (
        <p className="text-xs text-muted-foreground mt-4 text-center">{filtered.length} active missions</p>
      )}
    </div>
  );
}
