import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import StrategistThemeProvider from '../../components/strategist/StrategistThemeProvider';
import ControlRoomBackdrop from '../../components/strategist/ControlRoomBackdrop';
import StrategistWarRoom from '../../components/strategist/war-room/StrategistWarRoom';
import { StrategistThemeToggle } from '../../components/strategist/StrategistThemeToggle';

const BACKEND = process.env.REACT_APP_BACKEND_URL || '';
const SUNSET_BUFFER_MS = 30 * 60 * 1000;

function formatDisplayDate(dateValue) {
  return dateValue.toLocaleDateString('en-IN', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  });
}

function formatTransitionDate(isoString) {
  if (!isoString) return undefined;
  const d = new Date(isoString);
  if (Number.isNaN(d.getTime())) return undefined;
  return d.toLocaleDateString('en-IN', { month: 'long', year: 'numeric' });
}

function getLayout() {
  if (typeof window === 'undefined') return 'grid';
  return window.innerWidth < 768 ? 'snap' : 'grid';
}

function shapeDasha(data) {
  if (!data?.current_mahadasha) return undefined;

  const today = new Date();

  function parseDateToElapsed(startStr) {
    if (!startStr) return 0;
    const start = new Date(startStr);
    if (Number.isNaN(start.getTime())) return 0;
    return Math.max(0, Math.floor((today - start) / 86400000));
  }

  function parseDateToTotal(startStr, endStr) {
    if (!startStr || !endStr) return 1;
    const start = new Date(startStr);
    const end = new Date(endStr);
    if (Number.isNaN(start.getTime()) || Number.isNaN(end.getTime())) return 1;
    return Math.max(1, Math.floor((end - start) / 86400000));
  }

  function fmtDate(str) {
    if (!str) return '';
    const parsed = new Date(str);
    if (Number.isNaN(parsed.getTime())) return '';
    return parsed.toLocaleDateString('en-IN', { month: 'short', year: 'numeric' });
  }

  return {
    mahadasha: {
      planet: data.current_mahadasha,
      elapsedDays: parseDateToElapsed(data.current_mahadasha_start),
      totalDays: parseDateToTotal(data.current_mahadasha_start, data.current_mahadasha_end),
      startedLabel: fmtDate(data.current_mahadasha_start),
      endsLabel: fmtDate(data.current_mahadasha_end),
    },
    antardasha: data.current_antardasha
      ? {
          planet: data.current_antardasha,
          elapsedDays: parseDateToElapsed(data.current_antardasha_start),
          totalDays: parseDateToTotal(data.current_antardasha_start, data.current_antardasha_end),
          startedLabel: fmtDate(data.current_antardasha_start),
          endsLabel: fmtDate(data.current_antardasha_end),
        }
      : undefined,
  };
}

function computeGoldenHourWindows(sunsetIso) {
  if (!sunsetIso) return [];

  const sunsetDate = new Date(sunsetIso);
  const sunset = sunsetDate.getTime();
  if (Number.isNaN(sunset)) return [];

  const now = Date.now();
  const dayStart = new Date(sunsetDate);
  dayStart.setHours(0, 0, 0, 0);
  const dayEnd = new Date(dayStart.getTime() + 24 * 60 * 60 * 1000);
  const goldenStart = new Date(sunset - SUNSET_BUFFER_MS);
  const goldenEnd = new Date(sunset);
  const offensiveEnd = new Date(sunset - SUNSET_BUFFER_MS);
  const defensiveStart = new Date(sunset);

  return [
    {
      id: 'offensive',
      label: 'Offensive Window',
      name: 'Offensive Window',
      state: 'OFFENSIVE_GOLD',
      start: dayStart.toISOString(),
      end: offensiveEnd.toISOString(),
      startIso: dayStart.toISOString(),
      endIso: offensiveEnd.toISOString(),
      active: now < sunset - SUNSET_BUFFER_MS,
      countdownSeconds: null,
      type: 'auspicious',
      planet: 'sun',
    },
    {
      id: 'golden',
      label: 'Golden Hour',
      name: 'Golden Hour',
      state: 'GOLDEN_HOUR',
      start: goldenStart.toISOString(),
      end: goldenEnd.toISOString(),
      startIso: goldenStart.toISOString(),
      endIso: goldenEnd.toISOString(),
      active: now >= sunset - SUNSET_BUFFER_MS && now <= sunset,
      countdownSeconds:
        now >= sunset - SUNSET_BUFFER_MS && now <= sunset
          ? Math.max(0, Math.floor((sunset - now) / 1000))
          : null,
      type: 'auspicious',
      planet: 'sun',
    },
    {
      id: 'defensive',
      label: 'Defensive Window',
      name: 'Defensive Window',
      state: 'DEFENSIVE_MIDNIGHT',
      start: defensiveStart.toISOString(),
      end: dayEnd.toISOString(),
      startIso: defensiveStart.toISOString(),
      endIso: null,
      active: now > sunset,
      countdownSeconds: null,
      type: 'defensive',
      planet: 'sun',
    },
  ];
}

