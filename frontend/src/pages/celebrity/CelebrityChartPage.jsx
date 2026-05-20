import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { Link, useParams } from 'react-router-dom';
import { ArrowLeft, LoaderCircle, Sparkles } from 'lucide-react';
import { Footer } from '../../components/Footer';
import { SEO } from '../../components/SEO';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;
const SITE = 'https://www.everydayhoroscope.in';

const CATEGORY_STYLES = {
  bollywood: 'border-pink-400/30 bg-pink-500/15 text-pink-300',
  cricket: 'border-sky-400/30 bg-sky-500/15 text-sky-300',
  politics: 'border-amber-400/30 bg-amber-500/15 text-amber-300',
  business: 'border-emerald-400/30 bg-emerald-500/15 text-emerald-300',
  spiritual: 'border-violet-400/30 bg-violet-500/15 text-violet-300',
  historical: 'border-stone-400/30 bg-stone-500/15 text-stone-300',
  global: 'border-indigo-400/30 bg-indigo-500/15 text-indigo-300',
};

function formatDob(value) {
  return new Date(`${value}T12:00:00`).toLocaleDateString('en-IN', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  });
}

function buildSchema(item) {
  if (!item) return null;
  return {
    '@context': 'https://schema.org',
    '@type': 'Person',
    name: item.name,
    birthDate: item.dob,
    birthPlace: {
      '@type': 'Place',
      name: item.pob,
    },
    url: `${SITE}/celebrity-horoscopes/${item.slug}`,
    description: `${item.name}'s Vedic birth chart profile on EverydayHoroscope.`,
  };
}

function renderSummaryValue(value, fallback = '--') {
  if (value === null || value === undefined || value === '') return fallback;
  return value;
}

