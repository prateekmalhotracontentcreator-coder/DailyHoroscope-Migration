import React from 'react';
import { Link, useParams } from 'react-router-dom';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '../../components/ui/accordion';
import { Footer } from '../../components/Footer';
import { SEO } from '../../components/SEO';
import { ANGEL_NUMBERS, ANGEL_NUMBER_ORDER } from './angelNumberContent';

const SITE = 'https://www.everydayhoroscope.in';

function buildFaq(item) {
  return [
    {
      question: `What does ${item.number} mean?`,
      answer: item.meaning,
    },
    {
      question: `What does ${item.number} mean in love?`,
      answer: item.love,
    },
    {
      question: `Is ${item.number} a lucky number?`,
      answer: `${item.number} is generally read as a supportive sign rather than a lottery symbol. Its message is about ${item.tagline.toLowerCase()}, and the luck comes from aligning with that lesson.`,
    },
    {
      question: `What should I do when I see ${item.number}?`,
      answer: item.what_to_do.join(' '),
    },
  ];
}

function buildSchema(item, faqItems) {
  return {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Article',
        headline: `${item.number} Angel Number Meaning`,
        description: `What does ${item.number} mean? Discover the spiritual meaning of angel number ${item.number} in love, career, and numerology. Vedic insights included.`,
        url: `${SITE}/angel-numbers/${item.number}`,
        author: {
          '@type': 'Organization',
          name: 'Everyday Horoscope',
        },
        publisher: {
          '@type': 'Organization',
          name: 'Everyday Horoscope',
        },
      },
      {
        '@type': 'FAQPage',
        mainEntity: faqItems.map((faq) => ({
          '@type': 'Question',
          name: faq.question,
          acceptedAnswer: {
            '@type': 'Answer',
            text: faq.answer,
          },
        })),
      },
    ],
  };
}

function getRelatedNumbers(number) {
  const index = ANGEL_NUMBER_ORDER.indexOf(number);
  if (index === -1) return ANGEL_NUMBER_ORDER.slice(0, 3);

  const candidates = [];
  [-1, 1, -2, 2, -3, 3].forEach((offset) => {
    const next = ANGEL_NUMBER_ORDER[index + offset];
    if (next && !candidates.includes(next)) {
      candidates.push(next);
    }
  });
  return candidates.slice(0, 3);
}