function mapWarRoomProps(dashboard, missions, layout) {
  const conquest = dashboard?.conquest_probability || {};
  const scoreboard = dashboard?.scoreboard || {};
  const pitruActive = Boolean(dashboard?.diagnosis_summary?.pitru_rin_active);
  const pitruRin = Array.isArray(dashboard?.pitru_rin_ledger) ? dashboard.pitru_rin_ledger : [];

  return {
    conquestScore: {
      score: Number(conquest.score) || 0,
      stampLabel: scoreboard.score_tier,
    },
    factors: Array.isArray(conquest.factors) ? conquest.factors : [],
    missions: Array.isArray(missions) ? missions : [],
    dasha: shapeDasha(dashboard),
    transition: formatTransitionDate(dashboard?.current_mahadasha_end),
    pitruRin,
    pitruDelta: pitruActive ? -20 : 0,
    pitruEmptyMeta: pitruActive ? undefined : { message: 'No active ancestral debt detected. Karma is balanced.' },
    goldenHour: computeGoldenHourWindows(dashboard?.sunset_iso),
    kpVerdict: scoreboard.gate0_last_verdict ?? '',
    locationLabel: dashboard?.success_direction
      ? `Power direction: ${dashboard.success_direction}`
      : undefined,
    dateLabel: formatDisplayDate(new Date()),
    layout,
    onRecalibrate: () => window.location.reload(),
  };
}

function LoadingState() {
  return (
    <StrategistThemeProvider>
      <ControlRoomBackdrop>
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            height: '60vh',
          }}
        >
          <p
            style={{
              color: 'var(--str-gold)',
              fontFamily: 'var(--str-font-display)',
              fontSize: '1.1rem',
              letterSpacing: '0.08em',
            }}
          >
            Calibrating War Room...
          </p>
        </div>
      </ControlRoomBackdrop>
    </StrategistThemeProvider>
  );
}

function LockedState() {
  return (
    <StrategistThemeProvider>
      <ControlRoomBackdrop>
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            height: '60vh',
            gap: '1.5rem',
          }}
        >
          <p
            style={{
              color: 'var(--str-gold)',
              fontFamily: 'var(--str-font-display)',
              fontSize: '1.1rem',
            }}
          >
            War Room Locked
          </p>
          <p
            style={{
              color: 'var(--str-muted)',
              fontSize: '0.9rem',
              textAlign: 'center',
              maxWidth: 340,
            }}
          >
            Complete your Strategist onboarding to activate the live engine.
          </p>
          <a
            href="/strategist"
            style={{
              color: 'var(--str-gold)',
              textDecoration: 'underline',
              fontSize: '0.9rem',
            }}
          >
            Return to Strategist
          </a>
        </div>
      </ControlRoomBackdrop>
    </StrategistThemeProvider>
  );
}

function ErrorState({ message }) {
  return (
    <StrategistThemeProvider>
      <ControlRoomBackdrop>
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            height: '60vh',
            gap: '1rem',
            padding: '0 1.5rem',
          }}
        >
          <p
            style={{
              color: 'var(--str-gold)',
              fontFamily: 'var(--str-font-display)',
              fontSize: '1.1rem',
            }}
          >
            War Room Unavailable
          </p>
          <p
            style={{
              color: 'var(--str-muted)',
              fontSize: '0.9rem',
              textAlign: 'center',
              maxWidth: 420,
            }}
          >
            {message}
          </p>
        </div>
      </ControlRoomBackdrop>
    </StrategistThemeProvider>
  );
}

