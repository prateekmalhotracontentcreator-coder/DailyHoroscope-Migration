import React, { useState } from 'react';

const BACKEND = process.env.REACT_APP_BACKEND_URL || '';
const PLANETS = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Rahu', 'Ketu'];
const RELATIVES = ['Father', 'Mother', 'Sister', 'Brother', 'Grandfather', 'Uncle', 'Spouse', 'Son', 'In-laws'];
const INDUSTRIES = ['Tech', 'Operations', 'Legal_Consulting', 'Leadership', 'Creative', 'Sales_Defense', 'E-commerce'];

export default function StrategistSurrogatePage() {
  const [planet, setPlanet] = useState('Sun');
  const [relative, setRelative] = useState('Father');
  const [industry, setIndustry] = useState('Tech');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const token = localStorage.getItem('token') || '';

  const findSurrogate = async () => {
    setLoading(true); setError(''); setResult(null);
    try {
      const res = await fetch(`${BACKEND}/api/strategist/surrogate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify({ planet, relative_unavailable: relative, industry }),
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'No surrogate found');
      }
      setResult(await res.json());
    } catch (e) { setError(e.message); } finally { setLoading(false); }
  };

  return (
    <div className="min-h-screen bg-background text-foreground px-4 py-8 max-w-xl mx-auto">
      <div className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-5 mb-5">
        <h1 className="text-xl font-bold text-gold mb-2">Surrogate Bridge</h1>
        <p className="text-sm text-muted-foreground mb-4">
          When a family member required for a remedy is unavailable, a surrogate ritual bridges the karmic gap.
        </p>

        <div className="space-y-3">
          <div>
            <label className="block text-xs text-muted-foreground mb-1">Command Planet</label>
            <select
              value={planet}
              onChange={e => setPlanet(e.target.value)}
              className="w-full bg-background border border-gold/20 rounded px-3 py-2 text-sm text-foreground"
            >
              {PLANETS.map(p => <option key={p} value={p}>{p}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-xs text-muted-foreground mb-1">Unavailable Relative</label>
            <select
              value={relative}
              onChange={e => setRelative(e.target.value)}
              className="w-full bg-background border border-gold/20 rounded px-3 py-2 text-sm text-foreground"
            >
              {RELATIVES.map(r => <option key={r} value={r}>{r}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-xs text-muted-foreground mb-1">Industry</label>
            <select
              value={industry}
              onChange={e => setIndustry(e.target.value)}
              className="w-full bg-background border border-gold/20 rounded px-3 py-2 text-sm text-foreground"
            >
              {INDUSTRIES.map(i => <option key={i} value={i}>{i}</option>)}
            </select>
          </div>
          <button
            onClick={findSurrogate}
            disabled={loading}
            className="w-full bg-gold text-background font-semibold rounded-lg px-4 py-2.5 disabled:opacity-50"
          >
            {loading ? 'Searching…' : 'Find Surrogate Ritual'}
          </button>
        </div>
      </div>

      {error && (
        <div className="rounded-xl border border-amber-500/30 bg-amber-500/10 p-4 mb-4">
          <p className="text-amber-400 text-sm">{error}</p>
          <p className="text-xs text-muted-foreground mt-1">Run Strategist ingest first to populate surrogate records (IDs 651–675).</p>
        </div>
      )}

      {result?.surrogate && (
        <div className="rounded-xl border border-emerald-500/30 bg-emerald-500/10 p-5">
          <p className="text-emerald-400 font-semibold mb-2">✅ Surrogate Bridge Activated</p>
          <div className="space-y-1 text-sm">
            {result.surrogate.mission_name && <p><strong className="text-foreground">Mission:</strong> <span className="text-muted-foreground">{result.surrogate.mission_name}</span></p>}
            {result.surrogate.strategy && <p><strong className="text-foreground">Strategy:</strong> <span className="text-muted-foreground">{result.surrogate.strategy}</span></p>}
            {result.surrogate.pivot_action && <p><strong className="text-foreground">Action:</strong> <span className="text-muted-foreground">{result.surrogate.pivot_action}</span></p>}
            {result.surrogate.industry && <p><strong className="text-foreground">Industry:</strong> <span className="text-muted-foreground">{result.surrogate.industry}</span></p>}
          </div>
          <p className="text-xs text-muted-foreground mt-3">
            Surrogate active → +12 to Conquest Probability. Continue the remedy cycle using this substitute ritual.
          </p>
        </div>
      )}
    </div>
  );
}
