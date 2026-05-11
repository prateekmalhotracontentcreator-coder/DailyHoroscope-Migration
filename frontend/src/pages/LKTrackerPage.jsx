import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const BACKEND = process.env.REACT_APP_BACKEND_URL || '';
const TOTAL_DAYS = 43;

const PHASE_LABEL = (day) => {
  if (day <= 7) return 'Shift';
  if (day <= 15) return 'Friction';
  if (day <= 30) return 'Anchor';
  return 'Lock';
};

function Ring({ day, total }) {
  const pct = Math.min(day / total, 1);
  const r = 52;
  const circ = 2 * Math.PI * r;
  const dash = pct * circ;
  return (
    <svg width="130" height="130" className="mx-auto">
      <circle cx="65" cy="65" r={r} fill="none" stroke="rgba(197,160,89,0.15)" strokeWidth="10" />
      <circle
        cx="65" cy="65" r={r} fill="none"
        stroke="#c5a059" strokeWidth="10"
        strokeDasharray={`${dash} ${circ}`}
        strokeLinecap="round"
        transform="rotate(-90 65 65)"
      />
      <text x="65" y="61" textAnchor="middle" fill="#c5a059" fontSize="20" fontWeight="bold">{day}</text>
      <text x="65" y="76" textAnchor="middle" fill="#888" fontSize="10">of {total}</text>
    </svg>
  );
}

export default function LKTrackerPage() {
  const [trackers, setTrackers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [logging, setLogging] = useState(false);
  const [checkIn, setCheckIn] = useState({ completed: false, within_window: false, prohibited_avoided: false });
  const [activeRemedy, setActiveRemedy] = useState(null);
  const [msg, setMsg] = useState('');
  const { user } = useAuth();
  const userEmail = user?.email || '';

  const fetchTrackers = async () => {
    if (!userEmail) { setLoading(false); return; }
    try {
      const res = await fetch(`${BACKEND}/api/lk/tracker/${encodeURIComponent(userEmail)}`, {
        credentials: 'include',
      });
      if (res.ok) {
        const data = await res.json();
        setTrackers(data.trackers || []);
        if (data.trackers?.length) setActiveRemedy(data.trackers[0].remedy_id);
      }
    } finally { setLoading(false); }
  };

  useEffect(() => { fetchTrackers(); }, []);

  const handleLog = async () => {
    if (!activeRemedy) return;
    setLogging(true); setMsg('');
    try {
      const res = await fetch(`${BACKEND}/api/lk/tracker/log`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ remedy_id: activeRemedy, ...checkIn }),
      });
      const data = await res.json();
      if (data.ok) {
        setMsg('Logged successfully!');
        fetchTrackers();
      } else {
        setMsg(data.message || 'Logged.');
      }
    } catch { setMsg('Error logging.'); } finally { setLogging(false); }
  };

  const active = trackers.find(t => t.remedy_id === activeRemedy && t.status === 'active');
  const streak = active?.streak_days || 0;

  if (loading) return (
    <div className="min-h-screen bg-background flex items-center justify-center text-muted-foreground text-sm">Loading tracker…</div>
  );

  if (trackers.length === 0) return (
    <div className="min-h-screen bg-background text-foreground px-4 py-8 max-w-md mx-auto">
      <div className="flex items-center mb-4">
        <Link to="/lk-remedies/report" className="text-xs text-muted-foreground hover:text-gold transition">← Diagnostic Report</Link>
      </div>
      <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-6 text-center">
        <p className="text-gold font-semibold mb-2">No Active Remedies</p>
        <p className="text-sm text-muted-foreground mb-4 leading-relaxed">
          Run your 5-Gate Diagnosis, then tap "Add to 43-Day Tracker" on a remedy in the Execution Roadmap.
        </p>
        <Link to="/lk-remedies/report" className="inline-block bg-gold text-background font-semibold rounded-lg px-5 py-2.5 text-sm">
          Go to Diagnostic Report →
        </Link>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-background text-foreground px-4 py-8 max-w-md mx-auto">
      <div className="flex items-center mb-4">
        <Link to="/lk-remedies/report" className="text-xs text-muted-foreground hover:text-gold transition">← Diagnostic Report</Link>
      </div>
      <div className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-6 text-center mb-4">
        <h1 className="text-xl font-bold text-gold mb-1">43-Day Remedy Tracker</h1>
        <p className="text-sm text-muted-foreground mb-4">Phase: <span className="text-gold font-medium">{PHASE_LABEL(streak)}</span></p>
        <Ring day={streak} total={TOTAL_DAYS} />
        {active?.status === 'complete' && (
          <p className="text-emerald-400 font-semibold mt-3">✅ 43-Day Cycle Complete!</p>
        )}
        {active?.status === 'broken' && (
          <p className="text-red-400 text-sm mt-3">🔴 Streak broken. 3-day cooling period before restart.</p>
        )}
      </div>

      {trackers.length > 1 && (
        <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-4 mb-4">
          <p className="text-xs text-muted-foreground mb-2">Active Remedy</p>
          <select
            value={activeRemedy || ''}
            onChange={e => setActiveRemedy(parseInt(e.target.value, 10))}
            className="w-full bg-background border border-gold/20 rounded px-2 py-1 text-sm text-foreground"
          >
            {trackers.map(t => (
              <option key={t.remedy_id} value={t.remedy_id}>Remedy #{t.remedy_id} — {t.status}</option>
            ))}
          </select>
        </div>
      )}

      <div className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-5">
        <h2 className="font-semibold text-gold mb-3">Daily Check-In</h2>
        {[
          { key: 'completed', label: '✓ Ritual completed today' },
          { key: 'within_window', label: '✓ Performed within sunrise–sunset' },
          { key: 'prohibited_avoided', label: '✓ Prohibited acts avoided' },
        ].map(({ key, label }) => (
          <label key={key} className="flex items-center gap-3 mb-3 cursor-pointer">
            <input
              type="checkbox"
              checked={checkIn[key]}
              onChange={e => setCheckIn(prev => ({ ...prev, [key]: e.target.checked }))}
              className="w-4 h-4 accent-gold"
            />
            <span className="text-sm">{label}</span>
          </label>
        ))}
        {msg && <p className="text-sm text-emerald-400 mb-2">{msg}</p>}
        <button
          onClick={handleLog}
          disabled={logging || !activeRemedy || !checkIn.completed || !checkIn.within_window || !checkIn.prohibited_avoided}
          className="w-full bg-gold text-background font-semibold rounded-lg px-4 py-2 mt-1 disabled:opacity-40"
        >
          {logging ? 'Logging…' : 'Log Today\'s Ritual'}
        </button>
      </div>
    </div>
  );
}