export function AngelNumberPage() {
  const { number = '' } = useParams();
  const item = ANGEL_NUMBERS[number];

  if (!item) {
    return (
      <div className="min-h-screen bg-[linear-gradient(180deg,#fcfaf5_0%,#f5efe3_55%,#efe7d6_100%)] text-stone-900">
        <SEO
          title="Angel Number Not Found"
          description="Browse the full angel numbers hub to explore meaning pages."
          url={`${SITE}/angel-numbers`}
          noindex
        />
        <main className="mx-auto flex min-h-[70vh] max-w-3xl flex-col items-center justify-center px-4 text-center">
          <p className="text-xs font-semibold uppercase tracking-[0.28em] text-gold">Angel Numbers</p>
          <h1 className="mt-4 font-cinzel text-4xl font-semibold text-stone-900">Number not found</h1>
          <p className="mt-4 max-w-xl text-sm leading-7 text-stone-600">
            This angel number page is not part of the current hub. You can still explore the full list of published numbers below.
          </p>
          <Link
            to="/angel-numbers"
            className="mt-6 inline-flex rounded-full bg-gold px-6 py-3 text-sm font-semibold text-stone-950"
          >
            View angel numbers hub
          </Link>
        </main>
        <Footer />
      </div>
    );
  }

  const faqItems = buildFaq(item);
  const related = getRelatedNumbers(item.number).map((entry) => ANGEL_NUMBERS[entry]);

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,rgba(201,150,31,0.18),transparent_26%),linear-gradient(180deg,#fcfaf5_0%,#f5efe3_55%,#efe7d6_100%)] text-stone-900">
      <SEO
        title={`${item.number} Angel Number Meaning - ${item.tagline}`}
        description={`What does ${item.number} mean? Discover the spiritual meaning of angel number ${item.number} in love, career, and numerology. Vedic insights included.`}
        url={`${SITE}/angel-numbers/${item.number}`}
        schema={buildSchema(item, faqItems)}
      />

      <main className="mx-auto max-w-6xl px-4 py-12 sm:px-6 lg:px-8">
        <nav className="text-sm text-stone-500">
          <Link to="/angel-numbers" className="transition hover:text-gold">
            Angel Numbers
          </Link>
          <span className="mx-2">/</span>
          <span>{item.number}</span>
        </nav>

        <section className="mt-5 rounded-[2rem] border border-gold/20 bg-white/70 p-8 shadow-sm backdrop-blur sm:p-10">
          <div className="flex flex-col gap-6 md:flex-row md:items-end md:justify-between">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.28em] text-gold">Angel Number Meaning</p>
              <h1 className="mt-4 font-cinzel text-6xl font-semibold leading-none text-stone-900 sm:text-8xl">
                {item.number}
              </h1>
              <p className="mt-4 font-playfair text-2xl italic text-stone-700">{item.tagline}</p>
            </div>
            <div className="rounded-[1.5rem] border border-gold/20 bg-gradient-to-br from-white/90 to-gold/10 px-6 py-5 text-right">
              <p className="text-xs font-semibold uppercase tracking-[0.2em] text-gold">Vedic connection</p>
              <p className="mt-3 text-lg font-semibold text-stone-800">{item.vedic_connection}</p>
            </div>
          </div>
        </section>

        <section className="mt-8 grid gap-6 lg:grid-cols-[1.15fr_0.85fr]">
          <article className="rounded-[1.75rem] border border-gold/20 bg-white/80 p-6 shadow-sm">
            <h2 className="font-playfair text-2xl font-semibold text-stone-900">Main meaning</h2>
            <p className="mt-4 text-sm leading-8 text-stone-600">{item.meaning}</p>
          </article>

          <article className="rounded-[1.75rem] border border-gold/20 bg-white/80 p-6 shadow-sm">
            <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">In Vedic numerology</p>
            <p className="mt-4 text-sm leading-8 text-stone-600">{item.spiritual}</p>
            <div className="mt-6 rounded-2xl border border-gold/20 bg-gold/5 p-4">
              <p className="text-xs font-semibold uppercase tracking-[0.2em] text-gold">Base number</p>
              <p className="mt-2 text-2xl font-cinzel text-stone-900">{item.numerology_base}</p>
            </div>
          </article>
        </section>

        <section className="mt-8 grid gap-5 md:grid-cols-3">
          {[
            ['In love', item.love],
            ['In career', item.career],
            ['Spiritual note', item.spiritual],
          ].map(([title, body]) => (
            <article key={title} className="rounded-[1.75rem] border border-gold/20 bg-white/80 p-6 shadow-sm">
              <h2 className="font-playfair text-xl font-semibold text-stone-900">{title}</h2>
              <p className="mt-3 text-sm leading-7 text-stone-600">{body}</p>
            </article>
          ))}
        </section>

        <section className="mt-8 rounded-[1.75rem] border border-gold/20 bg-white/80 p-6 shadow-sm">
          <h2 className="font-playfair text-2xl font-semibold text-stone-900">
            What to do when you see {item.number}
          </h2>
          <ul className="mt-5 grid gap-4 md:grid-cols-2">
            {item.what_to_do.map((step) => (
              <li key={step} className="flex gap-3 rounded-2xl border border-gold/15 bg-gold/5 p-4 text-sm leading-7 text-stone-600">
                <span className="font-semibold text-gold">✓</span>
                <span>{step}</span>
              </li>
            ))}
          </ul>
        </section>

        <section className="mt-8 rounded-[1.75rem] border border-gold/20 bg-white/80 p-6 shadow-sm">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <h2 className="font-playfair text-2xl font-semibold text-stone-900">Related angel numbers</h2>
              <p className="mt-2 text-sm text-stone-600">Explore the neighbouring signals around this message.</p>
            </div>
            <Link to="/angel-numbers" className="text-sm font-semibold text-gold transition hover:opacity-80">
              View full hub
            </Link>
          </div>
          <div className="mt-5 flex flex-wrap gap-3">
            {related.map((entry) => (
              <Link
                key={entry.number}
                to={`/angel-numbers/${entry.number}`}
                className="rounded-full border border-gold/20 bg-gold/10 px-4 py-2 text-sm font-semibold text-gold transition hover:bg-gold hover:text-stone-950"
              >
                {entry.number} - {entry.tagline}
              </Link>
            ))}
          </div>
        </section>

        <section className="mt-8 rounded-[1.75rem] border border-gold/20 bg-white/80 p-6 shadow-sm">
          <h2 className="font-playfair text-2xl font-semibold text-stone-900">Frequently asked questions</h2>
          <Accordion type="single" collapsible className="mt-4">
            {faqItems.map((faq) => (
              <AccordionItem key={faq.question} value={faq.question}>
                <AccordionTrigger className="text-left text-base font-semibold text-stone-900">
                  {faq.question}
                </AccordionTrigger>
                <AccordionContent className="text-sm leading-7 text-stone-600">
                  {faq.answer}
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </section>

        <section className="mt-8 rounded-[2rem] border border-gold/20 bg-gradient-to-br from-gold/10 via-white/80 to-white/80 p-8 text-center shadow-sm">
          <h2 className="font-playfair text-2xl font-semibold text-stone-900">
            Your numerology numbers reveal the deeper pattern behind the signs.
          </h2>
          <p className="mx-auto mt-3 max-w-2xl text-sm leading-7 text-stone-600">
            Angel numbers show what keeps calling for your attention. A full numerology reading shows the core design of your life path, name vibration, and relationship timing.
          </p>
          <Link
            to="/numerology"
            className="mt-6 inline-flex rounded-full bg-gold px-6 py-3 text-sm font-semibold text-stone-950 transition hover:opacity-90"
          >
            Explore my numerology
          </Link>
        </section>
      </main>

      <Footer />
    </div>
  );
}

export default AngelNumberPage;
