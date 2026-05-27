import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { Link, useParams } from 'react-router-dom';
import { ArrowLeft, BookMarked, LoaderCircle } from 'lucide-react';
import { Footer } from '../../components/Footer';
import { SEO } from '../../components/SEO';
import { API, SITE, buildBreadcrumbSchema, buildCollectionSchema, titleCaseSlug } from './faithShared';
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
        url: `${SITE}/faith/bible/topic/${data.topic_slug}`,
        items: (data.transitions || []).map((item) => ({ name: item.label, url: `${SITE}${item.href}` })),
      }),
      buildBreadcrumbSchema([
        { name: 'Home', url: SITE },
        { name: 'Faith Hubs', url: `${SITE}/faith` },
        { name: 'Bible', url: `${SITE}/faith/bible` },
        { name: data.topic_label, url: `${SITE}/faith/bible/topic/${data.topic_slug}` },
      ]),
    ],
  };
}

export function FaithBibleTopicPage() {
  const { topicSlug = '' } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let ignore = false;

    async function fetchTopic() {
      try {
        setLoading(true);
        setError('');
        const response = await axios.get(`${API}/bible/topic/${topicSlug}`);
        if (!ignore) setData(response.data);
      } catch (err) {
        if (!ignore) {
          setData(null);
          setError(err?.response?.status === 404 ? 'Bible topic hub not found.' : 'Unable to load this Bible topic right now.');
        }
      } finally {
        if (!ignore) setLoading(false);
      }
    }

    fetchTopic();
    return () => {
      ignore = true;
    };
  }, [topicSlug]);

  const schema = useMemo(() => buildSchema(data), [data]);

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,rgba(74,222,128,0.13),transparent_30%),linear-gradient(180deg,#0f1116_0%,#151b22_42%,#1d2530_100%)] text-stone-100">
      <SEO
        title={data?.meta_title || `${titleCaseSlug(topicSlug)} Bible Promises`}
        description={data?.meta_description || 'Bible promise topic hub.'}
        url={`${SITE}/faith/bible/topic/${topicSlug}`}
        schema={schema}
        noindex={!loading && !!error && !data}
      />

      <main className="mx-auto max-w-6xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="mb-6 flex items-center gap-2 text-sm text-stone-400">
          <Link to="/faith" className="transition hover:text-emerald-300">Faith Hubs</Link>
          <span>/</span>
          <Link to="/faith/bible" className="transition hover:text-emerald-300">Bible</Link>
          <span>/</span>
          <span className="text-stone-200">{data?.topic_label || titleCaseSlug(topicSlug)}</span>
        </div>

        <Link to="/faith/bible" className="mb-6 inline-flex items-center text-sm font-medium text-stone-400 transition hover:text-emerald-300">
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Bible hub
        </Link>

        {loading ? (
          <div className="flex items-center justify-center rounded-[2rem] border border-emerald-300/20 bg-white/[0.05] p-12 text-stone-300">
            <LoaderCircle className="mr-3 h-5 w-5 animate-spin text-emerald-200" />
            Loading Bible topic hub...
          </div>
        ) : error ? (
          <div className="rounded-[2rem] border border-red-400/25 bg-red-500/10 p-6 text-sm text-red-200">{error}</div>
        ) : data ? (
          <>
            <section className="rounded-[2rem] border border-emerald-300/20 bg-white/[0.05] p-8 shadow-[0_24px_80px_rgba(0,0,0,0.28)] backdrop-blur">
              <div className="flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
                <div className="max-w-3xl">
                  <div className="inline-flex items-center gap-2 rounded-full border border-emerald-300/25 bg-emerald-400/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.24em] text-emerald-200">
                    <BookMarked className="h-3.5 w-3.5" />
                    {data.topic_label}
                  </div>
                  <h1 className="mt-4 font-cinzel text-4xl font-semibold leading-tight text-stone-50 sm:text-5xl">{data.hero_title}</h1>
                  <p className="mt-4 text-base leading-8 text-stone-300">{data.hero_body}</p>
                </div>
                <div className="rounded-[1.5rem] border border-emerald-300/18 bg-emerald-400/10 px-5 py-4 text-sm">
                  <p className="text-xs font-semibold uppercase tracking-[0.18em] text-emerald-200">Theme note</p>
                  <p className="mt-2 font-semibold text-stone-50">{data.theme_term}</p>
                  <p className="mt-2 max-w-xs text-stone-300">{data.theme_term_note}</p>
                </div>
              </div>
            </section>

            <section className="mt-8 rounded-[1.8rem] border border-emerald-300/18 bg-white/[0.05] p-7">
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-emerald-200">Sample promise</p>
              <p className="mt-4 text-sm font-semibold text-stone-50">{data.sample_reference}</p>
              <p className="mt-3 font-playfair text-xl text-stone-100">{data.sample_text}</p>
              <p className="mt-4 text-xs uppercase tracking-[0.18em] text-stone-500">Source: {data.sample_source}</p>
            </section>

            <section className="mt-8 grid gap-6 lg:grid-cols-[1.05fr_0.95fr]">
              <article className="rounded-[1.8rem] border border-emerald-300/18 bg-white/[0.05] p-7">
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-emerald-200">More scriptures for this moment</p>
                <div className="mt-5 flex flex-wrap gap-3">
                  {(data.supporting_references || []).map((item) => (
                    <span
                      key={`${item.source_slug}-${item.reference}`}
                      className="rounded-full border border-emerald-300/16 bg-white/[0.04] px-4 py-2 text-sm text-stone-200"
                    >
                      {item.reference}
                    </span>
                  ))}
                </div>
              </article>

              <article className="rounded-[1.8rem] border border-emerald-300/18 bg-white/[0.05] p-7">
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-emerald-200">Symbolic vocabulary</p>
                <div className="mt-5 flex flex-wrap gap-3">
                  {(data.meaning_tags || []).map((item) => (
                    <span
                      key={item.key}
                      className="rounded-full border border-emerald-300/16 bg-white/[0.04] px-4 py-2 text-sm text-stone-200"
                    >
                      {item.label}
                    </span>
                  ))}
                </div>
                <p className="mt-5 text-sm leading-7 text-stone-300">
                  These controlled tags are internal flavor cues shaped from the reviewed Bible meanings source, while all public wording remains original.
                </p>
              </article>
            </section>

            <section className="mt-8 rounded-[1.8rem] border border-emerald-300/18 bg-white/[0.05] p-7">
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-emerald-200">Source trail</p>
              <p className="mt-4 text-sm leading-7 text-stone-300">
                Primary verse spine: {data.provenance?.primary_source?.label} / {data.provenance?.primary_source?.section_title}.
              </p>
              <p className="mt-3 text-sm leading-7 text-stone-300">
                Supporting reference bank: {(data.provenance?.supporting_sources?.[0]?.topic_labels || []).join(', ')}.
              </p>
            </section>

            <section className="mt-8 grid gap-5 lg:grid-cols-2">
              {(data.transitions || []).map((item) => (
                <article key={item.slug} className="rounded-[1.7rem] border border-emerald-300/18 bg-white/[0.05] p-6">
                  <p className="text-xs font-semibold uppercase tracking-[0.18em] text-emerald-200">{item.label}</p>
                  <p className="mt-4 text-sm leading-7 text-stone-300">
                    Read how this Bible theme applies specifically inside the transition of {item.label.toLowerCase()}.
                  </p>
                  <Link
                    to={item.href}
                    className="mt-5 inline-flex rounded-full bg-emerald-300 px-4 py-2 text-sm font-semibold text-slate-950 transition hover:opacity-90"
                  >
                    Open transition page
                  </Link>
                </article>
              ))}
            </section>

            <FaithPathwayLinks
              theme="emerald"
              title="Need a narrower starting point than the full transition grid?"
              body="Use a guided pathway when this Bible theme is part of a larger pressure pattern like anxiety, financial strain, parenting stress, or health disruption."
            />

            <FaithGrowthPanel
              theme="emerald"
              sourceTag={`faith-bible-topic-${topicSlug}`}
              title="Help us deepen this Bible topic with devotional follow-ups"
              body="Join the Faith updates list if you want more guided sequences around this theme and related life transitions."
            />
          </>
        ) : null}
      </main>

      <Footer />
    </div>
  );
}