export default function StrategistWarRoomPage() {
  const navigate = useNavigate();
  const [layout, setLayout] = useState(getLayout);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [locked, setLocked] = useState(false);
  const [dashboard, setDashboard] = useState(null);
  const [missions, setMissions] = useState([]);

  // Derived synchronously in render -- avoids a 1-frame "Unavailable" flash
  // that would occur if warRoomProps were a separate useState + useEffect.
  const warRoomProps = dashboard ? mapWarRoomProps(dashboard, missions, layout) : null;

  useEffect(() => {
    function handleResize() {
      setLayout(getLayout());
    }

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  useEffect(() => {
    let active = true;

    async function loadWarRoom() {
      setLoading(true);
      setError('');
      setLocked(false);

      try {
        const [dashRes, missRes] = await Promise.all([
          fetch(`${BACKEND}/api/strategist/dashboard`, {
            credentials: 'include',
          }),
          fetch(`${BACKEND}/api/strategist/missions`, {
            method: 'POST',
            credentials: 'include',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              user_id: null,
              date: new Date().toISOString().split('T')[0],
            }),
          }),
        ]);

        const [dashboardData, missionsData] = await Promise.all([
          dashRes.json().catch(() => ({})),
          missRes.json().catch(() => ({})),
        ]);

        if (!active) return;

        if (dashboardData?.error?.includes('LK profile missing')) {
          setLocked(true);
          return;
        }

        if (!dashRes.ok) {
          throw new Error(dashboardData?.error || 'Unable to load strategist dashboard.');
        }

        if (!missRes.ok) {
          throw new Error(missionsData?.error || 'Unable to load strategist missions.');
        }

        setDashboard(dashboardData);
        setMissions(missionsData?.missions || []);
      } catch (fetchError) {
        if (!active) return;
        setError(fetchError.message || 'Unable to load the War Room right now.');
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    }

    loadWarRoom();
    return () => {
      active = false;
    };
  }, []);

  if (loading) return <LoadingState />;
  if (locked) return <LockedState />;
  if (error) return <ErrorState message={error} />;
  if (!warRoomProps) return <ErrorState message="Unable to map strategist engine output." />;

  return (
    <StrategistThemeProvider>
      {/* Module nav strip -- sticky just below the app NavBar (h-14 = 56px), within module boundaries */}
      <div style={{
        position: 'sticky',
        top: 56,
        zIndex: 29,
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '10px 20px',
        background: 'rgba(7, 17, 30, 0.92)',
        backdropFilter: 'blur(12px)',
        WebkitBackdropFilter: 'blur(12px)',
        borderBottom: '1px solid rgba(197, 160, 89, 0.12)',
      }}>
        {/* Back to landing */}
        <a
          href="/strategist"
          style={{
            color: 'var(--strategist-gold)',
            fontFamily: 'Cinzel, serif',
            fontSize: '0.72rem',
            letterSpacing: '0.16em',
            textTransform: 'uppercase',
            textDecoration: 'none',
            opacity: 0.75,
            display: 'flex',
            alignItems: 'center',
            gap: 6,
            transition: 'opacity 0.2s',
          }}
          onMouseEnter={e => e.currentTarget.style.opacity = 1}
          onMouseLeave={e => e.currentTarget.style.opacity = 0.75}
        >
          ← The Strategist
        </a>

        {/* Breadcrumb label */}
        <span style={{
          color: 'rgba(197,160,89,0.55)',
          fontFamily: 'Cinzel, serif',
          fontSize: '0.68rem',
          letterSpacing: '0.20em',
          textTransform: 'uppercase',
        }}>
          War Room · Overview
        </span>

        {/* Right side: manual link + enter war room CTA + theme toggle */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <a
            href="/strategist/manual"
            style={{
              color: 'rgba(197,160,89,0.60)',
              fontFamily: 'Cinzel, serif',
              fontSize: '0.68rem',
              letterSpacing: '0.16em',
              textTransform: 'uppercase',
              textDecoration: 'none',
              transition: 'color 0.2s',
            }}
            onMouseEnter={e => e.currentTarget.style.color = 'rgba(197,160,89,1)'}
            onMouseLeave={e => e.currentTarget.style.color = 'rgba(197,160,89,0.60)'}
          >
            Field Manual
          </a>
          <button
            type="button"
            onClick={() => navigate('/strategist/war-room')}
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: 6,
              padding: '6px 16px',
              borderRadius: 9999,
              border: '1px solid rgba(197,160,89,0.35)',
              background: 'rgba(197,160,89,0.10)',
              color: 'var(--strategist-gold)',
              fontFamily: 'Cinzel, serif',
              fontSize: '0.72rem',
              letterSpacing: '0.16em',
              textTransform: 'uppercase',
              cursor: 'pointer',
              transition: 'background 0.2s, opacity 0.2s',
              opacity: 0.85,
            }}
            onMouseEnter={e => { e.currentTarget.style.opacity = 1; e.currentTarget.style.background = 'rgba(197,160,89,0.18)'; }}
            onMouseLeave={e => { e.currentTarget.style.opacity = 0.85; e.currentTarget.style.background = 'rgba(197,160,89,0.10)'; }}
          >
            Enter Full War Room →
          </button>
          <StrategistThemeToggle />
        </div>
      </div>

      <StrategistWarRoom {...warRoomProps} />
    </StrategistThemeProvider>
  );
}
