import React, { useEffect, useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { Clock3, MapPin } from 'lucide-react';
import { SEO } from '../../components/SEO';
import { Footer } from '../../components/Footer';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api/panchang`;
const SITE = 'https://www.everydayhoroscope.in';
const LOCATION_KEY = 'panchang_location_slug';
const FALLBACK_LOCATION_KEY = 'selectedCity';
const DEFAULT_SLUG = 'new-delhi-india';

const planetClass = {
  Sun: 'bg-amber-500/15 text-amber-300 border-amber-400/30',
  Moon: 'bg-slate-500/15 text-slate-300 border-slate-400/30',
  Mars: 'bg-red-500/15 text-red-300 border-red-400/30',
  Mercury: 'bg-emerald-500/15 text-emerald-300 border-emerald-400/30',
  Jupiter: 'bg-yellow-500/15 text-yellow-300 border-yellow-400/30',
  Venus: 'bg-pink-500/15 text-pink-300 border-pink-400/30',
  Saturn: 'bg-indigo-500/15 text-indigo-300 border-indigo-400/30',
};

function getStoredLocationSlug() {
  return localStorage.getItem(LOCATION_KEY) || localStorage.getItem(FALLBACK_LOCATION_KEY) || DEFAULT_SLUG;
}

function formatDateLabel(isoDate, timezone) {
  return new Date(`${isoDate}T12:00:00`).toLocaleDateString('en-IN', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    timeZone: timezone,
  });
}

function formatTimeRange(value, timezone) {
  return new Date(value).toLocaleTimeString('en-IN', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: true,
    timeZone: timezone,
  });
}

function buildHoraSchema(dateValue) {
  return {
    '@context': 'https://schema.org',
    '@type': 'WebPage',
    name: 'Hora Today -- Planetary Hours Schedule',
    description: `Today's Hora schedule with all 24 planetary hours for ${dateValue}.`,
    url: `${SITE}/hora`,
    datePublished: dateValue,
  };
}

function HoraLocationPicker({ locations, selectedSlug, onChange }) {
  return (
    <label className="flex flex-col gap-2 text-sm text-muted-foreground">
      <span className="font-medium text-foreground">Location</span>
      <div className="flex items-center gap-2 rounded-xl border border-gold/20 bg-gold/[0.04] px-3 py-2">
        <MapPin className="h-4 w-4 text-gold" />
        <select
          value={selectedSlug}
          onChange={(event) => onChange(event.target.value)}
          className="w-full bg-transparent text-sm text-foreground outline-none"
        >
          {locations.map((location) => (
            <option key={location.slug} value={location.slug}>
              {location.label}
            </option>
          ))}
        </select>
      </div>
    </label>
  );
}

