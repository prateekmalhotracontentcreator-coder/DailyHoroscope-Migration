import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { ArrowLeft, BookHeart, LoaderCircle, Sparkles } from 'lucide-react';
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
        url: `${SITE}/faith/gita`,
        items: (data.chapters || []).map((item) => ({ name: `Chapter ${item.chapter}`, url: `${SITE}${item.href}` })),
      }),
      buildBreadcrumbSchema([
        { name: 'Home', url: SITE },
        { name: 'Faith Hubs', url: `${SITE}/faith` },
        { name: 'Gita', url: `${SITE}/faith/gita` },
      ]),
    ],
  };
}

export function FaithGitaHubPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let ignore = false;

    async function fetchHub() {
      try {
        setLoading(true);
        setError('');
        const response = await axios.get(`${API}/gita/hub`);
        if (!ignore) setData(response.data);
      } catch {
        if (!ignore) {
          setData(null);
          setError('Unable to load the Gita hub right now.');
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
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,rgba(255,214,102,0.14),transparent_28%),linear-gradient(180deg,#0d1015_0%,#141a22_42%,#1f2731_100%)] text-stone-100">
      <SEO
        title={data?.meta_title || 'Bhagavad Gita Verse Library'}
        description={data?.meta_description || 'Live Bhagavad Gita verse hub for Faith Hubs.'}
        url={`${SITE}/faith/gita`}
        schema={schema}
      />

      <main className="mx-auto max-w-6xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="mb-6 flex items-center gap-2 text-sm text-stone-400">
          <Link to="/faith" className="transition hover:text-[#f3d27a]">Faith Hubs</Link>
          <span>/</span>
          <span className="text-stone-200">Gita</span>
        </div>

        <Link to="/faith" className="mb-6 inline-flex items-center text-sm font-medium text-stone-400 transition hover:text-[#f3d27a]">
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Faith Hubs
        </Link>

        {loading ? (
          <div className="flex items-center justify-center rounded-[2rem] border border-[#d4af37]/20 bg-white/[0.05] p-12 text-stone-300">
            <LoaderCircle className="mr-3 h-5 w-5 animate-spin text-[#f3d27a]" />
            Loading Gita library...
          </div>
        ) : error ? (
          <div className="rounded-[2rem] border border-red-400/25 bg-red-500/10 p-6 text-sm text-red-200">{error}</div>
        ) : data ? (
          <>
            <section className="rounded-[2rem] border border-[#d4af37]/20 bg-white/[0.05] p-8 shadow-[0_24px_80px_rgba(0,0,0,0.28)] backdrop-blur">
              <div className="flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
                <div className="max-w-3xl">
                  <div className="inline-flex items-center gap-2 rounded-full border border-[#d4af37]/25 bg-[#d4af37]/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.24em] text-[#f3d27a]">
                    <BookHeart className="h-3.5 w-3.5" />
                    Phase 2 Live
                  </div>
                  <h1 className="mt-5 font-cinzel text-4xl font-semibold leading-tight text-stone-50 sm:text-5xl">{data.hero_title}</h1>
                  <p className="mt-5 max-w-3xl text-base leading-8 text-stone-300">{data.hero_body}</p>
                  <p className="mt-6 rounded-[1.2rem] border border-[#d4af37]/16 bg-white/[0.04] px-5 py-4 text-sm leading-7 text-stone-300">{data.phase_note}</p>
                </div>
                <div className="grid gap-3 sm:grid-cols-2">
                  <div className="rounded-[1.4rem] border border-[#d4af37]/18 bg-white/[0.04] px-5 py-4 text-sm">
                    <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[#f3d27a]">Verse pages</p>
                    <p className="mt-2 font-semibold text-stone-50">{data.counts?.pages}</p>
                  </div>
                  <div className="rounded-[1.4rem] border border-[#d4af37]/18 bg-white/[0.04] px-5 py-4 text-sm">
                    <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[#f3d27a]">Chapters</p>
                    <p className="mt-2 font-semibold text-stone-50">{data.counts?.chapters}</p>
                  </div>
                </div>
              </div>
            </section>

            <section className="mt-8 rounded-[1.8rem] border border-[#d4af37]/18 bg-white/[0.05] p-7">
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[#f3d27a]">Situation paths</p>
              <div className="mt-5 flex flex-wrap gap-3">
                {(data.situations || []).map((item) => (
                  <span key={item.slug} className="rounded-full border border-[#d4af37]/16 bg-white/[0.04] px-4 py-2 text-sm text-stone-200">
                    {item.label}
                  </span>
                ))}
              </div>
            </section>

            <section className="mt-8 grid gap-5 md:grid-cols-2 xl:grid-cols-3">
              {(data.chapters || []).map((item) => (
                <article key={item.chapter} className="rounded-[1.7rem] border border-[#d4af37]/18 bg-white/[0.05] p-6">
                  <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[#f3d27a]">Chapter {item.chapter}</p>
                  <h2 className="mt-3 font-playfair text-2xl text-stone-50">{item.title}</h2>
                  <p className="mt-4 text-sm leading-7 text-stone-300">{item.verse_count} verses with 15 situation routes each.</p>
                  <div className="mt-5 flex gap-3">
                    <Link to={item.href} className="inline-flex rounded-full bg-[#d4af37] px-4 py-2 text-sm font-semibold text-stone-950 transition hover:opacity-90">
                      Browse chapter
                    </Link>
                    <Link to={item.sample_href} className="inline-flex rounded-full border border-[#d4af37]/18 bg-white/[0.04] px-4 py-2 text-sm font-semibold text-stone-100 transition hover:border-[#d4af37]/35 hover:bg-white/[0.07]">
                      Open sample
                    </Link>
                  </div>
                </article>
              ))}
            </section>

            <section className="mt-8 grid gap-5 md:grid-cols-2 xl:grid-cols-4">
              {(data.featured_verses || []).map((item) => (
                <article key={item.reference} className="rounded-[1.7rem] border border-[#d4af37]/18 bg-white/[0.05] p-6">
                  <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[#f3d27a]">{item.reference}</p>
                  <p className="mt-4 font-playfair text-xl text-stone-50">{item.translation}</p>
                  <Link to={item.href} className="mt-5 inline-flex rounded-full border border-[#d4af37]/18 bg-white/[0.04] px-4 py-2 text-sm font-semibold text-stone-100 transition hover:border-[#d4af37]/35 hover:bg-white/[0.07]">
                    Open verse page
                  </Link>
                </article>
              ))}
            </section>

            <section className="mt-8 rounded-[1.8rem] border border-[#d4af37]/18 bg-white/[0.05] p-7">
              <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
                <div className="max-w-3xl">
                  <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[#f3d27a]">
                    <Sparkles className="mr-2 inline h-4 w-4" />
                    Recitation mode
                  </p>
                  <h2 className="mt-2 font-playfair text-2xl font-semibold text-stone-50">A smaller featured set for repetition and devotional pacing.</h2>
                  <p className="mt-3 text-sm leading-7 text-stone-300">
                    Start with the curated recitation set if you want a slower entry path than the full 700-verse library.
                  </p>
                </div>
                <div className="flex flex-wrap gap-3">
                  <div className="rounded-full border border-[#d4af37]/16 bg-white/[0.04] px-4 py-2 text-sm text-stone-200">
                    {data.recitation_collection?.count} featured verses
                  </div>
                  <Link to={data.recitation_collection?.href || '/faith/gita/recitation'} className="inline-flex rounded-full bg-[#d4af37] px-5 py-3 text-sm font-semibold text-stone-950 transition hover:opacity-90">
                    Open recitation mode
                  </Link>
                </div>
              </div>
              <div className="mt-5 flex flex-wrap gap-3">
                {(data.recitation_collection?.preview_refs || []).map((item) => (
                  <span key={item} className="rounded-full border border-[#d4af37]/16 bg-white/[0.04] px-4 py-2 text-sm text-stone-200">
                    {item}
                  </span>
                ))}
              </div>
            </section>

            <FaithPathwayLinks
              theme="gold"
              title="Move from verse browsing into guided Gita pathways"
              body="If you want a smaller entry point than the full verse library, start with a curated pathway built around a real life concern and connected support pages."
            />

            <FaithGrowthPanel
              theme="gold"
              sourceTag="faith-gita-hub"
              title="Turn Gita discovery into a devotional reading path"
              body="Join the Faith updates list if you want guided Gita journeys, recitation tracks, and more situation-first verse pathways."
            />
          </>
        ) : null}
      </main>

      <Footer />
    </div>
  );
}
