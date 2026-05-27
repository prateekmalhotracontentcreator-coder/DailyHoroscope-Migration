import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { Link, useParams } from 'react-router-dom';
import { ArrowLeft, BookMarked, LoaderCircle } from 'lucide-react';
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
        url: `${SITE}/faith/gita/chapter/${data.chapter}`,
        items: (data.verses || []).map((item) => ({ name: item.reference, url: `${SITE}${item.preview_href}` })),
      }),
      buildBreadcrumbSchema([
        { name: 'Home', url: SITE },
        { name: 'Faith Hubs', url: `${SITE}/faith` },
        { name: 'Gita', url: `${SITE}/faith/gita` },
        { name: `Chapter ${data.chapter}`, url: `${SITE}/faith/gita/chapter/${data.chapter}` },
      ]),
    ],
  };
}

export function FaithGitaChapterPage() {
  const { chapter = '' } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let ignore = false;

    async function fetchChapter() {
      try {
        setLoading(true);
        setError('');
        const response = await axios.get(`${API}/gita/chapter/${chapter}`);
        if (!ignore) setData(response.data);
      } catch (err) {
        if (!ignore) {
          setData(null);
          setError(err?.response?.status === 404 ? 'Gita chapter hub not found.' : 'Unable to load this Gita chapter right now.');
        }
      } finally {
        if (!ignore) setLoading(false);
      }
    }

    fetchChapter();
    return () => {
      ignore = true;
    };
  }, [chapter]);

  const schema = useMemo(() => buildSchema(data), [data]);

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,rgba(236,179,61,0.16),transparent_30%),linear-gradient(180deg,#0f1014_0%,#17171f_45%,#201f29_100%)] text-stone-100">
      <SEO
        title={data?.meta_title || `Bhagavad Gita Chapter ${chapter}`}
        description={data?.meta_description || 'Bhagavad Gita chapter hub.'}
        url={`${SITE}/faith/gita/chapter/${chapter}`}
        schema={schema}
        noindex={!loading && !!error && !data}
      />

      <main className="mx-auto max-w-6xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="mb-6 flex items-center gap-2 text-sm text-stone-400">
          <Link to="/faith" className="transition hover:text-[#f3d27a]">Faith Hubs</Link>
          <span>/</span>
          <Link to="/faith/gita" className="transition hover:text-[#f3d27a]">Gita</Link>
          <span>/</span>
          <span className="text-stone-200">Chapter {data?.chapter || chapter}</span>
        </div>

        <Link to="/faith/gita" className="mb-6 inline-flex items-center text-sm font-medium text-stone-400 transition hover:text-[#f3d27a]">
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Gita hub
        </Link>

        {loading ? (
          <div className="flex items-center justify-center rounded-[2rem] border border-[#d4af37]/20 bg-white/[0.05] p-12 text-stone-300">
            <LoaderCircle className="mr-3 h-5 w-5 animate-spin text-[#f3d27a]" />
            Loading chapter hub...
          </div>
        ) : error ? (
          <div className="rounded-[2rem] border border-red-400/25 bg-red-500/10 p-6 text-sm text-red-200">{error}</div>
        ) : data ? (
          <>
            <section className="rounded-[2rem] border border-[#d4af37]/20 bg-white/[0.05] p-8 shadow-[0_24px_80px_rgba(0,0,0,0.28)] backdrop-blur">
              <div className="flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
                <div className="max-w-3xl">
                  <div className="inline-flex items-center gap-2 rounded-full border border-[#d4af37]/25 bg-[#d4af37]/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.24em] text-[#f3d27a]">
                    <BookMarked className="h-3.5 w-3.5" />
                    Chapter {data.chapter}
                  </div>
                  <h1 className="mt-4 font-cinzel text-4xl font-semibold leading-tight text-stone-50 sm:text-5xl">{data.hero_title}</h1>
                  <p className="mt-4 text-base leading-8 text-stone-300">{data.hero_body}</p>
                </div>
                <div className="rounded-[1.5rem] border border-[#d4af37]/18 bg-[#d4af37]/10 px-5 py-4 text-sm">
                  <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[#f3d27a]">Chapter size</p>
                  <p className="mt-2 font-semibold text-stone-50">{data.verse_count} verses</p>
                </div>
              </div>
            </section>

            <section className="mt-8 rounded-[1.8rem] border border-[#d4af37]/18 bg-white/[0.05] p-7">
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[#f3d27a]">Situation index</p>
              <div className="mt-5 flex flex-wrap gap-3">
                {(data.situations || []).map((item) => (
                  <span key={item.slug} className="rounded-full border border-[#d4af37]/16 bg-white/[0.04] px-4 py-2 text-sm text-stone-200">
                    {item.label}
                  </span>
                ))}
              </div>
            </section>

            <section className="mt-8 grid gap-5 lg:grid-cols-2">
              {(data.verses || []).map((item) => (
                <article key={item.reference} className="rounded-[1.7rem] border border-[#d4af37]/18 bg-white/[0.05] p-6">
                  <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[#f3d27a]">{item.reference}</p>
                  <p className="mt-4 font-playfair text-xl text-stone-50">{item.translation}</p>
                  <div className="mt-5 flex flex-wrap gap-2">
                    {(item.top_situations || []).map((situation) => (
                      <Link
                        key={`${item.reference}-${situation.slug}`}
                        to={situation.href}
                        className="rounded-full border border-[#d4af37]/16 bg-white/[0.04] px-3 py-2 text-xs font-medium text-stone-200 transition hover:border-[#d4af37]/40 hover:text-[#f6dda0]"
                      >
                        {situation.label}
                      </Link>
                    ))}
                  </div>
                  <Link
                    to={item.preview_href}
                    className="mt-5 inline-flex rounded-full bg-[#d4af37] px-4 py-2 text-sm font-semibold text-stone-950 transition hover:opacity-90"
                  >
                    Open sample path
                  </Link>
                </article>
              ))}
            </section>

            <FaithPathwayLinks
              theme="gold"
              title="Need a smaller doorway into this chapter?"
              body="Guided pathways group Gita, Bible, transit, and daily pages around one life issue, which can be easier than starting from the whole chapter at once."
            />

            <FaithGrowthPanel
              theme="gold"
              sourceTag={`faith-gita-chapter-${chapter}`}
              title="Turn this chapter into a guided devotional sequence"
              body="Join the Faith updates list if you want chapter-based Gita journeys, recitation layers, and more situation-first devotional pathways."
            />
          </>
        ) : null}
      </main>

      <Footer />
    </div>
  );
}
