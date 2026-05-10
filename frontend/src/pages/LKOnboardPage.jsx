import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const PLANETS = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Rahu', 'Ketu'];
const RELATIVES = ['father', 'mother', 'brother', 'sister', 'grandfather_paternal', 'grandfather_maternal'];
const REL_LABELS = {
  father: 'Father', mother: 'Mother', brother: 'Brother',
  sister: 'Sister', grandfather_paternal: 'Paternal Grandfather',
  grandfather_maternal: 'Maternal Grandfather',
};
const STATUS_OPTIONS = ['living', 'deceased', 'unknown'];

const BACKEND = process.env.REACT_APP_BACKEND_URL || '';

export default function LKOnboardPage() {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [age, setAge] = useState('');
  const [natal, setNatal] = useState(Object.fromEntries(PLANETS.map(p => [p, ''])));
  const [census, setCensus] = useState(Object.fromEntries(RELATIVES.map(r => [r, 'unknown'])));
  const [locationSlug, setLocationSlug] = useState('new-delhi');
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');

  const token = localStorage.getItem('token') || '';

  const handleNatal = (planet, val) => {
    const house = parseInt(val, 10);
    setNatal(prev => ({ ...prev, [planet]: isNaN(house) ? '' : Math.min(12, Math.max(1, house)) }));
  };

  const handleCensus = (rel, val) => setCensus(prev => ({ ...prev, [rel]: val }));

  const handleSubmit = async () => {
    setSaving(true);
    setError('');
    try {
      const natalChart = Object.fromEntries(
        Object.entries(natal).filter(([, v]) => v !== '').map(([k, v]) => [k, parseInt(v, 10)])
      );
      const res = await fetch(`${BACKEND}/api/lk/onboard`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify({
          age: parseInt(age, 10),
          natal_chart: natalChart,
          family_census: census,
          location_slug: locationSlug,
        }),
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Onboarding failed');
      }
      navigate('/lk-remedies/report');
    } catch (e) {
      setError(e.message);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="min-h-screen bg-background text-foreground px-4 py-8 max-w-2xl mx-auto">
      <div className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-6">
        <h1 className="text-xl font-bold text-gold mb-1">LK Onboarding</h1>
        <p className="text-muted-foreground text-sm mb-5">Step {step} of 3</p>

        {/* Step indicator */}
        <div className="flex gap-2 mb-6">
          {[1, 2, 3].map(s => (
            <div key={s} className={`h-1.5 flex-1 rounded-full ${s <= step ? 'bg-gold' : 'bg-gold/20'}`} />
          ))}
        </div>

        {step === 1 && (
          <div className="space-y-4">
            <h2 className="font-semibold text-foreground">Age & Natal Chart</h2>
            <div>
              <label className="block text-sm text-muted-foreground mb-1">Your Age</label>
              <input
                type="number" min="0" max="121" value={age}
                onChange={e => setAge(e.target.value)}
                className="w-full rounded-lg border border-gold/20 bg-background px-3 py-2 text-foreground text-sm focus:outline-none focus:border-gold/50"
                placeholder="e.g. 36"
              />
            </div>
            <div>
              <p className="text-sm text-muted-foreground mb-2">Enter house number (1–12) for each planet in your birth chart. Leave blank if unknown.</p>
              <div className="grid grid-cols-3 gap-3">
                {PLANETS.map(p => (
                  <div key={p}>
                    <label className="block text-xs text-muted-foreground mb-1">{p}</label>
                    <input
                      type="number" min="1" max="12" value={natal[p]}
                      onChange={e => handleNatal(p, e.target.value)}
                      className="w-full rounded border border-gold/20 bg-background px-2 py-1.5 text-sm text-foreground focus:outline-none focus:border-gold/50"
                      placeholder="House"
                    />
                  </div>
                ))}
              </div>
            </div>
            <button
              onClick={() => setStep(2)}
              disabled={!age}
              className="w-full bg-gold text-background font-semibold rounded-lg px-4 py-2 mt-2 disabled:opacity-40"
            >
              Next →
            </button>
          </div>
        )}

        {step === 2 && (
          <div className="space-y-4">
            <h2 className="font-semibold text-foreground">Family Census</h2>
            <p className="text-sm text-muted-foreground">This determines which karmic debts require surrogates.</p>
            {RELATIVES.map(rel => (
              <div key={rel} className="flex items-center justify-between">
                <span className="text-sm">{REL_LABELS[rel]}</span>
                <div className="flex gap-2">
                  {STATUS_OPTIONS.map(s => (
                    <button
                      key={s}
                      onClick={() => handleCensus(rel, s)}
                      className={`text-xs px-2 py-1 rounded ${census[rel] === s ? 'bg-gold text-background font-semibold' : 'border border-gold/20 text-muted-foreground'}`}
                    >
                      {s}
                    </button>
                  ))}
                </div>
              </div>
            ))}
            <div className="flex gap-2 mt-2">
              <button onClick={() => setStep(1)} className="flex-1 border border-gold/30 text-gold rounded-lg px-4 py-2 text-sm">← Back</button>
              <button onClick={() => setStep(3)} className="flex-1 bg-gold text-background font-semibold rounded-lg px-4 py-2 text-sm">Next →</button>
            </div>
          </div>
        )}

        {step === 3 && (
          <div className="space-y-4">
            <h2 className="font-semibold text-foreground">Location</h2>
            <p className="text-sm text-muted-foreground">Used for sunrise/sunset window and geographical alignment.</p>
            <div>
              <label className="block text-sm text-muted-foreground mb-1">City Slug</label>
              <input
                type="text" value={locationSlug}
                onChange={e => setLocationSlug(e.target.value.toLowerCase().replace(/\s+/g, '-'))}
                className="w-full rounded-lg border border-gold/20 bg-background px-3 py-2 text-foreground text-sm focus:outline-none focus:border-gold/50"
                placeholder="e.g. new-delhi"
              />
              <p className="text-xs text-muted-foreground mt-1">Use same city slug as Panchang picker.</p>
            </div>
            {error && <p className="text-red-400 text-sm">{error}</p>}
            <div className="flex gap-2 mt-2">
              <button onClick={() => setStep(2)} className="flex-1 border border-gold/30 text-gold rounded-lg px-4 py-2 text-sm">← Back</button>
              <button
                onClick={handleSubmit}
                disabled={saving}
                className="flex-1 bg-gold text-background font-semibold rounded-lg px-4 py-2 text-sm disabled:opacity-50"
              >
                {saving ? 'Saving...' : 'Complete & Diagnose'}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
