import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { Link, useParams } from 'react-router-dom';
import { ArrowLeft, ArrowRight, LoaderCircle, Sparkles } from 'lucide-react';
import { Footer } from '../../components/Footer';
import { SEO } from '../../components/SEO';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '../../components/ui/accordion';
import { API, SITE, buildArticleSchema, buildBreadcrumbSchema, buildFaqSchema, titleCaseSlug } from './faithShared';
import { FaithGrowthPanel } from './FaithGrowthPanel';
import { FaithPathwayLinks } from './FaithPathwayLinks';

function buildSchema(data) {
  if (!data) return null;
  return {
    '@context': 'https://schema.org',
    '@graph': [
      buildArticleSchema({
        headline: data.title,
        description: data.meta_description,
        url: `${SITE}${data.route}`,
        about: {
          '@type': 'Book',
          name: 'Bible',
        },
      }),
      buildFaqSchema(data.faq),
      buildBreadcrumbSchema([
        { name: 'Home', url: SITE },
        { name: 'Faith Hubs', url: `${SITE}/faith` },
        { name: 'Bible', url: `${SITE}/faith/bible` },
        { name: data.topic_label, url: `${SITE}/faith/bible/topic/${data.topic_slug}` },
        { name: data.transition_label, url: `${SITE}${data.route}` },
      ]),
    ],
  };
}

