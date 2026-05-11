import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

const BACKEND = process.env.REACT_APP_BACKEND_URL || '';

const DEBT_LABELS = {
  'Pitru Rin':  'Paternal Ancestral Debt',
  'Matru Rin':  'Maternal Ancestral Debt',
  'Bhatru Rin': 'Brother Debt',
  'Bhagini Rin':'Sister Debt',
  'Pitra Rin':  'Father Lineage Debt',
  'Kanya Rin':  'Daughter Debt',
  'Putra Rin':  'Son Debt',
  'Guru Rin':   'Teacher / Mentor Debt',
  'Mitra Rin':  'Social Circle / Friend Debt',
};

function DebtCard({ debt }) {
  const [open, setOpen] = useState(false);
  const { remedy_record: r, relative_available, use_substitute } = debt;
  if (!r) return null;

  const title = r.debt_type || r.title || `Record #${r.id}`;
  const label = DEBT_LABELS[title] || title;

  return (
    <div className={`rounded-xl border overflow-hidden mb-3 ${use_substitute ? 'border-amber-500/30 bg-amber-500/[0.04]' : 'border-gold/20 bg-gold/[0.04]'}`}>
      <button
        onClick={() => setOpen(o => !o)}
        className="w-full flex items-center gap-3 px-4 py-3 text-left"
      >
        <span className={`h-2 w-2 shrink-0 rounded-full ${use_substitute ? 'bg-amber-400' : 'bg-emerald-400'}`} />
        <span className="flex-1 text-sm font-semibold text-foreground">{label}</span>
        <span className={`text-xs px-2 py-0.5 rounded-full mr-2 ${use_substitute ? 'bg-amber-500/20 text-amber-400' : 'bg-emerald-500/20 text-emerald-400'}`}>
          {use_substitute ? 'Surrogate' : 'Primary'}
        </span>
        <span className="text-xs text-muted-foreground opacity-60">{open ? '▲' : '▼'}</span>
      </button>

      {open && (
        <div className="px-4 pb-4 pt-1 border-t border-gold/10 space-y-2">
          {r.planet && (
            <p className="text-xs text-muted-foreground">
              Planet: <strong className="text-gold">{r.planet}</strong>
              {r.house ? ` · House ${r.house}` : ''}
            </p>
          )}
          {r.symptom && (
            <p className="text-xs text-muted-foreground">Symptom: <span className="text-foreground">{r.symptom}</span></p>
          )}
          {r.blood_relation_target && (
            <p className="text-xs text-muted-foreground">
              Requires: <strong className="text-foreground">{r.blood_relation_target}</strong>
              {' — '}
              {relative_available
                ? <span className="text-emerald-400">✅ Available</span>
                : <span className="text-amber-400">⚠️ Unavailable — surrogate ritual applies</span>}
            </p>
          )}
          {use_substitute && r.substitute_item && (
            <div className="mt-2 p-3 rounded-lg bg-amber-500/10 border border-amber-500/20">
              <p className="text-[10px] uppercase tracking-widest text-amber-400 mb-1">Surrogate Ritual</p>
              <p className="text-xs text-muted-foreground leading-relaxed">{r.substitute_item}</p>
            </div>
          )}
          {!use_substitute && r.ritual_item && (
            <div className="mt-2 p-3 rounded-lg bg-gold/5 border border-gold/15">
              <p className="text-[10px] uppercase tracking-widest text-gold/60 mb-1">Remedy</p>
              <p className="text-xs text-muted-foreground leading-relaxed">{r.ritual_item}</p>
            </div>
          )}
          {r.strategy && (
            <p className="text-xs text-muted-foreground leading-relaxed pt-1 border-t border-gold/10">{r.strategy}</p>
          )}
        </div>
      )}
    </div>
  );
}

export default function LKDebtAuditPage() {
  const [debts, setDebts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    (async () => {
      try {
        const res = await fetch(`${BACKEND}/api/lk/debt-audit`, {
          method: 'POST',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({}),
        });
        if (!res.ok) {
          const err = await res.json();
          throw new Error(err.detail || 'Debt audit failed');
        }
        const data = await res.json();
        setDebts(data.debts || []);
      } catch (e) { setError(e.message); } finally { setLoading(false); }
    })();
  }, []);

  if (loading) return (
    <div className="min-h-screen bg-background flex items-center justify-center text-muted-foreground text-sm">
      Consulting the Ancestor Record…
    </div>
  );

  return (
    <div className="min-h-screen bg-background text-foreground px-4 py-8 max-w-2xl mx-auto">
      <div className="flex items-center mb-5">
        <Link to="/lk-remedies/report" className="text-xs text-muted-foreground hover:text-gold transition">← Diagnostic Report</Link>
      </div>

      <div className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-5 mb-5">
        <h1 className="text-xl font-bold text-gold mb-1">Karmic Debt Audit</h1>
        <p className="text-sm text-muted-foreground italic leading-relaxed">
          "The debts of ancestors ripple through living blood. Each debt type maps to a planetary house and a living relative — primary remedy requires the relative, surrogate ritual applies when unavailable."
        </p>
      </div>

      {error && (
        <div className="rounded-xl border border-red-500/30 bg-red-500/5 p-4 mb-4">
          <p className="text-red-400 text-sm">{error}</p>
          <Link to="/lk-remedies/onboard" className="text-gold text-xs underline mt-1 block">Complete Onboarding First →</Link>
        </div>
      )}

      {debts.length === 0 && !error && (
        <div className="rounded-xl border border-emerald-500/30 bg-emerald-500/5 p-5 text-center">
          <p className="text-emerald-400 font-semibold">✅ No active karmic debts detected.</p>
          <p className="text-muted-foreground text-sm mt-1">Ancestral slate appears clear for this configuration.</p>
        </div>
      )}

      {debts.length > 0 && (
        <p className="text-xs text-muted-foreground mb-3">
          {debts.length} debt{debts.length > 1 ? 's' : ''} detected — tap each to view remedy instructions.
        </p>
      )}

      {debts.map((d, i) => <DebtCard key={i} debt={d} />)}
    </div>
  );
}
