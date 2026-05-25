import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { Link, useParams } from 'react-router-dom';
import { ArrowLeft, LoaderCircle, Orbit, Sparkles } from 'lucide-react';
import { Footer } from '../../components/Footer';
import { SEO } from '../../components/SEO';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;
const SITE = 'https://www.everydayhoroscope.in';
const PLANETS = ['sun', 'moon', 'mars', 'mercury', 'jupiter', 'venus', 'saturn', 'rahu', 'ketu'];
const SIGNS = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces'];

function buildSchema(data, canonicalUrl) {
  if (!data) return null;
  return {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Event',
        name: `${data.planet} in ${data.sign}`,
        startDate: data.transit_window.start_date,
        endDate: data.transit_window.end_date,
        eventStatus: data.transit_window.active_now ? 'https://schema.org/EventScheduled' : 'https://schema.org/EventScheduled',
        eventAttendanceMode: 'https://schema.org/OnlineEventAttendanceMode',
        description: data.summary,
        url: canonicalUrl,
      },
      {
        '@type': 'FAQPage',
        mainEntity: data.faq.map((item) => ({
          '@type': 'Question',
          name: item.question,
          acceptedAnswer: {
            '@type': 'Answer',
            text: item.answer,
          },
        })),
      },
    ],
  };
}

