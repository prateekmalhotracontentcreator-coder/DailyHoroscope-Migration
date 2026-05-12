import { SEO } from '../components/SEO';
import React, { useEffect, useState, useCallback } from 'react';

const BACKEND = process.env.REACT_APP_BACKEND_URL || '';
const PLANETS = ['', 'Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Rahu', 'Ketu'];
const SCIENCE_IDS = [
  { value: 'jyotish_lk_remedies', label: 'Lal Kitab Core Remedies' },
  { value: 'jyotish_remedies_dhana', label: 'Dhana Remedies' },
  { value: 'jyotish_remedies_gemstones', label: 'Gemstones' },
  { value: 'jyotish_remedies_crystals', label: 'Crystals' },
  { value: 'jyotish_remedies_chakra', label: 'Chakra' },
];

function RemCard({ r, onTrack }) {
  const sev = r.severity || 0;
  const sevColor = sev >= 4 ? 'text-red-400' : sev >= 2 ? 'text-amber-400' : 'text-emerald-400';
  return (
    <div className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-4">
      <div className="flex items-start justify-between gap-2 mb-1">
        <p className="font-semibold text-sm text-foreground leading-tight">
          {r.title || r.ritual_item || r.remedy_name || `Record #${r.id}`}
        </p>
        {sev > 0 && <span className={`text-xs font-mono ${sevColor} shrink-0`}>sev {sev}</span>}
      </div>
      {r.planet && <p className="text-xs text-muted-foreground mb-1">🪐 {r.planet}{r.house ? ` · House ${r.house}` : ''}</p>}
      {r.focus_area && <p className="text-xs text-muted-foreground mb-1">Focus: {r.focus_area}</p>}
      {(r.ritual_item || r.summary) && (
        <p className="text-xs text-muted-foreground line-clamp-2 mb-2">{r.ritual_item || r.summary}</p>
      )}
      <button
        onClick={() => onTrack(r.id)}
        className="text-xs text-gold border border-gold/30 rounded px-2 py-0.5 hover:bg-gold/10 transition"
      >
        + Start Tracker
      </button>
    </div>
  );
}

export default function LKBrowsePage() {
  const [records, setRecords] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [scienceId, setScienceId] = useState('jyotish_lk_remedies');
  const [planet, setPlanet] = useState('');
  const [house, setHouse] = useState('');
  const [minSev, setMinSev] = useState('');
  const [skip, setSkip] = useState(0);
  const LIMIT = 20;
  const fetchRemedies = useCallback(async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams({ science_id: scienceId, skip, limit: LIMIT });
      if (planet) params.append('planet', planet);
      if (house) params.append('house', house);
      if (minSev) params.append('severity', minSev);
      const res = await fetch(`${BACKEND}/api/lk/remedies?${params}`);
      if (res.ok) {
        const data = await res.json();
        setRecords(data.records || []);
        setTotal(data.total || 0);
      }
    } finally { setLoading(false); }
  }, [scienceId, planet, house, minSev, skip]);

  useEffect(() => { fetchRemedies(); }, [fetchRemedies]);

  const handleTrack = (remedyId) => {
    alert(`Remedy #${remedyId} — go to /lk-remedies/tracker to start this remedy's 43-day cycle.`);
  };

  return (
    <div className="min-h-screen bg-background text-foreground px-4 py-8 max-w-3xl mx-auto">
      <SEO title="Browse Lal Kitab Remedies" noindex={true} />
      <div className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-5 mb-5">
        <h1 className="text-xl font-bold text-gold mb-3">Browse Remedies</h1>
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
          <div>
            <label className="block text-xs text-muted-foreground mb-1">Collection</label>
            <select
              value={scienceId}
              onChange={e => { setScienceId(e.target.value); setSkip(0); }}
              className="w-full bg-background border border-gold/20 rounded px-2 py-1.5 text-xs text-foreground"
            >
              {SCIENCE_IDS.map(s => <option key={s.value} value={s.value}>{s.label}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-xs text-muted-foreground mb-1">Planet</label>
            <select
              value={planet}
              onChange={e => { setPlanet(e.target.value); setSkip(0); }}
              className="w-full bg-background border border-gold/20 rounded px-2 py-1.5 text-xs text-foreground"
            >
              {PLANETS.map(p => <option key={p} value={p}>{p || 'All'}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-xs text-muted-foreground mb-1">House</label>
            <input
              type="number" min="1" max="12" value={house}
              onChange={e => { setHouse(e.target.value); setSkip(0); }}
              className="w-full bg-background border border-gold/20 rounded px-2 py-1.5 text-xs text-foreground"
              placeholder="1–12"
            />
          </div>
          <div>
            <label className="block text-xs text-muted-foreground mb-1">Min Severity</label>
            <input
              type="number" min="1" max="5" value={minSev}
              onChange={e => { setMinSev(e.target.value); setSkip(0); }}
              className="w-full bg-background border border-gold/20 rounded px-2 py-1.5 text-xs text-foreground"
              placeholder="1–5"
            />
          </div>
        </div>
      </div>

      {loading && <p className="text-muted-foreground text-sm mb-4">Loading…</p>}

      <p className="text-xs text-muted-foreground mb-3">{total} records found</p>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {records.map((r, i) => <RemCard key={`${r.id}-${i}`} r={r} onTrack={handleTrack} />)}
      </div>

      <div className="flex gap-3 mt-5 justify-center">
        <button
          onClick={() => setSkip(Math.max(0, skip - LIMIT))}
          disabled={skip === 0}
          className="border border-gold/30 text-gold text-sm rounded-lg px-4 py-1.5 disabled:opacity-30"
        >
          ← Prev
        </button>
        <span className="text-muted-foreground text-sm self-center">{skip + 1}–{Math.min(skip + LIMIT, total)}</span>
        <button
          onClick={() => setSkip(skip + LIMIT)}
          disabled={skip + LIMIT >= total}
          className="border border-gold/30 text-gold text-sm rounded-lg px-4 py-1.5 disabled:opacity-30"
        >
          Next →
        </button>
      </div>
    </div>
  );
}
