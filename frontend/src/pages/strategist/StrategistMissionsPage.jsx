import { SEO } from '../../components/SEO';
import React, { useEffect, useState } from 'react';
import { ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';
import MissionCard from '../../components/MissionCard';
import StrategistThemeProvider from '../../components/strategist/StrategistThemeProvider';
import { StrategistThemeToggle } from '../../components/strategist/StrategistThemeToggle';
import '../../styles/strategist-tokens.css';

const BACKEND = process.env.REACT_APP_BACKEND_URL || '';
const PLANETS = ['', 'Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Rahu', 'Ketu'];
const BENEFIC_PLANETS = ['Jupiter', 'Venus', 'Mercury', 'Moon'];

function formatDate(dateText) {
  if (!dateText) return 'Unknown';
  const parsed = new Date(dateText);
  if (Number.isNaN(parsed.getTime())) return dateText;
  return parsed.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' });
}

function monthDelta(endDateText) {
  if (!endDateText) return null;
  const end = new Date(endDateText);
  if (Number.isNaN(end.getTime())) return null;
  const now = new Date();
  const months = (end.getFullYear() - now.getFullYear()) * 12 + (end.getMonth() - now.getMonth());
  return Math.max(0, months);
}

function durationPercent(startText, endText) {
  const start = new Date(startText);
  const end = new Date(endText);
  const now = new Date();
  if ([start, end, now].some((value) => Number.isNaN(value.getTime()))) return null;
  const total = end.getTime() - start.getTime();
  if (total <= 0) return null;
  const elapsed = Math.min(Math.max(now.getTime() - start.getTime(), 0), total);
  return Math.round((elapsed / total) * 100);
}

function DashaTimingBar({ dashboard }) {
  const mahadasha = dashboard?.mahadasha || dashboard?.current_mahadasha || '';
  const antardasha = dashboard?.antardasha || dashboard?.current_antardasha || '';
  const mahadashaStart = dashboard?.mahadasha_start || dashboard?.current_mahadasha_start || '';
  const mahadashaEnd = dashboard?.mahadasha_end || dashboard?.current_mahadasha_end || '';
  const antardashaStart = dashboard?.antardasha_start || dashboard?.current_antardasha_start || '';
  const antardashaEnd = dashboard?.antardasha_end || dashboard?.current_antardasha_end || '';
  const activePlanet = antardasha || mahadasha;
  const isBenefic = BENEFIC_PLANETS.includes(activePlanet);
  const barTone = isBenefic ? 'from-gold via-gold/90 to-amber-200' : 'from-amber-500 via-orange-500 to-red-400';
  const labelTone = isBenefic ? 'text-gold' : 'text-amber-300';
  const percent = durationPercent(antardashaStart, antardashaEnd);
  const monthsRemaining = monthDelta(antardashaEnd);

  return (
    <div className="rounded-[28px] border border-gold/20 bg-gold/[0.04] p-5 shadow-sm sm:p-6">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <p className="text-[11px] uppercase tracking-[0.28em] text-gold/70">Dasha Timing</p>
          <h2 className="mt-2 text-2xl font-cinzel text-foreground">Current Strategic Weather</h2>
        </div>
        {activePlanet ? (
          <span className={`rounded-full border px-3 py-1 text-xs font-semibold ${isBenefic ? 'border-gold/30 bg-gold/10 text-gold' : 'border-amber-500/30 bg-amber-500/10 text-amber-300'}`}>
            {isBenefic ? 'Benefic phase' : 'Malefic phase'}
          </span>
        ) : null}
      </div>

      <div className="mt-5 grid gap-4 lg:grid-cols-2">
        <div className="rounded-2xl border border-white/8 bg-white/[0.03] p-4">
          <p className="text-[11px] uppercase tracking-[0.22em] text-muted-foreground">Mahadasha</p>
          <p className="mt-2 text-xl font-semibold text-foreground">{mahadasha || 'Unavailable from current payload'}</p>
          <p className="mt-1 text-sm text-muted-foreground">
            {mahadashaStart || mahadashaEnd ? `${formatDate(mahadashaStart)} - ${formatDate(mahadashaEnd)}` : 'Date range not exposed by current strategist dashboard response'}
          </p>
        </div>

        <div className="rounded-2xl border border-white/8 bg-white/[0.03] p-4">
          <p className="text-[11px] uppercase tracking-[0.22em] text-muted-foreground">Antardasha</p>
          <p className={`mt-2 text-xl font-semibold ${labelTone}`}>{antardasha || 'Unavailable from current payload'}</p>
          <p className="mt-1 text-sm text-muted-foreground">
            {antardashaStart || antardashaEnd ? `${formatDate(antardashaStart)} - ${formatDate(antardashaEnd)}` : 'Timing range not currently supplied to the frontend'}
          </p>
        </div>
      </div>

      <div className="mt-5 rounded-2xl border border-white/8 bg-white/[0.03] p-4">
        <div className="flex flex-wrap items-center justify-between gap-3 text-sm">
          <span className="text-muted-foreground">Antardasha progress</span>
          <span className={labelTone}>
            {monthsRemaining != null ? `${monthsRemaining} month${monthsRemaining === 1 ? '' : 's'} remaining` : 'Remaining duration unavailable'}
          </span>
        </div>
        <div className="mt-3 h-3 overflow-hidden rounded-full bg-white/8">
          <div
            className={`h-full rounded-full bg-gradient-to-r transition-all duration-500 ${barTone}`}
            style={{ width: `${percent ?? 0}%` }}
          />
        </div>
        {percent == null ? (
          <p className="mt-3 text-xs text-muted-foreground">
            The STR-2J brief expects explicit dasha start/end dates, but the live strategist dashboard does not currently document them. This bar will auto-complete once those fields are exposed in the payload.
          </p>
        ) : null}
      </div>
    </div>
  );
}

export default function StrategistMissionsPage() {
  const [missions, setMissions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filterPlanet, setFilterPlanet] = useState('');
  const [dashboard, setDashboard] = useState(null);
  const [dashboardError, setDashboardError] = useState('');

  useEffect(() => {
    let mounted = true;

    Promise.all([
      fetch(`${BACKEND}/api/strategist/missions`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({}),
      }).then((response) => response.json()),
      fetch(`${BACKEND}/api/strategist/dashboard`, {
        credentials: 'include',
      }).then((response) => response.json()),
    ])
      .then(([missionsData, dashboardData]) => {
        if (!mounted) return;
        setMissions(missionsData.missions || []);
        if (dashboardData?.error) {
          setDashboardError(dashboardData.error);
        } else {
          setDashboard(dashboardData);
        }
      })
      .catch((fetchError) => {
        if (!mounted) return;
        setError(fetchError.message || 'Unable to load strategist missions.');
      })
      .finally(() => {
        if (mounted) setLoading(false);
      });

    return () => {
      mounted = false;
    };
  }, []);

  const filtered = filterPlanet
    ? missions.filter((mission) => {
      const fields = [
        mission.trigger_condition,
        mission.mission_name,
        mission.strategy,
        mission.planet_lord,
      ].filter(Boolean).join(' ');
      return fields.toLowerCase().includes(filterPlanet.toLowerCase());
    })
    : missions;

  return (
    <StrategistThemeProvider>
    {/* Floating Strategist theme toggle -- top-right, module-scoped */}
    <div style={{ position: 'fixed', top: 16, right: 20, zIndex: 50 }}>
      <StrategistThemeToggle />
    </div>
    <div className="min-h-screen bg-background px-4 py-8 text-foreground sm:px-6 lg:px-8">
      <SEO title="Mission Board -- The Strategist" noindex={true} />
      <div className="mx-auto max-w-5xl">
        <div className="rounded-[30px] border border-gold/20 bg-gold/[0.04] p-5 shadow-sm sm:p-6">
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div className="max-w-3xl">
              <p className="text-[11px] uppercase tracking-[0.28em] text-gold/70">The Strategist -- Layer 3</p>
              <h1 className="mt-2 text-3xl font-cinzel text-gold sm:text-4xl">Mission Board</h1>
              <p className="mt-3 text-sm leading-7 text-muted-foreground">
                Transit-triggered missions, pivot logic, and command-planet alignment in one responsive strategist grid.
              </p>
            </div>
            <Link
              to="/strategist"
              className="inline-flex items-center gap-2 rounded-full border border-gold/25 bg-gold/[0.08] px-4 py-2 text-sm font-semibold text-gold transition hover:bg-gold/[0.14]"
            >
              Back to War Room <ArrowRight className="h-4 w-4" />
            </Link>
          </div>

          <div className="mt-5 flex flex-wrap items-center gap-3">
            <label htmlFor="planet-filter" className="text-xs uppercase tracking-[0.22em] text-muted-foreground">
              Filter by planet
            </label>
            <select
              id="planet-filter"
              value={filterPlanet}
              onChange={(event) => setFilterPlanet(event.target.value)}
              className="rounded-full border border-gold/20 bg-background px-3 py-2 text-sm text-foreground outline-none transition focus:border-gold/50"
            >
              {PLANETS.map((planet) => <option key={planet} value={planet}>{planet || 'All planets'}</option>)}
            </select>
          </div>
        </div>

        <div className="mt-6">
          <DashaTimingBar dashboard={dashboard} />
        </div>

        {loading ? <p className="mt-6 text-sm text-muted-foreground">Loading missions...</p> : null}
        {error ? <p className="mt-6 rounded-2xl border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-300">{error}</p> : null}
        {dashboardError ? <p className="mt-6 rounded-2xl border border-amber-500/30 bg-amber-500/10 px-4 py-3 text-sm text-amber-200">{dashboardError}</p> : null}

        {!loading && filtered.length === 0 ? (
          <div className="mt-6 rounded-[28px] border border-gold/20 bg-gold/[0.04] p-6 text-center">
            <p className="text-sm text-muted-foreground">No active missions match current transits.</p>
            <p className="mt-1 text-xs text-muted-foreground">Complete onboarding and run diagnosis to trigger missions.</p>
          </div>
        ) : null}

        <div className="mt-6 grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
          {filtered.map((mission, index) => (
            <MissionCard
              key={mission.id || index}
              mission={mission}
              commandPlanet={dashboard?.command_planet || ''}
            />
          ))}
        </div>

        {!loading && missions.length > 0 ? (
          <p className="mt-5 text-center text-xs text-muted-foreground">{filtered.length} active missions</p>
        ) : null}
      </div>
    </div>
    </StrategistThemeProvider>
  );
}
