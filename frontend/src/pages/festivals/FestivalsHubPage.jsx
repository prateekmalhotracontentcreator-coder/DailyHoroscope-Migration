import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { CalendarDays, ChevronLeft, ChevronRight, Sparkles } from 'lucide-react';
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

const badgeClass = {
  festival: 'bg-orange-500/15 text-orange-400 border-orange-400/30',
  vrat: 'bg-purple-500/15 text-purple-400 border-purple-400/30',
  observance: 'bg-sky-500/15 text-sky-400 border-sky-400/30',
};

function getStoredLocationSlug() {
  return localStorage.getItem(LOCATION_KEY) || localStorage.getItem(FALLBACK_LOCATION_KEY) || DEFAULT_SLUG;
}

function formatDisplayDate(isoDate) {
  const date = new Date(`${isoDate}T12:00:00`);
  return date.toLocaleDateString('en-IN', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
    weekday: 'short',
  });
}

function buildFestivalSchema(year, items) {
  return {
    '@context': 'https://schema.org',
    '@type': 'ItemList',
    name: `Hindu Festival Calendar ${year}`,
    description: `Complete Hindu festival calendar for ${year}. Dates for major festivals, vrats, and observances with Panchang context.`,
    url: `${SITE}/festivals`,
    itemListElement: items.slice(0, 50).map((item, index) => ({
      '@type': 'ListItem',
      position: index + 1,
      name: item.name,
      url: `${SITE}/festivals/${item.slug}`,
    })),
  };
}

export function FestivalsHubPage() {
  const [year, setYear] = useState(new Date().getFullYear());
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let ignore = false;

    async function fetchFestivals() {
      try {
        setLoading(true);
        setError('');
        const response = await axios.get(`${API}/festivals`, {
          params: {
            year,
            location_slug: getStoredLocationSlug(),
          },
        });
        if (!ignore) setData(response.data);
      } catch {
        if (!ignore) setError('Unable to load the festival calendar right now.');
      } finally {
        if (!ignore) setLoading(false);
      }
    }

    fetchFestivals();
    return () => {
      ignore = true;
    };
  }, [year]);

  const grouped = MONTH_NAMES.map((monthName, index) => ({
    monthName,
    items: (data?.items || []).filter((item) => {
      const itemDate = new Date(`${item.date}T12:00:00`);
      return itemDate.getMonth() === index;
    }),
  }));

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <SEO
        title={`Hindu Festival Calendar ${year} -- Dates, Panchang & Muhurat`}
        description={`Complete Hindu festival calendar for ${year}. Dates for Holi, Diwali, Navratri, Ekadashi, Purnima and all major Indian festivals with Panchang details.`}
        url={`${SITE}/festivals`}
        schema={buildFestivalSchema(year, data?.items || [])}
      />

      <main className="flex-1 max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="rounded-3xl border border-gold/20 bg-gradient-to-br from-gold/[0.08] via-background to-background p-8 shadow-sm">
          <div className="flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
            <div className="space-y-3">
              <div className="inline-flex items-center gap-2 rounded-full border border-gold/20 bg-gold/[0.06] px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-gold">
                <Sparkles className="h-3.5 w-3.5" />
                Festival Hub
              </div>
              <div>
                <h1 className="text-3xl font-playfair font-bold text-foreground sm:text-4xl">
                  Hindu Festival Calendar {year}
                </h1>
                <p className="mt-3 max-w-2xl text-sm leading-6 text-muted-foreground">
                  Explore major Hindu festivals, vrats, and observances month by month, with quick links to the full Panchang for each day.
                </p>
              </div>
            </div>

            <div className="flex items-center gap-3 self-start rounded-full border border-gold/20 bg-gold/[0.04] p-2">
              <button
                onClick={() => setYear((current) => current - 1)}
                className="rounded-full p-2 text-gold transition hover:bg-gold/10"
                aria-label="Previous year"
              >
                <ChevronLeft className="h-4 w-4" />
              </button>
              <span className="min-w-24 text-center text-sm font-semibold text-foreground">{year}</span>
              <button
                onClick={() => setYear((current) => current + 1)}
                className="rounded-full p-2 text-gold transition hover:bg-gold/10"
                aria-label="Next year"
              >
                <ChevronRight className="h-4 w-4" />
              </button>
            </div>
          </div>
        </div>

        {loading && <p className="py-12 text-center text-muted-foreground">Loading festival calendar...</p>}
        {error && <p className="py-12 text-center text-muted-foreground">{error}</p>}

        {!loading && !error && (
          <div className="mt-8 grid gap-6 lg:grid-cols-2 xl:grid-cols-3">
            {grouped.map(({ monthName, items }) => (
              <section key={monthName} className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm">
                <div className="flex items-center justify-between border-b border-gold/10 px-5 py-4">
                  <h2 className="text-lg font-semibold text-foreground">{monthName}</h2>
                  <span className="text-xs uppercase tracking-[0.2em] text-muted-foreground">
                    {items.length} items
                  </span>
                </div>

                <div className="space-y-3 p-5">
                  {items.length === 0 && (
                    <p className="text-sm text-muted-foreground">No listed observances for this month.</p>
                  )}

                  {items.map((item) => (
                    <div key={`${item.slug}-${item.date}`} className="rounded-xl border border-border/70 bg-background/80 p-4">
                      <div className="flex flex-wrap items-start justify-between gap-3">
                        <div className="space-y-2">
                          <Link to={`/festivals/${item.slug}`} className="text-base font-semibold text-foreground transition hover:text-gold">
                            {item.name}
                          </Link>
                          <p className="text-xs text-muted-foreground">{formatDisplayDate(item.date)}</p>
                        </div>
                        <span className={`rounded-full border px-2.5 py-1 text-[11px] font-semibold uppercase tracking-wide ${badgeClass[item.observance_type] || badgeClass.observance}`}>
                          {item.observance_type}
                        </span>
                      </div>
                      <p className="mt-3 text-sm leading-6 text-muted-foreground">{item.summary}</p>
                      <div className="mt-4 flex flex-wrap gap-4 text-sm">
                        <Link to={`/panchang/date/${item.date}`} className="text-gold transition hover:underline">
                          View full Panchang for this day
                        </Link>
                        <Link to="/panchang" className="text-gold transition hover:underline">
                          Plan your Puja -- Check Muhurat
                        </Link>
                      </div>
                    </div>
                  ))}
                </div>
              </section>
            ))}
          </div>
        )}

        <div className="mt-10 rounded-2xl border border-gold/20 bg-gold/[0.05] p-6 shadow-sm">
          <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
            <div>
              <h2 className="text-xl font-semibold text-foreground">Need a deeper Panchang view?</h2>
              <p className="mt-2 text-sm text-muted-foreground">
                Jump into the full Panchang for any date, or get personalised auspicious timing based on your birth chart.
              </p>
            </div>
            <div className="flex flex-wrap gap-3">
              <Link to="/panchang" className="inline-flex items-center gap-2 rounded-full border border-gold px-4 py-2 text-sm font-semibold text-gold transition hover:bg-gold/10">
                <CalendarDays className="h-4 w-4" />
                Get Panchang for any date
              </Link>
              <Link to="/birth-chart" className="inline-flex items-center gap-2 rounded-full bg-gold px-4 py-2 text-sm font-semibold text-background transition hover:opacity-90">
                Personalised auspicious timing
              </Link>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}
