import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { ArrowLeft, BookHeart, LoaderCircle, Sparkles } from 'lucide-react';
import { Footer } from '../../components/Footer';
import { SEO } from '../../components/SEO';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '../../components/ui/accordion';
import { API, SITE, buildArticleSchema, buildBreadcrumbSchema, buildFaqSchema } from './faithShared';
import { FaithGrowthPanel } from './FaithGrowthPanel';

function buildSchema(data) {
  if (!data) return null;
  return {
    '@context': 'https://schema.org',
    '@graph': [
      buildArticleSchema({
        headline: data.hero_title,
        description: data.meta_description,
        url: `${SITE}/faith/gita/recitation`,
        about: {
          '@type': 'Book',
          name: 'Bhagavad Gita',
        },
      }),
      buildFaqSchema(data.faq || []),
      buildBreadcrumbSchema([
        { name: 'Home', url: SITE },
        { name: 'Faith Hubs', url: `${SITE}/faith` },
        { name: 'Gita', url: `${SITE}/faith/gita` },
        { name: 'Recitation Mode', url: `${SITE}/faith/gita/recitation` },
      ]),
    ],
  };
}

export function FaithGitaRecitationPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let ignore = false;

    async function fetchPage() {
      try {
        setLoading(true);
        setError('');
        const response = await axios.get(`${API}/gita/recitation`);
        if (!ignore) setData(response.data);
      } catch {
        if (!ignore) {
          setData(null);
          setError('Unable to load Gita recitation mode right now.');
        }
      } finally {
        if (!ignore) setLoading(false);
      }
    }

    fetchPage();
    return () => {
      ignore = true;
    };
  }, []);

  const schema = useMemo(() => buildSchema(data), [data]);

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,rgba(255,214,102,0.14),transparent_28%),linear-gradient(180deg,#0d1015_0%,#141a22_42%,#1f2731_100%)] text-stone-100">
      <SEO
        title={data?.meta_title || 'Bhagavad Gita Recitation Mode'}
        description={data?.meta_description || 'A featured Bhagavad Gita recitation set for devotional repetition.'}
        url={`${SITE}/faith/gita/recitation`}
        schema={schema}
      />

      <main className="mx-auto max-w-6xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="mb-6 flex items-center gap-2 text-sm text-stone-400">
          <Link to="/faith" className="transition hover:text-[#f3d27a]">Faith Hubs</Link>
          <span>/</span>
          <Link to="/faith/gita" className="transition hover:text-[#f3d27a]">Gita</Link>
          <span>/</span>
          <span className="text-stone-200">Recitation Mode</span>
        </div>

        <Link to="/faith/gita" className="mb-6 inline-flex items-center text-sm font-medium text-stone-400 transition hover:text-[#f3d27a]">
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Gita hub
        </Link>

        {loading ? (
          <div className="flex items-center justify-center rounded-[2rem] border border-[#d4af37]/20 bg-white/[0.05] p-12 text-stone-300">
            <LoaderCircle className="mr-3 h-5 w-5 animate-spin text-[#f3d27a]" />
            Loading recitation mode...
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
                    Featured Verse Set
                  </div>
                  <h1 className="mt-5 font-cinzel text-4xl font-semibold leading-tight text-stone-50 sm:text-5xl">{data.hero_title}</h1>
                  <p className="mt-5 max-w-3xl text-base leading-8 text-stone-300">{data.hero_body}</p>
                </div>
                <div className="rounded-[1.5rem] border border-[#d4af37]/18 bg-[#d4af37]/10 px-5 py-4 text-sm">
                  <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[#f3d27a]">Practice note</p>
                  <p className="mt-2 max-w-xs text-stone-300">Slow repetition first, interpretation second. The goal here is steadiness, not speed.</p>
                </div>
              </div>
            </section>

            <section className="mt-8 rounded-[1.8rem] border border-[#d4af37]/18 bg-white/[0.05] p-7">
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[#f3d27a]">How to use it</p>
              <div className="mt-5 grid gap-4 md:grid-cols-3">
                {(data.intro_steps || []).map((item) => (
                  <div key={item} className="rounded-[1.35rem] border border-[#d4af37]/16 bg-white/[0.04] px-5 py-5 text-sm leading-7 text-stone-300">
                    {item}
                  </div>
                ))}
              </div>
            </section>

            <section className="mt-8 grid gap-5">
              {(data.featured_verses || []).map((item) => (
                <article key={item.reference} className="rounded-[1.8rem] border border-[#d4af37]/18 bg-white/[0.05] p-7">
                  <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
                    <div className="max-w-3xl">
                      <div className="inline-flex items-center gap-2 rounded-full border border-[#d4af37]/18 bg-white/[0.04] px-3 py-1 text-xs font-semibold uppercase tracking-[0.18em] text-[#f3d27a]">
                        <Sparkles className="h-3.5 w-3.5" />
                        {item.focus}
                      </div>
                      <h2 className="mt-4 font-cinzel text-3xl font-semibold text-stone-50">{item.reference}</h2>
                      <p className="mt-4 text-sm leading-8 text-stone-300">{item.why}</p>
                    </div>
                    <Link to={item.href} className="inline-flex rounded-full bg-[#d4af37] px-5 py-3 text-sm font-semibold text-stone-950 transition hover:opacity-90">
                      Open verse page
                    </Link>
                  </div>

                  <div className="mt-6 grid gap-6 lg:grid-cols-[1.05fr_0.95fr]">
                    <article className="rounded-[1.5rem] border border-[#d4af37]/16 bg-white/[0.04] p-6">
                      <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[#f3d27a]">Recitation lines</p>
                      <div className="mt-4 space-y-3">
                        {(item.display_lines || []).map((line) => (
                          <p key={line} className="font-playfair text-xl leading-9 text-stone-50">{line}</p>
                        ))}
                      </div>
                    </article>

                    <article className="rounded-[1.5rem] border border-[#d4af37]/16 bg-white/[0.04] p-6">
                      <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[#f3d27a]">Practice window</p>
                      <p className="mt-4 text-sm leading-8 text-stone-300">{item.practice_window}</p>
                      <p className="mt-5 text-sm leading-8 text-stone-200">{item.translation}</p>
                    </article>
                  </div>
                </article>
              ))}
            </section>

            <section className="mt-8 rounded-[1.8rem] border border-[#d4af37]/18 bg-white/[0.05] p-7">
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[#f3d27a]">FAQ</p>
              <Accordion type="single" collapsible className="mt-4 space-y-3">
                {(data.faq || []).map((item, index) => (
                  <AccordionItem key={item.q} value={`faq-${index}`} className="rounded-[1.1rem] border border-[#d4af37]/16 bg-white/[0.04] px-4">
                    <AccordionTrigger className="text-left text-sm font-semibold text-stone-100">{item.q}</AccordionTrigger>
                    <AccordionContent className="text-sm leading-7 text-stone-300">{item.a}</AccordionContent>
                  </AccordionItem>
                ))}
              </Accordion>
            </section>

            <FaithGrowthPanel
              theme="gold"
              sourceTag="faith-gita-recitation"
              title="Want more guided recitation tracks?"
              body="Join the Faith updates list if you want chapter-based chanting plans, themed recitation sets, and devotional follow-ups built around repetition."
            />
          </>
        ) : null}
      </main>

      <Footer />
    </div>
  );
}
