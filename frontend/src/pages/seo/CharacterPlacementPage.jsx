import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { Link, useParams } from 'react-router-dom';
import { ArrowLeft, LoaderCircle, Sparkles, UserRoundSearch } from 'lucide-react';
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
        '@type': 'Article',
        headline: data.title,
        description: data.summary,
        url: canonicalUrl,
        author: {
          '@type': 'Organization',
          name: 'EverydayHoroscope',
        },
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

export function CharacterPlacementPage() {
  const { sign = '', chartPoint = '', house = '' } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!sign || !chartPoint || !house) {
      setLoading(false);
      setError('Character placement page not found.');
      setData(null);
      return;
    }

    let ignore = false;

    async function fetchPlacement() {
      try {
        setLoading(true);
        setError('');
        const response = await axios.get(`${API}/seo/traits/${sign}/${chartPoint}/${house}`);
        if (!ignore) setData(response.data);
      } catch (err) {
        if (!ignore) {
          setData(null);
          setError(err?.response?.data?.detail || 'Unable to load this placement page right now.');
        }
      } finally {
        if (!ignore) setLoading(false);
      }
    }

    fetchPlacement();
    return () => {
      ignore = true;
    };
  }, [chartPoint, house, sign]);

  const canonicalUrl = sign && chartPoint && house ? `${SITE}/traits/${sign}/${chartPoint}/${house}` : `${SITE}/traits`;
  const schema = useMemo(() => buildSchema(data, canonicalUrl), [canonicalUrl, data]);
  const title = data ? data.meta_title : 'Character Placements';
  const description = data ? data.meta_description : 'Sign, house, and chart-point personality pages.';

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
        noindex={!sign || !chartPoint || !house}
      />

      <main className="flex-1 max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="mb-6 flex items-center gap-2 text-sm text-muted-foreground">
          <Link to="/birth-chart" className="hover:text-gold transition">Birth Chart</Link>
          <span>/</span>
          <span className="text-foreground">{data ? data.title : 'Placement'}</span>
        </div>

        <Link
          to="/birth-chart"
          className="mb-6 inline-flex items-center text-sm font-medium text-muted-foreground transition hover:text-gold"
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Find your chart placements
        </Link>

        {loading ? (
          <div className="flex items-center justify-center rounded-2xl border border-gold/15 bg-background/80 p-12 text-muted-foreground">
            <LoaderCircle className="mr-3 h-5 w-5 animate-spin text-gold" />
            Loading placement profile...
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
                    <UserRoundSearch className="h-3.5 w-3.5" />
                    Character Placement
                  </div>
                  <h1 className="mt-4 text-3xl font-playfair font-bold text-foreground sm:text-4xl">
                    {data.title}
                  </h1>
                  <p className="mt-3 text-sm leading-7 text-muted-foreground">
                    {data.summary}
                  </p>
                </div>

                <div className="rounded-2xl border border-gold/20 bg-background/80 px-5 py-4 text-sm shadow-sm">
                  <p className="text-xs uppercase tracking-[0.18em] text-gold">Placement focus</p>
                  <p className="mt-2 font-semibold text-foreground">{data.chart_point} in the {data.house}</p>
                  <p className="text-muted-foreground">{data.sign}</p>
                </div>
              </div>
            </section>

            <section className="mt-8 grid gap-8 lg:grid-cols-[1.05fr_0.95fr]">
              <div className="rounded-2xl border border-gold/20 bg-background/80 p-6 shadow-sm">
                <div className="flex items-center gap-2 text-gold">
                  <Sparkles className="h-4 w-4" />
                  <h2 className="text-xl font-semibold text-foreground">Core traits</h2>
                </div>
                <ul className="mt-5 space-y-3 text-sm text-muted-foreground">
                  {data.core_traits.map((item) => (
                    <li key={item} className="rounded-2xl border border-gold/10 bg-gold/[0.04] px-4 py-3">
                      {item}
                    </li>
                  ))}
                </ul>
              </div>

              <div className="rounded-2xl border border-gold/20 bg-background/80 p-6 shadow-sm">
                <h2 className="text-xl font-semibold text-foreground">Life areas activated</h2>
                <ul className="mt-5 space-y-3 text-sm text-muted-foreground">
                  {data.life_areas.map((item) => (
                    <li key={item} className="rounded-2xl border border-gold/10 bg-gold/[0.04] px-4 py-3">
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            </section>

            <section className="mt-8 grid gap-8 lg:grid-cols-3">
              <div className="rounded-2xl border border-gold/20 bg-background/80 p-6 shadow-sm">
                <h2 className="text-xl font-semibold text-foreground">Strengths</h2>
                <ul className="mt-5 space-y-3 text-sm text-muted-foreground">
                  {data.strengths.map((item) => (
                    <li key={item} className="rounded-2xl border border-gold/10 bg-gold/[0.04] px-4 py-3">
                      {item}
                    </li>
                  ))}
                </ul>
              </div>

              <div className="rounded-2xl border border-gold/20 bg-background/80 p-6 shadow-sm">
                <h2 className="text-xl font-semibold text-foreground">Shadow side</h2>
                <ul className="mt-5 space-y-3 text-sm text-muted-foreground">
                  {data.shadow_side.map((item) => (
                    <li key={item} className="rounded-2xl border border-gold/10 bg-gold/[0.04] px-4 py-3">
                      {item}
                    </li>
                  ))}
                </ul>
              </div>

              <div className="rounded-2xl border border-gold/20 bg-background/80 p-6 shadow-sm">
                <h2 className="text-xl font-semibold text-foreground">Compatible placements</h2>
                <ul className="mt-5 space-y-3 text-sm text-muted-foreground">
                  {data.compatible_placements.map((item) => (
                    <li key={item} className="rounded-2xl border border-gold/10 bg-gold/[0.04] px-4 py-3">
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            </section>

            <section className="mt-8 grid gap-8 lg:grid-cols-[1.05fr_0.95fr]">
              <div className="rounded-2xl border border-gold/20 bg-background/80 p-6 shadow-sm">
                <h2 className="text-xl font-semibold text-foreground">Vedic perspective</h2>
                <div className="mt-5 space-y-3">
                  {data.vedic_perspective.map((item) => (
                    <p key={item} className="rounded-2xl border border-gold/10 bg-gold/[0.04] px-4 py-3 text-sm leading-6 text-muted-foreground">
                      {item}
                    </p>
                  ))}
                </div>
                <Link
                  to="/birth-chart"
                  className="mt-6 inline-flex items-center rounded-full bg-gold px-5 py-3 text-sm font-semibold text-background transition hover:opacity-90"
                >
                  Find your chart placements
                </Link>
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

            {data.famous_people?.length ? (
              <section className="mt-8 rounded-2xl border border-gold/20 bg-background/80 p-6 shadow-sm">
                <h2 className="text-xl font-semibold text-foreground">Famous people</h2>
                <div className="mt-5 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                  {data.famous_people.map((item) => (
                    <article key={item.name} className="rounded-2xl border border-gold/10 bg-gold/[0.04] p-5">
                      <h3 className="text-base font-semibold text-foreground">{item.name}</h3>
                      <p className="mt-2 text-sm leading-6 text-muted-foreground">{item.note}</p>
                    </article>
                  ))}
                </div>
              </section>
            ) : null}
          </>
        ) : null}
      </main>

      <Footer />
    </div>
  );
}
