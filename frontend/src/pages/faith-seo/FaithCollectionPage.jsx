import React, { useMemo } from 'react';
import { Link, useParams } from 'react-router-dom';
import { ArrowLeft, ArrowRight, Compass, Sparkles } from 'lucide-react';
import { Footer } from '../../components/Footer';
import { SEO } from '../../components/SEO';
import { SITE, buildBreadcrumbSchema, buildCollectionSchema, titleCaseSlug } from './faithShared';
import { getFaithCollection } from './faithCollections';
import { FaithGrowthPanel } from './FaithGrowthPanel';

function buildSchema(item) {
  if (!item) return null;
  return {
    '@context': 'https://schema.org',
    '@graph': [
      buildCollectionSchema({
        name: item.title,
        description: item.description,
        url: `${SITE}/faith/pathways/${item.slug}`,
        items: item.primaryLinks.map((linkItem) => ({ name: linkItem.label, url: `${SITE}${linkItem.href}` })),
      }),
      buildBreadcrumbSchema([
        { name: 'Home', url: SITE },
        { name: 'Faith Hubs', url: `${SITE}/faith` },
        { name: 'Guided Pathways', url: `${SITE}/faith/pathways` },
        { name: item.title, url: `${SITE}/faith/pathways/${item.slug}` },
      ]),
    ],
  };
}

export function FaithCollectionPage() {
  const { collectionSlug = '' } = useParams();
  const item = useMemo(() => getFaithCollection(collectionSlug), [collectionSlug]);
  const schema = useMemo(() => buildSchema(item), [item]);

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,rgba(227,179,74,0.16),transparent_28%),linear-gradient(180deg,#0d1015_0%,#141a22_42%,#1f2731_100%)] text-stone-100">
      <SEO
        title={item?.title || `${titleCaseSlug(collectionSlug)} Faith Pathway`}
        description={item?.description || 'Guided Faith pathway.'}
        url={`${SITE}/faith/pathways/${collectionSlug}`}
        schema={schema}
        noindex={!item}
      />

      <main className="mx-auto max-w-6xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="mb-6 flex items-center gap-2 text-sm text-stone-400">
          <Link to="/faith" className="transition hover:text-[#f3d27a]">Faith Hubs</Link>
          <span>/</span>
          <Link to="/faith/pathways" className="transition hover:text-[#f3d27a]">Guided Pathways</Link>
          <span>/</span>
          <span className="text-stone-200">{item?.title || titleCaseSlug(collectionSlug)}</span>
        </div>

        <Link to="/faith/pathways" className="mb-6 inline-flex items-center text-sm font-medium text-stone-400 transition hover:text-[#f3d27a]">
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to guided pathways
        </Link>

        {!item ? (
          <div className="rounded-[2rem] border border-red-400/25 bg-red-500/10 p-6 text-sm text-red-200">Faith pathway not found.</div>
        ) : (
          <>
            <section className="rounded-[2rem] border border-[#d4af37]/20 bg-white/[0.05] p-8 shadow-[0_24px_80px_rgba(0,0,0,0.28)] backdrop-blur">
              <div className="flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
                <div className="max-w-3xl">
                  <div className="inline-flex items-center gap-2 rounded-full border border-[#d4af37]/25 bg-[#d4af37]/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.24em] text-[#f3d27a]">
                    <Compass className="h-3.5 w-3.5" />
                    {item.eyebrow}
                  </div>
                  <h1 className="mt-5 font-cinzel text-4xl font-semibold leading-tight text-stone-50 sm:text-5xl">{item.title}</h1>
                  <p className="mt-5 text-base leading-8 text-stone-300">{item.intro}</p>
                </div>
                <div className="rounded-[1.5rem] border border-[#d4af37]/18 bg-[#d4af37]/10 px-5 py-4 text-sm">
                  <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[#f3d27a]">Why this page exists</p>
                  <p className="mt-2 max-w-xs text-stone-300">{item.description}</p>
                </div>
              </div>
            </section>

            <section className="mt-8 rounded-[1.8rem] border border-[#d4af37]/18 bg-white/[0.05] p-7">
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[#f3d27a]">Primary route</p>
              <div className="mt-5 grid gap-4">
                {item.primaryLinks.map((linkItem) => (
                  <Link
                    key={linkItem.href}
                    to={linkItem.href}
                    className="rounded-[1.35rem] border border-[#d4af37]/16 bg-white/[0.04] px-5 py-5 transition hover:border-[#d4af37]/35 hover:bg-white/[0.07]"
                  >
                    <div className="flex items-start justify-between gap-4">
                      <div>
                        <p className="font-semibold text-stone-100">{linkItem.label}</p>
                        <p className="mt-2 text-sm leading-7 text-stone-300">{linkItem.note}</p>
                      </div>
                      <ArrowRight className="mt-1 h-4 w-4 text-[#f3d27a]" />
                    </div>
                  </Link>
                ))}
              </div>
            </section>

            <section className="mt-8 rounded-[1.8rem] border border-[#d4af37]/18 bg-white/[0.05] p-7">
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[#f3d27a]">Support routes</p>
              <div className="mt-5 grid gap-4 md:grid-cols-2">
                {item.supportLinks.map((linkItem) => (
                  <Link
                    key={linkItem.href}
                    to={linkItem.href}
                    className="rounded-[1.25rem] border border-[#d4af37]/16 bg-white/[0.04] px-5 py-5 transition hover:border-[#d4af37]/35 hover:bg-white/[0.07]"
                  >
                    <p className="font-semibold text-stone-100">{linkItem.label}</p>
                    <p className="mt-2 text-sm leading-7 text-stone-300">{linkItem.note}</p>
                  </Link>
                ))}
              </div>
            </section>

            <section className="mt-8 rounded-[1.8rem] border border-[#d4af37]/18 bg-white/[0.05] p-7">
              <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
                <div>
                  <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[#f3d27a]">Next layer</p>
                  <h2 className="mt-2 font-playfair text-2xl font-semibold text-stone-50">Turn this pathway into a repeatable devotional rhythm.</h2>
                  <p className="mt-3 max-w-2xl text-sm leading-7 text-stone-300">
                    When a pathway resonates, the next move is to anchor it in a daily rhythm. Use Lumina for ongoing practice or browse more pathways if the pressure has shifted.
                  </p>
                </div>
                <div className="flex flex-wrap gap-3">
                  <Link to="/lumina" className="inline-flex items-center rounded-full bg-[#d4af37] px-5 py-3 text-sm font-semibold text-stone-950 transition hover:opacity-90">
                    Start in Lumina
                  </Link>
                  <Link to="/faith/pathways" className="inline-flex items-center rounded-full border border-[#d4af37]/18 bg-white/[0.04] px-5 py-3 text-sm font-semibold text-stone-100 transition hover:border-[#d4af37]/35 hover:bg-white/[0.07]">
                    Browse more pathways
                  </Link>
                </div>
              </div>
            </section>

            <FaithGrowthPanel
              theme="gold"
              sourceTag={`faith-pathway-${item.slug}`}
              title="Help us shape the next devotional pathway"
              body="Choose the concern you want more support around and join the Faith updates list. This gives us a real signal for which devotional and email sequences should come next."
            />
          </>
        )}
      </main>

      <Footer />
    </div>
  );
}