function HoraTable({ title, items, activeId, timezone }) {
  return (
    <section className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm">
      <div className="border-b border-gold/10 px-5 py-4">
        <h2 className="text-lg font-semibold text-foreground">{title}</h2>
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead>
            <tr className="border-b border-gold/10 text-left text-xs uppercase tracking-[0.2em] text-muted-foreground">
              <th className="px-5 py-3">Planet</th>
              <th className="px-5 py-3">Start</th>
              <th className="px-5 py-3">End</th>
              <th className="px-5 py-3">Quality</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => {
              const active = activeId === item.index;
              return (
                <tr key={item.index} className={`border-b border-gold/5 ${active ? 'bg-gold/[0.08]' : ''}`}>
                  <td className="px-5 py-4">
                    <div className="flex items-center gap-3">
                      {active && <span className="h-2.5 w-2.5 animate-pulse rounded-full bg-gold" />}
                      <span className={`rounded-full border px-2.5 py-1 text-xs font-semibold ${planetClass[item.planet] || ''}`}>
                        {item.planet}
                      </span>
                    </div>
                  </td>
                  <td className="px-5 py-4 text-muted-foreground">{formatTimeRange(item.start, timezone)}</td>
                  <td className="px-5 py-4 text-muted-foreground">{formatTimeRange(item.end, timezone)}</td>
                  <td className="px-5 py-4 text-foreground">{item.quality}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </section>
  );
}

export function HoraTodayPage() {
  const [locations, setLocations] = useState([]);
  const [locationSlug, setLocationSlug] = useState(getStoredLocationSlug());
  const [horaData, setHoraData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let ignore = false;

    async function fetchLocations() {
      try {
        const response = await axios.get(`${API}/locations`);
        if (!ignore) setLocations(response.data);
      } catch {
        if (!ignore) setLocations([]);
      }
    }

    fetchLocations();
    return () => {
      ignore = true;
    };
  }, []);

  useEffect(() => {
    localStorage.setItem(LOCATION_KEY, locationSlug);
  }, [locationSlug]);

  useEffect(() => {
    let ignore = false;

    async function fetchHora() {
      try {
        setLoading(true);
        setError('');
        const response = await axios.get(`${API}/hora`, {
          params: {
            location_slug: locationSlug,
          },
        });
        if (!ignore) setHoraData(response.data);
      } catch {
        if (!ignore) setError('Unable to load Hora timings right now.');
      } finally {
        if (!ignore) setLoading(false);
      }
    }

    fetchHora();
    return () => {
      ignore = true;
    };
  }, [locationSlug]);

  const activeHora = useMemo(() => {
    if (!horaData) return null;
    const now = new Date();
    return [...horaData.day_hora, ...horaData.night_hora].find(
      (item) => now >= new Date(item.start) && now < new Date(item.end)
    ) || null;
  }, [horaData]);

  const timezone = horaData?.location?.timezone || 'Asia/Kolkata';
  const dateLabel = horaData ? formatDateLabel(horaData.date, timezone) : '';

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <SEO
        title="Hora Today -- Planetary Hours Schedule"
        description="Today's Hora schedule with all 24 planetary hours. Find the most auspicious time for your activities using Vedic Hora timing."
        url={`${SITE}/hora`}
        schema={buildHoraSchema(horaData?.date || new Date().toISOString().slice(0, 10))}
      />

      <main className="flex-1 max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="rounded-3xl border border-gold/20 bg-gradient-to-br from-gold/[0.08] via-background to-background p-8 shadow-sm">
          <div className="flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
            <div className="space-y-3">
              <div className="inline-flex items-center gap-2 rounded-full border border-gold/20 bg-gold/[0.06] px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-gold">
                <Clock3 className="h-3.5 w-3.5" />
                Hora Today
              </div>
              <div>
                <h1 className="text-3xl font-playfair font-bold text-foreground sm:text-4xl">
                  Hora Today -- Planetary Hours
                </h1>
                <p className="mt-3 max-w-2xl text-sm leading-6 text-muted-foreground">
                  Track the 24 Hora periods for today and spot the active planetary hour for timing decisions, rituals, communication, travel, or business.
                </p>
              </div>
            </div>
            <div className="w-full max-w-sm">
              <HoraLocationPicker locations={locations} selectedSlug={locationSlug} onChange={setLocationSlug} />
            </div>
          </div>
        </div>

        {loading && <p className="py-12 text-center text-muted-foreground">Loading Hora schedule...</p>}
        {error && <p className="py-12 text-center text-muted-foreground">{error}</p>}

        {!loading && !error && horaData && (
          <>
            <div className="mt-8 rounded-2xl border border-gold/20 bg-gold/[0.05] p-6 shadow-sm">
              <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
                <div>
                  <p className="text-xs font-semibold uppercase tracking-[0.2em] text-gold">{dateLabel}</p>
                  <h2 className="mt-2 text-2xl font-semibold text-foreground">
                    {activeHora ? `Now: ${activeHora.planet} Hora` : 'Hora schedule loaded'}
                  </h2>
                  <p className="mt-2 text-sm text-muted-foreground">
                    {activeHora
                      ? `${activeHora.quality} -- ends ${formatTimeRange(activeHora.end, timezone)}`
                      : 'Browse all day and night planetary hours below.'}
                  </p>
                </div>
                <div className="rounded-xl border border-gold/20 bg-background/70 px-4 py-3 text-sm text-muted-foreground">
                  Sunrise {formatTimeRange(horaData.sunrise, timezone)} · Sunset {formatTimeRange(horaData.sunset, timezone)}
                </div>
              </div>
            </div>

            <div className="mt-8 grid gap-6">
              <HoraTable title="Day Horas" items={horaData.day_hora} activeId={activeHora?.index} timezone={timezone} />
              <div className="text-center text-xs font-semibold uppercase tracking-[0.25em] text-muted-foreground">
                Sunset -- Night begins
              </div>
              <HoraTable title="Night Horas" items={horaData.night_hora} activeId={activeHora?.index} timezone={timezone} />
            </div>

            <div className="mt-8 grid gap-6 lg:grid-cols-[1.5fr_1fr]">
              <section className="rounded-xl border border-gold/20 bg-gold/[0.04] p-5 shadow-sm">
                <h2 className="text-lg font-semibold text-foreground">What is Hora?</h2>
                <p className="mt-3 text-sm leading-6 text-muted-foreground">
                  Hora divides the day and night into 24 planetary hours. Each period is ruled by a planet and is traditionally used in Vedic astrology to assess favourable timing for communication, travel, authority work, creativity, discipline, and spiritual activity.
                </p>
                <p className="mt-3 text-sm leading-6 text-muted-foreground">
                  Use Hora as a timing layer alongside the Panchang and your birth chart when planning launches, meetings, travel, investments, worship, or rituals.
                </p>
              </section>

              <aside className="rounded-xl border border-gold/20 bg-gold/[0.05] p-5 shadow-sm">
                <h2 className="text-lg font-semibold text-foreground">Go deeper</h2>
                <p className="mt-3 text-sm leading-6 text-muted-foreground">
                  Find the best Hora for your business launch, travel, worship, or investment decisions with your personal chart context.
                </p>
                <div className="mt-5 flex flex-col gap-3">
                  <Link to="/panchang" className="inline-flex items-center justify-center rounded-full border border-gold px-4 py-2 text-sm font-semibold text-gold transition hover:bg-gold/10">
                    View today's full Panchang
                  </Link>
                  <Link to="/birth-chart" className="inline-flex items-center justify-center rounded-full bg-gold px-4 py-2 text-sm font-semibold text-background transition hover:opacity-90">
                    Personalised timing from your birth chart
                  </Link>
                </div>
              </aside>
            </div>
          </>
        )}
      </main>
      <Footer />
    </div>
  );
}
