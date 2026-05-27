import React, { useMemo } from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft, ArrowRight, Compass, Sparkles } from 'lucide-react';
import { Footer } from '../../components/Footer';
import { SEO } from '../../components/SEO';
import { SITE, buildBreadcrumbSchema, buildCollectionSchema } from './faithShared';
import { FAITH_COLLECTIONS } from './faithCollections';
import { FaithGrowthPanel } from './FaithGrowthPanel';

function buildSchema() {
  return {
    '@context': 'https://schema.org',
    '@graph': [
      buildCollectionSchema({
        name: 'Faith Guided Pathways',
        description: 'Curated Faith pathways that group Gita, Bible, transit, and daily pages around one life concern.',
        url: `${SITE}/faith/pathways`,
        items: FAITH_COLLECTIONS.map((item) => ({ name: item.title, url: `${SITE}/faith/pathways/${item.slug}` })),
      }),
      buildBreadcrumbSchema([
        { name: 'Home', url: SITE },
        { name: 'Faith Hubs', url: `${SITE}/faith` },
        { name: 'Guided Pathways', url: `${SITE}/faith/pathways` },
      ]),
    ],
  };
}

export function FaithCollectionsHubPage() {
  const schema = useMemo(() => buildSchema(), []);

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,rgba(227,179,74,0.16),transparent_28%),linear-gradient(180deg,#0d1015_0%,#141a22_42%,#1f2731_100%)] text-stone-100">
      <SEO
        title="Faith Guided Pathways"
        description="Curated Faith pathways for anxiety, career resets, grief, Mercury retrograde, relationship healing, and new beginnings."
        url={`${SITE}/faith/pathways`}
        schema={schema}
      />

      <main className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="mb-6 flex items-center gap-2 text-sm text-stone-400">
          <Link to="/faith" className="transition hover:text-[#f3d27a]">Faith Hubs</Link>
          <span>/</span>
          <span className="text-stone-200">Guided Pathways</span>
        </div>

        <Link to="/faith" className="mb-6 inline-flex items-center text-sm font-medium text-stone-400 transition hover:text-[#f3d27a]">
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Faith Hubs
        </Link>

        <section className="rounded-[2rem] border border-[#d4af37]/20 bg-white/[0.05] p-8 shadow-[0_24px_80px_rgba(0,0,0,0.28)] backdrop-blur">
          <div className="inline-flex items-center gap-2 rounded-full border border-[#d4af37]/25 bg-[#d4af37]/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.24em] text-[#f3d27a]">
            <Compass className="h-3.5 w-3.5" />
            Guided Pathways
          </div>
          <h1 className="mt-5 font-cinzel text-4xl font-semibold leading-tight text-stone-50 sm:text-5xl">
            Start from the life issue, not just the scripture library.
          </h1>
          <p className="mt-5 max-w-3xl text-base leading-8 text-stone-300">
            These curated entry pages are built for readers who need a cleaner starting point. Each pathway groups Gita, Bible, transit, and daily Faith pages around one real concern so the reader can move forward without guessing where to begin.
          </p>
        </section>

        <section className="mt-8 grid gap-5 lg:grid-cols-2 xl:grid-cols-3">
          {FAITH_COLLECTIONS.map((item) => (
            <article key={item.slug} className="rounded-[1.8rem] border border-[#d4af37]/18 bg-white/[0.05] p-6">
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[#f3d27a]">{item.eyebrow}</p>
              <h2 className="mt-3 font-playfair text-2xl font-semibold text-stone-50">{item.title}</h2>
              <p className="mt-4 text-sm leading-7 text-stone-300">{item.description}</p>
              <div className="mt-5 space-y-3">
                {item.primaryLinks.slice(0, 2).map((linkItem) => (
                  <Link
                    key={linkItem.href}
                    to={linkItem.href}
                    className="block rounded-[1.2rem] border border-[#d4af37]/16 bg-white/[0.04] px-4 py-4 text-sm transition hover:border-[#d4af37]/35 hover:bg-white/[0.07]"
                  >
                    <p className="font-semibold text-stone-100">{linkItem.label}</p>
                    <p className="mt-2 text-stone-300">{linkItem.note}</p>
                  </Link>
                ))}
              </div>
              <Link to={`/faith/pathways/${item.slug}`} className="mt-6 inline-flex items-center text-sm font-semibold text-[#f3d27a]">
                Open pathway
                <ArrowRight className="ml-2 h-4 w-4" />
              </Link>
            </article>
          ))}
        </section>

        <FaithGrowthPanel
          theme="gold"
          sourceTag="faith-pathways-hub"
          title="Build devotional follow-ups from real reader intent"
          body="This pathway layer is meant to surface what people actually need first. Join the Faith updates list and choose the concern you want more guidance around."
        />
      </main>

      <Footer />
    </div>
  );
}
