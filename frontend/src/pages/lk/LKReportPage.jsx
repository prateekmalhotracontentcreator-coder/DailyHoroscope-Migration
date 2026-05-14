import { SEO } from '../../components/SEO';
import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

const GATE_CONTEXT = {
  gate1_karmic_debt:     { what: 'Karmic Debt Gate', why: 'Identifies active ancestral debts based on your family census. Each unpaid debt corresponds to a missing ritual from a relative.' },
  gate2_house_awakening: { what: 'House Awakening Gate', why: 'Maps which natal houses are dormant. Dormant houses block energy flow until a specific ritual activates them.' },
  gate3_year_cycle:      { what: '35-Year Cycle Gate', why: 'Lal Kitab assigns each year of life to a planetary lord. Your current year-lord determines which remedies are effective right now.' },
  gate4_mercury_scan:    { what: 'Mercury Scan Gate', why: 'Mercury governs communication, business clarity, and mental precision. This gate flags if Mercury is an empty vessel or in Rahu collision.' },
  gate5_geographical:    { what: 'Geographical Alignment Gate', why: 'Your office and home direction relative to birth city determines whether your Digbala (directional strength) amplifies or weakens outcomes.' },
};

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

function GateCard({ title, gate, gateKey }) {
  const [open, setOpen] = useState(false);
  if (!gate) return null;
  const status = gate.status || 'SCAN';
  const style = STATUS_STYLE[status] || STATUS_STYLE.SCAN;
  const icon = STATUS_ICON[status] || '🔍';
  const ctx = GATE_CONTEXT[gateKey] || {};

  return (
    <div className={`rounded-xl border mb-3 overflow-hidden ${style}`}>
      <button
        onClick={() => setOpen(o => !o)}
        className="w-full flex items-center gap-3 px-4 py-3 text-left"
      >
        <span>{icon}</span>
        <span className="flex-1 font-semibold text-sm">{title}</span>
        <span className="text-xs font-mono opacity-70 mr-2">{status}</span>
        <span className="text-xs opacity-60">{open ? '▲' : '▼'}</span>
      </button>
      {open && (
        <div className="px-4 pb-4 pt-2 border-t border-current/10 space-y-2.5">
          {ctx.why && (
            <div className="rounded-lg bg-current/5 px-3 py-2">
              <p className="text-[10px] uppercase tracking-widest opacity-60 mb-0.5">What this gate checks</p>
              <p className="text-xs opacity-80 leading-relaxed">{ctx.why}</p>
            </div>
          )}
          {gate.narrative && (
            <div>
              <p className="text-[10px] uppercase tracking-widest opacity-60 mb-0.5">Your Result</p>
              <p className="text-xs opacity-90 leading-relaxed font-medium">{gate.narrative}</p>
            </div>
          )}
          {gate.planet && (
            <p className="text-xs opacity-70">Year-Lord: <strong>{gate.planet}</strong>{gate.age_range ? ` (${gate.age_range})` : ''}</p>
          )}
          {gate.dormant_houses?.length > 0 && (
            <p className="text-xs opacity-70">Dormant Houses: {gate.dormant_houses.join(', ')}</p>
          )}
        </div>
      )}
    </div>
  );
}

export default function LKReportPage() {
  const navigate = useNavigate();
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [trackerMsg, setTrackerMsg] = useState(null);
  const [addingTracker, setAddingTracker] = useState(false);
  useEffect(() => {
    (async () => {
      try {
        const res = await fetch(`${BACKEND}/api/lk/diagnose`, {
          method: 'POST',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' },
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
  }, []);

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
      <SEO title="Lal Kitab Diagnostic Report" noindex={true} />
      <div className="flex items-center mb-5">
        <Link to="/strategist" className="text-xs text-muted-foreground hover:text-gold transition">← The Strategist</Link>
      </div>

      <div className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-5 mb-4">
        <h1 className="text-xl font-bold text-gold mb-1">5-Gate Diagnostic Report</h1>
        <p className="text-xs text-muted-foreground mb-2">Generated {new Date(report.generated_at).toLocaleString()}</p>
        <p className="text-xs text-muted-foreground leading-relaxed">
          Lal Kitab runs five diagnostic gates on your natal chart, age, family census, and location.
          Each gate can block or amplify your strategic outcomes. Tap each gate to read your result and understand what it means.
        </p>
      </div>

      <GateCard title="Gate 1 — Karmic Debt" gate={gates?.gate1_karmic_debt} gateKey="gate1_karmic_debt" />
      <GateCard title="Gate 2 — House Awakening" gate={gates?.gate2_house_awakening} gateKey="gate2_house_awakening" />
      <GateCard title="Gate 3 — 35-Year Cycle" gate={gates?.gate3_year_cycle} gateKey="gate3_year_cycle" />
      <GateCard title="Gate 4 — Mercury Scan" gate={gates?.gate4_mercury_scan} gateKey="gate4_mercury_scan" />
      <GateCard title="Gate 5 — Geographical Alignment" gate={gates?.gate5_geographical} gateKey="gate5_geographical" />

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
                      onClick={() => setTrackerMsg(step.remedy_id)}
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

      {trackerMsg && (
        <div className="fixed inset-0 z-50 flex items-end justify-center pb-8 px-4 pointer-events-none">
          <div className="pointer-events-auto rounded-xl border border-gold/30 bg-card shadow-xl p-5 max-w-sm w-full">
            <p className="text-sm font-semibold text-foreground mb-1">Start 43-Day Tracker</p>
            <p className="text-xs text-muted-foreground mb-4 leading-relaxed">
              This remedy comes from your Execution Roadmap. Tapping "Start Tracker" will activate it and open the daily check-in.
            </p>
            <div className="flex gap-3">
              <button
                disabled={addingTracker}
                onClick={async () => {
                  setAddingTracker(true);
                  try {
                    await fetch(`${BACKEND}/api/lk/tracker/start`, {
                      method: 'POST',
                      credentials: 'include',
                      headers: { 'Content-Type': 'application/json' },
                      body: JSON.stringify({ remedy_id: trackerMsg }),
                    });
                  } catch {}
                  setTrackerMsg(null);
                  setAddingTracker(false);
                  navigate('/lk-remedies/tracker');
                }}
                className="flex-1 bg-gold text-background font-semibold rounded-lg px-4 py-2 text-xs disabled:opacity-50"
              >
                {addingTracker ? 'Starting…' : 'Start Tracker →'}
              </button>
              <button
                onClick={() => setTrackerMsg(null)}
                className="flex-1 border border-gold/30 text-gold rounded-lg px-4 py-2 text-xs"
              >
                Dismiss
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