export function TransitProfilePage() {
  const { transitSlug = '' } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const parts = transitSlug.split('-in-').map((part) => part.trim().toLowerCase()).filter(Boolean);
  const isValid = parts.length === 2 && PLANETS.includes(parts[0]) && SIGNS.includes(parts[1]);
  const [planetSlug, signSlug] = parts;

  useEffect(() => {
    if (!isValid) {
      setLoading(false);
      setError('Transit page not found.');
      setData(null);
      return;
    }

    let ignore = false;

    async function fetchTransit() {
      try {
        setLoading(true);
        setError('');
        const response = await axios.get(`${API}/seo/transit/${planetSlug}/${signSlug}`);
        if (!ignore) setData(response.data);
      } catch (err) {
        if (!ignore) {
          setData(null);
          setError(err?.response?.data?.detail || 'Unable to load this transit profile right now.');
        }
      } finally {
        if (!ignore) setLoading(false);
      }
    }

    fetchTransit();
    return () => {
      ignore = true;
    };
  }, [isValid, planetSlug, signSlug]);

  const canonicalUrl = isValid ? `${SITE}/transits/${transitSlug}` : `${SITE}/transits`;
  const schema = useMemo(() => buildSchema(data, canonicalUrl), [canonicalUrl, data]);
  const title = data ? data.meta_title : 'Transit Profiles';
  const description = data ? data.meta_description : 'Planetary transit dates, effects, and remedies.';

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <SEO
        title={title}
        description={description}
        canonical={canonicalUrl}
        hreflang={[
          { lang: 'en-in', href: canonicalUrl },
          { lang: 'en-us', href: canonicalUrl },
        ]}
        jsonLd={schema}
        noindex={!isValid}
      />

      <main className="flex-1 max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="mb-6 flex items-center gap-2 text-sm text-muted-foreground">
          <Link to="/birth-chart" className="hover:text-gold transition">Birth Chart</Link>
          <span>/</span>
          <span className="text-foreground">{data ? `${data.planet} in ${data.sign}` : 'Transit Profile'}</span>
        </div>

        <Link
          to="/birth-chart"
          className="mb-6 inline-flex items-center text-sm font-medium text-muted-foreground transition hover:text-gold"
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Check your full chart
        </Link>

        {loading ? (
          <div className="flex items-center justify-center rounded-2xl border border-gold/15 bg-background/80 p-12 text-muted-foreground">
            <LoaderCircle className="mr-3 h-5 w-5 animate-spin text-gold" />
            Loading transit profile...
          </div>
        ) : error ? (
          <div className="rounded-2xl border border-red-400/20 bg-red-500/10 p-6 text-sm text-red-200">
            {error}
          </div>
        ) : data ? (
          <>
            <section className="rounded-3xl border border-gold/20 bg-gradient-to-br from-gold/[0.08] via-background to-background p-8 shadow-sm">
              <div className="flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
                <div className="max-w-3xl">
                  <div className="inline-flex items-center gap-2 rounded-full border border-gold/20 bg-gold/[0.06] px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-gold">
                    <Orbit className="h-3.5 w-3.5" />
                    Transit Profile
                  </div>
                  <h1 className="mt-4 text-3xl font-playfair font-bold text-foreground sm:text-4xl">
                    {data.title}
                  </h1>
                  <p className="mt-3 text-sm leading-7 text-muted-foreground">
                    {data.summary}
                  </p>
                </div>

                <div className="rounded-2xl border border-gold/20 bg-background/80 px-5 py-4 text-sm shadow-sm">
                  <p className="font-semibold text-foreground">{data.transit_window.active_now ? 'Active now' : 'Upcoming window'}</p>
                  <p className="mt-1 text-muted-foreground">{data.transit_window.start_date} to {data.transit_window.end_date}</p>
                  <p className="mt-2 text-xs uppercase tracking-[0.18em] text-gold">{data.theme_phrase}</p>
                </div>
              </div>
            </section>

            <section className="mt-8 grid gap-8 lg:grid-cols-[1.05fr_0.95fr]">
              <div className="rounded-2xl border border-gold/20 bg-background/80 p-6 shadow-sm">
                <div className="flex items-center gap-2 text-gold">
                  <Sparkles className="h-4 w-4" />
                  <h2 className="text-xl font-semibold text-foreground">Transit dates and snapshot</h2>
                </div>
                <div className="mt-5 grid gap-4 sm:grid-cols-2">
                  <div className="rounded-2xl border border-gold/10 bg-gold/[0.04] p-4">
                    <p className="text-xs uppercase tracking-[0.18em] text-gold">Window</p>
                    <p className="mt-2 text-sm text-foreground">{data.transit_window.start_date}</p>
                    <p className="text-sm text-muted-foreground">to {data.transit_window.end_date}</p>
                  </div>
                  <div className="rounded-2xl border border-gold/10 bg-gold/[0.04] p-4">
                    <p className="text-xs uppercase tracking-[0.18em] text-gold">Current sky</p>
                    <p className="mt-2 text-sm text-foreground">{data.current_snapshot.sign}</p>
                    <p className="text-sm text-muted-foreground">
                      Longitude {Number(data.current_snapshot.longitude || 0).toFixed(2)}°
                    </p>
                  </div>
                </div>
                <div className="mt-5 rounded-2xl border border-gold/10 bg-gold/[0.04] p-4 text-sm text-muted-foreground">
                  {data.transit_window.active_now
                    ? `${data.planet} has been in ${data.sign} for ${data.transit_window.days_elapsed ?? 0} days and has ${data.transit_window.days_remaining ?? 0} days left in this run.`
                    : `${data.planet} next enters ${data.sign} on ${data.transit_window.next_occurrence_date}.`}
                </div>
              </div>

              <div className="rounded-2xl border border-gold/20 bg-background/80 p-6 shadow-sm">
                <h2 className="text-xl font-semibold text-foreground">Ritual and remedy</h2>
                <p className="mt-4 text-sm leading-7 text-muted-foreground">{data.ritual}</p>
                <ul className="mt-5 space-y-3 text-sm text-muted-foreground">
                  {data.remedies.map((item) => (
                    <li key={item} className="rounded-2xl border border-gold/10 bg-gold/[0.04] px-4 py-3">
                      {item}
                    </li>
                  ))}
                </ul>
                <Link
                  to="/birth-chart"
                  className="mt-6 inline-flex items-center rounded-full bg-gold px-5 py-3 text-sm font-semibold text-background transition hover:opacity-90"
                >
                  Check if {data.planet} is transiting your chart now
                </Link>
              </div>
            </section>

            <section className="mt-8 rounded-2xl border border-gold/20 bg-background/80 p-6 shadow-sm">
              <h2 className="text-xl font-semibold text-foreground">Key themes</h2>
              <div className="mt-5 grid gap-4 md:grid-cols-2">
                {data.themes.map((item) => (
                  <article key={item} className="rounded-2xl border border-gold/10 bg-gold/[0.04] p-5 text-sm leading-6 text-muted-foreground">
                    {item}
                  </article>
                ))}
              </div>
            </section>

            <section className="mt-8 rounded-2xl border border-gold/20 bg-background/80 p-6 shadow-sm">
              <h2 className="text-xl font-semibold text-foreground">For your rising sign</h2>
              <div className="mt-5 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
                {data.for_signs.map((item) => (
                  <article key={item.sign_slug} className="rounded-2xl border border-gold/10 bg-gold/[0.04] p-5">
                    <div className="flex items-center justify-between gap-3">
                      <h3 className="text-base font-semibold text-foreground">{item.sign}</h3>
                      <span className="text-xs font-semibold uppercase tracking-[0.16em] text-gold">{item.activated_house}</span>
                    </div>
                    <p className="mt-3 text-sm leading-6 text-muted-foreground">{item.message}</p>
                  </article>
                ))}
              </div>
            </section>

            <section className="mt-8 grid gap-8 lg:grid-cols-[0.9fr_1.1fr]">
              <div className="rounded-2xl border border-gold/20 bg-background/80 p-6 shadow-sm">
                <h2 className="text-xl font-semibold text-foreground">Watch for</h2>
                <ul className="mt-5 space-y-3 text-sm text-muted-foreground">
                  {data.watch_for.map((item) => (
                    <li key={item} className="rounded-2xl border border-gold/10 bg-gold/[0.04] px-4 py-3">
                      {item}
                    </li>
                  ))}
                </ul>
              </div>

              <div className="rounded-2xl border border-gold/20 bg-background/80 p-6 shadow-sm">
                <h2 className="text-xl font-semibold text-foreground">FAQ</h2>
                <div className="mt-5 space-y-3">
                  {data.faq.map((item) => (
                    <details key={item.question} className="rounded-2xl border border-gold/10 bg-gold/[0.04] px-4 py-3">
                      <summary className="cursor-pointer text-sm font-semibold text-foreground">{item.question}</summary>
                      <p className="mt-3 text-sm leading-6 text-muted-foreground">{item.answer}</p>
                    </details>
                  ))}
                </div>
              </div>
            </section>
          </>
        ) : null}
      </main>

      <Footer />
    </div>
  );
}
