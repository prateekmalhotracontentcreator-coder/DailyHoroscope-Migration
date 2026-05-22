import React from 'react';
import { Link } from 'react-router-dom';
import { Footer } from '../../components/Footer';
import { SEO } from '../../components/SEO';
import { ANGEL_NUMBERS, ANGEL_NUMBER_ORDER } from './angelNumberContent';

const SITE = 'https://www.everydayhoroscope.in';

function buildHubSchema() {
  return {
    '@context': 'https://schema.org',
    '@type': 'ItemList',
    name: 'Angel Numbers',
    itemListElement: ANGEL_NUMBER_ORDER.map((number, index) => ({
      '@type': 'ListItem',
      position: index + 1,
      name: ANGEL_NUMBERS[number].title,
      url: `${SITE}/angel-numbers/${number}`,
    })),
  };
}

export function AngelNumbersHubPage() {
  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,rgba(201,150,31,0.16),transparent_30%),linear-gradient(180deg,#fcfaf5_0%,#f5efe3_55%,#efe7d6_100%)] text-stone-900">
      <SEO
        title="Angel Numbers - Meanings, Signs and Messages"
        description="Complete guide to angel numbers. Discover the meaning of 111, 222, 333, 444, 555, 777, 888, 1111 and more with Vedic numerology insights."
        url={`${SITE}/angel-numbers`}
        schema={buildHubSchema()}
      />

      <main className="mx-auto max-w-6xl px-4 py-12 sm:px-6 lg:px-8">
        <section className="rounded-[2rem] border border-gold/20 bg-white/70 p-8 shadow-sm backdrop-blur sm:p-10">
          <div className="max-w-3xl">
            <p className="text-xs font-semibold uppercase tracking-[0.28em] text-gold">Numerology Content Hub</p>
            <h1 className="mt-4 font-cinzel text-4xl font-semibold tracking-tight text-stone-900 sm:text-5xl">
              Angel Numbers
            </h1>
            <p className="mt-4 text-lg font-playfair italic text-stone-700">
              Meanings, signs, and messages from the Universe.
            </p>
            <p className="mt-4 max-w-2xl text-sm leading-7 text-stone-600">
              Angel numbers are repeating sequences that many people experience during moments of transition, confirmation, or spiritual growth. This hub gathers the most-searched angel numbers and interprets them through a Vedic numerology lens.
            </p>
          </div>
        </section>

        <section className="mt-8 rounded-[2rem] border border-gold/20 bg-white/75 p-6 shadow-sm backdrop-blur">
          <h2 className="font-playfair text-2xl font-semibold text-stone-900">What are angel numbers?</h2>
          <p className="mt-3 max-w-3xl text-sm leading-7 text-stone-600">
            They are repeating number sequences that many people experience as symbolic nudges, confirmations, or energetic check-ins. In this interpretation style, each number carries a distinct message around love, purpose, timing, abundance, or spiritual alignment.
          </p>
        </section>

        <section className="mt-8">
          <div className="mb-5 flex items-end justify-between gap-4">
            <div>
              <h2 className="font-playfair text-2xl font-semibold text-stone-900">Explore every angel number</h2>
              <p className="mt-2 text-sm text-stone-600">Start with the number you keep seeing most often.</p>
            </div>
            <Link
              to="/numerology"
              className="hidden rounded-full border border-gold/30 bg-gold/10 px-4 py-2 text-sm font-semibold text-gold transition hover:bg-gold hover:text-stone-950 sm:inline-flex"
            >
              Explore my numerology
            </Link>
          </div>

          <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
            {ANGEL_NUMBER_ORDER.map((number) => {
              const item = ANGEL_NUMBERS[number];
              return (
                <article
                  key={number}
                  className={`rounded-[1.75rem] border border-gold/15 bg-gradient-to-br ${item.colour} from-white/80 via-white/75 p-6 shadow-sm`}
                >
                  <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">Angel number</p>
                  <div className="mt-3 flex items-start justify-between gap-3">
                    <h3 className="font-cinzel text-5xl font-semibold leading-none text-stone-900">{item.number}</h3>
                    <span className="rounded-full border border-gold/20 bg-white/75 px-3 py-1 text-xs font-medium text-stone-600">
                      {item.icon}
                    </span>
                  </div>
                  <p className="mt-4 font-playfair text-xl italic text-stone-800">{item.tagline}</p>
                  <p className="mt-3 text-sm leading-7 text-stone-600">
                    {item.meaning.split('. ')[0]}.
                  </p>
                  <Link
                    to={`/angel-numbers/${item.number}`}
                    className="mt-5 inline-flex items-center rounded-full bg-gold px-4 py-2 text-sm font-semibold text-stone-950 transition hover:opacity-90"
                  >
                    Read more
                  </Link>
                </article>
              );
            })}
          </div>
        </section>

        <section className="mt-10 rounded-[2rem] border border-gold/20 bg-white/80 p-8 text-center shadow-sm">
          <h2 className="font-playfair text-2xl font-semibold text-stone-900">
            Your personal numerology numbers reveal the deeper pattern.
          </h2>
          <p className="mx-auto mt-3 max-w-2xl text-sm leading-7 text-stone-600">
            Angel numbers show what is being highlighted around you. Your birth date and name numbers show what is wired within you.
          </p>
          <Link
            to="/numerology"
            className="mt-6 inline-flex rounded-full bg-gold px-6 py-3 text-sm font-semibold text-stone-950 transition hover:opacity-90"
          >
            Discover your personal numerology
          </Link>
        </section>
      </main>

      <Footer />
    </div>
  );
}

export default AngelNumbersHubPage;
