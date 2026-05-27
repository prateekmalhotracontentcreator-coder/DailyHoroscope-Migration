import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { Link, useParams } from 'react-router-dom';
import { ArrowLeft, ArrowRight, BookHeart, LoaderCircle, Sparkles } from 'lucide-react';
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
          name: 'Bhagavad Gita',
        },
      }),
      buildFaqSchema(data.faq),
      buildBreadcrumbSchema([
        { name: 'Home', url: SITE },
        { name: 'Faith Hubs', url: `${SITE}/faith` },
        { name: 'Gita', url: `${SITE}/faith/gita` },
        { name: `Chapter ${data.chapter}`, url: `${SITE}/faith/gita/chapter/${data.chapter}` },
        { name: data.situation_label, url: `${SITE}${data.route}` },
      ]),
    ],
  };
}

function parseChapterVerse(value) {
  const [chapter, verse] = String(value || '').split('-').map((item) => Number(item));
  return {
    chapter: Number.isFinite(chapter) ? chapter : 0,
    verse: Number.isFinite(verse) ? verse : 0,
  };
}

export function GitaVersePage() {
  const { chapterVerse = '', situationSlug = '' } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { chapter, verse } = useMemo(() => parseChapterVerse(chapterVerse), [chapterVerse]);

  useEffect(() => {
    let ignore = false;

    async function fetchPage() {
      try {
        setLoading(true);
        setError('');
        const response = await axios.get(`${API}/gita/${chapter}/${verse}/${situationSlug}`);
        if (!ignore) setData(response.data);
      } catch (err) {
        if (!ignore) {
          setData(null);
          setError(err?.response?.status === 404 ? 'Gita verse page not found.' : 'Unable to load this Gita page right now.');
        }
      } finally {
        if (!ignore) setLoading(false);
      }
    }

    if (chapter && verse && situationSlug) {
      fetchPage();
    } else {
      setData(null);
      setLoading(false);
      setError('Invalid Gita verse route.');
    }

    return () => {
      ignore = true;
    };
  }, [chapter, verse, situationSlug]);

  const schema = useMemo(() => buildSchema(data), [data]);

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,rgba(233,179,71,0.14),transparent_30%),linear-gradient(180deg,#0f1014_0%,#16171e_46%,#201f29_100%)] text-stone-100">
      <SEO
        title={data?.meta_title || `Bhagavad Gita ${chapter}:${verse} for ${titleCaseSlug(situationSlug)}`}
        description={data?.meta_description || 'Bhagavad Gita verse guidance by life situation.'}
        url={data ? `${SITE}${data.route}` : `${SITE}/faith/gita/${chapterVerse}/${situationSlug}`}
        schema={schema}
        noindex={!loading && !!error && !data}
      />

      <main className="mx-auto max-w-6xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="mb-6 flex items-center gap-2 text-sm text-stone-400">
          <Link to="/faith" className="transition hover:text-[#f3d27a]">Faith Hubs</Link>
          <span>/</span>
          <Link to="/faith/gita" className="transition hover:text-[#f3d27a]">Gita</Link>
          <span>/</span>
          <Link to={`/faith/gita/chapter/${chapter}`} className="transition hover:text-[#f3d27a]">Chapter {chapter}</Link>
          <span>/</span>
          <span className="text-stone-200">{data?.situation_label || titleCaseSlug(situationSlug)}</span>
        </div>

        <Link to={`/faith/gita/chapter/${chapter}`} className="mb-6 inline-flex items-center text-sm font-medium text-stone-400 transition hover:text-[#f3d27a]">
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to chapter hub
        </Link>

        {loading ? (
          <div className="flex items-center justify-center rounded-[2rem] border border-[#d4af37]/20 bg-white/[0.05] p-12 text-stone-300">
            <LoaderCircle className="mr-3 h-5 w-5 animate-spin text-[#f3d27a]" />
            Loading Gita guidance...
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
                    {data.reference}
                  </div>
                  <h1 className="mt-4 font-cinzel text-4xl font-semibold leading-tight text-stone-50 sm:text-5xl">{data.title}</h1>
                  <p className="mt-4 text-base leading-8 text-stone-300">{data.summary}</p>
                </div>
                <div className="rounded-[1.5rem] border border-[#d4af37]/18 bg-[#d4af37]/10 px-5 py-4 text-sm">
                  <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[#f3d27a]">Transit companion</p>
                  <Link to={data.links.faith_transit_href} className="mt-2 block font-semibold text-stone-50 underline underline-offset-4">
                    {data.situation_label} transit page
                  </Link>
                </div>
              </div>
            </section>

            <section className="mt-8 rounded-[1.8rem] border border-[#d4af37]/18 bg-white/[0.05] p-7">
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[#f3d27a]">Situation hook</p>
              <p className="mt-4 text-sm leading-8 text-stone-300">{data.hook}</p>
            </section>

            <section className="mt-8 grid gap-6 lg:grid-cols-[1.05fr_0.95fr]">
              <article className="rounded-[1.8rem] border border-[#d4af37]/18 bg-white/[0.05] p-7">
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[#f3d27a]">Verse presentation</p>
                <p className="mt-4 font-playfair text-xl leading-9 text-stone-50">{data.verse_iast}</p>
                <p className="mt-4 text-sm italic leading-7 text-stone-300">{data.transliteration}</p>
                <p className="mt-5 text-sm leading-7 text-stone-200">{data.translation}</p>
                <p className="mt-4 text-xs uppercase tracking-[0.18em] text-stone-500">Source: {data.source}</p>
              </article>

              <article className="rounded-[1.8rem] border border-[#d4af37]/18 bg-white/[0.05] p-7">
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[#f3d27a]">Apply it today</p>
                <p className="mt-4 text-sm leading-8 text-stone-300">{data.application}</p>
                <ul className="mt-5 space-y-3 text-sm text-stone-300">
                  {(data.practice_prompts || []).map((item) => (
                    <li key={item} className="rounded-[1.1rem] border border-[#d4af37]/16 bg-white/[0.04] px-4 py-3 leading-7">
                      {item}
                    </li>
                  ))}
                </ul>
              </article>
            </section>

            <section className="mt-8 grid gap-5 md:grid-cols-3">
              {(data.etymology_items || []).map((item) => (
                <article key={item.term} className="rounded-[1.5rem] border border-[#d4af37]/18 bg-white/[0.05] p-6">
                  <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[#f3d27a]">{item.term}</p>
                  <p className="mt-3 text-sm font-semibold text-stone-50">{item.gloss}</p>
                  <p className="mt-4 text-sm leading-7 text-stone-300">{item.application}</p>
                </article>
              ))}
            </section>

            <section className="mt-8 grid gap-6 lg:grid-cols-[0.95fr_1.05fr]">
              <article className="rounded-[1.8rem] border border-[#d4af37]/18 bg-white/[0.05] p-7">
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[#f3d27a]">
                  <Sparkles className="mr-2 inline h-4 w-4" />
                  Transit layer
                </p>
                <p className="mt-4 text-sm leading-8 text-stone-300">{data.transit_layer}</p>
                <div className="mt-6 flex flex-wrap gap-3">
                  <Link to={data.links.current_month_href} className="inline-flex rounded-full bg-[#d4af37] px-5 py-3 text-sm font-semibold text-stone-950 transition hover:opacity-90">
                    Open current month guide
                  </Link>
                  <a href={data.links.panchang_href} className="inline-flex rounded-full border border-[#d4af37]/18 bg-white/[0.04] px-5 py-3 text-sm font-semibold text-stone-100 transition hover:border-[#d4af37]/35 hover:bg-white/[0.07]">
                    Check panchang timing
                  </a>
                </div>
              </article>

              <article className="rounded-[1.8rem] border border-[#d4af37]/18 bg-white/[0.05] p-7">
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[#f3d27a]">FAQ</p>
                <Accordion type="single" collapsible className="mt-4 space-y-3">
                  {(data.faq || []).map((item, index) => (
                    <AccordionItem key={item.q} value={`faq-${index}`} className="rounded-[1.1rem] border border-[#d4af37]/16 bg-white/[0.04] px-4">
                      <AccordionTrigger className="text-left text-sm font-semibold text-stone-100">{item.q}</AccordionTrigger>
                      <AccordionContent className="text-sm leading-7 text-stone-300">{item.a}</AccordionContent>
                    </AccordionItem>
                  ))}
                </Accordion>
              </article>
            </section>

            <section className="mt-8 rounded-[1.8rem] border border-[#d4af37]/18 bg-white/[0.05] p-7">
              <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
                <div>
                  <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[#f3d27a]">More situation paths</p>
                  <h2 className="mt-2 font-playfair text-2xl font-semibold text-stone-50">The same verse can guide a very different kind of pressure.</h2>
                </div>
                <Link to={data.links.chapter_hub_href} className="inline-flex items-center rounded-full border border-[#d4af37]/20 bg-white/[0.04] px-5 py-3 text-sm font-semibold text-stone-100 transition hover:border-[#d4af37]/35 hover:bg-white/[0.07]">
                  Browse the whole chapter
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </div>
              <div className="mt-6 flex flex-wrap gap-3">
                {(data.top_situations || []).map((item) => (
                  <Link
                    key={item.slug}
                    to={item.href}
                    className="rounded-full border border-[#d4af37]/16 bg-white/[0.04] px-4 py-2 text-sm text-stone-200 transition hover:border-[#d4af37]/40 hover:text-[#f6dda0]"
                  >
                    {item.label}
                  </Link>
                ))}
              </div>
            </section>

            <FaithPathwayLinks
              theme="gold"
              title="Open a broader guided pathway from this verse"
              body="If this verse resonates but the pressure around it is larger than one page, move into a pathway that connects the verse with Bible, transit, and daily support pages."
            />

            <FaithGrowthPanel
              theme="gold"
              sourceTag={`faith-gita-${situationSlug}`}
              title="Want more Gita guidance around this exact pressure?"
              body="Join the Faith updates list and choose the track you want more help with. This is how we prioritize guided verse journeys, recitation layers, and devotional follow-ups."
            />
          </>
        ) : null}
      </main>

      <Footer />
    </div>
  );
}
