import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { ArrowLeft, LoaderCircle, Sparkles } from 'lucide-react';
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
        name: data.hero_title,
        description: data.hero_body,
        url: `${SITE}/faith/bible`,
        items: (data.topics || []).map((item) => ({ name: item.label, url: `${SITE}${item.href}` })),
      }),
      buildBreadcrumbSchema([
        { name: 'Home', url: SITE },
        { name: 'Faith Hubs', url: `${SITE}/faith` },
        { name: 'Bible', url: `${SITE}/faith/bible` },
      ]),
    ],
  };
}

export function FaithBibleHubPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let ignore = false;

    async function fetchHub() {
      try {
        setLoading(true);
        setError('');
        const response = await axios.get(`${API}/bible/hub`);
        if (!ignore) setData(response.data);
      } catch {
        if (!ignore) {
          setData(null);
          setError('Unable to load the Bible hub right now.');
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
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,rgba(167,243,208,0.12),transparent_28%),linear-gradient(180deg,#0f1116_0%,#151b22_42%,#1d2530_100%)] text-stone-100">
      <SEO
        title={data?.meta_title || 'Bible Promise Library'}
        description={data?.meta_description || 'Bible promise library for Faith Hubs.'}
        url={`${SITE}/faith/bible`}
        schema={schema}
      />

      <main className="mx-auto max-w-6xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="mb-6 flex items-center gap-2 text-sm text-stone-400">
          <Link to="/faith" className="transition hover:text-emerald-300">Faith Hubs</Link>
          <span>/</span>
          <span className="text-stone-200">Bible</span>
        </div>

        <Link to="/faith" className="mb-6 inline-flex items-center text-sm font-medium text-stone-400 transition hover:text-emerald-300">
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Faith Hubs
        </Link>

        {loading ? (
          <div className="flex items-center justify-center rounded-[2rem] border border-emerald-300/20 bg-white/[0.05] p-12 text-stone-300">
            <LoaderCircle className="mr-3 h-5 w-5 animate-spin text-emerald-200" />
            Loading Bible library...
          </div>
        ) : error ? (
          <div className="rounded-[2rem] border border-red-400/25 bg-red-500/10 p-6 text-sm text-red-200">{error}</div>
        ) : data ? (
          <>
            <section className="rounded-[2rem] border border-emerald-300/20 bg-white/[0.05] p-8 shadow-[0_24px_80px_rgba(0,0,0,0.28)] backdrop-blur">
              <div className="flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
                <div className="max-w-3xl">
                  <div className="inline-flex items-center gap-2 rounded-full border border-emerald-300/25 bg-emerald-400/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.24em] text-emerald-200">
                    <Sparkles className="h-3.5 w-3.5" />
                    Phase 3 Live
                  </div>
                  <h1 className="mt-5 font-cinzel text-4xl font-semibold leading-tight text-stone-50 sm:text-5xl">{data.hero_title}</h1>
                  <p className="mt-5 max-w-3xl text-base leading-8 text-stone-300">{data.hero_body}</p>
                  <p className="mt-6 rounded-[1.2rem] border border-emerald-300/16 bg-white/[0.04] px-5 py-4 text-sm leading-7 text-stone-300">{data.phase_note}</p>
                </div>
                <div className="grid gap-3 sm:grid-cols-3">
                  <div className="rounded-[1.4rem] border border-emerald-300/18 bg-white/[0.04] px-5 py-4 text-sm">
                    <p className="text-xs font-semibold uppercase tracking-[0.18em] text-emerald-200">Pages</p>
                    <p className="mt-2 font-semibold text-stone-50">{data.counts?.pages}</p>
                  </div>
                  <div className="rounded-[1.4rem] border border-emerald-300/18 bg-white/[0.04] px-5 py-4 text-sm">
                    <p className="text-xs font-semibold uppercase tracking-[0.18em] text-emerald-200">Topics</p>
                    <p className="mt-2 font-semibold text-stone-50">{data.counts?.topics}</p>
                  </div>
                  <div className="rounded-[1.4rem] border border-emerald-300/18 bg-white/[0.04] px-5 py-4 text-sm">
                    <p className="text-xs font-semibold uppercase tracking-[0.18em] text-emerald-200">Transitions</p>
                    <p className="mt-2 font-semibold text-stone-50">{data.counts?.transitions}</p>
                  </div>
                </div>
              </div>
            </section>

            <section className="mt-8 rounded-[1.8rem] border border-emerald-300/18 bg-white/[0.05] p-7">
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-emerald-200">Transition index</p>
              <div className="mt-5 flex flex-wrap gap-3">
                {(data.transition_index || []).slice(0, 25).map((item) => (
                  <span key={item.slug} className="rounded-full border border-emerald-300/16 bg-white/[0.04] px-4 py-2 text-sm text-stone-200">
                    {item.label}
                  </span>
                ))}
              </div>
            </section>

            <section className="mt-8 grid gap-5 md:grid-cols-2 xl:grid-cols-3">
              {(data.featured_topics || []).map((item) => (
                <article key={item.slug} className="rounded-[1.7rem] border border-emerald-300/18 bg-white/[0.05] p-6">
                  <p className="text-xs font-semibold uppercase tracking-[0.18em] text-emerald-200">{item.label}</p>
                  <p className="mt-4 text-sm font-semibold text-stone-50">{item.reference}</p>
                  <p className="mt-3 font-playfair text-xl text-stone-100">{item.text}</p>
                  <Link to={item.href} className="mt-5 inline-flex rounded-full border border-emerald-300/18 bg-white/[0.04] px-4 py-2 text-sm font-semibold text-stone-100 transition hover:border-emerald-300/35 hover:bg-white/[0.07]">
                    Open topic hub
                  </Link>
                </article>
              ))}
            </section>

            <section className="mt-8 grid gap-5 md:grid-cols-2 xl:grid-cols-4">
              {(data.topics || []).slice(0, 24).map((item) => (
                <article key={item.slug} className="rounded-[1.6rem] border border-emerald-300/18 bg-white/[0.05] p-5">
                  <p className="font-semibold text-stone-50">{item.label}</p>
                  <div className="mt-4 flex gap-3">
                    <Link to={item.href} className="inline-flex rounded-full bg-emerald-300 px-4 py-2 text-sm font-semibold text-slate-950 transition hover:opacity-90">
                      Topic hub
                    </Link>
                    <Link to={item.sample_href} className="inline-flex rounded-full border border-emerald-300/18 bg-white/[0.04] px-4 py-2 text-sm font-semibold text-stone-100 transition hover:border-emerald-300/35 hover:bg-white/[0.07]">
                      Sample page
                    </Link>
                  </div>
                </article>
              ))}
            </section>

            <FaithPathwayLinks
              theme="emerald"
              title="Start with a guided pathway if the topic library feels too wide"
              body="Pathways turn the Bible topic graph into smaller journeys built around anxiety, money pressure, illness, parenting strain, and other immediate concerns."
            />

            <FaithGrowthPanel
              theme="emerald"
              sourceTag="faith-bible-hub"
              title="Help us build the next Bible devotional sequences"
              body="Join the Faith updates list if you want topic-based Bible journeys, crisis collections, and more guided promise paths."
            />
          </>
        ) : null}
      </main>

      <Footer />
    </div>
  );
}
