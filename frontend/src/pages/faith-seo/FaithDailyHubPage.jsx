import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { ArrowLeft, CalendarDays, LoaderCircle, Sparkles } from 'lucide-react';
import { Footer } from '../../components/Footer';
import { SEO } from '../../components/SEO';
import { API, SITE, buildBreadcrumbSchema, buildCollectionSchema } from './faithShared';
import { FaithGrowthPanel } from './FaithGrowthPanel';
import { FaithPathwayLinks } from './FaithPathwayLinks';

function buildSchema(data) {
  if (!data) return null;
  return {
    '@context': 'https://schema.org',
    '@graph': [
      buildCollectionSchema({
        name: 'Faith Daily Hub',
        description: data.hero_body,
        url: `${SITE}/faith/daily`,
        items: (data.signs || []).map((item) => ({ name: item.name, url: `${SITE}/faith/daily/${item.slug}` })),
      }),
      buildBreadcrumbSchema([
        { name: 'Home', url: SITE },
        { name: 'Faith Hubs', url: `${SITE}/faith` },
        { name: 'Daily', url: `${SITE}/faith/daily` },
      ]),
    ],
  };
}

export function FaithDailyHubPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let ignore = false;

    async function fetchHub() {
      try {
        setLoading(true);
        setError('');
        const response = await axios.get(`${API}/daily/hub`);
        if (!ignore) setData(response.data);
      } catch {
        if (!ignore) {
          setData(null);
          setError('Unable to load the daily scripture hub right now.');
        }
      } finally {
        if (!ignore) setLoading(false);
      }
    }

    fetchHub();
    return () => {
      ignore = true;
    };
  }, []);

  const schema = useMemo(() => buildSchema(data), [data]);

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,rgba(144,202,249,0.14),transparent_28%),linear-gradient(180deg,#0f1116_0%,#151b22_42%,#1d2530_100%)] text-stone-100">
      <SEO
        title={data?.meta_title || 'Faith Daily Hub'}
        description={data?.meta_description || 'Evergreen daily scripture by sign and month.'}
        url={`${SITE}/faith/daily`}
        schema={schema}
      />

      <main className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="mb-6 flex items-center gap-2 text-sm text-stone-400">
          <Link to="/faith" className="transition hover:text-sky-300">Faith Hubs</Link>
          <span>/</span>
          <span className="text-stone-200">Daily</span>
        </div>

        <Link to="/faith" className="mb-6 inline-flex items-center text-sm font-medium text-stone-400 transition hover:text-sky-300">
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Faith Hubs
        </Link>

        <section className="rounded-[2rem] border border-sky-300/20 bg-white/[0.05] p-8 shadow-[0_24px_80px_rgba(0,0,0,0.28)] backdrop-blur">
          <div className="inline-flex items-center gap-2 rounded-full border border-sky-300/25 bg-sky-400/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.24em] text-sky-200">
            <CalendarDays className="h-3.5 w-3.5" />
            Evergreen Daily Guides
          </div>
          <h1 className="mt-5 font-cinzel text-4xl font-semibold leading-tight text-stone-50 sm:text-5xl">
            {data?.hero_title || 'Daily Scripture by Sign and Month'}
          </h1>
          <p className="mt-5 max-w-3xl text-base leading-8 text-stone-300">
            {data?.hero_body || 'Browse evergreen spiritual guides built around sign energy and monthly practice.'}
          </p>
        </section>

        {!loading && data ? (
          <section className="mt-8 rounded-[1.9rem] border border-sky-300/18 bg-white/[0.05] p-7">
            <p className="text-xs font-semibold uppercase tracking-[0.24em] text-sky-200">Month layer</p>
            <div className="mt-5 flex flex-wrap gap-2">
              {(data.months || []).map((item) => (
                <span key={item.slug} className="rounded-full border border-sky-300/16 bg-white/[0.04] px-4 py-2 text-sm text-stone-200">
                  {item.name}
                </span>
              ))}
            </div>
          </section>
        ) : null}

        <section className="mt-8">
          {loading ? (
            <div className="flex items-center justify-center rounded-[2rem] border border-sky-300/20 bg-white/[0.05] p-10 text-stone-300">
              <LoaderCircle className="mr-3 h-5 w-5 animate-spin text-sky-200" />
              Loading daily guides...
            </div>
          ) : error ? (
            <div className="rounded-[2rem] border border-red-400/25 bg-red-500/10 p-6 text-sm text-red-200">{error}</div>
          ) : (
            <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
              {(data?.signs || []).map((item) => (
                <Link
                  key={item.slug}
                  to={`/faith/daily/${item.slug}`}
                  className="group rounded-[1.7rem] border border-sky-300/18 bg-white/[0.05] p-6 shadow-sm transition-all hover:-translate-y-1 hover:border-sky-300/35 hover:bg-white/[0.08]"
                >
                  <div className="inline-flex rounded-2xl border border-sky-300/18 bg-sky-400/10 p-3 text-sky-200">
                    <Sparkles className="h-5 w-5" />
                  </div>
                  <h2 className="mt-5 font-cinzel text-2xl font-semibold text-stone-50">{item.name}</h2>
                  <p className="mt-3 text-sm leading-7 text-stone-300">
                    {item.element} sign ruled by {item.ruler}. Browse all 12 month guides for this sign's spiritual rhythm.
                  </p>
                  <p className="mt-5 text-sm font-semibold text-sky-200">Open monthly guide index</p>
                </Link>
              ))}
            </div>
          )}
        </section>

        {!loading && !error && data ? (
          <FaithPathwayLinks
            theme="sky"
            title="Turn daily browsing into a more intentional faith routine"
            body="If monthly sign pages feel too broad, start with a guided pathway that narrows the concern and links you into the most relevant daily, transit, Bible, and Gita pages."
          />
        ) : null}

        <FaithGrowthPanel
          theme="sky"
          sourceTag="faith-daily-hub"
          title="Turn daily pages into a repeat-visit devotional habit"
          body="Join the Faith updates list if you want sign-based monthly devotionals, guided daily sequences, and follow-up scripture plans."
        />
      </main>

      <Footer />
    </div>
  );
}
