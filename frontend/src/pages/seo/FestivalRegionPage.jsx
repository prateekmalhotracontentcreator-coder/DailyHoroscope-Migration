import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { Link, useParams } from 'react-router-dom';
import { ArrowLeft, CalendarDays, LoaderCircle, MapPinned, Sparkles } from 'lucide-react';
import { Footer } from '../../components/Footer';
import { SEO } from '../../components/SEO';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;
const SITE = 'https://www.everydayhoroscope.in';

function buildSchema(data, canonicalUrl) {
  if (!data) return null;
  return {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Event',
        name: `${data.festival} in ${data.region}`,
        startDate: data.date,
        description: data.summary,
        location: {
          '@type': 'Place',
          name: data.region,
        },
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

export function FestivalRegionPage() {
  const { festivalSlug = '', region = '' } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!festivalSlug || !region) {
      setLoading(false);
      setError('Festival region page not found.');
      setData(null);
      return;
    }

    let ignore = false;

    async function fetchPage() {
      try {
        setLoading(true);
        setError('');
        const response = await axios.get(`${API}/seo/festivals/${festivalSlug}/${region}`);
        if (!ignore) setData(response.data);
      } catch (err) {
        if (!ignore) {
          setData(null);
          setError(err?.response?.data?.detail || 'Unable to load this festival page right now.');
        }
      } finally {
        if (!ignore) setLoading(false);
      }
    }

    fetchPage();
    return () => {
      ignore = true;
    };
  }, [festivalSlug, region]);

  const canonicalUrl = festivalSlug && region ? `${SITE}/festivals/${festivalSlug}/${region}` : `${SITE}/festivals`;
  const schema = useMemo(() => buildSchema(data, canonicalUrl), [canonicalUrl, data]);
  const title = data ? data.meta_title : 'Festival by Region';
  const description = data ? data.meta_description : 'Regional festival dates and celebration customs.';

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
        noindex={!festivalSlug || !region}
      />

      <main className="flex-1 max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="mb-6 flex items-center gap-2 text-sm text-muted-foreground">
          <Link to="/festivals" className="hover:text-gold transition">Festivals</Link>
          <span>/</span>
          <span className="text-foreground">{data ? `${data.festival} in ${data.region}` : 'Regional Page'}</span>
        </div>

        <Link
          to="/festivals"
          className="mb-6 inline-flex items-center text-sm font-medium text-muted-foreground transition hover:text-gold"
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to festival hub
        </Link>

        {loading ? (
          <div className="flex items-center justify-center rounded-2xl border border-gold/15 bg-background/80 p-12 text-muted-foreground">
            <LoaderCircle className="mr-3 h-5 w-5 animate-spin text-gold" />
            Loading regional festival guide...
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
                    <MapPinned className="h-3.5 w-3.5" />
                    Regional Festival Guide
                  </div>
                  <h1 className="mt-4 text-3xl font-playfair font-bold text-foreground sm:text-4xl">
                    {data.title}
                  </h1>
                  <p className="mt-3 text-sm leading-7 text-muted-foreground">
                    {data.summary}
                  </p>
                </div>

                <div className="rounded-2xl border border-gold/20 bg-background/80 px-5 py-4 text-sm shadow-sm">
                  <p className="text-xs uppercase tracking-[0.18em] text-gold">Festival date</p>
                  <p className="mt-2 text-lg font-semibold text-foreground">{data.date}</p>
                  <p className="text-muted-foreground">{data.regional_name}</p>
                </div>
              </div>
            </section>

            <section className="mt-8 grid gap-8 lg:grid-cols-[1.05fr_0.95fr]">
              <div className="rounded-2xl border border-gold/20 bg-background/80 p-6 shadow-sm">
                <div className="flex items-center gap-2 text-gold">
                  <Sparkles className="h-4 w-4" />
                  <h2 className="text-xl font-semibold text-foreground">Local traditions</h2>
                </div>
                <ul className="mt-5 space-y-3 text-sm text-muted-foreground">
                  {data.traditions.map((item) => (
                    <li key={item} className="rounded-2xl border border-gold/10 bg-gold/[0.04] px-4 py-3">
                      {item}
                    </li>
                  ))}
                </ul>
              </div>

              <div className="rounded-2xl border border-gold/20 bg-background/80 p-6 shadow-sm">
                <div className="flex items-center gap-2 text-gold">
                  <CalendarDays className="h-4 w-4" />
                  <h2 className="text-xl font-semibold text-foreground">Auspicious timing</h2>
                </div>
                {data.auspicious_timing ? (
                  <div className="mt-5 grid gap-4 sm:grid-cols-2">
                    <div className="rounded-2xl border border-gold/10 bg-gold/[0.04] p-4 text-sm">
                      <p className="font-semibold text-foreground">Sunrise / Sunset</p>
                      <p className="mt-2 text-muted-foreground">{data.auspicious_timing.sunrise}</p>
                      <p className="text-muted-foreground">{data.auspicious_timing.sunset}</p>
                    </div>
                    <div className="rounded-2xl border border-gold/10 bg-gold/[0.04] p-4 text-sm">
                      <p className="font-semibold text-foreground">Tithi / Nakshatra</p>
                      <p className="mt-2 text-muted-foreground">{data.auspicious_timing.tithi}</p>
                      <p className="text-muted-foreground">{data.auspicious_timing.nakshatra}</p>
                    </div>
                    <div className="rounded-2xl border border-gold/10 bg-gold/[0.04] p-4 text-sm text-muted-foreground sm:col-span-2">
                      {data.auspicious_timing.note}
                    </div>
                  </div>
                ) : (
                  <p className="mt-5 text-sm text-muted-foreground">Timing details are unavailable right now.</p>
                )}
              </div>
            </section>

            <section className="mt-8 grid gap-8 lg:grid-cols-[0.95fr_1.05fr]">
              <div className="rounded-2xl border border-gold/20 bg-background/80 p-6 shadow-sm">
                <h2 className="text-xl font-semibold text-foreground">How it is celebrated</h2>
                <ol className="mt-5 space-y-3 text-sm text-muted-foreground">
                  {data.celebration_steps.map((item, index) => (
                    <li key={item} className="rounded-2xl border border-gold/10 bg-gold/[0.04] px-4 py-3">
                      <span className="mr-2 font-semibold text-gold">{index + 1}.</span>
                      {item}
                    </li>
                  ))}
                </ol>
              </div>

              <div className="rounded-2xl border border-gold/20 bg-background/80 p-6 shadow-sm">
                <h2 className="text-xl font-semibold text-foreground">Did you know?</h2>
                <p className="mt-5 text-sm leading-7 text-muted-foreground">{data.did_you_know}</p>
                <div className="mt-6 rounded-2xl border border-gold/15 bg-gold/[0.05] p-5">
                  <p className="text-sm font-semibold text-foreground">Related pages</p>
                  <div className="mt-4 flex flex-wrap gap-3">
                    {data.related_pages.map((item) => (
                      <a
                        key={item.href}
                        href={item.href}
                        className="rounded-full border border-gold/20 px-4 py-2 text-sm text-muted-foreground transition hover:text-gold"
                      >
                        {item.label}
                      </a>
                    ))}
                  </div>
                </div>
              </div>
            </section>

            <section className="mt-8 rounded-2xl border border-gold/20 bg-background/80 p-6 shadow-sm">
              <h2 className="text-xl font-semibold text-foreground">FAQ</h2>
              <div className="mt-5 space-y-3">
                {data.faq.map((item) => (
                  <details key={item.question} className="rounded-2xl border border-gold/10 bg-gold/[0.04] px-4 py-3">
                    <summary className="cursor-pointer text-sm font-semibold text-foreground">{item.question}</summary>
                    <p className="mt-3 text-sm leading-6 text-muted-foreground">{item.answer}</p>
                  </details>
                ))}
              </div>
            </section>
          </>
        ) : null}
      </main>

      <Footer />
    </div>
  );
}
