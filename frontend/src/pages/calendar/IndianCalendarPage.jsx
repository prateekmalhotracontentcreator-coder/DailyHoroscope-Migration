import React, { useEffect, useMemo, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';
import { CalendarDays, ChevronLeft, ChevronRight } from 'lucide-react';
import { SEO } from '../../components/SEO';
import { Footer } from '../../components/Footer';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api/panchang`;
const SITE = 'https://www.everydayhoroscope.in';
const LOCATION_KEY = 'panchang_location_slug';
const FALLBACK_LOCATION_KEY = 'selectedCity';
const DEFAULT_SLUG = 'new-delhi-india';
const MONTH_NAMES = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December',
];
const WEEKDAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

const badgeClass = {
  festival: 'bg-orange-500/15 text-orange-400 border-orange-400/30',
  vrat: 'bg-purple-500/15 text-purple-400 border-purple-400/30',
  observance: 'bg-sky-500/15 text-sky-400 border-sky-400/30',
};

function getStoredLocationSlug() {
  return localStorage.getItem(LOCATION_KEY) || localStorage.getItem(FALLBACK_LOCATION_KEY) || DEFAULT_SLUG;
}

function buildMonthSchema(monthLabel, days) {
  const events = days.flatMap((day) =>
    (day.observances || []).slice(0, 3).map((item) => ({
      '@type': 'Event',
      name: item.name,
      startDate: day.date,
      eventAttendanceMode: 'https://schema.org/OnlineEventAttendanceMode',
      eventStatus: 'https://schema.org/EventScheduled',
      url: `${SITE}/panchang/date/${day.date}`,
    }))
  );

  return events.length ? {
    '@context': 'https://schema.org',
    '@graph': events,
  } : {
    '@context': 'https://schema.org',
    '@type': 'WebPage',
    name: `Indian Calendar ${monthLabel}`,
    url: `${SITE}/calendar`,
  };
}

function buildGrid(days, year, month) {
  const firstDay = new Date(year, month - 1, 1).getDay();
  const leading = Array.from({ length: firstDay }, (_, index) => ({ empty: true, key: `empty-${index}` }));
  return [...leading, ...days];
}

export function IndianCalendarPage() {
  const navigate = useNavigate();
  const params = useParams();
  const now = new Date();
  const initialYear = Number(params.year || now.getFullYear());
  const initialMonth = Number(params.month || now.getMonth() + 1);
  const [calendarData, setCalendarData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let ignore = false;

    async function fetchCalendar() {
      try {
        setLoading(true);
        setError('');
        const response = await axios.get(`${API}/calendar/${initialYear}/${initialMonth}`, {
          params: {
            location_slug: getStoredLocationSlug(),
          },
        });
        if (!ignore) setCalendarData(response.data);
      } catch {
        if (!ignore) setError('Unable to load the Indian calendar right now.');
      } finally {
        if (!ignore) setLoading(false);
      }
    }

    fetchCalendar();
    return () => {
      ignore = true;
    };
  }, [initialYear, initialMonth]);

  const monthLabel = `${MONTH_NAMES[initialMonth - 1]} ${initialYear}`;
  const calendarGrid = useMemo(
    () => buildGrid(calendarData?.days || [], initialYear, initialMonth),
    [calendarData, initialYear, initialMonth]
  );

  function shiftMonth(offset) {
    const next = new Date(initialYear, initialMonth - 1 + offset, 1);
    navigate(`/calendar/${next.getFullYear()}/${next.getMonth() + 1}`);
  }

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <SEO
        title={`Indian Calendar ${monthLabel} -- Tithi, Festivals & Panchang`}
        description={`Indian calendar for ${monthLabel} with daily Tithi, Hindu festivals, Ekadashi, Purnima and auspicious dates. Powered by Vedic Panchang.`}
        url={`${SITE}/calendar/${initialYear}/${initialMonth}`}
        schema={buildMonthSchema(monthLabel, calendarData?.days || [])}
      />

      <main className="flex-1 max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="rounded-3xl border border-gold/20 bg-gradient-to-br from-gold/[0.08] via-background to-background p-8 shadow-sm">
          <div className="flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
            <div className="space-y-3">
              <div className="inline-flex items-center gap-2 rounded-full border border-gold/20 bg-gold/[0.06] px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-gold">
                <CalendarDays className="h-3.5 w-3.5" />
                Indian Calendar
              </div>
              <div>
                <h1 className="text-3xl font-playfair font-bold text-foreground sm:text-4xl">
                  Indian Calendar -- {monthLabel}
                </h1>
                <p className="mt-3 max-w-2xl text-sm leading-6 text-muted-foreground">
                  Daily Tithi, monthly festival markers, and fast links into the full Panchang for each date.
                </p>
              </div>
            </div>

            <div className="flex items-center gap-3 self-start rounded-full border border-gold/20 bg-gold/[0.04] p-2">
              <button
                onClick={() => shiftMonth(-1)}
                className="rounded-full p-2 text-gold transition hover:bg-gold/10"
                aria-label="Previous month"
              >
                <ChevronLeft className="h-4 w-4" />
              </button>
              <span className="min-w-32 text-center text-sm font-semibold text-foreground">{monthLabel}</span>
              <button
                onClick={() => shiftMonth(1)}
                className="rounded-full p-2 text-gold transition hover:bg-gold/10"
                aria-label="Next month"
              >
                <ChevronRight className="h-4 w-4" />
              </button>
            </div>
          </div>
        </div>

        {loading && <p className="py-12 text-center text-muted-foreground">Loading calendar...</p>}
        {error && <p className="py-12 text-center text-muted-foreground">{error}</p>}

        {!loading && !error && (
          <>
            <div className="mt-8 overflow-hidden rounded-2xl border border-gold/20 bg-gold/[0.04] shadow-sm">
              <div className="grid grid-cols-7 border-b border-gold/10 bg-gold/[0.06]">
                {WEEKDAYS.map((weekday) => (
                  <div key={weekday} className="px-2 py-3 text-center text-xs font-semibold uppercase tracking-[0.2em] text-muted-foreground">
                    {weekday}
                  </div>
                ))}
              </div>
              <div className="grid grid-cols-7">
                {calendarGrid.map((day, index) => (
                  <div
                    key={day.key || day.date || index}
                    className={`min-h-32 border-b border-r border-gold/10 p-3 ${day.empty ? 'bg-transparent' : 'bg-background/70'}`}
                  >
                    {!day.empty && (
                      <>
                        <div className="flex items-start justify-between gap-2">
                          <Link to={`/panchang/date/${day.date}`} className="text-lg font-semibold text-foreground transition hover:text-gold">
                            {day.day}
                          </Link>
                          {day.observances?.[0] && (
                            <span className={`rounded-full border px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wide ${badgeClass[day.observances[0].observance_type] || badgeClass.observance}`}>
                              {day.observances[0].observance_type}
                            </span>
                          )}
                        </div>
                        <p className="mt-2 text-xs leading-5 text-muted-foreground">{day.tithi}</p>
                        {day.observances?.length > 0 && (
                          <div className="mt-3 space-y-1">
                            {day.observances.slice(0, 2).map((item) => (
                              <Link key={`${item.slug}-${item.date}`} to={`/festivals/${item.slug}`} className="block text-xs font-medium leading-5 text-gold transition hover:underline">
                                {item.name}
                              </Link>
                            ))}
                          </div>
                        )}
                      </>
                    )}
                  </div>
                ))}
              </div>
            </div>

            <div className="mt-8 grid gap-6 lg:grid-cols-[2fr_1fr]">
              <section className="rounded-xl border border-gold/20 bg-gold/[0.04] p-5 shadow-sm">
                <h2 className="text-xl font-semibold text-foreground">Festivals this month</h2>
                <div className="mt-4 space-y-3">
                  {calendarData?.days?.flatMap((day) =>
                    (day.observances || []).map((item) => (
                      <div key={`${day.date}-${item.slug}`} className="rounded-xl border border-border/70 bg-background/80 p-4">
                        <div className="flex flex-wrap items-start justify-between gap-3">
                          <div>
                            <Link to={`/festivals/${item.slug}`} className="text-base font-semibold text-foreground transition hover:text-gold">
                              {item.name}
                            </Link>
                            <p className="mt-1 text-xs text-muted-foreground">{day.date}</p>
                          </div>
                          <span className={`rounded-full border px-2.5 py-1 text-[11px] font-semibold uppercase tracking-wide ${badgeClass[item.observance_type] || badgeClass.observance}`}>
                            {item.observance_type}
                          </span>
                        </div>
                        <p className="mt-3 text-sm leading-6 text-muted-foreground">{item.summary}</p>
                        <Link to={`/panchang/date/${day.date}`} className="mt-3 inline-block text-sm text-gold transition hover:underline">
                          See full Panchang for {item.name}
                        </Link>
                      </div>
                    ))
                  )}
                  {calendarData?.days?.every((day) => !day.observances?.length) && (
                    <p className="text-sm text-muted-foreground">No listed festivals for this month.</p>
                  )}
                </div>
              </section>

              <aside className="rounded-xl border border-gold/20 bg-gold/[0.05] p-5 shadow-sm">
                <h2 className="text-lg font-semibold text-foreground">Your Personalised Auspicious Calendar</h2>
                <p className="mt-3 text-sm leading-6 text-muted-foreground">
                  Pair the public Panchang with your own birth chart for personalised date selection, timing windows, and premium planning.
                </p>
                <div className="mt-5 flex flex-col gap-3">
                  <Link to="/panchang" className="inline-flex items-center justify-center rounded-full border border-gold px-4 py-2 text-sm font-semibold text-gold transition hover:bg-gold/10">
                    View full Panchang for today
                  </Link>
                  <Link to="/pricing" className="inline-flex items-center justify-center rounded-full bg-gold px-4 py-2 text-sm font-semibold text-background transition hover:opacity-90">
                    Premium auspicious calendar
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
