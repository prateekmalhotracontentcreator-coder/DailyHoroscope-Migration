import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { ArrowLeft, BookOpenText, LoaderCircle, Orbit } from 'lucide-react';
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
        name: 'Faith Transit Hub',
        description: data.hero_body,
        url: `${SITE}/faith/transit`,
        items: (data.transits || []).slice(0, 78).map((item) => ({ name: item.label, url: `${SITE}/faith/transit/${item.slug}/gita` })),
      }),
      buildBreadcrumbSchema([
        { name: 'Home', url: SITE },
        { name: 'Faith Hubs', url: `${SITE}/faith` },
        { name: 'Transit', url: `${SITE}/faith/transit` },
      ]),
    ],
  };
}

export function FaithTransitHubPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let ignore = false;

    async function fetchHub() {
      try {
        setLoading(true);
        setError('');
        const response = await axios.get(`${API}/transit/hub`);
        if (!ignore) setData(response.data);
      } catch {
        if (!ignore) {
          setData(null);
          setError('Unable to load the Faith transit hub right now.');
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
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,rgba(255,193,94,0.14),transparent_28%),linear-gradient(180deg,#0d1015_0%,#141a22_42%,#1f2731_100%)] text-stone-100">
      <SEO
        title={data?.meta_title || 'Faith Transit Hub'}
        description={data?.meta_description || 'Transit-based Gita and Bible guidance.'}
        url={`${SITE}/faith/transit`}
        schema={schema}
      />

      <main className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="mb-6 flex items-center gap-2 text-sm text-stone-400">
          <Link to="/faith" className="transition hover:text-[#f3d27a]">Faith Hubs</Link>
          <span>/</span>
          <span className="text-stone-200">Transit</span>
        </div>

        <Link to="/faith" className="mb-6 inline-flex items-center text-sm font-medium text-stone-400 transition hover:text-[#f3d27a]">
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Faith Hubs
        </Link>

        <section className="rounded-[2rem] border border-[#d4af37]/20 bg-white/[0.05] p-8 shadow-[0_24px_80px_rgba(0,0,0,0.28)] backdrop-blur">
          <div className="inline-flex items-center gap-2 rounded-full border border-[#d4af37]/25 bg-[#d4af37]/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.24em] text-[#f3d27a]">
            <Orbit className="h-3.5 w-3.5" />
            Faith Transit Hub
          </div>
          <h1 className="mt-5 font-cinzel text-4xl font-semibold leading-tight text-stone-50 sm:text-5xl">
            {data?.hero_title || 'Transit and Scripture Guidance'}
          </h1>
          <p className="mt-5 max-w-3xl text-base leading-8 text-stone-300">
            {data?.hero_body || 'Planetary transit pages paired with grounded scripture guidance.'}
          </p>
        </section>

        {!loading && data ? (
          <section className="mt-8 grid gap-4 md:grid-cols-2">
            {(data.traditions || []).map((item) => (
              <article key={item.slug} className="rounded-[1.7rem] border border-[#d4af37]/18 bg-white/[0.05] p-6">
                <p className="text-xs font-semibold uppercase tracking-[0.2em] text-[#f3d27a]">{item.label}</p>
                <p className="mt-3 text-sm leading-7 text-stone-300">{item.description}</p>
              </article>
            ))}
          </section>
        ) : null}

        <section className="mt-8">
          {loading ? (
            <div className="flex items-center justify-center rounded-[2rem] border border-[#d4af37]/20 bg-white/[0.05] p-10 text-stone-300">
              <LoaderCircle className="mr-3 h-5 w-5 animate-spin text-[#f3d27a]" />
              Loading transit guides...
            </div>
          ) : error ? (
            <div className="rounded-[2rem] border border-red-400/25 bg-red-500/10 p-6 text-sm text-red-200">{error}</div>
          ) : (
            <div className="grid gap-5 lg:grid-cols-2">
              {(data?.transits || []).map((item) => (
                <article key={item.slug} className="rounded-[1.7rem] border border-[#d4af37]/18 bg-white/[0.05] p-6">
                  <div className="flex items-center justify-between gap-4">
                    <div className="inline-flex rounded-2xl border border-[#d4af37]/18 bg-[#d4af37]/10 p-3 text-[#f3d27a]">
                      <BookOpenText className="h-5 w-5" />
                    </div>
                    <span className="rounded-full border border-[#d4af37]/16 bg-white/[0.04] px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.18em] text-[#f3d27a]">
                      2 traditions
                    </span>
                  </div>
                  <h2 className="mt-4 font-cinzel text-2xl font-semibold text-stone-50">{item.label}</h2>
                  <div className="mt-5 grid gap-3 sm:grid-cols-2">
                    <Link
                      to={`/faith/transit/${item.slug}/gita`}
                      className="rounded-[1.2rem] border border-[#d4af37]/18 bg-white/[0.04] px-4 py-3 text-sm font-semibold text-stone-100 transition hover:border-[#d4af37]/35 hover:bg-white/[0.07]"
                    >
                      Gita guidance
                    </Link>
                    <Link
                      to={`/faith/transit/${item.slug}/bible`}
                      className="rounded-[1.2rem] border border-[#d4af37]/18 bg-white/[0.04] px-4 py-3 text-sm font-semibold text-stone-100 transition hover:border-[#d4af37]/35 hover:bg-white/[0.07]"
                    >
                      Bible guidance
                    </Link>
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>

        {!loading && !error && data ? (
          <FaithPathwayLinks
            theme="gold"
            title="Use a pathway when the transit is only part of the pressure"
            body="Transit pages work best when they connect to a bigger concern. Start with a guided pathway if you want to combine scripture, timing, and daily support."
          />
        ) : null}

        <FaithGrowthPanel
          theme="gold"
          sourceTag="faith-transit-hub"
          title="Use transit intent to shape the next Faith journeys"
          body="Join the Faith updates list if you want more transit-linked devotionals, compare-tradition pages, and seasonal guidance sequences."
        />
      </main>

      <Footer />
    </div>
  );
}
