import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { ArrowRight, BookHeart, LoaderCircle, Orbit, Sparkles, SunMoon } from 'lucide-react';
import { Footer } from '../../components/Footer';
import { SEO } from '../../components/SEO';
import { API, SITE, buildBreadcrumbSchema, buildCollectionSchema } from './faithShared';
import { FEATURED_FAITH_COLLECTIONS } from './faithCollections';
import { FaithGrowthPanel } from './FaithGrowthPanel';

const ICONS = {
  transit: Orbit,
  daily: SunMoon,
  gita: BookHeart,
  bible: Sparkles,
};

function buildSchema(data) {
  if (!data) return null;
  return {
    '@context': 'https://schema.org',
    '@graph': [
      buildCollectionSchema({
        name: 'Faith Hubs',
        description: data.hero_body,
        url: `${SITE}/faith`,
        items: (data.collections || []).map((item) => ({ name: item.title, url: `${SITE}${item.href}` })),
      }),
      buildBreadcrumbSchema([
        { name: 'Home', url: SITE },
        { name: 'Faith Hubs', url: `${SITE}/faith` },
      ]),
    ],
  };
}

export function FaithHubPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let ignore = false;

    async function fetchHub() {
      try {
        setLoading(true);
        setError('');
        const response = await axios.get(`${API}/hub`);
        if (!ignore) setData(response.data);
      } catch {
        if (!ignore) {
          setData(null);
          setError('Unable to load Faith Hubs right now.');
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
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,rgba(212,175,55,0.18),transparent_28%),linear-gradient(180deg,#0d1015_0%,#141a22_42%,#1f2731_100%)] text-stone-100">
      <SEO
        title={data?.meta_title || 'Faith Hubs'}
        description={data?.meta_description || 'Scripture hubs for daily practice and transit guidance.'}
        url={`${SITE}/faith`}
        schema={schema}
      />

      <main className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <section className="relative overflow-hidden rounded-[2rem] border border-[#d4af37]/20 bg-white/[0.05] p-8 shadow-[0_24px_80px_rgba(0,0,0,0.28)] backdrop-blur md:p-10">
          <div className="absolute -right-10 top-0 h-56 w-56 rounded-full bg-[#d4af37]/10 blur-3xl" />
          <div className="relative max-w-3xl">
            <div className="inline-flex items-center gap-2 rounded-full border border-[#d4af37]/25 bg-[#d4af37]/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.24em] text-[#f3d27a]">
              <Sparkles className="h-3.5 w-3.5" />
              Faith and Scripture
            </div>
            <h1 className="mt-5 font-cinzel text-4xl font-semibold leading-tight text-stone-50 sm:text-5xl">
              {data?.hero_title || 'Faith Hubs for Daily Practice and Transit Wisdom'}
            </h1>
            <p className="mt-5 max-w-2xl text-base leading-8 text-stone-300">
              {data?.hero_body || 'Explore scripture-led hubs shaped around daily practice, spiritual timing, and grounded life application.'}
            </p>
            <div className="mt-8 flex flex-wrap gap-3 text-sm text-stone-300">
              <span className="rounded-full border border-[#d4af37]/20 bg-white/[0.04] px-4 py-2">
                {data?.counts?.phase_total || 300} published pages
              </span>
              <span className="rounded-full border border-[#d4af37]/20 bg-white/[0.04] px-4 py-2">
                {data?.counts?.transit_pages || 156} transit pages
              </span>
              <span className="rounded-full border border-[#d4af37]/20 bg-white/[0.04] px-4 py-2">
                {data?.counts?.daily_pages || 144} evergreen daily guides
              </span>
              <span className="rounded-full border border-[#d4af37]/20 bg-white/[0.04] px-4 py-2">
                {data?.counts?.gita_pages || 10500} Gita situation pages
              </span>
            </div>
          </div>
        </section>

        <section className="mt-8">
          {loading ? (
            <div className="flex items-center justify-center rounded-[2rem] border border-[#d4af37]/20 bg-white/[0.05] p-10 text-stone-300">
              <LoaderCircle className="mr-3 h-5 w-5 animate-spin text-[#f3d27a]" />
              Loading Faith Hubs...
            </div>
          ) : error ? (
            <div className="rounded-[2rem] border border-red-400/25 bg-red-500/10 p-6 text-sm text-red-200">{error}</div>
          ) : (
            <div className="grid gap-5 lg:grid-cols-2">
              {(data?.collections || []).map((item) => {
                const Icon = ICONS[item.slug] || Sparkles;
                return (
                  <Link
                    key={item.slug}
                    to={item.href}
                    className="group rounded-[1.8rem] border border-[#d4af37]/18 bg-white/[0.05] p-7 shadow-sm transition-all hover:-translate-y-1 hover:border-[#d4af37]/35 hover:bg-white/[0.08]"
                  >
                    <div className="flex items-start justify-between gap-4">
                      <div className="inline-flex rounded-2xl border border-[#d4af37]/20 bg-[#d4af37]/10 p-3 text-[#f3d27a]">
                        <Icon className="h-6 w-6" />
                      </div>
                      <span className="rounded-full border border-[#d4af37]/20 bg-white/[0.04] px-3 py-1 text-xs font-semibold uppercase tracking-[0.18em] text-[#f3d27a]">
                        {item.count_label}
                      </span>
                    </div>
                    <h2 className="mt-5 font-cinzel text-3xl font-semibold text-stone-50">{item.title}</h2>
                    <p className="mt-4 text-sm leading-7 text-stone-300">{item.description}</p>
                    <div className="mt-6 inline-flex items-center text-sm font-semibold text-[#f3d27a]">
                      Enter hub
                      <ArrowRight className="ml-2 h-4 w-4 transition group-hover:translate-x-1" />
                    </div>
                  </Link>
                );
              })}
            </div>
          )}
        </section>

        {!loading && data ? (
          <section className="mt-10 grid gap-6 lg:grid-cols-[1.05fr_0.95fr]">
            <article className="rounded-[1.9rem] border border-[#d4af37]/18 bg-white/[0.05] p-7">
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[#f3d27a]">Transit preview</p>
              <h2 className="mt-3 font-playfair text-2xl font-semibold text-stone-50">First published transit themes</h2>
              <div className="mt-6 grid gap-3 sm:grid-cols-2">
                {(data.featured_transits || []).map((item) => (
                  <Link
                    key={item.slug}
                    to={`/faith/transit/${item.slug}/gita`}
                    className="rounded-[1.35rem] border border-[#d4af37]/16 bg-white/[0.04] px-4 py-4 text-sm text-stone-200 transition hover:border-[#d4af37]/35 hover:bg-white/[0.07]"
                  >
                    <p className="font-semibold text-stone-50">{item.label}</p>
                    <p className="mt-2 text-xs uppercase tracking-[0.18em] text-[#f3d27a]">Open Gita guidance</p>
                  </Link>
                ))}
              </div>
            </article>

            <article className="rounded-[1.9rem] border border-[#d4af37]/18 bg-white/[0.05] p-7">
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[#f3d27a]">Sign entry points</p>
              <h2 className="mt-3 font-playfair text-2xl font-semibold text-stone-50">Evergreen daily guides by sign</h2>
              <div className="mt-6 grid gap-3 sm:grid-cols-2">
                {(data.featured_signs || []).map((item) => (
                  <Link
                    key={item.slug}
                    to={`/faith/daily/${item.slug}`}
                    className="rounded-[1.35rem] border border-[#d4af37]/16 bg-white/[0.04] px-4 py-4 text-sm text-stone-200 transition hover:border-[#d4af37]/35 hover:bg-white/[0.07]"
                  >
                    <p className="font-semibold text-stone-50">{item.name}</p>
                    <p className="mt-2 text-xs uppercase tracking-[0.18em] text-[#f3d27a]">{item.element} • {item.ruler}</p>
                  </Link>
                ))}
              </div>
            </article>
          </section>
        ) : null}

        <section className="mt-8 rounded-[1.9rem] border border-[#d4af37]/18 bg-white/[0.05] p-7">
          <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[#f3d27a]">Guided pathways</p>
              <h2 className="mt-2 font-playfair text-2xl font-semibold text-stone-50">Start from the concern if the full library feels too broad.</h2>
            </div>
            <Link to="/faith/pathways" className="inline-flex items-center rounded-full border border-[#d4af37]/20 bg-white/[0.04] px-5 py-3 text-sm font-semibold text-stone-100 transition hover:border-[#d4af37]/35 hover:bg-white/[0.07]">
              Browse pathways
              <ArrowRight className="ml-2 h-4 w-4" />
            </Link>
          </div>
          <div className="mt-6 grid gap-4 md:grid-cols-3">
            {FEATURED_FAITH_COLLECTIONS.map((item) => (
              <Link
                key={item.slug}
                to={`/faith/pathways/${item.slug}`}
                className="rounded-[1.35rem] border border-[#d4af37]/16 bg-white/[0.04] px-5 py-5 transition hover:border-[#d4af37]/35 hover:bg-white/[0.07]"
              >
                <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[#f3d27a]">{item.eyebrow}</p>
                <p className="mt-3 font-semibold text-stone-100">{item.title}</p>
                <p className="mt-3 text-sm leading-7 text-stone-300">{item.description}</p>
              </Link>
            ))}
          </div>
        </section>

        <FaithGrowthPanel
          theme="gold"
          sourceTag="faith-hub"
          title="Help us build the next devotional engine"
          body="We are now layering pathways, email journeys, and devotional products on top of the Faith library. Join the Faith updates list and tell us which concern should shape the next sequence."
        />
      </main>

      <Footer />
    </div>
  );
}
