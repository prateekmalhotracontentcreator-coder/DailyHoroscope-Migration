import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { Link, Navigate, useParams } from 'react-router-dom';
import { ArrowLeft, HeartHandshake, LoaderCircle, Sparkles, Star } from 'lucide-react';
import { Footer } from '../../components/Footer';
import { SEO } from '../../components/SEO';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;
const SITE = 'https://www.everydayhoroscope.in';
const SIGN_SLUGS = [
  'aries',
  'taurus',
  'gemini',
  'cancer',
  'leo',
  'virgo',
  'libra',
  'scorpio',
  'sagittarius',
  'capricorn',
  'aquarius',
  'pisces',
];

const BAND_STYLES = {
  excellent: 'border-emerald-400/30 bg-emerald-500/15 text-emerald-300',
  'very-good': 'border-sky-400/30 bg-sky-500/15 text-sky-300',
  good: 'border-amber-400/30 bg-amber-500/15 text-amber-300',
  challenging: 'border-red-400/30 bg-red-500/15 text-red-300',
};

function titleCaseSlug(slug) {
  return slug.split('-').map((part) => part.charAt(0).toUpperCase() + part.slice(1)).join(' ');
}

function buildDatasetSchema(data, canonicalUrl) {
  if (!data) return null;
  return {
    '@context': 'https://schema.org',
    '@type': 'Dataset',
    name: `${data.sign1} and ${data.sign2} Compatibility`,
    description: `Ashta-Koota compatibility score for ${data.sign1} and ${data.sign2}, including all 8 Koota breakdowns.`,
    url: canonicalUrl,
    creator: {
      '@type': 'Organization',
      name: 'EverydayHoroscope',
    },
    measurementTechnique: 'Ashta-Koota Gun Milan',
    variableMeasured: data.kootas.map((item) => item.name),
  };
}

