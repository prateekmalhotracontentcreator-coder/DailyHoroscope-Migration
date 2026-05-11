import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Loader2, Sparkles } from 'lucide-react';
import SharedBirthCityPicker from '../components/SharedBirthCityPicker';

const RELATIVES = ['father', 'mother', 'brother', 'sister', 'grandfather_paternal', 'grandfather_maternal'];
const REL_LABELS = {
  father: 'Father', mother: 'Mother', brother: 'Brother',
  sister: 'Sister', grandfather_paternal: 'Paternal Grandfather',
  grandfather_maternal: 'Maternal Grandfather',
};
const STATUS_OPTIONS = ['living', 'deceased', 'unknown'];

const BACKEND = process.env.REACT_APP_BACKEND_URL || '';

const PLANET_ORDER = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Rahu', 'Ketu'];

export default function LKOnboardPage() {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);

  // Step 1 — birth details
  const [birthForm, setBirthForm] = useState({
    date_of_birth: '',
    time_of_birth: '',
    city_name: 'New Delhi',
    city_slug: 'new-delhi',
    timezone_offset: '+05:30',
  });
  const [age, setAge] = useState('');
  const [computingChart, setComputingChart] = useState(false);
  const [computedChart, setComputedChart] = useState(null); // {lagna, vedic_display, lk_chart}

  // Step 2 — family census
  const [census, setCensus] = useState(Object.fromEntries(RELATIVES.map(r => [r, 'unknown'])));

  // Step 3 — location slug
  const [locationSlug, setLocationSlug] = useState('new-delhi');

  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');

  const handleComputeChart = async () => {
    if (!birthForm.date_of_birth) { setError('Date of birth is required'); return; }
    setError('');
    setComputingChart(true);
    try {
      const res = await fetch(`${BACKEND}/api/lk/compute-chart`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          date_of_birth: birthForm.date_of_birth,
          time_of_birth: birthForm.time_of_birth || '12:00',
          place_of_birth: birthForm.city_name,
          timezone_offset: birthForm.timezone_offset,
        }),
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Chart computation failed');
      }
      const data = await res.json();
      setComputedChart(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setComputingChart(false);
    }
  };

  const handleSubmit = async () => {
    setSaving(true);
    setError('');
    try {
      const natalChart = computedChart?.lk_chart || {};
      const res = await fetch(`${BACKEND}/api/lk/onboard`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          age: parseInt(age, 10) || 0,
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
        <h1 className="text-xl font-bold text-gold mb-1">Lal Kitab Onboarding</h1>
        <p className="text-muted-foreground text-sm mb-5">Step {step} of 3</p>

        {/* Step indicator */}
        <div className="flex gap-2 mb-6">
          {[1, 2, 3].map(s => (
            <div key={s} className={`h-1.5 flex-1 rounded-full ${s <= step ? 'bg-gold' : 'bg-gold/20'}`} />
          ))}
        </div>

        {/* ── STEP 1: Birth Details ── */}
        {step === 1 && (
          <div className="space-y-5">
            <h2 className="font-semibold text-foreground">Birth Details</h2>
            <p className="text-sm text-muted-foreground">
              Your birth details are used to auto-compute your Lal Kitab chart. We show both the Jyotish house (Lagna-relative) and the Lal Kitab house (natural zodiac, Aries=1) so you can see the distinction.
            </p>

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
              <label className="block text-sm text-muted-foreground mb-1">Date of Birth <span className="text-red-400">*</span></label>
              <input
                type="date"
                value={birthForm.date_of_birth}
                onChange={e => setBirthForm(f => ({ ...f, date_of_birth: e.target.value }))}
                className="w-full rounded-lg border border-gold/20 bg-background px-3 py-2 text-foreground text-sm focus:outline-none focus:border-gold/50"
              />
            </div>

            <div>
              <label className="block text-sm text-muted-foreground mb-1">
                Time of Birth <span className="text-muted-foreground/60 text-xs">(improves Lagna accuracy)</span>
              </label>
              <input
                type="time"
                value={birthForm.time_of_birth}
                onChange={e => setBirthForm(f => ({ ...f, time_of_birth: e.target.value }))}
                className="w-full rounded-lg border border-gold/20 bg-background px-3 py-2 text-foreground text-sm focus:outline-none focus:border-gold/50"
              />
            </div>

            <SharedBirthCityPicker
              inputId="lk-birth-city"
              label="Place of Birth"
              value={birthForm.city_slug}
              onChange={city => setBirthForm(f => ({
                ...f,
                city_name: city.city_name,
                city_slug: city.slug,
                timezone_offset: city.timezone_offset || '+05:30',
              }))}
            />

            {error && <p className="text-red-400 text-sm">{error}</p>}

            {/* Compute button */}
            {!computedChart && (
              <button
                onClick={handleComputeChart}
                disabled={!birthForm.date_of_birth || computingChart}
                className="w-full bg-gold text-background font-semibold rounded-lg px-4 py-2.5 flex items-center justify-center gap-2 disabled:opacity-40"
              >
                {computingChart
                  ? <><Loader2 className="h-4 w-4 animate-spin" /> Computing Chart...</>
                  : <><Sparkles className="h-4 w-4" /> Compute My Chart</>
                }
              </button>
            )}

            {/* Chart preview */}
            {computedChart && (
              <div className="space-y-4">
                <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-4">
                  <p className="text-[10px] uppercase tracking-widest text-gold/60 mb-3">
                    Computed Chart · Lagna: {computedChart.lagna}
                  </p>
                  <div className="overflow-x-auto">
                    <table className="w-full text-xs">
                      <thead>
                        <tr className="text-muted-foreground/60">
                          <th className="text-left pb-2 font-medium pr-3">Planet</th>
                          <th className="text-left pb-2 font-medium pr-3">Sign</th>
                          <th className="text-left pb-2 font-medium pr-3">Jyotish H.</th>
                          <th className="text-left pb-2 font-medium text-amber-400/80">LK House</th>
                        </tr>
                      </thead>
                      <tbody>
                        {PLANET_ORDER.map(pName => {
                          const p = computedChart.vedic_display?.find(d => d.planet === pName);
                          if (!p) return null;
                          return (
                            <tr key={p.planet} className="border-t border-gold/10">
                              <td className="py-1.5 font-medium pr-3">{p.planet}</td>
                              <td className="py-1.5 text-muted-foreground pr-3">{p.sign}</td>
                              <td className="py-1.5 text-muted-foreground pr-3">H{p.jyotish_house}</td>
                              <td className="py-1.5 font-semibold text-amber-400">H{p.lk_house}</td>
                            </tr>
                          );
                        })}
                      </tbody>
                    </table>
                  </div>
                  <p className="text-[10px] text-muted-foreground/50 mt-3">
                    <span className="text-muted-foreground/70">Jyotish House</span> = Lagna-relative · <span className="text-amber-400/80">LK House</span> = natural zodiac (Aries always H1)
                  </p>
                </div>

                <div className="flex gap-2">
                  <button
                    onClick={() => setComputedChart(null)}
                    className="flex-1 border border-gold/30 text-gold rounded-lg px-4 py-2 text-sm"
                  >
                    Recompute
                  </button>
                  <button
                    onClick={() => setStep(2)}
                    className="flex-1 bg-gold text-background font-semibold rounded-lg px-4 py-2 text-sm"
                  >
                    Next →
                  </button>
                </div>
              </div>
            )}
          </div>
        )}

        {/* ── STEP 2: Family Census ── */}
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
                      onClick={() => setCensus(prev => ({ ...prev, [rel]: s }))}
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

        {/* ── STEP 3: Location ── */}
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
