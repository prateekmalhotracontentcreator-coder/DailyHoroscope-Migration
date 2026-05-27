import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Compass } from 'lucide-react';
import { FEATURED_FAITH_COLLECTIONS } from './faithCollections';

export function FaithPathwayLinks({
  title = 'Guided pathways',
  body = 'Use a curated pathway when you want a smaller, more intentional starting point than the full Faith library.',
  items = FEATURED_FAITH_COLLECTIONS,
  theme = 'gold',
}) {
  const palettes = {
    gold: {
      border: 'border-[#d4af37]/18',
      badge: 'text-[#f3d27a]',
      link: 'border-[#d4af37]/16 hover:border-[#d4af37]/35',
    },
    emerald: {
      border: 'border-emerald-300/18',
      badge: 'text-emerald-200',
      link: 'border-emerald-300/16 hover:border-emerald-300/35',
    },
    sky: {
      border: 'border-sky-300/18',
      badge: 'text-sky-200',
      link: 'border-sky-300/16 hover:border-sky-300/35',
    },
  };
  const palette = palettes[theme] || palettes.gold;

  return (
    <section className={`mt-8 rounded-[1.8rem] border bg-white/[0.05] p-7 ${palette.border}`}>
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <p className={`text-xs font-semibold uppercase tracking-[0.24em] ${palette.badge}`}>
            <Compass className="mr-2 inline h-4 w-4" />
            Guided pathways
          </p>
          <h2 className="mt-2 font-playfair text-2xl font-semibold text-stone-50">{title}</h2>
          <p className="mt-3 max-w-2xl text-sm leading-7 text-stone-300">{body}</p>
        </div>
        <Link
          to="/faith/pathways"
          className="inline-flex items-center rounded-full border border-white/10 bg-white/[0.04] px-5 py-3 text-sm font-semibold text-stone-100 transition hover:bg-white/[0.07]"
        >
          Browse all pathways
          <ArrowRight className="ml-2 h-4 w-4" />
        </Link>
      </div>
      <div className="mt-6 grid gap-4 md:grid-cols-3">
        {items.map((item) => (
          <Link
            key={item.slug}
            to={`/faith/pathways/${item.slug}`}
            className={`rounded-[1.3rem] border bg-white/[0.04] px-5 py-5 transition ${palette.link}`}
          >
            <p className={`text-xs font-semibold uppercase tracking-[0.18em] ${palette.badge}`}>{item.eyebrow}</p>
            <p className="mt-3 font-semibold text-stone-100">{item.title}</p>
            <p className="mt-3 text-sm leading-7 text-stone-300">{item.description}</p>
          </Link>
        ))}
      </div>
    </section>
  );
}
