import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { Compass, LoaderCircle, MapPinned, Sparkles, Stars, SunMedium } from 'lucide-react';
import { Footer } from '../../components/Footer';
import { SEO } from '../../components/SEO';
import { API, CALCULATOR_FAQS, SITE, buildBreadcrumbSchema, buildFaqSchema } from './crystalShared';
import { CrystalFaqs, CrystalPageFrame, CrystalSection } from './CrystalUi';

export function CrystalCalculatorPage() {
  const [catalog, setCatalog] = useState(null);
  const [loadingCatalog, setLoadingCatalog] = useState(true);
  const [form, setForm] = useState({
    date: '',
    time: '12:00',
    place: 'New Delhi',
    intention: 'clarity-focus',
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    let ignore = false;
    async function fetchCatalog() {
      try {
        setLoadingCatalog(true);
        const response = await axios.get(`${API}/list`);
        if (!ignore) {
          setCatalog(response.data);
        }
      } catch (err) {
        if (!ignore) {
          setError(err?.response?.data?.detail || 'Unable to load calculator options right now.');
        }
      } finally {
        if (!ignore) {
          setLoadingCatalog(false);
        }
      }
    }

    fetchCatalog();
    return () => {
      ignore = true;
    };
  }, []);

  async function handleSubmit(event) {
    event.preventDefault();
    setLoading(true);
    setError('');
    try {
      const response = await axios.post(`${API}/calculator`, form);
      setResult(response.data);
    } catch (err) {
      setResult(null);
      setError(err?.response?.data?.detail || 'Unable to calculate your crystal recommendation right now.');
    } finally {
      setLoading(false);
    }
  }

  const schema = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'WebApplication',
        applicationCategory: 'LifestyleApplication',
        name: 'Crystal Calculator',
        description: 'Birth-chart crystal recommendation calculator powered by Vedic chart data and intention overlays.',
        url: `${SITE}/crystals/calculator`,
      },
      buildFaqSchema(CALCULATOR_FAQS),
      buildBreadcrumbSchema([
        { name: 'Home', url: SITE },
        { name: 'Crystals', url: `${SITE}/crystals` },
        { name: 'Calculator', url: `${SITE}/crystals/calculator` },
      ]),
    ],
  };

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,_rgba(197,160,89,0.16),_transparent_30%),linear-gradient(180deg,_#fffdf8_0%,_#f6efe2_42%,_#fffaf2_100%)]">
      <SEO
        title="Crystal Calculator - Your Personal Recommendation from Your Birth Chart"
        description="Get a primary Vedic gemstone and support crystals based on your birth chart, active dasha, and current intention."
        canonical={`${SITE}/crystals/calculator`}
        jsonLd={schema}
      />

      <CrystalPageFrame
        eyebrow="Personal Calculator"
        title="Crystal Calculator - Your Personal Recommendation from Your Birth Chart"
        description="Use your birth details and a current life intention to generate one primary Vedic gemstone plus softer support crystals. This tool blends active dasha themes with practical intention overlays so the recommendation feels more personal than a general crystal list."
      >
        <div className="grid gap-6 lg:grid-cols-[0.95fr_1.05fr]">
          <CrystalSection title="Enter Your Birth Details">
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid gap-4 md:grid-cols-2">
                <label className="block">
                  <span className="text-sm font-medium text-stone-700">Date of birth</span>
                  <input
                    type="date"
                    required
                    value={form.date}
                    onChange={(event) => setForm((current) => ({ ...current, date: event.target.value }))}
                    className="mt-2 w-full rounded-xl border border-gold/20 bg-white px-4 py-3 text-sm text-stone-700 outline-none transition focus:border-gold/50"
                  />
                </label>
                <label className="block">
                  <span className="text-sm font-medium text-stone-700">Birth time</span>
                  <input
                    type="time"
                    required
                    value={form.time}
                    onChange={(event) => setForm((current) => ({ ...current, time: event.target.value }))}
                    className="mt-2 w-full rounded-xl border border-gold/20 bg-white px-4 py-3 text-sm text-stone-700 outline-none transition focus:border-gold/50"
                  />
                </label>
              </div>

              <label className="block">
                <span className="text-sm font-medium text-stone-700">Birth place or lat,lon</span>
                <div className="relative mt-2">
                  <MapPinned className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-stone-400" />
                  <input
                    type="text"
                    required
                    value={form.place}
                    onChange={(event) => setForm((current) => ({ ...current, place: event.target.value }))}
                    placeholder="New Delhi or 28.6139,77.2090"
                    className="w-full rounded-xl border border-gold/20 bg-white px-10 py-3 text-sm text-stone-700 outline-none transition focus:border-gold/50"
                  />
                </div>
              </label>

              <label className="block">
                <span className="text-sm font-medium text-stone-700">Current intention</span>
                <select
                  value={form.intention}
                  onChange={(event) => setForm((current) => ({ ...current, intention: event.target.value }))}
                  className="mt-2 w-full rounded-xl border border-gold/20 bg-white px-4 py-3 text-sm text-stone-700 outline-none transition focus:border-gold/50"
                >
                  {(catalog?.intentions || []).map((item) => (
                    <option key={item.slug} value={item.slug}>{item.display}</option>
                  ))}
                </select>
              </label>

              <button
                type="submit"
                disabled={loading || loadingCatalog}
                className="inline-flex items-center gap-2 rounded-full border border-gold/30 bg-gold/15 px-5 py-3 text-sm font-semibold text-stone-900 transition hover:bg-gold/25 disabled:cursor-not-allowed disabled:opacity-60"
              >
                {loading ? <LoaderCircle className="h-4 w-4 animate-spin" /> : <Compass className="h-4 w-4" />}
                Get recommendation
              </button>
            </form>

            <div className="mt-6 space-y-3 text-sm leading-7 text-stone-600">
              <p>This calculator is strongest when the birth time is accurate. If your time is approximate, the result can still be useful as a soft directional recommendation rather than a strict prescription.</p>
              <p>The intention overlay is there to make the result feel practical now, not just astrologically correct in theory.</p>
            </div>
          </CrystalSection>

          <CrystalSection title="Your Result">
            {loadingCatalog ? (
              <div className="flex items-center justify-center rounded-2xl border border-gold/15 bg-white/70 p-12 text-stone-500">
                <LoaderCircle className="mr-3 h-5 w-5 animate-spin text-gold" />
                Loading calculator options...
              </div>
            ) : error ? (
              <div className="rounded-2xl border border-red-300/40 bg-red-50 p-6 text-sm text-red-700">{error}</div>
            ) : !result ? (
              <div className="rounded-2xl border border-dashed border-gold/20 bg-white/60 p-8 text-sm leading-7 text-stone-600">
                <p>Enter your details to receive a primary Vedic gemstone, a smaller support set of healing crystals, and a practical placement tip.</p>
              </div>
            ) : (
              <div className="space-y-5">
                <div className="rounded-2xl border border-gold/30 bg-gold/10 p-6">
                  <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.24em] text-gold/80">
                    <SunMedium className="h-4 w-4" />
                    Primary Vedic Gemstone
                  </div>
                  <h2 className="mt-3 font-playfair text-3xl font-semibold text-stone-900">{result.primary_vedic.crystal}</h2>
                  <p className="mt-3 text-sm leading-7 text-stone-600">{result.primary_vedic.reason}</p>
                  <div className="mt-5 grid gap-3 md:grid-cols-2">
                    <div className="rounded-2xl border border-gold/20 bg-white/75 p-4 text-sm leading-7 text-stone-600">
                      <p><span className="font-semibold text-stone-900">Metal:</span> {result.primary_vedic.wearing?.metal || 'Varies'}</p>
                      <p><span className="font-semibold text-stone-900">Finger:</span> {result.primary_vedic.wearing?.finger || 'Varies'}</p>
                      <p><span className="font-semibold text-stone-900">Day:</span> {result.primary_vedic.wearing?.day || 'Varies'}</p>
                    </div>
                    <div className="rounded-2xl border border-gold/20 bg-white/75 p-4 text-sm leading-7 text-stone-600">
                      <p><span className="font-semibold text-stone-900">Mantra:</span> {result.primary_vedic.wearing?.mantra || 'Use intention and prayer with the stone.'}</p>
                    </div>
                  </div>
                  <Link to={`/crystals/${result.primary_vedic.slug}`} className="mt-5 inline-flex items-center gap-2 text-sm font-semibold text-stone-900 underline decoration-gold/70 underline-offset-4">
                    Learn more about {result.primary_vedic.crystal}
                  </Link>
                </div>

                <div className="grid gap-4 md:grid-cols-2">
                  {result.healing_recommendations?.map((item) => (
                    <div key={item.slug} className="rounded-2xl border border-sky-200/60 bg-sky-50/70 p-5">
                      <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.24em] text-sky-700">
                        <Stars className="h-4 w-4" />
                        Healing Support
                      </div>
                      <h3 className="mt-3 font-playfair text-2xl font-semibold text-stone-900">{item.crystal}</h3>
                      <p className="mt-3 text-sm leading-7 text-stone-600">{item.reason}</p>
                      <Link to={`/crystals/${item.slug}`} className="mt-4 inline-flex text-sm font-semibold text-stone-900 underline decoration-sky-400 underline-offset-4">
                        Read crystal page
                      </Link>
                    </div>
                  ))}
                </div>

                {result.intention_boosters?.length ? (
                  <div className="grid gap-4 md:grid-cols-2">
                    {result.intention_boosters.map((item) => (
                      <div key={item.slug} className="rounded-2xl border border-emerald-200/70 bg-emerald-50/80 p-5">
                        <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.24em] text-emerald-700">
                          <Sparkles className="h-4 w-4" />
                          Intention Booster
                        </div>
                        <h3 className="mt-3 font-playfair text-2xl font-semibold text-stone-900">{item.crystal}</h3>
                        <p className="mt-3 text-sm leading-7 text-stone-600">{item.reason}</p>
                        <Link to={`/crystals/${item.slug}`} className="mt-4 inline-flex text-sm font-semibold text-stone-900 underline decoration-emerald-400 underline-offset-4">
                          Read crystal page
                        </Link>
                      </div>
                    ))}
                  </div>
                ) : null}

                <div className="rounded-2xl border border-gold/20 bg-white/80 p-5 text-sm leading-7 text-stone-600">
                  <p><span className="font-semibold text-stone-900">Placement tip:</span> {result.placement_tip}</p>
                  <p className="mt-3"><span className="font-semibold text-stone-900">Chart context:</span> Lagna {result.chart_context?.lagna || 'Unknown'}, Moon sign {result.chart_context?.moon_sign || 'Unknown'}.</p>
                </div>
              </div>
            )}
          </CrystalSection>
        </div>

        <CrystalFaqs title="Crystal Calculator FAQs" items={CALCULATOR_FAQS} />
      </CrystalPageFrame>
      <Footer />
    </div>
  );
}

export default CrystalCalculatorPage;
