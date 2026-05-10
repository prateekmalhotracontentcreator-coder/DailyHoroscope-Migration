import React, { useEffect, useState } from 'react';

const BACKEND = process.env.REACT_APP_BACKEND_URL || '';

const DEBT_TYPES = [
  'Pitru Rin', 'Matru Rin', 'Bhatru Rin', 'Bhagini Rin',
  'Pitra Rin', 'Kanya Rin', 'Putra Rin', 'Guru Rin', 'Mitra Rin',
];

function DebtCard({ debt }) {
  const { remedy_record: r, relative_available, use_substitute } = debt;
  if (!r) return null;
  return (
    <div className={`rounded-xl border p-4 mb-3 ${use_substitute ? 'border-amber-500/30 bg-amber-500/5' : 'border-gold/20 bg-gold/[0.04]'}`}>
      <div className="flex items-center justify-between mb-1">
        <h3 className="font-semibold text-sm text-foreground">{r.debt_type || r.title || `Record #${r.id}`}</h3>
        <span className={`text-xs px-2 py-0.5 rounded-full ${use_substitute ? 'bg-amber-500/20 text-amber-400' : 'bg-emerald-500/20 text-emerald-400'}`}>
          {use_substitute ? 'Surrogate' : 'Primary'}
        </span>
      </div>
      {r.planet && <p className="text-xs text-muted-foreground mb-1">Planet: <strong className="text-gold">{r.planet}</strong>{r.house ? ` · House ${r.house}` : ''}</p>}
      {r.symptom && <p className="text-xs text-muted-foreground mb-1">Symptom: {r.symptom}</p>}
      {r.blood_relation_target && (
        <p className="text-xs text-muted-foreground mb-1">
          Requires: <strong>{r.blood_relation_target}</strong> — {relative_available ? '✅ Available' : '⚠️ Unavailable'}
        </p>
      )}
      {use_substitute && r.substitute_item && (
        <div className="mt-2 p-2 rounded-lg bg-amber-500/10 border border-amber-500/20">
          <p className="text-xs text-amber-400 font-semibold mb-0.5">Surrogate Ritual:</p>
          <p className="text-xs text-muted-foreground">{r.substitute_item}</p>
        </div>
      )}
      {!use_substitute && r.ritual_item && (
        <p className="text-xs text-muted-foreground mt-2">Remedy: {r.ritual_item}</p>
      )}
    </div>
  );
}

export default function LKDebtAuditPage() {
  const [debts, setDebts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const token = localStorage.getItem('token') || '';

  useEffect(() => {
    (async () => {
      try {
        const res = await fetch(`${BACKEND}/api/lk/debt-audit`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
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
  }, [token]);

  if (loading) return (
    <div className="min-h-screen bg-background flex items-center justify-center text-muted-foreground text-sm">
      Consulting the Ancestor Record…
    </div>
  );

  return (
    <div className="min-h-screen bg-background text-foreground px-4 py-8 max-w-2xl mx-auto">
      <div className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-5 mb-5">
        <h1 className="text-xl font-bold text-gold mb-1">Karmic Debt Audit</h1>
        <p className="text-sm text-muted-foreground italic">
          "The debts of ancestors ripple through living blood. Acknowledge what was left undone."
        </p>
      </div>

      {error && <p className="text-red-400 text-sm mb-4">{error}</p>}

      {debts.length === 0 && !error && (
        <div className="rounded-xl border border-emerald-500/30 bg-emerald-500/5 p-5 text-center">
          <p className="text-emerald-400 font-semibold">✅ No active karmic debts detected.</p>
          <p className="text-muted-foreground text-sm mt-1">Ancestral slate appears clear for this configuration.</p>
        </div>
      )}

      {debts.map((d, i) => <DebtCard key={i} debt={d} />)}
    </div>
  );
}
