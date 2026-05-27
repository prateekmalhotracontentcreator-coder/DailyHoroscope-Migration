import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { Link, useParams } from 'react-router-dom';
import { ArrowLeft, LoaderCircle } from 'lucide-react';
import { Footer } from '../../components/Footer';
import { SEO } from '../../components/SEO';
import { API, SITE, buildBreadcrumbSchema, buildCollectionSchema, titleCaseSlug } from './faithShared';
import { FaithGrowthPanel } from './FaithGrowthPanel';
import { FaithPathwayLinks } from './FaithPathwayLinks';

function buildSchema(data, signSlug) {
  if (!data) return null;
  return {
    '@context': 'https://schema.org',
    '@graph': [
      buildCollectionSchema({
        name: `${data.sign?.name || titleCaseSlug(signSlug)} spiritual guides`,
        description: data.hero_body,
        url: `${SITE}/faith/daily/${signSlug}`,
        items: (data.months || []).map((item) => ({ name: `${data.sign?.name || titleCaseSlug(signSlug)} - ${item.month_name}`, url: `${SITE}${item.href}` })),
      }),
      buildBreadcrumbSchema([
        { name: 'Home', url: SITE },
        { name: 'Faith Hubs', url: `${SITE}/faith` },
        { name: 'Daily', url: `${SITE}/faith/daily` },
        { name: data.sign?.name || titleCaseSlug(signSlug), url: `${SITE}/faith/daily/${signSlug}` },
      ]),
    ],
  };
}

export function FaithDailySignPage() {
  const { sign = '' } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let ignore = false;

    async function fetchHub() {
      try {
        setLoading(true);
        setError('');
        const response = await axios.get(`${API}/daily/sign/${sign}`);
        if (!ignore) setData(response.data);
      } catch (err) {
        if (!ignore) {
          setData(null);
          setError(err?.response?.status === 404 ? 'Faith sign hub not found.' : 'Unable to load this sign hub right now.');
        }
      } finally {
        if (!ignore) setLoading(false);
      }
    }

    fetchHub();
    return () => {
      ignore = true;
    };
  }, [sign]);

  const schema = useMemo(() => buildSchema(data, sign), [data, sign]);

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,rgba(144,202,249,0.14),transparent_28%),linear-gradient(180deg,#0f1116_0%,#151b22_42%,#1d2530_100%)] text-stone-100">
      <SEO
        title={data?.meta_title || `${titleCaseSlug(sign)} Spiritual Guides`}
        description={data?.meta_description || `Monthly spiritual guides for ${titleCaseSlug(sign)}.`}
        url={`${SITE}/faith/daily/${sign}`}
        schema={schema}
        noindex={!loading && !!error && !data}
      />

      <main className="mx-auto max-w-6xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="mb-6 flex items-center gap-2 text-sm text-stone-400">
          <Link to="/faith" className="transition hover:text-sky-300">Faith Hubs</Link>
          <span>/</span>
          <Link to="/faith/daily" className="transition hover:text-sky-300">Daily</Link>
          <span>/</span>
          <span className="text-stone-200">{data?.sign?.name || titleCaseSlug(sign)}</span>
        </div>

        <Link to="/faith/daily" className="mb-6 inline-flex items-center text-sm font-medium text-stone-400 transition hover:text-sky-300">
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to daily hub
        </Link>

        {loading ? (
          <div className="flex items-center justify-center rounded-[2rem] border border-sky-300/20 bg-white/[0.05] p-10 text-stone-300">
            <LoaderCircle className="mr-3 h-5 w-5 animate-spin text-sky-200" />
            Loading sign guide...
          </div>
        ) : error ? (
          <div className="rounded-[2rem] border border-red-400/25 bg-red-500/10 p-6 text-sm text-red-200">{error}</div>
        ) : data ? (
          <>
            <section className="rounded-[2rem] border border-sky-300/20 bg-white/[0.05] p-8 shadow-[0_24px_80px_rgba(0,0,0,0.28)] backdrop-blur">
              <span className="rounded-full border border-sky-300/20 bg-sky-400/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-sky-200">
                {data.sign.element} • {data.sign.ruler}
              </span>
              <h1 className="mt-5 font-cinzel text-4xl font-semibold text-stone-50 sm:text-5xl">{data.hero_title}</h1>
              <p className="mt-5 max-w-3xl text-base leading-8 text-stone-300">{data.hero_body}</p>
            </section>

            <section className="mt-8 grid gap-5 md:grid-cols-2 xl:grid-cols-3">
              {(data.months || []).map((item) => (
                <Link
                  key={item.month_slug}
                  to={item.href}
                  className="group rounded-[1.7rem] border border-sky-300/18 bg-white/[0.05] p-6 shadow-sm transition-all hover:-translate-y-1 hover:border-sky-300/35 hover:bg-white/[0.08]"
                >
                  <p className="text-xs font-semibold uppercase tracking-[0.18em] text-sky-200">{item.month_name}</p>
                  <h2 className="mt-4 font-cinzel text-2xl font-semibold text-stone-50">{data.sign.name} - {item.month_name}</h2>
                  <p className="mt-4 text-sm leading-7 text-stone-300">{item.summary}</p>
                  <p className="mt-5 text-sm font-semibold text-sky-200">Open guide</p>
                </Link>
              ))}
            </section>

            <FaithPathwayLinks
              theme="sky"
              title="Prefer a concern-first reading path?"
              body="Guided pathways help readers jump into the Faith graph by life issue first, then branch into daily, transit, Bible, and Gita pages from there."
            />

            <FaithGrowthPanel
              theme="sky"
              sourceTag={`faith-daily-sign-${sign}`}
              title="Turn this sign hub into a devotional habit loop"
              body="Join the Faith updates list if you want sign-based devotional sequences, monthly reading plans, and follow-up scripture journeys matched to this kind of rhythm."
            />
          </>
        ) : null}
      </main>

      <Footer />
    </div>
  );
}