export function BibleTopicPage() {
  const { topicSlug = '', transitionSlug = '' } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let ignore = false;

    async function fetchPage() {
      try {
        setLoading(true);
        setError('');
        const response = await axios.get(`${API}/bible/${topicSlug}/${transitionSlug}`);
        if (!ignore) setData(response.data);
      } catch (err) {
        if (!ignore) {
          setData(null);
          setError(err?.response?.status === 404 ? 'Bible promise page not found.' : 'Unable to load this Bible page right now.');
        }
      } finally {
        if (!ignore) setLoading(false);
      }
    }

    fetchPage();
    return () => {
      ignore = true;
    };
  }, [topicSlug, transitionSlug]);

  const schema = useMemo(() => buildSchema(data), [data]);

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,rgba(74,222,128,0.13),transparent_30%),linear-gradient(180deg,#0f1116_0%,#151b22_42%,#1d2530_100%)] text-stone-100">
      <SEO
        title={data?.meta_title || `Bible Promises for ${titleCaseSlug(transitionSlug)}`}
        description={data?.meta_description || 'Bible promise page by transition.'}
        url={data ? `${SITE}${data.route}` : `${SITE}/faith/bible/${topicSlug}/${transitionSlug}`}
        schema={schema}
        noindex={!loading && !!error && !data}
      />

      <main className="mx-auto max-w-6xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="mb-6 flex items-center gap-2 text-sm text-stone-400">
          <Link to="/faith" className="transition hover:text-emerald-300">Faith Hubs</Link>
          <span>/</span>
          <Link to="/faith/bible" className="transition hover:text-emerald-300">Bible</Link>
          <span>/</span>
          <Link to={`/faith/bible/topic/${topicSlug}`} className="transition hover:text-emerald-300">{data?.topic_label || titleCaseSlug(topicSlug)}</Link>
          <span>/</span>
          <span className="text-stone-200">{data?.transition_label || titleCaseSlug(transitionSlug)}</span>
        </div>

        <Link to={`/faith/bible/topic/${topicSlug}`} className="mb-6 inline-flex items-center text-sm font-medium text-stone-400 transition hover:text-emerald-300">
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to topic hub
        </Link>

        {loading ? (
          <div className="flex items-center justify-center rounded-[2rem] border border-emerald-300/20 bg-white/[0.05] p-12 text-stone-300">
            <LoaderCircle className="mr-3 h-5 w-5 animate-spin text-emerald-200" />
            Loading Bible guidance...
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
                    {data.topic_label}
                  </div>
                  <h1 className="mt-4 font-cinzel text-4xl font-semibold leading-tight text-stone-50 sm:text-5xl">{data.title}</h1>
                  <p className="mt-4 text-base leading-8 text-stone-300">{data.summary}</p>
                </div>
                <div className="rounded-[1.5rem] border border-emerald-300/18 bg-emerald-400/10 px-5 py-4 text-sm">
                  <p className="text-xs font-semibold uppercase tracking-[0.18em] text-emerald-200">Cross-tradition bridge</p>
                  <Link to={data.links.gita_cross_href} className="mt-2 block font-semibold text-stone-50 underline underline-offset-4">
                    {data.links.gita_cross_reference}
                  </Link>
                </div>
              </div>
            </section>

            <section className="mt-8 rounded-[1.8rem] border border-emerald-300/18 bg-white/[0.05] p-7">
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-emerald-200">Emotional frame</p>
              <p className="mt-4 text-sm leading-8 text-stone-300">{data.emotional_frame}</p>
            </section>

            <section className="mt-8 grid gap-6 lg:grid-cols-[1.05fr_0.95fr]">
              <article className="rounded-[1.8rem] border border-emerald-300/18 bg-white/[0.05] p-7">
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-emerald-200">Verse presentation</p>
                <p className="mt-4 text-sm font-semibold text-stone-50">{data.reference}</p>
                <p className="mt-3 font-playfair text-xl text-stone-100">{data.verse_text}</p>
                <p className="mt-4 text-xs uppercase tracking-[0.18em] text-stone-500">Source: {data.source}</p>
              </article>

              <article className="rounded-[1.8rem] border border-emerald-300/18 bg-white/[0.05] p-7">
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-emerald-200">Hermeneutical unpacking</p>
                <p className="mt-4 text-sm leading-8 text-stone-300">{data.hermeneutical}</p>
              </article>
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
                <p className="mt-5 text-sm leading-7 text-stone-300">
                  These references come from the reviewed Scripture for Every Moment topical bank and widen the page without copying additional devotional prose.
                </p>
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
                  These are controlled internal cues from the reviewed Bible meanings source, used to vary interpretive flavor while keeping the published wording original.
                </p>
              </article>
            </section>

            <section className="mt-8 grid gap-6 lg:grid-cols-[0.95fr_1.05fr]">
              <article className="rounded-[1.8rem] border border-emerald-300/18 bg-white/[0.05] p-7">
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-emerald-200">Practical application</p>
                <p className="mt-4 text-sm leading-8 text-stone-300">{data.application}</p>
              </article>

              <article className="rounded-[1.8rem] border border-emerald-300/18 bg-white/[0.05] p-7">
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-emerald-200">Vedic resonance bridge</p>
                <p className="mt-4 text-sm leading-8 text-stone-300">{data.vedic_bridge}</p>
                <div className="mt-6 flex flex-wrap gap-3">
                  <Link to={data.links.gita_cross_href} className="inline-flex rounded-full bg-emerald-300 px-5 py-3 text-sm font-semibold text-slate-950 transition hover:opacity-90">
                    Open parallel Gita page
                  </Link>
                  <Link to={data.links.faith_transit_href} className="inline-flex rounded-full border border-emerald-300/18 bg-white/[0.04] px-5 py-3 text-sm font-semibold text-stone-100 transition hover:border-emerald-300/35 hover:bg-white/[0.07]">
                    Open transit companion
                  </Link>
                </div>
              </article>
            </section>

            <section className="mt-8 rounded-[1.8rem] border border-emerald-300/18 bg-white/[0.05] p-7">
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-emerald-200">Source trail</p>
              <p className="mt-4 text-sm leading-7 text-stone-300">
                Primary source bucket: {data.provenance?.primary_source?.label} / {data.provenance?.primary_source?.section_title}.
              </p>
              <p className="mt-3 text-sm leading-7 text-stone-300">
                Supporting topical bank: {(data.provenance?.supporting_sources?.[0]?.topic_labels || []).join(', ')}.
              </p>
              <p className="mt-3 text-sm leading-7 text-stone-300">
                Symbolic lexicon tags: {(data.provenance?.supporting_sources?.[1]?.meaning_keys || []).join(', ')}.
              </p>
            </section>

            <section className="mt-8 grid gap-6 lg:grid-cols-[0.95fr_1.05fr]">
              <article className="rounded-[1.8rem] border border-emerald-300/18 bg-white/[0.05] p-7">
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-emerald-200">FAQ</p>
                <Accordion type="single" collapsible className="mt-4 space-y-3">
                  {(data.faq || []).map((item, index) => (
                    <AccordionItem key={item.q} value={`faq-${index}`} className="rounded-[1.1rem] border border-emerald-300/16 bg-white/[0.04] px-4">
                      <AccordionTrigger className="text-left text-sm font-semibold text-stone-100">{item.q}</AccordionTrigger>
                      <AccordionContent className="text-sm leading-7 text-stone-300">{item.a}</AccordionContent>
                    </AccordionItem>
                  ))}
                </Accordion>
              </article>

              <article className="rounded-[1.8rem] border border-emerald-300/18 bg-white/[0.05] p-7">
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-emerald-200">More transition paths</p>
                <div className="mt-5 flex flex-wrap gap-3">
                  {(data.top_transitions || []).map((item) => (
                    <Link
                      key={item.slug}
                      to={item.href}
                      className="rounded-full border border-emerald-300/16 bg-white/[0.04] px-4 py-2 text-sm text-stone-200 transition hover:border-emerald-300/40 hover:text-emerald-200"
                    >
                      {item.label}
                    </Link>
                  ))}
                </div>
                <div className="mt-6">
                  <a href={data.links.traits_href} className="inline-flex items-center rounded-full border border-emerald-300/18 bg-white/[0.04] px-5 py-3 text-sm font-semibold text-stone-100 transition hover:border-emerald-300/35 hover:bg-white/[0.07]">
                    Related traits page
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </a>
                </div>
              </article>
            </section>

            <FaithPathwayLinks
              theme="emerald"
              title="Take this promise into a broader guided pathway"
              body="Pathways help connect this Bible page with matching Gita, transit, and daily surfaces when the reader needs a more complete route through the same concern."
            />

            <FaithGrowthPanel
              theme="emerald"
              sourceTag={`faith-bible-${topicSlug}`}
              title="Want more Bible guidance for this kind of transition?"
              body="Join the Faith updates list and tell us which concern should shape the next devotional sequence, email plan, or printable scripture pack."
            />
          </>
        ) : null}
      </main>

      <Footer />
    </div>
  );
}
