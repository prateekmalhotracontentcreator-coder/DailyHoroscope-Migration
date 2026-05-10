import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

const BACKEND = process.env.REACT_APP_BACKEND_URL || '';

const STATUS_STYLE = {
  WARNING: 'bg-amber-500/10 border-amber-500/40 text-amber-400',
  DORMANT: 'bg-blue-500/10 border-blue-400/40 text-blue-400',
  ACTIVE: 'bg-emerald-500/10 border-emerald-500/40 text-emerald-400',
  CLEAR: 'bg-emerald-500/10 border-emerald-500/40 text-emerald-400',
  EMPTY_VESSEL: 'bg-amber-500/10 border-amber-500/40 text-amber-400',
  RAHU_COLLISION: 'bg-red-500/10 border-red-400/40 text-red-400',
  SCAN: 'bg-blue-500/10 border-blue-400/40 text-blue-400',
};

const STATUS_ICON = {
  WARNING: '⚠️', DORMANT: '💤', ACTIVE: '⚡', CLEAR: '✅',
  EMPTY_VESSEL: '🔍', RAHU_COLLISION: '⚠️', SCAN: '🔍',
};

function GateCard({ title, gate, gate_key }) {
  if (!gate) return null;
  const status = gate.status || 'SCAN';
  const style = STATUS_STYLE[status] || STATUS_STYLE.SCAN;
  const icon = STATUS_ICON[status] || '🔍';

  return (
    <div className={`rounded-xl border p-4 mb-4 ${style}`}>
      <div className="flex items-center gap-2 mb-2">
        <span>{icon}</span>
        <h3 className="font-semibold text-sm">{title}</h3>
        <span className="ml-auto text-xs font-mono opacity-70">{status}</span>
      </div>
      {gate.narrative && <p className="text-xs opacity-80 mb-2">{gate.narrative}</p>}
      {gate.planet && <p className="text-xs opacity-70">Year-Lord: <strong>{gate.planet}</strong> ({gate.age_range})</p>}
      {gate.dormant_houses?.length > 0 && (
        <p className="text-xs opacity-70">Dormant Houses: {gate.dormant_houses.join(', ')}</p>
      )}
    </div>
  );
}

export default function LKReportPage() {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const token = localStorage.getItem('token') || '';

  useEffect(() => {
    (async () => {
      try {
        const res = await fetch(`${BACKEND}/api/lk/diagnose`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
          body: JSON.stringify({}),
        });
        if (!res.ok) {
          const err = await res.json();
          throw new Error(err.detail || 'Diagnosis failed');
        }
        setReport(await res.json());
      } catch (e) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    })();
  }, [token]);

  if (loading) return (
    <div className="min-h-screen bg-background flex items-center justify-center text-muted-foreground text-sm">
      Running 5-Gate Diagnostic…
    </div>
  );

  if (error) return (
    <div className="min-h-screen bg-background flex flex-col items-center justify-center gap-4 px-4">
      <p className="text-red-400 text-sm">{error}</p>
      <Link to="/lk-remedies/onboard" className="text-gold text-sm underline">Complete Onboarding First</Link>
    </div>
  );

  if (!report) return null;

  const { gates, execution_roadmap } = report;

  return (
    <div className="min-h-screen bg-background text-foreground px-4 py-8 max-w-2xl mx-auto">
      <div className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-5 mb-4">
        <h1 className="text-xl font-bold text-gold mb-1">5-Gate Diagnostic Report</h1>
        <p className="text-xs text-muted-foreground">Generated {new Date(report.generated_at).toLocaleString()}</p>
      </div>

      <GateCard title="Gate 1 — Karmic Debt" gate={gates?.gate1_karmic_debt} gate_key="gate1" />
      <GateCard title="Gate 2 — House Awakening" gate={gates?.gate2_house_awakening} gate_key="gate2" />
      <GateCard title="Gate 3 — 35-Year Cycle" gate={gates?.gate3_year_cycle} gate_key="gate3" />
      <GateCard title="Gate 4 — Mercury Scan" gate={gates?.gate4_mercury_scan} gate_key="gate4" />
      <GateCard title="Gate 5 — Geographical Alignment" gate={gates?.gate5_geographical} gate_key="gate5" />

      {execution_roadmap?.length > 0 && (
        <div className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-5 mt-4">
          <h2 className="font-semibold text-gold mb-3">Execution Roadmap</h2>
          <div className="space-y-2">
            {execution_roadmap.map((step, i) => (
              <div key={i} className="flex items-start gap-3 text-sm">
                <span className="text-gold font-mono text-xs mt-0.5 whitespace-nowrap">Day {step.days}</span>
                <div>
                  <p className="text-foreground">{step.task}</p>
                  {step.remedy_id && (
                    <button
                      className="text-xs text-gold/70 underline mt-0.5"
                      onClick={() => alert(`Add remedy #${step.remedy_id} to tracker — use Tracker page`)}
                    >
                      Add to 43-Day Tracker
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="flex gap-3 mt-5">
        <Link to="/lk-remedies/debt-audit" className="flex-1 text-center border border-gold/30 text-gold rounded-lg px-4 py-2 text-sm">Debt Audit →</Link>
        <Link to="/lk-remedies/tracker" className="flex-1 text-center bg-gold text-background font-semibold rounded-lg px-4 py-2 text-sm">Start Tracker →</Link>
      </div>
    </div>
  );
}