export function CompatibilityPage() {
  const { signPair = '' } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const parts = signPair.split('-and-').map((part) => part.trim().toLowerCase()).filter(Boolean);
  const isValidPair = parts.length === 2 && parts.every((part) => SIGN_SLUGS.includes(part));
  const canonicalPair = isValidPair ? [...parts].sort().join('-and-') : '';

  useEffect(() => {
    if (!isValidPair) {
      setLoading(false);
      setError('Compatibility page not found.');
      setData(null);
      return;
    }

    let ignore = false;

    async function fetchCompatibility() {
      try {
        setLoading(true);
        setError('');
        const response = await axios.get(`${API}/compatibility/${canonicalPair}`);
        if (!ignore) setData(response.data);
      } catch (err) {
        if (!ignore) {
          setData(null);
          setError(err?.response?.data?.detail || 'Unable to load this compatibility page right now.');
        }
      } finally {
        if (!ignore) setLoading(false);
      }
    }

    fetchCompatibility();
    return () => {
      ignore = true;
    };
  }, [canonicalPair, isValidPair]);

  const canonicalUrl = isValidPair ? `${SITE}/compatibility/${canonicalPair}` : `${SITE}/compatibility/name`;
  const schema = useMemo(() => buildDatasetSchema(data, canonicalUrl), [canonicalUrl, data]);

  if (isValidPair && canonicalPair !== signPair) {
    return <Navigate to={`/compatibility/${canonicalPair}`} replace />;
  }
  const title = data
    ? `${data.sign1} and ${data.sign2} Compatibility - Marriage Gun Milan Score`
    : 'Compatibility by Moon Sign';
  const description = data
    ? `Are ${data.sign1} and ${data.sign2} compatible for marriage? View full Ashta-Koota Gun Milan analysis with score out of 36.`
    : 'Moon sign compatibility and Gun Milan insights.';
  const badgeClass = data ? BAND_STYLES[data.band] || BAND_STYLES.good : BAND_STYLES.good;

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
        noindex={!isValidPair}
      />

      <main className="flex-1 max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="mb-6 flex items-center gap-2 text-sm text-muted-foreground">
          <Link to="/compatibility/name" className="hover:text-gold transition">Compatibility</Link>
          <span>/</span>
          <span className="text-foreground">
            {isValidPair ? `${titleCaseSlug(parts[0] || '')} and ${titleCaseSlug(parts[1] || '')}` : 'Moon Sign Match'}
          </span>
        </div>

        <Link
          to="/compatibility/name"
          className="mb-6 inline-flex items-center text-sm font-medium text-muted-foreground transition hover:text-gold"
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Try name compatibility
        </Link>

        {loading ? (
          <div className="flex items-center justify-center rounded-2xl border border-gold/15 bg-background/80 p-12 text-muted-foreground">
            <LoaderCircle className="mr-3 h-5 w-5 animate-spin text-gold" />
            Loading compatibility analysis...
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
                    <HeartHandshake className="h-3.5 w-3.5" />
                    Marriage Gun Milan
                  </div>
                  <h1 className="mt-4 text-3xl font-playfair font-bold text-foreground sm:text-4xl">
                    {data.sign1} and {data.sign2} Compatibility
                  </h1>
                  <p className="mt-3 text-sm leading-6 text-muted-foreground">
                    {data.summary}
                  </p>
                </div>

                <div className="rounded-3xl border border-gold/20 bg-background/80 px-6 py-5 text-center shadow-sm">
                  <p className="text-xs font-semibold uppercase tracking-[0.18em] text-gold">Overall score</p>
                  <div className="mt-3 flex items-end justify-center gap-2">
                    <span className="text-5xl font-playfair font-bold text-foreground">{data.compatibility_score}</span>
                    <span className="pb-1 text-lg text-muted-foreground">/ 36</span>
                  </div>
                  <div className={`mt-4 inline-flex rounded-full border px-3 py-1 text-xs font-semibold uppercase tracking-[0.18em] ${badgeClass}`}>
                    {data.verdict}
                  </div>
                  <p className="mt-3 text-xs text-muted-foreground">
                    Based on {data.sample_size} nakshatra pairings across both moon signs
                  </p>
                </div>
              </div>
            </section>

            <section className="mt-8 grid gap-8 lg:grid-cols-[1.1fr_0.9fr]">
              <div className="rounded-2xl border border-gold/20 bg-background/80 p-6 shadow-sm">
                <div className="flex items-center gap-2 text-gold">
                  <Sparkles className="h-4 w-4" />
                  <h2 className="text-xl font-semibold text-foreground">All 8 Koota Scores</h2>
                </div>
                <div className="mt-5 overflow-hidden rounded-2xl border border-gold/10">
                  <table className="min-w-full divide-y divide-gold/10 text-sm">
                    <thead className="bg-gold/[0.06] text-left text-xs uppercase tracking-[0.18em] text-muted-foreground">
                      <tr>
                        <th className="px-4 py-3">Koota</th>
                        <th className="px-4 py-3">Score</th>
                        <th className="px-4 py-3">Reading</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gold/10">
                      {data.kootas.map((item) => (
                        <tr key={item.key}>
                          <td className="px-4 py-4 font-semibold text-foreground">{item.name}</td>
                          <td className="px-4 py-4 text-muted-foreground">{item.score} / {item.max_score}</td>
                          <td className="px-4 py-4 text-muted-foreground">{item.label}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              <div className="rounded-2xl border border-gold/20 bg-background/80 p-6 shadow-sm">
                <div className="flex items-center gap-2 text-gold">
                  <Star className="h-4 w-4" />
                  <h2 className="text-xl font-semibold text-foreground">Marriage Timing Note</h2>
                </div>
                <p className="mt-5 text-sm leading-7 text-muted-foreground">
                  {data.marriage_timing_note}
                </p>
                <div className="mt-6 rounded-2xl border border-gold/15 bg-gold/[0.05] p-5">
                  <p className="text-sm font-semibold text-foreground">Next step for real marriage matching</p>
                  <p className="mt-2 text-sm leading-6 text-muted-foreground">
                    A sign-level page is a strong starting point, but real Gun Milan should also check birth nakshatra, Manglik factors, dashas, and partner timing.
                  </p>
                  <Link
                    to="/birth-chart"
                    className="mt-4 inline-flex items-center rounded-full bg-gold px-5 py-3 text-sm font-semibold text-background transition hover:opacity-90"
                  >
                    Get your full 36-attribute Gun Milan report
                  </Link>
                </div>
              </div>
            </section>

            <section className="mt-8 rounded-2xl border border-gold/20 bg-background/80 p-6 shadow-sm">
              <h2 className="text-xl font-semibold text-foreground">Strengths and sensitive areas</h2>
              <div className="mt-5 grid gap-4 md:grid-cols-2">
                {data.kootas.map((item) => (
                  <article key={item.key} className="rounded-2xl border border-gold/10 bg-gold/[0.04] p-5">
                    <div className="flex items-center justify-between gap-3">
                      <h3 className="text-base font-semibold text-foreground">{item.name}</h3>
                      <span className="text-xs font-semibold uppercase tracking-[0.16em] text-gold">
                        {item.score}/{item.max_score}
                      </span>
                    </div>
                    <p className="mt-2 text-sm text-muted-foreground">{item.meaning}</p>
                    <p className="mt-3 text-sm leading-6 text-muted-foreground">{item.narrative}</p>
                  </article>
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