export function CelebrityChartPage() {
  const { slug } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let ignore = false;

    async function fetchCelebrityChart() {
      try {
        setLoading(true);
        setError('');
        const response = await axios.get(`${API}/celebrities/${slug}`);
        if (!ignore) setData(response.data);
      } catch (err) {
        if (!ignore) {
          setData(null);
          setError(err?.response?.status === 404 ? 'Celebrity chart not found.' : 'Unable to load this celebrity chart right now.');
        }
      } finally {
        if (!ignore) setLoading(false);
      }
    }

    fetchCelebrityChart();
    return () => {
      ignore = true;
    };
  }, [slug]);

  const canonicalUrl = data ? `${SITE}/celebrity-horoscopes/${data.slug}` : `${SITE}/celebrity-horoscopes`;
  const summary = data?.chart_summary || {};
  const lagna = summary.lagna || {};
  const moonSign = summary.moon_sign || {};
  const sunSign = summary.sun_sign || {};
  const nakshatra = summary.nakshatra || {};
  const currentDasha = summary.current_dasha || {};
  const schema = useMemo(() => buildSchema(data), [data]);
  const description = data
    ? `${data.name}'s Vedic birth chart - Moon sign ${moonSign.sign || 'unknown'}, Lagna ${lagna.sign || 'unknown'}, ${nakshatra.name || 'birth star'} Nakshatra. Full Kundali analysis with Dasha timeline.`
    : 'Celebrity Vedic birth chart.';

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <SEO
        title={data ? `${data.name} Birth Chart - Vedic Horoscope & Kundali` : 'Celebrity Birth Chart'}
        description={description}
        url={canonicalUrl}
        schema={schema}
      />

      <main className="flex-1 max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="mb-6 flex items-center gap-2 text-sm text-muted-foreground">
          <Link to="/celebrity-horoscopes" className="hover:text-gold transition">Celebrity Horoscopes</Link>
          <span>/</span>
          <span className="text-foreground">{data?.name || 'Chart'}</span>
        </div>

        <Link
          to="/celebrity-horoscopes"
          className="mb-6 inline-flex items-center text-sm font-medium text-muted-foreground transition hover:text-gold"
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          All Celebrity Charts
        </Link>

        {loading ? (
          <div className="flex items-center justify-center rounded-2xl border border-gold/15 bg-background/80 p-12 text-muted-foreground">
            <LoaderCircle className="mr-3 h-5 w-5 animate-spin text-gold" />
            Loading celebrity chart...
          </div>
        ) : error ? (
          <div className="rounded-2xl border border-red-400/20 bg-red-500/10 p-6 text-sm text-red-200">
            {error}
          </div>
        ) : (
          <>
            <section className="rounded-3xl border border-gold/20 bg-gradient-to-br from-gold/[0.08] via-background to-background p-8 shadow-sm">
              <div className="flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
                <div>
                  <span className={`inline-flex rounded-full border px-3 py-1 text-xs font-medium ${CATEGORY_STYLES[data.category] || 'border-gold/30 bg-gold/10 text-gold'}`}>
                    {data.category_label}
                  </span>
                  <h1 className="mt-4 text-3xl font-playfair font-bold text-foreground sm:text-4xl">
                    {data.name} Birth Chart
                  </h1>
                  <p className="mt-3 text-sm leading-6 text-muted-foreground">
                    Born on {formatDob(data.dob)} in {data.pob}
                    {data.birth_time_confirmed ? ` at ${data.tob}` : ' · birth time not confirmed'}
                  </p>
                </div>

                <div className="rounded-2xl border border-gold/20 bg-background/80 px-5 py-4 text-sm shadow-sm">
                  <p className="font-semibold text-foreground">{data.cached ? 'Cached chart' : 'Fresh chart'}</p>
                  <p className="mt-1 text-muted-foreground">
                    Source: {data.source}
                  </p>
                </div>
              </div>
            </section>

            <div className="mt-8 grid gap-8 lg:grid-cols-[0.95fr_1.05fr]">
              <section className="rounded-2xl border border-gold/20 bg-background/80 p-6 shadow-sm">
                <div className="flex items-center gap-2 text-gold">
                  <Sparkles className="h-4 w-4" />
                  <h2 className="text-xl font-semibold text-foreground">Chart Summary</h2>
                </div>
                <div className="mt-5 grid gap-4 sm:grid-cols-2">
                  <div className="rounded-xl border border-gold/15 bg-gold/[0.04] p-4">
                    <p className="text-xs uppercase tracking-[0.2em] text-gold">Lagna</p>
                    <p className="mt-2 text-lg font-semibold text-foreground">
                      {data.birth_time_confirmed ? renderSummaryValue(lagna.sign_vedic || lagna.sign) : 'Unknown'}
                    </p>
                  </div>
                  <div className="rounded-xl border border-gold/15 bg-gold/[0.04] p-4">
                    <p className="text-xs uppercase tracking-[0.2em] text-gold">Moon Sign</p>
                    <p className="mt-2 text-lg font-semibold text-foreground">
                      {renderSummaryValue(moonSign.sign_vedic || moonSign.sign)}
                    </p>
                  </div>
                  <div className="rounded-xl border border-gold/15 bg-gold/[0.04] p-4">
                    <p className="text-xs uppercase tracking-[0.2em] text-gold">Sun Sign</p>
                    <p className="mt-2 text-lg font-semibold text-foreground">
                      {renderSummaryValue(sunSign.sign_vedic || sunSign.sign)}
                    </p>
                  </div>
                  <div className="rounded-xl border border-gold/15 bg-gold/[0.04] p-4">
                    <p className="text-xs uppercase tracking-[0.2em] text-gold">Nakshatra</p>
                    <p className="mt-2 text-lg font-semibold text-foreground">
                      {renderSummaryValue(nakshatra.name)}
                    </p>
                    <p className="mt-1 text-xs text-muted-foreground">
                      Pada {renderSummaryValue(nakshatra.pada)} · Lord {renderSummaryValue(nakshatra.lord)}
                    </p>
                  </div>
                  <div className="rounded-xl border border-gold/15 bg-gold/[0.04] p-4 sm:col-span-2">
                    <p className="text-xs uppercase tracking-[0.2em] text-gold">Current Mahadasha</p>
                    <p className="mt-2 text-lg font-semibold text-foreground">
                      {renderSummaryValue(currentDasha.planet)}
                    </p>
                    <p className="mt-1 text-xs text-muted-foreground">
                      {currentDasha.start && currentDasha.end ? `${currentDasha.start} to ${currentDasha.end}` : 'Timeline available below'}
                    </p>
                  </div>
                </div>

                {data.chart_svg ? (
                  <div className="mt-6 rounded-xl border border-gold/15 bg-[#0f0d0a] p-4">
                    <div dangerouslySetInnerHTML={{ __html: data.chart_svg }} />
                  </div>
                ) : (
                  <div className="mt-6 rounded-xl border border-gold/15 bg-background p-4 text-sm text-muted-foreground">
                    Lagna chart is hidden because the birth time is not confirmed for this celebrity.
                  </div>
                )}
              </section>

              <section className="rounded-2xl border border-gold/20 bg-background/80 p-6 shadow-sm">
                <h2 className="text-xl font-semibold text-foreground">Key Planetary Positions</h2>
                <div className="mt-5 overflow-hidden rounded-xl border border-gold/15">
                  <table className="min-w-full text-sm">
                    <thead className="bg-gold/[0.08] text-left text-foreground">
                      <tr>
                        <th className="px-4 py-3 font-semibold">Planet</th>
                        <th className="px-4 py-3 font-semibold">Sign</th>
                        <th className="px-4 py-3 font-semibold">House</th>
                        <th className="px-4 py-3 font-semibold">Status</th>
                      </tr>
                    </thead>
                    <tbody>
                      {data.planet_positions.map((item, index) => (
                        <tr key={item.planet} className={index % 2 === 0 ? 'bg-gold/[0.02]' : 'bg-background'}>
                          <td className="px-4 py-3 text-foreground">{item.planet}</td>
                          <td className="px-4 py-3 text-muted-foreground">{item.sign_vedic || item.sign}</td>
                          <td className="px-4 py-3 text-muted-foreground">{item.house || '--'}</td>
                          <td className="px-4 py-3 text-muted-foreground">{item.status}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </section>
            </div>

            <div className="mt-8 grid gap-8 lg:grid-cols-[1fr_1fr]">
              <section className="rounded-2xl border border-gold/20 bg-background/80 p-6 shadow-sm">
                <h2 className="text-xl font-semibold text-foreground">Dasha Timeline</h2>
                <div className="mt-5 grid gap-3">
                  {data.dasha_timeline.slice(0, 9).map((item) => (
                    <div key={`${item.planet}-${item.start}`} className="rounded-xl border border-gold/15 bg-gold/[0.03] p-4">
                      <div className="flex items-center justify-between gap-4">
                        <p className="font-semibold text-foreground">{item.planet} Mahadasha</p>
                        <p className="text-xs text-muted-foreground">{item.years} years</p>
                      </div>
                      <p className="mt-2 text-sm text-muted-foreground">
                        {item.start} to {item.end}
                      </p>
                    </div>
                  ))}
                </div>
              </section>

              <section className="rounded-2xl border border-gold/20 bg-background/80 p-6 shadow-sm">
                <h2 className="text-xl font-semibold text-foreground">Notable Yogas</h2>
                <div className="mt-5 grid gap-3">
                  {data.notable_yogas.map((item) => (
                    <div key={item.name} className="rounded-xl border border-gold/15 bg-gold/[0.03] p-4">
                      <p className="font-semibold text-foreground">{item.name}</p>
                      <p className="mt-2 text-sm leading-6 text-muted-foreground">{item.detail}</p>
                    </div>
                  ))}
                </div>
              </section>
            </div>

            <section className="mt-8 rounded-2xl border border-gold/20 bg-gold/[0.05] p-6 shadow-sm">
              <p className="text-sm leading-6 text-muted-foreground">{data.interpretation_note}</p>
            </section>

            <section className="mt-8 rounded-2xl border border-gold/20 bg-background/80 p-8 text-center shadow-sm">
              <h2 className="text-2xl font-playfair font-bold text-foreground">Get your own birth chart</h2>
              <p className="mt-3 text-sm leading-6 text-muted-foreground">
                Public celebrity charts are interesting for comparison, but your own chart gives the timing and guidance that actually applies to your life.
              </p>
              <Link
                to="/birth-chart"
                className="mt-5 inline-flex items-center justify-center rounded-lg bg-gold px-5 py-3 text-sm font-semibold text-primary-foreground transition hover:bg-gold/90"
              >
                Generate My Birth Chart
              </Link>
            </section>
          </>
        )}
      </main>

      <Footer />
    </div>
  );
}
