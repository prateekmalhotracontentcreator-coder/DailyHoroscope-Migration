import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { LoaderCircle, Sparkles } from 'lucide-react';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '../../components/ui/accordion';
import { Footer } from '../../components/Footer';
import { SEO } from '../../components/SEO';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api/seo/zibu/symbols`;
const SITE = 'https://www.everydayhoroscope.in';

const CATEGORY_ORDER = [
  { key: 'all', label: 'All 88' },
  { key: 'love', label: 'Love' },
  { key: 'abundance', label: 'Abundance' },
  { key: 'healing', label: 'Healing' },
  { key: 'protection', label: 'Protection' },
  { key: 'spiritual', label: 'Spiritual' },
  { key: 'peace', label: 'Peace' },
  { key: 'manifestation', label: 'Manifestation' },
];

const CATEGORY_STYLES = {
  love: 'border-rose-400/25 bg-rose-500/10 text-rose-200',
  abundance: 'border-amber-400/25 bg-amber-500/10 text-amber-200',
  healing: 'border-emerald-400/25 bg-emerald-500/10 text-emerald-200',
  protection: 'border-sky-400/25 bg-sky-500/10 text-sky-200',
  spiritual: 'border-violet-400/25 bg-violet-500/10 text-violet-200',
  peace: 'border-teal-400/25 bg-teal-500/10 text-teal-200',
  manifestation: 'border-fuchsia-400/25 bg-fuchsia-500/10 text-fuchsia-200',
};

const FAQ_ITEMS = [
  {
    question: 'What are Zibu Symbols?',
    answer: 'Zibu Symbols are spiritual intention symbols used in meditation, manifestation, journaling, and personal ritual work. People often work with them as visual anchors for qualities such as peace, healing, courage, or abundance.',
  },
  {
    question: 'Do Zibu Symbols work?',
    answer: 'Their value is usually experiential rather than mechanical. Many people find that symbols help them focus attention, deepen ritual consistency, and stay emotionally aligned with the intention they are practicing.',
  },
  {
    question: 'How do you draw Zibu Symbols?',
    answer: 'Traditionally, people draw or trace a symbol slowly while holding a clear intention. The goal is not artistic perfection but presence, repetition, and sincere focus.',
  },
  {
    question: 'Are Zibu Symbols safe to work with?',
    answer: 'For most people, they function like other reflective spiritual tools: journaling prompts, meditation objects, or symbolic prayer aids. It is wise to use them as supportive ritual elements, not as substitutes for medical, mental-health, or legal care.',
  },
  {
    question: 'Who created Zibu Symbols?',
    answer: 'Zibu Symbols are associated with Debbie Zylstra Almstedt. On this page, the symbol names are used as factual reference while all explanatory text is original writing created for EverydayHoroscope.',
  },
];

function buildSchema(symbols) {
  return {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'BreadcrumbList',
        itemListElement: [
          {
            '@type': 'ListItem',
            position: 1,
            name: 'Home',
            item: SITE,
          },
          {
            '@type': 'ListItem',
            position: 2,
            name: 'Zibu Symbols',
            item: `${SITE}/zibu`,
          },
        ],
      },
      {
        '@type': 'FAQPage',
        mainEntity: FAQ_ITEMS.map((item) => ({
          '@type': 'Question',
          name: item.question,
          acceptedAnswer: {
            '@type': 'Answer',
            text: item.answer,
          },
        })),
      },
      {
        '@type': 'CollectionPage',
        name: 'Zibu Symbols',
        url: `${SITE}/zibu`,
        description: 'Explore all 88 Zibu angelic symbols for manifestation, healing, peace, and abundance.',
        mainEntity: {
          '@type': 'ItemList',
          itemListElement: symbols.slice(0, 88).map((symbol, index) => ({
            '@type': 'ListItem',
            position: index + 1,
            name: symbol.display_name,
            url: `${SITE}/zibu/${symbol.slug}`,
          })),
        },
      },
    ],
  };
}

export function ZibuHubPage() {
  const [symbols, setSymbols] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeCategory, setActiveCategory] = useState('all');

  useEffect(() => {
    let ignore = false;

    async function fetchSymbols() {
      try {
        setLoading(true);
        setError('');
        const response = await axios.get(API);
        if (!ignore) {
          setSymbols(response.data?.symbols || []);
        }
      } catch {
        if (!ignore) {
          setSymbols([]);
          setError('Unable to load Zibu symbols right now.');
        }
      } finally {
        if (!ignore) {
          setLoading(false);
        }
      }
    }

    fetchSymbols();
    return () => {
      ignore = true;
    };
  }, []);

  const visibleSymbols = useMemo(() => {
    if (activeCategory === 'all') {
      return symbols;
    }
    return symbols.filter((symbol) => symbol.category === activeCategory);
  }, [activeCategory, symbols]);

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,rgba(197,160,89,0.2),transparent_32%),linear-gradient(180deg,#110f0a_0%,#19140e_38%,#221b14_100%)] text-stone-100">
      <SEO
        title="Zibu Symbols - 88 Angelic Symbols for Love, Abundance and Healing"
        description="Explore all 88 Zibu angelic symbols. Find the right symbol for love, abundance, protection, healing, and manifestation with original meanings and practical guidance."
        url={`${SITE}/zibu`}
        schema={buildSchema(symbols)}
      />

      <main className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <section className="relative overflow-hidden rounded-[2rem] border border-gold/20 bg-white/[0.06] p-8 shadow-[0_20px_80px_rgba(0,0,0,0.28)] backdrop-blur md:p-10">
          <div className="absolute inset-y-0 right-0 hidden w-1/3 bg-[radial-gradient(circle_at_center,rgba(197,160,89,0.18),transparent_62%)] lg:block" />
          <div className="relative max-w-3xl">
            <div className="inline-flex items-center gap-2 rounded-full border border-gold/30 bg-gold/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.24em] text-gold">
              <Sparkles className="h-3.5 w-3.5" />
              Angelic Symbol Library
            </div>
            <h1 className="mt-5 font-cinzel text-4xl font-semibold leading-tight text-stone-50 sm:text-5xl">
              Zibu Symbols - 88 Angelic Symbols for Manifestation and Healing
            </h1>
            <p className="mt-5 max-w-2xl text-base leading-8 text-stone-300">
              Zibu Symbols are often used as contemplative anchors for prayer, meditation, manifestation, and emotional healing. Each symbol is linked to a specific intention, so the practice becomes less about decoration and more about focusing your energy with care. This hub gathers all 88 symbol names from the source chart and pairs them with original EverydayHoroscope guidance on meaning and use.
            </p>
            <div className="mt-8 flex flex-wrap gap-3 text-sm text-stone-300">
              <span className="rounded-full border border-gold/20 bg-white/[0.04] px-4 py-2">89 SEO pages</span>
              <span className="rounded-full border border-gold/20 bg-white/[0.04] px-4 py-2">7 filter groups</span>
              <span className="rounded-full border border-gold/20 bg-white/[0.04] px-4 py-2">Original meanings and affirmations</span>
            </div>
          </div>
        </section>

        <section className="mt-8 rounded-[2rem] border border-gold/20 bg-white/[0.05] p-6 backdrop-blur">
          <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">Browse by intention</p>
              <h2 className="mt-2 font-playfair text-2xl font-semibold text-stone-50">Find the symbol that matches the energy you want to work with.</h2>
            </div>
            <p className="max-w-xl text-sm leading-7 text-stone-300">
              Use the tabs below to move between relationship, abundance, healing, protection, spiritual, peace, and manifestation themes.
            </p>
          </div>

          <div className="mt-6 flex flex-wrap gap-2">
            {CATEGORY_ORDER.map((item) => {
              const active = activeCategory === item.key;
              return (
                <button
                  key={item.key}
                  type="button"
                  onClick={() => setActiveCategory(item.key)}
                  className={`rounded-full border px-4 py-2 text-sm font-semibold transition ${
                    active
                      ? 'border-gold bg-gold text-stone-950'
                      : 'border-gold/20 bg-white/[0.04] text-stone-200 hover:border-gold/40 hover:bg-gold/10'
                  }`}
                >
                  {item.label}
                </button>
              );
            })}
          </div>
        </section>

        <section className="mt-8">
          {loading ? (
            <div className="flex items-center justify-center rounded-[2rem] border border-gold/20 bg-white/[0.05] p-10 text-stone-300">
              <LoaderCircle className="mr-3 h-5 w-5 animate-spin text-gold" />
              Loading the Zibu symbol library...
            </div>
          ) : error ? (
            <div className="rounded-[2rem] border border-red-400/25 bg-red-500/10 p-6 text-sm text-red-200">
              {error}
            </div>
          ) : (
            <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
              {visibleSymbols.map((symbol) => (
                <Link
                  key={symbol.slug}
                  to={`/zibu/${symbol.slug}`}
                  className="group rounded-[1.75rem] border border-gold/20 bg-white/[0.05] p-6 shadow-sm transition-all hover:-translate-y-1 hover:border-gold/40 hover:bg-white/[0.08]"
                >
                  <div className="flex items-start justify-between gap-4">
                    <div>
                      <p className="text-xs font-semibold uppercase tracking-[0.2em] text-gold">
                        Symbol {symbol.symbol_number}
                      </p>
                      <h3 className="mt-3 font-cinzel text-2xl font-semibold leading-tight text-stone-50">
                        {symbol.intention}
                      </h3>
                    </div>
                    <span className={`inline-flex rounded-full border px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.16em] ${CATEGORY_STYLES[symbol.category] || 'border-gold/20 bg-gold/10 text-gold'}`}>
                      {symbol.category_short_label}
                    </span>
                  </div>
                  <p className="mt-4 text-sm leading-7 text-stone-300">{symbol.tagline}</p>
                  <p className="mt-5 text-sm font-semibold text-gold transition group-hover:text-gold/80">
                    Read meaning and ritual guidance
                  </p>
                </Link>
              ))}
            </div>
          )}
        </section>

        <section className="mt-10 grid gap-6 lg:grid-cols-[0.95fr_1.05fr]">
          <article className="rounded-[2rem] border border-gold/20 bg-white/[0.05] p-7 backdrop-blur">
            <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">How to use Zibu Symbols</p>
            <h2 className="mt-3 font-playfair text-2xl font-semibold text-stone-50">A simple four-step ritual</h2>
            <div className="mt-6 grid gap-4">
              {[
                ['1. Intention', 'Choose one symbol and name exactly what you want to invite, soften, protect, or release.'],
                ['2. Draw', 'Sketch or trace the symbol slowly in a journal, on a card, or with your finger in the air.'],
                ['3. Visualise', 'Imagine the symbol filling with warm gold light and carrying your intention into your body and surroundings.'],
                ['4. Release', 'Repeat a brief affirmation, then let the symbol hold the prayer while you return to grounded action.'],
              ].map(([title, body]) => (
                <div key={title} className="rounded-2xl border border-gold/15 bg-gold/[0.05] p-4">
                  <h3 className="font-semibold text-stone-50">{title}</h3>
                  <p className="mt-2 text-sm leading-7 text-stone-300">{body}</p>
                </div>
              ))}
            </div>
          </article>

          <article className="rounded-[2rem] border border-gold/20 bg-[linear-gradient(160deg,rgba(197,160,89,0.14),rgba(255,255,255,0.04))] p-7 backdrop-blur">
            <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">Important note</p>
            <h2 className="mt-3 font-playfair text-2xl font-semibold text-stone-50">Use symbols as supportive ritual tools, not replacements for real-world care.</h2>
            <p className="mt-4 text-sm leading-7 text-stone-200">
              A symbol can help focus the mind, steady emotions, and deepen a spiritual practice. It cannot replace medical treatment, therapy, financial planning, or legal advice. The most grounded use is to let the symbol clarify your energy while your practical actions handle the rest.
            </p>
            <div className="mt-6 rounded-2xl border border-gold/20 bg-black/10 p-5">
              <p className="text-sm leading-7 text-stone-200">
                Copyright note: the original symbol names are used as factual reference. This hub does not reproduce the copyrighted symbol drawings; instead, each page uses original text guidance and abstract placeholder art.
              </p>
            </div>
          </article>
        </section>

        <section className="mt-10 rounded-[2rem] border border-gold/20 bg-white/[0.05] p-7 backdrop-blur">
          <h2 className="font-playfair text-2xl font-semibold text-stone-50">Frequently asked questions</h2>
          <Accordion type="single" collapsible className="mt-4">
            {FAQ_ITEMS.map((item) => (
              <AccordionItem key={item.question} value={item.question} className="border-gold/15">
                <AccordionTrigger className="text-left text-base font-semibold text-stone-50">
                  {item.question}
                </AccordionTrigger>
                <AccordionContent className="text-sm leading-7 text-stone-300">
                  {item.answer}
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </section>
      </main>

      <Footer />
    </div>
  );
}

export default ZibuHubPage;
